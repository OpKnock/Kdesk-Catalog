#!/usr/bin/env python3
"""
Fix universal YAML instructions - extract from JSON
"""
import os
import yaml
import json

UNIVERSAL_DIR = "universal-agents"

def extract_first_json(text):
    """Extract the first complete JSON object from text"""
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

def fix_universal():
    fixed = 0
    for root, dirs, files in os.walk(UNIVERSAL_DIR):
        for f in files:
            if f.endswith('.yaml') and f != 'registry.yaml':
                path = os.path.join(root, f)
                try:
                    with open(path) as fp:
                        data = yaml.safe_load(fp)
                except:
                    continue
                
                instr = data.get('instructions', '')
                if instr.strip().startswith('{'):
                    try:
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
                                yaml.dump(data, fp, default_flow_style=False, sort_keys=False, allow_unicode=True)
                            fixed += 1
                    except:
                        pass
    print('Fixed ' + str(fixed) + ' universal agents')

if __name__ == '__main__':
    fixed = 0
    for root, dirs, files in os.walk(UNIVERSAL_DIR):
        for f in files:
            if f.endswith('.yaml') and f != 'registry.yaml':
                path = os.path.join(root, f)
                try:
                    with open(path) as fp:
                        data = yaml.safe_load(fp)
                except:
                    continue
                
                instr = data.get('instructions', '')
                if instr.strip().startswith('{'):
                    try:
                        # Extract first complete JSON object
                        depth = 0
                        in_string = False
                        escape = False
                        end_pos = 0
                        
                        for i, ch in enumerate(instr):
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
                            json_str = instr[:end_pos]
                            parsed = json.loads(json_str)
                            
                            if 'instructions' in parsed:
                                data['instructions'] = parsed['instructions']
                            elif 'description' in parsed:
                                data['instructions'] = parsed['description']
                            else:
                                data['instructions'] = data.get('description', '')
                            
                            with open(path, 'w') as fp:
                                yaml.dump(data, fp, default_flow_style=False, sort_keys=False, allow_unicode=True)
                            fixed += 1
                    except:
                        pass
    
    print('Fixed ' + str(fixed) + ' universal agents')