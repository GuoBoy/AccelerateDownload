from store.db import BaseDBStore

class History(BaseDBStore):
	"""历史记录存取"""
	def __init__(self):
		super().__init__()

	def load(self) -> list:
		"""加载下载历史"""
		return self._select_many("select * from histories")

	def save(self,filename, link,size, save_dir):
		"""添加历史记录"""
		self._insert("insert into histories (filename, link,size, dir) values (?,?,?,?)", filename, link,size, save_dir)

	def clear(self):
		"""删除历史记录"""
		self._execute("delete from histories")