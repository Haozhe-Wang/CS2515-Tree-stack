import math
class TreeNode(object):
    def __init__(self,element,leftchild=None,rightchild=None,parent=None):
        self._element=element
        self._leftchild=leftchild
        self._rightchild=rightchild
        self._parent=parent
    def __str__(self):
        return 'Node element is %s'%(str(self._element))
    def getElement(self):
        return self._element
    def getLeftchild(self):
        return self._leftchild
    def getRightchild(self):
        return self._rightchild
    def getParent(self):
        return self._parent
    def setElement(self,element):
        self._element=element
    def setLeftchild(self,leftchild):
        self._leftchild=leftchild
    def setRightchild(self,rightchild):
        self._rightchild=rightchild
    def setParent(self,parent):
        self._parent=parent
    leftchild=property(getLeftchild,setLeftchild)
    element=property(getElement,setElement)
    rightchild=property(getRightchild,setRightchild)
    parent=property(getParent,setParent)

#calculation expression, convert from in-order to post-order
#need ADT: list(result), stack
#if it is a number, append it to the list;
#if it is an open bracket, push it onto the stack;
#if it is an operator, while the top of the stack is an operator of equal or higher precedence, pop from the stack and append to the list, and then push the current operator onto the stack;
#if it is a close bracket, keep popping from the stack and appending to the list until you pop an open bracket
def calculationInOrderToPostOrder(expression):
    stack=[]
    result=[]
    num=''
    for n in expression:
        if n.isdigit():
            num+=n
        elif num!='':
            result.append(int(num))
            num=''
        if n in ['(','[']:
            stack.append(n)
        elif n in ['*','+','-','/']:
            if stack==[]:
                pass
            elif n in ['*','/'] and stack[-1] in ['*','/'] or n in ['+','-'] and stack[-1] in ['+','-','*','/']:
                result.append(stack.pop())
            stack.append(n)
        elif n in [')',']']:
            op=''
            if n==')':
                op='('
            elif n=='[':
                op='['
            while stack[-1]!=op:
                result.append(stack.pop())
            stack.pop()
    if num!='':
        result.append(num)
    while stack!=[]:
        result.append(stack.pop())
    return result

def preOrderBuildTree(expression):
    depth=math.ceil(math.log(len(expression),2))
    layer=1
    root=TreeNode(expression[0])
    node=root
    for e in expression[1:]:
        tree=TreeNode(e)
        while 1:
            if not node.leftchild and layer<depth:
                node.leftchild=tree
                tree.parent=node
                node=tree
                layer+=1
                break
            elif not node.rightchild and layer<depth:
                node.rightchild = tree
                tree.parent = node
                node = tree
                layer += 1
                break
            else:
                node=node.parent
                layer-=1
    return root


#note the expression should be postorder, if not, use upper functions to convert
def buildTree(expression):
    stack=[]
    for e in expression:
        if type(e)==int or e.isdigit():
            stack.append(TreeNode(e))
        elif e in ['+','*','/','-']:
            right=stack.pop()
            left=stack.pop()
            operation=TreeNode(e,left,right)
            left.parent=operation
            right.parent=operation
            stack.append(operation)
    return stack[0]

def preOrderShowTree(node):
    output=''
    if node==None:
        return ''
    else:
        output+=str(node.element)
        output+=preOrderShowTree(node.leftchild)
        output+=preOrderShowTree(node.rightchild)
    return output
def inOrderShowTree(node):
    output=''
    if node==None:
        return ''
    else:
        bracket=''
        back_bracket=''
        if  node.leftchild and  node.rightchild:
            bracket='('
            back_bracket = ')'
        output+=bracket+inOrderShowTree(node.leftchild)
        output += str(node.element)
        output+=inOrderShowTree(node.rightchild)+back_bracket
    return output
def postOrderShowTree(node):
    output = ''
    if node == None:
        return ''
    else:
        output += postOrderShowTree(node.leftchild)
        output += postOrderShowTree(node.rightchild)
        output += str(node.element)
    return output
print(postOrderShowTree(buildTree(calculationInOrderToPostOrder('(4 + 2) * (5 - 3)'))))
print(postOrderShowTree(preOrderBuildTree('*+42-53')))

