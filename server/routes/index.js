

const router = require('express').Router();
const stableRoutes = require('./routes/stableRoutes');


router.use('/stable', stableRoutes);



// router.use((req, res) => res.send('Wrong routlle!'));

module.exports = router;