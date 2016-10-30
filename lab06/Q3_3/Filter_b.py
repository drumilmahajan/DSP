# Reads an audio wav file
# Filter it using band pass filter
# PLays the filter and audio output in different channels
# Plots the real time output of the waveform.
# reads blocks of data and process it at once. 
# plots the left and right channel. 
# Original file by Gerald Schuller, October 2013
# Modified by Drumil Mahajan
# Oct, 2016, New York University

import pyaudio
import wave
import struct
import math
from math import sin, cos, pi
from matplotlib import pyplot as plt
import pylab
import numpy as np
import matplotlib
matplotlib.use('GTKAgg') 
from scipy import signal


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


# Creating variables to read  and write blocks

BLOCKSIZE = 4096 # Block size // user defined.
numBlocks = int(math.floor(signal_length/BLOCKSIZE)) # Total number of blocks in the input. 
output_block = [0.0 for n in range(0, 2 * BLOCKSIZE)] # output block, initialized to zero. size twice in BLOCKSIZE to store the original input and filtered output
##
# This array is to store a sequence of input values which will be processed at once by lfilter. 
x0_arr= [0.0 for n in range(0, BLOCKSIZE)]
zf = [0.0,0.0,0.0,0.0] # This the the array to store the final values zf from the filter so that there are no transient effects. 
error_signal = [0.0 for n in range(0, BLOCKSIZE)] # Stores the difference between output of normal filter and lfilter
##

# Creating line space , N points from 0 to BLOCKSIZE
n = np.linspace(0, BLOCKSIZE-1, BLOCKSIZE)

# Setting up the figure/plot and turning of interative mode. 
plt.ion() # Turn on interactive mode so plot gets updated

fig = plt.figure(1)

input_plot = plt.subplot(3, 1, 1)
input_plot.set_title('ERROR PLOT')
line_in, = plt.plot(error_signal)
plt.ylim(-3, 3)
plt.xlim(0, BLOCKSIZE)
plt.show()

# Difference equation coefficients for bandpass filter 500-100 Hz. 
b0 =  0.008442692929081
b2 = -0.016885385858161
b4 =  0.008442692929081

a0 =  1.000000000000000
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



# Creating arrays for filter coeeficients
b_array = [b0, 0.0, b2, 0.0 , b4]
a_array = [a0, a1, a2, a3, a4]

p = pyaudio.PyAudio()

# Array to plot difference between input and output
# Array for plotting output signal through lfilter
output_lfilter = []

#Array for plotting output signal through normal filter (without using scipy lfilter)
output_manual = []

# Open audio stream
stream = p.open(format      = pyaudio.paInt16,
                channels    = 2,
                rate        = RATE,
                input       = False,
                output      = True )




# Go through wave file 
for i in range(0, numBlocks):
    #print "hello"

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
    
        x0_arr[n] = x0
        #print y0
        # Writing on the left channel values of the output_block
        output_block[2*n] = clip16(y0)
        output_manual.append(clip16(y0))

    # Filtering using lfilter
    output_scipy, zf = signal.lfilter(b_array, a_array, x0_arr, axis = -1,  zi = zf)
    
    # Writing riht channel values in output block
    for k in range(0, BLOCKSIZE):
        #output_block[2*k] = x0_arr[k]
        output_block[2*k + 1] = clip16(output_scipy[k])
        output_lfilter.append(clip16(output_scipy[k]))
        error_signal[k] = output_block[2*k + 1] - output_block[2*k]
    
    #Update the plot with error signal
    line_in.set_ydata(error_signal)
    plt.pause(0.0001)

    # Convert output value to binary string
    output_string = struct.pack('h'* 2 * BLOCKSIZE, *output_block)  

    # Write binary string to audio stream
    stream.write(output_string) 

print("**** Done ****")

input_plot = plt.subplot(3, 1, 2)
input_plot.set_title('Filter output without scipy filter')
line, = plt.plot(output_manual)
plt.ylim(-16000, 16000)
plt.show()

input_plot = plt.subplot(3, 1, 3)
('Filter output with scipy filter')
line, = plt.plot(output_lfilter)
plt.ylim(-16000, 16000)
plt.show()

stream.stop_stream()
stream.close()
p.terminate()
