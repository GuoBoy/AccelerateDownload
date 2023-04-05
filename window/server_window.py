from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QDialog, QHeaderView, QMenu, QErrorMessage, QApplication
from ui.server_ui import Ui_Dialog
from store.server import Server

class ServerWindow(QDialog, Ui_Dialog):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.setupUi(self)
		self.currentData = {}
		self.items = []
		self.serv = Server()
		self.load_items()

	def load_items(self):
		model = QStandardItemModel()
		# 设置表格表头
		self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
		model.clear()
		title = ['id',"addr", 'create_at', 'is_default']
		model.setHorizontalHeaderLabels(title)
		self.tableView.setModel(model)
		# 添加数据
		items = self.serv.load()
		for item in items:
			for itm in item:
				sitem = QStandardItem(itm)
				model.setItem(items.index(item), item.index(itm), sitem)
				self.tableView.setModel(model)
		self.tableView.customContextMenuRequested.connect(self.generateMenu)

	def generateMenu(self, pos):
		print(f"右键位置{pos}")
		try:
			index = self.tableView.currentIndex().row()
			self.currentData = self.items[index]
			menu = QMenu()
			item1 = menu.addAction(u"设置为默认服务")
			item2 = menu.addAction(u"删除")
			action = menu.exec_(self.tableView.mapToGlobal(pos))
			print(action, self.currentData)
			if action == item1:
				link = self.currentData.get('link')
				QApplication.clipboard().setText(link)
			elif action == item2:
				try:
					pass
				except Exception as ret:
					err = QErrorMessage(self)
					err.setWindowTitle("提示")
					err.showMessage("打开文件失败")
					print("打开文件失败", ret)
			else:
				return
		except Exception as ret:
			print(f'右键菜单异常{ret}')

	def on_add_server(self):
		addr = self.lineEdit.text()
		if addr:
			try:
				self.serv.save(addr)
			except Exception as ret:
				print(ret)
			self.load_items()