from store.db import BaseDBStore

class Server(BaseDBStore):
	"""历史记录存取"""
	def __init__(self):
		super().__init__()

	def load(self) -> list:
		"""加载下载历史"""
		return self._select_many("select * from servers")

	@property
	def server(self)->str:
		return self._select_one("select addr from servers where is_default=1")[0]

	def save(self, addr:str):
		"""添加历史记录"""
		self._insert("insert into servers (addr) values (?)", addr)

	def set_default_server(self, sid:int):
		"""设置默认服务器"""
		self._execute("update servers set (is_default)=0 where is_default=1")
		self._execute("update servers set (is_default)=1 where id = ?", sid)

	def delete(self, sid:int):
		"""删除服务器"""
		self._execute("delete from servers where id = ?" , sid)