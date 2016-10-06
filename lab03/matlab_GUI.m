


%% MATLAB GUI
function plot_for_impulse_response

global r
global F1

r = .999
F1 = 400


N = 4000; % Number of input values
x = zeros(N, 1); % Array of N values all initialized to 1
x(1) = 1;  % first value is 1, rest all zeros



figure(1);
clf
line_handle = plot(x);
title('Noisy data', 'fontsize', 12 )
xlabel('Time')
box off
xlim([0, N]);
ylim([-3 3])

box off

drawnow;


pole_slider = uicontrol('Style', 'slider', ...
    'Min', 0.8, 'Max', 1,...
    'Value', 1, ...
    'SliderStep', [0.001 0.01], ...
    'Position', [5 5 200 20], ...           % [left, bottom, width, height]
    'Callback',  {@fun1, line_handle, x});

radius_slider = uicontrol('Style', 'slider', ...
    'Min', 0, 'Max', 1,...
    'Value', 1, ...
    'SliderStep', [0.01 0.1], ...
    'Position', [350 5 200 20], ...           % [left, bottom, width, height]
    'Callback',  {@fun2, line_handle, x});



end

function fun1(hObject, eventdata, line_handle , x)

global r
global F1
r = get(hObject, 'Value');

Fs = 8000 ;   % Sampling frequency. 
     %  of the signal we want. The sampling
              % frequency must be more than twice of frequency we want to 
              % sample. Nyquist theorm  
f1 = F1/Fs;   % Normalized frequency. Ratio of Frequency/ And sampling fre
om1 = 2 * pi * f1 ; % angular frequency

a = [1 -2*r*cos(om1) r^2]; 
b = 1; 
y = filter(b, a, x); 

figure(2)
zplane(b,a)

set(line_handle, 'ydata',  y);
title( sprintf('Radius = %.3f , frequency = %.3f ', r , F1), 'fontsize', 12 )

figure(3)
[H, om] = freqz(b, a);
f = om / (2*pi) * Fs;
plot(f, abs(H))
title('Frequency response')
xlabel('Frequency (cycles/second)')
xlim([0 1000])
grid

end

function fun2(hObject, eventdata, line_handle , x)

global r
global F1
F1 = 1000*get(hObject, 'Value');

Fs = 8000 ;   % Sampling frequency. 
    %  of the signal we want. The sampling
              % frequency must be more than twice of frequency we want to 
              % sample. Nyquist theorm  
f1 = F1/Fs;   % Normalized frequency. Ratio of Frequency/ And sampling fre
om1 = 2 * pi * f1 ; % angular frequency
   % Radius of the pole 
a = [1 -2*r*cos(om1) r^2]; 
b = 1; 
y = filter(b, a, x); 

figure(2)
zplane(b,a)

figure(3)
[H, om] = freqz(b, a);
f = om / (2*pi) * Fs;
plot(f, abs(H))
title('Frequency response')
xlabel('Frequency (cycles/second)')
xlim([0 1000])
grid

set(line_handle, 'ydata',  y);
title( sprintf('Radius = %.3f , frequency = %.3f ', r , F1), 'fontsize', 12 )

end




