# cmo.website

## Preamble

This command creates specifications for promotional/marketing websites and landing pages.

**Must read before execution:**
1. `.mission/agent-governance.md`
2. `CMO/.ethics/ethics.md`
3. `CEO/.ceo/memory/business-plan.md` (if exists)
4. Brand guidelines (if exist)

---

## Outline

Define website requirements, structure, and content for marketing purposes.

### Website Specification Template

```markdown
# Website Specification: [Site Name]
Generated: [Date]
Type: [Landing Page / Marketing Site / Product Site]

## Overview

| Element | Details |
|---------|---------|
| Purpose | [Primary goal] |
| Target Audience | [Who] |
| Primary CTA | [What action] |
| Launch Target | [Date] |
| Domain | [Domain name] |

---

## Business Objectives

### Primary Objective
[What is this site supposed to accomplish?]

### Conversion Goals
| Goal | Target | Measurement |
|------|--------|-------------|
| [Goal 1] | [Target] | [How measured] |
| [Goal 2] | [Target] | [How measured] |

### Success Metrics
| Metric | Baseline | Target |
|--------|----------|--------|
| Conversion Rate | N/A | X% |
| Bounce Rate | N/A | <X% |
| Time on Site | N/A | >X sec |
| Email Signups | N/A | X/month |

---

## Site Architecture

### Page Structure
```
Home
├── Features
├── Pricing
├── About
├── Contact
├── Blog (optional)
├── Privacy Policy
└── Terms of Service
```

### For Landing Page
```
Single Page:
├── Hero Section
├── Problem Statement
├── Solution/Benefits
├── Social Proof
├── Features (brief)
├── CTA Section
├── FAQ
└── Footer (legal links)
```

---

## Page Specifications

### Hero Section
| Element | Specification |
|---------|---------------|
| Headline | [Main value prop, <10 words] |
| Subheadline | [Supporting copy, 1-2 sentences] |
| CTA Button | [Button text] |
| Visual | [Image/video description] |
| Above Fold | Everything visible without scrolling |

### Problem/Solution
| Element | Specification |
|---------|---------------|
| Problem Statement | [Pain point we address] |
| Solution | [How we solve it] |
| Key Benefits | [3-5 bullet points] |

### Social Proof
| Type | Quantity | Source |
|------|----------|--------|
| Testimonials | [#] | [Where from] |
| Logos | [#] | [Which companies] |
| Statistics | [#] | [What metrics] |
| Press mentions | [#] | [Which outlets] |

⚠️ All testimonials must be genuine. See CLO for compliance.

### Features
| Feature | Headline | Description | Visual |
|---------|----------|-------------|--------|
| [Feature 1] | [Headline] | [2-3 sentences] | [Icon/Screenshot] |
| [Feature 2] | [Headline] | [2-3 sentences] | [Icon/Screenshot] |
| [Feature 3] | [Headline] | [2-3 sentences] | [Icon/Screenshot] |

### Pricing (if applicable)
| Plan | Price | Features | CTA |
|------|-------|----------|-----|
| [Plan 1] | $X/mo | [Features] | [Button] |
| [Plan 2] | $X/mo | [Features] | [Button] |
| [Plan 3] | $X/mo | [Features] | [Button] |

### FAQ
| Question | Answer |
|----------|--------|
| [Q1] | [A1] |
| [Q2] | [A2] |
| [Q3] | [A3] |

---

## Content Requirements

### Copy Needs
| Section | Word Count | Status |
|---------|------------|--------|
| Hero | 50-100 | [ ] |
| Problem/Solution | 150-200 | [ ] |
| Features | 100-150 each | [ ] |
| Testimonials | 50-100 each | [ ] |
| FAQ | 50-100 each | [ ] |
| Legal pages | Standard | [ ] |

### Visual Assets
| Asset | Specs | Status |
|-------|-------|--------|
| Hero image/video | [Dimensions] | [ ] |
| Feature icons | [Size] × [#] | [ ] |
| Screenshots | [Dimensions] × [#] | [ ] |
| Testimonial photos | [Size] × [#] | [ ] |
| Logo variations | [Sizes needed] | [ ] |

---

## Technical Requirements

### Platform
| Option | Pros | Cons | Recommendation |
|--------|------|------|----------------|
| Framer | Fast, visual, hosting | Learning curve | Marketing sites |
| Webflow | Flexible, visual | Cost | Complex sites |
| Next.js | Full control | Dev needed | Product sites |
| WordPress | Familiar | Maintenance | Content-heavy |

**Recommendation:** [Platform]

### Performance Requirements
| Metric | Target |
|--------|--------|
| First Contentful Paint | <1.5s |
| Largest Contentful Paint | <2.5s |
| Time to Interactive | <3s |
| Mobile Score | >90 |

### SEO Requirements
| Element | Requirement |
|---------|-------------|
| Meta title | <60 chars, keyword focus |
| Meta description | <160 chars, compelling |
| H1 | One per page, keyword |
| Image alt text | Descriptive |
| URL structure | Clean, readable |
| Sitemap | Auto-generated |
| Robots.txt | Configured |

### Mobile Requirements
- Responsive at all breakpoints
- Mobile-first design priority
- Touch-friendly buttons (min 44px)
- No horizontal scroll

---

## Integrations

| Integration | Purpose | Provider |
|-------------|---------|----------|
| Analytics | Traffic tracking | Google Analytics 4 |
| Form handling | Lead capture | [Provider] |
| Email | Newsletter | [Provider] |
| Chat | Support | [Provider] |
| Payment | Transactions | [Provider] |
| CRM | Lead management | [Provider] |

---

## Legal Requirements

### Required Pages
- [ ] Privacy Policy → CLO
- [ ] Terms of Service → CLO
- [ ] Cookie Policy (if EU) → CLO

### Compliance
- [ ] Cookie consent banner (if EU users)
- [ ] CCPA "Do Not Sell" link (if CA users)
- [ ] Accessibility (WCAG 2.1 AA)
- [ ] Ad disclosure (if paid promotion)

→ Escalate to CLO for legal review

---

## Design Guidelines

### Brand Elements
| Element | Specification |
|---------|---------------|
| Primary Color | [Hex] |
| Secondary Color | [Hex] |
| Typography | [Font family] |
| Heading Font | [Font family] |
| Button Style | [Rounded/Square/etc.] |
| Logo Usage | [Guidelines] |

### Design References
[Links to inspiration or mood boards]

---

## Launch Checklist

### Pre-Launch
- [ ] All content reviewed and approved
- [ ] All links tested
- [ ] Forms tested
- [ ] Analytics installed
- [ ] SEO meta tags set
- [ ] Performance tested
- [ ] Mobile tested
- [ ] Legal pages live
- [ ] SSL certificate
- [ ] Backup configured

### Launch
- [ ] DNS pointed
- [ ] SSL verified
- [ ] 301 redirects (if migrating)
- [ ] Verify in Google Search Console
- [ ] Submit sitemap

### Post-Launch
- [ ] Monitor analytics
- [ ] Check for 404s
- [ ] Test conversions
- [ ] Gather feedback

---

## Timeline

| Phase | Duration | Tasks |
|-------|----------|-------|
| Planning | [X days] | This spec, approvals |
| Design | [X days] | Wireframes, mockups |
| Development | [X days] | Build, integrate |
| Content | [X days] | Copy, assets |
| QA | [X days] | Testing |
| Launch | [Date] | Go live |

---

## Approvals Required

- [ ] CMO content approval
- [ ] CLO legal review
- [ ] CIO technical review (if complex)
- [ ] CEO final approval
- [ ] **GREENLIGHT** from Human
```

---

## Execution Flow

1. **Define objectives**
   - What should the site accomplish?
   - Who is the audience?

2. **Plan structure**
   - What pages needed?
   - What's the user journey?

3. **Specify content**
   - What copy for each section?
   - What visuals needed?

4. **Technical planning**
   - What platform?
   - What integrations?

5. **Legal compliance**
   - Privacy, terms, accessibility
   - Escalate to CLO

---

## Logging

Log to `CMO/logs/YYYY-MM-DD-website.md`:
```
## Website Log: [Date]
Site: [Name]
Type: [Landing/Marketing/Product]
Platform: [Selected platform]
Pages: [Count]
Launch target: [Date]
Status: [Spec/Design/Dev/Live]
```

---

## Context

- Run when launching new marketing presence
- Coordinate with CTO for technical build
- Legal review required before launch
- Feeds into marketing campaigns

---

*Website launches require human approval (GREENLIGHT).*
