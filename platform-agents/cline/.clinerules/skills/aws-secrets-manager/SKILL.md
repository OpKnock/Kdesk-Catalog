---
name: "aws-secrets-manager"
description: "Manages secrets in AWS Secrets Manager: creation, retrieval, rotation, versioning, and deletion with the AWS CLI."
---

# Aws Secrets Manager

Manages secrets in AWS Secrets Manager: creation, retrieval, rotation, versioning, and deletion with the AWS CLI.

## Instructions

# AWS Secrets Manager

## What this skill does

Manages secrets in AWS Secrets Manager: creating secrets from JSON, retrieving current/previous versions, rotating with Lambda, generating strong passwords, and enforcing IAM access.

## When to use

- Storing DB credentials, API keys, and tokens centrally
- Rotating credentials automatically or manually
- Auditing which services can read a secret

## Real commands

```bash
# Create a secret
aws secretsmanager create-secret --name prod/api-db --secret-string '{"user":"admin","pass":"x"}' --tags Key=env,Value=prod

# Retrieve
aws secretsmanager get-secret-value --secret-id prod/api-db --query SecretString --output text | jq .

# Rotate the value
aws secretsmanager put-secret-value --secret-id prod/api-db --secret-string '{"user":"admin","pass":"rotated"}'

# Read the previous version
aws secretsmanager get-secret-value --secret-id prod/api-db --version-stage AWSPREVIOUS

# Generate a strong password
aws secretsmanager get-random-password --password-length 32 --exclude-punctuation | jq -r .RandomPassword

# Schedule rotation
aws secretsmanager rotate-secret --secret-id prod/api-db --rotation-lambda-arn arn:aws:lambda:us-east-1:111122223333:function:rotate
```

## Testing

- Verify version stages with list-secret-version-ids
- Test rollback by reading AWSPREVIOUS after a bad rotation

## Best practices

- Use IAM policies scoped to individual secrets
- Enable automatic rotation for database passwords
- Use get-random-password instead of hand-rolled generation
- Schedule deletion (no force) during transitions so secrets can be restored

## Capabilities

### secret-lifecycle
Create, retrieve, list, and delete secrets.

**Commands:**
- `aws secretsmanager create-secret --name prod/api-db --secret-string '{"user":"admin","pass":"x"}'`
- `aws secretsmanager get-secret-value --secret-id prod/api-db`
- `aws secretsmanager list-secrets`
- `aws secretsmanager delete-secret --secret-id prod/api-db --force-delete-without-recovery`
- `aws secretsmanager restore-secret --secret-id prod/api-db`

**Examples:**
- aws secretsmanager create-secret --name prod/api-db --secret-string '{"user":"admin","pass":"secret123"}' --tags Key=env,Value=prod
- aws secretsmanager get-secret-value --secret-id prod/api-db --query SecretString --output text | jq .
- aws secretsmanager list-secrets --query 'SecretList[].{name:Name,last:LastChangedDate}' --output table

### rotation-versioning
Manage secret versions and rotation.

**Commands:**
- `aws secretsmanager put-secret-value --secret-id prod/api-db --secret-string '{"user":"admin","pass":"new"}'`
- `aws secretsmanager rotate-secret --secret-id prod/api-db --rotation-lambda-arn arn:aws:lambda:us-east-1:111122223333:function:rotate`
- `aws secretsmanager describe-secret --secret-id prod/api-db`
- `aws secretsmanager list-secret-version-ids --secret-id prod/api-db`
- `aws secretsmanager get-secret-value --secret-id prod/api-db --version-stage AWSPREVIOUS`

**Examples:**
- aws secretsmanager put-secret-value --secret-id prod/api-db --secret-string "$(aws secretsmanager get-secret-value --secret-id prod/api-db --query SecretString --output text | jq '.pass="rotated"')"
- aws secretsmanager describe-secret --secret-id prod/api-db | jq '.RotationRules'
- aws secretsmanager get-secret-value --secret-id prod/api-db --version-stage AWSPREVIOUS --query SecretString --output text

### iam-access
Grant and verify cross-account/service access to secrets.

**Commands:**
- `aws secretsmanager get-random-password --password-length 32 --exclude-punctuation`
- `aws secretsmanager get-random-password --password-length 20 --require-each-included-type`
- `aws iam put-role-policy --role-name api-role --policy-name secret-read --policy-document file://policy.json`
- `aws secretsmanager describe-secret --secret-id prod/api-db --query 'Tags'`

**Examples:**
- aws secretsmanager get-random-password --password-length 32 --exclude-punctuation --exclude-numbers | jq -r .RandomPassword
- aws iam put-role-policy --role-name api-role --policy-name secret-read --policy-document '{"Version":"2012-10-17","Statement":[{"Effect":"Allow","Action":["secretsmanager:GetSecretValue"],"Resource":"arn:aws:secretsmanager:us-east-1:111122223333:secret:prod/api-db-*"}]}'
- aws secretsmanager get-random-password --password-length 40
