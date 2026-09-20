# -*- coding: utf-8 -*-
"""
Fiche de synthese - Societe Francaise d'Anesthesie et de Reanimation (SFAR).
"Prise en charge anesthesique des patients en hospitalisation ambulatoire" -
Recommandations Formalisees d'Experts (RFE). Coordonnateur du groupe de
travail : Dr Anne Guidat (Lille). Ann Fr Anesth Reanim 29 (2010) 67-72
(doi:10.1016/j.annfar.2009.12.008). 6 pages, telecharge depuis sfar.org
(wp-content/uploads/2015/10/2_AFAR_Prise-en-charge-anesthesique-des-patients-
en-hospitalisation-ambulatoire.pdf).

METHODOLOGIE - CONVENTION BESPOKE (8e distincte de ce corpus) : ce texte ne
porte AUCUN grade GRADE/RAND/Niveau-Score imprime a cote de chaque
recommandation - la force est encodee uniquement par le verbe modal
introduisant chaque enonce : "il est recommande de/que" (force forte),
"il est souhaitable" (force intermediaire), "il est possible" (permissif/
optionnel), "il n'est pas recommande" (negatif). Aucune legende
methodologique explicite dans le texte source ne nomme ces 4 categories -
elles sont deduites directement et exhaustivement du verbe modal de chacune
des 71 recommandations numerotees, jamais inventees. Chips utilises : R
(recommande), S (souhaitable), P (possible), N (non recommande) - legende
explicite en page 1, memes principes de couleur neutre (gris) que les autres
conventions bespoke de ce corpus (ex. catheters_veineux_centraux) faute de
correspondance avec les couleurs GRADE standard.

COUVERTURE : integralite des 71 recommandations numerotees (Questions 1 a
11), avec le paragraphe de contexte minimal precedant chaque question quand
necessaire a la comprehension (concept du triptyque acte-patient-structure,
etc.) - pas d'argumentaire scientifique detaille au-dela de ce qui est deja
dans l'enonce de la recommandation lui-meme (regle de projet 2026-09-14).
Comite d'organisation et groupe de travail nommes en page finale (sources).

Aucune table/figure image dans ce document - texte seul, aucun rendu visuel
requis au-dela de la verification standard page par page.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from style import *
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.units import mm

OUT = "/home/user/rfe-sfar-website/output/Fiche_SFAR_Hospitalisation_Ambulatoire_2009.pdf"

SOURCE_TXT = ("Source : « Prise en charge anesthésique des patients en hospitalisation "
              "ambulatoire » — RFE SFAR, Ann Fr Anesth Réanim 29 (2010) 67-72. Fiche de "
              "synthèse non officielle : se référer au texte intégral.")

def P(txt, style=S_CELL):
    return Paragraph(txt, style)

def chip(label, **kw):
    return grade_chip(label, **kw)

CW_FULL = PAGE_W - 2 * MARGIN
RCW = [CW_FULL - 14 * mm, 14 * mm]

def reco_table(rows, col_widths=RCW):
    """rows: (num, text, grade_label)."""
    data = [[P("Recommandation", S_HEAD_W), P("Force", S_HEAD_W_C)]]
    for num, txt, grade in rows:
        data.append([P("<b>%s.</b> %s" % (num, txt), S_CELL), chip(grade, width=11 * mm)])
    t = Table(data, colWidths=col_widths, repeatRows=1)
    style_cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), NAVY), ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTNAME", (0, 0), (-1, 0), FONT_BOLD), ("FONTSIZE", (0, 0), (-1, 0), 8),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("ALIGN", (1, 0), (1, -1), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 0.5, GREY_LIGHT),
        ("TOPPADDING", (0, 0), (-1, -1), 3.2), ("BOTTOMPADDING", (0, 0), (-1, -1), 3.2),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            style_cmds.append(("BACKGROUND", (0, i), (-1, i), BG_PANEL))
    t.setStyle(TableStyle(style_cmds))
    return t

def legend_flowable():
    chip_w = 13 * mm
    content_w = CW_FULL
    row = Table([[chip("R", width=chip_w - 2 * mm), chip("S", width=chip_w - 2 * mm),
                  chip("P", width=chip_w - 2 * mm), chip("N", width=chip_w - 2 * mm),
                  P("<b>Force</b> (déduite du verbe modal de la source, aucune grille de "
                    "cotation imprimée) — <b>R</b> = « il est recommandé » (forte) ; "
                    "<b>S</b> = « il est souhaitable » (intermédiaire) ; <b>P</b> = « il est "
                    "possible » (permissif/optionnel) ; <b>N</b> = « il n'est pas "
                    "recommandé » (négatif).", S_BADGE_HEAD)]],
                colWidths=[chip_w, chip_w, chip_w, chip_w, content_w - 4 * chip_w])
    row.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                              ("LEFTPADDING", (0, 0), (-1, -1), 1),
                              ("RIGHTPADDING", (0, 0), (-1, -1), 1),
                              ("TOPPADDING", (0, 0), (-1, -1), 0),
                              ("BOTTOMPADDING", (0, 0), (-1, -1), 0)]))
    return row

TOTAL_PAGES = {"n": 6}

def on_page(canvas, doc, page_title):
    header_band(canvas, doc, "SFAR — RFE, 2009",
                "Prise en charge anesthésique en hospitalisation ambulatoire",
                page_title, icon_fn=lambda c, x, y: icon_shield(c, x, y, 13 * mm), color=TEAL_DARK)
    footer_band(canvas, doc, SOURCE_TXT, f"Page {doc.page} / {TOTAL_PAGES['n']}")

# ---------------------------------------------------------------------------
def _section_intro():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Résumé :</b> Recommandations Formalisées d'Experts SFAR sur l'organisation de "
        "la prise en charge anesthésique en hospitalisation ambulatoire (sortie le jour "
        "même, sans nuit d'hébergement), structurées en 11 questions : définitions, "
        "critères d'éligibilité, information du patient, choix de la technique "
        "d'anesthésie, prise en charge des suites opératoires (douleur, prévention "
        "thromboembolique, NVPO), procédure de sortie, coordination et continuité des "
        "soins, évaluation et gestion des risques, spécificités liées à l'âge (pédiatrie, "
        "gériatrie), spécificités organisationnelles et spatiales, et responsabilité de "
        "l'anesthésiste-réanimateur. <b>71 recommandations au total.</b>", S_BODY),
        bg=BG_PANEL, border=TEAL))
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("Méthodologie"))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "Ce texte ne comporte <b>aucune grille de cotation scientifique imprimée</b> "
        "(pas de GRADE, pas de niveau de preuve, pas d'accord RAND/UCLA) — la force de "
        "chaque recommandation est encodée uniquement par le verbe modal qui l'introduit. "
        "Cette fiche reproduit cette convention telle quelle, par un chip déduit "
        "directement et exhaustivement du verbe modal de chaque énoncé (voir légende "
        "ci-dessous) — aucun grade GRADE n'est inventé pour ce document qui n'en emploie "
        "aucun.", S_BODY_SM))
    story.append(Spacer(1, 1.5 * mm))
    story.append(legend_flowable())
    return story

# ---------------------------------------------------------------------------
def _section_q1_q2():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Question 1 — Définitions"),
        Spacer(1, 1.5 * mm),
        P("La prise en charge anesthésique en hospitalisation ambulatoire est un concept "
          "d'organisation centré sur le patient, avec sortie le jour même sans nuit "
          "d'hébergement, quel que soit l'acte (chirurgical ou médical, diagnostique ou "
          "thérapeutique) réalisé dans les conditions de sécurité d'un bloc opératoire.",
          S_BODY_SM),
    ]))
    story.append(Spacer(1, 1.5 * mm))
    story.append(reco_table([
        (1, "Il est recommandé de privilégier le mode de prise en charge ambulatoire des "
            "patients dès que les conditions de sa réalisation sont réunies.", "R"),
        (2, "Il est recommandé que seuls les acteurs d'une même structure définissent "
            "entre eux la liste des actes ambulatoires adaptés à leur expertise et à "
            "l'organisation mise en place, liste évolutive ; décision médicale prise en "
            "colloque singulier avec le patient.", "R"),
        (3, "Il est souhaitable qu'il n'y ait pas de liste réglementaire d'actes à "
            "réaliser en ambulatoire.", "S"),
    ]))
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Question 2 — Critères d'éligibilité à l'hospitalisation ambulatoire"),
        Spacer(1, 1.5 * mm),
        P("Concept fondamental : le triptyque acte-patient-structure (analyse du "
          "bénéfice/risque, prévisibilité de la prise en charge, organisation en place).",
          S_BODY_SM),
    ]))
    story.append(Spacer(1, 1.5 * mm))
    story.append(reco_table([
        (4, "Il est recommandé que l'éligibilité à l'ambulatoire repose sur l'analyse du "
            "bénéfice/risque pour le patient, la prévisibilité de sa prise en charge et "
            "de l'organisation mise en place, en particulier la permanence et la "
            "continuité des soins.", "R"),
        (5, "Il est recommandé que la sélection des actes réalisés en ambulatoire soit "
            "fondée sur la maîtrise des risques, de la durée et des suites de ces actes.", "R"),
        (6, "Il est possible d'intégrer certains actes urgents dans un programme "
            "ambulatoire, à condition de ne pas perturber le fonctionnement de l'unité "
            "et de garantir le même niveau de qualité et de sécurité au patient.", "P"),
        (7, "Il est recommandé que les patients de statut ASA I, II et III stable soient "
            "éligibles à l'ambulatoire, sur analyse du rapport bénéfice/risque au cas par "
            "cas.", "R"),
        (8, "Il est recommandé d'assurer les conditions de la compréhension et de "
            "l'acceptation des modalités de prise en charge par le patient : traducteur "
            "pour les patients non francophones, accompagnement des mineurs par un "
            "parent/représentant légal, accompagnement des patients à trouble du "
            "jugement par un tiers garant du jeûne/observance/continuité des soins.", "R"),
        (9, "Il est recommandé de s'informer auprès du patient que le lieu de résidence "
            "postopératoire est compatible avec la prise en charge ambulatoire — la "
            "durée du transport et la distance ne sont pas des facteurs d'exclusion.", "R"),
        (10, "Il est recommandé de formaliser une convention entre établissements afin de "
             "prévoir la prise en charge d'une complication éventuelle par un "
             "établissement autre que celui de l'acte ambulatoire.", "R"),
        (11, "Il est recommandé de s'assurer que lors du trajet de retour le patient ne "
             "conduise pas un véhicule et qu'il soit accompagné par un tiers.", "R"),
        (12, "Il est recommandé que la présence d'un accompagnant au lieu de résidence "
             "postopératoire soit évaluée en fonction du couple acte-patient et définie "
             "au préalable par les acteurs de la structure.", "R"),
    ]))
    return story

def _section_intro_q1_q2():
    story = _section_intro()
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_q1_q2())
    return story

# ---------------------------------------------------------------------------
def _section_q3():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Question 3 — Modalités de l'information du patient"),
        Spacer(1, 1.5 * mm),
        P("Le patient hospitalisé en ambulatoire est acteur de sa préparation "
          "préopératoire et de sa réhabilitation postopératoire au lieu de résidence.",
          S_BODY_SM),
    ]))
    story.append(Spacer(1, 1.5 * mm))
    story.append(reco_table([
        (13, "Il est recommandé de délivrer une information précoce et réitérée à chaque "
             "étape de la prise en charge.", "R"),
        (14, "Il est recommandé que l'information donnée au patient soit élaborée et "
             "concertée entre les différents acteurs amenés à en délivrer tout ou "
             "partie.", "R"),
        (15, "Il est recommandé que la consultation préanesthésique soit réalisée par un "
             "anesthésiste-réanimateur connaissant les modalités de fonctionnement de la "
             "structure ambulatoire.", "R"),
        (16, "Il est recommandé, au cours de la consultation pré-anesthésique, de "
             "dispenser une information adaptée sur : le jeûne et la gestion des "
             "traitements, les exigences des techniques d'anesthésie, les conditions de "
             "sortie et l'accompagnement nécessaire, les consignes postopératoires, les "
             "méthodes d'analgésie, les recours en cas d'événement imprévu, l'accès à une "
             "information complémentaire.", "R"),
        (17, "Il est recommandé d'informer le patient des effets de l'anesthésie/sédation "
             "sur les fonctions cognitives et la vigilance pendant les 12 premières "
             "heures, avec variabilité interindividuelle de ces effets et de leur "
             "durée.", "R"),
        (18, "Il est recommandé d'informer le patient que la conduite de tout véhicule "
             "est proscrite pendant les 12 premières heures du fait de l'anesthésie ; la "
             "reprise devra tenir compte du handicap lié à l'acte.", "R"),
        (19, "Il est recommandé d'informer le patient pratiquant la conduite de groupe "
             "lourd ou de machine à haut niveau attentionnel que des troubles de la "
             "vigilance peuvent persister pendant quelques jours.", "R"),
        (20, "Il est recommandé d'informer les patients des effets secondaires possibles "
             "du traitement péri-opératoire (anxiolytique, antalgiques majeurs) sur les "
             "fonctions cognitives et la vigilance.", "R"),
        (21, "Il est recommandé de ne pas dispenser d'information au patient pendant la "
             "phase de récupération de l'anesthésie, du fait d'une possible altération "
             "de la mémoire et de sa consolidation.", "R"),
        (22, "Il est recommandé que l'information délivrée soit orale, complétée par un "
             "support écrit court et lisible ou audiovisuel, incitant le patient à poser "
             "toute question utile, avec traçabilité.", "R"),
        (23, "Il est possible de faire signer au patient le document rappelant les "
             "exigences de prise en charge ambulatoire (vertu pédagogique) — cette "
             "signature n'engage pas la responsabilité juridique du patient et ne "
             "défausse pas celle du médecin.", "P"),
        (24, "Il est recommandé de pouvoir établir un contact avec le patient dans les "
             "jours précédant l'hospitalisation pour réitérer les consignes, en "
             "particulier en cas de consultation délocalisée ou d'acte itératif.", "R"),
    ]))
    return story

# ---------------------------------------------------------------------------
def _section_q4():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Question 4 — Choix de la technique d'anesthésie"),
        Spacer(1, 1.5 * mm),
        P("Le choix de la technique repose sur l'analyse du bénéfice/risque pour le "
          "patient, l'acte réalisé et l'organisation mise en place.", S_BODY_SM),
    ]))
    story.append(Spacer(1, 1.5 * mm))
    story.append(reco_table([
        (25, "Il est souhaitable de formaliser les modalités de réalisation de la visite "
             "préanesthésique et d'en assurer la traçabilité.", "S"),
        (26, "Il est possible de prescrire une prémédication anxiolytique et/ou "
             "analgésique.", "P"),
        (27, "Il est recommandé d'établir des règles de jeûne préopératoire adaptées à la "
             "programmation opératoire pour améliorer le confort du patient.", "R"),
        (28, "Il n'est pas recommandé de stratégie spécifique à la prise en charge "
             "anesthésique ambulatoire — l'ensemble des agents (hypnotiques, "
             "morphiniques, curares) peut être utilisé, en privilégiant si possible les "
             "agents à durée de vie courte et effets secondaires réduits.", "N"),
        (29, "Il est souhaitable d'adapter la technique de rachianesthésie à la nécessité "
             "d'une reprise rapide de l'autonomie (faibles doses, adjuvants "
             "liposolubles, latéralisation).", "S"),
        (30, "Il est recommandé de réaliser des blocs périphériques en accord avec le "
             "patient pour les interventions des membres qui s'y prêtent.", "R"),
    ]))
    return story

def _section_q3_q4():
    story = _section_q3()
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_q4())
    return story

# ---------------------------------------------------------------------------
def _section_q5():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Question 5 — Prise en charge des suites opératoires"),
        Spacer(1, 1.5 * mm),
        P("<b>5.1 Douleur postopératoire</b> — la maîtrise de la douleur allie "
          "anticipation, rigueur de prescription et respect de l'observance.", S_BODY_SM),
    ]))
    story.append(Spacer(1, 1.5 * mm))
    story.append(reco_table([
        (31, "Il est recommandé de mettre en place une stratégie multimodale de la prise "
             "en charge de la douleur postopératoire y compris au lieu de résidence : "
             "information, prévention, traitement et évaluation.", "R"),
        (32, "Il est souhaitable que les ordonnances d'antalgiques soient remises au "
             "patient dès la consultation préopératoire de chirurgie ou d'anesthésie.", "S"),
        (33, "Il est recommandé que les ordonnances d'antalgiques précisent les horaires "
             "de prise systématiques et les conditions de recours à un antalgique de "
             "niveau plus élevé si nécessaire.", "R"),
        (34, "Il est souhaitable que les modalités de gestion et de prise des analgésiques "
             "de « secours » soient expliquées dès la consultation préopératoire.", "S"),
        (35, "Il est souhaitable d'utiliser les infiltrations et les blocs périphériques "
             "seuls ou en complément d'une autre technique pour la douleur "
             "postopératoire.", "S"),
        (36, "Il est recommandé de formaliser l'organisation du suivi de l'analgésie par "
             "cathéters périnerveux au lieu de résidence.", "R"),
        (37, "Il est recommandé de prescrire tout moyen non médicamenteux permettant de "
             "réduire la douleur postopératoire (application de froid, posture "
             "antalgique...).", "R"),
    ]))
    story.append(Spacer(1, 2 * mm))
    story.append(P("<b>5.2 Prévention thromboembolique</b> — incidence globalement faible "
                    "après chirurgie ambulatoire.", S_BODY_SM))
    story.append(Spacer(1, 1 * mm))
    story.append(reco_table([
        (38, "Il est recommandé de prendre en compte la combinaison du risque individuel "
             "du patient et du risque de la chirurgie ; la prévention pharmacologique "
             "n'est pas systématique.", "R"),
        (39, "Il est recommandé que la durée du traitement pharmacologique ne soit pas "
             "inférieure à cinq jours et soit adaptée au cas par cas ; en risque global "
             "faible à modéré, la prophylaxie mécanique par bas de contention est "
             "efficace.", "R"),
    ]))
    story.append(Spacer(1, 2 * mm))
    story.append(P("<b>5.3 Nausées et vomissements postopératoires (NVPO)</b> — pas de "
                    "stratégie de prévention spécifique à l'ambulatoire ; algorithme "
                    "usuel selon les facteurs de risque.", S_BODY_SM))
    story.append(Spacer(1, 1 * mm))
    story.append(reco_table([
        (40, "Il est recommandé d'adopter une stratégie antiémétique prophylactique "
             "multimodale chez les patients ambulatoires à haut risque de NVPO.", "R"),
        (41, "Il est souhaitable que le traitement des NVPO survenant après la sortie "
             "repose sur des antiémétiques validés en prophylaxie, en changeant de "
             "classe et de forme galénique en cas d'échec du premier choix.", "S"),
    ]))
    return story

def _section_intro_all_q5():
    story = _section_intro_q1_q2()
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_q3_q4())
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_q5())
    return story

# ---------------------------------------------------------------------------
def _section_q6():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Question 6 — Modalités de la procédure de sortie"),
        Spacer(1, 1.5 * mm),
        P("Autoriser la sortie sans concession à la sécurité est le moment-clé de la "
          "prise en charge ambulatoire ; les critères évaluent « l'aptitude au retour au "
          "lieu de résidence ».", S_BODY_SM),
    ]))
    story.append(Spacer(1, 1.5 * mm))
    story.append(reco_table([
        (42, "Il est recommandé que l'ensemble des modalités de sortie soit formalisé et "
             "porté à la connaissance des patients, dans la charte de fonctionnement de "
             "l'unité ambulatoire.", "R"),
        (43, "Il est recommandé en l'absence imprévue d'accompagnant de rechercher une "
             "alternative avant de proposer un transfert en hospitalisation "
             "conventionnelle ; en cas de refus du patient, avoir formalisé une "
             "procédure de « sortie contraire à la pratique de l'ambulatoire ».", "R"),
        (44, "Il est souhaitable d'utiliser un score pour autoriser la sortie, facile à "
             "mettre en œuvre — pas d'intérêt à utiliser des tests psychomoteurs.", "S"),
        (45, "Il n'est pas recommandé d'imposer une réalimentation liquide et solide "
             "avant la sortie.", "N"),
        (46, "Il est possible, après anesthésie générale ou bloc périphérique, de ne pas "
             "exiger une miction pour autoriser la sortie, en l'absence de facteur de "
             "risque lié au patient ou au type de chirurgie.", "P"),
        (47, "Il est possible, après une rachianesthésie, de ne pas attendre une miction "
             "pour autoriser la sortie, sous réserve d'une estimation (clinique, au "
             "mieux échographique) du volume vésical résiduel et de l'absence de "
             "facteur de risque.", "P"),
        (48, "Il est possible, lorsque des blocs périphériques sont utilisés, de "
             "permettre la sortie malgré l'absence de levée du bloc, sous réserve de "
             "mesures de protection du membre endormi, d'une information précise et "
             "d'une assistance à domicile.", "P"),
        (49, "Il est recommandé, après un bloc périmédullaire, de s'assurer des capacités "
             "de déambulation du patient avant la sortie ; le port d'attelle ou de "
             "béquille peut être utilisé.", "R"),
    ]))
    return story

# ---------------------------------------------------------------------------
def _section_q7_q8():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Question 7 — Coordination entre les acteurs et continuité des soins"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        (50, "Il est recommandé que l'organisation mise en place permette le partage de "
             "l'information entre les acteurs de la structure et la coordination des "
             "soins avec la médecine de ville.", "R"),
        (51, "Il est recommandé que soient remis au patient, à sa sortie, les documents "
             "nécessaires à la continuité des soins.", "R"),
        (52, "Il est recommandé que les acteurs de la structure s'assurent que le "
             "processus du retour au lieu de résidence du patient est organisé.", "R"),
        (53, "Il est recommandé que les acteurs de la structure, en collaboration avec la "
             "médecine de ville, organisent le suivi du patient après sa sortie en "
             "fonction de la prévisibilité des suites et des antécédents du patient.", "R"),
    ]))
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Question 8 — Évaluation et gestion des risques en ambulatoire"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        (54, "Il est recommandé de mettre en place une démarche qualité au sein de "
             "l'unité ambulatoire : description du processus, analyse des points "
             "critiques, plan d'amélioration.", "R"),
        (55, "Il est recommandé que l'organisation de la structure prenne en compte le "
             "risque propre au statut d'acteur direct du patient, en particulier dans "
             "les phases d'éligibilité, de sortie et de suivi à domicile.", "R"),
        (56, "Il est recommandé de mettre en place une démarche d'analyse et de maîtrise "
             "des risques de l'activité ambulatoire et de son évolution dans le temps.", "R"),
        (57, "Il est souhaitable de définir des indicateurs d'analyse et de pilotage "
             "adaptés à la structure (qualité des soins, satisfaction, suivi des actes, "
             "données médicoéconomiques).", "S"),
        (58, "Il est recommandé d'assurer le suivi de la qualité des soins et de la "
             "satisfaction des patients après leur sortie.", "R"),
    ]))
    return story

def _section_q6_q7_q8():
    story = _section_q6()
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_q7_q8())
    return story

# ---------------------------------------------------------------------------
def _section_q9():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Question 9 — Spécificités liées à l'âge"),
        Spacer(1, 1.5 * mm),
        P("<b>9.1 Pédiatrie</b>", S_CELL_B),
    ]))
    story.append(Spacer(1, 1 * mm))
    story.append(reco_table([
        (59, "Il est recommandé que seuls les acteurs d'une même structure définissent "
             "entre eux la liste des actes ambulatoires pédiatriques adaptés ; décision "
             "médicale prise en colloque singulier avec les parents.", "R"),
        (60, "Il est recommandé que les enfants de score ASA I, II et ASA III équilibré "
             "soient éligibles : nés à terme, patients de plus de 3 mois (moins de 3 mois "
             "possibles selon l'expérience de l'équipe) ; nés prématurés, âge post-"
             "conceptionnel ≥60 semaines (jusqu'à 1 an possible selon l'expérience de "
             "l'équipe), <60 semaines = facteur d'exclusion.", "R"),
        (61, "Il est recommandé que l'information délivrée soit adaptée, personnalisée et "
             "compréhensible pour les parents et pour l'enfant, incluant le risque "
             "possible de report de l'intervention.", "R"),
        (62, "Il est recommandé d'informer les parents de la présence nécessaire d'un "
             "accompagnant non conducteur ; au-delà de 10 ans, un second accompagnant "
             "n'est plus nécessaire.", "R"),
    ]))
    story.append(Spacer(1, 2 * mm))
    story.append(P("<b>9.2 Gériatrie</b> — le grand âge n'est pas une contre-indication en "
                    "soi ; l'ambulatoire semble diminuer l'incidence des troubles du "
                    "comportement postopératoire par rapport à une hospitalisation "
                    "conventionnelle.", S_BODY_SM))
    story.append(Spacer(1, 1 * mm))
    story.append(reco_table([
        (63, "Il est recommandé de faire bénéficier les personnes âgées d'une prise en "
             "charge ambulatoire selon l'analyse du bénéfice/risque, la prévisibilité de "
             "la prise en charge et l'organisation mise en place.", "R"),
        (64, "Il est recommandé d'éviter les benzodiazépines en préopératoire — elles "
             "augmentent l'incidence des troubles du comportement postopératoire.", "R"),
    ]))
    return story

# ---------------------------------------------------------------------------
def _section_q10_q11():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Question 10 — Spécificités organisationnelles et spatiales"),
        Spacer(1, 1.5 * mm),
        P("Le parcours du patient est au centre de l'organisation de la structure "
          "ambulatoire ; il n'y a pas de modèle architectural unique de structure "
          "ambulatoire.", S_BODY_SM),
    ]))
    story.append(Spacer(1, 1.5 * mm))
    story.append(reco_table([
        (65, "Il est recommandé que le parcours du patient soit fluide et maîtrisé, "
             "relevant d'une pensée logistique agencée avec l'équipe qui prendra en "
             "charge le fonctionnement de l'unité.", "R"),
        (66, "Il est recommandé de mettre en place une organisation qui permette une "
             "optimisation des flux, garante de la prise en charge des patients dans les "
             "délais prévus.", "R"),
        (67, "Il est recommandé que l'unité ambulatoire maîtrise sa propre organisation "
             "en ordonnant, contrôlant et dirigeant tous les flux (patients, "
             "informations, personnels, matériels).", "R"),
    ]))
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Question 11 — Responsabilité de l'anesthésiste-réanimateur"),
        Spacer(1, 1.5 * mm),
        P("La responsabilité de l'anesthésiste-réanimateur n'est pas différente de ce "
          "qu'elle est en hospitalisation conventionnelle. L'accompagnant est un tiers "
          "sans statut particulier (aucune responsabilité juridique spécifique hors "
          "mineur/incapable majeur) ; sa signature n'a pas lieu d'être.", S_BODY_SM),
    ]))
    story.append(Spacer(1, 1.5 * mm))
    story.append(reco_table([
        (68, "Il est recommandé de remettre au patient un document écrit concernant les "
             "consignes de l'ambulatoire et d'archiver ce document dans le dossier du "
             "patient.", "R"),
        (69, "Il est recommandé de vérifier le respect des consignes et d'assurer la "
             "traçabilité dans le dossier du patient.", "R"),
        (70, "Il est recommandé d'écrire clairement les modalités d'autorisation de "
             "sortie du patient au sein de la charte de fonctionnement de la structure.", "R"),
        (71, "Il est recommandé que l'organisation prévoie qu'un anesthésiste-"
             "réanimateur puisse être joint en cas de survenue d'un événement imprévu en "
             "rapport avec l'anesthésie, dans les suites immédiates et après la sortie du "
             "patient.", "R"),
    ]))
    return story

def _section_q9_q10_q11():
    story = _section_q9()
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_q10_q11())
    return story

# ---------------------------------------------------------------------------
def _section_sources():
    story = []
    story.append(section_bar("Sources et traçabilité", color=GREY))
    story.append(Spacer(1, 2 * mm))
    story.append(P(
        "<b>Document source :</b> « Prise en charge anesthésique des patients en "
        "hospitalisation ambulatoire » — Recommandations Formalisées d'Experts (RFE), "
        "Société française d'anesthésie et de réanimation (SFAR). Président du comité "
        "d'organisation : Dr Laurent Jouffroy. Coordonnateur du groupe de travail : "
        "Dr Anne Guidat (CHRU de Lille). Secrétaire de séance : Dr Bernard Coustets. "
        "Groupe de travail : J. Bataille, J. Bientz, C. Bléry, G. Bontemps, J.-F. Cerfon, "
        "M.-L. Cittanova, N. Dufeu, L. Delaunay, P. Diemunsch, C. Gatecel, M. Gentili, "
        "H. Le Hetet, M. Maillet, S. Nguyen Roux, L. Pain, P. Pérucho, B. Plaud, "
        "M. Raucoules-Aime, M. Samama, F. Venutolo.", S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P("<b>Version :</b> Ann Fr Anesth Réanim 29 (2010) 67-72. "
                    "doi:10.1016/j.annfar.2009.12.008.", S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P("<b>Méthodologie :</b> aucune grille de cotation scientifique imprimée "
                    "— force déduite du verbe modal introduisant chaque recommandation "
                    "(convention bespoke, voir détail en page 1).", S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>URL source :</b> https://sfar.org/wp-content/uploads/2015/10/"
        "2_AFAR_Prise-en-charge-anesthesique-des-patients-en-hospitalisation-"
        "ambulatoire.pdf", S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P("<b>Couverture :</b> intégralité des 71 recommandations (11 "
                    "questions), avec le contexte minimal nécessaire à leur "
                    "compréhension. Argumentaire scientifique détaillé volontairement "
                    "non transcrit au-delà de ce que porte déjà l'énoncé de chaque "
                    "recommandation — se référer au texte intégral.", S_SOURCE))
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Avertissement — document de 2009/2010 :</b> cette fiche de synthèse "
        "indépendante reprend l'intégralité des 71 recommandations du texte source, mais "
        "ne le remplace pas et n'est ni éditée ni validée par la SFAR. Les pratiques "
        "organisationnelles et les seuils cités ayant pu évoluer depuis 2009, se référer "
        "à un avis spécialisé et aux recommandations actualisées avant toute décision.",
        S_BODY_SM), bg=GREY_LIGHT, border=GREY))
    return story

def _section_q9_q10_q11_sources():
    story = _section_q9_q10_q11()
    story.append(Spacer(1, 4 * mm))
    story.extend(_section_sources())
    return story

SECTIONS = [
    ("Méthodologie, définitions, éligibilité, information & choix de la technique (Q1-4)",
     _section_intro_all_q5),
    ("Sortie, coordination et gestion des risques en ambulatoire (Q6-8)",
     _section_q6_q7_q8),
    ("Spécificités liées à l'âge, organisation, responsabilité & sources (Q9-11)",
     _section_q9_q10_q11_sources),
]

def _make_doc(path=None):
    return SimpleDocTemplate(path or OUT, pagesize=A4,
                              leftMargin=MARGIN, rightMargin=MARGIN,
                              topMargin=32 * mm, bottomMargin=16 * mm,
                              title="Fiche SFAR 2009 - Hospitalisation ambulatoire",
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
