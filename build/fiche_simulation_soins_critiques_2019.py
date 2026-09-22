# -*- coding: utf-8 -*-
"""
Fiche de synthese - "Interets de l'apprentissage par simulation en soins
critiques" - Recommandations communes SRLF/SFAR/SFMU/SOFRASIMS,
Recommandations pour la Pratique Professionnelle (RPP), texte valide par
les CA de la SRLF (20/12/2018), de la SFAR (10/01/2019), de la SFMU
(16/01/2019) et de la SOFRASIMS (18/01/2019). 41 pages, telecharge depuis
sfar.org (wp-content/uploads/2019/05/rfe-interets-de-lapprentissage-par-
simulation-en-soins-critiques.pdf - le slug de l'URL source dit "rfe" mais
le texte precise explicitement avoir choisi un format RPP plutot que RFE,
divergence disclosed ici, non corrigee).

METHODOLOGIE : methode GRADE pour l'analyse de la litterature (format PICO)
mais format RPP retenu en amont (terminologie "les experts suggerent de
faire/ne pas faire"), cotation GRADE grid (>= 70% d'opinions favorables,
< 20% d'opinions contraires pour valider). 24 recommandations au total (10
competences techniques + 12 competences non techniques + 2 situations
sanitaires exceptionnelles, decompte explicite de la synthese du texte
source, verifie exact par extraction integrale des 24 items). **Chip
unique "AF" (Accord Fort)** : les 24 recommandations ont recueilli un
accord fort, sans exception - aucune recommandation a accord faible ou
avis d'experts distinct, verifie par grep exhaustif ("Accord fort" x24,
"Accord faible" x0 dans le texte source).

DISCLOSURE - numerotation source irreguliere : R1.3 est imprimee sans le
point separant le numero du texte ("R1.3 Les experts...", contre "R 1.1."
etc. pour les autres) - artefact de mise en forme du PDF source, item
neanmoins present et transcrit normalement (pas un saut de numerotation
reel, verifie par lecture du texte source complet).

PERIMETRE : integral sur les 24 recommandations des 3 champs (competences
techniques, competences non techniques, situations sanitaires
exceptionnelles). Argumentaire minimal (regle 2026-09-14) : les etudes
citees a l'appui de chaque recommandation (bibliographie de ~150
references) ne sont pas transcrites - seul l'enonce actionnable est
retenu. Les 2 echelles d'evaluation nommees dans le texte (TEAM, ANTS,
Tableaux 2-3) sont mentionnees par leur nom dans R2.11 sans reproduction
integrale des grilles (non essentiel a la comprehension de la
recommandation elle-meme). Composition nominative des experts (page 2,
non reproduite) - non actionnable cliniquement.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from style import *
GRADE_COLORS["AF"] = (GREEN, WHITE)
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.units import mm

OUT = "/home/user/rfe-sfar-website/output/Fiche_SRLF_SFAR_SFMU_SOFRASIMS_Simulation_Soins_Critiques_2019.pdf"

SOURCE_TXT = ("Source : SRLF/SFAR/SFMU/SOFRASIMS, « Intérêts de l'apprentissage par simulation "
              "en soins critiques », RPP, textes validés par les CA respectifs "
              "(déc. 2018 - janv. 2019). Fiche de synthèse non officielle : se référer au texte "
              "intégral.")

def P(txt, style=S_CELL):
    return Paragraph(txt, style)

def chip(label, **kw):
    return grade_chip(label, **kw)

CW_FULL = PAGE_W - 2 * MARGIN

def reco_table(rows, col_widths):
    """rows: (ref, text, grade_label)."""
    data = [[P("Réf.", S_HEAD_W), P("Recommandation", S_HEAD_W), P("Cotation", S_HEAD_W_C)]]
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

def legend_flowable():
    chip_w = 17 * mm
    content_w = CW_FULL
    row = Table([[chip("AF", width=chip_w - 2 * mm),
                  P("<b>AF = Accord Fort</b> — cotation GRADE grid (≥ 70 % d'opinions "
                    "favorables, &lt; 20 % d'opinions contraires). <b>Les 24 recommandations "
                    "ont toutes recueilli un accord fort</b>, sans exception (aucune à accord "
                    "faible). Terminologie RPP : « les experts suggèrent de faire/ne pas "
                    "faire » — pas de grade GRADE numérique par item (méthode GRADE utilisée "
                    "seulement pour l'analyse de la littérature en amont).", S_BADGE_HEAD)]],
                colWidths=[chip_w, content_w - chip_w])
    row.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                              ("LEFTPADDING", (0, 0), (-1, -1), 1),
                              ("RIGHTPADDING", (0, 0), (-1, -1), 1),
                              ("TOPPADDING", (0, 0), (-1, -1), 0),
                              ("BOTTOMPADDING", (0, 0), (-1, -1), 0)]))
    return row

TOTAL_PAGES = {"n": 4}

def on_page(canvas, doc, page_title):
    header_band(canvas, doc, "SRLF / SFAR / SFMU / SOFRASIMS — RECOMMANDATIONS PPP, 2019",
                "Intérêts de l'apprentissage par simulation en soins critiques",
                page_title, icon_fn=lambda c, x, y: icon_shield(c, x, y, 13 * mm), color=TEAL_DARK)
    footer_band(canvas, doc, SOURCE_TXT, f"Page {doc.page} / {TOTAL_PAGES['n']}")

# ---------------------------------------------------------------------------
def _section_intro():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Résumé :</b> RPP commune SRLF/SFAR/SFMU/SOFRASIMS sur l'intérêt de la simulation "
        "en soins critiques (anesthésie-réanimation, réanimation, médecine d'urgence) — "
        "24 recommandations réparties en 3 champs : compétences techniques (10), "
        "compétences non techniques (12), situations sanitaires exceptionnelles (2). "
        "Simulation « basse fidélité » (mannequins/simulateurs simples, faible réalisme) vs "
        "« haute fidélité » (simulateurs avancés, immersion réaliste) — les deux ont leur "
        "place selon l'objectif pédagogique.", S_BODY), bg=BG_PANEL, border=TEAL_DARK))
    story.append(Spacer(1, 2.5 * mm))
    story.append(legend_flowable())
    story.append(Spacer(1, 3 * mm))
    story.append(KeepTogether([
        section_bar("Champ 1 — Compétences techniques en soins critiques"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("R1.1", "Utiliser la simulation pour l'apprentissage des gestes techniques en "
         "formation initiale, afin d'en améliorer l'acquisition.", "AF"),
        ("R1.2", "Utiliser la simulation pour maintenir la compétence des professionnels en "
         "exercice en formation continue, ou lors de l'introduction de nouvelles techniques "
         "ou matériels.", "AF"),
        ("R1.3", "Utiliser préférentiellement la simulation basse fidélité, plutôt que haute "
         "fidélité, pour l'apprentissage des gestes techniques.", "AF"),
        ("R1.4", "Évaluer systématiquement l'impact de la simulation sur l'apprentissage des "
         "apprenants à l'aide d'indicateurs spécifiques.", "AF"),
        ("R1.5", "Ne pas utiliser la simulation comme méthode pédagogique unique, sans "
         "intégration à un curriculum de formation.", "AF"),
    ], RCW))
    return story

# ---------------------------------------------------------------------------
def _section_champ1_suite():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(reco_table([
        ("R1.6", "Adapter la liste de compétences techniques enseignées par simulation en "
         "formation initiale aux conditions spécifiques d'exercice, en respectant les "
         "obligations réglementaires.", "AF"),
        ("R1.7", "Utiliser la simulation pour l'apprentissage de la gestion des voies "
         "aériennes en formation initiale, pour améliorer l'apprentissage du geste et la "
         "performance lors de sa réalisation sur les patients.", "AF"),
        ("R1.8", "Utiliser la simulation pour l'apprentissage de la pose des cathéters "
         "veineux centraux, pour améliorer la confiance et les connaissances des apprenants "
         "et les pratiques professionnelles/soins apportés aux patients.", "AF"),
        ("R1.9", "Utiliser la simulation basse fidélité pour l'apprentissage en formation "
         "initiale du cathétérisme artériel, pour améliorer la performance et réduire les "
         "complications chez les patients.", "AF"),
        ("R1.10", "Utiliser la simulation pour la formation initiale à la pose d'un drain "
         "pleural, pour améliorer la confiance et la performance des apprenants et réduire "
         "le taux de complications.", "AF"),
    ], RCW))
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Champ 2 — Compétences non techniques en soins critiques"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("R2.1", "Utiliser la simulation pour mieux développer et structurer l'apprentissage "
         "des compétences non techniques lors de l'intégration des novices médicaux et "
         "paramédicaux.", "AF"),
        ("R2.2", "Utiliser la simulation haute fidélité pour développer les compétences non "
         "techniques en soins critiques, en formation initiale et continue.", "AF"),
        ("R2.3", "Utiliser la simulation haute fidélité pour améliorer le travail en équipe "
         "pluri-professionnel dans la gestion de crises en soins critiques.", "AF"),
        ("R2.4", "Utiliser la simulation pour améliorer les compétences en communication "
         "entre professionnels en soins critiques, en formation initiale et continue, "
         "médicale et paramédicale.", "AF"),
        ("R2.5", "Utiliser la simulation pour développer les compétences en communication "
         "avec les patients et leurs proches, en formation initiale et continue.", "AF"),
    ], RCW))
    return story

# ---------------------------------------------------------------------------
def _section_champ2_suite():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(reco_table([
        ("R2.6", "Utiliser la simulation afin d'évaluer les connaissances antérieures et "
         "corriger les erreurs cognitives des apprenants en soins critiques.", "AF"),
        ("R2.7", "Utiliser la simulation afin d'améliorer la conscience de la situation en "
         "soins critiques, en formation initiale et continue, médicale et paramédicale.",
         "AF"),
        ("R2.8", "Utiliser la simulation afin d'améliorer la résolution de problème et la "
         "prise de décision en soins critiques, en formation initiale et continue "
         "médicale.", "AF"),
        ("R2.9", "Utiliser la simulation afin de développer les compétences relationnelles "
         "(notamment gestion des désaccords et conflits) pour les médicaux et "
         "paramédicaux.", "AF"),
        ("R2.10", "Utiliser la simulation pluri-professionnelle ou inter-professionnelle "
         "pour développer les compétences non techniques en soins critiques.", "AF"),
        ("R2.11", "Utiliser des outils d'évaluation spécifique du travail d'équipe (ex. "
         "échelles TEAM, ANTS) lors des formations par simulation centrées sur les "
         "compétences non techniques, pour améliorer la performance des équipes.", "AF"),
        ("R2.12", "Faire un débriefing afin d'améliorer l'apprentissage par simulation des "
         "compétences non techniques en soins critiques.", "AF"),
    ], RCW))
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Champ 3 — Situations sanitaires exceptionnelles"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("R3.1", "Utiliser la simulation pour acquérir les compétences nécessaires à la "
         "prise en charge des situations sanitaires exceptionnelles, sans qu'un outil "
         "particulier puisse être privilégié.", "AF"),
        ("R3.2", "Utiliser la simulation afin d'améliorer la confiance et les connaissances "
         "des apprenants en formation initiale, et d'améliorer les pratiques "
         "professionnelles pour le tri des victimes lors de situations sanitaires "
         "exceptionnelles.", "AF"),
    ], RCW))
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("Sources et avertissement"))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "SRLF/SFAR/SFMU/SOFRASIMS, « Intérêts de l'apprentissage par simulation en soins "
        "critiques », RPP, textes validés par les CA de la SRLF (20/12/2018), de la SFAR "
        "(10/01/2019), de la SFMU (16/01/2019) et de la SOFRASIMS (18/01/2019). Méthode "
        "GRADE (analyse de la littérature) + cotation GRADE grid. ~150 références "
        "bibliographiques citées dans le texte intégral (non reproduites ici).", S_SOURCE))
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Avertissement :</b> cette fiche est une synthèse indépendante, produite pour un "
        "usage d'aide-mémoire. Elle reprend intégralement les 24 recommandations du texte "
        "source mais condense l'argumentaire de chaque item (études citées) et omet la "
        "composition nominative du groupe d'experts ainsi que les grilles détaillées des "
        "outils d'évaluation (TEAM, ANTS). Elle ne remplace pas le texte intégral et n'est "
        "ni éditée ni validée par les sociétés savantes concernées.", S_BODY_SM),
        bg=GREY_LIGHT, border=GREY))
    return story

# ---------------------------------------------------------------------------
def _section_all():
    story = _section_intro()
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_champ1_suite())
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_champ2_suite())
    return story

SECTIONS = [
    ("Intérêts de l'apprentissage par simulation en soins critiques", _section_all),
]

def _make_doc(path=None):
    return SimpleDocTemplate(path or OUT, pagesize=A4,
                              leftMargin=MARGIN, rightMargin=MARGIN,
                              topMargin=32 * mm, bottomMargin=16 * mm,
                              title="Fiche RPP 2019 - Interets de la simulation en soins critiques",
                              author="Synthèse indépendante (source SRLF/SFAR/SFMU/SOFRASIMS)")

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
