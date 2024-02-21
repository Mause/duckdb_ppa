# DUCKDB

DuckDB is an SQL OLAP management system

## USAGE

FILENAME is the name of an DuckDB database. A new database is created
if the file does not previously exist.

Usage: duckdb [OPTIONS] FILENAME [SQL]

## OPTIONS

- `-append`: append the database to the end of the file
- `-ascii`: set output mode to 'ascii'
- `-bail`: stop after hitting an error
- `-batch`: force batch I/O
- `-box`: set output mode to 'box'
- `-column`: set output mode to 'column'
- `-cmd COMMAND`: run "COMMAND" before reading stdin
- `-c COMMAND`: run "COMMAND" and exit
- `-csv`: set output mode to 'csv'
- `-echo`: print commands before execution
- `-init FILENAME`: read/process named file
- `-[no]header`: turn headers on or off
- `-help`: show this message
- `-html`: set output mode to HTML
- `-interactive`: force interactive I/O
- `-json`: set output mode to 'json'
- `-line`: set output mode to 'line'
- `-list`: set output mode to 'list'
- `-markdown`: set output mode to 'markdown'
- `-newline SEP`: set output row separator. Default: '\n'
- `-nofollow`: refuse to open symbolic links to database files
- `-no-stdin`: exit after processing options instead of reading stdin
- `-nullvalue TEXT`: set text string for NULL values. Default ''
- `-quote`: set output mode to 'quote'
- `-readonly`: open the database read-only
- `-s COMMAND`: run "COMMAND" and exit
- `-separator SEP`: set output column separator. Default: '\|'
- `-stats`: print memory stats before each finalize
- `-table`: set output mode to 'table'
- `-unredacted`: allow printing unredacted secrets
- `-unsigned`: allow loading of unsigned extensions
- `-version`: show DuckDB version
