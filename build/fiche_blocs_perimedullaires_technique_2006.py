# -*- coding: utf-8 -*-
"""
Fiche de synthese - "Les blocs perimedullaires chez l'adulte" - Question 3
(Rachianesthesie), Question 4 (Anesthesie peridurale) et Question 5
(Association AG-Bloc perimedullaire) - Recommandations pour la Pratique
Clinique (RPC), SFAR/Sofcot/Sofmer, presentees le 24 septembre 2005 (47e
congres SFAR), publiees Ann Fr Anesth Reanim 26 (2007) 720-752.

DEUXIEME INSTALLMENT de ce document (voir `fiche_blocs_perimedullaires_ci_2006.py`
pour le premier, Questions 1-2). Perimetre volontairement limite (meme
pattern) : le document source complet contient 369 citations de grade sur
15 "Questions" au total. Cette fiche couvre INTEGRALEMENT les Questions 3
(modalites de realisation de la rachianesthesie), 4 (modalites de
realisation de l'anesthesie peridurale) et 5 (association blocs
perimedullaires-anesthesie generale : chronologie, surveillance
peroperatoire) - le "groupe technique" du document. Les Questions 6 a 15
(travail obstetrical, cesarienne, analgesie postoperatoire, terrains
cardiovasculaire/respiratoire/hemostase/neurologique/infectieux
specifiques, gestion de l'echec, facteurs de risque de complications)
NE SONT PAS couvertes ici - installments futurs.

COLLISION A VERIFIER AU PROCHAIN INSTALLMENT (pas cette fiche) : la
Question 6 (travail obstetrical) de ce document pourrait recouper le
perimetre de `douleur_accouchement_2025` (HAS 2025, deja git-tracke) -
a verifier explicitement avant de construire cet installment.

METHODOLOGIE : grille EBM classique A/B/C (identique au premier
installment) + une nouvelle variante terminologique rencontree dans les
Questions 3-5 : « consensus professionnel » (Question 5, une occurrence),
distincte des formulations deja rencontrees dans les Questions 1-2
(« accord professionnel », « avis d'experts ») mais de sens strictement
equivalent (absence d'etudes, plus faible niveau de preuve de la grille) -
chip local "AE" reutilise, disclosed comme troisieme variante
terminologique du meme palier, pas un palier distinct.

DECOMPTE - methodologie de consolidation (disclosed explicitement) :
un grep exhaustif sur le texte source des Questions 3-5 (lignes 712-1091
du fichier texte extrait) trouve 31 citations de grade individuelles :
grade A x17, grade B x5, grade C x8, "consensus professionnel" x1.
Plusieurs de ces citations, lorsqu'elles portent le MEME grade et
decrivent la MEME recommandation/le meme theme clinique au sein d'un seul
paragraphe source (ex. "l'extension du bloc depend de nombreux facteurs
(grade A) ... (grade A) ... (grade A)"), sont regroupees en une seule
ligne de tableau plutot que dupliquees - jamais deux citations de grades
DIFFERENTS ne sont fusionnees dans une seule ligne/puce (regle anti-
grade-composite respectee, verifie par regex apres redaction : zero
occurrence de grades merges "X/Y" trouvee). Apres consolidation : 24
lignes de recommandations gradees (A:11, B:4, C:8, AE:1), verifie par
regex sur le script final - Question 3 (rachianesthesie) 11 lignes
(A:6, B:3, C:2), Question 4 (peridurale) 7 lignes (A:5, B:1, C:1),
Question 5 (AG-bloc) 6 lignes (C:5, AE:1). Les trois tableaux
pharmacologiques du texte source (Tableau 2 - facteurs determinant le
bloc en rachianesthesie ; Tableau 3 - pharmacodynamie comparee des AL en
rachianesthesie ; Tableau 4 - pharmacodynamie comparee des AL en
peridurale) sont reproduits verbatim, y compris leurs cellules vides
(ex. "Position du patient" et "Age" n'ont pas de valeur de "Duree" dans
le Tableau 2 source, "Levobupivacaine" n'a pas de valeur de "Duree du
bloc moteur" dans le Tableau 4 source - verifie par rendu visuel du PDF
source a 200dpi, pages 726-728, pas suppose) - verifie par rendu visuel
du PDF source a 200dpi (pages 726-728) avant redaction, pas simplement a
partir du texte extrait (risque connu de ce corpus : desordre de colonnes
a l'extraction PyMuPDF sur des tableaux multi-colonnes - non constate ici
apres verification, l'extraction texte s'est averee fidele a l'ordre
visuel).
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from style import *
GRADE_COLORS["A"] = (GREEN, WHITE)
GRADE_COLORS["B"] = (TEAL, WHITE)
GRADE_COLORS["C"] = (AMBER, WHITE)
GRADE_COLORS["AE"] = (GREY, WHITE)
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.units import mm

OUT = "/home/user/rfe-sfar-website/output/Fiche_Blocs_Perimedullaires_Technique_2006.pdf"

SOURCE_TXT = ("Source : SFAR/Sofcot/Sofmer, « Les blocs périmédullaires chez l'adulte », "
              "RPC, Ann Fr Anesth Réanim 26 (2007) 720-752 — Questions 3-5 uniquement. "
              "Fiche de synthèse non officielle : se référer au texte intégral.")

def P(txt, style=S_CELL):
    return Paragraph(txt, style)

def chip(label, **kw):
    return grade_chip(label, **kw)

CW_FULL = PAGE_W - 2 * MARGIN

def reco_table(rows, col_widths):
    """rows: (ref, text, grade_label)."""
    data = [[P("Catégorie", S_HEAD_W), P("Recommandation", S_HEAD_W), P("Grade", S_HEAD_W_C)]]
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

RCW = [30 * mm, CW_FULL - 30 * mm - 15 * mm, 15 * mm]

def context_note_local(txt):
    return P(f"<i>Précision du source :</i> {txt}", S_NOTE)

def practical_block(title, bullets):
    story = [P(f"<b>{title}</b>", S_BODY_SM)]
    for b in bullets:
        story.append(P(f"• {b}", S_BODY_SM))
    return story

def data_table(headers, rows, col_widths):
    data = [[P(h, S_HEAD_W_C) for h in headers]]
    for r in rows:
        data.append([P(c, S_CELL) for c in r])
    t = Table(data, colWidths=col_widths, repeatRows=1)
    style_cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), GREY), ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTNAME", (0, 0), (-1, 0), FONT_BOLD), ("FONTSIZE", (0, 0), (-1, 0), 7.4),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 0.5, GREY_LIGHT),
        ("TOPPADDING", (0, 0), (-1, -1), 2.4), ("BOTTOMPADDING", (0, 0), (-1, -1), 2.4),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            style_cmds.append(("BACKGROUND", (0, i), (-1, i), BG_PANEL))
    t.setStyle(TableStyle(style_cmds))
    return t

def legend_flowable():
    chip_w = 16 * mm
    content_w = CW_FULL
    row = Table([[chip("A", width=chip_w - 2 * mm), chip("B", width=chip_w - 2 * mm),
                  chip("C", width=chip_w - 2 * mm), chip("AE", width=chip_w - 2 * mm),
                  P("<b>Grille EBM classique</b> — <b>A</b> : essais randomisés de forte "
                    "puissance/méta-analyses ; <b>B</b> : essais randomisés de faible "
                    "puissance/études de cohorte ; <b>C</b> : cas-témoins/études "
                    "rétrospectives ; <b>AE</b> : accord professionnel (absence d'études) — "
                    "regroupe aussi « consensus professionnel » (Question 5), même tiers. "
                    "Fiche limitée aux Questions 3-5/15 du document (rachianesthésie, "
                    "péridurale, association AG-bloc).", S_BADGE_HEAD)]],
                colWidths=[chip_w] * 4 + [content_w - 4 * chip_w])
    row.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                              ("LEFTPADDING", (0, 0), (-1, -1), 1),
                              ("RIGHTPADDING", (0, 0), (-1, -1), 1),
                              ("TOPPADDING", (0, 0), (-1, -1), 0),
                              ("BOTTOMPADDING", (0, 0), (-1, -1), 0)]))
    return row

TOTAL_PAGES = {"n": 6}

def on_page(canvas, doc, page_title):
    header_band(canvas, doc, "SFAR/SOFCOT/SOFMER — RPC 2007 (Q3-5/15 — PÉRIMÈTRE LIMITÉ)",
                "Les blocs périmédullaires chez l'adulte",
                page_title, icon_fn=lambda c, x, y: icon_shield(c, x, y, 13 * mm), color=TEAL_DARK)
    footer_band(canvas, doc, SOURCE_TXT, f"Page {doc.page} / {TOTAL_PAGES['n']}")

# ---------------------------------------------------------------------------
def _section_rachianesthesie():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Périmètre limité — installment 2/n :</b> ce document source compte 15 « Questions » "
        "cliniques et 369 citations de grade au total. Cette fiche couvre INTÉGRALEMENT les "
        "Questions 3, 4 et 5 (modalités techniques de la rachianesthésie et de la péridurale, "
        "association avec l'anesthésie générale). Les Questions 1-2 (information, "
        "contre-indications générales) sont couvertes par une fiche séparée. Les Questions 6 à "
        "15 (travail obstétrical, césarienne, analgésie postopératoire, terrains spécifiques, "
        "échec, facteurs de risque) ne sont PAS couvertes ici — installments futurs.", S_BODY),
        bg=AMBER_LIGHT, border=AMBER))
    story.append(Spacer(1, 2.5 * mm))
    story.append(legend_flowable())
    story.append(Spacer(1, 3 * mm))
    story.append(KeepTogether([
        section_bar("Question 3 — Modalités de réalisation de la rachianesthésie"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(P(
        "<b>Repères non gradés :</b> la réalisation pratique ne se conçoit que dans un site "
        "d'anesthésie équipé, chez un patient perfusé et oxygéné, avec asepsie « chirurgicale » "
        "(lavage des mains, désinfection cutanée, calot, gants, masque). Plusieurs techniques de "
        "ponction sont possibles (assise ou décubitus latéral ; médiane, paramédiane ou méthode "
        "de Taylor) — un repérage échographique peut faciliter le geste.", S_BODY_SM))
    story.append(Spacer(1, 1.5 * mm))
    story.append(data_table(
        ["Facteur", "Extension", "Durée"],
        [
            ["Dose", "++++", "++++"],
            ["Volume et concentration", "±", "–"],
            ["Densité", "++", "+"],
            ["Niveau de ponction (sol. hyperbare)", "+", "–"],
            ["Vitesse d'injection", "+", "–"],
            ["Pression abdominale (grossesse–obésité)", "+", "–"],
            ["Position du patient (sol. hyperbare)", "++", ""],
            ["Volume du LCR", "+++", "+"],
            ["Âge", "++", ""],
            ["Orientation de l'orifice de l'aiguille", "+", "+"],
        ], [CW_FULL - 40 * mm, 20 * mm, 20 * mm]))
    story.append(Spacer(1, 1 * mm))
    story.append(P("<i>Tableau 2 — Principaux facteurs déterminant les caractéristiques du "
                    "bloc en rachianesthésie (cellules vides = non renseigné par le source).</i>", S_NOTE))
    story.append(Spacer(1, 2 * mm))
    story.append(reco_table([
        ("Ponction", "Réaliser la ponction lombaire chez un patient conscient, dans l'espace "
         "interépineux le plus bas situé parmi ceux identifiés en dessous de la ligne de "
         "Tuffier.", "C"),
        ("Matériel", "Privilégier une aiguille 26-27G à pointe conique (Sprotte ou Whitacre) — "
         "le choix entre elles peut être guidé par le coût (performances comparables). Pas "
         "d'avantage à utiliser une aiguille plus fine que 27G (risque de ponctions multiples, "
         "maniement plus difficile) ; ne pas dépasser 24G (risque de céphalées).", "B"),
        ("Technique", "La progression de l'aiguille doit être lente, pour percevoir les "
         "structures anatomiques traversées et interrompre la progression dès que le passage "
         "de la dure-mère est perçu.", "C"),
        ("AL autorisés", "La ropivacaïne, la bupivacaïne et la lévobupivacaïne sont les seuls "
         "anesthésiques locaux à bénéficier de l'AMM pour l'injection intrathécale.", "A"),
        ("AL contre-indiqués", "La lidocaïne 5 % n'a plus l'AMM par voie intrathécale (risque de "
         "syndrome d'irritation radiculaire transitoire et de syndrome de la queue-de-cheval) ; "
         "les formes moins concentrées sont également contre-indiquées.", "A"),
    ], RCW))
    story.append(Spacer(1, 2 * mm))
    story.append(data_table(
        ["Molécule", "Niveau supérieur (à la piqûre)", "Durée bloc moteur (min)",
         "Durée bloc sensitif : régression 2 dermatomes (min)", "Levée complète bloc sensitif S2 (min)"],
        [
            ["Bupivacaïne 4 mg", "T8 (T6–T12)", "NA", "21 ± 4", "115 ± 42"],
            ["Bupivacaïne 8 mg", "T5 (T4–T10)", "49 ± 44", "60 ± 15", "198 ± 33"],
            ["Bupivacaïne 12 mg", "T5 (T3–T10)", "70 ± 37", "65 ± 32", "220 ± 63"],
            ["Bupivacaïne 15 mg", "T4 (T3–T11)", "180 (120–210)", "80 ± 40", "255 (150–420)"],
            ["Lévobupivacaïne 4 mg", "T10 (T7–T12)", "NA", "24 ± 7", "102 ± 52"],
            ["Lévobupivacaïne 8 mg", "T5 (T3–T7)", "39 ± 23", "50 ± 12", "175 ± 46"],
            ["Lévobupivacaïne 12 mg", "T5 (T3–T7)", "55 ± 35", "60 ± 30", "165 ± 59"],
            ["Lévobupivacaïne 15 mg", "T4 (T3–T8)", "180 (100–210)", "80 ± 40", "200 ± 70"],
            ["Ropivacaïne 4 mg", "T8 (T4–L1)", "NA", "40 ± 30", "81 ± 44"],
            ["Ropivacaïne 8 mg", "T8 (T3–L1)", "NA", "75 ± 21", "130 ± 27"],
            ["Ropivacaïne 12 mg", "T8 (T4–L2)", "60", "85 ± 18", "150 ± 44"],
            ["Ropivacaïne 14 mg", "T6 (T11–C7)", "90 (45–150)", "95 ± 32", "175 ± 42"],
            ["Ropivacaïne 20 mg", "T3 (T11–C2)", "120 (23–150)", "95 ± 32", "200 (180–345)"],
        ], [30 * mm, 24 * mm, 24 * mm, CW_FULL - 30 * mm - 24 * mm - 24 * mm - 32 * mm, 32 * mm]))
    story.append(Spacer(1, 1 * mm))
    story.append(P("<i>Tableau 3 — Pharmacodynamie comparée des AL en solution isobare en "
                    "rachianesthésie, ponction en L4-L5 (à titre indicatif).</i>", S_NOTE))
    story.append(Spacer(1, 2 * mm))
    story.append(reco_table([
        ("Extension du bloc", "L'extension du bloc anesthésique est peu prévisible : elle "
         "dépend de nombreux facteurs (patient, technique d'injection, caractéristiques du LCR "
         "et de la solution) ; en pratique, elle dépend essentiellement de la dose d'AL et du "
         "volume du LCR (non estimable en clinique).", "A"),
        ("Extension du bloc", "Le volume et la concentration de la solution modifient peu "
         "l'étendue du bloc.", "B"),
        ("Solutions hyperbares", "Avec les solutions hyperbares, l'extension du bloc dépend de "
         "la position du patient et sa régression est plus rapide ; le niveau de blocage "
         "sensitivomoteur est plus reproductible qu'avec les solutions normobares.", "A"),
        ("Solutions hyperbares", "La quantité de glucose ajoutée pour rendre les solutions "
         "hyperbares est généralement trop importante.", "B"),
        ("Dose/facteurs", "Pour un même niveau d'extension, réduire la dose avec l'âge et en "
         "cas de pression intra-abdominale élevée (grossesse, obésité, ascite). La vitesse "
         "d'installation, l'intensité et la durée du bloc dépendent de la dose totale "
         "administrée (rapport volume/concentration).", "A"),
        ("Limitation du bloc", "La limitation unilatérale ou caudale du bloc est favorisée par "
         "l'injection de faibles doses, l'injection lente, et le maintien en position latérale "
         "ou assise ; une extension secondaire retardée reste possible lors de la mobilisation.", "A"),
    ], RCW))
    story.append(Spacer(1, 1.5 * mm))
    story.extend(practical_block("Repères pratiques non gradés :", [
        "Évaluation du bloc : discrimination chaud-froid pour le niveau sensitif, score de "
        "Bromage (ou modifié) pour le bloc moteur ; connaissance du niveau métamérique requis "
        "selon l'acte chirurgical impérative.",
        "Adjuvants morphiniques : ne modifient pas la pharmacocinétique des AL. Sufentanil "
        "(2,5-5 µg) : +25-50 % de durée d'analgésie. Morphine (≤ 0,3 mg) : analgésie prolongée "
        "6-24h.",
        "Indications préférentielles : terrain (estomac plein, intubation difficile prévue, "
        "insuffisance respiratoire, artériopathie des membres inférieurs) et type "
        "d'intervention (urogénitale, abdominale basse, orthopédique, traumatologique et "
        "vasculaire des membres inférieurs, obstétricale).",
        "Rachianesthésie continue : meilleure stabilité hémodynamique (titration) et "
        "prolongation du bloc par réinjections itératives ; précautions requises (syndrome de "
        "la queue-de-cheval, irritation radiculaire transitoire, méningite infectieuse).",
        "Rachianesthésie unilatérale : réduit l'hypotension et la rétention vésicale en "
        "limitant le bloc sympathique ; adaptée au sujet âgé et à la chirurgie ambulatoire.",
    ]))
    return story

# ---------------------------------------------------------------------------
def _section_peridurale():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Question 4 — Modalités de réalisation de l'anesthésie péridurale"),
        Spacer(1, 1.5 * mm),
    ]))
    story.extend(practical_block("Repères pratiques non gradés :", [
        "Repérage de l'espace péridural lombaire : mandrin liquidien recommandé ; l'utilisation "
        "du mandrin gazeux ne peut être recommandée.",
        "Dose-test (AL + 15 µg d'adrénaline) : recommandée en dehors du travail obstétrical — sa "
        "négativité ne garantit pas l'absence de risque d'injection erratique. L'injection de "
        "la dose anesthésique doit être lente et fractionnée.",
        "AMM péridurale : lidocaïne, ropivacaïne, bupivacaïne, lévobupivacaïne et mépivacaïne.",
    ]))
    story.append(Spacer(1, 1.5 * mm))
    story.append(reco_table([
        ("Hygiène", "Réaliser l'anesthésie péridurale sous mesures d'hygiène strictes : "
         "désinfection cutanée, lavage des mains, port de calot/gants/masque facial, habillage "
         "chirurgical de l'opérateur en cas de pose de cathéter, calot et masque facial pour "
         "tout le personnel de la salle.", "C"),
    ], RCW))
    story.append(Spacer(1, 2 * mm))
    story.append(data_table(
        ["", "Concentration (%)", "Doses maximales (mg)", "Délai d'installation (bloc 4 seg.) [min]",
         "Durée bloc moteur (min)", "Régression 2 seg. ± 2 DS (min)"],
        [
            ["Lidocaïne", "1–2", "400 (6–10 mg/kg)", "5–15", "60", "100 ± 80"],
            ["Mépivacaïne", "1–2", "400 (6–10 mg/kg)", "6–17", "60", "115 ± 15"],
            ["Bupivacaïne", "0,5", "150 (2–3 mg/kg)", "5–17", "180", "150 ± 200"],
            ["Lévobupivacaïne", "0,5", "150 (2–3 mg/kg)", "10–20", "150–200", ""],
            ["Ropivacaïne", "0,5 / 0,75 / 1", "225–300 (3–4 mg/kg)", "10–20", "138 / 180 / 300",
             "168 ± 60 / 180 ± 30 / 180 ± 30"],
        ], [32 * mm, 20 * mm, 30 * mm, 28 * mm, 22 * mm, CW_FULL - 32 * mm - 20 * mm - 30 * mm - 28 * mm - 22 * mm]))
    story.append(Spacer(1, 1 * mm))
    story.append(P("<i>Tableau 4 — Pharmacodynamie comparée des AL en anesthésie péridurale "
                    "(cellule vide = non renseignée par le source ; les 3 lignes de ropivacaïne "
                    "sont condensées ici par concentration croissante, ordre identique au "
                    "source).</i>", S_NOTE))
    story.append(Spacer(1, 2 * mm))
    story.append(reco_table([
        ("Pharmacodynamie", "Le délai d'installation, la durée d'action et l'intensité du bloc "
         "dépendent de la dose administrée ; le niveau d'extension et la vitesse de régression "
         "du bloc sensitif et moteur en dépendent également.", "A"),
        ("Pharmacodynamie", "La vitesse d'injection influence le niveau supérieur du bloc.", "B"),
        ("Bloc différentiel", "Le bloc différentiel (sensitivomoteur) est d'autant plus marqué "
         "que les concentrations utilisées sont faibles : lidocaïne ≤ 1 %, ropivacaïne ≤ 0,2 %, "
         "bupivacaïne ≤ 0,25 %.", "A"),
        ("Choix de l'AL", "Lidocaïne et mépivacaïne : délai d'action rapide, durée limitée. "
         "Ropivacaïne, bupivacaïne et lévobupivacaïne : délai d'action long, durée prolongée ; "
         "à dose équivalente, bupivacaïne et lévobupivacaïne sont pharmacodynamiquement "
         "équivalentes (rapport de puissance ropivacaïne : bupivacaïne/lévobupivacaïne ≈ 3:2).", "A"),
        ("Facteurs", "L'âge augmente l'extension et réduit la durée du bloc.", "A"),
        ("Facteurs", "Au cours de la grossesse, l'espace péridural est réduit, ce qui accentue "
         "l'extension du bloc pour un volume d'AL donné.", "A"),
    ], RCW))
    story.append(Spacer(1, 1.5 * mm))
    story.extend(practical_block("Repères pratiques non gradés :", [
        "Réinjections péridurales : tenir compte de la dose initiale et de la demi-vie "
        "d'élimination de l'AL, pour limiter le risque d'intoxication.",
        "Étage thoracique : espace péridural réduit, faible densité de graisse — de faibles "
        "doses (4-5 ml) entraînent une extension de plus de 4-5 dermatomes par comparaison à "
        "l'étage lombaire.",
    ]))
    return story

# ---------------------------------------------------------------------------
def _section_ag_bloc_sources():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Question 5 — AG et bloc périmédullaire : chronologie & surveillance"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(context_note_local(
        "l'analyse de la littérature ne permet pas de conclure sur l'existence d'une relation "
        "entre le moment de réalisation d'une anesthésie périmédullaire par rapport à "
        "l'induction d'une anesthésie générale et le risque de survenue d'une complication "
        "neurologique."))
    story.append(Spacer(1, 1.5 * mm))
    story.append(reco_table([
        ("Monitorage", "Un monitorage par électrocardioscope, pression artérielle non invasive "
         "et oxymètre de pouls est obligatoire ; le matériel d'intubation et un plateau "
         "d'agents injectables (induction d'une AG et/ou maintien de la pression artérielle) "
         "doivent être prêts et immédiatement disponibles dès le début de la procédure et "
         "pendant toute la durée du bloc anesthésique.", "AE"),
        ("Chronologie", "L'APD doit être réalisée chez un sujet éveillé, éventuellement sous "
         "sédation légère ; chez l'adulte, la réalisation sous AG doit rester exceptionnelle, "
         "d'autant plus qu'elle est pratiquée à un niveau métamérique supérieur à L3 (risque de "
         "lésion médullaire).", "C"),
        ("Surveillance", "L'administration d'oxygène est recommandée lors de la réalisation de "
         "l'anesthésie péridurale.", "C"),
        ("Surveillance", "Le risque d'arrêt cardiocirculatoire persiste pendant toute la durée "
         "du bloc sympathique ; une bradycardie doit être considérée comme un signe d'alerte "
         "pouvant précéder un arrêt cardiocirculatoire.", "C"),
        ("Surveillance", "L'association peropératoire d'une APD et d'une AG peut être "
         "responsable d'une hypotension artérielle sévère.", "C"),
        ("Facteurs de risque", "Le risque de complication neurologique médullaire est favorisé "
         "en cas d'artériopathie sévère préexistante, d'hyperlordose ou de canal lombaire "
         "étroit.", "C"),
    ], RCW))
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("Sources et avertissement", color=GREY))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>Document source :</b> SFAR/Sofcot/Sofmer, « Les blocs périmédullaires chez "
        "l'adulte », Recommandations pour la Pratique Clinique, présentées le 24 septembre "
        "2005 (47e congrès SFAR), Annales Françaises d'Anesthésie et de Réanimation 26 "
        "(2007) 720-752.", S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>URL source :</b> https://sfar.org/les-blocs-perimedullaires-chez-ladulte/", S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>Couverture :</b> Questions 3-5/15 uniquement (rachianesthésie, péridurale, "
        "association AG-bloc) — 24 recommandations gradées (A:11, B:4, C:8, AE:1). Les "
        "Questions 1-2 sont couvertes par une fiche séparée. Les Questions 6 à 15 (travail "
        "obstétrical, césarienne, analgésie postopératoire, terrains spécifiques, échec, "
        "facteurs de risque de complications) ne sont pas couvertes ici — hors périmètre de "
        "cette fiche, installments futurs. Argumentaire scientifique détaillé (document source "
        "complet) non reproduit.", S_SOURCE))
    story.append(Spacer(1, 2 * mm))
    story.append(info_panel(P(
        "<b>Avertissement :</b> cette fiche est une synthèse indépendante et PARTIELLE "
        "(Questions 3-5 uniquement, sur 15). Elle ne remplace pas le texte intégral — en "
        "particulier pour toute question d'obstétrique ou de terrain spécifique. Cette fiche "
        "n'est ni éditée ni validée par la SFAR.", S_BODY_SM),
        bg=GREY_LIGHT, border=GREY))
    return story

# ---------------------------------------------------------------------------
SECTIONS = [
    ("Question 3 — Rachianesthésie", _section_rachianesthesie),
    ("Question 4 — Anesthésie péridurale", _section_peridurale),
    ("Question 5 — Association AG-Bloc & sources", _section_ag_bloc_sources),
]

def _make_doc(path=None):
    return SimpleDocTemplate(path or OUT, pagesize=A4,
                              leftMargin=MARGIN, rightMargin=MARGIN,
                              topMargin=32 * mm, bottomMargin=16 * mm,
                              title="Fiche SFAR 2007 - Blocs perimedullaires (Q3-5 - Technique)",
                              author="Synthèse indépendante (source SFAR/Sofcot/Sofmer)")

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
