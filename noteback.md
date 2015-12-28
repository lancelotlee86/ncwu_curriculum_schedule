写 User 类，并作为Student和Teacher类的父类

完善数据库中的信息，否则寸步难行

新建 FryCourse 类，专门用来接受一个 lessons 序列，并处理成一个fry_courses序列返回

先做添加个性化
再做删除个性化
最后再做查询个性化课表






# python备忘

   sql查询语句中，where的字段名，不能带引号
   
   深拷贝 generator 的时候要用 tee，详见http://stackoverflow.com/questions/21315207/deep-copying-a-generator-in-python
   
   好好利用Debugger Thread 调试，看之前的运行步骤的结果
   
   当用到多继承时，子类并不能很好的调用父类的 由类方法组成的构造函数，可能可以用，但是我们不会用。
   构造函数的重载，在没有更好的思路的情况下，就手动判断默认 __init__ 的参数个数及类型好了