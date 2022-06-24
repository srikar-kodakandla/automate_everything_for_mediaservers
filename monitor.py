import sys
import time
import logging
from watchdog.observers import Observer 
from watchdog.events import LoggingEventHandler 
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
root='/home/ubuntu/Googledrive/videos' ###################### directory in which videos are present 
import subprocess
import os
from plexconvert import *
from time import sleep
a=[os.path.join(path, name) for path, subdirs, files in os.walk(root) for name in files]
if len(a)==0:
    a=root
import re
#This step makes PLEX to recognize the movie names correctly 
regex="www.+?- "
for i in a:     #renaming files (it removes website names from the file name )
    if len(re.findall(regex,i.lower()))>0:
        index=re.search(regex,i.lower()).span()
        print(re.search(regex,i.lower()))
        uu=i[:index[0]]+i[index[1]:]
        print(uu)
        os.system(f'mv "{i}" "{uu}"')
print("Done renaming files...")

def rename_file(i):
        index=re.search(regex,i.lower()).span()
        print(re.search(regex,i.lower()))
        uu=i[:index[0]]+i[index[1]:]
        print(uu)
        os.system(f'mv "{i}" "{uu}"')
        scan_all_library()
        #optimize_video()


class MyHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        #scan(s=False)
        #print('on any event')
        #rint(event.event_type, event.src_path)
        #scan()
        #sleep(20)
        pass
    def on_created(self, event):
        print('created')
        print("on_created", event.src_path)
        if "/home/ubuntu/Googledrive/videos/downloaded videos/Plex Versions/" in event.src_path:
            print('skip checking as it is converting video in plex')
            return
        try:
            #sleep(60*10)
            rename_file(event.src_path)
            #os.system('bash /home/ubuntu/jellyfin_convert.sh')
            scan_all_library()
            try:
                optimize_video()
            except Exception as error:
                print(error)
            scan_all_library()
            try:
                optimize_video()
            except Exception as error:
                print(error)
        except Exception as error:
            print(error)
    def on_deleted(self, event):
        #print('deleted')
        #scan(s=False)
        #print("on_deleted", event.src_path)
        pass
    def on_modified(self, event):
        #print('modified')
        #scan(s=False)
        #print("on_modified", event.src_path)
        pass
    def on_moved(self, event):
        #scan(s=False)
        #print('moved')
        #print("on_moved", event.src_path)
        pass
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s')
    #path = sys.argv[1] if len(sys.argv) > 1 else '.'
    path='/home/ubuntu/Googledrive/videos/'
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)  #Scheduling monitoring of a path with the observer instance and event handler. There is 'recursive=True' because only with it enabled, watchdog.observers.Observer can monitor sub-directories
    observer.start()  #for starting the observer thread
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
