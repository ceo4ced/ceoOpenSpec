# OpenSpec Quick Start Guide

Get up and running with OpenSpec in under 5 minutes.

## What is OpenSpec?

OpenSpec is a CLI tool that helps you and your AI coding assistants agree on specifications before writing code. It provides a lightweight workflow for spec-driven development with no API keys required.

## Installation

### Step 1: Install the CLI

```bash
npm install -g @fission-ai/openspec@latest
```

Verify installation:
```bash
openspec --version
```

### Step 2: Initialize in Your Project

Navigate to your project:
```bash
cd my-project
```

Initialize OpenSpec:
```bash
openspec init
```

**What happens:**
- Creates an `openspec/` directory with your project structure
- Configures slash commands for your AI tools (if you selected any)
- Generates `AGENTS.md` instructions for AI assistants

## Your First Change

Let's walk through creating a simple feature using OpenSpec.

### 1. Ask Your AI to Create a Proposal

Tell your AI assistant:

```
Create an OpenSpec change proposal for adding a user profile page
```

Or use the shortcut (if your tool supports it):
```
/openspec:proposal Add user profile page
```

**Your AI will create:**
```
openspec/changes/add-user-profile/
├── proposal.md    # Why and what changes
├── tasks.md       # Implementation checklist
└── specs/
    └── profile/
        └── spec.md # Requirements and scenarios
```

### 2. Review the Proposal

Check what was created:
```bash
openspec list                      # See all active changes
openspec show add-user-profile     # View the full proposal
```

Validate the spec format:
```bash
openspec validate add-user-profile
```

### 3. Refine the Specs

Iterate with your AI:
```
Can you add acceptance criteria for editing the profile?
```

Your AI will update the specs. Validate again when done:
```bash
openspec validate add-user-profile
```

### 4. Implement the Change

Once the specs look good:
```
The specs look good. Let's implement this change.
```

Or use the shortcut:
```
/openspec:apply add-user-profile
```

Your AI will work through the tasks, implementing the feature according to the agreed specs.

### 5. Archive the Completed Change

After implementation and testing:
```bash
openspec archive add-user-profile --yes
```

**What happens:**
- The change moves to `openspec/changes/archive/`
- Spec updates are merged into `openspec/specs/`
- Your source of truth is updated

## Essential Commands

```bash
# View active changes
openspec list

# View existing specs
openspec list --specs

# Show details of a change or spec
openspec show <name>

# Validate a change
openspec validate <name>

# Validate all changes
openspec validate

# Archive a completed change
openspec archive <change-id> --yes

# Interactive dashboard
openspec view
```

## Common Workflows

### Starting a New Feature

1. Create proposal: `/openspec:proposal <feature-name>`
2. Review: `openspec show <feature-name>`
3. Validate: `openspec validate <feature-name>`
4. Implement: `/openspec:apply <feature-name>`
5. Archive: `openspec archive <feature-name> --yes`

### Modifying Existing Functionality

1. Check current spec: `openspec show <capability-name> --type spec`
2. Create change proposal that modifies the spec
3. Follow the same workflow as above

### Working with Multiple Changes

```bash
# List all active work
openspec list

# Check for conflicts
openspec show change-1
openspec show change-2

# Archive in the right order
openspec archive change-1 --yes
openspec archive change-2 --yes
```

## AI Tool Integration

### Native Slash Commands

These tools have built-in OpenSpec support:

| Tool | Commands |
|------|----------|
| **Cursor** | `/openspec-proposal`, `/openspec-apply`, `/openspec-archive` |
| **GitHub Copilot** | `/openspec-proposal`, `/openspec-apply`, `/openspec-archive` |
| **Windsurf** | `/openspec-proposal`, `/openspec-apply`, `/openspec-archive` |
| **Claude Code** | `/openspec:proposal`, `/openspec:apply`, `/openspec:archive` |
| ...and many more | See [README.md](README.md#supported-ai-tools) for full list |

### AGENTS.md Compatible

These tools automatically read `openspec/AGENTS.md`:
- Amp
- Jules
- Others supporting the [AGENTS.md convention](https://agents.md/)

Just ask them to follow the OpenSpec workflow!

## Troubleshooting

### "Command not found" after installation

```bash
# Verify installation
npm list -g @fission-ai/openspec

# Try reinstalling
npm uninstall -g @fission-ai/openspec
npm install -g @fission-ai/openspec@latest
```

### Slash commands not appearing in my AI tool

1. Restart your AI tool (commands load at startup)
2. Check that `openspec init` completed successfully
3. Run `openspec update` to refresh configurations

### Validation errors

```bash
# Use strict mode for detailed errors
openspec validate <change-id> --strict

# Common issues:
# - Scenarios must use #### headers (not bullets)
# - Every requirement needs at least one scenario
# - Spec files must have operation headers (## ADDED Requirements)
```

### "Change must have at least one delta"

Your change needs spec updates in `changes/<id>/specs/`. Make sure you have:
```
changes/your-change/
└── specs/
    └── some-capability/
        └── spec.md  # With ## ADDED/MODIFIED/REMOVED
```

### Getting help

```bash
# Show command help
openspec --help
openspec <command> --help

# View interactive dashboard
openspec view
```

## Next Steps

- **Populate project context**: Edit `openspec/project.md` with your project conventions
- **Learn the workflow**: Read [openspec/AGENTS.md](openspec/AGENTS.md) for detailed guidance
- **Explore examples**: Check the [README.md](README.md) for more examples
- **Join the community**: [Discord](https://discord.gg/YctCnvvshC) | [Twitter](https://x.com/0xTab)

## Quick Reference Card

```bash
# Setup
openspec init                  # Initialize in project
openspec update                # Update agent instructions

# Working with changes
openspec list                  # List active changes
openspec show <name>           # View details
openspec validate <name>       # Check format
openspec archive <id> --yes    # Complete and archive

# Working with specs
openspec list --specs          # List capabilities
openspec show <spec> --type spec  # View a spec

# Interactive mode
openspec view                  # Dashboard
openspec show                  # Prompted selection
openspec validate              # Bulk validation
```

## Pro Tips

1. **Run `openspec list` often** to see what's active
2. **Validate early and often** - catch format issues immediately
3. **Use descriptive change IDs** - make them verb-led (add-, update-, remove-)
4. **Archive promptly** - keep changes/ clean and specs/ up-to-date
5. **Populate project.md** - help your AI understand your conventions
6. **Check for conflicts** - review changes before archiving multiple

Happy spec-driven development! 🚀
