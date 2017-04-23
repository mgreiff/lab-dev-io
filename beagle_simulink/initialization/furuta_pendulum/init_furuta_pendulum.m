%% Furuta pendulum parameters
J  = 0.0000972; % [kg\cdot m^2]
M  = 0.02025;   % [kg]
ma = 0.072;     % [kg]
mp = 0.00775;   % [kg]
la = 0.250;     % [m]
lp = 0.4125;    % [m]
g  = 9.81;      % [m/s^2]

alpha = J + (M + (1/3)*ma + mp)*la^2;
beta  = (M + (1/3)*mp)*lp^2;
gamma = (M + (1/2)*mp)*la*lp;
delta = (M + (1/2)*mp)*g*lp;

%% Initial conditions
phi0 = 0;    % [rad]
theta0 = pi;  % [rad]
dphi0 = 0;   % [rad/s]
dtheta0 = 0; % [rad/s]

q0  = [phi0;  theta0];
dq0 = [dphi0; dtheta0];
x0   = [q0; dq0];