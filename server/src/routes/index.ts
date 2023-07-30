import { Router } from "express";
import {
  getUsers,
  registerUser,
  loginUser,
  logoutUser,
} from "../controllers/userControllers";
import {
  emailFormatValidator,
  emailExistsValidator,
  passwordComplexityValidator,
} from "../validators/registrationValidators";
import { loginFieldsValidator } from "../validators/loginValidators";
import { validationsMiddleware } from "../middlewares/validationsMiddleware";

const router: Router = Router();

// Test Route
router.get("/users", getUsers);

// User Routes
router.post(
  "/register",
  emailFormatValidator,
  emailExistsValidator,
  passwordComplexityValidator,
  validationsMiddleware,
  registerUser
);
router.post("/login", loginFieldsValidator, validationsMiddleware, loginUser);
router.post("/logout", logoutUser)

module.exports = router;
