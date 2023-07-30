import { Request } from "express";
const { check } = require("express-validator");
const db = require("../database");
const { compare } = require("bcryptjs");

// Login Fields Validator
export const loginFieldsValidator = check("user_email").custom(
  async (value: String, { req }: { req: Request }) => {
    const user = await db.query("SELECT * FROM users WHERE user_email = $1", [
      value,
    ]);

    if (!user.rows.length) {
      throw new Error("Email does not exist");
    }

    const validPassword = await compare(
      req.body.user_password,
      user.rows[0].user_password
    ); // It looks like the compare function automatically unhashes the password from the database and compares it to the password from the request body.  Both hash and compare methods are from the bcryptjs library.

    if (!validPassword) {
      throw new Error("Invalid password");
    }

    return user.rows
  }
);
