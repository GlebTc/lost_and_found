import { Router, Request, Response } from 'express';
import { getUsers, registerUser } from "../controllers/userControllers"

const router: Router = Router();

// Test Route
router.get('/test', getUsers);
router.post('/register', registerUser)

module.exports = router;