# -*- coding: utf-8 -*-
"""
Fiche de synthese - Groupe d'Interet en Hemostase Perioperatoire (GIHP).
"Gestion des Anticoagulants Oraux Directs pour la chirurgie et les actes
invasifs programmes : propositions reactualisees du GIHP" - Septembre 2015
(reactualisation des propositions GIHP 2011). Auteurs : P. Albaladejo,
F. Bonhomme, N. Blais, J.P. Collet, D. Faraoni, P. Fontana, A. Godier, J. Llau,
D. Longrois, P. Mismetti, E. Marret, N. Rosencher, S. Roullet, C.M. Samama,
P. Sie, J.F. Schved, A. Steib, S. Susen. 10 pages, telecharge depuis sfar.org
(download/gestion-perioperatoire-des-patients-sous-aod-pour-un-acte-programme/
?wpdmdl=33608).

METHODOLOGIE : PAS de grille de grade (ni GRADE, ni A/B/C, ni Sfar fort/
faible) - ce document est un ensemble de "propositions" pragmatiques d'un
groupe d'interet (GIHP), sans cotation formelle de la force des recommandations
ni du niveau de preuve. Aucun chip de grade n'est donc utilise dans cette
fiche (a la difference de la quasi-totalite du reste du corpus) - convention
propre a ce document, disclosed explicitement dans le panneau methodologie
pour eviter toute confusion avec les grilles GRADE/Sfar/ANAES utilisees
ailleurs.

DISCLOSURE - doublon d'indexation dans library_final.json : ce document
apparait DEUX FOIS dans l'index de bibliotheque du projet, sous deux hrefs
differents et deux annees differentes ("2021", via le lien "download" actuel
de sfar.org, et "2015", via l'ancien lien direct "wp-content/uploads/2015/09/
Reactualisation-GIHP_AOD_actes-programmes_Septembre-20151.pdf"). Verification
faite avant construction : les deux PDF ont une premiere page identique
("propositions reactualisees ... Septembre 2015") et une bibliographie finale
de 18 references strictement identique (seule la mise en page differe - 10
pages vs 14 pages selon l'outil d'export PDF utilise par sfar.org, d'ou le
nombre de pages different mais le contenu textuel identique) : il s'agit du
MEME document GIHP de septembre 2015, pas d'une actualisation 2021 distincte.
Le champ "year": "2021" de l'entree la plus recente de library_final.json
reflete donc la date de derniere modification de la PAGE sfar.org, pas une
nouvelle date de publication du document lui-meme - disclosed ici plutot que
resolu silencieusement (regle 5 du projet). Cette fiche est indexee sous les
DEUX needles (wpdmdl=33608 et le chemin wp-content/2015/09) dans
FICHE_HREF_MATCH pour que les deux entrees de bibliotheque soient reconnues
comme couvertes.

PERIMETRE — distinct de la fiche deja construite `aod_urgence` : ce document
couvre la gestion PROGRAMMEE (acte invasif elective, delai d'arret preetabli)
des AOD, alors que `aod_urgence` couvre la gestion en URGENCE (hemorragie,
chirurgie non programmee, thrombolyse d'AVC sous anticoagulant) - deux
documents complementaires mais non redondants, verifie par grep sur site/
app.js avant construction (aucune collision de perimetre trouvee).

COUVERTURE : integrale sur le texte des propositions (risque hemorragique
faible/eleve, definitions, schemas d'arret et de reprise, cas de la phase
precoce d'un evenement thromboembolique veineux, cas du catheter perimedullaire,
surveillance de la creatininemie postoperatoire), le Tableau 1 (schema
recapitulatif, reproduit fidelement depuis un rendu visuel 220dpi - texte natif
absent/fragmente pour cette page) et le Tableau 2 (indications et posologies
usuelles des 4 AOD, meme methode de transcription visuelle, la couche texte
etant fragmentee colonne par colonne par l'export PDF source). L'introduction/
contexte epidemiologique (§1) et la conclusion (§4, redondante avec le resume)
sont condenses conformement a la regle de projet 2026-09-14 (argumentaire
minimal) - l'information clinique actionnable est integralement dans les
tableaux et le texte des propositions elles-memes.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from style import *
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.units import mm

OUT = "/home/user/rfe-sfar-website/output/Fiche_GIHP_AOD_Actes_Programmes_2015.pdf"

SOURCE_TXT = ("Source : GIHP, « Gestion des AOD pour la chirurgie et les actes invasifs "
              "programmés », propositions réactualisées, septembre 2015. Fiche de synthèse "
              "non officielle : se référer au texte intégral.")

def P(txt, style=S_CELL):
    return Paragraph(txt, style)

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

def bullets(items, style=S_BODY_SM):
    html = "&bull; " + "<br/>&bull; ".join(items)
    return P(html, style)

TOTAL_PAGES = {"n": 4}

def on_page(canvas, doc, page_title):
    header_band(canvas, doc, "GIHP — PROPOSITIONS RÉACTUALISÉES, SEPTEMBRE 2015",
                "Gestion des AOD pour un acte invasif programmé",
                page_title, icon_fn=lambda c, x, y: icon_drop(c, x, y, 13 * mm), color=TEAL_DARK)
    footer_band(canvas, doc, SOURCE_TXT, f"Page {doc.page} / {TOTAL_PAGES['n']}")

# ---------------------------------------------------------------------------
def _section_intro():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Résumé :</b> pour les actes programmés à risque hémorragique <b>faible</b>, il "
        "est proposé de ne pas prendre d'AOD la veille au soir ni le matin de "
        "l'intervention (quel que soit le schéma posologique), et de reprendre le "
        "traitement selon le schéma habituel au moins 6 heures après la fin du geste. Pour "
        "les actes à risque hémorragique <b>élevé</b>, dernière prise à J-3 pour "
        "rivaroxaban/apixaban/edoxaban ; dernière prise de dabigatran à J-4 (clairance de "
        "la créatinine [ClCr] ≥ 50 mL/min) ou J-5 (ClCr 30-49 mL/min). En neurochirurgie "
        "intracrânienne et anesthésie neuraxiale, délais plus longs. Plus de place pour les "
        "relais anticoagulants ni pour le dosage des concentrations d'AOD, sauf situations "
        "exceptionnelles.", S_BODY), bg=BG_PANEL, border=TEAL))
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("Méthodologie et périmètre"))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>Aucune grille de grade</b> — ce document est un ensemble de <b>propositions</b> "
        "pragmatiques du Groupe d'Intérêt en Hémostase Périopératoire (GIHP), sans cotation "
        "formelle de la force des recommandations (ni GRADE, ni A/B/C, ni fort/faible Sfar). "
        "Aucun chip de grade n'est donc utilisé dans cette fiche.", S_BODY_SM))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>⚠ Doublon d'indexation :</b> ce document apparaît deux fois dans l'index "
        "bibliothèque du projet (« 2021 » et « 2015 », deux URL sfar.org différentes) mais "
        "il s'agit du <b>même document GIHP de septembre 2015</b> — page de titre et "
        "bibliographie de 18 références strictement identiques entre les deux PDF, seule la "
        "mise en page diffère (10 vs 14 pages). Le « 2021 » reflète la date de dernière "
        "modification de la page sfar.org, pas une nouvelle publication.", S_NOTE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>Distinct de la fiche « AOD : chirurgie et hémorragie en urgence » :</b> ce "
        "document couvre la gestion <b>programmée</b> (acte électif, délai d'arrêt "
        "préétabli) ; l'autre fiche couvre la gestion en <b>urgence</b> (hémorragie, acte non "
        "programmé, thrombolyse). Deux documents complémentaires, non redondants.",
        S_NOTE))
    return story

# ---------------------------------------------------------------------------
def _section_risque_faible():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("1. Gestes à risque hémorragique faible"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(theme_table([
        ("Définition",
         "Actes responsables de saignements peu fréquents, de faible intensité ou aisément "
         "contrôlés, réalisables chez un patient anticoagulé à taux thérapeutiques (critères "
         "HAS 2008 pour les AVK, étendus par extension aux AOD). Exemples non limitatifs : "
         "chirurgie cutanée, chirurgie de la cataracte, certains actes de rhumatologie, de "
         "chirurgie bucco-dentaire, d'endoscopie digestive."),
        ("Avant le geste",
         "Pas de prise la veille au soir ni le matin de l'intervention, quel que soit le "
         "schéma posologique du patient (2 prises/j : saute les 2 prises précédant "
         "l'acte ; 1 prise le matin : saute 1 prise ; 1 prise le soir : saute 1 prise, "
         "dernière prise l'avant-veille au soir). Objectif : éviter une concentration "
         "plasmatique élevée pendant le geste, pas d'obtenir une concentration nulle."),
        ("Relai et dosage",
         "Pas de relai par héparine (HNF/HBPM) en préopératoire. Pas d'indication à la "
         "mesure de la concentration de l'AOD avant l'intervention."),
        ("Après le geste",
         "Reprise à l'heure habituelle du schéma du patient, au moins 6 heures après la "
         "fin de l'acte invasif (le soir de l'acte pour une prise unique le soir ou une "
         "prise biquotidienne ; le lendemain matin pour une prise unique le matin)."),
        ("Accident hémorragique peropératoire",
         "Le schéma postopératoire à appliquer devient celui du risque hémorragique "
         "élevé : reprise du traitement retardée, thromboprophylaxie veineuse "
         "(mécanique ou médicamenteuse) prescrite si risque thrombo-embolique."),
    ], TCW, head=("Thème", "Proposition")))
    return story

def _section_risque_eleve():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("2. Gestes à risque hémorragique élevé"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(theme_table([
        ("Définition",
         "Geste ne pouvant raisonnablement être réalisé en présence d'anticoagulant "
         "(fenêtre sans anticoagulant nécessaire pour une hémostase optimale) — regroupe "
         "les catégories parfois distinguées ailleurs en « risque modéré » et « risque "
         "majeur »."),
        ("Avant le geste",
         "Dernière prise à J-3 pour rivaroxaban, apixaban et edoxaban (ClCr > 30 mL/min, "
         "pharmacocinétiques similaires). Pour le dabigatran (élimination principalement "
         "rénale) : dernière prise à J-4 si ClCr ≥ 50 mL/min, à J-5 si ClCr entre 30 et 50 "
         "mL/min — nécessite une créatininémie récente (< 1 an en l'absence "
         "d'événement intercurrent). Ces délais supposent un schéma posologique adapté à "
         "la ClCr actuelle (formule de Cockcroft-Gault), à l'âge, et à l'absence "
         "d'interaction médicamenteuse susceptible d'augmenter les concentrations "
         "plasmatiques d'AOD (inhibiteurs de la P-glycoprotéine pour tous les AOD, "
         "inhibiteurs du CYP3A4 pour les -xabans)."),
        ("Procédures à très haut risque hémorragique",
         "Neurochirurgie intracrânienne, ponctions/anesthésies neuraxiales : schéma "
         "adapté par une équipe multidisciplinaire référente, délai d'arrêt plus long "
         "(dernière prise à J-5 pour les -xabans et le dabigatran en l'absence "
         "d'insuffisance rénale), sans relai héparinique. Techniques rachidiennes/blocs "
         "profonds déconseillés si une concentration détectable d'AOD reste possible — "
         "notamment dabigatran chez le patient > 80 ans ou insuffisant rénal."),
        ("Phase précoce d'un événement thromboembolique veineux",
         "Sous rivaroxaban 15 mg x2/j (3 semaines) ou apixaban 10 mg x2/j (10 jours) en "
         "phase de traitement initial d'une TVP/EP, le schéma standard du Tableau 1 ne "
         "s'applique pas — programmer une chirurgie doit rester rare, stratégie "
         "personnalisée par une équipe multidisciplinaire référente."),
        ("Relai et dosage",
         "Pas de relai héparinique en préopératoire avec les schémas proposés (sauf cas "
         "exceptionnel à très haut risque thrombotique, décision multidisciplinaire — "
         "AOD et héparine jamais administrés simultanément). Pas de dosage/test "
         "d'hémostase standard hors circonstance exceptionnelle ou recherche clinique, si "
         "les délais sont respectés et sans suspicion d'accumulation."),
        ("Après le geste — dose prophylactique",
         "Si une thromboprophylaxie veineuse est indiquée : héparine (HNF/HBPM) ou "
         "fondaparinux au moins 6 heures après la fin de l'acte invasif ; l'AOD à dose "
         "adaptée à la prévention de la MTEV peut ensuite être prescrit, sans "
         "chevauchement lors du changement de molécule."),
        ("Après le geste — dose curative",
         "Dès que l'hémostase chirurgicale le permet (à titre indicatif, entre 24 et 72 "
         "heures), l'AOD initial peut être repris à dose adaptée — sauf en présence d'un "
         "cathéter d'analgésie périmédullaire, où l'anticoagulation thérapeutique doit se "
         "faire par héparine jusqu'au retrait du cathéter. Première dose « curative » "
         "d'AOD administrée 12 heures après la dernière injection sous-cutanée d'HBPM à "
         "dose prophylactique."),
        ("Surveillance postopératoire",
         "Créatininémie mesurée en postopératoire si l'acte et/ou l'état du patient font "
         "craindre une altération de la fonction rénale — une baisse de la ClCr impose "
         "d'adapter la dose d'AOD ou de changer de molécule anticoagulante."),
    ], TCW, head=("Thème", "Proposition")))
    return story

def _section_risques_all():
    story = _section_risque_faible()
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_risque_eleve())
    return story

# ---------------------------------------------------------------------------
T1_HEAD_STYLE = pstyle("t1_head", fontSize=8, leading=9.6, textColor=WHITE, fontName=FONT_BOLD,
                       alignment=TA_CENTER)
T1_CELL = pstyle("t1_cell", fontSize=8, leading=10, textColor=INK, alignment=TA_CENTER)
T1_CELL_L = pstyle("t1_cell_l", fontSize=8, leading=10, textColor=INK, fontName=FONT_BOLD)

def _tableau1():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(P("<b>Tableau 1 — Gestion périopératoire des AOD en fonction du risque "
                    "hémorragique</b> (transcrit fidèlement depuis un rendu visuel 220dpi, "
                    "page 7 du PDF source)", S_CELL_B))
    story.append(Spacer(1, 1.2 * mm))
    t = Table([
        ["", Paragraph("Risque hémorragique faible", T1_HEAD_STYLE),
         Paragraph("Risque hémorragique élevé", T1_HEAD_STYLE)],
        [Paragraph("Avant<br/>le geste", T1_CELL_L),
         Paragraph("Pas de prise la veille au soir ni le matin de l'acte invasif", T1_CELL),
         Paragraph("Rivaroxaban / apixaban / edoxaban, ClCr ≥ 30 mL/min → dernière prise à "
                    "J-3<br/>Dabigatran, ClCr ≥ 50 mL/min → dernière prise à J-4<br/>"
                    "Dabigatran, ClCr 30-49 mL/min → dernière prise à J-5", T1_CELL)],
        ["", Paragraph("<b>Pas de relai — Pas de dosage</b>", T1_CELL), ""],
        [Paragraph("Après<br/>le geste", T1_CELL_L),
         Paragraph("Reprise à l'heure habituelle, au moins 6 h après la fin de l'acte "
                    "invasif", T1_CELL),
         Paragraph("Anticoagulant dose « prophylactique » au moins 6 h après l'acte si "
                    "thromboprophylaxie indiquée ; dose « curative » dès que l'hémostase "
                    "le permet (indicativement 24-72 h)", T1_CELL)],
    ], colWidths=[22 * mm, (CW_FULL - 22 * mm) / 2, (CW_FULL - 22 * mm) / 2])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("SPAN", (1, 2), (2, 2)),
        ("GRID", (0, 0), (-1, -1), 0.5, GREY_LIGHT),
        ("BACKGROUND", (0, 1), (0, -1), BG_PANEL),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 3.6), ("BOTTOMPADDING", (0, 0), (-1, -1), 3.6),
        ("LEFTPADDING", (0, 0), (-1, -1), 4), ("RIGHTPADDING", (0, 0), (-1, -1), 4),
    ]))
    story.append(t)
    return story

# ---------------------------------------------------------------------------
T2_HEAD = pstyle("t2_head", fontSize=7.6, leading=9, textColor=WHITE, fontName=FONT_BOLD,
                  alignment=TA_CENTER)
T2_ROWHEAD = pstyle("t2_rh", fontSize=7.6, leading=9.2, textColor=WHITE, fontName=FONT_BOLD)
T2_CELL = pstyle("t2_cell", fontSize=7.4, leading=9, textColor=INK, alignment=TA_CENTER)

def _tableau2():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(P("<b>Tableau 2 — Indications et posologies usuelles des AOD</b> (transcrit "
                    "fidèlement depuis un rendu visuel 220dpi, page 8 du PDF source)",
                    S_CELL_B))
    story.append(Spacer(1, 1.2 * mm))
    colw = [30 * mm] + [(CW_FULL - 30 * mm) / 4.0] * 4
    data = [
        [Paragraph("Indication", T2_HEAD), Paragraph("dabigatran<br/>Pradaxa®", T2_HEAD),
         Paragraph("rivaroxaban<br/>Xarelto®", T2_HEAD), Paragraph("apixaban<br/>Eliquis®", T2_HEAD),
         Paragraph("edoxaban<br/>Lixiana®", T2_HEAD)],
        [Paragraph("Prévention de la TVP après chirurgie orthopédique majeure", T2_ROWHEAD),
         Paragraph("220 mg x1/j ou 150 mg x1/j si ClCr 30-50 mL/min, inhibiteurs P-gp, âge "
                    "≥ 75 ans — PTH : 28-35 j ; PTG : 10 j", T2_CELL),
         Paragraph("10 mg x1/j — PTH : 5 sem. ; PTG : 2 sem.", T2_CELL),
         Paragraph("2,5 mg x2/j — PTH : 32-38 j ; PTG : 10-14 j", T2_CELL),
         Paragraph("NA", T2_CELL)],
        [Paragraph("Traitement de la TVP ou EP / prévention de la MTEV au long cours", T2_ROWHEAD),
         Paragraph("150 mg x2/j ou 110 mg x2/j si âge ≥ 80 ans ou prise de vérapamil", T2_CELL),
         Paragraph("15 mg x2/j (3 sem.), puis 20 mg x1/j", T2_CELL),
         Paragraph("10 mg x2/j (7 j), puis 5 mg x2/j, puis 2,5 mg x2/j en prévention des "
                    "récidives après 6 mois de traitement d'une TVP/EP", T2_CELL),
         Paragraph("60 mg x1/j ou 30 mg x1/j si ClCr 15-50 mL/min, poids ≤ 60 kg, "
                    "inhibiteurs P-gp", T2_CELL)],
        [Paragraph("Prévention des AVC et embolies dans la FA non valvulaire", T2_ROWHEAD),
         Paragraph("150 mg x2/j ou 110 mg x2/j si âge ≥ 80 ans ou prise de vérapamil", T2_CELL),
         Paragraph("20 mg x1/j ou 15 mg x1/j si ClCr 30-49 mL/min", T2_CELL),
         Paragraph("5 mg x2/j ou 2,5 mg x2/j si 2 critères parmi : âge ≥ 80 ans, poids ≤ "
                    "60 kg, créatinine ≥ 133 µmol/L", T2_CELL),
         Paragraph("60 mg x1/j ou 30 mg x1/j si ClCr 15-50 mL/min, poids ≤ 60 kg, "
                    "inhibiteurs P-gp", T2_CELL)],
    ]
    t = Table(data, colWidths=colw, repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("BACKGROUND", (0, 1), (0, -1), TEAL_DARK), ("TEXTCOLOR", (0, 1), (0, -1), WHITE),
        ("GRID", (0, 0), (-1, -1), 0.5, GREY_LIGHT),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 3.2), ("BOTTOMPADDING", (0, 0), (-1, -1), 3.2),
        ("LEFTPADDING", (0, 0), (-1, -1), 3), ("RIGHTPADDING", (0, 0), (-1, -1), 3),
    ]))
    story.append(t)
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "TVP : thrombose veineuse profonde ; EP : embolie pulmonaire ; MTEV : maladie "
        "thromboembolique veineuse ; AVC : accident vasculaire cérébral ; FA : fibrillation "
        "atriale ; PTH/PTG : prothèse totale de hanche/genou ; ClCr : clairance de la "
        "créatinine (Cockcroft-Gault) ; P-gp : P-glycoprotéine ; NA : non applicable.",
        S_SOURCE))
    return story

def _section_tableaux():
    story = _tableau1()
    story.extend(_tableau2())
    return story

# ---------------------------------------------------------------------------
def _section_sources():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("Sources et avertissement"))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "GIHP, « Gestion des Anticoagulants Oraux Directs pour la chirurgie et les actes "
        "invasifs programmés : propositions réactualisées », septembre 2015 (réactualisation "
        "des propositions GIHP 2011). 18 références bibliographiques dans le texte intégral.",
        S_SOURCE))
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Avertissement — document de 2015 :</b> cette fiche est une synthèse "
        "indépendante, produite pour un usage d'aide-mémoire. Elle reprend l'intégralité des "
        "propositions et des deux tableaux du texte source, mais ne remplace pas le texte "
        "intégral et n'est ni éditée ni validée par le GIHP/SFAR. Les posologies, la "
        "disponibilité de nouveaux AOD/antidotes et les pratiques de gestion périopératoire "
        "ayant pu évoluer depuis 2015, se référer à un avis spécialisé et aux recommandations "
        "actualisées avant toute décision thérapeutique.", S_BODY_SM), bg=GREY_LIGHT, border=GREY))
    return story

# ---------------------------------------------------------------------------
def _section_all():
    story = _section_intro()
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_risques_all())
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_tableaux())
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_sources())
    return story

SECTIONS = [
    ("Méthodologie, gestes à risque faible/élevé, tableaux 1-2 & sources", _section_all),
]

def _make_doc(path=None):
    return SimpleDocTemplate(path or OUT, pagesize=A4,
                              leftMargin=MARGIN, rightMargin=MARGIN,
                              topMargin=32 * mm, bottomMargin=16 * mm,
                              title="Fiche GIHP 2015 - Gestion des AOD pour un acte programme",
                              author="Synthèse indépendante (source GIHP)")

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
