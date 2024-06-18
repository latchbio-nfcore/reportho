
from dataclasses import dataclass
import typing
import typing_extensions

from flytekit.core.annotation import FlyteAnnotation

from latch.types.metadata import NextflowParameter
from latch.types.file import LatchFile
from latch.types.directory import LatchDir, LatchOutputDir

# Import these into your `__init__.py` file:
#
# from .parameters import generated_parameters

generated_parameters = {
    'input': NextflowParameter(
        type=LatchFile,
        default=None,
        section_title='Input/output options',
        description='Path to comma-separated file containing information about the samples in the experiment.',
    ),
    'outdir': NextflowParameter(
        type=typing_extensions.Annotated[LatchDir, FlyteAnnotation({'output': True})],
        default=None,
        section_title=None,
        description='The output directory where the results will be saved. You have to use absolute paths to storage on Cloud infrastructure.',
    ),
    'output_intermediates': NextflowParameter(
        type=typing.Optional[bool],
        default='false',
        section_title=None,
        description='Output intermediate files, including specific prediction lists.',
    ),
    'email': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='Email address for completion summary.',
    ),
    'multiqc_title': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='MultiQC report title. Printed as page header, used for filename if not otherwise specified.',
    ),
    'use_all': NextflowParameter(
        type=typing.Optional[bool],
        default='false',
        section_title='Ortholog search options',
        description='Use all ortholog search methods. Will mix online and local methods if needed. Overrides all individual database flags.',
    ),
    'local_databases': NextflowParameter(
        type=typing.Optional[bool],
        default='false',
        section_title=None,
        description='Use local databases for the analysis.',
    ),
    'offline_run': NextflowParameter(
        type=typing.Optional[bool],
        default='false',
        section_title=None,
        description='Run the pipeline in offline mode. Overrides all online database flags.',
    ),
    'skip_oma': NextflowParameter(
        type=typing.Optional[bool],
        default='false',
        section_title=None,
        description='Skip using OMA for the ortholog search.',
    ),
    'oma_path': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='Path to the OMA database.',
    ),
    'oma_uniprot_path': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='Path to the Uniprot-OMA ID map.',
    ),
    'oma_ensembl_path': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='Path to the Ensembl-OMA ID map.',
    ),
    'oma_refseq_path': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='Path to the RefSeq-OMA ID map.',
    ),
    'skip_panther': NextflowParameter(
        type=typing.Optional[bool],
        default='false',
        section_title=None,
        description='Skip using PANTHER for the ortholog search.',
    ),
    'panther_path': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='Path to the PANTHER database.',
    ),
    'skip_orthoinspector': NextflowParameter(
        type=typing.Optional[bool],
        default='false',
        section_title=None,
        description='Skip using OrthoInspector for the ortholog search.',
    ),
    'orthoinspector_version': NextflowParameter(
        type=typing.Optional[str],
        default='Eukaryota2023',
        section_title=None,
        description='The version of the OrthoInspector database to use.',
    ),
    'orthoinspector_path': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='Path to the OrthoInspector database.',
    ),
    'skip_eggnog': NextflowParameter(
        type=typing.Optional[bool],
        default='false',
        section_title=None,
        description='Use EggNOG for the ortholog search.',
    ),
    'eggnog_path': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='Path to the EggNOG database.',
    ),
    'eggnog_idmap_path': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='Path to the EggNOG ID map.',
    ),
    'use_centroid': NextflowParameter(
        type=typing.Optional[bool],
        default='false',
        section_title=None,
        description='Use centroid strategy for the ortholog search. Overrides min_score.',
    ),
    'min_score': NextflowParameter(
        type=typing.Optional[float],
        default=2,
        section_title=None,
        description='Minimum score for the ortholog search.',
    ),
    'skip_downstream': NextflowParameter(
        type=typing.Optional[bool],
        default='false',
        section_title='Downstream analysis options',
        description='Skip the downstream analysis. Overrides all other downstream options.',
    ),
    'skip_report': NextflowParameter(
        type=typing.Optional[bool],
        default='false',
        section_title=None,
        description='Skip report generation.',
    ),
    'use_structures': NextflowParameter(
        type=typing.Optional[bool],
        default='false',
        section_title=None,
        description='Use structures for the analysis.',
    ),
    'iqtree_bootstrap': NextflowParameter(
        type=typing.Optional[int],
        default=1000,
        section_title=None,
        description='Number of bootstrap replicates for IQ-TREE.',
    ),
    'fastme_bootstrap': NextflowParameter(
        type=typing.Optional[int],
        default=100,
        section_title=None,
        description='Number of bootstrap replicates for FastME.',
    ),
    'skip_orthoplots': NextflowParameter(
        type=typing.Optional[bool],
        default='false',
        section_title='Process skipping options',
        description='Skip the ortholog plots.',
    ),
    'skip_iqtree': NextflowParameter(
        type=typing.Optional[bool],
        default='false',
        section_title=None,
        description='Skip using IQ-TREE for the phylogenetic analysis.',
    ),
    'skip_fastme': NextflowParameter(
        type=typing.Optional[bool],
        default='false',
        section_title=None,
        description='Skip using FastME for the phylogenetic analysis.',
    ),
    'skip_treeplots': NextflowParameter(
        type=typing.Optional[bool],
        default='false',
        section_title=None,
        description='Skip the tree plots.',
    ),
    'skip_multiqc': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='Skip MultiQC.',
    ),
    'multiqc_methods_description': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title='Generic options',
        description='Custom MultiQC yaml file containing HTML including a methods description.',
    ),
}

