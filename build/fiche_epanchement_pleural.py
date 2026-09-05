# -*- coding: utf-8 -*-
"""
Fiche de synthese - RPP SFAR 2023 (avec SFMU, SPLF, SFCTCV)
Epanchement pleural liquidien de l'adulte en soins critiques
(a l'exception des pleuresies purulentes, hemothorax et epanchements neoplasiques).
Texte valide CRC SFAR 10/04/2023, CA SFAR 20/04/2023, CA SFCTCV/SFMU 21/06/2023, CA SPLF 18/07/2023.

Methodologie : PAS de GRADE numerique - toutes les 25 recommandations sont des "avis d'experts"
avec "accord FORT" (methode GRADE grid pour le vote, mais litterature jugee insuffisante pour
graduer numeriquement chaque item - RPP, pas RFE). 4 champs, 25 recommandations + 3 items
"ABSENCE DE RECOMMANDATION" explicites (absence de litterature).

Comptage experts : le resume de la source annonce "15 experts", mais un comptage direct des 4
listes nominatives (Experts SFAR=9, SFCTCV=3, SFMU=2, SPLF=2) donne 16 - incoherence interne a
la source, non reconciliee, disclosee ici (meme pattern que les fiches EER/IH de ce corpus).

1 tableau verbatim (gestion des anticoagulants avant drainage pleural, 6 lignes) + 1 figure
(Figure 1, photos d'equipement de drainage - pure image, decrite en prose, non retranscrite en
tableau car elle n'illustre qu'une terminologie deja expliquee dans le texte).
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from style import *
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.units import mm

OUT = "/private/tmp/claude-501/-Users-macbook-Downloads-claude/65498e3e-5ddf-47a6-b100-3ac535d1faa0/scratchpad/rfe_sfar/output/Fiche_SFAR_Epanchement_Pleural_2023.pdf"

SOURCE_TXT = ("Source : Recommandations pour la Pratique Professionnelle « Épanchement pleural "
              "liquidien de l'adulte en soins critiques » - SFAR, SFMU, SPLF, SFCTCV. Publié 2023. "
              "Fiche de synthèse non officielle : se référer au texte intégral.")

def P(txt, style=S_CELL):
    return Paragraph(txt, style)

def chip(label, **kw):
    return grade_chip(label, **kw)

def reco_table(rows, col_widths):
    """rows: (ref, text) - toutes les recommandations de cette RPP sont Avis d'experts (AE)"""
    data = [[P("Réf.", S_HEAD_W), P("Recommandation", S_HEAD_W), P("Accord", S_HEAD_W_C)]]
    for ref, txt in rows:
        data.append([P(ref, S_CELL_B), P(txt, S_CELL), chip("AE")])
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

def simple_table(header, rows, col_widths):
    data = [[P(h, S_HEAD_W) for h in header]]
    for r in rows:
        data.append([P(c, S_CELL) for c in r])
    t = Table(data, colWidths=col_widths, repeatRows=1)
    st = [
        ("BACKGROUND",(0,0),(-1,0), TEAL_DARK), ("TEXTCOLOR",(0,0),(-1,0), WHITE),
        ("FONTNAME",(0,0),(-1,0), FONT_BOLD), ("FONTSIZE",(0,0),(-1,0), 8),
        ("GRID",(0,0),(-1,-1),0.5,GREY_LIGHT), ("VALIGN",(0,0),(-1,-1),"TOP"),
        ("TOPPADDING",(0,0),(-1,-1),3.2), ("BOTTOMPADDING",(0,0),(-1,-1),3.2), ("LEFTPADDING",(0,0),(-1,-1),5),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            st.append(("BACKGROUND",(0,i),(-1,i), BG_PANEL))
    t.setStyle(TableStyle(st))
    return t

def no_reco_panel(text):
    return info_panel(P("<b>Absence de recommandation</b> — " + text, S_BODY_SM), bg=GREY_LIGHT, border=GREY)

TOTAL_PAGES = {"n": 6}

def on_page(canvas, doc, page_title):
    header_band(canvas, doc, "SFAR / SFMU / SPLF / SFCTCV — RPP 2023 — FICHE DE SYNTHÈSE",
                "Épanchement pleural liquidien de l'adulte",
                page_title, icon_fn=lambda c,x,y: icon_drop(c, x, y, 13*mm), color=TEAL_DARK)
    footer_band(canvas, doc, SOURCE_TXT, f"Page {doc.page} / {TOTAL_PAGES['n']}")

# ---------------------------------------------------------------------------
def _section_intro_champ1():
    story = []
    story.append(Spacer(1, 3*mm))
    story.append(info_panel(P(
        "<b>Champ de la RPP :</b> diagnostic et prise en charge (indication du drainage, choix du "
        "type de drain, pose, surveillance, retrait) des épanchements pleuraux <b>liquidiens</b> "
        "de l'adulte en soins critiques — <b>hors pleurésie purulente, hémothorax et épanchement "
        "néoplasique</b>, et hors population pédiatrique. RPP sous l'égide de la SFAR, avec la SFMU "
        "(médecine d'urgence), la SPLF (pneumologie) et la SFCTCV (chirurgie thoracique).<br/><br/>"
        "<b>25 recommandations</b> réparties en 4 champs : (1) diagnostic et retentissement, "
        "(2) procédure de drainage, (3) surveillance de l'efficacité et des complications, "
        "(4) procédure de retrait du drain. <b>Toutes les recommandations sont des « avis "
        "d'experts » avec accord FORT</b> (méthode GRADE grid utilisée pour le vote, mais aucune "
        "recommandation n'a pu être graduée numériquement faute de littérature suffisante — RPP, "
        "et non RFE). Après 4 tours de cotation, un accord fort a été obtenu pour les 25 "
        "recommandations, sans exception. Pour <b>3 questions</b>, les experts n'ont pas été en "
        "mesure de formuler de recommandation, faute de données dans la littérature (signalées "
        "explicitement plus bas). Selon le résumé de la source, « 15 experts » ont participé — un "
        "comptage direct des 4 listes nominatives (Experts SFAR, SFCTCV, SFMU, SPLF) donne "
        "toutefois 16 noms : incohérence interne à la source, non reconciliée.",
        S_BODY), bg=BG_PANEL, border=TEAL))
    story.append(Spacer(1, 3*mm))

    story.append(section_bar("Champ 1 — Diagnostic et retentissement des épanchements pleuraux"))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("R1.1", "Privilégier l'échographie pleuro-pulmonaire par rapport à la radiographie "
                 "thoracique pour affirmer ou infirmer le diagnostic d'un épanchement pleural en "
                 "soins critiques, sous réserve de la disponibilité d'un échographe et de "
                 "l'expertise de l'opérateur."),
        ("R1.2", "Réaliser une analyse biochimique, cytologique et bactériologique du liquide "
                 "pleural lors de la première ponction, puis à chaque fois que la cause de "
                 "l'épanchement pourrait avoir changé, pour établir un diagnostic étiologique et "
                 "optimiser la prise en charge thérapeutique."),
        ("R1.3.1", "Ne pas utiliser uniquement des critères quantitatifs basés sur l'imagerie "
                    "pour poser l'indication d'une ponction ou d'un drainage d'un épanchement "
                    "pleural liquidien, pour diminuer la morbi-mortalité."),
        ("R1.3.2", "Utiliser le volume de l'épanchement, le délai précoce et la rapidité "
                    "d'installation, ainsi que la tolérance respiratoire (avec notamment une "
                    "baisse de la compliance thoraco-pulmonaire chez le patient ventilé) pour "
                    "poser l'indication d'une ponction ou d'un drainage et améliorer le rapport "
                    "PaO2/FiO2."),
    ], [16*mm, PAGE_W-2*MARGIN-16*mm-18*mm, 18*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(no_reco_panel(
        "devant l'absence de données dans la littérature, les experts ne sont pas en mesure "
        "d'émettre une recommandation concernant le choix préférentiel d'une évacuation par "
        "drainage ou par ponction d'un épanchement pleural liquidien chez les patients de soins "
        "critiques."))
    return story

def _section_champ2a():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Champ 2 — Procédure de drainage"))
    story.append(Spacer(1, 1.5*mm))
    story.append(P(
        "Un drain ≥ 20 Fr (1 French = 1/3 mm de diamètre interne, soit 24 Fr ≈ 8 mm) est considéré "
        "de gros calibre ; &lt; 20 Fr, de petit calibre. Les drains de petit calibre en « queue de "
        "cochon » (pigtail) sont posés par technique de Seldinger ; les drains de moyen/gros "
        "calibre sont montés sur trocart (drain de Joly) ou introducteur (Figure 1 — photographies "
        "d'équipement, non reproduites ici, cf. texte intégral).", S_NOTE))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("R2.1.1", "Réaliser une échographie pleuro-pulmonaire (au minimum un écho-repérage ; au "
                    "mieux un écho-guidage) pour améliorer la qualité et la sécurité du drainage "
                    "pleural."),
        ("R2.1.2", "Quelle que soit la voie d'abord, faire suivre la ponction et l'insertion du "
                    "drain le bord supérieur de la côte, pour minimiser le risque de lésions "
                    "vasculaires et nerveuses intercostales."),
        ("R2.1.3", "Lorsque les données de l'échographie laissent le choix à plusieurs sites "
                    "d'insertion, privilégier le « triangle de sécurité », pour diminuer la "
                    "morbidité liée à la pose."),
        ("R2.1.4", "Faire réaliser le drainage pleural par des personnes expérimentées lorsque "
                    "les données de l'échographie ne retiennent pas le triangle de sécurité comme "
                    "site possible d'insertion, pour diminuer la morbidité liée à la pose."),
    ], [16*mm, PAGE_W-2*MARGIN-16*mm-18*mm, 18*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(no_reco_panel(
        "devant l'absence de littérature, les experts ne sont pas en mesure d'émettre de "
        "recommandation concernant la position préférentielle du patient (allongée ou demi-assise) "
        "lors de l'évacuation d'un épanchement pleural liquidien, par drainage ou par ponction "
        "évacuatrice, chez les patients de soins critiques."))
    return story

def _section_champ2b():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("R2.2.1", "Ne pas privilégier le drainage percutané par la technique de Seldinger par "
                    "rapport à un drainage par technique chirurgicale, pour diminuer la "
                    "mortalité."),
        ("R2.2.2", "Privilégier le drainage percutané par la technique de Seldinger, pour "
                    "diminuer la douleur."),
        ("R2.3", "Devant l'absence de différence d'efficacité et de sécurité, privilégier un "
                 "drain de petit calibre, pour diminuer la douleur."),
    ], [16*mm, PAGE_W-2*MARGIN-16*mm-18*mm, 18*mm]))
    story.append(Spacer(1, 3*mm))

    story.append(reco_table([
        ("R2.4.1", "Ne pas arrêter les antithrombotiques (anticoagulants ou antiplaquettaires) "
                    "avant de réaliser une ponction pleurale, considérée comme une procédure "
                    "invasive à faible risque hémorragique, pour diminuer la morbi-mortalité."),
        ("R2.4.2", "Suspendre les anticoagulants et les antiplaquettaires anti-P2Y12 (clopidogrel, "
                    "prasugrel, ticagrelor) avant un drainage pleural, considéré comme une "
                    "procédure invasive à haut risque hémorragique, pour diminuer la "
                    "morbi-mortalité. L'aspirine peut être poursuivie."),
        ("R2.4.3", "Lorsque l'urgence ne permet pas un arrêt suffisamment long des "
                    "anticoagulants, discuter au cas par cas de la réversion de l'effet "
                    "anticoagulant avant le drainage, pour diminuer la morbi-mortalité — "
                    "évaluation bénéfice/risque incluant la classe d'anticoagulant, le niveau "
                    "d'anticoagulation (par dosage biologique ou en fonction de la dernière "
                    "administration), la technique de drainage (percutanée vs chirurgicale) et le "
                    "niveau d'expertise de l'opérateur."),
    ], [16*mm, PAGE_W-2*MARGIN-16*mm-18*mm, 18*mm]))
    story.append(Spacer(1, 3*mm))
    story.append(KeepTogether([
        P("<b>TABLEAU</b> — Suggestion de prise en charge des anticoagulants avant drainage pleural", S_H2),
        Spacer(1, 1*mm),
        simple_table(
            ["Anticoagulant", "Délai d'arrêt avant drainage", "Agent de réversion (si indiqué)"],
            [
                ["AVK", "5 jours", "Concentrés de complexe prothrombinique + vitamine K"],
                ["Dabigatran", "4 jours*", "Idarucizumab"],
                ["Apixaban, rivaroxaban", "3 jours", "Concentrés de complexe prothrombinique"],
                ["HNF IVSE curative", "6 heures", "Protamine"],
                ["HNF SC curative", "12 heures", "Protamine"],
                ["HBPM curative", "24 heures*", "Protamine"],
            ], [38*mm, 48*mm, PAGE_W-2*MARGIN-38*mm-48*mm]),
        Spacer(1, 1*mm),
        P("<i>* En l'absence d'insuffisance rénale.</i>", S_NOTE)
    ]))
    story.append(Spacer(1, 2*mm))
    story.append(P(
        "<i>Argumentaire :</i> l'aspirine augmente peu le risque hémorragique, le drainage peut "
        "donc être réalisé sans arrêt. Il est suggéré de ne pas transfuser de plaquettes pour "
        "neutraliser les antiplaquettaires ; en urgence vitale immédiate, il est suggéré de ne pas "
        "attendre la correction de l'hémostase.", S_NOTE))
    return story

def _section_champ2c():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("R2.5", "Ne pas modifier les paramètres ventilatoires lors d'une ponction pleurale ou "
                 "d'un drainage pleural, pour diminuer la morbidité liée à la pose."),
        ("R2.6.1", "Réaliser systématiquement une anesthésie locale lors de la pose d'un drain "
                    "pleural, quelle que soit la technique de pose utilisée, pour diminuer la "
                    "douleur."),
        ("R2.6.2", "Mettre en place une stratégie analgésique adaptée au patient pendant la durée "
                    "du drainage, pour diminuer la douleur."),
        ("R2.6.3", "Réévaluer quotidiennement l'indication du maintien du drain thoracique pour "
                    "permettre de le retirer le plus rapidement possible, et ainsi diminuer la "
                    "douleur liée à sa présence."),
        ("R2.6.4", "Réaliser une analgésie multimodale associée à une infiltration d'anesthésique "
                    "local et/ou à l'application locale de froid, afin de diminuer la douleur lors "
                    "du retrait du drain."),
    ], [16*mm, PAGE_W-2*MARGIN-16*mm-18*mm, 18*mm]))
    story.append(Spacer(1, 4*mm))

    story.append(section_bar("Champ 3 — Surveillance de l'efficacité et des complications"))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("R3.1", "Réaliser systématiquement une radiographie thoracique après le drainage d'un "
                 "épanchement pleural, pour visualiser la bonne position du drain (orientation, "
                 "longueur dans la cavité pleurale) et dépister précocement une complication "
                 "(pneumothorax, hémothorax)."),
        ("R3.2", "Ne pas mettre le drain systématiquement en aspiration, pour diminuer le risque "
                 "de pneumothorax ou accélérer l'évacuation de l'épanchement."),
    ], [16*mm, PAGE_W-2*MARGIN-16*mm-18*mm, 18*mm]))
    return story

def _section_champ4_trace():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Champ 4 — Procédure de retrait des drains"))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("R4.1.1", "Ne pas retirer un drain évacuant plus de 450 mL/24h, pour ne pas augmenter "
                    "la morbidité."),
        ("R4.1.2", "Retirer un drain évacuant moins de 300 mL/24h, pour diminuer la durée de "
                    "drainage thoracique."),
        ("R4.2", "Lorsqu'une imagerie est jugée nécessaire, privilégier l'échographie à la "
                 "radiographie de thorax pour évaluer la vidange pleurale et confirmer "
                 "l'indication de l'ablation du drain."),
        ("R4.3", "Chez un patient en ventilation spontanée, retirer le drain pleural en fin "
                 "d'expiration forcée, afin de diminuer le risque de pneumothorax après le "
                 "retrait."),
    ], [16*mm, PAGE_W-2*MARGIN-16*mm-18*mm, 18*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(no_reco_panel(
        "chez un patient sous ventilation mécanique, les experts ne sont pas en mesure d'émettre "
        "de recommandation concernant le meilleur temps du cycle respiratoire auquel retirer un "
        "drain pour diminuer le risque de pneumothorax après retrait."))
    story.append(Spacer(1, 2*mm))
    story.append(P(
        "<i>Argumentaire :</i> la littérature ne concerne essentiellement que des patients en "
        "ventilation spontanée, et peu de patients sous ventilation mécanique.", S_NOTE))
    story.append(Spacer(1, 4*mm))

    story.append(section_bar("Sources et traçabilité", color=GREY))
    story.append(Spacer(1, 2*mm))
    story.append(P(
        "<b>Document source :</b> « Épanchement pleural liquidien de l'adulte en soins critiques » "
        "— Recommandations pour la Pratique Professionnelle, SFAR, avec SFMU, SPLF, SFCTCV. "
        "Auteurs : B. Bouhemad, C. Arbelot, E. Artaud Macari, L. Brouchet, O. Collange, "
        "M. Froudarakis, A. Godier, S. Hamada, S. Garnier-Kepka, F. Le Pimpec-Barthes, "
        "M.-R. Losser, T. Marx, J. M. Maury, N. Mayeur, F. Remérand, H. Rozé, B. Riu-Poulenc, "
        "M. Jabaudon, H. Charbonneau. Coordonnateur : B. Bouhemad. Organisateurs : H. Charbonneau, "
        "M. Jabaudon. Résumé : 15 experts — un comptage direct des 4 listes nominatives "
        "(SFAR 9, SFCTCV 3, SFMU 2, SPLF 2) donne 16, incohérence interne non reconciliée.",
        S_SOURCE))
    story.append(Spacer(1, 1.5*mm))
    story.append(P("<b>Version :</b> texte validé par le Comité des Référentiels Cliniques de la "
                    "SFAR le 10/04/2023, le CA de la SFAR le 20/04/2023, les CA de la SFCTCV et de "
                    "la SFMU le 21/06/2023, et le CA de la SPLF le 18/07/2023.", S_SOURCE))
    story.append(P("<b>Méthodologie :</b> avis d'experts (méthode GRADE grid pour le vote — RPP, "
                    "aucune recommandation graduée numériquement faute de littérature). Accord "
                    "fort obtenu pour les 25 recommandations après 4 tours de cotation. 3 "
                    "questions sans recommandation formulée (disclosées ci-dessus).", S_SOURCE))
    story.append(P("<b>URL source :</b> https://sfar.org/epanchement-pleural-liquidien-de-ladulte-en-soins-critiques/", S_SOURCE))
    story.append(Spacer(1, 3*mm))
    story.append(info_panel(P(
        "<b>Avertissement :</b> ce document est une fiche de synthèse indépendante, produite pour "
        "un usage d'aide-mémoire. Il reprend l'intégralité des 25 recommandations et des 3 items "
        "« absence de recommandation » de la RPP, mais ne remplace pas le texte intégral "
        "(argumentaire complet, références bibliographiques par recommandation) et n'est ni édité "
        "ni validé par la SFAR, la SFMU, la SPLF ni la SFCTCV. En cas de doute, se référer au texte "
        "intégral et/ou à un avis spécialisé.",
        S_BODY_SM), bg=GREY_LIGHT, border=GREY))
    return story

def _section_a():
    return (_section_intro_champ1() + [Spacer(1, 3*mm)] + _section_champ2a()
            + [Spacer(1, 3*mm)] + _section_champ2b())

def _section_b():
    return _section_champ2c() + [Spacer(1, 4*mm)] + _section_champ4_trace()

SECTIONS = [
    ("Champ 1-2 — Diagnostic, voie d'abord, antithrombotiques", _section_a),
    ("Champ 2-4 — Analgésie, surveillance, retrait", _section_b),
]

def _make_doc():
    return SimpleDocTemplate(OUT, pagesize=A4,
                              leftMargin=MARGIN, rightMargin=MARGIN,
                              topMargin=32*mm, bottomMargin=16*mm,
                              title="Fiche SFAR 2023 - Épanchement pleural liquidien",
                              author="Synthèse indépendante (source SFAR/SFMU/SPLF/SFCTCV)")

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
    import pypdf
    doc = _make_doc()
    doc.build(story_flowables, onFirstPage=_silent_page, onLaterPages=_silent_page)
    return len(pypdf.PdfReader(OUT).pages)

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
