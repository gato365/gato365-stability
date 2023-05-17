const express = require('express');
const db = require('./config/connection');
const stableRoutes = require('./routes/stableRoutes');
const path = require('path');
const PORT = process.env.PORT || 3001;
const app = express();





 
// Express middleware
app.use(express.urlencoded({ extended: true }));
app.use(express.json());
app.use(stableRoutes);

// Serve up static assets
app.use(express.static(path.join(__dirname, '..', 'public')))
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, '..', 'public', 'index.html'));
});

// Default response for any other request (Not Found)
app.use((err, req, res, next) => {
    console.error(err.stack);
    res.status(500).send('Something went wrong');
});

db.once('open', () => {
    app.listen(PORT, () => {
        console.log(`API server running on port ${PORT}!`);
        console.log(`Here is the link http://localhost:${PORT}`)
    });

});