# -*- coding: utf-8 -*-
"""
Fiche de synthese - RFE commune SFAR-AFEF 2018
Insuffisance hepatique en soins critiques (Liver failure in intensive care unit).
Texte publie 2018-09-29. Auteurs : C. Paugam-Burtz, E. Levesque, A. Louvet, D. Thabut et al.
23 experts (9 SFAR, 8 AFEF, 2 coordonnateurs SFAR, 2 coordonnateurs AFEF, 2 organisateurs).
Methodologie GRADE. Deux champs : (1) insuffisance hepatique aigue (IHA, 3 questions),
(2) insuffisance hepatique sur foie cirrhotique / ACLF (7 questions).

Comptage : 19 recommandations numerotees identifiees (R1, R2.1-2.3, R3, R4, R5.1-5.2, R6,
R7.1-7.2, R8.1-8.6, R9, R10) + 1 item explicite "Pas de recommandation" (thromboprophylaxie
medicamenteuse chez le cirrhotique, sous-partie de la Question 9) - alors que le resume de la
source annonce "18 recommandations". Ecart non reconcilie et disclose : la propre repartition
par grade du resume (6 Grade 1 + 7 Grade 2 + 6 avis d'experts = 19) correspond exactement a un
comptage direct des 19 items numerotes, confirmant que le total "19" est correct et que la
phrase-resume "18 recommandations" est une incoherence interne a la source. Chaque item
individuel est fidele a son propre libelle et grade litteral, seul le total-resume est en cause.
Accord FORT obtenu pour 100% des recommandations (aucune exception a "Accord Faible",
contrairement a d'autres documents du corpus) - disclose explicitement.

3 tableaux verbatim (Tableau 1 : prise en charge symptomatique IHA ; Tableau 2 : KDIGO modifie
cirrhose ; Tableau 3 : definition du syndrome hepatorenal) + 2 figures/algorithmes (Figure 1 :
bilan/traitement IHA ; Figure 2 : prise en charge de l'IRA du cirrhotique) + 2 annexes (CLIF-SOFA,
grade ACLF), toutes transcrites depuis le texte source (aucune image pure - toutes verifiees
directement dans la couche texte du PDF, contrairement a plusieurs fiches anterieures du corpus
dont les figures etaient des images pures).
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from style import *
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.units import mm

OUT = "/private/tmp/claude-501/-Users-macbook-Downloads-claude/65498e3e-5ddf-47a6-b100-3ac535d1faa0/scratchpad/rfe_sfar/output/Fiche_SFAR_AFEF_Insuffisance_Hepatique_2018.pdf"

SOURCE_TXT = ("Source : Recommandations Formalisees d'Experts « Insuffisance hepatique en soins "
              "critiques » - SFAR, AFEF. Publie 2018. Methodologie GRADE. Fiche de synthese non "
              "officielle : se referer au texte integral.")

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
        ("TOPPADDING",(0,0),(-1,-1),3.2), ("BOTTOMPADDING",(0,0),(-1,-1),3.2), ("LEFTPADDING",(0,0),(-1,-1),5),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            st.append(("BACKGROUND",(0,i),(-1,i), BG_PANEL))
    t.setStyle(TableStyle(st))
    return t

def legend_flowable():
    items = [("1+", "Recommandé (forte)"), ("1-", "Non recommandé (forte)"),
             ("2+", "Proposé (optionnel)"), ("2-", "Proposé de ne pas faire"),
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

def no_reco_panel(text):
    return info_panel(P("<b>Pas de recommandation</b> — " + text, S_BODY_SM), bg=GREY_LIGHT, border=GREY)

TOTAL_PAGES = {"n": 8}

def on_page(canvas, doc, page_title):
    header_band(canvas, doc, "SFAR / AFEF — RFE 2018 — FICHE DE SYNTHÈSE",
                "Insuffisance hépatique en soins critiques",
                page_title, icon_fn=lambda c,x,y: icon_liver(c, x, y, 13*mm), color=NAVY)
    footer_band(canvas, doc, SOURCE_TXT, f"Page {doc.page} / {TOTAL_PAGES['n']}")

# ---------------------------------------------------------------------------
def _section_intro():
    story = []
    story.append(Spacer(1, 3*mm))
    story.append(info_panel(P(
        "<b>Champ de la RFE :</b> prise en charge de première ligne de l'insuffisance hépatique en "
        "soins critiques, pour un public large de réanimateurs — ne détaille pas les mesures "
        "spécifiques des unités spécialisées (transplantation hépatique). RFE commune SFAR "
        "(Société Française d'Anesthésie et de Réanimation) et AFEF (Association Française pour "
        "l'Étude du Foie) — <b>23 experts</b> francophones selon le résumé (confirmé par comptage "
        "direct), mais l'introduction affirme séparément « <b>vingt</b> » — incohérence interne à "
        "la source, non reconciliée. Population pédiatrique exclue du champ.<br/><br/>"
        "<b>Deux champs :</b> (1) l'insuffisance hépatique aiguë (IHA), maladie rare devant être "
        "reconnue rapidement (3 questions) ; (2) l'insuffisance hépatique sur foie cirrhotique / "
        "Acute-on-Chronic Liver Failure (ACLF), motif fréquent d'hospitalisation en soins critiques "
        "(7 questions). <b>19 recommandations</b> numérotées identifiées dans le texte (le résumé de "
        "la source annonce « 18 recommandations », mais sa propre répartition par grade — 6 Grade 1 "
        "+ 7 Grade 2 + 6 avis d'experts = 19 — correspond exactement à un comptage direct des items "
        "numérotés ; le total « 18 » de la phrase-résumé est donc une incohérence interne à la "
        "source, non reconciliée ici). La source évoque aussi, à deux reprises, « trois protocoles "
        "de soins » distincts des 19 recommandations — probablement le Tableau 1 et les Figures 1-2 "
        "(structurés en tableaux/étapes) — repris ici intégralement, sans correspondance stricte "
        "forcée. Après deux tours de cotation, <b>un accord fort a été obtenu "
        "pour 100 % des recommandations</b> — aucune exception « Accord Faible » à signaler, "
        "contrairement à d'autres documents de ce corpus. Pour une sous-question (Question 9, "
        "thromboprophylaxie médicamenteuse), les experts n'ont pas pu formuler de recommandation "
        "(signalé explicitement plus bas).",
        S_BODY), bg=BG_PANEL, border=TEAL))
    story.append(Spacer(1, 3*mm))

    story.append(section_bar("Légende des grades (méthodologie GRADE)"))
    story.append(Spacer(1, 2*mm))
    story.append(legend_flowable())
    story.append(Spacer(1, 4*mm))

    story.append(section_bar("Champ 1 — Insuffisance hépatique aiguë (IHA)", color=NAVY))
    story.append(Spacer(1, 1.5*mm))
    story.append(P(
        "L'IHA est une maladie rare (&lt; 10 cas/million/an) : dysfonction hépatique rapidement "
        "évolutive avec baisse du TP, en l'absence d'hépatopathie préexistante, en moins de 26 "
        "semaines. <b>Sévère</b> si TP &lt; 50 % ; <b>grave</b> si une encéphalopathie s'y associe. "
        "Survie à 2 ans ≈ 90 % en cas de transplantation ou après IHA sévère au paracétamol sans "
        "transplantation.", S_NOTE))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("R1", "Chez les patients présentant une IHA sévère, il est recommandé d'effectuer le "
               "dosage sanguin du paracétamol, les sérologies virales A (IgM VHA) et B (Ag HBs, "
               "IgM HBc), la recherche urinaire de toxiques (amphétamine, cocaïne), une "
               "échographie cardiaque, et une écho-Doppler hépatique.", "1+"),
        ("R2.1", "En cas d'IHA, lorsqu'une intoxication au paracétamol est suspectée, il est "
                 "recommandé d'instaurer un traitement par N-acétylcystéine sans attendre le "
                 "résultat du dosage sanguin du paracétamol et quelle que soit sa valeur.", "1+"),
        ("R2.2", "En cas d'IHA sévère, quelle que soit l'étiologie suspectée, il est probablement "
                 "recommandé d'instaurer un traitement par N-acétylcystéine afin de diminuer la "
                 "morbi-mortalité.", "2+"),
        ("R2.3", "En cas d'IHA sévère, quelle que soit l'étiologie suspectée, les experts "
                 "suggèrent de prendre contact avec un centre de transplantation hépatique pour "
                 "discuter du bilan étiologique de seconde intention (si le bilan initial est "
                 "négatif) et de l'indication de transplantation.", "AE"),
    ], [13*mm, PAGE_W-2*MARGIN-13*mm-15*mm, 15*mm]))
    return story

def _section_champ1_suite():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(P(
        "<b>Transplantation hépatique (TH) :</b> une IHA sévère (TP &lt; 50 %) suffit à prendre l'avis "
        "d'un centre de TH. La présence d'une encéphalopathie hépatique diminue significativement "
        "la survie (90,1 % sans encéphalopathie vs 37,8 % avec, p&lt;0,0001) ; les critères "
        "historiques du King's College Hospital (encéphalopathie ≥ grade III, créatinine "
        "&gt; 300 µmol/L, temps de Quick &gt; 100 s, pH &lt; 7,3, ± lactatémie &gt; 3,5 mmol/L à "
        "4 h ou 3,0 mmol/L à 12 h) restent validés mais avec une sensibilité de 50-60 % seulement.",
        S_NOTE))
    story.append(Spacer(1, 3*mm))

    story.append(reco_table([
        ("R3", "Afin de diminuer la morbi-mortalité des patients présentant une IHA sévère, les "
               "experts suggèrent de traiter précocement la survenue des défaillances d'organes "
               "autres que la défaillance hépatique et d'éviter tout facteur aggravant, selon le "
               "tableau proposé (Tableau 1).", "AE"),
    ], [13*mm, PAGE_W-2*MARGIN-13*mm-15*mm, 15*mm]))
    story.append(Spacer(1, 3*mm))

    story.append(KeepTogether([
        P("<b>TABLEAU 1</b> — Prise en charge symptomatique des défaillances d'organe extrahépatiques au cours de l'IHA sévère", S_H2),
        Spacer(1, 1*mm),
        simple_table(
            ["Système", "Ce qu'il faut faire", "Ce qu'il ne faut pas faire"],
            [
                ["Neurologique", "Surveillance neurologique ; natrémie cible 140-145 mmol/L ; dépistage/traitement "
                 "hypoglycémie toutes les 2h ; intubation si Glasgow < 8 ; minimiser la sédation ; Doppler "
                 "trans-crânien ; si HTIC : traitement non spécifique",
                 "Benzodiazépines et autres psychotropes (dont métoclopramide) ; laxatifs/antibiotiques non "
                 "absorbables visant à diminuer l'ammoniémie"],
                ["Respiratoire", "Ventilation mécanique protectrice selon les recommandations usuelles", "—"],
                ["Hémodynamique", "Évaluation répétée de la volémie et des fonctions cardiaques D/G ; "
                 "remplissage par cristalloïdes en 1ère intention ; hypotension réfractaire : noradrénaline", "—"],
                ["Rénal", "EER selon les indications usuelles", "AINS et autres néphrotoxiques"],
                ["Gastro-intestinal", "Prévention des hémorragies digestives de stress selon les recommandations usuelles", "—"],
                ["Hémostase", "—", "Administration systématique de facteurs de coagulation ou plaquettes en "
                 "l'absence d'hémorragie"],
                ["Immunitaire", "Antibiothérapie dès suspicion d'un sepsis, incluant l'aggravation de "
                 "l'encéphalopathie", "—"],
            ], [30*mm, (PAGE_W-2*MARGIN-30*mm)*0.52, (PAGE_W-2*MARGIN-30*mm)*0.48])
    ]))
    story.append(Spacer(1, 3*mm))

    story.append(KeepTogether([
        P("<b>FIGURE 1</b> — Prise en charge spécifique de l'insuffisance hépatique aiguë sévère (TP &lt; 50 %)", S_H2),
        Spacer(1, 1*mm),
        simple_table(
            ["Étape", "Contenu"],
            [
                ["Bilan étiologique", "Bilan sanguin (paracétamol, sérologies VHA/VHB, toxiques urinaires) ; "
                 "écho-Doppler hépatique ; échographie cardiaque"],
                ["Évaluation de la gravité", "Encéphalopathie ; défaillance hémodynamique ; défaillance rénale"],
                ["Surveillance", "TP et/ou INR, facteur V ; glycémie ; acidose, lactatémie ; ammoniémie"],
                ["Traitement", "N-acétylcystéine quelle que soit l'étiologie suspectée ; traitement étiologique ; "
                 "aciclovir IV si suspicion d'hépatite herpétique (fièvre > 40 °C)"],
                ["Orientation", "Prendre contact avec un centre de transplantation hépatique"],
            ], [40*mm, PAGE_W-2*MARGIN-40*mm])
    ]))
    return story

def _section_champ2_intro_r4_r5():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Champ 2 — Insuffisance hépatique sur foie cirrhotique (ACLF)", color=NAVY))
    story.append(Spacer(1, 1.5*mm))
    story.append(P(
        "700 000 personnes atteintes de cirrhose en France (100-150 000 décès/an) ; alcool, "
        "syndrome métabolique et virus responsables de 90 % des cas. L'<b>Acute-on-Chronic Liver "
        "Failure (ACLF)</b> — décompensation aiguë de la cirrhose définie par le nombre de "
        "défaillances d'organes (CLIF-SOFA, Annexes 1-2) — prédit mieux la mortalité en réanimation "
        "que les scores habituels (Child-Pugh, MELD). Mortalité en soins critiques ≈ 30-50 %.",
        S_NOTE))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("R4", "Il n'est probablement pas recommandé de refuser d'admettre les patients "
               "cirrhotiques en soins critiques, du fait de leur seule maladie cirrhotique.", "2-"),
        ("R5.1", "Afin de définir et d'évaluer la sévérité de l'insuffisance rénale aiguë (IRA) "
                 "chez les patients cirrhotiques, les experts suggèrent : d'utiliser la "
                 "classification KDIGO modifiée pour ces patients (Tableau 2) ; de traiter l'IRA "
                 "selon son stade de gravité et selon l'algorithme proposé (Figure 2) ; de ne pas "
                 "contre-indiquer de principe une épuration extrarénale en cas d'IRA chez le "
                 "patient cirrhotique du fait de sa seule pathologie cirrhotique.", "AE"),
    ], [13*mm, PAGE_W-2*MARGIN-13*mm-15*mm, 15*mm]))
    story.append(Spacer(1, 3*mm))

    story.append(P("<b>TABLEAU 2</b> — Classification KDIGO modifiée de l'IRA chez les patients atteints de cirrhose", S_H2))
    story.append(Spacer(1, 1*mm))
    story.append(KeepTogether([
        simple_table(
            ["Élément", "Définition"],
            [
                ["Créatininémie de base", "Valeur la plus récente datant de moins de 3 mois avant l'épisode d'IRA ; "
                 "à défaut, la créatininémie à l'admission"],
                ["Définition de l'IRA", "Augmentation ≥ 0,3 mg/dL (≥ 26,5 µmol/L) en 48 h, ou > 1,5 fois la "
                 "créatininémie de base dans les 7 jours précédents"],
                ["Stade 1", "Augmentation ≥ 0,3 mg/dL (≥ 26,5 µmol/L) ou > 1,5 à 2 fois la créatininémie de base"],
                ["Stade 2", "Augmentation > 2 à 3 fois la créatininémie de base"],
                ["Stade 3", "Augmentation > 3 fois la créatininémie de base, ou ≥ 4 mg/dL (353,6 µmol/L), ou "
                 "début d'épuration extra-rénale"],
            ], [38*mm, PAGE_W-2*MARGIN-38*mm]),
        Spacer(1, 1.5*mm),
        P("<i>Contrairement à la classification KDIGO standard, le critère diurèse est exclu chez le "
          "cirrhotique (oligurie fréquente par rétention hydrosodée malgré une fonction rénale "
          "normale).</i>", S_NOTE)
    ]))
    return story

def _section_fig2_shr_r52():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(KeepTogether([
     P("<b>FIGURE 2</b> — Prise en charge de l'IRA du cirrhotique selon la classification KDIGO modifiée", S_H2),
     Spacer(1, 1*mm),
     info_panel(P(
        "<b>Stade 1 :</b> arrêt des facteurs précipitants/aggravants (agents néphrotoxiques : AINS, "
        "vasodilatateurs, diurétiques) et correction d'une hypovolémie, puis surveillance.<br/>"
        "<b>Stade 2-3 :</b> arrêt des facteurs précipitants/aggravants et administration d'albumine "
        "1 g/kg pendant 48 h → si <b>amélioration</b> : surveillance ; si <b>aggravation/progression</b> : "
        "rechercher les critères de syndrome hépatorénal (SHR, Tableau 3) — si présents : "
        "vasoconstricteurs et albumine, épuration extrarénale à discuter avec un centre spécialisé "
        "(selon la RFE SFAR/SRLF EER 2014) ; si absents : prise en charge selon la RFE SFAR/SRLF "
        "IRA en réanimation (2015).", S_BODY_SM), bg=BG_PANEL, border=TEAL)
    ]))
    story.append(Spacer(1, 3*mm))

    story.append(KeepTogether([
     P("<b>TABLEAU 3</b> — Définition du syndrome hépatorénal (SHR) — tous les critères doivent être réunis", S_H2),
     Spacer(1, 1*mm),
     info_panel(P(
        "Diagnostic de cirrhose avec présence d'ascite &nbsp;•&nbsp; Diagnostic d'IRA stade 2 ou 3 "
        "selon les critères KDIGO modifiés (Tableau 2), sans prendre en compte la valeur de la "
        "créatininémie &nbsp;•&nbsp; Absence de réponse après 2 jours consécutifs d'arrêt des "
        "diurétiques et remplissage vasculaire par albumine (1 g/kg) &nbsp;•&nbsp; Absence d'état de "
        "choc &nbsp;•&nbsp; Absence d'administration récente de néphrotoxiques (AINS, aminosides, "
        "produits de contraste iodé) &nbsp;•&nbsp; Absence de signe d'atteinte rénale "
        "parenchymateuse (protéinurie &gt; 500 mg/j, hématurie &gt; 50 érythrocytes/champ, "
        "échographie rénale normale)", S_BODY_SM), bg=BG_PANEL, border=TEAL)
    ]))
    story.append(Spacer(1, 3*mm))

    story.append(reco_table([
        ("R5.2", "Il est probablement recommandé de traiter, chez les patients cirrhotiques "
                 "hospitalisés en soins critiques, un syndrome hépatorénal (SHR) par un "
                 "vasoconstricteur (terlipressine en première intention), en association avec de "
                 "l'albumine.", "2+"),
    ], [13*mm, PAGE_W-2*MARGIN-13*mm-15*mm, 15*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(P(
        "Terlipressine : 0,5-1 mg IV toutes les 4-6 h, augmentée progressivement si la créatininémie "
        "ne diminue pas de plus de 25 %, jusqu'à 2 mg toutes les 4-6 h (ou 2-12 mg/24h IVSE en "
        "continu) ; poursuivie jusqu'à réponse complète ou 14 jours maximum si réponse partielle. "
        "L'association midodrine + octréotide est moins efficace et ne doit pas être utilisée. "
        "Albumine : 1 g/kg avant le vasoconstricteur puis 20-40 g/j (doses empiriques).", S_NOTE))
    return story

def _section_r6_r7():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("R6", "Afin de diminuer la morbi-mortalité des patients cirrhotiques hospitalisés en "
               "unité de soins critiques, il est probablement recommandé, quels que soient les "
               "symptômes et la (les) défaillance(s) d'organe présentés, de rechercher "
               "systématiquement une infection (incluant le prélèvement du liquide d'ascite — "
               "polynucléaires neutrophiles &gt; 250/mm³ définissant une infection) et de débuter "
               "précocement une antibiothérapie probabiliste ciblée sur le foyer suspecté et "
               "adaptée à l'écologie locale et à celle du patient.", "2+"),
        ("R7.1", "Il est recommandé d'administrer de l'albumine concentrée chez le cirrhotique en "
                 "soins critiques, en cas de paracentèse excédant 4 à 5 litres.", "1+"),
        ("R7.2", "Il est probablement recommandé d'administrer de l'albumine concentrée chez le "
                 "cirrhotique en soins critiques en cas d'infection spontanée du liquide d'ascite "
                 "(ILA).", "2+"),
    ], [13*mm, PAGE_W-2*MARGIN-13*mm-15*mm, 15*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(P(
        "R6 — un patient cirrhotique sur trois-quatre développe une infection ; l'antibiothérapie "
        "empirique doit cibler entérobactéries et Cocci Gram+, principaux germes en cause (ILA et "
        "infections urinaires &gt; 50 % des cas). R7.1 — 6-8 g d'albumine par litre d'ascite retiré, "
        "dès le 1er litre si la paracentèse dépasse 4-5 L. R7.2 — albumine 1,5 g/kg à J1 puis 1 g/kg à "
        "J3, restreinte aux patients avec ILA (niveau de preuve abaissé, preuve indirecte).", S_NOTE))
    return story

def _section_r8():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Question 8 — Hémorragie digestive chez le cirrhotique", color=NAVY))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("R8.1", "Chez les patients cirrhotiques, en cas d'hémorragie digestive, il est recommandé "
                 "d'administrer le plus tôt possible un traitement vasoactif intraveineux par "
                 "octréotide, somatostatine ou terlipressine, en association avec une "
                 "antibiothérapie préventive.", "1+"),
        ("R8.2", "Chez les patients cirrhotiques, en cas d'hémorragie digestive, il est "
                 "probablement recommandé d'administrer le plus tôt possible un traitement par "
                 "inhibiteurs de la pompe à protons.", "2+"),
        ("R8.3", "Chez les patients cirrhotiques, en cas d'hémorragie digestive, il est recommandé "
                 "de réaliser une endoscopie œsogastroduodénale dès que possible.", "1+"),
        ("R8.4", "Chez les patients cirrhotiques, en cas d'hémorragie digestive, il est recommandé "
                 "d'adopter une stratégie transfusionnelle restrictive visant une hémoglobinémie "
                 "comprise entre 7 et 8 g/dL.", "1+"),
        ("R8.5", "En cas de rupture de varices œsophagiennes ou œsogastriques chez un patient "
                 "cirrhotique, il est probablement recommandé d'envisager un TIPS (shunt "
                 "porto-cave intra-hépatique par voie transjugulaire) à l'aide d'une prothèse "
                 "couverte, dans un délai de 24 à 72 heures, chez les patients avec un score "
                 "Child-Pugh C &lt; 14, ou un score Child-Pugh B ayant initialement présenté un "
                 "saignement actif à l'endoscopie (prophylaxie secondaire par TIPS préemptif).", "2+"),
        ("R8.6", "En cas de rupture de varices œsophagiennes ou œsogastriques chez un patient "
                 "cirrhotique, les experts suggèrent d'envisager un TIPS avec prothèse couverte, "
                 "en urgence, en cas d'hémorragie réfractaire au traitement endoscopique (TIPS de "
                 "sauvetage).", "AE"),
    ], [13*mm, PAGE_W-2*MARGIN-13*mm-15*mm, 15*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(P(
        "<i>Argumentaire (R8.3) :</i> l'endoscopie doit être effectuée dans un délai maximal de "
        "12 heures, délai le plus souvent rapporté dans les études sur ce sujet. R8.6 — le TIPS de "
        "sauvetage arrête le saignement dans &gt; 80 % des cas ; le tamponnement (sonde de "
        "Blakemore/Linton) ou la prothèse œsophagienne auto-expansible peuvent servir de « bridge » "
        "en attendant le TIPS, mais <i>aucune recommandation n'a pu être formulée entre ces deux "
        "options</i> (1 seul essai randomisé de faible effectif, sans bénéfice démontré).",
        S_NOTE))
    return story

def _section_r9_r10_annexes():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Questions 9-10 — Hémostase et recours à un avis spécialisé", color=NAVY))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("R9", "Avant la réalisation d'un geste invasif chez le patient cirrhotique, les experts "
               "suggèrent de ne pas administrer systématiquement, de manière préventive, du "
               "plasma, des plaquettes ou du fibrinogène pour limiter le saignement.", "AE"),
    ], [13*mm, PAGE_W-2*MARGIN-13*mm-15*mm, 15*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(P(
        "<i>Argumentaire (R9) :</i> l'évaluation du rapport bénéfice/risque doit se faire au cas "
        "par cas, selon le bilan d'hémostase du patient et le caractère invasif du geste.", S_NOTE))
    story.append(Spacer(1, 2*mm))
    story.append(no_reco_panel(
        "après analyse de la littérature, les experts ne sont pas en mesure d'émettre une "
        "recommandation concernant la prescription de thromboprophylaxie médicamenteuse chez le "
        "patient cirrhotique hospitalisé en soins critiques (niveau de preuve bas, études "
        "hétérogènes) — l'évaluation du rapport bénéfice/risque doit se faire au cas par cas, "
        "notamment en post-opératoire ; l'héparine non fractionnée semble majorer le risque "
        "hémorragique par rapport aux HBPM."))
    story.append(Spacer(1, 3*mm))

    story.append(reco_table([
        ("R10", "Les experts suggèrent de demander un avis spécialisé pour tout patient "
                "cirrhotique hospitalisé en soins critiques : (1) à l'admission si le patient est "
                "déjà inscrit sur liste de transplantation hépatique ; (2) pour discuter "
                "précocement de l'engagement thérapeutique selon le nombre de défaillances "
                "d'organes et leur évolution ; (3) pour discuter de l'intérêt d'une suppléance "
                "hépatique ; (4) à la sortie des soins critiques, pour organiser une prise en "
                "charge en hépatologie en vue d'une possible transplantation.", "AE"),
    ], [13*mm, PAGE_W-2*MARGIN-13*mm-15*mm, 15*mm]))
    story.append(Spacer(1, 4*mm))

    story.append(section_bar("Annexes — CLIF-SOFA et grade ACLF", color=GREY))
    story.append(Spacer(1, 1.5*mm))
    story.append(P(
        "<i>Score utilisé dans l'argumentaire des questions 4 et 10 pour graduer la sévérité de la "
        "décompensation et guider l'admission/réévaluation en soins critiques (vérifié directement "
        "dans le texte source, tableau reproduit ici).</i>", S_NOTE))
    story.append(Spacer(1, 2*mm))
    story.append(simple_table(
        ["Organe/système", "Score 0", "Score 1", "Score 2", "Score 3", "Score 4"],
        [
            ["Foie — bilirubine (µmol/L)", "< 20", "20,4-34", "34-102", "102-204", "≥ 204"],
            ["Rein — créatinine (µmol/L)", "< 105", "105-165", "165-305", "305-440", "≥ 440"],
            ["Cérébral — enceph. (West Haven)", "Absente", "Grade 1", "Grade 2", "Grade 3", "Grade 4"],
            ["Coagulation — INR", "< 1,1", "1,1-1,25", "1,26-1,5", "1,51-2,5", "> 2,5 (TP = 30 %) ou plaq. ≤ 20 G/L"],
            ["Circulation — PAM/vasopresseurs", "PAM ≥ 70", "PAM < 70", "Dopamine ≤5 ou dobutamine/terlipressine",
             "Dopamine 5-15 ou noradré./adré. ≤0,1", "Dopamine >15 ou noradré./adré. >0,1"],
            ["Poumon — PaO2/FiO2 ou SpO2/FiO2", "> 400 / > 512", "≤ 400 / 357-512", "≤ 300 / 214-357",
             "≤ 200 / 89-214", "≤ 100 / ≤ 89"],
        ], [42*mm] + [(PAGE_W-2*MARGIN-42*mm)/5]*5))
    story.append(Spacer(1, 1.5*mm))
    story.append(P("<i>Une case notée « défaillance d'organe » dans la source (score ≥ 3 pour la plupart des systèmes) "
                    "déclenche le comptage de défaillances utilisé pour le grade ACLF ci-dessous.</i>", S_NOTE))
    story.append(Spacer(1, 3*mm))
    story.append(simple_table(
        ["Grade ACLF", "Définition (à partir du CLIF-SOFA)"],
        [
            ["Pas d'ACLF", "Pas de défaillance d'organe ; ou monodéfaillance (foie/coagulation/circulatoire/pulmonaire) "
             "avec créatininémie < 132 µmol/L et sans encéphalopathie ; ou monodéfaillance cérébrale avec "
             "créatininémie < 132 µmol/L"],
            ["ACLF-1", "Monodéfaillance rénale ; ou monodéfaillance (foie/coagulation/circulatoire/pulmonaire) avec "
             "créatininémie 132-165 µmol/L et/ou encéphalopathie grade 1-2 ; ou monodéfaillance cérébrale avec "
             "créatininémie 132-165 µmol/L"],
            ["ACLF-2", "2 défaillances d'organe"],
            ["ACLF-3", "Au moins 3 défaillances d'organe"],
        ], [28*mm, PAGE_W-2*MARGIN-28*mm]))
    return story

def _section_tracabilite():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Sources et traçabilité", color=GREY))
    story.append(Spacer(1, 2*mm))
    story.append(P(
        "<b>Document source :</b> « Insuffisance hépatique en soins critiques » (Liver failure in "
        "intensive care unit) — Recommandations Formalisées d'Experts, SFAR et AFEF. Auteurs : "
        "C. Paugam-Burtz, E. Levesque, A. Louvet, D. Thabut, R. Amathieu, C. Bureau, C. Camus, "
        "G. Chanques, S. Faure, M. Ferrandière, C. Francoz, A. Galbois, T. Gustot, C. Ichai, "
        "P. Ichai, S. Jaber, T. Lescot, R. Moreau, S. Roullet, F. Saliba, T. Thevenot, L. Velly, "
        "E. Weiss. Coordonnateurs SFAR : E. Levesque, C. Paugam-Burtz. Coordonnateurs AFEF : "
        "A. Louvet, D. Thabut. Résumé : 23 experts (confirmé par comptage des listes) — "
        "l'introduction affirme cependant « vingt », incohérence interne non reconciliée.",
        S_SOURCE))
    story.append(Spacer(1, 1.5*mm))
    story.append(P("<b>Méthodologie :</b> GRADE (force forte [1+/1-] ou faible [2+/2-] ; avis "
                    "d'experts lorsque la littérature ne permettait pas de graduer, via une méthode "
                    "GRADE grid — validation d'une recommandation si ≥ 50 % des experts convergent "
                    "et &lt; 20 % s'y opposent ; recommandation forte si ≥ 70 % convergent). Accord "
                    "fort obtenu pour 100 % des recommandations après 2 tours de cotation.", S_SOURCE))
    story.append(P("<b>Comptage :</b> 19 items numérotés identifiés dans le texte (R1 à R10, avec "
                    "sous-numéros), contre « 18 recommandations » annoncées par le résumé de la "
                    "source — la propre répartition par grade du résumé (6+7+6=19) confirme que 19 "
                    "est le total correct ; incohérence interne à la source, non reconciliée. Un "
                    "item « Pas de recommandation » (thromboprophylaxie médicamenteuse, "
                    "sous-question 9) est en sus, comme dans la source.", S_SOURCE))
    story.append(P("<b>URL source :</b> https://sfar.org/wp-content/uploads/2018/09/RFE-IH-soins-critiques.pdf", S_SOURCE))
    story.append(Spacer(1, 3*mm))
    story.append(info_panel(P(
        "<b>Avertissement :</b> ce document est une fiche de synthèse indépendante, produite pour un "
        "usage d'aide-mémoire. Il reprend l'intégralité des 19 recommandations, de l'item "
        "« pas de recommandation » et des tableaux/figures/annexes de la RFE, mais ne remplace pas "
        "le texte intégral (argumentaire complet, références bibliographiques par recommandation) "
        "et n'est ni édité ni validé par la SFAR ni l'AFEF. En cas de doute, se référer au texte "
        "intégral et/ou à un avis spécialisé.",
        S_BODY_SM), bg=GREY_LIGHT, border=GREY))
    return story

def _section_a():
    return (_section_intro() + [Spacer(1, 3*mm)] + _section_champ1_suite()
            + [Spacer(1, 4*mm)] + _section_champ2_intro_r4_r5()
            + [Spacer(1, 3*mm)] + _section_fig2_shr_r52())

def _section_b():
    return (_section_r6_r7() + [Spacer(1, 4*mm)] + _section_r8()
            + [Spacer(1, 4*mm)] + _section_r9_r10_annexes()
            + [Spacer(1, 4*mm)] + _section_tracabilite())

SECTIONS = [
    ("Champ 1 — IHA ; Champ 2 — admission, IRA, SHR", _section_a),
    ("Champ 2 — Infection, hémorragie, hémostase, annexes", _section_b),
]

def _make_doc():
    return SimpleDocTemplate(OUT, pagesize=A4,
                              leftMargin=MARGIN, rightMargin=MARGIN,
                              topMargin=32*mm, bottomMargin=16*mm,
                              title="Fiche SFAR/AFEF 2018 - Insuffisance hépatique en soins critiques",
                              author="Synthèse indépendante (source SFAR/AFEF)")

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
