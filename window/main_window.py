from PyQt5.QtWidgets import QWidget, QFileDialog, QApplication
import os
import sys
import traceback

from config import Config
from libs.downloader import Downloader
from libs.functions import check_url,filter_tuple2str
from ui.window import Ui_Form
from .history_window import HistoryWindow
from .server_window import ServerWindow
from store import Server


# from  . import HistoryWindow, ServerWindow


class MainWindow(QWidget, Ui_Form):
	"""主窗口"""

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.setupUi(self)
		self.downloader = Downloader()
		self.downloader.progressSignal.connect(self.set_progress)
		self.downloader.messageSignal.connect(self.message)
		self.config = Config()

		self.save_path_input.setText(self.config.last_path)
		# self.server_input.setText(self.config.server)

		self.serv = Server()
		self.servers = self.serv.load()
		self.comboBox.addItems(filter_tuple2str(self.servers, 1))
		for i in self.servers:
			if i[3] == 1:
				self.comboBox.setCurrentIndex(self.servers.index(i))
				break
		self.comboBox.currentIndexChanged.connect(self.modify_server)
		self.whether_open.setChecked(bool(self.config.open_path))

	def on_download(self):
		"""点击下载按钮"""
		try:
			if not check_url(self.url):
				self.message("请输入正确地址，例如：\nhttps://github.com/mitmproxy/mitmproxy/archive/master.zip")
				return
			self.download_btn.setDisabled(True)
			self.download_btn.setText("下载中")
			self.downloader.set_url(self.url)
			self.downloader.set_path(self.path)
			self.downloader.start()
			self.message("开始下载。。。")
			self.set_progress(0)
		except Exception as ret:
			print(f'安排下载{ret}')
			self.message(repr(ret))
			traceback.print_exc()

	def on_path(self):
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

	def message(self, text):
		"""控制台输出信息"""
		self.log_area.append("==> {}".format(text))

	def set_progress(self, v):
		self.progress_bar.setValue(v)
		if v == 100:
			self.download_btn.setDisabled(False)
			self.download_btn.setText("下载")

	def to_openpath(self, state):
		"""是否下载完成打开文件夹
		state:
			0 未选中
			2 选中
		"""
		try:
			self.config.update(open_path=state)
		except Exception as ret:
			print(ret)
			self.message(repr(ret))

	def show_history(self):
		"""显示下载历史窗口"""
		try:
			HistoryWindow(parent=self).show()
		except Exception as ret:
			print(ret)
			self.message(repr(ret))

	def modify_server(self, idx):
		"""修改服务器地址"""
		try:
			self.serv.set_default_server(self.servers[idx][0])
			self.message(f"修改服务器为：{self.servers[idx][1]}")
			print(idx)
		except Exception as ret:
			print(ret)

	def show_server_manager(self):
		"""显示服务器管理窗口"""
		try:
			ServerWindow(parent=self).show()
		except Exception as ret:
			print(ret)
			self.message(repr(ret))


def run():
	app = QApplication(sys.argv)
	window = MainWindow()
	window.show()
	sys.exit(app.exec())
