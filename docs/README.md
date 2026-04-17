# Documentation Pages

Build with Sphinx.
The assumption of the default setup are that Markdown will be used in all locations.
This package is set up to use [MyST Parser](https://myst-parser.readthedocs.io/en/latest/index.html), which provides a Markdown equivalent of reStructuredText syntax.
Anything that you can do with RST, you can do with MyST.

That doesn't mean you can't use RST!
You can use either or both and all links and cross-doc references will work.

## External link checking
Sphinx can automatically check for any broken external links in your documentation using requests.

1. Run ``make linkcheck`` from this directory (``/docs/``)
2. The results will be displayed and saved to ``/docs/output.txt``

## Generating Documentation
You need to `pip install` the dev requirements:
```
pip install -e .[dev]
```
To update the documentation, from the root directory, run:
```
make sphinx
```
This will automatically regenerate the api documentation using `sphinx-apidoc`.
The rendered documentation will be stored in the `/docs/` directory.
The GitHub pages sits on the `gh-pages` branch.

To push the documentation changes to the `gh-pages` branch:
```
make ghpages && git push origin gh-pages
```
Note about documentation: The [Numpy and Google style docstrings](https://www.sphinx-doc.org/) are activated by default.
Just make sure Sphinx 1.3 or above is installed.
