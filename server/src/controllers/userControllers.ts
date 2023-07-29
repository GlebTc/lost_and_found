import { Request, Response } from "express";
const db = require("../database");
const { hash } = require("bcryptjs");

export const getUsers = async (req: Request, res: Response) => {
  try {
    const { rows } = await db.query("SELECT * FROM users");
    res.status(400).send({
      success: true,
      data: rows,
    });
  } catch (err) {
    console.log(err);
  }
};

export const registerUser = async (req: Request, res: Response) => {
  try {
    const { user_email, user_password, user_site, user_role } =
      req.body;
    const hashedPassword = await hash(user_password, 10);
    const { rows } = await db.query(
      "INSERT INTO users (user_email, user_password, user_site, user_role) VALUES ($1, $2, $3, $4) RETURNING *",
      [user_email, hashedPassword, user_site, user_role]
    );
    res.status(201).send({
      success: true,
      data: rows[0],
    });
  } catch (err) {
    console.log(err);
  }
};
