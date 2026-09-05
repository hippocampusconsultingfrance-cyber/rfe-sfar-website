# -*- coding: utf-8 -*-
"""
Fiche de synthese - RFE SFAR 2025, en association avec la SOFMER
Decisions de limitation et d'arret de traitements (LAT) en soins critiques de l'adulte
Source verifiee : texte valide par le Comite des Referentiels Cliniques de la SFAR (10/05/2025)
et le CA SFAR (15/07/2025). Comite de 20 experts SFAR/SOFMER + 1 expert usager (HAS) + 1 expert
soins palliatifs. 3 champs, 9 questions au format PICO, methode GRADE(R), recherche
bibliographique 2000-2025.

Resultats (resume officiel) : 9 recommandations avec accord fort (1 GRADE1, 2 GRADE2,
6 avis d'experts) + 2 absences de recommandation, apres un tour de vote. Mon propre inventaire
independant, question par question, denombre exactement les memes 9 recommandations numerotees
(R1.1-R1.4, R2.1, R3.1-R3.3.2) + 2 absences de recommandation (extubation vs sevrage progressif ;
equipe de mediation) - concordance exacte avec le resume officiel, sans mismatch d'agregat a
signaler (cas rare dans ce corpus, la plupart des documents precedents necessitant une
disclosure de divergence de comptage).

Particularite de grading propre a cette source (distincte des autres RFE du corpus) : aucun tag
GRADE de ce document ne porte de signe +/- (contrairement aux RFE "classiques" qui utilisent
GRADE 1+/1-/2+/2-). Les 3 recommandations gradees (R1.4, R3.1, R3.3.2) portent litteralement les
tags "GRADE 2", "GRADE 1", "GRADE 2" sans polarite imprimee - verifie par lecture directe aux
3 emplacements. Polarite inferee a partir du verbe de chaque enonce ("il est (probablement)
recommande de faire...") : les 3 sont de sens positif, aucune recommandation negative n'existe
dans ce document. Tagees "1+"/"2+"/"2+" ici pour coherence visuelle/chromatique avec le reste du
corpus (meme logique de disclosure deja appliquee sur la fiche traumatisme_cranien pour un
GRADE2 non signe).

Divergence mineure de formulation source-interne relevee entre le corps de texte (sous chaque
question) et le "Tableau recapitulatif recommandations" final (R1.3 : le tableau recapitulatif
ajoute "et au sein de l'equipe soignante" ; R2.1 : reformulation mineure "protocole de sedation"
vs "protocole pour l'administration de la sedation") - la methode de la source explicite que ce
tableau recapitulatif integre les "amendements valides par les experts concernes et le
coordinateur, ainsi que les groupes de lecture", ce qui en fait la version finale amendee ; c'est
donc la formulation du tableau recapitulatif qui est reproduite ici comme texte de reference pour
R1.3 et R2.1, disclosure explicite dans la section tracabilite.

8 figures/annexes toutes integralement exploitables (aucune image brute non transcriptible dans
ce document, contrairement a plusieurs fiches precedentes du corpus) : Figures 1-2 (encadres
reglementaires texte), Figure 3 (algorithme decisionnel patient capable/incapable de s'exprimer -
transcrit en tableau comparatif 2 colonnes), Figure 4 (encadre reglementaire texte), Figure 5
(deroulement en 5 phases + check-list des membres a convier - transcrit en tableaux), Figure 6
(protocole de sedation profonde et continue maintenue jusqu'au deces, avec posologies
medicamenteuses precises, + echelles RASS/BPS/RDOS - transcrit integralement), Figure 7
(strategie d'accompagnement des proches en 9 etapes chronologiques - transcrit en tableau),
Figure 8 (outils de communication en 5 sections - transcrit integralement).
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from style import *
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.units import mm

OUT = "/private/tmp/claude-501/-Users-macbook-Downloads-claude/65498e3e-5ddf-47a6-b100-3ac535d1faa0/scratchpad/rfe_sfar/output/Fiche_SFAR_LAT_Soins_Critiques_2025.pdf"

SOURCE_TXT = ("Source : Recommandations Formalisées d'Experts (RFE) de la SFAR, en association "
              "avec la SOFMER « Décisions de limitation et d'arrêt de traitements (LAT) en soins "
              "critiques de l'adulte » — 2025, texte validé par le Comité des Référentiels "
              "Cliniques de la SFAR (10/05/2025) et le CA SFAR (15/07/2025). Fiche de synthèse "
              "non officielle : se référer au texte intégral.")

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
    header_band(canvas, doc, "SFAR / SOFMER — RFE 2025 — FICHE DE SYNTHÈSE",
                "Décisions de LAT en soins critiques",
                page_title, icon_fn=lambda c,x,y: icon_shield(c, x, y, 13*mm), color=NAVY)
    footer_band(canvas, doc, SOURCE_TXT, f"Page {doc.page} / {TOTAL_PAGES['n']}")

# ---------------------------------------------------------------------------
def _section_intro():
    story = []
    story.append(Spacer(1, 3*mm))
    story.append(info_panel(P(
        "<b>Objectif :</b> la SFAR et la SOFMER (Société Française de Médecine Physique et de "
        "Réadaptation) se sont associées pour proposer des recommandations pour la pratique "
        "professionnelle sur les décisions de limitation et arrêt de traitements (LAT) en "
        "services de soins critiques de l'adulte (les services de soins critiques pédiatriques "
        "sont exclus du champ de ces recommandations).<br/><br/>"
        "<b>Conception :</b> groupe de 20 experts (SFAR/SOFMER, dont un expert usager HAS et un "
        "expert soins palliatifs). Méthode GRADE® — 3 champs, 9 questions au format PICO "
        "(Population, Intervention, Comparison, Outcome), recherche bibliographique extensive "
        "2000-2025 (MEDLINE, Tripdatabase, Prospero, ClinicalTrials.gov, EMBASE, SCOPUS, "
        "Cochrane).<br/><br/>"
        "<b>Résultats (résumé officiel) :</b> 9 recommandations avec accord fort après 1 tour de "
        "vote (1 GRADE 1, 2 GRADE 2, 6 avis d'experts) et 2 absences de recommandation.",
        S_BODY), bg=BG_PANEL, border=TEAL))
    story.append(Spacer(1, 3*mm))
    story.append(info_panel(P(
        "<b>Contexte épidémiologique (France) :</b> 53 % des décès surviennent en milieu "
        "hospitalier, dont 23 % en services de soins critiques (soit environ 12 % de l'ensemble "
        "des décès français). 80 à 90 % des décès en soins critiques font suite à une décision "
        "de LAT ; 12 à 14 % des patients admis en soins critiques font l'objet d'une telle "
        "décision au cours de leur séjour.",
        S_BODY_SM), bg=GREY_LIGHT, border=GREY))
    story.append(Spacer(1, 3*mm))
    story.append(info_panel(P(
        "<b>Terminologie GRADE® utilisée par la source :</b> GRADE 1 = recommandation "
        "« forte » (« il est/n'est pas recommandé de faire… ») • GRADE 2 = recommandation "
        "« optionnelle » (« il est/n'est probablement pas recommandé de faire… ») • "
        "Avis d'experts = littérature trop faible ou inexistante (« les experts suggèrent… ») • "
        "Absence de recommandation = littérature insuffisante pour conclure, à distinguer d'une "
        "recommandation négative. <b>Particularité de cette source :</b> aucun tag GRADE de ce "
        "document ne porte de signe +/- (contrairement à d'autres RFE) ; polarité inférée du "
        "verbe de chaque énoncé — les 3 recommandations gradées de ce document sont toutes de "
        "sens positif, tagées « 1+ »/« 2+ » ici par cohérence avec le code couleur du reste du "
        "corpus.",
        S_BODY_SM), bg=AMBER_LIGHT, border=AMBER))
    story.append(Spacer(1, 3*mm))
    cw = PAGE_W - 2*MARGIN
    story.append(simple_table(
        ["Champ", "Objet", "Recommandations"],
        [
            ["Champ 1 (4 questions)", "Prérequis et modalités d'une décision de LAT "
             "(réunions pluriprofessionnelles, recherche des volontés du patient, protocole "
             "d'aide à la décision, participation des équipes paramédicales)", "R1.1 à R1.4"],
            ["Champ 2 (2 questions)", "Modalités de mise en œuvre d'une décision de LAT "
             "(protocole de sédation profonde et continue, extubation vs sevrage progressif)",
             "R2.1 + 1 absence de reco."],
            ["Champ 3 (3 questions)", "Relations avec les proches, communication, désaccords "
             "et conflits (stratégie d'accompagnement, formation à la communication, structure "
             "d'éthique clinique, médiation)", "R3.1 à R3.3.2 + 1 absence de reco."],
        ],
        [cw*0.22, cw*0.60, cw*0.18]))
    story.append(Spacer(1, 3*mm))
    story.append(info_panel(P(
        "<b>Repères terminologiques (définitions de la source) :</b><br/>"
        "• <b>Obstination déraisonnable :</b> actes de prévention, d'investigation ou de soins "
        "poursuivis alors qu'ils sont inutiles, disproportionnés, ou n'ayant d'autre effet que le "
        "seul maintien artificiel de la vie.<br/>"
        "• <b>Limitation des traitements :</b> non-majoration d'un traitement de suppléance "
        "d'organe, ou non-instauration d'un traitement en cas de nouvelle défaillance d'organe. "
        "<b>Arrêt des traitements :</b> interruption d'un ou plusieurs traitements de suppléance "
        "d'organe assurant un maintien artificiel en vie.<br/>"
        "• <b>Niveau d'engagement thérapeutique</b> (Fiche LAT SFAR) : niveau 1 = engagement "
        "maximal ; niveau 2 = limitation d'une ou plusieurs thérapeutiques ; niveau 3 = arrêt des "
        "traitements et démarche palliative.<br/>"
        "• <b>Procédure collégiale :</b> concertation entre l'équipe soignante et au moins un "
        "médecin consultant sans lien hiérarchique (« consultant extérieur »). Obligatoire si "
        "patient hors d'état d'exprimer sa volonté, avant une sédation profonde et continue, ou "
        "en cas de refus d'appliquer des directives anticipées.<br/>"
        "• <b>Sédation profonde et continue maintenue jusqu'au décès (SPCMD) :</b> suspension de "
        "la conscience poursuivie jusqu'au décès, encadrée par la loi du 2 février 2016, titrée "
        "sur une échelle (RASS cible -4/-5).<br/>"
        "• <b>Réanimation d'attente (« time-limited trial ») :</b> prise en charge de quelques "
        "heures à quelques jours (usuellement jusqu'à 2 jours, durée pouvant s'étendre jusqu'à "
        "5 j chez le sujet âgé fragile) lorsque l'indication n'est pas claire, pour recueillir "
        "les informations nécessaires à une décision éclairée.",
        S_BODY_SM), bg=BG_PANEL, border=TEAL))
    return story

def _section_champ1a():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Champ 1 — Réunions pluriprofessionnelles & volontés du patient"))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("R1.1", "Les experts suggèrent d'organiser des réunions pluriprofessionnelles "
         "régulières de réflexion et d'échange autour du projet de soins des patients afin "
         "d'améliorer la qualité des soins.", "AE"),
        ("R1.2", "Les experts suggèrent de rechercher les volontés du patient hospitalisé en "
         "soins critiques précocement et par tout moyen possible afin d'améliorer la qualité "
         "des soins.", "AE"),
    ], [13*mm, PAGE_W-2*MARGIN-13*mm-20*mm, 20*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(P("R1.1 : une bonne collaboration interprofessionnelle médecins-infirmiers "
                    "est associée à une moindre perception de soins inappropriés (OR=0,72 IC95 "
                    "[0,56-0,92]). Une « bonne » ambiance éthique (mesurée par l'EDMCQ) est "
                    "associée à une meilleure concordance entre perception d'obstination "
                    "déraisonnable et évolution défavorable réelle à 1 an (100 % vs 85,9 %), à "
                    "davantage de décisions de LAT formalisées, et à une moindre intention des "
                    "professionnels de quitter leur poste. R1.2 : seuls 15 % des patients admis "
                    "en réanimation ont désigné une personne de confiance avec document formel "
                    "et 4 % ont rédigé des directives anticipées (étude française "
                    "multicentrique) ; 14,4 % des admissions en réanimation sont perçues comme "
                    "non-bénéfiques par les réanimateurs, le manque de connaissance des volontés "
                    "du patient étant un facteur fréquemment cité.", S_NOTE))
    story.append(Spacer(1, 3*mm))
    story.append(section_bar("Figure 1 (source) — Directives anticipées : aspects réglementaires et pratiques", color=GREY))
    story.append(Spacer(1, 2*mm))
    story.append(info_panel(P(
        "<b>Cadre réglementaire :</b> régies par la loi du 2 février 2016 (Claeys-Leonetti). "
        "Expriment la volonté de la personne relative à sa fin de vie (poursuite, limitation, "
        "arrêt ou refus de traitement) ; n'ont pas vocation à être utilisées si le patient peut "
        "s'exprimer ; droit et non obligation ; datées et signées ; s'imposent au médecin pour "
        "toute décision ; validité illimitée ; révisables et révocables à tout moment (le "
        "document le plus récent fait foi). Le médecin peut ne pas les appliquer dans 2 "
        "situations seulement : urgence vitale (le temps d'une évaluation complète), ou "
        "directives manifestement inappropriées/non conformes après procédure collégiale — la "
        "décision est alors inscrite au dossier et portée à la connaissance de la personne de "
        "confiance ou, à défaut, de la famille.<br/><br/>"
        "<b>En pratique :</b> les DA aident le médecin à percevoir ce que le patient aurait "
        "qualifié d'obstination déraisonnable — elles n'ont pas vocation à définir l'indication "
        "de techniques précises de suppléance d'organes ; en pratique, elles ont plus d'intérêt "
        "lorsqu'elles informent sur les « objectifs de vie » et les valeurs du patient que "
        "lorsqu'elles listent des moyens (intubation, trachéotomie, épuration extra-rénale…). "
        "Ce ne sont ni un testament, ni un document d'organisation des obsèques.",
        S_BODY_SM), bg=BG_PANEL, border=TEAL))
    story.append(Spacer(1, 3*mm))
    story.append(section_bar("Figure 2 (source) — Personne de confiance : aspects réglementaires et pratiques", color=GREY))
    story.append(Spacer(1, 2*mm))
    story.append(info_panel(P(
        "<b>Cadre réglementaire</b> (CSP Art. L1111-6, loi Kouchner 2002, modifiée par la loi "
        "n°2024-317) : toute personne majeure peut désigner une personne de confiance (parent, "
        "proche ou médecin traitant), consultée si elle-même est hors d'état d'exprimer sa "
        "volonté. Son témoignage prévaut sur tout autre témoignage. Désignation écrite, "
        "cosignée, valable sans limitation de durée, révisable à tout moment. Chaque "
        "établissement de santé doit proposer cette désignation à l'admission.<br/><br/>"
        "<b>En pratique :</b> lorsque le patient ne peut plus s'exprimer, la personne de "
        "confiance a une mission de référent — elle rend compte de la volonté du patient sans "
        "prendre elle-même la décision médicale ; en l'absence de DA, son témoignage prévaut sur "
        "celui de la famille. Une seule personne de confiance peut être désignée par patient "
        "adulte ; en présence de plusieurs documents, le plus récent fait foi. "
        "<b>Attention :</b> à ne pas confondre avec la « personne à prévenir/référente », "
        "simplement contactée en cas de dégradation de l'état de santé.",
        S_BODY_SM), bg=BG_PANEL, border=TEAL))
    return story

def _section_champ1b():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Champ 1 — Protocole d'aide à la décision & équipes paramédicales"))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("R1.3", "Pour les patients hospitalisés en soins critiques, lors d'une réflexion "
         "autour d'une prise de décision de limitation et/ou d'arrêt des traitements, les "
         "experts suggèrent d'utiliser un protocole de service d'aide à la décision et de "
         "communication avec les proches et au sein de l'équipe soignante pour améliorer la "
         "qualité des soins.", "AE"),
        ("R1.4", "Pour les patients hospitalisés en service de soins critiques, il est "
         "probablement recommandé d'inclure la participation active des équipes paramédicales "
         "aux réunions de procédure collégiale de limitation et/ou arrêt des traitements afin "
         "d'améliorer la qualité des soins.", "2+"),
    ], [13*mm, PAGE_W-2*MARGIN-13*mm-20*mm, 20*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(P("R1.3 : dans une étude rétrospective multicentrique (343 patients), la "
                    "SPCMD n'était appliquée qu'à 60 % des patients concernés (11 % pas du tout "
                    "sédatés), la procédure collégiale manquait dans 17 % des cas, le consultant "
                    "extérieur dans 29 % des cas, et un protocole de service formalisé n'existait "
                    "que dans 32 % des unités. R1.4 : les IDE perçoivent quasi-systématiquement "
                    "l'ambiance éthique de fin de vie comme moins favorable que les médecins et "
                    "décrivent leur participation aux décisions comme insuffisante ; l'insatisfaction "
                    "des IDE est principalement liée à des décisions de LAT jugées trop tardives, "
                    "et la poursuite de soins perçus comme futiles est associée à un niveau de "
                    "détresse morale élevé chez les IDE.", S_NOTE))
    story.append(Spacer(1, 3*mm))
    story.append(section_bar("Figure 3 (source) — Algorithme décisionnel de LAT en soins critiques", color=GREY))
    story.append(Spacer(1, 2*mm))
    cw = PAGE_W - 2*MARGIN
    story.append(simple_table(
        ["Étape", "Patient en mesure de s'exprimer", "Patient incapable de s'exprimer"],
        [
            ["1. Initiation de la réflexion", "Patient, médecin, équipe paramédicale, personne "
             "de confiance, proches", "Patient, médecin, équipe paramédicale, personne de "
             "confiance, proches"],
            ["2. Recueil des éléments", "Décision du patient avec le médecin (± personne de "
             "confiance)", "Information de la personne de confiance et des proches de "
             "l'initiation d'une procédure de LAT (consignée au dossier) + consultation des "
             "directives anticipées, de la personne de confiance, de la famille et des proches"],
            ["3. Délibération", "Si décision de limitation/arrêt → mise en œuvre directe par "
             "l'équipe de soin ; si demande associée de SPCMD → procédure collégiale (équipe de "
             "soin + intervenant extérieur)", "Procédure collégiale obligatoire (équipe de soin "
             "+ intervenant extérieur)"],
            ["4. Décision", "Par le médecin en charge du patient ; inscription au dossier de la "
             "décision de LAT et de la procédure de SPCMD le cas échéant", "Par le médecin en "
             "charge du patient ; inscription au dossier + information de la personne de "
             "confiance et des proches"],
            ["5. Mise en œuvre", "Mise en œuvre de la décision d'arrêt des traitements par "
             "l'équipe de soin → SPCMD si besoin", "Délai permettant l'exercice d'un recours en "
             "temps utile → mise en œuvre par l'équipe de soin → arrêt ou limitation des "
             "traitements (inscription au dossier) → si l'arrêt concerne un traitement "
             "nécessaire au maintien en vie → SPCMD"],
        ],
        [cw*0.16, cw*0.42, cw*0.42]))
    story.append(Spacer(1, 3*mm))
    story.append(section_bar("Figure 4 (source) — Procédure collégiale & intervenant extérieur", color=GREY))
    story.append(Spacer(1, 2*mm))
    story.append(info_panel(P(
        "<b>Cadre réglementaire</b> (CSP, Code de déontologie médicale Art. R4127-37-2) : la "
        "décision de limitation/arrêt respecte la volonté antérieurement exprimée par le "
        "patient ; si le patient est hors d'état de s'exprimer, la décision ne peut être prise "
        "qu'à l'issue de la procédure collégiale, dans le respect des directives anticipées ou, "
        "à défaut, du témoignage de la personne de confiance, de la famille ou d'un proche. Le "
        "médecin en charge peut engager la procédure de sa propre initiative ou à la demande de "
        "la personne de confiance/famille/proches. La décision est prise par le médecin en "
        "charge à l'issue d'une concertation avec l'équipe de soins et l'avis motivé d'au moins "
        "un médecin consultant, sans lien hiérarchique avec lui ; un second avis peut être "
        "recueilli si l'un des médecins l'estime utile. La décision est motivée et inscrite au "
        "dossier.<br/><br/>"
        "<b>En pratique :</b> 3 situations imposent la procédure collégiale — patient hors "
        "d'état d'exprimer sa volonté avant une limitation/arrêt susceptible d'entraîner le "
        "décès ; avant toute SPCMD ; en cas de refus d'appliquer des directives anticipées "
        "jugées inappropriées. Le consultant extérieur doit être sans lien hiérarchique avec "
        "l'équipe ; pour la SRLF et la SFAR, il doit examiner le patient (le CNOM admet un avis "
        "à distance). Les médecins traitant ou spécialiste déjà impliqués ne sont pas considérés "
        "comme consultants extérieurs.",
        S_BODY_SM), bg=BG_PANEL, border=TEAL))
    return story

def _section_champ1c():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Figure 5 (source) — Déroulement et check-list d'une procédure collégiale"))
    story.append(Spacer(1, 2*mm))
    cw = PAGE_W - 2*MARGIN
    story.append(simple_table(
        ["Phase", "Contenu"],
        [
            ["1. Initiation", "Par tout soignant (médecin ou non) impliqué dans la prise en "
             "charge ; indirectement par le patient via des directives anticipées ; à la "
             "demande de la personne de confiance, de la famille ou d'un proche ; à la demande "
             "du patient lui-même pour une demande de SPCMD."],
            ["2. Préparation", "Recueillir les informations médicales pertinentes (antécédents, "
             "traitements, diagnostic, pronostic) ; consulter les directives anticipées ; "
             "recueillir le témoignage de la personne de confiance ou, à défaut, de la famille "
             "ou des proches ; recueillir l'avis d'un médecin consultant extérieur à l'équipe "
             "(un second avis si nécessaire) ; informer la famille et les proches (sauf "
             "opposition du patient exprimée dans les DA) ; tracer l'information au dossier."],
            ["3. Délibération collégiale", "Réunir une équipe participant à la réunion "
             "collégiale ; discuter les éléments médicaux (situation clinique, souffrance, "
             "traitements en cours, alternatives, pronostic, évolution) et non-médicaux "
             "(souhaits du patient, témoignage de la personne de confiance et des proches) ; "
             "objectif = recueillir tous les avis, sans viser nécessairement un consensus."],
            ["4. Décision", "À l'issue de la délibération, décision motivée par le médecin en "
             "charge du patient ; consignation au dossier médical avec mention des participants "
             "et des arguments discutés."],
            ["5. Mise en œuvre et suivi", "Informer la famille et les proches de la décision et "
             "de sa justification ; en cas d'opposition, solliciter une structure d'éthique "
             "clinique, prendre le temps du cheminement (entretiens répétés, interlocuteurs "
             "variés) et informer des recours légaux possibles en cas de blocage ; s'assurer du "
             "confort du patient."],
        ],
        [cw*0.20, cw*0.80]))
    story.append(Spacer(1, 3*mm))
    story.append(info_panel(P(
        "<b>Check-list des membres à convier</b><br/>"
        "<b>Participation obligatoire</b> (au regard de la loi) : médecin sénior en charge du "
        "patient • un médecin extérieur au service, appelé en qualité de consultant • membres "
        "présents de l'équipe soignante.<br/>"
        "<b>Participation recommandée :</b> au moins un autre médecin du service • interne(s) "
        "impliqué(s) dans la prise en charge • médecins et IDE d'autres services directement "
        "impliqués (médecin généraliste, chirurgien, spécialistes…).<br/>"
        "<b>Participation idéale :</b> cadre du service • kinésithérapeute impliqué • étudiants "
        "hospitaliers/IDE/AS/kinésithérapeute • psychologue • assistante sociale.",
        S_BODY_SM), bg=BG_PANEL, border=TEAL))
    return story

def _section_champ2():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Champ 2 — Sédation profonde et continue & extubation"))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("R2.1", "Chez les patients hospitalisés en soins critiques, après une décision d'arrêt "
         "des traitements, les experts suggèrent d'utiliser un protocole de sédation profonde et "
         "continue maintenue jusqu'au décès pour améliorer la qualité des soins.", "AE"),
    ], [13*mm, PAGE_W-2*MARGIN-13*mm-20*mm, 20*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(no_reco_panel("en l'absence de données, il n'est pas possible de formuler une "
                                "recommandation sur la pratique d'une extubation après une "
                                "décision d'arrêt de traitements, chez les patients ventilés en "
                                "soins critiques, pour améliorer la qualité des soins."))
    story.append(Spacer(1, 2*mm))
    story.append(P("R2.1 : étude multicentrique française (343 patients, 57 services) — la "
                    "SPCMD était appliquée à 60 % des patients décédés après LAT, avec objectif "
                    "de RASS -5 atteint dans 60 % des cas et analgésie associée dans 94 % des "
                    "cas ; un protocole formalisé n'existait que dans 32 % des services. Une "
                    "étude sur 450 patients a montré qu'une sédation profonde (RASS -5) était "
                    "associée à moins d'inconfort (OR=0,47 IC95 [0,28-0,78]), sans différence sur "
                    "les scores de deuil compliqué ou de stress post-traumatique des proches, "
                    "quel que soit le moment de l'évaluation (3, 6 ou 12 mois après le décès). "
                    "Extubation : une seule étude "
                    "interventionnelle disponible (étude ARREVE, 402 proches/458 patients) — pas "
                    "de différence entre extubation terminale et sevrage progressif sur le stress "
                    "post-traumatique, les symptômes anxio-dépressifs ou le deuil compliqué à "
                    "12 mois ; fréquence accrue de gasps/obstruction des voies aériennes après "
                    "extubation (non retrouvée si sédation protocolisée avec score de dyspnée).", S_NOTE))
    story.append(Spacer(1, 3*mm))
    story.append(section_bar("Figure 6 (source) — Protocole de sédation profonde et continue (SPCMD)", color=GREY))
    story.append(Spacer(1, 2*mm))
    cw = PAGE_W - 2*MARGIN
    story.append(simple_table(
        ["Étape", "Contenu"],
        [
            ["Préparation de la famille", "Proposer un recours à un représentant du culte ; "
             "demander si la famille souhaite être présente tout au long du processus ; "
             "proposer un accompagnement et un soutien aux proches (psychologue…)."],
            ["Mesures générales", "S'assurer d'une voie veineuse efficace ; arrêt de la "
             "nutrition et de l'hydratation artificielles ; scopolamine 1 à 3 patchs derrière "
             "l'oreille ; en cas de nausées/vomissements : ondansétron 4 mg x3/j IVL ou SC, ou "
             "métoclopramide 10 mg IV/SC x3/j (relais 30-60 mg/24h IVSE)."],
            ["Le jour de l'arrêt", "Désactiver les alarmes (pression invasive/non invasive, "
             "SpO2), garder la surveillance du pouls et de la fréquence respiratoire ; "
             "privilégier les soins de confort ; arrêter les soins inconfortables (prélèvements, "
             "aspirations systématiques, injections SC…) ; reconsidérer le maintien des "
             "dispositifs invasifs (garder sonde vésicale et voie veineuse centrale pour le "
             "confort) ; sédation maintenue jusqu'au décès selon les objectifs RASS et BPS/RDOS, "
             "associant obligatoirement un hypnotique et un analgésique de palier 3."],
        ],
        [cw*0.22, cw*0.78]))
    story.append(Spacer(1, 2*mm))
    story.append(info_panel(P(
        "<b>Patient déjà sédaté :</b> maintien ou augmentation de la sédation-analgésie pour "
        "l'objectif cible avant l'arrêt des traitements.<br/><br/>"
        "<b>Patient non sédaté — posologies proposées :</b><br/>"
        "• <b>Midazolam</b> (anxiolytique/sédatif) — 1 mg/mL, IVSE ; bolus initial 1 mg IVD "
        "toutes les 3 min jusqu'à l'objectif ; entretien en dose de titration/h ; objectif RASS "
        "-4 ou -5 ; posologie maximale 30 mg/h.<br/>"
        "• <b>Sufentanil</b> (analgésique) — 5 µg/mL, IVSE ; bolus initial 5 µg IVD toutes les "
        "3 min jusqu'à l'objectif ; entretien en dose de titration/h ; objectif BPS ≤5 à la "
        "stimulation douloureuse ; posologie maximale 50 µg/h.<br/>"
        "• <b>Morphine</b> (alternative au sufentanil) — 1 mg/mL, IVSE ; bolus initial 3 mg IVD "
        "toutes les 5 min jusqu'à l'objectif ; entretien en dose de titration/h ; objectif "
        "BPS ≤5 à la stimulation douloureuse.<br/>"
        "• Si les objectifs (RASS/BPS ou RASS/RDOS) ne sont pas atteints aux doses maximales : "
        "ajout de propofol par bolus de titration puis administration continue, à l'appréciation "
        "du clinicien.",
        S_BODY_SM), bg=BG_PANEL, border=TEAL))
    return story

def _section_champ2b():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Figure 6 (suite) — Échelles d'évaluation RASS, BPS, RDOS"))
    story.append(Spacer(1, 2*mm))
    story.append(P("Cette proposition de protocole est utilisable pour toute décision de SPCMD "
                    "(qu'il y ait ou non une procédure Maastricht III suite à la décision de "
                    "LAT). Chez un patient conscient, un arrêt des traitements de maintien en "
                    "vie nécessite : demande répétée (temps de la réflexion, entretiens "
                    "multiples tracés), capacité de discernement du patient (évaluation "
                    "psychiatrique/psychologique avec son accord), demande libre et éclairée "
                    "(connaissance de la maladie, du traitement, de l'évolution, du pronostic, "
                    "des conséquences et risques de la sédation).", S_NOTE))
    story.append(Spacer(1, 3*mm))
    cw = PAGE_W - 2*MARGIN
    story.append(simple_table(
        ["RASS (Richmond Agitation-Sedation Scale)", "Description"],
        [
            ["+4 Combatif", "Danger immédiat envers l'équipe."],
            ["+3 Très agité", "Tire, arrache tuyaux/cathéters et/ou agressif envers l'équipe."],
            ["+2 Agité", "Mouvements fréquents sans but précis et/ou désadaptation au respirateur."],
            ["+1 Ne tient pas en place", "Anxieux ou craintif, mouvements orientés, peu vigoureux, non agressif."],
            ["0 Éveillé et calme", "—"],
            ["-1 Somnolent", "Pas complètement éveillé, contact visuel à l'appel (>10s)."],
            ["-2 Diminution légère de la vigilance", "Contact visuel bref à l'appel (<10s)."],
            ["-3 Diminution modérée", "N'importe quel mouvement à l'appel, sans contact visuel."],
            ["-4 Diminution profonde", "Aucun mouvement à l'appel ; mouvement à la stimulation "
             "physique (friction non nociceptive épaule/sternum)."],
            ["-5 Non réveillable", "Aucun mouvement, ni à l'appel, ni à la stimulation physique."],
        ],
        [cw*0.40, cw*0.60]))
    story.append(Spacer(1, 3*mm))
    story.append(simple_table(
        ["Échelle BPS (Behavioural Pain Scale)", "1 point", "2 points", "3 points", "4 points"],
        [
            ["Expression du visage", "Détendu", "Partiellement crispé", "Crispé", "Grimace"],
            ["Tonus des membres supérieurs", "Aucun mouvement", "Flexion partielle", "Flexion "
             "complète", "Rétraction"],
            ["Adaptation au respirateur", "Adapté", "Déclenche ponctuellement", "Lutte contre le "
             "respirateur", "Non ventilable"],
        ],
        [cw*0.28, cw*0.18, cw*0.18, cw*0.18, cw*0.18]))
    story.append(Spacer(1, 2*mm))
    story.append(simple_table(
        ["Échelle RDOS (Respiratory Distress Observation Scale)", "0 point", "1 point", "2 points"],
        [
            ["Fréquence cardiaque (/min)", "< 90", "90-109", "≥ 110"],
            ["Fréquence respiratoire (/min)", "< 19", "19-30", "> 30"],
            ["Agitation, mouvements involontaires", "Non", "Occasionnels", "Fréquents"],
            ["Respiration abdominale paradoxale", "Non", "—", "Oui"],
            ["Muscles accessoires inspiratoires", "Non", "Légère", "Prononcée"],
            ["Râles expiratoires", "Non", "—", "Oui"],
            ["Battement des ailes du nez", "Non", "—", "Oui"],
            ["Expression de crainte", "Non", "—", "Oui"],
        ],
        [cw*0.40, cw*0.20, cw*0.20, cw*0.20]))
    return story

def _section_champ3():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Champ 3 — Relations avec les proches, communication, conflits"))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("R3.1", "Pour les proches de patients hospitalisés en services de soins critiques, il "
         "est recommandé d'utiliser une stratégie d'accompagnement structurée après une décision "
         "d'arrêt et/ou limitation de traitements, incluant des interactions proactives avec "
         "l'équipe soignante et/ou des supports de communication, pour améliorer la qualité des "
         "soins.", "1+"),
        ("R3.2", "En service de soins critiques, les experts suggèrent de former l'équipe "
         "médico-soignante à la communication pour permettre de prévenir les conflits entre "
         "proches et équipes médico-soignantes.", "AE"),
        ("R3.3.1", "Pour les proches de patients hospitalisés et l'équipe médico-soignante en "
         "service de soins critiques, en cas de désaccords/conflits autour d'une décision de "
         "limitation et/ou arrêt des traitements, les experts suggèrent de faire intervenir une "
         "structure d'éthique clinique pour améliorer la qualité des soins.", "AE"),
        ("R3.3.2", "Pour les proches de patients hospitalisés et l'équipe médico-soignante en "
         "service de soins critiques, en prévention d'un désaccord/conflit entre proches et "
         "équipes soignantes dans une situation à risque de conflit de valeurs autour d'une "
         "décision de limitation et/ou arrêt des traitements, il est probablement recommandé de "
         "faire intervenir une structure d'éthique clinique pour améliorer la qualité des "
         "soins.", "2+"),
    ], [15*mm, PAGE_W-2*MARGIN-15*mm-20*mm, 20*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(no_reco_panel("les experts ne sont pas en mesure d'émettre une recommandation "
                                "concernant l'intervention d'une équipe de médiation pour "
                                "améliorer la qualité des soins."))
    story.append(Spacer(1, 2*mm))
    story.append(P("R3.1 : 3 essais randomisés multicentriques français concordants — "
                    "conférence de fin de vie structurée (126 proches/22 services) réduisant le "
                    "stress post-traumatique, l'anxiété et la dépression à 90 j ; livret "
                    "d'information (90 proches/3 services) réduisant le stress post-traumatique "
                    "(40 % vs 73 %, p=0,001) ; stratégie en 3 temps — information/écoute, "
                    "accompagnement au décès, rencontre post-décès — (34 services) réduisant le "
                    "deuil prolongé (15 % vs 21 %, p=0,035). R3.3.1/R3.3.2 : sur 8 études "
                    "(5 essais randomisés + 3 méta-analyses), une structure d'éthique clinique "
                    "« proactive » est associée à une réduction de la durée de séjour, une "
                    "réduction des ressources médicales chez les patients qui vont décéder, et "
                    "une meilleure satisfaction des soignants/proches ; son intérêt pour la "
                    "résolution de conflits déjà avérés reste en revanche incertain (2 études "
                    "rétrospectives monocentriques de conciliation par une SEC sur des conflits "
                    "majeurs déjà installés — l'une d'elles rapporte un consensus obtenu dans "
                    "36 % des 116 cas recensés). Médiation : une seule étude disponible, données "
                    "trop indirectes pour conclure.", S_NOTE))
    story.append(Spacer(1, 3*mm))
    story.append(section_bar("Figure 7 (source) — Stratégies d'accompagnement des proches", color=GREY))
    story.append(Spacer(1, 2*mm))
    cw = PAGE_W - 2*MARGIN
    story.append(simple_table(
        ["Étape chronologique", "Contenu"],
        [
            ["Dès l'admission du patient", "Supports écrits et numériques pour faciliter la "
             "compréhension de la situation par les proches."],
            ["Présence et implication des proches", "Assouplir les horaires de visite et le "
             "nombre de visiteurs ; encourager leur participation aux soins non médicaux s'ils "
             "le souhaitent."],
            ["Communication continue", "Organiser des réunions régulières ; adopter une "
             "stratégie de communication structurée."],
            ["Soutien psychologique et spirituel", "Proposer un soutien psychologique ; "
             "faciliter l'accès aux représentants du culte."],
            ["Décision de LAT", "Expliquer clairement la situation médicale et les décisions de "
             "LAT, s'assurer de la compréhension ; proposer une approche individualisée selon "
             "les croyances et valeurs du patient et de ses proches."],
            ["Préparation au décès", "Informer des signes cliniques ; proposer un livret "
             "explicatif des démarches ; dédier un espace de recueillement adapté."],
            ["Moment du décès", "Offrir aux proches la possibilité de rester autant de temps "
             "qu'ils le souhaitent ; permettre un rituel d'adieu selon leurs souhaits."],
            ["Suivi post-décès", "Proposer une réunion entre les proches et les soignants s'ils "
             "le souhaitent ; ne pas envoyer systématiquement de lettre de condoléance, qui peut "
             "aggraver le deuil."],
            ["Gestion des conflits", "Préparer un protocole local de gestion des conflits entre "
             "famille/proches et équipe soignante ; encourager des temps d'écoute pour "
             "favoriser une décision partagée."],
        ],
        [cw*0.26, cw*0.74]))
    story.append(Spacer(1, 3*mm))
    story.append(section_bar("Figure 8 (source) — Outils pour la communication d'une LAT", color=GREY))
    story.append(Spacer(1, 2*mm))
    story.append(info_panel(P(
        "<b>Avant la réunion :</b> recueillir les souhaits du patient si non encore fait (DA, "
        "personne de confiance, proches) ; informer de la future tenue d'une réunion "
        "collégiale.<br/>"
        "<b>Environnement :</b> présentation des interlocuteurs ; endroit garantissant "
        "l'intimité ; être assis ; établir un contact ; impliquer les proches ; anticiper et "
        "gérer les contraintes de temps et interruptions.<br/>"
        "<b>Transmettre la décision :</b> reprendre l'histoire du patient (temps imparfait), la "
        "décision de la réunion collégiale (temps présent), ce qui va se passer (temps futur — "
        "prononcer les mots « fin de vie », « mort » si c'est le cas) ; s'assurer de la "
        "compréhension ; reformuler si besoin.<br/>"
        "<b>Congruence communication non verbale/verbale :</b> ton adapté, rythme lent sans être "
        "traînant ; empathie ; écoute active (émotions et langage) ; reconnaître les émotions et "
        "mécanismes de défense (tristesse, colère, choc, sidération, déni) ; adapter la conduite "
        "selon que le stress est adapté (poursuivre l'entretien) ou dépassé (soutenir avant de "
        "reformuler) ; respecter les silences ; être disponible.<br/>"
        "<b>Fin d'entretien et synthèse :</b> demander si besoin de plus d'informations ; "
        "accompagner la distribution d'un livret de fin de vie ; proposer une aide psychologique "
        "et/ou la visite d'un représentant du culte si besoin ; faire intervenir une structure "
        "d'éthique clinique en cas de difficultés ; proposer une prochaine rencontre. "
        "Disponibilité d'un médecin et d'un infirmier durant les derniers jours de vie pour "
        "témoigner du soutien ; proposer de revoir les proches après le décès.",
        S_BODY_SM), bg=BG_PANEL, border=TEAL))
    return story

def _section_synthese():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Synthèse et messages clés"))
    story.append(Spacer(1, 2*mm))
    story.append(P(
        "• Champ 1 : organiser des réunions pluriprofessionnelles régulières autour du projet "
        "de soins, rechercher les volontés du patient le plus précocement possible et par tout "
        "moyen (DA, personne de confiance, proches, médecins référents), utiliser un protocole "
        "de service d'aide à la décision, et inclure activement les équipes paramédicales aux "
        "réunions de procédure collégiale (probablement recommandé).<br/>"
        "• La procédure collégiale est obligatoire dans 3 situations : patient hors d'état "
        "d'exprimer sa volonté avant une limitation/arrêt susceptible d'entraîner le décès ; "
        "avant toute sédation profonde et continue ; en cas de refus d'appliquer des directives "
        "anticipées jugées inappropriées. Elle associe l'équipe de soins et au moins un médecin "
        "consultant extérieur, sans lien hiérarchique.<br/>"
        "• Champ 2 : utiliser un protocole de sédation profonde et continue maintenue jusqu'au "
        "décès (associant obligatoirement un hypnotique et un analgésique de palier 3, titrés "
        "sur les scores RASS/BPS/RDOS) après une décision d'arrêt des traitements. Aucune "
        "recommandation ne peut être formulée entre extubation et sevrage progressif, faute de "
        "littérature suffisante — si une extubation est choisie, elle doit s'accompagner d'un "
        "protocole de sédation adapté pour prévenir les signes d'inconfort.<br/>"
        "• Champ 3 : une stratégie d'accompagnement structurée des proches (interactions "
        "proactives, supports de communication) est recommandée après une décision de LAT ; "
        "former l'équipe médico-soignante à la communication pour prévenir les conflits ; faire "
        "intervenir une structure d'éthique clinique tant en prévention (situation à risque de "
        "conflit de valeurs) qu'en cas de désaccord avéré — son bénéfice est mieux établi en "
        "prévention que pour la résolution de conflits déjà installés. Aucune recommandation "
        "n'a pu être formulée sur le recours à une équipe de médiation, faute de données.",
        S_BODY))
    story.append(Spacer(1, 5*mm))

    story.append(section_bar("Sources et traçabilité", color=GREY))
    story.append(Spacer(1, 2*mm))
    story.append(P(
        "<b>Document source :</b> « Décisions de limitation et d'arrêt de traitements (LAT) en "
        "soins critiques de l'adulte » — Recommandations Formalisées d'Experts de la SFAR, en "
        "association avec la SOFMER. 2025, texte validé par le Comité des Référentiels Cliniques "
        "de la SFAR (10/05/2025) et le CA SFAR (15/07/2025). Comité de 20 experts, coordination "
        "M. Giabicani (SFAR).", S_SOURCE))
    story.append(Spacer(1, 1.5*mm))
    story.append(P("<b>Couverture :</b> 9 recommandations numérotées (R1.1-R1.4, R2.1, "
                    "R3.1-R3.3.2) et 2 absences de recommandation (extubation vs sevrage "
                    "progressif ; équipe de médiation) reproduites intégralement — concordance "
                    "exacte avec le résumé officiel (9 recommandations : 1 GRADE1, 2 GRADE2, "
                    "6 avis d'experts + 2 absences), sans divergence de comptage à signaler. Les "
                    "8 figures/annexes de la source (aucune n'étant une simple image non "
                    "exploitable) sont toutes reproduites : Figures 1, 2 et 4 (encadrés "
                    "réglementaires), Figure 3 (algorithme décisionnel, transcrit en tableau "
                    "comparatif), Figure 5 (déroulement en 5 phases + check-list), Figure 6 "
                    "(protocole de sédation avec posologies + échelles RASS/BPS/RDOS), Figure 7 "
                    "(stratégie d'accompagnement des proches) et Figure 8 (outils de "
                    "communication).", S_SOURCE))
    story.append(Spacer(1, 1.5*mm))
    story.append(P("<b>Grading :</b> aucun tag GRADE de cette source ne porte de signe +/- "
                    "(convention propre à ce document, différente des autres RFE du corpus). "
                    "Polarité inférée du verbe de chacune des 3 recommandations gradées "
                    "(R1.4, R3.1, R3.3.2) — toutes de sens positif — et tagée « + » ici par "
                    "cohérence visuelle avec le reste du corpus.", S_SOURCE))
    story.append(Spacer(1, 1.5*mm))
    story.append(P("<b>Formulation R1.3 et R2.1 :</b> le texte du « Tableau récapitulatif "
                    "recommandations » de la source diffère très légèrement de celui imprimé "
                    "sous l'argumentaire de chaque question (R1.3 : ajout de « et au sein de "
                    "l'équipe soignante » ; R2.1 : « protocole de sédation » vs « protocole pour "
                    "l'administration de la sédation »). La méthode de la source précise que ce "
                    "tableau récapitulatif intègre les « amendements validés par les experts "
                    "concernés et le coordinateur, ainsi que les groupes de lecture » — c'est "
                    "donc cette formulation finale amendée qui est reproduite ici pour R1.3 et "
                    "R2.1.", S_SOURCE))
    story.append(Spacer(1, 3*mm))
    story.append(info_panel(P(
        "<b>Avertissement :</b> ce document est une fiche de synthèse indépendante, produite "
        "pour un usage d'aide-mémoire. Il reprend l'intégralité des recommandations de la RFE "
        "mais ne remplace pas le texte intégral et n'est ni édité ni validé par la SFAR/SOFMER. "
        "En cas de doute, se référer au texte intégral, aux recommandations ultérieures et/ou à "
        "un avis spécialisé.",
        S_BODY_SM), bg=GREY_LIGHT, border=GREY))
    return story

SECTIONS = [
    ("Introduction, méthodologie", _section_intro),
    ("Champ 1 — Réunions pluriprofessionnelles & volontés du patient", _section_champ1a),
    ("Champ 1 — Protocole d'aide à la décision & équipes paramédicales", _section_champ1b),
    ("Champ 1 — Procédure collégiale : déroulement & check-list", _section_champ1c),
    ("Champ 2 — Sédation profonde et continue & extubation", _section_champ2),
    ("Champ 2 — Échelles d'évaluation RASS, BPS, RDOS", _section_champ2b),
    ("Champ 3 — Relations avec les proches, communication, conflits", _section_champ3),
    ("Synthèse, sources & traçabilité", _section_synthese),
]

def _make_doc():
    return SimpleDocTemplate(OUT, pagesize=A4,
                              leftMargin=MARGIN, rightMargin=MARGIN,
                              topMargin=32*mm, bottomMargin=16*mm,
                              title="Fiche SFAR-SOFMER 2025 - Decisions de LAT en soins critiques",
                              author="Synthèse indépendante (source SFAR/SOFMER)")

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
