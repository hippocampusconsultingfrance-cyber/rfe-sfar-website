# -*- coding: utf-8 -*-
"""
Fiche de synthese - "Optimisation du traitement par Beta-Lactamines chez le
patient de soins critiques" - Recommandations de Pratiques Professionnelles
(RPP) communes SFPT (Groupe Suivi Therapeutique Pharmacologique et
Personnalisation des Traitements) / SFAR, 2018. 41 pages, telecharge
depuis sfar.org (wp-content/uploads/2018/09/RPP_beta-lactamines-en-soins-
critiques_041018_logoSFPT.pdf).

METHODOLOGIE : methode GRADE pour l'analyse de la litterature (PRISMA,
format PICO) mais format RPP retenu en amont (peu d'etudes a critere de
jugement fort type mortalite), terminologie "les experts suggerent de
faire/ne pas faire", cotation GRADE grid (>=70% d'opinions favorables,
<20% contraires). Synthese du texte source : "21 recommandations et un
schema recapitulatif... un accord fort a ete obtenu pour l'ensemble des
recommandations et pour le schema" - decompte verifie exact : les items
numerotes a 3 niveaux (ex. R1.2.1/R1.2.2, R4.7.1/R4.7.2, R4.8.1/R4.8.2/
R4.8.3) sont des sous-methodes d'UNE recommandation-parent (R1.2, R4.7,
R4.8) pour le decompte officiel de 21, mais chaque sous-item est cote et
transcrit individuellement ici (26 lignes au total) - jamais fusionne,
tous a "Accord fort" uniforme (aucune exception, verifie par lecture
complete du texte source).

RELATION AVEC LA FICHE EXISTANTE `reduction_antibiotiques_reanimation_2014`
(SRLF/SFAR 2014) : cette derniere contient deja des recommandations
generales sur le dosage/TDM et la perfusion continue des beta-lactamines
(Q4b/Q4c), mais de facon large et non specifique a une molecule. Ce
document-ci (SFPT/SFAR 2018, posterieur) est un RPP dedie et beaucoup plus
detaille specifiquement aux beta-lactamines : cibles PK-PD par molecule
(Tableau 1, 11 molecules), modalites precises d'ajustement post-dosage,
methode chromatographique de reference. Complementaire, pas redondant -
verifie par lecture des deux textes, aucune recommandation dupliquee a
l'identique.

PERIMETRE : integral sur les 4 champs (variabilite pharmacocinetique,
relation PK-PD, modalites d'administration, suivi therapeutique
pharmacologique/TDM) et le Tableau 1 (cibles therapeutiques par molecule,
11 beta-lactamines, reproduit integralement - colonnes condensees a
l'essentiel clinique : fraction libre, cible en infection documentee, CMI
seuil consideree ; la colonne "infection non documentee" et les notes de
bas de tableau tres detaillees ne sont pas toutes reproduites, renvoi au
texte integral). Argumentaire minimal (regle 2026-09-14) : les etudes
citees a l'appui de chaque recommandation ne sont pas transcrites - seul
l'enonce actionnable est retenu. Composition nominative des groupes
d'experts/lecture (page 1, non reproduite) - non actionnable cliniquement.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from style import *
GRADE_COLORS["AF"] = (GREEN, WHITE)
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.units import mm

OUT = "/home/user/rfe-sfar-website/output/Fiche_SFPT_SFAR_Optimisation_Beta_Lactamines_Soins_Critiques_2018.pdf"

SOURCE_TXT = ("Source : SFPT (Groupe STP/PT) / SFAR, « Optimisation du traitement par "
              "bêta-lactamines chez le patient de soins critiques », RPP, 2018. Fiche de "
              "synthèse non officielle : se référer au texte intégral.")

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

RCW = [16 * mm, CW_FULL - 16 * mm - 16 * mm, 16 * mm]

def grid_table(head, rows, col_widths, center_cols=()):
    data = [[P(h, S_HEAD_W_C if i in center_cols or i == 0 else S_HEAD_W) for i, h in enumerate(head)]]
    for r in rows:
        row = []
        for i, cell in enumerate(r):
            style = S_CELL_C if i in center_cols else (S_CELL_B if i == 0 else S_CELL)
            row.append(P(cell, style))
        data.append(row)
    t = Table(data, colWidths=col_widths, repeatRows=1)
    style_cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), NAVY), ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTNAME", (0, 0), (-1, 0), FONT_BOLD), ("FONTSIZE", (0, 0), (-1, 0), 7.6),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("GRID", (0, 0), (-1, -1), 0.5, GREY_LIGHT),
        ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING", (0, 0), (-1, -1), 4), ("RIGHTPADDING", (0, 0), (-1, -1), 4),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            style_cmds.append(("BACKGROUND", (0, i), (-1, i), BG_PANEL))
    t.setStyle(TableStyle(style_cmds))
    return t

def bullets(items, style=S_BODY_SM):
    html = "&bull; " + "<br/>&bull; ".join(items)
    return P(html, style)

def legend_flowable():
    chip_w = 17 * mm
    content_w = CW_FULL
    row = Table([[chip("AF", width=chip_w - 2 * mm),
                  P("<b>AF = Accord Fort</b> — cotation GRADE grid (≥ 70 % d'opinions "
                    "favorables, &lt; 20 % contraires). <b>Les 21 recommandations (26 "
                    "sous-items cotés) ont toutes recueilli un accord fort</b>, sans "
                    "exception. Terminologie RPP : « les experts suggèrent de faire/ne pas "
                    "faire » — pas de grade GRADE numérique par item (méthode GRADE "
                    "utilisée pour l'analyse de la littérature en amont).", S_BADGE_HEAD)]],
                colWidths=[chip_w, content_w - chip_w])
    row.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                              ("LEFTPADDING", (0, 0), (-1, -1), 1),
                              ("RIGHTPADDING", (0, 0), (-1, -1), 1),
                              ("TOPPADDING", (0, 0), (-1, -1), 0),
                              ("BOTTOMPADDING", (0, 0), (-1, -1), 0)]))
    return row

TOTAL_PAGES = {"n": 5}

def on_page(canvas, doc, page_title):
    header_band(canvas, doc, "SFPT / SFAR — RECOMMANDATIONS DE PRATIQUES PROFESSIONNELLES, 2018",
                "Optimisation du traitement par bêta-lactamines en soins critiques",
                page_title, icon_fn=lambda c, x, y: icon_pill(c, x, y, 13 * mm), color=TEAL_DARK)
    footer_band(canvas, doc, SOURCE_TXT, f"Page {doc.page} / {TOTAL_PAGES['n']}")

# ---------------------------------------------------------------------------
def _section_intro_champ1():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Résumé :</b> RPP commune SFPT/SFAR sur l'optimisation du traitement par "
        "bêta-lactamines (posologie, modalités d'administration, suivi thérapeutique "
        "pharmacologique) chez le patient de soins critiques — 21 recommandations sur 4 "
        "champs : variabilité pharmacocinétique, relation PK-PD, modalités "
        "d'administration, suivi thérapeutique pharmacologique (TDM). Complémentaire de "
        "la fiche « Réduction de l'utilisation des antibiotiques en réanimation » "
        "(SRLF/SFAR 2014, recommandations générales) — celle-ci détaille spécifiquement "
        "les cibles PK-PD par molécule.", S_BODY), bg=BG_PANEL, border=TEAL_DARK))
    story.append(Spacer(1, 2.5 * mm))
    story.append(legend_flowable())
    story.append(Spacer(1, 3 * mm))
    story.append(KeepTogether([
        section_bar("Champ 1 — Variabilité pharmacocinétique"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("R1.1", "Tenir systématiquement et quotidiennement compte des nombreuses sources "
         "de variabilité pharmacocinétique lors de la prescription de bêta-lactamines.",
         "AF"),
        ("R1.2.1", "Estimer le débit de filtration glomérulaire par le calcul de la "
         "clairance de la créatinine (formule UxV/P) au début du traitement et lors de "
         "toute modification significative de l'état clinique/fonction rénale.", "AF"),
        ("R1.2.2", "Estimer le DFG (clairance créatinine, formule UxV/P) lors de la "
         "réalisation d'un dosage des bêta-lactamines, pour aider à l'interprétation du "
         "résultat.", "AF"),
        ("R1.3", "Effectuer un suivi thérapeutique pharmacologique des bêta-lactamines "
         "chez les patients traités par épuration extra-rénale.", "AF"),
        ("R1.4.1", "Doser l'albuminémie (à défaut la protidémie) au moins une fois au "
         "début du traitement, pour évaluer le degré d'hypoalbuminémie et guider la "
         "prescription.", "AF"),
        ("R1.4.2", "Doser l'albuminémie (à défaut la protidémie) lors de la réalisation "
         "d'un dosage des bêta-lactamines, pour aider à l'interprétation du résultat.",
         "AF"),
        ("R1.5", "Dans l'attente du résultat du suivi thérapeutique, administrer à "
         "l'initiation une posologie journalière plus élevée que hors soins critiques, a "
         "fortiori chez les patients les plus graves à fonction rénale conservée.", "AF"),
    ], RCW))
    return story

# ---------------------------------------------------------------------------
def _section_champ2_3():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Champ 2 — Relation pharmacocinétique-pharmacodynamique (PK-PD)"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("R2.1", "Considérer le paramètre PK-PD %fT &gt; k×CMI (temps pendant lequel la "
         "concentration plasmatique libre dépasse un multiple de la CMI) comme cible "
         "thérapeutique des bêta-lactamines.", "AF"),
        ("R2.2", "Cibler une concentration plasmatique libre entre 4 et 8 fois la CMI "
         "pendant 100 % de l'intervalle de dose (%fT ≥ 4-8×CMI à 100 %) pour optimiser les "
         "chances de guérison clinique dans les infections graves.", "AF"),
        ("R2.3", "Pour les molécules sans seuil toxique validé, il est inutile voire "
         "dangereux de dépasser une concentration plasmatique &gt; 8 fois la CMI de la "
         "bactérie incriminée.", "AF"),
    ], RCW))
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Champ 3 — Modalités d'administration"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("R3.1", "Administrer les bêta-lactamines en perfusion prolongée ou continue en "
         "cas de CMI élevée de la bactérie responsable, pour augmenter les chances "
         "d'atteindre l'objectif PK-PD.", "AF"),
        ("R3.2", "Administrer les bêta-lactamines en perfusion prolongée ou continue chez "
         "les patients en état de choc et/ou à score de gravité élevé, pour améliorer le "
         "taux de guérison clinique.", "AF"),
        ("R3.3", "Administrer les bêta-lactamines en perfusion prolongée ou continue chez "
         "les patients avec infection respiratoire basse, pour améliorer le taux de "
         "guérison clinique.", "AF"),
        ("R3.4", "Administrer les bêta-lactamines en perfusion prolongée ou continue chez "
         "les patients ayant une infection à bacille à Gram négatif non-fermentant, pour "
         "améliorer le taux de guérison clinique.", "AF"),
        ("R3.5", "Précéder l'administration continue ou prolongée par une dose de charge "
         "en bolus intraveineux lent, au début du traitement.", "AF"),
    ], RCW))
    return story

# ---------------------------------------------------------------------------
def _section_champ4():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Champ 4 — Suivi thérapeutique pharmacologique (TDM)"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("R4.1", "Réaliser le suivi thérapeutique chez l'ensemble des patients pour "
         "lesquels une variabilité pharmacocinétique est attendue et/ou présentant des "
         "signes de toxicité aux bêta-lactamines.", "AF"),
        ("R4.2", "Réaliser le suivi par un dosage de la concentration résiduelle en cas "
         "d'administration discontinue, et un dosage à l'équilibre en cas d'administration "
         "continue.", "AF"),
        ("R4.3", "Réaliser le suivi thérapeutique 24-48h après l'initiation du traitement, "
         "après toute modification de posologie, et en cas de modification importante de "
         "l'état clinique.", "AF"),
        ("R4.4", "En cas d'infection neuro-méningée, réaliser si possible un dosage sur "
         "échantillons sanguin et de liquide cérébro-spinal prélevés de manière "
         "contemporaine.", "AF"),
        ("R4.5", "Réaliser le dosage selon une technique chromatographique validée, avec "
         "un rendu des résultats au clinicien le plus rapide possible.", "AF"),
        ("R4.6", "Considérer comme cibles thérapeutiques les concentrations plasmatiques "
         "du Tableau 1 (ci-dessous), par molécule.", "AF"),
        ("R4.7.1", "En cas de non-obtention de la concentration cible : en 1ère intention, "
         "augmenter la fréquence d'administration (fractionner la dose) ou passer en "
         "perfusion continue à dose journalière égale, ou augmenter la dose unitaire.",
         "AF"),
        ("R4.7.2", "En cas de persistance d'une concentration inférieure à la cible après "
         "ces mesures : passer à une administration continue/prolongée associée à une "
         "augmentation de dose.", "AF"),
        ("R4.8.1", "En cas de concentration supra-thérapeutique : diminuer en 1ère "
         "intention la dose unitaire discontinue de 25-50 % (fréquence conservée), ou "
         "diminuer la dose journalière si administration continue.", "AF"),
        ("R4.8.2", "En cas d'accumulation importante et/ou de signes évocateurs de "
         "toxicité compatibles avec un surdosage : suspendre l'administration, reprendre "
         "sous surveillance de la décroissance des concentrations.", "AF"),
        ("R4.8.3", "Envisager une épuration extra-rénale si une insuffisance rénale aiguë "
         "est au moins en partie à l'origine d'un surdosage symptomatique.", "AF"),
    ], RCW))
    story.append(Spacer(1, 2.5 * mm))
    story.append(P("<b>Tableau 1 — Cibles thérapeutiques par molécule (infection "
                    "documentée) :</b>", S_CELL_B))
    story.append(Spacer(1, 1 * mm))
    GCW = [30 * mm, 22 * mm, CW_FULL - 30 * mm - 22 * mm - 40 * mm, 40 * mm]
    story.append(grid_table(
        ["Molécule", "Fraction libre", "Cible visée (Cmin/Céq ≥ 4×CMI)", "CMI seuil retenue"],
        [
            ["Amoxicilline", "≈80 %", "40-80 mg/L", "8 mg/L (E. coli)"],
            ["Céfazoline", "≈15-20 %", "40-80 mg/L", "2 mg/L (S. aureus)"],
            ["Céfépime", "80 %", "5-20 mg/L (Cmin) / 5-35 mg/L (Céq)", "1 mg/L (entérobactéries)"],
            ["Céfotaxime", "≈60-80 %", "25-60 mg/L", "4 mg/L (S. aureus)"],
            ["Ceftazidime", "≈90 %", "35-80 mg/L", "8 mg/L (P. aeruginosa)"],
            ["Ceftriaxone", "≈10 %", "20-100 mg/L (Cmin)", "0,5 mg/L (E. cloacae)"],
            ["Cloxacilline", "≈10 %", "20-50 mg/L", "0,5 mg/L (S. aureus)"],
            ["Ertapénème", "≈10 %", "5-10 mg/L (Cmin)", "0,125 mg/L (H. influenzae)"],
            ["Imipénème", "≈80 %", "2,5-5 mg/L (Cmin)", "0,5 mg/L (E. coli)"],
            ["Méropénème", "≈100 %", "8-16 mg/L", "2 mg/L (P. aeruginosa)"],
            ["Pipéracilline", "≈80 %", "80-160 mg/L (Céq)", "16 mg/L (P. aeruginosa)"],
        ], GCW))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "Cmin = concentration résiduelle (administration discontinue) ; Céq = concentration "
        "à l'équilibre (administration continue). Plage haute = seuil de toxicité à ne pas "
        "dépasser. Colonne « infection non documentée » et notes de bas de tableau détaillées "
        "non reproduites ici — se référer au texte intégral (Tableau 1).", S_NOTE))
    return story

# ---------------------------------------------------------------------------
def _section_sources():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("Sources et avertissement"))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "SFPT (Groupe STP/PT) / SFAR, « Optimisation du traitement par bêta-lactamines "
        "chez le patient de soins critiques », RPP, 2018. Méthode GRADE (analyse de la "
        "littérature, PRISMA, format PICO) + cotation GRADE grid. Références "
        "bibliographiques citées dans le texte intégral (non reproduites ici) ; "
        "composition nominative des groupes d'experts/lecture (non reproduite).", S_SOURCE))
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Avertissement :</b> cette fiche est une synthèse indépendante, produite pour un "
        "usage d'aide-mémoire. Elle reprend intégralement les 21 recommandations (26 "
        "sous-items) et le Tableau 1 des cibles par molécule (colonne « infection "
        "documentée »), mais condense l'argumentaire de chaque item, la colonne « infection "
        "non documentée » et les notes de bas de tableau détaillées, et omet la composition "
        "nominative des groupes d'experts. Elle ne remplace pas le texte intégral et n'est "
        "ni éditée ni validée par la SFPT/SFAR.", S_BODY_SM), bg=GREY_LIGHT, border=GREY))
    return story

# ---------------------------------------------------------------------------
def _section_all():
    story = _section_intro_champ1()
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_champ2_3())
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_champ4())
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_sources())
    return story

SECTIONS = [
    ("Optimisation du traitement par bêta-lactamines en soins critiques", _section_all),
]

def _make_doc(path=None):
    return SimpleDocTemplate(path or OUT, pagesize=A4,
                              leftMargin=MARGIN, rightMargin=MARGIN,
                              topMargin=32 * mm, bottomMargin=16 * mm,
                              title="Fiche SFPT-SFAR 2018 - Optimisation beta-lactamines soins critiques",
                              author="Synthèse indépendante (source SFPT/SFAR)")

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
