#!/usr/bin/env python3
"""
Fix JSON strings in claude_code instructions - extract actual instructions from JSON with extra data
"""
import os
import json
import re

PATH = "platform-agents/claude_code"

def fix_instructions():
    fixed = 0
    for f in os.listdir(PATH):
        if f.endswith('.json'):
            path = os.path.join(PATH, f)
            with open(path) as fp:
                data = json.load(fp)
            
            instr = data.get('instructions', '')
            if instr.strip().startswith('{'):
                # Try to extract the first complete JSON object
                try:
                    # Find the end of the first JSON object
                    depth = 0
                    in_string = False
                    escape = False
                    end_pos = 0
                    
                    for i, ch in enumerate(instr):
                        if escape:
                            escape = False
                            continue
                        if ch == '\\':
                            escape = True
                            continue
                        if ch == '"' and not escape:
                            in_string = not in_string
                        if not in_string:
                            if ch == '{':
                                depth += 1
                            elif ch == '}':
                                depth -= 1
                                if depth == 0:
                                    end_pos = i + 1
                                    break
                    
                    if end_pos > 0:
                        json_str = instr[:end_pos]
                        parsed = json.loads(json_str)
                        
                        # Extract the actual instructions
                        if 'instructions' in parsed:
                            data['instructions'] = parsed['instructions']
                        elif 'description' in parsed:
                            data['instructions'] = parsed['description']
                        else:
                            data['instructions'] = data.get('description', '')
                        
                        with open(path, 'w') as fp:
                            json.dump(data, fp, indent=2)
                        fixed += 1
                        print('Fixed: ' + f)
                except Exception as e:
                    print('Error fixing ' + f + ': ' + str(e))
    
    print('Fixed ' + str(fixed) + ' agents')

if __name__ == '__main__':
    fixed = 0
    for f in os.listdir(PATH):
        if f.endswith('.json'):
            path = os.path.join(PATH, f)
            with open(path) as fp:
                data = json.load(fp)
            
            instr = data.get('instructions', '')
            if instr.strip().startswith('{'):
                # Try to extract the first complete JSON object
                try:
                    # Find the end of the first JSON object
                    depth = 0
                    in_string = False
                    escape = False
                    end_pos = 0
                    
                    for i, ch in enumerate(instr):
                        if escape:
                            escape = False
                            continue
                        if ch == '\\':
                            escape = True
                            continue
                        if ch == '"' and not escape:
                            in_string = not in_string
                        if not in_string:
                            if ch == '{':
                                depth += 1
                            elif ch == '}':
                                depth -= 1
                                if depth == 0:
                                    end_pos = i + 1
                                    break
                    
                    if end_pos > 0:
                        json_str = instr[:end_pos]
                        parsed = json.loads(json_str)
                        
                        # Extract the actual instructions
                        if 'instructions' in parsed:
                            data['instructions'] = parsed['instructions']
                        elif 'description' in parsed:
                            data['instructions'] = parsed['description']
                        else:
                            data['instructions'] = data.get('description', '')
                        
                        with open(path, 'w') as fp:
                            json.dump(data, fp, indent=2)
                        fixed += 1
                        print('Fixed: ' + f)
                except Exception as e:
                    print('Error fixing ' + f + ': ' + str(e))
    
    print('Fixed ' + str(fixed) + ' agents')