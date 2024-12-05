.PHONY: setup tests clean

all: 
	@echo "Usage: make [command]"
	@echo "Commands:"
	@echo "  setup: Install dependencies"
	@echo "  tests: Run tests"
	@echo "  clean: Remove temporary files"
	@echo "  corrector: Run corrector"
	@echo "  compressor: Run compressor"
	@echo "  latex: Compile latex"
	@echo "  pseudo-code: Generate pseudo-code for a given python file"
	@echo "  wordgame: Run wordgame"

corrector:
	@python3 src/corrector/convolutional.py
	$(MAKE) -s clean

compressor:
	@python3 src/compressor/huffman.py
	$(MAKE) -s clean

latex:
	pdftex --etex --output-format=pdf --output-directory=./ assets/rapport/main.tex
	$(MAKE) -s clean

setup:
	export PYTHONPATH=$PYTHONPATH:`pwd`
	@pip3 install -r requirements.txt
	@python3 setup.py install

tests:
	@python3 tests/*.py
	$(MAKE) -s clean

pseudo-code:
	@python3 python2pseudo.py
	$(MAKE) -s clean

wordgame:
	@python3 src/wordgame/wordle.py
	$(MAKE) -s clean

clean:
	@rm -rf src/*/__pycache__/ .pytest_cache/ .vscode/ *toc *synctex.gz *.dvi *.aux *.log *.pdf