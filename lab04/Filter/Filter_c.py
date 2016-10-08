# play_wav_mono.py

import pyaudio
import wave
import struct
import math


def clip16( x ):    
    # Clipping for 16 bits
    if x > 32767:
        x = 32767
    elif x < -32768:
        x = -32768
    else:
        x = x        
    return int(x)



wavfile = 'author.wav'
output = 'Filter_c_output.wav'
# wavfile = 'sin01_mono.wav'
# Open wave file to be written to. 
wf_out = wave.open(output , 'w')

print("Play the wave file %s." % wavfile)

# Open wave file (should be mono channel)
wf = wave.open( wavfile, 'rb' )

# Read the wave file properties
num_channels = wf.getnchannels()       	# Number of channels
RATE = wf.getframerate()                # Sampling rate (frames/second)
signal_length  = wf.getnframes()       	# Signal length
width = wf.getsampwidth()       		# Number of bytes per sample

# Set parameters for the output file 
wf_out.setnchannels(num_channels)
wf_out.setsampwidth(width)
wf_out.setframerate(RATE)


print("The file has %d channel(s)."            % num_channels)
print("The frame rate is %d frames/second."    % RATE)
print("The file has %d frames."                % signal_length)
print("There are %d bytes per sample."         % width)


# Difference equation coefficients
b0 =  0.870330779310479
b1 = -3.347537822194806
b2 = 4.959555379629657
b3 = -3.347537822194806
b4 =  0.870330779310479

#a0 =  1.000000000000000
a1 = -3.580673542760981
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
                channels    = num_channels,
                rate        = RATE,
                input       = False,
                output      = True )

# Get first frame
input_string = wf.readframes(1)

while input_string != '':

    # Convert string to number
    input_tuple = struct.unpack('h', input_string)  # One-element tuple
    input_value = input_tuple[0]                    # Number

    # Set input to difference equation
    x0 = input_value

    # Difference equation
    y0 = b0*x0 + b1*x1 + b2*x2 + b3*x3 + b4*x4 - a1*y1 - a2*y2 - a3*y3 - a4*y4 

    # Delays
    x4 = x3
    x3 = x2
    x2 = x1
    x1 = x0
    y4 = y3
    y3 = y2
    y2 = y1
    y1 = y0

    # Compute output value
    output_value = clip16(y0)    # Number

    # Convert output value to binary string
    output_string = struct.pack('h', output_value)  

    # Write binary string to audio stream
    stream.write(output_string) 

    #Writing to the audio file  
    wf_out.writeframes(output_string)                    

    # Get next frame
    input_string = wf.readframes(1)

print("**** Done ****")
wf_out.close()
stream.stop_stream()
stream.close()
p.terminate()
