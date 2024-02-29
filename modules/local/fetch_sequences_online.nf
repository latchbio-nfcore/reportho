process FETCH_SEQUENCES_ONLINE {
    tag "${meta.id}"
    label "process_single"

    // add container here when available

    input:
    tuple val(meta), path(ids), path(query_fasta)

    output:
    tuple val(meta), path("orthologs.fa"), emit: fasta
    path "hits.txt", emit: hits
    path "misses.txt", emit: misses
    path "versions.yml", emit: versions

    script:
    add_query = params.uniprot_query ? "" : "cat $query_fasta >> orthologs.fa"
    """
    fetch_sequences.py $ids > orthologs.fa
    $add_query

    cat <<- END_VERSIONS > versions.yml
    "${task.process}":
        Python: \$(python --version | cut -d ' ' -f 2)
        Python Requests: \$(pip show requests | grep Version | cut -d ' ' -f 2)
    \$(get_oma_version.py)
    END_VERSIONS
    """
}
