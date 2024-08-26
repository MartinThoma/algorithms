pg_dump: warning: there are circular foreign-key constraints among these tables:
pg_dump: detail: tablea
pg_dump: detail: tableb
pg_dump: hint: You might not be able to restore the dump without using --disable-triggers or temporarily dropping the constraints.
pg_dump: hint: Consider using a full dump instead of a --data-only dump to avoid this problem.
--
-- PostgreSQL database dump
--

-- Dumped from database version 15.8 (Debian 15.8-1.pgdg120+1)
-- Dumped by pg_dump version 15.8 (Debian 15.8-1.pgdg120+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Data for Name: tablea; Type: TABLE DATA; Schema: public; Owner: myuser
--

COPY public.tablea (id, name, table_b_id) FROM stdin;
1	A1	1
\.


--
-- Data for Name: tableb; Type: TABLE DATA; Schema: public; Owner: myuser
--

COPY public.tableb (id, description, table_a_id) FROM stdin;
1	B1	1
\.


--
-- PostgreSQL database dump complete
--

