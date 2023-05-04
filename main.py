import random
import PySimpleGUI as sg
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.fx.speedx import speedx
from moviepy.video.compositing.concatenate import concatenate_videoclips
from moviepy.audio.io.AudioFileClip import AudioFileClip

sg.theme("DefaultNoMoreNagging")

layout = [        [sg.Text("Selecione o arquivo de áudio:")],
    [sg.Input(), sg.FileBrowse(key="-AUDIO-")],
    [sg.Text("Selecione o arquivo de vídeo:")],
    [sg.Input(), sg.FileBrowse(key="-VIDEO-")],
    [sg.Text("Duração máxima do vídeo (em segundos):"), sg.InputText("", key="-MAX_DURATION-")],
    [sg.Text("Fator de aceleração:"), sg.InputText("1.0", key="-SPEED_FACTOR-")],
    [sg.Text("Selecione o caminho de destino para o vídeo gerado:")],
    [sg.Input(), sg.FileSaveAs(key="-OUTPUT-")],
    [sg.Submit(), sg.Cancel()]
]

window = sg.Window("Adicionar áudio a vídeo", layout)

while True:
    event, values = window.read()
    if event in (sg.WINDOW_CLOSED, "Cancel"):
        break
    elif event == "Submit":
        audio_path = values["-AUDIO-"]
        video_path = values["-VIDEO-"]
        max_duration = int(values["-MAX_DURATION-"])
        output_path = values["-OUTPUT-"]
        speed_factor = float(values["-SPEED_FACTOR-"])

        video = VideoFileClip(video_path)
        video = speedx(video, factor=speed_factor)

        audio = AudioFileClip(audio_path)
        max_duration = min(max_duration, audio.duration)

        video_parts = []
        while sum([part.duration for part in video_parts]) < max_duration:
            start = random.uniform(0, video.duration - 1)
            end = random.uniform(start + 1, video.duration)
            video_part = video.subclip(start, end)
            video_parts.append(video_part)

        final_video = concatenate_videoclips(video_parts)

        if final_video.duration > max_duration:
            final_video = final_video.subclip(0, max_duration)

        final_video = final_video.set_audio(audio)

        final_video.write_videofile(output_path)

        sg.popup("Vídeo gerado com sucesso!")


window.close()
