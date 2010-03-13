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
# File version: 0.3.0b

__version__ = (0, 3, 0)

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

		# The list of sub-Configurations.
		self.components = components

		# The list of direct key replacements.
		#
		# Aliases are not forwarded.
		self.aliases = {}
	
	#
	# Component methods ...
	#

	def add_components(self, **components):
		"""Add components **COMPONENTS = {name: component}."""

		self.components.update(components)

	def remove_components(self, *names):
		"""Removes components *NAMES.  Fails if the given components do not
		exist."""
		
		for name in names:
			del self.components[name]

	#
	# Alias methods ...
	#

	def set_aliases(self, **aliases):
		"""Set aliases ALIASES = {alias: target key}."""

		for (alias, target_key) in aliases.items():
			self.aliases[alias] = target_key

	def unset_aliases(self, *aliases):
		"""Delete aliases ALIASES.  Nonexistent aliases fail."""

		for alias in aliases:
			del self.aliases[alias]
		
	#
	# Key methods ...
	#

	def _get_target(self, key):
		"""Returns (key_target, key_component) for the key KEY.  Tries to
		forward KEY to some component.  If the KEY cannot be forwarded, the
		tuple (key, self) will be returned.  Also resolves aliases."""

		# First, search the aliases ...

		for (alias, target_key) in self.aliases.items():
			if key == alias:
				key = target_key

		# Second, try to forward the de-aliased key ...

		for (name, component) in self.components.items():
			prefix = name + '_'
			if key.startswith(prefix):
				# Forward the argument.
				key_stripped = key.replace(prefix, '', 1)
				return (key_stripped, component)

		# The key could not be forwarded ...

		return (key, self)
	
	# Config methods.

	def _configure(self, key, value):
		"""Called to actually *set* a key."""

		if value is not None:
			self[key] = value

	def configure(self, **kwargs):
		"""Update the Configuration and its components with all kwargs given.  
		Arguments given with value None will be left unchanged."""

		# Iterate through the kwarguments ...

		for (key, value) in kwargs.items():
			# Find the target.
			(key_target, target) = self._get_target(key)
			
			if target is self:
				self._configure(key_target, value)
			else:
				target.configure(**{key_target: value})
	
	# Unconfig methods.

	def _unconfigure(self, key):
		"""Called to actually *unset* a key."""

		if key in self:
			del self[key]

	def unconfigure(self, *args):
		"""Delete the args given from the dictionary.  If they do not exist,
		they will be silently ignored."""

		for key in args:
			# Find the target.
			(key_target, target) = self._get_target(key)

			if target is self:
				self._unconfigure(key_target)
			else:
				target.unconfigure(key_target)

	# Config retrieval methods.

	def _get_config(self, key):
		"""Called to actually *retrieve* a key's configuration."""

		return self[key]

	def get_config(self, key):
		"""Retrieve the Configuration's key KEY.  If the KEY doesn't exist,
		the call will raise KeyError."""

		# Find the target.
		(key_target, target) = self._get_target(key)

		if target is self:
			return self._get_config(key_target)
		else:
			return target.get_config(key_target)

	# Config check methods.

	def _is_configured(self, key):
		"""Called to actually *find out* if a key is configured."""

		return key in self
	
	def is_configured(self, key):
		"""Return True if KEY exists, else False."""

		# Find target.
		(key_target, target) = self._get_target(key)

		if target is self:
			return self._is_configured(key_target)
		else:
			return target.is_configured(key_target)
