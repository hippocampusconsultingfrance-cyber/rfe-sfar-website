# -*- coding: utf-8 -*-
"""
Fiche de synthese - Societe Francaise d'Anesthesie et de Reanimation (SFAR).
"Echographie en anesthesie locoregionale" - Recommandations Formalisees
d'Experts (RFE), 2011. Auteurs : H. Bouaziz, F. Aubrun, A.A. Belbachir,
P. Cuvillon, E. Eisenberg, D. Jochum, C. Aveline, P. Biboulet, M. Binhas,
S. Bloc, G. Boccara, M. Carles, O. Choquet, L. Delaunay, J.-P. Estebe,
R. Fuzier, E. Gaertner, A. Gnaho, K. Nouette-Gaulain, E. Nouvellon, J. Ripart,
V. Tubert. Ann Fr Anesth Reanim 30 (2011) e33-e35 (doi:10.1016/j.annfar.
2011.06.008). 3 pages, telecharge depuis sfar.org (wp-content/uploads/2015/
10/2_AFAR_echographie-en-anesthesie-locoregionale.pdf).

METHODOLOGIE - CONVENTION BESPOKE (9e distincte de ce corpus) : texte
narratif SANS numerotation R1/R2 et SANS grille GRADE/RAND imprimee - la
force de chaque enonce est portee par une locution modale entre guillemets
dans le texte source lui-meme, avec TROIS niveaux distincts (pas les 4 de
hospit_ambulatoire) : « il est recommande »/« est recommande(s) » (force
pleine), « il est probablement recommande »/« est probablement
recommandee » (force intermediaire/probable, explicitement distinguee de la
recommandation pleine par la source), et deux occurrences de « il est
possible » (permissif/qualifie) : l'abord sciatique par voie glutaire
(techniquement plus difficile), et la realisation d'un bloc chez un
patient sous anesthesie/sedation - cette derniere etait a l'origine dans la
meme phrase source que la recommandation "probablement recommande" sur le
patient eveille, mais porte une force differente (permissif vs
probable) : scindee en 2 lignes distinctes plutot que fusionnee en un
chip composite, conformement a la regle de projet sur les grades
composites. Aucune occurrence de forme negative
(« non recommande ») dans ce texte. Chips deduits directement et
exhaustivement des locutions modales du texte source, jamais inventes -
legende explicite en page 1. Couleur neutre (gris), meme principe que les
autres conventions bespoke de ce corpus faute de correspondance avec les
couleurs GRADE standard.

COUVERTURE : integralite des enonces de recommandation du texte narratif
(introduction/contexte, regles generales et apprentissage, materiel et
aspect technique, regles de securite, blocs des membres et du tronc,
conditions de realisation et hygiene), y compris le Tableau 1 (classement
des dispositifs medicaux et niveaux de traitement requis) reproduit
verbatim. Enonces non modalises (ex. equivalence de taux de succes
echographie/neurostimulation pour le bloc supraclaviculaire) rapportes
comme contexte descriptif, pas comme lignes de recommandation gradees,
conformement a la regle de projet de ne jamais inventer un grade absent de
la source.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from style import *
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.units import mm

OUT = "/home/user/rfe-sfar-website/output/Fiche_SFAR_Echographie_Anesthesie_Locoregionale_2011.pdf"

SOURCE_TXT = ("Source : « Échographie en anesthésie locorégionale » — RFE SFAR, "
              "Ann Fr Anesth Réanim 30 (2011) e33-e35. Fiche de synthèse non "
              "officielle : se référer au texte intégral.")

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

def reco_table(rows, col_widths):
    """rows: (text, force_label) ou force_label in {'R','PR','P'}."""
    data = [[P("Recommandation", S_HEAD_W), P("Force", S_HEAD_W_C)]]
    for txt, force in rows:
        data.append([P(txt, S_CELL), chip(force)])
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

RCW = [CW_FULL - 14 * mm, 14 * mm]
TCW = [46 * mm, CW_FULL - 46 * mm]

def legend_flowable():
    chip_w = 18 * mm
    content_w = CW_FULL
    row = Table([[chip("R", width=chip_w - 2 * mm), chip("PR", width=chip_w - 2 * mm),
                  chip("P", width=chip_w - 2 * mm),
                  P("<b>Force</b> (déduite des locutions modales du texte, aucune grille "
                    "de cotation imprimée) — <b>R</b> = « il est recommandé » (force pleine) ; "
                    "<b>PR</b> = « il est probablement recommandé » (force intermédiaire, "
                    "distinguée par la source elle-même) ; <b>P</b> = « il est possible » "
                    "(permissif/qualifié). Aucune occurrence de forme négative dans ce texte.",
                    S_BADGE_HEAD)]],
                colWidths=[chip_w, chip_w, chip_w, content_w - 3 * chip_w])
    row.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                              ("LEFTPADDING", (0, 0), (-1, -1), 1),
                              ("RIGHTPADDING", (0, 0), (-1, -1), 1),
                              ("TOPPADDING", (0, 0), (-1, -1), 0),
                              ("BOTTOMPADDING", (0, 0), (-1, -1), 0)]))
    return row

TOTAL_PAGES = {"n": 4}

def on_page(canvas, doc, page_title):
    header_band(canvas, doc, "SFAR — RFE, 2011",
                "Échographie en anesthésie locorégionale",
                page_title, icon_fn=lambda c, x, y: icon_shield(c, x, y, 13 * mm), color=TEAL_DARK)
    footer_band(canvas, doc, SOURCE_TXT, f"Page {doc.page} / {TOTAL_PAGES['n']}")

# ---------------------------------------------------------------------------
def _section_intro():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Résumé :</b> Recommandations Formalisées d'Experts SFAR (2011) sur "
        "l'utilisation de l'échographie en anesthésie locorégionale (ALR) — règles "
        "générales et apprentissage, matériel et aspect technique, règles de sécurité, "
        "application aux blocs des membres et du tronc, conditions de réalisation et "
        "hygiène (dont le classement des dispositifs médicaux, Tableau 1).",
        S_BODY), bg=GREY_LIGHT, border=GREY))
    story.append(Spacer(1, 2.5 * mm))
    story.append(P(
        "L'introduction de l'échographie en ALR est un événement récent qui suppose "
        "une formation préalable et un matériel spécifique que ne possèdent pas tous "
        "les médecins anesthésistes-réanimateurs. <b>La publication de ce référentiel "
        "ne signifie pas que le non-recours à l'échographie constitue une mauvaise "
        "pratique médicale — la neurostimulation reste une technique de repérage "
        "validée.</b> Ce référentiel complète les recommandations pour la pratique "
        "clinique de 2002 sur les blocs périphériques des membres chez l'adulte et "
        "celles de 2006 sur les blocs périmédullaires, sans les remplacer.",
        S_BODY_SM))
    story.append(Spacer(1, 3 * mm))
    story.append(legend_flowable())
    return story

def _section_generalites():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Règles générales, apprentissage et procédure de réalisation"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("La compréhension des bases physiques des ultrasons et des réglages de "
         "l'échographe, pour l'exécution des blocs périphériques sous échographie "
         "avec assurance et sécurité.", "R"),
        ("Avoir des connaissances anatomiques et de sonoanatomie pour identifier les "
         "structures concernées : muscles, vaisseaux, nerfs, tendons, fascias, os, "
         "plèvre.", "R"),
        ("Un entraînement préalable pour l'acquisition de la sonoanatomie (mannequin) "
         "et la visualisation de l'aiguille jusqu'à sa cible (fantômes et/ou pièces "
         "anatomiques). La compréhension des techniques de guidage de l'aiguille "
         "« dans le plan » et « en dehors du plan » est un prérequis pour la sécurité "
         "et le succès de l'exécution d'une ALR.", "R"),
        ("Suivre sa propre courbe d'apprentissage, en raison de la variabilité "
         "interindividuelle dans la rapidité d'acquisition de la technique.", "R"),
        ("Des moyens complémentaires pour la réalisation du bloc : la "
         "neurostimulation et/ou l'hydrolocalisation et/ou l'hydrodissection et/ou "
         "le déplacement des tissus avec les mouvements de l'aiguille.", "R"),
        ("En cas de difficulté de visualisation de la sonoanatomie, associer la "
         "neurostimulation à l'échoguidage.", "R"),
    ], RCW))
    return story

def _section_materiel():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Matériel et aspect technique"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("Disposer de sondes de fréquence et de forme adaptées à l'anesthésie "
         "réalisée ; le choix de la sonde dépend du type de bloc et de la profondeur "
         "de la cible.", "R"),
        ("Utiliser la fréquence la plus élevée possible, pour privilégier la "
         "résolution spatiale et améliorer la précision de l'image.", "R"),
        ("Utiliser les différentes fonctions proposées par l'échographe et adapter "
         "leurs réglages à l'image native et à la profondeur de la cible : gains "
         "général et étagé, profondeur étudiée, nombre et position des focales, "
         "imagerie multi-incidence, mode Doppler.", "R"),
        ("Réaliser, avant le geste anesthésique, une visualisation large et dynamique "
         "des éléments anatomiques en recherchant précisément les structures cibles "
         "et adjacentes — permet de planifier la trajectoire de l'aiguille et de "
         "déterminer le plan de visualisation du nerf (petit et/ou grand axe).", "R"),
        ("Visualiser les nerfs cibles en « petit axe » pour les blocs superficiels "
         "et profonds. Le choix d'approche de l'aiguille (dans le plan ou en dehors "
         "du plan) est indépendant de la profondeur de la cible.", "PR"),
        ("Utiliser des aiguilles dédiées à l'ALR.", "R"),
        ("Mettre en évidence et corriger les mouvements intempestifs de la sonde, "
         "suivre la progression de l'extrémité de l'aiguille et visualiser la "
         "distribution de l'anesthésique local.", "R"),
    ], RCW))
    return story

def _section_securite():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Règles techniques de sécurité"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("Afin de limiter le risque d'injection intraneurale, aborder le nerf "
         "tangentiellement et vérifier avant l'injection, par de petites "
         "mobilisations de l'aiguille, que son extrémité n'est pas solidaire du "
         "nerf.", "PR"),
        ("Interrompre l'injection de la solution anesthésique en l'absence de "
         "visualisation en temps réel de la diffusion de l'anesthésique local et/ou "
         "en cas de douleur, de paresthésie, de résistance à l'injection, ou de "
         "gonflement du nerf.", "R"),
        ("Retirer l'aiguille en cas d'injection intraneurale, car il est impossible "
         "de faire la preuve de l'innocuité d'une telle injection malgré son "
         "caractère souvent indolore.", "R"),
    ], RCW))
    return story

def _section_blocs():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Blocs des membres et du tronc"),
        Spacer(1, 1.5 * mm),
        P("Aux membres supérieur (interscalénique, périclaviculaire, axillaire), "
          "inférieur (fémoral, poplité) et au niveau du tronc, l'échographie peut "
          "permettre de visualiser (totalement ou partiellement) les structures "
          "nerveuses et leurs rapports (variations anatomiques comprises) avec les "
          "structures vasculaires, musculotendineuses (et fascia), péritonéales ou "
          "pleurales. Au creux axillaire, elle permet de visualiser l'artère "
          "axillaire, le tendon du grand dorsal et les nerfs (médian, "
          "musculocutané, radial, ulnaire), et de limiter la durée de repérage liée "
          "aux variations anatomiques. Pour le bloc fémoral et le bloc iliofascial, "
          "elle permet de visualiser l'artère fémorale commune et ses branches, le "
          "fascia iliaca et le nerf fémoral. Il est possible de bloquer le nerf "
          "sciatique, à partir de la région subglutéale, tout le long de son trajet "
          "sous échoguidage. Pour le bloc supraclaviculaire, l'échographie permet "
          "d'obtenir un taux de succès équivalent au repérage par neurostimulation.",
          S_BODY_SM),
    ]))
    story.append(Spacer(1, 1.5 * mm))
    story.append(reco_table([
        ("L'échoguidage pour les blocs interscalénique, supraclaviculaire, "
         "axillaire, fémoral, poplité, distaux et de paroi — peut réduire "
         "l'incidence des ponctions vasculaires accidentelles, le nombre de "
         "redirections d'aiguilles et la dose d'anesthésique local par rapport aux "
         "autres techniques de repérage.", "PR"),
        ("Par voie glutéale, l'abord du nerf sciatique sous échographie est "
         "techniquement plus difficile (profondeur de ponction), incitant à "
         "privilégier probablement un abord subglutéal.", "P"),
        ("Pour les blocs d'espace (paroi abdominale, iliofascial) — permet "
         "d'administrer l'anesthésique local plus précisément qu'avec les autres "
         "techniques.", "PR"),
        ("Pour les blocs périmédullaires — constitue une aide à la procédure en "
         "permettant de visualiser les structures périmédullaires, de déterminer le "
         "niveau de ponction et la profondeur de l'espace péridural.", "PR"),
        ("Pour optimiser le positionnement du cathéter périnerveux.", "PR"),
    ], RCW))
    return story

TABLEAU1_ROWS = [
    ("Introduction dans le système vasculaire ou dans une cavité ou tissu stérile "
     "quelle que soit la voie d'abord",
     "Critique", "Haut risque",
     "Stérilisation ou usage unique stérile à défaut — Désinfection de haut niveau"),
    ("En contact avec une muqueuse, ou la peau lésée superficiellement",
     "Semi-critique", "Risque médian", "Désinfection de niveau intermédiaire"),
    ("En contact avec la peau intacte du patient ou sans contact avec le patient",
     "Non critique", "Risque bas", "Désinfection de bas niveau"),
]

def tableau1_flowable():
    HW = [S_HEAD_W, S_HEAD_W, S_HEAD_W, S_HEAD_W]
    data = [[P("Destination du matériel", S_HEAD_W), P("Classement", S_HEAD_W),
              P("Niveau de risque infectieux", S_HEAD_W), P("Traitement requis", S_HEAD_W)]]
    for dest, classement, risque, traitement in TABLEAU1_ROWS:
        data.append([P(dest, S_CELL), P(classement, S_CELL_B), P(risque, S_CELL),
                     P(traitement, S_CELL)])
    cw = [CW_FULL * 0.34, CW_FULL * 0.16, CW_FULL * 0.18, CW_FULL * 0.32]
    t = Table(data, colWidths=cw, repeatRows=1)
    style_cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), NAVY), ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTNAME", (0, 0), (-1, 0), FONT_BOLD), ("FONTSIZE", (0, 0), (-1, 0), 7.6),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.5, GREY_LIGHT),
        ("TOPPADDING", (0, 0), (-1, -1), 3.2), ("BOTTOMPADDING", (0, 0), (-1, -1), 3.2),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            style_cmds.append(("BACKGROUND", (0, i), (-1, i), BG_PANEL))
    t.setStyle(TableStyle(style_cmds))
    return t

def _section_hygiene():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Conditions de réalisation, hygiène"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("Réaliser un bloc échoguidé chez un patient éveillé, calme et coopérant.", "PR"),
        ("Dans des situations où le rapport bénéfice-risque est favorable et "
         "justifié, réaliser un bloc chez un patient sous anesthésie (générale ou "
         "régionale) ou sédation — l'échographie apporte alors probablement une "
         "sécurité supplémentaire dans ce cas.", "P"),
    ], RCW))
    story.append(Spacer(1, 2 * mm))
    story.append(P("<b>Tableau 1 — Classement des dispositifs médicaux et niveaux de "
                    "traitement requis</b> (reproduit verbatim du texte source).",
                    S_CELL_B))
    story.append(Spacer(1, 1 * mm))
    story.append(tableau1_flowable())
    story.append(Spacer(1, 2 * mm))
    story.append(reco_table([
        ("Respecter les mesures d'asepsie pour la sonde d'échographie, en raison du "
         "risque de transmission croisée et de la nécessité d'un environnement "
         "stérile requis en ALR.", "R"),
        ("Avant chaque procédure, essuyer, nettoyer et désinfecter les sondes et les "
         "câbles ; nettoyer régulièrement l'ensemble de l'appareil.", "R"),
        ("Utiliser une gaine de protection stérile à usage unique dédiée et adaptée, "
         "et du gel stérile unidose lors de l'usage d'une sonde d'échographie.", "R"),
        ("En l'absence de perforation ou de déchirure de la gaine lors du retrait de "
         "la protection, la désinfection de la sonde entre chaque patient doit être "
         "au minimum celle correspondant à une désinfection de bas niveau.", "R"),
        ("En cas de rupture de la gaine ou de souillure de la sonde, la désinfection "
         "doit être de niveau plus élevé (cf. Tableau 1).", "R"),
        ("À la fin du programme opératoire, nettoyer la sonde avec un détergent, la "
         "rincer, la sécher et la ranger dans un endroit propre.", "R"),
        ("Faire valider les différentes procédures de nettoyage et de désinfection "
         "par le CLIN et/ou le service d'hygiène.", "R"),
    ], RCW))
    return story

def _section_sources():
    story = []
    story.append(section_bar("Sources et traçabilité", color=GREY))
    story.append(Spacer(1, 2 * mm))
    story.append(P(
        "<b>Document source :</b> « Échographie en anesthésie locorégionale » — "
        "Recommandations Formalisées d'Experts (RFE), Société française "
        "d'anesthésie et de réanimation (SFAR). Auteurs : H. Bouaziz (auteur "
        "correspondant), F. Aubrun, A.A. Belbachir, P. Cuvillon, E. Eisenberg, "
        "D. Jochum, C. Aveline, P. Biboulet, M. Binhas, S. Bloc, G. Boccara, "
        "M. Carles, O. Choquet, L. Delaunay, J.-P. Estebe, R. Fuzier, E. Gaertner, "
        "A. Gnaho, K. Nouette-Gaulain, E. Nouvellon, J. Ripart, V. Tubert.",
        S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P("<b>Version :</b> Ann Fr Anesth Réanim 30 (2011) e33-e35, "
                    "disponible sur Internet le 17 août 2011. "
                    "doi:10.1016/j.annfar.2011.06.008.", S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P("<b>Méthodologie :</b> texte narratif sans grille de cotation "
                    "imprimée — force déduite des locutions modales du texte "
                    "(convention bespoke, voir détail en page 1).", S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>URL source :</b> https://sfar.org/wp-content/uploads/2015/10/"
        "2_AFAR_echographie-en-anesthesie-locoregionale.pdf", S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P("<b>Couverture :</b> intégralité des énoncés de recommandation du "
                    "texte narratif (règles générales, matériel, sécurité, blocs des "
                    "membres et du tronc, conditions de réalisation et hygiène), y "
                    "compris le Tableau 1 reproduit verbatim. Complète, sans "
                    "remplacer, les RPC 2002 (blocs périphériques des membres) et "
                    "2006 (blocs périmédullaires).", S_SOURCE))
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Avertissement — document de 2011 :</b> cette fiche de synthèse "
        "indépendante reprend l'intégralité des énoncés de recommandation du texte "
        "source, mais ne le remplace pas et n'est ni éditée ni validée par la SFAR. "
        "Le matériel et les pratiques d'échoguidage ayant pu évoluer depuis 2011, se "
        "référer à un avis spécialisé et aux recommandations actualisées avant toute "
        "décision.", S_BODY_SM), bg=GREY_LIGHT, border=GREY))
    return story

def _section_intro_generalites_materiel():
    story = _section_intro()
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_generalites())
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_materiel())
    return story

def _section_securite_blocs_hygiene_sources():
    story = _section_securite()
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_blocs())
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_hygiene())
    story.append(Spacer(1, 4 * mm))
    story.extend(_section_sources())
    return story

def _section_all():
    story = _section_intro_generalites_materiel()
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_securite_blocs_hygiene_sources())
    return story

SECTIONS = [
    ("Contexte, apprentissage, matériel, sécurité, blocs & sources", _section_all),
]

def _make_doc(path=None):
    return SimpleDocTemplate(path or OUT, pagesize=A4,
                              leftMargin=MARGIN, rightMargin=MARGIN,
                              topMargin=32 * mm, bottomMargin=16 * mm,
                              title="Fiche SFAR 2011 - Echographie en anesthesie locoregionale",
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
