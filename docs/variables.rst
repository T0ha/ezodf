.. _variables:

Variables Objects
=================

Variables Class and Subclasses
------------------------------

.. class:: Variables()

   The :class:`Variables` is dict-like container for subclasses of :class:`Variable`.
   This is superclass for :class:`SimpleVariables` and :class:`UserFields`

.. warning::

   Don't create instances of this class  and its subclasses yourself, use :attr:`document.body.variables` or :attr:`document.body.userfields`


Methods
~~~~~~~

.. method::  Variables.__getitem__(key)
    
    Get :class:`Variable` instance by varible name

    :param str key: Variable name
    :rtype: :class:`Variable` instance
    :return: Variable class instance
    
.. method::  Variables.__setitem__(key, value)
    
    Set :class:`Variable` instance by varible name

    :param str key: Variable name
    :param value: Variable value
    :type value: float or boolean or str
    :rtype: :class:`Variable` instance
    :return: Variable class instance

.. class:: SimpleVariables()

   The :class:`SimpleVariables` is dict-like container for :class:`SimpleVariable`, it's a subclass of :class:`Variables`
   
.. class:: UserFields()

   The :class:`UserFields` is dict-like container for :class:`UserField`, it's a subclass of :class:`Variables`
   

Variable class and subclasses
-----------------------------

.. class:: Variable()

    This class represents a variable. 
    The instances of it can be found in :class:`Variables` and accessed through `document.body.variables['somevar']` or `document.body.userfields['somevar']`

Attributes
~~~~~~~~~~

.. attribute:: Variable.type(read/write)
    
    Type of the variable can be 'string', 'float', 'boolean' or other described in 19.385 of "OpenDocument-v1.2-os-part1"

    :type: str

.. attribute:: Variable.value(read/write)

    Value of the variable converted to Python type according to :attr:`Variable.type`

    :type: str, float, boolean

.. attribute:: Variable.instances(read/write)

    See :class:`SimpleVariableInstance` and :class:`UserFieldInstance`

.. warning::

    Use with caution can work a bit unexpected

.. class:: SimpleVariable()

    This class represents a simple variable. The instances of it can be found in :class:`SimpleVariables` and accessed through `document.body.variables['somevar']`

Attributes
~~~~~~~~~~

.. attribute:: SimpleVariable.instances(read/write)

    List of :class:`SimpleVariableInstance` subclasses that represents occurrences of variable in document see 7.4.4 - 6 of "OpenDocument-v1.2-os-part1"

.. warning::

    Use with caution can work a bit unexpected

.. class:: UserField()

    This class represents a simple variable. The instances of it can be found in :class:`SimpleVariables` and accessed through `document.body.variables['somevar']`

Attributes
~~~~~~~~~~

.. attribute:: UserField.instances(read/write)

    List of :class:`UserFieldInstance` subclasses that represents occurrences of variable in document see 7.4.9 - 10 of "OpenDocument-v1.2-os-part1"

.. warning::

    Use with caution can work a bit unexpected

Simple Variable Instance Subclasses
-----------------------------------

.. class:: SimpleVariableInstance()

    Base class for :class:`SimpleVariableGet`, :class:`SimpleVariableSet` and :class:`SimpleVariableInput`

Attributes
~~~~~~~~~~

.. attribute:: SimpleVariableInstance.type(read/write)
    
    Type of the variable can be 'string', 'float', 'boolean' or other described in 19.385 of "OpenDocument-v1.2-os-part1"

    :type: str

.. attribute:: SimpleVariableInstance.value(read/write)

    Value of the variable converted to Python type according to :attr:`SimpleVariableInstance.type`

    :type: str, float, boolean

.. class:: SimpleVariableGet()

    Subclass of :class:`SimpleVariableInstance` handling "text:variable-get" tag.

.. class:: SimpleVariableSet()

    Subclass of :class:`SimpleVariableInstance` handling "text:variable-set" tag.

.. class:: SimpleVariableInput()

    Subclass of :class:`SimpleVariableInstance` handling "text:variable-input" tag.
