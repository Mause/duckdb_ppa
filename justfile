FOLDER := "duckdb-{{DUCKDB_VERSION}}"

all:
	@echo No.

clean DUCKDB_VERSION:
	rm -f duckdb_{{DUCKDB_VERSION}}-*
	rm -f duckdb_{{DUCKDB_VERSION}}.orig.tar.gz
	rm -f '<project>-{{DUCKDB_VERSION}}.tar.gz'
	find ./{{FOLDER}}/* -maxdepth 0 | grep -v debian | grep -v '.pc' | xargs rm -rf

setup DUCKDB_VERSION:
	uscan --force-download --debug || echo "uscan failed"
	tar xf duckdb_{{DUCKDB_VERSION}}.orig.tar.gz

bump DUCKDB_VERSION:
	git add -p
	cd {{FOLDER}} && dch --distribution jammy --upstream
	git add {{FOLDER}}/debian/changelog
	cd {{FOLDER}} && debcommit


docs:
	mkdir -p duckdb_ppa/doc/man
	ronn --roff duckdb.1.md --output duckdb_ppa/doc/man/ --organization "DuckDB Labs" --manual "User Commands"

deb DUCKDB_VERSION:
	cd {{FOLDER}} && dpkg-buildpackage -us -uc

source_deb DUCKDB_VERSION:
	cd {{FOLDER}} && debuild -S -sa
