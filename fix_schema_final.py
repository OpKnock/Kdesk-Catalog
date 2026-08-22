import os
import yaml

def fix_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = yaml.safe_load(f)
        
        if not content:
            return False
            
        modified = False
        
        # Fix capabilities - add examples and parameters
        caps = content.get('capabilities', [])
        for cap in caps:
            if 'examples' not in cap:
                subcat = content.get('subcategory', '')
                cap['examples'] = [f'{subcat}-cli --help', f'{subcat}-api --help']
                modified = True
            if 'parameters' not in cap:
                cap['parameters'] = []
                modified = True
        
        # Fix instructions
        inst = content.get('instructions', '')
        if len(str(inst)) < 200:
            cat = content.get('category', '')
            subcat = content.get('subcategory', '')
            content['instructions'] = f"""You are a {content.get('category', '')} {subcat} specialist. Provide expert guidance on {subcat} topics.

Core workflow:
1. Analyze requirements and constraints
2. Design solutions following best practices
3. Implement with proper testing and validation
4. Document and maintain solutions

Key behaviors:
- Always validate inputs and assumptions
- Follow industry best practices and standards
- Consider scalability, security, and maintainability
- Document decisions and trade-offs

Output: Expert guidance, code examples, architecture diagrams, and implementation plans."""
            modified = True
        
        # Add top-level examples if missing
        if 'examples' not in content:
            subcat = content.get('subcategory', '')
            content['examples'] = [f'{subcat}-cli --help', f'{subcat}-api --help']
            modified = True
        
        if modified:
            with open(filepath, 'w', encoding='utf-8') as f:
                yaml.dump(content, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
            return True
        return False
    except Exception as e:
        print(f'Error processing {filepath}: {e}')
        return False

def main():
    fixed = 0
    for root_dir, dirs, files in os.walk(r'C:\Users\wagde\Kdesk-Catalog\universal-agents'):
        for f in files:
            if f.endswith('.yaml') and f != 'registry.yaml':
                path = os.path.join(root_dir, f)
                if fix_file(os.path.join(root_dir, f)):
                    print(f'Fixed: {os.path.relpath(os.path.join(root_dir, f), r"C:\\Users\\wagde\\Kdesk-Catalog\\universal-agents")}')
                    fixed += 1
    print(f'Fixed {fixed} files')

if __name__ == '__main__':
    main()