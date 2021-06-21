# © TamilBots 2021-22

from pyrogram import Client, filters
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
import youtube_dl
from youtube_search import YoutubeSearch
import requests

import os
from config import Config

bot = Client(
    'SongPlayRoBot',
    bot_token = Config.BOT_TOKEN,
    api_id = Config.API_ID,
    api_hash = Config.API_HASH
)

## Extra Fns -------------------------------

# Convert hh:mm:ss to seconds
def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60 ** i for i, x in enumerate(reversed(stringt.split(':'))))


## Commands --------------------------------
@bot.on_message(filters.command(['start']))
def start(client, message):
    TamilBots = """ Hoşgeldin [{}](tg://user?id={}), 
**BEN DJ NEFİSE DESTEKÇİM @Azerbesk.
Beni ᴇʙᴛ | Nefise🌼 İçin Özel Olarak Tasarladı. O Yüzden Başka Gruplara Eklenmemi Yasakladı. O Özel İnsanlara Güzel Hediyeler Vermeyi Sever . 🌹🌸**
[.](https://telegra.ph/file/a05f929282c3158544d5d.mp4)
"""
    message.reply_text(
        text=TamilBots, 
        quote=False,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("🙎🏻‍♀️ Nefise", url="https://t.me/YineBenHakliyim"),
                    InlineKeyboardButton("🙎🏻‍♂️ Yapımcı", url="https://t.me/Azerbesk")
                ]
            ]
        )
    )

@bot.on_message(filters.command(['e']))
def a(client, message):
    query = ''
    for i in message.command[1:]:
        query += ' ' + str(i)
    print(query)
    m = message.reply('👸🏻 DJ Nefise Şarkıyı Gönderiyor Biraz Bekle Tatlım 🌼')
    ydl_opts = {"format": "bestaudio[ext=m4a]"}
    try:
        results = []
        count = 0
        while len(results) == 0 and count < 6:
            if count>0:
                time.sleep(1)
            results = YoutubeSearch(query, max_results=1).to_dict()
            count += 1
        # results = YoutubeSearch(query, max_results=1).to_dict()
        try:
            link = f"https://youtube.com{results[0]['url_suffix']}"
            # print(results)
            title = results[0]["title"]
            thumbnail = results[0]["thumbnails"][0]
            duration = results[0]["duration"]

            ## UNCOMMENT THIS IF YOU WANT A LIMIT ON DURATION. CHANGE 1800 TO YOUR OWN PREFFERED DURATION AND EDIT THE MESSAGE (30 minutes cap) LIMIT IN SECONDS
            # if time_to_seconds(duration) >= 1800:  # duration limit
            #     m.edit("Exceeded 30mins cap")
            #     return

            views = results[0]["views"]
            thumb_name = f'thumb{message.message_id}.jpg'
            thumb = requests.get(thumbnail, allow_redirects=True)
            open(thumb_name, 'wb').write(thumb.content)

        except Exception as e:
            print(e)
            m.edit('🥺 Şarkıyı Bulamadım')
            return
    except Exception as e:
        m.edit(
            "HATA! 👉🏼 /e Şarkı Adı"
        )
        print(str(e))
        return
    m.edit("Çok Beklersin")
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            audio_file = ydl.prepare_filename(info_dict)
            ydl.process_info(info_dict)
        rep = f'Şarkı Hazır Bana Teşekkür Et 🙆🏻‍♀️'
        secmul, dur, dur_arr = 1, 0, duration.split(':')
        for i in range(len(dur_arr)-1, -1, -1):
            dur += (int(dur_arr[i]) * secmul)
            secmul *= 60
        message.reply_audio(audio_file, caption=rep, parse_mode='md',quote=False, title=title, duration=dur, thumb=thumb_name)
        m.delete()
    except Exception as e:
        m.edit('❌ Hata Yardım İçin @Azerbesk ❤️')
        print(e)
    try:
        os.remove(audio_file)
        os.remove(thumb_name)
    except Exception as e:
        print(e)

bot.run()
