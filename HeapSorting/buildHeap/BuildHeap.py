#Build this heap by building from the bottom to the top
def upHeap(lst):
    num=len(lst)
    index=num-1-(num//2)
    leftchild=index*2+1
    rightchild=index*2+2
    i=index
    while i>=0 :
        while  leftchild<num:
            #if rightchild have value greater than leftchild, and greater than the current value
            if rightchild<num and lst[rightchild]>lst[leftchild] and lst[rightchild]>lst[index]:
                lst[index],lst[rightchild]=lst[rightchild],lst[index]
                index = rightchild
            #if there is leftchild and has value greater than current value
            elif lst[leftchild]>lst[index]:
                lst[index], lst[leftchild] = lst[leftchild], lst[index]
                index = leftchild
            else:
                break

            #update the leftchild and rightchild
            leftchild = index * 2 + 1
            rightchild = index * 2 + 2

        #move to next element of the list
        i-=1
        index=i
        leftchild = index * 2 + 1
        rightchild = index * 2 + 2
    return lst

#build this heap by building from top to the bottom
def downHeap(lst):
    i=1
    while i<len(lst):
        index=i
        parent=(index-1)//2
        while parent>=0 and lst[parent]<lst[index]:
            lst[parent],lst[index]=lst[index],lst[parent]
            index=parent
            parent=(index-1)//2
        i+=1
    return lst
def generateList(n):
    from random import shuffle
    lst = [None] * n
    for i in range(n):
        lst[i] = i
    shuffle(lst)
    return lst
def Heaptest(n,number):
    from time import perf_counter
    total_up=0
    total_down=0

    for i in range(number):
        lst=generateList(n)
        lst2=lst.copy()

        #this should be the fast version with O(n)
        start=perf_counter()
        upHeap(lst)
        total_up+=perf_counter()-start

        #this should be the slower version with O(nlogn)
        start = perf_counter()
        downHeap(lst2)
        total_down += perf_counter() - start


    print('bubble up heap average: %f'%(total_up/number)) #time 0.963352

    print('bubble down heap average: %f' % (total_down / number)) #time 0.731332


Heaptest(1000000,20)
# print(upHeap([2,1,4,6,6,6,8,4,4,24]))