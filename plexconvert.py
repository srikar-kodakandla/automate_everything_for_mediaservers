from plexapi.myplex import MyPlexAccount
account = MyPlexAccount('username', 'password') ## add username and password of your plex account
plex = account.resource('username').connect()  ## add username of your plex account

def scan_all_library():
    from plexapi.myplex import MyPlexAccount
    account = MyPlexAccount('username', 'password')  ## add username and password of your plex account
    plex = account.resource('username').connect()    ## add username of your plex account
    plex.library.update()
def optimize_video():
    print('')
    print('PLEX: optimizing all videos in Movies')
    from plexapi.myplex import MyPlexAccount
    account = MyPlexAccount('username', 'password')  ## add username and password of your plex account
    plex = account.resource('username').connect()   ## add username of your plex account
    plex.library.update()
    movies = plex.library.section('Movies')
    for video in movies.search():
        try:
            print(video.title)
            video.optimize(targetTagID='TV')
        except Exception as error:
            print(error)

if __name__=="__main__":
    optimize_video()

