# -*- coding: utf-8 -*-
"""
Fiche de synthese - "Prevention des erreurs medicamenteuses en
anesthesie-reanimation" - Recommandations pour la Pratique Professionnelle
(RPP), SFAR en collaboration avec la Societe Francaise de Pharmacie
Clinique (SFPC), texte valide par le Comite des Referentiels Cliniques de
la SFAR le 30 avril 2024. 66 pages, telecharge depuis sfar.org
(wpdmdl=68460).

RELATION AVEC UN DOCUMENT DEJA GIT-TRACKE : ce corpus tracke deja
`erreurs_medicamenteuses_ar_2016` (SFAR/SFPC, preconisation, novembre
2016, meme sujet). Ce document-ci (2024) est une reactualisation
explicitement plus recente et beaucoup plus etendue (29 recommandations
sur 4 champs vs le format "preconisation" 2016) - complementaire, non
redondant, garde sous une cle distincte (comme
optimisation_hemodynamique_adulte_2024 vis-a-vis de
remplissage_perioperatoire, ou resection_hepatique_2025 vis-a-vis
d'aucun equivalent). Les deux fiches restent utiles : celle-ci pour le
detail 2024 (logiciels de prescription, SPR, connectique, pharmaciens
cliniciens, pénuries), l'autre pour le contexte historique 2016.

METHODOLOGIE : format RPP choisi en amont (pas RFE) "du fait de la tres
faible quantite d'etudes permettant de coter avec la methode GRADE" -
les 29 recommandations sont donc TOUTES des avis d'experts, a accord
fort pour la totalite d'entre elles (decompte source verifie exact :
methode GRADE grid utilisee seulement pour le VOTE, jamais imprimee
comme grade numerique par item - meme pattern que
fiche_facteurs_humains_2022.py). Chip unique "AE" + "ABS" pour les 2
absences de recommandation trouvees (imprimees en encadrement avant ET
apres le texte, motif deja rencontre sur les fiches HAS de ce corpus -
verifie ici sur chaque occurrence pour ne pas compter en double).

PERIMETRE : integral sur les 4 champs (environnement de travail et
processus ; facteurs humains et organisationnels ; gestion des risques a
posteriori ; problematique des penuries medicamenteuses), les 29
recommandations et les 2 absences de recommandation (informatisation de
la prescription en anesthesie [distincte de R1.2.1-1.2.3, specifiques
aux soins critiques] ; systemes data-matrix et RFID [distincts de R1.10,
traçabilite par code barre]). Aucune annexe dans le document source.
Argumentaire minimal (regle de projet 2026-09-14) : les paragraphes de
justification (etudes, registres d'erreurs, citations) ne sont pas
transcrits - seul l'enonce actionnable de chaque recommandation est
retenu. Bibliographie et composition nominative du groupe d'experts non
reproduites.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from style import *
GRADE_COLORS["AE"] = (GREY, WHITE)
GRADE_COLORS["ABS"] = (GREY_LIGHT, INK)
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.units import mm

OUT = "/home/user/rfe-sfar-website/output/Fiche_SFAR_SFPC_Erreurs_Medicamenteuses_2024.pdf"

SOURCE_TXT = ("Source : SFAR / Société Française de Pharmacie Clinique (SFPC), « Prévention "
              "des erreurs médicamenteuses en anesthésie-réanimation », RPP, 2024. Fiche de "
              "synthèse non officielle : se référer au texte intégral.")

def P(txt, style=S_CELL):
    return Paragraph(txt, style)

def chip(label, **kw):
    return grade_chip(label, **kw)

CW_FULL = PAGE_W - 2 * MARGIN

def reco_table(rows, col_widths):
    """rows: (ref, text, grade_label)."""
    data = [[P("Réf.", S_HEAD_W), P("Avis d'experts (accord fort)", S_HEAD_W), P("", S_HEAD_W_C)]]
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

def absence_note(question_txt):
    return info_panel(P(
        f"<b>ABS — Absence de recommandation</b> (données insuffisantes) : {question_txt}",
        S_BODY_SM), bg=GREY_LIGHT, border=GREY)

def legend_flowable():
    chip_w = 15 * mm
    content_w = CW_FULL
    row = Table([[chip("AE", width=chip_w - 2 * mm), chip("ABS", width=chip_w - 2 * mm),
                  P("<b>AE</b> = avis d'experts — format RPP choisi en amont (pas RFE) faute "
                    "d'un nombre suffisant d'études permettant une cotation GRADE numérique : "
                    "les 29 recommandations sont TOUTES des avis d'experts, à accord fort pour "
                    "100 % d'entre elles (décompte source vérifié exact). <b>ABS</b> = absence "
                    "de recommandation (données insuffisantes, aucune proposition faite).",
                    S_BADGE_HEAD)]],
                colWidths=[chip_w] * 2 + [content_w - 2 * chip_w])
    row.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                              ("LEFTPADDING", (0, 0), (-1, -1), 1),
                              ("RIGHTPADDING", (0, 0), (-1, -1), 1),
                              ("TOPPADDING", (0, 0), (-1, -1), 0),
                              ("BOTTOMPADDING", (0, 0), (-1, -1), 0)]))
    return row

TOTAL_PAGES = {"n": 6}

def on_page(canvas, doc, page_title):
    header_band(canvas, doc, "SFAR / SFPC — RPP, 2024",
                "Prévention des erreurs médicamenteuses en anesthésie-réanimation",
                page_title, icon_fn=lambda c, x, y: icon_pill(c, x, y, 13 * mm), color=TEAL_DARK)
    footer_band(canvas, doc, SOURCE_TXT, f"Page {doc.page} / {TOTAL_PAGES['n']}")

# ---------------------------------------------------------------------------
def _section_intro_champ1a():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Résumé :</b> RPP SFAR/SFPC (2024) — 29 recommandations (toutes avis d'experts, "
        "accord fort) et 2 absences de recommandation, sur 4 champs : environnement de "
        "travail et processus, facteurs humains et organisationnels, gestion des risques a "
        "posteriori, problématique des pénuries médicamenteuses. Complémentaire de la "
        "fiche déjà git-trackée <i>erreurs_medicamenteuses_ar_2016</i> (préconisation "
        "SFAR/SFPC antérieure, sur le même sujet).", S_BODY), bg=BG_PANEL, border=TEAL_DARK))
    story.append(Spacer(1, 2.5 * mm))
    story.append(legend_flowable())
    story.append(Spacer(1, 3 * mm))
    story.append(KeepTogether([
        section_bar("Champ 1 — Environnement de travail et processus (1/2)"),
        Spacer(1, 1 * mm),
        P("<b>Prescription</b>", S_CELL_B),
        Spacer(1, 1 * mm),
    ]))
    story.append(reco_table([
        ("R1.1", "Standardiser et utiliser des protocoles de prescription des médicaments "
         "(dilution, solvant, durée, vitesse, voie d'administration), pour réduire la "
         "survenue d'erreurs médicamenteuses.", "AE"),
        ("R1.2.1", "Utiliser un logiciel de prescription en soins critiques, pour diminuer "
         "les erreurs médicamenteuses et les effets indésirables évitables.", "AE"),
        ("R1.2.2", "Implémenter en soins critiques des outils informatiques d'aide à la "
         "prescription, pour réduire les erreurs médicamenteuses.", "AE"),
        ("R1.2.3", "Adapter les logiciels de prescription et outils d'aide à la population "
         "des services de soins critiques (adultes, enfants, nouveau-nés), les paramétrer "
         "avant déploiement (soignants + pharmaciens cliniciens) et les actualiser en "
         "continu, pour réduire les erreurs médicamenteuses.", "AE"),
    ], RCW))
    story.append(Spacer(1, 2 * mm))
    story.append(absence_note(
        "informatisation de la prescription en anesthésie (distincte de R1.2.1-1.2.3, "
        "spécifiques aux soins critiques)."))
    story.append(Spacer(1, 2 * mm))
    story.append(reco_table([
        ("R1.3", "Réaliser un bilan médicamenteux et une conciliation médicamenteuse en "
         "anesthésie et soins critiques, pour réduire les erreurs médicamenteuses.", "AE"),
    ], RCW))
    story.append(Spacer(1, 2 * mm))
    story.append(P("<b>Préparation</b>", S_CELL_B))
    story.append(Spacer(1, 1 * mm))
    story.append(reco_table([
        ("R1.4.1", "Standardiser la préparation des médicaments avec des protocoles "
         "(dilution, solvant, durée, vitesse, voie d'administration), pour réduire les "
         "erreurs médicamenteuses.", "AE"),
        ("R1.4.2", "Proscrire la coexistence de différentes concentrations d'un même "
         "médicament dans le plateau de médicaments, pour éviter les erreurs "
         "d'administration.", "AE"),
    ], RCW))
    return story

# ---------------------------------------------------------------------------
def _section_champ1b():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Champ 1 — Environnement de travail et processus (2/2)"),
        Spacer(1, 1 * mm),
        P("<b>Administration</b>", S_CELL_B),
        Spacer(1, 1 * mm),
    ]))
    story.append(reco_table([
        ("R1.5.1", "Standardiser l'administration des médicaments, utiliser des protocoles "
         "(durée, vitesse, voie) et le double contrôle, pour réduire les erreurs "
         "médicamenteuses.", "AE"),
        ("R1.5.2", "En dehors de l'IV directe, choisir des dispositifs médicaux adaptés "
         "(pousse-seringue électrique) à l'administration des médicaments injectables et "
         "former les professionnels à leur usage.", "AE"),
    ], RCW))
    story.append(Spacer(1, 2 * mm))
    story.append(P("<b>Étiquetage</b>", S_CELL_B))
    story.append(Spacer(1, 1 * mm))
    story.append(reco_table([
        ("R1.6.1", "Utiliser les codes couleurs internationaux pour l'étiquetage des "
         "seringues, poches et voies d'administration.", "AE"),
        ("R1.6.2", "Sur l'étiquette des poches de perfusion/PCA/PCEA, mentionner : nom du "
         "médicament (DCI), quantité/concentration, date-heure et auteur de la "
         "préparation, date-heure de pose, identité du patient (code barre).", "AE"),
        ("R1.6.3", "Apposer sur les voies d'administration (parties proximale et distale) "
         "des étiquettes de couleur à bordure spécifique, mentionnant explicitement la "
         "voie d'administration.", "AE"),
    ], RCW))
    story.append(Spacer(1, 2 * mm))
    story.append(P("<b>Conditionnement, dispositifs et connectique</b>", S_CELL_B))
    story.append(Spacer(1, 1 * mm))
    story.append(reco_table([
        ("R1.7.1", "Choisir des ampoules/flacons à étiquetage conforme aux recommandations "
         "ANSM (typographie, mentions, code couleur ISO 26825-2020 par classe "
         "pharmacologique).", "AE"),
        ("R1.7.2", "Limiter au strict nécessaire le nombre de médicaments différents "
         "disponibles ; éviter deux concentrations différentes ou des conditionnements "
         "similaires (forme, couleur, dénomination) pour un même médicament.", "AE"),
        ("R1.8", "Utiliser des seringues préremplies (SPR) plutôt que des seringues "
         "traditionnelles.", "AE"),
        ("R1.9", "Utiliser des normes de connectique par type de voie d'administration.",
         "AE"),
        ("R1.10", "Utiliser un système de traçabilité (code barre) aux différentes étapes "
         "du circuit du médicament.", "AE"),
    ], RCW))
    story.append(Spacer(1, 2 * mm))
    story.append(absence_note(
        "systèmes data-matrix et RFID (distincts de R1.10, traçabilité par code barre)."))
    story.append(Spacer(1, 2 * mm))
    story.append(P("<b>Approvisionnement et stockage</b>", S_CELL_B))
    story.append(Spacer(1, 1 * mm))
    story.append(reco_table([
        ("R1.11.1", "Standardiser l'approvisionnement, le rangement et le stockage en soins "
         "critiques (armoire à pharmacie, chariot d'urgence).", "AE"),
        ("R1.11.2", "Standardiser l'approvisionnement/rangement/stockage en anesthésie avec "
         "un système commun à tous les sites (chariots d'ALR, de pédiatrie, d'urgence).",
         "AE"),
    ], RCW))
    return story

# ---------------------------------------------------------------------------
def _section_champ2():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Champ 2 — Facteurs humains et organisationnels"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("R2.1.1", "Lutter contre les interruptions de tâches et les distractions.", "AE"),
        ("R2.1.2", "Restreindre les communications non essentielles lors de la préparation "
         "et de l'administration de médicaments.", "AE"),
        ("R2.1.3", "Réaliser au sein de chaque équipe un audit standardisé visant à limiter "
         "les interruptions de tâches spécifiques à l'équipe et à l'organisation.", "AE"),
        ("R2.2", "Utiliser la lecture attentive, la double lecture, la concordance, une "
         "communication sécurisée et une organisation du processus lors de la préparation "
         "et de l'administration.", "AE"),
        ("R2.3", "Utiliser la formation par tout type de simulation.", "AE"),
        ("R2.4", "Intégrer des pharmaciens cliniciens formés spécifiquement dans les "
         "services d'anesthésie et de soins critiques.", "AE"),
    ], RCW))
    return story

# ---------------------------------------------------------------------------
def _section_champ3_4_sources():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Champ 3 — Gestion des risques a posteriori"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("R3.1.1", "Déclarer et analyser a posteriori les erreurs médicamenteuses.", "AE"),
        ("R3.1.2", "Mettre en place des REX (Retour d'EXpérience).", "AE"),
    ], RCW))
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Champ 4 — Problématique des pénuries médicamenteuses"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("R4.1.1", "Anticiper le plus possible les changements de médicaments (marché ou "
         "rupture), en partenariat avec les pharmaciens cliniciens.", "AE"),
        ("R4.1.2", "Inclure des mesures de gestion des pénuries de produits de santé dans "
         "les plans de gestion des risques des établissements.", "AE"),
    ], RCW))
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("Sources et avertissement", color=GREY))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>Méthode :</b> groupe d'experts SFAR/SFPC, recherche bibliographique 2004-2024 "
        "(PRISMA), format PICO. Format RPP choisi en amont faute de données suffisantes "
        "pour une cotation GRADE numérique — 29 recommandations formulées comme avis "
        "d'experts, votées par méthode GRADE grid, accord fort obtenu pour la totalité "
        "après un tour de vote et quelques ajustements.", S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>Document source :</b> SFAR, en collaboration avec la Société Française de "
        "Pharmacie Clinique (SFPC), « Prévention des erreurs médicamenteuses en "
        "anesthésie-réanimation », RPP, texte validé par le Comité des Référentiels "
        "Cliniques de la SFAR le 30 avril 2024.", S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>URL source :</b> https://sfar.org/prevention-des-erreurs-medicamenteuses-en-"
        "anesthesie-reanimation/", S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>Couverture :</b> intégralité des 29 recommandations et des 2 absences de "
        "recommandation (4 champs). Aucune annexe dans le document source. Bibliographie "
        "et composition nominative du groupe d'experts non reproduites.", S_SOURCE))
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Avertissement :</b> cette fiche est une synthèse indépendante, produite pour "
        "un usage d'aide-mémoire. Elle reprend intégralement les 29 recommandations et les "
        "2 absences de recommandation du texte source, mais condense l'argumentaire de "
        "chaque item. Elle ne remplace pas le texte intégral et n'est ni éditée ni validée "
        "par la SFAR ni la SFPC.", S_BODY_SM), bg=GREY_LIGHT, border=GREY))
    return story

# ---------------------------------------------------------------------------
def _section_champ2_3_4_sources():
    story = _section_champ2()
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_champ3_4_sources())
    return story

SECTIONS = [
    ("Champ 1 — Environnement de travail et processus (1/2)", _section_intro_champ1a),
    ("Champ 1 — Environnement de travail et processus (2/2)", _section_champ1b),
    ("Champs 2-4 — Facteurs humains, risques & pénuries, sources",
     _section_champ2_3_4_sources),
]

def _make_doc(path=None):
    return SimpleDocTemplate(path or OUT, pagesize=A4,
                              leftMargin=MARGIN, rightMargin=MARGIN,
                              topMargin=32 * mm, bottomMargin=16 * mm,
                              title="Fiche SFAR/SFPC 2024 - Prevention des erreurs medicamenteuses",
                              author="Synthèse indépendante (source SFAR/SFPC)")

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
