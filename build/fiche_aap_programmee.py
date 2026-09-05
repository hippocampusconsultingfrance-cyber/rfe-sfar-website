# -*- coding: utf-8 -*-
"""
Fiche de synthese - GIHP & GFHT, en collaboration avec la SFAR (2018)
"Gestion des agents antiplaquettaires (AAP) pour une procedure invasive programmee" -
Propositions (pas une RFE GRADE classique). Anne Godier et al., Anesth Reanim 2018
(ANREA-314), doi 10.1016/j.anrea.2018.01.002. Companion document de la fiche deja
construite pour la procedure invasive NON programmee / hemorragie (fiche_aap_urgence.py),
meme corpus GIHP/GFHT/SFAR, meme annee.

METHODOLOGIE : PAS de systeme GRADE (pas de niveaux 1+/1-/2+/2-). Les propositions ont
ete redigees par 5 groupes de travail GIHP/GFHT puis soumises a un vote (n=37) : une
proposition est retenue si >=50% d'accord (et <20% d'opposition) ; l'accord est qualifie
de "fort" si >=70%. Chaque proposition individuelle du corps du texte porte le tag
explicite "(accord fort)" - aucune autre mention de force n'est imprimee nulle part dans
le document.

DIVERGENCE SOURCE-INTERNE (disclosure, non resolue silencieusement) : le Resume de la
source affirme "Ces propositions ont ete discutees et validees par vote ; toutes sauf une
ont fait l'objet d'un accord fort" (une exception implicite). Une verification directe,
item par item, de chaque proposition imprimee dans le corps du texte (comptage exhaustif
des occurrences "(accord fort)", et verification visuelle a 200dpi pour les propositions
associees a la figure 1 / tableau I qui ne sont pas du texte extractible pur) montre que
TOUTES les propositions retrouvees portent le tag "(accord fort)", sans qu'aucune ne porte
un tag different ou plus faible. L'exception annoncee par le resume n'est donc identifiable
nulle part dans le corps du document - elle n'est pas devinee ici, mais disclosee telle
quelle dans le panneau d'introduction et dans "Sources et tracabilite".

CONVENTION DE CHIP : comme la quasi-totalite des propositions partage un tag identique
"(accord fort)", un chip synthetique GRADE 1+/2+/AE serait invente (non imprime par la
source) - a eviter (meme principe que fiche_nutrition.py, seule autre fiche du corpus a
utiliser un chip "Fort"/"Faible" plutot qu'un GRADE numerique). Extension locale, non
invasive, du dictionnaire GRADE_COLORS partage (comme dans fiche_nutrition.py) :
"Fort" -> vert. Un unique item (le paragraphe sur la dose de charge des anti-P2Y12,
section "Bitherapie ... stent coronaire") est une ABSENCE explicite de proposition
("Aucune proposition ne peut etre faite...") et est donc traite comme un panneau
no_reco_panel(), jamais comme une ligne de tableau avec chip.

FIGURE 1 (synthese des propositions, page 8 source) et TABLEAU I (caracteristiques a haut
risque thrombotique, page 11 source) sont tous deux reproduits integralement en tableaux
structures - ce sont le coeur clinique du document. Contenu verifie/fourni en amont de ce
script (cf. specification de tache), retranscrit ici sans paraphrase ni compression.

~33 propositions individuelles au total (6 + 3 + 5 + 8 + 3 + 4 + 4 par section), toutes
"(accord fort)" sauf l'item unique d'absence de proposition (dose de charge anti-P2Y12).
Pas d'arrondis Unicode (fleches/exposants/emoji) dans le corps du texte - encodage
Helvetica de cette chaine de production.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from style import *
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.units import mm

# Local, non-invasive extension of the shared GRADE_COLORS dict (safe: no other fiche in
# the corpus uses this exact label combination the way this document needs it; mirrors the
# precedent set in fiche_nutrition.py).
GRADE_COLORS["Fort"] = (GREEN, WHITE)

OUT = "/private/tmp/claude-501/-Users-macbook-Downloads-claude/65498e3e-5ddf-47a6-b100-3ac535d1faa0/scratchpad/rfe_sfar/output/Fiche_SFAR_AAP_Programmee_2018.pdf"

SOURCE_TXT = ("Source : Godier A, et al., GIHP & GFHT, en collaboration avec la SFAR — « Gestion "
              "des agents antiplaquettaires pour une procédure invasive programmée » — Propositions, "
              "Anesth Reanim 2018 (ANREA-314), doi 10.1016/j.anrea.2018.01.002. Fiche de synthèse non "
              "officielle : se référer au texte intégral.")

def P(txt, style=S_CELL):
    return Paragraph(txt, style)

def chip(label, **kw):
    return grade_chip(label, **kw)

def theme_table(rows, col_widths):
    """rows: (theme, text, grade_label) — 'theme' replaces the usual Réf. column since
    this source has no per-recommendation reference numbers (Propositions présentées en
    listes à puces, sans numérotation R1/R2)."""
    data = [[P("Thème", S_HEAD_W), P("Proposition", S_HEAD_W), P("Accord", S_HEAD_W_C)]]
    for theme, txt, grade in rows:
        data.append([P(theme, S_CELL_B), P(txt, S_CELL), chip(grade)])
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
    return info_panel(P("<b>Absence de proposition</b> — " + text, S_BODY_SM), bg=GREY_LIGHT, border=GREY)

def legend_flowable():
    chip_w = 18*mm
    content_w = PAGE_W - 2*MARGIN
    text_w = content_w - chip_w
    row = Table([[chip("Fort", width=chip_w-2*mm),
                  P("Proposition retenue par vote du groupe de travail GIHP/GFHT (n = 37) avec "
                    "« accord fort » (≥ 70 % des voix). Seul tag de force imprimé par la source à "
                    "côté de chaque proposition individuelle du corps du texte (voir encadré "
                    "ci-dessous).", S_BADGE_HEAD)]], colWidths=[chip_w, text_w])
    row.setStyle(TableStyle([("VALIGN",(0,0),(-1,-1),"MIDDLE"), ("LEFTPADDING",(0,0),(-1,-1),1), ("RIGHTPADDING",(0,0),(-1,-1),1)]))
    return row

def matrix_table():
    """Figure 1 — synthèse des propositions : risque hémorragique de la procédure (colonnes)
    x risque thrombotique du patient (lignes). Nouveau petit helper local (aucun helper
    existant du corpus ne correspond exactement à une matrice 3 colonnes x groupes de
    lignes) — reprend les conventions visuelles déjà établies (fonds BG_PANEL, bordures
    NAVY/TEAL_DARK) plutôt que d'inventer de nouvelles couleurs."""
    cw = PAGE_W - 2*MARGIN
    c0 = 54*mm
    c1 = c2 = c3 = (cw - c0) / 3.0

    S_MX = pstyle("mx", fontSize=7.6, leading=9.3, textColor=INK)
    S_MX_B = pstyle("mx_b", fontSize=7.6, leading=9.3, textColor=INK, fontName=FONT_BOLD)
    S_MX_HEAD = pstyle("mx_head", fontSize=8.2, leading=10, textColor=WHITE, fontName=FONT_BOLD, alignment=TA_CENTER)
    S_MX_SUPER = pstyle("mx_super", fontSize=7.4, leading=9, textColor=WHITE, fontName=FONT_BOLD, alignment=TA_CENTER)
    S_MX_GROUP = pstyle("mx_group", fontSize=7.6, leading=9.3, textColor=WHITE, fontName=FONT_BOLD)

    def mc(txt, style=S_MX):
        return Paragraph(txt, style)

    data = [
        [mc("", S_MX_HEAD),
         mc("Risque hémorragique de la procédure (à évaluer avec le chirurgien ou le "
            "responsable de la procédure)", S_MX_SUPER), "", ""],
        [mc("Risque thrombotique du patient", S_MX_HEAD), mc("Faible", S_MX_HEAD),
         mc("Intermédiaire", S_MX_HEAD), mc("Élevé", S_MX_HEAD)],
        [mc("Aspirine en prévention primaire", S_MX_B),
         mc("Arrêt ou poursuite"), mc("Arrêt"), mc("Arrêt")],
        [mc("AAP en prévention secondaire (prévention cardiovasculaire, artériopathie des "
            "membres inférieurs, antécédent d'accident vasculaire cérébral ischémique)", S_MX_GROUP), "", "", ""],
        [mc("Aspirine en monothérapie", S_MX_B),
         mc("Poursuite"), mc("Poursuite"), mc("Arrêt")],
        [mc("Clopidogrel en monothérapie", S_MX_B),
         mc("Poursuite"), mc("Arrêt et relais par aspirine"), mc("Arrêt")],
        [mc("Bithérapie antiplaquettaire pour stent coronaire (différer la procédure à la fin "
            "de la bithérapie antiplaquettaire en l'absence de risque vital ou fonctionnel)", S_MX_GROUP), "", "", ""],
        [mc("Stent &lt; 1 mois / stent &lt; 6 mois à haut risque thrombotique* / IDM &lt; 6 mois", S_MX_B),
         mc("Différer la procédure. Si impossible : poursuivre les 2 AAP"),
         mc("Différer la procédure. Si impossible : poursuivre l'aspirine, interrompre l'anti-P2Y12"),
         mc("Différer la procédure. Si impossible : interrompre les 2 AAP**")],
        [mc("Aucun des 3 critères ci-dessus", S_MX_B),
         mc("Poursuivre les 2 AAP"), mc("Poursuivre l'aspirine, interrompre l'anti-P2Y12"),
         mc("Interrompre les 2 AAP")],
    ]
    t = Table(data, colWidths=[c0, c1, c2, c3])
    style_cmds = [
        ("SPAN", (1, 0), (3, 0)),
        ("SPAN", (0, 3), (3, 3)),
        ("SPAN", (0, 6), (3, 6)),
        ("BACKGROUND", (0, 0), (-1, 1), TEAL_DARK),
        ("BACKGROUND", (0, 3), (-1, 3), NAVY),
        ("BACKGROUND", (0, 6), (-1, 6), NAVY),
        ("BACKGROUND", (0, 2), (-1, 2), WHITE),
        ("BACKGROUND", (0, 4), (-1, 4), BG_PANEL),
        ("BACKGROUND", (0, 5), (-1, 5), WHITE),
        ("BACKGROUND", (0, 7), (-1, 7), BG_PANEL),
        ("BACKGROUND", (0, 8), (-1, 8), WHITE),
        ("GRID", (0, 0), (-1, -1), 0.5, GREY_LIGHT),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 3.2), ("BOTTOMPADDING", (0, 0), (-1, -1), 3.2),
        ("LEFTPADDING", (0, 0), (-1, -1), 4), ("RIGHTPADDING", (0, 0), (-1, -1), 4),
    ]
    t.setStyle(TableStyle(style_cmds))
    return t

TOTAL_PAGES = {"n": 7}

def on_page(canvas, doc, page_title):
    header_band(canvas, doc, "GIHP / GFHT / SFAR — PROPOSITIONS 2018 — FICHE DE SYNTHÈSE",
                "AAP pour une procédure programmée",
                page_title, icon_fn=lambda c, x, y: icon_pill(c, x, y, 13*mm), color=NAVY)
    footer_band(canvas, doc, SOURCE_TXT, f"Page {doc.page} / {TOTAL_PAGES['n']}")

# ---------------------------------------------------------------------------
def _section_intro():
    story = []
    story.append(Spacer(1, 3*mm))
    story.append(info_panel(P(
        "<b>Champ :</b> gestion péri-procédurale d'un traitement antiplaquettaire (AAP) oral au "
        "long cours — aspirine, clopidogrel, prasugrel, ticagrélor — chez un patient devant "
        "bénéficier d'une <b>procédure invasive programmée</b> (élective). Complète la fiche déjà "
        "construite dans ce site pour la procédure invasive <b>non programmée / l'hémorragie</b> "
        "(document distinct, même groupe de travail).<br/><br/>"
        "<b>Méthodologie — distincte de GRADE :</b> ce document ne comporte pas de niveaux GRADE "
        "1+/1-/2+/2-. Les propositions ont été rédigées par cinq groupes de travail du Groupe "
        "d'intérêt en hémostase périopératoire (GIHP) et du Groupe français d'études sur "
        "l'hémostase et la thrombose (GFHT), en collaboration avec la SFAR, puis soumises à un "
        "vote (n = 37) : une proposition est retenue si au moins 50 % des votants expriment leur "
        "accord (et moins de 20 % une opinion contraire) ; l'accord est qualifié de <b>« fort »</b> "
        "si le seuil atteint 70 %. En l'absence d'accord, les propositions étaient reformulées puis "
        "resoumises au vote.",
        S_BODY), bg=BG_PANEL, border=TEAL))
    story.append(Spacer(1, 3*mm))
    story.append(info_panel(P(
        "<b>Divergence source-interne (disclosure) :</b> le Résumé de la source affirme : « Ces "
        "propositions ont été discutées et validées par vote ; <i>toutes sauf une</i> ont fait "
        "l'objet d'un accord fort. » Une vérification directe, proposition par proposition, de "
        "l'intégralité du corps du texte (y compris les propositions associées à la Figure 1 et au "
        "Tableau I, vérifiées visuellement sur le rendu de page) montre que <b>toutes les "
        "propositions retrouvées portent explicitement le tag « (accord fort) »</b>, sans qu'aucune "
        "ne porte un tag différent ou plus faible nulle part dans le document. L'exception annoncée "
        "par le résumé n'est donc <b>pas identifiable</b> dans le corps du texte source — elle n'est "
        "pas devinée ici ; les deux constats (l'affirmation du résumé et l'absence de toute "
        "proposition tagée autrement que « accord fort » dans le corps du texte) sont disclosés tels "
        "quels, sans résolution silencieuse.",
        S_BODY_SM), bg=AMBER_LIGHT, border=AMBER))
    story.append(Spacer(1, 3*mm))

    story.append(section_bar("Légende (convention de ce document)"))
    story.append(Spacer(1, 2*mm))
    story.append(legend_flowable())
    return story

def _section_classification():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(KeepTogether([
        section_bar("Classification du risque hémorragique de la procédure"),
        Spacer(1, 2*mm),
        theme_table([
            ("Principe", "Il est proposé de diviser le risque hémorragique associé à la "
             "procédure invasive en risque élevé, intermédiaire et faible.", "Fort"),
            ("Risque élevé", "Les procédures à risque hémorragique élevé sont définies comme "
             "non réalisables sous AAP, même sous aspirine en monothérapie. Ce sont celles pour "
             "lesquelles le risque hémorragique sous aspirine est soit inconnu mais considéré "
             "comme potentiellement préoccupant, soit inacceptable ou jugé comme tel (risque "
             "létal ou fonctionnel). Elles sont peu fréquentes et incluent, par exemple, certains "
             "actes d'urologie lorsque des techniques alternatives ne peuvent pas être "
             "utilisées, de nombreux actes de neurochirurgie intracrânienne, les chirurgies avec "
             "des délabrements importants ou de grandes dissections, certains actes de "
             "chirurgie hépatique ou thoracique.", "Fort"),
            ("Risque intermédiaire", "Les procédures à risque hémorragique intermédiaire sont "
             "définies comme réalisables sous aspirine seule. Il s'agit de la majorité des "
             "procédures invasives.", "Fort"),
            ("Risque faible", "Les procédures à faible risque hémorragique sont définies comme "
             "réalisables sous bithérapie antiplaquettaire. Elles incluent, par exemple, la "
             "chirurgie de la cataracte, certains actes de chirurgie buccodentaire, certains "
             "actes d'urologie telle l'uréthrocystoscopie, certains actes de chirurgie "
             "vasculaire, certaines bronchoscopies, certains actes d'endoscopie digestive, "
             "incluant par exemple, toutes les endoscopies diagnostiques avec ou sans biopsies, "
             "les cholangio-pancréatographies rétrogrades endoscopiques sans sphinctérotomie, "
             "les polypectomies coliques &lt; 1 cm. Toutefois, l'expérience de ces procédures "
             "avec le ticagrélor ou le prasugrel est limitée. De plus, l'administration associée "
             "d'autres médicaments interférant avec l'hémostase, ou l'existence d'une "
             "comorbidité augmentant le risque hémorragique, peuvent conduire à choisir "
             "l'interruption de l'anti-P2Y12.", "Fort"),
            ("Absence de consensus", "Lorsqu'il n'existe pas de consensus ou de référentiel "
             "pour classer un acte invasif dans une de ces catégories, il est proposé qu'une "
             "équipe référente (opérateur, anesthésiste, cardiologue, pneumologue, médecin "
             "vasculaire, hémostasien…) dans l'établissement de santé définisse une attitude de "
             "prise en charge, au cas par cas, ou pour un profil de patient ou de geste. Ces "
             "décisions sont notifiées dans le dossier du patient ou dans les procédures de "
             "l'établissement.", "Fort"),
            ("Endoscopies digestives", "Concernant les endoscopies digestives, il est proposé "
             "que des stratégies de gestion des AAP soient définies dans chaque centre en "
             "fonction du profil des patients pris en charge et donc du geste invasif pouvant "
             "être potentiellement réalisé pendant l'endoscopie. Ainsi, si la probabilité d'un "
             "geste nécessitant une interruption des AAP pour un profil de patient déterminé est "
             "jugée élevée, c'est cette stratégie qui est adoptée (ex. : sphinctérotomie, "
             "gastrostomie…). En revanche, si la probabilité est faible, c'est la poursuite des "
             "AAP qui est privilégiée (ex. : maladies inflammatoires chroniques de l'intestin, "
             "dyspepsie…). Quand la probabilité et la nature des lésions à réséquer n'est pas "
             "connue a priori, chaque centre détermine son attitude (ex. : recherche de "
             "polypes).", "Fort"),
        ], [30*mm, PAGE_W-2*MARGIN-30*mm-16*mm, 16*mm]),
    ]))
    return story

def _section_figure1():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Figure 1 — Synthèse des propositions"))
    story.append(Spacer(1, 1.5*mm))
    story.append(P("<i>Tableau-matrice reproduisant intégralement la Figure 1 du document source "
                    "(risque hémorragique de la procédure en colonnes, risque thrombotique du "
                    "patient en lignes).</i>", S_NOTE))
    story.append(Spacer(1, 1.5*mm))
    story.append(matrix_table())
    story.append(Spacer(1, 3*mm))

    cw = PAGE_W - 2*MARGIN
    story.append(P("<b>Risque hémorragique de la procédure</b>", S_CELL_B))
    story.append(Spacer(1, 1*mm))
    story.append(simple_table(
        ["Faible", "Intermédiaire", "Élevé"],
        [["Réalisable sous bithérapie antiplaquettaire (ex : cataracte)",
          "Réalisable sous aspirine seule (ex : PTH)",
          "Non réalisable sous AAP (ex : ampullectomie endoscopique)"]],
        [cw/3.0, cw/3.0, cw/3.0]))
    story.append(Spacer(1, 3*mm))

    story.append(info_panel(P(
        "<b>Délai d'arrêt des AAP — dernière prise à :</b> J-3 pour l'aspirine ; J-5 pour le "
        "clopidogrel et le ticagrélor ; J-7 pour le prasugrel (ajouter 2 jours à chaque durée si "
        "neurochirurgie intracrânienne). En post-opératoire, reprendre les 2 AAP au plus vite, en "
        "fonction du risque hémorragique.",
        S_BODY_SM), bg=BG_PANEL, border=TEAL))
    story.append(Spacer(1, 3*mm))

    story.append(KeepTogether([
        P("<b>TABLEAU I</b> — Caractéristiques d'un stent à haut risque thrombotique*", S_H2),
        Spacer(1, 1*mm),
        simple_table(
            ["Caractéristique"],
            [
                ["Antécédent de thrombose de stent sous bithérapie antiplaquettaire"],
                ["Maladie coronaire diffuse en particulier chez le diabétique"],
                ["Insuffisance rénale chronique (i.e. ClCr &lt; 60 mL/min)"],
                ["Traitement d'une occlusion coronaire chronique"],
                ["Stenting de la dernière artère coronaire perméable"],
                ["Au moins trois stents implantés"],
                ["Au moins trois lésions traitées"],
                ["Bifurcation avec deux stents implantés"],
                ["Longueur totale de stent &gt; 60 mm"],
            ], [cw]),
        Spacer(1, 1*mm),
        P("<i>* Renvoi de la Figure 1 et du Tableau I. ** Si stent &lt; 1 mois, discuter un relais "
          "par AAP injectable.</i>", S_NOTE),
    ]))
    return story

def _section_durees():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(KeepTogether([
        section_bar("Durées d'interruption des AAP et relais"),
        Spacer(1, 2*mm),
        theme_table([
            ("Durées d'interruption", "Si l'interruption des AAP avant une procédure invasive "
             "est indiquée, il est proposé de les interrompre de la façon suivante : dernière "
             "prise d'aspirine à J-3 (J0 correspond au jour de la procédure) ; dernière prise de "
             "clopidogrel et de ticagrélor à J-5 ; dernière prise de prasugrel à J-7.", "Fort"),
            ("Relais", "Il est recommandé de n'utiliser ni les héparines (HNF ou HBPM) ni les "
             "AINS en relais des AAP.", "Fort"),
            ("Aspirine — posologie", "Chez les patients traités au long cours par aspirine à "
             "des posologies allant jusqu'à 300 mg/j, il est proposé de ne pas réduire la "
             "posologie en vue de la chirurgie.", "Fort"),
        ], [30*mm, PAGE_W-2*MARGIN-30*mm-16*mm, 16*mm]),
    ]))
    story.append(Spacer(1, 2*mm))
    story.append(P(
        "<b>Note (neurochirurgie intracrânienne) :</b> pour la neurochirurgie intracrânienne, il "
        "est proposé que la dernière prise soit à J-5 pour l'aspirine, J-7 pour le clopidogrel et "
        "le ticagrélor, J-9 pour le prasugrel (accord fort).", S_NOTE))
    story.append(Spacer(1, 1.5*mm))
    story.append(P(
        "<b>Note (ticagrélor, pontage semi-urgent) :</b> des données récentes suggèrent que la "
        "chirurgie semi-urgente de pontage aortocoronaire puisse être réalisée après une "
        "interruption plus courte du ticagrélor, de trois à cinq jours, sans surrisque "
        "hémorragique pour la majorité des patients. Cependant, dans cette situation, les "
        "patients n'ayant pas une correction de l'inhibition plaquettaire induite par le "
        "ticagrélor sont exposés à un risque accru d'hémorragie.", S_NOTE))
    return story

def _section_indication():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(KeepTogether([
        section_bar("Gestion des AAP en fonction de leur indication"),
        Spacer(1, 2*mm),
        theme_table([
            ("Prévention primaire — non-initiation", "Il est proposé de ne pas initier un "
             "traitement par aspirine en préopératoire d'une chirurgie non cardiaque (à "
             "l'exception de l'endartériectomie carotidienne) dans le but de réduire les "
             "évènements cardiovasculaires périopératoires.", "Fort"),
            ("Prévention primaire — arrêt", "Il est proposé d'arrêter l'aspirine en "
             "préopératoire lorsqu'elle est prescrite en prévention primaire.", "Fort"),
            ("Prévention secondaire — poursuite", "Il est proposé de ne pas arrêter l'aspirine "
             "en préopératoire lorsqu'elle est prescrite en prévention cardiovasculaire "
             "secondaire (post-accident vasculaire cérébral ischémique, coronaropathie, "
             "artériopathie des membres inférieurs), à l'exception des procédures à risque "
             "hémorragique élevé.", "Fort"),
            ("Anti-P2Y12 monothérapie — relais aspirine", "Il est proposé que chez les patients "
             "traités par un anti-P2Y12 en monothérapie et programmés pour une chirurgie à "
             "risque intermédiaire, l'AAP soit remplacé par de l'aspirine, à la dose journalière "
             "75 à 100 mg. Ce changement pourrait avoir lieu plus de sept jours avant la "
             "chirurgie, afin de permettre une correction complète de l'inhibition plaquettaire "
             "induite par l'anti-P2Y12.", "Fort"),
            ("Reprise postopératoire", "Il est proposé que la reprise de l'AAP soit aussi "
             "précoce que possible, en fonction du risque de saignement postopératoire, chez "
             "les patients ayant une indication à un traitement par AAP en monothérapie au long "
             "cours.", "Fort"),
        ], [36*mm, PAGE_W-2*MARGIN-36*mm-16*mm, 16*mm]),
    ]))
    return story

def _section_stent():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(KeepTogether([
        section_bar("Bithérapie antiplaquettaire chez le patient porteur de stent coronaire"),
        Spacer(1, 2*mm),
        theme_table([
            ("Décision multidisciplinaire", "Il est proposé que la gestion préopératoire des "
             "AAP et leur reprise postopératoire soit discutée avec le cardiologue du patient ou "
             "un cardiologue référent et tracée dans le dossier lorsqu'il s'agit d'une procédure "
             "à risque hémorragique intermédiaire ou élevé.", "Fort"),
            ("Report de la chirurgie", "Il est proposé de reporter toute chirurgie non cardiaque "
             "à la fin de la durée recommandée de la bithérapie antiplaquettaire quand cela ne "
             "génère pas de risque vital ou fonctionnel majeur pour le patient.", "Fort"),
            ("Si report impossible", "Si ce report n'est pas possible, il est proposé de "
             "repousser toute chirurgie non cardiaque au-delà du 1er mois qui suit la pose de "
             "stent, quel que soit le type de stent, quelle que soit l'indication (IDM ou "
             "coronaropathie stable). Si le geste ne peut être différé au-delà du 1er mois, il "
             "est proposé de réaliser cette chirurgie en poursuivant l'aspirine et dans un "
             "centre ayant un plateau de cardiologie interventionnelle actif 24 heures sur "
             "24.", "Fort"),
            ("Haut risque thrombotique / IDM", "Chez les patients sous bithérapie "
             "antiplaquettaire dans les suites d'un IDM ou en cas de pose de stent associé à des "
             "caractéristiques à haut risque thrombotique, il est proposé de reporter toute "
             "chirurgie non cardiaque au-delà du 6e mois qui suit la pose de stent.", "Fort"),
            ("Aspirine — poursuite", "Il est recommandé de poursuivre l'aspirine en "
             "préopératoire. Si elle a été interrompue, il est recommandé de la reprendre aussi "
             "précocement que possible après la procédure invasive, au mieux le jour même, en "
             "fonction du risque de saignement postopératoire.", "Fort"),
            ("Relais parentéral (cas exceptionnels)", "Si les deux AAP doivent être interrompus "
             "dans le 1er mois suivant la pose de stent, un relais par des AAP parentéraux "
             "réversibles comme le tirofiban ou le cangrélor peut être discuté au cas par cas, "
             "avec une approche multidisciplinaire (utilisation hors AMM). Dans ces situations "
             "exceptionnelles, associées à un haut risque hémorragique et thrombotique, le "
             "relais doit être réalisé en soins intensifs et la chirurgie doit être réalisée "
             "dans un centre ayant un service de cardiologie interventionnelle actif 24 heures "
             "sur 24.", "Fort"),
            ("Reprise des anti-P2Y12", "Si les anti-P2Y12 ont été interrompus avant la "
             "chirurgie, ils doivent être repris précocement, au mieux dans les 24 à 72 heures "
             "après la chirurgie, compte tenu de l'augmentation du risque thrombotique. La "
             "reprise se fait avec le même anti-P2Y12 qu'en préopératoire.", "Fort"),
            ("AINS", "Il est proposé de ne pas administrer d'AINS en périopératoire chez les "
             "patients traités par bithérapie antiplaquettaire.", "Fort"),
        ], [34*mm, PAGE_W-2*MARGIN-34*mm-16*mm, 16*mm]),
    ]))
    story.append(Spacer(1, 2*mm))
    story.append(no_reco_panel(
        "concernant le recours, ou non, à une dose de charge lors de la reprise des "
        "anti-P2Y12 après leur interruption préopératoire, aucune proposition ne peut être "
        "faite."))
    story.append(Spacer(1, 1.5*mm))
    story.append(P(
        "<b>Note (AINS) :</b> l'utilisation périopératoire des coxibs reste possible.", S_NOTE))
    return story

def _section_alr():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(KeepTogether([
        section_bar("Anesthésie locorégionale rachidienne (ALR-R)"),
        Spacer(1, 2*mm),
        theme_table([
            ("Aspirine", "L'aspirine ne contre-indique pas une ALR rachidienne si le rapport "
             "bénéfice-risque est favorable, en vérifiant l'absence d'anomalie associée de "
             "l'hémostase, incluant un traitement anticoagulant. Il est proposé de préférer si "
             "possible la rachianesthésie en ponction unique à la péridurale.", "Fort"),
            ("Anti-P2Y12", "L'ALR rachidienne est contre-indiquée en cas de traitement par "
             "anti-P2Y12 (clopidogrel, prasugrel, ticagrélor), sauf si ces AAP ont été "
             "interrompus respectivement 5, 7 et 5 jours avant le geste.", "Fort"),
            ("Cathéter péridural", "La mise en place d'un cathéter péridural expose à une "
             "gestion complexe des AAP. Le retrait du cathéter suit les mêmes règles que la "
             "pose. Le recours au cathéter péridural ne doit pas compromettre la reprise "
             "postopératoire des AAP, et en particulier des anti-P2Y12.", "Fort"),
        ], [26*mm, PAGE_W-2*MARGIN-26*mm-16*mm, 16*mm]),
    ]))
    story.append(Spacer(1, 3*mm))

    story.append(section_bar("Blocs nerveux périphériques"))
    story.append(Spacer(1, 2*mm))
    story.append(P(
        "<b>Blocs à faible risque hémorragique</b> (saignement facilement contrôlable, zone "
        "compressible) : blocs superficiels — bloc fémoral, bloc axillaire, bloc sciatique au "
        "creux poplité, etc.<br/>"
        "<b>Blocs à haut risque hémorragique</b> (saignement non compressible ou aux "
        "conséquences potentiellement graves) : blocs profonds — bloc infraclaviculaire, bloc "
        "sciatique para-sacré, bloc du plexus lombaire postérieur, etc. ; contre-indiqués sous "
        "anti-P2Y12.", S_BODY_SM))
    story.append(Spacer(1, 2*mm))
    story.append(theme_table([
        ("Faible risque", "Il est proposé que les blocs nerveux périphériques à faible risque "
         "hémorragique puissent être réalisés sous AAP, en mono- ou en bithérapie, si le "
         "rapport bénéfice/risque est favorable.", "Fort"),
        ("Haut risque", "Il est proposé que les blocs nerveux périphériques à haut risque "
         "hémorragique puissent être réalisés sous aspirine en monothérapie si le rapport "
         "bénéfice/risque est favorable. Ces blocs sont contre-indiqués sous anti-P2Y12 "
         "(clopidogrel, prasugrel, ticagrélor), sauf si ces AAP ont été interrompus "
         "respectivement 5, 7 et 5 jours avant le geste.", "Fort"),
        ("Échoguidage", "Il est proposé que ces blocs (superficiels ou profonds) soient "
         "réalisés par échoguidage et par un opérateur expérimenté.", "Fort"),
        ("Cathéter périnerveux", "La mise en place d'un cathéter périnerveux ne doit pas "
         "compromettre la reprise postopératoire des AAP, et en particulier des anti-P2Y12. "
         "Son retrait suit les mêmes règles que la pose.", "Fort"),
    ], [26*mm, PAGE_W-2*MARGIN-26*mm-16*mm, 16*mm]))
    return story

def _section_pac():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(KeepTogether([
        section_bar("Chirurgie cardiaque de pontage aortocoronaire (PAC)"),
        Spacer(1, 2*mm),
        theme_table([
            ("Décision multidisciplinaire", "Il est proposé que la stratégie de gestion des AAP "
             "en vue de pontage aortocoronaire (PAC) soit décidée de façon multidisciplinaire en "
             "fonction du risque hémorragique et du risque thrombotique de chaque patient.", "Fort"),
            ("Aspirine", "Il est proposé de poursuivre l'aspirine pour la chirurgie de PAC.", "Fort"),
            ("Anti-P2Y12 — durées", "Pour les patients traités par bithérapie antiplaquettaire, "
             "il est proposé de réaliser les procédures de PAC après interruption des "
             "anti-P2Y12, avec dernière prise de clopidogrel et de ticagrélor à J-5 et une "
             "dernière prise de prasugrel à J-7.", "Fort"),
            ("Ticagrélor — données récentes", "Des données récentes suggèrent que la chirurgie "
             "semi-urgente puisse être réalisée après une interruption plus courte du "
             "ticagrélor, de 3 à 5 jours, sans surrisque hémorragique pour la majorité des "
             "patients. Cependant, dans cette situation, les patients n'ayant pas une correction "
             "de l'inhibition plaquettaire induite par le ticagrélor sont exposés à un risque "
             "d'hémorragie.", "Fort"),
        ], [34*mm, PAGE_W-2*MARGIN-34*mm-16*mm, 16*mm]),
    ]))
    return story

def _section_sources():
    story = []
    story.append(Spacer(1, 3*mm))
    story.append(section_bar("Sources et traçabilité", color=GREY))
    story.append(Spacer(1, 2*mm))
    story.append(P(
        "<b>Document source :</b> « Gestion des agents antiplaquettaires pour une procédure "
        "invasive programmée » — Propositions du Groupe d'intérêt en hémostase périopératoire "
        "(GIHP) et du Groupe français d'études sur l'hémostase et la thrombose (GFHT), en "
        "collaboration avec la Société française d'anesthésie-réanimation (SFAR). Anne Godier, "
        "Pierre Fontana, Serge Motte, Annick Steib, Fanny Bonhomme, Sylvie Schlumberger, Thomas "
        "Lecompte, Nadia Rosencher, Sophie Susen, André Vincentelli, Yves Gruel, Pierre "
        "Albaladejo, Jean-Philippe Collet, et le French Working Group on perioperative "
        "hemostasis (GIHP). Anesth Reanim 2018 (ANREA-314).", S_SOURCE))
    story.append(Spacer(1, 1.5*mm))
    story.append(P("<b>Publication :</b> doi 10.1016/j.anrea.2018.01.002.", S_SOURCE))
    story.append(P("<b>Méthodologie :</b> pas de système GRADE — propositions rédigées par cinq "
                    "groupes de travail GIHP/GFHT puis validées par vote (n = 37) ; seuil de "
                    "50 % pour retenir une proposition, seuil de 70 % pour un « accord fort » "
                    "(voir légende page 1 et disclosure sur la divergence source-interne "
                    "concernant l'unique exception annoncée par le résumé mais non identifiable "
                    "dans le corps du texte).", S_SOURCE))
    story.append(Spacer(1, 1.5*mm))
    story.append(P("<b>Couverture :</b> cette fiche reprend l'intégralité des propositions du "
                    "corps du texte (classification du risque hémorragique de la procédure, "
                    "durées d'interruption et relais, gestion selon l'indication, bithérapie "
                    "pour stent coronaire, anesthésie locorégionale rachidienne et blocs "
                    "périphériques, chirurgie de pontage aortocoronaire), ainsi que la Figure 1 "
                    "(synthèse des propositions) et le Tableau I (caractéristiques d'un stent à "
                    "haut risque thrombotique), reproduits intégralement en tableaux "
                    "structurés.", S_SOURCE))
    story.append(Spacer(1, 3*mm))
    story.append(info_panel(P(
        "<b>Avertissement :</b> ce document est une fiche de synthèse indépendante, produite "
        "pour un usage d'aide-mémoire. Il reprend l'intégralité des propositions, de la Figure 1 "
        "et du Tableau I du document source, mais ne remplace pas le texte intégral "
        "(argumentaire complet, références bibliographiques) et n'est ni édité ni validé par le "
        "GIHP, le GFHT ou la SFAR. En cas de doute, se référer au texte intégral et/ou à un avis "
        "spécialisé. Document de 2018 : vérifier l'existence d'une actualisation plus récente en "
        "cas de doute.",
        S_BODY_SM), bg=GREY_LIGHT, border=GREY))
    return story

def _section_1():
    return _section_intro()

def _section_2():
    return _section_classification()

def _section_3():
    return _section_figure1()

def _section_4():
    return _section_durees() + [Spacer(1, 3*mm)] + _section_indication()

def _section_5():
    return _section_stent()

def _section_6():
    return _section_alr()

def _section_7():
    return _section_pac() + [Spacer(1, 4*mm)] + _section_sources()

SECTIONS = [
    ("Introduction, méthodologie & légende", _section_1),
    ("Classification du risque hémorragique de la procédure", _section_2),
    ("Figure 1 — synthèse des propositions & Tableau I", _section_3),
    ("Durées d'interruption, relais & gestion selon l'indication", _section_4),
    ("Bithérapie antiplaquettaire — stent coronaire", _section_5),
    ("Anesthésie locorégionale (rachidienne & blocs périphériques)", _section_6),
    ("Chirurgie de pontage aortocoronaire & traçabilité", _section_7),
]

def _make_doc(path=None):
    return SimpleDocTemplate(path or OUT, pagesize=A4,
                              leftMargin=MARGIN, rightMargin=MARGIN,
                              topMargin=32*mm, bottomMargin=16*mm,
                              title="Fiche GIHP/GFHT/SFAR 2018 - AAP pour une procédure programmée",
                              author="Synthèse indépendante (source GIHP/GFHT/SFAR)")

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
    # Use a throwaway temp path (never OUT) for these measurement-only builds: reusing OUT
    # here was found to corrupt page 1's header_band in the final build (repeated silent
    # builds to the same path as the real output somehow interfered with the last build's
    # first page — reproduced and fixed by isolating counting passes to their own file).
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
