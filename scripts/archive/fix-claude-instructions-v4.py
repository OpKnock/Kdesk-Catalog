#!/usr/bin/env python3
"""
Fix claude_code instructions - properly extract from JSON with extra markdown data
"""
import os
import json

PATH = "platform-agents/claude_code"

def extract_first_json(text):
    """Extract the first complete JSON object from text that may have extra data after"""
    depth = 0
    in_string = False
    escape = False
    
    for i, ch in enumerate(text):
        if ch == '\\' and not escape:
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
                    return text[:i+1]
    return None

def fix_instructions():
    fixed = 0
    for f in os.listdir(PATH):
        if f.endswith('.json'):
            path = os.path.join(PATH, f)
            with open(path) as fp:
                data = json.load(fp)
            
            instr = data.get('instructions', '')
            if instr.strip().startswith('{'):
                try:
                    # Extract first complete JSON object
                    json_str = extract_first_json(instr)
                    if json_str:
                        parsed = json.loads(json_str)
                        
                        if 'instructions' in parsed:
                            data['instructions'] = parsed['instructions']
                        elif 'description' in parsed:
                            data['instructions'] = parsed['description']
                        else:
                            data['instructions'] = data.get('description', '')
                        
                        with open(path, 'w') as fp:
                            json.dump(data, fp, indent=2)
                        fixed += 1
                except Exception as e:
                    pass  # Skip errors
    
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
                try:
                    # Extract first complete JSON object
                    depth = 0
                    in_string = False
                    escape = False
                    end_pos = 0
                    
                    for i, ch in enumerate(data.get('instructions', '')):
                        if ch == '\\' and not escape:
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
                        json_str = data['instructions'][:end_pos]
                        parsed = json.loads(json_str)
                        
                        if 'instructions' in parsed:
                            data['instructions'] = parsed['instructions']
                        elif 'description' in parsed:
                            data['instructions'] = parsed['description']
                        else:
                            data['instructions'] = data.get('description', '')
                        
                        with open(path, 'w') as fp:
                            json.dump(data, fp, indent=2)
                        fixed += 1
                except Exception as e:
                    pass
    
    print('Fixed ' + str(fixed) + ' agents')