
from re import L
from prolog_structures import Rule, RuleBody, Term, Function, Variable, Atom, Number
from typing import List
from functools import reduce

import sys
import random
from final import Interpreter, Not_unifiable

#class Not_unifiable(Exception):
	#pass
fresh_counter = 0
def variables_of_term (t : Term) -> set :
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

def test_variables_of_term ():
    t = Function("f", [Variable("X"), Variable("Y"), Atom("a")])
    assert (variables_of_term (t) == set([Variable("X"), Variable("Y")]))
    #print((variables_of_term (t)) )
    #print((set([Variable("X"), Variable("Y")])))



def variables_of_clause (c : Rule) -> set :
    cl=set()
    c1=c.head.terms
    c2=c.body.terms
    for i in c1:
        if isinstance(i, Variable):
            cl.add(i)
        else: 
            pass
    for i in c2:
        for j in i.terms:
            if isinstance(j, Variable):
                cl.add(j)
            else: 
                pass
    return(cl)

def substitute_in_term ( s : dict, t : Term) -> Term:
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
                    i=substitute_in_term(s, i)
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
            #print(t)
            for v in s:
                if str(v)==str(t):
                    t=s[v]
                    break
            res=t
            #rint(t)
        else:
            res=t
        return(res)
'''

def substitute_in_clause (s : dict, c : Rule) -> Rule:
    if not c:
        return c
    if not s:
        return c
    else: 
        c1=c.head.terms
        c2=c.body.terms
        rule=[]
        rule2=[]
        #print(c)
        if isinstance(c1, Function):
            for i in c1:
                #print(i)
                for v in s:
                    if str(v)==str(i):
                        i=s[v]
                        break
                    else: 
                        pass
                #print(i)
                rule.append(i)
            res=Rule(c.head, rule)
            print("res", res)

        else:
            for i in c1:
                if isinstance(i, Variable):
                    for v in s:
                        if str(v)==str(i):
                            i=s[v]
                            break
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
                    for v in s:
                        if str(v)==str(i):
                            i=s[v]
                            break
                        else:
                            pass
                else:
                    pass
                rule2.append(i)
            #print('12122121',c.head.terms)
            #print('12121212',rule)
            c.head.terms=rule
            c.body.terms=rule2
            return c

        #return(res)

'''
def substitute_in_clause (s : dict, c : Rule) -> Rule:
    if not c:
        return c
    if not s:
        return c
    else: 
        c1=c.head.terms
        c2=c.body.terms
        rule=[]
        rule2=[]
    #print(c)
        if isinstance(c1, Function):
            for i in c1:
            #print(i)
                for v in s:
                    if str(v)==str(i):
                        i=s[v]
                        break
                    else: 
                        pass
            #print(i)
                rule.append(i)
            #res=Rule(c.head, rule)

        else:
            for i in c1:
                if isinstance(i, Variable):
                    for v in s:
                        if str(v)==str(i):
                            i=s[v]
                            break
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
                    for v in s:
                        if str(v)==str(i):
                            i=s[v]
                            break
                        else:
                            pass
                else:
                    pass
                rule2.append(i)
        #print('12122121',c.head.terms)
        #print('12121212',rule)
            c.head.terms=rule
            c.body.terms=rule2
            return c

        #return t
'''
def unify ( t1: Term, t2: Term) -> dict:
    s={}
    brk=0
    global unini
    t1=substitute_in_term (s, t1)
    t2=substitute_in_term(s, t2)

#else: 
    if isinstance(t1, Variable):
        if t1!=t2:
            s[t1]=t2
    
    if isinstance(t2, Variable):
        #print("here",unini)
        try: 
            if unini!=0:
                if t1!=t2:
                    s[t2]=t1
        except: 
            if not isinstance(t1, Variable):
                s[t2]=t1
            else: 
                pass

    elif isinstance (t1, Function) and isinstance(t2, Function) and len(t1.terms)==len(t2.terms):
        ta=t1.terms
        unini=len(ta)
        tb=t2.terms
        lst=list(zip(ta, tb))
        i1=0; j1=0
    #print(s)
    #print(lst)
    #print((reduce((lambda a,b: unify(a,b)), lst, s)))
        for i in lst:
            a=i[0]
            b=i[1]
            s.update(unify(a, b))
            

        if len(s)!= 1:
            alt=0
            altt=False
            #while alt!= len(s)-1: 
            for i in s:
                i1=i1+1
                for j in s:
                    j1=j1+1
                    if i==j and s[i]!=s[j]:
                        if i1<j1:
                            s[i]=s[j]
                            altt=True
                        else: 
                            s[j]=s[i]
                            altt=True
                    
                    j1=0
                    #if altt!= True:
                    #    alt=alt+1

        if s=={}:
            brk=1
    else: 
        if t1==t2:
            pass
        else: 
            try: 
                if unini!=0:
                    pass
                else:
                    brk=1
            except: 
                brk=1

    if brk!=1:
        di=0
        for i in s:
            if i==s[i]:
                s.pop(i)
                break
        for i in s:
            for j in s:
                if i==s[j] and j==s[i]:
                    s.pop(j)
                    di=1
                    break
            if di==1: 
                break
        return s
    else: 
        raise Not_unifiable

    #if isinstance(i, Variable):
'''
def unify (t1: Term, t2: Term) -> dict:
    brk=0
    s={}
    brk, s = un_helper(brk, t1, t2, s)
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

def un_helper(brk, t1, t2, s):
        #s={}
    er=0

    t1=substitute_in_term(s, t1)
    t2=substitute_in_term(s, t2)
#else: 
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
        print("here")
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
                j0=0
        return brk, s
    elif isinstance (t1, Function) and isinstance(t2, Function) and len(t1.terms)==len(t2.terms):
        ta=t1.terms
        tb=t2.terms
        lst=list(zip(ta, tb))
        for (i,j) in lst:
            brk, s =un_helper(brk,i,j,s)
            i0=0
            j0=0      
            for i in s:
                i0=i0+1
                for j in s:
                    j0=j0+1
                    if j==s[i] and j0>i0:
                        s[i]=s[j]
                j0=0
            if er==1 and s=={}:
                brk=brk+1
            else: 
                return brk, s
    else: 
        if t1==t2:
            return brk, s
        else: 

            brk=brk+1
            print(brk)
            return brk, s


#==============================
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
    def substitute_in_clause (self, s : dict, c : Rule) -> Rule:
        if not c:
            return c
        if not s:
            return c
        else: 
            c1=c.head.terms
            c2=c.body.terms
            rule=[]
            rule2=[]
        #print(c)
            if isinstance(c1, Function):
                for i in c1:
                #print(i)
                    if isinstance(i,Function):
                        i=self.substitute_in_clause(s, i)
                    for v in s:
                        if str(v)==str(i):
                            i=s[v]
                            break
                        else: 
                            pass
                #print(i)
                    rule.append(i)
                #res=Rule(c.head, rule)

            else:
                for i in c1:
                    if isinstance(i, Variable):
                        for v in s:
                            if str(v)==str(i):
                                i=s[v]
                                break
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
                        for v in s:
                            if str(v)==str(i):
                                i=s[v]
                                break
                            else:
                                pass
                    else:
                        pass
                    rule2.append(i)
            #print('12122121',c.head.terms)
            #print('12121212',rule)
                c.head.terms=rule
                c.body.terms=rule2
                return c
        


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

fresh_counter = 0
def fresh(fresh_counter) -> Variable:
    fresh_counter += 1
    return Variable("_G" + str(fresh_counter))
def freshen(c: Rule) -> Rule:
    c_vars = variables_of_clause(c)
    theta = {}
    for c_var in c_vars:
        theta[c_var] = fresh(0)

    return substitute_in_clause(theta, c)

def nondet_query (program : List[Rule], pgoal : List[Term]) -> List[Term]:
    cur=pgoal[:]
    c=non(program, pgoal, cur, {}, 0)
    for i in c:
        if isinstance(i, Function):
            if "G_" in i.terms:
                print("here")
        else:
            print("nope")
    return c
def rand(x):
    b=len(x)-1
    return random.randint(0, b)

def non(program, pgoal, cur, s, cn):
    for i in cur:
        print("resol", i)

    #for i in pgoal:
        #print ('pgoals', i)

    ran_pro=[]
    c=True
    if not cur:
        return []
    while cur: 
        rand_r=rand(cur)
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
        for jz in ran_pro:
            print("possible", jz)
        if not ran_pro:
            print("no ran_pro")
        rand_p=rand(ran_pro)
        if ran_pro==[]:
            return pgoal
        prog=ran_pro[rand_p]
        if isinstance(prog, Function):
            p=prog
            p2=()
            print("func")
        elif isinstance(prog, RuleBody):
            p=prog
            p2=()
            print("rb")
        else: 
            p=prog.head.terms
            print(prog.head)
            p2=prog.body
            print("normal", p2)
        if isinstance(goal, RuleBody):
            g=goal.terms[0]
            g=g.terms
        else:
            g=goal.terms
        #new_code
        '''
        ref=0
        ref2=0
        le=0
        le2=0
        id=[]
        id2=[]
        for i in p:
            for j in p:
                if i==j and ref!=ref2: 
                    for gl in pgoal:
                        print("length", len(pgoal))
                        for glt in gl.terms:
                            if le==len(gl.terms):
                                break
                            if glt==i:
                                if glt!=gl.terms[ref]:
                                    glt=gl.terms[ref]
                                elif glt!=gl.terms[ref2]:
                                    glt=gl.terms[ref2]
                            le=le+1
                            print(gl,"..")
                            id.append(glt)
                        c=Function(gl.relation, id)
                        le2=le2+1
                        if le2==len(pgoal):
                            break
                    id2.append(c)
                print("changed")
                    #pgoal=id
                ref2+=1
            ref+=1
            ref2=0
        '''
        lst=list(zip(g, p))
        '''
        le=0
        le2=0
        for i in id2:
            for j in id2:
                if i==j:
                    if le2>le:
                        id2.remove(j)
                    elif le2<le:
                        id2.remove(i)
                le2=le2+1
            le=le+1
            le2=0
        if id2!=[]:
            pgoal=id2
        for i in pgoal:
            print(i,"?")
        '''
        #new_code
        '''
        ref=0
        ref2=0
        for (a,b) in lst:
            for (c,d) in lst:
                if b==d and ref!=ref2 and a!=c:
                    if b!=a and c==d:
                        lst[ref2]=(a,b)
                    elif c!=d and a==b:
                        lst[ref]=(c,d)
                ref2+=1
            ref2=0
            ref+=1
        '''
        for (a,b) in lst:
            
            un_helper(cn, a,b, s)
            cn, s=un_helper(cn, a,b, s)
        print("\n","starts","\n","\n")
        for h in s:
            print("key:", h, "val:", s[h])
        cur.remove(goal)
        #print(str(p2))
        if str(p2) != '()':
            cur.append(p2)
        new_goal=[]
        new_cur=[]
        for i in pgoal:
            #print("i", i)
            check=0
            dig=0
            newl=[]
            '''
            if isinstance(i, Function):
                print("ow")
                for j in i.terms:
                    dig=dig+1
                    if isinstance(j, Function):
                        check=1
                if dig!=0 and check==1:
                    for j in i.terms: 
                        nj=(substitute_in_term(s, j))
                        newl.append(nj)
                    z=Function(i.relation, newl)
                    new_goal.append(z)
            else: 
            '''
            #print(i)
            z=substitute_in_term(s, i)
            #print(z)
            new_goal.append(z)

        if cur:
            for i in cur:
                #print("\n","curi", i)
                z=substitute_in_term(s, i)
                new_cur.append(z)
        #for i in new_cur:
            #print("\n","new_resol", i, "\n")
        #print("ends here")
        if new_cur==[]:
            return new_goal
        else: 
            #print("--------------")
            #for i in new_goal:
                #print("newg", i, "\n")
            
            #for i in new_cur:
                #print("new_resol", i, "\n")
            #for h in s:
                #print("s", h, "v", s[h])
            c=non(program, new_goal, new_cur, s, cn)
            #print("----------------")
            return c



'''
def det_query (program : List[Rule], pgoal : List[Term]) -> List[List[Term]]:
    resol=pgoal[:]
    res={}
    count=5
    last=[]
    det=False
    while count>=0:
        det=False
        c=non(program, pgoal, resol, res, 0)
        if c not in last:
            if c!=[]:
                for i in c:
                    print("im here", i)
                    for j in pgoal:
                        if i==j:
                            print("what")
                            det=True
                            break
                    if det==True:
                        break
                if det!=True:
                    last.append(c)
                    count=count+1
            else: 
                count=count-1
        else: 
            count=count-1
    for i in last:
        for j in i:
            print("res:", j)
    return last


def det(program, pgoal, resol, s, brk):
    cur_rul=[]
    while resol!=[]:
        rand_r=rand(resol)
        cur_goal=resol[rand_r]
        for i in program:
            j=i.head
            if isinstance(cur_goal, RuleBody):
                l=cur_goal.terms
                for t in l:
                    if t.relation==j.relation: 
                        cur_rul.append(i)
            else:
                if j.relation==cur_goal.relation: 
                    cur_rul.append(i)
        rand_p=rand(cur_rul)
        if cur_rul==[]:
            return pgoal
        rul=cur_rul[rand_p]
        if isinstance(rul, Function):
            p=rul
            p2=()
        elif isinstance(rul, RuleBody):
            p=rul.terms
            p2=()
        else:
            p=rul.head
            p2=rul.body.terms
        if isinstance(cur_goal, RuleBody):
            g=cur_goal.terms[0]
        else:
            g=cur_goal
        lst=list(zip(g,p))
        for (a,b) in lst:
            un_helper(0, a, b, s)
            cn, s= un_helper(0, a, b, s)
        resol.remove(cur_goal)
        if str(p2) !="()":
            resol.append(p2)
        new_goal=[]
        new_resol=[]
        for i in pgoal:
            z=substitute_in_term(s, i)
            new_goal.append(z)
        if resol:
            for i in resol:
                z=substitute_in_term(s, i)
                new_resol.append(z)
        if new_resol==[]:
            return new_goal
        else: 
            return det(program, new_goal, new_resol, s, brk)

'''

def dfs(resolvent, goal, solutions,program):
    '''
    print("----------")
    for i in solutions:
        for j in i: 
            print(j)
    if not solutions:
        print("what")
    print("res",resolvent)
    print("goal", goal)
    print("----------")
    '''
    #for i in solutions:
        #for j in i: 
            #print(j)
    if not resolvent:
        solutions.append(goal)
        #for i in solutions:
            #for j in i: 
                #print(j)
        return True
    while resolvent:
        chosen_goal=resolvent.pop(0)
        #resolvent.remove(chosen_goal)
        searched=False
        for rule in program:
            if (rule.head).relation==chosen_goal.relation:
                rule=freshen(rule)
                #print(chosen_goal)
                #print(rule.head)
                c,s=un_helper(0,chosen_goal, rule.head,{})
                new_resolvent, new_goal=resolvent[:], goal[:]
                for i in rule.body.terms:
                    new_resolvent.append(i)
                #for i in s:
                    #print("key", i, "val", s[i])
                resol=[]
                
                for j in new_resolvent:
                    #print(j)
                    j=substitute_in_term(s, j)
                    resol.append(j)
                new_resolvent=resol

                ng=[]
                for z in new_goal:
                    z=substitute_in_term(s, z)
                    ng.append(z)
                new_goal=ng
                
                res=dfs(new_resolvent, new_goal, solutions,program)
                searched=res or searched
                print(searched)

    if not searched: 
        return

    #if not searched:
        #print('zz')
        #return solutions

    


def det_query (program : List[Rule], pgoal : List[Term]) -> List[List[Term]]:
    #returned=dfs([], pgoal, [], program)
    #print("well")
    #for i in returned:
        #for j in i:
            #print(j)
    solutions=[]
    reslo=pgoal[:]
    dfs(reslo, pgoal, solutions, program)
    print("what")
    z,c=dfs(reslo, pgoal, solutions, program)
    #if not c:
        #print("what")
    for i in c:
        for j in i:
            print("res",j)






def test (program : List[Rule], pgoal : List[Term]):
    for i in pgoal:
        for j in program:
            j=j.head
            if j.relation == i.relation: 
                print(i.relation)
                print(i.terms)
                print(j.terms)
            #else: 
                #print("nope")

def list2str(l):
    return ('(' + (',' + ' ').join(
        list(map(str, l))) + ')')
    
def test_final_4_2():
    psimple = [Rule(Function ("f", [Atom("a"), Atom("b")]), RuleBody ([]))]
    g = [Function ("f", [Variable("X"), Atom("b")])]
    print (f"Goal: {list2str(g)}")
    g_ = nondet_query (psimple, g)
    assert (g_ == [Function ("f", [Atom("a"), Atom("b")])])

def test_final_4_3():
    psimple = [Rule(Function ("f", [Atom("a"), Atom("b")]), RuleBody ([]))]
    g = [Function ("f", [Variable ("X"), Variable("Y")])]
    print (f"Goal: {list2str(g)}")
    g_ = nondet_query (psimple, g)
    assert (g_ == [Function ("f", [Atom("a"), Atom("b")])])
    print (f"Solution: {list2str(g_)}")

def test_final_3_1 ():
    t = Variable ("X")
    t_ = Variable ("Y")
    u = {Variable ("Y"): Variable ("X")}
    u_ = {Variable ("X"): Variable ("Y")}
    assert (unify (t, t_) == u or unify (t, t_) == u_)

def test_final_3_2 ():
    t = Variable ("Y")
    t_ = Variable ("X")
    u = {Variable ("X"): Variable ("Y")}
    u_ = {Variable ("Y"): Variable ("X")}
    assert (unify (t, t_) == u or unify (t, t_) == u_)

def test_final_3_3 ():
    t = Variable ("Y")
    t_ = Variable ("Y")
    assert (unify (t, t_) == {})

def test_final_3_4 ():
    t = Number("0")
    t_ = Number("0")
    assert (unify (t, t_) == {})

def test_final_3_5 ():
    t = Number ("0")
    t_ = Variable ("Y")
    u = {Variable ("Y"): Number("0")}
    assert (unify (t, t_) == u)

def test_final_3_6 ():
    t = Number("0")
    t_ = Number("1")
    try:
        unify (t, t_)
        assert False
    except Not_unifiable:
        assert True

def test_final_3_7 ():
    t = Function ("f", [Number("0")])
    t_ = Function ("g", [Number("1")])
    try:
        unify (t, t_)
        assert False
    except Not_unifiable:
        assert True

def test_final_3_8 ():
    u = {(Variable ("X")): (Variable ("Y"))}
    u_ = {(Variable ("Y")): (Variable ("X"))}
    t = Function ("f", [Variable ("X")])
    t_ = Function ("f", [Variable ("Y")])
    assert (unify (t, t_) == u or unify (t, t_) == u_)

def test_final_3_9 ():
    t1 = Function ("f", [Variable ("X"), Variable ("Y"), Variable ("Y")])
    t2 = Function ("f", [Variable ("Y"), Variable ("Z"), Atom ("a")])
    u = { Variable("X"): Atom("a"), Variable("Y"): Atom("a"), Variable("Z"): Atom("a") }
    assert (unify (t1, t2) == u)

    
psimple = [Rule(Function ("f", [Atom("a"), Atom("b")]), RuleBody ([]))]
def ancestor (x, y): return Function ("ancestor", [x, y])
def father (x, y): return Function ("father", [x, y])
def father_consts (x, y):  return father (Atom (x), Atom (y))
f1 = Rule (father_consts ("rickard", "ned"), RuleBody([]))
f2 = Rule (father_consts ("ned", "robb"), RuleBody([]))
r1 = Rule (ancestor (Variable ("X"), Variable ("Y")), RuleBody([father (Variable ("X"), Variable ("Y"))]))
r2 = Rule (ancestor (Variable ("X"), Variable ("Y")), \
                RuleBody([father (Variable ("X"), Variable ("Z")), ancestor (Variable ("Z"), Variable ("Y"))]))
pstark = [f1,f2,r1,r2]

def test_final_4_4():
    print (f"\nProgram: {list2str(pstark)}")
    g = [ancestor (Atom("rickard"), Atom("ned"))]
    print (f"Goal: {list2str(g)}")
    g_ = nondet_query (pstark, g)
    print (f"Solution: {list2str(g_)}")
    assert (g_ == [ancestor (Atom("rickard"), Atom("ned"))])

def test_final_4_5():
    g = [ancestor (Atom("rickard"), Atom("robb"))]
    print (f"Goal: {list2str(g)}")
    g_ = nondet_query (pstark, g)
    print (f"Solution: {list2str(g_)}")
    assert (g_ == [ancestor (Atom("rickard"), Atom("robb"))])

def test_final_4_6 ():
    g = [ancestor (Variable("X"), Atom("robb"))]
    print (f"Goal: {list2str(g)}")
    nondet_query (pstark, g)
    g_ = nondet_query (pstark, g)
    print (f"Solution: {list2str(g_)}")
    #assert (g_ == [ancestor (Atom("ned"), Atom("robb"))] or
                    #g_ == [ancestor (Atom("rickard"), Atom("robb"))])

def test_final_2_4 ():
    s = { Variable(("Y")): Number("0"), Variable("X"): Variable(("Y")) }
    p = Function ("p", [Variable("X"), Variable(("Y")), Atom(("a"))])
    q = Function ("q", [Atom(("a")), Atom(("b")), Atom(("a"))])
    p_ = Function ("p", [Variable(("Y")), Number("0"), Atom(("a"))])
    q_ = Function ("q", [Atom(("a")), Atom(("b")), Atom(("a"))])
    r = Rule (p, RuleBody([q]))
    r_ = Rule (p_, RuleBody([q_]))
    print(substitute_in_clause(s, r))
    assert (substitute_in_clause(s, r) == r_)


nil = Atom("nil")
def cons (h, t): return Function ("cons", [h, t])
def append (x, y, z): return Function ("append", [x, y, z])
c1 = Rule (append (nil, Variable("Q"), Variable("Q")), RuleBody([]))
c2 = Rule (append ((cons (Variable("H"), Variable("P"))), Variable("Q"), (cons (Variable("H"), Variable("R")))), \
                RuleBody([append (Variable("P"), Variable("Q"), Variable("R"))]))
pappend = [c1, c2]
def test_final_4_7():
    print (f"\nProgram: {list2str(pappend)}")
    g = [append (Variable("X"), Variable("Y"), \
            (cons (Number("1"), (cons (Number("2"), (cons (Number("3"), nil)))))))]
    print (f"Goal: {list2str(g)}")
    g_ = Inte.nondet_query (pappend, g)
    print (f"Solution: {list2str(g_)}")
    assert (
    g_ == [append (nil, (cons (Number("1"), (cons (Number("2"), (cons (Number("3"), nil)))))), \
                            (cons (Number("1"), (cons (Number("2"), (cons (Number("3"), nil)))))))] or
    g_ == [append ((cons (Number("1"), nil)), (cons (Number("2"), (cons (Number("3"), nil)))), \
                            (cons (Number("1"), (cons (Number("2"), (cons (Number("3"), nil)))))))] or
    g_ == [append ((cons (Number("1"), (cons (Number("2"), nil)))), (cons (Number("3"), nil)), \
                            (cons (Number("1"), (cons (Number("2"), (cons (Number("3"), nil)))))))] or
    g_ == [append ((cons (Number("1"), (cons (Number("2"), (cons (Number("3"), nil)))))), nil, \
                            (cons (Number("1"), (cons (Number("2"), (cons (Number("3"), nil)))))))] )



def test_challenge_1():
    print ("\n\n###################################################")
    print ("###### Testing the deterministic interpreter ######")
    print ("###################################################")
    print (f"Program: {list2str(psimple)}")
    # Tests query failure
    g = [Function ("f", [Atom ("a"), Atom ("c")])]
    print (f"Goal: {list2str(g)}")
    print("we have:",det_query (psimple, g))
    assert (det_query (psimple, g) == [])
    

# Test on the Stark House program
def test_challenge_2():
    print (f"\nProgram:{list2str(pstark)}")
    # Tests backtracking
    g = [ancestor (Atom("rickard"), Atom("robb"))]
    print (f"Goal: {list2str(g)}")
    g_ = det_query (pstark, g)
    assert (len(g_) == 1)
    g_ = g_[0]
    print (f"Solution: {list2str(g_)}")
    assert (g_ == g)


def test_challenge_3():
    # Tests choice points
    g = [ancestor (Variable("X"), Atom("robb"))]
    print (f"Goal: {list2str(g)}")
    g_ = det_query (pstark, g)
    assert (len(g_) == 2)
    g1, g2 = g_[0], g_[1]
    print (f"Solution: {list2str(g1)}")
    print (f"Solution: {list2str(g2)}")
    assert (g1 == [ancestor (Atom("ned"), Atom("robb"))])
    assert (g2 == [ancestor (Atom("rickard"), Atom("robb"))])

# Test on the list append program
def test_challenge_4():
    print (f"\nProgram: {list2str(pappend)}")
    # Tests choice points
    g = [append (Variable("X"), (Variable("Y")), (cons (Number("1"), (cons (Number("2"), (cons (Number("3"), nil)))))))]
    print (f"Goal: {list2str(g)}")
    g_ = det_query (pappend, g)
    assert (len(g_) == 4)
    for sg in g_:
        print (f"Solution: {list2str(sg)}")
        
if __name__ == '__main__':
    #h = Function ("p", [Variable ("X"), Variable ("Y"), Atom ("a")])
    #b = [Function ("q", [Atom ("a"), Atom ("b"), Atom ("a")]), Function("f", [Variable("Z")])]
    #r2 = Rule (h, RuleBody(b))
    #print(variables_of_clause(r2))
    s = { Variable(("Y")): Number(0), Variable("X"): Variable(("Y")) }
    #t = Function ("f", [Variable ("X"), Variable ("Y"), Atom ("a")])
    t=Variable ("X")
    #t_= Function ("f", [Variable ("Y"), Number("0"), Atom ("a")])
    #print(s)
    #print(t)
    #substitute_in_term (s, t)

    #test_variables_of_term ()

    #2-2
    #s = { Variable(("Y")): Number(0), Variable("X"): Variable(("Y")) }
    #print("s", s)
    #s2={ Variable(("Y")): Number(0), Variable("X"): Variable(("Y")) }
    #q = Function ("q", [Atom(("a")), Atom(("b")), Atom(("a"))])
    #r = Rule ((Function ("p", [Variable ("X"), Variable ("Y"), Atom ("a")])), RuleBody([q]))
    #print("r", r)
    #r_ = Rule ((Function ("p", [Variable ("Y"), Number("0"), Atom ("a")])), RuleBody([]))
	#s = { Variable(("Y")): Number(0), Variable("X"): Variable(("Y")) }
	#r = Rule ((Function ("p", [Variable ("X"), Variable ("Y"), Atom ("a")])), RuleBody([]))
	#r_ = Rule ((Function ("p", [Variable ("Y"), Number("0"), Atom ("a")])), RuleBody([]))
	#assert (substitute_in_clause (s, r) == r_)

    #3
    '''
    t = Variable ("X")
    t_ = Variable ("Y")
    u = {Variable ("Y"): Variable ("X")}
    u_ = {Variable ("X"): Variable ("Y")}
    '''
   # c=(unify (t, t_))
    #assert (unify (t, t_) == u)
    #print(unify (t, t_, {}))
    #assert (unify (t, t_) == u or unify (t, t_) == u_)
    

    '''
    t = Number ("0")
    t_ = Variable ("Y")
    u = {Variable ("Y"): Number("0")}
    print(unify (t, t_, {}))
    '''
    #assert (unify (t, t_, s) == u)

    #t = Function ("f", [Variable ("X")])
    #t_ = Function ("f", [Variable ("Y")])
    #u = {(Variable ("X")): (Variable ("Y"))}
    #unify(t, t_)
    
    #assert (unify (t, t_) == u)
    '''
    u = {(Variable ("X")): (Variable ("Y"))}
    u_ = {(Variable ("Y")): (Variable ("X"))}
    t = Function ("f", [Variable ("X")])
    t_ = Function ("f", [Variable ("Y")])

    c=unify (t, t_, {})
    for i in c:
        print("i", i, "c", c[i])

    #assert (unify (t, t_) == u or unify (t, t_) == u_)
    
    t1 = Function ("f", [Variable ("X"), Variable ("Y"), Variable ("Y")])
    t2 = Function ("f", [Variable ("Y"), Variable ("Z"), Atom ("a")])
    u = { Variable("X"): Atom("a"), Variable("Y"): Atom("a"), Variable("Z"): Atom("a") }
    c=unify (t1, t2)
    for i in c:
        print("i", i, "c", c[i])
    assert (unify (t1, t2) == u)
    t = Number ("0")
    t_ = Variable ("Y")
    u = {Variable ("Y"): Number("0")}
    c=(unify (t, t_))
    for i in c:
        print("i", i, "c", c[i])
    assert (unify (t, t_) == u)



    test_final_3_1 ()
    test_final_3_2 ()
    test_final_3_3 ()
    test_final_3_4 ()
    test_final_3_5 ()
    print('here')

    print('here')
    t1 = Function ("f", [Variable ("P"), Variable ("P"), Variable ("Q"), ])
    t2 = Function ("f", [Variable ("Q"), Variable ("R"), Atom ("a")])
    c=unify (t1, t2,{})
    for i in c:
        print("i", i, "c", c[i])
    for i in c:
        print("i", i, "c", c[i])

    t = Number("0")
    t_ = Number("1")
    try:
        unify (t, t_)
        assert False
    except Not_unifiable:
        assert True
     
    t1 = Function ("f", [Variable ("X"), Variable ("Y"), Variable ("Y")])
    t2 = Function ("f", [Variable ("Y"), Variable ("Z"), Atom ("a")])
    u = { Variable("X"): Atom("a"), Variable("Y"): Atom("a"), Variable("Z"): Atom("a") }
    c=unify (t1, t2)
    for i in c:
        print("i", i, "c", c[i])
    '''
    #test_final_4_2()
    #test_final_4_3()
    #test_final_4_4()
    #test_final_4_5()
    #test_final_4_6()
    
    #g_ = [append (nil, (cons (Number("1"), (cons (Number("2"), (cons (Number("3"), nil)))))), 
    #                        (cons (Number("1"), (cons (Number("2"), (cons (Number("3"), nil)))))))]
    #print("expected", list2str(g_))
    #g_ = [append ((cons (Number("1"), nil)), (cons (Number("2"), (cons (Number("3"), nil)))), 
    #                        (cons (Number("1"), (cons (Number("2"), (cons (Number("3"), nil)))))))]
    #print("expected", list2str(g_))
    #g_ = [append ((cons (Number("1"), (cons (Number("2"), nil)))), (cons (Number("3"), nil)), 
    #                        (cons (Number("1"), (cons (Number("2"), (cons (Number("3"), nil)))))))]
    #print("expected", list2str(g_))
    #g_ = [append ((cons (Number("1"), (cons (Number("2"), (cons (Number("3"), nil)))))), nil, 
    #                        (cons (Number("1"), (cons (Number("2"), (cons (Number("3"), nil)))))))] 
    #print("expected", list2str(g_))
    test_final_4_7()
    #test_final_2_4()
    #psimple = [Rule(Function ("f", [Atom("a"), Atom("b")]), RuleBody ([]))]
    #g = [Function ("f", [Variable("X"), Atom("b")])]
    #c=(nondet_query(psimple, g))
    #print(c)


    #test_challenge_1()
    #test_challenge_2()
    #g = [ancestor (Variable("X"), Atom("robb"))]
    #print (f"Goal: {list2str(g)}")
    #det_query (pstark, g)

    #print (f"\nProgram: {list2str(pappend)}")
    # Tests choice points
    #g = [append (Variable("X"), (Variable("Y")), (cons (Number("1"), (cons (Number("2"), (cons (Number("3"), nil)))))))]
    #print (f"Goal: {list2str(g)}")
    #g_ = det_query (pappend, g)

    #print (f"\nProgram:{list2str(pstark)}")
    # Tests backtracking
    #g = [ancestor (Atom("rickard"), Atom("robb"))]
    #print (f"Goal: {list2str(g)}")
   # g_ = det_query (pstark, g)
	#assert (len(g_) == 2)
	#g1, g2 = g_[0], g_[1]
		#print (f"Solution: {list2str(g1)}")
		#print (f"Solution: {list2str(g2)}")
		#assert (g1 == [ancestor (Atom("ned"), Atom("robb"))])
		#assert (g2 == [ancestor (Atom("rickard"), Atom("robb"))])