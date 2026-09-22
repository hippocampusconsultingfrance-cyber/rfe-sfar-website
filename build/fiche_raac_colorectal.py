# -*- coding: utf-8 -*-
"""
Fiche de synthese - Societe Francaise d'Anesthesie et de Reanimation (SFAR),
avec la Societe Francaise de Chirurgie Digestive (SFCD). "Rehabilitation
rapide apres une chirurgie colorectale programmee" - Recommandations
Formalisees d'Experts (RFE), Ann Fr Anesth Reanim 33 (2014) 370-384.
Auteurs : P. Alfonsi, K. Slim, M. Chauvin, P. Mariani, J.-L. Faucheron,
D. Fletcher. 15 pages (12 pages de contenu + 3 pages de bibliographie),
telecharge depuis sfar.org (wp-content/uploads/2015/10/2_AFAR_Rehabilitation-
rapide-apres-une-chirurgie-colorectale-programmee.pdf).

METHODOLOGIE : methode GRADE standard deja largement utilisee dans ce corpus
(qualite des preuves Haute/Moderee/Basse/Tres basse, force Forte GRADE 1+/1-
ou Faible GRADE 2+/2-, vote Delphi selon 4 facteurs). PARTICULARITE de cette
RFE : CHAQUE recommandation porte DEUX cotations independantes, imprimees
cote a cote dans le texte source - (1) le grade GRADE (1+/1-/2+/2-) quand la
methode a pu s'appliquer (30/35 recommandations : 22 fortes Grade 1, 8
faibles Grade 2), et (2) le resultat du vote Delphi du groupe de relecture,
"Accord Fort" ou "Accord Faible" (toujours present, sur les 35
recommandations : 28 Accord Fort, 7 Accord Faible) - deux axes distincts
(force de la preuve GRADE vs. force du consensus du groupe de relecture),
tous deux transcrits ici (chip GRADE + suffixe textuel "Accord Fort/Faible"),
jamais fusionnes en un seul chip. 5 recommandations n'ont PAS de grade GRADE
du tout (la methode ne pouvait pas s'appliquer, faute de preuves suffisantes)
- chip "AP" (pas de grade, position du groupe d'experts uniquement) pour ces
5, distinct des chips GRADE numeriques. Decompte verifie par transcription
integrale des 35 recommandations et confirme exactement contre les totaux
annonces par le texte source lui-meme (22+8+5=35 ; 28+7=35).

DISCLOSURE - artefact d'extraction de police : le signe moins des grades
negatifs ("GRADE 1-", "GRADE 2-") est imprime dans le PDF source avec un
caractere qui se convertit en caractere de controle illisible (\\x03) lors de
l'extraction PyMuPDF (meme categorie de bug que le "-"->"S" deja documente
dans fiche_sujet_age_esf.py) - le signe negatif est donc restitue ici a
partir de la formulation explicite de chaque recommandation ("n'est pas
recommande(e)" = negatif), jamais devine sans verification : chacune des 9
recommandations concernees a ete verifiee individuellement contre la
formulation de son enonce avant d'assigner le signe negatif.

PERIMETRE : integral sur les 35 recommandations (3 periodes : pre-, per- et
postoperatoire) et l'annexe de synthese (tableau recapitulatif par
parametre). Le preambule methodologique et les 3 pages de bibliographie
finale sont condenses conformement a la regle de projet 2026-09-14
(argumentaire minimal) - l'information clinique actionnable est integralement
dans les recommandations elles-memes.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from style import *
GRADE_COLORS["AP"] = (GREY, WHITE)
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.units import mm

OUT = "/home/user/rfe-sfar-website/output/Fiche_SFAR_SFCD_RAAC_Colorectale_2014.pdf"

SOURCE_TXT = ("Source : SFAR/SFCD, « Réhabilitation rapide après une chirurgie colorectale "
              "programmée », RFE, Ann Fr Anesth Réanim 33 (2014) 370-384. Fiche de synthèse "
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

TCW = [40 * mm, CW_FULL - 40 * mm]

def reco_table(rows, col_widths):
    """rows: (ref, text, grade_label)."""
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

RCW = [14 * mm, CW_FULL - 14 * mm - 18 * mm, 18 * mm]

def bullets(items, style=S_BODY_SM):
    html = "&bull; " + "<br/>&bull; ".join(items)
    return P(html, style)

def legend_flowable():
    chip_w = 14 * mm
    content_w = CW_FULL
    row = Table([[chip("1+", width=chip_w - 2 * mm), chip("1-", width=chip_w - 2 * mm),
                  chip("2+", width=chip_w - 2 * mm), chip("2-", width=chip_w - 2 * mm),
                  chip("AP", width=chip_w - 2 * mm),
                  P("<b>GRADE</b> — 1+/1- : recommandation <b>forte</b> (« il faut faire / "
                    "ne pas faire ») ; 2+/2- : recommandation <b>faible</b> (« il est possible "
                    "de faire / ne pas faire ») ; <b>AP</b> : méthode GRADE non applicable "
                    "(absence de preuves suffisantes). Chaque recommandation porte en outre un "
                    "résultat de vote Delphi indépendant, <b>Accord Fort</b> ou <b>Accord "
                    "Faible</b>, indiqué dans le texte de chaque ligne.", S_BADGE_HEAD)]],
                colWidths=[chip_w] * 5 + [content_w - 5 * chip_w])
    row.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                              ("LEFTPADDING", (0, 0), (-1, -1), 1),
                              ("RIGHTPADDING", (0, 0), (-1, -1), 1),
                              ("TOPPADDING", (0, 0), (-1, -1), 0),
                              ("BOTTOMPADDING", (0, 0), (-1, -1), 0)]))
    return row

TOTAL_PAGES = {"n": 6}

def on_page(canvas, doc, page_title):
    header_band(canvas, doc, "SFAR / SFCD — RFE, 2014",
                "Réhabilitation rapide après chirurgie colorectale programmée",
                page_title, icon_fn=lambda c, x, y: icon_pill(c, x, y, 13 * mm), color=TEAL_DARK)
    footer_band(canvas, doc, SOURCE_TXT, f"Page {doc.page} / {TOTAL_PAGES['n']}")

# ---------------------------------------------------------------------------
def _section_intro():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Résumé :</b> 35 recommandations organisées en 3 périodes (pré-, per- et "
        "postopératoire) pour un programme de réhabilitation rapide après chirurgie "
        "colorectale programmée. Facteurs non suffisamment appliqués en pratique mais "
        "recommandés : apport de carbohydrates préopératoire, optimisation hémodynamique "
        "peropératoire, reprise de l'alimentation orale avant h24, mastication de "
        "gommes postopératoire, lever et marche avant h24. Pratiques confirmées inutiles : "
        "préparation colique mécanique (chirurgie colique), sonde nasogastrique "
        "systématique, drainage chirurgical systématique (chirurgie colique).",
        S_BODY), bg=BG_PANEL, border=TEAL))
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("Méthodologie — GRADE + vote Delphi (double cotation)"))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "Méthode GRADE : qualité des preuves en 4 catégories (Haute/Modérée/Basse/Très "
        "basse) ; force toujours binaire — <b>forte</b> (GRADE 1+/1-, « il faut faire / ne "
        "pas faire ») ou <b>faible</b> (GRADE 2+/2-, « il est possible de faire / ne pas "
        "faire »). <b>Particularité de cette RFE :</b> chaque recommandation porte en plus "
        "un résultat de <b>vote Delphi</b> indépendant du groupe de relecture (30 experts, "
        "3 tours) — <b>Accord Fort</b> ou <b>Accord Faible</b> — deux axes distincts (force "
        "de la preuve vs. force du consensus), transcrits séparément ici, jamais fusionnés. "
        "Sur 35 recommandations : 22 fortes (Grade 1), 8 faibles (Grade 2), 5 sans grade "
        "GRADE (preuves insuffisantes, chip AP) ; 28 Accord Fort, 7 Accord Faible.",
        S_BODY_SM))
    story.append(Spacer(1, 1.5 * mm))
    story.append(legend_flowable())
    return story

# ---------------------------------------------------------------------------
def _section_preop():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Période préopératoire (R1-10)"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("R1", "L'information et les conseils liés au programme de réhabilitation sont des "
         "obligations réglementaires (loi n°2009-879 du 21 juillet 2009). — Accord Fort",
         "AP"),
        ("R2", "Lors d'une chirurgie colique, une préparation colique n'est pas recommandée "
         "de manière systématique. — Accord Fort", "1-"),
        ("R3", "Pour une chirurgie rectale, les données ne permettent pas d'émettre de "
         "recommandation sur l'utilité de la préparation colique. — Accord Faible", "AP"),
        ("R4", "Les données ne permettent pas d'émettre de recommandation sur l'impact "
         "d'une prémédication anxiolytique. — Accord Fort", "AP"),
        ("R5", "Les recommandations des sociétés savantes sont valides : jeûne de 2 h pour "
         "les liquides clairs, 4 à 6 h pour les solides. — Accord Fort", "AP"),
        ("R6", "Il est recommandé de donner une solution isotonique riche en carbohydrates "
         "aux patients ASA 1 ou 2 en préopératoire. — Accord Fort", "1+"),
        ("R7", "Il n'est pas recommandé de donner cette solution aux patients diabétiques "
         "ou ayant des troubles de la vidange gastrique. — Accord Fort", "1-"),
        ("R8", "Il est probablement recommandé de prescrire une immunonutrition en "
         "préopératoire d'une chirurgie colorectale carcinologique. — Accord Fort", "2+"),
        ("R9", "Il n'est pas recommandé de poursuivre une immunonutrition en postopératoire "
         "d'une chirurgie carcinologique. — Accord Fort", "1-"),
        ("R10", "Il n'est pas recommandé de prescrire une immunonutrition préopératoire "
         "pour une chirurgie colorectale non carcinologique. — Accord Faible", "1-"),
    ], RCW))
    return story

def _section_peropw():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Période peropératoire (R11-18)"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("R11", "Un apport excessif de solutés n'est pas recommandé pendant le geste "
         "chirurgical. — Accord Fort", "1-"),
        ("R12", "L'optimisation des apports liquidiens peropératoires, basée sur la mesure "
         "d'un paramètre hémodynamique reflétant la volémie, est recommandée. — Accord "
         "Fort", "1+"),
        ("R13", "L'administration d'une dose unique de corticostéroïdes en préopératoire "
         "immédiat est probablement recommandée. — Accord Faible", "2+"),
        ("R14", "La prévention de l'hypothermie peropératoire est recommandée. — Accord "
         "Fort", "1+"),
        ("R15", "L'administration d'une antibioprophylaxie couvrant les germes aérobies et "
         "anaérobies est recommandée. — Accord Fort", "1+"),
        ("R16", "La prévention des nausées et vomissements postopératoires est recommandée "
         "(stratégie basée sur le score d'Apfel). — Accord Fort", "1+"),
        ("R17", "La chirurgie par laparoscopie est recommandée. — Accord Fort", "1+"),
        ("R18", "En cas de laparotomie, aucune recommandation ne peut être faite sur le "
         "type d'incision (transversale ou verticale). — Accord Fort", "AP"),
    ], RCW))
    return story

def _section_preop_perop():
    story = _section_preop()
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_peropw())
    return story

# ---------------------------------------------------------------------------
def _section_postop_analgesie():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Période postopératoire — analgésie (R19-26)"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("R19", "Il n'est pas recommandé de laisser une sonde nasogastrique après une "
         "chirurgie colorectale. — Accord Fort", "1-"),
        ("R20", "Il est recommandé de prescrire une analgésie multimodale privilégiant les "
         "antalgiques non morphiniques et/ou une technique d'ALR. — Accord Fort", "1+"),
        ("R21", "Les AINS sont probablement recommandés, mais un doute persiste sur le "
         "risque de fistule digestive. — Accord Faible", "2+"),
        ("R22", "Après chirurgie par laparoscopie, l'analgésie péridurale thoracique n'est "
         "probablement pas recommandée. — Accord Faible", "2-"),
        ("R23", "Après chirurgie colorectale par laparotomie, l'analgésie péridurale "
         "thoracique est une des techniques recommandées. — Accord Fort", "1+"),
        ("R24", "L'administration intraveineuse continue de lidocaïne est recommandée "
         "(alternative en cas de laparoscopie/contre-indication à la péridurale). — Accord "
         "Fort", "1+"),
        ("R25", "L'irrigation pariétale avec une perfusion d'anesthésique local est "
         "probablement recommandée. — Accord Faible", "2+"),
        ("R26", "Le bloc dans le plan du muscle transverse de l'abdomen (TAP block) est "
         "probablement recommandé, mais son bénéfice sur la réhabilitation reste à "
         "démontrer. — Accord Fort", "2+"),
    ], RCW))
    return story

def _section_postop_reste():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Période postopératoire — suite (R27-35)"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("R27", "L'administration d'une héparine de bas poids moléculaire à dose "
         "prophylactique élevée est recommandée. — Accord Fort", "1+"),
        ("R28", "Lors de la chirurgie colique, la mise en place d'un drainage n'est pas "
         "recommandée. — Accord Fort", "1-"),
        ("R29", "Lors d'une chirurgie avec anastomose sous-péritonéale, un drainage "
         "aspiratif est probablement recommandé. — Accord Fort", "2+"),
        ("R30", "Le lever précoce (avant h24) est recommandé. — Accord Fort", "1+"),
        ("R31", "Il est recommandé de débuter précocement (avant h24) une alimentation "
         "orale. — Accord Fort", "1+"),
        ("R32", "Après une chirurgie colique, la durée du sondage vésical ne doit pas "
         "excéder 24 heures. — Accord Fort", "1+"),
        ("R33", "Lors d'une chirurgie du bas rectum nécessitant un drainage vésical > 4 "
         "jours, un cathéter sus-pubien est recommandé chez l'homme. — Accord Fort", "1+"),
        ("R34", "L'administration de naloxone n'est pas recommandée. — Accord Faible", "1-"),
        ("R35", "La mastication de gommes (chewing-gum) est probablement recommandée. — "
         "Accord Fort", "2+"),
    ], RCW))
    return story

def _section_postop():
    story = _section_postop_analgesie()
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_postop_reste())
    return story

# ---------------------------------------------------------------------------
def _section_annexe():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Annexe — classement par période et impact (source, reproduit)"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(theme_table([
        ("Information et conseils au patient", "Oui (recommandation principale)."),
        ("Préparation colique", "Non si chirurgie colique. Absence de recommandation si "
         "chirurgie rectale."),
        ("Prémédication anxiolytique", "Absence de données."),
        ("Jeûne préopératoire", "Solides : 6 heures. Liquides clairs et/ou sucrés : "
         "2 heures."),
        ("Apport en carbohydrates (veille + matin)", "Oui si ASA 1 ou 2. Non si diabète ou "
         "troubles de la vidange gastrique."),
        ("Immunonutrition", "Oui en préopératoire de chirurgie carcinologique (recommandation "
         "principale). Non en préopératoire de chirurgie non carcinologique, non en "
         "postopératoire (recommandations secondaires)."),
        ("Apports liquidiens peropératoires", "Oui : optimisation de la volémie "
         "(principale). Non : apport excessif de solutés (secondaire)."),
        ("Prévention du stress opératoire", "Oui : dose unique de corticostéroïdes en "
         "préopératoire immédiat (secondaire)."),
        ("Prévention des infections du site opératoire", "Oui, par la prévention de "
         "l'hypothermie peropératoire (principale) et l'antibioprophylaxie (secondaire)."),
        ("Prévention des NVPO", "Oui, systématique (recommandation principale)."),
        ("Voie d'abord chirurgical", "Par laparoscopie (principale). Si laparotomie : "
         "aucune recommandation sur le type d'incision."),
        ("Sondes nasogastriques", "Non, à enlever systématiquement en fin d'intervention "
         "(recommandation principale)."),
        ("Analgésie postopératoire — principes généraux", "Analgésie multimodale "
         "privilégiant les antalgiques non morphiniques et/ou l'ALR (principale). "
         "Prescription d'AINS (secondaire)."),
        ("Analgésie postopératoire — laparotomie", "Oui : analgésie péridurale thoracique "
         "(principale). Secondaires : irrigation pariétale, ou lidocaïne IV, ou TAP block."),
        ("Analgésie postopératoire — laparoscopie", "Oui : lidocaïne IV continue "
         "(principale). Non : analgésie péridurale thoracique. Secondaires : irrigation "
         "pariétale, ou TAP block."),
        ("Thromboprophylaxie", "Oui, par une HBPM à dose prophylactique élevée "
         "(recommandation principale)."),
        ("Mise en place d'un drainage chirurgical", "Oui si anastomose sous-péritonéale "
         "(secondaire). Non si chirurgie colique (principale)."),
        ("Mobilisation précoce", "Oui, avant h24 (recommandation principale)."),
        ("Alimentation orale", "Oui, à débuter avant h24 (recommandation principale)."),
        ("Sondage vésical", "Oui, < 24 h après chirurgie colique (principale). Chirurgie du "
         "bas rectum : cathéter sus-pubien chez l'homme (secondaire)."),
        ("Prévention de l'iléus postopératoire", "Oui : mastication de gommes (secondaire). "
         "Non : administration de naloxone (secondaire)."),
    ], TCW, head=("Paramètre", "Recommandation(s)")))
    return story

# ---------------------------------------------------------------------------
def _section_sources():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("Sources et avertissement"))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "SFAR/SFCD, « Réhabilitation rapide après une chirurgie colorectale programmée », "
        "RFE, Ann Fr Anesth Réanim 33 (2014) 370-384. Population : chirurgie colorectale "
        "programmée (carcinologique ou non), patient autonome en préopératoire, sans "
        "critère d'âge. ~40 000 interventions/an en France (80 % programmées, 70 % "
        "carcinologiques) ; durée de séjour moyenne 18 jours, mortalité 3,4 %, "
        "complications 25-35 % — un référentiel de réhabilitation appliqué avec une bonne "
        "compliance réduit ces deux derniers indicateurs.", S_SOURCE))
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Avertissement — document de 2014 :</b> cette fiche est une synthèse "
        "indépendante, produite pour un usage d'aide-mémoire. Elle reprend l'intégralité "
        "des 35 recommandations et le tableau de synthèse en annexe, mais ne remplace pas "
        "le texte intégral et n'est ni éditée ni validée par la SFAR/SFCD. Les pratiques de "
        "réhabilitation rapide (notamment les techniques d'analgésie et les seuils "
        "d'apport liquidien) ayant pu évoluer depuis 2014, se référer à un avis spécialisé "
        "et aux recommandations actualisées avant toute décision thérapeutique.",
        S_BODY_SM), bg=GREY_LIGHT, border=GREY))
    return story

# ---------------------------------------------------------------------------
def _section_all():
    story = _section_intro()
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_preop_perop())
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_postop())
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_annexe())
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_sources())
    return story

SECTIONS = [
    ("Méthodologie, R1-35 (pré/per/postopératoire), annexe & sources", _section_all),
]

def _make_doc(path=None):
    return SimpleDocTemplate(path or OUT, pagesize=A4,
                              leftMargin=MARGIN, rightMargin=MARGIN,
                              topMargin=32 * mm, bottomMargin=16 * mm,
                              title="Fiche SFAR/SFCD 2014 - Rehabilitation rapide chirurgie colorectale",
                              author="Synthèse indépendante (source SFAR/SFCD)")

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
