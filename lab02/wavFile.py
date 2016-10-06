from struct import pack
from math import sin, pi
import wave

wf = wave.open('cat01.wav' , 'rb') # read only binary 

# To read properties of the wav file

num_channel = wf.getnchannels() # get no of channels
fs = wf.getframerate()        # sampling rate. There is a difference between sampling and frame rate
length_signal = wf.getnframes() # signal length
width = wf.getsampwidth()     # byters per frame


print num_channel
print fs
print length_signal
print width