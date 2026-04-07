from .detector import detect_payer, detect_data_type, detect_format
from .pattern_generator import generate_pattern
from .generic_generator import generate_generic_pattern
from .matcher import find_layout_id


def process_filename(filename):
    filename = filename.lower()
    payer = detect_payer(filename)
    dtype = detect_data_type(filename)
    fmt = detect_format(filename)

    pattern = generate_pattern(filename)
    generic = generate_generic_pattern(filename)
    layout_id = find_layout_id(generic)

    return {
        "payer": payer,
        "type": dtype,
        "format": fmt,
        "pattern": pattern,
        "generic": generic,
        "layout_id": layout_id
    }