import re

def generate_generic_pattern(filename):
    return re.sub(r'\d+', '[0-9]+', filename)