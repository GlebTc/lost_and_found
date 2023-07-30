const express = require("express");
const cors = require("cors");
const { SERVER_PORT, CLIENT_URL } = require("./constants");
const cookieParser = require("cookie-parser");
const router = require("./routes/index");


// Initialize Express
const app = express();

// Middleware
app.use(cors({ origin: CLIENT_URL, credentials: true }));
app.use(express.json());
app.use(`/api/v1`, router);


// App Start
const appStart = () => {
  try {
    app.listen(SERVER_PORT, () => console.log(`Server is listening on port ${SERVER_PORT}`));
  } catch (error) {
    console.log(error);
  }
};

appStart();
