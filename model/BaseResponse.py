from flask_restful import fields

class BaseResponse(object):
	status = ""
	message = ""

resource_fields = {
	'status': fields.String,
	'message': fields.String,
	'reason' : fields.String
}