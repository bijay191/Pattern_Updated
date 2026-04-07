from .detector import detect_payer, detect_data_type, detect_format
import re


def generate_pattern(filename):
    payer = detect_payer(filename)
    dtype = detect_data_type(filename)
    fmt = detect_format(filename)

    # ---------- MERITAIN ----------
    if payer == "MERITAIN":

        parts = filename.split('.')
        policy = parts[4]

        if fmt == "Meritian_ELIG":
            return f"ELIG.EXTRACT.VERSCEND.ELIG.{policy}.[0-9]+"

        elif fmt == "Meritian_CLAIMS":
            return f"ICD10.STANDARD.CLAIMS.EXTRACT.{policy}.[0-9]{{8}}"

    # ---------- UHC ----------
    elif payer == "UHC":
        parts = filename.split('_')

        prefix = parts[0]     # 718
        policy = parts[2]     # 94777

        if fmt == "ELIG_FORMAT_1":
            return f"{prefix}_UHC_{policy}_ELIGIBILITIES_[0-9]+_[0-9]+_SPLIT.txt"

        elif fmt == "CLAIMS_FORMAT_1":
            suffix = parts[7] if len(parts) > 7 else ""

            # convert numbers inside suffix to regex
            suffix = re.sub(r"(\D)\d+(\.txt)", r"\1[0-9]+\2", suffix)

            return f"{prefix}_UHC_{policy}_CLAIMS_[0-9]+_[0-9]+_SPLIT_{suffix}"

        elif fmt == "RX_FORMAT_1":
            return f"{prefix}_UHC_{policy}_RXCLAIMS_[0-9]+_[0-9]+_SPLIT.txt"

        elif fmt == "FORMAT_2":
            group = parts[7] if len(parts) > 7 else "UNKNOWN"

            if dtype == "RX":
                return f"{prefix}_UHC_{policy}_RXCLAIMS_[0-9]+_[0-9]+_SPLIT_{group}_[0-9]+_[0-9]+_[0-9]+_[0-9]+.txt"

            elif dtype == "CLAIMS":
                return f"{prefix}_UHC_{policy}_CLAIMS_[0-9]+_[0-9]+_SPLIT_{group}_[0-9]+_[0-9]+_[0-9]+_[0-9]+.txt"

            elif dtype == "ELIG":
                return f"{prefix}_UHC_{policy}_ELIGIBILITIES_[0-9]+_[0-9]+_SPLIT_{group}_[0-9]+_[0-9]+_[0-9]+_[0-9]+.txt"

    return None