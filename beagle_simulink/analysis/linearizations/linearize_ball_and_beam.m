% Generate function handles for the linearized furuta system
syms M m Ja L g r rdot alpha alphadot taualpha fr 'real'

q = [alpha; r];
dq = [alphadot; rdot];

x = [q;dq];
u = [taualpha; fr];

M = [Ja + m*r.^2,  0;
     0, 7/5];
C = [m*r*rdot, m*r*alphadot;
     -r,  0];
G = [0;
     -g*sin(theta)];

f = [dq;
     M\(u - C * dq - G)];

Z2 = zeros(2);
I2 = eye(2);
Ac = [Z2, I2; Z2, -M\C];
Bc = [Z2; inv(M)];
Gc = [0;0;G];

Amat = jacobian(f,x);
Bmat = jacobian(f,u);

%Write the non-linear dynamics to a file
matlabFunction(f ,'file','ballandbeamDynSys.m','vars',{'M', 'm', 'Ja', 'L', 'g', 'r', 'rdot', 'alpha', 'alphadot', 'taualpha', 'fr'},'outputs',{'dstates'});

%Write the non-linear dynamical matrices to a file
matlabFunction(Ac, Bc, Gc,'file','ballandbeamDynMat.m','vars',{'M', 'm', 'Ja', 'L', 'g', 'r', 'rdot', 'alpha', 'alphadot', 'taualpha', 'fr'},'outputs',{'Ac','Bc','Gc'});

%Write the linearized dynamics to a file
matlabFunction(Amat,Bmat,'file','ballandbeamLinSys.m','vars',{'M', 'm', 'Ja', 'L', 'g', 'r', 'rdot', 'alpha', 'alphadot', 'taualpha', 'fr'},'outputs',{'Amat','Bmat'});


