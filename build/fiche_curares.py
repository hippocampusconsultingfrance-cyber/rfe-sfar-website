# -*- coding: utf-8 -*-
"""
Fiche de synthese - RFE SFAR 2018 (actualisation de la CC 1999)
Curarisation et decurarisation en anesthesie
Source verifiee : sfar.org (PDF "Curares_2018", texte valide par le CA SFAR le 21/06/2018)
Methodologie GRADE, tags Grade X+/- et "Avis d'experts" imprimes litteralement apres chaque
recommandation (meme convention basse-risque que traumatisme_abdominal/vni). 33 recommandations
numerotees R1.1 a R8.14 (dont 2 avis d'experts, sans grade GRADE) + 5 questions/sous-questions
"PAS DE RECOMMANDATION" (donnees insuffisantes) + 2 algorithmes de decurarisation (neostigmine,
sugammadex, pages 48-49 source, reproduits ici sous forme de tableaux structures fideles au
contenu de l'organigramme). Incoherence arithmetique interne au resume de la source (« trente
recommandations », 11+21 GRADE = 32, +2 avis d'experts = 34, alors que 33 items sont numerotes
R1.1-R8.14) : le resume officiel est cite verbatim dans la fiche plutot que recalcule, conformement
a l'usage etabli sur ce projet (chaque recommandation individuelle reste fidele a son propre tag
litteral). 49 pages source (dont 2 pages d'organigramme quasi sans texte extractible, verifiees et
transcrites) -> couverture complete des 8 questions.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from style import *
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.units import mm

OUT = "/private/tmp/claude-501/-Users-macbook-Downloads-claude/65498e3e-5ddf-47a6-b100-3ac535d1faa0/scratchpad/rfe_sfar/output/Fiche_SFAR_Curares_2018.pdf"

SOURCE_TXT = ("Source : Recommandations Formalisées d'Experts SFAR « Curarisation et décurarisation en "
              "anesthésie » (actualisation de la Conférence de Consensus de 1999) — texte validé par le "
              "Conseil d'Administration de la SFAR le 21 juin 2018. Méthodologie GRADE. "
              "Fiche de synthèse non officielle : se référer au texte intégral.")

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

def no_reco_panel(text):
    return info_panel(P("<b>Absence de recommandation</b> — " + text, S_BODY_SM), bg=GREY_LIGHT, border=GREY)

def legend_flowable():
    items = [("1+", "Il faut faire"), ("1-", "Il ne faut pas faire"),
             ("2+", "Il faut probablement"), ("2-", "Il ne faut probablement pas"),
             ("AE", "Avis d'experts")]
    content_w = PAGE_W - 2*MARGIN
    n = len(items)
    chip_w = 15*mm
    text_w = (content_w - n*chip_w) / n
    row_cells, col_widths = [], []
    for g, txt in items:
        row_cells.append(chip(g, width=chip_w-1.5*mm))
        row_cells.append(P(txt, S_BADGE_HEAD))
        col_widths += [chip_w, text_w]
    row = Table([row_cells], colWidths=col_widths)
    row.setStyle(TableStyle([("VALIGN",(0,0),(-1,-1),"MIDDLE"), ("LEFTPADDING",(0,0),(-1,-1),1), ("RIGHTPADDING",(0,0),(-1,-1),1)]))
    return row

TOTAL_PAGES = {"n": 12}

def on_page(canvas, doc, page_title):
    header_band(canvas, doc, "SFAR — RFE 2018 — FICHE DE SYNTHÈSE",
                "Curarisation et décurarisation",
                page_title, icon_fn=lambda c,x,y: icon_pill(c, x, y, 13*mm), color=NAVY)
    footer_band(canvas, doc, SOURCE_TXT, f"Page {doc.page} / {TOTAL_PAGES['n']}")

# ---------------------------------------------------------------------------
def _section_intro():
    story = []
    story.append(Spacer(1, 3*mm))
    story.append(info_panel(P(
        "<b>Champ :</b> actualisation 2018 de la Conférence de Consensus SFAR de 1999 sur les "
        "indications de la curarisation en anesthésie. Comité de 16 experts, déclaration et suivi "
        "des liens d'intérêts, aucun financement industriel. Méthode GRADE® : chaque question "
        "formulée en format PICO, analyse quantitative de la littérature, force de recommandation "
        "validée par vote Delphi/GRADE Grid (accord fort ≥ 70 %).<br/><br/>"
        "<b>Résultats (texte du résumé officiel, cité verbatim) :</b> « Le travail de synthèse des "
        "experts et l'application de la méthode GRADE ont abouti à trente recommandations. Parmi "
        "les recommandations formalisées, 11 ont un niveau de preuve élevé (GRADE 1+/-) et 21 un "
        "niveau de preuve faible (GRADE 2+/-). Pour deux recommandations, la méthode GRADE ne "
        "pouvait pas s'appliquer, aboutissant à un avis d'experts. […] un accord fort a été obtenu "
        "pour l'ensemble des recommandations. » <i>Le décompte ci-dessus est celui du résumé "
        "officiel, reproduit tel quel malgré une incohérence arithmétique interne à la source "
        "(11+21+2 = 34, pour 33 items effectivement numérotés R1.1 à R8.14 dans le corps du texte) "
        "— chaque recommandation individuelle de cette fiche reste fidèle à son propre tag "
        "littéral, ce qui importe davantage cliniquement que le total agrégé.</i><br/><br/>"
        "<b>La SFAR recommande l'usage d'un dispositif de monitorage de la curarisation au cours "
        "d'une anesthésie générale</b> (conclusion du résumé officiel).",
        S_BODY), bg=BG_PANEL, border=TEAL))
    story.append(Spacer(1, 3*mm))

    story.append(section_bar("Légende des grades (méthodologie GRADE)"))
    story.append(Spacer(1, 2*mm))
    story.append(legend_flowable())
    story.append(Spacer(1, 4*mm))

    story.append(section_bar("Les 8 questions traitées par la RFE"))
    story.append(Spacer(1, 2*mm))
    cw = PAGE_W - 2*MARGIN
    story.append(simple_table(
        ["#", "Question"],
        [
            ["Q1", "Vérifier la ventilation au masque avant curarisation ? Curariser pour faciliter la ventilation au masque ?"],
            ["Q2", "Curariser pour faciliter l'intubation de la trachée ?"],
            ["Q3", "Curariser pour la mise en place et la gestion des complications des dispositifs supra-glottiques ?"],
            ["Q4", "Monitorer la curarisation pour le contrôle des voies aériennes ?"],
            ["Q5", "Curariser pour faciliter les procédures interventionnelles, et lesquelles ?"],
            ["Q6", "Monitorer la curarisation en peropératoire ?"],
            ["Q7", "Stratégies de diagnostic et de traitement de la curarisation résiduelle ?"],
            ["Q8", "Indications et précautions chez les populations spéciales (enfant, obésité, maladies neuromusculaires, ECT, insuffisance rénale/hépatique, sujet âgé) ?"],
        ],
        [cw*0.08, cw*0.92]))
    story.append(Spacer(1, 3*mm))
    story.append(P("<b>Risque allergique</b> — rappel des experts : les curares sont en cause dans plus "
                    "de la moitié des accidents allergiques peranesthésiques en France depuis plus de "
                    "trente ans. Pharmacovigilance française (680 cas confirmés tryptase + tests "
                    "cutanés positifs) : taux de notification succinylcholine 7,05/100 000 "
                    "administrations, rocuronium 4,15/100 000, autres curares entre 0,17 et "
                    "0,36/100 000 — deux groupes distincts (succinylcholine/rocuronium à taux élevé, "
                    "autres curares à taux faible).", S_NOTE))
    return story

def _section_q1_q2():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Question 1 — Ventilation au masque facial"))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("R1.1", "Il n'est probablement pas recommandé de tester la possibilité de ventiler au "
         "masque avant d'administrer un curare.", "2-"),
        ("R1.2", "Il est probablement recommandé d'administrer un curare pour faciliter la "
         "ventilation au masque facial.", "2+"),
    ], [16*mm, PAGE_W-2*MARGIN-16*mm-20*mm, 20*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(P("Tester la ventilation au masque avant curarisation allonge la durée d'induction. "
                    "Le réveil pour intubation impossible est extrêmement rare (2 cas sur ~100 "
                    "intubations difficiles au sein d'une série de 11 257 intubations, et 9 cas "
                    "parmi 698 patients avec ventilation au masque et intubation difficiles dans "
                    "les séries citées). La curarisation "
                    "n'augmente pas systématiquement la durée d'apnée ni le risque de désaturation "
                    "et améliore la ventilation au masque dans plusieurs séries, y compris chez les "
                    "patients à critères de ventilation/intubation difficiles.", S_NOTE))
    story.append(Spacer(1, 4*mm))

    story.append(section_bar("Question 2 — Intubation de la trachée"))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("R2.1", "Il est recommandé d'administrer un curare pour faciliter l'intubation de la "
         "trachée.", "1+"),
        ("R2.2", "Il est recommandé d'administrer un curare pour réduire les traumatismes du "
         "pharynx et/ou du larynx.", "1+"),
        ("R2.3", "Il est probablement recommandé d'administrer un curare à délai d'action court "
         "pour l'induction en séquence rapide.", "2+"),
    ], [16*mm, PAGE_W-2*MARGIN-16*mm-20*mm, 20*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(P("Cohorte de 103 784 patients : mauvaises conditions d'intubation 6,7 % sans curare "
                    "vs 4,5 % avec curare (facteur de risque indépendant d'intubation difficile). Six "
                    "études randomisées (746 patients) : traumatismes pharyngo-laryngés réduits de "
                    "22,6 % à 9,7 % avec curarisation. Méta-analyse Cochrane (50 études, 4 151 "
                    "patients) : la succinylcholine procure d'excellentes conditions d'intubation plus "
                    "souvent que le rocuronium, différence non retrouvée si rocuronium &gt; 0,9 mg/kg "
                    "— hétérogénéité justifiant un GRADE 2.", S_NOTE))
    return story

def _section_q3_q4():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Question 3 — Dispositifs supra-glottiques"))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("R3.1", "Il n'est probablement pas recommandé d'administrer systématiquement un curare "
         "pour faciliter la pose d'un dispositif supra-glottique.", "2-"),
        ("R3.2", "Il est probablement recommandé d'administrer un curare en cas d'obstruction des "
         "voies aériennes liée à un dispositif supra-glottique.", "2+"),
    ], [16*mm, PAGE_W-2*MARGIN-16*mm-20*mm, 20*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(P("<b>Laryngospasme</b> (fermeture glottique complète) : curarisation fortement "
                    "recommandée même si le propofol (0,25-0,8 mg/kg) est efficace dans 77 % des cas. "
                    "Agent de choix : succinylcholine (IV 1 mg/kg ; IM voire sublinguale 4 mg/kg si "
                    "pas d'abord veineux) — associer atropine 0,02 mg/kg chez l'enfant &lt; 3 ans "
                    "pour éviter bradycardie/arrêt cardiaque. Alternative possible : curare non "
                    "dépolarisant à faible dose (rocuronium ou atracurium 0,1-0,2 mg/kg) si "
                    "profondeur d'anesthésie suffisante.", S_NOTE))
    story.append(Spacer(1, 4*mm))

    story.append(section_bar("Question 4 — Monitorage et contrôle des voies aériennes"))
    story.append(Spacer(1, 2*mm))
    story.append(no_reco_panel("Les données de la littérature sont insuffisantes pour établir une "
                                "recommandation sur l'utilisation d'un monitorage instrumental de la "
                                "curarisation lors de l'intubation de la trachée."))
    story.append(Spacer(1, 3*mm))
    story.append(reco_table([
        ("R4.1", "Les experts suggèrent que si un monitorage instrumental de la curarisation est "
         "utilisé, le muscle sourcilier soit le site utilisé du fait de sa sensibilité aux curares "
         "et de sa cinétique de curarisation comparables à celles des muscles laryngés.", "AE"),
    ], [16*mm, PAGE_W-2*MARGIN-16*mm-20*mm, 20*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(P("Les conditions d'intubation sont moins bonnes lorsque l'orbiculaire de l'œil "
                    "(plus sensible aux curares) est utilisé pour décider du moment de "
                    "l'intubation, comparé au muscle sourcilier ou à l'adducteur du pouce.", S_NOTE))
    return story

def _section_q5_q6():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Question 5 — Procédures interventionnelles"))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("R5.1", "Il est recommandé d'administrer un curare pour faciliter l'acte opératoire en "
         "chirurgie abdominale par laparotomie ou par laparoscopie.", "1+"),
        ("R5.2", "Il est probablement recommandé d'administrer un curare pour faciliter l'acte "
         "opératoire en chirurgie ORL sous laser.", "2+"),
    ], [16*mm, PAGE_W-2*MARGIN-16*mm-20*mm, 20*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(no_reco_panel("Les données de la littérature sont insuffisantes pour établir une "
                                "recommandation sur le niveau de bloc neuromusculaire à atteindre "
                                "(modéré versus profond) en chirurgie abdominale par laparotomie ou "
                                "par laparoscopie."))
    story.append(Spacer(1, 2*mm))
    story.append(P("Bloc modéré = 1-2 réponses au train de quatre (TDQ) à l'adducteur du pouce ; "
                    "bloc profond = compte post-tétanique (CPT) ≤ 5, 0 réponse au TDQ. Un patient sur "
                    "quatre bénéficierait du bloc profond en termes de conditions opératoires (études "
                    "à faibles effectifs, n = 24-102), sans différence démontrée sur la morbidité "
                    "chirurgicale. Chirurgie laryngée sous laser : curarisation profonde associée à une "
                    "meilleure exposition du champ, moins de mouvements des cordes vocales et moins de "
                    "sécheresse buccale postopératoire, sans différence sur les événements "
                    "indésirables.", S_NOTE))
    story.append(Spacer(1, 4*mm))

    story.append(section_bar("Question 6 — Monitorage peropératoire"))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("R6.1", "Il est recommandé de monitorer la curarisation en peropératoire.", "1+"),
        ("R6.2", "Il est probablement recommandé d'utiliser la stimulation par train de quatre du "
         "nerf ulnaire à l'adducteur du pouce pour monitorer la curarisation peropératoire.", "2+"),
    ], [16*mm, PAGE_W-2*MARGIN-16*mm-20*mm, 20*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(P("Recommandation applicable en salle d'intervention et en SSPI. Pour une "
                    "curarisation profonde (diaphragme, paroi abdominale), attendre la disparition "
                    "des 4 réponses au TDQ puis monitorer par CPT (1 à 5 réponses = paralysie "
                    "complète des muscles abdominaux). Alternative : stimulation du nerf facial / "
                    "muscle sourcilier (cinétique comparable aux muscles résistants) si accès aux "
                    "membres supérieurs impossible. En fin d'intervention, basculer dès que possible "
                    "sur l'adducteur du pouce pour quantifier la décurarisation.", S_NOTE))
    return story

def _section_q7_diag():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Question 7 — Curarisation résiduelle : diagnostic"))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("R7.1", "Il est probablement recommandé d'utiliser un monitorage quantitatif de la "
         "curarisation à l'adducteur du pouce pour le diagnostic de la curarisation résiduelle et "
         "d'obtenir un rapport T4/T1 ≥ 0,9 à l'adducteur du pouce pour éliminer formellement le "
         "diagnostic de curarisation résiduelle.", "2+"),
    ], [16*mm, PAGE_W-2*MARGIN-16*mm-20*mm, 20*mm]))
    story.append(Spacer(1, 3*mm))
    story.append(info_panel(P(
        "<b>Aucun test clinique n'est suffisamment sensible</b> pour dépister une curarisation "
        "résiduelle. Seul le monitorage instrumental quantitatif (rapport T4/T1, stimulation "
        "supramaximale, adducteur du pouce) permet de l'évaluer. Conséquences documentées d'une "
        "curarisation résiduelle non traitée : morbi-mortalité accrue dans les 24 premières heures "
        "postopératoires, risque accru d'événements respiratoires critiques en SSPI, risque accru "
        "de pneumopathie postopératoire, dysfonction des muscles pharyngés, prolongation de la "
        "durée de séjour en SSPI.",
        S_BODY), bg=RED_LIGHT, border=RED))
    return story

def _section_q7_neostigmine():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Question 7 — Décurarisation par la néostigmine"))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("R7.2", "Il est recommandé après l'administration d'un curare non dépolarisant d'attendre "
         "une décurarisation spontanée égale à quatre réponses musculaires à l'adducteur du pouce "
         "après une stimulation en train de quatre au nerf ulnaire avant d'injecter de la "
         "néostigmine.", "1+"),
        ("R7.3", "Il est recommandé d'administrer la néostigmine sous couvert d'un monitorage de la "
         "curarisation à l'adducteur du pouce, d'administrer une dose comprise entre 40 et 50 "
         "µg/kg adaptée à la masse idéale, de ne pas augmenter la dose au-delà et de ne pas "
         "l'administrer en l'absence de bloc résiduel.", "1+"),
        ("R7.4", "Il est probablement recommandé de réduire la dose de néostigmine de moitié en cas "
         "de bloc résiduel très faible.", "2+"),
        ("R7.5", "Il est recommandé de poursuivre le monitorage quantitatif de la curarisation après "
         "l'administration de la néostigmine jusqu'à l'obtention d'un rapport du train de quatre "
         "supérieur ou égal à 0,9.", "1+"),
    ], [16*mm, PAGE_W-2*MARGIN-16*mm-20*mm, 20*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(P("La néostigmine administrée après récupération complète (TDQ = 100 %) augmente la "
                    "pression de fermeture des voies aériennes supérieures et réduit l'activité du "
                    "muscle génio-glosse : elle diminue la perméabilité pharyngée si administrée hors "
                    "bloc résiduel. À l'inverse, une dose trop élevée pour un bloc très superficiel "
                    "peut altérer la transmission neuromusculaire (fatigue au TDQ) si administrée "
                    "après récupération spontanée &gt; 90 %.", S_NOTE))
    story.append(Spacer(1, 4*mm))

    story.append(section_bar("Algorithme 1 — Décurarisation avec la néostigmine", color=GREY))
    story.append(Spacer(1, 1.5*mm))
    story.append(P("Après curare non dépolarisant (benzylisoquinoline ou stéroïdien). "
                    "TDQ = stimulation en train de quatre à l'adducteur du pouce (AP), N = nombre de "
                    "réponses (0 à 4).", S_NOTE))
    story.append(Spacer(1, 2*mm))
    cw = PAGE_W - 2*MARGIN
    story.append(simple_table(
        ["Évaluation initiale", "Conduite à tenir", "Résultat attendu"],
        [
            ["N &lt; 4 réponses au TDQ", "Attendre et maintenir l'anesthésie, recontrôler plus tard "
             "le TDQ", "—"],
            ["N = 4 réponses au TDQ", "Néostigmine 0,04 mg/kg + atropine 0,02 mg/kg", "Rapport TDQ "
             "≥ 0,9 en 10 à 20 minutes"],
        ],
        [cw*0.28, cw*0.44, cw*0.28]))
    return story

def _section_q7_sugammadex():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Question 7 — Décurarisation par le sugammadex"))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("R7.6", "Il est recommandé d'ajuster la dose de sugammadex sur la masse idéale et en "
         "fonction du degré de bloc neuromusculaire induit par le rocuronium.", "1+"),
        ("R7.7", "Il est probablement recommandé de poursuivre le monitorage quantitatif de la "
         "curarisation après l'administration de sugammadex afin de détecter une recurarisation.", "2+"),
    ], [16*mm, PAGE_W-2*MARGIN-16*mm-20*mm, 20*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(P("Le sugammadex (gamma-cyclodextrine) n'encapsule que les curares stéroïdiens "
                    "(rocuronium, vécuronium), une molécule pour une molécule : plus le bloc "
                    "stéroïdien est profond, plus la dose nécessaire est élevée. Une dose "
                    "insuffisante expose à une recurarisation. Efficacité ralentie chez le patient "
                    "âgé et en cas d'insuffisance rénale sévère (clairance de la créatinine "
                    "&lt; 30 mL/min), particulièrement pour la décurarisation d'un bloc profond.", S_NOTE))
    story.append(Spacer(1, 3*mm))
    cw = PAGE_W - 2*MARGIN
    story.append(simple_table(
        ["Degré de bloc (rocuronium)", "Dose de sugammadex", "Délai d'efficacité (TDQ &gt; 0,9)"],
        [
            ["Très modéré (TDQ = 50 %)", "0,22 mg/kg", "&lt; 5 min (95 % des patients)"],
            ["Modéré (4 réponses au TDQ)", "1 mg/kg (0,5 mg/kg efficace mais plus lent)", "&lt; 5 min "
             "(10 min à 0,5 mg/kg)"],
            ["Modéré (2 réponses au TDQ)", "≥ 2 mg/kg", "&lt; 5 min"],
            ["Profond (1-2 réponses au compte post-tétanique)", "≥ 4 mg/kg", "&lt; 5 min"],
            ["Très profond (3-15 min après forte dose de rocuronium)", "≥ 8 mg/kg", "&lt; 5 min"],
        ],
        [cw*0.34, cw*0.34, cw*0.32]))
    story.append(Spacer(1, 4*mm))

    story.append(section_bar("Algorithme 2 — Décurarisation avec le sugammadex", color=GREY))
    story.append(Spacer(1, 1.5*mm))
    story.append(P("Uniquement avec le rocuronium. AP = adducteur du pouce, CPT = compte "
                    "post-tétanique.", S_NOTE))
    story.append(Spacer(1, 2*mm))
    story.append(simple_table(
        ["Évaluation initiale", "Conduite à tenir", "Résultat attendu"],
        [
            ["N ≥ 2 réponses au TDQ à l'AP", "Sugammadex 2 mg/kg", "Rapport TDQ &gt; 0,9 en 3 à "
             "5 minutes"],
            ["N = 0, CPT = 1 ou 2", "Sugammadex 4 mg/kg", "Rapport TDQ &gt; 0,9 en 3 à 5 minutes"],
            ["N = 0, CPT = 0", "Attendre et maintenir l'anesthésie, recontrôler le CPT plus tard — ou "
             "décurarisation immédiate : sugammadex 8-16 mg/kg", "Rapport TDQ &gt; 0,9 en 3 à "
             "5 minutes"],
        ],
        [cw*0.28, cw*0.44, cw*0.28]))
    return story

def _section_q8_ect_obesite():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Question 8 — Populations spéciales : ECT et obésité"))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("R8.1", "Il est probablement recommandé d'administrer un curare à délai d'action court "
         "pour l'électro-convulsivothérapie.", "2+"),
    ], [16*mm, PAGE_W-2*MARGIN-16*mm-20*mm, 20*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(P("Objectif : prévenir les conséquences motrices de la convulsion généralisée "
                    "(morsure de langue, chute, luxation, fracture). Succinylcholine recommandée en "
                    "première intention ; en cas de contre-indication formelle, l'association "
                    "rocuronium-sugammadex a été proposée à partir de séries de cas.", S_NOTE))
    story.append(Spacer(1, 4*mm))

    story.append(reco_table([
        ("R8.2", "Il est probablement recommandé chez l'obèse massif (IMC ≥ 40 kg/m²) d'administrer "
         "un curare à délai d'action court pour faciliter l'intubation de la trachée.", "2+"),
        ("R8.3", "Il est probablement recommandé d'administrer la succinylcholine à la dose de "
         "1 mg/kg adaptée sur la masse réelle de l'obèse.", "2+"),
        ("R8.4", "Les experts suggèrent d'administrer le curare non dépolarisant à une dose calculée "
         "sur la masse maigre du patient obèse.", "AE"),
    ], [16*mm, PAGE_W-2*MARGIN-16*mm-20*mm, 20*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(no_reco_panel("Les données sont insuffisantes pour formuler des recommandations sur "
                                "l'intérêt du bloc profond en chirurgie par laparoscopie chez l'obèse."))
    story.append(Spacer(1, 3*mm))
    story.append(reco_table([
        ("R8.5", "Il est probablement recommandé d'utiliser le sugammadex adapté à la masse idéale "
         "en cas d'utilisation de rocuronium chez l'obèse massif (IMC ≥ 40 kg/m²) compte tenu de "
         "l'allongement du délai de décurarisation et du risque de recurarisation avec la "
         "néostigmine.", "2+"),
    ], [16*mm, PAGE_W-2*MARGIN-16*mm-20*mm, 20*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(P("Succinylcholine sur masse réelle : conditions d'intubation excellentes et "
                    "reproductibles (posologie sur masse idéale/maigre associée à de mauvaises "
                    "conditions). Curares non dépolarisants et décurarisants : hydrosolubles, dose "
                    "calculée sur la masse maigre (formule de Janmahasatian), augmentée chez l'obèse. "
                    "Sugammadex chez l'obèse massif : 2 mg/kg sur masse idéale majorée de 40 % pour un "
                    "bloc partiel (2 réponses au TDQ), 4 mg/kg pour un bloc profond (absence de "
                    "réponse au TDQ).", S_NOTE))
    return story

def _section_q8_enfant():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Question 8 — Populations spéciales : l'enfant"))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("R8.6", "Hors situations relevant d'une indication à une induction à séquence rapide et à "
         "l'utilisation d'un curare dépolarisant, il est probablement recommandé d'utiliser un "
         "curare non dépolarisant pour améliorer les conditions d'intubation au cours de "
         "l'anesthésie générale par induction intraveineuse chez l'enfant.", "2+"),
        ("R8.7", "Dans l'induction en séquence rapide classique, il est recommandé d'utiliser un "
         "curare d'action rapide chez l'enfant.", "1+"),
        ("R8.8", "Dans l'induction en séquence rapide classique, il est probablement recommandé "
         "d'utiliser chez l'enfant la succinylcholine en première intention pour l'induction en "
         "séquence rapide. En cas de contre-indication à la succinylcholine, il est probablement "
         "recommandé d'utiliser du rocuronium.", "2+"),
    ], [16*mm, PAGE_W-2*MARGIN-16*mm-20*mm, 20*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(no_reco_panel("Les données sont insuffisantes chez l'enfant pour formuler des "
                                "recommandations concernant l'administration de curare pour faciliter "
                                "la ventilation au masque facial, la mise en place et la gestion des "
                                "complications des dispositifs supra-glottiques, faciliter le geste "
                                "chirurgical, l'intérêt du monitorage de la curarisation pour "
                                "l'intubation de la trachée et en peropératoire, le diagnostic et le "
                                "traitement de la curarisation résiduelle."))
    story.append(Spacer(1, 3*mm))
    cw = PAGE_W - 2*MARGIN
    story.append(simple_table(
        ["Âge", "Dose de succinylcholine (ISR)"],
        [
            ["&lt; 1 mois", "1,8 mg/kg"],
            ["1 mois - 1 an", "2 mg/kg"],
            ["1 an - 10 ans", "1,2 mg/kg"],
            ["&gt; 10 ans", "1 mg/kg"],
        ],
        [cw*0.4, cw*0.6]))
    story.append(Spacer(1, 2*mm))
    story.append(P("Rocuronium (alternative si CI à la succinylcholine) : &gt; 0,9 mg/kg selon la "
                    "revue Cochrane citée (posologies de 0,6-0,9 mg/kg également rapportées) ; "
                    "sugammadex non autorisé en 2018 chez l'enfant de moins de 2 ans. Contre-"
                    "indications à la succinylcholine : risque d'hyperthermie maligne, pathologies "
                    "musculaires à risque de rhabdomyolyse, hyperkaliémie, allergie, situations à "
                    "risque d'hyperkaliémie. Alerte ANSM du 15/12/2017 : un curare dépolarisant ne "
                    "doit pas être utilisé pour une induction intraveineuse ne relevant pas d'une "
                    "induction en séquence rapide.", S_NOTE))
    return story

def _section_q8_neuromusculaire():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Question 8 — Populations spéciales : maladies neuromusculaires"))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("R8.9", "Il n'est pas recommandé d'utiliser la succinylcholine en cas d'atteinte musculaire "
         "primitive (myopathies) ou de dérégulation haute du récepteur nicotinique à l'acétylcholine "
         "de la plaque motrice (déficit moteur chronique).", "1-"),
        ("R8.10", "Il est probablement recommandé de monitorer la curarisation en cas "
         "d'administration de curare chez un patient atteint d'une maladie neuromusculaire.", "2+"),
        ("R8.11", "Il est probablement recommandé d'administrer du sugammadex pour le traitement "
         "d'une curarisation résiduelle en cas d'administration de curare stéroïdien chez un "
         "patient atteint d'une maladie neuromusculaire.", "2+"),
    ], [16*mm, PAGE_W-2*MARGIN-16*mm-20*mm, 20*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(info_panel(P(
        "<b>Succinylcholine formellement contre-indiquée</b> : atteintes musculaires pures "
        "(myopathie, myotonie) → contracture généralisée avec rhabdomyolyse ; dérégulation haute du "
        "récepteur nicotinique (lésion chronique du moto-neurone, brûlures étendues, séjour "
        "prolongé en réanimation) → hyperkaliémie engageant le pronostic vital, pendant une durée "
        "prolongée après la constitution de la lésion.",
        S_BODY), bg=RED_LIGHT, border=RED))
    story.append(Spacer(1, 2*mm))
    story.append(P("Myasthénie (dérégulation basse) : curares non contre-indiqués mais résistance à "
                    "la succinylcholine, sensibilité accrue et durée d'action allongée pour les "
                    "curares non dépolarisants (réduction habituelle de 50-75 % des doses "
                    "d'atracurium/cis-atracurium). Dystrophie musculaire de Duchenne : sensibilité "
                    "très augmentée au rocuronium (délai d'installation et récupération "
                    "significativement plus longs).", S_NOTE))
    return story

def _section_q8_ir_ih():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Question 8 — Insuffisance rénale, hépatique, sujet âgé"))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("R8.12", "Il est probablement recommandé d'utiliser un curare de type benzylisoquinolines "
         "(atracurium/cis-atracurium) en cas d'insuffisance rénale ou hépatique.", "2+"),
        ("R8.13", "Il est recommandé de ne pas modifier la dose initiale en cas d'insuffisance "
         "rénale ou hépatique quel que soit le type de curare.", "1+"),
        ("R8.14", "En cas d'utilisation du sugammadex chez l'insuffisant rénal, il est probablement "
         "recommandé de l'utiliser aux doses habituelles.", "2+"),
    ], [16*mm, PAGE_W-2*MARGIN-16*mm-20*mm, 20*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(no_reco_panel("Les données de la littérature sont insuffisantes pour établir une "
                                "recommandation sur l'utilisation des curares chez le sujet âgé."))
    story.append(Spacer(1, 3*mm))
    story.append(P("Rocuronium : élimination rénale et biliaire, clairance réduite chez l'insuffisant "
                    "rénal et variabilité accrue chez le cirrhotique. Atracurium/cis-atracurium : "
                    "élimination majoritairement non organique (réaction d'Hofmann, hydrolyse "
                    "estérasique) → pharmacocinétique similaire quelle que soit la fonction "
                    "rénale/hépatique ; le métabolite laudanosine s'accumule en insuffisance rénale "
                    "sans effet indésirable démontré même après 72 h de perfusion. Sugammadex éliminé "
                    "par le rein, s'accumule en insuffisance rénale mais efficacité préservée aux "
                    "doses habituelles, sans recurarisation observée ; dialysable (ainsi que le "
                    "complexe sugammadex-rocuronium).", S_NOTE))
    return story

def _section_synthese():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Synthèse et messages clés"))
    story.append(Spacer(1, 2*mm))
    story.append(P(
        "• La curarisation facilite la ventilation au masque, l'intubation trachéale (réduction des "
        "traumatismes pharyngo-laryngés) et l'acte opératoire en chirurgie abdominale — sans tester "
        "systématiquement la ventilation au masque au préalable.<br/>"
        "• Le monitorage quantitatif de la curarisation (adducteur du pouce, TDQ) est recommandé en "
        "peropératoire et indispensable pour poser ou éliminer le diagnostic de curarisation "
        "résiduelle (T4/T1 ≥ 0,9).<br/>"
        "• Néostigmine : n'attendre le retour d'au moins 4 réponses au TDQ, dose 40-50 µg/kg sur "
        "masse idéale, jamais au-delà, jamais en l'absence de bloc résiduel.<br/>"
        "• Sugammadex : dose ajustée sur la masse idéale et le degré de bloc (rocuronium "
        "uniquement) ; efficacité ralentie chez le sujet âgé et en insuffisance rénale sévère.<br/>"
        "• Monitorage quantitatif à poursuivre après toute décurarisation pharmacologique, quel que "
        "soit l'agent, pour détecter une recurarisation.<br/>"
        "• Succinylcholine formellement contre-indiquée en cas de myopathie ou de dérégulation "
        "haute du récepteur nicotinique (brûlures étendues, lésion neurologique chronique, "
        "réanimation prolongée) — risque d'hyperkaliémie engageant le pronostic vital.",
        S_BODY))
    story.append(Spacer(1, 5*mm))

    story.append(section_bar("Sources et traçabilité", color=GREY))
    story.append(Spacer(1, 2*mm))
    story.append(P(
        "<b>Document source :</b> « Curarisation et décurarisation en anesthésie » (actualisation de "
        "la Conférence de Consensus SFAR de 1999) — Recommandations Formalisées d'Experts, Société "
        "Française d'Anesthésie et de Réanimation. Comité de consensus de 16 experts, coordination "
        "C. Baillard, B. Debaene, B. Plaud. Texte validé par le Conseil d'Administration de la SFAR "
        "le 21 juin 2018.", S_SOURCE))
    story.append(Spacer(1, 1.5*mm))
    story.append(P("<b>Méthodologie :</b> GRADE®, tags Grade 1+/1-/2+/2- et « Avis d'experts » imprimés "
                    "littéralement après chaque recommandation dans le texte source — cités ici tels "
                    "quels, sans convention à déduire.", S_SOURCE))
    story.append(Spacer(1, 1.5*mm))
    story.append(P("<b>Couverture :</b> 33 recommandations numérotées (R1.1 à R8.14, dont 2 avis "
                    "d'experts) et 5 questions/sous-questions « pas de recommandation » reproduites "
                    "intégralement, ainsi que les 2 algorithmes de décurarisation (néostigmine, "
                    "sugammadex ; pages 48-49 de la source, pages d'organigramme à faible contenu "
                    "textuel extractible, vérifiées visuellement et reproduites ici sous forme de "
                    "tableaux structurés fidèles au contenu).", S_SOURCE))
    story.append(Spacer(1, 3*mm))
    story.append(info_panel(P(
        "<b>Avertissement :</b> ce document est une fiche de synthèse indépendante, produite pour un "
        "usage d'aide-mémoire. Il reprend l'intégralité des recommandations de la RFE mais ne "
        "remplace pas le texte intégral et n'est ni édité ni validé par la SFAR. En cas de doute, se "
        "référer au texte intégral, aux recommandations ultérieures et/ou à un avis spécialisé.",
        S_BODY_SM), bg=GREY_LIGHT, border=GREY))
    return story

SECTIONS = [
    ("Introduction, méthodologie & plan", _section_intro),
    ("Q1-Q2 — Ventilation au masque & intubation", _section_q1_q2),
    ("Q3-Q4 — Dispositifs supra-glottiques & monitorage VAS", _section_q3_q4),
    ("Q5-Q6 — Procédures interventionnelles & monitorage peropératoire", _section_q5_q6),
    ("Q7 (1/3) — Curarisation résiduelle : diagnostic", _section_q7_diag),
    ("Q7 (2/3) — Décurarisation par la néostigmine", _section_q7_neostigmine),
    ("Q7 (3/3) — Décurarisation par le sugammadex", _section_q7_sugammadex),
    ("Q8 (1/4) — Électro-convulsivothérapie & obésité", _section_q8_ect_obesite),
    ("Q8 (2/4) — L'enfant", _section_q8_enfant),
    ("Q8 (3/4) — Maladies neuromusculaires", _section_q8_neuromusculaire),
    ("Q8 (4/4) — Insuffisance rénale, hépatique, sujet âgé", _section_q8_ir_ih),
    ("Synthèse, sources & traçabilité", _section_synthese),
]

def _make_doc():
    return SimpleDocTemplate(OUT, pagesize=A4,
                              leftMargin=MARGIN, rightMargin=MARGIN,
                              topMargin=32*mm, bottomMargin=16*mm,
                              title="Fiche SFAR 2018 - Curarisation et decurarisation en anesthesie",
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
