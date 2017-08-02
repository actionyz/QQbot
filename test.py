# coding:utf-8
from qqbot import QQBotSlot as qqbotslot, RunBot
from qqbot import QQBotSched as qqbotsched, RunBot
from requests import *
import json
import test1

select_group = ['hahaha','红吉劲谭']

# @qqbotsched(hour='11,17', minute='55')
# def mytask(bot):
#     gl = bot.List('group', '红吉劲谭')
#     if gl is not None:
#         for group in gl:
#             bot.SendTo(group, '同志们：开饭啦啦啦啦啦啦！！！')

def shutdown():
    import requests
    import json
    # print contact.name,qq
    # headers = {
    # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    # 'Accept-Encoding' : 'gzip, deflate',
    # 'Accept-Language' : 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    # 'Connection' : 'keep-alive',
    # 'Host' :  '127.0.0.1:8188',
    # 'Upgrade-Insecure-Requests' : '1',
    # 'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0'
    # }
    # re = requests.get('http://127.0.0.1:8188/list/group-member/hahaha/:like:335',headers=headers)
    # print re.content
    # content = json.loads(re.content)
    # qq = content['result'][0]['membs']['r'][0]['qq']
    # requests.get('http://127.0.0.1:8188/group-shut/'+contact.name+'/'+qq+'/'+time,headers=headers)
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Encoding' : 'gzip, deflate',
        'Accept-Language' : 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        'Connection' : 'keep-alive',
        'Host' :  '127.0.0.1:8188',
        'Upgrade-Insecure-Requests' : '1',
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0'
    }
    print 1
    # re = requests.get('http://127.0.0.1:8188/list/group-member/hahaha/:like:180',headers=headers)
    re = requests.get('http://127.0.0.1:8188/list/group-member/hahaha/:like:180',headers=headers)
    print re.content
    content = json.loads(re.content)
    
    qq = content['result'][0]['membs']['r'][0]['qq']
    requests.get('http://127.0.0.1:8188/group-shut/hahaha/'+qq+'/'+'10',headers=headers)


def find80s(keyword):
    import requests
    from bs4 import BeautifulSoup
    import re
    move_list = []
    single = []
    search_url = 'http://www.80s.tw/search'
    s = requests.post(search_url,data={'keyword':keyword})
    soup = BeautifulSoup(s.content,'lxml')
    r = soup.find_all(name='ul',attrs={'class':"clearfix search_list"})
    k = r[0].find_all(name='li')

    for i in k:
        single.append(i.find_all(name='a')[0].get_text().replace(' ','').replace('\n',''))
        single.append('http://www.80s.tw'+re.findall('href="(.*)" ',str(i))[0])
        move_list.append(single)
        single = []

    return move_list

#api接口调用
def api(message,contact):
    url = 'http://www.tuling123.com/openapi/api'
    seckey = 'f970843087b34043861851e97538f26e'
    data = {
     'key':seckey,
     'info':message
    }
    req = post(url=url,params=data)
    content = json.loads(req.content)
    if '电影' in message:
        # return ''.join([i['name']+'\n'+i['icon']+i['info']+'****************************'+'\n' for i in content['list'][:5]])
        arry = find80s(message[message.find('电影')+6:])
        return ''.join(i[0]+':'+i[1]+'\n' for i in arry)
    elif '禁言' in message:
        string = message.split(' ')
        print string
        test1.shutdown()
    else:
        return content['text']


def Frequently_used(contact):
    if contact.ctype == 'group':
        if contact.name in select_group:
            return 1
        else:
            return 0

#群聊用此函数
def group_chat(bot, contact, member, content):
    if Frequently_used(contact):
        print 2,bot.conf.qq,getattr(member, 'uin', None)
        if getattr(member, 'uin', None) != bot.conf.qq:#判断是否是自己
            bot.SendTo(contact,api(content,contact))#使用api对话


@qqbotslot
def onQQMessage(bot, contact, member, content):
    print '@ME'

    if contact.ctype == 'group':
        if '@ME' in content:
            group_chat(bot, contact, member, content)
    else:
        bot.SendTo(contact,api(content,contact))

if __name__ == '__main__':
    RunBot()
