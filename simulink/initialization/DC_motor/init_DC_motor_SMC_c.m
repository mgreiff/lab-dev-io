J = 0.01;
b = 0.1;
K = 0.01;
R = 1;
L = 0.5;

A = [0, 1, 0; 0, -b/J, K/J; 0, -K/L, -R/L];
B = [0; 0; 1/L];

Asmc = [0, 1, 0; 0, -b/J, K/J; 0, -K/L, -R/L];
Bsmc = [0; 0; 1/L];
p = [10; 1; 0.5];
mu = 10;