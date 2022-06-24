# automate_everything_for_mediaservers
why to pay premiums for prime, netflix , hotstar , etc... when we have the below program which automatically downloads new movies , preprocess it , converts it and adds to your own media server

The above program downloads newly released movies from movierulz website (pirated movies website) then it preprocess the title , converts the video so that the video can play in any device with out transcoding and adds it to PLEX (media server). 

you can schedule the program to run every day by using crontab in ubuntu  , so that you don't need to run program manually every time when new movie gets released. 

add below two lines in "crontab -e"
>00 * * * * screen -dmS movierulz_download ipython3 addnewmovies.py  # This program is for downloading new movies from movierulz website.

>@reboot screen -dmS monitor_directory ipython3 monitor.py #This program monitors the given library , if a new movie is added then it preprocess movie names, converts and adds it to plex library 

With the above program , when ever a new movie is released in movierulz , it automatically downloads , converts  and adds to plex media server.after running that program in cronjob , just sitback and turn on tv , open plex app , enjoy new movies . 
