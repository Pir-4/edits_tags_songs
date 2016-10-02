__author__ = 'valentin'
#you need to install eyeD3: pip install eyeD3#
import os
import eyed3
import json
import shutil

#path = '/my_files/github/edits_tags_songs/music/Dead By April - Last Goodbye (New Album: "Incomparable" 2011).mp3'
#pathFile = '/my_files/github/edits_tags_songs/music/info.json'


def get_info_song(pathSong):
    info = {}
    trackInfo = eyed3.load(pathSong)
    try:
        info.update({"artist":str(trackInfo.tag.artist)})
    except:
        info.update({"artist":str(" ")})
    try:
        info.update({"title":str(trackInfo.tag.title)})
    except:
         info.update({"title":str(" ")})
    try:
        info.update({"album":str(trackInfo.tag.album)})
    except:
        info.update({"album":str(" ")})
    try:
        info.update({"album_artist":str(trackInfo.tag.album_artist)})
    except:
        info.update({"album_artist":str(" ")})
    try:
        info.update({"artist_url":str(trackInfo.tag.artist_url)})
    except:
        info.update({"artist_url":str(" ")})
    return info

def set_info_song(pathSong,info):
    trackInfo = eyed3.load(pathSong)

    trackInfo.tag.artist = info.get("artist")
    trackInfo.tag.title = info.get("title")
    trackInfo.tag.album = info.get("album")
    trackInfo.tag.album_artist = info.get("album_artist")
    trackInfo.tag.artist_url = info.get("artist_url")
    trackInfo.tag.save()

def write_file(pathInfo,info):
    with open(pathInfo,'w') as outfile:
        json.dump(info,outfile)

def read_file(pathinfo):
    with open(pathinfo,'r') as outfile:
        info =  json.load(outfile)
    return info

def getAllPathSongs(startDir):
    paths= []
    files = os.listdir(startDir)
    for file in files:
        path = os.path.join(startDir,file)
        if path.endswith("mp3"):paths.append(path)
    return paths

def copyFileRenameDir(renameDir,filePaths):
    count = 0
    newFiles = []
    if  os.path.exists(renameDir):
        shutil.rmtree(renameDir)

    os.mkdir(renameDir)
    for path in filePaths:
        newpath = os.path.join(renameDir,str(count))
        os.mkdir(newpath)
        shutil.copy(path,newpath)
        count += 1
        newFiles.append(newpath)
    return newFiles

def get_all_info(paths):
    for path in paths:
     for dir,d,files in os.walk(path):
         for file in files:
            song = os.path.join(dir,file)
            info = get_info_song(song)
            infoPath = os.path.join(dir,"info.json")
            write_file(infoPath,info)
            print song

def get_info(startDir):
    renameDir = "RenameDir"
    paths = getAllPathSongs(startDir)
    renameDir = os.path.join(startDir,renameDir)
    paths = copyFileRenameDir(renameDir,paths)
    get_all_info(paths)

#info =  get_info_song(path)
#print info
#write_file(pathFile,info)
#info = read_file(pathFile)
#print info
#set_info_song(path,info)

startDir = "/my_files/github/edits_tags_songs/music/"

#get_info(startDir)

