"""
Pretend that OpenMM is installed.

Anything can be imported from the "simtk" namespace. Names starting in lower
case are imported as packages (so other names can be imported from them), names
staring in upper case are imported as classes (so they can be used as type
annotations).
"""

from pretends import add_pretend_module
add_pretend_module('simtk')