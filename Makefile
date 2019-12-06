doc: README.md

README.md: doc/static-discharge.tex
	pandoc -f latex -t markdown-pipe_tables-simple_tables -o README.md doc/static-discharge.tex

all: doc

clean:
	rm README.md
