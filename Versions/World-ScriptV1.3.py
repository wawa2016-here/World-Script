import time
import threading
import sys

allCode = []
totalItems = 0
Vars = {}
CurrentLineData = ""
DoneWithInputCom = True
is_running = False
Printed = 0

def Run():
    global totalItems, DoneWithInputCom, is_running, Vars, Printed
    if is_running:
        return
    
    is_running = True
    DoneWithInputCom = False
    
    print("\n--- Output ---\n")
    totalItems = len(allCode)
    
    i = 0
    while i < totalItems:
        line = allCode[i].strip()

        if not line or line.strip() == "":
            i += 1
            continue

        if line.startswith('RUN_CODE'):
            continue
        if line.startswith('var '):
            parts = line[4:].split('=', 1)
            if len(parts) == 2:
                var_name = parts[0].strip()
                var_value = parts[1].strip()
                if var_value.startswith('"') and var_value.endswith('"'):
                    Vars[var_name] = var_value[1:-1]
                else:
                    Vars[var_name] = var_value
            else:
                print(f"Syntax Error: Invalid variable assignment on line {i+1}")

        elif line.startswith('say '):
            argument = line[4:].strip()
            if argument.startswith('"') and argument.endswith('"'):
                print(argument[1:-1])
            elif argument in Vars:
                print(Vars[argument])
            else:
                print(f"Syntax Error: Variable '{argument}' or missing quotes on line {i+1}")

        elif line.startswith('ask '):
            parts = line[4:].split(' to ', 1)
            if len(parts) == 2:
                prompt = parts[0].strip()
                target_var = parts[1].strip()
                if prompt.startswith('"') and prompt.endswith('"'):
                    print(prompt[1:-1], end=" ", flush=True)
                    user_response = sys.stdin.readline().strip()
                    Vars[target_var] = user_response
                else:
                    print(f"Syntax Error: Missing quotes in prompt on line {i+1}")
            else:
                if line[4:].strip().startswith('"') and line[4:].strip().endswith('"'):
                    print(line[4:].strip()[1:-1], end=" ", flush=True)
                    sys.stdin.readline()
                else:
                    print(f"Syntax Error: Invalid 'ask' command on line {i+1}")

        elif line.startswith('wait '):
            parts = line[5:].split(' to ', 1)
            if len(parts) == 2:
                prompt = parts[0].strip()
                target_var = parts[1].strip()
                if prompt.startswith('"') and prompt.endswith('"'):
                    try:
                        seconds = float(prompt[1:-1])
                        time.sleep(seconds)
                        Vars[target_var] = str(seconds)
                    except ValueError:
                        print(f"Syntax Error: 'wait' value must be a number on line {i+1}")
                else:
                    print(f"Syntax Error: Missing quotes in prompt on line {i+1}")
            else:
                fallback = line[5:].strip()
                if fallback.startswith('"') and fallback.endswith('"'):
                    try:
                        seconds = float(fallback[1:-1])
                        time.sleep(seconds)
                    except ValueError:
                        print(f"Syntax Error: 'wait' value must be a number on line {i+1}")
                else:
                    print(f"Syntax Error: Invalid 'wait' command on line {i+1}")

        elif line.startswith('var') or line.startswith('say') or line.startswith('ask') or line.startswith('wait'):
            print(f"Put a space before the quotes. On line {i+1} ERROR")

        elif line.startswith('READ_AND_RUN_FILE_'):
            filename = line[18:].strip()
            try:
                with open(filename, "r", encoding="utf-8") as f:
                    file_lines = [l.strip() for l in f.readlines()]
                
                print(f"--- Loading File: {filename} ---")
                
                allCode[i+1:i+1] = file_lines
                totalItems = len(allCode)
                i += 1
                continue
                
            except FileNotFoundError:
                print(f"Compiler Error: File '{filename}' not found.")
            except Exception as e:
                print(f"Compiler Error: Failed to read file. {e}")
        else:
            print(f"ERROR COMMAND NOT FOUND. On line {i+1}")
            
        i += 1
        
    print("\n--- EXECUTION FINISHED ---\n")
    allCode.clear()
    DoneWithInputCom = True
    is_running = False
    

def Compile():
    global CurrentLineData
    while True:
        if DoneWithInputCom:
            try:
                print(">>> ", end="", flush=True)
                CurrentLineData = sys.stdin.readline().strip()
                if CurrentLineData.strip() == 'RUN_CODE':
                    Run()
                elif CurrentLineData:
                    allCode.append(CurrentLineData)
            except EOFError:
                break
        else:
            while not DoneWithInputCom:
                time.sleep(0.05)

print("This is World-Script.V1.3")
Compile()
