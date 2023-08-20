# Usage

- setup server
- setup save path
- download link & down


# Design

## 设置
### 服务器管理
- 添加
- 删除
### 其他设置
- 下载完成是否打开

## 添加下载任务
- 选择服务器
- 保存地址
- 下载链接，下载

## 任务列表
- 任务
  - 下载链接
  - 创建时间
  - 进度
  - 文件名
  - 保存路径


```python
# 每个任务保存在下载列表中
list = {
  task_id:
  {
    "tid": 0,
    "url":""
    ...
  }
}
# 每个任务一个线程
task_id: 0
```

