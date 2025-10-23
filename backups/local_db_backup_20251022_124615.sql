--
-- PostgreSQL database dump
--

\restrict fjvq9d8G1kNG8APTjn6xGFOAO5949mB8NcxJH0gx8fWy4xW6sJIOYJPexzTC4Pg

-- Dumped from database version 14.19
-- Dumped by pg_dump version 14.19

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
-- Name: auth_group; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.auth_group (
    id integer NOT NULL,
    name character varying(150) NOT NULL
);


ALTER TABLE public.auth_group OWNER TO admin;

--
-- Name: auth_group_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.auth_group_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_group_id_seq OWNER TO admin;

--
-- Name: auth_group_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.auth_group_id_seq OWNED BY public.auth_group.id;


--
-- Name: auth_group_permissions; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.auth_group_permissions (
    id integer NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_group_permissions OWNER TO admin;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.auth_group_permissions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_group_permissions_id_seq OWNER TO admin;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.auth_group_permissions_id_seq OWNED BY public.auth_group_permissions.id;


--
-- Name: auth_permission; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.auth_permission (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    content_type_id integer NOT NULL,
    codename character varying(100) NOT NULL
);


ALTER TABLE public.auth_permission OWNER TO admin;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.auth_permission_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_permission_id_seq OWNER TO admin;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.auth_permission_id_seq OWNED BY public.auth_permission.id;


--
-- Name: auth_user; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.auth_user (
    id integer NOT NULL,
    password character varying(128) NOT NULL,
    last_login timestamp with time zone,
    is_superuser boolean NOT NULL,
    username character varying(150) NOT NULL,
    first_name character varying(150) NOT NULL,
    last_name character varying(150) NOT NULL,
    email character varying(254) NOT NULL,
    is_staff boolean NOT NULL,
    is_active boolean NOT NULL,
    date_joined timestamp with time zone NOT NULL
);


ALTER TABLE public.auth_user OWNER TO admin;

--
-- Name: auth_user_groups; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.auth_user_groups (
    id integer NOT NULL,
    user_id integer NOT NULL,
    group_id integer NOT NULL
);


ALTER TABLE public.auth_user_groups OWNER TO admin;

--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.auth_user_groups_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_user_groups_id_seq OWNER TO admin;

--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.auth_user_groups_id_seq OWNED BY public.auth_user_groups.id;


--
-- Name: auth_user_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.auth_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_user_id_seq OWNER TO admin;

--
-- Name: auth_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.auth_user_id_seq OWNED BY public.auth_user.id;


--
-- Name: auth_user_user_permissions; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.auth_user_user_permissions (
    id integer NOT NULL,
    user_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_user_user_permissions OWNER TO admin;

--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.auth_user_user_permissions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_user_user_permissions_id_seq OWNER TO admin;

--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.auth_user_user_permissions_id_seq OWNED BY public.auth_user_user_permissions.id;


--
-- Name: authtoken_token; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.authtoken_token (
    key character varying(40) NOT NULL,
    created timestamp with time zone NOT NULL,
    user_id integer NOT NULL
);


ALTER TABLE public.authtoken_token OWNER TO admin;

--
-- Name: django_admin_log; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.django_admin_log (
    id integer NOT NULL,
    action_time timestamp with time zone NOT NULL,
    object_id text,
    object_repr character varying(200) NOT NULL,
    action_flag smallint NOT NULL,
    change_message text NOT NULL,
    content_type_id integer,
    user_id integer NOT NULL,
    CONSTRAINT django_admin_log_action_flag_check CHECK ((action_flag >= 0))
);


ALTER TABLE public.django_admin_log OWNER TO admin;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.django_admin_log_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_admin_log_id_seq OWNER TO admin;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.django_admin_log_id_seq OWNED BY public.django_admin_log.id;


--
-- Name: django_content_type; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.django_content_type (
    id integer NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);


ALTER TABLE public.django_content_type OWNER TO admin;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.django_content_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_content_type_id_seq OWNER TO admin;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.django_content_type_id_seq OWNED BY public.django_content_type.id;


--
-- Name: django_migrations; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.django_migrations (
    id integer NOT NULL,
    app character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);


ALTER TABLE public.django_migrations OWNER TO admin;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.django_migrations_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_migrations_id_seq OWNER TO admin;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.django_migrations_id_seq OWNED BY public.django_migrations.id;


--
-- Name: django_session; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);


ALTER TABLE public.django_session OWNER TO admin;

--
-- Name: trials_app_application; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.trials_app_application (
    id bigint NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    application_number character varying(100) NOT NULL,
    submission_date date NOT NULL,
    applicant character varying(512) NOT NULL,
    applicant_inn_bin character varying(12),
    contact_person_name character varying(255),
    contact_person_phone character varying(50),
    contact_person_email character varying(255),
    maturity_group character varying(3),
    purpose text,
    status character varying(20) NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    created_by_id integer NOT NULL,
    sort_record_id bigint NOT NULL
);


ALTER TABLE public.trials_app_application OWNER TO admin;

--
-- Name: trials_app_application_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.trials_app_application_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.trials_app_application_id_seq OWNER TO admin;

--
-- Name: trials_app_application_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.trials_app_application_id_seq OWNED BY public.trials_app_application.id;


--
-- Name: trials_app_application_target_oblasts; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.trials_app_application_target_oblasts (
    id integer NOT NULL,
    application_id bigint NOT NULL,
    oblast_id bigint NOT NULL,
    status character varying(20) DEFAULT 'planned'::character varying,
    trial_plan_id integer,
    trial_id integer,
    created_at timestamp without time zone DEFAULT now(),
    updated_at timestamp without time zone DEFAULT now(),
    decision_date date,
    decision_justification text,
    decided_by_id integer,
    decision_year integer
);


ALTER TABLE public.trials_app_application_target_oblasts OWNER TO admin;

--
-- Name: trials_app_application_target_oblasts_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.trials_app_application_target_oblasts_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.trials_app_application_target_oblasts_id_seq OWNER TO admin;

--
-- Name: trials_app_application_target_oblasts_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.trials_app_application_target_oblasts_id_seq OWNED BY public.trials_app_application_target_oblasts.id;


--
-- Name: trials_app_applicationdecisionhistory; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.trials_app_applicationdecisionhistory (
    id bigint NOT NULL,
    year integer NOT NULL,
    decision character varying(20) NOT NULL,
    decision_date date NOT NULL,
    decision_justification text,
    average_yield double precision,
    years_tested_total integer NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    application_id bigint NOT NULL,
    decided_by_id integer,
    oblast_id bigint NOT NULL
);


ALTER TABLE public.trials_app_applicationdecisionhistory OWNER TO admin;

--
-- Name: trials_app_applicationdecisionhistory_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.trials_app_applicationdecisionhistory_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.trials_app_applicationdecisionhistory_id_seq OWNER TO admin;

--
-- Name: trials_app_applicationdecisionhistory_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.trials_app_applicationdecisionhistory_id_seq OWNED BY public.trials_app_applicationdecisionhistory.id;


--
-- Name: trials_app_climatezone; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.trials_app_climatezone (
    id bigint NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    name character varying(255) NOT NULL,
    code character varying(50) NOT NULL,
    description text,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL
);


ALTER TABLE public.trials_app_climatezone OWNER TO admin;

--
-- Name: trials_app_climatezone_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.trials_app_climatezone_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.trials_app_climatezone_id_seq OWNER TO admin;

--
-- Name: trials_app_climatezone_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.trials_app_climatezone_id_seq OWNED BY public.trials_app_climatezone.id;


--
-- Name: trials_app_culture; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.trials_app_culture (
    id bigint NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    culture_id integer NOT NULL,
    name character varying(128) NOT NULL,
    code character varying(128),
    synced_at timestamp with time zone,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    group_culture_id bigint
);


ALTER TABLE public.trials_app_culture OWNER TO admin;

--
-- Name: trials_app_culture_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.trials_app_culture_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.trials_app_culture_id_seq OWNER TO admin;

--
-- Name: trials_app_culture_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.trials_app_culture_id_seq OWNED BY public.trials_app_culture.id;


--
-- Name: trials_app_document; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.trials_app_document (
    id bigint NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    title character varying(255) NOT NULL,
    document_type character varying(30) NOT NULL,
    file character varying(100) NOT NULL,
    description text,
    uploaded_at timestamp with time zone NOT NULL,
    is_mandatory boolean NOT NULL,
    application_id bigint,
    trial_id bigint,
    uploaded_by_id integer NOT NULL
);


ALTER TABLE public.trials_app_document OWNER TO admin;

--
-- Name: trials_app_document_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.trials_app_document_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.trials_app_document_id_seq OWNER TO admin;

--
-- Name: trials_app_document_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.trials_app_document_id_seq OWNED BY public.trials_app_document.id;


--
-- Name: trials_app_groupculture; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.trials_app_groupculture (
    id bigint NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    group_culture_id integer NOT NULL,
    name character varying(128) NOT NULL,
    description text NOT NULL,
    code character varying(64),
    synced_at timestamp with time zone,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL
);


ALTER TABLE public.trials_app_groupculture OWNER TO admin;

--
-- Name: trials_app_groupculture_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.trials_app_groupculture_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.trials_app_groupculture_id_seq OWNER TO admin;

--
-- Name: trials_app_groupculture_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.trials_app_groupculture_id_seq OWNED BY public.trials_app_groupculture.id;


--
-- Name: trials_app_indicator; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.trials_app_indicator (
    id bigint NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    code character varying(100) NOT NULL,
    name character varying(255) NOT NULL,
    unit character varying(50),
    description text,
    is_numeric boolean NOT NULL,
    category character varying(20) NOT NULL,
    is_quality boolean NOT NULL,
    sort_order integer NOT NULL,
    is_universal boolean NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    calculation_formula text,
    is_auto_calculated boolean NOT NULL,
    is_recommended boolean NOT NULL,
    is_required boolean NOT NULL,
    validation_rules jsonb NOT NULL
);


ALTER TABLE public.trials_app_indicator OWNER TO admin;

--
-- Name: trials_app_indicator_group_cultures; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.trials_app_indicator_group_cultures (
    id integer NOT NULL,
    indicator_id bigint NOT NULL,
    groupculture_id bigint NOT NULL
);


ALTER TABLE public.trials_app_indicator_group_cultures OWNER TO admin;

--
-- Name: trials_app_indicator_group_cultures_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.trials_app_indicator_group_cultures_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.trials_app_indicator_group_cultures_id_seq OWNER TO admin;

--
-- Name: trials_app_indicator_group_cultures_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.trials_app_indicator_group_cultures_id_seq OWNED BY public.trials_app_indicator_group_cultures.id;


--
-- Name: trials_app_indicator_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.trials_app_indicator_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.trials_app_indicator_id_seq OWNER TO admin;

--
-- Name: trials_app_indicator_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.trials_app_indicator_id_seq OWNED BY public.trials_app_indicator.id;


--
-- Name: trials_app_oblast; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.trials_app_oblast (
    id bigint NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    name character varying(255) NOT NULL,
    code character varying(10) NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL
);


ALTER TABLE public.trials_app_oblast OWNER TO admin;

--
-- Name: trials_app_oblast_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.trials_app_oblast_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.trials_app_oblast_id_seq OWNER TO admin;

--
-- Name: trials_app_oblast_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.trials_app_oblast_id_seq OWNED BY public.trials_app_oblast.id;


--
-- Name: trials_app_originator; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.trials_app_originator (
    id bigint NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    originator_id integer NOT NULL,
    name character varying(512) NOT NULL,
    synced_at timestamp with time zone,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    code integer,
    is_foreign boolean NOT NULL,
    is_nanoc boolean NOT NULL
);


ALTER TABLE public.trials_app_originator OWNER TO admin;

--
-- Name: trials_app_originator_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.trials_app_originator_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.trials_app_originator_id_seq OWNER TO admin;

--
-- Name: trials_app_originator_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.trials_app_originator_id_seq OWNED BY public.trials_app_originator.id;


--
-- Name: trials_app_planneddistribution; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.trials_app_planneddistribution (
    id bigint NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    planting_season character varying(50),
    status character varying(20) NOT NULL,
    year_started integer,
    year_completed integer,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    notes text,
    application_id bigint NOT NULL,
    created_by_id integer NOT NULL,
    region_id bigint NOT NULL,
    trial_type_id bigint
);


ALTER TABLE public.trials_app_planneddistribution OWNER TO admin;

--
-- Name: trials_app_planneddistribution_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.trials_app_planneddistribution_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.trials_app_planneddistribution_id_seq OWNER TO admin;

--
-- Name: trials_app_planneddistribution_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.trials_app_planneddistribution_id_seq OWNED BY public.trials_app_planneddistribution.id;


--
-- Name: trials_app_region; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.trials_app_region (
    id bigint NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    name character varying(255) NOT NULL,
    address text,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    climate_zone_id bigint,
    oblast_id bigint NOT NULL
);


ALTER TABLE public.trials_app_region OWNER TO admin;

--
-- Name: trials_app_region_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.trials_app_region_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.trials_app_region_id_seq OWNER TO admin;

--
-- Name: trials_app_region_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.trials_app_region_id_seq OWNED BY public.trials_app_region.id;


--
-- Name: trials_app_sortoriginator; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.trials_app_sortoriginator (
    id bigint NOT NULL,
    percentage integer NOT NULL,
    originator_id bigint NOT NULL,
    sort_record_id bigint NOT NULL,
    CONSTRAINT trials_app_sortoriginator_percentage_check CHECK ((percentage >= 0))
);


ALTER TABLE public.trials_app_sortoriginator OWNER TO admin;

--
-- Name: trials_app_sortoriginator_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.trials_app_sortoriginator_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.trials_app_sortoriginator_id_seq OWNER TO admin;

--
-- Name: trials_app_sortoriginator_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.trials_app_sortoriginator_id_seq OWNED BY public.trials_app_sortoriginator.id;


--
-- Name: trials_app_sortrecord; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.trials_app_sortrecord (
    id bigint NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    sort_id integer NOT NULL,
    name character varying(255) NOT NULL,
    public_code character varying(128),
    patents_status integer,
    lifestyle integer,
    characteristic integer,
    development_cycle integer,
    applicant character varying(512),
    patent_nis boolean,
    note text,
    trial_notes text,
    synced_at timestamp with time zone,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    culture_id bigint
);


ALTER TABLE public.trials_app_sortrecord OWNER TO admin;

--
-- Name: trials_app_sortrecord_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.trials_app_sortrecord_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.trials_app_sortrecord_id_seq OWNER TO admin;

--
-- Name: trials_app_sortrecord_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.trials_app_sortrecord_id_seq OWNED BY public.trials_app_sortrecord.id;


--
-- Name: trials_app_trial; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.trials_app_trial (
    id bigint NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    area_ha numeric(10,4),
    planting_season character varying(20) NOT NULL,
    agro_background character varying(20),
    growing_conditions character varying(20),
    cultivation_technology character varying(20),
    growing_method character varying(20),
    harvest_timing character varying(20),
    harvest_date date,
    additional_info text,
    status character varying(20) NOT NULL,
    start_date date NOT NULL,
    year integer,
    responsible_person character varying(255),
    laboratory_status character varying(20),
    laboratory_sent_date date,
    laboratory_completed_date date,
    laboratory_sample_weight double precision,
    laboratory_sample_source text,
    laboratory_notes text,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    created_by_id integer NOT NULL,
    culture_id bigint,
    predecessor_culture_id bigint,
    region_id bigint NOT NULL,
    trial_plan_id bigint,
    trial_type_id bigint,
    maturity_group_code character varying(10),
    maturity_group_name character varying(100),
    lsd_095 double precision,
    error_mean double precision,
    accuracy_percent double precision,
    replication_count integer NOT NULL,
    trial_code character varying(50),
    culture_code character varying(50),
    predecessor_code character varying(50),
    responsible_person_title character varying(255),
    approval_date date,
    patents_culture_id integer
);


ALTER TABLE public.trials_app_trial OWNER TO admin;

--
-- Name: trials_app_trial_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.trials_app_trial_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.trials_app_trial_id_seq OWNER TO admin;

--
-- Name: trials_app_trial_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.trials_app_trial_id_seq OWNED BY public.trials_app_trial.id;


--
-- Name: trials_app_trial_indicators; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.trials_app_trial_indicators (
    id integer NOT NULL,
    trial_id bigint NOT NULL,
    indicator_id bigint NOT NULL
);


ALTER TABLE public.trials_app_trial_indicators OWNER TO admin;

--
-- Name: trials_app_trial_indicators_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.trials_app_trial_indicators_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.trials_app_trial_indicators_id_seq OWNER TO admin;

--
-- Name: trials_app_trial_indicators_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.trials_app_trial_indicators_id_seq OWNED BY public.trials_app_trial_indicators.id;


--
-- Name: trials_app_triallaboratoryresult; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.trials_app_triallaboratoryresult (
    id bigint NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    value double precision,
    text_value text,
    analysis_date date,
    sample_weight_kg double precision,
    notes text,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    created_by_id integer NOT NULL,
    indicator_id bigint NOT NULL,
    participant_id bigint,
    trial_id bigint NOT NULL
);


ALTER TABLE public.trials_app_triallaboratoryresult OWNER TO admin;

--
-- Name: trials_app_triallaboratoryresult_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.trials_app_triallaboratoryresult_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.trials_app_triallaboratoryresult_id_seq OWNER TO admin;

--
-- Name: trials_app_triallaboratoryresult_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.trials_app_triallaboratoryresult_id_seq OWNED BY public.trials_app_triallaboratoryresult.id;


--
-- Name: trials_app_trialparticipant; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.trials_app_trialparticipant (
    id bigint NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    statistical_group integer NOT NULL,
    statistical_result integer,
    participant_number integer NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    application_id bigint,
    sort_record_id bigint NOT NULL,
    trial_id bigint NOT NULL,
    maturity_group_code character varying(10)
);


ALTER TABLE public.trials_app_trialparticipant OWNER TO admin;

--
-- Name: trials_app_trialparticipant_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.trials_app_trialparticipant_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.trials_app_trialparticipant_id_seq OWNER TO admin;

--
-- Name: trials_app_trialparticipant_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.trials_app_trialparticipant_id_seq OWNED BY public.trials_app_trialparticipant.id;


--
-- Name: trials_app_trialplan; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.trials_app_trialplan (
    id bigint NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    year integer NOT NULL,
    status character varying(20) NOT NULL,
    participants jsonb NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    created_by_id integer NOT NULL,
    oblast_id bigint NOT NULL,
    trial_type_id bigint,
    total_participants integer NOT NULL
);


ALTER TABLE public.trials_app_trialplan OWNER TO admin;

--
-- Name: trials_app_trialplan_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.trials_app_trialplan_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.trials_app_trialplan_id_seq OWNER TO admin;

--
-- Name: trials_app_trialplan_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.trials_app_trialplan_id_seq OWNED BY public.trials_app_trialplan.id;


--
-- Name: trials_app_trialplanculture; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.trials_app_trialplanculture (
    id bigint NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    created_by_id integer NOT NULL,
    culture_id bigint NOT NULL,
    trial_plan_id bigint NOT NULL
);


ALTER TABLE public.trials_app_trialplanculture OWNER TO admin;

--
-- Name: trials_app_trialplanculture_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.trials_app_trialplanculture_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.trials_app_trialplanculture_id_seq OWNER TO admin;

--
-- Name: trials_app_trialplanculture_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.trials_app_trialplanculture_id_seq OWNED BY public.trials_app_trialplanculture.id;


--
-- Name: trials_app_trialplanculturetrialtype; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.trials_app_trialplanculturetrialtype (
    id bigint NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    created_by_id integer NOT NULL,
    trial_plan_culture_id bigint NOT NULL,
    trial_type_id bigint NOT NULL,
    season character varying(20) NOT NULL
);


ALTER TABLE public.trials_app_trialplanculturetrialtype OWNER TO admin;

--
-- Name: trials_app_trialplanculturetrialtype_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.trials_app_trialplanculturetrialtype_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.trials_app_trialplanculturetrialtype_id_seq OWNER TO admin;

--
-- Name: trials_app_trialplanculturetrialtype_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.trials_app_trialplanculturetrialtype_id_seq OWNED BY public.trials_app_trialplanculturetrialtype.id;


--
-- Name: trials_app_trialplanparticipant; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.trials_app_trialplanparticipant (
    id bigint NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    patents_sort_id integer NOT NULL,
    statistical_group integer NOT NULL,
    seeds_provision character varying(20) NOT NULL,
    participant_number integer NOT NULL,
    maturity_group character varying(10) NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    application_id bigint,
    created_by_id integer NOT NULL,
    culture_trial_type_id bigint NOT NULL
);


ALTER TABLE public.trials_app_trialplanparticipant OWNER TO admin;

--
-- Name: trials_app_trialplanparticipant_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.trials_app_trialplanparticipant_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.trials_app_trialplanparticipant_id_seq OWNER TO admin;

--
-- Name: trials_app_trialplanparticipant_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.trials_app_trialplanparticipant_id_seq OWNED BY public.trials_app_trialplanparticipant.id;


--
-- Name: trials_app_trialplantrial; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.trials_app_trialplantrial (
    id bigint NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    predecessor character varying(50) NOT NULL,
    seeding_rate double precision NOT NULL,
    season character varying(20) NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    created_by_id integer NOT NULL,
    participant_id bigint NOT NULL,
    region_id bigint NOT NULL
);


ALTER TABLE public.trials_app_trialplantrial OWNER TO admin;

--
-- Name: trials_app_trialplantrial_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.trials_app_trialplantrial_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.trials_app_trialplantrial_id_seq OWNER TO admin;

--
-- Name: trials_app_trialplantrial_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.trials_app_trialplantrial_id_seq OWNED BY public.trials_app_trialplantrial.id;


--
-- Name: trials_app_trialresult; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.trials_app_trialresult (
    id bigint NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    value double precision,
    text_value text,
    measurement_date date,
    notes text,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    created_by_id integer NOT NULL,
    indicator_id bigint NOT NULL,
    participant_id bigint,
    sort_record_id bigint,
    trial_id bigint,
    plot_1 double precision,
    plot_2 double precision,
    plot_3 double precision,
    plot_4 double precision,
    is_rejected boolean NOT NULL,
    rejection_reason text,
    is_restored boolean NOT NULL
);


ALTER TABLE public.trials_app_trialresult OWNER TO admin;

--
-- Name: trials_app_trialresult_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.trials_app_trialresult_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.trials_app_trialresult_id_seq OWNER TO admin;

--
-- Name: trials_app_trialresult_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.trials_app_trialresult_id_seq OWNED BY public.trials_app_trialresult.id;


--
-- Name: trials_app_trialtype; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.trials_app_trialtype (
    id bigint NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    code character varying(50) NOT NULL,
    name character varying(255) NOT NULL,
    name_full character varying(512) NOT NULL,
    category character varying(20) NOT NULL,
    description text,
    requires_area boolean NOT NULL,
    requires_standard boolean NOT NULL,
    default_area_ha numeric(10,4),
    sort_order integer NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL
);


ALTER TABLE public.trials_app_trialtype OWNER TO admin;

--
-- Name: trials_app_trialtype_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.trials_app_trialtype_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.trials_app_trialtype_id_seq OWNER TO admin;

--
-- Name: trials_app_trialtype_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.trials_app_trialtype_id_seq OWNED BY public.trials_app_trialtype.id;


--
-- Name: auth_group id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auth_group ALTER COLUMN id SET DEFAULT nextval('public.auth_group_id_seq'::regclass);


--
-- Name: auth_group_permissions id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auth_group_permissions ALTER COLUMN id SET DEFAULT nextval('public.auth_group_permissions_id_seq'::regclass);


--
-- Name: auth_permission id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auth_permission ALTER COLUMN id SET DEFAULT nextval('public.auth_permission_id_seq'::regclass);


--
-- Name: auth_user id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auth_user ALTER COLUMN id SET DEFAULT nextval('public.auth_user_id_seq'::regclass);


--
-- Name: auth_user_groups id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auth_user_groups ALTER COLUMN id SET DEFAULT nextval('public.auth_user_groups_id_seq'::regclass);


--
-- Name: auth_user_user_permissions id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auth_user_user_permissions ALTER COLUMN id SET DEFAULT nextval('public.auth_user_user_permissions_id_seq'::regclass);


--
-- Name: django_admin_log id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.django_admin_log ALTER COLUMN id SET DEFAULT nextval('public.django_admin_log_id_seq'::regclass);


--
-- Name: django_content_type id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.django_content_type ALTER COLUMN id SET DEFAULT nextval('public.django_content_type_id_seq'::regclass);


--
-- Name: django_migrations id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.django_migrations ALTER COLUMN id SET DEFAULT nextval('public.django_migrations_id_seq'::regclass);


--
-- Name: trials_app_application id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.trials_app_application ALTER COLUMN id SET DEFAULT nextval('public.trials_app_application_id_seq'::regclass);


--
-- Name: trials_app_application_target_oblasts id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.trials_app_application_target_oblasts ALTER COLUMN id SET DEFAULT nextval('public.trials_app_application_target_oblasts_id_seq'::regclass);


--
-- Name: trials_app_applicationdecisionhistory id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.trials_app_applicationdecisionhistory ALTER COLUMN id SET DEFAULT nextval('public.trials_app_applicationdecisionhistory_id_seq'::regclass);


--
-- Name: trials_app_climatezone id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.trials_app_climatezone ALTER COLUMN id SET DEFAULT nextval('public.trials_app_climatezone_id_seq'::regclass);


--
-- Name: trials_app_culture id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.trials_app_culture ALTER COLUMN id SET DEFAULT nextval('public.trials_app_culture_id_seq'::regclass);


--
-- Name: trials_app_document id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.trials_app_document ALTER COLUMN id SET DEFAULT nextval('public.trials_app_document_id_seq'::regclass);


--
-- Name: trials_app_groupculture id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.trials_app_groupculture ALTER COLUMN id SET DEFAULT nextval('public.trials_app_groupculture_id_seq'::regclass);


--
-- Name: trials_app_indicator id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.trials_app_indicator ALTER COLUMN id SET DEFAULT nextval('public.trials_app_indicator_id_seq'::regclass);


--
-- Name: trials_app_indicator_group_cultures id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.trials_app_indicator_group_cultures ALTER COLUMN id SET DEFAULT nextval('public.trials_app_indicator_group_cultures_id_seq'::regclass);


--
-- Name: trials_app_oblast id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.trials_app_oblast ALTER COLUMN id SET DEFAULT nextval('public.trials_app_oblast_id_seq'::regclass);


--
-- Name: trials_app_originator id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.trials_app_originator ALTER COLUMN id SET DEFAULT nextval('public.trials_app_originator_id_seq'::regclass);


--
-- Name: trials_app_planneddistribution id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.trials_app_planneddistribution ALTER COLUMN id SET DEFAULT nextval('public.trials_app_planneddistribution_id_seq'::regclass);


--
-- Name: trials_app_region id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.trials_app_region ALTER COLUMN id SET DEFAULT nextval('public.trials_app_region_id_seq'::regclass);


--
-- Name: trials_app_sortoriginator id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.trials_app_sortoriginator ALTER COLUMN id SET DEFAULT nextval('public.trials_app_sortoriginator_id_seq'::regclass);


--
-- Name: trials_app_sortrecord id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.trials_app_sortrecord ALTER COLUMN id SET DEFAULT nextval('public.trials_app_sortrecord_id_seq'::regclass);


--
-- Name: trials_app_trial id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.trials_app_trial ALTER COLUMN id SET DEFAULT nextval('public.trials_app_trial_id_seq'::regclass);


--
-- Name: trials_app_trial_indicators id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.trials_app_trial_indicators ALTER COLUMN id SET DEFAULT nextval('public.trials_app_trial_indicators_id_seq'::regclass);


--
-- Name: trials_app_triallaboratoryresult id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.trials_app_triallaboratoryresult ALTER COLUMN id SET DEFAULT nextval('public.trials_app_triallaboratoryresult_id_seq'::regclass);


--
-- Name: trials_app_trialparticipant id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.trials_app_trialparticipant ALTER COLUMN id SET DEFAULT nextval('public.trials_app_trialparticipant_id_seq'::regclass);


--
-- Name: trials_app_trialplan id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.trials_app_trialplan ALTER COLUMN id SET DEFAULT nextval('public.trials_app_trialplan_id_seq'::regclass);


--
-- Name: trials_app_trialplanculture id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.trials_app_trialplanculture ALTER COLUMN id SET DEFAULT nextval('public.trials_app_trialplanculture_id_seq'::regclass);


--
-- Name: trials_app_trialplanculturetrialtype id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.trials_app_trialplanculturetrialtype ALTER COLUMN id SET DEFAULT nextval('public.trials_app_trialplanculturetrialtype_id_seq'::regclass);


--
-- Name: trials_app_trialplanparticipant id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.trials_app_trialplanparticipant ALTER COLUMN id SET DEFAULT nextval('public.trials_app_trialplanparticipant_id_seq'::regclass);


--
-- Name: trials_app_trialplantrial id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.trials_app_trialplantrial ALTER COLUMN id SET DEFAULT nextval('public.trials_app_trialplantrial_id_seq'::regclass);


--
-- Name: trials_app_trialresult id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.trials_app_trialresult ALTER COLUMN id SET DEFAULT nextval('public.trials_app_trialresult_id_seq'::regclass);


--
-- Name: trials_app_trialtype id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.trials_app_trialtype ALTER COLUMN id SET DEFAULT nextval('public.trials_app_trialtype_id_seq'::regclass);


--
-- Data for Name: auth_group; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.auth_group (id, name) FROM stdin;
\.


--
-- Data for Name: auth_group_permissions; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.auth_group_permissions (id, group_id, permission_id) FROM stdin;
\.


--
-- Data for Name: auth_permission; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.auth_permission (id, name, content_type_id, codename) FROM stdin;
1	Can add log entry	1	add_logentry
2	Can change log entry	1	change_logentry
3	Can delete log entry	1	delete_logentry
4	Can view log entry	1	view_logentry
5	Can add permission	2	add_permission
6	Can change permission	2	change_permission
7	Can delete permission	2	delete_permission
8	Can view permission	2	view_permission
9	Can add group	3	add_group
10	Can change group	3	change_group
11	Can delete group	3	delete_group
12	Can view group	3	view_group
13	Can add user	4	add_user
14	Can change user	4	change_user
15	Can delete user	4	delete_user
16	Can view user	4	view_user
17	Can add content type	5	add_contenttype
18	Can change content type	5	change_contenttype
19	Can delete content type	5	delete_contenttype
20	Can view content type	5	view_contenttype
21	Can add session	6	add_session
22	Can change session	6	change_session
23	Can delete session	6	delete_session
24	Can view session	6	view_session
25	Can add Token	7	add_token
26	Can change Token	7	change_token
27	Can delete Token	7	delete_token
28	Can view Token	7	view_token
29	Can add token	8	add_tokenproxy
30	Can change token	8	change_tokenproxy
31	Can delete token	8	delete_tokenproxy
32	Can view token	8	view_tokenproxy
33	Can add Заявка на испытание	9	add_application
34	Can change Заявка на испытание	9	change_application
35	Can delete Заявка на испытание	9	delete_application
36	Can view Заявка на испытание	9	view_application
37	Can add Природно-климатическая зона	10	add_climatezone
38	Can change Природно-климатическая зона	10	change_climatezone
39	Can delete Природно-климатическая зона	10	delete_climatezone
40	Can view Природно-климатическая зона	10	view_climatezone
41	Can add Культура	11	add_culture
42	Can change Культура	11	change_culture
43	Can delete Культура	11	delete_culture
44	Can view Культура	11	view_culture
45	Can add Группа культур	12	add_groupculture
46	Can change Группа культур	12	change_groupculture
47	Can delete Группа культур	12	delete_groupculture
48	Can view Группа культур	12	view_groupculture
49	Can add Показатель	13	add_indicator
50	Can change Показатель	13	change_indicator
51	Can delete Показатель	13	delete_indicator
52	Can view Показатель	13	view_indicator
53	Can add Область	14	add_oblast
54	Can change Область	14	change_oblast
55	Can delete Область	14	delete_oblast
56	Can view Область	14	view_oblast
57	Can add Оригинатор	15	add_originator
58	Can change Оригинатор	15	change_originator
59	Can delete Оригинатор	15	delete_originator
60	Can view Оригинатор	15	view_originator
61	Can add Сортоучасток (ГСУ)	16	add_region
62	Can change Сортоучасток (ГСУ)	16	change_region
63	Can delete Сортоучасток (ГСУ)	16	delete_region
64	Can view Сортоучасток (ГСУ)	16	view_region
65	Can add Запись о сорте	17	add_sortrecord
66	Can change Запись о сорте	17	change_sortrecord
67	Can delete Запись о сорте	17	delete_sortrecord
68	Can view Запись о сорте	17	view_sortrecord
69	Can add Испытание	18	add_trial
70	Can change Испытание	18	change_trial
71	Can delete Испытание	18	delete_trial
72	Can view Испытание	18	view_trial
73	Can add Участник сортоопыта	19	add_trialparticipant
74	Can change Участник сортоопыта	19	change_trialparticipant
75	Can delete Участник сортоопыта	19	delete_trialparticipant
76	Can view Участник сортоопыта	19	view_trialparticipant
77	Can add План испытаний	20	add_trialplan
78	Can change План испытаний	20	change_trialplan
79	Can delete План испытаний	20	delete_trialplan
80	Can view План испытаний	20	view_trialplan
81	Can add Культура в плане	21	add_trialplanculture
82	Can change Культура в плане	21	change_trialplanculture
83	Can delete Культура в плане	21	delete_trialplanculture
84	Can view Культура в плане	21	view_trialplanculture
85	Can add Тип испытания в культуре плана	22	add_trialplanculturetrialtype
86	Can change Тип испытания в культуре плана	22	change_trialplanculturetrialtype
87	Can delete Тип испытания в культуре плана	22	delete_trialplanculturetrialtype
88	Can view Тип испытания в культуре плана	22	view_trialplanculturetrialtype
89	Can add Участник плана	23	add_trialplanparticipant
90	Can change Участник плана	23	change_trialplanparticipant
91	Can delete Участник плана	23	delete_trialplanparticipant
92	Can view Участник плана	23	view_trialplanparticipant
93	Can add Тип испытания	24	add_trialtype
94	Can change Тип испытания	24	change_trialtype
95	Can delete Тип испытания	24	delete_trialtype
96	Can view Тип испытания	24	view_trialtype
97	Can add Испытание в плане	25	add_trialplantrial
98	Can change Испытание в плане	25	change_trialplantrial
99	Can delete Испытание в плане	25	delete_trialplantrial
100	Can view Испытание в плане	25	view_trialplantrial
101	Can add Документ	26	add_document
102	Can change Документ	26	change_document
103	Can delete Документ	26	delete_document
104	Can view Документ	26	view_document
105	Can add Годовая таблица решений	27	add_annualdecisiontable
106	Can change Годовая таблица решений	27	change_annualdecisiontable
107	Can delete Годовая таблица решений	27	delete_annualdecisiontable
108	Can view Годовая таблица решений	27	view_annualdecisiontable
109	Can add Результат испытания	28	add_trialresult
110	Can change Результат испытания	28	change_trialresult
111	Can delete Результат испытания	28	delete_trialresult
112	Can view Результат испытания	28	view_trialresult
113	Can add Лабораторный результат испытания	29	add_triallaboratoryresult
114	Can change Лабораторный результат испытания	29	change_triallaboratoryresult
115	Can delete Лабораторный результат испытания	29	delete_triallaboratoryresult
116	Can view Лабораторный результат испытания	29	view_triallaboratoryresult
117	Can add Оригинатор сорта	30	add_sortoriginator
118	Can change Оригинатор сорта	30	change_sortoriginator
119	Can delete Оригинатор сорта	30	delete_sortoriginator
120	Can view Оригинатор сорта	30	view_sortoriginator
121	Can add Плановое распределение	31	add_planneddistribution
122	Can change Плановое распределение	31	change_planneddistribution
123	Can delete Плановое распределение	31	delete_planneddistribution
124	Can view Плановое распределение	31	view_planneddistribution
125	Can add Элемент годовой таблицы	32	add_annualdecisionitem
126	Can change Элемент годовой таблицы	32	change_annualdecisionitem
127	Can delete Элемент годовой таблицы	32	delete_annualdecisionitem
128	Can view Элемент годовой таблицы	32	view_annualdecisionitem
129	Can add Статус заявки по области	33	add_applicationoblaststatus
130	Can change Статус заявки по области	33	change_applicationoblaststatus
131	Can delete Статус заявки по области	33	delete_applicationoblaststatus
132	Can view Статус заявки по области	33	view_applicationoblaststatus
133	Can add История решения	34	add_applicationdecisionhistory
134	Can change История решения	34	change_applicationdecisionhistory
135	Can delete История решения	34	delete_applicationdecisionhistory
136	Can view История решения	34	view_applicationdecisionhistory
\.


--
-- Data for Name: auth_user; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.auth_user (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) FROM stdin;
2	pbkdf2_sha256$260000$al87KPFyl8GlCxQ63DcvN5$Me24QmCsL6m3nwqBCidBZo0opWPUYq7wbvEP+yztaTs=	\N	f	testuser			testuser@example.com	f	t	2025-10-16 08:54:15.803851+00
1	pbkdf2_sha256$260000$vNfJUPmxkqQCU1WqSrN88S$TU8GmV0KRRFv0RWQ9cUMGsZCvopC4hp4wUYN9AP95QM=	\N	t	admin			admin@example.com	t	t	2025-10-16 08:54:15.774297+00
\.


--
-- Data for Name: auth_user_groups; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.auth_user_groups (id, user_id, group_id) FROM stdin;
\.


--
-- Data for Name: auth_user_user_permissions; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.auth_user_user_permissions (id, user_id, permission_id) FROM stdin;
\.


--
-- Data for Name: authtoken_token; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.authtoken_token (key, created, user_id) FROM stdin;
5ebc884bc68f0c10f955a83cdad8520cc36036f1	2025-10-16 08:55:01.335863+00	1
60bbac63a19bc6c03651206cdcb3801c259bb81d	2025-10-20 04:37:59.830647+00	2
\.


--
-- Data for Name: django_admin_log; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) FROM stdin;
\.


--
-- Data for Name: django_content_type; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.django_content_type (id, app_label, model) FROM stdin;
1	admin	logentry
2	auth	permission
3	auth	group
4	auth	user
5	contenttypes	contenttype
6	sessions	session
7	authtoken	token
8	authtoken	tokenproxy
9	trials_app	application
10	trials_app	climatezone
11	trials_app	culture
12	trials_app	groupculture
13	trials_app	indicator
14	trials_app	oblast
15	trials_app	originator
16	trials_app	region
17	trials_app	sortrecord
18	trials_app	trial
19	trials_app	trialparticipant
20	trials_app	trialplan
21	trials_app	trialplanculture
22	trials_app	trialplanculturetrialtype
23	trials_app	trialplanparticipant
24	trials_app	trialtype
25	trials_app	trialplantrial
26	trials_app	document
27	trials_app	annualdecisiontable
28	trials_app	trialresult
29	trials_app	triallaboratoryresult
30	trials_app	sortoriginator
31	trials_app	planneddistribution
32	trials_app	annualdecisionitem
33	trials_app	applicationoblaststatus
34	trials_app	applicationdecisionhistory
\.


--
-- Data for Name: django_migrations; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.django_migrations (id, app, name, applied) FROM stdin;
1	contenttypes	0001_initial	2025-10-16 08:52:10.140872+00
2	auth	0001_initial	2025-10-16 08:52:10.164469+00
3	admin	0001_initial	2025-10-16 08:52:10.170991+00
4	admin	0002_logentry_remove_auto_add	2025-10-16 08:52:10.173224+00
5	admin	0003_logentry_add_action_flag_choices	2025-10-16 08:52:10.175447+00
6	contenttypes	0002_remove_content_type_name	2025-10-16 08:52:10.179899+00
7	auth	0002_alter_permission_name_max_length	2025-10-16 08:52:10.182133+00
8	auth	0003_alter_user_email_max_length	2025-10-16 08:52:10.184397+00
9	auth	0004_alter_user_username_opts	2025-10-16 08:52:10.187157+00
10	auth	0005_alter_user_last_login_null	2025-10-16 08:52:10.189887+00
11	auth	0006_require_contenttypes_0002	2025-10-16 08:52:10.19064+00
12	auth	0007_alter_validators_add_error_messages	2025-10-16 08:52:10.192912+00
13	auth	0008_alter_user_username_max_length	2025-10-16 08:52:10.196592+00
14	auth	0009_alter_user_last_name_max_length	2025-10-16 08:52:10.199474+00
15	auth	0010_alter_group_name_max_length	2025-10-16 08:52:10.202611+00
16	auth	0011_update_proxy_permissions	2025-10-16 08:52:10.205011+00
17	auth	0012_alter_user_first_name_max_length	2025-10-16 08:52:10.208351+00
18	authtoken	0001_initial	2025-10-16 08:52:10.213896+00
19	authtoken	0002_auto_20160226_1747	2025-10-16 08:52:10.22074+00
20	authtoken	0003_tokenproxy	2025-10-16 08:52:10.221729+00
21	sessions	0001_initial	2025-10-16 08:52:10.225872+00
22	trials_app	0001_initial	2025-10-16 08:52:10.612879+00
23	trials_app	0002_auto_20251016_1352	2025-10-16 08:52:34.352758+00
24	trials_app	0003_remove_unused_trial_fields	2025-10-16 15:30:02.770289+00
25	trials_app	0004_rename_total_varieties_to_total_participants	2025-10-16 16:36:17.871706+00
26	trials_app	0005_change_seeds_provision_default	2025-10-16 17:07:53.627528+00
27	trials_app	0006_auto_20251016_2250	2025-10-16 17:50:26.766411+00
28	trials_app	0007_auto_20251016_2328	2025-10-16 18:29:21.019168+00
29	trials_app	0008_indicator_validation_rules	2025-10-16 18:32:34.022986+00
30	trials_app	0009_trial_form008_fields	2025-10-16 20:17:15.843273+00
31	trials_app	0010_trial_participant_and_result_form008	2025-10-16 20:17:15.956863+00
32	trials_app	0011_auto_20251017_0117	2025-10-16 20:17:15.975915+00
33	trials_app	0012_add_drained_soils_option	2025-10-16 21:02:02.137546+00
34	trials_app	0013_add_patents_culture_id_to_trial	2025-10-17 05:15:39.730322+00
35	trials_app	0014_add_subgroup_field	2025-10-18 11:40:50.319803+00
36	trials_app	0015_remove_laboratory_code_from_trial_laboratory_result	2025-10-18 11:41:18.42901+00
37	trials_app	0016_remove_trialparticipant_subgroup_code	2025-10-18 13:43:44.359264+00
38	trials_app	0017_alter_annualdecisionitem_years_tested	2025-10-18 13:47:17.493643+00
39	trials_app	0018_alter_annualdecisionitem_year_started	2025-10-18 13:48:48.872582+00
40	trials_app	0019_create_application_oblast_status	2025-10-18 14:05:46.342937+00
41	trials_app	0020_add_status_column	2025-10-18 14:09:44.779517+00
42	trials_app	0021_add_status_to_existing_table	2025-10-18 14:10:47.175958+00
43	trials_app	0022_remove_application_oblast_status	2025-10-18 14:14:05.36291+00
44	trials_app	0023_add_decision_fields_to_target_oblasts	2025-10-18 14:26:43.064045+00
45	trials_app	0024_create_application_decision_history	2025-10-18 14:26:43.126257+00
46	trials_app	0025_remove_annual_decision_tables	2025-10-18 14:29:11.08852+00
47	trials_app	0026_remove_annual_decision_item_id	2025-10-18 14:32:36.060828+00
48	trials_app	0027_add_originator_fields	2025-10-21 20:49:00.509922+00
\.


--
-- Data for Name: django_session; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.django_session (session_key, session_data, expire_date) FROM stdin;
\.


--
-- Data for Name: trials_app_application; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.trials_app_application (id, is_deleted, deleted_at, application_number, submission_date, applicant, applicant_inn_bin, contact_person_name, contact_person_phone, contact_person_email, maturity_group, purpose, status, created_at, updated_at, created_by_id, sort_record_id) FROM stdin;
5	f	\N	5	2025-10-16	Test	555555555555	ТЕСТ	+7 (555) 555-55-55	3rddfg@affds	D03		in_progress	2025-10-16 09:04:46.308988+00	2025-10-18 14:14:45.048638+00	1	5
4	f	\N	4	2025-10-16	Test	444444444444	ТЕСТ	+7 (444) 444-44-44	3rddfg@affds	D03		in_progress	2025-10-16 09:03:46.366371+00	2025-10-18 14:14:45.052711+00	1	4
3	f	\N	3	1999-10-16	Test	111111111111	ТЕСТ	+7 (111) 111-11-11	3rddfg@affds	D03		in_progress	2025-10-16 09:02:16.627246+00	2025-10-18 14:14:45.059838+00	1	3
1	f	\N	1	1980-10-16	Test	111111111111	ТЕСТ	+7 (111) 111-11-11	3rddfg@affds	D07		in_progress	2025-10-16 09:00:26.788036+00	2025-10-18 14:14:45.063333+00	1	1
2	f	\N	2	2019-10-16	Test	111111111111	adfs1221	+7 (111) 111-11-11	3rddfg@affds	D03		submitted	2025-10-16 09:01:15.903672+00	2025-10-18 15:43:10.530255+00	1	2
6	f	\N	10	2025-10-02	ТОО Агрофмира	323232323232	ТЕСТ	+7 (111) 111-11-11	3rddfg@affds	D04	we	submitted	2025-10-20 07:33:24.27856+00	2025-10-20 07:33:24.278564+00	1	2131
7	f	\N	11	2025-10-20	ТТАЫ	673676767326	ывывча	+7 (434) 343-43-53	3rddfg@affds	D04	ыфвирофыв	submitted	2025-10-20 09:58:43.723185+00	2025-10-20 09:58:43.72319+00	1	615
\.


--
-- Data for Name: trials_app_application_target_oblasts; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.trials_app_application_target_oblasts (id, application_id, oblast_id, status, trial_plan_id, trial_id, created_at, updated_at, decision_date, decision_justification, decided_by_id, decision_year) FROM stdin;
2	1	7	planned	\N	\N	2025-10-18 14:10:47.170911	2025-10-18 14:10:47.170911	\N	\N	\N	\N
4	2	7	planned	\N	\N	2025-10-18 14:10:47.170911	2025-10-18 14:10:47.170911	\N	\N	\N	\N
6	3	7	planned	\N	\N	2025-10-18 14:10:47.170911	2025-10-18 14:10:47.170911	\N	\N	\N	\N
8	4	7	planned	\N	\N	2025-10-18 14:10:47.170911	2025-10-18 14:10:47.170911	\N	\N	\N	\N
10	5	7	planned	\N	\N	2025-10-18 14:10:47.170911	2025-10-18 14:10:47.170911	\N	\N	\N	\N
9	5	17	decision_pending	\N	\N	2025-10-18 09:10:47.170911	2025-10-18 14:14:45.048125	\N	\N	\N	\N
7	4	17	decision_pending	\N	\N	2025-10-18 09:10:47.170911	2025-10-18 14:14:45.052392	\N	\N	\N	\N
5	3	17	decision_pending	\N	\N	2025-10-18 09:10:47.170911	2025-10-18 14:14:45.059518	\N	\N	\N	\N
1	1	17	decision_pending	\N	\N	2025-10-18 09:10:47.170911	2025-10-18 14:14:45.063067	\N	\N	\N	\N
3	2	17	decision_pending	\N	\N	2025-10-18 09:10:47.170911	2025-10-18 15:43:10.529434	\N	\N	\N	\N
11	6	13	planned	\N	\N	2025-10-20 07:33:24.279888	2025-10-20 07:33:24.279888	\N	\N	\N	\N
12	7	1	planned	\N	\N	2025-10-20 09:58:43.724092	2025-10-20 09:58:43.724092	\N	\N	\N	\N
13	7	5	planned	\N	\N	2025-10-20 09:58:43.724092	2025-10-20 09:58:43.724092	\N	\N	\N	\N
\.


--
-- Data for Name: trials_app_applicationdecisionhistory; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.trials_app_applicationdecisionhistory (id, year, decision, decision_date, decision_justification, average_yield, years_tested_total, created_at, updated_at, application_id, decided_by_id, oblast_id) FROM stdin;
\.


--
-- Data for Name: trials_app_climatezone; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.trials_app_climatezone (id, is_deleted, deleted_at, name, code, description, created_at, updated_at) FROM stdin;
1	f	\N	Лесостепная зона	forest-steppe	Природно-климатическая зона: Лесостепная зона	2025-10-16 08:53:53.922261+00	2025-10-16 08:53:53.92227+00
2	f	\N	Степная слабо увлажнённая	steppe-low-humid	Природно-климатическая зона: Степная слабо увлажнённая	2025-10-16 08:53:53.927462+00	2025-10-16 08:53:53.927465+00
3	f	\N	Степная слабо засушливая	steppe-low-arid	Природно-климатическая зона: Степная слабо засушливая	2025-10-16 08:53:53.930073+00	2025-10-16 08:53:53.930077+00
4	f	\N	Степная умеренно засушливая	steppe-moderate-arid	Природно-климатическая зона: Степная умеренно засушливая	2025-10-16 08:53:53.95222+00	2025-10-16 08:53:53.952224+00
5	f	\N	Пустынно-степная умеренно засушливая	desert-steppe-moderate-arid	Природно-климатическая зона: Пустынно-степная умеренно засушливая	2025-10-16 08:53:53.953593+00	2025-10-16 08:53:53.953597+00
6	f	\N	Предгорная (Джунгарский Алатау, северо-запад Тянь-Шань)	foothill-dzungarian-tienshan	Природно-климатическая зона: Предгорная (Джунгарский Алатау, северо-запад Тянь-Шань)	2025-10-16 08:53:53.969384+00	2025-10-16 08:53:53.969388+00
7	f	\N	Предгорная (Северо-Западный Тянь-Шань)	foothill-northwest-tienshan	Природно-климатическая зона: Предгорная (Северо-Западный Тянь-Шань)	2025-10-16 08:53:53.974557+00	2025-10-16 08:53:53.974561+00
8	f	\N	Пустынная очень засушливая	desert-very-arid	Природно-климатическая зона: Пустынная очень засушливая	2025-10-16 08:53:53.976103+00	2025-10-16 08:53:53.976107+00
9	f	\N	Предгорная (Заилийский Алатау)	foothill-zailiysky-alatau	Природно-климатическая зона: Предгорная (Заилийский Алатау)	2025-10-16 08:53:53.977566+00	2025-10-16 08:53:53.977569+00
10	f	\N	Пустынная сухая	desert-dry	Природно-климатическая зона: Пустынная сухая	2025-10-16 08:53:53.982236+00	2025-10-16 08:53:53.98224+00
11	f	\N	Предгорная (Северного и Западного Тянь-Шаня)	foothill-north-west-tienshan	Природно-климатическая зона: Предгорная (Северного и Западного Тянь-Шаня)	2025-10-16 08:53:53.989732+00	2025-10-16 08:53:53.989735+00
\.


--
-- Data for Name: trials_app_culture; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.trials_app_culture (id, is_deleted, deleted_at, culture_id, name, code, synced_at, created_at, updated_at, group_culture_id) FROM stdin;
1	f	\N	720	пшеница	\N	2025-10-22 07:33:56.210242+00	2025-10-16 09:00:26.772876+00	2025-10-22 07:33:56.210322+00	\N
2	f	\N	71	абрикос	\N	2025-10-21 21:50:08.175573+00	2025-10-16 17:24:37.92908+00	2025-10-21 21:50:08.175627+00	\N
3	f	\N	535	Айва	\N	2025-10-21 21:50:08.17845+00	2025-10-16 17:24:37.9315+00	2025-10-21 21:50:08.178479+00	\N
4	f	\N	246	Алыча	\N	2025-10-21 21:50:08.179427+00	2025-10-16 17:24:37.932371+00	2025-10-21 21:50:08.179448+00	\N
5	f	\N	2	арбуз	\N	2025-10-21 21:50:08.180309+00	2025-10-16 17:24:37.933125+00	2025-10-21 21:50:08.18034+00	\N
6	f	\N	702	Африканское просо	\N	2025-10-21 21:50:08.181409+00	2025-10-16 17:24:37.934135+00	2025-10-21 21:50:08.181432+00	\N
7	f	\N	29	Базилик	\N	2025-10-21 21:50:08.182375+00	2025-10-16 17:24:37.935383+00	2025-10-21 21:50:08.182401+00	\N
8	f	\N	31	Баклажан	\N	2025-10-21 21:50:08.18324+00	2025-10-16 17:24:37.936334+00	2025-10-21 21:50:08.183263+00	\N
9	f	\N	81	береза	\N	2025-10-21 21:50:08.183937+00	2025-10-16 17:24:37.937166+00	2025-10-21 21:50:08.183958+00	\N
10	f	\N	705	брокколи	\N	2025-10-21 21:50:08.184776+00	2025-10-16 17:24:37.937779+00	2025-10-21 21:50:08.1848+00	\N
11	f	\N	739	Брокколи (новая методика)	\N	2025-10-21 21:50:08.185703+00	2025-10-16 17:24:37.938357+00	2025-10-21 21:50:08.185736+00	\N
12	f	\N	534	Брюква	\N	2025-10-21 21:50:08.186597+00	2025-10-16 17:24:37.938936+00	2025-10-21 21:50:08.18662+00	\N
13	f	\N	536	Вигна	\N	2025-10-21 21:50:08.187482+00	2025-10-16 17:24:37.939522+00	2025-10-21 21:50:08.187507+00	\N
14	f	\N	538	Вика	\N	2025-10-21 21:50:08.188287+00	2025-10-16 17:24:37.940045+00	2025-10-21 21:50:08.188309+00	\N
15	f	\N	537	Вика посевная	\N	2025-10-21 21:50:08.189104+00	2025-10-16 17:24:37.940817+00	2025-10-21 21:50:08.189126+00	\N
16	f	\N	68	виноград 	\N	2025-10-21 21:50:08.189817+00	2025-10-16 17:24:37.941373+00	2025-10-21 21:50:08.189838+00	\N
17	f	\N	3	Вишня	\N	2025-10-21 21:50:08.190534+00	2025-10-16 17:24:37.942099+00	2025-10-21 21:50:08.190555+00	\N
18	f	\N	730	вишня (по старой методике)	\N	2025-10-21 21:50:08.191248+00	2025-10-16 17:24:37.942904+00	2025-10-21 21:50:08.191268+00	\N
19	f	\N	547	голубика	\N	2025-10-21 21:50:08.191996+00	2025-10-16 17:24:37.943885+00	2025-10-21 21:50:08.192021+00	\N
20	f	\N	24	горох	\N	2025-10-21 21:50:08.192721+00	2025-10-16 17:24:37.944702+00	2025-10-21 21:50:08.192742+00	\N
21	f	\N	726	Горох посевной, Горох овощной (новая методика)	\N	2025-10-21 21:50:08.19342+00	2025-10-16 17:24:37.945576+00	2025-10-21 21:50:08.193441+00	\N
22	f	\N	22	Горчица	\N	2025-10-21 21:50:08.194382+00	2025-10-16 17:24:37.946263+00	2025-10-21 21:50:08.194406+00	\N
23	f	\N	784	Горчица белая (Новая методика)	\N	2025-10-21 21:50:08.195129+00	2025-10-16 17:24:37.946878+00	2025-10-21 21:50:08.19515+00	\N
24	f	\N	725	горчица (по старой методике)	\N	2025-10-21 21:50:08.195857+00	2025-10-16 17:24:37.947419+00	2025-10-21 21:50:08.195878+00	\N
25	f	\N	719	Горчица сарептская (новая методика)	\N	2025-10-21 21:50:08.1968+00	2025-10-16 17:24:37.947944+00	2025-10-21 21:50:08.196834+00	\N
26	f	\N	255	грецкий орех	\N	2025-10-21 21:50:08.19777+00	2025-10-16 17:24:37.948493+00	2025-10-21 21:50:08.197793+00	\N
27	f	\N	16	гречиха 	\N	2025-10-21 21:50:08.198543+00	2025-10-16 17:24:37.949024+00	2025-10-21 21:50:08.198564+00	\N
28	f	\N	722	Гречиха (новая методика)	\N	2025-10-21 21:50:08.199206+00	2025-10-16 17:24:37.949538+00	2025-10-21 21:50:08.199227+00	\N
32	f	\N	1	дыня	\N	2025-10-21 21:50:08.202222+00	2025-10-16 17:24:37.952072+00	2025-10-21 21:50:08.202246+00	\N
82	f	\N	38	перец	\N	2025-10-21 21:50:08.238484+00	2025-10-16 17:24:37.983093+00	2025-10-21 21:50:08.238505+00	\N
29	f	\N	74	груша	\N	2025-10-21 21:50:08.199851+00	2025-10-16 17:24:37.950037+00	2025-10-21 21:50:08.199872+00	\N
30	f	\N	728	Груша грушелистная (новая методика)	\N	2025-10-21 21:50:08.200749+00	2025-10-16 17:24:37.95061+00	2025-10-21 21:50:08.20077+00	\N
31	f	\N	50	донник 	\N	2025-10-21 21:50:08.201451+00	2025-10-16 17:24:37.951266+00	2025-10-21 21:50:08.201473+00	\N
33	f	\N	60	ежа сборная	\N	2025-10-21 21:50:08.203003+00	2025-10-16 17:24:37.952953+00	2025-10-21 21:50:08.203025+00	\N
34	f	\N	522	жимолость	\N	2025-10-21 21:50:08.203689+00	2025-10-16 17:24:37.953775+00	2025-10-21 21:50:08.20371+00	\N
35	f	\N	64	житняк 	\N	2025-10-21 21:50:08.204454+00	2025-10-16 17:24:37.954405+00	2025-10-21 21:50:08.204476+00	\N
36	f	\N	732	житняк (по старой методике)	\N	2025-10-21 21:50:08.205423+00	2025-10-16 17:24:37.955067+00	2025-10-21 21:50:08.205462+00	\N
37	f	\N	675	земляника	\N	2025-10-21 21:50:08.206302+00	2025-10-16 17:24:37.955734+00	2025-10-21 21:50:08.206324+00	\N
38	f	\N	33	кабачок	\N	2025-10-21 21:50:08.207046+00	2025-10-16 17:24:37.956252+00	2025-10-21 21:50:08.207067+00	\N
39	f	\N	750	Капуста белокочанная, краснокочанная, савойская (Новая методика)	\N	2025-10-21 21:50:08.20771+00	2025-10-16 17:24:37.956838+00	2025-10-21 21:50:08.207731+00	\N
40	f	\N	35	капуста бк	\N	2025-10-21 21:50:08.208424+00	2025-10-16 17:24:37.957361+00	2025-10-21 21:50:08.208445+00	\N
41	f	\N	712	капуста листовая	\N	2025-10-21 21:50:08.209094+00	2025-10-16 17:24:37.95794+00	2025-10-21 21:50:08.209114+00	\N
42	f	\N	34	Капуста цветная	\N	2025-10-21 21:50:08.209865+00	2025-10-16 17:24:37.958664+00	2025-10-21 21:50:08.209886+00	\N
43	f	\N	14	Картофель	\N	2025-10-21 21:50:08.210811+00	2025-10-16 17:24:37.95934+00	2025-10-21 21:50:08.210834+00	\N
44	f	\N	723	Картофель (по старой методике)	\N	2025-10-21 21:50:08.211558+00	2025-10-16 17:24:37.96019+00	2025-10-21 21:50:08.211579+00	\N
45	f	\N	51	клевер	\N	2025-10-21 21:50:08.212286+00	2025-10-16 17:24:37.960977+00	2025-10-21 21:50:08.212307+00	\N
46	f	\N	785	клубника	\N	2025-10-21 21:50:08.212982+00	2025-10-16 17:24:37.961689+00	2025-10-21 21:50:08.213003+00	\N
47	f	\N	706	кориандр	\N	2025-10-21 21:50:08.213635+00	2025-10-16 17:24:37.962366+00	2025-10-21 21:50:08.213655+00	\N
48	f	\N	737	Кориандр (новая методика)	\N	2025-10-21 21:50:08.214304+00	2025-10-16 17:24:37.962946+00	2025-10-21 21:50:08.214324+00	\N
49	f	\N	63	кострец	\N	2025-10-21 21:50:08.214943+00	2025-10-16 17:24:37.963465+00	2025-10-21 21:50:08.214964+00	\N
50	f	\N	717	кострец (по старой методике)	\N	2025-10-21 21:50:08.215586+00	2025-10-16 17:24:37.963997+00	2025-10-21 21:50:08.215607+00	\N
51	f	\N	692	кохия	\N	2025-10-21 21:50:08.216265+00	2025-10-16 17:24:37.964502+00	2025-10-21 21:50:08.216285+00	\N
52	f	\N	539	Крыжовник	\N	2025-10-21 21:50:08.216963+00	2025-10-16 17:24:37.965006+00	2025-10-21 21:50:08.216986+00	\N
53	f	\N	749	Кукуруза (Новая методика)	\N	2025-10-21 21:50:08.217608+00	2025-10-16 17:24:37.965545+00	2025-10-21 21:50:08.217628+00	\N
54	f	\N	26	кукуруза полузубовидная	\N	2025-10-21 21:50:08.21839+00	2025-10-16 17:24:37.966253+00	2025-10-21 21:50:08.218411+00	\N
55	f	\N	21	лен масличный	\N	2025-10-21 21:50:08.219183+00	2025-10-16 17:24:37.966903+00	2025-10-21 21:50:08.219207+00	\N
56	f	\N	748	Лен масличный (Новая методика)	\N	2025-10-21 21:50:08.219945+00	2025-10-16 17:24:37.967609+00	2025-10-21 21:50:08.219966+00	\N
57	f	\N	66	ломкоколосник ситниковый	\N	2025-10-21 21:50:08.220696+00	2025-10-16 17:24:37.968499+00	2025-10-21 21:50:08.220717+00	\N
58	f	\N	454	лук батун	\N	2025-10-21 21:50:08.221374+00	2025-10-16 17:24:37.969197+00	2025-10-21 21:50:08.221395+00	\N
59	f	\N	540	Лук порей	\N	2025-10-21 21:50:08.222036+00	2025-10-16 17:24:37.97006+00	2025-10-21 21:50:08.222057+00	\N
60	f	\N	36	лук репчатый	\N	2025-10-21 21:50:08.222674+00	2025-10-16 17:24:37.970659+00	2025-10-21 21:50:08.222698+00	\N
61	f	\N	53	люцерна 	\N	2025-10-21 21:50:08.223353+00	2025-10-16 17:24:37.971271+00	2025-10-21 21:50:08.223374+00	\N
62	f	\N	49	Лядвенец рог. метод для бобовых	\N	2025-10-21 21:50:08.224085+00	2025-10-16 17:24:37.971793+00	2025-10-21 21:50:08.224106+00	\N
63	f	\N	347	малина	\N	2025-10-21 21:50:08.224768+00	2025-10-16 17:24:37.972281+00	2025-10-21 21:50:08.224796+00	\N
64	f	\N	747	Мангольд (Новая методика)	\N	2025-10-21 21:50:08.225461+00	2025-10-16 17:24:37.972832+00	2025-10-21 21:50:08.225482+00	\N
65	f	\N	45	маш овощной	\N	2025-10-21 21:50:08.226169+00	2025-10-16 17:24:37.973363+00	2025-10-21 21:50:08.226188+00	\N
66	f	\N	245	миндаль	\N	2025-10-21 21:50:08.226793+00	2025-10-16 17:24:37.974007+00	2025-10-21 21:50:08.226813+00	\N
67	f	\N	46	морковь 	\N	2025-10-21 21:50:08.227739+00	2025-10-16 17:24:37.9746+00	2025-10-21 21:50:08.227761+00	\N
68	f	\N	746	Морковь (Новая методика 2024)	\N	2025-10-21 21:50:08.228515+00	2025-10-16 17:24:37.975135+00	2025-10-21 21:50:08.228536+00	\N
69	f	\N	47	морковь по нов.методике	\N	2025-10-21 21:50:08.229216+00	2025-10-16 17:24:37.975759+00	2025-10-21 21:50:08.229244+00	\N
70	f	\N	716	морковь (по старой методике)	\N	2025-10-21 21:50:08.229912+00	2025-10-16 17:24:37.976464+00	2025-10-21 21:50:08.229933+00	\N
71	f	\N	5	Мягкая пшеница	\N	2025-10-21 21:50:08.230569+00	2025-10-16 17:24:37.977232+00	2025-10-21 21:50:08.23059+00	\N
72	f	\N	221	мятлик луговой	\N	2025-10-21 21:50:08.231216+00	2025-10-16 17:24:37.977885+00	2025-10-21 21:50:08.231236+00	\N
73	f	\N	545	Нектарин	\N	2025-10-21 21:50:08.231891+00	2025-10-16 17:24:37.978546+00	2025-10-21 21:50:08.231921+00	\N
74	f	\N	25	нут	\N	2025-10-21 21:50:08.232521+00	2025-10-16 17:24:37.979147+00	2025-10-21 21:50:08.232541+00	\N
75	f	\N	541	Облепиха	\N	2025-10-21 21:50:08.233147+00	2025-10-16 17:24:37.979638+00	2025-10-21 21:50:08.233168+00	\N
76	f	\N	11	овес	PC-11	2025-10-21 21:50:08.233852+00	2025-10-16 17:24:37.980139+00	2025-10-21 21:50:08.233874+00	\N
77	f	\N	727	овес (по старой методике)	\N	2025-10-21 21:50:08.234741+00	2025-10-16 17:24:37.980611+00	2025-10-21 21:50:08.234762+00	\N
78	f	\N	134	овсяница тростниковая	\N	2025-10-21 21:50:08.235566+00	2025-10-16 17:24:37.981091+00	2025-10-21 21:50:08.23559+00	\N
79	f	\N	58	огурец посевной	\N	2025-10-21 21:50:08.236348+00	2025-10-16 17:24:37.981641+00	2025-10-21 21:50:08.236368+00	\N
80	f	\N	672	одуванчик, кок-сагыз	\N	2025-10-21 21:50:08.237071+00	2025-10-16 17:24:37.982135+00	2025-10-21 21:50:08.237091+00	\N
81	f	\N	57	Патиссон	\N	2025-10-21 21:50:08.237728+00	2025-10-16 17:24:37.982598+00	2025-10-21 21:50:08.237749+00	\N
83	f	\N	714	перец (по старой методике)	\N	2025-10-21 21:50:08.239202+00	2025-10-16 17:24:37.983603+00	2025-10-21 21:50:08.239224+00	\N
84	f	\N	542	Персик	\N	2025-10-21 21:50:08.239848+00	2025-10-16 17:24:37.984177+00	2025-10-21 21:50:08.239869+00	\N
85	f	\N	710	Петрушка	\N	2025-10-21 21:50:08.240578+00	2025-10-16 17:24:37.984949+00	2025-10-21 21:50:08.240599+00	\N
86	f	\N	731	Петрушка (новая методика)	\N	2025-10-21 21:50:08.24128+00	2025-10-16 17:24:37.985754+00	2025-10-21 21:50:08.241301+00	\N
87	f	\N	544	Подвои косточковых	\N	2025-10-21 21:50:08.242036+00	2025-10-16 17:24:37.98665+00	2025-10-21 21:50:08.242057+00	\N
88	f	\N	17	подсолнечник	\N	2025-10-21 21:50:08.242701+00	2025-10-16 17:24:37.987241+00	2025-10-21 21:50:08.242722+00	\N
89	f	\N	734	подсолнечник (по старой методике)	\N	2025-10-21 21:50:08.243419+00	2025-10-16 17:24:37.987809+00	2025-10-21 21:50:08.24344+00	\N
90	f	\N	13	просо	\N	2025-10-21 21:50:08.244312+00	2025-10-16 17:24:37.988317+00	2025-10-21 21:50:08.244334+00	\N
91	f	\N	735	Просо африканское (новая методика)	\N	2025-10-21 21:50:08.245091+00	2025-10-16 17:24:37.988915+00	2025-10-21 21:50:08.245112+00	\N
92	f	\N	598	прутняк (изень)	\N	2025-10-21 21:50:08.245847+00	2025-10-16 17:24:37.989511+00	2025-10-21 21:50:08.245975+00	\N
93	f	\N	695	пшеница мягкая (новая методика)	\N	2025-10-21 21:50:08.247675+00	2025-10-16 17:24:37.990377+00	2025-10-21 21:50:08.247697+00	\N
94	f	\N	644	пырей	\N	2025-10-21 21:50:08.248388+00	2025-10-16 17:24:37.990942+00	2025-10-21 21:50:08.248411+00	\N
95	f	\N	59	пырей бескорневищный 	\N	2025-10-21 21:50:08.249092+00	2025-10-16 17:24:37.991511+00	2025-10-21 21:50:08.249113+00	\N
96	f	\N	4	Райграс	\N	2025-10-21 21:50:08.249728+00	2025-10-16 17:24:37.992171+00	2025-10-21 21:50:08.249748+00	\N
97	f	\N	23	рапс  	\N	2025-10-21 21:50:08.250348+00	2025-10-16 17:24:37.992987+00	2025-10-21 21:50:08.250369+00	\N
98	f	\N	745	Рапс (Новая методика)	\N	2025-10-21 21:50:08.251024+00	2025-10-16 17:24:37.99375+00	2025-10-21 21:50:08.251048+00	\N
99	f	\N	250	редис	\N	2025-10-21 21:50:08.251933+00	2025-10-16 17:24:37.994562+00	2025-10-21 21:50:08.251954+00	\N
100	f	\N	724	Редька (новая методика)	\N	2025-10-21 21:50:08.252592+00	2025-10-16 17:24:37.995278+00	2025-10-21 21:50:08.252615+00	\N
101	f	\N	721	Репа, Турнепс (новая методика)	\N	2025-10-21 21:50:08.253359+00	2025-10-16 17:24:37.995963+00	2025-10-21 21:50:08.253382+00	\N
102	f	\N	12	рис	\N	2025-10-21 21:50:08.254038+00	2025-10-16 17:24:37.996616+00	2025-10-21 21:50:08.254057+00	\N
103	f	\N	8	рожь	\N	2025-10-21 21:50:08.254671+00	2025-10-16 17:24:37.997135+00	2025-10-21 21:50:08.254691+00	\N
104	f	\N	39	Салат	\N	2025-10-21 21:50:08.25532+00	2025-10-16 17:24:37.997849+00	2025-10-21 21:50:08.25534+00	\N
105	f	\N	738	Салат (новая методика)	\N	2025-10-21 21:50:08.256258+00	2025-10-16 17:24:37.998331+00	2025-10-21 21:50:08.256283+00	\N
106	f	\N	20	сафлор	\N	2025-10-21 21:50:08.257008+00	2025-10-16 17:24:37.998829+00	2025-10-21 21:50:08.25703+00	\N
107	f	\N	679	сахарная свекла	\N	2025-10-21 21:50:08.257705+00	2025-10-16 17:24:37.999307+00	2025-10-21 21:50:08.257725+00	\N
108	f	\N	41	свекла	\N	2025-10-21 21:50:08.258365+00	2025-10-16 17:24:37.999866+00	2025-10-21 21:50:08.258386+00	\N
109	f	\N	42	свекла сахарная	\N	2025-10-21 21:50:08.259098+00	2025-10-16 17:24:38.000406+00	2025-10-21 21:50:08.259119+00	\N
110	f	\N	744	Свекла столовая (Новая методика)	\N	2025-10-21 21:50:08.260014+00	2025-10-16 17:24:38.001017+00	2025-10-21 21:50:08.260041+00	\N
111	f	\N	743	Сельдерей корневой (Новая методика)	\N	2025-10-21 21:50:08.260831+00	2025-10-16 17:24:38.001623+00	2025-10-21 21:50:08.260853+00	\N
112	f	\N	742	Сельдерей (новая методика)	\N	2025-10-21 21:50:08.261534+00	2025-10-16 17:24:38.002398+00	2025-10-21 21:50:08.261555+00	\N
113	f	\N	76	слива	\N	2025-10-21 21:50:08.262193+00	2025-10-16 17:24:38.003108+00	2025-10-21 21:50:08.262215+00	\N
114	f	\N	733	слива (по старой методике)	\N	2025-10-21 21:50:08.26284+00	2025-10-16 17:24:38.003728+00	2025-10-21 21:50:08.262861+00	\N
115	f	\N	28	сорго 	\N	2025-10-21 21:50:08.263532+00	2025-10-16 17:24:38.004333+00	2025-10-21 21:50:08.263552+00	\N
116	f	\N	741	Сорго (Новая методика)	\N	2025-10-21 21:50:08.264161+00	2025-10-16 17:24:38.004966+00	2025-10-21 21:50:08.264181+00	\N
117	f	\N	620	сорго-суданковый гибрид	\N	2025-10-21 21:50:08.264802+00	2025-10-16 17:24:38.005556+00	2025-10-21 21:50:08.264823+00	\N
118	f	\N	82	сосна 	\N	2025-10-21 21:50:08.265448+00	2025-10-16 17:24:38.006038+00	2025-10-21 21:50:08.265469+00	\N
119	f	\N	18	соя	\N	2025-10-21 21:50:08.266117+00	2025-10-16 17:24:38.006521+00	2025-10-21 21:50:08.26614+00	\N
120	f	\N	718	соя (по старой методике)	\N	2025-10-21 21:50:08.266802+00	2025-10-16 17:24:38.006971+00	2025-10-21 21:50:08.266823+00	\N
121	f	\N	572	суданская трава	\N	2025-10-21 21:50:08.267525+00	2025-10-16 17:24:38.007458+00	2025-10-21 21:50:08.267548+00	\N
122	f	\N	48	суд. трава 	\N	2025-10-21 21:50:08.26821+00	2025-10-16 17:24:38.007966+00	2025-10-21 21:50:08.26823+00	\N
123	f	\N	7	Твердая пшеница	\N	2025-10-21 21:50:08.269058+00	2025-10-16 17:24:38.00849+00	2025-10-21 21:50:08.269084+00	\N
124	f	\N	703	Твердая пшеница (новая)	\N	2025-10-21 21:50:08.269829+00	2025-10-16 17:24:38.009041+00	2025-10-21 21:50:08.269849+00	\N
125	f	\N	61	тимофеевка луговая	\N	2025-10-21 21:50:08.270497+00	2025-10-16 17:24:38.009705+00	2025-10-21 21:50:08.270518+00	\N
126	f	\N	56	томат обыкновенный	\N	2025-10-21 21:50:08.271146+00	2025-10-16 17:24:38.010603+00	2025-10-21 21:50:08.271167+00	\N
127	f	\N	10	тритикале	\N	2025-10-21 21:50:08.271787+00	2025-10-16 17:24:38.011353+00	2025-10-21 21:50:08.271807+00	\N
128	f	\N	32	тыква твердокорая овощная 	\N	2025-10-21 21:50:08.272458+00	2025-10-16 17:24:38.012016+00	2025-10-21 21:50:08.272479+00	\N
129	f	\N	711	укроп	\N	2025-10-21 21:50:08.273109+00	2025-10-16 17:24:38.012595+00	2025-10-21 21:50:08.27313+00	\N
130	f	\N	594	фасоль	\N	2025-10-21 21:50:08.273767+00	2025-10-16 17:24:38.013112+00	2025-10-21 21:50:08.273787+00	\N
131	f	\N	44	фасоль овощная	\N	2025-10-21 21:50:08.274392+00	2025-10-16 17:24:38.013612+00	2025-10-21 21:50:08.274412+00	\N
132	f	\N	491	фундук	\N	2025-10-21 21:50:08.275053+00	2025-10-16 17:24:38.014108+00	2025-10-21 21:50:08.275081+00	\N
133	f	\N	67	хлопчатник	\N	2025-10-21 21:50:08.27575+00	2025-10-16 17:24:38.014624+00	2025-10-21 21:50:08.275771+00	\N
134	f	\N	783	Цветная капуста (Новая методика)	\N	2025-10-21 21:50:08.276447+00	2025-10-16 17:24:38.015162+00	2025-10-21 21:50:08.276465+00	\N
135	f	\N	78	черешня наст.	\N	2025-10-21 21:50:08.277379+00	2025-10-16 17:24:38.015672+00	2025-10-21 21:50:08.277407+00	\N
136	f	\N	729	черешня (по старой методике)	\N	2025-10-21 21:50:08.278169+00	2025-10-16 17:24:38.016172+00	2025-10-21 21:50:08.278189+00	\N
137	f	\N	72	черная смородина	\N	2025-10-21 21:50:08.278824+00	2025-10-16 17:24:38.016718+00	2025-10-21 21:50:08.278845+00	\N
138	f	\N	55	чеснок озимый	\N	2025-10-21 21:50:08.279484+00	2025-10-16 17:24:38.017186+00	2025-10-21 21:50:08.279505+00	\N
139	f	\N	715	чеснок озимый (по старой методике)	\N	2025-10-21 21:50:08.280148+00	2025-10-16 17:24:38.017898+00	2025-10-21 21:50:08.280169+00	\N
140	f	\N	54	чеснок яровой	\N	2025-10-21 21:50:08.280987+00	2025-10-16 17:24:38.01865+00	2025-10-21 21:50:08.281008+00	\N
141	f	\N	295	Чечевица	\N	2025-10-21 21:50:08.281685+00	2025-10-16 17:24:38.01943+00	2025-10-21 21:50:08.281705+00	\N
142	f	\N	740	Шпинат (Новая методика)	\N	2025-10-21 21:50:08.282439+00	2025-10-16 17:24:38.020192+00	2025-10-21 21:50:08.282461+00	\N
143	f	\N	52	эcпарцет 	\N	2025-10-21 21:50:08.283184+00	2025-10-16 17:24:38.020795+00	2025-10-21 21:50:08.283205+00	\N
144	f	\N	575	эспарцет	\N	2025-10-21 21:50:08.283873+00	2025-10-16 17:24:38.021386+00	2025-10-21 21:50:08.283894+00	\N
145	f	\N	543	Эхинацея	\N	2025-10-21 21:50:08.284569+00	2025-10-16 17:24:38.02203+00	2025-10-21 21:50:08.284589+00	\N
146	f	\N	73	яблоня	\N	2025-10-21 21:50:08.285213+00	2025-10-16 17:24:38.022584+00	2025-10-21 21:50:08.285233+00	\N
147	f	\N	736	яблоня (по старой методике)	\N	2025-10-21 21:50:08.286253+00	2025-10-16 17:24:38.023151+00	2025-10-21 21:50:08.286276+00	\N
148	f	\N	713	Яблоня (по старой методике)	\N	2025-10-21 21:50:08.286936+00	2025-10-16 17:24:38.023935+00	2025-10-21 21:50:08.286956+00	\N
149	f	\N	9	ячмень 	\N	2025-10-21 21:50:08.287587+00	2025-10-16 17:24:38.02441+00	2025-10-21 21:50:08.287607+00	\N
150	f	\N	704	Ячмень (новая)	\N	2025-10-21 21:50:08.288227+00	2025-10-16 17:24:38.024946+00	2025-10-21 21:50:08.288248+00	\N
\.


--
-- Data for Name: trials_app_document; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.trials_app_document (id, is_deleted, deleted_at, title, document_type, file, description, uploaded_at, is_mandatory, application_id, trial_id, uploaded_by_id) FROM stdin;
1	f	\N	REFEREE_REPORT_5	application_for_testing	documents/2025/10/16/REFEREE_REPORT_5_eELboqt.pdf	\N	2025-10-16 09:00:26.838006+00	t	1	\N	1
2	f	\N	REFEREE_REPORT_5	variety_description	documents/2025/10/16/REFEREE_REPORT_5_0hzuWte.pdf	\N	2025-10-16 09:00:26.83813+00	t	1	\N	1
3	f	\N	REFEREE_REPORT_5	breeding_questionnaire	documents/2025/10/16/REFEREE_REPORT_5_5zXZDaN.pdf	\N	2025-10-16 09:00:26.838284+00	t	1	\N	1
4	f	\N	REFEREE_REPORT_5	plant_photo_with_ruler	documents/2025/10/16/REFEREE_REPORT_5_ujhcun1.pdf	\N	2025-10-16 09:00:26.841444+00	t	1	\N	1
5	f	\N	REFEREE_REPORT_5	breeding_questionnaire	documents/2025/10/16/REFEREE_REPORT_5_i7sgr00.pdf	\N	2025-10-16 09:01:15.946287+00	t	2	\N	1
6	f	\N	REFEREE_REPORT_5	application_for_testing	documents/2025/10/16/REFEREE_REPORT_5_3EhKMtY.pdf	\N	2025-10-16 09:01:15.947439+00	t	2	\N	1
7	f	\N	REFEREE_REPORT_5	plant_photo_with_ruler	documents/2025/10/16/REFEREE_REPORT_5_HJJtbLR.pdf	\N	2025-10-16 09:01:15.949613+00	t	2	\N	1
8	f	\N	REFEREE_REPORT_5	variety_description	documents/2025/10/16/REFEREE_REPORT_5_PNtG9aM.pdf	\N	2025-10-16 09:01:15.952831+00	t	2	\N	1
9	f	\N	REFEREE_REPORT_5	breeding_questionnaire	documents/2025/10/16/REFEREE_REPORT_5_HQvY3Lk.pdf	\N	2025-10-16 09:02:16.668948+00	t	3	\N	1
10	f	\N	REFEREE_REPORT_5	variety_description	documents/2025/10/16/REFEREE_REPORT_5_nqwN2MF.pdf	\N	2025-10-16 09:02:16.670045+00	t	3	\N	1
11	f	\N	REFEREE_REPORT_5	plant_photo_with_ruler	documents/2025/10/16/REFEREE_REPORT_5_pW2Dqsr.pdf	\N	2025-10-16 09:02:16.670207+00	t	3	\N	1
12	f	\N	REFEREE_REPORT_5	application_for_testing	documents/2025/10/16/REFEREE_REPORT_5_zArZ6wb.pdf	\N	2025-10-16 09:02:16.671388+00	t	3	\N	1
13	f	\N	REFEREE_REPORT_5	plant_photo_with_ruler	documents/2025/10/16/REFEREE_REPORT_5_rAn5FGk.pdf	\N	2025-10-16 09:03:46.41081+00	t	4	\N	1
14	f	\N	REFEREE_REPORT_5	application_for_testing	documents/2025/10/16/REFEREE_REPORT_5_XeODBN2.pdf	\N	2025-10-16 09:03:46.410926+00	t	4	\N	1
15	f	\N	REFEREE_REPORT_5	variety_description	documents/2025/10/16/REFEREE_REPORT_5_xRgwyxZ.pdf	\N	2025-10-16 09:03:46.41104+00	t	4	\N	1
16	f	\N	REFEREE_REPORT_5	breeding_questionnaire	documents/2025/10/16/REFEREE_REPORT_5_FZbxYmE.pdf	\N	2025-10-16 09:03:46.411174+00	t	4	\N	1
17	f	\N	REFEREE_REPORT_5	breeding_questionnaire	documents/2025/10/16/REFEREE_REPORT_5_sQ6gqK8.pdf	\N	2025-10-16 09:04:46.349146+00	t	5	\N	1
18	f	\N	REFEREE_REPORT_5	application_for_testing	documents/2025/10/16/REFEREE_REPORT_5_WFWIOMf.pdf	\N	2025-10-16 09:04:46.352302+00	t	5	\N	1
19	f	\N	REFEREE_REPORT_5	plant_photo_with_ruler	documents/2025/10/16/REFEREE_REPORT_5_nI7Lfsx.pdf	\N	2025-10-16 09:04:46.352879+00	t	5	\N	1
20	f	\N	REFEREE_REPORT_5	variety_description	documents/2025/10/16/REFEREE_REPORT_5_Jaci7u6.pdf	\N	2025-10-16 09:04:46.353013+00	t	5	\N	1
21	f	\N	NDA_Nurali_signed	application_for_testing	documents/2025/10/20/NDA_Nurali_signed.pdf	\N	2025-10-20 07:33:24.327009+00	t	6	\N	1
22	f	\N	NDA_Nurali_signed	variety_description	documents/2025/10/20/NDA_Nurali_signed_CMuXXdM.pdf	\N	2025-10-20 07:33:24.332656+00	t	6	\N	1
23	f	\N	Договор оказания услуг № 2_signed	plant_photo_with_ruler	documents/2025/10/20/Договор_оказания_услуг__2_signed.pdf	\N	2025-10-20 07:33:24.332841+00	t	6	\N	1
24	f	\N	NDA_Nurali_signed	breeding_questionnaire	documents/2025/10/20/NDA_Nurali_signed_a9YZiRP.pdf	\N	2025-10-20 07:33:24.333593+00	t	6	\N	1
25	f	\N	NDA_Nurali_signed	application_for_testing	documents/2025/10/20/NDA_Nurali_signed_vVlEbiS.pdf	\N	2025-10-20 09:58:43.776981+00	t	7	\N	1
26	f	\N	NDA_Nurali_signed	breeding_questionnaire	documents/2025/10/20/NDA_Nurali_signed_Lewmnpg.pdf	\N	2025-10-20 09:58:43.777104+00	t	7	\N	1
27	f	\N	Договор оказания услуг № 2_signed	plant_photo_with_ruler	documents/2025/10/20/Договор_оказания_услуг__2_signed_GVHwKTu.pdf	\N	2025-10-20 09:58:43.778682+00	t	7	\N	1
28	f	\N	Договор оказания услуг № 2_signed	variety_description	documents/2025/10/20/Договор_оказания_услуг__2_signed_uuH2tc5.pdf	\N	2025-10-20 09:58:43.77883+00	t	7	\N	1
\.


--
-- Data for Name: trials_app_groupculture; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.trials_app_groupculture (id, is_deleted, deleted_at, group_culture_id, name, description, code, synced_at, created_at, updated_at) FROM stdin;
1	f	\N	1	Зерновые	Пшеница мягкая\nПшеница твердая\nЯчмень\nРожь\nТритикале\nПшеница тургидум\nОвес\nКукуруза\nСорго	GRAIN	\N	2025-10-16 09:00:26.784746+00	2025-10-20 09:58:43.714784+00
2	f	\N	8	Updated Group 1759959034	дыня, арбуз	melons	\N	2025-10-16 17:22:08.441802+00	2025-10-16 17:22:08.441811+00
3	f	\N	2	Зернобобовые	Горох\nЧечевица\nМаш\nЧина\nНут\nФасоль	LEGUMES	\N	2025-10-16 17:22:08.444578+00	2025-10-16 17:22:08.444594+00
4	f	\N	6	Кормовые	Донник белый\nДонник волжский\nДонник желтый\nДонник зубчатый\nЖитняк узкоколосый\nЖитняк ширококолосый\nКострец безостый\nКострец прямой\nЛюцерна\nСуданская трава\nАмарант метельчатый\nАстрагал лисий\nАстрагал лисовидный\nАстрагал миндальный\nАстрагал шарагаловый\nВайда Буассье\nВика полевая\nВика посевная\nГорец забайкальский\nЕжа сборная\nЖузгун безлистный\nЖузгун белокорый\nЖузгун голова медузы\nЖузгун колючекрылый\nЖузгун Кызылкумский\nЖузгун мелкоплодный\nЖузгун обыкновенный\nЖузгун шерстистый\nКамфоросма Лессинга\nКанареечник тростниковый\nКейреук\nКлевер луговой\nКлевер ползучий\nКозлятник восточный\nЛебеда многоплодная\nЛомкоколосник ситниковый\nЛуговик дернистый\nЛядвенец рогатый\nМогар\nМятлик луговой\nМятлик обыкновенный\nОвсяница бороздчатая\nОвсяница красная\nОвсяница луговая\nОвсяница овечья\nОвсяница разнолистная\nОвсяница тростниковая\nПолевица побегоносная\nПолынь белоземельная\nПолынь гладкая\nПолынь солелюбивая\nПолынь туранская\nПросо африканское\nПрутняк (изень, кохия стелющаяся)\nПырей бескорневищный\nПырейник даурский\nПырейник сибирский\nПырей сизый\nРайграс гибридный\nРайграс многолетний\nРайграс однолетний\nСаксаул белый\nСаксаул черный\nСвекла кормовая\nСолянка (черкез) рихтера\nСорго веничное\nСорго-суданковый гибрид\nСурепица\nТерескен\nТерескен эверсмана\nТимофеевка луговая\nТопинамбур\nТопинсолнечник\nТурнепс\nТутовый шелкопряд\nЧогон\nЧумиза\nШелковица\nЭхинацея пурпурная\nЭспарцет	FORAGE	\N	2025-10-16 17:22:08.446964+00	2025-10-16 17:22:08.44697+00
5	f	\N	15	Крупяные	Просо\nГречиха\nРис	porridge	\N	2025-10-16 17:22:08.448011+00	2025-10-16 17:22:08.448016+00
6	f	\N	14	Лесные деревья	Береза повислая\nПавловния\nСосна обыкновенная	TREES	\N	2025-10-16 17:22:08.448875+00	2025-10-16 17:22:08.44888+00
7	f	\N	9	Масличные	Подсолнечник\nклещевина\nГорчица сарептская\nГорчица белая\nСафлор\nСоя\nКунжут\nРапс\nРыжик\nЛен масличный	OILSEEDS	\N	2025-10-16 17:22:08.44975+00	2025-10-16 17:22:08.449757+00
8	f	\N	3	Овощные	Картофель\nКапуста белокачанная\nКапуста краснокачанная\nКапуста цветная\nКапуста пекинская\nКапуста брокколи\nСалат\nКапуста савойская\nШпинат\nЩавель\nУкроп\nРевень\nОгурец\nТомат\nЛук репчатый\nЛук баун\nЛук шалот\nЛук порей\nЧеснок\nМорковь\nСвекла столовая\nРепа\nБрюква\nРедька\nРедис\nПетрушка\nПастернак\nСельдерей\nДвурядник тонколистый\nМангольд\nБазилик овощной\nПерец\nБаклажан\nТыква\nКабачок\nПатиссон\nТурнепс	VEGETABLES	\N	2025-10-16 17:22:08.450806+00	2025-10-16 17:22:08.450811+00
9	f	\N	12	Орехоплодные	Миндаль\nОрех грецкий\nФундук	NUTS	\N	2025-10-16 17:22:08.452042+00	2025-10-16 17:22:08.452047+00
10	f	\N	4	Плодовые культуры и виноград	Яблоня\nГруша\nРябина\nАйва\nСлива\nАлыча\nВишня обыкновенная\nЧерешня\nАбрикос\nПерсик\nВиноград	FRUITS	\N	2025-10-16 17:22:08.452817+00	2025-10-16 17:22:08.452821+00
11	f	\N	10	Прядильные	Хлопчатник	COTTON	\N	2025-10-16 17:22:08.453642+00	2025-10-16 17:22:08.453647+00
12	f	\N	5	Технические	Свекла сахарная\nТабак\nКоксагыз	TECHNICAL	\N	2025-10-16 17:22:08.454324+00	2025-10-16 17:22:08.454328+00
13	f	\N	13	Цветочно-декоративные	Гиацинт\nГладиолус\nИрис\nКанна\nКлематис\nЛилейник\nЛилия\nНарцисс\nПион\nРозa\nРомашка аптечная\nСирень\nТагетес\nТюльпан\nУнаби обыкновенная\nФацелия пижмолистная\nФрезия\nХризантема\nЦинния	FLOWERS	\N	2025-10-16 17:22:08.455212+00	2025-10-16 17:22:08.455216+00
14	f	\N	11	Цитрусовые и субтропические	Инжир\nГранат\nУнаби\nбанан	TROPICAL	\N	2025-10-16 17:22:08.455847+00	2025-10-16 17:22:08.45585+00
15	f	\N	7	Ягодные	земляника\nсмородина черная\nсмородина красная\nсмородина белая\nмалина\nежевика\nкрыжовник\nжимолость\nоблепиха\nголубика	BERRY	\N	2025-10-16 17:22:08.456544+00	2025-10-16 17:22:08.456548+00
16	t	\N	42	Обновленная тестовая группа	Обновленное описание для тестирования	\N	2025-10-21 22:02:47.35928+00	2025-10-21 22:02:33.590081+00	2025-10-21 22:02:52.124721+00
\.


--
-- Data for Name: trials_app_indicator; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.trials_app_indicator (id, is_deleted, deleted_at, code, name, unit, description, is_numeric, category, is_quality, sort_order, is_universal, created_at, updated_at, calculation_formula, is_auto_calculated, is_recommended, is_required, validation_rules) FROM stdin;
26	f	\N	baking_score	Общая хлебопекарная оценка	балл (1-5)	Комплексная хлебопекарная оценка	t	quality	t	113	f	2025-10-16 08:54:03.903265+00	2025-10-16 17:56:34.805865+00		f	t	f	{"max_value": 5, "min_value": 1, "precision": 1}
47	t	2025-10-16 18:38:04.551176+00	head_density	Плотность кочана	балл (1-5)	Плотность кочана капусты	t	common	f	63	f	2025-10-16 08:54:03.925137+00	2025-10-16 18:38:04.551234+00		f	t	f	{"max_value": 5, "min_value": 1, "precision": 1}
22	f	\N	threshability	Обмолачиваемость	балл (1-9)	Легкость обмолота зерна	t	common	f	24	f	2025-10-16 08:54:03.899378+00	2025-10-16 18:38:04.555906+00		f	t	f	{"max_value": 9, "min_value": 1, "precision": 0}
17	f	\N	shedding_resistance	Устойчивость к осыпанию	балл (1-9)	Устойчивость к осыпанию	t	common	f	15	f	2025-10-16 08:54:03.892943+00	2025-10-16 18:38:04.55781+00		f	t	f	{"max_value": 9, "min_value": 1, "precision": 0}
5	f	\N	plant_height	Высота растений	см	Высота растения или стеблестоя	t	common	f	5	f	2025-10-16 08:54:03.875089+00	2025-10-16 17:56:34.748214+00		f	t	f	{"max_value": 1000, "min_value": 0, "precision": 0}
20	f	\N	lodging_drooping_brittleness	Устойчивость к пониканию / ломкости колоса	балл (1-9)	Устойчивость колоса к пониканию и ломкости	t	common	f	22	f	2025-10-16 08:54:03.896807+00	2025-10-16 18:38:04.556723+00		f	t	f	{"max_value": 9, "min_value": 1, "precision": 0}
4	f	\N	vegetation_period	Вегетационный период	дней	Период от посева/всходов до созревания	t	common	f	4	f	2025-10-16 08:54:03.872927+00	2025-10-16 18:38:04.577986+00		f	t	f	{"max_value": 365, "min_value": 30, "precision": 0}
9	f	\N	winter_hardiness	Зимостойкость	балл (1-9)	Устойчивость к зимним условиям (для озимых и многолетних)	t	common	f	9	f	2025-10-16 08:54:03.881948+00	2025-10-16 17:56:34.762731+00		f	t	f	{"max_value": 9, "min_value": 1, "precision": 0}
53	f	\N	emergence_completeness	Полнота всходов	%	Полнота всходов, определяется после полных всходов	t	common	f	50	f	2025-10-17 21:56:42.502362+00	2025-10-17 21:56:42.502374+00	\N	f	t	f	{}
8	f	\N	disease_pest_resistance	Устойчивость к болезням и вредителям	балл (1-9)	Общая устойчивость к болезням и вредителям	t	common	f	8	f	2025-10-16 08:54:03.879554+00	2025-10-16 17:56:34.758579+00		f	t	f	{"max_value": 9, "min_value": 0, "precision": 0}
2	f	\N	deviation_standard_abs	Отклонение от стандарта (абсолютное)	ц/га	Отклонение урожайности от стандартного сорта в ц/га	t	common	f	2	f	2025-10-16 08:54:03.870284+00	2025-10-16 17:56:34.737078+00	Урожайность участника - Урожайность стандарта	t	t	f	{}
51	f	\N	fruit_berry_weight	Средняя масса плода/ягоды	г	Средняя масса одного плода или ягоды	t	common	f	70	f	2025-10-16 08:54:03.928762+00	2025-10-16 18:38:04.565439+00		f	t	t	{}
12	f	\N	marketability	Товарность	%	Процент товарной продукции от общего урожая	t	common	f	12	f	2025-10-16 08:54:03.885947+00	2025-10-16 18:38:04.566414+00	(Товарная урожайность / Общая урожайность) × 100	t	t	f	{"max_value": 100, "min_value": 0, "precision": 1}
14	f	\N	protein_content	Содержание белка/протеина	%	Лабораторный анализ содержания белка	t	quality	t	100	f	2025-10-16 08:54:03.888948+00	2025-10-16 18:38:04.568585+00		f	t	t	{"max_value": 50, "min_value": 0, "precision": 1}
6	f	\N	lodging_resistance	Устойчивость к полеганию	балл (1-9)	Устойчивость к полеганию стеблей	t	common	f	6	f	2025-10-16 08:54:03.876678+00	2025-10-16 18:38:04.572567+00		f	t	f	{"max_value": 9, "min_value": 1, "precision": 0}
7	f	\N	drought_resistance	Устойчивость к засухе	балл (1-9)	Устойчивость к засушливым условиям	t	common	f	7	f	2025-10-16 08:54:03.878091+00	2025-10-16 18:38:04.573221+00		f	t	f	{"max_value": 9, "min_value": 1, "precision": 0}
10	f	\N	thousand_seed_weight	Масса 1000 зёрен/семян	г	Масса 1000 семян или зёрен	t	common	f	10	f	2025-10-16 08:54:03.883282+00	2025-10-16 18:38:04.575729+00		f	t	t	{"max_value": 1000, "min_value": 1, "precision": 1}
50	f	\N	days_to_first_harvest	Период до первого сбора	дней	От всходов до первого сбора урожая	t	common	f	65	f	2025-10-16 08:54:03.92757+00	2025-10-16 18:38:04.578863+00		f	t	f	{"max_value": 365, "min_value": 30, "precision": 0}
11	f	\N	variety_rating	Общая оценка сорта	балл (1-9)	Комплексная оценка сорта	t	common	f	11	f	2025-10-16 08:54:03.884765+00	2025-10-16 18:38:04.579726+00		f	f	f	{"max_value": 9, "min_value": 1, "precision": 0}
13	f	\N	tasting_score	Дегустационная оценка	балл (1-5)	Органолептическая оценка вкусовых качеств	t	common	f	13	f	2025-10-16 08:54:03.887492+00	2025-10-16 18:38:04.580327+00		f	f	f	{"max_value": 5, "min_value": 1, "precision": 1}
29	f	\N	ear_attachment_height	Высота прикрепления нижнего початка	см	Высота первого початка от земли (кукуруза)	t	specific	f	32	f	2025-10-16 08:54:03.906232+00	2025-10-16 17:56:34.812683+00		f	t	f	{}
30	f	\N	ears_per_plant	Количество початков на растении	шт.	Число початков на одном растении (кукуруза)	t	specific	f	33	f	2025-10-16 08:54:03.907109+00	2025-10-16 17:56:34.815103+00		f	t	f	{}
33	f	\N	leafiness	Облиственность	%	Доля листьев в общей массе растения	t	common	f	42	f	2025-10-16 08:54:03.91001+00	2025-10-16 17:56:34.822535+00		f	t	f	{}
34	f	\N	fiber_content	Содержание клетчатки	%	Содержание сырой клетчатки	t	quality	t	120	f	2025-10-16 08:54:03.91148+00	2025-10-16 17:56:34.824914+00		f	t	f	{}
35	f	\N	fat_content	Содержание жира	%	Содержание сырого жира	t	quality	t	121	f	2025-10-16 08:54:03.912705+00	2025-10-16 17:56:34.827119+00		f	t	f	{}
36	f	\N	starch_content	Содержание крахмала	%	Содержание крахмала (для силосных)	t	quality	t	122	f	2025-10-16 08:54:03.914056+00	2025-10-16 17:56:34.829544+00		f	t	f	{}
16	f	\N	vitamin_c_content	Содержание витамина С	мг/%	Лабораторный анализ витамина С	t	quality	t	102	f	2025-10-16 08:54:03.891545+00	2025-10-16 17:56:34.783535+00		f	t	f	{}
27	f	\N	ear_weight	Масса початка	г	Средняя масса одного початка (кукуруза)	t	specific	f	30	f	2025-10-16 08:54:03.904383+00	2025-10-16 17:56:34.807933+00		f	t	f	{}
21	f	\N	germination_resistance	Устойчивость к прорастанию на корню	балл (1-9)	Устойчивость зерна к прорастанию до уборки	t	common	f	23	f	2025-10-16 08:54:03.898351+00	2025-10-16 17:56:34.795129+00		f	t	f	{"max_value": 9, "min_value": 1, "precision": 0}
40	f	\N	early_yield	Ранняя урожайность	ц/га	Урожайность от первых сборов	t	common	f	60	f	2025-10-16 08:54:03.918333+00	2025-10-16 17:56:34.837501+00		f	t	f	{}
41	f	\N	total_marketable_yield	Товарная урожайность	ц/га	Урожайность товарной продукции	t	common	f	61	f	2025-10-16 08:54:03.91943+00	2025-10-16 17:56:34.839734+00	Общая урожайность × (Товарность / 100)	t	t	f	{}
18	f	\N	grain_nature	Натура зерна	г/л	Объёмная масса зерна (только для зерновых)	t	common	f	20	f	2025-10-16 08:54:03.894392+00	2025-10-16 18:38:04.555038+00		f	t	f	{}
25	f	\N	bread_volume	Объём хлеба	мл	Объём хлеба из муки (хлебопекарное качество)	t	quality	t	112	f	2025-10-16 08:54:03.902126+00	2025-10-16 17:56:34.803053+00		f	t	f	{}
37	f	\N	seeds_per_basket	Масса семян в одной корзинке/коробочке/стручке	г	Масса семян из одного соцветия/плода	t	specific	f	50	f	2025-10-16 08:54:03.915398+00	2025-10-16 17:56:34.83132+00		f	t	f	{}
19	f	\N	tillering	Продуктивная кустистость	шт. продуктивных стеблей	Количество продуктивных стеблей на растении	t	common	f	21	f	2025-10-16 08:54:03.895575+00	2025-10-16 17:56:34.790761+00		f	t	f	{}
45	f	\N	carotenoids_content	Содержание каротиноидов (морковь)	%	Содержание каротиноидов (провитамин А)	t	quality	t	142	f	2025-10-16 08:54:03.92352+00	2025-10-16 17:56:34.848317+00		f	t	f	{}
46	f	\N	sugar_content_beet	Содержание сахара (свёкла)	%	Содержание сахара в столовой свёкле	t	quality	t	143	f	2025-10-16 08:54:03.924345+00	2025-10-16 17:56:34.850057+00		f	t	f	{}
24	f	\N	vitreousness	Стекловидность	%	Стекловидность зерна	t	quality	t	111	f	2025-10-16 08:54:03.901217+00	2025-10-16 18:38:04.570158+00		f	t	f	{"max_value": 100, "min_value": 0, "precision": 1}
31	f	\N	green_mass_yield	Урожайность зеленой массы	ц/га	Урожай зеленой (свежей) массы	t	common	f	40	f	2025-10-16 08:54:03.907994+00	2025-10-16 18:38:04.574745+00		f	t	t	{"max_value": 2000, "min_value": 0, "precision": 1}
28	f	\N	grain_output	Выход зерна	%	Процент зерна от массы початка (кукуруза)	t	specific	f	31	f	2025-10-16 08:54:03.905321+00	2025-10-16 17:56:34.810139+00	(Масса зерна / Масса початка) × 100	f	t	f	{}
23	f	\N	gluten_content	Содержание клейковины	%	Содержание клейковины (для пшеницы)	t	quality	t	110	f	2025-10-16 08:54:03.900329+00	2025-10-16 18:38:04.56935+00		f	t	f	{"max_value": 50, "min_value": 0, "precision": 1}
32	f	\N	dry_matter_yield	Урожайность сухого вещества	ц/га	Урожай в пересчете на абсолютно сухое вещество	t	common	f	41	f	2025-10-16 08:54:03.908847+00	2025-10-16 18:38:04.561671+00		f	t	t	{}
15	f	\N	dry_matter_content	Содержание сухого вещества	%	Процент сухого вещества в общей массе	t	quality	t	101	f	2025-10-16 08:54:03.890305+00	2025-10-16 18:38:04.562335+00		f	t	t	{}
43	f	\N	starch_content_tubers	Содержание крахмала (картофель)	%	Содержание крахмала в клубнях	t	quality	t	140	f	2025-10-16 08:54:03.921499+00	2025-10-16 18:38:04.563857+00		f	t	t	{}
44	f	\N	storability	Лёжкость при хранении	%	Процент сохранившейся продукции после хранения	t	quality	t	141	f	2025-10-16 08:54:03.922457+00	2025-10-16 18:38:04.564537+00		f	t	t	{}
3	f	\N	deviation_standard_pct	Отклонение от стандарта (%)	%	Отклонение урожайности от стандартного сорта в процентах	t	common	f	3	f	2025-10-16 08:54:03.871645+00	2025-10-16 18:38:04.567559+00	((Урожайность участника - Урожайность стандарта) / Урожайность стандарта) × 100	t	t	f	{"max_value": 1000, "min_value": -100, "precision": 1}
49	f	\N	juice_dry_matter	Содержание сухого вещества в соке (томат)	%	Сухое вещество в соке томата	t	quality	t	144	f	2025-10-16 08:54:03.926742+00	2025-10-16 17:56:34.856374+00		f	t	f	{}
52	f	\N	sugar_content_grapes	Сахаристость (виноград)	%	Содержание сахара в ягодах винограда	t	quality	t	150	f	2025-10-16 08:54:03.92985+00	2025-10-16 17:56:34.863378+00		f	t	f	{}
39	f	\N	oil_content	Содержание масла	%	Масличность семян	t	quality	t	130	f	2025-10-16 08:54:03.917438+00	2025-10-16 17:56:34.834949+00		f	t	f	{}
38	t	2025-10-16 18:38:04.548993+00	ripening_uniformity	Выравненность созревания	%	Процент одновременно созревших растений	t	common	f	51	f	2025-10-16 08:54:03.916518+00	2025-10-16 18:38:04.549072+00		f	t	f	{}
48	t	2025-10-16 18:38:04.551961+00	bolting_resistance	Устойчивость к цветушности	%	Устойчивость к преждевременному стрелкованию	t	common	f	64	f	2025-10-16 08:54:03.925928+00	2025-10-16 18:38:04.551993+00		f	t	f	{}
1	f	\N	yield	Урожайность	ц/га	Общий показатель урожайности для большинства культур	t	common	f	1	f	2025-10-16 08:54:03.866366+00	2025-10-16 18:38:04.573904+00		f	t	t	{"max_value": 1000, "min_value": 0, "precision": 1}
42	f	\N	fruit_vegetable_weight	Средняя масса плода/корнеплода/кочана	г	Средний вес товарного плода/корнеплода	t	common	f	62	f	2025-10-16 08:54:03.920364+00	2025-10-16 18:38:04.576833+00		f	t	t	{"max_value": 50000, "min_value": 1, "precision": 1}
\.


--
-- Data for Name: trials_app_indicator_group_cultures; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.trials_app_indicator_group_cultures (id, indicator_id, groupculture_id) FROM stdin;
1	1	1
2	1	2
3	1	3
4	1	4
5	1	7
6	1	8
7	1	10
8	1	15
9	2	1
10	2	3
11	2	7
12	3	1
13	3	3
14	3	7
15	4	1
16	4	2
17	4	3
18	4	4
19	4	7
20	4	8
21	5	1
22	5	3
23	5	4
24	5	7
25	6	1
26	6	3
27	6	4
28	6	7
29	7	1
30	7	3
31	7	4
32	7	7
33	8	1
34	8	2
35	8	3
36	8	4
37	8	7
38	8	8
39	8	10
40	8	15
41	9	1
42	9	3
43	9	4
44	10	1
45	10	3
46	10	4
47	10	7
48	11	1
49	11	3
50	11	7
51	12	8
52	12	2
53	12	10
54	12	15
55	13	8
56	13	2
57	13	10
58	13	15
59	14	1
60	14	3
61	14	4
62	15	8
63	15	2
64	15	4
65	16	8
66	16	2
67	17	3
68	18	1
69	19	1
70	20	1
71	21	1
72	22	1
73	23	1
74	24	1
75	25	1
76	26	1
77	27	1
78	28	1
79	29	1
80	30	1
81	31	4
82	32	4
83	33	4
84	34	4
85	35	4
86	36	4
87	37	7
88	38	7
89	39	7
90	40	8
91	40	2
92	41	8
93	42	8
94	42	2
95	43	8
96	44	8
97	44	10
98	45	8
99	46	8
100	47	8
101	48	8
102	49	8
103	50	8
104	50	2
105	51	10
106	51	15
107	52	10
108	17	1
109	53	1
\.


--
-- Data for Name: trials_app_oblast; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.trials_app_oblast (id, is_deleted, deleted_at, name, code, created_at, updated_at) FROM stdin;
1	f	\N	Акмолинская	01	2025-10-16 08:53:45.939071+00	2025-10-16 08:53:45.93908+00
2	f	\N	Актюбинская	02	2025-10-16 08:53:45.940698+00	2025-10-16 08:53:45.940704+00
3	f	\N	Алматинская	03	2025-10-16 08:53:45.941474+00	2025-10-16 08:53:45.941479+00
4	f	\N	Атырауская	04	2025-10-16 08:53:45.942124+00	2025-10-16 08:53:45.942128+00
5	f	\N	Восточно-Казахстанская	05	2025-10-16 08:53:45.942673+00	2025-10-16 08:53:45.942676+00
6	f	\N	Жамбылская	06	2025-10-16 08:53:45.943202+00	2025-10-16 08:53:45.943205+00
7	f	\N	Западно-Казахстанская	07	2025-10-16 08:53:45.943813+00	2025-10-16 08:53:45.943817+00
8	f	\N	Карагандинская	08	2025-10-16 08:53:45.944353+00	2025-10-16 08:53:45.944356+00
9	f	\N	Костанайская	09	2025-10-16 08:53:45.944844+00	2025-10-16 08:53:45.944848+00
10	f	\N	Кызылординская	10	2025-10-16 08:53:45.945354+00	2025-10-16 08:53:45.945357+00
11	f	\N	Мангистауская	11	2025-10-16 08:53:45.945827+00	2025-10-16 08:53:45.94583+00
12	f	\N	Павлодарская	12	2025-10-16 08:53:45.946294+00	2025-10-16 08:53:45.946297+00
13	f	\N	Северо-Казахстанская	13	2025-10-16 08:53:45.946768+00	2025-10-16 08:53:45.946771+00
14	f	\N	Туркестанская	14	2025-10-16 08:53:45.947279+00	2025-10-16 08:53:45.947282+00
15	f	\N	Улытау	15	2025-10-16 08:53:45.947746+00	2025-10-16 08:53:45.947749+00
16	f	\N	Абай	16	2025-10-16 08:53:45.948221+00	2025-10-16 08:53:45.948224+00
17	f	\N	Жетісу	17	2025-10-16 08:53:45.948689+00	2025-10-16 08:53:45.948692+00
\.


--
-- Data for Name: trials_app_originator; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.trials_app_originator (id, is_deleted, deleted_at, originator_id, name, synced_at, created_at, updated_at, code, is_foreign, is_nanoc) FROM stdin;
4	f	\N	7847	ANHUI LONGPING HIGH-TECH (XINQIAO) SEEDS CO., LTD., Китай	2025-10-16 17:31:25.446805+00	2025-10-16 17:31:25.447273+00	2025-10-16 17:31:25.447277+00	\N	f	f
25	f	\N	6044	Danko Hodowla Roslin Sp. zо.о.	2025-10-16 17:31:25.45995+00	2025-10-16 17:31:25.460176+00	2025-10-16 17:31:25.460179+00	\N	f	f
28	f	\N	7797	Donau Saat S.R.L.	2025-10-16 17:31:25.461392+00	2025-10-16 17:31:25.461612+00	2025-10-16 17:31:25.461614+00	\N	f	f
33	f	\N	7719	Fall Greek Farm & Nursey Ink.	2025-10-16 17:31:25.464725+00	2025-10-16 17:31:25.465032+00	2025-10-16 17:31:25.465035+00	\N	f	f
34	f	\N	7839	Fenikks Seeds Global Ltd. Китай	2025-10-16 17:31:25.465295+00	2025-10-16 17:31:25.465529+00	2025-10-16 17:31:25.465532+00	\N	f	f
36	f	\N	7079	Frito Lay North America, Inc.	2025-10-16 17:31:25.466216+00	2025-10-16 17:31:25.466442+00	2025-10-16 17:31:25.466445+00	\N	f	f
37	f	\N	7829	Gansu Jiarui Seeds Co.Itd	2025-10-16 17:31:25.466689+00	2025-10-16 17:31:25.466914+00	2025-10-16 17:31:25.466917+00	\N	f	f
43	f	\N	7801	Heilongjiang Longke Seed Industry Group, Ltd	2025-10-16 17:31:25.469489+00	2025-10-16 17:31:25.469723+00	2025-10-16 17:31:25.469726+00	\N	f	f
45	f	\N	5768	IMCCS  AMC Magroselect  SRU	2025-10-16 17:31:25.470518+00	2025-10-16 17:31:25.470867+00	2025-10-16 17:31:25.470891+00	\N	f	f
48	f	\N	6615	Intraseed ltd,Молдава	2025-10-16 17:31:25.472715+00	2025-10-16 17:31:25.473049+00	2025-10-16 17:31:25.473052+00	\N	f	f
53	f	\N	7810	Jinli Agriculture Development Co., Ltd	2025-10-16 17:31:25.475403+00	2025-10-16 17:31:25.475637+00	2025-10-16 17:31:25.475639+00	\N	f	f
54	f	\N	7822	Jiuquan Bosher flora Seed Industry Co	2025-10-16 17:31:25.475915+00	2025-10-16 17:31:25.476157+00	2025-10-16 17:31:25.476159+00	\N	f	f
56	f	\N	7848	JTSD LTD, UK	2025-10-16 17:31:25.476868+00	2025-10-16 17:31:25.477089+00	2025-10-16 17:31:25.477092+00	\N	f	f
67	f	\N	7852	Moguer Cuna de Platero, Sociedad Cooperativa Andaluza (S.C.A.) (Могер Куна дэ Платеро, Сосьедад Кооператива Андалуза (Эс.Cи.A.) (ES)	2025-10-16 17:31:25.482444+00	2025-10-16 17:31:25.482683+00	2025-10-16 17:31:25.482686+00	\N	f	f
70	f	\N	7818	"MTI Maize Technologies International"	2025-10-16 17:31:25.483758+00	2025-10-16 17:31:25.483987+00	2025-10-16 17:31:25.483989+00	\N	f	f
71	f	\N	6786	Na Jong Hyeon 	2025-10-16 17:31:25.4842+00	2025-10-16 17:31:25.484414+00	2025-10-16 17:31:25.484416+00	\N	f	f
73	f	\N	7809	National Agricultural Reserch and Development Institute Fundelea	2025-10-16 17:31:25.485048+00	2025-10-16 17:31:25.485256+00	2025-10-16 17:31:25.485259+00	\N	f	f
19	f	\N	7333	BREUN SEED GmbH&Co KG, Германия	2025-10-22 07:34:02.430908+00	2025-10-16 17:31:25.457065+00	2025-10-22 07:34:02.430927+00	340	f	f
40	f	\N	7702	GIE LINEA Semences de Lin, Франция	2025-10-22 07:34:02.442065+00	2025-10-16 17:31:25.468317+00	2025-10-22 07:34:02.442085+00	459	f	f
50	f	\N	6237	HIBRISOL, S.L., Испания	2025-10-22 07:34:02.443738+00	2025-10-16 17:31:25.474036+00	2025-10-22 07:34:02.443757+00	480	f	f
1070	f	\N	6867	Agri Obtentions SA., Франция	2025-10-22 07:34:02.424257+00	2025-10-22 07:34:02.424699+00	2025-10-22 07:34:02.424702+00	412	f	f
3	f	\N	7824	Alfaseed KFT, Венгрия	2025-10-22 07:34:02.426076+00	2025-10-16 17:31:25.446215+00	2025-10-22 07:34:02.426103+00	483	f	f
10	f	\N	6079	Aspria seeds S.A., Люксенбург	2025-10-22 07:34:02.427598+00	2025-10-16 17:31:25.451141+00	2025-10-22 07:34:02.42762+00	346	f	f
13	f	\N	6246	Bass Genetics Inc, Соединенные Штаты Америки	2025-10-22 07:34:02.429891+00	2025-10-16 17:31:25.452822+00	2025-10-22 07:34:02.42991+00	437	f	f
15	f	\N	5701	Bayer CropScience Raps GmbH, Германия	2025-10-22 07:34:02.430361+00	2025-10-16 17:31:25.453856+00	2025-10-22 07:34:02.43038+00	342	f	f
21	f	\N	6222	Cerela Inc., Канада	2025-10-22 07:34:02.431431+00	2025-10-16 17:31:25.458238+00	2025-10-22 07:34:02.43145+00	454	f	f
27	f	\N	5859	DLF SEEDS A/S, Дания	2025-10-22 07:34:02.436788+00	2025-10-16 17:31:25.461159+00	2025-10-22 07:34:02.436808+00	473	f	f
47	f	\N	6585	Interseed Potatoes Gesellschaft mit beschränkter Haftung, Германия	2025-10-22 07:34:02.444917+00	2025-10-16 17:31:25.472406+00	2025-10-22 07:34:02.444936+00	414	f	f
49	f	\N	6144	IPM Pototo Group, Ирландия	2025-10-22 07:34:02.445583+00	2025-10-16 17:31:25.473564+00	2025-10-22 07:34:02.445602+00	396	f	f
60	f	\N	6491	Lidea France SAS., Франция	2025-10-22 07:34:02.449454+00	2025-10-16 17:31:25.478863+00	2025-10-22 07:34:02.449475+00	456	f	f
65	f	\N	7798	MAS Seeds, Франция	2025-10-22 07:34:02.449994+00	2025-10-16 17:31:25.481716+00	2025-10-22 07:34:02.450017+00	368	f	f
18	f	\N	6206	Wiersum Plantbreeding Besloten Vennootschap, Нидерланды	2025-10-22 07:34:02.467052+00	2025-10-16 17:31:25.456073+00	2025-10-22 07:34:02.467074+00	369	f	f
52	f	\N	6300	Джон Кит, Новая Зеландия	2025-10-22 07:34:02.521873+00	2025-10-16 17:31:25.474911+00	2025-10-22 07:34:02.521893+00	310	f	f
32	f	\N	6501	Евросорго (Eurosorgho), Франция	2025-10-22 07:34:02.529929+00	2025-10-16 17:31:25.464419+00	2025-10-22 07:34:02.529951+00	360	f	f
82	f	\N	6859	Pen Hirtigh BV, P.O.Вох 3 A A EMMELOORD, Nethenlands	2025-10-16 17:31:25.489658+00	2025-10-16 17:31:25.489931+00	2025-10-16 17:31:25.489934+00	\N	f	f
93	f	\N	6796	SAKA PflanzenzuchinGmbH & Co, KG	2025-10-16 17:31:25.494963+00	2025-10-16 17:31:25.495188+00	2025-10-16 17:31:25.495191+00	\N	f	f
98	f	\N	7790	SEMILLAS BATLLE, S.A	2025-10-16 17:31:25.497899+00	2025-10-16 17:31:25.498172+00	2025-10-16 17:31:25.498175+00	\N	f	f
99	f	\N	7827	SEMMILAS BATLLE S.A (СЕММИЛЛАС БАТЛЛЕ, С.А)	2025-10-16 17:31:25.498428+00	2025-10-16 17:31:25.498658+00	2025-10-16 17:31:25.49866+00	\N	f	f
107	f	\N	6295	Tarim University, Китай	2025-10-16 17:31:25.502682+00	2025-10-16 17:31:25.502915+00	2025-10-16 17:31:25.502918+00	\N	f	f
108	f	\N	6580	TOO"Land Master"AMG Agroselect Comert SRL	2025-10-16 17:31:25.503185+00	2025-10-16 17:31:25.50344+00	2025-10-16 17:31:25.503443+00	\N	f	f
110	f	\N	5900	Updated 1759945856	2025-10-16 17:31:25.504241+00	2025-10-16 17:31:25.504498+00	2025-10-16 17:31:25.504501+00	\N	f	f
111	f	\N	5952	Updated Originator Name	2025-10-16 17:31:25.504787+00	2025-10-16 17:31:25.505121+00	2025-10-16 17:31:25.505124+00	\N	f	f
113	f	\N	7821	Xinjiang Jiuyu Development Seed Co., Ltd	2025-10-16 17:31:25.506773+00	2025-10-16 17:31:25.507113+00	2025-10-16 17:31:25.507116+00	\N	f	f
116	f	\N	7757	АБЦз Гроуп Б.В./С.Р.Л. (BE)	2025-10-16 17:31:25.508432+00	2025-10-16 17:31:25.508661+00	2025-10-16 17:31:25.508664+00	\N	f	f
117	f	\N	6042	АГ Алюмни Сиид	2025-10-16 17:31:25.508894+00	2025-10-16 17:31:25.509118+00	2025-10-16 17:31:25.509121+00	\N	f	f
118	f	\N	7500	Агрикалчурал рисерч энд экстеншн сервисс Жежу спешиал селф-говернинг провинс	2025-10-16 17:31:25.509332+00	2025-10-16 17:31:25.509554+00	2025-10-16 17:31:25.509557+00	\N	f	f
124	f	\N	7106	Агро Плюс Коммерц. Хаубитрассе,Германия 	2025-10-16 17:31:25.512077+00	2025-10-16 17:31:25.512302+00	2025-10-16 17:31:25.512305+00	\N	f	f
1071	f	\N	7495	(CIP) Международный центр по картофелю, Перу	2025-10-22 07:34:02.432188+00	2025-10-22 07:34:02.432448+00	2025-10-22 07:34:02.43245+00	415	f	f
1072	f	\N	8291	Den Hartigh Besloten Vennootschap, Нидерланды366.	2025-10-22 07:34:02.434251+00	2025-10-22 07:34:02.434504+00	2025-10-22 07:34:02.434507+00	365	f	f
1073	f	\N	8307	DLF BEET SEED ApS, Дания468.	2025-10-22 07:34:02.435383+00	2025-10-22 07:34:02.435629+00	2025-10-22 07:34:02.435631+00	467	f	f
131	f	\N	7792	Адванта Сид Интернешнл	2025-10-16 17:31:25.515983+00	2025-10-16 17:31:25.516219+00	2025-10-16 17:31:25.516222+00	\N	f	f
1074	f	\N	8298	DLF (Dansk Landbrugs Frøselskab) SEEDS A/S (Aktieselskab), Дания418.	2025-10-22 07:34:02.435953+00	2025-10-22 07:34:02.436244+00	2025-10-22 07:34:02.436246+00	417	f	f
29	f	\N	5717	Dow AgroSciences limited liability company, Соединенные Штаты Америки	2025-10-22 07:34:02.437672+00	2025-10-16 17:31:25.462079+00	2025-10-22 07:34:02.437692+00	356	f	f
87	f	\N	7271	RAGT 2n, Франция	2025-10-22 07:34:02.457991+00	2025-10-16 17:31:25.492378+00	2025-10-22 07:34:02.45801+00	355	f	f
136	f	\N	7849	Американ Генетикс, Греция	2025-10-16 17:31:25.518176+00	2025-10-16 17:31:25.518386+00	2025-10-16 17:31:25.518388+00	\N	f	f
102	f	\N	7846	Research Institute for Cereals and Industrial Crops, Румыния	2025-10-22 07:34:02.458499+00	2025-10-16 17:31:25.500472+00	2025-10-22 07:34:02.458518+00	304	f	f
138	f	\N	6371	Ананьева Зинаида Петровна 	2025-10-16 17:31:25.519022+00	2025-10-16 17:31:25.519232+00	2025-10-16 17:31:25.519235+00	\N	f	f
86	f	\N	7789	Saatzucht Donau Ges.m.b.H. & CoKG, Австрия	2025-10-22 07:34:02.459007+00	2025-10-16 17:31:25.491895+00	2025-10-22 07:34:02.459027+00	481	f	f
95	f	\N	6861	«Secobra Recherches», Франция	2025-10-22 07:34:02.462985+00	2025-10-16 17:31:25.496263+00	2025-10-22 07:34:02.463005+00	316	f	f
132	f	\N	6448	Алматинский государственный университе	2025-10-22 07:34:02.477361+00	2025-10-16 17:31:25.516704+00	2025-10-22 07:34:02.477381+00	6	f	f
101	f	\N	6343	Societa Produttori Sementi Spa, Швейцария	2025-10-22 07:34:02.463881+00	2025-10-16 17:31:25.500003+00	2025-10-22 07:34:02.463901+00	385	f	f
112	f	\N	5775	Winall Hi – The Seed Co, Китайская Народная Республика	2025-10-22 07:34:02.467611+00	2025-10-16 17:31:25.506331+00	2025-10-22 07:34:02.46763+00	465	f	f
120	f	\N	6630	"Агроалиментаре СЮД СпА,Италия	2025-10-22 07:34:02.470839+00	2025-10-16 17:31:25.510461+00	2025-10-22 07:34:02.470859+00	222	f	f
122	f	\N	6261	«Агромейд» Единичное общество с ограниченной доверенностью, Болгария	2025-10-22 07:34:02.471961+00	2025-10-16 17:31:25.51138+00	2025-10-22 07:34:02.471982+00	424	f	f
114	f	\N	6018	Заатбау Линце еГен, Австрия	2025-10-22 07:34:02.533734+00	2025-10-16 17:31:25.50768+00	2025-10-22 07:34:02.53376+00	347	f	f
129	f	\N	6223	Институт селекции и растениеводства, Хорватия	2025-10-22 07:34:02.548213+00	2025-10-16 17:31:25.515308+00	2025-10-22 07:34:02.548232+00	298	f	f
97	f	\N	6016	Компания «Семенс Прогрейн Инк», Канада	2025-10-22 07:34:02.571357+00	2025-10-16 17:31:25.497624+00	2025-10-22 07:34:02.571377+00	328	f	f
139	f	\N	6185	Селекционно-генетический институт, город Одесса	2025-10-22 07:34:02.662429+00	2025-10-16 17:31:25.51965+00	2025-10-22 07:34:02.662452+00	169	f	f
78	f	\N	6692	Фирма «NUNHEMS NETHERLANDS», Нидерланды	2025-10-22 07:34:02.767918+00	2025-10-16 17:31:25.487491+00	2025-10-22 07:34:02.767937+00	264	f	f
96	f	\N	7780	Фирма «Selgen» Чехия	2025-10-22 07:34:02.768536+00	2025-10-16 17:31:25.49702+00	2025-10-22 07:34:02.768566+00	248	f	f
83	f	\N	7153	Фирма «Пионер», Соединенные Штаты Америки	2025-10-22 07:34:02.779564+00	2025-10-16 17:31:25.490421+00	2025-10-22 07:34:02.779588+00	234	f	f
106	f	\N	5969	Фирма «Синдгента Сидс Б.В.», Нидерланды	2025-10-22 07:34:02.786958+00	2025-10-16 17:31:25.502441+00	2025-10-22 07:34:02.786985+00	245	f	f
151	f	\N	5964	АСК Техник ( Норика Германия) 	2025-10-16 17:31:25.525649+00	2025-10-16 17:31:25.525864+00	2025-10-16 17:31:25.525867+00	\N	f	f
159	f	\N	6469	Бем Нордкартофель агропродуктион ОХГ Европлант Пфланцихт Гмбх	2025-10-16 17:31:25.529387+00	2025-10-16 17:31:25.529685+00	2025-10-16 17:31:25.529688+00	\N	f	f
162	f	\N	7356	БО Гертссон	2025-10-16 17:31:25.531367+00	2025-10-16 17:31:25.531617+00	2025-10-16 17:31:25.53162+00	\N	f	f
166	f	\N	7756	ВАШИНГТОН СТЕЙТ ЮНИВЕРСИТИ (US)	2025-10-16 17:31:25.533262+00	2025-10-16 17:31:25.533495+00	2025-10-16 17:31:25.533497+00	\N	f	f
168	f	\N	6751	Виерзум Плантбридинг БВ 	2025-10-16 17:31:25.534171+00	2025-10-16 17:31:25.534384+00	2025-10-16 17:31:25.534386+00	\N	f	f
1075	f	\N	7590	ENTAV-INRA, Франция	2025-10-22 07:34:02.437958+00	2025-10-22 07:34:02.438352+00	2025-10-22 07:34:02.438355+00	296	f	f
1076	f	\N	6043	Euralis semences, Франция	2025-10-22 07:34:02.438841+00	2025-10-22 07:34:02.439145+00	2025-10-22 07:34:02.439148+00	345	f	f
1077	f	\N	7826	Florimond Desprez Veuve et Fils SAS, ФРАНЦИЯ	2025-10-22 07:34:02.439905+00	2025-10-22 07:34:02.440167+00	2025-10-22 07:34:02.440169+00	\N	f	f
51	f	\N	7696	Istanbul Tarim Sanayi Ve Ticaret Anonim Sirket, Турция	2025-10-22 07:34:02.446814+00	2025-10-16 17:31:25.474468+00	2025-10-22 07:34:02.44684+00	433	f	f
1078	f	\N	8308	Meiosis LTD, Великобритания475.	2025-10-22 07:34:02.450937+00	2025-10-22 07:34:02.451277+00	2025-10-22 07:34:02.451279+00	474	f	f
1079	f	\N	8283	Monsanto Holand Besloten Vennootschap, Нидерланды322.	2025-10-22 07:34:02.45183+00	2025-10-22 07:34:02.452133+00	2025-10-22 07:34:02.452136+00	321	f	f
1080	f	\N	7842	Panam France SAS, Франция	2025-10-22 07:34:02.455084+00	2025-10-22 07:34:02.455347+00	2025-10-22 07:34:02.455349+00	456	f	f
1081	f	\N	8274	Plant select hrv beice s.r.b., Чехия275.	2025-10-22 07:34:02.455886+00	2025-10-22 07:34:02.45614+00	2025-10-22 07:34:02.456142+00	274	f	f
58	f	\N	7785	Progress Agrar Handelsgesellschaft mbH, Германия	2025-10-22 07:34:02.457455+00	2025-10-16 17:31:25.477937+00	2025-10-22 07:34:02.457475+00	407	f	f
185	f	\N	7760	Герасимова Елена Григорьевна	2025-10-16 17:31:25.542566+00	2025-10-16 17:31:25.542815+00	2025-10-16 17:31:25.542817+00	\N	f	f
187	f	\N	7607	Германия Лимбкенг	2025-10-16 17:31:25.543489+00	2025-10-16 17:31:25.543726+00	2025-10-16 17:31:25.543728+00	\N	f	f
188	f	\N	7395	Германия фирма Лемберкент	2025-10-16 17:31:25.543964+00	2025-10-16 17:31:25.544203+00	2025-10-16 17:31:25.544205+00	\N	f	f
189	f	\N	6702	ГККП "Капланбексикй высший аграрно-технический колледж" 	2025-10-16 17:31:25.544449+00	2025-10-16 17:31:25.54469+00	2025-10-16 17:31:25.544693+00	\N	f	f
1082	f	\N	8303	SECOBRA Recherches SAS, Франция448.	2025-10-22 07:34:02.462106+00	2025-10-22 07:34:02.4624+00	2025-10-22 07:34:02.462404+00	447	f	f
1083	f	\N	7248	ZEAINVENT TRNAVA s.r.o., Словакия	2025-10-22 07:34:02.468667+00	2025-10-22 07:34:02.468918+00	2025-10-22 07:34:02.46892+00	373	f	f
154	f	\N	6061	Атырауский научно исследовательский институт сельского хозяйства	2025-10-22 07:34:02.483828+00	2025-10-16 17:31:25.527282+00	2025-10-22 07:34:02.483852+00	269	f	f
179	f	\N	6603	Всероссийский научно-исследовательский институт картофельного хозяйства	2025-10-22 07:34:02.500457+00	2025-10-16 17:31:25.539981+00	2025-10-22 07:34:02.500476+00	60	f	f
1084	f	\N	8278	А.В. Емельянов296.	2025-10-22 07:34:02.469483+00	2025-10-22 07:34:02.469791+00	2025-10-22 07:34:02.469793+00	295	f	f
1085	f	\N	7794	"Агроконтакт-Георгиеви" ЕООД, Болгария	2025-10-22 07:34:02.471155+00	2025-10-22 07:34:02.471413+00	2025-10-22 07:34:02.471415+00	424	f	f
1086	f	\N	8123	Адыгейский научно исследовательский институт сельского хозяйства47.	2025-10-22 07:34:02.47326+00	2025-10-22 07:34:02.473525+00	2025-10-22 07:34:02.473527+00	46	f	f
191	f	\N	7405	Главный ботанический сад Академии наук Республики Казахстан	2025-10-22 07:34:02.513036+00	2025-10-16 17:31:25.545826+00	2025-10-22 07:34:02.513058+00	9	f	f
184	f	\N	7599	Научная станция Тохоку, Мариока, Япония	2025-10-22 07:34:02.595893+00	2025-10-16 17:31:25.542341+00	2025-10-22 07:34:02.595912+00	313	f	f
170	f	\N	6271	Федеральное государственное бюджетное научное учреждение «Федеральный научный центр «Всероссийский научно-исследовательский институт масличных культур имени В.С. Пустовойта»	2025-10-22 07:34:02.757413+00	2025-10-16 17:31:25.535238+00	2025-10-22 07:34:02.757436+00	64	f	f
186	f	\N	6168	Фирма «Европлант», Германия	2025-10-22 07:34:02.774296+00	2025-10-16 17:31:25.543266+00	2025-10-22 07:34:02.774316+00	300	f	f
198	f	\N	7240	ГНУ АНИИ СХ СО Россельхозакадемии	2025-10-16 17:31:25.549258+00	2025-10-16 17:31:25.549503+00	2025-10-16 17:31:25.549505+00	\N	f	f
228	f	\N	7136	De Ruiter Seeds, Нидерланды	2025-10-22 07:34:02.435037+00	2025-10-16 17:31:25.566019+00	2025-10-22 07:34:02.435064+00	309	f	f
248	f	\N	5817	G.I.E. GRASS Ла Литиер, Франция	2025-10-22 07:34:02.441597+00	2025-10-16 17:31:25.575846+00	2025-10-22 07:34:02.441619+00	392	f	f
1087	f	\N	8104	Актюбинская опытная станция кормов и пастбищ	2025-10-22 07:34:02.473817+00	2025-10-22 07:34:02.474061+00	2025-10-22 07:34:02.474063+00	3	f	f
1088	f	\N	8105	Алматинский государственный сортоиспытательный участок закрытого грунта	2025-10-22 07:34:02.476466+00	2025-10-22 07:34:02.476767+00	2025-10-22 07:34:02.476769+00	5	f	f
218	f	\N	6454	Даниско Сид Хайбигардвег	2025-10-16 17:31:25.559935+00	2025-10-16 17:31:25.56017+00	2025-10-16 17:31:25.560173+00	\N	f	f
1089	f	\N	8223	Андижанская племенная шелководческая станция186.	2025-10-22 07:34:02.480169+00	2025-10-22 07:34:02.48045+00	2025-10-22 07:34:02.480452+00	185	f	f
1090	f	\N	8224	Андижанский филиал Всесоюзного научно-исследовательского института хлопководства187.	2025-10-22 07:34:02.4808+00	2025-10-22 07:34:02.481086+00	2025-10-22 07:34:02.481088+00	186	f	f
1091	f	\N	6548	АО"КазНИИ КОХ" АО" КазАгроИнновация"	2025-10-22 07:34:02.481464+00	2025-10-22 07:34:02.481735+00	2025-10-22 07:34:02.481737+00	\N	f	f
1092	f	\N	8124	Армавирская опытная станция Всероссийского научно-исследовательского института масличных культур49.	2025-10-22 07:34:02.482076+00	2025-10-22 07:34:02.482364+00	2025-10-22 07:34:02.482366+00	48	f	f
1093	f	\N	8242	Армянский научно-исследовательский институт виноградарства, виноделия и садоводства205.	2025-10-22 07:34:02.48285+00	2025-10-22 07:34:02.483103+00	2025-10-22 07:34:02.483105+00	204	f	f
236	f	\N	6907	Др.Петер Франк- Германия	2025-10-16 17:31:25.569453+00	2025-10-16 17:31:25.569691+00	2025-10-16 17:31:25.569693+00	\N	f	f
1094	f	\N	8125	Бакчарский опорный пункт Научно-исследовательского института садоводства Сибири имени М.А. Лисавенко50.	2025-10-22 07:34:02.484594+00	2025-10-22 07:34:02.484854+00	2025-10-22 07:34:02.484856+00	49	f	f
217	f	\N	5906	Дайге Загреределюнг А.Г (Германия)	2025-10-22 07:34:02.520332+00	2025-10-16 17:31:25.559702+00	2025-10-22 07:34:02.520353+00	\N	f	f
227	f	\N	7085	Днепропетровский аграрный университет	2025-10-22 07:34:02.522405+00	2025-10-16 17:31:25.565509+00	2025-10-22 07:34:02.522424+00	153	f	f
243	f	\N	6378	Емельенов Андрей Вячеславович	2025-10-16 17:31:25.573229+00	2025-10-16 17:31:25.573461+00	2025-10-16 17:31:25.573464+00	\N	f	f
230	f	\N	6484	Добруджанский институт земледелия, Болгария	2025-10-22 07:34:02.522897+00	2025-10-16 17:31:25.566939+00	2025-10-22 07:34:02.522917+00	469	f	f
232	f	\N	7450	Донецкая государственная областная сельскохозяйственная опытная станция	2025-10-22 07:34:02.523379+00	2025-10-16 17:31:25.567781+00	2025-10-22 07:34:02.523398+00	154	f	f
233	f	\N	7234	Др. Ласло Селений, Германия	2025-10-22 07:34:02.527928+00	2025-10-16 17:31:25.568272+00	2025-10-22 07:34:02.527948+00	323	f	f
238	f	\N	6498	КОССАД СЕМЕНСЕС, Франция	2025-10-22 07:34:02.573068+00	2025-10-16 17:31:25.570535+00	2025-10-22 07:34:02.573087+00	331	f	f
250	f	\N	7759	Жаухаров Бейбит Жаксылыкович	2025-10-16 17:31:25.576488+00	2025-10-16 17:31:25.576718+00	2025-10-16 17:31:25.576721+00	\N	f	f
202	f	\N	5998	Краснокутская селекционно-опытная станция Научно-исследовательского института сельского хозяйства Юго-Востока	2025-10-22 07:34:02.575431+00	2025-10-16 17:31:25.551568+00	2025-10-22 07:34:02.575458+00	97	f	f
203	f	\N	7293	Красноярский научно-исследовательский институт сельского хозяйства	2025-10-22 07:34:02.576529+00	2025-10-16 17:31:25.552036+00	2025-10-22 07:34:02.576568+00	99	f	f
222	f	\N	6172	Научно-исследовательский институт хлопководства Юго-Западного научно-производственного центра сельского хозяйства	2025-10-22 07:34:02.601921+00	2025-10-16 17:31:25.561931+00	2025-10-22 07:34:02.601948+00	10	f	f
205	f	\N	6191	Сибирский научно исследовательский институт сельского хозяйства	2025-10-22 07:34:02.666813+00	2025-10-16 17:31:25.552932+00	2025-10-22 07:34:02.666832+00	138	f	f
208	f	\N	6572	Ставропольский научно-исследовательский институт сельского хозяйства	2025-10-22 07:34:02.671739+00	2025-10-16 17:31:25.555516+00	2025-10-22 07:34:02.671758+00	139	f	f
244	f	\N	7309	Фирма «Енза Заден», Нидерланды	2025-10-22 07:34:02.774787+00	2025-10-16 17:31:25.573911+00	2025-10-22 07:34:02.774806+00	227	f	f
209	f	\N	6356	Фирма «Марибо», Дания	2025-10-22 07:34:02.777551+00	2025-10-16 17:31:25.556024+00	2025-10-22 07:34:02.777575+00	231	f	f
213	f	\N	7256	Фирма «Синджента Сидс Б.В.», Франция	2025-10-22 07:34:02.787535+00	2025-10-16 17:31:25.557876+00	2025-10-22 07:34:02.787557+00	262	f	f
258	f	\N	5738	Занерпопкорн хибрид США	2025-10-16 17:31:25.580686+00	2025-10-16 17:31:25.580958+00	2025-10-16 17:31:25.58096+00	\N	f	f
265	f	\N	7754	ЗАУК БВБА (BE)	2025-10-16 17:31:25.583976+00	2025-10-16 17:31:25.584188+00	2025-10-16 17:31:25.58419+00	\N	f	f
268	f	\N	6000	ИЗИ Сементи	2025-10-16 17:31:25.585231+00	2025-10-16 17:31:25.585442+00	2025-10-16 17:31:25.585444+00	\N	f	f
269	f	\N	6314	Израиль  компания "Зераши Гедера"	2025-10-16 17:31:25.585644+00	2025-10-16 17:31:25.585862+00	2025-10-16 17:31:25.585865+00	\N	f	f
270	f	\N	7730	Ингеборг ВЭСТЕРИДЖК	2025-10-16 17:31:25.586076+00	2025-10-16 17:31:25.586284+00	2025-10-16 17:31:25.586287+00	\N	f	f
271	f	\N	7418	Индуцированный сорт (Америка)	2025-10-16 17:31:25.586503+00	2025-10-16 17:31:25.586764+00	2025-10-16 17:31:25.586766+00	\N	f	f
272	f	\N	5737	Иновационно-Государствен. фонд Южно-Каз. области	2025-10-16 17:31:25.586993+00	2025-10-16 17:31:25.587205+00	2025-10-16 17:31:25.587207+00	\N	f	f
281	f	\N	7748	Институт растениеводческих ресурсов Хэйлунцзянской академии сельскохозяйтсвенных наук	2025-10-16 17:31:25.59162+00	2025-10-16 17:31:25.591851+00	2025-10-16 17:31:25.591854+00	\N	f	f
1095	f	\N	8106	Балхашское опытное поле Министерства сельского хозяйства Республики Казахстан	2025-10-22 07:34:02.485133+00	2025-10-22 07:34:02.48541+00	2025-10-22 07:34:02.485412+00	7	f	f
1096	f	\N	8127	Башкирский научно-исследовательский институт земледелия и селекции полевых культур53.	2025-10-22 07:34:02.485701+00	2025-10-22 07:34:02.485982+00	2025-10-22 07:34:02.485985+00	52	f	f
1097	f	\N	7492	Башкирский научно-исследовательский институт сельского хозяйства	2025-10-22 07:34:02.486289+00	2025-10-22 07:34:02.486542+00	2025-10-22 07:34:02.486544+00	51	f	f
1098	f	\N	8126	Башкирский научно-исследовательский и проектно-технологический институт животноводства и кормопроизводства51.	2025-10-22 07:34:02.486804+00	2025-10-22 07:34:02.487047+00	2025-10-22 07:34:02.487049+00	50	f	f
1099	f	\N	8128	Белгородская опытная станция Всероссийского научно-исследовательского института масличных культур54.	2025-10-22 07:34:02.487304+00	2025-10-22 07:34:02.487599+00	2025-10-22 07:34:02.487601+00	53	f	f
294	f	\N	6354	Иоган Дикман	2025-10-16 17:31:25.598114+00	2025-10-16 17:31:25.598373+00	2025-10-16 17:31:25.598376+00	\N	f	f
276	f	\N	7850	Государственное учреждение «Институт зерновых культур Национальной академии аграрных наук Украины», Украина	2025-10-22 07:34:02.518569+00	2025-10-16 17:31:25.589596+00	2025-10-22 07:34:02.518588+00	408	f	f
297	f	\N	7841	ИП Глава КФХ Завражнов Антон Владимирович	2025-10-16 17:31:25.599492+00	2025-10-16 17:31:25.599714+00	2025-10-16 17:31:25.599716+00	\N	f	f
280	f	\N	7213	Институт Растениеводства «Порумбень», Молдова	2025-10-22 07:34:02.546807+00	2025-10-16 17:31:25.591423+00	2025-10-22 07:34:02.546834+00	353	f	f
273	f	\N	7770	Ялтушковская опытно-селекционная станция Института биоэнергетических культур и сахарной свеклы Национальной академии аграрных наук Украины	2025-10-22 07:34:02.804176+00	2025-10-16 17:31:25.587767+00	2025-10-22 07:34:02.804196+00	182	f	f
292	f	\N	5779	Товарищество с ограниченной ответственностью «Казахский научно-исследовательский институт земледелия и растениеводства»	2025-10-22 07:34:02.682318+00	2025-10-16 17:31:25.596956+00	2025-10-22 07:34:02.682339+00	18	f	f
282	f	\N	7713	Институт физиологии растений и генетики Национальной академии наук Украины, Украина	2025-10-22 07:34:02.548794+00	2025-10-16 17:31:25.59226+00	2025-10-22 07:34:02.54882+00	448	f	f
289	f	\N	6718	Институт фитохимии Министерства образования и науки Республики Казахстан	2025-10-22 07:34:02.549476+00	2025-10-16 17:31:25.595231+00	2025-10-22 07:34:02.549496+00	268	f	f
295	f	\N	5793	Общество с ограниченной ответственностью «Научно-исследовательский институт овощеводства защищенного грунта», Россия	2025-10-22 07:34:02.621438+00	2025-10-16 17:31:25.598854+00	2025-10-22 07:34:02.621465+00	380	f	f
266	f	\N	6973	Фирма «ЗПС», Нидерланды	2025-10-22 07:34:02.776407+00	2025-10-16 17:31:25.584614+00	2025-10-22 07:34:02.776426+00	229	f	f
264	f	\N	7149	Юго-Западный научно-производственный центр сельского хозяйства Министерства сельского хозяйства Республики Казахстан	2025-10-22 07:34:02.80221+00	2025-10-16 17:31:25.583763+00	2025-10-22 07:34:02.802229+00	20	f	f
311	f	\N	7051	Nuseed Evropa limited trade development, Англия	2025-10-22 07:34:02.454772+00	2025-10-16 17:31:25.607877+00	2025-10-22 07:34:02.454794+00	367	f	f
1100	f	\N	8221	Белорусский научно исследовательский институт земледелия184.	2025-10-22 07:34:02.487877+00	2025-10-22 07:34:02.488203+00	2025-10-22 07:34:02.488205+00	183	f	f
1101	f	\N	8222	Белорусский научно-исследовательский институт картофелеводства и плодоовощеводства185.	2025-10-22 07:34:02.488524+00	2025-10-22 07:34:02.488839+00	2025-10-22 07:34:02.488841+00	184	f	f
1102	f	\N	8129	Бирючекутская овощная селекционно-опытная станция55.	2025-10-22 07:34:02.489389+00	2025-10-22 07:34:02.489632+00	2025-10-22 07:34:02.489634+00	54	f	f
306	f	\N	6238	ИП Хамзатханов ООО "Агростандарт" г. Краснодар Россия 	2025-10-16 17:31:25.603709+00	2025-10-16 17:31:25.603951+00	2025-10-16 17:31:25.603954+00	\N	f	f
307	f	\N	6211	Исакулов Е.Б. - 	2025-10-16 17:31:25.604567+00	2025-10-16 17:31:25.605014+00	2025-10-16 17:31:25.605017+00	\N	f	f
1103	f	\N	8238	Ботанический сад Академии наук Киргизии201.	2025-10-22 07:34:02.490171+00	2025-10-22 07:34:02.490412+00	2025-10-22 07:34:02.490414+00	200	f	f
1104	f	\N	8245	Ботанический сад Академии наук Республики Молдова208.	2025-10-22 07:34:02.490698+00	2025-10-22 07:34:02.490938+00	2025-10-22 07:34:02.49094+00	207	f	f
1105	f	\N	8130	Ботанический сад Нижегородского государственного университета56.	2025-10-22 07:34:02.491233+00	2025-10-22 07:34:02.491486+00	2025-10-22 07:34:02.491488+00	55	f	f
1106	f	\N	8271	Буйнакская опытная станция садоводства, Дагестан261.	2025-10-22 07:34:02.491793+00	2025-10-22 07:34:02.492042+00	2025-10-22 07:34:02.492045+00	260	f	f
1107	f	\N	8131	Бурятский научно исследовательский институт сельского хозяйства57.	2025-10-22 07:34:02.492346+00	2025-10-22 07:34:02.492611+00	2025-10-22 07:34:02.492613+00	56	f	f
1108	f	\N	8132	Быковская бахчевая селекционная опытная станция58.	2025-10-22 07:34:02.492889+00	2025-10-22 07:34:02.493172+00	2025-10-22 07:34:02.493174+00	57	f	f
1109	f	\N	8248	Вахшский филиал Таджикской научно-производственное объединение «Земледелие»214.	2025-10-22 07:34:02.493495+00	2025-10-22 07:34:02.493758+00	2025-10-22 07:34:02.49376+00	213	f	f
1110	f	\N	8193	Веселоподолянская опытно-селекционная станция151.	2025-10-22 07:34:02.494918+00	2025-10-22 07:34:02.495219+00	2025-10-22 07:34:02.495221+00	150	f	f
1111	f	\N	8146	Волгоградская государственная сельскохозяйственная академия77.	2025-10-22 07:34:02.495819+00	2025-10-22 07:34:02.496061+00	2025-10-22 07:34:02.496063+00	76	f	f
1112	f	\N	8145	Волгоградская опытная станция Всероссийского научно исследовательского института растениеводства76.	2025-10-22 07:34:02.496378+00	2025-10-22 07:34:02.496619+00	2025-10-22 07:34:02.496622+00	75	f	f
1113	f	\N	8147	Воронежская овощная опытная станция78.	2025-10-22 07:34:02.496886+00	2025-10-22 07:34:02.497145+00	2025-10-22 07:34:02.497148+00	77	f	f
1004	f	\N	7964	Восточно-Казахстанский государственный университет имени Сарсена Аманжолова	2025-10-22 07:34:02.497678+00	2025-10-21 21:50:08.598781+00	2025-10-22 07:34:02.497701+00	393	f	f
1114	f	\N	8133	Всероссийский научно-исследовательский институт генетики и селекции плодовых растений имени И.В. Мичурина59.	2025-10-22 07:34:02.499022+00	2025-10-22 07:34:02.499385+00	2025-10-22 07:34:02.499388+00	58	f	f
1115	f	\N	8006	Всероссийский научно-исследовательский институт кукурузы, город Ставрополь	2025-10-22 07:34:02.500754+00	2025-10-22 07:34:02.501001+00	2025-10-22 07:34:02.501004+00	61	f	f
1116	f	\N	8134	Всероссийский научно-исследовательский институт лекарственных и ароматических растений63.	2025-10-22 07:34:02.501317+00	2025-10-22 07:34:02.501583+00	2025-10-22 07:34:02.501585+00	62	f	f
1117	f	\N	8135	Всероссийский научно-исследовательский институт мясного скотоводства64.	2025-10-22 07:34:02.501879+00	2025-10-22 07:34:02.502166+00	2025-10-22 07:34:02.502168+00	63	f	f
1118	f	\N	8136	Всероссийский научно-исследовательский институт овощеводства66.	2025-10-22 07:34:02.50249+00	2025-10-22 07:34:02.502896+00	2025-10-22 07:34:02.502936+00	65	f	f
1119	f	\N	8056	Всероссийский научно-исследовательский институт орошаемого овощеводства и бахчеводства	2025-10-22 07:34:02.503388+00	2025-10-22 07:34:02.503734+00	2025-10-22 07:34:02.503736+00	66	f	f
1120	f	\N	8137	Всероссийский научно-исследовательский институт растениеводства имени Н.И. Вавилова68.	2025-10-22 07:34:02.504097+00	2025-10-22 07:34:02.504409+00	2025-10-22 07:34:02.504411+00	67	f	f
1121	f	\N	8138	Всероссийский научно исследовательский институт риса69.	2025-10-22 07:34:02.504821+00	2025-10-22 07:34:02.505655+00	2025-10-22 07:34:02.505658+00	68	f	f
1122	f	\N	8139	Всероссийский научно-исследовательский институт садоводства имени И.В. Мичурина70.	2025-10-22 07:34:02.506043+00	2025-10-22 07:34:02.506698+00	2025-10-22 07:34:02.506701+00	69	f	f
1123	f	\N	8140	Всероссийский научно-исследовательский институт сахарной свеклы и сахара имени А.Л. Мазлумова71.	2025-10-22 07:34:02.507072+00	2025-10-22 07:34:02.507355+00	2025-10-22 07:34:02.507357+00	70	f	f
1124	f	\N	8141	Всероссийский научно-исследовательский институт селекции и семеноводства овощных культур72.	2025-10-22 07:34:02.507647+00	2025-10-22 07:34:02.50789+00	2025-10-22 07:34:02.507892+00	71	f	f
330	f	\N	5953	ИКАРДА	2025-10-22 07:34:02.541288+00	2025-10-16 17:31:25.617999+00	2025-10-22 07:34:02.541307+00	271	f	f
329	f	\N	6521	Украинский научно исследовательский институт орошаемого земледелия	2025-10-22 07:34:02.712501+00	2025-10-16 17:31:25.617553+00	2025-10-22 07:34:02.712522+00	176	f	f
1330	f	\N	8190	Хакасская сельскохозяйственная опытная станция147.	2025-10-22 07:34:02.791395+00	2025-10-22 07:34:02.791656+00	2025-10-22 07:34:02.791658+00	146	f	f
1331	f	\N	8217	Херсонская селекционно-опытная станция бахчеводства179.	2025-10-22 07:34:02.792185+00	2025-10-22 07:34:02.792429+00	2025-10-22 07:34:02.792431+00	178	f	f
1332	f	\N	8120	Целиноградская государственная сельскохозяйственная опытная станция43.	2025-10-22 07:34:02.793674+00	2025-10-22 07:34:02.793929+00	2025-10-22 07:34:02.793931+00	42	f	f
1125	f	\N	8143	Всероссийский научно-исследовательский институт селекции и семеноводства сорговых культур74.	2025-10-22 07:34:02.508355+00	2025-10-22 07:34:02.508623+00	2025-10-22 07:34:02.508626+00	73	f	f
1126	f	\N	8142	Всероссийский научно-исследовательский институт селекции плодовых культур, город Орел73.	2025-10-22 07:34:02.508913+00	2025-10-22 07:34:02.509179+00	2025-10-22 07:34:02.509181+00	72	f	f
1127	f	\N	8144	Всероссийский научно исследовательский институт сои75.	2025-10-22 07:34:02.509446+00	2025-10-22 07:34:02.509717+00	2025-10-22 07:34:02.509719+00	74	f	f
1128	f	\N	7196	Всероссийский селекционно-технологический институт садоводства и питомниководства	2025-10-22 07:34:02.509999+00	2025-10-22 07:34:02.510294+00	2025-10-22 07:34:02.510297+00	78	f	f
1129	f	\N	6967	ГКП Махтааральская с-х опытная станция	2025-10-22 07:34:02.512116+00	2025-10-22 07:34:02.512432+00	2025-10-22 07:34:02.512435+00	\N	f	f
1130	f	\N	8148	Главный ботанический сад имени Н.В. Цицина Российской академии наук80.	2025-10-22 07:34:02.513374+00	2025-10-22 07:34:02.513679+00	2025-10-22 07:34:02.513696+00	79	f	f
1131	f	\N	8194	Гороховский совхоз-техникум, Украина152.	2025-10-22 07:34:02.51417+00	2025-10-22 07:34:02.514429+00	2025-10-22 07:34:02.514431+00	151	f	f
1132	f	\N	8107	Государственное казенное предприятие опытно-производственное хозяйство «Зыряновское»12.	2025-10-22 07:34:02.51472+00	2025-10-22 07:34:02.514981+00	2025-10-22 07:34:02.514983+00	11	f	f
1133	f	\N	8108	Государственное казенное предприятие опытно-производственное хозяйство «Масличные культуры»13.	2025-10-22 07:34:02.515264+00	2025-10-22 07:34:02.515515+00	2025-10-22 07:34:02.515517+00	12	f	f
1134	f	\N	8277	Государственное научное учреждение «Алтайский научно исследовательский институт сельского хозяйства», Россия289.	2025-10-22 07:34:02.515792+00	2025-10-22 07:34:02.516046+00	2025-10-22 07:34:02.516048+00	288	f	f
367	f	\N	7188	Казахстан Нидера СА 	2025-10-16 17:31:25.635844+00	2025-10-16 17:31:25.636086+00	2025-10-16 17:31:25.636089+00	\N	f	f
368	f	\N	7466	Казахстан Сипиел Рисеч Нон-Профит НИИ СХ Франция 	2025-10-16 17:31:25.636327+00	2025-10-16 17:31:25.636594+00	2025-10-16 17:31:25.636597+00	\N	f	f
1135	f	\N	8282	Государственное научное учреждение «Всероссийский научно-исследовательский и проектно-технологический институт рапса», Россия319.	2025-10-22 07:34:02.51679+00	2025-10-22 07:34:02.517033+00	2025-10-22 07:34:02.517035+00	318	f	f
371	f	\N	6518	Қаз егістік ҒЗИ	2025-10-16 17:31:25.638348+00	2025-10-16 17:31:25.638702+00	2025-10-16 17:31:25.638705+00	\N	f	f
1136	f	\N	7890	Государственное научное учреждение «Сибирская опытная станция Всероссийского научно-исследовательского института имени В.С. Пустовойта»	2025-10-22 07:34:02.51783+00	2025-10-22 07:34:02.518084+00	2025-10-22 07:34:02.518086+00	272	f	f
1137	f	\N	8195	Государственный Никитский Ботанический сад, Украина153.	2025-10-22 07:34:02.519468+00	2025-10-22 07:34:02.519748+00	2025-10-22 07:34:02.519751+00	152	f	f
1138	f	\N	8149	Дальневосточная опытная станция Всероссийского научно исследовательского института растениеводства81.	2025-10-22 07:34:02.520663+00	2025-10-22 07:34:02.520957+00	2025-10-22 07:34:02.520959+00	80	f	f
379	f	\N	6731	Канадская фирма	2025-10-16 17:31:25.642481+00	2025-10-16 17:31:25.642708+00	2025-10-16 17:31:25.642711+00	\N	f	f
1139	f	\N	8196	Донецкая овощебахчевая опытная станция156.	2025-10-22 07:34:02.523645+00	2025-10-22 07:34:02.523884+00	2025-10-22 07:34:02.523887+00	155	f	f
345	f	\N	5707	Институт кукурузы «Земун Поле», Сербия и Черногория	2025-10-22 07:34:02.545609+00	2025-10-16 17:31:25.625719+00	2025-10-22 07:34:02.545629+00	220	f	f
376	f	\N	6207	Научно-исследовательский институт лесного хозяйства и агролесомелиорации	2025-10-22 07:34:02.598105+00	2025-10-16 17:31:25.641163+00	2025-10-22 07:34:02.598132+00	265	f	f
381	f	\N	6340	Пензенский научно исследовательский институт сельского хозяйства	2025-10-22 07:34:02.640622+00	2025-10-16 17:31:25.643627+00	2025-10-22 07:34:02.640641+00	124	f	f
395	f	\N	7420	К.И.В. – КОНСОРЦИО ИТАЛЬЯНО ВИВАИСТИ – Сочиета Консортиле а р.л.	2025-10-16 17:31:25.650839+00	2025-10-16 17:31:25.65106+00	2025-10-16 17:31:25.651062+00	\N	f	f
409	f	\N	7080	Компания Остеррас 	2025-10-16 17:31:25.658597+00	2025-10-16 17:31:25.658836+00	2025-10-16 17:31:25.658839+00	\N	f	f
422	f	\N	6579	Крестьянское хоз. "Саялы"	2025-10-16 17:31:25.6656+00	2025-10-16 17:31:25.665864+00	2025-10-16 17:31:25.665866+00	\N	f	f
389	f	\N	6031	Gleen Seeds LTD, Канада	2025-10-22 07:34:02.442541+00	2025-10-16 17:31:25.648318+00	2025-10-22 07:34:02.44256+00	482	f	f
432	f	\N	7440	Ландвиртшафтлихе Леранштальтен Трисдорф, Германия 	2025-10-16 17:31:25.670207+00	2025-10-16 17:31:25.67043+00	2025-10-16 17:31:25.670432+00	\N	f	f
431	f	\N	5727	LABOULET Semences, Франция	2025-10-22 07:34:02.448821+00	2025-10-16 17:31:25.669956+00	2025-10-22 07:34:02.448841+00	374	f	f
435	f	\N	5879	Макенов Т.Е. КВС ЗААТ СЕ	2025-10-16 17:31:25.672029+00	2025-10-16 17:31:25.672353+00	2025-10-16 17:31:25.672355+00	\N	f	f
439	f	\N	6068	May-Agro Tohumculuk Sanayi ve Ticaret A.Ş., Турция	2025-10-22 07:34:02.450586+00	2025-10-16 17:31:25.674786+00	2025-10-22 07:34:02.450613+00	457	f	f
440	f	\N	6944	Махтааральская опытная станция  НАЦ АИ РК	2025-10-16 17:31:25.675012+00	2025-10-16 17:31:25.67523+00	2025-10-16 17:31:25.675232+00	\N	f	f
393	f	\N	6863	Stet Holland B.V. Нидерланды	2025-10-22 07:34:02.464396+00	2025-10-16 17:31:25.650139+00	2025-10-22 07:34:02.464416+00	486	f	f
1140	f	\N	8150	Донская опытная станция Всероссийского научно-исследовательского института масличных культур82.	2025-10-22 07:34:02.524137+00	2025-10-22 07:34:02.524379+00	2025-10-22 07:34:02.524381+00	81	f	f
391	f	\N	6403	Картофельцухт Бем, Германия	2025-10-22 07:34:02.564524+00	2025-10-16 17:31:25.649259+00	2025-10-22 07:34:02.564545+00	343	f	f
1141	f	\N	8151	Донской селекционный центр Донского зонального научно исследовательского института сельского хозяйства84.	2025-10-22 07:34:02.525138+00	2025-10-22 07:34:02.525404+00	2025-10-22 07:34:02.525406+00	83	f	f
1142	f	\N	8152	Донской сельскохозяйственный институт85.	2025-10-22 07:34:02.525682+00	2025-10-22 07:34:02.52594+00	2025-10-22 07:34:02.525942+00	84	f	f
1143	f	\N	8295	Дорогобед Алексей Алексеевич, Россия400.	2025-10-22 07:34:02.526258+00	2025-10-22 07:34:02.526769+00	2025-10-22 07:34:02.526773+00	399	f	f
1144	f	\N	7099	Дубовская опытная станция	2025-10-22 07:34:02.528486+00	2025-10-22 07:34:02.528769+00	2025-10-22 07:34:02.528771+00	132	f	f
1007	f	\N	7998	Ершовская опытная станция орошаемого земледелия	2025-10-22 07:34:02.530665+00	2025-10-21 21:50:08.604048+00	2025-10-22 07:34:02.530684+00	85	f	f
1145	f	\N	6174	Еуроплант  Пфланзензухт Гмбх	2025-10-22 07:34:02.530969+00	2025-10-22 07:34:02.531238+00	2025-10-22 07:34:02.53124+00	\N	f	f
410	f	\N	6818	Компания «Сесвандерхаве» Бельгия	2025-10-22 07:34:02.57193+00	2025-10-16 17:31:25.659268+00	2025-10-22 07:34:02.57195+00	305	f	f
421	f	\N	6810	Краснодарский научно-исследовательский институт сельского хозяйства имени П.П. Лукьяненко	2025-10-22 07:34:02.574897+00	2025-10-16 17:31:25.665324+00	2025-10-22 07:34:02.574916+00	96	f	f
428	f	\N	7230	Крестьянское хозяйство «Багратион», Казахстан	2025-10-22 07:34:02.577349+00	2025-10-16 17:31:25.668606+00	2025-10-22 07:34:02.577369+00	468	f	f
425	f	\N	7367	Курт Хортсхолм Сейет, Дания	2025-10-22 07:34:02.583096+00	2025-10-16 17:31:25.667279+00	2025-10-22 07:34:02.583115+00	301	f	f
438	f	\N	6344	Мария Ан Смит, Австралия	2025-10-22 07:34:02.589268+00	2025-10-16 17:31:25.674238+00	2025-10-22 07:34:02.589292+00	312	f	f
408	f	\N	6456	Научно-производственное фермерское хозяйство «Компания МАИС», Украина	2025-10-22 07:34:02.604691+00	2025-10-16 17:31:25.658221+00	2025-10-22 07:34:02.604713+00	423	f	f
1260	f	\N	8229	Среднеазиатская опытная станция Всероссийского научно исследовательской института растениеводства192.	2025-10-22 07:34:02.670165+00	2025-10-22 07:34:02.670491+00	2025-10-22 07:34:02.670493+00	191	f	f
1261	f	\N	8230	Среднеазиатский научно-исследовательский и технологический институт шелководства193.	2025-10-22 07:34:02.670832+00	2025-10-22 07:34:02.67117+00	2025-10-22 07:34:02.671172+00	192	f	f
406	f	\N	7278	Фирма «Хруккэм», Соединенные Штаты Америки	2025-10-22 07:34:02.789665+00	2025-10-16 17:31:25.657254+00	2025-10-22 07:34:02.789684+00	285	f	f
444	f	\N	6546	Мишель Марде. Франция	2025-10-16 17:31:25.676834+00	2025-10-16 17:31:25.677062+00	2025-10-16 17:31:25.677064+00	\N	f	f
457	f	\N	6120	НАО научно-исслед тех. Университет им. К.И.Сатпаев Институт хим и био-х технологий 	2025-10-16 17:31:25.683425+00	2025-10-16 17:31:25.683641+00	2025-10-16 17:31:25.683644+00	\N	f	f
446	f	\N	7360	C. Meijer Besloten Vennootschap, Нидерланды	2025-10-22 07:34:02.433007+00	2025-10-16 17:31:25.677942+00	2025-10-22 07:34:02.433026+00	431	f	f
467	f	\N	6606	NIDERA SA (Нидера Са), Аргентина	2025-10-22 07:34:02.45429+00	2025-10-16 17:31:25.688948+00	2025-10-22 07:34:02.454309+00	341	f	f
1146	f	\N	8296	Жамбылский филиал товарищества с ограниченной ответственностью «Казахский научно-исследовательский институт земледелия и растениеводства»403.	2025-10-22 07:34:02.531552+00	2025-10-22 07:34:02.531831+00	2025-10-22 07:34:02.531833+00	402	f	f
1147	f	\N	8109	Жезказганская сельскохозяйственная опытная станция14.	2025-10-22 07:34:02.532361+00	2025-10-22 07:34:02.532622+00	2025-10-22 07:34:02.532624+00	13	f	f
1148	f	\N	8197	Жеребковская опытная станция Научно-исследовательского института кукурузы Украины157.	2025-10-22 07:34:02.532923+00	2025-10-22 07:34:02.53321+00	2025-10-22 07:34:02.533212+00	156	f	f
1149	f	\N	6865	ЗаКа Пфланценцухт ГбР, Германия	2025-10-22 07:34:02.535714+00	2025-10-22 07:34:02.53621+00	2025-10-22 07:34:02.536213+00	334	f	f
489	f	\N	5821	НПЦ ППП	2025-10-16 17:31:25.700147+00	2025-10-16 17:31:25.700391+00	2025-10-16 17:31:25.700394+00	\N	f	f
490	f	\N	5903	Нунемс Б.В.	2025-10-16 17:31:25.700618+00	2025-10-16 17:31:25.70086+00	2025-10-16 17:31:25.700863+00	\N	f	f
453	f	\N	6057	Казахский государственный агротехнический университет имени Сакена Сейфуллина	2025-10-22 07:34:02.556065+00	2025-10-16 17:31:25.681627+00	2025-10-22 07:34:02.556089+00	2	f	f
469	f	\N	6765	Кокинский опорный пункт по садоводству Научно-исследовательского зонального института садоводства Нечерноземной полосы	2025-10-22 07:34:02.568173+00	2025-10-16 17:31:25.690169+00	2025-10-22 07:34:02.568194+00	94	f	f
477	f	\N	7306	Компания «Никерсон Цваан», Нидерланды	2025-10-22 07:34:02.57049+00	2025-10-16 17:31:25.694185+00	2025-10-22 07:34:02.57051+00	294	f	f
471	f	\N	7211	Научно-исследовательский институт кукурузы и сорго Республики Молдова	2025-10-22 07:34:02.59697+00	2025-10-16 17:31:25.691189+00	2025-10-22 07:34:02.596989+00	208	f	f
473	f	\N	7643	Научно-исследовательский институт садоводства Сибири имени М.А. Лисавенко	2025-10-22 07:34:02.599178+00	2025-10-16 17:31:25.692199+00	2025-10-22 07:34:02.599202+00	112	f	f
476	f	\N	5997	Научно исследовательский институт сельского хозяйства Юго-Востока	2025-10-22 07:34:02.601387+00	2025-10-16 17:31:25.693628+00	2025-10-22 07:34:02.601407+00	114	f	f
483	f	\N	6020	Научно-производственное объединение «Соя-Центр», Россия	2025-10-22 07:34:02.603447+00	2025-10-16 17:31:25.697557+00	2025-10-22 07:34:02.603476+00	445	f	f
460	f	\N	7033	Научно-производственное объединение "Шымкент"	2025-10-22 07:34:02.604079+00	2025-10-16 17:31:25.68496+00	2025-10-22 07:34:02.604099+00	406	f	f
487	f	\N	6091	Научно-производственный центр зернового хозяйства имени А.И. Бараева Министерства сельского хозяйства Республики Казахстан	2025-10-22 07:34:02.605581+00	2025-10-16 17:31:25.699456+00	2025-10-22 07:34:02.605619+00	19	f	f
465	f	\N	6935	Некоммерческое акционерное общество «Казахский национальный аграрный университет»	2025-10-22 07:34:02.607486+00	2025-10-16 17:31:25.687439+00	2025-10-22 07:34:02.607505+00	441	f	f
482	f	\N	6139	Нордринг-картофелцухт-унд фермерунг-ГМБХ гросс Люсевитц, Германия	2025-10-22 07:34:02.610795+00	2025-10-16 17:31:25.696925+00	2025-10-22 07:34:02.610854+00	332	f	f
479	f	\N	6438	Частное предприятие «Новомосковский плодопитомник», Украина	2025-10-22 07:34:02.797232+00	2025-10-16 17:31:25.695095+00	2025-10-22 07:34:02.797251+00	472	f	f
475	f	\N	7554	Частное учреждение «Научно-исследовательский институт экологии и экспериментальной биологии Республики Казахстан»	2025-10-22 07:34:02.798281+00	2025-10-16 17:31:25.693127+00	2025-10-22 07:34:02.798301+00	307	f	f
498	f	\N	7040	Омский СХИ Челябинский НИИ СХ	2025-10-16 17:31:25.704907+00	2025-10-16 17:31:25.705264+00	2025-10-16 17:31:25.705267+00	\N	f	f
505	f	\N	7488	ООО "Агролига Центр селекции растений", Россия	2025-10-16 17:31:25.70888+00	2025-10-16 17:31:25.709088+00	2025-10-16 17:31:25.709091+00	\N	f	f
510	f	\N	6257	ООО агрофирма "Украиские семена" 	2025-10-16 17:31:25.710968+00	2025-10-16 17:31:25.711186+00	2025-10-16 17:31:25.711189+00	\N	f	f
511	f	\N	7840	ООО "Акпадон-Агро", Украина	2025-10-16 17:31:25.711393+00	2025-10-16 17:31:25.711609+00	2025-10-16 17:31:25.711612+00	\N	f	f
516	f	\N	7815	ООО "ГРИНОМИКА ТРЕЙД"	2025-10-16 17:31:25.714838+00	2025-10-16 17:31:25.7151+00	2025-10-16 17:31:25.715103+00	\N	f	f
518	f	\N	7837	ООО "Дока-Генные Технологии", Россия	2025-10-16 17:31:25.71587+00	2025-10-16 17:31:25.716095+00	2025-10-16 17:31:25.716098+00	\N	f	f
546	f	\N	5765	Monsanto Vegetable IP Menegement B.V., Нидерланды	2025-10-22 07:34:02.453218+00	2025-10-16 17:31:25.731488+00	2025-10-22 07:34:02.453237+00	439	f	f
528	f	\N	7781	ООО "НПК "Серый хлеб Урала"	2025-10-16 17:31:25.720536+00	2025-10-16 17:31:25.720886+00	2025-10-16 17:31:25.720888+00	\N	f	f
1150	f	\N	8153	Западно-Сибирская овощекартофельная опытная станция88.	2025-10-22 07:34:02.538734+00	2025-10-22 07:34:02.539013+00	2025-10-22 07:34:02.539015+00	87	f	f
1151	f	\N	6533	Зыряновский селекционно-семеноводческий опорный пункт Восточно-Казахстанского научно-исследовательского института сельского хозяйства	2025-10-22 07:34:02.539626+00	2025-10-22 07:34:02.539886+00	2025-10-22 07:34:02.539889+00	256	f	f
1152	f	\N	8198	Ивано-Франковский научно-исследовательский институт крестоцветных культур158.	2025-10-22 07:34:02.54015+00	2025-10-22 07:34:02.540391+00	2025-10-22 07:34:02.540393+00	157	f	f
534	f	\N	5999	ООО " Селекционно-семеноводческая фирма "Манул"	2025-10-16 17:31:25.724425+00	2025-10-16 17:31:25.72483+00	2025-10-16 17:31:25.724834+00	\N	f	f
506	f	\N	7362	Общество с ограниченной ответственностью «Агроплазма», Россия	2025-10-22 07:34:02.61298+00	2025-10-16 17:31:25.709501+00	2025-10-22 07:34:02.613002+00	359	f	f
512	f	\N	6395	Общество с ограниченной ответственностью «Актив Агро», Россия	2025-10-22 07:34:02.615482+00	2025-10-16 17:31:25.712101+00	2025-10-22 07:34:02.615502+00	422	f	f
541	f	\N	7808	ООО "Текджан Тохумджулук"	2025-10-16 17:31:25.727993+00	2025-10-16 17:31:25.728231+00	2025-10-16 17:31:25.728234+00	\N	f	f
513	f	\N	6013	Общество с ограниченной ответственностью «Всерусский научно-исследовательский институт сорго и сои «Славянское поле», Россия	2025-10-22 07:34:02.615986+00	2025-10-16 17:31:25.712764+00	2025-10-22 07:34:02.616009+00	377	f	f
520	f	\N	6175	Общество с ограниченной ответственностью Инновационно производственная агрофирма «Отбор», Россия	2025-10-22 07:34:02.61749+00	2025-10-16 17:31:25.717059+00	2025-10-22 07:34:02.617509+00	388	f	f
522	f	\N	5800	Общество с ограниченной ответственностью Компания «СОКО», Россия	2025-10-22 07:34:02.619634+00	2025-10-16 17:31:25.718008+00	2025-10-22 07:34:02.619665+00	426	f	f
549	f	\N	5766	Отдел селекции семеноводства подсолнечника	2025-10-16 17:31:25.732729+00	2025-10-16 17:31:25.73294+00	2025-10-16 17:31:25.732943+00	\N	f	f
523	f	\N	6582	Общество с ограниченной ответственностью Кукурузокалибровочный завод «Золотой початок», Россия	2025-10-22 07:34:02.620281+00	2025-10-16 17:31:25.718466+00	2025-10-22 07:34:02.620301+00	438	f	f
524	f	\N	6328	Общество с ограниченной ответственностью «Научно-исследовательская компания зерновых культур», Венгрия	2025-10-22 07:34:02.620822+00	2025-10-16 17:31:25.718932+00	2025-10-22 07:34:02.620848+00	411	f	f
545	f	\N	5949	Общество с ограниченной ответственностью «ЭКОНива-Семена», Россия	2025-10-22 07:34:02.630152+00	2025-10-16 17:31:25.730926+00	2025-10-22 07:34:02.630173+00	449	f	f
504	f	\N	7731	Федеральное государственное бюджетное учреждение науки «Самарский федеральный исследовательский центр Российской академии наук», Россия	2025-10-22 07:34:02.759833+00	2025-10-16 17:31:25.708653+00	2025-10-22 07:34:02.759858+00	451	f	f
525	f	\N	7768	Общество с ограниченной ответственностью «Научно-исследовательский институт сои», Украина	2025-10-22 07:34:02.62204+00	2025-10-16 17:31:25.719394+00	2025-10-22 07:34:02.622061+00	327	f	f
530	f	\N	6879	Общество с ограниченной ответственностью «Научно производственное объединение «Семеноводство Кубани», Россия	2025-10-22 07:34:02.623542+00	2025-10-16 17:31:25.721957+00	2025-10-22 07:34:02.62356+00	406	f	f
536	f	\N	7530	Общество с ограниченной ответственностью «Семенная Лига», Россия	2025-10-22 07:34:02.627276+00	2025-10-16 17:31:25.725892+00	2025-10-22 07:34:02.627295+00	463	f	f
543	f	\N	6993	Общество с ограниченной ответственностью «ТСО-Саратов», Россия	2025-10-22 07:34:02.627923+00	2025-10-16 17:31:25.729414+00	2025-10-22 07:34:02.627951+00	371	f	f
544	f	\N	5820	Общество с ограниченной ответственностью «Фабалес», Россия	2025-10-22 07:34:02.628744+00	2025-10-16 17:31:25.73013+00	2025-10-22 07:34:02.628768+00	354	f	f
540	f	\N	7838	Южно-Уральский научно-исследовательский институт плодоводства и картофелеводства	2025-10-22 07:34:02.803582+00	2025-10-16 17:31:25.727735+00	2025-10-22 07:34:02.803605+00	149	f	f
552	f	\N	7523	ОХМК	2025-10-16 17:31:25.734199+00	2025-10-16 17:31:25.73441+00	2025-10-16 17:31:25.734412+00	\N	f	f
559	f	\N	6298	помологический сад	2025-10-16 17:31:25.737737+00	2025-10-16 17:31:25.738117+00	2025-10-16 17:31:25.738121+00	\N	f	f
571	f	\N	7357	Рапуль Казахстан (Саl West Seeds) 	2025-10-16 17:31:25.743931+00	2025-10-16 17:31:25.744162+00	2025-10-16 17:31:25.744165+00	\N	f	f
572	f	\N	7791	РВА Райфайзен Варе Австрия АО	2025-10-16 17:31:25.744377+00	2025-10-16 17:31:25.744596+00	2025-10-16 17:31:25.744598+00	\N	f	f
550	f	\N	6943	Акционерное общество «ЯССЫ», Туркестанская область	2025-10-22 07:34:02.476083+00	2025-10-16 17:31:25.733357+00	2025-10-22 07:34:02.476103+00	279	f	f
582	f	\N	6085	РГКП НИИ каракулеводства	2025-10-16 17:31:25.749875+00	2025-10-16 17:31:25.750095+00	2025-10-16 17:31:25.750097+00	\N	f	f
585	f	\N	6192	Дочернее государственное предприятие «Институт биологии и биотехнологии растений» Национального центра биотехнологии Республики Казахстан Комитета науки Министерства образования и науки Республики Казахстан	2025-10-22 07:34:02.527403+00	2025-10-16 17:31:25.751429+00	2025-10-22 07:34:02.527422+00	16	f	f
1153	f	\N	8110	Илийский комплексный сортоучасток Алматинской области15.	2025-10-22 07:34:02.541613+00	2025-10-22 07:34:02.541873+00	2025-10-22 07:34:02.541875+00	14	f	f
1154	f	\N	7896	Институт биоэнергетических культур и сахарной свеклы Украинской академии аграрных наук, Украина	2025-10-22 07:34:02.542777+00	2025-10-22 07:34:02.543052+00	2025-10-22 07:34:02.543055+00	361	f	f
442	f	\N	5797	Институт ботаники и фитоинтродукции растений Академии наук Республики Казахстан	2025-10-22 07:34:02.543562+00	2025-10-16 17:31:25.676127+00	2025-10-22 07:34:02.543583+00	15	f	f
1155	f	\N	8199	Институт винограда и вина «Магарач» (Украина)159.	2025-10-22 07:34:02.543863+00	2025-10-22 07:34:02.544162+00	2025-10-22 07:34:02.544165+00	158	f	f
1156	f	\N	6745	Институт гельминтологии имени К.С. Скрябина	2025-10-22 07:34:02.544614+00	2025-10-22 07:34:02.54493+00	2025-10-22 07:34:02.544934+00	88	f	f
593	f	\N	7753	РГП «Научноисследовательский институт проблем биологической безопасности» Министерства здравоохранения Республики Казахстан	2025-10-16 17:31:25.755286+00	2025-10-16 17:31:25.755632+00	2025-10-16 17:31:25.755634+00	\N	f	f
551	f	\N	7261	Оригинатор не зарегистрирован	2025-10-22 07:34:02.637008+00	2025-10-16 17:31:25.733983+00	2025-10-22 07:34:02.637035+00	1	f	f
562	f	\N	6190	Приднестровский научно-исследовательский институт сельского хозяйства	2025-10-22 07:34:02.645315+00	2025-10-16 17:31:25.739862+00	2025-10-22 07:34:02.645337+00	212	f	f
563	f	\N	7312	Производственный кооператив «Имени Ходжа Ахмеда Яссави», город Шымкент	2025-10-22 07:34:02.647075+00	2025-10-16 17:31:25.74035+00	2025-10-22 07:34:02.647094+00	250	f	f
567	f	\N	6274	Профген до Бразилия ЛТДА (лимитада), Бразилия	2025-10-22 07:34:02.648162+00	2025-10-16 17:31:25.742293+00	2025-10-22 07:34:02.648184+00	306	f	f
592	f	\N	7634	Республиканское государственное казенное предприятие «Национальный центр по биотехнологии Республики Казахстан», город Степногорск	2025-10-22 07:34:02.653563+00	2025-10-16 17:31:25.754825+00	2025-10-22 07:34:02.653582+00	281	f	f
600	f	\N	6164	РГП НПЦ переробатыв. и пищевой промышленности	2025-10-16 17:31:25.759113+00	2025-10-16 17:31:25.759361+00	2025-10-16 17:31:25.759364+00	\N	f	f
609	f	\N	7089	Роберт Гебриэл, США	2025-10-16 17:31:25.763699+00	2025-10-16 17:31:25.76403+00	2025-10-16 17:31:25.764033+00	\N	f	f
613	f	\N	6056	Рурал Девелопмент Администрейшн, Корея	2025-10-16 17:31:25.765906+00	2025-10-16 17:31:25.76612+00	2025-10-16 17:31:25.766123+00	\N	f	f
623	f	\N	7035	Секобра- 	2025-10-16 17:31:25.770082+00	2025-10-16 17:31:25.770289+00	2025-10-16 17:31:25.770292+00	\N	f	f
628	f	\N	7793	Семиллас Батлле, С.А	2025-10-16 17:31:25.773451+00	2025-10-16 17:31:25.773775+00	2025-10-16 17:31:25.773777+00	\N	f	f
616	f	\N	6310	GOLDEN WEST SEED BULGARIA (limited trade development), Болгария	2025-10-22 07:34:02.443015+00	2025-10-16 17:31:25.767363+00	2025-10-22 07:34:02.443034+00	372	f	f
619	f	\N	6167	Алнарпская опытная станция садоводства, Швеция	2025-10-22 07:34:02.47821+00	2025-10-16 17:31:25.768617+00	2025-10-22 07:34:02.478249+00	257	f	f
639	f	\N	6902	В.В. Воронин	2025-10-22 07:34:02.494567+00	2025-10-16 17:31:25.779154+00	2025-10-22 07:34:02.494591+00	297	f	f
1157	f	\N	8200	Институт садоводства Украинской аграрной академии наук160.	2025-10-22 07:34:02.547376+00	2025-10-22 07:34:02.547652+00	2025-10-22 07:34:02.547654+00	159	f	f
1158	f	\N	8154	Институт химической физики имени Н.Н. Семенова Российской академии наук90.	2025-10-22 07:34:02.549792+00	2025-10-22 07:34:02.550079+00	2025-10-22 07:34:02.550082+00	89	f	f
637	f	\N	5710	Синцзянская компания науки и технологии семенной промышленности КэПуЛи ЛТД, Китай	2025-10-16 17:31:25.77795+00	2025-10-16 17:31:25.778189+00	2025-10-16 17:31:25.778192+00	\N	f	f
638	f	\N	6577	СКНИИ СХ; ТОО "СКНИИ СХ" 	2025-10-16 17:31:25.778421+00	2025-10-16 17:31:25.778644+00	2025-10-16 17:31:25.778647+00	\N	f	f
1159	f	\N	8155	Йыгеваская селекционная станция93.	2025-10-22 07:34:02.553826+00	2025-10-22 07:34:02.55411+00	2025-10-22 07:34:02.554112+00	92	f	f
1160	f	\N	5916	Кабардино-Балкарская государственная сельскохозяйственная опытная станция	2025-10-22 07:34:02.554486+00	2025-10-22 07:34:02.554835+00	2025-10-22 07:34:02.554837+00	93	f	f
1161	f	\N	8111	Казахская зональная опытная станция18.	2025-10-22 07:34:02.555169+00	2025-10-22 07:34:02.555463+00	2025-10-22 07:34:02.555466+00	17	f	f
1162	f	\N	8269	Казахский государственный национальный университет имени Аль-Фараби256.	2025-10-22 07:34:02.556445+00	2025-10-22 07:34:02.556699+00	2025-10-22 07:34:02.556701+00	255	f	f
1163	f	\N	6848	Казахский НИИ каракульеводства	2025-10-22 07:34:02.557603+00	2025-10-22 07:34:02.557866+00	2025-10-22 07:34:02.557868+00	\N	f	f
1164	f	\N	8289	Камут предприятия Европы353.	2025-10-22 07:34:02.558794+00	2025-10-22 07:34:02.55907+00	2025-10-22 07:34:02.559072+00	352	f	f
605	f	\N	6473	Республиканское государственное казенное предприятие «Келеский», Туркестанская область	2025-10-22 07:34:02.65244+00	2025-10-16 17:31:25.761552+00	2025-10-22 07:34:02.652458+00	278	f	f
649	f	\N	7264	США в 1880 году	2025-10-16 17:31:25.784475+00	2025-10-16 17:31:25.784702+00	2025-10-16 17:31:25.784705+00	\N	f	f
612	f	\N	6038	Республиканское унитарное предприятие «Научно-Практический центр Национальной академии наук Беларуси по земледелию», Республика Беларусь	2025-10-22 07:34:02.654137+00	2025-10-16 17:31:25.765683+00	2025-10-22 07:34:02.654159+00	362	f	f
615	f	\N	7193	Саката Сид Корпорейшн, Япония	2025-10-22 07:34:02.655778+00	2025-10-16 17:31:25.766953+00	2025-10-22 07:34:02.655797+00	303	f	f
617	f	\N	6162	Самарский научно-исследовательский институт сельского хозяйства имени Н.М. Тулайкова	2025-10-22 07:34:02.657196+00	2025-10-16 17:31:25.767803+00	2025-10-22 07:34:02.657217+00	129	f	f
648	f	\N	6671	Сельскохозяйственный производственный кооператив семеноводческая фирма «Картофель»	2025-10-22 07:34:02.663554+00	2025-10-16 17:31:25.784254+00	2025-10-22 07:34:02.663574+00	277	f	f
599	f	\N	6776	Сибирский научно-исследовательский институт растениеводства и селекции	2025-10-22 07:34:02.666348+00	2025-10-16 17:31:25.75887+00	2025-10-22 07:34:02.666368+00	137	f	f
640	f	\N	6996	«Соларис хибриди» д.о.о., Сербия	2025-10-22 07:34:02.669803+00	2025-10-16 17:31:25.779723+00	2025-10-22 07:34:02.669822+00	443	f	f
629	f	\N	5784	Фирма «Семинис», Нидерланды	2025-10-22 07:34:02.782973+00	2025-10-16 17:31:25.774335+00	2025-10-22 07:34:02.782993+00	293	f	f
654	f	\N	7732	Тик Энтепрайсиз Пти Лимитед (AU)(TEAK ENTERPRISES Pty Limited, AU)	2025-10-16 17:31:25.786753+00	2025-10-16 17:31:25.786979+00	2025-10-16 17:31:25.786982+00	\N	f	f
655	f	\N	7358	Типа Хендриксон	2025-10-16 17:31:25.787202+00	2025-10-16 17:31:25.787471+00	2025-10-16 17:31:25.787474+00	\N	f	f
658	f	\N	7494	Томаровский Петр Федоровия	2025-10-16 17:31:25.789134+00	2025-10-16 17:31:25.789391+00	2025-10-16 17:31:25.789394+00	\N	f	f
665	f	\N	7745	ТОО EVS Group,Команов Евгений Николаевич	2025-10-16 17:31:25.792488+00	2025-10-16 17:31:25.792706+00	2025-10-16 17:31:25.792708+00	\N	f	f
667	f	\N	6869	ТОО"PAM DIO Science" РК.Лимагрейн Вернель Холдинг 	2025-10-16 17:31:25.793315+00	2025-10-16 17:31:25.793524+00	2025-10-16 17:31:25.793526+00	\N	f	f
668	f	\N	6694	ТОО "RAM Bioseience" РК.Limagrain Europa SA 	2025-10-16 17:31:25.793731+00	2025-10-16 17:31:25.793938+00	2025-10-16 17:31:25.79394+00	\N	f	f
669	f	\N	7672	ТОО "RAM Bioseience" РК.Nicerson international Research SNC 	2025-10-16 17:31:25.79414+00	2025-10-16 17:31:25.794349+00	2025-10-16 17:31:25.794351+00	\N	f	f
677	f	\N	6341	ТОО"Агро Италия Казахстан" ТОО Лайон Сиде (Италия)	2025-10-16 17:31:25.798762+00	2025-10-16 17:31:25.798995+00	2025-10-16 17:31:25.798997+00	\N	f	f
662	f	\N	5947	Barenburg Hollang B.V. (Besloten Vennootschap), Нидерланды	2025-10-22 07:34:02.428849+00	2025-10-16 17:31:25.791387+00	2025-10-22 07:34:02.428869+00	398	f	f
664	f	\N	6176	Gebroeders Bakker Zaadteelt en Zaadhandel B.V., Нидерланды	2025-10-22 07:34:02.441058+00	2025-10-16 17:31:25.792266+00	2025-10-22 07:34:02.441078+00	440	f	f
666	f	\N	6071	Strube D&S GmbH, Германия	2025-10-22 07:34:02.46492+00	2025-10-16 17:31:25.793115+00	2025-10-22 07:34:02.464941+00	241	f	f
1165	f	\N	6574	Карабалыкская сельскохозяйственная опытная станция	2025-10-22 07:34:02.559605+00	2025-10-22 07:34:02.559873+00	2025-10-22 07:34:02.559875+00	24	f	f
685	f	\N	7173	ТОО "Ак Бидай Агро"	2025-10-16 17:31:25.802291+00	2025-10-16 17:31:25.802544+00	2025-10-16 17:31:25.802547+00	\N	f	f
1166	f	\N	6721	Карагандинская сельскохозяйственная опытная станция	2025-10-22 07:34:02.5604+00	2025-10-22 07:34:02.56067+00	2025-10-22 07:34:02.560672+00	261	f	f
1167	f	\N	5846	Карагандинский научно-исследовательский институт растениеводства и селекции	2025-10-22 07:34:02.560974+00	2025-10-22 07:34:02.56145+00	2025-10-22 07:34:02.561452+00	43	f	f
1168	f	\N	8112	Карагандинский овощной государственный сортоиспытательный участок26.	2025-10-22 07:34:02.561797+00	2025-10-22 07:34:02.562141+00	2025-10-22 07:34:02.562145+00	25	f	f
1169	f	\N	8225	Каракалпакский научно исследовательский институт земледелия188.	2025-10-22 07:34:02.562494+00	2025-10-22 07:34:02.56279+00	2025-10-22 07:34:02.562792+00	187	f	f
1170	f	\N	8226	Каракалпакский филиал Академии наук Узбекистана189.	2025-10-22 07:34:02.563105+00	2025-10-22 07:34:02.563405+00	2025-10-22 07:34:02.563407+00	188	f	f
676	f	\N	6104	Общество с ограниченной ответственностью «Агрокомплекс» Кургансемена», город Курган, Россия	2025-10-22 07:34:02.61231+00	2025-10-16 17:31:25.798489+00	2025-10-22 07:34:02.61234+00	282	f	f
657	f	\N	6795	Товарищество с ограниченной ответсвенностью  фирма "КОЛОС"	2025-10-22 07:34:02.677509+00	2025-10-16 17:31:25.788838+00	2025-10-22 07:34:02.677529+00	287	f	f
695	f	\N	6903	ТОО "Алем Агро" LTD ОЗ Алтын Тарим Шилетмелеры Сан.Ве Тик А.Ш. - 	2025-10-16 17:31:25.808446+00	2025-10-16 17:31:25.808679+00	2025-10-16 17:31:25.808682+00	\N	f	f
672	f	\N	5851	Товарищество с ограниченной ответственностью «STEV AGRO», Казахстан	2025-10-22 07:34:02.678157+00	2025-10-16 17:31:25.795711+00	2025-10-22 07:34:02.67818+00	435	f	f
678	f	\N	6919	Товарищество с ограниченной ответственностью «Агросемконсалт»	2025-10-22 07:34:02.678873+00	2025-10-16 17:31:25.799447+00	2025-10-22 07:34:02.678896+00	275	f	f
699	f	\N	6301	ТОО "Алем Агро" ЛТД, G.I.E. Grass	2025-10-16 17:31:25.810287+00	2025-10-16 17:31:25.810517+00	2025-10-16 17:31:25.810519+00	\N	f	f
674	f	\N	6509	Тракийский сельскохозяйственный научно-исследовательский институт, Турция	2025-10-22 07:34:02.704808+00	2025-10-16 17:31:25.79713+00	2025-10-22 07:34:02.704834+00	418	f	f
684	f	\N	5853	Фирма «Сатимекс», Германия	2025-10-22 07:34:02.781941+00	2025-10-16 17:31:25.802082+00	2025-10-22 07:34:02.78196+00	290	f	f
703	f	\N	7250	ТОО"АРС RAGT 2N 	2025-10-16 17:31:25.812452+00	2025-10-16 17:31:25.812729+00	2025-10-16 17:31:25.812731+00	\N	f	f
706	f	\N	6325	ТОО "АРС АгроПлюс (Штробе ГмБХ) - 	2025-10-16 17:31:25.814455+00	2025-10-16 17:31:25.814715+00	2025-10-16 17:31:25.814718+00	\N	f	f
708	f	\N	7512	ТОО "А.С.К. Техник" Biotek Tohumculuk Tar,Ur.San.Tic.Ltd.Sti	2025-10-16 17:31:25.815437+00	2025-10-16 17:31:25.815652+00	2025-10-16 17:31:25.815655+00	\N	f	f
723	f	\N	7762	Cельскохозяйственный производственный кооператив «Будан», Казахстан	2025-10-22 07:34:02.433708+00	2025-10-16 17:31:25.824042+00	2025-10-22 07:34:02.433727+00	270	f	f
717	f	\N	6004	ТОО "Аят Транс Трейд"  Агрико И.А - 	2025-10-16 17:31:25.819416+00	2025-10-16 17:31:25.819637+00	2025-10-16 17:31:25.81964+00	\N	f	f
709	f	\N	7081	PROGEN TOHUM, Турция	2025-10-22 07:34:02.456869+00	2025-10-16 17:31:25.816123+00	2025-10-22 07:34:02.456892+00	484	f	f
722	f	\N	6263	Toft Plant Breeding APS, Дания	2025-10-22 07:34:02.465665+00	2025-10-16 17:31:25.823571+00	2025-10-22 07:34:02.465684+00	485	f	f
710	f	\N	6205	Евро Грасс Бридинг ГмбХ и Ко КГ, Германия	2025-10-22 07:34:02.529354+00	2025-10-16 17:31:25.816555+00	2025-10-22 07:34:02.529379+00	314	f	f
721	f	\N	6219	ТОО "Био-НАН"	2025-10-16 17:31:25.822471+00	2025-10-16 17:31:25.82288+00	2025-10-16 17:31:25.822883+00	\N	f	f
1171	f	\N	8113	Каратальское опытное поле Казахского научно-исследовательского института земледелия27.	2025-10-22 07:34:02.563751+00	2025-10-22 07:34:02.564014+00	2025-10-22 07:34:02.564016+00	26	f	f
1172	f	\N	8201	Киевская овощекартофельная опытная станция161.	2025-10-22 07:34:02.565021+00	2025-10-22 07:34:02.565286+00	2025-10-22 07:34:02.565289+00	160	f	f
726	f	\N	6461	ТОО Ворлд Вайд Вит США	2025-10-16 17:31:25.825222+00	2025-10-16 17:31:25.825464+00	2025-10-16 17:31:25.825467+00	\N	f	f
1173	f	\N	8241	Киргизская опытная станция хлопководства204.	2025-10-22 07:34:02.565559+00	2025-10-22 07:34:02.565801+00	2025-10-22 07:34:02.565803+00	203	f	f
729	f	\N	6468	ТОО Генезис - М Floromond Besprez Veure et Fils, Франция -	2025-10-16 17:31:25.826624+00	2025-10-16 17:31:25.826864+00	2025-10-16 17:31:25.826866+00	\N	f	f
1174	f	\N	8239	Киргизский научно исследовательский институт земледелия202.	2025-10-22 07:34:02.566062+00	2025-10-22 07:34:02.566362+00	2025-10-22 07:34:02.566365+00	201	f	f
1175	f	\N	8240	Киргизский научно-исследовательский технологический институт пастбищ и кормов203.	2025-10-22 07:34:02.566674+00	2025-10-22 07:34:02.566973+00	2025-10-22 07:34:02.566975+00	202	f	f
1176	f	\N	6117	«Клоз» Франция	2025-10-22 07:34:02.567309+00	2025-10-22 07:34:02.567565+00	2025-10-22 07:34:02.567567+00	308	f	f
734	f	\N	6798	ТОО "Жолбарыс Агро" 	2025-10-16 17:31:25.829039+00	2025-10-16 17:31:25.82945+00	2025-10-16 17:31:25.829453+00	\N	f	f
1177	f	\N	5828	Кокшетауский филиал Научно-производственного центра зернового хозяйства имени А.И. Бараева	2025-10-22 07:34:02.568474+00	2025-10-22 07:34:02.568749+00	2025-10-22 07:34:02.568752+00	27	f	f
1178	f	\N	6391	«Континентал Семенсиз», Италия	2025-10-22 07:34:02.572235+00	2025-10-22 07:34:02.572506+00	2025-10-22 07:34:02.572508+00	397	f	f
1179	f	\N	6011	Краснодарский научно-исследовательский институт овощного и картофельного хозяйства	2025-10-22 07:34:02.574141+00	2025-10-22 07:34:02.574388+00	2025-10-22 07:34:02.57439+00	95	f	f
1180	f	\N	7761	Крестьянское хозяйство "Иван"	2025-10-22 07:34:02.577704+00	2025-10-22 07:34:02.578225+00	2025-10-22 07:34:02.578233+00	468	f	f
1181	f	\N	8156	Крымская опытная станция садоводства101.	2025-10-22 07:34:02.579659+00	2025-10-22 07:34:02.579989+00	2025-10-22 07:34:02.579992+00	100	f	f
1182	f	\N	8157	Крымская селекционно-опытная станция Всероссийского научно-исследовательского института растениеводства102.	2025-10-22 07:34:02.580347+00	2025-10-22 07:34:02.580668+00	2025-10-22 07:34:02.58067+00	101	f	f
1183	f	\N	8158	Кубанский сельскохозяйственный институт103.	2025-10-22 07:34:02.580991+00	2025-10-22 07:34:02.581335+00	2025-10-22 07:34:02.581338+00	102	f	f
1184	f	\N	8159	Куйбышевская зональная опытная станция садоводства104.	2025-10-22 07:34:02.581731+00	2025-10-22 07:34:02.581982+00	2025-10-22 07:34:02.581984+00	103	f	f
1185	f	\N	6923	Курганский научно исследовательский институт зернового хозяйства	2025-10-22 07:34:02.58228+00	2025-10-22 07:34:02.58258+00	2025-10-22 07:34:02.582583+00	104	f	f
1186	f	\N	8160	Лаборатория гельминтологии Российской академии наук106.	2025-10-22 07:34:02.583425+00	2025-10-22 07:34:02.583689+00	2025-10-22 07:34:02.583691+00	105	f	f
1187	f	\N	8286	«Лайон Сидс» (LION SEEDS), Великобритания339.	2025-10-22 07:34:02.584467+00	2025-10-22 07:34:02.584714+00	2025-10-22 07:34:02.584716+00	338	f	f
1188	f	\N	8161	Ленинградский опорный пункт Института общей генетики Российской академии наук107.	2025-10-22 07:34:02.585209+00	2025-10-22 07:34:02.585474+00	2025-10-22 07:34:02.585476+00	106	f	f
6	f	\N	6870	Лимагрейн Европа, Франция	2025-10-22 07:34:02.585979+00	2025-10-16 17:31:25.448707+00	2025-10-22 07:34:02.586007+00	317	f	f
1189	f	\N	8252	Литовский научно-исследовательский институт плодоовощного хозяйства (Витенская плодовоовощная опытная станция)218.	2025-10-22 07:34:02.586373+00	2025-10-22 07:34:02.586676+00	2025-10-22 07:34:02.586679+00	217	f	f
1190	f	\N	8202	Луганская государственная областная сельскохозяйственная опытная станция162.	2025-10-22 07:34:02.586991+00	2025-10-22 07:34:02.587303+00	2025-10-22 07:34:02.587306+00	161	f	f
737	f	\N	6055	Фирма «Агрико», Нидерланды	2025-10-22 07:34:02.770155+00	2025-10-16 17:31:25.831824+00	2025-10-22 07:34:02.770184+00	223	f	f
943	f	\N	6269	Прикумский филиал Ставропольского научно-исследовательского института сельского хозяйства	2025-10-22 07:34:02.646548+00	2025-10-16 17:31:25.940457+00	2025-10-22 07:34:02.646568+00	127	f	f
750	f	\N	5863	Товарищество с ограниченной ответственностью «Казахский научно-исследовательский институт животноводства и кормопроизводства»	2025-10-22 07:34:02.681809+00	2025-10-16 17:31:25.838787+00	2025-10-22 07:34:02.681831+00	22	f	f
774	f	\N	6665	Акционерное общество «Солодовенный завод Суффле Казахстан»	2025-10-22 07:34:02.475054+00	2025-10-16 17:31:25.850734+00	2025-10-22 07:34:02.475073+00	325	f	f
784	f	\N	6784	Ист-Моллингская опытная станция садоводства, Англия	2025-10-22 07:34:02.553419+00	2025-10-16 17:31:25.856055+00	2025-10-22 07:34:02.553447+00	258	f	f
780	f	\N	5836	Казахский научно-исследовательский институт плодоводства и виноградарства	2025-10-22 07:34:02.557264+00	2025-10-16 17:31:25.853644+00	2025-10-22 07:34:02.557285+00	23	f	f
1191	f	\N	8162	Льговская опытная селекционная станция108.	2025-10-22 07:34:02.587624+00	2025-10-22 07:34:02.587915+00	2025-10-22 07:34:02.587918+00	107	f	f
1192	f	\N	8163	Майкопская опытная станция Всероссийского научно исследовательской института растениеводства109.	2025-10-22 07:34:02.588257+00	2025-10-22 07:34:02.588511+00	2025-10-22 07:34:02.588514+00	108	f	f
1193	f	\N	8203	Мироновский институт пшеницы имени В.Н. Ремесло163.	2025-10-22 07:34:02.59065+00	2025-10-22 07:34:02.590894+00	2025-10-22 07:34:02.590896+00	162	f	f
1194	f	\N	8164	Мичуринский государственный аграрный университет110.	2025-10-22 07:34:02.591218+00	2025-10-22 07:34:02.591469+00	2025-10-22 07:34:02.591471+00	109	f	f
1195	f	\N	8204	Млиевский научно-исследовательский институт садоводства лесостепи Украины имени Л.П. Симиренко164.	2025-10-22 07:34:02.591981+00	2025-10-22 07:34:02.59226+00	2025-10-22 07:34:02.592262+00	163	f	f
1196	f	\N	8246	Молдавский научно-исследовательский институт виноградарства и виноделия210.	2025-10-22 07:34:02.592547+00	2025-10-22 07:34:02.592806+00	2025-10-22 07:34:02.592809+00	209	f	f
1197	f	\N	8247	Молдавский научно-исследовательский институт орошаемого земледелия и овощеводства211.	2025-10-22 07:34:02.593057+00	2025-10-22 07:34:02.593316+00	2025-10-22 07:34:02.593319+00	210	f	f
1198	f	\N	8284	Монич Руслан Васильевич, Украина327.	2025-10-22 07:34:02.594212+00	2025-10-22 07:34:02.594523+00	2025-10-22 07:34:02.594526+00	326	f	f
1199	f	\N	8165	Московское отделение Всероссийского научно-исследовательского института растениеводства111.	2025-10-22 07:34:02.594848+00	2025-10-22 07:34:02.595151+00	2025-10-22 07:34:02.595154+00	110	f	f
1200	f	\N	8205	Научно-исследовательский институт земледелия и животноводства западных районов Украины165.	2025-10-22 07:34:02.596211+00	2025-10-22 07:34:02.596488+00	2025-10-22 07:34:02.596491+00	164	f	f
1201	f	\N	8206	Научно-исследовательский институт кукурузы Украины166.	2025-10-22 07:34:02.597273+00	2025-10-22 07:34:02.59755+00	2025-10-22 07:34:02.597553+00	165	f	f
1202	f	\N	8270	Научно-исследовательский институт садоводства имени Джона Инесса, город Мертон, Англия260.	2025-10-22 07:34:02.598422+00	2025-10-22 07:34:02.598671+00	2025-10-22 07:34:02.598673+00	259	f	f
1203	f	\N	8227	Научно-исследовательский институт селекции и семеноводства хлопчатника имени Г.С. Зайцева190.	2025-10-22 07:34:02.599481+00	2025-10-22 07:34:02.599723+00	2025-10-22 07:34:02.599725+00	189	f	f
1204	f	\N	8167	Научно-исследовательский институт сельского хозяйства Центрально-Черноземной полосы имени В.В. Докучаева114.	2025-10-22 07:34:02.600024+00	2025-10-22 07:34:02.600301+00	2025-10-22 07:34:02.600303+00	113	f	f
1205	f	\N	8168	Научно-исследовательский институт сельского хозяйства центральных районов Нечерноземной зоны116.	2025-10-22 07:34:02.6006+00	2025-10-22 07:34:02.60086+00	2025-10-22 07:34:02.600862+00	115	f	f
781	f	\N	6545	Товарищество с ограниченной ответственностью «Казахский научно-исследовательский институт лесного хозяйства и агролесомелиорации имени А.Н. Букейхана», Казахстан	2025-10-22 07:34:02.683389+00	2025-10-16 17:31:25.854156+00	2025-10-22 07:34:02.68341+00	462	f	f
777	f	\N	5870	Товарищество с ограниченной ответственностью «Казахский научно-исследовательский институт рисоводства имени И. Жахаева»	2025-10-22 07:34:02.684493+00	2025-10-16 17:31:25.852278+00	2025-10-22 07:34:02.68451+00	31	f	f
801	f	\N	6067	ТОО"Кокше-Диал" Мэй Агро Тохумкулук Санай ве Тикарет 	2025-10-16 17:31:25.864499+00	2025-10-16 17:31:25.864829+00	2025-10-16 17:31:25.864832+00	\N	f	f
802	f	\N	7819	ТОО "Корпорация NEXAGRO"	2025-10-16 17:31:25.8651+00	2025-10-16 17:31:25.86534+00	2025-10-16 17:31:25.865343+00	\N	f	f
803	f	\N	7758	ТОО "Кортаева Агрисаенс Казахстан"	2025-10-16 17:31:25.865568+00	2025-10-16 17:31:25.865819+00	2025-10-16 17:31:25.865822+00	\N	f	f
836	f	\N	6244	Agroscope Changins – Wädenswil ACW, Швейцария	2025-10-22 07:34:02.425539+00	2025-10-16 17:31:25.884143+00	2025-10-22 07:34:02.42556+00	370	f	f
842	f	\N	6852	Ijselmeerpolders B.V. (Besloten Vennootschap) (Айзельмеерпольдерс Б.В.), Нидерланды	2025-10-22 07:34:02.444233+00	2025-10-16 17:31:25.886948+00	2025-10-22 07:34:02.444252+00	394	f	f
839	f	\N	6102	Saatzucht Fritz Lange KG, Германия	2025-10-22 07:34:02.461463+00	2025-10-16 17:31:25.885504+00	2025-10-22 07:34:02.461487+00	395	f	f
810	f	\N	6381	Красноводопадская селекционная опытная станция	2025-10-22 07:34:02.573835+00	2025-10-16 17:31:25.868976+00	2025-10-22 07:34:02.573855+00	29	f	f
1206	f	\N	8267	Научно-производственное объединение «Нива Татарстана»253.	2025-10-22 07:34:02.602239+00	2025-10-22 07:34:02.602505+00	2025-10-22 07:34:02.602507+00	252	f	f
1207	f	\N	7102	Научный институт полеводства и овощеводства «Новый сад», Сербия и Черногория	2025-10-22 07:34:02.606034+00	2025-10-22 07:34:02.606426+00	2025-10-22 07:34:02.606429+00	289	f	f
1208	f	\N	8268	Национальный ботанический сад имени Н.Н. Гришко Национальной Академии Наук Украины255.	2025-10-22 07:34:02.606779+00	2025-10-22 07:34:02.607029+00	2025-10-22 07:34:02.607031+00	254	f	f
816	f	\N	6425	ТОО НИИ КОХ 	2025-10-16 17:31:25.872837+00	2025-10-16 17:31:25.873138+00	2025-10-16 17:31:25.873141+00	\N	f	f
1209	f	\N	8166	Нижне-Волжский научно-исследовательский институт сельского хозяйства112.	2025-10-22 07:34:02.60776+00	2025-10-22 07:34:02.608001+00	2025-10-22 07:34:02.608003+00	111	f	f
1210	f	\N	8169	Новосибирская зональная плодово-ягодная опытная станция имени И.В. Мичурина117.	2025-10-22 07:34:02.608309+00	2025-10-22 07:34:02.608582+00	2025-10-22 07:34:02.608585+00	116	f	f
1211	f	\N	8170	Новосибирский сельскохозяйственный институт118.	2025-10-22 07:34:02.608906+00	2025-10-22 07:34:02.609208+00	2025-10-22 07:34:02.609211+00	117	f	f
1212	f	\N	6396	Общество с ограниченной ответственностью «Агростандарт», Россия	2025-10-22 07:34:02.613993+00	2025-10-22 07:34:02.61434+00	2025-10-22 07:34:02.614342+00	403	f	f
1213	f	\N	6748	Общество с ограниченной ответственностью «ГСА Агро», Россия	2025-10-22 07:34:02.616773+00	2025-10-22 07:34:02.617023+00	2025-10-22 07:34:02.617025+00	478	f	f
1214	f	\N	8301	Общество с ограниченной ответственностью «Интер – Логистик Плюс», Россия430.	2025-10-22 07:34:02.618029+00	2025-10-22 07:34:02.618311+00	2025-10-22 07:34:02.618313+00	429	f	f
1215	f	\N	6142	Общество с ограниченной ответственностью Компания «Соевый комплекс», Россия	2025-10-22 07:34:02.618652+00	2025-10-22 07:34:02.618911+00	2025-10-22 07:34:02.618913+00	329	f	f
529	f	\N	5942	Общество с ограниченной ответственностью «Научно-производственное объединение Алтай», Россия	2025-10-22 07:34:02.623041+00	2025-10-16 17:31:25.721383+00	2025-10-22 07:34:02.62306+00	425	f	f
1216	f	\N	7972	Общество с ограниченной ответственностью «Опеновское», Россия	2025-10-22 07:34:02.623806+00	2025-10-22 07:34:02.624057+00	2025-10-22 07:34:02.624059+00	446	f	f
1217	f	\N	8294	Общество с ограниченной ответственностью Опытно-внедренческое предприятие «Покровское», Россия388.	2025-10-22 07:34:02.624337+00	2025-10-22 07:34:02.624579+00	2025-10-22 07:34:02.624581+00	387	f	f
1218	f	\N	8285	Общество с ограниченной ответственностью «Прогрейн Евразия», Украина331.	2025-10-22 07:34:02.624857+00	2025-10-22 07:34:02.625117+00	2025-10-22 07:34:02.62512+00	330	f	f
835	f	\N	6103	Общество с ограниченной ответственностью «Российская гибридная индустрия», Россия	2025-10-22 07:34:02.625668+00	2025-10-16 17:31:25.88365+00	2025-10-22 07:34:02.625687+00	409	f	f
1219	f	\N	8293	Общество с ограниченной ответственностью «Селекционная фирма Гавриш», Россия382.	2025-10-22 07:34:02.625963+00	2025-10-22 07:34:02.626238+00	2025-10-22 07:34:02.62624+00	381	f	f
837	f	\N	5777	ТОО "Рапуль Казахстан" Deusche Saatveredelung	2025-10-16 17:31:25.88438+00	2025-10-16 17:31:25.884606+00	2025-10-16 17:31:25.884609+00	\N	f	f
1220	f	\N	8306	Общество с ограниченной ответственностью «Селекционно -семеноводческий центр «Отбор»465.	2025-10-22 07:34:02.626516+00	2025-10-22 07:34:02.626759+00	2025-10-22 07:34:02.626761+00	464	f	f
1221	f	\N	8300	Общество с ограниченной ответственностью «Штрубе Рус», Россия429.	2025-10-22 07:34:02.629109+00	2025-10-22 07:34:02.62946+00	2025-10-22 07:34:02.629463+00	428	f	f
1222	f	\N	8171	Овощная опытная станция имени В.И. Эдельштейна Тимирязевской сельскохозяйственной академии119.	2025-10-22 07:34:02.630462+00	2025-10-22 07:34:02.630708+00	2025-10-22 07:34:02.630711+00	118	f	f
834	f	\N	6201	Товарищество с ограниченной ответственностью «Потейтоу Велли Ко», Южная Корея	2025-10-22 07:34:02.688135+00	2025-10-16 17:31:25.883208+00	2025-10-22 07:34:02.688165+00	336	f	f
843	f	\N	6890	Фирма «Дойче Заатфеределюнг Актиенгезельшафт», Германия	2025-10-22 07:34:02.773781+00	2025-10-16 17:31:25.88763+00	2025-10-22 07:34:02.773801+00	291	f	f
1223	f	\N	8207	Одесская государственная областная сельскохозяйственная станция167.	2025-10-22 07:34:02.631+00	2025-10-22 07:34:02.631284+00	2025-10-22 07:34:02.631286+00	166	f	f
1224	f	\N	7795	ООО "ЕВРОСЕМ"	2025-10-22 07:34:02.632958+00	2025-10-22 07:34:02.633233+00	2025-10-22 07:34:02.633235+00	\N	f	f
1225	f	\N	7830	ООО "ОРАНДО" Украина	2025-10-22 07:34:02.633762+00	2025-10-22 07:34:02.634037+00	2025-10-22 07:34:02.634039+00	\N	f	f
831	f	\N	5955	Павлодарский научно исследовательский институт сельского хозяйства	2025-10-22 07:34:02.639336+00	2025-10-16 17:31:25.880779+00	2025-10-22 07:34:02.639355+00	30	f	f
819	f	\N	5993	Фирма «Черны», Чехия	2025-10-22 07:34:02.790173+00	2025-10-16 17:31:25.874651+00	2025-10-22 07:34:02.790195+00	322	f	f
856	f	\N	6983	ТОО "Рапуль Нидера СА" 	2025-10-16 17:31:25.894505+00	2025-10-16 17:31:25.894726+00	2025-10-16 17:31:25.894728+00	\N	f	f
858	f	\N	7380	ТОО "Рейс Зваан Казахстан"	2025-10-16 17:31:25.8954+00	2025-10-16 17:31:25.895621+00	2025-10-16 17:31:25.895625+00	\N	f	f
869	f	\N	6988	ISEA Srl, Италия	2025-10-22 07:34:02.446297+00	2025-10-16 17:31:25.901572+00	2025-10-22 07:34:02.446316+00	351	f	f
871	f	\N	5876	Государственное учреждение «Институт масличных культур Национальной академии аграрных наук Украины», Украина	2025-10-22 07:34:02.51908+00	2025-10-16 17:31:25.902418+00	2025-10-22 07:34:02.519105+00	391	f	f
90	f	\N	5757	Компания «Заатен Юнион», Германия	2025-10-22 07:34:02.569739+00	2025-10-16 17:31:25.493778+00	2025-10-22 07:34:02.569766+00	292	f	f
857	f	\N	5970	Мартонвашарский сельскохозяйственный институт, Венгрия	2025-10-22 07:34:02.590112+00	2025-10-16 17:31:25.895176+00	2025-10-22 07:34:02.590145+00	349	f	f
886	f	\N	6559	Общество с ограниченной ответственностью «Всеукраинский научный институт селекции (ВНИС)», Украина	2025-10-22 07:34:02.616481+00	2025-10-16 17:31:25.909817+00	2025-10-22 07:34:02.616501+00	444	f	f
1226	f	\N	8173	Опытная станция по картофелю "Елецкая"121.	2025-10-22 07:34:02.634758+00	2025-10-22 07:34:02.635064+00	2025-10-22 07:34:02.635066+00	120	f	f
1227	f	\N	8172	Опытная станция по картофелю "Ульяновская"120.	2025-10-22 07:34:02.635501+00	2025-10-22 07:34:02.635765+00	2025-10-22 07:34:02.635767+00	119	f	f
1228	f	\N	8174	Оренбургский научно-исследовательский институт сельского хозяйства122.	2025-10-22 07:34:02.636067+00	2025-10-22 07:34:02.636388+00	2025-10-22 07:34:02.63639+00	121	f	f
1229	f	\N	8175	Орловский научно исследовательский институт сельского хозяйства123.	2025-10-22 07:34:02.637377+00	2025-10-22 07:34:02.63766+00	2025-10-22 07:34:02.637663+00	122	f	f
1230	f	\N	8176	Павловская опытная станция Всероссийского научно исследовательского института растениеводства124.	2025-10-22 07:34:02.638563+00	2025-10-22 07:34:02.638801+00	2025-10-22 07:34:02.638803+00	123	f	f
1231	f	\N	7884	Пацификс Сиде (Австрия)	2025-10-22 07:34:02.63986+00	2025-10-22 07:34:02.640117+00	2025-10-22 07:34:02.640119+00	\N	f	f
1232	f	\N	8177	Поволжский научно-исследовательский институт селекции и семеноводства имени П.Н. Константинова126.	2025-10-22 07:34:02.640893+00	2025-10-22 07:34:02.641146+00	2025-10-22 07:34:02.641148+00	125	f	f
1233	f	\N	8208	Полесская опытная станция имени А.Н. Засухина168.	2025-10-22 07:34:02.641411+00	2025-10-22 07:34:02.641691+00	2025-10-22 07:34:02.641693+00	167	f	f
887	f	\N	7817	ТОО "Сорея-Нур"	2025-10-16 17:31:25.910029+00	2025-10-16 17:31:25.91024+00	2025-10-16 17:31:25.910243+00	\N	f	f
888	f	\N	6616	ТОО Сочьета Продуттори Сементи (Италия)	2025-10-16 17:31:25.910489+00	2025-10-16 17:31:25.910718+00	2025-10-16 17:31:25.910721+00	\N	f	f
870	f	\N	7616	Полтавская государственная аграрная академия, Украина	2025-10-22 07:34:02.642162+00	2025-10-16 17:31:25.902+00	2025-10-22 07:34:02.642181+00	384	f	f
1234	f	\N	8209	Полтавская государственная областная сельскохозяйственная опытная станция169.	2025-10-22 07:34:02.642435+00	2025-10-22 07:34:02.642694+00	2025-10-22 07:34:02.642696+00	168	f	f
1235	f	\N	8178	Полярная опытная станция Всероссийского научно исследовательской института растениеводства127.	2025-10-22 07:34:02.642973+00	2025-10-22 07:34:02.643229+00	2025-10-22 07:34:02.643231+00	126	f	f
1236	f	\N	8281	Представительство «СИММИТ Казахстан»316.	2025-10-22 07:34:02.643699+00	2025-10-22 07:34:02.643958+00	2025-10-22 07:34:02.64396+00	315	f	f
879	f	\N	5742	Фирма «Сингента Сидс С.А.», Франция	2025-10-22 07:34:02.786404+00	2025-10-16 17:31:25.906644+00	2025-10-22 07:34:02.786431+00	233	f	f
859	f	\N	5790	Фирма «HZPC», Нидерланды	2025-10-22 07:34:02.767385+00	2025-10-16 17:31:25.896271+00	2025-10-22 07:34:02.767407+00	244	f	f
1237	f	\N	8114	Пригородный овоще молочный совхоз Алматинской области33.	2025-10-22 07:34:02.644229+00	2025-10-22 07:34:02.644536+00	2025-10-22 07:34:02.64454+00	32	f	f
1238	f	\N	8254	Приекульская опытно селекционная станция, Латвия220.	2025-10-22 07:34:02.645628+00	2025-10-22 07:34:02.645943+00	2025-10-22 07:34:02.645945+00	219	f	f
1239	f	\N	7468	Производственный сельскохозяйственный кооператив «Опытное»	2025-10-22 07:34:02.647415+00	2025-10-22 07:34:02.647663+00	2025-10-22 07:34:02.647665+00	266	f	f
1240	f	\N	8179	Пушкинские лаборатории Всероссийского научно-исследовательского института растениеводства129.	2025-10-22 07:34:02.648491+00	2025-10-22 07:34:02.648744+00	2025-10-22 07:34:02.648746+00	128	f	f
1241	f	\N	8264	Рейхель Н.В.243.	2025-10-22 07:34:02.650591+00	2025-10-22 07:34:02.650836+00	2025-10-22 07:34:02.650838+00	242	f	f
1242	f	\N	7746	Репаблик оф Корея (Рурал Девелопмент Администрэйшн)	2025-10-22 07:34:02.651146+00	2025-10-22 07:34:02.651393+00	2025-10-22 07:34:02.651395+00	\N	f	f
1243	f	\N	8243	Республиканская селекционно семеноводческая станция овощных и бахчевых культур, Республика Армения206.	2025-10-22 07:34:02.651685+00	2025-10-22 07:34:02.651928+00	2025-10-22 07:34:02.65193+00	205	f	f
863	f	\N	5889	Северо Казахстанская сельскохозяйственная опытная станция	2025-10-22 07:34:02.661607+00	2025-10-16 17:31:25.898905+00	2025-10-22 07:34:02.661627+00	34	f	f
1333	f	\N	8218	Центральная селекционно генетическая станция180.	2025-10-22 07:34:02.794696+00	2025-10-22 07:34:02.794982+00	2025-10-22 07:34:02.794984+00	179	f	f
902	f	\N	6895	Агро-ТИП Гмбх, Германия	2025-10-22 07:34:02.472738+00	2025-10-16 17:31:25.918139+00	2025-10-22 07:34:02.472757+00	337	f	f
926	f	\N	6388	Всероссийский научно-исследовательский институт зернобобовых и крупяных культур	2025-10-22 07:34:02.499945+00	2025-10-16 17:31:25.930175+00	2025-10-22 07:34:02.499965+00	59	f	f
904	f	\N	7567	ТОО ЧАФ "Тургень", Алматы-	2025-10-16 17:31:25.918853+00	2025-10-16 17:31:25.919079+00	2025-10-16 17:31:25.919082+00	\N	f	f
905	f	\N	7788	ТОО "Шортанбай 2019"	2025-10-16 17:31:25.919302+00	2025-10-16 17:31:25.919529+00	2025-10-16 17:31:25.919532+00	\N	f	f
906	f	\N	7642	ТОО "Эко Агро продукт" Франция	2025-10-16 17:31:25.919768+00	2025-10-16 17:31:25.92+00	2025-10-16 17:31:25.920003+00	\N	f	f
924	f	\N	6884	Государственное научное учреждение «Всероссийский научно-исследовательский институт зерновых культур имени И.Г.Калиненко», Россия	2025-10-22 07:34:02.516508+00	2025-10-16 17:31:25.928932+00	2025-10-22 07:34:02.516527+00	344	f	f
1244	f	\N	7072	Республиканское государственное казенное предприятие «Кокшетауский Государственный Университет имени Шокана Уалиханова»	2025-10-22 07:34:02.652739+00	2025-10-22 07:34:02.653007+00	2025-10-22 07:34:02.65301+00	286	f	f
1245	f	\N	8115	Рузаевская сельскохозяйственная опытная станция34.	2025-10-22 07:34:02.654678+00	2025-10-22 07:34:02.654978+00	2025-10-22 07:34:02.65498+00	33	f	f
1246	f	\N	8228	Самаркандский филиал Узбекского научно-исследовательского института садоводства, виноградарства и виноделия имени Р.Р. Шредера191.	2025-10-22 07:34:02.656094+00	2025-10-22 07:34:02.656444+00	2025-10-22 07:34:02.656447+00	190	f	f
1247	f	\N	8180	Санкт-Петербургский государственный аграрный университет131.	2025-10-22 07:34:02.657552+00	2025-10-22 07:34:02.65788+00	2025-10-22 07:34:02.657882+00	130	f	f
913	f	\N	7733	Туржанов Аскарбек Орманбекович	2025-10-16 17:31:25.923679+00	2025-10-16 17:31:25.923915+00	2025-10-16 17:31:25.923918+00	\N	f	f
1248	f	\N	8181	Саратовская государственная сельскохозяйственная академия имени Н.Н. Вавилова132.	2025-10-22 07:34:02.658235+00	2025-10-22 07:34:02.658521+00	2025-10-22 07:34:02.658524+00	131	f	f
1249	f	\N	8272	Саратовская опытная станция садоводства264.	2025-10-22 07:34:02.658831+00	2025-10-22 07:34:02.659081+00	2025-10-22 07:34:02.659083+00	263	f	f
918	f	\N	5868	Учреждение адвокадская контора Хасанова,  Компания "HZPC" IPR B.V - 	2025-10-16 17:31:25.925941+00	2025-10-16 17:31:25.926153+00	2025-10-16 17:31:25.926156+00	\N	f	f
920	f	\N	5778	Фалл Крийк Фарм & Нурсерй, Инк., США	2025-10-16 17:31:25.926776+00	2025-10-16 17:31:25.926983+00	2025-10-16 17:31:25.926986+00	\N	f	f
1250	f	\N	8182	Северо Западный научно-исследовательский институт сельского хозяйства, Россия134.	2025-10-22 07:34:02.659371+00	2025-10-22 07:34:02.659607+00	2025-10-22 07:34:02.659609+00	133	f	f
1251	f	\N	6804	Северо Западный научно-производственный центр сельского хозяйства	2025-10-22 07:34:02.65993+00	2025-10-22 07:34:02.660214+00	2025-10-22 07:34:02.660217+00	28	f	f
1252	f	\N	8290	Сельскохозяйственный институт Добруджа, Болгария358.	2025-10-22 07:34:02.662781+00	2025-10-22 07:34:02.663049+00	2025-10-22 07:34:02.663051+00	357	f	f
1253	f	\N	8116	Семипалатинский филиал Восточно-Казахстанского научно-исследовательского института сельского хозяйства36.	2025-10-22 07:34:02.664044+00	2025-10-22 07:34:02.664303+00	2025-10-22 07:34:02.664305+00	35	f	f
1254	f	\N	8292	Серебрякова Марина Сергеевна, Россия376.	2025-10-22 07:34:02.664593+00	2025-10-22 07:34:02.66484+00	2025-10-22 07:34:02.664842+00	375	f	f
1255	f	\N	8183	Сибирская опытная станция масличных культур136.	2025-10-22 07:34:02.665143+00	2025-10-22 07:34:02.665389+00	2025-10-22 07:34:02.665391+00	135	f	f
1256	f	\N	7947	Сибирский научно исследовательский институт кормов	2025-10-22 07:34:02.665661+00	2025-10-22 07:34:02.665907+00	2025-10-22 07:34:02.665909+00	136	f	f
105	f	\N	5745	Сингента Кроп Протекшн, Швейцария	2025-10-22 07:34:02.66731+00	2025-10-16 17:31:25.501825+00	2025-10-22 07:34:02.667329+00	358	f	f
1257	f	\N	8210	Синельниковская селекционно опытная станция171.	2025-10-22 07:34:02.667569+00	2025-10-22 07:34:02.667812+00	2025-10-22 07:34:02.667814+00	170	f	f
915	f	\N	7787	УНИГЕНЕТИК ЕООД, Болгария	2025-10-22 07:34:02.714468+00	2025-10-16 17:31:25.924858+00	2025-10-22 07:34:02.714491+00	424	f	f
916	f	\N	6286	Уральская сельскохозяйственная опытная станция	2025-10-22 07:34:02.715946+00	2025-10-16 17:31:25.925305+00	2025-10-22 07:34:02.715965+00	40	f	f
927	f	\N	7766	Федеральное государственное бюджетное научное учреждение «Всероссийский научно исследовательский институт органических удобрений и торфа», Россия	2025-10-22 07:34:02.719914+00	2025-10-16 17:31:25.931582+00	2025-10-22 07:34:02.719938+00	405	f	f
932	f	\N	6333	Федеральное государственное бюджетное научное учреждение «Национальный центр зерна имени П.П. Лукьяненко», Россия	2025-10-22 07:34:02.720514+00	2025-10-16 17:31:25.934049+00	2025-10-22 07:34:02.720534+00	479	f	f
934	f	\N	7113	Федеральное государственное бюджетное научное учреждение «Омский аграрный научный центр», Россия	2025-10-22 07:34:02.72131+00	2025-10-16 17:31:25.934921+00	2025-10-22 07:34:02.721336+00	421	f	f
921	f	\N	6416	Фирма «Бейо Заден», Нидерланды	2025-10-22 07:34:02.771734+00	2025-10-16 17:31:25.927423+00	2025-10-22 07:34:02.771773+00	221	f	f
956	f	\N	7844	Флорида Фаундэйшн Cид Продьюсерс, Инк. (Florida Foundation Seed Producers, Inc.)	2025-10-16 17:31:25.946273+00	2025-10-16 17:31:25.946532+00	2025-10-16 17:31:25.946535+00	\N	f	f
958	f	\N	7707	ФНИИ КОХ НПЦ ЗР	2025-10-16 17:31:25.947945+00	2025-10-16 17:31:25.948209+00	2025-10-16 17:31:25.948211+00	\N	f	f
987	f	\N	8020	An Jeongtak, Южная Корея	2025-10-22 07:34:02.426861+00	2025-10-21 21:50:08.555537+00	2025-10-22 07:34:02.426881+00	416	f	f
989	f	\N	8023	Baek Hyang Gu, Южная Корея	2025-10-22 07:34:02.428165+00	2025-10-21 21:50:08.558311+00	2025-10-22 07:34:02.428193+00	419	f	f
12	f	\N	5712	BASF Agricultural Solution Seed (United States limited liability company), Соединенные Штаты Америки	2025-10-22 07:34:02.429405+00	2025-10-16 17:31:25.452265+00	2025-10-22 07:34:02.429426+00	383	f	f
967	f	\N	6228	Хамзатханов Ислам Ибрагимович ФГБНУ "ВНИИМК им.Пуставойта"  -	2025-10-16 17:31:25.952251+00	2025-10-16 17:31:25.952472+00	2025-10-16 17:31:25.952474+00	\N	f	f
990	f	\N	8021	Choi Jae Won, Южная Корея	2025-10-22 07:34:02.431909+00	2025-10-21 21:50:08.563095+00	2025-10-22 07:34:02.431928+00	390	f	f
980	f	\N	5961	KAZSEEDS Limited, Казахстан	2025-10-22 07:34:02.44822+00	2025-10-16 17:31:25.959113+00	2025-10-22 07:34:02.448247+00	466	f	f
68	f	\N	5774	Monsanto Technology limited liability company, Соединенные Штаты Америки	2025-10-22 07:34:02.452694+00	2025-10-16 17:31:25.483111+00	2025-10-22 07:34:02.452715+00	348	f	f
994	f	\N	8029	Xisen Potato Industry Group Ltd. Co, Китайская Народная Республика	2025-10-22 07:34:02.468347+00	2025-10-21 21:50:08.572409+00	2025-10-22 07:34:02.468368+00	430	f	f
974	f	\N	6968	Центр аграрных научных исследовании венгерская академия 	2025-10-16 17:31:25.956138+00	2025-10-16 17:31:25.956351+00	2025-10-16 17:31:25.956354+00	\N	f	f
948	f	\N	6106	Институт цитологии и генетики Сибирского отделения Российской академии наук	2025-10-22 07:34:02.550636+00	2025-10-16 17:31:25.942891+00	2025-10-22 07:34:02.550655+00	90	f	f
979	f	\N	6012	Общество с ограниченной ответственностью научно-производственная компания «АгроАльянс», Россия	2025-10-22 07:34:02.62256+00	2025-10-16 17:31:25.958691+00	2025-10-22 07:34:02.622579+00	382	f	f
982	f	\N	6199	Шехзаделер маниса, Турция	2025-10-16 17:31:25.959751+00	2025-10-16 17:31:25.959966+00	2025-10-16 17:31:25.959969+00	\N	f	f
1258	f	\N	8117	Совхоз «Алматинский» Алматинской области37.	2025-10-22 07:34:02.668473+00	2025-10-22 07:34:02.668735+00	2025-10-22 07:34:02.668737+00	36	f	f
985	f	\N	7055	Югославия ТОО "МТС Югмаш"	2025-10-16 17:31:25.961092+00	2025-10-16 17:31:25.961339+00	2025-10-16 17:31:25.961341+00	\N	f	f
988	f	\N	8059	ArmanDevelop	2025-10-21 21:50:08.55712+00	2025-10-21 21:50:08.557384+00	2025-10-21 21:50:08.557386+00	\N	f	f
992	f	\N	8101	Co.na.se.soc.coop.Agr	2025-10-21 21:50:08.564332+00	2025-10-21 21:50:08.56455+00	2025-10-21 21:50:08.564552+00	\N	f	f
944	f	\N	7721	Уральский научно исследовательский институт сельского хозяйства	2025-10-22 07:34:02.716503+00	2025-10-16 17:31:25.941019+00	2025-10-22 07:34:02.716527+00	243	f	f
951	f	\N	7698	Федеральное государственное унитарное предприятие «Бакчарское», Россия	2025-10-22 07:34:02.763243+00	2025-10-16 17:31:25.94417+00	2025-10-22 07:34:02.763272+00	434	f	f
1259	f	\N	8118	Совхоз имени Томаровского Алматинской области38.	2025-10-22 07:34:02.669011+00	2025-10-22 07:34:02.669284+00	2025-10-22 07:34:02.669287+00	37	f	f
954	f	\N	6984	Фельдзаатен Фройденбергер ГмбХ, Германия	2025-10-22 07:34:02.764332+00	2025-10-16 17:31:25.9454+00	2025-10-22 07:34:02.764374+00	379	f	f
962	f	\N	5724	Фирма «Флоримонд Депре», Франция	2025-10-22 07:34:02.788065+00	2025-10-16 17:31:25.950212+00	2025-10-22 07:34:02.788084+00	240	f	f
972	f	\N	5713	Хроматин Инк, Соединенные Штаты Америки	2025-10-22 07:34:02.792898+00	2025-10-16 17:31:25.955404+00	2025-10-22 07:34:02.792917+00	378	f	f
978	f	\N	6947	Цезеа, Чехия	2025-10-22 07:34:02.793379+00	2025-10-16 17:31:25.958252+00	2025-10-22 07:34:02.7934+00	364	f	f
977	f	\N	7321	Частное предприятие Селекционно-производственный центр «Яровит», Украина	2025-10-22 07:34:02.797755+00	2025-10-16 17:31:25.957637+00	2025-10-22 07:34:02.797774+00	476	f	f
995	f	\N	8060	Tomato Research Center	2025-10-21 21:50:08.582287+00	2025-10-21 21:50:08.582531+00	2025-10-21 21:50:08.582534+00	\N	f	f
1020	f	\N	7952	Коюда Сергей Петрович()	2025-10-21 21:50:08.635105+00	2025-10-21 21:50:08.635313+00	2025-10-21 21:50:08.635315+00	\N	f	f
1031	f	\N	8054	ООО агрофирма "Сады Украины"	2025-10-21 21:50:08.654584+00	2025-10-21 21:50:08.654851+00	2025-10-21 21:50:08.654854+00	\N	f	f
149	f	\N	5729	Акционерное общество «Цинь Фен Юань», Китайская Народная Республика	2025-10-22 07:34:02.475558+00	2025-10-16 17:31:25.525018+00	2025-10-22 07:34:02.475577+00	376	f	f
194	f	\N	5943	Алтайский научно-исследовательский институт земледелия и селекции сельскохозяйственных культур	2025-10-22 07:34:02.479121+00	2025-10-16 17:31:25.547706+00	2025-10-22 07:34:02.47927+00	47	f	f
998	f	\N	7996	Ациро	2025-10-22 07:34:02.484327+00	2025-10-21 21:50:08.592688+00	2025-10-22 07:34:02.484346+00	16	f	f
1008	f	\N	7961	Государственное научное учреждение «Северо-Кубанская сельскохозяйственная опытная станция», Россия	2025-10-22 07:34:02.517537+00	2025-10-21 21:50:08.604931+00	2025-10-22 07:34:02.517558+00	413	f	f
1009	f	\N	7903	Донской зональный научно-исследовательский институт сельского хозяйства	2025-10-22 07:34:02.524851+00	2025-10-21 21:50:08.608297+00	2025-10-22 07:34:02.52487+00	82	f	f
321	f	\N	5894	Забайкальский научно исследовательский институт сельского хозяйства	2025-10-22 07:34:02.535389+00	2025-10-16 17:31:25.612789+00	2025-10-22 07:34:02.535411+00	86	f	f
1011	f	\N	7904	Закрытое акционерное общество научно-производственная фирма «Семена Дона», Россия	2025-10-22 07:34:02.536925+00	2025-10-21 21:50:08.61499+00	2025-10-22 07:34:02.536949+00	319	f	f
262	f	\N	5728	Закрытое акционерное общество «Научно-производственная фирма Сибирская аграрная компания», Россия	2025-10-22 07:34:02.537926+00	2025-10-16 17:31:25.582894+00	2025-10-22 07:34:02.537968+00	335	f	f
1029	f	\N	8013	Исильский питомник Омской области	2025-10-22 07:34:02.552306+00	2025-10-21 21:50:08.651317+00	2025-10-22 07:34:02.552333+00	91	f	f
430	f	\N	5950	Крестьянское хозяйство «Семена масличных», Казахстан	2025-10-22 07:34:02.579133+00	2025-10-16 17:31:25.669519+00	2025-10-22 07:34:02.579159+00	389	f	f
1023	f	\N	7981	Лазар Койич Хибриди, Сербия	2025-10-22 07:34:02.584186+00	2025-10-21 21:50:08.639751+00	2025-10-22 07:34:02.584204+00	363	f	f
1033	f	\N	7912	Молдавский научно исследовательский институт полевых культур	2025-10-22 07:34:02.593868+00	2025-10-21 21:50:08.659172+00	2025-10-22 07:34:02.593893+00	211	f	f
507	f	\N	5725	Общество с ограниченной ответственностью «АгроСемГавриш», Россия	2025-10-22 07:34:02.613533+00	2025-10-16 17:31:25.709911+00	2025-10-22 07:34:02.613557+00	366	f	f
1017	f	\N	8089	Северо-Кавказский научно-исследовательский институт горного и предгорного садоводства	2025-10-22 07:34:02.660932+00	2025-10-21 21:50:08.623858+00	2025-10-22 07:34:02.660967+00	134	f	f
359	f	\N	5806	Товарищество с ограниченной ответственностью «Казахский научно-исследовательский институт картофелеводства и овощеводства»	2025-10-22 07:34:02.682806+00	2025-10-16 17:31:25.632457+00	2025-10-22 07:34:02.682828+00	21	f	f
441	f	\N	5718	Фирма «Агра Сочета», Италия	2025-10-22 07:34:02.769279+00	2025-10-16 17:31:25.675683+00	2025-10-22 07:34:02.769319+00	222	f	f
1035	f	\N	7881	Пацифик Сидс	2025-10-21 21:50:08.664571+00	2025-10-21 21:50:08.664805+00	2025-10-21 21:50:08.664808+00	\N	f	f
1051	f	\N	8030	ТОО "BioTechTKS	2025-10-21 21:50:08.687442+00	2025-10-21 21:50:08.687707+00	2025-10-21 21:50:08.687709+00	\N	f	f
1053	f	\N	7915	ТОО"Астра Агро	2025-10-21 21:50:08.695087+00	2025-10-21 21:50:08.695324+00	2025-10-21 21:50:08.695326+00	\N	f	f
1063	f	\N	8027	ФГБНУ "Владимирский НИИСХ"	2025-10-21 21:50:08.722245+00	2025-10-21 21:50:08.722566+00	2025-10-21 21:50:08.722569+00	\N	f	f
690	f	\N	5909	Актюбинская сельскохозяйственная опытная станция	2025-10-22 07:34:02.474573+00	2025-10-16 17:31:25.805829+00	2025-10-22 07:34:02.474591+00	4	f	f
547	f	\N	5773	Восточно-Казахстанский научно-исследовательский институт сельского хозяйства	2025-10-22 07:34:02.498483+00	2025-10-16 17:31:25.732028+00	2025-10-22 07:34:02.498537+00	8	f	f
1060	f	\N	8007	Германцев Леонид Алексеевич, Россия	2025-10-22 07:34:02.511493+00	2025-10-21 21:50:08.717237+00	2025-10-22 07:34:02.511518+00	420	f	f
853	f	\N	5830	ЗААТЦУХТ ФРИТЦ ЛАНГЕ КГ, Германия	2025-10-22 07:34:02.534342+00	2025-10-16 17:31:25.893337+00	2025-10-22 07:34:02.534365+00	320	f	f
1043	f	\N	7944	Институт молекулярной биологии и биохимии им. М.А. Айтхожина	2025-10-22 07:34:02.5462+00	2025-10-21 21:50:08.673099+00	2025-10-22 07:34:02.546228+00	253	f	f
1041	f	\N	7925	Красноярская опытная станция плодоводства	2025-10-22 07:34:02.575991+00	2025-10-21 21:50:08.6715+00	2025-10-22 07:34:02.576011+00	98	f	f
570	f	\N	5759	Нордзаад Заатцухтзеллшафт мбХ, Германия	2025-10-22 07:34:02.60982+00	2025-10-16 17:31:25.743646+00	2025-10-22 07:34:02.60984+00	324	f	f
1052	f	\N	7914	Общество с ограниченной ответственностью «Агротехконсалт», Узбекистан	2025-10-22 07:34:02.61493+00	2025-10-21 21:50:08.690678+00	2025-10-22 07:34:02.614949+00	276	f	f
602	f	\N	5910	Региональный филиал «Кайнар» товарищества с ограниченной ответственностью «Казахский научно-исследовательский институт плодоовощеводства»	2025-10-22 07:34:02.65028+00	2025-10-16 17:31:25.760276+00	2025-10-22 07:34:02.650299+00	442	f	f
1055	f	\N	8097	Товарищество с ограниченной ответственностью «ДиЛэнд», Казахстан	2025-10-22 07:34:02.681317+00	2025-10-21 21:50:08.697967+00	2025-10-22 07:34:02.681337+00	436	f	f
1062	f	\N	8026	торфа"	2025-10-22 07:34:02.704203+00	2025-10-21 21:50:08.719241+00	2025-10-22 07:34:02.704226+00	405	f	f
923	f	\N	5816	Федеральное государственное бюджетное научное учреждение «Аграрный научный центр «Донской», Россия	2025-10-22 07:34:02.719357+00	2025-10-16 17:31:25.928361+00	2025-10-22 07:34:02.719381+00	475	f	f
931	f	\N	5809	Федеральное государственное бюджетное научное учреждение «Федеральный исследовательский центр Тюменский научный центр СО РАН», Россия	2025-10-22 07:34:02.755998+00	2025-10-16 17:31:25.9336+00	2025-10-22 07:34:02.756028+00	477	f	f
960	f	\N	5844	Фирма «ЗААТЗУХТ», Германия	2025-10-22 07:34:02.775294+00	2025-10-16 17:31:25.949294+00	2025-10-22 07:34:02.775315+00	283	f	f
847	f	\N	5714	Фирма «Норд Дойче Пфланценцухт», Германия	2025-10-22 07:34:02.778957+00	2025-10-16 17:31:25.890492+00	2025-10-22 07:34:02.778977+00	299	f	f
1262	f	\N	8211	Сумская государственная областная сельскохозяйственная опытная станция172.	2025-10-22 07:34:02.672272+00	2025-10-22 07:34:02.672543+00	2025-10-22 07:34:02.672545+00	171	f	f
1263	f	\N	8249	Таджикский научно исследовательский институт земледелия215.	2025-10-22 07:34:02.673096+00	2025-10-22 07:34:02.673367+00	2025-10-22 07:34:02.673369+00	214	f	f
1264	f	\N	8250	Таджикский научно-исследовательский институт садоводства, виноградарства и овощеводства216.	2025-10-22 07:34:02.673647+00	2025-10-22 07:34:02.673894+00	2025-10-22 07:34:02.673896+00	215	f	f
1265	f	\N	8119	Талгарский сельскохозяйственный техникум, Алматинская область39.	2025-10-22 07:34:02.674203+00	2025-10-22 07:34:02.674445+00	2025-10-22 07:34:02.674447+00	38	f	f
652	f	\N	5904	Талдыкорганский филиал Научно-производственного центра земледелия и растениеводства	2025-10-22 07:34:02.674949+00	2025-10-16 17:31:25.786011+00	2025-10-22 07:34:02.674968+00	39	f	f
1266	f	\N	8184	Тамбовская государственная областная сельскохозяйственная опытная станция141.	2025-10-22 07:34:02.675256+00	2025-10-22 07:34:02.675502+00	2025-10-22 07:34:02.675505+00	140	f	f
1267	f	\N	8185	Татарский научно исследовательский институт сельского хозяйства142.	2025-10-22 07:34:02.675789+00	2025-10-22 07:34:02.676031+00	2025-10-22 07:34:02.676034+00	141	f	f
1268	f	\N	8186	Тимирязевская сельскохозяйственная академия143.	2025-10-22 07:34:02.676552+00	2025-10-22 07:34:02.6768+00	2025-10-22 07:34:02.676802+00	142	f	f
1013	f	\N	7923	Товарищество с ограниченной ответственностью «Агрофирма «Бирлик», село Бирлик, Балхашский район, Алматинская область	2025-10-22 07:34:02.67954+00	2025-10-21 21:50:08.617656+00	2025-10-22 07:34:02.679563+00	287	f	f
1269	f	\N	6214	Товарищество с ограниченной ответственностью «Восточно Казахстанская сельскохозяйственная опытная станция»	2025-10-22 07:34:02.67987+00	2025-10-22 07:34:02.680175+00	2025-10-22 07:34:02.680177+00	470	f	f
1270	f	\N	8275	Товарищество с ограниченной ответственностью «Генофонд растений»281.	2025-10-22 07:34:02.680501+00	2025-10-22 07:34:02.680775+00	2025-10-22 07:34:02.680778+00	280	f	f
747	f	\N	5783	Товарищество с ограниченной ответственностью «Казахский научно-исследовательский институт плодоовощеводства»	2025-10-22 07:34:02.683927+00	2025-10-16 17:31:25.836589+00	2025-10-22 07:34:02.683948+00	471	f	f
1271	f	\N	6719	Товарищество с ограниченной ответственностью «Казахский научно-исследовательский институт хлопководства», Казахстан	2025-10-22 07:34:02.684808+00	2025-10-22 07:34:02.685094+00	2025-10-22 07:34:02.685096+00	461	f	f
1272	f	\N	6911	Товарищество с ограниченной ответственностью «Научно производственная фирма «Фитон», Костанайской области	2025-10-22 07:34:02.685398+00	2025-10-22 07:34:02.685663+00	2025-10-22 07:34:02.685665+00	251	f	f
1273	f	\N	8279	Товарищество с ограниченной ответственностью «НЛК»303.	2025-10-22 07:34:02.685953+00	2025-10-22 07:34:02.68678+00	2025-10-22 07:34:02.686783+00	302	f	f
827	f	\N	5720	Товарищество с ограниченной ответственностью «Опытное хозяйство масличных культур», Казахстан	2025-10-22 07:34:02.687505+00	2025-10-16 17:31:25.878329+00	2025-10-22 07:34:02.687527+00	458	f	f
1274	f	\N	7803	Товарищество с ограниченной ответственностью «Сельскохозяйственная опытная станция «Заречное», Казахстан	2025-10-22 07:34:02.688595+00	2025-10-22 07:34:02.68886+00	2025-10-22 07:34:02.688862+00	460	f	f
1275	f	\N	8003	Товарищество с ограниченной ответственностью «Ұлан – Жеміс»	2025-10-22 07:34:02.689183+00	2025-10-22 07:34:02.689454+00	2025-10-22 07:34:02.689456+00	400	f	f
1276	f	\N	8287	Товарищество с ограниченной ответственностью «Филип Моррис Казахстан»340.	2025-10-22 07:34:02.689757+00	2025-10-22 07:34:02.690009+00	2025-10-22 07:34:02.690011+00	339	f	f
1277	f	\N	8288	Товарищество с ограниченной ответственностью «Частная агропромышленная фирма «Тургень»351.	2025-10-22 07:34:02.69032+00	2025-10-22 07:34:02.690567+00	2025-10-22 07:34:02.690569+00	350	f	f
1278	f	\N	7270	ТОО "Агро Плюс Комерц ",РАЖТ 2 Н	2025-10-22 07:34:02.692439+00	2025-10-22 07:34:02.692675+00	2025-10-22 07:34:02.692677+00	\N	f	f
1279	f	\N	6974	ТОО "Алем Агро" ЛТД, ОзАлтын Тарим Ишлетмелеры Сан. Ве Тик А.Ш. -	2025-10-22 07:34:02.693627+00	2025-10-22 07:34:02.693868+00	2025-10-22 07:34:02.69387+00	\N	f	f
1280	f	\N	7200	ТОО Жемис Голландия	2025-10-22 07:34:02.696555+00	2025-10-22 07:34:02.696837+00	2025-10-22 07:34:02.696839+00	\N	f	f
1281	f	\N	8068	ТОО КОХ НИИ	2025-10-22 07:34:02.698067+00	2025-10-22 07:34:02.698317+00	2025-10-22 07:34:02.69832+00	\N	f	f
1282	f	\N	7015	ТОО научно сельсохозяйственная компания "Цзя Юй Гуань Хуа", КНР 	2025-10-22 07:34:02.698609+00	2025-10-22 07:34:02.698867+00	2025-10-22 07:34:02.698869+00	\N	f	f
1283	f	\N	7128	ТОО"Рапуль Казахстан" Агроскоп Шангинс-Веденсвил АЦВ  Рут де Дуллер 	2025-10-22 07:34:02.699585+00	2025-10-22 07:34:02.699827+00	2025-10-22 07:34:02.699829+00	\N	f	f
1284	f	\N	6990	ТОО "Рапуль Казахстан" (Евро ГрассБридинг 	2025-10-22 07:34:02.700309+00	2025-10-22 07:34:02.700608+00	2025-10-22 07:34:02.70061+00	\N	f	f
1285	f	\N	7941	ТОО"Рапуль Казахстан" РАПС	2025-10-22 07:34:02.7009+00	2025-10-22 07:34:02.701177+00	2025-10-22 07:34:02.701179+00	\N	f	f
1286	f	\N	7437	ТО " Рейк зваан Казахстан"	2025-10-22 07:34:02.70329+00	2025-10-22 07:34:02.703578+00	2025-10-22 07:34:02.70358+00	\N	f	f
1287	f	\N	8187	Тулунская государственная селекционная станция144.	2025-10-22 07:34:02.705119+00	2025-10-22 07:34:02.70538+00	2025-10-22 07:34:02.705382+00	143	f	f
1288	f	\N	8251	Туркменский научно исследовательский институт земледелия217.	2025-10-22 07:34:02.706121+00	2025-10-22 07:34:02.706551+00	2025-10-22 07:34:02.706555+00	216	f	f
1289	f	\N	8231	Узбекский научно исследовательский институт богарного земледелия194.	2025-10-22 07:34:02.706919+00	2025-10-22 07:34:02.707274+00	2025-10-22 07:34:02.707276+00	193	f	f
1290	f	\N	8232	Узбекский научно-исследовательский институт зерна195.	2025-10-22 07:34:02.70762+00	2025-10-22 07:34:02.707887+00	2025-10-22 07:34:02.707889+00	194	f	f
1291	f	\N	8233	Узбекский научно-исследовательский институт овощебахчевых культур и картофеля196.	2025-10-22 07:34:02.708185+00	2025-10-22 07:34:02.708439+00	2025-10-22 07:34:02.708441+00	195	f	f
1292	f	\N	8234	Узбекский научно-исследовательский институт риса197.	2025-10-22 07:34:02.708745+00	2025-10-22 07:34:02.709005+00	2025-10-22 07:34:02.709007+00	196	f	f
1293	f	\N	8235	Узбекский научно-исследовательский институт садоводства, виноградарства и виноделия имени академика Р.Р. Шредера198.	2025-10-22 07:34:02.709294+00	2025-10-22 07:34:02.709538+00	2025-10-22 07:34:02.70954+00	197	f	f
1294	f	\N	8212	Украинский научно исследовательский институт земледелия173.	2025-10-22 07:34:02.709814+00	2025-10-22 07:34:02.710072+00	2025-10-22 07:34:02.710075+00	172	f	f
1295	f	\N	8213	Украинский научно исследовательский институт инженерного проектирования174.	2025-10-22 07:34:02.710379+00	2025-10-22 07:34:02.710672+00	2025-10-22 07:34:02.710675+00	173	f	f
1296	f	\N	8214	Украинский научно исследовательский институт кормов175.	2025-10-22 07:34:02.71103+00	2025-10-22 07:34:02.711337+00	2025-10-22 07:34:02.711339+00	174	f	f
1297	f	\N	8215	Украинский научно-исследовательский институт овощеводства и бахчеводства176.	2025-10-22 07:34:02.711641+00	2025-10-22 07:34:02.711921+00	2025-10-22 07:34:02.711923+00	175	f	f
1298	f	\N	8216	Украинский научно-исследовательский институт растениеводства, селекции и генетики имени В.Я. Юрьева178.	2025-10-22 07:34:02.712864+00	2025-10-22 07:34:02.71321+00	2025-10-22 07:34:02.713212+00	177	f	f
1299	f	\N	8188	Ульяновский научно исследовательский институт сельского хозяйства145.	2025-10-22 07:34:02.713553+00	2025-10-22 07:34:02.713839+00	2025-10-22 07:34:02.713842+00	144	f	f
1300	f	\N	7332	Унипланта Заатцухт КГ, Германия	2025-10-22 07:34:02.71509+00	2025-10-22 07:34:02.715415+00	2025-10-22 07:34:02.715417+00	333	f	f
1006	f	\N	8039	Усть-Каменогорский опорный пункт Института цитологии и генетики Сибирского отделения Российской академии наук	2025-10-22 07:34:02.717043+00	2025-10-21 21:50:08.600311+00	2025-10-22 07:34:02.717064+00	41	f	f
1301	f	\N	8189	Учебно-опытное поле имени М.Н. Калинина146.	2025-10-22 07:34:02.717383+00	2025-10-22 07:34:02.717637+00	2025-10-22 07:34:02.717639+00	145	f	f
1302	f	\N	8302	Фарм Фритс, Нидерланды433.	2025-10-22 07:34:02.71834+00	2025-10-22 07:34:02.718579+00	2025-10-22 07:34:02.718581+00	432	f	f
532	f	\N	6010	Федеральное государственное бюджетное научное учреждение «Российский научно исследовательский и проектно-технологический институт сорго и кукурузы», Россия	2025-10-22 07:34:02.731794+00	2025-10-16 17:31:25.723552+00	2025-10-22 07:34:02.732284+00	386	f	f
1303	f	\N	7767	Федеральное государственное бюджетное научное учреждение «Сибирский федеральный научный центр агробиотехнологий Российской академии наук», Россия	2025-10-22 07:34:02.737464+00	2025-10-22 07:34:02.741558+00	2025-10-22 07:34:02.741569+00	404	f	f
1304	f	\N	8305	Федеральное государственное бюджетное научное учреждение Уфимский федеральный исследовательский центр Российской академии наук, Башкортостан454.	2025-10-22 07:34:02.74436+00	2025-10-22 07:34:02.748038+00	2025-10-22 07:34:02.748043+00	453	f	f
1305	f	\N	5978	Федеральное государственное бюджетное научное учреждение «Федеральный Алтайский научный центр агробиотехнологий», Россия	2025-10-22 07:34:02.751693+00	2025-10-22 07:34:02.754902+00	2025-10-22 07:34:02.754907+00	401	f	f
1306	f	\N	8299	Федеральное государственное бюджетное научное учреждение «Федеральный научный центр агроэкологии, комплексных мелиораций и защитного лесоразведения Российской академии наук», Россия428.	2025-10-22 07:34:02.756407+00	2025-10-22 07:34:02.756725+00	2025-10-22 07:34:02.756727+00	427	f	f
1307	f	\N	8304	Федеральное государственное бюджетное научное учреждение «Федеральный научный центр лубяных культур», Россия453.	2025-10-22 07:34:02.757799+00	2025-10-22 07:34:02.758097+00	2025-10-22 07:34:02.758099+00	452	f	f
1308	f	\N	7396	Федеральное государственное бюджетное научное учреждение «Челябинский научно-исследовательский институт сельского хозяйства», Россия	2025-10-22 07:34:02.758476+00	2025-10-22 07:34:02.758852+00	2025-10-22 07:34:02.758856+00	455	f	f
1067	f	\N	7879	Федеральное государственное бюджетное учреждение науки «Федеральный исследовательский центр «Казанский научный центр Российской академии наук», Татарстан	2025-10-22 07:34:02.761262+00	2025-10-21 21:50:08.726961+00	2025-10-22 07:34:02.761306+00	450	f	f
1309	f	\N	8237	Ферганская зональная научно-исследовательская станция шелководства200.	2025-10-22 07:34:02.765009+00	2025-10-22 07:34:02.765455+00	2025-10-22 07:34:02.765458+00	199	f	f
1310	f	\N	8236	Филиал виноделия Узбекского научно-исследовательского института садоводства199.	2025-10-22 07:34:02.765861+00	2025-10-22 07:34:02.76624+00	2025-10-22 07:34:02.766243+00	198	f	f
1311	f	\N	8297	Фирма «Hild Samen Gesellschaft mit beschränkter Haftung», Германия411.	2025-10-22 07:34:02.766588+00	2025-10-22 07:34:02.766868+00	2025-10-22 07:34:02.766871+00	410	f	f
1312	f	\N	8255	Фирма «Баболна», Венгрия225.	2025-10-22 07:34:02.770494+00	2025-10-22 07:34:02.770861+00	2025-10-22 07:34:02.770863+00	224	f	f
1313	f	\N	8256	Фирма «ВанДерХаве», Нидерланды226.	2025-10-22 07:34:02.772266+00	2025-10-22 07:34:02.772669+00	2025-10-22 07:34:02.772671+00	225	f	f
1314	f	\N	8257	Фирма «Декалб», Соединенные Штаты Америки227.	2025-10-22 07:34:02.772981+00	2025-10-22 07:34:02.773259+00	2025-10-22 07:34:02.773262+00	226	f	f
1315	f	\N	8258	Фирма «Зенека», Великобритания229.	2025-10-22 07:34:02.775581+00	2025-10-22 07:34:02.775837+00	2025-10-22 07:34:02.775839+00	228	f	f
1316	f	\N	8259	Фирма «КВС», Германия231.	2025-10-22 07:34:02.776708+00	2025-10-22 07:34:02.776982+00	2025-10-22 07:34:02.776984+00	230	f	f
1317	f	\N	6236	Фирма «Монсанто», Швецария	2025-10-22 07:34:02.777955+00	2025-10-22 07:34:02.778295+00	2025-10-22 07:34:02.778298+00	247	f	f
1318	f	\N	8261	Фирма «Прогрейн Женетик», Франция236.	2025-10-22 07:34:02.7799+00	2025-10-22 07:34:02.780226+00	2025-10-22 07:34:02.780229+00	235	f	f
1319	f	\N	6508	Фирма «Рийк Цваан Заадтеелт ен Заадхандел Б.В.», Нидерланды	2025-10-22 07:34:02.78057+00	2025-10-22 07:34:02.780831+00	2025-10-22 07:34:02.780833+00	236	f	f
1320	f	\N	6399	Фирма «Роял Слейс», Нидерланды	2025-10-22 07:34:02.781167+00	2025-10-22 07:34:02.781416+00	2025-10-22 07:34:02.781418+00	237	f	f
1321	f	\N	7436	Фирма «Селена», Германия	2025-10-22 07:34:02.782225+00	2025-10-22 07:34:02.782494+00	2025-10-22 07:34:02.782497+00	273	f	f
1322	f	\N	8276	Фирма «Серасем», Франция285.	2025-10-22 07:34:02.783272+00	2025-10-22 07:34:02.783584+00	2025-10-22 07:34:02.783586+00	284	f	f
1323	f	\N	8262	Фирма «Сес Юроп», Бельгия239.	2025-10-22 07:34:02.783856+00	2025-10-22 07:34:02.784102+00	2025-10-22 07:34:02.784105+00	238	f	f
1324	f	\N	8263	Фирма «Сиба Гейги», Швейцария240.	2025-10-22 07:34:02.784437+00	2025-10-22 07:34:02.784705+00	2025-10-22 07:34:02.784707+00	239	f	f
1325	f	\N	8260	Фирма «Сингента Сидс А.Б.», Швеция233.	2025-10-22 07:34:02.784996+00	2025-10-22 07:34:02.78525+00	2025-10-22 07:34:02.785252+00	232	f	f
1326	f	\N	8273	Фирма «Сингента Сидс кфт», Венгрия268.	2025-10-22 07:34:02.785515+00	2025-10-22 07:34:02.785763+00	2025-10-22 07:34:02.785765+00	267	f	f
1327	f	\N	8265	Фирма «Холли Шугар», Соединенные Штаты Америки247.	2025-10-22 07:34:02.788417+00	2025-10-22 07:34:02.788668+00	2025-10-22 07:34:02.78867+00	246	f	f
1328	f	\N	8266	Фирма «Хордеум», Словакия250.	2025-10-22 07:34:02.788939+00	2025-10-22 07:34:02.789202+00	2025-10-22 07:34:02.789204+00	249	f	f
1329	f	\N	6108	Ф. "НуНЕМС  ЗАДЕН"	2025-10-22 07:34:02.790853+00	2025-10-22 07:34:02.791116+00	2025-10-22 07:34:02.791118+00	\N	f	f
1334	f	\N	8219	Центральный республиканский ботанический сад Академии наук Украины181.	2025-10-22 07:34:02.795299+00	2025-10-22 07:34:02.795568+00	2025-10-22 07:34:02.79557+00	180	f	f
1335	f	\N	8191	Центральный сибирский ботанический сад148.	2025-10-22 07:34:02.795894+00	2025-10-22 07:34:02.79622+00	2025-10-22 07:34:02.796223+00	147	f	f
1336	f	\N	8244	Цхалтубская опытная станция овощеводства научно исследовательский институт земледелия, Республика Грузия207.	2025-10-22 07:34:02.796492+00	2025-10-22 07:34:02.796731+00	2025-10-22 07:34:02.796733+00	206	f	f
1337	f	\N	8280	Частный питомник город Вилсбург, Соединенные Штаты Америки312.	2025-10-22 07:34:02.7986+00	2025-10-22 07:34:02.798891+00	2025-10-22 07:34:02.798894+00	311	f	f
1338	f	\N	8220	Черниговская государственная областная сельскохозяйственная опытная станция182.	2025-10-22 07:34:02.799173+00	2025-10-22 07:34:02.79944+00	2025-10-22 07:34:02.799443+00	181	f	f
1339	f	\N	8121	Чиликский табачный государственный сортоиспытательный участок Алматинской области45.	2025-10-22 07:34:02.799708+00	2025-10-22 07:34:02.799951+00	2025-10-22 07:34:02.799953+00	44	f	f
1340	f	\N	6029	ЧП"Научная селекционно-семеноводческ. фирма" Соевой век 	2025-10-22 07:34:02.800257+00	2025-10-22 07:34:02.8005+00	2025-10-22 07:34:02.800502+00	\N	f	f
1341	f	\N	8192	Шадринская сельскохозяйственная опытная станция149.	2025-10-22 07:34:02.800754+00	2025-10-22 07:34:02.800999+00	2025-10-22 07:34:02.801001+00	148	f	f
1342	f	\N	8253	Эстонский научно-исследовательский институт земледелия и мелиорации219.	2025-10-22 07:34:02.801464+00	2025-10-22 07:34:02.801734+00	2025-10-22 07:34:02.801736+00	218	f	f
1343	f	\N	8122	Юго-Западный научно-производственный центр сельского хозяйства Министерства сельского хозяйства Республики Казахстан46.	2025-10-22 07:34:02.802482+00	2025-10-22 07:34:02.80276+00	2025-10-22 07:34:02.802763+00	45	f	f
\.


--
-- Data for Name: trials_app_planneddistribution; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.trials_app_planneddistribution (id, is_deleted, deleted_at, planting_season, status, year_started, year_completed, created_at, updated_at, notes, application_id, created_by_id, region_id, trial_type_id) FROM stdin;
\.


--
-- Data for Name: trials_app_region; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.trials_app_region (id, is_deleted, deleted_at, name, address, created_at, updated_at, climate_zone_id, oblast_id) FROM stdin;
1	f	\N	Кокшетауский ГСУ	\N	2025-10-16 08:53:53.924525+00	2025-10-16 08:53:53.924529+00	1	1
2	f	\N	Сандыктауский ГСУ	\N	2025-10-16 08:53:53.926359+00	2025-10-16 08:53:53.926364+00	1	1
3	f	\N	Шортандинский ГСУ	\N	2025-10-16 08:53:53.928309+00	2025-10-16 08:53:53.928312+00	2	1
4	f	\N	Целиноградский ГСУ	\N	2025-10-16 08:53:53.929205+00	2025-10-16 08:53:53.92921+00	2	1
5	f	\N	Егиндыкольский ГСУ	\N	2025-10-16 08:53:53.930809+00	2025-10-16 08:53:53.930813+00	3	1
6	f	\N	Жаксынский ГСУ	\N	2025-10-16 08:53:53.931559+00	2025-10-16 08:53:53.931563+00	3	1
7	f	\N	Арыкбалыкский ГСУ	\N	2025-10-16 08:53:53.932823+00	2025-10-16 08:53:53.932828+00	1	13
8	f	\N	Айыртауский ГСУ	\N	2025-10-16 08:53:53.933592+00	2025-10-16 08:53:53.933595+00	1	13
9	f	\N	Есильский ГСУ	\N	2025-10-16 08:53:53.934341+00	2025-10-16 08:53:53.934346+00	1	13
10	f	\N	Рузаевский ГСУ	\N	2025-10-16 08:53:53.935704+00	2025-10-16 08:53:53.935708+00	2	13
11	f	\N	Шалакынский ГСУ	\N	2025-10-16 08:53:53.936664+00	2025-10-16 08:53:53.936668+00	2	13
12	f	\N	Сергеевский ГСУ	\N	2025-10-16 08:53:53.937399+00	2025-10-16 08:53:53.937403+00	2	13
13	f	\N	Кызылжарский ГСУ	\N	2025-10-16 08:53:53.93808+00	2025-10-16 08:53:53.938083+00	2	13
14	f	\N	Мендыкаринский ГСУ	\N	2025-10-16 08:53:53.939259+00	2025-10-16 08:53:53.939263+00	2	9
15	f	\N	Федоровский ГСУ	\N	2025-10-16 08:53:53.939966+00	2025-10-16 08:53:53.939969+00	2	9
16	f	\N	Казахстанская ГСС	\N	2025-10-16 08:53:53.940763+00	2025-10-16 08:53:53.940767+00	2	9
17	f	\N	Костанайский комплексный ГСУ	\N	2025-10-16 08:53:53.941466+00	2025-10-16 08:53:53.941469+00	2	9
18	f	\N	Костанайский	\N	2025-10-16 08:53:53.942127+00	2025-10-16 08:53:53.942131+00	2	9
19	f	\N	Житикаринский	\N	2025-10-16 08:53:53.943439+00	2025-10-16 08:53:53.943445+00	3	9
20	f	\N	Железинская ГСС	\N	2025-10-16 08:53:53.944779+00	2025-10-16 08:53:53.944787+00	2	12
21	f	\N	Плодоовощной ГСУ	\N	2025-10-16 08:53:53.945803+00	2025-10-16 08:53:53.945807+00	2	12
22	f	\N	Телер	\N	2025-10-16 08:53:53.946489+00	2025-10-16 08:53:53.946493+00	2	12
23	f	\N	Иртышский комплексный ГСУ	\N	2025-10-16 08:53:53.947545+00	2025-10-16 08:53:53.947548+00	3	12
24	f	\N	Павлодарский зерновой ГСУ	\N	2025-10-16 08:53:53.948226+00	2025-10-16 08:53:53.94823+00	3	12
25	f	\N	Павлодарский овощной ГСУ	\N	2025-10-16 08:53:53.94916+00	2025-10-16 08:53:53.949165+00	3	12
26	f	\N	Карагандинский овощной ГСУ	\N	2025-10-16 08:53:53.950523+00	2025-10-16 08:53:53.950528+00	3	8
27	f	\N	Оскаровский ГСУ	\N	2025-10-16 08:53:53.951405+00	2025-10-16 08:53:53.95141+00	3	8
28	f	\N	Каркаралинский ГСУ	\N	2025-10-16 08:53:53.952835+00	2025-10-16 08:53:53.952838+00	4	8
29	f	\N	Жана-Аркинский ГСУ	\N	2025-10-16 08:53:53.954196+00	2025-10-16 08:53:53.954199+00	5	15
30	f	\N	Бурлинский ГСУ	\N	2025-10-16 08:53:53.955255+00	2025-10-16 08:53:53.955259+00	3	7
31	f	\N	Зелёновский ГСУ	\N	2025-10-16 08:53:53.955913+00	2025-10-16 08:53:53.955917+00	3	7
32	f	\N	Уральский ГСУ	\N	2025-10-16 08:53:53.95672+00	2025-10-16 08:53:53.956724+00	3	7
33	f	\N	Сырымский ГСУ	\N	2025-10-16 08:53:53.957534+00	2025-10-16 08:53:53.957539+00	3	7
34	f	\N	Алгинский ГСУ	\N	2025-10-16 08:53:53.958975+00	2025-10-16 08:53:53.958979+00	3	2
35	f	\N	Айтекебийский ГСУ	\N	2025-10-16 08:53:53.959825+00	2025-10-16 08:53:53.95983+00	3	2
36	f	\N	Мартукский ГСУ	\N	2025-10-16 08:53:53.961223+00	2025-10-16 08:53:53.961229+00	2	2
37	f	\N	Шемонаихинский ГСУ	\N	2025-10-16 08:53:53.962356+00	2025-10-16 08:53:53.96236+00	3	5
38	f	\N	Курчумский ГСС	\N	2025-10-16 08:53:53.963614+00	2025-10-16 08:53:53.963619+00	4	5
39	f	\N	ГСУ Алтай	\N	2025-10-16 08:53:53.964589+00	2025-10-16 08:53:53.964592+00	2	5
40	f	\N	Кокпектинский ГСУ	\N	2025-10-16 08:53:53.965687+00	2025-10-16 08:53:53.965691+00	2	16
41	f	\N	Новопокровский ГСУ	\N	2025-10-16 08:53:53.966468+00	2025-10-16 08:53:53.966472+00	2	16
42	f	\N	Урджарский ГСУ	\N	2025-10-16 08:53:53.967624+00	2025-10-16 08:53:53.967627+00	4	16
43	f	\N	Восточно-Казахстанский	\N	2025-10-16 08:53:53.968647+00	2025-10-16 08:53:53.96865+00	5	16
44	f	\N	Плодово-ягодный ГСУ	\N	2025-10-16 08:53:53.970146+00	2025-10-16 08:53:53.970149+00	6	17
45	f	\N	Талдыкорганский п/ягодный ГСУ	\N	2025-10-16 08:53:53.970767+00	2025-10-16 08:53:53.97077+00	6	17
46	f	\N	Карабулакский ГСУ	\N	2025-10-16 08:53:53.971362+00	2025-10-16 08:53:53.971365+00	6	17
47	f	\N	Когалинский ГСУ	\N	2025-10-16 08:53:53.971951+00	2025-10-16 08:53:53.971954+00	6	17
48	f	\N	Саркандский ГСУ	\N	2025-10-16 08:53:53.972624+00	2025-10-16 08:53:53.972627+00	6	17
49	f	\N	Панфиловский ГСУ	\N	2025-10-16 08:53:53.973455+00	2025-10-16 08:53:53.973459+00	6	17
50	f	\N	Кербулакский ГСУ	\N	2025-10-16 08:53:53.975331+00	2025-10-16 08:53:53.975335+00	7	17
51	f	\N	Балхашский рисовый	\N	2025-10-16 08:53:53.97671+00	2025-10-16 08:53:53.976714+00	8	3
52	f	\N	Алматинский п/ягодный ГСУ	\N	2025-10-16 08:53:53.978157+00	2025-10-16 08:53:53.97816+00	9	3
53	f	\N	Каскеленский п/ягодный ГСУ	\N	2025-10-16 08:53:53.978751+00	2025-10-16 08:53:53.978754+00	9	3
54	f	\N	Енбекшиказахский ГСУ	\N	2025-10-16 08:53:53.979411+00	2025-10-16 08:53:53.979414+00	9	3
55	f	\N	Илийский зерновой ГСУ	\N	2025-10-16 08:53:53.980066+00	2025-10-16 08:53:53.980071+00	9	3
56	f	\N	Илийский комплексный ГСУ	\N	2025-10-16 08:53:53.9807+00	2025-10-16 08:53:53.980704+00	9	3
57	f	\N	Райымбекский ГСУ	\N	2025-10-16 08:53:53.981347+00	2025-10-16 08:53:53.981351+00	9	3
58	f	\N	Шиелийский ГСУ	\N	2025-10-16 08:53:53.982956+00	2025-10-16 08:53:53.98296+00	10	10
59	f	\N	Жанакорганский ГСУ	\N	2025-10-16 08:53:53.983692+00	2025-10-16 08:53:53.983696+00	10	10
60	f	\N	Казалинский ГСУ	\N	2025-10-16 08:53:53.984525+00	2025-10-16 08:53:53.984528+00	10	10
61	f	\N	Жалагашский ГСУ	\N	2025-10-16 08:53:53.985298+00	2025-10-16 08:53:53.985304+00	10	10
62	f	\N	Хали	\N	2025-10-16 08:53:53.986083+00	2025-10-16 08:53:53.986087+00	10	10
63	f	\N	Т.Рыскуловский ГСУ	\N	2025-10-16 08:53:53.987015+00	2025-10-16 08:53:53.987019+00	7	6
64	f	\N	Жуалинский ГСУ	\N	2025-10-16 08:53:53.987668+00	2025-10-16 08:53:53.987671+00	7	6
65	f	\N	Жамбылский комплексный ГСУ	\N	2025-10-16 08:53:53.988251+00	2025-10-16 08:53:53.988254+00	7	6
66	f	\N	Байзакский ГСУ	\N	2025-10-16 08:53:53.988839+00	2025-10-16 08:53:53.988842+00	7	6
67	f	\N	Сарыагашский ГСУ	\N	2025-10-16 08:53:53.990647+00	2025-10-16 08:53:53.990651+00	11	14
68	f	\N	Ленгерский ГСУ	\N	2025-10-16 08:53:53.991399+00	2025-10-16 08:53:53.991403+00	11	14
69	f	\N	Сайрамский комплексный ГСУ	\N	2025-10-16 08:53:53.992084+00	2025-10-16 08:53:53.992089+00	11	14
70	f	\N	Георгиевский ГСУ	\N	2025-10-16 08:53:53.992757+00	2025-10-16 08:53:53.992761+00	11	14
71	f	\N	Сарыагашский п/ягодный ГСУ	\N	2025-10-16 08:53:53.993459+00	2025-10-16 08:53:53.993465+00	11	14
72	f	\N	Сарыагашский хлопковый ГСУ	\N	2025-10-16 08:53:53.994211+00	2025-10-16 08:53:53.994215+00	11	14
73	f	\N	Туркестанский ГСУ	\N	2025-10-16 08:53:53.995032+00	2025-10-16 08:53:53.995035+00	11	14
\.


--
-- Data for Name: trials_app_sortoriginator; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.trials_app_sortoriginator (id, percentage, originator_id, sort_record_id) FROM stdin;
1	100	67	10
2	100	13	19
3	100	13	20
4	100	887	21
5	100	887	22
6	100	887	23
8	100	113	62
9	100	541	63
10	100	523	64
11	100	87	67
12	100	4	70
13	100	4	71
14	100	4	72
15	100	4	73
16	100	4	74
19	100	56	124
20	100	170	125
21	100	56	126
23	100	4	128
24	100	4	129
28	100	102	133
29	100	102	136
39	100	529	151
42	100	920	154
43	100	505	155
46	100	513	158
47	100	513	160
49	100	513	163
51	100	28	165
52	100	65	166
53	100	513	167
54	100	529	168
55	100	513	169
56	100	513	170
57	100	513	171
58	100	6	172
61	100	113	175
63	100	6	177
65	100	6	179
66	100	513	180
67	100	513	181
68	100	513	182
69	100	513	183
74	100	65	188
75	100	65	189
76	100	65	190
82	100	87	196
83	100	65	197
84	100	65	198
85	100	60	199
86	100	60	200
87	100	60	201
93	100	428	207
94	100	428	208
95	100	428	209
96	100	511	210
97	100	12	211
101	100	6	215
103	100	34	217
104	100	34	221
106	100	511	223
107	100	131	224
108	100	297	225
109	100	297	226
110	100	297	227
111	100	430	228
112	100	511	229
115	100	96	232
118	100	3	235
119	100	428	236
122	100	131	239
123	100	131	240
124	100	131	241
125	100	131	242
126	100	131	243
127	100	131	244
128	50	453	245
130	100	34	246
131	100	34	247
138	100	453	254
139	100	540	255
140	100	518	256
141	100	518	257
142	100	518	258
143	100	518	259
150	100	932	272
154	100	430	285
158	100	6	319
159	100	6	320
162	100	506	323
163	100	827	324
168	100	95	329
169	100	95	330
172	100	505	333
173	100	505	334
174	100	95	335
175	100	95	336
176	100	95	337
194	100	777	541
251	100	827	620
256	100	863	625
266	100	87	640
272	100	934	647
273	100	934	648
274	50	831	649
276	100	934	650
277	100	934	651
281	50	831	655
292	100	827	664
293	100	827	665
301	100	827	673
313	100	106	685
317	100	90	697
323	100	6	741
327	100	918	746
328	100	918	748
329	100	95	750
331	100	505	752
332	100	95	754
334	100	95	758
348	100	932	778
349	100	932	779
351	100	932	781
352	100	545	782
353	100	545	783
354	100	545	784
355	100	545	785
358	100	516	798
360	100	516	800
361	100	516	801
363	100	920	803
364	100	516	804
365	100	516	806
367	100	516	809
395	100	516	843
396	100	516	844
397	100	516	846
414	100	487	875
417	100	3	878
418	100	3	879
419	100	3	880
420	100	3	881
421	100	934	882
422	100	65	884
423	100	28	885
424	100	87	886
431	100	628	894
432	100	628	896
433	100	628	898
434	100	131	899
436	100	827	902
439	100	827	906
440	100	827	908
441	100	827	910
443	100	827	913
450	100	827	922
454	100	131	929
455	100	37	930
465	100	541	940
466	100	541	941
467	100	541	942
471	50	723	946
473	100	13	947
474	100	13	948
475	100	13	949
477	100	86	952
479	100	827	956
480	100	86	957
483	100	86	960
486	100	43	965
487	100	86	966
490	100	934	970
491	100	43	972
500	100	628	984
502	100	12	987
514	100	73	1003
515	100	73	1004
516	100	73	1005
524	100	60	1012
525	100	60	1013
526	100	60	1014
527	100	60	1015
528	100	53	1016
529	100	53	1017
530	100	53	1018
531	100	53	1019
532	100	53	1020
533	100	53	1021
534	100	944	1022
535	100	53	1023
536	100	628	1024
537	100	37	1025
538	100	37	1026
539	100	37	1027
557	100	628	1054
558	100	95	1056
560	100	95	1058
561	100	95	1059
562	100	101	1060
563	100	101	1061
565	100	21	1063
566	100	21	1064
567	100	95	1065
570	100	95	1068
571	100	58	1069
572	100	58	1070
573	100	86	1072
574	100	86	1074
578	100	83	1078
579	100	6	1079
581	100	99	1082
582	100	96	1083
584	100	86	1086
585	100	86	1087
587	100	86	1090
588	100	86	1092
590	100	86	1095
591	100	86	1096
593	100	86	1099
594	100	86	1100
595	100	95	1101
605	100	934	1116
610	100	545	1124
613	10	528	1127
616	50	593	1130
619	100	934	1137
620	100	545	1138
622	100	545	1140
624	100	827	1142
631	100	944	1151
632	100	96	1153
633	100	96	1155
638	100	934	1164
639	100	934	1166
640	100	572	1168
642	100	95	1172
644	100	98	1176
645	100	690	1178
646	100	86	1180
649	100	827	1185
651	100	915	1187
653	100	506	1189
656	100	58	1192
658	100	58	1194
665	100	21	1200
667	100	60	1202
668	100	60	1203
669	100	60	1204
672	100	65	1207
676	100	827	1211
695	100	487	1240
699	100	665	1252
703	100	747	1256
704	100	871	1257
705	100	871	1258
706	100	871	1259
715	100	729	1269
718	100	827	1272
719	100	105	1273
721	100	690	1275
722	100	827	1276
723	100	831	1277
725	100	831	1279
728	100	934	1282
732	100	21	1286
733	100	21	1287
734	100	21	1288
743	100	863	1297
745	100	536	1299
746	100	506	1300
747	100	506	1301
754	100	750	1309
756	100	920	1311
762	100	750	1318
765	100	512	1321
766	100	512	1322
767	100	512	1323
771	100	238	1327
775	100	827	1331
785	100	967	1341
786	100	967	1342
789	100	943	1346
790	100	967	1347
795	100	979	1352
799	50	927	1355
812	100	827	1372
813	100	827	1373
814	100	827	1374
815	100	827	1375
816	100	913	1376
817	100	827	1377
818	100	913	1378
819	100	827	1379
820	100	827	1380
821	100	827	1381
822	100	827	1382
824	100	827	1384
827	100	827	1387
842	100	863	1403
846	100	734	1407
848	100	505	1410
849	50	617	1411
850	50	504	1411
854	100	827	1415
855	100	827	1416
856	100	672	1417
857	100	827	1418
860	100	831	1421
861	100	934	1422
862	100	483	1423
863	100	483	1424
865	100	483	1426
872	100	810	1433
874	100	827	1435
880	100	831	1441
881	100	512	1442
885	100	512	1446
887	100	934	1448
888	100	934	1449
890	100	934	1451
896	100	831	1457
904	100	934	1466
911	100	827	1473
912	100	827	1474
913	100	827	1475
915	100	592	1477
918	100	672	1480
919	100	613	1481
927	100	613	1489
929	100	810	1491
942	100	205	1504
944	100	810	1506
945	100	810	1507
959	100	36	1521
964	100	487	1526
965	100	827	1527
976	100	831	1537
979	100	750	1540
991	100	810	1552
993	100	487	1554
997	100	482	1558
999	100	487	1560
1000	100	482	1561
1002	100	690	1563
1006	100	831	1567
1013	100	810	1575
1016	100	979	1578
1023	100	810	1585
1026	100	810	1588
1033	100	827	1595
1052	100	690	1614
1053	100	395	1615
1055	100	690	1617
1070	100	321	1632
1097	100	359	1659
1128	100	307	1693
1144	100	863	1711
1146	100	863	1713
1149	100	690	1716
1150	100	863	1717
1151	100	205	1718
1152	100	205	1719
1159	100	205	1727
1160	100	205	1728
1161	100	810	1729
1165	100	205	1734
1166	100	205	1735
1167	100	205	1736
1168	100	205	1737
1169	100	205	1738
1170	100	205	1739
1171	100	205	1740
1179	100	810	1750
1180	100	205	1751
1181	100	205	1752
1182	100	205	1753
1183	100	205	1754
1184	100	205	1755
1185	100	810	1756
1188	100	827	1760
1189	100	904	1761
1190	100	904	1762
1201	100	205	1773
1203	100	36	1775
1204	100	36	1776
1205	100	36	1777
1209	100	205	1781
1218	100	810	1790
1223	100	810	1795
1228	100	863	1800
1229	100	592	1801
1238	100	810	1811
1242	100	863	1815
1250	100	205	1823
1251	100	321	1824
1254	100	359	1827
1255	100	321	1828
1256	100	321	1829
1258	100	863	1831
1259	100	205	1832
1260	100	205	1833
1261	100	205	1834
1263	100	321	1836
1264	100	863	1837
1287	100	750	1864
1289	100	827	1866
1295	100	810	1872
1300	100	827	1877
1303	100	810	1881
1305	100	747	1883
1316	100	810	1894
1322	100	827	1899
1334	100	863	1911
1336	100	863	1913
1343	100	836	1920
1344	100	168	1921
1345	100	827	1926
1354	100	810	1938
1357	100	453	1941
1359	100	781	1943
1362	100	863	1946
1366	100	810	1950
1367	100	863	1951
1371	100	810	1955
1373	100	827	1957
1374	100	690	1958
1375	100	827	1959
1376	100	827	1960
1387	100	827	1972
1397	100	613	1982
1398	100	118	1983
1401	100	487	1986
1407	100	827	1992
1412	100	345	1997
1418	100	831	2009
1419	100	831	2010
1431	100	205	2034
1434	100	321	2037
1438	100	750	2047
1439	100	831	2051
1457	100	376	2109
1460	100	750	2119
\.


--
-- Data for Name: trials_app_sortrecord; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.trials_app_sortrecord (id, is_deleted, deleted_at, sort_id, name, public_code, patents_status, lifestyle, characteristic, development_cycle, applicant, patent_nis, note, trial_notes, synced_at, created_at, updated_at, culture_id) FROM stdin;
2134	t	2025-10-22 07:36:38.553594+00	2249	Сорт для тестирования обновления	\N	\N	\N	\N	\N		f		\N	2025-10-21 22:07:50.102472+00	2025-10-21 22:07:50.102775+00	2025-10-22 07:36:38.553712+00	3
2132	t	2025-10-22 07:36:38.555699+00	2247	Арман 5	\N	\N	\N	\N	\N		f		\N	2025-10-21 21:50:12.982868+00	2025-10-21 21:50:12.983747+00	2025-10-22 07:36:38.555757+00	38
2131	t	2025-10-22 07:36:38.556803+00	2246	Арман 34	БД 20	\N	1	1	1	Тест 1	f	\N	\N	2025-10-20 07:33:24.276776+00	2025-10-20 07:33:24.23492+00	2025-10-22 07:36:38.556855+00	1
6	t	2025-10-22 07:36:38.558067+00	2245	Тестовый сорт	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:05.932817+00	2025-10-16 17:29:05.933837+00	2025-10-22 07:36:38.55813+00	32
5	t	2025-10-22 07:36:38.558912+00	2243	Патриция		\N	1	1	1		f	\N	\N	2025-10-16 17:21:56.128869+00	2025-10-16 09:04:46.271977+00	2025-10-22 07:36:38.558945+00	1
4	t	2025-10-22 07:36:38.559699+00	2244	Элайя		\N	1	1	1		f	\N	\N	2025-10-16 17:21:56.160117+00	2025-10-16 09:03:46.324557+00	2025-10-22 07:36:38.559735+00	1
2	f	\N	2242	БГ23-1633 (BG23-1633)		\N	1	1	1		f	\N	\N	2025-10-22 07:36:38.5616+00	2025-10-16 09:01:15.863746+00	2025-10-22 07:36:38.561708+00	53
1	f	\N	2241	БГ23-1637 (BG23-1637)		\N	1	1	1		f	\N	\N	2025-10-22 07:36:38.563572+00	2025-10-16 09:00:26.747378+00	2025-10-22 07:36:38.563607+00	53
3	f	\N	1926	Арай		1	1	2	1	ТОО «Казахский научно-исследователь-ский институт земледелия и растениеводства»	f	\N	\N	2025-10-16 17:21:56.192098+00	2025-10-16 09:02:16.585549+00	2025-10-16 17:21:56.192138+00	1
7	f	\N	2239	п/с Лазурная	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:05.939224+00	2025-10-16 17:29:05.939578+00	2025-10-16 17:29:05.939581+00	61
8	f	\N	2238	наурыз	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:05.940467+00	2025-10-16 17:29:05.940997+00	2025-10-16 17:29:05.941+00	119
9	f	\N	2237	Абака	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:05.942314+00	2025-10-16 17:29:05.942793+00	2025-10-16 17:29:05.942797+00	119
10	f	\N	2236	Купла / Cupla	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:05.943713+00	2025-10-16 17:29:05.944043+00	2025-10-16 17:29:05.944045+00	19
11	f	\N	2224	Казахстанский 70 пс	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:05.944713+00	2025-10-16 17:29:05.945038+00	2025-10-16 17:29:05.94504+00	76
12	f	\N	2223	Айна пс	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:05.945635+00	2025-10-16 17:29:05.946028+00	2025-10-16 17:29:05.946031+00	93
13	f	\N	2222	Династия пс	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:05.94656+00	2025-10-16 17:29:05.946875+00	2025-10-16 17:29:05.946877+00	93
14	f	\N	2221	Сыргалым	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:05.947352+00	2025-10-16 17:29:05.947642+00	2025-10-16 17:29:05.947644+00	76
15	f	\N	2220	Костасол	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:05.948135+00	2025-10-16 17:29:05.948386+00	2025-10-16 17:29:05.948388+00	88
16	f	\N	2218	Яркое юбилейное п/с	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:05.949032+00	2025-10-16 17:29:05.94945+00	2025-10-16 17:29:05.949453+00	90
17	f	\N	2217	Таганрог п/с	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:05.950382+00	2025-10-16 17:29:05.950808+00	2025-10-16 17:29:05.95081+00	124
18	f	\N	2216	Целинная юбилейная п/с	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:05.951538+00	2025-10-16 17:29:05.951918+00	2025-10-16 17:29:05.951921+00	93
19	f	\N	2215	Нова	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:05.952522+00	2025-10-16 17:29:05.95284+00	2025-10-16 17:29:05.952842+00	53
20	f	\N	2214	Бану	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:05.953372+00	2025-10-16 17:29:05.953654+00	2025-10-16 17:29:05.953657+00	53
21	f	\N	2213	Ария 200	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:05.954167+00	2025-10-16 17:29:05.954436+00	2025-10-16 17:29:05.954438+00	53
22	f	\N	2212	Ария 250	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:05.954942+00	2025-10-16 17:29:05.955199+00	2025-10-16 17:29:05.955202+00	53
23	f	\N	2211	Ария 300	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:05.955708+00	2025-10-16 17:29:05.955976+00	2025-10-16 17:29:05.955979+00	53
24	f	\N	2210	Аликос	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:05.956422+00	2025-10-16 17:29:05.956689+00	2025-10-16 17:29:05.956691+00	30
25	f	\N	2209	пс Манифест	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:05.95732+00	2025-10-16 17:29:05.957732+00	2025-10-16 17:29:05.957735+00	43
26	f	\N	2208	пс Аурум	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:05.9586+00	2025-10-16 17:29:05.959021+00	2025-10-16 17:29:05.959024+00	43
27	f	\N	2207	пс КВС Акбатор	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:05.959646+00	2025-10-16 17:29:05.959972+00	2025-10-16 17:29:05.959974+00	103
28	f	\N	2206	пс КВС Етерно	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:05.960465+00	2025-10-16 17:29:05.960778+00	2025-10-16 17:29:05.96078+00	103
29	f	\N	2205	пс Кокше	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:05.961259+00	2025-10-16 17:29:05.961533+00	2025-10-16 17:29:05.961535+00	61
30	f	\N	2204	пс RSD 982	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:05.96201+00	2025-10-16 17:29:05.962267+00	2025-10-16 17:29:05.962269+00	98
31	f	\N	2203	пс Брандер	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:05.962707+00	2025-10-16 17:29:05.962961+00	2025-10-16 17:29:05.962963+00	98
32	f	\N	2202	пс Казар	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:05.963413+00	2025-10-16 17:29:05.96368+00	2025-10-16 17:29:05.963683+00	56
33	f	\N	2201	пс Сиберия	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:05.964132+00	2025-10-16 17:29:05.964383+00	2025-10-16 17:29:05.964385+00	119
34	f	\N	2200	пс Аляска	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:05.964945+00	2025-10-16 17:29:05.965348+00	2025-10-16 17:29:05.965351+00	119
35	f	\N	2199	пс Майя	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:05.965995+00	2025-10-16 17:29:05.966391+00	2025-10-16 17:29:05.966393+00	119
36	f	\N	2198	пс Ариса	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:05.966928+00	2025-10-16 17:29:05.967279+00	2025-10-16 17:29:05.967282+00	119
37	f	\N	2197	пс Тайга	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:05.967971+00	2025-10-16 17:29:05.968299+00	2025-10-16 17:29:05.968301+00	119
38	f	\N	2196	пс Юнка	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:05.968858+00	2025-10-16 17:29:05.969141+00	2025-10-16 17:29:05.969143+00	119
39	f	\N	2195	пс JXR-7186	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:05.969645+00	2025-10-16 17:29:05.969924+00	2025-10-16 17:29:05.969927+00	88
40	f	\N	2194	пс Имидж	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:05.970367+00	2025-10-16 17:29:05.970603+00	2025-10-16 17:29:05.970606+00	88
41	f	\N	2193	пс НСХ 496	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:05.971257+00	2025-10-16 17:29:05.971497+00	2025-10-16 17:29:05.9715+00	88
42	f	\N	2192	пс Джинн	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:05.971938+00	2025-10-16 17:29:05.972184+00	2025-10-16 17:29:05.972186+00	88
43	f	\N	2191	пс Белла	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:05.972659+00	2025-10-16 17:29:05.972936+00	2025-10-16 17:29:05.972938+00	88
44	f	\N	2190	пс Белла	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:05.97342+00	2025-10-16 17:29:05.973686+00	2025-10-16 17:29:05.973688+00	88
45	f	\N	2189	пс Sumet	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:05.974162+00	2025-10-16 17:29:05.974557+00	2025-10-16 17:29:05.97456+00	88
46	f	\N	2188	пс МАС 85 СУ	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:05.975301+00	2025-10-16 17:29:05.975781+00	2025-10-16 17:29:05.975784+00	88
47	f	\N	2187	пс Baiterek S	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:05.976477+00	2025-10-16 17:29:05.976763+00	2025-10-16 17:29:05.976766+00	88
48	f	\N	2186	пс Светлана КЛП	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:05.977281+00	2025-10-16 17:29:05.977556+00	2025-10-16 17:29:05.977558+00	88
49	f	\N	2185	пс Pioneer P 63 LE 10	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:05.978084+00	2025-10-16 17:29:05.978354+00	2025-10-16 17:29:05.978356+00	88
50	f	\N	2184	пс Шығыс 9	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:05.978844+00	2025-10-16 17:29:05.979107+00	2025-10-16 17:29:05.97911+00	88
51	f	\N	2183	пс Даурен	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:05.97956+00	2025-10-16 17:29:05.979839+00	2025-10-16 17:29:05.979841+00	127
52	f	\N	2182	пс Байландо	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:05.980292+00	2025-10-16 17:29:05.980535+00	2025-10-16 17:29:05.980537+00	93
53	f	\N	2181	пс Квинтус	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:05.981016+00	2025-10-16 17:29:05.981294+00	2025-10-16 17:29:05.981296+00	93
54	f	\N	2180	пс Ликамеро	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:05.981761+00	2025-10-16 17:29:05.982012+00	2025-10-16 17:29:05.982014+00	93
55	f	\N	2179	пс Омская 36	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:05.982546+00	2025-10-16 17:29:05.983047+00	2025-10-16 17:29:05.983051+00	93
56	f	\N	2178	Альбасете	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:05.984252+00	2025-10-16 17:29:05.984699+00	2025-10-16 17:29:05.984703+00	93
57	f	\N	2177	пс Арабелла	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:05.985367+00	2025-10-16 17:29:05.985632+00	2025-10-16 17:29:05.985634+00	93
58	f	\N	2176	ДБ Тирас	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:05.986135+00	2025-10-16 17:29:05.986376+00	2025-10-16 17:29:05.986378+00	53
59	f	\N	2175	ДХ Акпадон	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:05.986819+00	2025-10-16 17:29:05.987094+00	2025-10-16 17:29:05.987096+00	53
60	f	\N	2174	ДХ Бакота	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:05.98754+00	2025-10-16 17:29:05.987794+00	2025-10-16 17:29:05.987796+00	53
61	f	\N	2173	ДХ Калюс	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:05.988233+00	2025-10-16 17:29:05.988472+00	2025-10-16 17:29:05.988474+00	53
62	f	\N	2172	Хюакси 948	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:05.988963+00	2025-10-16 17:29:05.989256+00	2025-10-16 17:29:05.989259+00	53
63	f	\N	2171	ТКС 1535	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:05.989762+00	2025-10-16 17:29:05.99001+00	2025-10-16 17:29:05.990012+00	53
64	f	\N	2170	Золотой початок 232 АМВ	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:05.990492+00	2025-10-16 17:29:05.99081+00	2025-10-16 17:29:05.990813+00	53
65	f	\N	2169	Гамилтон	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:05.991329+00	2025-10-16 17:29:05.991662+00	2025-10-16 17:29:05.991666+00	53
66	f	\N	2168	Вичита	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:05.992383+00	2025-10-16 17:29:05.992729+00	2025-10-16 17:29:05.992731+00	53
67	f	\N	2167	Арсантто	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:05.993553+00	2025-10-16 17:29:05.994031+00	2025-10-16 17:29:05.994034+00	53
68	f	\N	2166	АГН 720	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:05.994622+00	2025-10-16 17:29:05.994898+00	2025-10-16 17:29:05.9949+00	53
69	f	\N	2165	АГН 601	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:05.995379+00	2025-10-16 17:29:05.995659+00	2025-10-16 17:29:05.995661+00	53
70	f	\N	2164	АГМ-9	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:05.996113+00	2025-10-16 17:29:05.996387+00	2025-10-16 17:29:05.996389+00	53
71	f	\N	2163	АГМ-8	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:05.996861+00	2025-10-16 17:29:05.997125+00	2025-10-16 17:29:05.997127+00	53
72	f	\N	2162	АГМ-6	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:05.997573+00	2025-10-16 17:29:05.997847+00	2025-10-16 17:29:05.99785+00	53
73	f	\N	2161	АГМ-3	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:05.998402+00	2025-10-16 17:29:05.998787+00	2025-10-16 17:29:05.99879+00	53
74	f	\N	2160	АГМ-7	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:05.999588+00	2025-10-16 17:29:06.000066+00	2025-10-16 17:29:06.000069+00	53
75	f	\N	2159	Ахрам-2	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.000801+00	2025-10-16 17:29:06.001126+00	2025-10-16 17:29:06.001128+00	106
76	f	\N	2158	Амур Смарт (Amur Smart)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.001715+00	2025-10-16 17:29:06.001985+00	2025-10-16 17:29:06.001987+00	107
77	f	\N	2157	Атаман Смарт (ATAMAN SMART)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.00248+00	2025-10-16 17:29:06.002753+00	2025-10-16 17:29:06.002756+00	107
78	f	\N	2156	Айро	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.003256+00	2025-10-16 17:29:06.003564+00	2025-10-16 17:29:06.003566+00	88
79	f	\N	2155	Джамбо Стар (Jumbo Star)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.004019+00	2025-10-16 17:29:06.004263+00	2025-10-16 17:29:06.004265+00	117
80	f	\N	2154	Нутритоп Стар (Nutritop Star)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.004925+00	2025-10-16 17:29:06.0052+00	2025-10-16 17:29:06.005202+00	117
81	f	\N	2153	Алегриас (Alegrias)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.005649+00	2025-10-16 17:29:06.005929+00	2025-10-16 17:29:06.005931+00	93
82	f	\N	2152	Сенека (Seneca)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.006365+00	2025-10-16 17:29:06.006655+00	2025-10-16 17:29:06.006658+00	124
83	f	\N	2151	Космос	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.007212+00	2025-10-16 17:29:06.007634+00	2025-10-16 17:29:06.007636+00	150
84	f	\N	2150	Евсей (Evsei)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.008323+00	2025-10-16 17:29:06.008837+00	2025-10-16 17:29:06.008839+00	150
85	f	\N	2148	Жан	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.009633+00	2025-10-16 17:29:06.00995+00	2025-10-16 17:29:06.009953+00	127
86	f	\N	2147	КВС Эмфор (KWS Emphor)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.010446+00	2025-10-16 17:29:06.01073+00	2025-10-16 17:29:06.010733+00	103
87	f	\N	2146	КВС H10141	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.011254+00	2025-10-16 17:29:06.011557+00	2025-10-16 17:29:06.011559+00	103
88	f	\N	2145	ВИНКС (WINX)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.012103+00	2025-10-16 17:29:06.012391+00	2025-10-16 17:29:06.012394+00	93
89	f	\N	2144	МОУГЛИ (MOWGLI)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.012926+00	2025-10-16 17:29:06.013208+00	2025-10-16 17:29:06.01321+00	93
90	f	\N	2143	Тарантино (TARANTINO)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.013703+00	2025-10-16 17:29:06.013962+00	2025-10-16 17:29:06.013964+00	93
91	f	\N	2142	Леди Джейн	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.014415+00	2025-10-16 17:29:06.014657+00	2025-10-16 17:29:06.01466+00	43
92	f	\N	2141	Леди Алисия	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.015096+00	2025-10-16 17:29:06.015331+00	2025-10-16 17:29:06.015333+00	43
93	f	\N	2140	пс SY Atlante	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.015771+00	2025-10-16 17:29:06.016222+00	2025-10-16 17:29:06.016225+00	93
94	f	\N	2139	пс Виконт	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.016897+00	2025-10-16 17:29:06.017342+00	2025-10-16 17:29:06.017345+00	150
95	f	\N	2138	пс Одесский 22	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.018035+00	2025-10-16 17:29:06.018321+00	2025-10-16 17:29:06.018324+00	150
96	f	\N	2137	пс Уреньга	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.018867+00	2025-10-16 17:29:06.019127+00	2025-10-16 17:29:06.019129+00	150
97	f	\N	2136	пс RRSA 649/7	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.019621+00	2025-10-16 17:29:06.019893+00	2025-10-16 17:29:06.019895+00	102
98	f	\N	2135	пс Порумбень 235	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.020342+00	2025-10-16 17:29:06.020579+00	2025-10-16 17:29:06.020581+00	53
99	f	\N	2134	пс ГВ 9003	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.021104+00	2025-10-16 17:29:06.02135+00	2025-10-16 17:29:06.021353+00	53
100	f	\N	2133	пс Кодекса	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.021836+00	2025-10-16 17:29:06.022103+00	2025-10-16 17:29:06.022106+00	53
101	f	\N	2132	пс Мейджор	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.022594+00	2025-10-16 17:29:06.022888+00	2025-10-16 17:29:06.022891+00	53
102	f	\N	2131	пс П0217	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.023433+00	2025-10-16 17:29:06.023726+00	2025-10-16 17:29:06.023728+00	53
103	f	\N	2130	пс П7552	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.024492+00	2025-10-16 17:29:06.02495+00	2025-10-16 17:29:06.024954+00	53
104	f	\N	2129	пс П7552	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.025815+00	2025-10-16 17:29:06.026138+00	2025-10-16 17:29:06.02614+00	53
105	f	\N	2128	пс ДН Пивиха	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.026746+00	2025-10-16 17:29:06.027039+00	2025-10-16 17:29:06.027041+00	53
106	f	\N	2127	пс ДН Астра	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.027532+00	2025-10-16 17:29:06.027822+00	2025-10-16 17:29:06.027825+00	53
107	f	\N	2126	пс ДК Бурштин	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.028278+00	2025-10-16 17:29:06.028546+00	2025-10-16 17:29:06.028549+00	53
108	f	\N	2125	пс SY Prosperic	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.028992+00	2025-10-16 17:29:06.029256+00	2025-10-16 17:29:06.029258+00	53
109	f	\N	2124	пс Сай Майами	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.029705+00	2025-10-16 17:29:06.030002+00	2025-10-16 17:29:06.030004+00	53
110	f	\N	2123	пс ПР 2105	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.030484+00	2025-10-16 17:29:06.030812+00	2025-10-16 17:29:06.030814+00	53
111	f	\N	2122	пс ДКС 6777	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.031506+00	2025-10-16 17:29:06.031804+00	2025-10-16 17:29:06.031807+00	53
112	f	\N	2121	пс ЛГ 31545	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.03227+00	2025-10-16 17:29:06.032648+00	2025-10-16 17:29:06.032651+00	53
113	f	\N	2120	пс ЛГ 31545	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.033339+00	2025-10-16 17:29:06.033722+00	2025-10-16 17:29:06.033725+00	53
114	f	\N	2119	пс Инвитэйшн	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.034481+00	2025-10-16 17:29:06.034787+00	2025-10-16 17:29:06.034789+00	53
115	f	\N	2118	пс ЛГ 31380	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.035313+00	2025-10-16 17:29:06.035586+00	2025-10-16 17:29:06.035588+00	53
116	f	\N	2117	СИ Фуэрза	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.036073+00	2025-10-16 17:29:06.036347+00	2025-10-16 17:29:06.03635+00	53
117	f	\N	2116	Кепо	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.036847+00	2025-10-16 17:29:06.037104+00	2025-10-16 17:29:06.037107+00	39
118	f	\N	2115	пс Platinum Dynasty	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.037806+00	2025-10-16 17:29:06.038069+00	2025-10-16 17:29:06.038071+00	43
119	f	\N	2114	пс Алуэт	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.038546+00	2025-10-16 17:29:06.03883+00	2025-10-16 17:29:06.038833+00	43
120	f	\N	2113	пс Ред Скарлет	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.039274+00	2025-10-16 17:29:06.039519+00	2025-10-16 17:29:06.039521+00	43
121	f	\N	2112	пс Скарб	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.040034+00	2025-10-16 17:29:06.040317+00	2025-10-16 17:29:06.040319+00	43
122	f	\N	2111	пс Манифест	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.040932+00	2025-10-16 17:29:06.041291+00	2025-10-16 17:29:06.041294+00	43
123	f	\N	2110	пс Кингемен	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.041987+00	2025-10-16 17:29:06.042423+00	2025-10-16 17:29:06.042426+00	43
124	f	\N	2109	Санрайз	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.043056+00	2025-10-16 17:29:06.043356+00	2025-10-16 17:29:06.043359+00	56
125	f	\N	2108	Флиз	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.043836+00	2025-10-16 17:29:06.044081+00	2025-10-16 17:29:06.044083+00	56
126	f	\N	2107	Абакус	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.04455+00	2025-10-16 17:29:06.04485+00	2025-10-16 17:29:06.044853+00	56
127	f	\N	2106	ОСР23С54	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.045348+00	2025-10-16 17:29:06.045619+00	2025-10-16 17:29:06.045622+00	98
128	f	\N	2105	АГС-11	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.046062+00	2025-10-16 17:29:06.046298+00	2025-10-16 17:29:06.0463+00	98
129	f	\N	2104	АГС-12	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.04674+00	2025-10-16 17:29:06.046978+00	2025-10-16 17:29:06.046981+00	98
130	f	\N	2103	ДЛЕ25902С25	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.047425+00	2025-10-16 17:29:06.047688+00	2025-10-16 17:29:06.047691+00	98
131	f	\N	2102	ДЛЕ25845С15	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.048111+00	2025-10-16 17:29:06.048407+00	2025-10-16 17:29:06.048409+00	98
132	f	\N	2101	ДЛЕ24901С21	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.049077+00	2025-10-16 17:29:06.049458+00	2025-10-16 17:29:06.049461+00	98
133	f	\N	2100	Рустика 223 СУ	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.050321+00	2025-10-16 17:29:06.05064+00	2025-10-16 17:29:06.050642+00	88
134	f	\N	2099	Абака (Abaca)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.051179+00	2025-10-16 17:29:06.05145+00	2025-10-16 17:29:06.051453+00	119
135	f	\N	2098	Амбелла (Ambella)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.051899+00	2025-10-16 17:29:06.052172+00	2025-10-16 17:29:06.052174+00	119
136	f	\N	2097	СД45Е22	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.052653+00	2025-10-16 17:29:06.052928+00	2025-10-16 17:29:06.05293+00	88
137	f	\N	2096	Аксинья	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.053434+00	2025-10-16 17:29:06.053701+00	2025-10-16 17:29:06.053703+00	71
138	f	\N	2095	Краса дона	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.054142+00	2025-10-16 17:29:06.054377+00	2025-10-16 17:29:06.054379+00	71
139	f	\N	2094	Вольный дон	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.054856+00	2025-10-16 17:29:06.055101+00	2025-10-16 17:29:06.055103+00	71
140	f	\N	2093	Шеф	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.055548+00	2025-10-16 17:29:06.055856+00	2025-10-16 17:29:06.055859+00	71
141	f	\N	2092	Баргузин	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.056307+00	2025-10-16 17:29:06.056575+00	2025-10-16 17:29:06.056577+00	119
142	f	\N	2091	Этюд	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.057062+00	2025-10-16 17:29:06.05733+00	2025-10-16 17:29:06.057333+00	71
143	f	\N	2090	Нала	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.057961+00	2025-10-16 17:29:06.058301+00	2025-10-16 17:29:06.058304+00	119
144	f	\N	2089	ПР2501	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.059111+00	2025-10-16 17:29:06.059458+00	2025-10-16 17:29:06.059461+00	119
145	f	\N	2088	ПР2201	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.059998+00	2025-10-16 17:29:06.060268+00	2025-10-16 17:29:06.060271+00	119
146	f	\N	2087	ПР2202	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.060848+00	2025-10-16 17:29:06.061117+00	2025-10-16 17:29:06.061119+00	119
147	f	\N	2086	ОС23ФС136	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.061598+00	2025-10-16 17:29:06.061879+00	2025-10-16 17:29:06.061881+00	88
148	f	\N	2085	АГР 09	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.062318+00	2025-10-16 17:29:06.062557+00	2025-10-16 17:29:06.062559+00	88
149	f	\N	2084	АГР 11	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.062983+00	2025-10-16 17:29:06.063266+00	2025-10-16 17:29:06.063269+00	88
150	f	\N	2083	Аладдин	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.063772+00	2025-10-16 17:29:06.064078+00	2025-10-16 17:29:06.064081+00	88
151	f	\N	2082	Атом	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.064544+00	2025-10-16 17:29:06.064835+00	2025-10-16 17:29:06.064837+00	88
152	f	\N	2081	Василиса	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.065305+00	2025-10-16 17:29:06.065709+00	2025-10-16 17:29:06.065712+00	88
153	f	\N	2080	Фелиция	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.066288+00	2025-10-16 17:29:06.066673+00	2025-10-16 17:29:06.066676+00	61
154	f	\N	2079	FC12-205	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.067502+00	2025-10-16 17:29:06.067809+00	2025-10-16 17:29:06.067811+00	19
155	f	\N	2078	Никола	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.068303+00	2025-10-16 17:29:06.06858+00	2025-10-16 17:29:06.068583+00	124
156	f	\N	2077	Гарнет	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.069263+00	2025-10-16 17:29:06.069523+00	2025-10-16 17:29:06.069526+00	141
157	f	\N	2076	Сибирская	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.069983+00	2025-10-16 17:29:06.070253+00	2025-10-16 17:29:06.070255+00	141
158	f	\N	2075	Джедай	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.070685+00	2025-10-16 17:29:06.070921+00	2025-10-16 17:29:06.070923+00	88
159	f	\N	2074	Клип	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.071341+00	2025-10-16 17:29:06.071575+00	2025-10-16 17:29:06.071577+00	88
160	f	\N	2073	Мериот	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.072009+00	2025-10-16 17:29:06.072244+00	2025-10-16 17:29:06.072247+00	88
161	f	\N	2072	КазНИИЗиР-90СВ	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.072716+00	2025-10-16 17:29:06.072998+00	2025-10-16 17:29:06.073+00	54
162	f	\N	2071	NS H 8003	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.073476+00	2025-10-16 17:29:06.073724+00	2025-10-16 17:29:06.073726+00	88
163	f	\N	2070	Орис	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.074252+00	2025-10-16 17:29:06.074605+00	2025-10-16 17:29:06.074608+00	88
164	f	\N	2069	ОС23ФС137	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.07526+00	2025-10-16 17:29:06.075661+00	2025-10-16 17:29:06.075664+00	88
165	f	\N	2068	Софиасол	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.076464+00	2025-10-16 17:29:06.076762+00	2025-10-16 17:29:06.076765+00	88
166	f	\N	2067	Старфаер	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.077304+00	2025-10-16 17:29:06.077577+00	2025-10-16 17:29:06.077579+00	88
167	f	\N	2066	Чумацкий шлях	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.078044+00	2025-10-16 17:29:06.078285+00	2025-10-16 17:29:06.078287+00	88
168	f	\N	2065	Юнион	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.078723+00	2025-10-16 17:29:06.078994+00	2025-10-16 17:29:06.078996+00	88
169	f	\N	2064	Табун	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.079437+00	2025-10-16 17:29:06.079709+00	2025-10-16 17:29:06.079712+00	53
170	f	\N	2063	Кентавр	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.080151+00	2025-10-16 17:29:06.080389+00	2025-10-16 17:29:06.080391+00	53
171	f	\N	2062	Скифион	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.08086+00	2025-10-16 17:29:06.081129+00	2025-10-16 17:29:06.081131+00	53
172	f	\N	2061	ЛГ 31538	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.081587+00	2025-10-16 17:29:06.081864+00	2025-10-16 17:29:06.081866+00	53
173	f	\N	2060	ДМС Призер	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.082317+00	2025-10-16 17:29:06.082691+00	2025-10-16 17:29:06.082693+00	53
174	f	\N	2059	ДМС Тулон	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.083232+00	2025-10-16 17:29:06.083687+00	2025-10-16 17:29:06.08369+00	53
175	f	\N	2058	Ксианда 2024	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.084416+00	2025-10-16 17:29:06.08472+00	2025-10-16 17:29:06.084723+00	53
176	f	\N	2057	ДМС Эпос	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.085443+00	2025-10-16 17:29:06.085718+00	2025-10-16 17:29:06.08572+00	53
177	f	\N	2056	ЛГ 31400	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.086225+00	2025-10-16 17:29:06.086489+00	2025-10-16 17:29:06.086492+00	53
178	f	\N	2055	ЛГ 31515	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.086943+00	2025-10-16 17:29:06.087211+00	2025-10-16 17:29:06.087214+00	53
179	f	\N	2054	Горизон	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.087658+00	2025-10-16 17:29:06.087934+00	2025-10-16 17:29:06.087936+00	53
180	f	\N	2053	Номад	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.088377+00	2025-10-16 17:29:06.088625+00	2025-10-16 17:29:06.088629+00	53
181	f	\N	2052	Сармат	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.089122+00	2025-10-16 17:29:06.0894+00	2025-10-16 17:29:06.089402+00	53
182	f	\N	2051	Ковбой	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.08985+00	2025-10-16 17:29:06.090103+00	2025-10-16 17:29:06.090106+00	53
183	f	\N	2050	Тореадор	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.090545+00	2025-10-16 17:29:06.09091+00	2025-10-16 17:29:06.090957+00	53
184	f	\N	2049	СИ Курсор	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.091505+00	2025-10-16 17:29:06.09191+00	2025-10-16 17:29:06.091913+00	53
185	f	\N	2048	СИ Итака	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.092714+00	2025-10-16 17:29:06.093045+00	2025-10-16 17:29:06.093047+00	53
186	f	\N	2047	СИ Итака	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.09357+00	2025-10-16 17:29:06.093854+00	2025-10-16 17:29:06.093857+00	53
187	f	\N	2046	СИ Майлстон	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.094325+00	2025-10-16 17:29:06.094573+00	2025-10-16 17:29:06.094575+00	53
188	f	\N	2045	Астон	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.095045+00	2025-10-16 17:29:06.095285+00	2025-10-16 17:29:06.095287+00	53
189	f	\N	2044	МАС 250Ф	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.095732+00	2025-10-16 17:29:06.095967+00	2025-10-16 17:29:06.095969+00	53
190	f	\N	2043	Мас 400Д	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.096385+00	2025-10-16 17:29:06.096645+00	2025-10-16 17:29:06.096648+00	53
191	f	\N	2042	Бриозо	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.097091+00	2025-10-16 17:29:06.097397+00	2025-10-16 17:29:06.0974+00	53
192	f	\N	2041	КВС Рабато	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.097887+00	2025-10-16 17:29:06.098162+00	2025-10-16 17:29:06.098164+00	53
193	f	\N	2040	КВС Альканто	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.098647+00	2025-10-16 17:29:06.098918+00	2025-10-16 17:29:06.098921+00	53
194	f	\N	2039	КВС Авезо	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.099541+00	2025-10-16 17:29:06.09987+00	2025-10-16 17:29:06.099872+00	53
195	f	\N	2038	КВС Калейдо	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.100918+00	2025-10-16 17:29:06.101239+00	2025-10-16 17:29:06.101241+00	53
196	f	\N	2037	РА 8126042	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.101806+00	2025-10-16 17:29:06.102085+00	2025-10-16 17:29:06.102088+00	88
197	f	\N	2036	МАС 852СУ	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.102597+00	2025-10-16 17:29:06.102887+00	2025-10-16 17:29:06.102889+00	88
198	f	\N	2035	МАС 920КП	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.103335+00	2025-10-16 17:29:06.103592+00	2025-10-16 17:29:06.103594+00	88
199	f	\N	2034	1046 Х СУ	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.104038+00	2025-10-16 17:29:06.104274+00	2025-10-16 17:29:06.104277+00	88
200	f	\N	2033	1047 Л СЛП	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.104721+00	2025-10-16 17:29:06.104989+00	2025-10-16 17:29:06.104992+00	88
201	f	\N	2032	ЛИД 6038 Х СЛП	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.105487+00	2025-10-16 17:29:06.10587+00	2025-10-16 17:29:06.105873+00	88
202	f	\N	2031	КВС Юстос КЛ	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.10672+00	2025-10-16 17:29:06.106992+00	2025-10-16 17:29:06.106995+00	98
203	f	\N	2030	КВС Джерардос	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.107787+00	2025-10-16 17:29:06.108093+00	2025-10-16 17:29:06.108096+00	98
204	f	\N	2029	КВС Джерардос	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.109069+00	2025-10-16 17:29:06.109449+00	2025-10-16 17:29:06.109452+00	98
205	f	\N	2028	КВС Этнос КЛ	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.110043+00	2025-10-16 17:29:06.110318+00	2025-10-16 17:29:06.11032+00	98
206	f	\N	2027	КВС Адемес СУ	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.110795+00	2025-10-16 17:29:06.111059+00	2025-10-16 17:29:06.111061+00	88
207	f	\N	2026	БА Новатор	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.111524+00	2025-10-16 17:29:06.111812+00	2025-10-16 17:29:06.111815+00	88
208	f	\N	2025	БА Улан	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.112279+00	2025-10-16 17:29:06.112541+00	2025-10-16 17:29:06.112543+00	88
209	f	\N	2024	БА Прагматик	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.113015+00	2025-10-16 17:29:06.11326+00	2025-10-16 17:29:06.113263+00	88
210	f	\N	2023	Ориентир	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.1137+00	2025-10-16 17:29:06.11394+00	2025-10-16 17:29:06.113943+00	88
211	f	\N	2022	5 ЕН 0045	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.11438+00	2025-10-16 17:29:06.114663+00	2025-10-16 17:29:06.114666+00	98
212	f	\N	2021	Рокстон	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.115124+00	2025-10-16 17:29:06.115392+00	2025-10-16 17:29:06.115395+00	119
213	f	\N	2020	Хоуден	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.115936+00	2025-10-16 17:29:06.116244+00	2025-10-16 17:29:06.116246+00	119
214	f	\N	2019	ЛГ 50639 СХ	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.116904+00	2025-10-16 17:29:06.117454+00	2025-10-16 17:29:06.117461+00	88
215	f	\N	2018	ЛГ 50489 СХ	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.118487+00	2025-10-16 17:29:06.118873+00	2025-10-16 17:29:06.118876+00	88
216	f	\N	2017	НПЦ25001С	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.119459+00	2025-10-16 17:29:06.11974+00	2025-10-16 17:29:06.119742+00	98
217	f	\N	2016	Фениккс РСС155	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.120199+00	2025-10-16 17:29:06.120438+00	2025-10-16 17:29:06.12044+00	98
218	f	\N	2015	Чароит	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.120996+00	2025-10-16 17:29:06.121278+00	2025-10-16 17:29:06.121281+00	43
219	f	\N	2014	Приуральная	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.121789+00	2025-10-16 17:29:06.122037+00	2025-10-16 17:29:06.122039+00	71
220	f	\N	2013	Болашақ	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.122531+00	2025-10-16 17:29:06.122978+00	2025-10-16 17:29:06.122981+00	107
221	f	\N	2012	Фениккс ЭсЭль023	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.123471+00	2025-10-16 17:29:06.123735+00	2025-10-16 17:29:06.123738+00	88
222	f	\N	2011	Сәтті	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.124668+00	2025-10-16 17:29:06.125102+00	2025-10-16 17:29:06.125104+00	56
223	f	\N	2010	Катерина	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.125841+00	2025-10-16 17:29:06.126151+00	2025-10-16 17:29:06.126154+00	88
224	f	\N	2009	Хайсан 238 IT	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.126665+00	2025-10-16 17:29:06.126941+00	2025-10-16 17:29:06.126943+00	88
225	f	\N	2008	Мария Ими	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.127422+00	2025-10-16 17:29:06.127715+00	2025-10-16 17:29:06.127717+00	88
226	f	\N	2007	Валентина	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.12818+00	2025-10-16 17:29:06.128419+00	2025-10-16 17:29:06.128421+00	88
227	f	\N	2006	Куба	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.128862+00	2025-10-16 17:29:06.129139+00	2025-10-16 17:29:06.129141+00	88
228	f	\N	2005	Шығыс 24	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.129589+00	2025-10-16 17:29:06.129869+00	2025-10-16 17:29:06.129871+00	88
229	f	\N	2004	Азимут	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.130362+00	2025-10-16 17:29:06.130674+00	2025-10-16 17:29:06.130676+00	88
230	f	\N	2003	Кочевница	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.131155+00	2025-10-16 17:29:06.131402+00	2025-10-16 17:29:06.131404+00	93
231	f	\N	2002	Шортандинская 24	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.131845+00	2025-10-16 17:29:06.132091+00	2025-10-16 17:29:06.132094+00	93
232	f	\N	2001	Синди	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.13258+00	2025-10-16 17:29:06.133024+00	2025-10-16 17:29:06.133026+00	93
233	f	\N	2000	Актюбинская 70	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.133991+00	2025-10-16 17:29:06.134396+00	2025-10-16 17:29:06.134399+00	93
234	f	\N	1999	Тевкеч	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.134957+00	2025-10-16 17:29:06.135232+00	2025-10-16 17:29:06.135235+00	150
235	f	\N	1998	Белле	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.135731+00	2025-10-16 17:29:06.135985+00	2025-10-16 17:29:06.135987+00	121
236	f	\N	1997	Рейджана	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.136429+00	2025-10-16 17:29:06.136708+00	2025-10-16 17:29:06.136711+00	61
237	f	\N	1996	Фелиция	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.137162+00	2025-10-16 17:29:06.137443+00	2025-10-16 17:29:06.137445+00	61
238	f	\N	1995	Төзімді	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.137871+00	2025-10-16 17:29:06.138104+00	2025-10-16 17:29:06.138106+00	61
239	f	\N	1994	Джамбо Стар	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.138564+00	2025-10-16 17:29:06.138867+00	2025-10-16 17:29:06.138869+00	117
240	f	\N	1993	Нутритоп Стар	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.139377+00	2025-10-16 17:29:06.139669+00	2025-10-16 17:29:06.139672+00	117
241	f	\N	1992	Сентинел ИГ	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.140155+00	2025-10-16 17:29:06.140415+00	2025-10-16 17:29:06.140417+00	116
242	f	\N	1991	Зумба	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.141052+00	2025-10-16 17:29:06.141393+00	2025-10-16 17:29:06.141396+00	116
243	f	\N	1990	АФ 8301	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.142129+00	2025-10-16 17:29:06.142547+00	2025-10-16 17:29:06.142549+00	115
244	f	\N	1989	АФ 7102	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.143354+00	2025-10-16 17:29:06.143637+00	2025-10-16 17:29:06.143639+00	115
245	f	\N	1988	Мерей	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.144182+00	2025-10-16 17:29:06.144438+00	2025-10-16 17:29:06.14444+00	90
246	f	\N	1987	Фениккс ЦеЭль43	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.144875+00	2025-10-16 17:29:06.145147+00	2025-10-16 17:29:06.145149+00	133
247	f	\N	1986	Фениккс АшЭрЭс546	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.145622+00	2025-10-16 17:29:06.145892+00	2025-10-16 17:29:06.145894+00	102
248	f	\N	1985	ФД 25 Б 5143	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.146365+00	2025-10-16 17:29:06.146646+00	2025-10-16 17:29:06.146649+00	109
249	f	\N	1984	ФД ТАББИ	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.147133+00	2025-10-16 17:29:06.147411+00	2025-10-16 17:29:06.147414+00	109
250	f	\N	1983	ФД ЭПИК	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.14789+00	2025-10-16 17:29:06.148163+00	2025-10-16 17:29:06.148166+00	107
251	f	\N	1982	ФД 25 Б 5144	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.148635+00	2025-10-16 17:29:06.148912+00	2025-10-16 17:29:06.148915+00	109
252	f	\N	1981	БТС 2645	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.149532+00	2025-10-16 17:29:06.149866+00	2025-10-16 17:29:06.149868+00	109
253	f	\N	1980	БТС 590	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.150661+00	2025-10-16 17:29:06.151035+00	2025-10-16 17:29:06.151037+00	109
254	f	\N	1979	Силк Роуз	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.151659+00	2025-10-16 17:29:06.151968+00	2025-10-16 17:29:06.15197+00	43
255	f	\N	1978	Аляска	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.152469+00	2025-10-16 17:29:06.152739+00	2025-10-16 17:29:06.152742+00	43
256	f	\N	1977	Прайм	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.153174+00	2025-10-16 17:29:06.153411+00	2025-10-16 17:29:06.153413+00	43
257	f	\N	1976	Кармен	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.153837+00	2025-10-16 17:29:06.15408+00	2025-10-16 17:29:06.154083+00	43
258	f	\N	1975	Фламинго	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.154504+00	2025-10-16 17:29:06.154814+00	2025-10-16 17:29:06.154817+00	43
259	f	\N	1974	Атлетик	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.155265+00	2025-10-16 17:29:06.155506+00	2025-10-16 17:29:06.155508+00	43
260	f	\N	1973	Леграна	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.155931+00	2025-10-16 17:29:06.156233+00	2025-10-16 17:29:06.156235+00	68
261	f	\N	1972	Бриксберри	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.156813+00	2025-10-16 17:29:06.157133+00	2025-10-16 17:29:06.157143+00	5
262	f	\N	1971	Легента	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.15788+00	2025-10-16 17:29:06.15833+00	2025-10-16 17:29:06.158333+00	39
263	f	\N	1970	Панчи	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.159138+00	2025-10-16 17:29:06.159423+00	2025-10-16 17:29:06.159425+00	43
264	f	\N	1969	Асель-2017	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.159884+00	2025-10-16 17:29:06.160159+00	2025-10-16 17:29:06.160161+00	115
265	f	\N	1968	Шанс	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.160608+00	2025-10-16 17:29:06.160902+00	2025-10-16 17:29:06.160904+00	20
266	f	\N	1967	Янтарная 150	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.161389+00	2025-10-16 17:29:06.161682+00	2025-10-16 17:29:06.161684+00	123
267	f	\N	1966	Анель 16	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.162172+00	2025-10-16 17:29:06.162445+00	2025-10-16 17:29:06.162447+00	71
268	f	\N	1965	Семеновна	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.163016+00	2025-10-16 17:29:06.163277+00	2025-10-16 17:29:06.163279+00	71
269	f	\N	1964	Карагандинская 31	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.163752+00	2025-10-16 17:29:06.164014+00	2025-10-16 17:29:06.164016+00	71
270	f	\N	1963	Таймас	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.164459+00	2025-10-16 17:29:06.164718+00	2025-10-16 17:29:06.16472+00	71
271	f	\N	1962	п/с к Омский 100	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.165418+00	2025-10-16 17:29:06.165689+00	2025-10-16 17:29:06.165692+00	149
272	f	\N	1961	Ясенка	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.166329+00	2025-10-16 17:29:06.166701+00	2025-10-16 17:29:06.166703+00	123
273	f	\N	1960	п/с к Омский лазурит	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.167459+00	2025-10-16 17:29:06.167803+00	2025-10-16 17:29:06.167805+00	123
274	f	\N	1959	Алуа	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.168318+00	2025-10-16 17:29:06.1686+00	2025-10-16 17:29:06.168602+00	16
275	f	\N	1958	Алмалык-85	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.169066+00	2025-10-16 17:29:06.169327+00	2025-10-16 17:29:06.169329+00	146
276	f	\N	1957	Примино	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.169773+00	2025-10-16 17:29:06.170035+00	2025-10-16 17:29:06.170037+00	54
277	f	\N	1956	п/с к сорту Вектор	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.170513+00	2025-10-16 17:29:06.170812+00	2025-10-16 17:29:06.170815+00	71
278	f	\N	1955	Курьер	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.171258+00	2025-10-16 17:29:06.171492+00	2025-10-16 17:29:06.171494+00	71
279	f	\N	1954	Курьер	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.171924+00	2025-10-16 17:29:06.172163+00	2025-10-16 17:29:06.172165+00	71
280	f	\N	1953	Дән	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.172621+00	2025-10-16 17:29:06.172872+00	2025-10-16 17:29:06.172874+00	71
281	f	\N	1952	Керемет	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.173357+00	2025-10-16 17:29:06.173619+00	2025-10-16 17:29:06.173622+00	71
282	f	\N	1951	Пироль/Pirol	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.174116+00	2025-10-16 17:29:06.174492+00	2025-10-16 17:29:06.174494+00	97
283	f	\N	1950	Тенгри	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.175247+00	2025-10-16 17:29:06.17566+00	2025-10-16 17:29:06.175663+00	97
284	f	\N	1949	Кемель	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.176292+00	2025-10-16 17:29:06.176571+00	2025-10-16 17:29:06.176573+00	148
285	f	\N	1948	Гүлім	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.177094+00	2025-10-16 17:29:06.177346+00	2025-10-16 17:29:06.177348+00	88
286	f	\N	1947	Никотер (Nicoter)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.177806+00	2025-10-16 17:29:06.178058+00	2025-10-16 17:29:06.17806+00	148
287	f	\N	1946	Никогрин (Nicogreen)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.178493+00	2025-10-16 17:29:06.178782+00	2025-10-16 17:29:06.178784+00	148
288	f	\N	1945	Казахстанский 435 СВ	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.179254+00	2025-10-16 17:29:06.179504+00	2025-10-16 17:29:06.179506+00	54
289	f	\N	1944	Туран 680 СВ	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.179927+00	2025-10-16 17:29:06.180168+00	2025-10-16 17:29:06.18017+00	54
290	f	\N	1943	Будан 237 МВ	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.180645+00	2025-10-16 17:29:06.180907+00	2025-10-16 17:29:06.18091+00	54
291	f	\N	1942	Казахстанский 705 СВ	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.181353+00	2025-10-16 17:29:06.181618+00	2025-10-16 17:29:06.181622+00	54
292	f	\N	1941	Казахстанский 700 СВ	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.18205+00	2025-10-16 17:29:06.182289+00	2025-10-16 17:29:06.182292+00	54
293	f	\N	1940	Казахстанский 420 СВ	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.182989+00	2025-10-16 17:29:06.183352+00	2025-10-16 17:29:06.183355+00	54
294	f	\N	1939	Туран 559 СВ	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.184121+00	2025-10-16 17:29:06.184433+00	2025-10-16 17:29:06.184435+00	54
295	f	\N	1938	Сары-Арка 150 СВ	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.184989+00	2025-10-16 17:29:06.185308+00	2025-10-16 17:29:06.185311+00	54
296	f	\N	1937	Казахстанский-341	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.185846+00	2025-10-16 17:29:06.186099+00	2025-10-16 17:29:06.186101+00	89
297	f	\N	1936	Сункар	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.186541+00	2025-10-16 17:29:06.186829+00	2025-10-16 17:29:06.186832+00	89
298	f	\N	1935	Восточный	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.187305+00	2025-10-16 17:29:06.187544+00	2025-10-16 17:29:06.187547+00	89
299	f	\N	1934	Солнечный-20	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.187986+00	2025-10-16 17:29:06.188222+00	2025-10-16 17:29:06.188224+00	89
300	f	\N	1933	Казахстанский-465	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.188656+00	2025-10-16 17:29:06.188897+00	2025-10-16 17:29:06.188899+00	89
301	f	\N	1932	Казахстанский-1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.189321+00	2025-10-16 17:29:06.189584+00	2025-10-16 17:29:06.189586+00	89
302	f	\N	1931	Лютесценс 32	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.190042+00	2025-10-16 17:29:06.190301+00	2025-10-16 17:29:06.190304+00	1
303	f	\N	1930	Казахстанская 19	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.190821+00	2025-10-16 17:29:06.191179+00	2025-10-16 17:29:06.191181+00	1
304	f	\N	1929	Казахстаский 70	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.191807+00	2025-10-16 17:29:06.192255+00	2025-10-16 17:29:06.192258+00	77
305	f	\N	1928	Казахстанская 15	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.193171+00	2025-10-16 17:29:06.193464+00	2025-10-16 17:29:06.193466+00	1
306	f	\N	1927	Лютесценс 90	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.193967+00	2025-10-16 17:29:06.194232+00	2025-10-16 17:29:06.194234+00	1
307	f	\N	1925	Сильфид (Sylphide)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.195316+00	2025-10-16 17:29:06.195562+00	2025-10-16 17:29:06.195564+00	149
308	f	\N	1924	Жулдыз	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.196014+00	2025-10-16 17:29:06.196249+00	2025-10-16 17:29:06.196251+00	149
309	f	\N	1923	Сауле	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.196871+00	2025-10-16 17:29:06.197108+00	2025-10-16 17:29:06.19711+00	149
310	f	\N	1922	Северь-1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.197537+00	2025-10-16 17:29:06.197781+00	2025-10-16 17:29:06.197783+00	149
311	f	\N	1921	Асем	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.198223+00	2025-10-16 17:29:06.198472+00	2025-10-16 17:29:06.198474+00	149
312	f	\N	1920	Арна	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.199118+00	2025-10-16 17:29:06.199464+00	2025-10-16 17:29:06.199466+00	149
313	f	\N	1919	Туран-2	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.200174+00	2025-10-16 17:29:06.200749+00	2025-10-16 17:29:06.200753+00	149
314	f	\N	1918	Байлык	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.201482+00	2025-10-16 17:29:06.201824+00	2025-10-16 17:29:06.201826+00	114
315	f	\N	1917	Ансар	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.202298+00	2025-10-16 17:29:06.202562+00	2025-10-16 17:29:06.202565+00	114
316	f	\N	1916	П63ЛЕ166	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.203034+00	2025-10-16 17:29:06.203305+00	2025-10-16 17:29:06.203307+00	88
317	f	\N	1915	П64ЛП130	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.203741+00	2025-10-16 17:29:06.203976+00	2025-10-16 17:29:06.203978+00	88
318	f	\N	1914	ЛГ 50480	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.204438+00	2025-10-16 17:29:06.204707+00	2025-10-16 17:29:06.204709+00	88
319	f	\N	1913	ЛГ 50450	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.205145+00	2025-10-16 17:29:06.20544+00	2025-10-16 17:29:06.205443+00	88
320	f	\N	1912	ЛГ 50479 СХ	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.205901+00	2025-10-16 17:29:06.20617+00	2025-10-16 17:29:06.206172+00	88
321	f	\N	1911	ЛГ 50635 КЛП	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.206633+00	2025-10-16 17:29:06.207048+00	2025-10-16 17:29:06.20705+00	88
322	f	\N	1910	ЛГ 50541 КЛП	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.207717+00	2025-10-16 17:29:06.208107+00	2025-10-16 17:29:06.208111+00	88
323	f	\N	1909	Махаон КЛП	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.208888+00	2025-10-16 17:29:06.209178+00	2025-10-16 17:29:06.209181+00	88
324	f	\N	1908	Агробизнес 2050	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.209661+00	2025-10-16 17:29:06.209903+00	2025-10-16 17:29:06.209905+00	88
325	f	\N	1907	VR 808	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.210342+00	2025-10-16 17:29:06.210623+00	2025-10-16 17:29:06.210626+00	43
326	f	\N	1906	п/с SHC 909	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.21109+00	2025-10-16 17:29:06.211357+00	2025-10-16 17:29:06.21136+00	43
327	f	\N	1905	SHC 909	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.2118+00	2025-10-16 17:29:06.212044+00	2025-10-16 17:29:06.212047+00	43
328	f	\N	1904	VR 808	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.212515+00	2025-10-16 17:29:06.212783+00	2025-10-16 17:29:06.212786+00	43
329	f	\N	1903	п/с Маргрет	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.213235+00	2025-10-16 17:29:06.21351+00	2025-10-16 17:29:06.213512+00	149
330	f	\N	1902	п/с Маргрет	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.214016+00	2025-10-16 17:29:06.214288+00	2025-10-16 17:29:06.21429+00	149
331	f	\N	1901	Тася	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.21477+00	2025-10-16 17:29:06.215044+00	2025-10-16 17:29:06.215046+00	149
332	f	\N	1900	Целинный голозерный	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.215491+00	2025-10-16 17:29:06.215797+00	2025-10-16 17:29:06.215799+00	149
333	f	\N	1899	п/с Безенчукская Нива	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.216652+00	2025-10-16 17:29:06.21718+00	2025-10-16 17:29:06.217185+00	123
334	f	\N	1898	п/с Безенчукская 210	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.217935+00	2025-10-16 17:29:06.218279+00	2025-10-16 17:29:06.218282+00	123
335	f	\N	1897	п/с Тризо	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.218799+00	2025-10-16 17:29:06.219054+00	2025-10-16 17:29:06.219056+00	71
336	f	\N	1896	п/с Тризо	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.219501+00	2025-10-16 17:29:06.219797+00	2025-10-16 17:29:06.219799+00	71
337	f	\N	1895	п/с Тризо	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.220264+00	2025-10-16 17:29:06.220503+00	2025-10-16 17:29:06.220505+00	71
338	f	\N	1894	Людмила	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.22095+00	2025-10-16 17:29:06.221205+00	2025-10-16 17:29:06.221207+00	16
339	f	\N	1893	Кунсулу	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.221654+00	2025-10-16 17:29:06.221915+00	2025-10-16 17:29:06.221917+00	16
340	f	\N	1892	Ляззат	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.222364+00	2025-10-16 17:29:06.222604+00	2025-10-16 17:29:06.222606+00	136
341	f	\N	1891	Тайпакский	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.223108+00	2025-10-16 17:29:06.223375+00	2025-10-16 17:29:06.223377+00	36
342	f	\N	1890	Уральский узкоколосый	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.223871+00	2025-10-16 17:29:06.224188+00	2025-10-16 17:29:06.22419+00	36
343	f	\N	1889	Ема	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.224925+00	2025-10-16 17:29:06.225366+00	2025-10-16 17:29:06.225369+00	123
344	f	\N	1888	Алтын шыгыс	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.226069+00	2025-10-16 17:29:06.226377+00	2025-10-16 17:29:06.22638+00	123
345	f	\N	1887	Карабалыкская озимая	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.226942+00	2025-10-16 17:29:06.227206+00	2025-10-16 17:29:06.227209+00	1
346	f	\N	1886	Костанайская 10	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.227741+00	2025-10-16 17:29:06.22801+00	2025-10-16 17:29:06.228012+00	123
347	f	\N	1885	Маржан	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.228677+00	2025-10-16 17:29:06.228937+00	2025-10-16 17:29:06.228939+00	16
348	f	\N	1884	Жедель	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.229412+00	2025-10-16 17:29:06.229678+00	2025-10-16 17:29:06.22968+00	18
349	f	\N	1883	Айгерим	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.230145+00	2025-10-16 17:29:06.230385+00	2025-10-16 17:29:06.230387+00	136
350	f	\N	1882	Центр-70	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.230857+00	2025-10-16 17:29:06.231125+00	2025-10-16 17:29:06.231127+00	106
351	f	\N	1881	Казар	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.231594+00	2025-10-16 17:29:06.232255+00	2025-10-16 17:29:06.232258+00	55
352	f	\N	1880	Дуняша	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.233011+00	2025-10-16 17:29:06.233422+00	2025-10-16 17:29:06.233425+00	44
353	f	\N	1879	Костанайские новости	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.234022+00	2025-10-16 17:29:06.234324+00	2025-10-16 17:29:06.234327+00	44
354	f	\N	1878	Алмалы	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.23481+00	2025-10-16 17:29:06.235079+00	2025-10-16 17:29:06.235081+00	1
355	f	\N	1877	Наз	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.235533+00	2025-10-16 17:29:06.235842+00	2025-10-16 17:29:06.235845+00	1
356	f	\N	1876	Эритроспермум 350	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.236326+00	2025-10-16 17:29:06.236577+00	2025-10-16 17:29:06.236579+00	1
357	f	\N	1875	Жетысу	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.237067+00	2025-10-16 17:29:06.237309+00	2025-10-16 17:29:06.237311+00	1
358	f	\N	1874	Богарная 56	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.237771+00	2025-10-16 17:29:06.238015+00	2025-10-16 17:29:06.238017+00	1
359	f	\N	1873	Эврика 357	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.238471+00	2025-10-16 17:29:06.238737+00	2025-10-16 17:29:06.238739+00	120
360	f	\N	1872	Казахстанская 2309	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.239197+00	2025-10-16 17:29:06.239444+00	2025-10-16 17:29:06.239446+00	120
361	f	\N	1871	Казахстанская 2309	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.239944+00	2025-10-16 17:29:06.240196+00	2025-10-16 17:29:06.240199+00	120
362	f	\N	1870	Жалпаксай	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.240666+00	2025-10-16 17:29:06.241022+00	2025-10-16 17:29:06.241025+00	120
363	f	\N	1869	Мисула 1092	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.241601+00	2025-10-16 17:29:06.242016+00	2025-10-16 17:29:06.24202+00	120
364	f	\N	1868	Стекловидная-24	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.242758+00	2025-10-16 17:29:06.243074+00	2025-10-16 17:29:06.243076+00	1
365	f	\N	1867	Сапалы	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.243553+00	2025-10-16 17:29:06.243847+00	2025-10-16 17:29:06.243849+00	1
366	f	\N	1866	Целинный 160 МВ	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.244374+00	2025-10-16 17:29:06.244644+00	2025-10-16 17:29:06.244647+00	54
367	f	\N	1865	Казахстанский 587 СВ	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.245085+00	2025-10-16 17:29:06.245361+00	2025-10-16 17:29:06.245363+00	54
368	f	\N	1864	Тургайская 5/87	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.24586+00	2025-10-16 17:29:06.246115+00	2025-10-16 17:29:06.246118+00	54
369	f	\N	1863	Ливиус (LIVIUS)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.246589+00	2025-10-16 17:29:06.246876+00	2025-10-16 17:29:06.246878+00	97
370	f	\N	1862	Абилити (ABILITI)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.247365+00	2025-10-16 17:29:06.247649+00	2025-10-16 17:29:06.247651+00	97
371	f	\N	1861	Актер	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.248145+00	2025-10-16 17:29:06.248422+00	2025-10-16 17:29:06.248424+00	1
372	f	\N	1860	Карабалыкский 7	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.248944+00	2025-10-16 17:29:06.249306+00	2025-10-16 17:29:06.249309+00	55
373	f	\N	1859	Кустанайский янтарь	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.249939+00	2025-10-16 17:29:06.250505+00	2025-10-16 17:29:06.250508+00	55
374	f	\N	1858	Шортандинская 2	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.25119+00	2025-10-16 17:29:06.251489+00	2025-10-16 17:29:06.251491+00	27
375	f	\N	1857	Кормовое 98	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.251983+00	2025-10-16 17:29:06.25223+00	2025-10-16 17:29:06.252232+00	90
376	f	\N	1856	Кормовое 89	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.252727+00	2025-10-16 17:29:06.252973+00	2025-10-16 17:29:06.252975+00	90
377	f	\N	1855	Шортандинское 7	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.253429+00	2025-10-16 17:29:06.253683+00	2025-10-16 17:29:06.253686+00	90
378	f	\N	1854	Целинный 91	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.25415+00	2025-10-16 17:29:06.254395+00	2025-10-16 17:29:06.254397+00	149
379	f	\N	1853	Астана 2000	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.254862+00	2025-10-16 17:29:06.255108+00	2025-10-16 17:29:06.25511+00	149
380	f	\N	1852	Целинная 24	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.255558+00	2025-10-16 17:29:06.25584+00	2025-10-16 17:29:06.255842+00	1
381	f	\N	1851	Цединная 3 С	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.256319+00	2025-10-16 17:29:06.256669+00	2025-10-16 17:29:06.256672+00	1
382	f	\N	1850	Астана	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.25728+00	2025-10-16 17:29:06.257637+00	2025-10-16 17:29:06.257639+00	1
383	f	\N	1849	Акмола 2	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.25832+00	2025-10-16 17:29:06.258606+00	2025-10-16 17:29:06.258609+00	1
384	f	\N	1848	Шортандинская 95 улучшенная	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.259139+00	2025-10-16 17:29:06.259408+00	2025-10-16 17:29:06.25941+00	1
385	f	\N	1847	Гордеиформе 254	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.260047+00	2025-10-16 17:29:06.260294+00	2025-10-16 17:29:06.260296+00	123
386	f	\N	1846	Сид-88	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.260759+00	2025-10-16 17:29:06.261026+00	2025-10-16 17:29:06.261028+00	123
387	f	\N	1845	Эритроспермум 35	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.261451+00	2025-10-16 17:29:06.261716+00	2025-10-16 17:29:06.261718+00	1
388	f	\N	1844	Карабалыкская 92	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.262145+00	2025-10-16 17:29:06.26238+00	2025-10-16 17:29:06.262383+00	1
389	f	\N	1843	Карабалыкская 7	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.262807+00	2025-10-16 17:29:06.263075+00	2025-10-16 17:29:06.263077+00	1
390	f	\N	1842	Костанайская 12	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.263526+00	2025-10-16 17:29:06.263805+00	2025-10-16 17:29:06.263807+00	123
391	f	\N	1841	Шортандинская крупнозерная	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.264281+00	2025-10-16 17:29:06.264551+00	2025-10-16 17:29:06.264553+00	27
392	f	\N	1840	Битик	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.264997+00	2025-10-16 17:29:06.265239+00	2025-10-16 17:29:06.265241+00	77
393	f	\N	1839	Карабалыкская 90	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.265696+00	2025-10-16 17:29:06.266066+00	2025-10-16 17:29:06.266068+00	1
394	f	\N	1838	Гранал	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.266656+00	2025-10-16 17:29:06.266987+00	2025-10-16 17:29:06.266989+00	149
395	f	\N	1837	Убаган	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.267735+00	2025-10-16 17:29:06.268043+00	2025-10-16 17:29:06.268046+00	149
396	f	\N	1836	Костанайская 52	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.268562+00	2025-10-16 17:29:06.268844+00	2025-10-16 17:29:06.268847+00	123
397	f	\N	1835	Карабалыкский 110	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.269285+00	2025-10-16 17:29:06.269522+00	2025-10-16 17:29:06.269524+00	149
398	f	\N	1834	Медикум 85	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.269961+00	2025-10-16 17:29:06.270212+00	2025-10-16 17:29:06.270215+00	149
399	f	\N	1833	Дружный	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.270698+00	2025-10-16 17:29:06.270973+00	2025-10-16 17:29:06.270975+00	149
400	f	\N	1832	Карабалыкский 150	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.271441+00	2025-10-16 17:29:06.271783+00	2025-10-16 17:29:06.271785+00	149
401	f	\N	1831	Райхан	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.272278+00	2025-10-16 17:29:06.272525+00	2025-10-16 17:29:06.272527+00	61
402	f	\N	1830	Шортандинский 83	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.273027+00	2025-10-16 17:29:06.273326+00	2025-10-16 17:29:06.273328+00	144
403	f	\N	1829	Сарбас	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.273807+00	2025-10-16 17:29:06.274131+00	2025-10-16 17:29:06.274134+00	31
404	f	\N	1828	Акмолинский 91	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.274801+00	2025-10-16 17:29:06.275138+00	2025-10-16 17:29:06.27514+00	50
405	f	\N	1827	Сыр аруы	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.275994+00	2025-10-16 17:29:06.276332+00	2025-10-16 17:29:06.276335+00	149
406	f	\N	1826	Тогускен 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.276897+00	2025-10-16 17:29:06.277183+00	2025-10-16 17:29:06.277186+00	102
407	f	\N	1825	Арал 202	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.277667+00	2025-10-16 17:29:06.277906+00	2025-10-16 17:29:06.277908+00	102
408	f	\N	1824	Алмакен	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.278335+00	2025-10-16 17:29:06.278599+00	2025-10-16 17:29:06.278601+00	1
409	f	\N	1823	Алтын дала	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.279242+00	2025-10-16 17:29:06.279486+00	2025-10-16 17:29:06.279488+00	123
410	f	\N	1822	Рикотензе 2006	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.279932+00	2025-10-16 17:29:06.280172+00	2025-10-16 17:29:06.280174+00	149
411	f	\N	1821	Томирис	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.280595+00	2025-10-16 17:29:06.280836+00	2025-10-16 17:29:06.280838+00	1
412	f	\N	1820	Карагандинская 22	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.281267+00	2025-10-16 17:29:06.281508+00	2025-10-16 17:29:06.28151+00	1
413	f	\N	1819	Карагандинская 70	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.28193+00	2025-10-16 17:29:06.282201+00	2025-10-16 17:29:06.282203+00	1
414	f	\N	1818	Карагандинский 5	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.282802+00	2025-10-16 17:29:06.283111+00	2025-10-16 17:29:06.283114+00	149
415	f	\N	1817	Дарья	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.28386+00	2025-10-16 17:29:06.284226+00	2025-10-16 17:29:06.284228+00	108
416	f	\N	1816	Краюшка	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.284804+00	2025-10-16 17:29:06.285095+00	2025-10-16 17:29:06.285097+00	71
417	f	\N	1815	Рассвет	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.285572+00	2025-10-16 17:29:06.28586+00	2025-10-16 17:29:06.285863+00	126
418	f	\N	1814	Лучезарный	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.286489+00	2025-10-16 17:29:06.286757+00	2025-10-16 17:29:06.286759+00	126
419	f	\N	1813	Шугыла	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.287202+00	2025-10-16 17:29:06.287464+00	2025-10-16 17:29:06.287466+00	32
420	f	\N	1812	Азат	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.287902+00	2025-10-16 17:29:06.288146+00	2025-10-16 17:29:06.288148+00	79
421	f	\N	1811	Шильде	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.288565+00	2025-10-16 17:29:06.288834+00	2025-10-16 17:29:06.288836+00	79
422	f	\N	1810	Августин	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.289254+00	2025-10-16 17:29:06.289486+00	2025-10-16 17:29:06.289488+00	60
423	f	\N	1809	Сокол	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.289956+00	2025-10-16 17:29:06.290388+00	2025-10-16 17:29:06.29039+00	60
424	f	\N	1808	Табыс	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.291155+00	2025-10-16 17:29:06.291541+00	2025-10-16 17:29:06.291544+00	60
425	f	\N	1807	Акмолинская нива	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.292468+00	2025-10-16 17:29:06.292786+00	2025-10-16 17:29:06.292788+00	1
426	f	\N	1806	Шуакты	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.293304+00	2025-10-16 17:29:06.293544+00	2025-10-16 17:29:06.293546+00	88
427	f	\N	1805	Шортандинская 2007	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.29405+00	2025-10-16 17:29:06.294312+00	2025-10-16 17:29:06.294314+00	1
428	f	\N	1804	Астана 2007	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.294791+00	2025-10-16 17:29:06.295055+00	2025-10-16 17:29:06.295057+00	149
429	f	\N	1803	Виола	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.295499+00	2025-10-16 17:29:06.295769+00	2025-10-16 17:29:06.295771+00	61
430	f	\N	1802	Барс	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.296207+00	2025-10-16 17:29:06.29644+00	2025-10-16 17:29:06.296442+00	31
431	f	\N	1801	Шортандинский пастбищный	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.296857+00	2025-10-16 17:29:06.297122+00	2025-10-16 17:29:06.297124+00	57
432	f	\N	1800	Надежда	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.29757+00	2025-10-16 17:29:06.297847+00	2025-10-16 17:29:06.297849+00	120
433	f	\N	1799	Тажан	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.298283+00	2025-10-16 17:29:06.298539+00	2025-10-16 17:29:06.298541+00	120
434	f	\N	1798	Алматы	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.298961+00	2025-10-16 17:29:06.299312+00	2025-10-16 17:29:06.299314+00	120
435	f	\N	1797	Красноводопадская поливная	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.299885+00	2025-10-16 17:29:06.300194+00	2025-10-16 17:29:06.300196+00	61
436	f	\N	1796	Красноводопадская скороспелая	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.301237+00	2025-10-16 17:29:06.301838+00	2025-10-16 17:29:06.301841+00	61
437	f	\N	1795	Байшешек	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.302683+00	2025-10-16 17:29:06.303033+00	2025-10-16 17:29:06.303036+00	149
438	f	\N	1794	Вита	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.30352+00	2025-10-16 17:29:06.303804+00	2025-10-16 17:29:06.303806+00	120
439	f	\N	1793	Нина	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.304242+00	2025-10-16 17:29:06.304517+00	2025-10-16 17:29:06.304519+00	120
440	f	\N	1792	Радость	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.304957+00	2025-10-16 17:29:06.305205+00	2025-10-16 17:29:06.305207+00	120
441	f	\N	1791	Аламан	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.305644+00	2025-10-16 17:29:06.30591+00	2025-10-16 17:29:06.305912+00	77
442	f	\N	1790	Жорға	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.306409+00	2025-10-16 17:29:06.306683+00	2025-10-16 17:29:06.306685+00	77
443	f	\N	1789	Кулагер	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.30711+00	2025-10-16 17:29:06.307386+00	2025-10-16 17:29:06.307388+00	77
444	f	\N	1788	Самгау	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.308101+00	2025-10-16 17:29:06.308576+00	2025-10-16 17:29:06.308579+00	1
445	f	\N	1787	Сусын	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.309325+00	2025-10-16 17:29:06.309668+00	2025-10-16 17:29:06.309671+00	149
446	f	\N	1786	Жан	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.310246+00	2025-10-16 17:29:06.310535+00	2025-10-16 17:29:06.310537+00	149
447	f	\N	1785	Илек-9	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.311079+00	2025-10-16 17:29:06.311327+00	2025-10-16 17:29:06.311329+00	149
448	f	\N	1784	Куралай	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.311787+00	2025-10-16 17:29:06.312058+00	2025-10-16 17:29:06.31206+00	149
449	f	\N	1783	Елік	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.312523+00	2025-10-16 17:29:06.312783+00	2025-10-16 17:29:06.312785+00	149
450	f	\N	1782	Қымбат	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.31341+00	2025-10-16 17:29:06.313657+00	2025-10-16 17:29:06.313659+00	149
451	f	\N	1781	Сымбат	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.314118+00	2025-10-16 17:29:06.314361+00	2025-10-16 17:29:06.314364+00	149
452	f	\N	1780	Өсімтал	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.314791+00	2025-10-16 17:29:06.315033+00	2025-10-16 17:29:06.315036+00	61
453	f	\N	1779	Жамиля	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.315472+00	2025-10-16 17:29:06.315822+00	2025-10-16 17:29:06.315825+00	24
454	f	\N	1778	Целинная 2007	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.316467+00	2025-10-16 17:29:06.316841+00	2025-10-16 17:29:06.316843+00	1
455	f	\N	1777	Целиноградский юбилейный	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.317583+00	2025-10-16 17:29:06.317883+00	2025-10-16 17:29:06.317885+00	50
456	f	\N	1776	Секе	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.31838+00	2025-10-16 17:29:06.318688+00	2025-10-16 17:29:06.31869+00	1
457	f	\N	1775	Павлодарское	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.319205+00	2025-10-16 17:29:06.319494+00	2025-10-16 17:29:06.319496+00	90
458	f	\N	1774	Приаральский-19	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.319989+00	2025-10-16 17:29:06.320239+00	2025-10-16 17:29:06.320242+00	31
459	f	\N	1773	Вид-1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.32068+00	2025-10-16 17:29:06.320943+00	2025-10-16 17:29:06.320945+00	44
460	f	\N	1772	Вид-2	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.321365+00	2025-10-16 17:29:06.321597+00	2025-10-16 17:29:06.321599+00	44
461	f	\N	1771	Тулпар	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.322065+00	2025-10-16 17:29:06.322306+00	2025-10-16 17:29:06.322308+00	149
462	f	\N	1770	Нутанс 39	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.322792+00	2025-10-16 17:29:06.32307+00	2025-10-16 17:29:06.323072+00	149
463	f	\N	1769	Жазира	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.323574+00	2025-10-16 17:29:06.323873+00	2025-10-16 17:29:06.323875+00	1
464	f	\N	1768	Карабалыкский рубиновый	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.324502+00	2025-10-16 17:29:06.324831+00	2025-10-16 17:29:06.324834+00	144
465	f	\N	1767	Карабалыкский юбилейный-75	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.32552+00	2025-10-16 17:29:06.325905+00	2025-10-16 17:29:06.325907+00	144
466	f	\N	1766	Карабалыкская жемчужина	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.326406+00	2025-10-16 17:29:06.326703+00	2025-10-16 17:29:06.326706+00	61
467	f	\N	1765	Юбилейная 90	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.327212+00	2025-10-16 17:29:06.32745+00	2025-10-16 17:29:06.327452+00	61
468	f	\N	1764	Карабалыкская радуга	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.327939+00	2025-10-16 17:29:06.328218+00	2025-10-16 17:29:06.32822+00	61
469	f	\N	1763	Карабалыкская 101	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.328672+00	2025-10-16 17:29:06.328917+00	2025-10-16 17:29:06.32892+00	1
470	f	\N	1762	Ягодный-19	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.329408+00	2025-10-16 17:29:06.329672+00	2025-10-16 17:29:06.329675+00	43
471	f	\N	1761	Ертіс 7	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.330179+00	2025-10-16 17:29:06.330422+00	2025-10-16 17:29:06.330424+00	1
472	f	\N	1760	Туркестан-15	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.330883+00	2025-10-16 17:29:06.331151+00	2025-10-16 17:29:06.331153+00	61
473	f	\N	1759	Лазурная	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.331629+00	2025-10-16 17:29:06.331966+00	2025-10-16 17:29:06.331968+00	61
474	f	\N	1758	Майбұлақ	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.332424+00	2025-10-16 17:29:06.332792+00	2025-10-16 17:29:06.332794+00	97
475	f	\N	1757	Уральская синяя	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.333589+00	2025-10-16 17:29:06.333966+00	2025-10-16 17:29:06.333968+00	61
476	f	\N	1756	Марэль	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.334553+00	2025-10-16 17:29:06.334849+00	2025-10-16 17:29:06.334852+00	96
477	f	\N	1755	Шал	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.335355+00	2025-10-16 17:29:06.335642+00	2025-10-16 17:29:06.335645+00	20
478	f	\N	1754	Усач Казахстанский	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.33609+00	2025-10-16 17:29:06.336334+00	2025-10-16 17:29:06.336336+00	20
479	f	\N	1753	Камила	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.336808+00	2025-10-16 17:29:06.337054+00	2025-10-16 17:29:06.337057+00	74
480	f	\N	1752	Казахстанская 10	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.337517+00	2025-10-16 17:29:06.337788+00	2025-10-16 17:29:06.337791+00	1
481	f	\N	1751	Казахстанская раннеспелая	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.338221+00	2025-10-16 17:29:06.338455+00	2025-10-16 17:29:06.338457+00	1
482	f	\N	1750	Казахстанская 25	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.338879+00	2025-10-16 17:29:06.339124+00	2025-10-16 17:29:06.339126+00	1
483	f	\N	1749	Ласточка	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.339575+00	2025-10-16 17:29:06.339871+00	2025-10-16 17:29:06.339873+00	120
484	f	\N	1748	Кайыр	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.340316+00	2025-10-16 17:29:06.340551+00	2025-10-16 17:29:06.340553+00	1
485	f	\N	1747	Табыз	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.34112+00	2025-10-16 17:29:06.341435+00	2025-10-16 17:29:06.341437+00	20
486	f	\N	1746	Қазақстан-16	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.342406+00	2025-10-16 17:29:06.342773+00	2025-10-16 17:29:06.342775+00	1
487	f	\N	1745	Алатау	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.343321+00	2025-10-16 17:29:06.343599+00	2025-10-16 17:29:06.343601+00	1
488	f	\N	1744	Риза	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.344129+00	2025-10-16 17:29:06.344402+00	2025-10-16 17:29:06.344405+00	120
489	f	\N	1743	Камила 1255	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.344854+00	2025-10-16 17:29:06.345098+00	2025-10-16 17:29:06.345101+00	74
490	f	\N	1742	Камила 1255	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.345537+00	2025-10-16 17:29:06.345808+00	2025-10-16 17:29:06.34581+00	74
491	f	\N	1741	Актюбе 39	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.346236+00	2025-10-16 17:29:06.34647+00	2025-10-16 17:29:06.346472+00	71
492	f	\N	1740	Степная 2	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.346888+00	2025-10-16 17:29:06.347121+00	2025-10-16 17:29:06.347123+00	71
493	f	\N	1739	Степная 50	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.347541+00	2025-10-16 17:29:06.347836+00	2025-10-16 17:29:06.347838+00	71
494	f	\N	1738	Степная 60	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.348279+00	2025-10-16 17:29:06.348513+00	2025-10-16 17:29:06.348515+00	71
495	f	\N	1737	Степная 62	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.348945+00	2025-10-16 17:29:06.34935+00	2025-10-16 17:29:06.349353+00	71
496	f	\N	1736	Каргала 9	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.34992+00	2025-10-16 17:29:06.350239+00	2025-10-16 17:29:06.350241+00	123
497	f	\N	1735	Каргала 69	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.350974+00	2025-10-16 17:29:06.351271+00	2025-10-16 17:29:06.351273+00	123
498	f	\N	1734	Каргала 34	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.351771+00	2025-10-16 17:29:06.35204+00	2025-10-16 17:29:06.352042+00	123
499	f	\N	1733	Илек 16	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.352502+00	2025-10-16 17:29:06.352787+00	2025-10-16 17:29:06.352789+00	149
500	f	\N	1732	Илек 34	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.353224+00	2025-10-16 17:29:06.353459+00	2025-10-16 17:29:06.353461+00	149
577	f	\N	1655	Олимп	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.415604+00	2025-10-16 17:29:06.415947+00	2025-10-16 17:29:06.415949+00	60
501	f	\N	1731	Памяти Берсиева	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.353885+00	2025-10-16 17:29:06.354149+00	2025-10-16 17:29:06.354151+00	90
502	f	\N	1730	Яркое 3	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.354599+00	2025-10-16 17:29:06.354878+00	2025-10-16 17:29:06.35488+00	90
503	f	\N	1729	Ирсо	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.355327+00	2025-10-16 17:29:06.35559+00	2025-10-16 17:29:06.355592+00	88
504	f	\N	1728	Славячил	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.356086+00	2025-10-16 17:29:06.356337+00	2025-10-16 17:29:06.35634+00	55
505	f	\N	1727	Алая заря	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.356816+00	2025-10-16 17:29:06.357055+00	2025-10-16 17:29:06.357057+00	43
506	f	\N	1726	Заречный	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.357646+00	2025-10-16 17:29:06.357952+00	2025-10-16 17:29:06.357954+00	88
507	f	\N	1725	Павлодарская 93	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.358569+00	2025-10-16 17:29:06.359204+00	2025-10-16 17:29:06.359206+00	71
508	f	\N	1724	Ертіс 97	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.35981+00	2025-10-16 17:29:06.360082+00	2025-10-16 17:29:06.360084+00	71
509	f	\N	1723	Шортандинская 3	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.360579+00	2025-10-16 17:29:06.36087+00	2025-10-16 17:29:06.360873+00	27
510	f	\N	1722	Целина 50	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.361346+00	2025-10-16 17:29:06.361634+00	2025-10-16 17:29:06.361636+00	71
511	f	\N	1721	Асыл сапа	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.362088+00	2025-10-16 17:29:06.362332+00	2025-10-16 17:29:06.362334+00	71
512	f	\N	1720	Бурабай	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.362787+00	2025-10-16 17:29:06.363037+00	2025-10-16 17:29:06.363039+00	35
513	f	\N	1719	Шортандинский рубин	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.363454+00	2025-10-16 17:29:06.363737+00	2025-10-16 17:29:06.36374+00	144
514	f	\N	1718	Ишимский юбилейный	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.364181+00	2025-10-16 17:29:06.364474+00	2025-10-16 17:29:06.364477+00	50
515	f	\N	1717	Алау	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.364992+00	2025-10-16 17:29:06.365257+00	2025-10-16 17:29:06.36526+00	70
516	f	\N	1716	Пикант	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.365772+00	2025-10-16 17:29:06.36608+00	2025-10-16 17:29:06.366083+00	83
517	f	\N	1715	Ники	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.366852+00	2025-10-16 17:29:06.367278+00	2025-10-16 17:29:06.36728+00	139
518	f	\N	1714	Каз-Тай	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.368014+00	2025-10-16 17:29:06.368305+00	2025-10-16 17:29:06.368308+00	83
519	f	\N	1713	Баян-Сулу	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.368804+00	2025-10-16 17:29:06.369086+00	2025-10-16 17:29:06.369088+00	83
520	f	\N	1712	Айтугановка	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.369547+00	2025-10-16 17:29:06.369841+00	2025-10-16 17:29:06.369843+00	103
521	f	\N	1711	Заман	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.370294+00	2025-10-16 17:29:06.370568+00	2025-10-16 17:29:06.370571+00	148
522	f	\N	1710	SK-10194	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.371011+00	2025-10-16 17:29:06.37125+00	2025-10-16 17:29:06.371252+00	88
523	f	\N	1709	Карабалыкская 9	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.371698+00	2025-10-16 17:29:06.371982+00	2025-10-16 17:29:06.371984+00	71
524	f	\N	1708	Мерейтой-50	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.372481+00	2025-10-16 17:29:06.372799+00	2025-10-16 17:29:06.372802+00	16
525	f	\N	1707	Егемен	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.373514+00	2025-10-16 17:29:06.373784+00	2025-10-16 17:29:06.373786+00	146
526	f	\N	1706	Лидер	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.374389+00	2025-10-16 17:29:06.374712+00	2025-10-16 17:29:06.374715+00	126
527	f	\N	1705	Икарда 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.375527+00	2025-10-16 17:29:06.375919+00	2025-10-16 17:29:06.375921+00	74
528	f	\N	1704	Луч	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.376476+00	2025-10-16 17:29:06.376766+00	2025-10-16 17:29:06.376769+00	74
529	f	\N	1703	Наурыз 6	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.377268+00	2025-10-16 17:29:06.377552+00	2025-10-16 17:29:06.377554+00	123
530	f	\N	1702	Наурыз 2	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.378061+00	2025-10-16 17:29:06.37835+00	2025-10-16 17:29:06.378352+00	123
531	f	\N	1701	Ертол	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.378831+00	2025-10-16 17:29:06.379102+00	2025-10-16 17:29:06.379105+00	123
532	f	\N	1700	Лан	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.37957+00	2025-10-16 17:29:06.379867+00	2025-10-16 17:29:06.379869+00	123
533	f	\N	1699	Сафия	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.380326+00	2025-10-16 17:29:06.380566+00	2025-10-16 17:29:06.380568+00	97
534	f	\N	1698	Костанайский-11	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.381058+00	2025-10-16 17:29:06.381319+00	2025-10-16 17:29:06.381321+00	55
535	f	\N	1697	Тустеп	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.381766+00	2025-10-16 17:29:06.382001+00	2025-10-16 17:29:06.382003+00	43
536	f	\N	1696	Валерий	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.382474+00	2025-10-16 17:29:06.382902+00	2025-10-16 17:29:06.382904+00	43
537	f	\N	1695	Шортандинское 11	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.383538+00	2025-10-16 17:29:06.384055+00	2025-10-16 17:29:06.384058+00	90
538	f	\N	1694	Кормовое 2008	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.384762+00	2025-10-16 17:29:06.385079+00	2025-10-16 17:29:06.385081+00	90
539	f	\N	1693	Памяти Каскарбаева	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.385578+00	2025-10-16 17:29:06.385865+00	2025-10-16 17:29:06.385867+00	71
540	f	\N	1692	Абулхайыр	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.386368+00	2025-10-16 17:29:06.386634+00	2025-10-16 17:29:06.386637+00	109
541	f	\N	1691	Жадыра 21	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.387082+00	2025-10-16 17:29:06.387336+00	2025-10-16 17:29:06.387338+00	54
542	f	\N	1690	Маржан	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.387799+00	2025-10-16 17:29:06.388049+00	2025-10-16 17:29:06.388052+00	102
543	f	\N	1689	Аул	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.388483+00	2025-10-16 17:29:06.388726+00	2025-10-16 17:29:06.388728+00	43
544	f	\N	1688	Акколь	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.389215+00	2025-10-16 17:29:06.389509+00	2025-10-16 17:29:06.389511+00	43
545	f	\N	1687	Аксор	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.390011+00	2025-10-16 17:29:06.390363+00	2025-10-16 17:29:06.390365+00	43
546	f	\N	1686	Карасайский	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.391019+00	2025-10-16 17:29:06.391421+00	2025-10-16 17:29:06.391424+00	43
547	f	\N	1685	Тениз	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.392049+00	2025-10-16 17:29:06.392327+00	2025-10-16 17:29:06.39233+00	43
548	f	\N	1684	Тамаша	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.392803+00	2025-10-16 17:29:06.393059+00	2025-10-16 17:29:06.393062+00	43
549	f	\N	1683	Когалы	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.393501+00	2025-10-16 17:29:06.393779+00	2025-10-16 17:29:06.393782+00	43
550	f	\N	1682	Альянс	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.394261+00	2025-10-16 17:29:06.394549+00	2025-10-16 17:29:06.394551+00	43
551	f	\N	1681	Нэрли	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.395006+00	2025-10-16 17:29:06.395246+00	2025-10-16 17:29:06.395248+00	43
552	f	\N	1680	Жанайсан	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.395674+00	2025-10-16 17:29:06.395909+00	2025-10-16 17:29:06.395911+00	43
553	f	\N	1679	Памяти Боброва	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.396362+00	2025-10-16 17:29:06.396598+00	2025-10-16 17:29:06.3966+00	43
554	f	\N	1678	Валентина	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.397031+00	2025-10-16 17:29:06.397265+00	2025-10-16 17:29:06.397267+00	43
555	f	\N	1677	Мирас	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.397694+00	2025-10-16 17:29:06.397957+00	2025-10-16 17:29:06.39796+00	43
556	f	\N	1676	Балшекер 375 СВ	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.398378+00	2025-10-16 17:29:06.398633+00	2025-10-16 17:29:06.398636+00	54
557	f	\N	1675	Сыр-Сулуы 375 СВ	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.399076+00	2025-10-16 17:29:06.399541+00	2025-10-16 17:29:06.399543+00	54
558	f	\N	1674	Заман	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.400178+00	2025-10-16 17:29:06.400598+00	2025-10-16 17:29:06.400601+00	146
559	f	\N	1673	Акдидар	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.401188+00	2025-10-16 17:29:06.401465+00	2025-10-16 17:29:06.401467+00	16
560	f	\N	1672	Куралай	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.402021+00	2025-10-16 17:29:06.40228+00	2025-10-16 17:29:06.402282+00	16
561	f	\N	1671	Жаркын	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.402752+00	2025-10-16 17:29:06.40299+00	2025-10-16 17:29:06.402992+00	146
562	f	\N	1670	Руфина	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.403431+00	2025-10-16 17:29:06.403693+00	2025-10-16 17:29:06.403696+00	16
563	f	\N	1669	Бакытнур	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.404325+00	2025-10-16 17:29:06.404561+00	2025-10-16 17:29:06.404563+00	16
564	f	\N	1668	ҚЫЗЫЛЖАР 75 СВ	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.40498+00	2025-10-16 17:29:06.405222+00	2025-10-16 17:29:06.405224+00	54
565	f	\N	1667	Астана 10 СВ	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.405646+00	2025-10-16 17:29:06.405966+00	2025-10-16 17:29:06.405968+00	54
566	f	\N	1666	Нурлан	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.406452+00	2025-10-16 17:29:06.406735+00	2025-10-16 17:29:06.406737+00	106
567	f	\N	1665	Акмай	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.407186+00	2025-10-16 17:29:06.407488+00	2025-10-16 17:29:06.40749+00	106
568	f	\N	1664	Жаналык	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.408095+00	2025-10-16 17:29:06.408395+00	2025-10-16 17:29:06.408397+00	74
569	f	\N	1663	Тассай	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.40928+00	2025-10-16 17:29:06.409631+00	2025-10-16 17:29:06.409633+00	74
570	f	\N	1662	Сарқыра	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.410302+00	2025-10-16 17:29:06.410595+00	2025-10-16 17:29:06.410597+00	61
571	f	\N	1661	Союз	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.411103+00	2025-10-16 17:29:06.411347+00	2025-10-16 17:29:06.411349+00	43
572	f	\N	1660	Улан	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.411833+00	2025-10-16 17:29:06.412096+00	2025-10-16 17:29:06.412098+00	43
573	f	\N	1659	Тамыр	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.412575+00	2025-10-16 17:29:06.412856+00	2025-10-16 17:29:06.412859+00	43
574	f	\N	1658	Қызылқоңыр	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.413313+00	2025-10-16 17:29:06.413592+00	2025-10-16 17:29:06.413595+00	108
575	f	\N	1657	сюрприз	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.414121+00	2025-10-16 17:29:06.414398+00	2025-10-16 17:29:06.414401+00	126
576	f	\N	1656	Янтарь	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.414852+00	2025-10-16 17:29:06.415122+00	2025-10-16 17:29:06.415125+00	126
578	f	\N	1654	Игилик	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.416434+00	2025-10-16 17:29:06.41672+00	2025-10-16 17:29:06.416722+00	60
579	f	\N	1653	Айдын	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.417256+00	2025-10-16 17:29:06.417843+00	2025-10-16 17:29:06.417846+00	150
580	f	\N	1652	Ақжайық 17 СВ	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.41841+00	2025-10-16 17:29:06.418699+00	2025-10-16 17:29:06.418702+00	54
581	f	\N	1651	Нартау	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.419205+00	2025-10-16 17:29:06.419474+00	2025-10-16 17:29:06.419476+00	43
582	f	\N	1650	Үшқоңыр	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.419971+00	2025-10-16 17:29:06.420227+00	2025-10-16 17:29:06.420229+00	43
583	f	\N	1649	Текес	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.420665+00	2025-10-16 17:29:06.42094+00	2025-10-16 17:29:06.420942+00	43
584	f	\N	1648	Дарын	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.421364+00	2025-10-16 17:29:06.4216+00	2025-10-16 17:29:06.421602+00	126
585	f	\N	1647	Памяти Кабировой	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.422033+00	2025-10-16 17:29:06.422267+00	2025-10-16 17:29:06.422269+00	79
586	f	\N	1646	Казахстанская 20	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.422707+00	2025-10-16 17:29:06.422976+00	2025-10-16 17:29:06.422978+00	115
587	f	\N	1645	Жетысу-1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.423412+00	2025-10-16 17:29:06.423685+00	2025-10-16 17:29:06.423687+00	115
588	f	\N	1644	Ырым	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.424152+00	2025-10-16 17:29:06.424509+00	2025-10-16 17:29:06.424511+00	71
589	f	\N	1643	Балауса 8	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.425303+00	2025-10-16 17:29:06.425806+00	2025-10-16 17:29:06.425811+00	127
590	f	\N	1642	Мөлдір-2008	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.426447+00	2025-10-16 17:29:06.426768+00	2025-10-16 17:29:06.42677+00	106
591	f	\N	1641	Самад	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.427257+00	2025-10-16 17:29:06.427557+00	2025-10-16 17:29:06.42756+00	71
592	f	\N	1640	Оркен	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.428052+00	2025-10-16 17:29:06.428298+00	2025-10-16 17:29:06.4283+00	79
593	f	\N	1639	Алия	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.428751+00	2025-10-16 17:29:06.429011+00	2025-10-16 17:29:06.429013+00	71
594	f	\N	1638	Майра	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.429451+00	2025-10-16 17:29:06.429717+00	2025-10-16 17:29:06.429719+00	71
595	f	\N	1637	Нуреке	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.430217+00	2025-10-16 17:29:06.430483+00	2025-10-16 17:29:06.430485+00	71
596	f	\N	1636	Степная 75	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.430932+00	2025-10-16 17:29:06.431245+00	2025-10-16 17:29:06.431247+00	71
597	f	\N	1635	Илек 20	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.431727+00	2025-10-16 17:29:06.431997+00	2025-10-16 17:29:06.431999+00	149
598	f	\N	1634	КАЗНИИР-5	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.432476+00	2025-10-16 17:29:06.43285+00	2025-10-16 17:29:06.432853+00	102
599	f	\N	1633	Инкар	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.433463+00	2025-10-16 17:29:06.433968+00	2025-10-16 17:29:06.433971+00	149
600	f	\N	1632	Раминал	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.43487+00	2025-10-16 17:29:06.43519+00	2025-10-16 17:29:06.435192+00	71
601	f	\N	1631	Салауат	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.435923+00	2025-10-16 17:29:06.436196+00	2025-10-16 17:29:06.436199+00	123
602	f	\N	1630	Достык	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.43697+00	2025-10-16 17:29:06.437276+00	2025-10-16 17:29:06.437278+00	144
603	f	\N	1629	Кумис	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.437814+00	2025-10-16 17:29:06.438132+00	2025-10-16 17:29:06.438134+00	16
604	f	\N	1628	Абзал	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.438629+00	2025-10-16 17:29:06.438925+00	2025-10-16 17:29:06.438928+00	113
605	f	\N	1627	Казахстан-20	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.439395+00	2025-10-16 17:29:06.439671+00	2025-10-16 17:29:06.439673+00	16
606	f	\N	1626	Ай-Ару	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.440114+00	2025-10-16 17:29:06.440355+00	2025-10-16 17:29:06.440357+00	16
607	f	\N	1625	Столичный	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.440917+00	2025-10-16 17:29:06.441272+00	2025-10-16 17:29:06.441274+00	43
608	f	\N	1624	Арай-255	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.442008+00	2025-10-16 17:29:06.4424+00	2025-10-16 17:29:06.442425+00	60
609	f	\N	1623	Эгалите	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.443076+00	2025-10-16 17:29:06.443364+00	2025-10-16 17:29:06.443366+00	79
610	f	\N	1622	Мадина	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.443848+00	2025-10-16 17:29:06.444121+00	2025-10-16 17:29:06.444123+00	102
611	f	\N	1621	Жансая	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.444554+00	2025-10-16 17:29:06.444827+00	2025-10-16 17:29:06.444829+00	119
612	f	\N	1620	Искра	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.445269+00	2025-10-16 17:29:06.445509+00	2025-10-16 17:29:06.445511+00	119
613	f	\N	1619	Болашақ	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.445968+00	2025-10-16 17:29:06.446217+00	2025-10-16 17:29:06.44622+00	119
614	f	\N	1618	КАЗСУФФЛЕ-1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.446653+00	2025-10-16 17:29:06.446923+00	2025-10-16 17:29:06.446926+00	149
616	f	\N	1616	Целинный 2005	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.448231+00	2025-10-16 17:29:06.448488+00	2025-10-16 17:29:06.44849+00	149
617	f	\N	1615	Никола	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.448941+00	2025-10-16 17:29:06.44922+00	2025-10-16 17:29:06.449223+00	76
618	f	\N	1614	Памяти Раисы	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.449856+00	2025-10-16 17:29:06.450207+00	2025-10-16 17:29:06.450209+00	149
619	f	\N	1613	Майлы дән	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.450884+00	2025-10-16 17:29:06.451199+00	2025-10-16 17:29:06.451201+00	97
620	f	\N	1612	SK-10178	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.45178+00	2025-10-16 17:29:06.452059+00	2025-10-16 17:29:06.452061+00	88
621	f	\N	1611	Аннушка	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.452578+00	2025-10-16 17:29:06.452867+00	2025-10-16 17:29:06.452869+00	119
622	f	\N	1610	Анастасия	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.453361+00	2025-10-16 17:29:06.453666+00	2025-10-16 17:29:06.453669+00	119
623	f	\N	1609	Билявка	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.454181+00	2025-10-16 17:29:06.454427+00	2025-10-16 17:29:06.454429+00	119
624	f	\N	1608	Мавка	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.454906+00	2025-10-16 17:29:06.455167+00	2025-10-16 17:29:06.455169+00	119
625	f	\N	1607	Шагалалы	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.455626+00	2025-10-16 17:29:06.45589+00	2025-10-16 17:29:06.455892+00	43
626	f	\N	1606	Кизинд	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.456361+00	2025-10-16 17:29:06.456604+00	2025-10-16 17:29:06.456606+00	115
627	f	\N	1605	Аружан	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.457053+00	2025-10-16 17:29:06.457285+00	2025-10-16 17:29:06.457287+00	90
628	f	\N	1604	КазЕр-6	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.457851+00	2025-10-16 17:29:06.458149+00	2025-10-16 17:29:06.458152+00	102
629	f	\N	1603	Жуалы	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.459041+00	2025-10-16 17:29:06.459696+00	2025-10-16 17:29:06.459699+00	43
630	f	\N	1602	Жолбарыс	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.460411+00	2025-10-16 17:29:06.460719+00	2025-10-16 17:29:06.460721+00	43
631	f	\N	1601	ЭН ЦЕФЕЙ	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.461214+00	2025-10-16 17:29:06.46146+00	2025-10-16 17:29:06.461462+00	71
632	f	\N	1600	ЭН ЦЕФЕЙ	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.461911+00	2025-10-16 17:29:06.462155+00	2025-10-16 17:29:06.462157+00	71
633	f	\N	1599	Максим	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.462602+00	2025-10-16 17:29:06.462908+00	2025-10-16 17:29:06.46291+00	43
634	f	\N	1598	Таңшолпан	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.463416+00	2025-10-16 17:29:06.463684+00	2025-10-16 17:29:06.463687+00	126
635	f	\N	1597	Волгоуральская	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.46418+00	2025-10-16 17:29:06.464445+00	2025-10-16 17:29:06.464447+00	71
636	f	\N	1596	Атланта	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.464946+00	2025-10-16 17:29:06.465197+00	2025-10-16 17:29:06.465199+00	119
637	f	\N	1595	Караой-90	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.465648+00	2025-10-16 17:29:06.46613+00	2025-10-16 17:29:06.466132+00	71
638	f	\N	1594	Момышұлы	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.466792+00	2025-10-16 17:29:06.467219+00	2025-10-16 17:29:06.467223+00	71
639	f	\N	1593	Карабалыкская озимая	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.468072+00	2025-10-16 17:29:06.468383+00	2025-10-16 17:29:06.468385+00	71
640	f	\N	1592	РА 1040506	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.468866+00	2025-10-16 17:29:06.469111+00	2025-10-16 17:29:06.469113+00	88
641	f	\N	1591	Булава	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.469548+00	2025-10-16 17:29:06.469827+00	2025-10-16 17:29:06.469829+00	71
642	f	\N	1590	Нур-38	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.470262+00	2025-10-16 17:29:06.470516+00	2025-10-16 17:29:06.470518+00	71
643	f	\N	1589	Симбиоз	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.470954+00	2025-10-16 17:29:06.471195+00	2025-10-16 17:29:06.471197+00	20
644	f	\N	1588	Ақсары	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.471629+00	2025-10-16 17:29:06.471891+00	2025-10-16 17:29:06.471893+00	20
645	f	\N	1587	Старт	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.472311+00	2025-10-16 17:29:06.472546+00	2025-10-16 17:29:06.472549+00	71
646	f	\N	1586	Степь	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.473056+00	2025-10-16 17:29:06.473321+00	2025-10-16 17:29:06.473323+00	71
647	f	\N	1585	Омский Коралл	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.473751+00	2025-10-16 17:29:06.474014+00	2025-10-16 17:29:06.474017+00	123
648	f	\N	1584	Омская 43	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.474785+00	2025-10-16 17:29:06.475188+00	2025-10-16 17:29:06.475191+00	71
649	f	\N	1583	ОВЁС ЕРТІС САМАЛЫ	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.476203+00	2025-10-16 17:29:06.476579+00	2025-10-16 17:29:06.476581+00	76
650	f	\N	1582	Омская 42	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.477128+00	2025-10-16 17:29:06.477424+00	2025-10-16 17:29:06.477426+00	71
651	f	\N	1581	Омская 42	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.477879+00	2025-10-16 17:29:06.478117+00	2025-10-16 17:29:06.478119+00	71
652	f	\N	1580	Вираж	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.478566+00	2025-10-16 17:29:06.478856+00	2025-10-16 17:29:06.478859+00	149
653	f	\N	1579	Династия	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.479354+00	2025-10-16 17:29:06.479597+00	2025-10-16 17:29:06.4796+00	71
654	f	\N	1578	Янтарная 150	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.480131+00	2025-10-16 17:29:06.48038+00	2025-10-16 17:29:06.480383+00	123
655	f	\N	1577	Ертіс самалы	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.480838+00	2025-10-16 17:29:06.48109+00	2025-10-16 17:29:06.481092+00	76
656	f	\N	1576	Махтаарал-5040	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.481568+00	2025-10-16 17:29:06.481851+00	2025-10-16 17:29:06.481853+00	133
657	f	\N	1575	Махтаарал-5030	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.482299+00	2025-10-16 17:29:06.482802+00	2025-10-16 17:29:06.482804+00	133
658	f	\N	1574	Шаңырақ	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.483436+00	2025-10-16 17:29:06.483864+00	2025-10-16 17:29:06.483867+00	71
659	f	\N	1573	Карабалыкская ранняя	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.484479+00	2025-10-16 17:29:06.48476+00	2025-10-16 17:29:06.484763+00	71
660	f	\N	1572	Бірлік КВ	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.485255+00	2025-10-16 17:29:06.485538+00	2025-10-16 17:29:06.48554+00	119
661	f	\N	1571	Августина	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.486038+00	2025-10-16 17:29:06.486301+00	2025-10-16 17:29:06.486303+00	71
662	f	\N	1570	Отар-2	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.486755+00	2025-10-16 17:29:06.487011+00	2025-10-16 17:29:06.487013+00	71
663	f	\N	1569	Урал-1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.487452+00	2025-10-16 17:29:06.48771+00	2025-10-16 17:29:06.487713+00	43
664	f	\N	1568	Прогресс	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.488162+00	2025-10-16 17:29:06.488402+00	2025-10-16 17:29:06.488404+00	119
665	f	\N	1567	Батыр	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.488821+00	2025-10-16 17:29:06.489052+00	2025-10-16 17:29:06.489054+00	88
666	f	\N	1566	Ламис	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.489469+00	2025-10-16 17:29:06.48972+00	2025-10-16 17:29:06.489722+00	71
667	f	\N	1565	Ивушка	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.490142+00	2025-10-16 17:29:06.490403+00	2025-10-16 17:29:06.490405+00	119
668	f	\N	1564	Кулан	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.491044+00	2025-10-16 17:29:06.491389+00	2025-10-16 17:29:06.491391+00	76
669	f	\N	1563	Скульптор	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.492264+00	2025-10-16 17:29:06.492638+00	2025-10-16 17:29:06.492641+00	119
670	f	\N	1562	Сакура	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.49341+00	2025-10-16 17:29:06.493716+00	2025-10-16 17:29:06.493718+00	141
671	f	\N	1561	Алуа	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.494214+00	2025-10-16 17:29:06.494492+00	2025-10-16 17:29:06.494494+00	119
672	f	\N	1560	Аль-Фараби 2020	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.494964+00	2025-10-16 17:29:06.495208+00	2025-10-16 17:29:06.49521+00	71
673	f	\N	1559	ЭКСПО	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.495676+00	2025-10-16 17:29:06.495916+00	2025-10-16 17:29:06.495918+00	88
674	f	\N	1558	Экспо-2017	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.496374+00	2025-10-16 17:29:06.496628+00	2025-10-16 17:29:06.496631+00	71
675	f	\N	1557	Шырайлы	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.497069+00	2025-10-16 17:29:06.497303+00	2025-10-16 17:29:06.497305+00	141
676	f	\N	1556	Жарык	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.497842+00	2025-10-16 17:29:06.498097+00	2025-10-16 17:29:06.498099+00	107
677	f	\N	1555	Орда	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.498556+00	2025-10-16 17:29:06.498832+00	2025-10-16 17:29:06.498835+00	127
678	f	\N	1554	Джелли	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.499374+00	2025-10-16 17:29:06.499693+00	2025-10-16 17:29:06.499696+00	43
679	f	\N	1553	Целинная 2008	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.500414+00	2025-10-16 17:29:06.500842+00	2025-10-16 17:29:06.500845+00	71
680	f	\N	1552	Красноводопадская 210	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.501404+00	2025-10-16 17:29:06.501704+00	2025-10-16 17:29:06.501706+00	71
681	f	\N	1551	Октябрина 70	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.502319+00	2025-10-16 17:29:06.502564+00	2025-10-16 17:29:06.502566+00	71
682	f	\N	1550	Южная 12	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.503022+00	2025-10-16 17:29:06.503261+00	2025-10-16 17:29:06.503263+00	71
683	f	\N	1549	Береке-54	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.503686+00	2025-10-16 17:29:06.503926+00	2025-10-16 17:29:06.503928+00	149
684	f	\N	1548	Богара	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.504342+00	2025-10-16 17:29:06.504622+00	2025-10-16 17:29:06.504625+00	149
685	f	\N	1547	Kafka	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.505061+00	2025-10-16 17:29:06.505292+00	2025-10-16 17:29:06.505294+00	79
686	f	\N	1546	Pruva	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.505737+00	2025-10-16 17:29:06.506027+00	2025-10-16 17:29:06.50603+00	79
687	f	\N	1545	DRW 7629 F1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.506474+00	2025-10-16 17:29:06.506752+00	2025-10-16 17:29:06.506754+00	126
688	f	\N	1544	Локе	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.507253+00	2025-10-16 17:29:06.507631+00	2025-10-16 17:29:06.507634+00	33
689	f	\N	1543	Назар	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.508285+00	2025-10-16 17:29:06.508694+00	2025-10-16 17:29:06.508697+00	35
690	f	\N	1542	Фейерверк	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.509293+00	2025-10-16 17:29:06.509574+00	2025-10-16 17:29:06.509577+00	75
691	f	\N	1541	Әсем	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.510062+00	2025-10-16 17:29:06.510338+00	2025-10-16 17:29:06.510341+00	75
692	f	\N	1540	Плакучая	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.510787+00	2025-10-16 17:29:06.511052+00	2025-10-16 17:29:06.511054+00	75
693	f	\N	1539	Айлана-2017	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.511486+00	2025-10-16 17:29:06.511732+00	2025-10-16 17:29:06.511734+00	121
694	f	\N	1538	Кокорай	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.512211+00	2025-10-16 17:29:06.512511+00	2025-10-16 17:29:06.512514+00	61
695	f	\N	1537	Шабыт-80	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.51298+00	2025-10-16 17:29:06.513239+00	2025-10-16 17:29:06.513242+00	61
696	f	\N	1536	Асалет	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.513759+00	2025-10-16 17:29:06.514044+00	2025-10-16 17:29:06.514047+00	126
697	f	\N	1535	Беатрикс	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.514499+00	2025-10-16 17:29:06.514793+00	2025-10-16 17:29:06.514796+00	149
698	f	\N	1534	Алтыночка	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.515288+00	2025-10-16 17:29:06.515549+00	2025-10-16 17:29:06.515552+00	32
699	f	\N	1533	Савел	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.516213+00	2025-10-16 17:29:06.516524+00	2025-10-16 17:29:06.516527+00	58
700	f	\N	1532	Сарқыра	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.517358+00	2025-10-16 17:29:06.517745+00	2025-10-16 17:29:06.517748+00	61
701	f	\N	1531	Ривертон (Riverton)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.518296+00	2025-10-16 17:29:06.518592+00	2025-10-16 17:29:06.518594+00	119
702	f	\N	1530	Нунавик (Nunavik)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.519364+00	2025-10-16 17:29:06.519648+00	2025-10-16 17:29:06.51965+00	119
703	f	\N	1529	Ньюпорт (Newport)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.520111+00	2025-10-16 17:29:06.520354+00	2025-10-16 17:29:06.520356+00	119
704	f	\N	1528	Киркленд (Kirkland)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.520798+00	2025-10-16 17:29:06.52105+00	2025-10-16 17:29:06.521052+00	119
705	f	\N	1527	Калгари (Calgary)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.521813+00	2025-10-16 17:29:06.522051+00	2025-10-16 17:29:06.522053+00	119
706	f	\N	1526	Эри (Erie)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.522474+00	2025-10-16 17:29:06.522734+00	2025-10-16 17:29:06.522736+00	119
707	f	\N	1524	ЗАУК 31	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.523204+00	2025-10-16 17:29:06.523461+00	2025-10-16 17:29:06.523464+00	146
708	f	\N	1523	Тогжан	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.524081+00	2025-10-16 17:29:06.524495+00	2025-10-16 17:29:06.524497+00	137
709	f	\N	1522	Колсай	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.525117+00	2025-10-16 17:29:06.525576+00	2025-10-16 17:29:06.525579+00	113
710	f	\N	1521	Колсай	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.526473+00	2025-10-16 17:29:06.526763+00	2025-10-16 17:29:06.526765+00	113
711	f	\N	1520	Бейбит	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.527304+00	2025-10-16 17:29:06.527574+00	2025-10-16 17:29:06.527576+00	29
712	f	\N	1519	Бейбит	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.528026+00	2025-10-16 17:29:06.528271+00	2025-10-16 17:29:06.528273+00	29
713	f	\N	1518	ЛГ 50549 СХ	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.528753+00	2025-10-16 17:29:06.529019+00	2025-10-16 17:29:06.529021+00	88
714	f	\N	1517	ЛГ 5463 КЛ	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.52949+00	2025-10-16 17:29:06.529751+00	2025-10-16 17:29:06.529754+00	88
715	f	\N	1516	проверочный гибрид	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.530192+00	2025-10-16 17:29:06.530428+00	2025-10-16 17:29:06.53043+00	88
716	f	\N	1515	проверочный гибрид	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.530866+00	2025-10-16 17:29:06.531121+00	2025-10-16 17:29:06.531123+00	88
717	f	\N	1514	проверочный гибрид	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.531564+00	2025-10-16 17:29:06.53185+00	2025-10-16 17:29:06.531852+00	88
718	f	\N	1513	Кларасол	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.532305+00	2025-10-16 17:29:06.532681+00	2025-10-16 17:29:06.532684+00	88
719	f	\N	1512	Сегурия	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.533303+00	2025-10-16 17:29:06.533744+00	2025-10-16 17:29:06.533747+00	88
720	f	\N	1511	Медикум 18	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.534388+00	2025-10-16 17:29:06.534673+00	2025-10-16 17:29:06.534675+00	150
721	f	\N	1510	Маргрет	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.535142+00	2025-10-16 17:29:06.535412+00	2025-10-16 17:29:06.535414+00	149
722	f	\N	1509	Маргрет	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.535898+00	2025-10-16 17:29:06.536189+00	2025-10-16 17:29:06.536191+00	149
723	f	\N	1508	Маргрет	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.536695+00	2025-10-16 17:29:06.53697+00	2025-10-16 17:29:06.536973+00	149
724	f	\N	1507	Медикум 18	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.537411+00	2025-10-16 17:29:06.537662+00	2025-10-16 17:29:06.537664+00	149
725	f	\N	1506	Медикум 18	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.538103+00	2025-10-16 17:29:06.538339+00	2025-10-16 17:29:06.538341+00	149
726	f	\N	1505	Омская 36	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.53877+00	2025-10-16 17:29:06.539013+00	2025-10-16 17:29:06.539015+00	71
727	f	\N	1504	Тризо	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.539492+00	2025-10-16 17:29:06.539764+00	2025-10-16 17:29:06.539767+00	71
728	f	\N	1503	Ламис	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.540219+00	2025-10-16 17:29:06.540452+00	2025-10-16 17:29:06.540454+00	71
729	f	\N	1502	Ламис	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.540993+00	2025-10-16 17:29:06.541311+00	2025-10-16 17:29:06.541314+00	71
730	f	\N	1501	Асангали 20	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.542087+00	2025-10-16 17:29:06.542493+00	2025-10-16 17:29:06.542496+00	123
731	f	\N	1500	Фурио Камилло	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.543077+00	2025-10-16 17:29:06.543361+00	2025-10-16 17:29:06.543364+00	123
732	f	\N	1499	Фурио Камилло	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.543881+00	2025-10-16 17:29:06.544131+00	2025-10-16 17:29:06.544133+00	123
733	f	\N	1498	Градиска (Gradisca)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.544583+00	2025-10-16 17:29:06.544882+00	2025-10-16 17:29:06.544884+00	146
734	f	\N	1497	ВА 38 (WA 38)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.54535+00	2025-10-16 17:29:06.545592+00	2025-10-16 17:29:06.545594+00	146
735	f	\N	1496	RX 01IMI	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.546049+00	2025-10-16 17:29:06.546296+00	2025-10-16 17:29:06.546298+00	88
736	f	\N	1495	Султан	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.546739+00	2025-10-16 17:29:06.546994+00	2025-10-16 17:29:06.546996+00	88
737	f	\N	1494	Алекса СУ	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.547452+00	2025-10-16 17:29:06.547751+00	2025-10-16 17:29:06.547753+00	88
738	f	\N	1493	КХЦ 00121	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.548214+00	2025-10-16 17:29:06.548485+00	2025-10-16 17:29:06.548487+00	88
739	f	\N	1490	ЛГ 50549 СХ	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.54891+00	2025-10-16 17:29:06.549264+00	2025-10-16 17:29:06.549267+00	88
740	f	\N	1489	ЛГ 58390	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.549876+00	2025-10-16 17:29:06.550226+00	2025-10-16 17:29:06.550229+00	88
741	f	\N	1488	ЛГ 50550 КЛП	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.550964+00	2025-10-16 17:29:06.551255+00	2025-10-16 17:29:06.551257+00	88
742	f	\N	1487	Артезия	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.55175+00	2025-10-16 17:29:06.552024+00	2025-10-16 17:29:06.552026+00	119
743	f	\N	1486	Памела	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.552478+00	2025-10-16 17:29:06.552755+00	2025-10-16 17:29:06.552758+00	119
744	f	\N	1485	Милка	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.553189+00	2025-10-16 17:29:06.553419+00	2025-10-16 17:29:06.553421+00	119
745	f	\N	1483	Sylvana	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.55385+00	2025-10-16 17:29:06.554151+00	2025-10-16 17:29:06.554153+00	43
746	f	\N	1482	Камелия	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.554811+00	2025-10-16 17:29:06.555061+00	2025-10-16 17:29:06.555063+00	43
747	f	\N	1481	Lady Rosetta	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.555495+00	2025-10-16 17:29:06.555739+00	2025-10-16 17:29:06.555741+00	43
748	f	\N	1480	Норман	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.556163+00	2025-10-16 17:29:06.556409+00	2025-10-16 17:29:06.556411+00	43
749	f	\N	1479	Бурбон	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.556832+00	2025-10-16 17:29:06.557069+00	2025-10-16 17:29:06.557071+00	123
750	f	\N	1478	Евгения	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.557565+00	2025-10-16 17:29:06.55797+00	2025-10-16 17:29:06.557973+00	149
751	f	\N	1477	Лариса янтарная	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.558582+00	2025-10-16 17:29:06.559003+00	2025-10-16 17:29:06.559006+00	123
752	f	\N	1476	Таганрог	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.559629+00	2025-10-16 17:29:06.559951+00	2025-10-16 17:29:06.559954+00	123
753	f	\N	1475	Бурбон	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.560451+00	2025-10-16 17:29:06.560765+00	2025-10-16 17:29:06.560768+00	123
754	f	\N	1474	Евгения	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.561214+00	2025-10-16 17:29:06.561458+00	2025-10-16 17:29:06.56146+00	149
755	f	\N	1473	Лауреат	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.561938+00	2025-10-16 17:29:06.562185+00	2025-10-16 17:29:06.562187+00	71
756	f	\N	1472	Орда	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.562624+00	2025-10-16 17:29:06.56288+00	2025-10-16 17:29:06.562882+00	149
757	f	\N	1471	Эксплоер	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.563303+00	2025-10-16 17:29:06.563538+00	2025-10-16 17:29:06.563541+00	150
758	f	\N	1470	Калисперо	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.563967+00	2025-10-16 17:29:06.56421+00	2025-10-16 17:29:06.564212+00	71
759	f	\N	1469	Карагандинская 31	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.564651+00	2025-10-16 17:29:06.564924+00	2025-10-16 17:29:06.564926+00	71
760	f	\N	1468	Челябинка	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.565349+00	2025-10-16 17:29:06.565595+00	2025-10-16 17:29:06.565597+00	71
761	f	\N	1466	Карагандинский 5	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.566474+00	2025-10-16 17:29:06.567126+00	2025-10-16 17:29:06.567129+00	150
762	f	\N	1465	Улан	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.56793+00	2025-10-16 17:29:06.568233+00	2025-10-16 17:29:06.568235+00	150
763	f	\N	1464	Достык УК	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.568749+00	2025-10-16 17:29:06.569009+00	2025-10-16 17:29:06.569011+00	88
764	f	\N	1463	Медикум 18	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.569559+00	2025-10-16 17:29:06.569828+00	2025-10-16 17:29:06.56983+00	150
765	f	\N	1462	P64LE25	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.570249+00	2025-10-16 17:29:06.570508+00	2025-10-16 17:29:06.570511+00	88
766	f	\N	1461	TERMEZ	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.570974+00	2025-10-16 17:29:06.571223+00	2025-10-16 17:29:06.571225+00	5
767	f	\N	1460	Астана	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.571653+00	2025-10-16 17:29:06.571915+00	2025-10-16 17:29:06.571918+00	93
768	f	\N	1459	Уральская 100	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.572353+00	2025-10-16 17:29:06.572635+00	2025-10-16 17:29:06.572638+00	93
769	f	\N	1458	Медина	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.573096+00	2025-10-16 17:29:06.573385+00	2025-10-16 17:29:06.573388+00	146
770	f	\N	1457	Адина	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.573967+00	2025-10-16 17:29:06.574285+00	2025-10-16 17:29:06.574287+00	146
771	f	\N	1456	Аликос	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.57493+00	2025-10-16 17:29:06.575426+00	2025-10-16 17:29:06.575428+00	29
772	f	\N	1455	Жадыра	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.576003+00	2025-10-16 17:29:06.576291+00	2025-10-16 17:29:06.576293+00	113
773	f	\N	1454	Маркен	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.576981+00	2025-10-16 17:29:06.577247+00	2025-10-16 17:29:06.577249+00	137
774	f	\N	1453	Алмаз-23	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.577758+00	2025-10-16 17:29:06.578023+00	2025-10-16 17:29:06.578025+00	137
775	f	\N	1452	Эндем	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.578516+00	2025-10-16 17:29:06.578784+00	2025-10-16 17:29:06.578787+00	113
776	f	\N	1451	Ерме-Сат	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.579216+00	2025-10-16 17:29:06.579455+00	2025-10-16 17:29:06.579457+00	16
777	f	\N	1450	Назерке	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.5799+00	2025-10-16 17:29:06.580157+00	2025-10-16 17:29:06.580159+00	16
778	f	\N	1449	Безостая 100 оз.	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.58064+00	2025-10-16 17:29:06.580909+00	2025-10-16 17:29:06.580911+00	71
779	f	\N	1448	Еланчик оз.	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.58138+00	2025-10-16 17:29:06.581655+00	2025-10-16 17:29:06.581657+00	71
780	f	\N	1447	Жалғас оз.	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.582148+00	2025-10-16 17:29:06.582407+00	2025-10-16 17:29:06.582409+00	149
781	f	\N	1446	Тимирязевка 150 оз.	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.582866+00	2025-10-16 17:29:06.583113+00	2025-10-16 17:29:06.583115+00	71
782	f	\N	1445	ЭН ПЕРСЕЙ (EN PERSEY) оз.	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.583576+00	2025-10-16 17:29:06.583869+00	2025-10-16 17:29:06.583871+00	71
783	f	\N	1444	ЭН ВОИН (EN VOIN) оз.	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.584625+00	2025-10-16 17:29:06.58497+00	2025-10-16 17:29:06.584972+00	71
784	f	\N	1443	ЭН ВИНТЕРФЕЛЛ (EN WINTERFELL) оз.	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.585544+00	2025-10-16 17:29:06.585842+00	2025-10-16 17:29:06.585844+00	71
785	f	\N	1442	ЭН ТАЙГЕТА (EN TAYGETA) оз.	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.586337+00	2025-10-16 17:29:06.586585+00	2025-10-16 17:29:06.586587+00	71
786	f	\N	1441	Салуозо (Saluoso)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.587115+00	2025-10-16 17:29:06.587378+00	2025-10-16 17:29:06.58738+00	126
787	f	\N	1440	Томари (Tomary)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.587854+00	2025-10-16 17:29:06.588097+00	2025-10-16 17:29:06.5881+00	126
788	f	\N	1439	Уюм (Uyum)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.588536+00	2025-10-16 17:29:06.588789+00	2025-10-16 17:29:06.588791+00	126
789	f	\N	1438	Атари (Atary)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.589214+00	2025-10-16 17:29:06.589456+00	2025-10-16 17:29:06.589458+00	126
790	f	\N	1437	Зульфия (Zulfia)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.590185+00	2025-10-16 17:29:06.590506+00	2025-10-16 17:29:06.590508+00	126
791	f	\N	1436	Кавагучи (Kawaguchi)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.591601+00	2025-10-16 17:29:06.591966+00	2025-10-16 17:29:06.591968+00	126
792	f	\N	1435	Викарио (Vicario)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.592566+00	2025-10-16 17:29:06.592863+00	2025-10-16 17:29:06.592866+00	10
793	f	\N	1434	Конгама (Congama)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.593334+00	2025-10-16 17:29:06.593596+00	2025-10-16 17:29:06.593598+00	40
794	f	\N	1433	Санфредо (Sanfredo)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.594079+00	2025-10-16 17:29:06.594342+00	2025-10-16 17:29:06.594344+00	126
795	f	\N	1432	Карилло (Karillo)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.594806+00	2025-10-16 17:29:06.595064+00	2025-10-16 17:29:06.595066+00	41
796	f	\N	1431	Куантум (Kuantum)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.595511+00	2025-10-16 17:29:06.595768+00	2025-10-16 17:29:06.59577+00	126
797	f	\N	1430	Каргу (KARGU)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.596207+00	2025-10-16 17:29:06.596444+00	2025-10-16 17:29:06.596446+00	79
798	f	\N	1429	Фактор	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.596869+00	2025-10-16 17:29:06.597101+00	2025-10-16 17:29:06.597103+00	58
799	f	\N	1428	Бақытжан оз.	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.597523+00	2025-10-16 17:29:06.597775+00	2025-10-16 17:29:06.597777+00	71
800	f	\N	1427	Дельта	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.598257+00	2025-10-16 17:29:06.598891+00	2025-10-16 17:29:06.598894+00	129
801	f	\N	1426	Индиго F1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.599582+00	2025-10-16 17:29:06.600271+00	2025-10-16 17:29:06.600275+00	82
802	f	\N	1425	Долина	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.601033+00	2025-10-16 17:29:06.60135+00	2025-10-16 17:29:06.601353+00	144
803	f	\N	1424	FC13-113	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.601837+00	2025-10-16 17:29:06.602089+00	2025-10-16 17:29:06.602091+00	19
804	f	\N	1423	БАЗАР	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.602532+00	2025-10-16 17:29:06.602861+00	2025-10-16 17:29:06.602864+00	47
877	f	\N	1350	Феникс	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.662132+00	2025-10-16 17:29:06.6624+00	2025-10-16 17:29:06.662402+00	94
805	f	\N	1422	Шуга Деликата Ф1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.603316+00	2025-10-16 17:29:06.603555+00	2025-10-16 17:29:06.603557+00	5
806	f	\N	1421	Микадо F1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.604005+00	2025-10-16 17:29:06.604244+00	2025-10-16 17:29:06.604247+00	5
807	f	\N	1420	Velox	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.604666+00	2025-10-16 17:29:06.604903+00	2025-10-16 17:29:06.604905+00	43
808	f	\N	1419	Адората	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.605349+00	2025-10-16 17:29:06.605589+00	2025-10-16 17:29:06.605591+00	43
809	f	\N	1418	Мегаполис F1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.606048+00	2025-10-16 17:29:06.606284+00	2025-10-16 17:29:06.606286+00	40
810	f	\N	1417	МОА	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.60677+00	2025-10-16 17:29:06.60712+00	2025-10-16 17:29:06.607123+00	43
811	f	\N	1416	Памяти Байтулина	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.607852+00	2025-10-16 17:29:06.608177+00	2025-10-16 17:29:06.608179+00	75
812	f	\N	1415	Шетластинка	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.60868+00	2025-10-16 17:29:06.608916+00	2025-10-16 17:29:06.608918+00	75
813	f	\N	1414	Алпагу (Alpagu)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.609385+00	2025-10-16 17:29:06.609643+00	2025-10-16 17:29:06.609645+00	79
814	f	\N	1413	Прогресс	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.610258+00	2025-10-16 17:29:06.610543+00	2025-10-16 17:29:06.610545+00	126
815	f	\N	1412	Адванс (Advance)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.611331+00	2025-10-16 17:29:06.611669+00	2025-10-16 17:29:06.611671+00	126
816	f	\N	1411	Солероссо	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.612151+00	2025-10-16 17:29:06.612387+00	2025-10-16 17:29:06.612389+00	126
817	f	\N	1410	Н 6438	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.612861+00	2025-10-16 17:29:06.613105+00	2025-10-16 17:29:06.613107+00	126
818	f	\N	1409	Гоген (Gaugin)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.613539+00	2025-10-16 17:29:06.613815+00	2025-10-16 17:29:06.613817+00	104
819	f	\N	1408	Каравел (Caravel)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.614243+00	2025-10-16 17:29:06.614516+00	2025-10-16 17:29:06.614518+00	104
820	f	\N	1407	Кармези (Carmesi)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.615016+00	2025-10-16 17:29:06.615286+00	2025-10-16 17:29:06.615288+00	104
821	f	\N	1406	Лозано (Lozano)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.616011+00	2025-10-16 17:29:06.616307+00	2025-10-16 17:29:06.61631+00	104
822	f	\N	1405	Аквино (Aquino)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.616923+00	2025-10-16 17:29:06.61754+00	2025-10-16 17:29:06.617544+00	104
823	f	\N	1404	Экспедишн (Expedition)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.618414+00	2025-10-16 17:29:06.618783+00	2025-10-16 17:29:06.618786+00	104
824	f	\N	1403	Портека (Porteca)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.619368+00	2025-10-16 17:29:06.619655+00	2025-10-16 17:29:06.619657+00	82
825	f	\N	1402	Рубинштейн (Rubinstein)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.620128+00	2025-10-16 17:29:06.620383+00	2025-10-16 17:29:06.620386+00	79
826	f	\N	1401	Заказ 4 (Zakaz 4)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.620826+00	2025-10-16 17:29:06.621095+00	2025-10-16 17:29:06.621097+00	40
827	f	\N	1400	Тэфия Ф1 (Tephia F1)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.62152+00	2025-10-16 17:29:06.621793+00	2025-10-16 17:29:06.621796+00	5
828	f	\N	1399	Корвин (Korvin)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.622252+00	2025-10-16 17:29:06.622588+00	2025-10-16 17:29:06.62259+00	79
829	f	\N	1398	Силема (Cilema)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.623086+00	2025-10-16 17:29:06.623366+00	2025-10-16 17:29:06.623368+00	40
830	f	\N	1397	Адема (Adema)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.623857+00	2025-10-16 17:29:06.624324+00	2025-10-16 17:29:06.624328+00	40
831	f	\N	1396	Тореадор (Toreador)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.62512+00	2025-10-16 17:29:06.625608+00	2025-10-16 17:29:06.625622+00	40
832	f	\N	1395	Ливерпуль (Liverpool)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.62667+00	2025-10-16 17:29:06.627003+00	2025-10-16 17:29:06.627006+00	5
833	f	\N	1394	Гонгга (Gongga)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.627529+00	2025-10-16 17:29:06.627815+00	2025-10-16 17:29:06.627817+00	10
834	f	\N	1393	СК Альта	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.628277+00	2025-10-16 17:29:06.628557+00	2025-10-16 17:29:06.62856+00	119
835	f	\N	1392	СК Артика	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.629014+00	2025-10-16 17:29:06.629261+00	2025-10-16 17:29:06.629263+00	119
836	f	\N	1391	СК Виола	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.629706+00	2025-10-16 17:29:06.629965+00	2025-10-16 17:29:06.629967+00	119
837	f	\N	1390	Лансор (Lancor)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.630386+00	2025-10-16 17:29:06.630637+00	2025-10-16 17:29:06.63064+00	126
838	f	\N	1389	Ольмека (Olmeca)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.631125+00	2025-10-16 17:29:06.631396+00	2025-10-16 17:29:06.631398+00	126
839	f	\N	1388	Рива (Riva)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.631827+00	2025-10-16 17:29:06.632068+00	2025-10-16 17:29:06.63207+00	40
840	f	\N	1387	СПЕЙССТАР ГОЛД (Spacestar Gold)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.632535+00	2025-10-16 17:29:06.632968+00	2025-10-16 17:29:06.632971+00	42
841	f	\N	1386	КМ 5512	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.633682+00	2025-10-16 17:29:06.634132+00	2025-10-16 17:29:06.634135+00	126
842	f	\N	1385	Латона Ф1 (Latona F1)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.63475+00	2025-10-16 17:29:06.635031+00	2025-10-16 17:29:06.635034+00	5
843	f	\N	1384	Импреса F1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.635526+00	2025-10-16 17:29:06.635792+00	2025-10-16 17:29:06.635794+00	79
844	f	\N	1383	Бетси F1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.636255+00	2025-10-16 17:29:06.636502+00	2025-10-16 17:29:06.636504+00	38
845	f	\N	1382	ГАСПАР Ф1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.636983+00	2025-10-16 17:29:06.637254+00	2025-10-16 17:29:06.637257+00	126
846	f	\N	1381	Айкидо F1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.637715+00	2025-10-16 17:29:06.637953+00	2025-10-16 17:29:06.637955+00	126
847	f	\N	1380	May 558	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.638385+00	2025-10-16 17:29:06.63863+00	2025-10-16 17:29:06.638632+00	133
848	f	\N	1379	МH 7001	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.639087+00	2025-10-16 17:29:06.639324+00	2025-10-16 17:29:06.639327+00	107
849	f	\N	1378	МH 7002	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.639802+00	2025-10-16 17:29:06.64007+00	2025-10-16 17:29:06.640072+00	107
850	f	\N	1377	Маргарита КВС	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.640525+00	2025-10-16 17:29:06.640811+00	2025-10-16 17:29:06.640814+00	107
851	f	\N	1376	Росселина КВС (Rosselina KWS)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.641268+00	2025-10-16 17:29:06.641506+00	2025-10-16 17:29:06.641508+00	107
852	f	\N	1375	Смарт Фьола КВС	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.641924+00	2025-10-16 17:29:06.642173+00	2025-10-16 17:29:06.642175+00	107
853	f	\N	1374	Смарт Деонила КВС	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.642607+00	2025-10-16 17:29:06.642888+00	2025-10-16 17:29:06.64289+00	107
854	f	\N	1373	Смарт Фьола КВС	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.643312+00	2025-10-16 17:29:06.643622+00	2025-10-16 17:29:06.643625+00	107
855	f	\N	1372	Смарт Сеза КВС (Smart Seza KWS)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.644298+00	2025-10-16 17:29:06.644589+00	2025-10-16 17:29:06.644591+00	107
856	f	\N	1371	БТС Смарт 3525	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.64517+00	2025-10-16 17:29:06.645423+00	2025-10-16 17:29:06.645425+00	107
857	f	\N	1370	БТС Смарт 2020 (BTS Smart 2020)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.645877+00	2025-10-16 17:29:06.646121+00	2025-10-16 17:29:06.646124+00	107
858	f	\N	1369	БТС 980	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.64682+00	2025-10-16 17:29:06.647081+00	2025-10-16 17:29:06.647083+00	107
859	f	\N	1368	БТС 3560 (BTS 3560)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.647531+00	2025-10-16 17:29:06.647805+00	2025-10-16 17:29:06.647808+00	107
860	f	\N	1367	БТС Смарт 2020	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.648267+00	2025-10-16 17:29:06.648515+00	2025-10-16 17:29:06.648517+00	107
861	f	\N	1366	БТС Смарт 3525 (BTS SMART 3525)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.64898+00	2025-10-16 17:29:06.649367+00	2025-10-16 17:29:06.64937+00	107
862	f	\N	1365	БТС 3560	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.649859+00	2025-10-16 17:29:06.650133+00	2025-10-16 17:29:06.650135+00	107
863	f	\N	1364	БТС 980 (BTS 980)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.650575+00	2025-10-16 17:29:06.650849+00	2025-10-16 17:29:06.650851+00	107
864	f	\N	1363	Вакита Смарт (Vaquita Smart)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.651274+00	2025-10-16 17:29:06.651579+00	2025-10-16 17:29:06.651581+00	107
865	f	\N	1362	Агама Смарт (Agame Smart)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.652133+00	2025-10-16 17:29:06.652419+00	2025-10-16 17:29:06.652421+00	107
866	f	\N	1361	БТС Смарт 2020	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.652871+00	2025-10-16 17:29:06.65316+00	2025-10-16 17:29:06.653162+00	107
867	f	\N	1360	БТС Смарт 9695	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.653602+00	2025-10-16 17:29:06.653885+00	2025-10-16 17:29:06.653888+00	107
868	f	\N	1359	Аксу	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.654344+00	2025-10-16 17:29:06.654586+00	2025-10-16 17:29:06.654588+00	107
869	f	\N	1358	Ынтымақ	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.655077+00	2025-10-16 17:29:06.655358+00	2025-10-16 17:29:06.65536+00	107
870	f	\N	1357	Светлана	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.655854+00	2025-10-16 17:29:06.656129+00	2025-10-16 17:29:06.656132+00	29
871	f	\N	1356	Аяулым	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.656655+00	2025-10-16 17:29:06.65696+00	2025-10-16 17:29:06.656963+00	16
872	f	\N	1355	Мукагали-90	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.657641+00	2025-10-16 17:29:06.657957+00	2025-10-16 17:29:06.657959+00	146
873	f	\N	1354	Аягоз	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.658796+00	2025-10-16 17:29:06.659166+00	2025-10-16 17:29:06.659169+00	137
874	f	\N	1353	Акмолинец	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.659773+00	2025-10-16 17:29:06.660098+00	2025-10-16 17:29:06.660101+00	115
875	f	\N	1352	Северянка	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.660633+00	2025-10-16 17:29:06.66091+00	2025-10-16 17:29:06.660912+00	121
876	f	\N	1351	Батыр Дала	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.661393+00	2025-10-16 17:29:06.661684+00	2025-10-16 17:29:06.661687+00	35
878	f	\N	1349	Саури (Sauri)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.662871+00	2025-10-16 17:29:06.663143+00	2025-10-16 17:29:06.663146+00	115
879	f	\N	1348	Ида (Ida)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.663653+00	2025-10-16 17:29:06.663973+00	2025-10-16 17:29:06.663975+00	61
880	f	\N	1347	Бовитал (Bovital)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.664492+00	2025-10-16 17:29:06.664791+00	2025-10-16 17:29:06.664794+00	117
881	f	\N	1346	Манила (Manila)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.665283+00	2025-10-16 17:29:06.666733+00	2025-10-16 17:29:06.666743+00	117
882	f	\N	1345	Эффект (Effect)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.668518+00	2025-10-16 17:29:06.673042+00	2025-10-16 17:29:06.673052+00	49
883	f	\N	1344	Илонара/Ilonara	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.67702+00	2025-10-16 17:29:06.679322+00	2025-10-16 17:29:06.679332+00	79
884	f	\N	1343	МАС 804Г	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.681583+00	2025-10-16 17:29:06.683524+00	2025-10-16 17:29:06.683548+00	88
885	f	\N	1342	Арунасан ИР (Arunasun IR)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.687139+00	2025-10-16 17:29:06.688746+00	2025-10-16 17:29:06.688755+00	88
886	f	\N	1341	Волльтер СУ (Vollter SU)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.692735+00	2025-10-16 17:29:06.693412+00	2025-10-16 17:29:06.693416+00	88
887	f	\N	1340	Сани Ими (Sunny IMI)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.694363+00	2025-10-16 17:29:06.694745+00	2025-10-16 17:29:06.694748+00	88
888	f	\N	1339	ЕС Авалон (ES Avalon)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.695684+00	2025-10-16 17:29:06.696198+00	2025-10-16 17:29:06.696202+00	88
889	f	\N	1338	ЕС Тор (ES Tor)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.697415+00	2025-10-16 17:29:06.69828+00	2025-10-16 17:29:06.698283+00	88
890	f	\N	1337	ЕС Старк (ES Stark)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.699759+00	2025-10-16 17:29:06.7002+00	2025-10-16 17:29:06.700203+00	88
891	f	\N	1336	МИШО (Misho)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.701184+00	2025-10-16 17:29:06.70156+00	2025-10-16 17:29:06.701563+00	88
892	f	\N	1335	ВЕСИ (Vessy)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.702155+00	2025-10-16 17:29:06.702451+00	2025-10-16 17:29:06.702454+00	88
893	f	\N	1334	Solexis	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.703018+00	2025-10-16 17:29:06.703309+00	2025-10-16 17:29:06.703311+00	88
894	f	\N	1333	КРИПТОСОЛ СУЛЬФО (KRIPTOSOL SULFO)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.703795+00	2025-10-16 17:29:06.704059+00	2025-10-16 17:29:06.704062+00	88
895	f	\N	1332	SANDER	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.704515+00	2025-10-16 17:29:06.704825+00	2025-10-16 17:29:06.704827+00	88
896	f	\N	1331	КЛАРАСОЛ КЛ (ClARASOL CL)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.705325+00	2025-10-16 17:29:06.705622+00	2025-10-16 17:29:06.705625+00	88
897	f	\N	1330	Solexis	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.70624+00	2025-10-16 17:29:06.706528+00	2025-10-16 17:29:06.70653+00	88
898	f	\N	1329	СЕГИРИЯ СУЛЬФО (SEGUIRIYA SULFO))	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.707058+00	2025-10-16 17:29:06.707332+00	2025-10-16 17:29:06.707334+00	88
899	f	\N	1328	ХАЙСАН 254 (Hysun 254)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.708067+00	2025-10-16 17:29:06.708449+00	2025-10-16 17:29:06.708451+00	88
900	f	\N	1327	Азур	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.709248+00	2025-10-16 17:29:06.709697+00	2025-10-16 17:29:06.7097+00	55
901	f	\N	1326	Достык УК	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.710329+00	2025-10-16 17:29:06.710644+00	2025-10-16 17:29:06.710646+00	88
902	f	\N	1325	Үміт УК	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.71123+00	2025-10-16 17:29:06.711556+00	2025-10-16 17:29:06.711558+00	88
903	f	\N	1324	Жасылай	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.712112+00	2025-10-16 17:29:06.712414+00	2025-10-16 17:29:06.712416+00	20
904	f	\N	1323	Көкшалғын	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.712957+00	2025-10-16 17:29:06.713231+00	2025-10-16 17:29:06.713233+00	61
905	f	\N	1322	Агробизнес 2050	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.713683+00	2025-10-16 17:29:06.713942+00	2025-10-16 17:29:06.713944+00	88
906	f	\N	1321	Agroforce (Агрофорсе)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.71439+00	2025-10-16 17:29:06.714669+00	2025-10-16 17:29:06.714671+00	88
907	f	\N	1320	Казахстанский 465	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.715169+00	2025-10-16 17:29:06.715449+00	2025-10-16 17:29:06.715451+00	88
908	f	\N	1319	KZ 777 (КЗ 777)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.716175+00	2025-10-16 17:29:06.716701+00	2025-10-16 17:29:06.716704+00	88
909	f	\N	1318	Baiterek S	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.717663+00	2025-10-16 17:29:06.718033+00	2025-10-16 17:29:06.718036+00	88
910	f	\N	1317	Baiterek 23 (Байтерек 23)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.718642+00	2025-10-16 17:29:06.718954+00	2025-10-16 17:29:06.718956+00	88
911	f	\N	1316	Елмерей	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.719473+00	2025-10-16 17:29:06.71974+00	2025-10-16 17:29:06.719742+00	119
912	f	\N	1315	Ақбастау	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.720262+00	2025-10-16 17:29:06.720551+00	2025-10-16 17:29:06.720553+00	119
913	f	\N	1314	Вектор	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.721061+00	2025-10-16 17:29:06.721347+00	2025-10-16 17:29:06.721349+00	71
914	f	\N	1313	Хошими	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.721805+00	2025-10-16 17:29:06.722058+00	2025-10-16 17:29:06.72206+00	102
915	f	\N	1312	Айсара	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.722602+00	2025-10-16 17:29:06.7229+00	2025-10-16 17:29:06.722902+00	102
916	f	\N	1311	Аманат	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.723452+00	2025-10-16 17:29:06.723722+00	2025-10-16 17:29:06.723724+00	71
917	f	\N	1310	Дулати	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.724409+00	2025-10-16 17:29:06.72478+00	2025-10-16 17:29:06.724783+00	71
918	f	\N	1309	Адесса (Adessa)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.725382+00	2025-10-16 17:29:06.725837+00	2025-10-16 17:29:06.72584+00	119
919	f	\N	1308	Иринасол (Irinasol)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.72642+00	2025-10-16 17:29:06.726715+00	2025-10-16 17:29:06.726717+00	88
920	f	\N	1307	Хелесан СУ (Helesun SU)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.727217+00	2025-10-16 17:29:06.727472+00	2025-10-16 17:29:06.727474+00	88
921	f	\N	1306	Агробизнес 2050	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.72794+00	2025-10-16 17:29:06.728219+00	2025-10-16 17:29:06.728221+00	88
922	f	\N	1305	OLEIN 23 (ОЛЕИН 23)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.728702+00	2025-10-16 17:29:06.728982+00	2025-10-16 17:29:06.728984+00	88
923	f	\N	1304	СИЛАЧ	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.729473+00	2025-10-16 17:29:06.729793+00	2025-10-16 17:29:06.729795+00	71
924	f	\N	1303	Камелия	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.73033+00	2025-10-16 17:29:06.730681+00	2025-10-16 17:29:06.730684+00	27
925	f	\N	1302	Шортандинское 7	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.731222+00	2025-10-16 17:29:06.731572+00	2025-10-16 17:29:06.731575+00	90
926	f	\N	1301	Реноме	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.732435+00	2025-10-16 17:29:06.732903+00	2025-10-16 17:29:06.732905+00	90
927	f	\N	1300	Кормовое 89	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.733798+00	2025-10-16 17:29:06.734273+00	2025-10-16 17:29:06.734276+00	90
928	f	\N	1299	Изумрудное	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.734922+00	2025-10-16 17:29:06.735227+00	2025-10-16 17:29:06.735229+00	90
929	f	\N	1298	Нутриджет (Nutrijet)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.735755+00	2025-10-16 17:29:06.736027+00	2025-10-16 17:29:06.736029+00	6
930	f	\N	1297	Фениккс ЭсЭль012 (FENIKKS SL012)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.736513+00	2025-10-16 17:29:06.73681+00	2025-10-16 17:29:06.736812+00	88
931	f	\N	1296	Казветта	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.737299+00	2025-10-16 17:29:06.737552+00	2025-10-16 17:29:06.737555+00	102
932	f	\N	1295	Алмавита	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.738016+00	2025-10-16 17:29:06.738278+00	2025-10-16 17:29:06.73828+00	102
933	f	\N	1294	Куман (KUMAN)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.738736+00	2025-10-16 17:29:06.739+00	2025-10-16 17:29:06.739002+00	88
934	f	\N	1293	Маттео (MATTEO)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.739462+00	2025-10-16 17:29:06.739734+00	2025-10-16 17:29:06.739736+00	88
935	f	\N	1292	Темплар	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.740281+00	2025-10-16 17:29:06.740542+00	2025-10-16 17:29:06.740544+00	88
936	f	\N	1291	Коммент (Komment)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.741284+00	2025-10-16 17:29:06.741723+00	2025-10-16 17:29:06.741726+00	88
937	f	\N	1290	Данте (DANTE)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.74247+00	2025-10-16 17:29:06.742927+00	2025-10-16 17:29:06.74293+00	88
938	f	\N	1289	АРНЕТЕС СУ (ARNETES SU)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.743554+00	2025-10-16 17:29:06.743872+00	2025-10-16 17:29:06.743875+00	88
939	f	\N	1288	ДОДЖ КЛП (DODGE CLP)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.7444+00	2025-10-16 17:29:06.744679+00	2025-10-16 17:29:06.744682+00	88
940	f	\N	1287	АГР 07 (AGR 07)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.745146+00	2025-10-16 17:29:06.745412+00	2025-10-16 17:29:06.745415+00	88
941	f	\N	1286	АГР 05 (AGR 05)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.745882+00	2025-10-16 17:29:06.746138+00	2025-10-16 17:29:06.74614+00	88
942	f	\N	1285	1931 СЛ (1931 CL)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.746583+00	2025-10-16 17:29:06.746868+00	2025-10-16 17:29:06.746871+00	88
943	f	\N	1284	Репост (REPOST)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.747318+00	2025-10-16 17:29:06.747569+00	2025-10-16 17:29:06.747572+00	88
944	f	\N	1283	Ивушка	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.748109+00	2025-10-16 17:29:06.748378+00	2025-10-16 17:29:06.74838+00	119
945	f	\N	1282	ҚосТана	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.748832+00	2025-10-16 17:29:06.74923+00	2025-10-16 17:29:06.749233+00	119
946	f	\N	1281	Алана	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.75015+00	2025-10-16 17:29:06.750633+00	2025-10-16 17:29:06.750636+00	119
947	f	\N	1280	Аруна (ВГ2Т008)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.751416+00	2025-10-16 17:29:06.75181+00	2025-10-16 17:29:06.751813+00	119
948	f	\N	1279	Алайа (ВГ2Т009)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.752377+00	2025-10-16 17:29:06.752718+00	2025-10-16 17:29:06.752721+00	119
949	f	\N	1278	Махаббат (ВГ2Т010)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.753379+00	2025-10-16 17:29:06.753773+00	2025-10-16 17:29:06.753775+00	119
1098	f	\N	1128	Amandus	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.882894+00	2025-10-16 17:29:06.883195+00	2025-10-16 17:29:06.883197+00	93
950	f	\N	1277	Акасса (Acassa)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.754278+00	2025-10-16 17:29:06.754549+00	2025-10-16 17:29:06.754552+00	119
951	f	\N	1276	Малага	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.755051+00	2025-10-16 17:29:06.755304+00	2025-10-16 17:29:06.755306+00	119
952	f	\N	1275	Акумара (Akumara)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.7558+00	2025-10-16 17:29:06.756042+00	2025-10-16 17:29:06.756044+00	119
953	f	\N	1274	Ласточка	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.756553+00	2025-10-16 17:29:06.756863+00	2025-10-16 17:29:06.756865+00	119
954	f	\N	1273	Амалия	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.757636+00	2025-10-16 17:29:06.758039+00	2025-10-16 17:29:06.758042+00	119
955	f	\N	1272	Аннушка	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.759078+00	2025-10-16 17:29:06.759434+00	2025-10-16 17:29:06.759437+00	119
956	f	\N	1271	EURASIA (ЕВРАЗИЯ)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.760038+00	2025-10-16 17:29:06.760337+00	2025-10-16 17:29:06.760339+00	119
957	f	\N	1270	Анабелла (Annabella)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.760929+00	2025-10-16 17:29:06.761191+00	2025-10-16 17:29:06.761193+00	119
958	f	\N	1269	СХ 8282	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.761685+00	2025-10-16 17:29:06.761953+00	2025-10-16 17:29:06.761955+00	88
959	f	\N	1268	СХ 2264	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.762435+00	2025-10-16 17:29:06.762712+00	2025-10-16 17:29:06.762715+00	88
960	f	\N	1267	Атакама (Atacama)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.763206+00	2025-10-16 17:29:06.763485+00	2025-10-16 17:29:06.763487+00	119
961	f	\N	1266	СХ 2314	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.764048+00	2025-10-16 17:29:06.764369+00	2025-10-16 17:29:06.764371+00	88
962	f	\N	1265	Опус	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.764878+00	2025-10-16 17:29:06.765157+00	2025-10-16 17:29:06.765159+00	119
963	f	\N	1264	Элина (Elina)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.765762+00	2025-10-16 17:29:06.766217+00	2025-10-16 17:29:06.76622+00	119
964	f	\N	1263	Черемош	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.767352+00	2025-10-16 17:29:06.767853+00	2025-10-16 17:29:06.767856+00	119
965	f	\N	1262	Сюнонг 42 (Suinong 42)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.768505+00	2025-10-16 17:29:06.768826+00	2025-10-16 17:29:06.768828+00	119
966	f	\N	1261	Ангелика (Angelica)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.769373+00	2025-10-16 17:29:06.769625+00	2025-10-16 17:29:06.769628+00	119
967	f	\N	1260	Вегас	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.77017+00	2025-10-16 17:29:06.770448+00	2025-10-16 17:29:06.77045+00	88
968	f	\N	1259	Атанга (Atanga)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.77096+00	2025-10-16 17:29:06.771234+00	2025-10-16 17:29:06.771236+00	119
969	f	\N	1258	Сибирячка	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.771739+00	2025-10-16 17:29:06.772094+00	2025-10-16 17:29:06.772097+00	119
970	f	\N	1257	Сибириада	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.77271+00	2025-10-16 17:29:06.773007+00	2025-10-16 17:29:06.773009+00	119
971	f	\N	1256	Кубань 43	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.77353+00	2025-10-16 17:29:06.773883+00	2025-10-16 17:29:06.773886+00	119
972	f	\N	1255	Хэйхэ 43 (Heihe 43)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.774541+00	2025-10-16 17:29:06.774942+00	2025-10-16 17:29:06.774944+00	119
973	f	\N	1254	Максус	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.775734+00	2025-10-16 17:29:06.776151+00	2025-10-16 17:29:06.776154+00	119
974	f	\N	1253	Юнка (Yunka)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.776784+00	2025-10-16 17:29:06.7771+00	2025-10-16 17:29:06.777103+00	119
975	f	\N	1252	Берисей	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.777677+00	2025-10-16 17:29:06.777961+00	2025-10-16 17:29:06.777963+00	20
976	f	\N	1251	Асылай	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.778446+00	2025-10-16 17:29:06.778702+00	2025-10-16 17:29:06.778705+00	20
977	f	\N	1250	Камила 1255	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.7792+00	2025-10-16 17:29:06.779467+00	2025-10-16 17:29:06.779469+00	74
978	f	\N	1249	Алпамыс	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.779933+00	2025-10-16 17:29:06.780187+00	2025-10-16 17:29:06.780189+00	74
979	f	\N	1248	Сымбат 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.78067+00	2025-10-16 17:29:06.780944+00	2025-10-16 17:29:06.780946+00	74
980	f	\N	1247	Самға	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.781421+00	2025-10-16 17:29:06.781699+00	2025-10-16 17:29:06.781701+00	74
981	f	\N	1246	Шанс	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.782175+00	2025-10-16 17:29:06.782572+00	2025-10-16 17:29:06.782575+00	20
982	f	\N	1245	Карлос 115	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.783165+00	2025-10-16 17:29:06.783466+00	2025-10-16 17:29:06.783469+00	88
983	f	\N	1244	BADIL	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.784119+00	2025-10-16 17:29:06.784461+00	2025-10-16 17:29:06.784464+00	74
984	f	\N	1243	Гарсуко (Garsuco)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.784991+00	2025-10-16 17:29:06.785277+00	2025-10-16 17:29:06.785279+00	74
985	f	\N	1242	Юбилейный	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.78581+00	2025-10-16 17:29:06.786102+00	2025-10-16 17:29:06.786104+00	74
986	f	\N	1241	Ақжол	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.786583+00	2025-10-16 17:29:06.786875+00	2025-10-16 17:29:06.786877+00	74
987	f	\N	1240	4 ЕН 0044 (4 EN 0044)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.787355+00	2025-10-16 17:29:06.787634+00	2025-10-16 17:29:06.787636+00	97
988	f	\N	1239	Панчо	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.788087+00	2025-10-16 17:29:06.788358+00	2025-10-16 17:29:06.78836+00	88
989	f	\N	1238	Нурлан	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.788817+00	2025-10-16 17:29:06.789071+00	2025-10-16 17:29:06.789073+00	106
990	f	\N	1237	Водопад-23	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.789572+00	2025-10-16 17:29:06.789868+00	2025-10-16 17:29:06.78987+00	106
991	f	\N	1236	Центр 70	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.790334+00	2025-10-16 17:29:06.790585+00	2025-10-16 17:29:06.790587+00	106
992	f	\N	1235	Глория	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.79159+00	2025-10-16 17:29:06.792109+00	2025-10-16 17:29:06.792112+00	106
993	f	\N	1234	Тиаки	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.792816+00	2025-10-16 17:29:06.79312+00	2025-10-16 17:29:06.793122+00	88
994	f	\N	1233	ОС22ЛУ02 (OS22LU02)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.793715+00	2025-10-16 17:29:06.794001+00	2025-10-16 17:29:06.794003+00	55
995	f	\N	1232	Центр 70	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.794567+00	2025-10-16 17:29:06.794863+00	2025-10-16 17:29:06.794866+00	106
996	f	\N	1231	БҚ-1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.795375+00	2025-10-16 17:29:06.795678+00	2025-10-16 17:29:06.795681+00	106
997	f	\N	1230	Интеркрус	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.796165+00	2025-10-16 17:29:06.796417+00	2025-10-16 17:29:06.796419+00	88
998	f	\N	1229	Тенгри	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.796893+00	2025-10-16 17:29:06.797156+00	2025-10-16 17:29:06.797158+00	97
999	f	\N	1228	Магнум	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.797628+00	2025-10-16 17:29:06.797925+00	2025-10-16 17:29:06.797927+00	88
1000	f	\N	1227	ОСР23СС20	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.798463+00	2025-10-16 17:29:06.799056+00	2025-10-16 17:29:06.799059+00	97
1001	f	\N	1226	Веховская	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.799915+00	2025-10-16 17:29:06.800362+00	2025-10-16 17:29:06.800364+00	141
1002	f	\N	1225	Ханшайым	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.801401+00	2025-10-16 17:29:06.801788+00	2025-10-16 17:29:06.80179+00	141
1003	f	\N	1224	ФД16СЛ50	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.802357+00	2025-10-16 17:29:06.80265+00	2025-10-16 17:29:06.802654+00	88
1004	f	\N	1223	ФД19Е42	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.803158+00	2025-10-16 17:29:06.80343+00	2025-10-16 17:29:06.803432+00	88
1005	f	\N	1222	ФД18Е41	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.803896+00	2025-10-16 17:29:06.804154+00	2025-10-16 17:29:06.804156+00	88
1006	f	\N	1221	Фолк	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.804647+00	2025-10-16 17:29:06.804903+00	2025-10-16 17:29:06.804905+00	88
1007	f	\N	1220	Колумб	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.80537+00	2025-10-16 17:29:06.805645+00	2025-10-16 17:29:06.805647+00	88
1008	f	\N	1219	Тенет	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.806144+00	2025-10-16 17:29:06.80641+00	2025-10-16 17:29:06.806412+00	88
1009	f	\N	1218	Мастак	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.806887+00	2025-10-16 17:29:06.80714+00	2025-10-16 17:29:06.807142+00	88
1010	f	\N	1217	Карлос 105	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.80782+00	2025-10-16 17:29:06.808186+00	2025-10-16 17:29:06.808188+00	88
1011	f	\N	1216	Солнечное настроение	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.809029+00	2025-10-16 17:29:06.809439+00	2025-10-16 17:29:06.809442+00	88
1012	f	\N	1214	ЕС ЛОНДОН СУ (ES LONDON SU)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.810058+00	2025-10-16 17:29:06.810324+00	2025-10-16 17:29:06.810326+00	88
1013	f	\N	1213	ЕС ГЕНЕЗИС (ES GENESIS)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.810854+00	2025-10-16 17:29:06.811113+00	2025-10-16 17:29:06.811115+00	88
1014	f	\N	1212	ИНСАН 288 СЛП (INSUN 288 CLP)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.811575+00	2025-10-16 17:29:06.811861+00	2025-10-16 17:29:06.811863+00	88
1015	f	\N	1211	1044 Л СУ (1044L SU)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.812327+00	2025-10-16 17:29:06.812587+00	2025-10-16 17:29:06.812589+00	88
1016	f	\N	1210	Фениккс ДжиЭль1578 (FENIKKS JL1578)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.813054+00	2025-10-16 17:29:06.813305+00	2025-10-16 17:29:06.813307+00	88
1017	f	\N	1209	Фениккс ДжиЭль888 (FENIKKS JL888)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.813779+00	2025-10-16 17:29:06.814022+00	2025-10-16 17:29:06.814024+00	88
1018	f	\N	1208	Фениккс ДжиЭль 777 (FENIKKS JL 777)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.814489+00	2025-10-16 17:29:06.814783+00	2025-10-16 17:29:06.814793+00	88
1019	f	\N	1207	Фениккс ДжиЭль 5131 (FENIKKS JL5131)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.815238+00	2025-10-16 17:29:06.815514+00	2025-10-16 17:29:06.815516+00	88
1020	f	\N	1206	Фениккс ДжиЭль5131	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.816269+00	2025-10-16 17:29:06.816656+00	2025-10-16 17:29:06.816659+00	88
1021	f	\N	1205	Фениккс ДжиЭль516 (FENIKKS JL516)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.817322+00	2025-10-16 17:29:06.817731+00	2025-10-16 17:29:06.817734+00	88
1022	f	\N	1204	Метеор	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.818324+00	2025-10-16 17:29:06.818669+00	2025-10-16 17:29:06.818671+00	20
1023	f	\N	1203	Фениккс ДжиЭль524 (FENIKKS JL524)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.819168+00	2025-10-16 17:29:06.819453+00	2025-10-16 17:29:06.819455+00	88
1024	f	\N	1202	Гинда (GUINDA)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.819964+00	2025-10-16 17:29:06.820274+00	2025-10-16 17:29:06.820276+00	20
1025	f	\N	1201	Фениккс ЭсЭль 177 (FENIKKS SL 177)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.820855+00	2025-10-16 17:29:06.821135+00	2025-10-16 17:29:06.821137+00	88
1026	f	\N	1200	Фениккс ЭсЭль012 (FENIKKS SL012)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.821592+00	2025-10-16 17:29:06.821878+00	2025-10-16 17:29:06.82188+00	88
1027	f	\N	1199	Фениккс ЭсЭль008 (FENIKKS SL008)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.82233+00	2025-10-16 17:29:06.82258+00	2025-10-16 17:29:06.822582+00	88
1028	f	\N	1198	СУБЕРИК (SUBERIC)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.823089+00	2025-10-16 17:29:06.823537+00	2025-10-16 17:29:06.82354+00	88
1029	f	\N	1197	СИ ДАРВИН КЛП (SY DARVIN CLP)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.824224+00	2025-10-16 17:29:06.824632+00	2025-10-16 17:29:06.824634+00	88
1030	f	\N	1196	СИ Нерида (SY NERIDA)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.825537+00	2025-10-16 17:29:06.826038+00	2025-10-16 17:29:06.826041+00	88
1031	f	\N	1195	P63LE10	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.826701+00	2025-10-16 17:29:06.82699+00	2025-10-16 17:29:06.826993+00	88
1032	f	\N	1194	АЯЧЕ СУ (AIACE SU)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.827506+00	2025-10-16 17:29:06.827767+00	2025-10-16 17:29:06.827769+00	88
1033	f	\N	1193	ES CEYLON	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.828257+00	2025-10-16 17:29:06.828515+00	2025-10-16 17:29:06.828517+00	88
1034	f	\N	1192	АПС94 (APS94)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.829+00	2025-10-16 17:29:06.829272+00	2025-10-16 17:29:06.829274+00	88
1035	f	\N	1191	LG5463	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.829766+00	2025-10-16 17:29:06.830024+00	2025-10-16 17:29:06.830026+00	88
1036	f	\N	1190	АПС 85 (APS85)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.830518+00	2025-10-16 17:29:06.830819+00	2025-10-16 17:29:06.830821+00	88
1037	f	\N	1189	НЕМО (NEMO)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.831333+00	2025-10-16 17:29:06.831713+00	2025-10-16 17:29:06.831716+00	88
1038	f	\N	1188	FORTIMI	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.832578+00	2025-10-16 17:29:06.83305+00	2025-10-16 17:29:06.833052+00	88
1039	f	\N	1187	LG59580	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.833779+00	2025-10-16 17:29:06.834105+00	2025-10-16 17:29:06.834108+00	88
1040	f	\N	1186	ЙОЛЕН (IOLEN)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.834657+00	2025-10-16 17:29:06.83494+00	2025-10-16 17:29:06.834942+00	88
1041	f	\N	1185	АПСФ32 (APSF32)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.835424+00	2025-10-16 17:29:06.835712+00	2025-10-16 17:29:06.835715+00	88
1042	f	\N	1184	TRISTAN	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.836193+00	2025-10-16 17:29:06.83647+00	2025-10-16 17:29:06.836472+00	88
1043	f	\N	1183	КСИЛО (XILO)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.836932+00	2025-10-16 17:29:06.837207+00	2025-10-16 17:29:06.83721+00	88
1044	f	\N	1182	СХ 2014	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.8377+00	2025-10-16 17:29:06.838005+00	2025-10-16 17:29:06.838008+00	88
1045	f	\N	1181	СХ 5326	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.838482+00	2025-10-16 17:29:06.838762+00	2025-10-16 17:29:06.838764+00	88
1046	f	\N	1180	СХ 5220	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.839213+00	2025-10-16 17:29:06.83949+00	2025-10-16 17:29:06.839492+00	88
1047	f	\N	1179	СХ 2154	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.839945+00	2025-10-16 17:29:06.840205+00	2025-10-16 17:29:06.840207+00	88
1048	f	\N	1178	СХ 2365	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.840776+00	2025-10-16 17:29:06.84114+00	2025-10-16 17:29:06.841142+00	88
1049	f	\N	1177	Інжу-077	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.841815+00	2025-10-16 17:29:06.842318+00	2025-10-16 17:29:06.842322+00	130
1050	f	\N	1176	Асыл	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.843088+00	2025-10-16 17:29:06.843405+00	2025-10-16 17:29:06.843408+00	130
1051	f	\N	1175	Шырайлы	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.844031+00	2025-10-16 17:29:06.84431+00	2025-10-16 17:29:06.844312+00	141
1052	f	\N	1174	Кочевница	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.84482+00	2025-10-16 17:29:06.845072+00	2025-10-16 17:29:06.845075+00	141
1053	f	\N	1173	BADIL	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.84555+00	2025-10-16 17:29:06.845838+00	2025-10-16 17:29:06.845841+00	74
1054	f	\N	1172	Гарбинье (Garbine)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.846294+00	2025-10-16 17:29:06.846566+00	2025-10-16 17:29:06.846569+00	74
1055	f	\N	1171	Евгения	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.847056+00	2025-10-16 17:29:06.847314+00	2025-10-16 17:29:06.847316+00	149
1056	f	\N	1170	Крешендо	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.847797+00	2025-10-16 17:29:06.848048+00	2025-10-16 17:29:06.848051+00	149
1057	f	\N	1169	Тася	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.84858+00	2025-10-16 17:29:06.84887+00	2025-10-16 17:29:06.848874+00	149
1058	f	\N	1168	Ейфель	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.849455+00	2025-10-16 17:29:06.849769+00	2025-10-16 17:29:06.849771+00	149
1059	f	\N	1167	ФОРМУЛА 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.850495+00	2025-10-16 17:29:06.850853+00	2025-10-16 17:29:06.850856+00	149
1060	f	\N	1166	Массимо Меридио	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.851485+00	2025-10-16 17:29:06.851795+00	2025-10-16 17:29:06.851798+00	123
1061	f	\N	1165	Марко Аурелио	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.852322+00	2025-10-16 17:29:06.852604+00	2025-10-16 17:29:06.852606+00	123
1062	f	\N	1164	Ахмет 150	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.853189+00	2025-10-16 17:29:06.853453+00	2025-10-16 17:29:06.853456+00	123
1063	f	\N	1163	Топаз	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.85395+00	2025-10-16 17:29:06.854203+00	2025-10-16 17:29:06.854205+00	71
1064	f	\N	1162	Минот	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.854696+00	2025-10-16 17:29:06.854956+00	2025-10-16 17:29:06.854959+00	71
1065	f	\N	1161	Каликсо	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.855412+00	2025-10-16 17:29:06.855698+00	2025-10-16 17:29:06.8557+00	71
1066	f	\N	1160	КС Элем	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.856356+00	2025-10-16 17:29:06.85667+00	2025-10-16 17:29:06.856672+00	71
1067	f	\N	1159	Элайя	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.857323+00	2025-10-16 17:29:06.857704+00	2025-10-16 17:29:06.857706+00	71
1068	f	\N	1158	Ликамеро	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.858422+00	2025-10-16 17:29:06.858832+00	2025-10-16 17:29:06.858835+00	71
1069	f	\N	1157	КВС Акбатор	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.859423+00	2025-10-16 17:29:06.859738+00	2025-10-16 17:29:06.85974+00	103
1070	f	\N	1156	KWS-H10129	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.860259+00	2025-10-16 17:29:06.860518+00	2025-10-16 17:29:06.86052+00	103
1071	f	\N	1155	Charisma	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.861005+00	2025-10-16 17:29:06.861267+00	2025-10-16 17:29:06.861269+00	150
1072	f	\N	1154	Финола (Finola)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.861748+00	2025-10-16 17:29:06.862009+00	2025-10-16 17:29:06.862011+00	150
1073	f	\N	1153	KWS Tonik	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.862485+00	2025-10-16 17:29:06.862742+00	2025-10-16 17:29:06.862744+00	150
1074	f	\N	1152	Кариока (Carioca)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.863196+00	2025-10-16 17:29:06.863452+00	2025-10-16 17:29:06.863454+00	150
1075	f	\N	1151	СХ 2321	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.863942+00	2025-10-16 17:29:06.864201+00	2025-10-16 17:29:06.864203+00	88
1076	f	\N	1150	СХ 2563	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.864652+00	2025-10-16 17:29:06.86491+00	2025-10-16 17:29:06.864913+00	88
1077	f	\N	1149	ЕС Пегас (EC Pegas)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.86538+00	2025-10-16 17:29:06.865651+00	2025-10-16 17:29:06.865654+00	88
1078	f	\N	1148	П64ЛЕ137 (P64LE137)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.866285+00	2025-10-16 17:29:06.866603+00	2025-10-16 17:29:06.866605+00	88
1079	f	\N	1147	ЛГ 50449 СХ (LG 50449 SX)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.867318+00	2025-10-16 17:29:06.867712+00	2025-10-16 17:29:06.867715+00	88
1080	f	\N	1146	ЛГ 50321 КЛП (LG 50321 CLP)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.868346+00	2025-10-16 17:29:06.868665+00	2025-10-16 17:29:06.868668+00	88
1081	f	\N	1145	SANDER	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.869153+00	2025-10-16 17:29:06.869428+00	2025-10-16 17:29:06.869431+00	88
1082	f	\N	1144	КОСТАСОЛ КЛ (KOSTASOL CL)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.869931+00	2025-10-16 17:29:06.870191+00	2025-10-16 17:29:06.870193+00	88
1083	f	\N	1143	Токката	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.87071+00	2025-10-16 17:29:06.870966+00	2025-10-16 17:29:06.870968+00	71
1084	f	\N	1142	НСХ 69 (NSH 8269)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.871419+00	2025-10-16 17:29:06.871675+00	2025-10-16 17:29:06.871677+00	88
1085	f	\N	1141	Lunadur	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.872144+00	2025-10-16 17:29:06.872397+00	2025-10-16 17:29:06.872399+00	124
1086	f	\N	1140	Самбадур (Sambadur)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.872904+00	2025-10-16 17:29:06.873164+00	2025-10-16 17:29:06.873166+00	124
1087	f	\N	1139	Теннодур (Tennodur)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.87366+00	2025-10-16 17:29:06.873923+00	2025-10-16 17:29:06.873925+00	124
1088	f	\N	1138	НСХ 8266 (NSH 8266)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.874625+00	2025-10-16 17:29:06.875013+00	2025-10-16 17:29:06.875015+00	88
1089	f	\N	1137	Amandus	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.875602+00	2025-10-16 17:29:06.875924+00	2025-10-16 17:29:06.875927+00	93
1090	f	\N	1136	Мандарин (Mandarin)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.876478+00	2025-10-16 17:29:06.876828+00	2025-10-16 17:29:06.87683+00	93
1091	f	\N	1135	Bernstein	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.877376+00	2025-10-16 17:29:06.877676+00	2025-10-16 17:29:06.877678+00	93
1092	f	\N	1134	Аронио (Aronio)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.878156+00	2025-10-16 17:29:06.878423+00	2025-10-16 17:29:06.878425+00	93
1093	f	\N	1133	НСХ 8149 (NSH 8149)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.878897+00	2025-10-16 17:29:06.879167+00	2025-10-16 17:29:06.87917+00	88
1094	f	\N	1132	Guido	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.879661+00	2025-10-16 17:29:06.879929+00	2025-10-16 17:29:06.879932+00	93
1095	f	\N	1131	Гаудио (Gaudio)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.880401+00	2025-10-16 17:29:06.880676+00	2025-10-16 17:29:06.880678+00	93
1096	f	\N	1130	Монако (Monaco)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.881108+00	2025-10-16 17:29:06.881419+00	2025-10-16 17:29:06.881421+00	93
1097	f	\N	1129	НСХ 8147 (NSH 8147)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.881944+00	2025-10-16 17:29:06.882317+00	2025-10-16 17:29:06.882319+00	88
1099	f	\N	1127	Маурицио (Maurizio)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.88368+00	2025-10-16 17:29:06.883929+00	2025-10-16 17:29:06.883931+00	93
1100	f	\N	1126	Цампано (Zampano)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.884406+00	2025-10-16 17:29:06.884687+00	2025-10-16 17:29:06.88469+00	93
1101	f	\N	1125	Флоренс	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.885192+00	2025-10-16 17:29:06.885459+00	2025-10-16 17:29:06.885461+00	71
1102	f	\N	1124	НСХ 8005 (NSH 8005)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.885917+00	2025-10-16 17:29:06.886173+00	2025-10-16 17:29:06.886175+00	88
1103	f	\N	1123	KIZ-90	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.886681+00	2025-10-16 17:29:06.886944+00	2025-10-16 17:29:06.886946+00	93
1104	f	\N	1122	Әділет	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.887589+00	2025-10-16 17:29:06.887878+00	2025-10-16 17:29:06.88788+00	93
1105	f	\N	1121	НСХ 7822 (NSH 7822)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.888365+00	2025-10-16 17:29:06.888648+00	2025-10-16 17:29:06.88865+00	88
1106	f	\N	1120	Solexis	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.889134+00	2025-10-16 17:29:06.889387+00	2025-10-16 17:29:06.889389+00	88
1107	f	\N	1119	Solexis	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.889934+00	2025-10-16 17:29:06.890201+00	2025-10-16 17:29:06.890203+00	88
1108	f	\N	1118	НСХ 7749 Сумо (NSH 7749 Sumo)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.890676+00	2025-10-16 17:29:06.89103+00	2025-10-16 17:29:06.891033+00	88
1109	f	\N	1117	Ворожея	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.891594+00	2025-10-16 17:29:06.891924+00	2025-10-16 17:29:06.891926+00	71
1110	f	\N	1116	НСХ 7749 (NSH 7749)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.892445+00	2025-10-16 17:29:06.892725+00	2025-10-16 17:29:06.892727+00	88
1111	f	\N	1115	НСХ 6341 (NSH 6341)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.893235+00	2025-10-16 17:29:06.893484+00	2025-10-16 17:29:06.893486+00	88
1112	f	\N	1114	НСХ 6046 (NSH 6046)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.893949+00	2025-10-16 17:29:06.894214+00	2025-10-16 17:29:06.894217+00	88
1113	f	\N	1113	Сыргалым	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.894744+00	2025-10-16 17:29:06.895002+00	2025-10-16 17:29:06.895004+00	76
1114	f	\N	1112	Дамсинский голозерный	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.895459+00	2025-10-16 17:29:06.895738+00	2025-10-16 17:29:06.89574+00	76
1115	f	\N	1111	Урал	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.896229+00	2025-10-16 17:29:06.896495+00	2025-10-16 17:29:06.896497+00	76
1116	f	\N	1110	Иртыш 33	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.896944+00	2025-10-16 17:29:06.897187+00	2025-10-16 17:29:06.897189+00	76
1117	f	\N	1109	Карагандинский 6	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.897643+00	2025-10-16 17:29:06.897908+00	2025-10-16 17:29:06.897911+00	150
1118	f	\N	1108	Карагандинский 23	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.898376+00	2025-10-16 17:29:06.898637+00	2025-10-16 17:29:06.898639+00	150
1119	f	\N	1107	Деспина	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.899254+00	2025-10-16 17:29:06.899574+00	2025-10-16 17:29:06.899576+00	150
1120	f	\N	1106	РАНЕ	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.900116+00	2025-10-16 17:29:06.900388+00	2025-10-16 17:29:06.90039+00	150
1121	f	\N	1105	Абба	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.900907+00	2025-10-16 17:29:06.901188+00	2025-10-16 17:29:06.901191+00	150
1122	f	\N	1104	СТИНГ	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.901706+00	2025-10-16 17:29:06.902008+00	2025-10-16 17:29:06.90201+00	150
1123	f	\N	1103	НС КНЕЗ (NS KNEZ)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.90251+00	2025-10-16 17:29:06.902799+00	2025-10-16 17:29:06.902801+00	88
1124	f	\N	1102	ЭН Акцент	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.903262+00	2025-10-16 17:29:06.90353+00	2025-10-16 17:29:06.903532+00	119
1125	f	\N	1101	НС Оскар (NS Oskar)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.904018+00	2025-10-16 17:29:06.904282+00	2025-10-16 17:29:06.904284+00	88
1126	f	\N	1100	Яик	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.904761+00	2025-10-16 17:29:06.905029+00	2025-10-16 17:29:06.905031+00	150
1127	f	\N	1099	Челябинский 100	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.905525+00	2025-10-16 17:29:06.905828+00	2025-10-16 17:29:06.905831+00	150
1128	f	\N	1098	Медикум 18	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.906305+00	2025-10-16 17:29:06.906559+00	2025-10-16 17:29:06.906561+00	150
1129	f	\N	1097	НСХ 8004 (NSH 8004)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.907001+00	2025-10-16 17:29:06.907368+00	2025-10-16 17:29:06.907371+00	88
1130	f	\N	1096	Аскер	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.907982+00	2025-10-16 17:29:06.908304+00	2025-10-16 17:29:06.908306+00	150
1131	f	\N	1095	Дамсинская 90	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.908778+00	2025-10-16 17:29:06.909017+00	2025-10-16 17:29:06.90902+00	124
1132	f	\N	1094	Омский 96	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.909482+00	2025-10-16 17:29:06.90976+00	2025-10-16 17:29:06.909763+00	150
1133	f	\N	1093	Медикум 18	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.910255+00	2025-10-16 17:29:06.910505+00	2025-10-16 17:29:06.910507+00	150
1134	f	\N	1092	Медикум 18	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.910972+00	2025-10-16 17:29:06.911239+00	2025-10-16 17:29:06.911241+00	150
1135	f	\N	1091	Атлет	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.91174+00	2025-10-16 17:29:06.911991+00	2025-10-16 17:29:06.911994+00	150
1136	f	\N	1090	Искандер	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.912466+00	2025-10-16 17:29:06.912755+00	2025-10-16 17:29:06.912758+00	150
1137	f	\N	1089	Омский 102	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.91323+00	2025-10-16 17:29:06.913531+00	2025-10-16 17:29:06.913533+00	150
1138	f	\N	1088	ЭН Аргумент	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.914053+00	2025-10-16 17:29:06.914317+00	2025-10-16 17:29:06.914319+00	119
1139	f	\N	1087	Торғай	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.9148+00	2025-10-16 17:29:06.915054+00	2025-10-16 17:29:06.915056+00	124
1140	f	\N	1086	ЭН 1107	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.915555+00	2025-10-16 17:29:06.915871+00	2025-10-16 17:29:06.915874+00	119
1141	f	\N	1085	Сәуле	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.916809+00	2025-10-16 17:29:06.917109+00	2025-10-16 17:29:06.917111+00	119
1142	f	\N	1084	Жаз	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.917604+00	2025-10-16 17:29:06.917887+00	2025-10-16 17:29:06.917889+00	119
1143	f	\N	1083	ФД22Б5006	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.918405+00	2025-10-16 17:29:06.918719+00	2025-10-16 17:29:06.918723+00	107
1144	f	\N	1082	Зауральский простор	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.919225+00	2025-10-16 17:29:06.919476+00	2025-10-16 17:29:06.919478+00	93
1145	f	\N	1081	Казахстанская раннеспелая	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.91993+00	2025-10-16 17:29:06.920183+00	2025-10-16 17:29:06.920185+00	93
1146	f	\N	1080	Айым	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.920638+00	2025-10-16 17:29:06.920894+00	2025-10-16 17:29:06.920896+00	93
1147	f	\N	1079	Йолдыз	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.921341+00	2025-10-16 17:29:06.921592+00	2025-10-16 17:29:06.921594+00	93
1148	f	\N	1078	100 ЛЕТ ТАССР	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.922114+00	2025-10-16 17:29:06.922387+00	2025-10-16 17:29:06.922389+00	93
1149	f	\N	1077	ФД22Б5004	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.922853+00	2025-10-16 17:29:06.92312+00	2025-10-16 17:29:06.923122+00	107
1150	f	\N	1076	Омская 35	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.923631+00	2025-10-16 17:29:06.92389+00	2025-10-16 17:29:06.923893+00	93
1151	f	\N	1075	Радуга	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.924474+00	2025-10-16 17:29:06.924776+00	2025-10-16 17:29:06.924779+00	93
1152	f	\N	1074	Токката	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.925276+00	2025-10-16 17:29:06.92557+00	2025-10-16 17:29:06.925572+00	93
1153	f	\N	1073	Синди	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.926099+00	2025-10-16 17:29:06.926364+00	2025-10-16 17:29:06.926366+00	93
1154	f	\N	1072	Регистана	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.926853+00	2025-10-16 17:29:06.92713+00	2025-10-16 17:29:06.927133+00	93
1155	f	\N	1071	Коко	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.927583+00	2025-10-16 17:29:06.92784+00	2025-10-16 17:29:06.927842+00	93
1156	f	\N	1070	Саратовская 68	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.928312+00	2025-10-16 17:29:06.92857+00	2025-10-16 17:29:06.928572+00	93
1157	f	\N	1069	Саратовская 73	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.929055+00	2025-10-16 17:29:06.929318+00	2025-10-16 17:29:06.92932+00	93
1158	f	\N	1068	Саратовская 68	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.929799+00	2025-10-16 17:29:06.930118+00	2025-10-16 17:29:06.930121+00	93
1159	f	\N	1067	Саратовская 76	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.930601+00	2025-10-16 17:29:06.930878+00	2025-10-16 17:29:06.93088+00	93
1160	f	\N	1066	Экада 265	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.931321+00	2025-10-16 17:29:06.931586+00	2025-10-16 17:29:06.931588+00	93
1161	f	\N	1065	Надира	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.932051+00	2025-10-16 17:29:06.932307+00	2025-10-16 17:29:06.93231+00	93
1162	f	\N	1064	ФД Пульс	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.93289+00	2025-10-16 17:29:06.933187+00	2025-10-16 17:29:06.933189+00	107
1163	f	\N	1063	Омская 38	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.933726+00	2025-10-16 17:29:06.934006+00	2025-10-16 17:29:06.934009+00	93
1164	f	\N	1062	Омская 45	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.934509+00	2025-10-16 17:29:06.934813+00	2025-10-16 17:29:06.934815+00	93
1165	f	\N	1061	Омская 38	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.935297+00	2025-10-16 17:29:06.935538+00	2025-10-16 17:29:06.93554+00	93
1166	f	\N	1060	Омская 44	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.936013+00	2025-10-16 17:29:06.936266+00	2025-10-16 17:29:06.936268+00	93
1167	f	\N	1059	Елена	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.936764+00	2025-10-16 17:29:06.937013+00	2025-10-16 17:29:06.937015+00	150
1168	f	\N	1058	Эдельмира (Edelmira)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.937456+00	2025-10-16 17:29:06.937735+00	2025-10-16 17:29:06.937737+00	150
1169	f	\N	1057	Целинный голозерный	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.938192+00	2025-10-16 17:29:06.938462+00	2025-10-16 17:29:06.938464+00	150
1170	f	\N	1056	Сочинский голозерный	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.938947+00	2025-10-16 17:29:06.939193+00	2025-10-16 17:29:06.939195+00	150
1171	f	\N	1055	Эксплоер	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.939672+00	2025-10-16 17:29:06.939937+00	2025-10-16 17:29:06.939939+00	149
1172	f	\N	1054	Рапид (Rapid)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.940391+00	2025-10-16 17:29:06.940679+00	2025-10-16 17:29:06.940681+00	150
1173	f	\N	1053	Сыр аруы	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.94134+00	2025-10-16 17:29:06.941639+00	2025-10-16 17:29:06.941641+00	150
1174	f	\N	1052	Дамир	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.942177+00	2025-10-16 17:29:06.942434+00	2025-10-16 17:29:06.942436+00	150
1175	f	\N	1051	Бонидуро	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.942903+00	2025-10-16 17:29:06.943144+00	2025-10-16 17:29:06.943146+00	124
1176	f	\N	1050	Рамидур (Ramidur)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.943601+00	2025-10-16 17:29:06.943872+00	2025-10-16 17:29:06.943874+00	124
1177	f	\N	1049	Каргала 71	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.944349+00	2025-10-16 17:29:06.944599+00	2025-10-16 17:29:06.944601+00	124
1178	f	\N	1048	Янтарная 160	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.945266+00	2025-10-16 17:29:06.945515+00	2025-10-16 17:29:06.945517+00	124
1179	f	\N	1047	Росадур	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.945975+00	2025-10-16 17:29:06.946237+00	2025-10-16 17:29:06.946239+00	124
1180	f	\N	1046	Видеодур (Videodur)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.946708+00	2025-10-16 17:29:06.946968+00	2025-10-16 17:29:06.94697+00	124
1181	f	\N	1045	Пинкджейн	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.947433+00	2025-10-16 17:29:06.947703+00	2025-10-16 17:29:06.947705+00	126
1182	f	\N	1044	Айна	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.948195+00	2025-10-16 17:29:06.948472+00	2025-10-16 17:29:06.948474+00	93
1183	f	\N	1043	Айна	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.94896+00	2025-10-16 17:29:06.949205+00	2025-10-16 17:29:06.949207+00	93
1184	f	\N	1042	Кордай	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.949672+00	2025-10-16 17:29:06.949941+00	2025-10-16 17:29:06.949943+00	93
1185	f	\N	1041	Байтерек 22	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.950415+00	2025-10-16 17:29:06.950686+00	2025-10-16 17:29:06.950689+00	88
1186	f	\N	1040	Інжу	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.95117+00	2025-10-16 17:29:06.95143+00	2025-10-16 17:29:06.951432+00	93
1187	f	\N	1039	БГ Унистар	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.951905+00	2025-10-16 17:29:06.952177+00	2025-10-16 17:29:06.952179+00	93
1188	f	\N	1038	БГ Икона 2с	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.952665+00	2025-10-16 17:29:06.952949+00	2025-10-16 17:29:06.952952+00	93
1189	f	\N	1037	Экселент	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.953433+00	2025-10-16 17:29:06.953719+00	2025-10-16 17:29:06.953721+00	88
1190	f	\N	1036	БГ Фенома	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.954161+00	2025-10-16 17:29:06.954405+00	2025-10-16 17:29:06.954407+00	93
1191	f	\N	1035	БГ Логика	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.954875+00	2025-10-16 17:29:06.955147+00	2025-10-16 17:29:06.955149+00	93
1192	f	\N	1034	КВС Экспектум	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.955601+00	2025-10-16 17:29:06.955882+00	2025-10-16 17:29:06.955884+00	93
1193	f	\N	1033	Чаглинская 23	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.956377+00	2025-10-16 17:29:06.956702+00	2025-10-16 17:29:06.956705+00	93
1194	f	\N	1032	КВС Карусум	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.957389+00	2025-10-16 17:29:06.957725+00	2025-10-16 17:29:06.957727+00	93
1195	f	\N	1031	Санарис	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.958217+00	2025-10-16 17:29:06.958468+00	2025-10-16 17:29:06.95847+00	88
1196	f	\N	1030	Дурофинус	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.958965+00	2025-10-16 17:29:06.959261+00	2025-10-16 17:29:06.959264+00	123
1197	f	\N	1029	Тессадур	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.959796+00	2025-10-16 17:29:06.96006+00	2025-10-16 17:29:06.960062+00	123
1198	f	\N	1028	Гранни	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.960524+00	2025-10-16 17:29:06.960809+00	2025-10-16 17:29:06.960811+00	71
1199	f	\N	1027	Северное сияние	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.961271+00	2025-10-16 17:29:06.961521+00	2025-10-16 17:29:06.961523+00	119
1200	f	\N	1026	Хайленд	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.962064+00	2025-10-16 17:29:06.962346+00	2025-10-16 17:29:06.962349+00	149
1201	f	\N	1025	Сәулетай	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.962832+00	2025-10-16 17:29:06.963081+00	2025-10-16 17:29:06.963083+00	88
1202	f	\N	1024	ЕСХ 91753	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.963538+00	2025-10-16 17:29:06.963845+00	2025-10-16 17:29:06.963847+00	88
1203	f	\N	1023	ЕСХ 21106	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.964312+00	2025-10-16 17:29:06.964563+00	2025-10-16 17:29:06.964565+00	88
1204	f	\N	1022	КСФ 21084	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.965063+00	2025-10-16 17:29:06.965321+00	2025-10-16 17:29:06.965323+00	88
1205	f	\N	1021	M94S35	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.965795+00	2025-10-16 17:29:06.966057+00	2025-10-16 17:29:06.966059+00	88
1206	f	\N	1020	M96CLP51	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.966551+00	2025-10-16 17:29:06.966827+00	2025-10-16 17:29:06.966829+00	88
1207	f	\N	1019	МАС 83СУ	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.967289+00	2025-10-16 17:29:06.967559+00	2025-10-16 17:29:06.967561+00	88
1208	f	\N	1018	СВ 3807 ВТ	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.968034+00	2025-10-16 17:29:06.968297+00	2025-10-16 17:29:06.968299+00	5
1209	f	\N	1017	Асай	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.968783+00	2025-10-16 17:29:06.969087+00	2025-10-16 17:29:06.969089+00	55
1210	f	\N	1016	Улан 43	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.96958+00	2025-10-16 17:29:06.969858+00	2025-10-16 17:29:06.969861+00	71
1211	f	\N	1015	Тан	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.970336+00	2025-10-16 17:29:06.970592+00	2025-10-16 17:29:06.970594+00	119
1212	f	\N	1014	Бомбикс	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.971064+00	2025-10-16 17:29:06.971339+00	2025-10-16 17:29:06.971342+00	5
1213	f	\N	1013	Батыс 4	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.971817+00	2025-10-16 17:29:06.972066+00	2025-10-16 17:29:06.972068+00	35
1214	f	\N	1012	Лг Тосса (LG Tosca)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.972533+00	2025-10-16 17:29:06.972826+00	2025-10-16 17:29:06.972828+00	149
1215	f	\N	1011	Дамсинская 20-17	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.973291+00	2025-10-16 17:29:06.973541+00	2025-10-16 17:29:06.973543+00	123
1216	f	\N	1010	Ишимская 9	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.974187+00	2025-10-16 17:29:06.974456+00	2025-10-16 17:29:06.974458+00	71
1217	f	\N	1009	Балшырын	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.974946+00	2025-10-16 17:29:06.975202+00	2025-10-16 17:29:06.975204+00	32
1218	f	\N	1008	Госеул (Goseul)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.975679+00	2025-10-16 17:29:06.97593+00	2025-10-16 17:29:06.975932+00	37
1219	f	\N	1007	FC13-122	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.976399+00	2025-10-16 17:29:06.976708+00	2025-10-16 17:29:06.97671+00	19
1220	f	\N	1006	Мактаарал-5035	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.977231+00	2025-10-16 17:29:06.977493+00	2025-10-16 17:29:06.977495+00	133
1221	f	\N	1005	Отар 2022	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.977982+00	2025-10-16 17:29:06.978246+00	2025-10-16 17:29:06.978248+00	149
1222	f	\N	1004	Карабалыкский 22	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.978735+00	2025-10-16 17:29:06.978987+00	2025-10-16 17:29:06.978989+00	149
1223	f	\N	1003	Жасөркен	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.979443+00	2025-10-16 17:29:06.979729+00	2025-10-16 17:29:06.979731+00	149
1224	f	\N	1002	Болашақ	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.980186+00	2025-10-16 17:29:06.98044+00	2025-10-16 17:29:06.980442+00	107
1225	f	\N	1001	Хазрет	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.98096+00	2025-10-16 17:29:06.981245+00	2025-10-16 17:29:06.981247+00	71
1226	f	\N	1000	Токаш	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.981743+00	2025-10-16 17:29:06.982007+00	2025-10-16 17:29:06.982009+00	71
1227	f	\N	999	Рагнарр	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.982475+00	2025-10-16 17:29:06.982755+00	2025-10-16 17:29:06.982757+00	97
1228	f	\N	998	Искандер	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.983211+00	2025-10-16 17:29:06.983477+00	2025-10-16 17:29:06.983479+00	35
1229	f	\N	997	Карагандинская юбилейная	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.983965+00	2025-10-16 17:29:06.984225+00	2025-10-16 17:29:06.984227+00	71
1230	f	\N	996	Хан-Тенгри	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.984709+00	2025-10-16 17:29:06.984992+00	2025-10-16 17:29:06.984994+00	71
1231	f	\N	995	Сәтті	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.985599+00	2025-10-16 17:29:06.985988+00	2025-10-16 17:29:06.98599+00	74
1232	f	\N	994	Ер-сұлтан	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.986575+00	2025-10-16 17:29:06.986879+00	2025-10-16 17:29:06.986881+00	74
1233	f	\N	993	Алия Молдагулова	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.987457+00	2025-10-16 17:29:06.987764+00	2025-10-16 17:29:06.987766+00	79
1234	f	\N	992	Дагус	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.988299+00	2025-10-16 17:29:06.988557+00	2025-10-16 17:29:06.988559+00	20
1235	f	\N	991	Cordesso (Кордессо)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.989017+00	2025-10-16 17:29:06.989277+00	2025-10-16 17:29:06.989279+00	54
1236	f	\N	990	Marcamo (Маркамо)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.989788+00	2025-10-16 17:29:06.990143+00	2025-10-16 17:29:06.990147+00	54
1237	f	\N	989	Лумп (Lump)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.990734+00	2025-10-16 17:29:06.991037+00	2025-10-16 17:29:06.99104+00	20
1238	f	\N	988	FC13-083	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.991542+00	2025-10-16 17:29:06.991837+00	2025-10-16 17:29:06.991839+00	19
1239	f	\N	987	Грант	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.992311+00	2025-10-16 17:29:06.992572+00	2025-10-16 17:29:06.992574+00	5
1240	f	\N	986	Спартак	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.993035+00	2025-10-16 17:29:06.993288+00	2025-10-16 17:29:06.993291+00	149
1241	f	\N	985	Припять	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.993765+00	2025-10-16 17:29:06.994045+00	2025-10-16 17:29:06.994047+00	119
1242	f	\N	984	Волма	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.994546+00	2025-10-16 17:29:06.994831+00	2025-10-16 17:29:06.994833+00	119
1243	f	\N	983	Ершовский 5	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.995528+00	2025-10-16 17:29:06.995788+00	2025-10-16 17:29:06.995791+00	117
1244	f	\N	981	Екатериновская	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.996264+00	2025-10-16 17:29:06.996511+00	2025-10-16 17:29:06.996513+00	141
1245	f	\N	980	нут	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.996948+00	2025-10-16 17:29:06.997211+00	2025-10-16 17:29:06.997213+00	74
1246	f	\N	979	Мактаарал-5040	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.997695+00	2025-10-16 17:29:06.997978+00	2025-10-16 17:29:06.99798+00	133
1247	f	\N	978	Мактаарал 3047	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.998473+00	2025-10-16 17:29:06.998753+00	2025-10-16 17:29:06.998755+00	133
1248	f	\N	977	Мактаарал 3047	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:06.999288+00	2025-10-16 17:29:06.999639+00	2025-10-16 17:29:06.999643+00	107
1249	f	\N	974	Мактаарал- 5030	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.000198+00	2025-10-16 17:29:07.000471+00	2025-10-16 17:29:07.000473+00	133
1250	f	\N	961	Достык 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.000959+00	2025-10-16 17:29:07.001202+00	2025-10-16 17:29:07.001204+00	71
1251	f	\N	960	Таймас	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.0017+00	2025-10-16 17:29:07.00198+00	2025-10-16 17:29:07.001982+00	71
1252	f	\N	959	Гранни (Granny)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.002419+00	2025-10-16 17:29:07.002676+00	2025-10-16 17:29:07.002678+00	71
1253	f	\N	958	Красноуральская	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.003144+00	2025-10-16 17:29:07.0034+00	2025-10-16 17:29:07.003402+00	71
1254	f	\N	957	Дарко (1)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.003873+00	2025-10-16 17:29:07.004122+00	2025-10-16 17:29:07.004124+00	60
1255	f	\N	956	Барусо (1)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.004589+00	2025-10-16 17:29:07.004865+00	2025-10-16 17:29:07.004867+00	60
1256	f	\N	955	ГРАНТ (1)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.005335+00	2025-10-16 17:29:07.005623+00	2025-10-16 17:29:07.005625+00	5
1257	f	\N	954	Соната Полтавська	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.006102+00	2025-10-16 17:29:07.006363+00	2025-10-16 17:29:07.006366+00	71
1258	f	\N	953	Санжара	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.006836+00	2025-10-16 17:29:07.007102+00	2025-10-16 17:29:07.007104+00	71
1259	f	\N	952	Самара 2	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.007595+00	2025-10-16 17:29:07.007884+00	2025-10-16 17:29:07.007886+00	71
1260	f	\N	951	Ятоба 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.008353+00	2025-10-16 17:29:07.008601+00	2025-10-16 17:29:07.008603+00	60
1261	f	\N	950	Каоба 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.00909+00	2025-10-16 17:29:07.00934+00	2025-10-16 17:29:07.009342+00	60
1262	f	\N	949	Ногал 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.009831+00	2025-10-16 17:29:07.010109+00	2025-10-16 17:29:07.010111+00	60
1263	f	\N	948	Сентоза 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.010583+00	2025-10-16 17:29:07.010852+00	2025-10-16 17:29:07.010855+00	126
1264	f	\N	947	КИЗ-2020	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.011324+00	2025-10-16 17:29:07.011583+00	2025-10-16 17:29:07.011585+00	149
1265	f	\N	946	Бехрам 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.012078+00	2025-10-16 17:29:07.012335+00	2025-10-16 17:29:07.012337+00	126
1266	f	\N	945	Несіпхан	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.012848+00	2025-10-16 17:29:07.013104+00	2025-10-16 17:29:07.013106+00	71
1267	f	\N	944	Брандино	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.013549+00	2025-10-16 17:29:07.013824+00	2025-10-16 17:29:07.013826+00	79
1268	f	\N	943	Свифтер	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.014257+00	2025-10-16 17:29:07.014508+00	2025-10-16 17:29:07.01451+00	97
1269	f	\N	942	ЕВКЛИД	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.014991+00	2025-10-16 17:29:07.015281+00	2025-10-16 17:29:07.015283+00	71
1270	f	\N	941	Мөлдір 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.015797+00	2025-10-16 17:29:07.016201+00	2025-10-16 17:29:07.016203+00	88
1271	f	\N	940	N4H161Cl(1)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.016751+00	2025-10-16 17:29:07.017037+00	2025-10-16 17:29:07.017039+00	88
1272	f	\N	939	Евразия-1(1)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.01752+00	2025-10-16 17:29:07.017804+00	2025-10-16 17:29:07.017806+00	88
1273	f	\N	938	НХ 01163	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.018503+00	2025-10-16 17:29:07.018789+00	2025-10-16 17:29:07.018791+00	88
1274	f	\N	936	Вираж (1)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.019257+00	2025-10-16 17:29:07.019508+00	2025-10-16 17:29:07.01951+00	149
1275	f	\N	935	Династия 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.019955+00	2025-10-16 17:29:07.020214+00	2025-10-16 17:29:07.020216+00	71
1276	f	\N	932	Альтаир 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.020686+00	2025-10-16 17:29:07.020944+00	2025-10-16 17:29:07.020947+00	71
1277	f	\N	931	Людмила (1)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.021397+00	2025-10-16 17:29:07.021665+00	2025-10-16 17:29:07.021667+00	71
1278	f	\N	930	Татьяна 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.022131+00	2025-10-16 17:29:07.022384+00	2025-10-16 17:29:07.022386+00	71
1279	f	\N	929	Людмила	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.022842+00	2025-10-16 17:29:07.023112+00	2025-10-16 17:29:07.023115+00	71
1280	f	\N	928	Жақұт-20	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.023577+00	2025-10-16 17:29:07.023867+00	2025-10-16 17:29:07.023869+00	123
1281	f	\N	927	Голозерный 62 (1)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.024324+00	2025-10-16 17:29:07.024569+00	2025-10-16 17:29:07.024571+00	149
1282	f	\N	925	Омский коралл	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.025041+00	2025-10-16 17:29:07.025304+00	2025-10-16 17:29:07.025306+00	123
1283	f	\N	924	Снигурка	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.025798+00	2025-10-16 17:29:07.026066+00	2025-10-16 17:29:07.026068+00	71
1284	f	\N	923	Силач 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.026514+00	2025-10-16 17:29:07.0268+00	2025-10-16 17:29:07.026803+00	71
1285	f	\N	922	Момышұлы	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.027269+00	2025-10-16 17:29:07.027539+00	2025-10-16 17:29:07.027541+00	71
1286	f	\N	921	ОС14-16.32	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.028005+00	2025-10-16 17:29:07.028276+00	2025-10-16 17:29:07.028278+00	149
1287	f	\N	920	БС15-750	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.028752+00	2025-10-16 17:29:07.029013+00	2025-10-16 17:29:07.029016+00	71
1288	f	\N	919	ОС15-908(1)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.029459+00	2025-10-16 17:29:07.029767+00	2025-10-16 17:29:07.02977+00	149
1289	f	\N	918	Приуральня	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.030244+00	2025-10-16 17:29:07.030517+00	2025-10-16 17:29:07.030519+00	71
1290	f	\N	917	Карагандинский 20 (1)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.031168+00	2025-10-16 17:29:07.031446+00	2025-10-16 17:29:07.031449+00	149
1291	f	\N	916	Карагандинская 55	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.031903+00	2025-10-16 17:29:07.032153+00	2025-10-16 17:29:07.032155+00	71
1292	f	\N	915	Кеноби (1)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.032639+00	2025-10-16 17:29:07.032887+00	2025-10-16 17:29:07.032889+00	123
1293	f	\N	914	Кеноби (1)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.033351+00	2025-10-16 17:29:07.03359+00	2025-10-16 17:29:07.033592+00	123
1294	f	\N	913	ЛГ Бельканто 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.034091+00	2025-10-16 17:29:07.034345+00	2025-10-16 17:29:07.034347+00	149
1295	f	\N	912	Кеноби	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.034817+00	2025-10-16 17:29:07.035079+00	2025-10-16 17:29:07.035081+00	123
1296	f	\N	911	Теодорико	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.035549+00	2025-10-16 17:29:07.035832+00	2025-10-16 17:29:07.035834+00	123
1297	f	\N	910	Лютесценс 346-9	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.036292+00	2025-10-16 17:29:07.036537+00	2025-10-16 17:29:07.036539+00	71
1298	f	\N	909	Кабото	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.036982+00	2025-10-16 17:29:07.037242+00	2025-10-16 17:29:07.037244+00	123
1299	f	\N	908	Тингер	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.03774+00	2025-10-16 17:29:07.038018+00	2025-10-16 17:29:07.03802+00	71
1300	f	\N	907	МАХАОН КЛП	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.038486+00	2025-10-16 17:29:07.038755+00	2025-10-16 17:29:07.038757+00	88
1301	f	\N	906	СВЕТЛАНА КЛП	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.039216+00	2025-10-16 17:29:07.039464+00	2025-10-16 17:29:07.039466+00	88
1302	f	\N	905	Рейна (1)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.039943+00	2025-10-16 17:29:07.040194+00	2025-10-16 17:29:07.040197+00	88
1303	f	\N	904	ЕСХ 8019 (1)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.040676+00	2025-10-16 17:29:07.040938+00	2025-10-16 17:29:07.04094+00	88
1304	f	\N	903	ECX8118	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.04139+00	2025-10-16 17:29:07.041651+00	2025-10-16 17:29:07.041654+00	88
1305	f	\N	901	ЕСХ 9153 (1)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.042139+00	2025-10-16 17:29:07.042394+00	2025-10-16 17:29:07.042396+00	88
1306	f	\N	900	NX03272	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.042865+00	2025-10-16 17:29:07.043116+00	2025-10-16 17:29:07.043118+00	88
1307	f	\N	899	Асыл-Айым (1)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.043574+00	2025-10-16 17:29:07.043825+00	2025-10-16 17:29:07.043827+00	146
1308	f	\N	898	ОБФ0622	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.044316+00	2025-10-16 17:29:07.044573+00	2025-10-16 17:29:07.044575+00	19
1309	f	\N	897	Зебри-85 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.045059+00	2025-10-16 17:29:07.045316+00	2025-10-16 17:29:07.045318+00	51
1310	f	\N	896	Уральский самоцвет	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.045819+00	2025-10-16 17:29:07.046072+00	2025-10-16 17:29:07.046074+00	144
1311	f	\N	895	ZF08-070 (1)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.046727+00	2025-10-16 17:29:07.046988+00	2025-10-16 17:29:07.046991+00	19
1312	f	\N	894	Деркульский 150 СВ (1)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.047471+00	2025-10-16 17:29:07.047737+00	2025-10-16 17:29:07.047739+00	54
1313	f	\N	893	Северо-Западная 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.048212+00	2025-10-16 17:29:07.048458+00	2025-10-16 17:29:07.04846+00	61
1314	f	\N	892	Таскалинский (1)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.048923+00	2025-10-16 17:29:07.049185+00	2025-10-16 17:29:07.049187+00	35
1315	f	\N	891	Батыс (1)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.049646+00	2025-10-16 17:29:07.049914+00	2025-10-16 17:29:07.049916+00	35
1316	f	\N	890	Первенец Семиречья (1)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.050372+00	2025-10-16 17:29:07.050634+00	2025-10-16 17:29:07.050637+00	97
1317	f	\N	889	Сантиана 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.051109+00	2025-10-16 17:29:07.05136+00	2025-10-16 17:29:07.051362+00	126
1318	f	\N	888	Искен	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.051828+00	2025-10-16 17:29:07.052075+00	2025-10-16 17:29:07.052077+00	51
1319	f	\N	887	Медовый 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.052549+00	2025-10-16 17:29:07.052851+00	2025-10-16 17:29:07.052853+00	31
1320	f	\N	886	Нектарный -30	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.053314+00	2025-10-16 17:29:07.053558+00	2025-10-16 17:29:07.05356+00	144
1321	f	\N	885	Питерка	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.054068+00	2025-10-16 17:29:07.054325+00	2025-10-16 17:29:07.054328+00	121
1692	f	\N	507	Лавина	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.329682+00	2025-10-16 17:29:07.329952+00	2025-10-16 17:29:07.329954+00	123
1322	f	\N	884	Дергачевский	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.054803+00	2025-10-16 17:29:07.055066+00	2025-10-16 17:29:07.055069+00	115
1323	f	\N	883	Ершовский 5 (1)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.055562+00	2025-10-16 17:29:07.055845+00	2025-10-16 17:29:07.055847+00	115
1324	f	\N	882	Бақбарыс (1)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.056299+00	2025-10-16 17:29:07.056561+00	2025-10-16 17:29:07.056563+00	16
1325	f	\N	881	Інжу-Маржан (1)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.057039+00	2025-10-16 17:29:07.057297+00	2025-10-16 17:29:07.057299+00	137
1326	f	\N	880	Юбилейная Котухова	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.057774+00	2025-10-16 17:29:07.058037+00	2025-10-16 17:29:07.058039+00	75
1327	f	\N	879	ЕСХ 19153 (1)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.05849+00	2025-10-16 17:29:07.058746+00	2025-10-16 17:29:07.058748+00	88
1328	f	\N	878	ECX 99538	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.059194+00	2025-10-16 17:29:07.059454+00	2025-10-16 17:29:07.059456+00	88
1329	f	\N	877	N4L102CL (1)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.059944+00	2025-10-16 17:29:07.060219+00	2025-10-16 17:29:07.060221+00	88
1330	f	\N	876	ЛГ50480	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.060713+00	2025-10-16 17:29:07.060958+00	2025-10-16 17:29:07.06096+00	88
1331	f	\N	875	ARLAN	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.061403+00	2025-10-16 17:29:07.061676+00	2025-10-16 17:29:07.061679+00	88
1332	f	\N	874	ЛГ 50529	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.062128+00	2025-10-16 17:29:07.062377+00	2025-10-16 17:29:07.062379+00	88
1333	f	\N	873	ЛГ 50455 КЛП (1)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.06283+00	2025-10-16 17:29:07.063081+00	2025-10-16 17:29:07.063083+00	88
1334	f	\N	872	ЛГ50479	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.063527+00	2025-10-16 17:29:07.063796+00	2025-10-16 17:29:07.063798+00	88
1335	f	\N	871	ПЖР-Н13-135 (1)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.064216+00	2025-10-16 17:29:07.064463+00	2025-10-16 17:29:07.064465+00	76
1336	f	\N	870	Сабросо F1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.064928+00	2025-10-16 17:29:07.065183+00	2025-10-16 17:29:07.065185+00	60
1337	f	\N	869	Гадис 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.065665+00	2025-10-16 17:29:07.06593+00	2025-10-16 17:29:07.065932+00	71
1338	f	\N	868	Жалгас 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.066384+00	2025-10-16 17:29:07.066657+00	2025-10-16 17:29:07.06666+00	149
1339	f	\N	867	Сыргалым 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.067128+00	2025-10-16 17:29:07.06738+00	2025-10-16 17:29:07.067382+00	76
1340	f	\N	866	РЖТ Планет  1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.067871+00	2025-10-16 17:29:07.06813+00	2025-10-16 17:29:07.068133+00	149
1341	f	\N	865	Десант 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.068602+00	2025-10-16 17:29:07.068873+00	2025-10-16 17:29:07.068875+00	76
1342	f	\N	864	Вайнах	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.069346+00	2025-10-16 17:29:07.069597+00	2025-10-16 17:29:07.069599+00	149
1343	f	\N	863	Любава 25	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.070083+00	2025-10-16 17:29:07.070361+00	2025-10-16 17:29:07.070363+00	71
1344	f	\N	862	Уралосибирская 2  1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.070852+00	2025-10-16 17:29:07.07111+00	2025-10-16 17:29:07.071112+00	71
1345	f	\N	861	Өскемен	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.071581+00	2025-10-16 17:29:07.071844+00	2025-10-16 17:29:07.071847+00	103
1346	f	\N	860	Фируза 40	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.072293+00	2025-10-16 17:29:07.072543+00	2025-10-16 17:29:07.072545+00	71
1347	f	\N	859	Курьер	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.073016+00	2025-10-16 17:29:07.073282+00	2025-10-16 17:29:07.073285+00	71
1348	f	\N	858	Атлас	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.073757+00	2025-10-16 17:29:07.074014+00	2025-10-16 17:29:07.074016+00	71
1349	f	\N	857	Бесагаш	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.074491+00	2025-10-16 17:29:07.074767+00	2025-10-16 17:29:07.074769+00	71
1350	f	\N	856	Сеймур 17	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.07539+00	2025-10-16 17:29:07.075673+00	2025-10-16 17:29:07.075675+00	123
1351	f	\N	855	Костанайская 207	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.07615+00	2025-10-16 17:29:07.076401+00	2025-10-16 17:29:07.076404+00	123
1352	f	\N	854	Алабуга	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.076879+00	2025-10-16 17:29:07.077149+00	2025-10-16 17:29:07.077152+00	71
1353	f	\N	853	Нур-38	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.077636+00	2025-10-16 17:29:07.077904+00	2025-10-16 17:29:07.077906+00	71
1354	f	\N	852	Вавилов	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.078374+00	2025-10-16 17:29:07.078634+00	2025-10-16 17:29:07.078636+00	71
1355	f	\N	851	Дәурен	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.079099+00	2025-10-16 17:29:07.079347+00	2025-10-16 17:29:07.07935+00	127
1356	f	\N	850	Семёновна	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.079817+00	2025-10-16 17:29:07.080067+00	2025-10-16 17:29:07.080069+00	71
1357	f	\N	849	Димаш	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.080522+00	2025-10-16 17:29:07.080779+00	2025-10-16 17:29:07.080781+00	71
1358	f	\N	848	КС Форвард	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.081274+00	2025-10-16 17:29:07.08153+00	2025-10-16 17:29:07.081532+00	71
1359	f	\N	847	Кудесник 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.082171+00	2025-10-16 17:29:07.082428+00	2025-10-16 17:29:07.08243+00	149
1360	f	\N	846	Икар	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.082898+00	2025-10-16 17:29:07.083151+00	2025-10-16 17:29:07.083153+00	71
1361	f	\N	845	Гернада	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.083709+00	2025-10-16 17:29:07.08396+00	2025-10-16 17:29:07.083962+00	71
1362	f	\N	844	АВИАДа	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.084429+00	2025-10-16 17:29:07.08469+00	2025-10-16 17:29:07.084692+00	71
1363	f	\N	843	КС Гарант 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.085156+00	2025-10-16 17:29:07.085404+00	2025-10-16 17:29:07.085406+00	71
1364	f	\N	842	Апексус (Apexus)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.085899+00	2025-10-16 17:29:07.086156+00	2025-10-16 17:29:07.086158+00	123
1365	f	\N	841	ЦЛБ08-008.008 (CLB085-008.008)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.086621+00	2025-10-16 17:29:07.086884+00	2025-10-16 17:29:07.086886+00	71
1366	f	\N	840	Ача 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.08733+00	2025-10-16 17:29:07.087579+00	2025-10-16 17:29:07.087581+00	149
1367	f	\N	839	ЦЛО06-025.025 (CLO06-025.025)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.08801+00	2025-10-16 17:29:07.088256+00	2025-10-16 17:29:07.088258+00	149
1368	f	\N	838	Зауральский янтарь	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.08871+00	2025-10-16 17:29:07.088966+00	2025-10-16 17:29:07.088968+00	71
1369	f	\N	837	ЦЛО06-053.088 (CLO06-053.088)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.089423+00	2025-10-16 17:29:07.089698+00	2025-10-16 17:29:07.0897+00	149
1370	f	\N	836	Новосибирская 31	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.090171+00	2025-10-16 17:29:07.090422+00	2025-10-16 17:29:07.090424+00	71
1371	f	\N	835	Новосибирская 75	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.090889+00	2025-10-16 17:29:07.091137+00	2025-10-16 17:29:07.091139+00	71
1372	f	\N	834	Фатима 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.091607+00	2025-10-16 17:29:07.09188+00	2025-10-16 17:29:07.091882+00	149
1373	f	\N	833	Сварог	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.092343+00	2025-10-16 17:29:07.092598+00	2025-10-16 17:29:07.0926+00	71
1374	f	\N	832	Собербаш	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.093069+00	2025-10-16 17:29:07.093316+00	2025-10-16 17:29:07.093318+00	71
1375	f	\N	831	Темирязевка 150	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.093763+00	2025-10-16 17:29:07.094022+00	2025-10-16 17:29:07.094024+00	71
1376	f	\N	830	Оазис 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.094484+00	2025-10-16 17:29:07.094751+00	2025-10-16 17:29:07.094753+00	123
1377	f	\N	829	Гомер	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.095222+00	2025-10-16 17:29:07.095486+00	2025-10-16 17:29:07.095489+00	71
1378	f	\N	828	Шукшинка 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.095951+00	2025-10-16 17:29:07.096214+00	2025-10-16 17:29:07.096216+00	123
1379	f	\N	827	Классика	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.096698+00	2025-10-16 17:29:07.096983+00	2025-10-16 17:29:07.096985+00	71
1380	f	\N	826	Ясенка 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.097473+00	2025-10-16 17:29:07.097758+00	2025-10-16 17:29:07.09776+00	123
1381	f	\N	825	Керемет 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.098228+00	2025-10-16 17:29:07.098491+00	2025-10-16 17:29:07.098493+00	71
1382	f	\N	824	Тая 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.098946+00	2025-10-16 17:29:07.09921+00	2025-10-16 17:29:07.099212+00	71
1383	f	\N	823	Азия 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.099668+00	2025-10-16 17:29:07.099925+00	2025-10-16 17:29:07.099927+00	37
1384	f	\N	822	КАНЮК (KANYUK)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.100366+00	2025-10-16 17:29:07.100643+00	2025-10-16 17:29:07.100645+00	71
1385	f	\N	821	Алба 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.101088+00	2025-10-16 17:29:07.10134+00	2025-10-16 17:29:07.101342+00	37
1386	f	\N	820	Патриция (Patricia)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.101815+00	2025-10-16 17:29:07.10207+00	2025-10-16 17:29:07.102073+00	71
1387	f	\N	819	Дән	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.102509+00	2025-10-16 17:29:07.102786+00	2025-10-16 17:29:07.102788+00	71
1388	f	\N	818	Боунтис 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.103439+00	2025-10-16 17:29:07.103734+00	2025-10-16 17:29:07.103737+00	126
1389	f	\N	817	Отм трежа (Autumn Treasure)  1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.104211+00	2025-10-16 17:29:07.10446+00	2025-10-16 17:29:07.104462+00	63
1390	f	\N	816	Октавия (Octavia)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.104945+00	2025-10-16 17:29:07.105211+00	2025-10-16 17:29:07.105214+00	63
1391	f	\N	815	Маллинг Джуно (Malling Juno) 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.105742+00	2025-10-16 17:29:07.106013+00	2025-10-16 17:29:07.106015+00	63
1392	f	\N	814	Партова 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.10648+00	2025-10-16 17:29:07.106754+00	2025-10-16 17:29:07.106756+00	126
1393	f	\N	813	Джоан Джей (Joan J) 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.107216+00	2025-10-16 17:29:07.107463+00	2025-10-16 17:29:07.107465+00	63
1394	f	\N	812	Омалос  1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.107947+00	2025-10-16 17:29:07.108231+00	2025-10-16 17:29:07.108233+00	40
1395	f	\N	811	Ред Хэвен 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.10869+00	2025-10-16 17:29:07.108963+00	2025-10-16 17:29:07.108965+00	5
1396	f	\N	810	Хакимару 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.10943+00	2025-10-16 17:29:07.109707+00	2025-10-16 17:29:07.109709+00	126
1397	f	\N	809	Миннесота 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.110213+00	2025-10-16 17:29:07.110469+00	2025-10-16 17:29:07.110471+00	60
1398	f	\N	808	ПЛБАР Б1 (PLBAR B1)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.110942+00	2025-10-16 17:29:07.111213+00	2025-10-16 17:29:07.111215+00	146
1399	f	\N	807	Емдәмдік картоп 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.111683+00	2025-10-16 17:29:07.111933+00	2025-10-16 17:29:07.111935+00	43
1400	f	\N	806	Глауко-Мильтурум-КК2	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.11243+00	2025-10-16 17:29:07.112808+00	2025-10-16 17:29:07.11281+00	71
1401	f	\N	805	Кихаре ньюс	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.113275+00	2025-10-16 17:29:07.113549+00	2025-10-16 17:29:07.113552+00	71
1402	f	\N	804	Велютинум-инфлатум-КК1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.114021+00	2025-10-16 17:29:07.11428+00	2025-10-16 17:29:07.114282+00	71
1403	f	\N	803	Семеновна 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.114762+00	2025-10-16 17:29:07.115017+00	2025-10-16 17:29:07.115019+00	71
1404	f	\N	802	Подарок Нуртазиной1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.115482+00	2025-10-16 17:29:07.115759+00	2025-10-16 17:29:07.115761+00	146
1405	f	\N	801	Нұрлы-80 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.116226+00	2025-10-16 17:29:07.116476+00	2025-10-16 17:29:07.116478+00	74
1406	f	\N	800	Остинато 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.116965+00	2025-10-16 17:29:07.117217+00	2025-10-16 17:29:07.117219+00	20
1407	f	\N	799	Оркеш 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.11771+00	2025-10-16 17:29:07.117975+00	2025-10-16 17:29:07.117977+00	43
1408	f	\N	798	Айшолпан 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.11844+00	2025-10-16 17:29:07.118699+00	2025-10-16 17:29:07.118701+00	109
1409	f	\N	797	Жибек 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.119154+00	2025-10-16 17:29:07.1194+00	2025-10-16 17:29:07.119402+00	146
1410	f	\N	796	Таганрог	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.119866+00	2025-10-16 17:29:07.120118+00	2025-10-16 17:29:07.12012+00	123
1411	f	\N	795	Зауральская волна	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.120597+00	2025-10-16 17:29:07.120878+00	2025-10-16 17:29:07.12088+00	71
1412	f	\N	794	Балгул 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.121327+00	2025-10-16 17:29:07.121572+00	2025-10-16 17:29:07.121574+00	144
1413	f	\N	793	Тауекел 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.122037+00	2025-10-16 17:29:07.122277+00	2025-10-16 17:29:07.122279+00	144
1414	f	\N	792	Эдельвейс 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.122753+00	2025-10-16 17:29:07.123007+00	2025-10-16 17:29:07.123009+00	71
1415	f	\N	791	БАТЫР 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.123623+00	2025-10-16 17:29:07.123956+00	2025-10-16 17:29:07.123959+00	88
1416	f	\N	790	АТАМЕКЕН 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.124452+00	2025-10-16 17:29:07.124739+00	2025-10-16 17:29:07.124741+00	119
1417	f	\N	789	Краюшка 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.125217+00	2025-10-16 17:29:07.125483+00	2025-10-16 17:29:07.125485+00	71
1418	f	\N	788	ПРОГРЕСС 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.125977+00	2025-10-16 17:29:07.126241+00	2025-10-16 17:29:07.126243+00	119
1419	f	\N	787	Отар-2 (1)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.126753+00	2025-10-16 17:29:07.127009+00	2025-10-16 17:29:07.127011+00	71
1420	f	\N	786	KZ231 (1)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.127501+00	2025-10-16 17:29:07.127772+00	2025-10-16 17:29:07.127774+00	71
1421	f	\N	785	Анель-16 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.128249+00	2025-10-16 17:29:07.128498+00	2025-10-16 17:29:07.1285+00	71
1422	f	\N	784	Омский лазурит 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.12898+00	2025-10-16 17:29:07.129231+00	2025-10-16 17:29:07.129233+00	123
1423	f	\N	783	Оресса 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.129723+00	2025-10-16 17:29:07.130012+00	2025-10-16 17:29:07.130015+00	119
1424	f	\N	782	Волма 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.130489+00	2025-10-16 17:29:07.130748+00	2025-10-16 17:29:07.13075+00	119
1425	f	\N	781	Кайрат 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.131213+00	2025-10-16 17:29:07.131463+00	2025-10-16 17:29:07.131465+00	149
1426	f	\N	780	Припять1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.132132+00	2025-10-16 17:29:07.132386+00	2025-10-16 17:29:07.132388+00	119
1427	f	\N	779	Абулхайыр 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.132826+00	2025-10-16 17:29:07.133073+00	2025-10-16 17:29:07.133075+00	109
1428	f	\N	778	Зере	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.133511+00	2025-10-16 17:29:07.133789+00	2025-10-16 17:29:07.133791+00	71
1429	f	\N	777	Рэд Роуз	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.134284+00	2025-10-16 17:29:07.134553+00	2025-10-16 17:29:07.134555+00	43
1430	f	\N	776	Кудесница	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.135008+00	2025-10-16 17:29:07.135264+00	2025-10-16 17:29:07.135266+00	71
1431	f	\N	775	Памяти Каскарбаева	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.135733+00	2025-10-16 17:29:07.13599+00	2025-10-16 17:29:07.135992+00	71
1432	f	\N	774	Аванс 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.13644+00	2025-10-16 17:29:07.136703+00	2025-10-16 17:29:07.136705+00	71
1433	f	\N	773	Таңбалы	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.13717+00	2025-10-16 17:29:07.137435+00	2025-10-16 17:29:07.137438+00	71
1434	f	\N	772	Сәтті-14 (1)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.137914+00	2025-10-16 17:29:07.138173+00	2025-10-16 17:29:07.138175+00	123
1435	f	\N	771	БАЙКОНУР 21 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.138637+00	2025-10-16 17:29:07.138892+00	2025-10-16 17:29:07.138894+00	88
1436	f	\N	770	Степь	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.13936+00	2025-10-16 17:29:07.139631+00	2025-10-16 17:29:07.139634+00	71
1437	f	\N	769	Маэстро 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.140112+00	2025-10-16 17:29:07.140368+00	2025-10-16 17:29:07.140371+00	71
1438	f	\N	768	Кең 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.140886+00	2025-10-16 17:29:07.141213+00	2025-10-16 17:29:07.141216+00	71
1439	f	\N	767	Кулан 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.141759+00	2025-10-16 17:29:07.142057+00	2025-10-16 17:29:07.142059+00	76
1440	f	\N	766	Старт	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.142579+00	2025-10-16 17:29:07.142922+00	2025-10-16 17:29:07.142925+00	71
1441	f	\N	765	Павлодарское 4 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.143432+00	2025-10-16 17:29:07.143711+00	2025-10-16 17:29:07.143713+00	90
1442	f	\N	764	Екатериновская 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.144209+00	2025-10-16 17:29:07.14447+00	2025-10-16 17:29:07.144472+00	141
1443	f	\N	763	Костанай	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.144926+00	2025-10-16 17:29:07.145206+00	2025-10-16 17:29:07.145208+00	71
1444	f	\N	762	Көркем 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.145671+00	2025-10-16 17:29:07.145927+00	2025-10-16 17:29:07.145929+00	126
1445	f	\N	761	Татьяна 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.146445+00	2025-10-16 17:29:07.146695+00	2025-10-16 17:29:07.146698+00	71
1446	f	\N	760	Ровенский	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.147153+00	2025-10-16 17:29:07.147407+00	2025-10-16 17:29:07.147409+00	74
1447	f	\N	759	Алатау-2015 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.147852+00	2025-10-16 17:29:07.148104+00	2025-10-16 17:29:07.148106+00	149
1448	f	\N	758	Сибирский геркулес 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.148564+00	2025-10-16 17:29:07.148839+00	2025-10-16 17:29:07.148841+00	76
1449	f	\N	757	Омский 100  (1)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.149297+00	2025-10-16 17:29:07.149565+00	2025-10-16 17:29:07.149568+00	149
1450	f	\N	756	КАТУНЬ	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.150032+00	2025-10-16 17:29:07.150294+00	2025-10-16 17:29:07.150296+00	71
1451	f	\N	755	Прииртышская 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.150775+00	2025-10-16 17:29:07.151045+00	2025-10-16 17:29:07.151048+00	71
1452	f	\N	754	Чароит 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.151523+00	2025-10-16 17:29:07.151791+00	2025-10-16 17:29:07.151793+00	43
1453	f	\N	753	СК Альта 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.152285+00	2025-10-16 17:29:07.152573+00	2025-10-16 17:29:07.152575+00	119
1454	f	\N	752	Крсаноуральская	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.153106+00	2025-10-16 17:29:07.153361+00	2025-10-16 17:29:07.153363+00	71
1455	f	\N	751	Алтай 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.153869+00	2025-10-16 17:29:07.154127+00	2025-10-16 17:29:07.154129+00	71
1456	f	\N	750	Приуральная	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.154576+00	2025-10-16 17:29:07.154864+00	2025-10-16 17:29:07.154866+00	71
1457	f	\N	749	Ертіс самалы 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.155307+00	2025-10-16 17:29:07.155559+00	2025-10-16 17:29:07.155561+00	76
1458	f	\N	748	Достык 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.156019+00	2025-10-16 17:29:07.15627+00	2025-10-16 17:29:07.156272+00	71
1459	f	\N	747	ГРАНАТ	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.156765+00	2025-10-16 17:29:07.157032+00	2025-10-16 17:29:07.157034+00	5
1460	f	\N	746	Алия Молдагулова 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.157484+00	2025-10-16 17:29:07.157778+00	2025-10-16 17:29:07.15778+00	79
1461	f	\N	745	Астронавт (Astronaute)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.158268+00	2025-10-16 17:29:07.158521+00	2025-10-16 17:29:07.158523+00	20
1462	f	\N	743	Назгум 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.158984+00	2025-10-16 17:29:07.159231+00	2025-10-16 17:29:07.159233+00	146
1463	f	\N	742	Алтын Орда	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.159688+00	2025-10-16 17:29:07.159973+00	2025-10-16 17:29:07.159976+00	123
1464	f	\N	741	Алаш	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.160712+00	2025-10-16 17:29:07.160956+00	2025-10-16 17:29:07.160958+00	71
1465	f	\N	740	Ақбастау 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.161421+00	2025-10-16 17:29:07.161697+00	2025-10-16 17:29:07.1617+00	119
1466	f	\N	739	Омская 42	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.162194+00	2025-10-16 17:29:07.162442+00	2025-10-16 17:29:07.162444+00	71
1467	f	\N	737	Елмерей 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.162915+00	2025-10-16 17:29:07.163166+00	2025-10-16 17:29:07.163168+00	119
1468	f	\N	736	СК Арктика 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.163648+00	2025-10-16 17:29:07.163907+00	2025-10-16 17:29:07.16391+00	119
1469	f	\N	735	СК Виола 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.164372+00	2025-10-16 17:29:07.164631+00	2025-10-16 17:29:07.164634+00	119
1470	f	\N	734	Скульптор 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.165191+00	2025-10-16 17:29:07.165445+00	2025-10-16 17:29:07.165447+00	119
1471	f	\N	733	Данелия 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.166085+00	2025-10-16 17:29:07.166412+00	2025-10-16 17:29:07.166414+00	119
1472	f	\N	731	Диар 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.166929+00	2025-10-16 17:29:07.167208+00	2025-10-16 17:29:07.16721+00	43
1473	f	\N	730	Baiterek-S 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.167706+00	2025-10-16 17:29:07.168018+00	2025-10-16 17:29:07.168021+00	88
1474	f	\N	729	Байконур 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.168506+00	2025-10-16 17:29:07.168819+00	2025-10-16 17:29:07.168821+00	88
1475	f	\N	728	Тан 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.169315+00	2025-10-16 17:29:07.169561+00	2025-10-16 17:29:07.169563+00	119
1476	f	\N	726	Алуа 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.170041+00	2025-10-16 17:29:07.170296+00	2025-10-16 17:29:07.170298+00	119
1477	f	\N	725	Биотех 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.17076+00	2025-10-16 17:29:07.171005+00	2025-10-16 17:29:07.171007+00	71
1478	f	\N	724	КазНау-90 (1)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.171447+00	2025-10-16 17:29:07.171717+00	2025-10-16 17:29:07.171719+00	43
1479	f	\N	723	Янтарная 150	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.172155+00	2025-10-16 17:29:07.172404+00	2025-10-16 17:29:07.172406+00	123
1480	f	\N	721	Айгуль	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.172877+00	2025-10-16 17:29:07.173118+00	2025-10-16 17:29:07.17312+00	71
1481	f	\N	720	Саибонг 11	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.173566+00	2025-10-16 17:29:07.173844+00	2025-10-16 17:29:07.173846+00	43
1482	f	\N	719	Сакура 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.174294+00	2025-10-16 17:29:07.174561+00	2025-10-16 17:29:07.174563+00	141
1483	f	\N	718	Ивушка 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.175021+00	2025-10-16 17:29:07.175276+00	2025-10-16 17:29:07.175278+00	119
1484	f	\N	717	Шаңырақ 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.175734+00	2025-10-16 17:29:07.176005+00	2025-10-16 17:29:07.176008+00	71
1485	f	\N	716	Герда 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.176485+00	2025-10-16 17:29:07.176744+00	2025-10-16 17:29:07.176746+00	71
1486	f	\N	715	Ламис 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.177221+00	2025-10-16 17:29:07.177506+00	2025-10-16 17:29:07.177508+00	71
1487	f	\N	714	Августина 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.177993+00	2025-10-16 17:29:07.17825+00	2025-10-16 17:29:07.178252+00	71
1488	f	\N	713	Бірлік КВ 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.178744+00	2025-10-16 17:29:07.179009+00	2025-10-16 17:29:07.179012+00	119
1489	f	\N	711	Саибонг 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.179489+00	2025-10-16 17:29:07.179748+00	2025-10-16 17:29:07.179751+00	43
1490	f	\N	710	Урал-1 (1)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.180208+00	2025-10-16 17:29:07.18049+00	2025-10-16 17:29:07.180492+00	43
1491	f	\N	709	Казыгурт 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.181003+00	2025-10-16 17:29:07.181262+00	2025-10-16 17:29:07.181264+00	149
1492	f	\N	708	Тамыз 1 (1)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.181735+00	2025-10-16 17:29:07.182014+00	2025-10-16 17:29:07.182016+00	90
1493	f	\N	707	Таймас	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.182468+00	2025-10-16 17:29:07.18274+00	2025-10-16 17:29:07.182743+00	71
1494	f	\N	706	Эрпсведо-17 (1)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.183394+00	2025-10-16 17:29:07.183667+00	2025-10-16 17:29:07.183669+00	71
1495	f	\N	705	Маэстро-Барбаросса 21  1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.184125+00	2025-10-16 17:29:07.18437+00	2025-10-16 17:29:07.184373+00	71
1496	f	\N	704	Статус 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.184831+00	2025-10-16 17:29:07.185069+00	2025-10-16 17:29:07.185071+00	20
1497	f	\N	703	Золотистая 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.185493+00	2025-10-16 17:29:07.185767+00	2025-10-16 17:29:07.18577+00	119
1498	f	\N	702	Велютинум-нифлатум-КК1 (1)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.186252+00	2025-10-16 17:29:07.186493+00	2025-10-16 17:29:07.186495+00	71
1499	f	\N	701	Кенеке 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.186925+00	2025-10-16 17:29:07.187193+00	2025-10-16 17:29:07.187195+00	71
1500	f	\N	700	Суббарба-23 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.187639+00	2025-10-16 17:29:07.187888+00	2025-10-16 17:29:07.18789+00	71
1501	f	\N	699	Эльдорадо 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.188342+00	2025-10-16 17:29:07.188606+00	2025-10-16 17:29:07.188609+00	119
1502	f	\N	698	Саша 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.189072+00	2025-10-16 17:29:07.189332+00	2025-10-16 17:29:07.189334+00	149
1503	f	\N	697	Глауко-Мильтрум-КК2 (1)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.18981+00	2025-10-16 17:29:07.190068+00	2025-10-16 17:29:07.19007+00	71
1504	f	\N	696	Омский голозерный 1 (1)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.190534+00	2025-10-16 17:29:07.190823+00	2025-10-16 17:29:07.190825+00	149
1505	f	\N	695	Омский 99 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.191278+00	2025-10-16 17:29:07.19154+00	2025-10-16 17:29:07.191542+00	149
1506	f	\N	694	Алтын масақ	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.192002+00	2025-10-16 17:29:07.192262+00	2025-10-16 17:29:07.192264+00	123
1507	f	\N	693	Жебе 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.192779+00	2025-10-16 17:29:07.193043+00	2025-10-16 17:29:07.193046+00	149
1508	f	\N	692	Карабалыкская черноколосая 20 (1)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.193493+00	2025-10-16 17:29:07.193766+00	2025-10-16 17:29:07.193768+00	123
1509	f	\N	691	Нұрлы 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.194224+00	2025-10-16 17:29:07.194491+00	2025-10-16 17:29:07.194493+00	123
1510	f	\N	690	Емдәмдік 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.194953+00	2025-10-16 17:29:07.19521+00	2025-10-16 17:29:07.195212+00	43
1511	f	\N	689	Тумар 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.195675+00	2025-10-16 17:29:07.195943+00	2025-10-16 17:29:07.195946+00	71
1512	f	\N	688	Эу-мильтурум ККЗ 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.196397+00	2025-10-16 17:29:07.196668+00	2025-10-16 17:29:07.19667+00	71
1513	f	\N	687	Туыс 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.197132+00	2025-10-16 17:29:07.197382+00	2025-10-16 17:29:07.197384+00	71
1514	f	\N	686	ГЛИКК 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.197852+00	2025-10-16 17:29:07.19811+00	2025-10-16 17:29:07.198112+00	71
1515	f	\N	685	Татулы	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.198555+00	2025-10-16 17:29:07.198833+00	2025-10-16 17:29:07.198835+00	137
1516	f	\N	684	Кихара ньюс 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.199281+00	2025-10-16 17:29:07.199543+00	2025-10-16 17:29:07.199545+00	123
1517	f	\N	683	Эл-мильтурум ККЗ 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.200003+00	2025-10-16 17:29:07.200261+00	2025-10-16 17:29:07.200264+00	71
1518	f	\N	682	Шортандинская 2012 (1)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.200738+00	2025-10-16 17:29:07.200999+00	2025-10-16 17:29:07.201001+00	71
1519	f	\N	681	Аяз 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.201444+00	2025-10-16 17:29:07.201733+00	2025-10-16 17:29:07.201735+00	71
1520	f	\N	680	Дамсинская янтарная 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.202204+00	2025-10-16 17:29:07.202465+00	2025-10-16 17:29:07.202467+00	123
1521	f	\N	679	Шелфорд1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.202918+00	2025-10-16 17:29:07.203191+00	2025-10-16 17:29:07.203193+00	43
1522	f	\N	678	Нургуль 85 (1)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.203639+00	2025-10-16 17:29:07.203897+00	2025-10-16 17:29:07.2039+00	144
1523	f	\N	677	КарагандинскаЯ 29	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.204343+00	2025-10-16 17:29:07.204606+00	2025-10-16 17:29:07.204608+00	71
1524	f	\N	676	Северянка	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.20507+00	2025-10-16 17:29:07.205321+00	2025-10-16 17:29:07.205323+00	71
1525	f	\N	675	Мейрам-20 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.205807+00	2025-10-16 17:29:07.206082+00	2025-10-16 17:29:07.206085+00	79
1526	f	\N	674	Алтынбас 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.206531+00	2025-10-16 17:29:07.206809+00	2025-10-16 17:29:07.206812+00	31
1527	f	\N	673	Казахстанский-92 (1)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.207255+00	2025-10-16 17:29:07.207523+00	2025-10-16 17:29:07.207526+00	88
1528	f	\N	672	Казахстан 75 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.208004+00	2025-10-16 17:29:07.208268+00	2025-10-16 17:29:07.20827+00	71
1529	f	\N	671	Көкбалауса	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.208752+00	2025-10-16 17:29:07.209008+00	2025-10-16 17:29:07.20901+00	61
1530	f	\N	670	КазНИИЗиР 75 (1)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.209649+00	2025-10-16 17:29:07.210009+00	2025-10-16 17:29:07.210011+00	54
1531	f	\N	669	Егемен-20 (1)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.210489+00	2025-10-16 17:29:07.210756+00	2025-10-16 17:29:07.210758+00	71
1532	f	\N	668	Когершин 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.211236+00	2025-10-16 17:29:07.211521+00	2025-10-16 17:29:07.211523+00	29
1533	f	\N	667	Донен 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.212004+00	2025-10-16 17:29:07.212256+00	2025-10-16 17:29:07.212258+00	76
1534	f	\N	666	Юбилейная 75	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.21272+00	2025-10-16 17:29:07.21297+00	2025-10-16 17:29:07.212972+00	71
1535	f	\N	665	Ракансам 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.213446+00	2025-10-16 17:29:07.213755+00	2025-10-16 17:29:07.213758+00	71
1536	f	\N	664	Багалы	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.21424+00	2025-10-16 17:29:07.214517+00	2025-10-16 17:29:07.214519+00	113
1537	f	\N	663	Кондитерская яровая 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.215011+00	2025-10-16 17:29:07.215263+00	2025-10-16 17:29:07.215265+00	71
1538	f	\N	662	Батыс 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.215728+00	2025-10-16 17:29:07.215976+00	2025-10-16 17:29:07.215979+00	35
1539	f	\N	661	Памяти Конаева 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.21643+00	2025-10-16 17:29:07.216705+00	2025-10-16 17:29:07.216707+00	43
1540	f	\N	660	Майса 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.217184+00	2025-10-16 17:29:07.217432+00	2025-10-16 17:29:07.217434+00	61
1541	f	\N	659	Калисто 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.21792+00	2025-10-16 17:29:07.218184+00	2025-10-16 17:29:07.218186+00	79
1542	f	\N	658	Дихан	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.21867+00	2025-10-16 17:29:07.218957+00	2025-10-16 17:29:07.218959+00	43
1543	f	\N	657	Каргала 71 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.219473+00	2025-10-16 17:29:07.219751+00	2025-10-16 17:29:07.219753+00	123
1544	f	\N	656	Сочинский 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.220224+00	2025-10-16 17:29:07.220471+00	2025-10-16 17:29:07.220473+00	88
1545	f	\N	655	Яркое 7	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.22092+00	2025-10-16 17:29:07.221181+00	2025-10-16 17:29:07.221183+00	90
1546	f	\N	654	Корона 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.221651+00	2025-10-16 17:29:07.221912+00	2025-10-16 17:29:07.221914+00	123
1547	f	\N	653	Казахстан 20 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.222379+00	2025-10-16 17:29:07.222665+00	2025-10-16 17:29:07.222668+00	71
1548	f	\N	652	ВКНИИСХ-2011(1)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.223137+00	2025-10-16 17:29:07.223388+00	2025-10-16 17:29:07.22339+00	88
1549	f	\N	651	Ақ орда1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.223862+00	2025-10-16 17:29:07.224115+00	2025-10-16 17:29:07.224117+00	71
1550	f	\N	650	Зара 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.224582+00	2025-10-16 17:29:07.224847+00	2025-10-16 17:29:07.224849+00	119
1551	f	\N	649	Алихан 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.22533+00	2025-10-16 17:29:07.225591+00	2025-10-16 17:29:07.225593+00	71
1552	f	\N	648	Тэрра-1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.226083+00	2025-10-16 17:29:07.226331+00	2025-10-16 17:29:07.226333+00	43
1553	f	\N	647	Акбидай 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.226822+00	2025-10-16 17:29:07.227072+00	2025-10-16 17:29:07.227074+00	71
1554	f	\N	646	Жайдарман 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.227536+00	2025-10-16 17:29:07.227791+00	2025-10-16 17:29:07.227794+00	88
1555	f	\N	645	Майқұдық 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.228264+00	2025-10-16 17:29:07.22852+00	2025-10-16 17:29:07.228523+00	97
1556	f	\N	644	Улар1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.229014+00	2025-10-16 17:29:07.229268+00	2025-10-16 17:29:07.22927+00	149
1557	f	\N	643	Биргит 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.229746+00	2025-10-16 17:29:07.23+00	2025-10-16 17:29:07.230002+00	43
1558	f	\N	642	Гала 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.23044+00	2025-10-16 17:29:07.230712+00	2025-10-16 17:29:07.230714+00	43
1559	f	\N	641	Шортандинский ширококолосый	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.231164+00	2025-10-16 17:29:07.231415+00	2025-10-16 17:29:07.231417+00	35
1560	f	\N	640	Антей 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.231856+00	2025-10-16 17:29:07.232105+00	2025-10-16 17:29:07.232107+00	76
1561	f	\N	639	Солист 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.232545+00	2025-10-16 17:29:07.232821+00	2025-10-16 17:29:07.232823+00	43
1562	f	\N	638	Сабира1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.233265+00	2025-10-16 17:29:07.233513+00	2025-10-16 17:29:07.233515+00	119
1563	f	\N	637	Ахрам 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.233991+00	2025-10-16 17:29:07.23425+00	2025-10-16 17:29:07.234252+00	106
1564	f	\N	636	Шалқар 39	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.234718+00	2025-10-16 17:29:07.234976+00	2025-10-16 17:29:07.234978+00	97
1565	f	\N	635	КАСИБ	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.23542+00	2025-10-16 17:29:07.235707+00	2025-10-16 17:29:07.23571+00	20
1566	f	\N	634	Жарық 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.236168+00	2025-10-16 17:29:07.23642+00	2025-10-16 17:29:07.236422+00	109
1567	f	\N	633	Павлодарская юбилейная 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.236904+00	2025-10-16 17:29:07.237179+00	2025-10-16 17:29:07.237181+00	71
1568	f	\N	632	Кормилица 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.237832+00	2025-10-16 17:29:07.238086+00	2025-10-16 17:29:07.238088+00	43
1569	f	\N	631	Бірлік - 20 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.238519+00	2025-10-16 17:29:07.238822+00	2025-10-16 17:29:07.238825+00	149
1570	f	\N	630	Сарыжаз (1)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.23932+00	2025-10-16 17:29:07.239572+00	2025-10-16 17:29:07.239574+00	80
1571	f	\N	629	Шабындық 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.240052+00	2025-10-16 17:29:07.240315+00	2025-10-16 17:29:07.240317+00	144
1572	f	\N	628	Сыр-Дешт	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.240794+00	2025-10-16 17:29:07.241045+00	2025-10-16 17:29:07.241047+00	61
1573	f	\N	627	Нур-Алем1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.241506+00	2025-10-16 17:29:07.241768+00	2025-10-16 17:29:07.24177+00	43
1574	f	\N	626	Талап(1)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.242243+00	2025-10-16 17:29:07.242512+00	2025-10-16 17:29:07.242514+00	106
1575	f	\N	625	Сарша 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.242992+00	2025-10-16 17:29:07.243245+00	2025-10-16 17:29:07.243248+00	106
1576	f	\N	624	Самал1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.243707+00	2025-10-16 17:29:07.243963+00	2025-10-16 17:29:07.243965+00	71
1577	f	\N	623	Бидай-2020	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.244422+00	2025-10-16 17:29:07.244691+00	2025-10-16 17:29:07.244693+00	71
1578	f	\N	622	Самат 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.245145+00	2025-10-16 17:29:07.245397+00	2025-10-16 17:29:07.245399+00	20
1579	f	\N	621	Әния1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.24584+00	2025-10-16 17:29:07.246085+00	2025-10-16 17:29:07.246087+00	71
1580	f	\N	620	Расад1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.246534+00	2025-10-16 17:29:07.246827+00	2025-10-16 17:29:07.24683+00	71
1581	f	\N	619	Сары-Арка -1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.247269+00	2025-10-16 17:29:07.247514+00	2025-10-16 17:29:07.247516+00	60
1582	f	\N	618	Чудесный 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.247949+00	2025-10-16 17:29:07.248215+00	2025-10-16 17:29:07.248217+00	126
1583	f	\N	617	Анара1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.248676+00	2025-10-16 17:29:07.248934+00	2025-10-16 17:29:07.248936+00	71
1584	f	\N	616	Аружан 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.249393+00	2025-10-16 17:29:07.24966+00	2025-10-16 17:29:07.249662+00	90
1585	f	\N	615	Алая заря-2 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.250116+00	2025-10-16 17:29:07.250365+00	2025-10-16 17:29:07.250367+00	43
1586	f	\N	614	Ажарлы 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.250833+00	2025-10-16 17:29:07.25107+00	2025-10-16 17:29:07.251073+00	71
1587	f	\N	613	Экспо-Астана 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.25153+00	2025-10-16 17:29:07.251807+00	2025-10-16 17:29:07.251809+00	5
1588	f	\N	612	Рауан 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.252271+00	2025-10-16 17:29:07.252541+00	2025-10-16 17:29:07.252543+00	88
1589	f	\N	611	Авангард 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.252996+00	2025-10-16 17:29:07.253251+00	2025-10-16 17:29:07.253253+00	71
1590	f	\N	610	АйКерим 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.253721+00	2025-10-16 17:29:07.253977+00	2025-10-16 17:29:07.253979+00	102
1591	f	\N	609	Мирас 07 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.254432+00	2025-10-16 17:29:07.254706+00	2025-10-16 17:29:07.254709+00	74
1592	f	\N	608	Роза 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.255151+00	2025-10-16 17:29:07.255407+00	2025-10-16 17:29:07.255409+00	119
1593	f	\N	607	Жетистик (1)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.255869+00	2025-10-16 17:29:07.256139+00	2025-10-16 17:29:07.256141+00	76
1594	f	\N	606	Арап улучшенный	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.2566+00	2025-10-16 17:29:07.256883+00	2025-10-16 17:29:07.256885+00	71
1595	f	\N	605	Оскемен	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.257328+00	2025-10-16 17:29:07.257573+00	2025-10-16 17:29:07.257575+00	71
1596	f	\N	604	Даулет 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.258035+00	2025-10-16 17:29:07.2583+00	2025-10-16 17:29:07.258302+00	71
1597	f	\N	603	Болашақ 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.258788+00	2025-10-16 17:29:07.259054+00	2025-10-16 17:29:07.259056+00	43
1598	f	\N	602	Тәуелсіздікө20 СВ (1)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.25951+00	2025-10-16 17:29:07.259785+00	2025-10-16 17:29:07.259787+00	54
1599	f	\N	601	Саян 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.260245+00	2025-10-16 17:29:07.260519+00	2025-10-16 17:29:07.260522+00	43
1600	f	\N	600	Кожа	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.26106+00	2025-10-16 17:29:07.261374+00	2025-10-16 17:29:07.261376+00	127
1601	f	\N	599	Байсан	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.261872+00	2025-10-16 17:29:07.262158+00	2025-10-16 17:29:07.26216+00	71
1602	f	\N	598	Кадия 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.262647+00	2025-10-16 17:29:07.262933+00	2025-10-16 17:29:07.262935+00	137
1603	f	\N	597	Баян 2017	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.263409+00	2025-10-16 17:29:07.263684+00	2025-10-16 17:29:07.263686+00	119
1604	f	\N	596	Азиада1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.264143+00	2025-10-16 17:29:07.264391+00	2025-10-16 17:29:07.264393+00	127
1605	f	\N	595	Кызылбидай1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.26485+00	2025-10-16 17:29:07.265113+00	2025-10-16 17:29:07.265115+00	71
1606	f	\N	594	Фараби 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.265777+00	2025-10-16 17:29:07.266047+00	2025-10-16 17:29:07.26605+00	71
1607	f	\N	593	Мерей той 75 СВ 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.266531+00	2025-10-16 17:29:07.266794+00	2025-10-16 17:29:07.266796+00	54
1608	f	\N	592	Фламинго 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.267275+00	2025-10-16 17:29:07.267528+00	2025-10-16 17:29:07.26753+00	144
1609	f	\N	591	Владимир 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.268005+00	2025-10-16 17:29:07.268255+00	2025-10-16 17:29:07.268257+00	71
1610	f	\N	590	Жаик-2 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.268727+00	2025-10-16 17:29:07.268985+00	2025-10-16 17:29:07.268987+00	149
1611	f	\N	589	Абзал1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.269465+00	2025-10-16 17:29:07.269737+00	2025-10-16 17:29:07.269739+00	113
1612	f	\N	588	Райгаубек 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.270198+00	2025-10-16 17:29:07.270448+00	2025-10-16 17:29:07.27045+00	96
1613	f	\N	587	Перизат1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.270917+00	2025-10-16 17:29:07.271163+00	2025-10-16 17:29:07.271165+00	119
1614	f	\N	586	Яркое 5 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.271643+00	2025-10-16 17:29:07.271895+00	2025-10-16 17:29:07.271897+00	90
1615	f	\N	585	ЦИВГ198(CIVG198)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.272382+00	2025-10-16 17:29:07.272638+00	2025-10-16 17:29:07.27264+00	146
1616	f	\N	584	Баканасский 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.273086+00	2025-10-16 17:29:07.273343+00	2025-10-16 17:29:07.273345+00	102
1617	f	\N	583	Степная 51	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.273803+00	2025-10-16 17:29:07.274041+00	2025-10-16 17:29:07.274043+00	71
1618	f	\N	582	Данияр 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.274491+00	2025-10-16 17:29:07.274775+00	2025-10-16 17:29:07.274777+00	146
1619	f	\N	581	Глубочанка 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.275245+00	2025-10-16 17:29:07.275495+00	2025-10-16 17:29:07.275497+00	71
1620	f	\N	580	Мереке 75 (1)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.275965+00	2025-10-16 17:29:07.276231+00	2025-10-16 17:29:07.276233+00	71
1621	f	\N	579	Костанайская 15	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.27672+00	2025-10-16 17:29:07.276994+00	2025-10-16 17:29:07.276996+00	123
1622	f	\N	578	Достық	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.277472+00	2025-10-16 17:29:07.277745+00	2025-10-16 17:29:07.277747+00	144
1623	f	\N	577	Медикум 18 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.278207+00	2025-10-16 17:29:07.278475+00	2025-10-16 17:29:07.278477+00	149
1624	f	\N	576	Малиновое Чудо 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.27896+00	2025-10-16 17:29:07.279234+00	2025-10-16 17:29:07.279236+00	126
1625	f	\N	575	Карабалыкский 85 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.279728+00	2025-10-16 17:29:07.28+00	2025-10-16 17:29:07.280003+00	149
1626	f	\N	574	Казахстанский-5	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.280485+00	2025-10-16 17:29:07.28078+00	2025-10-16 17:29:07.280782+00	88
1627	f	\N	573	Заломе (Salome) 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.281244+00	2025-10-16 17:29:07.281509+00	2025-10-16 17:29:07.281512+00	149
1628	f	\N	572	Казахстан-20(1)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.282043+00	2025-10-16 17:29:07.282323+00	2025-10-16 17:29:07.282326+00	16
1629	f	\N	571	Аққу	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.283002+00	2025-10-16 17:29:07.283312+00	2025-10-16 17:29:07.283314+00	119
1630	f	\N	570	Сердце Астаны 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.283807+00	2025-10-16 17:29:07.284083+00	2025-10-16 17:29:07.284085+00	126
1631	f	\N	569	Степнодар 90	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.284596+00	2025-10-16 17:29:07.284898+00	2025-10-16 17:29:07.2849+00	71
1632	f	\N	568	Шортандинская 2 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.285363+00	2025-10-16 17:29:07.285634+00	2025-10-16 17:29:07.285637+00	61
1633	f	\N	567	Гульден 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.28614+00	2025-10-16 17:29:07.286395+00	2025-10-16 17:29:07.286397+00	119
1634	f	\N	566	Амина1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.286879+00	2025-10-16 17:29:07.287133+00	2025-10-16 17:29:07.287136+00	71
1635	f	\N	565	Нурлы 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.287634+00	2025-10-16 17:29:07.287917+00	2025-10-16 17:29:07.287919+00	123
1636	f	\N	564	Галия 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.288386+00	2025-10-16 17:29:07.288664+00	2025-10-16 17:29:07.288666+00	127
1637	f	\N	563	Доната 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.289167+00	2025-10-16 17:29:07.289421+00	2025-10-16 17:29:07.289423+00	43
1638	f	\N	562	Милана 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.289896+00	2025-10-16 17:29:07.290166+00	2025-10-16 17:29:07.290169+00	123
1639	f	\N	561	Аян-216	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.290642+00	2025-10-16 17:29:07.290908+00	2025-10-16 17:29:07.290911+00	126
1640	f	\N	560	Астаналык	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.291381+00	2025-10-16 17:29:07.291659+00	2025-10-16 17:29:07.291662+00	43
1641	f	\N	559	Восточно-Казахстанская 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.292146+00	2025-10-16 17:29:07.292398+00	2025-10-16 17:29:07.2924+00	71
1642	f	\N	558	Гульбагыс	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.292889+00	2025-10-16 17:29:07.293166+00	2025-10-16 17:29:07.293168+00	88
1643	f	\N	557	Орал 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.293624+00	2025-10-16 17:29:07.293879+00	2025-10-16 17:29:07.293881+00	71
1644	f	\N	556	Карагандинский 6 (1)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.294513+00	2025-10-16 17:29:07.2948+00	2025-10-16 17:29:07.294802+00	149
1645	f	\N	555	Удовицкий 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.295264+00	2025-10-16 17:29:07.295532+00	2025-10-16 17:29:07.295535+00	43
1646	f	\N	554	Дар Кайнара	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.296013+00	2025-10-16 17:29:07.296272+00	2025-10-16 17:29:07.296274+00	60
1647	f	\N	553	София 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.296742+00	2025-10-16 17:29:07.297008+00	2025-10-16 17:29:07.297011+00	43
1648	f	\N	552	Ақниет1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.29748+00	2025-10-16 17:29:07.297765+00	2025-10-16 17:29:07.297768+00	60
1649	f	\N	551	Сабир 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.298243+00	2025-10-16 17:29:07.298509+00	2025-10-16 17:29:07.298511+00	149
1650	f	\N	550	Коксарай 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.299012+00	2025-10-16 17:29:07.299273+00	2025-10-16 17:29:07.299275+00	61
1651	f	\N	549	Алиша 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.299741+00	2025-10-16 17:29:07.29999+00	2025-10-16 17:29:07.299992+00	71
1652	f	\N	548	Карабалыкский гранатовый	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.300428+00	2025-10-16 17:29:07.300709+00	2025-10-16 17:29:07.300712+00	144
1653	f	\N	547	Беркут 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.301162+00	2025-10-16 17:29:07.301411+00	2025-10-16 17:29:07.301413+00	43
1654	f	\N	546	Омега 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.3019+00	2025-10-16 17:29:07.302171+00	2025-10-16 17:29:07.302173+00	43
1655	f	\N	545	Рэд Фэнтази 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.302636+00	2025-10-16 17:29:07.302902+00	2025-10-16 17:29:07.302904+00	43
1656	f	\N	544	Даная 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.303338+00	2025-10-16 17:29:07.303601+00	2025-10-16 17:29:07.303603+00	119
1657	f	\N	543	Алпамыс 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.304063+00	2025-10-16 17:29:07.304307+00	2025-10-16 17:29:07.304309+00	138
1658	f	\N	542	Дуэт Азии 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.304794+00	2025-10-16 17:29:07.305044+00	2025-10-16 17:29:07.305046+00	74
1659	f	\N	541	Таңщолпан 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.305514+00	2025-10-16 17:29:07.3058+00	2025-10-16 17:29:07.305802+00	126
1660	f	\N	540	Целинная 26	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.306278+00	2025-10-16 17:29:07.306532+00	2025-10-16 17:29:07.306534+00	71
1661	f	\N	539	Ермак 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.306984+00	2025-10-16 17:29:07.307239+00	2025-10-16 17:29:07.307242+00	144
1662	f	\N	538	Акбас	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.307697+00	2025-10-16 17:29:07.307953+00	2025-10-16 17:29:07.307955+00	31
1663	f	\N	537	Ильин 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.308401+00	2025-10-16 17:29:07.308654+00	2025-10-16 17:29:07.308657+00	43
1664	f	\N	536	Сайлау 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.309087+00	2025-10-16 17:29:07.309342+00	2025-10-16 17:29:07.309345+00	79
1665	f	\N	535	КазНИИР-7	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.309807+00	2025-10-16 17:29:07.310062+00	2025-10-16 17:29:07.310064+00	102
1666	f	\N	534	Джелли 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.310508+00	2025-10-16 17:29:07.310803+00	2025-10-16 17:29:07.310805+00	43
1667	f	\N	533	777	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.311296+00	2025-10-16 17:29:07.311585+00	2025-10-16 17:29:07.311587+00	5
1668	f	\N	532	СанСпарк 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.312072+00	2025-10-16 17:29:07.31233+00	2025-10-16 17:29:07.312333+00	146
1669	f	\N	531	Ульбинка 55	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.312797+00	2025-10-16 17:29:07.313049+00	2025-10-16 17:29:07.313051+00	71
1670	f	\N	530	Тяньшанский 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.313515+00	2025-10-16 17:29:07.313794+00	2025-10-16 17:29:07.313796+00	43
1671	f	\N	529	Ляззат	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.314244+00	2025-10-16 17:29:07.314499+00	2025-10-16 17:29:07.314501+00	71
1672	f	\N	528	Наргиз	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.314969+00	2025-10-16 17:29:07.315226+00	2025-10-16 17:29:07.315228+00	71
1673	f	\N	527	Пиротрикс 28	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.315679+00	2025-10-16 17:29:07.315931+00	2025-10-16 17:29:07.315933+00	71
1674	f	\N	526	Целинная нива	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.316422+00	2025-10-16 17:29:07.316692+00	2025-10-16 17:29:07.316694+00	71
1675	f	\N	525	Тәтті-2012 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.317331+00	2025-10-16 17:29:07.317585+00	2025-10-16 17:29:07.317587+00	54
1676	f	\N	524	Целинная юбилейная	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.318082+00	2025-10-16 17:29:07.318342+00	2025-10-16 17:29:07.318344+00	71
1677	f	\N	523	Астана 2	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.318819+00	2025-10-16 17:29:07.319056+00	2025-10-16 17:29:07.319058+00	71
1678	f	\N	522	Коралл 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.319498+00	2025-10-16 17:29:07.319778+00	2025-10-16 17:29:07.31978+00	144
1679	f	\N	520	Коктобе 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.320233+00	2025-10-16 17:29:07.320492+00	2025-10-16 17:29:07.320494+00	146
1680	f	\N	519	Шугыла	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.320963+00	2025-10-16 17:29:07.321235+00	2025-10-16 17:29:07.321237+00	71
1681	f	\N	518	Өріс 1 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.321715+00	2025-10-16 17:29:07.321987+00	2025-10-16 17:29:07.321989+00	20
1682	f	\N	517	Адия 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.322449+00	2025-10-16 17:29:07.322712+00	2025-10-16 17:29:07.322715+00	123
1683	f	\N	516	Европрима 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.323175+00	2025-10-16 17:29:07.323429+00	2025-10-16 17:29:07.323431+00	43
1684	f	\N	515	Неженка	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.323898+00	2025-10-16 17:29:07.324166+00	2025-10-16 17:29:07.324168+00	40
1685	f	\N	514	Саламанка 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.32464+00	2025-10-16 17:29:07.324904+00	2025-10-16 17:29:07.324906+00	20
1686	f	\N	513	Желтоксан 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.325364+00	2025-10-16 17:29:07.325627+00	2025-10-16 17:29:07.32563+00	29
1687	f	\N	512	Юбилейный 40 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.326095+00	2025-10-16 17:29:07.326353+00	2025-10-16 17:29:07.326355+00	88
1688	f	\N	511	Алем 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.326822+00	2025-10-16 17:29:07.327073+00	2025-10-16 17:29:07.327076+00	71
1689	f	\N	510	Сорая 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.327522+00	2025-10-16 17:29:07.327799+00	2025-10-16 17:29:07.327801+00	43
1690	f	\N	509	Шортандинское 12	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.328245+00	2025-10-16 17:29:07.328506+00	2025-10-16 17:29:07.328508+00	90
1691	f	\N	508	Кормовое 2011 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.328955+00	2025-10-16 17:29:07.329219+00	2025-10-16 17:29:07.329221+00	90
1693	f	\N	506	Бота 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.330409+00	2025-10-16 17:29:07.330696+00	2025-10-16 17:29:07.330699+00	146
1694	f	\N	505	BP 808(VR 808)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.331182+00	2025-10-16 17:29:07.331433+00	2025-10-16 17:29:07.331435+00	43
1695	f	\N	504	Мамыр	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.331868+00	2025-10-16 17:29:07.332141+00	2025-10-16 17:29:07.332143+00	71
1696	f	\N	503	Тәуелсіздік 20	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.332577+00	2025-10-16 17:29:07.332852+00	2025-10-16 17:29:07.332855+00	71
1697	f	\N	502	Бригадир 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.333302+00	2025-10-16 17:29:07.333567+00	2025-10-16 17:29:07.33357+00	149
1698	f	\N	501	Алихан 17 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.33405+00	2025-10-16 17:29:07.334316+00	2025-10-16 17:29:07.334318+00	109
1699	f	\N	500	Шортандинская 2017 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.334777+00	2025-10-16 17:29:07.335024+00	2025-10-16 17:29:07.335027+00	71
1700	f	\N	499	Бірлестік 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.335482+00	2025-10-16 17:29:07.335756+00	2025-10-16 17:29:07.335758+00	71
1701	f	\N	498	Калиббр 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.336216+00	2025-10-16 17:29:07.336474+00	2025-10-16 17:29:07.336476+00	149
1702	f	\N	497	Тараз 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.336918+00	2025-10-16 17:29:07.337181+00	2025-10-16 17:29:07.337184+00	109
1703	f	\N	496	Дамсинская 20-17 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.337658+00	2025-10-16 17:29:07.337909+00	2025-10-16 17:29:07.337911+00	123
1704	f	\N	495	Кредо 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.33836+00	2025-10-16 17:29:07.338643+00	2025-10-16 17:29:07.338645+00	90
1705	f	\N	494	Укосное 1 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.339098+00	2025-10-16 17:29:07.339355+00	2025-10-16 17:29:07.339358+00	90
1706	f	\N	493	Тим-Бидай 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.339814+00	2025-10-16 17:29:07.34008+00	2025-10-16 17:29:07.340082+00	71
1707	f	\N	492	Гунтикум 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.34053+00	2025-10-16 17:29:07.340814+00	2025-10-16 17:29:07.340816+00	71
1708	f	\N	491	ВЕК 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.341274+00	2025-10-16 17:29:07.341543+00	2025-10-16 17:29:07.341545+00	71
1709	f	\N	490	ЦИВП21  1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.342026+00	2025-10-16 17:29:07.342296+00	2025-10-16 17:29:07.342298+00	146
1710	f	\N	489	Зарина 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.342757+00	2025-10-16 17:29:07.343018+00	2025-10-16 17:29:07.34302+00	71
1711	f	\N	488	Зерен 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.343481+00	2025-10-16 17:29:07.343754+00	2025-10-16 17:29:07.343756+00	43
1712	f	\N	487	Эмиль-10 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.344207+00	2025-10-16 17:29:07.344474+00	2025-10-16 17:29:07.344476+00	71
1713	f	\N	486	Чаглинская 14 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.345182+00	2025-10-16 17:29:07.345447+00	2025-10-16 17:29:07.345449+00	61
1714	f	\N	485	Шортандинское 14 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.345897+00	2025-10-16 17:29:07.346162+00	2025-10-16 17:29:07.346164+00	90
1715	f	\N	484	Целинный 60 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.346625+00	2025-10-16 17:29:07.34689+00	2025-10-16 17:29:07.346893+00	149
1716	f	\N	483	Степная 53 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.347342+00	2025-10-16 17:29:07.347595+00	2025-10-16 17:29:07.347597+00	71
1717	f	\N	482	Фортуна1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.348066+00	2025-10-16 17:29:07.348326+00	2025-10-16 17:29:07.348328+00	43
1718	f	\N	481	Светланка1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.348782+00	2025-10-16 17:29:07.349049+00	2025-10-16 17:29:07.349051+00	71
1719	f	\N	480	Уран1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.34952+00	2025-10-16 17:29:07.349791+00	2025-10-16 17:29:07.349793+00	76
1720	f	\N	479	Ливера1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.350249+00	2025-10-16 17:29:07.350518+00	2025-10-16 17:29:07.35052+00	32
1721	f	\N	478	Пренигро-20 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.350996+00	2025-10-16 17:29:07.351252+00	2025-10-16 17:29:07.351254+00	71
1722	f	\N	477	Костанайская 207 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.351725+00	2025-10-16 17:29:07.351991+00	2025-10-16 17:29:07.351993+00	123
1723	f	\N	476	Гайни	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.352473+00	2025-10-16 17:29:07.352766+00	2025-10-16 17:29:07.352769+00	146
1724	f	\N	475	Бабаев1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.353224+00	2025-10-16 17:29:07.353495+00	2025-10-16 17:29:07.353498+00	43
1725	f	\N	474	Балнур1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.353957+00	2025-10-16 17:29:07.35422+00	2025-10-16 17:29:07.354222+00	29
1726	f	\N	473	Рамиса1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.354686+00	2025-10-16 17:29:07.35497+00	2025-10-16 17:29:07.354973+00	71
1727	f	\N	472	Эльддорадо1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.355423+00	2025-10-16 17:29:07.355697+00	2025-10-16 17:29:07.3557+00	119
1728	f	\N	470	Сибирячка1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.356162+00	2025-10-16 17:29:07.356433+00	2025-10-16 17:29:07.356435+00	119
1729	f	\N	469	Үміт1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.35694+00	2025-10-16 17:29:07.357206+00	2025-10-16 17:29:07.357208+00	106
1730	f	\N	468	Азим	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.357699+00	2025-10-16 17:29:07.357956+00	2025-10-16 17:29:07.357958+00	16
1731	f	\N	467	Статаус	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.358414+00	2025-10-16 17:29:07.358687+00	2025-10-16 17:29:07.35869+00	20
1732	f	\N	466	КазИнд	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.359192+00	2025-10-16 17:29:07.359453+00	2025-10-16 17:29:07.359455+00	115
1733	f	\N	462	Экада 113 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.359929+00	2025-10-16 17:29:07.360192+00	2025-10-16 17:29:07.360194+00	71
1734	f	\N	461	Мелодия	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.360672+00	2025-10-16 17:29:07.360963+00	2025-10-16 17:29:07.360965+00	71
1735	f	\N	460	Серебристая 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.361436+00	2025-10-16 17:29:07.36171+00	2025-10-16 17:29:07.361712+00	71
1736	f	\N	459	Иртыш 21	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.362178+00	2025-10-16 17:29:07.36244+00	2025-10-16 17:29:07.362442+00	76
1737	f	\N	458	Памяти Азиева 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.362913+00	2025-10-16 17:29:07.363163+00	2025-10-16 17:29:07.363165+00	71
1738	f	\N	457	Омская 35 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.363636+00	2025-10-16 17:29:07.363906+00	2025-10-16 17:29:07.363908+00	71
1739	f	\N	456	Омская 36 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.364356+00	2025-10-16 17:29:07.364607+00	2025-10-16 17:29:07.364618+00	71
1740	f	\N	455	Омская 38	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.365115+00	2025-10-16 17:29:07.365385+00	2025-10-16 17:29:07.365387+00	71
1741	f	\N	454	Префер-22	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.365859+00	2025-10-16 17:29:07.366108+00	2025-10-16 17:29:07.36611+00	71
1742	f	\N	453	Ерпреудо-24	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.366596+00	2025-10-16 17:29:07.366863+00	2025-10-16 17:29:07.366865+00	71
1743	f	\N	452	Мейрам - 55	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.367331+00	2025-10-16 17:29:07.367598+00	2025-10-16 17:29:07.3676+00	16
1744	f	\N	451	Валет	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.368068+00	2025-10-16 17:29:07.368321+00	2025-10-16 17:29:07.368323+00	32
1745	f	\N	450	Фуджион (Fujion)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.368816+00	2025-10-16 17:29:07.369071+00	2025-10-16 17:29:07.369073+00	146
1746	f	\N	449	Смеральда	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.369579+00	2025-10-16 17:29:07.36987+00	2025-10-16 17:29:07.369873+00	146
1747	f	\N	448	Салима	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.370348+00	2025-10-16 17:29:07.370597+00	2025-10-16 17:29:07.370599+00	29
1748	f	\N	447	Актюбинский 2 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.371068+00	2025-10-16 17:29:07.371325+00	2025-10-16 17:29:07.371327+00	43
1749	f	\N	446	Асыл 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.371796+00	2025-10-16 17:29:07.372063+00	2025-10-16 17:29:07.372065+00	138
1750	f	\N	445	Сымбат 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.372544+00	2025-10-16 17:29:07.372839+00	2025-10-16 17:29:07.372841+00	74
1751	f	\N	444	Омская 41 (1)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.373457+00	2025-10-16 17:29:07.373734+00	2025-10-16 17:29:07.373737+00	71
1752	f	\N	443	Омская 39 (1)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.374196+00	2025-10-16 17:29:07.374474+00	2025-10-16 17:29:07.374476+00	71
1753	f	\N	442	Омская 37	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.374953+00	2025-10-16 17:29:07.375219+00	2025-10-16 17:29:07.375221+00	71
1754	f	\N	441	Жемчужина Сибири 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.375696+00	2025-10-16 17:29:07.375985+00	2025-10-16 17:29:07.375987+00	123
1755	f	\N	440	Памяти Богачкова	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.376456+00	2025-10-16 17:29:07.376743+00	2025-10-16 17:29:07.376746+00	76
1756	f	\N	439	Талап 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.377207+00	2025-10-16 17:29:07.377489+00	2025-10-16 17:29:07.377491+00	61
1757	f	\N	438	Омский изумруд	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.377948+00	2025-10-16 17:29:07.378212+00	2025-10-16 17:29:07.378214+00	123
1758	f	\N	437	Белоснежка	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.378664+00	2025-10-16 17:29:07.378924+00	2025-10-16 17:29:07.378926+00	113
1759	f	\N	436	Таулы	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.379371+00	2025-10-16 17:29:07.379647+00	2025-10-16 17:29:07.37965+00	137
1760	f	\N	435	Казахстанский-95	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.380137+00	2025-10-16 17:29:07.380398+00	2025-10-16 17:29:07.3804+00	88
1761	f	\N	434	Дива	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.380969+00	2025-10-16 17:29:07.381273+00	2025-10-16 17:29:07.381275+00	71
1762	f	\N	433	Умай	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.381828+00	2025-10-16 17:29:07.382104+00	2025-10-16 17:29:07.382106+00	71
1763	f	\N	432	Крапинка	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.382874+00	2025-10-16 17:29:07.383222+00	2025-10-16 17:29:07.383225+00	141
1764	f	\N	431	Керемет	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.384106+00	2025-10-16 17:29:07.384487+00	2025-10-16 17:29:07.38449+00	126
1765	f	\N	430	Аят	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.385042+00	2025-10-16 17:29:07.38532+00	2025-10-16 17:29:07.385322+00	149
1766	f	\N	429	Монолит	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.385827+00	2025-10-16 17:29:07.386086+00	2025-10-16 17:29:07.386088+00	149
1767	f	\N	428	Фантазия	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.38662+00	2025-10-16 17:29:07.386911+00	2025-10-16 17:29:07.386913+00	71
1768	f	\N	427	СимКар 20	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.387378+00	2025-10-16 17:29:07.387655+00	2025-10-16 17:29:07.387657+00	71
1769	f	\N	426	Асангали 20	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.388168+00	2025-10-16 17:29:07.388437+00	2025-10-16 17:29:07.388439+00	123
1770	f	\N	425	Камила	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.388944+00	2025-10-16 17:29:07.389222+00	2025-10-16 17:29:07.389224+00	146
1771	f	\N	424	Айдана	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.389727+00	2025-10-16 17:29:07.389998+00	2025-10-16 17:29:07.39+00	29
1772	f	\N	423	Ренклод талгарский	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.390446+00	2025-10-16 17:29:07.390851+00	2025-10-16 17:29:07.390853+00	113
1773	f	\N	422	Омская степная	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.391469+00	2025-10-16 17:29:07.391854+00	2025-10-16 17:29:07.391857+00	123
1774	f	\N	421	Күн нұры	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.392575+00	2025-10-16 17:29:07.392898+00	2025-10-16 17:29:07.392901+00	88
1775	f	\N	420	Брук	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.393436+00	2025-10-16 17:29:07.393738+00	2025-10-16 17:29:07.39374+00	43
1776	f	\N	419	Шелфрод	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.394244+00	2025-10-16 17:29:07.394519+00	2025-10-16 17:29:07.394521+00	43
1777	f	\N	418	Ньютон	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.395013+00	2025-10-16 17:29:07.395278+00	2025-10-16 17:29:07.39528+00	43
1778	f	\N	417	Кешен	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.395758+00	2025-10-16 17:29:07.396032+00	2025-10-16 17:29:07.396034+00	115
1779	f	\N	416	Анель	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.396492+00	2025-10-16 17:29:07.396776+00	2025-10-16 17:29:07.396778+00	146
1780	f	\N	415	Балжан	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.397237+00	2025-10-16 17:29:07.397539+00	2025-10-16 17:29:07.397541+00	29
1781	f	\N	414	Омская янтарная	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.398+00	2025-10-16 17:29:07.39825+00	2025-10-16 17:29:07.398252+00	123
1782	f	\N	413	Ишимский 13	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.398761+00	2025-10-16 17:29:07.399097+00	2025-10-16 17:29:07.399099+00	76
1783	f	\N	412	КазСИП 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.399772+00	2025-10-16 17:29:07.400114+00	2025-10-16 17:29:07.400116+00	43
1784	f	\N	411	Шортандинская 5	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.401088+00	2025-10-16 17:29:07.401453+00	2025-10-16 17:29:07.401456+00	27
1785	f	\N	410	Матай	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.401986+00	2025-10-16 17:29:07.40224+00	2025-10-16 17:29:07.402242+00	71
1786	f	\N	409	Шахристан	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.402728+00	2025-10-16 17:29:07.402998+00	2025-10-16 17:29:07.403+00	149
1787	f	\N	408	Восторг	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.403466+00	2025-10-16 17:29:07.403732+00	2025-10-16 17:29:07.403735+00	126
1788	f	\N	407	Тәлімі-80	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.40424+00	2025-10-16 17:29:07.404494+00	2025-10-16 17:29:07.404496+00	71
1789	f	\N	406	ДГЛ KZR	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.405146+00	2025-10-16 17:29:07.4054+00	2025-10-16 17:29:07.405402+00	71
1790	f	\N	405	Коктем-1 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.405881+00	2025-10-16 17:29:07.406137+00	2025-10-16 17:29:07.406139+00	43
1791	f	\N	404	ДГЛ KZ 19	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.406591+00	2025-10-16 17:29:07.406875+00	2025-10-16 17:29:07.406877+00	71
1792	f	\N	403	АйСауле 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.40742+00	2025-10-16 17:29:07.40785+00	2025-10-16 17:29:07.407853+00	102
1793	f	\N	402	Сарайчик	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.408475+00	2025-10-16 17:29:07.408913+00	2025-10-16 17:29:07.408916+00	31
1794	f	\N	401	КизНид	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.409567+00	2025-10-16 17:29:07.409882+00	2025-10-16 17:29:07.409885+00	115
1795	f	\N	400	Лина Костаная	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.410367+00	2025-10-16 17:29:07.410626+00	2025-10-16 17:29:07.410629+00	43
1796	f	\N	399	Преемница	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.411076+00	2025-10-16 17:29:07.411322+00	2025-10-16 17:29:07.411324+00	17
1797	f	\N	398	Курчатовская	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.411791+00	2025-10-16 17:29:07.412049+00	2025-10-16 17:29:07.412052+00	17
1798	f	\N	397	Карабалыкская 20	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.412501+00	2025-10-16 17:29:07.412781+00	2025-10-16 17:29:07.412783+00	71
1799	f	\N	396	Кормовое 2014	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.413256+00	2025-10-16 17:29:07.413522+00	2025-10-16 17:29:07.413524+00	90
1800	f	\N	395	Кокшетауский 10	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.414051+00	2025-10-16 17:29:07.41435+00	2025-10-16 17:29:07.414352+00	31
1801	f	\N	394	Дархан дән 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.414856+00	2025-10-16 17:29:07.415141+00	2025-10-16 17:29:07.415144+00	71
1802	f	\N	393	Галатея	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.415631+00	2025-10-16 17:29:07.416084+00	2025-10-16 17:29:07.416086+00	71
1803	f	\N	392	Акжайык	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.416855+00	2025-10-16 17:29:07.417402+00	2025-10-16 17:29:07.417405+00	16
1804	f	\N	391	Бостандық	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.418096+00	2025-10-16 17:29:07.418387+00	2025-10-16 17:29:07.418389+00	71
1805	f	\N	390	Великан	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.418892+00	2025-10-16 17:29:07.419183+00	2025-10-16 17:29:07.419185+00	149
1806	f	\N	389	Карабалыкская изумрудная	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.419688+00	2025-10-16 17:29:07.419949+00	2025-10-16 17:29:07.419951+00	61
1807	f	\N	388	Беллароза	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.420415+00	2025-10-16 17:29:07.420691+00	2025-10-16 17:29:07.420693+00	43
1808	f	\N	387	Соколовское	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.421187+00	2025-10-16 17:29:07.421449+00	2025-10-16 17:29:07.421452+00	146
1809	f	\N	386	Вивиана	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.421906+00	2025-10-16 17:29:07.422197+00	2025-10-16 17:29:07.422199+00	43
1810	f	\N	385	Илек 36	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.422679+00	2025-10-16 17:29:07.422945+00	2025-10-16 17:29:07.422947+00	149
1811	f	\N	384	Артем	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.4234+00	2025-10-16 17:29:07.423646+00	2025-10-16 17:29:07.423649+00	43
1812	f	\N	383	Айжан	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.424186+00	2025-10-16 17:29:07.424742+00	2025-10-16 17:29:07.424745+00	146
1813	f	\N	382	ДГЛ AST	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.425935+00	2025-10-16 17:29:07.426283+00	2025-10-16 17:29:07.426285+00	71
1814	f	\N	381	Шапагат	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.426851+00	2025-10-16 17:29:07.42714+00	2025-10-16 17:29:07.427142+00	71
1815	f	\N	380	Акжол-14 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.427635+00	2025-10-16 17:29:07.42791+00	2025-10-16 17:29:07.427912+00	43
1816	f	\N	379	Серке	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.428403+00	2025-10-16 17:29:07.42869+00	2025-10-16 17:29:07.428692+00	123
1817	f	\N	378	Суламит 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.429148+00	2025-10-16 17:29:07.429419+00	2025-10-16 17:29:07.429421+00	119
1818	f	\N	377	Ай-Ару	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.429897+00	2025-10-16 17:29:07.430189+00	2025-10-16 17:29:07.430191+00	16
1819	f	\N	376	Казахстанский ранний	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.430641+00	2025-10-16 17:29:07.430894+00	2025-10-16 17:29:07.430896+00	60
1820	f	\N	375	Жигер	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.431346+00	2025-10-16 17:29:07.431594+00	2025-10-16 17:29:07.431596+00	79
1821	f	\N	374	Ерке	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.432093+00	2025-10-16 17:29:07.432367+00	2025-10-16 17:29:07.432369+00	32
1822	f	\N	373	Сеним	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.433174+00	2025-10-16 17:29:07.433521+00	2025-10-16 17:29:07.433524+00	43
1823	f	\N	372	Омский 95	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.434904+00	2025-10-16 17:29:07.435329+00	2025-10-16 17:29:07.435332+00	149
1824	f	\N	371	Шортандинская 2014	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.435969+00	2025-10-16 17:29:07.436268+00	2025-10-16 17:29:07.43627+00	71
1825	f	\N	370	Тамыз	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.436771+00	2025-10-16 17:29:07.437059+00	2025-10-16 17:29:07.437061+00	43
1826	f	\N	369	Увельская	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.437532+00	2025-10-16 17:29:07.437836+00	2025-10-16 17:29:07.437838+00	113
1827	f	\N	368	Эдем1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.438505+00	2025-10-16 17:29:07.438782+00	2025-10-16 17:29:07.438785+00	43
1828	f	\N	367	Дамсинская юбилейная	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.439235+00	2025-10-16 17:29:07.439519+00	2025-10-16 17:29:07.439521+00	123
1829	f	\N	365	Люция 14	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.439991+00	2025-10-16 17:29:07.440253+00	2025-10-16 17:29:07.440255+00	61
1830	f	\N	364	Уралосибирская	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.440866+00	2025-10-16 17:29:07.441321+00	2025-10-16 17:29:07.441323+00	71
1831	f	\N	363	Кокшетауский 14	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.442148+00	2025-10-16 17:29:07.442581+00	2025-10-16 17:29:07.442584+00	31
1832	f	\N	362	Омская 28 (1)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.443281+00	2025-10-16 17:29:07.443607+00	2025-10-16 17:29:07.443626+00	71
1833	f	\N	361	Омская краса 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.444167+00	2025-10-16 17:29:07.444428+00	2025-10-16 17:29:07.44443+00	71
1834	f	\N	360	Памяти Майстренко 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.44495+00	2025-10-16 17:29:07.445249+00	2025-10-16 17:29:07.445251+00	71
1835	f	\N	359	Победа 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.445736+00	2025-10-16 17:29:07.445991+00	2025-10-16 17:29:07.445993+00	71
1836	f	\N	358	Целинная 2014 (1)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.446449+00	2025-10-16 17:29:07.446733+00	2025-10-16 17:29:07.446735+00	71
1837	f	\N	357	Ханшайым	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.4472+00	2025-10-16 17:29:07.447454+00	2025-10-16 17:29:07.447456+00	61
1838	f	\N	356	Южанка 12	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.447909+00	2025-10-16 17:29:07.448171+00	2025-10-16 17:29:07.448173+00	32
1839	f	\N	355	Иртыш 22	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.448645+00	2025-10-16 17:29:07.44893+00	2025-10-16 17:29:07.448932+00	76
1840	f	\N	354	Памяти Гуцалюк	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.44955+00	2025-10-16 17:29:07.449898+00	2025-10-16 17:29:07.449902+00	5
1841	f	\N	353	Федор 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.450656+00	2025-10-16 17:29:07.45099+00	2025-10-16 17:29:07.450992+00	43
1842	f	\N	352	Заря Караганды	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.451545+00	2025-10-16 17:29:07.451833+00	2025-10-16 17:29:07.451836+00	43
1843	f	\N	351	Кайсар	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.452368+00	2025-10-16 17:29:07.452646+00	2025-10-16 17:29:07.452649+00	149
1844	f	\N	350	Патриот	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.453114+00	2025-10-16 17:29:07.453363+00	2025-10-16 17:29:07.453365+00	88
1845	f	\N	349	Шөл	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.453864+00	2025-10-16 17:29:07.454118+00	2025-10-16 17:29:07.45412+00	71
1846	f	\N	348	Памяти Лигай	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.454584+00	2025-10-16 17:29:07.454865+00	2025-10-16 17:29:07.454867+00	43
1847	f	\N	347	Яркое 6	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.455371+00	2025-10-16 17:29:07.455639+00	2025-10-16 17:29:07.455641+00	90
1848	f	\N	346	Күздік	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.456077+00	2025-10-16 17:29:07.456336+00	2025-10-16 17:29:07.456338+00	5
1849	f	\N	345	БЕРНИНА (BERNINA)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.456869+00	2025-10-16 17:29:07.457115+00	2025-10-16 17:29:07.457117+00	43
1850	f	\N	344	ОЗИРА (OSIRA)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.457809+00	2025-10-16 17:29:07.458126+00	2025-10-16 17:29:07.458128+00	43
1851	f	\N	343	НАНДИНА (NANDINA)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.458891+00	2025-10-16 17:29:07.459267+00	2025-10-16 17:29:07.45927+00	43
1852	f	\N	342	МАДЕЙРА (MADEIRA)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.45986+00	2025-10-16 17:29:07.460189+00	2025-10-16 17:29:07.460192+00	43
1853	f	\N	341	КОНКОРДИА (CONCORDIA)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.460742+00	2025-10-16 17:29:07.461038+00	2025-10-16 17:29:07.46104+00	43
1854	f	\N	340	РЕД СОНЯ (RED SONIA)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.461526+00	2025-10-16 17:29:07.461795+00	2025-10-16 17:29:07.461797+00	43
1855	f	\N	339	САНИБЕЛ (SANIBEL)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.462261+00	2025-10-16 17:29:07.462515+00	2025-10-16 17:29:07.462517+00	43
1856	f	\N	338	ЮЛИНКА (JULINKA)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.463018+00	2025-10-16 17:29:07.463275+00	2025-10-16 17:29:07.463277+00	43
1857	f	\N	337	Назым	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.463732+00	2025-10-16 17:29:07.46398+00	2025-10-16 17:29:07.463982+00	71
1858	f	\N	336	Шортандинская 2015	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.464417+00	2025-10-16 17:29:07.464699+00	2025-10-16 17:29:07.464702+00	71
1859	f	\N	335	Шымкала	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.465185+00	2025-10-16 17:29:07.465451+00	2025-10-16 17:29:07.465453+00	71
1860	f	\N	334	Экспо 2017	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.466063+00	2025-10-16 17:29:07.466366+00	2025-10-16 17:29:07.466368+00	71
1861	f	\N	333	Любава 5	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.467049+00	2025-10-16 17:29:07.467432+00	2025-10-16 17:29:07.467437+00	71
1862	f	\N	332	Солнечная	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.468106+00	2025-10-16 17:29:07.468415+00	2025-10-16 17:29:07.468418+00	71
1863	f	\N	331	Тимирязевская степная	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.468912+00	2025-10-16 17:29:07.469165+00	2025-10-16 17:29:07.469167+00	123
1864	f	\N	330	Олжа	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.469687+00	2025-10-16 17:29:07.469977+00	2025-10-16 17:29:07.469979+00	61
1865	f	\N	329	Степная 100	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.470689+00	2025-10-16 17:29:07.470955+00	2025-10-16 17:29:07.470957+00	71
1866	f	\N	328	Нур плюс 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.471419+00	2025-10-16 17:29:07.471685+00	2025-10-16 17:29:07.471687+00	119
1867	f	\N	327	Думан	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.472147+00	2025-10-16 17:29:07.472396+00	2025-10-16 17:29:07.472398+00	76
1868	f	\N	326	Ласточка	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.472882+00	2025-10-16 17:29:07.473169+00	2025-10-16 17:29:07.473171+00	102
1869	f	\N	325	Орйюн	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.473646+00	2025-10-16 17:29:07.473898+00	2025-10-16 17:29:07.4739+00	43
1870	f	\N	324	Акжаик 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.474544+00	2025-10-16 17:29:07.474893+00	2025-10-16 17:29:07.474896+00	43
1871	f	\N	323	Огонек-777 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.475602+00	2025-10-16 17:29:07.475948+00	2025-10-16 17:29:07.47595+00	126
1872	f	\N	322	Сары	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.476488+00	2025-10-16 17:29:07.476789+00	2025-10-16 17:29:07.476792+00	88
1873	f	\N	321	Мақсат 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.477364+00	2025-10-16 17:29:07.47766+00	2025-10-16 17:29:07.477662+00	43
1874	f	\N	320	Самұрық 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.47811+00	2025-10-16 17:29:07.478371+00	2025-10-16 17:29:07.478373+00	43
1875	f	\N	319	Яркое 120	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.47881+00	2025-10-16 17:29:07.47907+00	2025-10-16 17:29:07.479072+00	90
1876	f	\N	318	Солнышко	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.479521+00	2025-10-16 17:29:07.479793+00	2025-10-16 17:29:07.479795+00	60
1877	f	\N	317	Астана-109	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.480239+00	2025-10-16 17:29:07.480507+00	2025-10-16 17:29:07.480509+00	88
1878	f	\N	316	Байконур 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.481051+00	2025-10-16 17:29:07.481306+00	2025-10-16 17:29:07.481308+00	102
1879	f	\N	315	СК Оптима 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.481814+00	2025-10-16 17:29:07.482193+00	2025-10-16 17:29:07.482195+00	119
1880	f	\N	314	Селекта 301 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.483323+00	2025-10-16 17:29:07.483699+00	2025-10-16 17:29:07.483701+00	119
1881	f	\N	313	Ильич	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.484384+00	2025-10-16 17:29:07.484731+00	2025-10-16 17:29:07.484734+00	55
1882	f	\N	312	Ұлытау 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.485273+00	2025-10-16 17:29:07.485545+00	2025-10-16 17:29:07.485547+00	43
1883	f	\N	311	Раяна	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.486034+00	2025-10-16 17:29:07.486284+00	2025-10-16 17:29:07.486287+00	137
1884	f	\N	310	Карабалыкский 16	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.486742+00	2025-10-16 17:29:07.487003+00	2025-10-16 17:29:07.487005+00	97
1885	f	\N	309	Рустем	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.487461+00	2025-10-16 17:29:07.487736+00	2025-10-16 17:29:07.487739+00	55
1886	f	\N	308	Карабалыкская степная 25	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.48819+00	2025-10-16 17:29:07.48847+00	2025-10-16 17:29:07.488472+00	61
1887	f	\N	307	Алка	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.488958+00	2025-10-16 17:29:07.489223+00	2025-10-16 17:29:07.489225+00	137
1888	f	\N	306	Деспина (Despina)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.489713+00	2025-10-16 17:29:07.489998+00	2025-10-16 17:29:07.49+00	149
1889	f	\N	305	Гульшара	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.490462+00	2025-10-16 17:29:07.490779+00	2025-10-16 17:29:07.490782+00	16
1890	f	\N	304	Балкия 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.491608+00	2025-10-16 17:29:07.491974+00	2025-10-16 17:29:07.491977+00	2
1891	f	\N	303	Алаула	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.49253+00	2025-10-16 17:29:07.492848+00	2025-10-16 17:29:07.492851+00	31
1892	f	\N	302	Нур	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.493441+00	2025-10-16 17:29:07.493785+00	2025-10-16 17:29:07.493788+00	92
1893	f	\N	301	Мактаарал -4017	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.494359+00	2025-10-16 17:29:07.494638+00	2025-10-16 17:29:07.494642+00	133
1894	f	\N	300	Гульсары 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.495317+00	2025-10-16 17:29:07.495586+00	2025-10-16 17:29:07.495589+00	97
1895	f	\N	299	Тан батыр	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.496098+00	2025-10-16 17:29:07.496351+00	2025-10-16 17:29:07.496353+00	35
1896	f	\N	298	Дамана	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.49687+00	2025-10-16 17:29:07.497148+00	2025-10-16 17:29:07.49715+00	16
1897	f	\N	297	Баян 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.497637+00	2025-10-16 17:29:07.497918+00	2025-10-16 17:29:07.49792+00	135
1898	f	\N	296	Жулдыз	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.498419+00	2025-10-16 17:29:07.498899+00	2025-10-16 17:29:07.498902+00	81
1899	f	\N	295	Нарым	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.49968+00	2025-10-16 17:29:07.500219+00	2025-10-16 17:29:07.500222+00	88
1900	f	\N	294	Ақ таң	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.500933+00	2025-10-16 17:29:07.50123+00	2025-10-16 17:29:07.501232+00	31
1901	f	\N	293	Осирис 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.501821+00	2025-10-16 17:29:07.502085+00	2025-10-16 17:29:07.502087+00	97
1902	f	\N	292	ЛипКар 2014	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.502593+00	2025-10-16 17:29:07.502884+00	2025-10-16 17:29:07.502887+00	97
1903	f	\N	291	Салима-1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.503407+00	2025-10-16 17:29:07.503681+00	2025-10-16 17:29:07.503684+00	102
1904	f	\N	290	Егемен-25	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.504145+00	2025-10-16 17:29:07.504414+00	2025-10-16 17:29:07.504416+00	43
1905	f	\N	289	Еламан	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.504866+00	2025-10-16 17:29:07.505116+00	2025-10-16 17:29:07.505118+00	43
1906	f	\N	288	Краса	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.505576+00	2025-10-16 17:29:07.505888+00	2025-10-16 17:29:07.50589+00	43
1907	f	\N	287	Супер-25	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.506341+00	2025-10-16 17:29:07.506608+00	2025-10-16 17:29:07.506621+00	60
1908	f	\N	286	Карабалыкский 79 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.507137+00	2025-10-16 17:29:07.507424+00	2025-10-16 17:29:07.507427+00	149
1909	f	\N	285	Байзат	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.50805+00	2025-10-16 17:29:07.508379+00	2025-10-16 17:29:07.508381+00	76
1910	f	\N	284	Тим-Бидай	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.509108+00	2025-10-16 17:29:07.509554+00	2025-10-16 17:29:07.509557+00	71
1911	f	\N	283	Кокшетауский 17 (1)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.510156+00	2025-10-16 17:29:07.510445+00	2025-10-16 17:29:07.510448+00	31
1912	f	\N	282	Өнімді -90	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.51093+00	2025-10-16 17:29:07.51119+00	2025-10-16 17:29:07.511192+00	61
1913	f	\N	281	Чаглинская 17	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.511669+00	2025-10-16 17:29:07.511917+00	2025-10-16 17:29:07.51192+00	61
1914	f	\N	280	Зимняя Алмалы	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.512416+00	2025-10-16 17:29:07.512694+00	2025-10-16 17:29:07.512697+00	29
1915	f	\N	279	Кокжазык 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.51317+00	2025-10-16 17:29:07.513446+00	2025-10-16 17:29:07.513448+00	61
1916	f	\N	278	КИЗ-590	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.513906+00	2025-10-16 17:29:07.514159+00	2025-10-16 17:29:07.514161+00	115
1917	f	\N	277	Танзира	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.514678+00	2025-10-16 17:29:07.51494+00	2025-10-16 17:29:07.514942+00	61
1918	f	\N	276	Айзере	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.515605+00	2025-10-16 17:29:07.516001+00	2025-10-16 17:29:07.516004+00	146
1919	f	\N	275	Айна 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.516783+00	2025-10-16 17:29:07.517199+00	2025-10-16 17:29:07.517202+00	71
1920	f	\N	274	Континенталь ( Kontinental )	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.517846+00	2025-10-16 17:29:07.51816+00	2025-10-16 17:29:07.518162+00	71
1921	f	\N	273	Квинтус (Quintus)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.518667+00	2025-10-16 17:29:07.518931+00	2025-10-16 17:29:07.518933+00	71
1922	f	\N	272	Сыр Сулуы 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.519414+00	2025-10-16 17:29:07.519719+00	2025-10-16 17:29:07.519722+00	102
1923	f	\N	271	Сулу	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.520203+00	2025-10-16 17:29:07.520453+00	2025-10-16 17:29:07.520456+00	76
1924	f	\N	270	Нұрлы - 80	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.520941+00	2025-10-16 17:29:07.5212+00	2025-10-16 17:29:07.521202+00	74
1925	f	\N	268	Отан плюс	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.521694+00	2025-10-16 17:29:07.52195+00	2025-10-16 17:29:07.521952+00	119
1926	f	\N	267	Отан плюс 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.522432+00	2025-10-16 17:29:07.522748+00	2025-10-16 17:29:07.522751+00	119
1927	f	\N	266	Атлас 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.52324+00	2025-10-16 17:29:07.523483+00	2025-10-16 17:29:07.523485+00	71
1928	f	\N	265	Ай Сауле 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.523942+00	2025-10-16 17:29:07.524245+00	2025-10-16 17:29:07.524248+00	119
1929	f	\N	264	Садима 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.524903+00	2025-10-16 17:29:07.525348+00	2025-10-16 17:29:07.525351+00	16
1930	f	\N	263	JSH6138	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.526143+00	2025-10-16 17:29:07.526468+00	2025-10-16 17:29:07.52647+00	54
1931	f	\N	262	Любава 25 (1)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.527003+00	2025-10-16 17:29:07.52726+00	2025-10-16 17:29:07.527263+00	71
1932	f	\N	261	Уралосибирская 2	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.527942+00	2025-10-16 17:29:07.528203+00	2025-10-16 17:29:07.528205+00	71
1933	f	\N	260	Янтарная 60 (1)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.528699+00	2025-10-16 17:29:07.528971+00	2025-10-16 17:29:07.528974+00	71
1934	f	\N	259	Яркое юбилейное 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.529434+00	2025-10-16 17:29:07.529692+00	2025-10-16 17:29:07.529694+00	90
1935	f	\N	258	Светлячок 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.530145+00	2025-10-16 17:29:07.530398+00	2025-10-16 17:29:07.5304+00	119
1936	f	\N	257	Viktory (Виктори)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.53087+00	2025-10-16 17:29:07.531174+00	2025-10-16 17:29:07.531176+00	119
1937	f	\N	256	JSH5847 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.531706+00	2025-10-16 17:29:07.531981+00	2025-10-16 17:29:07.531984+00	54
1938	f	\N	255	Алтын	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.532589+00	2025-10-16 17:29:07.532994+00	2025-10-16 17:29:07.532997+00	55
1939	f	\N	254	Кокжазык 2	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.533649+00	2025-10-16 17:29:07.534002+00	2025-10-16 17:29:07.534005+00	61
1940	f	\N	253	Талгарская раняя	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.53455+00	2025-10-16 17:29:07.534866+00	2025-10-16 17:29:07.534868+00	17
1941	f	\N	252	Арқа ырысы	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.535391+00	2025-10-16 17:29:07.535665+00	2025-10-16 17:29:07.535667+00	149
1942	f	\N	251	Мирана	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.536152+00	2025-10-16 17:29:07.536432+00	2025-10-16 17:29:07.536434+00	16
1943	f	\N	250	Төзімді қарағай	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.536904+00	2025-10-16 17:29:07.537166+00	2025-10-16 17:29:07.537168+00	118
1944	f	\N	248	Туран 480 СВ	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.53764+00	2025-10-16 17:29:07.537934+00	2025-10-16 17:29:07.537937+00	54
1945	f	\N	247	Бэлла	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.538388+00	2025-10-16 17:29:07.538648+00	2025-10-16 17:29:07.53865+00	40
1946	f	\N	246	Зерендинский -16	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.539119+00	2025-10-16 17:29:07.539407+00	2025-10-16 17:29:07.539409+00	43
1947	f	\N	245	Памяти Искакова	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.539895+00	2025-10-16 17:29:07.540155+00	2025-10-16 17:29:07.540157+00	123
1948	f	\N	244	Алматы 1000	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.540647+00	2025-10-16 17:29:07.541127+00	2025-10-16 17:29:07.54113+00	79
1949	f	\N	243	Дамсинская 90	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.541827+00	2025-10-16 17:29:07.542224+00	2025-10-16 17:29:07.542226+00	71
1950	f	\N	242	Қоснұр 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.543074+00	2025-10-16 17:29:07.543361+00	2025-10-16 17:29:07.543364+00	88
1951	f	\N	241	Зерендинский - 17 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.543894+00	2025-10-16 17:29:07.544173+00	2025-10-16 17:29:07.544176+00	43
1952	f	\N	240	Алтын арай 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.544688+00	2025-10-16 17:29:07.544953+00	2025-10-16 17:29:07.544955+00	149
1953	f	\N	239	Карабалыкский 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.545471+00	2025-10-16 17:29:07.545754+00	2025-10-16 17:29:07.545757+00	74
1954	f	\N	238	Целинный голозерный 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.546217+00	2025-10-16 17:29:07.546468+00	2025-10-16 17:29:07.54647+00	149
1955	f	\N	237	Русия 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.546927+00	2025-10-16 17:29:07.547206+00	2025-10-16 17:29:07.547208+00	119
1956	f	\N	236	Белоглинка	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.547685+00	2025-10-16 17:29:07.547928+00	2025-10-16 17:29:07.54793+00	71
1957	f	\N	235	Барыс	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.548387+00	2025-10-16 17:29:07.548669+00	2025-10-16 17:29:07.548671+00	71
1958	f	\N	234	Акбаян	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.549214+00	2025-10-16 17:29:07.549588+00	2025-10-16 17:29:07.549591+00	106
1959	f	\N	233	Экспо 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.550225+00	2025-10-16 17:29:07.550733+00	2025-10-16 17:29:07.550737+00	88
1960	f	\N	232	Байтерек 17	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.551364+00	2025-10-16 17:29:07.551661+00	2025-10-16 17:29:07.551664+00	88
1961	f	\N	231	Даямонд Джубили	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.552204+00	2025-10-16 17:29:07.552503+00	2025-10-16 17:29:07.552506+00	63
1962	f	\N	230	Карагандинская 60	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.552974+00	2025-10-16 17:29:07.553226+00	2025-10-16 17:29:07.553228+00	71
1963	f	\N	229	Аринара	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.553714+00	2025-10-16 17:29:07.553976+00	2025-10-16 17:29:07.553978+00	79
1964	f	\N	228	ВР 808	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.55444+00	2025-10-16 17:29:07.554714+00	2025-10-16 17:29:07.554717+00	43
1965	f	\N	227	Бинго	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.555171+00	2025-10-16 17:29:07.555421+00	2025-10-16 17:29:07.555423+00	55
1966	f	\N	226	Өнімді-2020(1)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.555894+00	2025-10-16 17:29:07.556147+00	2025-10-16 17:29:07.556149+00	61
1967	f	\N	225	Нурсат	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.55662+00	2025-10-16 17:29:07.556881+00	2025-10-16 17:29:07.556883+00	146
1968	f	\N	224	Лидок	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.557417+00	2025-10-16 17:29:07.5578+00	2025-10-16 17:29:07.557803+00	16
1969	f	\N	223	Оркестра 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.558434+00	2025-10-16 17:29:07.558855+00	2025-10-16 17:29:07.558858+00	20
1970	f	\N	222	Айбони	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.559817+00	2025-10-16 17:29:07.560102+00	2025-10-16 17:29:07.560105+00	31
1971	f	\N	221	СиЭйч 201	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.560631+00	2025-10-16 17:29:07.560931+00	2025-10-16 17:29:07.560933+00	29
1972	f	\N	220	Юстесс	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.561422+00	2025-10-16 17:29:07.561722+00	2025-10-16 17:29:07.561725+00	55
1973	f	\N	219	Сары-Арқа сапасы	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.562193+00	2025-10-16 17:29:07.562456+00	2025-10-16 17:29:07.562458+00	71
1974	f	\N	218	Трованзо	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.562921+00	2025-10-16 17:29:07.563171+00	2025-10-16 17:29:07.563173+00	126
1975	f	\N	217	Хлеберже	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.563668+00	2025-10-16 17:29:07.563937+00	2025-10-16 17:29:07.563939+00	71
1976	f	\N	216	Байсары	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.564398+00	2025-10-16 17:29:07.564693+00	2025-10-16 17:29:07.564695+00	123
1977	f	\N	215	Аль-Фараби 2020	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.565173+00	2025-10-16 17:29:07.565437+00	2025-10-16 17:29:07.565439+00	71
1978	f	\N	214	Экада 247	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.566043+00	2025-10-16 17:29:07.566354+00	2025-10-16 17:29:07.566357+00	71
1979	f	\N	212	Карагандинская 31	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.56715+00	2025-10-16 17:29:07.567488+00	2025-10-16 17:29:07.567491+00	71
1980	f	\N	211	Бочонок	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.568046+00	2025-10-16 17:29:07.568316+00	2025-10-16 17:29:07.568319+00	149
1981	f	\N	210	Бостандык 19	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.568878+00	2025-10-16 17:29:07.569172+00	2025-10-16 17:29:07.569175+00	149
1982	f	\N	209	Ариранг-1хо	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.569655+00	2025-10-16 17:29:07.569916+00	2025-10-16 17:29:07.569918+00	43
1983	f	\N	208	Тамна 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.570373+00	2025-10-16 17:29:07.570635+00	2025-10-16 17:29:07.570638+00	43
1984	f	\N	204	Память ЮГК 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.571112+00	2025-10-16 17:29:07.571361+00	2025-10-16 17:29:07.571363+00	119
1985	f	\N	203	Сенна (Senna)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.571828+00	2025-10-16 17:29:07.572077+00	2025-10-16 17:29:07.572079+00	40
1986	f	\N	202	Майланған	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.572559+00	2025-10-16 17:29:07.572868+00	2025-10-16 17:29:07.57287+00	88
1987	f	\N	201	Сафия-1818	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.573341+00	2025-10-16 17:29:07.573618+00	2025-10-16 17:29:07.573621+00	82
1988	f	\N	200	Экспромт	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.574121+00	2025-10-16 17:29:07.574475+00	2025-10-16 17:29:07.574478+00	90
1989	f	\N	199	Астана 17	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.57514+00	2025-10-16 17:29:07.575942+00	2025-10-16 17:29:07.575946+00	149
1990	f	\N	198	Отолия	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.576774+00	2025-10-16 17:29:07.577087+00	2025-10-16 17:29:07.577089+00	43
1991	f	\N	197	Карелия	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.577607+00	2025-10-16 17:29:07.577904+00	2025-10-16 17:29:07.577906+00	43
1992	f	\N	196	Агробизнес 2050	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.578398+00	2025-10-16 17:29:07.578669+00	2025-10-16 17:29:07.578671+00	88
1993	f	\N	195	Лирина	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.579132+00	2025-10-16 17:29:07.579413+00	2025-10-16 17:29:07.579416+00	55
1994	f	\N	194	карагандинская 30	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.579873+00	2025-10-16 17:29:07.580123+00	2025-10-16 17:29:07.580125+00	71
1995	f	\N	193	Марал	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.580585+00	2025-10-16 17:29:07.580902+00	2025-10-16 17:29:07.580904+00	137
1996	f	\N	192	Қарлыбас	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.581381+00	2025-10-16 17:29:07.581675+00	2025-10-16 17:29:07.581677+00	31
1997	f	\N	191	Памяти Абугалиева	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.582163+00	2025-10-16 17:29:07.582452+00	2025-10-16 17:29:07.582455+00	109
1998	f	\N	190	Си Эйч 211	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.583074+00	2025-10-16 17:29:07.5834+00	2025-10-16 17:29:07.583403+00	29
1999	f	\N	185	ана	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.584074+00	2025-10-16 17:29:07.584385+00	2025-10-16 17:29:07.584387+00	96
2000	f	\N	166	Шекер	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.584947+00	2025-10-16 17:29:07.585252+00	2025-10-16 17:29:07.585254+00	109
2001	f	\N	165	Айдын-2015 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.585829+00	2025-10-16 17:29:07.586107+00	2025-10-16 17:29:07.58611+00	109
2002	f	\N	164	Аксу	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.586642+00	2025-10-16 17:29:07.586909+00	2025-10-16 17:29:07.586911+00	109
2003	f	\N	163	Кызылконыр 	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.587387+00	2025-10-16 17:29:07.587658+00	2025-10-16 17:29:07.587661+00	108
2004	f	\N	161	Сафия-1818	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.588126+00	2025-10-16 17:29:07.588373+00	2025-10-16 17:29:07.588376+00	82
2005	f	\N	160	Жетысу 5	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.588837+00	2025-10-16 17:29:07.589114+00	2025-10-16 17:29:07.589117+00	146
2006	f	\N	159	Айгерим компакт 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.589641+00	2025-10-16 17:29:07.589939+00	2025-10-16 17:29:07.589941+00	135
2007	f	\N	158	Ника 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.590434+00	2025-10-16 17:29:07.590722+00	2025-10-16 17:29:07.590725+00	122
2008	f	\N	157	Аймак 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.591622+00	2025-10-16 17:29:07.59197+00	2025-10-16 17:29:07.591972+00	135
2009	f	\N	156	Достык 15 (1)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.592694+00	2025-10-16 17:29:07.59301+00	2025-10-16 17:29:07.593012+00	122
2010	f	\N	155	Алина	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.593566+00	2025-10-16 17:29:07.593852+00	2025-10-16 17:29:07.593854+00	122
2011	f	\N	154	Айкын	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.594362+00	2025-10-16 17:29:07.594643+00	2025-10-16 17:29:07.594645+00	135
2012	f	\N	153	Казахстанская 3	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.595102+00	2025-10-16 17:29:07.595387+00	2025-10-16 17:29:07.595389+00	122
2013	f	\N	152	Бриз	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.59585+00	2025-10-16 17:29:07.59612+00	2025-10-16 17:29:07.596122+00	95
2014	f	\N	151	Талгарская ранняя	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.596565+00	2025-10-16 17:29:07.596833+00	2025-10-16 17:29:07.596835+00	17
2015	f	\N	150	Кызыл Жар	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.597284+00	2025-10-16 17:29:07.597534+00	2025-10-16 17:29:07.597536+00	95
2016	f	\N	149	Карабалыкский сизый 	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.597992+00	2025-10-16 17:29:07.598239+00	2025-10-16 17:29:07.598241+00	95
2017	f	\N	148	Колутонский (Арман)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.59877+00	2025-10-16 17:29:07.599135+00	2025-10-16 17:29:07.599137+00	95
2018	f	\N	147	Шалгын	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.599841+00	2025-10-16 17:29:07.600192+00	2025-10-16 17:29:07.600194+00	33
2019	f	\N	146	Айша 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.600813+00	2025-10-16 17:29:07.601123+00	2025-10-16 17:29:07.601126+00	33
2020	f	\N	145	Буктырма	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.601677+00	2025-10-16 17:29:07.601967+00	2025-10-16 17:29:07.601969+00	33
2021	f	\N	144	Сәуле	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.602474+00	2025-10-16 17:29:07.602773+00	2025-10-16 17:29:07.602776+00	125
2022	f	\N	143	Козы-Корпеш	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.603291+00	2025-10-16 17:29:07.603545+00	2025-10-16 17:29:07.603547+00	82
2023	f	\N	142	Курчатовская	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.60401+00	2025-10-16 17:29:07.60426+00	2025-10-16 17:29:07.604262+00	17
2024	f	\N	141	Коркем	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.604743+00	2025-10-16 17:29:07.605007+00	2025-10-16 17:29:07.605009+00	125
2025	f	\N	140	Баян-Сулу	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.605473+00	2025-10-16 17:29:07.605765+00	2025-10-16 17:29:07.605768+00	82
2026	f	\N	139	Томирис	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.606219+00	2025-10-16 17:29:07.606477+00	2025-10-16 17:29:07.606479+00	125
2027	f	\N	138	Фермерский 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.606969+00	2025-10-16 17:29:07.607229+00	2025-10-16 17:29:07.607231+00	49
2028	f	\N	137	Каз-Тай	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.608126+00	2025-10-16 17:29:07.60896+00	2025-10-16 17:29:07.608964+00	82
2029	f	\N	136	Церси 	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.609777+00	2025-10-16 17:29:07.610082+00	2025-10-16 17:29:07.610084+00	42
2030	f	\N	135	КазСиб-14	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.61068+00	2025-10-16 17:29:07.610975+00	2025-10-16 17:29:07.610977+00	49
2031	f	\N	134	Карина	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.611476+00	2025-10-16 17:29:07.611765+00	2025-10-16 17:29:07.611767+00	128
2032	f	\N	133	Юкон РЦ F1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.612209+00	2025-10-16 17:29:07.612457+00	2025-10-16 17:29:07.612459+00	5
2033	f	\N	132	Титан	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.61293+00	2025-10-16 17:29:07.613179+00	2025-10-16 17:29:07.613181+00	49
2034	f	\N	131	Эльбрус 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.613648+00	2025-10-16 17:29:07.613911+00	2025-10-16 17:29:07.613913+00	49
2035	f	\N	130	Маяк 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.614383+00	2025-10-16 17:29:07.614682+00	2025-10-16 17:29:07.614684+00	49
2036	f	\N	129	Кайнар	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.615172+00	2025-10-16 17:29:07.615438+00	2025-10-16 17:29:07.61544+00	49
2037	f	\N	128	Акмолинский изумрудный 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.615954+00	2025-10-16 17:29:07.616257+00	2025-10-16 17:29:07.61626+00	49
2038	f	\N	127	Лиманный	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.616936+00	2025-10-16 17:29:07.617711+00	2025-10-16 17:29:07.617715+00	49
2039	f	\N	126	Ишимский юбилейный	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.618492+00	2025-10-16 17:29:07.618841+00	2025-10-16 17:29:07.618843+00	49
2040	f	\N	125	Целиноградский юбилейный	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.619374+00	2025-10-16 17:29:07.619649+00	2025-10-16 17:29:07.619652+00	49
2041	f	\N	124	Афродита	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.620147+00	2025-10-16 17:29:07.620422+00	2025-10-16 17:29:07.620424+00	128
2042	f	\N	123	Акмолинский 91	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.620895+00	2025-10-16 17:29:07.621153+00	2025-10-16 17:29:07.621155+00	49
2043	f	\N	122	Тайпакский 	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.621625+00	2025-10-16 17:29:07.621916+00	2025-10-16 17:29:07.621918+00	35
2044	f	\N	121	Геракл	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.622373+00	2025-10-16 17:29:07.622634+00	2025-10-16 17:29:07.622637+00	128
2045	f	\N	120	Уральский узкоколосый 	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.623149+00	2025-10-16 17:29:07.623403+00	2025-10-16 17:29:07.623405+00	35
2046	f	\N	119	Батыс-3 (пустынный)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.624112+00	2025-10-16 17:29:07.624478+00	2025-10-16 17:29:07.62448+00	35
2047	f	\N	118	Назар (гребенчатый)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.62517+00	2025-10-16 17:29:07.625543+00	2025-10-16 17:29:07.625546+00	35
2048	f	\N	117	Батыс 9( гребневид)	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.626394+00	2025-10-16 17:29:07.626714+00	2025-10-16 17:29:07.626716+00	35
2049	f	\N	116	Сабат	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.627243+00	2025-10-16 17:29:07.627499+00	2025-10-16 17:29:07.627501+00	35
2050	f	\N	115	Нило 	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.627972+00	2025-10-16 17:29:07.628221+00	2025-10-16 17:29:07.628223+00	8
2051	f	\N	114	Далалық	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.628719+00	2025-10-16 17:29:07.628981+00	2025-10-16 17:29:07.628983+00	35
2052	f	\N	113	Черный принц 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.629464+00	2025-10-16 17:29:07.629765+00	2025-10-16 17:29:07.629768+00	8
2053	f	\N	112	Шортандинский ширлококолосый	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.630258+00	2025-10-16 17:29:07.630512+00	2025-10-16 17:29:07.630514+00	35
2054	f	\N	111	Мактаарал-5027  1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.631018+00	2025-10-16 17:29:07.631284+00	2025-10-16 17:29:07.631286+00	133
2055	f	\N	110	Бурабай 	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.631764+00	2025-10-16 17:29:07.632028+00	2025-10-16 17:29:07.632031+00	35
2056	f	\N	109	Память Ералиева	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.632644+00	2025-10-16 17:29:07.632967+00	2025-10-16 17:29:07.632969+00	133
2057	f	\N	108	Батыр	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.633676+00	2025-10-16 17:29:07.634076+00	2025-10-16 17:29:07.634079+00	35
2058	f	\N	107	Батыс-3159	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.634682+00	2025-10-16 17:29:07.634991+00	2025-10-16 17:29:07.634993+00	35
2059	f	\N	106	БТМ-4047	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.635509+00	2025-10-16 17:29:07.635803+00	2025-10-16 17:29:07.635805+00	133
2060	f	\N	105	Фарадиз 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.636268+00	2025-10-16 17:29:07.636535+00	2025-10-16 17:29:07.636537+00	57
2061	f	\N	104	Атакент-2010	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.636999+00	2025-10-16 17:29:07.637277+00	2025-10-16 17:29:07.637279+00	133
2062	f	\N	103	Шортандинский	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.637728+00	2025-10-16 17:29:07.63798+00	2025-10-16 17:29:07.637982+00	57
2063	f	\N	102	Мырзашол-80	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.638435+00	2025-10-16 17:29:07.638712+00	2025-10-16 17:29:07.638715+00	133
2064	f	\N	101	Мактаарал-4011	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.639274+00	2025-10-16 17:29:07.639559+00	2025-10-16 17:29:07.639562+00	133
2065	f	\N	100	Мактаарал-4007	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.6401+00	2025-10-16 17:29:07.640356+00	2025-10-16 17:29:07.640358+00	133
2066	f	\N	99	Береке-07	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.640966+00	2025-10-16 17:29:07.641273+00	2025-10-16 17:29:07.641276+00	133
2067	f	\N	98	Туркистан	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.641902+00	2025-10-16 17:29:07.642415+00	2025-10-16 17:29:07.642418+00	133
2068	f	\N	97	Пахтаарал-3031	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.643035+00	2025-10-16 17:29:07.643338+00	2025-10-16 17:29:07.64334+00	133
2069	f	\N	96	Мактаарал-4005	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.643842+00	2025-10-16 17:29:07.644113+00	2025-10-16 17:29:07.644116+00	133
2070	f	\N	95	Пахтаарал-3044	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.644644+00	2025-10-16 17:29:07.644917+00	2025-10-16 17:29:07.644919+00	133
2071	f	\N	94	Балғын1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.64537+00	2025-10-16 17:29:07.645637+00	2025-10-16 17:29:07.64564+00	7
2072	f	\N	93	Злато	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.646106+00	2025-10-16 17:29:07.646361+00	2025-10-16 17:29:07.646363+00	38
2073	f	\N	92	Красное чудо 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.646815+00	2025-10-16 17:29:07.647069+00	2025-10-16 17:29:07.647072+00	82
2074	f	\N	91	Пикант 	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.647527+00	2025-10-16 17:29:07.647795+00	2025-10-16 17:29:07.647797+00	82
2075	f	\N	90	Нежный	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.648263+00	2025-10-16 17:29:07.648511+00	2025-10-16 17:29:07.648513+00	104
2076	f	\N	89	Достық-10	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.649053+00	2025-10-16 17:29:07.649457+00	2025-10-16 17:29:07.649459+00	5
2077	f	\N	88	Куздик 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.650242+00	2025-10-16 17:29:07.65066+00	2025-10-16 17:29:07.650663+00	5
2078	f	\N	87	Талисман 	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.651275+00	2025-10-16 17:29:07.651579+00	2025-10-16 17:29:07.651581+00	5
2079	f	\N	86	Асар	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.652087+00	2025-10-16 17:29:07.65234+00	2025-10-16 17:29:07.652342+00	5
2080	f	\N	85	Алакөл	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.652833+00	2025-10-16 17:29:07.653082+00	2025-10-16 17:29:07.653084+00	5
2081	f	\N	84	Медок Семипалатинский	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.653503+00	2025-10-16 17:29:07.65377+00	2025-10-16 17:29:07.653772+00	5
2082	f	\N	83	Жетыген	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.654481+00	2025-10-16 17:29:07.654763+00	2025-10-16 17:29:07.654765+00	5
2083	f	\N	82	Семей	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.655232+00	2025-10-16 17:29:07.655482+00	2025-10-16 17:29:07.655484+00	5
2084	f	\N	81	Алтаир 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.65601+00	2025-10-16 17:29:07.656265+00	2025-10-16 17:29:07.656267+00	32
2085	f	\N	80	Рикура РЦ	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.656744+00	2025-10-16 17:29:07.656994+00	2025-10-16 17:29:07.656996+00	32
2086	f	\N	79	Дукрал РЦ	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.657523+00	2025-10-16 17:29:07.657975+00	2025-10-16 17:29:07.657977+00	32
2087	f	\N	78	Алаколь аруы	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.658725+00	2025-10-16 17:29:07.659053+00	2025-10-16 17:29:07.659055+00	32
2088	f	\N	77	Балшекер	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.659673+00	2025-10-16 17:29:07.660015+00	2025-10-16 17:29:07.660018+00	32
2089	f	\N	76	Ната	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.660538+00	2025-10-16 17:29:07.660833+00	2025-10-16 17:29:07.660835+00	32
2090	f	\N	75	Малика	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.661355+00	2025-10-16 17:29:07.661605+00	2025-10-16 17:29:07.661607+00	32
2091	f	\N	74	Медовая	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.662107+00	2025-10-16 17:29:07.662363+00	2025-10-16 17:29:07.662365+00	32
2092	f	\N	73	Карақай 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.662829+00	2025-10-16 17:29:07.663078+00	2025-10-16 17:29:07.66308+00	32
2093	f	\N	72	Алтыночка	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.663545+00	2025-10-16 17:29:07.663824+00	2025-10-16 17:29:07.663826+00	32
2094	f	\N	71	Майбел	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.6643+00	2025-10-16 17:29:07.664601+00	2025-10-16 17:29:07.664604+00	32
2095	f	\N	70	Джукар	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.665133+00	2025-10-16 17:29:07.665383+00	2025-10-16 17:29:07.665385+00	32
2096	f	\N	69	Реймиел	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.665871+00	2025-10-16 17:29:07.666226+00	2025-10-16 17:29:07.666229+00	32
2097	f	\N	68	Карибеан голд	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.666926+00	2025-10-16 17:29:07.667312+00	2025-10-16 17:29:07.667315+00	32
2098	f	\N	67	Мирелла	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.668009+00	2025-10-16 17:29:07.668317+00	2025-10-16 17:29:07.66832+00	32
2099	f	\N	66	Жиеншар	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.668879+00	2025-10-16 17:29:07.669168+00	2025-10-16 17:29:07.669171+00	32
2100	f	\N	65	Ерке	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.669677+00	2025-10-16 17:29:07.669965+00	2025-10-16 17:29:07.669967+00	32
2101	f	\N	64	Дамели	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.670424+00	2025-10-16 17:29:07.670697+00	2025-10-16 17:29:07.670699+00	32
2102	f	\N	63	Прима	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.671167+00	2025-10-16 17:29:07.671414+00	2025-10-16 17:29:07.671416+00	32
2103	f	\N	61	Сырдарья	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.671878+00	2025-10-16 17:29:07.672129+00	2025-10-16 17:29:07.672131+00	32
2104	f	\N	60	Кемель	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.672619+00	2025-10-16 17:29:07.672901+00	2025-10-16 17:29:07.672903+00	146
2105	f	\N	59	Никотер	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.673391+00	2025-10-16 17:29:07.673659+00	2025-10-16 17:29:07.673662+00	146
2106	f	\N	58	Никогрин	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.674289+00	2025-10-16 17:29:07.67463+00	2025-10-16 17:29:07.674632+00	146
2107	f	\N	57	Иссилькульская	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.675217+00	2025-10-16 17:29:07.675507+00	2025-10-16 17:29:07.675509+00	9
2108	f	\N	56	полудинская	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.676066+00	2025-10-16 17:29:07.676429+00	2025-10-16 17:29:07.676432+00	9
2109	f	\N	55	Жоғары қарағай 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.676987+00	2025-10-16 17:29:07.677263+00	2025-10-16 17:29:07.677265+00	118
2110	f	\N	54	Төзімді қарағай	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.677768+00	2025-10-16 17:29:07.678061+00	2025-10-16 17:29:07.678064+00	118
2111	f	\N	53	Боровская-44	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.678535+00	2025-10-16 17:29:07.678815+00	2025-10-16 17:29:07.678818+00	118
2112	f	\N	52	Боровская-22	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.679271+00	2025-10-16 17:29:07.679551+00	2025-10-16 17:29:07.679554+00	118
2113	f	\N	51	Чебаркульская	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.680015+00	2025-10-16 17:29:07.68028+00	2025-10-16 17:29:07.680282+00	118
2114	f	\N	50	Аракарагайская	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.68092+00	2025-10-16 17:29:07.681174+00	2025-10-16 17:29:07.681176+00	118
2115	f	\N	49	Урумкайская 53	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.681671+00	2025-10-16 17:29:07.681954+00	2025-10-16 17:29:07.681956+00	118
2116	f	\N	48	Боровская 30	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.682545+00	2025-10-16 17:29:07.682948+00	2025-10-16 17:29:07.682951+00	118
2117	f	\N	47	Урумкайская 38	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.683723+00	2025-10-16 17:29:07.684055+00	2025-10-16 17:29:07.684058+00	118
2118	f	\N	46	Ассоль	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.684556+00	2025-10-16 17:29:07.684849+00	2025-10-16 17:29:07.684851+00	131
2119	f	\N	45	Инжу 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.685321+00	2025-10-16 17:29:07.685605+00	2025-10-16 17:29:07.685607+00	119
2120	f	\N	44	Жасыл дэн	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.686102+00	2025-10-16 17:29:07.686379+00	2025-10-16 17:29:07.686381+00	65
2121	f	\N	43	Дербес	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.686832+00	2025-10-16 17:29:07.687083+00	2025-10-16 17:29:07.687085+00	69
2122	f	\N	42	Медуза 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.687533+00	2025-10-16 17:29:07.687812+00	2025-10-16 17:29:07.687814+00	81
2123	f	\N	41	Ақжол 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.688292+00	2025-10-16 17:29:07.68854+00	2025-10-16 17:29:07.688542+00	140
2124	f	\N	40	Атамекен	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.689016+00	2025-10-16 17:29:07.689266+00	2025-10-16 17:29:07.689268+00	45
2125	f	\N	39	Ақтоғай 1	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.689768+00	2025-10-16 17:29:07.690163+00	2025-10-16 17:29:07.690165+00	62
2126	f	\N	38	Сладкий боб 	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.690653+00	2025-10-16 17:29:07.691038+00	2025-10-16 17:29:07.69104+00	20
2127	f	\N	37	ССГ КИЗ-2	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.691608+00	2025-10-16 17:29:07.691946+00	2025-10-16 17:29:07.691949+00	115
2128	f	\N	36	ССГ КИЗ-3	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.69297+00	2025-10-16 17:29:07.693359+00	2025-10-16 17:29:07.693361+00	115
2129	f	\N	35	Жамиля 	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.693926+00	2025-10-16 17:29:07.694234+00	2025-10-16 17:29:07.694236+00	22
2130	f	\N	34	Өскемен	\N	\N	\N	\N	\N		f		\N	2025-10-16 17:29:07.694732+00	2025-10-16 17:29:07.694989+00	2025-10-16 17:29:07.694991+00	103
615	f	\N	1617	Арман		1	1	1	1	\N	f	\N	\N	2025-10-20 09:58:43.716081+00	2025-10-16 17:29:06.447738+00	2025-10-20 09:58:43.716127+00	76
2133	t	2025-10-21 22:07:24.864521+00	2248	Тестовый сорт CRUD	\N	\N	\N	\N	\N		f		\N	2025-10-21 22:06:13.47396+00	2025-10-21 22:06:13.474339+00	2025-10-21 22:07:24.864603+00	3
\.


--
-- Data for Name: trials_app_trial; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.trials_app_trial (id, is_deleted, deleted_at, area_ha, planting_season, agro_background, growing_conditions, cultivation_technology, growing_method, harvest_timing, harvest_date, additional_info, status, start_date, year, responsible_person, laboratory_status, laboratory_sent_date, laboratory_completed_date, laboratory_sample_weight, laboratory_sample_source, laboratory_notes, created_at, updated_at, created_by_id, culture_id, predecessor_culture_id, region_id, trial_plan_id, trial_type_id, maturity_group_code, maturity_group_name, lsd_095, error_mean, accuracy_percent, replication_count, trial_code, culture_code, predecessor_code, responsible_person_title, approval_date, patents_culture_id) FROM stdin;
10	f	\N	0.5000	spring	favorable	rainfed	organic	greenhouse	medium_early	2025-10-02		completed	2025-10-01	2023	Иванов	completed	2025-10-17	2025-10-17	2	Иванов		2025-10-16 21:31:03.312675+00	2025-10-17 09:57:28.28062+00	1	1	\N	50	1	1	D07	Среднеранний	0.69	0.35	3.25	4	САР-2023-D07	ПШЕ	fallow	\N	2025-10-17	\N
11	f	\N	0.5000	spring	moderate	rainfed	traditional	hydroponics	medium_early	2025-10-16		completed	2025-10-01	2023	Патриция	completed	2025-10-17	2025-10-17	2	TEst		2025-10-17 09:59:34.487773+00	2025-10-17 10:32:12.556731+00	1	1	\N	47	1	1	D07	Среднеранний	0.45	0.23	2.53	4	КЕР-2023-D07	ПШЕ	fallow	\N	2025-10-17	\N
14	f	\N	0.5000	spring	moderate	drained	traditional	hydroponics	early	2025-09-30		completed	2025-10-15	2024	Ивнано	completed	2025-10-17	2025-10-17	2	ew		2025-10-17 10:42:24.431961+00	2025-10-17 10:57:30.493824+00	1	1	\N	50	2	1	D07	Среднеранний	0.16	0.08	1.45	4	КЕР-2024-D07	ПШЕ	fallow	\N	2025-10-17	\N
21	f	\N	0.5000	spring	favorable	irrigated	minimal	hydroponics	medium	2025-10-01		active	2025-10-08	2025	Иванов Иван	\N	\N	\N	\N	\N	\N	2025-10-20 10:02:28.306672+00	2025-10-20 10:13:15.490903+00	1	1	\N	50	3	1	D07	Среднеранний	\N	\N	\N	4	КЕР-2025-D07	ПШЕ	fallow	\N	\N	\N
12	f	\N	0.5000	spring	moderate	rainfed	organic	hydroponics	medium_early	2025-10-03		completed	2025-10-01	2023	цфчыф	completed	2025-10-17	2025-10-17	2	sa		2025-10-17 10:00:14.703261+00	2025-10-17 10:37:18.378662+00	1	1	\N	48	1	1	D07	Среднеранний	0.76	0.39	3.31	4	КОГ-2023-D07	ПШЕ	fallow	\N	2025-10-17	\N
13	f	\N	0.5000	spring	moderate	rainfed	minimal	hydroponics	medium_early	2025-10-01		completed	2025-10-08	2024	Иванов Иван	completed	2025-10-17	2025-10-17	2	323		2025-10-17 10:42:12.402809+00	2025-10-17 10:54:39.37751+00	1	1	\N	48	2	1	D07	Среднеранний	0.13	0.07	0.41	4	САР-2024-D07	ПШЕ	fallow	\N	2025-10-17	\N
18	f	\N	0.5000	spring	unfavorable	rainfed	traditional	greenhouse	medium	2025-10-01		completed	2025-10-01	2025	Иванов	completed	2025-10-18	2025-10-18	2	Делянка 5		2025-10-18 11:48:59.705958+00	2025-10-18 12:53:08.340191+00	1	1	\N	48	3	1	D03	Средний (среднеспелый)	1.7	0.52	3.17	4	САР-2025-D03	ПШЕ	fallow	\N	2025-10-18	\N
20	f	\N	0.5000	spring	moderate	irrigated	traditional	\N	medium	2025-10-01		completed	2025-10-08	2025	Иванов Иван	completed	2025-10-20	2025-10-20	2.5	Поле 1		2025-10-20 10:02:28.248193+00	2025-10-20 10:22:52.579079+00	1	1	\N	50	3	1	D03	Средний (среднеспелый)	21.67	6.71	34.62	4	КЕР-2025-D03	ПШЕ	fallow	\N	2025-10-20	\N
17	f	\N	0.5000	spring	\N	rainfed	traditional	\N	\N	\N	\N	active	2025-10-01	2025	Иванов Иван	\N	\N	\N	\N	\N	\N	2025-10-17 21:08:25.139729+00	2025-10-20 09:53:18.906324+00	1	1	\N	47	3	1	D07	Среднеранний	\N	\N	\N	4	КОГ-2025-D07	ПШЕ	fallow	\N	\N	\N
16	f	\N	0.5000	spring	moderate	rainfed	traditional	hydroponics	medium	2025-10-01		completed	2025-10-01	2025	Иванов Иван	completed	2025-10-18	2025-10-18	2	АГронам		2025-10-17 21:08:25.06052+00	2025-10-18 11:48:31.368944+00	1	1	\N	47	3	1	D03	Средний (среднеспелый)	4.08	1.26	14.49	4	КОГ-2025-D03	ПШЕ	fallow	\N	2025-10-18	\N
19	f	\N	0.5000	spring	\N	rainfed	traditional	\N	\N	\N	\N	active	2025-10-01	2025	Иванов	\N	\N	\N	\N	\N	\N	2025-10-18 11:48:59.795618+00	2025-10-18 11:48:59.795624+00	1	1	\N	48	3	1	D07	Среднеранний	\N	\N	\N	4	САР-2025-D07	ПШЕ	fallow	\N	\N	\N
15	f	\N	0.5000	spring	moderate	rainfed	traditional	greenhouse	medium_early	2025-10-02		completed	2025-10-01	2024	hjh	completed	2025-10-17	2025-10-17	2	6tty		2025-10-17 10:45:03.983932+00	2025-10-17 12:01:01.777556+00	1	1	\N	47	2	1	D07	Среднеранний	0.11	0.06	0.24	4	КОГ-2024-D07	ПШЕ	fallow	\N	2025-10-17	\N
\.


--
-- Data for Name: trials_app_trial_indicators; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.trials_app_trial_indicators (id, trial_id, indicator_id) FROM stdin;
97	10	4
98	10	6
99	10	8
100	10	7
101	11	1
102	11	10
103	11	14
104	11	18
105	11	20
106	11	22
107	11	24
108	12	1
109	12	10
110	12	14
111	12	18
112	12	20
113	12	22
114	12	24
115	13	1
116	13	10
117	13	14
118	13	18
119	13	20
120	13	22
121	13	24
122	14	1
123	14	10
124	14	14
125	14	18
126	14	20
127	14	22
128	14	24
129	15	1
130	15	10
131	15	14
132	15	18
133	15	20
134	15	22
135	15	24
137	15	4
138	15	5
139	15	9
140	16	1
141	16	10
142	16	14
143	16	18
144	16	20
146	16	24
147	17	1
148	17	10
149	17	14
151	17	20
153	17	24
154	17	5
155	17	6
156	17	17
157	17	7
76	10	1
77	10	10
78	10	14
79	10	18
80	10	20
81	10	22
82	10	24
158	17	21
159	17	4
160	17	53
161	17	19
162	17	18
163	16	4
164	16	5
165	16	6
166	16	7
167	16	17
168	16	19
169	16	21
170	16	53
171	16	28
172	18	1
173	18	10
174	18	14
177	19	1
178	19	10
179	19	14
180	19	20
181	19	23
182	18	6
183	18	7
185	18	17
186	18	18
187	18	5
188	18	4
189	18	21
190	18	28
191	18	53
192	18	8
193	18	19
195	18	23
196	20	1
197	20	10
198	20	14
199	21	1
200	21	10
201	21	14
202	21	4
203	21	6
204	21	7
205	21	8
206	21	9
207	21	18
208	21	20
\.


--
-- Data for Name: trials_app_triallaboratoryresult; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.trials_app_triallaboratoryresult (id, is_deleted, deleted_at, value, text_value, analysis_date, sample_weight_kg, notes, created_at, updated_at, created_by_id, indicator_id, participant_id, trial_id) FROM stdin;
1	f	\N	43	\N	2025-10-17	\N	\N	2025-10-17 09:57:07.673679+00	2025-10-17 09:57:07.673693+00	1	14	20	10
2	f	\N	55	\N	2025-10-17	\N	\N	2025-10-17 09:57:07.679079+00	2025-10-17 09:57:07.679089+00	1	24	20	10
3	f	\N	32	\N	2025-10-17	\N	\N	2025-10-17 09:57:15.653809+00	2025-10-17 09:57:15.653821+00	1	14	21	10
4	f	\N	32	\N	2025-10-17	\N	\N	2025-10-17 09:57:15.658281+00	2025-10-17 09:57:15.658289+00	1	24	21	10
5	f	\N	32	\N	2025-10-17	\N	\N	2025-10-17 09:57:18.539867+00	2025-10-17 09:57:18.53988+00	1	14	22	10
6	f	\N	32	\N	2025-10-17	\N	\N	2025-10-17 09:57:18.544472+00	2025-10-17 09:57:18.544482+00	1	24	22	10
7	f	\N	11	\N	2025-10-17	\N	\N	2025-10-17 10:32:01.423861+00	2025-10-17 10:32:01.423874+00	1	14	23	11
8	f	\N	21	\N	2025-10-17	\N	\N	2025-10-17 10:32:01.427517+00	2025-10-17 10:32:01.427525+00	1	24	23	11
9	f	\N	12	\N	2025-10-17	\N	\N	2025-10-17 10:32:04.418822+00	2025-10-17 10:32:04.418838+00	1	14	24	11
10	f	\N	21	\N	2025-10-17	\N	\N	2025-10-17 10:32:04.422367+00	2025-10-17 10:32:04.422374+00	1	24	24	11
11	f	\N	12	\N	2025-10-17	\N	\N	2025-10-17 10:32:07.38464+00	2025-10-17 10:32:07.384653+00	1	14	25	11
12	f	\N	21	\N	2025-10-17	\N	\N	2025-10-17 10:32:07.388899+00	2025-10-17 10:32:07.38891+00	1	24	25	11
13	f	\N	1	\N	2025-10-17	\N	\N	2025-10-17 10:37:07.432389+00	2025-10-17 10:37:07.432398+00	1	14	26	12
14	f	\N	1	\N	2025-10-17	\N	\N	2025-10-17 10:37:07.436224+00	2025-10-17 10:37:07.436229+00	1	24	26	12
15	f	\N	2	\N	2025-10-17	\N	\N	2025-10-17 10:37:10.056274+00	2025-10-17 10:37:10.056287+00	1	14	27	12
16	f	\N	2	\N	2025-10-17	\N	\N	2025-10-17 10:37:10.060401+00	2025-10-17 10:37:10.060409+00	1	24	27	12
17	f	\N	2	\N	2025-10-17	\N	\N	2025-10-17 10:37:13.391212+00	2025-10-17 10:37:13.391225+00	1	14	28	12
18	f	\N	12	\N	2025-10-17	\N	\N	2025-10-17 10:37:13.395844+00	2025-10-17 10:37:13.395854+00	1	24	28	12
19	f	\N	4	\N	2025-10-17	\N	\N	2025-10-17 12:00:49.930807+00	2025-10-17 12:00:49.930819+00	1	14	35	15
20	f	\N	4	\N	2025-10-17	\N	\N	2025-10-17 12:00:49.935334+00	2025-10-17 12:00:49.935343+00	1	24	35	15
21	f	\N	3	\N	2025-10-17	\N	\N	2025-10-17 12:00:52.995236+00	2025-10-17 12:00:52.995247+00	1	14	36	15
22	f	\N	3	\N	2025-10-17	\N	\N	2025-10-17 12:00:52.999831+00	2025-10-17 12:00:52.999841+00	1	24	36	15
23	f	\N	3	\N	2025-10-17	\N	\N	2025-10-17 12:00:56.529759+00	2025-10-17 12:00:56.529772+00	1	14	37	15
24	f	\N	5	\N	2025-10-17	\N	\N	2025-10-17 12:00:56.533498+00	2025-10-17 12:00:56.533506+00	1	24	37	15
\.


--
-- Data for Name: trials_app_trialparticipant; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.trials_app_trialparticipant (id, is_deleted, deleted_at, statistical_group, statistical_result, participant_number, created_at, updated_at, application_id, sort_record_id, trial_id, maturity_group_code) FROM stdin;
33	f	\N	1	-24	2	2025-10-17 10:42:24.454394+00	2025-10-17 10:57:13.393452+00	1	1	14	D07
47	f	\N	1	\N	1	2025-10-18 11:48:59.798375+00	2025-10-18 11:48:59.801131+00	1	1	19	D07
37	f	\N	1	-13	3	2025-10-17 10:45:04.013344+00	2025-10-17 12:00:00.021289+00	1	1	15	D07
22	f	\N	1	0	3	2025-10-16 21:31:03.34296+00	2025-10-17 09:18:49.690174+00	1	1	10	D07
25	f	\N	1	-2	3	2025-10-17 09:59:34.517945+00	2025-10-17 10:29:57.179841+00	1	1	11	D07
52	f	\N	1	\N	1	2025-10-20 10:02:28.30932+00	2025-10-20 10:13:15.514174+00	1	1	21	D07
43	f	\N	1	1	1	2025-10-18 11:48:59.714873+00	2025-10-18 12:43:47.887475+00	5	5	18	D03
44	f	\N	1	1	2	2025-10-18 11:48:59.726407+00	2025-10-18 12:43:47.891338+00	4	4	18	D03
45	f	\N	0	0	3	2025-10-18 11:48:59.732761+00	2025-10-18 12:43:47.892095+00	3	3	18	D03
46	f	\N	0	0	4	2025-10-18 11:48:59.737248+00	2025-10-18 12:43:47.89281+00	2	2	18	D03
21	f	\N	0	0	2	2025-10-16 21:31:03.335249+00	2025-10-17 09:18:49.687517+00	3	3	10	D03
28	f	\N	1	-1	3	2025-10-17 10:00:14.730507+00	2025-10-17 10:36:02.290458+00	1	1	12	D07
29	f	\N	1	-24	1	2025-10-17 10:42:12.412169+00	2025-10-17 10:54:16.229161+00	2	2	13	D03
23	f	\N	1	3	1	2025-10-17 09:59:34.497781+00	2025-10-17 10:29:57.17499+00	2	2	11	D03
31	f	\N	0	0	3	2025-10-17 10:42:12.432749+00	2025-10-17 10:54:16.233315+00	3	3	13	D03
27	f	\N	0	0	2	2025-10-17 10:00:14.722986+00	2025-10-17 10:36:02.287255+00	3	3	12	D03
26	f	\N	1	4	1	2025-10-17 10:00:14.711708+00	2025-10-17 10:36:02.286222+00	2	2	12	D03
35	f	\N	1	7	1	2025-10-17 10:45:03.994754+00	2025-10-17 12:00:00.017174+00	2	2	15	D03
20	f	\N	1	0	1	2025-10-16 21:31:03.323385+00	2025-10-17 09:18:49.686694+00	2	2	10	D03
30	f	\N	1	-13	2	2025-10-17 10:42:12.42499+00	2025-10-17 10:54:16.232367+00	1	1	13	D07
24	f	\N	0	0	2	2025-10-17 09:59:34.510664+00	2025-10-17 10:29:57.176262+00	3	3	11	D03
36	f	\N	0	0	2	2025-10-17 10:45:04.005359+00	2025-10-17 12:00:00.01793+00	3	3	15	D03
32	f	\N	1	-3	1	2025-10-17 10:42:24.441411+00	2025-10-17 10:57:13.390575+00	2	2	14	D03
34	f	\N	0	0	3	2025-10-17 10:42:24.462646+00	2025-10-17 10:57:13.394258+00	3	3	14	D03
38	f	\N	1	0	1	2025-10-17 21:08:25.068089+00	2025-10-18 11:28:42.009305+00	5	5	16	D03
39	f	\N	1	0	2	2025-10-17 21:08:25.079317+00	2025-10-18 11:28:42.01316+00	4	4	16	D03
48	f	\N	1	0	1	2025-10-20 10:02:28.258571+00	2025-10-20 10:21:51.207241+00	5	5	20	D03
42	f	\N	1	\N	1	2025-10-17 21:08:25.142437+00	2025-10-20 09:53:18.951006+00	1	1	17	D07
40	f	\N	0	0	3	2025-10-17 21:08:25.08733+00	2025-10-18 11:28:42.014275+00	3	3	16	D03
41	f	\N	0	0	4	2025-10-17 21:08:25.093967+00	2025-10-18 11:28:42.015093+00	2	2	16	D03
49	f	\N	1	0	2	2025-10-20 10:02:28.267767+00	2025-10-20 10:21:51.211969+00	4	4	20	D03
50	f	\N	0	0	3	2025-10-20 10:02:28.272217+00	2025-10-20 10:21:51.212904+00	3	3	20	D03
51	f	\N	0	0	4	2025-10-20 10:02:28.275251+00	2025-10-20 10:21:51.213724+00	2	2	20	D03
\.


--
-- Data for Name: trials_app_trialplan; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.trials_app_trialplan (id, is_deleted, deleted_at, year, status, participants, created_at, updated_at, created_by_id, oblast_id, trial_type_id, total_participants) FROM stdin;
1	f	\N	2023	structured	{}	2025-10-16 09:04:57.368637+00	2025-10-16 17:04:29.290733+00	1	17	\N	4
2	f	\N	2024	structured	{}	2025-10-17 09:58:08.732204+00	2025-10-17 10:44:02.962281+00	1	17	\N	3
3	f	\N	2025	structured	{}	2025-10-17 12:07:09.104244+00	2025-10-17 12:11:29.547597+00	1	17	\N	5
4	f	\N	2025	planned	{}	2025-10-20 09:59:01.696445+00	2025-10-20 09:59:01.701818+00	1	14	\N	0
5	f	\N	2025	planned	{}	2025-10-20 10:00:15.542391+00	2025-10-20 10:00:15.547472+00	1	7	\N	0
\.


--
-- Data for Name: trials_app_trialplanculture; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.trials_app_trialplanculture (id, is_deleted, deleted_at, created_at, updated_at, created_by_id, culture_id, trial_plan_id) FROM stdin;
1	f	\N	2025-10-16 09:05:04.505172+00	2025-10-16 09:05:04.505183+00	1	1	1
2	f	\N	2025-10-17 09:58:20.725831+00	2025-10-17 09:58:20.725843+00	1	1	2
3	f	\N	2025-10-17 12:07:17.208843+00	2025-10-17 12:07:17.208853+00	1	1	3
4	f	\N	2025-10-20 09:59:13.380955+00	2025-10-20 09:59:13.380972+00	1	1	4
5	f	\N	2025-10-20 10:00:24.234232+00	2025-10-20 10:00:24.234248+00	1	1	5
\.


--
-- Data for Name: trials_app_trialplanculturetrialtype; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.trials_app_trialplanculturetrialtype (id, is_deleted, deleted_at, created_at, updated_at, created_by_id, trial_plan_culture_id, trial_type_id, season) FROM stdin;
1	f	\N	2025-10-16 09:07:20.49279+00	2025-10-16 09:07:20.492799+00	1	1	1	spring
3	f	\N	2025-10-17 09:58:28.022206+00	2025-10-17 09:58:28.022217+00	1	2	1	spring
4	f	\N	2025-10-17 12:07:27.182156+00	2025-10-17 12:07:27.182168+00	1	3	1	spring
5	f	\N	2025-10-20 09:59:19.952907+00	2025-10-20 09:59:19.95292+00	1	4	4	spring
6	f	\N	2025-10-20 10:00:28.885563+00	2025-10-20 10:00:28.885576+00	1	5	4	spring
\.


--
-- Data for Name: trials_app_trialplanparticipant; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.trials_app_trialplanparticipant (id, is_deleted, deleted_at, patents_sort_id, statistical_group, seeds_provision, participant_number, maturity_group, created_at, updated_at, application_id, created_by_id, culture_trial_type_id) FROM stdin;
3	f	\N	2242	1	provided	1	D07	2025-10-16 11:15:36.29253+00	2025-10-16 11:15:36.292553+00	2	1	1
5	f	\N	2241	1	provided	3	D07	2025-10-16 11:21:00.461836+00	2025-10-16 11:21:00.461841+00	1	1	1
7	f	\N	2244	1	not_provided	4	D01	2025-10-16 17:04:29.282117+00	2025-10-16 17:04:29.282128+00	\N	1	1
4	f	\N	1926	0	provided	2	D07	2025-10-16 11:21:00.457264+00	2025-10-16 11:21:00.457269+00	3	1	1
8	f	\N	2242	1	provided	1	D07	2025-10-17 10:39:14.202221+00	2025-10-17 10:39:14.202233+00	2	1	3
9	f	\N	2241	1	provided	2	D07	2025-10-17 10:39:14.208638+00	2025-10-17 10:39:14.208643+00	1	1	3
10	f	\N	1926	0	provided	3	D07	2025-10-17 10:39:14.211609+00	2025-10-17 10:39:14.211614+00	3	1	3
11	f	\N	2243	1	provided	1	D03	2025-10-17 12:11:29.529415+00	2025-10-17 12:11:29.529425+00	5	1	4
12	f	\N	2244	1	provided	2	D03	2025-10-17 12:11:29.534201+00	2025-10-17 12:11:29.534208+00	4	1	4
15	f	\N	2241	1	provided	5	D07	2025-10-17 12:11:29.545446+00	2025-10-17 12:11:29.545452+00	1	1	4
14	f	\N	2242	0	provided	4	D03	2025-10-17 12:11:29.541836+00	2025-10-17 12:11:29.541841+00	2	1	4
13	f	\N	1926	0	provided	3	D03	2025-10-17 12:11:29.537781+00	2025-10-17 12:11:29.537786+00	3	1	4
\.


--
-- Data for Name: trials_app_trialplantrial; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.trials_app_trialplantrial (id, is_deleted, deleted_at, predecessor, seeding_rate, season, created_at, updated_at, created_by_id, participant_id, region_id) FROM stdin;
1	f	\N	fallow	5	spring	2025-10-16 11:21:00.451176+00	2025-10-16 11:21:00.451186+00	1	3	48
2	f	\N	fallow	5	spring	2025-10-16 11:21:00.454231+00	2025-10-16 11:21:00.454237+00	1	3	47
3	f	\N	fallow	5	spring	2025-10-16 11:21:00.454838+00	2025-10-16 11:21:00.454843+00	1	3	50
4	f	\N	fallow	5	spring	2025-10-16 11:21:00.458263+00	2025-10-16 11:21:00.45827+00	1	4	48
5	f	\N	fallow	5	spring	2025-10-16 11:21:00.459073+00	2025-10-16 11:21:00.45908+00	1	4	47
6	f	\N	fallow	5	spring	2025-10-16 11:21:00.45984+00	2025-10-16 11:21:00.459845+00	1	4	50
7	f	\N	fallow	5	spring	2025-10-16 11:21:00.462553+00	2025-10-16 11:21:00.462557+00	1	5	48
8	f	\N	fallow	5	spring	2025-10-16 11:21:00.462966+00	2025-10-16 11:21:00.46297+00	1	5	47
9	f	\N	fallow	5	spring	2025-10-16 11:21:00.463357+00	2025-10-16 11:21:00.463361+00	1	5	50
11	f	\N	fallow	5	spring	2025-10-16 17:04:29.284865+00	2025-10-16 17:04:29.284875+00	1	7	48
12	f	\N	fallow	5	spring	2025-10-17 10:39:14.204823+00	2025-10-17 10:39:14.20483+00	1	8	50
13	f	\N	fallow	5	spring	2025-10-17 10:39:14.206385+00	2025-10-17 10:39:14.20639+00	1	8	48
14	f	\N	fallow	5	spring	2025-10-17 10:39:14.206884+00	2025-10-17 10:39:14.206887+00	1	8	48
15	f	\N	fallow	5	spring	2025-10-17 10:39:14.209261+00	2025-10-17 10:39:14.20927+00	1	9	50
16	f	\N	fallow	5	spring	2025-10-17 10:39:14.209741+00	2025-10-17 10:39:14.209747+00	1	9	48
17	f	\N	fallow	5	spring	2025-10-17 10:39:14.210168+00	2025-10-17 10:39:14.210172+00	1	9	48
18	f	\N	fallow	5	spring	2025-10-17 10:39:14.212361+00	2025-10-17 10:39:14.21237+00	1	10	50
19	f	\N	fallow	5	spring	2025-10-17 10:39:14.212999+00	2025-10-17 10:39:14.213005+00	1	10	48
20	f	\N	fallow	5	spring	2025-10-17 10:39:14.213832+00	2025-10-17 10:39:14.213839+00	1	10	48
21	f	\N	fallow	5	spring	2025-10-17 10:44:02.955774+00	2025-10-17 10:44:02.955821+00	1	8	47
22	f	\N	fallow	5	spring	2025-10-17 10:44:02.959564+00	2025-10-17 10:44:02.95957+00	1	10	47
23	f	\N	fallow	5	spring	2025-10-17 10:44:02.961013+00	2025-10-17 10:44:02.961018+00	1	9	47
24	f	\N	fallow	5	spring	2025-10-17 12:11:29.530849+00	2025-10-17 12:11:29.530854+00	1	11	48
25	f	\N	fallow	5	spring	2025-10-17 12:11:29.531787+00	2025-10-17 12:11:29.531792+00	1	11	50
26	f	\N	fallow	5	spring	2025-10-17 12:11:29.532298+00	2025-10-17 12:11:29.532302+00	1	11	47
27	f	\N	fallow	5	spring	2025-10-17 12:11:29.534658+00	2025-10-17 12:11:29.534663+00	1	12	48
28	f	\N	fallow	5	spring	2025-10-17 12:11:29.535328+00	2025-10-17 12:11:29.535335+00	1	12	50
29	f	\N	fallow	5	spring	2025-10-17 12:11:29.535956+00	2025-10-17 12:11:29.535961+00	1	12	47
30	f	\N	fallow	5	spring	2025-10-17 12:11:29.538251+00	2025-10-17 12:11:29.538256+00	1	13	48
31	f	\N	fallow	5	spring	2025-10-17 12:11:29.538643+00	2025-10-17 12:11:29.538646+00	1	13	50
32	f	\N	fallow	5	spring	2025-10-17 12:11:29.540216+00	2025-10-17 12:11:29.540222+00	1	13	47
33	f	\N	fallow	5	spring	2025-10-17 12:11:29.542239+00	2025-10-17 12:11:29.542243+00	1	14	48
34	f	\N	fallow	5	spring	2025-10-17 12:11:29.542779+00	2025-10-17 12:11:29.542782+00	1	14	50
35	f	\N	fallow	5	spring	2025-10-17 12:11:29.543346+00	2025-10-17 12:11:29.543354+00	1	14	47
36	f	\N	fallow	5	spring	2025-10-17 12:11:29.545898+00	2025-10-17 12:11:29.545902+00	1	15	48
37	f	\N	fallow	5	spring	2025-10-17 12:11:29.546236+00	2025-10-17 12:11:29.54624+00	1	15	50
38	f	\N	fallow	5	spring	2025-10-17 12:11:29.546566+00	2025-10-17 12:11:29.546569+00	1	15	47
\.


--
-- Data for Name: trials_app_trialresult; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.trials_app_trialresult (id, is_deleted, deleted_at, value, text_value, measurement_date, notes, created_at, updated_at, created_by_id, indicator_id, participant_id, sort_record_id, trial_id, plot_1, plot_2, plot_3, plot_4, is_rejected, rejection_reason, is_restored) FROM stdin;
145	f	\N	6	\N	2025-10-02	\N	2025-10-17 06:50:32.487569+00	2025-10-17 09:18:49.67293+00	1	7	22	1	10	\N	\N	\N	\N	f	\N	f
132	f	\N	32.3	\N	2025-10-02	\N	2025-10-16 21:31:03.346703+00	2025-10-17 09:18:49.675175+00	1	10	22	1	10	\N	\N	\N	\N	f	\N	f
133	f	\N	32	\N	2025-10-02	\N	2025-10-16 21:31:03.347609+00	2025-10-17 09:18:49.67775+00	1	18	22	1	10	\N	\N	\N	\N	f	\N	f
131	f	\N	2.3	\N	2025-10-02	\N	2025-10-16 21:31:03.344812+00	2025-10-17 09:18:49.679952+00	1	1	22	1	10	2.3	2.3	2.3	2.3	f	\N	f
148	f	\N	\N	\N	\N	\N	2025-10-17 09:37:30.634342+00	2025-10-17 09:37:30.634352+00	1	14	20	2	10	\N	\N	\N	\N	f	\N	f
149	f	\N	\N	\N	\N	\N	2025-10-17 09:37:30.637475+00	2025-10-17 09:37:30.637484+00	1	24	20	2	10	\N	\N	\N	\N	f	\N	f
150	f	\N	\N	\N	\N	\N	2025-10-17 09:37:30.640419+00	2025-10-17 09:37:30.640427+00	1	14	21	3	10	\N	\N	\N	\N	f	\N	f
125	f	\N	2	\N	2025-10-02	\N	2025-10-16 21:31:03.33452+00	2025-10-17 09:18:49.603046+00	1	22	20	2	10	\N	\N	\N	\N	f	\N	f
124	f	\N	3	\N	2025-10-02	\N	2025-10-16 21:31:03.333458+00	2025-10-17 09:18:49.606356+00	1	20	20	2	10	\N	\N	\N	\N	f	\N	f
137	f	\N	343	\N	2025-10-02	\N	2025-10-17 06:45:07.064657+00	2025-10-17 09:18:49.61+00	1	4	20	2	10	\N	\N	\N	\N	f	\N	f
138	f	\N	8	\N	2025-10-02	\N	2025-10-17 06:45:41.471194+00	2025-10-17 09:18:49.612888+00	1	8	20	2	10	\N	\N	\N	\N	f	\N	f
151	f	\N	\N	\N	\N	\N	2025-10-17 09:37:30.641821+00	2025-10-17 09:37:30.641827+00	1	24	21	3	10	\N	\N	\N	\N	f	\N	f
152	f	\N	\N	\N	\N	\N	2025-10-17 09:37:30.643677+00	2025-10-17 09:37:30.643684+00	1	14	22	1	10	\N	\N	\N	\N	f	\N	f
153	f	\N	\N	\N	\N	\N	2025-10-17 09:37:30.645047+00	2025-10-17 09:37:30.645074+00	1	24	22	1	10	\N	\N	\N	\N	f	\N	f
136	f	\N	1	\N	2025-10-02	\N	2025-10-17 06:24:06.277522+00	2025-10-17 09:18:49.615551+00	1	6	20	2	10	\N	\N	\N	\N	f	\N	f
140	f	\N	7	\N	2025-10-02	\N	2025-10-17 06:50:32.4457+00	2025-10-17 09:18:49.618297+00	1	7	20	2	10	\N	\N	\N	\N	f	\N	f
122	f	\N	32	\N	2025-10-02	\N	2025-10-16 21:31:03.331139+00	2025-10-17 09:18:49.620854+00	1	10	20	2	10	\N	\N	\N	\N	f	\N	f
123	f	\N	32	\N	2025-10-02	\N	2025-10-16 21:31:03.332359+00	2025-10-17 09:18:49.624364+00	1	18	20	2	10	\N	\N	\N	\N	f	\N	f
121	f	\N	2.3	\N	2025-10-02	\N	2025-10-16 21:31:03.32621+00	2025-10-17 09:18:49.627309+00	1	1	20	2	10	2.3	2.3	2.3	2.3	f	\N	f
130	f	\N	2	\N	2025-10-02	\N	2025-10-16 21:31:03.341833+00	2025-10-17 09:18:49.635582+00	1	22	21	3	10	\N	\N	\N	\N	f	\N	f
129	f	\N	6	\N	2025-10-02	\N	2025-10-16 21:31:03.340909+00	2025-10-17 09:18:49.638382+00	1	20	21	3	10	\N	\N	\N	\N	f	\N	f
139	f	\N	35	\N	2025-10-02	\N	2025-10-17 06:50:15.147102+00	2025-10-17 09:18:49.641154+00	1	4	21	3	10	\N	\N	\N	\N	f	\N	f
146	f	\N	3	\N	2025-10-02	\N	2025-10-17 06:50:38.366516+00	2025-10-17 09:18:49.644049+00	1	8	21	3	10	\N	\N	\N	\N	f	\N	f
141	f	\N	3	\N	2025-10-02	\N	2025-10-17 06:50:32.465529+00	2025-10-17 09:18:49.646793+00	1	6	21	3	10	\N	\N	\N	\N	f	\N	f
142	f	\N	3	\N	2025-10-02	\N	2025-10-17 06:50:32.466825+00	2025-10-17 09:18:49.649244+00	1	7	21	3	10	\N	\N	\N	\N	f	\N	f
127	f	\N	32	\N	2025-10-02	\N	2025-10-16 21:31:03.338653+00	2025-10-17 09:18:49.652108+00	1	10	21	3	10	\N	\N	\N	\N	f	\N	f
128	f	\N	32	\N	2025-10-02	\N	2025-10-16 21:31:03.339925+00	2025-10-17 09:18:49.654685+00	1	18	21	3	10	\N	\N	\N	\N	f	\N	f
126	f	\N	2.6	\N	2025-10-02	\N	2025-10-16 21:31:03.337195+00	2025-10-17 09:18:49.657036+00	1	1	21	3	10	2.6	2.6	2.6	2.6	f	\N	f
135	f	\N	2	\N	2025-10-02	\N	2025-10-16 21:31:03.349246+00	2025-10-17 09:18:49.661041+00	1	22	22	1	10	\N	\N	\N	\N	f	\N	f
134	f	\N	2	\N	2025-10-02	\N	2025-10-16 21:31:03.348429+00	2025-10-17 09:18:49.663418+00	1	20	22	1	10	\N	\N	\N	\N	f	\N	f
143	f	\N	303	\N	2025-10-02	\N	2025-10-17 06:50:32.484521+00	2025-10-17 09:18:49.665576+00	1	4	22	1	10	\N	\N	\N	\N	f	\N	f
147	f	\N	3	\N	2025-10-02	\N	2025-10-17 06:50:53.931476+00	2025-10-17 09:18:49.668142+00	1	8	22	1	10	\N	\N	\N	\N	f	\N	f
144	f	\N	3	\N	2025-10-02	\N	2025-10-17 06:50:32.486198+00	2025-10-17 09:18:49.670689+00	1	6	22	1	10	\N	\N	\N	\N	f	\N	f
160	f	\N	1	\N	2025-10-16	\N	2025-10-17 09:59:34.514044+00	2025-10-17 10:29:57.128073+00	1	10	24	3	11	\N	\N	\N	\N	f	\N	f
161	f	\N	21	\N	2025-10-16	\N	2025-10-17 09:59:34.514918+00	2025-10-17 10:29:57.131073+00	1	18	24	3	11	\N	\N	\N	\N	f	\N	f
168	f	\N	2	\N	2025-10-16	\N	2025-10-17 09:59:34.524618+00	2025-10-17 10:29:57.144832+00	1	22	25	1	11	\N	\N	\N	\N	f	\N	f
167	f	\N	1	\N	2025-10-16	\N	2025-10-17 09:59:34.523741+00	2025-10-17 10:29:57.153518+00	1	20	25	1	11	\N	\N	\N	\N	f	\N	f
165	f	\N	11.8	\N	2025-10-16	\N	2025-10-17 09:59:34.522028+00	2025-10-17 10:29:57.160828+00	1	10	25	1	11	\N	\N	\N	\N	f	\N	f
166	f	\N	12	\N	2025-10-16	\N	2025-10-17 09:59:34.522887+00	2025-10-17 10:29:57.163756+00	1	18	25	1	11	\N	\N	\N	\N	f	\N	f
164	f	\N	8	\N	2025-10-16	\N	2025-10-17 09:59:34.520019+00	2025-10-17 10:29:57.166447+00	1	1	25	1	11	8	8	8	8	f	\N	f
176	f	\N	21	\N	2025-10-03	\N	2025-10-17 10:00:14.727154+00	2025-10-17 10:36:02.259782+00	1	18	27	3	12	\N	\N	\N	\N	f	\N	f
157	f	\N	2	\N	2025-10-16	\N	2025-10-17 09:59:34.508794+00	2025-10-17 10:29:57.098962+00	1	20	23	2	11	\N	\N	\N	\N	f	\N	f
155	f	\N	1	\N	2025-10-16	\N	2025-10-17 09:59:34.506397+00	2025-10-17 10:29:57.103097+00	1	10	23	2	11	\N	\N	\N	\N	f	\N	f
156	f	\N	12	\N	2025-10-16	\N	2025-10-17 09:59:34.507634+00	2025-10-17 10:29:57.10702+00	1	18	23	2	11	\N	\N	\N	\N	f	\N	f
163	f	\N	1	\N	2025-10-16	\N	2025-10-17 09:59:34.516835+00	2025-10-17 10:29:57.12141+00	1	22	24	3	11	\N	\N	\N	\N	f	\N	f
162	f	\N	1	\N	2025-10-16	\N	2025-10-17 09:59:34.51587+00	2025-10-17 10:29:57.124357+00	1	20	24	3	11	\N	\N	\N	\N	f	\N	f
174	f	\N	11.125	\N	2025-10-03	\N	2025-10-17 10:00:14.72491+00	2025-10-17 10:36:02.262843+00	1	1	27	3	12	11.1	11.1	11.2	11.1	f	\N	f
183	f	\N	1	\N	2025-10-03	\N	2025-10-17 10:00:14.737226+00	2025-10-17 10:36:02.26699+00	1	22	28	1	12	\N	\N	\N	\N	f	\N	f
182	f	\N	1	\N	2025-10-03	\N	2025-10-17 10:00:14.735999+00	2025-10-17 10:36:02.270183+00	1	20	28	1	12	\N	\N	\N	\N	f	\N	f
180	f	\N	12	\N	2025-10-03	\N	2025-10-17 10:00:14.734114+00	2025-10-17 10:36:02.272611+00	1	10	28	1	12	\N	\N	\N	\N	f	\N	f
181	f	\N	21	\N	2025-10-03	\N	2025-10-17 10:00:14.735036+00	2025-10-17 10:36:02.275022+00	1	18	28	1	12	\N	\N	\N	\N	f	\N	f
172	f	\N	2	\N	2025-10-03	\N	2025-10-17 10:00:14.720851+00	2025-10-17 10:36:02.229806+00	1	20	26	2	12	\N	\N	\N	\N	f	\N	f
171	f	\N	21	\N	2025-10-03	\N	2025-10-17 10:00:14.719623+00	2025-10-17 10:36:02.236672+00	1	18	26	2	12	\N	\N	\N	\N	f	\N	f
178	f	\N	2	\N	2025-10-03	\N	2025-10-17 10:00:14.729244+00	2025-10-17 10:36:02.249961+00	1	22	27	3	12	\N	\N	\N	\N	f	\N	f
177	f	\N	2	\N	2025-10-03	\N	2025-10-17 10:00:14.728059+00	2025-10-17 10:36:02.253425+00	1	20	27	3	12	\N	\N	\N	\N	f	\N	f
175	f	\N	11	\N	2025-10-03	\N	2025-10-17 10:00:14.72624+00	2025-10-17 10:36:02.256731+00	1	10	27	3	12	\N	\N	\N	\N	f	\N	f
173	f	\N	3	\N	2025-10-03	\N	2025-10-17 10:00:14.722334+00	2025-10-17 10:36:02.225851+00	1	22	26	2	12	\N	\N	\N	\N	f	\N	f
170	f	\N	11	\N	2025-10-03	\N	2025-10-17 10:00:14.718219+00	2025-10-17 10:36:02.232825+00	1	10	26	2	12	\N	\N	\N	\N	f	\N	f
169	f	\N	14.3	\N	2025-10-03	\N	2025-10-17 10:00:14.714466+00	2025-10-17 10:36:02.239599+00	1	1	26	2	12	14.3	14.4	14.3	14.2	f	\N	f
179	f	\N	9.8	\N	2025-10-03	\N	2025-10-17 10:00:14.732299+00	2025-10-17 10:36:02.278328+00	1	1	28	1	12	9.8	9.8	9.8	9.8	f	\N	f
190	f	\N	\N	\N	\N	\N	2025-10-17 10:37:03.690691+00	2025-10-17 10:37:03.690702+00	1	14	26	2	12	\N	\N	\N	\N	f	\N	f
191	f	\N	\N	\N	\N	\N	2025-10-17 10:37:03.693873+00	2025-10-17 10:37:03.693883+00	1	24	26	2	12	\N	\N	\N	\N	f	\N	f
192	f	\N	\N	\N	\N	\N	2025-10-17 10:37:03.696346+00	2025-10-17 10:37:03.696354+00	1	14	27	3	12	\N	\N	\N	\N	f	\N	f
193	f	\N	\N	\N	\N	\N	2025-10-17 10:37:03.697855+00	2025-10-17 10:37:03.697862+00	1	24	27	3	12	\N	\N	\N	\N	f	\N	f
194	f	\N	\N	\N	\N	\N	2025-10-17 10:37:03.699856+00	2025-10-17 10:37:03.699863+00	1	14	28	1	12	\N	\N	\N	\N	f	\N	f
195	f	\N	\N	\N	\N	\N	2025-10-17 10:37:03.701581+00	2025-10-17 10:37:03.701589+00	1	24	28	1	12	\N	\N	\N	\N	f	\N	f
158	f	\N	1	\N	2025-10-16	\N	2025-10-17 09:59:34.509962+00	2025-10-17 10:29:57.094113+00	1	22	23	2	11	\N	\N	\N	\N	f	\N	f
154	f	\N	10.399999999999999	\N	2025-10-16	\N	2025-10-17 09:59:34.500527+00	2025-10-17 10:29:57.111282+00	1	1	23	2	11	10.2	10.2	10.2	11	f	\N	f
159	f	\N	9	\N	2025-10-16	\N	2025-10-17 09:59:34.51271+00	2025-10-17 10:29:57.134863+00	1	1	24	3	11	9	9	9	9	f	\N	f
184	f	\N	\N	\N	\N	\N	2025-10-17 10:31:56.094084+00	2025-10-17 10:31:56.094098+00	1	14	23	2	11	\N	\N	\N	\N	f	\N	f
185	f	\N	\N	\N	\N	\N	2025-10-17 10:31:56.097741+00	2025-10-17 10:31:56.09775+00	1	24	23	2	11	\N	\N	\N	\N	f	\N	f
186	f	\N	\N	\N	\N	\N	2025-10-17 10:31:56.100127+00	2025-10-17 10:31:56.100135+00	1	14	24	3	11	\N	\N	\N	\N	f	\N	f
187	f	\N	\N	\N	\N	\N	2025-10-17 10:31:56.101803+00	2025-10-17 10:31:56.101811+00	1	24	24	3	11	\N	\N	\N	\N	f	\N	f
188	f	\N	\N	\N	\N	\N	2025-10-17 10:31:56.104308+00	2025-10-17 10:31:56.104316+00	1	14	25	1	11	\N	\N	\N	\N	f	\N	f
189	f	\N	\N	\N	\N	\N	2025-10-17 10:31:56.106024+00	2025-10-17 10:31:56.106029+00	1	24	25	1	11	\N	\N	\N	\N	f	\N	f
208	f	\N	\N	\N	2025-10-01	\N	2025-10-17 10:42:12.437206+00	2025-10-17 10:54:16.221715+00	1	18	31	3	13	\N	\N	\N	\N	f	\N	f
206	f	\N	17.8	\N	2025-10-01	\N	2025-10-17 10:42:12.434736+00	2025-10-17 10:54:16.224101+00	1	1	31	3	13	17.8	17.8	17.8	17.8	f	\N	f
241	f	\N	\N	\N	\N	\N	2025-10-17 10:54:33.062411+00	2025-10-17 10:54:33.062422+00	1	14	29	2	13	\N	\N	\N	\N	f	\N	f
200	f	\N	3	\N	2025-10-01	\N	2025-10-17 10:42:12.422713+00	2025-10-17 10:54:16.170082+00	1	22	29	2	13	\N	\N	\N	\N	f	\N	f
199	f	\N	1	\N	2025-10-01	\N	2025-10-17 10:42:12.421637+00	2025-10-17 10:54:16.17469+00	1	20	29	2	13	\N	\N	\N	\N	f	\N	f
197	f	\N	12	\N	2025-10-01	\N	2025-10-17 10:42:12.41931+00	2025-10-17 10:54:16.178481+00	1	10	29	2	13	\N	\N	\N	\N	f	\N	f
198	f	\N	12	\N	2025-10-01	\N	2025-10-17 10:42:12.420534+00	2025-10-17 10:54:16.182172+00	1	18	29	2	13	\N	\N	\N	\N	f	\N	f
196	f	\N	14.6	\N	2025-10-01	\N	2025-10-17 10:42:12.414872+00	2025-10-17 10:54:16.185572+00	1	1	29	2	13	14.7	14.5	14.7	14.5	f	\N	f
205	f	\N	3	\N	2025-10-01	\N	2025-10-17 10:42:12.432276+00	2025-10-17 10:54:16.195468+00	1	22	30	1	13	\N	\N	\N	\N	f	\N	f
204	f	\N	6	\N	2025-10-01	\N	2025-10-17 10:42:12.431445+00	2025-10-17 10:54:16.198668+00	1	20	30	1	13	\N	\N	\N	\N	f	\N	f
202	f	\N	21	\N	2025-10-01	\N	2025-10-17 10:42:12.429694+00	2025-10-17 10:54:16.201837+00	1	10	30	1	13	\N	\N	\N	\N	f	\N	f
203	f	\N	12	\N	2025-10-01	\N	2025-10-17 10:42:12.430571+00	2025-10-17 10:54:16.204479+00	1	18	30	1	13	\N	\N	\N	\N	f	\N	f
201	f	\N	16	\N	2025-10-01	\N	2025-10-17 10:42:12.426946+00	2025-10-17 10:54:16.207075+00	1	1	30	1	13	16	16	16	16	f	\N	f
210	f	\N	2	\N	2025-10-01	\N	2025-10-17 10:42:12.438806+00	2025-10-17 10:54:16.213839+00	1	22	31	3	13	\N	\N	\N	\N	f	\N	f
209	f	\N	3	\N	2025-10-01	\N	2025-10-17 10:42:12.437982+00	2025-10-17 10:54:16.216481+00	1	20	31	3	13	\N	\N	\N	\N	f	\N	f
207	f	\N	21	\N	2025-10-01	\N	2025-10-17 10:42:12.436345+00	2025-10-17 10:54:16.219355+00	1	10	31	3	13	\N	\N	\N	\N	f	\N	f
242	f	\N	\N	\N	\N	\N	2025-10-17 10:54:33.065677+00	2025-10-17 10:54:33.065686+00	1	24	29	2	13	\N	\N	\N	\N	f	\N	f
222	f	\N	11.8	\N	2025-09-30	\N	2025-10-17 10:42:24.465454+00	2025-10-17 10:57:13.380419+00	1	10	34	3	14	\N	\N	\N	\N	f	\N	f
223	f	\N	12	\N	2025-09-30	\N	2025-10-17 10:42:24.466633+00	2025-10-17 10:57:13.382844+00	1	18	34	3	14	\N	\N	\N	\N	f	\N	f
221	f	\N	7.1	\N	2025-09-30	\N	2025-10-17 10:42:24.464235+00	2025-10-17 10:57:13.385252+00	1	1	34	3	14	7.1	7	7.2	7.1	f	\N	f
238	f	\N	4	\N	2025-10-02	\N	2025-10-17 10:45:04.017878+00	2025-10-17 11:59:59.999937+00	1	18	37	1	15	\N	\N	\N	\N	f	\N	f
212	f	\N	21	\N	2025-09-30	\N	2025-10-17 10:42:24.448153+00	2025-10-17 10:57:13.338224+00	1	10	32	2	14	\N	\N	\N	\N	f	\N	f
213	f	\N	12	\N	2025-09-30	\N	2025-10-17 10:42:24.449243+00	2025-10-17 10:57:13.341668+00	1	18	32	2	14	\N	\N	\N	\N	f	\N	f
220	f	\N	2	\N	2025-09-30	\N	2025-10-17 10:42:24.462177+00	2025-10-17 10:57:13.354858+00	1	22	33	1	14	\N	\N	\N	\N	f	\N	f
219	f	\N	2	\N	2025-09-30	\N	2025-10-17 10:42:24.46128+00	2025-10-17 10:57:13.358204+00	1	20	33	1	14	\N	\N	\N	\N	f	\N	f
217	f	\N	21	\N	2025-09-30	\N	2025-10-17 10:42:24.459203+00	2025-10-17 10:57:13.361041+00	1	10	33	1	14	\N	\N	\N	\N	f	\N	f
218	f	\N	12	\N	2025-09-30	\N	2025-10-17 10:42:24.460301+00	2025-10-17 10:57:13.364281+00	1	18	33	1	14	\N	\N	\N	\N	f	\N	f
225	f	\N	2	\N	2025-09-30	\N	2025-10-17 10:42:24.468736+00	2025-10-17 10:57:13.374592+00	1	22	34	3	14	\N	\N	\N	\N	f	\N	f
224	f	\N	3	\N	2025-09-30	\N	2025-10-17 10:42:24.467838+00	2025-10-17 10:57:13.377293+00	1	20	34	3	14	\N	\N	\N	\N	f	\N	f
229	f	\N	4	\N	2025-10-02	\N	2025-10-17 10:45:04.003817+00	2025-10-17 11:59:59.932702+00	1	20	35	2	15	\N	\N	\N	\N	f	\N	f
227	f	\N	1	\N	2025-10-02	\N	2025-10-17 10:45:04.001263+00	2025-10-17 11:59:59.937393+00	1	10	35	2	15	\N	\N	\N	\N	f	\N	f
228	f	\N	4	\N	2025-10-02	\N	2025-10-17 10:45:04.002706+00	2025-10-17 11:59:59.940529+00	1	18	35	2	15	\N	\N	\N	\N	f	\N	f
226	f	\N	24.4	\N	2025-10-02	\N	2025-10-17 10:45:03.997234+00	2025-10-17 11:59:59.943925+00	1	1	35	2	15	24.4	24.4	24.3	24.5	f	\N	f
235	f	\N	4	\N	2025-10-02	\N	2025-10-17 10:45:04.012254+00	2025-10-17 11:59:59.968385+00	1	22	36	3	15	\N	\N	\N	\N	f	\N	f
234	f	\N	3	\N	2025-10-02	\N	2025-10-17 10:45:04.010799+00	2025-10-17 11:59:59.9721+00	1	20	36	3	15	\N	\N	\N	\N	f	\N	f
232	f	\N	2	\N	2025-10-02	\N	2025-10-17 10:45:04.008256+00	2025-10-17 11:59:59.974951+00	1	10	36	3	15	\N	\N	\N	\N	f	\N	f
233	f	\N	4	\N	2025-10-02	\N	2025-10-17 10:45:04.009641+00	2025-10-17 11:59:59.978326+00	1	18	36	3	15	\N	\N	\N	\N	f	\N	f
240	f	\N	3	\N	2025-10-02	\N	2025-10-17 10:45:04.019691+00	2025-10-17 11:59:59.992524+00	1	22	37	1	15	\N	\N	\N	\N	f	\N	f
239	f	\N	1	\N	2025-10-02	\N	2025-10-17 10:45:04.01881+00	2025-10-17 11:59:59.99533+00	1	20	37	1	15	\N	\N	\N	\N	f	\N	f
237	f	\N	3	\N	2025-10-02	\N	2025-10-17 10:45:04.016588+00	2025-10-17 11:59:59.997702+00	1	10	37	1	15	\N	\N	\N	\N	f	\N	f
243	f	\N	\N	\N	\N	\N	2025-10-17 10:54:33.068186+00	2025-10-17 10:54:33.068193+00	1	14	30	1	13	\N	\N	\N	\N	f	\N	f
244	f	\N	\N	\N	\N	\N	2025-10-17 10:54:33.069682+00	2025-10-17 10:54:33.069688+00	1	24	30	1	13	\N	\N	\N	\N	f	\N	f
245	f	\N	\N	\N	\N	\N	2025-10-17 10:54:33.071376+00	2025-10-17 10:54:33.071382+00	1	14	31	3	13	\N	\N	\N	\N	f	\N	f
246	f	\N	\N	\N	\N	\N	2025-10-17 10:54:33.072811+00	2025-10-17 10:54:33.072819+00	1	24	31	3	13	\N	\N	\N	\N	f	\N	f
265	f	\N	\N	\N	\N	\N	2025-10-17 12:00:35.322473+00	2025-10-17 12:00:35.322479+00	1	24	36	3	15	\N	\N	\N	\N	f	\N	f
266	f	\N	\N	\N	\N	\N	2025-10-17 12:00:35.324304+00	2025-10-17 12:00:35.32431+00	1	14	37	1	15	\N	\N	\N	\N	f	\N	f
267	f	\N	\N	\N	\N	\N	2025-10-17 12:00:35.325612+00	2025-10-17 12:00:35.325618+00	1	24	37	1	15	\N	\N	\N	\N	f	\N	f
230	f	\N	4	\N	2025-10-02	\N	2025-10-17 10:45:04.004838+00	2025-10-17 11:59:59.928886+00	1	22	35	2	15	\N	\N	\N	\N	f	\N	f
253	f	\N	30	\N	2025-10-02	\N	2025-10-17 11:59:29.887251+00	2025-10-17 11:59:59.953633+00	1	4	35	2	15	\N	\N	\N	\N	f	\N	f
256	f	\N	1	\N	2025-10-02	\N	2025-10-17 11:59:38.192026+00	2025-10-17 11:59:59.960965+00	1	9	35	2	15	\N	\N	\N	\N	f	\N	f
259	f	\N	6	\N	2025-10-02	\N	2025-10-17 11:59:52.729146+00	2025-10-17 11:59:59.964929+00	1	5	35	2	15	\N	\N	\N	\N	f	\N	f
231	f	\N	23.525	\N	2025-10-02	\N	2025-10-17 10:45:04.006972+00	2025-10-17 11:59:59.981158+00	1	1	36	3	15	23.5	23.5	23.6	23.5	f	\N	f
215	f	\N	2	\N	2025-09-30	\N	2025-10-17 10:42:24.451897+00	2025-10-17 10:57:13.330222+00	1	22	32	2	14	\N	\N	\N	\N	f	\N	f
214	f	\N	1	\N	2025-09-30	\N	2025-10-17 10:42:24.450635+00	2025-10-17 10:57:13.334195+00	1	20	32	2	14	\N	\N	\N	\N	f	\N	f
211	f	\N	6.6	\N	2025-09-30	\N	2025-10-17 10:42:24.444406+00	2025-10-17 10:57:13.345306+00	1	1	32	2	14	6.6	6.7	6.5	6.6	f	\N	f
216	f	\N	3.2	\N	2025-09-30	\N	2025-10-17 10:42:24.456173+00	2025-10-17 10:57:13.367295+00	1	1	33	1	14	3.2	3.2	3.1	3.3	f	\N	f
247	f	\N	\N	\N	\N	\N	2025-10-17 10:57:25.660933+00	2025-10-17 10:57:25.660944+00	1	14	32	2	14	\N	\N	\N	\N	f	\N	f
248	f	\N	\N	\N	\N	\N	2025-10-17 10:57:25.663648+00	2025-10-17 10:57:25.663656+00	1	24	32	2	14	\N	\N	\N	\N	f	\N	f
249	f	\N	\N	\N	\N	\N	2025-10-17 10:57:25.665708+00	2025-10-17 10:57:25.665714+00	1	14	33	1	14	\N	\N	\N	\N	f	\N	f
250	f	\N	\N	\N	\N	\N	2025-10-17 10:57:25.667139+00	2025-10-17 10:57:25.667145+00	1	24	33	1	14	\N	\N	\N	\N	f	\N	f
251	f	\N	\N	\N	\N	\N	2025-10-17 10:57:25.669106+00	2025-10-17 10:57:25.669112+00	1	14	34	3	14	\N	\N	\N	\N	f	\N	f
252	f	\N	\N	\N	\N	\N	2025-10-17 10:57:25.671042+00	2025-10-17 10:57:25.671051+00	1	24	34	3	14	\N	\N	\N	\N	f	\N	f
254	f	\N	30	\N	2025-10-02	\N	2025-10-17 11:59:35.397257+00	2025-10-17 11:59:59.984181+00	1	4	36	3	15	\N	\N	\N	\N	f	\N	f
257	f	\N	1	\N	2025-10-02	\N	2025-10-17 11:59:43.073883+00	2025-10-17 11:59:59.987035+00	1	9	36	3	15	\N	\N	\N	\N	f	\N	f
260	f	\N	6	\N	2025-10-02	\N	2025-10-17 11:59:52.751976+00	2025-10-17 11:59:59.989641+00	1	5	36	3	15	\N	\N	\N	\N	f	\N	f
236	f	\N	22	\N	2025-10-02	\N	2025-10-17 10:45:04.014899+00	2025-10-17 12:00:00.002468+00	1	1	37	1	15	22	22	22	22	f	\N	f
255	f	\N	30	\N	2025-10-02	\N	2025-10-17 11:59:35.416805+00	2025-10-17 12:00:00.008372+00	1	4	37	1	15	\N	\N	\N	\N	f	\N	f
258	f	\N	1	\N	2025-10-02	\N	2025-10-17 11:59:46.978942+00	2025-10-17 12:00:00.010965+00	1	9	37	1	15	\N	\N	\N	\N	f	\N	f
261	f	\N	6	\N	2025-10-02	\N	2025-10-17 11:59:52.774625+00	2025-10-17 12:00:00.01357+00	1	5	37	1	15	\N	\N	\N	\N	f	\N	f
262	f	\N	\N	\N	\N	\N	2025-10-17 12:00:35.316156+00	2025-10-17 12:00:35.316165+00	1	14	35	2	15	\N	\N	\N	\N	f	\N	f
263	f	\N	\N	\N	\N	\N	2025-10-17 12:00:35.318334+00	2025-10-17 12:00:35.318348+00	1	24	35	2	15	\N	\N	\N	\N	f	\N	f
264	f	\N	\N	\N	\N	\N	2025-10-17 12:00:35.321028+00	2025-10-17 12:00:35.321035+00	1	14	36	3	15	\N	\N	\N	\N	f	\N	f
271	f	\N	\N	\N	2025-10-01	\N	2025-10-17 21:08:25.076398+00	2025-10-18 11:28:41.84531+00	1	20	38	5	16	\N	\N	\N	\N	f	\N	f
276	f	\N	\N	\N	2025-10-01	\N	2025-10-17 21:08:25.085922+00	2025-10-18 11:28:41.88972+00	1	20	39	4	16	\N	\N	\N	\N	f	\N	f
277	f	\N	\N	\N	2025-10-01	\N	2025-10-17 21:08:25.086906+00	2025-10-18 11:28:41.892577+00	1	22	39	4	16	\N	\N	\N	\N	f	\N	f
270	f	\N	\N	\N	2025-10-01	\N	2025-10-17 21:08:25.075224+00	2025-10-18 11:28:41.872255+00	1	18	38	5	16	\N	\N	\N	\N	f	\N	f
295	f	\N	81	\N	2025-10-01	\N	2025-10-17 22:58:23.097526+00	2025-10-18 11:28:41.900268+00	1	4	39	4	16	\N	\N	\N	\N	f	\N	f
294	f	\N	80	\N	2025-10-01	\N	2025-10-17 22:58:16.483532+00	2025-10-18 11:28:41.941097+00	1	4	40	3	16	\N	\N	\N	\N	f	\N	f
279	f	\N	25.2	\N	2025-10-01	\N	2025-10-17 21:08:25.089876+00	2025-10-18 11:28:41.951463+00	1	10	40	3	16	\N	\N	\N	\N	f	\N	f
275	f	\N	\N	\N	2025-10-01	\N	2025-10-17 21:08:25.085007+00	2025-10-18 11:28:41.914488+00	1	18	39	4	16	\N	\N	\N	\N	f	\N	f
280	f	\N	\N	\N	2025-10-01	\N	2025-10-17 21:08:25.090727+00	2025-10-18 11:28:41.956451+00	1	18	40	3	16	\N	\N	\N	\N	f	\N	f
278	f	\N	7.15	\N	2025-10-01	\N	2025-10-17 21:08:25.088769+00	2025-10-18 11:28:41.965524+00	1	1	40	3	16	7.9	7.1	7.1	6.5	f	\N	f
293	f	\N	78	\N	2025-10-01	\N	2025-10-17 22:58:09.144757+00	2025-10-18 11:28:41.980824+00	1	4	41	2	16	\N	\N	\N	\N	f	\N	f
272	f	\N	\N	\N	2025-10-01	\N	2025-10-17 21:08:25.077402+00	2025-10-18 11:28:41.848433+00	1	22	38	5	16	\N	\N	\N	\N	f	\N	f
297	f	\N	51	\N	2025-10-01	\N	2025-10-17 23:00:11.939179+00	2025-10-18 11:28:41.853919+00	1	5	38	5	16	\N	\N	\N	\N	f	\N	f
296	f	\N	80	\N	2025-10-01	\N	2025-10-17 22:58:32.5322+00	2025-10-18 11:28:41.856655+00	1	4	38	5	16	\N	\N	\N	\N	f	\N	f
268	f	\N	9.2	\N	2025-10-01	\N	2025-10-17 21:08:25.070426+00	2025-10-18 11:28:41.881011+00	1	1	38	5	16	9.3	9.2	9.2	9.1	f	\N	f
287	f	\N	\N	\N	2025-10-01	\N	2025-10-17 21:08:25.099109+00	2025-10-18 11:28:41.973253+00	1	22	41	2	16	\N	\N	\N	\N	f	\N	f
281	f	\N	\N	\N	2025-10-01	\N	2025-10-17 21:08:25.09178+00	2025-10-18 11:28:41.929246+00	1	20	40	3	16	\N	\N	\N	\N	f	\N	f
282	f	\N	\N	\N	2025-10-01	\N	2025-10-17 21:08:25.093064+00	2025-10-18 11:28:41.932132+00	1	22	40	3	16	\N	\N	\N	\N	f	\N	f
269	f	\N	24.4	\N	2025-10-01	\N	2025-10-17 21:08:25.073793+00	2025-10-18 11:28:41.86774+00	1	10	38	5	16	\N	\N	\N	\N	f	\N	f
274	f	\N	24.3	\N	2025-10-01	\N	2025-10-17 21:08:25.084027+00	2025-10-18 11:28:41.910012+00	1	10	39	4	16	\N	\N	\N	\N	f	\N	f
283	f	\N	8.2	\N	2025-10-01	\N	2025-10-17 21:08:25.095478+00	2025-10-18 11:28:42.002885+00	1	1	41	2	16	8.2	8.2	10.3	6.1	f	\N	f
286	f	\N	\N	\N	2025-10-01	\N	2025-10-17 21:08:25.098296+00	2025-10-18 11:28:41.970518+00	1	20	41	2	16	\N	\N	\N	\N	f	\N	f
284	f	\N	24.8	\N	2025-10-01	\N	2025-10-17 21:08:25.096595+00	2025-10-18 11:28:41.990775+00	1	10	41	2	16	\N	\N	\N	\N	f	\N	f
285	f	\N	\N	\N	2025-10-01	\N	2025-10-17 21:08:25.09746+00	2025-10-18 11:28:41.995684+00	1	18	41	2	16	\N	\N	\N	\N	f	\N	f
288	f	\N	11	\N	\N	\N	2025-10-17 21:08:25.143756+00	2025-10-20 09:53:18.944043+00	1	1	42	1	17	10	11	11	12	f	\N	f
292	f	\N	\N	\N	\N	\N	2025-10-17 21:08:25.148135+00	2025-10-20 09:53:18.914727+00	1	22	42	1	17	\N	\N	\N	\N	f	\N	f
291	f	\N	\N	\N	\N	\N	2025-10-17 21:08:25.147417+00	2025-10-20 09:53:18.923305+00	1	20	42	1	17	\N	\N	\N	\N	f	\N	f
289	f	\N	\N	\N	\N	\N	2025-10-17 21:08:25.145934+00	2025-10-20 09:53:18.938342+00	1	10	42	1	17	\N	\N	\N	\N	f	\N	f
290	f	\N	\N	\N	\N	\N	2025-10-17 21:08:25.146665+00	2025-10-20 09:53:18.941272+00	1	18	42	1	17	\N	\N	\N	\N	f	\N	f
330	f	\N	\N	\N	\N	\N	2025-10-18 11:42:38.06239+00	2025-10-18 11:42:38.062399+00	1	24	38	5	16	\N	\N	\N	\N	f	\N	f
331	f	\N	\N	\N	\N	\N	2025-10-18 11:42:38.064768+00	2025-10-18 11:42:38.064775+00	1	14	39	4	16	\N	\N	\N	\N	f	\N	f
327	f	\N	79	\N	2025-10-01	\N	2025-10-18 11:28:21.08188+00	2025-10-18 11:28:41.902739+00	1	53	39	4	16	\N	\N	\N	\N	f	\N	f
302	f	\N	5	\N	2025-10-01	\N	2025-10-17 23:07:53.36575+00	2025-10-18 11:28:41.90494+00	1	6	39	4	16	\N	\N	\N	\N	f	\N	f
332	f	\N	\N	\N	\N	\N	2025-10-18 11:42:38.066131+00	2025-10-18 11:42:38.066136+00	1	24	39	4	16	\N	\N	\N	\N	f	\N	f
303	f	\N	4	\N	2025-10-01	\N	2025-10-17 23:14:36.735567+00	2025-10-18 11:28:41.90712+00	1	7	39	4	16	\N	\N	\N	\N	f	\N	f
318	f	\N	5	\N	2025-10-01	\N	2025-10-18 11:26:43.706832+00	2025-10-18 11:28:41.912324+00	1	21	39	4	16	\N	\N	\N	\N	f	\N	f
333	f	\N	\N	\N	\N	\N	2025-10-18 11:42:38.067841+00	2025-10-18 11:42:38.067847+00	1	14	40	3	16	\N	\N	\N	\N	f	\N	f
334	f	\N	\N	\N	\N	\N	2025-10-18 11:42:38.069461+00	2025-10-18 11:42:38.069469+00	1	24	40	3	16	\N	\N	\N	\N	f	\N	f
314	f	\N	1.1	\N	2025-10-01	\N	2025-10-18 11:26:14.513601+00	2025-10-18 11:28:41.917346+00	1	19	39	4	16	\N	\N	\N	\N	f	\N	f
322	f	\N	32	\N	2025-10-01	\N	2025-10-18 11:27:46.319762+00	2025-10-18 11:28:41.919724+00	1	28	39	4	16	\N	\N	\N	\N	f	\N	f
273	f	\N	10.3	\N	2025-10-01	\N	2025-10-17 21:08:25.080739+00	2025-10-18 11:28:41.921871+00	1	1	39	4	16	10.2	10.4	11.8	8.8	f	\N	f
311	f	\N	5	\N	2025-10-01	\N	2025-10-18 11:25:49.8029+00	2025-10-18 11:28:41.935665+00	1	17	40	3	16	\N	\N	\N	\N	f	\N	f
335	f	\N	\N	\N	\N	\N	2025-10-18 11:42:38.071471+00	2025-10-18 11:42:38.071479+00	1	14	41	2	16	\N	\N	\N	\N	f	\N	f
336	f	\N	\N	\N	\N	\N	2025-10-18 11:42:38.072674+00	2025-10-18 11:42:38.072679+00	1	24	41	2	16	\N	\N	\N	\N	f	\N	f
299	f	\N	48	\N	2025-10-01	\N	2025-10-17 23:01:36.543309+00	2025-10-18 11:28:41.938408+00	1	5	40	3	16	\N	\N	\N	\N	f	\N	f
326	f	\N	74	\N	2025-10-01	\N	2025-10-18 11:28:13.107888+00	2025-10-18 11:28:41.94397+00	1	53	40	3	16	\N	\N	\N	\N	f	\N	f
305	f	\N	5	\N	2025-10-01	\N	2025-10-17 23:16:05.912618+00	2025-10-18 11:28:41.946172+00	1	6	40	3	16	\N	\N	\N	\N	f	\N	f
307	f	\N	3	\N	2025-10-01	\N	2025-10-17 23:16:25.119759+00	2025-10-18 11:28:41.948444+00	1	7	40	3	16	\N	\N	\N	\N	f	\N	f
319	f	\N	5	\N	2025-10-01	\N	2025-10-18 11:26:43.738525+00	2025-10-18 11:28:41.953698+00	1	21	40	3	16	\N	\N	\N	\N	f	\N	f
315	f	\N	1.1	\N	2025-10-01	\N	2025-10-18 11:26:14.538963+00	2025-10-18 11:28:41.959615+00	1	19	40	3	16	\N	\N	\N	\N	f	\N	f
323	f	\N	29	\N	2025-10-01	\N	2025-10-18 11:27:54.069297+00	2025-10-18 11:28:41.962114+00	1	28	40	3	16	\N	\N	\N	\N	f	\N	f
312	f	\N	5	\N	2025-10-01	\N	2025-10-18 11:25:49.825596+00	2025-10-18 11:28:41.976298+00	1	17	41	2	16	\N	\N	\N	\N	f	\N	f
309	f	\N	5	\N	2025-10-01	\N	2025-10-18 11:25:49.748735+00	2025-10-18 11:28:41.851543+00	1	17	38	5	16	\N	\N	\N	\N	f	\N	f
300	f	\N	42	\N	2025-10-01	\N	2025-10-17 23:01:43.151862+00	2025-10-18 11:28:41.978683+00	1	5	41	2	16	\N	\N	\N	\N	f	\N	f
325	f	\N	76	\N	2025-10-01	\N	2025-10-18 11:28:08.920314+00	2025-10-18 11:28:41.983568+00	1	53	41	2	16	\N	\N	\N	\N	f	\N	f
328	f	\N	77	\N	2025-10-01	\N	2025-10-18 11:28:31.636525+00	2025-10-18 11:28:41.859896+00	1	53	38	5	16	\N	\N	\N	\N	f	\N	f
301	f	\N	5	\N	2025-10-01	\N	2025-10-17 23:01:55.975209+00	2025-10-18 11:28:41.862343+00	1	6	38	5	16	\N	\N	\N	\N	f	\N	f
304	f	\N	4	\N	2025-10-01	\N	2025-10-17 23:15:48.58274+00	2025-10-18 11:28:41.865056+00	1	7	38	5	16	\N	\N	\N	\N	f	\N	f
306	f	\N	5	\N	2025-10-01	\N	2025-10-17 23:16:18.607792+00	2025-10-18 11:28:41.98618+00	1	6	41	2	16	\N	\N	\N	\N	f	\N	f
308	f	\N	4	\N	2025-10-01	\N	2025-10-17 23:16:27.81846+00	2025-10-18 11:28:41.988325+00	1	7	41	2	16	\N	\N	\N	\N	f	\N	f
320	f	\N	5	\N	2025-10-01	\N	2025-10-18 11:26:43.767882+00	2025-10-18 11:28:41.99359+00	1	21	41	2	16	\N	\N	\N	\N	f	\N	f
316	f	\N	1.1	\N	2025-10-01	\N	2025-10-18 11:26:14.564705+00	2025-10-18 11:28:41.997956+00	1	19	41	2	16	\N	\N	\N	\N	f	\N	f
324	f	\N	34	\N	2025-10-01	\N	2025-10-18 11:27:58.227889+00	2025-10-18 11:28:42.000618+00	1	28	41	2	16	\N	\N	\N	\N	f	\N	f
349	f	\N	\N	\N	\N	\N	2025-10-18 11:48:59.799618+00	2025-10-18 11:48:59.799621+00	1	1	47	1	19	\N	\N	\N	\N	f	\N	f
317	f	\N	5	\N	2025-10-01	\N	2025-10-18 11:26:43.668012+00	2025-10-18 11:28:41.869978+00	1	21	38	5	16	\N	\N	\N	\N	f	\N	f
313	f	\N	1.1	\N	2025-10-01	\N	2025-10-18 11:26:14.481206+00	2025-10-18 11:28:41.8754+00	1	19	38	5	16	\N	\N	\N	\N	f	\N	f
329	f	\N	\N	\N	\N	\N	2025-10-18 11:42:38.059275+00	2025-10-18 11:42:38.059286+00	1	14	38	5	16	\N	\N	\N	\N	f	\N	f
350	f	\N	\N	\N	\N	\N	2025-10-18 11:48:59.802166+00	2025-10-18 11:48:59.80217+00	1	10	47	1	19	\N	\N	\N	\N	f	\N	f
321	f	\N	29	\N	2025-10-01	\N	2025-10-18 11:27:33.449859+00	2025-10-18 11:28:41.87778+00	1	28	38	5	16	\N	\N	\N	\N	f	\N	f
351	f	\N	\N	\N	\N	\N	2025-10-18 11:48:59.803005+00	2025-10-18 11:48:59.803008+00	1	20	47	1	19	\N	\N	\N	\N	f	\N	f
345	f	\N	\N	\N	2025-10-01	\N	2025-10-18 11:48:59.736759+00	2025-10-18 12:43:47.824563+00	1	20	45	3	18	\N	\N	\N	\N	f	\N	f
344	f	\N	27.1	\N	2025-10-01	\N	2025-10-18 11:48:59.735821+00	2025-10-18 12:43:47.831788+00	1	10	45	3	18	\N	\N	\N	\N	f	\N	f
310	f	\N	5	\N	2025-10-01	\N	2025-10-18 11:25:49.779902+00	2025-10-18 11:28:41.895079+00	1	17	39	4	16	\N	\N	\N	\N	f	\N	f
298	f	\N	41	\N	2025-10-01	\N	2025-10-17 23:00:44.802186+00	2025-10-18 11:28:41.897468+00	1	5	39	4	16	\N	\N	\N	\N	f	\N	f
348	f	\N	\N	\N	2025-10-01	\N	2025-10-18 11:48:59.740834+00	2025-10-18 12:43:47.856219+00	1	20	46	2	18	\N	\N	\N	\N	f	\N	f
347	f	\N	28.7	\N	2025-10-01	\N	2025-10-18 11:48:59.739999+00	2025-10-18 12:43:47.863111+00	1	10	46	2	18	\N	\N	\N	\N	f	\N	f
346	f	\N	15.600000000000001	\N	2025-10-01	\N	2025-10-18 11:48:59.738725+00	2025-10-18 12:43:47.865415+00	1	1	46	2	18	15.6	15.6	15.5	15.7	f	\N	f
342	f	\N	\N	\N	2025-10-01	\N	2025-10-18 11:48:59.73221+00	2025-10-18 12:43:47.784914+00	1	20	44	4	18	\N	\N	\N	\N	f	\N	f
353	f	\N	46	\N	2025-10-01	\N	2025-10-18 12:31:29.97207+00	2025-10-18 12:43:47.78263+00	1	5	44	4	18	\N	\N	\N	\N	f	\N	f
343	f	\N	14.6	\N	2025-10-01	\N	2025-10-18 11:48:59.734363+00	2025-10-18 12:43:47.833933+00	1	1	45	3	18	14.6	14.6	14.7	14.5	f	\N	f
352	f	\N	57	\N	2025-10-01	\N	2025-10-18 12:31:24.623972+00	2025-10-18 12:43:47.729436+00	1	5	43	5	18	\N	\N	\N	\N	f	\N	f
339	f	\N	5	\N	2025-10-01	\N	2025-10-18 11:48:59.724057+00	2025-10-18 12:43:47.732621+00	1	20	43	5	18	\N	\N	\N	\N	f	\N	f
356	f	\N	5	\N	2025-10-01	\N	2025-10-18 12:32:29.290629+00	2025-10-18 12:43:47.735994+00	1	6	43	5	18	\N	\N	\N	\N	f	\N	f
337	f	\N	17.466666666666665	\N	2025-10-01	\N	2025-10-18 11:48:59.71767+00	2025-10-18 12:43:47.744704+00	1	1	43	5	18	\N	18.5	16.5	17.4	f	\N	f
340	f	\N	18.5	\N	2025-10-01	\N	2025-10-18 11:48:59.728166+00	2025-10-18 12:43:47.796853+00	1	1	44	4	18	18.5	19	18.1	18.4	f	\N	f
338	f	\N	24.3	\N	2025-10-01	\N	2025-10-18 11:48:59.72293+00	2025-10-18 12:43:47.741751+00	1	10	43	5	18	\N	\N	\N	\N	f	\N	f
355	f	\N	52	\N	2025-10-01	\N	2025-10-18 12:31:40.096932+00	2025-10-18 12:43:47.853899+00	1	5	46	2	18	\N	\N	\N	\N	f	\N	f
354	f	\N	60	\N	2025-10-01	\N	2025-10-18 12:31:36.286112+00	2025-10-18 12:43:47.822392+00	1	5	45	3	18	\N	\N	\N	\N	f	\N	f
387	f	\N	28	\N	2025-10-01	\N	2025-10-18 12:43:08.122043+00	2025-10-18 12:43:47.848705+00	1	28	45	3	18	\N	\N	\N	\N	f	\N	f
391	f	\N	99	\N	2025-10-01	\N	2025-10-18 12:43:34.225783+00	2025-10-18 12:43:47.850794+00	1	53	45	3	18	\N	\N	\N	\N	f	\N	f
381	f	\N	5	\N	2025-10-01	\N	2025-10-18 12:41:51.462303+00	2025-10-18 12:43:47.769169+00	1	21	43	5	18	\N	\N	\N	\N	f	\N	f
385	f	\N	36	\N	2025-10-01	\N	2025-10-18 12:42:55.997473+00	2025-10-18 12:43:47.775934+00	1	28	43	5	18	\N	\N	\N	\N	f	\N	f
389	f	\N	98	\N	2025-10-01	\N	2025-10-18 12:43:27.200546+00	2025-10-18 12:43:47.779647+00	1	53	43	5	18	\N	\N	\N	\N	f	\N	f
359	f	\N	5	\N	2025-10-01	\N	2025-10-18 12:32:29.336162+00	2025-10-18 12:43:47.858337+00	1	6	46	2	18	\N	\N	\N	\N	f	\N	f
363	f	\N	4	\N	2025-10-01	\N	2025-10-18 12:33:03.073384+00	2025-10-18 12:43:47.860421+00	1	7	46	2	18	\N	\N	\N	\N	f	\N	f
357	f	\N	5	\N	2025-10-01	\N	2025-10-18 12:32:29.309805+00	2025-10-18 12:43:47.78767+00	1	6	44	4	18	\N	\N	\N	\N	f	\N	f
361	f	\N	4	\N	2025-10-01	\N	2025-10-18 12:32:57.392848+00	2025-10-18 12:43:47.790804+00	1	7	44	4	18	\N	\N	\N	\N	f	\N	f
367	f	\N	76	\N	2025-10-01	\N	2025-10-18 12:39:29.373251+00	2025-10-18 12:43:47.868123+00	1	4	46	2	18	\N	\N	\N	\N	f	\N	f
372	f	\N	5	\N	2025-10-01	\N	2025-10-18 12:40:07.134533+00	2025-10-18 12:43:47.870781+00	1	17	46	2	18	\N	\N	\N	\N	f	\N	f
376	f	\N	785.2	\N	2025-10-01	\N	2025-10-18 12:40:52.286653+00	2025-10-18 12:43:47.873068+00	1	18	46	2	18	\N	\N	\N	\N	f	\N	f
341	f	\N	26.7	\N	2025-10-01	\N	2025-10-18 11:48:59.731192+00	2025-10-18 12:43:47.793712+00	1	10	44	4	18	\N	\N	\N	\N	f	\N	f
365	f	\N	77	\N	2025-10-01	\N	2025-10-18 12:39:02.398238+00	2025-10-18 12:43:47.803291+00	1	4	44	4	18	\N	\N	\N	\N	f	\N	f
380	f	\N	1.4	\N	2025-10-01	\N	2025-10-18 12:41:32.123721+00	2025-10-18 12:43:47.8752+00	1	19	46	2	18	\N	\N	\N	\N	f	\N	f
384	f	\N	5	\N	2025-10-01	\N	2025-10-18 12:41:51.545918+00	2025-10-18 12:43:47.877841+00	1	21	46	2	18	\N	\N	\N	\N	f	\N	f
370	f	\N	5	\N	2025-10-01	\N	2025-10-18 12:40:07.096512+00	2025-10-18 12:43:47.806094+00	1	17	44	4	18	\N	\N	\N	\N	f	\N	f
374	f	\N	750	\N	2025-10-01	\N	2025-10-18 12:40:38.768819+00	2025-10-18 12:43:47.80827+00	1	18	44	4	18	\N	\N	\N	\N	f	\N	f
388	f	\N	33	\N	2025-10-01	\N	2025-10-18 12:43:11.230941+00	2025-10-18 12:43:47.88013+00	1	28	46	2	18	\N	\N	\N	\N	f	\N	f
392	f	\N	98	\N	2025-10-01	\N	2025-10-18 12:43:34.256977+00	2025-10-18 12:43:47.882186+00	1	53	46	2	18	\N	\N	\N	\N	f	\N	f
393	f	\N	\N	\N	\N	\N	2025-10-18 12:44:08.332384+00	2025-10-18 12:44:08.332392+00	1	14	43	5	18	\N	\N	\N	\N	f	\N	f
394	f	\N	\N	\N	\N	\N	2025-10-18 12:44:08.334743+00	2025-10-18 12:44:08.334751+00	1	23	43	5	18	\N	\N	\N	\N	f	\N	f
378	f	\N	1.5	\N	2025-10-01	\N	2025-10-18 12:41:14.810035+00	2025-10-18 12:43:47.810469+00	1	19	44	4	18	\N	\N	\N	\N	f	\N	f
382	f	\N	5	\N	2025-10-01	\N	2025-10-18 12:41:51.494388+00	2025-10-18 12:43:47.813332+00	1	21	44	4	18	\N	\N	\N	\N	f	\N	f
395	f	\N	\N	\N	\N	\N	2025-10-18 12:44:08.336887+00	2025-10-18 12:44:08.336895+00	1	14	44	4	18	\N	\N	\N	\N	f	\N	f
402	f	\N	5	\N	\N	\N	2025-10-20 09:37:17.35497+00	2025-10-20 09:53:18.919119+00	1	5	42	1	17	\N	\N	\N	\N	f	\N	f
401	f	\N	30	\N	\N	\N	2025-10-20 09:37:17.35119+00	2025-10-20 09:53:18.927297+00	1	4	42	1	17	\N	\N	\N	\N	f	\N	f
403	f	\N	5	\N	\N	\N	2025-10-20 09:37:17.356551+00	2025-10-20 09:53:18.931531+00	1	6	42	1	17	\N	\N	\N	\N	f	\N	f
396	f	\N	\N	\N	\N	\N	2025-10-18 12:44:08.338523+00	2025-10-18 12:44:08.338528+00	1	23	44	4	18	\N	\N	\N	\N	f	\N	f
397	f	\N	\N	\N	\N	\N	2025-10-18 12:44:08.340339+00	2025-10-18 12:44:08.340345+00	1	14	45	3	18	\N	\N	\N	\N	f	\N	f
360	f	\N	4	\N	2025-10-01	\N	2025-10-18 12:32:45.16603+00	2025-10-18 12:43:47.738971+00	1	7	43	5	18	\N	\N	\N	\N	f	\N	f
386	f	\N	39	\N	2025-10-01	\N	2025-10-18 12:43:02.465903+00	2025-10-18 12:43:47.81606+00	1	28	44	4	18	\N	\N	\N	\N	f	\N	f
398	f	\N	\N	\N	\N	\N	2025-10-18 12:44:08.341677+00	2025-10-18 12:44:08.341682+00	1	23	45	3	18	\N	\N	\N	\N	f	\N	f
390	f	\N	100	\N	2025-10-01	\N	2025-10-18 12:43:27.238506+00	2025-10-18 12:43:47.819043+00	1	53	44	4	18	\N	\N	\N	\N	f	\N	f
399	f	\N	\N	\N	\N	\N	2025-10-18 12:44:08.343397+00	2025-10-18 12:44:08.343402+00	1	14	46	2	18	\N	\N	\N	\N	f	\N	f
400	f	\N	\N	\N	\N	\N	2025-10-18 12:44:08.344768+00	2025-10-18 12:44:08.344772+00	1	23	46	2	18	\N	\N	\N	\N	f	\N	f
364	f	\N	73	\N	2025-10-01	\N	2025-10-18 12:38:02.677721+00	2025-10-18 12:43:47.753009+00	1	4	43	5	18	\N	\N	\N	\N	f	\N	f
368	f	\N	0	\N	2025-10-01	\N	2025-10-18 12:39:39.405502+00	2025-10-18 12:43:47.756043+00	1	8	43	5	18	\N	\N	\N	\N	f	\N	f
358	f	\N	5	\N	2025-10-01	\N	2025-10-18 12:32:29.323286+00	2025-10-18 12:43:47.82683+00	1	6	45	3	18	\N	\N	\N	\N	f	\N	f
362	f	\N	3	\N	2025-10-01	\N	2025-10-18 12:33:03.058632+00	2025-10-18 12:43:47.829503+00	1	7	45	3	18	\N	\N	\N	\N	f	\N	f
369	f	\N	5	\N	2025-10-01	\N	2025-10-18 12:40:07.069371+00	2025-10-18 12:43:47.758649+00	1	17	43	5	18	\N	\N	\N	\N	f	\N	f
366	f	\N	77	\N	2025-10-01	\N	2025-10-18 12:39:18.191317+00	2025-10-18 12:43:47.837257+00	1	4	45	3	18	\N	\N	\N	\N	f	\N	f
373	f	\N	770	\N	2025-10-01	\N	2025-10-18 12:40:27.563873+00	2025-10-18 12:43:47.761134+00	1	18	43	5	18	\N	\N	\N	\N	f	\N	f
371	f	\N	5	\N	2025-10-01	\N	2025-10-18 12:40:07.116202+00	2025-10-18 12:43:47.839501+00	1	17	45	3	18	\N	\N	\N	\N	f	\N	f
375	f	\N	800	\N	2025-10-01	\N	2025-10-18 12:40:45.326836+00	2025-10-18 12:43:47.841584+00	1	18	45	3	18	\N	\N	\N	\N	f	\N	f
377	f	\N	1.4	\N	2025-10-01	\N	2025-10-18 12:41:09.617414+00	2025-10-18 12:43:47.763594+00	1	19	43	5	18	\N	\N	\N	\N	f	\N	f
379	f	\N	1.3	\N	2025-10-01	\N	2025-10-18 12:41:28.040539+00	2025-10-18 12:43:47.84372+00	1	19	45	3	18	\N	\N	\N	\N	f	\N	f
383	f	\N	5	\N	2025-10-01	\N	2025-10-18 12:41:51.520488+00	2025-10-18 12:43:47.846544+00	1	21	45	3	18	\N	\N	\N	\N	f	\N	f
404	f	\N	3	\N	\N	\N	2025-10-20 09:37:17.358078+00	2025-10-20 09:53:18.934982+00	1	7	42	1	17	\N	\N	\N	\N	f	\N	f
409	f	\N	21.5	\N	2025-10-01	\N	2025-10-20 10:02:28.273654+00	2025-10-20 10:21:51.194062+00	1	1	50	3	20	21	21	32	12	f	\N	f
414	f	\N	\N	\N	2025-10-01	\N	2025-10-20 10:02:28.313142+00	2025-10-20 10:13:15.502296+00	1	10	52	1	21	\N	\N	\N	\N	f	\N	f
413	f	\N	\N	\N	2025-10-01	\N	2025-10-20 10:02:28.310624+00	2025-10-20 10:13:15.506434+00	1	1	52	1	21	\N	\N	\N	\N	f	\N	f
412	f	\N	5	\N	2025-10-01	\N	2025-10-20 10:02:28.277714+00	2025-10-20 10:21:51.198451+00	1	10	51	2	20	\N	\N	\N	\N	f	\N	f
411	f	\N	22.5	\N	2025-10-01	\N	2025-10-20 10:02:28.2766+00	2025-10-20 10:21:51.200984+00	1	1	51	2	20	23	23	21	23	f	\N	f
415	f	\N	\N	\N	\N	\N	2025-10-20 10:22:12.352214+00	2025-10-20 10:22:12.352226+00	1	14	48	5	20	\N	\N	\N	\N	f	\N	f
406	f	\N	4	\N	2025-10-01	\N	2025-10-20 10:02:28.265865+00	2025-10-20 10:21:51.162449+00	1	10	48	5	20	\N	\N	\N	\N	f	\N	f
405	f	\N	21.5	\N	2025-10-01	\N	2025-10-20 10:02:28.261776+00	2025-10-20 10:21:51.167347+00	1	1	48	5	20	32	21	12	21	f	\N	f
408	f	\N	4	\N	2025-10-01	\N	2025-10-20 10:02:28.271716+00	2025-10-20 10:21:51.178911+00	1	10	49	4	20	\N	\N	\N	\N	f	\N	f
407	f	\N	12	\N	2025-10-01	\N	2025-10-20 10:02:28.269234+00	2025-10-20 10:21:51.181884+00	1	1	49	4	20	12	12	12	12	f	\N	f
410	f	\N	5	\N	2025-10-01	\N	2025-10-20 10:02:28.274787+00	2025-10-20 10:21:51.191101+00	1	10	50	3	20	\N	\N	\N	\N	f	\N	f
416	f	\N	\N	\N	\N	\N	2025-10-20 10:22:12.355389+00	2025-10-20 10:22:12.355396+00	1	14	49	4	20	\N	\N	\N	\N	f	\N	f
417	f	\N	\N	\N	\N	\N	2025-10-20 10:22:12.357798+00	2025-10-20 10:22:12.357806+00	1	14	50	3	20	\N	\N	\N	\N	f	\N	f
418	f	\N	\N	\N	\N	\N	2025-10-20 10:22:12.360209+00	2025-10-20 10:22:12.360215+00	1	14	51	2	20	\N	\N	\N	\N	f	\N	f
\.


--
-- Data for Name: trials_app_trialtype; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.trials_app_trialtype (id, is_deleted, deleted_at, code, name, name_full, category, description, requires_area, requires_standard, default_area_ha, sort_order, created_at, updated_at) FROM stdin;
1	f	\N	KSI	КСИ		mandatory	Конкурсное сортоиспытание	t	t	\N	0	2025-10-16 08:53:45.950651+00	2025-10-16 08:53:45.950655+00
2	f	\N	OOS	ООС		mandatory	Определение отличительных признаков	t	t	\N	0	2025-10-16 08:53:45.951546+00	2025-10-16 08:53:45.951551+00
3	f	\N	DUS	ДЮС		mandatory	ДЮС испытания	t	t	\N	0	2025-10-16 08:53:45.952544+00	2025-10-16 08:53:45.952549+00
4	f	\N	competitive	КСИ	Конкурсное сортоиспытание (КСИ)	mandatory	Основное испытание для оценки хозяйственной ценности сорта	t	t	0.0250	1	2025-10-17 21:17:36.629421+00	2025-10-17 21:17:36.629429+00
5	f	\N	oos	ООС	Опыты на хозяйственную полезность (ООС)	mandatory	Испытание для подтверждения хозяйственной полезности	t	t	0.0280	2	2025-10-17 21:17:36.630845+00	2025-10-17 21:17:36.630849+00
6	f	\N	dus	ДЮС-ТЕСТ	Испытание на отличимость, однородность и стабильность (ДЮС-ТЕСТ)	mandatory	Оценка отличимости от других сортов, однородности и стабильности признаков	t	f	0.0280	3	2025-10-17 21:17:36.631694+00	2025-10-17 21:17:36.631699+00
7	f	\N	production	Производственное	Производственное испытание	additional	Испытание в производственных условиях	t	t	1.0000	4	2025-10-17 21:17:36.632441+00	2025-10-17 21:17:36.632445+00
8	f	\N	variety_technology	Сортовая технология	Опыты по изучению сортовой технологии	additional	Изучение оптимальных приемов возделывания сорта	t	f	0.6000	5	2025-10-17 21:17:36.633336+00	2025-10-17 21:17:36.63334+00
9	f	\N	efu	ЭФУ	Опыты ЭФУ и демонстрационных посевов	demonstration	Экологическое испытание и демонстрация сортов	t	f	0.0100	6	2025-10-17 21:17:36.634052+00	2025-10-17 21:17:36.634056+00
10	f	\N	methodological	Методические опыты	Методические опыты, опыты по договору, коллекция	special	Специальные исследовательские опыты	t	f	0.1500	7	2025-10-17 21:17:36.634787+00	2025-10-17 21:17:36.634791+00
11	f	\N	ground_control	Грунтконтроль	Опыты по грунтконтролю	special	Контроль качества семян и почвы	f	f	\N	8	2025-10-17 21:17:36.635516+00	2025-10-17 21:17:36.63552+00
12	f	\N	ksi_applicant	КСИ на территории заявителя	Опыты КСИ на территории заявителя	additional	Конкурсное испытание на территории заявителя	t	t	0.0250	9	2025-10-17 21:17:36.636194+00	2025-10-17 21:17:36.636197+00
13	f	\N	seed_reproduction	Размножение семян	План размножения семян для целей сортоиспытания	reproduction	Размножение семян для дальнейших испытаний	t	f	\N	10	2025-10-17 21:17:36.636839+00	2025-10-17 21:17:36.636842+00
14	f	\N	planting_material	Выращивание посадочного материала	План выращивания посадочного материала плодовоягодных культур и винограда	reproduction	Выращивание саженцев для испытаний	t	f	\N	11	2025-10-17 21:17:36.637556+00	2025-10-17 21:17:36.63756+00
15	f	\N	technology_economic	Технолого-экономические	Технолого-экономические опыты	special	Оценка экономической эффективности сорта	t	f	\N	12	2025-10-17 21:17:36.638251+00	2025-10-17 21:17:36.638254+00
16	f	\N	seed_reproduction_production	Размножение для производства	План размножения семян для внедрения в производство	reproduction	Размножение семян для внедрения	t	f	\N	13	2025-10-17 21:17:36.638937+00	2025-10-17 21:17:36.638941+00
\.


--
-- Name: auth_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.auth_group_id_seq', 1, false);


--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.auth_group_permissions_id_seq', 1, false);


--
-- Name: auth_permission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.auth_permission_id_seq', 136, true);


--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.auth_user_groups_id_seq', 1, false);


--
-- Name: auth_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.auth_user_id_seq', 2, true);


--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.auth_user_user_permissions_id_seq', 1, false);


--
-- Name: django_admin_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.django_admin_log_id_seq', 1, false);


--
-- Name: django_content_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.django_content_type_id_seq', 34, true);


--
-- Name: django_migrations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.django_migrations_id_seq', 48, true);


--
-- Name: trials_app_application_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.trials_app_application_id_seq', 7, true);


--
-- Name: trials_app_application_target_oblasts_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.trials_app_application_target_oblasts_id_seq', 13, true);


--
-- Name: trials_app_applicationdecisionhistory_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.trials_app_applicationdecisionhistory_id_seq', 1, true);


--
-- Name: trials_app_climatezone_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.trials_app_climatezone_id_seq', 11, true);


--
-- Name: trials_app_culture_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.trials_app_culture_id_seq', 150, true);


--
-- Name: trials_app_document_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.trials_app_document_id_seq', 28, true);


--
-- Name: trials_app_groupculture_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.trials_app_groupculture_id_seq', 16, true);


--
-- Name: trials_app_indicator_group_cultures_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.trials_app_indicator_group_cultures_id_seq', 109, true);


--
-- Name: trials_app_indicator_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.trials_app_indicator_id_seq', 54, true);


--
-- Name: trials_app_oblast_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.trials_app_oblast_id_seq', 17, true);


--
-- Name: trials_app_originator_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.trials_app_originator_id_seq', 1343, true);


--
-- Name: trials_app_planneddistribution_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.trials_app_planneddistribution_id_seq', 1, false);


--
-- Name: trials_app_region_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.trials_app_region_id_seq', 73, true);


--
-- Name: trials_app_sortoriginator_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.trials_app_sortoriginator_id_seq', 1465, true);


--
-- Name: trials_app_sortrecord_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.trials_app_sortrecord_id_seq', 2134, true);


--
-- Name: trials_app_trial_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.trials_app_trial_id_seq', 21, true);


--
-- Name: trials_app_trial_indicators_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.trials_app_trial_indicators_id_seq', 215, true);


--
-- Name: trials_app_triallaboratoryresult_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.trials_app_triallaboratoryresult_id_seq', 24, true);


--
-- Name: trials_app_trialparticipant_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.trials_app_trialparticipant_id_seq', 52, true);


--
-- Name: trials_app_trialplan_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.trials_app_trialplan_id_seq', 5, true);


--
-- Name: trials_app_trialplanculture_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.trials_app_trialplanculture_id_seq', 5, true);


--
-- Name: trials_app_trialplanculturetrialtype_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.trials_app_trialplanculturetrialtype_id_seq', 6, true);


--
-- Name: trials_app_trialplanparticipant_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.trials_app_trialplanparticipant_id_seq', 15, true);


--
-- Name: trials_app_trialplantrial_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.trials_app_trialplantrial_id_seq', 38, true);


--
-- Name: trials_app_trialresult_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.trials_app_trialresult_id_seq', 418, true);


--
-- Name: trials_app_trialtype_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.trials_app_trialtype_id_seq', 16, true);


--
-- Name: auth_group auth_group_name_key; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);


--
-- Name: auth_group_permissions auth_group_permissions_group_id_permission_id_0cd325b0_uniq; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_permission_id_0cd325b0_uniq UNIQUE (group_id, permission_id);


--
-- Name: auth_group_permissions auth_group_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_group auth_group_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);


--
-- Name: auth_permission auth_permission_content_type_id_codename_01ab375a_uniq; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_codename_01ab375a_uniq UNIQUE (content_type_id, codename);


--
-- Name: auth_permission auth_permission_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups auth_user_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups auth_user_groups_user_id_group_id_94350c0c_uniq; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_group_id_94350c0c_uniq UNIQUE (user_id, group_id);


--
-- Name: auth_user auth_user_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auth_user
    ADD CONSTRAINT auth_user_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions auth_user_user_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions auth_user_user_permissions_user_id_permission_id_14a6b632_uniq; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_permission_id_14a6b632_uniq UNIQUE (user_id, permission_id);


--
-- Name: auth_user auth_user_username_key; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auth_user
    ADD CONSTRAINT auth_user_username_key UNIQUE (username);


--
-- Name: authtoken_token authtoken_token_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.authtoken_token
    ADD CONSTRAINT authtoken_token_pkey PRIMARY KEY (key);


--
-- Name: authtoken_token authtoken_token_user_id_key; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.authtoken_token
    ADD CONSTRAINT authtoken_token_user_id_key UNIQUE (user_id);


--
-- Name: django_admin_log django_admin_log_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_pkey PRIMARY KEY (id);


--
-- Name: django_content_type django_content_type_app_label_model_76bd3d3b_uniq; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_app_label_model_76bd3d3b_uniq UNIQUE (app_label, model);


--
-- Name: django_content_type django_content_type_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);


--
-- Name: django_migrations django_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.django_migrations
    ADD CONSTRAINT django_migrations_pkey PRIMARY KEY (id);


--
-- Name: django_session django_session_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.django_session
    ADD CONSTRAINT django_session_pkey PRIMARY KEY (session_key);


--
-- Name: trials_app_application trials_app_application_application_number_key; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.trials_app_application
    ADD CONSTRAINT trials_app_application_application_number_key UNIQUE (application_number);


--
-- Name: trials_app_application trials_app_application_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.trials_app_application
    ADD CONSTRAINT trials_app_application_pkey PRIMARY KEY (id);


--
-- Name: trials_app_application_target_oblasts trials_app_application_t_application_id_oblast_id_e5a14bf6_uniq; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.trials_app_application_target_oblasts
    ADD CONSTRAINT trials_app_application_t_application_id_oblast_id_e5a14bf6_uniq UNIQUE (application_id, oblast_id);


--
-- Name: trials_app_application_target_oblasts trials_app_application_target_oblasts_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.trials_app_application_target_oblasts
    ADD CONSTRAINT trials_app_application_target_oblasts_pkey PRIMARY KEY (id);


--
-- Name: trials_app_applicationdecisionhistory trials_app_applicationde_application_id_oblast_id_27ff0346_uniq; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.trials_app_applicationdecisionhistory
    ADD CONSTRAINT trials_app_applicationde_application_id_oblast_id_27ff0346_uniq UNIQUE (application_id, oblast_id, year);


--
-- Name: trials_app_applicationdecisionhistory trials_app_applicationdecisionhistory_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.trials_app_applicationdecisionhistory
    ADD CONSTRAINT trials_app_applicationdecisionhistory_pkey PRIMARY KEY (id);


--
-- Name: trials_app_climatezone trials_app_climatezone_code_key; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.trials_app_climatezone
    ADD CONSTRAINT trials_app_climatezone_code_key UNIQUE (code);


--
-- Name: trials_app_climatezone trials_app_climatezone_name_key; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.trials_app_climatezone
    ADD CONSTRAINT trials_app_climatezone_name_key UNIQUE (name);


--
-- Name: trials_app_climatezone trials_app_climatezone_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.trials_app_climatezone
    ADD CONSTRAINT trials_app_climatezone_pkey PRIMARY KEY (id);


--
-- Name: trials_app_culture trials_app_culture_culture_id_key; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.trials_app_culture
    ADD CONSTRAINT trials_app_culture_culture_id_key UNIQUE (culture_id);


--
-- Name: trials_app_culture trials_app_culture_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.trials_app_culture
    ADD CONSTRAINT trials_app_culture_pkey PRIMARY KEY (id);


--
-- Name: trials_app_document trials_app_document_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.trials_app_document
    ADD CONSTRAINT trials_app_document_pkey PRIMARY KEY (id);


--
-- Name: trials_app_groupculture trials_app_groupculture_group_culture_id_key; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.trials_app_groupculture
    ADD CONSTRAINT trials_app_groupculture_group_culture_id_key UNIQUE (group_culture_id);


--
-- Name: trials_app_groupculture trials_app_groupculture_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.trials_app_groupculture
    ADD CONSTRAINT trials_app_groupculture_pkey PRIMARY KEY (id);


--
-- Name: trials_app_indicator trials_app_indicator_code_key; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.trials_app_indicator
    ADD CONSTRAINT trials_app_indicator_code_key UNIQUE (code);


--
-- Name: trials_app_indicator_group_cultures trials_app_indicator_gro_indicator_id_groupcultur_df35d3fe_uniq; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.trials_app_indicator_group_cultures
    ADD CONSTRAINT trials_app_indicator_gro_indicator_id_groupcultur_df35d3fe_uniq UNIQUE (indicator_id, groupculture_id);


--
-- Name: trials_app_indicator_group_cultures trials_app_indicator_group_cultures_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.trials_app_indicator_group_cultures
    ADD CONSTRAINT trials_app_indicator_group_cultures_pkey PRIMARY KEY (id);


--
-- Name: trials_app_indicator trials_app_indicator_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.trials_app_indicator
    ADD CONSTRAINT trials_app_indicator_pkey PRIMARY KEY (id);


--
-- Name: trials_app_oblast trials_app_oblast_code_key; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.trials_app_oblast
    ADD CONSTRAINT trials_app_oblast_code_key UNIQUE (code);


--
-- Name: trials_app_oblast trials_app_oblast_name_key; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.trials_app_oblast
    ADD CONSTRAINT trials_app_oblast_name_key UNIQUE (name);


--
-- Name: trials_app_oblast trials_app_oblast_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.trials_app_oblast
    ADD CONSTRAINT trials_app_oblast_pkey PRIMARY KEY (id);


--
-- Name: trials_app_originator trials_app_originator_originator_id_key; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.trials_app_originator
    ADD CONSTRAINT trials_app_originator_originator_id_key UNIQUE (originator_id);


--
-- Name: trials_app_originator trials_app_originator_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.trials_app_originator
    ADD CONSTRAINT trials_app_originator_pkey PRIMARY KEY (id);


--
-- Name: trials_app_planneddistribution trials_app_planneddistri_application_id_region_id_9771754c_uniq; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.trials_app_planneddistribution
    ADD CONSTRAINT trials_app_planneddistri_application_id_region_id_9771754c_uniq UNIQUE (application_id, region_id);


--
-- Name: trials_app_planneddistribution trials_app_planneddistribution_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.trials_app_planneddistribution
    ADD CONSTRAINT trials_app_planneddistribution_pkey PRIMARY KEY (id);


--
-- Name: trials_app_region trials_app_region_name_oblast_id_88eeb945_uniq; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.trials_app_region
    ADD CONSTRAINT trials_app_region_name_oblast_id_88eeb945_uniq UNIQUE (name, oblast_id);


--
-- Name: trials_app_region trials_app_region_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.trials_app_region
    ADD CONSTRAINT trials_app_region_pkey PRIMARY KEY (id);


--
-- Name: trials_app_sortoriginator trials_app_sortoriginato_sort_record_id_originato_a1b8c0d0_uniq; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.trials_app_sortoriginator
    ADD CONSTRAINT trials_app_sortoriginato_sort_record_id_originato_a1b8c0d0_uniq UNIQUE (sort_record_id, originator_id);


--
-- Name: trials_app_sortoriginator trials_app_sortoriginator_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.trials_app_sortoriginator
    ADD CONSTRAINT trials_app_sortoriginator_pkey PRIMARY KEY (id);


--
-- Name: trials_app_sortrecord trials_app_sortrecord_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.trials_app_sortrecord
    ADD CONSTRAINT trials_app_sortrecord_pkey PRIMARY KEY (id);


--
-- Name: trials_app_sortrecord trials_app_sortrecord_sort_id_key; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.trials_app_sortrecord
    ADD CONSTRAINT trials_app_sortrecord_sort_id_key UNIQUE (sort_id);


--
-- Name: trials_app_trial_indicators trials_app_trial_indicators_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.trials_app_trial_indicators
    ADD CONSTRAINT trials_app_trial_indicators_pkey PRIMARY KEY (id);


--
-- Name: trials_app_trial_indicators trials_app_trial_indicators_trial_id_indicator_id_c37664a8_uniq; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.trials_app_trial_indicators
    ADD CONSTRAINT trials_app_trial_indicators_trial_id_indicator_id_c37664a8_uniq UNIQUE (trial_id, indicator_id);


--
-- Name: trials_app_trial trials_app_trial_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.trials_app_trial
    ADD CONSTRAINT trials_app_trial_pkey PRIMARY KEY (id);


--
-- Name: trials_app_triallaboratoryresult trials_app_triallaborato_trial_id_indicator_id_pa_0ef58ca0_uniq; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.trials_app_triallaboratoryresult
    ADD CONSTRAINT trials_app_triallaborato_trial_id_indicator_id_pa_0ef58ca0_uniq UNIQUE (trial_id, indicator_id, participant_id);


--
-- Name: trials_app_triallaboratoryresult trials_app_triallaboratoryresult_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.trials_app_triallaboratoryresult
    ADD CONSTRAINT trials_app_triallaboratoryresult_pkey PRIMARY KEY (id);


--
-- Name: trials_app_trialparticipant trials_app_trialparticip_trial_id_participant_num_d61b86d8_uniq; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.trials_app_trialparticipant
    ADD CONSTRAINT trials_app_trialparticip_trial_id_participant_num_d61b86d8_uniq UNIQUE (trial_id, participant_number);


--
-- Name: trials_app_trialparticipant trials_app_trialparticip_trial_id_sort_record_id_f40a87e1_uniq; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.trials_app_trialparticipant
    ADD CONSTRAINT trials_app_trialparticip_trial_id_sort_record_id_f40a87e1_uniq UNIQUE (trial_id, sort_record_id);


--
-- Name: trials_app_trialparticipant trials_app_trialparticipant_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.trials_app_trialparticipant
    ADD CONSTRAINT trials_app_trialparticipant_pkey PRIMARY KEY (id);


--
-- Name: trials_app_trialplan trials_app_trialplan_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.trials_app_trialplan
    ADD CONSTRAINT trials_app_trialplan_pkey PRIMARY KEY (id);


--
-- Name: trials_app_trialplanculturetrialtype trials_app_trialplancult_trial_plan_culture_id_tr_5c530c26_uniq; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.trials_app_trialplanculturetrialtype
    ADD CONSTRAINT trials_app_trialplancult_trial_plan_culture_id_tr_5c530c26_uniq UNIQUE (trial_plan_culture_id, trial_type_id, is_deleted);


--
-- Name: trials_app_trialplanculture trials_app_trialplancult_trial_plan_id_culture_id_1ccb6d61_uniq; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.trials_app_trialplanculture
    ADD CONSTRAINT trials_app_trialplancult_trial_plan_id_culture_id_1ccb6d61_uniq UNIQUE (trial_plan_id, culture_id, is_deleted);


--
-- Name: trials_app_trialplanculture trials_app_trialplanculture_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.trials_app_trialplanculture
    ADD CONSTRAINT trials_app_trialplanculture_pkey PRIMARY KEY (id);


--
-- Name: trials_app_trialplanculturetrialtype trials_app_trialplanculturetrialtype_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.trials_app_trialplanculturetrialtype
    ADD CONSTRAINT trials_app_trialplanculturetrialtype_pkey PRIMARY KEY (id);


--
-- Name: trials_app_trialplanparticipant trials_app_trialplanpart_culture_trial_type_id_pa_73ad0c65_uniq; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.trials_app_trialplanparticipant
    ADD CONSTRAINT trials_app_trialplanpart_culture_trial_type_id_pa_73ad0c65_uniq UNIQUE (culture_trial_type_id, participant_number, is_deleted);


--
-- Name: trials_app_trialplanparticipant trials_app_trialplanparticipant_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.trials_app_trialplanparticipant
    ADD CONSTRAINT trials_app_trialplanparticipant_pkey PRIMARY KEY (id);


--
-- Name: trials_app_trialplantrial trials_app_trialplantrial_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.trials_app_trialplantrial
    ADD CONSTRAINT trials_app_trialplantrial_pkey PRIMARY KEY (id);


--
-- Name: trials_app_trialresult trials_app_trialresult_participant_id_indicator_afd094ca_uniq; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.trials_app_trialresult
    ADD CONSTRAINT trials_app_trialresult_participant_id_indicator_afd094ca_uniq UNIQUE (participant_id, indicator_id);


--
-- Name: trials_app_trialresult trials_app_trialresult_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.trials_app_trialresult
    ADD CONSTRAINT trials_app_trialresult_pkey PRIMARY KEY (id);


--
-- Name: trials_app_trialtype trials_app_trialtype_code_key; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.trials_app_trialtype
    ADD CONSTRAINT trials_app_trialtype_code_key UNIQUE (code);


--
-- Name: trials_app_trialtype trials_app_trialtype_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.trials_app_trialtype
    ADD CONSTRAINT trials_app_trialtype_pkey PRIMARY KEY (id);


--
-- Name: auth_group_name_a6ea08ec_like; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX auth_group_name_a6ea08ec_like ON public.auth_group USING btree (name varchar_pattern_ops);


--
-- Name: auth_group_permissions_group_id_b120cbf9; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX auth_group_permissions_group_id_b120cbf9 ON public.auth_group_permissions USING btree (group_id);


--
-- Name: auth_group_permissions_permission_id_84c5c92e; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX auth_group_permissions_permission_id_84c5c92e ON public.auth_group_permissions USING btree (permission_id);


--
-- Name: auth_permission_content_type_id_2f476e4b; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX auth_permission_content_type_id_2f476e4b ON public.auth_permission USING btree (content_type_id);


--
-- Name: auth_user_groups_group_id_97559544; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX auth_user_groups_group_id_97559544 ON public.auth_user_groups USING btree (group_id);


--
-- Name: auth_user_groups_user_id_6a12ed8b; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX auth_user_groups_user_id_6a12ed8b ON public.auth_user_groups USING btree (user_id);


--
-- Name: auth_user_user_permissions_permission_id_1fbb5f2c; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX auth_user_user_permissions_permission_id_1fbb5f2c ON public.auth_user_user_permissions USING btree (permission_id);


--
-- Name: auth_user_user_permissions_user_id_a95ead1b; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX auth_user_user_permissions_user_id_a95ead1b ON public.auth_user_user_permissions USING btree (user_id);


--
-- Name: auth_user_username_6821ab7c_like; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX auth_user_username_6821ab7c_like ON public.auth_user USING btree (username varchar_pattern_ops);


--
-- Name: authtoken_token_key_10f0b77e_like; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX authtoken_token_key_10f0b77e_like ON public.authtoken_token USING btree (key varchar_pattern_ops);


--
-- Name: django_admin_log_content_type_id_c4bce8eb; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX django_admin_log_content_type_id_c4bce8eb ON public.django_admin_log USING btree (content_type_id);


--
-- Name: django_admin_log_user_id_c564eba6; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX django_admin_log_user_id_c564eba6 ON public.django_admin_log USING btree (user_id);


--
-- Name: django_session_expire_date_a5c62663; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX django_session_expire_date_a5c62663 ON public.django_session USING btree (expire_date);


--
-- Name: django_session_session_key_c0390e0f_like; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX django_session_session_key_c0390e0f_like ON public.django_session USING btree (session_key varchar_pattern_ops);


--
-- Name: trials_app__applica_df5144_idx; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX trials_app__applica_df5144_idx ON public.trials_app_applicationdecisionhistory USING btree (application_id, oblast_id, year);


--
-- Name: trials_app__decisio_646cbe_idx; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX trials_app__decisio_646cbe_idx ON public.trials_app_applicationdecisionhistory USING btree (decision, year);


--
-- Name: trials_app_application_application_number_7fb60d7a_like; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX trials_app_application_application_number_7fb60d7a_like ON public.trials_app_application USING btree (application_number varchar_pattern_ops);


--
-- Name: trials_app_application_created_by_id_42010fc1; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX trials_app_application_created_by_id_42010fc1 ON public.trials_app_application USING btree (created_by_id);


--
-- Name: trials_app_application_sort_record_id_54e27471; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX trials_app_application_sort_record_id_54e27471 ON public.trials_app_application USING btree (sort_record_id);


--
-- Name: trials_app_application_target_oblasts_application_id_bcd7129f; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX trials_app_application_target_oblasts_application_id_bcd7129f ON public.trials_app_application_target_oblasts USING btree (application_id);


--
-- Name: trials_app_application_target_oblasts_oblast_id_3d905481; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX trials_app_application_target_oblasts_oblast_id_3d905481 ON public.trials_app_application_target_oblasts USING btree (oblast_id);


--
-- Name: trials_app_applicationdecisionhistory_application_id_91f33d25; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX trials_app_applicationdecisionhistory_application_id_91f33d25 ON public.trials_app_applicationdecisionhistory USING btree (application_id);


--
-- Name: trials_app_applicationdecisionhistory_decided_by_id_2e8aa2c0; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX trials_app_applicationdecisionhistory_decided_by_id_2e8aa2c0 ON public.trials_app_applicationdecisionhistory USING btree (decided_by_id);


--
-- Name: trials_app_applicationdecisionhistory_oblast_id_60ea54ab; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX trials_app_applicationdecisionhistory_oblast_id_60ea54ab ON public.trials_app_applicationdecisionhistory USING btree (oblast_id);


--
-- Name: trials_app_climatezone_code_7c8a791e_like; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX trials_app_climatezone_code_7c8a791e_like ON public.trials_app_climatezone USING btree (code varchar_pattern_ops);


--
-- Name: trials_app_climatezone_name_31808453_like; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX trials_app_climatezone_name_31808453_like ON public.trials_app_climatezone USING btree (name varchar_pattern_ops);


--
-- Name: trials_app_culture_group_culture_id_3df16e08; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX trials_app_culture_group_culture_id_3df16e08 ON public.trials_app_culture USING btree (group_culture_id);


--
-- Name: trials_app_document_application_id_3df2eb59; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX trials_app_document_application_id_3df2eb59 ON public.trials_app_document USING btree (application_id);


--
-- Name: trials_app_document_trial_id_a13eea15; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX trials_app_document_trial_id_a13eea15 ON public.trials_app_document USING btree (trial_id);


--
-- Name: trials_app_document_uploaded_by_id_7a8f4d1e; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX trials_app_document_uploaded_by_id_7a8f4d1e ON public.trials_app_document USING btree (uploaded_by_id);


--
-- Name: trials_app_indicator_code_aca87b12_like; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX trials_app_indicator_code_aca87b12_like ON public.trials_app_indicator USING btree (code varchar_pattern_ops);


--
-- Name: trials_app_indicator_group_cultures_groupculture_id_23aac67c; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX trials_app_indicator_group_cultures_groupculture_id_23aac67c ON public.trials_app_indicator_group_cultures USING btree (groupculture_id);


--
-- Name: trials_app_indicator_group_cultures_indicator_id_3aa1ff50; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX trials_app_indicator_group_cultures_indicator_id_3aa1ff50 ON public.trials_app_indicator_group_cultures USING btree (indicator_id);


--
-- Name: trials_app_oblast_code_c310a0aa_like; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX trials_app_oblast_code_c310a0aa_like ON public.trials_app_oblast USING btree (code varchar_pattern_ops);


--
-- Name: trials_app_oblast_name_b40eb7d1_like; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX trials_app_oblast_name_b40eb7d1_like ON public.trials_app_oblast USING btree (name varchar_pattern_ops);


--
-- Name: trials_app_planneddistribution_application_id_6f451447; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX trials_app_planneddistribution_application_id_6f451447 ON public.trials_app_planneddistribution USING btree (application_id);


--
-- Name: trials_app_planneddistribution_created_by_id_11526a15; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX trials_app_planneddistribution_created_by_id_11526a15 ON public.trials_app_planneddistribution USING btree (created_by_id);


--
-- Name: trials_app_planneddistribution_region_id_3f8c0cb0; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX trials_app_planneddistribution_region_id_3f8c0cb0 ON public.trials_app_planneddistribution USING btree (region_id);


--
-- Name: trials_app_planneddistribution_trial_type_id_1f2e55d2; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX trials_app_planneddistribution_trial_type_id_1f2e55d2 ON public.trials_app_planneddistribution USING btree (trial_type_id);


--
-- Name: trials_app_region_climate_zone_id_e5235d1f; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX trials_app_region_climate_zone_id_e5235d1f ON public.trials_app_region USING btree (climate_zone_id);


--
-- Name: trials_app_region_oblast_id_6745553c; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX trials_app_region_oblast_id_6745553c ON public.trials_app_region USING btree (oblast_id);


--
-- Name: trials_app_sortoriginator_originator_id_1950c760; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX trials_app_sortoriginator_originator_id_1950c760 ON public.trials_app_sortoriginator USING btree (originator_id);


--
-- Name: trials_app_sortoriginator_sort_record_id_ac64ad48; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX trials_app_sortoriginator_sort_record_id_ac64ad48 ON public.trials_app_sortoriginator USING btree (sort_record_id);


--
-- Name: trials_app_sortrecord_culture_id_3b241a4d; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX trials_app_sortrecord_culture_id_3b241a4d ON public.trials_app_sortrecord USING btree (culture_id);


--
-- Name: trials_app_trial_created_by_id_1278f30a; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX trials_app_trial_created_by_id_1278f30a ON public.trials_app_trial USING btree (created_by_id);


--
-- Name: trials_app_trial_culture_id_8c66bf24; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX trials_app_trial_culture_id_8c66bf24 ON public.trials_app_trial USING btree (culture_id);


--
-- Name: trials_app_trial_indicators_indicator_id_65ea677a; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX trials_app_trial_indicators_indicator_id_65ea677a ON public.trials_app_trial_indicators USING btree (indicator_id);


--
-- Name: trials_app_trial_indicators_trial_id_c9960394; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX trials_app_trial_indicators_trial_id_c9960394 ON public.trials_app_trial_indicators USING btree (trial_id);


--
-- Name: trials_app_trial_maturity_group_code_e5e1c97d; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX trials_app_trial_maturity_group_code_e5e1c97d ON public.trials_app_trial USING btree (maturity_group_code);


--
-- Name: trials_app_trial_maturity_group_code_e5e1c97d_like; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX trials_app_trial_maturity_group_code_e5e1c97d_like ON public.trials_app_trial USING btree (maturity_group_code varchar_pattern_ops);


--
-- Name: trials_app_trial_patents_culture_id_8162ed6a; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX trials_app_trial_patents_culture_id_8162ed6a ON public.trials_app_trial USING btree (patents_culture_id);


--
-- Name: trials_app_trial_predecessor_culture_id_16c24fa9; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX trials_app_trial_predecessor_culture_id_16c24fa9 ON public.trials_app_trial USING btree (predecessor_culture_id);


--
-- Name: trials_app_trial_region_id_2be04931; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX trials_app_trial_region_id_2be04931 ON public.trials_app_trial USING btree (region_id);


--
-- Name: trials_app_trial_trial_plan_id_c6526d77; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX trials_app_trial_trial_plan_id_c6526d77 ON public.trials_app_trial USING btree (trial_plan_id);


--
-- Name: trials_app_trial_trial_type_id_a48f52e4; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX trials_app_trial_trial_type_id_a48f52e4 ON public.trials_app_trial USING btree (trial_type_id);


--
-- Name: trials_app_triallaboratoryresult_created_by_id_e66f37b9; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX trials_app_triallaboratoryresult_created_by_id_e66f37b9 ON public.trials_app_triallaboratoryresult USING btree (created_by_id);


--
-- Name: trials_app_triallaboratoryresult_indicator_id_0ec7fee8; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX trials_app_triallaboratoryresult_indicator_id_0ec7fee8 ON public.trials_app_triallaboratoryresult USING btree (indicator_id);


--
-- Name: trials_app_triallaboratoryresult_participant_id_5f944c6f; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX trials_app_triallaboratoryresult_participant_id_5f944c6f ON public.trials_app_triallaboratoryresult USING btree (participant_id);


--
-- Name: trials_app_triallaboratoryresult_trial_id_19fc7a12; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX trials_app_triallaboratoryresult_trial_id_19fc7a12 ON public.trials_app_triallaboratoryresult USING btree (trial_id);


--
-- Name: trials_app_trialparticipant_application_id_799501b0; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX trials_app_trialparticipant_application_id_799501b0 ON public.trials_app_trialparticipant USING btree (application_id);


--
-- Name: trials_app_trialparticipant_sort_record_id_eacaf123; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX trials_app_trialparticipant_sort_record_id_eacaf123 ON public.trials_app_trialparticipant USING btree (sort_record_id);


--
-- Name: trials_app_trialparticipant_statistical_result_49c52c79; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX trials_app_trialparticipant_statistical_result_49c52c79 ON public.trials_app_trialparticipant USING btree (statistical_result);


--
-- Name: trials_app_trialparticipant_trial_id_fe1c719a; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX trials_app_trialparticipant_trial_id_fe1c719a ON public.trials_app_trialparticipant USING btree (trial_id);


--
-- Name: trials_app_trialplan_created_by_id_8305b52f; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX trials_app_trialplan_created_by_id_8305b52f ON public.trials_app_trialplan USING btree (created_by_id);


--
-- Name: trials_app_trialplan_oblast_id_d8488688; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX trials_app_trialplan_oblast_id_d8488688 ON public.trials_app_trialplan USING btree (oblast_id);


--
-- Name: trials_app_trialplan_trial_type_id_5e3cf81b; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX trials_app_trialplan_trial_type_id_5e3cf81b ON public.trials_app_trialplan USING btree (trial_type_id);


--
-- Name: trials_app_trialplancultur_trial_plan_culture_id_5246cd2a; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX trials_app_trialplancultur_trial_plan_culture_id_5246cd2a ON public.trials_app_trialplanculturetrialtype USING btree (trial_plan_culture_id);


--
-- Name: trials_app_trialplanculture_created_by_id_0b052d10; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX trials_app_trialplanculture_created_by_id_0b052d10 ON public.trials_app_trialplanculture USING btree (created_by_id);


--
-- Name: trials_app_trialplanculture_culture_id_51b51873; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX trials_app_trialplanculture_culture_id_51b51873 ON public.trials_app_trialplanculture USING btree (culture_id);


--
-- Name: trials_app_trialplanculture_trial_plan_id_40742b01; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX trials_app_trialplanculture_trial_plan_id_40742b01 ON public.trials_app_trialplanculture USING btree (trial_plan_id);


--
-- Name: trials_app_trialplanculturetrialtype_created_by_id_d181b7e4; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX trials_app_trialplanculturetrialtype_created_by_id_d181b7e4 ON public.trials_app_trialplanculturetrialtype USING btree (created_by_id);


--
-- Name: trials_app_trialplanculturetrialtype_trial_type_id_a0db01bd; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX trials_app_trialplanculturetrialtype_trial_type_id_a0db01bd ON public.trials_app_trialplanculturetrialtype USING btree (trial_type_id);


--
-- Name: trials_app_trialplanparticipant_application_id_cc962c50; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX trials_app_trialplanparticipant_application_id_cc962c50 ON public.trials_app_trialplanparticipant USING btree (application_id);


--
-- Name: trials_app_trialplanparticipant_created_by_id_32fcc111; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX trials_app_trialplanparticipant_created_by_id_32fcc111 ON public.trials_app_trialplanparticipant USING btree (created_by_id);


--
-- Name: trials_app_trialplanparticipant_culture_trial_type_id_a09b9b2b; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX trials_app_trialplanparticipant_culture_trial_type_id_a09b9b2b ON public.trials_app_trialplanparticipant USING btree (culture_trial_type_id);


--
-- Name: trials_app_trialplantrial_created_by_id_96859269; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX trials_app_trialplantrial_created_by_id_96859269 ON public.trials_app_trialplantrial USING btree (created_by_id);


--
-- Name: trials_app_trialplantrial_participant_id_9e1e230c; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX trials_app_trialplantrial_participant_id_9e1e230c ON public.trials_app_trialplantrial USING btree (participant_id);


--
-- Name: trials_app_trialplantrial_region_id_a3504bfb; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX trials_app_trialplantrial_region_id_a3504bfb ON public.trials_app_trialplantrial USING btree (region_id);


--
-- Name: trials_app_trialresult_created_by_id_ba60bf5a; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX trials_app_trialresult_created_by_id_ba60bf5a ON public.trials_app_trialresult USING btree (created_by_id);


--
-- Name: trials_app_trialresult_indicator_id_fcc439b7; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX trials_app_trialresult_indicator_id_fcc439b7 ON public.trials_app_trialresult USING btree (indicator_id);


--
-- Name: trials_app_trialresult_participant_id_fa13ef4a; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX trials_app_trialresult_participant_id_fa13ef4a ON public.trials_app_trialresult USING btree (participant_id);


--
-- Name: trials_app_trialresult_sort_record_id_46f372cb; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX trials_app_trialresult_sort_record_id_46f372cb ON public.trials_app_trialresult USING btree (sort_record_id);


--
-- Name: trials_app_trialresult_trial_id_5ce7d750; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX trials_app_trialresult_trial_id_5ce7d750 ON public.trials_app_trialresult USING btree (trial_id);


--
-- Name: trials_app_trialtype_code_66b29021_like; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX trials_app_trialtype_code_66b29021_like ON public.trials_app_trialtype USING btree (code varchar_pattern_ops);


--
-- Name: auth_group_permissions auth_group_permissio_permission_id_84c5c92e_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissio_permission_id_84c5c92e_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permissions auth_group_permissions_group_id_b120cbf9_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_b120cbf9_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_permission auth_permission_content_type_id_2f476e4b_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_2f476e4b_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_groups auth_user_groups_group_id_97559544_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_group_id_97559544_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_groups auth_user_groups_user_id_6a12ed8b_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_6a12ed8b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_user_permissions auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_user_permissions auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: authtoken_token authtoken_token_user_id_35299eff_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.authtoken_token
    ADD CONSTRAINT authtoken_token_user_id_35299eff_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_log_content_type_id_c4bce8eb_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_content_type_id_c4bce8eb_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_log_user_id_c564eba6_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_user_id_c564eba6_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: trials_app_applicationdecisionhistory trials_app_applicati_application_id_91f33d25_fk_trials_ap; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.trials_app_applicationdecisionhistory
    ADD CONSTRAINT trials_app_applicati_application_id_91f33d25_fk_trials_ap FOREIGN KEY (application_id) REFERENCES public.trials_app_application(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: trials_app_application_target_oblasts trials_app_applicati_application_id_bcd7129f_fk_trials_ap; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.trials_app_application_target_oblasts
    ADD CONSTRAINT trials_app_applicati_application_id_bcd7129f_fk_trials_ap FOREIGN KEY (application_id) REFERENCES public.trials_app_application(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: trials_app_applicationdecisionhistory trials_app_applicati_decided_by_id_2e8aa2c0_fk_auth_user; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.trials_app_applicationdecisionhistory
    ADD CONSTRAINT trials_app_applicati_decided_by_id_2e8aa2c0_fk_auth_user FOREIGN KEY (decided_by_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: trials_app_application_target_oblasts trials_app_applicati_oblast_id_3d905481_fk_trials_ap; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.trials_app_application_target_oblasts
    ADD CONSTRAINT trials_app_applicati_oblast_id_3d905481_fk_trials_ap FOREIGN KEY (oblast_id) REFERENCES public.trials_app_oblast(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: trials_app_applicationdecisionhistory trials_app_applicati_oblast_id_60ea54ab_fk_trials_ap; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.trials_app_applicationdecisionhistory
    ADD CONSTRAINT trials_app_applicati_oblast_id_60ea54ab_fk_trials_ap FOREIGN KEY (oblast_id) REFERENCES public.trials_app_oblast(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: trials_app_application trials_app_applicati_sort_record_id_54e27471_fk_trials_ap; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.trials_app_application
    ADD CONSTRAINT trials_app_applicati_sort_record_id_54e27471_fk_trials_ap FOREIGN KEY (sort_record_id) REFERENCES public.trials_app_sortrecord(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: trials_app_application trials_app_application_created_by_id_42010fc1_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.trials_app_application
    ADD CONSTRAINT trials_app_application_created_by_id_42010fc1_fk_auth_user_id FOREIGN KEY (created_by_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: trials_app_application_target_oblasts trials_app_application_target_oblasts_decided_by_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.trials_app_application_target_oblasts
    ADD CONSTRAINT trials_app_application_target_oblasts_decided_by_id_fkey FOREIGN KEY (decided_by_id) REFERENCES public.auth_user(id) ON DELETE SET NULL;


--
-- Name: trials_app_application_target_oblasts trials_app_application_target_oblasts_trial_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.trials_app_application_target_oblasts
    ADD CONSTRAINT trials_app_application_target_oblasts_trial_id_fkey FOREIGN KEY (trial_id) REFERENCES public.trials_app_trial(id) ON DELETE SET NULL;


--
-- Name: trials_app_application_target_oblasts trials_app_application_target_oblasts_trial_plan_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.trials_app_application_target_oblasts
    ADD CONSTRAINT trials_app_application_target_oblasts_trial_plan_id_fkey FOREIGN KEY (trial_plan_id) REFERENCES public.trials_app_trialplan(id) ON DELETE SET NULL;


--
-- Name: trials_app_culture trials_app_culture_group_culture_id_3df16e08_fk_trials_ap; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.trials_app_culture
    ADD CONSTRAINT trials_app_culture_group_culture_id_3df16e08_fk_trials_ap FOREIGN KEY (group_culture_id) REFERENCES public.trials_app_groupculture(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: trials_app_document trials_app_document_application_id_3df2eb59_fk_trials_ap; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.trials_app_document
    ADD CONSTRAINT trials_app_document_application_id_3df2eb59_fk_trials_ap FOREIGN KEY (application_id) REFERENCES public.trials_app_application(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: trials_app_document trials_app_document_trial_id_a13eea15_fk_trials_app_trial_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.trials_app_document
    ADD CONSTRAINT trials_app_document_trial_id_a13eea15_fk_trials_app_trial_id FOREIGN KEY (trial_id) REFERENCES public.trials_app_trial(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: trials_app_document trials_app_document_uploaded_by_id_7a8f4d1e_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.trials_app_document
    ADD CONSTRAINT trials_app_document_uploaded_by_id_7a8f4d1e_fk_auth_user_id FOREIGN KEY (uploaded_by_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: trials_app_indicator_group_cultures trials_app_indicator_groupculture_id_23aac67c_fk_trials_ap; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.trials_app_indicator_group_cultures
    ADD CONSTRAINT trials_app_indicator_groupculture_id_23aac67c_fk_trials_ap FOREIGN KEY (groupculture_id) REFERENCES public.trials_app_groupculture(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: trials_app_indicator_group_cultures trials_app_indicator_indicator_id_3aa1ff50_fk_trials_ap; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.trials_app_indicator_group_cultures
    ADD CONSTRAINT trials_app_indicator_indicator_id_3aa1ff50_fk_trials_ap FOREIGN KEY (indicator_id) REFERENCES public.trials_app_indicator(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: trials_app_planneddistribution trials_app_planneddi_application_id_6f451447_fk_trials_ap; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.trials_app_planneddistribution
    ADD CONSTRAINT trials_app_planneddi_application_id_6f451447_fk_trials_ap FOREIGN KEY (application_id) REFERENCES public.trials_app_application(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: trials_app_planneddistribution trials_app_planneddi_created_by_id_11526a15_fk_auth_user; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.trials_app_planneddistribution
    ADD CONSTRAINT trials_app_planneddi_created_by_id_11526a15_fk_auth_user FOREIGN KEY (created_by_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: trials_app_planneddistribution trials_app_planneddi_region_id_3f8c0cb0_fk_trials_ap; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.trials_app_planneddistribution
    ADD CONSTRAINT trials_app_planneddi_region_id_3f8c0cb0_fk_trials_ap FOREIGN KEY (region_id) REFERENCES public.trials_app_region(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: trials_app_planneddistribution trials_app_planneddi_trial_type_id_1f2e55d2_fk_trials_ap; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.trials_app_planneddistribution
    ADD CONSTRAINT trials_app_planneddi_trial_type_id_1f2e55d2_fk_trials_ap FOREIGN KEY (trial_type_id) REFERENCES public.trials_app_trialtype(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: trials_app_region trials_app_region_climate_zone_id_e5235d1f_fk_trials_ap; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.trials_app_region
    ADD CONSTRAINT trials_app_region_climate_zone_id_e5235d1f_fk_trials_ap FOREIGN KEY (climate_zone_id) REFERENCES public.trials_app_climatezone(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: trials_app_region trials_app_region_oblast_id_6745553c_fk_trials_app_oblast_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.trials_app_region
    ADD CONSTRAINT trials_app_region_oblast_id_6745553c_fk_trials_app_oblast_id FOREIGN KEY (oblast_id) REFERENCES public.trials_app_oblast(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: trials_app_sortoriginator trials_app_sortorigi_originator_id_1950c760_fk_trials_ap; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.trials_app_sortoriginator
    ADD CONSTRAINT trials_app_sortorigi_originator_id_1950c760_fk_trials_ap FOREIGN KEY (originator_id) REFERENCES public.trials_app_originator(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: trials_app_sortoriginator trials_app_sortorigi_sort_record_id_ac64ad48_fk_trials_ap; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.trials_app_sortoriginator
    ADD CONSTRAINT trials_app_sortorigi_sort_record_id_ac64ad48_fk_trials_ap FOREIGN KEY (sort_record_id) REFERENCES public.trials_app_sortrecord(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: trials_app_sortrecord trials_app_sortrecor_culture_id_3b241a4d_fk_trials_ap; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.trials_app_sortrecord
    ADD CONSTRAINT trials_app_sortrecor_culture_id_3b241a4d_fk_trials_ap FOREIGN KEY (culture_id) REFERENCES public.trials_app_culture(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: trials_app_trial trials_app_trial_created_by_id_1278f30a_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.trials_app_trial
    ADD CONSTRAINT trials_app_trial_created_by_id_1278f30a_fk_auth_user_id FOREIGN KEY (created_by_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: trials_app_trial trials_app_trial_culture_id_8c66bf24_fk_trials_app_culture_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.trials_app_trial
    ADD CONSTRAINT trials_app_trial_culture_id_8c66bf24_fk_trials_app_culture_id FOREIGN KEY (culture_id) REFERENCES public.trials_app_culture(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: trials_app_trial_indicators trials_app_trial_ind_indicator_id_65ea677a_fk_trials_ap; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.trials_app_trial_indicators
    ADD CONSTRAINT trials_app_trial_ind_indicator_id_65ea677a_fk_trials_ap FOREIGN KEY (indicator_id) REFERENCES public.trials_app_indicator(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: trials_app_trial_indicators trials_app_trial_ind_trial_id_c9960394_fk_trials_ap; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.trials_app_trial_indicators
    ADD CONSTRAINT trials_app_trial_ind_trial_id_c9960394_fk_trials_ap FOREIGN KEY (trial_id) REFERENCES public.trials_app_trial(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: trials_app_trial trials_app_trial_predecessor_culture__16c24fa9_fk_trials_ap; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.trials_app_trial
    ADD CONSTRAINT trials_app_trial_predecessor_culture__16c24fa9_fk_trials_ap FOREIGN KEY (predecessor_culture_id) REFERENCES public.trials_app_culture(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: trials_app_trial trials_app_trial_region_id_2be04931_fk_trials_app_region_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.trials_app_trial
    ADD CONSTRAINT trials_app_trial_region_id_2be04931_fk_trials_app_region_id FOREIGN KEY (region_id) REFERENCES public.trials_app_region(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: trials_app_trial trials_app_trial_trial_plan_id_c6526d77_fk_trials_ap; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.trials_app_trial
    ADD CONSTRAINT trials_app_trial_trial_plan_id_c6526d77_fk_trials_ap FOREIGN KEY (trial_plan_id) REFERENCES public.trials_app_trialplan(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: trials_app_trial trials_app_trial_trial_type_id_a48f52e4_fk_trials_ap; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.trials_app_trial
    ADD CONSTRAINT trials_app_trial_trial_type_id_a48f52e4_fk_trials_ap FOREIGN KEY (trial_type_id) REFERENCES public.trials_app_trialtype(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: trials_app_triallaboratoryresult trials_app_triallabo_created_by_id_e66f37b9_fk_auth_user; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.trials_app_triallaboratoryresult
    ADD CONSTRAINT trials_app_triallabo_created_by_id_e66f37b9_fk_auth_user FOREIGN KEY (created_by_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: trials_app_triallaboratoryresult trials_app_triallabo_indicator_id_0ec7fee8_fk_trials_ap; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.trials_app_triallaboratoryresult
    ADD CONSTRAINT trials_app_triallabo_indicator_id_0ec7fee8_fk_trials_ap FOREIGN KEY (indicator_id) REFERENCES public.trials_app_indicator(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: trials_app_triallaboratoryresult trials_app_triallabo_participant_id_5f944c6f_fk_trials_ap; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.trials_app_triallaboratoryresult
    ADD CONSTRAINT trials_app_triallabo_participant_id_5f944c6f_fk_trials_ap FOREIGN KEY (participant_id) REFERENCES public.trials_app_trialparticipant(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: trials_app_triallaboratoryresult trials_app_triallabo_trial_id_19fc7a12_fk_trials_ap; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.trials_app_triallaboratoryresult
    ADD CONSTRAINT trials_app_triallabo_trial_id_19fc7a12_fk_trials_ap FOREIGN KEY (trial_id) REFERENCES public.trials_app_trial(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: trials_app_trialparticipant trials_app_trialpart_application_id_799501b0_fk_trials_ap; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.trials_app_trialparticipant
    ADD CONSTRAINT trials_app_trialpart_application_id_799501b0_fk_trials_ap FOREIGN KEY (application_id) REFERENCES public.trials_app_application(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: trials_app_trialparticipant trials_app_trialpart_sort_record_id_eacaf123_fk_trials_ap; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.trials_app_trialparticipant
    ADD CONSTRAINT trials_app_trialpart_sort_record_id_eacaf123_fk_trials_ap FOREIGN KEY (sort_record_id) REFERENCES public.trials_app_sortrecord(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: trials_app_trialparticipant trials_app_trialpart_trial_id_fe1c719a_fk_trials_ap; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.trials_app_trialparticipant
    ADD CONSTRAINT trials_app_trialpart_trial_id_fe1c719a_fk_trials_ap FOREIGN KEY (trial_id) REFERENCES public.trials_app_trial(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: trials_app_trialplanparticipant trials_app_trialplan_application_id_cc962c50_fk_trials_ap; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.trials_app_trialplanparticipant
    ADD CONSTRAINT trials_app_trialplan_application_id_cc962c50_fk_trials_ap FOREIGN KEY (application_id) REFERENCES public.trials_app_application(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: trials_app_trialplanculture trials_app_trialplan_created_by_id_0b052d10_fk_auth_user; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.trials_app_trialplanculture
    ADD CONSTRAINT trials_app_trialplan_created_by_id_0b052d10_fk_auth_user FOREIGN KEY (created_by_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: trials_app_trialplanparticipant trials_app_trialplan_created_by_id_32fcc111_fk_auth_user; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.trials_app_trialplanparticipant
    ADD CONSTRAINT trials_app_trialplan_created_by_id_32fcc111_fk_auth_user FOREIGN KEY (created_by_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: trials_app_trialplan trials_app_trialplan_created_by_id_8305b52f_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.trials_app_trialplan
    ADD CONSTRAINT trials_app_trialplan_created_by_id_8305b52f_fk_auth_user_id FOREIGN KEY (created_by_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: trials_app_trialplantrial trials_app_trialplan_created_by_id_96859269_fk_auth_user; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.trials_app_trialplantrial
    ADD CONSTRAINT trials_app_trialplan_created_by_id_96859269_fk_auth_user FOREIGN KEY (created_by_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: trials_app_trialplanculturetrialtype trials_app_trialplan_created_by_id_d181b7e4_fk_auth_user; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.trials_app_trialplanculturetrialtype
    ADD CONSTRAINT trials_app_trialplan_created_by_id_d181b7e4_fk_auth_user FOREIGN KEY (created_by_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: trials_app_trialplanculture trials_app_trialplan_culture_id_51b51873_fk_trials_ap; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.trials_app_trialplanculture
    ADD CONSTRAINT trials_app_trialplan_culture_id_51b51873_fk_trials_ap FOREIGN KEY (culture_id) REFERENCES public.trials_app_culture(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: trials_app_trialplanparticipant trials_app_trialplan_culture_trial_type_i_a09b9b2b_fk_trials_ap; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.trials_app_trialplanparticipant
    ADD CONSTRAINT trials_app_trialplan_culture_trial_type_i_a09b9b2b_fk_trials_ap FOREIGN KEY (culture_trial_type_id) REFERENCES public.trials_app_trialplanculturetrialtype(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: trials_app_trialplan trials_app_trialplan_oblast_id_d8488688_fk_trials_app_oblast_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.trials_app_trialplan
    ADD CONSTRAINT trials_app_trialplan_oblast_id_d8488688_fk_trials_app_oblast_id FOREIGN KEY (oblast_id) REFERENCES public.trials_app_oblast(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: trials_app_trialplantrial trials_app_trialplan_participant_id_9e1e230c_fk_trials_ap; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.trials_app_trialplantrial
    ADD CONSTRAINT trials_app_trialplan_participant_id_9e1e230c_fk_trials_ap FOREIGN KEY (participant_id) REFERENCES public.trials_app_trialplanparticipant(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: trials_app_trialplantrial trials_app_trialplan_region_id_a3504bfb_fk_trials_ap; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.trials_app_trialplantrial
    ADD CONSTRAINT trials_app_trialplan_region_id_a3504bfb_fk_trials_ap FOREIGN KEY (region_id) REFERENCES public.trials_app_region(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: trials_app_trialplanculturetrialtype trials_app_trialplan_trial_plan_culture_i_5246cd2a_fk_trials_ap; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.trials_app_trialplanculturetrialtype
    ADD CONSTRAINT trials_app_trialplan_trial_plan_culture_i_5246cd2a_fk_trials_ap FOREIGN KEY (trial_plan_culture_id) REFERENCES public.trials_app_trialplanculture(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: trials_app_trialplanculture trials_app_trialplan_trial_plan_id_40742b01_fk_trials_ap; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.trials_app_trialplanculture
    ADD CONSTRAINT trials_app_trialplan_trial_plan_id_40742b01_fk_trials_ap FOREIGN KEY (trial_plan_id) REFERENCES public.trials_app_trialplan(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: trials_app_trialplan trials_app_trialplan_trial_type_id_5e3cf81b_fk_trials_ap; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.trials_app_trialplan
    ADD CONSTRAINT trials_app_trialplan_trial_type_id_5e3cf81b_fk_trials_ap FOREIGN KEY (trial_type_id) REFERENCES public.trials_app_trialtype(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: trials_app_trialplanculturetrialtype trials_app_trialplan_trial_type_id_a0db01bd_fk_trials_ap; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.trials_app_trialplanculturetrialtype
    ADD CONSTRAINT trials_app_trialplan_trial_type_id_a0db01bd_fk_trials_ap FOREIGN KEY (trial_type_id) REFERENCES public.trials_app_trialtype(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: trials_app_trialresult trials_app_trialresu_indicator_id_fcc439b7_fk_trials_ap; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.trials_app_trialresult
    ADD CONSTRAINT trials_app_trialresu_indicator_id_fcc439b7_fk_trials_ap FOREIGN KEY (indicator_id) REFERENCES public.trials_app_indicator(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: trials_app_trialresult trials_app_trialresu_participant_id_fa13ef4a_fk_trials_ap; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.trials_app_trialresult
    ADD CONSTRAINT trials_app_trialresu_participant_id_fa13ef4a_fk_trials_ap FOREIGN KEY (participant_id) REFERENCES public.trials_app_trialparticipant(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: trials_app_trialresult trials_app_trialresu_sort_record_id_46f372cb_fk_trials_ap; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.trials_app_trialresult
    ADD CONSTRAINT trials_app_trialresu_sort_record_id_46f372cb_fk_trials_ap FOREIGN KEY (sort_record_id) REFERENCES public.trials_app_sortrecord(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: trials_app_trialresult trials_app_trialresult_created_by_id_ba60bf5a_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.trials_app_trialresult
    ADD CONSTRAINT trials_app_trialresult_created_by_id_ba60bf5a_fk_auth_user_id FOREIGN KEY (created_by_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: trials_app_trialresult trials_app_trialresult_trial_id_5ce7d750_fk_trials_app_trial_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.trials_app_trialresult
    ADD CONSTRAINT trials_app_trialresult_trial_id_5ce7d750_fk_trials_app_trial_id FOREIGN KEY (trial_id) REFERENCES public.trials_app_trial(id) DEFERRABLE INITIALLY DEFERRED;


--
-- PostgreSQL database dump complete
--

\unrestrict fjvq9d8G1kNG8APTjn6xGFOAO5949mB8NcxJH0gx8fWy4xW6sJIOYJPexzTC4Pg

