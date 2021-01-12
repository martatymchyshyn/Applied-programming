create table if not exists locations(
    id serial PRIMARY KEY,
    name varchar(50)
);

create table if not exists users(
    id serial PRIMARY KEY,
    first_name varchar(50),
    last_name varchar(50),
    password varchar(50),
    user_name varchar(50),
    location_id bigint,
    FOREIGN KEY (location_id) REFERENCES locations(id)
);

create table if not exists advertisements(
    id serial PRIMARY KEY,
    title varchar(40),
    body varchar(255),
    is_public boolean,
    user_id bigint,
    FOREIGN KEY (user_id) REFERENCES users(id)
);