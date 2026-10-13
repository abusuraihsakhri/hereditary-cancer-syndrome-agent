"use strict";
(function () {
  const KEYWORDS = ["DISCORDANT", "ANOMALY", "MUTANT", "VIOLATION", "FAIL", "REJECT"];

  function evaluate(input) {
    const taskId = String(input.task_id ?? "").trim();
    const targetId = String(input.target_identifier ?? "").trim();
    const descriptor = String(input.status_descriptor ?? "").trim();
    const primary = input.primary_metric;
    const secondary = input.secondary_metric;

    if (!/^[A-Za-z0-9._-]{1,64}$/.test(taskId) || !/^[A-Za-z0-9._-]{1,64}$/.test(targetId)) {
      throw new Error("Use 1–64 letters, digits, dots, underscores, or hyphens for synthetic IDs.");
    }
    if (typeof primary !== "number" || !Number.isFinite(primary) ||
        typeof secondary !== "number" || !Number.isFinite(secondary)) {
      throw new Error("Both metrics must be finite numbers.");
    }
    if (!descriptor || descriptor.length > 120) {
      throw new Error("Enter a status descriptor of 1–120 characters.");
    }
    if (typeof input.is_critical_flag !== "boolean") {
      throw new Error("Priority flag must be true or false.");
    }

    const alerts = [];
    if (primary > 25) {
      alerts.push({
        rule: "Primary threshold",
        urgency: "ELEVATED_RISK",
        finding: "The primary synthetic metric exceeds the illustrative threshold of 25.",
        explanation: "Demo-only numeric comparison; no clinical inference."
      });
    }
    if (input.is_critical_flag || secondary > 12) {
      alerts.push({
        rule: "Secondary threshold / manual flag",
        urgency: input.is_critical_flag ? "CRITICAL_STAT_PANIC" : "ELEVATED_RISK",
        finding: "The secondary synthetic metric is above 12 or the manual priority flag was selected.",
        explanation: "Demo priority is not a clinical emergency determination."
      });
    }
    if (KEYWORDS.some(word => descriptor.toUpperCase().includes(word))) {
      alerts.push({
        rule: "Descriptor keyword",
        urgency: "ELEVATED_RISK",
        finding: "The text contains a keyword used by the demonstration worker.",
        explanation: "Keyword detection does not establish genetic pathogenicity or diagnostic discordance."
      });
    }
    const priority = input.is_critical_flag && alerts.length
      ? "CRITICAL_STAT_PANIC" : alerts.length ? "ELEVATED_RISK" : "ROUTINE";
    return {
      system: "hereditary-cancer-syndrome-agent",
      mode: "local synthetic-rule demonstration",
      clinical_use: false,
      input: { task_id: taskId, target_identifier: targetId, primary_metric: primary,
        secondary_metric: secondary, status_descriptor: descriptor, is_critical_flag: input.is_critical_flag },
      priority,
      total_alerts: alerts.length,
      alerts,
      disclaimer: "Not NCCN genetic testing criteria; not clinical decision support."
    };
  }

  function setup() {
    const form = document.getElementById("audit-form");
    if (!form) return;
    const resultEl = document.getElementById("result");
    const exportBtn = document.getElementById("export");
    const errorEl = document.getElementById("error");
    const counterEl = document.getElementById("count");
    let latest = null;
    let count = 0;

    function add(tag, text, parent, cls) {
      const el = document.createElement(tag);
      if (cls) el.className = cls;
      el.textContent = text;
      parent.appendChild(el);
      return el;
    }

    form.addEventListener("submit", event => {
      event.preventDefault();
      errorEl.textContent = "";
      try {
        const input = {
          task_id: document.getElementById("task-id").value,
          target_identifier: document.getElementById("target-id").value,
          primary_metric: Number(document.getElementById("primary").value),
          secondary_metric: Number(document.getElementById("secondary").value),
          status_descriptor: document.getElementById("descriptor").value,
          is_critical_flag: document.getElementById("critical").checked
        };
        if (document.getElementById("primary").value.trim() === "" ||
            document.getElementById("secondary").value.trim() === "") {
          throw new Error("Both metrics are required.");
        }
        latest = evaluate(input);
        exportBtn.disabled = false;
        counterEl.textContent = String(++count);
        resultEl.replaceChildren();
        const badge = add("span", latest.priority, resultEl, "status" +
          (latest.total_alerts ? " flagged" : ""));
        badge.setAttribute("aria-label", "Demonstration priority");
        add("p", latest.total_alerts + " rule(s) matched", resultEl);
        const list = add("div", "", resultEl, "output");
        if (!latest.alerts.length) {
          add("div", "No demonstration rules matched. This is not a negative hereditary cancer assessment.", list, "empty");
        }
        latest.alerts.forEach(alert => {
          const item = add("article", "", list, "alert");
          add("strong", alert.rule + " — " + alert.urgency, item);
          add("p", alert.finding, item);
          add("p", alert.explanation, item);
        });
      } catch (error) {
        latest = null;
        exportBtn.disabled = true;
        resultEl.replaceChildren();
        add("div", "Please correct the inputs before evaluating.", resultEl, "empty");
        errorEl.textContent = error.message;
      }
    });

    exportBtn.addEventListener("click", () => {
      if (!latest) return;
      const blob = new Blob([JSON.stringify(latest, null, 2) + "\n"], { type: "application/json" });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = "synthetic-rule-evaluation.json";
      a.click();
      URL.revokeObjectURL(url);
    });
  }

  if (typeof module !== "undefined" && module.exports) module.exports = { evaluate };
  if (typeof document !== "undefined") {
    if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", setup);
    else setup();
  }
})();
