# -*- coding: utf-8 -*-
"""
Fiche de synthese - RFE SFAR, "Recommandations sur la prise en charge du
tabagisme en periode peri operatoire", 2016. Auteurs coordinateurs :
B. Dureuil, S. Pierre. Elabore avec la SFT, le CNCT, la SOFCOT, le CNP de
Chirurgie Plastique et le CNP de Chirurgie Thoracique et Cardio-vasculaire.
Actualisation de la conference d'experts OFT/SFAR/AFC de 2005. Source de 29
pages (texte + tableaux GRADE d'evidence detailles), telecharge depuis
sfar.org (wp-content/uploads/2016/08/2-SFAR-RFE-tabac_proposition-CRC.pdf).

METHODOLOGIE : GRADE standard (qualite des preuves 4 niveaux, force binaire
1+/1-/2+/2-). SEULEMENT 4 recommandations formelles au total (R1-R4),
TOUTES Grade 1+ (forte positive), Accord fort - verifie par lecture
integrale des 493 premieres lignes du texte source (au-dela : ~2000 lignes
de tableaux GRADE d'evidence statistique par etude/critere de jugement -
non reproduits ici, cf. regle de projet 7, ce sont des tableaux de preuve
scientifique detaillee, pas du contenu recommandationnel). Une 5eme
question (cigarette electronique) n'a AUCUNE recommandation formulee - les
2 propositions soumises au vote (s'abstenir / ne pas decourager l'usage
chez les patients deja utilisateurs) ont toutes deux echoue au seuil GRADE
Grid (>=50% d'avis favorables et <20% d'avis contraires) - disclosure
integrale de cet echec de consensus (regle de projet 5), pas une omission.

ARGUMENTAIRE : condense (regle de projet 2026-09-14) aux seuils/delais
directement actionnables (ex. R2 : delais de 2/4/8 semaines et leurs effets
respectifs) ; les statistiques d'etudes (RR, IC95%, nombre de patients par
meta-analyse) sont omises du corps de la fiche - se referer au texte
integral et a ses tableaux GRADE pour le detail des preuves.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from style import *
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.units import mm

OUT = "/home/user/rfe-sfar-website/output/Fiche_SFAR_Tabagisme_Perioperatoire_2016.pdf"

SOURCE_TXT = ("Source : « Recommandations sur la prise en charge du tabagisme en période "
              "périopératoire » — RFE SFAR, 2016. Fiche de synthèse non officielle : se "
              "référer au texte intégral.")

def P(txt, style=S_CELL):
    return Paragraph(txt, style)

def chip(label, **kw):
    return grade_chip(label, **kw)

CW_FULL = PAGE_W - 2 * MARGIN

def reco_table(rows, col_widths):
    """rows: (ref, text, grade)."""
    data = [[P("N°", S_HEAD_W_C), P("Recommandation", S_HEAD_W), P("Grade", S_HEAD_W_C)]]
    for ref, txt, grade in rows:
        data.append([P(ref, S_CELL_B), P(txt, S_CELL), chip(grade)])
    t = Table(data, colWidths=col_widths, repeatRows=1)
    style_cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), NAVY), ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTNAME", (0, 0), (-1, 0), FONT_BOLD), ("FONTSIZE", (0, 0), (-1, 0), 8),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("ALIGN", (0, 0), (0, -1), "CENTER"),
        ("ALIGN", (2, 0), (2, -1), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 0.5, GREY_LIGHT),
        ("TOPPADDING", (0, 0), (-1, -1), 3.4), ("BOTTOMPADDING", (0, 0), (-1, -1), 3.4),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            style_cmds.append(("BACKGROUND", (0, i), (-1, i), BG_PANEL))
    t.setStyle(TableStyle(style_cmds))
    return t

RCW = [12 * mm, CW_FULL - 12 * mm - 18 * mm, 18 * mm]

TOTAL_PAGES = {"n": 3}

def on_page(canvas, doc, page_title):
    header_band(canvas, doc, "SFAR — RFE, 2016",
                "Tabagisme en période périopératoire",
                page_title, icon_fn=lambda c, x, y: icon_shield(c, x, y, 13 * mm), color=TEAL_DARK)
    footer_band(canvas, doc, SOURCE_TXT, f"Page {doc.page} / {TOTAL_PAGES['n']}")

# ---------------------------------------------------------------------------
def _section_all():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Résumé :</b> actualisation 2016 (SFAR, avec SFT/CNCT/SOFCOT/CNP Chirurgie "
        "Plastique/CNP Chirurgie Thoracique et Cardio-vasculaire) de la conférence "
        "d'experts OFT/SFAR/AFC de 2005 — volontairement réduite à un nombre limité de "
        "recommandations simples et applicables. En France, ~30 % des 11 millions de "
        "patients opérés chaque année sous anesthésie sont fumeurs. Le tabagisme actif "
        "augmente d'environ 20 % la mortalité hospitalière et de 40 % les complications "
        "majeures postopératoires. La période préopératoire est identifiée comme un "
        "« teachable moment » particulièrement favorable au sevrage. <b>4 recommandations "
        "au total, toutes Grade 1+ (forte positive), Accord fort.</b>", S_BODY),
        bg=BG_PANEL, border=TEAL))
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("Méthodologie — GRADE"))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "Méthode GRADE standard : qualité des preuves en 4 catégories (Haute/Modérée/"
        "Basse/Très basse), force de recommandation binaire — <b>forte</b> (GRADE 1+/1−, "
        "« il est recommandé de faire/ne pas faire ») ou <b>faible</b> (GRADE 2+/2−, "
        "« il est probablement recommandé »). Pour valider une recommandation par vote "
        "GRADE Grid : ≥ 50 % des experts favorables et &lt; 20 % contraires. Recherche "
        "bibliographique Medline/Cochrane sur 10 ans (sauf question 4), privilégiant "
        "méta-analyses, revues systématiques et grandes cohortes. Population : adulte et "
        "enfant étudiés séparément (chez l'enfant, seule l'éviction tabagique est "
        "étudiée).", S_BODY_SM))
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Les 4 recommandations (Questions 1 à 4)"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("R1", "Offrir une prise en charge comportementale et la prescription d'une "
         "substitution nicotinique pour l'arrêt du tabac avant toute intervention "
         "chirurgicale programmée.", "1+"),
        ("R2", "Recommander systématiquement l'arrêt préopératoire du tabac, "
         "indépendamment de la date d'intervention.", "1+"),
        ("R3", "Tous les professionnels du parcours de soins (chirurgiens, "
         "anesthésistes-réanimateurs, soignants) doivent informer les fumeurs des effets "
         "positifs de l'arrêt du tabac et leur proposer une prise en charge dédiée et un "
         "suivi personnalisé.", "1+"),
        ("R4", "Recommander l'arrêt du tabagisme parental ou l'éviction de l'enfant de "
         "tout environnement tabagique, le plus en amont possible de l'intervention.", "1+"),
    ], RCW))
    story.append(Spacer(1, 1.8 * mm))
    story.append(P(
        "<b>R1 :</b> une intervention comportementale intensive (consultation dédiée, "
        "suivi 4 semaines, substituts nicotiniques) multiplie par 10 le taux de sevrage "
        "préopératoire et réduit les complications de 60 % vs absence d'intervention ; "
        "les substituts nicotiniques n'augmentent pas la douleur postopératoire ni la "
        "consommation d'opiacés.", S_BODY_SM))
    story.append(Spacer(1, 1.2 * mm))
    story.append(P(
        "<b>R2 — seuils de délai (donnée la plus actionnable de la RFE) :</b> arrêt "
        "&gt; 8 semaines avant l'intervention → environ −50 % de complications "
        "respiratoires vs fumeur actif ; arrêt &gt; 4 semaines → environ −25 % ; arrêt "
        "entre 2 et 4 semaines → pas de réduction démontrée des complications "
        "respiratoires ; <b>aucun effet délétère respiratoire démontré pour un arrêt "
        "&lt; 2 semaines</b> avant la chirurgie. Bénéfice sur la cicatrisation démontré "
        "après 3-4 semaines d'arrêt. Le bénéfice augmente proportionnellement à la durée "
        "du sevrage, quel que soit le délai par rapport à l'intervention.", S_BODY_SM))
    story.append(Spacer(1, 1.2 * mm))
    story.append(P(
        "<b>R3 :</b> un conseil bref (&lt; 20 min, ≤ 1 visite de suivi) augmente "
        "l'abstinence à 6 mois de 60 % ; un conseil intensif (&gt; 20 min, &gt; 1 visite, "
        "brochure) l'augmente de plus de 80 % — le conseil intensif est supérieur au "
        "conseil bref en comparaison directe.", S_BODY_SM))
    story.append(Spacer(1, 1.2 * mm))
    story.append(P(
        "<b>R4 :</b> le tabagisme passif chez l'enfant multiplie par 2 le risque "
        "d'effets indésirables périopératoires lors d'une anesthésie générale (toux, "
        "laryngospasme, bronchospasme, désaturation). Aucune étude n'a établi le délai "
        "nécessaire entre l'arrêt du tabac parental et la réduction du risque chez "
        "l'enfant.", S_BODY_SM))
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Question 5 — Cigarette électronique : aucune recommandation possible", color=AMBER),
        Spacer(1, 1.5 * mm),
        info_panel(P(
            "<b>PICO :</b> quelles sont les conséquences et la place de la cigarette "
            "électronique en période périopératoire ? <b>Aucune recommandation n'a pu "
            "être formulée</b> — disclosure intégrale, per la règle GRADE Grid elle-même "
            "(≥ 50 % d'avis favorables et &lt; 20 % contraires requis) : deux propositions "
            "ont été soumises au vote des experts — (1) s'abstenir de toute recommandation "
            "(balance jugée incertaine), et (2) suggérer de ne pas décourager l'usage chez "
            "les patients l'utilisant déjà pour leur sevrage ou refusant les autres "
            "substituts (grade faible proposé). Le vote a montré une <b>grande dispersion "
            "des avis</b> sur la proposition (1) et des <b>avis très divergents</b> sur la "
            "proposition (2) — ni l'une ni l'autre n'a atteint le seuil de consensus "
            "requis par la méthode GRADE.", S_BODY), bg=AMBER_LIGHT, border=AMBER),
    ]))
    story.append(Spacer(1, 1.8 * mm))
    story.append(P(
        "Éléments de contexte cités par la source (non recommandationnels) : un essai "
        "randomisé (hors contexte chirurgical) montre que la cigarette électronique "
        "multiplie par 2 le taux d'arrêt du tabac vs absence d'intervention, sans "
        "différence démontrée vs substituts nicotiniques (preuve de qualité basse). La "
        "HAS (2015) jugeait alors les données insuffisantes pour la recommander dans le "
        "sevrage tabagique. Le Haut Conseil de la Santé Publique (26/02/2016) estimait "
        "qu'elle peut être une aide au sevrage tout en pouvant constituer une porte "
        "d'entrée dans le tabagisme et un risque de renormalisation de sa consommation.",
        S_BODY_SM))
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("Déclaration d'intérêts, sources et traçabilité", color=GREY))
    story.append(Spacer(1, 2 * mm))
    story.append(P(
        "<b>Déclaration d'intérêts :</b> tous les experts (H. Bouaziz, B. Chaput, "
        "B. Dureuil, B. Le Maître, Y. Martinet, AC. Masquelet, S. Pierre, C. Rivera, "
        "AM. Ruppert, J. Saboye, A. Sautet, JJ. Tournier, N. Wirth) déclarent n'avoir "
        "aucun conflit d'intérêt en lien direct avec le sujet.", S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>Document source :</b> « Recommandations sur la prise en charge du tabagisme "
        "en période péri opératoire » (Guidelines on preoperative smoking cessation) — "
        "RFE SFAR. Coordinateurs d'experts : B. Dureuil, S. Pierre. Comité "
        "d'organisation : S. Pierre. Élaborée avec la Société Française de Tabacologie "
        "(SFT), le Comité National Contre le Tabagisme (CNCT), la SOFCOT, le CNP de "
        "Chirurgie Plastique et le CNP de Chirurgie Thoracique et Cardio-vasculaire — "
        "actualisation de la conférence d'experts OFT/SFAR/AFC de 2005.", S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P("<b>Version :</b> 2016.", S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P("<b>Méthodologie :</b> GRADE (qualité des preuves 1-4, force "
                    "1+/1-/2+/2-, seuil de consensus GRADE Grid) — voir détail en page 1.",
                    S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>URL source :</b> https://sfar.org/wp-content/uploads/2016/08/"
        "2-SFAR-RFE-tabac_proposition-CRC.pdf", S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>Couverture :</b> intégralité des 4 recommandations (texte + grade) et de la "
        "Question 5 (absence de recommandation, intégralement disclosed avec le détail du "
        "vote). Les tableaux GRADE d'évidence statistique détaillée (qualité des preuves "
        "par étude et par critère de jugement, ~20 pages du document source) ne sont pas "
        "reproduits — se référer au texte intégral pour le détail des preuves "
        "scientifiques sous-jacentes.", S_SOURCE))
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Avertissement — document de 2016 :</b> cette fiche de synthèse indépendante "
        "reprend l'intégralité des recommandations du texte source, mais ne remplace pas "
        "le texte intégral et n'est ni éditée ni validée par la SFAR. Les données sur la "
        "cigarette électronique en particulier ayant pu évoluer significativement depuis "
        "2016, se référer à un avis spécialisé et aux recommandations actualisées avant "
        "toute décision thérapeutique.", S_BODY_SM), bg=GREY_LIGHT, border=GREY))
    return story

SECTIONS = [
    ("Méthodologie, recommandations 1 à 4, Question 5 & sources", _section_all),
]

def _make_doc(path=None):
    return SimpleDocTemplate(path or OUT, pagesize=A4,
                              leftMargin=MARGIN, rightMargin=MARGIN,
                              topMargin=32 * mm, bottomMargin=16 * mm,
                              title="Fiche SFAR 2016 - Tabagisme en periode perioperatoire",
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
