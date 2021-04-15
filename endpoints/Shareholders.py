from flask_restful import Resource, marshal_with, reqparse
import json
import logging
from model.BaseResponse import BaseResponse, resource_fields
from repo.ShareHolderRepository import ShareHolderRepository

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
		result = repo.get_paginate(page=page)
		
		result_list = []
		
		for row in result:
			entry = {}
			entry['code'] = row[0].code
			entry['name'] = row[1].name
			entry['share'] = row[1].share
			entry['company'] = row[0].name
			result_list.append(entry)
		
		response = BaseResponse()
		response.message = 'success'
		response.status = 'success'
		response.data = result_list
		
		return response
