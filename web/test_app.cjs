"use strict";
const assert = require("node:assert/strict");
const { evaluate } = require("./app.js");

const baseline = {
  task_id: "TEST-001",
  target_identifier: "SYNTH-001",
  primary_metric: 10,
  secondary_metric: 5,
  status_descriptor: "NORMAL",
  is_critical_flag: false
};

const normal = evaluate(baseline);
assert.equal(normal.total_alerts, 0);
assert.equal(normal.priority, "ROUTINE");
assert.equal(normal.clinical_use, false);

const flagged = evaluate({ ...baseline, primary_metric: 30, secondary_metric: 13,
  status_descriptor: "DISCORDANT", is_critical_flag: true });
assert.equal(flagged.total_alerts, 3);
assert.equal(flagged.priority, "CRITICAL_STAT_PANIC");
assert.deepEqual(flagged.alerts.map(a => a.rule),
  ["Primary threshold", "Secondary threshold / manual flag", "Descriptor keyword"]);

const threshold = evaluate({ ...baseline, primary_metric: 25, secondary_metric: 12 });
assert.equal(threshold.total_alerts, 0);
const secondary = evaluate({ ...baseline, secondary_metric: 12.001 });
assert.equal(secondary.total_alerts, 1);
assert.equal(secondary.priority, "ELEVATED_RISK");

for (const invalid of [
  { ...baseline, primary_metric: NaN },
  { ...baseline, secondary_metric: Infinity },
  { ...baseline, task_id: "" },
  { ...baseline, target_identifier: "Jane Doe" },
  { ...baseline, status_descriptor: "" },
  { ...baseline, is_critical_flag: "true" }
]) assert.throws(() => evaluate(invalid), Error);

console.log("Browser sandbox rule smoke tests passed");
