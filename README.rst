Summmary
========

A module providing a framework for configuration of components using 
arguments to a top-level function.

The module is released under MIT, the license is included in the source file.

keyconf uses `Bento <http://github.com/cournape/Bento>`_ as its packaging 
solution, please refer to there for Bento usage documentation.

Below is some technical introduction.


Example
=======

::

    >>> import keyconf
    >>> component = keyconf.Configuration()

    # Configure a key.
    >>> component.configure(leaf = 'green')
    >>> component['leaf']
    'green'
    >>> component
    {'leaf': 'green'}

Now, let's use the {component} in another Configuration::

    >>> top = keyconf.Configuration(sub = component)

    # The component is hidden.
    >>> top
    {}

    # Configure ordinary keys in {top}.
    >>> top.configure(stem = 'brown')

    # Configure {component} by calls to {top}.
    >>> top.configure(sub_leaf = 'yellow')

    # The key has been forwarded.
    >>> component
    {'leaf': 'yellow'}

Overwriting and deletion of keys::

    # Configure the leaf again, but leave the value unchanged.
    >>> component.configure(leaf = None)
    >>> component['leaf']
    'yellow'

    # Delete an key, first create one, than delete it.
    >>> component.configure(ill = 'faint green')
    >>> top.unconfigure('sub_ill')
    >>> component
    {'leaf': 'yellow'}

Test whether some key is configured or not::

    # Test for keys.
    >>> top.is_configured('sub_ill')
    False
    >>> component.is_configured('leaf')
    True

Components can be added later by::

    >>> top.add_components(**components)

    and can be deleted by:

    >>> top.remove_components(*names)  .

Aliases make life easier or less troublesome sometimes::

    >>> top.set_alises(alias = 'sub_leaf')
    >>> top.is_configured('alias')
    True
    >>> top.unset_aliases('alias')
    >>> top.is_configured('alias')
    False
