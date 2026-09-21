# -*- coding: utf-8 -*-
"""
Fiche de synthese - "Prise en charge peri-operatoire du patient adulte lors
d'une resection hepatique" - Recommandation de bonne pratique (RBP), HAS,
adoptee par le College le 11 septembre 2025 ; travail mene par la SFAR avec
des experts de la Societe Francaise d'Hepatologie (AFEF) et de
l'Association Chirurgie Hepato-Bilio-Pancreatique et Transplantation
Hepatique (ACHBPT). 54 pages, telecharge depuis sfar.org (wpdmdl=123091).

METHODOLOGIE : methode GRADE (recherche bibliographique 2004-2024, PRISMA,
format PICO). Contrairement au format standard de ce corpus (1+/1-/2+/2-),
ce document n'imprime que "1" (recommandation forte) ou "2" (recommandation
faible) SANS signe +/- - le sens favorable/defavorable reste dans le verbe
de la phrase elle-meme ("il est recommande" vs "il n'est pas recommande"),
jamais invente. Chips locaux G1/G2/AE reutilises tels quels depuis
fiche_optimisation_hemodynamique_adulte_2024.py (meme convention de source
HAS/SFAR, meme absence de signe imprime). Chip ABS ajoute : ce document
distingue explicitement (legende p.2 du source) une "ABS - Pas de
recommandation" (absence d'etudes concluantes, aucune proposition faite)
d'un "AE - Avis d'experts" (proposition malgre l'absence de preuves fortes)
- meme distinction deja rencontree dans ce corpus pour
fiche_optimisation_hemodynamique_pediatrie_2024.py, non fusionnee ici.

DISCLOSURE - decompte du resume ("39 recommandations") vs decompte direct :
la synthese du texte source (section "Synthese des resultats") annonce 39
recommandations pour 14 questions (7 GRADE1 + 21 GRADE2 + 11 avis
d'experts), plus 3 questions sans recommandation (ABS). Un decompte direct,
item par item, des 40 recommandations numerotees (R 1.1.1 a R 3.4.3, chacune
suivie dans le texte de son chip 1/2/AE) trouve : 7 GRADE1 et 11 AE -
correspondant EXACTEMENT au resume - mais 22 GRADE2 (au lieu de 21), soit 40
recommandations au total (au lieu de 39). Les 3 ABS (albumine per-operatoire
§2.4, kétamine/nefopam/lidocaïne IV postoperatoire §2.7, traitements
specifiques de l'IHPH §3.2) correspondent exactement au resume. Chaque
paire (marqueur R x.y.z -> chip suivant) a ete revérifiee individuellement
(pas de chevauchement possible avec un marqueur ABS voisin) : l'ecart est
donc bien un GRADE2 numerote en plus du compte du resume, pas une erreur de
transcription de ce script. Disclosed tel quel, sans arbitrage : les 40
items numerotes sont tous inclus avec le chip reellement imprime a cote
d'eux dans le source.

Egalement disclose : le source numerote DEUX annexes differentes "Annexe 3"
(p.13, statut de l'evaluation du risque d'IHPH chez les patients CHC ; p.18,
antibioprophylaxie recommandee) - doublon de numerotation propre au source,
non corrige ici. L'Annexe 3 p.18 n'est pas reproduite (renvoi a la RFE
SFAR/SPILF "Antibioprophylaxie en chirurgie et medecine interventionnelle"
2024, deja git-trackee dans ce corpus sous la cle `antibioprophylaxie`).

PERIMETRE : integral sur les 3 champs (evaluation/optimisation
preoperatoire ; optimisation peroperatoire ; optimisation postoperatoire),
les 40 recommandations numerotees et les 3 absences de recommandation.
Annexe 1 (elements de prehabilitation multimodale), Annexe 2 (scores
clinico-biologiques MELD/Fib4/APRI/ALBI/FFR), Figure 2 (algorithme
analgesique postoperatoire) et Figure 3 (arbre decisionnel d'admission en
soins critiques) retranscrites depuis un rendu visuel a 180dpi (infographies
sans couche texte exploitable). Annexe 3 p.13 (figure CHC, secondaire) et
Annexe 4 (algorithme d'expansion volemique peroperatoire, deja couvert en
substance par R2.4.2/R2.4.3/R2.4.4) non retranscrites en detail - synthetisees
en une note courte pour ne pas dupliquer R2.4.2. Champs d'application
explicitement exclus par le source lui-meme (section Methode) : pediatrie,
transplantation hepatique, hydatidose et abces hepatiques, indications
chirurgicales, traitement interventionnel non-chirurgical - disclosed, non
traites ici. Argumentaire minimal (regle de projet 2026-09-14) : le texte
source est deja tres concis (format HAS RBP, une recommandation = un
paragraphe court), aucun bloc "Argumentaire" distinct a trimmer.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from style import *
GRADE_COLORS["G1"] = (GREEN, WHITE)
GRADE_COLORS["G2"] = (TEAL, WHITE)
GRADE_COLORS["AE"] = (GREY, WHITE)
GRADE_COLORS["ABS"] = (GREY_LIGHT, INK)
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.units import mm

OUT = "/home/user/rfe-sfar-website/output/Fiche_HAS_SFAR_Resection_Hepatique_Perioperatoire_2025.pdf"

SOURCE_TXT = ("Source : HAS/SFAR/AFEF/ACHBPT, « Prise en charge péri-opératoire du patient "
              "adulte lors d'une résection hépatique », RBP, septembre 2025. Fiche de "
              "synthèse non officielle : se référer au texte intégral.")

def P(txt, style=S_CELL):
    return Paragraph(txt, style)

def chip(label, **kw):
    return grade_chip(label, **kw)

CW_FULL = PAGE_W - 2 * MARGIN

def reco_table(rows, col_widths):
    """rows: (ref, text, grade_label)."""
    data = [[P("Réf.", S_HEAD_W), P("Recommandation", S_HEAD_W), P("Grade", S_HEAD_W_C)]]
    for ref, txt, grade in rows:
        data.append([P(ref, S_CELL_B), P(txt, S_CELL), chip(grade, width=15 * mm)])
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

RCW = [17 * mm, CW_FULL - 17 * mm - 15 * mm, 15 * mm]

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

def bullets(items, style=S_BODY_SM):
    html = "&bull; " + "<br/>&bull; ".join(items)
    return P(html, style)

def absence_note(question_txt):
    return info_panel(P(
        f"<b>ABS — Pas de recommandation</b> (absence d'études concluantes) : {question_txt}",
        S_BODY_SM), bg=GREY_LIGHT, border=GREY)

def legend_flowable():
    chip_w = 14 * mm
    content_w = CW_FULL
    row = Table([[chip("G1", width=chip_w - 2 * mm), chip("G2", width=chip_w - 2 * mm),
                  chip("AE", width=chip_w - 2 * mm), chip("ABS", width=chip_w - 2 * mm),
                  P("<b>G1/G2 = GRADE 1/GRADE 2</b> (le source imprime ces niveaux SANS "
                    "signe +/- ; sens repris du verbe de la phrase). <b>AE</b> = avis "
                    "d'experts (balance bénéfices/risques indéterminée, proposition "
                    "malgré tout). <b>ABS</b> = pas de recommandation (données "
                    "insuffisantes, AUCUNE proposition faite — distinct de AE et d'une "
                    "recommandation négative). Toutes à accord fort (2 tours de vote). "
                    "<b>Écart :</b> résumé « 39 recommandations » (7 G1+21 G2+11 AE) vs "
                    "40 trouvées en décompte direct (7 G1+22 G2+11 AE) — écart d'un "
                    "G2, disclosed en détail p.1 du script source.", S_BADGE_HEAD)]],
                colWidths=[chip_w] * 4 + [content_w - 4 * chip_w])
    row.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                              ("LEFTPADDING", (0, 0), (-1, -1), 1),
                              ("RIGHTPADDING", (0, 0), (-1, -1), 1),
                              ("TOPPADDING", (0, 0), (-1, -1), 0),
                              ("BOTTOMPADDING", (0, 0), (-1, -1), 0)]))
    return row

TOTAL_PAGES = {"n": 8}

def on_page(canvas, doc, page_title):
    header_band(canvas, doc, "HAS / SFAR / AFEF / ACHBPT — RBP, SEPTEMBRE 2025",
                "Prise en charge péri-opératoire — Résection hépatique",
                page_title, icon_fn=lambda c, x, y: icon_liver(c, x, y, 13 * mm), color=TEAL_DARK)
    footer_band(canvas, doc, SOURCE_TXT, f"Page {doc.page} / {TOTAL_PAGES['n']}")

# ---------------------------------------------------------------------------
def _section_intro_champ1():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Résumé :</b> RBP HAS/SFAR/AFEF/ACHBPT (septembre 2025) — prise en charge "
        "péri-opératoire de la résection hépatique de l'adulte (résections mineures, "
        "donneur vivant, tumeurs neuro-endocrines incluses ; pédiatrie, transplantation, "
        "hydatidose/abcès hépatiques, indications chirurgicales et traitement "
        "interventionnel non-chirurgical exclus). 3 champs — évaluation/optimisation "
        "préopératoire, optimisation peropératoire, optimisation postopératoire — 14 "
        "questions, 40 recommandations numérotées (accord fort) et 3 absences de "
        "recommandation.", S_BODY), bg=BG_PANEL, border=TEAL_DARK))
    story.append(Spacer(1, 2.5 * mm))
    story.append(legend_flowable())
    story.append(Spacer(1, 3 * mm))
    story.append(KeepTogether([
        section_bar("Champ 1 — Évaluation et optimisation préopératoire"),
        Spacer(1, 1 * mm),
        P("<b>1.1 Éléments du bilan préopératoire</b> (hors fonction hépatique)", S_CELL_B),
        Spacer(1, 1 * mm),
    ]))
    story.append(reco_table([
        ("R1.1.1", "Chez les patients opérés de résection hépatique (chirurgie à haut "
         "risque), rechercher systématiquement en préopératoire, pour réduire la "
         "morbi-mortalité péri-opératoire : anémie, thrombopénie, anomalie de "
         "l'hémostase (baisse du TP, hypofibrinogénémie) ; insuffisance rénale ; "
         "cholestase (cf R1.3.2) ; dénutrition/risque nutritionnel majeur ; fragilité ; "
         "anomalies de la capacité fonctionnelle (bilan cardiovasculaire adapté au "
         "risque).", "G1"),
    ], RCW))
    story.append(Spacer(1, 2 * mm))
    story.append(P("<b>1.2 Stratégies spécifiques d'optimisation préopératoire</b>", S_CELL_B))
    story.append(Spacer(1, 1 * mm))
    story.append(reco_table([
        ("R1.2.1", "<i>Préhabilitation —</i> réaliser une préhabilitation (cf Annexe 1) "
         "chez les patients à haut risque (dénutrition, âge &gt; 65 ans, fragilité, "
         "ASA &gt; 2), pour réduire la durée de séjour et le taux de complications "
         "péri-opératoires.", "G2"),
        ("R1.2.2", "<i>Nutrition préopératoire —</i> instaurer un support nutritionnel "
         "(oral ou entéral autant que possible) chez les patients présentant une "
         "dénutrition sévère ou un risque nutritionnel majeur, pour diminuer la "
         "morbidité péri-opératoire.", "G2"),
        ("R1.2.3", "Ne pas administrer d'immunonutrition pour diminuer la "
         "morbi-mortalité péri-opératoire.", "G1"),
        ("R1.2.4", "<i>Drainage biliaire préopératoire —</i> chez les patients "
         "présentant un ictère obstructif, discuter au cas par cas un drainage "
         "biliaire préopératoire pour diminuer la morbi-mortalité péri-opératoire.",
         "G2"),
    ], RCW))
    story.append(Spacer(1, 2 * mm))
    story.append(P("<b>1.3 Réduire le risque d'insuffisance hépatique post-hépatectomie "
                    "(IHPH)</b>", S_CELL_B))
    story.append(Spacer(1, 1 * mm))
    story.append(reco_table([
        ("R1.3.1", "Identifier en préopératoire les populations les plus à risque "
         "d'IHPH afin de limiter sa survenue.", "G1"),
        ("R1.3.2", "Utiliser un faisceau de critères ciblés selon le contexte "
         "clinique/ressources disponibles (cf Annexe 2) : chez tous les patients — "
         "scores clinico-biologiques (ALBI, APRI, ALBI+APRI, Fib4), volumétrie "
         "hépatique et/ou biomarqueurs spécifiques ; chez les patients atteints ou "
         "suspects d'hépatopathie chronique — score de Child-Pugh et/ou MELD, "
         "recherche de signes indirects d'hypertension portale, évaluation de "
         "l'hypertension portale (élastométrie ou cathétérisme hépatique si "
         "disponible).", "G2"),
    ], RCW))
    return story

def _section_annexes_12():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Annexe 1 — Éléments d'un programme de préhabilitation multimodale",
                    color=GREY),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(theme_table([
        ("Exercice physique", "Renforcement musculaire ; travail flexibilité/équilibre ; "
         "entraînement supervisé (≥ 3×/semaine) ; exercice aérobie d'intensité modérée "
         "(marche, jogging, cyclisme)."),
        ("Intervention nutritionnelle", "Évaluation/adaptation des apports caloriques ; "
         "optimisation de l'apport protéique (1,5 g/kg/j) ; supplémentation en "
         "protéines de lactosérum (whey) ; apport en vitamines et micronutriments."),
        ("Prise en charge psychologique", "Exercices de réduction d'anxiété et de "
         "respiration ; visualisation mentale ; stimulation cognitive et "
         "concentration."),
        ("Optimisation médicale", "Correction de l'anémie ; contrôle glycémique ; "
         "arrêt du tabac et de l'alcool."),
    ], TCW, head=("Axe", "Éléments")))
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Annexe 2 — Scores clinico-biologiques (risque d'IHPH)", color=GREY),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(theme_table([
        ("MELD", "3,78 × ln(bilirubine [mg/dl]) + 11,2 × ln(INR) + 9,57 × "
         "ln(créatinine [mg/dl]) + 6,43"),
        ("Fib4", "(Âge × ASAT [UI/l]) / (Plaquettes [10<super>9</super>/l] × "
         "√ALAT [UI/l])"),
        ("APRI", "(ASAT × 100) / plaquettes (10<super>9</super>/l) — ASAT exprimé en "
         "multiple de la limite supérieure de la normale"),
        ("ALBI", "(log<sub>10</sub> bilirubine [µmol/l] × 0,66) + (albumine [g/l] × "
         "−0,085)"),
        ("Volume critique du foie futur restant (FFR)", "FFR / VTH (volume total "
         "hépatique) ; FFR / poids corporel"),
    ], TCW, head=("Score", "Formule")))
    return story

# ---------------------------------------------------------------------------
def _section_champ2a():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Champ 2 — Optimisation peropératoire (1/2)"),
        Spacer(1, 1 * mm),
        P("<b>2.1 Choix de l'agent anesthésique</b>", S_CELL_B),
        Spacer(1, 1 * mm),
    ]))
    story.append(reco_table([
        ("R2.1.1", "Ne pas privilégier une modalité d'anesthésie générale (IV vs "
         "inhalée) dans le but de réduire la morbidité postopératoire ou d'améliorer "
         "la survie globale (dont récurrence carcinologique), quelle que soit "
         "l'indication.", "G2"),
    ], RCW))
    story.append(Spacer(1, 2 * mm))
    story.append(P("<b>2.2 Stratégie de préconditionnement hépatique</b>", S_CELL_B))
    story.append(Spacer(1, 1 * mm))
    story.append(reco_table([
        ("R2.2.1", "Administrer en peropératoire un bolus de 8-10 mg de "
         "dexaméthasone, pour réduire la morbidité postopératoire.", "G2"),
        ("R2.2.2", "Ne pas administrer de N-acétylcystéine pour réduire la "
         "morbi-mortalité postopératoire.", "G2"),
        ("R2.2.3", "Ne pas pratiquer de manœuvres de préconditionnement au "
         "sévoflurane ou ischémique (directes ou indirectes) pour réduire la "
         "morbidité postopératoire.", "G2"),
    ], RCW))
    story.append(Spacer(1, 2 * mm))
    story.append(P("<b>2.3 Choix de l'antibioprophylaxie</b>", S_CELL_B))
    story.append(Spacer(1, 1 * mm))
    story.append(reco_table([
        ("R2.3.1", "Administrer une antibioprophylaxie en respectant les molécules "
         "et modalités des recommandations les plus récentes (RFE SFAR/SPILF "
         "« Antibioprophylaxie en chirurgie et médecine interventionnelle », 2024 — "
         "déjà git-trackée dans ce corpus), pour prévenir les infections du site "
         "opératoire.", "AE"),
        ("R2.3.2", "En cas de résection hépatique associée à une chirurgie des voies "
         "biliaires : adapter l'antibioprophylaxie aux antécédents infectieux "
         "biliaires ; utiliser la pipéracilline-tazobactam chez un patient à risque "
         "de colonisation biliaire (drainage percutané/endoprothèse biliaire "
         "récents) sans antécédent de biliculture positive ni de BMR identifiée.",
         "AE"),
    ], RCW))
    story.append(Spacer(1, 2 * mm))
    story.append(P("<b>2.4 Optimisation hémodynamique peropératoire</b>", S_CELL_B))
    story.append(Spacer(1, 1 * mm))
    story.append(reco_table([
        ("R2.4.1", "Utiliser un monitorage du volume d'éjection systolique (VES) "
         "associé aux indices dynamiques, pour optimiser l'expansion volémique et "
         "diminuer la morbidité péri-opératoire.", "G2"),
        ("R2.4.2", "Pour réduire le saignement peropératoire : maintenir une "
         "précharge-dépendance par hypovolémie permissive (VVE élevée et/ou PVC "
         "basse) jusqu'à la fin de la transsection hépatique, sous couvert d'une "
         "pression de perfusion tissulaire adéquate ; restaurer une volémie efficace "
         "une fois la transsection terminée.", "G2"),
        ("R2.4.3", "Ne pas monitorer systématiquement la PVC pour diminuer la "
         "morbi-mortalité péri-opératoire.", "AE"),
        ("R2.4.4", "Ne pas recourir à des traitements (furosémide, nitroglycérine, "
         "milrinone) dans le seul but d'obtenir une PVC basse.", "AE"),
        ("R2.4.5", "Utiliser des solutés cristalloïdes balancés pour l'expansion "
         "volémique peropératoire.", "G2"),
        ("—", "Absence de recommandation concernant l'administration d'albumine "
         "pour l'expansion volémique peropératoire.", "ABS"),
    ], RCW))
    story.append(Spacer(1, 1.8 * mm))
    story.append(P(
        "<b>Annexe 4 (synthèse) :</b> l'algorithme SFAR proposé opérationnalise "
        "R2.4.2 en 2 phases — <i>transsection</i> (hypovolémie permissive : 12 % &lt; "
        "VVE &lt; 20 %, PVC &lt; 5 mmHg si disponible, PAM &gt; 65 mmHg [&gt; 70 mmHg "
        "ou &gt; 90 % de la valeur habituelle si hypertendu] ; surveillance des "
        "signes d'hypoperfusion — lactates &gt; 3 mmol/l, hausse des vasopresseurs, "
        "VVE &gt; 20 % ou baisse du VES) puis <i>post-résection</i> (restauration de "
        "la volémie guidée par le VES : bolus de 250 ml, poursuite si hausse du VES "
        "ou de la VVE ≥ 10 %, arrêt sinon).", S_BODY_SM))
    return story

def _section_champ2b():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Champ 2 — Optimisation peropératoire (2/2)"),
        Spacer(1, 1 * mm),
        P("<b>2.5 Stratégie ventilatoire</b>", S_CELL_B),
        Spacer(1, 1 * mm),
    ]))
    story.append(reco_table([
        ("R2.5.1", "Pour diminuer les complications pulmonaires postopératoires sans "
         "surrisque hémorragique peropératoire, appliquer une ventilation protectrice "
         "associant : volume courant 6-8 ml/kg de poids prédit ; individualisation de "
         "la PEP (≥ 5 cmH<sub>2</sub>O) pour maximiser la compliance pulmonaire ; manœuvres de "
         "recrutement prudentes sous réserve d'une bonne tolérance hémodynamique.",
         "G2"),
    ], RCW))
    story.append(Spacer(1, 2 * mm))
    story.append(P("<b>2.6 Hémostase peropératoire</b>", S_CELL_B))
    story.append(Spacer(1, 1 * mm))
    story.append(reco_table([
        ("R2.6.1", "Ne pas administrer systématiquement d'acide tranexamique de "
         "manière préventive en peropératoire, pour diminuer le saignement et la "
         "transfusion érythrocytaire.", "G2"),
        ("R2.6.2", "En l'absence d'administration préemptive d'acide tranexamique, "
         "administrer précocement 1 g d'acide tranexamique (± 2<super>e</super> dose de 1 g) en cas "
         "de saignement significatif peropératoire.", "AE"),
        ("R2.6.3", "Récupérer le sang épanché en peropératoire (résection "
         "carcinologique incluse) et, après évaluation bénéfice-risque, envisager sa "
         "réinjection pour diminuer la transfusion érythrocytaire péri-opératoire.",
         "G2"),
    ], RCW))
    story.append(Spacer(1, 2 * mm))
    story.append(P("<b>2.7 Stratégie analgésique</b>", S_CELL_B))
    story.append(Spacer(1, 1 * mm))
    story.append(reco_table([
        ("R2.7.1", "Sur foie sain (laparoscopie ou laparotomie), recourir à une "
         "analgésie multimodale associant paracétamol, AINS et opioïdes (sauf "
         "contre-indication), pour diminuer la morbidité postopératoire.", "G1"),
        ("R2.7.2", "En cas de risque ou d'altération manifeste des fonctions "
         "hépatique/rénale, réévaluer l'indication et/ou la posologie des "
         "traitements médicamenteux.", "AE"),
        ("R2.7.3", "Par laparoscopie, compléter l'analgésie systémique par une "
         "infiltration d'anesthésiques locaux ou un bloc locorégional échoguidé.",
         "G2"),
        ("R2.7.4", "Par laparotomie, compléter l'analgésie systémique par une "
         "infiltration d'anesthésiques locaux en continu, un bloc locorégional "
         "échoguidé ou une anesthésie péridurale (sauf contre-indication).", "G2"),
        ("R2.7.5", "Privilégier l'analgésie péridurale (APD) en cas d'hépatectomie "
         "mineure par laparotomie, chez des patients sans cirrhose préopératoire et "
         "avec INR/plaquettes normaux — en dehors de ce cadre, risque accru "
         "d'hématome épidural rendant l'APD plus à risque.", "AE"),
        ("—", "Absence de recommandation, sur foie sain postopératoire, concernant "
         "la kétamine, le néfopam ou la lidocaïne intraveineuse pour diminuer la "
         "douleur postopératoire.", "ABS"),
    ], RCW))
    story.append(Spacer(1, 1.8 * mm))
    story.append(P(
        "<b>Figure 2 (synthèse) :</b> l'algorithme SFAR distingue laparoscopie "
        "(infiltration ± cathéter, ou bloc périphérique ± cathéter) et laparotomie — "
        "hépatectomie mineure sur foie sain ou majeure (infiltration ± cathéter, bloc "
        "périphérique ± cathéter, ou péridurale) vs hépatectomie mineure sur foie "
        "cirrhotique (« pas de recommandation », en pointillés) ; réévaluation "
        "clinicien requise en cas d'altération rénale/hépatique préopératoire.",
        S_BODY_SM))
    return story

# ---------------------------------------------------------------------------
def _section_champ3a():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Champ 3 — Optimisation postopératoire (1/2)"),
        Spacer(1, 1 * mm),
        P("<b>3.1 Critères d'admission en unité de soins critiques</b>", S_CELL_B),
        Spacer(1, 1 * mm),
    ]))
    story.append(reco_table([
        ("R3.1.1", "Ne pas admettre systématiquement les patients en unités de soins "
         "critiques ; individualiser la décision selon les facteurs de risque liés "
         "au patient, à la chirurgie et à l'organisation locale.", "G2"),
        ("R3.1.2", "Décider de l'admission en s'appuyant sur l'arbre décisionnel "
         "proposé (cf Figure 3), comme outil d'aide à la réflexion clinique.", "AE"),
    ], RCW))
    story.append(Spacer(1, 2 * mm))
    story.append(P("<b>3.2 Gestion liée à une insuffisance hépatique</b>", S_CELL_B))
    story.append(Spacer(1, 1 * mm))
    story.append(reco_table([
        ("R3.2.1", "Réaliser une surveillance clinique (ascite, encéphalopathie, "
         "défaillances d'organes) et biologique (bilirubine totale, TP, INR, "
         "facteur V) régulière et rapprochée, pour dépister précocement une "
         "insuffisance hépatique.", "G1"),
        ("R3.2.2", "Chez les patients présentant une IHPH, rechercher "
         "systématiquement une infection et une complication vasculaire (cinétique "
         "des transaminases, scanner injecté et/ou écho-doppler hépatique).", "AE"),
        ("R3.2.3", "Ne pas utiliser la N-acétylcystéine pour prévenir ou traiter une "
         "IHPH.", "G2"),
        ("—", "Absence de recommandation sur l'utilisation de traitements "
         "spécifiques (glucocorticoïdes, terlipressine, somatostatine…) pour "
         "prévenir l'IHPH.", "ABS"),
        ("R3.2.4", "Solliciter un avis auprès d'un centre expert chez tout patient "
         "présentant une IHPH, pour évaluer l'intérêt d'une suppléance ou d'une "
         "transplantation hépatique.", "AE"),
    ], RCW))
    return story

def _section_champ3b_annexe3():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Champ 3 — Optimisation postopératoire (2/2)"),
        Spacer(1, 1 * mm),
        P("<b>3.3 Prévention du risque thromboembolique</b>", S_CELL_B),
        Spacer(1, 1 * mm),
    ]))
    story.append(reco_table([
        ("R3.3.1", "Résection carcinologique sans cirrhose : prescrire une "
         "thromboprophylaxie par HBPM pour une durée de 4 semaines, y compris en "
         "chirurgie mini-invasive ou parcours de réhabilitation améliorée.", "G1"),
        ("R3.3.2", "Résection carcinologique avec cirrhose : prescrire une "
         "thromboprophylaxie par HBPM ; ne pas considérer une thrombopénie modérée "
         "et/ou un TP abaissé comme une contre-indication absolue.", "AE"),
        ("R3.3.3", "Tumeur bénigne ou donneur vivant : prescrire une "
         "thromboprophylaxie par HBPM pour une durée minimale de 7 jours.", "G2"),
        ("R3.3.4", "En cas de très haut risque thromboembolique (résection "
         "carcinologique + facteur(s) de risque patient), associer une compression "
         "pneumatique intermittente per- et postopératoire à la thromboprophylaxie "
         "pharmacologique.", "G2"),
    ], RCW))
    story.append(Spacer(1, 2 * mm))
    story.append(P("<b>3.4 Mesures postopératoires précoces</b>", S_CELL_B))
    story.append(Spacer(1, 1 * mm))
    story.append(reco_table([
        ("R3.4.1", "Instaurer un programme de réhabilitation améliorée après "
         "chirurgie : mobilisation précoce ; réintroduction précoce de la nutrition "
         "orale ; support nutritionnel (entéral en 1<super>re</super> intention) si apports oraux "
         "impossibles/insuffisants (&lt; 50 % des besoins) &gt; 5-7 jours ; contrôle "
         "glycémique (éviter &gt; 180 mg/dl soit 10 mmol/l) ; réévaluation "
         "quotidienne des drainages avec l'équipe chirurgicale.", "G1"),
        ("R3.4.2", "Ne pas appliquer systématiquement une VNI prophylactique ou des "
         "séances de CPAP — y compris chez les patients à haut risque — pour "
         "prévenir les complications respiratoires postopératoires.", "G2"),
        ("R3.4.3", "En cas d'insuffisance respiratoire aiguë postopératoire, "
         "appliquer un support respiratoire non invasif (VNI, CPAP, oxygénothérapie "
         "haut débit) après avoir vérifié l'absence de nécessité de reprise "
         "chirurgicale.", "G2"),
    ], RCW))
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Figure 3 — Arbre décisionnel d'admission en soins critiques (USCr)",
                    color=GREY),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(theme_table([
        ("Étape 1 (préopératoire)", "Risque de décompensation post-opératoire d'une "
         "comorbidité, OU hypertension portale (1 critère suffit : varices "
         "œsophagiennes ; splénomégalie + plaquettes &lt; 150 G/l ; élasticité "
         "≥ 25 kPa) → si oui : USIP."),
        ("Étape 2 (postopératoire)", "Complication avec défaillance(s) d'organe "
         "→ si oui : réanimation."),
        ("Étape 3 (complexité de la résection)", "Bas grade (métastasectomie, "
         "mono-segmentectomie) ou grade intermédiaire (hépatectomie gauche, "
         "segmentectomies antéro-latérales, reconstruction biliaire) → étape "
         "suivante ; grade élevé (hépatectomie droite/centrale étendue ou non, "
         "segmentectomie postérieure complexe dont segment I ; sauf si "
         "cœlioscopie) → USIP directement."),
        ("Étape 4", "Hépatopathie chronique significative, OU pertes sanguines "
         "importantes/polytransfusion, OU ASA &gt; 3 → si oui : USIP/réanimation ; "
         "sinon → SSPI."),
        ("Étape 5 (SSPI)", "Lactatémie &gt; 3 mmol/l → surveillance prolongée en "
         "SSPI (correction volémique/métabolique/transfusion) puis USIP si "
         "persistance &gt; 3 mmol/l, sinon service de chirurgie ; lactatémie "
         "≤ 3 mmol/l d'emblée → service de chirurgie."),
    ], TCW, head=("Étape", "Critères / orientation")))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "USCr = unités de soins critiques (USIP = unité de soins intensifs "
        "polyvalents, ou réanimation). Scores utilisables pour l'hépatopathie "
        "chronique : Child-Pugh B, MELD &gt; 9, liver stiffness &gt; 8 kPa (si "
        "cirrhose/carcinome hépatocellulaire), score ABRI (isolé ou associé à "
        "l'APRI).", S_NOTE))
    return story

# ---------------------------------------------------------------------------
def _section_sources():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("Méthode, sources et avertissement", color=GREY))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>Champ d'application :</b> résections hépatiques (résections mineures, "
        "donneur vivant, tumeurs neuro-endocrines incluses). <b>Explicitement exclus "
        "par le texte source :</b> pédiatrie, transplantation hépatique, hydatidose "
        "et abcès hépatiques, indications chirurgicales, traitement interventionnel "
        "non-chirurgical.", S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>Méthode :</b> groupe d'experts SFAR, avec experts AFEF (Société "
        "Française d'Hépatologie) et ACHBPT intégrés pour les questions requérant "
        "leur expertise. Recherche bibliographique 2004-2024 (méthodologie PRISMA), "
        "questions formulées en format PICO. Méthode GRADE : niveau de preuve élevé "
        "→ recommandation forte (1) ; niveau de preuve faible → recommandation "
        "faible (2) ; balance bénéfices/risques indéterminée → avis d'experts (AE) ; "
        "absence d'études/résultats concluants → pas de recommandation (ABS). "
        "2 tours de vote, accord fort pour les 40 recommandations retenues.",
        S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>Document source :</b> HAS, « Prise en charge péri-opératoire du patient "
        "adulte lors d'une résection hépatique », recommandation de bonne pratique, "
        "adoptée par le Collège de la HAS le 11 septembre 2025. Élaborée par la "
        "SFAR avec l'AFEF et l'ACHBPT.", S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>URL source :</b> https://sfar.org/prise-en-charge-peri-operatoire-du-"
        "patient-adulte-lors-dune-resection-hepatique/", S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>Couverture :</b> intégralité des 40 recommandations numérotées et des 3 "
        "absences de recommandation (3 champs, 14 questions), de l'Annexe 1 "
        "(préhabilitation), de l'Annexe 2 (scores), et d'une synthèse de l'Annexe 4 "
        "et des Figures 2 et 3 (algorithmes/arbre décisionnel, retranscrits depuis un "
        "rendu visuel à 180dpi, sans couche texte exploitable). L'Annexe 3 relative à "
        "l'antibioprophylaxie (p.18 du source — doublonnant le numéro d'une autre "
        "Annexe 3 p.13, non résolu) renvoie à la RFE SFAR/SPILF 2024 déjà "
        "git-trackée sous la clé antibioprophylaxie. Bibliographie et composition "
        "nominative des groupes de travail non reproduites — non actionnables "
        "cliniquement.", S_SOURCE))
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Avertissement :</b> cette fiche est une synthèse indépendante, produite "
        "pour un usage d'aide-mémoire. Elle reprend intégralement les 40 "
        "recommandations et les 3 absences de recommandation du texte source (dont "
        "le léger écart de décompte avec le résumé de la synthèse, disclosed "
        "ci-dessus), mais condense l'argumentaire de chaque item. Elle ne remplace "
        "pas le texte intégral et n'est ni éditée ni validée par la HAS ni la SFAR.",
        S_BODY_SM), bg=GREY_LIGHT, border=GREY))
    return story

# ---------------------------------------------------------------------------
SECTIONS = [
    ("Champ 1 — Évaluation et optimisation préopératoire", _section_intro_champ1),
    ("Annexes 1-2 — Préhabilitation et scores clinico-biologiques", _section_annexes_12),
    ("Champ 2 — Optimisation peropératoire (1/2)", _section_champ2a),
    ("Champ 2 — Optimisation peropératoire (2/2)", _section_champ2b),
    ("Champ 3 — Optimisation postopératoire (1/2)", _section_champ3a),
    ("Champ 3 — Optimisation postopératoire (2/2) & Figure 3", _section_champ3b_annexe3),
    ("Méthode, sources et avertissement", _section_sources),
]

def _make_doc(path=None):
    return SimpleDocTemplate(path or OUT, pagesize=A4,
                              leftMargin=MARGIN, rightMargin=MARGIN,
                              topMargin=32 * mm, bottomMargin=16 * mm,
                              title="Fiche HAS/SFAR 2025 - Resection hepatique perioperatoire",
                              author="Synthèse indépendante (source HAS/SFAR)")

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
