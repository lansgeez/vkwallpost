import asyncio
from datetime import datetime
from vkwave.api import Token, BotSyncSingleToken, API
from vkwave.bots import  WallPhotoUploader
from vkwave.client import AIOHTTPClient
import time 
import random   

client = AIOHTTPClient()
api = API(clients=client, tokens=BotSyncSingleToken(Token("VKTOKEN")),)

f = open('date/sort.txt','r')
urls = f.readlines()
f.close()

def timepost(unixt = float):
    convertt = time.gmtime(unixt+10800)
    message = str
    night = False

    if convertt.tm_hour==23:
        night = True
        message = "Доброй ночи!"
    if night == False:
        message = ""
        
    while convertt.tm_hour>=0 and convertt.tm_hour < 7:
        unixt += 3600
        convertt = time.gmtime(unixt+10800)
        message = "Доброго утра!"
    array = [unixt, message] 

    return array

async def wall_upload():
    
    unixt = time.time() + 3600
    img=[]
    k=0
    group = -1 #GROUP ID

    for i in urls:
        if 'png' in i or 'jpeg' in i or 'gif' in i or 'jpg' in i :
            img.append(i.strip('\n'))
        else:
            try:
                src = i.strip('\n')
                print('------------------------------')
                print('Ссылка на изображение -', img)
                print('Ссылка на пост -', src)

                photo = await WallPhotoUploader(api.get_context()).get_attachments_from_links(
                group_id=group,
                links=img,)
                array = timepost(unixt)
                unixt = float(array[0])
                message = str(array[1])

                print("Время поста: ",time.ctime(unixt))

                if message != "":
                    print("Сообщение: ", message)

                await api.get_context().wall.post(owner_id=group,  attachments=photo, copyright=src, publish_date=unixt, message = message)

                unixt += random.randint(3450, 3750)
                k += 1

                print('Выставил -', k, 'пост')
                print('------------------------------')

                img.clear()
                time.sleep(1)  
                
            except Exception as exc: 
                print('------------------------------')
                print('Photo: ',photo)
                print(exc)
                print('Ошибка. Пост не выставлен')
                img.clear()
                time.sleep(1) 
                
    print('\n------------------------------')
    print('Готово, было выставлено -', k, 'пост(ов)')
    print('------------------------------\n\n')

asyncio.get_event_loop().run_until_complete(wall_upload())