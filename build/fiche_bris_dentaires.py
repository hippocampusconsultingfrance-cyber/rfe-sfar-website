# -*- coding: utf-8 -*-
"""
Fiche de synthese - RFE commune SFAR / Adarpef / SFSCMF, 2012
"Bris dentaires perianesthesiques : texte court". K. Nouette-Gaulain et al.,
Ann Fr Anesth Reanim 2012;31:272-275, doi 10.1016/j.annfar.2012.01.003.
Disponible sur Internet le 24 fevrier 2012.
Source telechargee : sfar.org/wp-content/uploads/2015/09/2_AFAR_COURT_Bris-dentaires-
perianesthesiques-copie.pdf (4 pages, texte integral capture - aucune page de reference
bibliographique separee, le document est un texte court sans bibliographie imprimee).

METHODOLOGIE : PAS de systeme GRADE (aucune mention "GRADE", aucun tag "1+/2+" nulle
part dans le texte). La source imprime UNE SEULE mention de force, globale et non
individuelle, immediatement apres l'introduction : « Toutes les propositions ont recu
un accord fort lors des votes par le groupe de travail. » - il n'existe donc PAS de
distinction fort/faible entre propositions individuelles dans ce document (a la
difference de fiche_aap_urgence.py ou fiche_nutrition.py, qui melangent les deux).
CONVENTION DE CHIP (meme precedent que fiche_aap_programmee.py, seule autre fiche du
corpus a n'avoir QUE des propositions a "accord fort") : chip unique "Fort" (extension
locale non invasive de GRADE_COLORS, vert, meme poids visuel que 1+) pour les 31
propositions - jamais un GRADE 1+/2+ invente. La variabilite du verbe employe par la
source elle-meme ("il faut" / "il faut probablement" / "il ne faut probablement pas" /
"il ne faut pas") est conservee TELLE QUELLE dans le texte de chaque proposition (elle
reflete une nuance de formulation de l'expert-redacteur, pas une force de vote distincte
- la source ne definit nulle part cette variabilite verbale comme un systeme de gradation
formel, contrairement a fiche_douleur_postoperatoire ou ce codage verbal EST la
methodologie explicitement definie par la source). Ne pas confondre les deux conventions.

COMPTAGE VERIFIE (script, regex sur le texte source aplati) : 31 propositions numerotees
consecutivement 1 a 31, sans lacune, reparties sur 3 chapitres / 10 questions. Plus 5
encarts "Proposition enfant" non numerotes (addenda pediatriques rattaches a des
propositions specifiques, jamais confondus avec une proposition numerotee a part entiere).
Le groupe de travail suggere que les propositions 1, 2, 3, 6, 9, 11 et 23 puissent faire
l'objet d'une evaluation des pratiques professionnelles (EPP) - disclosure reprise telle
quelle, en note de synthese plutot qu'en un chip invente.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from style import *
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.units import mm

GRADE_COLORS["Fort"] = (GREEN, WHITE)

OUT = "/home/user/rfe-sfar-website/output/Fiche_SFAR_Bris_Dentaires_2012.pdf"

SOURCE_TXT = ("Source : « Bris dentaires périanesthésiques : texte court » — SFAR / "
              "Adarpef / SFSCMF, RFE 2012 (Ann Fr Anesth Reanim 2012;31:272-275). Fiche "
              "de synthèse non officielle : se référer au texte intégral.")

def P(txt, style=S_CELL):
    return Paragraph(txt, style)

def chip(label, **kw):
    return grade_chip(label, **kw)

def reco_table(rows, col_widths):
    """rows: (ref, text, grade_label)"""
    data = [[P("N°", S_HEAD_W_C), P("Proposition", S_HEAD_W), P("Accord", S_HEAD_W_C)]]
    for ref, txt, grade in rows:
        data.append([P(ref, S_CELL_B), P(txt, S_CELL), chip(grade)])
    t = Table(data, colWidths=col_widths, repeatRows=1)
    style_cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), NAVY), ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTNAME", (0, 0), (-1, 0), FONT_BOLD), ("FONTSIZE", (0, 0), (-1, 0), 8),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("ALIGN", (0, 0), (0, -1), "CENTER"),
        ("ALIGN", (2, 0), (2, -1), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 0.5, GREY_LIGHT),
        ("TOPPADDING", (0, 0), (-1, -1), 3.4), ("BOTTOMPADDING", (0, 0), (-1, -1), 3.4),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            style_cmds.append(("BACKGROUND", (0, i), (-1, i), BG_PANEL))
    t.setStyle(TableStyle(style_cmds))
    return t

def child_panel(text):
    return info_panel(P("<b>Proposition enfant :</b> " + text, S_BODY_SM), bg=BG_PANEL, border=TEAL)

def legend_flowable():
    chip_w = 18*mm
    content_w = PAGE_W - 2*MARGIN
    text_w = content_w - chip_w
    row = Table([[chip("Fort", width=chip_w-2*mm),
                  P("Toutes les 31 propositions du texte ont reçu un <b>accord fort</b> lors "
                    "du vote du groupe de travail — seule mention de force imprimée par la "
                    "source, globale et non individuelle (voir disclosure méthodologique "
                    "ci-dessous).", S_BADGE_HEAD)]], colWidths=[chip_w, text_w])
    row.setStyle(TableStyle([("VALIGN",(0,0),(-1,-1),"MIDDLE"), ("LEFTPADDING",(0,0),(-1,-1),1), ("RIGHTPADDING",(0,0),(-1,-1),1)]))
    return row

RCW = [12*mm, PAGE_W-2*MARGIN-12*mm-18*mm, 18*mm]

TOTAL_PAGES = {"n": 4}

def on_page(canvas, doc, page_title):
    header_band(canvas, doc, "SFAR / ADARPEF / SFSCMF — RFE 2012 — FICHE DE SYNTHÈSE",
                "Bris dentaires périanesthésiques",
                page_title, icon_fn=lambda c, x, y: icon_shield(c, x, y, 13*mm), color=NAVY)
    footer_band(canvas, doc, SOURCE_TXT, f"Page {doc.page} / {TOTAL_PAGES['n']}")

# ---------------------------------------------------------------------------
def _section_intro():
    story = []
    story.append(Spacer(1, 3*mm))
    story.append(info_panel(P(
        "<b>Champ :</b> prévention et conduite à tenir devant un bris dentaire "
        "périanesthésique — RFE commune SFAR, Association des anesthésistes "
        "réanimateurs pédiatriques d'expression française (Adarpef), Société française "
        "de stomatologie et chirurgie maxillo-faciale (SFSCMF). Texte court, <b>31 "
        "propositions</b> réparties sur 3 chapitres / 10 questions : facteurs prédictifs "
        "de bris dentaires (consultation préanesthésique, traçabilité, information du "
        "patient), prévention au bloc opératoire (choix du protocole, matériel de "
        "contrôle des voies aériennes, protection dentaire, surveillance péri- et "
        "postopératoire), conduite à tenir devant un bris dentaire constaté (prise en "
        "charge immédiate, traçabilité, déclaration, information du patient).",
        S_BODY), bg=BG_PANEL, border=TEAL))
    story.append(Spacer(1, 3*mm))
    story.append(info_panel(P(
        "<b>Méthodologie :</b> ce document ne comporte <b>aucun système GRADE</b> (pas de "
        "tag « GRADE », pas de suffixe 1+/2+ nulle part dans le texte). La source imprime "
        "<b>une seule mention de force, globale</b>, immédiatement après l'introduction : "
        "« Toutes les propositions ont reçu un accord fort lors des votes par le groupe de "
        "travail. » Il n'existe donc pas de distinction fort/faible entre propositions "
        "individuelles — chaque proposition est chippée « Fort » de façon uniforme "
        "(extension locale de la légende de ce site, jamais un GRADE numérique inventé). "
        "La formulation verbale de chaque proposition (« il faut » / « il faut "
        "probablement » / « il ne faut probablement pas » / « il ne faut pas ») est "
        "reprise telle quelle depuis la source ; elle reflète une nuance de rédaction, "
        "pas une force de vote distincte formellement définie par le document.",
        S_BODY_SM), bg=AMBER_LIGHT, border=AMBER))
    story.append(Spacer(1, 3*mm))
    story.append(section_bar("Légende"))
    story.append(Spacer(1, 2*mm))
    story.append(legend_flowable())
    return story

def _section_ch1():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(KeepTogether([
        section_bar("Chapitre 1 — Facteurs prédictifs de bris dentaires"),
        Spacer(1, 1.5*mm),
        P("<b>Q1 — Spécificités de la consultation préanesthésique</b>", S_CELL_B),
        Spacer(1, 1.5*mm),
        reco_table([
            ("1", "Rechercher les critères d'intubation difficile et de ventilation au "
             "masque difficile.", "Fort"),
            ("2", "Rechercher lors de l'interrogatoire les facteurs de risque de bris "
             "dentaires : existence de prothèses, de restaurations (dent naturelle "
             "antérieure restaurée par résine composite ou facette collée — élément très "
             "fragile) et de traitement orthodontique, de mobilité des dents et des "
             "prothèses, ou d'antécédents traumatiques ou parodontaux.", "Fort"),
            ("3", "Insérer probablement des questions relatives à l'état buccodentaire "
             "dans un questionnaire rempli par le patient en vue de la consultation "
             "d'anesthésie.", "Fort"),
            ("4", "Porter une attention particulière aux incisives supérieures et "
             "inférieures, notamment en cas de dent isolée lors de la consultation "
             "d'anesthésie.", "Fort"),
        ], RCW),
    ]))
    story.append(Spacer(1, 2.5*mm))
    story.append(KeepTogether([
        P("<b>Q2 — Traçabilité des signes cliniques prédictifs</b>", S_CELL_B),
        Spacer(1, 1.5*mm),
        reco_table([
            ("5", "Consigner les signes prédictifs d'intubation et de ventilation au "
             "masque difficile dans le compte rendu de la consultation d'anesthésie.", "Fort"),
            ("6", "Consigner de façon compréhensible (schéma dentaire simplifié "
             "conseillé) les signes relatifs à l'état dentaire sur le dossier "
             "d'anesthésie.", "Fort"),
        ], RCW),
    ]))
    story.append(Spacer(1, 2.5*mm))
    story.append(KeepTogether([
        P("<b>Q3 — Classes de risque & conduite à tenir de prévention</b>", S_CELL_B),
        Spacer(1, 1.5*mm),
        reco_table([
            ("7", "Informer le patient du risque dentaire, et lui suggérer en cas de "
             "risque identifié une prise en charge par un odonto-stomatologiste avec "
             "panoramique dentaire. Chez un patient à risque avec traitement en cours ou "
             "prévu, évoquer le report d'intervention chirurgicale ou des soins dentaires "
             "dans l'information sur le rapport bénéfice-risque.", "Fort"),
            ("8", "Il ne faut probablement pas adresser systématiquement le patient chez "
             "le dentiste et/ou le stomatologue dans les autres cas.", "Fort"),
        ], RCW),
        Spacer(1, 1.5*mm),
        child_panel("chez l'enfant, en cas de traitement orthodontique en cours limitant "
             "l'ouverture de bouche (type bielle de Herbst fixe), ou présentant un "
             "obstacle au niveau du tiers antérieur du palais (grilles antilangue, "
             "antisuccion) avec un risque de bris et d'inhalation et/ou de matériel pouvant "
             "être abîmé au cours de l'acte chirurgical intrabuccal (bistouri électrique, "
             "ouvre-bouche), il faut probablement demander un avis spécialisé (possibilité "
             "de suspendre le traitement ou de démonter le dispositif) en dehors d'un "
             "contexte d'urgence."),
    ]))
    story.append(Spacer(1, 2.5*mm))
    story.append(KeepTogether([
        P("<b>Q4 — Traçabilité de l'information donnée au patient</b>", S_CELL_B),
        Spacer(1, 1.5*mm),
        reco_table([
            ("9", "Informer oralement et remettre un document au cours d'une consultation "
             "d'anesthésie précisant que les traumatismes dentaires sont possibles au "
             "cours de toute anesthésie. La preuve de cette information doit être "
             "consignée dans le dossier d'anesthésie, au moins pour les patients avec "
             "risque de bris dentaire identifié.", "Fort"),
            ("10", "La note d'information remise au patient doit lui recommander de "
             "signaler toute prothèse ou toute fragilité dentaire particulière, notamment "
             "au niveau des incisives supérieures et inférieures.", "Fort"),
        ], RCW),
        Spacer(1, 1.5*mm),
        child_panel("en cas d'accès aux voies aériennes potentiellement difficile chez un "
             "enfant, informer les parents du risque de luxation accidentelle d'une dent "
             "temporaire ou d'une dent définitive immature."),
    ]))
    return story

def _section_ch2():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(KeepTogether([
        section_bar("Chapitre 2 — Au bloc opératoire"),
        Spacer(1, 1.5*mm),
        P("<b>Q5 — Prévention lors du choix du protocole d'anesthésie & traçabilité</b>", S_CELL_B),
        Spacer(1, 1.5*mm),
        reco_table([
            ("11", "Au vu de l'ensemble des risques évalués, proposer une stratégie de "
             "prise en charge anesthésique dans le dossier.", "Fort"),
            ("12", "Pour améliorer la qualité des soins et la gestion du risque, mettre "
             "en place une stratégie d'équipe pour diminuer l'incidence des bris "
             "dentaires.", "Fort"),
            ("13", "En cas de risque de bris dentaire identifié, favoriser la pratique de "
             "l'anesthésie locorégionale dans le cadre de l'analyse bénéfice/risque.", "Fort"),
            ("14", "Obtenir un relâchement musculaire optimal pour faciliter les "
             "conditions d'intubation trachéale.", "Fort"),
        ], RCW),
        Spacer(1, 1.5*mm),
        child_panel("chez l'enfant entre 3 et 14 ans, rechercher avant l'induction de "
             "l'anesthésie une éventuelle dent temporaire devenue mobile depuis la "
             "consultation d'anesthésie, en vérifier l'état aux différents temps "
             "périopératoires (après l'intubation jusqu'à la sortie de la salle de soins "
             "postinterventionnels) et tracer l'information dans le dossier."),
    ]))
    story.append(Spacer(1, 2.5*mm))
    story.append(KeepTogether([
        P("<b>Q6 — Matériel de contrôle des voies aériennes supérieures</b>", S_CELL_B),
        Spacer(1, 1.5*mm),
        reco_table([
            ("15", "En cas d'intubation et/ou de ventilation au masque difficile prévue, "
             "tenir compte de l'état dentaire dans la stratégie de contrôle des voies "
             "aériennes supérieures.", "Fort"),
            ("16", "En cas de risque identifié de bris dentaire et en l'absence de "
             "difficulté de ventilation au masque, il ne faut probablement pas utiliser "
             "systématiquement une canule oropharyngée.", "Fort"),
            ("17", "Avoir probablement recours à des solutions alternatives à une canule "
             "oropharyngée pour la prévention de la morsure de la sonde (compresses "
             "roulées).", "Fort"),
            ("18", "En cas de risque identifié de bris dentaire, le contrôle des voies "
             "aériennes doit être assuré par un opérateur expérimenté.", "Fort"),
            ("19", "Si une anesthésie générale est décidée et que l'indication s'y prête, "
             "privilégier probablement le choix d'un dispositif supraglottique.", "Fort"),
            ("20", "Si une intubation de la trachée est indiquée, utiliser probablement "
             "une lame de laryngoscope type Macintosh métallique pour une intubation par "
             "laryngoscopie conventionnelle.", "Fort"),
            ("21", "Après discussion avec le patient et pour limiter le risque de bris "
             "dentaire, recommander probablement l'utilisation d'une protection dentaire "
             "(gouttière) — tenir compte, dans son choix, de l'épaisseur du dispositif qui "
             "peut rendre l'accès aux voies aériennes plus difficile.", "Fort"),
            ("22", "Si l'utilisation d'une gouttière est retenue, recommander probablement "
             "une gouttière sur mesure plutôt qu'une gouttière standard, et tracer "
             "l'information « incité à fournir un protège-dents sur mesure » dans le "
             "dossier (délai de réalisation et coût pour le patient, libre d'accepter ou "
             "de refuser).", "Fort"),
        ], RCW),
        Spacer(1, 1.5*mm),
        child_panel("chez l'enfant, utiliser une lame de laryngoscope dont la taille est "
             "la mieux adaptée à sa morphologie, notamment en présence de dents "
             "fragilisées (maladie carieuse précoce). En période néonatale, éviter "
             "d'exercer une pression avec la lame du laryngoscope au niveau de la gencive "
             "du maxillaire supérieur — risque d'altération/lésion des germes dentaires ou "
             "de déplacement de germes."),
    ]))
    story.append(Spacer(1, 2.5*mm))
    story.append(KeepTogether([
        P("<b>Q7 — Surveillance péri- et postopératoire de l'état dentaire</b>", S_CELL_B),
        Spacer(1, 1.5*mm),
        reco_table([
            ("23", "Pour les patients présentant un risque dentaire identifié, tracer "
             "probablement l'absence de dommage dentaire directement visible lié à "
             "l'anesthésie.", "Fort"),
            ("24", "En cas de risque de bris dentaire élevé, l'extubation trachéale doit "
             "probablement être réalisée par un opérateur expérimenté chez un patient "
             "complètement réveillé, sans curarisation résiduelle, et avec une ventilation "
             "spontanée efficace.", "Fort"),
        ], RCW),
    ]))
    return story

def _section_ch3():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(KeepTogether([
        section_bar("Chapitre 3 — Conduite à tenir devant un bris dentaire"),
        Spacer(1, 1.5*mm),
        P("<b>Q8 — Que faire en cas de bris dentaire ?</b>", S_CELL_B),
        Spacer(1, 1.5*mm),
        reco_table([
            ("25", "Si une luxation complète (dent totalement sortie de son alvéole) "
             "d'une dent définitive est constatée, la remettre probablement en place "
             "rapidement ou la conserver dans du sérum physiologique ou, si disponible, "
             "dans une Hank's Balanced Salt Solution (HBSS — conservation dans un milieu "
             "isotonique au desmodonte à température ambiante), et demander un avis "
             "spécialisé dans le plus bref délai.", "Fort"),
            ("26", "En cas de bris dentaire constaté : prendre en charge une éventuelle "
             "complication (inhalation ou ingestion, radiographie thoracique éventuelle) "
             "et la traiter ; conserver si possible la dent ou ce qu'il en reste dans du "
             "sérum physiologique ; conserver les prothèses descellées et les "
             "restaurations.", "Fort"),
        ], RCW),
        Spacer(1, 1.5*mm),
        child_panel("chez l'enfant, il ne faut pas réimplanter une dent temporaire en cas "
             "de luxation complète."),
    ]))
    story.append(Spacer(1, 2.5*mm))
    story.append(KeepTogether([
        reco_table([
            ("27", "Au décours d'un traumatisme dentaire : proposer un avis spécialisé "
             "avec panoramique dentaire ; établir un constat descriptif et factuel des "
             "lésions dans le dossier du patient (sans opinion ni jugement personnel) ; "
             "informer le patient rapidement, noter sa réaction et ses réponses ; garder "
             "pour soi-même un aide-mémoire détaillé et conserver les photocopies du "
             "dossier complet.", "Fort"),
            ("28", "Prendre probablement des photographies des lésions et les conserver.", "Fort"),
            ("29", "En cas de dommage constaté par le patient ultérieurement sans avoir "
             "été constaté en périopératoire : le patient doit être reçu par le "
             "professionnel ou un représentant de l'établissement de santé pour être "
             "informé sur les causes et circonstances du dommage, dans les 15 jours "
             "suivant la découverte du dommage ou la demande du patient ; récupérer un "
             "éventuel panoramique antérieur à l'acte anesthésique ; prévoir un avis "
             "spécialisé.", "Fort"),
        ], RCW),
    ]))
    story.append(Spacer(1, 2.5*mm))
    story.append(KeepTogether([
        P("<b>Q9 — Déclaration de bris dentaire</b>", S_CELL_B),
        Spacer(1, 1.5*mm),
        reco_table([
            ("30", "Le praticien doit effectuer, selon son mode d'activité, une "
             "déclaration de bris dentaire auprès de son assurance civile "
             "professionnelle, ou du service qualité / gestion des évènements "
             "indésirables (ou service de contentieux) de son établissement.", "Fort"),
        ], RCW),
    ]))
    story.append(Spacer(1, 2.5*mm))
    story.append(KeepTogether([
        P("<b>Q10 — Documents et information à remettre au patient</b>", S_CELL_B),
        Spacer(1, 1.5*mm),
        reco_table([
            ("31", "Apporter une information claire au patient, l'accompagner et lui "
             "fournir : les coordonnées du service qualité et relation avec les usagers "
             "de son établissement ; la radio panoramique effectuée en postopératoire ; "
             "les coordonnées du dentiste ou stomatologue ayant constaté l'incident.", "Fort"),
        ], RCW),
    ]))
    story.append(Spacer(1, 2.5*mm))
    story.append(P(
        "<i>Le groupe de travail suggère que les propositions 1, 2, 3, 6, 9, 11 et 23 "
        "puissent faire l'objet d'une évaluation des pratiques professionnelles (EPP).</i>",
        S_NOTE))
    story.append(Spacer(1, 4*mm))
    story.extend(_section_sources())
    return story

def _section_sources():
    story = []
    story.append(section_bar("Sources et traçabilité", color=GREY))
    story.append(Spacer(1, 2*mm))
    story.append(P(
        "<b>Document source :</b> « Bris dentaires périanesthésiques : texte court » — "
        "RFE commune Société française d'anesthésie et de réanimation (SFAR), Association "
        "des anesthésistes réanimateurs pédiatriques d'expression française (Adarpef), "
        "Société française de stomatologie et chirurgie maxillo-faciale (SFSCMF). "
        "K. Nouette-Gaulain, F. Lenfant, D. Jacquet Francillon, A. Belbachir, et al. Ann "
        "Fr Anesth Reanim 2012;31:272-275, doi 10.1016/j.annfar.2012.01.003. Disponible "
        "sur Internet le 24 février 2012.", S_SOURCE))
    story.append(Spacer(1, 1.5*mm))
    story.append(P("<b>Méthodologie :</b> pas de système GRADE — propositions rédigées par "
                    "un groupe d'experts, validées par les comités des référentiels "
                    "cliniques et le CA de la SFAR ; « toutes les propositions ont reçu un "
                    "accord fort lors des votes par le groupe de travail » (mention "
                    "globale, non individuelle — voir disclosure méthodologique en page "
                    "1).", S_SOURCE))
    story.append(Spacer(1, 1.5*mm))
    story.append(P("<b>Couverture :</b> cette fiche reprend l'intégralité des 31 "
                    "propositions numérotées du texte court, réparties sur les 3 "
                    "chapitres / 10 questions (facteurs prédictifs, prévention au bloc "
                    "opératoire, conduite à tenir devant un bris dentaire constaté), ainsi "
                    "que les 5 encarts « Proposition enfant » pédiatriques. Comité "
                    "d'organisation, déclaration d'intérêts et formulaires "
                    "d'accompagnement (EPP, diaporama pédagogique, déclaration de bris "
                    "dentaire — disponibles sur cfar.org / sfar.org) ne sont pas "
                    "retranscrits (sans contenu clinique actionnable au-delà de ce que "
                    "la fiche cite déjà).", S_SOURCE))
    story.append(Spacer(1, 3*mm))
    story.append(info_panel(P(
        "<b>Avertissement — document de 2012 :</b> ce document est une fiche de synthèse "
        "indépendante, produite pour un usage d'aide-mémoire. Elle reprend l'intégralité "
        "des 31 propositions du texte source, mais ne remplace pas le texte intégral "
        "(argumentaire complet, principales références) et n'est ni éditée ni validée par "
        "la SFAR, l'Adarpef ou la SFSCMF. En cas de bris dentaire constaté, utiliser le "
        "formulaire de déclaration disponible sur sfar.org et l'joindre au dossier du "
        "malade ; en cas de doute, se référer au texte intégral et/ou à un avis "
        "spécialisé (odonto-stomatologiste, chirurgien maxillo-facial).",
        S_BODY_SM), bg=GREY_LIGHT, border=GREY))
    return story

SECTIONS = [
    ("Introduction, méthodologie & légende", _section_intro),
    ("Chapitre 1 — Facteurs prédictifs", _section_ch1),
    ("Chapitre 2 — Au bloc opératoire", _section_ch2),
    ("Chapitre 3 — Conduite à tenir & sources", _section_ch3),
]

def _make_doc(path=None):
    return SimpleDocTemplate(path or OUT, pagesize=A4,
                              leftMargin=MARGIN, rightMargin=MARGIN,
                              topMargin=32*mm, bottomMargin=16*mm,
                              title="Fiche SFAR/Adarpef/SFSCMF 2012 - Bris dentaires perianesthesiques",
                              author="Synthèse indépendante (source SFAR/Adarpef/SFSCMF)")

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
    import pypdf, tempfile
    tmp_path = tempfile.mktemp(suffix=".pdf")
    doc = _make_doc(tmp_path)
    doc.build(story_flowables, onFirstPage=_silent_page, onLaterPages=_silent_page)
    with open(tmp_path, "rb") as f:
        n = len(pypdf.PdfReader(f).pages)
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
