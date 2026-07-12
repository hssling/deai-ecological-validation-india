const LMS_Z = -1.6448536269514722;
const state = {
  lmsRows: [],
};

const form = document.getElementById("patientForm");
const summaryStrip = document.getElementById("summaryStrip");
const spirometryCards = document.getElementById("spirometryCards");
const respInterpretation = document.getElementById("respInterpretation");
const ageingActions = document.getElementById("ageingActions");
const careMap = document.getElementById("careMap");
const patientPlan = document.getElementById("patientPlan");
const followUpPlan = document.getElementById("followUpPlan");
const outputMeta = document.getElementById("outputMeta");
const loadGauge = document.getElementById("loadGauge");
const priorityStack = document.getElementById("priorityStack");
const copyReport = document.getElementById("copyReport");
const downloadReport = document.getElementById("downloadReport");
const printReport = document.getElementById("printReport");
const backToTop = document.getElementById("backToTop");
let lastReportText = "";
let lastReportJson = null;

init();
initNavigation();

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

backToTop.addEventListener("click", () => {
  window.scrollTo({ top: 0, behavior: "smooth" });
});

copyReport.addEventListener("click", async () => {
  if (!lastReportText) return;
  try {
    await navigator.clipboard.writeText(lastReportText);
    setOutputMeta("Summary copied");
  } catch {
    setOutputMeta("Copy unavailable");
  }
});

downloadReport.addEventListener("click", () => {
  if (!lastReportJson) return;
  const payload = JSON.stringify(lastReportJson, null, 2);
  const blob = new Blob([payload], { type: "application/json" });
  const url = URL.createObjectURL(blob);
  const anchor = document.createElement("a");
  anchor.href = url;
  anchor.download = `healthy-ageing-summary-${new Date().toISOString().slice(0, 10)}.json`;
  document.body.append(anchor);
  anchor.click();
  anchor.remove();
  URL.revokeObjectURL(url);
  setOutputMeta("JSON downloaded");
});

function updateAssessment() {
  if (!state.lmsRows.length) return;

  try {
    const patient = readPatient();
    const respiratory = scoreSpirometry(patient);
    const actions = buildAgeingActions(patient, respiratory);
    const domainScores = buildDomainScores(patient, respiratory, actions);
    const patientCards = buildPatientPlan(patient, respiratory, actions, domainScores);
    const followUp = buildFollowUpPlan(patient, respiratory, actions);
    renderSummary(patient, respiratory, actions);
    renderReviewLoad(actions);
    renderSpirometryCards(respiratory);
    renderCareMap(domainScores);
    renderRespiratoryInterpretation(patient, respiratory);
    renderAgeingActions(actions);
    renderPatientPlan(patientCards);
    renderFollowUpPlan(followUp);
    lastReportText = buildReportText(patient, respiratory, actions, domainScores, patientCards, followUp);
    lastReportJson = buildReportJson(patient, respiratory, actions, domainScores, patientCards, followUp);
    setOutputMeta("Updated " + new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }));
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
    visitGoal: document.getElementById("visitGoal").value,
    planStyle: document.getElementById("planStyle").value,
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

function buildPatientPlan(patient, respiratory, actions, domains) {
  const urgent = [
    "Severe or worsening breathlessness at rest",
    "Chest pain, fainting, blue lips, confusion, or very low oxygen saturation if measured",
    "Coughing blood, new one-sided weakness, or sudden severe illness",
  ];
  const topDomains = domains
    .filter((item) => item.priority !== "Routine")
    .slice(0, 3)
    .map((item) => item.label.toLowerCase());
  const focus = visitGoalText(patient.visitGoal);
  const pattern = patternLabel(respiratory.classification);
  const resultText = respiratory.classification.obstructionLln || respiratory.classification.prismLln || respiratory.classification.rspLln
    ? "Some breathing test values are below the lower range expected for similar older Indian adults. This should be reviewed with test quality, symptoms, and examination."
    : "The breathing test is not below LASI lower-limit thresholds, but symptoms and clinical examination still matter.";
  const goalText = patient.planStyle === "brief"
    ? `Focus today: ${focus}. Review ${topDomains.length ? topDomains.join(", ") : "prevention and routine follow-up"}.`
    : `For this visit, the main focus is ${focus}. The clinical review should connect the test result with symptoms, activity, medicines, nutrition, falls, and support at home.`;

  return [
    patientCard("What the result means", resultText, "Result"),
    patientCard("Main goal", goalText, "Goal"),
    patientCard("What to do next", patientNextSteps(actions), "Next"),
    patientCard("Seek urgent care if", urgent.join("; "), "Safety"),
    patientCard("Questions for the visit", patientQuestions(patient, pattern).join("; "), "Questions"),
  ];
}

function patientCard(title, text, label) {
  return { title, text, label };
}

function visitGoalText(goal) {
  const labels = {
    respiratory: "breathing, cough, wheeze, and exercise capacity",
    function: "mobility, falls prevention, strength, and daily function",
    metabolic: "blood pressure, diabetes risk, weight, medicines, and prevention",
    memory: "memory, mood, sleep, caregiver support, and daily safety",
  };
  return labels[goal] || labels.respiratory;
}

function patientNextSteps(actions) {
  const highOrModerate = actions.filter((item) => item.priority !== "Routine").slice(0, 3);
  if (!highOrModerate.length) {
    return "Continue routine prevention review, physical activity, nutrition, vaccination checks, and follow-up as advised locally.";
  }
  return highOrModerate.map((item) => `${item.domain}: ${item.text}`).join(" ");
}

function patientQuestions(patient, pattern) {
  const questions = [
    `Do my breathing test results fit my symptoms and activity level?`,
    `Was the spirometry quality acceptable, and do I need repeat or post-bronchodilator testing?`,
  ];
  if (patient.tobacco !== "never") questions.push("What is my plan to reduce tobacco, biomass, or occupational exposure?");
  if (patient.falls > 0 || patient.frailtySignal === "yes") questions.push("What strength, balance, nutrition, or rehabilitation plan is appropriate?");
  if (patient.cognitionSignal === "yes" || patient.moodSignal === "yes") questions.push("Should we screen memory, mood, sleep, medicines, or caregiver needs?");
  questions.push(`What follow-up timing is appropriate for: ${pattern}?`);
  return questions;
}

function buildFollowUpPlan(patient, respiratory, actions) {
  const high = actions.filter((item) => item.priority === "High");
  const moderate = actions.filter((item) => item.priority === "Moderate");
  let timing = "Routine follow-up interval";
  let rationale = "No high-priority flags were generated from the entered data.";
  if (high.length) {
    timing = "Prompt clinical review";
    rationale = "One or more high-priority domains were flagged. Timing should be based on symptom severity, examination, local pathways, and clinician judgement.";
  } else if (moderate.length >= 2) {
    timing = "Planned follow-up after initial optimisation";
    rationale = "Multiple moderate-priority domains were flagged, so a structured follow-up visit is useful after initial review.";
  } else if (moderate.length === 1) {
    timing = "Targeted follow-up";
    rationale = "One moderate-priority domain was flagged and should be reviewed after initial management.";
  }
  const checklist = [
    "Confirm spirometry quality, contraindications, and whether bronchodilator testing is relevant.",
    "Review current medicines, adherence, side effects, and potentially inappropriate medicines.",
    "Document patient goals, caregiver concerns, and agreed next step.",
  ];
  if (patient.respSymptoms === "yes") checklist.push("Record symptom trajectory, oxygen saturation if available, examination, and referral threshold.");
  if (respiratory.classification.obstructionLln || respiratory.classification.prismLln || respiratory.classification.rspLln) checklist.push("Consider repeat spirometry, imaging/laboratory work-up, pulmonary rehabilitation, or specialist referral according to local guidance.");
  if (patient.falls > 0 || patient.frailtySignal === "yes") checklist.push("Add gait, orthostatic BP, vision, footwear, home safety, protein intake, and strength/balance exercise review.");
  return { timing, rationale, checklist };
}

function buildDomainScores(patient, respiratory, actions) {
  const c = respiratory.classification;
  const respiratoryLevel = c.obstructionLln || patient.respSymptoms === "yes"
    ? "High"
    : c.prismLln || c.rspLln || c.prismFixed || c.rspFixed || patient.tobacco !== "never"
      ? "Moderate"
      : "Routine";
  return [
    domain("Respiratory", respiratoryLevel, respiratorySummary(patient, respiratory), "--lung"),
    domain("Metabolic", metabolicLevel(patient), metabolicSummary(patient), "--metabolic"),
    domain("Frailty", patient.frailtySignal === "yes" ? "High" : "Routine", patient.frailtySignal === "yes" ? "Frailty signal reported" : "No frailty signal entered", "--frailty"),
    domain("Function", patient.functionSignal === "yes" ? "High" : "Routine", patient.functionSignal === "yes" ? "ADL/IADL difficulty reported" : "No functional difficulty entered", "--function"),
    domain("Falls", patient.falls > 1 ? "High" : patient.falls === 1 ? "Moderate" : "Routine", patient.falls > 0 ? `${patient.falls} fall(s) in 12 months` : "No falls entered", "--falls"),
    domain("Cognition", patient.cognitionSignal === "yes" ? "Moderate" : "Routine", patient.cognitionSignal === "yes" ? "Cognitive concern reported" : "No cognitive concern entered", "--cognition"),
    domain("Mood and sleep", patient.moodSignal === "yes" ? "Moderate" : "Routine", patient.moodSignal === "yes" ? "Mood, anxiety, or sleep concern reported" : "No mood/sleep concern entered", "--mood"),
    domain("Prevention", "Routine", "Vaccination, medications, nutrition, activity, vision/hearing, and social support review", "--prevention"),
  ];
}

function domain(label, priority, summary, colorVar) {
  return { label, priority, summary, colorVar };
}

function respiratorySummary(patient, respiratory) {
  const pattern = patternLabel(respiratory.classification);
  const symptom = patient.respSymptoms === "yes" ? "symptoms present" : "no prominent symptoms entered";
  return `${pattern}; ${symptom}`;
}

function metabolicLevel(patient) {
  if (patient.sbp >= 160 || patient.dbp >= 100 || patient.hba1c >= 6.5 || (patient.bmi !== null && (patient.bmi < 18.5 || patient.bmi >= 30))) {
    return "Moderate";
  }
  if (patient.sbp >= 140 || patient.dbp >= 90 || patient.hba1c >= 5.7 || (patient.bmi !== null && patient.bmi >= 25)) {
    return "Routine";
  }
  return "Routine";
}

function metabolicSummary(patient) {
  const bits = [];
  if (patient.bmi !== null) bits.push(`BMI ${patient.bmi.toFixed(1)}`);
  if (patient.sbp !== null && patient.dbp !== null) bits.push(`BP ${patient.sbp}/${patient.dbp}`);
  if (patient.hba1c !== null) bits.push(`HbA1c ${patient.hba1c.toFixed(1)}%`);
  return bits.length ? bits.join("; ") : "Metabolic values not fully entered";
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

function renderReviewLoad(actions) {
  const high = actions.filter((item) => item.priority === "High").length;
  const moderate = actions.filter((item) => item.priority === "Moderate").length;
  const score = Math.min(100, high * 32 + moderate * 16 + 10);
  const label = high > 0 ? "High" : moderate > 1 ? "Moderate" : "Routine";
  loadGauge.className = `load-gauge ${label.toLowerCase()}`;
  loadGauge.style.setProperty("--load", `${score}%`);
  loadGauge.querySelector("strong").textContent = label;
  priorityStack.innerHTML = `
    <div><span>High</span><strong>${high}</strong></div>
    <div><span>Moderate</span><strong>${moderate}</strong></div>
    <div><span>Routine</span><strong>${actions.filter((item) => item.priority === "Routine").length}</strong></div>
  `;
}

function renderSpirometryCards(respiratory) {
  const cards = [
    card("FEV1", respiratory.fev1, "L"),
    card("FVC", respiratory.fvc, "L"),
    card("FEV1/FVC", respiratory.ratio, "%"),
  ];
  spirometryCards.innerHTML = cards.join("");
}

function renderCareMap(domains) {
  careMap.innerHTML = domains.map((item) => `
    <article class="care-domain ${priorityClass(item.priority)}" style="--domain-color: var(${item.colorVar})">
      <div class="domain-icon" aria-hidden="true"></div>
      <div>
        <span>${escapeHtml(item.priority)}</span>
        <strong>${escapeHtml(item.label)}</strong>
        <p>${escapeHtml(item.summary)}</p>
      </div>
    </article>
  `).join("");
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
    <div class="action-item ${priorityClass(item.priority)}">
      <strong>${escapeHtml(item.domain)}<br>${escapeHtml(item.priority)}</strong>
      <p>${escapeHtml(item.text)}</p>
    </div>
  `).join("")}</div>`;
}

function renderPatientPlan(cards) {
  patientPlan.innerHTML = cards.map((item) => `
    <article class="patient-card">
      <span>${escapeHtml(item.label)}</span>
      <strong>${escapeHtml(item.title)}</strong>
      <p>${escapeHtml(item.text)}</p>
    </article>
  `).join("");
}

function renderFollowUpPlan(plan) {
  followUpPlan.innerHTML = `
    <div class="followup-summary">
      <strong>${escapeHtml(plan.timing)}</strong>
      <p>${escapeHtml(plan.rationale)}</p>
    </div>
    <div class="followup-checklist">
      ${plan.checklist.map((item) => `<div>${escapeHtml(item)}</div>`).join("")}
    </div>
  `;
}

function renderError(message) {
  summaryStrip.innerHTML = `<div class="error-state">${escapeHtml(message)}</div>`;
  spirometryCards.innerHTML = "";
  careMap.innerHTML = "";
  respInterpretation.innerHTML = "";
  ageingActions.innerHTML = "";
  if (patientPlan) patientPlan.innerHTML = "";
  if (followUpPlan) followUpPlan.innerHTML = "";
  if (loadGauge) {
    loadGauge.className = "load-gauge";
    loadGauge.style.setProperty("--load", "0%");
    loadGauge.querySelector("strong").textContent = "--";
  }
  if (priorityStack) priorityStack.innerHTML = "";
  lastReportText = "";
  lastReportJson = null;
  setOutputMeta("Check inputs");
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

function priorityClass(priority) {
  return String(priority).toLowerCase().replaceAll(" ", "-");
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

function buildReportText(patient, respiratory, actions, domains, patientCards, followUp) {
  const lines = [
    "India Healthy Ageing Clinical Support",
    "Clinical decision support summary - not a diagnosis",
    "",
    `Age: ${patient.age} years; sex for reference equation: ${patient.sex}; height: ${patient.height} cm`,
    `BMI: ${patient.bmi === null ? "not entered" : patient.bmi.toFixed(1)}`,
    "",
    "Spirometry against LASI national reference:",
    `FEV1 ${patient.fev1.toFixed(2)} L; predicted ${respiratory.fev1.predicted.toFixed(2)} L; LLN ${respiratory.fev1.lln.toFixed(2)} L; z ${respiratory.fev1.z.toFixed(2)}; ${respiratory.fev1.percentPredicted.toFixed(0)}% predicted`,
    `FVC ${patient.fvc.toFixed(2)} L; predicted ${respiratory.fvc.predicted.toFixed(2)} L; LLN ${respiratory.fvc.lln.toFixed(2)} L; z ${respiratory.fvc.z.toFixed(2)}; ${respiratory.fvc.percentPredicted.toFixed(0)}% predicted`,
    `FEV1/FVC ${respiratory.ratio.observed.toFixed(1)}%; predicted ${respiratory.ratio.predicted.toFixed(1)}%; LLN ${respiratory.ratio.lln.toFixed(1)}%; z ${respiratory.ratio.z.toFixed(2)}`,
    `Pattern: ${patternLabel(respiratory.classification)}`,
    "",
    "Care map:",
    ...domains.map((item) => `- ${item.label}: ${item.priority} - ${item.summary}`),
    "",
    "Suggested clinical review prompts:",
    ...actions.map((item) => `- ${item.domain} (${item.priority}): ${item.text}`),
    "",
    "Patient companion plan:",
    ...patientCards.map((item) => `- ${item.title}: ${item.text}`),
    "",
    `Follow-up planner: ${followUp.timing}`,
    followUp.rationale,
    ...followUp.checklist.map((item) => `- ${item}`),
    "",
    "Source: LASI national GAMLSS/LMS spirometry reference equations for Indian adults aged 45-90 years.",
  ];
  return lines.join("\n");
}

function buildReportJson(patient, respiratory, actions, domains, patientCards, followUp) {
  return {
    generatedAt: new Date().toISOString(),
    source: "LASI national GAMLSS/LMS spirometry reference equations for Indian adults aged 45-90 years",
    clinicalBoundary: "Clinical decision support only; not a diagnosis or prescribing system.",
    patientInputs: {
      sexForReference: patient.sex,
      ageYears: patient.age,
      heightCm: patient.height,
      weightKg: patient.weight,
      bmi: patient.bmi === null ? null : Number(patient.bmi.toFixed(1)),
      tobacco: patient.tobacco,
      respiratorySymptoms: patient.respSymptoms,
      visitGoal: patient.visitGoal,
    },
    spirometry: {
      fev1: roundedScore(respiratory.fev1),
      fvc: roundedScore(respiratory.fvc),
      fev1fvc: roundedScore(respiratory.ratio),
      pattern: patternLabel(respiratory.classification),
      classification: respiratory.classification,
    },
    careMap: domains,
    clinicianActions: actions,
    patientCompanionPlan: patientCards,
    followUpPlan: followUp,
  };
}

function roundedScore(score) {
  return {
    observed: Number(score.observed.toFixed(3)),
    predicted: Number(score.predicted.toFixed(3)),
    lln: Number(score.lln.toFixed(3)),
    z: Number(score.z.toFixed(3)),
    percentPredicted: Number(score.percentPredicted.toFixed(1)),
  };
}

function setOutputMeta(text) {
  if (outputMeta) outputMeta.textContent = text;
}

function initNavigation() {
  const sectionIds = ["calculator", "care-map", "patient-plan", "portal", "evidence"];
  const navLinks = Array.from(document.querySelectorAll("[data-nav-link]"));
  const sectionMap = new Map(
    sectionIds
      .map((id) => [id, document.getElementById(id)])
      .filter(([, element]) => Boolean(element))
  );

  function setActive(id) {
    navLinks.forEach((link) => {
      const active = link.dataset.navLink === id;
      link.classList.toggle("is-active", active);
      if (active) {
        link.setAttribute("aria-current", "true");
      } else {
        link.removeAttribute("aria-current");
      }
    });
  }

  if ("IntersectionObserver" in window) {
    const observer = new IntersectionObserver((entries) => {
      const visible = entries
        .filter((entry) => entry.isIntersecting)
        .sort((a, b) => b.intersectionRatio - a.intersectionRatio)[0];
      if (visible) setActive(visible.target.id);
    }, {
      rootMargin: "-24% 0px -58% 0px",
      threshold: [0.08, 0.18, 0.32],
    });
    sectionMap.forEach((element) => observer.observe(element));
  }

  window.addEventListener("scroll", () => {
    backToTop.classList.toggle("is-visible", window.scrollY > 620);
  }, { passive: true });

  setActive("calculator");
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
