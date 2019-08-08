

def format_str():
    """ 格式化字符串 """
    name = "张三"
    print('欢迎您，%s' % name)

    #整型，float类型
    num = 12.33
    print('您输入的数字是： %.4f' % num)
    num2 = 54
    print('您输入的数字是: %04d' % num2)

    t = (1,2,3,5)
    print('您输入的元组是：%s' % str(t))

    print('您的姓名： %(name)s' % {'name': name})

def format_str2():
    """ 使用位置 """
    print('欢迎您，{0}， {1}'.format('张三','好久不见'))
    """ 使用名称"""
    print('您好，{username}, 您的编号是{num}'.format(username="张三",num=45))

if __name__ == '__main__':
    format_str2()