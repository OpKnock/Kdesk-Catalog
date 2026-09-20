---
type: agent_requested
description: "Defines AWS infrastructure as code with the AWS CDK: init, synth, diff, deploy, and destroy. Use when working with aws cdk, devops or when the user mentions aws cdk, devops."
---

Defines AWS infrastructure as code with the AWS CDK: init, synth, diff, deploy, and destroy.

## Agentic Workflow: Read -> Reason -> Act (cdk)

You are **cdk** (devops/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — devops context for `cdk`
- Domain: Defines AWS infrastructure as code with the AWS CDK: init, synth, diff, deploy, and destroy.
- **aws-cdk**: Manage CDK apps across their full lifecycle — `cdk init app --language typescript`
- Check `knowledge` and `prerequisites: cdk`

### 2. Reason — think for `cdk`
- For `aws-cdk`: Manage CDK apps across their full lifecycle — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `cdk` tools
- Tools: `Glob`, `Grep`, `Read`, `Cdk` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `cdk:a313a8ed`

# AWS CDK

Infrastructure as code with real programming languages: construct stacks, synth
CloudFormation, deploy with diff verification.

## When to Use

- Building infrastructure as versioned code
- Reusable stack patterns across environments
- Reviewable, testable infra changes

## Real Commands

```bash
# Scaffold
sudo cdk init app --language typescript

# Bootstrap the account/region (once)
sudo cdk bootstrap aws://ACCOUNT_ID/eu-west-1

# Synthesize CloudFormation
sudo cdk synth
sudo cdk synth MyStack

# Preview changes
sudo cdk diff

# Deploy
sudo cdk deploy --all --require-approval never
sudo cdk deploy MyStack --context env=prod

# Lists stacks
sudo cdk list

# Destroy
sudo cdk destroy --all --force
```

## Example Stack (lib/my-stack.ts)

```ts
import * as s3 from 'aws-cdk-lib/aws-s3';

export class MyStack extends Stack {
  constructor(scope: Construct, id: string, props: StackProps) {
    super(scope, id, props);
    new s3.Bucket(this, 'Bucket', {
      bucketName: `app-assets-${this.account}`,
      versioned: true,
    });
  }
}
```

## Best Practices

- Use environments (accounts/regions) as context per stack
- Review `cdk diff` in PRs, not just deploy
- Prefer L2 constructs and escape hatches for customization
- Add tests with assertions on the synthesized template
- Bootstrap once per account/region with a dedicated role

## Example Response

Synthesizes the app, diffs against the live account, deploys, and reports the
created resources with their ARNs.

## Capabilities

### aws-cdk
Manage CDK apps across their full lifecycle

**Parameters:**
- `language` (string): App language: typescript, python, java, go
- `require-approval` (string): Deploy approval: never, any-change, broadening
- `context` (string): Context values, e.g. env=prod

**Commands:**
- `cdk init app --language typescript`
- `cdk bootstrap aws://ACCOUNT_ID/eu-west-1`
- `cdk synth`
- `cdk diff`
- `cdk deploy --all --require-approval never`

**Examples:**
- cdk list
- cdk deploy MyStack --context env=prod
- cdk destroy --all --force

## References
- [AWS CDK docs](https://docs.aws.amazon.com/cdk/v2/guide/home.html)
- [CDK CLI reference](https://docs.aws.amazon.com/cdk/v2/guide/cli.html)