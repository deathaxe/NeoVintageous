# Copyright (C) 2018-2023 The NeoVintageous Team (NeoVintageous).
#
# This file is part of NeoVintageous.
#
# NeoVintageous is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# NeoVintageous is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License

from NeoVintageous.tests import unittest

from NeoVintageous.nv.vi.text_objects import big_word_end


class Test_big_word_end(unittest.ViewTestCase):

    def test_basic(self):
        self.write('xyz x._a1     xx')

        self.assertEqual(3, big_word_end(self.view, 0))
        self.assertEqual(3, big_word_end(self.view, 1))
        self.assertEqual(3, big_word_end(self.view, 2))
        self.assertEqual(3, big_word_end(self.view, 3))

        self.assertEqual(9, big_word_end(self.view, 4))
        self.assertEqual(9, big_word_end(self.view, 5))
        self.assertEqual(9, big_word_end(self.view, 6))
        self.assertEqual(9, big_word_end(self.view, 7))
        self.assertEqual(9, big_word_end(self.view, 8))
        self.assertEqual(9, big_word_end(self.view, 9))

        self.assertEqual(10, big_word_end(self.view, 10))
        self.assertEqual(11, big_word_end(self.view, 11))
        self.assertEqual(12, big_word_end(self.view, 12))
        self.assertEqual(13, big_word_end(self.view, 13))

        self.assertEqual(16, big_word_end(self.view, 14))
        self.assertEqual(16, big_word_end(self.view, 15))
