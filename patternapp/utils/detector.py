def detect_payer(filename):
    if filename.startswith("ELIG.") or filename.startswith("ICD"):
        return "Meritian"
    elif "_UHC_" in filename:
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

    if filename.startswith("ELIG."):
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