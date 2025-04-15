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
sys.path.insert(0, '/media/keti/workdir/projects/app_carerobot')
sys.path.insert(0, '/media/keti/workdir/projects/pyconnect')

extensions = [
    'sphinx.ext.autodoc',  # For auto-generating docs from code
    # 'sphinx.ext.viewcode', # Links to source code
    'sphinx.ext.napoleon', # Supports Google/NumPy docstring styles
]

templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
#html_static_path = ['_static']