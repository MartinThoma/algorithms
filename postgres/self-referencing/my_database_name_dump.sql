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

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: tablea; Type: TABLE; Schema: public; Owner: myuser
--

CREATE TABLE public.tablea (
    id integer NOT NULL,
    name character varying(100),
    table_b_id integer NOT NULL
);


ALTER TABLE public.tablea OWNER TO myuser;

--
-- Name: tableb; Type: TABLE; Schema: public; Owner: myuser
--

CREATE TABLE public.tableb (
    id integer NOT NULL,
    description character varying(100),
    table_a_id integer NOT NULL
);


ALTER TABLE public.tableb OWNER TO myuser;

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
-- Name: tablea tablea_pkey; Type: CONSTRAINT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.tablea
    ADD CONSTRAINT tablea_pkey PRIMARY KEY (id);


--
-- Name: tableb tableb_pkey; Type: CONSTRAINT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.tableb
    ADD CONSTRAINT tableb_pkey PRIMARY KEY (id);


--
-- Name: tableb fk_table_a; Type: FK CONSTRAINT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.tableb
    ADD CONSTRAINT fk_table_a FOREIGN KEY (table_a_id) REFERENCES public.tablea(id);


--
-- Name: tablea fk_table_b; Type: FK CONSTRAINT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.tablea
    ADD CONSTRAINT fk_table_b FOREIGN KEY (table_b_id) REFERENCES public.tableb(id);


--
-- PostgreSQL database dump complete
--

