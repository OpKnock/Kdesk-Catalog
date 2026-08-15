#!/usr/bin/env python3
"""
Fix claude_code instructions - properly extract from JSON with extra data
"""
import os
import json

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
                try:
                    # Parse the full JSON (it may have extra data after)
                    # The instructions field contains a JSON string that was the original
                    # agent's instructions field, which itself was a JSON string
                    parsed = json.loads(instr)
                    
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
                    if fixed % 50 == 0:
                        print('Fixed: ' + str(fixed))
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
                try:
                    parsed = json.loads(instr)
                    
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
                    print('Error fixing ' + f + ': ' + str(e))
    
    print('Fixed ' + str(fixed) + ' agents')