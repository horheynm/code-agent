get_edited_python_files = $(shell git status --porcelain | awk '{print $$2}' | grep -E '.*\.(py)$$')

build:
	python3 setup.py sdist bdist_wheel

test:
	python -m pytest  -s -v ./tests/

style:
	@edited_files=$(get_edited_python_files); \
	if [ -n "$$edited_files" ]; then \
		echo "Running black on edited python files..."; \
		black $$edited_files; \
		echo "Running ruff on edited python files..."; \
		ruff check $$edited_files; \
	else \
		echo "No python files have been edited."; \
	fi

.PHONY: build style test
