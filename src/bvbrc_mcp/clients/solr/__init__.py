import httpx

from .core.http_client import create_context, run as run_internal
from .resources.antibiotics import Antibiotics
from .resources.bioset import Bioset
from .resources.bioset_result import BiosetResult
from .resources.enzyme_class_ref import EnzymeClassRef
from .resources.epitope import Epitope
from .resources.epitope_assay import EpitopeAssay
from .resources.experiment import Experiment
from .resources.feature_sequence import FeatureSequence
from .resources.gene_ontology_ref import GeneOntologyRef
from .resources.genome import Genome
from .resources.genome_amr import GenomeAmr
from .resources.genome_feature import GenomeFeature
from .resources.genome_sequence import GenomeSequence
from .resources.id_ref import IdRef
from .resources.pathway import Pathway
from .resources.pathway_ref import PathwayRef
from .resources.ppi import Ppi
from .resources.protein_feature import ProteinFeature
from .resources.protein_family_ref import ProteinFamilyRef
from .resources.protein_structure import ProteinStructure
from .resources.sequence_feature import SequenceFeature
from .resources.sequence_feature_vt import SequenceFeatureVt
from .resources.serology import Serology
from .resources.misc_niaid_sgc import MiscNiaidSgc
from .resources.spike_lineage import SpikeLineage
from .resources.spike_variant import SpikeVariant
from .resources.sp_gene import SpGene
from .resources.sp_gene_ref import SpGeneRef
from .resources.strain import Strain
from .resources.structured_assertion import StructuredAssertion
from .resources.subsystem import Subsystem
from .resources.subsystem_ref import SubsystemRef
from .resources.surveillance import Surveillance
from .resources.taxonomy import Taxonomy


class AsyncBVBRCClient:
  """
  Async BV-BRC API client with shared connection pooling.

  Usage:
    async with create_client() as client:
      ...
  """

  def __init__(self, context_overrides: dict | None = None):
    self._ctx = create_context(context_overrides or {})
    self._http_client: httpx.AsyncClient | None = None

  async def __aenter__(self):
    # Shared async client used by async Solr selectors.
    self._http_client = httpx.AsyncClient(timeout=self._ctx.get("timeout", 60.0))

    # Keep resource objects API-compatible; they still consume context only.
    self.antibiotics = Antibiotics(self._ctx)
    self.bioset = Bioset(self._ctx)
    self.bioset_result = BiosetResult(self._ctx)
    self.enzyme_class_ref = EnzymeClassRef(self._ctx)
    self.epitope = Epitope(self._ctx)
    self.epitope_assay = EpitopeAssay(self._ctx)
    self.experiment = Experiment(self._ctx)
    self.feature_sequence = FeatureSequence(self._ctx)
    self.gene_ontology_ref = GeneOntologyRef(self._ctx)
    self.genome = Genome(self._ctx)
    self.genome_amr = GenomeAmr(self._ctx)
    self.genome_feature = GenomeFeature(self._ctx)
    self.genome_sequence = GenomeSequence(self._ctx)
    self.id_ref = IdRef(self._ctx)
    self.pathway = Pathway(self._ctx)
    self.pathway_ref = PathwayRef(self._ctx)
    self.ppi = Ppi(self._ctx)
    self.protein_feature = ProteinFeature(self._ctx)
    self.protein_family_ref = ProteinFamilyRef(self._ctx)
    self.protein_structure = ProteinStructure(self._ctx)
    self.sequence_feature = SequenceFeature(self._ctx)
    self.sequence_feature_vt = SequenceFeatureVt(self._ctx)
    self.serology = Serology(self._ctx)
    self.misc_niaid_sgc = MiscNiaidSgc(self._ctx)
    self.spike_lineage = SpikeLineage(self._ctx)
    self.spike_variant = SpikeVariant(self._ctx)
    self.sp_gene = SpGene(self._ctx)
    self.sp_gene_ref = SpGeneRef(self._ctx)
    self.strain = Strain(self._ctx)
    self.structured_assertion = StructuredAssertion(self._ctx)
    self.subsystem = Subsystem(self._ctx)
    self.subsystem_ref = SubsystemRef(self._ctx)
    self.surveillance = Surveillance(self._ctx)
    self.taxonomy = Taxonomy(self._ctx)
    return self

  async def __aexit__(self, exc_type, exc_val, exc_tb):
    if self._http_client:
      await self._http_client.aclose()
    return False


def create_client(context_overrides: dict | None = None):
  """Factory to create an async client context manager."""
  return AsyncBVBRCClient(context_overrides)


def query(core: str, filter: str = "", options: dict | None = None):
  """Generic query function against any core.

  Args:
    core: The collection/core name, e.g. "genome".
    filter: RQL filter string (e.g. "eq(genome_id,123.45)").
    options: dict with optional keys: select (list[str]), sort (str), limit (int), http_download (bool).
  """
  ctx = create_context({})
  return run_internal(core, filter, options or {}, ctx["base_url"], ctx["headers"])


__all__ = [
  "AsyncBVBRCClient",
  "create_client",
  "query",
  "Antibiotics",
  "Bioset",
  "BiosetResult",
  "EnzymeClassRef",
  "Epitope",
  "EpitopeAssay",
  "Experiment",
  "FeatureSequence",
  "GeneOntologyRef",
  "Genome",
  "GenomeAmr",
  "GenomeFeature",
  "GenomeSequence",
  "IdRef",
  "Pathway",
  "PathwayRef",
  "Ppi",
  "ProteinFeature",
  "ProteinFamilyRef",
  "ProteinStructure",
  "SequenceFeature",
  "SequenceFeatureVt",
  "Serology",
  "MiscNiaidSgc",
  "SpikeLineage",
  "SpikeVariant",
  "SpGene",
  "SpGeneRef",
  "Strain",
  "StructuredAssertion",
  "Subsystem",
  "SubsystemRef",
  "Surveillance",
  "Taxonomy",
]


