from .detector import detect_payer, detect_data_type, detect_format


def generate_pattern(filename):
    payer = detect_payer(filename)
    dtype = detect_data_type(filename)
    fmt = detect_format(filename)

    # ---------- Meritian ----------
    if payer == "Meritian":

        if fmt == "Meritian_ELIG":
            parts = filename.split('.')
            policy = parts[4]
            return f"ELIG.ABSTRACT.VERSCEND.ELIG.{policy}.[0-9]+"

        elif fmt == "Meritian_CLAIMS":
            parts = filename.split('.')
            policy = parts[4]
            return f"ICD10.STANDARD.CLAIMS.ABSTRACT.{policy}.[0-9]{8}"

    # ---------- UHC ----------
    elif payer == "UHC":
        parts = filename.split('_')
        policy = parts[2]

        if fmt == "RX_FORMAT_1":
            return f"{parts[0]}_UHC_{policy}_RXCLAIMS_[0-9]+_[0-9]+_SPLIT_{policy}palrx[0-9]+.txt"

        elif fmt == "CLAIMS_FORMAT_1":
            return f"{parts[0]}_UHC_{policy}_CLAIMS_[0-9]+_[0-9]+_SPLIT_{policy}medclm[0-9]+.txt"

        elif fmt == "ELIG_FORMAT_1":
            return f"{parts[0]}_UHC_{policy}_ELIGIBILITIES_[0-9]+_[0-9]+_SPLIT_{policy}_ELIG_CLM_P{policy}_[0-9]+.txt"

        elif fmt == "FORMAT_2":
            group = parts[7]

            if dtype == "RX":
                return f"{parts[0]}_XYZ_{policy}_RXCLAIMS_[0-9]+_[0-9]+_SPLIT_{group}_[0-9]+_[0-9]+_[0-9]+_[0-9]+.txt"

            elif dtype == "CLAIMS":
                return f"{parts[0]}_XYZ_{policy}_CLAIMS_[0-9]+_[0-9]+_SPLIT_{group}_[0-9]+_[0-9]+_[0-9]+_[0-9]+.txt"

            elif dtype == "ELIG":
                return f"{parts[0]}_XYZ_{policy}_ELIGIBILITIES_[0-9]+_[0-9]+_SPLIT_{group}_[0-9]+_[0-9]+_[0-9]+_[0-9]+.txt"

    return None