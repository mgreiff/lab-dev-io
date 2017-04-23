%% Parameters set heuristically according to zeiger nichols method
Ku = 120;    % Oscillation gain
Tu = 25/40;  % Oscillation Period
N = 100;     % Derivative coefficient

% Method can be set to 'classic', 'pessen', 'overshoot' or 'best' where the
% first three are based on zeiger nichols method (which gets the
% proportional gain way too high), and the last one is a better tuning set
% by 
method = 'best';
switch method
    case 'classic'
        P = 0.6*Ku;
        I = Tu/2;
        D = Tu/8;
    case 'pessen'
        P = 0.7*Ku;
        I = Tu/2.5;
        D = 3*Tu/20;
    case 'overshoot'
        P = 0.2*Ku;
        I = Tu/2;
        D = Tu/3;
    case 'best'
        P = 11;
        I = 3.5;
        D = 2;
end