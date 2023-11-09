import os 
import re
from collections import deque 

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

    i = len(file_path)-1

    #finds the file name
    while file_path[i-1] != '\\':
        i-=1
    file_name = file_path[i:]

    #loops through file at controlled rate
    line_index = 0
    it_count = 0
    while line_index < len(lines):
        line = lines[line_index]
        match = re.match(r'\s*def\s+(\w+)\(',line) #checks for function creation

        if match: 
            function_name = match.group(1) #gets name
            function_line = line_index+1 #gets line
            print_line = function_line #gets current print line

            #finding end of function declaration
            while not line.rstrip().endswith(':'):
                line = lines[print_line]
                print_line+=1
            
            #indent level
            spaces = len(lines[print_line]) - len(lines[print_line].lstrip())

            #adds indent level
            print_statement = ""
            for i in range(spaces):
                print_statement += " "
            
            print_statement += "print('| File: "+file_name+" | Function: "+function_name+" | starts at line: "+str(function_line)+"')"
            
            print_line += 1 + it_count
            add_print(file_path,print_line,print_statement)
            
            it_count+=1

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

    print("Greating Print Statements")

    #adding the print statments
    for file_path in files:
        find_functions(file_path)
    
    print("Finished")

if __name__ == "__main__":
    directory = input("Enter dir: ")
    walk(directory)
    input("\nPress any key to quit\n>>> ")