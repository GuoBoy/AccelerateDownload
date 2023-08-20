import re
import hashlib
import time
import math

def check_url(url):
	"""
	:param url: 检查url是否合法
	:return: 返回合法状态
	"""
	return re.match('https?://.+?[a-z]/.+', url)


def format_filesize(size: float) -> str:
	def cal_size(bi):
		return size*1024/bi
	s = 1024 * 1024
	if size < s:
		return f'{cal_size(s)}KB'
	s = 1024*1024*1024
	if size < s:
		return f'{cal_size(s)}MB'
	s = 1024*1024*1024*1024
	if size < s:
		return f'{cal_size(s)}GB'
	else:
		return f'{size}KB'


def filter_tuple2str(ls:tuple|list, idx=1)->list:
	temp = list()
	for itm in ls:
		temp.append(itm[idx])
	return temp

def get_task_id(url:str)->str:
	"""生成下载任务id"""
	url = f"{url}+{time.time()}"
	return hashlib.md5(url).hexdigest()
