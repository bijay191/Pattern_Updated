import re
from patternapp.models import CentralizedPattern

def find_layout_id(generic_pattern):
    for entry in CentralizedPattern.objects.all():
        try:
            if re.fullmatch(entry.pattern, generic_pattern):
                return entry.layout_id
        except:
            continue
    return None