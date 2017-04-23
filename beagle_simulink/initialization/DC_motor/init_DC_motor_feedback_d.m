%% Discrete time
method = 'slow';
switch method
    case 'deadbeat'
        P = [0;0;0];
    case 'fast'
        P = [0.5;0.5;0.5];
    case 'slow'
        P = [0.8;0.8;0.8];
end
Kd = acker(Ad, Bd, P);
FFgaind = 1/([1,0,0]*inv(eye(3) - (Ad - Bd * Kd))*Bd);