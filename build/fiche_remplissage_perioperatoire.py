# -*- coding: utf-8 -*-
"""
Fiche de synthese - Societe Francaise d'Anesthesie et de Reanimation (SFAR),
en collaboration avec l'Adarpef. "Strategie du remplissage vasculaire
perioperatoire" - Recommandations Formalisees d'Experts (RFE), validees par
le conseil d'administration de la Sfar du 19 octobre 2012. Auteurs :
B. Vallet, Y. Blanloeil, B. Cholley, G. Orliaguet, S. Pierre, B. Tavernier.
Ann Fr Anesth Reanim 32 (2013) 454-462. 9 pages, telecharge depuis sfar.org
(wp-content/uploads/2015/09/2a_AFAR_FRANCAIS_Strategie-du-remplissage-
vasculaire-perioperatoire.pdf).

METHODOLOGIE : methode GRADE standard, deja largement utilisee dans ce
corpus (PAS une nouvelle convention) - qualite des preuves en 4 categories
(Haute/Moderee/Basse/Tres basse), force de recommandation binaire Forte
(GRADE 1+/1-) ou Faible (GRADE 2+/2-), determinee par vote Delphi selon 4
facteurs (estimation de l'effet, niveau global de preuve, balance effets
desirables/indesirables, valeurs/preferences, couts). En l'absence
d'evaluation quantifiee, avis d'experts (meme formulation, chip "AE").
15 recommandations : 9 sur GRADE explicite (1+/1-/2+), 6 sur avis d'experts.

COUVERTURE : integrale sur les 15 recommandations elles-memes (texte +
grade), le preambule (3.1 problematique - physiologie du remplissage
vasculaire, limites des indices hemodynamiques classiques PA/FC/diurese/PVC,
les deux approches modernes [titration sur VES ; indices dynamiques
VPP/VVE/PVI], monitorage de l'oxygenation tissulaire ; 3.1.2 rationnel de la
RFE ; 3.2 methodologie GRADE detaillee), la Figure 1 (algorithme de
titration retranscrit depuis un rendu visuel), la declaration d'interets et
la bibliographie complete (27 references).

ARGUMENTAIRE : volontairement condense (regle de projet 2026-09-14 - eviter
le remplissage de pages par une prose de rationale qui duplique le texte
source) aux seuls elements qui changent reellement la pratique au chevet du
patient - un seuil, une dose, une contre-indication non deja present dans la
ligne de recommandation elle-meme (ex. R5/R7 : doses d'ephedrine/
phenylephrine ; R11 : choix de l'HEA 130/0,4 specifiquement ; R15 : regle
4-2-1 detaillee). Les paragraphes de justification purement evidentielle
(statistiques d'etudes, IC95, mecanismes physiopathologiques deja resumes
dans le preambule) sont omis plutot que condenses en phrases denses -
se referer au texte integral pour le detail des etudes. Ceci est un choix de
scope assume, pas un oubli.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from style import *
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.units import mm

OUT = "/home/user/rfe-sfar-website/output/Fiche_SFAR_Remplissage_Vasculaire_Perioperatoire_2013.pdf"

SOURCE_TXT = ("Source : « Stratégie du remplissage vasculaire périopératoire » — RFE "
              "SFAR/Adarpef, Ann Fr Anesth Réanim 32 (2013) 454-462. Fiche de synthèse "
              "non officielle : se référer au texte intégral.")

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

TCW = [46 * mm, CW_FULL - 46 * mm]

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
        ("TOPPADDING", (0, 0), (-1, -1), 3.4), ("BOTTOMPADDING", (0, 0), (-1, -1), 3.4),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            style_cmds.append(("BACKGROUND", (0, i), (-1, i), BG_PANEL))
    t.setStyle(TableStyle(style_cmds))
    return t

RCW = [CW_FULL - 20 * mm, 20 * mm]

def bullets(items, style=S_BODY_SM):
    html = "&bull; " + "<br/>&bull; ".join(items)
    return P(html, style)

def legend_flowable():
    chip_w = 15 * mm
    content_w = CW_FULL
    row = Table([[chip("1+", width=chip_w - 2 * mm), chip("1-", width=chip_w - 2 * mm),
                  chip("2+", width=chip_w - 2 * mm), chip("2-", width=chip_w - 2 * mm),
                  chip("AE", width=chip_w - 2 * mm),
                  P("<b>GRADE</b> — 1+/1- : recommandation <b>forte</b> (« il faut faire "
                    "/ ne pas faire ») ; 2+/2- : recommandation <b>faible</b> (« il est "
                    "possible de faire / ne pas faire ») ; <b>AE</b> : avis d'experts "
                    "(absence d'évaluation quantifiée de l'effet).", S_BADGE_HEAD)]],
                colWidths=[chip_w, chip_w, chip_w, chip_w, chip_w, content_w - 5 * chip_w])
    row.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                              ("LEFTPADDING", (0, 0), (-1, -1), 1),
                              ("RIGHTPADDING", (0, 0), (-1, -1), 1),
                              ("TOPPADDING", (0, 0), (-1, -1), 0),
                              ("BOTTOMPADDING", (0, 0), (-1, -1), 0)]))
    return row

TOTAL_PAGES = {"n": 7}

def on_page(canvas, doc, page_title):
    header_band(canvas, doc, "SFAR / ADARPEF — RFE, 19 OCTOBRE 2012",
                "Stratégie du remplissage vasculaire périopératoire",
                page_title, icon_fn=lambda c, x, y: icon_drop(c, x, y, 13 * mm), color=TEAL_DARK)
    footer_band(canvas, doc, SOURCE_TXT, f"Page {doc.page} / {TOTAL_PAGES['n']}")

# ---------------------------------------------------------------------------
def _section_intro():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Résumé :</b> objectif — faire le point sur les pratiques de remplissage "
        "vasculaire (RV) périopératoire ayant démontré un bénéfice, pour les utiliser en "
        "pratique quotidienne. Chez les patients chirurgicaux « à haut risque », il est "
        "recommandé de titrer le RV peropératoire en se guidant sur une mesure du "
        "volume d'éjection systolique (VES), pour réduire la morbidité postopératoire, "
        "la durée de séjour et le délai de reprise alimentaire en chirurgie digestive — "
        "avec réévaluation régulière du VES, en particulier lors des séquences "
        "d'instabilité hémodynamique. En chirurgie « mineure », il est probablement "
        "recommandé d'administrer 15 mL/kg (gestes courts) à 20-30 mL/kg (gestes de "
        "1-2 h) de cristalloïdes. Chez l'enfant et le nouveau-né sans comorbidité, "
        "règle des « 4-2-1 » avec solution saline isotonique glucosée à 1 % (enfant/"
        "nourrisson) ou 10 % (nouveau-né) ; au-delà de 10 ans et/ou 30-40 kg, les "
        "recommandations adultes s'appliquent.", S_BODY), bg=BG_PANEL, border=TEAL))
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("Méthodologie — grille GRADE"))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "Méthode GRADE : qualité des preuves en 4 catégories — <b>1. Haute</b> "
        "(recherches futures ne changeront très probablement pas la confiance dans "
        "l'estimation de l'effet) ; <b>2. Modérée</b> (changeront probablement la "
        "confiance, pourraient modifier l'estimation) ; <b>3. Basse</b> (impact très "
        "probable sur la confiance et l'estimation) ; <b>4. Très basse</b> (estimation "
        "très incertaine). Force de recommandation toujours binaire — forte (GRADE 1+ "
        "ou 1−, « il faut faire / ne pas faire ») ou faible (GRADE 2+ ou 2−, « il est "
        "possible de faire / ne pas faire ») — déterminée par vote Delphi des experts "
        "selon 4 facteurs : estimation de l'effet ; niveau global de preuve ; balance "
        "effets désirables/indésirables ; valeurs et préférences (patient, médecin, "
        "décisionnaire) ; coûts/ressources. En l'absence d'évaluation quantifiée, avis "
        "d'experts (même formulation).", S_BODY_SM))
    story.append(Spacer(1, 1.5 * mm))
    story.append(legend_flowable())
    return story

def _section_preambule():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Préambule — problématique et rationnel"),
        Spacer(1, 1.5 * mm),
        P("Le remplissage vasculaire (RV) augmente le volume « contraint » et la "
          "pression systémique moyenne tout en réduisant la résistance au retour "
          "veineux, augmentant ainsi le retour veineux et le débit cardiaque — à "
          "condition que les ventricules soient « précharge-dépendants ». Le débit "
          "cardiaque est pourtant rarement monitoré en pratique courante (difficultés "
          "techniques historiques).", S_BODY),
    ]))
    story.append(Spacer(1, 1.8 * mm))
    story.append(P(
        "<b>Limites des indices classiques :</b> en l'absence de mesure du débit "
        "cardiaque, le RV est classiquement guidé sur PA, FC, diurèse, PVC — indices "
        "aux limites bien établies. Les variations de PA sont multifactorielles et ne "
        "reflètent pas le débit cardiaque (une PA « normale » peut coexister avec une "
        "perfusion tissulaire inadéquate). La FC peut augmenter sans baisse de "
        "précharge (réveil, douleur) ou ne pas augmenter malgré une baisse de "
        "précharge (bêta-bloquants, réflexe de Bezold-Jarisch). La diurèse basse "
        "n'est pas toujours associée à une hypoperfusion rénale (hormones de stress, "
        "morphiniques). La PVC (indice « statique ») est notoirement insuffisante pour "
        "prédire la précharge-dépendance, chez l'adulte comme chez l'enfant. Ces "
        "approches empiriques (« schémas stéréotypés », a priori sur le type de "
        "chirurgie) exposent au risque d'« hypovolémie occulte » et de décisions "
        "inadaptées.", S_BODY_SM))
    story.append(Spacer(1, 1.8 * mm))
    story.append(P(
        "<b>Deux approches modernes :</b> (1) titration sur le <b>VES</b> — maximaliser "
        "le VES pour limiter l'hypoperfusion ; l'absence d'augmentation du VES en "
        "réponse à un remplissage signe l'atteinte du plateau de la courbe de fonction "
        "cardiovasculaire (arrêt du RV). Une dizaine d'études contrôlées ont évalué "
        "cette stratégie (Doppler œsophagien, bolus de colloïde ~250 mL) avec "
        "réduction des complications postopératoires, accélération de la reprise du "
        "transit digestif et réduction des durées d'hospitalisation. (2) <b>Indices "
        "dynamiques</b> de précharge-dépendance (variations respiratoires du VES chez "
        "le patient ventilé) — variation de pression pulsée (VPP) ou du VES (VVE) : "
        "une VPP/VVE > 12-13 % prédit l'augmentation du débit cardiaque en réponse au "
        "RV ; < 9 % indique presque certainement l'absence de précharge-dépendance "
        "(zone grise 9-13 % : combiner à un test de remplissage). Conditions de "
        "validité : rythme cardiaque régulier, ventilation contrôlée à volume courant "
        "≥ 7 mL/kg, thorax fermé, monitorage invasif de la PA. Le Pleth Variability "
        "Index (PVI, non invasif, photopléthysmographie) pourrait permettre une "
        "généralisation en chirurgie mineure/moyenne. Chaque moniteur/algorithme doit "
        "être validé individuellement — les résultats d'un constructeur ne sont pas "
        "transposables à un autre.", S_BODY_SM))
    story.append(Spacer(1, 1.8 * mm))
    story.append(P(
        "Le monitorage hémodynamique n'a d'intérêt que s'il est associé à des "
        "décisions thérapeutiques (« optimisation hémodynamique » = « goal-directed "
        "hemodynamic therapy »), par opposition à un RV prédéterminé par type de "
        "chirurgie. Seules des stratégies rapides, opérateur-indépendantes, peu/non "
        "invasives et peu coûteuses pourront être généralisées. L'hémodynamique "
        "systémique et l'oxygénation tissulaire (SvO2 par cathéter artériel "
        "pulmonaire, ScvO2 par cathéter central) sont complémentaires, non opposées — "
        "mais aucune étude n'a confronté ces deux approches entre elles ; l'ajout "
        "d'inotropes/vasopresseurs pourrait justifier une évaluation de l'adéquation "
        "des apports en oxygène (lactate, SvO2, ScvO2), au cas par cas.", S_BODY_SM))
    story.append(Spacer(1, 1.8 * mm))
    story.append(P(
        "<b>Rationnel :</b> les référentiels existants (SRLF-Sfar, juin 1996) sont "
        "anciens ; de nouvelles données de littérature, de nouvelles techniques de "
        "monitorage, et l'opposition apparente des concepts de remplissage « restrictif "
        "» / « libéral » justifient cette actualisation. La mise en œuvre parallèle "
        "d'un programme d'Évaluation des pratiques professionnelles (EPP) est prévue, "
        "conformément à la politique conjointe Sfar/Cfar pour le développement "
        "professionnel continu (DPC).", S_BODY_SM))
    return story

def _section_intro_preambule():
    story = _section_intro()
    story.append(Spacer(1, 2 * mm))
    story.extend(_section_preambule())
    return story

# ---------------------------------------------------------------------------
# Figure 1 (source page 5/458) - titration algorithm, no reliable text layer
# for the diagram itself - rendered at 220dpi and transcribed as a looped
# decision table, branching/looping logic traced arrow-by-arrow.
FIGURE1_ROWS = [
    ("1er bolus (200 ± 50 mL en 10 min)",
     "→ mesure de la variation du VES"),
    ("Augmentation du VES < 10 %",
     "→ Arrêt du remplissage (puis surveillance)"),
    ("Augmentation du VES > 10 %",
     "→ Nouveau bolus (200 ± 50 mL en 10 min), puis remesure du VES (boucle)"),
    ("Après arrêt du remplissage — baisse du VES > 10 %",
     "→ Nouveau bolus (200 ± 50 mL en 10 min) — reprise du cycle de titration"),
]

def _section_reco_ves():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Recommandations 1 à 3 — Titration du remplissage sur le VES"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("<b>R1</b> — Chez les patients chirurgicaux « à haut risque », il est "
         "recommandé de titrer le remplissage vasculaire peropératoire en se guidant "
         "sur une mesure du VES, pour réduire la morbidité postopératoire, la durée de "
         "séjour hospitalier et le délai de reprise d'une alimentation orale des "
         "patients de chirurgie digestive.", "1+"),
        ("<b>R2</b> — Il est recommandé d'interrompre le remplissage en l'absence "
         "d'augmentation du VES.", "1+"),
        ("<b>R3</b> — Il est recommandé de réévaluer régulièrement le VES et son "
         "augmentation (ou non) en réponse à une épreuve de remplissage, en particulier "
         "lors des séquences d'instabilité hémodynamique.", "1+"),
    ], RCW))
    story.append(Spacer(1, 1.8 * mm))
    story.append(P(
        "<b>Précisions :</b> bolus de colloïde (HEA ou gélatine fluide modifiée, "
        "100-250 mL) le plus souvent dès le début de l'intervention ; bolus "
        "pédiatrique 10-20 mL/kg. En hémorragie active/menaçante, poursuivre le "
        "remplissage indépendamment du VES, ou refaire le test à distance de "
        "l'induction. Si monitorage de l'oxygénation tissulaire utilisé : cibles "
        "ScvO2 > 73 %, lactate < 2 mmol/L.", S_BODY_SM))
    story.append(Spacer(1, 1.8 * mm))
    story.append(P("<b>Figure 1 — Titration du remplissage guidée par le monitorage "
                    "de la variation du VES</b> (reproduit en tableau depuis un rendu "
                    "visuel, source page 458)", S_CELL_B))
    story.append(Spacer(1, 1 * mm))
    story.append(theme_table(FIGURE1_ROWS, TCW, head=("Situation", "Conduite")))
    return story

def _section_intro_preambule_ves():
    story = _section_intro_preambule()
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_reco_ves())
    return story

# ---------------------------------------------------------------------------
def _section_reco_obstetrique():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Recommandations 4 à 8 — Chirurgie mineure & obstétrique"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("<b>R4</b> — Au cours de la chirurgie « mineure » (durée < 2 h, y compris "
         "ambulatoire), pour diminuer l'incidence des nausées/vomissements et le "
         "recours aux antiémétiques, il est probablement recommandé d'administrer de "
         "15 à 30 mL/kg de cristalloïdes.", "2+"),
        ("<b>R5</b> — Il n'est pas recommandé d'utiliser un remplissage vasculaire "
         "systématique au cours du travail pour limiter le risque d'hypotension lors "
         "de l'installation d'une analgésie péridurale.", "1-"),
        ("<b>R6</b> — Il n'est pas recommandé d'effectuer un préremplissage par des "
         "cristalloïdes pour une rachianesthésie pour césarienne.", "1-"),
        ("<b>R7</b> — Afin d'éviter/limiter les risques maternels et fœtaux liés à "
         "l'hypotension après rachianesthésie, il est recommandé d'associer un "
         "coremplissage par cristalloïdes avec des vasoconstricteurs (phényléphrine, "
         "éventuellement associée à l'éphédrine).", "1+"),
        ("<b>R8</b> — Il n'est pas recommandé d'utiliser un colloïde (HEA) chez une "
         "patiente prééclamptique en dehors d'un état de choc hypovolémique/"
         "hémorragique.", "AE"),
    ], RCW))
    story.append(Spacer(1, 1.8 * mm))
    story.append(P(
        "<i>Disclosure :</i> le résumé de la source module la posologie R4 selon la "
        "durée du geste (15 mL/kg gestes courts, 20-30 mL/kg gestes de 1-2 h), alors "
        "que le texte de la recommandation R4 elle-même donne un intervalle unique "
        "« 15 à 30 mL/kg » sans distinction de durée — les deux formulations sont "
        "reproduites fidèlement chacune à sa place ; divergence interne à la source, "
        "non résolue ici.", S_NOTE))
    story.append(Spacer(1, 1.2 * mm))
    story.append(P(
        "<b>R5 :</b> le remplissage n'est pas efficace pour prévenir/traiter cette "
        "hypotension — traitement de base : faibles doses d'éphédrine (< 15-20 mg) "
        "+ décubitus latéral gauche.", S_BODY_SM))
    story.append(Spacer(1, 1.2 * mm))
    story.append(P(
        "<b>R7 :</b> coremplissage 1-2 L de cristalloïdes dès l'injection "
        "intrathécale. Vasoconstricteur privilégié : phényléphrine (perfusion IV "
        "continue 50 µg/min, max 100 µg/min, et/ou bolus IVD 50-150 µg ; bradycardie "
        "réflexe sévère → éphédrine ≤ 15 mg) — plus rapidement efficace et moins "
        "d'acidémie fœtale que l'éphédrine seule à forte dose. HEA en préremplissage "
        "efficace mais hors AMM dans cette indication en France.", S_BODY_SM))
    return story

def _section_intro_preambule_ves_obst():
    story = _section_intro_preambule_ves()
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_reco_obstetrique())
    return story

# ---------------------------------------------------------------------------
def _section_reco_speciales():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Recommandations 9 à 15 — Situations particulières"),
        Spacer(1, 1.5 * mm),
        reco_table([
        ("<b>R9</b> — Il n'est pas recommandé d'exclure les colloïdes chez un patient "
         "allergique à une substance autre que le colloïde lui-même.", "AE"),
        ("<b>R10</b> — Chez un opéré ayant présenté une anaphylaxie documentée ou "
         "suspectée à un colloïde (gélatine fluide modifiée ou HEA), il est recommandé "
         "d'utiliser, si nécessaire, un colloïde de l'autre classe.", "AE"),
        ("<b>R11</b> — En présence d'une altération de la fonction rénale (notamment "
         "d'origine septique), il est probablement recommandé d'éviter les HEA.",
         "2+"),
        ("<b>R12</b> — Il est probablement recommandé d'utiliser les cristalloïdes "
         "pour le remplissage vasculaire des donneurs de reins en état de mort "
         "encéphalique.", "AE"),
        ("<b>R13</b> — Il est recommandé de respecter les posologies maximales des "
         "HEA (33 mL/kg/24 h le 1er jour, 20 mL/kg/24 h les 2 jours suivants) et de "
         "ne pas les utiliser chez les patients ayant des troubles de l'hémostase.",
         "1+"),
        ("<b>R14</b> — Chez le patient cérébrolésé, il est recommandé de ne pas "
         "utiliser de solutés hypotoniques.", "AE"),
        ("<b>R15</b> — Chez l'enfant et le nouveau-né sans comorbidité, il est "
         "recommandé d'assurer un apport de base hydroélectrolytique et glucidique "
         "selon la règle des « 4-2-1 », avec solution saline isotonique glucosée à "
         "1 % (enfant/nourrisson) ou 10 % (nouveau-né).", "AE"),
    ], RCW),
    ]))
    story.append(Spacer(1, 1.8 * mm))
    story.append(P(
        "<b>R11 :</b> chez l'opéré à fonction rénale normale, limiter à 33 mL/kg et "
        "n'utiliser que l'HEA 130/0,4 (éviter les HEA de haut poids moléculaire/haut "
        "degré de substitution/hyperoncotiques).", S_BODY_SM))
    story.append(Spacer(1, 1.2 * mm))
    story.append(P(
        "<b>R15 (pédiatrie) :</b> débit selon la règle 4-2-1 (4 mL/kg/h pour les 10 "
        "premiers kg + 2 mL/kg/h pour les 10 kg suivants + 1 mL/kg/h au-delà, soit "
        "65 mL/h pour 25 kg), plus compensation du jeûne préopératoire (corrigée à "
        "50 % la 1<sup>re</sup> heure, 50 % sur les 2 heures suivantes). Surveillance "
        "de la natrémie/glycémie si jeûne prolongé (glycémie systématique chez le "
        "nouveau-né). Arrêt des perfusions inutiles après chirurgie mineure. "
        "Dispositif de contrôle du débit recommandé (pompe/seringue électrique, ou à "
        "défaut métrisette) — les régulateurs par réduction de calibre (type "
        "Dial-a-Flow™) sont à éviter (non fiables chez le petit enfant). Choix du "
        "soluté non documenté chez le nouveau-né. Le monitorage invasif d'indices "
        "statiques (PVC, PAPO) ne prédit pas la réponse au RV chez l'enfant/"
        "nourrisson ; seule la variabilité du pic de vélocité aortique (échographie "
        "transthoracique) le permet — les autres indices de variabilité du VES (VPP, "
        "PVI) n'ont pas montré d'intérêt à ce jour. Au-delà de 10 ans et/ou 30-40 kg, "
        "les recommandations adultes s'appliquent.", S_BODY_SM))
    return story

def _section_sources():
    story = []
    story.append(section_bar("Déclaration d'intérêts, sources et traçabilité",
                              color=GREY))
    story.append(Spacer(1, 2 * mm))
    story.append(P("<b>Déclaration d'intérêts :</b> les auteurs n'ont pas transmis de "
                    "déclaration de conflits d'intérêts.", S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>Document source :</b> « Stratégie du remplissage vasculaire "
        "périopératoire » — Recommandations Formalisées d'Experts (RFE), SFAR, "
        "rédigées en collaboration avec l'Adarpef, validées par le conseil "
        "d'administration de la Sfar du 19 octobre 2012. Auteurs : B. Vallet, "
        "Y. Blanloeil, B. Cholley, G. Orliaguet, S. Pierre, B. Tavernier. Comité "
        "d'organisation : les 6 auteurs. Groupes de travail thématiques (monitorage, "
        "chirurgie mineure, chirurgie majeure, contextes particuliers, pédiatrie) : "
        "O. Collange, O. Desebbe, J. Duranteau, I. Philip ; K. Asehnoune, M. Biais ; "
        "J.-L. Fellahi, D. Longrois, G. Lebuffe, E. Futier ; P. Dewachter, A. Godier, "
        "O. Joannes-Boyau, F.J. Mercier, A. Mignon, Y. Ozier, L. Velly ; S. Dahmani, "
        "C. Lejus, E. Wodey. Chargés de bibliographie : A. Bouglé, G. Dubar, "
        "T. Kortchinsky.", S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P("<b>Version :</b> Ann Fr Anesth Réanim 32 (2013) 454-462.",
                    S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P("<b>Méthodologie :</b> GRADE (qualité des preuves 1-4, force "
                    "1+/1-/2+/2-, avis d'experts) — voir détail en page 1.", S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>URL source :</b> https://sfar.org/wp-content/uploads/2015/09/"
        "2a_AFAR_FRANCAIS_Strategie-du-remplissage-vasculaire-perioperatoire.pdf",
        S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P("<b>Couverture :</b> intégralité du résumé, préambule "
                    "(physiopathologie, rationnel, méthodologie), des 15 "
                    "recommandations, de la Figure 1 (algorithme de titration) et de "
                    "la déclaration d'intérêts. L'argumentaire de chaque "
                    "recommandation est volontairement condensé aux seuls éléments "
                    "changeant la pratique (dose, seuil, contre-indication) — se "
                    "référer au texte intégral pour le détail des études sources.",
                    S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>Bibliographie (27 références) :</b> 1. Guyton AC, Physiol Rev "
        "1955;35:123-9. 2. Sinclair S et al., BMJ 1997;315:909-12. 3. Venn R et al., "
        "Br J Anaesth 2002;88:65-71. 4. Brandstrup B et al., Ann Surg 2003;238:641-8. "
        "5. Nisanevich V et al., Anesthesiology 2005;103:25-32. 6. Teboul JL, Groupe "
        "d'experts SRLF, Ann Fr Anesth Reanim 2005;24:568-76. 7. Tibby SM, Murdoch "
        "IA, Arch Dis Child 2003;88:46-52. 8. Phan TD et al., J Am Coll Surg "
        "2008;207:935-41. 9. Cannesson M et al., Anesthesiology 2011;115:231-41. "
        "10. Cannesson M et al., Br J Anaesth 2008;101:200-6. 11. Zimmermann M et "
        "al., Eur J Anaesthesiol 2010;27:555-61. 12. Hamilton MA et al., Anesth Analg "
        "2011;112:1392-402. 13. Atkins D et al., BMJ 2004;328:1490. 14. Copeland GP "
        "et al., Br J Surg 1991;78:355-60. 15. Rioux JP et al., Crit Care Med "
        "2009;37:1293-8. 16. Winkelmayer WC et al., Kidney Int 2003;64:1046-9. "
        "17. Mahmood A et al., Br J Surg 2007;94:427-33. 18. Mukhtar A et al., Anesth "
        "Analg 2009;109:924-30. 19. Godet G et al., Eur J Anaesthesiol "
        "2008;25:986-94. 20. Fenger-Eriksen C et al., Acta Anaesthesiol Scand "
        "2005;49:969-74. 21. Wu Y et al., Chin Med J 2010;123:3079-83. 22. Dart AB et "
        "al., Cochrane Database Syst Rev 2010;20:CD007594. 23. Hartog CS et al., "
        "Anesth Analg 2011;112:635-45. 24. Groeneveld AB et al., Ann Surg "
        "2011;253:470-83. 25. Kozek-Langenecker SA et al., Anesth Analg "
        "2008;107:382-90. 26. Sümpelmann R et al., Eur J Anaesthesiol 2011;28:637-9. "
        "27. Furman EB et al., Anesthesiology 1975;42:187-93.", S_SOURCE))
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Avertissement — document de 2013 :</b> ce document est une fiche de "
        "synthèse indépendante, produite pour un usage d'aide-mémoire. Elle reprend "
        "l'intégralité des recommandations du texte source (dont la Figure 1, "
        "transcrite depuis un rendu visuel du PDF faute de couche texte fiable pour le "
        "diagramme), mais ne remplace pas le texte intégral et n'est ni éditée ni "
        "validée par la SFAR. Les seuils de posologie des HEA, les pratiques "
        "obstétricales et les stratégies de monitorage hémodynamique ayant pu évoluer "
        "depuis 2013 (dont des restrictions réglementaires ultérieures sur les HEA "
        "dans plusieurs pays européens), se référer à un avis spécialisé et aux "
        "recommandations actualisées avant toute décision thérapeutique.",
        S_BODY_SM), bg=GREY_LIGHT, border=GREY))
    return story

def _section_speciales_sources():
    story = _section_reco_speciales()
    story.append(Spacer(1, 4 * mm))
    story.extend(_section_sources())
    return story

def _section_all():
    story = _section_intro_preambule_ves_obst()
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_speciales_sources())
    return story

SECTIONS = [
    ("Méthodologie, résumé, préambule, Recommandations 1 à 15 (Figure 1) & sources",
     _section_all),
]

def _make_doc(path=None):
    return SimpleDocTemplate(path or OUT, pagesize=A4,
                              leftMargin=MARGIN, rightMargin=MARGIN,
                              topMargin=32 * mm, bottomMargin=16 * mm,
                              title="Fiche SFAR 2013 - Strategie du remplissage "
                                    "vasculaire perioperatoire",
                              author="Synthèse indépendante (source SFAR/Adarpef)")

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
    # NOTE: pypdf/cryptography is broken in this container (pyo3 panic on
    # import) - use PyMuPDF (fitz) instead, per fiche_ponction_lombaire.py.
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
