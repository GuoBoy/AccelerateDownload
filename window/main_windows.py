from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QApplication, QHeaderView, QMenu, QErrorMessage, QProgressBar,QTableWidgetItem
import os
import sys
from config import Config
from libs.downloader import Downloader
from libs.functions import check_url,filter_tuple2str,get_task_id
from ui.mainwindow import Ui_MainWindow
import store


class MainWindow(QMainWindow, Ui_MainWindow):
	task_title_enum = {'filename': 0, 'url': 1, 'size': 2, 'progress': 3}

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.setupUi(self)
		self.config = Config()
		self.save_path_input.setText(self.config.last_path)
		# 下载任务
		self.downloaders = dict()
		# setup base resource
		self._setup_servers()
		self._setup_histories()
		self._setup_tasks()

	def _setup_servers(self):
		serv = store.Server()
		self.servers = serv.load()
		print(self.servers)
		self.comboBox.addItems(filter_tuple2str(self.servers, 1))
		self.comboBox.setCurrentIndex(0)
		# 设置表格表头
		self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
		model = QStandardItemModel()
		title_enum = {'server': 1, 'created_at': 2}
		model.setHorizontalHeaderLabels(title_enum.keys())
		self.tableView.setModel(model)
		# 添加数据
		#
		for row_id, his in enumerate(self.servers):
			for col_id, header_name in enumerate(title_enum.keys()):
				model.setItem(row_id, col_id, QStandardItem(his[title_enum[header_name]]))
			self.history_table.setModel(model)

	def _setup_histories(self):
		"""配置历史记录"""
		def generate_menu(pos):
			print(f"右键位置{pos}")
			try:
				index = self.history_table.currentIndex().row()
				self.currentData = data[index]
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
						self.log("打开文件失败"+repr(ret))
				else:
					return
			except Exception as ret:
				self.log(f'右键菜单异常{ret}')
		# 设置表格表头
		self.history_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
		model = QStandardItemModel()
		title_enum = {'filename': 1, 'time':5, 'url':2, 'size':3}
		model.setHorizontalHeaderLabels(title_enum.keys())
		self.history_table.setModel(model)
		# 添加数据
		history = store.History()
		data = history.load()
		# (1, 'apk', 'https://telegram.org/dl/android/apk', '67.79248142242432MB', 'D:/pySort/allspiders/AcclerateDownload', '2023-05-02 05:34:05'),
		for row_id, his in enumerate(data):
			for col_id, header_name in enumerate(title_enum.keys()):
				# sitem = QStandardItem()
				model.setItem(row_id, col_id, QStandardItem(his[title_enum[header_name]]))
			self.history_table.setModel(model)
		self.history_table.customContextMenuRequested.connect(generate_menu)
		# self.currentData = {}

	def _setup_tasks(self):
		title_enum = self.task_title_enum
		# 设置表格结构
		self.tableWidget.setRowCount(len(self.downloaders.keys()))
		self.tableWidget.setColumnCount(len(title_enum.keys()))
		self.tableWidget.setHorizontalHeaderLabels(title_enum.keys())
		self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
		for row_id, down in enumerate( self.downloaders.values()):
			for col_id, header_name in enumerate(title_enum.keys()):
				idx = title_enum[header_name]
				if header_name=="progress":
					item = QProgressBar(self)
					item.setValue(down[idx])
					self.tableWidget.setCellWidget(row_id, col_id, item)
				else:
					item = QTableWidgetItem(down[idx])
					self.tableWidget.setItem(row_id, col_id, item)

	def on_download(self):
		"""点击下载按钮"""
		try:
			if not check_url(self.url):
				self.log("请输入正确地址，例如：\nhttps://github.com/mitmproxy/mitmproxy/archive/master.zip")
				return
			tid = get_task_id(self.url)
			downloader = Downloader(self.url,self.path, tid)
			downloader.progressSignal.connect(self.on_progress_update)	# 进度
			downloader.messageSignal.connect(self.log)	# 消息
			downloader.initTaskSignal.connect(self.init_task_slot)	# 初始信息信号
			downloader.start()
			self.log("开始下载。。。")
			self.download_url_input.setText("")
		except Exception as ret:
			print(f'安排下载{ret}')
			self.log(ret)

	def init_task_slot(self, tid, filename, url, filesize, path):
		# 发送任务详细信息 tid, filename, url, filesize, path
		self.downloaders[tid]= [filename, url, filesize, 0]
		self._setup_tasks()
		print(tid, filename, url, filesize, path)

	def on_select_savepath(self):
		"""点击选择保存位置按钮"""
		last_path = self.config.last_path
		path = QFileDialog().getExistingDirectory(parent=self, caption="选择保存位置", directory=last_path)
		if path != last_path:
			self.config.update(last_path=path)
			self.save_path_input.setText(path)

	@property
	def path(self):
		"""用户选择的保存路径，若为空，默认保存当前位置"""
		path = os.getcwd() if self.save_path_input.text() == "" else self.save_path_input.text()
		self.save_path_input.setText(path)
		return path

	@property
	def url(self):
		"""用户输入的下载路径"""
		return self.download_url_input.text()

	def log(self, info):
		"""控制台输出信息"""
		self.log_area.append("==> {}".format(repr(info)))

	def on_progress_update(self, tid, v):
		if v == 200:
			del self.downloaders[tid]
			self._setup_histories()
		title_enum = self.task_title_enum
		self.downloaders[tid][title_enum["progress"]] = v
		self._setup_tasks()

	def on_openfile_change(self, state):
		"""是否下载完成打开文件夹state: 0 未选中;	2 选中"""
		try:
			self.config.update(open_path=state)
		except Exception as ret:
			self.log(ret)

	def on_add_server(self):
		"""添加服务器地址"""
		server = self.lineEdit.text()
		if not check_url(server):
			self.log("请重新确认服务器有效性")
			return
		serv = store.Server()
		serv.save(server)
		self._setup_servers()
		self.log("新增成功："+server)
		self.lineEdit.setText("")


def run():
	app = QApplication(sys.argv)
	window = MainWindow()
	window.show()
	sys.exit(app.exec())
