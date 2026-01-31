from datetime import date

import app


def test_western_zodiac_aries_boundary():
    assert app.western_zodiac(3, 21) == "Aries"
    assert app.western_zodiac(4, 19) == "Aries"


def test_chinese_zodiac_boundary_case():
    # Chinese New Year 2024 is Feb 10, 2024
    before = date(2024, 2, 9)
    after = date(2024, 2, 10)
    assert app.chinese_zodiac_for_date(before) == "Water Rabbit"
    assert app.chinese_zodiac_for_date(after) == "Wood Dragon"


def test_ceo_pleasantness_constraint_enforced():
    library = app.build_persona_library()
    ceo_candidates = library["CEO"]
    axes = {axis: 4 for axis in app.AXES}
    vibe = app.synthesize_vibe_profile(axes, "mostly calm")
    ok_candidates = [c for c in ceo_candidates if app.ceo_vibe_match_score(c, vibe)[0]]
    assert ok_candidates, "Expected at least one CEO candidate to pass pleasantness constraint"
    for candidate in ceo_candidates:
        candidate_axis = app.vibe_axis_score(candidate.trait_tags, "pleasantness")
        if candidate_axis < 4:
            assert not app.ceo_vibe_match_score(candidate, vibe)[0]
