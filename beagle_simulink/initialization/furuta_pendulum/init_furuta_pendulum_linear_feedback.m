%% Controller for linearization about (0,0,0,0)
% with closed loop characteristic equation
%
% (s^2 + 2*z1*w1*s + w1^2)*(s^2 + 2*z1*w1*s + w1^2)=0
%

% Closed loop specifications
w1 = 10;
z1 = 0.7;
w2 = 5;
z2 = 0.7;
s = tf('s');
pzmap((s^2 + 2*z1*w1*s + w1^2)*(s^2 + 2*z2*w2*s + w2^2))

% Controller synthesis
lphi       = -((alpha*beta - gamma^2)/delta)*w1^2*w2^2;
lphidot    = -2*((alpha*beta - gamma^2)/delta)*w1*w2*(w1*z2 + w2*z1);
ltheta     = -(alpha*delta)/gamma...
             -((alpha*beta-gamma^2)/gamma)...
             *((beta/delta)*w1^2*w2^2 + w1^2 + w2^2 + 4*w1*w2*z1*z2);
lthetadot  = -2*((alpha*beta - gamma^2)/gamma)...
               *((beta/delta)*w1^2*w2*z2 +...
                 (beta/delta)*w1*w2^2*z1 +...
                  w1*z1 + w2*z2);
L = [lphi, ltheta, lphidot, lthetadot];

%% Controller for linearization about (0,pi,0,0)
% with closed loop characteristic equation
%
% (s^2 + 2*z1*w1*s + w1^2)*(s^2 + 2*z1*w1*s + w1^2)=0
%

% Closed loop specifications
w1 = 10;
z1 = 0.7;
w2 = 5;
z2 = 0.7;
s = tf('s');
pzmap((s^2 + 2*z1*w1*s + w1^2)*(s^2 + 2*z2*w2*s + w2^2))

% Controller synthesis
lphi       = +((alpha*beta - gamma^2)/delta)*w1^2*w2^2;
lphidot    = +2*((alpha*beta - gamma^2)/delta)*w1*w2*(w1*z2 + w2*z1);
ltheta     = -(alpha*delta)/gamma...
             +((alpha*beta-gamma^2)/gamma)...
             *(-(beta/delta)*w1^2*w2^2 + w1^2 + w2^2 + 4*w1*w2*z1*z2);
lthetadot  = +2*((alpha*beta - gamma^2)/gamma)...
               *(-(beta/delta)*w1^2*w2*z2...
                 -(beta/delta)*w1*w2^2*z1...
                 + w1*z1 + w2*z2);
L = [lphi, ltheta, lphidot, lthetadot];