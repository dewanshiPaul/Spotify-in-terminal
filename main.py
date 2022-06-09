#importing libraries
import os
import webbrowser
import spotipy
import json
import sys
import spotipy.util as util
from json.decoder import JSONDecodeError
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

def spotify():
    #get username form terminal and scope. Scope is used in order to authorise the username and web browser to redirect to given url
    username = sys.argv[-1]
    scope = 'user-read-private user-read-playback-state user-modify-playback-state playlist-read-collaborative playlist-read-private'
    
    #clear cache ask permission from user before playing
    try:
        token = util.prompt_for_user_token(username,scope)
    except(AttributeError, JSONDecodeError):
        os.remove(f".cache-{username}")
        token = util.prompt_for_user_token(username,scope)
    
    #creation of spotify object
    spotifyObject = spotipy.Spotify(auth=token)
    
    #show devices from which song is played from
    device = spotifyObject.devices()
    print(json.dumps(device, sort_keys=True, indent=4))
    deviceID = device['devices'][0]['id']
    
    #get user details
    user = spotifyObject.current_user()
    displayUserName = user['display_name']
    
    list_of_songs = []
    list_of_URIs = []
    
    #menu
    while(True):
        print()
        print("||| Welcome to Spotify in terminal ||| " + displayUserName + " \^O^/" + "\n")
        print("0 - Search for an artist")
        print("1 - Search for track")
        print("2 - Print Queue")
        print("3 - Play")
        print("4 - Skip")
        print("5 - Previous track")
        print("6 - Pause")
        print("7 - See new releases (30 songs)")
        print("8 - Get current song status")
        print("9 - Exit")
        userChoice = input("Enter your choice: ")

        #search artists
        if(userChoice == "0"):
            print()
            query = input("Ok, what's their name?: ")
            print()
            #get search results
            results = spotifyObject.search(query,15,0,"artist")
            # Print artist details
            artist = results['artists']['items'][0]
            print(artist['name'])
            print(str(artist['followers']['total']) + " followers")
            print(artist['genres'])
            print()
            #webbrowser.open(artist['images'][0]['url'])
            artistID = artist['id']
            # Album details
            trackName = []
            trackArt = []
            trackURIs = []
            z = 0
            # Extract data from album
            albumResults = spotifyObject.artist_albums(artistID)
            albumResults = albumResults['items']
    
            for item in albumResults:
                print("ALBUM: " + item['name'])
                albumID = item['id']
                albumArt = item['images'][0]['url']
    
                # Extract track data
                trackResults = spotifyObject.album_tracks(albumID)
                trackResults = trackResults['items']
    
                for item in trackResults:
                    print(str(z) + ": " + item['name'])
                    trackName.append(item['name'])
                    trackArt.append(albumArt)
                    trackURIs.append(item['uri'])
                    z+=1
            # See album art
            while True:
                try:
                    songSelection = input("Enter song number to insert your track(to exit enter e): ")
                    if songSelection == "e":
                        break
                    list_of_songs.append(trackName[int(songSelection)])
                    list_of_URIs.append(trackURIs[int(songSelection)])
                except:
                    print("Enter number within index!!")


        # End program
        if(userChoice == "1"):
            query_track = input("Enter name of the song: ")
            result = spotifyObject.search(query_track,10,0,"track")
            nameSong = result['tracks']['items'][0]['name']
            artistName = result['tracks']['items'][0]['artists']
            uri = result['tracks']['items'][0]['uri']

            print("Artists:")
            for it in artistName:
                print(it['name'])
            list_of_songs.append(nameSong)   
            list_of_URIs.append(uri)
    
        if(userChoice == "2"):
            print("Tracks in queue:")
            print(list_of_songs)

        if(userChoice == "3"):
            if(len(list_of_URIs) != 0):
                spotifyObject.start_playback(deviceID, None, list_of_URIs)
            else:
                print("List is empty!!! Enter songs")

        if(userChoice == "4"):
            nextTrack = spotifyObject.next_track(device_id=None)
            print("Moved to next track")

        if(userChoice == "5"):
            prevTrack = spotifyObject.previous_track(device_id=None)
            print("Moved to previous track")
        
        if(userChoice == "6"):
            pause = spotifyObject.pause_playback(device_id=None)
            print("paused")

        if(userChoice == '7'):
            newRelease = spotifyObject.new_releases(country=None,limit=30,offset=0)

            for i in range(30):
                newReleaseSongNames = (newRelease['albums']['items'][i]['name'])
                newReleaseArtistName = (newRelease['albums']['items'][i]['artists'][0]['name'])
                print(i,newReleaseSongNames,'-',newReleaseArtistName,'\n')

        if(userChoice == '8'):
            track = spotifyObject.current_user_playing_track()
            artist = ''
            songName = ''
            try: 
                artist = track['item']['artists'][0]['name']
                songName = track['item']['name']
                currentUri = track['item']['uri']
            except Exception as e:
                print(e)
    
            if(artist != ""):
                print("Currently playing: " + artist + "-" + songName)

        if(userChoice == "9"):
            break