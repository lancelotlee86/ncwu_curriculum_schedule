import xlrd

xls_file_path = '201020111课表数据.xls'
book = xlrd.open_workbook(xls_file_path)
sh = book.sheet_by_index(0)

# 提取课程代码B列和课程名称C列
# 用于 course表的id和name
def write_course_id_and_name():
    data = []
    for i in range(sh.nrows):
        data_tuple = (sh.cell_value(rowx=i, colx=1), sh.cell_value(rowx=i, colx=2))
        if data_tuple not in data:
            data.append( data_tuple )

    file = open('data.py', 'w', encoding='utf-8')
    file.write('course_id_and_name = '+str(data))
    file.write('\n')
    file.close()
