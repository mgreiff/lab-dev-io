%% Parameters set heuristically according to zeiger nichols method
A = [0, 1, 0; 0, -b/J, K/J; 0, -K/L, -R/L];
B = [0; 0; 1/L];
C = eye(3);

Ae = [A, zeros(3,2);
      -1, 0, 0, 0, 0;
      0, -1, 0, 0, 0];
Be = [B; 0; 0];

%% Design parameters
Q = eye(size(Ae));    % dim(Q) = (n. of states, n. of states)
Q(1,1) = 1000;
Q(2,2) = 10;
Q(4,4) = 100;
Q(5,5) = 10;
R = eye(size(B, 2));  % dim(R) = (n. of c. signals, n. of c. signals)

%% Compute LQR gain
[LQR_K, ~, ~] = lqr(Ae,Be,Q,R);