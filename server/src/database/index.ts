const { Pool } = require('pg');
const { DB_USER, DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT } = require('../constants');

const pool = new Pool({
  user: DB_USER,
  host: DB_HOST,
  database: DB_NAME, // Replace 'name_of_db' with the actual name of your PostgreSQL database
  password: DB_PASSWORD, // Replace 'your_password' with the password for your PostgreSQL user
  port: DB_PORT, // The default port for PostgreSQL is 5432
});

module.exports = {
  query: (text: string, params: any[]) => pool.query(text, params),
}