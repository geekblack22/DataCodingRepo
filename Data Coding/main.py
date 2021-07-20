import pandas as pd 
import numpy as np
import collections

problem = pd.read_excel(r'C:\Users\yveder\Documents\2nd_set.xlsx')
start = pd.DataFrame(problem, columns=['start_state']).to_numpy()
goal = pd.DataFrame(problem, columns=['goal_state']).to_numpy()
expresion = pd.DataFrame(problem, columns=['expression']).to_numpy()

#start_equation = "5.255+32+49*15+32+9-5+9+9"
start_equation = str(start[1]).lstrip('[').rstrip(']')
start_equation_list = list(start_equation)

equation = str(expresion[1]).lstrip('[').rstrip(']')
equation_list = list(equation)

goal_eq = str(goal[27]).lstrip('[').rstrip(']')
goal_list = list(goal_eq)
def add_to_before(arr,index,type):
    before = ""
    
    for i in range(index-1,-1,-1):

        if (not arr[i].isnumeric() and arr[i] != '.'):
           if(type == "plus" or type == "minus"):
                if(arr[i] == '*' or arr[i] == '/'):
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
def add_to_after(arr,index,type):
    after = ""
    for i in range(index+1,len(arr),1):
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
def removeDuplicates(str,arr):
    
    duplicates = [item for item, count in collections.Counter(arr).items() if count > 1]
    
    #print(duplicates)
    
    duplicate_arr = [None]*len(duplicates)
  
    for i in range(len(duplicates)):
        duplicate = 0
        for j in range(len(arr)):
            if(arr[j] == duplicates[i]):
                duplicate +=1
            
        duplicate_arr[i] = duplicate
  
    
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
        if(start_equation_list[i] == '*'):
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
        if(start_equation_list[i] == '/'):
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
    return removeDuplicates(start_equation,add), removeDuplicates(start_equation,sub), removeDuplicates(start_equation,multi),removeDuplicates(start_equation,div)                
def remove_non_numeric(arr):
     for i in range(len(arr)):
         if( not arr[i].isnumeric()):
             arr.pop(i)
     return arr
def remove_duplicates(arr):
    res = []
    for i in arr:
        if i not in res:
            res.append(i)
    return res
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
def operation_is_calc(opp_list, start, express):
        start_count = 0
        express_count = 0
        for i in range(len(opp_list)):
            
            if(start.find(opp_list[i])  != -1):
                start_count += 1
            if(express.find(opp_list[i])  != -1):
                express_count += 1
        print(start_count)
        print(express_count)
        return express_count != 0 and express_count != start_count


#add = remove_non_numeric(add)
add, sub, multi, div = store_operation_list(start_equation)
is_multi = operation_is_calc(create_multi_list(multi), start_equation,equation)
is_add = operation_is_calc(create_add_list(add), start_equation,equation)
print(is_add)
print(create_multi_list(multi))
print(is_multi)
f = 32.0

