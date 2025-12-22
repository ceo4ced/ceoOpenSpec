# Patent Bar Study AI - Project Conventions

## Technology Stack

### Core Technologies

| Technology | Version | Purpose |
|------------|---------|---------|
| TypeScript | 5.x | Primary language |
| Node.js | ≥20.x | Runtime environment |
| React | 18.x | Frontend UI framework |
| Next.js | 14.x | Full-stack framework |
| pnpm | 9.x | Package manager |
| PostgreSQL | 16.x | Primary database |
| Prisma | 5.x | ORM and migrations |

### AI/ML Stack

| Technology | Purpose |
|------------|---------|
| OpenAI API | Question generation, explanations |
| Anthropic Claude | Study assistance, tutoring |
| Vector Database | MPEP semantic search |

### Testing

| Tool | Purpose |
|------|---------|
| Vitest | Unit and integration tests |
| Playwright | End-to-end testing |
| Testing Library | Component testing |

## Project Structure

```
patent-bar-study-ai/
├── openspec/               # Specifications
├── src/
│   ├── app/               # Next.js app router
│   ├── components/        # React components
│   │   ├── ui/           # Base UI components
│   │   ├── study/        # Study session components
│   │   ├── questions/    # Question display components
│   │   └── dashboard/    # Dashboard components
│   ├── lib/              # Shared utilities
│   │   ├── db/          # Database utilities
│   │   ├── mpep/        # MPEP reference utilities
│   │   ├── scoring/     # Scoring algorithms
│   │   └── spaced-rep/  # Spaced repetition logic
│   ├── server/           # Server-side code
│   │   ├── api/         # API routes
│   │   ├── services/    # Business logic
│   │   └── jobs/        # Background jobs
│   └── types/            # TypeScript types
├── prisma/
│   ├── schema.prisma     # Database schema
│   └── migrations/       # Database migrations
├── content/
│   ├── questions/        # Question bank
│   ├── flashcards/       # Flashcard decks
│   └── mpep/            # MPEP reference data
├── tests/
│   ├── unit/            # Unit tests
│   ├── integration/     # Integration tests
│   └── e2e/             # End-to-end tests
└── docs/                 # Documentation
```

## Coding Conventions

### TypeScript

```typescript
// Use explicit types for function parameters and returns
function calculateScore(answers: Answer[], questions: Question[]): ScoreResult {
  // ...
}

// Use interfaces for data structures
interface StudySession {
  id: string;
  userId: string;
  startedAt: Date;
  questions: SessionQuestion[];
  status: SessionStatus;
}

// Use enums for finite sets
enum SessionStatus {
  Active = 'active',
  Paused = 'paused',
  Completed = 'completed',
  Abandoned = 'abandoned',
}

// Use type for unions and computed types
type QuestionDifficulty = 'easy' | 'medium' | 'hard';
type MPEPChapter = `${number}00`;
```

### React Components

```typescript
// Use functional components with TypeScript
interface QuestionCardProps {
  question: Question;
  onAnswer: (answerId: string) => void;
  showExplanation?: boolean;
}

export function QuestionCard({
  question,
  onAnswer,
  showExplanation = false
}: QuestionCardProps) {
  // Component implementation
}
```

### File Naming

- **Components**: PascalCase (`QuestionCard.tsx`)
- **Utilities**: camelCase (`calculateScore.ts`)
- **Types**: PascalCase in `types/` folder
- **Tests**: `*.test.ts` or `*.spec.ts`
- **Specs**: `spec.md` in capability folders

### Error Handling

```typescript
// Use custom error classes
class MPEPReferenceError extends Error {
  constructor(
    public section: string,
    message: string
  ) {
    super(message);
    this.name = 'MPEPReferenceError';
  }
}

// Handle errors gracefully
async function getMPEPSection(section: string): Promise<MPEPContent> {
  try {
    const content = await fetchMPEPSection(section);
    if (!content) {
      throw new MPEPReferenceError(section, `Section ${section} not found`);
    }
    return content;
  } catch (error) {
    logger.error('MPEP fetch failed', { section, error });
    throw error;
  }
}
```

## Database Schema Principles

### Core Entities

```
User
├── id, email, name
├── createdAt, updatedAt
└── preferences (JSON)

Question
├── id, content, type
├── mpepSection, mpepChapter
├── difficulty, topic
├── correctAnswerId
└── explanation

Answer
├── id, questionId
├── content, isCorrect
└── explanation

StudySession
├── id, userId
├── type (practice|mock|flashcard)
├── startedAt, completedAt
├── score, totalQuestions
└── status

SessionQuestion
├── id, sessionId, questionId
├── userAnswerId
├── isCorrect, timeSpent
└── order

Flashcard
├── id, front, back
├── mpepSection, topic
├── deckId
└── easeFactor, interval, nextReview

UserProgress
├── id, userId
├── topic, mpepChapter
├── questionsAttempted, correctCount
├── lastStudied, mastery
└── weakAreas (JSON)
```

### Indexing Strategy

- Index on `userId` for all user-related queries
- Index on `mpepSection` for reference lookups
- Composite index on `(userId, topic)` for progress queries
- Index on `nextReview` for spaced repetition scheduling

## API Design

### REST Endpoints

```
# Study Sessions
POST   /api/sessions              # Start new session
GET    /api/sessions/:id          # Get session details
PATCH  /api/sessions/:id          # Update session (pause/resume)
POST   /api/sessions/:id/answer   # Submit answer
POST   /api/sessions/:id/complete # Complete session

# Questions
GET    /api/questions             # List questions (filtered)
GET    /api/questions/:id         # Get question details
GET    /api/questions/next        # Get next adaptive question

# MPEP Reference
GET    /api/mpep/:section         # Get MPEP section content
GET    /api/mpep/search           # Search MPEP content

# Progress
GET    /api/progress              # Get user progress overview
GET    /api/progress/:topic       # Get topic-specific progress
GET    /api/progress/readiness    # Get exam readiness score

# Flashcards
GET    /api/flashcards/due        # Get due flashcards
POST   /api/flashcards/:id/review # Submit flashcard review
```

### Response Format

```typescript
interface APIResponse<T> {
  success: boolean;
  data?: T;
  error?: {
    code: string;
    message: string;
    details?: unknown;
  };
  meta?: {
    page?: number;
    limit?: number;
    total?: number;
  };
}
```

## Testing Standards

### Unit Tests

- Test all scoring algorithms
- Test spaced repetition calculations
- Test MPEP section parsing
- Aim for 80%+ coverage on `lib/`

### Integration Tests

- Test database operations
- Test MPEP reference resolution
- Test session lifecycle
- Test progress calculations

### E2E Tests

- Complete study session flow
- Mock exam completion
- Flashcard review cycle
- Progress dashboard accuracy

## Performance Guidelines

### Response Times

- Page load: < 1 second
- Question display: < 200ms
- MPEP search: < 500ms
- Progress calculation: < 300ms

### Caching Strategy

- Cache MPEP content (immutable per version)
- Cache question bank (refresh daily)
- Cache user progress (invalidate on update)
- Use SWR for client-side caching

## Security Considerations

### Data Protection

- Encrypt user study data at rest
- Use secure sessions with proper expiry
- Rate limit API endpoints
- Validate all MPEP section references

### Content Integrity

- Verify question source attribution
- Track content version history
- Audit trail for answer changes
- Protect against answer scraping

## Deployment

### Environments

| Environment | Purpose |
|-------------|---------|
| Development | Local development |
| Staging | Pre-production testing |
| Production | Live application |

### CI/CD Pipeline

1. Run linting and type checking
2. Run unit and integration tests
3. Build application
4. Run E2E tests on staging
5. Deploy to production
6. Run smoke tests

## Version Control

### Branch Naming

- `main` - Production-ready code
- `develop` - Integration branch
- `feature/[name]` - New features
- `fix/[name]` - Bug fixes
- `content/[name]` - Content updates

### Commit Messages

Use Conventional Commits:

```
feat(questions): add PCT chapter questions
fix(scoring): correct weighted average calculation
docs(mpep): update chapter 2100 references
test(sessions): add mock exam completion tests
```
