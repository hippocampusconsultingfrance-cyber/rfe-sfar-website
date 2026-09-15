# -*- coding: utf-8 -*-
"""
Fiche de synthese - RFE commune SFAR/SRLF/SPILF/AFC/SFCD, "Prise en charge
des infections intra-abdominales", fevrier 2015 (Ann Fr Anesth Reanim,
tome 1, n1). Auteurs coordinateurs : P. Montravers, H. Dupont, M. Leone,
J-M. Constantin, P-M. Mertes, P-F. Laterre, B. Misset. Actualisation de la
Conference de consensus SFAR de 2000. 25 pages source, telecharge depuis
sfar.org (wp-content/uploads/2015/09/2_AFAR_Prise-en-charge-des-infections-
intra-abdominales.pdf).

METHODOLOGIE : GRADE standard (qualite des preuves 4 niveaux, force
1+/1-/2+/2-, vote Delphi). 62 recommandations initialement formalisees par
le comite d'organisation -> apres 2 tours de cotation par un groupe de
relecture de 38 medecins et divers amendements, 18 ont ete abandonnees ou
reformulees -> 44 RECOMMANDATIONS FINALES presentees dans le texte, TOUTES
a Accord fort (verifie par comptage direct : R1-R44, aucun numero manquant,
aucune sans "Accord FORT").

INCOHERENCE SOURCE DISCLOSED (regle 5) : le texte affirme que parmi les 44
recommandations, "10 sont fortes (Grade 1 positif ou negatif), 25 sont
faibles (Grade 2 positif ou negatif) et... 9 recommandations... correspon-
dent a un avis d'experts" (10+25+9=44). Un comptage direct de chaque tag
individuel (R1-R44) donne 11 Grade 1 (7x 1+ : R3,R7,R10,R11,R19,R25,R38 ;
4x 1- : R5,R8,R13,R14), 24 Grade 2, et 9 avis d'experts (11+24+9=44) - le
compte "10 fortes/25 faibles" de la source ne correspond pas au tally direct
des tags individuels, bien que le total (44) et le compte "avis d'experts"
(9) concordent exactement. Disclose, non resolu (source imprime peut-etre
un decompte erronement arrondi, ou une recommandation supplementaire a ete
comptee differemment lors de la redaction du texte de synthese).

PARTICULARITES PEDIATRIQUES : CORRECTION POST-AUDIT (l'affirmation initiale de
ce docstring etait fausse, trouvee par l'audit independant) - la section
"Recommandations pour les infections intra-abdominales en pediatrie" du texte
source N'EST PAS purement narrative : elle contient bien 3 recommandations
propres, R25, R26 et R27 (dont les argumentaires citent des etudes
specifiquement pediatriques - appendicite chez l'enfant pour R25, exposition
de l'enfant pour R26, comparaison explicite a "l'adulte" pour R27). Comptage
par theme reconcilie exactement les 44 recommandations sur les 6 themes du
texte source : communautaire R1-R24 (24) + pediatrie R25-R27 (3) + associees
aux soins R28-R44 (17) = 44. Ces 3 recommandations sont regroupees dans leur
propre section "Particularites pediatriques" plutot que sous "associees aux
soins" comme dans une version anterieure de cette fiche - corrige.

FIGURES : 3 algorithmes (Fig. 1 prise en charge péritonite communautaire,
Fig. 2 antibiotherapie probabiliste communautaire, Fig. 3 antibiotherapie
probabiliste associee aux soins) sont de purs schemas boites/fleches sans
couche texte exploitable - retranscrits en tableau apres rendu visuel direct
du PDF source a 170dpi (pages 97-99), et fideles a un pur resume visuel des
recommandations R1-R44 deja couvertes textuellement (aucun contenu
clinique nouveau au-dela de ce que R1-R44 couvrent deja).

ARGUMENTAIRE : condense (regle de projet 2026-09-14) - seuls les seuils/
schemas therapeutiques directement actionnables sont conserves ; les
statistiques d'etudes sont omises - se referer au texte integral.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from style import *
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.units import mm

OUT = "/home/user/rfe-sfar-website/output/Fiche_SFAR_Infections_Intra_Abdominales_2015.pdf"

SOURCE_TXT = ("Source : « Prise en charge des infections intra-abdominales » — RFE SFAR/"
              "SRLF/SPILF/AFC/SFCD, Ann Fr Anesth Réanim, tome 1 (2015). Fiche de synthèse "
              "non officielle : se référer au texte intégral.")

def P(txt, style=S_CELL):
    return Paragraph(txt, style)

def chip(label, **kw):
    return grade_chip(label, **kw)

CW_FULL = PAGE_W - 2 * MARGIN

def reco_table(rows, col_widths):
    """rows: (ref, text, grade)."""
    data = [[P("N°", S_HEAD_W_C), P("Recommandation", S_HEAD_W), P("Grade", S_HEAD_W_C)]]
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

RCW = [12 * mm, CW_FULL - 12 * mm - 18 * mm, 18 * mm]

def theme_table(rows, col_widths, head=("Thème", "Détail")):
    data = [[P(head[0], S_HEAD_W), P(head[1], S_HEAD_W)]]
    for theme, detail in rows:
        data.append([P(theme, S_CELL_B), P(detail, S_CELL)])
    t = Table(data, colWidths=col_widths, repeatRows=1)
    style_cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), NAVY), ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTNAME", (0, 0), (-1, 0), FONT_BOLD), ("FONTSIZE", (0, 0), (-1, 0), 8),
        ("VALIGN", (0, 0), (-1, -1), "TOP"), ("ALIGN", (0, 1), (0, -1), "LEFT"),
        ("GRID", (0, 0), (-1, -1), 0.5, GREY_LIGHT),
        ("TOPPADDING", (0, 0), (-1, -1), 3.4), ("BOTTOMPADDING", (0, 0), (-1, -1), 3.4),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            style_cmds.append(("BACKGROUND", (0, i), (-1, i), BG_PANEL))
    t.setStyle(TableStyle(style_cmds))
    return t

TCW = [50 * mm, CW_FULL - 50 * mm]

def legend_flowable():
    chip_w = 15 * mm
    content_w = CW_FULL
    row = Table([[chip("1+", width=chip_w - 2 * mm), chip("1-", width=chip_w - 2 * mm),
                  chip("2+", width=chip_w - 2 * mm), chip("2-", width=chip_w - 2 * mm),
                  chip("AE", width=chip_w - 2 * mm),
                  P("<b>GRADE</b> — 1+/1- : recommandation <b>forte</b> ; 2+/2- : "
                    "recommandation <b>faible/optionnelle</b> ; <b>AE</b> : avis d'experts "
                    "(méthode GRADE non applicable). Toutes les 44 recommandations de ce "
                    "texte sont à <b>Accord fort</b> (vote Delphi, 2 tours).", S_BADGE_HEAD)]],
                colWidths=[chip_w, chip_w, chip_w, chip_w, chip_w, content_w - 5 * chip_w])
    row.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                              ("LEFTPADDING", (0, 0), (-1, -1), 1),
                              ("RIGHTPADDING", (0, 0), (-1, -1), 1),
                              ("TOPPADDING", (0, 0), (-1, -1), 0),
                              ("BOTTOMPADDING", (0, 0), (-1, -1), 0)]))
    return row

TOTAL_PAGES = {"n": 10}

def on_page(canvas, doc, page_title):
    header_band(canvas, doc, "SFAR / SRLF / SPILF / AFC / SFCD — RFE, 2015",
                "Infections intra-abdominales",
                page_title, icon_fn=lambda c, x, y: icon_shield(c, x, y, 13 * mm), color=RED)
    footer_band(canvas, doc, SOURCE_TXT, f"Page {doc.page} / {TOTAL_PAGES['n']}")

# ---------------------------------------------------------------------------
SEVERITY_ROWS = [
    ("Définition", "Forme grave de péritonite = ≥ 2 des manifestations suivantes (en "
     "l'absence d'autre cause) :"),
    ("Critères (≥ 2 requis)", "Hypotension rapportée au sepsis ; lactacidémie au-dessus des "
     "valeurs normales du laboratoire ; diurèse &lt; 0,5 mL/kg/h pendant &gt; 2 h malgré un "
     "remplissage adapté ; ratio PaO<sub>2</sub>/FiO<sub>2</sub> &lt; 250 mmHg en l'absence de pneumopathie ; "
     "créatininémie &gt; 2 mg/dL (176,8 µmol/L) ; bilirubinémie &gt; 2 mg/dL (34,2 µmol/L) ; "
     "thrombopénie &lt; 100 000/mm³."),
]

def _section_intro():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Résumé :</b> actualisation 2015 (SFAR/SRLF/SPILF/AFC/SFCD) de la Conférence de "
        "consensus SFAR de 2000 sur les péritonites communautaires, étendue aux infections "
        "intra-abdominales (IIA) pédiatriques et associées aux soins. Champ : péritonites "
        "nécessitant une prise en charge chirurgicale — <b>hors champ</b> : infections "
        "primaires des cirrhoses, infections focalisées isolées (biliaires, abcès "
        "hépatiques isolés, sigmoïdites). Règles de bon sens rappelées par les experts : "
        "éradication systématique et en urgence de la source infectieuse ; ne jamais "
        "différer l'antibiothérapie pour les prélèvements ; ne jamais prélever sur redons/"
        "drains (résultats ininterprétables) ; le spectre antibiotique doit toujours "
        "couvrir les anaérobies. <b>44 recommandations, toutes Accord fort.</b>", S_BODY),
        bg=BG_PANEL, border=TEAL))
    story.append(Spacer(1, 3 * mm))
    story.append(KeepTogether([
        section_bar("Définition d'une péritonite grave", color=RED),
        Spacer(1, 1.5 * mm),
        theme_table(SEVERITY_ROWS, TCW),
    ]))
    story.append(Spacer(1, 1.2 * mm))
    story.append(P(
        "<i>Correction d'unité :</i> le texte source imprime « 176,8 mmol/L » et "
        "« 34,2 mmol/L » pour ces deux seuils — dimensionnellement incohérent avec "
        "2 mg/dL (probable artefact d'extraction du symbole µ, absent de tout le "
        "document source extrait) ; corrigé ici en µmol/L, seule unité physiologiquement "
        "plausible pour ces valeurs.", S_NOTE))
    story.append(Spacer(1, 2.5 * mm))
    story.append(section_bar("Méthodologie — GRADE", color=RED))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "GRADE standard : qualité des preuves en 4 catégories (Haute/Modérée/Basse/Très "
        "basse), force binaire — forte (GRADE 1+/1−) ou faible (GRADE 2+/2−) — déterminée "
        "par vote Delphi. 40 experts répartis en 6 groupes de travail ; publications "
        "retenues postérieures à 1999 (extension à 1990 si besoin). <b>62 recommandations "
        "initialement formalisées</b> → soumises à un groupe de relecture de 38 médecins → "
        "après 2 tours de cotation Delphi et amendements, 18 ont été abandonnées ou "
        "reformulées → <b>44 recommandations finales</b>, toutes à Accord fort.", S_BODY_SM))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<i>Disclosure :</i> le texte source affirme que parmi les 44 recommandations, "
        "« 10 sont fortes (Grade 1), 25 sont faibles (Grade 2) et... 9... avis d'experts ». "
        "Un comptage direct des tags individuels de ce document donne 11 Grade 1 (7×1+, "
        "4×1−), 24 Grade 2 et 9 avis d'experts (11+24+9=44) — le total et le compte « avis "
        "d'experts » concordent, mais la répartition forte/faible annoncée par la source "
        "(10/25) diffère du tally direct (11/24). Disclosure non résolue ici.", S_NOTE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(legend_flowable())
    return story

# ---------------------------------------------------------------------------
def _section_communautaire_diag():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("IIA communautaires — Diagnostic, contrôle de la source (R1-R8)", color=RED),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("R1", "Il ne faut probablement pas faire d'imagerie en cas de suspicion de "
         "péritonite par perforation d'organe chez un patient grave si celle-ci retarde "
         "la procédure chirurgicale.", "AE"),
        ("R2", "En cas de suspicion de péritonite par perforation d'ulcère gastroduodénal, "
         "l'indication opératoire peut être portée sur l'histoire clinique et la présence "
         "d'un pneumopéritoine sur un cliché d'abdomen sans préparation.", "AE"),
        ("R3", "Il faut opérer le plus rapidement possible un patient suspect de "
         "péritonite par perforation d'organe, tout particulièrement en cas de choc "
         "septique.", "1+"),
        ("R4", "Il ne faut probablement pas utiliser la voie laparoscopique pour l'ulcère "
         "peptique perforé en péritonite chez un patient avec plus d'1 des facteurs "
         "suivants : choc à l'admission, score ASA III-IV, symptômes &gt; 24 h (score de "
         "Boey).", "2-"),
        ("R5", "Il ne faut pas faire de voie d'abord laparoscopique en cas de péritonite "
         "stercorale d'origine diverticulaire (Hinchey IV) ou de péritonite généralisée.",
         "1-"),
        ("R6", "En l'absence d'instabilité hémodynamique (&gt; 0,1 mg/kg/min "
         "adrénaline/noradrénaline), il faut probablement discuter en pluridisciplinaire "
         "le drainage radiologique percutané en 1<sup>re</sup> intention des abcès "
         "intra-abdominaux (sans signe de perforation) avec analyse microbiologique.",
         "2+"),
        ("R7", "Il faut réaliser un contrôle du drainage par TDM en cas d'évolution "
         "défavorable.", "1+"),
        ("R8", "Lorsque le traitement chirurgical a été jugé satisfaisant (contrôle de la "
         "source, lavage), il ne faut pas programmer systématiquement de "
         "relaparotomies.", "1-"),
    ], RCW))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>Repères :</b> score de Boey (0-3 pts : choc à l'admission, ASA III-IV, "
        "symptômes &gt; 24 h) — laparoscopie sûre si score 0-1, contre-indiquée si score "
        "2-3. Relaparotomie « à la demande » (non systématique) : pas de bénéfice de "
        "survie démontré vs relaparotomie programmée, durées de séjour augmentées avec "
        "cette dernière.", S_BODY_SM))
    return story

def _section_communautaire_atb():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("IIA communautaires — Microbiologie et antibiothérapie (R9-R24)", color=RED),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("R9", "Il faut probablement prélever les liquides péritonéaux pour "
         "identification microbienne et sensibilité aux anti-infectieux.", "2+"),
        ("R10", "Chez les patients en choc septique et/ou immunodéprimés, il faut "
         "réaliser des hémocultures et un examen direct du liquide péritonéal à la "
         "recherche de levures.", "1+"),
        ("R11", "Il faut établir les protocoles de traitement probabiliste sur la base de "
         "l'analyse régulière des données microbiologiques nationales/régionales de "
         "résistance.", "1+"),
        ("R12", "Il ne faut probablement pas prendre en compte les E. coli résistants aux "
         "C3G sans signe de gravité, sauf résistance locorégionale &gt; 10 % ou séjour en "
         "zone à forte prévalence de BMR.", "2-"),
        ("R13", "Compte tenu de l'évolution des profils de sensibilité des bactéroïdes, "
         "il ne faut pas utiliser la clindamycine et la céfoxitine en probabiliste.", "1-"),
        ("R14", "En l'absence de signes de gravité, il ne faut pas initier de traitement "
         "probabiliste actif sur les Candidas.", "1-"),
        ("R15", "Dans les péritonites graves (communautaires ou associées aux soins), il "
         "faut probablement instaurer un traitement antifongique si ≥ 3 des critères "
         "suivants : défaillance hémodynamique, sexe féminin, chirurgie sus-mésocolique, "
         "antibiothérapie &gt; 48 h.", "2+"),
        ("R16", "Il ne faut probablement pas prendre en compte les entérocoques sans "
         "signe de gravité.", "2-"),
        ("R17", "En 1<sup>re</sup> intention : (1) amoxicilline/ac. clavulanique + "
         "gentamicine ; OU (2) céfotaxime/ceftriaxone + imidazolés.", "2+"),
        ("R18", "Si allergie avérée aux β-lactamines : lévofloxacine + gentamicine + "
         "métronidazole, ou à défaut tigécycline.", "AE"),
        ("R19", "En cas d'IIA grave, le traitement probabiliste doit être adapté sur les "
         "germes suspectés.", "1+"),
        ("R20", "Patient grave, IIA communautaire : pipéracilline/tazobactam ± "
         "gentamicine.", "2+"),
        ("R21", "Patient grave (communautaire ou associée aux soins), si traitement "
         "antifongique probabiliste décidé : échinocandine.", "AE"),
        ("R22", "Après réception des analyses microbiologiques/mycologiques, il faut "
         "probablement une désescalade (spectre le plus étroit possible).", "2+"),
        ("R23", "IIA communautaires localisées : antibiothérapie 2 à 3 jours.", "2+"),
        ("R24", "IIA communautaires généralisées : antibiothérapie 5 à 7 jours.", "2+"),
    ], RCW))
    return story

def _section_communautaire_all():
    story = _section_communautaire_diag()
    story.extend(_section_communautaire_atb())
    return story

# ---------------------------------------------------------------------------
def _section_pediatrie():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Particularités pédiatriques des IIA (R25-R27)", color=RED),
        Spacer(1, 1.5 * mm),
        P("Littérature limitée chez l'enfant (peu d'études, souvent observationnelles), "
          "raisonnements majoritairement extrapolés des données adulte ; pas de "
          "spécificité diagnostique propre à l'enfant (ni radiologique ni "
          "biologique).", S_BODY_SM),
        Spacer(1, 1 * mm),
    ]))
    story.append(reco_table([
        ("R25", "Chez l'enfant, il faut privilégier les examens iconographiques non "
         "irradiants.", "1+"),
        ("R26", "Chez l'enfant, il faut probablement prendre en compte Pseudomonas "
         "aeruginosa en cas de facteurs de gravité (défaillance viscérale, comorbidités) "
         "ou d'échec thérapeutique.", "2+"),
        ("R27", "Il ne faut probablement pas prolonger la durée de l'antibiothérapie "
         "pédiatrique au-delà de ce qui est recommandé chez l'adulte.", "2-"),
    ], RCW))
    return story

def _section_postop_diag():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("IIA associées aux soins — Diagnostic postopératoire (R28-R37)", color=RED),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("R28", "En cas de survenue ou d'aggravation d'une dysfonction d'organe dans les "
         "jours suivant une chirurgie abdominale, il faut probablement évoquer une "
         "IIA.", "2+"),
        ("R29", "À partir du 4<sup>e</sup>-5<sup>e</sup> jour post-intervention, il faut "
         "probablement discuter une reprise chirurgicale si aucune amélioration "
         "clinique/biologique.", "2+"),
        ("R30", "L'apparition postopératoire de signes de gravité sans autre cause "
         "évidente doit faire discuter une réintervention.", "2+"),
        ("R31", "Pour les abcès postopératoires : discuter en collégial le "
         "bénéfice-risque du drainage radiologique vs reprise chirurgicale, et "
         "probablement proposer une ponction diagnostique première à l'aiguille fine "
         "sous contrôle radiologique.", "2+"),
        ("R32", "En cas de suspicion de péritonite postopératoire chez un patient stable, "
         "il faut probablement réaliser une TDM abdominopelvienne avec injection (± "
         "opacification digestive à discuter).", "2+"),
        ("R33", "En l'absence d'amélioration clinique/biologique à 4-5 j, une TDM non "
         "contributive ne permet pas d'éliminer une IIA persistante.", "AE"),
        ("R34", "Il ne faut probablement pas utiliser de biomarqueur pour le diagnostic "
         "d'IIA persistante.", "2-"),
        ("R35", "Ponction diagnostique première à l'aiguille fine sous contrôle "
         "radiologique pour les collections des IIA associées aux soins, en cas de doute "
         "diagnostique.", "AE"),
        ("R36", "Il faut prélever hémocultures et liquides péritonéaux pour identification "
         "microbienne/fongique et sensibilité.", "AE"),
        ("R37", "Il faut probablement effectuer un examen direct du liquide péritonéal à "
         "la recherche de levures.", "2+"),
    ], RCW))
    return story

def _section_postop_atb():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("IIA associées aux soins — Antibiothérapie (R38-R44)", color=RED),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("R38", "1<sup>er</sup> épisode d'IIA associée aux soins : risque élevé de "
         "bactérie multirésistante si antibiothérapie dans les 3 mois précédents et/ou "
         "&gt; 2 jours avant le 1<sup>er</sup> épisode, et/ou délai &gt; 5 j entre 1<sup>re</sup> "
         "chirurgie et reprise.", "1+"),
        ("R39", "Patients porteurs connus d'entérobactéries résistantes aux C3G, "
         "entérocoques résistants ampicilline/vancomycine, ou SARM : il faut probablement "
         "en tenir compte dans le traitement probabiliste.", "2+"),
        ("R40", "Facteurs de risque d'entérocoque résistant à l'ampicilline (pathologie "
         "hépatobiliaire, transplanté hépatique, antibiothérapie en cours) : choisir un "
         "probabiliste actif (vancomycine, voire tigécycline).", "2+"),
        ("R41", "Traitement antifongique probabiliste si levure à l'examen direct "
         "(échinocandines si infection grave) ; traitement systématique si culture "
         "positive à levures hors redons/drains (échinocandines si grave ou souches "
         "résistantes au fluconazole).", "2+"),
        ("R42", "1<sup>er</sup> épisode, sans facteur de risque de BMR : pipéracilline/"
         "tazobactam + amikacine (optionnelle si non grave). ≥ 2 des 6 critères de BMR "
         "(ou 1 seul si choc septique) : carbapénème large spectre (imipénème/"
         "méropénème/doripénème) + amikacine (optionnelle si non grave — même règle que "
         "pour le 1<sup>er</sup> schéma). <i>6 critères BMR : traitement antérieur par "
         "céphalosporine de 3<sup>e</sup> gén. ou fluoroquinolone (dont monodose) &lt; 3 "
         "mois ; portage BLSE ou P. aeruginosa résistant ceftazidime &lt; 3 mois ; "
         "hospitalisation à l'étranger &lt; 12 mois ; EHPAD médicalisé + sonde/"
         "gastrotomie ; échec d'un traitement par céphalosporine 3<sup>e</sup> gén., "
         "fluoroquinolone ou pipéracilline-tazobactam à large spectre ; récidive &lt; 15 j "
         "d'infection traitée par pipéracilline-tazobactam ≥ 3 j.</i>", "2+"),
        ("R43", "Allergie aux β-lactamines : (1) ciprofloxacine + amikacine + "
         "métronidazole + vancomycine ; ou (2) aztréonam + amikacine + vancomycine + "
         "métronidazole ; ou (3) à défaut, tigécycline + ciprofloxacine.", "AE"),
        ("R44", "IIA nosocomiales/postopératoires : antibiothérapie 5 à 15 jours.", "AE"),
    ], RCW))
    return story

def _section_postop_all():
    story = _section_pediatrie()
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_postop_diag())
    story.extend(_section_postop_atb())
    return story

# ---------------------------------------------------------------------------
FIG1_ROWS = [
    ("Péritonite communautaire → signes de gravité ?", "(critères définis dans le "
     "préambule, cf. Définition d'une péritonite grave, page 1)"),
    ("Oui", "→ Chirurgie (laparoscopie ou laparotomie)"),
    ("Non", "→ Scanner abdominal → drainage radiologique de l'abcès, ou chirurgie si "
     "besoin"),
]

FIG2_ROWS = [
    ("Allergie aux β-lactamines ?", "Oui → lévofloxacine + métronidazole + gentamicine, "
     "OU tigécycline. Non → étape suivante."),
    ("Signes de gravité ?", "Oui → pipéracilline-tazobactam + gentamicine. Non → "
     "amoxicilline-ac. clavulanique + gentamicine, OU céfotaxime/ceftriaxone + "
     "métronidazole."),
    ("Traitement antifongique ? (critères R15)", "Oui → échinocandine (caspofungine, "
     "micafungine ou anidulafungine). Non → pas de traitement antifongique."),
]

FIG3_ROWS = [
    ("Allergie aux β-lactamines ?", "Oui → ciprofloxacine + métronidazole + amikacine + "
     "vancomycine, OU aztréonam + métronidazole + amikacine + vancomycine, OU "
     "tigécycline + ciprofloxacine. Non → étape suivante."),
    ("Facteurs de risque de BMR ? (critères R42)", "Oui → imipénème ou méropénème ± "
     "amikacine ± vancomycine. Non → pipéracilline-tazobactam + amikacine ± "
     "vancomycine."),
    ("Traitement antifongique ? (critères R15/R41)", "Oui → échinocandine (caspofungine, "
     "micafungine ou anidulafungine). Non → pas de traitement antifongique."),
]

def _section_figures_sources():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Algorithmes (Figures 1-3) — retranscrits depuis rendu visuel", color=RED),
        Spacer(1, 1.5 * mm),
        P("Les 3 algorithmes du texte source (pages 97-99) sont de purs schémas "
          "boîtes/flèches sans couche texte exploitable — retranscrits ci-dessous après "
          "rendu visuel direct à 170dpi. Ils résument visuellement les recommandations "
          "R1-R44 déjà couvertes ci-dessus, sans contenu clinique nouveau.", S_BODY_SM),
    ]))
    story.append(Spacer(1, 1.8 * mm))
    story.append(P("<b>Figure 1 — Prise en charge d'une péritonite communautaire</b>",
                    S_CELL_B))
    story.append(Spacer(1, 1 * mm))
    story.append(theme_table(FIG1_ROWS, TCW, head=("Étape", "Conduite")))
    story.append(Spacer(1, 2.2 * mm))
    story.append(P("<b>Figure 2 — Traitement anti-infectieux probabiliste, péritonite "
                    "communautaire</b>", S_CELL_B))
    story.append(Spacer(1, 1 * mm))
    story.append(theme_table(FIG2_ROWS, TCW, head=("Question", "Conduite")))
    story.append(Spacer(1, 2.2 * mm))
    story.append(P("<b>Figure 3 — Traitement anti-infectieux probabiliste, péritonite "
                    "associée aux soins</b>", S_CELL_B))
    story.append(Spacer(1, 1 * mm))
    story.append(theme_table(FIG3_ROWS, TCW, head=("Question", "Conduite")))
    story.append(Spacer(1, 2.5 * mm))
    story.append(section_bar("Déclaration d'intérêts, sources et traçabilité", color=GREY))
    story.append(Spacer(1, 2 * mm))
    story.append(P(
        "<b>Document source :</b> « Prise en charge des infections intra-abdominales » — "
        "RFE conjointe SFAR/SRLF/SPILF/AFC/SFCD. Coordinateurs : P. Montravers, H. Dupont, "
        "M. Leone, J-M. Constantin, P-M. Mertes (Sfar/SRLF), P-F. Laterre, B. Misset "
        "(SRLF), J-P. Bru, R. Gauzit, A. Sotto (SPILF), C. Brigand, A. Hamy (AFC), "
        "J-J. Tuech (SFCD). Actualisation de la Conférence de consensus Sfar de 2000. "
        "40 experts, 6 groupes de travail ; groupe de relecture de 38 médecins.", S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P("<b>Version :</b> Ann Fr Anesth Réanim, tome 1, n°1, février 2015.",
                    S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P("<b>Méthodologie :</b> GRADE (qualité des preuves 1-4, force "
                    "1+/1-/2+/2-, vote Delphi 2 tours) — voir détail en page 1.", S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>URL source :</b> https://sfar.org/wp-content/uploads/2015/09/"
        "2_AFAR_Prise-en-charge-des-infections-intra-abdominales.pdf", S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>Couverture :</b> intégralité des 44 recommandations finales sur les 6 thèmes "
        "de la source — communautaire (24), pédiatrie (3), associées aux soins (17) — "
        "(texte + grade) et des 3 figures/algorithmes (retranscrits depuis rendu "
        "visuel). Hors champ, explicitement exclu par la source elle-même : infections "
        "primaires des cirrhoses, infections focalisées isolées (biliaires, abcès "
        "hépatiques isolés, sigmoïdites). L'argumentaire détaillé (statistiques "
        "d'études, références bibliographiques) "
        "est volontairement condensé aux seuls seuils/schémas cliniquement actionnables "
        "— se référer au texte intégral pour le détail des preuves.", S_SOURCE))
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Avertissement — document de 2015 :</b> cette fiche de synthèse indépendante "
        "reprend l'intégralité des recommandations et algorithmes du texte source, mais "
        "ne remplace pas le texte intégral et n'est ni éditée ni validée par la Sfar, la "
        "SRLF, la SPILF, l'AFC ou la SFCD. Les schémas d'antibiothérapie probabiliste et "
        "les seuils de résistance bactérienne locorégionale ayant pu évoluer depuis 2015, "
        "se référer à un avis spécialisé (infectiologue, microbiologiste) et aux "
        "recommandations actualisées avant toute décision thérapeutique.",
        S_BODY_SM), bg=GREY_LIGHT, border=GREY))
    return story

def _section_intro_communautaire():
    story = _section_intro()
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_communautaire_all())
    return story

def _section_postop_figures_sources():
    story = _section_postop_all()
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_figures_sources())
    return story

SECTIONS = [
    ("Méthodologie, définitions & IIA communautaires", _section_intro_communautaire),
    ("IIA associées aux soins, algorithmes & sources", _section_postop_figures_sources),
]

def _make_doc(path=None):
    return SimpleDocTemplate(path or OUT, pagesize=A4,
                              leftMargin=MARGIN, rightMargin=MARGIN,
                              topMargin=32 * mm, bottomMargin=16 * mm,
                              title="Fiche SFAR 2015 - Infections intra-abdominales",
                              author="Synthèse indépendante (source SFAR/SRLF/SPILF/AFC/SFCD)")

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
