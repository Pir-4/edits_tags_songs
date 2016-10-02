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
        info.update({"artist":str("None")})
    try:
        info.update({"title":str(trackInfo.tag.title)})
    except:
         info.update({"title":str("None")})
    try:
        info.update({"album":str(trackInfo.tag.album)})
    except:
        info.update({"album":str("None")})
    try:
        info.update({"album_artist":str(trackInfo.tag.album_artist)})
    except:
        info.update({"album_artist":str("None")})
    try:
        info.update({"artist_url":str(trackInfo.tag.artist_url)})
    except:
        info.update({"artist_url":str("None")})
    return info

def set_info_song(pathSong,info):
    trackInfo = eyed3.load(pathSong)
    try:
        trackInfo.tag.artist = info.get("artist")
        trackInfo.tag.title = info.get("title")
        trackInfo.tag.album = info.get("album")
        trackInfo.tag.album_artist = info.get("album_artist")
        trackInfo.tag.artist_url = info.get("artist_url")
    except:
        print "Error write tag: " + pathSong

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
            infoPath = os.path.join(dir,JSONNAME)
            write_file(infoPath,info)
            print song

def set_all_info(dirs):
    pathIfo = ""
    pathSong = ""
    for dir in dirs:
        for file in os.listdir(dir):
            if JSONNAME in file:
                pathIfo = os.path.join(dir,file)
            else:
                pathSong = os.path.join(dir,file)
        info = read_file(pathIfo)
        set_info_song(pathSong,info)


def get_info(startDir):
    paths = getAllPathSongs(startDir)
    renameDir = os.path.join(startDir,RENAMEDIR)
    paths = copyFileRenameDir(renameDir,paths)
    get_all_info(paths)

def set_info(startDir):
    renameDir = os.path.join(startDir,RENAMEDIR)
    if not os.path.exists(renameDir):
        print "Not found " + renameDir
        os._exit(1)

    dirs = []
    for dir in os.listdir(renameDir):
        dirs.append(os.path.join(renameDir,dir))
    set_all_info(dirs)


JSONNAME = "info.json"
RENAMEDIR = "RenameDir"
startDir = "/my_files/github/edits_tags_songs/music/"

get_info(startDir)
#set_info(startDir)




