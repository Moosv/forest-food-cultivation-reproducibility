"""Synthetic-only tests. No research records are included in this repository."""
from copy import deepcopy
import tempfile
from pathlib import Path
import unittest
from analysis import (PUBLICATIONS, FOREST, CROPS, SELECTION, AGGREGATES,
                      normalize_and_validate, aggregate, compare_recorded_aggregates,
                      boolean, string_list, new_output_dir)


def synthetic_data():
    pubs = [dict(work_id="SYNTHETIC_A", pub_year=2000, research_focus_codes='["T1","T2"]',
                 focus_or_core_codes='["T1","T2"]', in_forestfood="true", in_food_linked="true"),
            dict(work_id="SYNTHETIC_B", pub_year=2025, research_focus_codes='["T1","OT"]',
                 focus_or_core_codes='["T1","OT"]', in_forestfood="false", in_food_linked="true")]
    crops = [dict(target_id="SYNTHETIC_LINK_1", work_id="SYNTHETIC_A", pub_year=2000,
                  target_role="direct_experiment", direct_experiment="true", analysis_stratum="forest_named",
                  crop_group="SYNTHETIC_CROP_1", production_stages='["seedling"]'),
             dict(target_id="SYNTHETIC_LINK_2", work_id="SYNTHETIC_A", pub_year=2000,
                  target_role="direct_experiment", direct_experiment="true", analysis_stratum="forest_named",
                  crop_group="SYNTHETIC_CROP_2", production_stages='["seedling","growth_harvest"]'),
             dict(target_id="SYNTHETIC_LINK_3", work_id="SYNTHETIC_B", pub_year=2025,
                  target_role="direct_experiment", direct_experiment="true", analysis_stratum="common_food_crop",
                  crop_group="SYNTHETIC_CROP_3", production_stages='["growth_harvest"]')]
    selection = [dict(work_id=r["work_id"], pub_year=r["pub_year"], current_disposition="included",
                      selection_basis_recorded="Synthetic fixture, not research evidence") for r in pubs]
    selection.extend(dict(work_id=f"SYNTHETIC_{state}", pub_year=2005, current_disposition=state,
                          selection_basis_recorded="Synthetic fixture") for state in ("excluded", "held"))
    return {PUBLICATIONS: pubs, FOREST: [dict(work_id="SYNTHETIC_A", pub_year=2000,
                                             facility_inclusion_basis="Synthetic fixture")],
            CROPS: crops, SELECTION: selection, AGGREGATES: []}


class AnalysisTests(unittest.TestCase):
    def test_unique_work_ids_across_crops_and_stages(self):
        data = normalize_and_validate(synthetic_data(), check_snapshot=False)
        result = aggregate(data)
        counts = {r["stage"]: r["n"] for r in result["selection_counts.csv"]}
        self.assertEqual(counts["forestfood"], 1)
        self.assertEqual(counts["food_linked"], 2)
        stages = {r["stage"]: r["n"] for r in result["forest_production_stages.csv"]}
        self.assertEqual(stages["seedling"], 1)

    def test_period_boundaries_and_multiple_technology_codes(self):
        result = aggregate(normalize_and_validate(synthetic_data(), False))
        tech = {r["code"]: r for r in result["technology_counts.csv"]}
        self.assertEqual(tech["T1"]["percent"], 100.0)
        self.assertEqual(tech["T2"]["percent"], 50.0)
        self.assertNotIn("OT", tech)
        annual = {r["year"]: r["n"] for r in result["annual_counts.csv"]}
        self.assertEqual(annual[2000], 1)
        self.assertEqual(annual[2025], 1)
        self.assertEqual(annual[2001], 0)
        empty = [r for r in result["period_technology.csv"] if r["period"] == "2005–2009"]
        self.assertTrue(all(r["percent"] is None for r in empty))

    def test_rounding(self):
        data = synthetic_data()
        row = deepcopy(data[PUBLICATIONS][1])
        row.update(work_id="SYNTHETIC_C", research_focus_codes='["T2"]',
                   focus_or_core_codes='["T2"]', in_food_linked="false")
        data[PUBLICATIONS].append(row)
        data[SELECTION].append(dict(work_id="SYNTHETIC_C", pub_year=2025,
                                    current_disposition="included", selection_basis_recorded="Synthetic"))
        rows = aggregate(normalize_and_validate(data, False))["technology_counts.csv"]
        self.assertEqual(rows[0]["percent"], 66.7)

    def test_duplicate_publication(self):
        data = synthetic_data()
        data[PUBLICATIONS].append(deepcopy(data[PUBLICATIONS][0]))
        with self.assertRaisesRegex(ValueError, "Duplicate work_id"):
            normalize_and_validate(data, False)

    def test_invalid_year_and_included_membership(self):
        for year in (1999, 2026):
            data = synthetic_data()
            data[PUBLICATIONS][0]["pub_year"] = year
            with self.assertRaisesRegex(ValueError, "Out-of-period"):
                normalize_and_validate(data, False)
        data = synthetic_data()
        data[SELECTION][0]["current_disposition"] = "excluded"
        with self.assertRaisesRegex(ValueError, "Included selection IDs"):
            normalize_and_validate(data, False)

    def test_orphan_crop_and_flag_mismatch(self):
        data = synthetic_data()
        data[CROPS][0]["work_id"] = "SYNTHETIC_MISSING"
        with self.assertRaisesRegex(ValueError, "Orphan"):
            normalize_and_validate(data, False)
        data = synthetic_data()
        data[PUBLICATIONS][0]["in_forestfood"] = "false"
        with self.assertRaisesRegex(ValueError, "Forest flags"):
            normalize_and_validate(data, False)

    def test_no_blank_or_unrecognized_codes(self):
        for value in ("", "yes", 0, None):
            with self.assertRaises(ValueError):
                boolean(value)
        for value in ('["T1","T1"]', "null", '"T1"'):
            with self.assertRaises(ValueError):
                string_list(value)
        data = synthetic_data()
        data[PUBLICATIONS][0]["research_focus_codes"] = '["T9"]'
        with self.assertRaisesRegex(ValueError, "Unknown technology"):
            normalize_and_validate(data, False)

    def test_snapshot_guard(self):
        with self.assertRaisesRegex(ValueError, "Different analysis snapshot"):
            normalize_and_validate(synthetic_data())

    def test_duplicate_aggregate_rejected(self):
        data = synthetic_data()
        row = dict(source_table="annual_counts.csv", year=2000, n=1)
        data[AGGREGATES] = [row, deepcopy(row)]
        with self.assertRaisesRegex(ValueError, "Duplicate aggregate key"):
            compare_recorded_aggregates(data, {})

    def test_existing_output_protected(self):
        with tempfile.TemporaryDirectory() as temp:
            with self.assertRaisesRegex(ValueError, "already exists"):
                new_output_dir(Path(temp))


if __name__ == "__main__":
    unittest.main()
