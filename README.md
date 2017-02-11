# 出租屋信息管理系统

基于**Django**开发的出租屋信息管理系统，开发初衷是给女友的圣诞礼物，她使用这个系统记录自己出租屋的收入信息

我在线上部署了一个[游客版](http://labrador.junjielee.site/)，账号和密码都是`guest`


## Usage

1. 创建Mysql数据库
2. 复制文件`labrador/labrador/conf/labrador_conf_default.py`到`labrador/labrador/conf/labrador_conf_dev.py`，修改对应的内容:

  ```python
  EXCEL_EXPORT_PATH 导出excel的文件路径
  EXCEL_IMPORT_PATH 导入excel的文件路径
  LOGGING_FILE 日志文件

  以及数据库相关配置
  ```
3. 安装开发环境

  先使用virtualenv建立一个环境，然后使用命令`pip install -r requirements.txt` 安装需要的包
4. 运行命令: `python manage.py runserver 127.0.0.1:8999`，然后在浏览器访问地址`127.0.0.1:8999`
