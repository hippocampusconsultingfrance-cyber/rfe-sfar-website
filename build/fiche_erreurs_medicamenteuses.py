# -*- coding: utf-8 -*-
"""
Fiche de synthese - Societe Francaise d'Anesthesie et de Reanimation (SFAR),
"Prevention des erreurs medicamenteuses en anesthesie". Recommandations de
la Sfar, novembre 2006 (redigees par G. Aulagner, P. Dewachter,
P. Diemunsch, Ph. Garnerin, M. Latourte, Q. Levrat, A. Mignon, V. Piriou ;
amendees et validees par le Comite Analyse et Maitrise du Risque de la
SFAR). 7 pages, telecharge depuis sfar.org (wp-content/uploads/2014/04/
preverreurmedic_recos.pdf).

METHODOLOGIE : 13e convention methodologique distincte de ce corpus - texte
narratif avec citations bibliographiques entre crochets [1], [2]... (20
references), AUCUN systeme de cotation GRADE/niveau de preuve individuel
par recommandation. Le texte source le dit lui-meme explicitement : "il
n'existe que tres peu de travaux ayant prouve de maniere irrefutable,
l'efficacite des mesures de prevention" - les recommandations reposent sur
un consensus d'experts amende par le Comite Analyse et Maitrise du Risque
de la SFAR, pas sur une grille de preuve formelle. Restitue en panneaux et
tableaux thematiques, jamais en reco_table avec chip - meme traitement que
fiche_sauv.py / fiche_relations_anesth_chir.py pour ce type de document.

COUVERTURE : integrale - etat des lieux (epidemiologie des erreurs
medicamenteuses, generale et specifique a l'anesthesie, repartition par
type d'erreur), origine des erreurs (Figure 1 - arbre des pannes complet,
rendu a 250dpi et retranscrit noeud par noeud avec ses portes logiques
ET/OU, aucune couche texte fiable pour ce schema), recommandations
(generalites, prevention des erreurs de reconstitution - specialite,
dilution, etiquetage -, prevention des erreurs d'administration - voie
d'administration, seringues -, Tableau 1 - codes couleurs/trames Pantone
des 13 classes pharmacologiques, reproduit verbatim), et la bibliographie
complete (20 references). Rien n'est omis. Le texte exclut lui-meme de son
perimetre les erreurs de moment/volume-debit (renvoyees aux dispositifs
medicaux d'administration) et les erreurs de patient (objet d'une
recommandation specifique separee) - disclosure reprise telle quelle
depuis la source, non une omission de cette fiche.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from style import *
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.units import mm

OUT = "/home/user/rfe-sfar-website/output/Fiche_SFAR_Erreurs_Medicamenteuses_Anesthesie_2006.pdf"

SOURCE_TXT = ("Source : « Prévention des erreurs médicamenteuses en anesthésie » — "
              "Recommandations de la SFAR, novembre 2006. Fiche de synthèse non "
              "officielle : se référer au texte intégral.")

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

TCW = [50 * mm, CW_FULL - 50 * mm]

def grid_table(head, rows, col_widths, small=True):
    st_cell = S_BODY_SM if small else S_CELL
    st_head = S_HEAD_W_C
    data = [[P(h, st_head) for h in head]]
    for row in rows:
        data.append([P(str(cell), st_cell) if i == 0 else P(str(cell), S_CELL_C)
                     for i, cell in enumerate(row)])
    t = Table(data, colWidths=col_widths, repeatRows=1)
    style_cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), NAVY), ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTNAME", (0, 0), (-1, 0), FONT_BOLD), ("FONTSIZE", (0, 0), (-1, 0), 7.6),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("ALIGN", (1, 1), (-1, -1), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 0.5, GREY_LIGHT),
        ("TOPPADDING", (0, 0), (-1, -1), 2.6), ("BOTTOMPADDING", (0, 0), (-1, -1), 2.6),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            style_cmds.append(("BACKGROUND", (0, i), (-1, i), BG_PANEL))
    t.setStyle(TableStyle(style_cmds))
    return t

def bullets(items, style=S_BODY_SM):
    html = "&bull; " + "<br/>&bull; ".join(items)
    return P(html, style)

TOTAL_PAGES = {"n": 4}

def on_page(canvas, doc, page_title):
    header_band(canvas, doc, "SFAR — RECOMMANDATIONS, NOVEMBRE 2006",
                "Prévention des erreurs médicamenteuses en anesthésie",
                page_title, icon_fn=lambda c, x, y: icon_pill(c, x, y, 13 * mm), color=RED)
    footer_band(canvas, doc, SOURCE_TXT, f"Page {doc.page} / {TOTAL_PAGES['n']}")

# ---------------------------------------------------------------------------
def _section_intro():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Champ :</b> recommandations de la SFAR (novembre 2006) sur la prévention "
        "des erreurs médicamenteuses en anesthésie — rédigées par un groupe d'experts, "
        "amendées et validées par le Comité Analyse et Maîtrise du Risque de la SFAR.",
        S_BODY), bg=BG_PANEL, border=TEAL))
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Méthodologie :</b> texte narratif appuyé sur une bibliographie de "
        "20 références (citées entre crochets, ex. [1], [16-19]) — <b>aucun système "
        "de cotation GRADE ni niveau de preuve individuel</b> par recommandation. Le "
        "texte source précise lui-même qu'il existe très peu de travaux ayant prouvé "
        "de manière irréfutable l'efficacité des mesures de prévention évoquées : les "
        "recommandations reposent sur un consensus d'experts, restitué ici en panneaux "
        "et tableaux thématiques, jamais en chip de grade inventé.", S_BODY_SM),
        bg=AMBER_LIGHT, border=AMBER))
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("État des lieux"))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "Les erreurs médicamenteuses sont fréquentes, à toutes les étapes du processus "
        "thérapeutique : l'erreur survient de 1 fois sur 100 à 1 fois sur 10 à chaque "
        "étape du circuit du médicament (prescription ; dispensation, reconstitution, "
        "administration). Environ 1 % de ces erreurs entraînent un événement "
        "indésirable grave (EIG) évitable. Aux États-Unis, elles représentent la "
        "4<sup>e</sup> cause d'EIG déclarés et sont responsables d'environ 7 000 décès "
        "annuels évitables. En France, elles provoquent un EIG toutes les 2 000 "
        "journées d'hospitalisation, soit environ 70 000 EIG par an (estimation sur la "
        "base de 140 millions de journées d'hospitalisation/an).", S_BODY))
    story.append(Spacer(1, 1.8 * mm))
    story.append(P(
        "<b>En anesthésie</b>, les rares études publiées montrent qu'une erreur "
        "médicamenteuse survient de 1 fois sur 900 à 1 fois sur 130 anesthésies. En "
        "estimant 5 médicaments administrés en moyenne par anesthésie, la fréquence "
        "par administration serait de l'ordre de 1 fois sur 10 000 à 1 fois sur 1 000 — "
        "chiffre vraisemblablement sous-estimé (déclarations volontaires, méthode peu "
        "adaptée) : la fréquence observée pourrait être jusqu'à 400 fois supérieure à "
        "celle déclarée.", S_BODY))
    story.append(Spacer(1, 1.8 * mm))
    story.append(P(
        "Répartition des erreurs relevées en anesthésie, par ordre de fréquence "
        "décroissante : seringues et ampoules (50 %) ; dispositifs médicaux "
        "d'administration (26 %) ; voie d'administration (14 %). Pour les erreurs de "
        "seringues/ampoules : 62 % de confusion de spécialité, 11 % d'erreur de "
        "concentration. Lors d'une confusion de spécialités, l'erreur survient dans "
        "55 % des cas à l'administration (erreur de seringue) et dans 45 % pendant la "
        "reconstitution (erreur de spécialité, erreur d'étiquetage).", S_BODY_SM))
    story.append(Spacer(1, 1.8 * mm))
    story.append(P(
        "Il n'existe que très peu de travaux ayant prouvé de manière irréfutable "
        "l'efficacité des mesures de prévention évoquées dans la littérature "
        "(étiquetage des seringues/perfusions, rangement des plateaux d'anesthésie, "
        "médicaments prêts à l'emploi). L'élaboration de ces recommandations par la "
        "SFAR est néanmoins justifiée par : la fréquence élevée des erreurs, leur "
        "gravité potentielle, leur caractère évitable et leur faible acceptabilité ; "
        "l'influence connue de l'environnement de travail sur la probabilité d'erreurs "
        "humaines dans les domaines industriels à risque ; la publication de "
        "recommandations/normes dans d'autres pays (Australie, Canada, États-Unis, "
        "Nouvelle-Zélande, Royaume-Uni).", S_BODY_SM))
    return story

# ---------------------------------------------------------------------------
# Figure 1 (source page 2) - fault-tree diagram ("arbre des pannes"), no
# reliable text layer - rendered at 250dpi and transcribed node-by-node with
# its logic gates (ET/OU), per the source's own caption + visual reading.
FIGURE1_ROWS = [
    ("Erreur médicamenteuse <i>(erreur résultante)</i>",
     "= Erreur de reconstitution <b>OU</b> Erreur d'administration"),
    ("Erreur de reconstitution <i>(erreur intermédiaire)</i>",
     "= Erreur de spécialité <b>OU</b> Erreur de dilution <b>OU</b> Erreur "
     "d'étiquetage"),
    ("&nbsp;&nbsp;- Erreur de spécialité <i>(erreur intermédiaire)</i>",
     "= Erreur de sélection (spécialité) <b>ET</b> Erreur de contrôle (spécialité) "
     "<i>(erreurs élémentaires)</i>"),
    ("&nbsp;&nbsp;- Erreur de dilution", "<i>Erreur non détaillée</i>"),
    ("&nbsp;&nbsp;- Erreur d'étiquetage", "<i>Erreur non détaillée</i>"),
    ("Erreur d'administration <i>(erreur intermédiaire)</i>",
     "= Erreur de seringue <b>OU</b> Erreur de voie d'administration <b>OU</b> "
     "Erreur de volume ou de débit <b>OU</b> Erreur de moment <b>OU</b> Erreur de "
     "patient"),
    ("&nbsp;&nbsp;- Erreur de seringue <i>(erreur intermédiaire)</i>",
     "= Erreur de sélection (seringue) <b>ET</b> Erreur de contrôle (seringue) "
     "<i>(erreurs élémentaires)</i>"),
    ("&nbsp;&nbsp;- Erreur de voie d'administration <i>(erreur intermédiaire)</i>",
     "= Erreur de sélection (voie) <b>ET</b> Erreur de contrôle (voie) "
     "<i>(erreurs élémentaires)</i>"),
    ("&nbsp;&nbsp;- Erreur de volume ou de débit", "<i>Erreur non détaillée</i>"),
    ("&nbsp;&nbsp;- Erreur de moment", "<i>Erreur non détaillée</i>"),
    ("&nbsp;&nbsp;- Erreur de patient", "<i>Erreur non détaillée</i>"),
]

def _section_origine():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Origine des erreurs médicamenteuses — Figure 1"),
        Spacer(1, 1.5 * mm),
        P("Modélisation par la méthode de l'arbre des pannes (Ph. Garnerin, 2006), à "
          "partir des combinaisons d'erreurs élémentaires pouvant survenir aux étapes "
          "menant à l'administration du médicament. Deux catégories : erreurs de "
          "reconstitution (spécialité, dilution, étiquetage) et erreurs "
          "d'administration (seringue, voie d'administration, volume/débit, moment, "
          "patient). Arbre reproduit ci-dessous en tableau (nœud, porte logique "
          "ET/OU, composantes) depuis un rendu visuel de la Figure 1 — aucune couche "
          "texte fiable dans le PDF source pour ce schéma.", S_BODY_SM),
    ]))
    story.append(Spacer(1, 1.5 * mm))
    story.append(grid_table(("Nœud de l'arbre", "Décomposition"), FIGURE1_ROWS,
                              [80 * mm, CW_FULL - 80 * mm], small=True))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>Légende des symboles source :</b> rectangle arrondi = erreur résultante ; "
        "rectangle = erreur intermédiaire ; losange = erreur non détaillée ; cercle = "
        "erreur élémentaire.", S_NOTE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "Le modèle met en évidence que les erreurs de spécialité, de seringue et de "
        "voie d'administration résultent toutes de la combinaison d'une erreur de "
        "<b>sélection</b> et d'une erreur de <b>contrôle</b>. La prévention de ces "
        "erreurs implique donc la combinaison de <b>mesures actives</b> de contrôle et "
        "de <b>mesures passives</b> destinées à en renforcer l'efficacité et à "
        "réduire les possibilités d'interversion.", S_BODY_SM))
    return story

def _section_intro_origine():
    story = _section_intro()
    story.append(Spacer(1, 2 * mm))
    story.extend(_section_origine())
    return story

# ---------------------------------------------------------------------------
def _section_recommandations_generalites():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Recommandations — Généralités"),
        Spacer(1, 1.5 * mm),
        P("Une structure de soins réalisant des anesthésies doit mener une réflexion "
          "pérenne sur les moyens à mettre en œuvre pour prévenir les erreurs "
          "médicamenteuses, aboutissant à des mesures de prévention spécifiques, "
          "communes à toute la structure et formalisées par écrit. Les actions mises "
          "en place doivent être réévaluées régulièrement. Les événements "
          "médicamenteux indésirables évitables, avérés ou potentiels, doivent "
          "pouvoir être déclarés — notamment à la commission du médicament et des "
          "dispositifs médicaux stériles — et faire l'objet d'une analyse détaillée, "
          "de préférence interdisciplinaire. L'ensemble de la démarche conduite par "
          "la structure doit être documenté, et les preuves de son existence "
          "apportées.", S_BODY),
    ]))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>Périmètre :</b> les mesures détaillées ci-dessous concernent l'ensemble "
        "des erreurs de reconstitution, ainsi que 2 erreurs d'administration (voie "
        "d'administration, seringues). Sont explicitement <b>exclues</b> de ce "
        "document : la prévention des erreurs de moment et des erreurs de volume/"
        "débit (relevant essentiellement des dispositifs médicaux d'administration — "
        "choix, paramétrage, maintenance, formation) ; la prévention des erreurs de "
        "patient (objet d'une recommandation spécifique séparée, non détaillée ici).",
        S_BODY_SM))
    return story

def _section_reconstitution():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Prévention des erreurs de reconstitution"),
        Spacer(1, 1.5 * mm),
        P("D'une manière générale, des dispositions destinées à limiter les "
          "perturbations lors des tâches de préparation des médicaments devraient "
          "être prises.", S_BODY_SM),
    ]))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P("<b>Erreurs de spécialité :</b> contrôle actif des informations "
                    "notées sur le conditionnement, par lecture attentive (nécessité "
                    "à rappeler périodiquement), complété par des mesures passives :",
                    S_BODY_SM))
    story.append(Spacer(1, 1 * mm))
    story.append(bullets([
        "choix des médicaments d'anesthésie restreint au strict nécessaire, en "
        "concertation avec le pharmacien de l'établissement ;",
        "stock disponible de chaque spécialité restreint au minimum ;",
        "système de rangement clair et commun (armoires, chariots d'urgence, table "
        "d'anesthésie, plateaux) ;",
        "médicaments et concentrations disponibles limités aux seuls régulièrement "
        "utilisés ;",
        "identification, signalement et, si possible, élimination systématiques des "
        "similitudes de forme/couleur/dénomination entre spécialités présentes ;",
        "information des utilisateurs de tout changement affectant les médicaments "
        "mis à disposition ;",
        "prise en compte, dans la réflexion générale, du retour des médicaments non "
        "utilisés vers leur lieu de rangement initial (source d'erreur).",
    ]))
    story.append(Spacer(1, 1.8 * mm))
    story.append(P(
        "<b>Erreurs de dilution :</b> protocoles de préparation des médicaments, "
        "faciles à mettre en œuvre, si possible communs à la structure d'anesthésie "
        "et aux autres structures de soins aigus de l'institution — précisant les "
        "modalités de reconstitution, la concentration (mg/ml, µg/ml, UI/ml), le "
        "volume à préparer et celui de la seringue utilisée. En accord avec le "
        "pharmacien : associations médicamenteuses utilisables et durée de "
        "conservation des préparations précisées. Le recours à des médicaments prêts "
        "à l'emploi (industrie pharmaceutique ou pharmacie de l'institution) devrait "
        "être encouragé.", S_BODY_SM))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>Erreurs d'étiquetage :</b> chaque médicament doit être reconstitué et "
        "étiqueté au cours d'une seule séquence de gestes, par la même personne, "
        "sans interruption ni changement de lieu.", S_BODY_SM))
    return story

def _section_recommandations_reconstitution():
    story = _section_recommandations_generalites()
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_reconstitution())
    return story

# ---------------------------------------------------------------------------
COLOR_TABLE_ROWS = [
    ("Anti-émétiques", "Métoclopramide, ondansétron", "Saumon 156"),
    ("Hypnotiques", "Thiopental, étomidate, kétamine, propofol", "Jaune"),
    ("Benzodiazépines", "Diazépam, midazolam", "Orange 151"),
    ("Antagoniste des benzodiazépines", "Flumazénil",
     "Orange 151 + bandes blanches diagonales"),
    ("Curarisants", "Succinylcholine, atracurium, cisatracurium, vécuronium, "
     "rocuronium", "Rouge fluorescent 805 ou rouge vif"),
    ("Antagonistes des curarisants", "Néostigmine",
     "Rouge fluorescent 805/rouge vif + bandes blanches diagonales"),
    ("Opioïdes", "Morphine, fentanyl, sufentanil, rémifentanil, alfentanil",
     "Bleu 297"),
    ("Antagonistes des opioïdes", "Naloxone", "Bleu 297 + bandes blanches diagonales"),
    ("Neuroleptiques", "Dropéridol", "Saumon 156"),
    ("Sympathomimétiques", "Adrénaline, noradrénaline, éphédrine, phényléphrine",
     "Violet 256"),
    ("Anti-hypertenseurs", "Nicardipine, nitroglycérine, phentolamine",
     "Violet 256 + bandes blanches diagonales"),
    ("Anesthésiques locaux", "Lidocaïne, bupivacaïne, ropivacaïne, "
     "lévobupivacaïne, mépivacaïne", "Gris 401"),
    ("Anticholinergiques", "Atropine", "Vert 367"),
    ("Autres", "Ocytocine, héparine, protamine, antibiotiques",
     "Blanc (protamine : blanc + bandes noires diagonales)"),
]

def _section_administration():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Prévention des erreurs d'administration"),
        Spacer(1, 1.5 * mm),
        P("<b>Erreurs de voie d'administration :</b> contrôle actif du point "
          "d'insertion de la voie (nécessité à rappeler périodiquement), complété "
          "par des mesures passives : voies d'administration identifiées par "
          "étiquettes mentionnant explicitement leur nature, apposées à proximité du "
          "patient et de tous les points d'entrée ; présence de robinets sur les "
          "cathéters/tubulures d'ALR à éviter ; recours à des systèmes physiques de "
          "limitation des erreurs (détrompeurs à connectique différente selon la "
          "voie, cathéters de couleur/forme différentes, ex. hélicoïdal) à "
          "considérer.", S_BODY),
    ]))
    story.append(Spacer(1, 1.8 * mm))
    story.append(P(
        "<b>Erreurs de seringues</b> (administration directe ou continue) : contrôle "
        "actif par lecture attentive des informations de l'étiquette (rappel "
        "périodique), complété par des mesures passives :", S_BODY_SM))
    story.append(Spacer(1, 1 * mm))
    story.append(bullets([
        "seringues systématiquement étiquetées, étiquette lisible sans masquer les "
        "graduations ;",
        "interdiction d'utiliser une seringue sans nom de spécialité ou sans "
        "concentration ;",
        "système uniforme d'étiquetage au sein de la structure, comprenant des "
        "étiquettes autocollantes pré-imprimées (DCI du médicament) et un "
        "emplacement libre réservé à la concentration (unité pré-imprimée) ;",
        "système d'étiquetage appuyé sur les codes internationaux de couleurs et de "
        "trames par classe pharmacologique (tableau ci-dessous) ;",
        "combinaison variable de majuscules/minuscules à considérer comme moyen "
        "supplémentaire (ex. DOBUTamine, DOPAmine, ATROpine, aPROTInine) ;",
        "sauf médicaments de l'urgence, pas de préparation à l'avance si "
        "l'utilisation pendant l'anesthésie n'est pas certaine ;",
        "sauf nécessité absolue, pas de plusieurs concentrations du même médicament "
        "simultanément disponibles sur un même plateau ;",
        "seringues préparées rangées dans les plateaux selon un plan prédéfini, "
        "commun à toute la structure ;",
        "plateaux d'anesthésie protégés, portant la date et l'heure de préparation "
        "et l'identification du préparateur.",
    ]))
    story.append(Spacer(1, 1.8 * mm))
    story.append(P("<b>Tableau 1 — Identification des seringues des médicaments de "
                    "l'anesthésie : codes internationaux de couleurs et de trames</b> "
                    "(reproduit verbatim)", S_CELL_B))
    story.append(Spacer(1, 1 * mm))
    story.append(grid_table(("Classe pharmacologique", "Exemples", "Couleur Pantone® et trame"),
                              COLOR_TABLE_ROWS,
                              [42 * mm, 68 * mm, CW_FULL - 110 * mm], small=True))
    story.append(Spacer(1, 1 * mm))
    story.append(P("Nb : les agents antagonistes sont identifiés à l'aide "
                    "d'étiquettes dont la trame est hachurée.", S_NOTE))
    return story

def _section_sources():
    story = []
    story.append(section_bar("Sources et traçabilité", color=GREY))
    story.append(Spacer(1, 2 * mm))
    story.append(P(
        "<b>Document source :</b> « Prévention des erreurs médicamenteuses en "
        "anesthésie » — Recommandations de la SFAR, novembre 2006. Rédigé par "
        "G. Aulagner, P. Dewachter, P. Diemunsch, Ph. Garnerin, M. Latourte, "
        "Q. Levrat, A. Mignon, V. Piriou ; amendé et validé par le Comité Analyse et "
        "Maîtrise du Risque de la SFAR.", S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P("<b>Version :</b> novembre 2006.", S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P("<b>Méthodologie :</b> texte narratif appuyé sur 20 références "
                    "bibliographiques, sans système de cotation GRADE — voir "
                    "disclosure méthodologique en page 1.", S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>URL source :</b> https://sfar.org/wp-content/uploads/2014/04/"
        "preverreurmedic_recos.pdf", S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P("<b>Couverture :</b> cette fiche reprend l'intégralité du texte "
                    "(état des lieux, Figure 1 — arbre des pannes complet, "
                    "recommandations générales, prévention des erreurs de "
                    "reconstitution et d'administration, Tableau 1 — codes "
                    "couleurs/trames) et la bibliographie complète ci-dessous.",
                    S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>Bibliographie (20 références) :</b> 1. Dean B et al., Qual Saf Health "
        "Care 2002;11:340-4. 2. Van den Bemt PM et al., Drug Saf 2002;25:135-43. "
        "3. Dean BS et al., Am J Health Syst Pharm 1995;52:2543-9. 4. Taxis K et al., "
        "Pharm World Sci 1999;21:25-31. 5. Cina JL et al., Jt Comm J Qual Patient Saf "
        "2006;32:73-80. 6. Bates DW et al., J Gen Intern Med 1995;10:99-205. "
        "7. JCAHO, Sentinel event statistics, 31 déc. 2005. 8. Phillips D et al., "
        "Lancet 1998;351:643-4. 9. Michel P et al., Études et résultats, DREES 2005. "
        "10. Fasting S, Gisvold SE, Can J Anaesth 2000;47:1060-7. 11. Webster CS et "
        "al., Anaesth Intensive Care 2001;29:494-500. 12. Flynn EA et al., Am J "
        "Health Syst Pharm 2002;59:436-46. 13. Abeysekera A et al., Anaesthesia "
        "2005;60:220-7. 14. Jensen LS et al., Anaesthesia 2004;59:493-504. "
        "15. Gertman DI, Blackman HS, Human reliability and safety analysis data "
        "handbook, 1994. 16. CAN/CSA-Z264.3, 1998. 17. ASTM D4774, 1994. "
        "18. AS/NZS 4375, 1996. 19. Royal College of Anaesthetists — AAGBI, Syringe "
        "labelling in critical care areas, juin 2004. 20. CEI/IEC 1025, Analyse par "
        "arbre des pannes, 1990.", S_SOURCE))
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Avertissement — document de 2006 :</b> ce document est une fiche de "
        "synthèse indépendante, produite pour un usage d'aide-mémoire. Elle reprend "
        "l'intégralité des recommandations du texte source (dont la Figure 1, "
        "transcrite depuis un rendu visuel du PDF faute de couche texte fiable, et le "
        "Tableau 1 des codes couleurs), mais ne remplace pas le texte intégral et "
        "n'est ni éditée ni validée par la SFAR. Les pratiques d'étiquetage et de "
        "prévention des erreurs médicamenteuses ayant pu évoluer depuis 2006 "
        "(recommandations plus récentes, nouveaux dispositifs), se référer à un avis "
        "spécialisé et aux recommandations actualisées avant toute décision.",
        S_BODY_SM), bg=GREY_LIGHT, border=GREY))
    return story

def _section_administration_sources():
    story = _section_administration()
    story.append(Spacer(1, 4 * mm))
    story.extend(_section_sources())
    return story

def _section_intro_origine_recommandations():
    # Merged onto shared pages (no forced page break): "Methodologie, etat
    # des lieux & origine (Figure 1)" alone left its 2nd page ~15% white -
    # combined with the recommandations generales/reconstitution section per
    # the <60%-full merge rule (CLAUDE.md build pipeline, step 7).
    story = _section_intro_origine()
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_recommandations_reconstitution())
    return story

SECTIONS = [
    ("Méthodologie, état des lieux, origine (Figure 1) & recommandations générales",
     _section_intro_origine_recommandations),
    ("Prévention des erreurs d'administration, Tableau 1 & sources",
     _section_administration_sources),
]

def _make_doc(path=None):
    return SimpleDocTemplate(path or OUT, pagesize=A4,
                              leftMargin=MARGIN, rightMargin=MARGIN,
                              topMargin=32 * mm, bottomMargin=16 * mm,
                              title="Fiche SFAR 2006 - Prevention des erreurs "
                                    "medicamenteuses en anesthesie",
                              author="Synthèse indépendante (source SFAR)")

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
