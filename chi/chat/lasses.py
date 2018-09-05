from flask_restful import Resource

items = [
	{
		'name' : 'cynema1',
		'message' : 'what are doing'		
	},
	{
		'name' : 'cilo',
		'message' : 'Who this'		
	},
	{
		'name' : 'Henny',
		'message' : 'Cilo comon'		
	},
	{
		'name' : 'Lorium1',
		'message' : 'Ayo'		
	}
]

class Messages(Resource):

	def get(self):
		return {'items' : items}
