# -*- coding: utf-8 -*-
"""
Fiche de synthese - RFE SFAR 2019 (actualisation de 2003/2004)
Prise en charge des patients presentant, ou a risque, de traumatisme vertebro-medullaire
Source verifiee : RFE SFAR, avec ANARLF/SFCR/SFMU/SOFCOT/SOFMER/SSA, texte valide par le Comite des
Referentiels Cliniques (15/05/2019) et le CA SFAR (24/05/2019). Methodologie GRADE standard (tags
"GRADE 1+/-" et "GRADE 2+/-" imprimes litteralement, contrairement a la fiche traumatisme_cranien
du meme corpus qui n'utilisait qu'un GRADE 2 sans signe). 19 recommandations (R1.1-R12.1) :
2 GRADE1 (R5.1 = 1-, R10.2 = 1+), 12 GRADE2 (tous 2+), 5 avis d'experts (R2.1, R3.2, R6.1, R9.2,
R11.1) - resume officiel "19 recommandations, 2 GRADE1, 12 GRADE2, 5 avis d'experts, accord fort
pour 100%" independamment reverifie item par item et confirme coherent, sans exception cette fois
(contrairement a plusieurs fiches du corpus dont le resume agrege ne se reconciliait pas
exactement avec un decompte independant).

Deux algorithmes (Figure 1 - immobilisation rachidienne ; Figure 2 - procedure d'intubation
tracheale), tous deux des diagrammes de decision avec branches (avis d'experts, non
numerotes individuellement comme R-items mais rattaches aux questions 1 et 8 respectivement) -
transcrits en tableaux de decision condenses apres rendu visuel des pages 10 et 21 a 200dpi
(l'extraction texte de ces deux pages produit un ordre de lecture disloque, propre aux
diagrammes avec boites/fleches ; verifie que la logique de branchement transcrite correspond
exactement au diagramme source, et non a un ordre de lecture errone du texte brut).
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from style import *
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.units import mm

OUT = "/private/tmp/claude-501/-Users-macbook-Downloads-claude/65498e3e-5ddf-47a6-b100-3ac535d1faa0/scratchpad/rfe_sfar/output/Fiche_SFAR_Traumatisme_Vertebromedullaire_2019.pdf"

SOURCE_TXT = ("Source : Recommandations Formalisées d'Experts SFAR, avec ANARLF/SFCR/SFMU/SOFCOT/"
              "SOFMER/SSA « Prise en charge des patients présentant, ou à risque, de traumatisme "
              "vertébro-médullaire » — 2019, texte validé par le CRC et le CA SFAR le 24/05/2019. "
              "Méthodologie GRADE. Fiche de synthèse non officielle : se référer au texte intégral.")

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

def legend_flowable():
    items = [("1+", "Il faut faire"), ("1-", "Il ne faut pas faire"),
             ("2+", "Il faut probablement"), ("2-", "Il ne faut probablement pas"),
             ("AE", "Avis d'experts")]
    content_w = PAGE_W - 2*MARGIN
    n = len(items)
    chip_w = 14*mm
    text_w = (content_w - n*chip_w) / n
    row_cells, col_widths = [], []
    for g, txt in items:
        row_cells.append(chip(g, width=chip_w-1.5*mm))
        row_cells.append(P(txt, S_BADGE_HEAD))
        col_widths += [chip_w, text_w]
    row = Table([row_cells], colWidths=col_widths)
    row.setStyle(TableStyle([("VALIGN",(0,0),(-1,-1),"MIDDLE"), ("LEFTPADDING",(0,0),(-1,-1),1), ("RIGHTPADDING",(0,0),(-1,-1),1)]))
    return row

TOTAL_PAGES = {"n": 9}

def on_page(canvas, doc, page_title):
    header_band(canvas, doc, "SFAR — RFE 2019 — FICHE DE SYNTHÈSE",
                "Traumatisme vertébro-médullaire",
                page_title, icon_fn=lambda c,x,y: icon_shield(c, x, y, 13*mm), color=NAVY)
    footer_band(canvas, doc, SOURCE_TXT, f"Page {doc.page} / {TOTAL_PAGES['n']}")

# ---------------------------------------------------------------------------
def _section_intro():
    story = []
    story.append(Spacer(1, 3*mm))
    story.append(info_panel(P(
        "<b>Champ :</b> prise en charge du patient traumatisé avec ou à risque de lésion "
        "médullaire (adulte). Actualisation de la conférence d'experts de 2004. Comité SFAR, "
        "avec ANARLF, SFCR, SFMU, SOFCOT, SOFMER et le SSA ; méthode GRADE®, format PICO, "
        "12 questions.<br/><br/>"
        "<b>Résultats (résumé officiel) :</b> 19 recommandations ; 2 de niveau de preuve élevé "
        "(GRADE 1+/-), 12 de niveau de preuve faible (GRADE 2+/-), 5 avis d'experts. Accord fort "
        "obtenu pour 100 % des recommandations après deux tours de cotation.<br/><br/>"
        "<i>En France, l'incidence des traumatismes médullaires est d'environ 2000 cas par an, "
        "touchant le plus souvent des hommes.</i>",
        S_BODY), bg=BG_PANEL, border=TEAL))
    story.append(Spacer(1, 3*mm))

    story.append(section_bar("Légende des grades (méthodologie GRADE)"))
    story.append(Spacer(1, 2*mm))
    story.append(legend_flowable())
    return story

def _section_q1_2():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Q1 — Immobilisation du rachis"))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("R1.1", "Il faut probablement immobiliser précocement le rachis de tout patient "
         "traumatisé suspect de lésion rachidienne pour limiter l'apparition ou l'aggravation "
         "d'un déficit neurologique à la phase initiale.", "2+"),
    ], [15*mm, PAGE_W-2*MARGIN-15*mm-20*mm, 20*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(P("46 % des patients avec lésion médullaire (étude rétrospective, 59 patients) "
                    "avaient subi une aggravation lésionnelle secondaire à une mobilisation, "
                    "probablement évitable dans 90 % des cas. Rachis cervical : maintien de tête "
                    "avec blocs latéraux, ou à défaut minerve cervicale rigide. Rachis "
                    "thoraco-lombaire : plan dur = gold standard pour l'extraction (mais "
                    "complications cutanées si usage prolongé) ; matelas à dépression recommandé "
                    "pour le transport (plus confortable, maintien équivalent au plan dur).", S_NOTE))
    story.append(Spacer(1, 3*mm))
    cw = PAGE_W - 2*MARGIN
    story.append(simple_table(
        ["Situation", "Conduite"],
        [
            ["Urgence vitale", "Extraction rapide avec maintien de l'axe tête-cou-tronc "
             "(minerve rigide)."],
            ["Pas d'urgence vitale, et aucun des critères suivants : douleur en regard des "
             "apophyses épineuses, troubles de la conscience, déficit neurologique focalisé, "
             "alcoolisation ou douleur distractive", "Pas d'immobilisation — transport sur "
             "matelas coquille."],
            ["Pas d'urgence vitale, et au moins un des critères ci-dessus présent",
             "Extraction sur plan dur + immobilisation cervicale (fixateur de tête)."],
        ],
        [cw*0.55, cw*0.45]))
    story.append(Spacer(1, 1.5*mm))
    story.append(P("Figure 1 (source) — Algorithme sur l'immobilisation rachidienne des patients "
                    "avec ou à risque de lésion médullaire cervicale (Avis d'experts) — transcrit "
                    "en tableau de décision, vérifié visuellement (page 10).", S_NOTE))
    story.append(Spacer(1, 4*mm))

    story.append(section_bar("Q2 — Intubation oro-trachéale en préhospitalier"))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("R2.1", "Chez le patient avec ou à risque de lésion médullaire cervicale, les experts "
         "suggèrent une stabilisation manuelle en ligne, associée à un retrait de la partie "
         "antérieure du collier cervical pendant les manœuvres d'intubation trachéale afin de "
         "limiter la mobilisation du rachis cervical et favoriser l'exposition glottique.", "AE"),
        ("R2.2", "Chez le patient avec ou à risque de lésion médullaire cervicale, pour "
         "l'intubation trachéale en préhospitalier, il faut probablement réaliser une procédure "
         "intégrant induction en séquence rapide avec laryngoscopie directe, utilisation d'une "
         "bougie type mandrin d'Eschmann et maintien du rachis cervical dans l'axe sans manœuvre "
         "de Sellick pour augmenter le taux de succès à la première tentative.", "2+"),
    ], [15*mm, PAGE_W-2*MARGIN-15*mm-20*mm, 20*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(P("Stabilisation manuelle en ligne (SMEL) : réduction majeure des complications "
                    "dans les séries historiques, mais augmente le taux d'intubation difficile "
                    "(moins bonne exposition en laryngoscopie directe) — l'ouverture du collier "
                    "cervical au moment de l'intubation améliore l'ouverture de bouche et "
                    "l'exposition glottique. Vidéolaryngoscopie non recommandée en première "
                    "intention en préhospitalier sur les données de la seule étude prospective "
                    "randomisée disponible.", S_NOTE))
    return story

def _section_q3_4():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Q3 — Objectifs de la réanimation hémodynamique"))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("R3.1", "Chez le patient avec risque de lésion médullaire, il faut probablement "
         "maintenir un niveau de pression artérielle systolique &gt; 110 mmHg avant réalisation "
         "du bilan lésionnel pour diminuer la mortalité.", "2+"),
        ("R3.2", "Chez le patient avec risque de lésion médullaire, les experts proposent de "
         "maintenir le niveau de pression artérielle moyenne &gt; 70 mmHg pendant la première "
         "semaine pour limiter le risque d'aggravation du déficit neurologique.", "AE"),
    ], [15*mm, PAGE_W-2*MARGIN-15*mm-20*mm, 20*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(P("Mortalité des traumatisés sévères : +4,8 % à chaque baisse de 10 mmHg de PAS "
                    "à l'admission, dès 110 mmHg (National Trauma Databank, 870 634 patients). "
                    "PAM cible &gt;70 mmHg : corrélation avec amélioration neurologique retrouvée "
                    "pendant les 2-3 premiers jours (analyse de 74 patients avec monitorage "
                    "continu) ; une pression de perfusion médullaire &gt;50 mmHg était corrélée à "
                    "un meilleur état neurologique à 6 mois (92 patients). Pas de niveau de "
                    "preuve suffisant pour recommander un objectif supra-physiologique "
                    "(PAM&gt;85 mmHg, proposé par l'AANS/CNS américaine sur 2 études sans groupe "
                    "contrôle).", S_NOTE))
    story.append(Spacer(1, 4*mm))

    story.append(section_bar("Q4 — Filière de soins"))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("R4.1", "Il faut probablement transférer directement en filière de soins spécialisée "
         "le patient avec traumatisme rachidien et déficit neurologique, y compris transitoire, "
         "pour diminuer la morbi-mortalité.", "2+"),
    ], [15*mm, PAGE_W-2*MARGIN-15*mm-20*mm, 20*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(P("Prise en charge directe en centre de traumatologie de niveau 1 : chirurgie "
                    "plus précoce, durée de séjour en réanimation réduite, amélioration du "
                    "pronostic neurologique. Filière « trauma center-SSR spécialisé » : réduit la "
                    "durée de séjour en soins aigus et diminue l'incidence des escarres et des "
                    "thromboses veineuses (niveau de preuve faible, études observationnelles).", S_NOTE))
    return story

def _section_q5_6():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Q5 — Corticothérapie à la phase initiale"))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("R5.1", "Chez le patient atteint d'une lésion médullaire traumatique, complète ou "
         "incomplète, il ne faut pas administrer de corticoïdes à la phase précoce dans "
         "l'objectif d'améliorer le pronostic neurologique.", "1-"),
    ], [15*mm, PAGE_W-2*MARGIN-15*mm-20*mm, 20*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(P("3 essais randomisés (NACSIS 1, 2, 3) sur la méthylprednisolone : NACSIS 2 a "
                    "montré une amélioration modeste des scores moteurs à 6 mois dans un "
                    "sous-groupe traité &lt;8h, sans mesure standardisée du handicap à long "
                    "terme, et davantage d'infections dans le groupe corticoïde forte dose "
                    "(7 % vs 3 % placebo, non significatif) — seul essai avec un vrai bras "
                    "placebo. NACSIS 1 (comparant 2 doses de corticoïde, sans placebo) a montré "
                    "plus de complications infectieuses dans le groupe à faible dose ; NACSIS 3 "
                    "(24h vs 48h de corticoïde, sans placebo) a montré plus de complications "
                    "septiques dans le groupe 48h, sans meilleure récupération motrice. Une "
                    "analyse par score de propension d'une large cohorte canadienne récente n'a "
                    "retrouvé aucun bénéfice sur la récupération motrice, avec plus de "
                    "complications infectieuses (urinaires, pulmonaires) dans le groupe traité.", S_NOTE))
    story.append(Spacer(1, 4*mm))

    story.append(section_bar("Q6 — Indications de l'IRM dans le bilan lésionnel"))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("R6.1", "Les experts suggèrent de réaliser une IRM médullaire dans les plus brefs "
         "délais devant toute anomalie de l'examen neurologique post-traumatique non expliquée "
         "par un scanner du rachis, pour indiquer la prise en charge chirurgicale.", "AE"),
        ("R6.2", "Si une IRM est réalisable sans retarder le traitement chirurgical et sans "
         "mettre le patient en danger, il faut probablement réaliser une IRM médullaire "
         "pré-opératoire afin d'améliorer la prise en charge chirurgicale.", "2+"),
    ], [15*mm, PAGE_W-2*MARGIN-15*mm-20*mm, 20*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(P("L'étude STASCIS a établi qu'une décompression médullaire précoce (&lt;24h) "
                    "guidée par IRM améliore significativement le pronostic neurologique "
                    "(OR=2,83, IC95 [1,10-7,28]). L'IRM détecte avec une sensibilité bonne à "
                    "excellente la compression médullaire, la contusion, la lésion ligamentaire, "
                    "la hernie discale et l'hématome épidural — 9,1 % des lésions cervicales ont "
                    "un hématome épidural post-traumatique (série de 1916 patients), dont "
                    "&gt;13 % avec un scanner interprété comme normal (diagnostiqués sur IRM "
                    "seule). Risque à mettre en balance : maintien en décubitus ~30 min (HTIC si "
                    "traumatisme crânien associé, instabilité hémodynamique).", S_NOTE))
    return story

def _section_q7_8():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Q7 — Délai optimal de prise en charge chirurgicale"))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("R7.1", "Chez les patients avec lésion médullaire traumatique, il faut probablement "
         "réaliser une décompression chirurgicale en urgence, au plus tard dans les 24 heures du "
         "déficit neurologique, pour augmenter la récupération neurologique à long terme.", "2+"),
    ], [15*mm, PAGE_W-2*MARGIN-15*mm-20*mm, 20*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(P("Chirurgie &lt;24h : amélioration de la récupération neurologique constatée "
                    "dans plusieurs études prospectives (RR=8,9 IC95 [1,12-70,64] pour atteintes "
                    "cervicales/thoraciques complètes ou incomplètes, n=84) — aucune étude ne "
                    "retrouve une meilleure récupération chez les patients opérés tardivement "
                    "(≥24h). Fréquence des complications pulmonaires toujours diminuée ou similaire "
                    "dans les groupes chirurgie précoce. Chirurgie ultra-précoce (&lt;8h) : "
                    "pourrait diminuer les complications respiratoires et augmenter les chances de "
                    "récupération neurologique (données rétrospectives limitées) — les trauma "
                    "centers de niveau I français peuvent opérer en sécurité &lt;8h, renforçant "
                    "l'utilité du transfert précoce.", S_NOTE))
    story.append(Spacer(1, 4*mm))

    story.append(section_bar("Q8 — Intubation trachéale en milieu hospitalier"))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("R8.1", "En urgence, il faut probablement réaliser une induction séquence rapide et, "
         "pour diminuer le risque d'échec d'intubation au premier essai, s'aider d'une "
         "vidéolaryngoscopie en première intention pour faciliter l'intubation.", "2+"),
        ("R8.2", "En dehors de l'urgence et chez un patient coopérant, il faut probablement "
         "réaliser une intubation fibroscopique en ventilation spontanée chez les patients à "
         "risque d'échec de ventilation au masque et/ou de laryngoscopie indirecte (ouverture de "
         "bouche &lt; 2,5 cm) pour diminuer le risque d'échec d'intubation au premier essai.", "2+"),
    ], [15*mm, PAGE_W-2*MARGIN-15*mm-20*mm, 20*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(P("Méta-analyse (24 études, 1866 patients) : la vidéolaryngoscopie réduit le "
                    "risque d'échec d'intubation au 1er essai vs laryngoscope de Macintosh "
                    "(RR=0,53 IC95 [0,35-0,80]) — seul l'Airtraq démontre une réduction "
                    "significative parmi les dispositifs testés (3,4 % vs 28,6 % d'échec ; "
                    "RR=0,14). Intubation fibroscopique en ventilation spontanée = technique "
                    "limitant le plus la mobilisation du rachis cervical, mais nécessite la "
                    "coopération du patient (peu adaptée à l'urgence). Succinylcholine utilisable "
                    "comme curare d'action rapide dans les premières 48h post-traumatiques — "
                    "au-delà de ce délai, la limite d'utilisation classique tient au risque "
                    "propre à toute désafférentation nerveuse (cf. littérature citée).", S_NOTE))
    story.append(Spacer(1, 3*mm))
    cw = PAGE_W - 2*MARGIN
    story.append(simple_table(
        ["Contexte", "Technique"],
        [
            ["Milieu extra-hospitalier", "Induction séquence rapide + laryngoscopie directe + "
             "mandrin long (type Eschmann) + stabilisation du rachis en ligne."],
            ["Milieu hospitalier — urgence vitale, ou estomac plein, ou (ouverture de bouche "
             "normale ET ventilation au masque non prévue difficile)", "Induction séquence "
             "rapide (si estomac plein ou urgence vitale) + vidéolaryngoscopie + stabilisation "
             "du rachis en ligne."],
            ["Milieu hospitalier — hors urgence vitale, estomac non plein, ET (ouverture de "
             "bouche limitée ou ventilation au masque prévue difficile)", "Intubation "
             "fibroscopique en ventilation spontanée + stabilisation du rachis en ligne."],
        ],
        [cw*0.55, cw*0.45]))
    story.append(Spacer(1, 1.5*mm))
    story.append(P("Figure 2 (source) — Algorithme : procédure de l'intubation trachéale chez les "
                    "patients avec ou à risque de lésion médullaire cervicale (Avis d'Experts) — "
                    "transcrit en tableau de décision, vérifié visuellement (page 21).", S_NOTE))
    return story

def _section_q9_10():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Q9 — Sevrage de la ventilation mécanique"))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("R9.1", "Il faut probablement associer un ensemble standardisé de méthodes pour "
         "faciliter le sevrage ventilatoire, incluant par exemple : ceinture abdominale chez le "
         "patient assis en ventilation spontanée ; kinésithérapie de drainage bronchique et de "
         "renforcement diaphragmatique ; toux assistée avec insufflateur/exsufflateur ; "
         "aérosolthérapie (bêta-2 mimétiques ± atropiniques) ; autonomisation respiratoire "
         "progressive.", "2+"),
        ("R9.2", "Les experts suggèrent la réalisation d'une trachéotomie pour accélérer le "
         "sevrage ventilatoire dans les 7 premiers jours en cas d'atteinte du rachis cervical "
         "haut (C2-C5), et uniquement après échec d'une ou plusieurs tentatives d'extubation "
         "réalisées dans des conditions optimales en cas d'atteinte du rachis cervical bas "
         "(C6-C7), y compris en cas d'atteinte complète.", "AE"),
    ], [15*mm, PAGE_W-2*MARGIN-15*mm-20*mm, 20*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(P("Principaux facteurs de risque d'échec du sevrage/recours à la trachéotomie : "
                    "lésion au-dessus de C5 (réduction de capacité vitale ≥50 %) et caractère "
                    "complet de l'atteinte. Trachéotomie précoce (&lt;7j) si lésion haute (&gt;C5) "
                    "+ kinésithérapie de drainage + toux assistée + aérosolthérapie : associée à "
                    "une meilleure récupération neurologique à 1 an (étude avant/après). Position "
                    "allongée souvent mieux tolérée que la position assise chez le tétraplégique "
                    "(effets de la pesanteur sur la capacité inspiratoire).", S_NOTE))
    story.append(Spacer(1, 4*mm))

    story.append(section_bar("Q10 — Traitement antalgique spécifique"))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("R10.1", "Il faut probablement introduire une analgésie multimodale associant "
         "analgésique non morphinique et anti-hyperalgésique (kétamine) aux opioïdes lors de la "
         "prise en charge chirurgicale pour prévenir la survenue de douleurs prolongées chez les "
         "blessés vertébro-médullaires.", "2+"),
        ("R10.2", "Pour contrôler les douleurs neuropathiques des blessés vertébro-médullaires, "
         "il faut introduire un traitement par voie orale par gabapentinoïdes pour une durée "
         "prolongée (&gt;6 mois), et y associer un antidépresseur tricyclique ou un inhibiteur "
         "mixte de la recapture de la sérotonine et de la noradrénaline si l'efficacité d'une "
         "monothérapie est insuffisante.", "1+"),
    ], [16*mm, PAGE_W-2*MARGIN-16*mm-20*mm, 20*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(P("Prévalence des douleurs chroniques chez le blessé médullaire : 65-85 %, dont "
                    "40 % neuropathiques. Méta-analyse : efficacité analgésique importante des "
                    "gabapentinoïdes (8 études, 524 patients, SMD 2,8 [2,4-3,2]) et modérée des "
                    "antidépresseurs (4 études, 188 patients, SMD 0,34 [0,05-0,62]). Questionnaires "
                    "DN4 et NPSI utilisables pour le diagnostic/l'évaluation de l'intensité — aucun "
                    "examen complémentaire nécessaire. Lidocaïne : non recommandée dans les "
                    "douleurs neuropathiques centrales (résultats contradictoires, 3 essais "
                    "randomisés).", S_NOTE))
    return story

def _section_q11_12():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Q11 — Installation et mobilisation spécifiques"))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("R11.1", "Afin de diminuer les complications neuro-orthopédiques et la spasticité des "
         "membres, les experts suggèrent de mettre en place au moins une fois par jour, dès la "
         "phase aiguë : rééducation et mobilisation passive des articulations intéressées par le "
         "déficit moteur ; installation des articulations dans le sens inverse de la déformation "
         "prévisible ; mise en place d'orthèses ; renforcement musculaire manuel.", "AE"),
        ("R11.2", "Dès la phase aiguë, il faut probablement mettre en place au moins une fois "
         "par jour, pour prévenir la survenue d'escarres : mobilisation précoce dès que le "
         "rachis est fixé ; vérifications visuelles et tactiles quotidiennes des zones à risque ; "
         "repositionnement toutes les 2 à 4 heures avec contrôle des zones d'appui ; outils de "
         "décharge (coussins, mousses, oreillers) ; support de prévention de haut niveau (matelas "
         "perte d'air, matelas dynamique).", "2+"),
    ], [16*mm, PAGE_W-2*MARGIN-16*mm-20*mm, 20*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(P("Étirements ≥20 minutes par zone, prolongés par orthèses de posture simple "
                    "(extension de coude, enroulement en flexion des métacarpo-phalangiennes, "
                    "ouverture de la commissure pouce-index). Prévalence des escarres jusqu'à "
                    "26 % (localisations principales : sacrum 39 %, talons 13 %, ischion 8 %, "
                    "occiput 6 %). Recommandation de moyens : réanimations accueillant des blessés "
                    "médullaires traumatiques devraient assurer 2,5 ETP de kinésithérapeute pour "
                    "15 lits (référence ARS Île-de-France pour les SSR neurologiques).", S_NOTE))
    story.append(Spacer(1, 4*mm))

    story.append(section_bar("Q12 — Sondage vésical intermittent précoce"))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("R12.1", "Il faut probablement mettre en place une stratégie permettant un sondage "
         "urinaire intermittent dès que le volume de diurèse quotidien le permet, afin de "
         "diminuer les complications urologiques (infection urinaire, lithiase urinaire) chez "
         "les patients avec lésion médullaire.", "2+"),
    ], [15*mm, PAGE_W-2*MARGIN-15*mm-20*mm, 20*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(P("Sondage intermittent = méthode de référence de drainage urinaire (diminution "
                    "du risque rénal et infectieux à long terme, favorise l'acquisition d'une "
                    "continence). La sonde à demeure doit être ôtée dès que le patient est "
                    "médicalement stable pour minimiser les risques urologiques à long terme. "
                    "Constipation = complication habituelle, prise en charge à débuter dès "
                    "l'admission et à poursuivre tout au long de la vie.", S_NOTE))
    return story

def _section_synthese():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Synthèse et messages clés"))
    story.append(Spacer(1, 2*mm))
    story.append(P(
        "• Immobilisation rachidienne précoce probablement recommandée pour tout patient "
        "suspect de lésion rachidienne ; extraction sur plan dur seulement si urgence vitale ou "
        "critères cliniques présents, sinon pas d'immobilisation systématique (transport matelas "
        "coquille).<br/>"
        "• Intubation : stabilisation manuelle en ligne + retrait de la partie antérieure du "
        "collier pendant le geste ; ISR + laryngoscopie directe + mandrin d'Eschmann en "
        "préhospitalier ; à l'hôpital, vidéolaryngoscopie en 1ère intention si urgence, "
        "fibroscopie en ventilation spontanée si patient coopérant et voies aériennes à "
        "risque.<br/>"
        "• Hémodynamique : PAS &gt; 110 mmHg avant le bilan lésionnel ; PAM &gt; 70 mmHg pendant "
        "la 1ère semaine (pas de niveau de preuve pour des objectifs supra-physiologiques "
        "&gt;85 mmHg). Transfert direct en filière spécialisée si déficit neurologique, y "
        "compris transitoire.<br/>"
        "• Pas de corticothérapie à la phase précoce (bénéfice non démontré, risque infectieux "
        "accru). IRM médullaire en urgence si déficit inexpliqué par le scanner, ou en "
        "pré-opératoire si réalisable sans retard ni danger. Décompression chirurgicale "
        "&lt;24h (recommandation formelle) — une chirurgie &lt;8h est évoquée par de nombreux "
        "spécialistes comme potentiellement bénéfique, mais reste un avis, non une "
        "recommandation graduée, faute d'études suffisantes.<br/>"
        "• Sevrage ventilatoire : approche multimodale standardisée (kinésithérapie, toux "
        "assistée, aérosolthérapie, ceinture abdominale) ; trachéotomie &lt;7j si atteinte "
        "haute (C2-C5), après échec d'extubation si atteinte basse (C6-C7).<br/>"
        "• Douleur : analgésie multimodale (kétamine + opioïdes) en périopératoire ; "
        "gabapentinoïdes en 1ère intention pour la douleur neuropathique, traitement à "
        "poursuivre &gt;6 mois si efficace, associé à un antidépresseur si insuffisant.<br/>"
        "• Installation/mobilisation quotidienne dès la phase aiguë (prévention neuro-"
        "orthopédique et des escarres) ; sondage urinaire intermittent dès que la diurèse le "
        "permet.",
        S_BODY))
    story.append(Spacer(1, 5*mm))

    story.append(section_bar("Sources et traçabilité", color=GREY))
    story.append(Spacer(1, 2*mm))
    story.append(P(
        "<b>Document source :</b> « Prise en charge des patients présentant, ou à risque, de "
        "traumatisme vertébro-médullaire » — Recommandations Formalisées d'Experts SFAR, avec "
        "ANARLF, SFCR, SFMU, SOFCOT, SOFMER et le SSA. 2019, texte validé par le Comité des "
        "Référentiels Cliniques (15/05/2019) et le CA SFAR (24/05/2019). Actualisation de la "
        "conférence d'experts de 2004. Comité de 27 experts, coordination A. Roquilly, B. Vigué.", S_SOURCE))
    story.append(Spacer(1, 1.5*mm))
    story.append(P("<b>Méthodologie :</b> GRADE®, tags « (GRADE X+/-) accord FORT » ou "
                    "« Avis d'experts » imprimés littéralement après chaque recommandation — "
                    "cités ici tels quels.", S_SOURCE))
    story.append(Spacer(1, 1.5*mm))
    story.append(P("<b>Couverture :</b> 19 recommandations (R1.1-R12.1) reproduites "
                    "intégralement. Les 2 algorithmes de la source (Figure 1 — immobilisation "
                    "rachidienne ; Figure 2 — procédure d'intubation trachéale), tous deux des "
                    "diagrammes de décision avec branches, sont transcrits en tableaux de "
                    "décision condensés, vérifiés par rendu visuel des pages source "
                    "correspondantes.", S_SOURCE))
    story.append(Spacer(1, 3*mm))
    story.append(info_panel(P(
        "<b>Avertissement :</b> ce document est une fiche de synthèse indépendante, produite pour "
        "un usage d'aide-mémoire. Il reprend l'intégralité des recommandations de la RFE mais ne "
        "remplace pas le texte intégral et n'est ni édité ni validé par la SFAR. En cas de doute, "
        "se référer au texte intégral, aux recommandations ultérieures et/ou à un avis "
        "spécialisé.",
        S_BODY_SM), bg=GREY_LIGHT, border=GREY))
    return story

SECTIONS = [
    ("Introduction, méthodologie", _section_intro),
    ("Q1-2 — Immobilisation & intubation préhospitalière", _section_q1_2),
    ("Q3-4 — Hémodynamique & filière de soins", _section_q3_4),
    ("Q5-6 — Corticothérapie & IRM", _section_q5_6),
    ("Q7-8 — Délai chirurgical & intubation hospitalière", _section_q7_8),
    ("Q9-10 — Sevrage ventilatoire & antalgie", _section_q9_10),
    ("Q11-12 — Installation, mobilisation & sondage vésical", _section_q11_12),
    ("Synthèse, sources & traçabilité", _section_synthese),
]

def _make_doc():
    return SimpleDocTemplate(OUT, pagesize=A4,
                              leftMargin=MARGIN, rightMargin=MARGIN,
                              topMargin=32*mm, bottomMargin=16*mm,
                              title="Fiche SFAR 2019 - Traumatisme vertebro-medullaire",
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
