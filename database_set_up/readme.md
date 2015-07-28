1. 通过database_set_up.sql文件，创建数据库的骨架
2. 通过"数据准备.py"从xls文件中提取数据，并保存到data.py，数据都以字典、列表等形式存储，方便调用
3. extract_from_xls_and_insert_into_database.py ：从data.py中获取一部分数据，然后在从xls文件中获取一行一行的文件，并存储到数据库中。