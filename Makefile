.PHONY: all bump docs deb source_deb setup


all:
	@echo No.


setup:
	uscan --force-download --debug || echo "uscan failed"
	tar xvf duckdb_0.10.0.orig.tar.gz


bump:
	git add -p
	cd duckdb-0.10.0 && dch --distribution jammy --upstream
	git add duckdb-0.10.0/debian/changelog
	cd duckdb-0.10.0 && debcommit


doc/man/duckdb.1: duckdb.1.md
	ronn --roff --html duckdb.1.md --output duckdb-0.10.0/doc/man/ --organization "DuckDB Labs"


docs: doc/man/duckdb.1



deb:
	dpkg-buildpackage -us -uc -b


source_deb:
	cd duckdb-0.10.0 && debuild -S -sa

