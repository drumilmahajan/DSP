# play_vibrato_ver1.py
# Reads a specified wave file (mono) and plays it with a vibrato effect.
# (Sinusoidal time-varying delay)
# This implementation uses a circular buffer with two buffer indices.
# No interpoltion..

import pyaudio
import wave
import struct
import math
from myfunctions import clip16

wavfile = 'author.wav'
print 'Play the wave file: {0:s}.'.format(wavfile)

# Open wave file
wf = wave.open( wavfile, 'rb')

# Read wave file properties
CHANNELS = wf.getnchannels()        # Number of channels
RATE = wf.getframerate()            # Sampling rate (frames/second)
LEN  = wf.getnframes()              # Signal length
WIDTH = wf.getsampwidth()           # Number of bytes per sample

print('The file has %d channel(s).'         % CHANNELS)
print('The file has %d frames/second.'      % RATE)
print('The file has %d frames.'             % LEN)
print('The file has %d bytes per sample.'   % WIDTH)

# Vibrato parameters for one channel
f0 = 3
W = 0.3
# W = 0 # for no effct

# Vibrato parameter for second channel 
f1 = 2
W1 = 0.5

# Create a buffer (delay line) for past values
BUFFER_LEN =  1024                          # Buffer length
buffer = [0.0 for i in range(BUFFER_LEN)]   # Initialize to zero

# Buffer (delay line) indices
kr = 0  # read index
kw = int(0.5 * BUFFER_LEN)  # write index (initialize to middle of buffer)

# Buffer for second channel 

kr1 = 0 # read index
kw1 = int(0.5 * BUFFER_LEN) # write index initialized in the middle of the buffer

# print('The delay of {0:.3f} seconds is {1:d} samples.'.format(delay_sec, delay_samples))
print 'The buffer is {0:d} samples long.'.format(BUFFER_LEN)

# Open an output audio stream
p = pyaudio.PyAudio()
stream = p.open(format      = pyaudio.paInt16,
                channels    = 2,
                rate        = RATE,
                input       = False,
                output      = True )

print ('* Playing...')

# Loop through wave file 
for n in range(0, LEN):

    # Get sample from wave file
    input_string = wf.readframes(1)

    # Convert string to number
    input_value = struct.unpack('h', input_string)[0]

    # Compute output value - time-varying delay, no direct path
    output_value = buffer[int(kr)]  # use int() for integer
    output_value1 = buffer[int(kr1)]

    # Update buffer (pure delay)
    buffer[kw] = input_value
    buffer[kw1] = input_value

    # Increment read index channel one
    kr = kr + 1 + W * math.sin( 2 * math.pi * f0 * n / RATE )
        # Note: kr is not integer!

    # Increment read index channel two     
    kr1 = kr1 + 1 + W1 * math.sin( 2 * math.pi * f1 * n / RATE )


    # Ensure that 0 <= kr < BUFFER_LEN
    if kr >= BUFFER_LEN:
        # End of buffer. Circle back to front.
        kr = 0
   # Ensure that 0 <= kr1 < BUFFER_LEN 
    if kr1 >= BUFFER_LEN:
        # End of buffer. Circle back to front.
        kr1 = 0         

    # Increment write index    
    kw = kw + 1
    if kw == BUFFER_LEN:
        # End of buffer. Circle back to front.
        kw = 0

    # Increment write index    
    kw1 = kw1 + 1
    if kw1 == BUFFER_LEN:
        # End of buffer. Circle back to front.
        kw1 = 0    

    # Clip and convert output value to binary string
    output_string = struct.pack('hh', clip16(output_value), clip16(output_value1))

    # Write output to audio stream
    stream.write(output_string)

print('* Done')

stream.stop_stream()
stream.close()
p.terminate()
