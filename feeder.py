import os 
import re
from collections import deque 

ADD_CLOSING = False

def calculate_indent_level(line) -> int:
    return len(line) - len(line.lstrip())

def is_line_function(line):
    match = re.match(r'\s*def\s+(\w+)\(',line) #checks for function creation
    if not match:
        match = re.match(r'\s*async\s*def\s+(\w+)\(',line)
    
    if match:
        return match
    else:
        return None

def is_line_return(line):
    line_match = re.match(r'\s*return',line)
    if not line_match:
        line_match = re.match(r'\s*pass',line)

    return line_match

#addes the print statement based off given line
def add_print(file_path, line_num, print_statment):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    lines.insert(line_num - 1, f"{print_statment}\n")

    with open(file_path, 'w') as file:
        file.writelines(lines)

def find_functions(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    end_bound = len(file_path)-1

    #finds the file name
    while file_path[end_bound-1] != '\\':
        end_bound-=1
    file_name = file_path[end_bound:]

    #loops through file at controlled rate
    line_index = 0
    it_count = 0
    while line_index < len(lines):
        line = lines[line_index]
        match = is_line_function(line)

        if match: 
            function_name = match.group(1) #gets name
            function_line = line_index+1 #gets line
            print_line = function_line #gets current print line

            #finding end of function declaration
            while not line.rstrip().endswith(':'):
                line = lines[print_line]
                print_line+=1
            
            end_line_index = print_line #store so we can loop through function

            #indent level
            function_indent_level = calculate_indent_level(lines[print_line])
            #adds indent level
            function_spacing = ""
            for i in range(function_indent_level):
                function_spacing += " "

            print_statement = function_spacing+"print('| File: "+file_name+" | Function: "+function_name+" | starts at line: "+str(function_line + it_count)+"')"
            
            print_line += 1 + it_count
            add_print(file_path,print_line,print_statement)

            it_count += 1

            #checks to see if we should add closing 
            if not ADD_CLOSING:
                line_index+=1
                continue

            last_vaild_index = end_line_index
            hit_return = False
            inside_comment = False
            added_print = False

            while end_line_index < len(lines): #until EOF (end of function)
                #check for out of bounds
                curr_line = lines[end_line_index]
                curr_indent_level = calculate_indent_level(lines[end_line_index])                    

                #checking if we are inside comments
                if not inside_comment and (curr_line.lstrip()[:3]=="'''" or curr_line.lstrip()[:3]=='"""'):
                    inside_comment = True
                    end_line_index+=1
                    continue

                #checks if we got out of comment
                elif inside_comment and (curr_line.rstrip()[-3:]=="'''" or curr_line.rstrip()[-3:]=='"""'):
                    inside_comment = False
                    end_line_index+=1
                    continue
                #if we are inside comment keep going
                elif inside_comment:
                    end_line_index+=1
                    last_vaild_index = end_line_index
                    continue

                #check if we reach EOF
                if len(curr_line.lstrip()) > 0 and curr_indent_level < function_indent_level:
                    if not hit_return:
                        end_print_statment = "print('| File: "+file_name+" | Function: "+function_name+" | ends at line: "+str(last_vaild_index+it_count+2)+"')"
                        add_print(file_path,last_vaild_index+it_count+2,function_spacing+end_print_statment)
                        added_print = True
                        it_count+=1

                    break
                
                #checks if we are hitting blanks
                if len(curr_line.lstrip()) > 0:
                    last_vaild_index = end_line_index
                
                line_match = is_line_return(curr_line)

                if line_match:
            
                    #calculating spacing of current line
                    curr_spacing = ""
                    if curr_indent_level != function_indent_level:
                        for i in range(curr_indent_level):
                            curr_spacing += " "
                    else:
                        curr_spacing = function_spacing

                    added_print = True
                    end_print_statment = "print('| File: "+file_name+" | Function: "+function_name+" | ends at line: "+str(end_line_index+it_count+1)+"')"
                    add_print(file_path,end_line_index+it_count+1,curr_spacing+end_print_statment)
                    it_count+=1
                    hit_return = True

                end_line_index+=1

            if not added_print: #checks if we reached end of file 
                end_print_statment = "print('| File: "+file_name+" | Function: "+function_name+" | ends at line: "+str(last_vaild_index+it_count+2)+"')"
                add_print(file_path,last_vaild_index+it_count+2,function_spacing+end_print_statment)

        line_index+=1

def walk(path_dir):
    curr_root = path_dir
    files = []
    sub_dir = deque()

    sub_dir.append(path_dir)

    if len(sub_dir) <= 0:
        print("Error No Files in Directory")
        return

    while len(sub_dir) > 0:
        #print("\n\nCurrent Directory: "+sub_dir[0])

        for name in os.listdir(sub_dir[0]):
            curr_root = sub_dir[0] #current route
            file_path = os.path.join(curr_root,name) #make the file path

            if os.path.isfile(file_path):
                #print("File: "+name)
                if name[-3:] == '.py': #checks if it's a python file
                    files.append(file_path)
            else:
                #print("Dir: "+name)
                sub_dir.append(file_path) #appends the next directory 

        sub_dir.popleft()

    print("Creating Print Statements")

    #adding the print statments
    for file_path in files:
        find_functions(file_path)
    
    print("Finished")

if __name__ == "__main__":
    directory = input("Enter dir: ")

    if int(input("1. Only add Start Statments.\n2. Add End Of Function Statements (buggy).\n>>> ")) == 2:
        ADD_CLOSING = True

    walk(directory)
    input("\nPress any key to quit\n>>> ")