from chi.models import User

class PaginatedAPIMixin (object):

	@staticmethod
	def to_dict_collection(query, page, per_page, endpoint, **kwargs):
		resources = query.paginate(page, per_page, False)
		data = {
			"users" : [item.to]
		}