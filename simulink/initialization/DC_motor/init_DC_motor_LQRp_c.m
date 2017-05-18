%% Parameters set heuristically according to zeiger nichols method
A = [0, 1, 0; 0, -b/J, K/J; 0, -K/L, -R/L];
B = [0; 0; 1/L];
C = eye(3);

disp(['System rank: ', num2str(size(A,1))])
disp(['Controllability matrix rank: ', num2str(rank(ctrb(A, B)))])

%% Design parameters
Q = eye(size(A));    % dim(Q) = (n. of states, n. of states)
Q(1,1) = 1000;
Q(2,2) = 10;
R = eye(size(B, 2));  % dim(R) = (n. of c. signals, n. of c. signals)

%% Compute LQR gain
[LQR_K, ~, ~] = lqr(A,B,Q,R);

%% Compute precompensation gain
s = size(A,1);
Z = [zeros([1,s]) 1];
Chat = [1,0,0];              % reference given with respect to theta
D = [0];
N = inv([A,B;Chat,0])*Z';
LQR_N = N(1+s) + LQR_K * N(1:s);