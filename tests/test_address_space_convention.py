import json
import tomllib
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class B32KAddressSpaceConventionTests(unittest.TestCase):
    def load(self):
        return json.loads((ROOT / 'artifacts/json/b32k_address_space_convention_001.json').read_text())

    def test_successor_boundary(self):
        c = self.load()['successor_convention']
        self.assertIsNone(c['actual_null']['catalogue_address'])
        self.assertEqual(c['registered_null']['catalogue_address'], 1)
        self.assertEqual(c['registered_null']['registered_index'], 0)
        self.assertEqual(c['b32k_bootloader']['catalogue_address'], 2)
        self.assertEqual(c['b32k_bootloader']['registered_index'], 1)
        self.assertEqual(c['organization_root']['catalogue_address'], 3)
        self.assertEqual(c['organization_root']['registered_index'], 2)
        self.assertEqual(c['ordinary_allocatable_positions']['catalogue_address_minimum'], 4)
        self.assertEqual(c['ordinary_allocatable_positions']['position_count'], 32765)

    def test_finite_entry_points_not_descendants(self):
        c = self.load()
        self.assertEqual(c['finite_catalogue']['registered_position_count'], 32768)
        self.assertTrue(c['lane_context_model']['registered_positions_are_entry_points'])
        self.assertTrue(c['lane_context_model']['finite_catalogue_exhausts_entry_points_not_objects'])
        self.assertTrue(c['lane_context_model']['lanes_or_contexts_may_be_unbounded'])
        self.assertFalse(c['nonclaims']['addressability_confers_authority'])
        self.assertFalse(c['nonclaims']['unsigned_addressability_confers_trust'])

    def test_version_bump(self):
        data = tomllib.loads((ROOT / 'pyproject.toml').read_text())
        self.assertEqual(data['project']['version'], '0.5.1')

if __name__ == '__main__':
    unittest.main()
