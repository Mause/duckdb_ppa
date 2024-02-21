DUCKDB_VERSION = 0.10.0
FOLDER = duckdb-$(DUCKDB_VERSION)

.PHONY: all bump docs deb source_deb setup

all:
	@echo No.

setup:
	uscan --force-download --debug || echo "uscan failed"
	tar xvf duckdb_$(DUCKDB_VERSION).orig.tar.gz

bump:
	git add -p
	cd $(FOLDER) && dch --distribution jammy --upstream
	git add $(FOLDER)/debian/changelog
	cd $(FOLDER) && debcommit

doc/man/duckdb.1: duckdb.1.md
	ronn --roff --html duckdb.1.md --output $(FOLDER)/doc/man/ --organization "DuckDB Labs"

docs: doc/man/duckdb.1

deb:
	dpkg-buildpackage -us -uc -b

source_deb:
	cd $(FOLDER) && debuild -S -sa
