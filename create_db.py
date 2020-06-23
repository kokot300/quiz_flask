q = """create table questions(
id serial, question text,
aaa varchar(60),
bbb varchar(60),
ccc varchar(60),
ddd varchar(60),
correct varchar(1),
category_id int,
when_added timestamp NOT NULL,
PRIMARY KEY (id),
FOREIGN KEY (category_id) REFERENCES categories(id));"""

q2="""CREATE TABLE categories(
id serial,
name varchar(60),
PRIMARY KEY (id)
);"""