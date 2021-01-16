# Setup For Django Development with Visual Studio Code

In a terminal:

    mkdir <project>
    cd <project>
    python -m venv .venv
    source .venv/bin/activate
    pip install django
    django-admin startproject <project-name> . # note the dot (doesn't create subfolder)
    deactivate
    code .

Edit `.vscode/settings.json` to include:

    {
        "files.associations": {
            "**/*.html": "html",
            "**/templates/**/*.html": "django-html",
            "**/templates/**/*": "django-txt",
            "**/requirements{/**,*}.{txt,in}": "pip-requirements"
        },
        "emmet.includeLanguages": {"django-html": "html"},
        "python.pythonPath": "/Users/anthony/develop/superlists/.venv/bin/python3",
        "python.linting.pylintEnabled": true,
        "python.linting.pylintArgs": [
            "--load-plugins",
            "pylint_django"
        ]
    }

Ensure that the .venv Python is selected and the right version

Open an integrated terminal in VS Code (⌃\`)

Ensure that the .venv is activated

    pip install pylint
    pip install pylint_django

Add a `.gitignore` to the project root folder

    *.db
    *.sqlite3
    *.pyc
    *~
    /.vscode
    /.venv

    # Accept these files in the repository
    !.gitignore
    !.travis.yml

Add a `.pylintrc` to the project root folder

    [BASIC]

    # Regular expression matching correct argument names. Overrides argument-
    # naming-style.
    # Allows short argument names such as "pk"
    argument-rgx=^[a-z][a-z0-9]*((_[a-z0-9]+)*)?$

    # Good variable names which should always be accepted, separated by a comma.
    good-names=i,
               j,
               k,
               ex,
               Run,
               _

    # Regular expression matching correct variable names. Overrides variable-
    # naming-style.
    # Allows short variable names such as "pk"
    variable-rgx=^[a-z][a-z0-9]*((_[a-z0-9]+)*)?$

Create and edit `.vscode/launch.json` to include:

    {
        "version": "0.2.0",
        "configurations": [
            {
                "name": "Python: Django",
                "type": "python",
                "request": "launch",
                "program": "${workspaceFolder}/manage.py",
                "args": [
                    "runserver"
                ],
                "django": true
            }
        ]
    }

## How to fix Virtual Env after python upgrade

    # Delete the broken links
    find .venv -type l -print
    find .venv -type l -delete
    python -m venv .venv
