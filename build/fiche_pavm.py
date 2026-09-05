# -*- coding: utf-8 -*-
"""
Fiche de synthese - RFE commune SFAR-SRLF (avec ADARPEF/GFRUP), "Pneumonies associees
aux soins de reanimation". Texte valide par le CA SFAR (29/06/2017) et le CA SRLF
(08/06/2017), publie Anesth Reanim. 2018;4:421-441. 16 experts francophones, methode GRADE,
recherche bibliographique PubMed/Cochrane sur 10 ans, format PICO, 3 champs (prevention,
diagnostic, traitement) + 4 populations specifiquement analysees (BPCO, neutropenie,
postoperatoire, pediatrie) - seules BPCO et pediatrie ont donne lieu a des recommandations
numerotees dediees (R1.5 pour la BPCO ; R1.1 et R2.2 "Pediatrique" pour la pediatrie) ;
neutropenie et postoperatoire n'ont informe que l'argumentaire d'autres recommandations
(ex. R2.2 sur les prelevements chez l'oncohematologique, R1.3 sur la VNI postoperatoire),
sans recommandation propre - disclose explicitement pour eviter toute impression
d'exhaustivite par population.

Resume officiel : 15 recommandations chez l'adulte (+ 2 recommandations pediatriques
specifiques) et 4 "protocoles de soins" (avis d'experts). Mon propre inventaire independant,
item par item, denombre exactement les memes 15 recommandations numerotees chez l'adulte
(R1.1-R1.5, R2.1-R2.3, R3.1-R3.7) et les 2 recommandations pediatriques (R1.1 Pediatrique,
R2.2 Pediatrique) - concordance totale sur le total et la numerotation.

DIVERGENCE mineure relevee sur la repartition GRADE1/GRADE2 : le resume officiel de la
source annonce "trois [recommandations] ont un niveau de preuve eleve (GRADE 1) et onze un
niveau de preuve faible (GRADE 2)" (+1 avis d'experts = 15). Mon propre comptage direct,
verifie a trois reprises sur le tag imprime a la fin de chacune des 15 recommandations
adultes, denombre 4 recommandations taggees GRADE 1 (R1.1=1+, R3.2=1+, R3.5=1-, R3.7=1-) et
10 taggees GRADE 2 (R1.2, R1.3, R1.4, R2.1, R1.5, R2.2, R2.3, R3.1, R3.4, R3.6) - le total
(4+10+1=15) concorde avec le resume officiel, mais pas la repartition 1/2 annoncee (3+11 vs
4+10 constate). Chaque tag individuel est reproduit ici exactement comme imprime a cote de
sa recommandation (verifie ligne par ligne) ; la divergence porte uniquement sur le chiffre
agrege du resume, disclosee explicitement en tracabilite plutot que silencieusement
recalculee ou ignoree - meme logique de disclosure deja appliquee a plusieurs reprises dans
ce corpus pour des mismatchs d'agregat (jamais un cas de tag individuel errone jusqu'ici).

4 "protocoles de soins" (tous avis d'experts, distincts des recommandations R-numerotees) :
Protocole n1 = Figure 1, algorithme multimodal de prevention (image, transcrit en tableau
4 etapes) ; Protocole n2 = decontamination digestive selective, texte integralement
extractible (posologies) ; Protocole n3 = Figure 2, algorithme de procedure diagnostique
(image, transcrit en tableau d'etapes) ; Protocole n4 = Tableau IV, schemas therapeutiques
par situation clinique (texte integralement extractible, tableau dense de posologies
antibiotiques - reproduit verbatim, contenu a haut risque clinique).
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from style import *
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.units import mm

OUT = "/private/tmp/claude-501/-Users-macbook-Downloads-claude/65498e3e-5ddf-47a6-b100-3ac535d1faa0/scratchpad/rfe_sfar/output/Fiche_SFAR_SRLF_PAVM_2017.pdf"

SOURCE_TXT = ("Source : Recommandations Formalisées d'Experts (RFE) communes SFAR-SRLF, en "
              "collaboration avec l'ADARPEF et le GFRUP « Pneumonies associées aux soins de "
              "réanimation » — texte validé par le CA SFAR (29/06/2017) et le CA SRLF "
              "(08/06/2017), publié Anesth Reanim. 2018;4:421-441. Fiche de synthèse non "
              "officielle : se référer au texte intégral.")

def P(txt, style=S_CELL):
    return Paragraph(txt, style)

def chip(label, **kw):
    return grade_chip(label, **kw)

def reco_table(rows, col_widths):
    """rows: (ref, text, grade_label_for_chip)"""
    data = [[P("Réf.", S_HEAD_W), P("Recommandation", S_HEAD_W), P("Grade", S_HEAD_W_C)]]
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

def no_reco_panel(text):
    return info_panel(P("<b>Absence de recommandation</b> — " + text, S_BODY_SM), bg=GREY_LIGHT, border=GREY)

def simple_table(header, rows, col_widths):
    data = [[P(h, S_HEAD_W) for h in header]]
    for r in rows:
        data.append([P(c, S_CELL) for c in r])
    t = Table(data, colWidths=col_widths, repeatRows=1)
    st = [
        ("BACKGROUND",(0,0),(-1,0), TEAL_DARK), ("TEXTCOLOR",(0,0),(-1,0), WHITE),
        ("FONTNAME",(0,0),(-1,0), FONT_BOLD), ("FONTSIZE",(0,0),(-1,0), 8),
        ("GRID",(0,0),(-1,-1),0.5,GREY_LIGHT), ("VALIGN",(0,0),(-1,-1),"TOP"),
        ("TOPPADDING",(0,0),(-1,-1),3.4), ("BOTTOMPADDING",(0,0),(-1,-1),3.4), ("LEFTPADDING",(0,0),(-1,-1),5),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            st.append(("BACKGROUND",(0,i),(-1,i), BG_PANEL))
    t.setStyle(TableStyle(st))
    return t

TOTAL_PAGES = {"n": 8}

def on_page(canvas, doc, page_title):
    header_band(canvas, doc, "SFAR / SRLF — RFE 2017 — FICHE DE SYNTHÈSE",
                "Pneumonies associées aux soins",
                page_title, icon_fn=lambda c,x,y: icon_shield(c, x, y, 13*mm), color=NAVY)
    footer_band(canvas, doc, SOURCE_TXT, f"Page {doc.page} / {TOTAL_PAGES['n']}")

# ---------------------------------------------------------------------------
def _section_intro():
    story = []
    story.append(Spacer(1, 3*mm))
    story.append(info_panel(P(
        "<b>Objectif :</b> RFE commune SFAR-SRLF (en collaboration avec l'ADARPEF et le "
        "GFRUP pour la pédiatrie) — 16 experts francophones, produisant un cadre facilitant "
        "la prise de décision face à un patient suspect de pneumonie associée aux soins "
        "(PAS). 3 champs : prévention, diagnostic, traitement. 4 populations spécifiquement "
        "analysées : BPCO, neutropénie, postopératoire, pédiatrie — <b>seules la BPCO et la "
        "pédiatrie ont donné lieu à des recommandations dédiées</b> (R1.5 ; R1.1 et R2.2 "
        "« Pédiatrique ») ; neutropénie et postopératoire n'ont informé que l'argumentaire "
        "d'autres recommandations, sans recommandation propre. Méthode GRADE, format PICO, "
        "recherche bibliographique PubMed/Cochrane sur 10 ans (langue anglaise ou "
        "française).<br/><br/>"
        "<b>Résultats (résumé officiel) :</b> 15 recommandations chez l'adulte + 2 "
        "recommandations pédiatriques spécifiques + 4 « protocoles de soins » (avis "
        "d'experts, à titre indicatif). Accord fort obtenu pour l'ensemble après 2 tours de "
        "cotation et un amendement.",
        S_BODY), bg=BG_PANEL, border=TEAL))
    story.append(Spacer(1, 3*mm))
    story.append(info_panel(P(
        "<b>Épidémiologie :</b> la pneumonie associée aux soins est l'infection la plus "
        "fréquente en réanimation. Incidence de la PAVM : 1,9 à 3,8/1000 jours de "
        "ventilation mécanique aux États-Unis, &gt;18/1000 jours en Europe. Mortalité "
        "associée ~20 %, mortalité attribuable débattue (5-13 %), probablement plus élevée "
        "chez le BPCO, quasi nulle chez le traumatisé. Un pathogène est identifié dans ~70 % "
        "des cas suspectés (infection polymicrobienne dans 30 % des cas) — Enterobacteriaceae, "
        "S. aureus, P. aeruginosa, A. baumannii principalement ; formes précoces (&lt;5 j) "
        "davantage liées à S. aureus méticilline-sensible, S. pneumoniae, H. influenzae.",
        S_BODY_SM), bg=GREY_LIGHT, border=GREY))
    story.append(Spacer(1, 3*mm))
    cw = PAGE_W - 2*MARGIN
    story.append(simple_table(
        ["Tableau I — Critères de définition d'une pneumonie", ""],
        [
            ["Signes radiologiques", "Deux clichés radiologiques successifs suggérant "
             "l'apparition d'un foyer (un seul cliché suffit en l'absence d'antécédent "
             "cardiopulmonaire) — ET au moins un signe parmi : température &gt;38,3°C sans "
             "autre cause • leucocytes &lt;4000/mm³ ou ≥12 000/mm³ — ET au moins deux signes "
             "parmi : sécrétions purulentes • toux ou dyspnée • désaturation, besoin accru en "
             "oxygène ou nécessité d'assistance ventilatoire."],
            ["Pneumonie précoce vs. tardive", "PAVM et pneumonie sévère acquise à l'hôpital = "
             "infections survenant après 48h de ventilation mécanique/d'hospitalisation "
             "respectivement, ni présentes ni en incubation à l'admission. Précoce = apparue "
             "&lt;5 jours ; tardive = ≥5 jours."],
        ],
        [cw*0.28, cw*0.72]))
    story.append(Spacer(1, 3*mm))
    story.append(info_panel(P(
        "<b>Divergence source-interne relevée (répartition GRADE) :</b> le résumé officiel "
        "annonce « 3 recommandations GRADE 1 et 11 GRADE 2 » (+1 avis d'experts = 15). Notre "
        "inventaire direct, vérifié tag par tag sur les 15 recommandations adultes, dénombre "
        "4 recommandations GRADE 1 (R1.1, R3.2, R3.5, R3.7) et 10 GRADE 2 — le total (15) "
        "concorde avec le résumé officiel, mais pas la répartition annoncée. Chaque tag "
        "individuel ci-après est reproduit tel qu'imprimé à côté de sa recommandation.",
        S_BODY_SM), bg=AMBER_LIGHT, border=AMBER))
    return story

def _section_prevention():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Prévention"))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("R1.1", "Il faut utiliser une approche standardisée multimodale de prévention des "
         "pneumonies associées aux soins pour diminuer la morbidité des patients hospitalisés "
         "en réanimation.", "1+"),
        ("R1.1 P", "<i>(Pédiatrique)</i> Il faut probablement utiliser une approche "
         "standardisée multimodale visant la prévention des pneumonies associées aux soins "
         "pour diminuer la morbidité des patients hospitalisés en réanimation pédiatrique.", "2+"),
        ("R1.2", "Dans les unités où la prévalence des bactéries multirésistantes est faible "
         "(&lt;20 %), il faut probablement appliquer une décontamination digestive sélective "
         "associant un topique antiseptique par voie entérale et une antibioprophylaxie par "
         "voie systémique pour une durée inférieure à 5 jours pour diminuer la mortalité.", "2+"),
        ("R1.3", "Dans le cadre d'une prévention multimodale, il faut probablement associer "
         "certaines des méthodes suivantes : favoriser le recours à la VNI pour éviter "
         "l'intubation (notamment en postopératoire de chirurgie digestive et chez le BPCO) ; "
         "limiter les doses et durées des sédatifs/analgésiques (échelles de sédation/douleur/"
         "confort, arrêts quotidiens) ; initier précocement une nutrition entérale ; contrôler "
         "régulièrement la pression du ballonnet ; réaliser une aspiration sous-glottique "
         "(toutes les 6-8h) ; préférer la voie orotrachéale pour l'intubation.", "2+"),
        ("R1.4", "Il ne faut probablement pas utiliser les méthodes suivantes : trachéotomie "
         "précoce systématique (hors indication spécifique) ; prophylaxie anti-ulcéreuse hors "
         "indication ; nutrition entérale post-pylorique hors indication ; "
         "probiotiques/synbiotiques ; changement "
         "précoce systématique des filtres humidificateurs ; systèmes clos d'aspiration "
         "endotrachéale ; sonde d'intubation imprégnée d'antiseptique ou ballonnet "
         "« optimisé » ; décontamination oropharyngée à la polyvidone iodée ; "
         "antibioprophylaxie par aérosols ; décontamination cutanée quotidienne "
         "antiseptique.", "2-"),
        ("R1.5", "Au cours du sevrage des patients BPCO, il faut probablement utiliser la "
         "VNI pour réduire la durée de ventilation mécanique invasive, l'incidence des "
         "pneumonies associées aux soins et la morbi-mortalité.", "2+"),
    ], [15*mm, PAGE_W-2*MARGIN-15*mm-18*mm, 18*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(P("R1.2 : méta-analyses d'ECR — diminution significative de la mortalité "
                    "hospitalière, de la durée de VM et de l'incidence des PAS avec la "
                    "décontamination digestive sélective ; effet sur la mortalité observé "
                    "uniquement pour les protocoles associant topique antiseptique entéral + "
                    "antibiothérapie systémique, plus marqué chez les patients les plus "
                    "graves ; efficacité démontrée dans des environnements à faible prévalence "
                    "de BMR — à ne pas recommander si prévalence élevée, avec suivi régulier "
                    "de l'écologie locale. R1.3 : bénéfices démontrés sur l'incidence des PAS "
                    "et/ou la durée de VM/séjour pour chaque méthode listée, mais sans "
                    "réduction de mortalité démontrée isolément — l'association pourrait "
                    "apporter un bénéfice non démontré à ce jour. R1.4 : aucun impact positif "
                    "démontré sur les PAS pour ces méthodes ; la polyvidone iodée expose à des "
                    "effets toxiques potentiels. R1.5 : 2 méta-analyses (632 et 959 patients "
                    "BPCO) — réduction significative de la mortalité (RR 0,36 et 0,27), de "
                    "l'échec de sevrage et du risque de PAVM, mais limites méthodologiques "
                    "(études non randomisées, faibles effectifs, définitions hétérogènes de "
                    "la PAVM).", S_NOTE))
    story.append(Spacer(1, 3*mm))
    story.append(section_bar("Figure 1 (source) — Protocole de soin n°1 : prévention multimodale (avis d'experts)", color=GREY))
    story.append(Spacer(1, 2*mm))
    cw = PAGE_W - 2*MARGIN
    story.append(simple_table(
        ["Étape", "Contenu"],
        [
            ["1", "Favoriser la ventilation non invasive (notamment en postopératoire de "
             "chirurgie digestive et chez le BPCO)."],
            ["2 (si VM invasive nécessaire)", "Appliquer un protocole de décontamination "
             "digestive sélective avec antibiothérapie systémique &lt;5 jours si prévalence "
             "de BMR faible (&lt;20 %)."],
            ["3 — Associer en 1ère intention", "Favoriser le recours à la VNI pour éviter "
             "l'intubation • limiter doses/durées des sédatifs-analgésiques • initier "
             "précocement une nutrition entérale • contrôler régulièrement la pression du "
             "ballonnet • aspiration sous-glottique (/6-8h) • privilégier la voie "
             "orotrachéale. NB : proclive &gt;30° et/ou décontamination oropharyngée à la "
             "chlorhexidine 0,12-0,2 % envisageables en association (efficacité faible, peu "
             "coûteux, bien tolérés)."],
            ["4 — Éviter", "Trachéotomie précoce systématique (hors indication spécifique) • "
             "prophylaxie anti-ulcéreuse hors indication • nutrition entérale post-pylorique "
             "hors indication • "
             "probiotiques • changement précoce systématique des filtres • systèmes clos "
             "d'aspiration • sonde/ballonnet « optimisés » • polyvidone iodée • "
             "antibioprophylaxie par aérosols • décontamination cutanée quotidienne."],
        ],
        [cw*0.22, cw*0.78]))
    story.append(Spacer(1, 3*mm))
    story.append(info_panel(P(
        "<b>Protocole de soin n°2 (avis d'experts) — Décontamination digestive sélective :</b> "
        "application oropharyngée d'une pâte/gel (×4/j jusqu'à sortie de réanimation) — "
        "polymyxine E 2 %, tobramycine 2 %, amphotéricine B 2 % — <b>+</b> suspension par "
        "sonde nasogastrique 10 mL (×4/j) — 100 mg polymyxine E, 80 mg tobramycine, 500 mg "
        "amphotéricine B — <b>+</b> antibioprophylaxie IV 48-72h chez les patients ne "
        "nécessitant pas d'antibiothérapie curative (posologie indicative en l'absence "
        "d'insuffisance rénale) : céfazoline 1g×3/j (si allergie aux céphalosporines : "
        "ofloxacine 200mg×2/j ou ciprofloxacine 400mg×2/j).",
        S_BODY_SM), bg=BG_PANEL, border=TEAL))
    story.append(Spacer(1, 1.5*mm))
    story.append(P("<i>Note : la source utilise « tobramycine » dans le texte de ce "
                    "protocole mais « gentamicine » dans la recette de préparation officinale "
                    "du Tableau III ci-dessous — incohérence propre au texte source, "
                    "reproduite fidèlement plutôt qu'harmonisée.</i>", S_NOTE))
    story.append(Spacer(1, 2*mm))
    story.append(KeepTogether(simple_table(
        ["Tableau III — Préparation officinale (indicatif)", "Gel oral (125 mL)", "Suspension (15 mL)"],
        [
            ["Polymyxine E", "4 g", "1 g"],
            ["Gentamicine", "4 g", "0,8 g"],
            ["Amphotéricine B", "4 g", "5 g"],
            ["Eau stérile", "134 mL", "100 mL"],
            ["Méthylcarboxycellulose", "6 g", "—"],
            ["Méthylparahydroxybenzoate", "0,3 g", "—"],
            ["Propylène glycol", "50 mL", "—"],
            ["Alcool mentholé", "6 mL", "—"],
        ],
        [cw*0.4, cw*0.3, cw*0.3])))
    return story

def _section_diagnostic():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Diagnostic"))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("R2.1", "Il ne faut probablement pas utiliser les scores cliniques (CPIS, CPIS "
         "modifié) pour le diagnostic des pneumonies associées aux soins.", "2-"),
        ("R2.2", "Il faut probablement réaliser des prélèvements microbiologiques des voies "
         "aériennes, quel que soit le type, avant toute introduction ou modification de "
         "l'antibiothérapie.", "2+"),
        ("R2.2 P", "<i>(Pédiatrique)</i> Il faut probablement réaliser des prélèvements "
         "microbiologiques des voies aériennes, quel que soit le type, avant toute "
         "introduction ou modification de l'antibiothérapie.", "2+"),
        ("R2.3", "Il ne faut probablement pas mesurer les concentrations plasmatiques de "
         "procalcitonine ou alvéolaires de TREM-1 soluble pour diagnostiquer une pneumonie "
         "associée aux soins.", "2-"),
    ], [15*mm, PAGE_W-2*MARGIN-15*mm-18*mm, 18*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(P("R2.1 : performances du CPIS variables (Se/Sp 60-80 % vs. LBA) selon le "
                    "comparateur et la probabilité pré-test ; peu d'utilité pronostique du "
                    "CPIS initial. R2.2 : méta-analyse — le type de prélèvement (aspiration "
                    "endotrachéale, brosse protégée, LBA) et de culture (quantitative ou non) "
                    "n'a pas d'effet significatif sur le devenir du patient (mortalité J28, "
                    "durée de VM/séjour) — choix laissé au clinicien selon les habitudes de "
                    "service ; possible avantage des cultures quantitatives pour le diagnostic "
                    "et des prélèvements invasifs pour raccourcir la durée de traitement "
                    "(~2 jours de moins) ; ne doit pas retarder l'antibiothérapie urgente des "
                    "formes graves ou en SDRA. R2.3 : procalcitonine — 8 études/589 patients, "
                    "Se 54 %, Sp 67 %, performances insuffisantes ; sTREM-1 — 7 études/317 "
                    "patients, Se 83 %, Sp 77 %, mais seuils très variables (5-900 pg/mL) selon "
                    "les techniques de dosage, non standardisées.", S_NOTE))
    story.append(Spacer(1, 3*mm))
    story.append(section_bar("Figure 2 (source) — Protocole de soin n°3 : procédure diagnostique (avis d'experts)", color=GREY))
    story.append(Spacer(1, 2*mm))
    cw = PAGE_W - 2*MARGIN
    story.append(simple_table(
        ["Étape", "Contenu"],
        [
            ["1. Seuil temporel", "≥48h depuis l'admission en milieu de soins ou l'exposition "
             "au risque invasif (intubation)."],
            ["2. Suspicion clinique", "Apparition/aggravation de : fièvre (≥38,3°C) • "
             "expectorations/aspirations purulentes ou d'aspect modifié • hyperleucocytose "
             "(≥12 000/mm³) ou leucopénie (≤4000/mm³) • hypoxémie ou oxygéno-dépendance • "
             "signes auscultatoires en foyer • ou sepsis/choc septique sans autre foyer "
             "évident. Diagnostics différentiels à évoquer : atélectasie(s), intubation "
             "sélective, épanchements pleuraux ; complications associées : abcès pulmonaires, "
             "pleurésie purulente."],
            ["3. Radiographie(s) de thorax", "Opacité(s) en foyer(s), nouvellement apparue(s) "
             "ou évolutive(s) = diagnostic radiographique. En cas de doute, envisager "
             "tomodensitométrie thoracique (sans/avec injection) ou échographie."],
            ["4. Prélèvements puis traitement probabiliste", "Prélèvement des voies "
             "respiratoires (invasif ou non) + culture."],
            ["5. Résultat de culture", "Négative → arrêt du traitement probabiliste. Positive "
             "(≥ seuil selon le type de prélèvement) = diagnostic microbiologique → "
             "adaptation/désescalade selon l'identification, puis selon l'antibiogramme."],
        ],
        [cw*0.24, cw*0.76]))
    return story

def _section_traitement():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Traitement"))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("R3.1", "Il faut probablement réaliser les prélèvements et initier le traitement "
         "antibiotique en tenant compte des facteurs de risque de bactéries résistantes "
         "immédiatement en cas de suspicion de pneumonie avec signes de gravité "
         "hémodynamique (choc), respiratoire (SDRA) ou de terrain fragile "
         "(immunodépression).", "2+"),
        ("R3.2", "Il faut traiter par monothérapie en probabiliste les pneumonies associées "
         "aux soins du patient immunocompétent sous ventilation mécanique, en dehors de la "
         "présence de facteurs de risque de bactéries multirésistantes, de bacilles à Gram "
         "négatif non fermentants, et/ou de facteurs de risque élevé de mortalité (choc "
         "septique, défaillances d'organes).", "1+"),
        ("R3.3", "Les experts suggèrent de ne pas utiliser de manière probabiliste et "
         "systématique un antibiotique actif contre S. aureus résistant à la méticilline "
         "(SARM) dans le traitement des pneumonies associées aux soins.", "AE"),
        ("R3.4", "Il faut probablement réduire le spectre et privilégier une monothérapie "
         "pour l'antibiothérapie des pneumonies associées aux soins après documentation, y "
         "compris pour les bacilles à Gram négatif non fermentants.", "2+"),
        ("R3.5", "Il ne faut pas prolonger plus de 7 jours la durée du traitement "
         "antibiotique pour les pneumonies associées aux soins, y compris pour les "
         "pneumonies à bacille à Gram négatif non fermentant, en dehors de certaines "
         "situations (immunodépression, empyème, pneumonie nécrosante ou abcédée).", "1-"),
        ("R3.6", "Dans le cadre des pneumonies documentées à bacilles à Gram négatif "
         "multirésistants, sensibles à la colimycine et/ou aux aminosides et lorsque aucun "
         "autre antibiotique n'est efficace, il faut probablement administrer la colimycine "
         "(colistiméthate sodique) et/ou un aminoside par voie nébulisée.", "2+"),
        ("R3.7", "Il ne faut pas administrer des statines comme traitement adjuvant des "
         "pneumonies associées aux soins.", "1-"),
    ], [15*mm, PAGE_W-2*MARGIN-15*mm-18*mm, 18*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(P("R3.2 : méta-analyse de 4 ECR (1163 patients) — aucune différence "
                    "mono- vs. bithérapie sur la mortalité (OR 0,97), la guérison clinique "
                    "(OR 0,88) ou les effets secondaires (OR 0,93) ; bithérapie probabiliste "
                    "indiquée si ≥1 facteur de risque de BMR/BGN non fermentant (antibiothérapie "
                    "&lt;90j, hospitalisation &gt;5j, EER, choc septique, SDRA) ou mortalité "
                    "prédictible &gt;25 % — à réadapter en monothérapie selon l'antibiogramme. "
                    "R3.3 : prévalence du SARM en France &lt;3 % (vs. 15 % dans l'étude "
                    "positive isolée) — pas d'argument pour un usage systématique ; facteurs "
                    "incitant à couvrir le SARM : prévalence locale élevée, colonisation "
                    "récente, lésion cutanée chronique, dialyse chronique. R3.5 : 2 "
                    "méta-analyses (508 et 883 patients) — pas de différence de mortalité "
                    "J28/séjour/hôpital entre traitement court (≤8j) et long (&gt;9j), plus de "
                    "jours vivants sans antibiotiques à J28 (+4,02j) avec le traitement court ; "
                    "tendance à plus de récidives pour les BGN non fermentants (non confirmée "
                    "dans la 2e méta-analyse) ; patients immunodéprimés et empyème/pneumonie "
                    "nécrosante exclus des études — ne pas étendre la recommandation à ces "
                    "situations. R3.6 : méta-analyse (6 ECR + 5 études observationnelles) — "
                    "bénéfice sur la mortalité (RR 0,64) et réduction de néphrotoxicité (RR "
                    "0,33) avec la voie nébulisée ; nécessite une formation préalable des "
                    "équipes au matériel spécifique. R3.7 : 5 ECR + 1 méta-analyse (867 "
                    "patients) — aucun bénéfice des statines sur mortalité, durée de séjour "
                    "ou de VM ; bonne tolérance mais absence d'effet retenue comme "
                    "interprétable malgré un sous-groupe observationnel favorable "
                    "(hétérogène, biais de publication).", S_NOTE))
    story.append(Spacer(1, 3*mm))
    story.append(section_bar("Tableau IV (source) — Protocole de soin n°4 : schémas thérapeutiques (avis d'experts)", color=GREY))
    story.append(Spacer(1, 2*mm))
    cw = PAGE_W - 2*MARGIN
    story.append(simple_table(
        ["Situation clinique", "Antibiothérapie probabiliste", "Si allergie aux β-lactamines"],
        [
            ["Pneumonie précoce (&lt;5j), sans choc septique ni FdR de BMR",
             "Amoxicilline/acide clavulanique 3-6 g/j OU céfotaxime (C3G) 3-6 g/j",
             "Lévofloxacine"],
            ["Pneumonie précoce (&lt;5j) + choc septique, sans FdR de BMR",
             "Amoxicilline/ac. clav. OU céfotaxime + aminoside (ex. gentamicine 8 mg/kg/j) "
             "OU fluoroquinolone (ex. ofloxacine 200 mg×2/j)",
             "Lévofloxacine 500 mg×2/j + gentamicine 8 mg/kg/j"],
            ["Pneumonie tardive (≥5j) ou FdR de bacille à Gram négatif non fermentant",
             "Ceftazidime 6 g/j OU céfépime 4-6 g/j OU pipéracilline-tazobactam 16 g/j (ou "
             "si BLSE) OU imipénem-cilastatine 3 g/j OU méropénème 3-6 g/j + aminoside "
             "(amikacine 30 mg/kg/j, priorité sur gentamicine) OU fluoroquinolone "
             "(ciprofloxacine 400 mg×3/j)",
             "Aztréonam 3-6 g/j + clindamycine 600 mg×3-4/j"],
            ["Facteurs de risque de SARM (ajout systématique)",
             "Vancomycine 15 mg/kg puis 30-40 mg/kg/j OU linézolide 600 mg×2/j", "—"],
        ],
        [cw*0.30, cw*0.50, cw*0.20]))
    story.append(Spacer(1, 2*mm))
    story.append(P("Posologies indicatives pour un patient à fonction rénale normale et "
                    "poids standard. FdR de bacille à Gram négatif non fermentant : "
                    "antibiothérapie dans les 90 jours précédents, hospitalisation &gt;5 "
                    "jours, épuration extra-rénale au diagnostic, choc septique, SDRA. FdR de "
                    "SARM : prévalence locale élevée, colonisation récente, lésion cutanée "
                    "chronique, dialyse chronique. Privilégier les aminosides aux "
                    "fluoroquinolones pour limiter l'émergence de BMR ; privilégier "
                    "l'amikacine à la gentamicine pour son activité sur les bacilles à Gram "
                    "négatif non fermentants.", S_NOTE))
    return story

def _section_synthese():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Synthèse et messages clés"))
    story.append(Spacer(1, 2*mm))
    story.append(P(
        "• Prévention : approche standardisée multimodale systématique (protocole n°1) — "
        "privilégier la VNI, limiter sédation, nutrition entérale précoce, contrôle du "
        "ballonnet, aspiration sous-glottique, voie orotrachéale. Décontamination digestive "
        "sélective probablement recommandée si prévalence de BMR &lt;20 % (durée "
        "d'antibioprophylaxie systémique &lt;5 jours). Plusieurs pratiques autrefois "
        "proposées (trachéotomie précoce systématique, polyvidone iodée, filtres "
        "systématiques, systèmes clos d'aspiration…) sont probablement à éviter.<br/>"
        "• Diagnostic : il ne faut probablement pas se fier aux scores cliniques (CPIS) ni "
        "aux biomarqueurs (PCT, sTREM-1) — diagnostic radio-clinico-microbiologique "
        "(protocole n°3). Il faut probablement réaliser un prélèvement microbiologique avant "
        "toute (ré)introduction d'antibiotique, sans retarder le traitement urgent des "
        "formes graves.<br/>"
        "• Traitement : bithérapie probabiliste réservée aux patients à risque de BMR/BGN "
        "non fermentant ou à mortalité prédictible élevée — monothérapie en 1ère intention "
        "sinon (recommandation forte), et désescalade probablement recommandée après "
        "documentation (y compris pour les BGN non fermentants). Pas de couverture anti-SARM "
        "systématique en France (prévalence &lt;3 %). Durée de traitement ≤7 jours "
        "(recommandation forte ; hors immunodépression, empyème, pneumonie "
        "nécrosante/abcédée). Nébulisation de colimycine/aminoside probablement indiquée en "
        "cas d'impasse thérapeutique sur BGN multirésistant. Statines : pas d'indication en "
        "traitement adjuvant (recommandation forte).<br/>"
        "• Chez le BPCO : VNI probablement recommandée pour le sevrage ventilatoire "
        "(réduction attendue de la durée de VM invasive, de l'incidence des PAS et de la "
        "morbi-mortalité). Chez "
        "l'enfant : approche multimodale et prélèvements avant antibiothérapie, mêmes "
        "principes que chez l'adulte (niveau de preuve GRADE 2+).",
        S_BODY))
    story.append(Spacer(1, 5*mm))

    story.append(section_bar("Sources et traçabilité", color=GREY))
    story.append(Spacer(1, 2*mm))
    story.append(P(
        "<b>Document source :</b> « Pneumonies associées aux soins de réanimation » — "
        "Recommandations Formalisées d'Experts communes SFAR-SRLF, en collaboration avec "
        "l'ADARPEF et le GFRUP. Texte validé par le CA SFAR (29/06/2017) et le CA SRLF "
        "(08/06/2017), publié Anesth Reanim. 2018;4:421-441. 16 experts francophones, "
        "coordination M. Leone (SFAR), L. Bouadma (SRLF).", S_SOURCE))
    story.append(Spacer(1, 1.5*mm))
    story.append(P("<b>Couverture :</b> les 15 recommandations numérotées chez l'adulte "
                    "(R1.1-R1.5, R2.1-R2.3, R3.1-R3.7), les 2 recommandations pédiatriques "
                    "(R1.1 et R2.2 « Pédiatrique »), et les 4 protocoles de soins (avis "
                    "d'experts) sont reproduits intégralement, avec les statistiques clés de "
                    "chaque argumentaire. Concordance exacte avec le résumé officiel sur le "
                    "total (15 recommandations adultes + 2 pédiatriques + 4 protocoles).", S_SOURCE))
    story.append(Spacer(1, 1.5*mm))
    story.append(P("<b>Divergence de répartition GRADE (disclosure) :</b> le résumé officiel "
                    "annonce « 3 GRADE 1 et 11 GRADE 2 » sur les 15 recommandations adultes ; "
                    "notre comptage direct sur chacun des 15 tags imprimés dénombre 4 GRADE 1 "
                    "(R1.1, R3.2, R3.5, R3.7) et 10 GRADE 2 — le total de 15 concorde, la "
                    "répartition annoncée par le résumé non. Chaque tag est reproduit ici "
                    "exactement comme imprimé à côté de sa recommandation dans le corps du "
                    "texte.", S_SOURCE))
    story.append(Spacer(1, 1.5*mm))
    story.append(P("<b>Populations spécifiques :</b> 4 populations ont été « analysées » par "
                    "la source (BPCO, neutropénie, postopératoire, pédiatrie) mais seules la "
                    "BPCO et la pédiatrie ont donné lieu à des recommandations numérotées "
                    "dédiées — neutropénie et postopératoire n'apparaissent que dans "
                    "l'argumentaire d'autres recommandations (ex. R2.2 pour "
                    "l'oncohématologie, R1.3 pour la VNI postopératoire), sans recommandation "
                    "propre.", S_SOURCE))
    story.append(Spacer(1, 3*mm))
    story.append(info_panel(P(
        "<b>Avertissement :</b> ce document est une fiche de synthèse indépendante, produite "
        "pour un usage d'aide-mémoire. Il reprend l'intégralité des recommandations de la "
        "RFE mais ne remplace pas le texte intégral et n'est ni édité ni validé par la "
        "SFAR/SRLF. En cas de doute, se référer au texte intégral, aux recommandations "
        "ultérieures et/ou à un avis spécialisé.",
        S_BODY_SM), bg=GREY_LIGHT, border=GREY))
    return story

SECTIONS = [
    ("Introduction, méthodologie", _section_intro),
    ("Prévention", _section_prevention),
    ("Diagnostic", _section_diagnostic),
    ("Traitement", _section_traitement),
    ("Synthèse, sources & traçabilité", _section_synthese),
]

def _make_doc():
    return SimpleDocTemplate(OUT, pagesize=A4,
                              leftMargin=MARGIN, rightMargin=MARGIN,
                              topMargin=32*mm, bottomMargin=16*mm,
                              title="Fiche SFAR-SRLF 2017 - Pneumonies associees aux soins de reanimation",
                              author="Synthèse indépendante (source SFAR/SRLF)")

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
