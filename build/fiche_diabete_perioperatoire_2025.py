# -*- coding: utf-8 -*-
"""
Fiche de synthese - "Prise en charge du patient diabetique en peri
operatoire" - Fiches simplifiees, Groupe SFAR/SFD (G. Cheisson, D.
Benhamou, E. Cosson, C. Ichai, S. Jacqueminet, B. Nicolescu-Catargi, A.
Ouattara, I. Tauveron), Version 2025. 11 pages (1 page de titre + 10 pages
d'algorithmes/tableaux), telecharge depuis sfar.org (download/prise-en-
charge-du-patient-diabetique-en-peri-operatoire/?wpdmdl=122568).

METHODOLOGIE : AUCUNE grille de grade / GRADE / niveau de preuve imprime -
il s'agit d'un jeu de "fiches simplifiees" (algorithmes decisionnels et
tableaux posologiques prets a l'emploi), pas d'une RFE/RPC classique. Pas
de chip invente ici (meme famille documentaire que fiche_aod_programme.py
et fiche_preparation_colique.py).

TRANSCRIPTION D'ALGORITHMES GRAPHIQUES - IMPORTANT : les 10 pages de
contenu sont des diagrammes/tableaux avec tres peu de texte narratif ;
l'extraction PyMuPDF produit un flux de texte deconnecte de la mise en
page reelle (chiffres et libelles extraits hors de leur alignement visuel
d'origine). CHAQUE algorithme a donc ete transcrit en le RENDANT a 200-400
dpi (PyMuPDF get_pixmap, avec recadrages cibles a 400dpi pour lever toute
ambiguite sur les bornes numeriques exactes des echelles de glycemie) et
en LISANT VISUELLEMENT la position/couleur de chaque case du diagramme,
jamais en se fiant a l'ordre du texte extrait brut - conformement a la
regle de projet "reproduire tableaux/figures verbatim... rendre et
transcrire visuellement". Les tableaux a cellules fusionnees du PDF source
(ex. l'echeancier glycemies capillaires pre-operatoire, le protocole IVSE
a 8 bandes) ont ete re-exprimes en tableaux simples ligne-par-bande
(une ligne = une bande de glycemie), plus lisibles sur mobile/PC sans
alterer aucune valeur numerique ni conduite a tenir.

PERIMETRE : integral sur les 10 pages de contenu (Generalites DT1/DT2,
prise en charge pre-operatoire, CAT hyperglycemie/hypoglycemie, protocoles
d'insulinotherapie IVSE et SC Basal Bolus, relais IVSE/SC, modalites de
reprise des antidiabetiques, intervention de courte duree). Document tres
recent (version 2025) - pas d'enjeu d'actualite a signaler au moment de la
construction.

AVERTISSEMENT DE SECURITE PATIENT (a conserver dans la fiche elle-meme,
pas seulement ce docstring) : ce document source est deja lui-meme un outil
de reference simplifie destine a l'usage clinique direct - cette fiche en
est une synthese supplementaire, produite pour aide-memoire uniquement.
Les posologies d'insuline doivent etre verifiees contre le texte source
original (ou un outil clinique valide) avant toute application, surtout
en cas de doute sur une valeur.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from style import *
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.units import mm

OUT = "/home/user/rfe-sfar-website/output/Fiche_SFAR_SFD_Diabete_Perioperatoire_2025.pdf"

SOURCE_TXT = ("Source : Groupe SFAR/SFD (Cheisson, Benhamou, Cosson, Ichai, Jacqueminet, "
              "Nicolescu-Catargi, Ouattara, Tauveron), « Prise en charge du patient diabétique "
              "en péri opératoire » — Fiches simplifiées, version 2025. Fiche de synthèse non "
              "officielle : se référer au texte intégral / outil clinique validé.")

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

def grid_table(head, rows, col_widths, center_cols=()):
    data = [[P(h, S_HEAD_W_C if i in center_cols or i == 0 else S_HEAD_W) for i, h in enumerate(head)]]
    for r in rows:
        row = []
        for i, cell in enumerate(r):
            style = S_CELL_C if i in center_cols else (S_CELL_B if i == 0 else S_CELL)
            row.append(P(cell, style))
        data.append(row)
    t = Table(data, colWidths=col_widths, repeatRows=1)
    style_cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), NAVY), ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTNAME", (0, 0), (-1, 0), FONT_BOLD), ("FONTSIZE", (0, 0), (-1, 0), 7.6),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("GRID", (0, 0), (-1, -1), 0.5, GREY_LIGHT),
        ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING", (0, 0), (-1, -1), 4), ("RIGHTPADDING", (0, 0), (-1, -1), 4),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            style_cmds.append(("BACKGROUND", (0, i), (-1, i), BG_PANEL))
    t.setStyle(TableStyle(style_cmds))
    return t

def bullets(items, style=S_BODY_SM):
    html = "&bull; " + "<br/>&bull; ".join(items)
    return P(html, style)

TOTAL_PAGES = {"n": 7}

def on_page(canvas, doc, page_title):
    header_band(canvas, doc, "GROUPE SFAR / SFD — FICHES SIMPLIFIÉES, 2025",
                "Prise en charge du patient diabétique en péri opératoire",
                page_title, icon_fn=lambda c, x, y: icon_pill(c, x, y, 13 * mm), color=TEAL_DARK)
    footer_band(canvas, doc, SOURCE_TXT, f"Page {doc.page} / {TOTAL_PAGES['n']}")

# ---------------------------------------------------------------------------
def _section_generalites():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Avertissement de sécurité :</b> cette fiche synthétise un document déjà conçu "
        "comme outil clinique simplifié (« Fiches simplifiées » SFAR/SFD, 2025). Elle est "
        "produite pour un usage d'aide-mémoire — vérifier toute posologie d'insuline contre "
        "le texte source intégral ou un outil clinique validé avant application, en "
        "particulier en cas de doute sur une valeur.", S_BODY), bg=RED_LIGHT, border=RED))
    story.append(Spacer(1, 2.5 * mm))
    story.append(section_bar("Généralités — DT1 et DT2"))
    story.append(Spacer(1, 1.5 * mm))
    story.append(grid_table(
        ["", "Diabète de type 1 (DT1)", "Diabète de type 2 (DT2)"],
        [
            ["Mécanisme", "Maladie auto-immune conduisant à une insulinopénie majeure",
             "Insulinorésistance avec insulinopénie relative"],
            ["Traitement", "L'apport d'insuline exogène est vital et ne peut être arrêté",
             "Régime puis antidiabétiques (AD) non insuliniques puis insuline à la phase "
             "tardive"],
            ["Complications", "Risque VITAL si arrêt de l'insuline basale (acidocétose)",
             "Accumulation des AD non insuliniques si insuffisance rénale"],
            ["Remarques", "Chirurgie pancréatique : le patient se comporte comme un DT1 si "
             "pancréatectomie", "Vérification de la fonction rénale avant reprise des AD "
             "non insuliniques"],
        ],
        [26 * mm, (CW_FULL - 26 * mm) / 2, (CW_FULL - 26 * mm) / 2],
    ))
    story.append(Spacer(1, 2.5 * mm))
    story.append(P(
        "<b>Objectifs glycémiques en péri opératoire : 5 à 10 mmol/L (0,9 à 1,8 g/L).</b> "
        "Évaluation du contrôle glycémique par le dosage d'hémoglobine glyquée (HbA1c) : "
        "récupérer le dernier dosage en consultation ou en faire un si le patient n'en a "
        "pas fait depuis plus de 3 mois, ou en cas de déséquilibre du diabète.", S_BODY_SM))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P("<b>Stratégie pré opératoire selon la valeur d'HbA1c (Groupe SFAR/SFD, 2025) :</b>",
                    S_CELL_B))
    story.append(Spacer(1, 1 * mm))
    story.append(grid_table(
        ["HbA1c", "Conduite à tenir"],
        [
            ["< 5 %", "Différer"],
            ["5 – 6 %", "Avis médecin généraliste / diabétologue"],
            ["6 – 8 %", "Intervention possible"],
            ["8 – 9 %", "Avis médecin généraliste / diabétologue"],
            ["> 9 %", "Différer"],
        ],
        [30 * mm, CW_FULL - 30 * mm], center_cols=(0,),
    ))
    story.append(Spacer(1, 1.5 * mm))
    story.append(info_panel(P(
        "<b>ATTENTION :</b> chez le patient DT1, quelle que soit la glycémie, "
        "<b>NE JAMAIS ARRÊTER L'INSULINE LENTE</b>. Si hypoglycémie : cf. « CAT devant une "
        "hypoglycémie à l'hôpital ». Si hyperglycémie : cf. « CAT devant une hyperglycémie "
        "à l'hôpital ».", S_BODY), bg=AMBER_LIGHT, border=AMBER))
    return story

# ---------------------------------------------------------------------------
def _section_preop():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Prise en charge pré opératoire (DT1 et DT2)"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(P("<b>Modalités d'arrêt des traitements antidiabétiques (AD) :</b>", S_CELL_B))
    story.append(Spacer(1, 1 * mm))
    story.append(grid_table(
        ["Traitement", "≤ 1 repas jeûné", "Intervention avec ≥ 2 repas jeûnés",
         "Intervention urgente"],
        [
            ["Metformine", "Pas d'arrêt", "Pas de prise le matin", "Arrêt"],
            ["Sulfamides, glinides, inhibiteurs α-glucosidases, inhibiteurs DPP-4",
             "Pas d'arrêt", "Pas de prise le matin", "Arrêt"],
            ["Agonistes récepteurs GLP-1",
             "Pas d'arrêt (échographie gastrique et/ou induction en séquence rapide)",
             "Pas d'arrêt (échographie gastrique et/ou induction en séquence rapide)",
             "Arrêt"],
            ["Inhibiteurs SGLT2",
             "Dernière prise 3 jours avant l'intervention (risque acidocétose "
             "euglycémique)", "idem", "Arrêt"],
            ["Insulines SC", "Pas d'arrêt", "Maintien de l'insuline lente (matin ou soir)",
             "Arrêt et relais"],
            ["Pompe à insuline", "Pas d'arrêt",
             "Arrêt de la pompe à l'arrivée au bloc*", "Arrêt et relais"],
        ],
        [42 * mm, (CW_FULL - 42 * mm) * 0.34, (CW_FULL - 42 * mm) * 0.44, (CW_FULL - 42 * mm) * 0.22],
    ))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<i>* Maintien possible d'une pompe à insuline si : intervention courte &lt; 2h ; "
        "perturbations du contrôle glycémique non attendues ; dispositif visible et à "
        "distance du champ opératoire ; glycémies artérielles/veineuses/capillaires "
        "préférées au glucose interstitiel en peropératoire ; accord du patient et de "
        "l'équipe d'anesthésie ; gestion du matériel par le patient précocement en post "
        "opératoire ; avis du diabétologue pour l'adaptation des débits.</i>", S_NOTE))
    story.append(Spacer(1, 2 * mm))
    story.append(P("<b>Règles de jeûne :</b>", S_CELL_B))
    story.append(Spacer(1, 1 * mm))
    story.append(bullets([
        "Repas du soir normal ; donner le traitement habituel (AD non insuliniques et/ou "
        "insulines aux mêmes posologies)",
        "Dernier repas solide à H-6, liquides clairs autorisés jusqu'à H-2 de l'intervention",
        "Perfusion de soluté glucosé <b>si et seulement si</b> : jeûne + insuline lente "
        "injectée (matin ou soir) ou pompe à insuline en cours → G10 % 40 mL/h à partir du "
        "premier repas jeûné ; ou jeûne prolongé (apports glucosés quotidiens nécessaires, "
        "100 à 150 g de glucose, ex. G10 % 40 mL/h)",
    ]))
    story.append(Spacer(1, 2 * mm))
    story.append(P(
        "<b>En pré opératoire, faire les glycémies capillaires (GC) et appliquer ce "
        "protocole</b> (bandes identiques à chaque échéance : GC &lt; 0,9 g/L [&lt; 5 "
        "mmol/L] ; 0,9-1,8 g/L [5-10 mmol/L] = cible, aucune correction ; 1,8-2,2 g/L "
        "[10-12 mmol/L] ; 2,2-3 g/L [12-16,5 mmol/L] ; &gt; 3 g/L [&gt; 16,5 mmol/L]) :",
        S_BODY_SM))
    story.append(Spacer(1, 1 * mm))
    story.append(grid_table(
        ["Échéance", "GC < 0,9 g/L (< 5 mmol/L)", "1,8-2,2 g/L (10-12 mmol/L)",
         "2,2-3 g/L (12-16,5 mmol/L)", "GC > 3 g/L (> 16,5 mmol/L)"],
        [
            ["Avant le repas du soir", "Sucre 15 g PO (prévenir le médecin)",
             "Analogue rapide 3 UI SC (si correction non faite par le patient)",
             "Analogue rapide 4 UI SC",
             "Analogue rapide 6 UI SC + recherche de cétose (prévenir le médecin)"],
            ["Au coucher (22h-0h) / si besoin (3h-4h)",
             "15 g PO ; GC à 15 min (prévenir le médecin)", "3 UI SC", "4 UI SC",
             "6 UI SC + recherche de cétose, ou IVSE en réa (prévenir le médecin)"],
            ["6h-7h",
             "Pas de prise d'AD non insuliniques ; G10 % 40 mL/h si insuline lente "
             "injectée ou pompe en cours", "idem", "idem", "VVP NaCl 0,9 %"],
            ["Pré opératoire (GC/3h)", "G10 % 60 mL/h (prévenir le médecin)", "3 UI SC",
             "4 UI SC", "IVSE en réa ; différer le bloc"],
        ],
        [30 * mm] + [(CW_FULL - 30 * mm) / 4] * 4,
    ))
    story.append(P(
        "<i>De 19h à 20h (tous les cas) : repas normal ± insulines habituelles ± AD non "
        "insuliniques. GC entre 0,9 et 1,8 g/L (5-10 mmol/L) : cible atteinte, aucune "
        "correction à aucune échéance.</i>", S_NOTE))
    return story

# ---------------------------------------------------------------------------
def _section_hyperglycemie():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("CAT devant une glycémie ≥ 16,5 mmol/L (3 g/L)"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(P(
        "Rechercher une cétose en préférant la cétonémie à la cétonurie.", S_BODY_SM))
    story.append(Spacer(1, 1 * mm))
    story.append(grid_table(
        ["Cétose", "Conduite à tenir", "Surveillance"],
        [
            ["Cétonémie < 0,5 mmol/L ; cétonurie = 0", "Faire 6 UI SC d'analogue rapide de "
             "l'insuline", "Surveillance glycémie à H4"],
            ["0,5 ≤ cétonémie ≤ 1,5 mmol/L ; cétonurie à 1 croix", "Faire 10 UI SC "
             "d'analogue rapide de l'insuline", "Contrôle glycémie et recherche de cétose "
             "à H4"],
            ["Cétonémie > 1,5 mmol/L ; cétonurie ≥ 2 croix", "Faire un GDS artériel pour "
             "rechercher une acidose", "Transfert en USC pour insulinothérapie IVSE"],
        ],
        [55 * mm, (CW_FULL - 55 * mm) / 2, (CW_FULL - 55 * mm) / 2],
    ))
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        P("<b>Cas particulier — traitement par inhibiteur SGLT2 ET arrêt &lt; 3 jours</b> "
          "(risque d'acidocétose euglycémique) :", S_CELL_B),
        Spacer(1, 1 * mm),
    ]))
    story.append(grid_table(
        ["Cétose", "Glycémie 8-12 mmol/L (1,5-2,2 g/L)", "Glycémie 12-16,4 mmol/L (2,2-2,99 g/L)",
         "Glycémie ≥ 16,5 mmol/L (3 g/L)"],
        [
            ["Cétonémie < 0,5 mmol/L ; cétonurie = 0", "Si hyperglycémie : cf. CAT "
             "hyperglycémie ≥ 16,5 mmol/L. Surveillance cétonémie à H12.", "idem", "idem"],
            ["0,5 ≤ cétonémie ≤ 1,5 mmol/L ; cétonurie à 1 croix (si pH > 7,20 au GDS)",
             "Analogue rapide 4 UI SC + 15 g glucose PO ou 3 g IVD",
             "Analogue rapide 6 UI SC", "Analogue rapide 10 UI SC"],
            ["Cétonémie > 1,5 mmol/L ; cétonurie ≥ 2 croix, ou pH ≤ 7,20 au GDS",
             "Faire un GDS artériel, éliminer une autre cause d'acidose métabolique "
             "(hyperlactatémie, hyperchlorémie, hypercapnie) → transfert en USC pour "
             "insulinothérapie IVSE si pH ≤ 7,20", "idem", "idem"],
        ],
        [55 * mm] + [(CW_FULL - 55 * mm) / 3] * 3,
    ))
    return story

# ---------------------------------------------------------------------------
def _section_hypoglycemie():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("CAT devant une hypoglycémie à l'hôpital"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(grid_table(
        ["État du patient", "Glycémie", "Conduite à tenir"],
        [
            ["Patient conscient", "< 3,3 mmol/L (0,6 g/L)",
             "Sucre PO : 3 morceaux de sucre ou 20 cL de jus de fruit"],
            ["Patient inconscient", "2,2 < glycémie < 3,3 mmol/L",
             "Glucose IV : 3 g soit 1 ampoule de 10 mL de G30 % IVD"],
            ["Patient inconscient", "< 2,2 mmol/L (0,4 g/L)",
             "Glucose IV : 6 g soit 2 ampoules de 10 mL de G30 % IVD"],
        ],
        [32 * mm, 40 * mm, CW_FULL - 32 * mm - 40 * mm],
    ))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>Contrôle de la glycémie à 15 min :</b> si glycémie ≥ 3,3 mmol/L (0,6 g/L) → "
        "contrôle glycémie à 1 heure, puis si toujours ≥ 3,3 mmol/L la prise en charge "
        "s'arrête là ; si &lt; 3,3 mmol/L à 1 heure ou dès le contrôle à 15 min → "
        "<b>reprendre l'arbre décisionnel et prévenir le médecin</b>.", S_BODY_SM))
    return story

# ---------------------------------------------------------------------------
def _section_ivse():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Protocole d'insulinothérapie IVSE"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(P(
        "<b>Objectifs glycémiques peropératoires : 5-10 mmol/L (0,9-1,8 g/L).</b> "
        "Modalités : en unités de soins critiques ou bloc opératoire seulement. Dilution : "
        "analogue rapide de l'insuline 1 UI/mL dans NaCl 0,9 %. Voie d'abord : robinet "
        "proximal sur cathéter central ou sur voie veineuse périphérique. Apports "
        "glucosés au bloc (G10 % 40 mL/h) sauf si hyperglycémie &gt; 16,5 mmol/L.",
        S_BODY_SM))
    story.append(Spacer(1, 1.5 * mm))
    story.append(grid_table(
        ["Glycémie", "Bolus IVD initial", "Débit IVSE initial", "Fréq. contrôle",
         "Adaptation du débit", "G30 %"],
        [
            ["< 2,2 mmol/L (< 0,4 g/L)", "0", "0", "15 min",
             "Arrêt (reprise à ½ débit si glyc > 5,5 DT1 / > 10 DT2)",
             "2 amp (6 g), prévenir médecin"],
            ["2,2-3,3 mmol/L (0,4-0,6 g/L)", "0", "0", "30 min",
             "Arrêt (reprise à ½ débit si glyc > 5,5 DT1 / > 10 DT2)", "1 amp 10 mL (3 g)"],
            ["3,3-5 mmol/L (0,6-0,9 g/L)", "0", "0", "1 h", "− 1 UI/h", "0"],
            ["5-6 mmol/L (0,9-1,1 g/L)", "0", "1 UI/h (DT1) ou 0 UI/h (DT2)", "1 h",
             "− 1 UI/h", "0"],
            ["6-10 mmol/L (1,1-1,8 g/L)", "0", "1 UI/h (DT1) ou 0 UI/h (DT2)", "2 h",
             "idem (pas de changement)", "0"],
            ["10-14 mmol/L (1,8-2,5 g/L)", "3 UI", "2 UI/h", "1 h", "+ 1 UI/h", "0"],
            ["14-16,5 mmol/L (2,5-3 g/L)", "4 UI", "3 UI/h", "1 h", "+ 2 UI/h", "0"],
            ["> 16,5 mmol/L (> 3 g/L)", "6 UI", "4 UI/h, prévenir médecin", "1 h",
             "Bolus 6 UI, prévenir médecin", "0"],
        ],
        [30 * mm, 18 * mm, 32 * mm, 16 * mm, 34 * mm, CW_FULL - (30 + 18 + 32 + 16 + 34) * mm],
    ))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<i>Remarques : privilégier les mesures de glycémie sur sang total (artériel ou "
        "veineux), si possible sur machine à gaz du sang. Surveillance de la kaliémie : "
        "objectif 4 à 4,5 mmol/L, contrôle/4h si stable sinon à chaque changement de débit. "
        "Pas de relais SC si insuline IVSE &gt; 4 UI/h. Arrêt du protocole IVSE et relais "
        "dès que glycémies stabilisées et ≤ 10 mmol/L (1,8 g/L), si alimentation orale, ou "
        "à la sortie de SSPI/soins critiques avec relais par insuline SC ou pompe.</i>",
        S_NOTE))
    return story

# ---------------------------------------------------------------------------
def _section_relais_basalbolus():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Relais insuline IVSE / SC"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(theme_table([
        ("Indications au relais",
         "Dès que les glycémies sont stabilisées et ≤ 10 mmol/L (1,8 g/L) ; reprise d'une "
         "alimentation orale (non une condition en soi) ; relais à l'arrêt de l'insuline "
         "IVSE si posologie ≤ 4 UI/h."),
        ("Contre-indications au relais",
         "Posologie d'insuline IVSE > 4 UI/h ; besoins en insuline non stabilisés."),
        ("Pas de relais SC si",
         "Posologie d'insuline IVSE ≤ 0,5 UI/h chez un patient non insulinotraité "
         "antérieurement. <b>Pas d'insuline IVSE en salle d'hospitalisation "
         "conventionnelle.</b>"),
        ("Calcul de dose (2 méthodes)",
         "Si quantité d'insuline inconnue : dose insuline lente SC 1×/soir = 0,3 UI/kg/24h "
         "; dose d'analogue rapide SC par repas = 0,3 UI/kg/24h divisée par 3. "
         "OU, à partir de la quantité totale d'insuline IVSE sur 24h : dose insuline lente "
         "SC 1×/soir = ½ dose IVSE/24h ; dose d'analogue rapide SC par repas = ½ dose "
         "IVSE/24h divisée par 3."),
        ("Modalités",
         "Pas de délai entre l'arrêt de l'insuline IVSE et l'injection d'insuline lente : "
         "faite en SSPI. Injection d'insuline lente SC prescrite de préférence à 20h ; "
         "sinon, injection complémentaire pour couvrir les besoins jusqu'à 20h selon le "
         "schéma : arrêt IVSE entre 0h-6h → 3/4 dose (prochaine dose à 20h le soir même) ; "
         "entre 6h-14h → 1/2 dose (20h le soir même) ; entre 14h-16h → 1/4 dose (20h le "
         "soir même) ; entre 16h-0h → dose de 20h (prochaine dose à 20h le jour suivant)."),
    ], [42 * mm, CW_FULL - 42 * mm]))
    return story

def _section_basalbolus():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Protocole d'insulinothérapie SC type Basal Bolus"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(theme_table([
        ("1. Basal (insuline lente)",
         "0,3 UI/kg/j SC à 20h (ou dose habituelle, ou 1/2 dose IV des dernières 24h). "
         "Adaptation à la glycémie du matin suivant à jeun : &lt; 5 mmol/L (0,9 g/L) → "
         "− 2 UI ; 5-10 mmol/L (0,9-1,8 g/L) → idem ; &gt; 10 mmol/L (1,8 g/L) → + 2 UI."),
        ("2. Bolus pour le repas",
         "Analogue rapide de l'insuline SC avant chaque repas oral, quelle que soit la "
         "glycémie : 0,1 UI/kg SC. Faire la moitié de la dose si apports caloriques "
         "insuffisants. Ne pas faire si alimentation entérale ou parentérale continue."),
        ("3. Bolus correcteur",
         "Analogue rapide SC à adapter selon glycémie, à additionner au bolus du repas "
         "(8h, 12h, 20h) ; glycémie pré-prandiale à 8h/12h/20h, et à 16h/0h/4h si "
         "déséquilibre important. Échelle : 3,3-5 mmol/L (0,6-0,9 g/L) → 0 ; 5-10 mmol/L "
         "(0,9-1,8 g/L) → 0 ; 10-12 mmol/L (1,8-2,2 g/L) → 3 UI SC ; 12-16,5 mmol/L "
         "(2,2-3 g/L) → 4 UI SC ; &gt; 16,5 mmol/L (&gt; 3 g/L) → 6 UI SC (ou 1 ampoule "
         "G30 % IV / 15 g sucre PO si hypoglycémie associée)."),
    ], [42 * mm, CW_FULL - 42 * mm]))
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Modalités de reprise des traitements antidiabétiques chez le DT2"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(P(
        "Conditions préalables à toute reprise : alimentation orale suffisante <b>et</b> "
        "glycémie &lt; 12 mmol/L (2,2 g/L) depuis plus de 24h — sinon, continuer et adapter "
        "le schéma Basal Bolus.", S_BODY_SM))
    story.append(Spacer(1, 1 * mm))
    story.append(grid_table(
        ["Clairance créatinine (idéalement mesurée)", "Reprise des AD non insuliniques"],
        [
            ["> 60 mL/min", "Reprise de tous les AD → retour domicile avec compte-rendu au médecin traitant"],
            ["30-60 mL/min", "Reprise des AD sauf metformine → retour domicile avec compte-rendu au médecin traitant"],
            ["< 30 mL/min", "Pas de reprise des AD → appel de l'équipe d'endocrinologie avant la sortie"],
        ],
        [50 * mm, CW_FULL - 50 * mm],
    ))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>En parallèle, arrêt du schéma Basal Bolus :</b> si le patient n'avait pas "
        "d'insuline antérieurement — continuer Basal Bolus si insuline lente ≥ 16 UI/j, "
        "l'arrêter si &lt; 16 UI/j ; si le patient avait de l'insuline antérieurement — "
        "reprise des insulines antérieures. Dans tous ces cas : retour à domicile avec "
        "compte-rendu au médecin traitant.", S_BODY_SM))
    return story

# ---------------------------------------------------------------------------
def _section_courte_duree():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Intervention de courte durée"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(P(
        "Rechercher les complications du diabète et doser l'HbA1c (différer la chirurgie "
        "si HbA1c &gt; 9 %). Stratégie définie selon le nombre de repas jeûnés — pour "
        "2 repas jeûnés ou plus, se reporter aux fiches DT1/DT2 (intervention mineure).",
        S_BODY_SM))
    story.append(Spacer(1, 1 * mm))
    story.append(grid_table(
        ["Repas jeûnés", "Horaire prévisible", "Attitude pratique"],
        [
            ["0", "Quel que soit l'horaire", "Poursuite du traitement le matin"],
            ["1", "Avant 10h", "Petit-déjeuner et traitement du matin pris après "
             "l'intervention"],
            ["1", "Entre 10h et 12h", "Pas de petit-déjeuner, traitement donné à "
             "l'arrivée. Perfusion G10 % 40 mL/h jusqu'au repas suivant si insuline ou "
             "sulfamide."],
            ["1", "Après 12h", "Poursuite du traitement le matin avec petit-déjeuner "
             "léger"],
            ["2", "—", "Cf. fiches DT1/DT2 — intervention mineure"],
        ],
        [22 * mm, 38 * mm, CW_FULL - 22 * mm - 38 * mm],
    ))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "En pré, per et post opératoire : bolus correcteur si besoin, selon l'échelle du "
        "protocole Basal Bolus (3,3-5 mmol/L → 0 ; 5-10 → 0 ; 10-12 → 3 UI SC ; 12-16,5 → "
        "4 UI SC ; &gt; 16,5 → 6 UI SC). <b>En post opératoire :</b> reprise d'une "
        "alimentation orale dès que possible ; si glycémie ≤ 10 mmol/L (1,8 g/L), reprendre "
        "les traitements habituels aux horaires habituels ; si &gt; 10 mmol/L, prolonger "
        "l'hospitalisation jusqu'à correction (5-10 mmol/L) avec bolus correcteurs ; si "
        "&gt; 16,5 mmol/L (3 g/L), contre-indication à une sortie à domicile et "
        "hospitalisation pour insulinothérapie IVSE.", S_BODY_SM))
    return story

# ---------------------------------------------------------------------------
def _section_sources():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("Sources et avertissement"))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "Groupe SFAR/SFD — G. Cheisson, D. Benhamou, E. Cosson, C. Ichai, S. Jacqueminet, "
        "B. Nicolescu-Catargi, A. Ouattara, I. Tauveron, « Prise en charge du patient "
        "diabétique en péri opératoire » — Fiches simplifiées, version 2025.", S_SOURCE))
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Avertissement :</b> cette fiche est une synthèse indépendante d'un document "
        "déjà lui-même conçu comme outil clinique simplifié — elle en reprend "
        "intégralement les algorithmes et tableaux posologiques, réorganisés en tableaux "
        "ligne-par-bande (plutôt que les diagrammes/tableaux à cellules fusionnées du "
        "PDF source) pour une lecture plus rapide sur mobile/PC, sans altérer aucune "
        "valeur numérique ni conduite à tenir. Elle ne remplace pas le texte intégral ni "
        "un outil clinique validé, et n'est ni éditée ni validée par la SFAR/SFD. "
        "<b>Vérifier toute posologie contre la source avant application.</b>",
        S_BODY_SM), bg=GREY_LIGHT, border=GREY))
    return story

# ---------------------------------------------------------------------------
SECTIONS = [
    ("Généralités DT1/DT2 & stratégie HbA1c", _section_generalites),
    ("Prise en charge pré opératoire", _section_preop),
    ("CAT hyperglycémie & hypoglycémie",
     lambda: _section_hyperglycemie() + _section_hypoglycemie()),
    ("Protocole d'insulinothérapie IVSE & relais IVSE/SC",
     lambda: _section_ivse() + _section_relais_basalbolus()),
    ("Protocole Basal Bolus SC & reprise des AD", _section_basalbolus),
    ("Intervention de courte durée & sources", lambda: _section_courte_duree() + _section_sources()),
]

def _make_doc(path=None):
    return SimpleDocTemplate(path or OUT, pagesize=A4,
                              leftMargin=MARGIN, rightMargin=MARGIN,
                              topMargin=32 * mm, bottomMargin=16 * mm,
                              title="Fiche SFAR/SFD 2025 - Diabete en peri operatoire",
                              author="Synthèse indépendante (source SFAR/SFD)")

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
