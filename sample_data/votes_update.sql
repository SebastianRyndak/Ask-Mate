ALTER TABLE public.question
ADD votes_up INT
DEFAULT 0;

ALTER TABLE public.question
ADD votes_down INT
DEFAULT 0;

ALTER TABLE public.answer
ADD votes_up INT
DEFAULT 0;

ALTER TABLE public.answer
ADD votes_down INT
DEFAULT 0;