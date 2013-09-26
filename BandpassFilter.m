% Elecanisms MiniProject III - Ultrasonic Ranging System
% Shivam Desai
% September 26th 2013
% Determining the bandpass filter

clear;
clc;

% s = jw
s=tf('s');

% We want the highpass to crossover around 35kHz (219911 rps)
C1 = 1e-9;
%R1 = 1/(2*pi*C1*35000);
R1 = 6024;
highpass = (R1*C1*s) / (R1*C1*s+1);

% We want the lowpass to crossover around 45kHz (282743 rps)
C2 = 1e-10;
%R2 = 1/(2*pi*C2*45000);
R2 = 30100;
lowpass  = (1)       / (R2*C2*s+1);

% Crossover at as close to 35kHz and 45kHz as possible
Fc1 = 1 / (2*pi*R1*C1)
Fc2 = 1 / (2*pi*R2*C2)

% Should be a couple of thousand
gain = -R2/R1;

% Transfer function
A = gain*highpass*lowpass;

% PLEASE BE GOOD
margin(A);