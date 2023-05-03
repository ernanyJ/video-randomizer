import random
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips
from moviepy.video import fx as vfx

audio = AudioFileClip("audio.mp3")
MAX_DURATION = audio.duration

video = VideoFileClip("keyrestoration.mp4").fx(vfx.speedx, 5)
video_parts = []

while sum([part.duration for part in video_parts]) < MAX_DURATION:
    start = random.uniform(0, video.duration - 1)
    end = min(start + random.uniform(1, 15), video.duration)
    video_part = video.subclip(start, end)
    video_parts.append(video_part)

final_video = concatenate_videoclips(video_parts)
final_video = final_video.set_audio(audio)

final_video.write_videofile("C:\\Users\\julio\\Documents\\out\\finalvideo.mp4")
