from flask_restful import Resource, marshal_with, reqparse
import json
import logging
from model.BaseResponse import BaseResponse, resource_fields
from repo.ShareHolderRepository import ShareHolderRepository
from repo.CompanyShareHolderRepository import CompanyShareHolderRepository
from repo.CompanyRepository import CompanyRepository

shareholders_get_args = reqparse.RequestParser()
shareholders_get_args.add_argument("page", type=int, required=False)


class Shareholders(Resource):
	@marshal_with(resource_fields)
	def get(self):
		args_ = shareholders_get_args.parse_args()
		page = args_['page']
		
		if page is None:
			page = 0
		
		repo = ShareHolderRepository()
		company_shareholder_repo = CompanyShareHolderRepository()
		company_repo = CompanyRepository()
		result = repo.get_paginate(page=page)
		
		
		
		result_list = []
		
		for row in result:
			company_shareholders = company_shareholder_repo.get_by_shareholder_id(row.id)
			codes = []
			
			for each_ in company_shareholders:
				codes.append(company_repo.get(each_.company_id).code)
			
			entry = {}
			entry['code'] = ', '.join(codes)
			entry['name'] = row.name
			entry['share'] = row.share
			result_list.append(entry)
		
		response = BaseResponse()
		response.message = 'success'
		response.status = 'success'
		response.data = result_list
		
		return response
