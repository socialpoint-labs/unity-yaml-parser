# Unity YAML Parser #

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
ProjectSettings.scriptingDefineSymbols[1] += ';CUSTOM_DEFINE'
ProjectSettings.scriptingDefineSymbols[7] = ProjectSettings.scriptingDefineSymbols[1]
doc.dump_yaml()

# You can also load YAML files with multiple documents and filter for a single or multiple entries
hero_prefab_file = 'UnityProject/Assets/Prefabs/Hero.prefab'
doc = UnityDocument.load_yaml(hero_prefab_file)
# accessing all entries
doc.entries
# [<UnityClass>, <UnityClass>, ...]
# accessing first entry
doc.entry
# <UnityClass>
# get single entry uniquely defined by filters
entry = doc.get(class_name='MonoBehaviour', attributes=('m_MaxHealth',))
entry.m_MaxHealth += 10
# get multiple entries matching a filter
entries = doc.filter(class_names=('MonoBehaviour',), attributes=('m_Enabled',))
for entry in entries:
    entry.m_Enabled = 1
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

#### unityparser.UnityDocument.get(class_name=None, attributes=None) ####

_**Method**_: Return a single entry uniquely matching the given filters. Must exist exactly one.

#### unityparser.UnityDocument.filter(class_names=None, attributes=None) ####

_**Method**_: Return a list of entries matching the given filters. Many or none can be matched.

### unityparser.loader.UnityLoader ###

PyYAML's Loader class, can be used directly with PyYAML to customise loading. 

### unityparser.dumper.UnityDumper ###

PyYAML's Dumper class, can be used directly with PyYAML to customise dumping. 

## Considerations ##

Text scalars which are single or double quoted that span multiple lines are not being dumped exactly as Unity does. There's a difference in the maximum length allowed per line and the logic to wrap them.

