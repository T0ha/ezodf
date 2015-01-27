.. module:: variables

Templating and Variables Management
===================================

OpenOffice documents have a function convenient for templating documents. It is user defined variables which can be filled-in by user once ore several times in document and automatically filled-in in all places where it is inserted. `OpenDocument-v1.2-os-part1` defines 2 types of such variables:

* Simple Variables
* User Fields

Both of them can be filled-in by **ezodf**.

Variables workflow examples
---------------------------

You can access simple variables through 

variables attribute for :class:`SimpleVariables`::
    
    from ezodf import opendoc
    doc = opendoc('somedoc.odt')
    # Print all simple variables with types and values
    for variable in doc.body.variables:
        print("%s (%s) = %s" % (v.name, v.type, v.value)
    # Set new value for 'test' variable
    d.body.variables['test'] = 22
    # Print new 'test' value and type
    v = doc.body.variables['test']
    print("%s (%s) = %s" % (v.name, v.type, v.value)


userfields attribute for :class:`UserFields`::
    
    from ezodf import opendoc
    doc = opendoc('somedoc.odt')

    # Print all userfields with types and values
    userfields = doc.body.userfields
    for v in userfields:
        print("%s (%s) = %s" % (v.name, v.type, v.value)

    # Set new value for 'test' variable
    d.body.userfields['test'] = 22

    # Print new 'test' value and type
    v = doc.body.userfields['test']
    print("%s (%s) = %s" % (v.name, v.type, v.value)


.. seealso:: :class:`SimpleVariables` and :class:`UserFields`
