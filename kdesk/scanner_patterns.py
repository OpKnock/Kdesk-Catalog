"""Expanded secret scanner patterns for cloud credentials, tokens, and keys."""

SECRET_PATTERNS = [
    # Cloud providers
    ("aws_access_key", r"AKIA[0-9A-Z]{16}", "AWS Access Key ID"),
    ("aws_secret_key", r"(?i)aws.{0,20}?['\"][0-9a-zA-Z/+]{40}['\"]", "AWS Secret Key"),
    ("gcp_api_key", r"AIza[0-9A-Za-z\-_]{35}", "Google API Key"),
    ("gcp_service_account", r"-----BEGIN PRIVATE KEY-----\s*eyJ", "GCP Service Account Key"),
    ("azure_storage_key", r"(?i)AccountKey=[0-9a-zA-Z+/=]{88}", "Azure Storage Account Key"),
    ("azure_connection_string", r"(?i)DefaultEndpointsProtocol=https;.*?AccountKey=", "Azure Connection String"),

    # AI provider keys
    ("openai_api_key", r"sk-[a-zA-Z0-9]{48}", "OpenAI API Key"),
    ("openai_project_key", r"sk-proj-[a-zA-Z0-9\-_]{56}", "OpenAI Project Key"),
    ("anthropic_api_key", r"sk-ant-[a-zA-Z0-9\-_]{80,}", "Anthropic API Key"),
    ("google_ai_studio", r"AIzaSy[a-zA-Z0-9\-_]{33}", "Google AI Studio Key"),
    ("huggingface_token", r"hf_[a-zA-Z0-9]{34}", "HuggingFace Token"),

    # Generic API keys
    ("api_key_bearer", r"(?i)bearer\s+[a-zA-Z0-9\-_\.]{30,}", "Bearer Token"),
    ("generic_api_key", r"(?i)(api[_-]?key|apikey)\s*[=:]\s*['\"][a-zA-Z0-9\-_]{32,}['\"]", "Generic API Key"),
    ("secret_assignment", r"(?i)(secret|token|password|passwd|pwd)\s*[=:]\s*['\"][^\s'\"]{12,}['\"]", "Secret Assignment"),

    # Tokens
    ("github_pat", r"ghp_[a-zA-Z0-9]{36}", "GitHub Personal Access Token"),
    ("github_oauth", r"gho_[a-zA-Z0-9]{36}", "GitHub OAuth Token"),
    ("github_app", r"ghs_[a-zA-Z0-9]{36}", "GitHub App Token"),
    ("gitlab_pat", r"glpat-[a-zA-Z0-9\-_]{20}", "GitLab PAT"),
    ("slack_bot_token", r"xoxb-[0-9]{10,13}-[0-9]{10,13}-[a-zA-Z0-9]{24}", "Slack Bot Token"),
    ("slack_user_token", r"xoxp-[0-9]{10,13}-[0-9]{10,13}-[a-zA-Z0-9]{24}", "Slack User Token"),
    ("discord_bot_token", r"(?i)discord.*['\"][a-zA-Z0-9]{50,}['\"]", "Discord Bot Token"),
    ("npm_token", r"npm_[a-zA-Z0-9]{36}", "NPM Token"),
    ("pypi_token", r"pypi-AgEIcHlwaS5vcmc[a-zA-Z0-9\-_]+", "PyPI Upload Token"),
    ("stripe_secret", r"[sk|rk]_live_[0-9a-zA-Z]{24}", "Stripe Secret Key"),
    ("twilio_sid", r"AC[a-zA-Z0-9]{32}", "Twilio Account SID"),
    ("sendgrid_key", r"SG\.[a-zA-Z0-9\-_]{22}\.[a-zA-Z0-9\-_]{43}", "SendGrid API Key"),

    # Private keys
    ("private_key_rsa", r"-----BEGIN RSA PRIVATE KEY-----", "RSA Private Key"),
    ("private_key_ec", r"-----BEGIN EC PRIVATE KEY-----", "EC Private Key"),
    ("private_key_generic", r"-----BEGIN PRIVATE KEY-----", "Private Key"),
    ("ssh_private_key", r"-----BEGIN OPENSSH PRIVATE KEY-----", "SSH Private Key"),

    # Database
    ("database_url", r"(?i)(postgres|mysql|mongodb|redis|amqp)://[^\s:@]+:[^\s@]+@[^\s]+", "Database Connection String"),
    ("jdbc_url_with_creds", r"jdbc:\w+://[^\s:]+:[0-9]+/.*?[?&]password=", "JDBC URL with Password"),

    # JWT
    ("jwt_token", r"eyJ[A-Za-z0-9\-_]+\.eyJ[A-Za-z0-9\-_]+\.[A-Za-z0-9\-_]*", "JWT Token"),

    # Webhook
    ("webhook_url_slack", r"https://hooks\.slack\.com/services/T[A-Za-z0-9]+/B[A-Za-z0-9]+/[a-zA-Z0-9]+", "Slack Webhook URL"),
]
