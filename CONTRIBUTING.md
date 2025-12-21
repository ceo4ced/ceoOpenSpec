# Contributing to OpenSpec

Thank you for your interest in contributing to OpenSpec! This guide will help you get started with development and understand how to contribute effectively.

## Table of Contents

- [Getting Started](#getting-started)
- [Development Environment](#development-environment)
- [Project Structure](#project-structure)
- [Development Workflow](#development-workflow)
- [Testing](#testing)
- [Submitting Changes](#submitting-changes)
- [Code Style](#code-style)
- [Documentation](#documentation)

## Getting Started

### Prerequisites

- **Node.js >= 20.19.0** - Check your version: `node --version`
- **pnpm** - Fast, disk space efficient package manager
- **Git** - Version control

### Quick Setup

1. **Fork and clone the repository**
   ```bash
   # If contributing to the upstream project:
   git clone https://github.com/YOUR_USERNAME/OpenSpec.git
   cd OpenSpec
   
   # Or for this fork:
   git clone https://github.com/YOUR_USERNAME/ceoOpenSpec.git
   cd ceoOpenSpec
   ```

2. **Install dependencies**
   ```bash
   pnpm install
   ```

3. **Build the project**
   ```bash
   pnpm run build
   ```

4. **Verify installation**
   ```bash
   pnpm run dev:cli -- --version
   ```

### Alternative: Use Dev Container

For a consistent development environment without local setup:

1. Install [VS Code](https://code.visualstudio.com/), [Docker Desktop](https://www.docker.com/products/docker-desktop), and the [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)
2. Open the project in VS Code
3. Click "Reopen in Container" when prompted
4. Wait for automatic setup to complete

See [.devcontainer/README.md](.devcontainer/README.md) for details.

## Development Environment

### Directory Structure

```
ceoOpenSpec/
├── src/              # TypeScript source code
│   ├── cli/          # CLI entry points
│   ├── commands/     # Command implementations
│   ├── core/         # Core OpenSpec logic
│   └── utils/        # Shared utilities
├── test/             # Test files
├── bin/              # CLI executable
├── scripts/          # Build and utility scripts
├── openspec/         # OpenSpec metadata (self-hosted)
│   ├── AGENTS.md     # AI assistant instructions
│   ├── project.md    # Project conventions
│   ├── specs/        # Specifications
│   └── changes/      # Change proposals
└── dist/             # Compiled output (gitignored)
```

### Key Files

- `src/index.ts` - Main library entry point
- `bin/openspec.js` - CLI executable wrapper
- `build.js` - Custom build script using TypeScript compiler
- `package.json` - Package configuration and scripts
- `tsconfig.json` - TypeScript configuration

## Development Workflow

### 1. Create a Branch

```bash
git checkout -b feature/your-feature-name
```

Use descriptive branch names:
- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation updates
- `refactor/` - Code refactoring

### 2. Make Your Changes

OpenSpec follows **spec-driven development**. Before making significant changes:

1. **Check for existing specs/changes**
   ```bash
   pnpm run dev:cli -- list
   pnpm run dev:cli -- list --specs
   ```

2. **Create a change proposal** (for new features or breaking changes)
   ```bash
   # Read openspec/AGENTS.md for guidance
   # Create a proposal in openspec/changes/
   pnpm run dev:cli -- validate your-change-id
   ```

3. **Implement your changes** following the tasks in your proposal

### 3. Development Commands

```bash
# Compile TypeScript in watch mode
pnpm run dev

# Run CLI in development mode
pnpm run dev:cli -- <command> <args>

# Build for production
pnpm run build

# Run tests
pnpm test

# Run tests in watch mode
pnpm test:watch

# Run tests with coverage
pnpm test:coverage
```

### 4. Test Your Changes

```bash
# Run the full test suite
pnpm test

# Test CLI commands manually
pnpm run dev:cli -- init /tmp/test-project
pnpm run dev:cli -- list
pnpm run dev:cli -- validate

# Link locally for end-to-end testing
pnpm link --global
cd /tmp/test-project
openspec --version
pnpm unlink --global
```

## Testing

### Test Structure

- Tests live in `test/` directory
- Use Vitest as the test framework
- Test files mirror the source structure: `test/core/archive.test.ts` → `src/core/archive.ts`

### Writing Tests

```typescript
import { describe, it, expect } from 'vitest';
import { yourFunction } from '../src/your-module';

describe('yourFunction', () => {
  it('should handle expected input', () => {
    const result = yourFunction('input');
    expect(result).toBe('expected');
  });

  it('should throw on invalid input', () => {
    expect(() => yourFunction(null)).toThrow();
  });
});
```

### Running Tests

```bash
# Run all tests
pnpm test

# Run tests in watch mode (useful during development)
pnpm test:watch

# Run tests with UI
pnpm test:ui

# Run tests with coverage report
pnpm test:coverage
```

## Submitting Changes

### Before Committing

1. **Run tests**
   ```bash
   pnpm test
   ```

2. **Build successfully**
   ```bash
   pnpm run build
   ```

3. **Validate your OpenSpec changes** (if applicable)
   ```bash
   pnpm run dev:cli -- validate --strict
   ```

### Commit Messages

Follow [Conventional Commits](https://conventionalcommits.org/):

```
type(scope): subject

body (optional)

footer (optional)
```

**Types:**
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `style:` - Code style changes (formatting, etc.)
- `refactor:` - Code refactoring
- `test:` - Adding or updating tests
- `chore:` - Maintenance tasks

**Examples:**
```bash
git commit -m "feat(cli): add --json flag to list command"
git commit -m "fix(archive): prevent data loss on parallel merges"
git commit -m "docs: add contributing guidelines"
```

### Creating a Pull Request

1. **Push your branch**
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Create a Pull Request** on GitHub
   - Use a clear, descriptive title
   - Reference any related issues
   - Describe what changed and why
   - Include testing steps if applicable

3. **Respond to feedback**
   - Address review comments
   - Push additional commits as needed
   - Mark conversations as resolved

## Code Style

### TypeScript Guidelines

- **Strict mode enabled** - Handle all type safety requirements
- **Async/await** - Use for all asynchronous operations
- **Descriptive names** - Functions and variables should be self-documenting
- **Minimal dependencies** - Only add dependencies when necessary
- **Error handling** - Let errors bubble to CLI level for consistent messaging

### Code Organization

```typescript
// Good: Clear separation of concerns
export async function listChanges(options: ListOptions): Promise<Change[]> {
  const changes = await readChangesDirectory();
  return filterChanges(changes, options);
}

// Good: Descriptive variable names
const activeChanges = changes.filter(c => !c.archived);

// Good: Early returns for clarity
if (!fs.existsSync(path)) {
  return [];
}
```

### File Organization

- Keep files focused on a single responsibility
- Group related functions together
- Export only what's necessary
- Use barrel exports (`index.ts`) for clean imports

## Documentation

### Code Documentation

- Add JSDoc comments for public APIs
- Include examples for complex functions
- Document edge cases and assumptions

```typescript
/**
 * Archives a completed change by moving it to the archive directory
 * and optionally updating the main specs.
 * 
 * @param changeId - The unique identifier of the change to archive
 * @param options - Archive options (skipSpecs, force, etc.)
 * @returns Promise that resolves when archiving is complete
 * @throws Error if the change doesn't exist or validation fails
 */
export async function archiveChange(
  changeId: string,
  options: ArchiveOptions
): Promise<void> {
  // Implementation
}
```

### Updating Documentation

When making changes that affect users:

1. Update `README.md` if it changes how people use OpenSpec
2. Update `openspec/AGENTS.md` if it changes AI assistant workflows
3. Update `CHANGELOG.md` using changesets (see below)
4. Add/update examples if introducing new features

### Changesets

We use [changesets](https://github.com/changesets/changesets) for version management:

```bash
# Add a changeset describing your changes
pnpm changeset

# Follow the prompts:
# 1. Select the type of change (major/minor/patch)
# 2. Describe the change for the changelog
```

This creates a file in `.changeset/` that will be used during release.

## Getting Help

- **Discord**: Join our [Discord community](https://discord.gg/YctCnvvshC)
- **Issues**: Check existing issues or create a new one in the repository
- **Twitter**: Follow [@0xTab](https://x.com/0xTab) for updates
- **Upstream**: [Fission-AI/OpenSpec](https://github.com/Fission-AI/OpenSpec) - Main repository

## License

By contributing to OpenSpec, you agree that your contributions will be licensed under the MIT License.
