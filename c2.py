#control your C2 server through a telegram text
#replace 'BOT_TOKEN' with your bot token

import subprocess, os, sys
from colorama import Fore, Back, Style
import logging
import telegram
import time
import shlex
import apt

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
                chat_id = bot.get_updates()[-1].message.chat_id
                bot.send_message(chat_id=chat_id, text="running...")
                return x.message.text


def sendTelegram(result):
    
    string = string + result
   
    chat_id = bot.get_updates()[-1].message.chat_id
    bot.send_message(chat_id=chat_id, text=string)

#badly done need to fix
def install_package(package_name, chat_id):
    cache = apt.cache.Cache()
    cache.update()
    cache.open()
    try:
        pkg = cache[package_name]
    except:
        text = "package not found..."
        bot.send_message(chat_id=chat_id, text=text)
        return
        
    if pkg.is_installed:
        text = "package is already installed..."
        bot.send_message(chat_id=chat_id, text=text)
    else:
        pkg.mark_install()
        try:
            cache.commit()
            text = "package " + package_name + " installed..."
            bot.send_message(chat_id=chat_id, text=text)
        except:
            text = "error: check spelling"
            bot.send_message(chat_id=chat_id, text=text)

def main():
    print("waiting for a text message...")
    resultstr = WaitGetHost()
    resultstr = shlex.split(resultstr)
    #resultstr.split()

    #default insert tor proxy
    if not 'np' in resultstr:
        resultstr.insert(0, 'proxychains')
    
    #get rid of no-proxy in commands
    elif 'np' in resultstr:
        resultstr.pop(0)

    if 'install' in resultstr:
        install_in = resultstr.index('install')
        pkg_inst = resultstr[install_in + 1]
        chat_id = bot.get_updates()[-1].message.chat_id
        output = "installing package ..." + pkg_inst
        bot.send_message(chat_id=chat_id, text=output)
        chat_id = bot.get_updates()[-1].message.chat_id
        install_package(pkg_inst, chat_id)
        main()
     

    #fetch latest human chat
    chat_id = bot.get_updates()[-1].message.chat_id
    
    #send command
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