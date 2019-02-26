from pytube import YouTube
import os
import glob


imagesPerRace = 500


def downloadYouTube(videoID, path):
    if not os.path.exists("videos/" + path + ".mp4"):
        print("Downloading video for " + path)
        yt = YouTube("https://www.youtube.com/watch?v=" + videoID)
        yt = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
        if not os.path.exists("videos/"):
            os.makedirs("videos/")
        yt.download(output_path="videos/", filename=path)
        print("Video downloaded " + path)
    print("The file videos/" + path + ".mp4 already exists")


def getImagesFromVideo(path):
    imagePaths = glob.glob('training/' + path + '/*.jpg')
    if not (len(imagePaths) == imagesPerRace):
        print("Getting images for " + path)
        if not os.path.exists("training/" + path):
            os.makedirs("training/" + path)
        os.system("ffmpeg -i videos/" + path + ".mp4 -r 1/10 -ss 00:10:00 training/" + path + "/$race%04d.jpg")
        print("Images saved " + path)


def cleanUpFiles(path):
    print("Cleaning up files for " + path)
    imagePaths = glob.glob('training/' + path + '/*.jpg')
    imagePaths.sort(key=os.path.getmtime)
    print(len(imagePaths))
    for i,imagePath in enumerate(imagePaths):
        if(i >= imagesPerRace):
            os.remove(imagePath)
    imagePaths = glob.glob('training/' + path + '/*.jpg')
    imagePaths.sort(key=os.path.getmtime)
    print(len(imagePaths))


def runIt(videoID, path):
    downloadYouTube(videoID, path)
    getImagesFromVideo(path)
    cleanUpFiles(path)




videoIDs = ['2IgUwJlMMPo', '02Go3cIX_ok', 'yDammSvXLKI', 'GjMQgY_qhg4', 'Etcm745fW0Q', 'Tzk3BuiFiyg']
tracks = ['daytona', 'sebring', 'long-beach', 'mid-ohio', 'belle-isle', 'watkins-glen']

testingVideoIDs = ['ndAho_l2PZ8']
testingTracks = ['test-daytona']

# downloadYouTube(testingVideoIDs[0], testingTracks[0])
# getImagesFromVideo(testingTracks[0])

# for i, value in enumerate(videoIDs):
#     unIt(videoIDs[i], tracks[i])  #training


# runIt(videoIDs[0], tracks[0])

# cleanUpFiles('long-beach')
# downloadYouTube('https://www.youtube.com/watch?v=' + , 'videos/')