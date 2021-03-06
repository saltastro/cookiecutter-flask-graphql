import re
import sys


MODULE_REGEX = r'^[_a-zA-Z][_a-zA-Z0-9]+$'

module_name = '{{ cookiecutter.project_slug }}'
open_source_license = '{{ cookiecutter.open_source_license }}'

if not re.match(MODULE_REGEX, module_name):
    print('ERROR: The package name (%s) is not a valid Python module name. Please do not use a - and use _ instead' % module_name)

    #Exit to cancel project
    sys.exit(1)
