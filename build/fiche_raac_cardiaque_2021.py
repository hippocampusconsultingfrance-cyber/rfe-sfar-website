# -*- coding: utf-8 -*-
"""
Fiche de synthese - "Rehabilitation amelioree apres chirurgie cardiaque
adulte sous CEC ou a coeur battant" - Recommandations Formalisees
d'Experts (RFE) SFAR/SFCTCV, 25/09/2021. 60 pages, telecharge depuis
sfar.org (wpdmdl=35416).

METHODOLOGIE : GRADE standard, meme famille que fiche_raac_orthopedique_
2019.py et fiche_raac_lobectomie_pulmonaire_2019.py. Synthese du texte
source : "33 recommandations. Apres trois tours de cotation et quelques
amendements, un accord fort a ete obtenu pour 33 recommandations [100%,
aucune exception]. Parmi ces recommandations, 10 ont un niveau de preuve
eleve (7 GRADE 1+ et 3 GRADE 1-), 19 ont un niveau de preuve modere a
faible (15 GRADE 2+ et 4 GRADE 2-) et 4 sont des avis d'experts. Enfin,
pour 3 questions, aucune recommandation n'a pu etre formulee." Decompte
verifie exact par extraction integrale des 33 items numerotes (R1.1 a
R6.3) et de leurs tags : 7+3+15+4+4=33 correspond exactement, et les 3
questions sans reponse correspondent aux 3 tags "ABSENCE DE
RECOMMANDATION" imprimes (dont 2 au sein de la meme Question 1 du Champ 4
- voies mini-invasives en chirurgie valvulaire aortique et en chirurgie
coronaire, sous-parties distinctes d'une question portant sur plusieurs
approches chirurgicales). Contrairement aux deux fiches RAAC precedentes
de ce corpus (orthopedique, lobectomie), AUCUNE incoherence de comptage
source n'a ete trouvee ici - tous les chiffres de synthese correspondent
exactement aux decomptes directs.

PERIMETRE : integral sur les 33 recommandations des 6 champs (parcours
patient/information, prise en charge et prehabilitation preoperatoire,
anesthesie et analgesie, strategie chirurgicale et gestion de la CEC,
gestion personnalisee du capital sanguin/PBM, rehabilitation
postoperatoire) et les 3 "absences de recommandation" disclosed
ci-dessus. Population pediatrique exclue (precise par le texte source).
Argumentaire minimal (regle 2026-09-14) : les etudes citees a l'appui de
chaque recommandation ne sont pas transcrites - seul l'enonce actionnable
est retenu. Bibliographie par question et composition nominative du
groupe d'experts (non reproduites) - non actionnable cliniquement.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from style import *
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.units import mm

OUT = "/home/user/rfe-sfar-website/output/Fiche_SFAR_SFCTCV_RAAC_Chirurgie_Cardiaque_2021.pdf"

SOURCE_TXT = ("Source : SFAR/SFCTCV, « Réhabilitation améliorée après chirurgie cardiaque "
              "adulte sous CEC ou à cœur battant », RFE, 25/09/2021. Fiche de synthèse non "
              "officielle : se référer au texte intégral.")

def P(txt, style=S_CELL):
    return Paragraph(txt, style)

def chip(label, **kw):
    return grade_chip(label, **kw)

CW_FULL = PAGE_W - 2 * MARGIN

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

RCW = [15 * mm, CW_FULL - 15 * mm - 16 * mm, 16 * mm]

def bullets(items, style=S_BODY_SM):
    html = "&bull; " + "<br/>&bull; ".join(items)
    return P(html, style)

def absence_note(question_txt):
    return info_panel(P(
        f"<b>Absence de recommandation</b> (données insuffisantes) : {question_txt}",
        S_BODY_SM), bg=GREY_LIGHT, border=GREY)

def legend_flowable():
    chip_w = 14 * mm
    content_w = CW_FULL
    row = Table([[chip("1+", width=chip_w - 2 * mm), chip("1-", width=chip_w - 2 * mm),
                  chip("2+", width=chip_w - 2 * mm), chip("2-", width=chip_w - 2 * mm),
                  chip("AE", width=chip_w - 2 * mm),
                  P("<b>GRADE</b> — 1+/1- : forte ; 2+/2- : faible ; <b>AE</b> : avis "
                    "d'experts (4/33, méthode GRADE non applicable). <b>Les 33 "
                    "recommandations ont toutes recueilli un accord fort</b>, sans "
                    "exception (aucune à accord faible — contrairement aux fiches "
                    "raac_orthopedique_2019 et raac_lobectomie_pulmonaire_2019 de ce "
                    "corpus, qui comptent chacune 1 exception).", S_BADGE_HEAD)]],
                colWidths=[chip_w] * 5 + [content_w - 5 * chip_w])
    row.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                              ("LEFTPADDING", (0, 0), (-1, -1), 1),
                              ("RIGHTPADDING", (0, 0), (-1, -1), 1),
                              ("TOPPADDING", (0, 0), (-1, -1), 0),
                              ("BOTTOMPADDING", (0, 0), (-1, -1), 0)]))
    return row

TOTAL_PAGES = {"n": 4}

def on_page(canvas, doc, page_title):
    header_band(canvas, doc, "SFAR / SFCTCV — RECOMMANDATIONS FORMALISÉES D'EXPERTS, 2021",
                "Réhabilitation améliorée après chirurgie cardiaque adulte",
                page_title, icon_fn=lambda c, x, y: icon_shield(c, x, y, 13 * mm), color=TEAL_DARK)
    footer_band(canvas, doc, SOURCE_TXT, f"Page {doc.page} / {TOTAL_PAGES['n']}")

# ---------------------------------------------------------------------------
def _section_intro_champ1_2():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Résumé :</b> 33 recommandations GRADE (SFAR/SFCTCV) organisées en 6 champs pour "
        "la réhabilitation améliorée après chirurgie cardiaque adulte (CEC ou à cœur "
        "battant, population pédiatrique exclue) : parcours patient/information, prise en "
        "charge et préhabilitation préopératoire, anesthésie/analgésie, stratégie "
        "chirurgicale et gestion de la CEC, gestion personnalisée du capital sanguin "
        "(PBM), réhabilitation postopératoire.", S_BODY), bg=BG_PANEL, border=TEAL_DARK))
    story.append(Spacer(1, 2.5 * mm))
    story.append(legend_flowable())
    story.append(Spacer(1, 3 * mm))
    story.append(KeepTogether([
        section_bar("Champ 1 — Sélection du parcours patient et information"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("R1.1", "Inclure les patients dans un programme de RAACC, pour réduire les durées "
         "de ventilation mécanique et d'hospitalisation en réanimation/hôpital.", "2+"),
        ("R1.2", "Délivrer une information et une éducation de qualité à l'aide de "
         "plusieurs supports avant chirurgie cardiaque, pour diminuer les complications "
         "postopératoires.", "2+"),
        ("R1.3", "Admettre les patients en unité de soins critiques (réanimation et/ou "
         "surveillance continue) en postopératoire, pour réduire les complications.", "2+"),
    ], RCW))
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Champ 2 — Prise en charge et préhabilitation préopératoire"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("R2.1", "Dépister la dénutrition avant chirurgie cardiaque pour la corriger, afin "
         "de diminuer les complications postopératoires.", "2+"),
        ("R2.2", "Obtenir le sevrage tabagique le plus tôt possible avant chirurgie "
         "cardiaque, pour réduire les complications notamment respiratoires.", "1+"),
        ("R2.3", "Disposer d'un dosage d'HbA1c de moins de 3 mois en préopératoire chez "
         "les patients diabétiques ou en syndrome métabolique, et prendre un avis "
         "diabétologique pour améliorer le contrôle glycémique.", "2+"),
        ("R2.4", "Proposer un programme de préhabilitation cardio-respiratoire et "
         "musculaire avant chirurgie cardiaque, pour diminuer complications et DMS.", "2+"),
        ("R2.5", "Procéder, sans dépistage microbiologique, à une décolonisation nasale du "
         "portage de S. aureus (mupirocine 2 % dans chaque narine) associée à une "
         "décontamination oropharyngée systématique par bain de bouche.", "1+"),
        ("R2.6", "Mettre en place une stratégie périopératoire de prévention de la "
         "fibrillation atriale postopératoire (maintien/introduction précoce "
         "d'anti-arythmiques), pour diminuer le risque d'AVC postopératoire.", "1+"),
        ("R2.7", "Ne pas initier de traitement par statine en l'absence de traitement "
         "préalable avant chirurgie cardiaque, pour réduire complications et DMS.", "2-"),
        ("R2.8", "Limiter le jeûne préopératoire à 6h pour les solides et 2h pour les "
         "liquides clairs, avec une solution carbohydratée préopératoire.", "2+"),
    ], RCW))
    return story

# ---------------------------------------------------------------------------
def _section_champ3():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Champ 3 — Anesthésie et analgésie pour chirurgie cardiaque"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("R3.1", "Ne pas privilégier des agents halogénés plutôt qu'intraveineux, pour "
         "diminuer complications et DMS.", "2-"),
        ("R3.2.1", "Appliquer une stratégie de ventilation protectrice hors CEC (Vt 6-8 "
         "mL/kg de poids idéal, PEP, manœuvres de recrutement), pour diminuer les "
         "complications respiratoires.", "2+"),
        ("R3.2.2", "Ne pas appliquer de ventilation pendant la CEC, pour diminuer les "
         "complications respiratoires et la DMS.", "2-"),
        ("R3.3", "Utiliser une stratégie d'optimisation hémodynamique per et "
         "postopératoire (monitorage systématique du volume d'éjection systolique, "
         "bilans entrées-sorties).", "2+"),
        ("R3.4.1", "Réaliser une analgésie locorégionale en privilégiant les blocs "
         "échoguidés de la paroi thoracique (injection unique ou continue).", "2+"),
        ("R3.4.2", "Ne pas réaliser d'infiltration pré-sternale et/ou d'analgésie par "
         "cathéter pré-sternal, pour diminuer les complications postopératoires.", "1-"),
        ("R3.5.1", "Utiliser une analgésie multimodale systémique avec épargne "
         "morphinique (aucune classe thérapeutique supérieure démontrée hors "
         "paracétamol).", "2+"),
        ("R3.5.2", "Ne pas utiliser la gabapentine dans le cadre de l'analgésie "
         "multimodale en chirurgie cardiaque, pour diminuer les complications.", "1-"),
    ], RCW))
    return story

# ---------------------------------------------------------------------------
def _section_champ4():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Champ 4 — Stratégie chirurgicale et gestion de la CEC"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(absence_note(
        "impact des voies mini-invasives en chirurgie valvulaire aortique — ne peut faire "
        "l'objet de recommandation dans l'état actuel de la littérature."))
    story.append(Spacer(1, 2 * mm))
    story.append(reco_table([
        ("R4.1", "Favoriser la chirurgie mitrale vidéo-assistée, pour diminuer le taux de "
         "transfusion et la DMS, sous réserve de l'expertise de l'équipe.", "AE"),
    ], RCW))
    story.append(Spacer(1, 2 * mm))
    story.append(absence_note(
        "impact des voies mini-invasives en chirurgie coronaire — ne peut faire l'objet "
        "de recommandation dans l'état actuel de la littérature."))
    story.append(Spacer(1, 2 * mm))
    story.append(reco_table([
        ("R4.2", "Réaliser la chirurgie sous CEC en normothermie, pour diminuer le risque "
         "de transfusion postopératoire.", "1+"),
        ("R4.3.1", "Ne pas réaliser les pontages à cœur battant de façon systématique, "
         "même après 75 ans, pour réduire mortalité et complications.", "1-"),
        ("R4.3.2", "Considérer la technique des pontages à cœur battant chez les patients "
         "à aorte très athéromateuse ou calcifiée, pour limiter le risque d'AVC lié au "
         "clampage aortique.", "AE"),
        ("R4.4", "Privilégier une technique de « CEC optimisée », pour réduire "
         "complications postopératoires et mortalité hospitalière.", "1+"),
        ("R4.5", "Ne pas privilégier une méthode de cardioplégie plutôt qu'une autre, pour "
         "réduire complications ou DMS.", "2-"),
    ], RCW))
    return story

# ---------------------------------------------------------------------------
def _section_champ5_6_sources():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Champ 5 — Gestion personnalisée du capital sanguin (PBM)"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("R5.1.1", "Implémenter un programme de PBM en chirurgie cardiaque, notamment "
         "rechercher et corriger une anémie ferriprive, pour réduire le recours aux "
         "transfusions.", "1+"),
        ("R5.1.2", "Implémenter un programme de PBM et corriger une anémie ferriprive, "
         "pour diminuer les complications postopératoires et la DMS.", "2+"),
        ("R5.2", "Utiliser un système de récupération sanguine peropératoire pour limiter "
         "la transfusion érythrocytaire.", "2+"),
    ], RCW))
    story.append(Spacer(1, 2 * mm))
    story.append(absence_note(
        "stratégie transfusionnelle restrictive ou libérale — les données actuelles ne "
        "permettent pas de recommander l'une ou l'autre stratégie pour diminuer "
        "complications ou DMS."))
    story.append(Spacer(1, 2 * mm))
    story.append(reco_table([
        ("R5.3", "Considérer individuellement l'état clinique du patient, le risque "
         "chirurgical et la balance apports en oxygène/extraction tissulaire, plutôt "
         "qu'une valeur systématique de seuil transfusionnel.", "AE"),
    ], RCW))
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Champ 6 — Réhabilitation postopératoire"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("R6.1", "Réaliser une extubation précoce (dans les 6h suivant la fin de la "
         "chirurgie), pour diminuer les complications et les durées de séjour.", "1+"),
        ("R6.2.1", "Mobiliser précocement les patients, pour réduire la morbidité "
         "postopératoire et les durées d'hospitalisation.", "2+"),
        ("R6.2.2", "Retirer précocement les drains thoraciques, la sonde vésicale et les "
         "cathéters artériel/veineux central, pour permettre la mobilisation précoce.",
         "AE"),
        ("R6.3", "Associer au programme de préhabilitation un programme de réhabilitation "
         "postopératoire débuté dans les 2 premières semaines (cardiovasculaire, "
         "kinésithérapie respiratoire et mobilisatrice).", "2+"),
    ], RCW))
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("Sources et avertissement"))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "SFAR/SFCTCV, « Réhabilitation améliorée après chirurgie cardiaque adulte sous CEC "
        "ou à cœur battant », RFE, validée le 25/09/2021. Méthode GRADE (3 tours de "
        "cotation, quelques amendements). Références bibliographiques par question et "
        "composition nominative du groupe d'experts (non reproduites ici).", S_SOURCE))
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Avertissement :</b> cette fiche est une synthèse indépendante, produite pour un "
        "usage d'aide-mémoire. Elle reprend intégralement les 33 recommandations et les 3 "
        "cas d'absence de recommandation du texte source, mais condense l'argumentaire de "
        "chaque item et omet la composition nominative du groupe d'experts. Elle ne "
        "remplace pas le texte intégral et n'est ni éditée ni validée par la SFAR/SFCTCV.",
        S_BODY_SM), bg=GREY_LIGHT, border=GREY))
    return story

# ---------------------------------------------------------------------------
def _section_all():
    story = _section_intro_champ1_2()
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_champ3())
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_champ4())
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_champ5_6_sources())
    return story

SECTIONS = [
    ("Réhabilitation améliorée après chirurgie cardiaque adulte", _section_all),
]

def _make_doc(path=None):
    return SimpleDocTemplate(path or OUT, pagesize=A4,
                              leftMargin=MARGIN, rightMargin=MARGIN,
                              topMargin=32 * mm, bottomMargin=16 * mm,
                              title="Fiche SFAR-SFCTCV 2021 - RAAC chirurgie cardiaque adulte",
                              author="Synthèse indépendante (source SFAR/SFCTCV)")

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
