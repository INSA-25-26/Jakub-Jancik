"""Self-contained HTML + JS: wizard UI, sliders, phone/internet-dependent fields."""

PREDICTION_PAGE_HTML = """<!DOCTYPE html>
<html lang="sk">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <title>Predikcia churn — Telco</title>
  <style>
    :root {
      --bg: #0c1222;
      --card: #151d2e;
      --text: #f1f5f9;
      --muted: #94a3b8;
      --accent: #22d3ee;
      --accent-dim: #0891b2;
      --danger: #f87171;
      --border: #2d3a52;
      --step-inactive: #334155;
    }
    * { box-sizing: border-box; }
    body {
      font-family: "Segoe UI", system-ui, sans-serif;
      background: linear-gradient(165deg, #0c1222 0%, #1a1030 50%, #0c1222 100%);
      color: var(--text);
      margin: 0;
      min-height: 100vh;
      padding: 1.25rem;
      line-height: 1.45;
    }
    .wrap { max-width: 44rem; margin: 0 auto; }
    h1 { font-size: 1.45rem; font-weight: 700; margin: 0 0 0.35rem; letter-spacing: -0.02em; }
    .intro-lead {
      color: var(--text);
      font-size: 0.95rem;
      line-height: 1.55;
      margin: 0 0 0.65rem;
      max-width: 42rem;
    }
    .intro-lead strong { color: var(--accent); font-weight: 600; }
    .intro-meta {
      color: var(--muted);
      font-size: 0.82rem;
      line-height: 1.5;
      margin: 0 0 1rem;
      max-width: 42rem;
    }
    .presets {
      display: flex; flex-wrap: wrap; gap: 0.5rem; align-items: center;
      margin-bottom: 1rem; padding: 0.75rem 1rem;
      background: var(--card); border: 1px solid var(--border); border-radius: 10px;
    }
    .presets > span { font-size: 0.8rem; color: var(--muted); margin-right: 0.25rem; }
    .preset-btn {
      font-size: 0.8rem; padding: 0.35rem 0.65rem; border-radius: 6px;
      border: 1px solid var(--border); background: #0f172a; color: var(--accent);
      cursor: pointer; font-family: inherit;
    }
    .preset-btn:hover { border-color: var(--accent-dim); background: #1e293b; }
    .wizard-progress {
      display: flex; gap: 0.35rem; margin-bottom: 1rem;
    }
    .wizard-progress button {
      flex: 1; padding: 0.5rem 0.4rem; border: none; border-radius: 8px;
      background: var(--step-inactive); color: var(--muted); font-size: 0.75rem;
      cursor: pointer; font-family: inherit; transition: background 0.15s, color 0.15s;
    }
    .wizard-progress button.active {
      background: linear-gradient(135deg, var(--accent-dim), var(--accent));
      color: #0f172a; font-weight: 700;
    }
    .wizard-progress button.done { background: #1e3a2f; color: #86efac; }
    form {
      background: var(--card);
      border: 1px solid var(--border);
      border-radius: 14px;
      padding: 1.25rem 1.35rem;
      box-shadow: 0 12px 40px rgba(0,0,0,0.35);
    }
    .step-panel { display: none; animation: fade 0.2s ease; }
    .step-panel.active { display: block; }
    @keyframes fade { from { opacity: 0; transform: translateY(4px); } to { opacity: 1; transform: none; } }
    .step-title { font-size: 1rem; font-weight: 600; color: var(--accent); margin: 0 0 0.75rem; }
    .step-help { font-size: 0.82rem; color: var(--muted); margin: -0.35rem 0 1rem; }
    fieldset {
      border: 1px solid var(--border);
      border-radius: 10px;
      margin: 0 0 1rem;
      padding: 0.65rem 0.85rem 0.85rem;
    }
    legend { padding: 0 0.35rem; color: var(--muted); font-size: 0.75rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.04em; }
    .grid {
      display: grid;
      gap: 0.85rem 1rem;
      grid-template-columns: repeat(auto-fill, minmax(13.5rem, 1fr));
    }
    label { display: flex; flex-direction: column; gap: 0.2rem; font-size: 0.78rem; color: var(--muted); }
    label span.key { color: var(--text); font-weight: 600; font-size: 0.82rem; }
    .hint { font-size: 0.72rem; color: var(--muted); line-height: 1.35; font-weight: 400; }
    label.field-locked { opacity: 0.75; }
    label.field-locked .key::after { content: " (automaticky)"; font-weight: 400; color: var(--accent); font-size: 0.7rem; }
    input, select {
      width: 100%;
      padding: 0.45rem 0.5rem;
      border-radius: 8px;
      border: 1px solid var(--border);
      background: #0f172a;
      color: var(--text);
      font-size: 0.9rem;
    }
    input:disabled, select:disabled { opacity: 0.65; cursor: not-allowed; }
    input:focus, select:focus { outline: 2px solid var(--accent); outline-offset: 1px; }
    .slider-row {
      display: flex; align-items: center; gap: 0.65rem;
    }
    input[type="range"] {
      flex: 1; height: 6px; accent-color: var(--accent);
    }
    .slider-row input[type="number"] {
      width: 5rem; flex: none; text-align: right;
    }
    .slider-val {
      min-width: 2.75rem; text-align: right; font-size: 0.85rem; font-weight: 600; color: var(--accent);
    }
    .wizard-actions {
      display: flex; flex-wrap: wrap; gap: 0.65rem; align-items: center; margin-top: 0.25rem; padding-top: 0.75rem;
      border-top: 1px solid var(--border);
    }
    .wizard-actions button {
      padding: 0.55rem 1.1rem; border-radius: 8px; font-weight: 600; font-size: 0.95rem;
      cursor: pointer; font-family: inherit; border: none;
    }
    #btn-prev { background: transparent; color: var(--muted); border: 1px solid var(--border); }
    #btn-prev:hover { color: var(--text); border-color: var(--muted); }
    #btn-next { background: #334155; color: var(--text); }
    #btn-next:hover { background: #475569; }
    #submit-btn {
      background: linear-gradient(135deg, var(--accent-dim), var(--accent));
      color: #0f172a;
    }
    #submit-btn:disabled { opacity: 0.45; cursor: not-allowed; }
    .hidden { display: none !important; }
    #result {
      margin-top: 1.25rem;
      padding: 1rem 1.25rem;
      border-radius: 12px;
      border: 1px solid var(--border);
      background: var(--card);
      display: none;
    }
    #result.visible { display: block; }
    #result.err { border-color: var(--danger); }
    #result.ok { border-color: #22c55e88; }
    .result-summary { margin: 0; }
    .result-row {
      display: grid;
      grid-template-columns: 1fr auto;
      gap: 0.5rem 1rem;
      align-items: baseline;
      padding: 0.65rem 0;
      border-bottom: 1px solid var(--border);
    }
    .result-row:last-of-type { border-bottom: none; padding-bottom: 0; }
    .result-label {
      font-size: 0.88rem;
      color: var(--muted);
      margin: 0;
    }
    .result-value {
      margin: 0;
      font-size: 1rem;
      font-weight: 600;
      color: var(--text);
      text-align: right;
    }
    .result-value.result-pct {
      font-size: 1.65rem;
      font-weight: 700;
      color: var(--accent);
    }
    .result-value.result-raw {
      font-size: 0.9rem;
      font-weight: 500;
      font-variant-numeric: tabular-nums;
      color: #cbd5e1;
    }
    footer { margin-top: 1.5rem; font-size: 0.78rem; color: var(--muted); }
    footer a { color: var(--accent); }
  </style>
</head>
<body>
  <div class="wrap">
    <h1>Predikcia odchodu zákazníka (churn)</h1>
    <p class="intro-lead">
      Táto služba <strong>odhaduje pravdepodobnosť, že zákazník telekomunikačného operátora ukončí odber</strong>
      (tzv. <em>churn</em> — odchod). Vychádza z natrénovaného modelu a verejného datasetu Telco Customer Churn:
      podľa zadaného profilu (demografia, zmluva, služby, poplatky) vypočíta, s akou pravdepodobnosťou by šlo o zákazníka,
      ktorý by podľa vzorca modelu „odišiel“. Ide o <strong>štatistickú predikciu</strong>, nie právne záväzné rozhodnutie.
    </p>

    <div class="wizard-progress" role="tablist">
      <button type="button" data-step-jump="1" class="active">1 · O zákazníkovi</button>
      <button type="button" data-step-jump="2">2 · Služby</button>
      <button type="button" data-step-jump="3">3 · Platba</button>
    </div>

    <form id="churn-form">
      <div class="step-panel active" data-step="1">
        <h2 class="step-title">Krok 1 — O zákazníkovi</h2>
        <p class="step-help">Demografia a ako dlho je u operátora. Slider pre dobu je v <strong>mesiacoch</strong> (v datasete 0–72).</p>
        <div class="grid">
          <label><span class="key">Pohlavie</span>
            <span class="hint">Hodnoty v dátach: Female / Male</span>
            <select name="gender" required>
              <option value="Female">Female</option>
              <option value="Male" selected>Male</option>
            </select>
          </label>
          <label><span class="key">Senior citizen</span>
            <span class="hint">1 = zákazník nad 65 r. (v CSV 0/1)</span>
            <select name="SeniorCitizen" required>
              <option value="0" selected>Nie (0)</option>
              <option value="1">Áno (1)</option>
            </select>
          </label>
          <label><span class="key">Má partnera / partnerku?</span>
            <span class="hint">Yes / No</span>
            <select name="Partner" required>
              <option value="Yes">Yes</option>
              <option value="No" selected>No</option>
            </select>
          </label>
          <label><span class="key">Nezaopatrené deti v domácnosti?</span>
            <span class="hint">Yes / No</span>
            <select name="Dependents" required>
              <option value="Yes">Yes</option>
              <option value="No" selected>No</option>
            </select>
          </label>
          <label style="grid-column: 1 / -1;">
            <span class="key">Doba u operátora (tenure)</span>
            <span class="hint">Jednotka: <strong>mesiace</strong> (0 = nový zákazník, max. v dátach 72).</span>
            <div class="slider-row">
              <input type="range" id="tenure-range" min="0" max="72" value="12" step="1" aria-label="Doba v mesiacoch"/>
              <span class="slider-val" id="tenure-val">12</span>
              <span style="color:var(--muted);font-size:0.8rem;">mes.</span>
              <input name="tenure" id="tenure-num" type="number" min="0" max="72" step="1" value="12" required aria-label="Doba presná hodnota"/>
            </div>
          </label>
        </div>
      </div>

      <div class="step-panel" data-step="2">
        <h2 class="step-title">Krok 2 — Služby</h2>
        <fieldset>
          <legend>Telefón</legend>
          <div class="grid">
            <label><span class="key">Phone service</span>
              <span class="hint">Má hlasovú pevnú / mobilnú linku u operátora?</span>
              <select name="PhoneService" id="PhoneService" required>
                <option value="Yes" selected>Yes</option>
                <option value="No">No</option>
              </select>
            </label>
            <label id="ml-label"><span class="key">Multiple lines</span>
              <span class="hint">Iba ak má telefón: Yes / No. Bez telefónu vždy „No phone service“.</span>
              <select name="MultipleLines" id="MultipleLines" required>
                <option value="Yes">Yes</option>
                <option value="No" selected>No</option>
                <option value="No phone service">No phone service</option>
              </select>
            </label>
          </div>
        </fieldset>
        <fieldset>
          <legend>Internet a doplnky</legend>
          <div class="grid">
            <label><span class="key">Internet service</span>
              <span class="hint">DSL / Fiber optic / No</span>
              <select name="InternetService" id="InternetService" required>
                <option value="DSL">DSL</option>
                <option value="Fiber optic" selected>Fiber optic</option>
                <option value="No">No</option>
              </select>
            </label>
            <label class="inet-dep"><span class="key">Online security</span>
              <select name="OnlineSecurity" class="inet-addon" required>
                <option value="Yes">Yes</option>
                <option value="No" selected>No</option>
                <option value="No internet service">No internet service</option>
              </select>
            </label>
            <label class="inet-dep"><span class="key">Online backup</span>
              <select name="OnlineBackup" class="inet-addon" required>
                <option value="Yes">Yes</option>
                <option value="No" selected>No</option>
                <option value="No internet service">No internet service</option>
              </select>
            </label>
            <label class="inet-dep"><span class="key">Device protection</span>
              <select name="DeviceProtection" class="inet-addon" required>
                <option value="Yes">Yes</option>
                <option value="No" selected>No</option>
                <option value="No internet service">No internet service</option>
              </select>
            </label>
            <label class="inet-dep"><span class="key">Tech support</span>
              <select name="TechSupport" class="inet-addon" required>
                <option value="Yes">Yes</option>
                <option value="No" selected>No</option>
                <option value="No internet service">No internet service</option>
              </select>
            </label>
            <label class="inet-dep"><span class="key">Streaming TV</span>
              <select name="StreamingTV" class="inet-addon" required>
                <option value="Yes">Yes</option>
                <option value="No" selected>No</option>
                <option value="No internet service">No internet service</option>
              </select>
            </label>
            <label class="inet-dep"><span class="key">Streaming movies</span>
              <select name="StreamingMovies" class="inet-addon" required>
                <option value="Yes">Yes</option>
                <option value="No" selected>No</option>
                <option value="No internet service">No internet service</option>
              </select>
            </label>
          </div>
        </fieldset>
      </div>

      <div class="step-panel" data-step="3">
        <h2 class="step-title">Krok 3 — Zmluva a poplatky</h2>
        <div class="grid">
          <label><span class="key">Contract</span>
            <span class="hint">Typ viazania</span>
            <select name="Contract" required>
              <option value="Month-to-month" selected>Month-to-month</option>
              <option value="One year">One year</option>
              <option value="Two year">Two year</option>
            </select>
          </label>
          <label><span class="key">Paperless billing</span>
            <select name="PaperlessBilling" required>
              <option value="Yes">Yes</option>
              <option value="No" selected>No</option>
            </select>
          </label>
          <label><span class="key">Payment method</span>
            <select name="PaymentMethod" required>
              <option value="Electronic check" selected>Electronic check</option>
              <option value="Mailed check">Mailed check</option>
              <option value="Bank transfer (automatic)">Bank transfer (automatic)</option>
              <option value="Credit card (automatic)">Credit card (automatic)</option>
            </select>
          </label>
          <label style="grid-column: 1 / -1;">
            <span class="key">Monthly charges ($)</span>
            <span class="hint">Mesačný poplatok (v dátach cca 18–120).</span>
            <div class="slider-row">
              <input type="range" id="monthly-range" min="18" max="120" value="55" step="1"/>
              <span class="slider-val" id="monthly-val">55</span>
              <input name="MonthlyCharges" id="monthly-num" type="number" min="0" step="0.01" value="55" required/>
            </div>
          </label>
          <label style="grid-column: 1 / -1;">
            <span class="key">Total charges ($)</span>
            <span class="hint">Kumulatívne účtované (v dátach zvyčajne 0–8000+).</span>
            <div class="slider-row">
              <input type="range" id="total-range" min="0" max="8000" value="650" step="10"/>
              <span class="slider-val" id="total-val">650</span>
              <input name="TotalCharges" id="total-num" type="number" min="0" step="0.01" value="650" required/>
            </div>
          </label>
        </div>
      </div>

      <div class="wizard-actions">
        <button type="button" id="btn-prev" class="hidden">← Späť</button>
        <button type="button" id="btn-next">Ďalej →</button>
        <button type="submit" id="submit-btn" class="hidden">Vypočítať predikciu</button>
      </div>
    </form>

    <div id="result" role="status" aria-live="polite"></div>

    <footer>
      <a href="/docs">OpenAPI / Swagger</a> ·
      <a href="/redoc">ReDoc</a> ·
      <a href="/health">Health</a> ·
      <a href="/grafana/">Grafana</a> ·
      <a href="/prometheus/">Prometheus</a>
    </footer>
  </div>

  <script>
(function () {
  const form = document.getElementById("churn-form");
  const result = document.getElementById("result");
  const btnSubmit = document.getElementById("submit-btn");
  const btnNext = document.getElementById("btn-next");
  const btnPrev = document.getElementById("btn-prev");
  const panels = form.querySelectorAll(".step-panel");
  const progressBtns = document.querySelectorAll("[data-step-jump]");
  let step = 1;
  const lastStep = 3;

  const tenureR = document.getElementById("tenure-range");
  const tenureN = document.getElementById("tenure-num");
  const tenureVal = document.getElementById("tenure-val");
  const monthlyR = document.getElementById("monthly-range");
  const monthlyN = document.getElementById("monthly-num");
  const monthlyVal = document.getElementById("monthly-val");
  const totalR = document.getElementById("total-range");
  const totalN = document.getElementById("total-num");
  const totalVal = document.getElementById("total-val");

  const phoneSel = document.getElementById("PhoneService");
  const mlSel = document.getElementById("MultipleLines");
  const mlLabel = document.getElementById("ml-label");
  const inetSel = document.getElementById("InternetService");
  const inetAddons = form.querySelectorAll(".inet-addon");

  function syncTenure() {
    var v = Math.max(0, Math.min(72, parseInt(tenureN.value, 10) || 0));
    tenureN.value = String(v);
    tenureR.value = String(v);
    tenureVal.textContent = String(v);
  }
  function syncMonthly() {
    var x = parseFloat(monthlyN.value);
    if (isNaN(x)) x = 55;
    x = Math.max(0, Math.min(120, x));
    monthlyN.value = String(Math.round(x * 100) / 100);
    var ri = Math.max(18, Math.min(120, Math.round(x)));
    monthlyR.value = String(ri);
    monthlyVal.textContent = monthlyN.value;
  }
  function syncTotal() {
    var x = parseFloat(totalN.value);
    if (isNaN(x)) x = 0;
    x = Math.max(0, Math.min(20000, x));
    totalN.value = String(Math.round(x * 100) / 100);
    var ri = Math.max(0, Math.min(8000, Math.round(x / 10) * 10));
    totalR.value = String(ri);
    totalVal.textContent = totalN.value;
  }

  tenureR.addEventListener("input", function () {
    tenureN.value = tenureR.value;
    tenureVal.textContent = tenureR.value;
  });
  tenureN.addEventListener("input", syncTenure);
  monthlyR.addEventListener("input", function () {
    monthlyN.value = monthlyR.value;
    monthlyVal.textContent = monthlyN.value;
  });
  monthlyN.addEventListener("input", syncMonthly);
  totalR.addEventListener("input", function () {
    totalN.value = totalR.value;
    totalVal.textContent = totalN.value;
  });
  totalN.addEventListener("input", syncTotal);

  function setOptionDisabled(select, value, disabled) {
    var opt = Array.prototype.find.call(select.options, function (o) { return o.value === value; });
    if (opt) opt.disabled = disabled;
  }

  function syncPhoneService() {
    var hasPhone = phoneSel.value === "Yes";
    if (!hasPhone) {
      mlSel.value = "No phone service";
      mlSel.disabled = true;
      mlLabel.classList.add("field-locked");
      setOptionDisabled(mlSel, "Yes", true);
      setOptionDisabled(mlSel, "No", true);
      setOptionDisabled(mlSel, "No phone service", false);
    } else {
      mlSel.disabled = false;
      mlLabel.classList.remove("field-locked");
      setOptionDisabled(mlSel, "Yes", false);
      setOptionDisabled(mlSel, "No", false);
      setOptionDisabled(mlSel, "No phone service", true);
      if (mlSel.value === "No phone service") mlSel.value = "No";
    }
  }

  function syncInternetService() {
    var noNet = inetSel.value === "No";
    inetAddons.forEach(function (sel) {
      var lab = sel.closest("label");
      if (noNet) {
        sel.value = "No internet service";
        sel.disabled = true;
        if (lab) lab.classList.add("field-locked");
        setOptionDisabled(sel, "Yes", true);
        setOptionDisabled(sel, "No", true);
        setOptionDisabled(sel, "No internet service", false);
      } else {
        sel.disabled = false;
        if (lab) lab.classList.remove("field-locked");
        setOptionDisabled(sel, "Yes", false);
        setOptionDisabled(sel, "No", false);
        setOptionDisabled(sel, "No internet service", true);
        if (sel.value === "No internet service") sel.value = "No";
      }
    });
  }

  phoneSel.addEventListener("change", syncPhoneService);
  inetSel.addEventListener("change", syncInternetService);

  function enableAllForSubmit() {
    form.querySelectorAll("select:disabled, input:disabled").forEach(function (el) {
      if (el.name && el.name !== "") {
        el.dataset.tmpDisabled = "1";
        el.disabled = false;
      }
    });
  }
  function restoreDisabledAfterSubmit() {
    form.querySelectorAll("[data-tmp-disabled]").forEach(function (el) {
      el.disabled = true;
      delete el.dataset.tmpDisabled;
    });
  }

  function showStep(n) {
    step = n;
    panels.forEach(function (p) {
      p.classList.toggle("active", parseInt(p.getAttribute("data-step"), 10) === n);
    });
    progressBtns.forEach(function (b, i) {
      var sn = i + 1;
      b.classList.remove("active", "done");
      if (sn === n) b.classList.add("active");
      else if (sn < n) b.classList.add("done");
    });
    btnPrev.classList.toggle("hidden", n === 1);
    btnNext.classList.toggle("hidden", n === lastStep);
    btnSubmit.classList.toggle("hidden", n !== lastStep);
    if (n === 2) {
      syncPhoneService();
      syncInternetService();
    }
  }

  btnNext.addEventListener("click", function () {
    if (step < lastStep) showStep(step + 1);
  });
  btnPrev.addEventListener("click", function () {
    if (step > 1) showStep(step - 1);
  });
  progressBtns.forEach(function (b) {
    b.addEventListener("click", function () {
      showStep(parseInt(b.getAttribute("data-step-jump"), 10));
    });
  });

  var PRESETS = {
    fiber_monthly: {
      gender: "Male", SeniorCitizen: "0", Partner: "No", Dependents: "No", tenure: "8",
      PhoneService: "Yes", MultipleLines: "No", InternetService: "Fiber optic",
      OnlineSecurity: "No", OnlineBackup: "No", DeviceProtection: "No", TechSupport: "No",
      StreamingTV: "No", StreamingMovies: "No",
      Contract: "Month-to-month", PaperlessBilling: "Yes", PaymentMethod: "Electronic check",
      MonthlyCharges: "85", TotalCharges: "720"
    },
    dsl_loyal: {
      gender: "Female", SeniorCitizen: "0", Partner: "Yes", Dependents: "Yes", tenure: "48",
      PhoneService: "Yes", MultipleLines: "Yes", InternetService: "DSL",
      OnlineSecurity: "Yes", OnlineBackup: "Yes", DeviceProtection: "No", TechSupport: "Yes",
      StreamingTV: "No", StreamingMovies: "No",
      Contract: "Two year", PaperlessBilling: "No", PaymentMethod: "Credit card (automatic)",
      MonthlyCharges: "65", TotalCharges: "3200"
    },
    no_net_phone: {
      gender: "Male", SeniorCitizen: "0", Partner: "No", Dependents: "No", tenure: "3",
      PhoneService: "Yes", MultipleLines: "No", InternetService: "No",
      OnlineSecurity: "No internet service", OnlineBackup: "No internet service",
      DeviceProtection: "No internet service",
      TechSupport: "No internet service", StreamingTV: "No internet service", StreamingMovies: "No internet service",
      Contract: "Month-to-month", PaperlessBilling: "Yes", PaymentMethod: "Mailed check",
      MonthlyCharges: "25", TotalCharges: "75"
    }
  };

  document.querySelectorAll(".preset-btn").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var key = btn.getAttribute("data-preset");
      var p = PRESETS[key];
      if (!p) return;
      Object.keys(p).forEach(function (name) {
        var el = form.elements.namedItem(name);
        if (el && "value" in el) el.value = p[name];
      });
      syncTenure();
      syncMonthly();
      syncTotal();
      syncPhoneService();
      syncInternetService();
      showStep(1);
      result.className = "";
      result.innerHTML = "";
    });
  });

  function payloadFromForm(fd) {
    return {
      gender: fd.get("gender"),
      SeniorCitizen: parseInt(fd.get("SeniorCitizen"), 10),
      Partner: fd.get("Partner"),
      Dependents: fd.get("Dependents"),
      tenure: parseInt(fd.get("tenure"), 10),
      PhoneService: fd.get("PhoneService"),
      MultipleLines: fd.get("MultipleLines"),
      InternetService: fd.get("InternetService"),
      OnlineSecurity: fd.get("OnlineSecurity"),
      OnlineBackup: fd.get("OnlineBackup"),
      DeviceProtection: fd.get("DeviceProtection"),
      TechSupport: fd.get("TechSupport"),
      StreamingTV: fd.get("StreamingTV"),
      StreamingMovies: fd.get("StreamingMovies"),
      Contract: fd.get("Contract"),
      PaperlessBilling: fd.get("PaperlessBilling"),
      PaymentMethod: fd.get("PaymentMethod"),
      MonthlyCharges: parseFloat(fd.get("MonthlyCharges")),
      TotalCharges: parseFloat(fd.get("TotalCharges")),
    };
  }

  form.addEventListener("submit", async function (e) {
    e.preventDefault();
    enableAllForSubmit();
    result.className = "visible";
    result.classList.remove("ok", "err");
    result.textContent = "Počítam…";
    btnSubmit.disabled = true;
    try {
      var body = payloadFromForm(new FormData(form));
      var res = await fetch("/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json", "Accept": "application/json" },
        body: JSON.stringify(body),
      });
      var data = await res.json().catch(function () { return {}; });
      if (!res.ok) {
        result.classList.add("err");
        var msg = data.detail != null
          ? (typeof data.detail === "string" ? data.detail : JSON.stringify(data.detail))
          : res.statusText;
        result.innerHTML = "<strong>Chyba</strong><p>" + escapeHtml(msg) + "</p>";
        return;
      }
      result.classList.add("ok");
      var p = Number(data.churn_probability);
      var pctSk = (p * 100).toLocaleString("sk-SK", {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
      });
      var rawSk = p.toLocaleString("sk-SK", {
        minimumFractionDigits: 6,
        maximumFractionDigits: 8
      });
      var predOdchod = data.label === "Yes"
        ? "Áno"
        : data.label === "No" ? "Nie" : escapeHtml(String(data.label));
      result.innerHTML =
        '<div class="result-summary">' +
        '<div class="result-row">' +
        '<p class="result-label">Pravdepodobnosť odchodu</p>' +
        '<p class="result-value result-pct">' + escapeHtml(pctSk) + " %</p>" +
        "</div>" +
        '<div class="result-row">' +
        '<p class="result-label">Predpokladaný odchod</p>' +
        '<p class="result-value">' + predOdchod + "</p>" +
        "</div>" +
        '<div class="result-row">' +
        '<p class="result-label">Vypočítaná pravdepodobnosť</p>' +
        '<p class="result-value result-raw">' + escapeHtml(rawSk) + "</p>" +
        "</div>" +
        "</div>";
    } catch (err) {
      result.classList.add("err");
      result.innerHTML = "<strong>Chyba siete</strong><p>" + escapeHtml(String(err)) + "</p>";
    } finally {
      restoreDisabledAfterSubmit();
      btnSubmit.disabled = false;
      syncPhoneService();
      syncInternetService();
    }
  });

  function escapeHtml(s) {
    return String(s)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  syncTenure();
  syncMonthly();
  syncTotal();
  syncPhoneService();
  syncInternetService();
  showStep(1);
})();
  </script>
</body>
</html>
"""
