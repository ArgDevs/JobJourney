CREATE USER job_journey WITH CREATEDB SUPERUSER PASSWORD 'password';
ALTER ROLE job_journey SET client_encoding TO 'utf8';
ALTER ROLE job_journey SET default_transaction_isolation TO 'read committed';
ALTER ROLE job_journey SET timezone TO 'UTC';

CREATE DATABASE job_journey_local ENCODING 'utf8' OWNER job_journey;
