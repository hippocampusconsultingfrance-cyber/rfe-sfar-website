# -*- coding: utf-8 -*-
"""
Fiche de synthese - "Organisation structurelle, materielle et
fonctionnelle des centres effectuant de l'anesthesie pediatrique" -
Recommandations pour la Pratique Professionnelle (RPP), SFAR-ADARPEF,
texte valide par le Comite des Referentiels Cliniques de la SFAR le
19/01/2023 et le Conseil d'Administration le 26/01/2023. 51 pages,
telecharge depuis sfar.org (wpdmdl=43179).

RELATION AVEC UN DOCUMENT DEJA GIT-TRACKE : ce corpus tracke deja
`anesth_pediatrique_structures` (SFAR, RFE, septembre 2000,
"Recommandations pour les structures et le materiel de l'anesthesie
pediatrique") - DEJA DISCLOSE dans le `short` de cette fiche comme
"Distinct de la RPP SFAR 2023 « Organisation de l'anesthesie
pediatrique » (organisation des centres), non traitee ici" : cette
fiche-ci EST ce document 2023 explicitement anticipe. Perimetre reel
verifie non redondant : le document 2000 detaille le materiel chiffre
(tailles de sondes, masques, canules...) au sein d'UN site ; le document
2023 porte sur l'organisation ENTRE sites/centres (reseaux ville/centre
specialise, criteres d'orientation par age/ASA, effectifs minimaux par
tranche d'age, formation des praticiens) - deux echelles differentes,
toutes deux necessaires, conservees sous des cles distinctes.

METHODOLOGIE : methode GRADE prevue en amont mais toutes les 34
recommandations formulees comme avis d'experts, a accord fort pour la
totalite (meme pattern que fiche_facteurs_humains_2022.py et
fiche_erreurs_medicamenteuses_2024.py - decompte source "34
preconisations" verifie exact par extraction integrale, aucune
divergence). Chip unique "AE". Terminologie du texte source : les
recommandations sont appelees "preconisations" dans la synthese des
resultats (RPP), mais chaque item individuel reste tague "avis
d'experts (accord fort)".

PERIMETRE : integral sur les 4 champs (structure et logistique ;
equipement et materiel ; formation ; organisation fonctionnelle) et les
34 recommandations. R4.3.1-4.3.4 (criteres d'effectifs par tranche
d'age) retranscrits a la fois en tableau texte integral (fidelite) et
resumes en tableau recapitulatif compact (lisibilite clinique - meme
information, deux presentations). Aucune absence de recommandation
trouvee dans ce document (contrairement a plusieurs autres RPP de ce
corpus). Bibliographie et composition nominative du groupe d'experts non
reproduites. Argumentaire minimal (regle de projet 2026-09-14).
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from style import *
GRADE_COLORS["AE"] = (GREY, WHITE)
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.units import mm

OUT = "/home/user/rfe-sfar-website/output/Fiche_SFAR_ADARPEF_Organisation_Anesthesie_Pediatrique_2023.pdf"

SOURCE_TXT = ("Source : SFAR-ADARPEF, « Organisation structurelle, matérielle et fonctionnelle des "
              "centres effectuant de l'anesthésie pédiatrique », RPP, 2023. Fiche de synthèse non "
              "officielle : se référer au texte intégral.")

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

TCW = [34 * mm, CW_FULL - 34 * mm]

def legend_flowable():
    chip_w = 15 * mm
    content_w = CW_FULL
    row = Table([[chip("AE", width=chip_w - 2 * mm),
                  P("<b>AE</b> = avis d'experts — méthode GRADE prévue en amont, mais les 34 "
                    "recommandations (« préconisations ») sont TOUTES formulées comme avis "
                    "d'experts, à accord fort pour la totalité d'entre elles (décompte source "
                    "vérifié exact). Aucune absence de recommandation dans ce document.",
                    S_BADGE_HEAD)]],
                colWidths=[chip_w] + [content_w - chip_w])
    row.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                              ("LEFTPADDING", (0, 0), (-1, -1), 1),
                              ("RIGHTPADDING", (0, 0), (-1, -1), 1),
                              ("TOPPADDING", (0, 0), (-1, -1), 0),
                              ("BOTTOMPADDING", (0, 0), (-1, -1), 0)]))
    return row

TOTAL_PAGES = {"n": 6}

def on_page(canvas, doc, page_title):
    header_band(canvas, doc, "SFAR / ADARPEF — RPP, 2023",
                "Organisation de l'anesthésie pédiatrique",
                page_title, icon_fn=lambda c, x, y: icon_shield(c, x, y, 13 * mm), color=TEAL_DARK)
    footer_band(canvas, doc, SOURCE_TXT, f"Page {doc.page} / {TOTAL_PAGES['n']}")

# ---------------------------------------------------------------------------
def _section_intro_champ1():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Résumé :</b> RPP SFAR-ADARPEF (2023) sur l'organisation structurelle, matérielle "
        "et fonctionnelle des centres pratiquant l'anesthésie pédiatrique — 34 "
        "recommandations (toutes avis d'experts, accord fort) sur 4 champs : structure et "
        "logistique, équipement et matériel, formation, organisation fonctionnelle. "
        "Complémentaire de la fiche déjà git-trackée <i>anesth_pediatrique_structures</i> "
        "(RFE SFAR 2000, matériel chiffré au sein d'un site) — celle-ci porte sur "
        "l'organisation ENTRE sites (réseaux, orientation par âge/ASA, effectifs).",
        S_BODY), bg=BG_PANEL, border=TEAL_DARK))
    story.append(Spacer(1, 2.5 * mm))
    story.append(legend_flowable())
    story.append(Spacer(1, 3 * mm))
    story.append(KeepTogether([
        section_bar("Champ 1 — Structure et logistique"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("R1.1", "Réaliser l'anesthésie pédiatrique dans une salle d'intervention disposant "
         "de matériel adapté au poids et à l'âge de l'enfant.", "AE"),
        ("R1.2", "Identifier un secteur pédiatrique en SSPI, pour regrouper personnel/"
         "matériel spécifiques et permettre la présence d'un accompagnant.", "AE"),
        ("R1.3.1", "Hospitaliser les enfants en pré et postopératoire dans un secteur dédié "
         "à la pédiatrie (conventionnel, ambulatoire ou soins critiques).", "AE"),
        ("R1.3.2", "Réaliser la consultation d'anesthésie dans un lieu dédié et adapté à "
         "l'enfant, pour favoriser son confort et diminuer son anxiété.", "AE"),
        ("R1.4.1", "Disposer d'un accès à un plateau technique (laboratoire, radiologie, "
         "produits sanguins labiles) capable de répondre aux besoins pédiatriques, dont les "
         "micro-prélèvements, pour toute activité pédiatrique programmée et/ou non "
         "programmée.", "AE"),
        ("R1.4.2", "Formaliser des réseaux de consultants spécialistes en pédiatrie, pour "
         "tout établissement ayant une activité pédiatrique programmée et/ou non "
         "programmée.", "AE"),
    ], RCW))
    return story

# ---------------------------------------------------------------------------
def _section_champ2():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Champ 2 — Équipement et matériel"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("R2.1.1", "Adapter tout le matériel d'assistance respiratoire à l'âge, au poids et "
         "à la taille de l'enfant, pour assurer normoxémie et normocapnie.", "AE"),
        ("R2.1.2", "Dans les salles non dédiées à la pédiatrie, utiliser un chariot mobile "
         "spécifique contenant le matériel de gestion des voies aériennes pédiatrique.",
         "AE"),
        ("R2.2.1", "Utiliser un matériel d'accès vasculaire adapté à l'âge/taille/poids de "
         "l'enfant.", "AE"),
        ("R2.2.2", "Disposer, dans tous les lieux d'anesthésie pédiatrique (bloc, SSPI), de "
         "matériel d'abord intra-osseux (perceuse et trocarts adaptés) pour les situations "
         "critiques.", "AE"),
        ("R2.3.1", "Pour les apports hydro-électrolytiques peropératoires de base : soluté "
         "glucosé à 5 % + ≥ 4 g NaCl/l (nouveau-né) ; soluté isotonique balancé glucosé à "
         "1 % (nourrisson/jeune enfant) ; soluté balancé isotonique (au-delà de 3 ans).",
         "AE"),
        ("R2.3.2", "Pour le remplissage vasculaire péri-opératoire : soluté balancé "
         "isotonique en 1<super>re</super> intention ; albumine si hypovolémie persistante, en particulier "
         "chez le nouveau-né/nourrisson.", "AE"),
        ("R2.4", "Disposer d'un chariot d'urgence pédiatrique avec aides cognitives "
         "spécifiques, en plus du matériel/médicaments d'urgence.", "AE"),
        ("R2.5.1", "Utiliser un monitorage dont les composants sont adaptés au poids et/ou "
         "à l'âge de l'enfant, pour une interprétation fiable.", "AE"),
        ("R2.5.2", "Chez le nouveau-né/nourrisson opéré de chirurgie majeure, monitorer "
         "l'oxygénation régionale cérébrale pour détecter précocement une désaturation "
         "cérébrale (hypotension, hypoxémie, anémie, hypocapnie).", "AE"),
        ("R2.6.1", "Réaliser un monitorage systématique de la température péri-opératoire "
         "chez l'enfant.", "AE"),
        ("R2.6.2", "Prévenir l'hypothermie dès le transport vers le bloc, débuter le "
         "réchauffement actif avant l'induction (dispositif adapté + contrôle de la "
         "température de salle), poursuivre en continu per- et postopératoire.", "AE"),
        ("R2.7", "Disposer de sondes échographiques linéaires 25-38 mm / 8-14 MHz pour les "
         "abords vasculaires et l'ALR chez l'enfant.", "AE"),
    ], RCW))
    return story

# ---------------------------------------------------------------------------
def _section_champ3_4a():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Champ 3 — Formation"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("R3.1.1", "Appliquer les recommandations européennes selon les spécificités "
         "nationales/locales : tout interne d'anesthésie-réanimation doit suivre ≥ 3 mois "
         "de formation en anesthésie pédiatrique en centre spécialisé (≥ 6 mois + passage "
         "en soins critiques pédiatriques pour une activité régulière future).", "AE"),
        ("R3.1.2", "Tout MAR pratiquant l'anesthésie pédiatrique doit avoir une activité "
         "régulière dédiée (≥ une demi-journée/semaine) et actualiser ses compétences via "
         "des programmes individuels, dans le cadre de la certification périodique.", "AE"),
        ("R3.1.3", "Promouvoir les programmes de formation basés sur la simulation, en "
         "formation initiale et continue.", "AE"),
    ], RCW))
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Champ 4 — Organisation fonctionnelle (1/2) — Réseaux et orientation"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("R4.1.1", "Les centres de proximité et spécialisés ayant une activité d'anesthésie "
         "pédiatrique doivent s'organiser en réseaux avec un centre spécialisé à vocation "
         "régionale, pour la chirurgie programmée ou non.", "AE"),
        ("R4.1.2", "Formaliser cette organisation en réseaux par une convention (charte de "
         "fonctionnement locale, transfert des cas complexes).", "AE"),
        ("R4.2.1", "Prendre en charge en centre spécialisé (ou à vocation régionale) : "
         "nouveau-né à terme &lt; 6 semaines, ancien prématuré &lt; 60 semaines d'âge "
         "post-conceptionnel, patients ASA 3 à 5 (risque majoré de complications "
         "cardio-respiratoires sévères).", "AE"),
        ("R4.2.2", "Certains patients ASA 3 peuvent être pris en charge hors centre "
         "spécialisé, dans un réseau de soins contractualisé (âge minimal, accord ARS).",
         "AE"),
    ], RCW))
    return story

# ---------------------------------------------------------------------------
def _section_champ4b():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Champ 4 — Organisation fonctionnelle (2/2) — Effectifs par âge"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(theme_table([
        ("&lt; 1 an, ou ASA 4-5\n(R4.3.1)", "Risque majoré d'arrêt cardiaque/hypoxie : "
         "2 professionnels dédiés exclusivement — ≥ 1 MAR à activité régulière et formation "
         "pédiatrique complémentaire, assisté d'un second professionnel d'anesthésie à "
         "activité pédiatrique régulière."),
        ("1-3 ans\n(R4.3.2)", "Risque majoré de complications respiratoires : MAR formé "
         "dédié + IADE à activité pédiatrique régulière dédié, OU MAR dédié seul avec "
         "second professionnel identifié à l'avance immédiatement disponible au bloc. "
         "Choix sous la responsabilité exclusive du MAR."),
        ("3-10 ans\n(R4.3.3)", "MAR formé + IADE dédié, OU MAR dédié avec second "
         "professionnel identifié à l'avance immédiatement disponible au bloc. Choix sous "
         "la responsabilité exclusive du MAR."),
        ("&gt; 10 ans\n(R4.3.4)", "Mêmes règles organisationnelles que chez l'adulte."),
    ], TCW, head=("Tranche d'âge", "Effectif requis")))
    story.append(Spacer(1, 2 * mm))
    story.append(P(
        "MAR = médecin anesthésiste-réanimateur ; IADE = infirmier anesthésiste diplômé "
        "d'État.", S_NOTE))
    story.append(Spacer(1, 2.5 * mm))
    story.append(reco_table([
        ("R4.4.1", "Présence permanente en SSPI d'une infirmière (IDE, IADE ou "
         "puéricultrice) formée au réveil pédiatrique.", "AE"),
        ("R4.4.2", "Associer systématiquement un second professionnel paramédical, pour "
         "les spécificités du réveil de l'enfant.", "AE"),
        ("R4.4.3", "Présence supplémentaire d'une seconde infirmière (IDE, IADE ou "
         "puéricultrice) si la SSPI a une capacité ≥ 6 postes.", "AE"),
        ("R4.5", "Pour une équipe à pratique mixte adulte/pédiatrique, concentrer "
         "l'activité pédiatrique sur un nombre limité de praticiens formés et actualisés.",
         "AE"),
        ("R4.6", "Collecter les données épidémiologiques/anesthésiques (dont incidents "
         "critiques) pour évaluer la qualité des soins par comparaison à la littérature "
         "récente.", "AE"),
    ], RCW))
    return story

# ---------------------------------------------------------------------------
def _section_sources():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("Sources et avertissement", color=GREY))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>Méthode :</b> groupe d'experts SFAR-ADARPEF, méthode GRADE prévue en amont, "
        "mais les 34 recommandations retenues sont toutes formulées comme avis d'experts, "
        "votées par méthode GRADE grid en 2 tours, accord fort pour la totalité.",
        S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>Document source :</b> SFAR-ADARPEF, « Organisation structurelle, matérielle et "
        "fonctionnelle des centres effectuant de l'anesthésie pédiatrique », RPP, texte "
        "validé par le Comité des Référentiels Cliniques de la SFAR le 19/01/2023 et le "
        "Conseil d'Administration le 26/01/2023.", S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>URL source :</b> https://sfar.org/organisation-de-lanesthesie-pediatrique/",
        S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>Couverture :</b> intégralité des 34 recommandations (4 champs). Aucune absence "
        "de recommandation dans ce document. R4.3.1-4.3.4 (effectifs par tranche d'âge) "
        "reproduites intégralement en tableau de recommandations ET résumées en tableau "
        "récapitulatif compact pour la lisibilité clinique. Bibliographie et composition "
        "nominative du groupe d'experts non reproduites.", S_SOURCE))
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Avertissement :</b> cette fiche est une synthèse indépendante, produite pour "
        "un usage d'aide-mémoire. Elle reprend intégralement les 34 recommandations du "
        "texte source, mais condense l'argumentaire de chaque item. Elle ne remplace pas "
        "le texte intégral et n'est ni éditée ni validée par la SFAR ni l'ADARPEF.",
        S_BODY_SM), bg=GREY_LIGHT, border=GREY))
    return story

def _section_champ4b_sources():
    story = _section_champ4b()
    story.append(Spacer(1, 3 * mm))
    story.extend(_section_sources())
    return story

# ---------------------------------------------------------------------------
SECTIONS = [
    ("Champ 1 — Structure et logistique", _section_intro_champ1),
    ("Champ 2 — Équipement et matériel", _section_champ2),
    ("Champs 3-4 — Formation & organisation (réseaux)", _section_champ3_4a),
    ("Champ 4 — Effectifs par âge & sources", _section_champ4b_sources),
]

def _make_doc(path=None):
    return SimpleDocTemplate(path or OUT, pagesize=A4,
                              leftMargin=MARGIN, rightMargin=MARGIN,
                              topMargin=32 * mm, bottomMargin=16 * mm,
                              title="Fiche SFAR-ADARPEF 2023 - Organisation anesthesie pediatrique",
                              author="Synthèse indépendante (source SFAR-ADARPEF)")

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
