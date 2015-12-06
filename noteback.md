几个父类的属性不能同名，稍微修改一下，比如现在Lesson的实例的_id属性就是继承了某一个父类的

写 Lesson类的 __repr__ 方法

将 func_getCourseNameAndPositionByTimeAndPosition(position, classTime):方法转移到 Lesson 类中，作为实例方法

写 User 类，并作为Student和Teacher类的父类