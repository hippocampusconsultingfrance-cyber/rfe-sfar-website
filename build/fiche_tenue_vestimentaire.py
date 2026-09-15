# -*- coding: utf-8 -*-
"""
Fiche de synthese - RPP commune SFAR-SF2H (avec validation de l'AFC et du
CERES), "Tenue vestimentaire au bloc operatoire", 2021. Texte valide par
le Comite des Referentiels Cliniques de la SFAR (05/05/2021), le CA de la
SFAR (19/05/2021), le Conseil Scientifique de la SF2H (06/05/2021) et le
CA de l'AFC/CERES (28/05/2021). Ces RPP se substituent explicitement aux
recommandations precedentes SFAR et/ou SF2H sur le meme champ. 21 pages
source, telecharge depuis sfar.org (download/tenue-vestimentaire-au-bloc-
operatoire/?wpdmdl=35399).

METHODOLOGIE : format RPP, methodologie GRADE partiellement applicable
("la methode GRADE ne pouvait etre appliquee dans son integralite" - la
plupart des questions relevent d'un avis d'expert plutot que d'un niveau
de preuve gradable). Formulation uniforme "les experts suggerent de
faire/de ne pas faire", chaque enonce individuellement tague "Avis
d'expert (Accord Fort)" - verifie par grep exhaustif : AUCUNE mention
d'Accord Faible dans le texte, 100% Accord Fort confirme egalement par la
source elle-meme ("un accord fort a ete obtenu pour 100% des
recommandations").

INCOHERENCE DE COMPTAGE SOURCE DISCLOSED (regle 5, jamais resolue
silencieusement) : la source annonce "13 recommandations" formalisees
(section 2.2 Synthese des resultats), mais le compte direct des enonces
individuellement numerotes et tagues "Avis d'expert (Accord Fort)" donne
16 (R1.1.1, R1.1.2, R1.2, R1.3.1, R1.3.2, R1.4.1, R1.4.2, R1.4.3, R1.5,
R2.1.1, R2.1.2, R2.2, R3.1, R3.2, R4.1, R4.2). Aucun regroupement naturel
par numero parent (R1.1, R1.3, R1.4, R2.1) ne permet de reconcilier
exactement ce chiffre avec 13 (le regroupement le plus evident donne 11
groupes, pas 13) - divergence non resolue ici, disclosed telle quelle.
Cette fiche liste les 16 enonces individuellement gradés, dans l'ordre et
la numerotation exacts de la source.

PORTEE : couverture complete des 16 enonces gradés, organises par les 4
"CHAMPS" thematiques de la source (tenue de bloc, articles coiffants,
masques, chaussures/sur-chaussures).

ARGUMENTAIRE : tres fortement condense (regle de projet 2026-09-14) - la
source consacre plusieurs paragraphes d'argumentaire bibliographique
detaille par recommandation (etudes Kasina/Markel/Elmously/Copp/Zhiqing
et al., etc.) ; seuls les elements directement actionnables (frequences de
changement, normes citees, contre-indications explicites) sont conserves.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from style import *
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.units import mm

OUT = "/home/user/rfe-sfar-website/output/Fiche_SFAR_SF2H_Tenue_Vestimentaire_2021.pdf"

SOURCE_TXT = ("Source : « Tenue vestimentaire au bloc opératoire » — RPP commune SFAR-SF2H, "
              "2021 (avec validation AFC/CERES). Fiche de synthèse non officielle : se référer "
              "au texte intégral.")

def P(txt, style=S_CELL):
    return Paragraph(txt, style)

def chip(label, **kw):
    return grade_chip(label, **kw)

CW_FULL = PAGE_W - 2 * MARGIN

def reco_table(rows, col_widths):
    """rows: (ref, text)."""
    data = [[P("N°", S_HEAD_W_C), P("Recommandation", S_HEAD_W), P("Accord", S_HEAD_W_C)]]
    for ref, txt in rows:
        data.append([P(ref, S_CELL_B), P(txt, S_CELL), chip("AE")])
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

RCW = [18 * mm, CW_FULL - 18 * mm - 18 * mm, 18 * mm]

def legend_flowable():
    chip_w = 15 * mm
    content_w = CW_FULL
    row = Table([[chip("AE", width=chip_w - 2 * mm),
                  P("Format <b>RPP</b>, méthodologie GRADE partiellement applicable — "
                    "formulation uniforme « les experts suggèrent » (avis d'expert). "
                    "Toutes les recommandations de ce texte sont à <b>Accord fort</b> "
                    "(100 % selon la source).", S_BADGE_HEAD)]],
                colWidths=[chip_w, content_w - chip_w])
    row.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                              ("LEFTPADDING", (0, 0), (-1, -1), 1),
                              ("RIGHTPADDING", (0, 0), (-1, -1), 1),
                              ("TOPPADDING", (0, 0), (-1, -1), 0),
                              ("BOTTOMPADDING", (0, 0), (-1, -1), 0)]))
    return row

TOTAL_PAGES = {"n": 3}

def on_page(canvas, doc, page_title):
    header_band(canvas, doc, "SFAR — SF2H, RPP 2021",
                "Tenue vestimentaire au bloc opératoire",
                page_title, icon_fn=lambda c, x, y: icon_shield(c, x, y, 13 * mm), color=TEAL_DARK)
    footer_band(canvas, doc, SOURCE_TXT, f"Page {doc.page} / {TOTAL_PAGES['n']}")

# ---------------------------------------------------------------------------
def _section_all():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Résumé :</b> RPP commune SFAR-SF2H (avec validation AFC/CERES) sur la tenue "
        "vestimentaire au bloc opératoire : tenue de bloc, articles coiffants, masques, "
        "chaussures/sur-chaussures. Objectifs : prévention du risque infectieux pour le "
        "patient <b>et</b> réduction de l'impact environnemental (choix "
        "réutilisable/usage unique). <b>Ces RPP se substituent</b> aux recommandations "
        "SFAR et/ou SF2H précédentes sur ce champ.", S_BODY), bg=BG_PANEL, border=TEAL))
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("Méthodologie"))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "Méthodologie GRADE annoncée mais non intégralement applicable (la majorité des "
        "questions relève d'un avis d'expert plutôt que d'un niveau de preuve gradable) "
        "— formulation uniforme « les experts suggèrent de faire/de ne pas faire », "
        "cotation Delphi GRADE grid. <i>Note de comptage :</i> la source annonce « 13 "
        "recommandations », mais le compte direct des énoncés individuellement tagués "
        "« Avis d'expert (Accord Fort) » donne <b>16</b> — aucun regroupement évident "
        "par numéro parent ne réconcilie exactement ce chiffre avec 13. Divergence "
        "disclosed, non résolue ; cette fiche liste les 16 énoncés individuels dans "
        "l'ordre et la numérotation de la source.", S_BODY_SM))
    story.append(Spacer(1, 1.5 * mm))
    story.append(legend_flowable())
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("CHAMP 1 — Tenue de bloc opératoire (R1.1-R1.5)"),
        Spacer(1, 1.5 * mm),
        reco_table([
            ("R1.1.1", "Le personnel de bloc opératoire porte une tenue dédiée au bloc "
             "opératoire, indifféremment à usage unique ou réutilisable, pour prévenir "
             "le risque infectieux pour le patient."),
            ("R1.1.2", "Le personnel porte une tenue <b>réutilisable</b> plutôt qu'une "
             "tenue à usage unique, pour diminuer l'impact environnemental."),
        ], RCW),
    ]))
    story.append(Spacer(1, 1.5 * mm))
    story.append(KeepTogether([
        reco_table([
            ("R1.2", "Réaliser un essai sur le terrain des différents produits "
             "sélectionnés (efficacité, coût environnemental) auprès du personnel qui "
             "les utilisera, pour en apprécier les caractéristiques d'usage."),
        ], RCW),
    ]))
    story.append(Spacer(1, 1.5 * mm))
    story.append(KeepTogether([
        reco_table([
            ("R1.3.1", "En cas de souhait de se protéger du froid, le personnel porte "
             "par-dessus sa tenue une veste à manches longues, indifféremment à usage "
             "unique ou réutilisable."),
            ("R1.3.2", "Le personnel qui souhaite se protéger du froid <b>n'utilise "
             "pas</b> une casaque chirurgicale stérile dans cette indication (surcoût, "
             "risque de contamination de la tenue si la casaque traîne au sol)."),
        ], RCW),
    ]))
    story.append(Spacer(1, 1.5 * mm))
    story.append(KeepTogether([
        reco_table([
            ("R1.4.1", "Le personnel ne quitte pas le bloc opératoire avec sa tenue de "
             "bloc, pour en limiter la contamination."),
            ("R1.4.2", "Si le personnel doit, à titre exceptionnel, répondre à un motif "
             "impérieux et quitter le bloc avec sa tenue, il en change à son retour."),
            ("R1.4.3", "En cas de sortie courte (quelques minutes), une alternative "
             "possible est de couvrir sa tenue de bloc par une blouse fermée."),
        ], RCW),
    ]))
    story.append(Spacer(1, 1.5 * mm))
    story.append(reco_table([
        ("R1.5", "Le personnel change de tenue de bloc en cas de souillures, et au "
         "minimum à la fin de chaque journée de travail."),
    ], RCW))
    return story

def _section_coiffants_masques_chaussures():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(KeepTogether([
        section_bar("CHAMP 2 — Articles coiffants (R2.1-R2.2)"),
        Spacer(1, 1.5 * mm),
        reco_table([
            ("R2.1.1", "Le personnel porte un article coiffant, indifféremment à usage "
             "unique ou réutilisable, lors de sa présence dans l'enceinte du bloc "
             "opératoire, pour prévenir le risque infectieux."),
            ("R2.1.2", "Le personnel porte un article coiffant <b>réutilisable</b> "
             "soumis à un entretien régulier plutôt qu'un article à usage unique, pour "
             "diminuer l'impact environnemental."),
        ], RCW),
    ]))
    story.append(Spacer(1, 1.5 * mm))
    story.append(reco_table([
        ("R2.2", "Le personnel porte un article coiffant recouvrant toute la chevelure "
         "— indifféremment une charlotte, un calot ou une cagoule, aucun type "
         "n'ayant démontré de supériorité pour prévenir le risque infectieux."),
    ], RCW))
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("CHAMP 3 — Masques (R3.1-R3.2)"),
        Spacer(1, 1.5 * mm),
        reco_table([
            ("R3.1", "Le personnel non-chirurgical de bloc opératoire porte un masque à "
             "usage médical de type II ou IIR (norme NF EN 14683:2019) en salle "
             "d'intervention, pour diminuer le risque de transmission de "
             "micro-organismes à partir de l'oropharynx et du nez."),
        ], RCW),
    ]))
    story.append(Spacer(1, 1.5 * mm))
    story.append(reco_table([
        ("R3.2", "Le personnel change de masque chirurgical quand celui-ci devient "
         "humide ou présente des traces de projections de liquides biologiques, pour "
         "diminuer le risque de transmission de micro-organismes."),
    ], RCW))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<i>Repère :</i> une étude (Zhiqing et al.) suggère une contamination "
        "significativement accrue du masque au-delà de 2 heures de port — pertinence "
        "clinique en termes d'infection du site opératoire non démontrée à ce jour ; "
        "en l'absence de notion de durée, changer le masque s'il est souillé ou humide "
        "reste la règle retenue (R3.2).", S_NOTE))
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("CHAMP 4 — Chaussures / sur-chaussures (R4.1-R4.2)"),
        Spacer(1, 1.5 * mm),
        reco_table([
            ("R4.1", "Pour réduire la contamination de l'environnement du bloc "
             "opératoire, le personnel porte des chaussures réservées exclusivement à "
             "l'enceinte du bloc (norme EN ISO 20347:2012), changées au minimum "
             "quotidiennement (et plus en cas de souillures visibles), lavées "
             "régulièrement en machine."),
            ("R4.2", "Le personnel <b>ne porte pas</b> de sur-chaussures en plus des "
             "chaussures dédiées — le port de sur-chaussures n'est pas plus efficace "
             "pour réduire la contamination de l'environnement, et s'accompagne d'un "
             "risque de contamination des mains."),
        ], RCW),
    ]))
    return story

def _section_sources():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("Sources et traçabilité", color=GREY))
    story.append(Spacer(1, 2 * mm))
    story.append(P(
        "<b>Document source :</b> « Tenue vestimentaire au bloc opératoire » — RPP "
        "commune SFAR-SF2H, avec validation de l'Association Française de Chirurgie "
        "(AFC) et du Collectif EcoResponsabilité En Santé (CERES). Texte validé par le "
        "Comité des Référentiels Cliniques de la SFAR (05/05/2021), le CA de la SFAR "
        "(19/05/2021), le Conseil Scientifique de la SF2H (06/05/2021) et le CA de "
        "l'AFC/CERES (28/05/2021).", S_SOURCE))
    story.append(Spacer(1, 1 * mm))
    story.append(P("<b>Méthodologie :</b> GRADE partiellement applicable, formulation "
                    "RPP (« les experts suggèrent »), cotation Delphi GRADE grid — voir "
                    "détail en page 1.", S_SOURCE))
    story.append(Spacer(1, 1 * mm))
    story.append(P(
        "<b>URL source :</b> https://sfar.org/download/tenue-vestimentaire-au-bloc-"
        "operatoire/?wpdmdl=35399", S_SOURCE))
    story.append(Spacer(1, 1 * mm))
    story.append(P(
        "<b>Couverture :</b> intégralité des 16 énoncés gradés individuellement "
        "(4 champs thématiques : tenue de bloc, articles coiffants, masques, "
        "chaussures/sur-chaussures) — voir disclosure de la divergence de comptage "
        "source (13 annoncées vs 16 comptées) en page 1.", S_SOURCE))
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Avertissement — document validé 2021 :</b> cette fiche de synthèse "
        "indépendante reprend l'intégralité des recommandations du texte source, mais "
        "ne le remplace pas et n'est ni éditée ni validée par la SFAR ou la SF2H. Se "
        "référer aux protocoles locaux d'hygiène du bloc opératoire et au texte "
        "intégral pour l'argumentaire bibliographique complet.", S_BODY_SM),
        bg=GREY_LIGHT, border=GREY))
    return story

def _section_coiffants_masques_chaussures_sources():
    story = _section_coiffants_masques_chaussures()
    story.extend(_section_sources())
    return story

SECTIONS = [
    ("Méthodologie & tenue de bloc opératoire", _section_all),
    ("Articles coiffants, masques, chaussures & sources", _section_coiffants_masques_chaussures_sources),
]

def _make_doc(path=None):
    return SimpleDocTemplate(path or OUT, pagesize=A4,
                              leftMargin=MARGIN, rightMargin=MARGIN,
                              topMargin=32 * mm, bottomMargin=16 * mm,
                              title="Fiche SFAR-SF2H 2021 - Tenue vestimentaire au bloc operatoire",
                              author="Synthèse indépendante (source SFAR/SF2H)")

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

    doc = _make_doc()
    story = _build_upto(fns)
    doc.build(story, onFirstPage=on_page_final, onLaterPages=on_page_final)
    print("OK ->", OUT, f"({total_pages} pages)")

if __name__ == "__main__":
    build()
