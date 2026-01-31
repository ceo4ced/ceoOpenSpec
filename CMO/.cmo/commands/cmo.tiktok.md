# cmo.tiktok

## Preamble

Specialized command for TikTok content creation, optimization, and distribution.

**Must read before execution:**
1. `CMO/.ethics/ethics.md`
2. `CMO/.cmo/memory/brand-kit.md`
3. `CMO/.cmo/asset-pipeline.md`
4. `CMO/.cmo/commands/cmo.content.md`

---

## Command Types

```
cmo.tiktok create --concept "[idea]"
cmo.tiktok trend --query "[topic]"
cmo.tiktok schedule --post-id [id] --time [datetime]
cmo.tiktok analytics --period [7d|30d|90d]
cmo.tiktok optimize --post-id [id]
```

---

## Create: `cmo.tiktok create`

### Input

```yaml
concept: "Behind the scenes of creating AI content"
style: 
  - trending  # trending, educational, funny, storytelling
  - energetic
hook_time: 3  # First X seconds to hook viewer
cta: "Link in bio to try free"
sound: trending  # trending, original, brand-music

# Advanced options
trends_to_leverage:
  - "POV format"
  - "Get ready with me"
duet_enabled: true
stitch_enabled: true
comments_enabled: true
```

### TikTok-Specific Generation

```python
def generate_tiktok_content(concept: dict) -> dict:
    """
    Generate TikTok-optimized content.
    """
    # Structure for TikTok success
    structure = {
        'hook': {
            'duration': '0-3s',
            'goal': 'Stop the scroll',
            'techniques': [
                'Surprising statement',
                'Visual pattern interrupt',
                'Direct address: "You need to see this"',
                'Controversy (brand-safe)'
            ]
        },
        'buildup': {
            'duration': '3-20s',
            'goal': 'Deliver value/entertainment',
            'keep_attention': True
        },
        'payoff': {
            'duration': '20-30s',
            'goal': 'Satisfy the hook promise',
            'cta': concept['cta']
        }
    }
    
    prompt = f"""
    Create TikTok video script:
    
    Concept: {concept['concept']}
    Style: {concept['style']}
    Target: {concept['audience']}
    
    Structure:
    - HOOK (0-3s): Stop scroll immediately
    - BUILDUP (3-20s): {concept['main_content']}
    - PAYOFF (20-30s): {concept['cta']}
    
    Trending elements to incorporate: {concept.get('trends', [])}
    
    Requirements:
    - Vertical format (9:16)
    - Captions included
    - Sound-on optimization
    - Brand colors: {concept['brand_colors']}
    """
    
    return nano_banana_generate(prompt, style='tiktok_viral')
```

---

## Trend: `cmo.tiktok trend`

Research current TikTok trends relevant to brand.

### Input
```yaml
query: "tech products"  # or "our industry"
limit: 10
include_sounds: true
include_hashtags: true
```

### Output

```markdown
# TikTok Trend Report
Generated: [Date]
Query: "tech products"

## Trending Sounds 🎵
| Sound | Uses | Vibe | Brand Fit |
|-------|------|------|-----------|
| [Sound Name] | 2.1M | Energetic | 🟢 Good |
| [Sound Name] | 1.8M | Funny | 🟢 Good |
| [Sound Name] | 1.2M | Emotional | 🟡 Maybe |

## Trending Formats 📱
| Format | Description | Example | Brand Application |
|--------|-------------|---------|-------------------|
| POV | Point of view storytelling | [Link] | Product unboxing POV |
| GRWM | Get ready with me | [Link] | Morning routine + product |
| Tutorial | How-to content | [Link] | How to use our product |

## Trending Hashtags 🏷️
| Hashtag | Views | Relevance |
|---------|-------|-----------|
| #TechTok | 5.2B | 🟢 High |
| #ProductReview | 3.1B | 🟢 High |
| #[BrandRelevant] | 890M | 🟢 High |

## Competitor Activity
| Competitor | Recent Posts | Avg Views | Strategy |
|------------|--------------|-----------|----------|
| [Comp 1] | 5 this week | 45K | Educational |
| [Comp 2] | 3 this week | 120K | Comedy |

## Recommended Content Ideas
1. **[Idea based on trends]**
   - Format: [Type]
   - Sound: [Recommended]
   - Hook: "[Suggested hook]"
   
2. **[Idea 2]**
   ...
```

---

## Schedule: `cmo.tiktok schedule`

Schedule approved content for optimal posting times.

### Optimal Posting Times (US)

| Day | Best Times (EST) | Why |
|-----|------------------|-----|
| Monday | 6am, 10am, 10pm | Morning scroll, lunch, before bed |
| Tuesday | 2am, 4am, 9am | Early risers, commute |
| Wednesday | 7am, 8am, 11pm | Morning routine, night scroll |
| Thursday | 9am, 12pm, 7pm | Work breaks, evening |
| Friday | 5am, 1pm, 3pm | Early, lunch, TGIF |
| Saturday | 11am, 7pm, 8pm | Relaxed morning, evening |
| Sunday | 7am, 8am, 4pm | Morning, afternoon leisure |

### Scheduling Logic

```python
def get_optimal_post_time(
    audience_timezone: str,
    content_type: str,
    day_preference: str = None
) -> datetime:
    """
    Calculate optimal posting time.
    """
    # Get audience analytics
    audience_active_hours = get_audience_analytics()
    
    # Cross-reference with global optimal times
    optimal_times = OPTIMAL_TIMES.get(day_preference or get_best_day())
    
    # Find intersection
    best_time = find_optimal_intersection(
        audience_active_hours,
        optimal_times,
        content_type
    )
    
    return best_time
```

---

## Analytics: `cmo.tiktok analytics`

Analyze TikTok performance.

### Output

```markdown
# TikTok Analytics Report
Period: [Date Range]

## Account Overview
| Metric | Current | vs Previous | Trend |
|--------|---------|-------------|-------|
| Followers | 12,543 | +2,341 (+23%) | 📈 |
| Total Views | 2.4M | +890K (+59%) | 📈 |
| Engagement Rate | 8.2% | +1.2% | 📈 |
| Profile Views | 45,231 | +12,000 | 📈 |

## Content Performance
### Top Performing Posts
| Post | Views | Likes | Comments | Shares | Watch % |
|------|-------|-------|----------|--------|---------|
| [Post 1] | 450K | 45K | 2.1K | 890 | 78% |
| [Post 2] | 320K | 32K | 1.8K | 650 | 72% |
| [Post 3] | 210K | 18K | 980 | 420 | 65% |

### Performance by Content Type
| Type | Avg Views | Avg Engagement | Count |
|------|-----------|----------------|-------|
| Tutorial | 280K | 9.2% | 5 |
| Entertainment | 350K | 7.8% | 8 |
| Behind Scenes | 190K | 11.2% | 3 |

## Audience Insights
| Metric | Value |
|--------|-------|
| Peak Active Time | 7-9 PM EST |
| Top Age Group | 18-24 (45%) |
| Gender Split | 55% F / 45% M |
| Top Locations | US (60%), UK (15%), CA (10%) |

## Recommendations
1. **Post more tutorials** - Highest engagement
2. **Increase frequency** - Gap on Tuesdays
3. **Leverage sound [X]** - Trending with audience
4. **Collaborate with [creator type]** - Audience overlap
```

---

## Optimize: `cmo.tiktok optimize`

Analyze a post and suggest improvements for future content.

### Input
```yaml
post_id: TT-2024-0131-001
analyze: 
  - hook_effectiveness
  - retention_curve
  - engagement_drivers
  - hashtag_performance
```

### Output

```markdown
# Post Optimization Analysis
Post ID: TT-2024-0131-001

## Performance Summary
| Metric | Actual | Benchmark | Rating |
|--------|--------|-----------|--------|
| Views | 45K | 80K avg | 🟡 Below |
| Watch % | 52% | 65% avg | 🟡 Below |
| Engagement | 8.1% | 7.5% avg | 🟢 Good |
| Shares | 2.1% | 1.8% avg | 🟢 Good |

## Retention Analysis
```
100%|████████████░░░░░░░░| 
 75%|███████████████░░░░░| 
 50%|█████████████████████| ← Drop at 12s
 25%|██████████████████████████|
    0s    5s    10s   15s   20s   25s   30s
```
**Critical drop at 12 seconds**

## Issues Identified
1. **Weak hook** - Only 60% retained past 3s
   - Suggestion: Open with more surprising visual
   
2. **Mid-video sag** - Drop at 12s
   - Suggestion: Add pattern interrupt at 10s
   
3. **CTA too late** - Most dropped before CTA
   - Suggestion: Add earlier soft CTA

## Improved Script
```
[0-3s] HOOK: "I made $X with AI and here's exactly how"
       (Show money/result immediately)

[3-10s] BUILDUP: Quick story setup
        (Fast cuts, keep visual interest)

[10-12s] PATTERN INTERRUPT: Unexpected visual
        (Prevent mid-video drop)

[12-25s] VALUE: Actual content/tutorial
        (Deliver on hook promise)

[25-30s] CTA: "Link in bio for free trial"
        (Clear, simple action)
```

## A/B Test Suggestions
| Element | Version A | Version B |
|---------|-----------|-----------|
| Hook | "[Current]" | "[Suggested]" |
| Thumbnail | Face close-up | Text overlay |
| CTA timing | 25s | 15s (earlier) |
```

---

## Content Rules (TikTok-Specific)

### Do's ✅
- Hook in first 1-3 seconds
- Use trending sounds when brand-appropriate
- Enable duets and stitches (builds community)
- Reply to comments with video
- Post consistently (min 1x/day optimal)
- Use captions (85% watch without sound)

### Don'ts ❌
- No watermarks from other platforms
- No overly salesy content (blend in)
- No low-quality video/audio
- No community guideline violations
- No engagement bait ("Like if you agree")

### FTC Requirements
| Disclosure Type | When Required |
|-----------------|---------------|
| #Ad / #Sponsored | Paid partnerships |
| #Gifted | Free products for review |
| Branded content toggle | All brand deals |

---

## Integration with Nano Banana

### Content Generation Pipeline

```
1. Research trends (cmo.tiktok trend)
         ↓
2. Define concept based on trends + brand
         ↓
3. Generate script with Nano Banana
         ↓
4. Generate visuals/video with Nano Banana
         ↓
5. Apply brand overlays (logo, colors)
         ↓
6. Content moderation check
         ↓
7. Human approval request
         ↓
8. Schedule for optimal time
         ↓
9. Publish
         ↓
10. Track analytics
```

---

## Logging

All TikTok activity logged to BigQuery:

```sql
-- TikTok content log
CREATE TABLE tiktok_content (
    post_id STRING,
    business_id STRING,
    
    -- Creation
    concept STRING,
    script STRING,
    nano_banana_prompt STRING,
    created_at TIMESTAMP,
    
    -- Approval
    moderation_passed BOOL,
    human_approved BOOL,
    approved_at TIMESTAMP,
    
    -- Publication
    published_at TIMESTAMP,
    tiktok_post_id STRING,
    url STRING,
    
    -- Performance (updated hourly)
    views INT64,
    likes INT64,
    comments INT64,
    shares INT64,
    watch_percentage FLOAT64,
    
    last_updated TIMESTAMP
);
```

---

*All TikTok content requires human approval before publication.*
