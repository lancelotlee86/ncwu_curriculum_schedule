# 用户注册与验证
1.	用途：	获取token
	URL：	
	方法：	GET
	参数：
	返回值：



# 课程表

1.	用途：	获取课程表（教学计划）
	URL：	
	方法：	GET
	参数：	key=（token）
	返回值：

2.	用途：	获取课程表（个性化课程）
	URL：	
	方法：	GET
	参数：	key=（token）
	返回值：

3.	用途：	添加课程（个性化课程）
	URL：	
	方法：	POST
	参数：	key=（token）
	返回值：

3.	用途：	删除课程（个性化课程）
	URL：	
	方法：	DELETE
	参数：	key=（token）
	返回值：

3.	用途：	修改课程（个性化课程）
	URL：	
	方法：	PUT
	参数：	key=（token）
	返回值：

---
### 拥挤度查询

用途：```获取拥挤度信息```
URL：	```/get_crowdedness_rate_by_position```
方法：	```GET```
参数:
```
    {
        token: 'token',
        position: '[龙]三号楼3402',
    }
```
返回值：
```
    {
      "crowdedness": 0.9
    }
```

-----
# 附近的课

#### 1. 获取附近的课
* URL：	```/get_nearby_lessons_by_position```
* 方法：	```GET```
* 参数：
```
{
	key=(token),
	position=(position),
	lesson_time=('20102011-1-11-3-1')
}
```
* 返回值： 一个json对象
```
    {
      "lessons": [
        {
          "name": "\u6570\u636e\u7ed3\u6784",
          "position": "[\u9f99]\u4e09\u53f7\u697c3402"
        },
        {
          "name": "\u6570\u636e\u7ed3\u6784",
          "position": "[\u9f99]\u4e09\u53f7\u697c3403"
        }
      ]
    }
```
* 说明： 
```
    position是教室地址的字符串，比如 position = '[龙]三号楼3402'
    lesson_time可以有可以没有，如果没有的话，默认为系统当前时间，如果有的话，按照'20102011-1-11-3-1'格式
```
