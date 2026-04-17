SHELL := /bin/bash

sphinx:
				@ . make_docs.sh

ghpages:
				rm -R -f docs_temp && \
				cp -r docs/ docs_temp/ && \
				git checkout gh-pages && \
				rm -R -f docs/ && \
				cp -r docs_temp/ docs/ && \
				rm -R -f docs_temp/ && \
				git add -u && \
				git add -A && \
				PRE_COMMIT_ALLOW_NO_CONFIG=1 git commit -m "Updated generated Sphinx documentation"
