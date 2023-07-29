import { Router, Request, Response } from 'express';

const router: Router = Router();

// Test Route
router.get('/test', (req: Request, res: Response) => {
    res.send('Hello World!');
    }
);

module.exports = router;