import re
#import ffmpeg
from subprocess import run
from pytube import Playlist,YouTube
play_list = Playlist("https://www.youtube.com/watch?v=P1bAPZg5uaE&list=PL_z_8CaSLPWdeOezg68SKkeLN4-T_jNHd")
download_path=r"E:\Downloaded"
print(YouTube(play_list[4]).streams.filter())

# val=1
for url in play_list:
    yt=YouTube(url)
    #file_title=re.sub('[\s]','_',yt.title)
    file_title=re.sub('[\|]','-',yt.title)
    file_title=re.sub('[\?]','@',file_title)
    #stream=yt.streams.get_highest_resolution()
    try:
        stream=yt.streams.get_by_itag(22)    #720p
        stream.download(download_path,file_title+".mp4") #save at location
        print("Downloaded "+file_title+"  Successfully ")
    except:
        #as 480p sometimes give no audio
        print("\t downloading in 480p"+file_title)
        download_path_temp=str(download_path+r"\temp")
        try:
            stream_vid=yt.streams.get_by_itag(244) #480p without audio
            stream_vid.download(download_path_temp,file_title+".mp4") #save at locationn
        except:
            stream_vid=yt.streams.get_by_itag(135) #480p without audio and 135 tag because sometimes 244 is unavailable
            stream_vid.download(download_path_temp,file_title+".mp4") #save at location


        ##downloading audio stream
        stream_aud=yt.streams.filter(only_audio=True).first()
        stream_aud.download(download_path_temp,file_title+".mp3") #save at location
        
        temp_full_video_path=str(download_path_temp+"\\"+file_title+".mp4")
        temp_full_audio_path=str(download_path_temp+"\\"+file_title+".mp3")
        output_path=str(download_path+"\\"+file_title+".mp4")
        
        
        print(temp_full_video_path)
        print(temp_full_audio_path)
        
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
    #else:
    #    print("Failed to Download the stream "+yt.title)
    #val+=1
    