doc: README.md

README.md: doc/static-discharge.tex
	pandoc -i doc/static-discharge.tex -o README.md
