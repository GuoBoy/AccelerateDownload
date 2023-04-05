import yaml
import pathlib

# dir path
DIR_PATH =  pathlib.Path(__file__).parent
# 配置文件路径
DEFAULT_C_FILENAME = DIR_PATH.joinpath("config.yaml")
# db path
DB_FILENAME = DIR_PATH.joinpath("database.db").as_posix()
# 默认请求头
DEFAULT_HEADERS = {
	"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36",
}

class Config:
    """配置加载"""
    def __init__(self, c_file=""):
        self.c_file = c_file
        if c_file == "":
            self.c_file = DEFAULT_C_FILENAME
        with open(self.c_file, 'r') as f:
            self.cfg: dict = yaml.safe_load(f)

    def update(self, **kwargs):
        """更新配置项"""
        self.cfg.update(**kwargs)
        with open(self.c_file, 'w') as f:
            yaml.safe_dump(self.cfg, f)

    @property
    def last_path(self):
        return self.cfg['last_path']

    @property
    def open_path(self):
        return self.cfg['open_path']

    @property
    def history_filename(self):
        return self.cfg['history_filename']

    @property
    def server(self):
        return self.cfg['server']

    @property
    def chunk_size(self):
        return self.cfg['chunk_size']
