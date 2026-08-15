#!/usr/bin/env python3
"""
Fix remaining 9 agents with truncated JSON in instructions
"""
import os
import json

PATH = "platform-agents/claude_code"

# The 9 problematic files
problematic = [
    'authentication.json',
    'graphql-subscription.json',
    'graphql-v2.json',
    'grpc-v2.json',
    'hypermedia.json',
    'rest-v2.json',
    'rest.json',
    'twirp.json',
    'webhook.json'
]

fixed = 0
for f in problematic:
    path = os.path.join(PATH, f)
    if os.path.exists(path):
        with open(path) as fp:
            data = json.load(fp)
        
        # Use description as instructions
        data['instructions'] = data.get('description', 'Expert in ' + data.get('name', 'this domain') + '. Use real CLI commands.')
        
        with open(path, 'w') as fp:
            json.dump(data, fp, indent=2)
        fixed += 1
        print('Fixed: ' + f)

print('Fixed ' + str(fixed) + ' agents')