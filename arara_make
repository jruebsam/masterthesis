BUILD_DIR=build
LATEXMK_OPTIONS= --pdf --output-directory=${BUILD_DIR} --pdflatex="pdflatex -interaction=nonstopmode"

.PHONY: all main clean

all: thesis

thesis: | ${BUILD_DIR}
	python build.py b

clean:
	rm -rf ${BUILD_DIR}

${BUILD_DIR}:
	mkdir -p ${BUILD_DIR}
