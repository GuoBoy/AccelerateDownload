from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QDialog, QHeaderView, QMenu, QErrorMessage, QApplication
import os

from store.history import History
from ui.history_ui import Ui_Dialog


class HistoryWindow(QDialog, Ui_Dialog):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.setupUi(self)

		model = QStandardItemModel()
		# 设置表格表头
		self.history_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
		model.clear()
		title = ['filename', 'time', 'url', 'size']
		model.setHorizontalHeaderLabels(title)
		self.history_table.setModel(model)
		# 添加数据
		history = History()
		self.data = data = history.all.get('data', [])
		data.reverse()
		for obj in data:
			for item in title:
				sitem = QStandardItem(obj.get(item))
				model.setItem(data.index(obj), title.index(item), sitem)
			self.history_table.setModel(model)
		self.history_table.customContextMenuRequested.connect(self.generateMenu)
		self.currentData = {}

	def generateMenu(self, pos):
		print(f"右键位置{pos}")
		try:
			index = self.history_table.currentIndex().row()
			self.currentData = self.data[index]
			menu = QMenu()
			item1 = menu.addAction(u"复制链接")
			item2 = menu.addAction(u"打开文件")
			action = menu.exec_(self.history_table.mapToGlobal(pos))
			if action == item1:
				link = self.currentData.get('link')
				QApplication.clipboard().setText(link)
			elif action == item2:
				try:
					os.startfile(os.path.dirname(self.currentData.get('filename')))
				except Exception as ret:
					err = QErrorMessage(self)
					err.setWindowTitle("提示")
					err.showMessage("打开文件失败")
					print("打开文件失败", ret)
			else:
				return
		except Exception as ret:
			print(f'右键菜单异常{ret}')
