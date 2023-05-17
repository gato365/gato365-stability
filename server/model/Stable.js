const mongoose = require('mongoose');

const stableSchema = new mongoose.Schema({
  date: { type: Date },
  wakeUp: { type: Date },
  weightAM: { type: Number },
  numberOfDays: { type: Number },
  dayYear: { type: Number },
  goals: { type: String, required: true },
  foodQuality: { type: String, required: true },
  mood: { type: String, required: true },
  MJ: { type: Number },
  alcohol: { type: Number },
  eatingOut: { type: Number },
  mode: { type: String },
  myYFourLife: { type: String },
  myYFourKelley: { type: String },
  myYFourGATO365: { type: String },
  blessings: { type: String },
  notes: { type: String },
  pushups: { type: Number },
  time: { type: String, required: true }
});

module.exports = mongoose.model('Stable', stableSchema);
