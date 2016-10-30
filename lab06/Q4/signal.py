# Created by Drumil Mahajan
# October 2016, New York University

from struct import pack
import pyaudio
import wave
import struct
import math
from math import sin, cos, pi
from matplotlib import pyplot as plt
import pylab
import numpy as np

Fs = 8000
maxAmp = 2**15-1.0 			# maximum amplitude


# Setting up the figure/plot and turning of interative mode. 
'''
plt.ion()           # Turn on interactive mode so plot gets updated
fig = plt.figure(1)
line_in, = plt.plot(input_data)
line_out, = plt.plot(output_data)
plt.ylim(-32000, 32000)
plt.xlim(0, BLOCKSIZE)
plt.xlabel('Time (n)')
plt.show()
'''

# Creating line space , N points from -999 to 1000 to save the spectrum values
n = np.linspace(0, 1000-1, 1000)

# Creating an array to update plot values 
plot_arr = [ 0 for i in range(0,1000)]


# array to save output values 
output_vals = []
# Setting up the figure/plot and turning of interative mode. 
plt.ion() # Turn on interactive mode so plot gets updated

fig = plt.figure(1)

input_plot = plt.subplot(2, 1, 1)
input_plot.set_title('Produced signal')
line_in, = plt.plot(plot_arr)
plt.ylim(-32000/2, 32000/2)
plt.xlim(0, 100)
plt.show()

input_plot = plt.subplot(2, 1, 2)
input_plot.set_title('fft of the signal')
line_out, = plt.plot(n)
plt.ylim(-164000, 164000)
plt.xlim(-50, 1050)
plt.show()


# Open the audio output stream
p = pyaudio.PyAudio()
stream = p.open(format = p.get_format_from_width(2),
                channels = 1,
                rate = Fs,
                input = False,
                output = True)


for n in range(0, 5*Fs):	# 5 second duration
    outputvalue =  maxAmp * sin(Fs*2*pi*((30*(n**2))+(200*n)))
    output_string = pack('h' , outputvalue)
    #output_string = pack('h' , maxAmp * sin(n*2*pi*200/Fs) )
    stream.write(output_string) 
    output_vals.append(outputvalue)
    if n%1000 == 999: 
        line_in.set_ydata(output_vals)
        out_fft = np.fft.fft(output_vals)
        line_out.set_ydata(out_fft.real)
        plt.pause(0.001)
        output_vals = []

	
stream.stop_stream()
stream.close()
p.terminate()
