__author__ = 'valentin'
#you need to install eyeD3: pip install eyeD3#
import os
import eyed3
import json
import shutil
import sys
import argparse

JSONNAME = "info.json"
RENAMEDIR = "RenameDir"

#************ work tags ****************
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
    artist = ""
    songname = ""
    try:
        trackInfo.tag.artist = info.get("artist")
        artist = info.get("artist")
        trackInfo.tag.title = info.get("title")
        songname = info.get("title")
        trackInfo.tag.album = info.get("album")
        trackInfo.tag.album_artist = info.get("album_artist")
        trackInfo.tag.artist_url = info.get("artist_url")
    except:
        print "Error write tag: " + pathSong

    trackInfo.tag.save()

    return artist, songname


def write_file(pathInfo,info):
    with open(pathInfo,'w') as outfile:
        json.dump(info,outfile)

def read_file(pathinfo):
    with open(pathinfo,'r') as outfile:
        info =  json.load(outfile)
    return info
#******************************************

#************ read songs ****************
def getAllPathSongs(startDir):
    paths= []
    files = os.listdir(startDir)
    for file in files:
        if file.endswith(".mp3"):
            path = os.path.join(startDir,file)
            paths.append(path)
    return paths

def copyFileRenameDir(renameDir,filePaths):
    count = 0
    newPatpFiles = []

    if  os.path.exists(renameDir):
        shutil.rmtree(renameDir)
    os.mkdir(renameDir)

    for path in filePaths:
        newpath = os.path.join(renameDir,str(count))
        os.mkdir(newpath)
        shutil.copy(path,newpath)
        count += 1
        newPatpFiles.append(newpath)
    return newPatpFiles

def get_all_info(paths):
    for path in paths:
     for dir,d,files in os.walk(path):
         for file in files:
            song = os.path.join(dir,file)
            info = get_info_song(song)
            infoPath = os.path.join(dir,JSONNAME)
            write_file(infoPath,info)
            print song

def get_info(startDir):
    paths = getAllPathSongs(startDir)
    renameDir = os.path.join(startDir,RENAMEDIR)
    paths = copyFileRenameDir(renameDir,paths)
    get_all_info(paths)
#************************************************

#************ write songs ****************
def set_all_info(dirs):
    pathIfo = ""
    pathSong = ""
    newSongs = {}
    for dir in dirs:
        songName = ""
        for file in os.listdir(dir):
            if JSONNAME in file:
                pathIfo = os.path.join(dir,file)
            else:
                pathSong = os.path.join(dir,file)
                songName = file

        info = read_file(pathIfo)
        artist,songname = set_info_song(pathSong,info)
        if not "None" in artist and not "None" in songname:
            songName = artist + " - " + songname
        newSongs.update({songName:pathSong})
    return newSongs

def set_info(startDir):
    renameDir = os.path.join(startDir,RENAMEDIR)
    if not os.path.exists(renameDir):
        print "Not found " + renameDir
        os._exit(1)

    dirs = []
    for dir in os.listdir(renameDir):
        dirs.append(os.path.join(renameDir,dir))
    newSongs = set_all_info(dirs)
    for key in newSongs:
        shutil.move(newSongs.get(key),os.path.join(renameDir,key))


def createParser():
        parser = argparse.ArgumentParser()
        parser.add_argument ('-startdir', nargs='?',default=os.getcwd())
        parser.add_argument ('-mode', nargs='?',default="g")
        return parser

if __name__== '__main__':
    parser = createParser()
    namespace = parser.parse_args(sys.argv[1:])
    startDir = namespace.startdir
    if not os.path.exists(startDir):
        print "Not found " + startDir
        os._exit(1)

    if namespace.mode == "g":
        get_info(startDir)
    elif namespace.mode == "s":
        set_info(startDir)
    else:
        print "Key '-mode' is empty entry 'g' or 's'"



