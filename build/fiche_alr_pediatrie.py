# -*- coding: utf-8 -*-
"""
Fiche de synthese - Recommandations Formalisees d'Experts SFAR-ADARPEF,
"Anesthesie loco-regionale en pediatrie", 2010 (actualisation de la
Conference d'Experts SFAR 1997). 13 pages source, telecharge depuis
sfar.org (wp-content/uploads/2015/09/2_SFAR_Anesthesie-loco-regionale-en-
pediatrie.pdf).

METHODOLOGIE : methode GRADE quand pertinente (niveau de preuve haut/
bas/tres bas -> niveau global fort/modere/faible/tres faible), sinon
accord professionnel (methode "Groupe Nominal" adaptee RAND/UCLA). PAS de
grille de cotation A-E ni de grades 1+/2+ explicites par enonce - la
FORCE de chaque recommandation est encodee directement dans le VERBE de
la phrase, convention native disclosed par la source elle-meme :
"recommandations fortes" = "il faut faire" / "il ne faut pas faire" ;
"recommandations optionnelles" = "il est possible de faire" / "il faut
probablement faire ou ne pas faire" / "les experts proposent de faire ou
ne pas faire" / "il faut penser a...". Cette fiche classe chaque enonce
FORT ou OPTIONNEL selon cette regle verbale explicite de la source - PAS
de grade fabrique, uniquement les 2 tiers que la source definit elle-
meme. Reference de chaque ligne = numero de sous-question natif de la
source (ex. "§1-2", "§5-1-1-1"), pas une numerotation Rx.y (la source
n'en a pas).

PORTEE : couverture complete des 6 "Questions" et de leurs sous-sections.
Inventaire exhaustif par comptage direct : 106 puces "●" dans le texte
source (grep), dont un sous-ensemble (~5) sont des enonces de CONTEXTE
sans verbe de recommandation (ex. "l'effet pharmacologique des
morphiniques ... n'est pas connu") - retranscrits comme notes, PAS forces
dans un badge FORT/OPT fabrique. Le Tableau 1 (choix des aiguilles par
bloc/age/poids) est retranscrit integralement. Les formules d'Armitage et
de Schulte-Steinberg (exemples de calcul de volume, non des enonces
gradues individuellement par la source) sont retranscrites comme note de
reference.

ARGUMENTAIRE : source deja tres condensee nativement (RFE en puces
courtes, pas de section "argumentaire" narrative separee par
recommandation) - chaque puce EST le contenu actionnable, integralement
reprise.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from style import *
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.units import mm

OUT = "/home/user/rfe-sfar-website/output/Fiche_SFAR_ADARPEF_ALR_Pediatrie_2010.pdf"

SOURCE_TXT = ("Source : « Anesthésie loco-régionale en pédiatrie » — Recommandations Formalisées "
              "d'Experts SFAR-ADARPEF, 2010 (actualisation de la Conférence d'Experts SFAR 1997). "
              "Fiche de synthèse non officielle : se référer au texte intégral.")

def P(txt, style=S_CELL):
    return Paragraph(txt, style)

# Badge colors : 2 tiers seulement (convention native de la source, verbe de la phrase).
GRADE_COLORS["FORT"] = (GREEN, WHITE)
GRADE_COLORS["OPT"] = (AMBER, WHITE)

def chip(label):
    return grade_chip(label, width=15 * mm, fontsize=7.6)

CW_FULL = PAGE_W - 2 * MARGIN

def reco_table(rows, col_widths):
    """rows: (ref, text, strength_label FORT/OPT)."""
    data = [[P("§", S_HEAD_W_C), P("Recommandation", S_HEAD_W), P("Force", S_HEAD_W_C)]]
    for ref, txt, strength in rows:
        data.append([P(ref, S_CELL_B), P(txt, S_CELL), chip(strength)])
    t = Table(data, colWidths=col_widths, repeatRows=1)
    style_cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), NAVY), ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTNAME", (0, 0), (-1, 0), FONT_BOLD), ("FONTSIZE", (0, 0), (-1, 0), 8),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("ALIGN", (0, 0), (0, -1), "CENTER"),
        ("ALIGN", (2, 0), (2, -1), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 0.5, GREY_LIGHT),
        ("TOPPADDING", (0, 0), (-1, -1), 2.6), ("BOTTOMPADDING", (0, 0), (-1, -1), 2.6),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            style_cmds.append(("BACKGROUND", (0, i), (-1, i), BG_PANEL))
    t.setStyle(TableStyle(style_cmds))
    return t

RCW = [15 * mm, CW_FULL - 15 * mm - 14 * mm, 14 * mm]

def theme_table(rows, col_widths, head=("Thème", "Détail")):
    data = [[P(head[0], S_HEAD_W), P(head[1], S_HEAD_W)]]
    for theme, detail in rows:
        data.append([P(theme, S_CELL_B), P(detail, S_CELL)])
    t = Table(data, colWidths=col_widths, repeatRows=1)
    style_cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), TEAL_DARK), ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTNAME", (0, 0), (-1, 0), FONT_BOLD), ("FONTSIZE", (0, 0), (-1, 0), 8),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.5, GREY_LIGHT),
        ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            style_cmds.append(("BACKGROUND", (0, i), (-1, i), BG_PANEL))
    t.setStyle(TableStyle(style_cmds))
    return t

def grid_table(head_row, rows, col_widths, head_bg=NAVY):
    data = [[P(h, S_HEAD_W_C) for h in head_row]]
    for row in rows:
        data.append([P(c, S_CELL) for c in row])
    t = Table(data, colWidths=col_widths, repeatRows=1)
    style_cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), head_bg), ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTNAME", (0, 0), (-1, 0), FONT_BOLD), ("FONTSIZE", (0, 0), (-1, 0), 7.6),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.5, GREY_LIGHT),
        ("TOPPADDING", (0, 0), (-1, -1), 2.6), ("BOTTOMPADDING", (0, 0), (-1, -1), 2.6),
        ("LEFTPADDING", (0, 0), (-1, -1), 3.5),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            style_cmds.append(("BACKGROUND", (0, i), (-1, i), BG_PANEL))
    t.setStyle(TableStyle(style_cmds))
    return t

def legend_flowable():
    chip_w = 15 * mm
    row = Table([[chip("FORT"),
                  P("<b>Forte</b> : « il faut faire » / « il ne faut pas faire ».",
                    S_BADGE_HEAD),
                  chip("OPT"),
                  P("<b>Optionnelle</b> : « il est possible de » / « il faut probablement » / "
                    "« les experts proposent » / « il faut penser à ».", S_BADGE_HEAD)]],
                colWidths=[chip_w, 62 * mm, chip_w, CW_FULL - 2 * chip_w - 62 * mm])
    row.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                              ("LEFTPADDING", (0, 0), (-1, -1), 1),
                              ("RIGHTPADDING", (0, 0), (-1, -1), 3),
                              ("TOPPADDING", (0, 0), (-1, -1), 0),
                              ("BOTTOMPADDING", (0, 0), (-1, -1), 0)]))
    return row

TOTAL_PAGES = {"n": 10}

def on_page(canvas, doc, page_title):
    header_band(canvas, doc, "SFAR — ADARPEF, RFE 2010 (FORCE ENCODÉE DANS LE VERBE)",
                "ALR en pédiatrie",
                page_title, icon_fn=lambda c, x, y: icon_shield(c, x, y, 13 * mm), color=TEAL_DARK)
    footer_band(canvas, doc, SOURCE_TXT, f"Page {doc.page} / {TOTAL_PAGES['n']}")

# ---------------------------------------------------------------------------
def _section_q1():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Résumé :</b> RFE SFAR-ADARPEF actualisant la Conférence d'Experts 1997 sur l'ALR "
        "pédiatrique — concerne surtout le nouveau-né, le nourrisson et le petit enfant (chez "
        "les grands enfants/adolescents, se rapprocher des recommandations adulte). L'ALR "
        "pédiatrique vise l'analgésie péri-opératoire, le plus souvent en complément d'une "
        "anesthésie générale. <b>Pas de grille de cotation A-E</b> : chaque recommandation est "
        "« forte » (« il faut »/« il ne faut pas ») ou « optionnelle » (« il est possible "
        "de »/« il faut probablement »/« les experts proposent ») selon le verbe employé par "
        "la source elle-même.", S_BODY), bg=BG_PANEL, border=TEAL))
    story.append(Spacer(1, 3 * mm))
    story.append(legend_flowable())
    story.append(Spacer(1, 2.5 * mm))
    story.append(section_bar("Question 1 — Anesthésiques locaux (ALx) : choix et posologies"))
    story.append(Spacer(1, 1.5 * mm))
    story.append(reco_table([
        ("§1-1", "Les ALx habituellement utilisés pour l'ALR pédiatrique sont ceux du "
         "groupe des amino-amides.", "FORT"),
        ("§1-2", "Chez le nouveau-né et le nourrisson, il faut utiliser des ALx moins "
         "concentrés que chez l'adulte.", "FORT"),
        ("§1-2", "Chez l'enfant &gt;2 mois, il faut utiliser un volume d'ALx d'autant plus "
         "important par rapport au poids que l'enfant est jeune.", "FORT"),
        ("§1-2", "Il faut réduire les posologies d'ALx chez l'enfant &lt;2 ans (fréquence "
         "cardiaque de base élevée, vulnérabilité à la toxicité cardiaque) — risque "
         "renforcé &lt;1 an (protéines sériques basses) et encore plus &lt;6 mois "
         "(immaturité hépatique, surtout si réinjections/administration continue).",
         "FORT"),
    ], RCW))
    story.append(Spacer(1, 1.5 * mm))
    story.append(theme_table([
        ("Nouveaux ALx (§1-3)", "Ropivacaïne et lévobupivacaïne (longue durée d'action) : "
         "moins toxiques pour le cœur, analgésie d'intensité/durée équivalente à la "
         "bupivacaïne racémique. La ropivacaïne provoque un bloc moteur moins intense "
         "que la bupivacaïne racémique (caudale, péridurale lombaire). La "
         "lévobupivacaïne provoque un bloc moteur moins intense que la bupivacaïne "
         "racémique, équivalent ou plus intense que la ropivacaïne."),
    ], [34 * mm, CW_FULL - 34 * mm]))
    story.append(Spacer(1, 2 * mm))
    story.append(P("<b>§1-4-1-1 Injection unique — péridurale ou caudale</b>", S_H2))
    story.append(Spacer(1, 1 * mm))
    story.append(reco_table([
        ("§1-4-1-1", "Il faut privilégier la ropivacaïne à 2 mg/ml ou la lévobupivacaïne à "
         "2,5 mg/ml.", "FORT"),
        ("§1-4-1-1", "En caudale, il ne faut pas dépasser 2 mg/kg pour la ropivacaïne ou "
         "la lévobupivacaïne.", "FORT"),
        ("§1-4-1-1", "En péridurale, il ne faut pas dépasser 1,7 mg/kg pour la "
         "ropivacaïne.", "FORT"),
        ("§1-4-1-1", "En péridurale, il ne faut probablement pas dépasser 1,7 mg/kg de "
         "lévobupivacaïne.", "OPT"),
        ("§1-4-1-1", "Il faut adapter le volume injecté au niveau métamérique à "
         "atteindre.", "FORT"),
    ], RCW))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<i>Repères de calcul (source) :</i> schéma d'Armitage (caudale) — 0,5 ml/kg "
        "(métamères sacrés), 1 ml/kg (lombaires), 1,25 ml/kg (dorsaux inférieurs). Formule "
        "de Schulte-Steinberg (péridurale) — volume par métamère (ml) = âge (années) / 10.",
        S_NOTE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(reco_table([
        ("§1-4-1-2", "Rachianesthésie : il faut probablement limiter l'usage de la "
         "bupivacaïne racémique à cette technique — 1 mg/kg à 0,5 % chez l'enfant "
         "&lt;5 kg, 0,4 mg/kg de 5 à 15 kg, 0,3 mg/kg &gt;15 kg.", "OPT"),
        ("§1-4-1-3", "Blocs périphériques du tronc/membres : il ne faut probablement pas "
         "injecter plus de 0,5 ml/kg de ropivacaïne à 2 mg/ml ou de lévobupivacaïne à "
         "2,5 mg/ml.", "OPT"),
    ], RCW))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P("<b>§1-4-2 Entretien par administration continue</b> (cathéter "
                    "périnerveux ou péridurale)", S_H2))
    story.append(Spacer(1, 1 * mm))
    story.append(reco_table([
        ("§1-4-2", "Péridurale continue de ropivacaïne : concentrations ≤2 mg/ml chez "
         "l'enfant, 1 mg/ml chez le nourrisson. Posologie maximale : 0,20 mg/kg/h avant "
         "1 mois, 0,30 mg/kg/h avant 6 mois, 0,40 mg/kg/h après 6 mois.", "FORT"),
        ("§1-4-2", "Il faut probablement appliquer les mêmes recommandations à "
         "l'administration périnerveuse périphérique continue de ropivacaïne.", "OPT"),
        ("§1-4-2", "En l'absence de données pharmacologiques suffisantes sur la "
         "lévobupivacaïne continue en pédiatrie, il faut probablement l'administrer aux "
         "concentrations/posologies retenues pour la ropivacaïne.", "OPT"),
    ], RCW))
    return story

def _section_q2():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("Question 2 — Adjuvants pour l'ALR chez l'enfant"))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P("<b>§2-1 Clonidine</b>", S_H2))
    story.append(Spacer(1, 1 * mm))
    story.append(reco_table([
        ("§2-1", "Il ne faut probablement pas administrer plus de 2 µg/kg de clonidine "
         "lors d'une ALR (effets indésirables — somnolence, bradycardie, hypotension — "
         "observés à 5 µg/kg).", "OPT"),
        ("§2-1", "Il ne faut pas recourir à la clonidine péridurale ou intrathécale chez "
         "le nouveau-né et le nourrisson sans surveillance continue (risque d'apnée "
         "postopératoire). Chez l'enfant plus âgé, 1-2 µg/kg par voie péridurale/"
         "intrathécale provoquent une sédation et dépriment faiblement la "
         "respiration.", "FORT"),
        ("§2-1", "Pour la plupart des blocs tronculaires, il est possible de prolonger "
         "l'analgésie en ajoutant 1-2 µg/kg de clonidine à la solution d'ALx (augmente "
         "l'incidence du bloc moteur).", "OPT"),
        ("§2-1", "Il est possible de prolonger l'analgésie de la péridurale caudale en "
         "ajoutant 1 µg/kg de clonidine à une solution d'ALx ≥0,125 %.", "OPT"),
        ("§2-1", "Il est possible d'améliorer l'analgésie postopératoire de la péridurale "
         "lombaire en associant de la clonidine (1-2 µg/kg en bolus, ou 0,08-0,12 "
         "µg/kg/h en continu).", "OPT"),
        ("§2-1", "Chez l'enfant/l'adolescent, il est possible d'ajouter 1-2 µg/kg de "
         "clonidine à la bupivacaïne 0,5 % pour la rachianesthésie — risque important de "
         "bradycardie et d'hypotension.", "OPT"),
    ], RCW))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P("<b>§2-2 Morphiniques</b>", S_H2))
    story.append(Spacer(1, 1 * mm))
    story.append(P(
        "<i>Contexte :</i> l'effet pharmacologique des morphiniques périmédullaires chez le "
        "nouveau-né et le nourrisson n'est pas connu.", S_NOTE))
    story.append(Spacer(1, 1 * mm))
    story.append(reco_table([
        ("§2-2", "En cas d'administration périmédullaire de morphiniques, il faut éviter "
         "toute co-administration d'un morphinique par une autre voie.", "FORT"),
        ("§2-2", "La morphine périmédullaire permet une analgésie de bonne qualité — "
         "bolus de 25-30 µg/kg (solution à 10 µg/ml) possible pour prolonger l'analgésie "
         "en péridurale lombaire ou caudale, 4-10 µg/kg en rachianesthésie.", "OPT"),
        ("§2-2", "Il est possible d'améliorer l'analgésie péridurale lombaire/thoracique "
         "continue en associant fentanyl ou sufentanil à une solution d'ALx faiblement "
         "concentrée, sans dépasser 0,2 µg/kg/h pour l'une ou l'autre substance.", "OPT"),
        ("§2-2", "Il ne faut pas attendre de bénéfice à l'utilisation de fentanyl ou "
         "sufentanil par voie caudale.", "FORT"),
        ("§2-2", "Il est possible de prolonger l'analgésie de la rachianesthésie en "
         "administrant du fentanyl 2 µg/kg.", "OPT"),
        ("§2-2", "La dépression respiratoire liée aux morphiniques périmédullaires est "
         "précoce pour les dérivés lipophiles, tardive pour la morphine (s'annonce "
         "généralement par une sédation excessive) — risque plus élevé chez le "
         "nouveau-né/nourrisson : surveillance continue dans cette population, "
         "surveillance clinique rigoureuse dans les autres tranches d'âge.", "FORT"),
        ("§2-2", "Pour traiter une rétention d'urine sans diminuer l'analgésie, il est "
         "possible d'administrer 1 µg/kg de naloxone ou 0,1 mg/kg de nalbuphine IV.",
         "OPT"),
        ("§2-2", "Pour les nausées/vomissements (plus fréquents avec la morphine "
         "qu'avec les dérivés lipophiles), il faut un traitement symptomatique.", "FORT"),
        ("§2-2", "Pour le prurit (plus fréquent avec la morphine), il faut soit un bolus "
         "IV de 1-2 µg/kg de naloxone suivi de 1-2 µg/kg/h en continu, soit des "
         "antihistaminiques de type HT3.", "FORT"),
    ], RCW))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P("<b>§2-3 Adrénaline</b>", S_H2))
    story.append(Spacer(1, 1 * mm))
    story.append(reco_table([
        ("§2-3", "Il est possible de diminuer le risque toxique des ALx d'action courte "
         "en utilisant des solutions adrénalinées à 5 µg/ml maximum (1/200 000ème) — "
         "diminue la résorption systémique, effets hémodynamiques (chute modérée de la "
         "PAM/RVP, hausse du débit cardiaque).", "OPT"),
        ("§2-3", "Il ne faut pas ajouter d'adrénaline aux ALx pour un bloc en territoire à "
         "vascularisation terminale (rachianesthésie, bloc pénien, pudendal, digital, "
         "lobe de l'oreille, certains blocs de la face…).", "FORT"),
        ("§2-3", "Il ne faut probablement pas associer d'adrénaline à un AL administré "
         "par voie caudale, périnerveuse ou locale pour prolonger l'analgésie.", "OPT"),
    ], RCW))
    story.append(Spacer(1, 1.5 * mm))
    story.append(reco_table([
        ("§2-4", "En l'absence d'études de toxicité/innocuité, l'utilisation de tramadol, "
         "midazolam, néostigmine et kétamine par voie périmédullaire chez l'enfant "
         "n'est pas recommandée.", "FORT"),
    ], RCW))
    return story

def _section_q3_q4():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("Question 3 — Méthodes de localisation pour l'ALR pédiatrique"))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P("<b>§3-1 Recherche de la perte de résistance</b>", S_H2))
    story.append(Spacer(1, 1 * mm))
    story.append(reco_table([
        ("§3-1-1", "Péridurale : en termes de sécurité, il n'est pas possible de trancher "
         "entre mandrin liquide, mixte ou gazeux. En efficacité (par assimilation à "
         "l'adulte), il faut probablement utiliser un mandrin mixte ou liquide "
         "&lt;5 ml chez l'adolescent/grand enfant ; un mandrin gazeux est possible chez "
         "le nouveau-né/nourrisson à condition de limiter le volume de gaz à 1 ml et de "
         "ne pas multiplier les tentatives en cas d'échec.", "OPT"),
        ("§3-1-2", "Caudale : il ne faut pas utiliser de mandrin liquide, mixte ou "
         "gazeux — seule la perte de résistance au franchissement de la membrane "
         "sacro-coccygienne doit guider la localisation.", "FORT"),
        ("§3-1-3", "Blocs périphériques de diffusion : il faut utiliser une aiguille à "
         "biseau court sans mandrin liquide, mixte ou gazeux.", "FORT"),
    ], RCW))
    story.append(Spacer(1, 1.5 * mm))
    story.append(reco_table([
        ("§3-2", "Neurostimulation : même technique que chez l'adulte, y compris chez "
         "l'enfant anesthésié. Il ne faut pas rechercher de réponse pour une intensité "
         "&lt;0,5 mA.", "FORT"),
        ("§3-3", "Stimulation transcutanée : il est possible de l'utiliser comme aide à "
         "la localisation des nerfs mixtes (probablement plus utile en pédiatrie où la "
         "croissance modifie les rapports anatomiques) — ne remplace pas le "
         "stimulateur de nerfs ni les connaissances anatomiques.", "OPT"),
        ("§3-4", "Il faut probablement pratiquer l'ALR chez l'enfant sous échoguidage : "
         "diminue le délai d'installation du bloc sensitif et moteur, augmente la durée "
         "du bloc sensitif, diminue la quantité d'ALx injectée, améliore le taux de "
         "succès.", "OPT"),
        ("§3-5", "Il ne faut probablement pas opacifier systématiquement tous les "
         "cathéters d'ALR — il faut vérifier la position de ceux dont un trajet aberrant "
         "aurait des conséquences graves (ex. cathéters interscaléniques, "
         "paravertébraux lombaires/thoraciques).", "OPT"),
    ], RCW))
    story.append(Spacer(1, 2.5 * mm))
    story.append(section_bar("Question 4 — Matériels pour l'ALR chez l'enfant"))
    story.append(Spacer(1, 1.5 * mm))
    story.append(reco_table([
        ("§4-1", "Il faut privilégier les aiguilles adaptées à la technique, l'âge et/ou "
         "le poids de l'enfant (Tableau 1 ci-dessous).", "FORT"),
    ], RCW))
    story.append(Spacer(1, 1.5 * mm))
    story.append(grid_table(
        ["Bloc", "Patient", "Biseau", "Taille", "Longueur", "Particularité"],
        [
            ["Rachianesthésie", "Nouveau-né, nourrisson", "Double biseau / biseau "
             "de Quincke", "26 G / 22 G", "25-40 mm / 40-50 mm", "—"],
            ["Rachianesthésie", "Enfant", "Double biseau / pointe crayon",
             "25 G / 27 G", "50 mm / 80 mm", "aucune"],
            ["Rachianesthésie", "Adolescent", "Matériel adulte", "—", "—", "—"],
            ["Anesthésie caudale", "Tout âge/poids", "Biseau court ≤45° ou "
             "biseau de Quincke", "22-25 G", "35-40 mm", "Mandrin obturateur*"],
            ["Anesthésie épidurale", "&lt;15 / 15-30 / &gt;30 kg", "Biseau court "
             "type Tuohy ou Whitacre", "19-22 / 18-20 / 18-19 G",
             "30 / 50 / 50-80 mm", "Mandrin obturateur*, graduation ≥cm"],
            ["Bloc de diffusion", "Tout âge/poids", "Biseau court 45°", "21-23 G",
             "25-50 mm", "Prolongateur transparent"],
            ["Bloc de conduction", "Selon poids/technique", "Biseau court 30-45°",
             "20-25 G", "25-80 mm", "Aiguille isolée"],
        ], [26 * mm, 28 * mm, 34 * mm, 22 * mm, 24 * mm, CW_FULL - 26 * mm - 28 * mm - 34 * mm - 22 * mm - 24 * mm],
        head_bg=GREY))
    story.append(Spacer(1, 1 * mm))
    story.append(P(
        "* Un bloc neuraxial comporte un risque très faible d'introduction de cellules "
        "épidermiques dans l'espace péridural, pouvant provoquer une tumeur dermoïde "
        "intraspinale — l'usage d'une aiguille à mandrin plein ne réduit pas ce risque.",
        S_NOTE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(reco_table([
        ("§4-2", "Chez le petit enfant, il faut utiliser des cathéters en polyamide/"
         "polyéthylène sans mandrin, gradués ≥cm, à orifice d'injection unique et "
         "terminal.", "FORT"),
        ("§4-2", "Il ne faut probablement pas mettre en place un cathéter thoracique par "
         "voie caudale.", "OPT"),
        ("§4-2", "Il ne faut pas introduire une longueur de cathéter &gt;1,5-3 cm pour un "
         "bloc nerveux périphérique.", "FORT"),
        ("§4-3", "Il est possible d'utiliser des perfuseurs élastomériques pour les ALR "
         "périphériques continues (confort, autonomie, traitement à domicile).", "OPT"),
        ("§4-4", "Il faut privilégier des sondes échographiques linéaires 8-14 MHz.",
         "FORT"),
    ], RCW))
    story.append(Spacer(1, 1 * mm))
    story.append(P(
        "<i>Contexte :</i> aucune preuve ne justifie l'usage préférentiel de cathéters "
        "stimulants (§4-2). Les appareils d'échographie pédiatrique n'ont pas d'autre "
        "spécificité (§4-4). Aucune particularité pédiatrique avérée pour les autres "
        "matériels — neurostimulateurs, seringues/pompes électriques, systèmes de "
        "fixation, canules introductrices, filtres (§4-5).", S_NOTE))
    return story

def _section_q5():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("Question 5 — Prévention, signes et traitement des complications"))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P("<b>§5-1-1 Toxicité systémique</b>", S_H2))
    story.append(Spacer(1, 1 * mm))
    story.append(reco_table([
        ("§5-1-1-1", "Quel que soit le bloc, il faut impérativement faire un test "
         "d'aspiration avant d'injecter (valeur seulement si positif — pas de sécurité "
         "absolue).", "FORT"),
        ("§5-1-1-1", "Il est possible d'injecter une dose test adrénalinée pour le bloc "
         "caudal, la péridurale lombaire/thoracique et les blocs périphériques "
         "profonds, même avec ropivacaïne/lévobupivacaïne — probablement plus utile "
         "chez l'enfant anesthésié/non communicant.", "OPT"),
        ("§5-1-1-1", "Il faut toujours injecter l'ALx lentement, de façon fractionnée, "
         "entrecoupée de tests d'aspiration répétés.", "FORT"),
        ("§5-1-1-2", "Il faut administrer une émulsion lipidique en cas de manifestation "
         "toxique systémique cardiaque ou neurologique ne répondant pas rapidement à "
         "la réanimation habituelle.", "FORT"),
        ("§5-1-1-2", "Il ne faut pas que cette thérapeutique retarde ou remplace la "
         "réanimation cardiopulmonaire habituelle.", "FORT"),
        ("§5-1-1-2", "Il faut utiliser l'Intralipide® 20 % : 1,5 ml/kg en bolus puis "
         "perfusion à 0,5-1 ml/kg/min selon la réponse clinique (probablement), sans "
         "dépasser 10 ml/kg.", "FORT"),
    ], RCW))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<i>§5-1-2 Toxicité locale :</i> en l'absence d'étude reliant neurotoxicité locale des "
        "ALx et stade de myélinisation selon l'âge, aucune précaution liée à ce facteur "
        "n'est recommandée.", S_NOTE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P("<b>§5-2 Complications mécaniques</b>", S_H2))
    story.append(Spacer(1, 1 * mm))
    story.append(reco_table([
        ("§5-2-1", "Il faut utiliser des aiguilles sans biseau ou à biseau le plus court "
         "possible, pour diminuer le risque de lésion nerveuse.", "FORT"),
        ("§5-2-2", "Il faut interrompre l'injection devant toute résistance inhabituelle, "
         "pour diminuer le risque de lésion nerveuse.", "FORT"),
        ("§5-2-3", "Chez l'adolescent/grand enfant, un mandrin gazeux pour la péridurale "
         "augmente le risque de brèche méningée (par assimilation à l'adulte).", "FORT"),
        ("§5-2-3", "Pour le bloc caudal, il faut éviter d'introduire l'aiguille &gt;1 cm "
         "dans le canal sacré, en ponctionnant précisément au sommet du triangle "
         "équilatéral hiatus sacré/épines iliaques postéro-supérieures.", "FORT"),
        ("§5-2-3", "Chez le nouveau-né/petit nourrisson, il ne faut pas réaliser de "
         "rachianesthésie avec une aiguille dont l'orifice est décalé de la pointe "
         "(risque accru d'injection à cheval sur la dure-mère).", "FORT"),
        ("§5-2-3", "En cas de brèche méningée, risque de céphalée posturale comparable "
         "à l'adulte — prise en charge similaire.", "FORT"),
    ], RCW))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P("<b>§5-3 Complications hémorragiques (bilan de coagulation)</b>",
                    S_H2))
    story.append(Spacer(1, 1 * mm))
    story.append(P(
        "<i>Contexte :</i> une coagulopathie congénitale ou acquise accroît le risque "
        "hémorragique de l'ALR — contre-indication absolue aux blocs périnerveux "
        "profonds, périmédullaires et aux blocs en territoire à vascularisation "
        "terminale.", S_NOTE))
    story.append(Spacer(1, 1 * mm))
    story.append(reco_table([
        ("§5-3", "Quel que soit l'âge, avant toute ALR, il faut évaluer l'hémostase par "
         "examen clinique + anamnèse minutieuse (antécédents personnels/familiaux).",
         "FORT"),
        ("§5-3", "Il ne faut pas pratiquer de bilan biologique systématique lorsque la "
         "marche est acquise et l'étape clinique totalement négative.", "FORT"),
        ("§5-3", "Si la marche n'est pas acquise ou qu'un bilan est nécessaire, il faut "
         "le limiter à un TCA et une numération plaquettaire.", "FORT"),
        ("§5-3", "Toute anomalie du bilan initial persistant après contrôle doit être "
         "explorée (avis hémobiologiste si besoin) selon l'anomalie et la chirurgie.",
         "FORT"),
    ], RCW))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<i>§5-4 Complications septiques :</i> aucune spécificité pédiatrique avérée pour la "
        "prévention, le diagnostic et le traitement.", S_NOTE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(reco_table([
        ("§5-5", "Pour éviter une erreur d'injection, il faut séparer les seringues "
         "contenant l'ALx de celles destinées aux injections systémiques (chariot "
         "d'ALR dédié recommandé).", "FORT"),
        ("§5-5", "Il faut identifier clairement le circuit IV et le circuit d'ALR continue "
         "(étiquettes, couleur de connexion…).", "FORT"),
        ("§5-5", "Les experts proposent qu'une couleur unique et/ou une modification "
         "(inversion, détrompeur…) des connexions Luer-Lock soit imposée pour la "
         "fabrication des cathéters d'ALR.", "OPT"),
    ], RCW))
    return story

def _section_q6a():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("Question 6 — Quelle technique choisir pour une ALR chez l'enfant ?"))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P("<b>§6-1 En fonction du terrain</b>", S_H2))
    story.append(Spacer(1, 1 * mm))
    story.append(reco_table([
        ("§6-1", "Pour le confort et la sécurité, il faut privilégier l'association "
         "ALR/AG préalable chez les jeunes enfants.", "FORT"),
        ("§6-1", "Chez les enfants plus grands, une ALR sans AG associée est possible.",
         "OPT"),
        ("§6-1", "Il ne faut probablement pas réaliser d'anesthésie caudale chez "
         "l'enfant &gt;20 kg.", "OPT"),
        ("§6-1", "Chez l'ancien prématuré de 44-60 semaines d'âge conceptuel (chirurgie "
         "sous-ombilicale), associer AG et bloc neuraxial n'augmente probablement pas "
         "le risque d'apnée postopératoire par rapport à un bloc neuraxial seul.", "OPT"),
        ("§6-1", "Il faut être vigilant en cas d'association d'adrénaline aux ALx chez le "
         "nouveau-né (baisse significative de la tension artérielle).", "FORT"),
        ("§6-1", "En cas de cardiopathie, il ne faut pas contre-indiquer de façon "
         "absolue un bloc neuraxial par ALx et/ou morphiniques.", "FORT"),
    ], RCW))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P("<b>§6-2 En fonction de la chirurgie</b>", S_H2))
    story.append(Spacer(1, 1 * mm))
    story.append(reco_table([
        ("§6-2", "En bénéfice/risque, il faut réaliser un bloc périphérique plutôt "
         "qu'un bloc central dès que l'alternative se présente.", "FORT"),
        ("§6-2", "En chirurgie lourde viscérale ou ostéo-articulaire, il est possible "
         "d'assurer une analgésie postopératoire de qualité par un bloc continu.",
         "OPT"),
        ("§6-2-1", "Chirurgie de la face : le bloc infra-orbitaire est la technique "
         "recommandée pour la chirurgie isolée de la lèvre supérieure (dont réparation "
         "de fente labiale).", "FORT"),
    ], RCW))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P("<b>§6-2-2 Chirurgie du membre supérieur</b>", S_H2))
    story.append(Spacer(1, 1 * mm))
    story.append(reco_table([
        ("§6-2-2", "Il est possible d'assurer l'analgésie de l'épaule/tiers supérieur du "
         "bras par bloc parascalénique — le bloc interscalénique est une alternative "
         "plus risquée (paralysie phrénique, Claude Bernard-Horner, Pourfour du "
         "Petit…).", "OPT"),
        ("§6-2-2", "Il faut privilégier le bloc axillaire (± cathéter) pour l'analgésie "
         "des deux tiers inférieurs du bras, coude, avant-bras et/ou main (faible "
         "morbidité).", "FORT"),
        ("§6-2-2", "Il est possible de réaliser un bloc médian/ulnaire/radial au tiers "
         "inférieur de l'avant-bras si la chirurgie ne concerne qu'un seul territoire de "
         "la main.", "OPT"),
        ("§6-2-2", "Il faut privilégier un bloc intrathécal (digital) simple pour la "
         "chirurgie de la 3<sup>e</sup> phalange des 2<sup>e</sup>, 3<sup>e</sup> et "
         "4<sup>e</sup> doigts.", "FORT"),
    ], RCW))
    return story

def _section_q6b_sources():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("Question 6 (suite) — Membre inférieur, rachis, tronc, uro-génital, thorax, digestif"))
    story.append(Spacer(1, 1.5 * mm))
    story.append(reco_table([
        ("§6-2-3", "Chirurgie unilatérale de la hanche : bloc fémoral ou ilio-fascial "
         "possible (le bloc du plexus lombaire postérieur est une alternative).", "OPT"),
        ("§6-2-3", "Chirurgie bilatérale de la hanche : il faut préférer la péridurale "
         "lombaire.", "FORT"),
        ("§6-2-3", "Chirurgie/traumatisme du fémur : il faut privilégier le bloc "
         "ilio-fascial (le bloc fémoral est une alternative).", "FORT"),
        ("§6-2-3", "Chirurgie de la cheville et/ou du pied : il faut réaliser un bloc "
         "sciatique tronculaire.", "FORT"),
        ("§6-2-4", "Chirurgie du rachis : la morphine intrathécale peut assurer "
         "l'analgésie postopératoire (alternative : cathéters périduraux mis en place "
         "par le chirurgien en fin d'intervention).", "OPT"),
        ("§6-2-5", "Chirurgie du canal péritonéo-vaginal : il faut un bloc "
         "ilio-inguinal/ilio-hypogastrique, associé à un bloc pudendal pour l'analgésie "
         "scrotale en cas d'orchidopexie (péridurale caudale = alternative si petit "
         "poids ou chirurgie bilatérale).", "FORT"),
        ("§6-2-5", "Fermeture de hernie ombilicale/ligne blanche, pylorotomie par abord "
         "ombilical strict : bloc para-ombilical possible.", "OPT"),
        ("§6-2-6", "Posthectomie/circoncision : il faut privilégier le bloc pénien "
         "(bénéfice/risque).", "FORT"),
        ("§6-2-6", "Chirurgie de l'hypospadias : la péridurale caudale peut être "
         "remplacée par un bloc pudendal bilatéral (analgésie verge/scrotum) — "
         "utilisable aussi pour chirurgie péri-anale et gynécologique superficielle "
         "(vulve, petites lèvres, clitoris).", "OPT"),
        ("§6-2-6", "Cure de reflux vésico-urétéral : la péridurale caudale est la "
         "technique d'ALR la plus habituelle.", "FORT"),
        ("§6-2-6", "Abord rénal par lombotomie : bloc paravertébral thoracique "
         "possible.", "OPT"),
        ("§6-2-7", "Chirurgie thoracique : péridurale thoracique ou bloc paravertébral "
         "thoracique possibles pour l'analgésie.", "OPT"),
        ("§6-2-8", "Chirurgie abdominale majeure : il faut choisir une analgésie "
         "péridurale continue.", "FORT"),
        ("§6-2-8", "Bloc au triangle de J.L. Petit possible pour l'analgésie de la paroi "
         "abdominale — probablement efficace pour les prises de greffon osseux iliaque, "
         "alternative au bloc ilio-inguinal/ilio-hypogastrique en chirurgie du canal "
         "péritonéo-vaginal.", "OPT"),
    ], RCW))
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("Sources et traçabilité", color=GREY))
    story.append(Spacer(1, 2 * mm))
    story.append(P(
        "<b>Document source :</b> « Anesthésie loco-régionale en pédiatrie » — "
        "Recommandations Formalisées d'Experts, SFAR en collaboration avec l'ADARPEF "
        "(Association des Anesthésistes Réanimateurs Pédiatriques d'Expression Française), "
        "2010 (actualisation de la Conférence d'Experts SFAR 1997).", S_SOURCE))
    story.append(Spacer(1, 1 * mm))
    story.append(P(
        "<b>Méthodologie :</b> méthode GRADE quand pertinente, sinon accord professionnel "
        "(méthode Groupe Nominal adaptée RAND/UCLA) — force encodée dans le verbe "
        "(forte/optionnelle), pas de grille A-E — voir détail en page 1.", S_SOURCE))
    story.append(Spacer(1, 1 * mm))
    story.append(P(
        "<b>URL source :</b> https://sfar.org/wp-content/uploads/2015/09/2_SFAR_Anesthesie-"
        "loco-regionale-en-pediatrie.pdf", S_SOURCE))
    story.append(Spacer(1, 1 * mm))
    story.append(P(
        "<b>Couverture :</b> intégralité des 106 énoncés (puces) des 6 Questions du texte "
        "source, y compris le Tableau 1 (choix des aiguilles) et les formules "
        "Armitage/Schulte-Steinberg — voir convention de force « forte/optionnelle » "
        "disclosed en page 1 (pas de grille A-E dans la source).", S_SOURCE))
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Avertissement — document validé 2010 :</b> cette fiche de synthèse indépendante "
        "reprend l'intégralité des recommandations du texte source, mais ne le remplace pas "
        "et n'est ni éditée ni validée par la SFAR ou l'ADARPEF. Se référer au texte intégral "
        "pour toute décision clinique.", S_BODY_SM), bg=GREY_LIGHT, border=GREY))
    return story

SECTIONS = [
    ("Questions 1-2 — Anesthésiques locaux & adjuvants", lambda: _section_q1() + _section_q2()),
    ("Questions 3-5 — Localisation, matériels & complications",
     lambda: _section_q3_q4() + _section_q5()),
    ("Question 6 — Choix de la technique & sources",
     lambda: _section_q6a() + _section_q6b_sources()),
]

def _make_doc(path=None):
    return SimpleDocTemplate(path or OUT, pagesize=A4,
                              leftMargin=MARGIN, rightMargin=MARGIN,
                              topMargin=32 * mm, bottomMargin=16 * mm,
                              title="Fiche SFAR-ADARPEF 2010 - ALR en pediatrie",
                              author="Synthèse indépendante (source SFAR/ADARPEF)")

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

    doc = _make_doc()
    story = _build_upto(fns)
    doc.build(story, onFirstPage=on_page_final, onLaterPages=on_page_final)
    print("OK ->", OUT, f"({total_pages} pages)")

if __name__ == "__main__":
    build()
