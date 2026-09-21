# -*- coding: utf-8 -*-
"""
Fiche de synthese - "Optimisation hemodynamique perioperatoire - Adulte
dont obstetrique" - Recommandations Formalisees d'Experts (RFE) SFAR,
janvier 2024. 55 pages, telecharge depuis sfar.org (wpdmdl=62044).
Reactualisation des recommandations SFAR de 2012 sur le remplissage
vasculaire perioperatoire (cf. fiche_remplissage_perioperatoire.py).

METHODOLOGIE : methode GRADE (analyse de la litterature, format PICO), y
compris pour les questions obstetricales (prefixees "OBS" dans le texte
source - meme methodologie, meme comite d'experts, sous-section dediee
pour les patientes en cesarienne programmee sous rachianesthesie).

DISCLOSURE - decompte du resume ("24 recommandations") vs decompte direct
: l'extraction integrale des items numerotes trouve 18 recommandations
reelles (2 GRADE1 [OBS R.4.1, OBS R.4.2] + 8 GRADE2 [R1.1, OBS R.1.1,
R2.1.1, R2.1.2, R2.1.3, R3.2, R4.1, R5.1] + 8 avis d'experts [R1.2, OBS
R.1.2, R3.1, R4.2.1, R4.2.2, R4.3.1, R4.3.2, OBS R.4.4]) et 6 "ABSENCE DE
RECOMMANDATION" imprimees. Les sous-totaux "2 GRADE1" et "8 GRADE2" du
resume correspondent EXACTEMENT au decompte direct, de meme que "6
questions" sans reponse - mais le total annonce ("24 recommandations")
ne correspond a aucune interpretation stricte de "recommandation" (18
reelles, pas 24). 18 (recommandations reelles) + 6 (absences) = 24 :
l'hypothese la plus coherente est que le resume du texte source compte
les absences de recommandation comme des "recommandations formulees" au
sens large (24 questions ayant recu une reponse, positive ou d'absence),
plutot qu'une erreur de calcul isolee comme trouve ailleurs dans ce corpus
(fiches raac_orthopedique_2019, raac_lobectomie_pulmonaire_2019) - les
deux lectures sont disclosees, aucune n'est presentee comme certaine.

Contrairement au format GRADE standard de ce corpus (1+/1-/2+/2-), ce
document n'imprime que "GRADE 1" ou "GRADE 2" sans signe +/- : le sens
(favorable/defavorable a l'intervention) est repris ici du verbe de la
phrase elle-meme ("il est recommande" vs "il n'est pas recommande"),
jamais invente. Chips locaux "G1"/"G2"/"AE" utilises pour refleter
fidelement cette absence de signe dans le texte source (au lieu des chips
1+/1-/2+/2- standards de ce corpus, qui impliqueraient un signe non
imprime ici).

PERIMETRE : integral sur les 5 champs (pression arterielle y compris
obstetrique, VES/indices dynamiques, indices de perfusion tissulaire,
expansion volemique/vasoconstricteurs/inotropes y compris obstetrique,
impact economique) et les 6 absences de recommandation. Argumentaire
minimal (regle 2026-09-14). Complementaire, non redondant, de
`fiche_remplissage_perioperatoire.py` (RFE SFAR/Adarpef 2012, deja
git-tracked - celle-ci est la reactualisation 2024 explicitement annoncee
par le texte source lui-meme). Bibliographie et composition nominative
du groupe d'experts (non reproduites) - non actionnable cliniquement.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from style import *
GRADE_COLORS["G1"] = (GREEN, WHITE)
GRADE_COLORS["G2"] = (TEAL, WHITE)
GRADE_COLORS["AE"] = (GREY, WHITE)
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.units import mm

OUT = "/home/user/rfe-sfar-website/output/Fiche_SFAR_Optimisation_Hemodynamique_Adulte_Obstetrique_2024.pdf"

SOURCE_TXT = ("Source : SFAR, « Optimisation hémodynamique périopératoire – Adulte dont "
              "obstétrique », RFE, janvier 2024. Fiche de synthèse non officielle : se référer "
              "au texte intégral.")

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

RCW = [16 * mm, CW_FULL - 16 * mm - 15 * mm, 15 * mm]

def bullets(items, style=S_BODY_SM):
    html = "&bull; " + "<br/>&bull; ".join(items)
    return P(html, style)

def absence_note(question_txt):
    return info_panel(P(
        f"<b>Absence de recommandation</b> (données insuffisantes) : {question_txt}",
        S_BODY_SM), bg=GREY_LIGHT, border=GREY)

def legend_flowable():
    chip_w = 15 * mm
    content_w = CW_FULL
    row = Table([[chip("G1", width=chip_w - 2 * mm), chip("G2", width=chip_w - 2 * mm),
                  chip("AE", width=chip_w - 2 * mm),
                  P("<b>G1/G2 = GRADE 1/GRADE 2</b> — le texte source imprime ces niveaux "
                    "SANS signe +/- (contrairement au format standard de ce corpus) ; le sens "
                    "favorable/défavorable de chaque item reste dans le verbe de la phrase "
                    "elle-même. <b>AE</b> = avis d'experts. Toutes les recommandations sont "
                    "à accord fort. ⚠ Le résumé du texte source annonce « 24 "
                    "recommandations » mais un décompte direct trouve 18 recommandations "
                    "réelles (2×G1 + 8×G2 + 8×AE, ces 3 sous-totaux correspondant "
                    "exactement au résumé) + 6 absences de recommandation — 18+6=24, "
                    "disclosed sans résolution certaine.", S_BADGE_HEAD)]],
                colWidths=[chip_w] * 3 + [content_w - 3 * chip_w])
    row.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                              ("LEFTPADDING", (0, 0), (-1, -1), 1),
                              ("RIGHTPADDING", (0, 0), (-1, -1), 1),
                              ("TOPPADDING", (0, 0), (-1, -1), 0),
                              ("BOTTOMPADDING", (0, 0), (-1, -1), 0)]))
    return row

TOTAL_PAGES = {"n": 4}

def on_page(canvas, doc, page_title):
    header_band(canvas, doc, "SFAR — RECOMMANDATIONS FORMALISÉES D'EXPERTS, 2024",
                "Optimisation hémodynamique périopératoire — Adulte / Obstétrique",
                page_title, icon_fn=lambda c, x, y: icon_drop(c, x, y, 13 * mm), color=TEAL_DARK)
    footer_band(canvas, doc, SOURCE_TXT, f"Page {doc.page} / {TOTAL_PAGES['n']}")

# ---------------------------------------------------------------------------
def _section_intro_champ1():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Résumé :</b> réactualisation 2024 des recommandations SFAR 2012 sur le "
        "remplissage vasculaire périopératoire — 18 recommandations (dont 4 spécifiques à "
        "la césarienne programmée sous rachianesthésie, préfixées OBS) et 6 absences de "
        "recommandation, sur 5 champs : pression artérielle, VES/indices dynamiques, "
        "indices de perfusion tissulaire, expansion volémique/vasoconstricteurs/"
        "inotropes, impact économique.", S_BODY), bg=BG_PANEL, border=TEAL_DARK))
    story.append(Spacer(1, 2.5 * mm))
    story.append(legend_flowable())
    story.append(Spacer(1, 3 * mm))
    story.append(KeepTogether([
        section_bar("Champ 1 — Optimisation périopératoire de la pression artérielle"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("R1.1", "Éviter un niveau de PA moyenne (PAM) peropératoire &lt; 60-70 mmHg chez "
         "le patient non hypertendu chronique, pour diminuer la morbimortalité "
         "postopératoire.", "G2"),
        ("R1.2", "Chez les patients hypertendus chroniques, cibler une PAM &gt; 90 % de sa "
         "valeur habituelle ou &gt; 70 mmHg, pour diminuer la morbi-mortalité.", "AE"),
    ], RCW))
    story.append(Spacer(1, 2 * mm))
    story.append(absence_note(
        "impact du monitorage continu de la pression artérielle sur la morbi-mortalité "
        "périopératoire chez les patients à risque faible à intermédiaire."))
    story.append(Spacer(1, 2 * mm))
    story.append(P("<b>OBS — Césarienne programmée sous rachianesthésie</b>", S_CELL_B))
    story.append(Spacer(1, 1 * mm))
    story.append(reco_table([
        ("OBS R1.1", "Maintenir la PA systolique maternelle entre 90 et 100 % de la PAS "
         "mesurée avant l'induction de la rachianesthésie, pour réduire l'incidence des "
         "nausées-vomissements.", "G2"),
        ("OBS R1.2", "Si la PAS est &lt; 80 % de la PAS de base, traiter l'hypotension "
         "sans délai, pour réduire l'incidence de l'acidose néonatale.", "AE"),
    ], RCW))
    return story

# ---------------------------------------------------------------------------
def _section_champ2_3():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Champ 2 — VES et indices dynamiques pour l'expansion volémique"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("R2.1.1", "Utiliser un monitorage du VES (Doppler œsophagien ou analyse de la "
         "courbe de PA via cathéter artériel) pour diminuer la morbidité périopératoire "
         "chez les patients à risque élevé et très élevé.", "G2"),
        ("R2.1.2", "En cas de monitorage du VES par analyse de la courbe de PA, associer "
         "un indice dynamique (VPP ou VVE) pour optimiser l'expansion volémique chez ces "
         "mêmes patients.", "G2"),
    ], RCW))
    story.append(Spacer(1, 2 * mm))
    story.append(absence_note(
        "utilisation d'un indice dynamique seul pour diminuer la morbidité périopératoire "
        "chez les patients à risque élevé ou très élevé."))
    story.append(Spacer(1, 2 * mm))
    story.append(reco_table([
        ("R2.1.3", "Ne pas utiliser de monitorage du VES ou d'indice dynamique (ou leur "
         "association) chez les patients à risque faible ou intermédiaire.", "G2"),
    ], RCW))
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Champ 3 — Indices de perfusion tissulaire"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("R3.1", "Chez les patients à risque très élevé, intégrer le dosage du lactate "
         "artériel dans le schéma d'optimisation hémodynamique.", "AE"),
        ("R3.2", "Ne pas utiliser le monitorage de la saturation veineuse centrale en "
         "oxygène (ScVO2) pour diminuer la morbi-mortalité périopératoire.", "G2"),
    ], RCW))
    story.append(Spacer(1, 2 * mm))
    story.append(absence_note(
        "impact du monitorage de la différence artério-veineuse en CO2 (DIVA-CO2) sur la "
        "morbi-mortalité périopératoire."))
    story.append(Spacer(1, 2 * mm))
    story.append(absence_note(
        "utilisation du monitorage de la perfusion/oxygénation tissulaire par "
        "spectrométrie proche infrarouge (NIRS) en chirurgie non cardiaque adulte."))
    return story

# ---------------------------------------------------------------------------
def _section_champ4():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Champ 4 — Expansion volémique, vasoconstricteurs, inotropes"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("R4.1", "Utiliser des solutés cristalloïdes balancés pour l'expansion volémique "
         "en chirurgie non cardiaque, pour préserver l'équilibre acido-basique.", "G2"),
        ("R4.2.1", "Dans un protocole d'optimisation hémodynamique, lorsque le VES a déjà "
         "été optimisé par expansion volémique, utiliser un vasoconstricteur pour "
         "diminuer la morbi-mortalité périopératoire.", "AE"),
        ("R4.2.2", "Lorsqu'un vasoconstricteur est nécessaire, privilégier la "
         "noradrénaline à la phényléphrine pour un meilleur maintien du débit cardiaque.",
         "AE"),
        ("R4.3.1", "En cas de persistance d'un index cardiaque inadapté après "
         "optimisation du VES et de la PA par vasoconstricteurs, utiliser un inotrope.",
         "AE"),
        ("R4.3.2", "Si un inotrope est utilisé pour index cardiaque inadapté, utiliser la "
         "dobutamine en 1ère intention.", "AE"),
    ], RCW))
    story.append(Spacer(1, 2 * mm))
    story.append(P("<b>OBS — Césarienne programmée sous rachianesthésie</b>", S_CELL_B))
    story.append(Spacer(1, 1 * mm))
    story.append(reco_table([
        ("OBS R4.1", "Ne pas utiliser l'éphédrine en traitement prophylactique (vs "
         "phényléphrine ou noradrénaline), pour réduire acidose néonatale, hypotension, "
         "nausées-vomissements et tachycardie maternelle.", "G1"),
        ("OBS R4.2", "Utiliser la phényléphrine ou la noradrénaline faiblement concentrée "
         "en traitement prophylactique, pour réduire hypotension, nausées-vomissements, "
         "tachycardie et lactatémie artérielle néonatale.", "G1"),
    ], RCW))
    story.append(Spacer(1, 2 * mm))
    story.append(absence_note(
        "préférence entre noradrénaline et phényléphrine comme vasoconstricteur "
        "prophylactique — données actuelles insuffisantes."))
    story.append(Spacer(1, 2 * mm))
    story.append(reco_table([
        ("OBS R4.4", "Conjointement à la phényléphrine/noradrénaline prophylactique, "
         "utiliser une expansion volémique rapide par cristalloïdes dès l'induction de la "
         "rachianesthésie (co-remplissage), pour réduire l'hypotension et les besoins en "
         "vasoconstricteurs.", "AE"),
    ], RCW))
    return story

# ---------------------------------------------------------------------------
def _section_champ5_sources():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Champ 5 — Impact économique de l'optimisation hémodynamique"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("R5.1", "Chez le patient à risque élevé et très élevé, optimiser l'hémodynamique "
         "pour diminuer la durée moyenne de séjour.", "G2"),
    ], RCW))
    story.append(Spacer(1, 2 * mm))
    story.append(absence_note(
        "impact de l'optimisation hémodynamique périopératoire sur les coûts liés aux "
        "soins."))
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("Sources et avertissement"))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "SFAR, « Optimisation hémodynamique périopératoire – Adulte dont obstétrique », "
        "RFE, janvier 2024 — réactualisation des recommandations SFAR de 2012. Méthode "
        "GRADE (analyse de la littérature, format PICO). Références bibliographiques par "
        "question et composition nominative du groupe d'experts (non reproduites ici).",
        S_SOURCE))
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Avertissement :</b> cette fiche est une synthèse indépendante, produite pour un "
        "usage d'aide-mémoire. Elle reprend intégralement les 18 recommandations réelles "
        "et les 6 cas d'absence de recommandation du texte source, mais condense "
        "l'argumentaire de chaque item et omet la composition nominative du groupe "
        "d'experts. Elle ne remplace pas le texte intégral et n'est ni éditée ni validée "
        "par la SFAR.", S_BODY_SM), bg=GREY_LIGHT, border=GREY))
    return story

# ---------------------------------------------------------------------------
def _section_all():
    story = _section_intro_champ1()
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_champ2_3())
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_champ4())
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_champ5_sources())
    return story

SECTIONS = [
    ("Optimisation hémodynamique périopératoire — Adulte / Obstétrique", _section_all),
]

def _make_doc(path=None):
    return SimpleDocTemplate(path or OUT, pagesize=A4,
                              leftMargin=MARGIN, rightMargin=MARGIN,
                              topMargin=32 * mm, bottomMargin=16 * mm,
                              title="Fiche SFAR 2024 - Optimisation hemodynamique perioperatoire adulte",
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
