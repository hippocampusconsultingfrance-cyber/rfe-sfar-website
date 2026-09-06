# -*- coding: utf-8 -*-
"""
Fiche de synthese - RFE SFAR (en collaboration SNFGE/SFR/SFNCM/SFED) 2021
"Pancreatite aigue grave du patient adulte en soins critiques". Source :
sources/pancreatite.pdf (48 pages), sources/pancreatite.txt (texte extrait,
2253 lignes). Pas de tampon d'obsolescence detecte a la lecture integrale de
la page 1 et du sommaire ; library_final.json marque ce document
"en vigueur", exact_date "2021-09-25" (coherent avec le texte validation CA
SFAR 30/06/2021, CA SFED 10/09/2021, CA SFNC 09/09/2021).

METHODOLOGIE - GRADE (1+/1-/2+/2-) + avis d'experts + "absence de
recommandation" quand la litterature ne permet pas de trancher. 14 questions
PICO reparties en 3 champs, 24 recommandations au total (verifie par grep
exhaustif 'GRADE [12][+-] \\(Accord' sur le texte source, en tenant compte
d'un tag GRADE 2+ de R3.4 precede d'un espace au debut de ligne qu'un grep
naif ancre '^GRADE' ne detecte pas -- 20 enonces GRADE-tagues + 4 avis
d'experts = 24, cf. R1.1/R1.2.1/R1.2.2/R1.3 (champ 1), R2.1-R2.11 (champ 2),
R3.1/R3.2/R3.3/R3.4/R3.5.1/R3.5.2/R3.6.1/R3.6.2/R3.7 (champ 3)).

DISCLOSURE - INCOHERENCE INTERNE A LA SOURCE sur la repartition des niveaux
de preuve : le RESUME francais (ligne 99-100) ET l'ABSTRACT anglais (ligne
133-134) annoncent tous deux "8 GRADE 1+/-, 12 GRADE 2+/-" -- ce qui
correspond exactement au tally direct des 20 enonces GRADE-tagues du corps
du texte (6x 1+, 2x 1-, 6x 2+, 6x 2- = 8 et 12). Mais la section "2.2
Recommandations" du corps du texte (ligne 325-326) annonce l'inverse : "9
GRADE 1+/-, 11 GRADE 2+/-". Les deux comptes internes a la source ne
concordent pas entre eux ; cette fiche affiche le compte verifie par tally
direct (8/12, coherent avec les 2 resumes) et signale explicitement le
chiffre alternatif donne par le corps du texte, sans trancher laquelle des
deux sources est "la bonne".

DISCLOSURE #2 - incoherence mineure supplementaire, confirmee par l'audit independant
(sous-agent aveugle au brouillon) : la note de bas de Tableau 1 sur l'estimation de la
FiO2 chez le patient non ventile attribue le meme debit "2 l/min d'oxygene" a la fois a
25% et a 30% ("...a 25% (sous 2 l/min d'oxygene), a 30% sous 2 l/min d'oxygene...") --
tres probablement un artefact d'extraction PDF->texte (un debit distinct, ex. 1 l/min
pour les 25%, a probablement ete perdu), mais reproduit tel quel avec un [sic] plutot
que de deviner/corriger silencieusement le debit manquant.

PERIMETRE - integralite des 3 champs (evaluation/admission ; phase initiale ;
complications evolutives), 24 recommandations + 4 questions sans
recommandation possible, Tableau 1 (score de Marshall modifie) reproduit
verbatim, Figure 1 (algorithme diagnostic/orientation, image pure sans
couche texte a la page 46 du PDF source, verifiee par rendu PyMuPDF
200dpi -- build/pancr_fig1.png) retranscrite fidelement sous forme de
boites/fleches vectorielles (pas de fleches courbes disponibles dans le
kit style.py de ce corpus : aucune fiche precedente ne dessine de vraies
fleches vectorielles, cf. grep 'drawCurve|arrow' sur build/*.py -- toutes
reproduisent le contenu des algorithmes sous forme de blocs textuels
structures), et Annexe 1 (criteres/scores BISAP, SIRS, Ranson, Balthazar,
CTSI) reproduite integralement. Argumentaires (revue de litterature,
references bibliographiques) condenses en une phrase de justification
clinique par recommandation, non reproduits in extenso (comme dans toutes
les fiches GRADE precedentes de ce corpus, ex. fiche_transfusion_plasma.py).

ICONE : icon_shield (etat critique aigu), deja utilisee pour
fiche_asthme_aigu_grave.py -- pas d'icone pancreas/digestif dediee dans
style.py (5 icones seulement : kidney/shield/pill/liver/drop).

_count_pages() : copie exacte du pattern fiche_aap_programmee.py, passes de
comptage vers un tempfile.mktemp() jetable, jamais vers OUT.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from style import *
from style import _c
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
                                 PageBreak, KeepTogether)
from reportlab.lib.units import mm

GRADE_COLORS["AE"] = (GREY, WHITE)
GRADE_COLORS["SR"] = (GREY_LIGHT, INK)

OUT = "/home/user/rfe-sfar-website/output/Fiche_SFAR_Pancreatite_Aigue_Grave_2021.pdf"

SOURCE_TXT = ("Source : RFE SFAR, en collaboration avec SNFGE, SFR, SFNCM, SFED — « Pancréatite "
              "aigüe grave du patient adulte en soins critiques » (2021). Fiche de synthèse non "
              "officielle : se référer au texte intégral.")

def P(txt, style=S_CELL):
    return Paragraph(txt, style)

def chip(label, **kw):
    return grade_chip(label, **kw)

GRADE_W = 20 * mm

def reco_table(rows, col_widths=None):
    """rows: (ref, text, grade_label) - grade_label parmi '1+','1-','2+','2-','AE','SR'."""
    ref_w = 13 * mm
    text_w = PAGE_W - 2 * MARGIN - ref_w - GRADE_W
    cw = col_widths or [ref_w, text_w, GRADE_W]
    data = [[P("Réf.", S_HEAD_W_C), P("Recommandation (texte condensé, fidèle à la source)", S_HEAD_W),
             P("Niveau", S_HEAD_W_C)]]
    for ref, txt, grade in rows:
        data.append([P(ref, S_CELL_B), P(txt, S_CELL), chip(grade, width=GRADE_W - 2 * mm)])
    t = Table(data, colWidths=cw, repeatRows=1)
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

def simple_table(header, rows, col_widths, small=False):
    hstyle = S_HEAD_W
    data = [[P(h, hstyle) for h in header]] + [[P(c, S_CELL if not small else S_BODY_SM) for c in row] for row in rows]
    t = Table(data, colWidths=col_widths, repeatRows=1)
    style_cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), NAVY), ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTNAME", (0, 0), (-1, 0), FONT_BOLD), ("FONTSIZE", (0, 0), (-1, 0), 8),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("ALIGN", (1, 0), (-1, -1), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 0.5, GREY_LIGHT),
        ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            style_cmds.append(("BACKGROUND", (0, i), (-1, i), BG_PANEL))
    t.setStyle(TableStyle(style_cmds))
    return t

def flow_box(text, bg=BG_PANEL, border=TEAL, width=None):
    st = pstyle("flowbox", base=S_BODY_SM, alignment=TA_LEFT)
    w = width or (PAGE_W - 2 * MARGIN)
    t = Table([[Paragraph(text, st)]], colWidths=[w])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), bg),
        ("BOX", (0, 0), (-1, -1), 1, border),
        ("TOPPADDING", (0, 0), (-1, -1), 3 * mm), ("BOTTOMPADDING", (0, 0), (-1, -1), 3 * mm),
        ("LEFTPADDING", (0, 0), (-1, -1), 3.5 * mm), ("RIGHTPADDING", (0, 0), (-1, -1), 3.5 * mm),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    return t

def arrow_row(labels=None):
    """Petite ligne de fleches verticales (texte) pour relier les etapes de l'algorithme."""
    st = pstyle("arrow", base=S_H2, alignment=TA_CENTER, fontSize=13)
    if labels is None:
        labels = ["↓"]
    w = (PAGE_W - 2 * MARGIN) / len(labels)
    t = Table([[Paragraph(l, st) for l in labels]], colWidths=[w] * len(labels))
    t.setStyle(TableStyle([("TOPPADDING", (0, 0), (-1, -1), 0), ("BOTTOMPADDING", (0, 0), (-1, -1), 0)]))
    return t

TOTAL_PAGES = {"n": 8}

def on_page(canvas, doc, page_title):
    header_band(canvas, doc, "SFAR / SNFGE / SFR / SFNCM / SFED — RFE 2021 — FICHE DE SYNTHÈSE",
                "Pancréatite aigüe grave en soins critiques",
                page_title, icon_fn=lambda c, x, y: icon_shield(c, x, y, 13 * mm), color=NAVY)
    footer_band(canvas, doc, SOURCE_TXT, f"Page {doc.page} / {TOTAL_PAGES['n']}")

# ---------------------------------------------------------------------------
def _section_intro():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Champ :</b> prise en charge du patient adulte de soins critiques (réanimation, "
        "surveillance continue, soins intensifs) présentant une pancréatite aigüe grave. RFE "
        "SFAR 2021, en collaboration avec la SNFGE, la SFR, la SFNCM et la SFED, actualisant les "
        "précédentes recommandations françaises (SFAR/CNGOF 2001). 14 questions PICO réparties "
        "en 3 champs, méthode GRADE® : <b>24 recommandations</b> formalisées (accord fort pour "
        "100 % d'entre elles après 1 à 2 tours de cotation) + 4 questions pour lesquelles aucune "
        "recommandation n'a pu être émise faute de données.", S_BODY), bg=BG_PANEL, border=TEAL))
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Méthodologie GRADE® :</b> qualité des preuves Haute/Modérée/Basse/Très basse → force "
        "de recommandation binaire, positive ou négative, Forte (<b>GRADE 1+/1-</b> : « il est "
        "recommandé/il n'est pas recommandé ») ou Faible (<b>GRADE 2+/2-</b> : « il est/n'est "
        "probablement pas recommandé »). Quand la méthode GRADE ne s'applique pas : <b>avis "
        "d'experts</b> (chip « AE »), validé à &gt;70 % d'accord. Quand aucune réponse n'a pu être "
        "apportée : <b>« absence de recommandation »</b> (chip « SR »). "
        "<b>Incohérence interne à la source, non résolue silencieusement :</b> le résumé français "
        "et l'abstract anglais du document annoncent tous deux « 8 recommandations de niveau "
        "GRADE 1+/-, 12 de niveau GRADE 2+/- » — chiffre qui correspond exactement au tally direct "
        "des 20 énoncés GRADE-tagués du corps du texte (6×1+, 2×1-, 6×2+, 6×2-). Mais la section "
        "« 2.2 Recommandations » du même document annonce l'inverse : « 9 GRADE 1+/-, 11 GRADE "
        "2+/- ». Cette fiche retient le compte vérifié par tally direct (8/12), cohérent avec les "
        "deux résumés, sans trancher laquelle des deux mentions internes de la source est erronée.",
        S_BODY_SM), bg=BG_PANEL, border=AMBER))
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("Contexte et définitions"))
    story.append(Spacer(1, 2 * mm))
    story.append(P(
        "Prévalence ≈ 15 000 cas/an en France. Dans 80-90 % des cas, pancréatite aigüe "
        "œdémateuse interstitielle, de gravité modérée. Dans 10-20 % des cas : forme grave, "
        "pouvant nécessiter une prise en charge en soins critiques. <b>Classification révisée "
        "d'Atlanta</b> : pancréatite peu grave (absence de défaillance d'organe et de "
        "complication locale/systémique), modérément grave (défaillance d'organe transitoire "
        "ou complication locale/exacerbation d'une maladie préexistante), <b>grave</b> "
        "(défaillance d'organe <b>persistante &gt; 48 h</b>). Complications locales : collections "
        "liquidiennes, nécrose pancréatique/péri-pancréatique, pseudokyste, hémorragie. "
        "Étiologies : lithiasique (40-50 %), alcool (20-30 %), hypercalcémie, "
        "hypertriglycéridémie, médicamenteuse, post-CPRE (2-20 %), indéterminée (10-25 %).",
        S_BODY_SM))
    return story

# ---------------------------------------------------------------------------
def _section_champ1():
    story = []
    story.append(Spacer(1, 2 * mm))
    story.append(section_bar("CHAMP 1 — Évaluation et admission en soins critiques"))
    story.append(Spacer(1, 2 * mm))
    story.append(reco_table([
        ("R1.1", "Décider de l'admission en soins critiques sur la présence d'une pancréatite "
         "aigüe grave (défaillance(s) d'organe(s) cardiovasculaire/respiratoire/rénale, avec ou "
         "sans nécrose infectée) ou jugée à risque de le devenir après évaluation "
         "multidisciplinaire — aucun score isolé ne peut à ce jour être recommandé pour cette "
         "décision.", "2+"),
        ("R1.2.1", "En cas de doute diagnostique après anamnèse/examen clinique/lipasémie, ou en "
         "l'absence de réponse au traitement ou d'aggravation clinique : réaliser un scanner "
         "abdomino-pelvien le plus tôt possible pour confirmer le diagnostic positif.", "1+"),
        ("R1.2.2", "Réaliser le plus rapidement possible : bilan hépatique (ASAT, ALAT, γGT, PAL, "
         "bilirubine), triglycéridémie, calcémie et échographie abdominale, pour préciser le "
         "diagnostic étiologique.", "1+"),
        ("R1.3", "Chez le patient ventilé de façon invasive : monitorer la pression "
         "intra-abdominale pour diagnostiquer et traiter précocement une hypertension "
         "intra-abdominale (retrouvée chez plus de la moitié des patients, facteur de "
         "mortalité indépendant).", "1+"),
    ]))
    story.append(Spacer(1, 3 * mm))

    story.append(KeepTogether([
        P("<b>Tableau 1 — Score modifié de Marshall</b> (définit les défaillances d'organe ; "
          "score ≥ 2 pour un organe = défaillance de cet organe)", S_H2),
        Spacer(1, 1.5 * mm),
        simple_table(
            ["Organe", "0", "1", "2", "3", "4"],
            [
                ["Poumon (PaO2/FiO2*)", ">400", "301-400", "201-300", "101-200", "≤100"],
                ["Rein (créatininémie, µmol/L)", "≤134", "134-169", "170-310", "311-439", ">439"],
                ["Cardiovasculaire (PAS, mmHg**)", ">90", "<90, répond au\nremplissage",
                 "<90, ne répond pas\nau remplissage", "<90, pH<7,3", "<90, pH<7,2"],
            ],
            [ (PAGE_W - 2*MARGIN) * w for w in (0.30, 0.14, 0.16, 0.16, 0.12, 0.12) ]),
        Spacer(1, 1 * mm),
        P("*Patient non ventilé : FiO2 estimée à 21 % (air ambiant), 25 % sous 2 L/min "
          "d'O2, <b>30 % sous 2 L/min d'O2 (sic — le texte source répète le même débit pour "
          "25 % et 30 %, incohérence non résolue silencieusement ici)</b>, 40 % sous "
          "6-8 L/min, 50 % sous 9-10 L/min. **Sans amines.", S_NOTE),
    ]))
    story.append(Spacer(1, 3 * mm))

    story.append(KeepTogether([
        P("<b>Figure 1 — Éléments du diagnostic positif, étiologique, des modalités "
          "d'hospitalisation et de la surveillance précoce d'une pancréatite aigüe grave</b> "
          "(algorithme, transcrit fidèlement depuis la source — image pure page 46, aucune "
          "couche texte)", S_H2),
        Spacer(1, 2 * mm),
        flow_box("<b>Suspicion de pancréatite aigüe (PA) grave</b>", bg=GREY_LIGHT, border=GREY),
        arrow_row(["↓", "↓"]),
    ]))
    story.append(Table(
        [[flow_box("<b>Diagnostic positif</b><br/>• Douleurs abdominales typiques<br/>"
                    "• Lipasémie &gt;3N<br/>• Scanner abdomino-pelvien si : doute diagnostique, "
                    "ou absence de réponse aux traitements et/ou aggravation clinique",
                    bg=_c(219, 230, 242), border=NAVY, width=(PAGE_W - 2*MARGIN - 4*mm) / 2),
          flow_box("<b>Diagnostic étiologique</b> (le plus rapidement possible)<br/>"
                    "• Bilan hépatique (ASAT, ALAT, γGT, PAL, bilirubine)<br/>• Triglycéridémie<br/>"
                    "• Calcémie<br/>• Échographie abdominale",
                    bg=AMBER_LIGHT, border=AMBER, width=(PAGE_W - 2*MARGIN - 4*mm) / 2)]],
        colWidths=[(PAGE_W - 2*MARGIN) / 2, (PAGE_W - 2*MARGIN) / 2],
        style=TableStyle([("LEFTPADDING", (0,0), (-1,-1), 0), ("RIGHTPADDING", (0,0), (-1,-1), 4*mm),
                           ("VALIGN", (0,0), (-1,-1), "TOP")])))
    story.append(arrow_row(["↓", "↓"]))
    story.append(flow_box(
        "<b>Diagnostic de sévérité</b><br/>• Défaillances d'organes<br/>• Évaluation "
        "multidisciplinaire du risque d'aggravation secondaire (Annexe 1), selon des critères "
        "clinico-biologiques et des critères radiologiques (scanner au moins 48-72 h après "
        "l'hospitalisation)", bg=_c(250, 224, 200), border=AMBER))
    story.append(arrow_row(["↓  OUI", "NON  ↓"]))
    story.append(Table(
        [[flow_box("<b>Surveillance renforcée en unité de soins critiques</b> (incluant "
                    "monitorage de la pression intra-abdominale si possible)",
                    bg=GREY_LIGHT, border=GREY, width=(PAGE_W - 2*MARGIN - 4*mm) / 2),
          flow_box("<b>Surveillance dans une unité conventionnelle</b>",
                    bg=GREY_LIGHT, border=GREY, width=(PAGE_W - 2*MARGIN - 4*mm) / 2)]],
        colWidths=[(PAGE_W - 2*MARGIN) / 2, (PAGE_W - 2*MARGIN) / 2],
        style=TableStyle([("LEFTPADDING", (0,0), (-1,-1), 0), ("RIGHTPADDING", (0,0), (-1,-1), 4*mm),
                           ("VALIGN", (0,0), (-1,-1), "TOP")])))
    return story

# ---------------------------------------------------------------------------
def _section_champ2():
    story = []
    story.append(Spacer(1, 2 * mm))
    story.append(section_bar("CHAMP 2 — Prise en charge à la phase initiale"))
    story.append(Spacer(1, 2 * mm))

    story.append(P("<b>Hémodynamique</b>", S_H2))
    story.append(Spacer(1, 1.5 * mm))
    story.append(reco_table([
        ("R2.1", "Ne pas utiliser systématiquement une stratégie de remplissage vasculaire massif "
         "(3-5 mL/kg/h pendant les premières 24 h) : pas de bénéfice démontré sur la mortalité, "
         "et risque accru d'insuffisance rénale aigüe (méta-analyse, RR 2,17).", "2-"),
    ]))
    story.append(Spacer(1, 3 * mm))

    story.append(P("<b>Respiratoire</b>", S_H2))
    story.append(Spacer(1, 1.5 * mm))
    story.append(reco_table([
        ("R2.2", "Ne pas utiliser de probiotiques par voie entérale pour réduire la mortalité ou "
         "les pneumonies associées aux soins (l'unique essai randomisé disponible montre une "
         "surmortalité et un excès d'ischémie mésentérique sous probiotiques).", "2-"),
        ("—", "Aucune recommandation possible sur la ventilation non-invasive, l'oxygénothérapie "
         "à haut débit, la stratégie de ventilation mécanique invasive ou la stratégie de "
         "sédation pour prévenir les complications respiratoires (absence d'étude).", "SR"),
    ]))
    story.append(Spacer(1, 3 * mm))

    story.append(P("<b>Nutrition</b>", S_H2))
    story.append(Spacer(1, 1.5 * mm))
    story.append(reco_table([
        ("R2.3", "Utiliser une nutrition entérale plutôt qu'une nutrition parentérale exclusive "
         "(réduction de mortalité démontrée par plusieurs méta-analyses, y compris dans les "
         "formes graves).", "1+"),
        ("R2.4", "Ne pas introduire systématiquement une nutrition entérale précoce (24-48 "
         "premières heures) dans le seul but de réduire la mortalité, les infections ou les "
         "défaillances d'organes — bénéfice non démontré sur ces critères pris isolément.", "1-"),
        ("R2.5", "Ne pas recourir en première intention à une sonde naso-jéjunale pour améliorer "
         "la tolérance de la nutrition entérale (pas de différence vs sonde naso-gastrique) ; "
         "réserver la voie jéjunale à l'impossibilité de la voie gastrique.", "1-"),
        ("R2.6", "Ne pas privilégier les mélanges semi-élémentaires/élémentaires, ni "
         "l'immunonutrition entérale, par rapport à une nutrition entérale polymérique "
         "standard.", "2-"),
        ("R2.7", "En cas d'intolérance avérée ou de contre-indication à la nutrition entérale : "
         "ajouter de la glutamine IV (0,20 g/kg/j de L-glutamine) à la nutrition parentérale.", "2+"),
        ("R2.8", "Ne pas utiliser d'antioxydants en complément de la nutrition entérale ou "
         "parentérale.", "2-"),
    ]))
    story.append(Spacer(1, 3 * mm))

    story.append(P("<b>Prise en charge interventionnelle médico-chirurgicale en urgence</b>", S_H2))
    story.append(Spacer(1, 1.5 * mm))
    story.append(reco_table([
        ("R2.9", "Pancréatite biliaire : ne réaliser une CPRE en urgence que chez les patients "
         "avec angiocholite associée — pas de bénéfice démontré d'une CPRE systématique en "
         "l'absence d'angiocholite (essai APEC notamment).", "1+"),
    ]))
    story.append(Spacer(1, 3 * mm))

    story.append(P("<b>Thérapeutiques non conventionnelles</b>", S_H2))
    story.append(Spacer(1, 1.5 * mm))
    story.append(reco_table([
        ("R2.10", "Ne pas utiliser de thérapeutique médicamenteuse non conventionnelle (aucune "
         "des nombreuses molécules testées — aprotinine, gabexate, octréotide, somatostatine, "
         "lexipafant, etc. — ne réduit la mortalité).", "2-"),
        ("R2.11", "Pancréatite hypertriglycéridémique en échec du traitement médical de 1<sup>re</sup> "
         "intention (fibrate, héparine + insuline) : envisager des échanges plasmatiques pour "
         "réduire rapidement une hypertriglycéridémie sévère (&gt;11,3 mmol/L) ou très sévère "
         "(&gt;22,4 mmol/L), objectif &lt;5,7 mmol/L.", "AE"),
    ]))
    story.append(Spacer(1, 3 * mm))

    story.append(P("<b>Antalgie</b>", S_H2))
    story.append(Spacer(1, 1.5 * mm))
    story.append(reco_table([
        ("—", "Aucune donnée ne permet de recommander un type d'analgésie particulier "
         "(morphiniques, anesthésiques locaux IV, AINS, paracétamol, péridurale) pour réduire "
         "la morbi-mortalité.", "SR"),
    ]))
    return story

# ---------------------------------------------------------------------------
def _section_champ3():
    story = []
    story.append(Spacer(1, 2 * mm))
    story.append(section_bar("CHAMP 3 — Prise en charge des complications évolutives"))
    story.append(Spacer(1, 2 * mm))

    story.append(P("<b>Traitement anti-infectieux préventif</b>", S_H2))
    story.append(Spacer(1, 1.5 * mm))
    story.append(reco_table([
        ("R3.1", "Ne pas administrer de traitement anti-infectieux intraveineux préventif en "
         "l'absence d'infection documentée : pas de réduction démontrée de la mortalité, des "
         "infections de coulées de nécrose ni des infections extra-pancréatiques.", "2-"),
    ]))
    story.append(Spacer(1, 3 * mm))

    story.append(P("<b>Diagnostic d'infection de nécrose pancréatique</b>", S_H2))
    story.append(Spacer(1, 1.5 * mm))
    story.append(reco_table([
        ("R3.2", "Ne pas se limiter à l'examen clinique et à la CRP : s'appuyer aussi sur la "
         "procalcitonine et la tomodensitométrie abdominale (air extra-digestif intra/"
         "extra-pancréatique) pour établir le diagnostic.", "2+"),
        ("R3.3", "Ne pas réaliser de ponction à l'aiguille fine pour le diagnostic d'infection de "
         "nécrose en l'absence de signes cliniques de sepsis et/ou de scanner évocateur de "
         "surinfection (faux négatifs 20-25 %, risque de complications iatrogènes).", "AE"),
    ]))
    story.append(Spacer(1, 3 * mm))

    story.append(P("<b>Drainage de la nécrose pancréatique infectée</b>", S_H2))
    story.append(Spacer(1, 1.5 * mm))
    story.append(reco_table([
        ("R3.4", "Nécrose pancréatique infectée : réaliser un drainage, et ne pas se limiter à "
         "une antibiothérapie systémique seule.", "2+"),
        ("R3.5.1", "Privilégier en première intention une approche graduée « mini-invasive » "
         "(endoscopique et/ou radiologique percutanée) pour le drainage, selon l'expertise "
         "locale et la localisation des coulées de nécrose.", "1+"),
        ("R3.5.2", "En l'absence d'équipe d'endoscopie et/ou de radiologie interventionnelle "
         "entraînée localement au drainage mini-invasif : transférer le patient vers un centre "
         "expert.", "AE"),
    ]))
    story.append(Spacer(1, 3 * mm))

    story.append(P("<b>Traitement anti-infectieux curatif</b>", S_H2))
    story.append(Spacer(1, 1.5 * mm))
    story.append(reco_table([
        ("R3.6.1", "Infection de coulée de nécrose : administrer une antibiothérapie "
         "probabiliste ciblant les entérobactéries résistantes, Enterococcus faecium, "
         "Pseudomonas aeruginosa et les levures (surinfections fongiques ≈30 % des cas).", "2+"),
        ("—", "Aucune recommandation possible sur la molécule précise à privilégier (diffusion "
         "pancréatique des antibiotiques mal établie).", "SR"),
        ("R3.6.2", "Adapter secondairement l'antibiothérapie aux résultats microbiologiques "
         "(ponction percutanée, écho-endoscopie, drainage chirurgical, hémocultures) après avis "
         "pluridisciplinaire réanimation/gastro-entérologie/infectiologie, pour réduire le "
         "spectre et préserver l'écologie bactérienne.", "AE"),
    ]))
    story.append(Spacer(1, 3 * mm))

    story.append(P("<b>Complications vasculaires</b>", S_H2))
    story.append(Spacer(1, 1.5 * mm))
    story.append(reco_table([
        ("R3.7", "Complication hémorragique viscérale (rupture de pseudo-anévrysme le plus "
         "souvent, mortalité 34-52 %) : privilégier en priorité une technique de radiologie "
         "interventionnelle endovasculaire (moindre surmortalité qu'une chirurgie de "
         "sauvetage : 13 % vs 29 % dans une étude rétrospective).", "2+"),
        ("—", "Thrombose veineuse splanchnique (14-22 % des pancréatites aigües) : données "
         "insuffisantes pour statuer sur le rapport bénéfice/risque d'une anticoagulation "
         "préventive (facteurs de risque) ou curative (TVS avérée).", "SR"),
    ]))
    return story

# ---------------------------------------------------------------------------
def _section_annexe():
    story = []
    story.append(Spacer(1, 2 * mm))
    story.append(section_bar("Annexe 1 — Critères et scores de risque d'aggravation"))
    story.append(Spacer(1, 2 * mm))
    story.append(P("Liste des critères et scores existants à prendre en compte pour juger du "
                    "risque d'aggravation d'une pancréatite aigüe (aucun score isolé recommandé "
                    "à ce jour — cf. R1.1). Reproduits intégralement depuis la source.", S_BODY_SM))
    story.append(Spacer(1, 2 * mm))

    story.append(P("<b>Critères biologiques</b> — CRP &gt; 150 mg/L dans les 72 h suivant "
                    "l'admission. Autres proposés : urée sanguine &gt; 7 mmol/L, hématocrite "
                    "&gt; 44 %, procalcitonine &gt; 3,8 ng/mL dans les 96 h, hyperlactatémie.",
                    S_BODY_SM))
    story.append(Spacer(1, 2 * mm))

    story.append(P("<b>Score BISAP</b> ≥ 2 (1 point/critère) : urée &gt; 8,9 mmol/L · SIRS · "
                    "altération de la conscience · âge &gt; 60 ans · épanchement pleural "
                    "radiographique.", S_BODY_SM))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P("<b>SIRS</b> (≥ 2 critères) : température &lt; 36 °C ou &gt; 38 °C · FC &gt; "
                    "90/min · FR &gt; 20/min ou PaCO2 &lt; 32 mmHg · leucocytes &gt; 12 000/mm³, "
                    "&lt; 4 000/mm³ ou formes immatures circulantes &gt; 10 %.", S_BODY_SM))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P("<b>Score APACHE</b> ≥ 8 (calculé à l'admission ou dans les 72 premières "
                    "heures).", S_BODY_SM))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P("<b>Score de Ranson</b> ≥ 3 (1 point/critère) — à l'admission : âge &gt; 55 "
                    "ans, leucocytes &gt; 16 000/mm³, LDH &gt; 1,5N, ASAT &gt; 6N, glycémie &gt; "
                    "11 mmol/L ; entre l'admission et la 48<sup>e</sup> heure : chute de l'hématocrite &gt; "
                    "10 points, élévation de l'urée sanguine &gt; 1,8 mmol/L, calcémie &lt; 2 "
                    "mmol/L, PaO2 &lt; 60 mmHg, chute des bicarbonates &gt; 4 mEq/L, "
                    "séquestration liquidienne &gt; 6 L de perfusion en 48 h.", S_BODY_SM))
    story.append(Spacer(1, 3 * mm))

    story.append(P("<b>Critères radiologiques</b> (scanner réalisé à partir de la 48<sup>e</sup> heure)",
                    S_H2))
    story.append(Spacer(1, 1.5 * mm))
    story.append(simple_table(
        ["Score de Balthazar", "Description"],
        [
            ["Grade A", "Pancréas normal"],
            ["Grade B", "Élargissement focal ou diffus du pancréas"],
            ["Grade C", "Pancréas hétérogène + densification de la graisse péri-pancréatique"],
            ["Grade D", "Coulée péri-pancréatique unique"],
            ["Grade E", "Coulées multiples, ou signes de surinfection (bulles de gaz)"],
        ],
        [(PAGE_W - 2*MARGIN) * 0.28, (PAGE_W - 2*MARGIN) * 0.72]))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P("Un score de Balthazar de haut grade, ou un <b>CT Severity Index (CTSI) ≥ 3</b> "
                    "(prédit une morbi-mortalité ≈17 %), sont associés à la sévérité.", S_BODY_SM))
    story.append(Spacer(1, 2 * mm))
    story.append(KeepTogether([
        simple_table(
            ["Aspects morphologiques", "Pts", "Étendue de la nécrose", "Pts"],
            [
                ["Pancréas morphologiquement normal", "0", "0 % de la glande nécrosée", "0"],
                ["Augmentation de volume", "1", "< 30 % de la glande nécrosée", "2"],
                ["Infiltration de la graisse péripancréatique", "2", "30-50 % de la glande nécrosée", "4"],
                ["Une seule collection extrapancréatique", "3", "> 50 % de la glande nécrosée", "6"],
                ["Au moins deux collections, ou une collection\ncontenant du gaz", "4", "", ""],
            ],
            [(PAGE_W - 2*MARGIN) * 0.36, (PAGE_W - 2*MARGIN) * 0.08,
             (PAGE_W - 2*MARGIN) * 0.42, (PAGE_W - 2*MARGIN) * 0.08]),
        Spacer(1, 1.5 * mm),
        P("Aspects morphologiques : valeur de 0 à 4. Étendue de la nécrose : valeur de 0 "
          "à 6. <b>CTSI = somme des deux valeurs.</b>", S_NOTE),
    ]))
    story.append(Spacer(1, 4 * mm))
    story.append(P("Fiche de synthèse indépendante, produite pour un usage d'aide-mémoire. Elle "
                    "reprend l'intégralité des 24 recommandations et des 4 questions sans "
                    "recommandation possible, ainsi que le Tableau 1, la Figure 1 et l'Annexe 1 "
                    "du texte source, mais ne remplace pas le texte intégral et n'est ni éditée "
                    "ni validée par la SFAR, la SNFGE, la SFR, la SFNCM ou la SFED. En cas de "
                    "doute, se référer au texte intégral et/ou à un avis spécialisé.", S_SOURCE))
    return story

# ---------------------------------------------------------------------------
SECTIONS = [
    ("Contexte, méthodologie & Champ 1 — Évaluation/admission",
     lambda: _section_intro() + [Spacer(1, 3*mm)] + _section_champ1(), True),
    # Pas de saut de page force ici non plus : Figure 1 ne remplit qu'un tiers de la
    # page 2, mesure faite (cf. meme remarque plus bas pour Champ 3).
    ("Champ 2 — Prise en charge à la phase initiale", _section_champ2, False),
    # Pas de saut de page force ici : la fin du Champ 2 (Antalgie) laisse trop peu de
    # contenu pour occuper une page complete (cf. CLAUDE.md etape 7, fusion de sections
    # adjacentes quand une page mesuree serait <60% pleine).
    ("Champ 3 — Prise en charge des complications évolutives", _section_champ3, False),
    # Idem : la fin du Champ 3 (page mesuree a ~40% pleine) laisse assez de place pour
    # enchainer directement sur l'Annexe 1 sans saut de page.
    ("Annexe 1 — Scores de risque d'aggravation", _section_annexe, False),
]

def _make_doc(path=None):
    return SimpleDocTemplate(path or OUT, pagesize=A4,
                              leftMargin=MARGIN, rightMargin=MARGIN,
                              topMargin=32 * mm, bottomMargin=16 * mm,
                              title="SFAR 2021 - Pancréatite aigüe grave en soins critiques",
                              author="Synthèse indépendante (source SFAR/SNFGE/SFR/SFNCM/SFED)")

def _silent_page(canvas, doc_):
    pass

def _build_upto(section_fns, break_flags):
    story = []
    for i, fn in enumerate(section_fns):
        if i > 0 and break_flags[i]:
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
    fns = [fn for _, fn, _ in SECTIONS]
    breaks = [b for _, _, b in SECTIONS]

    boundaries = []
    for i in range(1, len(fns) + 1):
        pages = _count_pages(_build_upto(fns[:i], breaks[:i]))
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

    final_story = _build_upto(fns, breaks)
    docf = _make_doc()
    docf.build(final_story, onFirstPage=on_page_final, onLaterPages=on_page_final)
    print("OK ->", OUT, f"({total_pages} pages)")

if __name__ == "__main__":
    build()
