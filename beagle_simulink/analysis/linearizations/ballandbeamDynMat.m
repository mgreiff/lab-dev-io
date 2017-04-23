function [Ac,Bc,Gc] = ballandbeamDynMat(M,m,Ja,L,g,r,rdot,alpha,alphadot,taualpha,fr)
%BALLANDBEAMDYNMAT
%    [AC,BC,GC] = BALLANDBEAMDYNMAT(M,M,JA,L,G,R,RDOT,ALPHA,ALPHADOT,TAUALPHA,FR)

%    This function was generated by the Symbolic Math Toolbox version 7.0.
%    23-Apr-2017 21:35:47

t2 = r.^2;
t3 = m.*t2;
t4 = Ja+t3;
t5 = 1.0./t4;
Ac = reshape([0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0,0.0,-m.*r.*rdot.*t5,r.*(5.0./7.0),0.0,1.0,-alphadot.*m.*r.*t5,0.0],[4,4]);
if nargout > 1
    Bc = reshape([0.0,0.0,t5,0.0,0.0,0.0,0.0,5.0./7.0],[4,2]);
end
if nargout > 2
    Gc = [0.0;0.0;0.0;g.*(-9.983341664682815e-2)];
end
