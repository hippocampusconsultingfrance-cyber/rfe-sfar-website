# -*- coding: utf-8 -*-
"""
Fiche de synthese - Conference de consensus commune Sfar/SRLF (2006), texte court du
jury : "Prise en charge hemodynamique du sepsis grave (nouveau-ne exclu)". Publiee
in extenso in Ann Fr Anesth Reanim 2006;25 et Reanimation 2006;15. Source : sources/
sepsis_hemodynamique.pdf (3 pages, texte court), sources/sepsis_hemodynamique.txt.
URL : https://sfar.org/prise-en-charge-hemodynamique-du-sepsis-grave-nouveau-ne-exclu/

CHAMP : prise en charge CIRCULATOIRE (hemodynamique) exclusivement du sepsis grave /
choc septique - le texte precise explicitement en introduction que les traitements
des autres defaillances d'organe (rein, foie, systeme nerveux, hemostase) ne sont pas
abordes ici. Ne pas confondre avec la fiche "sepsis" deja construite (prise en charge
GENERALE du sepsis, SRLF/SFAR RFE plus recente) : ce document, plus ancien (2006), est
un complement cible sur le volet hemodynamique/circulatoire, avec son propre jury et
sa propre echelle de grades.

METHODOLOGIE - PAS le systeme GRADE 1+/1-/2+/2-/AE. La source cote chaque enonce par
une seule lettre "grade X" (echelle A/B/C/D/E, precedent identique a fiche_hsa.py qui
utilise la meme echelle a lettre unique). Comptage exhaustif par regex "grade [A-Z]"
sur le texte extrait : 18x E, 10x B, 3x C, 2x D = 33 enonces gradues au total, AUCUNE
occurrence de grade A dans le corps du texte. Ce texte court ne definit nulle part la
signification de chaque lettre (l'echelle complete est presumee figurer dans
l'argumentaire long de cette conference, non disponible ici) - disclosure explicite
dans le panneau d'introduction et la legende, plutot qu'une definition inventee.

GRADE_COLORS etendu localement (meme precedent que fiche_hsa.py / fiche_corticotherapie.py)
avec les lettres B/C/D/E de cette source, distinctes des cles GRADE 1+/2+/etc.

TABLEAU REPRODUIT INTEGRALEMENT (texte extractible, pas une image) : Tableau 1 -
definitions du sepsis / sepsis grave / choc septique (colonnes adulte(A)/enfant(E)).

FIGURE 1 REDESSINEE (contenu integral, mise en page simplifiee) : le schema source est
un algorithme decisionnel a 3 etapes avec branches OUI/NON, boucle de reevaluation et
reperes temporels (60/90 min, 6 heures) verifie par rendu visuel de la page 3 a 200dpi.
Meme precedent que fiche_ira.py (funnel_diagram) : redessin structure en panneaux
empiles preservant 100% du contenu textuel et des reperes temporels, plutot qu'une
reproduction pixel-exacte des fleches/encadres imbriques - disclosure explicite dans
la fiche. Aucune information de la figure source n'est omise (toutes les puces des 3
etapes, les 2 branches de decision, la boucle de reevaluation, les 2 reperes temporels
adulte/enfant).

Particularites pediatriques du texte source (sous-sections 1.1/2.5/3.3/4.1 + valeurs en
italique du Tableau 1 et de la Figure 1) toutes reproduites et signalees explicitement
(mention "(Pédiatrie)") plutot que fondues silencieusement dans les recommandations
adulte.

ANOMALIES SOURCE DISCLOSEES (trouvees par un audit independant en sous-agent, blind au
premier jet de cette fiche, puis chacune verifiee ici par rendu de la page source a
600dpi - jamais silencieusement corrigees) :
  - Tableau 1 : la source imprime litteralement "> 176 mmol/l" (creatininemie) et
    "> 78 mmol/l" (bilirubine) - confirme a 600dpi, pas un artefact d'extraction. Ces
    valeurs sont cliniquement impossibles en mmol/l et correspondent aux seuils standards
    en µmol/l des criteres de sepsis grave (ACCP/SCCM) - reproduites en µmol/l comme tres
    probable coquille de la source, avec disclosure explicite en note de bas de tableau
    (call-out †) plutot qu'une correction silencieuse.
  - Tableau 1 : les valeurs enfant du critere respiratoire (SpO2 > 92%) et du temps de
    recoloration capillaire (> 5 sec) ne portent AUCUN repere "(E)" explicite dans la
    source (confirme a 600dpi) - contrairement a toutes les autres lignes du tableau.
    Reproduites a leur place sans "(E)" invente, avec disclosure (call-out *).
  - Q4.1 (ACTH) : la source imprime un blanc typographique entre "cortisolemie" et
    "9 µg/dl" - confirme a 600dpi, aucun symbole n'est imprime a cet endroit (pas un
    artefact d'extraction). Le "<" reproduit ici est la definition usuelle de la
    non-reponse au test au Synacthene, avec disclosure explicite (call-out ‡) plutot
    qu'une insertion silencieuse.
  - Q1 : la phrase de contexte non gradee "Toutes les proprietes cardiaques, a
    l'exception du debit sanguin coronaire, sont potentiellement modifiees par le
    sepsis" (precede 1.4 dans la source) est reproduite en note - omise dans un premier
    jet, ajoutee apres l'audit independant pour la couverture a 100%.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from style import *
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.units import mm

OUT = os.path.join(os.path.dirname(__file__), "..", "output",
                    "Fiche_SFAR_SRLF_Sepsis_Hemodynamique_2006.pdf")
OUT = os.path.abspath(OUT)

SOURCE_TXT = ("Source : Conférence de consensus commune Sfar/SRLF (2006), texte court du jury « Prise "
              "en charge hémodynamique du sepsis grave (nouveau-né exclu) » — Ann Fr Anesth Réanim "
              "2006;25, Réanimation 2006;15. Fiche de synthèse non officielle : se référer au texte "
              "intégral.")

# Extension locale de GRADE_COLORS - lettres B/C/D/E de cette source (voir docstring).
GRADE_COLORS["B"] = (TEAL, WHITE)
GRADE_COLORS["C"] = (AMBER, WHITE)
GRADE_COLORS["D"] = (NAVY, WHITE)
GRADE_COLORS["E"] = (GREY, WHITE)


def P(txt, style=S_CELL):
    return Paragraph(txt, style)


def chip(label, **kw):
    return grade_chip(label, width=13 * mm, **kw)


def reco_table(rows, col_widths):
    """rows: (ref, text, grade_letter)"""
    data = [[P("Réf.", S_HEAD_W), P("Recommandation du jury", S_HEAD_W), P("Grade", S_HEAD_W_C)]]
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


RECO_COLS = [13 * mm, PAGE_W - 2 * MARGIN - 13 * mm - 15 * mm, 15 * mm]


def legend_flowable():
    items = [("B", "« Grade B »"), ("C", "« Grade C »"),
             ("D", "« Grade D »"), ("E", "« Grade E »")]
    content_w = PAGE_W - 2 * MARGIN
    n = len(items)
    chip_w = 13 * mm
    text_w = (content_w - n * chip_w) / n
    row_cells, col_widths = [], []
    for g, txt in items:
        row_cells.append(chip(g))
        row_cells.append(P(txt, S_BADGE_HEAD))
        col_widths += [chip_w, text_w]
    row = Table([row_cells], colWidths=col_widths)
    row.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                              ("LEFTPADDING", (0, 0), (-1, -1), 1), ("RIGHTPADDING", (0, 0), (-1, -1), 1)]))
    return row


def definitions_table():
    """Tableau 1 de la source, reproduit integralement (colonnes Variables / Definitions)."""
    sirs = P(
        "Température &gt; 38,3°C ou &lt; 36°C<br/>"
        "Pouls &gt; 90 c/min (A), &gt; 2 DS pour l'âge (E)<br/>"
        "Fréquence respiratoire &gt; 20 c/min (A), &gt; 2 DS pour l'âge (E)<br/>"
        "Glycémie &gt; 7,7 mmol/l<br/>"
        "Leucocytes &gt; 12 000/mm³ ou &lt; 4 000/mm³ ou &gt; 10 % de formes immatures<br/>"
        "Altération des fonctions supérieures<br/>"
        "Temps de recoloration capillaire &gt; 2 sec (A), &gt; 5 sec<sup>*</sup><br/>"
        "Lactatémie &gt; 2 mmol/l", S_CELL)
    sepsis_grave = P(
        "Sepsis + [ lactates &gt; 4 mmol/l <b>ou</b> hypotension artérielle avant remplissage "
        "<b>ou</b> dysfonction d'organe (une seule suffit) ] :<br/>"
        "— respiratoire (PaO2/FiO2 &lt; 300 (A), FiO2 &gt; 0,5 pour SpO2 &gt; 92 %<sup>*</sup>)<br/>"
        "— rénale (créatininémie &gt; 176 µmol/l<sup>†</sup> (A), &gt; 2× normale ou oligurie (E))<br/>"
        "— coagulation (INR &gt; 1,5 (A), &gt; 2 (E))<br/>"
        "— hépatique (TP &gt; 60 s, bilirubine &gt; 78 µmol/l<sup>†</sup> (A+E), transaminases &gt; 2× normale)<br/>"
        "— thrombocytopénie (&lt; 100 000/mm³ (A), 80 000/mm³ (E))<br/>"
        "— fonctions supérieures (GCS &lt; 13 (A), &lt; 11 (E))", S_CELL)
    data = [
        [P("Variables", S_HEAD_W), P("Définitions", S_HEAD_W)],
        [P("Réponse inflammatoire systémique<br/>(≥ 2 des critères suivants)", S_CELL_B), sirs],
        [P("Sepsis", S_CELL_B), P("Réponse inflammatoire systémique + infection présumée ou identifiée", S_CELL)],
        [P("Sepsis grave", S_CELL_B), sepsis_grave],
        [P("Choc septique", S_CELL_B), P(
            "Sepsis grave + hypotension artérielle malgré le remplissage vasculaire "
            "(20-40 ml/kg (A), &gt; 40 ml/kg (E))", S_CELL)],
    ]
    col_w = [42 * mm, PAGE_W - 2 * MARGIN - 42 * mm]
    t = Table(data, colWidths=col_w, repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY), ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTNAME", (0, 0), (-1, 0), FONT_BOLD), ("FONTSIZE", (0, 0), (-1, 0), 8),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.5, GREY_LIGHT),
        ("TOPPADDING", (0, 0), (-1, -1), 3.4), ("BOTTOMPADDING", (0, 0), (-1, -1), 3.4),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("BACKGROUND", (0, 1), (-1, 1), BG_PANEL),
        ("BACKGROUND", (0, 3), (-1, 3), BG_PANEL),
    ]))
    return t


def flow_panel(title, bullets, color=TEAL_DARK):
    """Panneau d'etape de la Figure 1 redessinee - titre + liste a puces."""
    content_w = PAGE_W - 2 * MARGIN
    story = [section_bar(title, color=color, height=6.6 * mm, fontsize=9.6)]
    story.append(Spacer(1, 1.3 * mm))
    txt = "<br/>".join("• " + b for b in bullets)
    story.append(info_panel(P(txt, S_BODY_SM), bg=BG_PANEL, border=color))
    return KeepTogether(story)


TOTAL_PAGES = {"n": 4}


def on_page(canvas, doc, page_title):
    header_band(canvas, doc, "SFAR / SRLF — CONFÉRENCE DE CONSENSUS 2006 — FICHE DE SYNTHÈSE",
                "Prise en charge hémodynamique du sepsis grave",
                page_title, icon_fn=lambda c, x, y: icon_drop(c, x, y, 13 * mm), color=RED)
    footer_band(canvas, doc, SOURCE_TXT, f"Page {doc.page} / {TOTAL_PAGES['n']}")


# ---------------------------------------------------------------------------
def _section_intro():
    story = [Spacer(1, 3 * mm)]
    story.append(info_panel(P(
        "<b>Champ de la conférence :</b> prise en charge <b>circulatoire (hémodynamique)</b> "
        "exclusivement du sepsis grave et du choc septique — le jury précise explicitement que "
        "les thérapeutiques des défaillances d'organe éventuellement associées (rein, foie, "
        "système nerveux, hémostase…) ne sont <b>pas</b> envisagées dans ce texte. Conférence de "
        "consensus commune Sfar/SRLF, 2006, texte court du jury. Nouveau-né exclu du champ ; les "
        "particularités pédiatriques (enfant) sont en italique dans le texte source et signalées "
        "« (Pédiatrie) » dans cette fiche. <b>5 questions</b> : (1) cibles thérapeutiques, "
        "(2) modalités de l'expansion volémique, (3) place des inotropes et vasoactifs, "
        "(4) traitements complémentaires, (5) stratégie thérapeutique globale (algorithme)."
        "<br/><br/>"
        "<b>Méthodologie de cotation :</b> chaque énoncé porte une seule lettre "
        "« grade X ». <b>33 recommandations graduées</b> recensées par comptage exhaustif : "
        "18 grade E, 10 grade B, 3 grade C, 2 grade D — <b>aucune occurrence de grade A</b> dans "
        "le corps du texte. Ce texte court ne redéfinit nulle part la signification de chaque "
        "lettre (échelle présumée détaillée dans l'argumentaire scientifique long de cette "
        "conférence, non disponible ici) : disclosure explicite plutôt qu'une définition "
        "inventée — voir légende ci-dessous.", S_BODY), bg=BG_PANEL, border=RED))
    story.append(Spacer(1, 2 * mm))
    story.append(section_bar("Légende des cotations (lettres imprimées telles quelles par le jury)"))
    story.append(Spacer(1, 2 * mm))
    story.append(legend_flowable())
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "Répartition exacte des 33 énoncés gradués de ce texte : 18×E, 10×B, 3×C, 2×D "
        "(vérifiée par comptage automatisé sur le texte source extrait).", S_NOTE))
    return story


def _section_table1_q1():
    story = [Spacer(1, 3 * mm)]
    story.append(section_bar("Tableau 1 — Définitions du sepsis, du sepsis grave et du choc septique"))
    story.append(Spacer(1, 2 * mm))
    story.append(definitions_table())
    story.append(Spacer(1, 1.5 * mm))
    story.append(P("(A) = adulte, (E) = enfant. Valeurs propres à la pédiatrie reproduites telles "
                    "qu'imprimées par la source (en italique dans le texte original).", S_NOTE))
    story.append(Spacer(1, 1 * mm))
    story.append(P(
        "<sup>*</sup> Anomalie source disclosée : contrairement aux autres lignes de ce tableau, ces "
        "deux valeurs \"enfant\" (recoloration capillaire &gt; 5 sec ; SpO2 &gt; 92 %) ne portent "
        "explicitement aucun repère « (E) » dans le texte source (vérifié par rendu à 600 dpi) — "
        "reproduites ici à la même place que la valeur adulte correspondante, sans ajouter le repère "
        "« (E) » que la source elle-même n'imprime pas.<br/>"
        "<sup>†</sup> Anomalie source disclosée : le texte source imprime littéralement "
        "« &gt; 176 mmol/l » et « &gt; 78 mmol/l » pour la créatininémie et la bilirubine (vérifié par "
        "rendu à 600 dpi — ce n'est pas un artefact d'extraction de texte, l'unité est bien "
        "« mmol/l » sur la page imprimée). Ces valeurs sont cliniquement impossibles en mmol/l "
        "(176 mmol/l ou 78 mmol/l de créatininémie/bilirubinémie seraient incompatibles avec la vie) "
        "et correspondent aux seuils standards en <b>µmol/l</b> des critères de sepsis grave "
        "(ACCP/SCCM) — reproduites ici en µmol/l comme très probable coquille d'origine de la source, "
        "plutôt que reproduites littéralement avec une valeur trompeuse.", S_NOTE))
    story.append(Spacer(1, 3 * mm))

    story.append(section_bar("Question 1 — Quelles sont les cibles thérapeutiques ?"))
    story.append(Spacer(1, 2 * mm))
    story.append(reco_table([
        ("1.1", "La diurèse horaire et l'évolution biologique de la fonction rénale et de la "
                "lactatémie au cours du traitement sont les seuls paramètres de surveillance de la "
                "microcirculation disponibles (les possibilités de monitorage de la microcirculation "
                "sont limitées et les thérapeutiques spécifiques inexistantes).", "E"),
        ("1.2", "Le remplissage vasculaire précoce est recommandé : il augmente le transport de "
                "l'oxygène, corrige l'hypotension artérielle et améliore le pronostic des patients "
                "en sepsis grave.", "B"),
        ("1.3", "En dehors du traitement de la vasoplégie par amines vasoconstrictrices, il "
                "n'existe pas de thérapeutique spécifique de la dysfonction vasculaire.", "B"),
        ("1.4", "Seuls 10 à 20 % des patients adultes évoluent vers la défaillance cardiaque "
                "(index cardiaque et SvO2 bas persistant après expansion volémique) ; le traitement "
                "inotrope positif est réservé à ces patients.", "B"),
        ("1.5 P", "<i>(Pédiatrie)</i> Le sepsis grave de l'enfant se caractérise par une défaillance "
                   "myocardique plus fréquente et une hypovolémie majeure répondant bien au "
                   "remplissage. Le diagnostic est difficile (hypotension souvent tardive) : la "
                   "rapidité du diagnostic et d'une expansion volémique agressive associée à une "
                   "antibiothérapie très précoce est recommandée (mortalité pédiatrique plus faible "
                   "que chez l'adulte ; le Purpura fulminans mérite d'être individualisé).", "D"),
    ], RECO_COLS))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "Contexte (non gradé, précède 1.4 dans le texte source) : toutes les propriétés cardiaques, "
        "à l'exception du débit sanguin coronaire, sont potentiellement modifiées par le sepsis.",
        S_NOTE))
    return story


def _section_q2():
    story = [Spacer(1, 1.5 * mm)]
    story.append(section_bar("Question 2 — Modalités de l'expansion volémique (y compris transfusion)"))
    story.append(Spacer(1, 2 * mm))
    story.append(P("<b>2.1. Diagnostic et monitorage du déficit volémique — Phase initiale</b>", S_H2))
    story.append(Spacer(1, 1 * mm))
    story.append(reco_table([
        ("2.1a", "L'urgence est au remplissage vasculaire systématique (hypovolémie constante) : "
                 "aucun indice prédictif de la réponse au remplissage n'est nécessaire pour sa mise "
                 "en œuvre. Objectif recommandé : PAM &gt; 65 mmHg.", "C"),
        ("2.1b", "Lorsque l'hypotension engage le pronostic vital (ex. PAD &lt; 40 mmHg), le "
                 "recours aux agents vasopresseurs doit être immédiat, quelle que soit la volémie.", "E"),
    ], RECO_COLS))
    story.append(Spacer(1, 2 * mm))
    story.append(P("<b>Après la phase initiale</b> — poursuite du remplissage en utilisant des "
                    "indices prédictifs dynamiques de l'état de réserve de précharge.", S_BODY_SM))
    story.append(P("Grade D", S_NOTE))
    story.append(Spacer(1, 2 * mm))

    story.append(P("<b>2.2–2.3. Choix du soluté, quantité, rythme et modalité d'administration</b>", S_H2))
    story.append(Spacer(1, 1 * mm))
    story.append(reco_table([
        ("2.2", "Cristalloïdes/colloïdes titrés pour un même objectif hémodynamique ont une "
                "efficacité équivalente ; compte tenu d'un coût moindre et de leur innocuité, les "
                "cristalloïdes isotoniques sont recommandés, surtout à la phase initiale du choc "
                "(produits sanguins, dextrans et amidons de PM &gt; 150 kDa proscrits comme solutés "
                "de remplissage).", "B"),
        ("2.3a", "Le remplissage s'effectue par séquences de 500 ml de cristalloïdes isotoniques "
                 "en 15 min.", "E"),
        ("2.3b", "Ces séquences doivent être répétées jusqu'à obtention d'une PAM &gt; 65 mmHg, en "
                 "l'absence de signes d'œdème pulmonaire.", "B"),
        ("2.3c", "Si l'objectif de PAM n'est pas atteint, le recours aux amines vasopressives est "
                 "indiqué.", "E"),
    ], RECO_COLS))
    story.append(Spacer(1, 2 * mm))

    story.append(P("<b>2.4. Place de la transfusion sanguine</b>", S_H2))
    story.append(Spacer(1, 1 * mm))
    story.append(reco_table([
        ("2.4a", "Objectif : taux d'hémoglobine de 8 à 9 g/dl.", "C"),
        ("2.4b", "Des taux différents peuvent être justifiés par une intolérance clinique et/ou la "
                 "mesure de la SvcO2.", "E"),
    ], RECO_COLS))
    story.append(Spacer(1, 2 * mm))

    story.append(P("<b>2.5. Particularités pédiatriques</b>", S_H2))
    story.append(Spacer(1, 1 * mm))
    story.append(reco_table([
        ("2.5a P", "<i>(Pédiatrie)</i> Au cours de la première heure, un remplissage vasculaire "
                    "jusqu'à 60 ml/kg est recommandé car il réduit la mortalité.", "E"),
        ("2.5b P", "<i>(Pédiatrie)</i> Pour les mêmes raisons que chez l'adulte, les cristalloïdes "
                    "sont préférés.", "B"),
    ], RECO_COLS))
    return story


def _section_q3():
    story = [Spacer(1, 1.5 * mm)]
    story.append(section_bar("Question 3 — Place des médicaments inotropes positifs et vasoactifs"))
    story.append(Spacer(1, 2 * mm))
    story.append(P("<b>3.1. Traitement vasoconstricteur</b>", S_H2))
    story.append(Spacer(1, 1 * mm))
    story.append(reco_table([
        ("3.1a", "Les vasoconstricteurs doivent être utilisés si le remplissage vasculaire ne "
                 "permet pas d'obtenir une PAM &gt; 65 mmHg.", "B"),
        ("3.1b", "Leur utilisation précoce est recommandée : elle permet de limiter la survenue "
                 "des défaillances viscérales.", "E"),
        ("3.1c", "La noradrénaline, amine vasoconstrictrice la plus puissante, doit être utilisée "
                 "en première intention.", "E"),
        ("3.1d", "La vasopressine (0,01 à 0,04 U/min) ou la terlipressine (bolus de 1 à 2 mg) peut "
                 "être utilisée dans les chocs réfractaires.", "E"),
    ], RECO_COLS))
    story.append(Spacer(1, 2 * mm))

    story.append(P("<b>3.2. Traitement inotrope positif</b>", S_H2))
    story.append(Spacer(1, 1 * mm))
    story.append(reco_table([
        ("3.2a", "L'adjonction systématique des inotropes n'est pas recommandée.", "E"),
        ("3.2b", "Chez un patient ayant bénéficié d'un traitement bien conduit (optimisation de la "
                 "volémie, vasopresseurs, correction d'une anémie), l'indication des inotropes ne "
                 "peut pas se justifier par une valeur isolée de débit cardiaque : elle doit "
                 "toujours être associée à une SvcO2 &lt; 70 %.", "B"),
        ("3.2c", "Il est recommandé d'évaluer l'efficacité du traitement inotrope sur "
                 "l'amélioration de la SvcO2, la baisse de la lactatémie et la surveillance des "
                 "paramètres de fonction myocardique.", "E"),
        ("3.2d", "L'association dobutamine + noradrénaline (composantes α1/β2 adaptées séparément) "
                 "est recommandée en première intention ; l'adrénaline apparaît aussi efficace mais "
                 "ses effets métaboliques peuvent restreindre son utilisation (non gradé).", "E"),
    ], RECO_COLS))
    story.append(Spacer(1, 2 * mm))

    story.append(P("<b>3.3. Particularités pédiatriques</b>", S_H2))
    story.append(Spacer(1, 1 * mm))
    story.append(reco_table([
        ("3.3a P", "<i>(Pédiatrie)</i> La noradrénaline peut être recommandée en première "
                    "intention.", "E"),
        ("3.3b P", "<i>(Pédiatrie)</i> Les inhibiteurs de la phosphodiestérase de type III peuvent "
                    "être envisagés dans les états de bas débit cardiaque à PA normale.", "C"),
    ], RECO_COLS))
    return story


def _section_q4():
    story = [Spacer(1, 1.5 * mm)]
    story.append(section_bar("Question 4 — Place des traitements complémentaires"))
    story.append(Spacer(1, 2 * mm))
    story.append(reco_table([
        ("4.1", "La corticothérapie est recommandée précocement au cours du choc septique chez "
                "les patients non répondeurs à l'injection de 250 µg d'ACTH (augmentation de la "
                "cortisolémie &lt; 9 µg/dl<sup>‡</sup>).", "B"),
        ("4.2", "Hémisuccinate d'hydrocortisone 200 à 300 mg/j, pendant au moins cinq jours, suivi "
                "d'une décroissance progressive.", "E"),
        ("4.3", "La protéine C activée recombinante d'origine humaine ne doit pas être utilisée "
                "dans l'indication hémodynamique exclusive.", "E"),
        ("4.4", "L'hémofiltration n'est pas recommandée pour la prise en charge hémodynamique du "
                "choc septique en dehors d'une défaillance rénale associée.", "E"),
        ("4.5", "Les autres techniques d'épuration des médiateurs ne sont pas recommandées.", "E"),
        ("4.6", "Il est recommandé de ne pas utiliser les inhibiteurs non sélectifs de la NO "
                "synthase inductible : ils augmentent la mortalité.", "B"),
        ("4.7 P", "<i>(Pédiatrie)</i> Dose d'hydrocortisone recommandée : 1 mg/kg toutes les six "
                   "heures.", "E"),
    ], RECO_COLS))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<sup>‡</sup> Anomalie source disclosée (4.1) : le texte source imprime un blanc typographique "
        "entre « cortisolémie » et « 9 µg/dl » (vérifié par rendu à 600 dpi — aucun symbole n'est "
        "imprimé, ce n'est pas un artefact d'extraction de texte). Le seuil « &lt; 9 µg/dl » reproduit "
        "ici correspond à la définition usuelle de la non-réponse au test au Synacthène (delta "
        "cortisol insuffisant), mais ce symbole n'est pas visible dans le document source.", S_NOTE))
    return story


def _section_q5_figure():
    story = [Spacer(1, 1.5 * mm)]
    story.append(section_bar("Question 5 — Quelle stratégie thérapeutique ? (Fig. 1)"))
    story.append(Spacer(1, 2 * mm))
    story.append(P(
        "La rapidité d'instauration du traitement conditionne le pronostic des états septiques "
        "graves et doit reposer sur une chaîne de prise en charge et des protocoles thérapeutiques "
        "formalisés. En cas de détresse vitale (hypotension artérielle menaçante, insuffisance "
        "respiratoire aiguë, coma…), le patient est directement admis en réanimation.", S_BODY))
    story.append(Spacer(1, 2 * mm))
    story.append(info_panel(P(
        "<b>Figure 1 redessinée :</b> le schéma source est un algorigramme à encadrés imbriqués et "
        "flèches (rendu vérifié à 200 dpi). Restructuré ci-dessous en 3 panneaux séquentiels pour "
        "la lisibilité, en conservant l'intégralité du contenu — toutes les puces, les 2 branches "
        "de décision (OUI/NON) et les 2 repères temporels adulte/enfant — plutôt qu'une "
        "reproduction pixel-exacte des encadrés/flèches (même principe que le funnel_diagram de la "
        "fiche IRA 2015). Les éléments propres à l'enfant sont signalés « (Pédiatrie) », comme "
        "dans le texte source (italique).", S_BODY_SM), bg=GREY_LIGHT, border=GREY))
    story.append(Spacer(1, 2.5 * mm))

    story.append(flow_panel(
        "ÉTAPE 1 (0-60 min enfant / 0-90 min adulte) — Mesures d'urgence, orientation hors détresse vitale",
        ["Monitorage minimal ; O2 pour SpO2 ≥ 95 %",
         "REMPLISSAGE : cristalloïdes 500 ml/15 min répétés qsp PAM &gt; 65 mmHg <i>(ou selon l'âge — "
         "(Pédiatrie) : volume 60 ml/kg sur 1 h)</i>",
         "Prélèvements standardisés ; contrôle du foyer infectieux",
         "→ Réévaluation : normalisation hémodynamique + absence de comorbidité + pathologie "
         "infectieuse de bon pronostic + lactate &lt; 4 mmol/l ?",
         "<b>SI OUI</b> → unité de surveillance continue (objectifs : PAM &gt; 65 mmHg ou selon "
         "l'âge, diurèse &gt; 0,5 ml/kg/h)",
         "<b>SI NON</b> → passage à l'étape 2 (réanimation)"], color=TEAL_DARK))
    story.append(Spacer(1, 2.5 * mm))

    story.append(flow_panel(
        "ÉTAPE 2 (jusqu'à 6 heures) — Réanimation : objectifs et moyens",
        ["Moyens : KT central et artériel ; bilan sanguin (lactate, test ACTH) ; ventilation "
         "mécanique ; prélèvements microbiologiques ; contrôle du foyer infectieux ; traitement par "
         "hémisuccinate d'hydrocortisone (HSHC)",
         "Objectifs : absence d'hypoperfusion clinique + PAM &gt; 65 mmHg (ou selon l'âge) + "
         "diurèse &gt; 0,5 ml/kg/h + SvcO2 &gt; 70 %",
         "Boucle de réévaluation : « objectifs non atteints » → poursuite du remplissage et de la "
         "noradrénaline ? → puis, si besoin : transfusion qsp Hb &gt; 8 g/dl, remplissage "
         "complémentaire si réserve de précharge, dobutamine (± adrénaline) selon monitorage "
         "hémodynamique → réévaluation jusqu'à « objectifs atteints »"], color=NAVY))
    story.append(Spacer(1, 2.5 * mm))

    story.append(flow_panel(
        "ÉTAPE 3 — Adaptation des traitements",
        ["Maintien des objectifs",
         "Arrêt des corticoïdes si patient répondeur",
         "Désescalade thérapeutique si stabilisation avérée",
         "Envisager la vasopressine si inefficacité de la noradrénaline",
         "Discuter les inhibiteurs des phosphodiestérases <i>(Pédiatrie)</i>"], color=GREEN))
    return story


def _section_sources():
    story = [Spacer(1, 4 * mm)]
    story.append(section_bar("Sources et traçabilité", color=GREY))
    story.append(Spacer(1, 2 * mm))
    story.append(P(
        "<b>Document source :</b> Conférence de consensus commune Sfar/SRLF (2006), texte court du "
        "jury « Prise en charge hémodynamique du sepsis grave (nouveau-né exclu) » / « Haemodynamic "
        "management of severe sepsis (excluding neonates) ». Publication e-only : Ann Fr Anesth "
        "Réanim 2006 ; vol. 25 — Réanimation 2006 ; vol. 15. © 2006 Elsevier SAS.",
        S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>Méthodologie :</b> cotation à lettre unique (grade B/C/D/E dans ce texte, aucun grade A "
        "utilisé) — non-GRADE. Signification de chaque lettre non redéfinie dans ce texte court "
        "(voir disclosure page 1).", S_SOURCE))
    story.append(P(
        "<b>URL source :</b> https://sfar.org/prise-en-charge-hemodynamique-du-sepsis-grave-nouveau-ne-exclu/",
        S_SOURCE))
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Avertissement :</b> ce document est une fiche de synthèse indépendante, produite pour "
        "un usage d'aide-mémoire. Il reprend l'intégralité des 33 recommandations graduées, du "
        "tableau des définitions et de l'algorithme décisionnel de cette conférence, mais ne "
        "remplace pas le texte intégral (argumentaire complet, références bibliographiques) et "
        "n'est ni édité ni validé par la Sfar ou la SRLF. Conférence de 2006 : se référer également, "
        "en complément, aux données et pratiques plus récentes sur la prise en charge du sepsis "
        "(Surviving Sepsis Campaign, RFE françaises postérieures) et à un avis spécialisé en cas de "
        "doute.",
        S_BODY_SM), bg=GREY_LIGHT, border=GREY))
    return story


def _section_1():
    return _section_intro() + [Spacer(1, 2 * mm)] + _section_table1_q1()


def _section_2():
    return _section_q2() + [Spacer(1, 3 * mm)] + _section_q3()


def _section_3():
    return _section_q4() + [Spacer(1, 3 * mm)] + _section_q5_figure() + _section_sources()


SECTIONS = [
    ("Introduction, méthodologie & Questions 1 à 3", lambda: _section_1() + [Spacer(1, 3 * mm)] + _section_2()),
    ("Questions 4-5 — Traitements complémentaires, stratégie & traçabilité", _section_3),
]


def _make_doc(path=None):
    return SimpleDocTemplate(path or OUT, pagesize=A4,
                              leftMargin=MARGIN, rightMargin=MARGIN,
                              topMargin=32 * mm, bottomMargin=16 * mm,
                              title="Fiche SFAR/SRLF 2006 - Prise en charge hémodynamique du sepsis grave",
                              author="Synthèse indépendante (source SFAR/SRLF)")


def _silent_page(canvas, doc_):
    pass


def _build_upto(section_fns):
    # Originally 3 sections each forced onto a fresh page: with ~1.3 pages of
    # content per section that left pages 2/4/6 under 30% full (checked visually).
    # Merged down to 2 sections (see SECTIONS) so the one remaining PageBreak still
    # keeps each page's header title accurate to what it shows, without wasting a
    # near-empty page after every section.
    story = []
    for i, fn in enumerate(section_fns):
        if i > 0:
            story.append(PageBreak())
        story.extend(fn())
    return story


def _count_pages(story_flowables):
    # Throwaway measurement builds must NEVER write to OUT (see CLAUDE.md) - reusing OUT
    # here was found in a prior fiche to silently corrupt page 1's header_band in the final
    # build. Always use a fresh tempfile.mktemp() path for these measurement passes.
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
