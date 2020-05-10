# all the different sorting and searching algorithms

import time
from copy import deepcopy
numOps = 0
arrayPositions = []

# node class with left, right and value attributes
class Node():
    def __init__(self, value, left = None, right = None):
        self.value = value
        self.left = left
        self.right = right

# tree class: creates balanced trees and performs binary search
class Tree():
    def __init__(self, valueList):
        self.rootNode = self.createBalancedTree(valueList)
    # creates balanced tree
    def createBalancedTree(self, valueList):
        if valueList == []:
            return None
        # middle value is selected as parent node; makes tree more balanced
        mid = len(valueList)//2
        rootNode = Node(valueList[mid])
        rootNode.left = self.createBalancedTree(valueList[:mid])
        rootNode.right = self.createBalancedTree(valueList[mid+1:])
        return rootNode

    def binarySearch(self, value, parent, checked=[]):
        global numOps
        numOps += 1
        # if value is too small, perform binary search on the left side
        if value < parent.value:
            if parent.left:
                checked.append('left')
                if parent.left.value == value:
                    return checked
                else:
                    return self.binarySearch(value, parent.left, checked)
            else:
                return 'False'
        # if value is too small, perform binary search on the right side
        elif value > parent.value:
            if parent.right:
                checked.append('right')
                if parent.right.value == value:
                    return checked
                else:
                    return self.binarySearch(value, parent.right, checked)
            else:
                return 'False'
        else:
            return checked

def bubble(list_input):
    checked=0
    global numOps
    global arrayPositions
    for i in range(len(list_input)-1):
        for j in range(1, len(list_input)-checked):
            numOps+=1
            # compare elements, swap if next is smaller than previous
            if list_input[j-1]>list_input[j]:
                arrayPositions.append([j-1, deepcopy(list_input)])
                list_input[j-1],list_input[j]=list_input[j], list_input[j-1]
        checked+=1
    return list_input

def insert(list_input):
    global numOps
    global arrayPositions
    for i in range(1, len(list_input)):
        arrayPositions.append([i, deepcopy(list_input)])
        key = list_input[i]
        j = i-1
        # find correct position and insert element at this position
        while j >=0 and key < list_input[j] :
            numOps+=1
            list_input[j+1]=list_input[j]
            j -= 1
        list_input[j+1]=key
    return list_input

def merge(list_input):
    #breaks the list down to one-element lists
    new_list = []
    for i in list_input:
        new_list.append([i])
    global numOps
    global arrayPositions
    #actual merge sort function
    def merge2(list_input):
        global numOps
        global arrayPositions
        list_copy=[]
        for i in range(1,len(list_input),2):
            p=0
            q=0
            new_list=[]
            left = list_input[i-1]
            right = list_input[i]
            # merge two lists into one bigger one
            while p < len(left) and q < len(right):
                numOps+=1
                if left[p] < right [q]:
                    new_list.append(left[p])
                    p+=1
                else:
                    new_list.append(right[q])
                    q+=1
            # add the rest of the elements if one list is done
            if p == len (left) and q < len(right):
                new_list+=right[q:]
            elif p < len(left) and q == len (right):
                new_list+=left[p:]
            list_copy.append(new_list)
        # special case; number of lists is odd (can't merge)
        if (len(list_input))%2==1:
            list_copy.append(list_input[-1])

        list_input = deepcopy(list_copy)
        flat_list = [item for sublist in list_input for item in sublist]
        arrayPositions.append([-1, deepcopy(flat_list)])

        # only one list: list has been merged
        if len(list_copy) == 1:
            return new_list
        return merge2(list_copy)
    return merge2(new_list)

def counting(list_input):
    global numOps
    global arrayPositions
    my_list=[0]*100001
    # count occurences of each element
    for i in range(len(list_input)):
        numOps+=1
        my_list[list_input[i]] +=1
        arrayPositions.append([i, list_input])
    sorted_list=[]
    # add counted elements in order
    for i in range (0,100001):
        sorted_list+=[i]*my_list[i]
    return sorted_list

def partition(list_input,start,end):
    global arrayPositions
    global numOps
    i = start - 1
    pivot = list_input[end]
    for j in range(start , end):
        if list_input[j] < pivot:
            arrayPositions.append([j, deepcopy(list_input)])
            numOps += 1
            i = i+1
            list_input[i],list_input[j] = list_input[j],list_input[i]

    list_input[i+1],list_input[end] = list_input[end],list_input[i+1]
    return ( i+1 )

def quickSort(list_input,start=0,end=-1):
    if end == -1:
        end = len(list_input)-1
    global arrayPositions
    global numOps
    if start < end:
        pivot = partition(list_input,start,end)
        quickSort(list_input, start, pivot-1)
        quickSort(list_input, pivot+1, end)
    return list_input


def linearSearch(list_input, target):
    global numOps
    global arrayPositions
    for i in range(len(list_input)):
        numOps+=1
        arrayPositions.append([i, []])
        # check if current element is the target, if not go to next
        if list_input[i] == target:
            return i
    return 'False'

def binarySearch(list_input, target):
    global numOps
    global arrayPositions
    start = 0
    end = len(list_input) - 1
    pivot=0
    while start < end:
        pivot = int((start + end)/2)
        numOps+=1
        arrayPositions.append([pivot, []])
        # if element is smaller than pivot, go left; else go right
        if list_input[pivot] > target:
            end = pivot -1
        elif list_input[pivot] < target:
            start = pivot + 1
        else:
            return pivot
    return 'False'

def timeAlgorithm(algorithm, data, target=None, root=None):
    # numOps counts the number of comparisons
    # made global to help with recursion counting issues
    global numOps
    global arrayPositions
    numOps = 0
    arrayPositions = []
    start = time.time()
    # special case; it's a search algorithm
    if target:
        # special case; it's binary tree search
        if root:
            output = algorithm(target, root, [])
        else:
            output = algorithm(data, target)
    else:
        output = algorithm(data)
        arrayPositions.append([-1,output])
    end = time.time()
    # measure time needed for algorithm to run
    total = end - start

    return total, numOps, output, arrayPositions
