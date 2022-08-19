from requests import request
from bs4 import BeautifulSoup as soup


def get_torrent(movie_name):
    movie = movie_name.replace("[","")
    movie = movie.replace("]","")
    movie = movie.replace(" ","-")
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
    keyorder = ['8K','4K', '4K 2160p','4K SDR','1080p','1440p','720p', '480p', '320p','240p','144p']
    torrent_info = sorted(torrent_info.items(), key=lambda i:keyorder.index(i[1]))

    for link in container:
        magnet_link_ls.append(link.get('href'))

    for i,j in zip(magnet_link_ls,torrent_info):
        magnets.update({j[0]:i})

    return torrent_info,magnets