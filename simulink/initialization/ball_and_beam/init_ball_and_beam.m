%% Furuta pendulum parameters
Ja = 0.04;     % [kg\cdot m^2]
L  = 1.0;      % [m]
M  = 0.02025;  % [kg]
m  = 0.11;     % [kg]
g  = 9.81;     % [m/s^2]


%% Initial conditions
alpha0 = 0;   % [rad]
r0     = 0;   % [m]
dalpha0 = 0;  % [rad/s]
dr0 = 0;      % [m/s]

q0  = [alpha0;   r0];
dq0 = [dalpha0; dr0];
x0   = [q0; dq0];