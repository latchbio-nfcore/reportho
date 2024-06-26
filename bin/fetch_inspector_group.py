#!/usr/bin/env python3

# Written by Igor Trujnara, released under the MIT license
# See https://opensource.org/license/mit for details

import sys

from utils import safe_get


def fetch_inspector_by_id(uniprot_id: str, db_id: str = "Eukaryota2019") -> None:
    """
    Fetch orthologs for a given UniProt ID from the OrthoInspector database.
    """
    url = f"https://lbgi.fr/api/orthoinspector/{db_id}/protein/{uniprot_id}/orthologs"
    res = safe_get(url)

    if not res.ok:
        raise ValueError(f"HTTP error: {res.status_code}")

    json = res.json()
    orthologs = set()

    for i in json["data"]:
        for j in i["orthologs"]:
            orthologs.add(j)

    print("\n".join(orthologs))


def main() -> None:
    if len(sys.argv) < 3:
        raise ValueError("Too few arguments. Usage: fetch_inspector_group.py <id> <db_id>")

    fetch_inspector_by_id(sys.argv[1], sys.argv[2])


if __name__ == "__main__":
    main()
