#!/usr/bin/env python3
"""
Fix remaining 10 universal skills with truncated JSON
"""
import os
import yaml

problematic = [
    'universal-agents/api/authentication-skill.yaml',
    'universal-agents/api/caching-skill.yaml',
    'universal-agents/api/graphql-subscription-skill.yaml',
    'universal-agents/api/graphql-v2-skill.yaml',
    'universal-agents/api/grpc-v2-skill.yaml',
    'universal-agents/api/hypermedia-skill.yaml',
    'universal-agents/api/rest-skill.yaml',
    'universal-agents/api/rest-v2-skill.yaml',
    'universal-agents/api/twirp-skill.yaml',
    'universal-agents/api/webhook-skill.yaml'
]

fixed = 0
for path in problematic:
    if os.path.exists(path):
        with open(path) as fp:
            data = yaml.safe_load(fp)
        
        data['instructions'] = data.get('description', 'Expert in ' + data.get('name', 'this domain') + '. Use real CLI commands.')
        
        with open(path, 'w') as fp:
            yaml.dump(data, fp, default_flow_style=False, sort_keys=False, allow_unicode=True)
        fixed += 1
        print('Fixed: ' + path)

print('Fixed ' + str(fixed) + ' skills')