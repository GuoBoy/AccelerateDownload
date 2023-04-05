from PyQt5.QtCore import QThread, pyqtSignal
import requests
import os
from config import Config,DEFAULT_HEADERS
from libs.functions import format_filesize
from store import History, Server


class Downloader(QThread):
    """下载线程"""

    progressSignal = pyqtSignal(int)
    messageSignal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.url = ""   # 源文件地址
        self.path = ""  # 保存dir
        self.filename = ""
        self.filesize = ""
        self.downloader_info = {}
        self.config = Config()

    def set_url(self, url: str):
        # self.url = f"https://pd.zwc365.com/seturl/{url}"
        self.url = url

    @property
    def downloader_url(self)->str:
        return f"{Server().server}/{self.url}"

    def set_path(self, p: str):
        if p and not os.path.exists(p):
            self.messageSignal.emit("保存路径不存在，正在创建。。。")
            os.mkdir(p)
        self.path = p

    def run(self):
        try:
            r = requests.get(self.url, headers=DEFAULT_HEADERS, stream=True)
            r.raise_for_status()

            length = r.headers.get('Content-Length', '')
            length = float(length) if length else 0
            chunk_num = length / self.config.chunk_size
            self.filesize = format_filesize(length)
            self.messageSignal.emit(f"文件大小：{self.filesize}")

            # attachment; filename=Sandboxie-Plus-x64-v0.7.4.exe
            filename = r.headers.get('Content-Disposition', '').replace('attachment;', '').replace('filename=',
                                                                                                   '').strip()
            if filename != '':
                filename = filename.split("?")[0] if "?" in filename else filename
                filename = filename.split("#")[0] if "#" in filename else filename
                filename = self.url.split("/")[-1]
            # self.finished.emit("文件名类型未知，请自行判断文件类型并修改文件后缀")
            self.filename = filename
            filename = os.path.normpath(os.path.join(self.path, filename))
            self.messageSignal.emit(f"保存文件至-》 {filename}")
            with open(filename, 'ab') as f:
                i = 1
                # 文件大小未知
                if chunk_num == 0:
                    for chunk in r.iter_content(chunk_size=self.config.chunk_size):
                        f.write(chunk)
                        self.progressSignal.emit(i)
                        i += 1
                        if i == 99: i = 99
                else:  # 大小已知
                    for chunk in r.iter_content(chunk_size=self.config.chunk_size):
                        f.write(chunk)
                        self.progressSignal.emit(int(100 * i / chunk_num))
                        i += 1
            self.progressSignal.emit(100)
            self.messageSignal.emit("下载完毕！")
            if self.config.open_path:   # 下载完打开文件夹
                os.startfile(os.path.dirname(filename))
        except Exception as ret:
            self.progressSignal.emit(100)
            self.messageSignal.emit("下载失败，错误：{}\n请重试!".format(ret))
        finally:
            # 保存历史记录
            History().save(self.filename, self.downloader_url, self.filesize, self.path)
