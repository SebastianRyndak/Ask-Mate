-- Table: public.user

DROP TABLE IF EXISTS public."user" CASCADE;

CREATE TABLE IF NOT EXISTS public."user"
(
    id uuid NOT NULL DEFAULT gen_random_uuid(),
    username text COLLATE pg_catalog."default",
    registration_date timestamp without time zone,
    reputation integer DEFAULT 0,
    CONSTRAINT user_pkey PRIMARY KEY (id)
);

--ALTER TABLE IF EXISTS public."user"
--    OWNER to postgres;

--ALTER TABLE IF EXISTS public.answer
--    ADD COLUMN user_id uuid;

--ALTER TABLE IF EXISTS public.comment
--    ADD COLUMN user_id uuid;

--ALTER TABLE IF EXISTS public.question
--    ADD COLUMN user_id uuid;

ALTER TABLE ONLY public.answer
    ADD CONSTRAINT fk_user_id FOREIGN KEY (user_id) REFERENCES public.user(id);

ALTER TABLE ONLY public.comment
    ADD CONSTRAINT fk_user_id FOREIGN KEY (user_id) REFERENCES public.user(id);

ALTER TABLE ONLY public.question
    ADD CONSTRAINT fk_user_id FOREIGN KEY (user_id) REFERENCES public.user(id);