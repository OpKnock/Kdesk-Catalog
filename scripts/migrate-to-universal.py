#!/usr/bin/env python3
"""
Migrate existing agents to universal format
"""
import os
import json
import yaml
from pathlib import Path
from typing import Dict, Any, List

OLD_AGENTS_DIR = Path("agents")
OLD_SKILLS_DIR = Path("skills")
UNIVERSAL_DIR = Path("universal-agents")

CATEGORY_MAP = {
    "ml": "ml",
    "devops": "devops", 
    "database": "database",
    "api": "api",
    "security": "security",
    "monitoring": "monitoring",
    "testing": "testing",
    "sre": "sre",
    "compliance": "compliance",
    "finops": "finops",
    "networking": "networking",
    "messaging": "messaging",
    "devtools": "devtools",
    "data": "data",
    "backend": "backend",
    "frontend": "frontend",
    "mobile": "mobile",
    "infrastructure": "infrastructure",
    "cloud": "cloud",
    "code-quality": "code-quality",
    "patterns": "patterns"
}

SUBCATEGORY_MAP = {
    # ML subcategories
    "pytorch": "training",
    "tensorflow": "training", 
    "scikit-learn": "training",
    "xgboost": "training",
    "lightgbm": "training",
    "catboost": "training",
    "huggingface": "training",
    "langchain": "inference",
    "llamaindex": "inference",
    "semantic-kernel": "inference",
    "ollama": "inference",
    "vllm": "inference",
    "tgi": "inference",
    "llama-cpp": "inference",
    "mlx-lm": "inference",
    "stable-diffusion": "inference",
    "whisper": "inference",
    "mlflow": "monitoring",
    "wandb": "monitoring",
    "dvc": "monitoring",
    "dagster": "deployment",
    "prefect": "deployment",
    "kubeflow": "deployment",
    "ray": "deployment",
    "seldon": "deployment",
    "bentoml": "deployment",
    "triton": "inference",
    "torchserve": "inference",
    "openai": "inference",
    "anthropic": "inference",
    "groq": "inference",
    "mistral": "inference",
    "cohere": "inference",
    "deepseek": "inference",
    "xai": "inference",
    "pinecone": "vector-db",
    "weaviate": "vector-db",
    "qdrant": "vector-db",
    "milvus": "vector-db",
    "chroma": "vector-db",
    "elasticsearch": "vector-db",
    "opensearch": "vector-db",
    "embedding": "embedding",
    "rag": "rag",
    "agent": "agent",
    "prompt": "prompt",
    "fine-tuning": "fine-tuning",
    "evaluation": "evaluation",
    "monitoring": "monitoring",
    "governance": "governance",
    "safety": "safety",
    "privacy": "privacy",
    "fairness": "fairness",
    "explainability": "explainability",
    "compliance": "compliance",
    "risk": "risk",
    "audit": "audit",
    "validation": "validation",
    "versioning": "versioning",
    "documentation": "documentation",
    "collaboration": "collaboration",
    "communication": "communication",
    "coding": "coding",
    "project": "project",
    "innovation": "innovation",
    "exploration": "exploration",
    "creation": "creation",
    "transformation": "transformation",
    "evolution": "evolution",
    "streaming": "deployment",
    "batch": "deployment",
    "edge": "deployment",
    "embedded": "deployment",
    "hybrid": "deployment",
    "onprem": "deployment",
    "serverless": "deployment",
    "containerized": "deployment",
    "microservices": "deployment",
    "monolith": "deployment",
    "lambda": "deployment",
    "ecs": "deployment",
    "eks": "deployment",
    "gke": "deployment",
    "aks": "deployment",
    "firebase": "deployment",
    "huggingface": "deployment",
    "replicate": "deployment",
    "together": "deployment",
    "fireworks": "deployment",
    "deepseek": "deployment",
    "xai": "deployment",
    "bedrock": "deployment",
    "vertex": "deployment",
    "azure": "deployment",
    "pinecone": "deployment",
    "deploy-sdk": "deployment",
    "deploy-sdk-agent": "deployment",
}

DEFAULT_COMMANDS = {
    "ml": ["python train.py", "python infer.py", "docker run", "kubectl apply"],
    "devops": ["kubectl apply", "terraform apply", "docker build", "helm install"],
    "database": ["psql", "mysql", "mongosh", "redis-cli"],
    "api": ["curl", "httpie", "postman", "grpcurl"],
    "security": ["trivy", "gitleaks", "semgrep", "snyk"],
    "monitoring": ["prometheus", "grafana", "datadog", "jaeger"],
    "testing": ["pytest", "jest", "playwright", "k6"],
    "sre": ["kubectl", "prometheus", "alertmanager", "chaos"],
    "compliance": ["audit", "checkov", "tfsec", "kube-linter"],
    "finops": ["aws ce", "gcloud billing", "az cost", "infracost"],
    "networking": ["nginx", "haproxy", "envoy", "tc"],
    "messaging": ["kafka-topics", "rabbitmqctl", "nats", "redis-cli"],
    "devtools": ["git", "docker", "npm", "pip", "cargo"],
    "data": ["airflow", "dbt", "spark", "flink"],
    "backend": ["uvicorn", "node", "go run", "cargo run"],
    "frontend": ["npm run dev", "vite", "webpack", "esbuild"],
    "mobile": ["flutter", "xcodebuild", "gradle", "fastlane"],
    "infrastructure": ["terraform", "ansible", "packer", "helm"],
    "cloud": ["aws", "gcloud", "az", "vercel"],
    "code-quality": ["eslint", "prettier", "ruff", "black", "mypy"],
    "patterns": ["git", "editor", "terminal"]
}

def extract_category_subcategory(filepath: Path) -> tuple:
    """Extract category and subcategory from file path"""
    parts = filepath.relative_to(OLD_AGENTS_DIR).parts
    if len(parts) >= 2:
        category = parts[0]
        subcategory = parts[1].replace('.json', '').replace('-agent', '')
        return category, subcategory
    return "uncategorized", "general"

def infer_subcategory(name: str, category: str) -> str:
    """Infer subcategory from agent name"""
    name_lower = name.lower()
    
    # Check known mappings
    for key, value in SUBCATEGORY_MAP.items():
        if key in name_lower:
            return value
    
    # Category-based defaults
    defaults = {
        "ml": "inference",
        "devops": "deployment",
        "database": "management",
        "api": "development",
        "security": "scanning",
        "monitoring": "observability",
        "testing": "automation",
        "sre": "operations",
        "compliance": "audit",
        "finops": "optimization",
        "networking": "configuration",
        "messaging": "management",
        "devtools": "productivity",
        "data": "processing",
        "backend": "development",
        "frontend": "development",
        "mobile": "development",
        "infrastructure": "provisioning",
        "cloud": "management",
        "code-quality": "linting",
        "patterns": "implementation"
    }
    return defaults.get(category, "general")

def extract_commands_from_agent(agent: Dict[str, Any]) -> List[str]:
    """Extract CLI commands from agent examples and instructions"""
    commands = set()
    
    # From examples
    for ex in agent.get('examples', []):
        if isinstance(ex, str):
            # Extract command-like strings
            parts = ex.split()
            if parts and not parts[0].startswith('#'):
                cmd = parts[0]
                if not cmd.startswith('http') and not cmd.startswith('//'):
                    commands.add(ex[:100])
    
    # From instructions - look for code blocks
    instructions = agent.get('instructions', '')
    import re
    code_blocks = re.findall(r'`([^`]+)`', instructions)
    for block in code_blocks:
        if ' ' in block and not block.startswith('http'):
            commands.add(block[:100])
    
    return list(commands)[:10] if commands else DEFAULT_COMMANDS.get("ml", [])

def extract_capabilities(agent: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Extract capabilities from agent"""
    capabilities = []
    
    # Main capability from name/description
    capabilities.append({
        "name": agent.get('display_name', agent['name']).replace('-', ' ').title(),
        "description": agent.get('description', ''),
        "commands": extract_commands_from_agent(agent),
        "examples": agent.get('examples', [])[:5],
        "parameters": []
    })
    
    # Extract additional capabilities from instructions
    instructions = agent.get('instructions', '')
    if 'capabilit' in instructions.lower():
        # Try to parse capabilities from instructions
        pass
    
    return capabilities

def migrate_agent(json_path: Path) -> Dict[str, Any]:
    """Migrate single agent JSON to universal YAML"""
    with open(json_path, 'r') as f:
        agent = json.load(f)
    
    category, subcategory = extract_category_subcategory(json_path)
    category = CATEGORY_MAP.get(category, category)
    subcategory = infer_subcategory(json_path.stem, category)
    
    # Build universal agent
    universal = {
        "name": agent['name'],
        "display_name": agent['name'].replace('-', ' ').title(),
        "category": category,
        "subcategory": subcategory,
        "description": agent.get('description', ''),
        "version": "1.0.0",
        "tags": [category, subcategory] + agent.get('tags', []),
        "author": "Kdesk-Catalog",
        "license": "MIT",
        "capabilities": extract_capabilities(agent),
        "knowledge": [
            {
                "title": f"{agent['name']} Documentation",
                "type": "reference",
                "source": f"https://github.com/kdesk/agents/tree/main/agents/{category}/{subcategory}",
                "description": f"Reference documentation for {agent['name']}"
            }
        ],
        "instructions": agent.get('instructions', ''),
        "examples": agent.get('examples', [])[:10],
        "platforms": {
            "claude_code": {
                "tools": agent.get('tools', ["Bash", "Read", "Write", "Edit", "Glob", "Grep"]),
                "model": agent.get('model', "claude-3-5-sonnet-20241022")
            },
            "cursor": {
                "rule_type": "auto",
                "model": "gpt-4"
            },
            "github_copilot": {
                "prompt_file": f"{agent['name']}.md",
                "extension": "github.copilot"
            },
            "windsurf": {
                "model": "claude-3.5-sonnet",
                "tools": ["bash", "read", "write", "edit"],
                "instructions": agent.get('instructions', '')
            },
            "opencode": {
                "plugin": f"opencode-{agent['name']}"
            },
            "generic": {
                "system_prompt": f"You are {agent['name']}. {agent.get('description', '')}",
                "available_tools": ["bash", "read", "write", "edit", "glob", "grep"]
            }
        },
        "created_at": "2024-01-01T00:00:00Z",
        "updated_at": "2024-01-01T00:00:00Z"
    }
    
    return universal

def migrate_skill(md_path: Path) -> Dict[str, Any]:
    """Migrate skill markdown to universal format"""
    content = md_path.read_text()
    
    # Parse frontmatter if exists
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            frontmatter = yaml.safe_load(parts[1])
            body = parts[2].strip()
        else:
            frontmatter = {}
            body = content
    else:
        frontmatter = {}
        body = content
    
    category = md_path.parent.name
    name = md_path.stem.replace('-skill', '')
    
    universal = {
        "name": name,
        "display_name": frontmatter.get('name', name.replace('-', ' ').title()),
        "category": category,
        "subcategory": frontmatter.get('subcategory', 'general'),
        "description": frontmatter.get('description', body[:200]),
        "version": "1.0.0",
        "tags": [category] + frontmatter.get('tags', []),
        "author": "Kdesk-Catalog",
        "license": "MIT",
        "capabilities": [
            {
                "name": frontmatter.get('name', name),
                "description": frontmatter.get('description', ''),
                "commands": frontmatter.get('examples', [])[:10],
                "examples": frontmatter.get('examples', [])[:5],
                "parameters": []
            }
        ],
        "knowledge": [
            {
                "title": f"{name} Skill Documentation",
                "type": "documentation",
                "source": f"skills/{category}/{md_path.name}",
                "description": f"Complete guide for {name}"
            }
        ],
        "instructions": body,
        "examples": frontmatter.get('examples', [])[:10],
        "platforms": {
            "claude_code": {
                "tools": frontmatter.get('tools', ["Bash", "Read", "Write", "Edit"]),
                "model": frontmatter.get('model', "claude-3-5-sonnet-20241022")
            },
            "cursor": {"rule_type": "auto", "model": "gpt-4"},
            "github_copilot": {"prompt_file": f"{name}.md", "extension": "github.copilot"},
            "windsurf": {"model": "claude-3.5-sonnet", "tools": ["bash", "read", "write", "edit"]},
            "opencode": {"plugin": f"opencode-{name}"},
            "generic": {"system_prompt": f"You are an expert in {name}. {frontmatter.get('description', '')}", "available_tools": ["bash", "read", "write", "edit"]}
        },
        "created_at": "2024-01-01T00:00:00Z",
        "updated_at": "2024-01-01T00:00:00Z"
    }
    return universal

def main():
    UNIVERSAL_DIR.mkdir(parents=True, exist_ok=True)
    (UNIVERSAL_DIR / "registry.yaml").touch()
    
    print("Migrating agents...")
    agent_count = 0
    for json_path in OLD_AGENTS_DIR.rglob("*.json"):
        try:
            universal = migrate_agent(json_path)
            
            # Determine output path
            category = universal['category']
            subcategory = universal['subcategory']
            out_dir = UNIVERSAL_DIR / category / subcategory
            out_dir.mkdir(parents=True, exist_ok=True)
            
            out_path = out_dir / f"{universal['name']}.yaml"
            with open(out_path, 'w') as f:
                yaml.dump(universal, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
            
            agent_count += 1
            if agent_count % 100 == 0:
                print(f"  Migrated {agent_count} agents...")
        except Exception as e:
            print(f"Error migrating {json_path}: {e}")
    
    print(f"\nMigrated {agent_count} agents")
    
    print("\nMigrating skills...")
    skill_count = 0
    for md_path in OLD_SKILLS_DIR.rglob("*.md"):
        try:
            universal = migrate_skill(md_path)
            
            category = universal['category']
            out_dir = UNIVERSAL_DIR / category
            out_dir.mkdir(parents=True, exist_ok=True)
            
            out_path = out_dir / f"{universal['name']}-skill.yaml"
            with open(out_path, 'w') as f:
                yaml.dump(universal, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
            
            skill_count += 1
        except Exception as e:
            print(f"Error migrating skill {md_path}: {e}")
    
    print(f"Migrated {skill_count} skills")
    print(f"\nTotal: {agent_count} agents, {skill_count} skills")
    print(f"Output: {UNIVERSAL_DIR}")

if __name__ == "__main__":
    main()