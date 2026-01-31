# cmo.logo

## Preamble

This command handles logo creation and brand identity asset generation using AI tools with mandatory human approval.

**Must read before execution:**
1. `CMO/.ethics/ethics.md`
2. `CEO/.ceo/memory/vision.md`
3. `CMO/.cmo/commands/cmo.brand.md`

---

## ⚠️ CRITICAL: Logo Approval Required

Logo assets represent the brand permanently. 
**ALL logos require GREENLIGHT: BRAND from human before any use.**

---

## Command Types

```
cmo.logo generate --concept "[description]"
cmo.logo variations --logo-id [id] --type [type]
cmo.logo export --logo-id [id] --formats [list]
cmo.logo approve --logo-id [id]  # Human only
```

---

## Generate: `cmo.logo generate`

### Input

```yaml
# Business context
business_name: "Nano Banana"
tagline: "AI-powered content creation"
industry: "Technology / SaaS"

# Concept direction
concept: "Modern, playful tech company that doesn't take itself too seriously"
symbol_ideas:
  - banana
  - pixel
  - creative spark
  - AI/neural network

# Style preferences
style:
  - minimalist
  - geometric
  - playful
mood:
  - innovative
  - fun
  - trustworthy

# Colors (from brand kit or suggestions)
colors:
  primary: "#FFD700"  # Banana yellow
  secondary: "#1A1A2E"  # Dark tech
  accent: "#4ECDC4"  # Fresh teal

# Technical requirements
variations_needed: 5
include_wordmark: true
include_icon_only: true
```

### Generation Process

```
1. ANALYZE BRAND CONTEXT
   └─ Business name and meaning
   └─ Industry expectations
   └─ Target audience aesthetics
   └─ Competitor logos (what to avoid)

2. DEFINE DESIGN DIRECTION
   └─ 3-5 distinct concept directions
   └─ Each with rationale

3. GENERATE WITH AI
   └─ Create 5 initial concepts
   └─ Apply brand colors
   └─ Include text/wordmark versions

4. PREPARE FOR REVIEW
   └─ Create comparison sheet
   └─ Highlight pros/cons of each
   └─ Note any concerns

5. REQUEST HUMAN APPROVAL
   └─ Send all concepts
   └─ Wait for selection
```

### AI Generation Prompt Template

```
Create a logo for [BUSINESS_NAME]:

Business: [DESCRIPTION]
Industry: [INDUSTRY]
Values: [VALUE_LIST]

Style direction:
- [STYLE 1]
- [STYLE 2]
- [STYLE 3]

Symbol concepts:
- [SYMBOL 1]
- [SYMBOL 2]

Color palette:
- Primary: [HEX]
- Secondary: [HEX]

Requirements:
- Works at 16px (favicon) and 1000px+ sizes
- Clear on both light and dark backgrounds
- Simple enough to be memorable
- Unique enough to be protectable

Create [N] distinct variations with different approaches to the concept.
```

---

## Output: Logo Presentation

```markdown
# 🎨 LOGO CONCEPTS: Nano Banana
Generated: [Date]
Awaiting: GREENLIGHT: BRAND

---

## Concept 1: Geometric Banana

![Concept 1](preview-link)

| Attribute | Detail |
|-----------|--------|
| Style | Minimalist geometric |
| Symbol | Abstract banana shape |
| Colors | Yellow gradient on dark |
| Pros | Modern, scalable, tech-forward |
| Cons | Less playful than alternatives |

---

## Concept 2: Pixel Banana

![Concept 2](preview-link)

| Attribute | Detail |
|-----------|--------|
| Style | Pixelated / retro-digital |
| Symbol | 8-bit style banana |
| Colors | Flat yellow with teal accents |
| Pros | Unique, memorable, fun |
| Cons | May date faster |

---

## Concept 3: Neural Banana

![Concept 3](preview-link)

| Attribute | Detail |
|-----------|--------|
| Style | Abstract neural network |
| Symbol | Banana shape from connected nodes |
| Colors | Yellow nodes, dark connections |
| Pros | Communicates AI clearly |
| Cons | More complex |

---

## Concept 4: [Name]
[...]

## Concept 5: [Name]
[...]

---

## CMO Recommendation

Based on brand strategy and audience analysis:

**Recommended: Concept 2 (Pixel Banana)**

Rationale:
1. Stands out in crowded tech space
2. Memorable and shareable
3. Works well for social media
4. Appeals to creator/Gen Z audience

---

## Next Steps

Reply to approve a concept:
- "APPROVE CONCEPT 1" - Select Concept 1
- "APPROVE CONCEPT 2" - Select Concept 2
- "REVISE [feedback]" - Request new concepts
- "REJECT ALL" - Start over

⚠️ No logo will be used without your explicit approval.
```

---

## Variations: `cmo.logo variations`

Generate variations of an approved logo.

### Variation Types

| Type | Description | Use Case |
|------|-------------|----------|
| `primary` | Main logo (icon + wordmark) | Website header, documents |
| `icon` | Icon only, no text | Favicon, app icon, avatars |
| `wordmark` | Text only, no icon | When icon shown separately |
| `horizontal` | Wide layout | Email signatures, banners |
| `vertical` | Stacked layout | Social profiles |
| `reversed` | For dark backgrounds | Dark mode, video |
| `monochrome` | Single color | Print, embroidery |

### Input

```yaml
logo_id: LOGO-2024-0131-001
types:
  - primary
  - icon
  - wordmark
  - horizontal
  - reversed
  - monochrome
background_checks:
  - white
  - black
  - brand_primary
  - photo_overlay
```

---

## Export: `cmo.logo export`

Export approved logo in all required formats.

### Standard Export Package

```
brand/
├── logo/
│   ├── primary/
│   │   ├── nano-banana-logo-primary.svg      # Vector, scalable
│   │   ├── nano-banana-logo-primary.png      # Transparent
│   │   ├── nano-banana-logo-primary.pdf      # Print
│   │   ├── nano-banana-logo-primary.eps      # Print/design
│   │   └── sizes/
│   │       ├── nano-banana-logo-1200x630.png # OG image
│   │       ├── nano-banana-logo-512x512.png  # App icon
│   │       ├── nano-banana-logo-180x180.png  # Apple touch
│   │       └── nano-banana-logo-32x32.png    # Favicon
│   ├── icon/
│   │   ├── nano-banana-icon.svg
│   │   ├── nano-banana-icon.png
│   │   └── sizes/
│   │       ├── nano-banana-icon-512.png
│   │       ├── nano-banana-icon-192.png
│   │       └── nano-banana-icon-32.png
│   ├── wordmark/
│   │   └── [similar structure]
│   ├── reversed/
│   │   └── [same formats, inverted]
│   └── monochrome/
│       ├── nano-banana-mono-black.svg
│       └── nano-banana-mono-white.svg
├── colors/
│   ├── palette.svg
│   └── palette.pdf
└── fonts/
    └── [font files if licensed]
```

### Export Specifications

| Format | Use | Specs |
|--------|-----|-------|
| SVG | Web, scalable | Optimized, no embedded fonts |
| PNG | Digital use | Transparent background |
| PDF | Print | CMYK color space |
| EPS | Professional design | Vector, editable |
| ICO | Favicon | Multi-size icon file |

---

## Trademark Considerations

### Pre-Approval Checks

```python
def check_logo_trademark(logo: dict) -> dict:
    """
    Basic trademark clearance checks.
    """
    checks = {
        'visual_similarity': check_visual_database(logo),
        'name_availability': check_name_databases(logo['business_name']),
        'domain_availability': check_domain(logo['business_name'])
    }
    
    warnings = []
    
    if checks['visual_similarity']['matches']:
        warnings.append({
            'type': 'visual_similarity',
            'message': 'Similar logos found in database',
            'matches': checks['visual_similarity']['matches'],
            'action': 'Escalate to CLO for full trademark search'
        })
    
    return {
        'preliminary_clear': len(warnings) == 0,
        'warnings': warnings,
        'note': 'This is not legal advice. Full trademark search recommended.'
    }
```

### Escalation to CLO

If similarity detected:
```
→ CMO to CLO: "Logo concept may have trademark issues"
→ CLO runs clo.research for trademark clearance
→ If clear: Proceed with human approval
→ If not clear: Revise or get legal opinion
```

---

## Approval Workflow

```
GENERATE → REVIEW → APPROVE → EXPORT → USE
    │         │         │         │
    ▼         ▼         ▼         ▼
 5 concepts  CMO picks  Human    All formats
 created     top 3     selects   exported
                       one
```

### Approval States

| State | Meaning | Actions Allowed |
|-------|---------|-----------------|
| `draft` | Just generated | View, regenerate |
| `review` | CMO reviewing | Recommend, request more |
| `pending_approval` | With human | Approve, reject, revise |
| `approved` | Human approved | Export, use |
| `archived` | Not selected | Reference only |

---

## Logo Update Process

When updating an existing logo:

1. Load current brand kit
2. Note what's changing and why
3. Generate new concepts
4. Present comparison (old vs new)
5. Human approval required
6. Update all instances
7. Archive old logo (don't delete)

---

## Logging

```sql
INSERT INTO logo_generation (
    logo_id,
    business_id,
    concept_description,
    ai_prompt,
    variations_generated,
    created_at,
    
    -- Review
    cmo_recommendation,
    presented_to_human_at,
    
    -- Approval
    human_decision,
    approved_at,
    approved_by,
    
    -- Export
    exported_formats,
    exported_at,
    
    -- Usage tracking
    first_used_at,
    use_locations
) VALUES (...);
```

---

*All logo assets require GREENLIGHT: BRAND before any use.*
