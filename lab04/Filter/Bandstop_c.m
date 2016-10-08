
%% Load wave file

[x, Fs] = audioread('author.wav');
N = length(x);
n = 1:N;
t = n/Fs;

figure(1)
clf
plot(t, x)
xlabel('Time (sec)')
title('Speech signal')

%%

x_clipped =  min(1, max(-1, x*1000));

figure(1)
clf
plot(t, x_clipped, t, x)
xlabel('Time (sec)')
title('Clipped speech signal')
ylim([-2 2])

%% Make filter


%band stop filter 

[b, a] = butter(2, [500 1000]*2/Fs, 'stop');

%% Pole-zero diagram

figure(1)
clf
zplane(b, a)
title('Pole-zero diagram')

%% Frequency response

[H, om] = freqz(b, a);
f = om*Fs/(2*pi);
figure(1)
clf
plot(f, abs(H))
xlabel('Frequency (Hz)')
xlim([0 3000])
title('Frequency response')

%% Impulse response

L = 300;
imp = [1 zeros(1, L)];
h = filter(b, a, imp);

figure(1)
clf
stem(0:L, h)
xlabel('Discrete time (n)')
title('Impulse response')

%%

figure(1)
clf
plot((0:L)/Fs, h)
xlabel('Time (sec)')
title('Impulse response')

%% Apply filter to speech signal

% bandpass filter output of bandstop filter using Directform bandstop

y = filter(b, a, x);

%% Plotting two signals. One which is filtered by matlab and one which is filtered using Filter_c.py


figure(1)
clf
plot(t, x, t, y - 0.5)
xlabel('Time (sec)')
title('Speech signal and filtered speech signal')
zoom xon

%% Write output signal to wave file

audiowrite('output_matlab.wav', y, Fs);

sound(y, Fs)

%% 
format long
b'
a'



