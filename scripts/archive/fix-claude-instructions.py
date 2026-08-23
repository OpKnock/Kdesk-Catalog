#!/usr/bin/env python3
"""
Fix JSON strings in claude_code instructions - extract actual instructions from JSON
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
                    parsed = json.loads(instr)
                    # Extract the actual instructions
                    if 'instructions' in parsed:
                        data['instructions'] = parsed['instructions']
                    elif 'description' in parsed:
                        data['instructions'] = parsed['description']
                    else:
                        # Fallback: use description
                        data['instructions'] = data.get('description', '')
                    
                    with open(path, 'w') as fp:
                        json.dump(data, fp, indent=2)
                    fixed += 1
                    print('Fixed: ' + f)
                except Exception as e:
                    print('Error fixing ' + f + ': ' + str(e))
    
    print('Fixed ' + str(fixed) + ' agents')

if __name__ == '__main__':
    fix_instructions()