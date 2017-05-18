Am = [-2,-2;1,0];
Bm = [1;0];
Cm = [0,2];

sys = ss(Am, Bm, Cm, []);
sysd = c2d(sys, timestep);

Amd = sysd.A;
Bmd = sysd.B;
Cmd = sysd.C;

Gammau = 10;
Gammax = [10, 10];
Gammae = 10;