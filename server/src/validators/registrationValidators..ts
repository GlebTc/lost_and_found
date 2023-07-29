const { check } = require('express-validator');
const db = require('../database');

// Email format validator
export const emailFormatValidator = check('user_email').isEmail().withMessage("please use valid email")

// Email exists validator
export const emailExistsValidator = check('user_email').custom( async (user_email: String) => {
    const { rows } = await db.query('SELECT * FROM users WHERE user_email = $1', [user_email]);
    if (rows.length) {
        throw new Error('Email already exists');
    }
})

// Password Complexity Validator
export const passwordComplexityValidator = check('password')
  .isLength({ min: 6 })
  .withMessage('Password must be at least 6 characters long')
  .matches(/^(?=.*[$@!])(?=.*\d)/)
  .withMessage('Password must contain at least one number and at least one symbol');