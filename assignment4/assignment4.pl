/* YOUR CODE HERE (Problem 1, delete the following line) */
range(S,E,M) :- M>=S, M=<E.

?- range(1,2,2).
?- not(range(1,2,3)).

/* YOUR CODE HERE (Problem 2, delete the following line) */
reverseL([], []).
reverseL([H|T],RevX) :- reverseL(T, C),append(C,[H],RevX).

?- reverseL([],X).
?- reverseL([1,2,3],X).
?- reverseL([a,b,c],X).

/* YOUR CODE HERE (Problem 3, delete the following line) */
memberL(X,[]):-false.
memberL(X,[H|T]) :- X = H; memberL(X, T).

?- not(memberL(1, [])).
?- memberL(1,[1,2,3]).
?- not(memberL(4,[1,2,3])).
?- memberL(X, [1,2,3]).

/* YOUR CODE HERE (Problem 4, delete the following line) */
zip([], [], []) .
zip([], Ys, []).
zip(Xs, [], []).
zip([H|T], [O|P], [(H-O)|XYs]):- zip(T, P, XYs).


?- zip([1,2],[a,b],Z).
?- zip([a,b,c,d], [1,X,y], Z).
?- zip([a,b,c],[1,X,y,z], Z).
?- length(A,2), length(B,2), zip(A, B, [1-a, 2-b]).

/* YOUR CODE HERE (Problem 5, delete the following line) */
insert(X, [], [X]).
insert(X, [Hy | Ty], [X, Hy|Ty]):- X =< Hy.
insert(X, [Hy | Ty], [Hy|Tz]):- insert(X, Ty, Tz).

?- insert(3, [2,4,5], L).
?- insert(3, [1,2,3], L).
?- not(insert(3, [1,2,4], [1,2,3])).
?- insert(3, L, [2,3,4,5]).
?- insert(9, L, [1,3,6,9]).
?- insert(3, L, [1,3,3,5]).

/* YOUR CODE HERE (Problem 6, delete the following line) */

appd([],X,Y):- reverseL(X, Y).
appd([H|T],T3,T4) :- memberL(H, T3), appd(T,T3,T4); appd(T, [H|T3], T4).
remove_duplicates ([], _).
remove_duplicates([H], [H]).
remove_duplicates(T1, T2) :- appd(T1, [], T2).


?- remove_duplicates([1,2,3,4,2,3],X).
?- remove_duplicates([1,4,5,4,2,7,5,1,3],X).
?- remove_duplicates([], X).

/* YOUR CODE HERE (Problem 7, delete the following line) */
intersectionL([], [], []).
intersectionL(_, [], []).
intersectionL([], _, []).
intersectionL([H|T],L2,[H|L3]) :- memberL(H, L2), intersectionL(T, L2, L3).
intersectionL([H|T],L2,L3):- intersectionL(T, L2, L3).

?- intersectionL([1,2,3,4],[1,3,5,6],[1,3]).
?- intersectionL([1,2,3,4],[1,3,5,6],X).
?- intersectionL([1,2,3],[4,3],[3]).

prefix(P,L) :- append(P,_,L).
suffix(S,L) :- append(_,S,L).

/* YOUR CODE HERE (Problem 8, delete the following line) */
partition([],[],[]).
partition([X],[X],[]).
partition(L,P,S) :- length(L, N), Pl is div(N,2), Sl is (N-(div(N,2))),helper2(L,P,S,Pl,Sl).
helper2(L,P,S,Pl,Sl) :-length(P, Pl), length(S, Sl), prefix(P,L), suffix(S,L).

?- partition([a],[a],[]).
?- partition([1,2,3],[1],[2,3]).
?- partition([a,b,c,d],X,Y).

/* YOUR CODE HERE (Problem 9, delete the following line) */
merge([], X, X).
merge(X, [], X).
merge([],[],[]).
merge([H|T],[H2|T2],Z) :- H<H2, merge(T, [H2 | T2], R), append([H], R, Z); merge([H|T], T2, R), append([H2], R, Z).

?- merge([],[1],[1]).
?- merge([1],[],[1]).
?- merge([1,3,5],[2,4,6],X).

/* YOUR CODE HERE (Problem 10, delete the following line) */
mergesort([],[]).
mergesort([H], [H]).
mergesort([X, Y], [Y,X]) :- X>Y.
mergesort([X, Y], [X,Y]) :- X=<Y.
mergesort(L,SL) :- partition(L,P,S), mergesort(P, PL), mergesort(S, S2), merge(PL, S2, SL).

?- mergesort([3,2,1],X).
?- mergesort([1,2,3],Y).
?- mergesort([],Z).
