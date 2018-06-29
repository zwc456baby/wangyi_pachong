
music_root_path = 'http://music.163.com'

is_while_html = True
#is_while_songlist = True
#is_while_musiclist = True

html_req_list = {}
#htm_url_list = {}
#main_url_list = {}
#song_url_list = {}
music_url_list = {}

#编码
Encoding = 'utf-8'

MusicCookie = 'Province=021; City=021; __gads=ID=5822eb8ec2e4850b:T=1529640222:S=ALNI_Mbx09vblh_SuZ6okluhbqbkAmmFcQ; UM_distinctid=16425a96b1d33f-03515dac6d82ee-601a147a-1fa400-16425a96b1e23b; vjuids=6125d5b3e.16425a976ac.0.8391d64b1a0b7; vjlast=1529640220.1529640220.30; _ntes_nnid=cf1be79919a890f2830d1402cd284fca,1529640220343; ne_analysis_trace_id=1529640220351; s_n_f_l_n3=c263f26d5e533c7c1529640220357; _ntes_nuid=cf1be79919a890f2830d1402cd284fca; _antanalysis_s_id=1529640220523; vinfo_n_f_l_n3=c263f26d5e533c7c.1.0.1529640220356.0.1529640302466; _iuqxldmzr_=32; __utmc=94650624; __utmz=94650624.1529647949.1.1.utmcsr=youtiy.com|utmccn=(referral)|utmcmd=referral|utmcct=/detail_223.html; WM_TID=8tfhQiKEx6N4i77%2FCPVEbIh8OADjKS49; JSESSIONID-WYYY=fGmwuH%2FdGN%2BrT9E9lAOBFfkrkMPgCx%2B9a%2Fdi7Ar3bOHVXUSyo8cIq8XqRvDObbeF2Xd4JwGdxX82f31KbAlvFNGdn6tiNHlgWzVXh%2FF1Zkd5aa5EMmdJ0s%2FPBUibliZ5iaPeAYFni6w0Y%2BOoFPZCX%2FKQi6viJ9fB3jHpkJhZmjEG0ouY%3A1530088523236; __utma=94650624.186652425.1529647949.1530081234.1530086877.3; __utmb=94650624.8.10.1530086877'

#http请求头
Headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
    'Origin':'http://music.163.com',
               }


MusicItemHeaders = {
	'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
    'Referer':'https://music.163.com/artist?id=768306&_hash=songlist-28167631',
    'Cookie':MusicCookie,
    'Host':'music.163.com',
    'Upgrade-Insecure-Requests':'1',
    'Connection':'keep-alive',
    'Cache-Control':'max-age=0',

}


GetCommentHeaders = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
    'Origin':'https://music.163.com',
    'Referer':'https://music.163.com/song?id=526116065',
               }

# 这两个参数是加密参数，似乎不需要更改就可以一直使用
datas_params = '53HitGK8xWgDlHt39AeUFxdxK2GCMHNUSR9rDb3U3E8ytvjCUAzNf7Wk8CFOBYidssJVj78Iymon0AXsqsp73GfseXH71m7L/xttLtzvdgaM81VCOdcaXR2m+J3/DdlbFy6hsjhRCB9b1bF9sWidXjsVBZrR44CjjEKQ/vrUACW5LIr4hjmZ0F61VkB8EXcr'
datas_encSecKey = '9d03a31d61af4da8863ef8e9b94971f67b9e6c008e30f406f01374b8b2a82c395e3826d654f8638e6db4492a1eeb511fa6b3535c1bf5e208e7f70366136cca60df50dff4c6e9868793b5036c3c268b64797c2a4739e32a0e92212ba432e9d88bd73c5c7996f0a5f640bcd79b125688c8193d3a34e5a8586e8841667d96e40777'

GetCommentBaseUrl = 'https://music.163.com/weapi/v1/resource/comments/R_SO_4_%s?csrf_token='

GetDTCommentBaseUrl = 'https://music.163.com/weapi/v1/resource/comments/A_DJ_1_%s?csrf_token='