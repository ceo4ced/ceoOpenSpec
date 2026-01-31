```text
You are Codex. Build a small program that assigns “personality archetypes” to a set of executive AI agents (CEO, CFO, COO, CTO, CPO, CMO, CIO, CLO, EXA, optional Chairman) based on a human’s onboarding flow.

CRITICAL PRIORITY
1) Human ↔ CEO compatibility is the #1 objective.
2) The onboarding must begin by asking the human how they want the CEO to be (tone + behavior + conflict style). Everything else propagates from that.
3) The final output of the application is a CSV file (the agent personality chart). Console output is fine, but CSV is the required artifact.

LEGAL/SAFETY CONSTRAINTS (NON-NEGOTIABLE)
- Do NOT use protected demographic attributes (race, religion, ethnicity, sexual orientation, etc.) to make assignments.
- If the user says “demographics,” interpret as non-sensitive context such as:
  communication style preferences, leadership preferences, formality, culture/region preference (optional), language, timezone, industry context, team maturity, and desired company culture.
- Birthdate is allowed ONLY to compute zodiac for flavor. Treat it as sensitive: ephemeral use by default, don’t store unless user opts in.

GOAL
Given the human’s onboarding answers:
- infer (lightly) the human’s Enneagram + wing and MBTI (simple scoring, not clinical)
- compute western zodiac + chinese zodiac (for flavor)
- ask the human to define:
  A) CEO “vibe” (pleasantness, directness, conflict tolerance, decisiveness, empathy, humor, structure)
  B) desired company culture style (friendly/safe, performance-driven, chaotic startup, high-turnover, “toxic,” etc.)
  C) preferred leadership model (collaborative vs top-down; process-heavy vs improvisational; risk-averse vs risk-seeking)
Then assign personalities to roles such that:
- CEO meets the user’s chosen CEO vibe AND is compatible with the human’s inferred profile
- the rest of the executive team balances the CEO + human profile AND supports the chosen company culture style
- the team remains diverse (avoid too many duplicates of Enneagram cores or MBTI)
- some conflict is allowed (constructive conflict), but destructive conflict depends on the user’s chosen company style

DELIVERABLES
A) Clear algorithm description (step-by-step).
B) Working code (choose Python 3.11 OR TypeScript/Node; pick one and stick to it).
C) A CLI (or main function) that runs the onboarding and writes a CSV:
   - prompts for birthdate (YYYY-MM-DD) for zodiac flavor
   - asks CEO-vibe questions FIRST
   - asks company culture questions SECOND
   - asks onboarding questions to infer human MBTI + Enneagram THIRD
   - outputs:
     1) a short human profile summary (top 3 Enneagram + confidence; top 2 MBTI + confidence; zodiac results)
     2) a role assignment table to console
     3) writes CSV as the primary output artifact

ONBOARDING FLOW (MUST IMPLEMENT IN THIS ORDER)

STEP 0: Identify human’s position in the system
- Ask: “Are you the Chairman, CEO, or other?” (default: Chairman)
- If human is Chairman, ensure Chairman ↔ CEO compatibility is extremely high.

STEP 1: CEO VIBE QUESTIONS (PRIMARY DRIVER)
Ask the human how they want the CEO agent to feel to interact with daily. Use 6–10 questions, Likert 1–5.
Required dimensions:
- Pleasantness: warm/steady vs cold/direct
- Directness: blunt vs tactful
- Conflict style: avoids conflict vs embraces conflict
- Decision cadence: fast vs deliberate
- Structure: process-oriented vs flexible
- Emotional tone: validating vs no-nonsense
- Humor: none vs light vs frequent
- Coaching style: supportive vs challenging
At the end, synthesize a “CEO vibe profile” (tags + target ranges), e.g.:
  tags: pleasant, steady, tactful, decisive, low-drama, firm boundaries
  target MBTI family: (e.g., ISFJ/INFJ/ENFJ) depending on answers
  target Enneagram family: (e.g., 9w8 / 2w1 / 1w9) depending on answers
Also ask explicitly:
- “Do you want the CEO to challenge you sometimes, or mostly keep things calm?” (3 options)

STEP 2: COMPANY CULTURE / ORG STYLE (SECONDARY DRIVER)
Ask 6–10 questions that define the desired company style.
Include:
- culture_mode: one of
  (friendly_safe, performance_driven, high_velocity_startup, regulated_enterprise, high_turnover, intentionally_toxic_simulation)
- tolerance_for_conflict: low/medium/high
- tolerance_for_burnout: low/medium/high
- governance_level: low/medium/high
- innovation_level: low/medium/high
- risk_appetite: low/medium/high
- hiring_bar: low/medium/high
- quality_bar: low/medium/high
IMPORTANT: If the user selects “intentionally_toxic_simulation,” treat it as roleplay intensity only; do NOT recommend real-world harmful practices. The app is about agent personas, not HR advice.

STEP 3: HUMAN PERSONALITY INFERENCE (LIGHTWEIGHT)
Implement two short questionnaires:
A) MBTI: score E/I, S/N, T/F, J/P using ~8–12 questions total (Likert 1–5).
B) Enneagram: score types 1–9 using ~18–27 prompts (2–3 per type). Pick wing by comparing adjacent types.
Output top-3 Enneagram types + confidence and top-2 MBTI types + confidence.

ZODIAC (FOR FLAVOR ONLY)
- Western zodiac: compute from month/day.
- Chinese zodiac: compute animal + element from birth year, accounting for Chinese New Year boundary:
  - Prefer a library if available; otherwise embed a lookup table for Chinese New Year dates (1900–2100) OR implement a known algorithm.
  - Provide fallback: ask “Were you born before Chinese New Year that year?” if boundary uncertain.
- Output Chinese zodiac like “Fire Dragon”.

OUTPUT ROLES
Default roles list:
- CEO, CFO, COO, CTO, CPO, CMO, CIO, CLO, EXA
Optional:
- Chairman (if human is not Chairman, Chairman is an agent too)

PERSONA BUNDLE MODEL
Represent each candidate persona bundle as:
- enneagram_core (1–9)
- wing (e.g., 9w8)
- mbti (one of 16)
- western_zodiac (one of 12) [light weight]
- chinese_zodiac (animal + element) [light weight]
- trait tags (e.g., pleasant, risk, execution, innovation, diplomatic, analytical, intense)
- role_fit_weight (0–1)
- culture_fit_vector: weights per culture_mode (0–1)
You must define a default library of candidate bundles per role (3–8 candidates per role) to allow diversity and selection.

CEO-FIRST PROPAGATION LOGIC (REQUIRED)
- First select/construct the CEO persona bundle:
  - Must satisfy CEO vibe profile constraints
  - Must maximize compatibility with the human personality inference (human↔CEO compatibility weight is highest)
  - Must fit company culture_mode (secondary)
- After CEO selection, propagate to the rest of the org:
  - Choose CFO/COO/CTO/etc. to complement CEO and human while matching company culture_mode.
  - Use “buffers” if conflict tolerance is low:
    - include at least one diplomat/integrator type (e.g., enneagram 9/2/1w9; MBTI Fe-leaning types) in exec layer if needed
  - If culture_mode is high_turnover or intentionally_toxic_simulation:
    - allow more aggressive tension profiles, but still enforce CEO vibe constraints if user wants the CEO pleasant.

COMPATIBILITY + DIVERSITY SCORING (ALGORITHM REQUIREMENTS)
Implement a scoring function to search for an assignment:
total_score =
  + sum(role_fit_weight)
  + sum(culture_fit_vector[culture_mode])
  + human_ceo_bonus (very heavy)
  + chairman_ceo_bonus (heavy when human is Chairman)
  + pairwise_compatibility (moderate)
  + constructive_conflict_bonus (depends on conflict tolerance)
  - destructive_conflict_penalty (depends on conflict tolerance + burnout tolerance)
  - diversity_penalty (soft penalty for duplicates)

Define explainable heuristics:
- MBTI compatibility: complementary vs clashing communication styles (keep simple and transparent)
- Enneagram compatibility: simple synergy rules (no need for perfect theory)
- CEO pleasantness constraint: always enforced from Step 1 answers
- Diversity:
  - penalize repeated Enneagram core across execs
  - penalize repeated MBTI across execs
  - encourage at least 1 “integrator,” 1 “operator,” 1 “risk/governance,” 1 “innovator” among execs

SELECTION METHOD
Use a deterministic and explainable method:
- Beam search (top-k partial assignments) OR greedy+backtracking is fine.
- Must print “why” notes per role:
  - why this persona was selected
  - which constraints it satisfied
  - major tradeoffs
Also output a JSON debug block with scoring breakdown.

ENGINEERING CONSTRAINTS
- Prefer functional style: pure functions for parsing, scoring, selecting; minimal global state.
- No icons/emojis in outputs.
- Include basic tests:
  - western zodiac computation
  - chinese zodiac computation (boundary case)
  - CEO constraints enforced regardless of culture_mode
- Minimal dependencies; if a lunar library isn’t available, use the lookup/fallback approach.

OUTPUT FORMAT (PRIMARY ARTIFACT)
Write a CSV file with columns:
Role, Enneagram, Wing, MBTI, WesternZodiac, ChineseZodiac, Notes
This CSV is the final output for the application.

START NOW
Generate:
1) The algorithm explanation
2) The full working code
3) Example run input/output (brief)
in one response.
```
