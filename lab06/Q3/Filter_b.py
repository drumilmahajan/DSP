# Reads an audio wav file
# Filter it using band pass filter
# PLays the filter and audio output in different channels
# Plots the real time output of the waveform.
# reads blocks of data and process it at once. 
# plots the left and right channel. 

# Modified by Drumil Mahajan
# Oct, 2016, New York University

import pyaudio
import wave
import struct
import math
from math import sin, cos, pi
from matplotlib import pyplot as plt
import pylab


def clip16( x ):    
    # Clipping for 16 bits
    if x > 32767:
        x = 32767
    elif x < -32768:
        x = -32768
    else:
        x = x        
    return int(x)


# Reading the wave file

wavfile = 'author.wav'
# wavfile = 'sin01_mono.wav'

print("Play the wave file %s." % wavfile)

# Open wave file (should be mono channel)
wf = wave.open( wavfile, 'rb' )

# Read the wave file properties
num_channels = wf.getnchannels()       	# Number of channels
RATE = wf.getframerate()                # Sampling rate (frames/second)
signal_length  = wf.getnframes()       	# Signal length
width = wf.getsampwidth()       		# Number of bytes per sample

print("The file has %d channel(s)."            % num_channels)
print("The frame rate is %d frames/second."    % RATE)
print("The file has %d frames."                % signal_length)
print("There are %d bytes per sample."         % width)


# Creating variables to read blocks

BLOCKSIZE = 4096 # Block size // user defined.
numBlocks = int(math.floor(signal_length/BLOCKSIZE)) # Total number of blocks in the input. 
output_block = [0 for n in range(0, 2 * BLOCKSIZE)] # output block, initialized to zero. size twice in BLOCKSIZE to store the original input and filtered output
output_data = [0 for n in range(0, BLOCKSIZE)]
input_data  = [0 for n in range(0, BLOCKSIZE)]
# Setting up the figure/plot and turning of interative mode. 

plt.ion()           # Turn on interactive mode so plot gets updated
fig = plt.figure(1)
line_in, = plt.plot(input_data)
line_out, = plt.plot(output_data)
plt.ylim(-32000, 32000)
plt.xlim(0, BLOCKSIZE)
plt.xlabel('Time (n)')
plt.show()

# Difference equation coefficients
b0 =  0.008442692929081
b2 = -0.016885385858161
b4 =  0.008442692929081

# a0 =  1.000000000000000
a1 = -3.580673542760982
a2 =  4.942669993770672
a3 = -3.114402101627517
a4 =  0.757546944478829

# Initialization
x1 = 0.0
x2 = 0.0
x3 = 0.0
x4 = 0.0
y1 = 0.0
y2 = 0.0
y3 = 0.0
y4 = 0.0

p = pyaudio.PyAudio()

# Open audio stream
stream = p.open(format      = pyaudio.paInt16,
                channels    = 2,
                rate        = RATE,
                input       = False,
                output      = True )


# Go through wave file 
for i in range(0, numBlocks):

    # Readig blocksize number of frames
    input_string = wf.readframes(BLOCKSIZE)

    # Convert string to tuple of numbers
    input_tuple = struct.unpack('h' * BLOCKSIZE, input_string)  # One-element tuple
    ##input_value = input_tuple[0]                    # Number

    for n in range(0, BLOCKSIZE):

        # Set input to difference equation
        x0 = input_tuple[n]

        # Difference equation
        y0 = b0*x0 + b2*x2 + b4*x4 - a1*y1 - a2*y2 - a3*y3 - a4*y4 

        # Delays
        x4 = x3
        x3 = x2
        x2 = x1
        x1 = x0
        y4 = y3
        y3 = y2
        y2 = y1
        y1 = y0

        output_block[2*n] = clip16(y0)
        output_block[2*n + 1] = x0
        output_data[n] = clip16(y0-10000)
        input_data[n] = x0 + 10000

    line_in.set_ydata(input_data)
    line_out.set_ydata(output_data)
    plt.pause(0.001)

    # Convert output value to binary string
    output_string = struct.pack('h'* 2 * BLOCKSIZE, *output_block)  

    # Write binary string to audio stream
    stream.write(output_string) 

print("**** Done ****")

stream.stop_stream()
stream.close()
p.terminate()
