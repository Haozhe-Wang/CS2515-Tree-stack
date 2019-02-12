import random
import time
import copy
class Sort():
    def __init__(self,lst):
        self._lst=lst
        self._length=len(self._lst)
    def getLst(self):
        return self._lst
    def setLst(self,lst):
        self._lst=lst
        self._length = len(self._lst)
    def selectionSort(self):
        for i in range(self._length-1):
            current_pos=self._length-i-1
            big=current_pos
            for k in range(current_pos,-1,-1):
                if self._lst[big]<self._lst[k]:
                    big=k
            if big!=current_pos:
                self._lst[big],self._lst[current_pos]=self._lst[current_pos],self._lst[big]
        return self._lst
    def _quickSort(self,pivot,end):
        if pivot == end:
            return
        head=pivot+1
        tail=end
        while head<=tail and head<=end:
            if self._lst[head]<=self._lst[pivot]:
                head+=1
            elif self._lst[tail]>self._lst[pivot]:
                tail-=1
            elif self._lst[head]>self._lst[tail]:
                self._lst[head],self._lst[tail]=self._lst[tail],self._lst[head]
        self._lst[pivot],self._lst[tail]=self._lst[tail],self._lst[pivot]
        if pivot<tail:
            self._quickSort(pivot,tail-1)
        if tail+1<end:
            self._quickSort(tail+1, end)
    def quickSort(self):
        if self._lst==[]:return []
        random.shuffle(self._lst)
        self._quickSort(0,self._length-1)
        return self._lst
    def _mergeSort(self,lst):
        length=len(lst)
        if length<=1:
            return lst
        lst1=self._mergeSort(lst[:length//2])
        lst2=self._mergeSort(lst[length//2:])
        return self._merge(lst1,lst2,lst)
    def _merge(self,lst1,lst2,lst):
        f1=0
        f2=0
        current=0
        while current<len(lst):
            if f1==len(lst1) or f2<len(lst2) and lst1[f1]>lst2[f2]:
                lst[current]=lst2[f2]
                f2+=1
            else:
                lst[current] = lst1[f1]
                f1 += 1
            current+=1
        return lst
    def mergeSort(self):
        self._lst=self._mergeSort(self._lst)
        return self._lst

    def _createHeap(self):
        for i in range(1,self._length):
            index = i
            parent = (index - 1) // 2
            while parent >= 0 and self._lst[parent] < self._lst[index]:
                self._lst[parent], self._lst[index] = self._lst[index], self._lst[parent]
                index = parent
                parent = (index - 1) // 2
        return self._lst

    def _sortHeap(self):
        for pos in range(self._length-1,0,-1):
            self._lst[pos],self._lst[0]=self._lst[0],self._lst[pos]
            index = 0
            leftchild = 1
            rightchild = 2
            while leftchild < pos:
                # if rightchild have value greater than leftchild, and greater than the current value
                if rightchild < pos and self._lst[rightchild] > self._lst[leftchild] and self._lst[rightchild] > self._lst[index]:
                    self._lst[index], self._lst[rightchild] = self._lst[rightchild], self._lst[index]
                    index = rightchild
                # if there is leftchild and has value greater than current value
                elif self._lst[leftchild] > self._lst[index]:
                    self._lst[index], self._lst[leftchild] = self._lst[leftchild], self._lst[index]
                    index = leftchild
                else:
                    break

                # update the leftchild and rightchild
                leftchild = index * 2 + 1
                rightchild = index * 2 + 2
    def python(self):
        self._lst.sort()
        return self._lst

    def heapSort(self):
        self._createHeap()
        self._sortHeap()
        return self._lst

    lst = property(getLst, setLst)

def evaluateall(n, k):
    total_lst=[]
    lst = [None] * n
    for i in range(n-k):
        lst[i]=i
    for i in range(k):
        lst[n-k+i]=lst[random.randint(0,n-k-1)]
    for i in range(10):
        lst_temp=copy.copy(lst)
        random.shuffle(lst_temp)
        total_lst.append(lst_temp)
    return total_lst

def evaluate():
    ks=[0,20,70]
    sort=Sort([])
    for i in range(3):
        n=100
        k=ks[i]
        for b in range(4):
            if b >0:
                n=n*10
                k=k*10
            lsts=evaluateall(n,k)
            functions = {sort.heapSort: 0, sort.quickSort: 0, sort.mergeSort: 0, sort.selectionSort: 0,sort.python:0}
            for lst in lsts:
                for function in functions:
                    if function == sort.selectionSort and n>10000:
                        continue
                    lst_temp=copy.copy(lst)
                    sort.setLst(lst_temp)
                    start=time.perf_counter()
                    function()
                    end=time.perf_counter()
                    functions[function]+=end-start
            for function,t in functions.items():
                if function == sort.selectionSort and n>10000:
                        continue
                print('%f %s %d %d'%(t/10,function.__name__,n,k))
            print()
evaluate()

'''
for i in range(len(lst_temp) - 1):
    if lst_temp[i] > lst_temp[i + 1]:
        raise ValueError('wrong')
'''


'''
0.000297 heapSort 100 0         0.004961 heapSort 1000 0        0.065785 heapSort 10000 0        0.933791 heapSort 100000 0
0.000266 quickSort 100 0        0.004431 quickSort 1000 0       0.054386 quickSort 10000 0       0.708136 quickSort 100000 0
0.000335 mergeSort 100 0        0.004850 mergeSort 1000 0       0.060197 mergeSort 10000 0       0.773529 mergeSort 100000 0
0.000566 selectionSort 100 0    0.052635 selectionSort 1000 0   5.438045 selectionSort 10000 0  
0.000011 python 100 0           0.000171 python 1000 0          0.002371 python 10000 0          0.032999 python 100000 0


0.000280 heapSort 100 20         0.004735 heapSort 1000 200        0.068639 heapSort 10000 2000         0.971701 heapSort 100000 20000
0.000247 quickSort 100 20        0.004039 quickSort 1000 200       0.053144 quickSort 10000 2000        0.752591 quickSort 100000 20000
0.000327 mergeSort 100 20        0.004142 mergeSort 1000 200       0.056355 mergeSort 10000 2000        0.833350 mergeSort 100000 20000
0.000511 selectionSort 100 20    0.048355 selectionSort 1000 200   5.172299 selectionSort 10000 2000 
0.000011 python 100 20           0.000160 python 1000 200          0.002370 python 10000 2000           0.032869 python 100000 20000


0.000549 heapSort 100 70         0.005169 heapSort 1000 700        0.075700 heapSort 10000 7000         0.857019 heapSort 100000 70000
0.000534 quickSort 100 70        0.004397 quickSort 1000 700       0.060228 quickSort 10000 7000        0.707924 quickSort 100000 70000
0.000538 mergeSort 100 70        0.004272 mergeSort 1000 700       0.060859 mergeSort 10000 7000        0.713569 mergeSort 100000 70000
0.001071 selectionSort 100 70    0.049326 selectionSort 1000 700   5.311037 selectionSort 10000 7000
0.000010 python 100 70           0.000186 python 1000 700          0.002269 python 10000 7000           0.030877 python 100000 70000

The statistic shows that when the input size is only 100:
all the sorting algorithm have the same level of complexity except python built-in algorithm.
Python built-in sorting is around 30 to 50 times faster than heapSort, mergeSort and quickSort
The selectionSort is almost two times slower than the other three algorithm(except python built-in algorithm)
The speed of heapSort, mergeSort and quickSort are very close to each other, but quick sort is slightly faster than the other two(about 10% faster)
As the duplicate values grow, python built-in sorting remains in stationary time, but the other four sorting are all become slower

When the input size gets 10 times larger:
Horizontal observation:
heapSort, mergeSort, quickSort and python built-in algorithm are all over 10 times slower than the last smaller input size
however the selectionSort is over 10 square times slower than the last smaller input size
Vertical observation:
The relation of each sorting performance are similar to the size of 100
But the time gap between selectionSort and other sorting algorithms is getting much bigger when the size grows 
The quickSort is still the slightly fastest algorithm in general among heapSort, mergeSort and quickSort, however this is not always the case.
For instance, the input size is 1000 and 700 duplicates, the quickSort is slower than the mergeSort
Also, we could spot that the heapSort is usually the slowest sort among heapSort, mergeSort and quickSort
python built-in sort is still over 10 times faster than heapSort, mergeSort and quickSort
Contrary to the input size of 100, when input size changes, the numbers of duplicate values may have no relation with the average total time of each sort
(In other words, after the numbers of duplicate values change from 0 to 70, 700, 7000 or 70000,
the average total amount of time of each algorithm can be better, worse or the same.)

When the input size is 100000:
it is more clear that the heapSort is the slowest sort among heapSort, mergeSort and quickSort
and quickSort is the fastest sort in heapSort, mergeSort and quickSort, which is 10% faster than mergeSort
and python built-in sort is still the fastest sort of all sorting algorithm, and over 20 times faster than other three

'''