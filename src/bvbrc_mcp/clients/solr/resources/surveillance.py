from __future__ import annotations

from typing import Any, Dict
from urllib.parse import quote

from ..core.http_client import run
from ..core.query_builder import qb
from ..core.solr_query_builder import qb as solrqb
from ..core.solr_http_client import create_solr_context
from ..core.cursor import CursorPager


class Surveillance:
  def __init__(self, context: Dict[str, Any]):
    self._ctx = context

  def get_by_id(self, id: str, options: Dict[str, Any] | None = None):
    return run("surveillance", qb.eq("id", id), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def query_by(self, filters: Dict[str, Any] | None = None, options: Dict[str, Any] | None = None):
    return run("surveillance", qb.build_and_from(filters or {}), options or {}, self._ctx["base_url"], self._ctx["headers"])

  # Host-related methods
  def get_by_host_identifier(self, host_identifier: str, options: Dict[str, Any] | None = None):
    return run("surveillance", qb.eq("host_identifier", host_identifier), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_host_species(self, host_species: str, options: Dict[str, Any] | None = None):
    return run("surveillance", qb.eq("host_species", host_species), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_host_sex(self, host_sex: str, options: Dict[str, Any] | None = None):
    return run("surveillance", qb.eq("host_sex", host_sex), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_host_age(self, host_age: str, options: Dict[str, Any] | None = None):
    return run("surveillance", qb.eq("host_age", host_age), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_host_common_name(self, host_common_name: str, options: Dict[str, Any] | None = None):
    return run("surveillance", qb.eq("host_common_name", host_common_name), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_host_group(self, host_group: str, options: Dict[str, Any] | None = None):
    return run("surveillance", qb.eq("host_group", host_group), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_host_health(self, host_health: str, options: Dict[str, Any] | None = None):
    return run("surveillance", qb.eq("host_health", host_health), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_host_habitat(self, host_habitat: str, options: Dict[str, Any] | None = None):
    return run("surveillance", qb.eq("host_habitat", host_habitat), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_host_natural_state(self, host_natural_state: str, options: Dict[str, Any] | None = None):
    return run("surveillance", qb.eq("host_natural_state", host_natural_state), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_host_capture_status(self, host_capture_status: str, options: Dict[str, Any] | None = None):
    return run("surveillance", qb.eq("host_capture_status", host_capture_status), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_host_id_type(self, host_id_type: str, options: Dict[str, Any] | None = None):
    return run("surveillance", qb.eq("host_id_type", host_id_type), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_host_weight(self, host_weight: str, options: Dict[str, Any] | None = None):
    return run("surveillance", qb.eq("host_weight", host_weight), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_host_height(self, host_height: str, options: Dict[str, Any] | None = None):
    return run("surveillance", qb.eq("host_height", host_height), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_host_ethnicity(self, host_ethnicity: str, options: Dict[str, Any] | None = None):
    return run("surveillance", qb.eq("host_ethnicity", host_ethnicity), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_host_race(self, host_race: str, options: Dict[str, Any] | None = None):
    return run("surveillance", qb.eq("host_race", host_race), options or {}, self._ctx["base_url"], self._ctx["headers"])

  # Sample-related methods
  def get_by_sample_identifier(self, sample_identifier: str, options: Dict[str, Any] | None = None):
    return run("surveillance", qb.eq("sample_identifier", sample_identifier), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_sample_accession(self, sample_accession: str, options: Dict[str, Any] | None = None):
    return run("surveillance", qb.eq("sample_accession", sample_accession), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_sample_material(self, sample_material: str, options: Dict[str, Any] | None = None):
    return run("surveillance", qb.eq("sample_material", sample_material), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_sample_transport_medium(self, sample_transport_medium: str, options: Dict[str, Any] | None = None):
    return run("surveillance", qb.eq("sample_transport_medium", sample_transport_medium), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_sample_receipt_date(self, sample_receipt_date: str, options: Dict[str, Any] | None = None):
    return run("surveillance", qb.eq("sample_receipt_date", sample_receipt_date), options or {}, self._ctx["base_url"], self._ctx["headers"])

  # Collection-related methods
  def get_by_collection_city(self, collection_city: str, options: Dict[str, Any] | None = None):
    return run("surveillance", qb.eq("collection_city", collection_city), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_collection_country(self, collection_country: str, options: Dict[str, Any] | None = None):
    return run("surveillance", qb.eq("collection_country", collection_country), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_collection_state_province(self, collection_state_province: str, options: Dict[str, Any] | None = None):
    return run("surveillance", qb.eq("collection_state_province", collection_state_province), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_collection_poi(self, collection_poi: str, options: Dict[str, Any] | None = None):
    return run("surveillance", qb.eq("collection_poi", collection_poi), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_collection_season(self, collection_season: str, options: Dict[str, Any] | None = None):
    return run("surveillance", qb.eq("collection_season", collection_season), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_collection_year(self, collection_year: str, options: Dict[str, Any] | None = None):
    return run("surveillance", qb.eq("collection_year", collection_year), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_collector_institution(self, collector_institution: str, options: Dict[str, Any] | None = None):
    return run("surveillance", qb.eq("collector_institution", collector_institution), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_contributing_institution(self, contributing_institution: str, options: Dict[str, Any] | None = None):
    return run("surveillance", qb.eq("contributing_institution", contributing_institution), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_contact_email_address(self, contact_email_address: str, options: Dict[str, Any] | None = None):
    return run("surveillance", qb.eq("contact_email_address", contact_email_address), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_project_identifier(self, project_identifier: str, options: Dict[str, Any] | None = None):
    return run("surveillance", qb.eq("project_identifier", project_identifier), options or {}, self._ctx["base_url"], self._ctx["headers"])

  # Pathogen-related methods
  def get_by_species(self, species: str, options: Dict[str, Any] | None = None):
    return run("surveillance", qb.eq("species", species), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_strain(self, strain: str, options: Dict[str, Any] | None = None):
    return run("surveillance", qb.eq("strain", strain), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_subtype(self, subtype: str, options: Dict[str, Any] | None = None):
    return run("surveillance", qb.eq("subtype", subtype), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_pathogen_type(self, pathogen_type: str, options: Dict[str, Any] | None = None):
    return run("surveillance", qb.eq("pathogen_type", pathogen_type), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_genome_id(self, genome_id: str, options: Dict[str, Any] | None = None):
    return run("surveillance", qb.eq("genome_id", genome_id), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_sequence_accession(self, sequence_accession: str, options: Dict[str, Any] | None = None):
    return run("surveillance", qb.eq("sequence_accession", sequence_accession), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_taxon_lineage_id(self, taxon_lineage_id: str, options: Dict[str, Any] | None = None):
    return run("surveillance", qb.eq("taxon_lineage_ids", taxon_lineage_id), options or {}, self._ctx["base_url"], self._ctx["headers"])

  # Disease-related methods
  def get_by_disease_status(self, disease_status: str, options: Dict[str, Any] | None = None):
    return run("surveillance", qb.eq("disease_status", disease_status), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_disease_severity(self, disease_severity: str, options: Dict[str, Any] | None = None):
    return run("surveillance", qb.eq("disease_severity", disease_severity), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_diagnosis(self, diagnosis: str, options: Dict[str, Any] | None = None):
    return run("surveillance", qb.eq("diagnosis", diagnosis), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_symptoms(self, symptoms: str, options: Dict[str, Any] | None = None):
    return run("surveillance", qb.eq("symptoms", symptoms), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_sudden_onset(self, sudden_onset: str, options: Dict[str, Any] | None = None):
    return run("surveillance", qb.eq("sudden_onset", sudden_onset), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_onset_hours(self, onset_hours: str, options: Dict[str, Any] | None = None):
    return run("surveillance", qb.eq("onset_hours", onset_hours), options or {}, self._ctx["base_url"], self._ctx["headers"])

  # Treatment-related methods
  def get_by_treatment(self, treatment: str, options: Dict[str, Any] | None = None):
    return run("surveillance", qb.eq("treatment", treatment), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_treatment_type(self, treatment_type: str, options: Dict[str, Any] | None = None):
    return run("surveillance", qb.eq("treatment_type", treatment_type), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_treatment_dosage(self, treatment_dosage: str, options: Dict[str, Any] | None = None):
    return run("surveillance", qb.eq("treatment_dosage", treatment_dosage), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_duration_of_treatment(self, duration_of_treatment: str, options: Dict[str, Any] | None = None):
    return run("surveillance", qb.eq("duration_of_treatment", duration_of_treatment), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_initiation_of_treatment(self, initiation_of_treatment: str, options: Dict[str, Any] | None = None):
    return run("surveillance", qb.eq("initiation_of_treatment", initiation_of_treatment), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_pre_visit_medications(self, pre_visit_medications: str, options: Dict[str, Any] | None = None):
    return run("surveillance", qb.eq("pre_visit_medications", pre_visit_medications), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_post_visit_medications(self, post_visit_medications: str, options: Dict[str, Any] | None = None):
    return run("surveillance", qb.eq("post_visit_medications", post_visit_medications), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_maintenance_medication(self, maintenance_medication: str, options: Dict[str, Any] | None = None):
    return run("surveillance", qb.eq("maintenance_medication", maintenance_medication), options or {}, self._ctx["base_url"], self._ctx["headers"])

  # Hospitalization-related methods
  def get_by_hospitalized(self, hospitalized: str, options: Dict[str, Any] | None = None):
    return run("surveillance", qb.eq("hospitalized", hospitalized), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_hospitalization_duration(self, hospitalization_duration: str, options: Dict[str, Any] | None = None):
    return run("surveillance", qb.eq("hospitalization_duration", hospitalization_duration), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_intensive_care_unit(self, intensive_care_unit: str, options: Dict[str, Any] | None = None):
    return run("surveillance", qb.eq("intensive_care_unit", intensive_care_unit), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_ecmo(self, ecmo: str, options: Dict[str, Any] | None = None):
    return run("surveillance", qb.eq("ecmo", ecmo), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_ventilation(self, ventilation: str, options: Dict[str, Any] | None = None):
    return run("surveillance", qb.eq("ventilation", ventilation), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_oxygen_saturation(self, oxygen_saturation: str, options: Dict[str, Any] | None = None):
    return run("surveillance", qb.eq("oxygen_saturation", oxygen_saturation), options or {}, self._ctx["base_url"], self._ctx["headers"])

  # Vaccination-related methods
  def get_by_vaccination_type(self, vaccination_type: str, options: Dict[str, Any] | None = None):
    return run("surveillance", qb.eq("vaccination_type", vaccination_type), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_vaccine_dosage(self, vaccine_dosage: str, options: Dict[str, Any] | None = None):
    return run("surveillance", qb.eq("vaccine_dosage", vaccine_dosage), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_vaccine_lot_number(self, vaccine_lot_number: str, options: Dict[str, Any] | None = None):
    return run("surveillance", qb.eq("vaccine_lot_number", vaccine_lot_number), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_vaccine_manufacturer(self, vaccine_manufacturer: str, options: Dict[str, Any] | None = None):
    return run("surveillance", qb.eq("vaccine_manufacturer", vaccine_manufacturer), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_days_elapsed_to_vaccination(self, days_elapsed_to_vaccination: str, options: Dict[str, Any] | None = None):
    return run("surveillance", qb.eq("days_elapsed_to_vaccination", days_elapsed_to_vaccination), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_source_of_vaccine_information(self, source_of_vaccine_information: str, options: Dict[str, Any] | None = None):
    return run("surveillance", qb.eq("source_of_vaccine_information", source_of_vaccine_information), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_other_vaccinations(self, other_vaccinations: str, options: Dict[str, Any] | None = None):
    return run("surveillance", qb.eq("other_vaccinations", other_vaccinations), options or {}, self._ctx["base_url"], self._ctx["headers"])

  # Exposure-related methods
  def get_by_exposure(self, exposure: str, options: Dict[str, Any] | None = None):
    return run("surveillance", qb.eq("exposure", exposure), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_exposure_type(self, exposure_type: str, options: Dict[str, Any] | None = None):
    return run("surveillance", qb.eq("exposure_type", exposure_type), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_duration_of_exposure(self, duration_of_exposure: str, options: Dict[str, Any] | None = None):
    return run("surveillance", qb.eq("duration_of_exposure", duration_of_exposure), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_use_of_personal_protective_equipment(self, use_of_personal_protective_equipment: str, options: Dict[str, Any] | None = None):
    return run("surveillance", qb.eq("use_of_personal_protective_equipment", use_of_personal_protective_equipment), options or {}, self._ctx["base_url"], self._ctx["headers"])

  # Lifestyle and health-related methods
  def get_by_tobacco_use(self, tobacco_use: str, options: Dict[str, Any] | None = None):
    return run("surveillance", qb.eq("tobacco_use", tobacco_use), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_packs_per_day_for_how_many_years(self, packs_per_day_for_how_many_years: str, options: Dict[str, Any] | None = None):
    return run("surveillance", qb.eq("packs_per_day_for_how_many_years", packs_per_day_for_how_many_years), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_alcohol_or_other_drug_dependence(self, alcohol_or_other_drug_dependence: str, options: Dict[str, Any] | None = None):
    return run("surveillance", qb.eq("alcohol_or_other_drug_dependence", alcohol_or_other_drug_dependence), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_breastfeeding(self, breastfeeding: str, options: Dict[str, Any] | None = None):
    return run("surveillance", qb.eq("breastfeeding", breastfeeding), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_pregnancy(self, pregnancy: str, options: Dict[str, Any] | None = None):
    return run("surveillance", qb.eq("pregnancy", pregnancy), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_trimester_of_pregnancy(self, trimester_of_pregnancy: str, options: Dict[str, Any] | None = None):
    return run("surveillance", qb.eq("trimester_of_pregnancy", trimester_of_pregnancy), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_daycare_attendance(self, daycare_attendance: str, options: Dict[str, Any] | None = None):
    return run("surveillance", qb.eq("daycare_attendance", daycare_attendance), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_nursing_home_residence(self, nursing_home_residence: str, options: Dict[str, Any] | None = None):
    return run("surveillance", qb.eq("nursing_home_residence", nursing_home_residence), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_primary_living_situation(self, primary_living_situation: str, options: Dict[str, Any] | None = None):
    return run("surveillance", qb.eq("primary_living_situation", primary_living_situation), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_education(self, education: str, options: Dict[str, Any] | None = None):
    return run("surveillance", qb.eq("education", education), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_profession(self, profession: str, options: Dict[str, Any] | None = None):
    return run("surveillance", qb.eq("profession", profession), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_chronic_conditions(self, chronic_conditions: str, options: Dict[str, Any] | None = None):
    return run("surveillance", qb.eq("chronic_conditions", chronic_conditions), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_infections_within_five_years(self, infections_within_five_years: str, options: Dict[str, Any] | None = None):
    return run("surveillance", qb.eq("infections_within_five_years", infections_within_five_years), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_influenza_like_illness_over_the_past_year(self, influenza_like_illness_over_the_past_year: str, options: Dict[str, Any] | None = None):
    return run("surveillance", qb.eq("influenza_like_illness_over_the_past_year", influenza_like_illness_over_the_past_year), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_types_of_allergies(self, types_of_allergies: str, options: Dict[str, Any] | None = None):
    return run("surveillance", qb.eq("types_of_allergies", types_of_allergies), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_dialysis(self, dialysis: str, options: Dict[str, Any] | None = None):
    return run("surveillance", qb.eq("dialysis", dialysis), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_human_leukocyte_antigens(self, human_leukocyte_antigens: str, options: Dict[str, Any] | None = None):
    return run("surveillance", qb.eq("human_leukocyte_antigens", human_leukocyte_antigens), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_longitudinal_study(self, longitudinal_study: str, options: Dict[str, Any] | None = None):
    return run("surveillance", qb.eq("longitudinal_study", longitudinal_study), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_travel_history(self, travel_history: str, options: Dict[str, Any] | None = None):
    return run("surveillance", qb.eq("travel_history", travel_history), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_geographic_group(self, geographic_group: str, options: Dict[str, Any] | None = None):
    return run("surveillance", qb.eq("geographic_group", geographic_group), options or {}, self._ctx["base_url"], self._ctx["headers"])

  # Test-related methods
  def get_by_pathogen_test_type(self, pathogen_test_type: str, options: Dict[str, Any] | None = None):
    return run("surveillance", qb.eq("pathogen_test_type", pathogen_test_type), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_pathogen_test_result(self, pathogen_test_result: str, options: Dict[str, Any] | None = None):
    return run("surveillance", qb.eq("pathogen_test_result", pathogen_test_result), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_pathogen_test_interpretation(self, pathogen_test_interpretation: str, options: Dict[str, Any] | None = None):
    return run("surveillance", qb.eq("pathogen_test_interpretation", pathogen_test_interpretation), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_chest_imaging_interpretation(self, chest_imaging_interpretation: str, options: Dict[str, Any] | None = None):
    return run("surveillance", qb.eq("chest_imaging_interpretation", chest_imaging_interpretation), options or {}, self._ctx["base_url"], self._ctx["headers"])

  # Date range methods
  def get_by_collection_date_range(self, start_date: str, end_date: str, options: Dict[str, Any] | None = None):
    filters = [qb.gt("collection_date", start_date), qb.lt("collection_date", end_date)]
    return run("surveillance", qb.and_(*filters), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_submission_date_range(self, start_date: str, end_date: str, options: Dict[str, Any] | None = None):
    filters = [qb.gt("submission_date", start_date), qb.lt("submission_date", end_date)]
    return run("surveillance", qb.and_(*filters), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_last_update_date_range(self, start_date: str, end_date: str, options: Dict[str, Any] | None = None):
    filters = [qb.gt("last_update_date", start_date), qb.lt("last_update_date", end_date)]
    return run("surveillance", qb.and_(*filters), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_embargo_end_date_range(self, start_date: str, end_date: str, options: Dict[str, Any] | None = None):
    filters = [qb.gt("embargo_end_date", start_date), qb.lt("embargo_end_date", end_date)]
    return run("surveillance", qb.and_(*filters), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_date_inserted_range(self, start_date: str, end_date: str, options: Dict[str, Any] | None = None):
    filters = [qb.gt("date_inserted", start_date), qb.lt("date_inserted", end_date)]
    return run("surveillance", qb.and_(*filters), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_date_modified_range(self, start_date: str, end_date: str, options: Dict[str, Any] | None = None):
    filters = [qb.gt("date_modified", start_date), qb.lt("date_modified", end_date)]
    return run("surveillance", qb.and_(*filters), options or {}, self._ctx["base_url"], self._ctx["headers"])

  # Location range methods
  def get_by_collection_latitude_range(self, min_lat: float, max_lat: float, options: Dict[str, Any] | None = None):
    filters = [qb.gt("collection_latitude", min_lat), qb.lt("collection_latitude", max_lat)]
    return run("surveillance", qb.and_(*filters), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_collection_longitude_range(self, min_lon: float, max_lon: float, options: Dict[str, Any] | None = None):
    filters = [qb.gt("collection_longitude", min_lon), qb.lt("collection_longitude", max_lon)]
    return run("surveillance", qb.and_(*filters), options or {}, self._ctx["base_url"], self._ctx["headers"])

  # Time-related methods
  def get_by_days_elapsed_to_disease_status(self, days_elapsed_to_disease_status: str, options: Dict[str, Any] | None = None):
    return run("surveillance", qb.eq("days_elapsed_to_disease_status", days_elapsed_to_disease_status), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_days_elapsed_to_sample_collection(self, days_elapsed_to_sample_collection: str, options: Dict[str, Any] | None = None):
    return run("surveillance", qb.eq("days_elapsed_to_sample_collection", days_elapsed_to_sample_collection), options or {}, self._ctx["base_url"], self._ctx["headers"])

  # Metadata methods
  def get_by_additional_metadata(self, additional_metadata: str, options: Dict[str, Any] | None = None):
    return run("surveillance", qb.eq("additional_metadata", additional_metadata), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_comments(self, comments: str, options: Dict[str, Any] | None = None):
    return run("surveillance", qb.eq("comments", comments), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_by_collector_name(self, collector_name: str, options: Dict[str, Any] | None = None):
    return run("surveillance", qb.eq("collector_name", collector_name), options or {}, self._ctx["base_url"], self._ctx["headers"])

  def search_by_keyword(self, keyword: str, options: Dict[str, Any] | None = None):
    return run("surveillance", f"keyword({quote(keyword)})", options or {}, self._ctx["base_url"], self._ctx["headers"])

  def get_all(self, options: Dict[str, Any] | None = None):
    return run("surveillance", "", options or {}, self._ctx["base_url"], self._ctx["headers"])

  # Solr cursor-based streaming (Option B implementation)
  def stream_all_solr(
    self,
    *,
    rows: int = 1000,
    sort: str | None = None,
    unique_key: str | None = "id",
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
      collection="surveillance",
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


__all__ = ["Surveillance"]
