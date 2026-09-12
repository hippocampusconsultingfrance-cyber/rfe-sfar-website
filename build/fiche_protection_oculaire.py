# -*- coding: utf-8 -*-
"""
Fiche de synthese - RFE commune SFAR / SFO / SRLF, 2016
"Protection oculaire en anesthesie et reanimation". H. Keita, J-M Devys, J. Ripart,
M. Frost, I. Cochereau, F. Boutin, C. Guerin, D. Fletcher, V. Compere.
Anesth Reanim. 2016 (ANREA-135), doi 10.1016/j.anrea.2016.05.002. Texte valide par le
CA de la SFAR le 14/03/2016.
Source telechargee : sfar.org/wp-content/uploads/2016/03/Protection-oculaire-en-
Anesthesie-et-Reanimation-1.pdf (9 pages : 6 pages de texte clinique + references
[1]-[40] en fin de page 6-7 + Annexes 1-2, pages 7-9, tableaux de synthese des preuves
GRADE par etude - non retranscrits, voir disclosure de couverture).

METHODOLOGIE GRADE(R) : force 1+/1-/2+/2- (jamais imprime negatif dans ce texte) ou
avis d'experts (quand aucune meta-analyse ne permettait d'appliquer GRADE en totalite).
Accord du vote de relecture Delphi : "Accord FORT" imprime explicitement uniquement a
cote des 3 recommandations gradees GRADE (R1.1, R1.6, R2.2) - jamais reimprime a cote
des 9 avis d'experts individuels. Le paragraphe de synthese methodologique affirme
neanmoins que "un accord fort a ete obtenu pour la totalite des recommandations" apres
le tour de cotation Delphi - lu ici comme s'appliquant aux 12 recommandations, meme si
seules 3 le reimpriment explicitement item par item (disclosure, pas une invention de
tag pour les 9 autres).

INCOHERENCE SOURCE-INTERNE DISCLOSEE (verifiee par recomptage exhaustif, PAS silencieu-
sement resolue) : le paragraphe de methodologie affirme un chiffre total de "10 recom-
mandations" ("Apres synthese du travail des experts... 10 recommandations ont ete
formalisees... Parmi les recommandations, 1 est forte (Grade 1+), 2 sont faibles
(Grade 2) et, pour 9 recommandations, la methode GRADE ne pouvait pas s'appliquer...").
Mais 1+2+9 = 12, pas 10 - la propre addition du paragraphe contredit son propre chiffre
d'ouverture. Un recomptage exhaustif et programmatique du corps du texte (grep sur les
tags imprimes "(GRADE 1+)"/"(GRADE 2+)"/"(Avis d'experts)") confirme exactement
12 recommandations numerotees R1.1 a R3.4 (1x GRADE 1+, 2x GRADE 2+, 9x avis
d'experts) - la meme somme que celle du paragraphe (12), mais differente du chiffre
d'ouverture "10" imprime par la source elle-meme. Les deux chiffres source ("10"
d'ouverture vs "12" implicite par addition et confirme par comptage du corps du texte)
sont disclosés tels quels dans le panneau de methodologie ; aucun n'est devine "juste".

COUVERTURE : les 12 recommandations (R1.1-R3.4) et leurs argumentaires sont repris
integralement. Les Annexes 1 et 2 (tableaux de synthese des preuves GRADE, etude par
etude : plan d'experience, heterogeneite, biais, RR/WMD) ne sont pas retranscrites -
purement methodologiques/bibliographiques (justification du niveau de preuve deja
resumee dans chaque argumentaire), sans recommandation clinique supplementaire propre.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from style import *
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.units import mm

OUT = "/home/user/rfe-sfar-website/output/Fiche_SFAR_Protection_Oculaire_2016.pdf"

SOURCE_TXT = ("Source : « Protection oculaire en anesthésie et réanimation » — SFAR / "
              "SFO / SRLF, RFE 2016 (Anesth Reanim. 2016, ANREA-135). Fiche de synthèse "
              "non officielle : se référer au texte intégral.")

def P(txt, style=S_CELL):
    return Paragraph(txt, style)

def chip(label, **kw):
    return grade_chip(label, **kw)

def reco_table(rows, col_widths):
    """rows: (ref, text, grade_label)"""
    data = [[P("Réf.", S_HEAD_W), P("Recommandation", S_HEAD_W), P("Grade", S_HEAD_W_C)]]
    for ref, txt, grade in rows:
        data.append([P(ref, S_CELL_B), P(txt, S_CELL), chip(grade)])
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

def legend_flowable():
    items = [("1+", "Il faut faire"), ("2+", "Il faut probablement faire"),
             ("AE", "Avis d'experts")]
    content_w = PAGE_W - 2*MARGIN
    n = len(items)
    chip_w = 15*mm
    text_w = (content_w - n*chip_w) / n
    row_cells, col_widths = [], []
    for g, txt in items:
        row_cells.append(chip(g, width=chip_w-1.5*mm))
        row_cells.append(P(txt, S_BADGE_HEAD))
        col_widths += [chip_w, text_w]
    row = Table([row_cells], colWidths=col_widths)
    row.setStyle(TableStyle([("VALIGN",(0,0),(-1,-1),"MIDDLE"), ("LEFTPADDING",(0,0),(-1,-1),1), ("RIGHTPADDING",(0,0),(-1,-1),1)]))
    return row

RCW = [15*mm, PAGE_W-2*MARGIN-15*mm-18*mm, 18*mm]

TOTAL_PAGES = {"n": 6}

def on_page(canvas, doc, page_title):
    header_band(canvas, doc, "SFAR / SFO / SRLF — RFE 2016 — FICHE DE SYNTHÈSE",
                "Protection oculaire en anesthésie et réanimation",
                page_title, icon_fn=lambda c, x, y: icon_shield(c, x, y, 13*mm), color=NAVY)
    footer_band(canvas, doc, SOURCE_TXT, f"Page {doc.page} / {TOTAL_PAGES['n']}")

# ---------------------------------------------------------------------------
def _section_intro():
    story = []
    story.append(Spacer(1, 3*mm))
    story.append(info_panel(P(
        "<b>Champ :</b> prévention des complications oculaires liées à une perte de "
        "conscience prolongée (anesthésie ou réanimation) — toujours susceptibles de "
        "passer inaperçues puisque le patient ne peut pas manifester sa baisse de "
        "vision ou sa douleur. <b>Lésions de surface</b> (kératopathies, ulcères, liées "
        "à la malocclusion palpébrale) : les plus fréquentes, le plus souvent mineures "
        "et régressives, détectables par un œil rouge. <b>Accidents vasculaires</b> "
        "(occlusion de l'artère centrale de la rétine [OACR] par compression du globe, "
        "neuropathies optiques ischémiques aiguës [NOIA]) : se manifestent uniquement "
        "par une baisse de vision indolore, potentiellement définitive et bilatérale — "
        "l'OACR est le plus souvent unilatérale, les NOIA fréquemment bilatérales. RFE "
        "commune SFAR, Société française d'ophtalmologie (SFO), SRLF, <b>12 "
        "recommandations</b> sur 3 chapitres.",
        S_BODY), bg=BG_PANEL, border=TEAL))
    story.append(Spacer(1, 3*mm))
    story.append(info_panel(P(
        "<b>Méthodologie GRADE® :</b> force 1+/2+ (« il faut/probablement faire ») ou "
        "<b>avis d'experts</b> quand aucune méta-analyse ne permettait d'appliquer GRADE "
        "en totalité (revue systématique puis vote, validé si ≥ 70 % d'accord). "
        "L'« Accord FORT » du vote de relecture Delphi n'est imprimé explicitement, "
        "individuellement, qu'à côté des 3 recommandations gradées GRADE (R1.1, R1.6, "
        "R2.2) — jamais réimprimé à côté des 9 avis d'experts individuels. Le paragraphe "
        "de synthèse méthodologique affirme néanmoins qu'« un accord fort a été obtenu "
        "pour la totalité des recommandations » après le tour de cotation — lu ici comme "
        "s'appliquant aux 12 recommandations, sans réinventer un tag individuel pour les "
        "9 restantes.<br/><br/>"
        "<b>Disclosure — incohérence interne au document source</b> (vérifiée par "
        "recomptage exhaustif, non devinée) : le paragraphe de méthodologie affirme un "
        "total de <b>« 10 recommandations »</b>, mais sa propre répartition annoncée dans "
        "la même phrase (1 forte + 2 faibles + 9 avis d'experts) totalise <b>12</b> — et "
        "un recomptage programmatique du corps du texte confirme exactement <b>12 "
        "recommandations numérotées</b> (R1.1 à R3.4 : 1× GRADE 1+, 2× GRADE 2+, 9× avis "
        "d'experts). Les deux chiffres imprimés par la source (« 10 » d'ouverture vs "
        "« 12 » par addition et par comptage du corps du texte) sont disclosés tels "
        "quels ; aucun n'est deviné « juste ».",
        S_BODY_SM), bg=AMBER_LIGHT, border=AMBER))
    story.append(Spacer(1, 3*mm))
    story.append(section_bar("Légende des grades"))
    story.append(Spacer(1, 2*mm))
    story.append(legend_flowable())
    return story

def _section_ch1():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(KeepTogether([
        section_bar("Chapitre 1 — Prévention des lésions cornéennes en anesthésie"),
        Spacer(1, 1.5*mm),
        reco_table([
            ("R1.1", "Pour prévenir les lésions cornéennes lors d'une anesthésie "
             "générale, une <b>occlusion palpébrale systématique par bandes adhésives "
             "seules</b> est recommandée — supérieure ou équivalente aux autres méthodes "
             "(pommades, lubrifiants aqueux type méthylcellulose ou gel visqueux, "
             "lunettes de protection, lentilles hydrophiles, suture palpébrale, "
             "pansements hydrogel ou bio-occlusifs), avec moins d'effets indésirables. "
             "La simple fermeture manuelle de l'œil s'accompagne d'une incidence plus "
             "élevée de lésions cornéennes (10 % sur 300 « yeux », dont 90 % dans le "
             "groupe fermeture manuelle contre 6,6 % dans le groupe bandes adhésives).", "1+"),
            ("R1.2", "En dehors d'une induction en séquence rapide, l'occlusion "
             "palpébrale est recommandée dès la perte du réflexe ciliaire et avant "
             "l'intubation trachéale, afin de réduire le risque de lésions traumatiques "
             "de la cornée par un traumatisme direct (montres, badges, stéthoscopes, "
             "laryngoscope).", "AE"),
            ("R1.3", "Il est recommandé d'obtenir l'occlusion complète de l'œil en "
             "apposant jointivement la paupière supérieure et inférieure et de vérifier "
             "régulièrement l'efficacité de cette occlusion — une formation obligatoire "
             "sur ce point a permis de diviser par 3 l'incidence des lésions de cornée "
             "dans une étude de cohorte avant/après.", "AE"),
            ("R1.4", "Pour les chirurgies à risque (tête et cou, procédure en position "
             "ventrale ou latérale), il est probablement recommandé d'utiliser des "
             "lubrifiants aqueux sans conservateur et en unidose (méthylcellulose ou gel "
             "visqueux) en association à l'occlusion par bandes adhésives — alternative : "
             "pansements bio-occlusifs transparents sans lubrifiant.", "AE"),
            ("R1.5", "Pour les chirurgies à risque, il est recommandé de <b>ne pas "
             "utiliser les pommades grasses</b> — la méthylcellulose produit moins "
             "d'effets indésirables que les pommades à base de paraffine. Les positions "
             "ventrale/latérale et les chirurgies céphaliques/cervicales sont des "
             "facteurs de risque ; la durée d'anesthésie n'en est pas un, "
             "indépendamment.", "AE"),
            ("R1.6", "La mise en place, au sein des structures, d'un programme de "
             "formation et d'un protocole de prévention est probablement recommandée "
             "pour réduire l'incidence des lésions cornéennes sous anesthésie "
             "générale.", "2+"),
        ], RCW),
    ]))
    return story

def _section_ch2():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(KeepTogether([
        section_bar("Chapitre 2 — Prévention des lésions cornéennes en réanimation"),
        Spacer(1, 1.5*mm),
        reco_table([
            ("R2.1", "Chez les patients à risque (intubés-ventilés, sédatés ou à faible "
             "niveau de conscience), il faut probablement dépister les lésions "
             "cornéennes par un <b>test à la fluorescéine</b> (ophtalmoscope à lumière "
             "bleu-cobalt) — la majorité des lésions sont punctiformes, invisibles à "
             "l'œil nu, mais peuvent évoluer vers un ulcère de cornée avec séquelles "
             "visuelles. Incidence en réanimation : 8,6 % à 60 % selon les études, pic "
             "dans la première semaine d'admission. La sensibilité du dépistage par des "
             "réanimateurs formés est proche de celle des ophtalmologistes.", "AE"),
            ("R2.2", "Chez les patients de réanimation intubés-ventilés, il faut "
             "probablement utiliser du <b>gel aqueux ou des chambres humides</b> plutôt "
             "que des larmes artificielles — une méta-analyse de 7 études prospectives "
             "randomisées (n = 343 à 701 selon l'unité d'analyse) montre une réduction du "
             "risque de lésions avec la chambre humide par rapport aux larmes "
             "artificielles (RR 0,13 ; IC95 % 0,05-0,35), mais la chambre humide n'est "
             "pas supérieure au gel (RR 0,81 ; IC95 % 0,51-1,29). Données insuffisantes "
             "sur l'occlusion palpébrale, associée ou non à une lubrification.", "2+"),
        ], RCW),
    ]))
    return story

def _section_ch3():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(KeepTogether([
        section_bar("Chapitre 3 — Prévention des lésions rétiniennes (OACR & NOIA)"),
        Spacer(1, 1.5*mm),
        reco_table([
            ("R3.1", "Pour prévenir la compression directe du globe oculaire et les "
             "OACR en chirurgie du rachis en décubitus ventral (d'autant plus que la "
             "durée est longue), il est probablement recommandé d'utiliser des "
             "<b>têtières adaptées</b> garantissant l'absence de compression directe du "
             "globe (tête en position neutre, têtière à prise osseuse directe type "
             "Mayfield, ou coussin spécialement découpé permettant de contrôler les "
             "globes sans contact ni manipulation du patient).", "AE"),
            ("R3.2", "Il est probablement recommandé de <b>contrôler l'absence de toute "
             "compression extrinsèque</b> de la sphère oculaire tout au long de "
             "l'intervention. Dans le registre ASA des pertes de vision peropératoires, "
             "toutes les OACR (n = 10) étaient unilatérales, aucune n'avait eu de cadre "
             "de Mayfield et 70 % présentaient les stigmates d'un traumatisme externe du "
             "globe — les têtières « en fer à cheval » peuvent, en cas de déplacement, "
             "contribuer à une compression oculaire et une OACR.", "AE"),
            ("R3.3", "Dans la chirurgie de longue durée en décubitus ventral, il est "
             "probablement recommandé de préférer un léger proclive à une position de "
             "Trendelenburg, pour limiter la pression intraoculaire — le décubitus "
             "ventral majore le risque de compression en augmentant la PIO, d'autant "
             "plus marqué si associé à un Trendelenburg ; une inclinaison proclive de "
             "10° réduit ce risque.", "AE"),
            ("R3.4", "En chirurgie du rachis hémorragique de longue durée, pour prévenir "
             "les NOIA, il est probablement recommandé de <b>limiter l'hypotension "
             "artérielle, l'anémie sévère et l'hypovolémie</b>, d'autant plus que le "
             "patient est à risque (obésité, sexe masculin, HTA, facteur de risque "
             "vasculaire) — le nerf optique ne dispose pas d'une autorégulation aussi "
             "efficace que le cerveau ; dans le registre ASA, au moins un facteur de "
             "risque vasculaire était présent dans 82 % des cas malgré des patients "
             "souvent ASA 1. Facteurs de risque indépendants confirmés en chirurgie du "
             "rachis : sexe masculin, obésité, cadre de Wilson (compression "
             "abdominale), durée d'intervention longue, faible pourcentage de colloïde "
             "dans le remplissage.", "AE"),
        ], RCW),
    ]))
    story.append(Spacer(1, 4*mm))
    story.extend(_section_sources())
    return story

def _section_sources():
    story = []
    story.append(section_bar("Sources et traçabilité", color=GREY))
    story.append(Spacer(1, 2*mm))
    story.append(P(
        "<b>Document source :</b> « Protection oculaire en anesthésie et réanimation » "
        "— RFE commune Société française d'anesthésie et de réanimation (SFAR), Société "
        "française d'ophtalmologie (SFO), Société de réanimation de langue française "
        "(SRLF). Coordonnatrice d'experts : Hawa Keita-Meyer. H. Keita, J-M Devys, "
        "J. Ripart, M. Frost, I. Cochereau, F. Boutin, C. Guérin, D. Fletcher, V. "
        "Compère. Anesth Reanim. 2016 (ANREA-135), doi 10.1016/j.anrea.2016.05.002. "
        "Texte validé par le Conseil d'administration de la SFAR le 14/03/2016.", S_SOURCE))
    story.append(Spacer(1, 1.5*mm))
    story.append(P("<b>Méthodologie :</b> GRADE® (1+/2+ ou avis d'experts) ; « Accord "
                    "FORT » du vote Delphi imprimé individuellement pour les 3 items "
                    "gradés GRADE, affirmé globalement pour l'ensemble des 12 "
                    "recommandations par le paragraphe de synthèse — voir disclosure "
                    "méthodologique en page 1 sur l'incohérence \"10\" vs \"12\" "
                    "recommandations.", S_SOURCE))
    story.append(Spacer(1, 1.5*mm))
    story.append(P("<b>Couverture :</b> cette fiche reprend l'intégralité des 12 "
                    "recommandations (R1.1-R3.4) réparties sur les 3 chapitres "
                    "(prévention des lésions cornéennes en anesthésie, en réanimation, "
                    "prévention des lésions rétiniennes par OACR/NOIA), avec leurs "
                    "argumentaires. Comité d'organisation, groupe de lecture, les 40 "
                    "références bibliographiques et les Annexes 1-2 (tableaux de "
                    "synthèse des preuves GRADE étude par étude — plan d'expérience, "
                    "hétérogénéité, biais, RR/WMD) ne sont pas retranscrits : purement "
                    "méthodologiques/bibliographiques, sans recommandation clinique "
                    "propre au-delà de ce que chaque argumentaire résume déjà.", S_SOURCE))
    story.append(Spacer(1, 3*mm))
    story.append(info_panel(P(
        "<b>Avertissement — document de 2016 :</b> ce document est une fiche de "
        "synthèse indépendante, produite pour un usage d'aide-mémoire. Elle reprend "
        "l'intégralité des 12 recommandations du texte source, mais ne remplace pas le "
        "texte intégral (argumentaire complet, 40 références bibliographiques, Annexes "
        "1-2) et n'est ni éditée ni validée par la SFAR, la SFO ou la SRLF. En cas de "
        "doute, se référer au texte intégral et/ou à un avis ophtalmologique "
        "spécialisé.",
        S_BODY_SM), bg=GREY_LIGHT, border=GREY))
    return story

def _section_ch1_ch2():
    return _section_ch1() + [Spacer(1, 3*mm)] + _section_ch2()

SECTIONS = [
    ("Introduction, méthodologie & légende", _section_intro),
    ("Chapitres 1-2 — Lésions cornéennes", _section_ch1_ch2),
    ("Chapitre 3 — Lésions rétiniennes & sources", _section_ch3),
]

def _make_doc(path=None):
    return SimpleDocTemplate(path or OUT, pagesize=A4,
                              leftMargin=MARGIN, rightMargin=MARGIN,
                              topMargin=32*mm, bottomMargin=16*mm,
                              title="Fiche SFAR/SFO/SRLF 2016 - Protection oculaire en anesthesie et reanimation",
                              author="Synthèse indépendante (source SFAR/SFO/SRLF)")

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
    import pypdf, tempfile
    tmp_path = tempfile.mktemp(suffix=".pdf")
    doc = _make_doc(tmp_path)
    doc.build(story_flowables, onFirstPage=_silent_page, onLaterPages=_silent_page)
    with open(tmp_path, "rb") as f:
        n = len(pypdf.PdfReader(f).pages)
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
