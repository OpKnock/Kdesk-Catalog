#!/usr/bin/env python3
"""
Fix skill descriptions in universal agents
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
                with open(path) as fp:
                    data = yaml.safe_load(fp)
                
                desc = data.get('description', '')
                if desc.strip().startswith('{') and 'name' in desc:
                    # Try to extract from the JSON
                    try:
                        import json
                        parsed = json.loads(desc)
                        if 'description' in parsed:
                            data['description'] = parsed['description']
                        else:
                            data['description'] = parsed.get('name', 'Skill')
                        with open(path, 'w') as fp:
                            yaml.dump(data, fp, default_flow_style=False, sort_keys=False, allow_unicode=True)
                        fixed += 1
                        print(f"Fixed: {path}")
                    except Exception as e:
                        print(f"Error fixing {path}: {e}")
    
    print(f"Fixed {fixed} skill descriptions")

if __name__ == "__main__":
    from pathlib import Path
    fix_skill_descriptions()