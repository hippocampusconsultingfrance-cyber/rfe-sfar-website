# -*- coding: utf-8 -*-
"""
Fiche de synthese - RPP SFAR (avec SFMU, ADARPEF, CARO, CNCRH, CTSA, EFS,
GFRUP, GIHP, SSA), "Indications de transfusion de plasmas lyophilises
(PLYO) chez un patient en choc hemorragique ou a risque de transfusion
massive en milieu civil (adulte, enfant et nouveau-ne)", 2020. Texte
valide par le Comite des Referentiels Cliniques (16/06/2020) et le CA de
la SFAR (23/06/2020). 28 pages source (dont ~4 pages de contenu clinique
reel + 1 page d'annexe + reste methodologie/bibliographie), telecharge
depuis sfar.org (download/indications-de-transfusion-de-plasmas-
lyophilises-plyo-.../?wpdmdl=30312).

METHODOLOGIE : format RPP (pas RFE) - choix explicitement motive par la
source ("du fait de la tres faible quantite d'etudes repondant... au
critere de jugement majeur... et de la faible qualite methodologique de
ces etudes"). Methodologie GRADE appliquee pour l'analyse de la
litterature (niveau de preuve par reference), mais LA FORCE DE CHAQUE
RECOMMANDATION N'EST PAS un grade 1+/1-/2+/2- individuel : formulation
uniforme "les experts suggerent de faire/ne pas faire", cotation Delphi
(echelle 1-9, GRADE grid, seuil >=70% convergent/<20% divergent). 8
questions cliniques (PICO), 10 enonces gradés individuellement (R1, R2.1,
R2.2, R2.1-Pediatrie, R2.2-Pediatrie, R3, R3-Pediatrie, R4, R5, R6) -
TOUS a "Accord FORT" (verifie par grep exhaustif : aucune autre mention
d'accord dans le texte) - meme convention de chip unique "AE" que
fiche_brule_grave.py/fiche_bris_dentaires.py (aucun grade 1+/2+ invente).
Le decompte officiel de la source ("8 recommandations", section
"Synthese des resultats") correspond aux 8 QUESTIONS/groupes (R1, R2-
adulte, R2-pediatrie, R3-adulte, R3-pediatrie, R4, R5, R6) et non aux 10
enonces gradés individuellement listes ci-dessus (R2 et R3-adulte ont
chacun 2 sous-enonces .1/.2) - pas une incoherence, simple difference de
granularite de comptage, precisee ici pour eviter toute confusion.

PORTEE : couverture complete des 10 enonces gradés (8 questions
cliniques). L'annexe (posologies HAS 2012 de reference + tableau des
objectifs hemodynamiques pediatriques par age) est reproduite
integralement (regle 1). Les modalites administratives detaillees du
circuit PLYO (R6 : commande/transport/stockage/peremption, plusieurs
pages de details reglementaires - references de textes officiels,
mentions obligatoires de l'ordonnance, etc.) sont condensees a l'essentiel
operationnel (regle 7) - le texte integral doit etre consulte pour la
liste exhaustive des mentions reglementaires.

ARGUMENTAIRE : tres fortement condense (regle de projet 2026-09-14) - la
source consacre plusieurs pages d'argumentaire detaille par question
(etudes PAMPer/COMBAT/Pusateri et al. pour R2, etc.) ; seuls les chiffres
et seuils directement actionnables sont conserves (ex: seuil de 20 minutes
de transport, ratio plasma:CGR, volumes en mL/kg), la discussion
statistique/bibliographique detaillee est omise.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from style import *
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.units import mm

OUT = "/home/user/rfe-sfar-website/output/Fiche_SFAR_PLYO_Transfusion_2020.pdf"

SOURCE_TXT = ("Source : « Indications de transfusion de plasmas lyophilisés (PLYO) chez un "
              "patient en choc hémorragique ou à risque de transfusion massive en milieu "
              "civil » — RPP SFAR, 2020. Fiche de synthèse non officielle : se référer au "
              "texte intégral.")

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

RCW = [20 * mm, CW_FULL - 20 * mm - 18 * mm, 18 * mm]

def grid_table(head_row, rows, col_widths, head_bg=NAVY):
    data = [[P(h, S_HEAD_W_C) for h in head_row]]
    for row in rows:
        data.append([P(c, S_CELL) for c in row])
    t = Table(data, colWidths=col_widths, repeatRows=1)
    style_cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), head_bg), ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTNAME", (0, 0), (-1, 0), FONT_BOLD), ("FONTSIZE", (0, 0), (-1, 0), 8),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 0.5, GREY_LIGHT),
        ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            style_cmds.append(("BACKGROUND", (0, i), (-1, i), BG_PANEL))
    t.setStyle(TableStyle(style_cmds))
    return t

def legend_flowable():
    chip_w = 15 * mm
    content_w = CW_FULL
    row = Table([[chip("AE", width=chip_w - 2 * mm),
                  P("Format <b>RPP</b> (Recommandations pour la Pratique Professionnelle), "
                    "pas RFE — cotation Delphi (GRADE grid), formulation uniforme « les "
                    "experts suggèrent ». Toutes les recommandations de ce texte sont à "
                    "<b>Accord fort</b>.", S_BADGE_HEAD)]],
                colWidths=[chip_w, content_w - chip_w])
    row.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                              ("LEFTPADDING", (0, 0), (-1, -1), 1),
                              ("RIGHTPADDING", (0, 0), (-1, -1), 1),
                              ("TOPPADDING", (0, 0), (-1, -1), 0),
                              ("BOTTOMPADDING", (0, 0), (-1, -1), 0)]))
    return row

TOTAL_PAGES = {"n": 4}

def on_page(canvas, doc, page_title):
    header_band(canvas, doc, "SFAR — RPP, 2020",
                "Transfusion de plasmas lyophilisés (PLYO)",
                page_title, icon_fn=lambda c, x, y: icon_drop(c, x, y, 13 * mm), color=RED)
    footer_band(canvas, doc, SOURCE_TXT, f"Page {doc.page} / {TOTAL_PAGES['n']}")

# ---------------------------------------------------------------------------
def _section_all():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Résumé :</b> RPP SFAR (avec SFMU, ADARPEF, CARO, CNCRH, CTSA, EFS, GFRUP, "
        "GIHP, SSA) sur la place du <b>plasma lyophilisé (PLYO)</b>, par rapport au plasma "
        "frais congelé (PFC), chez l'adulte, l'enfant et le nouveau-né en choc "
        "hémorragique ou à risque de transfusion massive, en milieu civil (préhospitalier "
        "et intra-hospitalier). 8 questions cliniques, 10 énoncés gradés, tous "
        "<b>Accord fort</b>.", S_BODY), bg=BG_PANEL, border=TEAL))
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("Méthodologie"))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "Format RPP retenu (et non RFE) du fait de la très faible quantité d'études de "
        "forte puissance sur le critère de mortalité. Analyse de la littérature selon la "
        "méthodologie GRADE, mais formulation uniforme « les experts suggèrent de "
        "faire/de ne pas faire » (pas de grade 1+/1-/2+/2- individuel). Cotation Delphi "
        "(GRADE grid, échelle 1-9) : validée si ≥ 70 % des experts convergent et "
        "&lt; 20 % divergent. <i>Note de comptage :</i> la source annonce « 8 "
        "recommandations » (comptées par question clinique : R1, R2-adulte, "
        "R2-pédiatrie, R3-adulte, R3-pédiatrie, R4, R5, R6) — cette fiche liste les "
        "10 énoncés gradés individuellement ci-dessous (R2 et R3-adulte comportent "
        "chacun 2 sous-énoncés .1/.2), sans divergence réelle de fond, seulement de "
        "granularité de comptage.", S_BODY_SM))
    story.append(Spacer(1, 1.5 * mm))
    story.append(legend_flowable())
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Q1 — Hémorragie sans urgence vitale : PLYO ou PFC ?"),
        Spacer(1, 1.5 * mm),
        reco_table([
            ("R1", "Pour une hémorragie sans urgence vitale nécessitant une transfusion "
             "de plasma, les experts suggèrent d'utiliser des PFC."),
        ], RCW),
    ]))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>Repères :</b> le PLYO reste une alternative si le PFC n'est pas disponible "
        "(opération extérieure isolée, transport long vers une structure d'hémostase). "
        "Volume initial usuel de plasma : 10-15 mL/kg, guidé par le TQ (saignement "
        "anormal possible si TQ ≥ 1,5-1,8× témoin, soit TP &lt; 40 %) et la clinique.",
        S_BODY_SM))
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Q2 — Transports médicalisés (préhospitalier)"),
        Spacer(1, 1.5 * mm),
        reco_table([
            ("R2.1", "Chez l'adulte, au cours des transports médicalisés, transfusion de "
             "2 à 4 PLYO uniquement dans le cadre d'une activation d'un protocole de "
             "transfusion massive et lorsque la durée de transport vers le centre "
             "hospitalier le plus adapté est &gt; 20 min."),
            ("R2.2", "Dans cette indication chez l'adulte, transfusion de 2 à 4 PLYO "
             "seuls ou avec des concentrés de globules rouges (CGR) si disponibles "
             "immédiatement."),
            ("R2.1 (Pédiatrie)", "Par analogie avec l'adulte, transfusion initiale de "
             "10-15 mL/kg de PLYO chez l'enfant/nourrisson, si hémorragie nécessitant "
             "un protocole de transfusion massive, en particulier si le centre "
             "hospitalier adapté n'est pas à proximité."),
            ("R2.2 (Pédiatrie)", "Dans cette indication, transfusion initiale de "
             "10-15 mL/kg de PLYO seuls ou avec CGR si disponibles immédiatement."),
        ], RCW),
    ]))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>Repères :</b> chaque vecteur (véhicule/hélicoptère) doté de 4 unités de "
        "PLYO conservées à température ambiante (reconstitution en 6 min, isogroupe — "
        "4 unités = 840 mL de plasma). Avantage logistique net sur le PFC en contexte "
        "extrahospitalier.", S_BODY_SM))
    return story

def _section_intra_hospitalier():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("Q3 — Transfusion intra-hospitalière"))
    story.append(Spacer(1, 1.5 * mm))
    story.append(reco_table([
        ("R3", "Chez tout adulte en choc hémorragique nécessitant l'activation d'un "
         "protocole de transfusion massive, débuter <b>immédiatement</b> la transfusion "
         "de 2 à 4 PLYO, dans un ratio plasma:CGR ≥ 1:2, dans l'attente de plasma "
         "décongelé disponible."),
        ("R3 (Pédiatrie)", "Chez tout enfant/nourrisson en choc hémorragique nécessitant "
         "l'activation d'un protocole de transfusion massive, débuter immédiatement la "
         "transfusion de 10-15 mL/kg de PLYO, dans un ratio plasma:CGR ≥ 1:2, dans "
         "l'attente de plasma décongelé disponible."),
    ], RCW))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>Repères pédiatriques :</b> packs de PSL (ex. 1 CGR + 1 PFC + 2 concentrés "
        "plaquettaires) selon le poids — &lt; 10 kg = 1 pack, 10-30 kg = 2 packs, "
        "&gt; 30 kg = 3 packs, ratio PFC:CGR entre 1:2 et 1:1.", S_BODY_SM))
    story.append(Spacer(1, 2.5 * mm))
    story.append(section_bar("Q4 — Hémorragie du péripartum (HPP)"))
    story.append(Spacer(1, 1.5 * mm))
    story.append(reco_table([
        ("R4", "En cas d'activation d'un protocole de transfusion massive lors d'une HPP "
         "et/ou de catastrophe obstétricale avec coagulopathie, recourir à la "
         "transfusion de plasma en complément de CGR — le choix entre PLYO ou PFC est "
         "guidé par des raisons logistiques, notamment de disponibilité immédiate."),
    ], RCW))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>Repères :</b> l'HPP est la 1<sup>re</sup> cause de mortalité maternelle. La "
        "plupart des HPP de volume intermédiaire (&lt; 2500 mL ou &lt; 150 mL/10 min) se "
        "résolvent par utérotoniques + acide tranexamique ± fibrinogène + 1-2 CGR. Au-"
        "delà de 2500 mL, une coagulopathie obstétricale aiguë (fibrinogénolyse/"
        "fibrinolyse) est possible. Aucune donnée spécifique PLYO dans l'HPP à ce "
        "jour — le choix PLYO/PFC reste une question logistique, non tranchée sur le "
        "fond par la littérature.", S_BODY_SM))
    story.append(Spacer(1, 2.5 * mm))
    story.append(section_bar("Q5 — Examens biologiques et règles transfusionnelles"))
    story.append(Spacer(1, 1.5 * mm))
    story.append(reco_table([
        ("R5", "Réaliser un bilan d'immuno-hématologie pré-transfusionnel (phénotypage "
         "érythrocytaire + recherche d'anticorps anti-érythrocytaire, à la pose du "
         "premier abord veineux) systématique avant toute transfusion de PSL y compris "
         "de PLYO, si aucun résultat n'est disponible immédiatement."),
    ], RCW))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>Repères :</b> le PLYO est un PSL soumis à la réglementation transfusionnelle "
        "standard ; il peut être délivré avant les résultats immuno-hématologiques en "
        "urgence vitale immédiate et ne perturbe pas un groupage sanguin. Précautions "
        "identiques au PFC-IA (antécédent d'allergie à l'amotosalen/psoralènes → ne pas "
        "re-transfuser avant exploration complémentaire).", S_BODY_SM))
    return story

def _section_circuit_annexe_sources():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("Q6 — Circuit du PLYO (commande, stockage, péremption)"))
    story.append(Spacer(1, 1.5 * mm))
    story.append(reco_table([
        ("R6", "Le PLYO étant un PSL, il répond aux mêmes règles de circuit que les "
         "autres PSL (prescription, transport, stockage, traçabilité)."),
    ], RCW))
    story.append(Spacer(1, 1.5 * mm))
    story.append(grid_table(
        ["Étape", "Points clés (condensés — voir texte intégral pour le détail réglementaire complet)"],
        [
            ["Prescription", "Ordonnance PSL pré-imprimée : identité patient, "
             "établissement/service, date, prescripteur, nombre de PLYO, degré "
             "d'urgence (urgence vitale immédiate), indication (hémorragie massive), "
             "date/heure de transfusion."],
            ["Stockage", "À l'abri de la lumière, dans l'emballage d'origine, entre "
             "+2 °C et +25 °C, durée maximale 2 ans après lyophilisation."],
            ["Reconstitution", "Addition de 200 ou 250 mL d'eau pour préparation "
             "injectable ; complète en &lt; 6 min. Utilisation immédiate, au plus tard "
             "dans les 6 heures suivant reconstitution."],
            ["Après transfusion", "Flacon + dispositif de perfusion clampé conservés "
             "≥ 2 h après transfusion (procédure de l'établissement)."],
            ["Péremption", "Gérée par le site de délivrance (CTSA, EFS ou dépôt) ; "
             "produits périmés non repris, à charge du site de délivrance — prévoir une "
             "utilisation hors urgence avant péremption vu le coût du PLYO."],
        ], [30 * mm, CW_FULL - 30 * mm], head_bg=GREY))
    story.append(Spacer(1, 2.5 * mm))
    story.append(section_bar("Annexe — Posologies de référence (HAS 2012) et objectifs "
                              "hémodynamiques pédiatriques"))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>Adultes :</b> transfuser le plasma en association aux CGR, ratio PFC:CGR "
        "entre 1:2 et 1:1 (grade C). L'initiation sans délai nécessite des protocoles de "
        "transfusion massive dans les centres concernés (grade C). Posologie initiale "
        "usuelle : 15 mL/kg (accord professionnel), à augmenter si saignement majeur, "
        "répétition guidée par la réévaluation clinico-biologique.", S_BODY_SM))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>Enfants/nouveau-nés :</b> attitude calquée sur l'adulte (choix retenu dès "
        "l'actualisation HAS 2012), posologies adaptées au poids. Volume sanguin de "
        "référence : prématuré 90-100 mL/kg, nouveau-né à terme &lt; 3 mois "
        "80-90 mL/kg, enfant &gt; 3 mois 70 mL/kg.", S_BODY_SM))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P("<b>Tableau — Objectifs hémodynamiques pédiatriques par âge "
                    "(limites) :</b>", S_BODY_SM))
    story.append(Spacer(1, 1 * mm))
    story.append(grid_table(
        ["Âge", "FR (limite sup.)", "FC (limite sup.)", "PAS (limite inf.)", "PAM (limite inf.)"],
        [
            ["1 mois", "35 (55)", "120 (175)", "60 (50)", "45 (35)"],
            ["1 an", "30 (40)", "110 (170)", "80 (70)", "55 (40)"],
            ["2 ans", "25 (30)", "100 (160)", "90 + 2×âge", "55 + 1,5×âge"],
            ["6 ans", "20 (25)", "90 (130)", "90 + 2×âge", "55 + 1,5×âge"],
            ["12 ans", "15 (20)", "80 (100)", "120 (90)", "80 (65)"],
        ], [22 * mm] + [(CW_FULL - 22 * mm) / 4.0] * 4))
    story.append(Spacer(1, 1 * mm))
    story.append(P("<i>FR : fréquence respiratoire (/min) ; FC : fréquence cardiaque "
                    "(/min) ; PAS/PAM en mmHg. Valeurs entre parenthèses : secondes "
                    "limites indiquées par la source.</i>", S_NOTE))
    story.append(Spacer(1, 2.5 * mm))
    story.append(section_bar("Sources et traçabilité", color=GREY))
    story.append(Spacer(1, 2 * mm))
    story.append(P(
        "<b>Document source :</b> « Indications de transfusion de plasmas lyophilisés "
        "(PLYO) chez un patient en choc hémorragique ou à risque de transfusion "
        "massive en milieu civil (adulte, enfant et nouveau-né) » — RPP SFAR, avec "
        "SFMU, ADARPEF, CARO, CNCRH, CTSA, EFS, GFRUP, GIHP, SSA. Texte validé par le "
        "Comité des Référentiels Cliniques (16/06/2020) et le CA de la SFAR "
        "(23/06/2020).", S_SOURCE))
    story.append(Spacer(1, 1 * mm))
    story.append(P("<b>Méthodologie :</b> analyse GRADE de la littérature, formulation "
                    "RPP (« les experts suggèrent »), cotation Delphi GRADE grid — voir "
                    "détail en page 1.", S_SOURCE))
    story.append(Spacer(1, 1 * mm))
    story.append(P(
        "<b>URL source :</b> https://sfar.org/download/indications-de-transfusion-de-"
        "plasmas-lyophilises-plyo-chez-un-patient-en-choc-hemorragique-ou-a-risque-de-"
        "transfusion-massive-en-milieu-civil-adulte-enfant-et-nouveau-ne/?wpdmdl=30312",
        S_SOURCE))
    story.append(Spacer(1, 1 * mm))
    story.append(P(
        "<b>Couverture :</b> intégralité des 10 énoncés gradés (8 questions cliniques) "
        "et de l'annexe (posologies HAS 2012, objectifs hémodynamiques pédiatriques). "
        "Le circuit réglementaire détaillé du PLYO (R6) est condensé aux points "
        "opérationnels — voir texte intégral pour la liste exhaustive des mentions "
        "réglementaires obligatoires.", S_SOURCE))
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Avertissement — document validé 2020 :</b> cette fiche de synthèse "
        "indépendante reprend l'intégralité du contenu actionnable du texte source, "
        "mais ne le remplace pas et n'est ni éditée ni validée par la SFAR. Se référer "
        "aux protocoles locaux et aux textes réglementaires en vigueur (susceptibles "
        "d'évoluer) avant toute décision transfusionnelle.", S_BODY_SM),
        bg=GREY_LIGHT, border=GREY))
    return story

SECTIONS = [
    ("Méthodologie, hémorragie sans urgence vitale & transports", _section_all),
    ("Transfusion intra-hospitalière, HPP & règles transfusionnelles", _section_intra_hospitalier),
    ("Circuit du PLYO, annexe & sources", _section_circuit_annexe_sources),
]

def _make_doc(path=None):
    return SimpleDocTemplate(path or OUT, pagesize=A4,
                              leftMargin=MARGIN, rightMargin=MARGIN,
                              topMargin=32 * mm, bottomMargin=16 * mm,
                              title="Fiche SFAR 2020 - PLYO transfusion en urgence",
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

    doc = _make_doc()
    story = _build_upto(fns)
    doc.build(story, onFirstPage=on_page_final, onLaterPages=on_page_final)
    print("OK ->", OUT, f"({total_pages} pages)")

if __name__ == "__main__":
    build()
