from flask_restful import Resource, marshal_with
import json
import logging
from datetime import datetime
from model.BaseResponse import BaseResponse, resource_fields
from repo.CompanyRepository import CompanyRepository
from model.Scraper import WebDriver


class Scraping(Resource):
	@marshal_with(resource_fields)
	def get(self):
		response = BaseResponse()
		response.message = 'success'
		response.status = 'success'

		idx_parser = IdxParser()
		idx_parser.parse_companies()
		
		return response


class IdxParser(object):
	def __init__(self):
		self.wd = WebDriver()
	
	def parse_companies(self):
		stock_list_url = 'https://www.idx.co.id/umbraco/Surface/Helper/GetEmiten?emitenType=s'
		stocks_with_listing_date_url = 'https://www.idx.co.id/umbraco/Surface/ListedCompany/GetCompanyProfiles?draw=1&columns%5B0%5D%5Bdata%5D=KodeEmiten&columns%5B0%5D%5Bname%5D=&columns%5B0%5D%5Bsearchable%5D=true&columns%5B0%5D%5Borderable%5D=false&columns%5B0%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B0%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B1%5D%5Bdata%5D=KodeEmiten&columns%5B1%5D%5Bname%5D=&columns%5B1%5D%5Bsearchable%5D=true&columns%5B1%5D%5Borderable%5D=false&columns%5B1%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B1%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B2%5D%5Bdata%5D=NamaEmiten&columns%5B2%5D%5Bname%5D=&columns%5B2%5D%5Bsearchable%5D=true&columns%5B2%5D%5Borderable%5D=false&columns%5B2%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B2%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B3%5D%5Bdata%5D=TanggalPencatatan&columns%5B3%5D%5Bname%5D=&columns%5B3%5D%5Bsearchable%5D=true&columns%5B3%5D%5Borderable%5D=false&columns%5B3%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B3%5D%5Bsearch%5D%5Bregex%5D=false&start=0&search%5Bvalue%5D=&search%5Bregex%5D=false&_=1618490554596&length='
		trading_info_url = 'https://www.idx.co.id/umbraco/Surface/ListedCompany/GetTradingInfoDaily?language=en-us&code='
		
		stock_list = self.retrieve_json(stock_list_url)
		
		stocks_with_listing_date = self.retrieve_json(
				stocks_with_listing_date_url + str( len( stock_list ) )
			)
		
		# company_repo = CompanyRepository()
			
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
			
			# existing_company = company_repo.get_by_code(emiten_code)
			
			#if existing_company is not None:
			#	company_repo.update(company_entity)
			#else:
			#	company_repo.add(company_entity)
			
			self.parseShareHolder(emiten_code, 0, marcap)
	
	
	def parseShareHolder(self, emiten_code, company_id, marcap):
		company_profile_detail_url = 'https://www.idx.co.id/umbraco/Surface/ListedCompany/GetCompanyProfilesDetail?emitenType=s&language=en-us&kodeEmiten='
		company_profile_detail = self.retrieve_json( company_profile_detail_url + emiten_code )
		
		# share_holder_repo = ShareHolderRepository()
		
		for each_share_holder in company_profile_detail['PemegangSaham']:
			shareholder_entity = {}
			shareholder_entity['company_id'] = company_id
			shareholder_entity['name'] = each_share_holder['Nama']
			# why cant we just use the Jumlah?
			#shareholder_entity['share'] = long(each_share_holder['Jumlah'])
			shareholder_entity['share'] = int( marcap * float(each_share_holder['Persentase']) / 100 )
			print(shareholder_entity)
		
	
	def retrieve_json(self, url):
		self.wd.goto('view-source:' + url)
		json_ = json.loads(self.wd.session.find_element_by_tag_name('pre').text)
		
		return json_

