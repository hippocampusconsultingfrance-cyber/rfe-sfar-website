# -*- coding: utf-8 -*-
"""
Fiche de synthese - "Preparation colique et anesthesie generale : position
commune SFED/SFAR" - Bulois P, Bazin JE, Lapuelle J, Al Nasser B, Chaussade
S, Bonnet F, Robaszkiewicz M, Ecoffey C, au nom des conseils d'administration
de la SFED (7 juillet 2016) et de la SFAR (validation 21 septembre 2016).
9 pages (texte + 30 references bibliographiques), telecharge depuis sfar.org
(wp-content/uploads/2019/04/preparation-colique-anesthesie-generale.pdf).

METHODOLOGIE : texte de "position commune" narratif, revue de la litterature
avec synthese pratique - PAS de grille GRADE/numerotation R1/R2 imprimee, pas
de vote de consensus formel. La force des enonces est portee par le texte
lui-meme ("il faut", "il est etabli que", constats factuels). Deux tableaux
pratiques dans le source (Tableau I : situations ralentissant la vidange
gastrique ; Tableau II : synthese des delais de jeune selon l'horaire de la
coloscopie) sont reproduits integralement - ce sont les elements que le
clinicien utilisera reellement au quotidien.

PERIMETRE ET CONDENSATION (regle de projet 2026-09-14, argumentaire minimal) :
la justification scientifique detaillee (meta-analyses, essais individuels
avec leurs OR/IC, references numerotees 1-30) est condensee - seules les
conclusions pratiques et les valeurs seuils sont reprises integralement. Les
30 references bibliographiques (page 7-9 du PDF source) ne sont pas
transcrites (renvoi au texte integral).
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from style import *
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.units import mm

OUT = "/home/user/rfe-sfar-website/output/Fiche_SFED_SFAR_Preparation_Colique_2016.pdf"

SOURCE_TXT = ("Source : SFED/SFAR, « Préparation colique et anesthésie générale : position "
              "commune », validée 7 juillet 2016 (SFED) / 21 septembre 2016 (SFAR). Fiche de "
              "synthèse non officielle : se référer au texte intégral.")

def P(txt, style=S_CELL):
    return Paragraph(txt, style)

CW_FULL = PAGE_W - 2 * MARGIN

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

TCW = [42 * mm, CW_FULL - 42 * mm]

def bullets(items, style=S_BODY_SM):
    html = "&bull; " + "<br/>&bull; ".join(items)
    return P(html, style)

TOTAL_PAGES = {"n": 4}

def on_page(canvas, doc, page_title):
    header_band(canvas, doc, "SFED / SFAR — POSITION COMMUNE, 2016",
                "Préparation colique et anesthésie générale",
                page_title, icon_fn=lambda c, x, y: icon_drop(c, x, y, 13 * mm), color=TEAL_DARK)
    footer_band(canvas, doc, SOURCE_TXT, f"Page {doc.page} / {TOTAL_PAGES['n']}")

# ---------------------------------------------------------------------------
def _section_intro_horaire():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Résumé :</b> la coloscopie est la méthode de référence pour l'exploration du "
        "côlon ; la qualité de la préparation colique conditionne le taux d'intubation "
        "caecale et le taux de détection d'adénomes. La grande majorité des coloscopies en "
        "France est réalisée sous anesthésie générale — une collaboration étroite entre "
        "anesthésistes et gastroentérologues est nécessaire sur la prescription et les "
        "modalités de la préparation.", S_BODY), bg=BG_PANEL, border=TEAL))
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("Horaire d'administration de la préparation colique"))
    story.append(Spacer(1, 1.5 * mm))
    story.append(theme_table([
        ("Coloscopie le matin",
         "La prise <b>fractionnée avec pause nocturne</b> est supérieure à la prise "
         "complète la veille, sur la tolérance globale, l'efficacité et l'observance "
         "(méta-analyse de 47 essais, tous produits confondus) — également meilleur taux "
         "de détection des lésions planes et meilleure volonté des patients de reprendre "
         "le même type de préparation. Vrai pour PEG, phosphate de sodium (OPS) et "
         "picosulfates."),
        ("Coloscopie l'après-midi",
         "La prise complète <b>le matin même</b> peut être envisagée. Pour le PEG 4 L : "
         "améliore qualité et tolérance (moins de troubles du sommeil et de "
         "ballonnements). Pour le PEG 2 L + acide ascorbique : améliore la tolérance mais "
         "pas l'efficacité. Pour les OPS : améliore efficacité et tolérance et préférée "
         "des patients vs 2 doses (veille + matin)."),
        ("Délai préparation → coloscopie",
         "La qualité de la préparation est <b>inversement corrélée au délai</b> écoulé "
         "depuis la dernière dose (jusqu'à −10 %/heure dans une étude). Délai optimal "
         "identifié : <b>3 à 5 heures</b> entre la fin de la purge et le début de la "
         "coloscopie (au-delà de 5 h, la qualité se dégrade). Un délai court n'augmente "
         "pas le risque d'impériosité fécale pendant le transport domicile → unité "
         "d'endoscopie."),
    ], TCW, head=("Situation", "Constats et recommandations pratiques")))
    return story

# ---------------------------------------------------------------------------
def _section_jeune():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Délai minimal entre préparation colique et anesthésie"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(P(
        "Le jeûne préopératoire standard (patients sans risque de retard de vidange "
        "gastrique) est de <b>2 heures pour les liquides clairs</b> et <b>6 heures pour "
        "les solides</b>. Les liquides de préparation colique se comportent comme des "
        "liquides clairs. Le volume gastrique résiduel après préparation colique "
        "(fractionnée ou non) n'est pas différent de celui observé après une gastroscopie "
        "simple sans préparation, y compris pour un jeûne de 2 à 3 h — la préparation "
        "fractionnée n'augmente donc pas le résidu gastrique. Une validation "
        "échographique retrouve un estomac vide 2 heures après la prise de phosphate de "
        "sodium + 750 ml de liquide clair.", S_BODY_SM))
    story.append(Spacer(1, 1.5 * mm))
    story.append(info_panel(P(
        "<b>Recommandation pratique :</b> un délai de <b>3 heures</b> entre la dernière "
        "prise de préparation colique et l'induction anesthésique répond aux exigences de "
        "sécurité, chez les patients sans retard de vidange gastrique. Les autres liquides "
        "clairs restent autorisés jusqu'à 2 heures avant l'anesthésie.", S_BODY),
        bg=GREEN_LIGHT, border=GREEN))
    return story

# ---------------------------------------------------------------------------
def _section_risque():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Patients à risque de vidange gastrique retardée"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(P(
        "À différencier du risque de résidu gastrique important : le risque "
        "d'<b>inhalation par régurgitation</b> en dehors d'un estomac plein, majoré en "
        "cas de reflux gastro-œsophagien sévère (avec ou sans hernie hiatale), plus "
        "fréquent chez le patient obèse et la femme enceinte. Le volume gastrique "
        "résiduel critique augmentant le risque de régurgitation passive se situe entre "
        "25 et 200 ml.", S_BODY_SM))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P("<b>Tableau I — Situations ralentissant la vidange gastrique</b>", S_CELL_B))
    story.append(Spacer(1, 1 * mm))
    story.append(bullets([
        "Douleur aiguë", "Prise d'opiacés", "Sclérodermie", "Amylose",
        "Ulcère gastro-duodénal", "Vagotomie",
        "Dysautonomie neurovégétative (syndrome de Shy-Drager)", "Tétraplégie",
        "Maladie de Parkinson", "Diabète ancien mal équilibré", "Occlusion intestinale",
    ]))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "Le tabagisme chronique ralentit la vidange gastrique, mais <b>le port de patch "
        "nicotinique ne la modifie pas</b> — l'abstention tabagique dans les heures "
        "précédant l'anesthésie limite l'hypersécrétion gastrique. L'obésité et la "
        "grossesse en dehors du travail, l'anxiété seule et les benzodiazépines "
        "n'altèrent pas la vidange gastrique.", S_BODY_SM))
    return story

# ---------------------------------------------------------------------------
def _section_hydroelectro():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Troubles hydro-électrolytiques et interactions médicamenteuses"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(theme_table([
        ("Phosphate de sodium",
         "Risque d'hyperosmolarité, hyponatrémie, hypernatrémie, <b>hyperphosphatémie</b> "
         "et hypokaliémie. L'hyponatrémie (absorption excessive de fluide hypotonique) "
         "touche surtout l'insuffisant rénal et le sujet âgé, et peut donner des crises "
         "convulsives. Le risque d'hyperphosphatémie (pouvant aller jusqu'à une "
         "néphropathie aiguë) est majoré en cas d'insuffisance rénale, chez le sujet âgé, "
         "en présence d'une cardiopathie/néphropathie/diabète, ou sous IEC/ARA II/"
         "diurétiques/AINS. <b>Contre-indiqué chez les sujets &lt; 18 ans et &gt; 65 "
         "ans.</b> Éviter avec les diurétiques de l'anse (hypokaliémie) et les "
         "digitaliques (toxicité cardiaque/torsade de pointe favorisée par "
         "l'hypokaliémie)."),
        ("PEG (polyéthylène-glycol)",
         "Induit peu de désordres hydroélectrolytiques — meilleure tolérance que le "
         "phosphate de sodium en cas d'insuffisance rénale, hépatique ou cardiaque "
         "congestive. De rares cas de sécrétion inappropriée d'hormone antidiurétique "
         "rapportés. Chez le sujet de plus de 85 ans, des hypokaliémies et plus rarement "
         "des hyponatrémies ont été décrites — un ionogramme sanguin peut être utile "
         "avant la coloscopie dans cette population. À ingérer à au moins 2 heures de "
         "distance de toute autre prise médicamenteuse."),
    ], TCW, head=("Produit", "Précautions")))
    return story

# ---------------------------------------------------------------------------
def _tableau_ii():
    head = ["Horaire de l'examen", "Alimentation légère jusqu'à",
            "Préparation colique jusqu'à", "Autres liquides clairs jusqu'à"]
    rows = [
        ["8h - 10h", "2h", "5h", "6h"],
        ["10h - 12h", "4h", "7h", "8h"],
        ["12h - 14h", "6h", "9h", "10h"],
        ["14h - 16h", "8h", "11h", "12h"],
        ["16h - 18h", "10h", "13h", "14h"],
    ]
    data = [[P(h, S_HEAD_W_C) for h in head]]
    for r in rows:
        data.append([P(r[0], S_CELL_B)] + [P(v, S_CELL_C) for v in r[1:]])
    cw = [38 * mm] + [(CW_FULL - 38 * mm) / 3.0] * 3
    t = Table(data, colWidths=cw, repeatRows=1)
    style_cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), NAVY), ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTNAME", (0, 0), (-1, 0), FONT_BOLD), ("FONTSIZE", (0, 0), (-1, 0), 8),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("ALIGN", (1, 1), (-1, -1), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 0.5, GREY_LIGHT),
        ("TOPPADDING", (0, 0), (-1, -1), 3.6), ("BOTTOMPADDING", (0, 0), (-1, -1), 3.6),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            style_cmds.append(("BACKGROUND", (0, i), (-1, i), BG_PANEL))
    t.setStyle(TableStyle(style_cmds))
    return t

def _section_conclusion():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Conclusion et tableau de synthèse pratique"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(P(
        "Une préparation colique optimale doit être efficace, acceptée et comprise par le "
        "patient, sans effet secondaire majeur. L'horaire de prise et le fractionnement de "
        "la dose sont des critères importants de réussite, quelle que soit la méthode "
        "utilisée. Un délai de 3 h entre la dernière prise de préparation et l'induction "
        "anesthésique semble raisonnable pour garantir l'absence de risque d'inhalation "
        "chez les patients sans ralentissement de la vidange gastrique. La communication "
        "entre les différents acteurs (anesthésiste/gastroentérologue) sur la stratégie de "
        "préparation envisagée est un gage de sécurité pour le patient.", S_BODY_SM))
    story.append(Spacer(1, 2 * mm))
    story.append(P(
        "<b>Tableau II — Dernières prises autorisées selon l'horaire programmé de la "
        "coloscopie</b>", S_CELL_B))
    story.append(Spacer(1, 1 * mm))
    story.append(_tableau_ii())
    return story

# ---------------------------------------------------------------------------
def _section_sources():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("Sources et avertissement"))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "Bulois P, Bazin JE, Lapuelle J, Al Nasser B, Chaussade S, Bonnet F, "
        "Robaszkiewicz M, Ecoffey C, au nom des conseils d'administration de la SFED "
        "(7 juillet 2016) et de la SFAR (validation 21 septembre 2016), « Préparation "
        "colique et anesthésie générale : position commune SFED/SFAR ». 30 références "
        "bibliographiques dans le texte intégral (non reproduites ici).", S_SOURCE))
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Avertissement :</b> cette fiche est une synthèse indépendante, produite pour "
        "un usage d'aide-mémoire. Elle condense la justification scientifique détaillée "
        "(méta-analyses, essais individuels) mais reprend intégralement les conclusions "
        "pratiques, seuils et tableaux du texte source. Elle ne remplace pas le texte "
        "intégral et n'est ni éditée ni validée par la SFED/SFAR. Ce document n'imprime "
        "aucune grille de grade ni recommandation numérotée — les mentions « il faut »/"
        "constats factuels reprennent la formulation du texte source.",
        S_BODY_SM), bg=GREY_LIGHT, border=GREY))
    return story

# ---------------------------------------------------------------------------
def _section_all():
    story = _section_intro_horaire()
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_jeune())
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_risque())
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_hydroelectro())
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_conclusion())
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_sources())
    return story

SECTIONS = [
    ("Horaire, jeûne, patients à risque, hydro-électrolytique, synthèse & sources",
     _section_all),
]

def _make_doc(path=None):
    return SimpleDocTemplate(path or OUT, pagesize=A4,
                              leftMargin=MARGIN, rightMargin=MARGIN,
                              topMargin=32 * mm, bottomMargin=16 * mm,
                              title="Fiche SFED/SFAR 2016 - Preparation colique et anesthesie generale",
                              author="Synthèse indépendante (source SFED/SFAR)")

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
