# coding:utf-8
"""
create on Nov 26,2018 by Wayne Yu
Python+WeChat的玩法
"""
import itchat

# 登录
itchat.login()
# 发消息
itchat.send(u"这是一条自动发的消息！Hello, Python+Wechat……", 'filehelper')
# 获取好友列表
friends = itchat.get_friends(update=True)[0:]
male = female = other = 0
# 遍历这个列表，列表第一位是自己，所以从自己之后开始计算
for i in friends[1:]:
    sex = i['Sex']
    if sex == 1:
        male += 1
    elif sex == 2:
        female += 1
    else:
        other += 1
# 总数算上，好计算比例
total = len(friends[1:])
# 输出结果
print("男性好友:%.2f%%" % (float(male)/total * 100))
print("女性好友:%.2f%%" % (float(female)/total * 100))
print("其他好友:%.2f%%" % (float(other)/total * 100))

itchat.logout()