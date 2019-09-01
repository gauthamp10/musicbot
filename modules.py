from __future__ import unicode_literals
import json
import random
import requests
import youtube_dl
import urllib

from bs4 import BeautifulSoup

#----------------------------------------------------------------
def print_help():
    text='Example: All of stars\n'
    return text

def flag(code):
    code = code.upper()
    return chr(ord(code[0]) + OFFSET) + chr(ord(code[1]) + OFFSET)

#-----------------------------------------------------------------

def get_song_data(song):
    query = urllib.parse.quote(song+' song')
    url = "https://www.youtube.com/results?search_query=" + query
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
    headers = {'User-Agent': user_agent}
    response = requests.get(url,headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    vid_list=list()
    title_list=list()
    for vid in soup.findAll(attrs={'class':'yt-uix-tile-link'}):
        if vid['href'].startswith('/watch'):
            vid_list.append('https://www.youtube.com' + vid['href'][:20])
            title_list.append(vid.text)
        else:
            pass
    vid=dict(zip(vid_list, title_list))
    ydl_opts={}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        meta = ydl.extract_info(vid_list[0], download=False)
    for video in meta['formats']:
        if video['format_id']=='140':
            vid_url=video['url']       
    return meta['title'],meta['thumbnail'],vid_url
    
def get_ist():
    ist=requests.get('http://worldtimeapi.org/api/timezone/Asia/Kolkata').json()
    return ist["datetime"]