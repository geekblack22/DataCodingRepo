import pandas as pd 
import numpy as np
import collections

problem = pd.read_excel(r'C:\Users\yveder\Documents\2nd_set.xlsx')
start = pd.DataFrame(problem, columns=['start_state']).to_numpy()
goal = pd.DataFrame(problem, columns=['goal_state']).to_numpy()
expresion = pd.DataFrame(problem, columns=['expression']).to_numpy()

#start_equation = "5.255+32+49*15+32+9-5+9+9"
#store the equations from the excel sheet as strings
 
 #start_equation_list = list(start_equation)
#equation = str(expresion[1]).lstrip('[').rstrip(']')
# equation_list = list(equation)

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
    
    #print(duplicates)
    
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
           ## if(i == len(start_equation) - 2):
               # if(start_equation[i+2].isnumeric()):
               #    add.append(start_equation[i+2] + start_equation[i+1])
               # if(start_equation[i-2].isnumeric()):
                #   add.append(start_equation[i-1] + start_equation[i-2])
                    
              #       add.append(add_to_before(start_equation,i))
                #     add.append(add_to_after(start_equation,i))
               # else:
                  # add.append(start_equation[i-1])
                 #  add.append(start_equation[i+1])
           # else:
              #      if(i - 2 > -1):
                    #     add.append(add_to_before(start_equation,i,"plus"))
                   #      add.append(add_to_after(start_equation,i,"plus"))
                         
                        ##if(start_equation[i-2].isnumeric()):
                           ## add.append(start_equation[i-2] + start_equation[i-1])
                       ## else:
                         ##   add.append(start_equation[i-1])
                        ##if(start_equation[i+2].isnumeric()):
                            ##add.append(start_equation[i+1] + start_equation[i+2])
                       ## else:
                            ##add.append(start_equation[i+1])
        if(start_equation[i] == '-'):
             
              if(add_to_after(start_equation,i,"minus") != ""):
                   sub.append(add_to_after(start_equation,i,"minus"))
              if(add_to_before(start_equation,i,"minus") != ""):
                   add.append(add_to_before(start_equation,i,"minus"))
            # if(i == len(start_equation) - 2):
            #     if(start_equation[i-2].isnumeric()):
            #         add.append(start_equation[i-1] + start_equation[i-2])
            #         add.append(start_equation[i-1])
            #     else:
            #         add.append(start_equation[i-1])
            #         add.append(start_equation[i+1])
            # else:
            #     if(start_equation[i+2] != '*' or start_equation[i+2] != '/' ):
            #         if(i - 2 > -1):
            #             if(start_equation[i-2].isnumeric()):
            #                 add.append(start_equation[i-2] + start_equation[i-1])
            #             else:
            #                 add.append(start_equation[i-1])
            #             if(start_equation[i+2].isnumeric()):
            #                 add.append(start_equation[i+1] + start_equation[i+2])
            #             else:
            #                 add.append(start_equation[i+1])            
        if(start_equation[i] == '*'):
            if(add_to_before(start_equation,i,"multi") != ""):
                   multi.append(add_to_before(start_equation,i,"multi"))
            if(add_to_after(start_equation,i,"multi") != ""):
                   multi.append(add_to_after(start_equation,i,"multi"))
            # if(i == len(start_equation) - 2):
            #          if(start_equation[i-2] != '/'):
            #             if(start_equation[i-2].isnumeric()):
            #                 multi.append(start_equation[i-2] + start_equation[i-1])
            #                 multi.append(start_equation[i+1])
            #             else:
            #                 multi.append(start_equation[i-1])
            #                 multi.append(start_equation[i+1])
            # else:    
            #         if(start_equation[i-2] != '/'):
            #             if(i - 2 > -1):
            #                 if(start_equation[i-2].isnumeric()):
            #                     multi.append(start_equation[i-2] + start_equation[i-1])
            #                 else:
            #                     multi.append(start_equation[i-1])
            #                 if(start_equation[i+2].isnumeric()):
            #                     multi.append(start_equation[i+1] + start_equation[i+2])
            #                 else:
            #                     multi.append(start_equation[i+1])
        if(start_equation[i] == '/'):
            if(add_to_before(start_equation,i,"div") != ""):
                   div.append(add_to_before(start_equation,i,"div"))
            if(add_to_after(start_equation,i,"div") != ""):
               div.append(add_to_after(start_equation,i,"div"))
            # if(i == len(start_equation) - 2):
            #          if(start_equation[i-2] != '*'):
            #             if(start_equation[i-2].isnumeric()):
            #                 div.append(start_equation[i-2] + start_equation[i-1])
            #                 div.append(start_equation[i+1])
            #             else:
            #                 div.append(start_equation[i-1])
            #                 div.append(start_equation[i+1])
            # else:    
            #         if(start_equation[i-2] != '*'):
            #             if(i - 2 > -1):
            #                 if(start_equation[i-2].isnumeric()):
            #                     div.append(start_equation[i-2] + start_equation[i-1])
            #                 else:
            #                     div.append(start_equation[i-1])
            #                 if(start_equation[i+2].isnumeric()):
            #                     div.append(start_equation[i+1] + start_equation[i+2])
            #                 else:
            #                     div.append(start_equation[i+1])    
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
        start_count = 0
        express_count = 0
        different = False
        for i in range(len(opp_list)):
            if(start.find(opp_list[i])  == -1) and (express.find(opp_list[i])  != -1):
                different = True
            if(start.find(opp_list[i])  != -1):
                start_count += 1
            if(express.find(opp_list[i])  != -1):
                express_count += 1
        print(different)
        return express_count != 0  and (express_count != start_count  or different) and len(express) < len(start)


#add = remove_non_numeric(add)
response = []
for i in range(len(start)):
    start_equation = str(start[i]).lstrip('[').rstrip(']')


    equation = str(expresion[i]).lstrip('[').rstrip(']')
    is_multi = False
    is_add = False
    is_sub = False
    is_div = False
    add, sub, multi, div = store_operation_list(start_equation)
    if(not (create_multi_list(multi) is None)):
        is_multi = operation_is_calc(create_multi_list(multi), start_equation,equation)
    if(not (create_add_list(add) is None)):
        is_add = operation_is_calc(create_add_list(add), start_equation,equation)
    if(not (create_sub_list(sub,add) is None)):
        is_sub =  operation_is_calc(create_sub_list(sub,add), start_equation,equation)
    if(not (create_div_list(div) is None)):
        is_div = operation_is_calc(create_div_list(div), start_equation,equation)
    if(is_div or is_add or is_multi or is_sub):
        response.append("CALC")
    else:
        response.append("N/A")
start_equation = str(start[32]).lstrip('[').rstrip(']')
equation = str(expresion[32]).lstrip('[').rstrip(']')
add, sub, multi, div = store_operation_list(start_equation)   
#print(create_sub_list(sub,add))

print(response)
#print(len(response))

