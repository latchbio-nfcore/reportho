#!/usr/bin/env python3

# Written by Igor Trujnara, released under the MIT license
# See https://opensource.org/license/mit for details

import gzip
import sys


def oma2uniprot_local(ids_path: str, idmap_path: str) -> None:
    """
    Map a list of OMA IDs to UniProt IDs using a local ID mapping file.
    """
    with open(ids_path) as f:
        oma_ids = f.read().splitlines()

    mapping = dict()
    with gzip.open(idmap_path, "rt") as f:
        for line in f:
            items = line.split()
            if items[0] not in mapping and "_" not in items[1]:
                mapping[items[0]] = items[1]

    ids_mapped = [mapping[i] for i in oma_ids if i in mapping]
    ids_unmapped = [i for i in oma_ids if i not in mapping]

    for i in ids_mapped + ids_unmapped:
        print(i)


def main() -> None:
    if len(sys.argv) < 3:
        raise ValueError("Too few arguments. Usage: oma2uniprot_local.py <idmap_path> <ids_path>")

    oma2uniprot_local(sys.argv[2], sys.argv[1])


if __name__ == "__main__":
    main()
