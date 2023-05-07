const express = require('express');
const stableController = require('../controllers/stableController');

const router = express.Router();

// Create a new stable entry
router.post('/', stableController.create);

// Get chart data for stable entries with optional filters
router.get('/', stableController.getChartData);

module.exports = router;