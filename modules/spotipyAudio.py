import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import re,time

class spotipyAudio:
    def __init__(self):
        self.myID = #client ID
        mySecret =  #client secret
        self.keys=['C','C#/Db','D','D#/Eb','E','F','F#/Gb','G','G#/Ab','A','A#/Bb','B']
        ccm = SpotifyClientCredentials(client_id = self.myID, client_secret = mySecret)
        self.spotipyAudio = spotipy.Spotify(client_credentials_manager = ccm)
    
    def urlToID(self,URL):
        trackID=[]
        for url in URL:
            trackID.append(re.sub(r'^(.*/)(.*)?(\?.*)$', r"\2", url))
        return trackID

    def trackAnalysis(self, trackURL="https://open.spotify.com/intl-ja/track/1vvpFd7pRLCl5aVIjB2IT6?si=f40e201a7222472f"):
        #["https://open.spotify.com/intl-ja/track/1vvpFd7pRLCl5aVIjB2IT6?si=f40e201a7222472f"]
        trackID=self.urlToID(trackURL)
        audioFeatures = self.spotipyAudio.audio_features(trackID)
        trackInfo=self.spotipyAudio.tracks(trackID)['tracks']
        #print(trackFeatures)
        #print(trackInfo)
        trackFeatures=[]
        for feature,info in zip(audioFeatures,trackInfo):
            trackFeatures.append({'Title':info['name'],'Artists':info['artists'][0]['name'],'BPM':feature['tempo'],'key':self.keys[feature['key']]})
        return trackFeatures
    
    def playlistAnalysis(self,playlistURL="https://open.spotify.com/playlist/37i9dQZF1DZ06evO2wNuKI?si=VijIz_y9RkCV5fVI-R18Qw"):
        playlistID=self.urlToID(playlistURL)[0]
        playlist=self.spotipyAudio.user_playlist(self.myID,playlistID)
        playlistName=playlist['name']
        trackURI=[]
        #print(len(playlist['tracks']['items']))

        for track in playlist['tracks']['items']:
            trackURI.append(track['track']['uri'])

        while(playlist['tracks']['next']):
            playlist['tracks']=self.spotipyAudio.next(playlist['tracks'])
            for track in playlist['tracks']['items']:
                trackURI.append(track['track']['uri'])
        trackFeatures=[]
        trackInfo=[]
        i=0
        step=50
        while(i+step<len(trackURI)-1):
            trackFeatures += self.spotipyAudio.audio_features(trackURI[i:i+step])
            trackInfo+=self.spotipyAudio.tracks(trackURI[i:i+step])['tracks']
            i+=step
        trackFeatures += self.spotipyAudio.audio_features(trackURI[i:len(trackURI)])
        trackInfo+=self.spotipyAudio.tracks(trackURI[i:len(trackURI)])['tracks']
        #print(trackInfo,trackFeatures)

        audioFeatures = []
        keysSum={}
        for key in self.keys:keysSum[key]=0
        for result,info in zip(trackFeatures,trackInfo):
            audioFeatures.append({'Title':info['name'],'Artists':','.join([artist['name'] for artist in info['artists']]),'BPM':result['tempo'],'key':self.keys[result['key']]})
            keysSum[self.keys[result['key']]]+=1
        playlistFeatures={
            "playlistName":playlistName,
            "track":audioFeatures
        }

        return playlistFeatures,keysSum
    
    def playlistFeaturesMakeCSV(self,playlistFeatures):
        df=pd.DataFrame(playlistFeatures["track"])
        df.index+=1
        df.to_csv(f'{playlistFeatures["playlistName"]}.csv')
        return 