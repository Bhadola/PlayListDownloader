#import ffmpeg  too damn slow
import re
import os
import shutil           #to delete tempath
from subprocess import run
from pytube import Playlist,YouTube
from pytube.cli import on_progress
play_list = Playlist("https://www.youtube.com/watch?v=HujTzAI2vgk&list=PLLYz8uHU480j37APNXBdPz7YzAi4XlQUF")
download_path=r"E:\Downloaded"

# print(YouTube(play_list[11]).streams)          #prints stream data
# exit(1)
def convertencoding(oldstring):
    newstring=re.sub('[\s]','_',oldstring)
    newstring=re.sub('[\|]','-',newstring)
    newstring=re.sub('[/|]',',',newstring)
    newstring=re.sub('[\?]','@',newstring)
    return newstring

def createfolder(folder_path):              #might need to trim path also
    # print(folder_path)
    try:
        if(not os.path.exists(folder_path)):
            os.mkdir(folder_path)
    except:
        print("Some error occured")

newpath=download_path+"\\"+convertencoding(play_list.title)
createfolder(newpath)
tempath=newpath+"\\"+"temp"
createfolder(tempath)


val=1                                 ##uncomment val and append to file name in case numbering required

print("Downloading "+play_list.title)
for url in play_list:
    # yt=YouTube(url)
    yt=YouTube(url,on_progress_callback=on_progress)
    file_title=convertencoding(yt.title)        #converts to suitable encoding
    
    ####
    file_title=str(val)+" "+file_title
    val=val+1                       
    #####
    print("Downloading "+file_title)
    try:
        stream=yt.streams.get_by_itag(22)    #720p
        # print("Downloading "+file_title+" ("+str(stream.filesize//1048576)+") Mb")
        stream.download(newpath,file_title+".mp4") #save at location
    except:
        #as 480p sometimes give no audio
        try:
            stream_vid=yt.streams.get_by_itag(244) #480p without audio
            stream_vid.download(tempath,file_title+".mp4") #save at locationn
        except:
            stream_vid=yt.streams.get_by_itag(135) #480p without audio and 135 tag because sometimes 244 is unavailable
            stream_vid.download(tempath,file_title+".mp4") #save at location


        ##downloading audio stream
        stream_aud=yt.streams.filter(only_audio=True).first()
        stream_aud.download(tempath,file_title+".mp3") #save at location
        
        temp_full_video_path=str(tempath+"\\"+file_title+".mp4")
        temp_full_audio_path=str(tempath+"\\"+file_title+".mp3")
        output_path=str(newpath+"\\"+file_title+".mp4")
        
        
        
        run([
            "ffmpeg",
            "-i",
            f"{temp_full_video_path}",
            "-i",
            f"{temp_full_audio_path}",
            "-c",
            "copy",
            f"{output_path}"
        ])
        print("Downloaded "+file_title+"  Successfully ")
    # break
    print('\n_______________********DOWNLOADED********_______________\n')
if(os.path.exists(tempath)):
    shutil.rmtree(tempath)
    print("Removed temp folder successfully")
