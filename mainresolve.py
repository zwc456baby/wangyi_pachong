import requests
from bs4 import BeautifulSoup
import threading
#导入自定义模块
import base_content
import commentresolve
from bs4.element import Tag
import os
import time
import signal
import random

'''
启动各个线程，遍历网页，获取歌单链接
'''

start_url = base_content.music_root_path
#start_url = 'http://music.163.com/discover/playlist/'
#start_url = 'http://music.163.com/song?id=573125026'


def save(http_url,text):
	urls = http_url.split('/')
	dir_ = os.path.join(os.path.abspath('.'),'html_file')
	if not os.path.exists(dir_):
		try:
			os.mkdir(dir_)
		except Exception as e:
			print('save text error')
			return

	try:
		id_ = commentresolve.get_url_id(http_url)
		name = ''
		if(id_ == -1):
			name = os.path.join(dir_,urls[len(urls)-1])
		else:
			name = os.path.join(dir_,str(id_))
		print(name)
		open(name,'w',encoding = base_content.Encoding).write(text)
	except Exception as e:
		print('save text error')
		return

def add_url_toreqlist(url):
	if(url not in base_content.html_req_list):
		base_content.html_req_list[url] = 0
		print('add req url:'+url)
		return True
	else:
		return False

def add_url_tomusiclist(url):
	add_url_toreqlist(url)
	if(url not in base_content.music_url_list):
		base_content.music_url_list[url] = 0
		print('add music url:'+url)
		return True
	else:
		return False


def get_hotornew(soup):
	soup_hotornew = soup.find('div',class_ = 'u-btn f-fr u-btn-hot d-flag')
	if(soup_hotornew != None):
		#print('hot or new')
		for req_item in soup_hotornew.children:
			if(not isinstance(req_item,Tag)):
				continue
			new_req_url = base_content.music_root_path + req_item['href']
			add_url_toreqlist(new_req_url)

def get_page(soup):
	soup_page = soup.find_all('a',class_ = 'zpgi')
	if(soup_page != None and len(soup_page)>0):
		for page_item in soup_page:
			new_req_url = base_content.music_root_path + page_item['href']
			#print('查找翻页')
			add_url_toreqlist(new_req_url)

def get_findmusic(soup):
	soup_find = soup.find('ul',class_ = 'nav')
	
	if(soup_find != None):
		for item in soup_find.children:
			if(not isinstance(item,Tag)):
				continue
			#print(item)
			new_req_url = base_content.music_root_path + item.a['href']
			add_url_toreqlist(new_req_url)

#选择歌曲列表分类
def get_song_list_class(soup):
	soup_class = soup.find_all('a',class_ = 's-fc1')
	#print(soup_class)
	if(soup_class != None and len(soup_class)>0):
		for item in soup_class:
			new_req_url = base_content.music_root_path + item['href']
			#print('添加选择分类：'+new_req_url)
			add_url_toreqlist(new_req_url)

#获取排行榜
def get_toplist(soup):
	soup_toplist = soup.find_all('a',class_ = 's-fc0')
	if(soup_toplist != None):
		for item in soup_toplist:
			new_req_url = base_content.music_root_path + item['href']
			# print(item['title'])
			add_url_toreqlist(new_req_url)

#获取推荐歌单
def get_recomment(soup):
	#获取推荐列表，因为和toplist 有相同的class和结构，重复调用即可
	get_toplist(soup)

def get_songlist(soup):
	#获取推荐列表，因为和toplist 有相同的class和结构，重复调用即可
	get_toplist(soup)

	# songlist_a = soup.find_all('a',class_ = 'tit f-thide s-fc0')
	# if(songlist_a != None and len(songlist_a)>0):
	# 	for songlist_item in songlist_a:
	# 		music_ls_url = base_content.music_root_path + songlist_item['href']
	# 		add_url_toreqlist(music_ls_url)
	# 	print('此次循环获取到歌单数量：'+str(len(songlist_a)))


def get_dtlist(soup):
	dt_list_soup = soup.find('ul',class_ = 'box f-cb z-show')
	if(dt_list_soup != None):
		for li_item in dt_list_soup.children:
			if(not isinstance(li_item,Tag)):
				continue
			new_req_url = base_content.music_root_path + li_item.a['href']
			#print('电台条目：'+new_req_url)
			add_url_toreqlist(new_req_url)

def get_dtprogram(soup):
	dt_program_soup = soup.find_all('a',class_ = 's-fc1 f-fw0')
	if(dt_program_soup != None):
		for item in dt_program_soup:
			new_req_url = base_content.music_root_path + item['href']
			#print('推荐节目：'+new_req_url)
			add_url_toreqlist(new_req_url)

#获取电台列表分类
def get_dt_list_class(soup):
	#由于和 歌曲列表的分类具有相同属性，所以，调用歌单的分类
	get_song_list_class(soup)

def get_dt_toplist(soup):
	soup_dt_toplist = soup.find('ul',class_ = 'rdilist rdilist-2 f-cb')
	if(soup_dt_toplist != None):
		for item in soup_dt_toplist.children:
			if(not isinstance(item,Tag)):
				continue
			new_req_url = base_content.music_root_path + item.a['href']
			#print('电台排行榜：'+new_req_url)
			add_url_toreqlist(new_req_url)

def get_dt_maylove(soup):
	soup_dt_maylove = soup.find_all('p',class_ = 'f-thide')
	if(soup_dt_maylove != None):
		for item in soup_dt_maylove:
			if(item.a == None):
				continue
			new_req_url = base_content.music_root_path + item.a['href']
			#print('可能喜欢：'+new_req_url)
			add_url_toreqlist(new_req_url)

def get_music_maylove(soup):
	#每一首歌曲的右边都有可能喜欢，解析方式和电台的一样
	get_dt_maylove(soup)

#----------------------- 获取歌曲页面的方法
def get_dtmusic(soup):
	soup_dt = soup.find_all('div',class_ = 'tt f-thide')
	#print(soup_dt)
	if(soup_dt != None):
		for item in soup_dt:
			new_req_url = base_content.music_root_path + item.a['href']
			#print('电台：'+new_req_url)
			add_url_tomusiclist(new_req_url)

def get_music(soup):
	musiclist_ul = soup.find('ul',class_ = 'f-hide')
	index_number = 0
	if(musiclist_ul != None):
		for music_item in musiclist_ul.children:
			if(not isinstance(music_item,Tag)):
				continue
			index_number += 1
			musc_url = base_content.music_root_path + music_item.a['href']
			add_url_tomusiclist(musc_url)
		print('此次循环获取到歌曲数量：'+str(index_number))

#------------------- 主要的循环函数

def resolve_html_request(html_url):
	#线程随机暂停
	time.sleep(random.uniform(0.1,2))
	#print(html_url)
	#开始正式解析
	http_response = None
	try:
		http_response = requests.get(html_url,headers = base_content.Headers,timeout = 10)
	except Exception as e:
		print('request %s error,pelase check url'%(html_url,))
		return

	http_response.encoding = base_content.Encoding
	html_text = http_response.text
	soup = BeautifulSoup(html_text,'html.parser')
	save(html_url,html_text)

	# #查找 热门，最新
	try:
		get_hotornew(soup)
	except Exception as e:
		raise e
	

	# #查找翻页
	try:
		get_page(soup)
	except Exception as e:
		raise e
	

	#发现音乐
	try:
		get_findmusic(soup)
	except Exception as e:
		raise e
	

	#歌单列表选择分类
	try:
		get_song_list_class(soup)
	except Exception as e:
		raise e
	

	#遍历榜单
	try:
		get_toplist(soup)
	except Exception as e:
		raise e
	

	#获取推荐歌单
	try:
		get_recomment(soup)
	except Exception as e:
		raise e
	

	#获取电台列表
	try:
		get_dtlist(soup)
	except Exception as e:
		raise e
	

	#获取推荐节目
	try:
		get_dtprogram(soup)
	except Exception as e:
		raise e
	

	#电台列表选择分类
	try:
		get_dt_list_class(soup)
	except Exception as e:
		raise e
	

	#电台排行榜
	try:
		get_dt_toplist(soup)
	except Exception as e:
		raise e
	

	#电台页面-你可能也喜欢
	try:
		get_dt_maylove(soup)
	except Exception as e:
		raise e
	

	#歌曲页面- 可能喜欢
	try:
		get_music_maylove(soup)
	except Exception as e:
		raise e
	

	#--------------------------------------------
	#---------------- 查找歌单或者歌曲 -----------
	#--------------------------------------------
	#遍历歌单列表从其中查找 歌曲并添加
	try:
		get_songlist(soup)
	except Exception as e:
		raise e
	
	#遍历电台列表，从其中查找 歌曲并添加
	try:
		get_dtmusic(soup)
	except Exception as e:
		raise e
	

	# #查找 ul 中的歌曲
	try:
		get_music(soup)
	except Exception as e:
		raise e
	




def while_html_request_list():
	base_content.html_req_list[start_url] = 0
	while_index = 0
	is_test = False
	while True:
		try:
			is_new_url = False
			for req_item in base_content.html_req_list:
				if(base_content.html_req_list[req_item] != 0):
					continue
				is_new_url = True
				base_content.html_req_list[req_item] = 1

				resolve_html_request(req_item)
				#print('放置为 1：'+req_item)
				if(is_test):
					break
				if(len(base_content.music_url_list)>20):
					break

			#如果循环遍历发现没有新链接
			#为了防止 list 循环时数据增加错误
			#所以多遍历一次
			if(not is_new_url):
				while_index += 1
			else:
				while_index = 0

			if(while_index >= 2):
				break

			if(is_test):
				break
				
			if(len(base_content.music_url_list)>20):
				break
		except RuntimeError as e:
			pass
		except Exception as e:
			while_index = 0
			base_content.is_while_html = False
			raise e

	base_content.is_while_html = False

	print('req_length:'+str(len(base_content.html_req_list)))


def sigint_mothed(signum, frame):
	#print('sigint')
	print("receive a signal:%d , frame:%s"%(signum,signum))
	exit()

#注册监听线程方法
signal.signal(signal.SIGINT,sigint_mothed)



#创建其他执行线程
commentresolve_thread = threading.Thread(target = commentresolve.start_thread)
commentresolve_thread.setDaemon(True)

#启动线程解析 歌单，歌曲列表，歌曲
commentresolve_thread.start()

while_html_request_list()
#等待子线程完成
while True:
	if(commentresolve_thread.isAlive()):
		time.sleep(1)
	else:
		break



