from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import time
import urllib.request
import random
import os
import telebot

bot_token = '6172233153:AAE2yZFTGz_TOiR-c9RQ9yfbQoMIRqbJ5-Y'

bot = telebot.TeleBot(bot_token)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
	chat_id=message.chat.id
	msg=message.text
	if "https://www.instagram.com" in msg:
		bot.send_message(chat_id,"pasring link...")
		spl_url=msg.split('?')
		_url=spl_url[0]
		vid=get_source(_url)
		_link=get_link(vid)
		bot.send_message(chat_id,f"source link:\n {_link}")
		caption=get_caption(vid)
		bot.send_message(chat_id,caption)
	elif "https://www.instagram.com" not in msg:
		bot.send_message(chat_id,"send a valid link")
    
    

bot.polling()


def get_source(link):
	with sync_playwright() as p:
		browser = p.chromium.launch(headless=True)
		context = browser.new_context(user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36')
		page = context.new_page()
		page.goto(link)
		page.wait_for_timeout(10000)
		vid=page.inner_html("*")
		page.close()
		return vid

def get_link(vid):
	soup = BeautifulSoup(vid, 'html.parser')
	ln=soup.find_all("video")
	for i in ln:
		i=str(i)
		i=i.split()
		_filter=i[6]
		_filter=_filter.replace('src="','')
		_filter=_filter.replace('amp;','')
		_filter=_filter.replace('\\n','')
		link=_filter.replace('">\',','')
		return link

def gen_caption():
	_cats=['Cute cats','Lovely cats','Fluffy cats','Playful cats','Mischievous cats','Cuddly cats','Lazy cats','Elegant cats','Regal cats','Mysterious cats','Enchanting cats','Graceful cats','Majestic cats','Curious cats','Gentle cats','Grumpy cats']
	emoji=['😆', '😅', '😂', '🤣', '😉', '😌', '😍', '🥰', '😘', '😗', '😙', '😚', '😋', '😛', '😝', '😜', '🤪', '😎', '🤩', '🐱', '🦁', '🐈', '💥', '🔥', '⭐', '🌟', '✨', '⚡', '❤', '🔥', ' ']
	_cap=random.choice(_cats)
	_emoji=random.choice(emoji)
	choi1=_cap+' '+_emoji
	choi2=_cap+' '+_emoji+random.choice(emoji)
	choi3=_emoji+' '+_cap
	choi4=_emoji+_cap
	choices=[choi1,choi2,choi3,choi4]
	final_choi = random.choice(choices)
	return final_choi



def get_caption(vid):
	soup = BeautifulSoup(str(vid), 'html.parser')
	tags = soup.find("h1", {"dir": "auto"})
	try:
		tags=tags.text
	except Exception:
		tags=str(tags)

	if tags == "None":
		print("no caption here")
		print("generating caption....")
		_caption=gen_caption()
		return _caption

	else:
		_filter=tags.replace('\\','')
		_filter=_filter.replace('\\n','')
		_filter=_filter.replace('instagram','')
		_filter=_filter.replace('Instagram','')
		_filter=_filter.replace('INSTAGRAM','')
		_filter=_filter.replace(':','')
		_filter=_filter.replace(':-','')
		if "@" in _filter:
			_filter=_filter.split("@")
		else:
			_filter=_filter.split("#")
		
		return _filter[0]



def gen_file_name():
	file_name = f'insta_video{random.randint(1736571,183618900)}.mp4'
	return file_name

file_name=gen_file_name()

def remove_vid(file_name):
	os.remove(file_name)

def download_vid(link,file_name):	 
	dwn_link=link
	urllib.request.urlretrieve(dwn_link, file_name)

#vid=get_source(link)
#_link=get_link(vid)
#caption=get_caption(vid)
#print(caption)
#download_vid(link,file_name)
#remove_vid(file_name)
