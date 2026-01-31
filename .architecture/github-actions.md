# GitHub Actions Orchestration

## Overview

GitHub Actions workflows for multi-repository coordination and CI/CD.

> **Note:** This is a SPECIFICATION. Actual workflow files go in `.github/workflows/` when implementing.

---

## Workflow Categories

### 1. Specification Validation

Validate that specification files are properly formatted.

```yaml
# .github/workflows/validate-spec.yml
name: Validate Specification

on:
  pull_request:
    paths:
      - '**/*.md'
      - '**/*.yaml'
      - '**/*.yml'

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Validate YAML
        run: |
          find . -name "*.yml" -o -name "*.yaml" | while read f; do
            python -c "import yaml; yaml.safe_load(open('$f'))"
          done
          
      - name: Check Markdown Links
        uses: gaurav-nelson/github-action-markdown-link-check@v1
        
      - name: Lint Markdown
        uses: DavidAnson/markdownlint-cli2-action@v14
```

### 2. Schema Validation

Ensure BigQuery schemas are valid.

```yaml
# .github/workflows/validate-schemas.yml
name: Validate BigQuery Schemas

on:
  pull_request:
    paths:
      - '.architecture/logging.md'
      - '**/bigquery/**'

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          
      - name: Install dependencies
        run: pip install google-cloud-bigquery
        
      - name: Validate schemas
        run: python scripts/validate_schemas.py
```

### 3. Documentation Generation

Auto-generate documentation from specifications.

```yaml
# .github/workflows/generate-docs.yml
name: Generate Documentation

on:
  push:
    branches: [main]
    paths:
      - '**/*.md'

jobs:
  docs:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Generate command index
        run: python scripts/generate_command_index.py
        
      - name: Update README
        run: python scripts/update_readme.py
        
      - name: Commit changes
        uses: stefanzweifel/git-auto-commit-action@v5
        with:
          commit_message: "docs: auto-update documentation"
```

---

## Multi-Repository Coordination

When this template is used to spawn multiple businesses:

### Template Repository (ceoOpenSpec)

```yaml
# On release, notify spawned repositories
name: Template Update Notification

on:
  release:
    types: [published]

jobs:
  notify:
    runs-on: ubuntu-latest
    steps:
      - name: Notify spawned repos
        run: |
          # List of repositories spawned from this template
          REPOS=$(cat .spawned-repos.txt)
          
          for repo in $REPOS; do
            gh workflow run update-from-template.yml \
              --repo $repo \
              --field template_version=${{ github.event.release.tag_name }}
          done
        env:
          GH_TOKEN: ${{ secrets.REPO_ACCESS_TOKEN }}
```

### Spawned Repository

```yaml
# .github/workflows/update-from-template.yml
name: Update from Template

on:
  workflow_dispatch:
    inputs:
      template_version:
        description: 'Template version to update from'
        required: true

jobs:
  update:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Fetch template updates
        run: |
          git remote add template https://github.com/[org]/ceoOpenSpec.git
          git fetch template ${{ inputs.template_version }}
          
      - name: Create update PR
        run: |
          git checkout -b update-template-${{ inputs.template_version }}
          # Merge non-customized files only
          git checkout template/${{ inputs.template_version }} -- \
            .architecture/*.md \
            */README.md
          git commit -m "chore: update from template ${{ inputs.template_version }}"
          
      - name: Create Pull Request
        uses: peter-evans/create-pull-request@v6
        with:
          title: "Update from template ${{ inputs.template_version }}"
          body: |
            Template ceoOpenSpec has been updated to version ${{ inputs.template_version }}.
            
            This PR brings in non-customized specification files.
            Review carefully before merging.
```

---

## Agent Deployment Workflows

### Deploy Agent (Template)

```yaml
# .github/workflows/deploy-agent.yml
name: Deploy Agent

on:
  workflow_dispatch:
    inputs:
      agent:
        description: 'Agent to deploy (CEO, CFO, CMO, etc.)'
        required: true
        type: choice
        options: [CEO, CFO, CMO, COO, CIO, CLO, CPO, CTO, EXA]
      environment:
        description: 'Deployment environment'
        required: true
        type: choice
        options: [staging, production]

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: ${{ inputs.environment }}
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Google Cloud
        uses: google-github-actions/setup-gcloud@v2
        with:
          project_id: ${{ secrets.GCP_PROJECT_ID }}
          
      - name: Authenticate
        uses: google-github-actions/auth@v2
        with:
          credentials_json: ${{ secrets.GCP_SA_KEY }}
          
      - name: Deploy to Cloud Functions
        run: |
          gcloud functions deploy ${{ inputs.agent }}-agent \
            --gen2 \
            --runtime python311 \
            --region us-central1 \
            --source ./implementations/${{ inputs.agent }} \
            --entry-point handler \
            --trigger-topic ${{ inputs.agent }}-topic \
            --set-env-vars ENVIRONMENT=${{ inputs.environment }}
```

### Deploy All Agents

```yaml
# .github/workflows/deploy-all.yml
name: Deploy All Agents

on:
  workflow_dispatch:
    inputs:
      environment:
        description: 'Deployment environment'
        required: true
        type: choice
        options: [staging, production]

jobs:
  deploy:
    strategy:
      matrix:
        agent: [CEO, CFO, CMO, COO, CIO, CLO, CPO, CTO, EXA]
        
    uses: ./.github/workflows/deploy-agent.yml
    with:
      agent: ${{ matrix.agent }}
      environment: ${{ inputs.environment }}
    secrets: inherit
```

---

## Scheduled Workflows

### Daily Health Check

```yaml
# .github/workflows/health-check.yml
name: Daily Health Check

on:
  schedule:
    - cron: '0 8 * * *'  # 8 AM UTC daily

jobs:
  health:
    runs-on: ubuntu-latest
    steps:
      - name: Check all agents
        run: |
          AGENTS="CEO CFO CMO COO CIO CLO CPO CTO EXA"
          for agent in $AGENTS; do
            curl -f https://[region]-[project].cloudfunctions.net/${agent}-health || exit 1
          done
          
      - name: Notify on failure
        if: failure()
        run: |
          # Send alert to Telegram
          curl -X POST "https://api.telegram.org/bot${BOT_TOKEN}/sendMessage" \
            -d "chat_id=${CHAT_ID}" \
            -d "text=🔴 Agent health check failed!"
```

### Weekly Backup Verification

```yaml
# .github/workflows/backup-verify.yml
name: Weekly Backup Verification

on:
  schedule:
    - cron: '0 2 * * 0'  # 2 AM UTC every Sunday

jobs:
  verify:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Run backup verification
        run: python scripts/verify_backups.py
        
      - name: Report results
        run: python scripts/backup_report.py
```

---

## Repository Secrets Required

| Secret | Description | Used By |
|--------|-------------|---------|
| `GCP_PROJECT_ID` | GCP project identifier | All deployments |
| `GCP_SA_KEY` | Service account JSON | GCP authentication |
| `REPO_ACCESS_TOKEN` | GitHub PAT for cross-repo | Multi-repo coordination |
| `TELEGRAM_BOT_TOKEN` | Bot token | Notifications |
| `TELEGRAM_CHAT_ID` | Chat for alerts | Notifications |

---

## Branch Protection

Recommended branch protection rules:

```yaml
# .github/settings.yml (if using probot/settings)
branches:
  - name: main
    protection:
      required_status_checks:
        strict: true
        contexts:
          - validate
          - lint
      required_pull_request_reviews:
        required_approving_review_count: 1
      restrictions: null
      enforce_admins: true
```

---

*Automate the boring stuff. Keep specifications valid. Deploy with confidence.*
