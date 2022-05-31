from Google import Create_Service
from googleapiclient.http import MediaFileUpload
from pytube import YouTube


def upload(time, title, video_path):
    service = Create_Service('secret.json', 'youtube', 'v3', 'https://www.googleapis.com/auth/youtube.upload')

    request_body = {
        'snippet': {
            'categoryI': 19,
            'title': title,
            'description': '',
            'tags': []
        },
        'status': {
            'privacyStatus': 'private',
            'publishAt': time,
            'selfDeclaredMadeForKids': False,
        },
        'notifySubscribers': False
    }
    mf = MediaFileUpload(video_path)

    re = service.videos().insert(
        part='snippet,status',
        body=request_body,
        media_body=mf
    ).execute()


def download(link):
    video = YouTube(link)
    yt = video.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
    yt.download(output_path="download")

