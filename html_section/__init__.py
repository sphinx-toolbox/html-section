#!/usr/bin/env python3
#
#  __init__.py
"""
Sphinx extension to hide section headers with non-HTML builders.
"""
# Based on https://github.com/sphinx-doc/sphinx/blob/3.x/sphinx/writers/latex.py
#
# Copyright (c) 2007-2021 by the Sphinx team.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
# * Redistributions of source code must retain the above copyright
#   notice, this list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright
#   notice, this list of conditions and the following disclaimer in the
#   documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

# stdlib
from typing import Any, Dict, List, Set, Type, cast

# 3rd party
import sphinx.transforms
from docutils import nodes
from sphinx import addnodes
from sphinx.application import Sphinx
from sphinx.builders import Builder
from sphinx.environment import BuildEnvironment
from sphinx.locale import __
from sphinx.util import logging
from sphinx.util.docutils import SphinxDirective
from sphinx.util.nodes import clean_astext
from sphinx.writers.latex import LaTeXTranslator

__author__: str = "Dominic Davis-Foster"
__copyright__: str = "2021 Dominic Davis-Foster"
__license__: str = "BSD License"
__version__: str = "0.3.0"
__email__: str = "dominic@davis-foster.co.uk"

__all__ = [
		"html_section_indicator",
		"HTMLSectionDirective",
		"RemoveHTMLOnlySections",
		"phantom_section_indicator",
		"PhantomSectionDirective",
		"RemovePhantomSections",
		"visit_title",
		"depart_title",
		"setup",
		]

logger = logging.getLogger(__name__)


class _BuildEnvironment(BuildEnvironment):
	html_only_node_docnames: Set[str]
	phantom_node_docnames: Set[str]
	latex_only_node_docnames: Set[str]


def _traverse(node: nodes.Node, condition: Type[nodes.Node]) -> List[nodes.Node]:
	# node.findall is available, otherwise node.traverse
	if hasattr(node, "findall"):
		return list(node.findall(condition))
	else:
		return node.traverse(condition)


def visit_title(translator: LaTeXTranslator, node: nodes.title) -> None:
	"""
	Visit a :class:`docutils.nodes.title` node.

	:param translator:
	:param node: The node itself.
	"""

	if isinstance(node.parent, addnodes.seealso):  # pragma: no cover
		# the environment already handles this
		raise nodes.SkipNode

	elif isinstance(node.parent, nodes.section):
		if translator.this_is_the_title:
			if len(node.children) != 1 and not isinstance(node.children[0], nodes.Text):
				logger.warning(__("document title is not a single Text node"), location=node)
			if not translator.elements["title"]:
				# text needs to be escaped since it is inserted into
				# the output literally
				translator.elements["title"] = translator.escape(node.astext())
			translator.this_is_the_title = 0
			raise nodes.SkipNode

		# This is all from the original visit_title function
		else:  # pragma: no cover

			short = ''
			if _traverse(node, nodes.image):
				short = f"[{translator.escape(' '.join(clean_astext(node).split()))}]"

			try:
				translator.body.append(f"\\{translator.sectionnames[translator.sectionlevel]}{short}{{")
			except IndexError:
				# just use "subparagraph", it's not numbered anyway
				translator.body.append(f"\\{translator.sectionnames[-1]}{short}{{")
			# breakpoint()
			translator.context.append(f"}}\n{translator.hypertarget_to(node.parent)}")

	# This is all from the original visit_title function
	elif isinstance(node.parent, nodes.topic):  # pragma: no cover
		translator.body.append(r"\sphinxstyletopictitle{")
		translator.context.append('}\n')
	elif isinstance(node.parent, nodes.sidebar):  # pragma: no cover
		translator.body.append(r"\sphinxstylesidebartitle{")
		translator.context.append('}\n')
	elif isinstance(node.parent, nodes.Admonition):  # pragma: no cover
		translator.body.append('{')
		translator.context.append('}\n')
	elif isinstance(node.parent, nodes.table):  # pragma: no cover
		# Redirect body output until title is finished.
		translator.pushbody([])
	else:  # pragma: no cover
		logger.warning(
				__("encountered title node not in section, topic, table, admonition or sidebar"),
				location=node,
				)
		translator.body.append("\\sphinxstyleothertitle{")
		translator.context.append('}\n')

	translator.in_title = 1


def depart_title(
		translator: LaTeXTranslator,
		node: nodes.title,
		) -> None:  # pragma: no cover
	"""
	Depart a :class:`docutils.nodes.title` node.

	:param translator:
	:param node: The node itself.
	"""

	translator.in_title = 0
	if isinstance(node.parent, nodes.table):
		assert translator.table is not None
		translator.table.caption = translator.popbody()
	else:
		translator.body.append(translator.context.pop())


class html_section_indicator(nodes.paragraph):
	"""
	Docutils node to mark sections as being HTML only.
	"""


class HTMLSectionDirective(SphinxDirective):
	"""
	Sphinx directive for marking a section as being HTML-only.
	"""

	def run(self) -> List[nodes.Node]:  # noqa: D102
		return [html_section_indicator()]


class RemoveHTMLOnlySections(sphinx.transforms.SphinxTransform):
	"""
	Sphinx transform to mark the node, its parent and siblings as being HTML-only.
	"""

	default_priority = 999

	def apply(self, **kwargs) -> None:  # noqa: D102
		env = cast(_BuildEnvironment, self.env)

		if not hasattr(env, "html_only_node_docnames"):
			env.html_only_node_docnames = set()

		if self.app.builder.format.lower() == "html":
			return

		for node in _traverse(self.document, html_section_indicator):
			assert node.parent is not None
			parent = cast(nodes.Element, node.parent)
			env.html_only_node_docnames.add(env.docname)
			parent.replace_self(parent.children[parent.children.index(node):])


class phantom_section_indicator(nodes.paragraph):
	"""
	Docutils node to mark a section as being a phantom section.
	"""


class PhantomSectionDirective(SphinxDirective):
	"""
	Sphinx directive for marking a section as being a phantom section.
	"""

	def run(self) -> List[nodes.Node]:  # noqa: D102
		return [phantom_section_indicator()]


class RemovePhantomSections(sphinx.transforms.SphinxTransform):
	"""
	Sphinx transform to mark the node, its parent and siblings as being a phantom section.
	"""

	default_priority = 999

	def apply(self, **kwargs) -> None:  # noqa: D102
		env = cast(_BuildEnvironment, self.env)

		if not hasattr(env, "phantom_node_docnames"):
			env.phantom_node_docnames = set()

		for node in _traverse(self.document, phantom_section_indicator):
			assert node.parent is not None
			parent = cast(nodes.Element, node.parent)
			env.phantom_node_docnames.add(env.docname)
			parent.replace_self(parent.children[parent.children.index(node):])


class latex_section_indicator(nodes.paragraph):
	"""
	Docutils node to mark sections as being HTML only.

	.. versionadded:: 0.2.0
	"""


class LaTeXSectionDirective(SphinxDirective):
	"""
	Sphinx directive for marking a section as being LaTeX-only.

	.. versionadded:: 0.2.0
	"""

	def run(self) -> List[nodes.Node]:
		return [latex_section_indicator()]


class RemoveLaTeXOnlySections(sphinx.transforms.SphinxTransform):
	"""
	Sphinx transform to mark the node, its parent and siblings as being LaTeX-only.

	.. versionadded:: 0.2.0
	"""

	default_priority = 999

	def apply(self, **kwargs) -> None:
		env = cast(_BuildEnvironment, self.env)

		if not hasattr(env, "latex_only_node_docnames"):
			env.latex_only_node_docnames = set()

		if cast(Builder, self.app.builder).format.lower() == "latex":
			return

		for node in _traverse(self.document, latex_section_indicator):
			assert node.parent is not None
			parent = cast(nodes.Element, node.parent)
			env.latex_only_node_docnames.add(env.docname)
			parent.replace_self(parent.children[parent.children.index(node):])


def purge_outdated(
		app: Sphinx,
		env: BuildEnvironment,
		added: List[str],
		changed: List[str],
		removed: List[str],
		) -> List[str]:
	return [
			*getattr(env, "html_only_node_docnames", []),
			*getattr(env, "phantom_node_docnames", []),
			*getattr(env, "latex_only_node_docnames", []),
			]


def setup(app: Sphinx) -> Dict[str, Any]:
	"""
	Setup Sphinx Extension.

	:param app:
	"""

	app.add_directive("html-section", HTMLSectionDirective)
	app.add_directive("phantom-section", PhantomSectionDirective)
	app.add_directive("latex-section", LaTeXSectionDirective)

	app.add_transform(RemoveHTMLOnlySections)
	app.add_transform(RemovePhantomSections)
	app.add_transform(RemoveLaTeXOnlySections)

	app.add_node(nodes.title, override=True, latex=(visit_title, depart_title))
	app.connect("env-get-outdated", purge_outdated)

	return {"version": __version__}
