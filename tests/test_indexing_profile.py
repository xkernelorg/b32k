import csv
import json
import sys
import unittest
from pathlib import Path


PROJECT = Path(__file__).resolve().parents[1]
SRC = PROJECT / "src"

if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from b32k.codec import load_b32k_alphabet


class B32KIndexingProfileTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.profile = json.loads(
            (
                PROJECT
                / "artifacts/json/"
                "b32k_indexing_profile_001.json"
            ).read_text(encoding="utf-8")
        )
        cls.canon = json.loads(
            (
                PROJECT / "src/b32k/b32k.json"
            ).read_text(encoding="utf-8")
        )
        cls.aletheos = json.loads(
            (
                PROJECT
                / "artifacts/json/"
                "b32k_aletheos_canonical_index_001.json"
            ).read_text(encoding="utf-8")
        )

        with (
            PROJECT
            / "artifacts/csv/"
            "b32k_canonical_alphabet.csv"
        ).open(encoding="utf-8", newline="") as stream:
            cls.csv_rows = list(csv.DictReader(stream))

    def test_catalogue_is_complete_one_based(self):
        indices = [
            int(row["index"]) for row in self.csv_rows
        ]
        self.assertEqual(indices, list(range(1, 32769)))

    def test_csv_matches_canonical_json(self):
        json_rows = self.canon["alphabet"]["rows"]
        anchors = self.canon["anchors"]

        self.assertEqual(len(self.csv_rows), len(json_rows))

        for csv_row, json_row in zip(
            self.csv_rows,
            json_rows,
        ):
            self.assertEqual(
                int(csv_row["index"]),
                json_row["index"],
            )
            self.assertEqual(
                csv_row["unicode_point"],
                json_row["unicode_point"],
            )
            self.assertEqual(
                csv_row["anchor_domain"],
                json_row["anchor_id"],
            )
            self.assertEqual(
                csv_row["anchor_label"],
                anchors[json_row["anchor_id"]]["label"],
            )

    def test_mapping_is_bijective(self):
        for catalogue_address in range(1, 32769):
            wire_index = catalogue_address - 1
            self.assertGreaterEqual(wire_index, 0)
            self.assertLessEqual(wire_index, 32767)
            self.assertEqual(
                wire_index + 1,
                catalogue_address,
            )

    def test_registered_null_boundary(self):
        boundary = self.profile["reserved_boundary"]

        self.assertEqual(boundary["catalogue_address"], 1)
        self.assertEqual(boundary["wire_index"], 0)
        self.assertEqual(boundary["lane_index"], 0)
        self.assertEqual(boundary["key"], "NULL_WELL")
        self.assertFalse(
            self.profile["invariants"][
                "registered_null_has_positive_authority"
            ]
        )

        null_rows = [
            row for row in self.aletheos["entries"]
            if row.get("lane") == "b32k.aletheos.bound.v1"
            and row.get("index") == 0
        ]

        self.assertEqual(len(null_rows), 1)
        self.assertEqual(null_rows[0]["key"], "NULL_WELL")
        self.assertFalse(null_rows[0]["positive_authority"])

    def test_aletheos_root_boundary(self):
        root = self.profile["aletheos_root"]

        self.assertEqual(root["catalogue_address"], 2)
        self.assertEqual(root["wire_index"], 1)
        self.assertEqual(root["lane_index"], 1)
        self.assertEqual(root["key"], "ALETHEOS_ROOT")

        root_rows = [
            row for row in self.aletheos["entries"]
            if row.get("lane") == "b32k.aletheos.bound.v1"
            and row.get("index") == 1
        ]

        self.assertEqual(len(root_rows), 1)
        self.assertEqual(
            root_rows[0]["key"],
            "ALETHEOS_ROOT",
        )

    def test_codec_positions_are_wire_indices(self):
        symbols, reverse = load_b32k_alphabet()

        self.assertEqual(len(symbols), 32768)
        self.assertEqual(symbols[0], chr(1))
        self.assertEqual(symbols[-1], chr(0x8000))
        self.assertEqual(reverse[symbols[0]], 0)
        self.assertEqual(reverse[symbols[-1]], 32767)


    def test_explicit_codec_coordinate_helpers(self):
        from b32k.codec import (
            CATALOGUE_ADDRESS_MAX,
            CATALOGUE_ADDRESS_MIN,
            WIRE_INDEX_MAX,
            WIRE_INDEX_MIN,
            catalogue_address_to_wire_index,
            wire_index_to_catalogue_address,
        )

        self.assertEqual(CATALOGUE_ADDRESS_MIN, 1)
        self.assertEqual(CATALOGUE_ADDRESS_MAX, 32768)
        self.assertEqual(WIRE_INDEX_MIN, 0)
        self.assertEqual(WIRE_INDEX_MAX, 32767)

        self.assertEqual(
            catalogue_address_to_wire_index(1),
            0,
        )
        self.assertEqual(
            catalogue_address_to_wire_index(32768),
            32767,
        )
        self.assertEqual(
            wire_index_to_catalogue_address(0),
            1,
        )
        self.assertEqual(
            wire_index_to_catalogue_address(32767),
            32768,
        )

    def test_codec_coordinate_helpers_fail_closed(self):
        from b32k.codec import (
            catalogue_address_to_wire_index,
            wire_index_to_catalogue_address,
        )

        for value in [0, -1, 32769, True, "1", None]:
            with self.assertRaises(ValueError):
                catalogue_address_to_wire_index(value)

        for value in [-1, 32768, True, "0", None]:
            with self.assertRaises(ValueError):
                wire_index_to_catalogue_address(value)

    def test_all_coordinate_round_trips(self):
        from b32k.codec import (
            catalogue_address_to_wire_index,
            wire_index_to_catalogue_address,
        )

        for address in range(1, 32769):
            wire_index = catalogue_address_to_wire_index(
                address
            )
            self.assertEqual(
                wire_index_to_catalogue_address(wire_index),
                address,
            )


    def test_public_package_exports_index_contract(self):
        import b32k

        self.assertEqual(b32k.CATALOGUE_ADDRESS_MIN, 1)
        self.assertEqual(b32k.CATALOGUE_ADDRESS_MAX, 32768)
        self.assertEqual(b32k.WIRE_INDEX_MIN, 0)
        self.assertEqual(b32k.WIRE_INDEX_MAX, 32767)
        self.assertEqual(b32k.WIRE_INDEX_BITS, 15)
        self.assertEqual(
            b32k.catalogue_address_to_wire_index(1),
            0,
        )
        self.assertEqual(
            b32k.wire_index_to_catalogue_address(32767),
            32768,
        )


if __name__ == "__main__":
    unittest.main()
