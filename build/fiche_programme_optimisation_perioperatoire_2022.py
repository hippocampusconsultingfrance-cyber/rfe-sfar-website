# -*- coding: utf-8 -*-
"""
Fiche de synthese - "Programme d'optimisation perioperatoire du patient
adulte" - Recommandations Formalisees d'Experts (RFE), SFAR, texte valide
par le Comite des Referentiels Cliniques le 13/06/2022 et le Conseil
d'Administration le 29/06/2022. 61 pages, telecharge depuis sfar.org
(wpdmdl=37889).

METHODOLOGIE : methode GRADE standard de ce corpus (1+/1-/2+/2-, avis
d'experts si preuve tres faible/litterature quasi inexistante), vote
GRADE grid (>= 50% d'opinion convergente pour valider, < 20% d'opinion
contraire, >= 70% convergents pour une recommandation FORTE). Regle de
scope explicite du texte source : une mesure devait etre valable dans AU
MOINS 3 domaines chirurgicaux distincts pour faire l'objet d'une
recommandation dans ce "socle commun" - complementaire, non redondant,
des 4 RFE de RAAC specifiques a une chirurgie deja git-trackees dans ce
corpus (raac_lobectomie_pulmonaire_2019, raac_cardiaque_2021,
raac_orthopedique_2019, raac_colorectal).

DECOMPTE VERIFIE EXACT (cas "propre" de ce corpus, comme
raac_cardiaque_2021) : la synthese du texte source annonce 30
recommandations (16 GRADE1+ + 3 GRADE1- + 10 GRADE2+ + 0 GRADE2- + 1 avis
d'experts = 30) et 2 questions sans reponse. Un decompte direct,
item par item (chaque marqueur "Rx.y[.z] -" apparie individuellement a
son tag de grade suivant), retrouve EXACTEMENT les memes 5 sous-totaux
(16/3/10/0/1 = 30) et les memes 2 "ABSENCE DE RECOMMANDATION" imprimees
dans le texte (place de la medecine de ville en champ 1 ; moniteurs
d'analgesie en champ 3, sous-question de R3.9 sur le monitorage de la
profondeur d'anesthesie). Aucune divergence, contrairement aux fiches
optimisation_hemodynamique_adulte_2024 (fiche 129, ecart sur le TOTAL) et
resection_hepatique_2025 (fiche 130, ecart sur un SOUS-total GRADE2) -
document de reference "propre" pour un futur schema de migration.

PERIMETRE : integral sur les 4 champs (generalites, mesures
preoperatoires, peroperatoires, postoperatoires), les 30 recommandations
numerotees et les 2 absences de recommandation. L'Annexe 1 du source
(2 forest-plots meta-analytiques TIVA vs inhalation, support statistique
de R3.1) et le "schema recapitulant les grandes etapes du programme"
mentionne dans la synthese (non retrouve comme figure numerotee separee
dans le texte extrait, probablement une image de couverture) ne sont pas
retranscrits : purement evidentiaires/illustratifs, sans information
clinique supplementaire par rapport au texte des recommandations
elles-memes. Argumentaire minimal (regle de projet 2026-09-14) : chaque
recommandation est deja un enonce actionnable complet ; les paragraphes
"Argumentaire" (tres longs, citations d'etudes) ne sont pas transcrits.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from style import *
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.units import mm

OUT = "/home/user/rfe-sfar-website/output/Fiche_SFAR_Programme_Optimisation_Perioperatoire_2022.pdf"

SOURCE_TXT = ("Source : SFAR, « Programme d'optimisation périopératoire du patient adulte », "
              "RFE, 2022. Fiche de synthèse non officielle : se référer au texte intégral.")

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

RCW = [15 * mm, CW_FULL - 15 * mm - 15 * mm, 15 * mm]

def absence_note(question_txt):
    return info_panel(P(
        f"<b>Absence de recommandation</b> (données insuffisantes) : {question_txt}",
        S_BODY_SM), bg=GREY_LIGHT, border=GREY)

def legend_flowable():
    chip_w = 15 * mm
    content_w = CW_FULL
    row = Table([[chip("1+", width=chip_w - 2 * mm), chip("1-", width=chip_w - 2 * mm),
                  chip("2+", width=chip_w - 2 * mm), chip("2-", width=chip_w - 2 * mm),
                  chip("AE", width=chip_w - 2 * mm),
                  P("<b>GRADE</b> — 1+/1- : recommandation <b>forte</b> (« il faut faire "
                    "/ ne pas faire »,  ≥ 70 % d'opinion convergente) ; 2+/2- : "
                    "recommandation <b>faible</b> (« il est probablement recommandé de "
                    "faire / ne pas faire », preuve modérée/faible) ; <b>AE</b> : avis "
                    "d'experts (preuve très faible ou littérature quasi inexistante). "
                    "Règle de scope : une mesure devait être valable dans au moins 3 "
                    "domaines chirurgicaux pour faire l'objet d'une recommandation ici.",
                    S_BADGE_HEAD)]],
                colWidths=[chip_w] * 5 + [content_w - 5 * chip_w])
    row.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                              ("LEFTPADDING", (0, 0), (-1, -1), 1),
                              ("RIGHTPADDING", (0, 0), (-1, -1), 1),
                              ("TOPPADDING", (0, 0), (-1, -1), 0),
                              ("BOTTOMPADDING", (0, 0), (-1, -1), 0)]))
    return row

TOTAL_PAGES = {"n": 6}

def on_page(canvas, doc, page_title):
    header_band(canvas, doc, "SFAR — RECOMMANDATIONS FORMALISÉES D'EXPERTS, 2022",
                "Programme d'optimisation périopératoire du patient adulte",
                page_title, icon_fn=lambda c, x, y: icon_shield(c, x, y, 13 * mm), color=TEAL_DARK)
    footer_band(canvas, doc, SOURCE_TXT, f"Page {doc.page} / {TOTAL_PAGES['n']}")

# ---------------------------------------------------------------------------
def _section_intro_champ1():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Résumé :</b> socle commun de recommandations applicables quelle que soit la "
        "chirurgie (à la différence des RFE de réhabilitation améliorée déjà git-trackées "
        "dans ce corpus, spécifiques à une chirurgie) — une mesure devait être valable "
        "dans au moins 3 domaines chirurgicaux distincts pour être retenue ici. 30 "
        "recommandations (accord fort, décompte source vérifié exact) et 2 absences de "
        "recommandation, sur 4 champs : généralités, mesures préopératoires, "
        "peropératoires, postopératoires.", S_BODY), bg=BG_PANEL, border=TEAL_DARK))
    story.append(Spacer(1, 2.5 * mm))
    story.append(legend_flowable())
    story.append(Spacer(1, 3 * mm))
    story.append(KeepTogether([
        section_bar("Champ 1 — Généralités sur le programme d'optimisation périopératoire"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("R1.1", "Mettre en place et appliquer un programme d'optimisation "
         "périopératoire, pour réduire la durée de séjour et l'incidence des "
         "complications postopératoires.", "1+"),
    ], RCW))
    story.append(Spacer(1, 2 * mm))
    story.append(absence_note(
        "place de la médecine de ville dans les périodes pré- et postopératoire d'un "
        "programme d'optimisation périopératoire."))
    story.append(Spacer(1, 2 * mm))
    story.append(reco_table([
        ("R1.2", "Les experts suggèrent que l'implémentation et le suivi des programmes "
         "d'optimisation périopératoire soient effectués par une équipe "
         "pluriprofessionnelle, avec du temps dédié pour la coordination du parcours "
         "patient.", "AE"),
        ("R1.3", "Inclure tous les patients dans un programme d'optimisation "
         "périopératoire, notamment les patients âgés, fragiles ou comorbides, chez qui "
         "ce type de prise en charge diminue aussi le taux de complications "
         "postopératoires et la durée de séjour.", "1+"),
    ], RCW))
    return story

# ---------------------------------------------------------------------------
def _section_champ2():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Champ 2 — Mesures préopératoires"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("R2.1", "Mettre en œuvre un programme de préhabilitation avant chirurgie, pour "
         "réduire la morbidité et la durée de séjour postopératoire.", "2+"),
        ("R2.2", "Limiter la durée du jeûne préopératoire à 6 heures pour les solides et "
         "encourager la prise de liquides clairs (eau, thé, café, sucrés ou non, jus de "
         "fruit sans pulpe) jusqu'à 2 heures avant la chirurgie, pour réduire l'anxiété "
         "préopératoire et la durée de séjour.", "1+"),
        ("R2.3", "Ne pas prescrire systématiquement de prémédication sédative avant une "
         "intervention, pour réduire la survenue de complications postopératoires.",
         "1-"),
        ("R2.4", "Admettre les patients le jour de l'intervention, pour réduire la durée "
         "de séjour sans modifier la survenue de complications.", "2+"),
        ("R2.5", "Mettre en place un programme de gestion personnalisée du capital "
         "sanguin (« patient blood management »), pour réduire la durée de séjour et "
         "les complications postopératoires.", "2+"),
    ], RCW))
    return story

# ---------------------------------------------------------------------------
def _section_champ3a():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Champ 3 — Mesures peropératoires (1/2)"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("R3.1", "Ne pas privilégier une modalité d'anesthésie générale (intraveineuse "
         "vs inhalée ; avec vs sans opiacés), pour réduire la durée d'hospitalisation et "
         "les complications postopératoires.", "1-"),
        ("R3.2", "Ne pas privilégier un type d'anesthésie (locorégionale neuraxiale vs "
         "générale) en chirurgie des membres inférieurs, pour réduire la durée "
         "d'hospitalisation et les complications postopératoires.", "1-"),
        ("R3.3", "Mettre en place une ventilation protectrice — volume courant 6-8 "
         "ml/kg de poids idéal théorique, PEP ≥ 5 cmH<sub>2</sub>O, manœuvres de "
         "recrutement alvéolaire itératives — en chirurgie programmée de l'adulte, pour "
         "diminuer les complications postopératoires.", "1+"),
        ("R3.4", "Administrer des anesthésiques locaux par voie péri-nerveuse en "
         "chirurgie des membres, pour réduire les complications postopératoires.", "1+"),
        ("R3.5", "Réaliser une analgésie locorégionale après une chirurgie thoracique ou "
         "abdominale majeure (dont vasculaire) par voie ouverte, pour réduire les "
         "complications postopératoires.", "1+"),
        ("R3.6", "Réaliser une analgésie locorégionale pour une chirurgie thoracique par "
         "vidéothoracoscopie, une chirurgie pariétale thoraco-abdomino-pelvienne ou une "
         "chirurgie rachidienne, pour réduire l'incidence des complications "
         "postopératoires.", "2+"),
        ("R3.7", "Utiliser la lidocaïne IV en peropératoire de chirurgie "
         "abdomino-pelvienne laparoscopique, pour réduire l'incidence des complications "
         "postopératoires.", "2+"),
        ("R3.8", "Optimiser les apports liquidiens peropératoires en se basant sur la "
         "pression artérielle et le volume d'éjection systolique, pour diminuer les "
         "complications postopératoires et la durée d'hospitalisation.", "2+"),
    ], RCW))
    return story

def _section_champ3b():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Champ 3 — Mesures peropératoires (2/2)"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("R3.9", "Utiliser un monitorage de la profondeur d'anesthésie, notamment chez "
         "les patients à risque (chirurgie ou comorbidités), pour diminuer les "
         "complications neuro-cognitives postopératoires.", "2+"),
    ], RCW))
    story.append(Spacer(1, 2 * mm))
    story.append(absence_note(
        "monitorage de l'analgésie (moniteurs d'analgésie) dans le cadre de la "
        "réhabilitation accélérée postopératoire — sous-question de R3.9, littérature "
        "actuelle insuffisante."))
    story.append(Spacer(1, 2 * mm))
    story.append(reco_table([
        ("R3.10", "Lutter contre l'hypothermie péri-opératoire, pour diminuer la "
         "survenue de complications postopératoires.", "1+"),
        ("R3.11", "Mettre en place un protocole de prévention des nausées et "
         "vomissements postopératoires, pour favoriser la réhabilitation "
         "postopératoire.", "1+"),
        ("R3.12", "Administrer de la dexaméthasone IV (4 ou 8 mg) lors de chaque "
         "anesthésie générale, pour réduire les complications postopératoires, en "
         "particulier les NVPO.", "1+"),
        ("R3.13", "Administrer de l'acide tranexamique en peropératoire de chirurgie "
         "majeure et/ou à risque hémorragique, pour réduire les complications "
         "hémorragiques et le recours à la transfusion péri-opératoire.", "1+"),
        ("R3.14", "Administrer une antibioprophylaxie en respectant les indications et "
         "modalités de la RFE SFAR « Antibioprophylaxie » (déjà git-trackée dans ce "
         "corpus), pour réduire les infections du site opératoire.", "1+"),
        ("R3.15", "Monitorer la curarisation et respecter la RFE SFAR « Curarisation et "
         "décurarisation en anesthésie » pour la décurarisation, pour réduire les "
         "complications postopératoires.", "1+"),
    ], RCW))
    return story

# ---------------------------------------------------------------------------
def _section_champ4_sources():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Champ 4 — Mesures postopératoires"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("R4.1", "Utiliser une analgésie multimodale associant antalgiques non "
         "morphiniques et anesthésiques locaux, pour réaliser une épargne morphinique "
         "et réduire la durée de séjour et les complications postopératoires.", "1+"),
        ("R4.2", "Implémenter des protocoles de thromboprophylaxie (déambulation "
         "précoce, thromboprophylaxie médicamenteuse, compression pneumatique "
         "intermittente selon le risque thromboembolique lié à la chirurgie et au "
         "patient), pour réduire les événements thromboemboliques veineux et les "
         "complications postopératoires.", "1+"),
        ("R4.3", "Mettre en place les mesures du programme d'optimisation dès la SSPI "
         "(reprise des boissons, déambulation, retrait des cathéters et de la sonde "
         "urinaire), pour diminuer la durée de séjour et les complications "
         "postopératoires.", "2+"),
        ("R4.4", "Débuter une alimentation orale dans les 24 premières heures "
         "postopératoires, y compris après chirurgie avec anastomoses digestives (hors "
         "chirurgie carcinologique de l'oropharynx et en l'absence de contre-indication "
         "chirurgicale), pour limiter la durée de séjour et les complications.", "1+"),
        ("R4.5.1", "Faire déambuler le patient idéalement dans les 12 premières heures "
         "et dans tous les cas avant la 24<super>e</super> heure postopératoire, pour "
         "réduire la durée de séjour.", "1+"),
        ("R4.5.2", "Faire déambuler le patient idéalement dans les 12 premières heures "
         "et dans tous les cas avant la 24<super>e</super> heure postopératoire, pour "
         "réduire les complications postopératoires.", "2+"),
        ("R4.6", "Établir une liste de critères de sortie d'hospitalisation, pour "
         "réduire la durée de séjour sans impacter la survenue de complications "
         "postopératoires.", "2+"),
    ], RCW))
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("Sources et avertissement", color=GREY))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>Méthode :</b> groupe de 29 experts SFAR, méthode GRADE (analyse "
        "bibliographique sur 10 ans, PRISMA, format PICO), vote GRADE grid en 2 tours. "
        "Règle de scope propre à ce document : une mesure devait être valable dans au "
        "moins 3 domaines chirurgicaux distincts pour faire l'objet d'une "
        "recommandation — les argumentaires ne discutent donc pas systématiquement "
        "tous les domaines et certaines recommandations peuvent ne pas s'appliquer à "
        "des chirurgies particulières.", S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>Document source :</b> SFAR, « Programme d'optimisation périopératoire du "
        "patient adulte », RFE, texte validé par le Comité des Référentiels Cliniques "
        "le 13/06/2022 et le Conseil d'Administration le 29/06/2022.", S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>URL source :</b> https://sfar.org/programme-doptimisation-perioperatoire-"
        "du-patient-adulte/", S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>Couverture :</b> intégralité des 30 recommandations et des 2 absences de "
        "recommandation (4 champs, 26 questions). L'Annexe 1 (2 forest-plots "
        "méta-analytiques soutenant R3.1, TIVA vs inhalation sur la survie/récidive "
        "carcinologique) et le schéma synoptique du programme mentionné dans la "
        "synthèse ne sont pas retranscrits — purement évidentiaires/illustratifs, sans "
        "information clinique au-delà du texte des recommandations. Composition "
        "nominative des groupes de travail et bibliographie complète non reproduites.",
        S_SOURCE))
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Avertissement :</b> cette fiche est une synthèse indépendante, produite "
        "pour un usage d'aide-mémoire. Elle reprend intégralement les 30 "
        "recommandations et les 2 absences de recommandation du texte source, mais "
        "condense l'argumentaire de chaque item. Elle ne remplace pas le texte "
        "intégral et n'est ni éditée ni validée par la SFAR.",
        S_BODY_SM), bg=GREY_LIGHT, border=GREY))
    return story

def _section_champ1_2():
    story = _section_intro_champ1()
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_champ2())
    return story

def _section_champ3_all():
    story = _section_champ3a()
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_champ3b())
    return story

# ---------------------------------------------------------------------------
SECTIONS = [
    ("Champ 1-2 — Généralités & mesures préopératoires", _section_champ1_2),
    ("Champ 3 — Mesures peropératoires", _section_champ3_all),
    ("Champ 4 — Mesures postopératoires & sources", _section_champ4_sources),
]

def _make_doc(path=None):
    return SimpleDocTemplate(path or OUT, pagesize=A4,
                              leftMargin=MARGIN, rightMargin=MARGIN,
                              topMargin=32 * mm, bottomMargin=16 * mm,
                              title="Fiche SFAR 2022 - Programme d'optimisation perioperatoire",
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
