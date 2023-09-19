from prolog_structures import Rule, RuleBody, Term, Function, Variable, Atom, Number
from typing import List
from functools import reduce

import sys
import random

class Not_unifiable(Exception):
	pass

'''
Please read prolog_structures.py for data structures
that represent Prolog terms, rules, and goals.
'''
class Interpreter:
    def __init__(self):
        pass

    '''
	Example
	occurs_check (v, t) where v is of type Variable, t is of type Term.
	occurs_check (v, t) returns true if the Prolog Variable v occurs in t.
	Please see the lecture note Control in Prolog to revisit the concept of
	occurs-check.
	'''
    def occurs_check (self, v : Variable, t : Term) -> bool:
        if isinstance(t, Variable):
            return v == t
        elif isinstance(t, Function):
            for t in t.terms:
                if self.occurs_check(v, t):
                    return True
            return False
        return False


    '''
	Problem 1
	variables_of_term (t) where t is of type Term.
	variables_of_clause (c) where c is of type Rule.

	The function should return the Variables contained in a term or a rule
	using Python set.

	The result must be saved in a Python set. The type of each element (a Prolog Variable)
	in the set is Variable.
	'''
    def variables_of_term (self, t : Term) -> set :
        ta=set()
        terms=t.terms
        for i in terms:
            if isinstance(i, Variable):
                ta.add(i)
            elif isinstance(i, Function): 
                for j in i.terms: 
                    if isinstance(j, Variable):
                        ta.add(j)
            else: 
                pass
        return ta

    def variables_of_clause (self, c : Rule) -> set :
        s1=set()
        s2=set()
        c1=c.head.terms
        c2=c.body.terms
        for i in c1:
            if isinstance(i, Variable):
                s1.add(i)
            else: 
                pass
        for i in c2:
            for j in i.terms:
                if isinstance(j, Variable):
                    s2.add(j)
                elif isinstance(j, Function): 
                    for z in j.terms:
                        if isinstance(z, Variable): 
                            s2.add(z)
                else: 
                    pass
        res=s1.union(s2)
        return(res)


    '''
	Problem 2
	substitute_in_term (s, t) where s is of type dictionary and t is of type Term
	substitute_in_clause (s, t) where s is of type dictionary and c is of type Rule,

	The value of type dict should be a Python dictionary whose keys are of type Variable
	and values are of type Term. It is a map from variables to terms.

	The function should return t_ obtained by applying substitution s to t.

	Please use Python dictionary to represent a subsititution map.
	'''
    def substitute_in_term (self, s : dict, t : Term) -> Term:
        if not t:
            return t
        if not s:
            return t
        else: 
            if isinstance(t, Function):
                terms=[]
                t2=t.terms
                for i in t2:
                    if isinstance(t,Function):
                        i=self.substitute_in_term(s, i)
                    else: 
                        for v in s:
                            if str(v)==str(i):
                                i=s[v]
                                break
                            else: 
                                pass
                    terms.append(i)
                res=Function(t.relation, terms)
            elif isinstance(t, Variable):
                for v in s:
                    if str(v)==str(t):
                        t=s[v]
                        break
                res=t
            else:
                res=t
            return(res)

    
    def substitute_in_clause (self, s : dict, c : Rule) -> Rule:
        if not c:
            return c
        if not s:
            return c
        else: 
            try:
                c1=c.head.terms
            except: 
                pass
            try:
                c2=c.body.terms
            except: 
                pass
            rule=[]
            rule2=[]
            rul=[]
            got_it=0
            got_b=0
        #print(c)
            if isinstance(c.head, Function):
                for i in c1:
                #print(i)
                    if isinstance(i,Function):
                        i=self.substitute_in_clause(s, i)
                    for v in s:
                        if str(v)==str(i):
                            i=s[v]
                        else: 
                            pass
                #print(i)
                    rule.append(i)
                #res=Rule(c.head, rule)
            elif isinstance(c.head, Variable):
                got_it=1
                for v in s:
                    if str(c.head)==str(v):
                            c.head=s[v]

            else:
                for i in c1:
                    if isinstance(i, Variable):
                        for v in s:
                            if str(v)==str(i):
                                i=s[v]
                                break
                            else: 
                                pass
                    if isinstance(i, Function):
                        i=self.substitute_in_clause(s, i)
                        for v in s:
                            if str(v)==str(i):
                                i=s[v]
                            else: 
                                pass
                    rule.append(i)
                #print(i)
            for i in c2:
                if isinstance(i, Variable):
                    for v in s:
                        if str(v)==str(i):
                            i=s[v]
                            break
                        else:
                            pass
                elif isinstance(i, Function):
                    for j in i.terms:
                        if isinstance(j, Function):
                            j=self.substitute_in_clause(s, j)
                        elif isinstance(j, Variable):
                            for v in s:
                                if str(v)==str(j):
                                    j=s[v]
                                    break
                                else:
                                    pass
                        rul.append(j)
                    i=Function(i.relation, rul)
                rule2.append(i)
                            

        #print('12122121',c.head.terms)
        #print('12121212',rule)
            if got_it==1:
                pass
            else:
                c.head.terms=rule
            c.body.terms=rule2
            return c


    '''
	Problem 3
	unify (t1, t2) where t1 is of type term and t2 is of type Term.
	The function should return a substitution map of type dict,
	which is a unifier of the given terms. You may find the pseudocode
	of unify in the lecture note Control in Prolog useful.

	The function should raise the exception raise Not_unfifiable (),
	if the given terms are not unifiable.

	Please use Python dictionary to represent a subsititution map.
	'''

    def unify (self, t1: Term, t2: Term) -> dict:
        brk=0
        s={}
        brk, s = self.un_helper(brk, t1, t2, s)
        i0=0
        j0=0      
        for i in s:
            i0=i0+1
            for j in s:
                j0=j0+1
                if j==s[i] and j0>i0:
                    s[i]=s[j]

        if brk!= 0 and s=={}:
            raise Not_unifiable()
        else:
            return s 

    def un_helper(self, brk, t1, t2, s):
		    #s={}
        er=0
        t1=self.substitute_in_term(s, t1)
        t2=self.substitute_in_term(s, t2) 
        if isinstance(t1, Variable):
            if t1!=t2:
                for v in s:
                    if v==t1:
                        t1=s[v]
                if isinstance(t2, Variable):
                    for v in s:
                        if t2==v:
                            t2=s[v]
                            break

                for i in s:
                    if t1==s[i]:
                        s[i]=t2
                s[t1]=t2
            i0=0
            j0=0      
            for i in s:
                i0=i0+1
                for j in s:
                    j0=j0+1
                    if j==s[i] and j0>i0:
                        s[i]=s[j]
            return brk, s
    
        elif isinstance(t2, Variable):
            if t1!=t2:
                for v in s:
                    if v==t2:
                        t2=s[v]
                        break
                if isinstance(t1, Variable):
                    for v in s:
                        if t1==v:
                            t1=s[v]
                            break
                    for i in s:
                        if t1==s[i]:
                            s[i]=t2
                s[t2]=t1
            i0=0
            j0=0      
            for i in s:
                i0=i0+1
                for j in s:
                    j0=j0+1
                    if j==s[i] and j0>i0:
                        s[i]=s[j]
                s[t2]=t1
            return brk, s
        elif isinstance (t1, Function) and isinstance(t2, Function) and len(t1.terms)==len(t2.terms):
            ta=t1.terms
            tb=t2.terms
            lst=list(zip(ta, tb))
            for (i,j) in lst:
                brk, s=self.un_helper(brk,i,j,s)
                i0=0
                j0=0      
                for i in s:
                    i0=i0+1
                    for j in s:
                        j0=j0+1
                        if j==s[i] and j0>i0:
                            s[i]=s[j]
            if er==1 and s=={}:
                brk=brk+1
            else: 
                return brk, s
        else: 
            if t1==t2:
                return brk, s
            else: 
                brk=brk+1
                return brk, s

    fresh_counter = 0
    def fresh(self) -> Variable:
        self.fresh_counter += 1
        return Variable("_G" + str(self.fresh_counter))
    def freshen(self, c: Rule) -> Rule:
        c_vars = self.variables_of_clause(c)
        theta = {}
        for c_var in c_vars:
            theta[c_var] = self.fresh()

        return self.substitute_in_clause(theta, c)


    '''
	Problem 4
	Following the Abstract interpreter pseudocode in the lecture note Control in Prolog to implement
	a nondeterministic Prolog interpreter.

	nondet_query (program, goal) where
		the first argument is a program which is a list of Rules.
		the second argument is a goal which is a list of Terms.

	The function returns a list of Terms (results), which is an instance of the original goal and is
	a logical consequence of the program. See the tests cases (in src/main.py) as examples.
	'''
    def nondet_query (self, program : List[Rule], pgoal : List[Term]) -> List[Term]:
        cur=pgoal[:]
        c=self.non(program, pgoal, cur, {}, 0)
        for i in c:
            if isinstance(i, Function):
                for j in i.terms:
                    if str(j).startswith("_G"):
                        self.nondet_query(program,pgoal)
            elif str(i).startswith("_G"):
                self.nondet_query(program,pgoal)
            else:
                pass
        return c

    def rand(self,x):
        b=len(x)-1
        return random.randint(0, b)

    def non(self,program, pgoal, cur, s, cn):
        ran_pro=[]
        c=True
        if not cur:
            return []
        while cur: 
            rand_r=self.rand(cur)
            goal=cur[rand_r]
            for i in program:
                j=i.head
                if isinstance(goal, RuleBody):
                    for rl in goal.terms:
                        if rl.relation==j.relation:
                            ran_pro.append(i)
                else: 
                    if j.relation==goal.relation: 
                        ran_pro.append(i)
            #if not ran_pro:
                #return cur
            rand_p=self.rand(ran_pro)
            if ran_pro==[]:
                return pgoal
            prog=ran_pro[rand_p]
            prog=self.freshen(prog)
            if isinstance(prog, Function):
                p=prog.terms
                p2=()
            elif isinstance(prog, RuleBody):
                p=prog.terms
                p2=()
            else: 
                p=prog.head.terms
                p2=prog.body
            if isinstance(goal, RuleBody):
                g=goal.terms[0]
                g=g.terms
            else:
                g=goal.terms
            lst=list(zip(g, p))
            for (a,b) in lst:
                #print(a,b)
                try:
                    self.un_helper(cn, a,b, s)
                    cn, s=self.un_helper(cn, a,b, s)
                except:
                    self.nondet_query(program, pgoal)
            cur.remove(goal)
            if str(p2) != '()':
                cur.append(p2)
            new_goal=[]
            new_cur=[]
            for i in pgoal:
                z=self.substitute_in_term(s, i)
                new_goal.append(z)

            if cur:
                for i in cur:
                    z=self.substitute_in_term(s, i)
                    new_cur.append(z)
            if new_cur==[]:
                return new_goal
            else: 
                c=self.non(program, new_goal, new_cur, s, cn)
                return c



    '''
	Challenge Problem

	det_query (program, goal) where
		the first argument is a program which is a list of Rules.
		the second argument is a goal which is a list of Terms.

	The function returns a list of term lists (results). Each of these results is
	an instance of the original goal and is a logical consequence of the program.
	If the given goal is not a logical consequence of the program, then the result
	is an empty list. See the test cases (in src/main.py) as examples.
	'''
    def dfs(self,resolvent, goal, solutions,program):
        if not resolvent:
            if goal not in solutions: 
                solutions.append(goal)
            return True
        while resolvent:
            chosen_goal=resolvent.pop(0)
            #resolvent.remove(chosen_goal)
            searched=False
            for rule in program:
                if (rule.head).relation==chosen_goal.relation:
                    rule=self.freshen(rule)
                    #print(chosen_goal)
                    #print(rule.head)
                    ch, s=self.un_helper(0,chosen_goal, rule.head,{})
                    new_resolvent, new_goal=resolvent[:], goal[:]
                    for i in rule.body.terms:
                        new_resolvent.append(i)
                    #for i in s:
                        #print("key", i, "val", s[i])
                    resol=[]
                    
                    for j in new_resolvent:
                        #print(j)
                        j=self.substitute_in_term(s, j)
                        resol.append(j)
                    new_resolvent=resol

                    ng=[]
                    for z in new_goal:
                        z=self.substitute_in_term(s, z)
                        ng.append(z)
                    new_goal=ng
                    
                    res=self.dfs(new_resolvent, new_goal, solutions,program)
                    searched=res or searched
                    if res==solutions:
                        print("last")
                        return res
                    
                else:
                    if solutions is None:
                        pass
                    elif solutions==[]:
                        pass
                    else:
                        return solutions
                    

    def det_query (self, program : List[Rule], pgoal : List[Term]) -> List[List[Term]]:
        solutions=[]
        reslo=pgoal[:]
        c=self.dfs(reslo, pgoal, solutions, program)
        if c is None:
            return []
        else: 
            for i in c:
                for j in i:
                    print(j)
            return c[::-1]
