# CLAUDE.md

deckbridge is a python package designed to create customizable professional presentations that can be exported to common formats (PowerPoint or Google Slides).
This file provides guidance to Claude Code when working with this repository.

## Behavioral Directives
- **Response Complexity:** Keep responses concise and check-back in frequently.
- **Clarity & Confidence:** If you aren't sure what to do, ask me for clarification.
- **Thinking Limits:** Limit extended thinking to a concise budget (e.g., maximum 2,000 thinking tokens) to prevent over-analysis on minor code changes.
- **Task Execution:** Avoid unnecessary deliberation and proceed directly to code planning. 

## Common Development Commands
1. **Testing**
   ```bash
   pytest --cov=src -vv -ra --cov-report=html --verbose --cov-fail-under=80
   ```
2. **Linting**  
   ```bash
   # Run all configured linters (ruff, mypy, isort, pylint)
   # Use specific commands from pyproject.toml [tool.ruff], [tool.mypy], etc.
   ```
3. **Code Quality Checks**  
   ```bash
   # Run all QA tools
   pre-commit run --all-tasks
   ```

## Code Architecture Overview
1. **Project Structure**  
   - `src/`: Core application code (primary module namespace)
   - `tests/`: Test suite with pytest configuration
   - `notebooks/`: Experimental/interactive code notebooks
   - `docs/`: Documentation built with Sphinx/Furo
   - `dist/`: Distribution packages

2. **Key Files**  
   - `pyproject.toml`: Build system configuration (setuptools, dependencies)
   - `README.md`: Project documentation and setup instructions
   - `changelog.md`: Release history
   - `version.py`: Version tracking implementation

3. **Development Workflow**  
   - Uses `pre-commit` hooks for automated linting
   - Versioning managed via `versioneer.py`
   - Testing includes coverage reports and mypy static analysis
   - Documentation generation via `make_docs.sh`

4. **Dependencies**  
   - Primary dependencies in `requirements.txt`
   - Optional packages defined in `pyproject.toml` [project.optional-dependencies]

## Development Tips
- Maintain code quality with enforced ruff rules (line length: 140 chars)
- Test coverage must exceed 80% threshold
- Documentation should follow Google convention for docstrings

This file captures project-specific details rather than generic practices, focusing on the actual configuration found in the repository.
