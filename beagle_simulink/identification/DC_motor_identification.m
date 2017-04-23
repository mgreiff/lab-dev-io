load('responsedata1.mat')
Y = [voltage(3:end-1), voltage(2:end-2), voltage(1:end-3), ...
     -theta(3:end-1), -theta(2:end-2), -theta(1:end-3)];
est = (Y'*Y)\(Y'*theta(4:end));
sys = tf(est(1:3)', [1;est(4:6)]', 0.001);
pzmap(sys)