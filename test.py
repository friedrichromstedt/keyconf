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

		# Test passed.

if __name__ == '__main__':
	unittest.main()
