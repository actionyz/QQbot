# coding:utf-8
from qqbot import QQBotSlot as qqbotslot, RunBot
from requests import *
import json

select_group = ['hahaha','红吉劲谭']

def api(message):
    url = 'http://www.tuling123.com/openapi/api'
    seckey = 'f970843087b34043861851e97538f26e'
    data = {
     'key':seckey,
     'info':message
    }
    req = post(url=url,params=data)
    content = json.loads(req.content)
    if '电影' in message:
    	return ''.join([i['name']+'\n'+i['icon']+i['info']+'****************************'+'\n' for i in content['list'][:5]])
    else:
	    return content['text']

def check_group(contact):
	if contact.ctype == 'group':
		if contact.name in select_group:
			return 1
		else:
			return 0

#群聊用此函数
def group_chat(bot, contact, member, content):
	if check_group(contact):
		print 2,bot.conf.qq,getattr(member, 'uin', None)
		if getattr(member, 'uin', None) != bot.conf.qq:
			bot.SendTo(contact,api(content))


@qqbotslot
def onQQMessage(bot, contact, member, content):
	if contact.ctype == 'group':
		group_chat(bot, contact, member, content)
	else:

		bot.SendTo(contact,api(content))

if __name__ == '__main__':
    RunBot()