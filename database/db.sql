create extension if not exists pgcrypto;

create table public.blocked_ips (
  ip text not null,
  reason text null,
  blocked_at timestamp with time zone null default now(),
  constraint blocked_ips_pkey primary key (ip)
) TABLESPACE pg_default;

create table public.blushes (
  code text not null,
  sender_name text not null,
  message text not null,
  password_hash text not null,
  status text null default 'unread'::text,
  reply text null,
  replied_at timestamp with time zone null,
  created_at timestamp with time zone null default now(),
  creator_ip text null,
  constraint blushes_pkey primary key (code)
) TABLESPACE pg_default;

create table public.confessions (
  id uuid not null default gen_random_uuid (),
  receiver_name text not null,
  content text not null,
  creator_ip text null,
  created_at timestamp with time zone null default now(),
  constraint confessions_pkey primary key (id)
) TABLESPACE pg_default;

create table public.conversation_messages (
  id uuid not null default gen_random_uuid (),
  conversation_id uuid null,
  sender_type text null,
  encrypted_content text not null,
  created_at timestamp with time zone null default now(),
  constraint conversation_messages_pkey primary key (id),
  constraint conversation_messages_conversation_id_fkey foreign KEY (conversation_id) references conversations (id) on delete CASCADE,
  constraint conversation_messages_sender_type_check check (
    (
      sender_type = any (array['creator'::text, 'recipient'::text])
    )
  )
) TABLESPACE pg_default;

create table public.conversations (
  id uuid not null default gen_random_uuid (),
  public_token text not null,
  creator_token text not null,
  password_hash text not null,
  creator_flower text not null,
  recipient_flower text not null,
  failed_attempts integer null default 0,
  locked_until timestamp with time zone null,
  status text null default 'active'::text,
  max_messages integer null default 10,
  expires_at timestamp with time zone not null,
  created_at timestamp with time zone null default now(),
  constraint conversations_pkey primary key (id),
  constraint conversations_creator_token_key unique (creator_token),
  constraint conversations_public_token_key unique (public_token)
) TABLESPACE pg_default;

create table public.global_stats (
  id integer not null,
  total_created bigint null default 0,
  confessions_total bigint null default 0,
  constraint global_stats_pkey primary key (id),
  constraint global_stats_id_check check ((id = 1))
) TABLESPACE pg_default;

create table public.reported_blushes (
  id serial not null,
  original_code text null,
  sender_name text null,
  message_encrypted text null,
  reporter_ip text null,
  reported_at timestamp with time zone null default now(),
  sender_ip text null,
  constraint reported_blushes_pkey primary key (id)
) TABLESPACE pg_default;

