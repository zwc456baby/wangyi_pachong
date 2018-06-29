import requests
from bs4 import BeautifulSoup
import musicresolve
import base_content


'''
从一个链接中解析出歌单
'''
def add_url_tolist(url):
	if(url not in base_content.song_url_list):
		base_content.song_url_list[url] = 0
		print(url)
		return True
	else:
		return False

#遍历歌单列表
def resolve_url_songlist(music_url):

	http_response = requests.get(music_url,headers = base_content.Headers)
	http_response.encoding = base_content.Encoding

	#读取内容并加载到解析器中
	html_text = http_response.text
	soup = BeautifulSoup(html_text,'html.parser')
	#print(html_text)
	musicresolve.save(music_url,html_text)

	songlist_a = soup.find_all('a',class_ = 'tit f-thide s-fc0')
	
	if(songlist_a != None and len(songlist_a)>0):
		for songlist_item in songlist_a:
			music_ls_url = base_content.music_root_path + songlist_item['href']
			add_url_tolist(music_ls_url)
	print('此次循环获取到歌单数量：'+str(len(songlist_a)))

def start_thread():
	while base_content.is_while_html:
		try:
			for html_url_item in base_content.htm_url_list:
				if(base_content.htm_url_list[html_url_item] != 0):
					continue
				resolve_url_songlist(html_url_item)
				base_content.htm_url_list[html_url_item] = 1
		except RuntimeError as e:
			pass
		except Exception as e:
			pass

	print('遍历网页链接完成')
	for html_url_item in base_content.htm_url_list:
		if(base_content.htm_url_list[html_url_item] != 0):
			continue
		resolve_url_songlist(html_url_item)
		base_content.htm_url_list[html_url_item] = 1

	base_content.is_while_songlist = False