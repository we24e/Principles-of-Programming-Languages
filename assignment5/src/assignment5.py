from typing import List
from functools import reduce
import sys
import traceback

#################
### Problem  1 ##
#################

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
                
    return re

#################
### problem  2 ##
#################

def assoc_list (l):
    rt=[]
    if not l:
        pass
    else:
        l2=list(set(l))
        for i in l2:
            cnt=l.count(i)
            rt.append((i,cnt))
    return rt

#################
### Problem  3 ##
#################

def buckets (f, l):
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

    return out


###################################
# Definition for a binary tree node
###################################

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


#################
### Problem  4 ##
#################

def level_order(root: TreeNode):
    rt=[]
    rtl=TreeNode()
    rtr=TreeNode()
    rtl=root.left
    rtr=root.right
    order=[]
    init=[]
    stop=0

    if root.val == None:
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
                else:
                    pass
                if cur.right!= None:
                    init.append(cur.right)
                else: 
                    pass
                order.append(cur.val)
            rt.append(order)
            order=[]
        return rt


#################
### Problem  5 ##
#################

def dfs(r,lst,before, sum, back):
    '''
    print('lst', lst)
    print('r', r)
    print('back', back)
    #print(r.val)
    '''
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


#################
### Test cases ##
#################

def main():
    print ("Testing your code ...")
    error_count = 0

    # Testcases for Problem 1
    try:
        assert (closest_to([2,4,8,9],7) == 8)
        assert (closest_to([2,3,7,9],5) == 3)
    except AssertionError as err:
        error_count += 1
        _, _, tb = sys.exc_info()
        traceback.print_tb(tb)
        # tb_info = traceback.extract_tb(tb)
        # filename, line, func, text = tb_info[-1]
        # print('An error occurred on line {} in statement {}'.format(line, text))
    except:
        error_count += 1
        print("Unexpected error:", sys.exc_info()[0])
        _, _, tb = sys.exc_info()
        traceback.print_tb(tb)

    # Testcases for Problem 2
    try:
        result = assoc_list([1, 2, 2, 1, 3])
        result.sort(key=lambda x:x[0])
        assert (result == [(1,2), (2, 2), (3, 1)])

        result = assoc_list(["a","a","b","a"])
        result.sort(key=lambda x:x[0])
        assert (result == [("a",3), ("b",1)])

        result = assoc_list([1, 7, 7, 1, 5, 2, 7, 7])
        result.sort(key=lambda x:x[0])
        assert (result == [(1,2), (2,1), (5,1), (7,4)])
    except AssertionError as err:
        error_count += 1
        _, _, tb = sys.exc_info()
        traceback.print_tb(tb)
    except:
        error_count += 1
        print("Unexpected error:", sys.exc_info()[0])
        _, _, tb = sys.exc_info()
        traceback.print_tb(tb)

    # Testcases for Problem 3
    try:
        assert (buckets (lambda a, b : a == b, [1,2,3,4]) == [[1], [2], [3], [4]])
        assert (buckets (lambda a, b : a == b, [1,2,3,4,2,3,4,3,4]) == [[1], [2, 2], [3, 3, 3], [4, 4, 4]])
        assert (buckets (lambda a, b : a % 3 == b % 3, [1,2,3,4,5,6]) == [[1, 4], [2, 5], [3, 6]])
    except AssertionError as err:
        error_count += 1
        _, _, tb = sys.exc_info()
        traceback.print_tb(tb)
    except:
        error_count += 1
        print("Unexpected error:", sys.exc_info()[0])
        _, _, tb = sys.exc_info()
        traceback.print_tb(tb)

    ### Specify 3 trees for testing problems 4 & 5
    root_1 = TreeNode()
    root_1.list_to_tree([5,4,8,11,None,13,4,7,2,None,None,5,1])

    root_2 = TreeNode()
    root_2.list_to_tree([1,2,3])

    root_3 = TreeNode()
    root_3.list_to_tree([1,2])

    # Testcases for Problem 4
    try:
        assert (level_order(root_1) == [[5], [4, 8], [11, 13, 4], [7, 2, 5, 1]])
        assert (level_order(root_2) == [[1], [2, 3]])
        assert (level_order(root_3) == [[1], [2]])
    except AssertionError as err:
        error_count += 1
        _, _, tb = sys.exc_info()
        traceback.print_tb(tb)
    except:
        error_count += 1
        print("Unexpected error:", sys.exc_info()[0])
        _, _, tb = sys.exc_info()
        traceback.print_tb(tb)

    # Testcases for Problem 5
    try:
        assert (pathSum(root_1, 22) == [[5, 4, 11, 2], [5, 8, 4, 5]])
        assert (pathSum(root_2, 4) == [[1, 3]])
        assert (pathSum(root_3, 0) == [])
    except AssertionError as err:
        error_count += 1
        _, _, tb = sys.exc_info()
        traceback.print_tb(tb)
    except:
        error_count += 1
        print("Unexpected error:", sys.exc_info()[0])
        _, _, tb = sys.exc_info()
        traceback.print_tb(tb)

    print (f"{error_count} out of 5 programming questions are incorrect.")

main()
