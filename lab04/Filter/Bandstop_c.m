
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


%% Apply filter to speech signal

y = filter(b, a, x);

figure(1)
clf
plot(t, x, t, y - 0.5)
xlabel('Time (sec)')
title('Speech signal and filtered speech signal')
zoom xon

%% Write output signal to wave file

audiowrite('output_matlab.wav', y, Fs);



%%

sound(y, Fs)

%% 
format long
b'
a'



