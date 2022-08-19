import telebot
import requests
from requests import request
from bs4 import BeautifulSoup as soup
import time
import pickle

import re
import time
import os.path
import difflib 
from collections import OrderedDict
import itertools

#local imports
from latest_url import get_latest_movirulz_url
from get_torrent import get_torrent


try:
  API_KEY = '5689470925:AAEsWQjHO3mhnfPmXFOqg7bQvrkBGfq-vOs'
  bot = telebot.TeleBot(API_KEY)

  @bot.message_handler(commands=['Download_Movie'])
  def download_movie(message):
      
      def downmovie_util_3(user_quality_choice):
        user_quality_choicee = user_quality_choice.text
        user_quality_choiceee = int(user_quality_choicee)
        
        title_of_movie = movie_name_to_download
        
        with open('magnets.pkl', 'rb') as f:
            magnets = pickle.load(f)
        with open('torrents.pkl', 'rb') as ff:
            torrents = pickle.load(ff)
        try:   
            title_of_movie = movie_name_to_download+"_"+torrents[user_quality_choiceee-1][1]+"_"+torrents[user_quality_choiceee-1][0]
                
            magnet_link = magnets[torrents[user_quality_choiceee-1][0]]
            with open(f'torrents/{title_of_movie}.txt','w') as fp:
                fp.write(magnet_link)
            
            bot.send_message(message.chat.id,"Getting requested magnet link....")
            time.sleep(0.2)
            bot.send_message(message.chat.id,"Obtaining Metadata...")
            time.sleep(0.2)
            bot.send_message(message.chat.id,"Calculating seeds and peers....")
            bot.send_message(message.chat.id,"Here is Your Requested Magnet Link, Enjoy your movie...")

            torrent_hash = magnet_link[20:60].upper()
            torrent_download_link_= f"https://itorrents.org/torrent/{torrent_hash}.torrent"


            torrent_response = requests.get(torrent_download_link_, stream=True, headers={'User-agent': 'Mozilla/5.0'})
            open(f'torrents/{title_of_movie}.torrent',"wb").write(torrent_response.content)
            torrent_file = open(f'torrents/{title_of_movie}.torrent', 'rb')
            bot.send_document(message.from_user.id, torrent_file)
            bot.send_message(message.chat.id,"If the above torrent fails to add , paste this magnet url in your torrent client")
            bot.send_message(message.chat.id,magnet_link)
        except:
            bot.send_message(message.chat.id,"You Entered Wrong Option Mate, Try Again from /Download_Movie")

      
      
      def downmovie_util_2(user_movie_choice):
        user_movie_choiceee = user_movie_choice.text
        user_movie_choicee = int(user_movie_choiceee)
        
        with open('close_results_ls.pkl', 'rb') as f:
            close_results_ls = pickle.load(f)
        try:
            global movie_name_to_download
            movie_name_to_download = close_results_ls[user_movie_choicee-1]
            
            torrents,magnets = get_torrent(movie_name_to_download)
            
            with open('magnets.pkl', 'wb') as f:
                pickle.dump(magnets, f)
            with open('torrents.pkl', 'wb') as ff:
                pickle.dump(torrents, ff)
            
            quality_size="";c=1
            for ___ in torrents:
                quality_size+=f"{c}.{___[1]} <---> {___[0]}\n"
                c+=1
            
            print_2 = f"I found the following qualities for {movie_name_to_download}"
            bot.send_message(message.chat.id,print_2)
            bot.send_message(message.chat.id,quality_size)
            user_quality_choice = bot.send_message(message.chat.id,f"Enter Number of your desired quality from 1-{c-1}: ")
        
            bot.register_next_step_handler(user_quality_choice, downmovie_util_3)
        except:
            bot.send_message(message.chat.id,"You Entered Wrong Option Mate, Try Again from /Download_Movie")
    
      def downmovie_util(movie_name):
        movierulz_url = get_latest_movirulz_url('movierulz')+'?s='
    
        movie = movie_name.text.replace(" ","%20")

        url = movierulz_url+movie

        response = request('GET',url)
        bot.send_message(message.chat.id,"Searching for the query....Please Be Patient we are low on server power...")
        
        html_page_soup_1 = soup(response.text, "html.parser")
        search_container = html_page_soup_1.findAll("div", {"class": "content home_style"})
        try:
            movie_titles =  search_container[0].findAll("b")
        
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
            
            print_1 = f"I found a Couple results matching {movie_name.text}";count=1
            bot.send_message(message.chat.id, print_1)
            
            for __ in close_results:
                movie_name_string = f"{count}.{close_results[__]}"
                count+=1
                bot.send_message(message.chat.id,str(movie_name_string))
            close_results_ls = [*close_results.values()]
            
            with open('close_results_ls.pkl', 'wb') as f:
                pickle.dump(close_results_ls, f)
                
            user_movie_choice = bot.send_message(message.chat.id,f"Enter Number of your desired movie from 1-{count-1}: ")
            
            bot.register_next_step_handler(user_movie_choice, downmovie_util_2)
        except:
            bot.send_message(message.chat.id,"could'nt find movie, check for spelling mistake and try again with name and year of release of movie \n\n Eg: Pokiri 2006 or RRR 2022")
        
        
      dir = 'torrents/'
      for f in os.listdir(dir):
          os.remove(os.path.join(dir, f))
        
      movie_name = bot.send_message(message.chat.id,"Enter Movie Name: ")
        
      bot.register_next_step_handler(movie_name, downmovie_util)
  
  @bot.message_handler(commands=['start'])
  def welcome_message(message):
    greet_message = """
  Hey there! Welcome to Filmory-X Bot!
  
  Available Functions :
  
  /Download_Movie -- returns a magnet link of requested movie
  
    """
    bot.send_message(message.chat.id, greet_message)
  
  bot.polling(none_stop=True)
    
except Exception as ee:
    print(ee)