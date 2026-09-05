# -*- coding: utf-8 -*-
"""
Fiche de synthese - SFAR RFE, "Recommandations pour la prise en charge du SDRA"
Texte valide par le Comite des Referentiels Cliniques SFAR (12/12/2017) et le CA SFAR
(02/02/2018). IMPORTANT particularite de ce document, distincte de tout le reste du corpus :
il ne s'agit PAS d'une RFE originale redigee par un comite d'experts SFAR, mais de la
"traduction resumee" officielle par la SFAR d'un guideline international deja publie :
An Official American Thoracic Society/European Society of Intensive Care Medicine/Society of
Critical Care Medicine Clinical Practice Guideline: Mechanical Ventilation in Adult Patients
with Acute Respiratory Distress Syndrome (Am J Respir Crit Care Med 2017;195(9):1253-1263,
incluant erratum 2017;195(11):1540), realisee par le comite Reanimation de la SFAR sous la
responsabilite de M. Garnier, M. Jabaudon, A. Monsel, C. Quesnel, J-M. Constantin. Ceci est
explicitement disclose dans la fiche (page de garde du texte source lui-meme).

19 pages source (hors page de garde), PyMuPDF confirme 21 pages au total. Contenu
exceptionnellement compact pour ce corpus : seulement 5 recommandations numerotees (R1-R5) +
1 absence de recommandation explicite (Q6, ECMO) - 6 questions au total, mon propre inventaire
independant concorde exactement avec la structure du texte (aucun mismatch d'agregat, la source
ne fournit d'ailleurs pas de resume chiffre "X recommandations" comme les autres RFE du corpus
puisqu'il s'agit d'une traduction et non d'un texte SFAR natif). AUCUNE figure, tableau ou
algorithme dans ce document (verifie par lecture integrale des 21 pages) - contenu purement
narratif/textuel (Rationnel / Resume des connaissances / Justification et considerations
d'applicabilite / Orientation des recherches futures pour chaque question), avec des statistiques
tres precises (RR, IC95%, nombre d'etudes/patients) condensees ici en notes structurees plutot
que retranscrites integralement (le texte source de chaque question fait 1 a 2 pages pleines de
prose).

Particularite methodologique disclosee explicitement en page 4 du texte source lui-meme ("Note
des traducteurs") : contrairement a la version originale anglaise, la traduction francaise a
delibErement omis de reporter la confiance globale dans l'estimation de l'effet
(Haute/Moderee/Basse/Tres basse) a la fin de chaque recommandation, par souci de simplification
et conformite au format RFE SFAR standard ou cette gradation globale n'apparait pas - mais cette
confiance est preservee dans le texte du "Resume des connaissances" pour chaque critere de
jugement detaille (et donc bien presente dans cette fiche via les notes S_NOTE qui citent le
niveau de confiance associe a chaque statistique).

Grading : GRADE 1+/1-/2+/2- standard (pas de particularite de signe comme sur d'autres fiches de
ce corpus) - R1=1+, R2=1+, R3=1-, R4=2+, R5=2+, Q6=absence de recommandation. Poids theorique
(formules de Devine, utilisees pour le reglage du Vt) reproduites verbatim car directement
utiles au lit du patient : Homme = 50 + 0,91x[taille(cm)-152,4] ; Femme = 45,5 +
0,91x[taille(cm)-152,4].

Minor source-internal typo (not disclosed as a major finding, silently normalized): the source
uses both "VOHF" (Question 3 heading, most occurrences) and "VHFO" (R3's own recommendation
sentence) for the same abbreviation (Ventilation par Oscillations a Haute Frequence) - a letter-
transposition typo, not a substantive content difference. Normalized to "VOHF" throughout this
fiche for consistency, per the same logic already applied project-wide to genuine OCR/extraction
artifacts (unlike substantive source-internal quirks, this is disclosed here in-code only, not
in the fiche's own traçabilité section, since it changes no clinical content).
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from style import *
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.units import mm

OUT = "/private/tmp/claude-501/-Users-macbook-Downloads-claude/65498e3e-5ddf-47a6-b100-3ac535d1faa0/scratchpad/rfe_sfar/output/Fiche_SFAR_SDRA_2018.pdf"

SOURCE_TXT = ("Source : SFAR, « Recommandations pour la prise en charge du SDRA » — traduction "
              "résumée officielle de : An Official ATS/ESICM/SCCM Clinical Practice Guideline: "
              "Mechanical Ventilation in Adult Patients with ARDS (Am J Respir Crit Care Med "
              "2017;195(9):1253-1263). Texte validé par le Comité des Référentiels Cliniques "
              "SFAR (12/12/2017) et le CA SFAR (02/02/2018). Fiche de synthèse non officielle : "
              "se référer au texte intégral.")

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
    header_band(canvas, doc, "SFAR — TRADUCTION ATS/ESICM/SCCM 2017 — FICHE DE SYNTHÈSE",
                "SDRA — Ventilation mécanique",
                page_title, icon_fn=lambda c,x,y: icon_shield(c, x, y, 13*mm), color=NAVY)
    footer_band(canvas, doc, SOURCE_TXT, f"Page {doc.page} / {TOTAL_PAGES['n']}")

# ---------------------------------------------------------------------------
def _section_intro():
    story = []
    story.append(Spacer(1, 3*mm))
    story.append(info_panel(P(
        "<b>Nature de ce document :</b> il ne s'agit pas d'une RFE rédigée par un comité "
        "d'experts SFAR, mais de la <b>traduction résumée officielle par la SFAR</b> d'un "
        "guideline international déjà publié : <i>An Official American Thoracic Society / "
        "European Society of Intensive Care Medicine / Society of Critical Care Medicine "
        "Clinical Practice Guideline: Mechanical Ventilation in Adult Patients with Acute "
        "Respiratory Distress Syndrome</i> (Am J Respir Crit Care Med 2017;195(9):1253-1263, "
        "incluant l'erratum 2017;195(11):1540). Traduction réalisée par le comité Réanimation "
        "de la SFAR sous la responsabilité de M. Garnier, M. Jabaudon, A. Monsel, C. Quesnel, "
        "J-M. Constantin ; texte validé par le Comité des Référentiels Cliniques (12/12/2017) "
        "et le CA SFAR (02/02/2018).<br/><br/>"
        "<b>Champ :</b> stratégies ventilatoires chez l'adulte atteint de SDRA — 6 questions, "
        "méthode GRADE, comité international ATS/ESICM/SCCM (cliniciens, épidémiologistes, "
        "méthodologistes), revue systématique (MEDLINE, EMBASE, Cochrane, DARE, CINAHL, Web of "
        "Science) jusqu'à août 2016, méta-analyses sous RevMan 5.2. <b>Ces recommandations ne "
        "concernent que la prise en charge ventilatoire du SDRA et ne sont pas extrapolables "
        "aux autres causes d'insuffisance respiratoire aiguë.</b>",
        S_BODY), bg=BG_PANEL, border=TEAL))
    story.append(Spacer(1, 3*mm))
    cw = PAGE_W - 2*MARGIN
    story.append(simple_table(
        ["Sévérité du SDRA", "Rapport PaO2/FiO2"],
        [
            ["Léger", "201 à 300 mmHg"],
            ["Modéré", "101 à 200 mmHg"],
            ["Sévère", "≤ 100 mmHg"],
        ],
        [cw*0.5, cw*0.5]))
    story.append(Spacer(1, 3*mm))
    story.append(info_panel(P(
        "<b>Terminologie GRADE :</b> recommandation forte = « il est recommandé » de faire "
        "(GRADE 1+) ou de ne pas faire (GRADE 1-) ; recommandation faible/optionnelle = "
        "« il est probablement recommandé » de faire (GRADE 2+) ou de ne pas faire (GRADE 2-). "
        "Deux recommandations de force identique ne sont pas nécessairement équivalentes : la "
        "force résulte du niveau de preuve, de l'ampleur de l'effet, de la balance "
        "bénéfice/risque, des préférences et des coûts pris ensemble — deux recommandations "
        "« faibles » peuvent l'être pour des raisons très différentes. <b>Note des "
        "traducteurs :</b> par simplification et conformité au format RFE SFAR, la confiance "
        "globale dans l'estimation de l'effet (Haute/Modérée/Basse/Très basse) n'est pas "
        "reportée en fin d'énoncé comme dans la version originale anglaise, mais elle reste "
        "précisée dans le texte du « résumé des connaissances » pour chaque critère de "
        "jugement — et donc citée dans les notes ci-dessous.",
        S_BODY_SM), bg=AMBER_LIGHT, border=AMBER))
    story.append(Spacer(1, 3*mm))
    story.append(info_panel(P(
        "<b>Poids théorique (PT), pour le réglage du volume courant :</b><br/>"
        "• Homme : PT (kg) = 50 + 0,91 × [taille (cm) − 152,4]<br/>"
        "• Femme : PT (kg) = 45,5 + 0,91 × [taille (cm) − 152,4]",
        S_BODY_SM), bg=BG_PANEL, border=TEAL))
    return story

def _section_q1q2():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Volumes courants/pression de plateau & décubitus ventral"))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("R1", "Il est recommandé que les patients adultes atteints de SDRA soient ventilés "
         "avec une stratégie limitant le volume courant (Vt 4-8 mL/kg de poids théorique) et "
         "la pression de plateau (Pplat &lt; 30 cmH2O).", "1+"),
        ("R2", "Il est recommandé que les patients adultes atteints de SDRA sévère soient "
         "positionnés en décubitus ventral pendant plus de 12 heures par jour.", "1+"),
    ], [12*mm, PAGE_W-2*MARGIN-12*mm-20*mm, 20*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(P("<b>R1</b> — 9 ECR, 1629 patients ; Vt moyen 6,2±1,2 (faible Vt) vs. "
                    "11,4±1,1 mL/kg PT (conventionnel). Analyse principale (7 études, 1481 "
                    "patients, excluant les co-interventions PEP élevée) : pas de différence de "
                    "mortalité (RR 0,87 IC95 [0,70-1,08], confiance modérée). Analyse de "
                    "sensibilité incluant les 9 études (1629 patients) : réduction significative "
                    "de mortalité (RR 0,80 IC95 [0,66-0,98]) ; méta-régression confirmant une "
                    "relation dose-effet entre delta de Vt et réduction du risque relatif de "
                    "mortalité. Réglage initial : Vt 6 mL/kg PT, ajustable jusqu'à 8 mL/kg en "
                    "cas de double déclenchement ou de pression des voies aériennes sous la PEP.<br/>"
                    "<b>R2</b> — 8 ECR, 2129 patients. Pas de différence de mortalité en analyse "
                    "globale (RR 0,84 IC95 [0,68-1,04], confiance modérée), mais bénéfice net en "
                    "sous-groupes : décubitus ventral &gt;12h/j (5 études, 1002 patients, RR 0,74 "
                    "IC95 [0,56-0,99], confiance élevée) et SDRA modéré/sévère (5 études, 1006 "
                    "patients, RR 0,74 IC95 [0,54-0,99], confiance modérée) — confirmé par "
                    "l'étude PROSEVA (PaO2/FiO2 initial 100±30 mmHg). Complications : obstruction "
                    "de sonde d'intubation (RR 1,76 IC95 [1,24-2,50]) et lésions cutanées d'appui "
                    "(RR 1,22 IC95 [1,06-1,41]) plus fréquentes. Pas de consensus du comité pour "
                    "une recommandation en cas de SDRA modéré (PaO2/FiO2 101-150 mmHg, critères "
                    "PROSEVA) — 2 membres du comité en désaccord avec la gradation « forte ».", S_NOTE))
    return story

def _section_q3q4():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("VOHF & pression expiratoire positive (PEP) élevée"))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("R3", "Il est recommandé de ne pas utiliser la ventilation par oscillations à haute "
         "fréquence (VOHF) en routine chez les patients atteints de SDRA modéré ou sévère.", "1-"),
        ("R4", "Il est probablement recommandé que les patients adultes atteints de SDRA "
         "modéré à sévère soient ventilés avec une PEP élevée plutôt qu'avec une PEP basse.", "2+"),
    ], [12*mm, PAGE_W-2*MARGIN-12*mm-20*mm, 20*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(P("<b>R3</b> — 6 ECR, 1715 patients. Analyse principale (3 études, 1371 "
                    "patients, excluant co-interventions) : pas de différence de mortalité "
                    "(RR 1,14 IC95 [0,88-1,48], confiance élevée) ; 6 études combinées (1705 "
                    "patients) : RR 0,94 IC95 [0,71-1,2], confiance basse. Recommandation basée "
                    "prioritairement sur 2 grands essais récents : OSCILLATE (mortalité "
                    "significativement plus élevée sous VOHF, RR 1,41 IC95 [1,12-1,79]) et OSCAR "
                    "(aucun bénéfice, OR ajusté 1,03 IC95 [0,75-1,40]) — balance bénéfice/risque "
                    "en défaveur de l'intervention.<br/>"
                    "<b>R4</b> — 8 ECR, 2728 patients (PEP moyenne J1 : 15,1±3,6 vs. 9,1±2,7 "
                    "cmH2O). Analyse principale (6 études, 2580 patients) : pas de différence "
                    "significative de mortalité (RR 0,91 IC95 [0,80-1,03], confiance modérée) ; "
                    "oxygénation significativement meilleure sous PEP élevée (+61 mmHg IC95 "
                    "[46-77]). Recommandation basée avant tout sur une méta-analyse de données "
                    "individuelles (3 grands essais) : mortalité significativement plus basse "
                    "sous PEP élevée chez les SDRA modérés à sévères (PaO2/FiO2&lt;200, RR ajusté "
                    "0,90 IC95 [0,81-1,00]), sans bénéfice chez les SDRA légers. Point de départ "
                    "clinique raisonnable : une des stratégies « PEP élevée » des essais ALVEOLI, "
                    "LOV ou ExPRESS — en surveillant la pression de plateau (≥30 cmH2O = balance "
                    "bénéfice/risque à repeser).", S_NOTE))
    return story

def _section_q5q6():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Manœuvres de recrutement & ECMO"))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("R5", "Il est probablement recommandé d'appliquer des manœuvres de recrutement chez "
         "les patients adultes atteints de SDRA modéré à sévère.", "2+"),
    ], [12*mm, PAGE_W-2*MARGIN-12*mm-20*mm, 20*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(no_reco_panel("des preuves supplémentaires sont nécessaires pour formuler une "
                                "recommandation définitive sur l'utilisation de l'ECMO "
                                "veino-veineuse chez les patients atteints de SDRA sévère "
                                "(Question 6)."))
    story.append(Spacer(1, 2*mm))
    story.append(P("<b>R5</b> — 6 ECR, 1423 patients (types de manœuvres très variables : CPAP "
                    "prolongée 30-40 cmH2O, PEP croissante à pression motrice constante, "
                    "pressions motrices élevées). Étude sans co-intervention (1 étude, 110 "
                    "patients) : réduction significative de mortalité (RR 0,62 IC95 [0,39-0,98], "
                    "confiance basse) ; 6 études combinées (1423 patients) : RR 0,81 IC95 "
                    "[0,69-0,95], confiance modérée. Amélioration de l'oxygénation à 24h (+52 "
                    "mmHg IC95 [23-81]) et réduction du recours aux traitements de sauvetage "
                    "(RR 0,64 IC95 [0,35-0,93]). Prudence chez le patient hypovolémique ou en "
                    "état de choc (risque d'hypotension transitoire).<br/>"
                    "<b>Q6 (ECMO)</b> — étude CESAR (180 patients, transfert vs. centre "
                    "d'origine) : pas de différence de mortalité (RR 0,75 IC95 [0,53-1,06], "
                    "confiance basse) ; méta-analyse combinant CESAR + études observationnelles "
                    "(8 études, 1151 patients) : RR 0,96 IC95 [0,67-1,39], confiance très basse. "
                    "Limites méthodologiques de CESAR : critère composite, 24 % du groupe "
                    "interventionnel n'a pas reçu l'ECMO, pas de ventilation protectrice "
                    "standardisée dans le groupe contrôle, co-intervention de transfert vers un "
                    "centre expert à haut volume. En attendant l'essai EOLIA (en cours au moment "
                    "du texte source), le groupe recommande une prise en charge basée sur la "
                    "ventilation protectrice et une prise en charge médicalisée précoce avant "
                    "toute VV-ECMO éventuelle.", S_NOTE))
    story.append(Spacer(1, 3*mm))
    story.append(info_panel(P(
        "<b>Conclusion du texte source :</b> ces recommandations doivent être personnalisées "
        "au cas par cas (rapport bénéfice/risque individuel) ; le bénéfice potentiel de "
        "stratégies combinées ou séquentielles n'a jamais été évalué et ne fait l'objet "
        "d'aucune recommandation. Le groupe international ATS-ESICM-SCCM prévoyait de "
        "compléter ces recommandations par des travaux sur les traitements pharmacologiques et "
        "les mesures associées à la prise en charge du SDRA.",
        S_BODY_SM), bg=GREY_LIGHT, border=GREY))
    return story

def _section_synthese():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Synthèse et messages clés"))
    story.append(Spacer(1, 2*mm))
    story.append(P(
        "• Ventilation protectrice systématique : Vt 4-8 mL/kg de poids théorique (initial "
        "6 mL/kg, ajustable jusqu'à 8), Pplat &lt;30 cmH2O — recommandation forte, socle de la "
        "prise en charge quel que soit le niveau de sévérité.<br/>"
        "• Décubitus ventral &gt;12h/jour en cas de SDRA sévère — recommandation forte, "
        "bénéfice de mortalité démontré en sous-groupe (durée &gt;12h + SDRA modéré/sévère), "
        "mais pas de consensus pour le SDRA modéré isolé ; surveiller obstruction de sonde et "
        "points d'appui.<br/>"
        "• Ne pas utiliser la VOHF en routine dans le SDRA modéré ou sévère — recommandation "
        "forte contre, deux grands essais récents en défaveur (surmortalité ou absence de "
        "bénéfice).<br/>"
        "• PEP élevée plutôt que PEP basse dans le SDRA modéré à sévère (PaO2/FiO2&lt;200) — "
        "recommandation optionnelle, bénéfice de mortalité en méta-analyse de données "
        "individuelles limité à ce sous-groupe ; surveiller la pression de plateau.<br/>"
        "• Manœuvres de recrutement chez le SDRA modéré à sévère — recommandation optionnelle, "
        "prudence hémodynamique chez le patient hypovolémique/choqué.<br/>"
        "• ECMO veino-veineuse dans le SDRA sévère : aucune recommandation ne peut être "
        "formulée faute de preuves suffisantes — privilégier la ventilation protectrice et une "
        "prise en charge précoce en centre expert avant toute décision d'ECMO.<br/>"
        "• Ces recommandations concernent exclusivement la stratégie ventilatoire du SDRA et "
        "ne sont pas extrapolables aux autres causes d'insuffisance respiratoire aiguë.",
        S_BODY))
    story.append(Spacer(1, 5*mm))

    story.append(section_bar("Sources et traçabilité", color=GREY))
    story.append(Spacer(1, 2*mm))
    story.append(P(
        "<b>Document source :</b> SFAR, « Recommandations pour la prise en charge du SDRA » — "
        "traduction résumée officielle de : An Official ATS/ESICM/SCCM Clinical Practice "
        "Guideline: Mechanical Ventilation in Adult Patients with Acute Respiratory Distress "
        "Syndrome (Am J Respir Crit Care Med 2017;195(9):1253-1263, incluant l'erratum "
        "2017;195(11):1540). Traduction réalisée par le comité Réanimation de la SFAR sous la "
        "responsabilité de M. Garnier, M. Jabaudon, A. Monsel, C. Quesnel, J-M. Constantin ; "
        "texte validé par le Comité des Référentiels Cliniques SFAR (12/12/2017) et le CA SFAR "
        "(02/02/2018).", S_SOURCE))
    story.append(Spacer(1, 1.5*mm))
    story.append(P("<b>Couverture :</b> les 5 recommandations numérotées (R1-R5) et l'absence "
                    "de recommandation sur l'ECMO (Question 6) sont reproduites intégralement, "
                    "avec les statistiques clés (RR, IC95%, effectifs) de chaque « résumé des "
                    "connaissances ». Ce document ne comporte aucune figure, tableau ou "
                    "algorithme (vérifié par lecture intégrale des 21 pages du texte source) — "
                    "contenu purement narratif. Les argumentaires complets (rationnel détaillé, "
                    "justification méthodologique complète, orientations de recherche futures) "
                    "sont condensés ; se référer au texte intégral pour le détail exhaustif de "
                    "chaque méta-analyse.", S_SOURCE))
    story.append(Spacer(1, 1.5*mm))
    story.append(P("<b>Note méthodologique :</b> à la différence de la version originale "
                    "anglaise, la traduction française ne reporte pas la confiance globale dans "
                    "l'estimation de l'effet (Haute/Modérée/Basse/Très basse) à la fin de chaque "
                    "énoncé de recommandation, par souci de simplification et de conformité au "
                    "format RFE SFAR — cette confiance reste néanmoins précisée dans le texte "
                    "pour chaque critère de jugement détaillé, et citée dans les notes de cette "
                    "fiche.", S_SOURCE))
    story.append(Spacer(1, 3*mm))
    story.append(info_panel(P(
        "<b>Avertissement :</b> ce document est une fiche de synthèse indépendante, produite "
        "pour un usage d'aide-mémoire. Il reprend l'intégralité des recommandations mais ne "
        "remplace pas le texte intégral et n'est ni édité ni validé par la SFAR. En cas de "
        "doute, se référer au texte intégral, aux recommandations ultérieures et/ou à un avis "
        "spécialisé.",
        S_BODY_SM), bg=GREY_LIGHT, border=GREY))
    return story

def _section_intro_q1q2():
    return _section_intro() + [Spacer(1, 4*mm)] + _section_q1q2()

def _section_q3q4_q5q6():
    return _section_q3q4() + [Spacer(1, 4*mm)] + _section_q5q6()

SECTIONS = [
    ("Introduction & volumes courants/Pplat/décubitus ventral", _section_intro_q1q2),
    ("VOHF, PEP élevée, manœuvres de recrutement & ECMO", _section_q3q4_q5q6),
    ("Synthèse, sources & traçabilité", _section_synthese),
]

def _make_doc():
    return SimpleDocTemplate(OUT, pagesize=A4,
                              leftMargin=MARGIN, rightMargin=MARGIN,
                              topMargin=32*mm, bottomMargin=16*mm,
                              title="Fiche SFAR - Prise en charge du SDRA (trad. ATS-ESICM-SCCM 2017)",
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
