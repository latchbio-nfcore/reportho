#!/usr/bin/env python3

# Written by Igor Trujnara, released under the MIT license
# See https://opensource.org/license/mit for details

import sys

from map_uniprot import map_uniprot


def main() -> None:
    """
    Map IDs from OMA to UniProt IDs.
    """
    if len(sys.argv) != 2:
        print("Usage: python uniprotize_oma.py <oma_group_file>")
        sys.exit(1)

    oma_ids: list[str] = []

    with open(sys.argv[1]) as f:
        for line in f:
            oma_ids.append(line.strip())
    oma_ids_mapped = map_uniprot(oma_ids)

    for i in oma_ids_mapped:
        print(i)

if __name__ == "__main__":
    main()
