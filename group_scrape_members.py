from telethon import TelegramClient, events
from telethon.errors import SessionPasswordNeededError

# to get members
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch
from telethon.tl.types import (PeerChannel)

# to get messages
from telethon.tl.functions.messages import (GetHistoryRequest)
from telethon.tl.types import (PeerChannel)

from telethon import utils
from telethon.tl import functions, types

import re
import os
import string
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
import csv

from telethon.sessions import StringSession
import os

from dotenv import load_dotenv

load_dotenv()

api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')

#phone = '+658371431'
# Create the client and connect
client = TelegramClient('anon', api_id, api_hash)
client.start()
if not client.is_user_authorized():
    client.send_code_request(phone)
    try:
        client.sign_in(phone, input('Enter the code: '))
    except SessionPasswordNeededError:
        client.sign_in(password=input('Password: '))

chats = []
last_date = None
chunk_size = 200
groups=[]
result = client(GetDialogsRequest(
             offset_date=last_date,
             offset_id=0,
             offset_peer=InputPeerEmpty(),
             limit=chunk_size,
             hash = 0
         ))
chats.extend(result.chats)
for chat in chats:
    try:
        if chat.megagroup== True:
            groups.append(chat)
    except:
        continue

# id and select group
print('Choose a group to scrape members from: \n')
i=0
for g in groups:
    print(str(i) + '- ' + g.title)
    i+=1

g_index = input("\n Enter a Number: ")
target_group=groups[int(g_index)]

print("Configuring Scrape for " + str(target_group.title) + ": ")
csv_name = input("input the name of the file that will be generated. if blank, default name of vasmembers will be used\n")
csv_name = csv_name+'.csv' if csv_name!='' else 'vasmembers.csv'
currdir = os.getcwd()
filepath = os.path.join(currdir, csv_name)

print('Fetching Members... \n')
all_participants = []
all_participants = client.get_participants(target_group, aggressive=True)

# save group member details
print('Saving In file... \n')
with open(filepath,"w",encoding='UTF-8') as f:
    writer = csv.writer(f,delimiter=",",lineterminator="\n")
    writer.writerow(['username','user id', 'access hash','name','group', 'group id'])
    for user in all_participants:
        if user.username:
            username= user.username
        else:
            username= ""
        if user.first_name:
            first_name= user.first_name
        else:
            first_name= ""
        if user.last_name:
            last_name= user.last_name
        else:
            last_name= ""
        name= (first_name + ' ' + last_name).strip()
        writer.writerow([username,user.id,user.access_hash,name,target_group.title, target_group.id])      
print(str(target_group.title) + ' members scraped successfully and saved in ' + csv_name + '\n')

# print output csv name
print('Created CSV: ' + str(filepath) +'')
#all_participants = client.get_participants('1038947175', aggressive=True)
#print(all_participants)