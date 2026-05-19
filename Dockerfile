FROM apache/superset:latest

# Pindah sementara ke user root untuk memiliki hak akses instalasi global
USER root

# Instal driver DuckDB secara permanen ke dalam sistem internal
RUN pip install --no-cache-dir duckdb duckdb-engine

# Kembalikan hak akses ke user superset demi keamanan data
USER superset