BUILD_DIR=build
CHAPTERS=chapters
LATEXMK_OPTIONS= --pdf --pdflatex="pdflatex -interaction=batchmode"  -jobname=build/thesis

.PHONY: all main clean

all: thesis

thesis: | ${BUILD_DIR}
	latexmk ${LATEXMK_OPTIONS} thesis.tex

clean:
	rm -rf ${BUILD_DIR}

${BUILD_DIR}:
	mkdir -p ${BUILD_DIR}/${CHAPTERS}
