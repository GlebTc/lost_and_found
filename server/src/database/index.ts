const { Pool } = require('pg');

const pool = new Pool({
  user: 'postgres',
  host: 'localhost',
  database: 'lost_and_found', // Replace 'name_of_db' with the actual name of your PostgreSQL database
  password: 'postgres', // Replace 'your_password' with the password for your PostgreSQL user
  port: 5432, // The default port for PostgreSQL is 5432
});

module.exports = {
  query: (text: string, params: any[]) => pool.query(text, params),
}