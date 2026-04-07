import re
from patternapp.models import PatternLayoutMapping

def find_layout_id(generic_pattern):
    generic_pattern = generic_pattern.lower()  # 🔥 normalize

    for entry in PatternLayoutMapping.objects.all():
        db_pattern = entry.generic_pattern.lower()  # 🔥 normalize

        try:
            if re.fullmatch(db_pattern, generic_pattern):
                return entry.layout_id
        except:
            continue

    return None