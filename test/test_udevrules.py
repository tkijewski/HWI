#! /usr/bin/env python3

import unittest
import json
import filecmp
from os import makedirs, remove, removedirs, walk, path 
from hwilib.cli import process_commands

class TestUdevRulesInstaller(unittest.TestCase):
    INSTALLATION_FOLDER = 'rules.d'
    SOURCE_FOLDER = '../hwilib/udev'

    @classmethod
    def setUpClass(cls):
        # Create directory where copy the udev rules to.
        makedirs(cls.INSTALLATION_FOLDER, exist_ok=True)

    @classmethod
    def tearDownClass(self):
        for root, dirs, files in walk(self.INSTALLATION_FOLDER, topdown=False):
            for name in files:
                remove(path.join(root, name))
        removedirs(self.INSTALLATION_FOLDER)

    def test_rules_file_are_copied(self):
        result = process_commands( ['installudevrules', '--location', self.INSTALLATION_FOLDER])
        self.assertIn('error', result)
        self.assertIn('code', result)
        self.assertEqual(result['error'], 'Need to be root.')
        self.assertEqual(result['code'], -16)
        # Assert files wre copied
        for root, dirs, files in walk(self.INSTALLATION_FOLDER, topdown=False):
            for file_name in files:
                src = path.join(self.SOURCE_FOLDER, file_name)
                tgt = path.join(self.INSTALLATION_FOLDER, file_name)
                self.assertTrue(filecmp.cmp(src, tgt))

if __name__ == "__main__":
    unittest.main()
