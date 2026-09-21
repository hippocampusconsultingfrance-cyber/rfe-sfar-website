# -*- coding: utf-8 -*-
"""
Fiche de synthese - "Optimisation hemodynamique perioperatoire -
Pediatrie" - Recommandations pour la Pratique Professionnelle (RPP) SFAR,
mars 2024. 35 pages, telecharge depuis sfar.org (wpdmdl=62046).

METHODOLOGIE : methode GRADE pour l'analyse de la litterature (PRISMA)
mais format RPP retenu en amont (peu d'essais randomises controles chez
l'enfant permettant une recommandation graduee forte/faible classique) -
"les experts suggerent de faire/ne pas faire" pour chaque avis, cotation
GRADE grid. Synthese du texte source : "9 avis d'experts. Un accord fort
a ete obtenu pour 9 avis d'experts. Enfin, pour 4 questions, aucun avis
d'experts n'a pu etre formule." Decompte verifie exact par extraction
integrale : 9 items numerotes (R1.1.1-1.1.3 regroupes sous un seul avis
d'experts commun car sous-strates d'age d'une meme question, R2.1, R3.1,
R3.2, R4.1.1, R4.1.2, R4.2 individuellement tagges) et 4 tags "ABSENCE DE
RECOMMANDATION" imprimes, tous deux "Accord fort" - correspond exactement
aux chiffres de synthese, AUCUNE incoherence source trouvee (contrairement
a plusieurs fiches RAAC de ce corpus). Chip unique "AE" (avis d'experts) :
document entierement non-grade (methode GRADE appliquee seulement en
amont pour l'analyse bibliographique, jamais imprimee comme grade
numerique par item - le texte source precise explicitement la distinction
entre "absence de recommandation" [litterature insuffisante, evaluation
individualisee requise] et "recommandation negative" [litterature
suffisante pour dire de ne pas faire] - aucune des 9 recs de ce document
n'est une recommandation negative, disclosed pour clarte).

PERIMETRE : integral sur les 4 champs (optimisation de la pression
arterielle, VES/indices dynamiques pour guider l'expansion volemique,
indices de perfusion tissulaire, expansion volemique/vasoconstricteurs/
inotropes) et les 4 absences de recommandation. Complementaire, non
redondant, de la fiche existante `remplissage_perioperatoire` (RFE SFAR/
Adarpef 2012, remplissage guide par le VES chez l'adulte a haut risque,
brève mention pediatrique regle 4-2-1 uniquement) - ce document-ci est
un RPP 2024 dedie et beaucoup plus detaille specifiquement a la pediatrie
(cibles de PAM par tranche d'age, solutes recommandes, seuils
vasoconstricteurs). Argumentaire minimal (regle 2026-09-14) : les etudes
citees a l'appui de chaque avis ne sont pas transcrites - seul l'enonce
actionnable est retenu. Bibliographie et composition nominative du
groupe d'experts (non reproduites) - non actionnable cliniquement.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from style import *
GRADE_COLORS["AE"] = (GREY, WHITE)
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.units import mm

OUT = "/home/user/rfe-sfar-website/output/Fiche_SFAR_Optimisation_Hemodynamique_Pediatrie_2024.pdf"

SOURCE_TXT = ("Source : SFAR, « Optimisation hémodynamique périopératoire – Pédiatrie », RPP, "
              "mars 2024. Fiche de synthèse non officielle : se référer au texte intégral.")

def P(txt, style=S_CELL):
    return Paragraph(txt, style)

def chip(label, **kw):
    return grade_chip(label, **kw)

CW_FULL = PAGE_W - 2 * MARGIN

def reco_table(rows, col_widths):
    """rows: (ref, text, grade_label)."""
    data = [[P("Réf.", S_HEAD_W), P("Avis d'experts", S_HEAD_W), P("Cotation", S_HEAD_W_C)]]
    for ref, txt, grade in rows:
        data.append([P(ref, S_CELL_B), P(txt, S_CELL), chip(grade, width=17 * mm)])
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

RCW = [15 * mm, CW_FULL - 15 * mm - 18 * mm, 18 * mm]

def bullets(items, style=S_BODY_SM):
    html = "&bull; " + "<br/>&bull; ".join(items)
    return P(html, style)

def absence_note(question_txt):
    return info_panel(P(
        f"<b>Absence de recommandation</b> (littérature insuffisante — nécessite une "
        f"évaluation individualisée bénéfice/risque) : {question_txt}",
        S_BODY_SM), bg=GREY_LIGHT, border=GREY)

def legend_flowable():
    chip_w = 17 * mm
    content_w = CW_FULL
    row = Table([[chip("AE", width=chip_w - 2 * mm),
                  P("<b>AE = Avis d'experts</b> — méthode GRADE grid (≥ 70 % d'opinions "
                    "favorables, &lt; 20 % contraires). <b>Les 9 avis d'experts ont tous "
                    "recueilli un accord fort</b>, sans exception ; document entièrement "
                    "non gradé (aucun GRADE 1+/1-/2+/2- imprimé — la méthode GRADE n'a "
                    "servi qu'à l'analyse bibliographique en amont). Une « absence de "
                    "recommandation » (littérature insuffisante, 4 cas) est distincte "
                    "d'une recommandation négative (« il ne faut pas faire », absente de "
                    "ce document) — distinction explicite du texte source.",
                    S_BADGE_HEAD)]],
                colWidths=[chip_w, content_w - chip_w])
    row.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                              ("LEFTPADDING", (0, 0), (-1, -1), 1),
                              ("RIGHTPADDING", (0, 0), (-1, -1), 1),
                              ("TOPPADDING", (0, 0), (-1, -1), 0),
                              ("BOTTOMPADDING", (0, 0), (-1, -1), 0)]))
    return row

TOTAL_PAGES = {"n": 2}

def on_page(canvas, doc, page_title):
    header_band(canvas, doc, "SFAR — RECOMMANDATIONS POUR LA PRATIQUE PROFESSIONNELLE, 2024",
                "Optimisation hémodynamique périopératoire — Pédiatrie",
                page_title, icon_fn=lambda c, x, y: icon_drop(c, x, y, 13 * mm), color=TEAL_DARK)
    footer_band(canvas, doc, SOURCE_TXT, f"Page {doc.page} / {TOTAL_PAGES['n']}")

# ---------------------------------------------------------------------------
def _section_all():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Résumé :</b> RPP SFAR sur l'optimisation hémodynamique périopératoire en "
        "pédiatrie — 9 avis d'experts sur 4 champs : cibles de pression artérielle par "
        "tranche d'âge, monitorage du volume d'éjection systolique/indices dynamiques, "
        "indices de perfusion tissulaire, expansion volémique et vasoconstricteurs. "
        "Transfusion exclue du champ.", S_BODY), bg=BG_PANEL, border=TEAL_DARK))
    story.append(Spacer(1, 2.5 * mm))
    story.append(legend_flowable())
    story.append(Spacer(1, 3 * mm))
    story.append(KeepTogether([
        section_bar("Champ 1 — Optimisation périopératoire de la pression artérielle"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("R1.1.1", "Chez l'enfant anesthésié &lt; 6 mois, maintenir une PA moyenne "
         "peropératoire &gt; 35 mmHg pour limiter les complications cérébrales.", "AE"),
        ("R1.1.2", "Chez l'enfant anesthésié de 6 mois à 2 ans, maintenir une PA moyenne "
         "peropératoire &gt; 43 mmHg pour limiter les complications cérébrales.", "AE"),
        ("R1.1.3", "Chez l'enfant anesthésié de 2 à 10 ans, maintenir une PA moyenne "
         "peropératoire &gt; [1,5 × âge (ans) + 40] mmHg pour limiter la morbidité "
         "postopératoire.", "AE"),
    ], RCW))
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Champ 2 — VES et indices dynamiques pour l'expansion volémique"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(absence_note(
        "intérêt du monitorage du volume d'éjection systolique pour optimiser "
        "l'hémodynamique et diminuer la morbi-mortalité, pour la population pédiatrique "
        "générale."))
    story.append(Spacer(1, 2 * mm))
    story.append(absence_note(
        "intérêt des indices dynamiques seuls pour optimiser l'expansion volémique, pour "
        "la population pédiatrique générale."))
    story.append(Spacer(1, 2 * mm))
    story.append(reco_table([
        ("R2.1", "Utiliser le Doppler œsophagien pour optimiser l'hémodynamique "
         "peropératoire du patient pédiatrique à risque élevé ou très élevé, si la tête "
         "est accessible et en l'absence d'échocardiographie peropératoire.", "AE"),
    ], RCW))
    return story

def _section_champ3_4_sources():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Champ 3 — Indices de perfusion tissulaire"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("R3.1", "La surveillance de la lactatémie, en cas de circonstances évocatrices "
         "d'hypoxie tissulaire (bas débit peropératoire), peut être utile pour estimer la "
         "sévérité de la souffrance cellulaire et son évolution.", "AE"),
    ], RCW))
    story.append(Spacer(1, 2 * mm))
    story.append(absence_note(
        "intérêt de la différence veino-artérielle en CO2 (DIVA-CO2) et de la saturation "
        "veineuse en oxygène (ScvO2)."))
    story.append(Spacer(1, 2 * mm))
    story.append(reco_table([
        ("R3.2", "Utiliser un monitorage de la perfusion/oxygénation tissulaire cérébrale "
         "chez l'enfant &lt; 1 an opéré d'une chirurgie majeure ou à risque cérébral "
         "particulier, pour optimiser l'hémodynamique peropératoire.", "AE"),
    ], RCW))
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Champ 4 — Expansion volémique, vasoconstricteurs, inotropes"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("R4.1.1", "Privilégier l'expansion volémique initiale par un soluté cristalloïde "
         "balancé, limité dans le temps, pour maintenir l'homéostasie biologique et "
         "circulatoire.", "AE"),
        ("R4.1.2", "Chez le nouveau-né et le jeune nourrisson, utiliser l'albumine à 4-5 % "
         "après l'expansion volémique initiale cristalloïde, pour limiter le volume "
         "d'expansion volémique.", "AE"),
        ("R4.2", "En cas d'hypotension artérielle peropératoire persistante malgré une "
         "expansion volémique adaptée, utiliser un vasoconstricteur avec des doses "
         "rapportées au poids majorées par rapport à l'adulte.", "AE"),
    ], RCW))
    story.append(Spacer(1, 2 * mm))
    story.append(absence_note("quel vasoconstricteur utiliser pour la population pédiatrique."))
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("Sources et avertissement"))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "SFAR, « Optimisation hémodynamique périopératoire – Pédiatrie », RPP, mars 2024. "
        "Méthode GRADE (analyse de la littérature, PRISMA) + cotation GRADE grid. "
        "Références bibliographiques citées dans le texte intégral (non reproduites "
        "ici) ; composition nominative du groupe d'experts (non reproduite).", S_SOURCE))
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Avertissement :</b> cette fiche est une synthèse indépendante, produite pour un "
        "usage d'aide-mémoire. Elle reprend intégralement les 9 avis d'experts et les 4 "
        "cas d'absence de recommandation du texte source, mais condense l'argumentaire "
        "de chaque item et omet la composition nominative du groupe d'experts. Elle ne "
        "remplace pas le texte intégral et n'est ni éditée ni validée par la SFAR.",
        S_BODY_SM), bg=GREY_LIGHT, border=GREY))
    return story

def _section_full():
    story = _section_all()
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_champ3_4_sources())
    return story

SECTIONS = [
    ("Optimisation hémodynamique périopératoire — Pédiatrie", _section_full),
]

def _make_doc(path=None):
    return SimpleDocTemplate(path or OUT, pagesize=A4,
                              leftMargin=MARGIN, rightMargin=MARGIN,
                              topMargin=32 * mm, bottomMargin=16 * mm,
                              title="Fiche SFAR 2024 - Optimisation hemodynamique perioperatoire pediatrie",
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
