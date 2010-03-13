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

"""A module providing a framework for configuration of components using 
arguments to a top-level function."""


class Configuration(dict):
	"""Holds a number of parameters.  Read-only attributes:
		
	.components - A dictionary {name: Configuration}."""

	def __init__(self, **components):
		"""An Configuration may contain sub-Configurations **COMPONENTS.  To 
		use this, do:

		1. Create the component-Configuration {sub}.

		2. To add the component under name {name}, create *this* Configuration 
				with arguments {name} = {sub}.

		3. Calls to .configure() will forward kwargs starting with 
				{name} + '_' will be forwarded to {sub}.configure() with 
				name + '_' stripped."""
		
		dict.__init__(self)

		self.components = components
	
	def add_components(self, **components):
		"""Add components **COMPONENTS."""

		self.components.update(components)

	def remove_components(self, *names):
		"""Removes components *NAMES.  Fails if the given components do not
		exist."""
		
		for name in names:
			del self.components[name]

	def configure(self, **kwargs):
		"""Update the Configuration and its components with all kwargs given.  
		Arguments given with value None will be left unchanged."""

		# Iterate through the kwarguments ...

		for (key, value) in kwargs.items():
			# Try to forward the argument.
			forwarded = False
			for (name, component) in self.components.items():
				prefix = name + '_'
				if key.startswith(prefix):
					# Forward the argument:
					key_stripped = key.replace(prefix, '', 1)
					component.configure(**{key_stripped: value})
					forwarded = True
					break

			if not forwarded:
				# The argument hasn't been forwarded.
				if value is not None:
					self[key] = value

	def unconfigure(self, *args):
		"""Delete the args given from the dictionary.  If they do not exist,
		they will be silently ignored."""

		for key in args:
			# Try to forward the argument.
			forwarded = False
			for (name, component) in self.components.items():
				prefix = name + '_'
				if key.startswith(prefix):
					# Forward the argument:
					key_stripped = key.replace(prefix, '', 1)
					component.unconfigure(key_stripped)
					forwarded = True
					break

			if not forwarded:
				# The argument hasn't been forwarded.
				if key in self:
					del self[key]
