# Copyright (C) 2018 The NeoVintageous Team (NeoVintageous).
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
# along with NeoVintageous.  If not, see <https://www.gnu.org/licenses/>.

from unittest import mock  # noqa: F401
from unittest import skipIf  # noqa: F401
from unittest import TestCase  # noqa: F401
import unittest

# Use aliases to indicate that they are not public testing APIs.
from sublime import active_window as _active_window
from sublime import Region

# Use aliases to indicate that they are not public testing APIs.
from NeoVintageous.nv.state import State as _State

from NeoVintageous.nv.vim import COMMAND_LINE  # noqa: F401
from NeoVintageous.nv.vim import CTRL_X  # noqa: F401
from NeoVintageous.nv.vim import INSERT  # noqa: F401
from NeoVintageous.nv.vim import INTERNAL_NORMAL  # noqa: F401
from NeoVintageous.nv.vim import NORMAL  # noqa: F401
from NeoVintageous.nv.vim import NORMAL_INSERT  # noqa: F401
from NeoVintageous.nv.vim import OPERATOR_PENDING  # noqa: F401
from NeoVintageous.nv.vim import REPLACE  # noqa: F401
from NeoVintageous.nv.vim import SELECT  # noqa: F401
from NeoVintageous.nv.vim import UNKNOWN  # noqa: F401
from NeoVintageous.nv.vim import VISUAL  # noqa: F401
from NeoVintageous.nv.vim import VISUAL_BLOCK  # noqa: F401
from NeoVintageous.nv.vim import VISUAL_LINE  # noqa: F401


# DEPRECATED Use newer APIs.
def _make_region(view, a, b=None):
    # type: (...) -> Region
    try:
        pt_a = view.text_point(*a)
        pt_b = view.text_point(*b)

        return Region(pt_a, pt_b)
    except (TypeError, ValueError):
        pass

    if isinstance(a, int) and b is None:
        pass
    elif not (isinstance(a, int) and isinstance(b, int)):
        raise ValueError('a and b arguments must be integers or a tuple (row, col)')

    if b is not None:
        return Region(a, b)
    else:
        return Region(a)


class ViewTestCase(unittest.TestCase):

    def setUp(self):
        self.view = _active_window().new_file()

    def tearDown(self):
        if self.view:
            self.view.set_scratch(True)
            self.view.close()

    def content(self):
        # type: () -> str
        return self.view.substr(Region(0, self.view.size()))

    def Region(self, a, b=None):
        # Return a Region with initial values a and b.
        #
        # This method can save having to import `sublime.Region` into test
        # modules.
        #
        # Args:
        #   a (int): The first end of the region.
        #   b (int, optional): The second end of the region. Defaults to the
        #       same as the a end of the region. May be less that a, in
        #       which case the region is a reversed one.
        return Region(a, b)

    def select(self, selections):
        # Create selection in the view.
        #
        # Args:
        #   selections (int|tuple|Region|list<int|tuple|Region>)
        #
        # Existing selections are cleared.
        #
        # Integers and tuples are converted to Regions:
        # >>> select(3) is the short for: select(sublime.Region(3))
        # >>> select((3, 5)) is short for: select(sublime.Region(3, 5))
        #
        # Select a single point:
        # >>> select(3)
        #
        # Select a region of text e.g. from point 3 to 5:
        # >>> select((3, 5))
        #
        # Select multiple point selections:
        # >>> select([3, 5, 7])
        #
        # Select multiple text selections:
        # >>> select([(3, 5), (7, 11)])
        #
        # Select multiple points, and text selections:
        # >>> select([3, 5, (7, 11), 17, (19, 23)])

        self.view.sel().clear()

        if not isinstance(selections, list):
            selections = [selections]

        for selection in selections:
            if isinstance(selection, tuple):
                self.view.sel().add(Region(selection[0], selection[1]))
            else:
                self.view.sel().add(selection)

    def settings(self):
        return self.view.settings()

    def write(self, text):
        # type: (str) -> None
        self.view.run_command('_nv_test_write', {'text': text})

    def assertContent(self, expected, msg=None):
        # Test that view contents and *expected* are equal.
        #
        # Args:
        #   expected (str): Expected view contents.
        #   msg (str, optional): If specified, is used as the error message on
        #       failure.
        self.assertEqual(self.content(), expected, msg)

    def assertContentRegex(self, expected, msg=None):
        # Test that view contents matches (or does not match) *expected*.
        #
        # Args:
        #   expected (str): Expected regular expression that should match view
        #       contents.
        #   msg (str, optional): If specified, is used as the error message on
        #       failure.
        self.assertRegex(self.content(), expected, msg)

    def assertNormalMode(self):
        self.assertEquals(self.state.mode, NORMAL)

    def assertRegion(self, expected, actual):
        # Test that *actual* and *expected* are equal.
        #
        # Args:
        #   expected (str|int|tuple|Region): If the expected value is a str,
        #       int, or a tuple, it will be converted to a Region before
        #       evaluating against the actual value.
        #   actual (Region): Actual region.
        if isinstance(expected, str):
            self.assertEqual(expected, self.view.substr(actual))
        elif isinstance(expected, int):
            self.assertEqual(Region(expected), actual)
        elif isinstance(expected, tuple):
            self.assertEqual(Region(expected[0], expected[1]), actual)
        else:
            self.assertEqual(expected, actual)

    def assertSelection(self, expected):
        # Test that view selection and *expected* are equal.
        #
        # Args:
        #   expected (int|tuple|Region|list<Region>):
        #
        # Integers and tuples are converted to Regions:
        # >>> assertSelection(3) is the short for: assertSelection(sublime.Region(3))
        # >>> assertSelection((3, 5)) is short for: assertSelection(sublime.Region(3, 5))
        #
        # Assert that the view has one point selection:
        # >>> self.assertSelection(3)
        #
        # Assert that the view has multiple point selections:
        # >>> self.assertSelection([3, 5, 7])
        #
        # Assert that the view has a text area selection:
        # >>> self.assertSelection((3, 5))
        #
        # Assert that the view has multiple text selections:
        # >>> self.assertSelection([(3, 5), (7, 9))
        #
        # Assert that the view has multiple points, and text selections:
        # >>> self.assertSelection([3, 5, (7, 11)])

        if isinstance(expected, int):
            self.assertEqual([Region(expected)], list(self.view.sel()))
        elif isinstance(expected, tuple):
            self.assertEqual([Region(expected[0], expected[1])], list(self.view.sel()))
        elif isinstance(expected, Region):
            self.assertEqual([expected], list(self.view.sel()))
        else:
            # Defaults to expect a list of Regions.
            self.assertEqual(expected, list(self.view.sel()))

    def assertSelectionCount(self, expected):
        # Test that view selection count and *expected* are equal.
        #
        # Args:
        #   expected (int): Expected number of selections in view.
        self.assertEqual(expected, len(self.view.sel()))

    def assertSize(self, expected):
        # Test that number of view characters and *expected* are equal.
        #
        # Args:
        #   expected (int): Expected number of characters in view.
        self.assertEqual(expected, self.view.size())

    # DEPRECATED Try to avoid using this, it will eventually be removed in favour of something better.
    @property
    def state(self):
        return _State(self.view)

    # DEPRECATED Use newer APIs e.g. self.Region(), unittest.Region.
    def _R(self, a, b=None):
        return _make_region(self.view, a, b)

    # DEPRECATED Use newer APIs e.g. assertRegion(), assertSelection(), and assertContent().
    def _assertRegionsEqual(self, expected_region, actual_region, msg=None):
        # Test that regions covers the exact same region. Does not take region
        # orientation into account.
        if (expected_region.size() == 1) and (actual_region.size() == 1):
            expected_region = _make_region(self.view, expected_region.begin(),
                                           expected_region.end())
            actual_region = _make_region(self.view, actual_region.begin(),
                                         actual_region.end())

        self.assertEqual(expected_region, actual_region, msg)
