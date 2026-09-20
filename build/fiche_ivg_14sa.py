# -*- coding: utf-8 -*-
"""
Fiche de synthese - ANAES (Agence Nationale d'Accreditation et d'Evaluation en
Sante, predecesseur de la HAS), en partenariat avec l'ANCIC, l'ANSFL, le CNGE,
le CNGOF, le planning familial, la Federation Francaise de Psychiatrie, la
SFAR, la SFMG et la SFTG. "Prise en charge de l'interruption volontaire de
grossesse jusqu'a 14 semaines" - Recommandations pour la pratique clinique,
mars 2001 (mises a jour partiellement en decembre 2010). 12 pages, telecharge
depuis sfar.org (wp-content/uploads/2015/10/2_ANAES_Prise-en-charge-de-l-
interruption-volontaire-de-grossesse-jusqu-a-14-semaines.pdf).

METHODOLOGIE : grille ANAES a 3 niveaux - grade A (preuve scientifique
etablie : essais randomises de forte puissance, meta-analyses, analyses de
decision bien menees), grade B (presomption scientifique : essais randomises
de faible puissance, etudes comparatives non randomisees bien menees, etudes
de cohortes), grade C (niveau de preuve moindre : etudes cas-temoins, series
de cas). Convention explicite du texte source : "en l'absence de precision,
les recommandations proposees correspondent a un accord professionnel" - la
tres large majorite des recommandations de ce document (organisation des
structures, accueil, consultations pre-IVG, choix de la technique par tranche
d'age gestationnel hors 3 items gradés, prevention infectieuse, prevention
Rhesus, suites, evaluation) sont donc chippees "AP" (accord professionnel),
et non "grade" au sens des etudes cliniques - seuls 8 enonces portent un
grade A/B/C explicite dans le texte source (compte verifie par grep
'(grade [ABC])' sur le texte extrait : 3x A, 3x B, 2x C - 2x grade A sur la
preparation cervicale medicamenteuse, 1x grade B sur le choix de la
technique 13-14 SA, 2x grade C + 2x grade B sur la douleur/analgesie, 1x
grade A sur l'ibuprofene - detail exact dans les tableaux ci-dessous).
AUDIT : une premiere version de ce script comptait par erreur "7 enonces"
(erreur de decompte manuel, corrigee par un recomptage programmatique avant
finalisation - cf. discipline etablie par l'incident nutrition_perioperatoire
de cette meme session : ne jamais se fier a une relecture visuelle seule
pour un decompte).

DISCLOSURE - double perimetre temporel (2001/2010), rule 5 du projet : la
page de garde du PDF source indique explicitement que les recommandations de
mars 2001 concernant l'IVG MEDICAMENTEUSE sont remplacees par les
recommandations HAS de decembre 2010 (non incluses dans ce document source,
et donc non reprises ici), et que "les parties des recommandations de mars
2001 modifiees suite aux recommandations de decembre 2010 apparaissent en
ROUGE dans ce document [source]". Cette information de couleur est perdue a
l'extraction texte (PyMuPDF ne recupere pas la mise en forme couleur) : il
est donc IMPOSSIBLE de distinguer, dans le texte recupere, quelles phrases
exactes du corps du texte ont ete amendees en 2010 par rapport a la version
originale de 2001. Cette fiche presente fidelement le texte du PDF source tel
que recupere (qui integre deja, sans marquage recuperable, les eventuelles
corrections de 2010), et le signale explicitement dans le panneau
methodologie plutot que de pretendre a une datation uniforme (ni "tout 2001"
ni "tout 2010") - conformement a la regle de non-resolution silencieuse des
incoherences de source. Consequence pratique pour le lecteur : POUR L'IVG PAR
METHODE MEDICAMENTEUSE SPECIFIQUEMENT, se referer imperativement aux
recommandations HAS de decembre 2010 (non couvertes par cette fiche) ; cette
fiche couvre la technique chirurgicale et l'ensemble des elements communs aux
deux methodes (organisation, consultations, douleur, prevention infectieuse,
prevention Rhesus, suivi) tels que formules dans le document source.

COUVERTURE : integrale sur les recommandations enonçables des sections I a
IX du texte source (structures, accueil/organisation, consultations pre-IVG,
techniques par tranche d'age gestationnel, douleur/analgesie-anesthesie,
prevention infectieuse, prevention Rhesus, suites immediates, evaluation),
plus la section X (axes de recherche futurs, presentee comme une liste, pas
des recommandations). Les pages de garde/avant-propos/listes nominatives des
groupes de travail et de lecture (pages 1-6 du PDF) sont hors perimetre
(information administrative, non clinique).

ARGUMENTAIRE : minimal, conformement a la regle de projet 2026-09-14 - le
texte source lui-meme est deja tres concis (recommandations directement
formulees, peu de prose de justification a compresser davantage).
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from style import *
GRADE_COLORS["A"] = (GREEN, WHITE)
GRADE_COLORS["B"] = (TEAL, WHITE)
GRADE_COLORS["C"] = (AMBER, WHITE)
GRADE_COLORS["AP"] = (GREY, WHITE)
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.units import mm

OUT = "/home/user/rfe-sfar-website/output/Fiche_ANAES_IVG_14SA_2001.pdf"

SOURCE_TXT = ("Source : ANAES, « Prise en charge de l'interruption volontaire de grossesse "
              "jusqu'à 14 semaines », mars 2001 (màj partielle déc. 2010). Fiche de synthèse "
              "non officielle : se référer au texte intégral.")

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

TCW = [46 * mm, CW_FULL - 46 * mm]

def reco_table(rows, col_widths):
    """rows: (text, grade_label)."""
    data = [[P("Recommandation", S_HEAD_W), P("Grade", S_HEAD_W_C)]]
    for txt, grade in rows:
        data.append([P(txt, S_CELL), chip(grade)])
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

RCW = [CW_FULL - 20 * mm, 20 * mm]

def bullets(items, style=S_BODY_SM):
    html = "&bull; " + "<br/>&bull; ".join(items)
    return P(html, style)

def legend_flowable():
    chip_w = 15 * mm
    content_w = CW_FULL
    row = Table([[chip("A", width=chip_w - 2 * mm), chip("B", width=chip_w - 2 * mm),
                  chip("C", width=chip_w - 2 * mm), chip("AP", width=chip_w - 2 * mm),
                  P("<b>Grille ANAES</b> — <b>A</b> : preuve scientifique établie (essais "
                    "randomisés de forte puissance, méta-analyses) ; <b>B</b> : présomption "
                    "scientifique (essais randomisés de faible puissance, cohortes) ; "
                    "<b>C</b> : niveau de preuve moindre (cas-témoins, séries de cas) ; "
                    "<b>AP</b> : accord professionnel (absence de précision de grade dans "
                    "le texte source).", S_BADGE_HEAD)]],
                colWidths=[chip_w, chip_w, chip_w, chip_w, content_w - 4 * chip_w])
    row.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                              ("LEFTPADDING", (0, 0), (-1, -1), 1),
                              ("RIGHTPADDING", (0, 0), (-1, -1), 1),
                              ("TOPPADDING", (0, 0), (-1, -1), 0),
                              ("BOTTOMPADDING", (0, 0), (-1, -1), 0)]))
    return row

TOTAL_PAGES = {"n": 4}

def on_page(canvas, doc, page_title):
    header_band(canvas, doc, "ANAES — RECOMMANDATIONS, MARS 2001 (MÀJ PARTIELLE DÉC. 2010)",
                "Prise en charge de l'IVG jusqu'à 14 semaines",
                page_title, icon_fn=lambda c, x, y: icon_shield(c, x, y, 13 * mm), color=TEAL_DARK)
    footer_band(canvas, doc, SOURCE_TXT, f"Page {doc.page} / {TOTAL_PAGES['n']}")

# ---------------------------------------------------------------------------
def _section_intro():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Résumé :</b> recommandations ANAES (mars 2001) pour la prise en charge de "
        "l'IVG jusqu'à 14 semaines d'aménorrhée (SA), dans le cadre légal. Organisation "
        "des structures et de l'accueil, information et consultations pré-IVG, choix de "
        "la technique (chirurgicale ou médicamenteuse) et du mode d'anesthésie selon "
        "l'âge gestationnel, prise en charge de la douleur, prévention des complications "
        "infectieuses et de l'incompatibilité Rhésus, suites et suivi post-IVG.",
        S_BODY), bg=BG_PANEL, border=TEAL))
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>⚠ Périmètre — IVG médicamenteuse exclue de cette fiche :</b> le document "
        "source lui-même indique que ses recommandations sur l'IVG par <b>méthode "
        "médicamenteuse</b> sont remplacées par les recommandations HAS de "
        "<b>décembre 2010</b> (non incluses dans le PDF source, donc non reprises ici). "
        "Le PDF signale aussi que les passages de mars 2001 modifiés en 2010 apparaissent "
        "« en rouge » dans le document original — une information de couleur qui n'est "
        "<b>pas récupérable</b> lors de l'extraction du texte (limite technique, disclosed "
        "et non résolue silencieusement, cf. règle 5 du projet). Cette fiche reproduit "
        "fidèlement le texte tel qu'il apparaît dans le PDF source (donc déjà partiellement "
        "amendé, sans qu'on puisse distinguer 2001 de 2010) et porte principalement sur la "
        "<b>technique chirurgicale</b> et les éléments communs aux deux méthodes. Pour "
        "l'IVG médicamenteuse, se référer impérativement aux recommandations HAS 2010.",
        S_BODY_SM), bg=AMBER_LIGHT, border=AMBER))
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("Méthodologie — grille ANAES"))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "Grille à 3 niveaux : <b>grade A</b> (essais comparatifs randomisés de forte "
        "puissance, méta-analyses, analyses de décision bien menées) ; <b>grade B</b> "
        "(essais randomisés de faible puissance, études comparatives non randomisées "
        "bien menées, études de cohortes) ; <b>grade C</b> (études cas-témoins, séries "
        "de cas). « En l'absence de précision, les recommandations proposées "
        "correspondent à un <b>accord professionnel</b> » (citation littérale du texte "
        "source) — chip <b>AP</b> dans cette fiche. La grande majorité des "
        "recommandations de ce document sont non graduées (AP) ; seuls 8 énoncés "
        "portent un grade A/B/C explicite (détaillés ci-après).", S_BODY_SM))
    story.append(Spacer(1, 1.5 * mm))
    story.append(legend_flowable())
    return story

# ---------------------------------------------------------------------------
def _section_organisation():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("I-II. Structures de prise en charge, accueil et organisation"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(theme_table([
        ("Nombre de structures",
         "En nombre suffisant par département pour un accueil correct et rapide de "
         "toutes les demandes ; fonctionnement chaque semaine, sans interruption, toute "
         "l'année. <i>(AP)</i>"),
        ("Jusqu'à 12 SA (84 j)",
         "Structure intégrée à un établissement avec service de gynécologie-obstétrique, "
         "ou en convention avec un plateau technique permettant de prendre en charge "
         "l'ensemble des complications de l'IVG. <i>(AP)</i>"),
        ("Au-delà de 12 SA",
         "Prise en charge dans une structure disposant d'un plateau technique "
         "chirurgical, désignée et connue de tous les centres d'accueil du département. "
         "<i>(AP)</i>"),
        ("Équipement",
         "Chaque centre d'accueil doit disposer d'au moins un échographe avec sonde "
         "vaginale. Projet de service partagé par tout le personnel impliqué, avec "
         "formation spécifique à cette activité. <i>(AP)</i>"),
        ("Délai de rendez-vous",
         "Consultation obtenue dans les 5 jours suivant l'appel — l'IVG précoce réduit "
         "le risque de complications et élargit le choix des techniques. <i>(AP)</i>"),
        ("Accueil téléphonique",
         "Ligne téléphonique dédiée, connue et diffusée ; message clair et précis hors "
         "présence du personnel. <i>(AP)</i>"),
        ("Accueil/secrétariat",
         "Opérationnels pour répondre aux demandes, orienter vers les consultations "
         "préalables et informer sur les modalités de l'IVG ; signalés avec précision "
         "à l'entrée et dans l'établissement. <i>(AP)</i>"),
        ("Mode de prise en charge",
         "Sauf cas exceptionnel, IVG réalisées en ambulatoire ou en hôpital de jour "
         "(séjour < 12 heures). <i>(AP)</i>"),
    ], TCW, head=("Thème", "Recommandation")))
    return story

def _section_preivg():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("III. Consultations pré-IVG"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(theme_table([
        ("Information",
         "Informations claires et précises sur la procédure (méthode médicamenteuse ou "
         "chirurgicale), les choix d'anesthésie (locale/générale) et le temps de "
         "réflexion, à l'oral et par documents écrits. <i>(AP)</i>"),
        ("Entretien psychosocial",
         "Un entretien d'information, de soutien et d'écoute doit pouvoir être proposé "
         "systématiquement, confié à des professionnels qualifiés pour cet "
         "accompagnement. <i>(AP)</i>"),
        ("Âge gestationnel",
         "Précisé par l'interrogatoire et l'examen clinique ; recours à une échographie "
         "possible sur place lors de la consultation. <i>(AP)</i>"),
        ("Dépistage",
         "Dépistage des IST (dont VIH) et frottis cervico-vaginaux proposés selon le "
         "contexte clinique. <i>(AP)</i>"),
        ("Contraception ultérieure",
         "Abordée et éventuellement prescrite dès la consultation précédant l'IVG ; "
         "recherche des raisons de l'échec ou de l'absence de contraception. <i>(AP)</i>"),
        ("Procédure d'urgence",
         "Permet de raccourcir le délai de réflexion pour les femmes dont l'âge "
         "gestationnel est situé entre 12 et 14 SA. <i>(AP)</i>"),
        ("Bilan biologique",
         "Groupe sanguin Rhésus avec recherche d'agglutinines irrégulières (RAI) "
         "systématique pour toutes les patientes ; autres examens si besoin lors d'une "
         "éventuelle consultation préanesthésique. <i>(AP)</i>"),
    ], TCW, head=("Thème", "Recommandation")))
    return story

def _section_organisation_preivg():
    story = _section_organisation()
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_preivg())
    return story

# ---------------------------------------------------------------------------
def _section_technique_generale():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("IV. Techniques d'IVG — principes généraux"),
        Spacer(1, 1.5 * mm),
        P("Dans tous les cas possibles, la femme choisit la technique (médicale ou "
          "chirurgicale) et le mode d'anesthésie (locale ou générale). <i>(AP)</i> La "
          "technique chirurgicale repose sur la dilatation du col et l'évacuation du "
          "contenu utérin par aspiration, en conditions strictes d'asepsie, "
          "éventuellement précédée d'une préparation cervicale médicamenteuse. La "
          "technique médicamenteuse associe mifépristone et prostaglandines — "
          "<b>se référer aux recommandations HAS de décembre 2010</b> pour cette "
          "méthode (hors périmètre de cette fiche, voir avertissement en page 1).",
          S_BODY_SM),
    ]))
    story.append(Spacer(1, 1.8 * mm))
    story.append(reco_table([
        ("<b>Préparation cervicale</b> (lorsqu'elle est recommandée) — mifépristone "
         "200 mg per os 36 à 48 heures avant aspiration.", "A"),
        ("<b>Préparation cervicale</b> (alternative) — misoprostol 400 µg par voie "
         "orale ou vaginale 3 à 4 heures avant aspiration.", "A"),
    ], RCW))
    story.append(Spacer(1, 1.8 * mm))
    story.append(P(
        "La préparation cervicale, quel que soit le produit utilisé, ne nécessite pas "
        "d'hospitalisation. Le contrôle visuel du produit d'aspiration est indispensable. "
        "<i>(AP)</i> En postopératoire, toute patiente ayant bénéficié d'une sédation "
        "intraveineuse, d'une anesthésie générale ou périmédullaire doit séjourner en "
        "salle de surveillance post-interventionnelle (SSPI). <i>(AP)</i>", S_BODY_SM))
    return story

def _section_technique_age():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("IV (suite). Technique selon l'âge gestationnel"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(theme_table([
        ("Jusqu'à 7 SA révolues (49 j)",
         "Techniques chirurgicale et médicale utilisables selon disponibilités et choix "
         "de la patiente. Risque d'échec de la technique chirurgicale inférieur à la "
         "technique médicale, mais plus élevé à cet âge gestationnel que plus "
         "tardivement. <i>(AP)</i>"),
        ("8e-9e SA (50 à 63 j)",
         "Deux techniques utilisables. Pour la technique chirurgicale, préparation "
         "cervicale médicamenteuse recommandée chez la nullipare (mifépristone 200 mg "
         "36-48 h avant, ou misoprostol 400 µg 3-4 h avant). <i>(AP)</i>"),
        ("10e-12e SA (64 à 84 j)",
         "Technique chirurgicale = technique de choix. Préparation cervicale "
         "médicamenteuse recommandée (mêmes 2 options). <i>(AP)</i>"),
        ("13e-14e SA (85 à 98 j)",
         "Technique chirurgicale = technique de choix — évacuation par aspiration ± "
         "pinces spécifiques, nécessitant une formation spécifique. Préparation "
         "cervicale médicamenteuse recommandée. L'anesthésie locale éventuelle demande "
         "une très bonne maîtrise de la technique de dilatation-évacuation."),
    ], TCW, head=("Âge gestationnel", "Conduite recommandée")))
    story.append(Spacer(1, 1.5 * mm))
    story.append(reco_table([
        ("<b>13e-14e SA</b> — la technique chirurgicale est la technique de choix.", "B"),
    ], RCW))
    return story

def _section_technique_all():
    story = _section_technique_generale()
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_technique_age())
    return story

# ---------------------------------------------------------------------------
def _section_douleur():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("V. Prise en charge de la douleur — analgésie et anesthésie"),
        Spacer(1, 1.5 * mm),
        P("L'IVG médicamenteuse est responsable de douleurs modérées à sévères pour "
          "plus de 50 % des femmes, liées principalement aux prostaglandines ; "
          "l'efficacité des traitements antalgiques proposés a été peu évaluée. "
          "<i>(AP)</i>", S_BODY_SM),
    ]))
    story.append(Spacer(1, 1.8 * mm))
    story.append(reco_table([
        ("Lors des avortements par aspiration, l'anesthésie locale par bloc "
         "paracervical ne prévient pas la survenue de douleurs sévères pour environ le "
         "tiers des patientes.", "C"),
        ("L'injection de lidocaïne intracervicale (région isthmique, orifice interne du "
         "col) diminue significativement le score de douleur par comparaison à la "
         "technique de bloc paracervical précédente.", "B"),
        ("Facteurs de risque de douleur intense : jeune âge, peur de l'acte, utérus "
         "rétroversé, antécédents de dysménorrhée, grossesses les plus précoces et les "
         "plus avancées — justifient des antalgiques efficaces en préopératoire (AL) ou "
         "la proposition d'une anesthésie générale.", "C"),
        ("L'administration d'ibuprofène (AINS) diminue les scores de douleur per- et "
         "postopératoire (seul l'AINS étudié).", "A"),
        ("Les benzodiazépines sont inefficaces sur la douleur de l'IVG par aspiration ; "
         "l'efficacité du paracétamol n'est pas prouvée.", "AP"),
        ("Pour l'anesthésie générale : les halogénés à forte concentration augmentent le "
         "volume des pertes sanguines ; l'utilisation d'ocytocine le diminue.", "B"),
    ], RCW))
    story.append(Spacer(1, 1.8 * mm))
    story.append(P(
        "La patiente doit être informée des différentes modalités d'anesthésie "
        "possibles (générale ou locale) ; le choix du type d'anesthésie lui revient. "
        "Le recours à l'anesthésie générale doit être possible ; si retenue, elle "
        "répond aux exigences du décret n° 94-1050 du 5 décembre 1994. Les données "
        "anciennes sur l'augmentation des complications liées à l'AG (perforations, "
        "hémorragies, mortalité) précèdent l'utilisation du misoprostol et les mesures "
        "de surveillance actuelles. <i>(AP)</i>", S_BODY_SM))
    return story

# ---------------------------------------------------------------------------
def _section_prevention():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("VI-VII. Prévention infectieuse et prévention Rhésus"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(theme_table([
        ("Prévention infectieuse (VI)",
         "Bien qu'il n'existe pas de démonstration d'un bénéfice à long terme, il est "
         "recommandé, en cas d'IVG chirurgicale, d'adopter une stratégie pouvant "
         "associer : antibiothérapie en cas d'antécédent connu d'infection génitale "
         "haute ; pour toute autre situation à risque d'IST, prélèvement vaginal et/ou "
         "recherche de Chlamydiae trachomatis par PCR urinaire, avec traitement de la "
         "patiente et du(des) partenaire(s) en cas de positivité ; en l'absence de "
         "facteur de risque, les antibiotiques réduisent la fièvre post-IVG mais sans "
         "données sur un bénéfice à long terme (incohérence source disclosed : bénéfice "
         "à court terme démontré, bénéfice à long terme non démontré). <i>(AP)</i>"),
        ("Prévention Rhésus (VII)",
         "Systématique chez toute femme Rhésus négatif, par injection intraveineuse "
         "d'une dose standard de gamma-globulines anti-D. En cas d'IVG médicamenteuse à "
         "domicile, la prévention est faite lors de la prise de mifépristone. <i>(AP)</i>"),
    ], TCW, head=("Volet", "Recommandation")))
    return story

def _section_suites():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("VIII-IX. Suites immédiates, visite de contrôle et évaluation"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(theme_table([
        ("Avant la visite de contrôle",
         "Contraception œstroprogestative possible dès le lendemain de l'IVG (méthode "
         "médicamenteuse ou chirurgicale). Pose d'un dispositif intra-utérin (DIU) "
         "possible lors de l'examen de surveillance, ou en fin d'aspiration en cas "
         "d'IVG chirurgicale. Fiche de conseils sur les suites normales + numéro "
         "d'urgence remis à la patiente. <i>(AP)</i>"),
        ("Visite de contrôle",
         "Prévue entre le 14e et le 21e jour post-IVG. Contrôle de la vacuité utérine "
         "par examen clinique, complété par échographie selon les données de l'examen. "
         "Vérification de la compréhension et de la bonne utilisation de la "
         "contraception prescrite, et de la position d'un éventuel DIU (pose possible "
         "si non fait). Accompagnement psychologique spécifique proposé et disponible "
         "(peu de données sur le retentissement psychologique de l'IVG). <i>(AP)</i>"),
        ("Évaluation (IX)",
         "Les IVG doivent être déclarées. Un recueil national des données est "
         "nécessaire pour la surveillance épidémiologique et l'évaluation des "
         "pratiques ; ces données doivent être rapidement accessibles aux "
         "professionnels. <i>(AP)</i>"),
    ], TCW, head=("Volet", "Recommandation")))
    story.append(Spacer(1, 2.5 * mm))
    story.append(section_bar("X. Axes de recherche future proposés (liste, non gradés)"))
    story.append(Spacer(1, 1.5 * mm))
    story.append(bullets([
        "Comparer les techniques médicale et chirurgicale",
        "Améliorer la prise en charge de la douleur liée à l'IVG",
        "Déterminer l'utilité à long terme d'une antibioprophylaxie ou d'une "
        "antibiothérapie au cours de l'IVG",
        "Préciser le retentissement psychologique de l'IVG",
    ]))
    return story

def _section_prevention_suites():
    story = _section_prevention()
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_suites())
    return story

# ---------------------------------------------------------------------------
def _section_sources():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(section_bar("Sources et avertissement"))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "ANAES, « Prise en charge de l'interruption volontaire de grossesse jusqu'à 14 "
        "semaines », Recommandations pour la pratique clinique, mars 2001. Élaboré en "
        "partenariat avec l'ANCIC, l'ANSFL, le CNGE, le CNGOF, la Confédération "
        "nationale du mouvement pour le planning familial, la Fédération Française de "
        "Psychiatrie, la SFAR, la SFMG et la SFTG. Mise à jour partielle en décembre "
        "2010 (HAS) pour l'IVG médicamenteuse uniquement.", S_SOURCE))
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Avertissement — document de 2001, partiellement actualisé en 2010 :</b> "
        "cette fiche est une synthèse indépendante, produite pour un usage "
        "d'aide-mémoire. Elle reprend l'intégralité des recommandations énonçables du "
        "texte source pour la partie chirurgicale et les éléments communs aux deux "
        "méthodes d'IVG, mais ne remplace pas le texte intégral et n'est ni éditée ni "
        "validée par l'ANAES/HAS/SFAR. <b>Pour l'IVG médicamenteuse, se référer "
        "impérativement aux recommandations HAS de décembre 2010</b> (non incluses "
        "dans le PDF source de cette fiche). Le cadre légal, les techniques et les "
        "pratiques d'organisation des soins ayant pu évoluer depuis 2001/2010, se "
        "référer à un avis spécialisé et aux recommandations actualisées avant toute "
        "décision.", S_BODY_SM), bg=GREY_LIGHT, border=GREY))
    return story

# ---------------------------------------------------------------------------
def _section_all():
    story = _section_intro()
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_organisation_preivg())
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_technique_all())
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_douleur())
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_prevention_suites())
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_sources())
    return story

SECTIONS = [
    ("Méthodologie, organisation, consultations, techniques, douleur, prévention, "
     "suites & sources",
     _section_all),
]

def _make_doc(path=None):
    return SimpleDocTemplate(path or OUT, pagesize=A4,
                              leftMargin=MARGIN, rightMargin=MARGIN,
                              topMargin=32 * mm, bottomMargin=16 * mm,
                              title="Fiche ANAES 2001/2010 - IVG jusqu'a 14 semaines",
                              author="Synthèse indépendante (source ANAES/HAS)")

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
