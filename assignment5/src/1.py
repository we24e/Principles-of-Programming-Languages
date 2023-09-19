from collections import _OrderedDictItemsView
import sys
from typing import List

'''

def closest_to (l, v):
    re=None
    list.sort(l)
    c=0
    diff=abs(v-l[c])
    if not l:
        pass
    else:
        for i in l:
            c=c+1
            if i==v:
                c=c-1
                re=l[(c-1)]
                break
            else:
                cur_diff=abs(v-l[(c-1)])
                if cur_diff<diff:
                    diff=cur_diff
                    re=l[(c-1)]
                else:
                    pass
    print(re)
    return re


def main(l):
    rt=[]
    occ=1
    if not l:
        pass
    else:
        l2=list(set(l))
        for i in l2:
            cnt=l.count(i)
            rt.append((i,cnt))
    print(rt)
    return rt

'''

"""
def main(f,l):
    c=0
    out=[] 
    lst=l
    #lst=l[(c+1):]
    if not l:
        return out  
    else:
        for i in l:
            cur=[]
            c=c+1
            for j in lst: 
                t=f(i,j)
                if t==True:
                    cur.append(j)
            out.append(cur)
        c=0
        out2=out
        out=[]
        for li in out2:
            if li in out:
                pass
            else:
                out.append(li)
        print(out)

    return out
"""

class TreeNode:
    def __init__(self, val=None, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

    # construct tree from a list of values `ls`
    def list_to_tree(self, ls):
        self.val = self.left = self.right = None # clear the current tree

        if not ls: # ls is None or l == []
            return # tree is None

        i = 0
        self.val = ls[i]
        queue = [self]
        while queue: # while queue is not empty
            i += 1
            node = queue.pop(0)
            if node.val is None:
                continue

            if 2*i -1 >= len(ls) or ls[2*i-1] is None:
                pass
            else:
                node.left = TreeNode(ls[2*i-1])
                queue.append(node.left)

            if 2*i >= len(ls) or ls[2*i] is None:
                pass
            else:
                node.right = TreeNode(ls[2*i])
                queue.append(node.right)


def level_order(root: TreeNode):
    rt=[]
    rtl=TreeNode()
    rtr=TreeNode()
    rtl=root.left
    rtr=root.right
    order=[]
    init=[]
    stop=0

    if root.val== None:
        print(rt)
        return rt
        
    else:
        rt.append([root.val])
        if rtl!=None:
            init.append(rtl)
        if rtr!=None:
            init.append(rtr)

        while init!= []:
            c=len(init)
            #print(c)
            stop=0
            while stop < c: 
                stop=stop+1
                cur=init.pop(0)
                #print(cur)
                if cur.left!= None:
                    init.append(cur.left)
                if cur.right!= None:
                    init.append(cur.right)
                order.append(cur.val)
            rt.append(order)
            order=[]
        print(rt)
        return rt
'''
def dfs(cur, before,res):
    before=before+cur.val
    if(cur.left !=None):
        res=dfs(cur.left, before,res)
    if (cur.right!=None):
        res=dfs(cur.right, before,res)
    if (cur.left==None and cur.right==None):
        res.append(before=before+cur.val)
    print(res)

def dfs(r,lst,before, sum, back):
    print('lst', lst)
    print('r', r)
    print('back', back)
    #print(r.val)


    if r == None:
        return back
    else:
        cur=r.val
        before=before + cur
        if before==sum:
            if r.left==None and r.right==None:
                lst.append(cur)
                back.append(lst)
                return back
            else:
                pass
        else: 
             pass
        to=lst+[cur]
        dfs(r.left, to, before, sum, back)
        dfs(r.right, to, before, sum, back)
        return back

def pathSum(root: TreeNode, targetSum: int) -> List[List[int]]:
    init = [root]
    lst=[]
    back=[]
    if root.val==None :
        return []
    else:
        res=dfs(root,lst,0,targetSum, back)
        #print(res)
        return res
'''
'''
def check(root, self):
    res=[]
    if root is None:
        return[]
    if root.left==None and root.right==None:
        res.append([root.val])
        return (res)
    else:
        return [root.val+c] for c in
        self.check(root.right) + self.check(root.left)
'''
def path(root):
    res=[]
    queue=[root]
    if root is None:
        return[]
    if root.left==None and root.right==None:
        return [str(root.val)]
    else:
        paths=path(root.left)+path(root.right)
        #print(paths)
        for i in paths:
        #str so that can seperate
            res.append(str(root.val)+','+i)
        return res

def sum(lst, num):
    res=0
    resl=[]
    level=[]
    if lst==[]:
        return []
    for i in lst:
        i=i.split(",")
        for j in i:
            j=int(j)
            level.append(j)
            res=res+j
        if res==num:
            resl.append(level)
        level=[]
        res=0
    return resl

def pathSum(root: TreeNode, targetSum: int) -> List[List[int]]:
    c=path(root)
    res=sum(c, targetSum)
    return res


          

if __name__ == '__main__':
    root_1=TreeNode()
    root_1.list_to_tree([5,4,8,11,None,13,4,7,2,None,None,5,1])
    pathSum(root_1, 22)
    #root_1.list_to_tree([None, None])
    #level_order(root_1)
    #main(lambda a, b : a == b, [1,2,3,4])
    #main((lambda a, b : a == b), [1,2,3,4,2,3,4,3,4])
    #main(lambda a, b : a % 3 == b % 3, [1,2,3,4,5,6])
    #buckets(lambda a, b : a % 3 == b % 3, [1,2,3,4,5,6])