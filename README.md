# Unity YAML Parser #
![travis](https://travis-ci.org/socialpoint-labs/unity-yaml-parser.svg?branch=master)

This project aims to provide a python3 API to load and dump Unity YAML 
files(configurations, prefabs, scenes, serialized data, etc) in the exact same 
format the internal Unity YAML serializer does.

Using this API you will be able to easily manipulate(as python objects) 
Unity YAML files and save them just the same, keeping the YAML structure
exactly as Unity does. This has the advantages of, first not having to
configure PyYAML beforehand to deal with Unity YAMLs, and second as the
modified file keeps the same structure and formatting that Unity does, 
when the YAML file is loaded by Unity it won't make formatting changes 
to it that will make any VCS report unexpected file changes.

## Installing ##

Install and update using [pip](https://pip.pypa.io/en/stable/quickstart/):
````
pip install -U unityparser
````
## A Simple Example ##
````python
from unityparser import UnityDocument

# Loading and modifying a config file with a single YAML document
project_settings_file = 'UnityProject/ProjectSettings/ProjectSettings.asset'
doc = UnityDocument.load_yaml(project_settings_file)
ProjectSettings = doc.entry
ProjectSettings.scriptingDefineSymbols['1'] += ';CUSTOM_DEFINE'
ProjectSettings.scriptingDefineSymbols['7'] = ProjectSettings.scriptingDefineSymbols['1']
doc.dump_yaml()

# You can also load YAML files with multiple documents
hero_prefab_file = 'UnityProject/Assets/Prefabs/Hero.prefab'
doc = UnityDocument.load_yaml(hero_prefab_file)
for entry in doc.entries:
  if entry.__class__.__name__ == 'MonoBehaviour' and getattr(entry, 'MaxHealth', None) is not None:
    entry.MaxHealth = str(int(entry.MaxHealth) + 10)
    break
doc.dump_yaml()
# calling entry method for a doc with multiple document will return the first one
print(doc.entry.__class__.__name__)
# 'Prefab'
````

## Classes ##

### unityparser.UnityDocument ###

Main class to load and dump files.

#### unityparser.UnityDocument.load_yaml(file_path) ####

_**Classmethod**_: Load the given YAML file_path and return a UnityDocument file

#### unityparser.UnityDocument.dump_yaml(file_path=None) ####

Dump the UnityDocument to the previously loaded file location(overwrite). 
If *file_path* argument is provided, dump the document to the specified location instead.

This method **keeps line endings** of the original file when it dumps.

#### unityparser.UnityDocument.entries ####

_**Property**_: Return the _list_ of documents found in the YAML. The objects in the _list_ are of _types_ Class named after the serialized Unity class(ie. MonoBehaviour, GameObject, Prefab, CustomName, etc).

#### unityparser.UnityDocument.entry ####

_**Property**_: Return the first document in the YAML, useful if there is only one. Equivalent of doing `UnityDocument.entries[0]`.

### unityparser.loader.UnityLoader ###

PyYAML's Loader class, can be used directly with PyYAML to customise loading. 

### unityparser.dumper.UnityDumper ###

PyYAML's Dumper class, can be used directly with PyYAML to customise dumping. 

## Considerations ##

**unityparser** converts _every_ scalar value in the YAML to _string_ when loading the data for safety purposes. Any key from the mappings in the YAML included.   

You have to make sure to convert every modified/added value(or _dict_ key) in the loaded data object back to _string_ before dumping the document. Otherwise the written YAML will contain ugly tags.

Text scalars which are single or double quoted that span multiple lines are not being dumped exactly as Unity does. There's a difference in the maximum length allowed per line and the logic to wrap them.

**Unity scenes are not yet supported**. It shouldn't require much effort to do so.
