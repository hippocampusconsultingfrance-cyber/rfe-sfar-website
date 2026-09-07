(function(){
"use strict";

/* ============================================================
   Data
   ============================================================ */
var RAW = {
  anticoagulants: JSON.parse(document.getElementById('content-anticoagulants').textContent),
  ecbu: JSON.parse(document.getElementById('content-ecbu').textContent),
  choc_hemorragique: JSON.parse(document.getElementById('content-choc_hemorragique').textContent),
  intubation_urgence: JSON.parse(document.getElementById('content-intubation_urgence').textContent),
  sepsis: JSON.parse(document.getElementById('content-sepsis').textContent),
  urgences_obstetricales: JSON.parse(document.getElementById('content-urgences_obstetricales').textContent),
  anaphylaxie: JSON.parse(document.getElementById('content-anaphylaxie').textContent),
  preeclampsie: JSON.parse(document.getElementById('content-preeclampsie').textContent),
  hyperthermie_maligne: JSON.parse(document.getElementById('content-hyperthermie_maligne').textContent),
  anticoag_urgence: JSON.parse(document.getElementById('content-anticoag_urgence').textContent),
  traumatisme_abdominal: JSON.parse(document.getElementById('content-traumatisme_abdominal').textContent),
  sedation_reanimation: JSON.parse(document.getElementById('content-sedation_reanimation').textContent),
  sedation_urgences: JSON.parse(document.getElementById('content-sedation_urgences').textContent),
  vni: JSON.parse(document.getElementById('content-vni').textContent),
  aap_urgence: JSON.parse(document.getElementById('content-aap_urgence').textContent),
  curares: JSON.parse(document.getElementById('content-curares').textContent),
  remplissage: JSON.parse(document.getElementById('content-remplissage').textContent),
  traumatisme_membre: JSON.parse(document.getElementById('content-traumatisme_membre').textContent),
  voies_aeriennes_enfant: JSON.parse(document.getElementById('content-voies_aeriennes_enfant').textContent),
  intubation_difficile_adulte: JSON.parse(document.getElementById('content-intubation_difficile_adulte').textContent),
  traumatisme_pelvien: JSON.parse(document.getElementById('content-traumatisme_pelvien').textContent),
  traumatisme_thoracique: JSON.parse(document.getElementById('content-traumatisme_thoracique').textContent),
  traumatisme_cranien: JSON.parse(document.getElementById('content-traumatisme_cranien').textContent),
  traumatisme_vertebromedullaire: JSON.parse(document.getElementById('content-traumatisme_vertebromedullaire').textContent),
  intubation_reanimation: JSON.parse(document.getElementById('content-intubation_reanimation').textContent),
  traumatisme_cranien_leger: JSON.parse(document.getElementById('content-traumatisme_cranien_leger').textContent),
  lat_soins_critiques: JSON.parse(document.getElementById('content-lat_soins_critiques').textContent),
  sdra: JSON.parse(document.getElementById('content-sdra').textContent),
  pavm: JSON.parse(document.getElementById('content-pavm').textContent),
  tracheotomie: JSON.parse(document.getElementById('content-tracheotomie').textContent),
  nutrition: JSON.parse(document.getElementById('content-nutrition').textContent),
  eer: JSON.parse(document.getElementById('content-eer').textContent),
  ira: JSON.parse(document.getElementById('content-ira').textContent),
  ih: JSON.parse(document.getElementById('content-ih').textContent),
  epanchement_pleural: JSON.parse(document.getElementById('content-epanchement_pleural').textContent),
  anemie: JSON.parse(document.getElementById('content-anemie').textContent),
  hypothermie: JSON.parse(document.getElementById('content-hypothermie').textContent),
  nvpo: JSON.parse(document.getElementById('content-nvpo').textContent),
  aap_programmee: JSON.parse(document.getElementById('content-aap_programmee').textContent),
  mtev_perioperatoire: JSON.parse(document.getElementById('content-mtev_perioperatoire').textContent),
  glycemie: JSON.parse(document.getElementById('content-glycemie').textContent),
  mal_epileptique: JSON.parse(document.getElementById('content-mal_epileptique').textContent),
  allergie_prevention: JSON.parse(document.getElementById('content-allergie_prevention').textContent),
  antibioprophylaxie: JSON.parse(document.getElementById('content-antibioprophylaxie').textContent),
  controle_temperature: JSON.parse(document.getElementById('content-controle_temperature').textContent),
  tih: JSON.parse(document.getElementById('content-tih').textContent),
  civd: JSON.parse(document.getElementById('content-civd').textContent),
  eclsa: JSON.parse(document.getElementById('content-eclsa').textContent),
  transport_intrahospitalier: JSON.parse(document.getElementById('content-transport_intrahospitalier').textContent),
  transfusion_plasma: JSON.parse(document.getElementById('content-transfusion_plasma').textContent),
  sevrage_vm: JSON.parse(document.getElementById('content-sevrage_vm').textContent),
  asthme_aigu_grave: JSON.parse(document.getElementById('content-asthme_aigu_grave').textContent),
  pancreatite: JSON.parse(document.getElementById('content-pancreatite').textContent),
  corticotherapie: JSON.parse(document.getElementById('content-corticotherapie').textContent),
  antibiotherapie_probabiliste: JSON.parse(document.getElementById('content-antibiotherapie_probabiliste').textContent),
  hsa: JSON.parse(document.getElementById('content-hsa').textContent),
  sepsis_hemodynamique: JSON.parse(document.getElementById('content-sepsis_hemodynamique').textContent),
  securisation_proc: JSON.parse(document.getElementById('content-securisation_proc').textContent)
};

var LIBRARY = JSON.parse(document.getElementById('content-library').textContent);
// Mark library entries that already have a full interactive fiche on this site,
// by matching on href against each DOC_META's known source URL(s).
var FICHE_HREF_MATCH = {
  anticoagulants: ['gestion-des-anticoagulants-pour-une-procedure-invasive', 'RFE-20.4.2026'],
  ecbu: ['place-de-lecbu-avant-une-prise-en-charge-urologique', 'Reco_ECBU'],
  choc_hemorragique: ['recommandations-sur-la-reanimation-du-choc-hemorragique', '2_AFAR_Recommandations-sur-la-reanimation-du-choc-hemorragique'],
  intubation_urgence: ['intubation-en-urgence-dun-adulte-hors-bloc-operatoire', 'wpdmdl=103152'],
  sepsis: ['prise-en-charge-du-sepsis-du-nouveau-ne-de-lenfant-et-de-ladulte', 'wpdmdl=75093'],
  urgences_obstetricales: ['prise-en-charge-des-urgences-obstetricales-en-medecine-durgence', 'wpdmdl=36656'],
  anaphylaxie: ['diagnostic-et-prise-en-charge-des-reactions-dhypersensibilite-immediate-perioperatoires', 'wpdmdl=103153'],
  preeclampsie: ['prise-en-charge-de-la-patiente-avec-une-pre-eclampsie-severe', 'wpdmdl=34698'],
  hyperthermie_maligne: ['prise-en-charge-de-lhyperthermie-maligne', 'wpdmdl=24495'],
  anticoag_urgence: ['gestion-de-lanticoagulation-dans-un-contexte-durgence', 'wpdmdl=62045'],
  traumatisme_abdominal: ['traumatisme-abdominal-grave-de-ladulte-les-48-premieres-heures', 'wpdmdl=24463'],
  sedation_reanimation: ['sedation-et-analgesie-en-reanimation-nouveau-ne-exclu', 'Texte_court_Sedation-et-analgesie-en-reanimation'],
  sedation_urgences: ['sedation-analgesie-structure-durgence', '2_AFAR_Sedation-analgesie-en-structure-d-urgence'],
  vni: ['ventilation-non-invasive', 'Ventilation-Non-Invasive-au-cours-del-insuffisance-respiratoire-aigue'],
  aap_urgence: ['gestion-perioperatoire-des-patients-sous-aap-en-urgence', 'wpdmdl=34414'],
  curares: ['curarisation-et-decurarisation-en-anesthesie', '2_RFE-CURARE-3'],
  remplissage: ['choix-du-solute-pour-le-remplissage-vasculaire-en-situation-critique', 'wpdmdl=35406'],
  traumatisme_membre: ['prise-en-charge-des-patients-presentant-un-traumatisme-severe-de-membres', 'wpdmdl=30307'],
  voies_aeriennes_enfant: ['gestion-des-voies-aeriennes-de-lenfant', 'rfe-gestion-des-voies-aeriennes-de-lenfant'],
  intubation_difficile_adulte: ['actualisation-de-recommandations-intubation-difficile-et-extubation-en-anesthesie-chez-ladulte', 'RFE-ANREA-Intubation-difficile-et-extubation-en-anesthesie-chez-l-adulte'],
  traumatisme_pelvien: ['prise-charges-traumatises-pelviens-graves-a-phase-precoce-24-premieres-heures', 'rfe-prise-en-charge-des-traumatises-pelviens-graves-a-la-phase-precoce'],
  traumatisme_thoracique: ['traumatisme-thoracique-prise-en-charge-des-48-premieres-heures', '2_AFAR_Traumatisme-thoracique'],
  traumatisme_cranien: ['prise-en-charge-neurochirurgicales-des-traumatismes-cranio-encephaliques-de-ladulte-et-de-lenfant-a-la-phase-initiale', 'wpdmdl=123224'],
  traumatisme_vertebromedullaire: ['prise-en-charge-des-patients-presentant-ou-a-risque-de-traumatisme-vertebromedullaire', 'rfe-trauma-vertebro-medulaire'],
  intubation_reanimation: ['intubation-et-extubation-du-patient-de-reanimation', 'Intubation-et-extubation-du-patient-en-reanimation-ANREA'],
  traumatisme_cranien_leger: ['prise-en-charge-des-patients-presentant-un-traumatisme-cranien-leger-de-ladulte', 'wpdmdl=37891'],
  lat_soins_critiques: ['decisions-de-limitation-et-darret-de-traitements-lat-en-soins-critiques-de-ladulte', 'wpdmdl=123089'],
  sdra: ['recommandations-prise-charge-sdra', '2_Recos-SDRA'],
  pavm: ['pneumonies-associees-aux-soins-de-reanimation', 'Pneumonies-associees-au-soins-de-reanimation-ANREA'],
  tracheotomie: ['tracheotomie-en-reanimation', 'Tracheotomie-en-reanimation-ANREA'],
  nutrition: ['nutrition-artificielle-en-reanimation', 'AFAR_Nutrition-artificielle-en-reanimation'],
  eer: ['epuration-extrarenale-en-reanimation-adulte-et-pediatrique', 'REANIMATION_epuration-extrarenale-en-reanimation-adulte-et-pediatrique'],
  ira: ['insuffisance-renale-aigue', 'ANREA_132_RFE-IRA'],
  ih: ['insuffisance-hepatique-en-soins-critiques', 'RFE-IH-soins-critiques'],
  epanchement_pleural: ['epanchement-pleural-liquidien-de-ladulte-en-soins-critiques', 'wpdmdl=50053'],
  anemie: ['gestion-et-prevention-de-lanemie-hors-hemorragie-aigue-chez-le-patient-adulte-de-soins-critiques', 'wpdmdl=24462'],
  hypothermie: ['prevention-de-lhypothermie-peroperatoire-accidentelle-au-bloc-operatoire-chez-ladulte', 'RFE-Hypothermie'],
  nvpo: ['prise-en-charge-des-nausees-et-vomissements-postoperatoires', 'Prise-en-charge-des-nausees-et-vomissements-postoperatoires'],
  aap_programmee: ['gestion-agents-antiplaquettaires-procedure-invasive-programmee', 'Gestion-des-agents-antiplaquettaires-pour-une-procedure-invasive-programmee'],
  mtev_perioperatoire: ['prevention-de-la-maladie-thromboembolique-veineuse-peri-operatoire', '240516-Txt-definitif'],
  glycemie: ['controle-de-la-glycemie-en-reanimation-et-en-anesthesie', '2b_AFAR_Contrele-de-la-glycemie'],
  mal_epileptique: ['prise-en-charge-en-situation-durgence-et-en-reanimation-des-etats-de-mal-epileptiques', '3_REANIMATION_Prise-en-charge'],
  allergie_prevention: ['prevention-du-risque-allergique-peranesthesique-2', '2_AFAR_Prevention-du-risque-allergique-peranesthesique'],
  antibioprophylaxie: ['antibioprophylaxie-en-chirurgie-et-medecine-interventionnelle/', 'wpdmdl=68362'],
  controle_temperature: ['controle-cible-de-la-temperature-en-reanimation', 'rfe-controle-cible-de-la-temperature-en-reanimation'],
  tih: ['diagnostic-et-prise-en-charge-dune-thrombopenie-induite-par-lheparine', 'propositions-tih-gihp-gfht-sfar'],
  civd: ['coagulations-intra-vasculaires-disseminees-civd-en-reanimation', '86-civdccons'],
  eclsa: ['indications-de-lassistance-circulatoire-dans-le-traitement-des-arrets-cardiaques-refractaires', '2_AFAR_Recommandations-sur-les-indications-de-lassistance-circulatoire'],
  transport_intrahospitalier: ['transport-intrahospitalier-des-patients-a-risque-vital', '2_AFAR_Transport-intrahospitalier-des-patients-a-risque-vital'],
  transfusion_plasma: ['transfusion-de-plasma-therapeutique-produits-indications', '2_HAS_Texte-court-ransfusion-de-plasma-therapeutique'],
  sevrage_vm: ['sevrage-de-la-ventilation-mecanique', '2_SFAR_Sevrage-de-la-ventilation-mecanique'],
  asthme_aigu_grave: ['prise-en-charge-des-crises-dasthme-aigues-graves-de-ladulte-et-de-lenfant-a-lexclusion-du-nourrisson', 'REANIMATION_Prise-en-charge-des-crises-dasthme-aigues-graves'],
  pancreatite: ['pancreatite-aigue-grave-du-patient-adulte-en-soins-critiques', 'wpdmdl=35411'],
  corticotherapie: ['corticotherapie-au-cours-du-choc-septique-et-du-sdra', '2_SFAR_Corticotherapie-au-cours-du-choc-septique-et-du-SDRA'],
  antibiotherapie_probabiliste: ['antibiotherapie-probabiliste-des-etats-septiques-graves', '2_AFAR_Antibiotherapie-probabiliste-des-etats-septiques-graves'],
  hsa: ['hemorragie-sous-arachnoidienne-hsa-grave', '2a_SFAR_texte-court_Hemorragies-sous-arachnoidienne'],
  sepsis_hemodynamique: ['prise-en-charge-hemodynamique-du-sepsis-grave-nouveau-ne-exclu', '2a_TEXTE-COURT_Prise-en-charge-hemodynamique-du-sepsis-grave'],
  securisation_proc: ['securisation-des-procedures-a-risques-en-reanimation-risque-infectieux-exclu', '2a_AFAR_Texte_court_Securisation-des-procedures-a-risques-en-reanimation']
};
LIBRARY.forEach(function(item){
  item.fiche_key = null;
  Object.keys(FICHE_HREF_MATCH).forEach(function(k){
    FICHE_HREF_MATCH[k].forEach(function(needle){
      if((item.href||'').indexOf(needle) !== -1 || (item.direct_pdf_url||'').indexOf(needle) !== -1){
        item.fiche_key = k;
      }
    });
  });
});

var DOC_META = {
  anticoagulants: {
    key: 'anticoagulants',
    badge: 'GRADE',
    title: "Anticoagulants & procédure invasive",
    short: "Gestion péri-procédurale des anticoagulants pour une procédure invasive programmée.",
    society: "SFAR / GIHP — RFE 2026",
    version: "20 avril 2026",
    validated: "CA SFAR le 18/03/2026",
    methodology: "GRADE",
    pages: 19,
    url: "https://sfar.org/wp-content/uploads/2026/04/RFE-20.4.2026-deifinitif-et-validei.pdf"
  },
  ecbu: {
    key: 'ecbu',
    badge: 'HAS · RCF',
    title: "ECBU pré-urologique & colonisation",
    short: "Place de l'ECBU avant une prise en charge urologique et modalités de traitement d'une colonisation.",
    society: "AFU / CIAFU — partenaire SFAR",
    version: "Janvier 2026",
    validated: "publiée sfar.org le 04/03/2026",
    methodology: "HAS (RCF)",
    pages: 5,
    url: "https://www.urofrance.org/wp-content/uploads/2026/03/Reco_ECBU_Synthese_23.02.2023_MEL.pdf"
  },
  choc_hemorragique: {
    key: 'choc_hemorragique',
    badge: 'GRADE',
    title: "Réanimation du choc hémorragique",
    short: "Prise en charge du choc hémorragique à la phase précoce, pré- et intra-hospitalière (hors hémorragie digestive et obstétricale).",
    society: "SFAR / SRLF / SFMU / GEHT — RFE 2014",
    version: "Validée CA SFAR 12/09/2014",
    validated: "publiée le 2 février 2015",
    methodology: "GRADE",
    pages: 4,
    url: "https://sfar.org/wp-content/uploads/2015/09/2_AFAR_Recommandations-sur-la-reanimation-du-choc-hemorragique.pdf"
  },
  intubation_urgence: {
    key: 'intubation_urgence',
    badge: 'GRADE',
    title: "Intubation en urgence hors bloc & hors soins critiques",
    short: "Intubation trachéale de l'adulte en situation d'urgence, hors bloc opératoire et hors unité de soins critiques.",
    society: "SFAR / SFMU — RFE 2024",
    version: "Validée CA SFAR 03/12/2024",
    validated: "CA SFMU 21/11/2024",
    methodology: "GRADE",
    pages: 5,
    url: "https://sfar.org/download/intubation-en-urgence-dun-adulte-hors-bloc-operatoire-et-hors-unite-des-soins-critiques/?wpdmdl=103152"
  },
  sepsis: {
    key: 'sepsis',
    badge: 'HAS',
    title: "Sepsis — repérage & parcours de soins",
    short: "Définitions, scores diagnostiques (adulte/enfant), messages clés du parcours de soins, et l'intégralité des recommandations Surviving Sepsis Campaign 2021 (adulte) et 2020 (enfant/nouveau-né) validées pour le contexte français (~147 recommandations).",
    society: "HAS / SRLF / SFAR / SFMU & 16 sociétés — RBP 2025",
    version: "Validée Collège HAS 29/01/2025",
    validated: "RPC",
    methodology: "GRADE (RPC)",
    pages: 14,
    url: "https://sfar.org/download/prise-en-charge-du-sepsis-du-nouveau-ne-de-lenfant-et-de-ladulte-recommandations-pour-un-parcours-de-soins-integre/?wpdmdl=75093"
  },
  urgences_obstetricales: {
    key: 'urgences_obstetricales',
    badge: 'RPP',
    title: "Urgences obstétricales en médecine d'urgence",
    short: "Accouchement imminent, hémorragie du post-partum, MAP, pré-éclampsie/éclampsie, traumatisme, imagerie, arrêt cardiaque et formation — hors structure spécialisée.",
    society: "SFMU / SFAR / CNGOF — RPP 2022",
    version: "Validée CA SFAR 04/03/2022",
    validated: "CA SFMU 31/03/2022",
    methodology: "Avis d'experts (RPP)",
    pages: 5,
    url: "https://sfar.org/download/prise-en-charge-des-urgences-obstetricales-en-medecine-durgence/?wpdmdl=36656"
  },
  anaphylaxie: {
    key: 'anaphylaxie',
    badge: 'GRADE',
    title: "Anaphylaxie périopératoire",
    short: "Bilan diagnostique post-réaction (tryptase, histamine, IgE spécifiques, tests cutanés, tests de provocation), facteurs de risque (latex, bêtalactamines/céfazoline, pholcodine, mastocytose) et traitement de l'hypersensibilité immédiate périopératoire par grade de gravité (adrénaline, remplissage, réfractaire, chirurgie urgente).",
    society: "SFAR / SFA — RFE 2025",
    version: "2025",
    validated: "GRADE",
    methodology: "GRADE",
    pages: 13,
    url: "https://sfar.org/download/diagnostic-et-prise-en-charge-des-reactions-dhypersensibilite-immediate-perioperatoires/?wpdmdl=103153"
  },
  preeclampsie: {
    key: 'preeclampsie',
    badge: 'GRADE',
    title: "Pré-éclampsie sévère",
    short: "Définition, signes de gravité, traitement antihypertenseur (algorithme inclus), sulfate de magnésium, critères d'arrêt de grossesse, anesthésie et prise en charge postpartum.",
    society: "SFAR / CNGOF — RFE 2020",
    version: "Validée CRC SFAR 08/07/2020",
    validated: "CA SFAR 04/09/2020",
    methodology: "GRADE",
    pages: 6,
    url: "https://sfar.org/download/rfe-prise-en-charge-de-la-patiente-avec-une-pre-eclampsie-severe-2/?wpdmdl=34698"
  },
  hyperthermie_maligne: {
    key: 'hyperthermie_maligne',
    badge: 'RPP',
    title: "Hyperthermie maligne",
    short: "Dépistage, diagnostic de sensibilité, conduite anesthésique chez un patient à risque, et protocole complet de traitement de la crise (affiche + reconstitution du dantrolène).",
    society: "SFAR — RPP 2019 (actualisation 2013)",
    version: "Validée Comité Référentiels 30/05/2018",
    validated: "CA SFAR 21/06/2018",
    methodology: "Avis d'experts (RPP)",
    pages: 6,
    url: "https://sfar.org/download/rpp-hyperthermie-maligne/?wpdmdl=24495"
  },
  anticoag_urgence: {
    key: 'anticoag_urgence',
    badge: 'GRADE',
    title: "Anticoagulation en contexte d'urgence",
    short: "Hémorragie sous anticoagulant (AVK, dabigatran, AOD anti-Xa, héparines, fondaparinux), surdosages asymptomatiques, procédures invasives non programmées et thrombolyse de l'AVC ischémique sous anticoagulant.",
    society: "SFMU / SFAR / GIHP / SFTH — RFE 2024",
    version: "2024",
    validated: "GRADE",
    methodology: "GRADE",
    pages: 9,
    url: "https://sfar.org/download/gestion-de-lanticoagulation-dans-un-contexte-durgence/?wpdmdl=62045"
  },
  traumatisme_abdominal: {
    key: 'traumatisme_abdominal',
    badge: 'GRADE',
    title: "Traumatisme abdominal grave de l'adulte",
    short: "Stratégie diagnostique (examen clinique, FAST, scanner), stratégie thérapeutique (laparotomie, damage control, cœlioscopie, traitement non-opératoire, angio-embolisation) et modalités précoces de surveillance des 48 premières heures. Fiche réflexe préhospitalière et algorithme hospitalier inclus.",
    society: "SFAR / SFMU (AFC, AFU, SFRI, EVG) — RFE 2019",
    version: "2019",
    validated: "CA SFAR 20/06/2019, CA SFMU 16/09/2019",
    methodology: "GRADE",
    pages: 5,
    url: "https://sfar.org/download/rfe-urgence-trauma-abdominal/?wpdmdl=24463"
  },
  sedation_reanimation: {
    key: 'sedation_reanimation',
    badge: 'GRADE',
    title: "Sédation et analgésie en réanimation",
    short: "Définitions et buts, moyens médicamenteux et non médicamenteux (hypnotiques, morphiniques, curares), outils d'évaluation (échelles de douleur/conscience, BIS), arrêt de la sédation-analgésie et syndrome de sevrage, algorithme de conduite pratique.",
    society: "SFAR / SRLF — Conférence de Consensus 2007 (publiée 2008)",
    version: "2007/2008",
    validated: "Conférence de Consensus, Paris, 15/11/2007",
    methodology: "GRADE",
    pages: 5,
    url: "https://sfar.org/wp-content/uploads/2015/10/2a_AFAR_Texte_court_Sedation-et-analgesie-en-reanimation_nouveau-ne-exclu.pdf"
  },
  sedation_urgences: {
    key: 'sedation_urgences',
    badge: 'GRADE',
    title: "Sédation et analgésie en structure d'urgence",
    short: "Pharmacologie des agents, ventilation spontanée, intubation en séquence rapide, patient intubé-ventilé, circonstances particulières (choc, neuro, respiratoire, femme enceinte, actes douloureux, CEE, patient incarcéré, afflux de victimes) et pédiatrie — extra- et intra-hospitalier.",
    society: "SFAR / SFMU — RFE 2010 (réactualisation Conférence d'experts 1999)",
    version: "2010",
    validated: "RFE 2010",
    methodology: "GRADE (adaptée, 3 niveaux)",
    pages: 14,
    url: "https://sfar.org/wp-content/uploads/2016/01/2_AFAR_Sedation-analgesie-en-structure-d-urgence.pdf"
  },
  vni: {
    key: 'vni',
    badge: 'GRADE',
    title: "Ventilation non invasive (insuffisance respiratoire aiguë)",
    short: "Indications et contre-indications de la VNI, critères cliniques d'instauration par pathologie (BPCO, OAP cardiogénique, immunodéprimé, post-opératoire, neuromusculaire, pédiatrie), moyens de mise en œuvre (interfaces, réglages, monitorage), critères d'efficacité, d'échec et effets indésirables.",
    society: "SFAR / SPLF / SRLF — Conférence de Consensus 2006",
    version: "2006",
    validated: "3e Conférence de Consensus commune, 12/10/2006",
    methodology: "GRADE",
    pages: 6,
    url: "https://sfar.org/wp-content/uploads/2015/10/2a_SFAR_texte-court_Ventilation-Non-Invasive-au-cours-del-insuffisance-respiratoire-aigue.pdf"
  },
  aap_urgence: {
    key: 'aap_urgence',
    badge: 'Propositions',
    title: "Agents antiplaquettaires en urgence",
    short: "Gestion des agents antiplaquettaires oraux (aspirine, clopidogrel, prasugrel, ticagrelor) en cas de procédure invasive non programmée ou d'hémorragie : moyens de neutralisation, durées d'interruption, conduite selon le type de procédure et la gravité de l'hémorragie.",
    society: "GIHP / GFHT — en collaboration avec la SFAR, 2018",
    version: "2018",
    validated: "Vote Delphi (n=38), accord fort",
    methodology: "Propositions (non-GRADE)",
    pages: 5,
    url: "https://sfar.org/download/gestion-perioperatoire-des-patients-sous-aap-en-urgence/?wpdmdl=34414"
  },
  curares: {
    key: 'curares',
    badge: 'GRADE',
    title: "Curarisation et décurarisation en anesthésie",
    short: "Indications de la curarisation (ventilation au masque, intubation, dispositifs supra-glottiques, chirurgie), monitorage per-opératoire, diagnostic et traitement de la curarisation résiduelle (néostigmine, sugammadex), populations spéciales (enfant, obésité, maladies neuromusculaires, ECT, insuffisance rénale/hépatique).",
    society: "SFAR — RFE 2018 (actualisation de la CC 1999)",
    version: "2018",
    validated: "Texte validé par le CA SFAR le 21/06/2018",
    methodology: "GRADE",
    pages: 12,
    url: "https://sfar.org/wp-content/uploads/2018/10/2_RFE-CURARE-3.pdf"
  },
  remplissage: {
    key: 'remplissage',
    badge: 'GRADE',
    title: "Remplissage vasculaire — choix du soluté",
    short: "Choix du type de soluté de remplissage vasculaire (colloïdes vs cristalloïdes, type de cristalloïde) au cours du sepsis/choc septique, du choc hémorragique, chez le patient cérébrolésé et en péripartum. Tableau de composition des solutés inclus.",
    society: "SFAR / SFMU — RFE 2021",
    version: "2021",
    validated: "CA SFAR 19/05/2021, CA SFMU 29/06/2021",
    methodology: "GRADE",
    pages: 5,
    url: "https://sfar.org/download/choix-du-solute-pour-le-remplissage-vasculaire-en-situation-critique/?wpdmdl=35406"
  },
  traumatisme_membre: {
    key: 'traumatisme_membre',
    badge: 'GRADE',
    title: "Traumatisme sévère de membre(s)",
    short: "Orientation vers un centre spécialisé (critères de Vittel), contrôle du saignement (garrot), dépistage d'une lésion vasculaire, moment de l'ostéosynthèse (stabilisation précoce vs damage control orthopaedic surgery), sauvetage de membre vs amputation, prévention infectieuse et thromboembolique, syndrome des loges, rhabdomyolyse, embolie graisseuse, analgésie.",
    society: "SFAR / SFMU, avec SOFCOT / SCVE / SSA — RFE 2020",
    version: "2020",
    validated: "CRC 16/06/2020, CA SFAR 25/08/2020, CA SFMU 15/09/2020",
    methodology: "GRADE",
    pages: 9,
    url: "https://sfar.org/download/prise-en-charge-des-patients-presentant-un-traumatisme-severe-de-membres/?wpdmdl=30307"
  },
  voies_aeriennes_enfant: {
    key: 'voies_aeriennes_enfant',
    badge: 'GRADE',
    title: "Voies aériennes de l'enfant",
    short: "Dispositifs supraglottiques, sondes à ballonnet, vidéolaryngoscopes, curares et induction en séquence rapide, extubation, enfant enrhumé — avec les 3 algorithmes complets (intubation difficile imprévue, ventilation au masque difficile, CICO). Ne s'applique pas au nouveau-né/prématuré.",
    society: "SFAR / ADARPEF — RFE 2018",
    version: "2018",
    validated: "CA SFAR 21/06/2018, CA ADARPEF 24/05/2018",
    methodology: "GRADE",
    pages: 10,
    url: "https://sfar.org/wp-content/uploads/2019/10/rfe-gestion-des-voies-aeriennes-de-lenfant.pdf"
  },
  intubation_difficile_adulte: {
    key: 'intubation_difficile_adulte',
    badge: 'GRADE',
    title: "Intubation difficile & extubation (adulte)",
    short: "Actualisation de la Conférence d'Experts Intubation difficile 2006 : vidéolaryngoscopes en intubation prévue et non prévue, techniques d'oxygénation, anesthésie et curarisation, stratégie de gestion des voies aériennes en cas d'intubation difficile non prévue, extubation à risque (facteurs de risque, leadership et décision).",
    society: "SFAR — RFE 2017",
    version: "2017",
    validated: "Texte validé par le CA SFAR le 29/06/2017",
    methodology: "GRADE",
    pages: 11,
    url: "https://sfar.org/wp-content/uploads/2017/09/RFE-ANREA-Intubation-difficile-et-extubation-en-anesthesie-chez-l-adulte.pdf"
  },
  traumatisme_pelvien: {
    key: 'traumatisme_pelvien',
    badge: 'GRADE',
    title: "Traumatisme pelvien grave",
    short: "Prise en charge à la phase précoce (24 premières heures) : préhospitalier (orientation, contention pelvienne), imagerie initiale (TDM, opacification urètre/vessie), classifications Young-Burgess et Tile, contrôle de l'hémostase (embolisation, tamponnement extrapéritonéal, fixation externe), traumatisme pelvien ouvert.",
    society: "SFMU / SFAR, avec SFR / SSA / AFU / SOFCOT / SFCD — RFE 2017",
    version: "2017",
    validated: "CA SFMU et CA SFAR le 29/06/2017",
    methodology: "GRADE",
    pages: 9,
    url: "https://sfar.org/wp-content/uploads/2019/10/rfe-prise-en-charge-des-traumatises-pelviens-graves-a-la-phase-precoce.pdf"
  },
  traumatisme_thoracique: {
    key: 'traumatisme_thoracique',
    badge: 'GRADE',
    title: "Traumatisme thoracique — 48 premières heures",
    short: "Critères de gravité et orientation, stratégie diagnostique (échographie pleuropulmonaire, TDM), support ventilatoire (VNI, ventilation protectrice), stratégies analgésiques (ALR, bloc paravertébral, péridurale), drainage pleural, chirurgie et radiologie interventionnelle, spécificités du traumatisme pénétrant.",
    society: "SFAR / SFMU, avec SFCTCV / SFR — RFE 2015",
    version: "2015",
    validated: "Disponible en ligne le 23/05/2015",
    methodology: "GRADE",
    pages: 10,
    url: "https://sfar.org/wp-content/uploads/2015/10/2_AFAR_Traumatisme-thoracique-_prise-en-charge-des-48-premieres-heures.pdf"
  },
  traumatisme_cranien: {
    key: 'traumatisme_cranien',
    badge: 'GRADE',
    title: "Traumatisme cranio-encéphalique — prise en charge neurochirurgicale",
    short: "Facteurs de mauvais pronostic (fragilité, mydriase, délai), hématomes extra-duraux et sous-duraux aigus, embarrures et brèches ostéo-durales, traumatismes pénétrants (score SPIN), désordres hydrauliques post-traumatiques, particularités pédiatriques (HED néonatal, syndrome du bébé secoué, fracture ping-pong). Annexes GOSE, mFI-5, SPIN.",
    society: "SFNC, avec SFNCP/SFNCL/ANARLF/SFAR/GFRUP/SFNR/SPILF/SOFMER — RPP 2025",
    version: "2025",
    validated: "V1.13, 19/03/2025, publiée le 19/09/2025",
    methodology: "GRADE",
    pages: 9,
    url: "https://sfar.org/download/prise-en-charge-neurochirurgicales-des-traumatismes-cranio-encephaliques-de-ladulte-et-de-lenfant-a-la-phase-initiale/?wpdmdl=123224"
  },
  traumatisme_vertebromedullaire: {
    key: 'traumatisme_vertebromedullaire',
    badge: 'GRADE',
    title: "Traumatisme vertébro-médullaire",
    short: "Immobilisation du rachis, intubation oro-trachéale (pré-hospitalière et hospitalière, avec algorithmes), objectifs hémodynamiques, filière de soins spécialisée, corticothérapie (contre-indiquée), IRM, délai chirurgical, sevrage ventilatoire, antalgie neuropathique, installation/mobilisation, sondage vésical intermittent.",
    society: "SFAR, avec ANARLF/SFCR/SFMU/SOFCOT/SOFMER/SSA — RFE 2019",
    version: "2019",
    validated: "CRC 15/05/2019, CA SFAR 24/05/2019",
    methodology: "GRADE",
    pages: 8,
    url: "https://sfar.org/download/rfe-trauma-vertebro-medulaire/?wpdmdl=24464"
  },
  intubation_reanimation: {
    key: 'intubation_reanimation',
    badge: 'GRADE',
    title: "Intubation & extubation en réanimation",
    short: "Intubation compliquée (score MACOCHA), matériel (vidéolaryngoscopes, DSG, capnographie), agents d'induction (succinylcholine, rocuronium/sugammadex), protocoles/bundles avec algorithme IOT, pré-requis et échecs de l'extubation (test de fuite, corticothérapie), gestion pratique (VNI, ONHD, kinésithérapie) avec algorithme d'extubation.",
    society: "SFAR / SRLF, avec SFMU/GFRUP/ADARPEF/SKR — RFE 2016",
    version: "2016",
    validated: "CA SRLF et CA SFAR le 17/06/2016",
    methodology: "GRADE",
    pages: 8,
    url: "https://sfar.org/wp-content/uploads/2016/09/Intubation-et-extubation-du-patient-en-reanimation-ANREA.pdf"
  },
  traumatisme_cranien_leger: {
    key: 'traumatisme_cranien_leger',
    badge: 'RPP',
    title: "Traumatisme crânien léger de l'adulte",
    short: "Stratification du risque (élevé/intermédiaire), biomarqueurs (S100B, UCH-L1+GFAP), délai de la TDM cérébrale, Doppler transcrânien, imagerie de contrôle, réversion des anticoagulants et antiplaquettaires, critères de retour à domicile, filière de soins et information de sortie (fiche patient incluse).",
    society: "SFMU, avec SFAR/SFBC/SFR/SOFMER — RPP 2022",
    version: "2022",
    validated: "CA SFMU 24/05/2022, CA SFAR 15/09/2022",
    methodology: "Avis d'experts (RPP)",
    pages: 8,
    url: "https://sfar.org/download/prise-en-charge-des-patients-presentant-un-traumatisme-cranien-leger-de-ladulte/?wpdmdl=37891"
  },
  lat_soins_critiques: {
    key: 'lat_soins_critiques',
    badge: 'GRADE',
    title: "Décisions de LAT en soins critiques",
    short: "Prérequis et modalités d'une décision de limitation/arrêt de traitements (réunions pluriprofessionnelles, recherche des volontés du patient, procédure collégiale), protocole de sédation profonde et continue (posologies, échelles RASS/BPS/RDOS), relations avec les proches (accompagnement, communication, structure d'éthique clinique).",
    society: "SFAR, avec SOFMER — RFE 2025",
    version: "2025",
    validated: "Comité des Référentiels Cliniques SFAR 10/05/2025, CA SFAR 15/07/2025",
    methodology: "GRADE",
    pages: 9,
    url: "https://sfar.org/download/decisions-de-limitation-et-darret-de-traitements-lat-en-soins-critiques-de-ladulte/?wpdmdl=123089"
  },
  sdra: {
    key: 'sdra',
    badge: 'GRADE',
    title: "SDRA — Ventilation mécanique",
    short: "Traduction résumée officielle SFAR du guideline international ATS/ESICM/SCCM 2017 : volume courant/pression de plateau, décubitus ventral, VOHF, PEP élevée, manœuvres de recrutement, ECMO.",
    society: "SFAR (trad. ATS/ESICM/SCCM) — 2017-2018",
    version: "2018",
    validated: "Comité des Référentiels Cliniques SFAR 12/12/2017, CA SFAR 02/02/2018",
    methodology: "GRADE",
    pages: 3,
    url: "https://sfar.org/wp-content/uploads/2018/03/2_Recos-SDRA.pdf"
  },
  pavm: {
    key: 'pavm',
    badge: 'GRADE',
    title: "Pneumonies associées aux soins",
    short: "Prévention multimodale (dont décontamination digestive sélective), diagnostic (limites du CPIS et des biomarqueurs), traitement antibiotique probabiliste et documenté (schémas thérapeutiques détaillés), spécificités BPCO et pédiatrie.",
    society: "SFAR / SRLF, avec ADARPEF/GFRUP — RFE 2017",
    version: "2017",
    validated: "CA SFAR 29/06/2017, CA SRLF 08/06/2017",
    methodology: "GRADE",
    pages: 6,
    url: "https://sfar.org/wp-content/uploads/2017/09/Pneumonies-associees-au-soins-de-reanimation-ANREA.pdf"
  },
  tracheotomie: {
    key: 'tracheotomie',
    badge: 'GRADE',
    title: "Trachéotomie en réanimation",
    short: "Indications et contre-indications (délai ≥4 jours, situations à haut risque), technique percutanée par dilatation unique progressive, fibroscopie et échographie cervicale, protocoles détaillés (réalisation, soins post-trachéotomie, décanulation avec algorithme séquentiel).",
    society: "SRLF / SFAR, avec SFMU/SFORL — RFE 2016",
    version: "2016",
    validated: "CA SFAR 15/12/2016, CA SRLF 13/12/2016",
    methodology: "GRADE",
    pages: 5,
    url: "https://sfar.org/wp-content/uploads/2017/01/Tracheotomie-en-reanimation-ANREA.pdf"
  },
  nutrition: {
    key: 'nutrition',
    badge: 'GRADE',
    title: "Nutrition artificielle en réanimation",
    short: "Stratégie générale (entérale précoce vs. parentérale), objectifs caloriques/protéiques, nutrition entérale (sonde, position, prokinétiques, mélanges) et parentérale, pharmaconutrition, particularités par terrain (IRC épuré, insuffisant hépatique, SDRA, obèse, dénutrition sévère, brûlé) et pédiatriques — 71 recommandations.",
    society: "SFAR / SRLF / SFNEP — RFE 2014",
    version: "2014",
    validated: "Recommandations validées février 2013",
    methodology: "GRADE",
    pages: 9,
    url: "https://sfar.org/wp-content/uploads/2015/10/2_AFAR_Nutrition-artificielle-en-reanimation.pdf"
  },
  eer: {
    key: 'eer',
    badge: 'GRADE',
    title: "Épuration extrarénale en réanimation",
    short: "Indications et timing de l'EER (précoce vs. différée), modalités techniques (continue vs. intermittente, dose de dialyse, anticoagulation régionale au citrate vs. héparine, gestion du circuit par phase), particularités pédiatriques — 78 recommandations, adulte et pédiatrique.",
    society: "SRLF, avec SFAR/GFRUP/SFD — RFE 2014",
    version: "2014",
    validated: "Publication Réanimation 2014, DOI 10.1007/s13546-014-0917-6",
    methodology: "GRADE",
    pages: 7,
    url: "https://sfar.org/wp-content/uploads/2015/10/2_REANIMATION_epuration-extrarenale-en-reanimation-adulte-et-pediatrique.pdf"
  },
  ira: {
    key: 'ira',
    badge: 'GRADE',
    title: "Insuffisance rénale aiguë périopératoire",
    short: "Diagnostic et gravité (KDIGO/pRIFLE), diagnostic précoce (biomarqueurs, Doppler rénal), évaluation du risque, prévention non spécifique (HEA, PAM, remplissage), gestion des agents néphrotoxiques, stratégies pharmacologiques, nutrition et évaluation de la récupération rénale — 33 recommandations, adulte et pédiatrique.",
    society: "SFAR / SRLF, avec GFRUP/SFN — RFE 2015",
    version: "2015",
    validated: "CA SFAR 19/06/2015, CA SRLF 06/08/2015",
    methodology: "GRADE",
    pages: 5,
    url: "https://sfar.org/wp-content/uploads/2016/05/ANREA_132_RFE-IRA-.pdf"
  },
  ih: {
    key: 'ih',
    badge: 'GRADE',
    title: "Insuffisance hépatique en soins critiques",
    short: "Insuffisance hépatique aiguë (bilan étiologique, N-acétylcystéine, transplantation) et insuffisance hépatique sur cirrhose/ACLF (admission en soins critiques, IRA et syndrome hépatorénal, sepsis, albumine, hémorragie digestive et TIPS, hémostase, avis spécialisé) — 19 recommandations, CLIF-SOFA et grade ACLF en annexe.",
    society: "SFAR / AFEF — RFE 2018",
    version: "2018",
    validated: "Publié 2018",
    methodology: "GRADE",
    pages: 5,
    url: "https://sfar.org/wp-content/uploads/2018/09/RFE-IH-soins-critiques.pdf"
  },
  epanchement_pleural: {
    key: 'epanchement_pleural',
    badge: 'RPP',
    title: "Épanchement pleural liquidien",
    short: "Diagnostic échographique, indication de ponction/drainage, technique de pose (voie d'abord, calibre, gestion des antithrombotiques), analgésie, surveillance post-drainage et procédure de retrait du drain — 25 recommandations (avis d'experts, accord fort), hors pleurésie purulente/hémothorax/épanchement néoplasique.",
    society: "SFAR / SFMU / SPLF / SFCTCV — RPP 2023",
    version: "2023",
    validated: "CRC SFAR 10/04/2023, CA SFAR 20/04/2023, CA SFCTCV/SFMU 21/06/2023, CA SPLF 18/07/2023",
    methodology: "Avis d'experts (RPP)",
    pages: 4,
    url: "https://sfar.org/download/epanchement-pleural-liquidien-de-ladulte-en-soins-critiques/?wpdmdl=50053"
  },
  anemie: {
    key: 'anemie',
    badge: 'GRADE',
    title: "Anémie en soins critiques",
    short: "Prévention non pharmacologique (réduction des prélèvements sanguins), seuils transfusionnels restrictifs par contexte clinique (Hb 7,0-8,0 g/dL selon la situation), politique de transfusion unitaire, traitement par érythropoïétine et gestion du fer — 10 recommandations, hors hémorragie aiguë et anémies chroniques.",
    society: "SFAR / SRLF, avec SFTS/SFVTT — RFE 2019",
    version: "2019",
    validated: "CA SFAR 20/06/2019, CA SRLF 26/06/2019",
    methodology: "GRADE",
    pages: 3,
    url: "https://sfar.org/download/rfe-gestion-anemie-reanimation/?wpdmdl=24462"
  },
  hypothermie: {
    key: 'hypothermie',
    badge: 'GRADE',
    title: "Prévention de l'hypothermie peropératoire",
    short: "Seuil cible de température centrale (≥36,5°C), réchauffement cutané actif (pré-warming, per-anesthésie, SSPI), réchauffement des fluides IV/produits sanguins/liquides d'irrigation, risques (brûlures, infection) et stratégie chronologique par phase — 14 recommandations, première RFE française sur ce sujet.",
    society: "SFAR — RFE 2018",
    version: "2018",
    validated: "CRC SFAR 12/06/2018, CA SFAR 21/06/2018",
    methodology: "GRADE",
    pages: 3,
    url: "https://sfar.org/wp-content/uploads/2018/09/2_RFE-Hypothermie-Version-Finale-_-Validee-CRC120618.pdf"
  },
  nvpo: {
    key: 'nvpo',
    badge: 'GRADE',
    title: "NVPO — Nausées et vomissements postopératoires",
    short: "Facteurs de risque et scores prédictifs (Apfel, Koivuranta), sétrons, dexaméthasone, dropéridol, antagonistes NK1 (aprépitant), traitements alternatifs, stratégies de prévention multimodale et algorithme décisionnel par niveau de risque, particularités pédiatriques et en chirurgie ambulatoire — conférence d'experts, ~60 recommandations.",
    society: "SFAR — Conférence d'experts 2007/2008",
    version: "2008",
    validated: "Publié Ann Fr Anesth Réanim 2008;27:866-878",
    methodology: "GRADE",
    pages: 7,
    url: "https://sfar.org/wp-content/uploads/2015/10/2_AFAR_Prise-en-charge-des-nausees-et-vomissements-postoperatoires.pdf"
  },
  aap_programmee: {
    key: 'aap_programmee',
    badge: 'PROPOSITIONS',
    title: "Agents antiplaquettaires — procédure invasive programmée",
    short: "Classification du risque hémorragique de la procédure (faible/intermédiaire/élevé) et du risque thrombotique du patient, délais d'arrêt par molécule (J-3 aspirine, J-5 clopidogrel/ticagrélor, J-7 prasugrel), gestion selon l'indication, bithérapie et stent coronaire, anesthésie locorégionale rachidienne et blocs périphériques, chirurgie de pontage aortocoronaire — complète la fiche dédiée à la procédure non programmée/l'hémorragie.",
    society: "GIHP & GFHT, en collaboration avec la SFAR — Propositions 2018",
    version: "2018",
    validated: "Publié Anesth Reanim 2018 (ANREA-314), doi 10.1016/j.anrea.2018.01.002",
    methodology: "Propositions (vote GIHP/GFHT, n=37 — non GRADE)",
    pages: 7,
    url: "https://sfar.org/wp-content/uploads/2018/03/2_Gestion-des-agents-antiplaquettaires-pour-une-procedure-invasive-programmee.pdf"
  },
  mtev_perioperatoire: {
    key: 'mtev_perioperatoire',
    badge: 'GRADE',
    title: "Prévention de la MTEV péri-opératoire",
    short: "Actualisation 2024 des recommandations SFAR 2011 : implémentation de protocoles, facteurs de risque liés au patient, thromboprophylaxie pharmacologique par type de chirurgie (orthopédie/traumatologie, abdominopelvienne, carcinologique, vasculaire), délai d'introduction et anesthésie locorégionale, compression pneumatique intermittente, filtre cave, insuffisance rénale, obésité, pédiatrie, réanimation, acide tranexamique, monitorage biologique, TVP distale — 77 recommandations et schéma de synthèse.",
    society: "GIHP, en collaboration avec la SFAR, la SFTH et la SFMV — RFE 2024",
    version: "16.5.2024",
    validated: "Validation SFAR 30/04/2024, SFTH 23/02/2024, SFMV janvier 2024",
    methodology: "GRADE",
    pages: 14,
    url: "https://sfar.org/wp-content/uploads/2024/05/240516-Txt-definitif-.pdf"
  },
  glycemie: {
    key: 'glycemie',
    badge: 'NGP/ACCORD',
    title: "Contrôle de la glycémie en réanimation et en anesthésie",
    short: "Diagnostic et risques de l'hypoglycémie, cibles de contrôle glycémique en réanimation et en périopératoire, réalisation pratique (apports glucidiques, modalités de surveillance, algorithmes et protocoles), spécificités du patient diabétique et en pédiatrie — 74 recommandations cotées sur deux axes indépendants (niveau de preuve et force de l'accord d'experts), précédées d'un rappel de physiologie/physiopathologie du glucose et de l'insuline.",
    society: "SFAR & SRLF, avec Alfediam/Adarpef/Gefrup/Sbar/SFNEP/SIZ — RFE 2009",
    version: "2009 (validée juillet 2008)",
    validated: "Publié Ann Fr Anesth Reanim 2009;28:410-415, doi 10.1016/j.annfar.2009.02.020",
    methodology: "NGP + Accord (deux axes indépendants, non GRADE numérique)",
    pages: 8,
    url: "https://sfar.org/wp-content/uploads/2015/10/2b_AFAR_Contrele-de-la-glycemie-en-reanimation-et-en-anesthesie_une-reactualisation-necessaire.pdf"
  },
  mal_epileptique: {
    key: 'mal_epileptique',
    badge: 'ACCORD',
    title: "États de mal épileptiques — prise en charge d'urgence",
    short: "Définitions et classification opérationnelle de l'EME (8 formes cliniques par degré d'urgence pronostique), diagnostic différentiel (pseudo état de mal), EEG, enquête étiologique, facteurs pronostiques, prise en charge générale, schéma thérapeutique et posologies par molécule (benzodiazépines, phénobarbital, valproate, (fos)phénytoïne), particularités pédiatriques — adulte ET enfant, nouveau-né exclu.",
    society: "SRLF, avec le GFRUP et la SFMU — RFE 2009",
    version: "2008/2009",
    validated: "Publié Réanimation 2009;18:4-12, doi 10.1016/j.reaurg.2008.07.008",
    methodology: "Accord fort/faible (méthode RAND/UCLA, non GRADE)",
    pages: 14,
    url: "https://sfar.org/wp-content/uploads/2015/10/3_REANIMATION_Prise-en-charge-en-situation-durgence-et-en-reanimation-des-etats-de-mal-epileptiques-de-ladulte-et-de-lenfant.pdf"
  },
  allergie_prevention: {
    key: 'allergie_prevention',
    badge: 'NP (preuve)',
    title: "Prévention du risque allergique péranesthésique",
    short: "Réalité du risque et substances responsables (curares en tête), mécanismes et physiopathologie du choc, bilan diagnostique biologique (histamine, tryptase, IgE spécifiques) et cutané (tests cutanés, tableaux de concentrations de référence), facteurs favorisants et croisements allergéniques, place du bilan allergologique préanesthésique, prévention primaire/secondaire et choix de la technique — complète la fiche « Anaphylaxie 2025 » (traitement aigu) déjà publiée sur ce site.",
    society: "SFAR & Société française d'allergologie (SFA) — RFE 2011",
    version: "2011 (actualisation 2001/2002)",
    validated: "Publié Ann Fr Anesth Reanim 2011;30:212-222, doi:10.1016/j.annfar.2010.12.002",
    methodology: "Niveaux de preuve NP1-4 (argumentaire) — pas de grade par recommandation",
    pages: 9,
    url: "https://sfar.org/wp-content/uploads/2015/10/2_AFAR_Prevention-du-risque-allergique-peranesthesique.pdf"
  },
  antibioprophylaxie: {
    key: 'antibioprophylaxie',
    badge: 'GRADE',
    title: "Antibioprophylaxie — recommandations générales",
    short: "Les 11 recommandations générales (Champ 1) de la RFE : délai d'administration avant l'incision, réinjection peropératoire et rythme par molécule, durée (limitée à la période peropératoire dans la grande majorité des cas), adaptation posologique chez le patient obèse (céphalosporines, amoxicilline-clavulanate, clindamycine, gentamicine, vancomycine, teicoplanine), et dépistage/antibioprophylaxie ciblée chez le patient colonisé à E-BLSE avant chirurgie colo-rectale. Périmètre volontairement limité : exclut les Champs 2-3 (18 tableaux disciplinaires adultes et pédiatriques de posologie par procédure, ~85 pages) — voir le texte intégral pour le choix et la dose d'une procédure donnée.",
    society: "SFAR / SPILF (32 sociétés savantes associées) — RFE 2024",
    version: "V3.0 du 04/05/2026 (V1.0 originale 08/12/2023)",
    validated: "CA SFAR 30/06/2023 (Champs 1-2) ; CA SFAR 20/05/2026 (Champ 3 pédiatrique)",
    methodology: "GRADE",
    pages: 4,
    url: "https://sfar.org/download/antibioprophylaxie-en-chirurgie-et-medecine-interventionnelle/?wpdmdl=68362"
  },
  controle_temperature: {
    key: 'controle_temperature',
    badge: 'GRADE',
    title: "Contrôle ciblé de la température en réanimation",
    short: "30 recommandations GRADE réparties en 6 champs cliniques (adulte + variantes pédiatriques) : arrêt cardiaque (cible 32-36°C selon le rythme initial), traumatisme crânien grave (35-37°C, échec de la neuroprotection par hypothermie profonde), AVC grave et autres hémorragies cérébrales, état de mal épileptique réfractaire et méningite/méningo-encéphalite, états de choc (cardiogénique, septique), et modalités pratiques de mise en œuvre (méthodes asservies, sites de mesure, surveillance des complications). Hors nouveau-nés.",
    society: "RFE commune SRLF-SFAR, avec l'ANARLF, le GFRUP, la SFMU et la SFNV — 2016",
    version: "2016",
    validated: "CA SRLF et CA SFAR le 18/02/2016 ; publié Anesth Reanim. 2019;5:49-66, doi 10.1016/j.anrea.2018.10.004",
    methodology: "GRADE",
    pages: 6,
    url: "https://sfar.org/wp-content/uploads/2019/10/rfe-controle-cible-de-la-temperature-en-reanimation.pdf"
  },
  tih: {
    key: 'tih',
    badge: 'ACCORD',
    title: "Thrombopénie induite par l'héparine (TIH)",
    short: "12 questions, 40 propositions (toutes à accord fort, pas de grade GRADE) : stades et niveaux de risque, surveillance de la numération plaquettaire, circonstances évocatrices et score des 4T, diagnostic biologique (anticorps anti-FP4, tests fonctionnels), prise en charge initiale, choix et posologie des anticoagulants de substitution (danaparoïde, argatroban, bivalirudine, fondaparinux, AOD, AVK), chirurgie hors cardiaque et chirurgie cardiaque avec/sans CEC, médecine/obstétrique/pédiatrie, prévention d'une récidive.",
    society: "GIHP & GFHT, en collaboration avec la SFAR — Propositions 2019",
    version: "2019 (actualise la conférence d'experts SFAR de 2002)",
    validated: "Vote du groupe GIHP/GFHT (n=32 participants)",
    methodology: "Accord fort (méthode GIHP/GFHT, pas de grade GRADE)",
    pages: 9,
    url: "https://sfar.org/download/propositions-tih-gihp-gfht-sfar/?wpdmdl=24461"
  },
  civd: {
    key: 'civd',
    badge: 'PREUVE/FORCE',
    title: "CIVD en réanimation",
    short: "Coagulation intravasculaire disséminée (hors cancers et hémopathies malignes) : définition et terminologie retenue (biologique/clinique/compliquée), situations à risque (mécanismes physiopathologiques), diagnostic clinique et biologique (critères de consommation majeurs/mineurs), moyens thérapeutiques substitutifs et spécifiques, stratégie selon la situation clinique (organigramme SASC) — 22 énoncés cotés sur deux axes indépendants (niveau de preuve a-d, force de recommandation 1-3, pas toujours les deux).",
    society: "SRLF, avec la SFAR, la Société Française d'Hématologie (GEHT) et le GFRUP — Conférence de Consensus 2002",
    version: "2002 (XXIIe Conférence de Consensus)",
    validated: "Faculté de Médecine de Lille, 10 octobre 2002 — Président du jury : P.E. Bollaert",
    methodology: "Preuve (a-d) + Force (1-3), deux axes indépendants, non GRADE",
    pages: 6,
    url: "https://sfar.org/wp-content/uploads/2015/10/86-civdccons.pdf"
  },
  eclsa: {
    key: 'eclsa',
    badge: 'NIVEAU 5',
    title: "Assistance circulatoire — AC réfractaire",
    short: "Indications et contre-indications de l'assistance circulatoire (ECLS/ECMO) dans l'arrêt cardiaque réfractaire, intra- et extrahospitalier : définition et changement de paradigme, déterminants no-flow/low-flow, signes remettant en cause une durée de no-flow estimée (hypothermie, signes de vie, troubles du rythme), seuil ETCO2, algorithme décisionnel complet (Fig. 1), modalités pratiques (équipe, abord vasculaire), spécificités pédiatriques et de l'AC hypothermique, limites et lacunes de connaissances explicitement reconnues par les auteurs.",
    society: "Conseil français de réanimation cardiopulmonaire, SFAR, SFC, SFCTCV, SFMU, SF Pédiatrie, GFRUP, SF Perfusion, SRLF — RFE 2009",
    version: "2009 (Ann Fr Anesth Reanim 2009;28:182-186)",
    validated: "Coordonnateur : Bruno Riou — sous l'égide de la DGS/DHOS",
    methodology: "Prose continue, sans GRADE ni R1/R2 — niveau 5 (avis d'experts) global",
    pages: 5,
    url: "https://sfar.org/wp-content/uploads/2015/10/2_AFAR_Recommandations-sur-les-indications-de-lassistance-circulatoire-dans-le-traitement-des-arrets-cardiaques-refractaires.pdf"
  },
  transport_intrahospitalier: {
    key: 'transport_intrahospitalier',
    badge: 'ACCORD',
    title: "Transport intrahospitalier des patients à risque vital",
    short: "5 champs, 99 propositions (toutes à accord fort, pas de grade GRADE) : épidémiologie des événements indésirables (EI/EIG/EPR), matériels/monitorage/maintenance (ventilateurs de transport, dispositifs cardiaques, spécificités pédiatriques), préparation du malade avant transport, ressources humaines et formation des soignants, organisation/architecture/traçabilité.",
    society: "SRLF, SFAR, SFMU — Recommandations Formalisées d'Experts 2011",
    version: "2011 (Ann Fr Anesth Reanim 2011;30:952-956)",
    validated: "Présidents du comité d'organisation : J.-P. Quenot, C. Milesi, A. Cravoisy",
    methodology: "Accord fort (RAND/UCLA à deux tours, pas de grade GRADE)",
    pages: 5,
    url: "https://sfar.org/wp-content/uploads/2015/09/2_AFAR_Transport-intrahospitalier-des-patients-a-risque-vital.pdf"
  },
  transfusion_plasma: {
    key: 'transfusion_plasma',
    badge: 'GRADE A/B/C',
    title: "Transfusion de plasma thérapeutique",
    short: "Produits, caractéristiques et indications de la transfusion de plasma thérapeutique homologue (PFC-SD, PFC-IA, PFC-Se, PLYO) et autologue : compatibilité ABO, effets indésirables (TRALI, allergie), contre-indications ; indications gradées en chirurgie/traumatologie/obstétrique, en médecine (CIVD, micro-angiopathies thrombotiques, échanges plasmatiques, œdème angioneurotique héréditaire), en néonatologie/pédiatrie, et comme antidote exceptionnel au surdosage en AVK.",
    society: "ANSM & HAS — Actualisation 2012",
    version: "2012 (juin 2012)",
    validated: "ANSM / HAS, en concertation avec les sociétés savantes concernées",
    methodology: "Grades HAS/ANAES A/B/C + accord professionnel (pas de GRADE 1+/2+)",
    pages: 4,
    url: "https://sfar.org/wp-content/uploads/2015/10/2_HAS_Texte-court-ransfusion-de-plasma-therapeutique-Produits-indications.pdf"
  },
  sevrage_vm: {
    key: 'sevrage_vm',
    badge: 'PREUVE/FORCE',
    title: "Sevrage de la ventilation mécanique",
    short: "5 questions : quand débuter le sevrage (pré-requis généraux/respiratoires), prédiction du sevrage difficile (facteurs de risque, indice f/VT), conduite de l'épreuve de ventilation spontanée (pièce en T vs aide inspiratoire, durée, surveillance, conduite en cas d'échec), particularités selon le terrain (BPCO, cardiopathie, neurologique, chirurgical, pédiatrique), conduite à tenir en cas d'échec du sevrage (VNI, trachéotomie, domicile, limitation de soins) — avec l'organigramme complet de la procédure de sevrage.",
    society: "SRLF, avec la SFAR, la SPLF et le GFRUP — Conférence de Consensus 2001",
    version: "2001 (Réanimation 2001;10:697-8)",
    validated: "Président du jury : C. Richard (Le Kremlin-Bicêtre)",
    methodology: "Niveau de preuve a/b/c/d + niveau de recommandation 1/2/3 (Society of Critical Care Medicine Rating System 1997, pas de GRADE) — à l'exclusion du nouveau-né et du réveil d'anesthésie",
    pages: 12,
    url: "https://sfar.org/wp-content/uploads/2015/10/2_SFAR_Sevrage-de-la-ventilation-mecanique.pdf"
  },
  asthme_aigu_grave: {
    key: 'asthme_aigu_grave',
    badge: 'PREUVE/FORCE',
    title: "Crises d'asthme aiguës graves",
    short: "5 questions : prédiction de la gravité immédiate (Tableau I des critères de gravité), voie et schéma des bêta-2 mimétiques (nébulisation, aérosols-doseurs, voie SC, perfusion IV — Tableau II des molécules disponibles), place des autres thérapeutiques (oxygène, corticoïdes, anticholinergiques, adrénaline, aminophylline, sulfate de magnésium, hélium-oxygène, antibiothérapie), indications et modalités de l'hospitalisation (critères DEP adulte/enfant), modalités de la ventilation mécanique (intubation, réglages, sédation-curarisation, sevrage) — adulte et enfant, à l'exclusion du nourrisson.",
    society: "SRLF — Révision de la 3ᵉ Conférence de Consensus de 1988",
    version: "2002 (Réanimation 2002;11:1-9)",
    validated: "Coordinateur : E. L'Her (Brest)",
    methodology: "Niveau de preuve a/b/c/d + niveau de recommandation 1/2/3 (grille SRLF, pas de GRADE) — à l'exclusion du nourrisson",
    pages: 9,
    url: "https://sfar.org/wp-content/uploads/2015/10/REANIMATION_Prise-en-charge-des-crises-dasthme-aigues-graves-de-ladulte-et-de-lenfant-.pdf"
  },
  pancreatite: {
    key: 'pancreatite',
    badge: 'GRADE',
    title: "Pancréatite aigüe grave en soins critiques",
    short: "14 questions PICO réparties en 3 champs : évaluation et admission en soins critiques (critères de gravité, examens des 72 premières heures, surveillance de la pression intra-abdominale — Tableau 1 du score de Marshall modifié, Figure 1 de l'algorithme diagnostique, Annexe 1 des scores de risque BISAP/SIRS/APACHE/Ranson/Balthazar/CTSI) ; prise en charge à la phase initiale (hémodynamique, respiratoire, nutrition entérale/parentérale, CPRE, thérapeutiques non conventionnelles, antalgie) ; prise en charge des complications évolutives (antibioprophylaxie, diagnostic et drainage de la nécrose infectée, antibiothérapie curative, complications vasculaires, thrombose veineuse splanchnique). 24 recommandations + 4 questions sans recommandation possible.",
    society: "SFAR, en collaboration avec la SNFGE, la SFR, la SFNCM et la SFED",
    version: "2021 (validé CA SFAR 30/06/2021)",
    validated: "Coordonnateur d'experts : S. Jaber (Montpellier)",
    methodology: "GRADE® (1+/1-/2+/2-) + avis d'experts + absence de recommandation — actualise les recommandations SFAR/CNGOF 2001",
    pages: 48,
    url: "https://sfar.org/download/pancreatite-aigue-grave-du-patient-adulte-en-soins-critiques/?wpdmdl=35411"
  },
  corticotherapie: {
    key: 'corticotherapie',
    badge: 'PREUVE/FORCE',
    title: "Corticothérapie : choc septique & SDRA",
    short: "5 questions : manifestations du SDRA accessibles à la corticothérapie, conséquences surrénaliennes et vasculaires du choc septique (seuil de cortisolémie, place du test au Synacthène), bénéfices/risques attendus, indications et modalités dans le choc septique (hémisuccinate d'hydrocortisone 200-300 mg/j), indications et modalités dans le SDRA (méthylprednisolone 2 mg/kg/j à la phase fibro-proliférative). Les protocoles pratiques des Questions 4 et 5 ne portent aucune cotation dans le texte source (anomalie disclosée dans la fiche).",
    society: "SFAR, avec la SPILF, la SPLF et le GFRUP — XXe Conférence de Consensus, labellisée ANAES",
    version: "2000 (12 octobre 2000)",
    validated: "Président du jury : F. Fourrier (Lille)",
    methodology: "Niveau de preuve a/b/c/d + niveau de recommandation 1/2/3 (pas de GRADE) — niveau 3 et preuve d jamais utilisés dans le corps du texte ; protocoles pratiques des Questions 4-5 non cotés",
    pages: 6,
    url: "https://sfar.org/wp-content/uploads/2015/09/2_SFAR_Corticotherapie-au-cours-du-choc-septique-et-du-SDRA.pdf"
  },
  antibiotherapie_probabiliste: {
    key: 'antibiotherapie_probabiliste',
    badge: 'PROPOSITIONS',
    title: "Antibiothérapie probabiliste des états septiques graves",
    short: "12 sites infectieux (4.1-4.12) avec propositions d'antibiothérapie probabiliste par situation clinique : méningites communautaires/nosocomiales, pneumopathies communautaires/PAVM, infections urinaires, infections intra-abdominales (péritonites, pancréatites, angiocholites), infections cutanées/tissus mous (DHBN-FN), endocardites, infection sur cathéter, sepsis sans porte d'entrée. Plus généralités immunodéprimé/pédiatrie, réévaluation impérative à J2-J3 et J10, et tableau des posologies de première injection (24 antibiotiques). Aucune proposition individuelle n'est cotée par un niveau de preuve (disclosure dans la fiche).",
    society: "SFAR, avec la Société de réanimation de langue française, la Société de pathologie infectieuse de langue française, la Société de microbiologie, la Médecine militaire, la SFMU et la Société française de pédiatrie",
    version: "2004 (Conférence d'experts, texte court)",
    validated: "Coordonnateur : B. Veber (Rouen)",
    methodology: "Conférence d'experts — tableau général des niveaux de preuve I à V, non rattaché explicitement à une proposition individuelle du corps du texte",
    pages: 7,
    url: "https://sfar.org/wp-content/uploads/2015/10/2_AFAR_Antibiotherapie-probabiliste-des-etats-septiques-graves.pdf"
  },
  hsa: {
    key: 'hsa',
    badge: 'GRADE A/B/D/E',
    title: "Hémorragie sous-arachnoïdienne grave",
    short: "Prise en charge de l'HSA grave par rupture d'anévrysme (WFNS III-V) : diagnostic et prise en charge initiale (clinique, classifications WFNS/Hunt-Hess/Fisher, imagerie, ponction lombaire, transfert en centre de référence), complications précoces (HTIC, hydrocéphalie, resaignement, épilepsie, retentissement cardio-pulmonaire, natrémie), traitement de l'anévrysme (chirurgie vs endovasculaire, délai de 72h), anesthésie et douleur, vasospasme (diagnostic Doppler, prévention par nimodipine, triple H, traitement endovasculaire), stratégie de suivi et filière de soins. Grades A/B/D/E imprimés par le jury, sans définition dans ce texte court (disclosure dans la fiche) ; aucune occurrence de Grade C.",
    society: "SFAR, avec l'ANARLF, la Société française de neurochirurgie et la Société française de neuroradiologie",
    version: "2004 (Conférence d'experts, texte court)",
    validated: "Président du jury : L. Beydon (Angers)",
    methodology: "Conférence d'experts (grades A/B/D/E, pas de GRADE) — signification des lettres non définie dans le texte court",
    pages: 12,
    url: "https://sfar.org/wp-content/uploads/2015/10/2a_SFAR_texte-court_Hemorragies-sous-arachnoidienne.pdf"
  },
  sepsis_hemodynamique: {
    key: 'sepsis_hemodynamique',
    badge: 'Grades B/C/D/E',
    title: "Prise en charge hémodynamique du sepsis grave",
    short: "Volet circulatoire/hémodynamique exclusivement du sepsis grave et du choc septique (nouveau-né exclu) : cibles thérapeutiques, modalités de l'expansion volémique et de la transfusion, place des inotropes/vasoactifs, traitements complémentaires (corticothérapie), et algorithme de stratégie thérapeutique en 3 étapes avec repères temporels (60-90 min, 6h). 33 recommandations graduées B/C/D/E (aucun Grade A dans le texte), signification des lettres non définie dans ce texte court (disclosure dans la fiche).",
    society: "SFAR / SRLF",
    version: "2006 (Conférence de consensus commune, texte court)",
    validated: "Publication : Ann Fr Anesth Réanim 2006;25 — Réanimation 2006;15",
    methodology: "Conférence de consensus (grades B/C/D/E, pas de GRADE) — signification des lettres non définie dans le texte court",
    pages: 3,
    url: "https://sfar.org/wp-content/uploads/2015/10/2a_TEXTE-COURT_Prise-en-charge-hemodynamique-du-sepsis-grave.pdf"
  },
  securisation_proc: {
    key: 'securisation_proc',
    badge: 'ACCORD',
    title: "Sécurisation des procédures à risques en réanimation",
    short: "Pratiques de sécurité (« safety practices ») en réanimation, risque infectieux explicitement exclu : taxonomie EI/EPR et indicateurs, épidémiologie, organisation structurelle et managériale (protocoles, culture sécurité), sécurisation du matériel/dispositifs médicaux, ventilation mécanique (intubation, trachéotomie, sevrage, extubation, VNI), procédures circulatoires (vasoactifs, cathéters artériels/veineux centraux/artériels pulmonaires), épuration extra-rénale, spécificités pédiatriques — plus une zone d'indécision explicite de 3 propositions (ni accord ni désaccord), disclosée comme catégorie distincte.",
    society: "SRLF / SFAR",
    version: "2008 (Ann Fr Anesth Reanim 2008;27:e43-e51)",
    validated: "Groupes d'experts de la SRLF et de la SFAR",
    methodology: "Accord fort/faible (méthode RAND/UCLA, pas de GRADE) + zone d'indécision explicite",
    pages: 9,
    url: "https://sfar.org/wp-content/uploads/2015/10/2a_AFAR_Texte_court_Securisation-des-procedures-a-risques-en-reanimation.pdf"
  }
};

/* ============================================================
   Small helpers
   ============================================================ */
function esc(s){
  if(s == null) return '';
  return String(s);
}
var DIACRITICS_RE = new RegExp("[" + String.fromCharCode(0x0300) + "-" + String.fromCharCode(0x036f) + "]", "g");
function slugify(s, i){
  var base = (s||'').toLowerCase()
    .normalize('NFD').replace(DIACRITICS_RE,'')
    .replace(/[^a-z0-9]+/g,'-').replace(/(^-|-$)/g,'');
  return (base || 'section') + '-' + i;
}
var CHIP_CLASS = {
  '1+':'chip-good', 'A':'chip-good',
  '2+':'chip-accent', 'B':'chip-accent',
  '2-':'chip-warn', 'C':'chip-warn',
  '1-':'chip-crit',
  'AE':'chip-neutral'
};
function chipClass(label){ return CHIP_CLASS[label] || 'chip-neutral'; }

/* ============================================================
   Block rendering
   ============================================================ */
function isLegendTable(block){
  var rows = block.rows;
  if(rows.length !== 1) return false;
  return rows[0].every(function(c){
    return c && (c.t === 'chip' || (c.t === 'p' && c.style === 'badge_head'));
  });
}
function renderLegend(block){
  var cells = block.rows[0];
  var out = '<div class="legend">';
  for(var i=0;i<cells.length;i+=2){
    var chip = cells[i], label = cells[i+1];
    if(!chip) continue;
    out += '<div class="legend__item"><span class="chip ' + chipClass(chip.label) + '">' + esc(chip.label) + '</span><span>' + (label ? esc(label.html) : '') + '</span></div>';
  }
  out += '</div>';
  return out;
}
function isHeaderRow(row){
  return row.some(function(c){ return c && c.t === 'p' && (c.style === 'head_w' || c.style === 'head_w_c'); });
}
function renderCell(c, tag){
  if(c == null) return '<' + tag + '></' + tag + '>';
  if(c.t === 'chip'){
    return '<' + tag + ' class="num"><span class="chip ' + chipClass(c.label) + '">' + esc(c.label) + '</span></' + tag + '>';
  }
  if(c.t === 'p'){
    var cls = [];
    var inner = esc(c.html);
    if(c.style === 'cell_c' || c.style === 'head_w_c') cls.push('align-c');
    if(c.style === 'cell_b') inner = '<strong>' + inner + '</strong>';
    return '<' + tag + (cls.length ? ' class="' + cls.join(' ') + '"' : '') + '>' + inner + '</' + tag + '>';
  }
  if(c.t === 'table'){
    return '<' + tag + '>' + renderTable(c) + '</' + tag + '>';
  }
  return '<' + tag + '></' + tag + '>';
}
function renderTable(block){
  var rows = block.rows;
  if(!rows || !rows.length) return '';
  var html = '<div class="table-scroll"><table class="rfe">';
  var bodyRows = rows;
  if(isHeaderRow(rows[0])){
    html += '<thead><tr>' + rows[0].map(function(c){ return renderCell(c, 'th'); }).join('') + '</tr></thead>';
    bodyRows = rows.slice(1);
  }
  html += '<tbody>';
  bodyRows.forEach(function(row){
    html += '<tr>' + row.map(function(c){ return renderCell(c, 'td'); }).join('') + '</tr>';
  });
  html += '</tbody></table></div>';
  return html;
}
function renderBlock(b, toc){
  if(!b) return '';
  if(b.t === 'section'){
    var id = slugify(b.text, toc.counter++);
    toc.items.push({ id: id, text: b.text });
    return '<h2 class="block-section" id="' + id + '">' + esc(b.text) + '</h2>';
  }
  if(b.t === 'p'){
    var cls = 'block-p' + (b.style === 'note' ? ' is-note' : '') + (b.style === 'source' ? ' is-source' : '');
    return '<p class="' + cls + '">' + esc(b.html) + '</p>';
  }
  if(b.t === 'panel'){
    return '<div class="panel ' + esc(b.tone || 'default') + '">' + renderBlock(b.content, toc) + '</div>';
  }
  if(b.t === 'table'){
    if(isLegendTable(b)) return renderLegend(b);
    return renderTable(b);
  }
  return '';
}

function renderDocBody(docKey){
  var toc = { counter: 0, items: [] };
  var html = '';
  RAW[docKey].sections.forEach(function(sec){
    sec.items.forEach(function(item){
      html += renderBlock(item, toc);
    });
  });
  return { html: html, toc: toc.items };
}

/* ============================================================
   App state / router
   ============================================================ */
var state = { route: 'home', reports: [], dbReady: false, currentDocForReport: null, isAdmin: false, adminChecked: false };
var appEl = document.getElementById('app');

function parseRoute(){
  var h = location.hash.replace(/^#\/?/, '');
  if(!h) return { name: 'home' };
  var parts = h.split('/');
  if(parts[0] === 'doc' && DOC_META[parts[1]]) return { name: 'doc', key: parts[1] };
  if(parts[0] === 'admin') return { name: 'admin' };
  if(parts[0] === 'library') return { name: 'library' };
  return { name: 'home' };
}

function navLinkHtml(route){
  var homeActive = route.name === 'home';
  var links = '';
  links += '<button class="nav-link' + (homeActive ? ' is-active' : '') + '" data-nav="#/"><span class="nav-link__dot"></span>Accueil</button>';
  var libActive = route.name === 'library';
  links += '<button class="nav-link' + (libActive ? ' is-active' : '') + '" data-nav="#/library"><span class="nav-link__dot"></span>Toutes les recommandations<span class="count-badge" style="background:var(--accent)">' + LIBRARY.length + '</span></button>';
  Object.keys(DOC_META).forEach(function(k){
    var active = route.name === 'doc' && route.key === k;
    var pending = state.reports.filter(function(r){ return r.doc === k && r.status === 'nouveau'; }).length;
    links += '<button class="nav-link' + (active ? ' is-active' : '') + '" data-nav="#/doc/' + k + '"><span class="nav-link__dot"></span>' + esc(DOC_META[k].title) + '</button>';
  });
  if(state.isAdmin){
    var adminActive = route.name === 'admin';
    var pendingTotal = state.reports.filter(function(r){ return r.status === 'nouveau'; }).length;
    links += '<button class="nav-link' + (adminActive ? ' is-active' : '') + '" data-nav="#/admin"><span class="nav-link__dot"></span>Tableau de bord' + (pendingTotal ? '<span class="count-badge">' + pendingTotal + '</span>' : '') + '</button>';
  }
  return links;
}

function sidebarHtml(route, tocItems){
  var toc = '';
  if(route.name === 'doc' && tocItems && tocItems.length){
    toc = '<div class="toc">' + tocItems.map(function(t){
      return '<button type="button" class="toc__item" data-toc="' + t.id + '">' + esc(t.text) + '</button>';
    }).join('') + '</div>';
  }
  return '' +
    '<aside class="sidebar" id="sidebar">' +
      '<div class="sidebar__brand">' +
        '<div class="sidebar__mark">Medical Guidelines <small>SFAR</small></div>' +
        '<div class="sidebar__sub">Synthèses fiables des recommandations cliniques, au service de la pratique quotidienne.</div>' +
      '</div>' +
      '<div class="nav-group">' + navLinkHtml(route) + '</div>' +
      toc +
      '<div class="sidebar__footer">Synthèses indépendantes, non officielles.<br>Se référer aux textes intégraux en cas de doute.</div>' +
    '</aside>';
}

function render(){
  var route = parseRoute();
  var body, tocItems = null;
  if(route.name === 'home') body = renderHome();
  else if(route.name === 'doc'){
    var r = renderDocBody(route.key);
    tocItems = r.toc;
    body = renderDocPage(route.key, r.html);
  }
  else if(route.name === 'admin') body = renderAdmin();
  else if(route.name === 'library') body = renderLibrary();

  appEl.innerHTML =
    '<div class="menu-toggle"><button id="menuBtn" aria-label="Menu">☰</button> Medical Guidelines</div>' +
    sidebarHtml(route, tocItems) +
    '<main><div class="content-wrap">' + body + '</div></main>' +
    fabHtml();

  wireNav();
  wireFab(route);
  wireToc();
  if(route.name === 'admin') wireAdmin();
  if(route.name === 'library') wireLibrary();
  window.scrollTo(0,0);
}

function wireNav(){
  Array.prototype.forEach.call(document.querySelectorAll('[data-nav]'), function(el){
    el.addEventListener('click', function(){
      location.hash = el.getAttribute('data-nav');
      closeSidebarMobile();
    });
  });
  var menuBtn = document.getElementById('menuBtn');
  if(menuBtn){
    menuBtn.addEventListener('click', function(){
      document.getElementById('sidebar').classList.toggle('is-open');
    });
  }
}
function closeSidebarMobile(){
  var sb = document.getElementById('sidebar');
  if(sb) sb.classList.remove('is-open');
}

var tocObserver = null;
function wireToc(){
  if(tocObserver){ tocObserver.disconnect(); tocObserver = null; }
  var tocLinks = document.querySelectorAll('.toc__item');
  if(!tocLinks.length) return;
  Array.prototype.forEach.call(tocLinks, function(el){
    el.addEventListener('click', function(){
      var target = document.getElementById(el.getAttribute('data-toc'));
      if(target) target.scrollIntoView({ behavior:'smooth', block:'start' });
      closeSidebarMobile();
    });
  });
  var headers = document.querySelectorAll('.block-section');
  if(!headers.length || typeof IntersectionObserver === 'undefined') return;
  tocObserver = new IntersectionObserver(function(entries){
    entries.forEach(function(entry){
      var link = document.querySelector('.toc__item[data-toc="' + entry.target.id + '"]');
      if(!link) return;
      if(entry.isIntersecting) link.classList.add('is-active');
      else link.classList.remove('is-active');
    });
  }, { rootMargin: '-10% 0px -80% 0px' });
  Array.prototype.forEach.call(headers, function(h){ tocObserver.observe(h); });
}

window.addEventListener('hashchange', render);

/* ============================================================
   Library (full SFAR index — search & filters)
   ============================================================ */
var libState = { q: '', type: '', category: '', year: '', status: '' };

function libTypeLabel(t){
  var m = { RFE: 'RFE', RPP: 'RPP', CE: "Conférence d'Experts", CC: 'Conférence de Consensus',
            RPC: 'RPC', RBP: 'RBP', 'Préconisation': 'Préconisation' };
  return m[t] || t || 'Non classé';
}

function libMatches(item){
  var q = libState.q.trim().toLowerCase();
  if(q){
    var hay = [item.title, item.exact_type, item.category, (item.keywords||[]).join(' ')].join(' ').toLowerCase();
    if(hay.indexOf(q) === -1) return false;
  }
  if(libState.type && item.exact_type !== libState.type) return false;
  if(libState.category && (item.category||'').indexOf(libState.category) === -1) return false;
  if(libState.year && item.year !== libState.year) return false;
  if(libState.status === 'vigueur' && item.status && item.status !== 'en vigueur') return false;
  if(libState.status === 'abroge' && !(item.status && item.status !== 'en vigueur')) return false;
  return true;
}

function libOptions(field){
  var set = {};
  LIBRARY.forEach(function(item){
    var v = item[field];
    if(!v) return;
    if(field === 'category'){
      v.split(',').forEach(function(c){ c = c.trim(); if(c) set[c] = true; });
    } else {
      set[v] = true;
    }
  });
  return Object.keys(set).sort();
}

function renderLibraryList(){
  var filtered = LIBRARY.filter(libMatches);
  filtered.sort(function(a,b){ return (b.year||'').localeCompare(a.year||''); });
  var countHtml = '<div class="lib-count">' + filtered.length + ' recommandation' + (filtered.length!==1?'s':'') + ' sur ' + LIBRARY.length + '</div>';
  if(!filtered.length){
    return countHtml + '<div class="lib-empty">Aucun résultat. Essayez d\'élargir votre recherche.</div>';
  }
  var rows = filtered.map(function(item){
    var href = item.fiche_key ? ('#/doc/' + item.fiche_key) : (item.direct_pdf_url || item.href);
    var isInternal = !!item.fiche_key;
    var typePill = item.exact_type ? '<span class="type-pill">' + esc(libTypeLabel(item.exact_type)) + '</span>' : '';
    var catTags = (item.category||'').split(',').filter(Boolean).map(function(c){
      return '<span class="cat-tag">' + esc(c.trim()) + '</span>';
    }).join('');
    var statusTag = (item.status && item.status !== 'en vigueur') ? '<span class="status-tag-warn">⚠ ' + esc(item.status) + '</span>' : '';
    var ficheTag = isInternal ? '<span class="fiche-tag">Fiche complète</span>' : '';
    var ext = isInternal ? '' : '<span class="lib-row__ext">PDF source ↗</span>';
    var dataAttrs = isInternal ? ' data-nav="' + href + '"' : ' target="_blank" rel="noopener"';
    return '<a class="lib-row" href="' + esc(href) + '"' + dataAttrs + '>' +
      '<div class="lib-row__year">' + esc(item.exact_date ? item.exact_date.slice(0,4) : item.year) + '</div>' +
      '<div class="lib-row__body">' +
        '<div class="lib-row__title">' + esc(item.title) + '</div>' +
        '<div class="lib-row__meta">' + ficheTag + typePill + catTags + statusTag + '</div>' +
      '</div>' +
      ext +
    '</a>';
  }).join('');
  return countHtml + '<div class="lib-list">' + rows + '</div>';
}

function renderLibrary(){
  var types = libOptions('exact_type');
  var cats = libOptions('category');
  var years = Array.from(new Set(LIBRARY.map(function(i){ return i.year; }))).sort().reverse();

  var typeOpts = '<option value="">Tous types</option>' + types.map(function(t){
    return '<option value="' + esc(t) + '"' + (libState.type===t?' selected':'') + '>' + esc(libTypeLabel(t)) + '</option>';
  }).join('');
  var catOpts = '<option value="">Toutes catégories</option>' + cats.map(function(c){
    return '<option value="' + esc(c) + '"' + (libState.category===c?' selected':'') + '>' + esc(c) + '</option>';
  }).join('');
  var yearOpts = '<option value="">Toutes années</option>' + years.map(function(y){
    return '<option value="' + esc(y) + '"' + (libState.year===y?' selected':'') + '>' + esc(y) + '</option>';
  }).join('');

  return '' +
    '<div class="doc-header">' +
      '<div class="doc-header__eyebrow">Bibliothèque SFAR</div>' +
      '<h1>Toutes les recommandations</h1>' +
      '<div class="doc-header__meta"><span>Recherchez par mot-clé, filtrez par date ou par type. Les fiches marquées « Fiche complète » sont entièrement synthétisées sur ce site ; les autres renvoient vers le document source officiel.</span></div>' +
    '</div>' +
    '<div class="lib-toolbar">' +
      '<div class="lib-search">' +
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="11" cy="11" r="7"/><path d="m21 21-4.3-4.3"/></svg>' +
        '<input type="text" id="lib-q" placeholder="Rechercher un titre, un mot-clé (ex. sepsis, anticoagulants, intubation)…" value="' + esc(libState.q) + '">' +
      '</div>' +
      '<div class="lib-filters">' +
        '<span class="lib-filters__label">Filtrer :</span>' +
        '<select id="lib-type">' + typeOpts + '</select>' +
        '<select id="lib-category">' + catOpts + '</select>' +
        '<select id="lib-year">' + yearOpts + '</select>' +
        '<select id="lib-status">' +
          '<option value="">Tous statuts</option>' +
          '<option value="vigueur"' + (libState.status==='vigueur'?' selected':'') + '>En vigueur</option>' +
          '<option value="abroge"' + (libState.status==='abroge'?' selected':'') + '>Abrogée / remplacée</option>' +
        '</select>' +
      '</div>' +
    '</div>' +
    '<div id="lib-results">' + renderLibraryList() + '</div>';
}

function wireLibrary(){
  var q = document.getElementById('lib-q');
  var type = document.getElementById('lib-type');
  var cat = document.getElementById('lib-category');
  var year = document.getElementById('lib-year');
  var status = document.getElementById('lib-status');

  function refresh(){
    document.getElementById('lib-results').innerHTML = renderLibraryList();
    wireLibraryResultLinks();
  }
  if(q) q.addEventListener('input', function(){ libState.q = q.value; refresh(); });
  if(type) type.addEventListener('change', function(){ libState.type = type.value; refresh(); });
  if(cat) cat.addEventListener('change', function(){ libState.category = cat.value; refresh(); });
  if(year) year.addEventListener('change', function(){ libState.year = year.value; refresh(); });
  if(status) status.addEventListener('change', function(){ libState.status = status.value; refresh(); });
  wireLibraryResultLinks();
}

function wireLibraryResultLinks(){
  Array.prototype.forEach.call(document.querySelectorAll('#lib-results [data-nav]'), function(el){
    el.addEventListener('click', function(e){
      e.preventDefault();
      location.hash = el.getAttribute('data-nav');
      closeSidebarMobile();
    });
  });
}

/* ============================================================
   Views
   ============================================================ */
function renderHome(){
  var cards = Object.keys(DOC_META).map(function(k){
    var m = DOC_META[k];
    return '' +
      '<a class="doc-card" data-nav="#/doc/' + k + '" href="#/doc/' + k + '">' +
        '<span class="doc-card__badge">' + esc(m.badge) + '</span>' +
        '<h2>' + esc(m.title) + '</h2>' +
        '<p>' + esc(m.short) + '</p>' +
        '<div class="doc-card__meta"><span>' + esc(m.society) + '</span><span>' + m.pages + ' pages</span></div>' +
      '</a>';
  }).join('');
  return '' +
    '<div class="hero">' +
      '<div class="hero__eyebrow">Prototype — SFAR</div>' +
      '<h1>Les recommandations, enfin lisibles.</h1>' +
      '<p>Synthèses fidèles des RFE et recommandations des sociétés savantes en anesthésie-réanimation — grades conservés, sources tracées, pensées pour être lues en quelques minutes au moment de la décision clinique.</p>' +
    '</div>' +
    '<div class="doc-grid">' + cards + '</div>' +
    '<div class="info-strip">Vous avez repéré une erreur ou une imprécision&nbsp;? Utilisez le bouton « Signaler une erreur » en bas de chaque page — votre signalement est examiné avant toute correction.</div>';
}

function renderDocPage(key, bodyHtml){
  var m = DOC_META[key];
  return '' +
    '<div class="doc-header">' +
      '<div class="doc-header__eyebrow">' + esc(m.society) + '</div>' +
      '<h1>' + esc(m.title) + '</h1>' +
      '<div class="doc-header__meta">' +
        '<span><b>Méthodologie</b>&nbsp;' + esc(m.methodology) + '</span>' +
        '<span><b>Version</b>&nbsp;' + esc(m.version) + '</span>' +
        '<span><b>Validation</b>&nbsp;' + esc(m.validated) + '</span>' +
      '</div>' +
    '</div>' +
    bodyHtml;
}

/* ============================================================
   Feedback widget (report an error)
   ============================================================ */
function fabHtml(){
  return '' +
    '<button class="fab" id="fabBtn"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 9v4"/><path d="M12 17h.01"/><path d="M10.29 3.86 1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0Z"/></svg>Signaler une erreur</button>';
}

function currentVisibleSectionText(){
  var headers = Array.prototype.slice.call(document.querySelectorAll('.block-section'));
  var best = null;
  for(var i=0;i<headers.length;i++){
    var rect = headers[i].getBoundingClientRect();
    if(rect.top <= 140) best = headers[i];
    else break;
  }
  return best ? best.textContent : (headers[0] ? headers[0].textContent : '');
}

function wireFab(route){
  var btn = document.getElementById('fabBtn');
  if(!btn) return;
  btn.addEventListener('click', function(){
    openReportSheet(route);
  });
}

function openReportSheet(route){
  var isDoc = route.name === 'doc';
  var docOptions = Object.keys(DOC_META).map(function(k){
    var sel = (isDoc && route.key === k) ? ' selected' : '';
    return '<option value="' + k + '"' + sel + '>' + esc(DOC_META[k].title) + '</option>';
  }).join('');
  var prefillSection = isDoc ? currentVisibleSectionText() : '';

  var backdrop = document.createElement('div');
  backdrop.className = 'sheet-backdrop';
  backdrop.innerHTML =
    '<div class="sheet" role="dialog" aria-modal="true">' +
      '<h3>Signaler une erreur</h3>' +
      '<div class="sheet__sub">Votre signalement sera examiné avant toute correction du document.</div>' +
      '<div class="field"><label for="rf-doc">Document</label>' +
        '<select id="rf-doc">' + docOptions + '</select>' +
      '</div>' +
      '<div class="field"><label for="rf-section">Section / page concernée</label>' +
        '<input id="rf-section" type="text" value="' + esc(prefillSection) + '" placeholder="ex. Q10 — Insuffisance rénale">' +
        '<div class="field__hint">Pré-rempli avec la section actuellement affichée — modifiable.</div>' +
      '</div>' +
      '<div class="field"><label for="rf-desc">Description de l\'erreur</label>' +
        '<textarea id="rf-desc" placeholder="Décrivez précisément ce qui est incorrect ou manquant…"></textarea>' +
      '</div>' +
      '<div class="sheet__actions">' +
        '<button class="btn btn-ghost" id="rf-cancel">Annuler</button>' +
        '<button class="btn btn-primary" id="rf-submit">Envoyer le signalement</button>' +
      '</div>' +
    '</div>';
  document.body.appendChild(backdrop);
  backdrop.addEventListener('click', function(e){ if(e.target === backdrop) backdrop.remove(); });
  document.getElementById('rf-cancel').addEventListener('click', function(){ backdrop.remove(); });
  document.getElementById('rf-submit').addEventListener('click', function(){
    submitReport(backdrop);
  });
}

function submitReport(backdrop){
  var doc = document.getElementById('rf-doc').value;
  var section = document.getElementById('rf-section').value.trim();
  var desc = document.getElementById('rf-desc').value.trim();
  if(!desc){
    document.getElementById('rf-desc').focus();
    return;
  }
  var submitBtn = document.getElementById('rf-submit');
  submitBtn.disabled = true;
  submitBtn.textContent = 'Envoi…';

  var report = {
    doc: doc,
    docTitle: DOC_META[doc].title,
    section: section || '—',
    description: desc,
    status: 'nouveau',
    createdAt: new Date().toISOString()
  };

  saveReport(report).then(function(){
    backdrop.remove();
    showToast('Signalement envoyé — merci.');
  }).catch(function(err){
    submitBtn.disabled = false;
    submitBtn.textContent = 'Envoyer le signalement';
    showToast('Échec de l\'envoi — réessayez.');
  });
}

function showToast(msg){
  var t = document.createElement('div');
  t.className = 'toast';
  t.textContent = msg;
  document.body.appendChild(t);
  setTimeout(function(){ t.remove(); }, 3200);
}

/* ============================================================
   db capability wiring
   ============================================================ */
var dbApi = null;
var reportsCol = null, decisionsCol = null;

function initDb(){
  if(!(window.claude && window.claude.use)) return;
  window.claude.use('db').then(function(db){
    if(!db) return; // capability unavailable in this view — feature quietly disabled
    dbApi = db;
    reportsCol = db.collection('reports');
    decisionsCol = db.collection('decisions');

    // Admin gate: "admin_check" is db-rule-protected to write:"admin". A successful
    // write proves this viewer holds admin/owner sharing on the artifact; a rejected
    // write means a regular (interact-level) viewer. No `user` capability needed.
    db.doc('admin_check/self').set({ checkedAt: new Date().toISOString() }).then(function(){
      state.isAdmin = true;
    }).catch(function(){
      state.isAdmin = false;
    }).finally(function(){
      state.adminChecked = true;
      applyDecisionsAndRerenderNav();
    });

    reportsCol.orderBy('createdAt', 'desc').limit(200).onSnapshot(function(snap){
      var decisions = {};
      // merge decisions live too
      state.reports = snap.docs.map(function(d){
        var data = d.data() || {};
        return Object.assign({ id: d.id }, data);
      });
      applyDecisionsAndRerenderNav();
    }, function(err){
      console.warn('reports subscribe error', err);
    });
    decisionsCol.onSnapshot(function(snap){
      state.decisions = {};
      snap.docs.forEach(function(d){
        state.decisions[d.id] = d.data();
      });
      applyDecisionsAndRerenderNav();
    }, function(err){
      console.warn('decisions subscribe error', err);
    });
  }).catch(function(){ /* no db in this view */ });
}

function applyDecisionsAndRerenderNav(){
  state.decisions = state.decisions || {};
  state.reports.forEach(function(r){
    var d = state.decisions[r.id];
    if(d && d.status) r.status = d.status;
  });
  // refresh only the sidebar badge counts without a full re-render jank if on admin/home
  var route = parseRoute();
  if(route.name === 'admin'){
    render();
  } else {
    var navGroup = document.querySelector('.nav-group');
    if(navGroup) navGroup.innerHTML = navLinkHtml(route);
    wireNav();
  }
}

function saveReport(report){
  if(!reportsCol){
    return Promise.reject(new Error('db unavailable'));
  }
  return reportsCol.add(report);
}

function setDecision(reportId, status){
  if(!decisionsCol) return Promise.reject(new Error('db unavailable'));
  return decisionsCol.doc(reportId).set({ status: status, decidedAt: new Date().toISOString() });
}

/* ============================================================
   Admin dashboard
   ============================================================ */
var adminTab = 'nouveau';

function renderAdmin(){
  if(!state.isAdmin){
    var waiting = !state.adminChecked;
    return '' +
      '<div class="doc-header">' +
        '<div class="doc-header__eyebrow">Administration</div>' +
        '<h1>' + (waiting ? 'Vérification des droits…' : 'Accès réservé') + '</h1>' +
      '</div>' +
      '<div class="panel' + (waiting ? '' : ' crit') + '">' +
        (waiting
          ? '<p>Vérification de vos droits d\'accès en cours…</p>'
          : '<p>Le tableau de bord des signalements est réservé aux administrateurs de ce document. ' +
            'Si vous pensez devoir y avoir accès, demandez au propriétaire du site de vous ajouter comme éditeur.</p>') +
      '</div>';
  }
  var reports = state.reports || [];
  var counts = { nouveau: 0, valide: 0, rejete: 0 };
  reports.forEach(function(r){ counts[r.status] = (counts[r.status]||0) + 1; });

  var tabs = ['nouveau','valide','rejete'].map(function(t){
    var labels = { nouveau: 'Nouveaux', valide: 'Validés', rejete: 'Rejetés' };
    return '<button class="admin-tab' + (adminTab===t?' is-active':'') + '" data-tab="' + t + '">' + labels[t] + ' (' + (counts[t]||0) + ')</button>';
  }).join('');

  var filtered = reports.filter(function(r){ return r.status === adminTab; });
  var list = filtered.length ? filtered.map(renderReportCard).join('') :
    '<div class="empty-state">Aucun signalement dans cette catégorie.</div>';

  var dbNote = dbApi ? '' :
    '<div class="panel grey">Le stockage des signalements (capacité <code>db</code>) n\'est pas actif dans cette vue — ' +
    'les nouveaux signalements ne seront pas conservés tant que la page n\'est pas ouverte via claude.ai avec cette capacité activée.</div>';

  return '' +
    '<div class="doc-header">' +
      '<div class="doc-header__eyebrow">Administration</div>' +
      '<h1>Tableau de bord des signalements</h1>' +
      '<div class="doc-header__meta"><span>Validez un signalement pour générer le texte à transmettre à l\'IA.</span></div>' +
    '</div>' +
    dbNote +
    '<div class="admin-tabs">' + tabs + '</div>' +
    '<div id="admin-list">' + list + '</div>';
}

function renderReportCard(r){
  var statusCls = { nouveau: 'status-nouveau', valide: 'status-valide', rejete: 'status-rejete' }[r.status] || 'status-nouveau';
  var statusLbl = { nouveau: 'Nouveau', valide: 'Validé', rejete: 'Rejeté' }[r.status] || r.status;
  var date = '';
  try { date = new Date(r.createdAt).toLocaleString('fr-FR', { day:'2-digit', month:'2-digit', year:'numeric', hour:'2-digit', minute:'2-digit' }); } catch(e){}

  var actions = '';
  if(r.status === 'nouveau'){
    actions =
      '<button class="btn btn-primary btn-sm" data-action="valider" data-id="' + r.id + '">Valider</button>' +
      '<button class="btn btn-ghost btn-sm" data-action="rejeter" data-id="' + r.id + '">Rejeter</button>';
  } else if(r.status === 'valide'){
    actions =
      '<button class="btn btn-primary btn-sm" data-action="copier" data-id="' + r.id + '">Copier pour Claude</button>' +
      '<button class="btn btn-ghost btn-sm" data-action="rejeter" data-id="' + r.id + '">Rejeter</button>';
  } else {
    actions = '<button class="btn btn-ghost btn-sm" data-action="valider" data-id="' + r.id + '">Réexaminer → Valider</button>';
  }

  return '' +
    '<div class="report-card">' +
      '<div class="report-card__top">' +
        '<div>' +
          '<div class="report-card__where">' + esc(r.docTitle || r.doc) + ' — ' + esc(r.section) + '</div>' +
        '</div>' +
        '<div style="display:flex; gap:8px; align-items:center;">' +
          '<span class="status-pill ' + statusCls + '">' + statusLbl + '</span>' +
          '<span class="report-card__date">' + date + '</span>' +
        '</div>' +
      '</div>' +
      '<div class="report-card__desc">' + esc(r.description) + '</div>' +
      '<div class="report-card__actions">' + actions + '</div>' +
    '</div>';
}

function claudePrompt(r){
  return 'Corrige la fiche « ' + r.docTitle + ' » (site Medical Guidelines SFAR).\n' +
    'Section concernée : ' + r.section + '\n' +
    'Erreur signalée : ' + r.description + '\n' +
    'Vérifie contre le texte source avant de corriger, puis republie le document et le site.';
}

function wireAdmin(){
  Array.prototype.forEach.call(document.querySelectorAll('.admin-tab'), function(el){
    el.addEventListener('click', function(){
      adminTab = el.getAttribute('data-tab');
      render();
    });
  });
  Array.prototype.forEach.call(document.querySelectorAll('[data-action]'), function(el){
    el.addEventListener('click', function(){
      var id = el.getAttribute('data-id');
      var action = el.getAttribute('data-action');
      var report = (state.reports||[]).filter(function(r){ return r.id === id; })[0];
      if(!report) return;
      if(action === 'valider'){
        setDecision(id, 'valide').then(function(){ showToast('Signalement validé.'); }).catch(function(){ showToast('Action refusée (droits admin requis).'); });
      } else if(action === 'rejeter'){
        setDecision(id, 'rejete').then(function(){ showToast('Signalement rejeté.'); }).catch(function(){ showToast('Action refusée (droits admin requis).'); });
      } else if(action === 'copier'){
        var text = claudePrompt(report);
        copyToClipboard(text).then(function(){
          showToast('Texte copié — collez-le dans une conversation avec Claude.');
        }).catch(function(){
          showToast('Copie impossible — sélectionnez et copiez manuellement.');
        });
      }
    });
  });
}

function copyToClipboard(text){
  if(navigator.clipboard && navigator.clipboard.writeText){
    return navigator.clipboard.writeText(text);
  }
  return new Promise(function(resolve, reject){
    try{
      var ta = document.createElement('textarea');
      ta.value = text;
      ta.style.position = 'fixed';
      ta.style.opacity = '0';
      document.body.appendChild(ta);
      ta.select();
      document.execCommand('copy');
      document.body.removeChild(ta);
      resolve();
    } catch(e){ reject(e); }
  });
}

/* ============================================================
   Init
   ============================================================ */
initDb();
render();

})();
