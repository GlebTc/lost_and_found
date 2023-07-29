const express = require("express")

const app = express()
const PORT = 8000

// App Start
const appStart = () => {
    try {
      app.listen(PORT, () => console.log(`Server is listening on port ${PORT}`));
    } catch (error) {
      console.log(error);
    }
  };
  
  appStart();