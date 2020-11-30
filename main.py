states = list()
alphabet = list()
initial = ""
finalStates = list()
transitions = list()
transitions_dic = dict()

def SelectFile():
    """
    docstring
    """
    filename = input("Please enter the name of the file you want to work with (include '.txt') :")
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
    Menu()

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
            pass
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

    pass

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
                        
SelectFile()