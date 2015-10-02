# -*- coding: utf-8 -*-
#
# nfcpy documentation build configuration file, created by
# sphinx-quickstart on Mon Sep 19 18:10:55 2011.
#
# This file is execfile()d with the current directory set to its containing dir.
#
# Note that not all possible configuration values are present in this
# autogenerated file.
#
# All configuration values have a default; values that are commented out
# serve to show the default.

import sys, os
sys.path.insert(0, os.path.abspath('../'))
import nfc

# -- General configuration -----------------------------------------------------
extensions = ['sphinx.ext.autodoc']
templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'

# General information about the project.
project = u'nfcpy'
copyright = u'2009-2014, Stephen Tiedemann'
version = nfc.__version__
release = version
exclude_patterns = ['_build', '.#*', 'topics/.#*', 'examples/.#*']
pygments_style = 'sphinx'

# -- Options for HTML output ---------------------------------------------------

# on_rtd is whether we are on readthedocs.org
on_rtd = os.environ.get('READTHEDOCS', None) == 'True'

if not on_rtd:  # only import and set the theme if we're building docs locally
    html_theme = "sphinx_rtd_theme"
    html_theme_path = ["_themes", ]
    #try:
    #    import sphinx_rtd_theme
    #    html_theme = "sphinx_rtd_theme"
    #    html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]
    #    RTD_NEW_THEME = True
    #except ImportError:
    #    html_theme = 'nature'

html_title = ' '.join([project, version, "documentation"])
html_short_title = ' '.join([project, version])
html_logo = "images/nfcpy-logo-64x64.png"
html_favicon = "images/nfcpy-logo-32x32.ico"
html_static_path = ['_static']
html_last_updated_fmt = '%b %d, %Y'
html_show_sourcelink = True
htmlhelp_basename = 'nfcpydoc'

# -- Options for LaTeX output --------------------------------------------------

# The paper size ('letter' or 'a4').
#latex_paper_size = 'letter'

# The font size ('10pt', '11pt' or '12pt').
#latex_font_size = '10pt'

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title, author, documentclass [howto/manual]).
latex_documents = [
  ('index', 'nfcpy.tex', u'nfcpy documentation',
   u'Stephen Tiedemann', 'manual'),
]

# The name of an image file (relative to this directory) to place at the top of
# the title page.
#latex_logo = None

# For "manual" documents, if this is true, then toplevel headings are parts,
# not chapters.
#latex_use_parts = False

# If true, show page references after internal links.
#latex_show_pagerefs = False

# If true, show URL addresses after external links.
#latex_show_urls = False

# Additional stuff for the LaTeX preamble.
#latex_preamble = ''

# Documents to append as an appendix to all manuals.
#latex_appendices = []

# If false, no module index is generated.
#latex_domain_indices = True

autodoc_member_order = 'bysource'
