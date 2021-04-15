from model.BaseResponse import BaseResponse, resource_fields
from flask_restful import Resource, marshal_with
import json
import logging
from repo.CompanyRepository import CompanyRepository

from model.Scraper import WebDriver


class Scraping(Resource):
	@marshal_with(resource_fields)
	def get(self):
		response = BaseResponse()
		response.message = 'success'

		stock_list_url = 'https://www.idx.co.id/umbraco/Surface/Helper/GetEmiten?emitenType=s'
		stock_list_url_with_name = 'https://www.idx.co.id/umbraco/Surface/ListedCompany/GetCompanyProfiles?draw=1&columns%5B0%5D%5Bdata%5D=KodeEmiten&columns%5B0%5D%5Bname%5D=&columns%5B0%5D%5Bsearchable%5D=true&columns%5B0%5D%5Borderable%5D=false&columns%5B0%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B0%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B1%5D%5Bdata%5D=KodeEmiten&columns%5B1%5D%5Bname%5D=&columns%5B1%5D%5Bsearchable%5D=true&columns%5B1%5D%5Borderable%5D=false&columns%5B1%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B1%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B2%5D%5Bdata%5D=NamaEmiten&columns%5B2%5D%5Bname%5D=&columns%5B2%5D%5Bsearchable%5D=true&columns%5B2%5D%5Borderable%5D=false&columns%5B2%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B2%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B3%5D%5Bdata%5D=TanggalPencatatan&columns%5B3%5D%5Bname%5D=&columns%5B3%5D%5Bsearchable%5D=true&columns%5B3%5D%5Borderable%5D=false&columns%5B3%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B3%5D%5Bsearch%5D%5Bregex%5D=false&start=0&search%5Bvalue%5D=&search%5Bregex%5D=false&_=1618490554596&length=700'
		company_profile_detail_url = 'https://www.idx.co.id/en-us/listed-companies/company-profiles/company-profile-detail/?kodeEmiten='
		shareholders_url = 'https://www.idx.co.id/umbraco/Surface/ListedCompany/GetCompanyProfilesDetail?emitenType=&kodeEmiten=ABBA&language=en-us'
		trading_info_url = 'https://www.idx.co.id/umbraco/Surface/ListedCompany/GetTradingInfoDaily?code=ABBA&language=en-us'
		
		stock_list = self.retrieve_json(stock_list_url)
		
		return response

	def retrieve_json(self, url):
		wd = WebDriver('view-source:' + url)
		json_ = json.loads(wd.session.find_element_by_tag_name('pre').text)
		
		return json_

