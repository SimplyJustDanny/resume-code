
create table exercise_fragments (ctxid serial primary key , content text, embedding vector(768));

create table if not exists users (id serial primary key, email VARCHAR(255) not null, username VARCHAR(255) not null, userpassword VARCHAR(255) not null, created VARCHAR(255) not null);
