const express = require('express');
const db = require('./config/connection');
const stableRoutes = require('./routes/stableRoutes');

const PORT = process.env.PORT || 3001;
const app = express();





// Express middleware
app.use(express.urlencoded({ extended: true }));
app.use(express.json());
app.use(stableRoutes);

db.once('open', () => {
    app.listen(PORT, () => {
        console.log(`API server running on port ${PORT}!`);
        console.log(`Here is the link http://localhost:${PORT}`)
    });

});