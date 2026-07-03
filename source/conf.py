# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Care Robot'
copyright = '2025, Trung Bui'
author = 'Trung Bui'
release = '1.0.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration
import os
import sys

# Source roots for autodoc. The new closed-loop stack lives under
# .../remote_dir; keep carerobotapp/pyconnect for any legacy API pages.
_REPO = os.environ.get('CAREROBOT_REPO', '/media/keti/workdir/remote_dir')
for _pkg in ('robot_agent', 'kcare_robot', 'pyplanner', 'carerobotapp', 'pyconnect'):
    _path = os.path.join(_REPO, _pkg)
    if os.path.isdir(_path):
        sys.path.insert(0, _path)

extensions = [
    'sphinx.ext.autodoc',  # For auto-generating docs from code
    'sphinx.ext.viewcode', # Links to source code
    'sphinx.ext.napoleon', # Supports Google/NumPy docstring styles
]

templates_path = ['_templates']
# Legacy autodoc stubs for the old MARS ``carerobotapp`` package: they import
# ROS2/heavy deps that aren't present in the docs env and aren't in any toctree.
# Keep the files for reference but skip them at build time.
exclude_patterns = ['apidoc/**']


autodoc_default_options = {
    'members': True,
    'undoc-members': True,
    'private-members': False,
    'special-members': '__init__',
    'show-inheritance': True,
}




# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
# Holds self-hosted media (e.g. robot demo videos in _static/videos/).
html_static_path = ['_static']