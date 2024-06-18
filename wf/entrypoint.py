from dataclasses import dataclass
from enum import Enum
import os
import subprocess
import requests
import shutil
from pathlib import Path
import typing
import typing_extensions

from latch.resources.workflow import workflow
from latch.resources.tasks import nextflow_runtime_task, custom_task
from latch.types.file import LatchFile
from latch.types.directory import LatchDir, LatchOutputDir
from latch.ldata.path import LPath
from latch_cli.nextflow.workflow import get_flag
from latch_cli.nextflow.utils import _get_execution_name
from latch_cli.utils import urljoins
from latch.types import metadata
from flytekit.core.annotation import FlyteAnnotation

from latch_cli.services.register.utils import import_module_by_path

meta = Path("latch_metadata") / "__init__.py"
import_module_by_path(meta)
import latch_metadata

@custom_task(cpu=0.25, memory=0.5, storage_gib=1)
def initialize() -> str:
    token = os.environ.get("FLYTE_INTERNAL_EXECUTION_ID")
    if token is None:
        raise RuntimeError("failed to get execution token")

    headers = {"Authorization": f"Latch-Execution-Token {token}"}

    print("Provisioning shared storage volume... ", end="")
    resp = requests.post(
        "http://nf-dispatcher-service.flyte.svc.cluster.local/provision-storage",
        headers=headers,
        json={
            "storage_gib": 100,
        }
    )
    resp.raise_for_status()
    print("Done.")

    return resp.json()["name"]






@nextflow_runtime_task(cpu=4, memory=8, storage_gib=100)
def nextflow_runtime(pvc_name: str, input: LatchFile, outdir: typing_extensions.Annotated[LatchDir, FlyteAnnotation({'output': True})], email: typing.Optional[str], multiqc_title: typing.Optional[str], oma_path: typing.Optional[str], oma_uniprot_path: typing.Optional[str], oma_ensembl_path: typing.Optional[str], oma_refseq_path: typing.Optional[str], panther_path: typing.Optional[str], orthoinspector_path: typing.Optional[str], eggnog_path: typing.Optional[str], eggnog_idmap_path: typing.Optional[str], skip_multiqc: typing.Optional[bool], multiqc_methods_description: typing.Optional[str], output_intermediates: typing.Optional[bool], use_all: typing.Optional[bool], local_databases: typing.Optional[bool], offline_run: typing.Optional[bool], skip_oma: typing.Optional[bool], skip_panther: typing.Optional[bool], skip_orthoinspector: typing.Optional[bool], orthoinspector_version: typing.Optional[str], skip_eggnog: typing.Optional[bool], use_centroid: typing.Optional[bool], min_score: typing.Optional[float], skip_downstream: typing.Optional[bool], skip_report: typing.Optional[bool], use_structures: typing.Optional[bool], iqtree_bootstrap: typing.Optional[int], fastme_bootstrap: typing.Optional[int], skip_orthoplots: typing.Optional[bool], skip_iqtree: typing.Optional[bool], skip_fastme: typing.Optional[bool], skip_treeplots: typing.Optional[bool]) -> None:
    try:
        shared_dir = Path("/nf-workdir")



        ignore_list = [
            "latch",
            ".latch",
            "nextflow",
            ".nextflow",
            "work",
            "results",
            "miniconda",
            "anaconda3",
            "mambaforge",
        ]

        shutil.copytree(
            Path("/root"),
            shared_dir,
            ignore=lambda src, names: ignore_list,
            ignore_dangling_symlinks=True,
            dirs_exist_ok=True,
        )

        cmd = [
            "/root/nextflow",
            "run",
            str(shared_dir / "main.nf"),
            "-work-dir",
            str(shared_dir),
            "-profile",
            "docker",
            "-c",
            "latch.config",
                *get_flag('input', input),
                *get_flag('outdir', outdir),
                *get_flag('output_intermediates', output_intermediates),
                *get_flag('email', email),
                *get_flag('multiqc_title', multiqc_title),
                *get_flag('use_all', use_all),
                *get_flag('local_databases', local_databases),
                *get_flag('offline_run', offline_run),
                *get_flag('skip_oma', skip_oma),
                *get_flag('oma_path', oma_path),
                *get_flag('oma_uniprot_path', oma_uniprot_path),
                *get_flag('oma_ensembl_path', oma_ensembl_path),
                *get_flag('oma_refseq_path', oma_refseq_path),
                *get_flag('skip_panther', skip_panther),
                *get_flag('panther_path', panther_path),
                *get_flag('skip_orthoinspector', skip_orthoinspector),
                *get_flag('orthoinspector_version', orthoinspector_version),
                *get_flag('orthoinspector_path', orthoinspector_path),
                *get_flag('skip_eggnog', skip_eggnog),
                *get_flag('eggnog_path', eggnog_path),
                *get_flag('eggnog_idmap_path', eggnog_idmap_path),
                *get_flag('use_centroid', use_centroid),
                *get_flag('min_score', min_score),
                *get_flag('skip_downstream', skip_downstream),
                *get_flag('skip_report', skip_report),
                *get_flag('use_structures', use_structures),
                *get_flag('iqtree_bootstrap', iqtree_bootstrap),
                *get_flag('fastme_bootstrap', fastme_bootstrap),
                *get_flag('skip_orthoplots', skip_orthoplots),
                *get_flag('skip_iqtree', skip_iqtree),
                *get_flag('skip_fastme', skip_fastme),
                *get_flag('skip_treeplots', skip_treeplots),
                *get_flag('skip_multiqc', skip_multiqc),
                *get_flag('multiqc_methods_description', multiqc_methods_description)
        ]

        print("Launching Nextflow Runtime")
        print(' '.join(cmd))
        print(flush=True)

        env = {
            **os.environ,
            "NXF_HOME": "/root/.nextflow",
            "NXF_OPTS": "-Xms2048M -Xmx8G -XX:ActiveProcessorCount=4",
            "K8S_STORAGE_CLAIM_NAME": pvc_name,
            "NXF_DISABLE_CHECK_LATEST": "true",
        }
        subprocess.run(
            cmd,
            env=env,
            check=True,
            cwd=str(shared_dir),
        )
    finally:
        print()

        nextflow_log = shared_dir / ".nextflow.log"
        if nextflow_log.exists():
            name = _get_execution_name()
            if name is None:
                print("Skipping logs upload, failed to get execution name")
            else:
                remote = LPath(urljoins("latch:///your_log_dir/nf_nf_core_reportho", name, "nextflow.log"))
                print(f"Uploading .nextflow.log to {remote.path}")
                remote.upload_from(nextflow_log)



@workflow(metadata._nextflow_metadata)
def nf_nf_core_reportho(input: LatchFile, outdir: typing_extensions.Annotated[LatchDir, FlyteAnnotation({'output': True})], email: typing.Optional[str], multiqc_title: typing.Optional[str], oma_path: typing.Optional[str], oma_uniprot_path: typing.Optional[str], oma_ensembl_path: typing.Optional[str], oma_refseq_path: typing.Optional[str], panther_path: typing.Optional[str], orthoinspector_path: typing.Optional[str], eggnog_path: typing.Optional[str], eggnog_idmap_path: typing.Optional[str], skip_multiqc: typing.Optional[bool], multiqc_methods_description: typing.Optional[str], output_intermediates: typing.Optional[bool] = 'false', use_all: typing.Optional[bool] = 'false', local_databases: typing.Optional[bool] = 'false', offline_run: typing.Optional[bool] = 'false', skip_oma: typing.Optional[bool] = 'false', skip_panther: typing.Optional[bool] = 'false', skip_orthoinspector: typing.Optional[bool] = 'false', orthoinspector_version: typing.Optional[str] = 'Eukaryota2023', skip_eggnog: typing.Optional[bool] = 'false', use_centroid: typing.Optional[bool] = 'false', min_score: typing.Optional[float] = 2, skip_downstream: typing.Optional[bool] = 'false', skip_report: typing.Optional[bool] = 'false', use_structures: typing.Optional[bool] = 'false', iqtree_bootstrap: typing.Optional[int] = 1000, fastme_bootstrap: typing.Optional[int] = 100, skip_orthoplots: typing.Optional[bool] = 'false', skip_iqtree: typing.Optional[bool] = 'false', skip_fastme: typing.Optional[bool] = 'false', skip_treeplots: typing.Optional[bool] = 'false') -> None:
    """
    nf-core/reportho

    Sample Description
    """

    pvc_name: str = initialize()
    nextflow_runtime(pvc_name=pvc_name, input=input, outdir=outdir, output_intermediates=output_intermediates, email=email, multiqc_title=multiqc_title, use_all=use_all, local_databases=local_databases, offline_run=offline_run, skip_oma=skip_oma, oma_path=oma_path, oma_uniprot_path=oma_uniprot_path, oma_ensembl_path=oma_ensembl_path, oma_refseq_path=oma_refseq_path, skip_panther=skip_panther, panther_path=panther_path, skip_orthoinspector=skip_orthoinspector, orthoinspector_version=orthoinspector_version, orthoinspector_path=orthoinspector_path, skip_eggnog=skip_eggnog, eggnog_path=eggnog_path, eggnog_idmap_path=eggnog_idmap_path, use_centroid=use_centroid, min_score=min_score, skip_downstream=skip_downstream, skip_report=skip_report, use_structures=use_structures, iqtree_bootstrap=iqtree_bootstrap, fastme_bootstrap=fastme_bootstrap, skip_orthoplots=skip_orthoplots, skip_iqtree=skip_iqtree, skip_fastme=skip_fastme, skip_treeplots=skip_treeplots, skip_multiqc=skip_multiqc, multiqc_methods_description=multiqc_methods_description)

