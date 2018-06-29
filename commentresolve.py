import requests
from bs4 import BeautifulSoup
import base_content
import json
import urllib.parse
import dbmodels
import random
import time

'''
从歌曲中，下载评论
'''

datas = {
	'params':base_content.datas_params
	,'encSecKey':base_content.datas_encSecKey
}

def get_url_id(url):
	url_parse = urllib.parse.urlparse(url)
	url_params=urllib.parse.parse_qs(url_parse.query,True)
	#保存到数据库时，需要根据歌曲id判断是否重复
	#print(url_params['id'])
	if(url_params['id'] != None):
		return url_params['id'][0]
	else:
		return -1

def get_url_path(url):
	url_parse = urllib.parse.urlparse(url)
	return url_parse.path

def resolve_songls_comments(songlist_url,comments_url):
	pass


# 查找并解析歌词
def resolve_comments(music_url,comments_url = None):
	#线程随机暂停一段时间
	time.sleep(random.uniform(0.1,3))

	if (comments_url == None):
		base_url = base_content.GetCommentBaseUrl
		url_path = get_url_path(music_url)
		if(url_path == '/song'):
			base_url = base_content.GetCommentBaseUrl
		elif (url_path == '/program'):
			base_url = base_content.GetDTCommentBaseUrl

		comments_url = base_url%(get_url_id(music_url),)

	#print(comments_url)
	
	http_response = None
	try:
		http_response = requests.post(comments_url,headers = base_content.GetCommentHeaders,data = datas,timeout = 10)
	except Exception as e:
		print('request %s error,pelase check url'%(music_url,))
		return
	
	http_response.encoding = base_content.Encoding

	#读取内容并加载到解析器中
	html_text = http_response.text
	#print(html_text)
	html_json = json.loads(html_text)
	if(html_json['code'] != 200):
		print('get comment error：'+html_text)
		if(html_json['code'] == 460):
			print('网易检测到爬虫程序，禁止返回数据，请中断爬虫或者等待解封IP')
			#time.sleep(random,uniform(100,600))
			resolve_comments(music_url)
		return

	hotComments_json = html_json['hotComments']
	#print(hotComments_json)
	if(hotComments_json == None):
		return

	index = 0
	if(len(hotComments_json)>=3):
		index = 3
	elif(len(hotComments_json)==2):
		index = 2
	elif(len(hotComments_json)==1):
		index = 1

	#print(hotComments_json)
	for hot_index in range(index):
		hot_item = hotComments_json[hot_index]
		hot_item_user = hot_item['user']


		comment_context = hot_item['content']
		comment_zan = hot_item['likedCount']
		music_id = get_url_id(music_url)
		comment_id = hot_item['commentId']
		music_name = 'None'
		comment_user = hot_item_user['nickname']
		comment_httpurl = music_url
		
		dbmodels.save_item(comment_context,comment_zan,music_id,comment_id,music_name,comment_user,comment_httpurl)
		#comment_musicname = 


def start_thread():
	while(base_content.is_while_html):
		try:
			for music_item in base_content.music_url_list:
				if(base_content.music_url_list[music_item] != 0):
					continue
				base_content.music_url_list[music_item] = 1
				print('get comment thread start:'+music_item)
				resolve_comments(music_item)
		except RuntimeError as e:
			pass
		except Exception as e:
			pass

	print('循环获取网页完成，循环获取歌单列表完成，最后遍历一次歌曲列表')
	for music_item in base_content.music_url_list:
		if(base_content.music_url_list[music_item] != 0):
			continue
			
		base_content.music_url_list[music_item] = 1
		resolve_comments(music_item)
		
		
		
		
		