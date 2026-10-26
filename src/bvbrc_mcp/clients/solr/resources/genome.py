from __future__ import annotations

from typing import Any, Dict

from ..core.http_client import run
from ..core.query_builder import qb
from ..core.solr_query_builder import qb as solrqb
from ..core.solr_http_client import create_solr_context
from ..core.cursor import CursorPager


class Genome:
  def __init__(self, context: Dict[str, Any]):
    self._ctx = context

  def get_by_id(self, genome_id: str, options: Dict[str, Any] | None = None):
    return run("genome", qb.eq("genome_id", genome_id), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def query_by(self, filters: Dict[str, Any] | None = None, options: Dict[str, Any] | None = None):
    return run("genome", qb.build_and_from(filters or {}), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_taxon_id(self, taxon_id: int, options: Dict[str, Any] | None = None):
    return run("genome", qb.eq("taxon_id", taxon_id), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_genome_name(self, genome_name: str, options: Dict[str, Any] | None = None):
    return run("genome", qb.eq("genome_name", genome_name), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_strain(self, strain: str, options: Dict[str, Any] | None = None):
    return run("genome", qb.eq("strain", strain), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_species(self, species: str, options: Dict[str, Any] | None = None):
    return run("genome", qb.eq("species", species), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_genus(self, genus: str, options: Dict[str, Any] | None = None):
    return run("genome", qb.eq("genus", genus), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_family(self, family: str, options: Dict[str, Any] | None = None):
    return run("genome", qb.eq("family", family), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_order(self, order: str, options: Dict[str, Any] | None = None):
    return run("genome", qb.eq("order", order), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_class(self, class_name: str, options: Dict[str, Any] | None = None):
    return run("genome", qb.eq("class", class_name), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_phylum(self, phylum: str, options: Dict[str, Any] | None = None):
    return run("genome", qb.eq("phylum", phylum), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_kingdom(self, kingdom: str, options: Dict[str, Any] | None = None):
    return run("genome", qb.eq("kingdom", kingdom), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_superkingdom(self, superkingdom: str, options: Dict[str, Any] | None = None):
    return run("genome", qb.eq("superkingdom", superkingdom), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_genome_status(self, genome_status: str, options: Dict[str, Any] | None = None):
    return run("genome", qb.eq("genome_status", genome_status), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_genome_quality(self, genome_quality: str, options: Dict[str, Any] | None = None):
    return run("genome", qb.eq("genome_quality", genome_quality), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_assembly_accession(self, assembly_accession: str, options: Dict[str, Any] | None = None):
    return run("genome", qb.eq("assembly_accession", assembly_accession), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_bioproject_accession(self, bioproject_accession: str, options: Dict[str, Any] | None = None):
    return run("genome", qb.eq("bioproject_accession", bioproject_accession), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_biosample_accession(self, biosample_accession: str, options: Dict[str, Any] | None = None):
    return run("genome", qb.eq("biosample_accession", biosample_accession), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_sra_accession(self, sra_accession: str, options: Dict[str, Any] | None = None):
    return run("genome", qb.eq("sra_accession", sra_accession), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_refseq_accessions(self, refseq_accessions: str, options: Dict[str, Any] | None = None):
    return run("genome", qb.eq("refseq_accessions", refseq_accessions), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_genbank_accessions(self, genbank_accessions: str, options: Dict[str, Any] | None = None):
    return run("genome", qb.eq("genbank_accessions", genbank_accessions), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_gram_stain(self, gram_stain: str, options: Dict[str, Any] | None = None):
    return run("genome", qb.eq("gram_stain", gram_stain), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_motility(self, motility: str, options: Dict[str, Any] | None = None):
    return run("genome", qb.eq("motility", motility), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_oxygen_requirement(self, oxygen_requirement: str, options: Dict[str, Any] | None = None):
    return run("genome", qb.eq("oxygen_requirement", oxygen_requirement), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_habitat(self, habitat: str, options: Dict[str, Any] | None = None):
    return run("genome", qb.eq("habitat", habitat), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_isolation_country(self, isolation_country: str, options: Dict[str, Any] | None = None):
    return run("genome", qb.eq("isolation_country", isolation_country), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_isolation_source(self, isolation_source: str, options: Dict[str, Any] | None = None):
    return run("genome", qb.eq("isolation_source", isolation_source), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_geographic_location(self, geographic_location: str, options: Dict[str, Any] | None = None):
    return run("genome", qb.eq("geographic_location", geographic_location), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_geographic_group(self, geographic_group: str, options: Dict[str, Any] | None = None):
    return run("genome", qb.eq("geographic_group", geographic_group), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_cell_shape(self, cell_shape: str, options: Dict[str, Any] | None = None):
    return run("genome", qb.eq("cell_shape", cell_shape), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_sporulation(self, sporulation: str, options: Dict[str, Any] | None = None):
    return run("genome", qb.eq("sporulation", sporulation), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_optimal_temperature(self, optimal_temperature: str, options: Dict[str, Any] | None = None):
    return run("genome", qb.eq("optimal_temperature", optimal_temperature), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_temperature_range(self, temperature_range: str, options: Dict[str, Any] | None = None):
    return run("genome", qb.eq("temperature_range", temperature_range), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_salinity(self, salinity: str, options: Dict[str, Any] | None = None):
    return run("genome", qb.eq("salinity", salinity), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_depth(self, depth: str, options: Dict[str, Any] | None = None):
    return run("genome", qb.eq("depth", depth), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_altitude(self, altitude: str, options: Dict[str, Any] | None = None):
    return run("genome", qb.eq("altitude", altitude), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_type_strain(self, type_strain: str, options: Dict[str, Any] | None = None):
    return run("genome", qb.eq("type_strain", type_strain), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_serovar(self, serovar: str, options: Dict[str, Any] | None = None):
    return run("genome", qb.eq("serovar", serovar), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_pathovar(self, pathovar: str, options: Dict[str, Any] | None = None):
    return run("genome", qb.eq("pathovar", pathovar), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_biovar(self, biovar: str, options: Dict[str, Any] | None = None):
    return run("genome", qb.eq("biovar", biovar), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_clade(self, clade: str, options: Dict[str, Any] | None = None):
    return run("genome", qb.eq("clade", clade), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_subclade(self, subclade: str, options: Dict[str, Any] | None = None):
    return run("genome", qb.eq("subclade", subclade), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_subtype(self, subtype: str, options: Dict[str, Any] | None = None):
    return run("genome", qb.eq("subtype", subtype), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_lineage(self, lineage: str, options: Dict[str, Any] | None = None):
    return run("genome", qb.eq("lineage", lineage), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_mlst(self, mlst: str, options: Dict[str, Any] | None = None):
    return run("genome", qb.eq("mlst", mlst), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_sequencing_platform(self, sequencing_platform: str, options: Dict[str, Any] | None = None):
    return run("genome", qb.eq("sequencing_platform", sequencing_platform), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_assembly_method(self, assembly_method: str, options: Dict[str, Any] | None = None):
    return run("genome", qb.eq("assembly_method", assembly_method), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_genome_length_range(self, min_length: int, max_length: int, options: Dict[str, Any] | None = None):
    filters = [qb.gt("genome_length", min_length), qb.lt("genome_length", max_length)]
    return run("genome", qb.and_(*filters), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_gc_content_range(self, min_gc: float, max_gc: float, options: Dict[str, Any] | None = None):
    filters = [qb.gt("gc_content", min_gc), qb.lt("gc_content", max_gc)]
    return run("genome", qb.and_(*filters), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_cds_count_range(self, min_cds: int, max_cds: int, options: Dict[str, Any] | None = None):
    filters = [qb.gt("cds", min_cds), qb.lt("cds", max_cds)]
    return run("genome", qb.and_(*filters), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_contig_count_range(self, min_contigs: int, max_contigs: int, options: Dict[str, Any] | None = None):
    filters = [qb.gt("contigs", min_contigs), qb.lt("contigs", max_contigs)]
    return run("genome", qb.and_(*filters), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_collection_year_range(self, start_year: int, end_year: int, options: Dict[str, Any] | None = None):
    filters = [qb.gt("collection_year", start_year), qb.lt("collection_year", end_year)]
    return run("genome", qb.and_(*filters), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_date_range(self, start_date: str, end_date: str, options: Dict[str, Any] | None = None):
    filters = [qb.gt("date_inserted", start_date), qb.lt("date_inserted", end_date)]
    return run("genome", qb.and_(*filters), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_public_status(self, is_public: bool, options: Dict[str, Any] | None = None):
    return run("genome", qb.eq("public", is_public), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_all(self, options: Dict[str, Any] | None = None):
    return run("genome", "", options or {}, self._ctx["base_url"], self._ctx["headers"])

  # Solr cursor-based streaming (Option B implementation)
  def stream_all_solr(
    self,
    *,
    rows: int = 1000,
    sort: str | None = None,
    unique_key: str | None = "genome_id",
    fields: list[str] | None = None,
    q_expr: str | None = None,
    fq: list[str] | None = None,
    start_cursor: str = "*",
    context_overrides: Dict[str, Any] | None = None,
  ) -> CursorPager:
    # Combine base context with optional overrides to build Solr context
    merged_ctx: Dict[str, Any] = {}
    merged_ctx.update(self._ctx)
    if context_overrides:
      merged_ctx.update(context_overrides)
    solr_ctx = create_solr_context(merged_ctx)

    base_params = solrqb.build_params(
      q_expr=q_expr or "*:*",
      fq_list=fq or None,
      fields=fields or None,
      # sort, rows, cursorMark handled by CursorPager for iteration
    )

    return CursorPager(
      collection="genome",
      base_params=base_params,
      base_url=solr_ctx["solr_base_url"],
      headers=solr_ctx.get("headers"),
      auth=solr_ctx.get("auth"),
      rows=rows,
      sort=sort,
      unique_key=unique_key,
      start_cursor=start_cursor,
      timeout=solr_ctx.get("timeout", 60.0),
    )


__all__ = ["Genome"]


