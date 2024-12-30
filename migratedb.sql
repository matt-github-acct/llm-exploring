CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    zipcode VARCHAR(10) DEFAULT '84092'
);

INSERT INTO users (name, zipcode) VALUES ('Alice', '12345'), ('Bob', '67890');
