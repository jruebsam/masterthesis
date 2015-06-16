BUILD_DIR=build
LATEXMK_OPTIONS=--bibtex --pdf --output-directory=${BUILD_DIR} --pdflatex="pdflatex -interaction=nonstopmode"

.PHONY: all main clean

all: thesis

thesis: | ${BUILD_DIR}
	latexmk ${LATEXMK_OPTIONS} thesis.tex

clean:
	rm -rf ${BUILD_DIR}

${BUILD_DIR}:
	mkdir -p ${BUILD_DIR}
