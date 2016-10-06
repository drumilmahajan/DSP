
%% lab03_practice.m 

%  Implementation of fourth order filter using two second order filter. 


%% Creating an input signal
% The input signal is an impulse signal 

%%{
N = 4000; % Number of input values
x = zeros(N, 1); % Array of N values all initialized to 1
x(1) = 1;  % first value is 1, rest all zeros
%}



%% Plotting input function. 

figure(2)
clf
plot(x);
xlabel('value x for input')
title('Input signal')


%% Implementing the recursive filter 

Fs = 8000 ;   % Sampling frequency. 
F1 = 400;     % Frequency of the signal we want. The sampling
              % frequency must be more than twice of frequency we want to 
              % sample. Nyquist theorm  
f1 = F1/Fs;   % Normalized frequency. Ratio of Frequency/ And sampling fre
om1 = 2 * pi * f1 ; % angular frequency
r1 = 0.999;   % Radius of the pole 
a1 = [1 -2*r*cos(om1) r1^2]; 
b1 = 1; 
y = filter(b1, a1, x); 

%% Impulse response for filter 1

N = Fs;
n = 0:N;

imp = [1 zeros(1, N)];
h1 = filter(b1, a1, imp);

figure(1)
clf
plot(n/Fs, h1)
title('Impulse response with r = 0.999');
xlabel('Time (sec)')
zoom xon



%% Implementing fourth order recursive filter by passing the output of first filter through another second order filter.
 
% The input has already been filtered once so passing hte output through
% the filter again will serve the purpose. 
% The pole radus of the two filters is kept different. 

F1 = 400;     % Frequency of the signal we want. The sampling
              % frequency must be more than twice of frequency we want to 
              % sample. Nyquist theorm  
f1 = F1/Fs;   % Normalized frequency. Ratio of Frequency/ And sampling fre
om1 = 2 * pi * f1 ; % angular frequency
r2 = 0.998;   % Radius of the pole 
a2 = [1 -2*r*cos(om1) r2^2]; 
b2 = 1; 
z = filter(b2, a2, y); 

%% Impulse response for filter 2 

N = Fs;
n = 0:N;

imp = [1 zeros(1, N)];
h2 = filter(b2, a2, imp);

figure(2)
clf
plot(n/Fs, h2)
title('Impulse response with r = .998');
xlabel('Time (sec)')
zoom xon

%% Plotting the filtered output 

figure(3);
clf;
plot(z);
xlabel('N number of inputs');
title('Filtered output'); 









