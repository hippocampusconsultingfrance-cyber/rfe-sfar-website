# -*- coding: utf-8 -*-
"""
Fiche de synthese - SFAR / SPILF (avec 32 societes savantes associees), RFE 2024
"Antibioprophylaxie en chirurgie et medecine interventionnelle adulte et pediatrique"
V3.0 du 04/05/2026 (V1.0 originale du 08/12/2023).
Source : sources/antibioprophylaxie_full.txt (122 pages, extraction PyMuPDF integrale).

PERIMETRE EXPLICITEMENT PARTIEL (disclosure, cf. regle qualite #2) : le document source
couvre 3 "champs" : Champ 1 = 11 recommandations generales (questions transversales,
applicables a toute procedure), Champ 2 = 9 tableaux disciplinaires ADULTES par specialite
chirurgicale/interventionnelle (neurochirurgie, ORL/ophtalmo/maxillo-facial, cardiaque/
vasculaire, thoracique, plastique/brules, gyneco-obstetrique, orthopedie/traumato,
digestive/bariatrique, urologie), Champ 3 = les 9 memes tableaux en version PEDIATRIQUE/
neonatale. Les Champs 2 et 3 sont des tableaux de POSOLOGIE PAR PROCEDURE (antibiotique,
dose, voie, reinjection) consultes au cas par cas au bloc, pas des recommandations de
synthese narrative — ils totalisent ~85 pages et ne se pretent pas a une fiche de synthese
unique (chaque discipline necessiterait sa propre fiche-tableau). Cette fiche couvre donc
INTEGRALEMENT le Champ 1 (les 11 recommandations generales, applicables quelle que soit la
discipline), et exclut explicitement les Champs 2 et 3 - disclosure faite dans le panneau
d'introduction, pas d'omission silencieuse. Cf. CLAUDE.md, meme convention que les fiches
sepsis/anaphylaxie deja construites pour des sources surdimensionnees.

METHODOLOGIE : GRADE (R1.1-R1.7.3, 11 recommandations au total, comme annonce dans la
synthese des resultats de la source). La source imprime UNIQUEMENT "GRADE 1 (accord FORT)",
"GRADE 2 (accord FORT)" ou "Avis d'experts (accord FORT)" - jamais de suffixe +/- (verifie
par grep sur l'integralite du Champ 1, cf. tache). Aucun "GRADE 1+/2-" n'est donc invente ;
les chips utilisent les labels imprimes tels quels ("GRADE 1", "GRADE 2", "AE"), extension
locale non invasive de GRADE_COLORS (meme pattern que fiche_aap_programmee.py/"Fort").
Toutes les 11 recommandations ont obtenu un accord FORT (>=70% des experts) - pas de
recommandation a accord faible dans ce champ.

R1.5.2 (dose amoxicilline-clavulanate chez l'obese) est un ajout de la V3.0 (04/05/2026,
cf. historique des versions source, page 5-6) - la fiche integre donc la version la plus
recente du document, teicoplanine explicitement "non recommandee" chez l'obese (absence de
donnee) est disclosee comme telle dans R1.6, pas convertie en un chip separe.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from style import *
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.units import mm

GRADE_COLORS["GRADE 1"] = (GREEN, WHITE)
GRADE_COLORS["GRADE 2"] = (TEAL, WHITE)
# "AE" (avis d'experts) deja present dans GRADE_COLORS partage (gris).

OUT = os.path.join(os.path.dirname(__file__), "..", "output",
                    "Fiche_SFAR_SPILF_Antibioprophylaxie_Champ1_2024.pdf")
OUT = os.path.abspath(OUT)

SOURCE_TXT = ("Source : SFAR / SPILF (32 sociétés savantes associées) — RFE « Antibioprophylaxie "
              "en chirurgie et médecine interventionnelle adulte et pédiatrique » — V3.0 du "
              "04/05/2026 (V1.0 originale 08/12/2023). Fiche non officielle, limitée au Champ 1 : "
              "se référer au texte intégral pour les tableaux disciplinaires (Champs 2-3).")

def P(txt, style=S_CELL):
    return Paragraph(txt, style)

def chip(label, **kw):
    return grade_chip(label, **kw)

def reco_table(rows, col_widths):
    """rows: (ref, text, grade_label) — recommandations numerotees R1.x de la source."""
    data = [[P("Réf.", S_HEAD_W), P("Recommandation", S_HEAD_W), P("Niveau", S_HEAD_W_C)]]
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
    chip_w = 20*mm
    content_w = PAGE_W - 2*MARGIN
    text_w = content_w - chip_w
    rows = [
        ("GRADE 1", "Niveau de preuve global « fort » — recommandation forte (« il est "
         "recommandé de… » / « il n'est pas recommandé de… »)."),
        ("GRADE 2", "Niveau de preuve global modéré ou faible — recommandation optionnelle "
         "(« il est probablement recommandé de… » / « il n'est probablement pas recommandé "
         "de… »)."),
        ("AE", "Avis d'experts — littérature insuffisante pour graduer ; consensus formalisé "
         "du groupe d'experts (« les experts suggèrent… »)."),
    ]
    data = []
    for label, txt in rows:
        data.append([chip(label, width=chip_w-2*mm), P(txt, S_BADGE_HEAD)])
    t = Table(data, colWidths=[chip_w, text_w])
    t.setStyle(TableStyle([("VALIGN",(0,0),(-1,-1),"MIDDLE"), ("LEFTPADDING",(0,0),(-1,-1),1),
                            ("RIGHTPADDING",(0,0),(-1,-1),1), ("TOPPADDING",(0,0),(-1,-1),2),
                            ("BOTTOMPADDING",(0,0),(-1,-1),2)]))
    return t

TOTAL_PAGES = {"n": 6}

def on_page(canvas, doc, page_title):
    header_band(canvas, doc, "SFAR / SPILF — RFE 2024 (V3.0 · 2026) — FICHE DE SYNTHÈSE",
                "Antibioprophylaxie — Champ 1 (recommandations générales)",
                page_title, icon_fn=lambda c, x, y: icon_pill(c, x, y, 13*mm), color=NAVY)
    footer_band(canvas, doc, SOURCE_TXT, f"Page {doc.page} / {TOTAL_PAGES['n']}")

# ---------------------------------------------------------------------------
def _section_intro():
    story = []
    story.append(Spacer(1, 3*mm))
    story.append(info_panel(P(
        "<b>Champ :</b> antibioprophylaxie (prévention médicamenteuse de l'infection du site "
        "opératoire, ISO) en chirurgie et médecine interventionnelle — patients adultes et "
        "pédiatriques, chirurgies propres et propres-contaminées (classes 1-2 d'Altemeier). "
        "RFE de la SFAR et de la Société de Pathologie Infectieuse de Langue Française (SPILF), "
        "en association avec 32 sociétés savantes de chirurgie et médecine interventionnelle. "
        "V3.0 du 04/05/2026 (V1.0 originale du 08/12/2023 ; Champ 3 pédiatrique ajouté en V3.0).<br/><br/>"
        "<b>Méthodologie :</b> méthode GRADE® — analyse qualitative et quantitative de la "
        "littérature (recherche bibliographique MEDLINE/Cochrane/clinicaltrials.gov, janvier "
        "2000 à mars 2023, méthodologie PRISMA), cotation collective par grille GRADE Grid "
        "(validation à ≥ 70 % d'opinions convergentes et &lt; 20 % d'opinions contraires). "
        "Un seul critère de jugement « majeur » : l'infection du site opératoire.",
        S_BODY), bg=BG_PANEL, border=TEAL))
    story.append(Spacer(1, 3*mm))
    story.append(info_panel(P(
        "<b>Périmètre de cette fiche — partiel, disclosure explicite :</b> le document source "
        "traite <b>3 champs</b> : <b>Champ 1</b> — 11 recommandations générales, applicables à "
        "toute procédure quelle que soit la discipline (objet intégral de cette fiche) ; "
        "<b>Champ 2</b> — 9 tableaux disciplinaires <b>adultes</b> (neurochirurgie/neuroradiologie "
        "interventionnelle ; ORL/ophtalmologie/chirurgie maxillo-faciale ; chirurgie cardiaque/"
        "cardiologie interventionnelle/rythmologie/chirurgie vasculaire ; chirurgie thoracique/"
        "endoscopie thoracique/radiologie interventionnelle ; chirurgie plastique et "
        "reconstructrice/d'affirmation de genre/du patient brûlé ; chirurgie gynécologique et "
        "obstétrique ; chirurgie orthopédique et traumatologique ; chirurgie digestive et "
        "bariatrique/endoscopie et médecine interventionnelle digestive ; chirurgie urologique) ; "
        "<b>Champ 3</b> — 9 tableaux disciplinaires <b>pédiatriques et néonatals</b>, reprenant "
        "globalement les mêmes disciplines que le Champ 2, à deux différences près : la "
        "chirurgie gynécologique et obstétrique du Champ 2 n'a <b>pas</b> de tableau pédiatrique "
        "dédié, remplacée par un tableau spécifique de <b>chirurgie néonatalogique</b>. Les "
        "Champs 2 et 3 sont des <b>tableaux de posologie par procédure</b> (molécule, dose, voie, "
        "délai de réinjection), consultés au cas par cas au bloc opératoire — ils totalisent "
        "environ 85 pages et ne se prêtent pas à une fiche de synthèse narrative unique. "
        "<b>Cette fiche ne couvre donc PAS les Champs 2 et 3</b> : pour le choix et la posologie "
        "de l'antibioprophylaxie d'une procédure donnée, se référer directement au tableau "
        "disciplinaire correspondant dans le texte intégral.",
        S_BODY_SM), bg=AMBER_LIGHT, border=AMBER))
    story.append(Spacer(1, 3*mm))
    story.append(section_bar("Légende (grades GRADE de la source)"))
    story.append(Spacer(1, 2*mm))
    story.append(legend_flowable())
    story.append(Spacer(1, 2*mm))
    story.append(P("<i>Rappel de la source :</i> plus la force de la recommandation est faible "
                    "(avis d'experts &lt; GRADE 2 &lt; GRADE 1), plus une déclinaison locale "
                    "argumentée et pluridisciplinaire peut s'en écarter. Ce référentiel ne "
                    "traite pas de la définition de l'allergie aux bêtalactamines, ni de la "
                    "prévention de l'endocardite infectieuse (cf. recommandations européennes "
                    "2023 dédiées).", S_NOTE))
    return story

def _section_delai():
    story = []
    story.append(Spacer(1, 2*mm))
    cw = PAGE_W - 2*MARGIN
    story.append(KeepTogether([
        section_bar("Quand administrer l'antibioprophylaxie ?"),
        Spacer(1, 2*mm),
        reco_table([
            ("R1.1", "Il est recommandé d'administrer l'antibioprophylaxie par céphalosporine "
             "(ou ses alternatives en cas d'allergie, hors vancomycine) au plus tôt 60 minutes "
             "avant et au plus tard avant l'incision chirurgicale ou le début de la procédure "
             "interventionnelle, pour diminuer l'incidence d'ISO.", "GRADE 1"),
            ("R1.2", "En cas d'utilisation de la vancomycine, les experts suggèrent d'en débuter "
             "l'administration intraveineuse sur 60 minutes chez le patient non obèse au plus "
             "tôt 60 minutes avant, et au plus tard 30 minutes avant l'incision ou le début de "
             "la procédure, pour diminuer l'incidence d'ISO.", "AE"),
        ], [16*mm, cw-16*mm-22*mm, 22*mm]),
    ]))
    story.append(Spacer(1, 2*mm))
    story.append(P("<b>Argumentaire clé :</b> une administration après l'incision est associée à "
                    "un surrisque d'ISO (méta-analyse De Jonge 2017, OR 1,89 [1,05-3,40]) ; le "
                    "délai optimal se situe dans les 60 minutes précédant l'incision, sans "
                    "différence démontrée entre 60-30 min et 30-0 min. Une administration avant "
                    "l'induction anesthésique facilite l'imputabilité d'une éventuelle réaction "
                    "allergique. Pour la vancomycine, le délai optimal se situe entre 60 et 30 "
                    "minutes avant l'incision (un début trop précoce ou trop tardif est associé à "
                    "un surrisque d'ISO) ; dilution ≤ 5 mg/mL et antihistaminique prophylactique "
                    "réduisent les effets indésirables liés à la perfusion.", S_NOTE))
    return story

def _section_reinjection():
    story = []
    story.append(Spacer(1, 3*mm))
    cw = PAGE_W - 2*MARGIN
    story.append(KeepTogether([
        section_bar("Réinjection peropératoire"),
        Spacer(1, 2*mm),
        reco_table([
            ("R1.3.1", "Il est recommandé de réadministrer une à plusieurs dose(s) "
             "peropératoire(s) d'antibioprophylaxie en cas de prolongation de la chirurgie ou "
             "de l'acte interventionnel, pour diminuer l'incidence d'ISO.", "GRADE 1"),
            ("R1.3.2", "Il est probablement recommandé de réadministrer cette (ces) dose(s), à "
             "la moitié de la dose initiale, toutes les 2 demi-vies de l'antibiotique utilisé, "
             "pour diminuer l'incidence d'ISO.", "GRADE 2"),
        ], [16*mm, cw-16*mm-22*mm, 22*mm]),
    ]))
    story.append(Spacer(1, 2*mm))
    story.append(P("<b>Rythme de réinjection peropératoire</b> (posologie = moitié de la dose "
                    "initiale) :", S_CELL_B))
    story.append(Spacer(1, 1*mm))
    story.append(simple_table(
        ["Toutes les 2 h", "Toutes les 4 h", "Toutes les 8 h", "Pas de réinjection"],
        [["Céfoxitine (1 g)<br/>Céfuroxime (0,75 g)<br/>Amoxicilline/clavulanate (1 g)",
          "Céfazoline (1 g)<br/>Clindamycine (450 mg)", "Vancomycine (10 mg/kg)",
          "Gentamicine, métronidazole, teicoplanine<br/>(demi-vie très longue)"]],
        [cw/4.0]*4))
    story.append(Spacer(1, 2*mm))
    story.append(P("<i>Réadministration également à discuter en cas de saignement peropératoire "
                    "important et/ou de perfusion de grands volumes et/ou de transfusion de "
                    "plusieurs CGR, même si le délai normalement prévu n'est pas atteint (avis "
                    "d'experts, pas de seuil consensuel formulé en recommandation).</i>", S_NOTE))
    return story

def _section_duree():
    story = []
    story.append(Spacer(1, 3*mm))
    cw = PAGE_W - 2*MARGIN
    story.append(KeepTogether([
        section_bar("Durée de l'antibioprophylaxie"),
        Spacer(1, 2*mm),
        reco_table([
            ("R1.4", "Il n'est pas recommandé, dans la très grande majorité des cas (et hors "
             "exceptions mentionnées dans chaque tableau disciplinaire), de prolonger "
             "l'administration de l'antibioprophylaxie au-delà de la fin de la chirurgie, pour "
             "diminuer l'incidence d'ISO.", "GRADE 1"),
        ], [16*mm, cw-16*mm-22*mm, 22*mm]),
    ]))
    story.append(Spacer(1, 2*mm))
    story.append(P("<b>Argumentaire clé :</b> 33 méta-analyses (2000-2022) comparant "
                    "administration « courte » (peropératoire, ≤ 24 h postopératoires) vs. "
                    "« prolongée » (&gt; 24 h à 7 j) ne retrouvent, à de rares exceptions près "
                    "(chirurgie cardiaque, chirurgie orthognatique — données anciennes ou "
                    "contradictoires), aucune supériorité d'une administration prolongée. Quand "
                    "une prolongation pourrait exceptionnellement se discuter (à ne pas confondre "
                    "avec une antibiothérapie préemptive ou probabiliste), aucun argument ne "
                    "justifie de dépasser 48 heures postopératoires.", S_NOTE))
    return story

def _section_obese():
    story = []
    story.append(Spacer(1, 3*mm))
    cw = PAGE_W - 2*MARGIN
    story.append(KeepTogether([
        section_bar("Adaptation chez le patient obèse"),
        Spacer(1, 2*mm),
        reco_table([
            ("R1.5.1", "Il n'est probablement pas recommandé d'augmenter la dose unitaire de "
             "céphalosporine chez le patient obèse pour diminuer l'incidence d'ISO, en dehors "
             "de cas particuliers (notamment IMC &gt; 50 kg/m²).", "GRADE 2"),
            ("R1.5.2", "Les experts suggèrent de ne pas augmenter la dose unitaire "
             "d'amoxicilline-clavulanate chez le patient obèse, en dehors de cas particuliers "
             "(notamment IMC &gt; 50 kg/m²).", "AE"),
            ("R1.6", "Pour les alternatives aux bêtalactamines en cas d'allergie, les experts "
             "suggèrent d'utiliser des doses adaptées à l'IMC chez le patient obèse (détail "
             "ci-dessous), pour diminuer l'incidence d'ISO.", "AE"),
        ], [16*mm, cw-16*mm-22*mm, 22*mm]),
    ]))
    story.append(Spacer(1, 2*mm))
    story.append(P("<b>Rationnel R1.5.1/R1.5.2 :</b> céphalosporines (céfazoline, céfoxitine, "
                    "céfuroxime) et amoxicilline sont hydrophiles — leur volume de distribution "
                    "n'augmente pas proportionnellement à la masse grasse. Un bolus de 2 g de "
                    "céfazoline atteint la cible pharmacocinétique chez l'obèse jusqu'à la fin de "
                    "la chirurgie ou 4 h après injection (données PK/PD les plus étoffées), sans "
                    "bénéfice clinique démontré d'une dose supérieure (3 g) sur l'incidence d'ISO "
                    "dans plusieurs cohortes. Pour la céfoxitine (2 g), les concentrations "
                    "restent au-dessus de la cible jusqu'à 2 h après injection (intervalle de "
                    "réinjection) ; pour le céfuroxime, les données disponibles (bolus de 1,5 g) "
                    "montrent de même des concentrations satisfaisantes jusqu'à au moins 2 h.", S_NOTE))
    story.append(Spacer(1, 2*mm))
    story.append(P("<b>R1.6 — doses détaillées chez le patient obèse (alternatives aux "
                    "bêtalactamines) :</b>", S_CELL_B))
    story.append(Spacer(1, 1*mm))
    story.append(simple_table(
        ["Molécule", "Dose chez le patient obèse"],
        [
            ["Clindamycine", "900 mg pour IMC 30-45 kg/m² ; 1200 mg pour IMC 46-60 kg/m² ; "
                              "1600 mg pour IMC &gt; 60 kg/m²"],
            ["Gentamicine", "6 à 7 mg/kg de poids ajusté (identique au non-obèse, calcul sur "
                             "poids ajusté = poids idéal + 0,4 × [poids total − poids idéal])"],
            ["Vancomycine", "20 mg/kg de poids total (comme chez le non-obèse)"],
            ["Teicoplanine", "Non recommandée chez le patient obèse (absence de donnée dans "
                              "cette population)"],
        ], [40*mm, cw-40*mm]))
    return story

def _section_eblse():
    story = []
    story.append(Spacer(1, 3*mm))
    cw = PAGE_W - 2*MARGIN
    story.append(KeepTogether([
        section_bar("Patient colonisé au niveau rectal à E-BLSE (chirurgie colo-rectale)"),
        Spacer(1, 2*mm),
        reco_table([
            ("R1.7.1", "Dans les centres où la prévalence de colonisation digestive à "
             "entérobactéries productrices de BLSE (E-BLSE) des patients opérés de chirurgie "
             "colorectale est ≥ 10 %, les experts suggèrent un dépistage de la colonisation "
             "rectale à E-BLSE dans le mois précédant la chirurgie, pour adapter "
             "l'antibioprophylaxie et diminuer l'incidence d'ISO.", "AE"),
            ("R1.7.2", "En cas de positivité du dépistage, les experts suggèrent d'administrer, "
             "pour une chirurgie colo-rectale, une antibioprophylaxie ciblée active sur la "
             "souche d'E-BLSE identifiée, pour diminuer l'incidence d'ISO.", "AE"),
            ("R1.7.3", "Les experts suggèrent une prise en charge multidisciplinaire (anesthésiste-"
             "réanimateur, chirurgien, infectiologue ou référent en infectiologie, "
             "microbiologiste) pour individualiser l'antibioprophylaxie des patients colonisés "
             "au niveau rectal à E-BLSE en chirurgie colo-rectale.", "AE"),
        ], [16*mm, cw-16*mm-22*mm, 22*mm]),
    ]))
    story.append(Spacer(1, 2*mm))
    story.append(P("<b>Argumentaire clé :</b> la colonisation à E-BLSE multiplie par ~1,6 le "
                    "risque d'ISO toutes bactéries confondues, et par ~7 le risque d'ISO à E-BLSE "
                    "(méta-analyse Righi et al.). Chez les porteurs, une antibioprophylaxie "
                    "ciblée (ertapénème 2 g IV lent en dose unique, ou alternative efficace sur "
                    "la souche — céfoxitine, amoxicilline/clavulanate, pipéracilline/tazobactam) "
                    "réduit l'incidence d'ISO par rapport à une antibioprophylaxie standard "
                    "(étude Nutman : NNT = 13). Dans un objectif d'épargne des carbapénèmes, "
                    "l'administration systématique de carbapénème n'est <b>pas</b> synonyme "
                    "d'antibioprophylaxie ciblée : plusieurs alternatives actives sur certaines "
                    "souches d'E-BLSE existent. Seuil de 10 % retenu par analogie avec la "
                    "définition OMS d'une colonisation « élevée », en l'absence de seuil "
                    "prospectivement validé.", S_NOTE))
    return story

def _section_sources():
    story = []
    story.append(Spacer(1, 4*mm))
    story.append(section_bar("Sources et traçabilité", color=GREY))
    story.append(Spacer(1, 2*mm))
    story.append(P(
        "<b>Document source :</b> « Antibioprophylaxie en chirurgie et médecine interventionnelle "
        "adulte et pédiatrique » — Recommandations Formalisées d'Experts (RFE) de la Société "
        "Française d'Anesthésie et Réanimation (SFAR) et de la Société de Pathologie Infectieuse "
        "de Langue Française (SPILF), en association avec 32 sociétés savantes (AFU, SFR/RI, "
        "SFCR, SFO, SFSCMFCO, SFORL, ADARPEF, SOFCOT, SPLF, SFCTCV, SFC, CNGOF, SCVE, SFNC, SFB, "
        "SOFCPRE, SFED, SFCD, ACHBT, CARO, GPIP, SFOP, SOFOP, SFCP, SFCPP, SFUPA, AFOP, GFHFNP, "
        "SFNCP, SFN, et autres). Coordonnateurs : Marc Leone (SFAR, Marseille), Mathilde de "
        "Queiroz (SFAR, Lyon, partie pédiatrique), Rémy Gauzit (SPILF, Paris). Organisateurs : "
        "Marc Garnier (Clermont-Ferrand), Maxime Nguyen (Dijon, partie pédiatrique).", S_SOURCE))
    story.append(Spacer(1, 1.5*mm))
    story.append(P("<b>Validation :</b> Champs 1-2 (introduction, recommandations générales, "
                    "tableaux adultes) — CRC SFAR 15/06/2023, CA SFAR 30/06/2023, comité des "
                    "référentiels SPILF 06/09/2023, puis conseils d'administration des sociétés "
                    "associées entre septembre et décembre 2023 (validation tacite au "
                    "30/11/2023 pour les autres). Champ 3 (tableaux pédiatriques) — CRC SFAR "
                    "26/03/2026, CA SFAR 20/05/2026, SPILF 02/03/2026, GPIP 27/01/2026, puis "
                    "conseils d'administration des sociétés pédiatriques associées entre "
                    "décembre 2025 et mars 2026.", S_SOURCE))
    story.append(Spacer(1, 1.5*mm))
    story.append(P("<b>Historique des versions :</b> V1.0 (08/12/2023, version originale) ; "
                    "V1.1-V2.0 (déc. 2023 - mai 2024, corrections de coquilles et clarifications "
                    "dans les tableaux disciplinaires) ; <b>V3.0 (04/05/2026)</b> — ajout de la "
                    "recommandation R1.5.2 (dose d'amoxicilline-clavulanate chez l'obèse), "
                    "clarification de R1.6, et ajout du Champ 3 (9 tableaux pédiatriques et "
                    "néonatals) ; V3.1 (10/07/2026) — amendement d'un schéma de chirurgie "
                    "digestive néonatale. Cette fiche reflète la V3.0/V3.1.", S_SOURCE))
    story.append(Spacer(1, 1.5*mm))
    story.append(P("<b>Méthodologie :</b> méthode GRADE® — recherche bibliographique MEDLINE/"
                    "Cochrane/clinicaltrials.gov (janvier 2000 - mars 2023), méthodologie PRISMA, "
                    "cotation GRADE Grid par les experts (accord retenu à ≥ 70 % d'opinions "
                    "convergentes et &lt; 20 % d'opinions contraires ; avis d'experts systématiquement "
                    "soumis au même seuil de 70 %). Les 11 recommandations du Champ 1 ont toutes "
                    "obtenu un accord fort.", S_SOURCE))
    story.append(Spacer(1, 1.5*mm))
    story.append(P("<b>Couverture :</b> cette fiche reprend l'intégralité des <b>11 "
                    "recommandations du Champ 1</b> (recommandations générales) — délai "
                    "d'administration, réinjection peropératoire, durée, adaptation chez "
                    "l'obèse, patient colonisé à E-BLSE — avec leur argumentaire clé. Elle "
                    "<b>exclut explicitement</b> les Champs 2 et 3 (18 tableaux disciplinaires "
                    "adultes et pédiatriques de posologie par procédure, ~85 pages) : voir le "
                    "panneau de périmètre en page 1 et se référer au texte intégral pour le "
                    "choix et la dose de l'antibioprophylaxie d'une procédure donnée.", S_SOURCE))
    story.append(Spacer(1, 3*mm))
    story.append(info_panel(P(
        "<b>Avertissement :</b> ce document est une fiche de synthèse indépendante, produite "
        "pour un usage d'aide-mémoire, limitée au Champ 1 (recommandations générales) de la "
        "RFE SFAR/SPILF 2024 (V3.0 du 04/05/2026). Elle ne remplace pas le texte intégral "
        "(argumentaire complet, références bibliographiques, tableaux disciplinaires des "
        "Champs 2-3) et n'est ni éditée ni validée par la SFAR, la SPILF ou les sociétés "
        "savantes associées. En cas de doute, se référer au texte intégral et/ou à un avis "
        "spécialisé (infectiologue, référent antibiothérapie).",
        S_BODY_SM), bg=GREY_LIGHT, border=GREY))
    return story

def _section_1():
    return _section_intro()

def _section_2():
    return _section_delai() + _section_reinjection()

def _section_3():
    return _section_duree() + _section_obese()

def _section_4():
    return _section_eblse() + _section_sources()

SECTIONS = [
    ("Introduction, méthodologie, périmètre & légende", _section_1),
    ("Délai d'administration & réinjection peropératoire", _section_2),
    ("Durée & adaptation chez le patient obèse", _section_3),
    ("Patient colonisé à E-BLSE & traçabilité", _section_4),
]

def _make_doc(path=None):
    return SimpleDocTemplate(path or OUT, pagesize=A4,
                              leftMargin=MARGIN, rightMargin=MARGIN,
                              topMargin=32*mm, bottomMargin=16*mm,
                              title="Fiche SFAR/SPILF 2024 - Antibioprophylaxie (Champ 1)",
                              author="Synthèse indépendante (source SFAR/SPILF)")

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
    # Throwaway temp path (never OUT) for measurement-only builds — reusing OUT here was
    # found (in an earlier fiche) to silently corrupt page 1's header_band in the final PDF.
    import pypdf, tempfile
    tmp_path = tempfile.mktemp(suffix=".pdf")
    doc = _make_doc(tmp_path)
    doc.build(story_flowables, onFirstPage=_silent_page, onLaterPages=_silent_page)
    with open(tmp_path, "rb") as f:
        n = len(pypdf.PdfReader(f).pages)
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
