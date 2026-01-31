import csv
import hashlib
import json
import math
import os
import random
import urllib.error
import urllib.request
from dataclasses import dataclass
from datetime import date, datetime
from typing import Dict, List, Optional, Tuple
from PIL import Image, ImageDraw, ImageFont

CULTURE_MODES = [
    "friendly_safe",
    "performance_driven",
    "high_velocity_startup",
    "regulated_enterprise",
    "high_turnover",
    "intentionally_toxic_simulation",
]

ROLE_ORDER_DEFAULT = ["CEO", "CFO", "COO", "CTO", "CPO", "CMO", "CIO", "CLO", "CXA"]
WESTERN_ZODIAC_LIST = [
    "Aries",
    "Taurus",
    "Gemini",
    "Cancer",
    "Leo",
    "Virgo",
    "Libra",
    "Scorpio",
    "Sagittarius",
    "Capricorn",
    "Aquarius",
    "Pisces",
]

INTEGRATOR_TAGS = {"integrator", "diplomatic", "supportive", "people"}
OPERATOR_TAGS = {"operator", "execution", "process", "structured"}
GOVERNANCE_TAGS = {"governance", "risk", "compliance"}
INNOVATOR_TAGS = {"innovator", "creative", "vision", "experimental"}

AXES = [
    "pleasantness",
    "directness",
    "conflict",
    "decisiveness",
    "structure",
    "emotional_tone",
    "humor",
    "coaching",
]


@dataclass(frozen=True)
class PersonaBundle:
    persona_id: str
    enneagram_core: int
    wing: str
    mbti: str
    western_zodiac: str
    chinese_zodiac: str
    trait_tags: Tuple[str, ...]
    role_fit_weight: float
    culture_fit_vector: Dict[str, float]


@dataclass
class HumanProfile:
    top_enneagram: List[Tuple[int, float]]
    top_mbti: List[Tuple[str, float]]
    western_zodiac: str
    chinese_zodiac: str
    raw_mbti_scores: Dict[str, float]
    raw_enneagram_scores: Dict[int, float]


@dataclass
class VibeProfile:
    axes: Dict[str, int]
    tags: List[str]
    target_mbti_family: List[str]
    target_enneagram_family: List[str]
    challenge_preference: str


@dataclass
class CultureProfile:
    culture_mode: str
    tolerance_for_conflict: str
    conflict_emphasis: str
    tolerance_for_burnout: str
    governance_level: str
    innovation_level: str
    risk_appetite: str
    hiring_bar: str
    quality_bar: str


@dataclass(frozen=True)
class CultureCard:
    name: str
    description: str
    defaults: Dict[str, str]


@dataclass(frozen=True)
class SelectionConfig:
    randomness_level: str
    ceo_originality: str
    rng: random.Random
    seed_label: str


@dataclass
class Assignment:
    roles: Dict[str, PersonaBundle]
    score: float
    breakdown: Dict[str, Dict[str, float]]
    notes: Dict[str, str]
    image_prompts: Dict[str, str]
    image_prompts: Dict[str, str]
    backstories: Dict[str, str]
    image_paths: Dict[str, str]


RANDOMNESS_LEVELS = ["low", "medium", "high"]
CEO_ORIGINALITY_LEVELS = ["subtle", "balanced", "bold"]

CULTURE_CARDS = [
    CultureCard(
        "Calm Craft",
        "steady pace, care-first, polish over rush",
        {
            "culture_mode": "friendly_safe",
            "tolerance_for_conflict": "low",
            "conflict_emphasis": "low",
            "tolerance_for_burnout": "low",
            "governance_level": "medium",
            "innovation_level": "medium",
            "risk_appetite": "low",
            "hiring_bar": "medium",
            "quality_bar": "high",
        },
    ),
    CultureCard(
        "Competitive Drive",
        "goal-forward, crisp feedback, wins as fuel",
        {
            "culture_mode": "performance_driven",
            "tolerance_for_conflict": "high",
            "conflict_emphasis": "high",
            "tolerance_for_burnout": "medium",
            "governance_level": "medium",
            "innovation_level": "medium",
            "risk_appetite": "medium",
            "hiring_bar": "high",
            "quality_bar": "medium",
        },
    ),
    CultureCard(
        "Exploration Lab",
        "experiments over certainty, fast learning loops",
        {
            "culture_mode": "high_velocity_startup",
            "tolerance_for_conflict": "medium",
            "conflict_emphasis": "medium",
            "tolerance_for_burnout": "medium",
            "governance_level": "low",
            "innovation_level": "high",
            "risk_appetite": "high",
            "hiring_bar": "medium",
            "quality_bar": "medium",
        },
    ),
    CultureCard(
        "Guarded Precision",
        "high standards, guardrails, low variance",
        {
            "culture_mode": "regulated_enterprise",
            "tolerance_for_conflict": "low",
            "conflict_emphasis": "medium",
            "tolerance_for_burnout": "low",
            "governance_level": "high",
            "innovation_level": "low",
            "risk_appetite": "low",
            "hiring_bar": "high",
            "quality_bar": "high",
        },
    ),
    CultureCard(
        "Builder's Sprint",
        "short iterations, bold bets, playful urgency",
        {
            "culture_mode": "high_velocity_startup",
            "tolerance_for_conflict": "medium",
            "conflict_emphasis": "high",
            "tolerance_for_burnout": "high",
            "governance_level": "low",
            "innovation_level": "high",
            "risk_appetite": "high",
            "hiring_bar": "high",
            "quality_bar": "medium",
        },
    ),
    CultureCard(
        "Resilient Core",
        "steady trust, low drama, long-horizon focus",
        {
            "culture_mode": "friendly_safe",
            "tolerance_for_conflict": "low",
            "conflict_emphasis": "low",
            "tolerance_for_burnout": "low",
            "governance_level": "medium",
            "innovation_level": "low",
            "risk_appetite": "low",
            "hiring_bar": "medium",
            "quality_bar": "high",
        },
    ),
    CultureCard(
        "Operator's Rhythm",
        "process-first, dependable tempo, measured risk",
        {
            "culture_mode": "regulated_enterprise",
            "tolerance_for_conflict": "medium",
            "conflict_emphasis": "medium",
            "tolerance_for_burnout": "low",
            "governance_level": "high",
            "innovation_level": "low",
            "risk_appetite": "low",
            "hiring_bar": "medium",
            "quality_bar": "high",
        },
    ),
    CultureCard(
        "Pressure Heat",
        "simulated intensity, thin buffers, fast cycles",
        {
            "culture_mode": "high_turnover",
            "tolerance_for_conflict": "high",
            "conflict_emphasis": "high",
            "tolerance_for_burnout": "high",
            "governance_level": "low",
            "innovation_level": "medium",
            "risk_appetite": "high",
            "hiring_bar": "medium",
            "quality_bar": "medium",
        },
    ),
]


# ---------- Prompt helpers ----------

def prompt_text(prompt: str, default: Optional[str] = None) -> str:
    while True:
        suffix = f" [{default}]" if default else ""
        value = input(f"{prompt}{suffix}: ").strip()
        if value:
            return value
        if default is not None:
            return default


def prompt_likert(prompt: str, minimum: int = 1, maximum: int = 5, default: int = 3) -> int:
    while True:
        value = input(f"{prompt} ({minimum}-{maximum}) [{default}]: ").strip()
        if not value:
            return default
        if value.isdigit():
            num = int(value)
            if minimum <= num <= maximum:
                return num
        print("Please enter a number between 1 and 5.")


def prompt_choice(prompt: str, options: List[str], default_index: Optional[int] = None) -> str:
    for i, option in enumerate(options, start=1):
        print(f"  {i}) {option}")
    while True:
        default_note = f" [{default_index}]" if default_index is not None else ""
        value = input(f"{prompt}{default_note}: ").strip()
        if not value and default_index is not None:
            return options[default_index - 1]
        if value.isdigit():
            idx = int(value)
            if 1 <= idx <= len(options):
                return options[idx - 1]
        print("Please enter a valid option number.")


def prompt_int(prompt: str, minimum: int, maximum: int, default: Optional[int] = None) -> int:
    while True:
        suffix = f" [{default}]" if default is not None else ""
        value = input(f"{prompt}{suffix}: ").strip()
        if not value and default is not None:
            return default
        if value.isdigit():
            num = int(value)
            if minimum <= num <= maximum:
                return num
        print(f"Please enter a number between {minimum} and {maximum}.")


def prompt_mbti(prompt: str, default: Optional[str] = None) -> str:
    while True:
        value = prompt_text(prompt, default=default).upper()
        if len(value) == 4 and value[0] in "EI" and value[1] in "SN" and value[2] in "TF" and value[3] in "JP":
            return value
        print("Please enter a valid 4-letter MBTI (e.g., ENFJ).")


def prompt_western_zodiac(prompt: str, default: Optional[str] = None) -> str:
    options = WESTERN_ZODIAC_LIST + ["Unknown"]
    default_index = options.index(default) + 1 if default in options else None
    return prompt_choice(prompt, options, default_index=default_index)


def default_index(options: List[str], default_value: Optional[str], fallback_index: int) -> int:
    if default_value in options:
        return options.index(default_value) + 1
    return fallback_index


def stable_seed(seed_material: str) -> int:
    digest = hashlib.sha256(seed_material.encode("utf-8")).hexdigest()
    return int(digest[:16], 16)


def build_rng(seed_phrase: str) -> Tuple[random.Random, str]:
    cleaned = seed_phrase.strip()
    if cleaned:
        seed_label = cleaned
    else:
        nonce = random.SystemRandom().randint(100000, 999999)
        stamp = datetime.utcnow().strftime("%Y%m%d-%H%M%S")
        seed_label = f"mix-{stamp}-{nonce}"
    rng = random.Random(stable_seed(seed_label))
    return rng, seed_label


def selection_tuning(level: str) -> Tuple[float, float, int]:
    tuning = {
        "low": (0.0, 0.25, 1),
        "medium": (0.06, 0.6, 3),
        "high": (0.12, 1.0, 5),
    }
    return tuning.get(level, tuning["medium"])


def softmax_sample(assignments: List[Assignment], rng: random.Random, temperature: float) -> Assignment:
    if not assignments:
        raise ValueError("No assignments available for sampling.")
    if len(assignments) == 1:
        return assignments[0]
    max_score = max(a.score for a in assignments)
    temp = max(temperature, 0.05)
    weights = [math.exp((a.score - max_score) / temp) for a in assignments]
    return rng.choices(assignments, weights=weights, k=1)[0]


# ---------- Zodiac ----------

def western_zodiac(month: int, day: int) -> str:
    if (month == 3 and day >= 21) or (month == 4 and day <= 19):
        return "Aries"
    if (month == 4 and day >= 20) or (month == 5 and day <= 20):
        return "Taurus"
    if (month == 5 and day >= 21) or (month == 6 and day <= 20):
        return "Gemini"
    if (month == 6 and day >= 21) or (month == 7 and day <= 22):
        return "Cancer"
    if (month == 7 and day >= 23) or (month == 8 and day <= 22):
        return "Leo"
    if (month == 8 and day >= 23) or (month == 9 and day <= 22):
        return "Virgo"
    if (month == 9 and day >= 23) or (month == 10 and day <= 22):
        return "Libra"
    if (month == 10 and day >= 23) or (month == 11 and day <= 21):
        return "Scorpio"
    if (month == 11 and day >= 22) or (month == 12 and day <= 21):
        return "Sagittarius"
    if (month == 12 and day >= 22) or (month == 1 and day <= 19):
        return "Capricorn"
    if (month == 1 and day >= 20) or (month == 2 and day <= 18):
        return "Aquarius"
    return "Pisces"


# Chinese New Year calculation based on a widely-used lunar algorithm (Ho Ngoc Duc).
# Works reliably for years 1900-2100. Uses timezone +8 (China Standard Time).

def _jd_from_date(dd: int, mm: int, yy: int) -> int:
    a = (14 - mm) // 12
    y = yy + 4800 - a
    m = mm + 12 * a - 3
    jd = dd + (153 * m + 2) // 5 + 365 * y + y // 4 - y // 100 + y // 400 - 32045
    if jd < 2299161:
        jd = dd + (153 * m + 2) // 5 + 365 * y + y // 4 - 32083
    return jd


def _jd_to_date(jd: int) -> date:
    if jd > 2299160:
        a = jd + 32044
        b = (4 * a + 3) // 146097
        c = a - (146097 * b) // 4
    else:
        b = 0
        c = jd + 32082
    d = (4 * c + 3) // 1461
    e = c - (1461 * d) // 4
    m = (5 * e + 2) // 153
    day = e - (153 * m + 2) // 5 + 1
    month = m + 3 - 12 * (m // 10)
    year = b * 100 + d - 4800 + (m // 10)
    return date(year, month, day)


def _new_moon(k: float) -> float:
    from math import sin, pi

    t = k / 1236.85
    t2 = t * t
    t3 = t2 * t
    dr = pi / 180

    jd1 = 2415020.75933 + 29.53058868 * k + 0.0001178 * t2 - 0.000000155 * t3
    jd1 += 0.00033 * sin((166.56 + 132.87 * t - 0.009173 * t2) * dr)

    m = 359.2242 + 29.10535608 * k - 0.0000333 * t2 - 0.00000347 * t3
    mpr = 306.0253 + 385.81691806 * k + 0.0107306 * t2 + 0.00001236 * t3
    f = 21.2964 + 390.67050646 * k - 0.0016528 * t2 - 0.00000239 * t3

    c1 = (
        (0.1734 - 0.000393 * t) * sin(m * dr)
        + 0.0021 * sin(2 * m * dr)
        - 0.4068 * sin(mpr * dr)
        + 0.0161 * sin(2 * mpr * dr)
        - 0.0004 * sin(3 * mpr * dr)
        + 0.0104 * sin(2 * f * dr)
        - 0.0051 * sin((m + mpr) * dr)
        - 0.0074 * sin((m - mpr) * dr)
        + 0.0004 * sin((2 * f + m) * dr)
        - 0.0004 * sin((2 * f - m) * dr)
        - 0.0006 * sin((2 * f + mpr) * dr)
        + 0.0010 * sin((2 * f - mpr) * dr)
        + 0.0005 * sin((2 * mpr + m) * dr)
    )

    if t < -11:
        delta_t = (
            0.001
            + 0.000839 * t
            + 0.0002261 * t2
            - 0.00000845 * t3
            - 0.000000081 * t * t3
        )
    else:
        delta_t = -0.000278 + 0.000265 * t + 0.000262 * t2

    return jd1 + c1 - delta_t


def _sun_longitude(jdn: float) -> float:
    from math import sin, pi

    t = (jdn - 2451545.0) / 36525
    t2 = t * t
    dr = pi / 180

    m = 357.52910 + 35999.05030 * t - 0.0001559 * t2 - 0.00000048 * t * t2
    l0 = 280.46645 + 36000.76983 * t + 0.0003032 * t2
    dl = (
        (1.914600 - 0.004817 * t - 0.000014 * t2) * sin(m * dr)
        + (0.019993 - 0.000101 * t) * sin(2 * m * dr)
        + 0.000290 * sin(3 * m * dr)
    )
    l = l0 + dl
    l = l * dr
    l = l - 2 * pi * int(l / (2 * pi))
    return l


def _get_new_moon_day(k: int, time_zone: float) -> int:
    return int(_new_moon(k) + 0.5 + time_zone / 24)


def _get_sun_longitude(day_number: int, time_zone: float) -> int:
    return int(_sun_longitude(day_number - 0.5 - time_zone / 24) / (3.141592653589793 / 6))


def _get_lunar_month11(year: int, time_zone: float) -> int:
    off = _jd_from_date(31, 12, year) - 2415021
    k = int(off / 29.530588853)
    nm = _get_new_moon_day(k, time_zone)
    sun_long = _get_sun_longitude(nm, time_zone)
    if sun_long >= 9:
        nm = _get_new_moon_day(k - 1, time_zone)
    return nm


def _get_leap_month_offset(a11: int, time_zone: float) -> int:
    k = int(0.5 + (a11 - 2415021.076998695) / 29.530588853)
    last = 0
    i = 1
    arc = _get_sun_longitude(_get_new_moon_day(k + i, time_zone), time_zone)
    while arc != last and i < 14:
        last = arc
        i += 1
        arc = _get_sun_longitude(_get_new_moon_day(k + i, time_zone), time_zone)
    return i - 1


def _convert_lunar_to_solar(lunar_day: int, lunar_month: int, lunar_year: int, lunar_leap: int, time_zone: float) -> date:
    if lunar_month < 11:
        a11 = _get_lunar_month11(lunar_year - 1, time_zone)
        b11 = _get_lunar_month11(lunar_year, time_zone)
    else:
        a11 = _get_lunar_month11(lunar_year, time_zone)
        b11 = _get_lunar_month11(lunar_year + 1, time_zone)

    k = int(0.5 + (a11 - 2415021.076998695) / 29.530588853)
    off = lunar_month - 11
    if off < 0:
        off += 12

    if b11 - a11 > 365:
        leap_off = _get_leap_month_offset(a11, time_zone)
        leap_month = leap_off - 2
        if leap_month < 0:
            leap_month += 12
        if lunar_leap != 0 and lunar_month != leap_month:
            raise ValueError("Invalid lunar leap month")
        if lunar_leap != 0 or off >= leap_off:
            off += 1

    month_start = _get_new_moon_day(k + off, time_zone)
    return _jd_to_date(month_start + lunar_day - 1)


def chinese_new_year_date(year: int) -> Optional[date]:
    if year < 1900 or year > 2100:
        return None
    return _convert_lunar_to_solar(1, 1, year, 0, 8)


def chinese_zodiac_for_date(birth_date: date, boundary_answer: Optional[str] = None) -> str:
    cny = chinese_new_year_date(birth_date.year)
    zodiac_year = birth_date.year
    if cny is None:
        if boundary_answer is None:
            return "Unknown"
        if boundary_answer == "yes":
            zodiac_year -= 1
    else:
        if birth_date < cny:
            zodiac_year -= 1

    animals = [
        "Rat",
        "Ox",
        "Tiger",
        "Rabbit",
        "Dragon",
        "Snake",
        "Horse",
        "Goat",
        "Monkey",
        "Rooster",
        "Dog",
        "Pig",
    ]
    elements = [
        "Wood",
        "Wood",
        "Fire",
        "Fire",
        "Earth",
        "Earth",
        "Metal",
        "Metal",
        "Water",
        "Water",
    ]

    offset = (zodiac_year - 1984) % 60
    animal = animals[offset % 12]
    element = elements[offset % 10]
    return f"{element} {animal}"


# ---------- Vibe and culture ----------

def synthesize_vibe_profile(axes: Dict[str, int], challenge_preference: str) -> VibeProfile:
    tags = []
    if axes["pleasantness"] >= 4:
        tags.append("pleasant")
    elif axes["pleasantness"] <= 2:
        tags.append("reserved")
    if axes["directness"] >= 4:
        tags.append("direct")
    elif axes["directness"] <= 2:
        tags.append("tactful")
    if axes["conflict"] >= 4:
        tags.append("conflict-forward")
    elif axes["conflict"] <= 2:
        tags.append("conflict-averse")
    if axes["decisiveness"] >= 4:
        tags.append("decisive")
    elif axes["decisiveness"] <= 2:
        tags.append("deliberate")
    if axes["structure"] >= 4:
        tags.append("structured")
    elif axes["structure"] <= 2:
        tags.append("flexible")
    if axes["emotional_tone"] >= 4:
        tags.append("validating")
    elif axes["emotional_tone"] <= 2:
        tags.append("no-nonsense")
    if axes["humor"] >= 4:
        tags.append("playful")
    elif axes["humor"] <= 2:
        tags.append("serious")
    if axes["coaching"] >= 4:
        tags.append("supportive")
    elif axes["coaching"] <= 2:
        tags.append("challenging")

    mbti_scores = {"NF": 0, "SF": 0, "NT": 0, "ST": 0}
    if axes["pleasantness"] >= 4 or axes["emotional_tone"] >= 4:
        mbti_scores["NF"] += 2
        mbti_scores["SF"] += 1
    if axes["directness"] >= 4 or axes["decisiveness"] >= 4:
        mbti_scores["NT"] += 2
        mbti_scores["ST"] += 1
    if axes["structure"] >= 4:
        mbti_scores["ST"] += 1
        mbti_scores["NT"] += 1
    if axes["structure"] <= 2:
        mbti_scores["NF"] += 1
        mbti_scores["NT"] += 1

    target_mbti_family = [k for k, _ in sorted(mbti_scores.items(), key=lambda kv: kv[1], reverse=True)][:2]

    enneagram_scores = {1: 0, 2: 0, 3: 0, 8: 0, 9: 0, 7: 0}
    if axes["pleasantness"] >= 4:
        enneagram_scores[2] += 2
        enneagram_scores[9] += 2
    if axes["directness"] >= 4 or axes["conflict"] >= 4:
        enneagram_scores[8] += 2
        enneagram_scores[1] += 1
    if axes["structure"] >= 4:
        enneagram_scores[1] += 2
    if axes["humor"] >= 4:
        enneagram_scores[7] += 2
    if axes["decisiveness"] >= 4:
        enneagram_scores[3] += 2

    target_enneagram_family = [str(k) for k, _ in sorted(enneagram_scores.items(), key=lambda kv: kv[1], reverse=True)][:3]

    return VibeProfile(
        axes=axes,
        tags=tags,
        target_mbti_family=target_mbti_family,
        target_enneagram_family=target_enneagram_family,
        challenge_preference=challenge_preference,
    )


def culture_profile_from_inputs(defaults: Optional[Dict[str, str]] = None) -> CultureProfile:
    defaults = defaults or {}
    culture_mode = prompt_choice(
        "Choose the company culture mode",
        CULTURE_MODES,
        default_index=default_index(CULTURE_MODES, defaults.get("culture_mode"), 1),
    )
    tolerance_for_conflict = prompt_choice(
        "Conflict tolerance",
        ["low", "medium", "high"],
        default_index=default_index(
            ["low", "medium", "high"], defaults.get("tolerance_for_conflict"), 2
        ),
    )
    conflict_emphasis = prompt_choice(
        "Value of constructive conflict",
        ["low", "medium", "high"],
        default_index=default_index(
            ["low", "medium", "high"], defaults.get("conflict_emphasis"), 2
        ),
    )
    tolerance_for_burnout = prompt_choice(
        "Burnout tolerance",
        ["low", "medium", "high"],
        default_index=default_index(
            ["low", "medium", "high"], defaults.get("tolerance_for_burnout"), 2
        ),
    )
    governance_level = prompt_choice(
        "Governance level",
        ["low", "medium", "high"],
        default_index=default_index(
            ["low", "medium", "high"], defaults.get("governance_level"), 2
        ),
    )
    innovation_level = prompt_choice(
        "Innovation level",
        ["low", "medium", "high"],
        default_index=default_index(
            ["low", "medium", "high"], defaults.get("innovation_level"), 2
        ),
    )
    risk_appetite = prompt_choice(
        "Risk appetite",
        ["low", "medium", "high"],
        default_index=default_index(
            ["low", "medium", "high"], defaults.get("risk_appetite"), 2
        ),
    )
    hiring_bar = prompt_choice(
        "Hiring bar",
        ["low", "medium", "high"],
        default_index=default_index(
            ["low", "medium", "high"], defaults.get("hiring_bar"), 2
        ),
    )
    quality_bar = prompt_choice(
        "Quality bar",
        ["low", "medium", "high"],
        default_index=default_index(
            ["low", "medium", "high"], defaults.get("quality_bar"), 2
        ),
    )

    return CultureProfile(
        culture_mode=culture_mode,
        tolerance_for_conflict=tolerance_for_conflict,
        conflict_emphasis=conflict_emphasis,
        tolerance_for_burnout=tolerance_for_burnout,
        governance_level=governance_level,
        innovation_level=innovation_level,
        risk_appetite=risk_appetite,
        hiring_bar=hiring_bar,
        quality_bar=quality_bar,
    )


# ---------- Personality inference ----------

def infer_mbti() -> Tuple[List[Tuple[str, float]], Dict[str, float]]:
    questions = [
        ("I feel energized by leading group discussions.", "EI", "E"),
        ("I prefer to reflect before sharing in meetings.", "EI", "I"),
        ("I focus on tangible facts more than abstract ideas.", "SN", "S"),
        ("I enjoy exploring future possibilities.", "SN", "N"),
        ("I prioritize objective logic over personal values.", "TF", "T"),
        ("I consider the human impact first.", "TF", "F"),
        ("I like plans and schedules.", "JP", "J"),
        ("I stay open to last-minute changes.", "JP", "P"),
        ("I decide quickly once I have enough information.", "JP", "J"),
        ("I recharge best with solo time.", "EI", "I"),
    ]
    scores = {"EI": 0.0, "SN": 0.0, "TF": 0.0, "JP": 0.0}
    for text, axis, letter in questions:
        answer = prompt_likert(text)
        delta = answer - 3
        if letter in ("E", "S", "T", "J"):
            scores[axis] += delta
        else:
            scores[axis] -= delta

    def axis_letter(axis: str, positive_letter: str, negative_letter: str) -> str:
        return positive_letter if scores[axis] >= 0 else negative_letter

    primary = "".join(
        [
            axis_letter("EI", "E", "I"),
            axis_letter("SN", "S", "N"),
            axis_letter("TF", "T", "F"),
            axis_letter("JP", "J", "P"),
        ]
    )

    margins = {
        "EI": abs(scores["EI"]),
        "SN": abs(scores["SN"]),
        "TF": abs(scores["TF"]),
        "JP": abs(scores["JP"]),
    }
    weakest_axis = min(margins, key=margins.get)
    flipped = {
        "EI": {"E": "I", "I": "E"},
        "SN": {"S": "N", "N": "S"},
        "TF": {"T": "F", "F": "T"},
        "JP": {"J": "P", "P": "J"},
    }
    primary_letters = list(primary)
    axis_order = ["EI", "SN", "TF", "JP"]
    index = axis_order.index(weakest_axis)
    primary_letters[index] = flipped[weakest_axis][primary_letters[index]]
    secondary = "".join(primary_letters)

    total_strength = sum(margins.values()) + 0.0001
    primary_conf = (sum(margins.values()) - margins[weakest_axis]) / total_strength
    secondary_conf = margins[weakest_axis] / total_strength

    result = [(primary, round(primary_conf, 2)), (secondary, round(secondary_conf, 2))]
    return result, scores


def infer_enneagram() -> Tuple[List[Tuple[int, float]], Dict[int, float]]:
    prompts = {
        1: ["I notice flaws and feel driven to correct them.", "I set high standards for myself."] ,
        2: ["I feel valued when I help others succeed.", "I naturally look for ways to support people."] ,
        3: ["Achievement motivates me more than comfort.", "I like clear goals and measurable wins."] ,
        4: ["I often feel different from others.", "I value depth and authenticity above polish."] ,
        5: ["I conserve my energy and observe before acting.", "I feel secure when I understand systems deeply."] ,
        6: ["I look for risks and contingency plans.", "Loyalty and responsibility matter a lot to me."] ,
        7: ["I seek new options when things feel constrained.", "I dislike feeling stuck in routine."] ,
        8: ["I protect my autonomy and push back on control.", "I respect strength and directness."] ,
        9: ["I prefer harmony over confrontation.", "I adapt to keep the peace in a group."] ,
    }

    scores: Dict[int, float] = {k: 0.0 for k in prompts}
    for t, items in prompts.items():
        for text in items:
            answer = prompt_likert(text)
            scores[t] += answer

    sorted_types = sorted(scores.items(), key=lambda kv: kv[1], reverse=True)
    top3 = sorted_types[:3]
    total_top = sum(score for _, score in top3) + 0.0001
    top3_conf = [(t, round(score / total_top, 2)) for t, score in top3]
    return top3_conf, scores


# ---------- Scoring ----------

def mbti_compatibility(a: str, b: str) -> float:
    score = 0.0
    if a[2] == b[2]:
        score += 0.25
    else:
        score -= 0.1
    if a[3] == b[3]:
        score += 0.2
    else:
        score -= 0.05
    if a[0] != b[0]:
        score += 0.2
    else:
        score += 0.05
    if a[1] != b[1]:
        score += 0.1
    return score


def enneagram_compatibility(a: int, b: int) -> float:
    diff = min((a - b) % 9, (b - a) % 9)
    if diff == 0:
        return 0.1
    if diff == 1:
        return 0.3
    if diff == 2:
        return 0.15
    if diff in (3, 4):
        return -0.1
    return 0.0


def vibe_axis_score(tags: Tuple[str, ...], axis: str) -> int:
    base = 3
    tag_map = {
        "pleasantness": {"pleasant": 5, "supportive": 5, "diplomatic": 4, "reserved": 2, "blunt": 1},
        "directness": {"direct": 5, "blunt": 5, "tactful": 2, "diplomatic": 3},
        "conflict": {"conflict-forward": 5, "assertive": 4, "conflict-averse": 2},
        "decisiveness": {"decisive": 5, "deliberate": 2},
        "structure": {"structured": 5, "process": 4, "flexible": 2, "adaptive": 2},
        "emotional_tone": {"validating": 5, "supportive": 4, "no-nonsense": 2},
        "humor": {"playful": 5, "serious": 2},
        "coaching": {"supportive": 5, "challenging": 2},
    }
    scores = [tag_map.get(axis, {}).get(tag) for tag in tags if tag in tag_map.get(axis, {})]
    if scores:
        return int(round(sum(scores) / len(scores)))
    return base


def ceo_vibe_match_score(candidate: PersonaBundle, vibe: VibeProfile) -> Tuple[bool, float]:
    candidate_axes = {axis: vibe_axis_score(candidate.trait_tags, axis) for axis in AXES}
    pleasant_target = vibe.axes["pleasantness"]
    if pleasant_target >= 4 and candidate_axes["pleasantness"] < 4:
        return False, 0.0
    if pleasant_target <= 2 and candidate_axes["pleasantness"] > 2:
        return False, 0.0

    score = 0.0
    for axis in AXES:
        score -= abs(candidate_axes[axis] - vibe.axes[axis]) * 0.1

    if any(fam in candidate.mbti for fam in ["N", "S"]):
        pass

    if candidate.mbti[1] == "N" and "NF" in vibe.target_mbti_family:
        score += 0.2
    if candidate.mbti[2] == "F" and "NF" in vibe.target_mbti_family:
        score += 0.2
    if candidate.mbti[2] == "T" and "NT" in vibe.target_mbti_family:
        score += 0.2
    if str(candidate.enneagram_core) in vibe.target_enneagram_family:
        score += 0.3

    if vibe.challenge_preference == "mostly calm" and "challenging" in candidate.trait_tags:
        score -= 0.4
    if vibe.challenge_preference == "often challenge" and "challenging" in candidate.trait_tags:
        score += 0.2

    return True, score


def culture_fit_from_tags(tags: Tuple[str, ...]) -> Dict[str, float]:
    vector = {mode: 0.1 for mode in CULTURE_MODES}
    tag_weights = {
        "pleasant": {"friendly_safe": 0.4},
        "supportive": {"friendly_safe": 0.3},
        "diplomatic": {"friendly_safe": 0.3},
        "execution": {"performance_driven": 0.4},
        "operator": {"performance_driven": 0.2, "regulated_enterprise": 0.2},
        "structured": {"regulated_enterprise": 0.4},
        "governance": {"regulated_enterprise": 0.5},
        "risk": {"regulated_enterprise": 0.3},
        "innovator": {"high_velocity_startup": 0.4},
        "creative": {"high_velocity_startup": 0.3},
        "experimental": {"high_velocity_startup": 0.3},
        "intense": {"high_turnover": 0.4, "intentionally_toxic_simulation": 0.3},
        "direct": {"performance_driven": 0.2, "high_turnover": 0.2},
        "adaptive": {"high_velocity_startup": 0.2},
    }

    for tag in tags:
        if tag in tag_weights:
            for mode, weight in tag_weights[tag].items():
                vector[mode] = min(1.0, vector[mode] + weight)
    return vector


def build_persona_library() -> Dict[str, List[PersonaBundle]]:
    def bundle(
        persona_id: str,
        enneagram_core: int,
        wing: str,
        mbti: str,
        western: str,
        chinese: str,
        tags: List[str],
        role_fit_weight: float,
    ) -> PersonaBundle:
        return PersonaBundle(
            persona_id=persona_id,
            enneagram_core=enneagram_core,
            wing=wing,
            mbti=mbti,
            western_zodiac=western,
            chinese_zodiac=chinese,
            trait_tags=tuple(tags),
            role_fit_weight=role_fit_weight,
            culture_fit_vector=culture_fit_from_tags(tuple(tags)),
        )

    return {
        "CEO": [
            bundle(
                "CEO-Diplomat",
                9,
                "9w8",
                "ENFJ",
                "Libra",
                "Wood Goat",
                ["pleasant", "diplomatic", "supportive", "structured", "integrator"],
                0.85,
            ),
            bundle(
                "CEO-Strategist",
                8,
                "8w7",
                "ENTJ",
                "Aries",
                "Fire Tiger",
                ["direct", "conflict-forward", "decisive", "execution", "operator"],
                0.9,
            ),
            bundle(
                "CEO-Architect",
                1,
                "1w9",
                "INTJ",
                "Capricorn",
                "Metal Ox",
                ["structured", "deliberate", "no-nonsense", "governance", "operator"],
                0.82,
            ),
        ],
        "CFO": [
            bundle(
                "CFO-Analyst",
                5,
                "5w6",
                "INTJ",
                "Virgo",
                "Metal Rooster",
                ["analytical", "governance", "structured", "risk"],
                0.88,
            ),
            bundle(
                "CFO-Guardian",
                1,
                "1w2",
                "ISTJ",
                "Taurus",
                "Earth Ox",
                ["structured", "governance", "process", "operator"],
                0.86,
            ),
            bundle(
                "CFO-Optimizer",
                3,
                "3w4",
                "ENTJ",
                "Scorpio",
                "Water Dragon",
                ["execution", "direct", "performance", "operator"],
                0.84,
            ),
        ],
        "COO": [
            bundle(
                "COO-Executor",
                3,
                "3w2",
                "ESTJ",
                "Leo",
                "Fire Horse",
                ["execution", "structured", "operator", "direct"],
                0.9,
            ),
            bundle(
                "COO-Stabilizer",
                6,
                "6w5",
                "ISTJ",
                "Cancer",
                "Earth Dog",
                ["process", "risk", "structured", "operator"],
                0.86,
            ),
            bundle(
                "COO-Integrator",
                2,
                "2w3",
                "ESFJ",
                "Libra",
                "Wood Rabbit",
                ["supportive", "integrator", "people", "structured"],
                0.82,
            ),
        ],
        "CTO": [
            bundle(
                "CTO-Systems",
                5,
                "5w6",
                "INTP",
                "Aquarius",
                "Metal Rat",
                ["analytical", "innovator", "adaptive", "experimental"],
                0.9,
            ),
            bundle(
                "CTO-Builder",
                8,
                "8w7",
                "ENTJ",
                "Aries",
                "Fire Monkey",
                ["decisive", "execution", "direct", "operator"],
                0.85,
            ),
            bundle(
                "CTO-Explorer",
                7,
                "7w6",
                "ENTP",
                "Sagittarius",
                "Water Horse",
                ["innovator", "creative", "adaptive", "experimental"],
                0.86,
            ),
        ],
        "CPO": [
            bundle(
                "CPO-Caregiver",
                2,
                "2w1",
                "ENFJ",
                "Pisces",
                "Water Pig",
                ["supportive", "people", "integrator", "pleasant"],
                0.86,
            ),
            bundle(
                "CPO-Coach",
                6,
                "6w7",
                "ESFJ",
                "Cancer",
                "Earth Sheep",
                ["structured", "supportive", "process", "people"],
                0.82,
            ),
            bundle(
                "CPO-Culture",
                4,
                "4w3",
                "INFJ",
                "Libra",
                "Fire Rabbit",
                ["creative", "people", "diplomatic", "integrator"],
                0.8,
            ),
        ],
        "CMO": [
            bundle(
                "CMO-Creative",
                7,
                "7w6",
                "ENFP",
                "Gemini",
                "Wood Dragon",
                ["creative", "innovator", "people", "pleasant"],
                0.86,
            ),
            bundle(
                "CMO-Growth",
                3,
                "3w4",
                "ENTJ",
                "Scorpio",
                "Fire Rat",
                ["execution", "direct", "performance", "operator"],
                0.84,
            ),
            bundle(
                "CMO-Brand",
                4,
                "4w3",
                "INFP",
                "Pisces",
                "Water Rabbit",
                ["creative", "diplomatic", "people", "pleasant"],
                0.82,
            ),
        ],
        "CIO": [
            bundle(
                "CIO-Governor",
                1,
                "1w9",
                "INTJ",
                "Capricorn",
                "Metal Snake",
                ["governance", "structured", "risk", "operator"],
                0.86,
            ),
            bundle(
                "CIO-Guardian",
                6,
                "6w5",
                "ISTP",
                "Virgo",
                "Earth Ox",
                ["risk", "process", "analytical", "governance"],
                0.82,
            ),
            bundle(
                "CIO-Architect",
                5,
                "5w6",
                "ISTJ",
                "Taurus",
                "Water Monkey",
                ["analytical", "structured", "governance"],
                0.84,
            ),
        ],
        "CLO": [
            bundle(
                "CLO-Compliance",
                1,
                "1w2",
                "ISFJ",
                "Virgo",
                "Earth Rooster",
                ["governance", "structured", "risk", "diplomatic"],
                0.86,
            ),
            bundle(
                "CLO-Guardian",
                6,
                "6w5",
                "ISTJ",
                "Capricorn",
                "Metal Ox",
                ["risk", "process", "structured", "governance"],
                0.84,
            ),
            bundle(
                "CLO-Advisor",
                3,
                "3w2",
                "ESTJ",
                "Aries",
                "Fire Dog",
                ["direct", "execution", "structured", "operator"],
                0.8,
            ),
        ],
        "CXA": [
            bundle(
                "CXA-Anchor",
                9,
                "9w1",
                "ISFJ",
                "Libra",
                "Earth Goat",
                ["pleasant", "integrator", "supportive", "structured"],
                0.8,
            ),
            bundle(
                "CXA-Partner",
                2,
                "2w1",
                "ESFJ",
                "Cancer",
                "Water Ox",
                ["supportive", "people", "integrator"],
                0.78,
            ),
            bundle(
                "CXA-Organizer",
                6,
                "6w5",
                "ISTJ",
                "Virgo",
                "Metal Dog",
                ["process", "structured", "operator"],
                0.76,
            ),
        ],
        "Chairman": [
            bundle(
                "Chairman-Strategic",
                8,
                "8w9",
                "ENTJ",
                "Aries",
                "Fire Dragon",
                ["direct", "decisive", "vision", "operator"],
                0.9,
            ),
            bundle(
                "Chairman-Steward",
                1,
                "1w2",
                "ENFJ",
                "Libra",
                "Wood Tiger",
                ["pleasant", "governance", "diplomatic", "integrator"],
                0.88,
            ),
        ],
    }


def diversity_penalty(assignments: Dict[str, PersonaBundle]) -> float:
    mbti_counts: Dict[str, int] = {}
    enneagram_counts: Dict[int, int] = {}
    for bundle in assignments.values():
        mbti_counts[bundle.mbti] = mbti_counts.get(bundle.mbti, 0) + 1
        enneagram_counts[bundle.enneagram_core] = enneagram_counts.get(bundle.enneagram_core, 0) + 1

    penalty = 0.0
    for count in mbti_counts.values():
        if count > 1:
            penalty += (count - 1) * 0.2
    for count in enneagram_counts.values():
        if count > 1:
            penalty += (count - 1) * 0.2
    return penalty


def coverage_bonus(assignments: Dict[str, PersonaBundle]) -> float:
    tags = set()
    for bundle in assignments.values():
        tags.update(bundle.trait_tags)

    bonus = 0.0
    if tags.intersection(INTEGRATOR_TAGS):
        bonus += 0.2
    else:
        bonus -= 0.4
    if tags.intersection(OPERATOR_TAGS):
        bonus += 0.2
    else:
        bonus -= 0.4
    if tags.intersection(GOVERNANCE_TAGS):
        bonus += 0.2
    else:
        bonus -= 0.4
    if tags.intersection(INNOVATOR_TAGS):
        bonus += 0.2
    else:
        bonus -= 0.4
    return bonus


def construct_conflict_adjustment(
    assignments: Dict[str, PersonaBundle], culture: CultureProfile
) -> float:
    tolerance = culture.tolerance_for_conflict
    emphasis = culture.conflict_emphasis
    burnout = culture.tolerance_for_burnout
    adjust = 0.0
    bonus_multiplier = {"low": 0.5, "medium": 1.0, "high": 1.4}[emphasis]
    penalty_multiplier = {"low": 1.4, "medium": 1.0, "high": 0.7}[emphasis]

    bundles = list(assignments.values())
    for i in range(len(bundles)):
        for j in range(i + 1, len(bundles)):
            a = bundles[i]
            b = bundles[j]
            conflict_forward = "conflict-forward" in a.trait_tags or "conflict-forward" in b.trait_tags
            direct = "direct" in a.trait_tags or "direct" in b.trait_tags
            if tolerance == "high":
                if direct:
                    adjust += 0.05 * bonus_multiplier
            if tolerance == "low" and conflict_forward:
                adjust -= 0.2 * penalty_multiplier
            if burnout == "low" and ("intense" in a.trait_tags or "intense" in b.trait_tags):
                adjust -= 0.15 * penalty_multiplier
    return adjust


def ceo_originality_bonus(compatibility: float, preference: str) -> float:
    targets = {"subtle": 0.45, "balanced": 0.35, "bold": 0.25}
    widths = {"subtle": 0.15, "balanced": 0.2, "bold": 0.25}
    target = targets.get(preference, 0.35)
    width = widths.get(preference, 0.2)
    delta = abs(compatibility - target)
    if delta >= width:
        bonus = -0.05
    else:
        bonus = ((width - delta) / width) * 0.25
    if compatibility < 0.1:
        bonus -= 0.15
    return bonus


def human_ceo_compatibility(human: HumanProfile, candidate: PersonaBundle) -> float:
    mbti_target = human.top_mbti[0][0]
    enneagram_target = human.top_enneagram[0][0]
    score = mbti_compatibility(mbti_target, candidate.mbti)
    score += enneagram_compatibility(enneagram_target, candidate.enneagram_core)
    return score


def score_assignment(
    assignments: Dict[str, PersonaBundle],
    culture: CultureProfile,
    human: HumanProfile,
    vibe: VibeProfile,
    human_position: str,
    ceo_originality: str,
) -> Tuple[float, Dict[str, Dict[str, float]]]:
    breakdown: Dict[str, Dict[str, float]] = {}
    total = 0.0
    for role, bundle in assignments.items():
        role_breakdown = {}
        role_breakdown["role_fit_weight"] = bundle.role_fit_weight
        role_breakdown["culture_fit"] = bundle.culture_fit_vector.get(culture.culture_mode, 0.0)
        total += role_breakdown["role_fit_weight"] + role_breakdown["culture_fit"]

        if role == "CEO":
            match_ok, vibe_score = ceo_vibe_match_score(bundle, vibe)
            role_breakdown["vibe_match_score"] = vibe_score
            total += vibe_score
            if match_ok:
                role_breakdown["vibe_ok"] = 1.0
            else:
                role_breakdown["vibe_ok"] = -2.0
                total -= 2.0
            compatibility = human_ceo_compatibility(human, bundle)
            ceo_bonus = compatibility * 2.5
            role_breakdown["human_ceo_bonus"] = ceo_bonus
            total += ceo_bonus
            originality_bonus = ceo_originality_bonus(compatibility, ceo_originality)
            role_breakdown["ceo_originality_bonus"] = originality_bonus
            total += originality_bonus
            if human_position == "Chairman":
                chairman_bonus = compatibility * 1.5
                role_breakdown["chairman_ceo_bonus"] = chairman_bonus
                total += chairman_bonus

        breakdown[role] = role_breakdown

    roles_list = list(assignments.values())
    for i in range(len(roles_list)):
        for j in range(i + 1, len(roles_list)):
            pair_score = mbti_compatibility(roles_list[i].mbti, roles_list[j].mbti)
            pair_score += enneagram_compatibility(
                roles_list[i].enneagram_core, roles_list[j].enneagram_core
            )
            total += pair_score * 0.4

    total -= diversity_penalty(assignments)
    total += coverage_bonus(assignments)
    total += construct_conflict_adjustment(assignments, culture)

    return total, breakdown


def select_team(
    roles: List[str],
    library: Dict[str, List[PersonaBundle]],
    culture: CultureProfile,
    human: HumanProfile,
    vibe: VibeProfile,
    human_position: str,
    selection: Optional[SelectionConfig] = None,
    beam_width: int = 8,
) -> Assignment:
    if selection is None:
        selection = SelectionConfig(
            randomness_level="low",
            ceo_originality="balanced",
            rng=random.Random(0),
            seed_label="default",
        )
    jitter, temperature, pool_size = selection_tuning(selection.randomness_level)
    rng = selection.rng
    beam: List[Assignment] = [
        Assignment(roles={}, score=0.0, breakdown={}, notes={}, image_prompts={}, backstories={})
    ]

    for role in roles:
        candidates = library.get(role, [])
        new_beam: List[Assignment] = []
        for assignment in beam:
            for candidate in candidates:
                if role == "CEO":
                    match_ok, _ = ceo_vibe_match_score(candidate, vibe)
                    if not match_ok:
                        continue

                next_roles = dict(assignment.roles)
                next_roles[role] = candidate
                total_score, breakdown = score_assignment(
                    next_roles, culture, human, vibe, human_position, selection.ceo_originality
                )
                note = build_why_note(
                    role,
                    candidate,
                    culture,
                    vibe,
                    human,
                    human_position,
                    selection.ceo_originality,
                )
                notes = dict(assignment.notes)
                notes[role] = note
                new_beam.append(
                    Assignment(
                        roles=next_roles,
                        score=total_score,
                        breakdown=breakdown,
                        notes=notes,
                        image_prompts=assignment.image_prompts,
                        backstories=assignment.backstories,
                    )
                )
        if jitter > 0:
            new_beam.sort(
                key=lambda a: (
                    a.score + rng.uniform(-jitter, jitter),
                    a.roles.get(role).persona_id,
                ),
                reverse=True,
            )
        else:
            new_beam.sort(
                key=lambda a: (a.score, a.roles.get(role).persona_id), reverse=True
            )
        beam = new_beam[:beam_width]

    if pool_size <= 1 or len(beam) <= 1:
        return beam[0]
    pool = beam[: min(pool_size, len(beam))]
    return softmax_sample(pool, rng, temperature)


def build_why_note(
    role: str,
    candidate: PersonaBundle,
    culture: CultureProfile,
    vibe: VibeProfile,
    human: HumanProfile,
    human_position: str,
    ceo_originality: str,
) -> str:
    parts = []
    parts.append(f"role fit {candidate.role_fit_weight:.2f}")
    parts.append(
        f"culture {candidate.culture_fit_vector.get(culture.culture_mode, 0.0):.2f}"
    )
    if role == "CEO":
        _, vibe_score = ceo_vibe_match_score(candidate, vibe)
        parts.append(f"vibe score {vibe_score:.2f}")
        compatibility = human_ceo_compatibility(human, candidate)
        parts.append(f"human match {compatibility:.2f}")
        parts.append(f"originality {ceo_originality}")
        if human_position == "Chairman":
            parts.append("chairman priority")
    if "integrator" in candidate.trait_tags:
        parts.append("integrator buffer")
    if "governance" in candidate.trait_tags:
        parts.append("governance anchor")
    if "innovator" in candidate.trait_tags:
        parts.append("innovation lift")
    return "; ".join(parts)


def prompt_manual_persona(role: str, defaults: Optional[PersonaBundle] = None) -> Tuple[PersonaBundle, str]:
    default_core = defaults.enneagram_core if defaults else None
    default_wing = defaults.wing if defaults else ""
    default_mbti = defaults.mbti if defaults else None
    default_west = defaults.western_zodiac if defaults else None
    default_chinese = defaults.chinese_zodiac if defaults else ""

    enneagram_core = prompt_int(f"{role} enneagram core (1-9)", 1, 9, default=default_core)
    wing = prompt_text(f"{role} wing (e.g., 9w8)", default=default_wing)
    mbti = prompt_mbti(f"{role} MBTI", default=default_mbti)
    west = prompt_western_zodiac(f"{role} western zodiac", default=default_west)
    chinese = prompt_text(f"{role} Chinese zodiac (element animal)", default=default_chinese)
    notes = prompt_text(f"{role} notes", default="manual entry")

    bundle = PersonaBundle(
        persona_id=f"Manual-{role}",
        enneagram_core=enneagram_core,
        wing=wing,
        mbti=mbti,
        western_zodiac=west,
        chinese_zodiac=chinese,
        trait_tags=(),
        role_fit_weight=0.0,
        culture_fit_vector={mode: 0.1 for mode in CULTURE_MODES},
    )
    return bundle, notes


def build_manual_assignment(
    roles: List[str],
    base_assignment: Optional[Assignment] = None,
) -> Assignment:
    roles_map: Dict[str, PersonaBundle] = {}
    notes: Dict[str, str] = {}
    for role in roles:
        defaults = base_assignment.roles.get(role) if base_assignment else None
        bundle, note = prompt_manual_persona(role, defaults=defaults)
        roles_map[role] = bundle
        notes[role] = note

    return Assignment(
        roles=roles_map,
        score=0.0,
        breakdown={},
        notes=notes,
        image_prompts={},
        image_prompts={},
        backstories={},
        image_paths={},
    )


def build_default_image_prompt(role: str, bundle: Optional[PersonaBundle]) -> str:
    tags = set(bundle.trait_tags) if bundle else set()
    style = "photorealistic"
    attire = "business professional"
    setting = "modern office"
    mood = "focused, confident"
    palette = "neutral"
    if "innovator" in tags or "creative" in tags:
        setting = "modern studio workspace"
        palette = "bold"
    if "governance" in tags or "risk" in tags:
        palette = "conservative"
    if "pleasant" in tags or "supportive" in tags:
        mood = "warm, approachable"
    return f"{role} executive, senior professional, {attire}, {setting}, {mood}, {palette} palette, {style}"


def collect_image_prompts(roles: List[str], assignment: Assignment) -> Dict[str, str]:
    prompts: Dict[str, str] = {}
    print("\nImage prompt setup (no images generated here)")
    print(
        "Please avoid protected demographics (race, ethnicity, religion, sexual orientation, etc.). "
        "You can specify career stage, style, attire, setting, and tone."
    )
    for role in roles:
        if role == "Chairman":
            continue
        bundle = assignment.roles.get(role)
        print(f"\n{role} image prompt")
        career_stage = prompt_choice(
            "Career stage impression",
            ["early-career", "mid-career", "senior"],
            default_index=3,
        )
        style = prompt_choice(
            "Visual style",
            ["photorealistic", "illustration", "3d render", "line art"],
            default_index=1,
        )
        attire = prompt_text("Attire", default="business professional")
        setting = prompt_text("Setting", default="modern office")
        mood = prompt_text("Mood/tone", default="focused, confident")
        palette = prompt_text("Color palette", default="neutral")
        regional = prompt_text("Regional aesthetic (optional)", default="")
        extras = prompt_text("Optional details (props, lighting)", default="")
        default_prompt = build_default_image_prompt(role, bundle)

        base_parts = [
            f"{role} executive",
            f"{career_stage} professional",
            attire,
            setting,
            mood,
            f"{palette} palette",
            style,
        ]
        if regional:
            base_parts.append(regional)
        if extras:
            base_parts.append(extras)

        composed = ", ".join(part for part in base_parts if part)
        final_prompt = prompt_text("Image prompt (editable)", default=composed or default_prompt)
        prompts[role] = final_prompt

    return prompts


def generate_placeholder_image(role: str, output_path: str) -> None:
    # Create a simple colored placeholder with text
    size = (400, 400)
    colors = {
        "CEO": "#3b82f6", "CFO": "#10b981", "CMO": "#ec4899",
        "COO": "#f97316", "CIO": "#06b6d4", "CLO": "#f59e0b",
        "CPO": "#8b5cf6", "CTO": "#3b82f6", "CXA": "#f97316",
        "Chairman": "#fbbf24"
    }
    color = colors.get(role, "#6b7280")
    
    img = Image.new('RGB', size, color=color)
    draw = ImageDraw.Draw(img)
    
    # Try to load a font, fallback to default
    try:
        font = ImageFont.truetype("Arial.ttf", 60)
    except IOError:
        font = ImageFont.load_default()
        
    text = role
    bbox = draw.textbbox((0, 0), text, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    
    x = (size[0] - text_w) / 2
    y = (size[1] - text_h) / 2
    
    draw.text((x, y), text, fill="white", font=font)
    img.save(output_path)
    print(f"Generated placeholder for {role} at {output_path}")


def collect_image_paths(roles: List[str]) -> Dict[str, str]:
    paths: Dict[str, str] = {}
    print("\nStep 7b: Image Selection")
    print("For each role, you can use a generated placeholder or provide a path to your own image.")
    
    images_dir = "images_out"
    if not os.path.exists(images_dir):
        os.makedirs(images_dir)
        
    for role in roles:
        print(f"\n[{role}]")
        choice = prompt_choice(
            f"Image for {role}",
            ["Generate Placeholder", "Provide Custom Path"],
            default_index=1
        )
        
        if choice == "Generate Placeholder":
            filename = f"{role.lower()}.png"
            out_path = os.path.join(images_dir, filename)
            generate_placeholder_image(role, out_path)
            paths[role] = os.path.abspath(out_path)
        else:
            while True:
                custom_path = prompt_text("Enter absolute path to image file")
                # Remove quotes if user dragged file
                custom_path = custom_path.strip("'\"")
                if os.path.exists(custom_path):
                    paths[role] = os.path.abspath(custom_path)
                    break
                print("File not found. Please try again.")
                
    return paths


def culture_summary(culture: CultureProfile) -> str:
    return (
        f"mode={culture.culture_mode}; conflict_tolerance={culture.tolerance_for_conflict}; "
        f"conflict_emphasis={culture.conflict_emphasis}; burnout_tolerance={culture.tolerance_for_burnout}; "
        f"governance={culture.governance_level}; innovation={culture.innovation_level}; "
        f"risk_appetite={culture.risk_appetite}; hiring_bar={culture.hiring_bar}; quality_bar={culture.quality_bar}"
    )


def openrouter_request(
    api_key: str,
    model: str,
    messages: List[Dict[str, str]],
    temperature: float,
    max_tokens: int,
    timeout: int,
) -> str:
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    referer = os.getenv("OPENROUTER_REFERER")
    title = os.getenv("OPENROUTER_TITLE")
    if referer:
        headers["HTTP-Referer"] = referer
    if title:
        headers["X-Title"] = title
    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }
    request = urllib.request.Request(
        url, data=json.dumps(payload).encode("utf-8"), headers=headers
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        data = json.loads(response.read().decode("utf-8"))
    if "choices" not in data or not data["choices"]:
        raise ValueError(f"Unexpected OpenRouter response: {data}")
    return data["choices"][0]["message"]["content"].strip()


def load_env_file(path: str) -> None:
    if not os.path.exists(path):
        return
    with open(path, "r") as handle:
        for raw in handle:
            line = raw.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip().strip("'").strip('"')
            if key and key not in os.environ:
                os.environ[key] = value


def build_backstory_messages(
    role: str,
    bundle: PersonaBundle,
    culture: CultureProfile,
    vibe: VibeProfile,
    selection: SelectionConfig,
) -> List[Dict[str, str]]:
    system = (
        "You generate short, abstract executive backstories for a factory template (not a factory). "
        "Stay generic: no company names, no industries, no locations, and no real people. "
        "Avoid protected demographics. Keep compatibility with the CEO but preserve originality. "
        "Output a single paragraph, 3 sentences, 60-90 words."
    )
    user = (
        f"Role: {role}\n"
        f"Persona ID: {bundle.persona_id}\n"
        f"MBTI: {bundle.mbti}\n"
        f"Enneagram: {bundle.enneagram_core} ({bundle.wing})\n"
        f"Tags: {', '.join(bundle.trait_tags) if bundle.trait_tags else 'none'}\n"
        f"Culture: {culture_summary(culture)}\n"
        f"CEO vibe tags: {', '.join(vibe.tags)}\n"
        f"Originality bias: {selection.ceo_originality}\n"
        f"Seed label: {selection.seed_label}"
    )
    return [{"role": "system", "content": system}, {"role": "user", "content": user}]


def collect_backstories(
    roles: List[str],
    assignment: Assignment,
    culture: CultureProfile,
    vibe: VibeProfile,
    selection: SelectionConfig,
) -> Dict[str, str]:
    env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".env"))
    load_env_file(env_path)
    api_key = os.getenv("OPENROUTER_API_KEY", "").strip()
    default_model = os.getenv("OPENROUTER_MODEL", "mistralai/mistral-7b-instruct")
    print("\nStep 8: Backstory generation (OpenRouter required)")
    if not api_key:
        raise RuntimeError(
            "OPENROUTER_API_KEY is not set. Backstory generation requires OpenRouter."
        )
    backstories: Dict[str, str] = {}
    model = prompt_text("OpenRouter model", default=default_model)

    for role in roles:
        bundle = assignment.roles.get(role)
        if bundle is None:
            continue
        messages = build_backstory_messages(role, bundle, culture, vibe, selection)
        backstory = openrouter_request(
            api_key=api_key,
            model=model,
            messages=messages,
            temperature=0.6,
            max_tokens=180,
            timeout=20,
        )
        backstories[role] = backstory
    return backstories


# ---------- Reporting ----------

def print_role_table(assignment: Assignment) -> None:
    headers = ["Role", "Enneagram", "MBTI", "Western", "Chinese", "Persona"]
    rows = []
    for role, bundle in assignment.roles.items():
        rows.append(
            [
                role,
                f"{bundle.enneagram_core} ({bundle.wing})",
                bundle.mbti,
                bundle.western_zodiac,
                bundle.chinese_zodiac,
                bundle.persona_id,
            ]
        )

    col_widths = [
        max(len(str(row[i])) for row in [headers] + rows) for i in range(len(headers))
    ]
    header_line = " | ".join(h.ljust(col_widths[i]) for i, h in enumerate(headers))
    divider = "-+-".join("-" * width for width in col_widths)
    print(header_line)
    print(divider)
    for row in rows:
        print(" | ".join(str(row[i]).ljust(col_widths[i]) for i in range(len(headers))))


def write_csv(path: str, assignment: Assignment) -> None:
    with open(path, "w", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(
            [
                "Role",
                "Enneagram",
                "Wing",
                "MBTI",
                "Western Zodiac",
                "Chinese Zodiac",
                "Notes",
                "ImagePrompt",
                "Backstory",
                "ImagePath",
            ]
        )
        for role, bundle in assignment.roles.items():
            writer.writerow(
                [
                    role,
                    bundle.enneagram_core,
                    bundle.wing,
                    bundle.mbti,
                    bundle.western_zodiac,
                    bundle.chinese_zodiac,
                    assignment.notes.get(role, ""),
                    assignment.image_prompts.get(role, ""),
                    assignment.backstories.get(role, ""),
                    assignment.image_paths.get(role, ""),
                ]
            )


def print_human_profile(human: HumanProfile) -> None:
    enneagram_summary = ", ".join(
        [f"{t} ({int(conf * 100)}%)" for t, conf in human.top_enneagram]
    )
    mbti_summary = ", ".join(
        [f"{mbti} ({int(conf * 100)}%)" for mbti, conf in human.top_mbti]
    )
    print("Human profile summary")
    print(f"Enneagram top 3: {enneagram_summary}")
    print(f"MBTI top 2: {mbti_summary}")
    print(f"Western zodiac: {human.western_zodiac}")
    print(f"Chinese zodiac: {human.chinese_zodiac}")


def print_debug_json(assignment: Assignment) -> None:
    print("\nDebug scoring breakdown")
    print(json.dumps(assignment.breakdown, indent=2))


# ---------- Onboarding flow ----------

def prompt_selection_config() -> SelectionConfig:
    print("Step 0: Template variation (abstract options only)")
    randomness_level = prompt_choice(
        "How much randomness should the template allow?",
        RANDOMNESS_LEVELS,
        default_index=2,
    )
    ceo_originality = prompt_choice(
        "CEO originality bias (compatible but original)",
        CEO_ORIGINALITY_LEVELS,
        default_index=2,
    )
    seed_phrase = prompt_text(
        "Seed phrase (optional; leave blank for a fresh mix each run)",
        default="",
    )
    rng, seed_label = build_rng(seed_phrase)
    print(f"Variation seed: {seed_label}")
    return SelectionConfig(
        randomness_level=randomness_level,
        ceo_originality=ceo_originality,
        rng=rng,
        seed_label=seed_label,
    )


def prompt_culture_card(rng: random.Random) -> Optional[CultureCard]:
    print("\nCulture deck: pick a card, reroll, or go custom (abstract signals only).")
    while True:
        deck = rng.sample(CULTURE_CARDS, k=min(3, len(CULTURE_CARDS)))
        options = [f"{card.name} — {card.description}" for card in deck]
        options.extend(["Reroll deck", "Custom inputs"])
        choice = prompt_choice("Choose a culture card", options, default_index=1)
        if choice == "Reroll deck":
            continue
        if choice == "Custom inputs":
            return None
        idx = options.index(choice)
        if idx < len(deck):
            return deck[idx]


def ask_ceo_vibe_questions() -> VibeProfile:
    axes = {
        "pleasantness": prompt_likert("CEO warmth vs cold directness"),
        "directness": prompt_likert("CEO bluntness vs tact"),
        "conflict": prompt_likert("CEO avoids conflict vs embraces conflict"),
        "decisiveness": prompt_likert("CEO decision speed (fast vs deliberate)"),
        "structure": prompt_likert("CEO process orientation vs flexibility"),
        "emotional_tone": prompt_likert("CEO validating tone vs no-nonsense"),
        "humor": prompt_likert("CEO humor (none vs frequent)"),
        "coaching": prompt_likert("CEO coaching (supportive vs challenging)"),
    }
    challenge_preference = prompt_choice(
        "Do you want the CEO to challenge you sometimes, or mostly keep things calm?",
        ["mostly calm", "balanced", "often challenge"],
        default_index=2,
    )
    vibe = synthesize_vibe_profile(axes, challenge_preference)
    print("\nCEO vibe profile")
    print(f"Tags: {', '.join(vibe.tags)}")
    print(f"Target MBTI family: {', '.join(vibe.target_mbti_family)}")
    print(f"Target Enneagram family: {', '.join(vibe.target_enneagram_family)}")
    return vibe


def ask_birthdate() -> Tuple[date, str]:
    while True:
        value = prompt_text("Birthdate for zodiac (YYYY-MM-DD)")
        try:
            birth = datetime.strptime(value, "%Y-%m-%d").date()
            return birth, ""
        except ValueError:
            print("Please enter a valid date in YYYY-MM-DD format.")


def main() -> None:
    print("Executive AI Agent Personality Onboarding")
    selection = prompt_selection_config()
    print("\nStep 1: Identify your position")
    human_position = prompt_choice(
        "Are you the Chairman, CEO, or other?",
        ["Chairman", "CEO", "Other"],
        default_index=1,
    )

    print("\nStep 2: CEO vibe questions (primary driver)")
    vibe = ask_ceo_vibe_questions()

    print("\nStep 3: Company culture and org style")
    card = prompt_culture_card(selection.rng)
    if card:
        print(f"Selected culture card: {card.name} — {card.description}")
        culture = culture_profile_from_inputs(defaults=card.defaults)
    else:
        culture = culture_profile_from_inputs()
    if culture.culture_mode == "intentionally_toxic_simulation":
        print(
            "Note: This mode is treated as a roleplay intensity setting only. "
            "No real-world harmful practices are recommended."
        )

    print("\nStep 4: Birthdate for zodiac (flavor only)")
    birth_date, _ = ask_birthdate()

    print("\nStep 5: Human personality inference")
    top_mbti, raw_mbti_scores = infer_mbti()
    top_enneagram, raw_enneagram_scores = infer_enneagram()

    west = western_zodiac(birth_date.month, birth_date.day)
    cny = chinese_new_year_date(birth_date.year)
    boundary_answer = None
    if cny is None:
        boundary_answer = prompt_choice(
            "Were you born before Chinese New Year that year?",
            ["yes", "no", "unsure"],
            default_index=3,
        )
    if boundary_answer == "unsure":
        boundary_answer = None
    chinese = chinese_zodiac_for_date(birth_date, boundary_answer)

    human_profile = HumanProfile(
        top_enneagram=top_enneagram,
        top_mbti=top_mbti,
        western_zodiac=west,
        chinese_zodiac=chinese,
        raw_mbti_scores=raw_mbti_scores,
        raw_enneagram_scores=raw_enneagram_scores,
    )

    roles = list(ROLE_ORDER_DEFAULT)
    if human_position != "Chairman":
        roles.append("Chairman")

    library = build_persona_library()
    assignment = select_team(
        roles, library, culture, human_profile, vibe, human_position, selection=selection
    )

    print("\nHuman profile summary")
    print_human_profile(human_profile)

    print("\nRecommended role assignment table")
    print_role_table(assignment)

    print("\nWhy notes per role")
    for role, note in assignment.notes.items():
        print(f"{role}: {note}")

    print_debug_json(assignment)

    print("\nStep 6: Choose how to create the CSV")
    creation_mode = prompt_choice(
        "Select a CSV creation mode",
        ["use recommended", "edit recommended", "manual from scratch"],
        default_index=1,
    )

    if creation_mode == "edit recommended":
        print("\nEdit mode: press Enter to keep any suggested value.")
        assignment = build_manual_assignment(roles, base_assignment=assignment)
    elif creation_mode == "manual from scratch":
        print("\nManual mode: fill in each role to build your own CSV.")
        assignment = build_manual_assignment(roles)

    print("\nFinal role assignment table")
    print_role_table(assignment)

    if creation_mode == "manual from scratch":
        print("\nNotes: Manual entries skip scoring and debug output.")

    print("\nStep 7: Image prompts for each role (no images generated)")
    print("\nStep 7a: Image prompts for each role")
    assignment.image_prompts = collect_image_prompts(roles, assignment)
    
    assignment.image_paths = collect_image_paths(roles)

    assignment.backstories = collect_backstories(
        roles, assignment, culture, vibe, selection
    )

    print("\nStep 9: Create the CSV artifact")
    csv_path = prompt_text("CSV output path", default="agent_personality_chart.csv")
    while True:
        confirm = prompt_choice(
            "Create the CSV now?",
            ["yes", "no"],
            default_index=1,
        )
        if confirm == "yes":
            break
        print("CSV creation is required to finish the onboarding.")
    write_csv(csv_path, assignment)
    print(f"\nCSV written to {csv_path}")
    
    # Dashboard Integration
    print("\nStep 10: Dashboard Integration")
    sync_choice = prompt_choice(
        "Sync these agents and images to the Dashboard now?",
        ["yes", "no"],
        default_index=1
    )
    
    if sync_choice == "yes":
        import subprocess
        script_path = os.path.join("scripts", "sync_dashboard.py")
        if not os.path.exists(script_path):
            # Fallback for relative path from Onboarding dir
            script_path = os.path.join("..", "scripts", "sync_dashboard.py")
            
        if os.path.exists(script_path):
            print(f"Running sync script on {csv_path}...")
            try:
                subprocess.run(["python3", script_path, csv_path], check=True)
                print("Dashboard sync complete!")
            except subprocess.CalledProcessError as e:
                print(f"Sync failed: {e}")
            except Exception as e:
                print(f"Error running sync: {e}")
        else:
            print(f"Sync script not found at {script_path}")


if __name__ == "__main__":
    main()
