import requests
from bs4 import BeautifulSoup
import base_content
import os
from bs4.element import Tag
import commentresolve


'''
从歌单中，解析出歌曲列表
'''

def add_url_tolist(url):
	if(url not in base_content.music_url_list):
		base_content.music_url_list[url] = 0
		print(url)
		return True
	else:
		return False

def resolve_url_musiclist(songlist):

	http_response = requests.get(songlist,headers = base_content.Headers)
	http_response.encoding = base_content.Encoding

	#读取内容并加载到解析器中
	html_text = http_response.text
	soup = BeautifulSoup(html_text,'html.parser')
	save(songlist,html_text)

	musiclist_ul = soup.find('ul',class_ = 'f-hide')
	index_number = 0
	if(musiclist_ul != None):
		for music_item in musiclist_ul.children:
			if(not isinstance(music_item,Tag)):
				continue
			index_number += 1
			musc_url = base_content.music_root_path + music_item.a['href']
			add_url_tolist(musc_url)
	print('此次循环获取到歌曲数量：'+str(index_number))




def save(http_url,text):
	urls = http_url.split('/')
	dir_ = os.path.join(os.path.abspath('.'),'html_file')
	if not os.path.exists(dir_):
		try:
			os.mkdir(dir_)
			name = os.path.join(dir_,urls[len(urls)-1])
			open(name,'w',encoding = base_content.Encoding).write(text)
		except Exception as e:
			print('save text error')
			return


def start_thread():
	while(base_content.is_while_songlist):
		try:
			for music_item in base_content.song_url_list:
				if(base_content.song_url_list[music_item] != 0 ):
					continue

				resolve_url_musiclist(music_item)
				base_content.song_url_list[music_item] = 1
		except RuntimeError as e:
			pass
		except Exception as e:
			pass

	print('循环获取歌单列表完成')
	for music_item in base_content.song_url_list:
		if(base_content.song_url_list[music_item] != 0 ):
			continue
				
		resolve_url_musiclist(music_item)
		base_content.song_url_list[music_item] = 1

	base_content.is_while_musiclist = False