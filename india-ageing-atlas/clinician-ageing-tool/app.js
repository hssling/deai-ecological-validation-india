const LMS_Z = -1.6448536269514722;
const DEMO_ACCOUNTS = {
  clinician: {
    email: "clinician.demo@ihacs.local",
    password: "DemoClinician#2026",
    role: "clinician",
    name: "Demo clinician",
  },
  patient: {
    email: "patient.demo@ihacs.local",
    password: "DemoPatient#2026",
    role: "patient",
    name: "Demo patient",
  },
  caregiver: {
    email: "care.demo@ihacs.local",
    password: "DemoCare#2026",
    role: "caregiver",
    name: "Demo caregiver",
  },
};
const LANGUAGE_CONTENT = {
  en: {
    name: "English",
    title: "Patient education in Indian languages",
    intro: "Choose a language to adapt the patient-facing education, visit preparation, warning symptoms, and follow-up support content. Clinical calculations remain unchanged.",
    cards: [
      ["Result meaning", "Your breathing test is compared with Indian reference values for similar age, sex, and height. The result should be reviewed with symptoms, examination, and test quality."],
      ["Healthy ageing focus", "Discuss strength, nutrition, medicines, falls, memory, mood, sleep, vaccination, tobacco exposure, and daily function during follow-up."],
      ["Seek urgent care", "Get urgent help for severe breathlessness, chest pain, fainting, confusion, blue lips, coughing blood, or sudden weakness."],
      ["Visit preparation", "Bring current medicines, previous reports, vaccination history, symptom notes, fall history, and questions for the clinician."],
    ],
  },
  hi: {
    name: "हिन्दी",
    title: "भारतीय भाषाओं में रोगी शिक्षा",
    intro: "भाषा चुनने पर रोगी के लिए शिक्षा, चेतावनी लक्षण, फॉलो-अप और मुलाकात की तैयारी की सामग्री बदलती है। गणना वही रहती है।",
    cards: [
      ["परिणाम का अर्थ", "आपकी सांस की जांच की तुलना समान उम्र, लिंग और ऊंचाई वाले भारतीय संदर्भ मानों से की जाती है। लक्षण, जांच और स्पाइरोमेट्री गुणवत्ता के साथ समीक्षा जरूरी है।"],
      ["स्वस्थ ageing focus", "ताकत, पोषण, दवाएं, गिरना, याददाश्त, मनोदशा, नींद, टीकाकरण, तंबाकू/धुएं का संपर्क और दैनिक कार्य पर चर्चा करें।"],
      ["तुरंत सहायता लें", "बहुत अधिक सांस फूलना, सीने में दर्द, बेहोशी, भ्रम, होंठ नीले पड़ना, खून वाली खांसी या अचानक कमजोरी हो तो तुरंत मदद लें।"],
      ["मुलाकात की तैयारी", "दवाएं, पुराने रिपोर्ट, टीकाकरण जानकारी, लक्षण नोट्स, गिरने का इतिहास और अपने सवाल साथ लाएं।"],
    ],
  },
  kn: {
    name: "ಕನ್ನಡ",
    title: "ಭಾರತೀಯ ಭಾಷೆಗಳಲ್ಲಿ ರೋಗಿ ಶಿಕ್ಷಣ",
    intro: "ಭಾಷೆಯನ್ನು ಆಯ್ಕೆ ಮಾಡಿದರೆ ರೋಗಿಗೆ ಶಿಕ್ಷಣ, ಎಚ್ಚರಿಕೆ ಲಕ್ಷಣಗಳು, ಫಾಲೋ-ಅಪ್ ಮತ್ತು ಭೇಟಿ ಸಿದ್ಧತೆ ವಿಷಯ ಬದಲಾಗುತ್ತದೆ. ವೈದ್ಯಕೀಯ ಗಣನೆಗಳು ಬದಲಾಗುವುದಿಲ್ಲ.",
    cards: [
      ["ಫಲಿತಾಂಶದ ಅರ್ಥ", "ನಿಮ್ಮ ಉಸಿರಾಟ ಪರೀಕ್ಷೆಯನ್ನು ಸಮಾನ ವಯಸ್ಸು, ಲಿಂಗ ಮತ್ತು ಎತ್ತರದ ಭಾರತೀಯ ಉಲ್ಲೇಖ ಮೌಲ್ಯಗಳೊಂದಿಗೆ ಹೋಲಿಸಲಾಗುತ್ತದೆ. ಲಕ್ಷಣಗಳು, ಪರೀಕ್ಷೆ ಮತ್ತು ಸ್ಪೈರೊಮೆಟ್ರಿ ಗುಣಮಟ್ಟದೊಂದಿಗೆ ಪರಿಶೀಲಿಸಬೇಕು."],
      ["ಆರೋಗ್ಯಕರ ವಯೋವೃದ್ಧಿ", "ಶಕ್ತಿ, ಪೌಷ್ಟಿಕತೆ, ಔಷಧಿಗಳು, ಬೀಳುವಿಕೆ, ನೆನಪು, ಮನಸ್ಥಿತಿ, ನಿದ್ರೆ, ಲಸಿಕೆ, ತಂಬಾಕು/ಧೂಮ ಸಂಪರ್ಕ ಮತ್ತು ದಿನನಿತ್ಯದ ಕಾರ್ಯಗಳ ಬಗ್ಗೆ ಚರ್ಚಿಸಿ."],
      ["ತುರ್ತು ಸಹಾಯ ಪಡೆಯಿರಿ", "ತೀವ್ರ ಉಸಿರಾಟ ತೊಂದರೆ, ಎದೆ ನೋವು, ಮೂರ್ಛೆ, ಗೊಂದಲ, ನೀಲಿ ತುಟಿ, ರಕ್ತದ ಕೆಮ್ಮು ಅಥವಾ ಅಕಸ್ಮಾತ್ ದೌರ್ಬಲ್ಯ ಇದ್ದರೆ ತಕ್ಷಣ ಸಹಾಯ ಪಡೆಯಿರಿ."],
      ["ಭೇಟಿಗೆ ಸಿದ್ಧತೆ", "ಪ್ರಸ್ತುತ ಔಷಧಿಗಳು, ಹಿಂದಿನ ವರದಿಗಳು, ಲಸಿಕೆ ಇತಿಹಾಸ, ಲಕ್ಷಣಗಳ ಟಿಪ್ಪಣಿ, ಬೀಳುವಿಕೆ ಇತಿಹಾಸ ಮತ್ತು ಪ್ರಶ್ನೆಗಳನ್ನು ತಂದುಕೊಳ್ಳಿ."],
    ],
  },
  ta: {
    name: "தமிழ்",
    title: "இந்திய மொழிகளில் நோயாளர் கல்வி",
    intro: "மொழியைத் தேர்ந்தெடுத்தால் நோயாளருக்கான கல்வி, எச்சரிக்கை அறிகுறிகள், பின்தொடர்பு மற்றும் வருகைத் தயாரிப்பு உள்ளடக்கம் மாறும். மருத்துவ கணக்கீடுகள் மாறாது.",
    cards: [
      ["முடிவின் பொருள்", "உங்கள் மூச்சுப் பரிசோதனை ஒரே வயது, பாலினம், உயரம் கொண்ட இந்திய குறிப்புமதிப்புகளுடன் ஒப்பிடப்படுகிறது. அறிகுறிகள், பரிசோதனை மற்றும் ஸ்பைரோமெட்ரி தரத்துடன் மதிப்பிட வேண்டும்."],
      ["ஆரோக்கியமான முதுமை", "வலிமை, ஊட்டச்சத்து, மருந்துகள், விழுதல், நினைவு, மனநிலை, தூக்கம், தடுப்பூசி, புகை/தூசி வெளிப்பாடு மற்றும் தினசரி செயல்பாடு குறித்து பேசுங்கள்."],
      ["அவசர உதவி தேவை", "கடுமையான மூச்சுத்திணறல், நெஞ்சு வலி, மயக்கம், குழப்பம், நீல உதடு, இரத்தக் காசல் அல்லது திடீர் பலவீனம் இருந்தால் உடனடி உதவி பெறுங்கள்."],
      ["வருகைக்கு தயாராக", "தற்போதைய மருந்துகள், பழைய அறிக்கைகள், தடுப்பூசி வரலாறு, அறிகுறி குறிப்புகள், விழுதல் வரலாறு மற்றும் கேள்விகளை கொண்டு வாருங்கள்."],
    ],
  },
  te: {
    name: "తెలుగు",
    title: "భారతీయ భాషల్లో రోగి విద్య",
    intro: "భాషను ఎంచుకుంటే రోగి విద్య, హెచ్చరిక లక్షణాలు, ఫాలో-అప్ మరియు సందర్శన సిద్ధత మారుతుంది. క్లినికల్ లెక్కలు మారవు.",
    cards: [
      ["ఫలిత అర్థం", "మీ శ్వాస పరీక్షను అదే వయస్సు, లింగం, ఎత్తు ఉన్న భారతీయ సూచిక విలువలతో పోలుస్తారు. లక్షణాలు, పరీక్ష మరియు స్పైరోమెట్రీ నాణ్యతతో కలిసి సమీక్షించాలి."],
      ["ఆరోగ్యకర వృద్ధాప్యం", "బలం, పోషణ, మందులు, పడిపోవడం, జ్ఞాపకం, మూడ్, నిద్ర, టీకాలు, పొగాకు/పొగ పరిచయం మరియు రోజువారీ పనుల గురించి మాట్లాడండి."],
      ["అత్యవసర సహాయం", "తీవ్ర శ్వాస ఇబ్బంది, ఛాతి నొప్పి, మూర్ఛ, గందరగోళం, నీలి పెదవులు, రక్తంతో దగ్గు లేదా అకస్మాత్తు బలహీనత ఉంటే వెంటనే సహాయం పొందండి."],
      ["సందర్శన సిద్ధత", "ప్రస్తుత మందులు, పాత నివేదికలు, టీకా చరిత్ర, లక్షణాల గమనికలు, పడిపోవడం చరిత్ర మరియు ప్రశ్నలు తీసుకురండి."],
    ],
  },
  mr: {
    name: "मराठी",
    title: "भारतीय भाषांमध्ये रुग्ण शिक्षण",
    intro: "भाषा निवडल्यावर रुग्ण शिक्षण, इशारा लक्षणे, फॉलो-अप आणि भेटीची तयारी यातील मजकूर बदलतो. वैद्यकीय गणना बदलत नाहीत.",
    cards: [
      ["निकालाचा अर्थ", "आपली श्वसन चाचणी समान वय, लिंग आणि उंची असलेल्या भारतीय संदर्भ मूल्यांशी तुलना केली जाते. लक्षणे, तपासणी आणि स्पायरोमेट्री गुणवत्तेसह आढावा आवश्यक आहे."],
      ["आरोग्यदायी वृद्धत्व", "शक्ती, पोषण, औषधे, पडणे, स्मरणशक्ती, मनःस्थिती, झोप, लसीकरण, तंबाखू/धूर संपर्क आणि दैनंदिन कार्य यावर चर्चा करा."],
      ["तातडीची मदत घ्या", "तीव्र श्वास लागणे, छातीत दुखणे, बेशुद्ध पडणे, गोंधळ, ओठ निळे होणे, रक्ताची खोकला किंवा अचानक अशक्तपणा असल्यास तातडीची मदत घ्या."],
      ["भेटीची तयारी", "सध्याची औषधे, जुने अहवाल, लसीकरण इतिहास, लक्षणांच्या नोंदी, पडण्याचा इतिहास आणि प्रश्न सोबत आणा."],
    ],
  },
};
const ROLE_WORKFLOWS = {
  clinician: {
    title: "Clinician workspace",
    intro: "Structured assessment, documentation, education, referral review, and follow-up planning.",
    steps: [
      ["Assess", "Run LASI spirometry scoring, review frailty/function/cognition/mood/falls/metabolic signals, and confirm test quality."],
      ["Decide", "Use priority prompts to plan repeat testing, guideline-based management, referral, rehabilitation, medication review, and prevention."],
      ["Document", "Copy or save a concise summary with inputs, LASI comparison, domain priorities, and follow-up rationale."],
      ["Follow up", "Track longitudinal changes in lung function, symptoms, falls, BP, HbA1c, function, vaccinations, and patient goals."],
    ],
  },
  patient: {
    title: "Patient companion",
    intro: "Plain-language understanding, goals, warning symptoms, visit preparation, and follow-up support.",
    steps: [
      ["Understand", "Read patient-friendly result meaning in the selected language."],
      ["Prepare", "List medicines, prior reports, symptoms, falls, vaccination history, and questions before the visit."],
      ["Act", "Follow clinician-agreed goals for activity, breathing symptoms, nutrition, medicines, safety, and exposure reduction."],
      ["Return", "Use warning symptoms and follow-up timing to know when to seek help or attend planned review."],
    ],
  },
  caregiver: {
    title: "Caregiver support",
    intro: "Home safety, medicine support, symptom observation, appointment preparation, and escalation prompts.",
    steps: [
      ["Observe", "Track breathlessness, cough, activity tolerance, appetite, sleep, mood, memory, falls, and medicine adherence."],
      ["Support", "Help with appointments, reports, medicines, home safety, nutrition, exercise, and exposure reduction."],
      ["Escalate", "Recognise urgent warning symptoms and arrange timely clinical review."],
      ["Coordinate", "Share practical goals and concerns with the clinician and patient."],
    ],
  },
  researcher: {
    title: "Public health and research view",
    intro: "Evidence provenance, model limits, validation status, governance, and population-health learning needs.",
    steps: [
      ["Provenance", "Track LASI equation source, version, derivation population, age range, and validation status."],
      ["Governance", "Separate open education from patient-level records, maintain consent, audit trails, and role-based access."],
      ["Quality", "Monitor missing data, implausible inputs, repeated measures, and module versioning."],
      ["Evaluation", "Plan external validation, usability testing, calibration checks, and equity audits before high-stakes use."],
    ],
  },
};
const EVIDENCE_SOURCES = {
  lasi: "LASI national GAMLSS/LMS spirometry reference equations",
  whoIcope: "WHO ICOPE person-centred integrated care for older people",
  whoAgeing: "WHO Decade of Healthy Ageing: intrinsic capacity, functional ability, and environments",
  whoActivity: "WHO physical activity and sedentary behaviour guidance",
  cdcSteadi: "CDC STEADI falls prevention framework",
};
const PORTAL_MODULES = {
  clinician: [
    {
      title: "Respiratory decision support",
      flow: "Input spirometry -> compare with LASI LLN/z-score -> classify pattern -> confirm quality -> plan repeat testing/referral.",
      evidence: ["lasi"],
      status: "Active calculator module",
    },
    {
      title: "Intrinsic-capacity review",
      flow: "Screen mobility, cognition, mood, nutrition, sensory concerns, function, and social support -> prioritise care plan.",
      evidence: ["whoIcope", "whoAgeing"],
      status: "Structured prompt module",
    },
    {
      title: "Falls and frailty pathway",
      flow: "Falls history -> gait/orthostatic/vision/medicine/home-safety review -> strength, balance, referral, and follow-up tasks.",
      evidence: ["cdcSteadi", "whoIcope"],
      status: "Prompt module; validated scales can be added next",
    },
    {
      title: "Prevention and activity plan",
      flow: "Review activity, sedentary time, resistance/balance exercise, vaccination, tobacco exposure, nutrition, and medicines.",
      evidence: ["whoActivity", "whoAgeing"],
      status: "Education and documentation module",
    },
    {
      title: "Longitudinal monitoring",
      flow: "Save visit snapshots -> trend lung function, symptoms, BP, HbA1c, falls, function, and goals -> schedule follow-up.",
      evidence: ["whoIcope"],
      status: "Supabase-ready schema",
    },
  ],
  public: [
    {
      title: "Understand my result",
      flow: "Plain-language explanation -> selected Indian language -> key questions for clinician -> no self-diagnosis wording.",
      evidence: ["lasi", "whoAgeing"],
      status: "Multilingual education module",
    },
    {
      title: "Prepare for my visit",
      flow: "Medicine list, reports, symptoms, exposures, falls, vaccinations, caregiver concerns, and goals before appointment.",
      evidence: ["whoIcope"],
      status: "Patient companion module",
    },
    {
      title: "Act on agreed goals",
      flow: "Clinician-approved activity, nutrition, exposure reduction, medicine adherence, home safety, and follow-up reminders.",
      evidence: ["whoActivity", "cdcSteadi"],
      status: "Support and follow-up module",
    },
    {
      title: "Know warning symptoms",
      flow: "Clear urgent-care prompts for severe breathlessness, chest pain, fainting, confusion, blue lips, coughing blood, or sudden weakness.",
      evidence: ["whoIcope"],
      status: "Safety education module",
    },
    {
      title: "Caregiver coordination",
      flow: "Observe function and symptoms -> support medicines and appointments -> share concerns -> escalate when warning symptoms occur.",
      evidence: ["whoAgeing", "whoIcope"],
      status: "Caregiver workflow module",
    },
  ],
};
const PORTAL_LAUNCHES = {
  clinician: [
    ["Clinical assessment", "Open the LASI spirometry and healthy-ageing calculator.", "#calculator", "Assessment"],
    ["Respiratory review", "Review z-scores, LLN, pattern flags, symptoms, and test-quality prompts.", "#care-map", "Respiratory"],
    ["Care map", "Prioritise respiratory, metabolic, falls, frailty, cognition, mood, and prevention domains.", "#care-map", "Decision support"],
    ["Patient plan", "Generate language-ready education, visit preparation, and safety messages.", "#patient-plan", "Education"],
    ["Saved timeline", "Store and review visit snapshots with Supabase row-level security or demo storage.", "#portal-workflows", "Follow-up"],
    ["Evidence base", "Review LASI source, limits, acknowledgement, and implementation safeguards.", "#evidence", "Governance"],
  ],
  patient: [
    ["My result", "Read the patient-facing result explanation and agreed care plan.", "#patient-plan", "Understand"],
    ["Prepare visit", "Collect medicines, reports, symptoms, falls, vaccines, and questions.", "#language-support", "Preparation"],
    ["Warning symptoms", "Review when to seek urgent clinical help.", "#language-support", "Safety"],
    ["Follow-up plan", "Check the recommended review timing and practical next steps.", "#portal-workflows", "Follow-up"],
    ["Language support", "Switch patient education across supported Indian languages.", "#language-support", "Languages"],
    ["Shared summary", "Use saved snapshots or copied summaries for clinician discussion.", "#portal-workflows", "Records"],
  ],
  caregiver: [
    ["Home observation", "Track breathing, function, falls, medicines, mood, memory, sleep, and appetite.", "#patient-plan", "Observe"],
    ["Appointment support", "Prepare reports, medicines, caregiver concerns, and patient goals.", "#language-support", "Coordinate"],
    ["Escalation guide", "Review warning symptoms and timing for urgent or planned review.", "#language-support", "Safety"],
    ["Care timeline", "Keep saved visit snapshots and follow-up tasks visible.", "#portal-workflows", "Follow-up"],
    ["Education pack", "Use plain-language multilingual support for shared decisions.", "#language-support", "Education"],
    ["Clinician summary", "Open the structured assessment output for discussion.", "#calculator", "Assessment"],
  ],
  researcher: [
    ["Equation provenance", "Inspect LASI equation source, scope, and current validation limits.", "#evidence", "Provenance"],
    ["Model output", "Review generated z-scores, LLN, classifications, and domain prompts.", "#calculator", "Methods"],
    ["Governance", "Check consent, privacy, row-level security, and safe-use boundaries.", "#portal-workflows", "Governance"],
    ["Module library", "Review clinical and public workflow modules for maturity and next validation.", "#portal-workflows", "Modules"],
    ["Language content", "Inspect multilingual education coverage and communication scope.", "#language-support", "Equity"],
    ["Implementation notes", "Review deployment, source acknowledgement, and safeguards.", "#evidence", "Audit"],
  ],
};
const state = {
  lmsRows: [],
  language: "en",
  portalSession: null,
  supabaseClient: null,
  savedAssessments: [],
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
const languageSelect = document.getElementById("languageSelect");
const languageTitle = document.getElementById("languageTitle");
const languageIntro = document.getElementById("languageIntro");
const languageCards = document.getElementById("languageCards");
const portalStatus = document.getElementById("portalStatus");
const portalLanding = document.querySelector(".portal-landing");
const portalLaunchGrid = document.getElementById("portalLaunchGrid");
const sessionStatus = document.getElementById("sessionStatus");
const authForm = document.getElementById("authForm");
const authEmail = document.getElementById("authEmail");
const authPassword = document.getElementById("authPassword");
const authRole = document.getElementById("authRole");
const authStatus = document.getElementById("authStatus");
const consentAgreement = document.getElementById("consentAgreement");
const registerAccount = document.getElementById("registerAccount");
const signOut = document.getElementById("signOut");
const roleTitle = document.getElementById("roleTitle");
const roleIntro = document.getElementById("roleIntro");
const workflowGrid = document.getElementById("workflowGrid");
const clinicianModules = document.getElementById("clinicianModules");
const publicModules = document.getElementById("publicModules");
const timelineList = document.getElementById("timelineList");
const timelineIntro = document.getElementById("timelineIntro");
const saveAssessment = document.getElementById("saveAssessment");
let lastReportText = "";
let lastReportJson = null;

init();
initNavigation();
initPortal();

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

async function initPortal() {
  const config = await loadRuntimeConfig();
  if (window.supabase?.createClient && config.supabaseUrl && config.supabaseAnonKey) {
    state.supabaseClient = window.supabase.createClient(config.supabaseUrl, config.supabaseAnonKey);
    portalStatus.textContent = "Supabase configured";
    checkSupabaseConnection(config);
    state.supabaseClient.auth.getSession().then(({ data }) => {
      if (data?.session?.user) {
        state.portalSession = {
          mode: "supabase",
          email: data.session.user.email,
          role: data.session.user.user_metadata?.role || "clinician",
          name: data.session.user.user_metadata?.name || data.session.user.email,
          userId: data.session.user.id,
        };
        renderPortalShell();
        loadSupabaseAssessments();
      }
    });
  } else {
    portalStatus.textContent = "Demo mode active";
  }
  renderLanguageSupport();
  renderPortalShell();
}

async function checkSupabaseConnection(config) {
  try {
    const response = await fetch(`${config.supabaseUrl}/auth/v1/settings`, {
      headers: { apikey: config.supabaseAnonKey },
    });
    portalStatus.textContent = response.ok ? "Supabase connected" : "Supabase configured; check project settings";
  } catch {
    portalStatus.textContent = "Supabase configured; connection unavailable";
  }
}

async function loadRuntimeConfig() {
  const inlineConfig = window.IHACS_CONFIG || {};
  if (inlineConfig.supabaseUrl && inlineConfig.supabaseAnonKey) {
    return inlineConfig;
  }
  try {
    const response = await fetch("config.json", { cache: "no-store" });
    if (response.ok) {
      const fileConfig = await response.json();
      return { ...inlineConfig, ...fileConfig };
    }
    const publicResponse = await fetch("config.public.json", { cache: "no-store" });
    if (!publicResponse.ok) return inlineConfig;
    const publicConfig = await publicResponse.json();
    return { ...inlineConfig, ...publicConfig };
  } catch {
    return inlineConfig;
  }
}

async function signInPortal(register = false) {
  const email = authEmail.value.trim().toLowerCase();
  const password = authPassword.value;
  const role = authRole.value;
  if (!hasConsentAgreement()) {
    setAuthMessage("Accept consent terms first");
    return;
  }
  if (!email || !password) {
    setAuthMessage("Enter email and password");
    return;
  }

  if (state.supabaseClient && !email.endsWith("@ihacs.local")) {
    setAuthMessage(register ? "Creating account..." : "Signing in...");
    let response;
    try {
      response = register
        ? await state.supabaseClient.auth.signUp({ email, password, options: { data: { role } } })
        : await state.supabaseClient.auth.signInWithPassword({ email, password });
    } catch (error) {
      setAuthMessage(friendlyAuthMessage(error.message, register));
      return;
    }
    if (response.error) {
      setAuthMessage(friendlyAuthMessage(response.error.message, register));
      if (sessionStatus) sessionStatus.textContent = "Authentication needs attention";
      return;
    }
    if (register && !response.data.session) {
      state.portalSession = null;
      if (sessionStatus) sessionStatus.textContent = "Confirm email to finish registration";
      setAuthMessage("Registration created. Check the confirmation email, then return here to sign in.");
      renderPortalShell();
      return;
    }
    const user = response.data.session?.user || response.data.user;
    if (!user?.id) {
      state.portalSession = null;
      setAuthMessage(register
        ? "Registration did not return an active session. Try signing in after confirming email."
        : "Sign-in did not return an active portal session. Please try again.");
      renderPortalShell();
      return;
    }
    state.portalSession = {
      mode: "supabase",
      email,
      role: user?.user_metadata?.role || role,
      name: user?.email || email,
      userId: user?.id || null,
    };
    const consentError = await recordConsentEvent();
    setAuthMessage(consentError
      ? `${register ? "Registered and signed in" : "Signed in"}; consent audit could not be saved`
      : register ? "Registered and signed in" : "Signed in");
    renderPortalShell();
    await loadSupabaseAssessments();
    return;
  }

  const demo = Object.values(DEMO_ACCOUNTS).find((account) => account.email === email);
  if (!demo || demo.password !== password) {
    setAuthMessage("Use a listed demo account, or configure Supabase for real accounts");
    return;
  }
  state.portalSession = {
    mode: "demo",
    email: demo.email,
    role: demo.role,
    name: demo.name,
    userId: demo.email,
  };
  authRole.value = demo.role;
  setAuthMessage(register ? "Demo accounts are already registered; demo sign-in active" : "Demo sign-in active");
  renderPortalShell();
}

async function recordConsentEvent() {
  if (!state.supabaseClient || !state.portalSession?.userId || !hasConsentAgreement()) return null;
  try {
    const { error } = await state.supabaseClient.from("consent_events").insert({
      user_id: state.portalSession.userId,
      consent_version: "dpdp-clinical-support-v1",
      accepted: true,
      purpose: "clinical decision support, education, documentation, and follow-up planning",
      language_code: state.language,
      user_agent: navigator.userAgent,
    });
    return error || null;
  } catch (error) {
    return error;
  }
}

function friendlyAuthMessage(message = "", register = false) {
  const text = String(message || "").trim();
  const lower = text.toLowerCase();
  if (lower.includes("email not confirmed")) {
    return "Email is not confirmed yet. Open the confirmation email, then sign in again.";
  }
  if (lower.includes("invalid login credentials")) {
    return "Email or password is incorrect. Use a listed demo account or register a new real email.";
  }
  if (lower.includes("email_address_invalid") || lower.includes("invalid email")) {
    return "Use a real email address for registration. Demo accounts use the listed ihacs.local emails.";
  }
  if (lower.includes("password") && lower.includes("characters")) {
    return "Password is too short. Use at least 6 characters; a stronger password is recommended.";
  }
  if (lower.includes("user already registered") || lower.includes("already registered")) {
    return "This email is already registered. Use Sign in instead of Register.";
  }
  if (lower.includes("signup") && lower.includes("disabled")) {
    return "Registration is disabled in Supabase settings. Use demo sign-in or enable signups.";
  }
  if (lower.includes("failed to fetch") || lower.includes("network")) {
    return "Could not reach the portal database. Check network access and try again.";
  }
  return text || (register ? "Registration could not be completed." : "Sign-in could not be completed.");
}

function renderPortalShell() {
  const role = state.portalSession?.role || authRole?.value || "clinician";
  const workflow = ROLE_WORKFLOWS[role] || ROLE_WORKFLOWS.clinician;
  portalLanding?.classList.toggle("is-signed-in", Boolean(state.portalSession));
  if (roleTitle) roleTitle.textContent = workflow.title;
  if (roleIntro) roleIntro.textContent = workflow.intro;
  if (sessionStatus) {
    sessionStatus.textContent = state.portalSession
      ? `${state.portalSession.name} (${state.portalSession.mode})`
      : "Not signed in";
  }
  if (workflowGrid) {
    workflowGrid.innerHTML = workflow.steps.map((step, index) => `
      <article>
        <span>${String(index + 1).padStart(2, "0")}</span>
        <strong>${escapeHtml(step[0])}</strong>
        <p>${escapeHtml(step[1])}</p>
      </article>
    `).join("");
  }
  renderPortalLaunches(role);
  renderModuleLibrary();
  renderTimeline();
}

function renderPortalLaunches(role) {
  if (!portalLaunchGrid) return;
  const signedIn = Boolean(state.portalSession);
  const launches = PORTAL_LAUNCHES[role] || PORTAL_LAUNCHES.clinician;
  portalLaunchGrid.innerHTML = launches.map((launch) => {
    const [title, description, href, tag] = launch;
    return `
      <a class="portal-launch ${signedIn ? "is-ready" : "is-locked"}" href="${signedIn ? href : "#portal"}">
        <span>${escapeHtml(tag)}</span>
        <strong>${escapeHtml(title)}</strong>
        <p>${escapeHtml(description)}</p>
        <em>${signedIn ? "Open module" : "Sign in to open"}</em>
      </a>
    `;
  }).join("");
}

function renderModuleLibrary() {
  if (clinicianModules) {
    clinicianModules.innerHTML = PORTAL_MODULES.clinician.map(moduleCard).join("");
  }
  if (publicModules) {
    publicModules.innerHTML = PORTAL_MODULES.public.map(moduleCard).join("");
  }
}

function moduleCard(item) {
  return `
    <article>
      <span>${escapeHtml(item.status)}</span>
      <strong>${escapeHtml(item.title)}</strong>
      <p>${escapeHtml(item.flow)}</p>
      <em>${item.evidence.map((key) => escapeHtml(EVIDENCE_SOURCES[key])).join(" · ")}</em>
    </article>
  `;
}

function renderLanguageSupport() {
  const content = LANGUAGE_CONTENT[state.language] || LANGUAGE_CONTENT.en;
  if (languageTitle) languageTitle.textContent = content.title;
  if (languageIntro) languageIntro.textContent = content.intro;
  if (languageCards) {
    languageCards.innerHTML = content.cards.map((card, index) => `
      <article>
        <span>${content.name} ${String(index + 1).padStart(2, "0")}</span>
        <strong>${escapeHtml(card[0])}</strong>
        <p>${escapeHtml(card[1])}</p>
      </article>
    `).join("");
  }
}

async function saveCurrentAssessment() {
  if (!lastReportJson) {
    updateAssessment();
  }
  if (!lastReportJson) {
    setOutputMeta("No assessment available");
    return;
  }
  if (!state.portalSession) {
    setAuthMessage("Sign in to save");
    document.getElementById("portal")?.scrollIntoView({ behavior: "smooth" });
    return;
  }
  if (!hasConsentAgreement()) {
    setAuthMessage("Accept consent terms first");
    document.getElementById("portal")?.scrollIntoView({ behavior: "smooth" });
    return;
  }

  const record = {
    id: `${Date.now()}-${Math.random().toString(16).slice(2)}`,
    savedAt: new Date().toISOString(),
    role: state.portalSession.role,
    language: state.language,
    consent: consentMetadata(),
    summary: lastReportJson,
  };

  if (state.supabaseClient && state.portalSession.mode === "supabase") {
    const { error } = await state.supabaseClient.from("assessments").insert({
      owner_id: state.portalSession.userId,
      role_context: state.portalSession.role,
      language_code: state.language,
      patient_snapshot: lastReportJson.patientInputs,
      spirometry_result: lastReportJson.spirometry,
      care_map: lastReportJson.careMap,
      clinician_actions: lastReportJson.clinicianActions,
      patient_plan: lastReportJson.patientCompanionPlan,
      follow_up_plan: lastReportJson.followUpPlan,
      report_text: lastReportText,
      consent_context: consentMetadata(),
    });
    if (error) {
      setOutputMeta(error.message);
      return;
    }
    await loadSupabaseAssessments();
    setOutputMeta("Saved to Supabase");
    return;
  }

  state.savedAssessments.unshift(record);
  state.savedAssessments = state.savedAssessments.slice(0, 8);
  renderTimeline();
  setOutputMeta("Saved in demo timeline");
}

function hasConsentAgreement() {
  return Boolean(consentAgreement?.checked);
}

function consentMetadata() {
  return {
    accepted: hasConsentAgreement(),
    acceptedAt: hasConsentAgreement() ? new Date().toISOString() : null,
    version: "dpdp-clinical-support-v1",
    scope: "minimum necessary clinical decision support, education, documentation, and follow-up planning",
    warning: "not emergency triage, diagnosis, or prescribing",
  };
}

async function loadSupabaseAssessments() {
  if (!state.supabaseClient || !state.portalSession?.userId) return;
  const { data, error } = await state.supabaseClient
    .from("assessments")
    .select("id, created_at, role_context, language_code, spirometry_result, follow_up_plan")
    .order("created_at", { ascending: false })
    .limit(8);
  if (error) {
    setOutputMeta(error.message);
    return;
  }
  state.savedAssessments = (data || []).map((row) => ({
    id: row.id,
    savedAt: row.created_at,
    role: row.role_context,
    language: row.language_code,
    summary: {
      spirometry: row.spirometry_result,
      followUpPlan: row.follow_up_plan,
    },
  }));
  renderTimeline();
}

function renderTimeline() {
  if (!timelineIntro || !timelineList) return;
  timelineIntro.textContent = state.portalSession?.mode === "supabase"
    ? "Assessments are stored under the signed-in Supabase user with row-level security."
    : "Demo assessments are kept only in this browser unless Supabase is configured.";
  if (!state.savedAssessments.length) {
    timelineList.innerHTML = `<div class="empty-state">No saved assessments yet. Run the calculator, sign in, and select Save to portal.</div>`;
    return;
  }
  timelineList.innerHTML = state.savedAssessments.map((record) => {
    const pattern = record.summary?.spirometry?.pattern || record.summary?.spirometry?.classification ? "Saved spirometry result" : "Assessment saved";
    const followUp = record.summary?.followUpPlan?.timing || "Follow-up plan available";
    return `
      <article>
        <span>${escapeHtml(new Date(record.savedAt).toLocaleString())}</span>
        <strong>${escapeHtml(pattern)}</strong>
        <p>${escapeHtml(followUp)} · ${escapeHtml(record.role)} · ${escapeHtml(record.language)}</p>
      </article>
    `;
  }).join("");
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

if (languageSelect) {
  languageSelect.addEventListener("change", () => {
    state.language = languageSelect.value;
    renderLanguageSupport();
    renderPortalShell();
    document.documentElement.lang = state.language;
  });
}

if (authForm) {
  authForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    await signInPortal(false);
  });
}

if (authRole) {
  authRole.addEventListener("change", () => {
    renderPortalShell();
  });
}

if (registerAccount) {
  registerAccount.addEventListener("click", async () => {
    await signInPortal(true);
  });
}

if (signOut) {
  signOut.addEventListener("click", async () => {
    if (state.supabaseClient && state.portalSession?.mode === "supabase") {
      await state.supabaseClient.auth.signOut();
    }
    state.portalSession = null;
    renderPortalShell();
    setAuthMessage("Signed out");
  });
}

document.querySelectorAll("[data-demo-account]").forEach((button) => {
  button.addEventListener("click", async () => {
    const account = DEMO_ACCOUNTS[button.dataset.demoAccount];
    if (!account) return;
    authEmail.value = account.email;
    authPassword.value = account.password;
    authRole.value = account.role;
    if (consentAgreement) consentAgreement.checked = true;
    await signInPortal(false);
  });
});

if (saveAssessment) {
  saveAssessment.addEventListener("click", async () => {
    await saveCurrentAssessment();
  });
}

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
  const lungPattern = patternShortLabel(respiratory.classification);
  const ratioStatus = respiratory.classification.obstructionLln ? "Below LASI LLN" : "At or above LASI LLN";
  const fev1Status = respiratory.fev1.observed < respiratory.fev1.lln ? "below LLN" : "at or above LLN";
  const fvcStatus = respiratory.fvc.observed < respiratory.fvc.lln ? "below LLN" : "at or above LLN";
  const priorityText = high > 0 ? "Prompt review" : moderate > 1 ? "Structured review" : "Routine review";
  const metabolicText = metabolicSummary(patient);
  summaryStrip.innerHTML = [
    metric("Overall lung pattern", lungPattern, "Screening flag from FEV1, FVC, and FEV1/FVC against LASI LLN."),
    metric("FEV1 vs reference", `${respiratory.fev1.percentPredicted.toFixed(0)}% predicted`, `Observed ${respiratory.fev1.observed.toFixed(2)} L; ${fev1Status}.`),
    metric("FVC vs reference", `${respiratory.fvc.percentPredicted.toFixed(0)}% predicted`, `Observed ${respiratory.fvc.observed.toFixed(2)} L; ${fvcStatus}.`),
    metric("FEV1/FVC ratio", `${respiratory.ratio.observed.toFixed(1)}%`, ratioStatus),
    metric("Clinical review priority", priorityText, `${high} high-priority and ${moderate} moderate-priority prompts generated.`),
    metric("Metabolic snapshot", metabolicText, "BMI, blood pressure, and HbA1c entered for this visit."),
    metric("BMI", bmiLabel, patient.bmi === null ? "Weight or height not entered." : "Use with age, function, nutrition, and comorbidity context."),
    metric("Reference range", "LASI 45-90 years", `Current entry: ${patient.age.toFixed(1)} years, ${patient.height.toFixed(1)} cm.`),
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
    <div><span>High-priority prompts</span><strong>${high}</strong></div>
    <div><span>Moderate prompts</span><strong>${moderate}</strong></div>
    <div><span>Routine prompts</span><strong>${actions.filter((item) => item.priority === "Routine").length}</strong></div>
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

function metric(label, value, detail) {
  return `
    <div class="metric">
      <span>${escapeHtml(label)}</span>
      <strong>${escapeHtml(value)}</strong>
      <em>${escapeHtml(detail)}</em>
    </div>
  `;
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

function patternShortLabel(c) {
  if (c.obstructionLln) return "Obstruction flag";
  if (c.prismLln && c.rspLln) return "Low FEV1 + low FVC";
  if (c.prismLln) return "PRISm flag";
  if (c.rspLln) return "Restrictive pattern flag";
  if (c.prismFixed && c.rspFixed) return "Low FEV1 + low FVC";
  if (c.prismFixed) return "PRISm flag";
  if (c.rspFixed) return "Restrictive pattern flag";
  return "No LLN impairment flag";
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

function setAuthMessage(text) {
  if (authStatus) authStatus.textContent = text;
  setOutputMeta(text);
}

function initNavigation() {
  const sectionIds = ["calculator", "care-map", "patient-plan", "portal", "language-support", "evidence"];
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
