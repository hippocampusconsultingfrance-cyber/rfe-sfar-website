# -*- coding: utf-8 -*-
"""
Fiche de synthèse - RFE Sfar/SFA 2011
"Prévention du risque allergique péranesthésique. Texte court"
Société française d'anesthésie et réanimation (Sfar) & Société française d'allergologie (SFA)
Ann Fr Anesth Réanim 2011;30:212-222, doi:10.1016/j.annfar.2010.12.002.
Actualisation des recommandations élaborées en 2001 (Sfar/SFAIC) et publiées en 2002.
Source : sources/allergie_prevention.pdf (11 pages), texte extrait sources/allergie_prevention.txt
(~71 600 caractères, lu intégralement).

CHAMP DE CETTE FICHE : le document source est structuré en six questions. Cette fiche couvre
intégralement les questions 1 à 5 (réalité du risque et substances responsables, mécanismes/
physiopathologie, bilan diagnostique biologique et cutané, facteurs favorisants et place du bilan
allergologique préanesthésique, prévention primaire/secondaire-prémédication-choix de la technique
anesthésique). La question 6 (traitement du choc anaphylactique) est volontairement résumée en une
demi-page avec renvoi explicite, pour la raison ci-dessous.

RELATION AVEC LA FICHE COMPAGNON fiche_anaphylaxie.py / Fiche_SFAR_Anaphylaxie_2025.pdf -
CONSTAT IMPORTANT (divergence avec la prémisse initiale de la tâche, disclosée ici plutôt que
silencieusement corrigée) : la tâche de rédaction de cette fiche partait du principe que la fiche
2025 déjà construite dans ce corpus se limitait au Champ 4 (traitement aigu) et laissait tout le
bilan diagnostique (tryptase, tests cutanés, consultation allergo-anesthésie) hors champ, cette
fiche 2011 étant censée combler ce vide. Vérification faite : le fichier build/fiche_anaphylaxie.py
n'existe plus dans l'arborescence (seul un .pyc en cache subsiste), mais son contenu exact est
intégralement récupérable via build/content_anaphylaxie.json, qui est - selon le propre docstring
de build/extract_content.py - un enregistrement fidèle, en ordre de document, de ce que le script
produisait (aucune retypie). Cet examen montre que la fiche 2025 couvre en réalité déjà, intégrale-
ment et en détail : le Champ 1 (bilan diagnostique complet - scores/imputabilité, tryptase, hista-
mine, IgE spécifiques, test d'activation des basophiles, tests cutanés, tests de provocation, cas
particuliers enfant/femme enceinte), le Champ 2 (facteurs de risque - antécédents, latex, bêta-
lactamines/céfazoline, pholcodine, dépistage systématique, mastocytose), le Champ 4 (traitement
complet, classification de gravité Ring & Messmer modifiée/CIM-11, algorithme de synthèse) et la
conduite en chirurgie urgente (R3.4/R3.5, Annexe 6). Seul le "reste du Champ 3" (prévention
programmée au-delà de R3.4/R3.5) y est explicitement laissé hors champ.
Conséquence pratique pour CE script : la classification de gravité en 4 grades et le détail fin
tryptase/histamine/tests cutanés/TAB ne sont PAS re-tabulés intégralement ici (déjà couverts, plus
récemment, ailleurs sur le site) - ils sont mentionnés brièvement avec renvoi. En revanche, cette
fiche apporte le contenu du document 2011 qui n'est PAS dupliqué ailleurs sur le site : l'épidé-
miologie et les fréquences relatives des substances responsables, la physiopathologie du choc
(question 2), les tableaux de concentrations de référence pour les tests cutanés (Tableaux 3 et 4
du document source - la fiche 2025 cite son "Annexe 4" équivalente sans la reproduire), les
situations particulières de croisement allergénique de la question 4 (AINS, paracétamol, morphine/
codéine, œuf/soja, fruits de mer, protamine - aucune ne figure dans la fiche 2025), et surtout la
question 5 in extenso (prévention primaire/secondaire programmée, prémédication, choix de la
technique et des agents anesthésiques) - qui est précisément le volet que la fiche 2025 elle-même
déclare hors de son propre champ ("reste du Champ 3"). Le traitement (question 6) est résumé avec
renvoi explicite vers Fiche_SFAR_Anaphylaxie_2025.pdf pour l'algorithme actualisé.

MÉTHODOLOGIE - RECHERCHE D'UN GRADE PAR RECOMMANDATION (résultat négatif, disclosé) : le texte
source annonce une méthode "GRADE, modifiés et agréés par le comité des référentiels de la Sfar",
avec quatre niveaux de preuve globale NP1 (preuve forte) à NP4 (preuve très faible), attachés à de
très nombreux énoncés de l'argumentaire (comptage : 108 occurrences de "NP[1-4]" sur l'ensemble du
texte). Recherche exhaustive (grep insensible à la casse) de "Grade A", "Grade B", "Grade C" et
"accord professionnel" sur l'intégralité du texte source : AUCUNE occurrence. Il n'existe donc,
contrairement à d'autres RFE de ce corpus (Grade 1+/1-/2+/2- ou "accord fort"), aucun marqueur de
force imprimé à côté des recommandations individuelles - les NP1-4 qualifient le niveau de preuve
des constats de l'argumentaire (épidémiologie, mécanismes), pas la force d'une recommandation.
Conformément à la consigne de ce corpus en pareil cas : AUCUN chip de grade n'est fabriqué ici. Les
recommandations reproduites sont les phrases directives du texte source ("il faut", "il est
recommandé de", "il est proposé de", "il ne faut pas", "il n'y a pas lieu de"), présentées avec leur
repère de paragraphe (par ex. "S3.3.2.1") d'origine et, lorsque le texte source associe une citation
NP à l'énoncé, celle-ci est conservée entre parenthèses à titre de citation de preuve - jamais
présentée comme un grade de recommandation. Aucun appel à grade_chip()/GRADE_COLORS dans ce script.

Icône : icon_shield (bouclier/protection), choisie délibérément pour le thème "prévention" de cette
fiche, en complément visuel de l'icône probablement utilisée par la fiche 2025 (traitement aigu) -
différenciation volontaire entre les deux fiches compagnons plutôt que continuité visuelle stricte.

Pas d'arrondis Unicode (flèches/exposants/emoji) dans le corps du texte ; °C et µg/mL conservés
(convention déjà en usage dans fiche_hypothermie.py/fiche_curares.py de ce corpus).
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from style import *
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.units import mm

OUT = "/private/tmp/claude-501/-Users-macbook-Downloads-claude/65498e3e-5ddf-47a6-b100-3ac535d1faa0/scratchpad/rfe_sfar/output/Fiche_SFAR_SFA_Allergie_Prevention_2011.pdf"

SOURCE_TXT = ("Source : Sfar & Société française d'allergologie (SFA) -- « Prévention du risque "
              "allergique péranesthésique. Texte court » -- Recommandations formalisées d'experts, "
              "méthode GRADE modifiée (comité des référentiels de la Sfar). Ann Fr Anesth Réanim "
              "2011;30:212-222, doi:10.1016/j.annfar.2010.12.002. Fiche de synthèse non officielle : "
              "se référer au texte intégral.")

def P(txt, style=S_CELL):
    return Paragraph(txt, style)

# ---------------------------------------------------------------------------
# Local table helpers
# ---------------------------------------------------------------------------
def sect_table(rows, col_widths, text_header="Recommandation / conduite pratique (source)"):
    """rows: (ref, text) -- NO grade column: this source prints no per-recommendation grade
    (see méthodologie). 'ref' is the source's own paragraph marker (S1.7, S5.2.3, etc.)."""
    data = [[P("Rep.", S_HEAD_W), P(text_header, S_HEAD_W)]]
    for ref, txt in rows:
        data.append([P(ref, S_CELL_B), P(txt, S_CELL)])
    t = Table(data, colWidths=col_widths, repeatRows=1)
    style_cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), NAVY), ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTNAME", (0, 0), (-1, 0), FONT_BOLD), ("FONTSIZE", (0, 0), (-1, 0), 8),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
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
        ("BACKGROUND", (0, 0), (-1, 0), TEAL_DARK), ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTNAME", (0, 0), (-1, 0), FONT_BOLD), ("FONTSIZE", (0, 0), (-1, 0), 8),
        ("GRID", (0, 0), (-1, -1), 0.5, GREY_LIGHT), ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 3.2), ("BOTTOMPADDING", (0, 0), (-1, -1), 3.2),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            st.append(("BACKGROUND", (0, i), (-1, i), BG_PANEL))
    t.setStyle(TableStyle(st))
    return t

def highlight(text, bg=BG_PANEL, border=TEAL):
    return info_panel(P(text, S_BODY_SM), bg=bg, border=border)

def no_reco_panel(text):
    return info_panel(P("<b>Non recommandé / absence de justification</b> -- " + text, S_BODY_SM),
                       bg=GREY_LIGHT, border=GREY)

# Micro-styles for the wide concentration tables (Tableaux 3 & 4 du document source)
S_T3_HEAD = pstyle("t3_head", fontSize=6.8, leading=8, textColor=WHITE, fontName=FONT_BOLD, alignment=TA_CENTER)
S_T3_L = pstyle("t3_l", fontSize=7.3, leading=8.7, textColor=INK, alignment=TA_LEFT)
S_T3_LB = pstyle("t3_lb", fontSize=7.3, leading=8.7, textColor=INK, fontName=FONT_BOLD, alignment=TA_LEFT)
S_T3_C = pstyle("t3_c", fontSize=7.3, leading=8.7, textColor=INK, alignment=TA_CENTER)
S_T3_GROUP = pstyle("t3_group", fontSize=7.6, leading=9.2, textColor=WHITE, fontName=FONT_BOLD)

def t3(txt, style=S_T3_C):
    return Paragraph(txt, style)

def concentration_table(rows, group_rows=None):
    """rows: (DCI, nom_commercial, C, pt_dil, pt_cm, idr_dil, idr_cm).
    group_rows: optional list of (index_before_which_to_insert, label) for a spanning divider row
    (used by Tableau 4 to separate 'Antiseptiques' / 'Colorants', as printed in the source)."""
    cw = PAGE_W - 2 * MARGIN
    widths = [0.155 * cw, 0.185 * cw, 0.11 * cw, 0.135 * cw, 0.135 * cw, 0.14 * cw, 0.14 * cw]
    header = [t3("DCI", S_T3_HEAD), t3("Nom commercial", S_T3_HEAD), t3("C (mg/mL)", S_T3_HEAD),
              t3("PT Dilution", S_T3_HEAD), t3("PT CM (mg/mL)", S_T3_HEAD),
              t3("IDR Dilution", S_T3_HEAD), t3("IDR CM (mg/mL)", S_T3_HEAD)]
    data = [header]
    span_cmds = []
    bg_cmds = []
    row_i = 1
    groups = dict(group_rows) if group_rows else {}
    for idx, (dci, nom, c, ptd, ptcm, idrd, idrcm) in enumerate(rows):
        if idx in groups:
            data.append([t3(groups[idx], S_T3_GROUP), "", "", "", "", "", ""])
            span_cmds.append(("SPAN", (0, row_i), (-1, row_i)))
            bg_cmds.append(("BACKGROUND", (0, row_i), (-1, row_i), NAVY))
            row_i += 1
        data.append([t3(dci, S_T3_LB), t3(nom, S_T3_L), t3(c, S_T3_C), t3(ptd, S_T3_C),
                     t3(ptcm, S_T3_C), t3(idrd, S_T3_C), t3(idrcm, S_T3_C)])
        if (row_i - 1) % 2 == 0:
            bg_cmds.append(("BACKGROUND", (0, row_i), (-1, row_i), BG_PANEL))
        row_i += 1
    t = Table(data, colWidths=widths, repeatRows=1)
    style_cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("GRID", (0, 0), (-1, -1), 0.4, GREY_LIGHT),
        ("TOPPADDING", (0, 0), (-1, -1), 2.2), ("BOTTOMPADDING", (0, 0), (-1, -1), 2.2),
        ("LEFTPADDING", (0, 0), (-1, -1), 3), ("RIGHTPADDING", (0, 0), (-1, -1), 3),
    ] + span_cmds + bg_cmds
    t.setStyle(TableStyle(style_cmds))
    return t

TOTAL_PAGES = {"n": 8}

def on_page(canvas, doc, page_title):
    header_band(canvas, doc, "SFAR / SFA -- RFE 2011 -- FICHE DE SYNTHÈSE",
                "Prévention du risque allergique péranesthésique",
                page_title, icon_fn=lambda c, x, y: icon_shield(c, x, y, 13 * mm), color=TEAL_DARK)
    footer_band(canvas, doc, SOURCE_TXT, f"Page {doc.page} / {TOTAL_PAGES['n']}")

# ---------------------------------------------------------------------------
# Section 1 -- Introduction, méthodologie, champ, légende
# ---------------------------------------------------------------------------
def _section_intro():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Champ :</b> réactualisation (2011) des recommandations Sfar/SFAIC de 2001-2002 sur la "
        "<b>prévention</b> du risque allergique péranesthésique et la <b>conduite du bilan "
        "diagnostique</b> d'une réaction d'hypersensibilité immédiate (HSI) péranesthésique -- PAS le "
        "traitement aigu du choc, traité en question 6 (voir renvoi en fin de fiche). Le document est "
        "organisé en six questions ; cette fiche reproduit intégralement les <b>questions 1 à 5</b> "
        "(réalité du risque et substances responsables, mécanismes/physiopathologie, bilan "
        "diagnostique biologique et cutané, facteurs favorisants et place du bilan allergologique "
        "préanesthésique, prévention primaire/secondaire -- prémédication -- choix de la technique "
        "anesthésique) et résume la <b>question 6</b> (traitement) avec renvoi.<br/><br/>"
        "<b>Relation avec la fiche compagnon « Anaphylaxie 2025 » de ce site :</b> "
        "Fiche_SFAR_Anaphylaxie_2025.pdf (RFE Sfar/SFA plus récente, sur la prise en charge de "
        "l'hypersensibilité immédiate péri-opératoire) couvre déjà, intégralement et de façon plus à "
        "jour, le bilan diagnostique complet (tryptase, histamine, IgE spécifiques, test d'activation "
        "des basophiles, tests cutanés, tests de provocation), les facteurs de risque (latex, "
        "bêta-lactamines/céfazoline, pholcodine, mastocytose) et le traitement (classification de "
        "gravité, adrénaline, remplissage, choc réfractaire). Cette fiche-ci, bâtie sur le document "
        "source de 2011, ne duplique donc pas ce contenu : elle en reste au niveau de détail du texte "
        "de 2011 pour ces points communs (avec renvoi), et développe en revanche ce que le document "
        "2025 ne couvre pas -- épidémiologie/fréquences des substances responsables, physiopathologie "
        "du choc, tableaux de concentrations de référence pour les tests cutanés, situations "
        "particulières de croisement allergénique (AINS, paracétamol, morphine/codéine, œuf/soja, "
        "fruits de mer, protamine), et surtout la <b>question 5</b> -- prévention programmée, "
        "prémédication, choix de la technique -- que la fiche 2025 déclare elle-même hors de son "
        "propre champ.",
        S_BODY), bg=BG_PANEL, border=TEAL))
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Méthodologie -- niveaux de preuve (NP) et absence de grade par recommandation "
        "(disclosure) :</b> le texte source utilise une méthode GRADE modifiée, agréée par le comité "
        "des référentiels de la Sfar, pour attacher un niveau de preuve globale (NP1 à NP4, légende "
        "ci-dessous) à de nombreux constats de l'argumentaire (épidémiologie, mécanismes). Recherche "
        "exhaustive effectuée sur l'intégralité du texte source pour « Grade A », "
        "« Grade B », « Grade C » et « accord professionnel » : "
        "<b>aucune occurrence</b>. À la différence d'autres RFE de ce corpus (Grade 1+/1-/2+/2- ou "
        "« accord fort »), ce texte court <b>n'imprime aucun marqueur de force propre à "
        "chaque recommandation</b> : les NP1-4 qualifient le niveau de preuve d'un constat de "
        "l'argumentaire, pas la force d'une recommandation individuelle. Conformément à la règle de "
        "ce corpus dans cette situation, <b>aucun chip de grade n'est fabriqué ici</b>. Les "
        "recommandations reproduites ci-après sont les phrases directives du texte source (« il "
        "faut », « il est recommandé de », « il est proposé de », « il "
        "ne faut pas », « il n'y a pas lieu de »), présentées avec leur repère de "
        "paragraphe d'origine ; lorsque le texte source associe une citation NP à l'énoncé, elle est "
        "conservée entre parenthèses à titre de citation de preuve -- jamais comme un grade de "
        "recommandation.",
        S_BODY_SM), bg=AMBER_LIGHT, border=AMBER))
    story.append(Spacer(1, 3 * mm))
    story.append(KeepTogether([
        section_bar("Légende des niveaux de preuve (NP) -- argumentaire, PAS un grade de recommandation"),
        Spacer(1, 2 * mm),
        simple_table(
            ["Niveau", "Définition (méthode GRADE modifiée, comité des référentiels Sfar)"],
            [
                ["NP1", "Preuve globale forte : méta-analyses concordantes de haut niveau, ou étude(s) de haut "
                        "niveau non contredite(s), ou >= 2 études de bas niveau non contradictoires avec RR > 2 ou < 0,5."],
                ["NP2", "Preuve globale modérée : >= 2 études de bas niveau non contradictoires, mais RR < 2 ou "
                        "> 0,5 dans toutes (ou toutes sauf une)."],
                ["NP3", "Preuve globale faible : plusieurs études de bas niveau, dont certaines contradictoires, "
                        "avec une majorité se dégageant pour un effet favorable ou défavorable."],
                ["NP4", "Preuve globale très faible : études de haut niveau contradictoires, ou uniquement des "
                        "études de très bas niveau."],
            ], [16 * mm, PAGE_W - 2 * MARGIN - 16 * mm]),
    ]))
    story.append(Spacer(1, 2 * mm))
    story.append(P(
        "<i>Définitions du document source : réaction allergique = réaction immunologique lors d'un "
        "contact renouvelé avec un antigène chez un sujet sensibilisé (période de sensibilisation "
        "silencieuse, minimum dix jours) ; anaphylaxie = terme réservé à une réaction grave d'HSI "
        "allergique ou non allergique ; atopie = susceptibilité anormale à synthétiser des IgE "
        "spécifiques contre des antigènes naturels de l'environnement.</i>", S_NOTE))
    return story

# ---------------------------------------------------------------------------
# Section 2 -- Question 1 : réalité du risque
# ---------------------------------------------------------------------------
def _section_q1():
    story = []
    story.append(Spacer(1, 2 * mm))
    story.append(section_bar("Question 1 -- Réalité du risque d'hypersensibilité allergique en anesthésie"))
    story.append(Spacer(1, 2 * mm))
    story.append(P(
        "Parmi les réactions d'hypersensibilité immédiate (HSI) survenant en anesthésie, environ "
        "<b>60% sont IgE-dépendantes</b> (réaction allergique) (NP2). Plus de 7000 cas d'HSI "
        "IgE-dépendantes péranesthésiques ont été publiés au cours des 25 dernières années (NP2), "
        "provenant majoritairement de France, d'Australie, de Nouvelle-Zélande et, plus récemment, "
        "de Scandinavie, grâce à l'organisation mise en place pour le diagnostic et la communication "
        "de ces réactions. L'exploration et la déclaration en pharmacovigilance ou matériovigilance "
        "des réactions d'HSI doivent être systématiques ; la constitution de réseaux de consultations "
        "spécialisées, d'observatoires et de registres doit être encouragée.", S_BODY))
    story.append(Spacer(1, 2 * mm))
    story.append(highlight(
        "<b>Incidence :</b> variable selon les pays, de 1/10 000 à 1/20 000 anesthésies (NP2). "
        "Évaluée en France en 1996 à <b>1/13 000</b> anesthésies générales et locorégionales, toutes "
        "substances confondues. Anaphylaxie aux curares : <b>1/6500</b> anesthésies avec curare en "
        "France, <b>1/5200</b> en Norvège (NP2). <b>Mortalité</b> des réactions d'HSI péranesthésiques : "
        "<b>3 à 9%</b> selon les pays (NP2) ; la morbidité la plus sévère s'exprime par des séquelles "
        "anoxiques cérébrales, d'incidence non précisément connue.",
        bg=BG_PANEL, border=TEAL))
    story.append(Spacer(1, 3 * mm))
    story.append(KeepTogether([
        P("<b>Substances responsables</b> -- fréquence relative parmi les cas d'anaphylaxie publiés "
          "depuis 1980 (littérature anglaise et française) (NP2)", S_CELL_B),
        Spacer(1, 1.5 * mm),
        simple_table(
            ["Substance", "Fréquence relative"],
            [
                ["Curares", "62,6 %"],
                ["Latex", "13,8 %"],
                ["Hypnotiques", "7,2 %"],
                ["Antibiotiques", "6 %"],
                ["Substituts du plasma (colloïdes)", "3,2 %"],
                ["Morphiniques", "2,4 %"],
            ], [PAGE_W - 2 * MARGIN - 40 * mm, 40 * mm]),
    ]))
    story.append(Spacer(1, 2 * mm))
    story.append(P(
        "L'allergie aux anesthésiques locaux apparaît exceptionnelle compte tenu de leur fréquence "
        "d'utilisation. <b>Aucune réaction anaphylactique n'a été publiée avec les anesthésiques "
        "halogénés</b> (NP2). D'autres substances peuvent induire une anaphylaxie péranesthésique : "
        "aprotinine, chlorhexidine, protamine, papaïne, héparine, bleu patenté ou de méthylène. Tous "
        "les curares peuvent être en cause, y compris dès la première administration ; le curare le "
        "plus fréquemment impliqué dans les réactions immédiates allergiques est le "
        "<b>suxaméthonium</b> (NP2). Une sensibilisation croisée entre curares est possible.", S_BODY_SM))
    story.append(Spacer(1, 2 * mm))
    story.append(P(
        "<b>Aspects cliniques :</b> les manifestations sont décrites en quatre grades de gravité "
        "croissante (classification adaptée de Ring et Messmer, Tableau 1 du document source). Cette "
        "classification en 4 grades de 2011 (seuils : chute de la PA systolique > 30% et tachycardie "
        "> 30% pour le grade II) n'est pas retabulée ici : une version actualisée (Ring & Messmer "
        "modifiée / CIM-11 OMS, avec seuils chiffrés) est déjà reproduite intégralement dans la fiche "
        "compagnon Fiche_SFAR_Anaphylaxie_2025.pdf (Champ 4) -- s'y référer pour la classification de "
        "référence actuelle. Les manifestations sont souvent plus graves et durables en cas de réaction "
        "allergique que non allergique (NP2). Les signes cliniques ne sont pas toujours complets et "
        "peuvent prendre des masques trompeurs : l'absence de signes cutanéomuqueux n'exclut pas le "
        "diagnostic d'anaphylaxie (NP2). La symptomatologie est habituellement immédiate après "
        "l'induction, mais peut être retardée (jusqu'à plus d'une heure) si le latex ou des colorants "
        "sont en cause.", S_BODY_SM))
    story.append(Spacer(1, 2 * mm))
    story.append(highlight(
        "<b>Enfant :</b> les substances potentiellement responsables sont les mêmes que chez l'adulte, "
        "mais l'allergène le plus fréquemment en cause est le <b>latex</b>, en particulier chez "
        "l'enfant multiopéré et porteur de spina bifida, ce qui justifie une stratégie de prévention "
        "primaire de la sensibilisation au latex (NP1). Les réactions d'hypersensibilité non "
        "immédiate impliquant les produits de l'anesthésie sont peu fréquentes ; elles sont surtout "
        "décrites avec les anesthésiques locaux (NP2), les antibiotiques, les antiseptiques, les "
        "héparines et les produits de contraste iodés ou gadolinés (NP2).",
        bg=GREEN_LIGHT, border=GREEN))
    return story

# ---------------------------------------------------------------------------
# Section 3 -- Question 2 (mécanismes) + début Question 3 (bilan biologique)
# ---------------------------------------------------------------------------
def _section_q2_q3a():
    story = []
    story.append(Spacer(1, 2 * mm))
    story.append(section_bar("Question 2 -- Mécanismes de la sensibilisation et physiopathologie du choc"))
    story.append(Spacer(1, 2 * mm))
    story.append(P(
        "La réaction d'HSI allergique est un cas particulier de réaction inflammatoire spécifique "
        "d'un allergène reconnu par le système immunitaire. La présentation antigénique oriente la "
        "réponse vers des effecteurs de l'allergie (lymphocytes TCD4+ Th1 ou Th2, TCD8+ cytotoxiques, "
        "lymphocytes B producteurs d'IgE) ; la tolérance résulterait de la différenciation en "
        "lymphocytes T régulateurs (NP2). L'HSI allergique immédiate résulte d'une activation des "
        "lymphocytes Th2 et est liée à la production d'IgE ; l'HSI allergique non immédiate est "
        "associée à une activation de profil Th1 (production d'IFN-gamma, cytotoxicité) (NP2). Les "
        "antigènes médicamenteux sont rarement identifiés : une partie de la molécule (épitope) joue "
        "le rôle d'haptène et se lie à une protéine, puis à une molécule du CMH lors de sa digestion "
        "par une cellule présentatrice ; un autre mécanisme (« p-i concept ») correspondrait "
        "à la liaison non covalente des haptènes avec le CMH ou le récepteur T sans passer par la "
        "cellule présentatrice (NP3).", S_BODY_SM))
    story.append(Spacer(1, 2 * mm))
    story.append(P(
        "<b>Manifestations cliniques :</b> les réactions allergiques immédiates résultent de "
        "l'activation des mastocytes et basophiles par l'allergène reconnu par les IgE fixées à leur "
        "surface (NP2). Les médiateurs libérés -- histamine, dérivés de l'acide arachidonique, TNF "
        "alpha, enzymes (tryptase notamment) -- altèrent la perméabilité capillaire (urticaire, "
        "œdème), provoquent une bronchoconstriction et une chute tensionnelle avec tachycardie (NP1). "
        "Les réactions non allergiques (anciennement anaphylactoïdes) résultent d'une activation des "
        "basophiles/mastocytes indépendante des IgE et sont de gravité moindre.", S_BODY_SM))
    story.append(Spacer(1, 2 * mm))
    story.append(highlight(
        "<b>Physiopathologie du choc :</b> la première phase correspond à un choc hyperkinétique "
        "(tachycardie, effondrement des résistances vasculaires systémiques par vasodilatation "
        "artériolaire périphérique, diminution du retour veineux et du débit cardiaque). Puis "
        "s'installe un choc hypovolémique hypokinétique, secondaire à l'extravasation plasmatique "
        "transcapillaire ; les métabolites de l'acide arachidonique majorent les effets circulatoires "
        "par leurs actions sur le muscle lisse vasculaire et les plaquettes (NP2). Un retard au "
        "traitement ou une thérapeutique inadaptée peut aboutir à une anoxie tissulaire puis à une "
        "défaillance viscérale rendant le choc rapidement réfractaire. <b>La prise au long cours de "
        "bêta-bloquants est un facteur de gravité</b> (NP1).",
        bg=RED_LIGHT, border=RED))
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("Question 3 (1/3) -- Bilan diagnostique : dosages biologiques immédiats"))
    story.append(Spacer(1, 2 * mm))
    story.append(P(
        "Tout patient présentant une réaction d'HSI péranesthésique doit bénéficier d'une "
        "investigation immédiate et à distance (type de réaction, agent causal, sensibilisation "
        "croisée éventuelle). L'anesthésiste-réanimateur doit : assurer la mise en œuvre des "
        "investigations en partenariat avec une consultation d'allergo-anesthésie ; informer le "
        "patient et remettre un courrier détaillé et une carte d'allergie provisoire ; déclarer "
        "l'accident au centre régional de pharmacovigilance (médicament suspecté) ou au responsable "
        "de matériovigilance de l'établissement (latex suspecté).", S_BODY_SM))
    story.append(Spacer(1, 2 * mm))
    story.append(P(
        "La probabilité qu'une symptomatologie clinique soit liée à une HSI est augmentée en présence "
        "d'une élévation de la tryptase sérique et de l'histamine plasmatique (NP1), même si une "
        "concentration normale n'exclut pas totalement le diagnostic (NP3). Le détail fin des seuils "
        "et formules de tryptase/histamine actualisés (formule tenant compte du taux basal, seuils en "
        "contexte d'arrêt cardio-respiratoire) est déjà traité dans la fiche compagnon "
        "Fiche_SFAR_Anaphylaxie_2025.pdf (Champ 1, 2/4) ; les éléments du document 2011, résumés "
        "ci-dessous, restent la référence historique de cette question.", S_NOTE))
    story.append(Spacer(1, 2 * mm))
    story.append(sect_table([
        ("S3.3.2.1", "Une augmentation franche de la tryptase sérique (&gt; 25 microg/mL) est en "
                     "faveur d'un mécanisme IgE-dépendant (NP2). Les concentrations restent normales ou "
                     "peu augmentées dans les réactions cutanéomuqueuses (grade 1) et systémiques "
                     "modérées (grade 2)."),
        ("S3.3.2.2", "Délais optimaux de prélèvement de la tryptase : 15 à 60 minutes pour les grades "
                     "1-2 ; 30 minutes à 2 heures pour les grades 3-4. La positivité excède souvent "
                     "6 heures pour les grades sévères (NP3)."),
        ("S3.3.3.2", "Le pic d'histamine plasmatique est observé dès la première minute suivant la "
                     "réaction (d'autant plus élevé que la réaction est grave), avec une demi-vie "
                     "d'élimination de 15 à 20 minutes (NP2)."),
        ("S3.3.3.3", "Délai idéal de prélèvement de l'histamine : &lt; 15 min pour le grade 1, "
                     "&lt; 30 min pour le grade 2, &lt; 2 h pour les réactions plus sévères."),
        ("S3.3.3.5", "Il ne faut pas doser l'histamine plasmatique chez la femme enceinte à partir du "
                     "2e trimestre (synthèse placentaire de diamine oxydase) ni chez les patients sous "
                     "héparine (augmentation de diamine oxydase proportionnelle à la dose)."),
        ("S3.5.4", "En cas de décès, les prélèvements pour tryptase et IgE spécifiques doivent être "
                    "pratiqués avant l'arrêt de la réanimation plutôt qu'en post-mortem (NP4) ; le "
                    "prélèvement fémoral est recommandé (NP3)."),
    ], [22 * mm, PAGE_W - 2 * MARGIN - 22 * mm]))
    return story

# ---------------------------------------------------------------------------
# Section 4 -- Question 3 (2/3 et 3/3) : tests cutanés, cellulaires, provocation
# ---------------------------------------------------------------------------
def _section_q3bc():
    story = []
    story.append(Spacer(1, 2 * mm))
    story.append(P(
        "<b>IgE spécifiques :</b> un taux d'IgE totales n'a aucune pertinence diagnostique. La "
        "recherche d'IgE spécifiques concerne principalement les ammoniums quaternaires (curares), le "
        "thiopental, le latex, les bêta-lactamines et la chlorhexidine (NP2). L'IgE anti-ammonium "
        "quaternaire reste détectable plusieurs années après une réaction à un curare (NP1) ; les "
        "techniques à privilégier sont le SAQ-RIA ou le PAPPC-RIA (NP2). Les techniques de dosage des "
        "IgE spécifiques du latex ont une excellente sensibilité (NP2). Seuls quelques antibiotiques "
        "sont dosables (pénicilloyl G et V, amoxicilloyl, ampicilloyl, céfaclor) ; il ne faut pas les "
        "rechercher à titre systématique, et seul l'allergologue en charge du bilan est habilité à "
        "demander et interpréter ces dosages, compte tenu de leur sensibilité faible (NP2).", S_BODY_SM))
    story.append(Spacer(1, 2 * mm))
    story.append(KeepTogether([
        P("<b>Tableau 2 (source) -- modes et délais de prélèvement sanguin</b> pour les dosages "
          "d'histamine, de tryptase et d'IgE antiammonium quaternaire (AQ)", S_CELL_B),
        Spacer(1, 1.5 * mm),
        simple_table(
            ["Dosage", "Tube", "Prélèvement < 30 min", "Prélèvement 1 à 2 h", "Prélèvement > 24 h"],
            [
                ["Histamine", "EDTA", "+", "(+)", ""],
                ["Tryptase", "EDTA / sec", "+", "+", "+"],
                ["IgE anti-AQ", "Sec", "+", "(+)", "(+)"],
            ], [26 * mm, 22 * mm, 33 * mm, 33 * mm, None]),
        Spacer(1, 1 * mm),
        P("<i>+ : recommandé ; (+) : si non réalisé au moment de la réaction.</i>", S_NOTE),
    ]))
    story.append(Spacer(1, 2 * mm))
    story.append(P(
        "<b>Modalités de prélèvement (S3.5.1) :</b> histamine sur tube EDTA (5 mL) ; tryptase sur "
        "tube sec ou EDTA (le même tube EDTA peut servir aux deux dosages) ; IgE sur tube sec (7 mL). "
        "Transmission au laboratoire dans les 2 heures, sinon conservation à +4°C pendant 12 h "
        "maximum ; après centrifugation, plasma et sérum congelés à -20°C en aliquotes, le plasma "
        "étant recueilli à distance de la couche leucocytaire (NP2). Du fait de la gravité potentielle "
        "et de la demi-vie courte de certains médiateurs, il est conseillé de disposer au bloc "
        "opératoire d'un sachet contenant les tubes de prélèvement, le protocole de recueil et la "
        "fiche de collecte des données cliniques.", S_BODY_SM))
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("Question 3 (2/3) -- Tests cutanés : PT / IDR (référence diagnostique)"))
    story.append(Spacer(1, 2 * mm))
    story.append(highlight(
        "<b>Délai (S3.6.1) :</b> les tests cutanés doivent être effectués <b>4 à 6 semaines</b> après "
        "la réaction, pour permettre la reconstitution des médiateurs dans les basophiles et "
        "mastocytes (NP3). En cas de nécessité, ils peuvent être réalisés plus précocement, mais cela "
        "accroît le risque de faux négatifs et seuls les résultats positifs sont alors pris en compte "
        "-- ce bilan précoce ne se substitue pas au bilan réalisé après 4 à 6 semaines (NP4).",
        bg=BG_PANEL, border=TEAL))
    story.append(Spacer(1, 2 * mm))
    story.append(P(
        "Le diagnostic d'HSI repose sur l'association des signes cliniques, le dosage des médiateurs "
        "et un bilan allergologique à distance (tests cutanés, tests de laboratoire, éventuellement "
        "tests de provocation). Les tests cutanés ne peuvent être interprétés qu'en fonction de "
        "renseignements cliniques chronologiques et détaillés fournis par l'anesthésiste, idéalement "
        "avec copie de la feuille d'anesthésie et de SSPI ainsi que les résultats de tryptase/"
        "histamine. Conditions requises : consentement éclairé ; arrêt préalable des médicaments "
        "inhibant la réactivité cutanée (antihistaminiques, psychotropes) (NP2). Grossesse, jeune âge, "
        "bêta-bloquants (sauf pour les bêta-lactamines), corticoïdes oraux ou IEC ne sont <b>pas</b> "
        "des contre-indications aux tests cutanés (NP3). Il est recommandé de tester l'ensemble des "
        "médicaments du protocole anesthésique, le latex et les autres produits périanesthésiques ; le "
        "choix se fait par le binôme allergologue-anesthésiste lors de la consultation "
        "d'allergo-anesthésie.", S_BODY_SM))
    story.append(Spacer(1, 2 * mm))
    story.append(P(
        "<b>Technique :</b> solutions commerciales pures ou diluées extemporanément (sérum "
        "physiologique ou phénolé). La valeur prédictive des PT est inférieure à celle des IDR (NP4). "
        "Quand les PT sont négatifs, les IDR débutent à une dilution au 1/1000e (curares) ou 1/10 000e "
        "(morphine) de la solution mère ; si l'IDR est négative, la concentration suivante (x10) est "
        "utilisée, avec un intervalle de 20 minutes entre chaque test, sans dépasser les concentrations "
        "maximales des Tableaux 3 et 4 (NP1). En cas de réaction de grade IV, le médicament suspecté "
        "est testé dès le prick-test à partir du 1/100e de la solution mère. L'interprétation exige un "
        "témoin négatif et un témoin positif (phosphate de codéine 9% et/ou histamine 10 mg/mL, "
        "œdème >= 3 mm à 20 min) (NP2). Positivité du PT : œdème de diamètre supérieur de 3 mm au "
        "témoin négatif, ou >= à la moitié du diamètre du témoin positif (NP2). Positivité de l'IDR : "
        "papule obtenue de diamètre au moins double de la papule d'injection, à 20 minutes (NP2).",
        S_BODY_SM))
    story.append(Spacer(1, 2 * mm))
    story.append(P(
        "<b>Site des tests (S3.6.8.8) :</b> le site de réalisation des tests cutanés (dos, bras ou "
        "avant-bras) est indifférent à condition que l'interprétation du résultat tienne compte de la "
        "réactivité normale de la peau au site de réalisation du test et de la taille de la papule "
        "d'injection intradermique du produit à tester (NP2). "
        "<b>Volume d'injection des IDR (S3.6.8.10) :</b> il faut réaliser les IDR en injectant dans le "
        "derme un volume de 0,03 à 0,05 mL de la solution commerciale diluée, afin d'obtenir une "
        "papule d'injection (PI) ayant au maximum 4 mm de diamètre.",
        S_BODY_SM))
    story.append(Spacer(1, 2 * mm))
    story.append(P(
        "<b>Tableaux 3 et 4 du document source (ci-dessous, reproduits verbatim) :</b> concentrations "
        "normalement non réactives (C = concentration de la solution commerciale ; PT/IDR Dilution = "
        "dilution testée ; CM = concentration maximale à ne pas dépasser pour éviter les faux "
        "positifs).", S_NOTE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P("<b>Tableau 3 -- Agents anesthésiques</b>", S_CELL_B))
    story.append(Spacer(1, 1 * mm))
    story.append(concentration_table([
        ("Atracurium", "Tracrium", "10", "1/10", "1", "1/1000", "10"),
        ("Cis-atracurium", "Nimbex", "2", "Non dilué", "2", "1/100", "20"),
        ("Mivacurium", "Mivacron", "2", "1/10", "0,2", "1/1000", "2"),
        ("Pancuronium", "Pavulon", "2", "Non dilué", "2", "1/10", "200"),
        ("Rocuronium", "Esmeron", "10", "Non dilué", "10", "1/200", "50"),
        ("Suxaméthonium", "Célocurine-klorid", "50", "1/5", "10", "1/500", "100"),
        ("Vécuronium", "Norcuron", "4", "Non dilué", "4", "1/10", "400"),
        ("Étomidate", "Hypnomidate / Étomidate-Lipuro", "2", "Non dilué", "2", "1/10", "200"),
        ("Midazolam", "Hypnovel", "5", "Non dilué", "5", "1/10", "400"),
        ("Propofol", "Diprivan", "10", "Non dilué", "10", "1/10", "1000"),
        ("Thiopental", "Nesdonal", "25", "Non dilué", "25", "1/100", "250"),
        ("Kétamine", "Ketalar", "100", "1/10", "10", "1/100", "1000"),
        ("Alfentanil", "Rapifen", "0,5", "Non dilué", "0,5", "1/10", "50"),
        ("Fentanyl", "Fentanyl", "0,05", "Non dilué", "0,05", "1/10", "5"),
        ("Morphine", "Morphine", "10", "1/10", "1", "1/1000", "10"),
        ("Rémifentanil", "Ultiva", "0,05", "Non dilué", "0,05", "1/10", "5"),
        ("Sufentanil", "Sufentanyl", "0,005", "Non dilué", "0,005", "1/10", "0,5"),
        ("Bupivacaïne", "Marcaïne", "2,5", "Non dilué", "2,5", "1/10", "250"),
        ("Lidocaïne", "Xylocaïne", "10", "Non dilué", "10", "1/10", "1000"),
        ("Mépivacaïne", "Carbocaïne", "10", "Non dilué", "10", "1/10", "1000"),
        ("Ropivacaïne", "Naropéine", "2", "Non dilué", "2", "1/10", "200"),
    ]))
    story.append(Spacer(1, 3 * mm))
    story.append(P("<b>Tableau 4 -- Antiseptiques et colorants</b>", S_CELL_B))
    story.append(Spacer(1, 1 * mm))
    story.append(KeepTogether([
        concentration_table([
            ("Chlorhexidine aqueuse non colorée", "--", "0,5", "Non dilué", "0,5", "1/10", "50"),
            ("Povidone iodée aqueuse", "--", "100", "Non dilué", "10", "1/10", "10 000"),
            ("Bleu patenté", "--", "25", "Non dilué", "25", "1/10", "2500"),
            ("Bleu de méthylène (chlorure de méthylthionine)", "--", "10", "Non dilué", "10", "1/100", "100"),
        ], group_rows=[(0, "Antiseptiques"), (2, "Colorants")]),
        Spacer(1, 1 * mm),
        P("<i>Pour les tests intradermiques aux colorants, risque de tatouage persistant plusieurs "
          "mois.</i>", S_NOTE),
    ]))
    story.append(Spacer(1, 2 * mm))
    story.append(P(
        "<b>Autres points (S3.6.8.11 à S3.6.8.15) :</b> il faut rechercher une sensibilisation croisée "
        "avec tous les autres curares commercialisés en cas de positivité à un curare (NP2), y compris "
        "avec les curares nouvellement commercialisés après une réaction anaphylactique prouvée lors "
        "d'une anesthésie antérieure (NP3). En cas de réaction survenant plus de 24 heures après "
        "l'anesthésie, il est recommandé de réaliser des tests épicutanés (patch-tests) à lecture "
        "retardée (&gt;= 48 h), notamment pour une symptomatologie à type d'eczéma : antibiotiques, "
        "produits de contraste iodés, allergènes de contact (métaux, caoutchouc, colorants, "
        "antiseptiques) (NP3). Il faut exclure le terme « douteux » des comptes rendus : la "
        "réponse est binaire (positif/négatif), à refaire à distance si nécessaire (NP4). La "
        "performance des tests cutanés peut décroître avec le temps -- prolongée avec les curares, "
        "elle décroît avec les antibiotiques (NP2).", S_BODY_SM))
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("Question 3 (3/3) -- Tests cellulaires, tests de provocation, résultats"))
    story.append(Spacer(1, 2 * mm))
    story.append(P(
        "<b>Tests cellulaires</b> (histaminolibération, test d'activation des basophiles par "
        "cytométrie en flux, libération des leucotriènes leucocytaires) : aucun n'a démontré de "
        "supériorité franche sur les autres ; ils sont prescrits selon l'expertise du laboratoire, en "
        "complément des tests cutanés (pas en remplacement), inutiles si le diagnostic est déjà établi. "
        "Indications : réaction de grade >= II avec tests cutanés négatifs à tous les produits "
        "suspectés ; tests cutanés difficilement interprétables (dermographisme, sujet très âgé ou "
        "très jeune, atopique avec lésions cutanées étendues, prise d'antihistaminiques) ; confirmation "
        "du choix d'un curare dont le test cutané est négatif ; pour l'hypersensibilité aux AINS, "
        "cytométrie en flux ou libération de leucotriènes. Le protocole actualisé du test d'activation "
        "des basophiles (délai minimal, arrêt des corticoïdes) est détaillé dans la fiche compagnon "
        "Fiche_SFAR_Anaphylaxie_2025.pdf (Champ 1, 3/4).", S_BODY_SM))
    story.append(Spacer(1, 2 * mm))
    story.append(P(
        "<b>Tests de provocation / réintroduction :</b> indications restreintes -- médicaments à tests "
        "cutanés négatifs (anesthésiques locaux, antibiotiques, exceptionnellement latex) ou non "
        "validés/impossibles (AINS), ou allergène indisponible sous forme réactive (métabolites, "
        "pénicillines à tests cutanés négatifs, autres antibiotiques, AINS) (NP2). Réalisés au moins "
        "1 mois après la réaction, avec le même médicament et la même voie, sous haute surveillance, "
        "uniquement en centres spécialisés avec accès à un secteur de soins intensifs (NP1) ; "
        "consentement éclairé et rapport bénéfice/risque favorable préalables (NP3). "
        "<b>Réintroduction des anesthésiques locaux :</b> 0,5 à 1 mL de solution non diluée et non "
        "adrénalinée en sous-cutané ; négatif en l'absence de réaction dans les 30 minutes ; chez la "
        "parturiente, en salle de naissance, 30 minutes avant la technique périmédullaire, équipe "
        "obstétricale prévenue (NP4) -- protocole pour l'essentiel inchangé dans la mise à jour de "
        "2025 (voir fiche dédiée, R3.4.2/Annexe 6). <b>Test de provocation au latex :</b> port d'un "
        "gant en latex naturel riche en protéines, non poudré, pendant 15 minutes ; négatif en "
        "l'absence de signe d'HSI dans les 30 minutes (NP3).", S_BODY_SM))
    story.append(Spacer(1, 2 * mm))
    story.append(P(
        "<b>Résultats de l'enquête et traçabilité :</b> le compte rendu de l'allergologue est adressé "
        "à l'anesthésiste prescripteur et figure au dossier médical ; un double est adressé au centre "
        "régional de pharmacovigilance (avec le descriptif clinique) et au médecin traitant. À la fin "
        "de la consultation d'allergo-anesthésie, une lettre détaillée et une carte d'allergie "
        "définitive sont remises au patient, qui est encouragé à les porter près de ses papiers "
        "d'identité (port de bracelet ou médaille également encouragé). En cas de difficulté "
        "d'interprétation, le recours à un groupe régional ou local d'allergologues et "
        "d'anesthésistes-réanimateurs référents est souhaitable (liste disponible via les sites Sfar "
        "et SFA). Il est souhaitable de suivre régulièrement l'évolution du nombre de réactions d'HSI, "
        "en colligeant les données des centres référents et de pharmacovigilance régionale, situées "
        "dans le cadre des enquêtes de mortalité-morbidité de la Sfar ou du GERAP.", S_BODY_SM))
    return story

# ---------------------------------------------------------------------------
# Section 5 -- Question 4 : facteurs favorisants et bilan préanesthésique
# ---------------------------------------------------------------------------
def _section_q4():
    story = []
    story.append(Spacer(1, 2 * mm))
    story.append(section_bar("Question 4 -- Facteurs favorisants et place du bilan allergologique préanesthésique"))
    story.append(Spacer(1, 2 * mm))
    story.append(KeepTogether([
        P("<b>Patients à risque de réaction d'hypersensibilité (S4.1)</b>", S_CELL_B),
        Spacer(1, 1.5 * mm),
        sect_table([
            ("S4.1.1", "Diagnostic d'allergie à un médicament/produit de l'anesthésie déjà établi par "
                       "un bilan allergologique préalable."),
            ("S4.1.2", "Signes cliniques évocateurs d'une allergie lors d'une précédente anesthésie."),
            ("S4.1.3", "Manifestations cliniques lors d'une exposition au latex (NP2), quelles que "
                       "soient les circonstances d'exposition."),
            ("S4.1.4", "Enfants multiopérés, notamment pour spina bifida ou myéloméningocèle (fréquence "
                       "élevée de sensibilisation au latex, NP1, et d'HSI au latex, NP1)."),
            ("S4.1.5", "Manifestations à l'ingestion d'avocat, kiwi, banane, châtaigne, sarrasin, etc., "
                       "ou exposition au Ficus benjamina (fréquence élevée de sensibilisation croisée "
                       "avec le latex, NP2)."),
        ], [20 * mm, PAGE_W - 2 * MARGIN - 20 * mm]),
    ]))
    story.append(Spacer(1, 3 * mm))
    story.append(no_reco_panel(
        "dans la population générale, il n'y a pas lieu de pratiquer avant une anesthésie un dépistage "
        "systématique d'une sensibilisation aux médicaments/produits utilisés en anesthésie (S4.2.2) : "
        "les valeurs prédictives positive et négative des tests dans la population générale ne sont "
        "pas suffisamment connues, et une valeur faussement positive peut avoir des conséquences "
        "néfastes (changement de technique non nécessairement adapté) -- le rapport bénéfice/risque "
        "d'un tel dépistage est inconnu. De même, chez les patients atopiques ou allergiques à un "
        "médicament non utilisé en anesthésie, il n'y a pas lieu de rechercher une sensibilisation aux "
        "produits anesthésiques (S4.2.3)."))
    story.append(Spacer(1, 2 * mm))
    story.append(P(
        "Chez les patients à risque définis ci-dessus, il faut proposer des investigations "
        "allergologiques avant toute anesthésie (S4.2.4) ; au-delà de 6 mois après la réaction, le "
        "risque de faux négatif existe. <b>Investigations :</b> patients S4.1.1 -- conserver les "
        "conclusions du bilan antérieur, tester les curares nouvellement commercialisés en cas "
        "d'allergie aux curares ; patients S4.1.2 -- en situation réglée, rechercher le protocole "
        "suspect et le transmettre à l'allergologue (protocole inconnu : tester tous les curares et le "
        "latex ; protocole identifié : tester les médicaments du protocole ancien et le latex, avec "
        "test de réintroduction pour les anesthésiques locaux après tests cutanés négatifs) ; en "
        "situation d'urgence, exclure le latex de l'environnement et utiliser une anesthésie "
        "locorégionale ou générale évitant curares et histaminolibérateurs (NP4) ; patients "
        "S4.1.3-S4.1.5 -- pricks au latex + IgE spécifiques du latex.", S_BODY_SM))
    story.append(Spacer(1, 3 * mm))
    story.append(P("<b>Situations particulières et demande de bilan allergologique (S4.3)</b> -- "
                    "contenu propre au document 2011, non repris dans la fiche compagnon 2025", S_CELL_B))
    story.append(Spacer(1, 1.5 * mm))
    story.append(simple_table(
        ["Situation", "Conduite pratique (source)"],
        [
            ["HSI suspectée à un AINS non sélectif",
             "Non urgent : bilan allergologique hospitalier avec tests de réintroduction réalistes. "
             "Urgence : pas d'anti-COX-1 ; anti-COX-2 utilisables (célécoxib, parécoxib) ; paracétamol "
             "possible à dose réduite (effet anti-COX-1 à fortes doses) (NP2)."],
            ["HSI suspectée au paracétamol",
             "Intervention non urgente : bilan en milieu hospitalier spécialisé avec tests de "
             "réintroduction réalistes."],
            ["Réaction à la morphine ou à la codéine",
             "Ne pas réinjecter morphine ou codéine ; tous les autres morphiniques sont utilisables."],
            ["Allergie alimentaire à l'œuf ou au soja",
             "Propofol utilisable chez l'allergique à l'œuf (un seul cas rapporté) ; l'huile purifiée "
             "de soja de l'excipient ne contre-indique pas le propofol en cas d'allergie au soja (NP4)."],
            ["Allergie aux fruits de mer ou au poisson",
             "L'allergène en cause n'étant pas l'iode, médicaments et badigeons iodés ne sont pas "
             "contre-indiqués (NP3)."],
            ["Allergie documentée à la protamine",
             "Contre-indication à la protamine. Un cas rapporté chez un allergique au poisson, mais une "
             "revue récente de la littérature ne justifie pas son éviction en cas d'allergie au "
             "poisson (NP2)."],
        ], [42 * mm, PAGE_W - 2 * MARGIN - 42 * mm]))
    return story

# ---------------------------------------------------------------------------
# Section 6 -- Question 5 : prévention (pièce centrale de cette fiche)
# ---------------------------------------------------------------------------
def _section_q5():
    story = []
    story.append(Spacer(1, 2 * mm))
    story.append(section_bar("Question 5 -- Prévention primaire et secondaire. Prémédication et technique anesthésique"))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<i>Cette question est le cœur de cette fiche : c'est le volet du document 2011 que la fiche "
        "compagnon Fiche_SFAR_Anaphylaxie_2025.pdf déclare elle-même hors de son propre champ "
        "(« reste du Champ 3 -- prévention programmée »).</i>", S_NOTE))
    story.append(Spacer(1, 2 * mm))
    story.append(KeepTogether([
        P("<b>Prévention primaire (S5.1)</b>", S_CELL_B),
        Spacer(1, 1.5 * mm),
        sect_table([
            ("S5.1.1-2", "La prévention primaire d'une sensibilisation correspond à la non-exposition "
                        "au médicament ou au matériau. Impossible pour les agents anesthésiques, mais "
                        "réalisable pour certains matériaux comme le latex ; l'administration des "
                        "curares doit être raisonnée, selon les indications de la curarisation (NP4)."),
            ("S5.1.3", "Il faut éviter l'exposition des patients au latex pour diminuer le risque de "
                       "sensibilisation. La décision institutionnelle de travailler en ambiance "
                       "« latex-free » est une prévention primaire efficace (NP1)."),
        ], [18 * mm, PAGE_W - 2 * MARGIN - 18 * mm]),
    ]))
    story.append(Spacer(1, 3 * mm))
    story.append(P("<b>Prévention secondaire (S5.2)</b>", S_CELL_B))
    story.append(Spacer(1, 1.5 * mm))
    story.append(sect_table([
        ("S5.2.1", "La meilleure prévention secondaire est la non-administration du médicament auquel "
                   "le sujet est sensibilisé ; il faut déterminer l'allergène responsable pour éviter "
                   "une récidive lors d'une utilisation ultérieure (NP2)."),
        ("S5.2.2", "Facteurs de risque de sensibilisation au latex : terrain atopique, exposition "
                   "professionnelle ou non répétée au latex, malformations urinaires (spina bifida, "
                   "vessie neurologique, etc.), malformations justifiant de multiples interventions."),
        ("S5.2.3", "Les patients sensibilisés au latex doivent être inscrits en <b>première position</b> "
                   "sur le programme opératoire, dans un environnement exempt de latex ; il faut "
                   "notifier la sensibilisation pendant tout le séjour hospitalier (service, bloc, "
                   "SSPI) (NP3)."),
        ("S5.2.4", "On peut utiliser un questionnaire préopératoire pour dépister la sensibilisation au "
                   "latex lors de la consultation préanesthésique, ce qui pourrait réduire l'incidence "
                   "des réactions au latex (NP4)."),
        ("S5.2.5", "En cas de suspicion de sensibilisation au latex, il faut adresser le patient en "
                   "consultation d'allergologie en préopératoire (NP3)."),
        ("S5.2.6", "Il faut établir des listes, régulièrement mises à jour, des matériels contenant du "
                   "latex dans chaque service d'anesthésie-réanimation, en collaboration avec la "
                   "pharmacie (NP3)."),
        ("S5.2.7", "Il ne faut pas faire de recherche systématique préanesthésique d'une sensibilisation "
                   "en dehors des patients à risque (NP2)."),
        ("S5.2.8", "Il faut adresser en consultation d'allergologie, avant une anesthésie, les patients "
                   "à risque de réaction allergique aux médicaments/matériaux périopératoires : "
                   "réaction inexpliquée à un allergène non identifié lors d'une anesthésie antérieure, "
                   "ou sujets allergiques connus à une classe de médicaments à utiliser, ou à risque "
                   "d'allergie au latex."),
        ("S5.2.9", "Il ne faut pas utiliser la méthode de la dose-test par voie intraveineuse pour "
                   "détecter les sujets sensibilisés aux médicaments anesthésiques (NP4)."),
    ], [18 * mm, PAGE_W - 2 * MARGIN - 18 * mm]))
    story.append(Spacer(1, 3 * mm))
    story.append(P("<b>Prémédication (S5.3)</b>", S_CELL_B))
    story.append(Spacer(1, 1.5 * mm))
    story.append(no_reco_panel(
        "aucune prémédication n'est efficace pour prévenir une réaction d'HSI <b>allergique</b> "
        "(S5.3.1). L'administration préalable d'un antihistaminique peut diminuer l'incidence et "
        "l'intensité des réactions d'HSI <b>non allergiques</b> (NP2), mais l'association d'un anti-H1 "
        "à un anti-H2 n'a pas montré de supériorité à l'anti-H1 seul (NP3). Il n'existe pas de preuve "
        "d'efficacité, en administration unique, de la prémédication par corticoïdes pour prévenir une "
        "réaction d'HSI (NP4) -- chez l'asthmatique sous corticoïdes au long cours, ceux-ci diminuent "
        "l'incidence de l'hyperréactivité bronchique per-anesthésique (NP3)."))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<i>Convergence avec la fiche compagnon 2025 : cette conclusion de 2011 (pas de prémédication "
        "antihistaminique/corticoïde systématique) rejoint celle, 14 ans plus tard, de "
        "Fiche_SFAR_Anaphylaxie_2025.pdf (R3.5) -- « il n'est probablement pas recommandé de "
        "prescrire systématiquement une prémédication (antihistaminiques, corticoïdes) aux patients à "
        "risque de réaction d'HSI péri-opératoire, hors mastocytose ».</i>", S_NOTE))
    story.append(Spacer(1, 3 * mm))
    story.append(P("<b>Anesthésie des patients allergiques ou susceptibles de l'être (S5.4)</b>", S_CELL_B))
    story.append(Spacer(1, 1.5 * mm))
    story.append(sect_table([
        ("S5.4.1", "Il est recommandé d'administrer l'antibioprophylaxie préopératoire au bloc, chez un "
                   "patient monitoré et éveillé, avant l'induction : l'imputabilité de l'antibiotique "
                   "est plus facile à déterminer et la réanimation, sans médicament cardiovasculaire "
                   "déjà reçu, est plus facile (NP4)."),
        ("S5.4.2", "Le choix de la technique se fait selon le sujet et l'acte. En urgence, en l'absence "
                   "de bilan allergologique, il faut privilégier les techniques locorégionales et les "
                   "techniques générales évitant curares et histaminolibérateurs, en environnement sans "
                   "latex (NP3)."),
        ("S5.4.3", "Le choix des agents se fait selon les données anamnestiques et les résultats du "
                   "bilan allergologique (NP2) : les halogénés n'ont jamais été incriminés dans une "
                   "HSI ; l'allergie au propofol et aux benzodiazépines est exceptionnelle ; les "
                   "réactions aux opiacés (morphine, codéine) sont le plus souvent non allergiques ; "
                   "tous les curares peuvent induire une HSI allergique -- le choix se fait selon "
                   "l'indication de la curarisation et les tests cutanés (NP3). En cas d'HSI allergique "
                   "à un curare, il faut rechercher systématiquement une sensibilité croisée avec les "
                   "autres curares disponibles pour proposer un curare pour les interventions "
                   "ultérieures (NP3)."),
    ], [18 * mm, PAGE_W - 2 * MARGIN - 18 * mm]))
    return story

# ---------------------------------------------------------------------------
# Section 7 -- Question 6 (résumé + renvoi) + Sources et traçabilité
# ---------------------------------------------------------------------------
def _section_q6_sources():
    story = []
    story.append(Spacer(1, 2 * mm))
    story.append(section_bar("Question 6 -- Traitement des réactions d'hypersensibilité immédiates (résumé et renvoi)"))
    story.append(Spacer(1, 2 * mm))
    story.append(info_panel(P(
        "<b>Résumé (document 2011) :</b> mesures générales dans tous les cas -- arrêt du produit "
        "suspecté, information de l'équipe chirurgicale, oxygène pur (NP4). Grade I : mesures "
        "générales généralement suffisantes. Grades II-III : oxygénation, contrôle des voies aériennes, "
        "<b>adrénaline IV titrée</b> (10 à 20 microg pour le grade II, 100 à 200 microg pour le grade "
        "III, renouvelable toutes les 1 à 2 minutes jusqu'à PAM >= 60 mmHg ; voie IM 0,3-0,5 mg si "
        "absence de voie veineuse), remplissage vasculaire rapide par cristalloïdes (colloïdes si "
        "volume &gt; 30 mL/kg), salbutamol inhalé ou IV en cas de bronchospasme, glucagon en cas de "
        "choc réfractaire chez un patient sous bêta-bloquants. Grade IV (arrêt cardiaque) : massage "
        "cardiaque, adrénaline 1 mg toutes les 1 à 2 minutes, mesures habituelles de réanimation. "
        "Seconde intention : corticoïdes pour atténuer les manifestations tardives, surveillance "
        "intensive >= 24 heures. Particularités décrites chez la femme enceinte (décubitus latéral "
        "gauche, extraction fœtale dès 25 SA si échec de réanimation à 5 minutes) et chez l'enfant "
        "(adrénaline 10 microg/kg en arrêt circulatoire, cristalloïdes 20 mL/kg puis colloïdes "
        "10 mL/kg).<br/><br/>"
        "<b>Renvoi explicite :</b> cette section est volontairement résumée. Le corpus de ce site "
        "contient une fiche dédiée et bien plus récente, <b>Fiche_SFAR_Anaphylaxie_2025.pdf</b> (RFE "
        "Sfar/SFA, Champ 4), qui détaille l'algorithme de traitement actualisé -- classification de "
        "gravité Ring & Messmer modifiée/CIM-11 OMS, posologies d'adrénaline par grade (IV, IVSE, IM), "
        "remplissage vasculaire, prise en charge du choc réfractaire (noradrénaline, bleu de "
        "méthylène, argipressine, ECLS) et annexe 7 (algorithme visuel de synthèse). Les principes de "
        "2011 (adrénaline IV titrée, mêmes seuils de dose pour les grades II-III, remplissage par "
        "cristalloïdes) restent globalement cohérents avec les recommandations actualisées de 2025, "
        "qui les précisent. <b>Se référer à la fiche dédiée pour la prise en charge aiguë du choc "
        "anaphylactique.</b>",
        S_BODY_SM), bg=BG_PANEL, border=TEAL))
    story.append(Spacer(1, 4 * mm))
    story.append(section_bar("Sources et traçabilité", color=GREY))
    story.append(Spacer(1, 2 * mm))
    story.append(P(
        "<b>Document source :</b> Malinovsky JM (président), Baillard C, Radu D (chargés de projet), "
        "et le comité d'organisation et les groupes de travail Sfar/SFA -- « Prévention du risque "
        "allergique péranesthésique. Texte court », Recommandations formalisées d'experts, Société "
        "française d'anesthésie et réanimation (Sfar) & Société française d'allergologie (SFA). Ann Fr "
        "Anesth Réanim 2011;30:212-222.", S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P("<b>Publication :</b> doi:10.1016/j.annfar.2010.12.002. Actualisation des "
                    "recommandations Sfar/SFAIC élaborées en 2001 et publiées en 2002.", S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>Méthodologie :</b> méthode GRADE modifiée, agréée par le comité des référentiels de la "
        "Sfar -- quatre niveaux de preuve globale NP1 (forte) à NP4 (très faible) attachés aux constats "
        "de l'argumentaire. Recherche exhaustive de « Grade A/B/C » et « accord "
        "professionnel » sur l'intégralité du texte source : aucune occurrence. En l'absence de "
        "tout marqueur de force par recommandation, cette fiche reproduit les phrases directives du "
        "texte source avec leur repère de paragraphe d'origine, sans grade fabriqué (voir panneau "
        "méthodologique en page 1).", S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>Couverture :</b> questions 1 à 5 reproduites intégralement (réalité du risque et "
        "substances responsables, mécanismes et physiopathologie, bilan diagnostique biologique et "
        "cutané -- Tableaux 2, 3 et 4 reproduits verbatim --, facteurs favorisants et bilan "
        "préanesthésique avec situations particulières, prévention primaire/secondaire -- "
        "prémédication -- choix de la technique anesthésique). Question 6 (traitement) résumée avec "
        "renvoi explicite vers Fiche_SFAR_Anaphylaxie_2025.pdf, qui la traite intégralement et de "
        "manière plus actuelle. La classification de gravité en 4 grades (Tableau 1 du document "
        "source, variante 2011 de Ring & Messmer) n'est pas retabulée : une version actualisée est déjà "
        "reproduite intégralement dans cette même fiche compagnon (Champ 4).", S_SOURCE))
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Avertissement :</b> ce document est une fiche de synthèse indépendante, produite pour un "
        "usage d'aide-mémoire. Elle reprend intégralement les questions 1 à 5 du texte court et résume "
        "la question 6 avec renvoi vers une fiche compagnon plus récente, mais ne remplace pas le "
        "texte intégral (argumentaire complet, annexes I à V) et n'est ni éditée ni validée par la "
        "Sfar ou la SFA. Document de 2011 : plusieurs éléments (tests cellulaires, dosages "
        "biologiques, classification de gravité) ont été précisés par la RFE Sfar/SFA plus récente sur "
        "l'hypersensibilité immédiate péri-opératoire (voir fiche dédiée de ce site). En cas de doute, "
        "se référer au texte intégral et/ou à un avis spécialisé.",
        S_BODY_SM), bg=GREY_LIGHT, border=GREY))
    return story

# Density check (post-first-build): sections built one-per-page each landed on a near-empty
# tail page (Q3(2/3,3/3) alone = 3p with its 3rd page ~15% full ; Q5 alone = 2p with its 2nd
# page ~25% full), for a wasteful 10-page total. Merging the short Question 4 into Question
# 3's spare tail, and Question 6 (already a brief summary) into Question 5's spare tail --
# both via combinator functions, no PageBreak forced between them, exactly the pattern used
# in fiche_aap_programmee.py's _section_4()/_section_7() -- measured at 8 pages total (verified
# below via _count_pages on the merged story). Reverted to separate sections would cost 2 extra
# near-empty pages for no content gain, so the merge is kept.
def _section_q3bc_q4():
    return _section_q3bc() + [Spacer(1, 4 * mm)] + _section_q4()

def _section_q5_q6():
    return _section_q5() + [Spacer(1, 4 * mm)] + _section_q6_sources()

SECTIONS = [
    ("Introduction, méthodologie et légende", _section_intro),
    ("Question 1 -- Réalité du risque et substances responsables", _section_q1),
    ("Question 2 -- Mécanismes et Question 3 (1/3) -- Bilan biologique", _section_q2_q3a),
    ("Question 3 (2/3, 3/3) et 4 -- tests, facteurs de risque, bilan préop", _section_q3bc_q4),
    ("Question 5 et 6 (résumé) -- prévention, technique et traitement", _section_q5_q6),
]

def _make_doc(path=None):
    return SimpleDocTemplate(path or OUT, pagesize=A4,
                              leftMargin=MARGIN, rightMargin=MARGIN,
                              topMargin=32 * mm, bottomMargin=16 * mm,
                              title="Fiche Sfar/SFA 2011 - Prévention du risque allergique péranesthésique",
                              author="Synthèse indépendante (source Sfar/SFA)")

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
    # Use a throwaway temp path (never OUT) for these measurement-only builds: reusing OUT here
    # was found (in fiche_aap_programmee.py) to corrupt page 1's header_band in the final build --
    # reproduced and fixed there by isolating counting passes to their own file. Same pattern here.
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
    print("Pages per section:")
    prev = 0
    for title, end_page in boundaries:
        print(f"  {end_page - prev} p. -- {title}")
        prev = end_page

if __name__ == "__main__":
    build()
