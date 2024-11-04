# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys
from pathlib import Path

import django


project = 'rest framework extensions'
copyright = '2024, Xiang Wang'
author = 'Xiang Wang'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
        "myst_parser",
        "sphinx_design",
        "sphinx.ext.todo",
        "sphinx.ext.autodoc",
        "sphinxmermaid",
        ]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

language = 'en_US'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown',
}
myst_heading_anchors = 4
myst_enable_extensions = [
        "colon_fence",
        "tasklist",
]
suppress_warnings = ["myst.header", "myst.xref_missing"]
html_css_files = [
        "custom.css"
        ]
todo_include_todos = True

sys.path.insert(0,
                str(Path(__file__).parent.parent.joinpath(
                    "example").absolute()))
os.environ["DJANGO_SETTINGS_MODULE"] = "example.settings"
django.setup()
