# -*- coding: utf-8 -*-
"""
Fiche de synthese - Societe de Reanimation de Langue Francaise (SRLF),
reactualisation de la 12e conference de consensus (texte long, revue Reanimation
12 (2003) 258-265, J.-F. Timsit). "Infections liees aux catheters veineux
centraux en reanimation". 8 pages, telecharge depuis sfar.org
(wp-content/uploads/2015/10/1-s2.0-S1624069303000513-main.pdf, format
journal Elsevier ScienceDirect, 2 colonnes denses).

METHODOLOGIE : 10e convention methodologique distincte rencontree dans ce
corpus - systeme "Niveau de recommandation" (1/2/3) + "Score d'evaluation"
des etudes (a/b/c/d), les deux publies EXPLICITEMENT en legende dans le texte
source (page 2, grille reproduite ci-dessous), combines en un code du type
"(1-b)", "(2-a)", "(3-c)" apres chaque affirmation. A la difference de la
fiche candidoses_aspergilloses (legende absente, disclosure necessaire), ici
la legende existe reellement dans la source et est reproduite fidelement,
sans aucune interpretation ajoutee. Convention de couleur de cette fiche :
coloree par le chiffre (niveau) - 1 = vert (preuves indiscutables), 2 =
bleu-sarcelle (preuves + consensus d'experts), 3 = ambre (avis d'experts sans
preuve adequate) - coherent avec le code couleur 1+/2+/2- deja utilise pour
le systeme GRADE ailleurs dans ce corpus. Plusieurs points sont explicitement
marques "point non resolu" par la source elle-meme (aucune recommandation
delivree, litterature insuffisante) - reproduits avec un badge gris distinct
"[point non resolu]", jamais convertis en une fausse recommandation gradee.

COUVERTURE : integrale des 5 questions de la conference (definition et
diagnostic de l'ILC ; mecanismes de contamination/colonisation ; facteurs de
risque/incidence/morbi-mortalite ; prevention - 10 sous-sections 5.1 a 5.10 ;
strategie diagnostique et therapeutique initiale - 4 sous-sections 6.1.1 a
6.2.4) + la Figure 1 (algorithme decisionnel pleine page, aucune couche texte
exploitable - rendue a 250dpi et retranscrite en tableau Etape/Situation/
Conduite, logique de branchement tracee arrow-par-arrow) + le glossaire des
abreviations (page 1) + le colophon (auteur, comite d'organisation, experts,
references). Rien n'est omis. Les particularites pediatriques disseminees
dans le texte source (incidence, materiel, voie d'abord, ETO) sont conservees
inline, comme dans la source.

CORRECTIONS POST-AUDIT : un audit independant (subagent aveugle au brouillon,
instruit de tracer chaque fleche de la Figure 1 individuellement apres
l'episode de mauvaise lecture rencontre sur la fiche candidoses_aspergilloses)
a confirme la Figure 1 exacte (aucune inversion de fleche) mais a trouve
7 problemes reels, tous corriges : (1) la case finale de la Figure 1 omettait
la ligne "Infection profonde ?" - ajoutee a FIG1_ROWS ; (2) deux badges
"point non resolu" avaient ete fabriques sur des phrases que la source ne
marque PAS ainsi (incidence des infections sur catheter de dialyse ; voie
axillaire) - retires, ces phrases redeviennent de simples constats non
cotes ; (3) la grille methodologique (score a-d / niveau 1-3), presentee
comme reproduite "sans aucune interpretation", contenait 3 simplifications
lexicales reelles (item c : "publies dans des revues avec comite de lecture"
et "exterieurs" manquants ; item d : "publiees dans des journaux ou livres"
manquant ; niveau 3 : "scientifiques" manquant avant "adequates") - grille
desormais mot-a-mot fidele ; (4) le tag (2-c) en 5.5 portait a tort sur le
groupe pansement+dates+surveillance au lieu de la seule phrase "surveillance
quotidienne" que la source cote - recadre ; (5) 5.1 affirmait une donnee
pediatrique heparine/bacteriemie comme certitude alors que la source dit
"les donnees disponibles suggerent que" - conditionnel restaure ; (6)
plusieurs omissions de contenu narratif comblees (variantes de culture
quantitative - rincage endoluminal, sonication ; base clinique du seuil
vortexage ; qualificatifs de la table "infection non liee au CVC" ; phrases
sur les facteurs de risque/strategie initiale en ouverture de Q5 ; details
de l'attitude conservatrice en 6.1.2 ; detail du contenu des programmes
d'education en 5.8) ; (7) reference bibliographique [2] (methodologie de
revision) et mention de la validation par le groupe de lecture SRLF /
disponibilite en ligne, absentes du colophon - ajoutees.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from style import *
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.units import mm

OUT = "/home/user/rfe-sfar-website/output/Fiche_SRLF_Infections_Catheters_Veineux_Centraux_2003.pdf"

SOURCE_TXT = ("Source : « Réactualisation de la douzième conférence de consensus de la "
              "SRLF : infections liées aux cathéters veineux centraux en réanimation » — "
              "J.-F. Timsit, Réanimation 12 (2003) 258-265. Fiche de synthèse non "
              "officielle : se référer au texte intégral.")

def P(txt, style=S_CELL):
    return Paragraph(txt, style)

CW_FULL = PAGE_W - 2 * MARGIN

def _tagcolor(code):
    d = code[0]
    return {"1": "#2d8a56", "2": "#0e7c85", "3": "#c8790c"}.get(d, "#6b7980")

def tag(code):
    return ' <font color="%s"><b>[%s]</b></font>' % (_tagcolor(code), code)

def nr():
    """Badge distinct pour les points explicitement non resolus par la source."""
    return ' <font color="#6b7980"><b>[point non résolu]</b></font>'

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

TCW = [58 * mm, CW_FULL - 58 * mm]

def bullets(items, style=S_BODY_SM):
    html = "&bull; " + "<br/>&bull; ".join(items)
    return P(html, style)

TOTAL_PAGES = {"n": 5}

def on_page(canvas, doc, page_title):
    header_band(canvas, doc, "SRLF — RÉACTUALISATION 12E CONFÉRENCE DE CONSENSUS 2003",
                "Infections liées aux cathéters veineux centraux",
                page_title, icon_fn=lambda c, x, y: icon_drop(c, x, y, 13 * mm), color=TEAL_DARK)
    footer_band(canvas, doc, SOURCE_TXT, f"Page {doc.page} / {TOTAL_PAGES['n']}")

# ---------------------------------------------------------------------------
def _section_intro():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Champ :</b> réactualisation de la 12<sup>e</sup> conférence de consensus SRLF "
        "de 1994 sur les infections liées aux cathéters (ILC) veineux centraux en "
        "réanimation, chez l'adulte et l'enfant. 5 questions. Coordination : "
        "J.-F. Timsit (adulte), P. Durand (pédiatrie).", S_BODY),
        bg=BG_PANEL, border=TEAL))
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Méthodologie :</b> chaque affirmation est cotée par un code "
        "<b>Niveau-Score</b> tel que" + tag("1-b") + tag("2-a") + tag("3-c") +
        " — légende publiée intégralement par la source (grille ci-dessous), "
        "reproduite ici sans aucune interprétation ajoutée. Convention de couleur "
        "de cette fiche : coloré selon le chiffre (niveau). Plusieurs points sont "
        "explicitement signalés « point non résolu » par la source (littérature "
        "insuffisante, aucune recommandation) — reproduits tels quels" + nr() +
        ", jamais convertis en une fausse recommandation gradée.", S_BODY_SM),
        bg=AMBER_LIGHT, border=AMBER))
    story.append(Spacer(1, 3 * mm))
    story.append(theme_table([
        ("Score d'évaluation (type d'étude)",
         "a — études prospectives, contrôlées, randomisées&nbsp;;&nbsp; b — études non "
         "randomisées, comparaisons simultanées ou historiques de cohortes&nbsp;;&nbsp; "
         "c — mises au point, revues générales, éditoriaux, séries substantielles de cas "
         "publiés dans des revues avec comité de lecture et révisés par des experts "
         "extérieurs&nbsp;;&nbsp; d — publications d'opinions publiées dans des journaux "
         "ou livres sans comité de lecture."),
        ("Niveau de recommandation",
         "1 — justifiée par des preuves scientifiques indiscutables&nbsp;;&nbsp; "
         "2 — justifiée par des preuves scientifiques et le soutien consensuel des "
         "experts&nbsp;;&nbsp; 3 — ne reposant pas sur des preuves scientifiques "
         "adéquates mais soutenue par les données disponibles et l'opinion des experts."),
    ], TCW, head=("Grille", "Définition")))
    story.append(Spacer(1, 2.5 * mm))
    story.append(theme_table([
        ("ILC / CVC", "Infection liée au cathéter / Cathéter veineux central"),
        ("AB / HC", "Antibiotique / Hémocultures"),
        ("SCN / BGN", "Staphylocoques à coagulase négative / Bacilles Gram négatif"),
        ("ETO", "Échographie transœsophagienne"),
    ], TCW, head=("Abréviation", "Signification")))
    return story

def _section_q1():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Question 1 — Sur quels éléments définir une infection sur CVC, et "
                    "quelle(s) technique(s) pour en affirmer le diagnostic ?"),
        Spacer(1, 1.5 * mm),
        P("L'infection liée au CVC est définie par la présence de micro-organismes à la "
          "surface interne et/ou externe du CVC, responsable d'une infection locale et/ou "
          "générale. Les signes cliniques locaux et/ou généraux peuvent s'accompagner ou "
          "non d'une hémoculture positive, et inversement. À l'exclusion du pus au point "
          "de ponction, aucun signe clinique ne permet à lui seul d'affirmer l'infection "
          "sur CVC" + tag("2-b") + " — le lien avec la présence de micro-organismes requiert "
          "des analyses microbiologiques.", S_BODY),
    ]))
    story.append(Spacer(1, 1.8 * mm))
    story.append(P(
        "<b>Techniques de culture du cathéter</b> (nécessitent son ablation) : la culture "
        "qualitative en milieu liquide ne distingue pas contamination, colonisation et "
        "infection, et doit être abandonnée" + tag("1-b") +
        ". D'autres méthodes existent : culture semi-quantitative sur milieu gélosé, ou "
        "culture quantitative en milieu liquide après rinçage endoluminal ou après "
        "« vortexage » ou sonication. Le seuil de la technique "
        "semi-quantitative (méthode de Maki, > 15 ufc) n'explore que la portion "
        "extraluminale et n'a été qu'incomplètement validé en réanimation. Le seuil "
        "> 10³ ufc/ml de la technique par « vortexage », déterminé à l'aide d'une "
        "classification clinique des malades bactériémiques ou non en réanimation, "
        "possède un meilleur rapport valeur diagnostique/coût et devrait être préférée"
        + tag("2-b") + ".", S_BODY))
    story.append(Spacer(1, 1.8 * mm))
    story.append(P(
        "Le taux élevé d'ablations injustifiées (3/4 des cathéters retirés à tort) a fait "
        "proposer des techniques « cathéter en place », envisageables uniquement en "
        "l'absence d'état de choc, de tunnelite, de thrombophlébite et d'endocardite" +
        tag("2-c") + " : la culture des prélèvements cutanés au site de ponction a une "
        "bonne valeur prédictive négative" + tag("1-b") + " (la surveillance systématique "
        "du point d'insertion, sans point d'appel infectieux, n'a en revanche aucune "
        "indication en routine" + tag("1-b") + ") ; un rapport de comptes bactériens > 5 "
        "entre hémoculture centrale et périphérique (hémocultures quantitatives "
        "simultanées) est prédictif et spécifique" + tag("2-b") + " ; un délai différentiel "
        "de positivation d'au moins 2 h en faveur de l'hémoculture centrale est hautement "
        "prédictif (sensibilité et spécificité > 90 %)" + tag("1-b") +
        " — pour les cathéters de courte durée (< 14 j, contamination surtout "
        "extraluminale), des études complémentaires restent nécessaires pour confirmer "
        "cette valeur diagnostique" + nr() + ". Les hémocultures par le cathéter seul ne "
        "permettent pas de diagnostiquer une ILC non bactériémique" + tag("2-c") + ".",
        S_BODY_SM))
    story.append(Spacer(1, 1.8 * mm))
    story.append(theme_table([
        ("ILC sans bactériémie" + tag("2-c"),
         "Culture de CVC ≥ 10³ ufc/ml, ET régression totale ou partielle des signes "
         "infectieux dans les 48 h suivant l'ablation, OU purulence de l'orifice d'entrée "
         "/ tunnelite."),
        ("ILC bactériémique" + tag("2-c"),
         "Bactériémie survenant dans les 48 h encadrant le retrait du CVC, ET (culture "
         "positive du site d'insertion au même germe, OU culture du CVC ≥ 10³ ufc/ml du "
         "même germe, OU rapport hémoculture centrale/périphérique ≥ 5, OU délai "
         "différentiel de positivité ≥ 2 h)."),
        ("Infection NON liée au CVC",
         "CVC stérile ; OU culture du CVC positive à une souche différente de celle du "
         "sang et/ou d'un autre foyer infectieux présent au moment de l'ablation du CVC, "
         "sans régression du syndrome infectieux à l'ablation ; OU culture du CVC "
         "positive à une souche identique à celle trouvée dans un autre foyer infectieux "
         "identifié au moins 48 h avant l'ablation du CVC — qu'il soit ou non "
         "responsable de bactériémie — sans régression du syndrome infectieux à "
         "l'ablation (colonisation secondaire à partir d'un foyer à distance)."),
    ], TCW, head=("Situation", "Critères")))
    return story

def _section_intro_q1():
    story = _section_intro()
    story.append(Spacer(1, 2 * mm))
    story.extend(_section_q1())
    return story

# ---------------------------------------------------------------------------
def _section_q2():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Question 2 — Importance relative des mécanismes impliqués dans les "
                    "ILC"),
        Spacer(1, 1.5 * mm),
        P("<b>Voies de contamination :</b> la voie cutanée (extraluminale) est la plus "
          "fréquente, survenant lors de la pose ou par colonisation secondaire du site "
          "d'insertion. La contamination endoluminale, secondaire aux manipulations "
          "septiques des raccords (exceptionnellement à un liquide de perfusion "
          "contaminé), devient prépondérante au-delà de 3 semaines de cathétérisme" +
          tag("2-b") + ". La voie hématogène est rare" + tag("2-b") + ".", S_BODY),
    ]))
    story.append(Spacer(1, 1.8 * mm))
    story.append(P(
        "<b>Mécanismes de colonisation :</b> le contact initial sang/cathéter entraîne "
        "l'adsorption de protéines plasmatiques (albumine, adhésines) à la surface du "
        "cathéter, puis la formation d'un réseau fibrino-plaquettaire colonisé "
        "progressivement par leucocytes et collagène, organisé en manchon. Des protéines "
        "plasmatiques et plaquettaires (fibrine, fibrinogène, fibronectine, vitronectine, "
        "laminine, thrombospondine, collagène) favorisent l'adhérence bactérienne, selon "
        "des mécanismes spécifiques partiellement connus, multiples et variables d'une "
        "bactérie à l'autre ; certaines bactéries adhèrent aussi de façon non spécifique en "
        "s'enchâssant dans une substance polysaccharidique (« slime »). In vitro, le "
        "polyuréthane et les élastomères de silicone sont les matériaux les moins propices "
        "à l'adhésion bactérienne.", S_BODY_SM))
    return story

def _section_q3():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Question 3 — Facteurs de risque, incidence, pronostic et conséquences "
                    "des ILC en réanimation"),
        Spacer(1, 1.5 * mm),
        P("<b>Incidence :</b> par leur fréquence et leur mortalité, les ILC font partie "
          "des 3 principales infections acquises en réanimation" + tag("1-b") +
          " ; les bactériémies liées aux CVC représentent 1/3 des bactériémies acquises "
          "en réanimation" + tag("1-b") + ". Les cocci à Gram positif (surtout SCN) sont "
          "actuellement la principale cause ; entérobactéries et Pseudomonas représentent "
          "environ 1/3 des cas, surtout en territoire cave inférieur.", S_BODY),
    ]))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "Densité d'incidence médiane en France : bactériémies primaires 3 à 9/1000 "
        "j-cathéter ; bactériémies liées au CVC 1 à 2/1000 j-cathéter ; cultures positives "
        "de CVC en moyenne 7/1000 j-cathéter. Chez l'enfant, densité proche de 5/1000 "
        "j-cathéter (grande disparité selon les unités, plus élevée en unités de brûlés). "
        "L'épidémiologie des infections sur cathéter de dialyse en réanimation est mal "
        "connue et justifie des études complémentaires.", S_BODY_SM))
    story.append(Spacer(1, 2 * mm))
    story.append(theme_table([
        ("Liés au patient",
         "Sexe masculin" + tag("3-b") + " ; immunodépression" + tag("3-c") +
         " ; surtout la densité des soins" + tag("2-b") + " (facteurs mal évalués dans la "
         "littérature)."),
        ("Liés à la pose",
         "Polyuréthane/élastomères de silicone → moins d'ILC que le PVC. Voies fémorale "
         "et probablement jugulaire interne : risque supérieur à la voie sous-clavière" +
         tag("1-a") + " (non démontré chez l'enfant" + nr() +
         " ; chez l'adulte, aucune étude ne démontre la supériorité de la jugulaire "
         "interne sur la fémorale" + tag("2-b") + "). Asepsie chirurgicale à la pose : "
         "moins d'ILC en son absence" + tag("1-a") + "."),
        ("Liés à l'utilisation",
         "Fréquence des manipulations de la ligne" + tag("2-c") +
         ". Antibioprophylaxie à la pose : ne réduit pas le risque" + tag("2-a") +
         " ; antibiotiques IV pendant l'insertion : risque moindre" + tag("2-b") +
         ". Durée de cathétérisme : risque cumulé croissant" + tag("1-b") +
         " (risque instantané probablement non constant, possiblement croissant pour les "
         "cathéters de longue durée" + tag("3-c") +
         "). Cathéters artériels pulmonaires : risque accru au-delà du 4<sup>e</sup> jour" +
         tag("2-b") + "."),
    ], TCW, head=("Facteurs de risque", "Détail")))
    story.append(Spacer(1, 2 * mm))
    story.append(P(
        "<b>Morbidité, mortalité :</b> les ILC bactériémiques sont associées à une "
        "augmentation du risque de décès en réanimation estimée entre 4 et 20 %, et à une "
        "prolongation de séjour de 5 à 20 jours" + tag("1-b") +
        " (estimation rendue difficile par de nombreux facteurs confondants — gravité et "
        "évolution des patients, adéquation de l'antibiothérapie" + tag("1-b") +
        "). Les conséquences sont plus importantes en cas d'infection à <i>Staphylococcus "
        "aureus</i>, <i>Pseudomonas sp.</i> et <i>Candida sp.</i>" + tag("1-b") + ".",
        S_BODY_SM))
    return story

def _section_q2_q3():
    story = _section_q2()
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_q3())
    return story

# ---------------------------------------------------------------------------
def _section_q4():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Question 4 — Méthodes de prévention de l'ILC recommandées en "
                    "réanimation"),
        Spacer(1, 1.5 * mm),
        P("<b>5.1 — Choix du matériel :</b> l'emploi de matériaux moins thrombogènes "
          "(polyuréthane, élastomère de silicone) est recommandé" + tag("1-b") +
          ". Les cathéters imprégnés d'héparine n'ont pas fait la preuve de leur "
          "efficacité anti-infectieuse chez l'adulte" + tag("2-b") +
          " (ils diminuent le risque de thrombose" + tag("1-a") +
          "). Chez l'enfant, les données disponibles suggèrent que le recours à des "
          "modèles imprégnés d'héparine et/ou à une héparinisation des solutions de "
          "perfusion réduit les complications thrombotiques et les bactériémies pour "
          "les cathéters de petit diamètre (< 5 Fr) par voie fémorale" + tag("2-b") + ".",
          S_BODY_SM),
    ]))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>5.2 — Cathéters imprégnés d'antibiotiques/antiseptiques :</b> l'imprégnation "
        "par chlorhexidine-sulfadiazine argent ou association minocycline-rifampicine "
        "diminue le risque d'infection de moitié" + tag("1-a") +
        ". Cependant, quoique non démontré, ce type de matériau pourrait favoriser "
        "l'émergence de bactéries résistantes" + tag("2-c") +
        " — en particulier la rifampicine à dose sub-inhibitrice (antibiotique majeur en "
        "cas d'infection sur prothèse)" + tag("1-b") +
        ". En conséquence, l'utilisation de cathéters imprégnés d'agents anti-infectieux "
        "n'est pas recommandée en première intention ; celle des cathéters imprégnés de "
        "chlorhexidine-sulfadiazine argent est réservée aux unités où l'incidence des ILC "
        "reste élevée malgré le renforcement des mesures préventives non anti-infectieuses"
        + tag("2-c") + " (cathéters imprégnés d'antibiotiques : études complémentaires "
        "nécessaires" + nr() + ").", S_BODY_SM))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>5.3 — Technique de pose :</b> asepsie chirurgicale, y compris lors des "
        "échanges sur guide" + tag("1-a") +
        ". Peau détergée au savon antiseptique puis badigeonnée (povidone iodée, "
        "chlorhexidine ou alcool)" + tag("1-a") +
        " ; contact jusqu'à peau sèche, ≥ 2 min pour la polyvidone iodée" + tag("1-b") +
        ". Solvants (acétone…) déconseillés avant insertion/pansements" + tag("1-a") +
        ". Champs stériles larges" + tag("1-a") +
        ". La tunnelisation diminue le risque pour les cathéters jugulaires internes et "
        "fémoraux" + tag("1-a") + " (sans intérêt pour les sous-claviers" + tag("2-a") +
        "). Changement sur guide : mêmes conditions que la pose initiale" + tag("2-c") +
        ", gants stériles changés à la mise en place du nouveau cathéter" + tag("2-c") +
        ". Le changement systématique à intervalle régulier (sur guide ou nouveau site) "
        "est à proscrire" + tag("1-a") +
        ". Le risque des cathéters multilumières n'est pas supérieur à celui des "
        "monolumières dans les études randomisées" + tag("2-a") + ".", S_BODY_SM))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>5.4 — Site d'accès vasculaire :</b> la voie sous-clavière est préférée dès que "
        "la durée prévue dépasse 5-7 j, si le risque de barotraumatisme/ponction "
        "artérielle non compressible n'est pas trop important" + tag("1-a") +
        ". Si le risque mécanique est élevé, la voie jugulaire interne peut être "
        "envisagée" + tag("2-b") + " (tunnelisation alors recommandée" + tag("1-a") +
        "). La voie fémorale est discutée si le risque cave supérieur est élevé "
        "(tunnelisation recommandée)" + tag("2-a") +
        ". La voie axillaire mérite une évaluation complémentaire.",
        S_BODY_SM))
    return story

def _section_q4b():
    story = []
    story.append(Spacer(1, 2 * mm))
    story.append(P(
        "<b>5.5 — Pansement du site d'insertion :</b> l'efficacité de l'occlusion du site "
        "est démontrée" + tag("1-a") +
        " ; le type de pansement n'est pas décisif, mais un pansement semi-perméable "
        "transparent permet la surveillance visuelle/manuelle. L'intérêt des éponges "
        "imprégnées de chlorhexidine n'est pas tranché" + nr() +
        ". Intervalle optimal de changement : au moins 72 h. Dates de pose et de "
        "réfection notées. Le site d'insertion du cathéter doit être surveillé "
        "quotidiennement" + tag("2-c") + ".", S_BODY_SM))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>5.6 — Choix de l'antiseptique :</b> une méta-analyse récente suggère la "
        "supériorité de la chlorhexidine sur la povidone iodée" + tag("1-a") +
        " (chlorhexidine souvent fortement dosée ou associée à l'alcool dans les études "
        "incluses" + tag("2-a") + "). La povidone iodée-alcool semble supérieure à la "
        "povidone iodée seule" + tag("2-a") +
        " ; aucune étude n'a comparé povidone iodée-alcool et chlorhexidine-alcool" +
        nr() + ".", S_BODY_SM))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>5.7 — Entretien de la ligne veineuse :</b> limiter les manipulations" +
        tag("2-b") + ". L'éloignement des sites d'injection (prolongateur non changé) "
        "réduit la contamination" + tag("2-b") +
        ". Intervalle optimal de changement de ligne : 2 à 3 j" + tag("1-b") +
        " (délais plus longs, 4 à 7 j, suggérés par certaines études, à confirmer en "
        "réanimation" + tag("2-b") +
        "). Remplacer les tubulures ayant servi à des dérivés sanguins ou lipides (y "
        "compris propofol" + tag("2-b") + ") dans les 24 h" + tag("2-c") +
        ". L'efficacité des filtres antimicrobiens n'est pas démontrée" + tag("1-a") +
        ". L'héparinisation générale diminue le risque de thrombose sur CVC" + tag("1-a") +
        " (effet sur le risque infectieux suggéré par une méta-analyse mais non démontré"
        + nr() + ").", S_BODY_SM))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>5.8 — Politique générale de prévention :</b> limiter les indications de pose "
        "des CVC et cathéters de Swan-Ganz, ablation la plus précoce possible" +
        tag("1-b") + ". Protocoles écrits pour la pose, l'entretien et l'utilisation, "
        "élaborés en équipe et respectés par tous" + tag("1-b") +
        ". Les facteurs de risque étant essentiellement exogènes, cette infection "
        "nosocomiale se prête particulièrement aux programmes d'amélioration continue de "
        "la qualité : impact démontré d'équipes formées à la prise en charge des "
        "cathéters" + tag("1-a") +
        " et de programmes d'éducation, comportant une formation aux bonnes pratiques "
        "d'hygiène et des directives précises sur la pose des différents accès "
        "vasculaires (préparation du matériel, désinfection de la peau, précautions "
        "stériles maximales, techniques détaillées d'insertion), sur leur utilisation "
        "(désinfection systématique des mains, manipulations des rampes) et sur les "
        "soins qui leur sont apportés (schéma de remplacement, type et fréquence de "
        "réfection des pansements)" + tag("1-b") + ".", S_BODY_SM))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>5.9 — Cathéter de Swan-Ganz et cathéter artériel :</b> toutes les règles "
        "précédentes s'appliquent. Le site jugulaire est préférable au sous-clavier pour "
        "la surveillance hémodynamique péri-opératoire par Swan-Ganz (balance risque "
        "infectieux/complications mécaniques). Manchons plastifiés protecteurs "
        "recommandés" + tag("2-a") +
        ". Le changement systématique du Swan-Ganz ou des cathéters artériels n'est pas "
        "recommandé" + tag("2-c") +
        ". Sets de pression à usage unique préférables" + tag("2-b") +
        " ; systèmes d'injection clos pour les bolus (Swan-Ganz et système Picco®)" +
        tag("2-c") + ". Pas de soluté glucosé pour la purge des sets de pression" +
        tag("1-b") + ". Changement de l'ensemble tubulures/set de pression/robinet tous "
        "les 4 j" + tag("2-b") + ".", S_BODY_SM))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>5.10 — Cathéters de dialyse :</b> très peu de données en réanimation. "
        "Utilisation pour perfusion/prélèvement sanguin hors séances de dialyse non "
        "recommandée" + tag("2-c") + ". Changement systématique non recommandé" +
        tag("2-b") + ".", S_BODY_SM))
    return story

def _section_q4_full():
    # Merged onto shared pages: 5.1-5.4 alone left substantial whitespace, and
    # 5.5-5.10 alone would too - combined per the <60%-full merge rule
    # (CLAUDE.md build pipeline, step 7).
    story = _section_q4()
    story.append(Spacer(1, 2 * mm))
    story.extend(_section_q4b())
    return story

# ---------------------------------------------------------------------------
# Figure 1 (source page 7) - full-page decision algorithm, no reliable text
# layer - rendered at 250dpi and transcribed as an Etape/Situation/Conduite
# table, branching logic traced arrow-by-arrow.
FIG1_ROWS = [
    ("1 — Suspicion d'ILC, état de choc / sepsis sévère / écoulement purulent "
     "(tunnelite)",
     "Ablation immédiate du cathéter + antibiothérapie probabiliste (vancomycine ± "
     "β-lactamines + aminosides ; évaluer l'intérêt d'un antifongique) → culture du "
     "cathéter."),
    ("1 — Suspicion d'ILC, pas de signe de gravité",
     "Selon la stratégie retenue : échange du cathéter sur guide (→ culture du "
     "cathéter) OU culture du point de ponction."),
    ("2 — Culture du point de ponction négative",
     "Surveillance ; recherche d'un autre site infecté (± changement sur guide)."),
    ("2 — Culture du point de ponction positive",
     "Hémocultures périphérique + centrale couplées (ratio quantitatif > 5:1 et/ou "
     "délai de positivité > 2 h)."),
    ("3 — Hémocultures couplées négatives (ratio ≤ 5:1 et délai ≤ 2 h)",
     "Recherche d'une autre infection."),
    ("3 — Hémocultures couplées positives (ratio > 5:1 et/ou délai > 2 h)",
     "I.L.C. certaine."),
    ("4 — Culture du cathéter négative (après ablation ou échange sur guide)",
     "Recherche d'une autre infection."),
    ("4 — Culture du cathéter positive, résultat des hémocultures négatif "
     "(ablation du CVC si échange sur guide)",
     "« Amélioration après ablation du CVC ? »"),
    ("4 — Culture du cathéter positive, résultat des hémocultures positif",
     "I.L.C. certaine."),
    ("5 — Pas d'amélioration après ablation du CVC",
     "Probable colonisation (pas d'ILC)."),
    ("5 — Amélioration après ablation du CVC",
     "Probable I.L.C."),
    ("6 — Probable I.L.C. — S. aureus, Pseudomonas",
     "Antibiothérapie ~7 j (durée proposée avec réserve dans le schéma source)."),
    ("6 — Probable I.L.C. — SCN, BGN, Candida sp.",
     "Pas d'antibiothérapie sauf immunodépression ou maladie valvulaire ; alternative : "
     "pas d'antibiothérapie mais surveillance rapprochée et hémocultures répétées."),
    ("6 — I.L.C. certaine — S. aureus (ETO obligatoire), Pseudomonas, A. baumannii, "
     "champignon",
     "Ablation du CVC + antibiothérapie 14-21 j."),
    ("6 — I.L.C. certaine — SCN, autre BGN",
     "Ablation du CVC + antibiothérapie < 7 j, OU maintien du CVC + antibiothérapie "
     "14-21 j."),
    ("7 — Persistance du sepsis > 3 j, ou hémocultures positives > 3 j",
     "ETO obligatoire (adulte) ; recherche d'une infection profonde ; si endocardite → "
     "antibiothérapie 4-6 semaines ; si thrombophlébite → antibiothérapie 4-6 semaines ; "
     "si ostéomyélite → antibiothérapie 6-8 semaines."),
]

def _section_q5():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Question 5 — Stratégie diagnostique et thérapeutique initiale en cas "
                    "de présomption d'infection sur CVC"),
        Spacer(1, 1.5 * mm),
        P("L'attitude diagnostique et le traitement initial résultent de la confrontation "
          "des signes locaux, des manifestations cliniques générales et des résultats "
          "microbiologiques (locaux et hémocultures — prélevées systématiquement, au "
          "minimum en périphérie, de préférence simultanément par le cathéter, devant "
          "toute suspicion). Certains facteurs de risque doivent également être pris en "
          "compte, comme la durée de maintien du cathéter et le site d'implantation ; "
          "l'évolution des signes cliniques (persistance, aggravation) et la nature du "
          "ou des micro-organismes en cause doivent être intégrées dans les choix "
          "thérapeutiques. Deux questions se posent initialement : faut-il retirer le "
          "cathéter suspect ? faut-il prescrire une antibiothérapie ? En pratique, la "
          "stratégie initiale dépend de la présence de signes locaux d'une part et de la "
          "sévérité du syndrome septique d'autre part.", S_BODY),
    ]))
    story.append(Spacer(1, 1.8 * mm))
    story.append(P(
        "<b>6.1.1 — L'ablation immédiate</b> d'un cathéter présumé infecté s'impose : en "
        "présence de signes locaux francs (cellulite, tunnelite, collection purulente)" +
        tag("1-b") + " ; en cas d'infection compliquée d'emblée (thrombophlébite, "
        "endocardite" + tag("1-b") + " ; germes à haut risque — bactériémie à <i>S. "
        "aureus</i>, <i>Pseudomonas</i> ou <i>Candida</i>" + tag("1-b") +
        ") ; devant des signes de gravité (choc septique) sans autre cause apparente" +
        tag("1-b") + " ; en cas de bactériémie chez un porteur de prothèse endovasculaire "
        "ou de valve cardiaque" + tag("1-c") + " ou immunodéprimé" + nr() + ".",
        S_BODY_SM))
    story.append(Spacer(1, 1.8 * mm))
    story.append(P(
        "<b>6.1.2 — En l'absence de signes locaux et généraux de gravité,</b> plusieurs "
        "attitudes sont possibles (dans ces situations à présomption faible/modérée, la "
        "probabilité de retirer à tort un cathéter stérile est très élevée, 80 % des "
        "cas" + tag("1-b") + " — la nécessité d'implanter un nouveau cathéter sur un "
        "autre site exposant par ailleurs à des risques de complications mécaniques non "
        "négligeables) : le changement de cathéter sur guide (confirme/infirme "
        "en conservant l'abord vasculaire, solution temporaire en attendant 24 h les "
        "résultats microbiologiques, surtout justifiée si suspicion faible/modérée ou "
        "germe à faible risque) ; ou une attitude conservatrice (cathéter laissé en "
        "place, au moins dans un premier temps) : prélèvements locaux — du site "
        "d'insertion, du pavillon — qui, lorsqu'ils sont négatifs, permettent d'éliminer "
        "l'infection, et/ou hémocultures couplées du sang prélevé en périphérie et par "
        "le cathéter.", S_BODY_SM))
    story.append(Spacer(1, 1.8 * mm))
    story.append(P(
        "<b>6.2 — Antibiothérapie et conduite selon les résultats microbiologiques :</b> "
        "en présence de signes de gravité (sepsis sévère, choc), de complications "
        "(tunnelite, thrombophlébite, endocardite) ou de signes locaux patents "
        "(suppuration), une antibiothérapie probabiliste est débutée immédiatement " +
        tag("1-b") + " (dirigée notamment contre les Gram positifs, guidée par l'examen "
        "direct et l'écologie, réévaluée à réception des résultats définitifs" +
        tag("1-b") + "). Si l'infection est confirmée avec hémocultures positives à un "
        "germe à haut risque (<i>S. aureus</i>, <i>Candida sp.</i>, <i>Pseudomonas sp.</i>, "
        "Coryné JK, <i>Bacillus sp.</i>), le cathéter est enlevé s'il ne l'a pas déjà été et "
        "le traitement adapté est poursuivi.", S_BODY_SM))
    story.append(Spacer(1, 1.8 * mm))
    story.append(P(
        "En cas de septicémie à <i>S. aureus</i>, une échocardiographie transœsophagienne "
        "(transthoracique chez le jeune enfant) est recommandée pour vérifier l'état "
        "valvulaire" + tag("1-b") +
        " (fréquence d'endocardite associée estimée entre 5 et 20 %), avec un Doppler "
        "veineux. Sans lésion valvulaire ni thrombophlébite, et si le contrôle de "
        "l'infection est rapide (hémocultures négativées et régression en 48-72 h), un "
        "traitement « court » (10-14 j) paraît suffisant" + tag("1-b") +
        " (complications → traitement plus prolongé, cf. Figure 1). Pour "
        "<i>Acinetobacter baumannii</i> et les entérobactéries du groupe III, les données "
        "sont insuffisantes mais suggèrent un traitement" + tag("3-c") + ".", S_BODY_SM))
    story.append(Spacer(1, 1.8 * mm))
    story.append(P(
        "<b>6.2.3 — Bactériémie à staphylocoque à coagulase négative</b> (probablement "
        "liée au cathéter) : l'attitude la plus sûre est l'ablation du cathéter — une "
        "bactériémie isolée avec régression rapide après ablation ne nécessite pas "
        "nécessairement d'antibiothérapie, en l'absence de facteurs de risque associés" +
        tag("2-c") + ". Un changement sur guide, voire un maintien en place sous "
        "antibiothérapie adaptée, peut être envisagé (attitude fréquente en cas de "
        "cathéter d'alimentation parentérale prolongée ou en hémato-cancérologie) — la "
        "méthode du « verrou antibiotique » n'a toutefois pas été évaluée en réanimation "
        "et n'a pas d'indication reconnue dans ce contexte" + tag("2-c") +
        " (même raisonnement probable pour entérobactéries du groupe I/II et "
        "entérocoques" + tag("3-c") + ").", S_BODY_SM))
    story.append(Spacer(1, 1.8 * mm))
    story.append(P(
        "<b>6.2.4 — En l'absence de bactériémie, de signes de gravité et de germe à haut "
        "risque</b> (recommandations fondées sur avis d'experts, aucune étude ne permet "
        "de répondre formellement) : une infection locale non compliquée nécessite un "
        "traitement local désinfectant et une surveillance après retrait — la régression "
        "rapide (48 h) peut constituer le seul traitement, sous surveillance attentive et "
        "en l'absence d'immunodépression" + tag("2-c") +
        " (antibiothérapie généralement non nécessaire, sauf signes généraux francs "
        "d'emblée ou aggravation/réapparition de signes dans les 48 h, durée alors "
        "inconnue). Si un changement sur guide a été fait : remplacement sur nouveau site "
        "si colonisation significative du 1<sup>er</sup> cathéter (antibiothérapie "
        "généralement non nécessaire sans bactériémie) ; si SCN isolé sur le 1<sup>er</sup> "
        "cathéter, le 2<sup>e</sup> peut être laissé en place sous antibiothérapie, "
        "surveillance renforcée, retrait imposé si persistance des signes généraux" +
        tag("2-c") + ". Cathéter laissé en place (présomption faible/modérée), sans "
        "suppuration/bactériémie/signe de gravité : surveillance simple, antibiothérapie "
        "non recommandée, prélèvements renouvelés au moindre doute. Dans tous les cas, la "
        "recherche d'un autre foyer infectieux est nécessaire.", S_BODY_SM))
    story.append(Spacer(1, 3 * mm))
    story.append(KeepTogether([
        P("<b>Figure 1 — Algorithme décisionnel</b> (reproduit en tableau Étape/"
          "Situation/Conduite depuis le schéma source, page 7)", S_CELL_B),
        Spacer(1, 1 * mm),
    ]))
    story.append(theme_table(FIG1_ROWS, TCW, head=("Étape / Situation", "Conduite")))
    return story

def _section_sources():
    story = []
    story.append(section_bar("Sources et traçabilité", color=GREY))
    story.append(Spacer(1, 2 * mm))
    story.append(P(
        "<b>Document source :</b> « Réactualisation de la douzième conférence de "
        "consensus de la Société de réanimation de langue française (SRLF) : infections "
        "liées aux cathéters veineux centraux en réanimation ». J.-F. Timsit, service de "
        "réanimation médicale et infectieuse, hôpital Bichat-Claude-Bernard, Paris. "
        "Réanimation 12 (2003) 258-265. DOI: 10.1016/S1624-0693(03)00051-3.", S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>Comité d'organisation pour la révision :</b> Chargés de projet — adulte : "
        "J.-F. Timsit ; pédiatrie : P. Durand. Responsables pour la commission des "
        "référentiels : B. Guidet, R. Robert, M. Wolff, S. Leteurtre. Experts — adulte : "
        "G. Nitenberg ; pédiatrie : C. Dagueville. Membres de l'ancien jury : G. Bleichner, "
        "Y. Letulzo, M. Pinsard. Experts extérieurs : J.C. Lucet, B. Souweine, L. Soufir, "
        "P. Longuet, J. Merrer, A. Lepape, F. Blot, C. Martin, G. Nitenberg, O. Mimoz, "
        "Ph. Eggiman, G. Colas, C. Brun-Buisson.", S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P("<b>Version :</b> reçu et accepté le 11 décembre 2002, publié 2003 — "
                    "réactualisation de la 12<sup>e</sup> conférence de consensus SRLF de "
                    "1994. Le texte final a été validé par un groupe de lecture désigné "
                    "par la SRLF ; les textes des experts et la bibliographie complète "
                    "sont disponibles sur srlf.org.", S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P("<b>Méthodologie :</b> grille Niveau (1-3) - Score d'évaluation (a-d), "
                    "légende publiée intégralement par la source — voir page 1. Analyse de "
                    "la bibliographie et niveau des recommandations selon la méthodologie "
                    "publiée en référence [2].", S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>URL source :</b> https://sfar.org/wp-content/uploads/2015/10/"
        "1-s2.0-S1624069303000513-main.pdf", S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P("<b>Référence citée [1] :</b> Bleichner G, Beaucaire G, Gottot S, "
                    "Letulzo Y, Marty J, Minet M, et al. Infections liées aux cathéters "
                    "veineux en réanimation — Douzième conférence de consensus en "
                    "réanimation et médecine d'urgence. Rean Urg 1994;3:321-30.",
                    S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P("<b>Référence citée [2] :</b> Procédures de révision des "
                    "recommandations (conférences de consensus, recommandations pour la "
                    "pratique clinique). Réanim Urg 1998;7:357-9.", S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P("<b>Couverture :</b> cette fiche reprend l'intégralité des 5 questions "
                    "(définition/diagnostic ; mécanismes ; facteurs de risque/incidence/"
                    "morbi-mortalité ; prévention 5.1-5.10 ; stratégie diagnostique et "
                    "thérapeutique 6.1-6.2.4), la Figure 1 (algorithme, transcrite en "
                    "tableau depuis un rendu visuel) et le glossaire des abréviations.",
                    S_SOURCE))
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Avertissement — document de 2003 :</b> ce document est une fiche de synthèse "
        "indépendante, produite pour un usage d'aide-mémoire. Elle reprend l'intégralité "
        "des informations du texte source (dont la Figure 1, transcrite depuis un rendu "
        "visuel du PDF faute de couche texte fiable), mais ne remplace pas le texte "
        "intégral (argumentaire complet, bibliographie disponible sur srlf.org) et n'est "
        "ni éditée ni validée par la SRLF. Les pratiques de prévention et de traitement "
        "des ILC ayant évolué depuis 2003 (matériel, recommandations plus récentes), se "
        "référer à un avis spécialisé et aux recommandations actualisées avant toute "
        "décision.", S_BODY_SM), bg=GREY_LIGHT, border=GREY))
    return story

def _section_q5_sources():
    story = _section_q5()
    story.append(Spacer(1, 4 * mm))
    story.extend(_section_sources())
    return story

def _section_intro_q1_q2_q3():
    # Merged onto one page-group: intro/legende/glossaire/Q1 alone left most of
    # a page white (a single orphaned table row on its own page), and Q2/Q3
    # alone left a page ~40% white - combined per the <60%-full merge rule
    # (CLAUDE.md build pipeline, step 7).
    story = _section_intro_q1()
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_q2_q3())
    return story

def _section_q4_q5_sources():
    # Merged onto shared pages (no forced page break): Q5+sources alone left
    # its final page (the closing warning panel) almost empty - combined with
    # Q4 per the <60%-full merge rule (CLAUDE.md build pipeline, step 7).
    story = _section_q4_full()
    story.append(Spacer(1, 3 * mm))
    story.extend(_section_q5_sources())
    return story

SECTIONS = [
    ("Méthodologie, glossaire, Q1, Q2 & Q3", _section_intro_q1_q2_q3),
    ("Q4 & Q5 — Prévention, stratégie diagnostique/thérapeutique, Figure 1 & sources",
     _section_q4_q5_sources),
]
# NOTE on page-fill: both a 2-section merge (Q4+Q5+sources sharing pages) and
# a full single-section merge (entire document, no forced breaks at all) were
# tried and rebuilt to close the ~20%-full final page (the closing
# Avertissement panel alone) - both left the page count and the final page's
# fill UNCHANGED (6 pages either way), because the preceding pages (Q3's
# tail, Q4's single dense page) were already close to full and had no slack
# to absorb it. Reverted to the 2-section version for accurate per-page
# subtitles (a full merge would show one generic title across all 6 pages).
# Per CLAUDE.md build pipeline step 7 ("revert if it doesn't help"): a
# ~20%-full closing disclaimer/sources page is accepted as-is, consistent
# with the trailing whitespace already accepted on other fiches' final pages
# in this corpus (e.g. fiche_candidoses_aspergilloses's own closing page).

def _make_doc(path=None):
    return SimpleDocTemplate(path or OUT, pagesize=A4,
                              leftMargin=MARGIN, rightMargin=MARGIN,
                              topMargin=32 * mm, bottomMargin=16 * mm,
                              title="Fiche SRLF 2003 - Infections liees aux catheters "
                                    "veineux centraux en reanimation",
                              author="Synthèse indépendante (source SRLF)")

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
