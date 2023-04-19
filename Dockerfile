FROM postgres:latest

ENV POSTGRES_USER admin
ENV POSTGRES_PASSWORD pass
ENV POSTGRES_DB alpha

COPY schema.sql /docker-entrypoint-initdb.d/
