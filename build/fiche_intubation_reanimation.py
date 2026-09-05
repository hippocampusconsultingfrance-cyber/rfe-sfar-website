# -*- coding: utf-8 -*-
"""
Fiche de synthese - RFE commune SFAR-SRLF 2016
Intubation et extubation du patient de reanimation
Source verifiee : Anesth Reanim. 2018;4:523-547 (publication en ligne 13/09/2018), texte valide par
le CA SRLF et le CA SFAR (17/06/2016), egalement publie dans Anaesth Crit Care Pain Med
2017;36(5):327-341. Methodologie GRADE standard (tags "Grade X+/-" imprimes litteralement).
32 recommandations adultes (R1.1-R7.7) : 12 GRADE1 (tous +), 19 GRADE2 (18 positifs "+", 1 negatif
"-" = R7.5), 1 avis d'experts (R4.2) - resume officiel "32 recs adultes, 12 G1, 19 G2, 1 AE,
accord fort pour 31/32 (97%)" independamment reverifie item par item et confirme coherent. La
seule recommandation a accord FAIBLE (et non FORT) est explicitement disclosee dans le texte
source lui-meme (R7.5) - imprimee "(Grade 2-) Accord FAIBLE" alors que toutes les autres portent
"Accord FORT" ; le "-" a ete corrompu en caractere de controle non imprimable (\\x03) par
l'extraction automatique du PDF (meme piege que sur les fiches traumatisme_thoracique et
traumatisme_cranien du meme corpus) - confirme par la formulation negative de la phrase elle-meme
("il ne faut probablement pas...") ET par grep du caractere de controle dans le texte brut, sans
necessiter de rendu image supplementaire compte tenu de la coherence des deux signaux.

Perimetre deliberement limite aux recommandations ADULTES (32) : la source contient egalement
15 recommandations PEDIATRIQUES paralleles (5 GRADE1, 9 GRADE2, 1 avis d'experts, distinctes des
recommandations adultes bien que traitant des memes 7 champs) qui ne sont PAS reproduites ici,
disclosure explicite en introduction plutot qu'omission silencieuse. La gestion des voies
aeriennes en prehospitalier est explicitement exclue du champ par la source elle-meme (deja
couverte par d'autres recommandations existantes).

Deux algorithmes de synthese reproduits : "Algorithme IOT en reanimation" (avis d'experts, ACCORD
FAIBLE - source page 14, diagramme de decision complexe avec score MACOCHA, 2 branches selon score
<3/>=3, transcrit apres rendu visuel a 200dpi) et "Algorithme d'extubation en reanimation" (avis
d'experts, ACCORD FORT - source page 20, sequence largement lineaire avec 2 points de decision
conditionnels, transcrit apres rendu visuel a 200dpi). Tableau I (complications de l'intubation) et
Tableau II (score MACOCHA, 7 items, /12) integralement extractibles en texte, reproduits verbatim.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from style import *
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.units import mm

OUT = "/private/tmp/claude-501/-Users-macbook-Downloads-claude/65498e3e-5ddf-47a6-b100-3ac535d1faa0/scratchpad/rfe_sfar/output/Fiche_SFAR_SRLF_Intubation_Extubation_Reanimation_2016.pdf"

SOURCE_TXT = ("Source : Recommandations Formalisées d'Experts communes SFAR-SRLF, avec SFMU/GFRUP/"
              "ADARPEF/SKR « Intubation et extubation du patient de réanimation » — Anesth Reanim. "
              "2018;4:523-547, texte validé par le CA SRLF et le CA SFAR le 17/06/2016. "
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
    items = [("1+", "Il faut faire"), ("2+", "Il faut probablement"),
             ("2-", "Il ne faut probablement pas"), ("AE", "Avis d'experts")]
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
    header_band(canvas, doc, "SFAR / SRLF — RFE 2016 — FICHE DE SYNTHÈSE",
                "Intubation & extubation en réanimation",
                page_title, icon_fn=lambda c,x,y: icon_shield(c, x, y, 13*mm), color=NAVY)
    footer_band(canvas, doc, SOURCE_TXT, f"Page {doc.page} / {TOTAL_PAGES['n']}")

# ---------------------------------------------------------------------------
def _section_intro():
    story = []
    story.append(Spacer(1, 3*mm))
    story.append(info_panel(P(
        "<b>Champ :</b> intubation et extubation du patient adulte de réanimation (hors "
        "prise en charge pré-hospitalière, explicitement exclue par la source). Comité SFAR/"
        "SRLF, avec SFMU, GFRUP, ADARPEF, SKR ; méthode GRADE®, format PICO. Intubation "
        "explorée en 4 champs (intubation compliquée, matériel, agents d'induction, "
        "protocoles/bundles) ; extubation en 3 champs (pré-requis, échecs, gestion "
        "pratique).<br/><br/>"
        "<b>Résultats (résumé officiel, recommandations adultes) :</b> 32 recommandations ; "
        "12 de niveau de preuve élevé (Grade 1+/-), 19 de niveau de preuve faible (Grade 2+/-), "
        "1 avis d'experts. Accord fort obtenu pour 31/32 (97 %) des recommandations — la seule "
        "exception (R7.5) porte un accord qualifié « FAIBLE » dans le texte source lui-même, "
        "disclosure conservée telle quelle. 2 algorithmes de synthèse également "
        "formalisés.<br/><br/>"
        "<i>15 recommandations pédiatriques parallèles existent également dans ce document "
        "(5 Grade1, 9 Grade2, 1 avis d'experts) mais ne sont pas reproduites dans cette fiche, "
        "centrée sur l'adulte — se référer au texte intégral pour le volet pédiatrique.</i>",
        S_BODY), bg=BG_PANEL, border=TEAL))
    story.append(Spacer(1, 3*mm))

    story.append(section_bar("Légende des grades (méthodologie GRADE)"))
    story.append(Spacer(1, 2*mm))
    story.append(legend_flowable())
    return story

def _section_champ1():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Champ 1 — Intubation compliquée en réanimation"))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("R1.1", "Il faut considérer tous les patients de réanimation à risque d'intubation "
         "compliquée.", "1+"),
        ("R1.2", "Afin d'en réduire l'incidence, il faut que les complications respiratoires et "
         "hémodynamiques de l'intubation soient anticipées et prévenues grâce à une préparation "
         "soigneuse de la procédure, intégrant le maintien de l'oxygénation et de "
         "l'hémodynamique systémiques tout au long de la procédure.", "1+"),
        ("R1.3", "Il faut différencier les facteurs prédictifs d'intubation compliquée des "
         "facteurs prédictifs d'intubation difficile.", "1+"),
    ], [15*mm, PAGE_W-2*MARGIN-15*mm-20*mm, 20*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(P("Intubation en réanimation = procédure à haut risque (20-50 % de "
                    "complications pouvant menacer le pronostic vital), le plus souvent en "
                    "urgence chez un patient hypoxémique et hémodynamiquement précaire. "
                    "Intubation difficile (≥2 tentatives) : incidence 8-23 % en réanimation. "
                    "Score MACOCHA (voir tableau ci-dessous) : seuil ≥3 = VPN 97-98 %, "
                    "sensibilité 73-76 % pour prédire l'intubation difficile.", S_NOTE))
    story.append(Spacer(1, 3*mm))
    cw = PAGE_W - 2*MARGIN
    story.append(simple_table(
        ["Tableau I — Complications de l'intubation", ""],
        [
            ["Sévères", "Hypoxémie sévère • Collapsus cardiovasculaire sévère • Arrêt "
             "cardiaque • Décès"],
            ["Modérées", "Intubation difficile • Troubles du rythme • Intubation "
             "œsophagienne • Inhalation • Agitation • Bris dentaires"],
        ],
        [cw*0.22, cw*0.78]))
    story.append(Spacer(1, 3*mm))
    story.append(simple_table(
        ["Tableau II — Score MACOCHA", "Points"],
        [
            ["M — Mallampati score III ou IV", "5"],
            ["A — Apnées du sommeil", "2"],
            ["C — Cervicale (mobilité rachidienne réduite)", "1"],
            ["O — Ouverture de bouche < 3 cm", "1"],
            ["C — Coma", "1"],
            ["H — Hypoxémie", "1"],
            ["A — non-Anesthésiste ou Anesthésiste non entraîné", "1"],
        ],
        [cw*0.80, cw*0.20]))
    story.append(Spacer(1, 1.5*mm))
    story.append(P("Codé de 0 à 12. Un seuil ≥ 3 permet de retenir une intubation difficile "
                    "avec une bonne sensibilité (73-76 %) ; un score &lt; 3 permet de l'écarter "
                    "avec une excellente valeur prédictive négative (97-98 %).", S_NOTE))
    return story

def _section_champ2():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Champ 2 — Matériel de l'intubation"))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("R2.1", "Il faut mettre en œuvre un contrôle capnographique de l'intubation en "
         "réanimation pour confirmer la bonne position de la sonde d'intubation, du dispositif "
         "supra-glottique ou de l'abord trachéal direct.", "1+"),
        ("R2.2", "Il faut disposer d'un chariot d'intubation difficile et d'un bronchoscope "
         "(usuel ou à usage unique) en réanimation afin de pouvoir faire face immédiatement aux "
         "situations d'intubation difficile.", "1+"),
        ("R2.3", "Il faut employer des lames métalliques pour les laryngoscopies directes en "
         "réanimation afin d'en améliorer les chances de succès.", "1+"),
        ("R2.4", "Pour limiter les échecs d'intubation, il faut probablement utiliser les "
         "vidéolaryngoscopes (VL) pour l'intubation en réanimation, soit d'emblée soit après "
         "échec de la laryngoscopie directe.", "2+"),
        ("R2.5", "Il faut utiliser les dispositifs supra-glottiques (DSG) dans la gestion des "
         "intubations difficiles en réanimation, pour oxygéner le patient puis favoriser "
         "l'intubation sous contrôle bronchoscopique.", "1+"),
        ("R2.6", "Les connaissances théoriques et pratiques en matière d'intubation doivent "
         "être acquises et régulièrement entretenues.", "1+"),
    ], [15*mm, PAGE_W-2*MARGIN-15*mm-20*mm, 20*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(P("Intubation œsophagienne : incidence jusqu'à 51 % en cas d'intubation "
                    "difficile ; étude NAP4 — non-utilisation ou mauvaise interprétation de la "
                    "capnographie impliquée dans 74 % des décès/dommages cérébraux "
                    "irréversibles liés à l'intubation en réanimation/urgences. Méta-analyse "
                    "(9 études, 2133 patients) : les VL augmentent le succès dès la 1ère "
                    "tentative (OR=2,07 IC95 [1,35-3,16]), diminuent les intubations difficiles "
                    "(OR=0,29), les Cormack-Lehane 3-4 (OR=0,26) et les intubations "
                    "œsophagiennes (OR=0,14). Nombre de procédures recommandé en formation : "
                    "50-70 laryngoscopies directes, 20 poses de DSG, 30-60 intubations "
                    "fibroscopiques, 5 cricothyroïdotomies, 20 utilisations de VL.", S_NOTE))
    return story

def _section_champ3():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Champ 3 — Agents d'induction"))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("R3.1", "Il faut probablement choisir un hypnotique (étomidate, kétamine, propofol) "
         "permettant l'induction en séquence rapide (ISR) en fonction du terrain et de la "
         "situation clinique du patient.", "2+"),
        ("R3.2", "Chez le patient de réanimation, il faut probablement utiliser la "
         "succinylcholine comme curare de première intention lors de l'ISR afin de réduire la "
         "durée de la procédure et le risque d'inhalation.", "2+"),
        ("R3.3", "Il faut utiliser le rocuronium à une dose supérieure à 0,9 mg/kg "
         "[1,0-1,2 mg/kg] en cas de contre-indication à la succinylcholine et permettre un accès "
         "rapide au sugammadex en cas d'utilisation de celui-ci.", "1+"),
    ], [15*mm, PAGE_W-2*MARGIN-15*mm-20*mm, 20*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(P("Étomidate : augmentation de l'insuffisance surrénale relative même en "
                    "injection unique — prudence chez le patient septique. Kétamine : "
                    "propriétés stimulantes sympathiques, alternative valable à l'étomidate. "
                    "Propofol : risque d'instabilité hémodynamique, prévenu par le recours "
                    "précoce/préventif aux amines vasopressives. Revue Cochrane (50 essais) : "
                    "succinylcholine supérieure au rocuronium pour des conditions d'intubation "
                    "excellentes (OR=0,86 IC95 [0,81-0,92]) — différence non significative si "
                    "rocuronium &gt;0,9 mg/kg. Sugammadex 16 mg/kg : décurarisation plus rapide "
                    "que la décurarisation spontanée de la succinylcholine.", S_NOTE))
    return story

def _section_champ4():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Champ 4 — Protocoles et bundles de l'intubation"))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("R4.1", "Il faut probablement utiliser la VNI pour la préoxygénation des patients "
         "hypoxémiques en réanimation.", "2+"),
        ("R4.2", "Il est possible d'utiliser l'oxygénothérapie nasale haut débit (ONHD) pour la "
         "préoxygénation en réanimation, notamment pour les patients non sévèrement "
         "hypoxémiques.", "AE"),
        ("R4.3", "Il faut probablement utiliser un protocole d'intubation incluant un versant "
         "ventilatoire au cours de l'intubation en réanimation pour diminuer les complications "
         "respiratoires.", "2+"),
        ("R4.4", "Il faut probablement utiliser une manœuvre de recrutement post-intubation "
         "chez les patients de réanimation hypoxémiques en l'intégrant dans un protocole "
         "ventilatoire.", "2+"),
        ("R4.5", "Il faut probablement appliquer une PEEP d'au moins 5 cm H2O après intubation "
         "des patients hypoxémiques.", "2+"),
        ("R4.6", "Il faut probablement utiliser un protocole hémodynamique, définissant les "
         "modalités du remplissage vasculaire et de la mise en place précoce de catécholamines "
         "pour diminuer les complications hémodynamiques lors de l'intubation des patients en "
         "réanimation.", "2+"),
    ], [15*mm, PAGE_W-2*MARGIN-15*mm-20*mm, 20*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(P("Étude multicentrique avant/après : un protocole d'intubation incluant un "
                    "volet ventilatoire réduit significativement les complications sévères. "
                    "Étude « Preoxyflow » (randomisée) : l'ONHD n'est pas supérieure à "
                    "l'oxygénothérapie conventionnelle chez le patient sévèrement hypoxémique — "
                    "d'où sa place réservée aux patients non sévèrement hypoxémiques. "
                    "Manœuvre de recrutement post-intubation (CPAP 40 cmH2O &gt;30 sec, étude "
                    "bicentrique, 40 patients) : gain d'oxygénation significatif à 2 et 30 min "
                    "(236±117 vs 93±36 mmHg puis 180±79 vs 110±39 mmHg), sans conséquence "
                    "hémodynamique ni barotraumatisme. Bundle hémodynamique (244 patients, "
                    "3 centres) : réduction du collapsus post-intubation de 27 % à 15 %.", S_NOTE))
    story.append(Spacer(1, 3*mm))
    cw = PAGE_W - 2*MARGIN
    story.append(P("<b>Algorithme IOT en réanimation</b> (source — avis d'experts, ACCORD "
                    "FAIBLE) — transcrit en tableau de décision, vérifié par rendu visuel "
                    "(page 14) :", S_BODY_SM))
    story.append(Spacer(1, 1.5*mm))
    story.append(simple_table(
        ["Étape", "Contenu"],
        [
            ["Avant l'intubation", "Installation du patient, expansion volémique prudente "
             "(en l'absence de surcharge hydrosodée). Vérifier matériel (chariot d'intubation "
             "difficile, bronchoscope, matériel d'abord cervical direct) et personnel (2 "
             "médecins + 1 IDE en configuration optimale) : sédation, vasopresseurs, "
             "capnographie prêts. Évaluer le risque d'IOT difficile par le score MACOCHA "
             "(cf. Tableau II)."],
            ["Pendant l'intubation — préoxygénation", "Patient hypoxémique → VNI. Patient non "
             "hypoxémique → BAVU ou ONHD."],
            ["Pendant l'intubation — induction", "Induction en séquence rapide : "
             "kétamine/étomidate/propofol ; succinylcholine 1 mg/kg ou rocuronium 1,2 mg/kg "
             "(accès immédiat au sugammadex requis) ; manœuvre de Sellick."],
            ["Score MACOCHA &lt; 3", "1ère intention : laryngoscopie directe (Mc Intosh), sonde "
             "sur mandrin malléable, lame métallique, 2 tentatives max en 2 min. Échec → "
             "reprise au masque + appel expertise anesthésique → vidéolaryngoscope (retrait du "
             "Sellick, BURP, 2 tentatives max) → si échec → dispositif supra-glottique (DSG : "
             "retrait Sellick, BURP, 2 tentatives max) → ventilation efficace (contrôle "
             "capnographique, intubation à travers le DSG)."],
            ["Score MACOCHA ≥ 3", "1ère intention : vidéolaryngoscopie OU laryngoscopie directe "
             "(Mc Intosh, lame métallique, sonde sur mandrin malléable ou mandrin d'Eschmann), "
             "2 tentatives max en 2 min. Échec → reprise au masque + appel expertise "
             "anesthésique → dispositif supra-glottique (DSG). Nouvel échec → reprise au masque "
             "→ abord cervical direct (cricothyroïdotomie chirurgicale ou percutanée)."],
            ["Après l'intubation", "PEEP 5 cmH2O, ventilation protectrice, manœuvre de "
             "recrutement (FiO2 100 %, Paw 40 cmH2O, 30 sec — chez le patient hémodynamiquement "
             "stable, à interrompre immédiatement si elle induit une instabilité), mesure de la "
             "pression du ballonnet trachéal, recours aux vasopresseurs si PAD &lt; 35 mmHg."],
        ],
        [cw*0.28, cw*0.72]))
    return story

def _section_champ5_6():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Champ 5 — Pré-requis à l'extubation"))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("R5.1", "Il faut réaliser une épreuve de sevrage en VS avant toute extubation chez le "
         "patient de réanimation ventilé depuis plus de 48 h afin de réduire le risque d'échec "
         "d'extubation.", "1+"),
        ("R5.2", "L'épreuve de sevrage n'étant pas suffisante pour dépister tous les patients à "
         "risque d'échec d'extubation, il faut probablement rechercher les causes et facteurs "
         "de risque plus spécifiques d'échec incluant l'inefficacité de la toux, l'abondance des "
         "sécrétions bronchiques, l'inefficacité de la déglutition, et les troubles de la "
         "conscience.", "2+"),
    ], [15*mm, PAGE_W-2*MARGIN-15*mm-20*mm, 20*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(P("Succès de l'épreuve en VS (FR 10-30/min, SpO2&gt;92 %, absence de "
                    "sueur/agitation/hypertension/tachycardie) : meilleur test diagnostique "
                    "disponible pour prédire le succès de l'extubation, malgré ses limites "
                    "(30-40 % des patients extubés malgré échec de l'épreuve nécessitent d'être "
                    "réintubés). Échec d'extubation malgré succès de l'épreuve : 10-20 % des cas "
                    "(extrêmes 5-30 % selon populations) — taux acceptable en réanimation "
                    "entre 5 et 10 %.", S_NOTE))
    story.append(Spacer(1, 4*mm))

    story.append(section_bar("Champ 6 — Échecs de l'extubation (œdème laryngé)"))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("R6.1", "Il faut probablement effectuer un test de fuite avant l'extubation pour "
         "prédire la survenue d'un œdème laryngé.", "2+"),
        ("R6.2", "Il faut réaliser le test de fuite chez les patients de réanimation ayant au "
         "moins un facteur de risque de dyspnée laryngée afin de réduire les échecs d'extubation "
         "en rapport avec l'œdème laryngé.", "1+"),
        ("R6.3", "Il faut probablement mettre en œuvre des mesures limitant les lésions "
         "laryngées au cours de la ventilation mécanique.", "2+"),
        ("R6.4", "Si le volume de fuite est faible ou nul, il faut probablement prescrire une "
         "corticothérapie pour prévenir les échecs d'extubation en rapport avec l'œdème "
         "laryngé.", "2+"),
        ("R6.5", "Lorsqu'elle est décidée, la corticothérapie doit être débutée au moins 6 "
         "heures avant l'extubation pour être efficace.", "1+"),
    ], [15*mm, PAGE_W-2*MARGIN-15*mm-20*mm, 20*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(P("Lésions laryngées présentes chez &gt;75 % des patients ventilés (œdème, "
                    "ulcération muqueuse, parésie des cordes vocales, granulomes). Facteurs de "
                    "risque de dyspnée laryngée : sexe féminin, intubation nasale, sonde de gros "
                    "calibre, pressions de ballonnet élevées, intubation difficile/traumatique/"
                    "prolongée. Seuils du test de fuite : &lt;110 mL en volume absolu ou "
                    "&lt;10 % en volume relatif — bonne spécificité/VPN mais faible "
                    "sensibilité/VPP. Corticothérapie (~1 mg/kg/j équivalent prednisolone), "
                    "débutée ≥6h avant l'extubation, éventuellement en doses fractionnées, "
                    "réservée aux patients à test de fuite positif.", S_NOTE))
    return story

def _section_champ7():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Champ 7 — Gestion pratique de l'extubation"))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("R7.1", "En préventif, il faut probablement utiliser l'oxygénothérapie nasale à haut "
         "débit en postopératoire de chirurgie cardiothoracique.", "2+"),
        ("R7.2", "En préventif, il faut probablement utiliser l'oxygénothérapie nasale à haut "
         "débit après extubation programmée en réanimation chez les patients hypoxémiques ou à "
         "risque faible de réintubation.", "2+"),
        ("R7.3", "En préventif, il faut probablement utiliser la VNI prophylactique après "
         "extubation programmée en réanimation chez les patients à haut risque de réintubation, "
         "notamment chez les patients hypercapniques.", "2+"),
        ("R7.4", "En curatif, il faut probablement utiliser la VNI curative en cas "
         "d'insuffisance respiratoire aiguë postopératoire, notamment après chirurgie "
         "abdominale ou résection pulmonaire.", "2+"),
        ("R7.5", "En curatif, il ne faut probablement pas utiliser la VNI curative en cas "
         "d'insuffisance respiratoire aiguë survenant après extubation programmée en "
         "réanimation, excepté chez les patients BPCO ou en cas d'OAP évident.", "2-"),
        ("R7.6", "Il faut probablement faire intervenir un kinésithérapeute avant et après "
         "l'extubation chez les patients ventilés plus de 48 h afin de diminuer la durée de "
         "sevrage et limiter le risque de réintubation.", "2+"),
        ("R7.7", "Il faut probablement faire intervenir un kinésithérapeute au cours du geste "
         "de l'extubation, afin de limiter les complications immédiates liées au "
         "sur-encombrement chez les patients à risque.", "2+"),
    ], [15*mm, PAGE_W-2*MARGIN-15*mm-20*mm, 20*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(info_panel(P(
        "<b>R7.5 est la seule recommandation de cette RFE à accord qualifié « FAIBLE »</b> "
        "(et non « FORT ») dans le texte source lui-même — disclosure conservée telle quelle, "
        "cohérente avec le résumé officiel (« accord fort pour 31/32, 97 % » des "
        "recommandations adultes).",
        S_BODY_SM), bg=AMBER_LIGHT, border=AMBER))
    story.append(Spacer(1, 2*mm))
    story.append(P("Taux global de réintubation en réanimation ~15 %, jusqu'à 20-30 % chez les "
                    "patients à risque ; mortalité en cas d'échec : 25-50 %. VNI prophylactique "
                    "(6 études randomisées) : bénéfice non significatif toutes populations "
                    "confondues (OR=0,80 IC95 [0,64-1,01]) mais significatif chez les patients à "
                    "haut risque de réintubation (OR=0,63 IC95 [0,45-0,87]). VNI curative "
                    "après extubation programmée : non recommandée hors BPCO/OAP (masque les "
                    "signes d'IRA et retarde la réintubation). Kinésithérapie de "
                    "désencombrement : limiterait significativement les réintubations, sans "
                    "bénéfice démontré sur la durée de sevrage/VM.", S_NOTE))
    story.append(Spacer(1, 3*mm))
    cw = PAGE_W - 2*MARGIN
    story.append(P("<b>Algorithme d'extubation en réanimation</b> (source — avis d'experts, "
                    "ACCORD FORT) — transcrit en tableau de décision, vérifié par rendu visuel "
                    "(page 20) :", S_BODY_SM))
    story.append(Spacer(1, 1.5*mm))
    story.append(simple_table(
        ["Étape", "Contenu"],
        [
            ["1. Épreuve de sevrage", "Réaliser l'épreuve de sevrage en VS → succès de "
             "l'épreuve requis pour poursuivre."],
            ["2. Facteurs de risque spécifiques", "Rechercher : toux inefficace, encombrement "
             "trachéo-bronchique important, troubles sévères de déglutition, troubles de "
             "vigilance, balance hydrique positive. Si présents → envisager de différer "
             "l'extubation de 12 à 24h."],
            ["3. Test de fuite (si facteur de risque d'œdème laryngé)", "À réaliser uniquement "
             "si ≥1 facteur de risque présent : sexe féminin, intubation nasale, sonde de gros "
             "calibre, pressions de ballonnet élevées, intubation difficile/traumatique/"
             "prolongée. Si &lt;110 mL ou &lt;10-13 % → envisager corticothérapie ≥6h avant "
             "l'extubation."],
            ["4. Préparation du geste", "Expliquer le geste et asseoir le patient ; aspirer la "
             "cavité buccale ; pas d'aspiration intra-trachéale juste avant ni pendant "
             "l'extubation (si nécessaire, reventiler ≥2 min avant) ; pas de « pré-oxygénation » "
             "avant l'extubation."],
            ["5. Extubation et oxygénation", "Envisager l'ONHD chez les patients à risque "
             "faible, et la VNI prophylactique chez les patients à haut risque d'échec "
             "d'extubation (âge avancé, insuffisance respiratoire ou cardiaque chronique, "
             "PaCO2 &gt; 45 mmHg au cours de l'épreuve de VS)."],
        ],
        [cw*0.30, cw*0.70]))
    return story

def _section_synthese():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Synthèse et messages clés"))
    story.append(Spacer(1, 2*mm))
    story.append(P(
        "• Tout patient de réanimation = à risque d'intubation compliquée ; préparation "
        "soigneuse systématique (oxygénation + hémodynamique). Score MACOCHA ≥3 = intubation "
        "probablement difficile (VPN 97-98 % si &lt;3).<br/>"
        "• Matériel : capnographie systématique, chariot d'intubation difficile + bronchoscope "
        "disponibles immédiatement, lames métalliques, VL en 1ère intention ou après échec de "
        "la laryngoscopie directe, DSG pour la gestion des IRD. Formation continue "
        "indispensable (simulation).<br/>"
        "• Induction : hypnotique au choix (étomidate/kétamine/propofol) selon le terrain ; "
        "succinylcholine en 1ère intention (ISR) ; rocuronium &gt;0,9 mg/kg si "
        "contre-indication, avec accès immédiat au sugammadex.<br/>"
        "• Protocole d'intubation intégrant : VNI ou ONHD pour la préoxygénation (selon la "
        "sévérité de l'hypoxémie), volet ventilatoire (manœuvre de recrutement + PEEP ≥5 "
        "cmH2O), volet hémodynamique (remplissage + catécholamines précoces).<br/>"
        "• Extubation : épreuve de sevrage en VS obligatoire si VM &gt;48h, puis recherche des "
        "facteurs de risque spécifiques (toux inefficace, encombrement, troubles de "
        "déglutition/conscience). Test de fuite réservé aux patients à risque d'œdème "
        "laryngé — corticothérapie ≥6h avant si positif.<br/>"
        "• Après extubation : ONHD en préventif (postopératoire cardiothoracique, ou patients "
        "hypoxémiques/à risque faible de réintubation), VNI prophylactique si haut "
        "risque/hypercapnie ; VNI curative utile en postopératoire "
        "(chirurgie abdominale/résection pulmonaire) mais déconseillée en cas d'IRA "
        "post-extubation programmée hors BPCO/OAP. Kinésithérapie avant/pendant/après "
        "l'extubation chez les patients ventilés &gt;48h ou à risque de sur-encombrement.",
        S_BODY))
    story.append(Spacer(1, 5*mm))

    story.append(section_bar("Sources et traçabilité", color=GREY))
    story.append(Spacer(1, 2*mm))
    story.append(P(
        "<b>Document source :</b> « Intubation et extubation du patient de réanimation » — "
        "Recommandations Formalisées d'Experts communes SFAR-SRLF, avec SFMU, GFRUP, ADARPEF, "
        "SKR. Anesth Reanim. 2018;4:523-547, texte validé par le CA SRLF et le CA SFAR le "
        "17/06/2016. Coordination H. Quintard, J. Pottecher (SFAR), L. Donetti, E. l'Her (SRLF).", S_SOURCE))
    story.append(Spacer(1, 1.5*mm))
    story.append(P("<b>Méthodologie :</b> GRADE®, tags « (Grade X+/-) Accord FORT/FAIBLE » ou "
                    "« Avis d'experts » imprimés littéralement après chaque recommandation — "
                    "cités ici tels quels. Piège d'extraction identifié et corrigé avant "
                    "intégration : le signe moins du tag « Grade 2- » de R7.5 a été corrompu en "
                    "caractère de contrôle non imprimable par l'extraction automatique du PDF "
                    "source — confirmé par la formulation négative de la recommandation "
                    "elle-même et par inspection du texte brut.", S_SOURCE))
    story.append(Spacer(1, 1.5*mm))
    story.append(P("<b>Couverture :</b> 32 recommandations adultes (R1.1-R7.7) reproduites "
                    "intégralement, ainsi que les 2 algorithmes de synthèse et les 2 tableaux "
                    "(complications, score MACOCHA). Les 15 recommandations pédiatriques "
                    "parallèles de ce même document ne sont pas reproduites ici — fiche centrée "
                    "sur l'adulte, disclosure explicite en introduction. La gestion "
                    "pré-hospitalière des voies aériennes est explicitement exclue du champ par "
                    "la source elle-même.", S_SOURCE))
    story.append(Spacer(1, 3*mm))
    story.append(info_panel(P(
        "<b>Avertissement :</b> ce document est une fiche de synthèse indépendante, produite pour "
        "un usage d'aide-mémoire. Il reprend l'intégralité des recommandations adultes de la RFE "
        "mais ne remplace pas le texte intégral et n'est ni édité ni validé par la SFAR/SRLF. En "
        "cas de doute, se référer au texte intégral, aux recommandations ultérieures et/ou à un "
        "avis spécialisé.",
        S_BODY_SM), bg=GREY_LIGHT, border=GREY))
    return story

SECTIONS = [
    ("Introduction, méthodologie", _section_intro),
    ("Champ 1 — Intubation compliquée", _section_champ1),
    ("Champ 2 — Matériel de l'intubation", _section_champ2),
    ("Champ 3 — Agents d'induction", _section_champ3),
    ("Champ 4 — Protocoles & bundles + Algorithme IOT", _section_champ4),
    ("Champ 5-6 — Pré-requis & échecs de l'extubation", _section_champ5_6),
    ("Champ 7 — Gestion pratique de l'extubation + Algorithme", _section_champ7),
    ("Synthèse, sources & traçabilité", _section_synthese),
]

def _make_doc():
    return SimpleDocTemplate(OUT, pagesize=A4,
                              leftMargin=MARGIN, rightMargin=MARGIN,
                              topMargin=32*mm, bottomMargin=16*mm,
                              title="Fiche SFAR-SRLF 2016 - Intubation-extubation en reanimation",
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
