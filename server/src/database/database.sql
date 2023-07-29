-- users table

CREATE TABLE users (
  user_id SERIAL PRIMARY KEY,
  user_email VARCHAR(255) UNIQUE NOT NULL,
  user_password VARCHAR(255) NOT NULL,
  user_site VARCHAR(255) NOT NULL,
  user_role VARCHAR(255) NOT NULL,
  created_at date default CURRENT_DATE
);