# play_wav_stereo_ver2.py

import pyaudio
import wave
import struct
import math
import sys

if len(sys.argv) > 1:
    wavfile = sys.argv[1]
else:
    print "Thing program needs an command line input of the file name of the wav file. Try again"

def clip_n(y , n):
    '''
    This function takes two arguments.
    y is a floating point number
    n is a integer, which is equal to number of bits.

    This funtions bound the value y between max and min of n bit signed number
    '''
    max = 2**(n-1) - 1
    min = -2**(n)
    if y > max:  
        return max
    elif y < min:
        return min
    else:
        return y  

gain = 0.5

# wavfile = "cat01.wav"
# wavfile = 'sin01_mono.wav'


print("Play the wave file %s." % wavfile)
wf = wave.open( wavfile, 'rb' )

# Read the wave file properties
num_channels = wf.getnchannels()       	# Number of channels
RATE = wf.getframerate()                  # Sampling rate (frames/second)
signal_length  = wf.getnframes()       	# Signal length
width = wf.getsampwidth()       		# Number of bytes per sample

print("The file has %d channel(s)."            % num_channels)
print("The frame rate is %d frames/second."    % RATE)
print("The file has %d frames."                % signal_length)
print("There are %d bytes per sample."         % width)
p = pyaudio.PyAudio()


stream = p.open(format      = pyaudio.get_format_from_width(width),
                channels    = num_channels,
                rate        = RATE,
                input       = False,
                output      = True )

# Read first frame
input_string = wf.readframes(1)   

encoding_format = ''
if width == 1: 
    encoding_format = 'b' 
elif width == 2:    
     encoding_format = 'h'
elif width == 4:
    encoding_format = 'hh'
while input_string != '':

    

    # Convert string to numbers
    input_tuple = struct.unpack(encoding_format, input_string)  # produces a two-element tuple
    # Compute output values
    output_value0 = clip_n(gain * input_tuple[0], 8*width)

    if width  == 4: 
        output_value1 = clip_n(gain * input_tuple[1], 8*width)
        output_string = struct.pack(encoding_format, output_value0, output_value1)
    # Convert output value to binary string
    # output_string = struct.pack('hh', output_value0, output_value1)
    # Equivalently:
    else:
        output_string = struct.pack(encoding_format, output_value0)

    # Write output value to audio stream
    stream.write(output_string)

    # Get next frame
    input_string = wf.readframes(1)
    

print("**** Done ****")

stream.stop_stream()
stream.close()
p.terminate()
