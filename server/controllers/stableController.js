const Stable = require('../models/stable');



// @desc   Create a new stable entry
// @route  POST /api/v1/stable
// @access Public

const stableController = {
    create: async (req, res) => {
        try {
            // Create a new Stable instance based on the request body
            const newStable = new Stable(req.body);

            // Save the new stable entry to the database
            await newStable.save();

            // Send a success response with the new stable entry
            res.status(201).json({ success: true, data: newStable });
        } catch (error) {
            // If there was an error, send an error response
            res.status(500).json({ success: false, error: error.message });
        }
    },

    // @desc   Get all stable entries
    // @route  GET /api/v1/stable
    // @access Public

    getChartData: async (req, res) => {
        try {
            // Find all stable entries in the database
            const stableEntries = await Stable.find();

            // Create an array of objects representing the data for the chart
            const chartData = stableEntries.map(entry => ({
                date: entry.date,
                weightAM: entry.weightAM,
                goals: entry.goals,
                foodQuality: entry.foodQuality,
                mood: entry.mood
            }));

            // Send the chart data as JSON
            res.status(200).json({ success: true, data: chartData });
        } catch (error) {
            // If there was an error, send an error response
            res.status(500).json({ success: false, error: error.message });
        }
    }
};

module.exports = stableController;
