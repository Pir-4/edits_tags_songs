__author__ = 'valentin'
#you need to install eyeD3: pip install eyeD3#
import os
import eyed3
import json

#path = '/my_files/github/edits_tags_songs/music/Dead By April - Last Goodbye (New Album: "Incomparable" 2011).mp3'
#pathFile = '/my_files/github/edits_tags_songs/music/info.json'

def get_info_song(pathSong):
    info = {}
    trackInfo = eyed3.load(pathSong)
    info.update({"artist":str(trackInfo.tag.artist)})
    info.update({"title":str(trackInfo.tag.title)})
    info.update({"album":str(trackInfo.tag.album)})
    info.update({"album_artist":str(trackInfo.tag.album_artist)})
    info.update({"artist_url":str(trackInfo.tag.artist_url)})
    return info

def set_info_song(pathSong,info):
    trackInfo = eyed3.load(pathSong)

    trackInfo.tag.artist = info.get("artist")
    trackInfo.tag.title = info.get("title")
    trackInfo.tag.album = info.get("album")
    trackInfo.tag.album_artist = info.get("album_artist")
    trackInfo.tag.artist_url = info.get("artist_url")
    trackInfo.tag.save()

def write_file(pathDirInFile,info):
    with open(pathDirInFile,'w') as outfile:
        json.dump(info,outfile)

def read_file(pathDirInFile):
    with open(pathDirInFile,'r') as outfile:
        info =  json.load(outfile)
    return info

def getAllPathSongs(startDir):
    paths= []
    for d, dir,files in os.walk(startDir):
        for file in files:
            path = os.path.join(d,file)
            if path.endswith("mp3"):paths.append(path)
    return paths

#info =  get_info_song(path)
#print info
#write_file(pathFile,info)
#info = read_file(pathFile)
#print info
#set_info_song(path,info)

startDir = "/my_files/github/edits_tags_songs/music/"
paths = getAllPathSongs(startDir)