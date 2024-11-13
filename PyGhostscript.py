#
# Anthony Do
#

import re
def tokenize(s):
    return re.findall("/?[a-zA-Z()][a-zA-Z0-9_()]*|[-]?[0-9]+|[}{]+|%.*|[^ \t\n]", s)


# complete this function
# The it argument is an iterator.
# The sequence of return characters should represent a list of properly nested
# tokens, where the tokens between '{' and '}' is included as a sublist. If the
# parentheses in the input iterator is not properly nested, returns False.
def groupMatching2(it):
    res = []
    for c in it:
        if c == '}':
            return res
        elif c=='{':
            # Note how we use a recursive call to group the tokens inside the
            # inner matching parenthesis.
            # Once the recursive call returns the code array for the inner
            # paranthesis, it will be appended to the list we are constructing
            # as a whole.
            res.append(groupMatching2(it))
        else:
            res.append(convert(c))
    return False

# Complete this function
# Function to parse a list of tokens and arrange the tokens between { and } braces
# as code-arrays.
# Properly nested parentheses are arranged into a list of properly nested lists.
def parse(L):
    res = []
    it = iter(L)
    for c in it:
        if c=='}':  #non matching closing paranthesis; return false since there is
                    # a syntax error in the Postscript code.
            return False
        elif c=='{':
            res.append(groupMatching2(it))
        else:
            res.append(convert(c))
    return res

def convert(c):
    try: # try to convert to int
        r = int(c)
        return r
    except ValueError:
        c2 = c
        # try to convert to Boolean value
        if c2.lower() == "true":
            return True
        elif c2.lower() == "false":
            return False
        else: # not a Boolean
            return c # return without changes

# Write the necessary code here; again write
# auxiliary functions if you need them. This will probably be the largest
# function of the whole project, but it will have a very regular and obvious
# structure if you've followed the plan of the assignment.
#
def interpretSPS(code): # code is a code array
    for item in code:
        interpretSingle(item)

def psIf():
    codeArray = opPop()
    if isinstance(codeArray, list):
        bValue = opPop()
        if isinstance(bValue, bool):
            if bValue:
                interpretSPS(codeArray)
            else:
                return
        else:
            opPush(bValue)
            opPush(codeArray)
    else:
        opPush(codeArray)

def psIfelse():
    elseOption = opPop()
    if isinstance(elseOption, list):
        ifOption = opPop()
        if isinstance(ifOption, list):
            bValue = opPop()
            if isinstance(bValue, bool):
                if bValue:
                    interpretSPS(ifOption)
                else:
                    interpretSPS(elseOption)
            else:
                print("Error: /typecheck in --ifelse--")
                opPush(bValue)
                opPush(ifOption)
                opPush(elseOption)
        else:
            print("Error: /typecheck in --ifelse--")
            opPush(ifOption)
            opPush(elseOption)
    else:
        print("Error: /typecheck in --ifelse--")
        opPush(elseOption)

def psFor():
    codeArray = opPop()
    if isinstance(codeArray, list):
        final = opPop()
        if isinstance(final, int):
            incr = opPop()
            if isinstance(incr, int):
                init = opPop()
                if isinstance(init, int):
                    if incr == 0:
                        print("Not going to compute: results in infinity output.")
                    elif incr > 0:
                        while init <= final:
                            opPush(init)
                            interpretSPS(codeArray)

                            init += incr
                    else:
                        while init >= final:
                            opPush(init)
                            interpretSPS(codeArray)

                            init += incr
                else:
                    print("Error: /typecheck in --for--")
                    opPush(init)
                    opPush(incr)
                    opPush(final)
                    opPush(codeArray)
            else:
                print("Error: /typecheck in --for--")
                opPush(incr)
                opPush(final)
                opPush(codeArray)
        else:
            print("Error: /typecheck in --for--")
            opPush(final)
            opPush(codeArray)
    else:
        print("Error: /typecheck in --for--")
        opPush(codeArray)
    
# used to decide what to do for each input
def interpretSingle(i):
    if isinstance(i, str):
        if i[0] == "(":
            if i[len(i) - 1] == ")":
                opPush(i)
                return
        elif i[0] == "/":
            opPush(i)
        else:
            match(i):
                case "add":
                    add()
                case "sub":
                    sub()
                case "mul":
                    mul()
                case "div":
                    div()
                case "mod":
                    mod()
                case "lt":
                    lt()
                case "gt":
                    gt()
                case "eq":
                    eq()
                case "clear":
                    clear()
                case "dup":
                    dup()
                case "pop":
                    opPop()
                case "stack":
                    stack()
                case "exch":
                    exch()
                case "copy":
                    copy()
                case "roll":
                    roll()
                case "def":
                    psDef()
                case "dict":
                    psDict()
                case "begin":
                    begin()
                case "end":
                    end()
                case "put":
                    put()
                case "get":
                    get()
                case "length":
                    length()
                case "getinterval":
                    getinterval()
                case "if":
                    psIf()
                case "ifelse":
                    psIfelse()
                case "for":
                    psFor()
                case _:
                    lResult = lookup(i)
                    if isinstance(lResult, list):
                        interpretSPS(lResult)
                    else:
                        interpretSingle(lResult)
    elif isinstance(i, int):
        opPush(i)
        return
    elif isinstance(i, list):
        opPush(i)

def interpreter(s): # s is a string
    interpretSPS(parse(tokenize(s)))

#clear opstack and dictstack
def clear():
    del opstack[:]
    del dictstack[:]


#testing

input1 = """
        /square {
               dup mul
        } def
        (square)
        4 square
        dup 16 eq
        {(pass)} {(fail)} ifelse
        stack
        """

input2 ="""
    (facto) dup length /n exch def
    /fact {
        0 dict begin
           /n exch def
           n 2 lt
           { 1}
           {n 1 sub fact n mul }
           ifelse
        end
    } def
    n fact stack
    """

input3 = """
        /fact{
        0 dict
                begin
                        /n exch def
                        1
                        n -1 1 {mul} for
                end
        } def
        6
        fact
        stack
    """

input4 = """
        /lt6 { 6 lt } def
        1 2 3 4 5 6 4 -3 roll
        dup dup lt6 {mul mul mul} if
        stack
        clear
    """

input5 = """
        (CptS355_HW5) 4 3 getinterval
        (355) eq
        {(You_are_in_CptS355)} if
         stack
        """

input6 = """
        /pow2 {/n exch def
               (pow2_of_n_is) dup 8 n 48 add put
                1 n -1 1 {pop 2 mul} for
              } def
        (Calculating_pow2_of_9) dup 20 get 48 sub pow2
        stack
        """

print(tokenize(input1))
print(parse(tokenize(input1)))
print()

print(tokenize(input2))
print(parse(tokenize(input2)))
print()

print(tokenize(input3))
print(parse(tokenize(input3)))
print()

print(tokenize(input4))
print(parse(tokenize(input4)))
print()

print(tokenize(input5))
print(parse(tokenize(input5)))
print()

print(tokenize(input6))
print(parse(tokenize(input6)))
print()

#-------------------------------------------------------------------
# The operand stack: define the operand stack and its operations
opstack = []  #assuming top of the stack is the end of the list

# Now define the helper functions to push and pop values on the opstack
# (i.e, add/remove elements to/from the end of the Python list)
# Remember that there is a Postscript operator called "pop" so we choose
# different names for these functions.
# Recall that `pass` in python is a no-op: replace it with your code.

def opPop():
    try:
        poppedValue = opstack.pop()
        return poppedValue
    except (IndexError):
        print("Error: /stackunderflow in --pop--")
    # opPop should return the popped value.
    # The pop() function should call opPop to pop the top value from the opstack, but it will ignore the popped value.

def opPush(value):
    opstack.append(value)

#--------------------------------------------------------------------
# The dictionary stack: define the dictionary stack and its operations
dictstack = []  #assuming top of the stack is the end of the list

# now define functions to push and pop dictionaries on the dictstack, to
# define name, and to lookup a name

def dictPop():
    try:
        poppedDict = dictstack.pop()
        return poppedDict
    except (IndexError):
        print("Error: /dictstackunderflow in --end--")
    # dictPop pops the top dictionary from the dictionary stack.

def dictPush(d):
    dictstack.append(d)
    #dictPush pushes the dictionary ‘d’ to the dictstack.
    #Note that, your interpreter will call dictPush only when Postscript
    #“begin” operator is called. “begin” should pop the empty dictionary from
    #the opstack and push it onto the dictstack by calling dictPush.

def define(name, value):
    if len(dictstack) == 0:
        newDict = {}
        newDict[name] = value
        dictPush(newDict)
        return
    
    topDict = dictPop()
    if name not in topDict:
        topDict[name] = value
        dictPush(topDict)
        return
    else:
        dictPush(topDict)
        newDict = {}
        newDict[name] = value
        dictPush(newDict)
        return

    #add name:value pair to the top dictionary in the dictionary stack.
    #Keep the '/' in the name constant.
    #Your psDef function should pop the name and value from operand stack and
    #call the “define” function.

def lookup(name):
    newName = '/' + name
    for dict in reversed(dictstack):
        if newName in dict:
            return dict[newName]
    
    #print(f"--Error: {name} is undefined--")
    print(f"Error: /undefined in {name}")
    return

    # return the value associated with name
    # What is your design decision about what to do when there is no definition for “name”? If “name” is not defined, your program should not break, but should give an appropriate error message.

#---------------------------------------------------------------------
# Arithmetic and comparison operators: add, sub, mul, div, mod, eq, lt, gt
# Make sure to check the operand stack has the correct number of parameters
# and types of the parameters are correct.
def add():
    try:
        second = opstack.pop()
        if (isinstance(second, (int, float, complex))):
            first = opstack.pop()
            if (isinstance(first, (int, float, complex))):
                sum = first + second
                opPush(sum)
            else:
                opPush(first)
                opPush(second)
        else:
            opPush(second)
    except (IndexError):
        print("Error: /stackunderflow in --add--")

def sub():
    try:
        second = opstack.pop()
        if (isinstance(second, (int, float, complex))):
            first = opstack.pop()
            if (isinstance(first, (int, float, complex))):
                difference = first - second
                opPush(difference)
            else:
                opPush(first)
                opPush(second)
        else:
            opPush(second)
    except (IndexError):
        print("Error: /stackunderflow in --sub--")

def mul():
    try:
        second = opstack.pop()
        if (isinstance(second, (int, float, complex))):
            first = opstack.pop()
            if (isinstance(first, (int, float, complex))):
                product = first * second
                opPush(product)
            else:
                opPush(first)
                opPush(second)
        else:
            opPush(second)
    except (IndexError):
        print("Error: /stackunderflow in --mul--")

def div():
    try:
        second = opstack.pop()
        if second == 0:
            raise ZeroDivisionError("Cannot divide by zero.")
        if (isinstance(second, (int, float, complex))):
            first = opstack.pop()
            if (isinstance(first, (int, float, complex))):
                quotient = first / second
                opPush(quotient)
            else:
                opPush(first)
                opPush(second)
        else:
            opPush(second)
    except (IndexError):
        print("Error: /stackunderflow in --div--")

def mod():
    try:
        second = opstack.pop()
        if (isinstance(second, (int, float, complex))):
            first = opstack.pop()
            if (isinstance(first, (int, float, complex))):
                remainder = first % second
                opPush(remainder)
            else:
                opPush(first)
                opPush(second)
        else:
            opPush(second)
    except (IndexError):
        print("Error: /stackunderflow in --mod--")

def eq():
    try:
        second = opstack.pop()
        first = opstack.pop()
        opPush(first == second)
    except (IndexError):
        print("Error: /stackunderflow in --eq--")

def lt():
    try:
        second = opstack.pop()
        first = opstack.pop()
        opPush(first < second)
    except (IndexError):
        print("Error: /stackunderflow in --lt--")

def gt():
    try:
        second = opstack.pop()
        first = opstack.pop()
        opPush(first > second)
    except (IndexError):
        print("Error: /stackunderflow in --gt--")

#---------------------------------------------------------------------
# String operators: define the string operators length, get, getinterval, put
def length():
    endItem = opPop()
    if isinstance(endItem, str):
        if endItem[0] == '(' and endItem[len(endItem) - 1] == ')':
            opPush(len(endItem) - 2)
    else:
        print("Error: /typecheck in --length--")

def get():
    index = opPop()
    if (isinstance(index, int)):
        string = opPop()
        if (isinstance(string, str) and string[0] == '(' and string[len(string) - 1] == ')'):
            string = string[1:len(string)-1]
            opPush(ord(string[index]))
        else:
            opPush(string)
            opPush(index)
    else:
        opPush(index)

def getinterval():
    size = opPop()
    if isinstance(size, int) and size >= 0:
        index = opPop()
        if isinstance(index, int):
            string = opPop()
            if (isinstance(string, str) and string[0] == '(' and string[len(string) - 1] == ')'):
                if size == index:
                    opPush(string)
                    opPush(index)
                    opPush(size)
                elif size < 0:
                    opPush(string)
                    opPush(index)
                    opPush(size)
                    print("Error: /rangecheck in --getinterval--")
                else:
                    string = string[1:len(string)-1]
                    if size <= len(string):
                        newString = string[index:index+size]
                        opPush('(' + newString + ')')
            else:
                opPush(string)
                opPush(index)
                opPush(size)
        else:
            opPush(index)
            opPush(size)
    else:
        opPush(size)

def put():
    value = opPop()
    if isinstance(value, int):
        index = opPop()
        if isinstance(index, int):
            string = opPop()
            if (isinstance(string, str) and string[0] == '(' and string[len(string) - 1] == ')'):
                if index >= (len(string) - 2) or (index < 0):
                    opPush(string)
                    opPush(index)
                    opPush(value)
                    print("Error: /stackunderflow in --put--")
                else:
                    stringID = id(string)
                    string = string[1:len(string)-1]

                    # chr is used for getting the ascii value that "value" encodes
                    if index == (len(string) - 1):
                        string = '(' + string[0:index] + chr(value) + ')'
                        updateReferences(stringID, string)
                        return
                    
                    section1 = string[:index]
                    section2 = string[index + 1:]
                    string = '(' + section1 + chr(value) + section2 + ')'
                    updateReferences(stringID, string)
            else:
                opPush(string)
                opPush(index)
                opPush(value)
        else:
            opPush(index)
            opPush(value)
    else:
        opPush(value)

def updateReferences(stringID, newString):
    # update copies in the opstack
    for index, item in enumerate(opstack): #enumerate allows for "index" to be tracked, starting at 0
        if id(item) == stringID:
            #print("EQUAL!")
            opstack[index] = newString
        else:
            continue
        
    # update copies in the dictstack
    if len(dictstack) != 0:
        dict = dictstack[len(dictstack) - 1] # retrieve the top dictionary in the stack
        for name, item in dict.items():
            if id(item) == stringID:
                dict[name] = newString
            else:
                continue

    return

#---------------------------------------------------------------------
# Define the stack manipulation and print operators: dup, copy, pop, clear, exch, roll, stack
def dup():
    item = opPop()
    duplicateItem = item
    opPush(item)
    opPush(duplicateItem)

def copy():
    amount = opPop()
    if isinstance(amount, int):
        if len(opstack) >= amount:
            stackCopy = []
            for item in opstack:
                stackCopy.append(item)

            for item in stackCopy:
                opstack.append(item)
    else:
        opPush(amount)

def pop():
    opPop()

def clear():
    opstack.clear()

def exch():
    value1 = opPop()
    value2 = opPop()
    opPush(value1)
    opPush(value2)

def roll():
    #global opstack

    occurence = opPop()
    if isinstance(occurence, int):
        location = opPop()
        if isinstance(location, int):
            if location > len(opstack):
                print("Error: /stackunderflow in --roll--")
                return
            elif location < 0:
                print("Error: /rangecheck in --roll--")
                return
            elif location == 0 or location == 1:
                return

            if occurence == 0:
                opPush(location)
                opPush(occurence)
                return
            elif occurence < 0:
                occurence = abs(occurence)
                for i in range(0,occurence):
                    itemToMove = opstack.pop(len(opstack) - location)
                    opPush(itemToMove)
                return
            else:
                for i in range(0,occurence):
                    top = opstack[-1]
                    opstack.insert(len(opstack) - location, top)
                    opPop()
                return
        else:
            opPush(location)
            opPush(occurence)
    else:
        opPush(occurence)

def stack():
    for item in reversed(opstack):
        if isinstance(item, str):
            if item[0] == '/':
                print(item[1:])
                continue
        elif isinstance(item, dict):
            print ("--nostringval--")
        elif isinstance(item, list):
            print ("--nostringval--")

        print(item)

#---------------------------------------------------------------------
# Define the dictionary manipulation operators: psDict, begin, end, psDef
# name the function for the def operator psDef because def is reserved in Python. Similarly, call the function for dict operator as psDict.
# Note: The psDef operator will pop the value and name from the opstack and call your own "define" operator (pass those values as parameters).
# Note that psDef()won't have any parameters.

def psDict():
    size = opPop()
    if isinstance(size, int):
        newDict = {}
        opPush(newDict)
    else:
        opPush(size)
        raise Exception

def begin():
    item = opPop()
    if isinstance(item, dict):
        dictPush(item)
    else:
        opPush(item)
        raise Exception

def end():
    dictPop()

def psDef():
    value = opPop()
    name = opPop()
    if isinstance(name, str) and (name[0] == '/'):
        define(name, value)

#---------------------------------------------------------------------------------

# def testAdd():
#     opPush(1)
#     opPush(2)
#     add()
#     if opPop() != 3:
#         return False
#     return True

# def testPut():
#     opPush("(This is a test _)")
#     dup()
#     opPush("/s")
#     exch()
#     psDef()
#     dup()
#     opPush(15)
#     opPush(48)
#     put()
#     if lookup("s") != "(This is a test 0)" or opPop()!= "(This is a test 0)":
#         print(False)
#     print(True)

# def main():
    #print(testAdd())

    # opPush("(CptS355)")
    # dup()
    # opPush(17)
    # opPush(53)
    # stack()
    # put()
    # print()
    # stack()

    # opPush("(A STRING TO TEST)")
    # opPush(5)
    # opPush(17)
    # opPush(3)
    # copy()
    # stack()

    # if (id(opstack[0]) == id(opstack[3])):
    #     print("THEY'RE EQUAL!!!")

    # opstack.clear()
    # opPush(1)
    # opPush(2)
    # opPush(3)
    # opPush(4)
    # opPush(2)
    # opPush(3)
    # roll()
    # print(opstack)

#main()

#testPut()
#print(convert("hhjhh"))

# p1 = parse(['/pow2', '{', '/n', 'exch', 'def', '(Pow2_of_n_is)', 'dup', '8', 'n',
#        '48', 'add', 'put', '1', 'n', '-1', '1', '{', 'pop', '2', 'mul', '}', 'for',
#        '}', 'def', '(Calculating_pow2_of_9)', 'dup', '20', 'get', '48', 'sub', 'pow2', 'stack'])

# pResult = ['/pow2', ['/n', 'exch', 'def', '(Pow2_of_n_is)', 'dup', 8, 'n', 48, 'add',
#                      'put', 1, 'n', -1, 1, ['pop', 2, 'mul'], 'for'], 'def',
#                      '(Calculating_pow2_of_9)', 'dup', 20, 'get', 48, 'sub', 'pow2', 'stack']

# if p1 == pResult:
#     print(True)
# else:
#     print(False)

# interpreter("3 4 add /x 3 def /m {2 mul} def x m")
# clear()
# interpreter("1 6 -1 1 {mul} for")
# stack()
# stack()

clear()
interpreter(input1)
print()

clear()
interpreter(input2)
print()

clear()
interpreter(input3)
print()

clear()
interpreter(input4)
print()

clear()
interpreter(input5)
print()

clear()
interpreter(input6)
print()