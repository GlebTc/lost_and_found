const express = require("express")
const { PORT } = require("./constants")
const app = express()


// App Start
const appStart = () => {
    try {
      app.listen(PORT, () => console.log(`Server is listening on port ${PORT}`));
    } catch (error) {
      console.log(error);
    }
  };
  
  appStart();