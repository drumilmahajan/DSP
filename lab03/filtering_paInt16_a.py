from math import cos , pi
import pyaudio
import struct

# 16 bit / sample

# Fs : Sampling frequency ( samples / second )
Fs = 8000
# Try Fs = 16000 and 32000

T = 1 # T : Duration of audio to play ( seconds )
N = T*Fs # N : Number of samples to play

# Difference equation coefficients
a1 = -1.8999
a2 = 0.9977

# Initialization
y1 = 0.0
y2 = 0.0

# Initailzation of final output 
z1 = 0.0
z2 = 0.0

gain = 10000.0

p = pyaudio . PyAudio ()
stream = p. open ( format = pyaudio . paInt16 ,
channels = 1,
rate = Fs ,
input = False ,
output = True )

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

for n in range (0, N):

# Use impulse as input signal
    if n == 0:
        x0 = 1.0
    else :
        x0 = 0.0

    # Difference equation
    y0 = x0 - a1 * y1 - a2 * y2

    # Passing the output of first difference equation as the 
    # input to the second difference equation.

    z0 = y0 - a1 * z1 - a2 * z2    

    # Delays 
    y2 = y1
    y1 = y0
    z2 = z1
    z1 = z0
  

    # Output
    out = clip_n( gain * y0 , 16 ) 
    print out
    str_out = struct . pack ('h', out) # 'h' for 16 bits
    stream . write ( str_out )

print ("* done *")

stream . stop_stream ()
stream . close ()
p. terminate ()