# -*- coding: utf-8 -*-
"""
Fiche de synthese - "Les blocs perimedullaires chez l'adulte" - Question 8
(Analgesie postoperatoire par voie perimedullaire : agents, indications,
monitorage/surveillance) - Recommandations pour la Pratique Clinique (RPC),
SFAR/Sofcot/Sofmer, presentees le 24 septembre 2005 (47e congres SFAR),
publiees Ann Fr Anesth Reanim 26 (2007) 720-752.

QUATRIEME INSTALLMENT de ce document (voir `fiche_blocs_perimedullaires_ci_2006.py`
pour Q1-2, `fiche_blocs_perimedullaires_technique_2006.py` pour Q3-5,
`fiche_blocs_perimedullaires_cesarienne_2006.py` pour Q7). Perimetre
volontairement limite (meme pattern) : 369 citations de grade sur 15
"Questions" au total dans le document source complet. Question 6 (travail
obstetrical) reste EXCLUE (superseded par `douleur_accouchement_2025`, HAS
2025 - decision documentee dans l'installment Q7, non reexaminee ici). Les
Questions 9 a 15 (terrains cardiovasculaire/respiratoire/neurologique/
infectieux specifiques, gestion de l'echec, facteurs de risque de
complications) restent hors perimetre - installments futurs.

PERIMETRE EXACT DE CETTE FICHE : Question 8 du document source ("Analgesie
postoperatoire" - agents de l'analgesie perimedullaire postoperatoire,
indications par type de chirurgie, monitorage et modalites de surveillance),
lignes 1766-2198 du fichier texte extrait (`sources/blocs_perimedullaires_ci_2006.txt`).
Cette Question 8 n'a PAS de titre en lettres capitales unique - elle est
introduite par le bandeau "ANALGESIE POSTOPERATOIRE" suivi directement du
sous-titre "QUELS SONT LES AGENTS DE L'ANALGESIE POSTOPERATOIRE PAR VOIE
PERIMEDULLAIRE ?" (particularite deja signalee par le pipeline de commande de
cette fiche, verifiee ici par lecture directe du texte).

METHODOLOGIE : grille EBM classique A/B/C (ANAES avril 2004), identique aux
trois installments precedents. VERIFICATION EXPLICITE DEMANDEE (grade D,
"avis d'experts", "consensus professionnel") : un grep exhaustif sur les
lignes 1766-2198 ne trouve AUCUNE occurrence de "grade D" ni "avis
d'experts" ni "accord professionnel" - seulement A/B/C (71 citations) et UNE
occurrence de "consensus professionnel", mais celle-ci n'est PAS attachee a
une recommandation individuelle : elle figure dans la phrase d'ouverture de
la sous-section Monitorage ("Les recommandations reposent sur la
reglementation, d'une part, et sur un consensus professionnel, d'autre
part"), comme justification methodologique GLOBALE de tout ce sous-bloc, pas
comme citation ponctuelle greffee a une phrase precise (a la difference des
"accord professionnel"/"avis d'experts"/"consensus professionnel" ponctuels
deja rencontres et chippes "AE" dans les Questions 1-2/3-5/7). DISCLOSURE
(regle 4/5) : ce sous-bloc Monitorage n'est donc PAS retranscrit en lignes de
reco_table avec un chip "AE" invente pour chaque item (ce qui fabriquerait un
grade que le source n'attribue a aucune phrase individuelle) - il est
presente integralement comme reperes pratiques non gradees, avec la citation
"consensus professionnel" disclosed explicitement dans le texte de la fiche
elle-meme. Consequence : ni le chip "D" (NAVY, utilise dans l'installment
Q7) ni le chip "AE" (GREY) ne sont utilises dans cette fiche - seuls A/B/C
apparaissent, disclosed dans la legende.

DECOMPTE (verifie par regex sur le script final, pas seulement estime a la
lecture) : grep exhaustif sur le texte source de la Question 8 (lignes
1766-2198) trouve 71 citations de grade individuelles : grade A x28, grade B
x17, grade C x26, grade D x0. Deux citations de MEME grade decrivant le MEME
point clinique dans une seule phrase source sont regroupees en une seule
ligne (jamais deux grades DIFFERENTS fusionnes dans une seule ligne - verifie
par le safety net regex apres redaction, aucune occurrence trouvee) ; a la
relecture de cette Question 8, chaque citation (grade X) individuelle
correspond en pratique a un point clinique distinct (molecule, type de
chirurgie ou parametre different) - AUCUNE consolidation n'a donc ete
appliquee, chacune des 71 citations devient sa propre ligne de tableau.
Repartition : sous-section "Agents" (anesthesiques locaux, opiaces, agents
alpha2-adrenergiques, ketamine) - 20 lignes (A:13, B:4, C:3) ; sous-section
"Indications par type de chirurgie" (prerequis APD, thoracotomie, chirurgie
cardiaque, oesophage, chirurgie intra-abdominale/thoraco-abdominale majeure,
urologie, gynecologie, aorte abdominale, chirurgie vasculaire peripherique,
amputation de membre, arthroplastie du genou) - 51 lignes (A:15, B:13, C:23) ;
sous-section "Monitorage et surveillance" - 0 ligne gradee individuelle (voir
disclosure ci-dessus), contenu integralement condense en reperes pratiques
non gradees (reglementation, role infirmier, frequence de surveillance,
criteres cliniques, feuilles de surveillance). TOTAL : 71 recommandations
gradees (A:28, B:17, C:26) sur les 3 sous-sections de cette Question 8. Ce
tally a ete verifie par :
    python3 -c "import re; from collections import Counter; src=open('fiche_blocs_perimedullaires_postop_2006.py',encoding='utf-8').read(); print(Counter(re.findall(r'\"(A|B|C|D|AE)\"\\),', src)))"
avant finalisation - voir le paragraphe "Couverture" en fin de fiche pour les
chiffres retenus, identiques a ce tally.

CONTENU NON GRADE (regle 7, argumentaire minimal) : la narration purement
descriptive (mecanismes d'action non chiffres, doses recommandees non
graduees individuellement, la sous-section hepatectomie qui ne comporte
aucune citation (grade X) propre, le paragraphe PTH qui n'en comporte pas non
plus, et le paragraphe de synthese "Au total") est condensee en blocs
"Reperes pratiques non grades" (bullets courts, 1-2 phrases), jamais
retranscrite in extenso - conformement a la regle 7 de ce depot.

AUCUN TABLEAU NI FIGURE dans le perimetre de cette fiche (verifie par grep
"tableau|figure|fig\\." sur les lignes 1766-2198 : zero occurrence) - a la
difference des installments Q3-5 (3 tableaux pharmacologiques) et Q7 (1
figure/algorithme decisionnel), cette Question 8 est purement narrative avec
citations de grade inline. Aucun rendu PDF a 150-200dpi n'a donc ete
necessaire ici.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from style import *
GRADE_COLORS["A"] = (GREEN, WHITE)
GRADE_COLORS["B"] = (TEAL, WHITE)
GRADE_COLORS["C"] = (AMBER, WHITE)
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.units import mm

OUT = "/home/user/rfe-sfar-website/output/Fiche_Blocs_Perimedullaires_Postop_2006.pdf"

SOURCE_TXT = ("Source : SFAR/Sofcot/Sofmer, « Les blocs périmédullaires chez l'adulte », "
              "RPC, Ann Fr Anesth Réanim 26 (2007) 720-752 — Question 8 uniquement. "
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

RCW = [32 * mm, CW_FULL - 32 * mm - 15 * mm, 15 * mm]

def context_note_local(txt):
    return P(f"<i>Précision du source :</i> {txt}", S_NOTE)

def practical_block(title, bullets):
    story = [P(f"<b>{title}</b>", S_BODY_SM)]
    for b in bullets:
        story.append(P(f"• {b}", S_BODY_SM))
    return story

def subhead(txt):
    return P(f"<b>{txt}</b>", S_BODY)

def legend_flowable():
    chip_w = 16 * mm
    content_w = CW_FULL
    row = Table([[chip("A", width=chip_w - 2 * mm), chip("B", width=chip_w - 2 * mm),
                  chip("C", width=chip_w - 2 * mm),
                  P("<b>Grille EBM classique</b> — <b>A</b> : essais randomisés de forte "
                    "puissance/méta-analyses ; <b>B</b> : essais randomisés de faible "
                    "puissance/études de cohorte ; <b>C</b> : cas-témoins/études "
                    "rétrospectives. Aucune citation « grade D », « accord professionnel » "
                    "ou « avis d'experts » ponctuelle dans le périmètre de cette fiche "
                    "(disclosed en page 1) — chips « D »/« AE » donc absents ici. Fiche "
                    "limitée à la Question 8/15 du document (analgésie postopératoire "
                    "périmédullaire : agents, indications, monitorage).", S_BADGE_HEAD)]],
                colWidths=[chip_w] * 3 + [content_w - 3 * chip_w])
    row.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                              ("LEFTPADDING", (0, 0), (-1, -1), 1),
                              ("RIGHTPADDING", (0, 0), (-1, -1), 1),
                              ("TOPPADDING", (0, 0), (-1, -1), 0),
                              ("BOTTOMPADDING", (0, 0), (-1, -1), 0)]))
    return row

TOTAL_PAGES = {"n": 6}

def on_page(canvas, doc, page_title):
    header_band(canvas, doc, "SFAR/SOFCOT/SOFMER — RPC 2007 (Q8/15 — PÉRIMÈTRE LIMITÉ)",
                "Les blocs périmédullaires chez l'adulte",
                page_title, icon_fn=lambda c, x, y: icon_shield(c, x, y, 13 * mm), color=TEAL_DARK)
    footer_band(canvas, doc, SOURCE_TXT, f"Page {doc.page} / {TOTAL_PAGES['n']}")

# ---------------------------------------------------------------------------
def _section_agents():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Périmètre limité — installment 4/n :</b> ce document source compte 15 « Questions » "
        "cliniques et 369 citations de grade au total. Cette fiche couvre INTÉGRALEMENT la "
        "Question 8 (analgésie postopératoire par voie périmédullaire : agents, indications, "
        "monitorage/surveillance). La Question 6 (travail obstétrical) reste EXCLUE — superseded "
        "par une fiche séparée plus récente (HAS 2025, « Douleur de l'accouchement »). Les "
        "Questions 1-2, 3-5 et 7 sont couvertes par des fiches séparées. Les Questions 9 à 15 "
        "(terrains cardiovasculaire/respiratoire/neurologique/infectieux spécifiques, gestion de "
        "l'échec, facteurs de risque de complications) ne sont PAS couvertes ici — installments "
        "futurs.", S_BODY),
        bg=AMBER_LIGHT, border=AMBER))
    story.append(Spacer(1, 2.5 * mm))
    story.append(legend_flowable())
    story.append(Spacer(1, 3 * mm))
    story.append(KeepTogether([
        section_bar("Question 8 — Agents de l'analgésie postopératoire périmédullaire"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(context_note_local(
        "après injection péridurale, environ 10 % de l'AL traverse la dure-mère (absorption "
        "dans la graisse périmédullaire, résorption vasculaire, diffusion par les trous de "
        "conjugaison)."))
    story.append(Spacer(1, 1.5 * mm))
    story.append(subhead("Anesthésiques locaux"))
    story.append(Spacer(1, 1 * mm))
    story.append(reco_table([
        ("AL — Lidocaïne", "Contre-indiquée par voie intrathécale : neurotoxicité (syndrome de "
         "la queue-de-cheval, syndrome d'irritation radiculaire transitoire), retirée du marché "
         "dans cette indication.", "A"),
        ("AL — Alternatives", "De nombreuses alternatives à la lidocaïne existent, pour une "
         "même efficacité clinique.", "A"),
        ("AL — Bupivacaïne", "Molécule la plus cardiotoxique expérimentalement parmi les AL "
         "(mélange racémique).", "A"),
        ("AL — Bupivacaïne IT", "ED95 intrathécale ≈ 0,06 mg/cm de taille ; en deçà, associer "
         "un adjuvant (morphinique).", "A"),
        ("AL — Bupivacaïne péri.", "MLAC péridurale 0,048–0,067 %, majorée à 0,140 % en fin de "
         "travail/dystocie obstétricale.", "A"),
        ("AL — Ropivacaïne", "AL de longue durée d'action, expérimentalement le moins "
         "cardiotoxique.", "A"),
        ("AL — Lévobupivacaïne", "Cardiotoxicité intermédiaire entre bupivacaïne et "
         "ropivacaïne.", "A"),
        ("AL — Associations", "Résultats cliniques intermédiaires (inférieurs à la molécule la "
         "plus puissante), avec risque d'additivité voire de synergie de toxicité.", "C"),
    ], RCW))
    story.append(Spacer(1, 2.5 * mm))
    story.append(subhead("Opiacés"))
    story.append(Spacer(1, 1 * mm))
    story.append(reco_table([
        ("Opiacés", "Action analgésique synergique des opioïdes et des AL, par voie "
         "intrathécale et péridurale.", "A"),
        ("Opiacés", "Cette synergie permet de réduire la concentration minimale efficace des "
         "AL (MLAC).", "B"),
        ("Morphine", "Action spinale spécifique, temps de résidence prolongé dans le LCR.", "A"),
        ("Morphine", "Analgésie de 10-12h (jusqu'à 24h), délai d'action plus long que les "
         "opioïdes liposolubles.", "A"),
        ("Opioïdes liposolubles", "Action principalement systémique ; une action segmentaire "
         "(ganglions rachidiens) ne peut être exclue.", "B"),
        ("Opioïdes liposolubles", "Action segmentaire spinale préférentielle en administration "
         "en bolus, systémique en administration continue.", "C"),
        ("Opioïdes liposolubles", "Délai d'action plus rapide et durée d'action plus courte que "
         "la morphine.", "A"),
        ("Association triple", "Morphine + opioïde liposoluble + AL : réduit la dose de chacun "
         "tout en gardant leur bénéfice respectif.", "C"),
        ("Sécurité opiacés", "Pic du risque de dépression respiratoire : 6e heure (jusqu'à 24h) "
         "pour la morphine, contre 20 min (durée 6-8h) pour fentanyl/sufentanil.", "B"),
    ], RCW))
    story.append(Spacer(1, 1.5 * mm))
    story.extend(practical_block("Repères pratiques non gradés (doses) :", [
        "Morphine : 1-4 mg en péridural, 100-300 µg en intrathécal (doses réduites chez le "
        "sujet âgé : ne pas dépasser 200 µg intrathécal / 3 mg péridural).",
        "Fentanyl intrathécal 10 (5-25) µg, sufentanil intrathécal 5 (5-10) µg ; péridural : "
        "fentanyl 2 (2-20) µg/ml, sufentanil 0,5 (0,25-0,75) µg/ml.",
        "Effets secondaires dose-dépendants : nausées/vomissements plus fréquents avec la "
        "morphine ; prurit plus fréquent par voie intrathécale (ne limite généralement pas "
        "l'utilisation) ; la dépression respiratoire (cf. tableau) reste le facteur limitant "
        "principal.",
    ]))
    story.append(Spacer(1, 2.5 * mm))
    story.append(subhead("Agents agonistes alpha2-adrénergiques et kétamine"))
    story.append(Spacer(1, 1 * mm))
    story.append(reco_table([
        ("Adrénaline", "À des concentrations ≥ 1,5 µg/ml, diminue le délai d'installation du "
         "bloc après administration intrathécale d'AL.", "B"),
        ("Clonidine", "Absence de neurotoxicité : en fait un complément de choix des "
         "morphiniques.", "A"),
        ("Kétamine", "Contre-indiquée par voie périmédullaire : neurotoxicité du chlorobutanol "
         "(conservateur) ; une solution sans conservateur pourrait être envisagée mais le recul "
         "clinique est insuffisant.", "A"),
    ], RCW))
    story.append(Spacer(1, 1.5 * mm))
    story.extend(practical_block("Repères pratiques non gradés :", [
        "Clonidine : prolonge les blocs sensitif et moteur des AL et permet des doses d'AL plus "
        "faibles ; effets secondaires (hypotension, bradycardie, somnolence) dose-dépendants, "
        "limitant les doses à 15-75 µg intrathécal et 4-5 µg/ml péridural.",
    ]))
    return story

# ---------------------------------------------------------------------------
def _section_indications():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Question 8 — Indications de l'analgésie périmédullaire postopératoire"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(P(
        "<b>Repères non gradés :</b> l'analgésie péridurale (APD), de qualité et fiabilité "
        "supérieures, est la référence à laquelle les autres techniques d'analgésie aspirent — "
        "supérieure à l'analgésie parentérale pour quasiment tous les types de chirurgie. La "
        "rachianalgésie est plus limitée dans le temps et par les médicaments utilisables. Les "
        "indications ci-dessous sont établies par type de chirurgie, en tenant compte de la "
        "qualité d'analgésie, des bénéfices attendus et des risques de chaque technique.", S_BODY_SM))
    story.append(Spacer(1, 1.5 * mm))
    story.append(subhead("Prérequis pour une analgésie péridurale postopératoire"))
    story.append(Spacer(1, 1 * mm))
    story.append(reco_table([
        ("Prérequis APD", "Chirurgie abdominale/thoracique : associer un AL à faible "
         "concentration à un morphinique pour une analgésie supérieure aux autres techniques.", "A"),
        ("Prérequis APD", "Cathéter inséré au milieu de la zone des dermatomes à bloquer, le "
         "plus souvent au niveau thoracique.", "B"),
        ("Prérequis APD", "Administration des médicaments adaptée au mieux par le patient "
         "lui-même (PCA).", "C"),
    ], RCW))
    story.append(Spacer(1, 2.5 * mm))
    story.append(subhead("Chirurgie thoracique et cardiaque"))
    story.append(Spacer(1, 1 * mm))
    story.append(reco_table([
        ("Thoracotomie", "L'APD thoracique aux AL, plus ou moins associée à un morphinique, "
         "est la technique la plus efficace.", "A"),
        ("Thoracotomie", "Bloc paravertébral vs APD thoracique comparés par 2 études aux "
         "résultats discordants (l'une favorable au paravertébral avec moins d'effets "
         "secondaires, l'autre favorable à l'APD sur les 24 premières heures).", "B"),
        ("Thoracotomie", "Fonction respiratoire améliorée et complications pulmonaires "
         "diminuées par l'APD (AL et/ou morphinique).", "A"),
        ("Thoracotomie", "Diminution de l'incidence des troubles du rythme cardiaque.", "C"),
        ("Thoracotomie", "Diminution de l'incidence des douleurs chroniques "
         "post-thoracotomie.", "C"),
        ("Chir. cardiaque", "Analgésie périmédullaire d'excellente qualité, supérieure à la "
         "voie parentérale (durée plus limitée pour la voie rachidienne).", "A"),
        ("Chir. cardiaque", "Seule l'APD (pas la rachianalgésie) diminue la morbidité "
         "postopératoire.", "B"),
        ("Chir. cardiaque", "Diminution de la réaction de stress chirurgical.", "C"),
        ("Chir. cardiaque", "Diminution de l'incidence des troubles du rythme cardiaque.", "B"),
        ("Chir. cardiaque", "Diminution des complications respiratoires.", "B"),
        ("Chir. cardiaque", "Diminution des complications neurologiques.", "B"),
        ("Chir. cardiaque", "Diminution de la durée de ventilation postopératoire.", "B"),
    ], RCW))
    story.append(Spacer(1, 2.5 * mm))
    story.append(subhead("Chirurgie de l'œsophage et chirurgie abdominale majeure"))
    story.append(Spacer(1, 1 * mm))
    story.append(reco_table([
        ("Chir. œsophage", "L'APD diminue la douleur postopératoire.", "A"),
        ("Chir. œsophage", "Diminution de la réaction de stress chirurgical.", "C"),
        ("Chir. œsophage", "Diminution de l'incidence des complications respiratoires.", "B"),
        ("Chir. œsophage", "Réduction de la durée de ventilation postopératoire.", "C"),
        ("Chir. œsophage", "Réduction de la durée totale d'hospitalisation.", "C"),
        ("Abdo. majeure", "Association péridurale AL + morphinique : analgésie supérieure à la "
         "morphine péridurale seule, elle-même ≥ morphine parentérale.", "A"),
        ("Abdo. majeure", "Cette association réduit les scores de douleur d'≈15 mm sur les 48 "
         "premières heures, comparée à la morphine parentérale.", "A"),
        ("Abdo. majeure", "Morphine intrathécale : analgésie d'excellente qualité mais de "
         "durée moindre (≈20h sans réinjection).", "C"),
        ("Abdo. majeure", "AL péridurale (blocage sympathique) : glycémie et tolérance aux "
         "sucres normalisées.", "C"),
        ("Abdo. majeure", "Catabolisme et consommation d'O2 diminués, bilan azoté positivé.", "C"),
        ("Abdo. majeure", "Taux de cortisol/catécholamines/aldostérone/rénine/ADH diminués ; "
         "effet sur la fonction rénale minime.", "C"),
        ("Abdo. majeure", "APD (AL ou morphinique) : diminution des épisodes d'ischémie "
         "myocardique et des troubles du rythme, vs voie parentérale.", "C"),
        ("Abdo./thoracique", "Incidence des complications thromboemboliques NON diminuée par "
         "l'APD.", "B"),
        ("Abdo. majeure", "Oxygénation artérielle améliorée par l'APD.", "A"),
        ("Abdo. majeure", "Mécanique respiratoire améliorée par l'APD.", "C"),
        ("Thoraco-abdo majeure", "Diminution de l'incidence des complications respiratoires "
         "graves.", "A"),
        ("Thoraco-abdo majeure", "Extubation plus précoce.", "B"),
        ("Abdo. majeure", "Ponction lombaire : reprise du transit NON accélérée par l'APD.", "C"),
        ("Abdo. majeure", "Ponction thoracique (AL + morphinique ≥ 48h) : accélère la reprise "
         "du transit.", "A"),
        ("Abdo. majeure", "Statut neurologique postopératoire potentiellement amélioré.", "B"),
    ], RCW))
    story.append(Spacer(1, 1.5 * mm))
    story.extend(practical_block("Repères pratiques non gradés — hépatectomie :", [
        "Bénéfices superposables à ceux de la chirurgie digestive majeure (plusieurs études "
        "incluent des hépatectomies) ; particularité : risque de troubles de l'hémostase "
        "postopératoire, dont découlent les précautions de gestion du cathéter péridural.",
    ]))
    story.append(Spacer(1, 2.5 * mm))
    story.append(subhead("Urologie, gynécologie, chirurgie de l'aorte et vasculaire périphérique"))
    story.append(Spacer(1, 1 * mm))
    story.append(reco_table([
        ("Urologie", "Chirurgie vésicale transpéritonéale : réduction de l'iléus "
         "postopératoire, moindre fatigue, déambulation plus rapide.", "B"),
        ("Gynécologie", "Prolongation postopératoire de l'APD : analgésie de meilleure qualité "
         "que par voie systémique (hystérectomie).", "C"),
        ("Aorte abdominale", "APD utile pour l'analgésie.", "A"),
        ("Aorte abdominale", "Réduction de l'incidence des complications respiratoires.", "A"),
        ("Aorte abdominale", "Réduction de la durée de ventilation.", "A"),
        ("Aorte abdominale", "Pas d'impact sur les complications cardiovasculaires.", "A"),
        ("Aorte abdominale", "Risque de complications à type d'hématome péridural.", "C"),
        ("Vascul. périphérique", "Pas d'impact sur la mortalité ni sur les complications "
         "cardiaques et respiratoires.", "B"),
        ("Vascul. périphérique", "Effet protecteur sur la thrombose du greffon.", "A"),
        ("Vascul. périphérique", "Utilisation peropératoire jugée inutile.", "C"),
    ], RCW))
    story.append(Spacer(1, 1.5 * mm))
    story.extend(practical_block("Repères pratiques non gradés :", [
        "Urologie (prostatectomie) : effet analgésique préventif peropératoire possible ; pas "
        "de preuve d'effet sur la morbi-mortalité ; indication postopératoire non clairement "
        "établie après prostatectomie, mais potentiellement indiquée pour la chirurgie "
        "transpéritonéale (ex. cystectomie).",
        "Gynécologie (hystérectomie) : effet préventif peropératoire d'intérêt très limité ; "
        "pas de preuve d'effet sur la morbi-mortalité ; rachianalgésie à faible dose de "
        "morphine (< 0,1 mg) possible.",
        "Chirurgie de l'aorte : le cathéter doit être posé en préopératoire (anticoagulation "
        "peropératoire) — son utilisation peropératoire n'est pas utile.",
    ]))
    story.append(Spacer(1, 2.5 * mm))
    story.append(subhead("Amputation de membre et chirurgie orthopédique"))
    story.append(Spacer(1, 1 * mm))
    story.extend(practical_block("Repères pratiques non gradés — arthroplastie totale de hanche (PTH) :", [
        "Utilisation peropératoire réduirait le saignement et la thrombose veineuse (efficacité "
        "inférieure aux HBPM) ; impact sur la morbi-mortalité controversé ; en postopératoire, "
        "la poursuite de l'APD améliore l'analgésie sans améliorer la convalescence et expose à "
        "un risque de rétention urinaire, d'hypotension et de problèmes techniques.",
        "L'APD postopératoire N'EST PAS indiquée après PTH (faible niveau de douleur, faible "
        "rentabilité sur la convalescence) ; une rachianesthésie à faible dose de morphine "
        "(0,1 mg) est parfois proposée mais sa tolérance est médiocre (risque de dépression "
        "respiratoire).",
    ]))
    story.append(Spacer(1, 1.5 * mm))
    story.append(reco_table([
        ("Amputation membre", "APD utile pour l'analgésie postopératoire immédiate.", "C"),
        ("Amputation membre", "Incertitude sur la prévention des douleurs de membre "
         "fantôme.", "C"),
        ("Amputation membre", "Utilisation pré- et peropératoire souhaitable.", "C"),
        ("Arthroplastie genou", "APD postopératoire immédiate utile.", "C"),
        ("Arthroplastie genou", "Rééducation plus efficace, durée de séjour réduite.", "C"),
        ("Arthroplastie genou", "Utilisation peropératoire souhaitable pour limiter la "
         "thrombose.", "C"),
    ], RCW))
    story.append(Spacer(1, 1.5 * mm))
    story.extend(practical_block("Repères pratiques non gradés :", [
        "Genou : indications restent limitées par les effets secondaires ; le bloc fémoral est "
        "plus facile et tout aussi efficace ; la rachianalgésie est une alternative moins "
        "intéressante.",
        "Au total : l'APD bien conduite (respect des contre-indications, niveau de ponction "
        "adéquat, association AL + morphinique, adaptation des doses) procure une excellente "
        "analgésie au repos et à la mobilisation, supérieure aux autres techniques d'analgésie "
        "postopératoire — sauf blocs périphériques en orthopédie et bloc paravertébral en "
        "chirurgie thoracique. Elle doit s'intégrer dans un programme multimodal de "
        "réadaptation accélérée.",
    ]))
    return story

# ---------------------------------------------------------------------------
def _section_monitoring_sources():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Question 8 — Monitorage et modalités de surveillance postopératoire"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(info_panel(P(
        "<b>Disclosure méthodologique :</b> à la différence des deux sous-sections "
        "précédentes, cette sous-section ne comporte AUCUNE citation (grade X) individuelle "
        "dans le texte source. Le texte source l'introduit ainsi : « Les recommandations "
        "reposent sur la réglementation, d'une part, et sur un consensus professionnel, "
        "d'autre part » — une justification méthodologique globale, non rattachée à une "
        "phrase précise. Elle n'est donc pas retranscrite en lignes de tableau gradées "
        "(ce qui fabriquerait artificiellement un chip que le source n'attribue à aucun item), "
        "mais intégralement condensée en repères pratiques non gradés ci-dessous.", S_BODY_SM),
        bg=GREY_LIGHT, border=GREY))
    story.append(Spacer(1, 2 * mm))
    story.extend(practical_block("Cadre réglementaire :", [
        "Décret 95-100 du 6 septembre 1995 : le médecin doit s'efforcer de soulager les "
        "souffrances de son malade et l'assister moralement.",
        "Article L. 1110-5 du code de la santé publique : toute personne a le droit de "
        "recevoir des soins visant à soulager sa douleur, qui doit être prévenue, évaluée, "
        "prise en compte et traitée en toute circonstance.",
        "Article L. 710-3-1 du code de la santé publique : chaque établissement de santé doit "
        "définir, dans son projet d'établissement, un programme d'actions pour améliorer la "
        "prise en charge de la douleur.",
        "Décret n° 2002-194 du 11 février 2002 (actes infirmiers) : l'infirmier(e) est habilité "
        "à entreprendre et adapter les traitements antalgiques dans le cadre de protocoles "
        "écrits/datés/signés par un médecin, et à injecter dans les cathéters périduraux ou "

        "intrathécaux posés par un médecin (après que celui-ci en ait fait la première "
        "injection), à condition qu'un médecin puisse intervenir à tout moment.",
    ]))
    story.append(Spacer(1, 1.5 * mm))
    story.extend(practical_block("Information du patient et cahier des charges :", [
        "Le patient doit être informé des objectifs et modalités de l'analgésie périmédullaire "
        "dès la consultation d'anesthésie ; le mode d'évaluation de la douleur (EVA, EVS) est "
        "adapté au patient.",
        "Le protocole d'analgésie postopératoire est préparé en consultation et débute en "
        "période peropératoire ; en fin d'intervention, la prescription est personnalisée, "
        "nominative, horodatée et paraphée par le médecin anesthésiste ; un protocole de "
        "service (technique, analgésiques/doses, surveillance, conduite à tenir en cas d'effet "
        "secondaire) peut compléter la prise en charge en service de chirurgie.",
    ]))
    story.append(Spacer(1, 1.5 * mm))
    story.extend(practical_block("Fréquence et contenu de la surveillance :", [
        "Surveillance régulière plusieurs fois par période de 24h ; rapprochée dans l'heure "
        "suivant l'installation ou un changement de dose, puis toutes les 2 à 4 heures selon le "
        "patient et le type de chirurgie ; basée sur une échelle de douleur (EVA/EVS) au repos "
        "et à la mobilisation.",
        "Critères cliniques prioritaires : score d'éveil/sédation et fréquence respiratoire "
        "(nécessitent une formation adaptée des équipes soignantes) ; évaluation des blocs "
        "sensitif et moteur (étendue, intensité) au moins une fois par équipe infirmière.",
        "Après injection intrathécale de morphine : surveillance rapprochée en soins continus "
        "ou soins intensifs pendant 24 heures, SAUF pour les patients ayant reçu une dose "
        "inférieure à 0,2 mg.",
        "Les feuilles de surveillance doivent comporter : niveaux d'analgésie (EVA/EVS, au "
        "repos et à la mobilisation) et de sédation, paramètres cardiovasculaires (pression "
        "artérielle, fréquence cardiaque) et ventilatoires (fréquence respiratoire), blocs "
        "sensitif et moteur (si APD analgésique), effets indésirables mineurs (nausées, "
        "vomissements, prurit, rétention urinaire) et complications mécaniques liées aux "
        "cathéters, consommation analgésique (PCA/PCEA), et les conduites à tenir en cas "
        "d'effet secondaire.",
    ]))
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
        "<b>Couverture :</b> Question 8/15 uniquement (analgésie postopératoire par voie "
        "périmédullaire : agents, indications, monitorage/surveillance) — 71 recommandations "
        "gradées (A:28, B:17, C:26). Aucune citation « grade D », « accord professionnel » ou "
        "« avis d'experts » ponctuelle dans le périmètre de cette Question (disclosed en page "
        "1) — la sous-section Monitorage repose sur une justification méthodologique globale "
        "(« réglementation » + « consensus professionnel »), non rattachée à une recommandation "
        "individuelle, et est donc intégralement condensée en repères pratiques non gradés "
        "plutôt qu'en lignes de tableau. La Question 6 (travail obstétrical) est EXCLUE — "
        "superseded par une fiche séparée plus récente (HAS 2025). Les Questions 1-2, 3-5 et 7 "
        "sont couvertes par des fiches séparées. Les Questions 9 à 15 (terrains spécifiques, "
        "échec, facteurs de risque de complications) ne sont pas couvertes ici — hors périmètre "
        "de cette fiche, installments futurs. Argumentaire scientifique détaillé (document "
        "source complet) non reproduit.", S_SOURCE))
    story.append(Spacer(1, 2 * mm))
    story.append(info_panel(P(
        "<b>Avertissement :</b> cette fiche est une synthèse indépendante et PARTIELLE "
        "(Question 8 uniquement, sur 15). Elle ne remplace pas le texte intégral — en "
        "particulier pour le travail obstétrical (voir la fiche HAS 2025 dédiée), les "
        "contre-indications générales, la technique de réalisation des blocs, la césarienne, "
        "ou tout terrain spécifique. Cette fiche n'est ni éditée ni validée par la SFAR.", S_BODY_SM),
        bg=GREY_LIGHT, border=GREY))
    return story

# ---------------------------------------------------------------------------
SECTIONS = [
    ("Question 8 — Agents de l'analgésie postopératoire périmédullaire", _section_agents),
    ("Question 8 — Indications de l'analgésie périmédullaire postopératoire", _section_indications),
    ("Question 8 — Monitorage, surveillance & sources", _section_monitoring_sources),
]

def _make_doc(path=None):
    return SimpleDocTemplate(path or OUT, pagesize=A4,
                              leftMargin=MARGIN, rightMargin=MARGIN,
                              topMargin=32 * mm, bottomMargin=16 * mm,
                              title="Fiche SFAR 2007 - Blocs perimedullaires (Q8 - Analgesie postoperatoire)",
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
