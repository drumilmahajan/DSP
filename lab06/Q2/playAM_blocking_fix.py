# playAM_blocking_fix.py
# Play a mono wave file with amplitude modulation. 
# This implementation reads and plays a block at a time (blocking)
# and corrects for block-to-block angle mismatch.
# Assignment: modify this file so it works for both mono and stereo wave files
#  (where does this file have an error when wave file is stereo and why? )

# f0 = 0      # Normal audio
f0 = 400    # 'Duck' audio

BLOCKSIZE = 1024    # Number of frames per block

import pyaudio
import struct
import wave
import math
import matplotlib
from matplotlib import pyplot as plt
matplotlib.use('TkAgg')
from matplotlib import animation as ani
import pylab
from myfunctions import clip16
import time
import numpy as np

# Open wave file (mono)
wave_file_name = 'author.wav'
# wave_file_name = 'sin01_mono.wav'
# wave_file_name = 'sin01_stereo.wav'
wf = wave.open( wave_file_name, 'rb')
RATE = wf.getframerate()
WIDTH = wf.getsampwidth()
LEN = wf.getnframes() 
CHANNELS = wf.getnchannels() 

print 'The sampling rate is {0:d} samples per second'.format(RATE)
print 'Each sample is {0:d} bytes'.format(WIDTH)
print 'The signal is {0:d} samples long'.format(LEN)
print 'The signal has {0:d} channel(s)'.format(CHANNELS)



# Open audio stream
p = pyaudio.PyAudio()
stream = p.open(format = p.get_format_from_width(WIDTH),
                channels = 1,
                rate = RATE,
                input = False,
                output = True)

# Create block (initialize to zero)
output_block = [0 for n in range(0, BLOCKSIZE)]

output_data = [0 for n in range(0, BLOCKSIZE)]
input_data  = [0 for n in range(0, BLOCKSIZE)]

# input blocks 
input_int = [0 for n in range(0, BLOCKSIZE)]


# Number of blocks in wave file
num_blocks = int(math.floor(LEN/BLOCKSIZE))

# Initialize angle
theta = 0.0

# Block-to-block angle increment
theta_del = (float(BLOCKSIZE*f0)/RATE - math.floor(BLOCKSIZE*f0/RATE)) * 2.0 * math.pi
#theta_del = 100
# Turning on Interactive mode so plot gets updated

plt.ion()
line_out, = plt.plot(output_block)
#fig1 = plt.plot(output_block)[0]

line_in, = plt.plot(input_int)
plt.ylim(-32000,32000)
plt.xlim(0, BLOCKSIZE)
plt.xlabel("Time (n)")
plt.show()

fig = plt.figure(1)

input_plot = plt.subplot(2, 1, 1)
input_plot.set_title('INPUT FFT')
line_in, = plt.plot(input_data)
plt.ylim(-64000, 64000)
plt.xlim(0, BLOCKSIZE)
plt.show()

output_plot = plt.subplot(2, 1, 2)
output_plot.set_title('OUTPUT FFT')
line_out, = plt.plot(output_data)
plt.ylim(-64000, 64000)
plt.xlim(0, BLOCKSIZE)
plt.show()

print('* Playing...')

# Go through wave file 
for i in range(0, num_blocks):

    # Get block of samples from wave file
    input_string = wf.readframes(BLOCKSIZE)     # BLOCKSIZE = number of frames read
    # Convert binary string to tuple of numbers    
    input_tuple = struct.unpack('h' * BLOCKSIZE, input_string)
            # (h: two bytes per sample (WIDTH = 2))

    # Go through block
    for n in range(0, BLOCKSIZE):
        # Amplitude modulation  (f0 Hz cosine)
        output_block[n] = input_tuple[n] * math.cos(2*math.pi*n*f0/RATE + theta)
        input_int[n] = input_tuple[n]
        #fig1.set_data(output_block)
        output_data[n] = output_block[n]
        
        # output_block[n] = input_tuple[n] * 1.0  # for no processing
    
    # Set angle for next block
    theta = theta + theta_del

    # Taking fft of input and the output data
    in_fft = np.fft.fft(list(input_tuple))
    out_fft = np.fft.fft(output_data)

    # Plotting the graph
    line_in.set_ydata(in_fft.real)
    line_out.set_ydata(out_fft.real)
    plt.pause(0.001)

    # Convert values to binary string
    output_string = struct.pack('h' * BLOCKSIZE, *output_block)

    # Write binary string to audio output stream
    stream.write(output_string)

    
    

print('* Done')

stream.stop_stream()
stream.close()
p.terminate()

# Original file by Gerald Schuller, October 2013
