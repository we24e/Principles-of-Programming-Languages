
from prolog_structures import Rule, RuleBody, Term, Function, Variable, Atom, Number
from typing import List
from functools import reduce

import sys
import random
import traceback

class Not_unifiable(Exception):
	pass

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
                            print("v",v)
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


    #qsh q3
    def unify (self, t1: Term, t2: Term) -> dict:
        res=self.unify_2(t1, t2, {})
        return res
    
    def deter(self, a, b):
        z1=False
        z2=False
        if isinstance(a, Function):
            if b not in a.terms:
                z1=True
            else:
                pass
        elif a!=b:
            z2=True
        return z1, z2

    def replace(self, unifer):
        for key in unifer:
            for key2 in unifer:
                if key==unifer[key2]:
                    unifer[key2]=unifer[key]
        return unifer
                        

    def unify_2(self, X, Y, unifer):
        X=self.substitute_in_term(unifer,X)
        y=self.substitute_in_term(unifer,Y)
        z1, z2=self.deter(y,X)
        z3, z4=self.deter(X,y)
        if isinstance(X, Variable) and (z1 or z2):
            i=False
            for key in unifer:
                if key==X:
                    i=True
                    unifer[key]=y
                    break
                else:
                    pass
            if i==False:
                unifer[X]=y

            else: 
                pass
            unifer=self.replace(unifer)
            return unifer
        elif isinstance(y, Variable) and (z3 or z4):
            i=False
            for key in unifer:
                if key==y:
                    i=True
                    unifer[key]=X
                else:
                    pass
            if i==False:
                unifer[y]=X
            else:
                pass
            unifer=self.replace(unifer)
            return unifer
        elif X==y:
            return unifer
        elif isinstance(X, Function) and isinstance(y, Function) and len(X.terms) == len(y.terms):
            pre_lst=zip(X.terms, y.terms)
            f_list=list(pre_lst)
            c=reduce((lambda unifer, a: self.unify_2(a[0], a[1], unifer)), f_list, unifer)
            c=self.replace(c)
            return c
        else:
            raise Not_unifiable()
            
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
    '''
    '''
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
    '''

    '''
    def dfs(self,resolvent, goal, solutions,program):
        
        print("----------")
        for i in solutions:
            for j in i: 
                print(j)
        if not solutions:
            print("what")
        print("res",resolvent)
        print("goal", goal)
        print("----------")
        
        #for i in solutions:
            #for j in i: 
                #print(j)
        if not resolvent:
            print(solutions)
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
                    
        if not searched:
            return
        #if d==1:
            #return solutions

    def det_query (self, program : List[Rule], pgoal : List[Term]) -> List[List[Term]]:
        #returned=dfs([], pgoal, [], program)
        #print("well")
        #for i in returned:
            #for j in i:
                #print(j)
        solutions=[]
        reslo=pgoal[:]
        c=self.dfs(reslo, pgoal, solutions, program)
        print(c)
        print("what")
        #c,d=self.dfs(reslo, pgoal, solutions, program)
        #for i in c:
            #for j in i:
                #print(j)
        #for i in c:
            #for j in i:
                #print(j)
        if c is None:
            return []
        else: 
            for i in c:
                for j in i:
                    print(j)
            return c[::-1]
    '''  


    def nondet_query (self, program : List[Rule], pgoal : List[Term]) -> List[Term]:
        cur=pgoal[:]
        c=self.non(program, pgoal, cur, {}, 0)
        for i in c:
            print(i)
            if isinstance(i, Function):
                for j in i.terms:
                    if str(j).startswith("_G"):
                        self.nondet_query(program,pgoal)

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
            for i in s:
                print(i, s[i])
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
    #qsh
    def substitute_in_clause (self, s : dict, c : Rule) -> Rule:
        keys=s.keys()
        head=c.head
        body=c.body
        if isinstance(head,Variable):
            new_h=head
            for i in keys:
                if head==i:
                    new_h=s[i]
                else:
                    pass
            c.head=new_h

        elif isinstance(head,Function):
            new_h=[]
            for h in head.terms:
                if isinstance(h, Function):
                    h=self.substitute_in_term(s, h)
                elif isinstance(h, Variable):
                    for i in keys:
                        if h==i:
                            h=s[i]
                        else: 
                            pass
                else:
                    pass
                new_h.append(h)
            c.head=Function(head.relation, new_h)
        else:
            tms=[]
            for hd in head.terms:
                if isinstance(hd, Variable):
                    for i in keys:
                        if hd==i:
                            hd=s[i]
                        else:
                            pass
                elif isinstance(hd, Function):
                    te=[]
                    for tm in hd.terms:
                        if isinstance(tm, Variable):
                            for i in keys:
                                if tm==i:
                                    tm=s[i]
                                else:
                                    pass
                        elif isinstance(tm ,Function):
                            tm=self.substitute_in_term(s,tm)
                        else:
                            pass
                        te.append(tm)
                    hd=Function(hd.relation, te)
                else:
                    pass
                tms.append(hd)
            c.head.terms=tms

        new_body=[]
        for b in body.terms:
            if isinstance(b,Variable):
                for i in keys:
                    if b==i:
                        b=s[i]
                    else:
                        pass

            elif isinstance(b,Function):
                new_b=[]
                for i in b.terms:
                    if isinstance(i, Function):
                        i=self.substitute_in_term(s,i)
                    elif isinstance(i,Variable):
                        for n in keys:
                            if i==n:
                                i=s[n]
                            else:
                                pass
                    else:
                        pass
                    new_b.append(i)
                b=Function(b.relation, new_b)

            else:
                pass
            new_body.append(b)

        c.body.terms=new_body
        return c
    '''
    '''
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
            rul=[]
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
            c.head.terms=rule
            c.body.terms=rule2
            return c
    '''

    '''
    #qsh
    def nondet_query (self, program : List[Rule], pgoal : List[Term]) -> List[Term]:
        resolve=pgoal[:]
        g=self.nondet_2(program, pgoal, resolve, {})
        return g

    def nondet_2(self, program, goals, resolve, unifer):
        while resolve:
            random_int=random.randint(0, len(resolve)-1)
            A=resolve[random_int]
            rules=[]
            resolve_2=[]
            for rule in program:
                if isinstance(A, RuleBody):
                    for term in A.terms:
                        if rule.head.relation==term.relation:
                            rules.append(rule)
                elif rule.head.relation==A.relation:
                    rules.append(rule)
                else:
                    pass
            if rules==[]:
                return goals
            random_rule=random.randint(0, len(rules)-1)
            chosen_rule=rules[random_rule]
            chosen_rule=self.freshen(chosen_rule)
            try:
                unifer=self.unify_2(A, chosen_rule.head,unifer)
            except:
                print("sorry")
                return(self.nondet_query(program, goals))
            resolve.remove(A)
            for i in unifer:
                print(i, unifer[i])
            for b in chosen_rule.body.terms:
                b=self.substitute_in_term(unifer, b)
                resolve.append(b)
            go=[]
            for i in goals:
                i=self.substitute_in_term(unifer, i)
                go.append(i)
            if not resolve:
                return go
        '''

    def substitute_in_clause (self, s : dict, c : Rule) -> Rule:
        hd=c.head
        hdterm=c.head.terms
        body=c.body
        bdterm=c.body.terms
        head=[]
        if isinstance(hd, Variable):
            c.head=self.substitute_in_term(s, hd)
        elif isinstance(hd, Function):
            c.head=self.substitute_in_term(s, hd)
        else: 

            for i in hdterm:
                if isinstance(i, Variable):
                    i=self.substitute_in_term(s, i)
                elif isinstance(i, Function):
                    i=self.substitute_in_term(s, i)
                head.append(i)
            c.head.terms=head
            body=[]
            for i in bdterm:
                if isinstance(i, Variable):
                    i=self.substitute_in_term(s, i)
                elif isinstance(i, Function):
                    i=self.substitute_in_term(s, i)
                body.append(i)
            c.body.terms=body
        return c

    def dfs(self, goal, resolve, resu, program): 
        if not resolve:
            print(resu)
            if goal not in resu:
                resu.append(goal)
            return True
        while resolve:
            for i in resolve:
                our_goal=i
                break
            resolve.remove(our_goal)
            searched=False
            for p in program:
                res=[]
                goalp=[]
                rel1=p.head.relation
                rel2=our_goal.relation
                if rel1==rel2:
                    p=self.freshen(p)
                    try:
                        unifer=self.unify(our_goal, p.head)
                    except:
                        return resu
                    new_resolve=resolve[:]
                    n_goal=goal[:]
                    body=p.body
                    for b in body.terms:
                        new_resolve.append(b)
                    for re in new_resolve:
                        re=self.substitute_in_term(unifer, re)
                        res.append(re)
                    for re in n_goal:
                        re=self.substitute_in_term(unifer, re)
                        goalp.append(re)
                    new_resolve=res
                    n_goal=goalp

                    r=self.dfs(n_goal, new_resolve, resu, program)
                    searched=r or searched
                    if r==resu[::-1]:
                        return r
                else: 
                    if searched==True:
                        return resu[::-1]
        if not searched:
            return

    def det_query (self, program : List[Rule], pgoal : List[Term]) -> List[List[Term]]:
        resolve=pgoal[:]
        c=self.dfs(pgoal, resolve, [], program)
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


def test_final_3_2 ():
    t = Variable ("Y")
    t_ = Variable ("X")
    u = {Variable ("X"): Variable ("Y")}
    u_ = {Variable ("Y"): Variable ("X")}
    assert (interpreter.unify (t, t_) == u or interpreter.unify (t, t_) == u_)

def test_final_3_3 ():
    t = Variable ("Y")
    t_ = Variable ("Y")
    assert (interpreter.unify (t, t_) == {})

def test_final_3_4 ():
    t = Number("0")
    t_ = Number("0")
    assert (interpreter.unify (t, t_) == {})

def test_final_3_5 ():
    t = Number ("0")
    t_ = Variable ("Y")
    u = {Variable ("Y"): Number("0")}
    assert (interpreter.unify (t, t_) == u)
def test_final_3_6 ():
    t = Number("0")
    t_ = Number("1")
    try:
        interpreter.unify (t, t_)
        assert False
    except Not_unifiable:
        assert True

def test_final_3_7 ():
    t = Function ("f", [Number("0")])
    t_ = Function ("g", [Number("1")])
    try:
        interpreter.unify (t, t_)
        assert False
    except Not_unifiable:
        assert True

def test_final_3_8 ():
    u = {(Variable ("X")): (Variable ("Y"))}
    u_ = {(Variable ("Y")): (Variable ("X"))}
    t = Function ("f", [Variable ("X")])
    t_ = Function ("f", [Variable ("Y")])
    assert (interpreter.unify (t, t_) == u or interpreter.unify (t, t_) == u_)

def test_final_3_9 ():
    t1 = Function ("f", [Variable ("X"), Variable ("Y"), Variable ("Y")])
    t2 = Function ("f", [Variable ("Y"), Variable ("Z"), Atom ("a")])
    u = { Variable("X"): Atom("a"), Variable("Y"): Atom("a"), Variable("Z"): Atom("a") }
    #interpreter.unify (t1, t2)
    assert (interpreter.unify (t1, t2) == u)
def list2str(l):
    return ('(' + (',' + ' ').join(
        list(map(str, l))) + ')')

def test_challenge_3():
    # Tests choice points
    g = [ancestor (Variable("X"), Atom("robb"))]
    print (f"Goal: {list2str(g)}")
    g_ = interpreter.det_query (pstark, g)
    assert (len(g_) == 2)
    g1, g2 = g_[0], g_[1]
    print (f"Solution: {list2str(g1)}")
    print (f"Solution: {list2str(g2)}")
    assert (g1 == [ancestor (Atom("ned"), Atom("robb"))])
    assert (g2 == [ancestor (Atom("rickard"), Atom("robb"))])

def test_challenge_1():
    print ("\n\n###################################################")
    print ("###### Testing the deterministic interpreter ######")
    print ("###################################################")
    print (f"Program: {list2str(psimple)}")
    # Tests query failure
    g = [Function ("f", [Atom ("a"), Atom ("c")])]
    print (f"Goal: {list2str(g)}")
    print("we have:",interpreter.det_query (psimple, g))
    assert (interpreter.det_query (psimple, g) == [])
    

# Test on the Stark House program
def test_challenge_2():
    print (f"\nProgram:{list2str(pstark)}")
    # Tests backtracking
    g = [ancestor (Atom("rickard"), Atom("robb"))]
    print (f"Goal: {list2str(g)}")
    g_ = interpreter.det_query (pstark, g)
    assert (len(g_) == 1)
    g_ = g_[0]
    print (f"Solution: {list2str(g_)}")
    assert (g_ == g)

def test_challenge_4():
    print (f"\nProgram: {list2str(pappend)}")
    # Tests choice points
    g = [append (Variable("X"), (Variable("Y")), (cons (Number("1"), (cons (Number("2"), (cons (Number("3"), nil)))))))]
    print (f"Goal: {list2str(g)}")
    g_ = interpreter.det_query (pappend, g)
    assert (len(g_) == 4)
    for sg in g_:
        print (f"Solution: {list2str(sg)}")

def test_final_4_1():
    print ("\n\n################################################################")
    print ("###### Testing the non-deterministic abstract interpreter ######")
    print ("################################################################")
    print (f"Program: {list2str(psimple)}")
    g = [Function ("f", [Atom("a"), Atom("b")])]
    print (f"Goal: {list2str(g)}")
    #interpreter.nondet_query (psimple, g)
    g_ = interpreter.nondet_query (psimple, g)
    assert (g_ == [Function ("f", [Atom("a"), Atom("b")])])
    print (f"Solution: {list2str(g_)}")

def test_final_4_2():
    g = [Function ("f", [Variable("X"), Atom("b")])]
    print (f"Goal: {list2str(g)}")
    interpreter.nondet_query (psimple, g)
    g_ = interpreter.nondet_query (psimple, g)
    assert (g_ == [Function ("f", [Atom("a"), Atom("b")])]);
    print (f"Solution: {list2str(g_)}")
def test_final_4_3():
    g = [Function ("f", [Variable ("X"), Variable("Y")])]
    print (f"Goal: {list2str(g)}")
    g_ = interpreter.nondet_query (psimple, g)
    assert (g_ == [Function ("f", [Atom("a"), Atom("b")])])
    print (f"Solution: {list2str(g_)}")
def test_final_4_4():
    print (f"\nProgram: {list2str(pstark)}")
    g = [ancestor (Atom("rickard"), Atom("ned"))]
    print (f"Goal: {list2str(g)}")
    g_ = interpreter.nondet_query (pstark, g)
    print (f"Solution: {list2str(g_)}")
    assert (g_ == [ancestor (Atom("rickard"), Atom("ned"))])

def test_final_4_5():
    g = [ancestor (Atom("rickard"), Atom("robb"))]
    print (f"Goal: {list2str(g)}")
    interpreter.nondet_query (pstark, g)
    g_ = interpreter.nondet_query (pstark, g)
    print (f"Solution: {list2str(g_)}")
    assert (g_ == [ancestor (Atom("rickard"), Atom("robb"))])

def test_final_4_6 ():
    g = [ancestor (Variable("X"), Atom("robb"))]
    print (f"Goal: {list2str(g)}")
    g_ = interpreter.nondet_query (pstark, g)
    print (f"Solution: {list2str(g_)}")
    assert (g_ == [ancestor (Atom("ned"), Atom("robb"))] or
                    g_ == [ancestor (Atom("rickard"), Atom("robb"))])
def test_final_4_7():
    print (f"\nProgram: {list2str(pappend)}")
    g = [append (Variable("X"), Variable("Y"), \
            (cons (Number("1"), (cons (Number("2"), (cons (Number("3"), nil)))))))]
    print (f"Goal: {list2str(g)}")
    g_ = interpreter.nondet_query (pappend, g)
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
    '''
    assert (
    g_ == [append (nil, (cons (Number("1"), (cons (Number("2"), (cons (Number("3"), nil)))))), \
                            (cons (Number("1"), (cons (Number("2"), (cons (Number("3"), nil)))))))] or
    g_ == [append ((cons (Number("1"), nil)), (cons (Number("2"), (cons (Number("3"), nil)))), \
                            (cons (Number("1"), (cons (Number("2"), (cons (Number("3"), nil)))))))] or
    g_ == [append ((cons (Number("1"), (cons (Number("2"), nil)))), (cons (Number("3"), nil)), \
                            (cons (Number("1"), (cons (Number("2"), (cons (Number("3"), nil)))))))] or
    g_ == [append ((cons (Number("1"), (cons (Number("2"), (cons (Number("3"), nil)))))), nil, \
                            (cons (Number("1"), (cons (Number("2"), (cons (Number("3"), nil)))))))] )
    '''
if __name__ == '__main__':
    psimple = [Rule(Function ("f", [Atom("a"), Atom("b")]), RuleBody ([]))]
    interpreter = Interpreter()
    def ancestor (x, y): return Function ("ancestor", [x, y])
    def father (x, y): return Function ("father", [x, y])
    def father_consts (x, y):  return father (Atom (x), Atom (y))
    f1 = Rule (father_consts ("rickard", "ned"), RuleBody([]))
    f2 = Rule (father_consts ("ned", "robb"), RuleBody([]))
    r1 = Rule (ancestor (Variable ("X"), Variable ("Y")), RuleBody([father (Variable ("X"), Variable ("Y"))]))
    r2 = Rule (ancestor (Variable ("X"), Variable ("Y")), \
    RuleBody([father (Variable ("X"), Variable ("Z")), ancestor (Variable ("Z"), Variable ("Y"))]))
    pstark = [f1,f2,r1,r2]

    nil = Atom("nil")
    def cons (h, t): return Function ("cons", [h, t])
    def append (x, y, z): return Function ("append", [x, y, z])
    c1 = Rule (append (nil, Variable("Q"), Variable("Q")), RuleBody([]))
    c2 = Rule (append ((cons (Variable("H"), Variable("P"))), Variable("Q"), (cons (Variable("H"), Variable("R")))), \
                RuleBody([append (Variable("P"), Variable("Q"), Variable("R"))]))
    pappend = [c1, c2]
    #g = [ancestor (Variable("X"), Atom("robb"))]
    #print (f"Goal: {list2str(g)}")
    #g_ = interpreter.det_query (pstark, g)
    g = [ancestor (Variable("X"), Atom("robb"))]
    #print (f"Goal: {list2str(g)}")
    #interpreter.det_query (pstark, g)
    '''
    def test_challenge_3():
            # Tests choice points
            g = [ancestor (Variable("X"), Atom("robb"))]
            print (f"Goal: {list2str(g)}")
            g_ = interpreter.det_query (pstark, g)
            assert (len(g_) == 2)
            g1, g2 = g_[0], g_[1]
            print (f"Solution: {list2str(g1)}")
            print (f"Solution: {list2str(g2)}")
            assert (g1 == [ancestor (Atom("ned"), Atom("robb"))])
            assert (g2 == [ancestor (Atom("rickard"), Atom("robb"))])
    '''
    #test_final_3_2 ()
    #test_final_3_3 ()
    #test_final_3_4 ()
    #test_final_3_5 ()
    #test_final_3_6 ()
    #test_final_3_7 ()
    #test_final_3_9 ()
    #test_final_4_5()
    #test_final_4_6()


    #g = [ancestor (Variable("X"), Atom("robb"))]
    #print (f"Goal: {list2str(g)}")
    #interpreter.nondet_query (pstark, g)
    test_challenge_4()
