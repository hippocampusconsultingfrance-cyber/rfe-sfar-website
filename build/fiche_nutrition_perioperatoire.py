# -*- coding: utf-8 -*-
"""
Fiche de synthese - Societe Francaise d'Anesthesie et de Reanimation (SFAR) &
Societe francophone de nutrition clinique et metabolisme (SFNEP). "Recomman-
dations de bonnes pratiques cliniques sur la nutrition perioperatoire.
Actualisation 2010 de la conference de consensus de 1994 sur la nutrition
artificielle perioperatoire en chirurgie programmee de l'adulte." Coordonna-
teurs : C. Chambrier, F. Sztark. Ann Fr Anesth Reanim 30 (2011) 381-389
(doi:10.1016/j.annfar.2011.01.014). 9 pages, telecharge depuis sfar.org
(wp-content/uploads/2015/10/2_AFAR_Nutrition-artificielle-perioperatoire-en
-chirurgie-programmee-de-ladulte.pdf).

COLLISION VERIFIEE (regle de projet) : ne pas confondre avec la fiche deja
construite "nutrition" (= "Nutrition artificielle en reanimation", SFAR/
SRLF/SFNEP RFE 2014, patients de reanimation) - ce document-ci concerne la
chirurgie programmee de l'adulte (patients non-reanimatoires), actualise
une Conference de Consensus de 1994 distincte, methodologie et perimetre
clinique differents (evaluation nutritionnelle perioperatoire, jeune
preoperatoire, pharmaconutrition, obesite/chirurgie bariatrique, diabete).
Aucune collision : deux documents reellement distincts.

METHODOLOGIE : methode non formalisee des "avis d'experts" (enonce
explicitement par la source : "la methodologie choisie a ete celle non
formalisee des avis d'experts"), mais REDIGEE selon les declinaisons de
force utilisees par la Sfar et la methode GRADE, explicitement definies
par la source elle-meme : recommandation FORTE = "il faut faire/ne pas
faire" ou "nous recommandons de..." (chip 1+/1-) ; recommandation FAIBLE =
"il est possible/probable de faire/ne pas faire" ou "nous proposons
d'eventuellement faire..." (chip 2+/2-). Transcription directe de cette
correspondance explicite, pas une invention. 71 recommandations numerotees
(R1-R71) - parmi celles-ci, 10 sont des enonces definitionnels/descriptifs
sans verbe modal directif (ex. seuils diagnostiques de denutrition,
constats epidemiologiques) : chip "Def." distinct, disclosed en legende,
plutot que de leur attribuer arbitrairement une force 1+/2+ qu'elles ne
portent pas explicitement.

COUVERTURE : integralite des 71 recommandations numerotees sur les 6
champs (evaluation nutritionnelle, nutrition preoperatoire, nutrition
postoperatoire, pharmaconutrition, obesite et chirurgie, diabete). PORTEE
PARTIELLE DISCLOSED (rule 2) sur les Tableaux 3-6 ("protocoles de soins"
par grade nutritionnel [GN1-GN4] x sous-groupes [obesite morbide,
diabetique, personne agee]) : ces 4 tableaux tres denses (grille croisee
periode x sous-groupe) restituent en pratique le contenu deja couvert par
les 71 recommandations elles-memes sous forme de protocoles operationnels
- plutot que de les reproduire integralement (redondant et tres volumi-
neux), seuls les elements NUMERIQUES qui n'apparaissent nulle part dans
R1-R71 (apports hydro-electrolytiques standard en l'absence d'alimenta-
tion orale, formules nutritionnelles entale/parenterale des notes a/b/d)
sont extraits dans un tableau de synthese "Protocoles nutritionnels
types" distinct. Le Tableau 1 (facteurs de risque de denutrition) et le
Tableau 2 (grade nutritionnel GN1-GN4) sont reproduits verbatim (ce sont
les 2 tableaux structurants dont les 71 recommandations dependent
directement).
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from style import *
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.units import mm

OUT = "/home/user/rfe-sfar-website/output/Fiche_SFAR_SFNEP_Nutrition_Perioperatoire_2010.pdf"

SOURCE_TXT = ("Source : « Recommandations de bonnes pratiques cliniques sur la nutrition "
              "périopératoire » — SFAR/SFNEP, Ann Fr Anesth Réanim 30 (2011) 381-389. "
              "Fiche de synthèse non officielle : se référer au texte intégral.")

def P(txt, style=S_CELL):
    return Paragraph(txt, style)

def chip(label, **kw):
    return grade_chip(label, **kw)

CW_FULL = PAGE_W - 2 * MARGIN
RCW = [CW_FULL - 14 * mm, 14 * mm]
TCW = [55 * mm, CW_FULL - 55 * mm]

def reco_table(rows, col_widths=RCW):
    data = [[P("Recommandation", S_HEAD_W), P("Force", S_HEAD_W_C)]]
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

def theme_table(rows, col_widths=TCW, head=("Thème", "Détail")):
    data = [[P(head[0], S_HEAD_W), P(head[1], S_HEAD_W)]]
    for theme, detail in rows:
        data.append([P(theme, S_CELL_B), P(detail, S_CELL)])
    t = Table(data, colWidths=col_widths, repeatRows=1)
    style_cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), NAVY), ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTNAME", (0, 0), (-1, 0), FONT_BOLD), ("FONTSIZE", (0, 0), (-1, 0), 8),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.5, GREY_LIGHT),
        ("TOPPADDING", (0, 0), (-1, -1), 3.4), ("BOTTOMPADDING", (0, 0), (-1, -1), 3.4),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            style_cmds.append(("BACKGROUND", (0, i), (-1, i), BG_PANEL))
    t.setStyle(TableStyle(style_cmds))
    return t

def legend_flowable():
    chip_w = 14 * mm
    content_w = CW_FULL
    row = Table([[chip("1+", width=chip_w - 2 * mm), chip("1-", width=chip_w - 2 * mm),
                  chip("2+", width=chip_w - 2 * mm), chip("2-", width=chip_w - 2 * mm),
                  chip("Def.", width=chip_w - 2 * mm),
                  P("<b>Force</b> — méthode « avis d'experts » non formalisée, rédigée "
                    "selon les déclinaisons Sfar/GRADE explicitement définies par la "
                    "source. <b>1+</b> = « il faut faire »/recommandé (fort) ; "
                    "<b>1-</b> = « il ne faut pas faire »/non recommandé (fort) ; "
                    "<b>2+</b> = « il est possible/probable de faire » (faible) ; "
                    "<b>2-</b> = « il est possible/probable de ne pas faire » (faible) ; "
                    "<b>Def.</b> = énoncé définitionnel/descriptif de la source (seuil "
                    "diagnostique, constat), sans verbe modal directif propre.",
                    S_BADGE_HEAD)]],
                colWidths=[chip_w] * 5 + [content_w - 5 * chip_w])
    row.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                              ("LEFTPADDING", (0, 0), (-1, -1), 1),
                              ("RIGHTPADDING", (0, 0), (-1, -1), 1),
                              ("TOPPADDING", (0, 0), (-1, -1), 0),
                              ("BOTTOMPADDING", (0, 0), (-1, -1), 0)]))
    return row

TOTAL_PAGES = {"n": 9}

def on_page(canvas, doc, page_title):
    header_band(canvas, doc, "SFAR / SFNEP — Actualisation 2010",
                "Nutrition périopératoire (chirurgie programmée de l'adulte)",
                page_title, icon_fn=lambda c, x, y: icon_drop(c, x, y, 13 * mm), color=TEAL_DARK)
    footer_band(canvas, doc, SOURCE_TXT, f"Page {doc.page} / {TOTAL_PAGES['n']}")

# ---------------------------------------------------------------------------
def _section_intro():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Résumé :</b> Actualisation 2010 (SFAR/SFNEP) de la Conférence de Consensus "
        "1994 sur la nutrition artificielle périopératoire, étendue à la prise en "
        "charge nutritionnelle globale (alimentation orale et assistance "
        "nutritionnelle) de l'adulte en chirurgie programmée. 71 recommandations sur "
        "6 champs : évaluation de l'état nutritionnel, nutrition pré- et "
        "postopératoire, pharmaconutrition, obésité et chirurgie, diabète.",
        S_BODY), bg=GREY_LIGHT, border=GREY))
    story.append(Spacer(1, 2.5 * mm))
    story.append(P("Assistance nutritionnelle = nutrition entérale (sonde) ou "
                    "parentérale (cathéter) — les compléments nutritionnels oraux ne "
                    "sont pas considérés comme une assistance nutritionnelle. Nutrition "
                    "précoce = débutée dans les 24 premières heures après la "
                    "chirurgie.", S_BODY_SM))
    story.append(Spacer(1, 3 * mm))
    story.append(legend_flowable())
    return story

def _section_eval():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("1 — Évaluation de l'état nutritionnel périopératoire"),
        Spacer(1, 1.5 * mm),
        P("La dénutrition préopératoire est un facteur de risque indépendant de "
          "complications postopératoires (infections, retard de cicatrisation, "
          "mortalité, durée de séjour, coûts).", S_BODY_SM),
    ]))
    story.append(Spacer(1, 1 * mm))
    story.append(reco_table([
        ("R1. Les facteurs pouvant induire une dénutrition doivent être recherchés "
         "(Tableau 1).", "1+"),
        ("R2. Tout patient présentant au moins un facteur de risque de dénutrition "
         "doit bénéficier d'une évaluation de son état nutritionnel.", "1+"),
        ("R3. L'évaluation nutritionnelle doit comporter la mesure du poids actuel, "
         "l'estimation de la perte de poids par rapport au poids habituel et le "
         "calcul de l'IMC.", "1+"),
        ("R4. La mesure de l'albuminémie peut être utile en cas de difficulté de "
         "l'évaluation nutritionnelle.", "2+"),
        ("R5. En cas de chirurgie majeure, la mesure de l'albuminémie en "
         "préopératoire est probablement recommandée.", "2+"),
        ("R6. Un patient est considéré à risque de dénutrition s'il présente au "
         "moins un des facteurs de risque du Tableau 1.", "Def."),
        ("R7. Un patient est considéré dénutri (dénutrition cliniquement "
         "pertinente) s'il présente au moins un critère : IMC ≤18,5 (ou <21 si "
         ">70 ans) ; ou perte de poids récente ≥10 % ; ou albuminémie <30 g/L "
         "indépendamment de la CRP.", "Def."),
        ("R8. En chirurgie digestive non oncologique, le seuil d'albuminémie "
         "pourrait être fixé à 35 g/L pour définir une dénutrition pertinente.", "2+"),
        ("R9. En chirurgie cardiaque, un patient peut être considéré dénutri s'il a "
         "un IMC ≤24, ou une perte de poids ≥10 % en 6 mois, ou une albuminémie "
         "<37 g/L.", "2+"),
        ("R10. Un patient est très sévèrement dénutri (risque de syndrome de "
         "renutrition) s'il présente un IMC <13, ou un amaigrissement >20 % en "
         "3 mois, ou des apports oraux négligeables ≥15 jours.", "Def."),
        ("R11. Prendre en compte l'état nutritionnel, les facteurs de risque et le "
         "risque chirurgical via une stratification du risque global (grade "
         "nutritionnel, GN — Tableau 2).", "2+"),
        ("R12. Une recherche systématique des facteurs de risque de dénutrition, "
         "et si nécessaire une évaluation de l'état nutritionnel, doivent être "
         "réalisées en préopératoire par l'équipe médicochirurgicale.", "1+"),
        ("R13. Intégrer les résultats de l'évaluation nutritionnelle et du risque "
         "nutritionnel dans le dossier du patient.", "1+"),
        ("R14. Quand l'évaluation nutritionnelle n'a pas été faite en amont, elle "
         "doit être réalisée au cours de la consultation d'anesthésie.", "1+"),
        ("R15. La stratification du grade nutritionnel doit être mentionnée dans "
         "le rapport de consultation d'anesthésie.", "1+"),
    ]))
    story.append(Spacer(1, 2 * mm))
    story.append(KeepTogether([
        P("<b>Tableau 1 — Facteurs de risque de dénutrition pré- et "
          "postopératoire</b> (reproduit verbatim).", S_CELL_B),
        Spacer(1, 1 * mm),
        _tableau1_facteurs(),
    ]))
    story.append(Spacer(1, 2 * mm))
    story.append(KeepTogether([
        P("<b>Tableau 2 — Stratification du risque nutritionnel (grade "
          "nutritionnel, GN)</b> (reproduit verbatim).", S_CELL_B),
        Spacer(1, 1 * mm),
        _tableau2_gn(),
    ]))
    return story

def _tableau1_facteurs():
    rows = [
        ("Liés au patient (comorbidités)",
         "Âge >70 ans ; cancer ; hémopathie maligne ; sepsis ; pathologie chronique "
         "digestive ; insuffisance d'organe (respiratoire, cardiaque, rénale, "
         "intestinale, pancréatique, hépatique) ; pathologie neuromusculaire et "
         "polyhandicap ; diabète ; syndrome inflammatoire ; VIH/sida ; antécédent "
         "de chirurgie digestive majeure (grêle court, pancréatectomie, "
         "gastrectomie, chirurgie bariatrique) ; syndrome dépressif, troubles "
         "cognitifs, démence, syndrome confusionnel."),
        ("Symptômes persistants",
         "Dysphagie ; nausée/vomissement/satiété précoce ; douleur ; diarrhée ; "
         "dyspnée."),
        ("Liés à un traitement (traitement à risque)",
         "Traitement à visée carcinologique (chimiothérapie, radiothérapie) ; "
         "corticothérapie >1 mois ; polymédication >5 traitements."),
    ]
    return theme_table(rows, head=("Catégorie", "Facteurs de risque"))

def _tableau2_gn():
    head = ["Grade", "Définition"]
    rows = [
        ["GN 1", "Patient non dénutri, pas de facteur de risque de dénutrition, "
                 "chirurgie sans risque élevé de morbidité."],
        ["GN 2", "Patient non dénutri, ET (présence d'au moins un facteur de risque "
                 "de dénutrition OU chirurgie à risque élevé de morbidité)."],
        ["GN 3", "Patient dénutri, chirurgie sans risque élevé de morbidité."],
        ["GN 4", "Patient dénutri, chirurgie à risque élevé de morbidité."],
    ]
    data = [[P(h, S_HEAD_W) for h in head]]
    for r in rows:
        data.append([P(r[0], S_CELL_B), P(r[1], S_CELL)])
    cw = [22 * mm, CW_FULL - 22 * mm]
    t = Table(data, colWidths=cw, repeatRows=1)
    style_cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), NAVY), ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTNAME", (0, 0), (-1, 0), FONT_BOLD), ("FONTSIZE", (0, 0), (-1, 0), 8),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.5, GREY_LIGHT),
        ("TOPPADDING", (0, 0), (-1, -1), 3.4), ("BOTTOMPADDING", (0, 0), (-1, -1), 3.4),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            style_cmds.append(("BACKGROUND", (0, i), (-1, i), BG_PANEL))
    t.setStyle(TableStyle(style_cmds))
    return t

def _section_preop():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("2 — Nutrition préopératoire"),
        Spacer(1, 1.5 * mm),
        P("Un support nutritionnel préopératoire n'est pas recommandé en routine — "
          "réservé aux patients selon leur grade nutritionnel (GN).", S_BODY_SM),
    ]))
    story.append(Spacer(1, 1 * mm))
    story.append(reco_table([
        ("R16. Tout patient GN 2 ou 3 doit probablement bénéficier d'une prise en "
         "charge nutritionnelle préopératoire : conseils diététiques et "
         "compléments nutritionnels (GN 2) ; compléments, nutrition entérale ou "
         "parentérale (GN 3).", "2+"),
        ("R17. Tout patient GN 4 doit recevoir une assistance nutritionnelle "
         "préopératoire (entérale ou parentérale) d'au moins 7 à 10 jours.", "1+"),
        ("R18. Quand une assistance nutritionnelle préopératoire est indiquée, "
         "privilégier la nutrition entérale si le tube digestif est fonctionnel — "
         "la nutrition parentérale n'est alors pas recommandée.", "1+"),
        ("R19. Chez la personne âgée, les stratégies nutritionnelles préopératoires "
         "sont les mêmes que chez le sujet plus jeune ; la surveillance doit "
         "probablement être plus rapprochée (mauvaise adaptation à la dénutrition, "
         "résistance à la renutrition).", "2+"),
        ("R20. La prise en charge nutritionnelle postopératoire doit être "
         "anticipée ; le bilan préopératoire doit permettre de prévoir le type "
         "d'assistance nutritionnelle et la voie d'abord (sonde, stomie, voie "
         "veineuse).", "1+"),
        ("R21. Lors de chirurgie majeure sus-mésocolique, choisir en préopératoire "
         "la voie d'abord digestive (sonde transanastomotique, sonde de stomie) "
         "permettant de débuter précocement une nutrition entérale.", "1+"),
        ("R22. En chirurgie oncologique ORL (notamment avec radiothérapie "
         "combinée), la gastrostomie prethérapeutique, posée avant le traitement "
         "oncologique, est probablement la technique de choix.", "2+"),
        ("R23. Chez les patients sans risque de régurgitation, le jeûne "
         "préopératoire ne doit pas excéder 2 à 3 heures pour les liquides clairs "
         "et 6 heures pour un repas léger.", "1+"),
        ("R24. Chez les patients sans risque de régurgitation, la prise de "
         "liquides clairs sucrés (glucose ou maltodextrines) jusqu'à 2 heures "
         "avant la prémédication est probablement recommandée.", "2+"),
        ("R25. L'état nutritionnel d'un patient opéré en urgence doit être évalué "
         "si possible avant l'intervention, sinon dans les 48 premières heures "
         "postopératoires.", "1+"),
    ]))
    return story

def _section_postop():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("3 — Nutrition postopératoire (dont urgence)"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("R26. Reprendre le plus rapidement possible (24 premières heures) une "
         "alimentation orale selon la tolérance du patient, sauf contre-indication "
         "chirurgicale.", "1+"),
        ("R27. Chez les patients non dénutris (GN 1-2), la durée d'une assistance "
         "nutritionnelle postopératoire, quand elle est requise, ne doit pas être "
         "inférieure à 7 jours.", "1+"),
        ("R28. Chez un patient non dénutri (GN 1-2), instaurer une assistance "
         "nutritionnelle quand les apports postopératoires sont <60 % des besoins "
         "depuis 7 jours.", "1+"),
        ("R29. Chez les patients non dénutris (GN 1-2), instaurer probablement une "
         "assistance nutritionnelle précoce si les apports prévisibles seront "
         "<60 % des besoins durant les 7 jours postopératoires.", "2+"),
        ("R30. Instaurer, dès les 24 premières heures postopératoires, un support "
         "nutritionnel chez les patients dénutris (GN 3-4), qu'ils aient reçu ou "
         "non un support préopératoire.", "1+"),
        ("R31. La prise en charge nutritionnelle postopératoire d'un patient opéré "
         "en urgence n'est pas différente de celle recommandée pour la chirurgie "
         "programmée.", "Def."),
        ("R32. Fracture de l'extrémité supérieure du fémur chez la personne âgée : "
         "atteindre 30-40 kcal/kg/j et 1,2-1,5 g de protéines/kg/j ; prescrire des "
         "compléments nutritionnels oraux jusqu'à la sortie de rééducation "
         "(nutrition entérale si échec/impossibilité de la voie orale) ; "
         "prescrire de la vitamine D à 800-1200 UI/j (prévention des chutes et "
         "fractures).", "1+"),
    ]))
    return story

def _section_pharmaco():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("4 — Place de la pharmaconutrition en périopératoire"),
        Spacer(1, 1.5 * mm),
        P("Pharmaconutrition (immunonutrition) : arginine, glutamine, "
          "micronutriments, acides gras oméga-3, nucléotides — utilisés pour leur "
          "effet sur l'inflammation/l'immunité/la cicatrisation, pas seulement "
          "nutritionnel.", S_BODY_SM),
    ]))
    story.append(Spacer(1, 1 * mm))
    story.append(reco_table([
        ("R33. En chirurgie digestive oncologique programmée (dénutri ou non), "
         "prescrire en préopératoire pendant 5 à 7 jours un mélange nutritif "
         "digestif contenant une association de pharmaconutriments efficace.", "1+"),
        ("R34. Chez le patient non dénutri (GN 2) en chirurgie digestive "
         "oncologique programmée, ne pas prescrire de pharmaconutrition en "
         "postopératoire.", "1-"),
        ("R35. Chez le patient dénutri (GN 4) en chirurgie digestive oncologique "
         "programmée, poursuivre en postopératoire la pharmaconutrition "
         "digestive.", "1+"),
        ("R36. En chirurgie carcinologique ORL, prescrire probablement une "
         "pharmaconutrition selon les mêmes modalités qu'en digestif (études "
         "encore insuffisantes pour confirmer un bénéfice identique).", "2+"),
        ("R37. En chirurgie cardiaque (pontage coronaire), il n'est probablement "
         "pas recommandé de prescrire des pharmaconutriments (bénéfice sur les "
         "complications non établi).", "2-"),
        ("R38. Ne pas prescrire de pharmaconutriments contenant de l'arginine chez "
         "le patient septique ou hémodynamiquement instable.", "1-"),
        ("R39. En chirurgie programmée non compliquée, il n'est probablement pas "
         "recommandé de prescrire systématiquement de la glutamine en "
         "périopératoire.", "2-"),
        ("R40. En cas de complications postopératoires majeures, prescrire de la "
         "glutamine IV à forte dose (0,2-0,4 g/kg/j, soit 0,3-0,6 g/kg/j de "
         "dipeptide de glutamine).", "1+"),
        ("R41. Un support enrichi en oméga-3 (≥0,1 g/kg/j) est probablement "
         "recommandé en postopératoire d'une chirurgie abdominale majeure "
         "programmée.", "2+"),
        ("R42. En l'absence de données en chirurgie, la prescription de "
         "micronutriments à dose pharmacologique en périopératoire n'est pas "
         "recommandée.", "1-"),
    ]))
    return story

def _section_obesite():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("5 — Obésité et chirurgie"),
        Spacer(1, 1.5 * mm),
        P("Obésité : IMC ≥30 ; obésité morbide : IMC ≥40.", S_BODY_SM),
    ]))
    story.append(Spacer(1, 1 * mm))
    story.append(reco_table([
        ("R43. La surcharge pondérale (IMC ≥25) et l'obésité modérée (IMC 30-35) "
         "ne sont pas des facteurs de risque de mortalité postopératoire, mais "
         "l'obésité est associée à un risque accru de complications mineures et "
         "à une hospitalisation prolongée.", "Def."),
        ("R44. Pour la chirurgie bariatrique, l'obésité morbide avec IMC >50-55 "
         "est probablement associée à une surmortalité postopératoire.", "Def."),
        ("R45. Le patient obèse est un patient potentiellement dénutri.", "Def."),
        ("R46. Chez l'obèse, une perte de poids involontaire avant chirurgie est "
         "un facteur de risque de complication indépendant de la corpulence.", "Def."),
        ("R47. S'assurer que les besoins protéiques sont couverts chez le sujet "
         "âgé obèse en préopératoire (1,2-1,5 g/kg/j).", "1+"),
        ("R48. Dépister (fer sérique, ferritine) et corriger la carence en fer, "
         "plus fréquente chez l'obèse, en préopératoire.", "1+"),
        ("R49. Prévenir le risque de carence en vitamine B1 chez l'obèse en cas de "
         "perfusion de sérum glucosé ou de troubles digestifs (apport de "
         "thiamine orale ou parentérale).", "1+"),
        ("R50. Un ajustement de la supplémentation en vitamine B12 est "
         "probablement nécessaire après chirurgie entraînant une malabsorption "
         "(gastrectomie, résection iléale).", "2+"),
        ("R51. En cas d'amaigrissement avant un acte chirurgical, un bilan "
         "nutritionnel (hypoalbuminémie, carences en vitamines B1/B9/B12/C/A/D/E) "
         "est souhaitable.", "2+"),
        ("R52. Les régimes restrictifs entraînant une perte de masse maigre ne "
         "sont pas recommandés, notamment chez l'obésité commune (IMC 30-40) ou "
         "le sujet âgé obèse.", "1-"),
        ("R53. Une perte de poids volontaire préopératoire n'est pas recommandée "
         "dans les jours/semaines précédant un geste chirurgical (aucune preuve "
         "de bénéfice).", "1-"),
        ("R54. Si une perte de poids est nécessaire pour faciliter le geste "
         "opératoire (ex. cure d'éventration), une phase de stabilisation "
         "pondérale d'au moins 15 jours est probablement nécessaire.", "2+"),
        ("R55. Avant chirurgie bariatrique, le régime restrictif et/ou la perte "
         "de poids préopératoire n'est pas recommandée (ne modifie ni mortalité, "
         "ni complications, ni perte de poids à long terme).", "1-"),
        ("R56. Pour estimer les besoins protéino-énergétiques périopératoires de "
         "l'obèse, utiliser probablement le poids normalisé (IMC théorique de "
         "25 à 30).", "2+"),
        ("R57. Ne pas utiliser le poids dit « idéal ».", "1+"),
        ("R58. Le sujet obèse doit probablement recevoir un apport protéique "
         "postopératoire élevé (~1,5 g/kg de poids normalisé/j).", "2+"),
        ("R59. Il n'est probablement pas recommandé de prescrire une alimentation "
         "hypocalorique chez l'obèse en postopératoire.", "2-"),
        ("R60. Après chirurgie bariatrique, comme après toute chirurgie "
         "viscérale, une reprise alimentaire précoce est recommandée.", "1+"),
        ("R61. Après chirurgie bariatrique, la reprise alimentaire doit se faire "
         "progressivement en texture et en quantité, selon les protocoles "
         "établis par l'équipe.", "1+"),
        ("R62. Après chirurgie bariatrique, privilégier les aliments riches en "
         "protéines — apport minimal recommandé de 60 g/j.", "1+"),
    ]))
    return story

def _section_diabete():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("6 — Nutrition périopératoire chez le diabétique"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("R63. Le patient diabétique est un patient à haut risque de "
         "dénutrition.", "Def."),
        ("R64. En préopératoire, le diagnostic de dénutrition chez le sujet âgé "
         "doit faire rechercher systématiquement une hyperglycémie.", "1+"),
        ("R65. Couvrir les besoins protéino-énergétiques du patient diabétique et "
         "optimiser en conséquence son traitement antidiabétique.", "1+"),
        ("R66. Malgré un risque accru de carences vitaminiques chez le "
         "diabétique, aucune supplémentation spécifique n'est actuellement "
         "recommandée en périopératoire (besoins couverts par une alimentation "
         "variée).", "1-"),
        ("R67. En l'absence de données suffisantes, la prise de liquides clairs "
         "sucrés jusqu'à 2 heures avant la prémédication n'est probablement pas "
         "recommandée chez le patient diabétique.", "2-"),
        ("R68. L'utilisation de compléments nutritionnels oraux ou produits de "
         "nutrition entérale spécifiques pour diabétique (index glycémique "
         "faible) facilite probablement l'équilibre glycémique — l'adaptation "
         "des doses d'insuline reste l'élément primordial.", "2+"),
        ("R69. La gastroparésie (plus fréquente chez le diabétique) ne doit pas "
         "être un frein à la nutrition entérale.", "1+"),
        ("R69 (suite). Elle justifie probablement de contrôler les résidus gastriques, "
         "d'utiliser des prokinétiques et de mettre en place une sonde "
         "post-pylorique, notamment en cas de gastroparésie grave.", "2+"),
        ("R70. Les apports en glucides doivent être adaptés aux besoins "
         "énergétiques du patient ; un contrôle du débit de perfusion est "
         "recommandé.", "1+"),
        ("R71. L'insuline est le traitement de choix en cas d'hyperglycémie sous "
         "nutrition parentérale ; instaurer l'insulinothérapie selon des "
         "modalités précises et des protocoles validés (anticiper la baisse/"
         "l'arrêt de l'insulinothérapie à l'arrêt de la nutrition parentérale, "
         "risque d'hypoglycémie).", "1+"),
    ]))
    return story

def _section_protocoles_sources():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("7 — Protocoles nutritionnels types (Tableaux 3-6, synthèse)"),
        Spacer(1, 1.5 * mm),
        P("Les Tableaux 3 à 6 de la source déclinent les recommandations "
          "ci-dessus en protocoles opérationnels par grade nutritionnel (GN 1 à "
          "4) et sous-groupe (obésité morbide, diabétique, personne âgée). Ce "
          "contenu recoupe largement R1-R71 déjà couverts intégralement "
          "ci-dessus ; seuls les éléments numériques qui n'apparaissent nulle "
          "part ailleurs sont repris ici (portée partielle disclosed, voir "
          "méthodologie).", S_BODY_SM),
    ]))
    story.append(Spacer(1, 1.5 * mm))
    story.append(theme_table([
        ("Hydro-électrolytique standard (GN 1-3, en l'absence "
         "d'alimentation orale)",
         "1,5 à 2,5 L/24h de solution glucosée à 5 % (75-125 g de glucose) + "
         "50-100 mmol de NaCl/24h + 40-80 mmol de KCl/24h."),
        ("Assistance nutritionnelle — formule entérale",
         "25-30 kcal/kg/j dont 1,2-1,5 g/kg de protéines ; si sonde "
         "naso-gastrique, utiliser une sonde Charrière 10 silicone ou "
         "polyuréthane (pas de sonde de Salem)."),
        ("Assistance nutritionnelle — formule parentérale",
         "25-30 kcal/kg/j dont 0,20-0,25 g d'azote/kg/j, avec électrolytes "
         "(50-100 mmol NaCl/24h + 40-80 mmol KCl/24h), vitamines et "
         "oligoéléments."),
        ("Glutamine IV (complications postopératoires graves)",
         "0,3 g/kg/j, sans dépasser 21 jours de traitement."),
        ("GN 4 — dénutrition très sévère (IMC <13, amaigrissement >20 % en "
         "3 mois, apports oraux négligeables ≥15 jours)",
         "Nutrition préopératoire d'au moins 21 jours ; renutrition très "
         "progressive débutant à 10 kcal/kg/j avec augmentation progressive "
         "sur une semaine ; ajout systématique quotidien de thiamine "
         "(200-300 mg), phosphore (0,3-0,6 mmol/kg), magnésium (0,2 mmol/kg "
         "IV ou 0,4 mmol/kg per os), potassium (2-4 mmol/kg), vitamines et "
         "oligoéléments, avec évaluation biologique quotidienne."),
        ("GN 4 — chirurgie carcinologique digestive",
         "Complément nutritif oral immunomodulateur (type Oral Impact®) : "
         "3 briquettes/jour pendant 5-7 jours avant le geste (utiliser la "
         "forme entérale si la voie orale est impossible)."),
    ]))
    story.append(Spacer(1, 4 * mm))
    story.append(section_bar("Sources et traçabilité", color=GREY))
    story.append(Spacer(1, 2 * mm))
    story.append(P(
        "<b>Document source :</b> « Recommandations de bonnes pratiques cliniques "
        "sur la nutrition périopératoire. Actualisation 2010 de la conférence de "
        "consensus de 1994 sur la nutrition artificielle périopératoire en "
        "chirurgie programmée de l'adulte » — SFAR / Société francophone de "
        "nutrition clinique et métabolisme (SFNEP). Coordonnateurs : C. Chambrier "
        "(Lyon), F. Sztark (Bordeaux). Organisateur délégué : S. Pierre (Toulouse). "
        "Groupe d'experts : X. Alacoque, P. Bachmann, J. Berre, I. Bourdel-"
        "Marchasson, D. Caldari, P. Chardon, V. Colomb, P. Coti-Bertrand, "
        "D. Francon, É. Paillaud, A. Petit, N. Peretti, M.-A. Piquet, D. Quillot, "
        "M. Raucoules-Aimé, A. Raynaud-Simon, P. Senesse, R. Thibault, "
        "J.-F. Zazzo.", S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P("<b>Version :</b> Ann Fr Anesth Réanim 30 (2011) 381-389 (paru "
                    "initialement dans Nutrition Clinique et Métabolisme 2010;24:145-156). "
                    "doi:10.1016/j.annfar.2011.01.014.", S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P("<b>Méthodologie :</b> avis d'experts non formalisée, rédigée selon "
                    "les déclinaisons de force Sfar/GRADE (voir légende en page 1).",
                    S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>URL source :</b> https://sfar.org/wp-content/uploads/2015/10/"
        "2_AFAR_Nutrition-artificielle-perioperatoire-en-chirurgie-programmee-de-"
        "ladulte.pdf", S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P("<b>Couverture :</b> intégralité des 71 recommandations numérotées "
                    "(R1-R71). Tableaux 3-6 (protocoles croisés GN × sous-groupe) "
                    "condensés en tableau de synthèse des seuls éléments numériques "
                    "absents de R1-R71 — portée partielle disclosed, voir méthodologie.",
                    S_SOURCE))
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Avertissement — document de 2010/2011 :</b> cette fiche de synthèse "
        "indépendante reprend l'intégralité des 71 recommandations du texte source, "
        "mais ne le remplace pas et n'est ni éditée ni validée par la SFAR/SFNEP. "
        "Les produits, dosages et disponibilités ayant pu évoluer depuis 2010, se "
        "référer à un avis spécialisé et aux recommandations actualisées avant "
        "toute décision.", S_BODY_SM), bg=GREY_LIGHT, border=GREY))
    return story

def _section_intro_eval():
    story = _section_intro()
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_eval())
    return story

def _section_postop_pharmaco():
    story = _section_postop()
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_pharmaco())
    return story

def _section_diabete_protocoles_sources():
    story = _section_diabete()
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_protocoles_sources())
    return story

def _section_eval_preop():
    story = _section_intro_eval()
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_preop())
    return story

SECTIONS = [
    ("Méthodologie, évaluation nutritionnelle & nutrition préopératoire (§1-2)",
     _section_eval_preop),
    ("Nutrition postopératoire & pharmaconutrition (§3-4)", _section_postop_pharmaco),
    ("Obésité & chirurgie (§5)", _section_obesite),
    ("Diabète, protocoles types & sources (§6-7)", _section_diabete_protocoles_sources),
]

def _make_doc(path=None):
    return SimpleDocTemplate(path or OUT, pagesize=A4,
                              leftMargin=MARGIN, rightMargin=MARGIN,
                              topMargin=32 * mm, bottomMargin=16 * mm,
                              title="Fiche SFAR-SFNEP 2010 - Nutrition perioperatoire",
                              author="Synthèse indépendante (source SFAR/SFNEP)")

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
