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
W: duckdb-dbgsym: elf-error In program headers: Unable to find program interpreter name [usr/lib/debug/.build-id/fe/4c3e6d151417731b83252ba2ef47ad06438b38.debug]
```
