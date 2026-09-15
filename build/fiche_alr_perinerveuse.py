# -*- coding: utf-8 -*-
"""
Fiche de synthese - RFE SFAR, "Anesthesie loco-regionale perinerveuse
(ALR-PN)", validee par le CA de la SFAR le 18/11/2016 (publiee Anesth
Reanim. 2019;5:208-217, doi:10.1016/j.anrea.2019.02.003, Open Access CC
BY). Auteurs coordinateurs : M. Carles, S. Bloc. Mise a jour de la RPC-ALR
2003. 10 pages source, telecharge depuis sfar.org (wp-content/uploads/
2019/10/rfe-anesthesie-loco-regionale-perinerveuse.pdf).

METHODOLOGIE : GRADE standard (qualite des preuves 4 niveaux, force
1+/1-/2+/2-, vote Delphi GRADE Grid ; avis d'experts valide seulement si
accord fort >70%). 12 recommandations au total (R1.1-R5.2, comptees
directement, verifie exhaustif) : 1x Grade 1+ (R1.2), 1x Grade 1- (R1.3),
3x Grade 2+ (R3.2, R4.1, R4.2), 2x Grade 2- (R1.1, R3.1), 5x avis d'experts
(R2.1, R2.2, R2.3, R5.1, R5.2).

INCOHERENCE SOURCE DISCLOSED (regle 5) : le paragraphe de synthese
methodologique de la source contient un PLACEHOLDER NON REMPLI ("XX
recommandations ont été formalisées") et une repartition ("4 est forte
[Grade 1+], 5 sont faibles [Grade 2], 5... avis d'experts" = 4+5+5 = 14)
qui NE CORRESPOND PAS au compte direct de 12 recommandations numerotees
(R1.1 a R5.2) effectivement presentes dans le texte, ni a leur repartition
reelle par grade (2 Grade 1 [1x1+, 1x1-], 5 Grade 2 [3x2+, 2x2-], 5 avis
d'experts = 12). Tres probablement un paragraphe-modele issu d'un autre
document RFE du corpus SFAR jamais adapte a celui-ci avant publication -
disclose integralement, non resolu ici (le compte 12 ci-dessus est celui
utilise dans cette fiche, base sur un comptage exhaustif direct des
recommandations reellement presentes dans le texte).

ARTEFACT D'EXTRACTION : le signe "−" (negatif) est rendu "S" par
l'extraction PDF dans les tags de grade ("GRADE 2S", "GRADE 1S") - meme
classe d'artefact deja rencontree dans ce corpus (cf. fiche_sujet_age_esf).
Lu comme GRADE 2− et GRADE 1− respectivement, confirme par coherence du
sens des recommandations (formulations negatives : "ne sont probablement
pas recommandes", "n'est pas recommande").

SCOPE : la RFE ne remplace PAS la RPC 2003 (toujours valide pour les
donnees anatomocliniques et les techniques de base) - elle porte
uniquement sur les donnees NOUVELLES (echoguidage, adjuvants, toxicite,
terrains a risque). Perimetre volontairement limite aux 24 premieres
heures postoperatoires (douleur postoperatoire prolongee = referentiel
distinct, non couvert ici). Les redacteurs ne proposent plus d'indication
de l'ALR par type de chirurgie (les indications de la RPC 2003 sur ce
point sont jugees globalement peu pertinentes du fait de l'evolution des
techniques chirurgicales).

ARGUMENTAIRE : condense (regle de projet 2026-09-14) - seuls les seuils/
delais directement actionnables sont conserves ; les references
bibliographiques et la prose de justification sont omises.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from style import *
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.units import mm

OUT = "/home/user/rfe-sfar-website/output/Fiche_SFAR_ALR_Perinerveuse_2016.pdf"

SOURCE_TXT = ("Source : « Anesthésie loco-régionale périnerveuse (ALR-PN) » — RFE SFAR, "
              "validée 18/11/2016 (Anesth Reanim 2019;5:208-217). Fiche de synthèse non "
              "officielle : se référer au texte intégral.")

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
        ("TOPPADDING", (0, 0), (-1, -1), 3.2), ("BOTTOMPADDING", (0, 0), (-1, -1), 3.2),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            style_cmds.append(("BACKGROUND", (0, i), (-1, i), BG_PANEL))
    t.setStyle(TableStyle(style_cmds))
    return t

RCW = [14 * mm, CW_FULL - 14 * mm - 18 * mm, 18 * mm]

def legend_flowable():
    chip_w = 15 * mm
    content_w = CW_FULL
    row = Table([[chip("1+", width=chip_w - 2 * mm), chip("1-", width=chip_w - 2 * mm),
                  chip("2+", width=chip_w - 2 * mm), chip("2-", width=chip_w - 2 * mm),
                  chip("AE", width=chip_w - 2 * mm),
                  P("<b>GRADE</b> — 1+/1- : recommandation <b>forte</b> ; 2+/2- : "
                    "recommandation <b>faible</b> ; <b>AE</b> : avis d'experts (accord "
                    "fort &gt; 70 % requis). Toutes les recommandations de ce texte sont "
                    "à Accord fort.", S_BADGE_HEAD)]],
                colWidths=[chip_w, chip_w, chip_w, chip_w, chip_w, content_w - 5 * chip_w])
    row.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                              ("LEFTPADDING", (0, 0), (-1, -1), 1),
                              ("RIGHTPADDING", (0, 0), (-1, -1), 1),
                              ("TOPPADDING", (0, 0), (-1, -1), 0),
                              ("BOTTOMPADDING", (0, 0), (-1, -1), 0)]))
    return row

TOTAL_PAGES = {"n": 3}

def on_page(canvas, doc, page_title):
    header_band(canvas, doc, "SFAR — RFE, validée 18/11/2016",
                "Anesthésie loco-régionale périnerveuse",
                page_title, icon_fn=lambda c, x, y: icon_shield(c, x, y, 13 * mm), color=TEAL_DARK)
    footer_band(canvas, doc, SOURCE_TXT, f"Page {doc.page} / {TOTAL_PAGES['n']}")

# ---------------------------------------------------------------------------
def _section_all():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Résumé :</b> mise à jour de la RPC-ALR 2003 (SFAR), centrée sur les données "
        "nouvelles depuis 2003 (échoguidage devenu technique de référence, adjuvants, "
        "toxicité). <b>Ne remplace pas la RPC 2003</b>, toujours valide pour les données "
        "anatomocliniques et les techniques de base ; les redacteurs ne proposent plus "
        "d'indication de l'ALR par type de chirurgie (jugées peu pertinentes du fait de "
        "l'évolution des techniques chirurgicales). Périmètre volontairement limité aux "
        "24 premières heures postopératoires — la douleur postopératoire prolongée "
        "relève d'un référentiel distinct. 4 thèmes : médicaments, écueils liés au "
        "terrain, stratégies d'utilisation, hygiène et sécurité.", S_BODY),
        bg=BG_PANEL, border=TEAL))
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("Méthodologie — GRADE"))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "GRADE standard : qualité des preuves en 4 catégories (Haute/Modérée/Basse/Très "
        "basse), force binaire — forte (GRADE 1+/1−) ou faible (GRADE 2+/2−) — validée "
        "par vote Delphi (GRADE Grid). Seuls les essais randomisés contrôlés permettent "
        "une recommandation forte (Grade 1), sauf question à implication vitale majeure "
        "où l'allocation randomisée serait contraire à l'éthique. Un avis d'experts n'est "
        "validé qu'en cas d'accord fort (&gt; 70 % des experts).", S_BODY_SM))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<i>Disclosure :</i> le paragraphe de synthèse méthodologique de la source "
        "contient un texte non finalisé — « <b>XX</b> recommandations ont été "
        "formalisées » (XX littéralement non renseigné) et une répartition annoncée "
        "(4 fortes/5 faibles/5 avis d'experts = 14) qui ne correspond pas au compte "
        "direct des recommandations réellement présentes dans le texte (12, "
        "R1.1 à R5.2 : 2 Grade 1 [1×1+, 1×1−], 5 Grade 2 [3×2+, 2×2−], 5 avis "
        "d'experts). Très probablement un paragraphe-modèle d'un autre document RFE du "
        "corpus SFAR resté non adapté avant publication — disclosure non résolue ici ; "
        "le compte de 12 utilisé dans cette fiche est celui d'un comptage exhaustif "
        "direct.", S_NOTE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(legend_flowable())
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("1 — Médicaments pour la réalisation d'une ALR-PN (R1.1-R1.3)"),
        Spacer(1, 1.5 * mm),
        reco_table([
            ("R1.1", "Les mélanges d'AL (longue durée d'action + courte durée d'action) ne "
             "sont probablement pas recommandés si l'objectif est la réduction de la "
             "toxicité des AL.", "2-"),
            ("R1.2", "Il est recommandé d'utiliser l'échoguidage pour la réalisation d'une "
             "ALR périnerveuse, dans le but d'obtenir, pour une efficacité équivalente ou "
             "supérieure aux autres techniques, une réduction de la dose (volume et "
             "concentration) d'AL utilisés et donc du risque de toxicité systémique.",
             "1+"),
            ("R1.3", "Il n'est pas recommandé d'associer aux AL en périnerveux les "
             "agonistes morphiniques, le tramadol, la naloxone ou le magnésium, du fait de "
             "l'absence de bénéfice clinique significatif en termes de durée ou "
             "d'efficacité.", "1-"),
        ], RCW),
    ]))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>Repères :</b> la clonidine en adjuvant prolonge l'analgésie et la qualité du "
        "bloc sensitif/moteur, au prix d'un risque d'effets secondaires notables (balance "
        "bénéfice-risque à considérer au cas par cas — non formalisé en recommandation "
        "numérotée). L'adrénaline reste envisageable pour la réalisation de la "
        "dose-test.", S_BODY_SM))
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("2 — Écueils liés au terrain (R2.1-R2.3)"),
        Spacer(1, 1.5 * mm),
        reco_table([
            ("R2.1", "Il faut probablement administrer des émulsions lipidiques "
             "intraveineuses au cours d'une intoxication systémique aux anesthésiques "
             "locaux, en complément des mesures de réanimation.", "AE"),
            ("R2.2", "Il n'existe aucune contre-indication à la réalisation d'une ALR "
             "périnerveuse chez le patient septique, à la condition de ne pas ponctionner "
             "directement au niveau de la zone infectée.", "AE"),
            ("R2.3", "Chez un patient traité par anticoagulant oral direct (AOD) à dose "
             "curative et en dehors de l'urgence, il est probablement recommandé de "
             "respecter un intervalle d'arrêt de 3 jours avant l'ALR-PN (dernière prise à "
             "J-3), sauf dabigatran pour lequel une dernière prise à J-4 ou J-5 est "
             "préférable.", "AE"),
        ], RCW),
    ]))
    return story

def _section_strategies_hygiene():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("3 — Stratégies d'utilisation (R3.1-R4.2)"),
        Spacer(1, 1.5 * mm),
        reco_table([
            ("R3.1", "Il n'est probablement pas recommandé de réaliser systématiquement "
             "une ALR périnerveuse (bloc fémoral, bloc ilio-fascial ou bloc du plexus "
             "lombaire par voie postérieure) pour le contrôle de la douleur "
             "postopératoire en chirurgie programmée de la hanche.", "2-"),
            ("R3.2", "Pour la chirurgie du membre supérieur, il est probablement "
             "recommandé de réaliser une ALR périnerveuse par bloc des branches du "
             "plexus brachial comme seule technique anesthésique, pour un bénéfice sur "
             "les NVPO, l'épargne morphinique et la durée de séjour en SSPI.", "2+"),
            ("R4.1", "Pour la chirurgie de la carotide, la réalisation d'un bloc du plexus "
             "cervical superficiel est probablement recommandée en alternative ou "
             "associée à l'AG, pour la réalisation de la chirurgie et un meilleur "
             "contrôle de la douleur postopératoire immédiate.", "2+"),
            ("R4.2", "Pour la chirurgie de la thyroïde, la réalisation d'un bloc cervical "
             "superficiel bilatéral, associé à l'AG, est probablement recommandée pour "
             "réduire les doses d'agents anesthésiques peropératoires et contrôler la "
             "douleur postopératoire immédiate.", "2+"),
        ], RCW),
    ]))
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("4 — Hygiène et sécurité (R5.1-R5.2)"),
        Spacer(1, 1.5 * mm),
        reco_table([
            ("R5.1", "Lorsqu'un bloc périphérique est réalisé seul, il est recommandé de "
             "réaliser une durée de surveillance (clinique + monitorage) d'au moins "
             "30 minutes après une ALR du membre supérieur et 60 minutes après une ALR "
             "du membre inférieur (réalisée sans autre anesthésie : sédation, AG ou ALR "
             "périmédullaire).", "AE"),
            ("R5.2", "Il est probablement recommandé en première intention de réaliser "
             "une ALR chez un patient éveillé ou légèrement sédaté, calme et coopérant. "
             "Après discussion avec le patient, un bloc associé à une anesthésie "
             "(générale ou régionale) ou une sédation profonde reste possible s'il "
             "existe un bénéfice — traçabilité du choix importante ; l'échoguidage "
             "apporte alors probablement une sécurité supplémentaire.", "AE"),
        ], RCW),
    ]))
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Relecture RPC 2003 — Complications neurologiques des blocs "
                    "périphériques", color=AMBER),
        Spacer(1, 1.5 * mm),
        info_panel(P(
            "Conduite à tenir en cas de suspicion de lésion neurologique en rapport avec "
            "une ALR-PN (point d'actualisation, hors recommandation numérotée) : examen "
            "neurologique précis si la durée constatée du bloc dépasse la durée "
            "prévisible et/ou douleur neuropathique dans le territoire du bloc — avis "
            "neurologique rapide si déficit incomplet, neurochirurgical si déficit "
            "complet. En cas de suspicion de lésion nerveuse secondaire au bloc : "
            "<b>EMG précoce avant le 3<sup>e</sup> jour</b> (valeur de référence, "
            "dépistage d'une neuropathie préexistante), puis <b>EMG retardé à "
            "3 semaines</b> (diagnostic topographique/lésionnel). Imagerie possible dans "
            "le bilan étiologique, avec probablement un apport supérieur de l'IRM par "
            "rapport à l'échographie ou la TDM. L'information et l'accompagnement du "
            "patient sont des points capitaux de la prise en charge.", S_BODY), bg=AMBER_LIGHT, border=AMBER),
    ]))
    return story

def _section_sources():
    story = []
    story.append(Spacer(1, 1.5 * mm))
    story.append(section_bar("Déclaration d'intérêts, sources et traçabilité", color=GREY))
    story.append(Spacer(1, 1 * mm))
    story.append(P(
        "<b>Déclaration d'intérêts (sélection) :</b> Philippe Cuvillon (MSD, Ethypharma, "
        "Grunenthal, projet Smart Angel/BPI) ; Laurent Delaunay (Gamida, Nordic Pharma, "
        "GE) ; Valeria Martinez (Pfizer, Astellas, Grunenthal) ; Nadia Rosencher "
        "(Bayer, BMS, Pfizer, Aspen, Vifor, Hospira, Sandoz, Zimmer, Boehringer "
        "Ingelheim) ; Xavier Capdevila (Micrel, Pajunk, BBraun, Gamida, Halyard, "
        "Grunenthal, GE, Vifor Pharma, Pfizer, Sanofi). Les autres auteurs déclarent ne "
        "pas avoir de liens d'intérêts.", S_SOURCE))
    story.append(Spacer(1, 1 * mm))
    story.append(P(
        "<b>Document source :</b> « Anesthésie loco-régionale périnerveuse (ALR-PN) » — "
        "RFE SFAR. Coordinateurs : Michel Carles, Sébastien Bloc. Comité d'organisation : "
        "Dominique Fletcher. 4 groupes de travail (médicaments, écueils liés au terrain, "
        "stratégies d'utilisation, hygiène et sécurité). Texte validé par le Conseil "
        "d'administration de la SFAR le 18/11/2016.", S_SOURCE))
    story.append(Spacer(1, 1 * mm))
    story.append(P("<b>Version :</b> Anesth Reanim 2019;5:208-217. "
                    "doi:10.1016/j.anrea.2019.02.003. Publié en Open Access (CC BY 4.0).",
                    S_SOURCE))
    story.append(Spacer(1, 1 * mm))
    story.append(P("<b>Méthodologie :</b> GRADE (qualité des preuves 1-4, force "
                    "1+/1-/2+/2-, vote Delphi GRADE Grid) — voir détail en page 1.",
                    S_SOURCE))
    story.append(Spacer(1, 1 * mm))
    story.append(P(
        "<b>URL source :</b> https://sfar.org/wp-content/uploads/2019/10/"
        "rfe-anesthesie-loco-regionale-perinerveuse.pdf", S_SOURCE))
    story.append(Spacer(1, 1 * mm))
    story.append(P(
        "<b>Couverture :</b> intégralité des 12 recommandations (texte + grade, "
        "comptage exhaustif direct — voir disclosure méthodologique en page 1) et du "
        "point d'actualisation RPC 2003 sur les complications neurologiques. Hors "
        "champ, explicitement par la source elle-même : indications de l'ALR par type "
        "de chirurgie (non proposées, jugées peu pertinentes) ; douleur postopératoire "
        "prolongée au-delà des 24 premières heures (référentiel distinct) ; données "
        "anatomocliniques et techniques de base (toujours couvertes par la RPC 2003, "
        "non remplacée par ce texte).", S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(info_panel(P(
        "<b>Avertissement — document validé 2016 :</b> cette fiche de synthèse "
        "indépendante reprend l'intégralité des recommandations du texte source, mais "
        "ne remplace ni ce texte intégral ni la RPC 2003 sur l'ALR périnerveuse, et "
        "n'est ni éditée ni validée par la SFAR. Les techniques d'échoguidage et les "
        "seuils de gestion des anticoagulants oraux directs ayant pu évoluer depuis "
        "2016, se référer à un avis spécialisé et aux recommandations actualisées avant "
        "toute décision thérapeutique.", S_BODY_SM), bg=GREY_LIGHT, border=GREY))
    return story

def _section_strategies_hygiene_sources():
    story = _section_strategies_hygiene()
    story.extend(_section_sources())
    return story

SECTIONS = [
    ("Méthodologie, médicaments & écueils liés au terrain", _section_all),
    ("Stratégies d'utilisation, hygiène-sécurité & sources", _section_strategies_hygiene_sources),
]

def _make_doc(path=None):
    return SimpleDocTemplate(path or OUT, pagesize=A4,
                              leftMargin=MARGIN, rightMargin=MARGIN,
                              topMargin=32 * mm, bottomMargin=16 * mm,
                              title="Fiche SFAR 2016 - Anesthesie loco-regionale perinerveuse",
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
