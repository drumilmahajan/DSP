# Created by Drumil Mahajan
# Real Time Digital Signal Processing lab07
# New York University, November 2016.



import pyaudio
import struct
import cmath
import wave
import math

# Function to keep the output of filter in the limit of 16bit signed integer to 
# avoid overflow
from myfunctions import clip16


WIDTH = 2           # Number of bytes per sample
CHANNELS = 1        # mono
RATE = 16000        # Sampling rate (frames/second)
DURATION = 4        # duration of processing (seconds)
N = DURATION*RATE   # N : Number of samples to process




# Complex filter coffecients

b0 = 0.0423 + 0.0000j
b1 = 0.0000 - 0.1193j
b2 = -0.2395 - 0.0000j
b3 = -0.0000 + 0.3208j
b4 = 0.3208 + 0.0000j
b5 = 0.0000 - 0.2395j
b6 = -0.1193 - 0.0000j
b7 = -0.0000 + 0.0423j

a0 =  1.0000 + 0.0000j
a1 = -0.0000 + 1.2762j
a2 = -2.6471 - 0.0000j
a3 =  0.0000 - 2.2785j
a4 =  2.1026 + 0.0000j
a5 = -0.0000 + 1.1252j
a6 = -0.4876 - 0.0000j
a7 =  0.0000 - 0.1136j

# Delay value initilization

# Input delays
x1 = 0.0 + 0.0j
x2 = 0.0 + 0.0j
x3 = 0.0 + 0.0j
x4 = 0.0 + 0.0j
x5 = 0.0 + 0.0j
x6 = 0.0 + 0.0j
x7 = 0.0 + 0.0j

# Output delays
y1 = 0.0 + 0.0j
y2 = 0.0 + 0.0j
y3 = 0.0 + 0.0j
y4 = 0.0 + 0.0j
y5 = 0.0 + 0.0j
y6 = 0.0 + 0.0j
y7 = 0.0 + 0.0j


wave_file_name = 'author.wav'

wf = wave.open(wave_file_name, 'rb')
print wf.getframerate()

p = pyaudio.PyAudio()
# Open audio stream
stream = p.open(format = p.get_format_from_width(WIDTH),
                channels = CHANNELS,
                rate = RATE,
                input = True,
                output = True)

print("**** Start ****")

input_string = wf.readframes(1)

f1 = 400
#n = 0
for n in range(0, N):
#while input_string != '':
    
    # Get one frame from audio input (microphone)
    input_string = stream.read(1)
    
    
    # Convert binary string to tuple of numbers
    input_tuple = struct.unpack('h', input_string)

    # Convert one-element tuple to number
    input_value = input_tuple[0]

    # Set input to difference equation
    x0 = input_value

    # Difference equation
    y0 = b0*x0 + b1*x1 + b2*x2 + b3*x3 + b4*x4 + b5*x5 + b6*x6 + b7*x7 - a1*y1 - a2*y2 - a3*y3 - a4*y4 - a5*y5 - a6*y6 - a7*y7 
    
    # Delays
    x7 = x6
    x6 = x5
    x5 = x4
    x4 = x3
    x3 = x2
    x2 = x1
    x1 = x0
    y7 = y6
    y6 = y5
    y5 = y4
    y4 = y3
    y3 = y2
    y2 = y1
    y1 = y0
    
    power = 1j*2*(math.pi)*f1*n/16000
    z = y0 * cmath.exp(power)
    #z = 0.0 + 0.0j
    #z = y0 * (math.cos(2*(math.pi)*f1*n/16000))
    # g = r .* exp( I * 2 * pi * f1 * t );  
   
    stream.write(struct.pack('h', clip16(z.real)))  
    #stream.write(struct.pack('h', x0)) 
    
    #input_string = wf.readframes(1)
    #n = n + 1

print "*****Done****"        
    

