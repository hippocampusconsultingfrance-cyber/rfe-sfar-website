# -*- coding: utf-8 -*-
"""
Fiche de synthese - "Les blocs perimedullaires chez l'adulte" - Question 1
(Information au patient) et Question 2 (Contre-indications generales,
surveillance et monitorage) - Recommandations pour la Pratique Clinique
(RPC), SFAR/Sofcot/Sofmer, presentees le 24 septembre 2005 (47e congres
SFAR), publiees Ann Fr Anesth Reanim 26 (2007) 720-752.

PERIMETRE VOLONTAIREMENT LIMITE (pattern deja etabli dans ce corpus pour
les documents tres volumineux) : le document source complet (33 pages,
15 "Questions" cliniques) contient au total 369 citations de grade
individuelles (verifie par grep exhaustif : grade A x69, grade B x65,
grade C x235, accord professionnel x6) - beaucoup trop dense pour une
seule fiche. Cette fiche couvre INTEGRALEMENT les Questions 1 et 2
(information au patient ; contre-indications generales, surveillance et
monitorage) - le "portail d'entree" applicable a TOUTE anesthesie-
analgesie perimedullaire, quel que soit le contexte clinique. Les
Questions 3 a 15 (technique de la rachianesthesie, technique de la
peridurale, association AG-bloc, travail obstetrical, cesarienne,
analgesie postoperatoire, terrains cardiovasculaire/respiratoire/
neurologique/infectieux specifiques, gestion de l'echec, facteurs de
risque de complications) NE SONT PAS couvertes ici - installments futurs
de ce meme document source, a construire separement (chacune de ces
questions est egalement tres dense en citations de grade et merite son
propre decompte/audit dedie).

COLLISION VERIFIEE : ce document (2006/2007) est explicitement cite comme
non remplace par deux fiches deja git-trackees dans ce corpus -
`blocs_peripheriques_membres` (RFE 2011, echographie en ALR) precise
lui-meme dans son propre texte source "Complete, sans les remplacer, les
RPC 2002 (blocs peripheriques des membres) et 2006 (blocs perimedullaires)"
- et `douleur_accouchement_2025` (HAS 2025, analgesie obstetricale au
cours du travail) couvre un perimetre plus etroit et plus recent
(uniquement l'analgesie du travail, Question 6 de CE document) sans
aborder les Questions 1-2 traitees ici (information generale et
contre-indications generales, applicables a tout contexte, pas seulement
obstetrical).

METHODOLOGIE : grille EBM classique A/B/C (Grade A = niveau de preuve 1,
essais randomises de forte puissance/meta-analyses ; Grade B = niveau de
preuve 2, essais randomises de faible puissance/etudes de cohorte ;
Grade C = niveau de preuve 3-4, cas-temoins/etudes retrospectives) +
« Accord professionnel » (absence d'etudes, absence de niveau de preuve)
- chip local "AE" (accord d'experts, deja partage dans ce corpus) utilise
pour "accord professionnel" ET pour l'unique occurrence de la formulation
alternative "avis d'experts" trouvee dans le texte (memes sens, meme
tiers de preuve le plus faible de la grille - disclosed, pas traite comme
un tiers distinct).

DECOMPTE (verifie par regex sur le script final, pas seulement estime a la
lecture) : Question 1 (information) — 3 recommandations gradees (toutes
C) sur un total tres majoritairement narratif/deontologique (obligation
d'information, consentement, preuve de l'information) condense en
reperes pratiques non grades plutot que retranscrit in extenso (regle
7). Question 2 (contre-indications/surveillance) — 38 recommandations
gradees (A:3, C:28, AE:7), verifiees par relecture complete et
regroupees par categorie de risque (neurologique, hemodynamique,
septique, hemostase/anticoagulants, respiratoire, terrain
cardiovasculaire/respiratoire/neurologique, anomalies rachidiennes).
Total : 41 recommandations gradees sur les 2
questions.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from style import *
GRADE_COLORS["A"] = (GREEN, WHITE)
GRADE_COLORS["B"] = (TEAL, WHITE)
GRADE_COLORS["C"] = (AMBER, WHITE)
GRADE_COLORS["AE"] = (GREY, WHITE)
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.units import mm

OUT = "/home/user/rfe-sfar-website/output/Fiche_Blocs_Perimedullaires_Info_CI_2006.pdf"

SOURCE_TXT = ("Source : SFAR/Sofcot/Sofmer, « Les blocs périmédullaires chez l'adulte », "
              "RPC, Ann Fr Anesth Réanim 26 (2007) 720-752 — Questions 1-2 uniquement. "
              "Fiche de synthèse non officielle : se référer au texte intégral.")

def P(txt, style=S_CELL):
    return Paragraph(txt, style)

def chip(label, **kw):
    return grade_chip(label, **kw)

CW_FULL = PAGE_W - 2 * MARGIN

def reco_table(rows, col_widths):
    """rows: (ref, text, grade_label)."""
    data = [[P("Catégorie", S_HEAD_W), P("Recommandation", S_HEAD_W), P("Grade", S_HEAD_W_C)]]
    for ref, txt, grade in rows:
        data.append([P(ref, S_CELL_B), P(txt, S_CELL), chip(grade, width=15 * mm)])
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

RCW = [30 * mm, CW_FULL - 30 * mm - 15 * mm, 15 * mm]

def context_note_local(txt):
    return P(f"<i>Précision du source :</i> {txt}", S_NOTE)

def conversion_table(headers, rows, col_widths):
    data = [[P(h, S_HEAD_W_C) for h in headers]]
    for r in rows:
        data.append([P(c, S_CELL) for c in r])
    t = Table(data, colWidths=col_widths, repeatRows=1)
    style_cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), GREY), ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTNAME", (0, 0), (-1, 0), FONT_BOLD), ("FONTSIZE", (0, 0), (-1, 0), 7.6),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 0.5, GREY_LIGHT),
        ("TOPPADDING", (0, 0), (-1, -1), 2.6), ("BOTTOMPADDING", (0, 0), (-1, -1), 2.6),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            style_cmds.append(("BACKGROUND", (0, i), (-1, i), BG_PANEL))
    t.setStyle(TableStyle(style_cmds))
    return t

def legend_flowable():
    chip_w = 16 * mm
    content_w = CW_FULL
    row = Table([[chip("A", width=chip_w - 2 * mm), chip("B", width=chip_w - 2 * mm),
                  chip("C", width=chip_w - 2 * mm), chip("AE", width=chip_w - 2 * mm),
                  P("<b>Grille EBM classique</b> — <b>A</b> : essais randomisés de forte "
                    "puissance/méta-analyses ; <b>B</b> : essais randomisés de faible "
                    "puissance/études de cohorte ; <b>C</b> : cas-témoins/études "
                    "rétrospectives ; <b>AE</b> : accord professionnel (absence d'études) — "
                    "regroupe aussi l'unique occurrence « avis d'experts » du texte, même "
                    "tiers. Fiche limitée aux Questions 1-2/15 du document (information au "
                    "patient ; contre-indications générales et surveillance).", S_BADGE_HEAD)]],
                colWidths=[chip_w] * 4 + [content_w - 4 * chip_w])
    row.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                              ("LEFTPADDING", (0, 0), (-1, -1), 1),
                              ("RIGHTPADDING", (0, 0), (-1, -1), 1),
                              ("TOPPADDING", (0, 0), (-1, -1), 0),
                              ("BOTTOMPADDING", (0, 0), (-1, -1), 0)]))
    return row

TOTAL_PAGES = {"n": 6}

def on_page(canvas, doc, page_title):
    header_band(canvas, doc, "SFAR/SOFCOT/SOFMER — RPC 2007 (Q1-2/15 — PÉRIMÈTRE LIMITÉ)",
                "Les blocs périmédullaires chez l'adulte",
                page_title, icon_fn=lambda c, x, y: icon_shield(c, x, y, 13 * mm), color=TEAL_DARK)
    footer_band(canvas, doc, SOURCE_TXT, f"Page {doc.page} / {TOTAL_PAGES['n']}")

# ---------------------------------------------------------------------------
def _section_intro_information():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Périmètre limité :</b> le document source complet compte 15 « Questions » "
        "cliniques et 369 citations de grade individuelles — beaucoup trop dense pour une "
        "seule fiche. Cette fiche couvre INTÉGRALEMENT les Questions 1 et 2 (information au "
        "patient ; contre-indications générales, surveillance et monitorage) — le socle "
        "applicable à toute anesthésie-analgésie périmédullaire. Les Questions 3 à 15 "
        "(technique de la rachianesthésie et de la péridurale, association AG-bloc, travail "
        "obstétrical, césarienne, analgésie postopératoire, terrains spécifiques, gestion de "
        "l'échec, facteurs de risque de complications) ne sont PAS couvertes ici — "
        "installments futurs de ce même document, disclosed explicitement.", S_BODY),
        bg=AMBER_LIGHT, border=AMBER))
    story.append(Spacer(1, 2.5 * mm))
    story.append(legend_flowable())
    story.append(Spacer(1, 3 * mm))
    story.append(KeepTogether([
        section_bar("Question 1 — Quelle information donner au patient ?"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(P(
        "<b>Repères non gradés (obligation légale/déontologique) :</b> l'information est un "
        "prérequis du consentement éclairé — elle expose les avantages, inconvénients et "
        "risques de l'ALR périmédullaire par rapport à une AG, y compris le risque d'échec "
        "nécessitant le recours à une AG et le risque exceptionnel de séquelles "
        "neurologiques. Elle est personnalisée, orale en priorité (un document écrit peut la "
        "compléter, jamais la remplacer). La preuve de l'information ne requiert pas la "
        "signature du patient — la meilleure preuve reste une tenue appropriée du dossier "
        "médical. En obstétrique, l'information doit spécifiquement répondre aux "
        "particularités de la douleur du travail, aux bénéfices attendus, aux modalités de "
        "mise en œuvre et aux enjeux propres à une éventuelle césarienne.", S_BODY_SM))
    story.append(Spacer(1, 1.5 * mm))
    story.append(reco_table([
        ("Information", "Les risques habituels et les risques rares mais graves de l'ALR "
         "périmédullaire doivent être précisés à la femme enceinte, mais remis dans leur "
         "contexte.", "C"),
        ("Information", "Toute femme enceinte présentant un risque particulier de césarienne "
         "au cours du travail doit être fortement incitée à bénéficier de la mise en place "
         "précoce d'une analgésie péridurale.", "C"),
        ("Information", "En l'absence de consultation d'anesthésie à distance (réglementaire "
         "mais non réalisée), on ne peut refuser l'analgésie périmédullaire pour ce seul "
         "motif — il faut recueillir en urgence des éléments suffisants et la pratiquer si "
         "les conditions de sécurité sont réunies.", "C"),
    ], RCW))
    return story

# ---------------------------------------------------------------------------
def _section_ci_neuro_hemodynamique_septique():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Question 2 — Prérequis & contre-indications neurologiques, hémodynamiques, septiques"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("Prérequis", "La connaissance des techniques, l'adéquation des moyens de "
         "surveillance et le consentement éclairé du patient constituent les trois "
         "prérequis indispensables à la pratique d'une anesthésie périmédullaire (APM).", "A"),
        ("CI absolue", "Le refus du patient est une contre-indication absolue.", "A"),
        ("CI", "L'allergie documentée à l'un des agents injectés par voie intrathécale ou "
         "péridurale est une contre-indication.", "C"),
        ("CI absolue", "La lidocaïne est contre-indiquée de façon absolue par voie "
         "intrathécale.", "A"),
        ("CI", "Un patient non coopérant est une contre-indication (risque de lésion par "
         "l'aiguille et/ou le cathéter).", "C"),
        ("Non recommandé", "La réalisation d'une APM sous anesthésie générale n'est pas "
         "recommandée.", "C"),
        ("CI hémodynamique", "Une hypovolémie non corrigée et les situations où "
         "l'hémodynamique n'est pas stabilisée (état de choc, décompensation cardiaque) sont "
         "des contre-indications.", "C"),
        ("CI hémodynamique", "La chirurgie à haut risque hémorragique peropératoire doit "
         "faire préférer une technique anesthésique alternative.", "C"),
        ("Terrain à risque", "Chez le patient âgé ASA 3-4 en hypovolémie fréquente, si l'APM "
         "est choisie, préférer les techniques d'induction lente (rachianesthésie continue, "
         "anesthésie péridurale).", "C"),
        ("CI septique", "Une infection localisée à proximité du point de ponction et/ou une "
         "infection systémique documentée sont des contre-indications.", "C"),
        ("CI respiratoire", "Ne pas dépasser 0,3 mg de morphine intrathécale et mettre en "
         "place une surveillance clinique adéquate jusqu'à la 24e heure (dépression "
         "respiratoire).", "C"),
    ], RCW))
    return story

# ---------------------------------------------------------------------------
def _section_ci_hemostase():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Contre-indications liées à l'hémostase et aux anticoagulants/antiplaquettaires"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("Hémostase", "L'existence d'un trouble patent de l'hémostase est une "
         "contre-indication absolue. Le retrait d'un cathéter est une période à risque "
         "identique à la ponction.", "C"),
        ("Aspirine/AINS", "La prise d'aspirine ou d'AINS ne contre-indique pas l'APM si le "
         "bénéfice est jugé supérieur au risque exceptionnel d'hématome périmédullaire — à "
         "condition qu'aucun autre anticoagulant n'ait été reçu, qu'il n'existe pas "
         "d'anomalie associée de l'hémostase, de préférer la rachianesthésie en ponction "
         "unique, et d'assurer une surveillance neurologique postopératoire rigoureuse.", "C"),
        ("HBPM", "Avec les héparines de bas poids moléculaire, l'APM n'est pas "
         "contre-indiquée de façon absolue sous réserve de délais : 10-12h entre la dernière "
         "injection et l'APM/l'ablation du cathéter (dose unique quotidienne) ou 24h (deux "
         "doses/jour) ; 4-12h entre l'APM/l'ablation et la reprise des HBPM ; 24h avant la "
         "première dose en cas de ponction traumatique ou de difficultés techniques.", "AE"),
        ("HNF", "Avec l'héparine non fractionnée, l'APM n'est pas absolument contre-indiquée "
         "sous réserve de délais (Tableau 1) entre l'arrêt de l'héparine et l'APM/l'ablation "
         "du cathéter, entre l'APM et la reprise de l'héparinothérapie, et en cas de "
         "ponction traumatique.", "AE"),
        ("Anti-Xa nouvelle gén.", "En l'absence de recul suffisant, l'APM n'est pas "
         "recommandée sous prophylaxie par fondaparinux ou danaparoïde.", "AE"),
        ("AVK", "Avec les antivitamines K, l'APM n'est pas contre-indiquée de manière "
         "absolue à condition d'antagoniser ou d'arrêter suffisamment à l'avance le "
         "traitement et de vérifier un INR ≤ 1,5 avant ponction.", "AE"),
        ("Thiénopyridines", "Les APM sont contre-indiquées avec les traitements par "
         "thiénopyridines (ticlopidine, clopidogrel).", "AE"),
        ("Anti-GPIIb/IIIa", "La prise d'antagonistes des glycoprotéines IIb/IIIa (abciximab, "
         "eptifibatide, tirofiban) contre-indique toute APM ; en l'absence de données "
         "spécifiques, il est prudent d'éviter l'APM avant le délai de retour à la normale "
         "des fonctions plaquettaires (8h pour eptifibatide/tirofiban, 24-48h pour "
         "l'abciximab).", "C"),
        ("Inhib. thrombine", "Le risque d'hématome périmédullaire avec les inhibiteurs "
         "directs de la thrombine (hirudine) est inconnu — le risque potentiel et l'absence "
         "d'antidote contre-indiquent l'APM.", "AE"),
        ("Fibrinolytiques", "Les APM sont contre-indiquées en cas d'utilisation préopératoire "
         "de fibrinolytiques, ou lorsque leur utilisation péri/postopératoire est probable.", "C"),
    ], RCW))
    story.append(Spacer(1, 2 * mm))
    story.append(conversion_table(
        ["Héparine non fractionnée", "Voie sous-cutanée", "Voie intraveineuse"],
        [
            ["Délai arrêt héparine → APM/ablation cathéter", "12 h (raccourci possible sous contrôle TCA)", "4 h"],
            ["Délai APM → héparinothérapie", "6 à 8 h", "6 à 8 h"],
            ["Délai héparinothérapie → ponction traumatique", "?", "> 8 h"],
        ], [70 * mm, 55 * mm, CW_FULL - 125 * mm]))
    story.append(Spacer(1, 1 * mm))
    story.append(P("<i>Tableau 1 — Délais de réalisation d'une APM et héparinothérapie.</i>", S_NOTE))
    return story

# ---------------------------------------------------------------------------
def _section_ci_terrain_rachis_sources():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Contre-indications selon le terrain (cardiovasculaire, respiratoire, neurologique)"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("Cardiovasculaire", "L'insuffisant cardiaque : l'APM est contre-indiquée si la "
         "chirurgie nécessite un bloc étendu ; l'HTA non contrôlée et la péricardite "
         "constrictive sont des contre-indications.", "C"),
        ("Cardiovasculaire", "Les obstacles à l'éjection (rétrécissement mitral ou aortique "
         "serré, cardiomyopathie hypertrophique obstructive) sont des contre-indications.", "C"),
        ("Cardiovasculaire", "L'insuffisance mitrale ou aortique n'est pas une "
         "contre-indication si l'hypotension artérielle est rapidement traitée (remplissage "
         "et/ou vasoconstricteurs). La pathologie coronaire n'est pas une contre-indication.", "C"),
        ("Respiratoire", "Chez l'insuffisant respiratoire chronique, la rachianesthésie n'est "
         "théoriquement pas contre-indiquée si le bloc moteur ne dépasse pas T10.", "C"),
        ("Respiratoire", "L'APD thoracique aux anesthésiques locaux n'est pas contre-indiquée "
         "chez le BPCO sévère.", "C"),
        ("Neurologique", "L'hypertension intracrânienne est une contre-indication absolue. En "
         "urgence pour traumatologie des membres inférieurs avec traumatisme crânien récent, "
         "privilégier une technique de bloc périphérique.", "AE"),
        ("Neurologique", "Face à une pathologie neurologique chronique, la décision repose "
         "sur l'évaluation du rapport bénéfice/risque. La syringomyélie est une "
         "contre-indication à la rachianesthésie.", "C"),
        ("Neurologique", "Une épilepsie équilibrée n'est pas une contre-indication.", "C"),
        ("Neurologique", "Lors d'une sclérose en plaques, l'indication est individualisée ; "
         "préférer l'APD à la rachianesthésie (neurotoxicité potentielle des anesthésiques "
         "locaux).", "C"),
        ("Neurologique", "Le syndrome de Guillain-Barré et les neuropathies démyélinisantes "
         "non stabilisées (poussée ou récupération) contre-indiquent l'APM.", "C"),
        ("Neurologique", "Les antécédents céphalalgiques, migraineux ou de lombalgies ne sont "
         "pas des contre-indications absolues ; un canal lombaire étroit invite à la "
         "prudence pour la rachianesthésie.", "C"),
    ], RCW))
    story.append(Spacer(1, 1.5 * mm))
    story.append(context_note_local(
        "un bilan IRM est recommandé avant une APM chez un patient présentant une spina "
        "bifida identifiée."))
    story.append(Spacer(1, 3 * mm))
    story.append(KeepTogether([
        section_bar("Anomalies rachidiennes, matériel d'ostéosynthèse, antécédent de blood-patch"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("Matériel rachidien", "La présence de matériel d'ostéosynthèse rachidien n'est pas "
         "une contre-indication absolue, mais rend souvent nécessaires plusieurs ponctions à "
         "différents niveaux.", "C"),
        ("Chirurgie rachidienne", "Le risque de brèche durale est augmenté lors d'anesthésie "
         "péridurale en cas d'antécédent de chirurgie rachidienne.", "C"),
        ("Chirurgie rachidienne", "La diffusion de l'anesthésique local peut être anormale, "
         "avec un risque plus important par voie péridurale que par voie intrathécale.", "C"),
        ("Chirurgie rachidienne", "Une technique de titration est appropriée en cas de "
         "déformation rachidienne importante.", "C"),
        ("Chirurgie rachidienne", "Le repérage de la ligne médiane peut être facilité par "
         "l'échographie ; une ponction en dehors de la zone de fusion rachidienne est "
         "préférable.", "C"),
        ("Blood-patch", "Un antécédent de blood-patch ne contre-indique pas la "
         "rachianesthésie ; le risque d'extension insuffisante de l'anesthésie paraît plus "
         "élevé en péridurale.", "C"),
    ], RCW))
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("Sources et avertissement", color=GREY))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>Document source :</b> SFAR/Sofcot/Sofmer, « Les blocs périmédullaires chez "
        "l'adulte », Recommandations pour la Pratique Clinique, présentées le 24 septembre "
        "2005 (47e congrès SFAR), Annales Françaises d'Anesthésie et de Réanimation 26 "
        "(2007) 720-752.", S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>URL source :</b> https://sfar.org/les-blocs-perimedullaires-chez-ladulte/", S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>Couverture :</b> Questions 1-2/15 uniquement (information au patient ; "
        "contre-indications générales, surveillance et monitorage) — 41 recommandations "
        "gradées (A:3, C:31, AE:7). Les Questions 3 à 15 (technique rachianesthésie/"
        "péridurale, association AG-bloc, obstétrique, analgésie postopératoire, terrains "
        "spécifiques, échec, facteurs de risque de complications) ne sont pas couvertes ici "
        "— hors périmètre de cette fiche, disclosed en page 1, installments futurs. "
        "Argumentaire scientifique détaillé (document source complet) non reproduit.", S_SOURCE))
    story.append(Spacer(1, 2 * mm))
    story.append(info_panel(P(
        "<b>Avertissement :</b> cette fiche est une synthèse indépendante et PARTIELLE "
        "(Questions 1-2 uniquement, sur 15). Elle ne remplace pas le texte intégral — en "
        "particulier pour toute question de technique, d'obstétrique ou de terrain "
        "spécifique. Cette fiche n'est ni éditée ni validée par la SFAR.", S_BODY_SM),
        bg=GREY_LIGHT, border=GREY))
    return story

# ---------------------------------------------------------------------------
def _section_info_ci_neuro_hemo_septique():
    story = _section_intro_information()
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_ci_neuro_hemodynamique_septique())
    return story

def _section_hemostase_terrain_sources():
    story = _section_ci_hemostase()
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_ci_terrain_rachis_sources())
    return story

SECTIONS = [
    ("Information au patient & CI neurologiques/hémodynamiques/septiques", _section_info_ci_neuro_hemo_septique),
    ("CI hémostase/anticoagulants, terrain & sources", _section_hemostase_terrain_sources),
]

def _make_doc(path=None):
    return SimpleDocTemplate(path or OUT, pagesize=A4,
                              leftMargin=MARGIN, rightMargin=MARGIN,
                              topMargin=32 * mm, bottomMargin=16 * mm,
                              title="Fiche SFAR 2007 - Blocs perimedullaires (Q1-2 - Information et CI)",
                              author="Synthèse indépendante (source SFAR/Sofcot/Sofmer)")

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
