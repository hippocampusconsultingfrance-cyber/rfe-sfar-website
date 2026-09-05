# -*- coding: utf-8 -*-
"""
Fiche de synthese - RFE commune SFAR-SRLF 2015 (avec GFRUP pour la pediatrie et SFN)
Insuffisance renale aigue en perioperatoire et en reanimation (a l'exclusion des
techniques d'epuration extrarenale). Texte valide CA SFAR 19/06/2015, CA SRLF 06/08/2015.
Publie Anesth Reanim. 2016;2:184-205, DOI 10.1016/j.anrea.2016.04.001.
Source verifiee : https://sfar.org/wp-content/uploads/2016/05/ANREA_132_RFE-IRA-.pdf
Methodologie GRADE. 33 recommandations (8 champs) : 9 fortes (Grade 1), 16 faibles
(Grade 2), 8 avis d'experts (9+16+8=33, comptage exact concordant avec le resume de
la source). 4 tableaux verbatim (KDIGO adulte, pRIFLE pediatrique, facteurs de risque,
agents nephrotoxiques) + 1 figure conceptuelle (agression/atteinte/IRA), 22 pages source,
document compact -> couverture complete en un seul passage.

Bug d'extraction confirme et corrige (meme classe que les cas anterieurs du corpus) :
le glyphe µ (micro) de "µmol/L" est systematiquement extrait comme "mmol/L" par la
couche texte du PDF source (confirme par rendu visuel a 250dpi des pages 4-5) - les
seuils de creatininemie KDIGO (R1.1, Tableau I) sont donc bien exprimes en µmol/L,
pas en mmol/L (26,5 µmol/L et 354 µmol/L sont les seuils KDIGO internationaux
standards ; 26,5 mmol/L ou 354 mmol/L seraient physiologiquement absurdes).
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from style import *
from style import _rounded_rect
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.units import mm

OUT = "/private/tmp/claude-501/-Users-macbook-Downloads-claude/65498e3e-5ddf-47a6-b100-3ac535d1faa0/scratchpad/rfe_sfar/output/Fiche_SFAR_SRLF_Insuffisance_Renale_Aigue_2015.pdf"

SOURCE_TXT = ("Source : Recommandations Formalisees d'Experts « Insuffisance renale aigue en perioperatoire "
              "et en reanimation (a l'exclusion des techniques d'epuration extrarenale) » - SFAR, SRLF, avec "
              "GFRUP (pediatrie) et SFN. Texte valide CA SFAR (19/06/2015) et CA SRLF (06/08/2015). Publie "
              "Anesth Reanim. 2016;2:184-205. Methodologie GRADE. Fiche de synthese non officielle : se "
              "referer au texte integral.")

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

def funnel_diagram():
    """Redessin simplifie de la Figure 1 source (3 cercles concentres) sous forme de
    3 bandeaux empiles, du plus large (agression) au plus etroit (IRA constituee)."""
    w = PAGE_W - 2*MARGIN
    h = 30*mm
    d = Drawing(w, h)
    tiers = [
        (w, TEAL, "Agression rénale aiguë  (kidney attack)", WHITE),
        (w*0.68, TEAL_DARK, "Atteinte rénale aiguë  (acute kidney damage)", WHITE),
        (w*0.38, NAVY, "Insuffisance rénale aiguë  (acute kidney injury)", WHITE),
    ]
    band_h = h/3
    for i, (bw, bg, label, fg) in enumerate(tiers):
        y = h - (i+1)*band_h
        x = (w - bw)/2
        d.add(_rounded_rect(x, y+1, bw, band_h-2, 2.2, bg, bg))
        d.add(String(w/2, y + band_h/2 - 2.6, label, fontName=FONT_BOLD, fontSize=7.6,
                      fillColor=fg, textAnchor="middle"))
    return d

TOTAL_PAGES = {"n": 6}

def on_page(canvas, doc, page_title):
    header_band(canvas, doc, "SFAR / SRLF (avec GFRUP, SFN) — RFE 2015 — FICHE DE SYNTHÈSE",
                "Insuffisance rénale aiguë périopératoire et en réanimation",
                page_title, icon_fn=lambda c,x,y: icon_kidney(c, x, y, 13*mm), color=TEAL_DARK)
    footer_band(canvas, doc, SOURCE_TXT, f"Page {doc.page} / {TOTAL_PAGES['n']}")

# ---------------------------------------------------------------------------
def _section_intro_champ1():
    story = []
    story.append(Spacer(1, 3*mm))
    story.append(info_panel(P(
        "<b>Champ de la RFE :</b> diagnostic, évaluation du risque, prévention et traitement de "
        "l'insuffisance rénale aiguë (IRA) en réanimation et en période périopératoire — "
        "<b>hors techniques d'épuration extrarénale</b> (objet d'une RFE SRLF dédiée, 2014). "
        "RFE sous l'égide de la SFAR et de la SRLF, avec la participation du GFRUP (Groupe "
        "francophone de réanimation et urgences pédiatriques) pour le volet pédiatrique et de la "
        "SFN (Société française de néphrologie) — 24 experts répartis en 9 groupes de travail.<br/><br/>"
        "<b>33 recommandations</b> formalisées, réparties en 8 champs : (1) diagnostic et gravité de "
        "l'IRA, (2) stratégies de diagnostic précoce, (3) évaluation du risque, (4) prévention non "
        "spécifique, (5) gestion des agents néphrotoxiques, (6) stratégies pharmacologiques, "
        "(7) nutrition, (8) évaluation de la récupération rénale. Selon le résumé de la source : "
        "« 9 sont fortes (Grade 1), 16 sont faibles (Grade 2) et, pour 8 recommandations, la méthode "
        "GRADE ne pouvait pas s'appliquer et celles-ci correspondent à un avis d'experts » — un "
        "comptage exact recommandation par recommandation confirme ce total (9+16+8=33), sans écart "
        "à signaler cette fois. Après 2 tours de cotation Delphi, un accord fort a été obtenu pour "
        "32 des 33 recommandations (99 %) — la seule exception (R2.1) est signalée plus bas.",
        S_BODY), bg=BG_PANEL, border=TEAL))
    story.append(Spacer(1, 3*mm))

    story.append(section_bar("Légende des grades (méthodologie GRADE)"))
    story.append(Spacer(1, 2*mm))
    story.append(legend_flowable())
    story.append(Spacer(1, 4*mm))

    story.append(section_bar("Champ 1 — Diagnostic de l'IRA et évaluation de sa gravité"))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("R1.1", "Il faut utiliser les critères KDIGO (stade 1) pour définir une IRA par la présence "
                 "d'au moins 1 des 3 critères diagnostiques suivants : augmentation de la créatinine "
                 "plasmatique ≥ 26,5 µmol/L en 48 h ; augmentation de la créatinine plasmatique ≥ 1,5 "
                 "fois la valeur de base au cours des 7 derniers jours ; diurèse &lt; 0,5 mL/kg/h "
                 "pendant 6 h.", "AE"),
        ("R1.2", "Il faut utiliser la classification KDIGO pour caractériser la gravité d'une IRA, "
                 "selon le tableau I ci-dessous.", "AE"),
        ("R1.3", "Si l'on souhaite estimer le débit de filtration glomérulaire (DFG), il ne faut pas "
                 "utiliser les formules estimées (Cockroft-Gault, MDRD, CKD-EPI) chez le patient de "
                 "réanimation ou en postopératoire.", "1-"),
        ("R1.4", "Si l'on souhaite estimer le DFG, il faut probablement utiliser la formule de calcul "
                 "de la clairance de la créatinine (UV/P créatinine).", "2+"),
        ("R1.1 P", "<i>(Pédiatrique)</i> Chez l'enfant, il faut probablement établir le diagnostic "
                    "d'IRA en utilisant la classification de RIFLE modifiée pour la pédiatrie "
                    "(pRIFLE) : clairance estimée de la créatinine diminuée d'au moins 25 %, ou "
                    "diurèse &lt; 0,5 mL/kg/h pendant 8 heures.", "AE"),
        ("R1.2 P", "<i>(Pédiatrique)</i> Chez l'enfant, il faut probablement évaluer la gravité d'une "
                    "IRA selon les critères de la classification pRIFLE (tableau II ci-dessous).", "AE"),
    ], [13*mm, PAGE_W-2*MARGIN-13*mm-15*mm, 15*mm]))
    story.append(Spacer(1, 3*mm))

    story.append(P(
        "<i>Argumentaire (R1.4) :</i> le calcul de la clairance de la créatinine par la formule "
        "UV/P repose sur un recueil des urines d'au moins 1 heure.", S_NOTE))
    story.append(Spacer(1, 2*mm))

    story.append(P("<b>TABLEAU I</b> — Classification de l'IRA selon les critères KDIGO", S_H2))
    story.append(Spacer(1, 1*mm))
    story.append(KeepTogether([simple_table(
        ["Stade", "Créatinine plasmatique", "Diurèse"],
        [
            ["1", "≥ 26,5 µmol/L ou 1,5 à 1,9 fois la créatinine plasmatique de base", "< 0,5 mL/kg/h pendant 6 à 12 h"],
            ["2", "2,0 à 2,9 fois la créatinine plasmatique de base", "< 0,5 mL/kg/h pendant ≥ 12 h"],
            ["3", "3,0 fois la créatinine plasmatique de base, ou créatinine plasmatique ≥ 354 µmol/L, "
                  "ou mise en route de l'épuration extrarénale", "< 0,3 mL/kg/h pendant ≥ 24 h ou anurie pendant ≥ 12 h"],
        ], [14*mm, PAGE_W-2*MARGIN-14*mm-58*mm, 58*mm]),
        P("Le stade est déterminé par le critère le plus péjoratif entre « créatinine plasmatique » "
          "et « diurèse ».", S_NOTE)]))
    story.append(Spacer(1, 3*mm))

    story.append(KeepTogether([
        P("<b>TABLEAU II</b> — Critères diagnostiques et de gravité de l'IRA en pédiatrie (pRIFLE)", S_H2),
        Spacer(1, 1*mm),
        simple_table(
            ["Stade", "Clairance estimée créatinine", "Diurèse"],
            [
                ["Risk (risque)", "Diminuée de > 25 %", "< 0,5 mL/kg/h pendant > 8 h"],
                ["Injury (atteinte)", "Diminuée de > 50 %", "< 0,5 mL/kg/h pendant > 16 h"],
                ["Failure (défaillance)", "Diminuée de > 75 % ou clairance < 35 mL/min/1,73 m²", "< 0,3 mL/kg/h pendant 24 h ou anurie > 12 h"],
                ["Loss (perte de fonction)", "Stade « Failure » se prolongeant > 4 semaines", "—"],
                ["End stage (IRC terminale)", "Stade « Failure » se prolongeant > 3 mois", "—"],
            ], [30*mm, PAGE_W-2*MARGIN-30*mm-52*mm, 52*mm])
    ]))
    return story

def _section_champ2_3():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Champ 2 — Stratégies de diagnostic précoce de l'IRA"))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("R2.1", "Il ne faut pas utiliser les biomarqueurs rénaux pour faire le diagnostic précoce "
                 "d'IRA.", "1-"),
        ("R2.2", "Il ne faut probablement pas utiliser l'index de résistance mesuré par le Doppler "
                 "rénal pour diagnostiquer ou traiter une IRA.", "2-"),
    ], [13*mm, PAGE_W-2*MARGIN-13*mm-15*mm, 15*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(P(
        "<b>R2.1 est la seule des 33 recommandations à n'avoir obtenu qu'un « Accord Faible »</b> lors "
        "de la cotation Delphi du groupe de relecture, malgré un grade GRADE fort (1-) — les biomarqueurs "
        "rénaux <i>(argumentaire : NGAL, KIM-1, IL-18, cystatine C, IGFBP7/TIMP-2, etc.)</i> ont un "
        "signal fort pour la détection précoce de lésions rénales (sensibilité 70-92 %, "
        "spécificité 70-95 % selon le marqueur), mais aucune étude randomisée contrôlée ne permet à ce "
        "jour de les recommander pour le diagnostic de l'IRA proprement dit.", S_NOTE))
    story.append(Spacer(1, 4*mm))

    story.append(section_bar("Champ 3 — Évaluation du risque d'IRA"))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("R3.1", "Il faut rechercher les facteurs de risque d'IRA liés au terrain et/ou au contexte "
                 "(tableau III).", "AE"),
        ("R3.2", "Il faut probablement, dans les situations à risque, surveiller la diurèse et la "
                 "créatinine plasmatique pour objectiver la survenue d'une atteinte rénale aiguë et "
                 "prendre les mesures préventives appropriées.", "AE"),
    ], [13*mm, PAGE_W-2*MARGIN-13*mm-15*mm, 15*mm]))
    story.append(Spacer(1, 3*mm))

    story.append(P("<b>TABLEAU III</b> — Principaux facteurs de risque d'IRA liés au terrain et aux procédures", S_H2))
    story.append(Spacer(1, 1*mm))
    story.append(simple_table(
        ["Terrain / pathologies sous-jacentes", "Procédures / contextes"],
        [
            ["Âge > 65 ans*, insuffisance rénale chronique*, sexe masculin, origine ethnique africaine, "
             "obésité (IMC > 40 kg/m²), hypertension artérielle, insuffisance cardiaque congestive, "
             "insuffisance hépatocellulaire, insuffisance respiratoire sévère, diabète, cancer, anémie",
             "Sepsis*, instabilité hémodynamique, période périopératoire*, chirurgie majeure* (urgence, "
             "abdomino-pelvienne, cardiovasculaire, thoracique, hémorragique), brûlures étendues, "
             "traumatismes graves, agents néphrotoxiques (médicaments, produits de contraste iodés)"],
        ], [(PAGE_W-2*MARGIN)/2, (PAGE_W-2*MARGIN)/2]))
    story.append(P("* Facteurs de risque les plus importants.", S_NOTE))
    story.append(Spacer(1, 3*mm))

    story.append(P("<b>TABLEAU IV</b> — Principaux agents néphrotoxiques responsables d'IRA en réanimation et en période périopératoire", S_H2))
    story.append(Spacer(1, 1*mm))
    story.append(KeepTogether(info_panel(P(
        "Produits de contraste iodés &nbsp;•&nbsp; Aminosides &nbsp;•&nbsp; Amphotéricine &nbsp;•&nbsp; "
        "Anti-inflammatoires non stéroïdiens &nbsp;•&nbsp; β-lactamines (néphropathies interstitielles) "
        "&nbsp;•&nbsp; Sulfamides &nbsp;•&nbsp; Aciclovir, méthotrexate, cisplatine &nbsp;•&nbsp; "
        "Ciclosporine, tacrolimus &nbsp;•&nbsp; Inhibiteurs de l'enzyme de conversion de "
        "l'angiotensine (IEC)", S_BODY_SM), bg=BG_PANEL, border=TEAL)))
    return story

def _section_champ4():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Champ 4 — Stratégies de prévention non spécifiques de l'IRA"))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("R4.1", "En réanimation, il ne faut pas utiliser les hydroxyéthylamidons (HEA).", "1-"),
        ("R4.2", "Il faut probablement préférer les cristalloïdes aux colloïdes en cas de remplissage "
                 "vasculaire.", "2+"),
        ("R4.3", "Il faut probablement préférer les solutés balancés en cas de remplissage vasculaire "
                 "important.", "2+"),
        ("R4.4", "Il faut maintenir un niveau minimal de pression artérielle moyenne (PAM) compris "
                 "entre 60 et 70 mmHg pour prévenir et traiter l'IRA.", "1+"),
        ("R4.5", "Il faut probablement considérer que les patients hypertendus requièrent "
                 "un objectif de PAM > 70 mmHg.", "2+"),
        ("R4.6", "Il faut monitorer et optimiser le volume d'éjection systolique ou ses dérivés en "
                 "période périopératoire afin de guider le remplissage vasculaire.", "1+"),
        ("R4.7", "Il faut probablement appliquer les mêmes recommandations de monitorage/optimisation "
                 "hémodynamique en réanimation.", "2+"),
        ("R4.8", "Après stabilisation hémodynamique, il faut probablement éviter la surcharge "
                 "hydro-sodée en réanimation.", "2+"),
        ("R4.9", "Si un vasoconstricteur est nécessaire, il faut probablement utiliser la noradrénaline "
                 "en première intention pour maintenir les objectifs de PAM.", "2+"),
        ("R4.10", "Il ne faut probablement pas retarder la réalisation d'examens complémentaires ou "
                  "l'administration de médicaments potentiellement néphrotoxiques s'ils sont "
                  "nécessaires à la prise en charge du patient.", "AE"),
    ], [13*mm, PAGE_W-2*MARGIN-13*mm-15*mm, 15*mm]))
    story.append(Spacer(1, 3*mm))
    story.append(info_panel(P(
        "<b>Repères cliniques (argumentaire) :</b> le comité de pharmacovigilance de l'Agence "
        "européenne du médicament (11/10/2013) a statué que les HEA ne doivent plus être utilisés chez "
        "le patient septique, de réanimation ou brûlé (usage restant possible en choc hémorragique si "
        "les cristalloïdes seuls sont insuffisants, ≤ 24 h, avec surveillance rénale 90 jours). "
        "L'hyperchlorémie associée au NaCl 0,9 % est associée à une morbidité rénale accrue par rapport "
        "aux solutés balancés (ex. : recours à l'EER 4,8 % vs 1 % dans l'étude de Shaw et al., "
        "30 994 patients de chirurgie abdominale). Un niveau de PAM &lt; 55-60 mmHg est associé à un "
        "surcroît d'IRA en chirurgie non cardiaque (33 300 patients) ; une chute peropératoire de "
        "26 mmHg de PAM est associée à un surcroît d'IRA après chirurgie cardiaque. L'optimisation "
        "hémodynamique peropératoire vise typiquement un index cardiaque de 4,5 L/min/m², un transport "
        "en oxygène de 600 mL/min/m² ou une consommation en oxygène de 170 mL/min/m².",
        S_BODY_SM), bg=BG_PANEL, border=TEAL))
    return story

def _section_champ5_6():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Champ 5 — Gestion des agents néphrotoxiques"))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("R5.1", "Il faut probablement recourir à une hydratation par cristalloïdes pour prévenir la "
                 "néphropathie associée aux produits de contraste iodés, idéalement avant l'injection "
                 "et en poursuivant l'hydratation pendant 6 à 12 heures.", "2+"),
        ("R5.2", "Il ne faut probablement pas utiliser la N-acétylcystéine et/ou le bicarbonate de "
                 "sodium en prévention de la néphropathie associée aux produits de contraste.", "2-"),
        ("R5.3", "Il faut probablement appliquer les règles suivantes lorsque l'usage d'aminosides est "
                 "nécessaire : administrer en une injection par jour ; monitorer les taux résiduels "
                 "au-delà d'une injection ; administrer au maximum 3 jours à chaque fois que possible.", "2+"),
        ("R5.4", "Il faut probablement ne pas utiliser les anti-inflammatoires non stéroïdiens (AINS), "
                 "inhibiteurs de l'enzyme de conversion (IEC) et antagonistes des récepteurs de "
                 "l'angiotensine 2 (ARA2) chez les patients à risque d'IRA.", "AE"),
    ], [13*mm, PAGE_W-2*MARGIN-13*mm-15*mm, 15*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(P(
        "<i>Argumentaire (R5.3) :</i> cette limitation à 3 jours ne s'applique pas aux infections "
        "endovasculaires/endocardites ni aux infections ostéo-articulaires sur matériel, où une durée "
        "plus longue peut être nécessaire.", S_NOTE))
    story.append(Spacer(1, 3*mm))

    story.append(section_bar("Champ 6 — Stratégies pharmacologiques de prévention et de traitement de l'IRA"))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("R6.1", "Il ne faut pas utiliser de diurétiques dans l'objectif de prévenir ou traiter une "
                 "IRA ; il faut probablement les réserver au traitement de la surcharge hydro-sodée.", "1-"),
        ("R6.2", "Il ne faut probablement pas utiliser le bicarbonate de sodium pour prévenir ou "
                 "traiter une IRA.", "2-"),
        ("R6.3", "Il ne faut pas utiliser les traitements suivants dans l'objectif de prévenir ou "
                 "traiter une IRA : mannitol, dopamine, fenoldopam, facteur atrial natriurétique, "
                 "N-acétylcystéine, insulin-like growth factor-1, érythropoïétine, antagonistes des "
                 "récepteurs de l'adénosine.", "1-"),
    ], [13*mm, PAGE_W-2*MARGIN-13*mm-15*mm, 15*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(P(
        "Deux situations particulières, non couvertes par R6.1-R6.3, gardent un traitement préventif "
        "spécifique selon l'argumentaire : (1) méthotrexate à forte dose (1-12 g/m²) — hyperhydratation "
        "≥ 2 L/m² IV et alcalinisation des urines ; (2) patients à haut risque de syndrome de lyse "
        "tumorale — la rasburicase réduit l'uricémie plus vite que l'allopurinol, sans bénéfice démontré "
        "sur l'incidence d'IRA à ce jour.", S_NOTE))
    return story

def _section_champ7_8():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Champ 7 — Modalités de nutrition en cas d'IRA"))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("R7.1", "Il faut probablement appliquer les mêmes règles de support nutritionnel chez le "
                 "patient de réanimation en présence ou non d'une IRA (sans EER).", "2+"),
        ("R7.2", "Il ne faut pas limiter les apports nutritionnels dans le seul but de prévenir la "
                 "surcharge hydro-sodée et/ou le recours à l'EER.", "1-"),
        ("R7.1 P", "<i>(Pédiatrique)</i> Il faut probablement adapter les apports protéiques en "
                    "fonction de l'âge des enfants présentant une IRA.", "2+"),
    ], [13*mm, PAGE_W-2*MARGIN-13*mm-15*mm, 15*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(P(
        "<i>Argumentaire (R7.1) :</i> à défaut de calorimétrie indirecte, apport énergétique de 20 à "
        "30 kcal/kg/j et apport protéique de 1,5 g/kg/j en l'absence d'épuration extrarénale. "
        "<i>Argumentaire pédiatrique (R7.1 P) :</i> selon les KDIGO 2012, 2-3 g/kg/j de 0 à 2 ans ; "
        "1,5-2 g/kg/j de 2 à 13 ans ; 1,5 g/kg/j après 13 ans. En présence d'une épuration extrarénale, "
        "il faut probablement majorer l'apport protéique (y compris en glutamine) et les micronutriments "
        "(vitamines hydrosolubles, oligo-éléments) — les vitamines du groupe B (B1, folates) sont "
        "éliminées en quantité significative lors de l'EER.",
        S_NOTE))
    story.append(Spacer(1, 4*mm))

    story.append(section_bar("Champ 8 — Évaluation de la récupération de la fonction rénale après IRA"))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("R8.1", "Il faut considérer à risque de survenue d'insuffisance rénale chronique les patients "
                 "ayant présenté une IRA.", "1+"),
        ("R8.2", "Il faut probablement évaluer la fonction rénale des patients ayant présenté une IRA "
                 "6 mois après la survenue de l'épisode aigu.", "2+"),
        ("R8.3", "Il faut probablement définir la non-récupération de la fonction rénale après IRA "
                 "comme suit : augmentation de la créatinine plasmatique de plus de 25 % de la valeur "
                 "de base, ou dépendance à l'EER.", "2+"),
    ], [13*mm, PAGE_W-2*MARGIN-13*mm-15*mm, 15*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(P(
        "Un suivi néphrologique systématique est conseillé chez tout patient ayant développé une IRA, "
        "quel que soit le degré de récupération apparent : une récupération biologique jugée complète "
        "peut néanmoins évoluer vers l'insuffisance rénale chronique dans 10 % des cas à 3 ans (études "
        "pédiatriques), et un suivi néphrologique à 3 mois est associé à une meilleure survie "
        "(RR 0,76 [IC95% 0,62-0,93], cohorte de 3877 patients).", S_NOTE))
    return story

def _section_figure_tracabilite():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Figure 1 — De l'agression à la dysfonction rénale", color=TEAL_DARK))
    story.append(Spacer(1, 1.5*mm))
    story.append(P(
        "<i>Redessin simplifié du schéma à cercles concentriques de la page 3 du document source "
        "(vérifié visuellement) : trois notions emboîtées, de la plus large à la plus sévère.</i>", S_NOTE))
    story.append(Spacer(1, 2*mm))
    story.append(funnel_diagram())
    story.append(Spacer(1, 3*mm))
    story.append(P(
        "L'<b>agression rénale aiguë</b> (kidney attack) désigne les situations exposant le rein à un "
        "risque d'IRA (sepsis, chirurgie majeure, agents néphrotoxiques...), sans lésion constituée. "
        "L'<b>atteinte rénale aiguë</b> (acute kidney damage) désigne une lésion parenchymateuse rénale "
        "(mise en évidence par l'histologie ou des biomarqueurs de lésion tissulaire), sans "
        "nécessairement de perte de fonction. L'<b>insuffisance rénale aiguë</b> (acute kidney injury) "
        "est le stade de dysfonction constituée, défini par les critères KDIGO (tableau I). Ces trois "
        "notions se développent conjointement plutôt que strictement séquentiellement.", S_BODY_SM))
    story.append(Spacer(1, 5*mm))

    story.append(section_bar("Sources et traçabilité", color=GREY))
    story.append(Spacer(1, 2*mm))
    story.append(P(
        "<b>Document source :</b> « Insuffisance rénale aiguë en périopératoire et en réanimation (à "
        "l'exclusion des techniques d'épuration extrarénale) » — Recommandations Formalisées d'Experts. "
        "C. Ichai, C. Vinsonneau, B. Souweine, F. Armando, E. Canet, C. Clec'h, J.-M. Constantin, "
        "M. Darmon, J. Duranteau, T. Gaillot, A. Garnier, L. Jacob, O. Joannes-Boyau, L. Juillard, "
        "D. Journois, A. Lautrette, L. Muller, M. Legrand, N. Lerolle, T. Rimmelé, E. Rondeau, "
        "F. Tamion, Y. Walrave, L. Velly — pour la Sfar, la SRLF, le GFRUP et la SFN. "
        "Coordonnateur Sfar : C. Ichai. Coordonnateur adjoint SRLF : C. Vinsonneau. 24 experts répartis "
        "en 9 groupes de travail.", S_SOURCE))
    story.append(Spacer(1, 1.5*mm))
    story.append(P("<b>Version :</b> texte validé par le Conseil d'Administration de la Sfar le "
                    "19/06/2015 et le Conseil d'Administration de la SRLF le 06/08/2015. Publié "
                    "Anesth Reanim. 2016;2:184-205, DOI 10.1016/j.anrea.2016.04.001.", S_SOURCE))
    story.append(P("<b>Méthodologie :</b> GRADE (force forte [1+/1-] ou faible [2+/2-] via GRADE Grid "
                    "et méthode Delphi ; avis d'experts lorsque la littérature ne permettait pas de "
                    "graduer). Accord fort obtenu pour 32/33 recommandations (99 %) après 2 tours de "
                    "cotation du groupe de relecture — R2.1 est la seule exception (Accord Faible).", S_SOURCE))
    story.append(P("<b>Correction d'extraction :</b> les seuils de créatininémie de R1.1 et du "
                    "Tableau I sont exprimés en µmol/L dans la source (confirmé par vérification "
                    "visuelle des pages 4-5) ; l'extraction automatique du texte fait apparaître ces "
                    "valeurs comme « mmol/L » par corruption du glyphe µ — corrigé dans cette fiche.", S_SOURCE))
    story.append(P("<b>URL source :</b> https://sfar.org/wp-content/uploads/2016/05/ANREA_132_RFE-IRA-.pdf", S_SOURCE))
    story.append(Spacer(1, 3*mm))
    story.append(info_panel(P(
        "<b>Avertissement :</b> ce document est une fiche de synthèse indépendante, produite pour un "
        "usage d'aide-mémoire. Il reprend l'intégralité des 33 recommandations et des 4 tableaux de la "
        "RFE, mais ne remplace pas le texte intégral (argumentaire complet, références "
        "bibliographiques par recommandation) et n'est ni édité ni validé par la SFAR ni la SRLF. En "
        "cas de doute, se référer au texte intégral et/ou à un avis spécialisé.",
        S_BODY_SM), bg=GREY_LIGHT, border=GREY))
    return story

def _section_1_3():
    return _section_intro_champ1() + [Spacer(1, 3*mm)] + _section_champ2_3()

def _section_4_8():
    return (_section_champ4() + [Spacer(1, 4*mm)] + _section_champ5_6()
            + [Spacer(1, 4*mm)] + _section_champ7_8() + [Spacer(1, 4*mm)]
            + _section_figure_tracabilite())

SECTIONS = [
    ("Champs 1-3 — Diagnostic, gravité, risque", _section_1_3),
    ("Champs 4-8 — Prévention, traitement, nutrition, récupération", _section_4_8),
]

def _make_doc():
    return SimpleDocTemplate(OUT, pagesize=A4,
                              leftMargin=MARGIN, rightMargin=MARGIN,
                              topMargin=32*mm, bottomMargin=16*mm,
                              title="Fiche SFAR/SRLF 2015 - Insuffisance rénale aiguë",
                              author="Synthèse indépendante (source SFAR/SRLF/GFRUP/SFN)")

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
