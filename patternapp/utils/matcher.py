import re
from patternapp.models import PatternLayoutMapping


def tokenize_pattern(pattern):
    if not pattern:
        return set()

    pattern = pattern.lower()

    # remove regex placeholders
    pattern = re.sub(r"\[0-9\]\+", " ", pattern)
    pattern = re.sub(r"\[0-9\]\{\d+\}", " ", pattern)

    # MERITAIN style
    if "verscend" in pattern or "standard" in pattern:
        pattern = re.sub(r"\d+", " ", pattern)
    else:
        # UHC style: keep smaller useful numbers, remove large policy-like groups
        pattern = re.sub(r"\b\d{5,}\b", " ", pattern)

    pattern = re.sub(r"[^a-z0-9]+", " ", pattern)
    return set(pattern.split())


def tokenize_cuttingfloor(cuttingfloor):
    if not cuttingfloor:
        return set()

    cf = cuttingfloor.lower()

    # normalize common separators
    cf = cf.replace("|", " ")
    cf = cf.replace(":", " ")
    cf = cf.replace("-", "")
    cf = cf.replace("[", " ")
    cf = cf.replace("]", " ")

    # remove pure numbers like 300 300 300 / 2000 2000
    cf = re.sub(r"\b\d+\b", " ", cf)

    # keep only letters+digits as tokens
    cf = re.sub(r"[^a-z0-9]+", " ", cf)

    return set(cf.split())


def jaccard_score(tokens1, tokens2):
    if not tokens1 or not tokens2:
        return 0

    return len(tokens1 & tokens2) / len(tokens1 | tokens2)


def pattern_similarity(p1, p2):
    return jaccard_score(tokenize_pattern(p1), tokenize_pattern(p2))


def cuttingfloor_similarity(cf1, cf2):
    return jaccard_score(tokenize_cuttingfloor(cf1), tokenize_cuttingfloor(cf2))


def normalize_meritain_pattern(text):
    if not text:
        return ""

    text = text.lower()
    text = re.sub(r"\d+", "", text)
    text = re.sub(r"[^a-z]+", "", text)
    return text


def find_layout_id(generated_pattern, input_cuttingfloor=None):
    if not generated_pattern:
        return None

    entries = PatternLayoutMapping.objects.all()
    pattern_lower = generated_pattern.lower()

    # ---------------- MERITAIN ----------------
    if "verscend" in pattern_lower or "standard" in pattern_lower:
        gen_clean = normalize_meritain_pattern(generated_pattern)

        best_entry = None
        best_score = -1

        for entry in entries:
            db_clean = normalize_meritain_pattern(entry.pattern)

            if gen_clean == db_clean:
                if input_cuttingfloor and entry.cuttingfloor:
                    cf_score = cuttingfloor_similarity(input_cuttingfloor, entry.cuttingfloor)
                    if cf_score > best_score:
                        best_score = cf_score
                        best_entry = entry
                else:
                    return entry.layout_id

        if best_entry:
            return best_entry.layout_id

        return None

    # ---------------- UHC / GENERAL ----------------
    best_entry = None
    best_score = 0

    for entry in entries:
        p_score = pattern_similarity(generated_pattern, entry.pattern)

        cf_score = 0
        if input_cuttingfloor and entry.cuttingfloor:
            cf_score = cuttingfloor_similarity(input_cuttingfloor, entry.cuttingfloor)

        # pattern is primary, cuttingfloor confirms
        total_score = (0.75 * p_score) + (0.25 * cf_score)

        if total_score > best_score:
            best_score = total_score
            best_entry = entry

    if best_entry and best_score > 0.30:
        return best_entry.layout_id

    return None