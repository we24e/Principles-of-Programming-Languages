/* prefix(X, Z) :- append(X, Y, Z).
suffix(Y, Z) :- append(X, Y, Z). 
segment([], []).
segment(S, Lst) :- prefix(S, R), suffix(R, Lst). */

prefix(A,B):- append(A,C,B).
suffix(A,B):- append(C,A,B).
segment([],[]).
segment(A,B) :- prefix(A,D),suffix(D,B).





link(san_diego, seattle).
link(seattle, dallas).
link(dallas, new_york).
link(new_york, chicago).
link(new_york, seattle).
link(chicago, boston).
link(boston, san_diego).


path_2([],[]).
path_2(A,B):- link(A,C),link(C,B).

path_N(A,B,1) :- link(A,B).
path_N(A,B,L) :- L>1, Ls is L-1, link(A,C), path_N(C,B,Ls).


 



/*
path_2(X, Y) :- link(X, Z), link(Z, Y). 

path_N(X,Y,1):- link(X,Y). 
path_N(X,Y,N):- N>1, R is N-1, path_N(X,Z,R), link(Z,Y).
*/
