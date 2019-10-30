#control your C2 server through a telegram text
#replace 'BOT_TOKEN' with your bot token

import subprocess, os, sys
from colorama import Fore, Back, Style
import logging
import telegram
import time
import shlex

if os.getuid() != 0:
    print("please run as root...")
    sys.exit(1)

bot = telegram.Bot(token='BOT_TOKEN')


#waits for to recieve a new text, returns the latest text
def WaitGetHost():
    while(True):
        chat = bot.get_updates()[-1].message.message_id
        time.sleep(5)
        chat2 = bot.get_updates()[-1].message.message_id
        if chat != chat2:
            print("new message recieved:")
            var = bot.get_updates(offset=-1)
            for x in var:
                print (x.message.text)
                return x.message.text


def sendTelegram(result):
    
    string = string + result
   
    chat_id = bot.get_updates()[-1].message.chat_id
    bot.send_message(chat_id=chat_id, text=string)


def main():
    print("waiting for a text message...")
    resultstr = WaitGetHost()
    resultstr = shlex.split(resultstr)
    #resultstr.split()
    chat_id = bot.get_updates()[-1].message.chat_id
    resultstr.insert(0, 'proxychains')
    
    result = subprocess.run(resultstr, stdout=subprocess.PIPE)
    output = str(result.stdout)
    output = output[:1500]
    
    print("output: ", output)
    
    chat_id = bot.get_updates()[-1].message.chat_id
    bot.send_message(chat_id=chat_id, text=output)
    #except:
     #   bot.send_message(chat_id=chat_id, text="command couldnt run...")
    main()
if __name__ == "__main__":
    main()