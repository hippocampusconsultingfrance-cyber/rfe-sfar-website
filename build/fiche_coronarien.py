# -*- coding: utf-8 -*-
"""
Fiche de synthese - RFE SFAR/SFC (Societe francaise d'anesthesie et de
reanimation / Societe francaise de cardiologie), "Prise en charge du
coronarien qui doit etre opere en chirurgie non cardiaque", validee 2010-2011.
Auteurs coordinateurs : V. Piriou (Sfar), G. Derumeaux (SFC). Ann Fr Anesth
Reanim 30 (2011) e5-e29. doi:10.1016/j.annfar.2011.05.013. 26 pages source,
telecharge depuis sfar.org (wp-content/uploads/2015/10/2_AFAR_Prise-en-charge-
du-coronarien-qui-doit-etre-opere-en-chirurgie-non-cardiaque.pdf).

METHODOLOGIE : GRADE (force 1+/1-/2+/2-) CROISE avec un vote DELPHI
independant donnant un "accord" (fort ou faible) sur l'echelle 1-9 - CE SONT
DEUX AXES DISTINCTS dans cette source (contrairement a d'autres fiches du
corpus ou accord/grade sont confondus). La tres grande majorite des 65
recommandations formellement gradees sont Accord fort ; les Accord faible
sont signales individuellement.

COUVERTURE : 65 recommandations formellement taggees GRADE, sur les 4
"Questions" du texte (Q1 quantification du risque = 4 recs, Q2 examens
complementaires = 20 recs, Q3 revascularisation et medicaments = 41 recs,
Q4 strategie globale = 0 nouvelle recommandation gradee, synthese narrative
uniquement). Les 4 tableaux du corps du texte (score de Lee, capacite a
l'effort de Duke, indication ECG, gestion des AAP) et l'annexe 2
(classification CCS de l'angor) sont reproduits integralement. Les Figures 1
et 2 (algorithme general ; gestion des AAP post-angioplastie) sont de purs
schemas sans couche texte exploitable - retranscrites en tableau apres rendu
visuel direct du PDF source a 150dpi (pages e23/e27, confirme : diagramme
boites/fleches, pas de texte scramble).

ARGUMENTAIRE : volontairement condense (regle de projet 2026-09-14) - le
texte de chaque recommandation est raccourci aux elements cliniquement
actionnables (action, seuil, exception), la prose de justification
epidemiologique/statistique du corps du texte est omise. Precisions
posologiques/de seuils non deja dans la ligne de recommandation (ex. cible
FC beta-bloquant, delais de stent) sont conservees en note courte.

INCOHERENCES SOURCE DISCLOSED (regle 5, ne pas resoudre silencieusement) :
- R7 et R22 : taggees GRADE 1+ (positif) alors que leur texte est une
  recommandation negative ("il n'est pas recommande...") - incoherence de
  signe grade/texte, presente dans le texte source tel qu'extrait.
- R32 : le texte imprime "avant une chirurgie cardiaque" dans une section
  entierement consacree a la revascularisation preoperatoire avant chirurgie
  NON cardiaque - tres probable erreur typographique source, transcrite
  telle quelle avec [sic].
- Tableau 1 (score de Lee) : seuil de creatininemie imprime "177 mmol/L" -
  dimensionnellement incoherent avec "2,0 mg/dL" cite juste apres (2,0 mg/dL
  = 177 micromol/L, pas mmol/L) ; tres probable coquille d'unite, transcrite
  telle quelle avec la correction plausible entre crochets.
- Aucune section "Conflits d'interets"/"Liens d'interets" retrouvee dans le
  texte source extrait (grep complet du document) - flag explicite, ne pas
  assumer une absence reelle dans le PDF (section encadree possible non
  capturee par l'extraction).
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from style import *
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.units import mm

OUT = "/home/user/rfe-sfar-website/output/Fiche_SFAR_SFC_Coronarien_Chirurgie_Non_Cardiaque_2011.pdf"

SOURCE_TXT = ("Source : « Prise en charge du coronarien qui doit être opéré en chirurgie "
              "non cardiaque » — RFE SFAR/SFC, Ann Fr Anesth Réanim 30 (2011) e5-e29. "
              "Fiche de synthèse non officielle : se référer au texte intégral.")

def P(txt, style=S_CELL):
    return Paragraph(txt, style)

def chip(label, **kw):
    return grade_chip(label, **kw)

CW_FULL = PAGE_W - 2 * MARGIN

def theme_table(rows, col_widths, head=("Thème", "Détail")):
    data = [[P(head[0], S_HEAD_W), P(head[1], S_HEAD_W)]]
    for theme, detail in rows:
        data.append([P(theme, S_CELL_B), P(detail, S_CELL)])
    t = Table(data, colWidths=col_widths, repeatRows=1)
    style_cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), NAVY), ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTNAME", (0, 0), (-1, 0), FONT_BOLD), ("FONTSIZE", (0, 0), (-1, 0), 8),
        ("VALIGN", (0, 0), (-1, -1), "TOP"), ("ALIGN", (0, 1), (0, -1), "LEFT"),
        ("GRID", (0, 0), (-1, -1), 0.5, GREY_LIGHT),
        ("TOPPADDING", (0, 0), (-1, -1), 3.4), ("BOTTOMPADDING", (0, 0), (-1, -1), 3.4),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            style_cmds.append(("BACKGROUND", (0, i), (-1, i), BG_PANEL))
    t.setStyle(TableStyle(style_cmds))
    return t

TCW = [50 * mm, CW_FULL - 50 * mm]

def reco_table(rows, col_widths):
    """rows: (text, grade_label)."""
    data = [[P("Recommandation", S_HEAD_W), P("Grade", S_HEAD_W_C)]]
    for txt, grade in rows:
        data.append([P(txt, S_CELL), chip(grade)])
    t = Table(data, colWidths=col_widths, repeatRows=1)
    style_cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), NAVY), ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTNAME", (0, 0), (-1, 0), FONT_BOLD), ("FONTSIZE", (0, 0), (-1, 0), 8),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("ALIGN", (1, 0), (1, -1), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 0.5, GREY_LIGHT),
        ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            style_cmds.append(("BACKGROUND", (0, i), (-1, i), BG_PANEL))
    t.setStyle(TableStyle(style_cmds))
    return t

RCW = [CW_FULL - 18 * mm, 18 * mm]

def legend_flowable():
    chip_w = 15 * mm
    content_w = CW_FULL
    row = Table([[chip("1+", width=chip_w - 2 * mm), chip("1-", width=chip_w - 2 * mm),
                  chip("2+", width=chip_w - 2 * mm), chip("2-", width=chip_w - 2 * mm),
                  P("<b>GRADE</b> — 1+/1- : recommandation <b>forte</b> (« il est recommandé "
                    "de faire / ne pas faire ») ; 2+/2- : recommandation <b>optionnelle/"
                    "faible</b> (« il faut probablement faire / ne pas faire »). Axe "
                    "<b>Accord</b> (vote Delphi 1-9, distinct du GRADE) : fort par défaut "
                    "sauf mention « accord faible » explicite dans la ligne.", S_BADGE_HEAD)]],
                colWidths=[chip_w, chip_w, chip_w, chip_w, content_w - 4 * chip_w])
    row.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                              ("LEFTPADDING", (0, 0), (-1, -1), 1),
                              ("RIGHTPADDING", (0, 0), (-1, -1), 1),
                              ("TOPPADDING", (0, 0), (-1, -1), 0),
                              ("BOTTOMPADDING", (0, 0), (-1, -1), 0)]))
    return row

TOTAL_PAGES = {"n": 12}

def on_page(canvas, doc, page_title):
    header_band(canvas, doc, "SFAR / SFC — RFE, 2011 (AFAR 30, e5-e29)",
                "Coronarien opéré en chirurgie non cardiaque",
                page_title, icon_fn=lambda c, x, y: icon_shield(c, x, y, 13 * mm), color=NAVY)
    footer_band(canvas, doc, SOURCE_TXT, f"Page {doc.page} / {TOTAL_PAGES['n']}")

# ---------------------------------------------------------------------------
# Intro, méthodologie, Q1
# ---------------------------------------------------------------------------
LEE_ROWS = [
    ("Chirurgie à haut risque", "Vasculaire supra-inguinale, intrathoracique ou intrapéritonéale "
     "(1 pt — score classique uniquement, non compté dans le score clinique)"),
    ("Coronaropathie", "ATCD d'IDM, angor clinique, utilisation de dérivés nitrés, onde Q à "
     "l'ECG, ou test non invasif de la circulation coronaire positif (1 pt)"),
    ("Insuffisance cardiaque", "ATCD d'IC congestive, œdème pulmonaire, dyspnée nocturne "
     "paroxystique, crépitants bilatéraux, galop B3, ou redistribution vasculaire "
     "radiologique (1 pt)"),
    ("ATCD cérébrovasculaire", "AVC ischémique ou AIT (1 pt)"),
    ("Diabète insulino-traité", "(1 pt)"),
    ("Insuffisance rénale chronique", "Créatinine &gt; 2,0 mg/dL (imprimé « 177 mmol/L » dans "
     "la source — incohérent avec 2,0 mg/dL, très probablement 177 µmol/L) (1 pt)"),
]

MET_ROWS = [
    ("Excellente (&gt; 10 MET)", "Natation, tennis en simple, ski de fond, athlétisme, "
     "basketball — risque chirurgical estimé faible"),
    ("Très bonne à bonne (7-10 MET)", "Tennis en double, football, danse, gros travaux "
     "d'entretien, course courte distance, monter 2 étages ou plus, marche rapide à plat"),
    ("Modérée (4-7 MET)", "Monter 1 à 2 étages, ménage — risque chirurgical estimé faible"),
    ("Faible (&lt; 4 MET)", "Marche à plat 3-5 km/h, marche intérieure, toilette/habillage/"
     "repas — risque chirurgical estimé intermédiaire à élevé"),
    ("Non évaluable", "Seuil de décision : ≥ 4 MET → chirurgie sans exploration "
     "complémentaire ; &lt; 4 MET ou non évaluable → poursuivre la stratification (score "
     "de Lee, cf. Q4)"),
]

def _section_intro_q1():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Résumé :</b> première RFE conjointe Sfar/SFC (réflexion commune depuis 2008) "
        "sur le coronarien opéré en chirurgie non cardiaque, en 4 parties : quantification "
        "du risque (Q1), examens complémentaires (Q2), traitement médical/interventionnel "
        "(Q3), stratégie globale multidisciplinaire (Q4, algorithme). Message central : "
        "restreindre la revascularisation préopératoire systématique et les explorations non "
        "invasives non ciblées, privilégier l'optimisation du traitement médical "
        "(bêta-bloquant, statine) et une évaluation clinique structurée (risque "
        "chirurgical × risque patient × capacité à l'effort) formalisée par une fiche de "
        "liaison anesthésiste-cardiologue (Annexe 1).", S_BODY), bg=BG_PANEL, border=TEAL))
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("Méthodologie — GRADE + vote Delphi (deux axes distincts)"))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "La méthode GRADE dissocie le niveau de la recommandation (1 fort / 2 optionnel) du "
        "niveau de preuve scientifique sous-jacent. <b>Grade 1+</b> : recommandé de faire ; "
        "<b>Grade 2+</b> : probablement recommandé de faire ; <b>Grade 1−</b> : recommandé de "
        "ne pas faire ; <b>Grade 2−</b> : probablement recommandé de ne pas faire. "
        "Indépendamment, chaque recommandation a été soumise au vote de tous les experts "
        "(échelle Delphi 1-9) : <b>accord fort</b> si tous les experts (sauf un) ont coté "
        "entre 7 et 9 ; <b>accord faible</b> si tous (sauf un) ont coté entre 4 et 9 avec une "
        "majorité entre 7 et 9.", S_BODY_SM))
    story.append(Spacer(1, 1.5 * mm))
    story.append(legend_flowable())
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Question 1 — Quantification du risque (4 recommandations)"),
        Spacer(1, 1.5 * mm),
        reco_table([
            ("<b>R1</b> — Chez le patient coronarien ou à risque de maladie coronaire "
             "(Lee clinique ≥ 2) opéré d'une chirurgie non cardiaque à risque intermédiaire "
             "ou élevé, il est recommandé de réaliser de manière répétée dans les 48 "
             "premières heures postopératoires : ECG, dosage de troponine Ic, mesure de "
             "l'hémoglobine.", "1+"),
            ("<b>R2</b> — Chez le patient à risque de maladie coronaire opéré d'une "
             "chirurgie à risque élevé, il n'est pas recommandé de doser en postopératoire "
             "myoglobine, isoenzyme CK-MB, BNP/NT-proBNP, CRP/hsCRP.", "1-"),
            ("<b>R3</b> — Il est recommandé d'évaluer le risque périopératoire sur 3 "
             "critères : risque lié à l'intervention chirurgicale, risque lié à l'état "
             "cardiaque du patient, capacité à effectuer un effort.", "1+"),
            ("<b>R4</b> — Il n'est pas recommandé de doser en préopératoire BNP/NT-proBNP, "
             "troponine, CRP/hsCRP pour évaluer le risque périopératoire.", "1-"),
        ], RCW),
    ]))
    story.append(Spacer(1, 1.8 * mm))
    story.append(P(
        "<b>Risque chirurgical</b> (fréquence d'événements cardiaques périopératoires) : "
        "<b>faible</b> &lt; 1 % (chirurgie superficielle, mammaire, ophtalmologique, "
        "ambulatoire, endoscopie) ; <b>intermédiaire</b> 1-5 % (intra/rétropéritonéale, "
        "thoracique, carotidienne, tête/cou, orthopédique, prostatique, fort potentiel "
        "hémorragique) ; <b>majeur</b> &gt; 5 % (aortique y compris endoluminale, vasculaire "
        "majeure/périphérique ; fracture de hanche du sujet âgé en urgence assimilable au "
        "haut risque).", S_BODY_SM))
    story.append(Spacer(1, 1.5 * mm))
    story.append(KeepTogether([
        P("<b>Tableau 1 — Score de risque cardiaque de Lee</b> (score clinique "
          "utilisé en pratique = somme des points ci-dessous, hors item chirurgie)",
          S_CELL_B),
        Spacer(1, 1 * mm),
        theme_table(LEE_ROWS, TCW, head=("Facteur", "Définition (1 point chacun)")),
    ]))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "Incidence de complications cardiaques majeures (population de Lee, chirurgie "
        "programmée, &gt; 50 ans) : 0,4 % / 0,9 % / 7 % / 11 % pour 0, 1, 2 ou 3 facteurs "
        "cliniques respectivement.", S_NOTE))
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        P("<b>Tableau 2 — Capacité à l'effort</b> (échelle de Duke adaptée ; "
          "1 MET = VO2 3,5 mL/kg/min, homme 40 ans/70 kg)", S_CELL_B),
        Spacer(1, 1 * mm),
        theme_table(MET_ROWS, TCW, head=("Aptitude physique", "Activités / seuil décisionnel")),
    ]))
    return story

# ---------------------------------------------------------------------------
# Q2 — Examens complémentaires
# ---------------------------------------------------------------------------
ECG_MATRIX_ROWS = [
    ("Risque chirurgical faible", "Patient à risque faible : Non — Intermédiaire : Non — "
     "Majeur : à discuter"),
    ("Risque chirurgical intermédiaire", "Faible : à discuter si âge ≥ 50 ans — Intermédiaire : "
     "à discuter si âge ≥ 50 ans — Majeur : faire"),
    ("Risque chirurgical majeur", "Faible : faire — Intermédiaire : faire — Majeur : faire"),
]

def _section_q2():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Question 2 — Examens complémentaires (20 recommandations)"),
        Spacer(1, 1.5 * mm),
        P("Un examen complémentaire ne se justifie que s'il est susceptible de modifier la "
          "quantification du risque et/ou la stratégie périopératoire, et seulement chez les "
          "patients à haut risque clinique (score de Lee &gt; 2).", S_BODY_SM),
    ]))
    story.append(Spacer(1, 1.8 * mm))
    story.append(P("<b>Principe général et ECG</b>", S_H2))
    story.append(Spacer(1, 1 * mm))
    story.append(reco_table([
        ("<b>R5</b> — Il n'est pas recommandé de réaliser des examens spécialisés "
         "(échocardiographie dobutamine, scintigraphie thallium-persantine) lorsque leurs "
         "résultats ne sont pas susceptibles de modifier la stratégie périopératoire.", "1-"),
        ("<b>R6</b> — Il n'est pas recommandé de dépister systématiquement la coronaropathie "
         "chez un patient asymptomatique, quelle que soit la chirurgie.", "1-"),
        ("<b>R7</b> [sic — texte négatif taggé 1+, voir disclosure] — Il n'est pas recommandé "
         "de refaire un ECG (ou une autre exploration) chez un coronarien ayant un bilan "
         "cardiologique et un ECG de moins d'un an disponibles, en l'absence d'événement "
         "intercurrent ; l'ECG doit être transmis à la consultation d'anesthésie.", "1+"),
        ("<b>R8</b> — Il est recommandé de faire un ECG de repos 12 dérivations avant "
         "chirurgie vasculaire artérielle pour maladie athéromateuse avec facteurs de "
         "risque (score de Lee).", "1+"),
        ("<b>R9</b> — Il est suggéré de faire un ECG de repos avant chirurgie vasculaire "
         "même sans facteur de risque au score de Lee, pour disposer d'un ECG de "
         "référence.", "2+"),
        ("<b>R10</b> — Il est recommandé de faire un ECG de repos chez tout patient &gt; 50 "
         "ans ayant &gt; 1 facteur de risque (score de Lee) avant chirurgie à risque "
         "intermédiaire ou élevé.", "1+"),
        ("<b>R11</b> — Il n'est pas recommandé de réaliser un ECG systématique avant "
         "chirurgie à risque faible.", "1-"),
        ("<b>R12</b> — Il est recommandé de réaliser un ECG 12 dérivations (avec V3R, V4R, "
         "V7-V9) en périopératoire chez tout patient présentant une symptomatologie "
         "cardiologique de diagnostic non évident.", "1+"),
    ], RCW))
    story.append(Spacer(1, 1.5 * mm))
    story.append(KeepTogether([
        P("<b>Tableau 3 — Indication de l'ECG préopératoire</b> selon le risque "
          "chirurgical et le risque patient", S_CELL_B),
        Spacer(1, 1 * mm),
        theme_table(ECG_MATRIX_ROWS, TCW, head=("Risque chirurgical", "Selon risque patient (faible / intermédiaire / majeur)")),
    ]))
    story.append(Spacer(1, 2.5 * mm))
    story.append(P("<b>Holter, ECG d'effort, échocardiographie</b>", S_H2))
    story.append(Spacer(1, 1 * mm))
    story.append(reco_table([
        ("<b>R13</b> — Il n'est pas recommandé de prescrire un Holter ECG pour prédire le "
         "risque d'événement cardiaque périopératoire.", "1-"),
        ("<b>R14</b> — Il n'est pas recommandé de réaliser un ECG d'effort — surtout s'il "
         "risque d'être sous-maximal (&lt; 85 % FMT) — pour prédire le risque ischémique "
         "périopératoire.", "1-"),
        ("<b>R15</b> — Il n'est pas recommandé de prescrire une échocardiographie de repos "
         "pour évaluer le risque coronaire périopératoire.", "1-"),
        ("<b>R16</b> — Il est recommandé de prescrire une échocardiographie de stress si le "
         "niveau de risque impose un dépistage et si l'examen peut être réalisé/interprété "
         "selon les recommandations de l'EAE dans le centre.", "1+"),
        ("<b>R17</b> — Il est recommandé de rediscuter l'indication opératoire et de "
         "proposer un complément d'investigation si l'échocardiographie de stress est "
         "anormale sur &gt; 4/17 segments (avec ou sans dysfonction/dilatation VG).", "1+"),
    ], RCW))
    story.append(Spacer(1, 1.8 * mm))
    story.append(P("<b>Scintigraphie, choix du test, coronarographie, imagerie coupe</b>", S_H2))
    story.append(Spacer(1, 1 * mm))
    story.append(reco_table([
        ("<b>R18</b> — Il est recommandé de prescrire une scintigraphie myocardique si le "
         "niveau de risque impose un dépistage et si l'examen peut être réalisé/interprété "
         "dans le centre avec une expertise suffisante.", "1+"),
        ("<b>R19</b> — Il est recommandé de proposer un complément d'investigation, en "
         "tenant compte du contexte chirurgical, si la scintigraphie retrouve un défect "
         "perfusionnel &gt; 20 %.", "1+"),
        ("<b>R20</b> — Il est recommandé de discuter le choix scintigraphie/échographie de "
         "stress selon les disponibilités et compétences locales (en tenant compte du "
         "caractère irradiant de la scintigraphie) ; une feuille de liaison "
         "anesthésiste-cardiologue est encouragée (indication, score de Lee, tolérance à "
         "l'effort, traitements, justification du test → résultats et attitude "
         "proposée).", "1+"),
        ("<b>R21</b> — Il est recommandé que le cardiologue ayant réalisé l'examen propose "
         "à l'équipe d'anesthésie-réanimation des éléments de prise en charge "
         "(optimisation du traitement, discussion d'une revascularisation, report de "
         "chirurgie) selon le contexte opératoire.", "1+"),
        ("<b>R22</b> [sic — texte négatif taggé 1+, voir disclosure] — Il n'est pas "
         "recommandé de prescrire en première intention une coronarographie pour prédire "
         "le risque de complication ischémique postopératoire.", "1+"),
        ("<b>R23</b> — Il est recommandé que toute décision de coronarographie avant "
         "chirurgie non cardiaque programmée soit collégiale et tracée dans le "
         "dossier.", "1+"),
        ("<b>R24</b> — Il n'est pas recommandé de proposer un coroscanner, une IRM ou une "
         "TEP pour dépister le risque coronaire en période préopératoire.", "1-"),
    ], RCW))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<i>Disclosure :</i> R7 et R22 sont toutes deux imprimées avec un tag « GRADE 1+ » "
        "alors que leur texte formule une recommandation négative (« il n'est pas "
        "recommandé... ») — incohérence de signe grade/texte présente dans le document "
        "source tel qu'extrait, non résolue ici (les deux tags sont reproduits tels quels "
        "plutôt que « corrigés » en 1−, faute de pouvoir confirmer l'intention exacte des "
        "experts sans accès à une version PDF haute résolution du tableau récapitulatif).",
        S_NOTE))
    return story

# ---------------------------------------------------------------------------
# Q3 — Revascularisation et médicaments
# ---------------------------------------------------------------------------
def _section_q3a():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Question 3 — Revascularisation et médicaments (41 recommandations)"),
        Spacer(1, 1.5 * mm),
        P("<b>Indications de la revascularisation myocardique préopératoire</b>", S_H2),
    ]))
    story.append(Spacer(1, 1 * mm))
    story.append(reco_table([
        ("<b>R25</b> — La décision de revascularisation avant chirurgie non cardiaque doit "
         "être consensuelle entre praticiens, tracée dans le dossier (bénéfices/risques/"
         "alternatives, optimisation du traitement médical) et expliquée au patient.", "1+"),
        ("<b>R26</b> — La revascularisation myocardique préalable à une chirurgie non "
         "cardiaque doit rester exceptionnelle.", "1+"),
        ("<b>R27</b> — Situation clinique pouvant faire envisager une revascularisation : "
         "syndrome coronaire aigu préopératoire, avec ou sans sus-décalage ST. "
         "<i>(accord faible)</i>", "1+"),
        ("<b>R28</b> — Situation clinique : coronaropathie stable avec statut anatomique ou "
         "ischémique mettant en jeu un territoire myocardique important. "
         "<i>(accord faible)</i>", "2+"),
        ("<b>R29</b> — Situation anatomique : atteinte du tronc commun gauche ou des trois "
         "troncs coronaires, si patient symptomatique et/ou ischémie authentifiée sur "
         "≥ 3 segments.", "1+"),
        ("<b>R30</b> — Situation anatomique : occlusion d'un tronc coronaire dans un statut "
         "anatomique particulier (tronc commun, ou statut pluritronculaire impliquant "
         "l'IVA).", "1+"),
        ("<b>R31</b> — En dehors de ces situations, il n'est pas recommandé de "
         "revasculariser, notamment en cas d'occlusion chronique avec ischémie/viabilité "
         "modérées (bénéfice non démontré).", "1-"),
    ], RCW))
    story.append(Spacer(1, 1.8 * mm))
    story.append(P("<b>Choix de la technique de revascularisation</b>", S_H2))
    story.append(Spacer(1, 1 * mm))
    story.append(reco_table([
        ("<b>R32</b> [sic] — Le pontage aortocoronaire est la technique de référence "
         "« avant une chirurgie cardiaque » [texte source — incohérence probable, cette "
         "section traite de chirurgie NON cardiaque] si : atteinte du "
         "tronc commun/tritronculaire, altération de la FEVG, ou geste différable de "
         "quelques semaines. <i>(accord faible)</i>", "1+"),
        ("<b>R33</b> — L'angioplastie coronaire préopératoire n'est pas recommandée en "
         "prévention des événements ischémiques périopératoires, sauf situation clinique "
         "instable (difficultés de gestion périopératoire des antiplaquettaires) ; "
         "envisageable en cas de syndrome coronaire aigu préopératoire.", "1-"),
        ("<b>R34</b> — Si angioplastie réalisée avant chirurgie non cardiaque, il est "
         "recommandé de poser une endoprothèse nue (4-6 semaines de double "
         "antiagrégation seulement, limitant le report de chirurgie).", "1+"),
        ("<b>R35</b> — La chirurgie après endoprothèse nue doit être réalisée au minimum "
         "6 semaines plus tard, idéalement 3 mois plus tard.", "1+"),
        ("<b>R36</b> — Il n'est pas recommandé de poser une endoprothèse active/recouverte "
         "(double antiagrégation prolongée ≥ 1 an, voire plus).", "1-"),
        ("<b>R37</b> — Cette attitude peut être reconsidérée si chirurgie fonctionnelle non "
         "vitale différable ≥ 1 an, ou chirurgie à très faible risque hémorragique "
         "réalisable sous double antiagrégation.", "2+"),
        ("<b>R38</b> — Si une endoprothèse coronaire est choisie, la conduite à tenir sur "
         "le traitement antiplaquettaire périopératoire doit être discutée et transmise "
         "aux équipes anesthésie/chirurgie (risque hémorragique vs thrombotique).", "1+"),
    ], RCW))
    return story

def _section_q3b():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        P("<b>Bêta-bloquants</b>", S_H2),
    ]))
    story.append(Spacer(1, 1 * mm))
    story.append(reco_table([
        ("<b>R39</b> — Pour tout traitement bêta-bloquant, la posologie doit être ajustée "
         "pour une cible de FC préopératoire de 60-70 b/min, sans hypotension.", "1+"),
        ("<b>R40</b> — Il est recommandé de poursuivre en périopératoire un traitement "
         "bêta-bloquant prescrit pour insuffisance coronaire (avec ou sans trouble du "
         "rythme/insuffisance cardiaque associés).", "1+"),
        ("<b>R41</b> — La mise en route préopératoire d'un bêta-bloquant est recommandée "
         "chez les patients ayant une insuffisance coronaire clinique ou des signes "
         "d'ischémie à un examen non invasif.", "1+"),
        ("<b>R42</b> — Chez les patients à risque CV élevé/intermédiaire (score de Lee "
         "clinique ≥ 2, hors item chirurgie) opérés à haut risque, il peut être recommandé "
         "de débuter un bêta-bloquant (en tenant compte du risque d'hypotension/"
         "bradycardie peropératoire) ; pour une chirurgie à risque intermédiaire, la "
         "décision est plus discutable.", "2+"),
        ("<b>R43</b> — Il n'est pas recommandé de débuter un bêta-bloquant avant chirurgie "
         "à faible risque.", "1-"),
        ("<b>R44</b> — Chez les patients à faible risque, la mise en route préopératoire "
         "d'un bêta-bloquant n'est pas indiquée.", "1-"),
        ("<b>R45</b> — Si un traitement est débuté en préopératoire, un agent "
         "cardiosélectif sans activité sympathomimétique intrinsèque est recommandé "
         "(aténolol, métoprolol, bisoprolol).", "1+"),
        ("<b>R46</b> — Le traitement doit être administré lors de la prémédication, à la "
         "dose habituelle.", "1+"),
        ("<b>R47</b> — En peropératoire, il est recommandé de surveiller strictement FC et "
         "PA, et de traiter hypotension et/ou bradycardie par les mesures "
         "appropriées.", "1+"),
    ], RCW))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>Contexte (non un tag de recommandation) :</b> bêta-blocage périopératoire — "
        "réduction du risque d'IDM périopératoire (−28 à −35 %) et d'ischémie myocardique "
        "(−64 %), sans effet sur la mortalité CV ; l'essai POISE a montré +28 % de "
        "mortalité toute cause et un doublement des AVC (1,0 % vs 0,5 %) sous "
        "bêta-blocage — d'où la prudence sur l'initiation large et la cible de FC stricte "
        "ci-dessus plutôt qu'une bêta-blocage systématique non titré.", S_BODY_SM))
    story.append(Spacer(1, 2.2 * mm))
    story.append(KeepTogether([
        P("<b>Alpha2-agonistes</b>", S_H2),
        Spacer(1, 1 * mm),
        reco_table([
            ("<b>R48</b> — Bien que les alpha2-agonistes réduisent le risque de décès et "
             "d'IDM postopératoire chez le coronarien opéré de chirurgie vasculaire, leur "
             "administration n'est probablement pas à recommander (retentissement "
             "hémodynamique). <i>(accord faible)</i>", "2-"),
            ("<b>R49</b> — Il n'est probablement pas recommandé d'administrer un "
             "alpha2-agoniste chez le coronarien/patient à risque CV pour réduire le "
             "risque périopératoire en chirurgie non vasculaire. <i>(accord faible)</i>",
             "2-"),
        ], RCW),
    ]))
    story.append(Spacer(1, 2.2 * mm))
    story.append(P("<b>Statines et hypolipémiants</b>", S_H2))
    story.append(Spacer(1, 1 * mm))
    story.append(reco_table([
        ("<b>R50</b> — Si une statine est indiquée mais non prescrite, il est recommandé de "
         "la débuter avant chirurgie vasculaire, si possible au moins 1 semaine "
         "auparavant.", "1+"),
        ("<b>R51</b> — Les patients devant subir une chirurgie vasculaire artérielle "
         "pourraient bénéficier de l'introduction d'une statine.", "2+"),
        ("<b>R52</b> — Un traitement par statine chronique doit être poursuivi en "
         "périopératoire : administré le soir précédant l'intervention et repris le soir "
         "de l'intervention.", "1+"),
        ("<b>R53</b> — Il n'y a pas d'indication ni de bénéfice démontré à prescrire un "
         "hypolipémiant autre qu'une statine en périopératoire.", "1-"),
    ], RCW))
    return story

AAP_ROWS = [
    ("Risque thrombotique élevé¹ + risque hémorragique élevé",
     "(a) retarder le geste ; (b) réaliser sous ≥ 1 antiplaquettaire (sur-risque "
     "hémorragique jugé acceptable) ; (c) arrêt clopidogrel &lt; 5 j et aspirine &lt; 3 j "
     "sans substitution. Hiérarchie : (a) préféré à (b), préféré à (c)². Reprise "
     "postopératoire dès hémostase satisfaisante."),
    ("Risque thrombotique élevé¹ + risque hémorragique intermédiaire",
     "Retarder le geste, ou réaliser sous 1 antiplaquettaire."),
    ("Risque thrombotique élevé¹ + risque hémorragique faible",
     "Retarder le geste, ou réaliser sous bithérapie."),
    ("Risque thrombotique intermédiaire³ + risque hémorragique élevé",
     "(a) réaliser sous 1 antiplaquettaire ; (b) remplacer clopidogrel par aspirine (si "
     "pas de CI) ; (c) arrêt aspirine &lt; 3 j². Reprise postopératoire dès hémostase "
     "satisfaisante."),
    ("Risque thrombotique intermédiaire³ + risque hémorragique intermédiaire ou faible",
     "Réaliser le geste sous clopidogrel ou aspirine."),
]

def _section_q3c():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        P("<b>Agents antiplaquettaires (AAP)</b>", S_H2),
        Spacer(1, 1 * mm),
    ]))
    story.append(reco_table([
        ("<b>R54</b> — Une endoprothèse active posée dans les 12 mois précédents "
         "implique la poursuite de la double thérapie antiplaquettaire.", "1+"),
        ("<b>R55</b> — Une endoprothèse nue implique une double antiagrégation pendant "
         "4 à 6 semaines.", "1+"),
        ("<b>R56</b> — La survenue d'un syndrome coronaire aigu implique si possible une "
         "double antiagrégation pendant 1 an ; si risque hémorragique périopératoire "
         "élevé, l'interruption du clopidogrel avec poursuite de l'aspirine peut être "
         "indiquée.", "2+"),
        ("<b>R57</b> — En cas d'arrêt d'un antiplaquettaire (aspirine, clopidogrel), il est "
         "recommandé de réaliser la chirurgie après 5 jours d'arrêt (réduit le risque "
         "hémorragique, limite le risque thrombotique — maximal au-delà du 8e jour "
         "d'arrêt).", "1+"),
        ("<b>R58</b> — En cas de traitement par aspirine seule, il est recommandé de le "
         "poursuivre, sauf contre-indication liée à un très haut risque hémorragique "
         "chirurgical.", "1+"),
        ("<b>R59</b> — Si le patient est sous clopidogrel seul et que la chirurgie ne peut "
         "pas être réalisée sous ce médicament, il est recommandé de le remplacer par de "
         "l'aspirine (en l'absence de CI).", "1+"),
        ("<b>R60</b> — Si le patient est sous bithérapie, il est recommandé de conserver "
         "au moins un antiplaquettaire, idéalement l'aspirine, sauf contre-indication "
         "hémorragique.", "1+"),
        ("<b>R61</b> — Après la chirurgie et en concertation avec le chirurgien, il est "
         "recommandé de reprendre précocement le traitement antiplaquettaire interrompu "
         "(dose de charge possible si risque thrombotique élevé).", "2+"),
    ], RCW))
    story.append(Spacer(1, 1.5 * mm))
    story.append(KeepTogether([
        P("<b>Tableau 4 — Gestion des antiplaquettaires en période périopératoire</b>",
          S_CELL_B),
        Spacer(1, 1 * mm),
        theme_table(AAP_ROWS, TCW, head=("Situation (risque thrombotique × hémorragique)", "Conduite à tenir")),
    ]))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "¹ Risque thrombotique élevé : stent nu &lt; 4-6 semaines, stent actif &lt; 1 an, "
        "syndrome coronaire aigu &lt; 1 an, ou bithérapie en cours. ² Recommandations "
        "hiérarchiques, non optionnelles : (c) est dégradée par rapport à (b), qui est "
        "dégradée par rapport à (a). ³ Risque thrombotique intermédiaire : prévention "
        "secondaire sous monothérapie. Risque hémorragique déterminé a priori par les "
        "listes des sociétés savantes ; à défaut, jugé acceptable/inacceptable face au "
        "risque de l'arrêt.", S_NOTE))
    story.append(Spacer(1, 2.2 * mm))
    story.append(KeepTogether([
        P("<b>IEC / ARA2, dérivés nitrés, inhibiteurs calciques</b>", S_H2),
        Spacer(1, 1 * mm),
        reco_table([
            ("<b>R62</b> — Chez les coronariens, il est recommandé de maintenir les IEC/"
             "ARA2 en périopératoire lorsqu'ils sont prescrits pour une insuffisance "
             "cardiaque (tenir compte alors du risque d'hypotension en chirurgie majeure "
             "ou rachianesthésie).", "1+"),
            ("<b>R63</b> — Il est recommandé d'interrompre un IEC/ARA2 au moins 12 h avant "
             "l'intervention lorsqu'il constitue un traitement de fond de "
             "l'hypertension.", "1+"),
            ("<b>R64</b> — L'administration de dérivés nitrés (quelle que soit la voie) "
             "n'est pas recommandée en prévention des complications cardiaques "
             "périopératoires.", "1-"),
            ("<b>R65</b> — Il n'est pas recommandé d'administrer un inhibiteur calcique "
             "pour la prévention des complications cardiaques périopératoires.", "1-"),
        ], RCW),
    ]))
    return story

# ---------------------------------------------------------------------------
# Q4 — Algorithme global (Figures 1 et 2, transcrites depuis rendu visuel
# direct du PDF a 150dpi, pages e23 et e27 - aucune couche texte exploitable
# pour ces deux schemas boites/fleches).
# ---------------------------------------------------------------------------
FIG1_ROWS = [
    ("1. Urgence ?", "Chirurgie urgente/vitale → opérer sans délai (évaluation cardio "
     "limitée au dépistage du risque et à l'optimisation péri/postopératoire). Chirurgie "
     "non urgente → étape 2."),
    ("2. Instabilité cardiaque ?", "SCA récent, angor CCS III-IV, IC décompensée, "
     "valvulopathie sévère, trouble du rythme/conduction significatif → différer/"
     "contre-indiquer la chirurgie non cardiaque, traiter la pathologie cardiaque "
     "d'abord. Patient stable → étape 3."),
    ("3. Risque chirurgical", "Faible → opérer sans exploration cardiaque "
     "complémentaire. Intermédiaire ou élevé → étape 4."),
    ("4. Capacité fonctionnelle & score de Lee", "≥ 4 MET, asymptomatique → opérer "
     "(poursuite bêta-bloquant/statine en cours, ECG réalisé, pas de test de stress). "
     "&lt; 4 MET ou non évaluable → stratifier par le score de Lee."),
    ("4a. 0-1 facteur de Lee", "Opérer (sauf angor de novo classe I-II découvert en "
     "consultation d'anesthésie → avis cardiologique, décision collégiale du moment du "
     "bilan, ajustement du traitement)."),
    ("4b. ≥ 2 facteurs de Lee (chirurgie vasculaire) ou ≥ 3 facteurs (chirurgie "
     "intermédiaire/élevée non vasculaire)",
     "La RFE française privilégie un test d'ischémie fonctionnelle (scintigraphie ou "
     "échographie de stress, discuté collégialement) plutôt que le simple contrôle de "
     "FC par bêta-bloquant retenu par certaines recommandations européennes."),
    ("4c. Résultat du test d'ischémie", "Ischémie ≥ 20 % du myocarde (scintigraphie) ou "
     "&gt; 4/17 segments (écho de stress) → envisager une revascularisation "
     "préopératoire (bénéfice « modéré », discuté selon les essais CARP/DECREASE-5). "
     "Ischémie moindre → traitement médical optimisé, pas de revascularisation."),
]

FIG2_ROWS = [
    ("Chirurgie programmée &lt; 15 jours après angioplastie", "Contre-indiquée (période à "
     "risque catastrophique), sauf urgence vitale."),
    ("Chirurgie indispensable 15-30 jours après angioplastie", "Angioplastie au ballon "
     "seule à privilégier (pas de stent) ; chirurgie sous aspirine."),
    ("Chirurgie différable ≥ 6 semaines", "Stent nu à privilégier + 4 semaines de double "
     "antiagrégation, chirurgie réalisée 1 à 1,5 semaine après la fin de la double "
     "thérapie."),
    ("Stent actif (endoprothèse recouverte)", "Contre-indiqué si chirurgie non cardiaque "
     "prévue dans l'année suivante."),
    ("Chirurgie à risque hémorragique faible/modéré, sur avis collégial", "Poursuivre "
     "clopidogrel + aspirine pendant la chirurgie, même après angioplastie au "
     "ballon ou stent nu."),
    ("Chirurgie urgente/non programmée après angioplastie récente (&lt; 1 mois stent nu, "
     "&lt; 1 an stent actif), double thérapie non poursuivable",
     "Avis d'experts (non randomisé) : maintenir l'aspirine, arrêter le clopidogrel "
     "3-5 j avant, le reprendre dès que possible en postopératoire (&lt; 48 h), dose de "
     "charge si possible."),
]

CCS_ROWS = [
    ("Classe I", "Les efforts physiques de la vie courante n'entraînent pas d'angor ; "
     "celui-ci n'apparaît que lors d'efforts intenses, abrupts ou prolongés (ski, course "
     "modérée, déneigement possibles sans symptôme)."),
    ("Classe II", "Limitation légère : angor à la marche rapide/montée rapide d'escaliers, "
     "en côte, après repas, au froid, à l'émotion, au décubitus (primo décubitus), ou à marche &gt; 2 blocs/"
     "2-3 étages à vitesse habituelle. Jardinage, roller, marche 6 km/h, activité "
     "sexuelle possibles."),
    ("Classe III", "Limitation marquée : angor à 1-2 blocs de marche à plat ou 1 étage à "
     "vitesse normale. Habillage, toilette, marche lente (4 km/h) ou efforts domestiques "
     "de faible intensité possibles."),
    ("Classe IV", "Impossibilité de tout effort sans angor, pouvant apparaître même au "
     "repos (patient incapable d'un effort &gt; 2 MET sans angor)."),
]

def _section_q4_sources():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Question 4 — Stratégie globale multidisciplinaire (algorithme)"),
        Spacer(1, 1.5 * mm),
        P("Aucune nouvelle recommandation formellement gradée dans cette section : synthèse "
          "narrative qui ré-applique les grades établis en Q1-Q3 sous forme d'un algorithme "
          "décisionnel en 4 étapes (Figure 1), complété par la gestion spécifique des "
          "antiplaquettaires après angioplastie récente (Figure 2). Les deux figures sont "
          "de purs schémas boîtes/flèches du PDF source (pages e23 et e27), sans couche "
          "texte exploitable — retranscrites ci-dessous après lecture visuelle directe du "
          "rendu à 150dpi.", S_BODY_SM),
    ]))
    story.append(Spacer(1, 1.8 * mm))
    story.append(P("<b>Figure 1 — Algorithme général de prise en charge du coronarien avant "
                    "chirurgie non cardiaque</b>", S_CELL_B))
    story.append(Spacer(1, 1 * mm))
    story.append(theme_table(FIG1_ROWS, TCW, head=("Étape", "Conduite")))
    story.append(Spacer(1, 2.2 * mm))
    story.append(P("<b>Figure 2 — Gestion du traitement antiplaquettaire après angioplastie "
                    "préalable à une chirurgie non cardiaque</b>", S_CELL_B))
    story.append(Spacer(1, 1 * mm))
    story.append(theme_table(FIG2_ROWS, TCW, head=("Situation", "Conduite")))
    story.append(Spacer(1, 2.2 * mm))
    story.append(P(
        "<b>Autres points narratifs de la Q4</b> (non gradés) : l'HTA n'est pas en soi une "
        "contre-indication à la chirurgie non cardiaque ; une valvuloplastie percutanée "
        "peut être « raisonnable » avant chirurgie chez un patient à rétrécissement "
        "aortique sévère inopérable/à comorbidités lourdes ; en cas de fibrillation "
        "auriculaire à haut risque embolique, un relais par HBPM est envisagé selon les "
        "recommandations HAS 2008 sur les AVK ; une surveillance postopératoire "
        "troponine/ECG/segment ST est recommandée chez les patients à risque opérés en "
        "chirurgie à risque intermédiaire/élevé.", S_BODY_SM))
    story.append(Spacer(1, 2.5 * mm))
    story.append(P("<b>Annexe 2 — Classification canadienne (CCS) de l'angor</b>", S_CELL_B))
    story.append(Spacer(1, 1 * mm))
    story.append(theme_table(CCS_ROWS, TCW, head=("Classe", "Définition / activités")))
    story.append(Spacer(1, 2.5 * mm))
    story.append(section_bar("Déclaration d'intérêts, sources et traçabilité", color=GREY))
    story.append(Spacer(1, 2 * mm))
    story.append(P(
        "<b>Déclaration d'intérêts :</b> aucune section « conflits/liens d'intérêts » "
        "retrouvée dans le texte source tel qu'extrait — flag explicite, ne pas assumer "
        "une absence réelle dans le PDF (section encadrée possible non capturée par "
        "l'extraction de texte).", S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>Document source :</b> « Prise en charge du coronarien qui doit être opéré en "
        "chirurgie non cardiaque / Perioperative assessment of cardiac risk patient in "
        "non-cardiac surgery » — RFE Sfar/SFC. Coordinateurs : G. Derumeaux (SFC), "
        "V. Piriou (Sfar) ; aide méthodologique E. Marret. Coordinateurs par question : "
        "Q1 C. Girard/G. Vanzetto ; Q2 E. Donal/D. Longrois ; Q3 E. Samain/M. Elbaz ; "
        "Q4 J. Machecourt/V. Piriou. Groupes de lecture : CA de la Sfar (17 décembre 2010) "
        "et CA de la SFC (octobre 2010).", S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P("<b>Version :</b> Ann Fr Anesth Réanim 30 (2011) e5-e29. "
                    "doi:10.1016/j.annfar.2011.05.013.", S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P("<b>Méthodologie :</b> GRADE (1+/1-/2+/2-) croisé avec un accord Delphi "
                    "(fort/faible) distinct — voir détail en page 1.", S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>URL source :</b> https://sfar.org/wp-content/uploads/2015/10/"
        "2_AFAR_Prise-en-charge-du-coronarien-qui-doit-etre-opere-en-chirurgie-non-"
        "cardiaque.pdf", S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>Couverture :</b> intégralité des 65 recommandations formellement gradées "
        "(Q1-Q3), des 4 tableaux du corps du texte, de l'Annexe 2 (classification CCS) et "
        "des Figures 1-2 (retranscrites depuis rendu visuel). L'Annexe 1 (fiche de "
        "liaison anesthésiste-cardiologue, un formulaire de recueil de données sans "
        "contenu recommandationnel propre) et les synthèses narratives non gradées de Q4 "
        "sur l'HTA/RAC/FA sont résumées plutôt que reproduites in extenso. Scope "
        "explicitement exclu par la source elle-même : la gestion périopératoire des "
        "traitements chroniques en général, objet de recommandations Sfar antérieures "
        "distinctes.", S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>Références citées (3) :</b> 1. Sicari R, Nihoyannopoulos P, Evangelista A. "
        "Stress Echocardiography Expert Consensus Statement, Eur Heart J 2009;30:278-89. "
        "2. Poldermans D et al., Guidelines for pre-operative cardiac risk assessment "
        "(ESC/ESA), Eur J Anaesthesiol 2010;27:92-137. 3. Goldman L, Hashimoto B, Cook EF, "
        "Loscalzo A. Comparative reproducibility and validity of systems for assessing "
        "cardiovascular functional class, Circulation 1981;64:1227-34 (classification "
        "CCS, Annexe 2).", S_SOURCE))
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Avertissement — document de 2011 :</b> cette fiche de synthèse indépendante "
        "reprend l'intégralité des 65 recommandations gradées du texte source (dont les "
        "Figures 1 et 2, transcrites depuis un rendu visuel du PDF faute de couche texte "
        "exploitable pour ces schémas), mais ne remplace pas le texte intégral et n'est "
        "ni éditée ni validée par la Sfar ou la SFC. Les stratégies de gestion "
        "périopératoire des antiplaquettaires, les délais de double antiagrégation après "
        "stent et les seuils d'indication des tests d'ischémie ayant pu évoluer depuis "
        "2011 (recommandations ESC/ESC plus récentes, nouveaux stents), se référer à un "
        "avis cardiologique spécialisé et aux recommandations actualisées avant toute "
        "décision thérapeutique.", S_BODY_SM), bg=GREY_LIGHT, border=GREY))
    return story

def _q3_full():
    story = _section_q3a()
    story.extend(_section_q3b())
    story.extend(_section_q3c())
    return story

def _q1_q2_full():
    # Merged (no forced PageBreak) - Q1 + Tableau 2 leave page 1 under-filled if
    # Q2 starts on a fresh page; letting Q2 flow directly after Tableau 2 avoids
    # a near-empty page. Rebuilt/measured per pipeline step 7.
    story = _section_intro_q1()
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_q2())
    return story

SECTIONS = [
    ("Méthodologie, Q1 — Risque & Q2 — Examens complémentaires", _q1_q2_full),
    ("Q3 — Revascularisation et médicaments", _q3_full),
    ("Q4 — Algorithme global & sources", _section_q4_sources),
]

def _make_doc(path=None):
    return SimpleDocTemplate(path or OUT, pagesize=A4,
                              leftMargin=MARGIN, rightMargin=MARGIN,
                              topMargin=32 * mm, bottomMargin=16 * mm,
                              title="Fiche SFAR/SFC 2011 - Coronarien opere en chirurgie "
                                    "non cardiaque",
                              author="Synthèse indépendante (source SFAR/SFC)")

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
    import fitz, tempfile
    tmp_path = tempfile.mktemp(suffix=".pdf")
    doc = _make_doc(tmp_path)
    doc.build(story_flowables, onFirstPage=_silent_page, onLaterPages=_silent_page)
    n = fitz.open(tmp_path).page_count
    os.remove(tmp_path)
    return n

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
