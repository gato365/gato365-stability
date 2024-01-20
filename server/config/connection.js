// This file will be used to connect to the database
const { connect, connection } = require('mongoose');
require('dotenv').config();
const password = process.env.MONGODB_PASSWORD;


// After you create your Heroku application, visit https://dashboard.heroku.com/apps/ select the application name and add your Atlas connection string as a Config Var
// Node will look for this environment variable and if it exists, it will use it. Otherwise, it will assume that you are running this application locally



// const connectionString = process.env.MONGODB_URI || 'mongodb://127.0.0.1:27017/stabilityDB';
// connect(connectionString, {
//   useNewUrlParser: true,
//   useUnifiedTopology: true,
// });


const connectionString = `mongodb+srv://immanuelwilliams:${password}@cluster0.rjzoaxj.mongodb.net/?retryWrites=true&w=majority`;
connect(connectionString, {
  useNewUrlParser: true,
  useUnifiedTopology: true,
});









// This will log any errors connected to the database
module.exports = connection;