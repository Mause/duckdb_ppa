DUCKDB_VERSION = 1.0.0
FOLDER = duckdb-$(DUCKDB_VERSION)

.PHONY: all bump docs deb source_deb setup

all: clean setup deb
	@echo Built.

clean:
	rm -f duckdb_$(DUCKDB_VERSION)-*
	rm -f duckdb_$(DUCKDB_VERSION).orig.tar.gz
	rm -f '<project>-$(DUCKDB_VERSION).tar.gz'
	find ./$(FOLDER)/* -maxdepth 0 | grep -v debian | grep -v '.pc' | xargs rm -rf

setup:
	uscan --force-download --debug || echo "uscan failed"
	tar xf duckdb_$(DUCKDB_VERSION).orig.tar.gz

bump:
	git add -p
	cd $(FOLDER) && dch --distribution jammy --upstream
	git add $(FOLDER)/debian/changelog
	cd $(FOLDER) && debcommit

doc/man/duckdb.1: duckdb.1.md
	mkdir -p $(FOLDER)/doc/man
	ronn --roff duckdb.1.md --output $(FOLDER)/doc/man/ --organization "DuckDB Labs" --manual "User Commands"

docs: doc/man/duckdb.1


deb:
	cd $(FOLDER) && dpkg-buildpackage -us -uc --sign-key=0x981A37FD852376FA

source_deb:
	cd $(FOLDER) && debuild -S -sa --sign-key=0x981A37FD852376FA
