import xlrd

# 配置excel文件读取对象
xls_file_path = '201020111课表数据.xls'
book = xlrd.open_workbook(xls_file_path)
sh = book.sheet_by_index(0)

# 配置pymysql
import pymysql.cursors
connection = pymysql.connect(
    host='localhost',
    user='root',
    passwd='lishenzhi1214',
    db='curriculum_schedule_app',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)

# 提取课程代码B列和课程名称C列
# 用于 course表的id和name
def course_table_data():
    '''取出course表所需要的数据并存入文件方便取用
    遍历每一行，取B列的内容作为course表的id，取C列的内容作为course表的name，分别将这两个内容放在字典中，再放入列表中，最后输出到文件中，作为一个列表

    '''
    data = []
    for i in range(1, sh.nrows-1):
        data_dict = {
            'id':sh.cell_value(rowx=i, colx=1),
            'name':sh.cell_value(rowx=i, colx=2)
        }
        if data_dict not in data:
            data.append( data_dict )

    #file = open('data.py', 'a', encoding='utf-8')
    #file.write('course_table_data = '+str(data))
    #file.write('\n')
    #file.close()
    return data


def class_table_data():
    '''取出class表所需要的数据并存入文件方便取用
    遍历每一行，取G列内容的后7个字符作为class表的id，取G列前几个字符作为class表的major字段
    排除重复的行，这两个内容取出后以字典的形式存入一个列表并写入文件
    '''
    data = []
    for i in range(1, sh.nrows-1):
        data_dict = {
            'id': sh.cell_value(rowx=i, colx=6)[-7:],
            'major': sh.cell_value(rowx=i, colx=6)[:-7]
        }
        if data_dict not in data:
            data.append( data_dict )

    #file = open('data.py', 'a', encoding='utf-8')
    #file.write('class_table_data = '+str(data))
    #file.write('\n')
    #file.close()
    return data


def classroom_table_data():
    '''取出classroom表所需要的数据并存入文件方便取用
    id为自增
    position为K列内容
    campus为H列内容，注意要将“本部”换成“花园校区”
    building, capacity, floor, number等字段稍后进行处理填充
    '''
    def _change_benbu_to_huayuan(position):
        if position == '本部':
            return '花园校区'
        return '龙子湖校区'

    position_set = []
    data = []
    id_count = 1
    for i in range(1, sh.nrows-1):
        data_dict = {
            'id': id_count,
            'campus': _change_benbu_to_huayuan(sh.cell_value(rowx=i, colx=7)),
            'position': sh.cell_value(rowx=i, colx=10)
        }
        if i%1000 == 0:
            print(i)
        if sh.cell_value(rowx=i, colx=10) not in position_set:
            data.append( data_dict )
            position_set.append(sh.cell_value(rowx=i, colx=10))
            id_count += 1

    #file = open('data.py', 'a', encoding='utf-8')
    #file.write('\n')
    #file.write('classroom_table_data = '+str(data))
    #file.write('\n')
    #file.close()
    return data


def teacher_table_data():
    '''取出course表所需要的数据并存入文件方便取用
    遍历每一行，取B列的内容作为course表的id，取C列的内容作为course表的name，分别将这两个内容放在字典中，再放入列表中，最后输出到文件中，作为一个列表

    '''
    data = []
    for i in range(1, sh.nrows-1):
        data_dict = {
            'id':sh.cell_value(rowx=i, colx=11),
            'name':sh.cell_value(rowx=i, colx=12)
        }
        if data_dict not in data:
            data.append( data_dict )
    #file = open('data.py', 'a', encoding='utf-8')
    #file.write('course_table_data = '+str(data))
    #file.write('\n')
    #file.close()
    return data

def lesson_table_data():
    '''获取lesson表需要的信息，不存入文件中，直接取用，因为太大了

    '''
    _classroom_table_data = classroom_table_data()
    def _available_week_list(week_str, odd_or_dual = None):
        week_list = []
        # 这个if else是用来将周数分开，放到week_list列表中
        if ',' in week_str:
            # 意味着分成两段
            week_list = list(_available_week_list(week_str.split(',')[0])) + list(_available_week_list(week_str.split(',')[1]))
        elif '-' not in week_str:
            # 意味着只有一个周
            week_list.append(int(week_str))
        elif ',' in week_str:
            # 意味着分成两段
            week_list = list(_available_week_list(week_str.split(',')[0])) + list(_available_week_list(week_str.split(',')[1]))
        else:
            # 正常情况，如'1-16'
            week_start_at = int(week_str.split('-')[0])
            week_end_at = int(week_str.split('-')[1])
            week_list = list(range(week_start_at, week_end_at+1))
        # 现在看看是否要求奇偶周，按需返回值
        if odd_or_dual is None:
            return week_list
        elif odd_or_dual == 'odd':
            return filter(lambda x: x%2==1, week_list)
        else:
            return filter(lambda x: x%2==0, week_list)

    def _get_classroom_id_by_position(position):
        # classroom_table_data() 会返回一个列表
        for classroom in _classroom_table_data:
            if classroom['position'] == position:
                return classroom['id']

    def _get_lesson_time(time_str):
        if '单' in time_str:
            return mapping_time[time_str[2:-3]]
        elif '双' in time_str:
            return mapping_time[time_str[2:-3]]
        else:
            return mapping_time[time_str[2:-2]]

    data = []
    print(1)
    id_count = 1
    for i in range(1, sh.nrows-1):
        # i 代表行数
        # 检查 这一行是否为单双周专属
        odd_or_dual = None
        if '单' in sh.cell_value(rowx = i, colx = 9):
            odd_or_dual = 'odd'
        elif '双' in sh.cell_value(rowx = i, colx = 9):
            odd_or_dual = 'even'
        for j in _available_week_list(sh.cell_value(rowx = i, colx = 8), odd_or_dual = odd_or_dual):
            # j 代表每一个周数
            #print(sh.cell_value(rowx = i, colx = 9))
            #print(len(sh.cell_value(rowx = i, colx = 9)))
            #print(i)
            #print(j)
            data_dict = {
                'id': id_count,
                'course_id': sh.cell_value(rowx = i, colx = 1),
                'class_id': sh.cell_value(rowx=i, colx=6)[-7:],
                'year': '20102011',
                'term': '1',
                'week': str(j),
                'day': str(mapping_day[sh.cell_value(rowx = i, colx = 9)[0]]),
                'time': _get_lesson_time(sh.cell_value(rowx = i, colx = 9)),
                'classroom_id': _get_classroom_id_by_position(sh.cell_value(rowx = i, colx = 10)),
                'teacher_id': sh.cell_value(rowx = i, colx = 11)
            }
            id_count += 1
            data.append(data_dict)
            if id_count%1000 == 0:
                print(id_count)
    #file = open('data.py', 'a', encoding='utf-8')
    #file.write('\n')
    #file.write('lesson_table_data = '+str(data))
    #file.write('\n')
    #file.close()
    return data

mapping_day = {
    '一': '1',
    '二': '2',
    '三': '3',
    '四': '4',
    '五': '5',
    '六': '6',
    '七': '7'
}

mapping_time = {
    '1-2': '1',
    '1-4': '1',
    '3-4': '2',
    '5-6': '3',
    '5-8': '3',
    '7-8': '4',
    '9-10': '5'
}

def insert_course_data():
    cursor = connection.cursor()
    for course_data in course_table_data():
        sql = "INSERT INTO `course` (`id`, `name`) VALUES (%s, %s)"
        cursor.execute(sql, (course_data['id'], course_data['name']))
    connection.commit()
    connection.close()


def insert_classroom_data():
    cursor = connection.cursor()
    for classroom_data in classroom_table_data():
        sql = "INSERT INTO `classroom` (`id`, `campus`,`position`) VALUES (%s, %s, %s)"
        cursor.execute(sql, (classroom_data['id'], classroom_data['campus'], classroom_data['position']))
    connection.commit()
    connection.close()

def insert_class_data():
    cursor = connection.cursor()
    for class_data in class_table_data():
        sql = "INSERT INTO `class` (`id`, `major`) VALUES (%s, %s)"
        cursor.execute(sql, (class_data['id'], class_data['major']))
    connection.commit()
    connection.close()

def insert_teacher_data():
    cursor = connection.cursor()
    for teacher_data in teacher_table_data():
        sql = "INSERT INTO `teacher` (`id`, `name`) VALUES (%s, %s)"
        cursor.execute(sql, (teacher_data['id'], teacher_data['name']))
    connection.commit()
    connection.close()

def insert_lesson_data():
    cursor = connection.cursor()
    _lesson_table_data = lesson_table_data()
    for lesson_data in _lesson_table_data:
        sql = "INSERT INTO `lesson` (`id`, `course_id`, `class_id`, `year`, `term`, `week`, `day`, `time`, `teacher_id`, `classroom_id`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, (lesson_data['id'], lesson_data['course_id'], lesson_data['class_id'], lesson_data['year'], lesson_data['term'], lesson_data['week'], lesson_data['day'], lesson_data['time'], lesson_data['teacher_id'], lesson_data['classroom_id']))
        if lesson_data['id']%1000 == 0:
            print('正在插入第' + str(lesson_data['id']) + '个')
    print('开始commit')
    connection.commit()
    connection.close()
