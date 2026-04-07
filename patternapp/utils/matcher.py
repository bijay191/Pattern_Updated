import re
from patternapp.models import PatternLayoutMapping

def tokenize(pattern):
    if not pattern:
        return set()

    pattern = pattern.lower()

    # remove regex parts
    pattern = re.sub(r"\[[0-9]+\]|\[0-9\]\{\d+\}", "", pattern)

    if "verscend" in pattern or "standard" in pattern:
        pattern = re.sub(r"\d+", "", pattern)

    else:
        pattern = re.sub(r"\b\d{6,}\b", "", pattern)

    # remove special chars
    pattern = re.sub(r"[^a-z0-9]+", " ", pattern)

    return set(pattern.split())


def similarity_score(p1, p2):
    tokens1 = tokenize(p1)
    tokens2 = tokenize(p2)

    if not tokens1 or not tokens2:
        return 0

    return len(tokens1 & tokens2) / len(tokens1 | tokens2)


def find_layout_id(generated_pattern):
    if not generated_pattern:
        return None

    pattern_lower = generated_pattern.lower()

    # ---------------- MERITAIN DIRECT MATCH ----------------
    if "verscend" in pattern_lower:
        for entry in PatternLayoutMapping.objects.all():
            db_pattern = entry.pattern.lower()

            # remove numbers from both
            gen_clean = re.sub(r"\d+", "", pattern_lower)
            db_clean = re.sub(r"\d+", "", db_pattern)

            if gen_clean == db_clean:
                return entry.layout_id

        return None

    # ---------------- UHC SIMILARITY MATCH ----------------
    best_score = 0
    best_layout = None

    for entry in PatternLayoutMapping.objects.all():
        db_pattern = entry.pattern

        score = similarity_score(generated_pattern, db_pattern)

        if score > best_score:
            best_score = score
            best_layout = entry.layout_id

    if best_score > 0.3:
        return best_layout

    return None