# cmo.brand

## Preamble

This command creates and maintains brand identity documentation including visual identity, voice/tone, and style guidelines.

**Must read before execution:**
1. `.mission/agent-governance.md`
2. `CMO/.ethics/ethics.md`
3. `CEO/.ceo/memory/vision.md` (if exists)

---

## Outline

Establish complete brand identity that governs all digital assets and content.

### Brand Kit Template

```markdown
# Brand Kit: [Business Name]
Version: [X.X]
Last Updated: [Date]
Approved by: [Human approval required]

## ⚠️ APPROVAL REQUIRED

> All brand assets and guidelines require human approval before use.
> No external publication without **GREENLIGHT: BRAND** from human.

---

## Brand Overview

### Brand Story
[2-3 paragraphs about the brand's origin, purpose, and promise]

### Brand Promise
[One sentence: What do we promise to every customer?]

### Brand Values
| Value | What It Means | How We Show It |
|-------|---------------|----------------|
| [Value 1] | [Definition] | [Behavior] |
| [Value 2] | [Definition] | [Behavior] |
| [Value 3] | [Definition] | [Behavior] |

### Target Audience
| Attribute | Primary | Secondary |
|-----------|---------|-----------|
| Age Range | [Range] | [Range] |
| Location | [Where] | [Where] |
| Interests | [What] | [What] |
| Pain Points | [What] | [What] |
| Platform | [Where] | [Where] |

### Audience Age Gate ⚠️
| Status | Implications |
|--------|--------------|
| **Under 13** | 🔴 COPPA applies. Parental consent required. |
| **13-17** | 🟡 Age-appropriate content only. No adult themes. |
| **18+** | 🟢 Adult content permitted with disclosure. |

**This brand targets:** [Age range]

---

## Visual Identity

### Logo

#### Primary Logo
![Primary Logo](/path/to/primary-logo.png)
- **File formats:** SVG, PNG, PDF
- **Minimum size:** 32px height
- **Clear space:** 1x logo height all sides

#### Logo Variations
| Variation | Use Case | File |
|-----------|----------|------|
| Primary | Light backgrounds | [link] |
| Reversed | Dark backgrounds | [link] |
| Icon only | Favicons, avatars | [link] |
| Wordmark | When icon used separately | [link] |

#### Logo Don'ts
❌ Don't rotate the logo  
❌ Don't change colors arbitrarily  
❌ Don't stretch or distort  
❌ Don't add effects (shadows, glows)  
❌ Don't place on busy backgrounds  

### Color Palette

#### Primary Colors
| Name | Hex | RGB | Use |
|------|-----|-----|-----|
| Primary | #[XXXXXX] | rgb(X,X,X) | Main brand color |
| Secondary | #[XXXXXX] | rgb(X,X,X) | Accents |

#### Secondary Colors
| Name | Hex | RGB | Use |
|------|-----|-----|-----|
| Accent 1 | #[XXXXXX] | rgb(X,X,X) | CTAs, highlights |
| Accent 2 | #[XXXXXX] | rgb(X,X,X) | Secondary actions |

#### Neutral Colors
| Name | Hex | Use |
|------|-----|-----|
| Black | #[XXXXXX] | Text |
| Gray Dark | #[XXXXXX] | Secondary text |
| Gray Light | #[XXXXXX] | Borders, dividers |
| White | #FFFFFF | Backgrounds |

#### Color Accessibility
| Combination | Contrast Ratio | WCAG Level |
|-------------|----------------|------------|
| Primary on White | [X]:1 | [AAA/AA/Fail] |
| White on Primary | [X]:1 | [AAA/AA/Fail] |

### Typography

#### Primary Font
**[Font Name]** - [Google Fonts / Licensed]
| Style | Weight | Use |
|-------|--------|-----|
| Regular | 400 | Body text |
| Medium | 500 | Subheadings |
| Bold | 700 | Headlines |

#### Secondary Font (if applicable)
**[Font Name]**
| Use Case | Style |
|----------|-------|
| [Use] | [Style] |

#### Type Scale
| Element | Size | Weight | Line Height |
|---------|------|--------|-------------|
| H1 | 48px | Bold | 1.2 |
| H2 | 36px | Bold | 1.2 |
| H3 | 24px | Medium | 1.3 |
| Body | 16px | Regular | 1.5 |
| Small | 14px | Regular | 1.4 |
| Caption | 12px | Regular | 1.4 |

### Imagery

#### Photography Style
| Attribute | Guideline |
|-----------|-----------|
| Mood | [Bright/Dark/Moody/etc.] |
| Subjects | [People/Products/Lifestyle] |
| Colors | [On-brand color treatment] |
| Filters | [Specific filter/preset] |

#### Illustration Style (if applicable)
| Attribute | Guideline |
|-----------|-----------|
| Style | [Flat/3D/Hand-drawn] |
| Line weight | [X px] |
| Colors | [From palette] |

#### Stock Image Sources
- [Approved source 1]
- [Approved source 2]

#### Image Don'ts
❌ No low-resolution images  
❌ No images with visible watermarks  
❌ No images that contradict brand values  
❌ No images requiring releases we don't have  

---

## Voice & Tone

### Brand Voice
[2-3 sentences describing personality]

#### Voice Attributes
| Attribute | Description | DO | DON'T |
|-----------|-------------|-----|-------|
| [Friendly] | [Definition] | [Example] | [Example] |
| [Expert] | [Definition] | [Example] | [Example] |
| [Confident] | [Definition] | [Example] | [Example] |

### Tone by Context
| Context | Tone | Example |
|---------|------|---------|
| Social media | Casual, fun | "Hey, you! Ready to..." |
| Email | Warm, helpful | "Hope you're having a great day..." |
| Support | Empathetic, clear | "We understand this is frustrating..." |
| Legal | Professional, precise | "In accordance with..." |

### Writing Guidelines

#### Content Rules
| Rule | Guideline |
|------|-----------|
| Sentence length | Short. Punchy. Clear. |
| Paragraph length | 2-3 sentences max |
| Active voice | Always prefer active |
| Jargon | Avoid unless audience expects it |

#### Language Policy ⚠️

| Audience Age | Language Rules |
|--------------|----------------|
| **All Ages** | No profanity, No innuendo, Family-friendly |
| **13-17** | No profanity, Age-appropriate themes |
| **18+ Only** | Adult language permitted with clear disclosure |

**Current setting:** [All Ages / 13-17 / 18+]

```
IF audience_is_under_18:
    BLOCK: profanity, vulgarity, innuendo, adult themes
ELSE IF audience_is_18_plus AND explicit_content_enabled:
    ALLOW: with prominent age disclosure
ELSE:
    DEFAULT: family-friendly content only
```

#### Prohibited Words/Phrases
| Category | Examples | Reason |
|----------|----------|--------|
| Profanity | [list] | Brand safety |
| Competitors | [list] | Legal risk |
| Superlatives | "best", "guaranteed" | FTC compliance |
| Health claims | [list] | Regulatory |

#### Inclusive Language
| Instead of | Use |
|------------|-----|
| Guys | Everyone, folks, team |
| Crazy/insane | Incredible, amazing |
| Master/slave | Primary/secondary |

---

## Social Media Guidelines

### Platform-Specific

#### TikTok
| Element | Specification |
|---------|---------------|
| Video format | 9:16, 1080x1920 |
| Duration | 15-60 seconds sweet spot |
| Captions | Always on (accessibility) |
| Hashtags | 3-5 relevant |
| CTA | Clear, at end |
| Posting times | [Best times for audience] |

#### Instagram
| Element | Specification |
|---------|---------------|
| Feed posts | 1:1 (1080x1080) or 4:5 |
| Stories | 9:16 (1080x1920) |
| Reels | 9:16 (1080x1920) |
| Captions | Under 125 chars visible |
| Hashtags | 5-10 relevant |

#### Twitter/X
| Element | Specification |
|---------|---------------|
| Tweet length | Under 280, prefer under 200 |
| Images | 16:9 or 1:1 |
| Video | Under 2:20 |
| Threads | Max 5-7 tweets |

### Content Pillars
| Pillar | % of Content | Examples |
|--------|--------------|----------|
| Educational | 40% | Tips, how-tos |
| Entertaining | 30% | Trends, humor |
| Promotional | 20% | Products, offers |
| Community | 10% | UGC, responses |

### Hashtag Strategy
| Type | Examples | Use |
|------|----------|-----|
| Brand | #[BrandName] | Always |
| Campaign | #[CampaignTag] | During campaigns |
| Industry | #[IndustryTag] | Discoverability |
| Trending | [Varies] | When relevant |

---

## Asset Library

### Required Assets
| Asset | Status | Location |
|-------|--------|----------|
| Logo (all formats) | [ ] | `/brand/logo/` |
| Color swatches | [ ] | `/brand/colors/` |
| Font files | [ ] | `/brand/fonts/` |
| Social templates | [ ] | `/brand/social/` |
| Email templates | [ ] | `/brand/email/` |
| Presentation template | [ ] | `/brand/presentations/` |

### Naming Convention
```
[brand]-[asset-type]-[variant]-[size].[ext]
Example: nanoBanana-logo-primary-1200x630.png
```

---

## Approval Workflow

### Every asset requires:
1. Creation by CMO/design
2. Brand compliance check
3. Content moderation check
4. **Human approval** before publication

### Approval Levels
| Content Type | Approver | SLA |
|--------------|----------|-----|
| Social post | Human | 24 hours |
| Campaign creative | Human | 48 hours |
| Brand asset update | Human | 72 hours |
| Legal/sensitive | Human + CLO | ASAP |

---

## Version Control

| Version | Date | Changes | Approved By |
|---------|------|---------|-------------|
| 1.0 | [Date] | Initial brand kit | [Human] |
```

---

## Execution Flow

1. **Gather inputs**
   - Vision from CEO
   - Target audience
   - Competitive landscape

2. **Define foundation**
   - Brand story and values
   - Target audience profile
   - Age gate determination

3. **Create visual identity**
   - Logo concepts (for human review)
   - Color palette
   - Typography

4. **Define voice**
   - Brand personality
   - Tone guidelines
   - Language policy
   - Prohibited content

5. **Build guidelines**
   - Platform-specific rules
   - Asset specifications
   - Approval workflow

---

## Logging

Log to `CMO/logs/YYYY-MM-DD-brand.md`:
```
## Brand Log: [Date]
Action: [Create/Update]
Components updated: [List]
Approval status: PENDING HUMAN APPROVAL
Language policy: [All Ages/13-17/18+]
```

---

## Context

- Run at business inception
- Update when brand evolves
- Foundation for ALL content creation
- MUST be approved by human before any publishing

---

*No brand assets may be published without human approval (GREENLIGHT: BRAND).*
