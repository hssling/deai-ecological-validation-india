const LMS_Z = -1.6448536269514722;
const state = {
  lmsRows: [],
};

const form = document.getElementById("patientForm");
const summaryStrip = document.getElementById("summaryStrip");
const spirometryCards = document.getElementById("spirometryCards");
const respInterpretation = document.getElementById("respInterpretation");
const ageingActions = document.getElementById("ageingActions");
const printReport = document.getElementById("printReport");

init();

async function init() {
  try {
    const response = await fetch("assets/lasi_gamlss_lms_table.csv");
    if (!response.ok) {
      throw new Error(`Could not load LMS table: ${response.status}`);
    }
    const csv = await response.text();
    state.lmsRows = parseCsv(csv).map((row) => ({
      param: normalizeParameter(row.param),
      sex: normalizeSex(row.sex),
      refht: Number(row.refht),
      lnht_coef: row.lnht_coef === "NA" || row.lnht_coef === "" ? null : Number(row.lnht_coef),
      age: Number(row.age),
      L: Number(row.L),
      M: Number(row.M),
      S: Number(row.S),
    }));
    updateAssessment();
  } catch (error) {
    renderError(error.message);
  }
}

form.addEventListener("submit", (event) => {
  event.preventDefault();
  updateAssessment();
});

form.addEventListener("input", () => {
  updateAssessment();
});

form.addEventListener("reset", () => {
  window.setTimeout(updateAssessment, 0);
});

printReport.addEventListener("click", () => {
  window.print();
});

function updateAssessment() {
  if (!state.lmsRows.length) return;

  try {
    const patient = readPatient();
    const respiratory = scoreSpirometry(patient);
    const actions = buildAgeingActions(patient, respiratory);
    renderSummary(patient, respiratory, actions);
    renderSpirometryCards(respiratory);
    renderRespiratoryInterpretation(patient, respiratory);
    renderAgeingActions(actions);
  } catch (error) {
    renderError(error.message);
  }
}

function readPatient() {
  const age = numberFrom("age");
  const height = numberFrom("height");
  const weight = numberFrom("weight");
  const fev1 = numberFrom("fev1");
  const fvc = numberFrom("fvc");
  if (age < 45 || age > 90) {
    throw new Error("The LASI national reference equations are tabulated for ages 45-90 years.");
  }
  if (fvc <= 0 || fev1 <= 0 || fev1 > fvc * 1.15) {
    throw new Error("Check spirometry values. FEV1 and FVC must be positive and physiologically plausible.");
  }
  const bmi = height > 0 && weight > 0 ? weight / Math.pow(height / 100, 2) : null;
  return {
    sex: normalizeSex(document.getElementById("sex").value),
    age,
    height,
    weight,
    bmi,
    fev1,
    fvc,
    tobacco: document.getElementById("tobacco").value,
    respSymptoms: document.getElementById("respSymptoms").value,
    sbp: numberFrom("sbp", true),
    dbp: numberFrom("dbp", true),
    hba1c: numberFrom("hba1c", true),
    falls: numberFrom("falls", true),
    frailtySignal: document.getElementById("frailtySignal").value,
    functionSignal: document.getElementById("functionSignal").value,
    cognitionSignal: document.getElementById("cognitionSignal").value,
    moodSignal: document.getElementById("moodSignal").value,
  };
}

function scoreSpirometry(patient) {
  const fev1 = scoreObserved(patient.fev1, patient.sex, patient.age, patient.height, "fev1");
  const fvc = scoreObserved(patient.fvc, patient.sex, patient.age, patient.height, "fvc");
  const ratioPercent = (patient.fev1 / patient.fvc) * 100;
  const ratio = scoreObserved(ratioPercent, patient.sex, patient.age, patient.height, "fev1fvc");
  const obstructionLln = ratio.observed < ratio.lln;
  const preservedRatio = !obstructionLln;
  const lowFev1Fixed = fev1.percentPredicted < 80;
  const lowFvcFixed = fvc.percentPredicted < 80;
  const lowFev1Lln = fev1.observed < fev1.lln;
  const lowFvcLln = fvc.observed < fvc.lln;

  return {
    fev1,
    fvc,
    ratio,
    classification: {
      obstructionLln,
      preservedRatio,
      prismFixed: preservedRatio && lowFev1Fixed,
      prismLln: preservedRatio && lowFev1Lln,
      rspFixed: preservedRatio && lowFvcFixed,
      rspLln: preservedRatio && lowFvcLln,
    },
  };
}

function predict(sex, age, height, parameter) {
  const param = normalizeParameter(parameter);
  const row = interpolateLms(sex, age, param);
  let median = row.M;
  const heightExponent = param === "fev1fvc" ? null : row.lnht_coef;
  if (param !== "fev1fvc") {
    median = median * Math.pow(height / row.refht, heightExponent);
  }
  const lln = bccgQuantile(median, row.L, row.S, LMS_Z);
  return {
    median,
    lln,
    L: row.L,
    S: row.S,
    refHeight: row.refht,
    heightExponent,
  };
}

function scoreObserved(observed, sex, age, height, parameter) {
  const param = normalizeParameter(parameter);
  const observedValue = param === "fev1fvc" && observed <= 1.5 ? observed * 100 : observed;
  const prediction = predict(sex, age, height, param);
  const z = bccgZ(observedValue, prediction.median, prediction.L, prediction.S);
  return {
    observed: observedValue,
    predicted: prediction.median,
    lln: prediction.lln,
    z,
    percentPredicted: (observedValue / prediction.median) * 100,
  };
}

function interpolateLms(sex, age, parameter) {
  const rows = state.lmsRows
    .filter((row) => row.sex === normalizeSex(sex) && row.param === normalizeParameter(parameter))
    .sort((a, b) => a.age - b.age);
  if (!rows.length) {
    throw new Error("No LASI LMS reference rows found for the selected inputs.");
  }
  const minAge = rows[0].age;
  const maxAge = rows[rows.length - 1].age;
  if (age < minAge || age > maxAge) {
    throw new Error(`Age ${age} is outside the LASI reference range ${minAge}-${maxAge} years.`);
  }
  const exact = rows.find((row) => row.age === age);
  if (exact) return { ...exact };

  const lower = rows.filter((row) => row.age < age).pop();
  const upper = rows.find((row) => row.age > age);
  const weight = (age - lower.age) / (upper.age - lower.age);
  return {
    ...lower,
    L: lower.L + (upper.L - lower.L) * weight,
    M: lower.M + (upper.M - lower.M) * weight,
    S: lower.S + (upper.S - lower.S) * weight,
  };
}

function bccgZ(observed, median, L, S) {
  if (observed <= 0) {
    throw new Error("Observed spirometry value must be positive.");
  }
  if (Math.abs(L) < 1e-12) {
    return Math.log(observed / median) / S;
  }
  return (Math.pow(observed / median, L) - 1) / (L * S);
}

function bccgQuantile(median, L, S, z) {
  if (Math.abs(L) < 1e-12) {
    return median * Math.exp(S * z);
  }
  const base = 1 + L * S * z;
  if (base <= 0) {
    throw new Error("Invalid LMS quantile base. Check reference values.");
  }
  return median * Math.pow(base, 1 / L);
}

function buildAgeingActions(patient, respiratory) {
  const actions = [];
  const c = respiratory.classification;

  if (c.obstructionLln) {
    actions.push(action("Respiratory", "High", "FEV1/FVC is below the LASI lower limit of normal. Review test quality, bronchodilator status, symptoms, exposure history, prior TB/asthma/COPD, oxygen saturation if relevant, and consider guideline-based referral."));
  } else if (c.prismLln || c.rspLln || c.prismFixed || c.rspFixed) {
    actions.push(action("Respiratory", "Moderate", "Preserved-ratio low lung function is flagged. Confirm spirometry quality, repeat if needed, assess dyspnoea and exercise capacity, and look for cardiac, metabolic, anaemia, obesity, prior TB, and interstitial or neuromuscular contributors."));
  } else {
    actions.push(action("Respiratory", "Routine", "Spirometry is not below LASI LLN thresholds. Interpret with symptoms, exposure history, and test quality rather than the equation output alone."));
  }

  if (patient.respSymptoms === "yes") {
    actions.push(action("Symptoms", "High", "Respiratory symptoms are present. Normal reference classification should not stop clinical work-up when symptoms, low oxygen saturation, abnormal examination, or imaging concerns are present."));
  }

  if (patient.tobacco === "current") {
    actions.push(action("Tobacco", "High", "Offer brief cessation intervention, pharmacotherapy where appropriate, and follow-up. Document second-hand exposure and household air pollution separately."));
  } else if (patient.tobacco === "former" || patient.tobacco === "biomass") {
    actions.push(action("Exposure", "Moderate", "Document pack-years or biomass/occupational exposure intensity, check vaccination status, and consider exposure reduction counselling."));
  }

  if (patient.bmi !== null && patient.bmi < 18.5) {
    actions.push(action("Nutrition", "Moderate", "BMI is in the underweight range. Screen for malnutrition, oral/dental problems, food insecurity, chronic infection, malignancy symptoms, and sarcopenia risk."));
  } else if (patient.bmi !== null && patient.bmi >= 30) {
    actions.push(action("Metabolic", "Moderate", "BMI is in the obesity range. Review cardiometabolic risk, sleep apnoea symptoms, mobility limitations, and a realistic nutrition/activity plan."));
  }

  if (patient.sbp >= 140 || patient.dbp >= 90) {
    actions.push(action("Blood pressure", "Moderate", "BP is above common clinic thresholds. Confirm with repeat standardized measurements or home readings, review treatment adherence, renal risk, and cardiovascular risk."));
  }

  if (patient.hba1c >= 6.5) {
    actions.push(action("Glycaemia", "Moderate", "HbA1c is in the diabetes range if confirmed by accepted diagnostic standards. Review symptoms, medications, kidney function, eye/foot care, and individualised targets."));
  } else if (patient.hba1c >= 5.7) {
    actions.push(action("Glycaemia", "Routine", "HbA1c is in a higher-risk range. Discuss diet quality, physical activity, sleep, weight trajectory, and repeat testing interval."));
  }

  if (patient.falls > 0) {
    actions.push(action("Falls", patient.falls > 1 ? "High" : "Moderate", "Falls are reported. Check gait, vision, footwear, orthostatic BP, home hazards, osteoporosis risk, sedatives, antihypertensives, and strength/balance exercise options."));
  }

  if (patient.frailtySignal === "yes") {
    actions.push(action("Frailty", "High", "Frailty signals are present. Consider a structured frailty assessment, medication review, protein/energy intake review, resistance exercise, and reversible contributors."));
  }

  if (patient.functionSignal === "yes") {
    actions.push(action("Function", "High", "ADL/IADL difficulty is reported. Clarify the task limitation, caregiver support, rehabilitation needs, assistive devices, and home safety."));
  }

  if (patient.cognitionSignal === "yes") {
    actions.push(action("Cognition", "Moderate", "Cognitive concern is reported. Check delirium triggers, sensory impairment, depression, sleep, medications with anticholinergic burden, B12/thyroid testing where appropriate, and caregiver safety needs."));
  }

  if (patient.moodSignal === "yes") {
    actions.push(action("Mental health", "Moderate", "Mood, anxiety, or sleep concern is reported. Screen with a validated local tool, assess self-harm risk when relevant, review pain and social isolation, and plan follow-up."));
  }

  actions.push(action("Prevention", "Routine", "Review immunisation, oral health, vision/hearing, physical activity, protein intake, medication burden, social support, advance care preferences, and local referral options."));
  return actions;
}

function action(domain, priority, text) {
  return { domain, priority, text };
}

function renderSummary(patient, respiratory, actions) {
  const high = actions.filter((item) => item.priority === "High").length;
  const moderate = actions.filter((item) => item.priority === "Moderate").length;
  const bmiLabel = patient.bmi === null ? "Not entered" : patient.bmi.toFixed(1);
  const lungPattern = patternLabel(respiratory.classification);
  summaryStrip.innerHTML = [
    metric("Pattern", lungPattern),
    metric("FEV1", `${respiratory.fev1.percentPredicted.toFixed(0)}% predicted`),
    metric("FVC", `${respiratory.fvc.percentPredicted.toFixed(0)}% predicted`),
    metric("BMI", bmiLabel),
    metric("High priority", String(high)),
    metric("Moderate", String(moderate)),
    metric("Ratio", `${respiratory.ratio.observed.toFixed(1)}%`),
    metric("Age range", "LASI 45-90"),
  ].join("");
}

function renderSpirometryCards(respiratory) {
  const cards = [
    card("FEV1", respiratory.fev1, "L"),
    card("FVC", respiratory.fvc, "L"),
    card("FEV1/FVC", respiratory.ratio, "%"),
  ];
  spirometryCards.innerHTML = cards.join("");
}

function renderRespiratoryInterpretation(patient, respiratory) {
  const c = respiratory.classification;
  const tags = [];
  tags.push(tag(patternLabel(c), c.obstructionLln || c.prismLln || c.rspLln ? "alert" : c.prismFixed || c.rspFixed ? "warn" : ""));
  tags.push(tag(`FEV1 z-score ${respiratory.fev1.z.toFixed(2)}; LLN ${respiratory.fev1.lln.toFixed(2)} L`, respiratory.fev1.observed < respiratory.fev1.lln ? "alert" : ""));
  tags.push(tag(`FVC z-score ${respiratory.fvc.z.toFixed(2)}; LLN ${respiratory.fvc.lln.toFixed(2)} L`, respiratory.fvc.observed < respiratory.fvc.lln ? "alert" : ""));
  tags.push(tag(`FEV1/FVC z-score ${respiratory.ratio.z.toFixed(2)}; LLN ${respiratory.ratio.lln.toFixed(1)}%`, c.obstructionLln ? "alert" : ""));

  if (patient.age > 85 || patient.height < 135 || patient.height > 190) {
    tags.push(tag("Interpret cautiously at age or height extremes; external clinical validation is still needed.", "warn"));
  }
  if (patient.respSymptoms === "yes") {
    tags.push(tag("Symptoms are present; clinical review should continue even if values are above LLN.", "warn"));
  }

  respInterpretation.innerHTML = `<div class="tag-list">${tags.join("")}</div>`;
}

function renderAgeingActions(actions) {
  ageingActions.innerHTML = `<div class="action-list">${actions.map((item) => `
    <div class="action-item">
      <strong>${escapeHtml(item.domain)}<br>${escapeHtml(item.priority)}</strong>
      <p>${escapeHtml(item.text)}</p>
    </div>
  `).join("")}</div>`;
}

function renderError(message) {
  summaryStrip.innerHTML = `<div class="error-state">${escapeHtml(message)}</div>`;
  spirometryCards.innerHTML = "";
  respInterpretation.innerHTML = "";
  ageingActions.innerHTML = "";
}

function metric(label, value) {
  return `<div class="metric"><span>${escapeHtml(label)}</span><strong>${escapeHtml(value)}</strong></div>`;
}

function card(label, score, unit) {
  const status = score.observed < score.lln ? "Below LLN" : "Above LLN";
  const value = unit === "%" ? score.observed.toFixed(1) : score.observed.toFixed(2);
  const predicted = unit === "%" ? score.predicted.toFixed(1) : score.predicted.toFixed(2);
  const lln = unit === "%" ? score.lln.toFixed(1) : score.lln.toFixed(2);
  const barValue = Math.max(0, Math.min(120, score.percentPredicted));
  return `
    <article class="result-card">
      <span>${escapeHtml(label)}</span>
      <strong>${value} ${unit}</strong>
      <div>${status}</div>
      <div>Predicted ${predicted} ${unit}; LLN ${lln} ${unit}</div>
      <div>Z ${score.z.toFixed(2)}; ${score.percentPredicted.toFixed(0)}% predicted</div>
      <div class="bar" aria-hidden="true"><i style="--value:${barValue}%"></i></div>
    </article>
  `;
}

function tag(text, level) {
  return `<div class="tag ${level || ""}">${escapeHtml(text)}</div>`;
}

function patternLabel(c) {
  if (c.obstructionLln) return "Airflow obstruction flag by LASI LLN";
  if (c.prismLln && c.rspLln) return "Preserved ratio with low FEV1 and low FVC by LLN";
  if (c.prismLln) return "PRISm flag by LASI LLN";
  if (c.rspLln) return "Restrictive spirometric pattern flag by LASI LLN";
  if (c.prismFixed && c.rspFixed) return "Preserved ratio with low FEV1 and low FVC by fixed 80% threshold";
  if (c.prismFixed) return "PRISm flag by fixed 80% threshold";
  if (c.rspFixed) return "Restrictive spirometric pattern flag by fixed 80% threshold";
  return "No LASI LLN impairment flag";
}

function numberFrom(id, optional = false) {
  const value = document.getElementById(id).value;
  if (value === "" && optional) return null;
  const number = Number(value);
  if (!Number.isFinite(number)) {
    throw new Error(`Enter a valid number for ${id}.`);
  }
  return number;
}

function normalizeSex(value) {
  const text = String(value).trim().toLowerCase();
  if (["m", "male", "man", "men"].includes(text)) return "M";
  if (["f", "female", "woman", "women"].includes(text)) return "F";
  throw new Error("Sex must be male or female for the LASI reference equation.");
}

function normalizeParameter(value) {
  const text = String(value).trim().toLowerCase().replace("/", "");
  if (text === "fev1" || text === "fvc" || text === "fev1fvc") return text;
  if (text === "ratio") return "fev1fvc";
  throw new Error("Unknown spirometry parameter.");
}

function parseCsv(csv) {
  const rows = [];
  let row = [];
  let field = "";
  let inQuotes = false;

  for (let i = 0; i < csv.length; i += 1) {
    const char = csv[i];
    const next = csv[i + 1];
    if (char === '"' && inQuotes && next === '"') {
      field += '"';
      i += 1;
    } else if (char === '"') {
      inQuotes = !inQuotes;
    } else if (char === "," && !inQuotes) {
      row.push(field);
      field = "";
    } else if ((char === "\n" || char === "\r") && !inQuotes) {
      if (char === "\r" && next === "\n") i += 1;
      row.push(field);
      if (row.some((value) => value !== "")) rows.push(row);
      row = [];
      field = "";
    } else {
      field += char;
    }
  }

  if (field || row.length) {
    row.push(field);
    rows.push(row);
  }

  const headers = rows.shift().map((header) => header.trim());
  return rows.map((values) => Object.fromEntries(headers.map((header, index) => [header, values[index] || ""])));
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}
