# -*- coding: utf-8 -*-
"""
Fiche de synthese - Reactualisation de la recommandation sur la douleur
postoperatoire (SFAR, RFE, texte valide par le CA de la Sfar le 17/06/2016).
F. Aubrun, K. Nouette Gaulain, D. Fletcher, A. Belbachir, et al.
Anesth Reanim. 2016;2:421-430, doi 10.1016/j.anrea.2016.09.006.
Source telechargee : sfar.org/wp-content/uploads/2016/09/RFE-ANREA-Reactualisation-de-
la-recommandation-sur-la-douleur-postoperatoire.pdf (10 pages).

CHAMP : ce texte NE REMPLACE PAS la RFE 2008 "Prise en charge de la douleur
postoperatoire chez l'adulte et l'enfant" (deja couverte par une fiche distincte de ce
corpus, cf. content_douleur_postoperatoire.json / migration webapp 0071) : il la
COMPLETE sur des questions non traitees en 2008, ou modifie certaines recommandations
2008 a la lumiere de nouvelles donnees. Les deux textes restent donc distincts et
tous deux couverts separement dans ce corpus - aucune fusion.

METHODOLOGIE GRADE (R1.4, R1.5, R3.x, R4.x) : force 1+/1-/2+/2- + avis d'experts (pas de
grade numerique quand aucune meta-analyse ne permettait d'appliquer GRADE) ; accord du
vote Delphi/GRADE Grid (fort >=70%, faible en-deca) - convention identique a
fiche_sujet_age_esf.py : "(accord faible)" en italique inline dans la cellule,
JAMAIS un second chip invente. COMPTAGE VERIFIE (grep exhaustif du texte source) :
17 recommandations formalisees, imprimees individuellement R1.1-R1.5, R3.1-R3.9,
R4.1-R4.3 (AUCUN R2.x n'existe : la question 2, monitorage de l'analgesie, a
explicitement abouti a une "Absence de recommandation" - imprime tel quel deux fois
dans le texte source, disclosure reproduite ci-dessous, PAS un manque de cette fiche).
DIVERGENCE SOURCE-INTERNE DISCLOSEE (non resolue silencieusement) : l'introduction de
la source annonce elle-meme "11 [recommandations] fortes, 3 [...] faibles et, pour
3 recommandations, [...] un avis d'experts" (11+3+3=17) ; le recompte exhaustif,
tag par tag, des 17 recommandations imprimees individuellement donne 10x GRADE 1+/1-
(fortes), 4x GRADE 2+/2- (faibles) et 3x avis d'experts (10+4+3=17 egalement, mais
10 fortes et non 11). Aucun grade individuel n'a ete devine ou reassigne pour faire
correspondre les deux comptages ; les 17 tags imprimes individuellement font foi
ci-dessous, le desaccord avec le total agrege de l'introduction est signale tel quel.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from style import *
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.units import mm

OUT = "/home/user/rfe-sfar-website/output/Fiche_SFAR_Douleur_Postoperatoire_Reactualisation_2016.pdf"

SOURCE_TXT = ("Source : « Réactualisation de la recommandation sur la douleur "
              "postopératoire » — SFAR, RFE 2016 (Anesth Reanim. 2016;2:421-430). Fiche "
              "de synthèse non officielle : se référer au texte intégral.")

def P(txt, style=S_CELL):
    return Paragraph(txt, style)

def chip(label, **kw):
    return grade_chip(label, **kw)

RCW = [12*mm, PAGE_W-2*MARGIN-12*mm-18*mm, 18*mm]

def reco_table(rows, col_widths=RCW):
    """rows: (ref, text, grade_label)"""
    data = [[P("Réf.", S_HEAD_W_C), P("Recommandation (texte condensé, fidèle à la source)", S_HEAD_W), P("Grade", S_HEAD_W_C)]]
    for ref, txt, grade in rows:
        data.append([P(ref, S_CELL_B), P(txt, S_CELL), chip(grade)])
    t = Table(data, colWidths=col_widths, repeatRows=1)
    style_cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), NAVY), ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTNAME", (0, 0), (-1, 0), FONT_BOLD), ("FONTSIZE", (0, 0), (-1, 0), 8),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("ALIGN", (0, 0), (0, -1), "CENTER"),
        ("ALIGN", (2, 0), (2, -1), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 0.5, GREY_LIGHT),
        ("TOPPADDING", (0, 0), (-1, -1), 3.4), ("BOTTOMPADDING", (0, 0), (-1, -1), 3.4),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            style_cmds.append(("BACKGROUND", (0, i), (-1, i), BG_PANEL))
    t.setStyle(TableStyle(style_cmds))
    return t

def legend_flowable():
    labels = ["1+", "1-", "2+", "2-", "AE"]
    texts = ["Il faut faire", "Il ne faut pas faire", "Il faut probablement faire",
             "Il ne faut probablement pas faire", "Avis d'experts"]
    chip_w = 13*mm
    cells = []
    for g, t in zip(labels, texts):
        cells.append(chip(g, width=chip_w-1.5*mm))
        cells.append(P(t, S_BADGE_HEAD))
    row = Table([cells], colWidths=[chip_w, 30*mm]*len(labels))
    row.setStyle(TableStyle([("VALIGN",(0,0),(-1,-1),"MIDDLE"), ("LEFTPADDING",(0,0),(-1,-1),1), ("RIGHTPADDING",(0,0),(-1,-1),2)]))
    return row

TOTAL_PAGES = {"n": 5}

def on_page(canvas, doc, page_title):
    header_band(canvas, doc, "SFAR — RÉACTUALISATION RFE 2016 — FICHE DE SYNTHÈSE",
                "Douleur postopératoire — réactualisation 2016",
                page_title, icon_fn=lambda c, x, y: icon_pill(c, x, y, 13*mm), color=NAVY)
    footer_band(canvas, doc, SOURCE_TXT, f"Page {doc.page} / {TOTAL_PAGES['n']}")

# ---------------------------------------------------------------------------
def _section_intro():
    story = []
    story.append(Spacer(1, 3*mm))
    story.append(info_panel(P(
        "<b>Champ :</b> cette réactualisation 2016 de la SFAR ne remplace PAS la RFE 2008 "
        "« Prise en charge de la douleur postopératoire chez l'adulte et l'enfant » "
        "(déjà couverte par une fiche distincte de ce corpus) : elle la <b>complète</b> "
        "sur des questions non traitées en 2008, ou <b>modifie</b> certaines "
        "recommandations 2008 à la lumière de nouvelles données de la littérature. "
        "Groupe de 14 experts SFAR, méthode GRADE®. Trois grands champs : évaluation de "
        "la DPO chez l'adulte et l'enfant (dont le monitorage de l'analgésie), "
        "thérapeutiques médicamenteuses par voies systémique et orale, anesthésie "
        "locale et locorégionale postopératoire.", S_BODY), bg=BG_PANEL, border=TEAL))
    story.append(Spacer(1, 3*mm))
    story.append(info_panel(P(
        "<b>Méthodologie GRADE® :</b> qualité des preuves en 4 catégories (haute, "
        "modérée, basse, très basse) ; formulation finale toujours binaire — "
        "<b>forte</b> : il faut/ne faut pas faire (GRADE 1+ ou 1−) ; <b>faible</b> : il "
        "faut probablement/probablement pas faire (GRADE 2+ ou 2−). Vote Delphi/GRADE "
        "Grid : accord fort si ≥ 70 % des participants d'accord. Quand aucune "
        "méta-analyse ne permettait d'appliquer GRADE en totalité, un <b>avis "
        "d'experts</b> était proposé, validé si ≥ 70 % d'accord. <b>17 recommandations "
        "formalisées</b> au total ; accord fort obtenu pour 14 d'entre elles (accord "
        "faible pour 3, signalé en italique inline).", S_BODY_SM), bg=BG_PANEL, border=TEAL))
    story.append(Spacer(1, 3*mm))
    story.append(info_panel(P(
        "<b>⚠ Divergence source-interne disclosée</b> (non résolue silencieusement) : "
        "l'introduction de la source annonce elle-même « 11 [recommandations] fortes, "
        "3 [...] faibles et, pour 3 recommandations, [...] un avis d'experts » "
        "(11+3+3 = 17). Le recompte exhaustif, tag par tag, des 17 recommandations "
        "imprimées individuellement (R1.1-R1.5, R3.1-R3.9, R4.1-R4.3 — aucun R2.x "
        "n'existe, voir note ci-dessous) donne <b>10× GRADE 1+/1− (fortes), 4× GRADE "
        "2+/2− (faibles) et 3× avis d'experts</b> (10+4+3 = 17 également, mais 10 "
        "fortes et non 11). Aucun grade individuel n'a été deviné ou réassigné pour "
        "faire correspondre les deux comptages ; les 17 tags imprimés individuellement "
        "font foi dans cette fiche.", S_BODY_SM), bg=AMBER_LIGHT, border=AMBER))
    story.append(Spacer(1, 3*mm))
    story.append(info_panel(P(
        "<b>Absence de recommandation formalisée — question du monitorage :</b> la "
        "question « quelles méthodes permettent de monitorer l'analgésie au bloc "
        "opératoire et en postopératoire immédiat ? » n'a abouti à AUCUNE "
        "recommandation formalisée (pupillométrie, index de nociception ANI, surgical "
        "pleth index SPI : évaluation correcte de la balance analgésie-nociception "
        "sous anesthésie générale, mais aucune preuve que ce monitorage réduise la "
        "douleur ou la consommation d'antalgiques postopératoires) — disclosure "
        "explicite de la source elle-même (« Absence de recommandation », imprimé tel "
        "quel), reproduite ici plutôt que silencieusement omise. C'est pourquoi la "
        "numérotation des recommandations passe directement de R1.5 à R3.1 : la "
        "question 2 (monitorage) ne porte aucun numéro Rx.", S_BODY_SM), bg=GREY_LIGHT, border=GREY))
    story.append(Spacer(1, 3*mm))
    story.append(section_bar("Légende des grades"))
    story.append(Spacer(1, 2*mm))
    story.append(legend_flowable())
    return story

def _section_eval():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(KeepTogether([
        section_bar("1 — Évaluation de la douleur en périopératoire"),
        Spacer(1, 1.5*mm),
        P("<b>Quand et pourquoi évaluer ? Bénéfice sur les conséquences "
          "postopératoires/chronicisation</b>", S_CELL_B),
        Spacer(1, 1.5*mm),
        P("L'identification des patients vulnérables implique un suivi attentif avec "
          "une stratégie thérapeutique multimodale, comportant si possible une "
          "analgésie locorégionale et l'administration d'agents antihyperalgésiques. "
          "Facteurs chirurgicaux de risque de douleur chronique post-chirurgicale "
          "(DCPC) : type de chirurgie (thoracotomie, chirurgie mammaire, sternotomie, "
          "prélèvement de crête iliaque), reprises chirurgicales, douleurs "
          "préopératoires préexistantes, durée de chirurgie > 3 h. Facteurs "
          "psychologiques : anxiété, stress, dépression, catastrophisme — l'échelle "
          "APAIS (Amsterdam Preoperative Anxiety and Information Scale) permettrait de "
          "prédire la transition de la DPO aiguë à chronique. Une douleur "
          "neuropathique précoce devra être accompagnée d'un traitement adapté ; le "
          "résultat d'un dépistage positif devra être communiqué au patient, au "
          "chirurgien et au médecin traitant.", S_BODY_SM),
        Spacer(1, 1.5*mm),
        reco_table([
            ("R1.1", "En période préopératoire, il est recommandé d'identifier les "
             "patients les plus vulnérables à la douleur (à risque de développer une "
             "douleur postopératoire sévère et/ou une DCPC), en recherchant la présence "
             "d'une douleur préopératoire y compris en dehors du site opératoire, la "
             "consommation d'opiacés au long court, des facteurs chirurgicaux et "
             "psychiques tels que l'anxiété ou la dépression. <i>Avis d'experts, accord "
             "fort.</i>", "AE"),
            ("R1.2", "Il est probablement recommandé d'utiliser l'échelle Amsterdam "
             "Preoperative Anxiety and Information Scale (APAIS) pour rechercher une "
             "anxiété et/ou un besoin d'information en période préopératoire. <i>Avis "
             "d'experts, accord fort.</i>", "AE"),
            ("R1.3", "Il est recommandé d'identifier les facteurs de risques "
             "postopératoires de chronicisation de la DPO en recherchant une intensité "
             "élevée de la DPO à l'aide d'une échelle numérique (EN), une prolongation "
             "inhabituelle de la DPO, une douleur neuropathique précoce (échelle DN4), "
             "des signes d'anxiété et/ou de dépression. <i>Avis d'experts, accord "
             "fort.</i>", "AE"),
        ]),
    ]))
    story.append(Spacer(1, 2.5*mm))
    story.append(KeepTogether([
        P("<b>Échelles de douleur chez l'enfant de moins de 7 ans et chez le patient "
          "non communicant</b>", S_CELL_B),
        Spacer(1, 1.5*mm),
        P("Nouveau-nés : échelles EDIN, DAN, NFCS utilisables mais non validées en "
          "postopératoire ; FLACC utilisable à partir de 2 mois ; EVENDOL validée "
          "uniquement en préhospitalier/urgences ; l'EVA doit être présentée "
          "verticalement à l'enfant. Patient non communicant : FLACC modifiée-handicap "
          "(naissance à 18 ans, 5 items comportementaux) ; ALGOPLUS (score ≥ 2/5 : "
          "sensibilité 87 %, spécificité 80 %).", S_BODY_SM),
        Spacer(1, 1.5*mm),
        reco_table([
            ("R1.4", "Il est recommandé d'utiliser une échelle d'autoévaluation à partir "
             "de l'âge de 5 ans (échelle des visages). À défaut, il est recommandé "
             "d'utiliser l'échelle FLACC pour l'hétéroévaluation de la douleur "
             "postopératoire chez l'enfant de moins de 7 ans. <i>Accord fort.</i>", "1+"),
            ("R1.5", "Chez le patient non communiquant, il est probablement recommandé "
             "d'utiliser une échelle d'hétéroévaluation FLACC modifiée-handicap chez "
             "l'enfant et ALGOPLUS chez le vieillard. <i>(accord faible — tag imprimé "
             "« 1+ » par la source malgré la formulation « probablement recommandé », "
             "reproduit tel quel, non corrigé en 2+.)</i>", "1+"),
        ]),
    ]))
    story.append(Spacer(1, 2.5*mm))
    story.append(KeepTogether([
        P("<b>Surveillance des patients sous opioïdes en structure de soins "
          "conventionnels</b>", S_CELL_B),
        Spacer(1, 1.5*mm),
        P("Les modalités de surveillance (voie SC, ACP, péridurale) restent celles des "
          "conférences de consensus 1997/1999, non modifiées. Terrains à risque "
          "identifiés depuis : âge > 70 ans, naïveté aux opiacés, obésité morbide "
          "(IMC > 35), maladie respiratoire, SAOS, insuffisance hépatique/rénale, "
          "douleur intense cessant subitement, association à des dépresseurs du SNC "
          "(benzodiazépines, barbituriques, antidépresseurs, antiémétiques, "
          "antihistaminiques), alcool/drogues illicites, troubles neuromusculaires, "
          "voie périmédullaire. Une surveillance clinique plus fréquente et/ou un "
          "monitorage non invasif (saturométrie, capnographie en SSPI) sont "
          "probablement suggérés chez ces patients à risque — <b>aucune recommandation "
          "formalisée nouvelle</b> sur ce point (rappels méthodologiques uniquement).", S_BODY_SM),
    ]))
    story.append(Spacer(1, 2.5*mm))
    story.append(KeepTogether([
        P("<b>Monitorage de l'analgésie au bloc opératoire et en postopératoire "
          "immédiat</b>", S_CELL_B),
        Spacer(1, 1.5*mm),
        P("Pupillométrie, index de nociception (ANI), surgical pleth index (SPI) : "
          "évaluation correcte de la balance analgésie-nociception sous anesthésie "
          "générale, mais pas de preuve qu'un tel monitorage réduise la douleur "
          "postopératoire ou la consommation d'antalgiques. Chez le patient éveillé, "
          "corrélation partielle avec les scores d'auto/hétéroévaluation, sans preuve "
          "de supériorité en postopératoire immédiat ; aucune étude chez le patient "
          "« non communicant ».", S_BODY_SM),
        Spacer(1, 1.5*mm),
        info_panel(P("<b>Absence de recommandation formalisée</b> — imprimé tel quel par "
                      "la source (x2) pour cette question.", S_BODY_SM), bg=GREY_LIGHT, border=GREY),
    ]))
    return story

def _section_medoc():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(KeepTogether([
        section_bar("2 — Thérapeutiques médicamenteuses par voies systémique et orale"),
        Spacer(1, 1.5*mm),
        P("<b>AINS sélectifs (ISCOX2) et non sélectifs (AINS-NS)</b>", S_CELL_B),
        Spacer(1, 1.5*mm),
        P("Associés à la morphine : amélioration des scores de douleur, épargne "
          "morphinique significative, réduction des NVPO et de la durée de l'iléus "
          "(niveau de preuve élevé, 15 études dont 2 méta-analyses pour les AINS-NS, "
          "25 études dont 1 méta-analyse pour les ISCOX2). Risque rénal : contre-indiqués "
          "si clairance créatinine < 50 mL/min. Risque thrombotique : bien démontré pour "
          "les ISCOX2 ; pour les AINS-NS, 2 études rétrospectives (10 873 et 1309 "
          "patients) sans risque cardiovasculaire surajouté retrouvé. Risque "
          "hémorragique : les AINS utilisés en France (kétoprofène, ibuprofène) "
          "n'augmentent pas le risque hémorragique postopératoire, y compris après "
          "amygdalectomie ; vigilance chez les patients sous anticoagulants (étude sur "
          "8000 patients : risque de saignement x2,5 si AINS + anticoagulant curatif).", S_BODY_SM),
        Spacer(1, 1.5*mm),
        reco_table([
            ("R3.1", "Il est recommandé d'associer un AINS non sélectif (AINS-NS) ou un "
             "inhibiteur sélectif des cyclo-oxygénases de type 2 (ISCOX2) à la morphine "
             "en l'absence de contre-indication à l'usage de l'AINS. <i>Accord fort.</i>", "1+"),
            ("R3.2", "Il n'est pas recommandé d'utiliser un inhibiteur des "
             "cyclo-oxygénases de type 2 (ISCOX2) chez les patients ayant des "
             "antécédents athéro-thrombotiques artériels (AOMI, AVC, IDM). <i>Accord "
             "fort.</i>", "1-"),
            ("R3.3", "Les AINS-NS ne sont probablement pas recommandés chez les patients "
             "ayant des antécédents athéro-thrombotiques artériels (AOMI, AVC, IDM) "
             "au-delà de 7 jours de traitement. <i>Accord fort.</i>", "2-"),
            ("R3.4", "Il n'est pas recommandé d'associer des AINS-NS à un traitement "
             "anticoagulant à dose curative. <i>(accord faible)</i>", "1-"),
        ]),
    ]))
    story.append(Spacer(1, 2.5*mm))
    story.append(KeepTogether([
        P("<b>Oxycodone, opiacés forts, lidocaïne IV, corticoïdes</b>", S_CELL_B),
        Spacer(1, 1.5*mm),
        P("Oxycodone : efficacité clinique équivalente à la morphine (ratio 1/1 en IV, "
          "1/2 par voie orale — 5 mg oxycodone = 10 mg sulfate de morphine). Lidocaïne "
          "IV : propriétés analgésiques, antihyperalgésiques et anti-inflammatoires ; "
          "dose 1-2 mg/kg en bolus puis 1-2 mg/kg/h en continu. Dexaméthasone : "
          "corticoïde le plus étudié en prémédication, dose recommandée 8 mg chez "
          "l'adulte (0,15 mg/kg chez l'enfant).", S_BODY_SM),
        Spacer(1, 1.5*mm),
        reco_table([
            ("R3.5", "Il est recommandé de prescrire un opiacé fort (morphine ou "
             "oxycodone), préférentiellement par voie orale, en cas de douleurs "
             "postopératoires sévères ou insuffisamment calmées par les antalgiques des "
             "paliers inférieurs, et ceci quel que soit l'âge. <i>Accord fort.</i>", "1+"),
            ("R3.6", "Il est probablement recommandé d'administrer de la lidocaïne en "
             "intraveineux et en continu à la dose d'1 à 2 mg/kg en bolus intraveineux "
             "suivi de 1 à 2 mg/kg/h, chez les patients adultes opérés d'une chirurgie "
             "majeure (abdomino-pelvienne, rachidienne) et ne bénéficiant pas d'une "
             "analgésie périnerveuse ou péridurale concomitante, dans le but de diminuer "
             "la douleur postopératoire et d'améliorer la réhabilitation. <i>Accord "
             "fort.</i>", "2+"),
            ("R3.7", "Il est probablement recommandé d'administrer la dexaméthasone IV à "
             "la dose de 8 mg pour diminuer la douleur postopératoire. <i>Accord "
             "fort.</i>", "2+"),
        ]),
    ]))
    story.append(Spacer(1, 2.5*mm))
    story.append(KeepTogether([
        P("<b>Kétamine, magnésium, gabapentinoïdes</b>", S_CELL_B),
        Spacer(1, 1.5*mm),
        P("Kétamine à faible dose (0,5 mg/kg max après induction, entretien 0,125-0,25 "
          "mg/kg/h, arrêt 30 min avant la fin de la chirurgie) : réduit l'intensité de "
          "la douleur aiguë sur 24h, la consommation de morphine (~15 mg/24h) et les "
          "NVPO (niveau de preuve modéré) ; réduit l'incidence de la DCPC à 3 mois de "
          "30 % (niveau de preuve bas). Prolongation postopératoire : accroît le risque "
          "d'hallucinations sans bénéfice analgésique majoré. Magnésium : non "
          "recommandé (niveau de preuve insuffisant). Gabapentine/prégabaline en "
          "prémédication : réduisent douleur/consommation morphinique/NVPO sur 24h, "
          "mais aucun effet sur la DCPC (niveau de preuve élevé), risque de sédation/"
          "vertiges/troubles visuels ; bénéfice net surtout en chirurgie lourde "
          "pronociceptive (arthroplasties, rachis, amputations).", S_BODY_SM),
        Spacer(1, 1.5*mm),
        reco_table([
            ("R3.8", "En peropératoire, l'administration de faible dose de kétamine chez "
             "un patient sous anesthésie générale est recommandée dans les deux "
             "situations suivantes : (a) chirurgie à risque de douleur aiguë intense ou "
             "pourvoyeuse de DCPC ; (b) patients vulnérables à la douleur, en particulier "
             "sous opioïdes au long cours ou présentant une toxicomanie aux opiacés. "
             "<i>Accord fort.</i>", "1+"),
            ("R3.9", "L'utilisation systématique des gabapentinoïdes en périopératoire "
             "n'est pas recommandée pour la prise en charge de la DPO. <i>(accord "
             "faible)</i>", "1-"),
        ]),
    ]))
    return story

def _section_alr():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(KeepTogether([
        section_bar("3 — Anesthésie locale et locorégionale postopératoire"),
        Spacer(1, 1.5*mm),
        P("<b>Cathétérisme périnerveux, péridural et paravertébral</b>", S_CELL_B),
        Spacer(1, 1.5*mm),
        P("Intérêt confirmé d'un cathéter périnerveux en cas de risque de douleur "
          "postopératoire modérée à sévère, notamment chirurgie prothétique de "
          "l'épaule (interscalénique) et du genou (fémoral) : efficacité analgésique "
          "prolongée, épargne opioïde, réduction des NVPO, amélioration du sommeil et "
          "de la satisfaction — mais aucune preuve d'effet sur la chronicisation de la "
          "douleur. Risque de mobilisation du cathéter (5-25 %). Cathéter fémoral : "
          "bloc moteur pouvant favoriser les chutes et gêner la réhabilitation précoce "
          "après prothèse de genou. Cathéter interscalénique : parésie diaphragmatique "
          "à prendre en compte en cas de pathologie respiratoire. <b>Aucune "
          "recommandation formalisée nouvelle</b> sur ce point — la source imprime "
          "« Absence de recommandation » séparément pour le cathétérisme périnerveux "
          "ET pour le cathétérisme péridural/paravertébral (2 mentions distinctes, "
          "rappels méthodologiques uniquement).", S_BODY_SM),
    ]))
    story.append(Spacer(1, 2.5*mm))
    story.append(KeepTogether([
        P("<b>Cathéter d'infiltration du site opératoire</b>", S_CELL_B),
        Spacer(1, 1.5*mm),
        P("De nombreux protocoles d'infiltration sont proposés comme alternative aux "
          "cathéters nerveux périphériques, mais leur efficacité est moindre après la "
          "24<sup>e</sup> heure. Doses maximales d'anesthésiques locaux pour la première injection "
          "chez un adulte jeune ASA 1 :", S_BODY_SM),
        Spacer(1, 1.5*mm),
        _al_dose_table(),
    ]))
    story.append(Spacer(1, 2.5*mm))
    story.append(KeepTogether([
        reco_table([
            ("R4.1", "Il est recommandé de rester en deçà des doses maximales toxiques "
             "d'anesthésiques locaux, en particulier pour les infiltrations "
             "périprothétiques orthopédiques et lors d'association d'infiltrations "
             "cicatricielles et de cathéters périnerveux analgésiques. <i>Accord "
             "fort.</i>", "1+"),
            ("R4.2", "En cas de laparotomie (laparotomie, césarienne et lombotomie) et en "
             "l'absence d'analgésie périmédullaire, il est probablement recommandé de "
             "proposer la mise en place d'un cathéter cicatriciel pour infiltration "
             "continue. <i>Accord fort.</i>", "2+"),
            ("R4.3", "Il n'est pas recommandé de réaliser une infiltration analgésique au "
             "moyen d'un cathéter intra-articulaire en raison du risque toxique des "
             "anesthésiques locaux sur le cartilage (toxicité directe sur les "
             "chondrocytes). <i>Accord fort.</i>", "1-"),
        ]),
    ]))
    story.append(Spacer(1, 4*mm))
    story.extend(_section_sources())
    return story

def _al_dose_table():
    data = [[P("Agent", S_HEAD_W), P("Dose maximale (mg/kg)", S_HEAD_W_C)],
            [P("Lidocaïne adrénalinée", S_CELL), P("7", S_CELL_C)],
            [P("Mépivacaïne", S_CELL), P("5", S_CELL_C)],
            [P("Lévobupivacaïne", S_CELL), P("3", S_CELL_C)],
            [P("Ropivacaïne", S_CELL), P("3", S_CELL_C)]]
    w = PAGE_W - 2*MARGIN
    t = Table(data, colWidths=[w*0.6, w*0.4])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), NAVY), ("TEXTCOLOR", (0,0), (-1,0), WHITE),
        ("FONTNAME", (0,0), (-1,0), FONT_BOLD), ("FONTSIZE", (0,0), (-1,0), 8),
        ("GRID", (0,0), (-1,-1), 0.5, GREY_LIGHT),
        ("TOPPADDING", (0,0), (-1,-1), 3), ("BOTTOMPADDING", (0,0), (-1,-1), 3),
        ("LEFTPADDING", (0,0), (-1,-1), 5),
    ]))
    return t

def _section_sources():
    story = []
    story.append(section_bar("Sources et traçabilité", color=GREY))
    story.append(Spacer(1, 2*mm))
    story.append(P(
        "<b>Document source :</b> « Réactualisation de la recommandation sur la "
        "douleur postopératoire » — Recommandations formalisées d'experts, Société "
        "française d'anesthésie et de réanimation (SFAR). F. Aubrun, K. Nouette "
        "Gaulain, D. Fletcher, A. Belbachir, H. Beloeil, M. Carles, et al. Anesth "
        "Reanim. 2016;2:421-430, doi 10.1016/j.anrea.2016.09.006. Texte validé par le "
        "conseil d'administration de la Sfar le 17/06/2016, disponible sur Internet le "
        "31 octobre 2016.", S_SOURCE))
    story.append(Spacer(1, 1.5*mm))
    story.append(P("<b>Méthodologie :</b> GRADE® — 17 recommandations formalisées "
                    "(R1.1-R1.5, R3.1-R3.9, R4.1-R4.3 ; pas de R2.x, la question du "
                    "monitorage de l'analgésie n'ayant abouti à aucune recommandation "
                    "formalisée). Divergence source-interne sur le décompte agrégé "
                    "forte/faible/avis d'experts — voir disclosure méthodologique en "
                    "page 1.", S_SOURCE))
    story.append(Spacer(1, 1.5*mm))
    story.append(P("<b>Couverture :</b> cette fiche reprend l'intégralité des 17 "
                    "recommandations formalisées et de leurs argumentaires cliniques "
                    "sur les 3 champs traités (évaluation de la DPO, thérapeutiques "
                    "médicamenteuses systémique/orale, anesthésie locale et "
                    "locorégionale postopératoire), y compris le tableau des doses "
                    "maximales d'anesthésiques locaux. Comité d'organisation, groupe "
                    "d'experts, groupe de lecture et les 66 références bibliographiques "
                    "ne sont pas retranscrits (sans contenu clinique actionnable "
                    "au-delà de ce que l'argumentaire cite déjà).", S_SOURCE))
    story.append(Spacer(1, 3*mm))
    story.append(info_panel(P(
        "<b>Avertissement — document de 2016 :</b> ce document est une fiche de "
        "synthèse indépendante, produite pour un usage d'aide-mémoire. Elle reprend "
        "l'intégralité des 17 recommandations du texte source, mais ne remplace pas le "
        "texte intégral (argumentaire complet, 66 références bibliographiques) et "
        "n'est ni éditée ni validée par la SFAR. Ce texte COMPLÈTE (ne remplace pas) la "
        "RFE 2008 sur la douleur postopératoire, déjà couverte séparément dans ce "
        "corpus — se référer aux deux fiches pour une vue complète du sujet, et à un "
        "avis spécialisé en cas de doute.",
        S_BODY_SM), bg=GREY_LIGHT, border=GREY))
    return story

SECTIONS = [
    ("Introduction, méthodologie & légende", _section_intro),
    ("1 — Évaluation de la douleur en périopératoire", _section_eval),
    ("2 — Thérapeutiques médicamenteuses systémique/orale", _section_medoc),
    ("3 — ALR postopératoire & sources", _section_alr),
]

def _make_doc(path=None):
    return SimpleDocTemplate(path or OUT, pagesize=A4,
                              leftMargin=MARGIN, rightMargin=MARGIN,
                              topMargin=32*mm, bottomMargin=16*mm,
                              title="Fiche SFAR 2016 - Reactualisation douleur postoperatoire",
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

    final_story = _build_upto(fns)
    docf = _make_doc()
    docf.build(final_story, onFirstPage=on_page_final, onLaterPages=on_page_final)
    print("OK ->", OUT, f"({total_pages} pages)")

if __name__ == "__main__":
    build()
