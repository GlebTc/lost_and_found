import { Router } from "express";
import { getUsers, registerUser } from "../controllers/userControllers";
import {
  emailFormatValidator,
  emailExistsValidator,
  passwordComplexityValidator,
} from "../validators/registrationValidators.";
import { validationsMiddleware } from "../middlewares/validationsMiddleware";

const router: Router = Router();

// Test Route
router.get("/test", getUsers);
router.post(
  "/register",
  emailFormatValidator,
  emailExistsValidator,
  passwordComplexityValidator,
  validationsMiddleware,
  registerUser
);

module.exports = router;
