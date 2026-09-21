# -*- coding: utf-8 -*-
"""
Fiche de synthese - "Facteurs humains en situations critiques" -
Recommandations de Pratiques Professionnelles (RPP), SFAR en association
avec le Groupe Facteurs Humains en Sante (FHS), texte valide par le
Comite des Referentiels Cliniques de la SFAR le 14/05/2022 et les
Conseils d'Administration de la SFAR (19/05/2022) et de FHS (04/07/2022).
81 pages, telecharge depuis sfar.org (wpdmdl=37888).

METHODOLOGIE : methode GRADE prevue en amont (format PICO), mais "la
methode GRADE ne pouvant pas s'appliquer en totalite" (peu d'essais
randomises controles sur les facteurs humains en sante) - toutes les
recommandations formulees sous forme d'avis d'experts. Synthese du texte
source : "21 recommandations ... accord fort obtenu pour 100% des
recommandations". Decompte verifie exact par extraction integrale : 21
tags "Avis d'experts (accord fort)" imprimes (dont 1 au singulier "Avis
d'expert", meme sens), correspondant a 21 items numerotes - AUCUNE
incoherence source trouvee. Chip unique "AE" : document entierement
non-grade (comme fiche_optimisation_hemodynamique_pediatrie_2024.py).

PIEGE DE NUMEROTATION DISCLOSED : le texte source alterne, sans
justification apparente, entre le format "R3.8"/"R3.9" et "R.3.8"/
"R.3.10" (point apres le R) pour des items consecutifs de la meme
sous-liste - purement typographique, aucune signification, mais un
parseur automatique cherchant uniquement le motif "^R\\d" sans variante
"R\\." manquerait ces items (piege verifie et evite dans ce script par
lecture manuelle integrale, pas par regex seule).

PERIMETRE : integral sur les 4 champs (communication, organisation,
environnement de travail, formation) et les 21 recommandations. Les 16
annexes du source sont trois choses distinctes : (a) des liens externes
vers des mémos HAS/SFAR deja publies ailleurs (Annexes 1-3, 8, 12 -
non reproductibles, juste des URLs) ; (b) des exemples de cas cliniques
illustratifs (briefing/debriefing, Annexes 4, 6, 9, 11 - narratifs,
redondants avec le texte des recommandations, omis par la regle
argumentaire-minimal) ; (c) un seul outil pratique reellement
autoportant et non redondant avec le texte des recommandations,
l'Annexe 14 "Fiche de reaction immediate face a un comportement
hostile" (campagne SFAR/CFAR "1Patient1Equipe") - reproduite ici en
tableau condense, car directement actionnable au chevet/en situation de
tension d'equipe et non capturee par R1.1-R1.3. Bibliographie et
composition nominative des groupes de travail non reproduites.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from style import *
GRADE_COLORS["AE"] = (GREY, WHITE)
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.units import mm

OUT = "/home/user/rfe-sfar-website/output/Fiche_SFAR_Facteurs_Humains_Situations_Critiques_2022.pdf"

SOURCE_TXT = ("Source : SFAR / Groupe Facteurs Humains en Santé (FHS), « Facteurs humains en "
              "situations critiques », RPP, 2022. Fiche de synthèse non officielle : se référer "
              "au texte intégral.")

def P(txt, style=S_CELL):
    return Paragraph(txt, style)

def chip(label, **kw):
    return grade_chip(label, **kw)

CW_FULL = PAGE_W - 2 * MARGIN

def reco_table(rows, col_widths):
    """rows: (ref, text)."""
    data = [[P("Réf.", S_HEAD_W), P("Avis d'experts (accord fort)", S_HEAD_W)]]
    for ref, txt in rows:
        data.append([P(ref, S_CELL_B), P(txt, S_CELL)])
    t = Table(data, colWidths=col_widths, repeatRows=1)
    style_cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), NAVY), ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTNAME", (0, 0), (-1, 0), FONT_BOLD), ("FONTSIZE", (0, 0), (-1, 0), 8),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("GRID", (0, 0), (-1, -1), 0.5, GREY_LIGHT),
        ("TOPPADDING", (0, 0), (-1, -1), 3.4), ("BOTTOMPADDING", (0, 0), (-1, -1), 3.4),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            style_cmds.append(("BACKGROUND", (0, i), (-1, i), BG_PANEL))
    t.setStyle(TableStyle(style_cmds))
    return t

RCW = [16 * mm, CW_FULL - 16 * mm]

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

TCW = [44 * mm, CW_FULL - 44 * mm]

TOTAL_PAGES = {"n": 4}

def on_page(canvas, doc, page_title):
    header_band(canvas, doc, "SFAR / FHS — RECOMMANDATIONS DE PRATIQUES PROF., 2022",
                "Facteurs humains en situations critiques",
                page_title, icon_fn=lambda c, x, y: icon_shield(c, x, y, 13 * mm), color=TEAL_DARK)
    footer_band(canvas, doc, SOURCE_TXT, f"Page {doc.page} / {TOTAL_PAGES['n']}")

# ---------------------------------------------------------------------------
def _section_champ1_2():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Résumé :</b> RPP SFAR/FHS 2022 sur la gestion de crise en anesthésie-réanimation "
        "(« crisis resource management »). Méthode GRADE prévue en amont mais non applicable "
        "en totalité — les 21 recommandations sont toutes des <b>avis d'experts, à accord "
        "fort (100 %)</b>, sur 4 champs : communication, organisation, environnement de "
        "travail, formation. Décompte source vérifié exact.", S_BODY), bg=BG_PANEL,
        border=TEAL_DARK))
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Champ 1 — Communication"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("R1.1", "Réaliser un briefing avant la prise en charge d'une situation critique, "
         "pour améliorer les performances de l'équipe, le climat de sécurité et diminuer "
         "les événements indésirables."),
        ("R1.2", "Utiliser une communication sécurisée et standardisée en situation de "
         "crise, pour améliorer la morbi-mortalité et limiter l'incidence des événements "
         "indésirables."),
        ("R1.3", "Réaliser un débriefing juste après la prise en charge d'une situation "
         "critique, pour améliorer les compétences techniques et non techniques."),
    ], RCW))
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Champ 2 — Organisation"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("R2.1", "Développer une conscience situationnelle individuelle puis collective "
         "d'équipe, pour améliorer la qualité des soins et la sécurité du patient."),
        ("R2.2", "S'engager dans une démarche de développement de la culture de sécurité, "
         "pour améliorer la qualité des soins et réduire les événements indésirables "
         "graves en situation critique."),
        ("R2.3", "Adopter une organisation du travail en équipe reposant sur un leader "
         "clairement identifié, un partage d'informations, une coordination et une "
         "répartition cohérente des tâches, pour améliorer la sécurité des soins."),
        ("R2.4", "Utiliser une aide cognitive de crise, pour améliorer la qualité des "
         "soins et la sécurité du patient."),
    ], RCW))
    return story

# ---------------------------------------------------------------------------
def _section_champ3():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Champ 3 — Environnement de travail"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("R3.1.1", "Disposer le matériel nécessaire à la prise en charge d'une situation "
         "critique de façon logique, avec un emplacement connu de toute l'équipe, pour "
         "réduire les événements indésirables graves."),
        ("R3.1.2", "Organiser le réapprovisionnement et la vérification de ce matériel, "
         "pour réduire les événements indésirables graves."),
        ("R3.2.1", "Dispenser systématiquement une formation à tout nouveau matériel ou "
         "interface numérique avant sa mise en place, pour réduire les événements "
         "indésirables graves."),
        ("R3.2.2", "Former au moins un référent par service à l'utilisation avancée de ce "
         "matériel, pour réduire les événements indésirables graves."),
        ("R3.3", "Intégrer la notion d'utilisabilité des dispositifs complexes tout au "
         "long de leur cycle de vie (conception → utilisation en unité de soins), pour "
         "réduire les événements indésirables graves."),
        ("R3.4", "Se protéger d'une interruption de tâche, en particulier lors des étapes "
         "les plus vulnérables de la résolution de crise — sauf si l'interruption permet "
         "de rattraper une erreur en cours (cf R3.5-3.6)."),
        ("R3.5", "Ne pas interrompre les étapes aboutissant à l'administration d'une "
         "thérapeutique en situation critique, pour réduire les événements indésirables "
         "graves."),
        ("R3.6", "Porter, en amont d'une crise attendue ou anticipable, une attention "
         "particulière aux sources d'interruption technologiques (alarmes de moniteur, "
         "sonneries de téléphone…), pour améliorer la sécurité des patients."),
        ("R3.7", "Prendre en compte le risque de fatigue des professionnels exposés aux "
         "situations critiques et mettre en place des stratégies organisationnelles "
         "préventives (collectives et individuelles)."),
        ("R3.8", "Adapter la charge de travail aux effectifs présents, la répartir entre "
         "les membres de l'équipe et veiller à son adéquation avec les ressources "
         "disponibles, pour pouvoir faire face à une potentielle crise."),
        ("R3.9", "Maintenir une ambiance de travail adaptée en situation de crise — "
         "communication apaisée, niveau sonore optimal — pour améliorer la performance "
         "technique et non technique."),
        ("R3.10", "Limiter les facteurs responsables d'épuisement professionnel chez les "
         "soignants exposés aux situations de crise, pour diminuer le risque d'erreurs et "
         "de comportements non professionnels."),
    ], RCW))
    return story

# ---------------------------------------------------------------------------
def _section_champ4_annexe_sources():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Champ 4 — Formation"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("R4.1", "Assurer aux équipes confrontées aux situations critiques une "
         "préparation psychologique à la gestion du stress, pour améliorer leur vécu et "
         "leurs performances."),
        ("R4.2", "Former les équipes soignantes confrontées aux situations critiques aux "
         "facteurs humains, pour améliorer la qualité des soins et la sécurité du "
         "patient."),
    ], RCW))
    story.append(Spacer(1, 3 * mm))
    story.append(KeepTogether([
        section_bar("Annexe 14 — Réagir face à un comportement hostile (campagne "
                    "SFAR/CFAR « 1 Patient 1 Équipe »)", color=GREY),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(theme_table([
        ("1-3. Rester centré", "Rester concentré sur les soins et la situation du "
         "patient ; adopter soi-même un ton et une attitude calmes, directs, honnêtes, "
         "respectueux et positifs ; intervenir seulement quand l'autre est accessible "
         "émotionnellement (attendre que l'émotion redescende)."),
        ("4-8. Désamorcer", "Apaiser la tension en communiquant une intention positive ; "
         "écouter sans juger ; reformuler pour montrer sa compréhension ; demander "
         "confirmation de la bonne compréhension ; encourager la recherche d'un "
         "compromis."),
        ("3 attitudes contre-productives", "Éviter ou fuir ; se montrer agressif en "
         "retour ; répondre de façon sarcastique."),
        ("Méthode DESC (exprimer un désaccord)", "<b>D</b>écrire les faits/la situation "
         "(sans « tu »/« vous ») ; <b>E</b>xprimer une opinion/un ressenti sur les faits "
         "(« je ») ; <b>S</b>olutions — besoins centrés sur le patient, demande claire "
         "ouvrant à la négociation ; <b>C</b>onséquences positives de la solution pour "
         "les deux parties."),
    ], TCW, head=("Étape", "Contenu")))
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("Sources et avertissement", color=GREY))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>Méthode :</b> comité de 19 experts SFAR/FHS, méthode GRADE prévue en amont "
        "(format PICO) mais non applicable en totalité faute d'essais randomisés sur le "
        "sujet — 21 recommandations formulées comme avis d'experts après 2 tours de "
        "vote, accord fort pour 100 % d'entre elles. Ces RPP se substituent aux "
        "recommandations précédentes de la SFAR et/ou du groupe FHS sur le même champ.",
        S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>Document source :</b> SFAR, en association avec le Groupe Facteurs Humains "
        "en Santé (FHS), « Facteurs humains en situations critiques », RPP, texte validé "
        "le 14/05/2022 (SFAR) et le 04/07/2022 (FHS).", S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>URL source :</b> https://sfar.org/facteurs-humains-en-situations-critiques/",
        S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>Couverture :</b> intégralité des 21 recommandations (4 champs). L'Annexe 14 "
        "(fiche pratique de réaction face à un comportement hostile) est reproduite "
        "car directement actionnable et non redondante avec le texte des "
        "recommandations. Les autres annexes du source (exemples cliniques illustratifs "
        "de briefing/débriefing, liens externes vers des mémos HAS/SFAR déjà publiés "
        "ailleurs) ne sont pas reproduites. Bibliographie et composition nominative des "
        "groupes de travail non reproduites.", S_SOURCE))
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Avertissement :</b> cette fiche est une synthèse indépendante, produite pour "
        "un usage d'aide-mémoire. Elle reprend intégralement les 21 recommandations du "
        "texte source, mais condense l'argumentaire de chaque item. Elle ne remplace "
        "pas le texte intégral et n'est ni éditée ni validée par la SFAR ni FHS.",
        S_BODY_SM), bg=GREY_LIGHT, border=GREY))
    return story

# ---------------------------------------------------------------------------
SECTIONS = [
    ("Champ 1-2 — Communication & organisation", _section_champ1_2),
    ("Champ 3 — Environnement de travail", _section_champ3),
    ("Champ 4 — Formation, Annexe 14 & sources", _section_champ4_annexe_sources),
]

def _make_doc(path=None):
    return SimpleDocTemplate(path or OUT, pagesize=A4,
                              leftMargin=MARGIN, rightMargin=MARGIN,
                              topMargin=32 * mm, bottomMargin=16 * mm,
                              title="Fiche SFAR 2022 - Facteurs humains en situations critiques",
                              author="Synthèse indépendante (source SFAR/FHS)")

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
