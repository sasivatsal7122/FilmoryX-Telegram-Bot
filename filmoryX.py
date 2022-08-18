from requests import request
from bs4 import BeautifulSoup as soup
import re
import libtorrent
import time
import sys
import os.path
import difflib 
from collections import OrderedDict
import itertools
from pprint import pprint
#local imports
from latest_url import get_latest_movirulz_url
from mg2tor import mag2tor



def get_torrent(movie_name):
    
    movie = movie_name.replace(" ","-")
    base_url= "https://ww5.7movierulz.tc/"
    url = base_url+movie
    response = request('GET',url)
    
    html_page_soup = soup(response.text, "html.parser")
    container = html_page_soup.findAll("a", {"class": "mv_button_css"})
    movie_title = html_page_soup.findAll("h2", {"class": "entry-title"})

    torrent_quality = html_page_soup.findAll("small")
    movie_title = movie_title[0].text.strip()

    torrent_size_ls = [] ; torrent_resolution_ls = [] ; magnet_link_ls = [] ; magnets = dict()
    for i,torrent in enumerate(torrent_quality):
        if i%2==0:
            torrent_size_ls.append(torrent.text.strip())
        else:
            torrent_resolution_ls.append(torrent.text.strip())

    torrent_info = dict(zip(torrent_size_ls,torrent_resolution_ls))
    keyorder = ['8K','4K', '4K SDR','1080p','1440p','720p', '480p', '320p','240p','144p']
    torrent_info = sorted(torrent_info.items(), key=lambda i:keyorder.index(i[1]))

    for link in container:
        magnet_link_ls.append(link.get('href'))

    for i,j in zip(magnet_link_ls,torrent_info):
        magnets.update({j[0]:i})

    return torrent_info,magnets
    
def driver(movie_name):
    movierulz_url = get_latest_movirulz_url('movierulz')+'?s='
    
    movie = movie_name.replace(" ","%20")

    url = movierulz_url+movie

    response = request('GET',url)
    html_page_soup_1 = soup(response.text, "html.parser")
    search_container = html_page_soup_1.findAll("div", {"class": "content home_style"})
    try:
        movie_titles =  search_container[0].findAll("b")
    except:
        print("could'nt find movie")
    movie_title_ls = [] ; trimmed_movie_title_ls = []

    rep = {"Full": "", "Movie": "","Watch":" ","Online":"","Free":""}
    rep = dict((re.escape(k), v) for k, v in rep.items()) 
    pattern = re.compile("|".join(rep.keys()))

    for i in movie_titles:
        movie_title_ls.append(i.text.strip())
        trimmed_movie_name = pattern.sub(lambda m: rep[re.escape(m.group(0))],i.text.strip())
        trimmed_movie_title_ls.append(trimmed_movie_name.strip())
        
    if len(trimmed_movie_title_ls)==1:
        best_match = trimmed_movie_title_ls[0]
    else:
        best_match = difflib.get_close_matches(movie,trimmed_movie_title_ls,n=1,cutoff=0.2)[0]

    close_results=dict()
    for _ in trimmed_movie_title_ls:
        score = difflib.SequenceMatcher(None, _, best_match).ratio()
        close_results.update({score:_})
    close_results = OrderedDict(sorted(close_results.items(),reverse=True))   
    close_results = dict(itertools.islice(close_results.items(), 5))
    print(f"\n I found a Couple results matching {movie_name}");count=1
    for __ in close_results:
        print(f"{count}.{close_results[__]}");count+=1
    user_choice = int(input(f"Enter Number of your desired movie from 1-{count-1}: "))
    
    torrents,magnets = get_torrent(trimmed_movie_title_ls[user_choice-1])
    
    quality_size="";c=1
    for ___ in torrents:
        quality_size+=f"{c}.{___[1]} <---> {___[0]}\n"
        c+=1
    print(f"\nI found the following qualities for {movie_name}")
    print(quality_size)
    user_quality_choice = int(input(f"Enter Number of your desired quality from 1-{c-1}: "))
    print(magnets[torrents[0][user_quality_choice-1]])
    #mag2tor(trimmed_movie_title_ls[user_choice-1],magnets[torrents[0][user_quality_choice-1]])
    
    

if __name__=='__main__':
    user_movie = input("Enter Movie Name: ")
    driver(user_movie)
    