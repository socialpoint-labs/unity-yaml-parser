# How to contribute to unityparser #

(this is pretty much a copy of the [Sheetfu][sheetfu] contribution documentation).

Thank you for considering contributing to unityparser! This is a very young module,
easy to understand, where lots can be added.


## Support questions ##

For questions about your own code ask on [Stack Overflow][Stack Overflow]. Search with
Google first using:
`site:stackoverflow.com unityparser {search term, exception message, etc.}`

[Stack Overflow]: https://stackoverflow.com/questions/tagged/unityparser?sort=linked


## Reporting issues ##

Use the issue tracker for this:

- Describe what you expected to happen.
- If possible, include a [minimal, complete, and verifiable example][minimal, complete, and verifiable example] 
  to help us identify the issue. This also helps check that the issue is not with 
  your own code.
- Describe what actually happened. Include the full traceback if there was an
  exception.
- List your Python and unityparser version.

[minimal, complete, and verifiable example]: https://stackoverflow.com/help/mcve

## Submitting patches ##

- Include tests if your patch is supposed to solve a bug, and explain
  clearly under which circumstances the bug happens. Make sure the test fails
  without your patch.
- Try to follow [PEP8][PEP8].
- Use the utils at your disposition in test folders to mock api requests.
- Every mock request should be put in the fixture folder.
- Tests are run with pytest.

### First time setup ###

- Download and install the [latest version of git][latest version of git].
- Configure git with your [username][username] and [email][email]::
  ```
  git config --global user.name 'your name'
  git config --global user.email 'your email'
  ```

- Make sure you have a [GitHub account][[GitHub account]].
- Fork unityparser to your GitHub account by clicking the [Fork][Fork] button.
- [Clone][Clone] your GitHub fork locally::
  ```
  git clone https://github.com/{username}/unity-yaml-parser
  cd unity-yaml-parser
  ```

- Add the main repository as a remote to update later::
  ```
  git remote add socialpoint-labs https://github.com/socialpoint-labs/unity-yaml-parser
  git fetch socialpoint-labs
  ```

- Create a virtualenv::
  ```
  python3 -m venv env
  . env/bin/activate
  # or "env\Scripts\activate" on Windows
  ```

- Install unityparser requirements with development dependencies::
  ```
  pip install -r requirements/test.txt
  npm install .
  ```

[GitHub account]: https://github.com/join
[latest version of git]: https://git-scm.com/downloads
[username]: https://help.github.com/articles/setting-your-username-in-git/
[email]: https://help.github.com/articles/setting-your-email-in-git/
[Fork]: https://github.com/socialpoint-labs/unity-yaml-parser/fork
[Clone]: https://help.github.com/articles/fork-a-repo/#step-2-create-a-local-clone-of-your-fork

### Start coding ###

- Create a branch to identify the issue you would like to work on (e.g.
  `2287-dry-test-suite`)
- Using your favorite editor, make your changes, [committing as you go][committing as you go].
- Try to follow [PEP8][PEP8].
- Include tests that cover any code changes you make. Make sure the test fails
  without your patch.
- Push your commits to GitHub and [create a pull request][create a pull request].
- Celebrate 🎉

[committing as you go]: http://dont-be-afraid-to-commit.readthedocs.io/en/latest/git/commandlinegit.html#commit-your-changes
[PEP8]: https://pep8.org/
[create a pull request]: https://help.github.com/articles/creating-a-pull-request/


### Running the tests ###

Run the basic test suite with::
```
pytest
```

This only runs the tests for the current environment. Github Actions will run the full
suite when you submit your pull request.


### Running test coverage ###

Generating a report of lines that do not have test coverage can indicate
where to start contributing. Run `pytest` using `coverage` and generate a
report on the terminal and as an interactive HTML document::
```
coverage run -m pytest
coverage report
coverage html
# then open htmlcov/index.html
```

Read more about [coverage](https://coverage.readthedocs.io).


### Checking commit correctness ###

The Makefile provides an utility to check that your commits adhere to the below commit specification before opening a PR::
```
make lint
```

### Semantic versioning ###

Unityparser follows the 2.0.0 specification of Semantic Versioning. All version number should follow the following format::
```
v<major>.<minor>.<patch>
example: v3.5.1
```

Read more about [semantic versioning](https://semver.org/).


### AngularJS commit convention ###

Unityparser follows the AngularJS commit specifications. Commit messages should be structured with the following format::
```
<type>(<scope>): <subject>
<BLANK LINE>
<body>
<BLANK LINE>
<footer>
```

Allowed <type> values are the following::
```
build (build related)
chore (maintain)
ci (continuous integration related)
docs (documentation)
feat (feature)
fix (bug fix)
improvement (improve existing code)
perf (prefromance related improvements)
refactor (code refactoring)
revert (reverted code)
style (formatting)
test (when adding missing tests)
```

The exact rules are extracted from [this liter rules file](https://github.com/conventional-changelog/commitlint/blob/master/@commitlint/config-conventional/index.js).
It's important to follow this commit specification, as the version numbers will be generated accordingly to the commit messages since the previous version.
It's also important to specify which commits include breaking changes in the commit footer.

Read more about [AngularJS commit convention](https://gist.github.com/stephenparish/9941e89d80e2bc58a153/).


### Manually releasing a new version to Pypi ###

Only Admins of the repository have the ability to manually release a new version and publish it to Pypi.
To do so follow the below steps in addition to the environment setup for development described above::
````
pip install -r requirements/publish.txt
GH_TOKEN=<Personal API Token for Github with repo permission> \
  REPOSITORY_PASSWORD=<unity-yaml-parser Pypi API Token> \
  make release
````

### make targets ###

Unityparser provides a `Makefile` with various shortcuts.

- `make test` runs the basic test suite with `pytest`
- `make cov` runs the basic test suite with `coverage`

[sheetfu]: https://github.com/socialpoint-labs/sheetfu