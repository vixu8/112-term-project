from pydub import AudioSegment
from pydub.playback import play

# for playing mp3 file
song = AudioSegment.from_wav("wav_phone_linging.wav")
print('playing sound using  pydub')
play(song)