# Modified by Drumil Mahajan
# New York University
# October 2016

# play_vibrato_ver2.py
# Reads input from microphone and plays it with different vibrato effect on left and right channel.
# (Sinusoidal time-varying delay)
# This implementation uses a circular buffer with two buffer indices.
# Uses linear interpolation

import pyaudio
import wave
import struct
import math
from myfunctions import clip16

# Input properties
WIDTH = 2
CHANNELS = 1
RATE = 16000
DURATION = 10
N = DURATION*RATE

# OUTPUT PROPERTIES 

WIDTH_O = 2
CHANNELS_O = 2

#Same as input parameters
#RATE = 16000
#DURATION_O = 10
#N = DURATION*RATE

# Vibrato parameters for left channel
f0 = 2
W = 0.2
# W = 0 # for no effct

# vibrato parameter for right channel
f0_R = 10
W_R = 0.2

# OR
# f0 = 20
# ratio = 1.06
# W = (ratio - 1.0) / (2 * math.pi * f0 )
# print W

#BLOCKSIZE 
BLOCKSIZE = 64

# Create a buffer (delay line) for past values for Left Channel
buffer_MAX =  1024                          # Buffer length
buffer = [0.0 for i in range(buffer_MAX)]   # Initialize to zero

# Create a buffer (delay line) for past values for Right channel 
buffer_MAX_R =  1024                          # Buffer length
buffer_R = [0.0 for i in range(buffer_MAX)]   # Initialize to zero

# Buffer (delay line) indices for Left Channel
kr = 0  # read index
kw = int(0.5 * buffer_MAX)  # write index (initialize to middle of buffer)
kw = buffer_MAX/2

# Buffer (delay line) indicies for right channel

kr_R = 0  # read index
kw_R = int(0.5 * buffer_MAX)  # write index (initialize to middle of buffer)
kw_R = buffer_MAX/2

# print('The delay of {0:.3f} seconds is {1:d} samples.'.format(delay_sec, delay_samples))
print 'The buffer is {0:d} samples long.'.format(buffer_MAX)

# Open an output audio stream
p = pyaudio.PyAudio()

#Creating input stream
stream_in = p.open(format      = pyaudio.paInt16,
                channels    = CHANNELS,
                rate        = RATE,
                input       = True,
                output      = False )
#Creating output stream two channel
stream_out = p.open(format      = pyaudio.paInt16,
                channels    = CHANNELS_O,
                rate        = RATE,
                input       = False,
                output      = True )


# Creating an input of size BLOCKSIZE and initializing it to 0.
input_block = [0 for i in range(0,BLOCKSIZE)]

# Creating two output blocks of size 2*BLOCKSIZE for stereo outputs
output_block = [0 for i in range(0,2*BLOCKSIZE)]



output_all = ''            # output signal in all (string)

print ('* Playing...')

# Number of blocks 
num_blocks = int(math.floor(N/BLOCKSIZE))
for n in range(0, num_blocks):

    # Get blocksize number of frames from audio input (microphone)
    input_string = stream_in.read(BLOCKSIZE)

    # Convert binary into tuple of numbers
    input_value = struct.unpack('h'*BLOCKSIZE, input_string)

    # Traversing the block

    for n in range(0, BLOCKSIZE):
        
    # Get previous and next buffer values (since kr is fractional)
    # Processing for left channel
        kr_prev = int(math.floor(kr))               
        kr_next = kr_prev + 1
        frac = kr - kr_prev    # 0 <= frac < 1
        if kr_next >= buffer_MAX:
            kr_next = kr_next - buffer_MAX
    

        # Compute output value using interpolation
        output_value_L = (1-frac) * buffer[kr_prev] + frac * buffer[kr_next]

        # Update buffer (pure delay)
        buffer[kw] = input_value[n]

        # Increment read index
        kr = kr + 1 + W * math.sin( 2 * math.pi * f0 * n / RATE )
            # Note: kr is fractional (not integer!)

        # Ensure that 0 <= kr < buffer_MAX
        if kr >= buffer_MAX:
            # End of buffer. Circle back to front.
            kr = 0

        # Increment write index    
        kw = kw + 1
        if kw == buffer_MAX:
            # End of buffer. Circle back to front.
            kw = 0
        
        # Processing for Right channel     
        kr_prev_R = int(math.floor(kr_R))               
        kr_next_R = kr_prev_R + 1
        frac_R = kr_R - kr_prev_R    # 0 <= frac < 1
        if kr_next_R >= buffer_MAX_R:
            kr_next_R = kr_next_R - buffer_MAX_R
    

        # Compute output value using interpolation
        output_value_R = (1-frac_R) * buffer_R[kr_prev_R] + frac_R * buffer_R[kr_next_R]

        # Update buffer (pure delay)
        buffer_R[kw] = input_value[n]

        # Increment read index
        kr_R = kr_R + 1 + W_R * math.sin( 2 * math.pi * f0_R * n / RATE )
        # Note: kr is fractional (not integer!)

        # Ensure that 0 <= kr < buffer_MAX
        if kr_R >= buffer_MAX_R:
            # End of buffer. Circle back to front.
            kr_R = 0

        # Increment write index    
        kw_R = kw_R + 1
        if kw_R == buffer_MAX_R:
            # End of buffer. Circle back to front.
            kw_R = 0    

        # clip and put output values in two channels
        output_block[2*n] = clip16(output_value_L)
        output_block[2*n + 1] = clip16(output_value_R)

    # Convert output to binary string

    output_string = struct.pack('h'*2*BLOCKSIZE, *output_block)
    # write output to output stream
    stream_out.write(output_string)

    #output_all = output_all + output_string     # append new to total

print('* Done')

stream_in.stop_stream()
stream_in.close()
stream_out.stop_stream()
stream_out.close()
p.terminate()

