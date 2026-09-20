---
trigger: glob
description: "Operates AWS services with the AWS CLI: EC2, S3, IAM, Lambda, EKS, and CloudWatch across accounts and regions."
globs: ["**/*.json", "**/*.r", "**/*.sh"]
---

# aws

Operates AWS services with the AWS CLI: EC2, S3, IAM, Lambda, EKS, and CloudWatch across accounts and regions.

## Instructions

# AWS

Operate AWS with the official CLI.

## When to Use

- Managing S3, EC2, Lambda, EKS, and IAM
- Deploying and debugging serverless functions
- Cluster access for EKS
- Automation and scripted infrastructure checks

## Configuration

```bash
aws configure
aws configure --profile prod
export AWS_PROFILE=prod
aws sts get-caller-identity
```

## Commands

```bash
# S3
aws s3 ls
aws s3 cp file.txt s3://my-bucket/
aws s3 sync ./dist s3://my-bucket/ --delete

# EC2
aws ec2 describe-instances --query "Reservations[*].Instances[*].[InstanceId,State.Name]"
aws ec2 describe-instances --filters Name=instance-state-name,Values=running

# Lambda
aws lambda list-functions
aws lambda invoke --function-name myfunc --payload "{}" out.json
aws lambda update-function-code --function-name myfunc --zip-file fileb://func.zip
aws logs tail /aws/lambda/myfunc --follow

# EKS
aws eks update-kubeconfig --name my-cluster --region us-east-1
aws eks list-clusters
kubectl get nodes
```

## Best Practices

- Use named profiles and never hardcode credentials
- Prefer IAM roles over long-lived keys (instance profiles, OIDC)
- Add --query and --output table for readable scripts
- Pin the CLI version in CI and test with --dryrun
- Enable CloudTrail to audit CLI and SDK actions
- Always scope S3 policies and IAM policies to least privilege

## Capabilities

### aws-core
Manage core AWS resources from the CLI.

**Commands:**
- `aws s3 ls`
- `aws s3 cp file.txt s3://my-bucket/`
- `aws ec2 describe-instances --query "Reservations[*].Instances[*].[InstanceId,State.Name]"`
- `aws ec2 describe-regions`
- `aws sts get-caller-identity`

**Examples:**
- aws s3 sync ./dist s3://my-bucket/ --delete
- aws ec2 describe-instances --filters Name=instance-state-name,Values=running --query "Reservations[*].Instances[*].PublicIpAddress"
- aws iam list-users --output table

### aws-serverless
Deploy and manage Lambda functions.

**Commands:**
- `aws lambda list-functions --region us-east-1`
- `aws lambda invoke --function-name myfunc --payload "{}" out.json`
- `aws lambda update-function-code --function-name myfunc --zip-file fileb://func.zip`
- `aws logs tail /aws/lambda/myfunc`
- `aws logs describe-log-groups`

**Examples:**
- aws lambda invoke --cli-binary-format raw-in-base64-out --function-name myfunc --payload "{\"key\":\"v\"}" out.json
- aws logs tail /aws/lambda/myfunc --follow
- aws lambda get-function-configuration --function-name myfunc

### aws-kubernetes
Manage EKS clusters and kubeconfigs.

**Commands:**
- `aws eks update-kubeconfig --name my-cluster --region us-east-1`
- `aws eks list-clusters`
- `aws eks describe-cluster --name my-cluster --query "cluster.status"`
- `kubectl get nodes`

**Examples:**
- aws eks update-kubeconfig --name my-cluster --alias prod
- aws eks list-nodegroups --cluster-name my-cluster
