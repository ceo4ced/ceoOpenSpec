# OpenSpec Development Guide for AI Assistants

This document provides comprehensive guidance for AI assistants working on the OpenSpec codebase. OpenSpec is a CLI tool that enables spec-driven development for AI coding assistants.

## Project Overview

**What is OpenSpec?**
OpenSpec is an AI-native system for spec-driven development that aligns humans and AI coding assistants by establishing specifications before implementation. It provides a lightweight workflow that locks intent before coding, giving deterministic and reviewable outputs.

**Core Value Proposition:**
- Separates source of truth (`openspec/specs/`) from proposed changes (`openspec/changes/`)
- Provides structured change tracking with proposals, tasks, and spec deltas
- Works with 15+ AI coding assistants through native slash commands and AGENTS.md convention
- No API keys required, brownfield-friendly, minimal setup

**Key Capabilities:**
- Initialize OpenSpec structure in any project (`openspec init`)
- Manage change proposals and spec deltas
- Validate specs and changes against schema
- Archive completed changes and update source specs
- Generate AI tool configurations and slash commands
- Interactive dashboard for viewing specs and changes

## Technology Stack

- **Language:** TypeScript (strict mode, ES2022)
- **Runtime:** Node.js ≥20.19.0 (ESM modules)
- **Package Manager:** pnpm 9.x
- **CLI Framework:** commander.js
- **User Interaction:** @inquirer/prompts
- **Terminal UI:** ora (spinners), chalk (colors)
- **Testing:** Vitest with coverage
- **Build:** Custom build.js script (runs TypeScript compiler)
- **Versioning:** Changesets for semantic versioning
- **Distribution:** npm package `@fission-ai/openspec`

## Codebase Structure

```
ceoOpenSpec/
├── src/                          # Source code (TypeScript)
│   ├── cli/
│   │   └── index.ts              # Main CLI entry point, command registration
│   ├── commands/                 # Command implementations
│   │   ├── change.ts             # Legacy change subcommands (deprecated)
│   │   ├── completion.ts         # Shell completion commands
│   │   ├── show.ts               # Unified show command
│   │   ├── spec.ts               # Spec-specific commands
│   │   └── validate.ts           # Unified validate command
│   ├── core/                     # Core business logic
│   │   ├── archive.ts            # Archive completed changes
│   │   ├── config.ts             # AI tools registry
│   │   ├── global-config.ts      # XDG-compliant global config
│   │   ├── init.ts               # Initialize OpenSpec structure
│   │   ├── list.ts               # List changes and specs
│   │   ├── update.ts             # Update instruction files
│   │   ├── view.ts               # Interactive dashboard
│   │   ├── completions/          # Shell completion system
│   │   │   ├── command-registry.ts    # Command definitions
│   │   │   ├── completion-provider.ts # Core completion logic
│   │   │   ├── factory.ts             # Generator/installer factory
│   │   │   ├── generators/            # Shell-specific generators
│   │   │   └── installers/            # Shell-specific installers
│   │   ├── configurators/        # AI tool configurators
│   │   │   ├── base.ts           # ToolConfigurator interface
│   │   │   ├── registry.ts       # Configurator registry
│   │   │   ├── agents.ts         # AGENTS.md stub generator
│   │   │   ├── claude.ts         # Claude Code configurator
│   │   │   ├── cline.ts          # Cline configurator
│   │   │   ├── codebuddy.ts      # CodeBuddy configurator
│   │   │   ├── costrict.ts       # CoStrict configurator
│   │   │   ├── iflow.ts          # iFlow configurator
│   │   │   ├── qoder.ts          # Qoder configurator
│   │   │   ├── qwen.ts           # Qwen configurator
│   │   │   └── slash/            # Slash command generators
│   │   │       ├── base.ts       # SlashCommandConfigurator interface
│   │   │       ├── registry.ts   # Slash command registry
│   │   │       ├── toml-base.ts  # TOML-based configurators
│   │   │       └── [tool].ts     # Tool-specific slash commands
│   │   ├── converters/           # Format converters
│   │   │   └── json-converter.ts # Spec to JSON conversion
│   │   ├── parsers/              # Markdown and spec parsers
│   │   │   ├── change-parser.ts      # Change proposal parser
│   │   │   ├── markdown-parser.ts    # Markdown AST parser
│   │   │   └── requirement-blocks.ts # Requirement extraction
│   │   ├── schemas/              # Zod validation schemas
│   │   │   ├── base.schema.ts    # Common types
│   │   │   ├── change.schema.ts  # Change validation
│   │   │   └── spec.schema.ts    # Spec validation
│   │   ├── styles/               # Terminal styling
│   │   │   └── palette.ts        # Color definitions
│   │   ├── templates/            # Template content
│   │   │   ├── agents-root-stub.ts       # Root AGENTS.md stub
│   │   │   ├── agents-template.ts        # Full AGENTS.md instructions
│   │   │   ├── claude-template.ts        # CLAUDE.md stub
│   │   │   ├── cline-template.ts         # CLINE.md stub
│   │   │   ├── costrict-template.ts      # COSTRICT.md stub
│   │   │   ├── project-template.ts       # project.md template
│   │   │   └── slash-command-templates.ts # Shared slash command templates
│   │   └── validation/           # Validation logic
│   │       ├── constants.ts      # Validation patterns
│   │       ├── types.ts          # Validation types
│   │       └── validator.ts      # Main validator
│   ├── utils/                    # Shared utilities
│   │   ├── file-system.ts        # File operations with rollback
│   │   ├── interactive.ts        # Inquirer prompts
│   │   ├── item-discovery.ts     # Discover changes/specs
│   │   ├── match.ts              # Fuzzy matching
│   │   ├── shell-detection.ts    # Shell environment detection
│   │   └── task-progress.ts      # Progress tracking
│   └── index.ts                  # Package exports
├── test/                         # Test files (mirrors src/)
│   ├── cli-e2e/                  # End-to-end CLI tests
│   ├── commands/                 # Command tests
│   ├── core/                     # Core logic tests
│   ├── fixtures/                 # Test fixtures
│   ├── helpers/                  # Test helpers
│   └── utils/                    # Utility tests
├── bin/
│   └── openspec.js               # CLI executable entry point
├── scripts/
│   ├── pack-version-check.mjs    # Pre-publish version validation
│   └── postinstall.js            # Post-install script
├── openspec/                     # OpenSpec meta (dogfooding)
│   ├── project.md                # OpenSpec project conventions
│   ├── AGENTS.md                 # OpenSpec workflow instructions
│   ├── specs/                    # OpenSpec capability specs
│   └── changes/                  # Active and archived changes
├── .github/workflows/
│   └── ci.yml                    # CI/CD pipeline
├── .changeset/                   # Changeset configuration
├── build.js                      # Custom TypeScript build script
├── tsconfig.json                 # TypeScript configuration
├── vitest.config.ts              # Vitest configuration
├── package.json                  # Package metadata
└── pnpm-lock.yaml                # pnpm lockfile
```

## Development Workflow

### Initial Setup

```bash
# Clone the repository
git clone https://github.com/Fission-AI/OpenSpec
cd OpenSpec

# Install dependencies
pnpm install

# Build the project
pnpm run build

# Link for local development
pnpm link --global

# Verify installation
openspec --version
```

### Development Commands

```bash
pnpm run dev              # Watch mode (TypeScript compilation)
pnpm run dev:cli          # Build and run CLI
pnpm run build            # Production build
pnpm test                 # Run all tests
pnpm test:watch           # Watch mode for tests
pnpm test:ui              # Interactive test UI
pnpm test:coverage        # Generate coverage report
```

### Release Workflow

This project uses [Changesets](https://github.com/changesets/changesets) for versioning:

```bash
# Create a changeset (do this for each PR)
pnpm changeset

# Version packages (CI does this automatically)
pnpm run release:ci

# Local release (manual)
pnpm run release:local
```

**Important:** Always create a changeset for user-facing changes.

## Key Conventions and Patterns

### TypeScript Conventions

1. **Strict Mode Enabled:** All code must pass strict TypeScript checks
2. **ESM Modules:** Use `import/export`, not `require/module.exports`
3. **Async/Await:** All async operations use async/await (no raw promises)
4. **Explicit Types:** Prefer explicit return types on public functions
5. **No `any`:** Use `unknown` and type guards instead

### File Organization

1. **One Class Per File:** Each major class gets its own file
2. **Grouped Exports:** Related utilities in single files (e.g., `file-system.ts`)
3. **Index Files:** Use `index.ts` for public exports only
4. **Test Co-location:** Tests mirror source structure in `test/` directory

### Naming Conventions

- **Files:** kebab-case (`change-parser.ts`, `file-system.ts`)
- **Classes:** PascalCase (`InitCommand`, `ChangeParser`)
- **Functions:** camelCase (`parseMarkdown`, `validateSpec`)
- **Constants:** SCREAMING_SNAKE_CASE (`AI_TOOLS`, `DEFAULT_TIMEOUT`)
- **Interfaces:** PascalCase (`ToolConfigurator`, `ValidationResult`)
- **Change IDs:** kebab-case, verb-led (`add-cline-support`, `update-cli-init`)

### Error Handling

```typescript
// ❌ Don't: Catch errors in utilities
export function readFile(path: string): string {
  try {
    return fs.readFileSync(path, 'utf-8');
  } catch (error) {
    console.error('Failed to read file');
    return '';
  }
}

// ✅ Do: Let errors bubble to CLI layer
export function readFile(path: string): string {
  return fs.readFileSync(path, 'utf-8');
}

// ✅ Do: Catch at command level
class ShowCommand {
  async execute() {
    try {
      const content = readFile(path);
      // ... process
    } catch (error) {
      ora().fail(`Error: ${(error as Error).message}`);
      process.exit(1);
    }
  }
}
```

### Logging Patterns

```typescript
// Normal output
console.log('OpenSpec initialized successfully');

// Errors (stderr)
console.error(`Error: ${message}`);

// Spinners for progress
const spinner = ora('Creating OpenSpec structure...').start();
// ... work
spinner.succeed('OpenSpec structure created');

// Colors (use chalk sparingly)
import chalk from 'chalk';
console.log(chalk.green('✓ Success'));
```

### Exit Codes

- `0`: Success
- `1`: General error
- `2`: Misuse (reserved)
- `3`: User cancelled (reserved)

## Testing Strategy

### Test Organization

```
test/
├── cli-e2e/                     # Full CLI integration tests
├── commands/                    # Command-level tests
├── core/                        # Core logic unit tests
│   ├── archive.test.ts
│   ├── init.test.ts
│   ├── validation/
│   ├── configurators/
│   └── parsers/
├── fixtures/                    # Test data and fixtures
├── helpers/                     # Test utilities
└── utils/                       # Utility function tests
```

### Testing Best Practices

1. **Use Fixtures:** Real-world examples in `test/fixtures/`
2. **Isolation:** Each test should be independent
3. **Descriptive Names:** `test('should create CLAUDE.md with managed markers', ...)`
4. **Async Tests:** Always use `async/await` in tests
5. **Coverage:** Aim for >80% coverage on core logic

### Writing Tests

```typescript
import { describe, test, expect, beforeEach, afterEach } from 'vitest';
import { tmpdir } from 'os';
import { join } from 'path';
import { mkdirSync, rmSync } from 'fs';

describe('InitCommand', () => {
  let testDir: string;

  beforeEach(() => {
    testDir = join(tmpdir(), `openspec-test-${Date.now()}`);
    mkdirSync(testDir, { recursive: true });
  });

  afterEach(() => {
    rmSync(testDir, { recursive: true, force: true });
  });

  test('should create openspec directory structure', async () => {
    const init = new InitCommand();
    await init.execute(testDir);

    expect(existsSync(join(testDir, 'openspec/specs'))).toBe(true);
    expect(existsSync(join(testDir, 'openspec/changes'))).toBe(true);
  });
});
```

## Common Development Tasks

### Adding a New AI Tool Configurator

1. **Create configurator file:** `src/core/configurators/[tool].ts`

```typescript
import { ToolConfigurator } from './base.js';
import { writeFileWithRollback } from '../../utils/file-system.js';

export class MyToolConfigurator implements ToolConfigurator {
  name = 'MyTool';
  configFileName = 'MYTOOL.md';
  isAvailable = true;

  async configure(projectPath: string, openspecDir: string): Promise<void> {
    const filePath = join(projectPath, this.configFileName);
    const content = TemplateManager.getMyToolTemplate();
    await writeFileWithRollback(filePath, content);
  }
}
```

2. **Register in registry:** `src/core/configurators/registry.ts`

```typescript
import { MyToolConfigurator } from './mytool.js';

export const TOOL_CONFIGURATORS: ToolConfigurator[] = [
  // ... existing
  new MyToolConfigurator(),
];
```

3. **Add to AI_TOOLS:** `src/core/config.ts`

```typescript
export const AI_TOOLS = [
  // ... existing
  { value: 'mytool', label: 'MyTool', available: true },
];
```

4. **Create template:** `src/core/templates/mytool-template.ts`

```typescript
export class TemplateManager {
  static getMyToolTemplate(): string {
    return `<!-- OPENSPEC:START -->
# OpenSpec Instructions

This project uses OpenSpec. See @/openspec/AGENTS.md for details.
<!-- OPENSPEC:END -->
`;
  }
}
```

5. **Add tests:** `test/core/configurators/mytool.test.ts`

6. **Update README.md** with MyTool in supported tools list

### Adding Slash Command Support

1. **Create slash configurator:** `src/core/configurators/slash/[tool].ts`

```typescript
import { SlashCommandConfigurator } from './base.js';

export class MyToolSlashConfigurator extends SlashCommandConfigurator {
  getCommandsDir(projectPath: string): string {
    return join(projectPath, '.mytool', 'commands');
  }

  formatCommand(name: string, content: string): string {
    // Add tool-specific formatting (frontmatter, etc.)
    return content;
  }
}
```

2. **Register slash configurator:** `src/core/configurators/slash/registry.ts`

3. **Update init spec:** `openspec/specs/cli-init/spec.md`

### Modifying Validation Rules

1. **Update schemas:** `src/core/schemas/spec.schema.ts` or `change.schema.ts`
2. **Update validator:** `src/core/validation/validator.ts`
3. **Update constants:** `src/core/validation/constants.ts`
4. **Add tests:** `test/core/validation/`
5. **Update spec:** `openspec/specs/[relevant-spec]/spec.md`

### Adding a New Command

1. **Create command file:** `src/commands/[command].ts`

```typescript
export class MyCommand {
  async execute(options?: MyOptions): Promise<void> {
    try {
      // Command logic
      ora().succeed('Command completed');
    } catch (error) {
      ora().fail(`Error: ${(error as Error).message}`);
      process.exit(1);
    }
  }
}
```

2. **Register in CLI:** `src/cli/index.ts`

```typescript
program
  .command('mycommand [arg]')
  .description('Description of my command')
  .option('--flag', 'Flag description')
  .action(async (arg?: string, options?: { flag?: boolean }) => {
    try {
      const cmd = new MyCommand();
      await cmd.execute(arg, options);
    } catch (error) {
      ora().fail(`Error: ${(error as Error).message}`);
      process.exit(1);
    }
  });
```

3. **Add completion support:** `src/core/completions/command-registry.ts`

4. **Create tests:** `test/commands/[command].test.ts`

5. **Create spec:** `openspec/specs/cli-[command]/spec.md`

## Important Files and Their Purposes

### Core Entry Points

- **`bin/openspec.js`**: Executable entry point, sets up Node.js environment
- **`src/cli/index.ts`**: Main CLI, registers all commands
- **`src/index.ts`**: Package exports for programmatic use

### Critical Core Files

- **`src/core/init.ts`**: Initialization logic, AI tool setup
- **`src/core/archive.ts`**: Archive workflow, spec merging
- **`src/core/validation/validator.ts`**: Spec and change validation
- **`src/core/parsers/markdown-parser.ts`**: Markdown parsing engine
- **`src/core/schemas/spec.schema.ts`**: Zod schema for specs

### Configuration and Templates

- **`src/core/config.ts`**: AI tools registry
- **`src/core/templates/agents-template.ts`**: Primary AGENTS.md content
- **`src/core/templates/slash-command-templates.ts`**: Shared slash command templates

### Utilities

- **`src/utils/file-system.ts`**: File operations with rollback support
- **`src/utils/interactive.ts`**: Inquirer prompts and user interaction
- **`src/utils/item-discovery.ts`**: Discover changes and specs in filesystem

## Git Workflow and Commit Conventions

### Commit Messages

Follow [Conventional Commits](https://conventionalcommits.org/):

```
type(scope): subject

[optional body]

[optional footer]
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `refactor`: Code refactoring
- `test`: Test changes
- `chore`: Build, dependencies, etc.
- `perf`: Performance improvements

**Scopes:**
- `cli`: CLI commands
- `core`: Core logic
- `config`: Configuration
- `init`: Initialization
- `archive`: Archive functionality
- `validation`: Validation logic
- `completions`: Shell completions
- `global-config`: Global configuration

**Examples:**
```
feat(cli): add global config command
fix(validation): handle empty requirement blocks
docs: update CLAUDE.md with testing guidelines
refactor(core): simplify configurator registry
test(archive): add spec merge tests
chore(deps): update chalk to v5.5.0
```

### Branch Strategy

- **`main`**: Stable release branch
- **Feature branches**: `claude/[feature-name]-[SESSION_ID]`
- **Always create PRs** for review before merging

### Pre-commit Checklist

Before committing:
1. ✅ Run `pnpm run build` successfully
2. ✅ Run `pnpm test` (all tests pass)
3. ✅ Create changeset if needed (`pnpm changeset`)
4. ✅ Update relevant specs in `openspec/specs/`
5. ✅ Follow commit message conventions

## OpenSpec Meta: Dogfooding

**This repository uses OpenSpec for its own development.**

- **Current specs:** `openspec/specs/` contains capability specifications
- **Active changes:** `openspec/changes/` contains current proposals
- **Archived changes:** `openspec/changes/archive/` contains completed work

### Before Making Changes

1. **Review existing specs:** `openspec list --specs`
2. **Check active changes:** `openspec list`
3. **Read project conventions:** `openspec/project.md`
4. **Follow OpenSpec workflow:** See `openspec/AGENTS.md`

### Creating a Change Proposal

```bash
# 1. Choose a change ID (verb-led, kebab-case)
change_id="add-new-feature"

# 2. Create directory structure
mkdir -p openspec/changes/$change_id/specs

# 3. Create proposal.md
cat > openspec/changes/$change_id/proposal.md << 'EOF'
## Why
[Problem or opportunity]

## What Changes
- [List of changes]

## Impact
- Affected specs: [spec names]
- Affected code: [file paths]
EOF

# 4. Create tasks.md
cat > openspec/changes/$change_id/tasks.md << 'EOF'
## 1. Implementation
- [ ] 1.1 First task
- [ ] 1.2 Second task

## 2. Testing
- [ ] 2.1 Add unit tests
- [ ] 2.2 Add integration tests
EOF

# 5. Create spec deltas
# ... create spec delta files in specs/ subdirectory

# 6. Validate
openspec validate $change_id --strict

# 7. Get approval before implementing
```

### Implementing a Change

```bash
# Always read the proposal first
openspec show $change_id

# Implement tasks sequentially
# Mark tasks complete as you go

# After all implementation is done
openspec archive $change_id --yes
```

## Things to Watch Out For

### Common Pitfalls

1. **Managed Markers:** Always preserve `<!-- OPENSPEC:START -->` and `<!-- OPENSPEC:END -->` markers
2. **ESM Imports:** Use `.js` extensions in imports (e.g., `from './file.js'`)
3. **Async Operations:** Don't forget `await` - will cause silent failures
4. **Process.chdir:** Some tests use `process.chdir` - not compatible with worker threads
5. **Global State:** Avoid global state; use dependency injection
6. **Path Separators:** Use `path.join()`, not string concatenation
7. **File System Rollback:** Use `writeFileWithRollback` for atomic operations
8. **Exit Codes:** Always exit with appropriate code on error

### File System Operations

```typescript
// ✅ Do: Use rollback-safe operations
import { writeFileWithRollback, RollbackManager } from '../utils/file-system.js';

const rollback = new RollbackManager();
await writeFileWithRollback(filePath, content, rollback);

// ❌ Don't: Direct file writes without rollback
fs.writeFileSync(filePath, content);
```

### Cross-Platform Compatibility

- **Line Endings:** Normalize to `\n` for consistency
- **Path Separators:** Always use `path.join()` and `path.resolve()`
- **Shell Detection:** Use `detectShell()` for shell-specific logic
- **Case Sensitivity:** Assume case-sensitive filesystems

### Performance Considerations

- **Parallel Operations:** Use `Promise.all()` for independent operations
- **Streaming:** For large files, consider streaming
- **Caching:** Cache parsed specs and changes when appropriate
- **Concurrency:** Default to 6 concurrent validations (configurable)

## Architecture Patterns

### Configurator Pattern

Used for AI tool setup:

```typescript
interface ToolConfigurator {
  name: string;
  configFileName: string;
  isAvailable: boolean;
  configure(projectPath: string, openspecDir: string): Promise<void>;
}
```

Each AI tool gets a configurator that knows how to set up its instruction files.

### Command Pattern

Each CLI command is a class with an `execute` method:

```typescript
class InitCommand {
  async execute(targetPath: string, options?: Options): Promise<void> {
    // Command implementation
  }
}
```

### Template Pattern

Templates are centralized in `TemplateManager`:

```typescript
class TemplateManager {
  static getAgentsTemplate(): string { ... }
  static getClaudeTemplate(): string { ... }
  static getProjectTemplate(): string { ... }
}
```

### Parser Pattern

Parsers convert markdown to structured data:

```typescript
class MarkdownParser {
  parse(content: string): ParsedSpec { ... }
}

class ChangeParser {
  parse(changePath: string): Change { ... }
}
```

### Validation Pattern

Validators use Zod schemas + custom rules:

```typescript
const result = await validator.validate(spec);
if (!result.valid) {
  // Handle errors
}
```

## Debugging Tips

### Enable Debug Logging

```bash
# Show detailed validation output
openspec validate --strict --json | jq

# Show change structure
openspec show [change] --json | jq

# Test CLI in development
pnpm run dev:cli -- init test-dir --tools all
```

### Common Issues

**Issue:** "OpenSpec directory already exists"
- **Solution:** Run `openspec update` to refresh, or `openspec init` picks up extend mode

**Issue:** Import errors with `.js` extensions
- **Solution:** ESM requires `.js` extensions even for `.ts` files

**Issue:** Tests hang or timeout
- **Solution:** Check for missing `await`, or process.chdir issues in tests

**Issue:** Validation failures
- **Solution:** Run `openspec validate --strict --json` for detailed errors

## Resources and References

### External Documentation

- [Commander.js](https://github.com/tj/commander.js) - CLI framework
- [Inquirer](https://github.com/SBoudrias/Inquirer.js) - Interactive prompts
- [Vitest](https://vitest.dev/) - Test framework
- [Zod](https://zod.dev/) - Schema validation
- [Changesets](https://github.com/changesets/changesets) - Version management

### Internal Documentation

- **OpenSpec Workflow:** `openspec/AGENTS.md` (full workflow for AI assistants)
- **Project Conventions:** `openspec/project.md` (project-specific rules)
- **Specs Directory:** `openspec/specs/` (capability specifications)
- **README:** `README.md` (user-facing documentation)

### Getting Help

- **GitHub Issues:** [OpenSpec Issues](https://github.com/Fission-AI/OpenSpec/issues)
- **Discord:** [OpenSpec Discord](https://discord.gg/YctCnvvshC)
- **Twitter:** [@0xTab](https://x.com/0xTab)

## Quick Reference Card

### Essential Commands

```bash
# Development
pnpm install           # Install dependencies
pnpm run build         # Build project
pnpm test              # Run tests
pnpm link              # Link for local dev

# OpenSpec Meta
openspec list --specs  # List capabilities
openspec list          # List changes
openspec show [item]   # Show details
openspec validate      # Validate all

# Git
git checkout -b claude/feature-name-SESSION_ID
git add .
git commit -m "feat(scope): description"
pnpm changeset         # Create changeset
```

### File Locations

```
Core Logic:        src/core/
Commands:          src/commands/
Utilities:         src/utils/
Templates:         src/core/templates/
Configurators:     src/core/configurators/
Tests:             test/
Specs:             openspec/specs/
Changes:           openspec/changes/
```

### Key Patterns

```typescript
// Command structure
class Command {
  async execute(arg?: string, options?: Options): Promise<void> { }
}

// Error handling
try { } catch (error) {
  ora().fail(`Error: ${(error as Error).message}`);
  process.exit(1);
}

// File operations
await writeFileWithRollback(path, content, rollback);

// Validation
const result = await validator.validate(item);
```

---

**Last Updated:** 2025-12-21
**OpenSpec Version:** 0.16.0
**Node.js:** ≥20.19.0
**pnpm:** 9.x
