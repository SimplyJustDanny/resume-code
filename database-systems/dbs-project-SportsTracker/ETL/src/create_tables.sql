
create table if not exists sports(id serial primary key, name varchar(255), gender char(1), venue VARCHAR(10))

create table if not exists exercises(id serial primary key, alter_id VARCHAR, name VARCHAR, force VARCHAR, level VARCHAR, mechanic VARCHAR, equipment VARCHAR, category VARCHAR)

create table if not exists sport_exercises(sport INT references sports(id), exercise INT references exercises(id), primary key (sport, exercise))

create table if not exists exercise_instructions(id serial primary key ,exercise_id INT references exercises(id), instruction_number INT, instruction TEXT NOT NULL)

create table if not exists exercise_primary_muscles(id serial primary key , exercise_id INT references exercises(id), muscle VARCHAR NOT NULL)

create table if not exists exercise_secondary_muscles(id serial primary key, exercise_id INT references exercises(id), muscle VARCHAR NOT NULL)

create table if not exists exercise_images(id serial primary key, exercise_id INT references exercises(id),image_path VARCHAR)

create table if not exists teams(id serial primary key, name VARCHAR(255), sport INT references sports(id))

create table if not exists championships(id serial primary key, name VARCHAR(255), winner_team INT references teams(id), winner_year INT )

create table if not exists athletes(id serial primary key , name VARCHAR(255), age INT, gender CHAR(1), height DECIMAL(5,2), weight DECIMAL(5,2))

create table if not exists practices(fk_team INT references teams(id), fk_athlete INT references athletes(id), primary key(fk_team,fk_athlete) , season VARCHAR(50))
