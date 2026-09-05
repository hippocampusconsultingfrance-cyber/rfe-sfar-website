# -*- coding: utf-8 -*-
"""
Fiche de synthese - RFE SFAR 2017 (actualisation de la CE Intubation difficile 2006)
Intubation difficile et extubation en anesthesie chez l'adulte
Source verifiee : Anesth Reanim. 2017;3:552-571, texte valide CA SFAR 29/06/2017
Methodologie GRADE, tags "(Grade X+/-) Accord FORT" (et un "Accord faible" pour R2.3) imprimes
litteralement apres chaque recommandation. 13 recommandations numerotees R1.1-R1.3, R2.1-R2.3,
R4.1-R4.2 (pas de R3 : la question 3 sur l'AIVOC/AINOC a abouti a "Pas de recommandation"),
R5.1-R5.4, R6.1 - resume officiel "5 GRADE1 + 8 GRADE2 = 13" independamment reverifie item par
item et confirme coherent. "Accord fort obtenu pour 99% des recommandations" (pas 100%) : R2.3 est
la seule a porter litteralement "Accord faible" plutot que "Accord FORT" - fidelement reproduit.
2 "Pas de recommandation" (vidéolaryngoscope chez patient a risque de regurgitation/estomac plein ;
AIVOC/AINOC vs sedation par bolus). 6 algorithmes-diagrammes (pures images, pages 11-12 et 14-17 de
la source, 170-230 caracteres extractibles = legendes seules) transcrits integralement depuis le
rendu visuel : Intubation difficile prevue (fusion des pages 14+15, entree + arbre detaille),
Intubation difficile non prevue (page 17), Oxygenation/echec ventilation+intubation - equivalent
CICO (page 16), Extubation - facteurs de risque (page 11), Extubation - leadership/decision
(page 12). Complete le trio des fiches "voies aeriennes" de ce projet (intubation_urgence = adulte
hors bloc ; voies_aeriennes_enfant = pediatrie ; cette fiche = adulte au bloc operatoire).
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from style import *
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.units import mm

OUT = "/private/tmp/claude-501/-Users-macbook-Downloads-claude/65498e3e-5ddf-47a6-b100-3ac535d1faa0/scratchpad/rfe_sfar/output/Fiche_SFAR_Intubation_Difficile_Adulte_2017.pdf"

SOURCE_TXT = ("Source : Recommandations Formalisées d'Experts SFAR « Intubation difficile et "
              "extubation en anesthésie chez l'adulte » (actualisation de la Conférence d'Experts "
              "Intubation difficile 2006) — Anesth Reanim. 2017;3:552-571, texte validé par le CA "
              "SFAR le 29/06/2017. Méthodologie GRADE. "
              "Fiche de synthèse non officielle : se référer au texte intégral.")

def P(txt, style=S_CELL):
    return Paragraph(txt, style)

def chip(label, **kw):
    return grade_chip(label, **kw)

def reco_table(rows, col_widths):
    """rows: (ref, text, grade_label_for_chip)"""
    data = [[P("Réf.", S_HEAD_W), P("Recommandation", S_HEAD_W), P("Grade", S_HEAD_W_C)]]
    for ref, txt, grade in rows:
        data.append([P(ref, S_CELL_B), P(txt, S_CELL), chip(grade)])
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

def no_reco_panel(text):
    return info_panel(P("<b>Pas de recommandation</b> — " + text, S_BODY_SM), bg=GREY_LIGHT, border=GREY)

def simple_table(header, rows, col_widths):
    data = [[P(h, S_HEAD_W) for h in header]]
    for r in rows:
        data.append([P(c, S_CELL) for c in r])
    t = Table(data, colWidths=col_widths, repeatRows=1)
    st = [
        ("BACKGROUND",(0,0),(-1,0), TEAL_DARK), ("TEXTCOLOR",(0,0),(-1,0), WHITE),
        ("FONTNAME",(0,0),(-1,0), FONT_BOLD), ("FONTSIZE",(0,0),(-1,0), 8),
        ("GRID",(0,0),(-1,-1),0.5,GREY_LIGHT), ("VALIGN",(0,0),(-1,-1),"TOP"),
        ("TOPPADDING",(0,0),(-1,-1),3.4), ("BOTTOMPADDING",(0,0),(-1,-1),3.4), ("LEFTPADDING",(0,0),(-1,-1),5),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            st.append(("BACKGROUND",(0,i),(-1,i), BG_PANEL))
    t.setStyle(TableStyle(st))
    return t

def legend_flowable():
    items = [("1+", "Il faut faire"), ("1-", "Il ne faut pas faire"),
             ("2+", "Il faut probablement"), ("2-", "Il ne faut probablement pas")]
    content_w = PAGE_W - 2*MARGIN
    n = len(items)
    chip_w = 15*mm
    text_w = (content_w - n*chip_w) / n
    row_cells, col_widths = [], []
    for g, txt in items:
        row_cells.append(chip(g, width=chip_w-1.5*mm))
        row_cells.append(P(txt, S_BADGE_HEAD))
        col_widths += [chip_w, text_w]
    row = Table([row_cells], colWidths=col_widths)
    row.setStyle(TableStyle([("VALIGN",(0,0),(-1,-1),"MIDDLE"), ("LEFTPADDING",(0,0),(-1,-1),1), ("RIGHTPADDING",(0,0),(-1,-1),1)]))
    return row

TOTAL_PAGES = {"n": 11}

def on_page(canvas, doc, page_title):
    header_band(canvas, doc, "SFAR — RFE 2017 — FICHE DE SYNTHÈSE",
                "Intubation difficile & extubation (adulte)",
                page_title, icon_fn=lambda c,x,y: icon_pill(c, x, y, 13*mm), color=NAVY)
    footer_band(canvas, doc, SOURCE_TXT, f"Page {doc.page} / {TOTAL_PAGES['n']}")

# ---------------------------------------------------------------------------
def _section_intro():
    story = []
    story.append(Spacer(1, 3*mm))
    story.append(info_panel(P(
        "<b>Champ :</b> actualisation de la Conférence d'Experts « Intubation difficile » de 2006 — "
        "prévention de la désaturation, place des vidéolaryngoscopes, anesthésie et curarisation en "
        "situation difficile, critères d'extubation à risque, et synthèse sous forme d'algorithmes. "
        "Comité de 13 experts, méthode GRADE®, format PICO, 6 questions.<br/><br/>"
        "<b>Résultats (résumé officiel) :</b> 13 recommandations formalisées ; 5 de niveau de preuve "
        "élevé (Grade 1), 8 de niveau de preuve faible (Grade 2). Accord fort obtenu pour "
        "<b>99 %</b> des recommandations — une seule (R2.3) n'a recueilli qu'un accord faible, "
        "reproduit fidèlement ci-dessous plutôt que reformulé en « accord fort ».",
        S_BODY), bg=BG_PANEL, border=TEAL))
    story.append(Spacer(1, 3*mm))

    story.append(section_bar("Légende des grades (méthodologie GRADE)"))
    story.append(Spacer(1, 2*mm))
    story.append(legend_flowable())
    story.append(Spacer(1, 4*mm))

    story.append(section_bar("Les 6 questions traitées par la RFE"))
    story.append(Spacer(1, 2*mm))
    cw = PAGE_W - 2*MARGIN
    story.append(simple_table(
        ["#", "Question"],
        [
            ["1", "Techniques de préoxygénation et d'oxygénation apnéique pour éviter la désaturation lors des manœuvres d'intubation"],
            ["2", "Vidéolaryngoscopes vs laryngoscopie standard pour faciliter l'exposition trachéale (intubation difficile prévue, hors fibroscopie)"],
            ["3", "AIVOC/AINOC vs sédation par bolus pour le contrôle des voies aériennes en respiration spontanée"],
            ["4", "Anesthésie et curarisation chez un patient avec critères d'intubation difficile et ventilation au masque potentiellement difficile"],
            ["5", "Critères permettant d'anticiper les difficultés d'extubation trachéale postopératoire"],
            ["6", "Arbres décisionnels et algorithmes pour optimiser la prise en charge d'une difficulté prévue ou non"],
        ],
        [cw*0.08, cw*0.92]))
    return story

def _section_q1():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Question 1 — Préoxygénation et oxygénation apnéique"))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("R1.1", "Il faut prévenir systématiquement la désaturation artérielle en oxygène lors des "
         "manœuvres d'intubation trachéale ou d'insertion de dispositif supraglottique en raison "
         "des conséquences en termes de morbidité et de mortalité lors de sa survenue.", "1+"),
        ("R1.2", "Afin de prévenir une désaturation artérielle lors des manœuvres d'intubation "
         "trachéale ou d'insertion de dispositif supraglottique, il faut réaliser systématiquement "
         "une procédure de préoxygénation (3 min / 8 inspirations profondes), y compris dans le "
         "cadre de l'urgence.", "1+"),
        ("R1.3", "Dans certains cas, il faut probablement utiliser des techniques d'oxygénation "
         "apnéique avec des techniques spécifiques pour prévenir une désaturation artérielle en "
         "oxygène.", "2+"),
    ], [14*mm, PAGE_W-2*MARGIN-14*mm-20*mm, 20*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(P("NAP4 (Royaume-Uni) : l'intubation difficile ou l'échec d'intubation représentait "
                    "39 % des incidents liés au contrôle des voies aériennes. Sans préoxygénation, "
                    "désaturation &lt; 90 % chez 30-60 % des patients ASA I. Délai de désaturation : "
                    "1-2 min en air ambiant, prolongé à 6-8 min après préoxygénation en O2 pur. "
                    "FeO2 &gt; 90 % = préoxygénation efficace. Position proclive (20-30°) : bénéfice "
                    "démontré chez l'obèse (délai de désaturation +30 %, jusqu'à 3,5 min vs 2,5 min "
                    "en décubitus dorsal) et en population générale ; bénéfice non démontré chez la "
                    "femme enceinte malgré l'augmentation de CRF. Oxygénation apnéique (canule "
                    "nasale 5 L/min ou oxygène nasal à haut débit) : particulièrement utile chez "
                    "l'obèse (doublement du délai de désaturation) et en cas d'intubation difficile "
                    "prévue ou en technique de sauvetage.", S_NOTE))
    return story

def _section_q2a():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Question 2 (1/2) — Vidéolaryngoscopes : intubation difficile prévue"))
    story.append(Spacer(1, 2*mm))
    story.append(info_panel(P(
        "<b>Prérequis</b> — un vidéolaryngoscope ne doit pas être utilisé si : ouverture de bouche "
        "&lt; 2,5 cm • rachis cervical fixé en flexion • tumeur des voies aérodigestives supérieures "
        "avec stridor. Vérifier la possibilité d'introduction avant d'endormir le patient. Dans le "
        "cas d'une induction en séquence rapide pour estomac plein, les données de la littérature "
        "ne permettent pas de formuler de recommandation concernant l'utilisation des "
        "vidéolaryngoscopes. Une désaturation &lt; 95 % impose l'arrêt des manœuvres d'intubation "
        "au profit de l'oxygénation — le vidéolaryngoscope ne peut pas se substituer à un "
        "dispositif supraglottique en cas de risque avéré d'hypoxémie.",
        S_BODY_SM), bg=AMBER_LIGHT, border=AMBER))
    story.append(Spacer(1, 3*mm))
    story.append(reco_table([
        ("R2.1", "Dans le cadre d'une chirurgie programmée, il faut utiliser en première intention "
         "les vidéolaryngoscopes chez les patients avec une ventilation au masque possible et au "
         "moins deux critères d'intubation difficile.", "1+"),
    ], [14*mm, PAGE_W-2*MARGIN-14*mm-20*mm, 20*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(P("Chez les patients avec ≥ 2 facteurs prédictifs (dont Mallampati III/IV), les "
                    "vidéolaryngoscopes améliorent la vision glottique et le taux de succès à la "
                    "première tentative vs lame de Macintosh. En cas de rachis cervical pathologique, "
                    "une méta-analyse montre un taux de succès plus élevé, une meilleure vision et "
                    "moins de complications avec un Airtraq® qu'avec une lame Macintosh classique. "
                    "Chez l'obèse (IMC &gt; 30 kg/m²) : meilleure visualisation, meilleur taux de "
                    "succès, moins de désaturation &lt; 92 %.", S_NOTE))
    story.append(Spacer(1, 3*mm))
    story.append(no_reco_panel("La durée nécessaire pour une intubation trachéale avec un "
                                "vidéolaryngoscope peut être plus courte, identique ou plus longue "
                                "qu'avec une lame de Macintosh (paramètre dépendant du dispositif, de "
                                "l'opérateur et du terrain) : les vidéolaryngoscopes ne peuvent pas "
                                "être proposés systématiquement en première intention chez les "
                                "patients à risque de régurgitation et d'inhalation (estomac plein) — "
                                "la manœuvre de Sellick pourrait altérer la vision glottique sous "
                                "vidéolaryngoscope."))
    story.append(Spacer(1, 3*mm))
    story.append(info_panel(P(
        "<b>Prérequis</b> — chez le patient avec une intubation difficile <b>non prévue</b>, une à "
        "deux laryngoscopies par un praticien expert sont effectuées en première intention, en "
        "utilisant tous les moyens d'optimisation possibles (repositionnement de la tête du "
        "patient, long mandrin béquillé type Eschmann, appui laryngé externe BURP) pour visualiser "
        "la glotte et parvenir à intuber la trachée. Le mandrin béquillé fait partie de la "
        "première étape de la stratégie d'optimisation de la gestion des voies aériennes en cas "
        "d'intubation difficile non prévue.",
        S_BODY_SM), bg=AMBER_LIGHT, border=AMBER))
    story.append(Spacer(1, 3*mm))
    story.append(reco_table([
        ("R2.2", "Si une intubation difficile n'est pas prévue, il faut probablement utiliser les "
         "vidéolaryngoscopes en seconde intention chez les patients avec un stade de Cormack et "
         "Lehane III ou plus, si la ventilation au masque est possible.", "2+"),
    ], [14*mm, PAGE_W-2*MARGIN-14*mm-20*mm, 20*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(P("Réduit l'incidence des scores Cormack-Lehane III/IV observés initialement en "
                    "laryngoscopie directe. Étude rétrospective multicentrique (7 centres, "
                    "2004-2013, 1427 échecs de laryngoscopie directe) : la vidéolaryngoscopie est la "
                    "méthode de secours la plus utilisée en première intention, avec le taux de "
                    "succès le plus élevé parmi les dispositifs de secours.", S_NOTE))
    return story

def _section_q2b():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Question 2 (2/2) — Vidéolaryngoscopes en ventilation spontanée"))
    story.append(Spacer(1, 2*mm))
    story.append(info_panel(P(
        "<b>Prérequis</b> — en cas d'intubation impossible, la fibroscopie reste la méthode de "
        "référence (indication privilégiée : tumeurs de la base de langue). En cas de stridor "
        "associé à une détresse respiratoire, une trachéotomie première doit être envisagée en "
        "première intention. En cas d'échec de fibroscopie, les vidéolaryngoscopes ont "
        "probablement une place chez les patients avec une ouverture de bouche suffisante "
        "(&gt; 2,5 cm), seuls ou en association. Quelle que soit la technique choisie en cas "
        "d'intubation et ventilation au masque difficiles, le patient sédaté doit garder une "
        "respiration spontanée efficace.",
        S_BODY_SM), bg=AMBER_LIGHT, border=AMBER))
    story.append(Spacer(1, 3*mm))
    story.append(reco_table([
        ("R2.3", "Il faut probablement utiliser les vidéolaryngoscopes en technique alternative à "
         "l'utilisation du fibroscope chez les patients en ventilation spontanée, avec des critères "
         "d'intubation prévue difficile ou impossible et de ventilation au masque difficile.", "2+"),
    ], [14*mm, PAGE_W-2*MARGIN-14*mm-20*mm, 20*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(info_panel(P(
        "<b>Seule recommandation de cette RFE à ne pas avoir recueilli d'« Accord FORT »</b> — son "
        "grade est explicitement qualifié d'« Accord faible » dans le texte source, reproduit tel "
        "quel (les 12 autres recommandations ont toutes recueilli un Accord FORT).",
        S_BODY_SM), bg=GREY_LIGHT, border=GREY))
    story.append(Spacer(1, 2*mm))
    story.append(P("Peu d'études disponibles. Intubation orale ou nasale sous vidéolaryngoscopie en "
                    "ventilation spontanée réalisable par des opérateurs entraînés, avec une "
                    "technique de sédation (anesthésie topique + AIVOC rémifentanil) comparable à "
                    "celle de la fibro-intubation — technique alternative acceptable pour des "
                    "ouvertures buccales ≥ 2,5 cm, hors pathologie tumorale, chez des opérateurs "
                    "expérimentés.", S_NOTE))
    return story

def _section_q4():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Questions 3-4 — Anesthésie et curarisation"))
    story.append(Spacer(1, 2*mm))
    story.append(no_reco_panel("Faut-il utiliser l'AIVOC/AINOC plutôt que la sédation par bolus pour "
                                "le contrôle des voies aériennes en cas de difficulté suspectée ou "
                                "avérée chez un patient en respiration spontanée ? La CE/ID de 2006 "
                                "précisait déjà que l'utilisation du propofol ou du rémifentanil en "
                                "AIVOC s'accompagne d'un risque faible de désaturation, améliore les "
                                "conditions d'intubation pour l'opérateur et le confort du patient — "
                                "le rémifentanil permet une meilleure coopération. Les données "
                                "récentes de la littérature ne permettent pas de formuler une "
                                "nouvelle proposition au-delà de ce constat déjà établi."))
    story.append(Spacer(1, 3*mm))
    story.append(P("Il est indispensable de s'assurer de la disponibilité des techniques "
                    "d'oxygénation avant d'envisager une anesthésie générale.", S_BODY_SM))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("R4.1", "Il faut maintenir un niveau d'anesthésie profond afin d'optimiser les conditions "
         "de ventilation au masque et d'intubation en utilisant des agents rapidement réversibles.", "1+"),
        ("R4.2", "En cas d'intubation difficile prévue, il faut probablement utiliser un curare afin "
         "d'améliorer les conditions de ventilation au masque et d'intubation, en utilisant un "
         "curare d'action courte ou rapidement inactivée sous couvert du monitorage systématique de "
         "la curarisation.", "2+"),
    ], [14*mm, PAGE_W-2*MARGIN-14*mm-20*mm, 20*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(P("Propofol et sévoflurane = hypnotiques de choix (action rapidement réversible). "
                    "L'administration d'un curare en cas d'obstruction des voies aériennes "
                    "supérieures est un standard chez l'adulte, y compris quand une trachéotomie de "
                    "sauvetage est décidée — tester la ventilation au masque avant l'injection de "
                    "curare ne repose sur aucune donnée publiée. Deux curares d'action courte ou "
                    "rapidement inactivée : succinylcholine 1 mg/kg (poids réel), ou rocuronium "
                    "0,6 mg/kg (1,0 mg/kg en ISR), inactivable même en cas de bloc profond par "
                    "sugammadex 8-16 mg/kg selon la dose de rocuronium et le délai — la dose "
                    "nécessaire de sugammadex doit être immédiatement disponible en cas d'usage du "
                    "rocuronium pour une intubation difficile prévue.", S_NOTE))
    return story

def _section_q5a():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Question 5 (1/2) — Critères et stratégie d'extubation"))
    story.append(Spacer(1, 2*mm))
    story.append(info_panel(P(
        "<b>Prérequis — conditions de sécurité pour extuber</b> : TOF quantitatif &gt; 90 % "
        "(l'absence de signal fiable doit faire poser la question de l'antagonisation "
        "systématique) • respiration spontanée régulière avec échanges gazeux satisfaisants • "
        "conditions hémodynamiques satisfaisantes • patient éveillé (ouverture des yeux/réponse "
        "aux ordres/sans agitation), sauf décision d'extuber sous anesthésie • absence de risque "
        "immédiat de complication chirurgicale.",
        S_BODY_SM), bg=AMBER_LIGHT, border=AMBER))
    story.append(Spacer(1, 3*mm))
    story.append(reco_table([
        ("R5.1", "Il faut probablement adapter la prise en charge aux facteurs de risque d'échec "
         "d'extubation car la réintubation est source d'une surmorbidité et de surmortalité.", "2+"),
        ("R5.2", "Il faut probablement rechercher des facteurs de risque d'échec avant extubation.", "2+"),
    ], [14*mm, PAGE_W-2*MARGIN-14*mm-20*mm, 20*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(P("Facteurs de risque de réintubation postopératoire : curarisation résiduelle, "
                    "facteurs humains évitables (inexpérience, absence de procédures), facteurs "
                    "médicaux (réserves cardiaque/respiratoire limitées — BPCO et insuffisance "
                    "cardiaque dominent), obstruction des voies aériennes, dénutrition. Chirurgies à "
                    "risque : chirurgie lourde (vasculaire, transplantation, neurochirurgie, "
                    "thoracique, cardiaque), chirurgie tête et cou, chirurgie longue (&gt; 4h) en "
                    "position déclive avec remplissage sans monitorage et sonde &gt; 7,5 mm. Enquête "
                    "prospective : 38 incidents post-extubation (20 en SOP, 2 pendant le transport, "
                    "16 en SSPI) — 4 causes principales : laryngospasme, morsure du tube "
                    "(anoxie/œdème à pression négative), caillot obstructif, œdème cervical après "
                    "position de Trendelenburg prolongée ; 16/38 en chirurgie ORL. Test de fuite non "
                    "reconnu fiable en anesthésie (contrairement à la réanimation).", S_NOTE))
    return story

def _section_q5b():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Question 5 (2/2) — Mesures préventives et prise en charge"))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("R5.3", "Il faut probablement extuber un patient en suivant une stratégie rigoureuse.", "2+"),
        ("R5.4", "Il faut probablement prendre des mesures préventives en présence de facteurs de "
         "risque de difficultés d'extubation.", "2+"),
    ], [14*mm, PAGE_W-2*MARGIN-14*mm-20*mm, 20*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(P("<b>Stratégie rigoureuse d'extubation :</b> utiliser un algorithme dédié • "
                    "extuber en position demi-assise (obèse/SAOS) ou décubitus latéral si doute sur "
                    "la vacuité gastrique • dégonfler le ballonnet à la seringue • aspirer la bouche "
                    "en évitant les aspirations endotrachéales • prévenir les morsures de sonde "
                    "avant l'extubation, y compris pendant le transport • FiO2 = 1 et retrait en "
                    "pression positive, en fin d'inspiration • oxygéner et contrôler immédiatement "
                    "la reprise d'une ventilation spontanée de qualité (capnographe) • présence de "
                    "2 professionnels de santé, dont un médecin anesthésiste-réanimateur disponible "
                    "sans délai.<br/><br/>"
                    "<b>Mesures préventives si facteurs de risque :</b> leadership pour dérouler "
                    "l'algorithme de façon coordonnée • extubation seulement si matériel "
                    "d'oxygénation/réintubation disponible et 2 personnes présentes • attitude "
                    "consensuelle avec les opérateurs (item n°9 de la check-list HAS). En cas de "
                    "risque, options : extubation différée, trachéotomie, ou extubation sur guide "
                    "échangeur creux (efficace pour les réintubations dans les 10h postopératoires ; "
                    "échecs 7-14 %, surtout avec les petits diamètres ; ne pas laisser en place "
                    "&gt; 24h ; oxygénation par jet-ventilation manuelle réservée à l'extrême "
                    "urgence, risque de barotraumatisme). Information écrite du patient sur les "
                    "circonstances de la difficulté rencontrée.", S_NOTE))
    return story

def _section_q6():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Question 6 — Arbres décisionnels et algorithmes"))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("R6.1", "Il faut s'appuyer sur des arbres décisionnels ou algorithmes pour optimiser la "
         "gestion d'un contrôle difficile des voies aériennes.", "1+"),
    ], [14*mm, PAGE_W-2*MARGIN-14*mm-20*mm, 20*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(P("Priorité absolue : le maintien de l'oxygénation du patient en toutes "
                    "circonstances — dénominateur commun et intemporel de tous les algorithmes. "
                    "Accepter à temps l'échec d'une intubation trachéale (2 tentatives maximum) et "
                    "l'appel à l'aide (renfort technique et/ou anesthésiste senior) doivent être la "
                    "règle devant toute situation imprévue d'oxygénation et/ou d'intubation "
                    "difficiles. Il n'est pas souhaitable de pratiquer une laryngoscopie pour évaluer "
                    "la difficulté quand celle-ci est prévue/prévisible (profondeur d'anesthésie "
                    "insuffisante, risque de situation critique).", S_NOTE))
    story.append(Spacer(1, 4*mm))

    story.append(section_bar("Algorithme 1 — Intubation difficile prévue", color=GREY))
    story.append(Spacer(1, 1.5*mm))
    story.append(P("Transcrit intégralement depuis le rendu visuel de la source (pages 565-566, "
                    "pures images).", S_NOTE))
    story.append(Spacer(1, 2*mm))
    cw = PAGE_W - 2*MARGIN
    story.append(simple_table(
        ["Étape", "Décision / actions", "Résultat / suite"],
        [
            ["Orientation stratégique", "Évaluer la difficulté prévisible de la ventilation au "
             "masque facial → prévoir le maintien de l'oxygénation (masque laryngé ou masque "
             "laryngé pour l'intubation utilisables ? abord trachéal possible ? repérage "
             "échographique préalable ?) → choix des techniques d'anesthésie (apnée ou ventilation "
             "spontanée ?).", "—"],
            ["Si apnée possible", "1 critère ID : laryngoscope. ≥ 2 critères ID : "
             "vidéolaryngoscope. Dans tous les cas : 2 essais maximum, exposition glottique "
             "optimisée, possibilité de long mandrin béquillé.", "Succès → intubation. Échec → "
             "masque laryngé pour l'intubation (± fibroscope) → succès : intubation ± fibroscope / "
             "échec : réveil."],
            ["Si ventilation spontanée", "Aide prévue systématique. Masque laryngé pour "
             "l'intubation.", "Succès → intubation. Échec → fibroscope → succès : intubation / "
             "échec : réveil, abord trachéal si réveil impossible."],
        ],
        [cw*0.22, cw*0.50, cw*0.28]))
    return story

def _section_algo_non_prevue():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Algorithme 2 — Intubation difficile non prévue", color=GREY))
    story.append(Spacer(1, 1.5*mm))
    story.append(P("Transcrit depuis le rendu visuel de la source (page 568). Appel à l'aide dans "
                    "tous les cas + chariot d'intubation difficile + maintien de l'anesthésie + "
                    "leadership.", S_NOTE))
    story.append(Spacer(1, 2*mm))
    cw = PAGE_W - 2*MARGIN
    story.append(simple_table(
        ["Étape", "Décision / actions", "Résultat / suite"],
        [
            ["Ventilation au masque facial", "Évaluer immédiatement l'efficacité de la "
             "ventilation.", "Efficace → 1 critère ID : laryngoscope ; ≥ 2 critères ID : "
             "vidéolaryngoscope (2 essais max) → échec → masque laryngé pour l'intubation. "
             "Inefficace → masque laryngé pour l'intubation directement."],
            ["Masque laryngé pour l'intubation", "Évaluer l'efficacité de la ventilation à travers "
             "le dispositif.", "Efficace → Algorithme de l'intubation (Algorithme 1, arbre détaillé "
             "page précédente). Inefficace → Algorithme de l'oxygénation (Algorithme 3, ci-dessous)."],
        ],
        [cw*0.22, cw*0.40, cw*0.38]))
    story.append(Spacer(1, 5*mm))

    story.append(section_bar("Algorithme 3 — Oxygénation : ventilation au masque inefficace et échec d'intubation", color=RED))
    story.append(Spacer(1, 1.5*mm))
    story.append(P("Transcrit depuis le rendu visuel de la source (page 567). Appel à l'aide dans "
                    "tous les cas + leadership.", S_NOTE))
    story.append(Spacer(1, 2*mm))
    story.append(simple_table(
        ["Étape", "Décision / actions", "Résultat / suite"],
        [
            ["1re étape", "Masque laryngé pour l'intubation (DSG).", "Succès → intubation ou "
             "réveil. Échec/contre-indication → O2 transtrachéal."],
            ["2e étape", "O2 transtrachéal.", "Succès → réveil ou poursuite (autres techniques "
             "d'intubation / cricothyroïdotomie-trachéotomie). Échec → cricothyroïdotomie/"
             "trachéotomie directement."],
            ["3e étape (si autres techniques d'intubation tentées)", "Autres techniques "
             "d'intubation.", "Succès → intubation. Échec → réveil ou cricothyroïdotomie/"
             "trachéotomie."],
        ],
        [cw*0.24, cw*0.36, cw*0.40]))
    return story

def _section_algo_extubation():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Algorithme 4 — Extubation : facteurs de risque", color=GREY))
    story.append(Spacer(1, 1.5*mm))
    story.append(P("Transcrit depuis le rendu visuel de la source (page 562). Point d'entrée : "
                    "critères d'extubation présents et minimisation du risque d'inhalation (patient "
                    "éveillé en position assise, décurarisation complète, vidange de l'estomac, "
                    "stabilité hémodynamique).", S_NOTE))
    story.append(Spacer(1, 2*mm))
    cw = PAGE_W - 2*MARGIN
    story.append(simple_table(
        ["Branche", "Facteurs / actions", "Suite"],
        [
            ["Chirurgie à risque — facteurs locaux", "Chirurgie cervico-faciale, œdème cervical, "
             "modifications anatomiques des VAS, risque de reprise chirurgicale, position proclive "
             "prolongée, intubation traumatique, SAOS.", "→ Guide échangeur, trachéotomie ou "
             "masque laryngé, report de l'extubation, VNI si SAOS."],
            ["Chirurgie à risque — facteurs généraux", "BPCO, insuffisance cardiaque.",
             "→ Oxygénothérapie, oxygène nasal à haut débit, CPAP/VNI, optimisation médicale."],
            ["Les deux branches convergent vers", "—", "Réanimation / soins continus / "
             "hospitalisation conventionnelle, avec une durée de surveillance fixée (risque de "
             "dégradation retardée)."],
            ["Actions parallèles", "Évaluer les facteurs de risque d'échec locaux et/ou généraux "
             "d'extubation.", "→ Décision d'extuber (leadership +++, prudence si association de "
             "facteurs locaux et généraux) → gestion du transport et surveillance adaptée."],
        ],
        [cw*0.26, cw*0.42, cw*0.32]))
    story.append(Spacer(1, 5*mm))

    story.append(section_bar("Algorithme 5 — Extubation : leadership et décision", color=GREY))
    story.append(Spacer(1, 1.5*mm))
    story.append(P("Transcrit depuis le rendu visuel de la source (page 563). Point d'entrée : "
                    "leadership de la procédure (considérer le risque d'inhalation post-extubation, "
                    "l'hyper-réactivité bronchique des VAS) → deux professionnels de santé dont un "
                    "médecin anesthésiste-réanimateur disponible sans délai, matériel d'oxygénation "
                    "prêt à l'usage → consensus dans l'équipe d'anesthésie, concertation avec "
                    "l'opérateur.", S_NOTE))
    story.append(Spacer(1, 2*mm))
    story.append(simple_table(
        ["Choix", "Actions", "Suite"],
        [
            ["Choix d'extuber", "Extubation simple ou sur guide creux ; extubation différée sans "
             "sédation en SSPI ou réanimation.", "→ Maintien de l'oxygénation en position assise, "
             "sous oxygène voire sous VNI → fixer un lieu de surveillance adapté au risque."],
            ["Choix de ne pas extuber", "Maintien de l'anesthésie ; trachéotomie.",
             "→ Transmettre par écrit le risque et la conduite à tenir."],
        ],
        [cw*0.20, cw*0.44, cw*0.36]))
    return story

def _section_synthese():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Synthèse et messages clés"))
    story.append(Spacer(1, 2*mm))
    story.append(P(
        "• Préoxygénation systématique (3 min / 8 inspirations profondes), y compris en urgence ; "
        "position proclive chez l'obèse ; oxygénation apnéique en complément dans les situations à "
        "risque.<br/>"
        "• Vidéolaryngoscope en 1re intention si ≥ 2 critères d'intubation difficile et ventilation "
        "au masque possible ; en 2e intention (Cormack-Lehane III+) si intubation difficile non "
        "prévue ; pas de recommandation systématique en cas de risque de régurgitation.<br/>"
        "• Anesthésie profonde avec agents rapidement réversibles ; curare d'action courte "
        "(succinylcholine 1 mg/kg, ou rocuronium 0,6-1,0 mg/kg + sugammadex disponible) si "
        "intubation difficile prévue, sous monitorage systématique.<br/>"
        "• TOF &gt; 90 % avant toute extubation ; rechercher activement les facteurs de risque "
        "locaux (chirurgie cervico-faciale, œdème, SAOS) et généraux (BPCO, insuffisance "
        "cardiaque) ; leadership et présence de 2 professionnels dont un anesthésiste-réanimateur "
        "disponible sans délai.<br/>"
        "• S'appuyer systématiquement sur les algorithmes — 2 tentatives maximum avant d'accepter "
        "l'échec et d'appeler à l'aide ; priorité absolue : maintenir l'oxygénation en toutes "
        "circonstances.<br/>"
        "• Connaître la filière de secours en cas d'échec combiné ventilation/intubation : masque "
        "laryngé pour l'intubation → O2 transtrachéal → cricothyroïdotomie/trachéotomie.",
        S_BODY))
    story.append(Spacer(1, 5*mm))

    story.append(section_bar("Sources et traçabilité", color=GREY))
    story.append(Spacer(1, 2*mm))
    story.append(P(
        "<b>Document source :</b> « Intubation difficile et extubation en anesthésie chez l'adulte » "
        "(actualisation de la Conférence d'Experts Intubation difficile 2006) — Recommandations "
        "Formalisées d'Experts SFAR, Anesth Reanim. 2017;3:552-571. Comité de 13 experts, "
        "coordination O. Langeron, K. Nouette-Gaulain. Texte validé par le CA SFAR le 29/06/2017.", S_SOURCE))
    story.append(Spacer(1, 1.5*mm))
    story.append(P("<b>Méthodologie :</b> GRADE®, tags « (Grade X+/-) Accord FORT » (ou « Accord "
                    "faible » pour R2.3) imprimés littéralement après chaque recommandation — cités "
                    "ici tels quels.", S_SOURCE))
    story.append(Spacer(1, 1.5*mm))
    story.append(P("<b>Couverture :</b> 13 recommandations (R1.1-R1.3, R2.1-R2.3, R4.1-R4.2, "
                    "R5.1-R5.4, R6.1 — pas de R3, la question 3 a abouti à « pas de recommandation ») "
                    "et 2 questions « pas de recommandation » reproduites intégralement, ainsi que "
                    "les 6 algorithmes-diagrammes (pages 562-563 et 565-568 de la source, pures "
                    "images sans texte extractible, vérifiés visuellement et retranscrits "
                    "intégralement sous forme de tableaux structurés).", S_SOURCE))
    story.append(Spacer(1, 3*mm))
    story.append(info_panel(P(
        "<b>Avertissement :</b> ce document est une fiche de synthèse indépendante, produite pour un "
        "usage d'aide-mémoire. Il reprend l'intégralité des recommandations de la RFE mais ne "
        "remplace pas le texte intégral et n'est ni édité ni validé par la SFAR. En cas de doute, se "
        "référer au texte intégral, aux recommandations ultérieures et/ou à un avis spécialisé.",
        S_BODY_SM), bg=GREY_LIGHT, border=GREY))
    return story

SECTIONS = [
    ("Introduction, méthodologie & les 6 questions", _section_intro),
    ("Q1 — Préoxygénation & oxygénation apnéique", _section_q1),
    ("Q2 (1/2) — Vidéolaryngoscopes : intubation prévue", _section_q2a),
    ("Q2 (2/2) — Vidéolaryngoscopes en ventilation spontanée", _section_q2b),
    ("Q3-Q4 — Anesthésie & curarisation", _section_q4),
    ("Q5 (1/2) — Critères et stratégie d'extubation", _section_q5a),
    ("Q5 (2/2) — Mesures préventives d'extubation", _section_q5b),
    ("Q6 — Algorithmes : principes & intubation prévue", _section_q6),
    ("Algorithmes 2-3 — Intubation non prévue & oxygénation", _section_algo_non_prevue),
    ("Algorithmes 4-5 — Extubation", _section_algo_extubation),
    ("Synthèse, sources & traçabilité", _section_synthese),
]

def _make_doc():
    return SimpleDocTemplate(OUT, pagesize=A4,
                              leftMargin=MARGIN, rightMargin=MARGIN,
                              topMargin=32*mm, bottomMargin=16*mm,
                              title="Fiche SFAR 2017 - Intubation difficile et extubation chez l'adulte",
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
    import pypdf
    doc = _make_doc()
    doc.build(story_flowables, onFirstPage=_silent_page, onLaterPages=_silent_page)
    return len(pypdf.PdfReader(OUT).pages)

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
