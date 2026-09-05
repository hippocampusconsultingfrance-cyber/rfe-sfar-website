# -*- coding: utf-8 -*-
"""
Fiche de synthese - RPP de la Societe Francaise de Neurochirurgie (SFNC) 2025
Prises en charge neurochirurgicales des traumatismes cranio-encephaliques de l'adulte et de
l'enfant a la phase initiale
Source verifiee : texte integral SFNC/SFAR/ANARLF/SFNCP/SFNCL/GFRUP/SFNR/SPILF/SOFMER, V1.13 -
19/03/2025 (R. Manet, A. Dagain), publie sur sfar.org le 19/09/2025. Methodologie GRADE
simplifiee : cette RPP ne comporte NI "GRADE 1" NI de suffixe +/- imprime sur les tags - seuls
deux niveaux existent dans le texte source lui-meme : "GRADE 2 (ACCORD FORT)" et "AVIS D'EXPERTS
(ACCORD FORT)" (la Methodologie de la source explique ce choix par le faible niveau de preuve
disponible, justifiant le recours a une RPP plutot qu'a une RFE classique). Le sens (+/-) de
chaque "GRADE 2" est ici deduit de la formulation litterale de la phrase elle-meme
("il est probablement recommande de..." = 2+, "il n'est probablement pas recommande de..." = 2-)
et non retype depuis un tag source qui ne le precise pas - disclosure explicite dans le panneau de
methodologie. 45 items numerotes au total (R1.1 a R15.2) : 43 recommandations reelles (39 avis
d'experts + 4 GRADE 2) + 2 "ABSENCE DE RECOMMANDATION" explicites (R11.4, R14.2) - ce qui
reconcilie le chiffre "43 recommandations" affiche sur la page web sfar.org avec le chiffre "45
recommandations" du resume officiel du PDF source lui-meme (45 = items numerotes totaux, 43 =
recommandations reellement formulees) : les deux chiffres sont corrects, ils comptent des choses
differentes - disclosure explicite plutot que de choisir arbitrairement l'un des deux.

Incoherence source verifiee par rendu visuel (page 11 du PDF, 200dpi) : R6.4 utilise la formule
verbale "il est probablement recommande de..." (qui suit la convention du Grade 2 telle que
definie par la Methodologie de la source elle-meme) mais est tague litteralement "AVIS D'EXPERTS"
et non "GRADE 2" - contrairement a R6.5, juste en-dessous, qui utilise la meme formule verbale et
est correctement tague "GRADE 2". Ceci est une incoherence interne au document source lui-meme
(confirmee par rendu image, pas une erreur d'extraction) : le tag litteralement imprime fait foi
(R6.4 chippee "AE"), disclosure de l'incoherence dans le panneau de methodologie plutot que
correction silencieuse.

Annexes reproduites : echelle GOSE (8 niveaux + deces), score de fragilite mFI-5 (5 items),
Clinical Frailty Scale (9 niveaux, texte integralement transcrit depuis l'image source verifiee
visuellement), score SPIN (pronostic du TC penetrant, 7 parametres). Exclusions explicites de la
source elle-meme (deja couvertes par d'autres recommandations existantes, hors champ ici) :
derivation ventriculaire externe et craniectomie decompressive chez l'adulte et l'enfant.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from style import *
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.units import mm

OUT = "/private/tmp/claude-501/-Users-macbook-Downloads-claude/65498e3e-5ddf-47a6-b100-3ac535d1faa0/scratchpad/rfe_sfar/output/Fiche_SFNC_Traumatisme_Cranien_2025.pdf"

SOURCE_TXT = ("Source : Recommandations de Pratiques Professionnelles (RPP) de la Société "
              "Française de Neurochirurgie (SFNC), avec SFNCP/SFNCL/ANARLF/SFAR/GFRUP/SFNR/"
              "SPILF/SOFMER « Prises en charge neurochirurgicales des traumatismes "
              "cranio-encéphaliques de l'adulte et de l'enfant à la phase initiale » — V1.13, "
              "19/03/2025, publiée le 19/09/2025. Méthodologie GRADE simplifiée. Fiche de "
              "synthèse non officielle : se référer au texte intégral.")

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

def legend_flowable():
    items = [("2+", "Il est probablement recommandé"), ("2-", "Il n'est probablement pas recommandé"),
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

TOTAL_PAGES = {"n": 13}

def on_page(canvas, doc, page_title):
    header_band(canvas, doc, "SFNC — RPP 2025 — PRISE EN CHARGE NEUROCHIRURGICALE",
                "Traumatisme cranio-encéphalique",
                page_title, icon_fn=lambda c,x,y: icon_shield(c, x, y, 13*mm), color=NAVY)
    footer_band(canvas, doc, SOURCE_TXT, f"Page {doc.page} / {TOTAL_PAGES['n']}")

# ---------------------------------------------------------------------------
def _section_intro():
    story = []
    story.append(Spacer(1, 3*mm))
    story.append(info_panel(P(
        "<b>Champ :</b> prise en charge neurochirurgicale des traumatismes cranio-encéphaliques "
        "(TC) de l'adulte et de l'enfant nécessitant un geste neurochirurgical à la phase "
        "initiale. Comité SFNC, avec SFNCP, SFNCL, ANARLF, SFAR, GFRUP, SFNR, SPILF, SOFMER ; "
        "méthode GRADE®, format PICO, 7 champs / 15 questions. <b>Exclusions explicites de la "
        "source</b> (déjà couvertes par d'autres recommandations existantes) : dérivation "
        "ventriculaire externe et craniectomie décompressive, chez l'adulte comme chez "
        "l'enfant.<br/><br/>"
        "<b>Résultats (résumé officiel) :</b> 45 items formulés ; accord fort obtenu pour "
        "l'ensemble dès le premier tour de cotation. Parmi ces 45 items, 43 sont des "
        "recommandations réelles (39 avis d'experts + 4 « GRADE 2 ») et 2 sont des « ABSENCE DE "
        "RECOMMANDATION » explicites — ce qui réconcilie le chiffre « 43 » affiché sur la page "
        "sfar.org avec le chiffre « 45 » du résumé officiel du document lui-même : les deux "
        "sont corrects, ils ne comptent simplement pas la même chose.<br/><br/>"
        "<i>Première RPP portée spécifiquement par la neurochirurgie depuis 2006 — les "
        "recommandations françaises existantes sur le TC (SFAR/SFMU sur le TC léger et grave, "
        "monitorage cérébral) ne couvraient pas les indications et modalités des gestes "
        "neurochirurgicaux eux-mêmes.</i>",
        S_BODY), bg=BG_PANEL, border=TEAL))
    story.append(Spacer(1, 3*mm))

    story.append(section_bar("Légende des grades"))
    story.append(Spacer(1, 2*mm))
    story.append(legend_flowable())
    story.append(Spacer(1, 3*mm))
    story.append(info_panel(P(
        "<b>Méthodologie GRADE simplifiée</b> — cette RPP ne comporte ni palier « GRADE 1 » ni "
        "suffixe +/- imprimé sur ses tags (contrairement aux RFE classiques du site) : seuls "
        "deux niveaux existent littéralement dans le texte source, « GRADE 2 (ACCORD FORT) » et "
        "« AVIS D'EXPERTS (ACCORD FORT) ». Le sens (+/-) de chaque « GRADE 2 » est ici déduit de "
        "la formulation littérale de la phrase elle-même — « il est probablement recommandé "
        "de… » = 2+, « il n'est probablement pas recommandé de… » = 2- — et non retypé depuis un "
        "tag source qui ne le précise pas. <b>Incohérence source relevée</b> (vérifiée par rendu "
        "visuel de la page 11) : R6.4 utilise la formule verbale du Grade 2 (« il est "
        "probablement recommandé ») mais est littéralement taguée « AVIS D'EXPERTS » — le tag "
        "imprimé fait foi (chippée « AE » ci-après), incohérence signalée plutôt que corrigée "
        "silencieusement.",
        S_BODY_SM), bg=AMBER_LIGHT, border=AMBER))
    return story

def _section_champ1():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Champ 1 — Facteurs de mauvais pronostic (craniotomie en urgence, adulte)"))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("R1.1", "Chez le patient présentant un TC grave, nécessitant théoriquement une "
         "craniotomie en urgence, mais présentant des caractéristiques jugées « dépassées » (ne "
         "laissant aucun espoir de pronostic favorable), l'abstention neurochirurgicale précoce "
         "(avant 72h) doit systématiquement faire l'objet d'une décision collégiale, impliquant "
         "chaque fois que possible trois médecins séniors (neurochirurgien, anesthésiste-"
         "réanimateur, médecin rééducateur).", "AE"),
        ("R1.2", "En période de permanence des soins, une « collégialité restreinte » doit être "
         "mise en œuvre, impliquant au moins 2 médecins séniors pour permettre une meilleure "
         "évaluation du pronostic.", "AE"),
        ("R2.1", "Chez un patient victime de TC grave nécessitant une craniotomie en urgence, il "
         "est probablement recommandé de considérer les indices de fragilité pathologiques pour "
         "évaluer le pronostic, mais pas de manière isolée pour contre-indiquer le geste.", "2+"),
        ("R2.2", "Les scores suivants (détaillés en annexe ci-dessous) peuvent être considérés "
         "comme pathologiques pour évaluer le pronostic : mFI-5 ≥ 2 ; Clinical Frailty Scale "
         "≥ 4.", "AE"),
        ("R3", "Chez un patient présentant un TC grave nécessitant une craniotomie en urgence, la "
         "présence à la prise en charge d'une mydriase bilatérale aréactive non régressive "
         "(idéalement évaluée par pupillométrie automatisée) doit être considérée comme un "
         "facteur de mauvais pronostic, mais ne doit pas être considérée de manière isolée pour "
         "contre-indiquer le geste, en particulier si la mydriase est installée depuis moins de "
         "2h.", "AE"),
        ("R4", "Chez un patient victime de TC grave nécessitant une craniotomie en urgence, il "
         "ne faut pas prendre en compte le délai de prise en charge de manière isolée dans "
         "l'évaluation du pronostic et la décision neurochirurgicale.", "AE"),
        ("R5.1", "Chez les patients nécessitant une craniotomie en urgence, en particulier chez "
         "ceux de plus de 65 ans, il est probablement recommandé de considérer, de manière non "
         "isolée, la présence d'un traitement anticoagulant (AVK ou AOD) comme facteur de "
         "mauvais pronostic, mais sans que cela ne contre-indique le geste de manière "
         "isolée.", "2+"),
        ("R5.2", "Chez un patient présentant un TC grave nécessitant une craniotomie en urgence, "
         "il n'est probablement pas recommandé de considérer la présence d'un traitement "
         "anti-agrégant plaquettaire en monothérapie par aspirine comme un facteur de mauvais "
         "pronostic ; cela ne doit pas influencer l'indication opératoire.", "2-"),
    ], [15*mm, PAGE_W-2*MARGIN-15*mm-20*mm, 20*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(P("Les LATA précoces (&lt;72h) sont la première cause de décès après TC grave "
                    "(45-87 % de la mortalité hospitalière). Mydriase bilatérale aréactive : "
                    "évolution favorable (GOSE&gt;4) chez seulement 6,6 % des HSDA vs 54,3 % des "
                    "HED (méta-analyse, 82 patients) ; chirurgie de décompression ultra-précoce "
                    "(≤2h) = ~1 chance sur 3 de survie. Traitement AC préalable : surmortalité "
                    "significative dans de nombreuses études (OR 1,3 à 5,2 selon les cohortes) — "
                    "double AAP (OR 4,66), warfarine (OR 5,18), AOD (OR 5,09). Monothérapie "
                    "aspirine : aucune différence de mortalité retrouvée (revue de 2447 patients "
                    "sous AAP vs 4814 contrôles).", S_NOTE))
    story.append(Spacer(1, 3*mm))
    cw = PAGE_W - 2*MARGIN
    story.append(simple_table(
        ["mFI-5 (frailty index)", "Items (+1 chacun)", "Interprétation"],
        [["mFI-5", "Diabète • HTA • Défaillance cardiaque congestive (OAP &lt;30j) • BPCO • "
          "Non autonome", "0 = non fragile • 1 = vulnérable • ≥2 = fragile"]],
        [cw*0.20, cw*0.55, cw*0.25]))
    return story

def _section_champ2():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Champ 2 — Hématomes extra-duraux"))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("R6.1", "Chez le patient présentant un TC associé à un hématome extra-dural (HED), il "
         "faut réaliser l'évacuation chirurgicale en urgence dans l'une ou plusieurs des "
         "circonstances suivantes : GCS ≤ 8 ; mydriase ; volume &gt; 30 mL ; déviation de la "
         "ligne médiane &gt; 5 mm ; compression du tronc cérébral ; signe de saignement actif "
         "(swirl sign).", "AE"),
        ("R6.2", "Il faut privilégier un traitement conservateur en cas d'HED d'origine "
         "artérielle sans signe de gravité clinique et radiologique (cf. R6.1).", "AE"),
        ("R6.3", "Pour un HED d'origine veineuse, il faut évaluer la balance bénéfice-risque "
         "d'une prise en charge conservatrice au cas par cas, y compris en présence de signe de "
         "gravité, compte tenu des difficultés chirurgicales (plaie de sinus dural).", "AE"),
        ("R6.4", "En cas de décision de traitement conservateur, il faut effectuer une "
         "surveillance clinique rapprochée dans un centre doté d'un service de "
         "neurochirurgie.", "AE"),
        ("R6.5", "En cas de traitement conservateur, il est probablement recommandé de réaliser "
         "un scanner de contrôle systématiquement à 6 heures post-traumatisme (si le premier "
         "scanner a été fait avant H6), ou plus précocement en cas d'aggravation clinique.", "2+"),
    ], [15*mm, PAGE_W-2*MARGIN-15*mm-20*mm, 20*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(P("HED &gt;25-30mL = risque majoré de dégradation neurologique. Swirl sign "
                    "(saignement actif) : présent dans 14-30 % des HED, GOS moyen 3,58 vs 4,43 "
                    "sans ce signe. HED de fosse cérébrale postérieure : chirurgie si "
                    "volume &gt;10mL, épaisseur &gt;15mm ou déviation &gt;5mm (Brain Trauma "
                    "Foundation). 98,1 % des HED atteignent leur taille finale entre 5 et 6h post-"
                    "traumatisme — d'où le scanner de contrôle ciblé à H6 ; scanner répété à 2h si "
                    "altération clinique précoce. Attention particulière si lésion controlatérale "
                    "opérée (risque d'aggravation rapide de l'HED restant après décompression "
                    "controlatérale).", S_NOTE))
    return story

def _section_champ3():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Champ 3 — Hématomes sous-duraux aigus"))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("R7.1", "Il faut réaliser l'évacuation chirurgicale en urgence d'un hématome sous-dural "
         "aigu (HSDA) dans les circonstances suivantes, cumulativement : âge &lt;65 ans (ou "
         "65-80 ans avec score de fragilité faible) ET troubles de vigilance (GCS≤8 et/ou GCS≤12 "
         "mais perte rapide de ≥2 points de GCS) non expliqués par un autre mécanisme, ou HTIC "
         "réfractaire ET critères radiologiques (épaisseur &gt;10mm et/ou déviation de la ligne "
         "médiane &gt;5mm).", "AE"),
        ("R7.2", "En cas de resaignement au sein d'un hématome sous-dural chronique, il faut "
         "envisager une chirurgie différée, moins invasive.", "AE"),
        ("R7.3", "En dehors des circonstances ci-dessus, il faut préférer un traitement "
         "conservateur, avec scanner de contrôle : en urgence si évolution clinique péjorative ; "
         "précocement (7-10j) si réintroduction d'un traitement antithrombotique ; à distance "
         "(3-4 semaines) dans les autres cas.", "AE"),
    ], [15*mm, PAGE_W-2*MARGIN-15*mm-20*mm, 20*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(P("Critères classiques de la Brain Trauma Foundation (GCS≤8 et/ou "
                    "épaisseur&gt;10mm et/ou déviation&gt;5mm) établis sur des séries anciennes "
                    "de patients jeunes — nuancés ici par l'âge et la fragilité. GCS initial à 3 : "
                    "mortalité 65-100 %. Mydriase bilatérale associée à un HSDA : mortalité "
                    "66,4 %, évolution favorable (GOS≥4) chez seulement 6,6 % (méta-analyse, "
                    "82 patients). Bénéfice chirurgical démontré en mortalité (réduction absolue "
                    "23-40 %) mais pas en devenir neurologique (2 études récentes convergentes, "
                    "dont la cohorte CENTER-TBI, 1407 patients).", S_NOTE))
    return story

def _section_champ4():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Champ 4 — Embarrures et brèches ostéo-durales de la base du crâne"))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("R8.1", "En cas d'embarrure, il faut réaliser une prise en charge chirurgicale rapide "
         "(dans les 24h), afin d'améliorer le pronostic neurologique ou esthétique, dans l'une "
         "ou plusieurs des circonstances suivantes : plaie complexe/contaminée ou signes "
         "d'infection locale ; plaie durale suspectée/pneumencéphalie ; issue de LCS ; effet de "
         "masse significatif ; autre(s) lésion(s) neurochirurgicale(s) ; préjudice esthétique "
         "majeur.", "AE"),
        ("R8.2", "En cas d'embarrure des sinus frontaux, il faut réaliser une réduction/"
         "ostéosynthèse de la paroi antérieure, en l'absence de défect majeur de la paroi "
         "postérieure, de brèche durale évidente, ou d'atteinte des canaux naso-frontaux. Sinon, "
         "le geste doit être complété par une cranialisation des sinus frontaux.", "AE"),
        ("R8.3", "En cas de TC non pénétrant associé à une embarrure et à une crise épileptique, "
         "il faut instaurer une prophylaxie antiépileptique secondaire ; une prophylaxie "
         "primaire ne doit pas être systématique.", "AE"),
        ("R9.1", "En cas de brèche ostéoméningée (BOM) traumatique, il faut réaliser une "
         "chirurgie rapide (dans les 24h) uniquement en cas de défect dural majeur associé à une "
         "liquorrhée abondante. En cas d'indication neurochirurgicale pour d'autres lésions "
         "associées, la fermeture de la BOM dans le même temps opératoire est déconseillée en "
         "cas d'hypertension intracrânienne.", "AE"),
        ("R9.2", "Il faut envisager la chirurgie en cas de liquorrhée non abondante réfractaire "
         "à un traitement conservateur au-delà de 7 jours.", "AE"),
        ("R9.3", "Il faut associer au traitement conservateur des BOM un alitement en proclive à "
         "30°, ainsi que la prescription de laxatifs, d'antitussifs et d'antiémétiques pendant "
         "au moins 72h.", "AE"),
        ("R9.4", "Il faut réaliser ou mettre à jour les vaccinations suivantes : "
         "anti-pneumococcique (vaccin conjugué 15-valent chez le moins de 18 ans, 1 dose chez le "
         "plus de 2 ans ; ou 20-valent chez le plus de 18 ans, 1 dose non suivie de vaccin "
         "non-conjugué) ; anti-Haemophilus influenzae (1 dose) ; anti-méningococcique B et ACYW "
         "(rattrapage selon les recommandations générales : méningocoque ABCYW avant 2 ans et "
         "ACYW avant 25 ans).", "AE"),
        ("R9.5", "Il faut débuter la recherche d'une BOM traumatique par un scanner en fenêtre "
         "osseuse (coupes millimétriques) et une IRM incluant des séquences 3DT2 haute "
         "résolution. En cas de doute persistant, un myéloscanner puis une cisternographie "
         "isotopique peuvent être réalisés.", "AE"),
    ], [15*mm, PAGE_W-2*MARGIN-15*mm-20*mm, 20*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(P("Embarrures : lésions généralement de bon pronostic ; toute embarrure ouverte "
                    "impose d'éliminer une brèche durale (= TC pénétrant, champ 5). Reconstruction "
                    "préférentiellement en ostéosynthèse titane. Fuites de LCS : surviennent dans "
                    "0,3-39 % des fractures de la base du crâne ; &gt;50 % dans les 48h, 70 % dans "
                    "les 7j. Risque de méningite : 0,24 % à 24h, cumulatif ~1,3 %/jour (15 "
                    "premiers jours) puis 7,4 %/semaine (1er mois) — chute de 30,6 % (avant "
                    "chirurgie) à 4 % (après) en cas de fuite persistante. Traitement conservateur "
                    "(proclive 30° + laxatifs/antitussifs/antiémétiques 48-72h) : tarissement "
                    "dans 39,5-68 % des cas à J2-3. Petits défects (≤1cm) : voie endonasale "
                    "endoscopique ; défects &gt;1cm : voie haute. Pas d'antibioprophylaxie "
                    "systématique en cas de simple fracture de la base du crâne (RFE SFAR/SPILF "
                    "2023), sauf en cas d'intervention neurochirurgicale.", S_NOTE))
    return story

def _section_champ5():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Champ 5 — Traumatismes cranio-encéphaliques pénétrants"))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("R10.1", "Il faut évaluer et prendre en compte le risque de mortalité (score SPIN, "
         "score de Maritzburg), de manière non isolée, dans l'indication d'une intervention "
         "chirurgicale en urgence.", "AE"),
        ("R10.2", "Chez un patient avec un score de Glasgow ≥ 5, il faut proposer une prise en "
         "charge neurochirurgicale en urgence.", "AE"),
        ("R10.3", "La prise en charge neurochirurgicale doit être discutée au cas par cas pour "
         "les patients avec un score de Glasgow ≤ 4, en l'absence de mydriase bilatérale "
         "aréactive et en l'absence de lésions scanographiques de mauvais pronostic (cf. "
         "critères ci-dessous).", "AE"),
        ("R10.4", "En cas de délabrement cortical important, il faut réaliser une prophylaxie "
         "antiépileptique primaire pour une période d'au moins 7 jours, afin de réduire le "
         "risque épileptique à court terme.", "AE"),
        ("R10.5", "Il faut réaliser ou mettre à jour les vaccinations suivantes : chez la "
         "personne non à jour, vaccination antitétanique associée à une injection de 250 UI "
         "d'immunoglobulines humaines antitétaniques en cas de plaie étendue, pénétrante avec "
         "corps étranger ou traitée tardivement ; anti-méningococcique B et ACYW (rattrapage "
         "selon les recommandations générales : méningocoque ABCYW avant 2 ans et ACYW avant "
         "25 ans) ; anti-Haemophilus influenzae (1 dose) ; anti-pneumococcique (vaccin conjugué "
         "15-valent chez le moins de 18 ans, 1 dose chez le plus de 2 ans ; ou 20-valent chez le "
         "plus de 18 ans, 1 dose non suivie de vaccin non-conjugué).", "AE"),
        ("R11.1", "Il faut rechercher de manière systématique des lésions vasculaires "
         "intracrâniennes par angioscanner.", "AE"),
        ("R11.2", "Il faut compléter ce bilan par une artériographie cérébrale par soustraction "
         "numérique 6 axes en présence d'un ou plusieurs des facteurs suivants : détection/doute "
         "sur lésion vasculaire à l'angioscanner ; blessure ptérionale et/ou fronto-orbitaire ; "
         "violation durale multiple ; trajectoire/hématome à proximité des axes vasculaires "
         "principaux ; TC (fermé ou pénétrant) par explosion avec GCS &lt;8 ; vasospasme au "
         "doppler transcrânien et/ou baisse spontanée inexpliquée de la PtiO2.", "AE"),
        ("R11.3", "En cas de lésion vasculaire intracrânienne symptomatique ou asymptomatique à "
         "haut risque de rupture et/ou d'aggravation neurologique, il faut discuter d'un "
         "traitement en urgence.", "AE"),
    ], [15*mm, PAGE_W-2*MARGIN-15*mm-20*mm, 20*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(no_reco_panel("sur la modalité (endovasculaire ou chirurgicale) du traitement "
                                "d'une lésion vasculaire intracrânienne post-traumatique, qui "
                                "doit être discutée collégialement (R11.4)."))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("R11.5", "En l'absence d'authentification de lésion vasculaire intracrânienne initiale, "
         "il faut répéter une nouvelle imagerie cérébro-vasculaire à environ 14 jours du "
         "traumatisme.", "AE"),
    ], [15*mm, PAGE_W-2*MARGIN-15*mm-20*mm, 20*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(P("TC pénétrants : mortalité jusqu'à 85 % ; prise en charge agressive augmente "
                    "la survie. GCS initial = principal facteur pronostique (0 % de bon "
                    "pronostic si GCS 6-8 en conservateur vs 24 % si opéré ; 77,8 % de bons "
                    "résultats si GCS≥9 opéré). Chirurgie idéalement dans les 5h (réduction du "
                    "risque infectieux). Lésions vasculaires intracrâniennes : jusqu'à 60 % des "
                    "TC pénétrants ; anévrismes post-traumatiques 20-50 % d'incidence, mortalité "
                    "jusqu'à 50 % en cas de rupture. Artériographie = gold standard (angioscanner "
                    "moins sensible). Épilepsie précoce (7j) : 14-20 % d'incidence. "
                    "Antibioprophylaxie : amoxicilline-acide clavulanique 2g, poursuivie 24-48h "
                    "si plaie souillée (RFE SFAR/SPILF 2023).", S_NOTE))
    story.append(Spacer(1, 3*mm))
    cw = PAGE_W - 2*MARGIN
    story.append(simple_table(
        ["Score SPIN (pronostic TC pénétrant)", "Items", "Points"],
        [["SPIN", "GCS moteur (1-5 → 0 ; 6 → 9) • Pupilles (non réactives bilat. → 0 ; "
          "unilat. → 4 ; globe rompu → 6 ; normales → 9) • Blessure auto-infligée (oui → 0 ; "
          "non → 4) • Transfert d'un autre hôpital (non → 0 ; oui → 4) • Sexe (masculin → 0 ; "
          "féminin → 4) • ISS (≥56 → 0 ; 41-55 → 1 ; 25-40 → 5 ; ≤24 → 10) • INR (≥2,1 → 0 ; "
          "1,4-2 → 6 ; ≤1,3 → 12)",
          "Score ≥ 35 : 98 % de survie. Score ≤ 20 : 3 % de survie."]],
        [cw*0.15, cw*0.65, cw*0.20]))
    story.append(Spacer(1, 2*mm))
    story.append(P("<b>Critères scanographiques de mauvais pronostic dans le TC pénétrant :</b> "
                    "trajectoire multilobaire ou bihémisphérique (hors lésions bilatérales des "
                    "lobes frontaux) • trajectoire trans-ventriculaire • trajectoire traversant "
                    "le centre géographique du cerveau • trajectoire oblique dans les 3 plans "
                    "(x, y et z) • fragmentation diffuse • volume important de cerveau contus • "
                    "hémorragie intracérébrale importante • hémorragie sous-arachnoïdienne • "
                    "plaie de la fosse postérieure avec implication du tronc cérébral • signe "
                    "des « rails de tramway » (hémorragie de part et d'autre d'une piste "
                    "centrale sombre dans une blessure perforante) • déplacement de la ligne "
                    "médiane &gt; 10 mm • citernes basales comprimées ou oblitérées.", S_BODY_SM))
    return story

def _section_champ6():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Champ 6 — Désordres hydrauliques post-traumatiques"))
    story.append(Spacer(1, 2*mm))
    story.append(info_panel(P(
        "<b>Deux entités à distinguer</b> — <b>Hygrome :</b> collection de LCS généralement "
        "stable (rarement progressive), unilatérale, absence de signe neurologique, PIC "
        "normale. <b>Hydrocéphalie externe :</b> collection de LCS progressive (sur scanners "
        "successifs), généralement bilatérale, ET aggravation neurologique ET/OU élévation de "
        "la PIC.",
        S_BODY_SM), bg=BG_PANEL, border=TEAL))
    story.append(Spacer(1, 3*mm))
    story.append(reco_table([
        ("R12.1", "En cas d'hygrome, il faut réaliser un traitement conservateur en première "
         "intention.", "AE"),
        ("R12.2", "En cas d'hydrocéphalie externe, il faut drainer le LCS (ponction lombaire ou "
         "dérivation lombaire externe), après confirmation au scanner de : la perméabilité des "
         "citernes de la base ET l'absence de déviation de la ligne médiane &gt; 10mm ET "
         "l'absence d'engagement amygdalien. En cas d'hypertension intracrânienne, cette option "
         "ne doit être envisagée qu'après échec des mesures de 1ère ligne.", "AE"),
        ("R12.3", "En cas de dérivation lombaire externe pour hydrocéphalie externe, il faut "
         "placer le zéro de référence à hauteur du conduit auditif externe. En cas "
         "d'hypertension intracrânienne, un monitorage continu de la PIC doit être réalisé, et "
         "la contre-pression de drainage lombaire ne doit pas être abaissée en dessous de "
         "10 mmHg. Le drainage lombaire doit être interrompu en cas de gradient de pression "
         "&gt; 5 mmHg entre la PIC et la pression lombaire du LCS.", "AE"),
    ], [15*mm, PAGE_W-2*MARGIN-15*mm-20*mm, 20*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(P("Revue systématique de 10 études (221 patients) sur la dérivation lombaire "
                    "externe (DLE) dans le TC : réduction moyenne de PIC de -17,1 mmHg (-59,1 %). "
                    "Complications : méningite 5,7 % (12/208), engagement amygdalien 7,1 % "
                    "(21/295) — survenu surtout dans les études à contre-pression 0 ou +5cmH2O. "
                    "Critères scanographiques utilisés dans toutes les études : liberté des "
                    "citernes de la base, absence d'effet de masse significatif, absence de "
                    "déviation &gt;5-10mm, absence d'engagement uncal/amygdalien. Le drainage "
                    "lombaire externe n'a pas été retenu comme mesure thérapeutique de l'HTIC "
                    "post-traumatique par la conférence internationale de Seattle 2019.", S_NOTE))
    return story

def _section_champ7():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Champ 7 — Particularités pédiatriques"))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("R13.1", "Chez le nouveau-né (&lt;1 mois) avec TC associé à un hématome extradural "
         "(HED), il faut réaliser l'évacuation chirurgicale en urgence en présence de signes de "
         "gravité cliniques ou radiologiques (déviation &gt;5mm de la ligne médiane, compression "
         "du tronc cérébral).", "AE"),
        ("R13.2", "En l'absence de consensus sur la technique chirurgicale optimale, il faut "
         "privilégier des approches moins invasives avant de recourir à une craniotomie : "
         "ponction du céphalhématome, ponction via une fracture crânienne, ou ponction "
         "épidurale (notamment si HED sans fracture ni céphalhématome).", "AE"),
        ("R13.3", "En l'absence de signes de gravité (cf. R13.1), il faut privilégier une "
         "approche conservatrice, avec surveillance étroite en unité de soins intensifs (examens "
         "cliniques rapprochés et imagerie de contrôle).", "AE"),
        ("R14.1", "Chez le nourrisson (&lt;2 ans) avec TC non accidentel associé à un hématome "
         "sous-dural, il faut réaliser une prise en charge chirurgicale rapide, "
         "préférentiellement par drainage.", "AE"),
    ], [15*mm, PAGE_W-2*MARGIN-15*mm-20*mm, 20*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(no_reco_panel("sur l'utilisation de la craniectomie décompressive dans les TC "
                                "non accidentels du nourrisson (R14.2)."))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("R14.3", "Il faut envisager une prise en charge conservatrice en présence d'un "
         "hématome sous-dural chronique de faible épaisseur (&lt;10mm), bien toléré cliniquement, "
         "avec surveillance rapprochée et contrôle de l'imagerie.", "AE"),
        ("R15.1", "Chez le nourrisson (&lt;2 ans) avec embarrure type fracture « ping-pong », il "
         "faut réaliser une prise en charge chirurgicale en urgence en cas d'hypertension "
         "intracrânienne, ou d'effet de masse significatif sur le parenchyme, ou d'hématome "
         "intracrânien, ou de collection de LCS péri-encéphalique.", "AE"),
        ("R15.2", "En l'absence des critères ci-dessus, il faut privilégier initialement une "
         "prise en charge conservatrice ; une prise en charge chirurgicale pourra être "
         "ré-évaluée en l'absence d'évolution favorable.", "AE"),
    ], [15*mm, PAGE_W-2*MARGIN-15*mm-20*mm, 20*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(P("HED néonatal : rare (incidence des hémorragies intracrâniennes post-"
                    "instrumentales 0,4-1 %), souvent d'origine veineuse, tendance à se liquéfier "
                    "rapidement — approche conservatrice si épaisseur &lt;20mm, sans déviation ni "
                    "détérioration clinique ; chirurgie si volume &gt;30mL, épaisseur &gt;15mm, "
                    "déviation &gt;5mm. Craniotomie néonatale : éviter la fixation par matériel "
                    "d'ostéosynthèse (croissance crânienne ultérieure). Syndrome du bébé secoué "
                    "(HSD du nourrisson) : entité sans équivalent adulte (mélange sang+LCR) ; "
                    "mauvais pronostic corrélé à la sévérité clinique initiale, pas aux "
                    "complications de la dérivation ; ponction sous-durale transfontanellaire en "
                    "1ère intention si HTIC, dérivation sous-duro-péritonéale si récidive ; place "
                    "de la craniectomie décompressive non établie dans ce contexte spécifique "
                    "(« Big Black Brain » à l'admission = contre-indication). Fracture "
                    "« ping-pong » : incidence 1-2,5/10 000 nés vivants ; revue de 228 nourrissons "
                    "— 30 % chirurgie, 30 % aspiration, 40 % conservateur, &gt;96 % d'évolution "
                    "neurologique favorable quel que soit le type de prise en charge.", S_NOTE))
    return story

def _section_synthese():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Synthèse et messages clés"))
    story.append(Spacer(1, 2*mm))
    story.append(P(
        "• Décision d'abstention neurochirurgicale précoce (avant 72h) = toujours collégiale "
        "(3 médecins séniors, ou 2 en permanence de soins restreinte). Fragilité (mFI-5≥2, "
        "CFS≥4), mydriase bilatérale aréactive et délai de prise en charge = facteurs "
        "pronostiques à considérer mais jamais isolément décisifs.<br/>"
        "• HED : évacuation en urgence si GCS≤8, mydriase, volume&gt;30mL, déviation&gt;5mm, "
        "compression du tronc, swirl sign. Conservateur si artériel sans gravité ou veineux "
        "au cas par cas — scanner de contrôle à H6.<br/>"
        "• HSDA : évacuation en urgence si âge&lt;65 ans (ou fragilité faible) ET troubles de "
        "vigilance/HTIC réfractaire ET épaisseur&gt;10mm/déviation&gt;5mm. Conservateur sinon, "
        "avec scanner adapté au contexte.<br/>"
        "• Embarrure : chirurgie sous 24h si plaie complexe/contaminée, brèche durale/"
        "pneumencéphalie, issue de LCS, effet de masse, ou préjudice esthétique majeur. "
        "Sinus frontaux : préserver si paroi postérieure/canaux naso-frontaux intacts, sinon "
        "cranialiser. Brèche ostéoméningée : chirurgie si défect majeur + liquorrhée "
        "abondante, sinon conservateur (proclive 30°, laxatifs/antitussifs/antiémétiques "
        "≥72h) puis chirurgie si échec &gt;7j.<br/>"
        "• TC pénétrant : GCS≥5 → prise en charge neurochirurgicale en urgence ; GCS≤4 sans "
        "mydriase ni critères scanographiques péjoratifs → discussion au cas par cas. "
        "Angioscanner systématique ± artériographie 6 axes selon critères. Chirurgie "
        "idéalement &lt;5h. Vaccinations et antibioprophylaxie à jour.<br/>"
        "• Désordres hydrauliques : hygrome = conservateur ; hydrocéphalie externe = drainage "
        "après vérification scanographique stricte (citernes libres, déviation&lt;10mm, pas "
        "d'engagement).<br/>"
        "• Pédiatrie : HED néonatal souvent gérable médicalement (approches mini-invasives "
        "avant craniotomie) ; HSD non accidentel du nourrisson = drainage rapide, gravité "
        "corrélée à la présentation clinique initiale ; fracture « ping-pong » = conservateur "
        "sauf signes de gravité, pronostic favorable dans &gt;96 % des cas quelle que soit la "
        "prise en charge.",
        S_BODY))
    story.append(Spacer(1, 4*mm))

    story.append(section_bar("Annexes — GOSE"))
    story.append(Spacer(1, 2*mm))
    cw = PAGE_W - 2*MARGIN
    story.append(simple_table(
        ["GOSE", "Niveau", "Évolution"],
        [
            ["1", "Mort", "Mauvaise évolution neurologique"],
            ["2", "État végétatif", "Mauvaise évolution neurologique"],
            ["3", "Handicap sévère — niveau inférieur (totalement dépendant)", "Mauvaise évolution neurologique"],
            ["4", "Handicap sévère — niveau supérieur (très dépendant)", "Mauvaise évolution neurologique"],
            ["5", "Handicap moyen — niveau inférieur (partiellement dépendant)", "Bonne évolution neurologique"],
            ["6", "Handicap moyen — niveau supérieur (retour partiel au travail/école)", "Bonne évolution neurologique"],
            ["7", "Bonne récupération — niveau inférieur (séquelles légères)", "Bonne évolution neurologique"],
            ["8", "Bonne récupération — niveau supérieur (récupération complète)", "Bonne évolution neurologique"],
        ],
        [cw*0.10, cw*0.60, cw*0.30]))
    story.append(Spacer(1, 3*mm))

    story.append(section_bar("Sources et traçabilité", color=GREY))
    story.append(Spacer(1, 2*mm))
    story.append(P(
        "<b>Document source :</b> « Prises en charge neurochirurgicales des traumatismes "
        "cranio-encéphaliques de l'adulte et de l'enfant à la phase initiale » — RPP de la SFNC, "
        "avec SFNCP/SFNCL/ANARLF/SFAR/GFRUP/SFNR/SPILF/SOFMER. V1.13, 19/03/2025 "
        "(R. Manet, A. Dagain, H. de Courson, J.F. Payen), publiée sur sfar.org le 19/09/2025.", S_SOURCE))
    story.append(Spacer(1, 1.5*mm))
    story.append(P("<b>Méthodologie :</b> GRADE® simplifié à 2 niveaux (« GRADE 2 » et « Avis "
                    "d'experts », sans palier « GRADE 1 » ni suffixe +/- imprimé) — le sens +/- "
                    "de chaque « GRADE 2 » est déduit de la formulation littérale de la phrase, "
                    "disclosure en page 1. Incohérence source relevée et signalée (R6.4, "
                    "vérifiée par rendu visuel) plutôt que corrigée silencieusement.", S_SOURCE))
    story.append(Spacer(1, 1.5*mm))
    story.append(P("<b>Couverture :</b> 45 items reproduits intégralement (R1.1-R15.2) — 43 "
                    "recommandations réelles + 2 « Absence de recommandation » (R11.4, R14.2). "
                    "Annexes reproduites : GOSE (ci-dessus), mFI-5 (Champ 1), score SPIN et "
                    "critères scanographiques de mauvais pronostic du TC pénétrant (Champ 5). La "
                    "Clinical Frailty Scale (9 niveaux), transcrite depuis une image source "
                    "(page 50, sans couche de texte), n'est pas reproduite intégralement ici par "
                    "souci de place — se référer au texte intégral pour sa version complète ; "
                    "seul le seuil retenu par les experts (CFS ≥ 4 = fragile) est cité (R2.2). "
                    "Exclusions explicites de la source elle-même : dérivation ventriculaire "
                    "externe et craniectomie décompressive (adulte et enfant), déjà couvertes "
                    "par d'autres recommandations existantes.", S_SOURCE))
    story.append(Spacer(1, 3*mm))
    story.append(info_panel(P(
        "<b>Avertissement :</b> ce document est une fiche de synthèse indépendante, produite pour "
        "un usage d'aide-mémoire. Il reprend l'intégralité des recommandations de la RPP mais ne "
        "remplace pas le texte intégral et n'est ni édité ni validé par la SFNC/SFAR. En cas de "
        "doute, se référer au texte intégral, aux recommandations ultérieures et/ou à un avis "
        "spécialisé.",
        S_BODY_SM), bg=GREY_LIGHT, border=GREY))
    return story

SECTIONS = [
    ("Introduction, méthodologie", _section_intro),
    ("Champ 1 — Facteurs de mauvais pronostic", _section_champ1),
    ("Champ 2 — Hématomes extra-duraux", _section_champ2),
    ("Champ 3 — Hématomes sous-duraux aigus", _section_champ3),
    ("Champ 4 — Embarrures & brèches ostéo-durales", _section_champ4),
    ("Champ 5 — TC pénétrants", _section_champ5),
    ("Champ 6 — Désordres hydrauliques post-traumatiques", _section_champ6),
    ("Champ 7 — Particularités pédiatriques", _section_champ7),
    ("Synthèse, annexes, sources & traçabilité", _section_synthese),
]

def _make_doc():
    return SimpleDocTemplate(OUT, pagesize=A4,
                              leftMargin=MARGIN, rightMargin=MARGIN,
                              topMargin=32*mm, bottomMargin=16*mm,
                              title="Fiche SFNC 2025 - Traumatisme cranio-encéphalique",
                              author="Synthèse indépendante (source SFNC/SFAR)")

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
