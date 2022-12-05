from flask_restful import Resource, marshal_with
import json
import logging
from datetime import datetime
from model.BaseResponse import BaseResponse, resource_fields
from repo.CompanyRepository import CompanyRepository
from repo.ShareHolderRepository import ShareHolderRepository
from repo.CompanyShareHolderRepository import CompanyShareHolderRepository
from model.Scraper import WebDriver
from time import sleep
from symspellpy import SymSpell, Verbosity


class NameChecker(object):
	def __init__(self, name_list):
		self.sym_spell = SymSpell(max_dictionary_edit_distance=2, prefix_length=7)
		
		for each_name in name_list:
			self.sym_spell.create_dictionary_entry(each_name, len(each_name.split(' ')))
		
	def get_name(self, name):
		suggestions = self.sym_spell.lookup(name, Verbosity.CLOSEST, max_edit_distance=2, transfer_casing=True)
		
		if suggestions is not None and len(suggestions) > 0:
			return suggestions[0].term
		
		return name


class Scraping(Resource):
	@marshal_with(resource_fields)
	def get(self):
		response = BaseResponse()
		response.message = 'success'
		response.status = 'success'

		idx_parser = IdxParser()
		
		try:
			idx_parser.parse_companies()
		except Exception as e:
			idx_parser.quit()
			raise e
		
		idx_parser.quit()
		
		return response


class IdxParser(object):
	def __init__(self):
		self.wd = WebDriver()
		
	def quit(self):
		self.wd.quit()
	
	def parse_companies(self):
		stock_list_url = 'https://old.idx.co.id/umbraco/Surface/Helper/GetEmiten?emitenType=s'
		stocks_with_listing_date_url = 'https://old.idx.co.id/umbraco/Surface/ListedCompany/GetCompanyProfiles?draw=1&columns%5B0%5D%5Bdata%5D=KodeEmiten&columns%5B0%5D%5Bname%5D=&columns%5B0%5D%5Bsearchable%5D=true&columns%5B0%5D%5Borderable%5D=false&columns%5B0%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B0%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B1%5D%5Bdata%5D=KodeEmiten&columns%5B1%5D%5Bname%5D=&columns%5B1%5D%5Bsearchable%5D=true&columns%5B1%5D%5Borderable%5D=false&columns%5B1%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B1%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B2%5D%5Bdata%5D=NamaEmiten&columns%5B2%5D%5Bname%5D=&columns%5B2%5D%5Bsearchable%5D=true&columns%5B2%5D%5Borderable%5D=false&columns%5B2%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B2%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B3%5D%5Bdata%5D=TanggalPencatatan&columns%5B3%5D%5Bname%5D=&columns%5B3%5D%5Bsearchable%5D=true&columns%5B3%5D%5Borderable%5D=false&columns%5B3%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B3%5D%5Bsearch%5D%5Bregex%5D=false&start=0&search%5Bvalue%5D=&search%5Bregex%5D=false&_=1618490554596&length='
		trading_info_url = 'https://old.idx.co.id/umbraco/Surface/ListedCompany/GetTradingInfoDaily?language=en-us&code='
		
		stock_list = self.retrieve_json(stock_list_url)
		
		stocks_with_listing_date = self.retrieve_json(
				stocks_with_listing_date_url + str( len( stock_list ) )
			)
		
		company_repo = CompanyRepository()
			
		for each_data in stocks_with_listing_date['data']:
			company_entity = {}
			company_entity['name'] = each_data['NamaEmiten']
			company_entity['listing_date'] = datetime.strptime(each_data['TanggalPencatatan'], '%Y-%m-%dT%H:%M:%S')
			
			emiten_code = each_data['KodeEmiten']
			
			trading_info = self.retrieve_json( trading_info_url + emiten_code )
			company_entity['code'] = emiten_code
			
			marcap = trading_info['NumberForeigner']
			marcap = 0 if marcap is None else int(marcap)
			company_entity['market_capitalization'] = marcap
			
			existing_company = company_repo.get_by_code(emiten_code)
			
			company = None
			
			if existing_company is not None:
				company = company_repo.update(existing_company)
			else:
				company = company_repo.add(company_entity)
			
			self.parseShareHolder(emiten_code, company.id, marcap)
			sleep(60)
	
	
	def get_name_suggestion(self, name):
		shareholder_repo = ShareHolderRepository()
		name_suggestion_list = []
		
		for each_word in name.split(' '):
			if each_word.upper() == 'PT' or each_word.upper() == 'TBK':
				continue
				
				
			for each_ in shareholder_repo.get_like_name(each_word):
				if each_.name not in name_suggestion_list:
					name_suggestion_list.append(each_.name)
		
		if len(name_suggestion_list) < 1:
			return name
		
		try:
			name_checker = NameChecker(name_suggestion_list)
			return name_checker.get_name(name)
		except:
			return name
	
	
	def parseShareHolder(self, emiten_code, company_id, marcap):
		company_profile_detail_url = 'https://old.idx.co.id/umbraco/Surface/ListedCompany/GetCompanyProfilesDetail?emitenType=s&language=en-us&kodeEmiten='
		company_profile_detail = self.retrieve_json( company_profile_detail_url + emiten_code )
		
		shareholder_repo = ShareHolderRepository()
		company_shareholder_repo = CompanyShareHolderRepository()
		
		for each_share_holder in company_profile_detail['PemegangSaham']:
			if each_share_holder['Persentase'] > 100:
				logging.warning('Sharholder {} at {} has {} percantage of market cap'.format(each_share_holder['Nama'], company_id, each_share_holder['Persentase']))
				continue
			
			name = each_share_holder['Nama'].replace('.','')
			sharevalue = int( marcap * float(each_share_holder['Persentase']) / 100 )
			name = self.get_name_suggestion(name)
			
			existing_shareholder = shareholder_repo.get_by_name(name)
			
			if existing_shareholder is None:
				shareholder_entity = {}
				shareholder_entity['name'] = name
				shareholder_entity['share'] = sharevalue
				existing_shareholder = shareholder_repo.add(shareholder_entity)
			
			company_shareholder_entity = {}
			company_shareholder_entity['company_id'] = company_id
			company_shareholder_entity['shareholder_id'] = existing_shareholder.id
			# why cant we just use the Jumlah?
			#company_shareholder_entity['share'] = int(each_share_holder['Jumlah'])
			company_shareholder_entity['share'] = sharevalue
			# print(company_shareholder_entity)
			
			existing_company_shareholder = company_shareholder_repo.get(company_id, existing_shareholder.id)
			
			if existing_company_shareholder is not None:
				company_shareholder_entity['id'] = existing_company_shareholder.id
				company_shareholder_entity['create_date'] = existing_company_shareholder.create_date
				company_shareholder_repo.update(company_shareholder_entity)
			else:
				company_shareholder_repo.add(company_shareholder_entity)
			
			
			shareholder_entity = {}
			shareholder_entity['name'] = name
			shareholder_entity['share'] = sum(each_.share for each_ in company_shareholder_repo.get_by_shareholder_id(existing_shareholder.id))
			shareholder_entity['id'] = existing_shareholder.id
			shareholder_entity['create_date'] = existing_shareholder.create_date
			
			shareholder_repo.update(shareholder_entity)
	
	def retrieve_json(self, url):
		self.wd.goto('view-source:' + url)
		json_ = json.loads(self.wd.session.find_element_by_tag_name('pre').text)
		
		return json_
