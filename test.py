# Copyright (c) 2010 Friedrich Romstedt <www.friedrichromstedt.org>
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

# Last changed: 2010 Mar 13
# Developed since: Mar 2010
# File version: 0.1.1b

__version__ = (0, 1, 1)

import keyconf
import unittest


class Test(unittest.TestCase):
	def test(self):
		component = keyconf.Configuration()

		# Configure a key.
		component.configure(leaf = 'green')
		self.assert_(component['leaf'] == 'green')
		self.assert_(component == {'leaf': 'green'})

		# Create the top Configuration.
		top = keyconf.Configuration(sub = component)

		# The component is hidden.
		self.assert_(top == {})

		# Configure ordinary keys in {top}.
		top.configure(stem = 'brown')
		self.assert_(top == {'stem': 'brown'})

		self.assert_(top.is_configured('sub_leaf'))
		self.assert_(top.is_configured('stem'))
		self.assert_(not top.is_configured('sub_none'))
		self.assert_(not top.is_configured('none'))

		# Configure {component} by calls to {top}.
		top.configure(sub_leaf = 'yellow')
		self.assert_(component == {'leaf': 'yellow'})
		self.assert_(top == {'stem': 'brown'})

		# Configure the leaf again, but leave the value unchanged.
		component.configure(leaf = None)
		self.assert_(component == {'leaf': 'yellow'})

		# Configure another key.
		component.configure(ill = 'faint green')
		self.assert_(component == {'leaf': 'yellow', 'ill': 'faint green'})

		# Delete the second key.
		top.unconfigure('sub_ill')
		self.assert_(component == {'leaf': 'yellow'})

		top.set_aliases(alias = 'sub_leaf')
		self.assert_(top.get_config('alias') == 'yellow')

		top.unset_aliases('alias')
		self.assert_(not top.is_configured('alias'))

		# Test passed.

if __name__ == '__main__':
	unittest.main()
