import os
import json
import random
from moviepy.editor import TextClip, concatenate_videoclips, CompositeVideoClip
from moviepy.video.io.VideoFileClip import VideoFileClip
import moviepy.config as cfg
from moviepy.editor import VideoFileClip, CompositeVideoClip
from moviepy.video.VideoClip import ColorClip
from moviepy.video.fx.all import margin
gif = VideoFileClip('clock.gif')
from moviepy.editor import AudioFileClip

cfg.change_settings({"IMAGEMAGICK_BINARY": r"C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe"})

with open('./data/main.json', 'r') as f:
    data = json.load(f)

media_files = [os.path.join("./media", f) for f in os.listdir("./media") if f.endswith(".mp4")]
font_path = "RUBIK-BOLD.TTF"

# Place this line where you want to set the audio track
background_audio = AudioFileClip('audio/backgroundaudio.mp3')

for item in data:
    clips = []
   
    for key, value in item.items():
        color = 'white'
        strokeColor = 'black'
        strokeWidth = 4
        fontSize = 75
        if key == "ninche":
            duration = 3
            value = 'Ready to challenge your ' + value + ' knowledge? Guess the answer to...'
            color = '#FFC000'
           
        elif key == "question":
            duration = 6
            gif = gif.set_duration(duration)
            fontSize = 80
        elif key == "answer":
            duration = 4
            color = '#fff'
            strokeColor = 'black'
            fontSize = 80
            value = value
            strokeWidth = 4
        
        words = value.split()
        line_broken_text = '\n'.join([' '.join(words[i:i+2]) for i in range(0, len(words), 2)])
        text_clip = TextClip(line_broken_text, fontsize=fontSize, color=color, font=font_path, stroke_color=strokeColor, stroke_width=strokeWidth).set_duration(duration)


        if key == "question":
            # Create a composite clip for the question with the gif and the text
            question_text_clip = CompositeVideoClip([text_clip.set_position('center')], size=(1080,1920)) # Assuming a video size of 1920x1080
            gif_clip = CompositeVideoClip([gif.set_position(("center", "top"))], size=(1080,1920))
            question_clip = CompositeVideoClip([question_text_clip, gif_clip])
            clips.append(question_clip)
        else:
            clips.append(text_clip)
    
    # Create final TextClip here
    ending_text = "Follow to test your knowledge daily!"
    words = ending_text.split()
    line_broken_text = '\n'.join([' '.join(words[i:i+2]) for i in range(0, len(words), 2)])
    ending_text_color = '#097969'
    ending_text_duration = 3 
    ending_text_clip = TextClip(line_broken_text, fontsize=75, color=ending_text_color, 
                                font=font_path, stroke_color='white', stroke_width=2).set_duration(ending_text_duration)
    
    # Append ending_text_clip to the clips list
    clips.append(ending_text_clip)

    if not media_files:
       
        media_files = [os.path.join("./media", f) for f in os.listdir("./media") if f.endswith(".mp4")]
    bg_file = random.choice(media_files)
    media_files.remove(bg_file) 
    bg_video = VideoFileClip(bg_file)

    total_clips_duration = sum([clip.duration for clip in clips])

    bg_video = bg_video.subclip(0, total_clips_duration)

    final_video = concatenate_videoclips(clips).set_duration(total_clips_duration)
    
    final_clip = CompositeVideoClip([bg_video, final_video.set_position('center')])
    final_clip = final_clip.set_fps(bg_video.fps) 
    final_clip = final_clip.fx(margin, 15, color=(0,0,0))  # Adds a 5px black margin

     # Cut the audio file down to the video's length and set it as the video's audio
    final_audio = background_audio.subclip(0, final_clip.duration)
    final_clip = final_clip.set_audio(final_audio)

 
    output_folder = "output"

    output_file = os.path.join(output_folder, f"{item['question'].replace(' ', '_').replace('?', '')}.mp4")
    final_clip.write_videofile(output_file)
