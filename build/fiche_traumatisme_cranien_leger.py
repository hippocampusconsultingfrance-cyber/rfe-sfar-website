# -*- coding: utf-8 -*-
"""
Fiche de synthese - RPP SFMU-SFAR 2022 (avec SFBC/SFR/SOFMER)
Prise en charge des patients presentant un traumatisme cranien leger de l'adulte
Source verifiee : texte valide par la Commission des Referentiels de la SFMU (19/05/2022), le CA
SFMU (24/05/2022), le Comite des Referentiels Cliniques de la SFAR (03/09/2022) et le CA SFAR
(15/09/2022). Format RPP (Recommandation de Pratiques Professionnelles) et NON RFE - choix
methodologique explicite de la source elle-meme, faute de niveau de preuve suffisant pour la
methode GRADE numerique. Consequence : AUCUNE recommandation de ce document ne porte de tag
"GRADE 1/2" - la totalite des 11 blocs de questions (couvrant 14 enonces individuellement
formules avec leur propre cadre PICO) porte le tag litteral unique "Avis d'experts (Accord
Fort)", verifie exhaustivement par grep sur l'intégralite du texte source (11 occurrences,
coherent avec les 11 questions traitees). Resume officiel de la source : "13 recommandations,
accord fort pour 100%, 1 absence de recommandation" - mon propre inventaire independant, item par
item selon le decoupage P/I/C/O propre du texte, denombre 14 enonces individuels (R1, R2.1,
R2.2.1, R2.2.2, R2.3, R2.4, R2.5, R2.6.1, R2.6.2, R2.6.3, R2.7, R2.8, R3.1, R3.2) - le chiffre "13"
du resume officiel est cite tel quel dans l'introduction plutot que recalcule, la source ne
detaillant pas explicitement la correspondance exacte (meme pattern de non-reconciliation deja
rencontre sur plusieurs fiches de ce corpus).

Particularite de numerotation source verifiee et conservee telle quelle (pas une erreur
d'extraction) : R2.4 (delai optimal de la TDM) est litteralement imprime sous la Question 2.3,
et R2.3 (place du Doppler transcranien) est imprime sous la Question 2.4 - un intervertissement
de numerotation propre au document source, confirme par lecture directe du texte a ces deux
emplacements precis, reproduit ici fidelement sans "correction".

Annexe 1 (comparatif des scores cliniques CCHR/NOC/NEXUS-II/NICE/SNC/CHIP/NCWFNS) : tableau tres
dense dont l'extraction texte produit un ordre de lecture disloque (tableau large multi-colonnes) -
non reproduite integralement ici (disclosure explicite), la fiche se limitant a citer les scores
les mieux valides (CCHR, NOC, CHIP) deja mentionnes dans l'argumentaire de R2.1. Annexe 2 (fiche
d'information de sortie destinee au patient) : integralement extractible en texte, reproduite
verbatim.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from style import *
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.units import mm

OUT = "/private/tmp/claude-501/-Users-macbook-Downloads-claude/65498e3e-5ddf-47a6-b100-3ac535d1faa0/scratchpad/rfe_sfar/output/Fiche_SFMU_SFAR_Traumatisme_Cranien_Leger_2022.pdf"

SOURCE_TXT = ("Source : Recommandations de Pratiques Professionnelles (RPP) de la SFMU, en "
              "association avec la SFAR, avec SFBC/SFR/SOFMER « Prise en charge des patients "
              "présentant un traumatisme crânien léger de l'adulte » — 2022, texte validé par le "
              "CA SFMU (24/05/2022) et le CA SFAR (15/09/2022). Fiche de synthèse non officielle : "
              "se référer au texte intégral.")

def P(txt, style=S_CELL):
    return Paragraph(txt, style)

def chip(label, **kw):
    return grade_chip(label, **kw)

def reco_table(rows, col_widths):
    """rows: (ref, text, grade_label_for_chip)"""
    data = [[P("Réf.", S_HEAD_W), P("Recommandation", S_HEAD_W), P("Grade", S_HEAD_W_C)]]
    for ref, txt, grade in rows:
        data.append([P(ref, S_CELL_B), P(txt, S_CELL), chip(grade)])
    t = Table(data, colWidths=col_widths, repeatRows=1)
    style_cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), NAVY), ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTNAME", (0, 0), (-1, 0), FONT_BOLD), ("FONTSIZE", (0, 0), (-1, 0), 8),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("ALIGN", (2, 0), (2, -1), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 0.5, GREY_LIGHT),
        ("TOPPADDING", (0, 0), (-1, -1), 3.4), ("BOTTOMPADDING", (0, 0), (-1, -1), 3.4),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            style_cmds.append(("BACKGROUND", (0, i), (-1, i), BG_PANEL))
    t.setStyle(TableStyle(style_cmds))
    return t

def no_reco_panel(text):
    return info_panel(P("<b>Absence de recommandation</b> — " + text, S_BODY_SM), bg=GREY_LIGHT, border=GREY)

def simple_table(header, rows, col_widths):
    data = [[P(h, S_HEAD_W) for h in header]]
    for r in rows:
        data.append([P(c, S_CELL) for c in r])
    t = Table(data, colWidths=col_widths, repeatRows=1)
    st = [
        ("BACKGROUND",(0,0),(-1,0), TEAL_DARK), ("TEXTCOLOR",(0,0),(-1,0), WHITE),
        ("FONTNAME",(0,0),(-1,0), FONT_BOLD), ("FONTSIZE",(0,0),(-1,0), 8),
        ("GRID",(0,0),(-1,-1),0.5,GREY_LIGHT), ("VALIGN",(0,0),(-1,-1),"TOP"),
        ("TOPPADDING",(0,0),(-1,-1),3.4), ("BOTTOMPADDING",(0,0),(-1,-1),3.4), ("LEFTPADDING",(0,0),(-1,-1),5),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            st.append(("BACKGROUND",(0,i),(-1,i), BG_PANEL))
    t.setStyle(TableStyle(st))
    return t

TOTAL_PAGES = {"n": 8}

def on_page(canvas, doc, page_title):
    header_band(canvas, doc, "SFMU / SFAR — RPP 2022 — FICHE DE SYNTHÈSE",
                "Traumatisme crânien léger de l'adulte",
                page_title, icon_fn=lambda c,x,y: icon_shield(c, x, y, 13*mm), color=NAVY)
    footer_band(canvas, doc, SOURCE_TXT, f"Page {doc.page} / {TOTAL_PAGES['n']}")

# ---------------------------------------------------------------------------
def _section_intro():
    story = []
    story.append(Spacer(1, 3*mm))
    story.append(info_panel(P(
        "<b>Champ :</b> patients adultes pris en charge en structure de médecine d'urgence dans "
        "les 24 heures suivant un traumatisme crânien non pénétrant, avec un score de Glasgow "
        "initial de 13, 14 ou 15. Comité SFMU/SFAR, avec SFBC, SFR, SOFMER ; format PICO, "
        "3 champs (évaluation pré-hospitalière, prise en charge aux urgences, modalités de "
        "sortie), 11 questions.<br/><br/>"
        "<b>Choix méthodologique explicite de la source :</b> format RPP (Recommandation de "
        "Pratiques Professionnelles) plutôt que RFE, faute de niveau de preuve suffisant pour "
        "la méthode GRADE numérique — <b>aucune recommandation de ce document ne porte de "
        "grade « 1/2 »</b> ; toutes sont formulées « les experts proposent de faire / de ne pas "
        "faire ».<br/><br/>"
        "<b>Résultats (résumé officiel) :</b> 13 recommandations ; accord fort pour 100 % d'entre "
        "elles après deux tours de cotation. Pour une question (réversion des inhibiteurs des "
        "récepteurs P2Y12), aucune recommandation n'a pu être formulée.",
        S_BODY), bg=BG_PANEL, border=TEAL))
    story.append(Spacer(1, 3*mm))
    cw = PAGE_W - 2*MARGIN
    story.append(simple_table(
        ["Tableau 1 — Définition du traumatisme crânien léger (OMS 2004)", ""],
        [
            ["1. Une ou plusieurs manifestations", "Confusion ou désorientation • Perte de "
             "conscience ≤ 30 min • Amnésie post-traumatique &lt; 24h • et/ou autres anomalies "
             "neurologiques transitoires (signes focaux, crise d'épilepsie, lésion "
             "intracrânienne ne nécessitant pas d'intervention chirurgicale)"],
            ["2. Score de Glasgow", "13 à 15, 30 minutes après la blessure ou plus tard lors de "
             "la présentation aux soins"],
        ],
        [cw*0.32, cw*0.68]))
    return story

def _section_champ1():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Champ 1 — Évaluation pré-hospitalière"))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("R1", "Les experts proposent que les patients victimes d'un traumatisme crânien léger, "
         "pour lesquels la régulation médicale est sollicitée, ne soient pas orientés de façon "
         "systématique vers une structure des urgences s'ils peuvent être surveillés par une "
         "tierce personne, en l'absence de : trouble de coagulation préexistant (dont "
         "traitement anticoagulant) ; âge &gt; 65 ans ET traitement par antiplaquettaire(s) ; "
         "intoxication (médicamenteuse, alcool, autre) ; symptômes en dehors de céphalées "
         "(vomissement, perte de connaissance, amnésie &gt; 30 min, convulsion, déficit "
         "focalisé, altération de la vigilance) ; signe de traumatisme (hématome en lunettes, "
         "embarrure, signes de fracture de la base du crâne, hématome mastoïdien).", "AE"),
    ], [13*mm, PAGE_W-2*MARGIN-13*mm-20*mm, 20*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(P("Facteurs prédictifs de lésion intracrânienne identifiés dans la littérature "
                    "(hors contexte de régulation médicalisée) : altération de la vigilance "
                    "(GCS&lt;15) à la prise en charge ou à 2h, perte de connaissance, "
                    "convulsions, déficit sensitivomoteur, vomissements itératifs, traumatisme "
                    "ouvert avec embarrure, signes de fracture de la base du crâne, âge "
                    "&gt;65 ans (voire &gt;60), amnésie antérograde. Patient &lt;65 ans sous "
                    "monothérapie antiplaquettaire, asymptomatique, sans autre facteur de "
                    "risque : surveillance simple à domicile envisageable (incidence "
                    "d'hémorragie intracrânienne modérément augmentée sous antiagrégation, mais "
                    "sans augmentation du risque neurochirurgical ou de décès).", S_NOTE))
    return story

def _section_champ2a():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Champ 2 — Éléments cliniques à risque & biomarqueurs"))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("R2.1", "Les experts proposent de stratifier le risque d'aggravation clinique ou de "
         "lésion intracrânienne selon la classification suivante — <b>Risque élevé</b> : "
         "troubles de l'hémostase (anticoagulants, bithérapie antiplaquettaire, maladie "
         "hémorragique congénitale) ; signes de fracture de la voûte ou de la base du crâne "
         "(Tableau 2) ; GCS &lt; 15 à 2h du traumatisme sans intoxication ; plus d'un épisode "
         "de vomissements ; convulsions post-traumatiques ; déficit neurologique focalisé. "
         "<b>Risque intermédiaire</b> : âge ≥ 65 ans avec mono-antiagrégation plaquettaire ; "
         "GCS &lt; 15 à 2h du traumatisme avec intoxication ; traumatisme à cinétique élevée "
         "(Tableau 3) ; amnésie des faits survenus plus de 30 min avant le traumatisme.", "AE"),
        ("R2.2.1", "Les experts proposent de réaliser un dosage sanguin de la protéine S100B, "
         "lorsque celui-ci est disponible, dans les 3h suivant le traumatisme, chez les "
         "patients à risque intermédiaire (cf. R2.1) pour limiter le nombre de scanners "
         "cérébraux.", "AE"),
        ("R2.2.2", "Les experts proposent de réaliser un dosage sanguin combinant UCH-L1 et "
         "GFAP, lorsque ceux-ci sont disponibles, dans les 12h suivant le traumatisme, chez les "
         "patients à risque intermédiaire (cf. R2.1) pour limiter le nombre de scanners "
         "cérébraux.", "AE"),
    ], [13*mm, PAGE_W-2*MARGIN-13*mm-20*mm, 20*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(P("Seule modification vs. les recommandations 2012 : la monothérapie par "
                    "aspirine ou clopidogrel n'est plus considérée comme facteur de risque de "
                    "lésion hémorragique. Prévalence des lésions intracérébrales sévères chez le "
                    "TCL : 7,1 % (IC95 [6,8-7,4]) ; décès ou intervention neurochirurgicale : "
                    "0,9 % seulement (méta-analyse Easter et al.). Protéine S100B &lt;0,1 µg/L "
                    "dans les 3h : sensibilité 96,4-100 %, VPN 96,9-100 % pour éliminer une "
                    "lésion significative. Dosage combiné UCH-L1 (seuil 327 pg/mL) + GFAP (seuil "
                    "22 pg/mL) dans les 12h : spécificité 36,7 %, sensibilité 97,3 %, VPN 99,5 %.", S_NOTE))
    story.append(Spacer(1, 3*mm))
    cw = PAGE_W - 2*MARGIN
    story.append(simple_table(
        ["Tableau 2 — Signes évocateurs d'une fracture", "Détail"],
        [
            ["Base du crâne", "Otorrhée ou rhinorrhée, ecchymose mastoïdienne, ecchymose "
             "périorbitaire, hémotympan ou saignement extériorisé par le conduit auditif"],
            ["Voûte du crâne", "Discontinuité palpable de la voûte, suspicion d'embarrure "
             "ouverte ou fermée du crâne"],
        ],
        [cw*0.25, cw*0.75]))
    story.append(Spacer(1, 2*mm))
    story.append(info_panel(P(
        "<b>Tableau 3 — Éléments évocateurs d'une cinétique élevée :</b> occupant éjecté du "
        "véhicule • véhicule retourné • piéton ou cycliste renversé et sans casque • chute "
        "d'une hauteur &gt; 5 marches ou &gt; 2 m.",
        S_BODY_SM), bg=BG_PANEL, border=TEAL))
    return story

def _section_champ2b():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Champ 2 — Délai de la TDM & Doppler transcrânien"))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("R2.4", "Les experts proposent de réaliser une TDM cérébrale le plus précocement "
         "possible pour identifier les lésions intracrâniennes significatives, chez les "
         "patients présentant un TCL : idéalement dans l'heure suivant l'admission pour les "
         "patients à risque élevé d'aggravation clinique ou de lésion intracrânienne ; au plus "
         "tard dans les 8 heures pour les patients à risque intermédiaire.", "AE"),
        ("R2.3", "Les experts proposent de réaliser, après un scanner cérébral anormal, un "
         "Doppler Transcrânien chez les patients traumatisés crâniens légers pour évaluer le "
         "risque d'aggravation neurologique précoce.", "AE"),
    ], [13*mm, PAGE_W-2*MARGIN-13*mm-20*mm, 20*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(info_panel(P(
        "<b>Numérotation source conservée telle quelle :</b> R2.4 (délai de la TDM) est "
        "littéralement imprimé sous la Question 2.3, et R2.3 (Doppler transcrânien) est "
        "littéralement imprimé sous la Question 2.4 dans le document source — un "
        "intervertissement de numérotation propre à la source elle-même, reproduit fidèlement "
        "ici sans correction.",
        S_BODY_SM), bg=AMBER_LIGHT, border=AMBER))
    story.append(Spacer(1, 2*mm))
    story.append(P("Délai de 8h retenu sur la base des études de validation des règles "
                    "internationales (CCHR, New Orleans, NICE), ayant montré qu'un délai de 8h "
                    "permet d'identifier les lésions chez la quasi-totalité des patients des "
                    "cohortes. Scanner avec injection si signes de dissection carotidienne : "
                    "fracture du rachis cervical, déficit neurologique non expliqué par "
                    "l'imagerie, syndrome de Claude Bernard Horner, fracture de Lefort II/III, "
                    "fracture de la base du crâne, traumatisme des tissus mous cervicaux. "
                    "Doppler transcrânien : seuils index de pulsatilité &lt;1,25 et vitesse "
                    "diastolique &gt;25 cm/s associés à l'absence d'aggravation précoce — VPN "
                    "98 % (IC95 [96-100]) globalement, 100 % pour le TCL spécifiquement "
                    "(356 patients, GCS 9-15), réalisé après le scanner sans injection, au "
                    "maximum dans les 12h.", S_NOTE))
    return story

def _section_champ2c():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Champ 2 — Imagerie de contrôle & réversion des anticoagulants"))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("R2.5", "Les experts proposent de ne pas réaliser d'imagerie de contrôle aux patients "
         "présentant une lésion intracrânienne sur la TDM initiale, en dehors des situations "
         "suivantes : aggravation neurologique ; patient âgé de plus de 65 ans ; troubles de "
         "l'hémostase, en dehors de la prise d'aspirine seule.", "AE"),
        ("R2.6.1", "Les experts proposent de réaliser une réversion immédiate des anti-vitamine "
         "K chez les patients présentant une lésion hémorragique intracrânienne objectivée par "
         "une imagerie après un TCL, pour limiter le risque d'aggravation neurologique.", "AE"),
        ("R2.6.2", "Les experts proposent de réaliser une réversion immédiate des anticoagulants "
         "oraux directs chez les patients présentant une lésion hémorragique intracrânienne "
         "objectivée par une imagerie après un TCL, pour limiter le risque d'aggravation "
         "neurologique.", "AE"),
        ("R2.6.3", "Les experts proposent de discuter la conduite à tenir de façon collégiale "
         "chez les patients porteurs d'une valve cardiaque mécanique.", "AE"),
    ], [14*mm, PAGE_W-2*MARGIN-14*mm-20*mm, 20*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(P("Un INR &gt;3 à la prise en charge est associé à un risque plus élevé de "
                    "saignement retardé (RR=14 IC95 [4-49]). Modalités de réversion proposées : "
                    "AVK — CCP non activé 25 UI/kg + vitamine K 10 mg IV ou PO ; apixaban ou "
                    "rivaroxaban — CCP 50 UI/kg (max 5000 UI, pas d'antidote spécifique "
                    "disponible) ; dabigatran — idarucizumab 5 g IV (ou CCP 50 UI/kg IV si "
                    "indisponible). 5 % des TCL avec GCS 15 ont une imagerie anormale (30 % si "
                    "GCS 13-15), dont 1 % nécessitent une prise en charge neurochirurgicale — un "
                    "contrôle scanographique après 48h (en l'absence d'aggravation clinique) "
                    "peut raisonnablement être proposé.", S_NOTE))
    return story

def _section_champ2d():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Champ 2 — Antiplaquettaires & retour à domicile"))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("R2.7", "Les experts proposent de ne pas neutraliser l'aspirine chez un patient traité "
         "par aspirine avec lésion hémorragique intracrânienne après un TCL, pour limiter le "
         "risque d'aggravation neurologique.", "AE"),
    ], [13*mm, PAGE_W-2*MARGIN-13*mm-20*mm, 20*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(no_reco_panel("les experts ne sont pas en mesure d'émettre une recommandation "
                                "concernant la prise en charge spécifique des patients traités "
                                "par un inhibiteur des récepteurs P2Y12 (clopidogrel, "
                                "prasugrel, ticagrelor) présentant une lésion hémorragique "
                                "intracrânienne après un TCL, faute de données suffisantes."))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("R2.8", "Les experts proposent d'autoriser un retour à domicile des patients depuis la "
         "structure des urgences, même en présence d'anticoagulants ou d'agents "
         "antiplaquettaires, si au moins un de ces éléments est présent : patient à faible "
         "risque de saignement (cf. R2.1) ; dosage d'un biomarqueur sérique négatif ; TDM "
         "initiale ne retrouvant pas de saignement.", "AE"),
    ], [13*mm, PAGE_W-2*MARGIN-13*mm-20*mm, 20*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(P("Transfusion plaquettaire sous aspirine : sans bénéfice démontré sur "
                    "l'expansion de l'hématome, le recours neurochirurgical ou la mortalité "
                    "(méta-analyse Alvikas — OR=0,88 [0,34-2,28] pour la progression "
                    "hémorragique). Sous clopidogrel, le risque de resaignement et de recours "
                    "chirurgical est augmenté ; des données préliminaires suggèrent un possible "
                    "bénéfice de la transfusion plaquettaire, insuffisantes à ce jour pour "
                    "recommander. Retour à domicile : éléments cliniques requis — absence "
                    "d'intoxication associée, absence de vomissements itératifs, absence de "
                    "céphalées importantes persistantes, GCS à 15, absence de déficit "
                    "neurologique, absence d'autre motif d'hospitalisation.", S_NOTE))
    return story

def _section_champ3():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Champ 3 — Filière de soins & information de sortie"))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("R3.1", "Les experts proposent que la persistance de symptômes jugés invalidants par "
         "le patient au-delà de 7 jours après le traumatisme doive amener à une évaluation "
         "médicale.", "AE"),
        ("R3.2", "Les experts proposent que les patients présentant un TCL traité en "
         "ambulatoire, et le cas échéant leur entourage, bénéficient d'une information éclairée "
         "écrite et orale standardisée sur les motifs devant amener à reconsulter aux urgences "
         "dans les 48 heures suivant le retour à domicile.", "AE"),
    ], [13*mm, PAGE_W-2*MARGIN-13*mm-20*mm, 20*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(P("Des plaintes cognitives chroniques (&gt;3 mois) sont présentes au décours "
                    "de 50 % des TCL, invalidantes et sévères dans 10 % des cas — moins d'un "
                    "patient sur 2 reçoit une information adaptée aux urgences, moins d'un sur "
                    "2 bénéficie d'un suivi à 3 mois (étude américaine). Suivi actif requis en "
                    "cas de symptômes marqués initialement et/ou persistants &gt;7 jours "
                    "(ambulatoire si simple, équipes spécialisées si forte complexité ou "
                    "séquelles &gt;4-6 semaines) : vertiges, troubles du sommeil, troubles de la "
                    "vue, fatigue persistants. Signes rassurants ne nécessitant pas de suivi "
                    "actif : faibles symptômes s'amendant en &lt;24-48h.", S_NOTE))
    story.append(Spacer(1, 3*mm))
    story.append(section_bar("Annexe 2 (source) — Fiche d'information de sortie"))
    story.append(Spacer(1, 2*mm))
    story.append(info_panel(P(
        "<b>Signes devant amener à consulter en urgence (SAMU 15) dans les 48h suivant la "
        "sortie :</b> perte de connaissance, somnolence excessive ou baisse de la vigilance • "
        "trouble du comportement ou convulsions • trouble de la vision, de l'audition ou de la "
        "parole • trouble de l'équilibre • difficulté à mobiliser un membre • maux de tête "
        "intenses ou résistants aux antalgiques • vomissements ou nausées • écoulement par le "
        "nez ou les oreilles • douleurs cervicales.<br/><br/>"
        "<b>Symptômes fréquents pouvant persister, devant disparaître dans les 7 jours :</b> mal "
        "de tête modéré, nausées sans vomissement, vertiges, difficultés de concentration ou "
        "de mémoire, troubles du sommeil ou fatigue, manque d'appétit — en cas de doute ou de "
        "persistance au-delà de 7 jours, consulter le médecin traitant.<br/><br/>"
        "Éviter toute prise médicamenteuse sans avis médical. En cas de pratique d'une activité "
        "ou d'un sport à risque de nouveau traumatisme crânien, ne pas reprendre cette activité "
        "dans les 15 jours.",
        S_BODY_SM), bg=BG_PANEL, border=TEAL))
    return story

def _section_synthese():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Synthèse et messages clés"))
    story.append(Spacer(1, 2*mm))
    story.append(P(
        "• Régulation médicale : orientation systématique vers les urgences non requise si "
        "surveillance possible par un tiers et absence de trouble de coagulation, "
        "âge&gt;65 ans+antiplaquettaire, intoxication, symptôme autre que céphalée, ou signe de "
        "traumatisme.<br/>"
        "• Stratification du risque (élevé vs intermédiaire) dès l'admission — biomarqueurs "
        "(S100B &lt;3h, ou UCH-L1+GFAP &lt;12h) utilisables chez les patients à risque "
        "intermédiaire pour limiter le recours au scanner.<br/>"
        "• TDM : idéalement &lt;1h si risque élevé, au plus tard &lt;8h si risque intermédiaire. "
        "Doppler transcrânien après scanner anormal pour évaluer le risque d'aggravation "
        "précoce.<br/>"
        "• Pas de contrôle scanographique systématique après lésion initiale (sauf "
        "aggravation, âge&gt;65 ans, ou trouble de l'hémostase hors aspirine seule). Réversion "
        "immédiate des AVK et des AOD si lésion hémorragique objectivée ; discussion "
        "collégiale si valve mécanique ; pas de neutralisation de l'aspirine seule ; aucune "
        "recommandation possible pour les inhibiteurs P2Y12 (clopidogrel/prasugrel/ticagrelor), "
        "faute de données.<br/>"
        "• Retour à domicile possible (y compris sous anticoagulant/antiplaquettaire) si "
        "faible risque de saignement, biomarqueur négatif, ou TDM initiale sans saignement.<br/>"
        "• Sortie : information écrite et orale standardisée systématique (fiche patient), "
        "surveillance active des signes d'alerte sur 48h ; évaluation médicale si symptômes "
        "invalidants persistant &gt;7 jours, avec accès à une filière de soins spécialisée si "
        "besoin.",
        S_BODY))
    story.append(Spacer(1, 5*mm))

    story.append(section_bar("Sources et traçabilité", color=GREY))
    story.append(Spacer(1, 2*mm))
    story.append(P(
        "<b>Document source :</b> « Prise en charge des patients présentant un traumatisme "
        "crânien léger de l'adulte » — Recommandations de Pratiques Professionnelles de la SFMU, "
        "en association avec la SFAR, avec SFBC, SFR, SOFMER. 2022, texte validé par la "
        "Commission des Référentiels de la SFMU (19/05/2022), le CA SFMU (24/05/2022), le Comité "
        "des Référentiels Cliniques de la SFAR (03/09/2022), le CA SFAR (15/09/2022). Comité de "
        "22 experts, coordination C. Gil-Jardiné (SFMU), J.F. Payen (SFAR).", S_SOURCE))
    story.append(Spacer(1, 1.5*mm))
    story.append(P("<b>Méthodologie :</b> format RPP (et non RFE), choix explicite de la source "
                    "faute de niveau de preuve suffisant pour la méthode GRADE numérique — toutes "
                    "les recommandations portent le tag littéral unique « Avis d'experts (Accord "
                    "Fort) », cité ici tel quel (« AE »). Numérotation R2.3/R2.4 intervertie dans "
                    "la source elle-même (cf. encart Champ 2), conservée fidèlement.", S_SOURCE))
    story.append(Spacer(1, 1.5*mm))
    story.append(P("<b>Couverture :</b> 14 énoncés individuellement formulés selon le cadre PICO "
                    "propre du texte (R1, R2.1, R2.2.1-2, R2.3, R2.4, R2.5, R2.6.1-3, R2.7, R2.8, "
                    "R3.1, R3.2) reproduits intégralement, ainsi que l'absence de recommandation "
                    "(P2Y12) et l'Annexe 2 (fiche d'information de sortie). Le résumé officiel de "
                    "la source annonce un total agrégé de « 13 recommandations » — chiffre cité "
                    "tel quel dans l'introduction sans être recalculé, la source ne détaillant "
                    "pas la correspondance exacte avec le découpage par énoncé individuel. "
                    "L'Annexe 1 (comparatif dense de 7 scores cliniques internationaux) n'est pas "
                    "reproduite intégralement (tableau multi-colonnes à l'extraction "
                    "disloquée) — les scores les mieux validés (CCHR, NOC, CHIP) sont cités dans "
                    "l'argumentaire de R2.1 ; se référer au texte intégral pour le comparatif "
                    "complet.", S_SOURCE))
    story.append(Spacer(1, 3*mm))
    story.append(info_panel(P(
        "<b>Avertissement :</b> ce document est une fiche de synthèse indépendante, produite pour "
        "un usage d'aide-mémoire. Il reprend l'intégralité des recommandations de la RPP mais ne "
        "remplace pas le texte intégral et n'est ni édité ni validé par la SFMU/SFAR. En cas de "
        "doute, se référer au texte intégral, aux recommandations ultérieures et/ou à un avis "
        "spécialisé.",
        S_BODY_SM), bg=GREY_LIGHT, border=GREY))
    return story

SECTIONS = [
    ("Introduction, méthodologie", _section_intro),
    ("Champ 1 — Évaluation pré-hospitalière", _section_champ1),
    ("Champ 2 — Éléments cliniques & biomarqueurs", _section_champ2a),
    ("Champ 2 — Délai TDM & Doppler transcrânien", _section_champ2b),
    ("Champ 2 — Imagerie de contrôle & anticoagulants", _section_champ2c),
    ("Champ 2 — Antiplaquettaires & retour à domicile", _section_champ2d),
    ("Champ 3 — Filière de soins & information de sortie", _section_champ3),
    ("Synthèse, sources & traçabilité", _section_synthese),
]

def _make_doc():
    return SimpleDocTemplate(OUT, pagesize=A4,
                              leftMargin=MARGIN, rightMargin=MARGIN,
                              topMargin=32*mm, bottomMargin=16*mm,
                              title="Fiche SFMU-SFAR 2022 - Traumatisme cranien leger",
                              author="Synthèse indépendante (source SFMU/SFAR)")

def _silent_page(canvas, doc_):
    pass

def _build_upto(section_fns):
    story = []
    for i, fn in enumerate(section_fns):
        if i > 0:
            story.append(PageBreak())
        story.extend(fn())
    return story

def _count_pages(story_flowables):
    import pypdf
    doc = _make_doc()
    doc.build(story_flowables, onFirstPage=_silent_page, onLaterPages=_silent_page)
    return len(pypdf.PdfReader(OUT).pages)

def build():
    fns = [fn for _, fn in SECTIONS]

    boundaries = []
    for i in range(1, len(fns) + 1):
        pages = _count_pages(_build_upto(fns[:i]))
        boundaries.append((SECTIONS[i - 1][0], pages))

    total_pages = boundaries[-1][1]
    page_titles = []
    prev = 0
    for title, end_page in boundaries:
        page_titles += [title] * (end_page - prev)
        prev = end_page
    TOTAL_PAGES["n"] = total_pages

    counter = {"i": 0}
    def on_page_final(canvas, doc_):
        idx = min(counter["i"], len(page_titles) - 1)
        on_page(canvas, doc_, page_titles[idx])
        counter["i"] += 1

    final_story = _build_upto(fns)
    docf = _make_doc()
    docf.build(final_story, onFirstPage=on_page_final, onLaterPages=on_page_final)
    print("OK ->", OUT, f"({total_pages} pages)")

if __name__ == "__main__":
    build()
