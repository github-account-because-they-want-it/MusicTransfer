'''
Created on Dec 23, 2014
@author: Mohammed Hamdy
'''

from importlib import import_module
from glob import iglob
from os import path

def loadModulesFromPackage(package):
  """
  Loads all .py files in `package` as modules an returns them 
  package : a dotted path to a package, relative to sys.path (str)
  """
  found_modules = []
  # convert package name to folder name
  loaded_package = import_module(package)
  package_dir = path.dirname(loaded_package.__file__)
  python_files_in_package = iglob(path.join(package_dir, "*.py")) # it could also be .pyc, .pyw and probably others
  for pf in python_files_in_package:
    bare_module_name = path.splitext(path.split(pf)[1])[0]
    module_name = '.'.join([package, bare_module_name])
    found_modules.append(import_module(module_name))
  return found_modules

def parsePythonObjects(package):
  package_objects = []
  for module in loadModulesFromPackage(package):
    package_objects.extend([getattr(module, attr) for attr in dir(module) if not attr.startswith("__")])
  return package_objects
        
def parseSubclasses(package, cls):
  python_objects = parsePythonObjects(package)
  subclasses = []
  for po in python_objects:
    try:
      # if not po is cls because issubclass(cls, cls) returns True, which is undesired
      if not po is cls and callable(po) and issubclass(po, cls):
        subclasses.append(po)
    except TypeError: # issubclass will frown if po is a function. We just need to skip that
      continue
  return subclasses
    
