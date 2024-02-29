# DuckDB PPA

This is an unofficial and unsupported PPA for the duckdb CLI and shared library (+headers).
Right now, only `jammy` is configured and uploaded.

```sh
sudo add-apt-repository ppa:mause-me/duckdb
sudo apt update
sudo apt install duckdb libduckdb libduckdb-dev
```

You can also see more details on [launchpad](https://launchpad.net/~mause-me/+archive/ubuntu/duckdb/)

## Current issues

I'm currently working to resolve the following errors and warnings:

```
E: duckdb: extended-description-is-empty
E: libduckdb: extended-description-is-empty
E: libduckdb-dev: extended-description-is-empty
E: libduckdb: lacks-ldconfig-trigger usr/lib/libduckdb.so
W: duckdb-dbgsym: elf-error In program headers: Unable to find program interpreter name [usr/lib/debug/.build-id/67/0ab54fa42c73c4af46a4794ac1ee7617cfa8d8.debug]
W: libduckdb: lacks-unversioned-link-to-shared-library usr/lib/libduckdb.so usr/lib/libduckdb.so
W: libduckdb: shared-library-lacks-version usr/lib/libduckdb.so libduckdb.so
```
