# 用户注册与验证
1.	用途：	获取token
	URL：	`/token`
	方法：	`GET`
	参数：`?token=<string>`
	返回值：
	
	```
	{
		"token": <string>
	}
	```

# 课程表

1.	用途：	获取课程表（教学计划）
	URL：	`/static_lessons`
	方法：	`GET`
	参数：	`?token=<string>`
	返回值：  
    ```
    {
        lessons:
        [
            {
                "lesson_id": <num>,
                "name": <string>,
                teacher:[string],
                schedule:
                [
                    {
                        "week": <num>,
                        weekday:(num),
                        class_index:(num),
                    },
                    ...
                ]
            },
            {
                ...
            }
        ]
    }
    ```

2.	用途：	获取课程表（个性化课程）
	URL：	`/mylessons`
	方法：	`GET`
	参数：	`?token=<string>`
	返回值：
    ```
    {
        lessons:
        [
            {
                "lesson_id": <num>,
                "name": <string>,
                teacher:[string],
                schedule:
                [
                    {
                        "week": <num>,
                        weekday:(num),
                        class_index:(num),
                    },
                    ...
                ]
            },
            {
                ...
            }
        ]
    }
    ```

3.	用途：	`添加课程（个性化课程）`
	URL：	`/mylessons`
	方法：	`POST`
	参数：
	```
	{
	    "token":（token）,
	    lesson:{
            name:[string],
            teacher:[string],
            schedule:[
                {
                     week:(num),
                     weekday:(num),
                     class_index:(int)
                },
                ...
            ]
        }
	}
	```
	返回值：
	
	```
	{
		"result": "success/fault",
		"lesson_id": <num>
	}
	```

3.	用途：	删除课程（个性化课程）
	URL：	`/mycourse/<id>`
	方法：	`DELETE`
	参数：	`token=(token)`
	返回值：`状态码200或204`

3.	用途：	`修改课程（个性化课程）`
	URL：	`/mycourse/[id]`
	方法：	`PUT`
	参数：
	```
	{
	    "token":（token）,
	    lesson:{
            name:[string],
            teacher:[string],
            schedule:[
                {
                     week:(num),
                     weekday:(num),
                     class_index:(int)
                },
                ...
            ]
        }
	}
	```
	返回值：`状态码200或204`

-----
### 拥挤度查询
用途：```获取所有的拥挤度信息```
URL：	```/crowdedness```
方法：	```GET```
参数:	`token: <string>`
返回值:

```
{
    crowdness:
    [
        {
            position:(string),
            crowdedness:(num)
        },
        ...
    ]
}
```

用途：```按教室获取拥挤度信息```
URL：	```/position/crowdedness```
方法：	`GET`
参数:	`token: <string>`
返回值：
```
    {
      "crowdedness": 0.9
    }
```

用途：  ```按教室更新拥挤度信息```
URL：	```/<position>/crowdedness```
方法：	```post```
参数:
```
{
    token: <string>,
    crowdedness:(num)
}
```
返回值:	`状态码200或204`

-----
# 附近的课

#### 1. 获取附近的课
* URL：	```/<position>/nearby_lessons```
* 方法：	```GET```
* 参数：
```
{
	token=(token)
}
```
* 返回值： 一个json对象
```
    {
      "lessons": [
        {
          "name": "\u6570\u636e\u7ed3\u6784",
          "teacher":[string]
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
