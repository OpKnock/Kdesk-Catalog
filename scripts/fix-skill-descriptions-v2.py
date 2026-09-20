#!/usr/bin/env python3
"""
Fix skill descriptions by setting default descriptions
"""
import os
import yaml
from pathlib import Path

UNIVERSAL_DIR = Path("universal-agents")

def fix_skill_descriptions():
    fixed = 0
    for root, dirs, files in os.walk(UNIVERSAL_DIR):
        for f in files:
            if f.endswith('-skill.yaml'):
                path = os.path.join(root, f)
                try:
                    with open(path) as fp:
                        data = yaml.safe_load(fp)
                except Exception as e:
                    print(f"Error loading {path}: {e}")
                    continue
                
                desc = data.get('description', '')
                if desc.strip().startswith('{'):
                    # Set a default description based on the name
                    name = data.get('name', 'Skill')
                    data['description'] = f"{data.get('display_name', name)} - {data.get('category', 'general')} skill for {name.replace('-', ' ')} operations."
                    
                    with open(path, 'w') as fp:
                        yaml.dump(data, fp, default_flow_style=False, sort_keys=False, allow_unicode=True)
                    fixed += 1
                    print(f"Fixed: {path}")
    
    print(f"Fixed {fixed} skill descriptions")

if __name__ == "__main__":
    fix_skill_descriptions()