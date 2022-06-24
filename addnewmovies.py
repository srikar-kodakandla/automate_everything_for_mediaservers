from plexapi.myplex import MyPlexAccount
account = MyPlexAccount('userid', 'password')  #plex account userid and password
plex = account.resource('admin_user_id').connect() #add admin_user_id
plex_movies=[]
movies = plex.library.section('Movies')
for video in movies.search():
    plex_movies.append(video.title)

import sys
import re
# selenium 4
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from time import sleep
import background
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys

options = Options()
options.headless = True
driver = webdriver.Firefox(options=options,service=Service(GeckoDriverManager().install()))
#driver.get('https://7movierulz.at/telugu-movie/')
driver.get('https://7movierulz.ag/telugu-movie/')   #downloads latest movies from this website (telugu movies), if you want other language then change movierulz website which has your preferred language
movierulz=[]
for i in range(1,10000):
    try:
        y=(driver.find_element_by_xpath(f"/html/body/div/div[5]/div/article/div[2]/div/ul/li[{i}]/div/p/b").text)
        movierulz.append(y)
    except:
        break
movies_movierulz=[]    
for i in movierulz:
    movies_movierulz.append(i.split("(")[0])

movierulz_without_spaces=[]
for i in movies_movierulz:
    movierulz_without_spaces.append(re.sub(" ",'',i).lower())

plex_without_spaces=[]
for i in plex_movies:
    plex_without_spaces.append(re.sub(" ",'',i).lower())


should_not=['tamil']
should=['hd']
to_download_names=[]
to_download_index=[]
for i in range(len(movierulz_without_spaces)):
    if movierulz_without_spaces[i] not in plex_without_spaces:
        #print(movierulz_without_spaces[i])
        for b in should_not:
            if b in movierulz[i].lower():
                continue    
            if "english" in movierulz[i].lower():
                continue
            if "hd" in movierulz[i].lower():
                #print(movierulz[i])
                to_download_names.append(movierulz[i])
                to_download_index.append(i)

#to_download_str="\n".join(to_download_names)
already_downloaded=open("downloaded_movies.txt",'r').read().split('\n')
to_download_index
to_download=dict(list(zip(to_download_names,to_download_index)))
for i in to_download_names:
    if i in already_downloaded:
        del to_download[i]


to_download.keys()

magnetlinks=[]

for i in to_download.values():
    driver.get('https://7movierulz.at/telugu-movie/')
    driver.find_element_by_xpath(f"/html/body/div/div[5]/div/article/div[2]/div/ul/li[{i+1}]/div/div/a/img").click()

    for i in range(1,10000):
        try:
            r=driver.find_element_by_xpath(f'/html/body/div/div[5]/div/article/div[2]/p[5]/a[{i}]').text.split("gb")[0].split(' ')
            y=i
        except:
            break
        for i in r:
            try:
                gb=(float(i))
            except:
                pass
        if gb<4:
            magnetlinks.append(driver.find_element_by_xpath(f'/html/body/div/div[5]/div/article/div[2]/p[5]/a[{y}]').get_attribute("href"))        
            break
from time import sleep
try:
    if len(magnetlinks)==0:
        driver.quit()
        sleep(1)
        sys.exit()
        
except:
    driver.quit()
    sleep(1)
    sys.exit()

print("Downloading :,",to_download.keys())

driver.get("http://localhost:8000")    # address in which your qbittorrent is hosted 
driver.find_element_by_xpath('//*[@id="username"]').send_keys("user_id")  #qbittorrent userid 
driver.find_element_by_xpath('//*[@id="password"]').send_keys('password')  #qbittorrent password
driver.find_element_by_xpath('//*[@id="login"]').click()


driver.find_element_by_xpath("/html/body/div[1]/div[1]/div[2]/a[1]/img").click()
driver.switch_to.frame(0)
for i in magnetlinks:
    driver.find_element_by_xpath('//*[@id="urls"]').send_keys(i)
    driver.find_element_by_xpath('//*[@id="urls"]').send_keys(Keys.ENTER)

driver.find_element_by_xpath('//*[@id="submitButton"]').click()

already_downloaded=open("downloaded_movies.txt",'r').read()
ww=already_downloaded+"\n"+'\n'.join(to_download.keys())
open("downloaded_movies.txt",'w').write(ww)
driver.quit()


