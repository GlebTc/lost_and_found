import { Request, Response } from "express";
const db = require("../database");
const { hash } = require("bcryptjs");
const { sign } = require("jsonwebtoken");
const { SECRET } = require ("../constants")

interface Payload {
  user_email: string;
  user_password: string;
}

//  Get All users
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

// Register a New User
export const registerUser = async (req: Request, res: Response) => {
  try {
    const { user_email, user_password, user_site, user_role } = req.body;
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

// User Login
export const loginUser = async (req: Request, res: Response) => {
  // The request object is coming from loginValidators.js line 26, where we are explicitly setting the request object to the user object from the database
  const {user_email, user_password} = req.body

  try {
    const payload: Payload = {
      user_email: user_email,
      user_password: user_password,
    };

    const token = sign(payload, SECRET);

    const response = await db.query("SELECT * FROM users WHERE user_email = $1", [
        user_email,
      ]);

    res.status(200).cookie("access_token", token, { httpOnly: true }).json({
      success: true,
      userInfo: response.rows[0],
      message: "User logged in successfully",
    });
  } catch (error: any) { 
    return res.status(500).json({
      success: false,
      message: error.message,
    });
  }
};

// User Logout
export const logoutUser = async (req: Request, res: Response) => {
  try {
    res.clearCookie("access_token").json({
      success: true,
      message: "User logged out successfully",
    });
  } catch (error: any) {
    return res.status(500).json({
      success: false,
      message: error.message,
    });
  }
}
