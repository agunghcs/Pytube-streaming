
import telepot
import os
from random import randint
from youtubesearchpython import VideosSearch
from dotenv import load_dotenv
from os.path import join, dirname
from pytube import YouTube

dotenv_path = join(dirname(file), '.env')
load_dotenv(dotenv_path)
TOKEN = os.environ.get("TOKEN")
bot = telepot.Bot(TOKEN)

class Music:
    def init(self, user_input, msg):
        self.chat = msg['chat']['id']
        self.user_input = user_input[6:]

    def search_music(self, user_input):
        return VideosSearch(user_input, limit=1).result()

    def get_link_title(self, result):
        link = result['result'][0]['link']
        title = result['result'][0]['title']
        return link, title

    def get_duration(self, result):
        result = result['result'][0]['duration'].split(':')
        min_duration = int(result[0])
        split_count = len(result)
        return min_duration, split_count

    def download_music(self, file_name, link):
        yt = YouTube(link)
        stream = yt.streams.filter(only_audio=True, file_extension='mp4').first()
        stream.download(filename=file_name)

    def check_input(self, msg):
        user_input = msg['text'].replace('@TLMusicDownloader_bot', '')
        if user_input.startswith('/music'):
            if 'open.spotify.com' in user_input:
                bot.sendMessage(msg['chat']['id'], "‼️ *Oops! Bot tidak mendukung tautan Spotify!*\nCoba: '*/music* _judul lagu_' atau '*/music* _nama musisi - judul lagu_'", reply_to_message_id=msg['message_id'], parse_mode='Markdown')
            else:
                result = self.search_music(user_input)
                link, title = self.get_link_title(result)
                file_name = f"{title} - @TLMusicDownloader_bot_{str(randint(0, 999999))}.mp3"
                download_message = f"🎵 {title}\n🔗 {link}\n⬇️ Downloading..."
                
                try:
                    bot.sendMessage(msg['chat']['id'], download_message, reply_to_message_id=msg['message_id'])
                    self.download_music(file_name, link)
                    bot.sendAudio(msg['chat']['id'], audio=open(file_name, 'rb'), reply_to_message_id=msg['message_id'])
                    bot.sendMessage(msg['chat']['id'], "✅ Success!", reply_to_message_id=msg['message_id'])
                    
                    if os.path.exists(file_name):
                        os.remove(file_name)
                        
                except Exception as e:
                    bot.sendMessage(msg['chat']['id'], "❌ Error occurred during download process. Please try again later.", reply_to_message_id=msg['message_id'])
        else:
            bot.sendMessage(msg['chat']['id'], "‼️ *Oops! Perintah tidak valid!* Coba: '*/music* _judul lagu_' atau '*/music* _nama musisi - judul lagu_'", reply_to_message_id=msg['message_id'], parse_mode='Markdown')

def start_new_chat(msg):
    music = Music(msg['text'], msg)
    music.check_input(msg)

bot.message_loop(start_new_chat, run_forever=True)
