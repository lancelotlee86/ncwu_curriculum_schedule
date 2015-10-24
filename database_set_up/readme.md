这个文件夹是用来初始化数据库、从xls文件中提取数据、格式化数据并插入到数据库中去。
1. 通过database_set_up.sql文件，创建数据库的骨架，这个文件是通过HeidiSQL导出的；
2. 通过"数据准备.py"从xls文件中提取数据，并导入建立好的数据库，该步操作需要配置python环境，并安装pymysql模块
3. 数据库是 mysql或者MariaDb
