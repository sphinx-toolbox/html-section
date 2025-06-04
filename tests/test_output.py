# stdlib
import shutil
from typing import Dict, List, cast

# 3rd party
import pytest
from bs4 import BeautifulSoup
from domdf_python_tools.paths import PathPlus
from domdf_python_tools.stringlist import StringList
from sphinx.application import Sphinx
from sphinx.builders import Builder
from sphinx_toolbox.testing import HTMLRegressionFixture, LaTeXRegressionFixture


@pytest.fixture()
def doc_root(tmp_pathplus: PathPlus) -> None:
	doc_root = tmp_pathplus.parent / "test-html-section"
	doc_root.maybe_make()
	(doc_root / "conf.py").write_clean("extensions = ['html_section']\nproject='Python'\nauthor='unknown'")

	shutil.copy2(PathPlus(__file__).parent / "index.rst", doc_root / "index.rst")

	examples_dir = doc_root / "examples"
	examples_dir.maybe_make()


@pytest.mark.usefixtures("doc_root")
@pytest.mark.sphinx("html", testroot="test-html-section")
def test_build_example(app: Sphinx):
	app.build()
	app.build()


@pytest.mark.usefixtures("doc_root")
@pytest.mark.sphinx("html", testroot="test-html-section")
def test_html_output(app: Sphinx, html_regression: HTMLRegressionFixture):

	assert cast(Builder, app.builder).name.lower() == "html"

	app.build(force_all=True)

	output_file = PathPlus(app.outdir) / "index.html"
	page = BeautifulSoup(output_file.read_text(), "html5lib")

	for div in cast(List[Dict], page.find_all("script")):
		if div.get("src"):
			div["src"] = div["src"].split("?v=")[0]
			print(div["src"])

	for meta in cast(List[Dict], page.find_all("meta")):
		if meta.get("content", '') == "width=device-width, initial-scale=0.9, maximum-scale=0.9":
			meta.extract()  # type: ignore[attr-defined]

	html_regression.check(page, jinja2=True)


@pytest.mark.usefixtures("doc_root")
@pytest.mark.sphinx("latex", testroot="test-html-section")
def test_latex_output(app: Sphinx, latex_regression: LaTeXRegressionFixture):

	assert cast(Builder, app.builder).name.lower() == "latex"

	app.build(force_all=True)

	output_file = PathPlus(app.outdir) / "python.tex"
	latex_regression.check(StringList(output_file.read_lines()), jinja2=True)
