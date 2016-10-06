import pyaudio
import wave
import struct
import math
import sys

if len(sys.argv) > 1:
    wavfile = sys.argv[1]
else:
    print "Thing program needs an command line input of the file name of the wav file. Try again"

length = len(sys.argv)

for i in range(1,length):
    print 'Argument ' + str(i) +  ' is: ' +  sys.argv[i]



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

print("Play the wave file %s." % wavfile)
wf = wave.open( wavfile, 'rb' )

num_channels = wf.getnchannels()       	# Number of channels
RATE = wf.getframerate()                  # Sampling rate (frames/second)
signal_length  = wf.getnframes()       	# Signal length
width = wf.getsampwidth()       		# Number of bytes per sample

p = pyaudio.PyAudio()


stream = p.open(format      = pyaudio.paInt16,
                channels    = num_channels,
                rate        = RATE,
                input       = False,
                output      = True )

input_string = wf.readframes(1)     

while input_string != '':

    if num_channels == 2:
        # Convert string to numbers
        input_tuple = struct.unpack('hh', input_string)  # produces a two-element tuple

        # Compute output values
        output_value0 = clip_n(gain * input_tuple[0],16)
        output_value1 = clip_n(gain * input_tuple[1],16)

        # Convert output value to binary string
        # output_string = struct.pack('hh', output_value0, output_value1)
        # Equivalently:
        output_values = [output_value0, output_value1]
        output_string = struct.pack('hh', *output_values)

    elif num_channels == 1:

        input_value = struct.unpack('h', input_string)[0]
        # ... equivalently:
        # input_tuple = struct.unpack('h', input_string)  # One-element tuple
        # input_value = input_tuple[0]                    # Number

        # Compute output value
        output_value = clip_n(gain * input_value,16)    # Number

        # Convert output value to binary string
        output_string = struct.pack('h', output_value)      

    # Write output value to audio stream
    stream.write(output_string)

    # Get next frame
    input_string = wf.readframes(1)   

                    