.PHONY: all bump docs deb


all:
	@echo No.

bump:
	git add -p
	cd duckdb_ppa && dch -D jammy
	git add -p
	cd duckdb_ppa && debcommit


doc/man/duckdb.1: duckdb.1.md
	ronn --roff --html duckdb.1.md --output duckdb-0.10.0/doc/man/ --organization "DuckDB Labs"


docs: doc/man/duckdb.1



deb:
	dpkg-buildpackage -us -uc -b
	# debuild -S -sa

