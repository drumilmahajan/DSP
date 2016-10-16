# playAM_blocking_fix.py
# Play a mono wave file with amplitude modulation. 
# This implementation reads and plays a block at a time (blocking)
# and corrects for block-to-block angle mismatch.
# Modified by Drumil Mahajan as a part of course work. 

# f0 = 0      # Normal audio
f0 = 2000    # 'Duck' audio
f1 = 1000

BLOCKSIZE = 64      # Number of frames per block

import pyaudio
import struct
import wave
import math

WIDTH = 2           # Number of bytes per sample
CHANNELS = 1        # mono
RATE = 16000        # Sampling rate (frames/second)
DURATION = 10        # duration of processing (seconds)
LEN = DURATION*RATE   # N : Number of samples to process

def clip16( x ):    
    # Clipping for 16 bits
    if x > 32767:
        x = 32767
    elif x < -32768:
        x = -32768
    else:
        x = x        
    return int(x)

fileName = "Stereo.wav"

# Opening wave file to be written
wavOut = wave.open(fileName , 'w')
print("Writing in the wave file %s " % fileName)


# Set parameters for the output file 
wavOut.setnchannels(2)
wavOut.setsampwidth(WIDTH)
wavOut.setframerate(RATE)

# Open audio stream
p = pyaudio.PyAudio()
stream = p.open(format = p.get_format_from_width(WIDTH),
                channels = CHANNELS,
                rate = RATE,
                input = True,
                output = False)

                

# Create block (initialize to zero)
output_block = [0 for n in range(0, 2*BLOCKSIZE)]

# Number of blocks in DURATION
num_blocks = int(math.floor(LEN/BLOCKSIZE))

# Initialize angle
theta = 0.0
theta1 = 0.0

# Block-to-block angle increment
theta_del = (float(BLOCKSIZE*f0)/RATE - math.floor(BLOCKSIZE*f0/RATE)) * 2.0 * math.pi
theta_del1 = (float(BLOCKSIZE*f1)/RATE - math.floor(BLOCKSIZE*f1/RATE)) * 2.0 * math.pi

print('* Playing...')

# Go through the input from mic for time = DURATION
for i in range(0, num_blocks):

     # Get BLOCKSIZE number of frames from audio input (microphone)
    input_string = stream.read(BLOCKSIZE)

    # Convert binary string to tuple of numbers
    input_tuple = struct.unpack('h'*BLOCKSIZE, input_string)

    # Go through block
    for n in range(0, BLOCKSIZE):
        # Amplitude modulation  (f0 Hz cosine)
        output_block[2*n] = clip16( input_tuple[n] * math.cos(2*math.pi*n*f0/RATE + theta) )
        output_block[2*n+1] = clip16( input_tuple[n] * math.cos(2*math.pi*n*f1/RATE + theta1) )
        # output_block[n] = input_tuple[n] * 1.0  # for no processing

    # Set angle for next block
    theta = theta + theta_del
    theta1 = theta1 + theta_del1

    # Convert values to binary string
    output_string = struct.pack('h' * 2 * BLOCKSIZE, *output_block)

    # Write binary string to audio output stream
    wavOut.writeframes(output_string)

print('* Done')

stream.stop_stream()
stream.close()
p.terminate()

# Original file by Gerald Schuller, October 2013
