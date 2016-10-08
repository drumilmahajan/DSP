
%% Load wave file

% output file of bandpass filter using canonical form
[x, Fs] = audioread('Filter_d_output.wav');
% output file of bandpass filter using direct form 
[y ,Fs] = audioread('bandpass_matlab.wav'); 
n = 1:N;
t = n/Fs;



%% Potting outputs 

figure
clf
subplot(2,1,1)
plot(t, x, t, y - 0.5)
xlabel('Time (sec)')
title('Outputs of filter')
zoom xon

% Plotting the input and the output signal overlapping each other

subplot(2,1,2)
plot(t, x, t, y)
xlabel('Time (sec)')
title('Outputs of canonical and direct form overlapping')
zoom xon





