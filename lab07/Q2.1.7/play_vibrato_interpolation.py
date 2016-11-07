# Author : Drumil Mahajan
# Real Time Digital Signal Processing
# New York University, November 2017

# play_vibrato_interpolation.py
# Reads a specified wave file (mono) and plays it with a vibrato effect.
# (Sinusoidal time-varying delay)
# This implementation uses a circular buffer with two buffer indices.
# Uses linear interpolation


import pyaudio
import wave
import struct
import math
import time
from myfunctions import clip16


# Setting parameters for the stream
WIDTH = 2
CHANNELS = 1
RATE = 16000

# Vibrato parameters
f0 = 2
W = 0.2
# W = 0 # for no effct

# f0 = 10
# W = 0.2

# OR
# f0 = 20
# ratio = 1.06
# W = (ratio - 1.0) / (2 * math.pi * f0 )
# print W

# Create a buffer (delay line) for past values
buffer_MAX =  1024                          # Buffer length
buffer_ = [0.0 for i in range(buffer_MAX)]   # Initialize to zero

# Buffer (delay line) indices
kr = 0  # read index
kw = int(0.5 * buffer_MAX)  # write index (initialize to middle of buffer)
kw = buffer_MAX/2
n_global = 0

# print('The delay of {0:.3f} seconds is {1:d} samples.'.format(delay_sec, delay_samples))
print 'The buffer is {0:d} samples long.'.format(buffer_MAX)

def my_callback_fun(input_string , block_size, time_info, status):
    global kr, kw, buffer_MAX , buffer_, W, f0, n_global
    # Get sample from wave file
    y = [0 for i in range(block_size)]
    
    input_value = struct.unpack('h'* block_size, input_string)
    for n in range(0,block_size):
        
        # Get previous and next buffer values (since kr is fractional)
        kr_prev = int(math.floor(kr))               
        kr_next = kr_prev + 1
        frac = kr - kr_prev    # 0 <= frac < 1
        if kr_next >= buffer_MAX:
            kr_next = kr_next - buffer_MAX
        #print input_value
        # Compute output value using interpolation
        y[n] = (1-frac) * buffer_[kr_prev] + frac * buffer_[kr_next]
    
        # Update buffer (pure delay)
        buffer_[kw] = input_value[n]
    
        # Increment read index
        kr = kr + 1 + W * math.sin( 2 * math.pi * f0 * n_global / RATE )
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
        
        #Clip
        y[n] = clip16(y[n])
        
        # Increment n_global to maintain vibrato effect.
        n_global = n_global + 1
    
        # Packing the output values in output string and returning    
    output_string = struct.pack('h' * block_size, *y)
    return (output_string, pyaudio.paContinue)

    
    
 # Open an output audio stream
p = pyaudio.PyAudio()
stream = p.open(format      = pyaudio.paInt16,
                channels    = 1,
                rate        = RATE,
                input       = True,
                output      = True,
                stream_callback = my_callback_fun)

print ('* Playing...')
stream.start_stream()
# Stream on for 10 seconds
time.sleep(10.0)
# Stopping stream
stream.stop_stream()
print('* Done')
stream.close()
p.terminate()


