# -*- coding: utf-8 -*-
"""
Fiche de synthese - Conference d'experts, texte court, 2002 (publiee Ann Fr
Anesth Reanim 2004;23:167-176), "Pratique des anesthesies locales et
locoregionales par des medecins non specialises en anesthesie-reanimation,
dans le cadre des urgences" - SFAR, Samu de France, Societe francophone de
medecine d'urgence. 10 pages source (texte court), telecharge depuis
sfar.org (wp-content/uploads/2016/01/2_AFAR_Pratique-des-anesthesies-
locales-et-locoregionales-par-des-medecins-non-specialises-en-anesthesie-
reanimation-dans-le-cadre-des-urgences.pdf).

CHAMP : ce texte s'adresse SPECIFIQUEMENT aux medecins de l'urgence NON
specialises en anesthesie-reanimation (SAU, urgences prehospitalieres). Il
exclut explicitement l'anesthesie "chirurgicale" (bloc operatoire) et les
techniques d'ALR perimedullaires et les blocs du tronc/intercostaux/
paravertebraux/interpleuraux/multibloc laryngé, reserves aux anesthesistes-
reanimateurs (source elle-meme, section 3.2).

METHODOLOGIE : grille EBM classique de ce corpus (Tableau 1 : Niveaux de
preuve I-V ; Tableau 2 : Force des recommandations Grade A-E), identique au
schema deja rencontre dans fiche_hsa.py / fiche_sepsis_hemodynamique.py.
Contrairement aux RPP recentes (formulation Ri.j numerotee), ce texte de
2002 grade des affirmations directement dans la prose narrative des 5
"Questions" - AUCUNE numerotation Rx.y native. Convention de reference
adoptee ici (disclosed) : chaque enonce grade recoit une reference
synthetique "§<numero de sous-section source>" (ex. §2.1.3.2, §3.2.2.1)
reprenant la numerotation des sous-sections DU TEXTE SOURCE lui-meme (pas
inventee) ; quand plusieurs enonces distincts partagent la meme
sous-section, un suffixe (a), (b), (c) est ajoute dans l'ordre d'apparition.

INVENTAIRE EXHAUSTIF DES GRADES : grep exhaustif de sources/
alr_non_specialiste.txt pour le motif [A-E] entre crochets -> 35
occurrences. 34 lignes de reco_table dans cette fiche (une fusion : les
deux tags [A] consecutifs du §3.2.2.1, portant sur la MEME affirmation
d'efficacite/predictibilite du bloc femoral scindee en 2 phrases, sont
fusionnes en une seule ligne Grade A - fusion autorisee par la regle 4 du
projet car il s'agit du MEME grade, pas de 2 grades differents). Les deux
grades [B]/[E] du §3.3 portant sur la MEME phrase ("morphinique majore le
risque de depression respiratoire [B], qui doit donc etre evitee [E]")
sont au contraire SCINDES en 2 lignes distinctes (regle 4 : jamais fusionner
deux clauses differemment gradees). Le tag [D] du Tableau 4 ("Posologie
maximum [D]") est un grade de COLONNE (toute la colonne posologie du
tableau), pas une phrase individuelle - disclosed en legende du tableau
plutot que fabrique en ligne de reco_table.

PORTEE : couverture complete des 34 enonces gradés + les 5 tableaux du
texte source (Tableau 1 Niveaux de preuve, Tableau 2 Force des
recommandations, Tableau 3 Toxicite neurologique, Tableau 4 Posologie des
principaux anesthesiques locaux, Tableau 5 Diagnostic/prevention/
traitement des complications) + les listes non gradees mais cliniquement
importantes (contre-indications absolues/relatives, mesures de precaution
integrale ~15 items, formation requise ~9 items) + le detail anatomique
des 4 blocs de la face (nerfs V1/V2/V3, zones anesthesiees).

ARGUMENTAIRE : ce texte court de 2002 est deja tres condense nativement
(pas de section "argumentaire" separee a trimmer, contrairement a des RFE
plus recentes) - la prose narrative EST le contenu actionnable. Seules les
references bibliographiques numerotees [1]-[11] (liste finale) sont
omises, sans perte d'information clinique.

AUDIT INDEPENDANT (subagent, aveugle au brouillon) : grades/doses/contre-
indications tous confirmes exacts (aucune erreur de grade, aucune inversion
de contre-indication, aucun dosage errone). Points MEDIUM corriges suite a
l'audit - contenu reellement present dans la source mais initialement trop
condense (regle 2, couverture 100% ou scope explicitement disclosed) :
Tableau 3 "Prodromes" (etourdissement/sensation ebrieuse/empatement de la
parole/"voire absence" reintegres), Tableau 5 ligne "Toxicite systemique"
(sensation de malaise/logorrhee/bradycardie/PNI-hypotension reintegres),
reperes anatomiques des blocs median/radial/ulnaire (theme_table dediee) et
technique complete du bloc de la gaine des flechisseurs (angle 45°, signe
de verticalisation, injection sans resistance), positionnement + 3 blocs
du pied additionnels moins utilises (tibial, calcaneen interne, tibial
anterieur). Points LOW egalement corriges : scission du Tableau 4 Emla en
2 lignes (tube 30g / tube 5g, au lieu d'un seul, comme la source), rapport
de toxicite neurologique bupivacaine:ropivacaine:lidocaine 4:3:1, clause
"inadequation equipes/patients" en milieu difficile, "medicaments
antagonisables"/"autres hypnotiques inadaptes" en sedation associee,
paragraphe deontologique de cloture de la Question 5.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from style import *
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.units import mm

OUT = "/home/user/rfe-sfar-website/output/Fiche_SFAR_ALR_Non_Specialiste_Urgences_2002.pdf"

SOURCE_TXT = ("Source : « Pratique des anesthésies locales et locorégionales par des médecins non "
              "spécialisés en anesthésie-réanimation, dans le cadre des urgences » — Conférence "
              "d'experts, texte court, SFAR/Samu de France/SFMU, 2002 (Ann Fr Anesth Réanim "
              "2004;23:167-176). Fiche de synthèse non officielle : se référer au texte intégral.")

# Extension locale de GRADE_COLORS - lettres A-E de cette source (grille EBM classique,
# meme precedent que fiche_hsa.py / fiche_sepsis_hemodynamique.py).
GRADE_COLORS["A"] = (GREEN, WHITE)
GRADE_COLORS["B"] = (TEAL, WHITE)
GRADE_COLORS["C"] = (AMBER, WHITE)
GRADE_COLORS["D"] = (NAVY, WHITE)
GRADE_COLORS["E"] = (GREY, WHITE)

def P(txt, style=S_CELL):
    return Paragraph(txt, style)

def chip(label):
    return grade_chip(label, width=13 * mm, fontsize=8.6)

CW_FULL = PAGE_W - 2 * MARGIN

def reco_table(rows, col_widths):
    """rows: (ref, text, grade_label)."""
    data = [[P("Réf.", S_HEAD_W), P("Recommandation", S_HEAD_W), P("Grade", S_HEAD_W_C)]]
    for ref, txt, grade in rows:
        data.append([P(ref, S_CELL_B), P(txt, S_CELL), chip(grade)])
    t = Table(data, colWidths=col_widths, repeatRows=1)
    style_cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), NAVY), ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTNAME", (0, 0), (-1, 0), FONT_BOLD), ("FONTSIZE", (0, 0), (-1, 0), 8),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("ALIGN", (0, 0), (0, -1), "CENTER"),
        ("ALIGN", (2, 0), (2, -1), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 0.5, GREY_LIGHT),
        ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            style_cmds.append(("BACKGROUND", (0, i), (-1, i), BG_PANEL))
    t.setStyle(TableStyle(style_cmds))
    return t

RCW = [17 * mm, CW_FULL - 17 * mm - 15 * mm, 15 * mm]

def theme_table(rows, col_widths, head=("Thème", "Détail")):
    data = [[P(head[0], S_HEAD_W), P(head[1], S_HEAD_W)]]
    for theme, detail in rows:
        data.append([P(theme, S_CELL_B), P(detail, S_CELL)])
    t = Table(data, colWidths=col_widths, repeatRows=1)
    style_cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), TEAL_DARK), ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTNAME", (0, 0), (-1, 0), FONT_BOLD), ("FONTSIZE", (0, 0), (-1, 0), 8),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.5, GREY_LIGHT),
        ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            style_cmds.append(("BACKGROUND", (0, i), (-1, i), BG_PANEL))
    t.setStyle(TableStyle(style_cmds))
    return t

def grid_table(head_row, rows, col_widths, head_bg=NAVY):
    data = [[P(h, S_HEAD_W_C) for h in head_row]]
    for row in rows:
        data.append([P(c, S_CELL) for c in row])
    t = Table(data, colWidths=col_widths, repeatRows=1)
    style_cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), head_bg), ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTNAME", (0, 0), (-1, 0), FONT_BOLD), ("FONTSIZE", (0, 0), (-1, 0), 8),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.5, GREY_LIGHT),
        ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            style_cmds.append(("BACKGROUND", (0, i), (-1, i), BG_PANEL))
    t.setStyle(TableStyle(style_cmds))
    return t

def bullets(items, style=S_BODY_SM):
    return [P("• " + it, style) for it in items]

def grade_table(rows, col_widths):
    """rows: (grade_label, definition) — used for Tableau 2 (Force des recommandations)."""
    data = [[P("Grade", S_HEAD_W_C), P("Définition (Tableau 2 source)", S_HEAD_W)]]
    for label, definition in rows:
        data.append([chip(label), P(definition, S_CELL)])
    t = Table(data, colWidths=col_widths, repeatRows=1)
    style_cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), TEAL_DARK), ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTNAME", (0, 0), (-1, 0), FONT_BOLD), ("FONTSIZE", (0, 0), (-1, 0), 8),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("ALIGN", (0, 1), (0, -1), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 0.5, GREY_LIGHT),
        ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            style_cmds.append(("BACKGROUND", (0, i), (-1, i), BG_PANEL))
    t.setStyle(TableStyle(style_cmds))
    return t

TOTAL_PAGES = {"n": 7}

def on_page(canvas, doc, page_title):
    header_band(canvas, doc, "SFAR / SAMU DE FRANCE / SFMU — CONFÉRENCE D'EXPERTS, TEXTE COURT, 2002",
                "AL/ALR par médecins non spécialisés — urgences",
                page_title, icon_fn=lambda c, x, y: icon_shield(c, x, y, 13 * mm), color=TEAL_DARK)
    footer_band(canvas, doc, SOURCE_TXT, f"Page {doc.page} / {TOTAL_PAGES['n']}")

# ---------------------------------------------------------------------------
def _section_intro_pharmaco():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Résumé :</b> conférence d'experts encadrant la pratique de l'anesthésie locale "
        "(AL) et locorégionale (ALR) par des <b>médecins de l'urgence non spécialisés en "
        "anesthésie-réanimation</b> (structures d'accueil des urgences, urgences "
        "préhospitalières). Exclut explicitement l'anesthésie « chirurgicale » (bloc "
        "opératoire, compétence exclusive des anesthésistes-réanimateurs), les ALR "
        "périmédullaires (rachianesthésie, péridurale) et les blocs du tronc/intercostaux/"
        "paravertébraux/interpleuraux/multibloc laryngé. S'applique uniquement lorsque le "
        "même praticien réalise à la fois l'AL/ALR et l'acte d'urgence.", S_BODY),
        bg=BG_PANEL, border=TEAL))
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("Méthodologie & niveaux de preuve"))
    story.append(Spacer(1, 1.5 * mm))
    story.append(grid_table(
        ["Niveau de preuve", "Définition (Tableau 1 source)"],
        [
            ["I", "Études aléatoires, faible risque de faux positifs (α) et faux négatifs (β) — puissance élevée (β = 5-10 %)."],
            ["II", "Risque α élevé, ou faible puissance."],
            ["III", "Études non aléatoires, sujets « contrôlés » contemporains."],
            ["IV", "Études non aléatoires, sujets « contrôlés » non contemporains."],
            ["V", "Études de cas, avis d'experts."],
        ], [22 * mm, CW_FULL - 22 * mm], head_bg=TEAL_DARK))
    story.append(Spacer(1, 2 * mm))
    story.append(grade_table([
        ("A", "Deux (ou plus) études de niveau I."),
        ("B", "Une étude de niveau I."),
        ("C", "Étude(s) de niveau II."),
        ("D", "Étude(s) de niveau III."),
        ("E", "Étude(s) de niveau IV ou V."),
    ], [22 * mm, CW_FULL - 22 * mm]))
    story.append(Spacer(1, 2.5 * mm))
    story.append(section_bar("Question 1 — Propriétés et risques des anesthésiques locaux (AL)"))
    story.append(Spacer(1, 1.5 * mm))
    story.append(theme_table([
        ("Familles", "Aminoesters (procaïne, tétracaïne — pratiquement plus utilisés en "
         "Europe) et aminoamides (lidocaïne, mépivacaïne, bupivacaïne, ropivacaïne, "
         "articaïne)."),
        ("Puissance faible", "Lidocaïne, prilocaïne, mépivacaïne : délai d'action court "
         "(5-10 min selon le site), durée d'action 1h30-2h."),
        ("Puissance élevée", "Ropivacaïne, bupivacaïne : délai d'action plus long "
         "(10-20 min), durée d'action 2h30-3h30."),
        ("Pharmacocinétique", "Liaison protéique importante pour tous les amides ; "
         "acidose, hypoventilation et âge extrême (<1 an ou très avancé) diminuent la "
         "fixation protéique et augmentent la toxicité systémique. Métabolisme hépatique "
         "exclusif (cytochrome P450) — risque de surdosage en cas de bas débit cardiaque "
         "(insuffisance cardiaque, choc mal compensé, bêta-bloquants, ventilation "
         "mécanique). Solutions adrénalinées : ralentissent l'absorption systémique, "
         "augmentent la durée du bloc."),
        ("Ordre du pic d'absorption (décroissant)", "Scalp/infiltration autres territoires "
         "(gros volumes, risque de pic précoce, enfant particulièrement exposé) > "
         "anesthésie topique ORL/respiratoire (résorption très rapide) > bloc "
         "intercostal (absorption dès 6-10 min) > blocs fémoral/iliofascial."),
        ("Prudence", "Réinjections d'anesthésiques locaux, même espacées : risque toxique "
         "des doses cumulées. Chez l'enfant de moins d'un an : caractéristiques "
         "physiologiques imposant un usage particulier."),
    ], [40 * mm, CW_FULL - 40 * mm]))
    story.append(Spacer(1, 2.5 * mm))
    story.append(section_bar("Toxicité des anesthésiques locaux", color=RED))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>Toxicité locale :</b> la lidocaïne notamment est toxique pour le nerf, mais "
        "cette toxicité ne se manifeste que lors de rachianesthésies (hors champ de ce "
        "texte) ou d'injection intraneurale accidentelle. <b>Mécanismes systémiques :</b> "
        "injection accidentelle intravasculaire (d'où la nécessité de vérifier l'absence "
        "de reflux et d'injecter lentement), dose unique trop élevée, ou doses cumulées "
        "trop importantes.", S_BODY_SM))
    story.append(Spacer(1, 1.5 * mm))
    story.append(KeepTogether([
        reco_table([
            ("§2.1.3.2", "Toxicité neurologique centrale (prodromes puis convulsions, "
             "coma avec dépression cardiorespiratoire au stade ultime — Tableau 3) : le "
             "traitement doit être rapide — arrêt de l'injection, oxygénation et "
             "contrôle des voies aériennes, voire administration parentérale "
             "d'anticonvulsivants.", "D"),
        ], RCW),
    ]))
    story.append(Spacer(1, 1.5 * mm))
    story.append(grid_table(
        ["Toxicité neurologique — Tableau 3", ""],
        [
            ["Aspects cliniques", "Crise généralisée tonicoclonique (type grand mal, avec "
             "troubles neurovégétatifs : tachycardie, HTA, mydriase, sudation) ; état de "
             "mal épileptique ; crises partielles complexes possibles ; attaques de "
             "panique/sensation de mort imminente (décharges hippocampiques)."],
            ["Prodromes", "Signes subjectifs : paresthésies, fourmillements des "
             "extrémités, céphalées en casque ou frontales, goût métallique dans la "
             "bouche, malaise général avec angoisse, étourdissement, sensation ébrieuse, "
             "vertiges, logorrhée, hallucinations visuelles ou auditives, bourdonnements "
             "d'oreille. Signes objectifs : pâleur, tachycardie, irrégularité "
             "respiratoire, nausées/vomissements, confusion voire absence, empâtement de "
             "la parole, nystagmus, fasciculations des lèvres/langue. <i>Attention : "
             "peuvent être masqués par une prémédication sédative.</i>"],
            ["Conduite à tenir", "Arrêt de l'injection, décubitus dorsal, matériel de "
             "ventilation préparé (ballon autoremplisseur à valve unidirectionnelle sur "
             "source d'oxygène)."],
        ], [32 * mm, CW_FULL - 32 * mm], head_bg=GREY))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "Tous les anesthésiques locaux sont capables d'induire des accidents convulsifs. "
        "Le rapport des toxicités neurologiques de la bupivacaïne, de la ropivacaïne et "
        "de la lidocaïne est d'environ 4 ; 3 ; 1, correspondant au rapport de puissance "
        "approximatif de ces agents.", S_NOTE))
    story.append(Spacer(1, 1 * mm))
    story.append(P(
        "<b>Toxicité cardiaque :</b> aux concentrations toxiques (&gt;2-3 µg/ml), la "
        "bupivacaïne ralentit la conduction intraventriculaire (élargissement du QRS), "
        "avec risque de tachycardie ventriculaire, torsades de pointes ou bradycardie "
        "extrême — l'accident cardiotoxique peut précéder les prodromes neurologiques "
        "avec la bupivacaïne. Hypoxie, acidose, hypothermie et désordres électrolytiques "
        "(hyponatrémie sévère, hyperkaliémie) majorent le risque.", S_BODY_SM))
    story.append(Spacer(1, 1.5 * mm))
    story.append(reco_table([
        ("§2.1.3.2", "En cas d'arrêt cardiaque toxique lié aux anesthésiques locaux, "
         "aucun médicament anti-arythmique habituellement préconisé dans l'arrêt "
         "cardiaque ne doit être utilisé.", "D"),
        ("§2.1.3.2", "La ropivacaïne (réputée moins cardiotoxique que la bupivacaïne à "
         "dose égale) est une alternative intéressante à la bupivacaïne, dans les rares "
         "cas où un agent de longue durée d'action est requis.", "D"),
    ], RCW))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<i>Prévention :</i> plus que la dose-test adrénalinée, l'injection lente, "
        "fractionnée avec maintien du contact verbal représente la meilleure "
        "prévention.", S_NOTE))
    return story

def _section_intro_pharmaco_2():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(theme_table([
        ("Allergies", "Exceptionnelles pour les anesthésiques locaux amides ; dans les "
         "rares cas avérés, le conservateur des solutions adrénalinées (métabisulfite) "
         "est plus souvent en cause que l'anesthésique local lui-même."),
        ("Méthémoglobinémie", "Cyanose, dyspnée, tachycardie, céphalées, vertiges, "
         "hypoxémie. Chez le nouveau-né/nourrisson : possible jusqu'à 3h après "
         "prilocaïne (exceptionnellement lidocaïne). La crème Emla® contient de la "
         "prilocaïne mais n'expose pas à ce risque si utilisée selon le Tableau 4. "
         "<b>Traitement :</b> bleu de méthylène IV, 1 à 5 mg/kg."),
        ("Adjuvants (vasoconstricteurs)", "Les solutions adrénalinées contiennent un "
         "stabilisant (métabisulfite, allergisant possible) ; le passage intravasculaire "
         "rapide de l'adrénaline peut causer une HTA/malaise étiqueté à tort "
         "« allergie »."),
        ("Contre-indications absolues", "Allergie avérée à la classe (ou à un excipient) ; "
         "porphyrie pour la lidocaïne et la ropivacaïne ; traitement par IMAO de "
         "première génération ; blocs dans les régions à circulation terminale (pénis, "
         "face, doigts, orteils) pour les solutions adrénalinées."),
        ("Contre-indications relatives", "Cardiopathies ischémiques mal compensées ; "
         "thyréotoxicose."),
    ], [40 * mm, CW_FULL - 40 * mm]))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<i>Aspects pratiques (§2.2) :</i> pour minimiser les risques de toxicité "
        "systémique, il faut impérativement limiter les doses injectées, utiliser des "
        "solutions adrénalinées en l'absence de contre-indications (blocs de la face, "
        "interdigitaux et pénien), et préférer les agents les moins toxiques.", S_BODY_SM))
    story.append(Spacer(1, 1.5 * mm))
    story.append(grid_table(
        ["Agent", "Présentation", "Indications", "Posologie maximum*"],
        [
            ["Lidocaïne", "0,5 ; 1 et 2 % sans adrénaline", "Infiltration, bloc "
             "périphérique (de préférence 0,5 % adrénalinée)",
             "300 mg adulte / 5 mg/kg enfant (sans adrénaline) ; 500 mg adulte / "
             "6-7 mg/kg enfant (avec adrénaline 1/200 000)"],
            ["Xylocaïne® 5 % nébuliseur", "—", "Laryngoscopie",
             "10-25 pulvérisations (adulte) ; 2 pulv./10 kg (enfant)"],
            ["Xylocaïne® 5 % naphtazoline", "—", "Anesthésie/vasoconstriction muqueuses, "
             "endoscopie ORL", "25 pulvérisations, 5-8 ml (adulte) ; 0,1 ml/kg "
             "(enfant &gt;6 ans)"],
            ["Xylocaïne® visqueuse 2 %", "—", "Anesthésie buccale",
             "2-3 ml (adulte), absorption variable"],
            ["Xylocaïne® gel urétral 2 %", "—", "Anesthésie urétrale",
             "1 tube (adulte), absorption variable"],
            ["Crème Emla® (tube 30 g)", "—", "Ne pas laisser &gt;20 min au contact des "
             "muqueuses ou d'une plaie", "30 g (adulte)"],
            ["Crème Emla® (tube 5 g)", "—", "Ne pas laisser &gt;20 min au contact des "
             "muqueuses ou d'une plaie", "10 g (adulte, muqueuses) ; 0,15 g/kg (enfant)"],
            ["Mépivacaïne", "1 et 2 %", "Infiltration / bloc périphérique",
             "200 mg (infiltration) / 400 mg (bloc périphérique), adulte"],
            ["Ropivacaïne", "0,2 ; 0,75 et 1 %", "Infiltration, bloc périphérique",
             "150 mg adulte ; 2,5-3 mg/kg enfant &gt;12 ans"],
        ], [26 * mm, 28 * mm, 44 * mm, CW_FULL - 26 * mm - 28 * mm - 44 * mm], head_bg=NAVY))
    story.append(Spacer(1, 1 * mm))
    story.append(P(
        "* Colonne « Posologie maximum » gradée <b>D</b> dans le texte source (Tableau 4). "
        "Infiltration : dose maximale lidocaïne 200 mg. Les présentations contenant un "
        "conservateur sont signalées comme telles dans le texte source.", S_NOTE))
    return story

SECTION1_TITLE = "Méthodologie, pharmacologie & toxicité des anesthésiques locaux"
def _section1_all():
    return _section_intro_pharmaco() + _section_intro_pharmaco_2()

# ---------------------------------------------------------------------------
def _section_al_topique_infiltration():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("Question 2 — Indications, contre-indications et méthodes de l'AL et de l'ALR"))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P("<b>3.1 Anesthésie locale (AL)</b> — topique (muqueuses/peau) ou par "
                    "infiltration.", S_H2))
    story.append(Spacer(1, 1 * mm))
    story.append(theme_table([
        ("Muqueuses", "Analgésie efficace des muqueuses saines (nez, bouche, gorge, arbre "
         "trachéobronchique, œsophage, appareil génito-urinaire) par lidocaïne ou crème "
         "Emla® (≤20 min sur les muqueuses). Indications : traitement symptomatique de la "
         "douleur buccale/œsophagienne/hémorroïdaire (lidocaïne à ne pas poursuivre au "
         "retour à domicile — risque de convulsion, voire de décès) ; AL de contact avant "
         "explorations instrumentales (stomatologie, laryngoscopie, fibroscopie "
         "œso-gastrique) ; AL de surface avant infiltration ou geste douloureux ; AL "
         "nasale avant geste invasif ; AL avant exploration urologique ou infiltration "
         "des muqueuses génitales. <i>Risque :</i> suppression du réflexe de protection "
         "des voies aériennes supérieures — éviter toute alimentation solide/liquide "
         "pendant 4h après anesthésie des muqueuses du carrefour aérodigestif "
         "supérieur. Les gels peuvent induire une réaction positive aux tests "
         "antidopage."),
        ("Peau (Emla®)", "Mélange lidocaïne 2,5 %/prilocaïne 2,5 %, sous pansement occlusif "
         "≥1h, durée d'action 1-2h, anesthésie sur 5 mm de profondeur maximum. "
         "Indications : peau saine avant ponctions/abords vasculaires, ponction "
         "lombaire ou ALR ; avant chirurgie cutanée superficielle (incluant "
         "paraphimosis) ; avant détersion mécanique des ulcères veineux. Utilisable sur "
         "peau lésée à doses réduites. Éviter le contact oculaire."),
        ("Corps étrangers auriculaires", "Anesthésie du conduit auditif externe et de la "
         "membrane tympanique indiquée pour l'ablation en urgence. La perforation "
         "tympanique est une contre-indication."),
        ("Œil douloureux", "Instillation d'1-2 gouttes d'oxybuprocaïne (Novesine® 0,2 %) "
         "pour examiner sans douleur. <b>Ne pas poursuivre</b> : risque de lésions "
         "cornéennes graves par suppression de la sensibilité de la cornée."),
    ], [32 * mm, CW_FULL - 32 * mm]))
    story.append(Spacer(1, 1.5 * mm))
    story.append(reco_table([
        ("§3.1.2.2", "L'utilisation de l'Emla® n'est pas contre-indiquée chez l'enfant "
         "de moins de trois mois.", "B"),
    ], RCW))
    story.append(Spacer(1, 2 * mm))
    story.append(P("<b>Anesthésie par infiltration</b> — d'installation plus rapide que "
                    "la topique mais nécessitant plus de produit ; pour les plaies "
                    "étendues, la dose totale peut approcher la dose toxique.", S_H2))
    story.append(Spacer(1, 1 * mm))
    story.append(P(
        "<b>Choix de l'agent :</b> lidocaïne et mépivacaïne recommandées. La bupivacaïne "
        "n'a pas d'AMM pour cette indication (cardiotoxicité, cf. Question 1). Solutions "
        "adrénalinées recommandées sauf contre-indications (face, doigts).", S_BODY_SM))
    story.append(Spacer(1, 1.5 * mm))
    story.append(reco_table([
        ("§3.1.3.2", "Pour diminuer la douleur de l'injection : aiguilles de petit "
         "calibre, solutions réchauffées, injection intradermique régulière et lente "
         "dans les berges de la plaie et de proche en proche (technique également "
         "requise pour prévenir le risque septique en peau saine si la plaie est "
         "contaminée, et éviter l'injection intravasculaire).", "B"),
    ], RCW))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<i>Choix de la technique (§3.1.4) :</i> les méthodes sont associables (topique + "
        "ALR, topique + infiltration, ALR + infiltration complémentaire). Une surface "
        "opératoire étendue fait préférer une technique locorégionale (risque de "
        "toxicité systémique des grands volumes en infiltration). Le risque de "
        "distorsion des berges d'une plaie complexe fait préférer une anesthésie "
        "topique ou une ALR.", S_NOTE))
    return story

def _section_blocs_intro_contraintes():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(section_bar("3.2 Blocs locorégionaux (ALR)"))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "Les ALR périmédullaires (rachianesthésie, péridurale), les blocs du tronc, "
        "intercostaux, paravertébraux, interpleuraux et le multibloc laryngé sortent "
        "explicitement du cadre de ces recommandations (efficacité variable, iatrogénie "
        "potentielle). Les blocs périphériques, sans retentissement général "
        "(hémodynamique, ventilatoire, neurologique central), sont bien adaptés à "
        "l'urgence.", S_BODY_SM))
    story.append(Spacer(1, 1.5 * mm))
    story.append(reco_table([
        ("§3.2", "Deux situations se prêtent, de manière schématique, à la mise en "
         "œuvre d'une ALR dans le cadre de ces recommandations : les traumatismes des "
         "membres et les traumatismes de la face.", "A"),
        ("§3.2", "Le seul bloc qui, de manière consensuelle, semble adapté à l'urgence "
         "extrahospitalière est le bloc du nerf fémoral.", "D"),
    ], RCW))
    story.append(Spacer(1, 2 * mm))
    story.append(P("<b>3.2.1 Contraintes et spécificités de l'urgence</b>", S_H2))
    story.append(Spacer(1, 1 * mm))
    story.append(P(
        "Le contexte de l'urgence ne dispense pas de dresser par écrit un inventaire "
        "précis et exhaustif des lésions. Contre-indications classiques à respecter : "
        "infection locale, troubles majeurs de l'hémostase, exceptionnelle allergie aux "
        "anesthésiques locaux.", S_BODY_SM))
    story.append(Spacer(1, 1.5 * mm))
    story.append(reco_table([
        ("§3.2.1", "Il est indispensable, avant tout bloc, de consigner par écrit les "
         "données de l'examen neurologique (motricité, sensibilité) de la zone "
         "considérée.", "E"),
        ("§3.2.1", "L'interrogatoire, lorsqu'il est possible, doit rechercher une "
         "anomalie constitutionnelle ou acquise de l'hémostase (un bilan biologique "
         "d'hémostase systématique n'est pas utile).", "E"),
        ("§3.2.1", "Avant la réalisation d'une ALR (bloc fémoral ou iliofascial), un "
         "niveau élevé de douleur, spontanée ou induite par une éventuelle mobilisation "
         "du malade, justifie une analgésie première par voie systémique.", "E"),
    ], RCW))
    return story

SECTION2_TITLE = "Anesthésie locale, infiltration & ALR — cadre général"
def _section2_all():
    return _section_al_topique_infiltration() + _section_blocs_intro_contraintes()

# ---------------------------------------------------------------------------
def _section_blocs_membres():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("3.2.2 ALR et traumatismes des membres"))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P("<b>Bloc du nerf fémoral / bloc iliofascial</b>", S_H2))
    story.append(Spacer(1, 1 * mm))
    story.append(KeepTogether([
        reco_table([
            ("§3.2.2.1", "Le bloc du nerf fémoral pour fracture de la diaphyse fémorale "
             "est la technique d'ALR la plus répandue et la plus éprouvée en urgence, "
             "procurant de manière prévisible une analgésie d'excellente qualité, chez "
             "l'enfant comme chez l'adulte, pour l'urgence pré- et intrahospitalière.",
             "A"),
        ], RCW),
    ]))
    story.append(Spacer(1, 1.5 * mm))
    story.append(reco_table([
        ("§3.2.2.1", "Indications : analgésie pour fracture de diaphyse fémorale ainsi "
         "que pour les plaies du genou — permettent, dans d'excellentes conditions "
         "d'analgésie, la mobilisation et le transport, la réalisation de clichés "
         "radiographiques, et la mise d'une attelle après pose éventuelle d'une broche "
         "de traction.", "A"),
        ("§3.2.2.1", "Ces blocs sont partiellement efficaces pour la prise en charge "
         "analgésique des fractures des extrémités supérieure ou inférieure du fémur.",
         "B"),
        ("§3.2.2.1", "Le bloc iliofascial doit être recommandé comme la technique de "
         "référence dans le cadre de l'urgence et permet de s'affranchir de "
         "l'utilisation d'un neurostimulateur.", "A"),
    ], RCW))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<i>Méthode :</i> patient en décubitus dorsal, point de ponction à la jonction "
        "1/3 moyen-1/3 externe du ligament inguinal (arcade crurale) ; l'aiguille à "
        "biseau court franchit le fascia lata puis le fascia iliaca (deux ressauts "
        "successifs) avant l'injection dans l'espace iliofascial.", S_BODY_SM))
    story.append(Spacer(1, 1.5 * mm))
    story.append(reco_table([
        ("§3.2.2.1", "Avec cette technique, le taux de succès est de 88 % pour le nerf "
         "fémoral (crural), de 90 % pour le nerf cutané latéral (fémorocutané), et de "
         "38 % pour le nerf obturateur — le bloc « 3 en 1 » échappe souvent au territoire "
         "obturateur (partie inféro-interne de la cuisse, adducteurs).", "B"),
        ("§3.2.2.1", "Des volumes de 0,3 à 0,4 ml/kg de lidocaïne à 1 % sont suffisants "
         "chez l'adulte pour anesthésier les trois branches du plexus lombaire — le "
         "recours à des volumes plus importants n'améliore pas la qualité du bloc.", "C"),
        ("§3.2.2.1", "Chez l'enfant, à défaut d'information précise sur le poids, le "
         "volume de lidocaïne 1 % peut être estimé à 1 ml/année d'âge (ropivacaïne non "
         "validée dans cette indication).", "C"),
    ], RCW))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<i>Délai :</i> l'analgésie débute entre la 5e et la 15e minute selon "
        "l'anesthésique local ; dès le bloc installé, le membre doit être immobilisé "
        "pour ne pas risquer un déplacement des fragments et une lésion "
        "vasculonerveuse secondaire alors que le signal d'alarme « douleur » a "
        "disparu.", S_NOTE))
    story.append(Spacer(1, 2 * mm))
    story.append(KeepTogether([
        P("<b>Blocs du pied</b>", S_H2),
        Spacer(1, 1 * mm),
        P("Patient en décubitus dorsal, jambe et cuisse fléchies, pied reposant à plat "
          "sur la table. Nerfs fibulaire superficiel (musculocutané) et sural, par "
          "injection sous-cutanée au niveau de la cheville, à quatre travers de doigt "
          "au-dessus de la pointe de la malléole latérale. Autres blocs, moins "
          "utilisés : nerf tibial (tibial postérieur), rameau calcanéen médial du nerf "
          "tibial postérieur (nerf calcanéen interne), fibulaire profond (nerf tibial "
          "antérieur).", S_BODY_SM),
        Spacer(1, 1 * mm),
        reco_table([
            ("§3.2.2.2", "Les blocs du pied sont proposés pour la prise en charge de "
             "plaies du pied.", "D"),
        ], RCW),
    ]))
    story.append(Spacer(1, 2 * mm))
    story.append(P("<b>Blocs du membre supérieur</b> — seuls les blocs tronculaires "
                    "périphériques sont retenus (lidocaïne 1 % non adrénalinée, "
                    "3-4 ml/bloc).", S_BODY_SM))
    story.append(Spacer(1, 1 * mm))
    story.append(theme_table([
        ("Nerf médian", "Face antérieure du poignet, dans le canal carpien, entre les "
         "tendons des muscles fléchisseur radial du carpe (grand palmaire) et long "
         "palmaire (petit palmaire) — injection après franchissement du rétinaculum "
         "des fléchisseurs (ligament annulaire)."),
        ("Nerf radial", "Avant-bras en position neutre, colonne du pouce en abduction "
         "et extension ; ligne transversale de 3 cm tracée à l'angle supérieur de la "
         "tabatière anatomique, 3 ml d'anesthésique local infiltrés en sous-cutané sur "
         "cette ligne."),
        ("Nerf ulnaire", "Pli de flexion tracé sur un poignet en extension ; point "
         "marqué 2-3 cm au-dessus, au bord médial interne du muscle fléchisseur "
         "ulnaire du carpe (cubital antérieur)."),
    ], [32 * mm, CW_FULL - 32 * mm]))
    story.append(Spacer(1, 1.5 * mm))
    story.append(reco_table([
        ("§3.2.2.3", "Ces blocs tronculaires périphériques permettent l'exploration et "
         "la suture de plaies n'intéressant qu'un ou deux territoires de la main.", "D"),
    ], RCW))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>Bloc de la gaine des fléchisseurs</b> — particulièrement intéressant pour "
        "les gestes courts sur les 2e-4e doigts (sutures de plaies, excision partielle "
        "ou reposition d'ongles, extraction de corps étranger, réduction de luxation "
        "interphalangienne, incision d'abcès). Aiguille introduite avec un angle de 45° "
        "au niveau du pli cutané de flexion métacarpophalangien ; le tendon fléchisseur "
        "est repéré par des mouvements de flexion au niveau de la tête du métacarpien "
        "correspondant ; la bonne position de l'aiguille dans la gaine tendineuse est "
        "attestée par sa verticalisation lors des mouvements de flexion — une injection "
        "sans résistance prouve que la solution est dans la gaine du tendon (lidocaïne "
        "non adrénalinée).", S_BODY_SM))
    story.append(Spacer(1, 1.5 * mm))
    story.append(reco_table([
        ("§3.2.2.3", "Cette technique doit être adoptée en lieu et place de l'ancienne "
         "technique d'anesthésie des nerfs collatéraux des doigts — relativement "
         "douloureuse et incriminée dans la survenue d'ischémie par compression "
         "d'artérioles terminales.", "B"),
    ], RCW))
    return story

def _section_blocs_face_sedation():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("3.2.3 ALR et traumatismes de la face"))
    story.append(Spacer(1, 1.5 * mm))
    story.append(reco_table([
        ("§3.2.3", "Les blocs de la face devraient supplanter au service d'accueil des "
         "urgences les traditionnelles anesthésies locales de la face, où l'on finit par "
         "infiltrer des volumes excessifs d'anesthésique local pour suturer des plaies "
         "aux berges devenues succulentes.", "E"),
        ("§3.2.3", "L'anesthésie tronculaire de la face représente une alternative de "
         "choix à l'anesthésie générale, chez des malades à l'estomac plein, pour "
         "sutures de plaies multiples de la face.", "D"),
    ], RCW))
    story.append(Spacer(1, 1.5 * mm))
    story.append(grid_table(
        ["Bloc", "Nerf (origine)", "Zone anesthésiée"],
        [
            ["Supra-orbitaire + supratrochléaire", "Nerf frontal, branche du nerf "
             "ophtalmique (V1) — foramen supra-orbitaire, à l'aplomb de la pupille",
             "Front (jusqu'à la suture coronale) et paupières supérieures, si bilatéral"],
            ["Infra-orbitaire", "Nerf infra-orbitaire, branche du nerf maxillaire (V2) — "
             "foramen infra-orbitaire, voie orale ou externe", "Joue et hémilèvre "
             "supérieure"],
            ["Mentonnier", "Nerf mentonnier, branche du nerf mandibulaire (V3) — foramen "
             "mentonnier, voie buccale ou transcutanée", "Menton et lèvre inférieure"],
        ], [42 * mm, 70 * mm, CW_FULL - 42 * mm - 70 * mm], head_bg=NAVY))
    story.append(Spacer(1, 2.5 * mm))
    story.append(section_bar("3.3 Sédation associée & 3.4 Analgésie associée"))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "Certains cas d'agitation peuvent nécessiter une sédation pour faciliter la "
        "réalisation du bloc. Aucune étude ne rapporte de majoration du risque de "
        "lésion nerveuse liée à la ponction lorsqu'une sédation légère est associée "
        "(niveau n'empêchant ni la paresthésie-signal d'alarme, ni le contact verbal). "
        "Sédation par voie IV périphérique, surveillance clinique et instrumentale "
        "(scope, oxymètre, PNI) obligatoire.", S_BODY_SM))
    story.append(Spacer(1, 1.5 * mm))
    story.append(reco_table([
        ("§3.3", "L'échec partiel ou total d'un bloc ne constitue en aucun cas "
         "l'indication d'une sédation.", "E"),
        ("§3.3", "Un score de Ramsay égal à 2 (patient coopérant, orienté et tranquille) "
         "est l'objectif souhaité — l'utilisation de médicaments facilement "
         "antagonisables est un gage de sécurité. Le midazolam (anxiolyse et amnésie), "
         "en titration par bolus de 0,5 à 1 mg, est la benzodiazépine la mieux adaptée "
         "à l'urgence (variabilité interindividuelle importante) ; les autres "
         "hypnotiques sont inadaptés à la sédation de complément d'une ALR en urgence.",
         "E"),
        ("§3.3", "Le risque de dépression respiratoire est majoré par l'association à "
         "un morphinique.", "B"),
        ("§3.3", "L'association d'un morphinique à la sédation d'une ALR doit donc être "
         "évitée.", "E"),
        ("§3.4", "La morphine est l'opiacé de référence pour assurer une analgésie "
         "préalable ou de complément (bolus initial 0,05 mg/kg IV, puis bolus titrés de "
         "2-3 mg toutes les 5 min) — les opiacés agonistes partiels ne sont pas "
         "recommandés.", "D"),
        ("§3.4", "Le mélange équimolaire oxygène-protoxyde d'azote (MEOPA), par son "
         "action sédative et analgésique, peut également être utilisé en complément "
         "d'une ALR.", "E"),
    ], RCW))
    return story

SECTION3_TITLE = "Blocs des membres, de la face & sédation/analgésie associées"
def _section3_all():
    return _section_blocs_membres() + _section_blocs_face_sedation()

# ---------------------------------------------------------------------------
def _section_precautions_surveillance():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("Question 3 — Précautions, surveillance et monitorage"))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>4.1 Complications</b> — outre la syncope vagale, la toxicité systémique et "
        "les réactions anaphylactiques (Tableau 5 ci-dessous), deux autres types de "
        "complications sont décrits dans le texte source : les <b>complications "
        "neurologiques périphériques</b> (traumatisme ou lésion ischémique par "
        "compression — le bloc moteur/sensitif peut masquer un traumatisme initial ou "
        "secondaire lié à un défaut d'immobilisation, un syndrome de loge, etc. ; une "
        "lésion neurologique préalable doit être recherchée, diagnostiquée et consignée "
        "par écrit avant l'ALR) et les <b>complications septiques</b> (favorisées par "
        "une antisepsie insuffisante ou une infection à proximité du point "
        "d'infiltration).", S_BODY_SM))
    story.append(Spacer(1, 2 * mm))
    story.append(grid_table(
        ["Complication — Tableau 5", "Prévention", "Signes cliniques / paracliniques "
         "(risque évolutif)", "Traitement"],
        [
            ["Syncope vagale", "Éviter milieu confiné/surchauffé ; décubitus dorsal",
             "Sueurs, malaise, pâleur, bradycardie (ECG), hypotension (PNI) → risque "
             "d'arrêt cardiaque",
             "Arrêt de la stimulation douloureuse, décubitus dorsal, surélévation des "
             "membres inférieurs, stimulation du patient ; oxygène 100 % ; atropine IV "
             "20 µg/kg ; recherche d'une cause déclenchante"],
            ["Réactions anaphylactiques", "Interrogatoire : recherche de réactions "
             "allergiques connues aux AL (éviction des produits en cause)",
             "Signes cutanés (érythème, urticaire), respiratoires (bronchospasme, gêne "
             "laryngée), tachycardie (ECG), hypotension (PNI), hypoxie (SpO2) → risque "
             "d'arrêt cardiaque",
             "Arrêt de l'injection ; antihistaminique ; oxygène 100 % ; si hypotension "
             "grave : voie veineuse + adrénaline titrée ; réanimation de l'arrêt "
             "cardiaque si besoin"],
            ["Toxicité systémique des AL", "Respect des doses maximales ; limitation des "
             "doses ; test d'aspiration avant et pendant l'injection ; injection "
             "fractionnée, lente ; maintien du contact verbal",
             "Bourdonnement d'oreille, hyperacousie, dysesthésies péribuccales, goût "
             "métallique, sensation de malaise, logorrhée ; convulsions (ECG : QRS "
             "élargi, tachycardie ventriculaire) ; troubles cardiaques : tachycardie, "
             "bradycardie (PNI : hypotension) → coma, arrêt cardiaque",
             "Arrêt de l'injection ; oxygène 100 % (éviter l'hypercapnie) ; "
             "anticomitial IV ; traitement symptomatique du coma et de l'arrêt "
             "cardiaque ; <b>aucun antiarythmique</b> en cas de troubles du rythme"],
        ], [26 * mm, 30 * mm, 46 * mm, CW_FULL - 26 * mm - 30 * mm - 46 * mm], head_bg=RED))
    return story

def _section_mesures_monitorage():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("4.2 Mesures de précaution", color=TEAL_DARK))
    story.append(Spacer(1, 1.5 * mm))
    for b in bullets([
        "L'opérateur doit avoir été formé pour la technique choisie.",
        "C'est au médecin réalisant l'acte d'évaluer le rapport bénéfice-risque pour le "
        "patient.",
        "Le choix de la technique dépend de l'indication, des comorbidités, des "
        "circonstances de survenue des lésions et de l'avis du patient.",
        "Information et recherche du consentement, chaque fois que possible.",
        "Neurostimulateur (recommandé pour les blocs distaux — poignet, chevilles) : "
        "maintenance et vérification avant chaque utilisation.",
        "Installation confortable du patient ; règles d'asepsie strictement appliquées.",
        "Procédures de sécurité contre les erreurs (conditionnements spécifiques, "
        "étiquetage des seringues).",
        "Contact verbal maintenu pendant la réalisation de l'AL/ALR.",
        "Aiguilles à biseau court recommandées.",
        "Prévention de la toxicité systémique : connaissance/respect des doses "
        "maximales, dose la plus faible possible, test d'aspiration avant et répété "
        "pendant l'injection, injection lente et fractionnée, recherche de "
        "tachycardie/HTA pendant l'injection de solutions adrénalinées.",
        "La recherche de paresthésie est fortement déconseillée.",
        "Une douleur fulgurante pendant la procédure impose l'arrêt immédiat de "
        "l'injection.",
        "Respect des délais d'installation de l'analgésie ; l'échec ne peut être "
        "envisagé qu'au-delà de ces délais (attention au risque de doses cumulées).",
        "Traçabilité écrite complète (patient, techniques, agents, déroulement, "
        "événements, suivi) — une fiche spécifique peut être utilisée.",
        "Chaîne de soins organisée : procédures communes avec les "
        "anesthésistes-réanimateurs, procédure d'appel d'un praticien en recours.",
    ]):
        story.append(b)
    story.append(Spacer(1, 2 * mm))
    story.append(section_bar("4.3 Monitorage", color=TEAL_DARK))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "Le monitorage cardiorespiratoire (scope, pression non invasive, SpO2) doit être "
        "disponible sans délai. Le choix des moyens de surveillance (installés avant le "
        "geste) dépend des doses d'anesthésique local, du type d'ALR, du geste "
        "(durée…), des comorbidités et de l'état du patient. En cas de sédation "
        "associée : voie veineuse périphérique et monitorage cardiorespiratoire "
        "d'emblée. Le matériel de réanimation pour la prise en charge des "
        "complications doit être immédiatement disponible, et le médecin formé à son "
        "utilisation.", S_BODY_SM))
    return story

SECTION4_TITLE = "Précautions, surveillance & monitorage (Question 3)"
def _section4_all():
    return _section_precautions_surveillance() + _section_mesures_monitorage()

# ---------------------------------------------------------------------------
def _section_milieu_difficile_enfant():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("Question 4 — Particularités des AL/ALR en milieu difficile et chez l'enfant"))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>Milieu difficile</b> (sauvetage individuel ou collectif — montagne, mer, "
        "transports en commun…) : les règles de sécurité et de formation des personnels "
        "sont particulièrement importantes. Problèmes spécifiques : conditions "
        "précaires d'évaluation et de réalisation (sécurité, hygiène, climat), durées de "
        "prise en charge, conséquences du relevage/transport, hypothermie, afflux "
        "massif de victimes ou inadéquation entre le nombre d'équipes médicales et le "
        "nombre de patients, impossibilité de monitorage. La nécessité d'une analgésie "
        "efficace et précoce ne doit pas être remise en question du seul fait que le "
        "milieu est difficile.", S_BODY_SM))
    story.append(Spacer(1, 1.5 * mm))
    story.append(reco_table([
        ("§Milieu diff.", "Toutes les techniques d'anesthésie locale préconisées dans ces "
         "recommandations peuvent être utilisées sous couvert des règles habituelles de "
         "sécurité — le bloc iliofascial doit être largement diffusé dans ce contexte, "
         "en particulier en cas d'afflux de victimes.", "E"),
        ("§Milieu diff.", "Dans certains cas particuliers (patient incarcéré, victime en "
         "milieu périlleux…), une analgésie préalable par voie intraveineuse peut "
         "s'avérer nécessaire, mais ne contre-indique pas la réalisation ultérieure de "
         "l'ALR.", "E"),
    ], RCW))
    story.append(Spacer(1, 2 * mm))
    story.append(P("<b>5.1 Particularités chez l'enfant</b> — l'AL est régulièrement "
                    "indiquée aux urgences (exploration/suture de plaie) ; les "
                    "anesthésies tronculaires se limitent aux blocs fémoral/iliofascial "
                    "(fractures de fémur) et aux blocs tronculaires au poignet "
                    "(traumatologie de la main).", S_H2))
    story.append(Spacer(1, 1 * mm))
    story.append(reco_table([
        ("§5.1", "Chez l'enfant de moins d'un an, la pharmacologie des anesthésiques "
         "locaux diffère fondamentalement de l'adulte (immaturité des métabolismes "
         "hépatique et rénal, diminution de certaines protéines plasmatiques), majorant "
         "le risque d'accumulation et de toxicité ; seule la lidocaïne est recommandée, "
         "à dose rapportée au poids corporel.", "D"),
        ("§5.1", "Comme chez l'adulte, le maintien du contact verbal est essentiel.",
         "C"),
        ("§5.1", "Les solutions associant de la cocaïne aux anesthésiques locaux doivent "
         "être évitées en raison de leurs dangers.", "D"),
        ("§5.1", "Le mélange équimoléculaire oxygène-protoxyde d'azote est utilisable "
         "chez l'enfant de plus de quatre ans, en respectant ses contre-indications "
         "habituelles.", "C"),
    ], RCW))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<i>Pratique :</i> AL par Emla® ou infiltration (aiguille la plus fine "
        "possible) ; conditions de monitorage/accès veineux identiques à l'adulte. "
        "Une sédation est souvent nécessaire chez l'enfant — rechercher au préalable une "
        "hypovolémie pouvant se masquer en agitation isolée ; objectif de sédation "
        "consciente par titration.", S_NOTE))
    return story

def _section_formation_sources():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(section_bar("Question 5 — Formation nécessaire", color=TEAL_DARK))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "L'AL fait partie de la formation universitaire initiale du médecin. La "
        "pratique de techniques d'ALR par des médecins non anesthésistes-réanimateurs, "
        "dans le contexte de la médecine d'urgence, peut se concevoir à condition de "
        "respecter la réglementation et les recommandations de la SFAR, et après avoir "
        "bénéficié d'une formation reconnue, théorique et pratique, notamment au bloc "
        "opératoire. Cela implique :", S_BODY_SM))
    story.append(Spacer(1, 1 * mm))
    for b in bullets([
        "Une formation théorique et pratique initiale encadrée par des médecins "
        "anesthésistes-réanimateurs.",
        "Une formation médicale continue accréditée.",
        "L'élaboration de procédures et de cahiers de protocoles, intégrés dans une "
        "approche globale du patient en situation d'urgence (soins préhospitaliers, "
        "SAU, bloc opératoire — sans interférer avec une technique d'anesthésie "
        "nécessaire à l'acte chirurgical).",
        "La mise en place de ces protocoles et procédures.",
        "La mise en place des moyens cliniques et biomédicaux de surveillance, de "
        "suppléance et de sécurité.",
        "La vérification du matériel avant chaque usage.",
        "La rédaction d'une fiche de surveillance (produits utilisés, variables de "
        "surveillance en fonction du temps).",
        "Une information au patient (ou à défaut à l'accompagnant) sur la procédure "
        "utilisée et les consignes de surveillance en cas de sortie.",
        "L'évaluation régulière des pratiques.",
    ]):
        story.append(b)
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "Conformément aux règles déontologiques, les praticiens doivent connaître les "
        "indications et les contre-indications des anesthésiques locaux et des "
        "techniques, acquérir l'expérience de leur utilisation et disposer des moyens, "
        "en particulier de surveillance, pour les mettre en œuvre. Ces connaissances "
        "doivent être régulièrement actualisées.", S_NOTE))
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("Sources et traçabilité", color=GREY))
    story.append(Spacer(1, 2 * mm))
    story.append(P(
        "<b>Document source :</b> « Pratique des anesthésies locales et locorégionales "
        "par des médecins non spécialisés en anesthésie-réanimation, dans le cadre des "
        "urgences » — Conférence d'experts, texte court, Société française "
        "d'anesthésie et de réanimation (SFAR), Samu de France, Société francophone de "
        "médecine d'urgence (SFMU), 2002. Publié Ann Fr Anesth Réanim 2004;23:167-176.",
        S_SOURCE))
    story.append(Spacer(1, 1 * mm))
    story.append(P("<b>Méthodologie :</b> conférence d'experts, grille EBM Niveaux de "
                    "preuve I-V / Grades A-E — voir détail en page 1.", S_SOURCE))
    story.append(Spacer(1, 1 * mm))
    story.append(P(
        "<b>URL source :</b> https://sfar.org/wp-content/uploads/2016/01/2_AFAR_"
        "Pratique-des-anesthesies-locales-et-locoregionales-par-des-medecins-non-"
        "specialises-en-anesthesie-reanimation-dans-le-cadre-des-urgences.pdf",
        S_SOURCE))
    story.append(Spacer(1, 1 * mm))
    story.append(P(
        "<b>Couverture :</b> intégralité des 34 énoncés gradés individuellement "
        "(Questions 1-5) et des 5 tableaux du texte source (niveaux de preuve, grades, "
        "toxicité neurologique, posologie des AL, gestion des complications) — voir "
        "convention de référencement §<i>sous-section</i> disclosée en page 1 (source "
        "non numérotée Rx.y).", S_SOURCE))
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Avertissement — texte de 2002 :</b> cette fiche de synthèse indépendante "
        "reprend l'intégralité des recommandations du texte source, mais ne le "
        "remplace pas et n'est ni éditée ni validée par la SFAR. Se référer aux "
        "protocoles locaux du service d'urgence et au texte intégral (y compris ses "
        "références bibliographiques [1]-[11], non reprises ici) pour toute décision "
        "clinique.", S_BODY_SM), bg=GREY_LIGHT, border=GREY))
    return story

SECTION5_TITLE = "Milieu difficile, enfant, formation & sources"
def _section5_all():
    return _section_milieu_difficile_enfant() + _section_formation_sources()

def _section123_all():
    return _section1_all() + _section2_all() + _section3_all()

def _section45_all():
    return _section4_all() + _section5_all()

def _section_full():
    return _section123_all() + _section45_all()

SECTIONS = [
    ("Pharmacologie, toxicité, blocs, précautions & sources", _section_full),
]

def _make_doc(path=None):
    return SimpleDocTemplate(path or OUT, pagesize=A4,
                              leftMargin=MARGIN, rightMargin=MARGIN,
                              topMargin=32 * mm, bottomMargin=16 * mm,
                              title="Fiche SFAR 2002 - AL-ALR par medecins non specialises en urgence",
                              author="Synthèse indépendante (source SFAR/Samu de France/SFMU)")

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
