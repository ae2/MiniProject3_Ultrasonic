% Elecanisms MiniProject III - Ultrasonic Ranging System
% Shivam Desai
% September 26th 2013
% Determining the bandpass filter

s=tf('s');


% We want the highpass to crossover around 35kHz (219911 rps)
R1 = 1;
C1 = 1e-9;
highpass = (R1*C1*s) / (R1*C1*s+1);

% We want the lowpass to crossover around 45kHz (282743 rps)
R2 = 100000;
C2 = 1e-9;
lowpass  = (1)       / (R2*C2*s+1);

% Should be a couple of thousand
gain = -R2/R1;

% Transfer function
A = gain*lowpass*highpass;

% PLEASE BE GOOD
margin(A);