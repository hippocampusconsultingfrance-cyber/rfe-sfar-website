# -*- coding: utf-8 -*-
"""
Fiche de synthese - "Rehabilitation amelioree apres chirurgie orthopedique
lourde du membre inferieur (Arthroplastie de hanche et de genou hors
fracture)" - Recommandations Formalisees d'Experts (RFE) SFAR, 20/09/2019.
36 pages, telecharge depuis sfar.org (wpdmdl=24459).

METHODOLOGIE : GRADE standard (comite de 19 experts, format PICO, 18
questions). "L'analyse de la litterature et les recommandations ont ete
formulees selon la methodologie GRADE".

DISCLOSURE - 3 incoherences internes au texte source, constatees par
transcription integrale et decompte direct, jamais resolues silencieusement
(regle de projet) :
1) Decompte total : la synthese (francaise ET anglaise) annonce "23
   recommandations" (7 GRADE1 + 15 GRADE2 + 1 avis d'experts). Un decompte
   direct des items numerotes (R1.1/R1.2, R2, R3.1-3.4, R4, R5, R6, R7, R8,
   R9, R10.1-10.4, R11.1-11.3, R12, R13, R14, R15) totalise 24 items, avec
   8 portant un tag GRADE1 (pas 7) - le compte GRADE2 (15) et avis
   d'experts (1, = R11.3) correspondent exactement. Ecart de 1 non resolu,
   localise sur le sous-total GRADE1.
2) Accord : la synthese affirme "un accord fort a ete obtenu pour
   l'ensemble des recommandations" apres 2 tours + 1 amendement. Pourtant
   R2 (gabapentinoides) porte elle-meme, imprime dans le texte source
   juste apres son grade, le tag "(accord faible)" - contradiction non
   resolue, chip "2-*" utilise pour cette seule recommandation avec note
   explicite.
3) Questions sans reponse : la synthese annonce "deux questions [qui]
   n'ont pas trouve de reponse dans la litterature". Le texte imprime
   pourtant la mention explicite "ABSENCE DE RECOMMANDATION" a 3 reprises
   (Question 2 - information/education preoperatoire ; Question 3 -
   rehabilitation preoperatoire/prehabilitation ; Question 7 -
   optimisation des apports liquidiens peroperatoire). Les 3 sont
   transcrites ici, pas seulement 2.

PERIMETRE : integral sur les 18 questions (15 avec recommandation graduee
ou avis d'experts, 3 avec absence de recommandation explicite). Argumentaire
minimal (regle 2026-09-14) : les etudes/statistiques citees a l'appui de
chaque recommandation ne sont pas transcrites - seul l'enonce de la
recommandation (et, pour R11.3, les conditions cliniques explicites qui
encadrent son usage) est retenu. Bibliographie par question (~10 refs
chacune, non reproduite), composition du comite d'experts (page 4, non
reproduite - non actionnable cliniquement).
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from style import *
GRADE_COLORS["2-*"] = (AMBER, WHITE)
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.units import mm

OUT = "/home/user/rfe-sfar-website/output/Fiche_SFAR_RAAC_Orthopedique_Hanche_Genou_2019.pdf"

SOURCE_TXT = ("Source : SFAR, « Réhabilitation améliorée après chirurgie orthopédique lourde "
              "du membre inférieur (arthroplastie de hanche et de genou) », RFE, 20/09/2019. "
              "Fiche de synthèse non officielle : se référer au texte intégral.")

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

RCW = [14 * mm, CW_FULL - 14 * mm - 16 * mm, 16 * mm]

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
                  P("<b>GRADE</b> — 1+/1- : recommandation <b>forte</b> (« il faut faire / "
                    "ne pas faire ») ; 2+/2- : recommandation <b>faible</b> (« il est "
                    "probablement recommandé... ») ; <b>AE</b> : avis d'experts, méthode "
                    "GRADE non applicable (R11.3 uniquement). Sauf mention contraire, la "
                    "cotation collective de toutes les recommandations est « accord fort » "
                    "— <b>seule R2 porte le tag imprimé « accord faible »</b>, en "
                    "contradiction avec la synthèse du texte source qui annonce un accord "
                    "fort unanime (incohérence disclosed, non résolue).", S_BADGE_HEAD)]],
                colWidths=[chip_w] * 5 + [content_w - 5 * chip_w])
    row.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                              ("LEFTPADDING", (0, 0), (-1, -1), 1),
                              ("RIGHTPADDING", (0, 0), (-1, -1), 1),
                              ("TOPPADDING", (0, 0), (-1, -1), 0),
                              ("BOTTOMPADDING", (0, 0), (-1, -1), 0)]))
    return row

TOTAL_PAGES = {"n": 6}

def on_page(canvas, doc, page_title):
    header_band(canvas, doc, "SFAR — RECOMMANDATIONS FORMALISÉES D'EXPERTS, 2019",
                "Réhabilitation améliorée — arthroplastie de hanche/genou",
                page_title, icon_fn=lambda c, x, y: icon_shield(c, x, y, 13 * mm), color=TEAL_DARK)
    footer_band(canvas, doc, SOURCE_TXT, f"Page {doc.page} / {TOTAL_PAGES['n']}")

# ---------------------------------------------------------------------------
def _section_intro():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Résumé :</b> 18 questions cliniques sur la réhabilitation améliorée (RAC) après "
        "arthroplastie de hanche ou de genou programmée (hors fracture) — 15 questions avec "
        "recommandation (graduée GRADE ou avis d'experts), 3 sans réponse dans la "
        "littérature (absence de recommandation explicite). Objectif : durée de séjour (DMS) "
        "et complications postopératoires.", S_BODY), bg=BG_PANEL, border=TEAL))
    story.append(Spacer(1, 2.5 * mm))
    story.append(legend_flowable())
    story.append(Spacer(1, 2 * mm))
    story.append(info_panel(P(
        "<b>⚠ 3 incohérences du texte source, disclosed non résolues</b> (voir docstring du "
        "script pour le détail complet) : (1) décompte total 23 vs 24 items numérotés "
        "(écart sur le sous-total GRADE1, 7 annoncé vs 8 dénombré) ; (2) « accord fort pour "
        "l'ensemble » annoncé alors que R2 porte le tag imprimé « accord faible » ; "
        "(3) « deux questions sans réponse » annoncées alors que 3 portent la mention "
        "explicite « ABSENCE DE RECOMMANDATION » (Q2, Q3, Q7).", S_BODY_SM),
        bg=AMBER_LIGHT, border=AMBER))
    return story

# ---------------------------------------------------------------------------
def _section_generalites_preop():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Généralités — Mise en place d'un programme de réhabilitation"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("R1.1", "Il est recommandé de mettre en place un programme de récupération "
         "améliorée afin de réduire la durée de séjour des patients opérés d'une "
         "arthroplastie de hanche ou de genou.", "1+"),
        ("R1.2", "Il est probablement recommandé de mettre en place un programme de "
         "récupération améliorée afin de réduire l'incidence de certaines complications "
         "après arthroplastie de hanche ou de genou.", "2+"),
    ], RCW))
    story.append(Spacer(1, 2 * mm))
    story.append(absence_note(
        "l'utilité de l'information et de l'éducation préopératoire du patient (Q2) et de "
        "la rééducation préopératoire/préhabilitation (Q3) sur la durée de séjour ou la "
        "survenue de complications — données contradictoires ou insuffisantes."))
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Préopératoire"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("R2", "Il n'est probablement pas recommandé d'utiliser systématiquement les "
         "gabapentinoïdes en péri-opératoire pour diminuer la douleur postopératoire "
         "(cotée « accord faible » dans le texte source, cf. encart ⚠ ci-dessus).",
         "2-*"),
        ("R3.1", "Il est recommandé d'utiliser l'érythropoïétine en préopératoire chez les "
         "patients ayant une anémie modérée (Hb 10-13 g/dL) pour diminuer le risque "
         "transfusionnel.", "1+"),
        ("R3.2", "Il est probablement recommandé d'ajuster le nombre d'injections "
         "d'érythropoïétine en fonction du taux d'Hb préopératoire et d'y associer un "
         "apport de fer (au mieux IV) en début de traitement.", "2+"),
        ("R3.3", "Il n'est pas recommandé d'utiliser des dispositifs de récupération de "
         "sang en périopératoire lorsqu'une stratégie d'épargne sanguine préopératoire est "
         "appliquée.", "1-"),
        ("R3.4", "Il est recommandé d'utiliser l'acide tranexamique en périopératoire pour "
         "diminuer le saignement, le recours transfusionnel et la DMS.", "1+"),
        ("R4", "Il n'est pas recommandé de réaliser un bilan infectieux systématique avant "
         "une arthroplastie du membre inférieur.", "1-"),
    ], RCW))
    return story

# ---------------------------------------------------------------------------
def _section_peropératoire():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Peropératoire"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(absence_note(
        "la gestion des apports liquidiens en peropératoire (Q7) — aucune étude "
        "spécifique dans ce contexte de réhabilitation ; chirurgie à risque intermédiaire "
        "pouvant nécessiter un monitorage hémodynamique invasif chez les patients à haut "
        "risque cardiovasculaire."))
    story.append(Spacer(1, 2 * mm))
    story.append(reco_table([
        ("R5", "Il est probablement recommandé d'administrer de la dexaméthasone IV en "
         "peropératoire pour diminuer la douleur postopératoire et l'incidence des "
         "nausées-vomissements.", "2+"),
        ("R6", "Il est recommandé de lutter contre l'hypothermie en péri-opératoire pour "
         "diminuer la survenue des complications hémorragiques per et postopératoires.",
         "1+"),
        ("R7", "Il n'est probablement pas recommandé de privilégier un type d'anesthésie "
         "(générale ou rachianesthésie) pour diminuer la DMS ou la survenue de "
         "complications.", "2-"),
        ("R8", "Il n'est probablement pas recommandé de privilégier une technique "
         "chirurgicale particulière pour réduire la DMS ou la survenue de complications.",
         "2-"),
        ("R9", "Il n'est probablement pas recommandé d'utiliser systématiquement un garrot "
         "pneumatique en peropératoire d'arthroplastie de genou pour réduire la DMS ou la "
         "survenue de complications.", "2-"),
    ], RCW))
    return story

# ---------------------------------------------------------------------------
def _section_postop_analgesie_thrombo():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Postopératoire — Analgésie"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("R10.1", "Il est probablement recommandé d'appliquer une stratégie d'épargne "
         "morphinique en postopératoire pour réduire la DMS et les complications "
         "digestives/respiratoires.", "2+"),
        ("R10.2", "Il est recommandé d'utiliser des techniques d'analgésie locale et/ou "
         "loco-régionale pour diminuer la douleur et la consommation de morphiniques "
         "après arthroplastie de genou.", "1+"),
        ("R10.3", "Il n'est probablement pas recommandé d'utiliser une rachianalgésie à la "
         "morphine ou une analgésie péridurale pour la prise en charge de la douleur après "
         "arthroplastie de hanche ou de genou.", "2-"),
        ("R10.4", "Il est probablement recommandé, en l'absence de contre-indication, de "
         "prescrire des AINS en postopératoire pour diminuer la consommation de "
         "morphiniques et leurs complications associées.", "2+"),
    ], RCW))
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Postopératoire — Thromboprophylaxie"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("R11.1", "Il est recommandé d'administrer une thromboprophylaxie après "
         "arthroplastie de hanche ou de genou pour diminuer les complications "
         "thromboemboliques postopératoires.", "1+"),
        ("R11.2", "L'aspirine est probablement recommandée après arthroplastie de hanche "
         "ou de genou comme alternative aux HBPM et aux anticoagulants oraux directs, dans "
         "les conditions ci-dessous (R11.3).", "2+"),
        ("R11.3", "Si le patient est inclus dans un programme de RAC, sans facteur de "
         "risque thromboembolique associé, levé dans les 24 premières heures "
         "postopératoires, sans AINS non-sélectifs associés, et avec une durée "
         "d'hospitalisation prévisible &lt; 3 jours : l'aspirine peut être utilisée comme "
         "alternative aux HBPM/AOD pour la thromboprophylaxie postopératoire. Choix "
         "individuel selon les facteurs de risque thromboembolique et hémorragique du "
         "patient.", "AE"),
    ], RCW))
    return story

# ---------------------------------------------------------------------------
def _section_postop_recuperation_sources():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Postopératoire — Récupération"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("R12", "Il n'est probablement pas recommandé d'utiliser un drainage chirurgical "
         "systématique en postopératoire pour diminuer la DMS ou les complications.", "2-"),
        ("R13", "Il est probablement recommandé d'utiliser une cryothérapie pour réduire "
         "la douleur postopératoire précoce.", "2+"),
        ("R14", "Il est probablement recommandé de lever les patients dans les 24 "
         "premières heures postopératoires pour réduire la DMS.", "2+"),
        ("R15", "Une rééducation précoce est probablement recommandée après arthroplastie "
         "de hanche ou de genou pour réduire la DMS.", "2+"),
    ], RCW))
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("Sources et avertissement"))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "SFAR, « Réhabilitation améliorée après chirurgie orthopédique lourde du membre "
        "inférieur (Arthroplastie de hanche et de genou hors fracture) », RFE, comité de "
        "19 experts, méthode GRADE (format PICO, 18 questions), validé le 20/09/2019. "
        "Références bibliographiques par question (non reproduites ici) ; composition "
        "nominative du comité d'experts (non reproduite).", S_SOURCE))
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Avertissement :</b> cette fiche est une synthèse indépendante, produite pour un "
        "usage d'aide-mémoire. Elle reprend intégralement les 24 items recommandés/gradés "
        "(dont le tag « accord faible » de R2 et les 3 mentions « absence de "
        "recommandation ») mais condense l'argumentaire de chaque question et omet la "
        "composition nominative du comité. Elle ne remplace pas le texte intégral et n'est "
        "ni éditée ni validée par la SFAR.", S_BODY_SM), bg=GREY_LIGHT, border=GREY))
    return story

# ---------------------------------------------------------------------------
def _section_all():
    story = _section_intro()
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_generalites_preop())
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_peropératoire())
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_postop_analgesie_thrombo())
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_postop_recuperation_sources())
    return story

SECTIONS = [
    ("Réhabilitation améliorée — arthroplastie de hanche/genou", _section_all),
]

def _make_doc(path=None):
    return SimpleDocTemplate(path or OUT, pagesize=A4,
                              leftMargin=MARGIN, rightMargin=MARGIN,
                              topMargin=32 * mm, bottomMargin=16 * mm,
                              title="Fiche SFAR 2019 - RAAC orthopedique hanche/genou",
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
