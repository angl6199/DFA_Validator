states = list()
alphabet = list()
initial = ""
finalStates = list()
transitions_dic = dict()
minimized = False

def SelectFile():
    """
    docstring
    """
    filename = input("Please enter the name of the file you want to work with (include '.txt') : ")
    ReadFile(filename)

def ReadFile(filename):
    """
    docstring
    """
    global states
    global alphabet
    global initial
    global finalStates
    global transitions_dic

    with open(filename) as f_obj:
        lines = f_obj.read().splitlines()
    
    states = lines[0].split(",")
    alphabet = lines[1].split(",")
    initial = lines[2]
    finalStates = lines[3].split(",")

    for x in range(4, len(lines)):
        temp1 = lines[x].split(",")
        temp2 = temp1[1].split("=>")
        temptransition = [temp1[0], temp2[0], temp2[1]]
        if temptransition[0] in transitions_dic:
            transitions_dic[temptransition[0]].append(temptransition)
        else:
            transitions_dic[temptransition[0]] = list()
            transitions_dic[temptransition[0]].append(temptransition)
    PrintDFA()
    Menu()

def PrintDFA():
    """
    docstring
    """
    print()
    print("States: ", end="")
    for state in states:
        print(state, end=" ")
    print()
    print("Alphabet: ", end="")
    for caracter in alphabet:
        print(caracter, end=" ")
    print()
    print("Initial state: ", end="")
    print(initial)
    print("Final States: ", end="")
    for state in finalStates:
        print(state, end=" ")
    print()
    for key in transitions_dic:
        for array in transitions_dic[key]:
            print("Transition: " + array[0] + "," + array[1] + "=>" + array[2])

def Menu():
    """
    docstring
    """
    decision = 0
    while decision != 3:
        print()
        print("------------------------------------")
        print("1. Test an input")
        print("2. Minimize automata")
        print("3. Exit")
        print("------------------------------------")
        print()
        decision = int(input("Enter a number: "))

        if decision == 1:
            test_input = str(input("Please enter the string to validate in the DFA: "))
            TestInput(test_input)
        if decision == 2:
            if minimized:
                print("The DFA is already minimized")
            else:
                MinimizeDFA()
        if decision == 3:
            print("Come back soon!")

def TestInput(test_input):
    """
    docstring
    """
    if ValidateInput(test_input):
        if MakeTransitions(test_input, initial):
            print("String is accepted")
        else:
            print("String is not accepted")
    else:
        print("Not valid input")

def ValidateInput(test_input):
    """
    docstring
    """
    counter = 0
    for caracter in test_input:
        for sym in alphabet:
            if caracter == sym:
                counter += 1
    
    if counter == len(test_input):
        return True
    else:
        return False

def MakeTransitions(test_input, actual_state):
    """
    docstring
    """
    if test_input == "":
        for state in finalStates:
            if actual_state == state:
                print(actual_state + " is a final state")
                return True
        print(actual_state + " is not a final state")
        return False
    else:
        temp = test_input[0]
        if actual_state in transitions_dic:
            for arrays in transitions_dic[actual_state]:
                if arrays[1] == temp:
                    print(actual_state + "," + temp + "=>" + arrays[2])
                    actual_state = arrays[2]
                    return MakeTransitions(test_input[1:], actual_state)
            print(actual_state + "," + temp + "=>Sink State")
            return False
        print(actual_state + " is a Sink State")
        return False

def MinimizeDFA():
    """
    docstring
    """
    global states
    global finalStates
    global transitions_dic
    global minimized

    var = CheckPairOfEntries() 
    stateToDelete = ""
    if  var == None:
        minimized = True
        PrintDFA()
    else:
        if var[1] != initial:
            stateToDelete = var[1]
            stateToSave = var[0]
        else:
            stateToDelete = var[0]
            stateToSave = var[1]
        states.remove(stateToDelete)
        if stateToDelete in finalStates:
            finalStates.remove(stateToDelete)
        del transitions_dic[stateToDelete]
        for key in transitions_dic:
            for array in transitions_dic[key]:
                for x in range(0, len(array)):
                    if array[x] == stateToDelete:
                        array[x] = stateToSave 
        MinimizeDFA()

def CheckPairOfEntries():
    """
    docstring
    """
    for x in range(0, len(states)-1):
        for y in range(x+1, len(states)):
            temp1 = transitions_dic[states[x]]
            temp2 = transitions_dic[states[y]]
            if Equivalence(temp1, temp2):
                var = [temp1[0][0], temp2[0][0]]
                return var
    
    return None
                        
def Equivalence(temp1, temp2):
    """
    docstring
    """
    if len(temp1) == len(temp2):
        for z in range(0, len(temp1)):
            if temp1[z][1] != temp2[z][1] or temp1[z][2] != temp2[z][2]:
                return False
        counter = 0
        for state in finalStates:
            if temp1[0][0] == state or temp2[0][0] == state:
                counter += 1
        if counter == 2 or counter == 0:
            return True
    else:
        return False
                        
SelectFile()