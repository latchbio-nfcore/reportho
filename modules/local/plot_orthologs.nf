process PLOT_ORTHOLOGS {
    tag "$meta.id"
    label 'process_single'

    conda     "conda-forge::r-tidyverse=2.0.0 conda-forge::r-reshape2=1.4.4 conda-forge::r-ggvenndiagram=1.5.2"
    container "${ workflow.containerEngine == 'singularity' && !task.ext.singularity_pull_docker_container ?
        'oras://community.wave.seqera.io/library/r-ggvenndiagram_r-reshape2_r-tidyverse:3941632557872dac' :
        'community.wave.seqera.io/library/r-ggvenndiagram_r-reshape2_r-tidyverse:6ab82708ae578c26' }"

    input:
    tuple val(meta), path(score_table)

    output:
    tuple val(meta), path("*_supports_light.png"), path("*_supports_dark.png"), emit: supports
    tuple val(meta), path("*_venn_light.png"), path("*_venn_dark.png")        , emit: venn
    tuple val(meta), path("*_jaccard_light.png"), path("*_jaccard_dark.png")  , emit: jaccard
    path "versions.yml"                                                       , emit: versions

    when:
    task.ext.when == null || task.ext.when

    script:
    prefix = task.ext.prefix ?: meta.id
    """
    plot_orthologs.R $score_table $prefix

    cat <<- END_VERSIONS > versions.yml
    "${task.process}":
        r-base: \$(echo \$(R --version 2>&1) | sed 's/^.*R version //; s/ .*\$//')
    END_VERSIONS
    """

    stub:
    def prefix = task.ext.prefix ?: "${meta.id}"
    """
    touch ${prefix}_supports_dark.png
    touch ${prefix}_supports_light.png
    touch ${prefix}_venn_dark.png
    touch ${prefix}_venn_light.png
    touch ${prefix}_jaccard_dark.png
    touch ${prefix}_jaccard_light.png

    cat <<- END_VERSIONS > versions.yml
    "${task.process}":
        r-base: \$(echo \$(R --version 2>&1) | sed 's/^.*R version //; s/ .*\$//')
    END_VERSIONS
    """
}
