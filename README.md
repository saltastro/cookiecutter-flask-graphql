# cookiecutter-python-package

A boilerplate for a Flask server with a GraphQL API. It is based on [Audrey Roy Greenfeld's pypackage cookiecutter](https://github.com/audreyr/cookiecutter-pypackage). The Flask configuration and the file layout have been adapted from the ones in Miguel Grinberg's *Web Development with Flask*, Second Edition (O'Reilly, 2018).

## Getting started

Ensure that [cookiecutter](https://cookiecutter.readthedocs.io/en/latest/) is installed on your computer.

You can then create a new project by using cookiecutter with this template.

```bash
cookiecutter https://github.com/saltastro/cookiecutter-flask-graphql.git
```

Assuming all the project's requirements have been installed, you need to define a couple of environment variables and then can start the server using a `make` target.

```bash
cd /path/to/your/project
export FLASK_CONFIG=development
export DEV_DATABASE_URI="mysql+pymysql://user:password@your.db.host/dev_db_name"
export TEST_DATABASE_URI="mysql+pymysql://user:password@your.db.host/test_db_name"
export DATABASE_URI="mysql+pymysql://user:password@your.db.host/db_name"
export JWT_SECRET_KEY=topsecret
export DSN_KEY=https://somecrypticstring@sentry.io/somenumber  # this is optional
make start
```

Of course you can also define the environment variables and launch the server from your IDE.

To test the server you may point your browser to [http://localhost:5000/graphql](http://localhost:5000/graphql).

## cookiecutter input

When using the template, cookiecutter asks you for various input:

`full_name`. Your full name, as it should appear in the license file and in `setup.py`.

`email`. Your email address. This is included as the value of `author_email` in `setup.py`.

`project_name`. The name of the project. This should be a human-friendly name and may contain spaces.

`project_slug`. The name of the package. This must be a valid Python package name.

`project_short_description`. A brief description of the project.

`version`. The version.

`log_file_path`. The file path for the log file. The file will be created automatically by Flask if it doesn't exist. If no file path is given, no logging to file is done. See the Python documentation on logging in general and that on rotating file handlers in particular for details on how logging is done.

`log_file_max_bytes`. The maximum file size of the log file, in bytes. The file content will be removed (or moved to a backup) once this limit is reached.

`log_file_backup_count`. The number of backup files for the log file.

`use_sentry`. Whether to use [Sentry](https://sentry.io/). You also have to define a `SENTRY_DSN` environment variable if you are planning to use Sentry.

`github_username`. Your Github username. This is used for generating the URL of the project's repository.

`github_repository`. The Github repository for the project.

`open_source_license`. The open source license to use for the project. For all choices other than "Not open source" a license file will be generated.

`install_requiremnts`. Whether to install this project's requirements. The project will be installed into a virtual environment `venv` in the project's root folder.

## Configuring the project

Once the project has been created, you should tweak various parts of it. **Take note of the warning in the section on documentation below before making any changes.**


### Modify the GraphQL content

The created Python code includes two GraphQl queries, `authToken` and `whoAmI`. `authToken` makes use of the `AuthType` object type defined in `app/graphql/schema/auth_token.py`. You have to modify its `resolve_token` method.

You should remove or modify the `whoAmI` query and its object type. The relevant files are `app/graphql/schema/query.py` and `app/graphql/schema/who_am_i.py`. Remember to remove or modify the tests in `tests/test_who_am_i.py` as well.

### Optionally modify the error handlers

Application error handlers are included in `app/main/errors.py`. Feel free to modify them as you deem fit.

### Adding a new blueprint

If you need to add a blueprint ('rest', say), you should:

* Create a folder `app/rest`.

* Create a file `app/rest/__init__.py` with the following content.

```python
from flask import Blueprint

main = Blueprint('rest', __name__)

from . import views
```

* Create a file `app/rest/views.py` defining the routes for the new blueprint.

* Register the blueprint in `app/__init__.py`:

```python
app.register_blueprint('rest', __name__)
```

### Modify the test content

The project's `/tests` folder contains two example test file, which need to be removed or modified. You may add other files in the `/tests` folder. Their name should start with `test_` so that pytest can access their tests.

Also see the section on testing below.

### Check the tox configuration

While this might not be necessary, you may tweak the configuration of tox by updating its configuration file `tox.ini`. In particular, you should add testing for Python 2.7 if you are planning to support this version.

### What about Python 3.7?

Python 3.7 is included in `tox.ini` but not in the `.travis.yml` file. The reason for the latter is that Travis does not support Python 3.7 "out of the box". If you want to include it, you have to modify the configuration file in line with the recipe given at the end of [https://github.com/travis-ci/travis-ci/issues/9069#issuecomment-425720905](https://github.com/travis-ci/travis-ci/issues/9069#issuecomment-425720905).

### Create documentation

First, a warning. When Sphinx generates the documentation, it will import the Python modules. **Make sure that all code with side effects such as changing files or updating a database is protected by an `if __name__ == '__main__'` condition.**

Documentation should be created in three places.

* Add docstrings to your code. All the docstrings should follow the [Numpy](https://numpydoc.readthedocs.io/en/latest/format.html#docstring-standard) or [Google](https://google.github.io/styleguide/pyguide.html#Comments) conventions. An API reference is automatically generated from your docstrings; see the file `docs/api.rst`.

* Add documentation in the `docs/` folder. When adding new files to this folder, you should remember to add them to the `toctree` directive in `docs/index.rst`. Both reStructuredText and Markdown (CommonMark, to be precise) files are supported, and they must have the suffix `.rst` and `.md`, respectively.

* And of course you should update the `README.md` file. While this file is not included in the documentation generated by [Sphinx](http://www.sphinx-doc.org/), it is what users will see when they navigate to your project's Github repository.

### Update the linting rules

[Flake8](http://flake8.pycqa.org/) is used for linting. If you need to configure any of its rules, modify the Flake8 section in `setup.cfg` accordingly. One rule which is tweaked in the configuration file is the maximum line length. It is set to 120 characters.

### Hook up the project

Optionally, you may hook up your project with [Travis](https://travis-ci.com) and [Read the Docs](https://readthedocs.org). When using Travis, make sure you define the required environment variables in your project's settings on Travis.

## Testing

All unit tests should be included in the `tests/` folder.

For convenience, the pytest configuration file `tests/conftest.py` includes a fixture `graphql` that facilitates writing tests for GraphQL queries. When used in a test, this fixture takes a GraphQL query and a user id, and sends the query to the GraphQL endpoint, along with the correct `Authorization` header for the user with the given user id. The server response is parsed as a JSON object, and the corresponding `dict` is returned.

The `snapshottest` package is included in the project requirements. It allows to use snapshots with GraphQL tests.

The following example illustrates the use of the `graphql` fixture and `snapshottest`.

```python
def test_returns_user_id(graphql, snapshot):
    """The user id is returned for the user making the request."""

    query = '''query {
    whoAmI {
        userId
    }
}'''
    res = graphql(query, 42)
    snapshot.assert_match(res)
```

You may update the snapshots by running:

```bash
python -m pytest --snapshot-update 
```

## Environment variables

The generated Python code requires several environment variables to be defined.

Name | Description | Example value
--- | --- | ---
FLASK_APP | Path to the app file | {{ cookiecutter.project_slug }}.py
FLASK_CONFIG | Flask configuration environment ('development', 'test' or 'production') | 'development'
DEV_DATABASE_URI | Database URI for development | mysql+pymysql://user:password@your.db.host/dev_db_name
TEST_DATABASE_URI | Database URI for tests | mysql+pymysql://user:password@your.db.host/test_db_name
DATABASE_URI | Database URI for production | mysql+pymysql://user:password@your.db.host/db_name
JWT_SECRET_KEY | Secret key for encoding JWT tokens | topsecret
SENTRY_DSN | Sentry DSN | https://somecrypticstring@sentry.io/somenumber

Note that the database URIs start with `mysql+pymysql` - the `+pymysql` is necessary.

In case you are starting the server by means of `make start`, you do not have to define `FLASK_APP`.

If `FLASK_CONFIG` is not set, 'development' is used as the configuration environment. 

The Sentry DSN is only required if you want to use Sentry. You should obtain it from the settings of your Sentry project.

In addition to these variables you may also wish to define `FLASK_ENV`, as explained in [Flask's configuration documentation](http://flask.pocoo.org/docs/1.0/config/).

## Support for the development process

### Using a virtual environment

While this is not strictly necessary, it is a good idea to use a dedicated virtual environment when doing development work on this project. Chances are that one has been set up in a `venv` folder within the project's root folder when the project files were generated. Remember that you have to activate it.

```bash
source venv/bin/activate
```

You may deactivate it again when you are finished working.

```bash
deactivate
```

If no virtual environment has been created, you may do this yourself and install the project requirements.

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements-to-freeze.txt
```

### The Makefile

The project's root folder contains a `Makefile` defining vartious useful tasks. You run a task (\some_task', say) by using the `make` command.

```bash
make some_task
```

The most important tasks are:

`help`. List all the available tasks.

`clean`. Remove all automatically generated artifacts.

`test`. Run pytest.

`lint`. Run Flake8 on the files in the `src/` and `tests/` folders (and their subfolders).

`coverage`. Check the test coverage and display the results in the terminal and in a browser.

`tox`. Run tox, using pytest and Flake8 for several Python versions.

`docs`. Create html documentation from the files in the `docs/` folder and open it in a browser. The documentation includes an API reference generated from the docstrings in the source code. See the warning in the section on documentation before using this task.

`start`. Start the server in development mode.

These tasks may clean up existing artificats before they run.

### Bumping the version

The project version is included both in `setup.py` and in the package's `__init__.py` file. So rather than manually updating it, it is easier to use [bumpversion](https://github.com/peritus/bumpversion).

```bash
bumpversion part
```

`part` must be 'major', 'minor' or 'patch', depending on the kind of version change you want to make. For example:

``` bash
# current version is 0.1.0
bump patch  # version is now 0.1.1
bump minor  # version is now 0.2.0
bump major  # version is now 1.0.0
```

bumpversion takes the current version from `setup.cfg` and replaces it with the new version after updating the other files.

## Deploying the project

This cookiecutter is completely agnostic as to how you should deploy the Flask server. See [http://flask.pocoo.org/docs/1.0/deploying/#deployment](http://flask.pocoo.org/docs/1.0/deploying/#deployment) for various options you have.
