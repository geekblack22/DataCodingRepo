import pandas as pd 
import numpy as np
import collections
import re

# read in excel files
problem = pd.read_excel(r'coding_results_world1.xlsx')
# convert to dataframes
start = pd.DataFrame(problem, columns=['start_state']).to_numpy()
goal = pd.DataFrame(problem, columns=['goal_state']).to_numpy()
expresion = pd.DataFrame(problem, columns=['expression']).to_numpy()
test_data =  pd.DataFrame(problem, columns=['MATH_\nSTRATEGIES']).to_numpy()


# strip goal equations and put them in single list
goal_eq = str(goal[27]).lstrip('[').rstrip(']')
goal_list = list(goal_eq)

#store number that appears before the operation symbol
def add_to_before(arr,index,type):
    before = ""
    for i in range(index-1,-1,-1):
        #break out of the loop if another operation symbol is reached
        if (not arr[i].isnumeric() and arr[i] != '.'):
           if(type == "plus"):
                if(arr[i] == '*' or arr[i] == '/'):
                    before = ""
                    break
                else:
                    break
           if( type == "minus"):
                if(arr[i] == '*' or arr[i] == '/' or arr[i] == '-'):
                    before = ""
                    break
                else:
                    break
           if(type == "multi"):
                if(arr[i] == '/'):
                    before = ""
                    break
                else:
                    break
           if(type == "div"):
                if(arr[i] == '*'):
                    before = ""
                    break
                else:
                    break
           
        else:
            before+=arr[i]
    before = before[::-1]
    return before

#store number that appears after the operation symbol
def add_to_after(arr,index,type):
    after = ""
    for i in range(index+1,len(arr),1):
        #break out of the loop if another operation symbol is reached
        if (not arr[i].isnumeric() and arr[i] != '.'):
            if(type == "plus" or type == "minus"):
                if(arr[i] == '*' or arr[i] == '/'):
                    after = ""
                    break
        
                else:
                    break
            else:
                    break
        else:
            after+=arr[i]
    return after

#check if single digit numbers are over counted and correct
def removeAditional(str,num, val):
    for i in range(len(str)):
        if(str[i] == val): 
            if(i-1 > -1):
                if(str[i -1].isnumeric()):
                    num -= 1
            
            if(i+1 < len(str)):
                if(str[i +1].isnumeric()):
                    num -= 1    
    return num

#remove number from operation list if it appears it iis accidently recored multiple times
def removeDuplicates(str,arr):
    #store all duplicates in an array
    duplicates = [item for item, count in collections.Counter(arr).items() if count > 1]
    duplicate_arr = [None]*len(duplicates)
    #store how many times a duplicate appears
    for i in range(len(duplicates)):
        duplicate = 0
        for j in range(len(arr)):
            if(arr[j] == duplicates[i]):
                duplicate +=1         
        duplicate_arr[i] = duplicate
    #remove duplicates that were not in the original equation 
    for i in range(len(duplicates)):
        original_num = removeAditional(str,str.count(duplicates[i]),duplicates[i])
        if(original_num < duplicate_arr[i]):
            limit = duplicate_arr[i] - original_num
            removed = 0
            for j in range(len(arr)):
                if(limit != 0):
                    for j in range(len(arr)):
                        if(removed == limit):
                            break
                        if(arr[j] == duplicates[i]):
                            arr.pop(j)
                            removed += 1
    return arr    

# remove non-numeric characters
def remove_non_numeric(arr):
     for i in range(len(arr)):
         if(not arr[i].isnumeric()):
             arr.pop(i)
     return arr

#store numbers in their respective operations list
def store_operation_list(start_equation):
    multi = []
    sub = []
    add = []
    div = []
    for i in range(len(start_equation)):
        if(start_equation[i] == '+'):
                if(add_to_before(start_equation,i,"plus") != ""):
                    add.append(add_to_before(start_equation,i,"plus"))
                if(add_to_after(start_equation,i,"plus") != ""):
                    add.append(add_to_after(start_equation,i,"plus"))
         
        if(start_equation[i] == '-'):
             
              if(add_to_after(start_equation,i,"minus") != ""):
                   sub.append(add_to_after(start_equation,i,"minus"))
              if(add_to_before(start_equation,i,"minus") != ""):
                   add.append(add_to_before(start_equation,i,"minus"))
                    
        if(start_equation[i] == '*'):
            if(add_to_before(start_equation,i,"multi") != ""):
                   multi.append(add_to_before(start_equation,i,"multi"))
            if(add_to_after(start_equation,i,"multi") != ""):
                   multi.append(add_to_after(start_equation,i,"multi"))
        
        if(start_equation[i] == '/'):
            if(add_to_before(start_equation,i,"div") != ""):
                   div.append(add_to_before(start_equation,i,"div"))
            if(add_to_after(start_equation,i,"div") != ""):
               div.append(add_to_after(start_equation,i,"div"))
             
    return remove_non_numeric(removeDuplicates(start_equation,add)), remove_non_numeric(removeDuplicates(start_equation,sub)), remove_non_numeric(removeDuplicates(start_equation,multi)),remove_non_numeric(removeDuplicates(start_equation,div))               

#remove duplicates from list of all possible operation list
def remove_duplicates(arr):
    res = []
    for i in arr:
        if i not in res:
            res.append(i)
    return res

#create list of all possible combinations from addition
def create_add_list(arr):
        add_vals = []
        for i in range(len(arr)):
            for j in range(len(arr)):
                if(j != i):
                    val = float(arr[i])+float(arr[j])
                    if(val.is_integer()):
                        val = int(val)
                    add_vals.append(str(val))
        return remove_duplicates(add_vals)

#create list of all possible combinations from multiplication
def create_multi_list(arr):
        multi_vals = []
        for i in range(len(arr)):
            for j in range(len(arr)):
                if(j != i):
                    val = float(arr[i])*float(arr[j])
                    if(val.is_integer()):
                        val = int(val)
                    multi_vals.append(str(val))
        return remove_duplicates(multi_vals)

#create list of all possible combinations from subtraction
def create_sub_list(arr,arr2):
        sub_vals = []
        for i in range(len(arr)):
            for j in range(len(arr)):
                if(j != i):
                    val = float(arr[i])+float(arr[j])
                    if(val.is_integer()):
                        val = int(val)
                    sub_vals.append(str(val))
        for i in range(len(arr)):
            for j in range(len(arr2)):
                val = float(arr2[j])-float(arr[i])
                if(val.is_integer()):
                    val = int(val)
                sub_vals.append(str(val))
            return remove_duplicates(sub_vals)

# create list of all possible combinations from division
def create_div_list(arr):
        div_vals = []
        for i in range(len(arr)):
            for j in range(len(arr)):
                if(j != i):
                    val = float(arr[i])/float(arr[j])
                    if(val.is_integer()):
                        val = int(val)
                    div_vals.append(str(val))
            return remove_duplicates(div_vals)

#check if an operation was performed
def operation_is_calc(opp_list, start, express):
        start = start.strip("\'")
        express = express.strip("\'")
        start = re.split('\+|-|\*| /', start)
        express = re.split('\+|-|\*| /', express)
        start_count = 0
        express_count = 0
        different = False
        for i in range(len(opp_list)):
            start_count += start.count(opp_list[i])
            express_count += express.count(opp_list[i])
            if not different:
                different = (start.count(opp_list[i]) == 0 and express.count(opp_list[i]) != 0)
            # if(start_count  == 0) and (express_count  > 0):
            #     different = True
           
        return start_count < express_count or different

response = []
for i in range(len(start)):
    start_equation = str(start[i]).lstrip('[').rstrip(']')

    equation = str(expresion[i]).lstrip('[').rstrip(']')
    # is_multi = False
    # is_add = False
    # is_sub = False
    # is_div = False
    add, sub, multi, div = store_operation_list(start_equation)
    # if(not (create_multi_list(multi) is None)):
    #     is_multi = operation_is_calc(create_multi_list(multi), start_equation,equation)
    if(not (create_add_list(add) is None)):
        is_add = operation_is_calc(create_add_list(add), start_equation,equation)
    # if(not (create_sub_list(sub,add) is None)):
    #     is_sub =  operation_is_calc(create_sub_list(sub,add), start_equation,equation)
    # if(not (create_div_list(div) is None)):
    #     is_div = operation_is_calc(create_div_list(div), start_equation,equation)
    if (is_add):
        response.append("CALC")
    else:
        response.append("N/A")
#start_equation = str(start[32]).lstrip('[').rstrip(']')
#equation = str(expresion[32]).lstrip('[').rstrip(']')
add, sub, multi, div = store_operation_list(start_equation)   
#print(create_sub_list(sub,add))
response = np.asarray(response)
count = 0
calc_count = 0
for i in range(len(response)):
    strat = response[i]
    test_strat = test_data[i]
    test_strat = str(test_strat).lstrip('[').rstrip(']')
    test_strat = str(test_strat).lstrip(''' ' ''').rstrip(''' ' ''')
    if test_strat == "CALC":
        calc_count += 1
    if test_strat == strat and test_strat == "CALC":
        # print('Yay')
        count += 1

    elif test_strat != strat and test_strat == "CALC": 
        print("Expected: " + test_strat + "\t" + "Actual: " + strat)
        print("Start: " + str(start[i]).lstrip('[').rstrip(']'))
        print("Expression: " + str(expresion[i]).lstrip('[').rstrip(']'))

# test_data = str(test_data[1]).lstrip('[').rstrip(']')

# print accuracy of code
print("Accuracy:" + str( (count/float(calc_count)) * 100))

# print("---------------------\n ---------------------")
print(test_data)
print(response)

