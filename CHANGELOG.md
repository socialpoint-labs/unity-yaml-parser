# [2.0.0](https://github.com/socialpoint-labs/unity-yaml-parser/compare/v1.0.0...v2.0.0) (2021-05-03)


### Bug Fixes

* **command:** convert Path to str ([157db9e](https://github.com/socialpoint-labs/unity-yaml-parser/commit/157db9eff900e604beb1408a48f4a6a648028aca))


### chore

* **setup:** drop support for Python 3.5 ([beaf2f6](https://github.com/socialpoint-labs/unity-yaml-parser/commit/beaf2f6ddbcd99ef05a95d8f613886d2687d194a))


### Features

* **representer:** save string representation ([6b2bb15](https://github.com/socialpoint-labs/unity-yaml-parser/commit/6b2bb150557fb7a13faba5bd7699722239762fa6))


### BREAKING CHANGES

* **setup:** A security update of PyYAML to 5.4 forces to drop
support to Python 3.5



# [1.0.0](https://github.com/socialpoint-labs/unity-yaml-parser/compare/v0.1.0...v1.0.0) (2019-12-06)


### Features

* **commitlint:** add commitlint configuration ([73d0d81](https://github.com/socialpoint-labs/unity-yaml-parser/commit/73d0d8112d7e62ef1db3f01b8f69f3803d037ccb))
* **Makefile:** add update-changelog make command ([eb3cbd5](https://github.com/socialpoint-labs/unity-yaml-parser/commit/eb3cbd55fb85202abb0e53540904a6874971ef2e))
* **resolver:** add safe value types int and float ([3bd6918](https://github.com/socialpoint-labs/unity-yaml-parser/commit/3bd6918cf20ba31c32b7fd567f2fc680c17f895f)), closes [#1](https://github.com/socialpoint-labs/unity-yaml-parser/issues/1) [#15](https://github.com/socialpoint-labs/unity-yaml-parser/issues/15)
* **travis:** add commitlint check step to Travis CI ([050f4d5](https://github.com/socialpoint-labs/unity-yaml-parser/commit/050f4d5f1aa245eee17555f1ea9a86a70286a7d2))
* **unitydocument:** add get and filter methods to UnityDocument ([36a4b91](https://github.com/socialpoint-labs/unity-yaml-parser/commit/36a4b9150c4b9cd81ccb0829ee07ec67c62c02fc))


### BREAKING CHANGES

* **resolver:** loaded UnityClass entries attributes may now be int or
float too, not only strings.

To migrate the code, ensure you are explicitly casting to str whenever you
manipulate entry attributes like below:

Before:

new_id = doc.entry.build + '-dev' # => '123-dev'

After:

new_id = str(doc.entry.build) + '-dev'

By allowing int and float safe values, no casting is needed in Python code
to do number manipulation back and forth(to deserialize from and serialize
to string).



# [0.1.0](https://github.com/socialpoint-labs/unity-yaml-parser/compare/v0.0.1...v0.1.0) (2019-10-18)


### Bug Fixes

* **tests:** add autouse fixture to ensure every test runs with a clear ([bc1db54](https://github.com/socialpoint-labs/unity-yaml-parser/commit/bc1db54fff5068182f8d0261af73a69ac09a006e))
* **travis:** fix windows miniconda not finding libraries ([6738224](https://github.com/socialpoint-labs/unity-yaml-parser/commit/6738224e96eff26a31b126d67358b05b93616a94))
* **UnitClassIdMap:** allow identifying Unity classes by it's 'id-name' ([18e55a4](https://github.com/socialpoint-labs/unity-yaml-parser/commit/18e55a49196f466f124be7485a86a60018beb5e9))
* **UnityClassIdMap:** make UnityClassIdMap reset method inter-process safe ([7175e3e](https://github.com/socialpoint-labs/unity-yaml-parser/commit/7175e3e57b438867f3bc46000f2542a66cebdfdc))


### Features

* **prefab:** add scene and prefab support ([dec5a27](https://github.com/socialpoint-labs/unity-yaml-parser/commit/dec5a27f1b4137cb496cafc788ed71da3d40d09f))



## [0.0.1](https://github.com/socialpoint-labs/unity-yaml-parser/compare/dd4c87ff3f320ba1f55d057e5946a9897c45cb1c...v0.0.1) (2019-06-11)


### Features

* **scope:** initial commit ([dd4c87f](https://github.com/socialpoint-labs/unity-yaml-parser/commit/dd4c87ff3f320ba1f55d057e5946a9897c45cb1c))



