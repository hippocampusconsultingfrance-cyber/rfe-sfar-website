# -*- coding: utf-8 -*-
"""
Fiche de synthese - "Prise en charge de la douleur de l'accouchement :
analgesie perimedullaire et alternatives medicamenteuses" - Recommandation
de bonne pratique (RBP), HAS, validee par le College le 30 avril 2025.
Promoteurs : SFAR et Collège d'Anesthesie et Reanimation en Obstetrique
(CARO), en association avec CNGOF/SF2H/CNSF/CIANE/GIHP/SFTH et d'autres.
38 pages, telecharge depuis sfar.org (wpdmdl=106110, "texte court").

METHODOLOGIE : meme convention que fiche_resection_hepatique_2025.py
(meme source HAS) - grade "1"/"2" SANS signe +/-, "Avis d'experts (AE)"
et "Pas de recommandation / Absence de recommandation (ABS)" imprimes
explicitement distincts l'un de l'autre des la page de legende du
source. Chips locaux G1/G2/AE/ABS reutilises tels quels.

DECOMPTE : ce document, contrairement a fiche_resection_hepatique_2025.py,
N'IMPRIME PAS de synthese chiffree globale ("XX recommandations" /
sous-totaux par grade) - aucune verification croisee resume-vs-decompte
n'est donc possible ici (rien a comparer). Decompte direct exhaustif,
chaque marqueur "R x.y[.z]" et chaque bloc "ABS" (imprime en encadrement
avant ET apres le texte de la recommandation - motif verifie sur chaque
occurrence pour ne pas compter en double) apparie individuellement a son
grade : 34 items numerotes (12 GRADE1 + 10 GRADE2 + 12 avis d'experts) +
5 "Pas de recommandation" (dont 2 sans numero R du tout, comme le
"port de la casaque sterile" et le "monitorage systematique pendant la
pose" - questions posees dans le texte mais n'ayant recu aucune
proposition, meme non numerotee) = 39 items sur 5 champs. Chaque paire
marqueur/grade a ete relue individuellement sur le texte source complet,
pas seulement via une regex automatique.

PERIMETRE : integral sur les 5 champs (pose de l'APM, initiation de
l'APM, entretien de l'APM, gestion de l'insuffisance/echec de l'APM,
alternatives medicamenteuses a l'APM) et les 39 items (34 recommandations
+ 5 absences). La Figure 4 (algorithme de synthese de la gestion de
l'analgesie perimedullaire, d'apres Rackelboom - directement liee aux
R4.2.4.1-4.2.4.4 de gestion de l'insuffisance/echec) est retranscrite en
tableau condense depuis un rendu visuel a 180dpi (infographie sans
couche texte exploitable pour le detail des blocs). Les Figures 1 et 2
(schemas techniques APD/PRC/PPD et modes d'administration BIP+PCEA vs
debit continu+PCEA) sont purement illustratives de terminologie deja
explicitee dans le texte des recommandations elles-memes (R2.1, R3.1) -
non retranscrites en detail, mais les definitions operationnelles du
source (APM precoce, insuffisance vs echec, deambulation) sont reprises
dans un encadre court car elles conditionnent la lecture exacte de
plusieurs recommandations. Bibliographie et composition nominative des
groupes de travail non reproduites. Argumentaire minimal (regle de
projet 2026-09-14) : le texte source est deja tres concis (format HAS
RBP), aucun bloc "Argumentaire" distinct a trimmer.
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

OUT = "/home/user/rfe-sfar-website/output/Fiche_HAS_SFAR_CARO_Douleur_Accouchement_2025.pdf"

SOURCE_TXT = ("Source : HAS/SFAR/CARO, « Prise en charge de la douleur de l'accouchement : "
              "analgésie périmédullaire et alternatives médicamenteuses », RBP, avril 2025. "
              "Fiche de synthèse non officielle : se référer au texte intégral.")

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

TCW = [42 * mm, CW_FULL - 42 * mm]

def absence_note(question_txt):
    return info_panel(P(
        f"<b>ABS — Pas de recommandation</b> (absence de données) : {question_txt}",
        S_BODY_SM), bg=GREY_LIGHT, border=GREY)

def legend_flowable():
    chip_w = 14 * mm
    content_w = CW_FULL
    row = Table([[chip("G1", width=chip_w - 2 * mm), chip("G2", width=chip_w - 2 * mm),
                  chip("AE", width=chip_w - 2 * mm), chip("ABS", width=chip_w - 2 * mm),
                  P("<b>G1/G2 = grade 1/grade 2</b> (le source imprime ces niveaux SANS "
                    "signe +/- ; sens repris du verbe de la phrase). <b>AE</b> = avis "
                    "d'experts. <b>ABS</b> = pas de recommandation (données "
                    "insuffisantes, aucune proposition faite). 39 items au total (34 "
                    "recommandations + 5 absences) sur 5 champs — ce document n'imprime "
                    "pas de synthèse chiffrée globale à recouper (contrairement à "
                    "fiche_resection_hepatique_2025.py) : décompte direct exhaustif "
                    "uniquement.", S_BADGE_HEAD)]],
                colWidths=[chip_w] * 4 + [content_w - 4 * chip_w])
    row.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                              ("LEFTPADDING", (0, 0), (-1, -1), 1),
                              ("RIGHTPADDING", (0, 0), (-1, -1), 1),
                              ("TOPPADDING", (0, 0), (-1, -1), 0),
                              ("BOTTOMPADDING", (0, 0), (-1, -1), 0)]))
    return row

TOTAL_PAGES = {"n": 7}

def on_page(canvas, doc, page_title):
    header_band(canvas, doc, "HAS / SFAR / CARO — RBP, AVRIL 2025",
                "Douleur de l'accouchement — Analgésie périmédullaire",
                page_title, icon_fn=lambda c, x, y: icon_drop(c, x, y, 13 * mm), color=TEAL_DARK)
    footer_band(canvas, doc, SOURCE_TXT, f"Page {doc.page} / {TOTAL_PAGES['n']}")

# ---------------------------------------------------------------------------
def _section_intro_champ1():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Résumé :</b> RBP HAS (avril 2025), promue par la SFAR et le CARO — "
        "actualisation des recommandations SFAR 2006 sur l'analgésie obstétricale. "
        "5 champs — pose, initiation, entretien, gestion de l'insuffisance/échec de "
        "l'analgésie périmédullaire (APM), alternatives médicamenteuses — 34 "
        "recommandations et 5 absences de recommandation (39 items).", S_BODY),
        bg=BG_PANEL, border=TEAL_DARK))
    story.append(Spacer(1, 2.5 * mm))
    story.append(legend_flowable())
    story.append(Spacer(1, 2.5 * mm))
    story.append(P(
        "<b>Définitions retenues :</b> APM <b>précoce</b> = pose à dilatation cervicale "
        "≤ 4 cm. <b>Insuffisance</b> d'analgésie = analgésie peu ou partiellement "
        "efficace ; <b>échec</b> = absence totale d'efficacité. <b>Déambulation</b> = "
        "possibilité de marcher et/ou se verticaliser sous APM, au 1<super>er</super> stade, au "
        "2<super>e</super> stade, ou aux deux.", S_BODY_SM))
    story.append(Spacer(1, 3 * mm))
    story.append(KeepTogether([
        section_bar("Champ 1 — Pose de l'analgésie périmédullaire (APM)"),
        Spacer(1, 1 * mm),
        P("<b>Repérage échographique</b>", S_CELL_B),
        Spacer(1, 1 * mm),
    ]))
    story.append(reco_table([
        ("R1.1.1", "Ne pas utiliser le repérage échographique de l'espace périmédullaire "
         "de manière systématique dans le but de réduire la morbidité maternelle.",
         "G2"),
        ("R1.1.2", "Utiliser le repérage échographique de l'espace périmédullaire pour "
         "les patientes obèses et les rachis difficiles, pour faciliter la pose de "
         "l'APM.", "G1"),
    ], RCW))
    story.append(Spacer(1, 2 * mm))
    story.append(P("<b>Position à adopter</b>", S_CELL_B))
    story.append(Spacer(1, 1 * mm))
    story.append(reco_table([
        ("R1.2", "Ne pas privilégier la pose en décubitus latéral par rapport à la "
         "position assise pour réduire la morbidité maternelle, les difficultés de "
         "pose, ou améliorer l'efficacité/la satisfaction maternelle.", "G2"),
    ], RCW))
    story.append(Spacer(1, 2 * mm))
    story.append(absence_note(
        "intérêt du monitorage systématique maternel et du rythme cardiaque fœtal "
        "pendant la pose de l'APM, pour réduire la morbidité néonatale."))
    story.append(Spacer(1, 2 * mm))
    story.append(reco_table([
        ("R1.3.1", "Dans tous les cas, si la pose de l'APM excède 30 minutes ou en cas "
         "de symptomatologie évocatrice d'une hypotension maternelle, vérifier la "
         "normalité de la pression artérielle maternelle et du RCF (même si cela "
         "impose une interruption transitoire de la procédure).", "AE"),
    ], RCW))
    story.append(Spacer(1, 2 * mm))
    story.append(absence_note(
        "port de la casaque stérile (indépendamment des mesures d'asepsie recommandées "
        "par la SF2H), pour réduire la morbidité infectieuse maternelle."))
    story.append(Spacer(1, 2 * mm))
    story.append(P("<b>Femmes sous traitement anticoagulant (HBPM)</b>", S_CELL_B))
    story.append(Spacer(1, 1 * mm))
    story.append(reco_table([
        ("R1.5.1", "Interrompre le traitement par HBPM à dose prophylactique ou "
         "curative avant la pose d'une APM, pour prévenir le risque d'hématome "
         "périmédullaire.", "G1"),
        ("R1.5.2", "Poser l'APM au moins 12h après la dernière injection d'HBPM à dose "
         "prophylactique et au moins 24h après une dose curative, pour prévenir le "
         "risque d'hématome périmédullaire.", "G2"),
        ("R1.5.3", "Chez une femme traitée par HBPM en cours de grossesse, vérifier "
         "avant la pose (ou l'ablation du cathéter) que l'activité anti-Xa est "
         "≤ 0,1 UI/ml — si délai &lt; 12h (prophylactique) ou &lt; 24h (curative), ou "
         "en cas d'insuffisance rénale modérée à sévère (DFG &lt; 50 ml/min).", "AE"),
    ], RCW))
    return story

# ---------------------------------------------------------------------------
def _section_champ2_3():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Champ 2 — Initiation de l'APM"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("R2.1", "Si une efficacité rapide de l'APM est attendue, proposer une "
         "technique avec ponction durale plutôt qu'une APM classique, pour améliorer "
         "le délai d'installation et la qualité du bloc initial.", "G2"),
        ("R2.2.1", "Accéder à une demande d'APM précoce (améliore la satisfaction "
         "maternelle sans augmenter la morbidité ni modifier la voie d'accouchement "
         "ou la durée du travail).", "G2"),
        ("R2.2.2", "Proposer une APM précoce dans les populations à risque* (maternel, "
         "anesthésique ou obstétrical), pour diminuer le risque de morbidité "
         "maternelle. *Ex. : obésité, comorbidité, intubation difficile prévisible, "
         "risque de césarienne augmenté, grossesse multiple.", "AE"),
        ("R2.3.1", "Ne pas réaliser de « dose test à la lidocaïne » pour vérifier le "
         "bon positionnement du cathéter de péridurale.", "G1"),
        ("R2.3.2", "Réaliser un bolus initial avec l'anesthésique local du mélange "
         "analgésique, pour détecter un mauvais positionnement du cathéter.", "G1"),
    ], RCW))
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Champ 3 — Entretien de l'APM"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("R3.1", "Utiliser le mode bolus intermittent programmé (BIP) plutôt que le "
         "débit continu, pour améliorer l'efficacité analgésique et la satisfaction "
         "maternelle.", "G2"),
        ("R3.2", "Permettre la déambulation pendant le travail sous APM aux patientes "
         "qui le souhaitent (pas d'impact négatif sur la morbidité maternelle/fœtale "
         "ni les issues obstétricales ; favorise la miction spontanée).", "AE"),
    ], RCW))
    return story

# ---------------------------------------------------------------------------
def _section_champ4a():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Champ 4 — Gestion de l'insuffisance et de l'échec de l'APM (1/2)"),
        Spacer(1, 1 * mm),
        P("<b>Surveillance pour limiter l'insuffisance/l'échec</b>", S_CELL_B),
        Spacer(1, 1 * mm),
    ]))
    story.append(reco_table([
        ("R4.1.1.1", "Réaliser la surveillance systématique de l'installation de l'APM "
         "et l'évaluation de l'intensité douloureuse à partir de 30 min après le "
         "bolus initial, avec identification des niveaux du bloc métamérique au test "
         "au froid.", "AE"),
        ("R4.1.1.2", "Évaluer toutes les heures l'efficacité de l'APM (intensité "
         "douloureuse), pour dépister une insuffisance ou un échec.", "AE"),
        ("R4.1.1.3", "Ne pas demander aux femmes de rester dans une position "
         "spécifique après l'injection péridurale dans le but d'améliorer l'efficacité "
         "ou de prévenir l'échec.", "G2"),
    ], RCW))
    story.append(Spacer(1, 2 * mm))
    story.append(absence_note(
        "organisation des soins d'anesthésie qui permettrait de limiter la survenue "
        "d'une insuffisance ou d'un échec d'analgésie."))
    story.append(Spacer(1, 2 * mm))
    story.append(P("<b>Anesthésique local et stratégies pharmacologiques</b>", S_CELL_B))
    story.append(Spacer(1, 1 * mm))
    story.append(reco_table([
        ("R4.1.3", "Ne pas privilégier un anesthésique local plutôt qu'un autre, entre "
         "bupivacaïne, lévobupivacaïne et ropivacaïne, pour réduire l'insuffisance ou "
         "l'échec d'analgésie.", "G1"),
        ("R4.1.4.1", "Associer systématiquement du sufentanil (morphinique liposoluble) "
         "aux anesthésiques locaux en péridural, pour réduire le risque d'insuffisance/"
         "échec et améliorer la satisfaction maternelle.", "G1"),
        ("R4.1.4.2", "Ne pas utiliser en 1<super>re</super> intention la clonidine associée aux "
         "anesthésiques locaux en péridural.", "G1"),
        ("R4.1.4.3", "Ne pas utiliser l'adrénaline en association aux anesthésiques "
         "locaux.", "G2"),
        ("R4.2.1.1", "En cas d'insuffisance d'analgésie, administrer un bolus (répété "
         "si besoin) du mélange analgésique d'entretien.", "AE"),
        ("R4.2.1.2", "Si l'insuffisance persiste, utiliser le même anesthésique local à "
         "plus forte concentration, éventuellement avec un adjuvant.", "AE"),
        ("R4.2.2", "En cas d'insuffisance, injecter du sufentanil ou de la clonidine "
         "pour améliorer l'efficacité de l'APM.", "AE"),
    ], RCW))
    return story

def _section_champ4b():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Champ 4 — Gestion de l'insuffisance et de l'échec de l'APM (2/2)"),
        Spacer(1, 1 * mm),
        P("<b>Évaluation complémentaire &amp; repose de cathéter</b>", S_CELL_B),
        Spacer(1, 1 * mm),
    ]))
    story.append(reco_table([
        ("R4.2.3", "En cas de reprise de la douleur, compléter l'évaluation de "
         "l'intensité douloureuse par une évaluation du niveau métamérique au test au "
         "froid.", "AE"),
        ("R4.2.4.1", "En cas d'échec/insuffisance et/ou d'insatisfaction maternelle, "
         "conduire des mesures correctrices (cf Figure 4) et en évaluer l'efficacité "
         "dans les 30-45 min.", "G1"),
        ("R4.2.4.2", "Poser à nouveau un cathéter péridural en cas d'échec à 45 min "
         "(après la 1<super>re</super> pose ou après les mesures correctrices).", "G1"),
        ("R4.2.4.3", "Faire réaliser une nouvelle pose de cathéter après échec par un "
         "médecin anesthésiste-réanimateur expérimenté.", "AE"),
        ("R4.2.4.4", "Utiliser une technique avec ponction durale en cas de nouvelle "
         "pose à dilatation cervicale avancée et/ou chez une parturiente hyperalgique.",
         "G2"),
    ], RCW))
    story.append(Spacer(1, 2 * mm))
    story.append(absence_note(
        "impact d'une position maternelle spécifique pour corriger une insuffisance ou "
        "un échec d'APM."))
    story.append(Spacer(1, 2 * mm))
    story.append(absence_note(
        "efficacité de l'hypnose et du soutien continu à prévenir/diminuer une "
        "insuffisance ou un échec d'APM."))
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Figure 4 — Algorithme de gestion de l'APM (d'après Rackelboom)",
                    color=GREY),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(theme_table([
        ("1. Pose", "Asepsie rigoureuse (antiseptique coloré) ; échorepérage si pose "
         "difficile prévue (obèse, rachis difficile) ; monitorage RCF+FC+PA/5min si "
         "pose &gt; 30 min ; délai après HBPM ≥ 12h (prophylactique) / ≥ 24h "
         "(curative)."),
        ("2. Initiation", "APD ou PPD avec bolus initial (AL faible concentration "
         "≤ 1 mg/ml) ; si niveau sensitif &gt; T6 + bloc moteur → suspicion cathéter "
         "intrathécal ; si niveau &gt; T6 + mosaïque ± Sd de Claude Bernard-Horner → "
         "suspicion cathéter sous-dural : dans les deux cas, arrêt de toute injection "
         "et attente de récupération sensitivo-motrice avant repose (privilégier PRC "
         "ou PPD si travail avancé/hyperalgique)."),
        ("3. Entretien", "BIP + PCEA (ou débit continu + PCEA) ; objectif niveau "
         "sensitif T10 sans bloc moteur ; surveillance douleur/niveau "
         "sensitif/PA/bloc moteur, évaluation à 30 min puis toutes les heures et après "
         "chaque ajustement ; signes de toxicité aux AL ou douleur persistante/absence "
         "de niveau &gt; 45 min → arrêt et réévaluation complète."),
        ("4. Insuffisance", "Niveau insuffisant &lt; T10 → vérifier absence de problème "
         "technique sur la ligne, effet volume (réinjection fractionnée), repère à la "
         "peau ; latéralisation/asymétrie → effet volume puis retrait du cathéter de "
         "1 cm si échec à 15 min ; puissance insuffisante/point douloureux → effet "
         "concentration (AL plus concentré) puis adjuvant (clonidine dose unique ou "
         "sufentanil) ; dans tous les cas, réévaluation à 30-45 min."),
    ], TCW, head=("Étape", "Points clés")))
    return story

# ---------------------------------------------------------------------------
def _section_champ5_sources():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Champ 5 — Alternatives médicamenteuses à l'APM"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("R5.1.1", "Recourir à l'APM plutôt qu'aux alternatives de type opioïdes en "
         "mode PCA, pour réduire la morbidité maternelle et améliorer l'efficacité/la "
         "satisfaction, sans impacter les issues obstétricales.", "G1"),
        ("R5.1.2", "En cas de contre-indication à l'APM, utiliser le rémifentanil IV en "
         "mode autocontrôlé (PCA) plutôt que l'absence de prise en charge, pour "
         "améliorer la morbidité maternelle sans impact sur la morbidité néonatale.",
         "G2"),
        ("R5.2.1", "Chez les parturientes sous opioïdes, assurer une surveillance "
         "rapprochée clinique (sédation, fréquence respiratoire) et paraclinique "
         "(SaO<sub>2</sub>, CO<sub>2</sub> expiré), pour réduire la morbidité maternelle.",
         "G1"),
        ("R5.2.2", "Apporter un supplément d'oxygène tout au long de la PCA de "
         "rémifentanil, pour réduire la morbidité maternelle.", "AE"),
        ("R5.3", "Ne pas utiliser le protoxyde d'azote dans le but d'améliorer "
         "l'efficacité analgésique ou la satisfaction maternelle comparé à l'APM.",
         "G1"),
    ], RCW))
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("Sources et avertissement", color=GREY))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>Promoteurs :</b> SFAR et Collège d'Anesthésie et Réanimation en Obstétrique "
        "(CARO), en association avec le CNGOF, la SF2H, le CNSF, le CIANE, le GIHP, la "
        "SFTH, le Collège des Infirmier(e)s Puéricultrices(teurs) et l'AFPBN. RBP "
        "labellisée HAS, validée par le Collège de la HAS le 30 avril 2025 — "
        "actualisation des recommandations SFAR de 2006 sur l'analgésie obstétricale.",
        S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>URL source :</b> https://sfar.org/prise-en-charge-de-la-douleur-de-"
        "laccouchement-analgesie-perimedullaire-et-alternatives-medicamenteuses/",
        S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>Couverture :</b> intégralité des 34 recommandations et des 5 absences de "
        "recommandation (5 champs). La Figure 4 (algorithme de gestion de "
        "l'insuffisance/échec) est retranscrite en tableau condensé depuis un rendu "
        "visuel. Les Figures 1 et 2 (schémas techniques APD/PRC/PPD et modes "
        "d'administration) ne sont pas retranscrites en détail — purement "
        "illustratives d'une terminologie déjà explicitée dans le texte des "
        "recommandations. Bibliographie et composition nominative des groupes de "
        "travail non reproduites.", S_SOURCE))
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Avertissement :</b> cette fiche est une synthèse indépendante, produite "
        "pour un usage d'aide-mémoire. Elle reprend intégralement les 34 "
        "recommandations et les 5 absences de recommandation du texte source, mais "
        "condense l'argumentaire de chaque item. Elle ne remplace pas le texte "
        "intégral et n'est ni éditée ni validée par la HAS, la SFAR ni le CARO.",
        S_BODY_SM), bg=GREY_LIGHT, border=GREY))
    return story

# ---------------------------------------------------------------------------
SECTIONS = [
    ("Champ 1 — Pose de l'analgésie périmédullaire", _section_intro_champ1),
    ("Champs 2-3 — Initiation & entretien de l'APM", _section_champ2_3),
    ("Champ 4 — Gestion de l'insuffisance/échec (1/2)", _section_champ4a),
    ("Champ 4 — Gestion de l'insuffisance/échec (2/2) & Figure 4", _section_champ4b),
    ("Champ 5 — Alternatives médicamenteuses & sources", _section_champ5_sources),
]

def _make_doc(path=None):
    return SimpleDocTemplate(path or OUT, pagesize=A4,
                              leftMargin=MARGIN, rightMargin=MARGIN,
                              topMargin=32 * mm, bottomMargin=16 * mm,
                              title="Fiche HAS/SFAR/CARO 2025 - Douleur de l'accouchement",
                              author="Synthèse indépendante (source HAS/SFAR/CARO)")

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
