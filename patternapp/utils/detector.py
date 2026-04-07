from transformers import pipeline
import re

# ---------------- AI PART ----------------
generator = None

def get_model():
    global generator
    if generator is None:
        generator = pipeline(
            "text-generation",
            model="google/flan-t5-base",
            max_length=128
        )
    return generator

def build_prompt(filename):
    return f"""
Convert this filename into a regex pattern.

Filename:
{filename}

Regex:
"""

def clean_output(output):
    if "Regex:" in output:
        output = output.split("Regex:")[-1]

    return output.strip().split("\n")[0]

def fallback_regex(filename):
    regex = filename
    regex = re.sub(r"\d+", r"[0-9]+", regex)
    regex = regex.replace(".", r"\.")
    return regex

def detect_payer(filename):
    f = filename.lower()

    if f.startswith("elig.") or f.startswith("icd"):
        return "MERITAIN"
    elif "_uhc_" in f:
        return "UHC"
    return "UNKNOWN"


def detect_data_type(filename):
    f = filename.lower()

    if "rxclaims" in f:
        return "RX"
    elif "elig" in f:
        return "ELIG"
    elif "claims" in f:
        return "CLAIMS"

    return "UNKNOWN"


def detect_format(filename):
    f = filename.lower()

    if f.startswith("elig."):
        return "Meritian_ELIG"

    if "claims.abstract" in f:
        return "Meritian_CLAIMS"

    if "split" in f and "palrx" in f:
        return "RX_FORMAT_1"

    if "split" in f and "medclm" in f:
        return "CLAIMS_FORMAT_1"

    if "elig_clm" in f:
        return "ELIG_FORMAT_1"

    if "split" in f:
        return "FORMAT_2"

    return "UNKNOWN"