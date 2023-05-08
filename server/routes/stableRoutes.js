const express = require('express');
const stableController = require('../controllers/stableController');

const router = express.Router();

// Create a new stable entry
router.post('/submit-data', stableController.create);

// Get chart data for stable entries with optional filters
router.get('/chart-data', stableController.getChartData);

module.exports = router;