# -*- coding: utf-8 -*-
"""
Fiche de synthese - "Reduction de l'impact environnemental de l'anesthesie
generale" - Recommandations de Pratiques Professionnelles (RPP), SFAR avec
la SF2H et la SFPC, 2022. Referentiel valide par le Comite des Referentiels
Cliniques de la SFAR le 02/06/2022, le CA de la SFAR le 29/06/2022 et le
Conseil Scientifique de la SF2H. 38 pages (17 pages de recommandations +
argumentaire detaille + bibliographie), telecharge depuis sfar.org
(download/reduction-de-limpact-environnemental-de-lanesthesie-generale/
?wpdmdl=37890).

METHODOLOGIE : methode GRADE(R) visee, mais NON applicable a l'ensemble des
questions (disclosed explicitement par la source elle-meme dans son propre
resume : "la methode GRADE ne pouvant pas etre appliquee a l'ensemble des
questions") - resultat : les 17 recommandations sont TOUTES au niveau
"Avis d'experts (Accord fort)", un seul et unique niveau pour l'ensemble du
document (meme convention qu'un chip unique deja rencontree dans ce corpus,
cf. fiche_bris_dentaires.py) - verifie par grep exhaustif ("Avis d'experts"
x17, "Accord fort" x17, decompte exact confirmant l'absence de variante
"Accord faible" ou de grade GRADE numerique 1+/1-/2+/2- dans ce document).

PERIMETRE ET CONDENSATION (regle de projet 2026-09-14, argumentaire
minimal) : le texte source consacre la tres grande majorite de ses 38 pages
a un "Argumentaire" detaille par recommandation (donnees environnementales
chiffrees : PRG100, duree de vie atmospherique, cout social du carbone,
etudes de consommation...) - exactement le pattern que la regle de projet
identifie a eviter. Les 17 enonces de recommandation eux-memes (texte
integral, jamais coupe) portent toute l'information actionnable ; seule une
poignee de chiffres cles est retenue en phrase de contexte quand elle
change concretement la pratique (PRG100 des halogenes, delai de changement
de circuit). Les 17 recommandations sont organisees en 3 "champs" (Vapeurs/
gaz anesthesiques ; Medicaments intraveineux ; Dispositifs medicaux et
environnement de travail), integralement repris. La bibliographie et la
methodologie GRADE detaillee (comite d'organisation, cotation Delphi) ne
sont pas transcrites (renvoi au texte integral).
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from style import *
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.units import mm

OUT = "/home/user/rfe-sfar-website/output/Fiche_SFAR_SF2H_SFPC_Impact_Environnemental_AG_2022.pdf"

SOURCE_TXT = ("Source : SFAR, avec la SF2H et la SFPC, « Réduction de l'impact environnemental de "
              "l'anesthésie générale », RPP, 2022. Fiche de synthèse non officielle : se référer au "
              "texte intégral.")

def P(txt, style=S_CELL):
    return Paragraph(txt, style)

def chip(label, **kw):
    return grade_chip(label, **kw)

CW_FULL = PAGE_W - 2 * MARGIN

def reco_table(rows, col_widths):
    """rows: (ref, text, grade_label)."""
    data = [[P("Réf.", S_HEAD_W), P("Recommandation", S_HEAD_W), P("Niveau", S_HEAD_W_C)]]
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

RCW = [16 * mm, CW_FULL - 16 * mm - 20 * mm, 20 * mm]

def bullets(items, style=S_BODY_SM):
    html = "&bull; " + "<br/>&bull; ".join(items)
    return P(html, style)

def legend_flowable():
    chip_w = 20 * mm
    content_w = CW_FULL
    row = Table([[chip("AE", width=chip_w - 2 * mm),
                  P("<b>AE = Avis d'experts (Accord fort).</b> Méthode GRADE® visée mais non "
                    "applicable à l'ensemble des questions (disclosed par la source elle-même) — "
                    "les 17 recommandations sont donc <b>toutes</b> à ce niveau unique, aucune "
                    "n'est graduée 1+/1-/2+/2- ni en « Accord faible ».", S_BADGE_HEAD)]],
                colWidths=[chip_w, content_w - chip_w])
    row.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                              ("LEFTPADDING", (0, 0), (-1, -1), 1),
                              ("RIGHTPADDING", (0, 0), (-1, -1), 1),
                              ("TOPPADDING", (0, 0), (-1, -1), 0),
                              ("BOTTOMPADDING", (0, 0), (-1, -1), 0)]))
    return row

TOTAL_PAGES = {"n": 4}

def on_page(canvas, doc, page_title):
    header_band(canvas, doc, "SFAR / SF2H / SFPC — RPP, 2022",
                "Réduction de l'impact environnemental de l'anesthésie générale",
                page_title, icon_fn=lambda c, x, y: icon_drop(c, x, y, 13 * mm), color=GREEN)
    footer_band(canvas, doc, SOURCE_TXT, f"Page {doc.page} / {TOTAL_PAGES['n']}")

# ---------------------------------------------------------------------------
def _section_intro_champ1():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Résumé :</b> 17 recommandations, en 3 champs, pour réduire l'impact "
        "environnemental de l'anesthésie générale sans compromettre la sécurité/qualité des "
        "soins : choix des vapeurs/gaz anesthésiques, médicaments intraveineux, dispositifs "
        "médicaux et organisation du travail. La méthode GRADE® n'a pu être appliquée à "
        "l'ensemble des questions — toutes les recommandations sont donc au niveau "
        "« Avis d'experts (Accord fort) ».", S_BODY), bg=GREEN_LIGHT, border=GREEN))
    story.append(Spacer(1, 2.5 * mm))
    story.append(legend_flowable())
    story.append(Spacer(1, 3 * mm))
    story.append(KeepTogether([
        section_bar("Champ 1 — Vapeurs et gaz anesthésiques"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("R1.1", "À bénéfice clinique égal, utiliser préférentiellement le sévoflurane au "
         "desflurane ou à l'isoflurane lors d'une anesthésie inhalée (PRG100 à 100 ans : "
         "sévoflurane 130, isoflurane 510, desflurane 2540 — desflurane jusqu'à 2540× plus "
         "réchauffant que le CO2).", "AE"),
        ("R1.2.1", "Ne pas utiliser le protoxyde d'azote lors d'une anesthésie inhalée, à "
         "bénéfice clinique égal (PRG100 = 265, durée de vie atmosphérique 114 ans).", "AE"),
        ("R1.2.2", "En cas d'utilisation du protoxyde d'azote, préférer un système "
         "d'administration par bouteille plutôt que par cadres et circuit de distribution.",
         "AE"),
        ("R1.3.1", "Utiliser un bas débit de gaz frais lors de l'anesthésie inhalée.", "AE"),
        ("R1.3.2", "En cas de système d'anesthésie inhalée à objectif de concentration "
         "(AINOC), utiliser préférentiellement le mode automatisé plutôt que manuel pour "
         "diminuer le débit de gaz frais.", "AE"),
        ("R1.4", "Utiliser un monitorage de la profondeur d'anesthésie en association avec "
         "la fraction expirée en vapeur anesthésique, pour diminuer la consommation "
         "d'halogénés.", "AE"),
        ("R1.5", "À bénéfice clinique égal, recourir indifféremment à un entretien par "
         "vapeurs inhalées ou par AIVOC au propofol : les vapeurs ont un impact par émission "
         "de gaz à effet de serre, le propofol une écotoxicité pour le sol et les eaux.",
         "AE"),
    ], RCW))
    return story

# ---------------------------------------------------------------------------
def _section_champ2():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Champ 2 — Médicaments intraveineux"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("R2.1.1", "En dehors d'une situation d'urgence attendue/prévisible, préparer juste "
         "avant leur utilisation uniquement les médicaments nécessaires à un patient donné, "
         "plutôt qu'une préparation systématique en amont (20 à 50 % des médicaments "
         "préparés sont in fine inutilisés et jetés selon les études citées ; jusqu'à 45 % "
         "des déchets pour le propofol seul).", "AE"),
        ("R2.1.2", "Utiliser préférentiellement des seringues pré-remplies pour les "
         "médicaments à usage occasionnel (drogues d'urgence : éphédrine, phényléphrine, "
         "atropine, adrénaline, suxaméthonium), plutôt que de les préparer à l'avance dans "
         "des seringues classiques.", "AE"),
        ("R2.2", "Lors de l'anesthésie générale totale intraveineuse, utiliser un "
         "monitorage de la profondeur d'anesthésie (BIS ou entropie), pour diminuer la "
         "consommation de propofol.", "AE"),
    ], RCW))
    return story

# ---------------------------------------------------------------------------
def _section_champ3():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Champ 3 — Dispositifs médicaux et environnement de travail"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("R3.1.1", "Privilégier au maximum les dispositifs médicaux réutilisables plutôt "
         "qu'à usage unique.", "AE"),
        ("R3.1.2", "Pour les dispositifs réutilisables, mettre en place des procédures "
         "d'inventaire et d'exploitation garantissant leur réutilisation maximale.", "AE"),
        ("R3.1.3", "Ne pas combiner, pour un dispositif médical donné, usage unique et "
         "usage multiple (effet additif de l'impact environnemental des deux types).",
         "AE"),
        ("R3.1.4", "Pour les dispositifs en plastique, sélectionner des modèles sans "
         "diéthylhexyle phtalate (DEHP) et privilégier des fabricants locaux.", "AE"),
        ("R3.2.1", "En association avec un changement de filtre à haute efficacité pour "
         "chaque patient et en l'absence de souillure visible, ne réaliser qu'un changement "
         "hebdomadaire des circuits de ventilateur plutôt qu'un changement quotidien.",
         "AE"),
        ("R3.3.1", "Mettre en place un programme de tri des déchets.", "AE"),
        ("R3.3.2", "Mettre en place un programme de recyclage et de valorisation des "
         "déchets.", "AE"),
    ], RCW))
    return story

# ---------------------------------------------------------------------------
def _section_sources():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("Sources et avertissement"))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "SFAR, avec la Société Française d'Hygiène Hospitalière (SF2H) et la Société "
        "Française de Pharmacie Clinique (SFPC), « Réduction de l'impact environnemental de "
        "l'anesthésie générale », Recommandations de Pratiques Professionnelles, référentiel "
        "validé par le Comité des Référentiels Cliniques de la SFAR le 02/06/2022, le "
        "Conseil d'Administration de la SFAR le 29/06/2022 et le Conseil Scientifique de la "
        "SF2H. Bibliographie extensive dans le texte intégral (non reproduite ici).",
        S_SOURCE))
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Avertissement :</b> cette fiche est une synthèse indépendante, produite pour un "
        "usage d'aide-mémoire. Elle reprend intégralement le texte des 17 recommandations "
        "mais condense fortement l'argumentaire environnemental détaillé (données "
        "chiffrées, références bibliographiques) qui compose l'essentiel du texte source "
        "(38 pages). Elle ne remplace pas le texte intégral et n'est ni éditée ni validée "
        "par la SFAR/SF2H/SFPC. La méthode GRADE® n'ayant pu être appliquée à l'ensemble des "
        "questions, aucune recommandation de ce document ne porte de grade numérique "
        "1+/1-/2+/2- — toutes sont des avis d'experts en accord fort, une information à ne "
        "pas perdre en cas de comparaison avec d'autres RFE de ce corpus.",
        S_BODY_SM), bg=GREY_LIGHT, border=GREY))
    return story

# ---------------------------------------------------------------------------
def _section_all():
    story = _section_intro_champ1()
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_champ2())
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_champ3())
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_sources())
    return story

SECTIONS = [
    ("Champ 1 (gaz), Champ 2 (médicaments IV), Champ 3 (dispositifs) & sources", _section_all),
]

def _make_doc(path=None):
    return SimpleDocTemplate(path or OUT, pagesize=A4,
                              leftMargin=MARGIN, rightMargin=MARGIN,
                              topMargin=32 * mm, bottomMargin=16 * mm,
                              title="Fiche SFAR/SF2H/SFPC 2022 - Impact environnemental de l'anesthesie generale",
                              author="Synthèse indépendante (source SFAR/SF2H/SFPC)")

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
