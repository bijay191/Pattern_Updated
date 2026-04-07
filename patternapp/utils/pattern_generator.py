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

        prefix = parts[0]
        policy = parts[2]

        if fmt == "FORMAT_2":

            suffix = "_".join(parts[7:]) if len(parts) > 7 else ""

            suffix = re.sub(r"(\d+)(?=\.[Tt][Xx][Tt]$)", "[0-9]+", suffix)

            if dtype == "ELIG":
                return f"{prefix}_UHC_{policy}_ELIGIBILITIES_[0-9]+_[0-9]+_SPLIT_{suffix}"

            elif dtype == "CLAIMS":
                return f"{prefix}_UHC_{policy}_CLAIMS_[0-9]+_[0-9]+_SPLIT_{suffix}"

            elif dtype == "RX":
                return f"{prefix}_UHC_{policy}_RXCLAIMS_[0-9]+_[0-9]+_SPLIT_{suffix}"

        elif fmt == "CLAIMS_FORMAT_1":
            suffix = "_".join(parts[7:]) if len(parts) > 7 else ""
            suffix = re.sub(r"(\d+)(?=\.[Tt][Xx][Tt]$)", "[0-9]+", suffix)

            return f"{prefix}_UHC_{policy}_CLAIMS_[0-9]+_[0-9]+_SPLIT_{suffix}"

        elif fmt == "RX_FORMAT_1":
            return f"{prefix}_UHC_{policy}_RXCLAIMS_[0-9]+_[0-9]+_SPLIT.txt"

        elif fmt == "ELIG_FORMAT_1":
            return f"{prefix}_UHC_{policy}_ELIGIBILITIES_[0-9]+_[0-9]+_SPLIT.txt"