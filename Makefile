.PHONY: all bump docs deb


all:
	@echo No.

bump:
	git add -p
	dch -D jammy
	git add -p
	debcommit


doc/man/duckdb.1: doc/man/duckdb.1.md
	ronn --roff doc/man/duckdb.1.md --organization "DuckDB Labs"


docs: doc/man/duckdb.1



deb:
	dpkg-buildpackage -us -uc -b
	# debuild -S -sa

