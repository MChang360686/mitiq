# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import datetime
import os
import shutil
import sys

import pybtex.style.formatting
import pybtex.style.formatting.unsrt
import pybtex.style.template
from pybtex.plugin import register_plugin as pybtex_register_plugin

sys.path.insert(0, os.path.abspath("."))
sys.path.insert(0, os.path.abspath(".."))
sys.path.insert(0, os.path.abspath("../../"))

# -- Project information -----------------------------------------------------

project = "Mitiq"
copyright = f"2020 - {datetime.date.today().year} Unitary Foundation"
author = "Tech Team @ Unitary Foundation"

# The full version, including alpha/beta/rc tags
directory_of_this_file = os.path.dirname(os.path.abspath(__file__))
with open(f"{directory_of_this_file}/../../VERSION.txt", "r") as f:
    release = f.read().strip()

sys.path.append(os.path.abspath("sphinxext"))


JUPYTER_EXECUTE_PATH = "../jupyter_execute"


def add_notebook_link_to_context_if_exists(app, pagename, context):
    nb_filename = pagename + ".ipynb"
    nb_exists = os.path.exists(
        os.path.join(app.outdir, JUPYTER_EXECUTE_PATH, nb_filename)
    )
    context["notebook_link"] = nb_filename if nb_exists else None


def handle_page_context(app, pagename, templatename, context, doctree):
    add_notebook_link_to_context_if_exists(app, pagename, context)


def move_notebook_dir(app):
    source_dir = os.path.join(app.outdir, JUPYTER_EXECUTE_PATH)
    target_dir = os.path.join(app.outdir, ".")

    if os.path.exists(source_dir):
        shutil.copytree(source_dir, target_dir, dirs_exist_ok=True)
        print(f"Copied Jupyter execution files to {target_dir}")
    else:
        print("No Jupyter execution files found to copy.")


def handle_build_finished(app, exception):
    if exception is None:  # Only proceed if the build completed successfully
        move_notebook_dir(app)


def setup(app):
    app.connect("html-page-context", handle_page_context)
    app.connect("build-finished", handle_build_finished)


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "myst_nb",
    "sphinx.ext.mathjax",
    "IPython.sphinxext.ipython_console_highlighting",
    "IPython.sphinxext.ipython_directive",
    "matplotlib.sphinxext.plot_directive",
    "sphinx.ext.napoleon",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx_autodoc_typehints",  # after napoleon and autodoc
    "sphinx.ext.todo",
    "sphinx.ext.extlinks",
    "sphinx.ext.intersphinx",
    "sphinx.ext.viewcode",
    "sphinx.ext.ifconfig",
    "sphinxcontrib.bibtex",
    "sphinx_copybutton",
    "nbsphinx",
    "sphinx_gallery.load_style",
    "sphinx_design",
    "sphinx_tags",
]

# to add tags to the documentation tutorials
tags_create_tags = True
tags_output_dir = "tags/"
tags_overview_title = "All tags"
tags_create_badges = True
tags_intro_text = "Tags on this page: "
tags_page_title = "Tags"
tags_page_header = "Pages with this tag: "
tags_index_head = "Tags in the documentation tutorials: "
tags_extension = ["md"]
tags_badge_colors = {
    "zne": "primary",
    "rem": "primary",
    "shadows": "primary",
    "cdr": "primary",
    "pec": "primary",
    "ddd": "primary",
    "calibration": "primary",
    "cirq": "secondary",
    "bqskit": "secondary",
    "braket": "secondary",
    "pennylane": "secondary",
    "qiskit": "secondary",
    "stim": "secondary",
    "qrack": "secondary",
    "qibo": "secondary",
    "ionq": "secondary",
    "basic": "success",
    "intermediate": "success",
    "advanced": "success",
}

# hide primary sidebar from the following pages
html_sidebars = {"apidoc": [], "changelog": [], "bibliography": []}

intersphinx_mapping = {
    "python": ("https://docs.python.org/3.10", None),
    "numpy": ("https://numpy.org/doc/stable/", None),
    "scipy": ("https://docs.scipy.org/doc/scipy/", None),
    # Cirq is no longer using sphinx docs so interlinking is not possible.
    # "cirq": ("https://quantumai.google/cirq", None),
    "pyquil": ("https://pyquil-docs.rigetti.com/en/stable/", None),
    "qiskit": ("https://docs.quantum.ibm.com/api/qiskit/", None),
    # TODO: qutip docs moved and the objects.inv file not yet found
    # "qutip": ("https://qutip.org/docs/latest/", None),
}

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = "en"

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []

# The master toctree document.
master_doc = "index"

# -- Options for myst_parser -------------------------------------------------
# Specifies which of the parsers should handle each file extension.
source_suffix = {
    ".md": "myst-nb",
    ".ipynb": "myst-nb",
}

# Enables extensions to MyST parser that allows for richer markup options.
# For more info on these, see:
# https://myst-parser.readthedocs.io/en/latest/using/syntax-optional.html
myst_enable_extensions = [
    "amsmath",
    "colon_fence",
    "deflist",
    "dollarmath",
    "html_image",
    "smartquotes",
]

myst_heading_anchors = 4

# Tells MyST to treat URIs beginning with these prefixes as external links.
# Links that don't begin with these will be treated as internal cross-links.
myst_url_schemes = ("http", "https", "mailto")

# -- Options for myst_nb -----------------------------------------------------

# How long should Sphinx wait while a notebook is being evaluated before
# quitting.
nb_execution_timeout = 600

# By default, if nothing has changed in the source, a notebook won't be
# re-run for a subsequent docs build.
nb_execution_mode = "cache"
if os.environ.get("DOCS_LITE"):
    print("*** Skipping all notebook execution ***")
    nb_execution_mode = "off"

# If SKIP_PYQUIL is True, do not re-run PyQuil notebooks.
if os.environ.get("SKIP_PYQUIL"):
    print("Skipping PyQuil notebooks execution since SKIP_PYQUIL is set.")
    nb_execution_excludepatterns = ["*pyquil*.ipynb"]

# -- Options for autodoc -----------------------------------------------------
napoleon_google_docstring = True
napoleon_use_ivar = True

autodoc_mock_imports = [
    "pyquil",
]

# autodoc-typehints extension setting
typehints_fully_qualified = False
always_document_param_types = True
set_type_checking_flag = False
typehints_document_rtype = True

# -- Options for Sphinxcontrib-bibtex ----------------------------------------
pybtex.style.formatting.unsrt.date = pybtex.style.template.words(sep="")[
    "(", pybtex.style.template.field("year"), ")"
]
bibtex_bibfiles = ["refs.bib"]

# Links matching with the following regular expressions will be ignored
linkcheck_ignore = [
    r"https://arxiv\.org/.*",
    r"https://doi\.org/.*",
    r"https://link\.aps\.org/doi/.*",
    r"https://www\.sciencedirect\.com/science/article/.*",
    r"https://github.com/unitaryfoundation/mitiq/compare/.*",
    r"https://github.com/unitaryfoundation/mitiq/compare/.*",
    r"https://github.com/unitaryfoundation/mitiq/projects/7",
]

linkcheck_retries = 3

linkcheck_anchors_ignore_for_url = [
    "https://github.com/unitaryfoundation/qrack/blob/main/README.md"
]


class ApsStyle(pybtex.style.formatting.unsrt.Style):
    """Style that mimicks APS journals."""

    def __init__(
        self,
        label_style=None,
        name_style=None,
        sorting_style=None,
        abbreviate_names=True,
        min_crossrefs=2,
        **kwargs,
    ):
        super().__init__(
            label_style=label_style,
            name_style=name_style,
            sorting_style=sorting_style,
            abbreviate_names=abbreviate_names,
            min_crossrefs=min_crossrefs,
            **kwargs,
        )

    def format_title(self, e, which_field, as_sentence=True):
        """Set titles in italics."""
        formatted_title = pybtex.style.template.field(
            which_field, apply_func=lambda text: text.capitalize()
        )
        formatted_title = pybtex.style.template.tag("em")[formatted_title]
        if as_sentence:
            return pybtex.style.template.sentence[formatted_title]
        else:
            return formatted_title

    def get_article_template(self, e):
        volume_and_pages = pybtex.style.template.first_of[
            # volume and pages
            pybtex.style.template.optional[
                pybtex.style.template.join[
                    " ",
                    pybtex.style.template.tag("strong")[
                        pybtex.style.template.field("volume")
                    ],
                    ", ",
                    pybtex.style.template.field(
                        "pages",
                        apply_func=pybtex.style.formatting.unsrt.dashify,
                    ),
                ],
            ],
            # pages only
            pybtex.style.template.words[
                "pages",
                pybtex.style.template.field(
                    "pages", apply_func=pybtex.style.formatting.unsrt.dashify
                ),
            ],
        ]
        template = pybtex.style.formatting.toplevel[
            self.format_names("author"),
            self.format_title(e, "title"),
            pybtex.style.template.sentence(sep=" ")[
                pybtex.style.template.field("journal"),
                pybtex.style.template.optional[volume_and_pages],
                pybtex.style.formatting.unsrt.date,
            ],
            self.format_web_refs(e),
        ]
        return template

    def get_book_template(self, e):
        template = pybtex.style.formatting.toplevel[
            self.format_author_or_editor(e),
            self.format_btitle(e, "title"),
            self.format_volume_and_series(e),
            pybtex.style.template.sentence(sep=" ")[
                pybtex.style.template.sentence(add_period=False)[
                    pybtex.style.template.field("publisher"),
                    pybtex.style.template.optional_field("address"),
                    self.format_edition(e),
                ],
                pybtex.style.formatting.unsrt.date,
            ],
            pybtex.style.template.optional[
                pybtex.style.template.sentence[self.format_isbn(e)]
            ],
            pybtex.style.template.sentence[
                pybtex.style.template.optional_field("note")
            ],
            self.format_web_refs(e),
        ]
        return template

    def get_incollection_template(self, e):
        template = pybtex.style.formatting.toplevel[
            pybtex.style.template.sentence[self.format_names("author")],
            self.format_title(e, "title"),
            pybtex.style.template.words[
                "In",
                pybtex.style.template.sentence[
                    pybtex.style.template.optional[
                        self.format_editor(e, as_sentence=False)
                    ],
                    self.format_btitle(e, "booktitle", as_sentence=False),
                    self.format_volume_and_series(e, as_sentence=False),
                    self.format_chapter_and_pages(e),
                ],
            ],
            pybtex.style.template.sentence(sep=" ")[
                pybtex.style.template.sentence(add_period=False)[
                    pybtex.style.template.optional_field("publisher"),
                    pybtex.style.template.optional_field("address"),
                    self.format_edition(e),
                ],
                pybtex.style.formatting.unsrt.date,
            ],
            self.format_web_refs(e),
        ]
        return template


pybtex_register_plugin("pybtex.style.formatting", "apsstyle", ApsStyle)

# -- Options for other extensions --------------------------------------------
# The name of the Pygments (syntax highlighting) style to use.
pygments_style = "sphinx"

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = False

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "pydata_sphinx_theme"  # 'alabaster', 'sphinx_rtd_theme'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_thumbnails"]

# display logo on top-left of html pages
html_logo = "img/mitiq-logo.png"

html_favicon = "img/mitiq.ico"

# Add extra paths that contain custom files here, relative to this directory.
# These files are copied directly to the root of the documentation.
html_extra_path = ["robots.txt"]

html_theme_options = {
    "icon_links": [
        {
            "name": "Source Repository",
            "url": "https://github.com/unitaryfoundation/mitiq",
            "icon": "fa-brands fa-github",
            "type": "fontawesome",
        }
    ],
    "secondary_sidebar_items": ["page-toc", "sourcelink", "notebook-download"],
    "show_toc_level": 2,
}

myst_update_mathjax = False

nbsphinx_custom_formats = {
    ".mystnb": ["jupytext.reads", {"fmt": "mystnb"}],
}

nbsphinx_execute = "always"

nbsphinx_thumbnails = {
    "examples/qibo-noisy-simulation": "_static/qibo-mitiq.png",
    "examples/hamiltonians": "_static/vqe-cirq-pauli-sum-mitigation-plot.png",
    "examples/braket_mirror_circuit": "_static/mirror-circuits.png",
    "examples/maxcut-demo": "_static/max-cut.png",
    "examples/layerwise-folding": "_static/layerwise.png",
    "examples/cirq-ibmq-backends": "_static/cirq-mitiq-ibmq.png",
    "examples/pennylane-ibmq-backends": "_static/zne-pennylane.png",
    "examples/ibmq-backends": "_static/ibmq-gate-map.png",
    "examples/simple-landscape-cirq": "_static/simple-landscape-cirq.png",
    "examples/simple-landscape-braket": "_static/simple-landscape-braket.png",
    "examples/molecular_hydrogen": "_static/molecular-hydrogen-vqe.png",
    "examples/molecular_hydrogen_pennylane": "_static/mol-h2-vqe-pl.png",
    "examples/vqe-pyquil-demo": "_static/vqe-pyquil-demo.png",
    "examples/pyquil_demo": "_static/pyquil-demo.png",
    "examples/mitiq-paper/*": "_static/mitiq-codeblocks.png",
    "examples/zne-braket-ionq": "_static/zne-braket-ionq.png",
    "examples/bqskit": "_static/bqskit.png",
    "examples/simple-landscape-qiskit": "_static/simple-landscape-qiskit.png",
    "examples/simple-landscape-pennylane": "_static/simple-landscape-pln.png",
    "examples/learning-depolarizing-noise": "_static/learn-depolarizing.png",
    "examples/pec_tutorial": "_static/pec-tutorial.png",
    "examples/scaling": "_static/scaling.png",
    "examples/shadows_tutorial": "_static/shadow-tutorial.png",
    "examples/rshadows_tutorial": "_static/rshadow_protocol.png",
    "examples/ddd_tutorial": "_static/ddd-tutorial.png",
    "examples/ddd_on_ibmq_ghz": "_static/ddd_qiskit_ghz_plot.png",
    "examples/calibration-tutorial": "_static/calibration.png",
    "examples/combine_rem_zne": "_static/combine_rem_zne.png",
    "examples/quantum_simulation_scars_ibmq": "_static/qmbs_ibmq.png",
    "examples/zne_logical_rb_cirq_stim": "_static/mitiq_stim_logo.png",
    "examples/quantum_simulation_1d_ising": "_static/quantum_simulation.png",
    "examples/cdr_qrack": "_static/cdr-qrack.png",
    "examples/loschmidt_echo_revival_zne": "_static/loschmidt_echo_qiskit.png",
    "examples/pt_zne": "_static/pt_zne.png",
    # default images if no thumbnail is specified
    "examples/*": "_static/mitiq-logo.png",
}
