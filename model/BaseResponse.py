from flask_restful import fields

class BaseResponse(object):
	status = ""
	message = ""
	data = None

data_fields = {
	'code': fields.String,
    'name': fields.String,
    'share': fields.String,
    'company': fields.String,
}

resource_fields = {
	'status': fields.String,
	'message': fields.String,
	'data' : fields.List(fields.Nested(data_fields)),
}

