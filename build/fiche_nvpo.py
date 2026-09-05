# -*- coding: utf-8 -*-
"""
Fiche de synthese - Conference d'experts - Texte court, SFAR 2007/2008
Prise en charge des nausees et vomissements postoperatoires (NVPO).
P. Diemunsch et al. Publie Ann Fr Anesth Reanim 2008;27:866-878 (disponible en ligne
25/10/2008). Methodologie GRADE, mais convention de cotation specifique a ce document
(rappelee explicitement en preambule de la source) :
  G1+ = il faut faire.      G2+ = il faut probablement faire.
  G1- = il ne faut pas faire. G2- = il ne faut probablement pas faire.
Pas de categorie "avis d'experts" numerique dans ce document : lorsque les donnees sont
insuffisantes, le panel declare explicitement "ne pas etre en mesure de proposer de
recommandation" (4 occurrences : dixyrazine, ephedrine, clonidine, gabapentine - meme
phrase formulaire repetee a l'identique, transcrite ici comme telle).

Document de type "conference d'experts, texte court" : contrairement aux RFE plus
recentes de ce corpus, les recommandations sont integrees dans le texte narratif
(pas de tableau recapitulatif separe) - meme structure que la fiche sedation_reanimation
(conference de consensus 2007/2008) deja construite dans ce corpus. ~60 recommandations
graduees individuelles reparties en 10 "Questions" (chapitres), transcrites ici de facon
exhaustive.

4 tableaux verbatim (Tableau 1 : scores de prediction Apfel/Koivuranta ; Tableau 2 :
pharmacocinetique des AR-5HT3 ; Tableau 3 : facteurs de risque pediatriques ; Tableau 4 :
posologies pediatriques) + 1 figure (Fig. 1, algorithme decisionnel a 3 niveaux de risque,
verifiee par rendu visuel a 200dpi de la page 11 source - pure image, transcrite en
tableau structure).

Bug d'extraction confirme et corrige (meme classe que les cas anterieurs du corpus) : le
Tableau 4 (posologies pediatriques) affiche "Posologie (IV) (mg/kg)" sans le glyphe mu dans
le texte extrait automatiquement ; verification visuelle a 250dpi de la page source confirme
que l'unite imprimee est bien "(microg/kg)" et non "(mg/kg)" - des valeurs en mg/kg (ex.
"50 a 75 mg/kg" de droperidol) seraient cliniquement absurdes (surdosage massif).
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from style import *
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.units import mm

OUT = "/private/tmp/claude-501/-Users-macbook-Downloads-claude/65498e3e-5ddf-47a6-b100-3ac535d1faa0/scratchpad/rfe_sfar/output/Fiche_SFAR_NVPO_2008.pdf"

SOURCE_TXT = ("Source : Conférence d'experts - Texte court « Prise en charge des nausées et "
              "vomissements postopératoires » - P. Diemunsch et al., SFAR. Publié Ann Fr Anesth "
              "Réanim 2008;27:866-878. Méthodologie GRADE (convention G1/G2 spécifique). Fiche "
              "de synthèse non officielle : se référer au texte intégral.")

def P(txt, style=S_CELL):
    return Paragraph(txt, style)

def chip(label, **kw):
    return grade_chip(label, **kw)

def reco_table(rows, col_widths):
    """rows: (theme, text, grade_label)"""
    data = [[P("Thème", S_HEAD_W), P("Recommandation", S_HEAD_W), P("Grade", S_HEAD_W_C)]]
    for theme, txt, grade in rows:
        data.append([P(theme, S_CELL_B), P(txt, S_CELL), chip(grade)])
    t = Table(data, colWidths=col_widths, repeatRows=1)
    style_cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), NAVY), ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTNAME", (0, 0), (-1, 0), FONT_BOLD), ("FONTSIZE", (0, 0), (-1, 0), 8),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("ALIGN", (2, 0), (2, -1), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 0.5, GREY_LIGHT),
        ("TOPPADDING", (0, 0), (-1, -1), 3.2), ("BOTTOMPADDING", (0, 0), (-1, -1), 3.2),
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
        ("TOPPADDING",(0,0),(-1,-1),3), ("BOTTOMPADDING",(0,0),(-1,-1),3), ("LEFTPADDING",(0,0),(-1,-1),5),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            st.append(("BACKGROUND",(0,i),(-1,i), BG_PANEL))
    t.setStyle(TableStyle(st))
    return t

def legend_flowable():
    items = [("1+", "Il faut faire"), ("2+", "Il faut probablement faire"),
             ("1-", "Il ne faut pas faire"), ("2-", "Il ne faut probablement pas faire")]
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

TOTAL_PAGES = {"n": 7}

def on_page(canvas, doc, page_title):
    header_band(canvas, doc, "SFAR — CONFÉRENCE D'EXPERTS 2008 — FICHE DE SYNTHÈSE",
                "Prise en charge des NVPO",
                page_title, icon_fn=lambda c,x,y: icon_pill(c, x, y, 13*mm), color=TEAL_DARK)
    footer_band(canvas, doc, SOURCE_TXT, f"Page {doc.page} / {TOTAL_PAGES['n']}")

# ---------------------------------------------------------------------------
def _section_intro_q12():
    story = []
    story.append(Spacer(1, 3*mm))
    story.append(info_panel(P(
        "<b>Champ :</b> prise en charge des nausées et vomissements postopératoires (NVPO) chez "
        "l'adulte et l'enfant — prévention (identification du risque, prophylaxie pharmacologique "
        "et non pharmacologique) et traitement curatif. Conférence d'experts SFAR (texte court), "
        "10 « Questions » (chapitres), publiée 2008. <b>Convention de cotation propre à ce "
        "document</b> : G1+ = il faut faire ; G2+ = il faut probablement faire ; G1- = il ne faut "
        "pas faire ; G2- = il ne faut probablement pas faire — <b>pas de catégorie « avis "
        "d'experts »</b> : lorsque les données sont insuffisantes, le panel déclare explicitement "
        "ne pas être en mesure de formuler de recommandation (4 occurrences, signalées "
        "explicitement dans cette fiche).<br/><br/>"
        "<b>Q1 — Les NVPO, un problème important ?</b> Environ 30 % des patients opérés sont "
        "sujets à des NVPO, jusqu'à 80 % dans certains groupes à risque. Facteurs associés : sexe "
        "féminin, enfants/adolescents, antécédents de NVPO/mal des transports (incidence "
        "augmentée) ; tabagisme, alcoolisme (incidence réduite) ; anesthésie générale par "
        "inhalation halogénée (vs AIVOC propofol) ; opiacés périopératoires ; néostigmine "
        "&gt; 2,5 mg ; durée d'anesthésie/chirurgie prolongée. Conséquences : inconfort, douleur "
        "postopératoire majorée, pneumopathie d'inhalation, troubles hydroélectrolytiques, "
        "désunion de sutures, retard de mobilisation, surcoûts (SSPI, réadmissions).",
        S_BODY), bg=BG_PANEL, border=TEAL))
    story.append(Spacer(1, 3*mm))

    story.append(section_bar("Légende des grades (convention propre à ce document)"))
    story.append(Spacer(1, 2*mm))
    story.append(legend_flowable())
    story.append(Spacer(1, 4*mm))

    story.append(section_bar("Q2 — Facteurs de risque des NVPO chez l'adulte"))
    story.append(Spacer(1, 1.5*mm))
    story.append(P(
        "Facteurs bien établis : sexe féminin (OR≈3, facteur indépendant le plus important) ; "
        "non-fumeur (OR≈2) ; antécédents de NVPO/mal des transports ; anesthésie par inhalation "
        "halogénée (double le risque vs AIVOC) ; protoxyde d'azote (facteur indépendant, "
        "influence moindre que les halogénés) ; morphiniques postopératoires (double le risque). "
        "Facteurs possibles : ASA I-II, migraine, anesthésie locorégionale (risque moindre), "
        "hydratation pré/peropératoire optimale (pourrait réduire le risque), sonde "
        "nasogastrique (aggravant), néostigmine aux doses habituelles (≤2,5 mg, sans "
        "sur-risque probable) ; type de chirurgie non clairement démontré comme facteur "
        "(données plus controversées pour la chirurgie gynécologique/laparoscopique). "
        "Facteurs réfutés : obésité, cycle menstruel, rémifentanil, FiO2 élevée (80 %).", S_BODY_SM))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("Scores de\nprédiction", "Utiliser des scores de prédiction simplifiés pour estimer le "
                                    "risque de NVPO d'un patient donné.", "1+"),
    ], [26*mm, PAGE_W-2*MARGIN-26*mm-15*mm, 15*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(KeepTogether([
        P("<b>TABLEAU 1</b> — Scores simplifiés de prédiction des NVPO", S_H2),
        Spacer(1, 1*mm),
        simple_table(
            ["Facteur de risque", "Apfel et al.", "Koivuranta et al."],
            [
                ["Sexe féminin", "+", "+"],
                ["Antécédent de NVPO", "+", "+"],
                ["Mal des transports", "", "+"],
                ["Non-fumeur", "+", "+"],
                ["Morphiniques postopératoires", "+", ""],
                ["Durée d'anesthésie > 60 min", "", "+"],
                ["Pouvoir discriminant (AUC ROC)", "0,68-0,71", "0,70-0,71"],
            ], [70*mm, (PAGE_W-2*MARGIN-70*mm)/2, (PAGE_W-2*MARGIN-70*mm)/2]),
        Spacer(1, 1*mm),
        P("<i>Risque de NVPO (%) selon le nombre de facteurs présents — Apfel : 0→&lt;10 %, "
          "1→21 %, 2→39 %, 3→61 %, 4→79 % ; Koivuranta : 0→17 %, 1→18 %, 2→42 %, 3→54 %, "
          "4→74 %, 5→87 %. Score Apfel = 4 critères ; score Koivuranta = 5 critères.</i>", S_NOTE)
    ]))
    return story

def _section_q3_q4a():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Q3 — Les antagonistes du récepteur 5HT3 (AR-5HT3, « sétrons »)"))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("Prophylaxie\nsystématique", "L'administration prophylactique systématique d'AR-5HT3 "
                                        "n'est pas recommandée.", "1-"),
        ("Prophylaxie\nciblée", "L'administration prophylactique d'un AR-5HT3 est recommandée en "
                                  "fin d'intervention chez les patients à risque.", "1+"),
        ("Approche\nmultimodale", "L'usage d'AR-5HT3 est recommandé dans le cadre de l'approche "
                                     "multimodale des NVPO.", "1+"),
        ("Traitement\ncuratif", "L'usage d'AR-5HT3 est recommandé dans le traitement curatif de "
                                  "première intention des NVPO.", "1+"),
    ], [26*mm, PAGE_W-2*MARGIN-26*mm-15*mm, 15*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(P(
        "Efficaces quels que soient type d'intervention/anesthésie/patient ; pas de supériorité "
        "démontrée sur la dexaméthasone ou le dropéridol. Doses prophylaxie : ondansétron 4 mg, "
        "granisétron 0,3 mg, dolasétron 12,5 mg, tropisétron 2 mg. Doses traitement : ondansétron "
        "4 mg (efficace dès 1 mg), dolasétron 12,5 mg, granisétron 0,1 mg, tropisétron 0,5 mg. "
        "Ne pas répéter le même antiémétique avant 6h ; changer de classe en cas d'échec. Effets "
        "secondaires modérés (céphalées 10-20 %, constipation 5-10 %) ; allongement du QT "
        "(effet de classe, sans conséquence clinique démontrée chez l'adulte).", S_NOTE))
    story.append(Spacer(1, 2*mm))
    story.append(KeepTogether([
        P("<b>TABLEAU 2</b> — Pharmacocinétique et posologies des principaux AR-5HT3 (adulte)", S_H2),
        Spacer(1, 1*mm),
        simple_table(
            ["AR-5HT3", "Demi-vie (h)", "Métabolisme CYP450", "Posologie NVPO (mg)"],
            [
                ["Ondansétron", "3", "2D6 + autres", "4,0"],
                ["Granisétron", "9-11", "3A", "0,3-1,0"],
                ["Tropisétron", "7,3", "2D6", "5,0"],
                ["Dolasétron", "7-9", "2D6", "12,5"],
            ], [38*mm, 32*mm, 46*mm, PAGE_W-2*MARGIN-38*mm-32*mm-46*mm])
    ]))
    return story

def _section_q4b():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Q4 — Corticostéroïdes (dexaméthasone) et dropéridol"))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("Dexa —\nprophylaxie", "La dexaméthasone est recommandée dans la prévention des NVPO "
                                  "des patients à risque ; chez les patients à risque élevé, "
                                  "l'association à un AR-5HT3 et/ou au dropéridol est recommandée.", "1+"),
        ("Dexa — ACP", "Dans l'état actuel des connaissances, la dexaméthasone administrée en "
                        "peropératoire n'est pas suffisante pour se substituer à l'ajout de "
                        "dropéridol dans la prévention des NV induits par la morphine en ACP.", "2+"),
        ("Dexa —\ntraitement", "La dexaméthasone ne doit pas être utilisée seule dans le "
                                 "traitement curatif de NVPO.", "2-"),
        ("Dexa — dose", "La dose intraveineuse recommandée de dexaméthasone est comprise entre "
                         "4 et 8 mg, administrée à l'induction de l'anesthésie.", "1+"),
        ("Dexa —\nitération", "L'administration répétée de dexaméthasone n'a pas été évaluée "
                                "dans cette indication et ne peut de ce fait pas être recommandée.", "2-"),
    ], [26*mm, PAGE_W-2*MARGIN-26*mm-15*mm, 15*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(P(
        "Dexaméthasone : efficacité similaire aux AR-5HT3 et au dropéridol, supérieure au "
        "métoclopramide ; simple, bien tolérée, peu coûteuse en dose unique. Hyperglycémie "
        "possible (diabétiques et non diabétiques) ; données rassurantes sur le risque infectieux.",
        S_NOTE))
    return story

def _section_q4c():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("Dropéridol —\nprophylaxie", "Le dropéridol est recommandé dans la prophylaxie des NVPO "
                                        "chez les patients à risque.", "1+"),
        ("Dropéridol —\ntraitement", "Le dropéridol est recommandé pour le traitement des NVPO.", "2+"),
        ("Dropéridol —\nhaut risque", "Chez les patients à haut risque, l'association du "
                                        "dropéridol à un AR-5HT3 et/ou à la dexaméthasone peut être "
                                        "recommandée ; le dropéridol est recommandé dans la "
                                        "prévention des NV induits par la morphine en ACP.", "1+"),
        ("Dropéridol —\nQT long", "Le dropéridol devrait être évité dans les syndromes du QT "
                                    "long congénitaux ou acquis.", "2-"),
        ("Dropéridol —\ndose/itération", "Il est recommandé d'utiliser la dose minimale efficace "
                                           "de dropéridol (0,625 à 1,25 mg IV) ; en cas de "
                                           "nécessité, il pourrait être réadministré au bout de "
                                           "6 heures.", "2+"),
    ], [26*mm, PAGE_W-2*MARGIN-26*mm-15*mm, 15*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(P(
        "Posologie en ACP : dropéridol 0,015 à 0,050 mg par mg de morphine. Le moment optimal "
        "d'administration du dropéridol n'a pas pu être déterminé par le panel d'experts "
        "(pas de recommandation sur ce point précis). Bien toléré globalement ; peut majorer la "
        "sédation et les symptômes extrapyramidaux (surtout en ACP) ; allonge le QT à faible dose "
        "(données épidémiologiques rassurantes sur le risque rythmique).", S_NOTE))
    return story

def _section_q5():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Q5 — Antagonistes du récepteur NK1 (AR-NK1)"))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("Aprépitant", "L'aprépitant (40 mg per os, 1 à 3 heures avant l'intervention) peut être "
                        "utilisé pour la prévention des NVPO.", "2+"),
        ("Enfant/\nadolescent", "La tolérance et l'efficacité n'ayant pas été établies chez "
                                  "l'enfant et l'adolescent, l'utilisation chez les patients de "
                                  "moins de 18 ans n'est pas recommandée.", "1-"),
    ], [26*mm, PAGE_W-2*MARGIN-26*mm-15*mm, 15*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(P(
        "Seul AR-NK1 approuvé en France en 2008 pour la prévention des NVPO. Supérieur à "
        "l'ondansétron 4 mg IV sur les vomissements et les nausées postopératoires. Forme "
        "injectable non disponible en France à la date de publication.", S_NOTE))
    return story

def _section_q6():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Q6 — Autres traitements (hors sétrons, dropéridol, stéroïdes, AR-NK1)"))
    story.append(Spacer(1, 1.5*mm))
    story.append(reco_table([
        ("Acupuncture", "Chez les patients à risque opposés à une prophylaxie pharmacologique "
                         "recherchant des alternatives, une technique par stimulation de points "
                         "d'acupuncture (point P6) peut être considérée.", "2+"),
        ("Relaxation/\nhypnose", "Ni la relaxation, ni l'hypnose ne peuvent être recommandées "
                                   "pour la prise en charge des NVPO.", "2-"),
        ("Cannabinoïdes", "Les cannabinoïdes ne doivent pas être utilisés pour le contrôle des "
                           "NVPO.", "1-"),
        ("Aromathérapie", "L'aromathérapie ne peut être recommandée pour le contrôle des NVPO.", "2-"),
        ("Oxygène —\npéropératoire", "La supplémentation en oxygène ne peut être recommandée en "
                                       "tant que mesure de contrôle des NVPO réalisée en "
                                       "peropératoire.", "1-"),
        ("Oxygène —\npostopératoire", "La supplémentation en oxygène ne peut être recommandée en "
                                        "tant que mesure de contrôle des NVPO réalisée en "
                                        "postopératoire.", "2-"),
        ("Soluté de\nremplissage", "La période de jeûne doit être compensée par l'administration "
                                     "d'une quantité adéquate de fluide.", "1+"),
        ("Métoclo-\npramide", "En raison d'une activité antiémétique modeste aux doses faibles et du "
                            "risque accru d'effets indésirables aux doses élevées, le "
                            "métoclopramide ne peut être recommandé en antiémétique de première "
                            "ligne.", "1-"),
    ], [26*mm, PAGE_W-2*MARGIN-26*mm-15*mm, 18*mm]))
    return story

def _section_q6b():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("Halopéridol —\nutilisation", "L'halopéridol à petites doses peut être utilisé comme "
                                          "antiémétique pour le contrôle des NVPO.", "2+"),
        ("Halopéridol —\n1ère ligne", "L'halopéridol ne peut pas être considéré comme un "
                                         "médicament de première ligne dans cette indication.", "2-"),
        ("Scopolamine\ntransdermique", "En l'absence de contre-indication, la scopolamine "
                                          "transdermique peut être considérée en tant "
                                          "qu'antiémétique pour la prévention des NVPO.", "2+"),
        ("AR-H1\n(prométhazine…)", "Les anesthésistes peuvent envisager le recours à la "
                                      "prométhazine ou au dimenhydrinate lorsque les autres "
                                      "antiémétiques dont l'effet est mieux établi ne sont pas "
                                      "disponibles.", "2+"),
        ("AR-H2", "Pour la prévention ou le traitement des NVPO, les AR-H2 ne peuvent être "
                   "recommandés.", "2-"),
        ("Gingembre", "Du fait de l'absence de données validées suffisantes, le groupe ne peut "
                       "recommander le gingembre pour le contrôle des NVPO.", "2-"),
        ("Midazolam", "Les anesthésistes peuvent considérer le midazolam en tant qu'alternative "
                       "lorsque d'autres antiémétiques dont l'effet est mieux établi ne sont pas "
                       "disponibles.", "2+"),
        ("Propofol à\npetites doses", "Pour le contrôle des NVPO établis résistant à d'autres "
                                         "traitements, on peut envisager la perfusion de propofol "
                                         "à petites doses subanesthésiques, sous surveillance par "
                                         "du personnel médical qualifié dans une structure adaptée.", "2+"),
    ], [26*mm, PAGE_W-2*MARGIN-26*mm-15*mm, 18*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(info_panel(P(
        "<b>Pas de recommandation possible (données insuffisantes)</b> — le panel déclare "
        "explicitement, dans les mêmes termes pour chacune des 4 substances suivantes, « ne pas "
        "être en mesure de proposer de recommandation » : <b>dixyrazine</b> (relation dose-effet "
        "inconnue, effets secondaires mal compris) ; <b>éphédrine</b> (peu d'essais, relation "
        "dose-effet non établie) ; <b>clonidine</b> (très peu d'essais randomisés) ; "
        "<b>gabapentine</b> (effet antiémétique propre non distingué d'un effet d'épargne "
        "opioïde).",
        S_BODY_SM), bg=GREY_LIGHT, border=GREY))
    return story

def _section_q7_fig1():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Q7 — Stratégies de prise en charge des NVPO"))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("Monothérapie", "La prévention antiémétique par un seul agent n'est recommandée que "
                          "chez des patients à faible risque de NVPO, et seulement si un "
                          "traitement de secours rapidement efficace peut être assuré sans délai.", "2+"),
        ("Combinaison", "Une combinaison de deux agents antiémétiques au moins doit être "
                         "utilisée pour la prévention des NVPO chez les patients présentant des "
                         "risques modérés ou élevés.", "1+"),
        ("Multimodal\nhaut risque", "Les patients à haut risque doivent bénéficier d'une "
                                       "approche multimodale de prévention des NVPO.", "1+"),
        ("Secours —\n1ère intention", "En l'absence de prophylaxie, les AR-5HT3 sont recommandés "
                                         "pour le traitement de première intention des NVPO.", "1+"),
        ("Secours —\néchec prophylaxie", "Si une prophylaxie a échoué dans les six heures suivant "
                                            "son administration, il est recommandé d'utiliser pour "
                                            "le traitement de secours un antiémétique d'une autre "
                                            "classe que celle qui a été choisie pour la prophylaxie ; "
                                            "une association d'antiémétiques est raisonnable pour "
                                            "assurer un traitement curatif et une prophylaxie "
                                            "secondaire efficaces.", "2+"),
    ], [26*mm, PAGE_W-2*MARGIN-26*mm-15*mm, 15*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(P(
        "<b>Conclusion (non graduée) :</b> les algorithmes améliorent la prise en charge "
        "antiémétique. Il n'existe cependant pas de preuve de la supériorité d'un algorithme par "
        "rapport aux autres — le facteur le plus important est le nombre d'antiémétiques "
        "administrés, pas l'algorithme précis suivi.", S_NOTE))
    story.append(Spacer(1, 3*mm))
    story.append(KeepTogether([
        P("<b>FIGURE 1</b> — Exemple d'algorithme de prise en charge des NVPO", S_H2),
        Spacer(1, 1*mm),
        P("<i>Redessin en tableau de l'algorithme de la page 876 du document source (vérifié "
          "visuellement à 200dpi) — combine le score de risque simplifié (Tableau 1, 0 à 4 "
          "facteurs), les circonstances/souhaits du patient, et 3 filières prophylaxie/secours "
          "par niveau de risque.</i>", S_NOTE),
        Spacer(1, 1.5*mm),
        simple_table(
            ["Niveau de risque", "Prophylaxie", "Traitement de secours"],
            [
                ["Faible\n(0-1 facteur)", "Expectative armée (pas de prophylaxie systématique, "
                 "traitement de secours prêt) — la monothérapie prophylactique reste une option "
                 "à ce niveau de risque si un traitement de secours rapide est assuré (cf. Q7)",
                 "1) AR-5HT3 ; 2) autre antiémétique validé ; 3) envisager la combinaison "
                 "d'interventions"],
                ["Moyen\n(≈2 facteurs)", "Dexaméthasone 4 mg + un autre antiémétique",
                 "1) antiémétique(s) de classe(s) différente(s) ; 2) combinaison d'interventions"],
                ["Élevé\n(3-4 facteurs)", "AG intraveineuse + dexaméthasone 4 mg + un autre "
                 "antiémétique (si possible, réduire le risque de base : ALR, éviter halogénés "
                 "peropératoires et morphiniques postopératoires)",
                 "1) antiémétique(s) de classe(s) différente(s) ; 2) combinaison d'interventions"],
            ], [26*mm, (PAGE_W-2*MARGIN-26*mm)*0.42, (PAGE_W-2*MARGIN-26*mm)*0.58])
    ]))
    return story

def _section_q8_q9():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Q8 — Intégration des situations locales ou particulières"))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("Algorithme", "Il est recommandé d'utiliser un algorithme pour la prise en charge des "
                        "NVPO, et d'adapter cette prise en charge aux situations locales ou "
                        "particulières.", "1+"),
        ("Programme\nqualité", "Cette démarche peut s'inscrire dans le cadre général d'un "
                                  "programme qualité institutionnel.", "2+"),
        ("Facteurs\nsuppl.", "Au-delà des facteurs de risque reconnus, il est recommandé "
                                         "de prendre en compte les situations où les vomissements "
                                         "entraînent un risque particulier pour le patient, de "
                                         "considérer les contraintes locales périopératoires, et de "
                                         "tenir compte des désirs exprimés par le patient.", "1+"),
    ], [26*mm, PAGE_W-2*MARGIN-26*mm-15*mm, 18*mm]))
    story.append(Spacer(1, 3*mm))

    story.append(section_bar("Q9 — Particularités en chirurgie pédiatrique"))
    story.append(Spacer(1, 1.5*mm))
    story.append(P(
        "Incidence des VPO ≈ 30 % tous âges/chirurgies confondus, jusqu'à 80 % pour strabisme, "
        "amygdalectomie, hernie inguinale, neurochirurgie. Facteur âge : faible avant 3 ans, "
        "augmente ensuite ; sexe : jeunes filles plus affectées après la puberté ; antécédent "
        "personnel/familial de VPO/NVPO/mal des transports.", S_BODY_SM))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("Dépistage", "L'identification des facteurs de risque est souhaitable pour établir une "
                       "stratégie de prise en charge préventive des VPO de l'enfant.", "2+"),
        ("Faible risque", "Chez les enfants à faible risque, l'administration prophylactique "
                           "d'antiémétique n'est pas indiquée.", "1-"),
        ("Risque de base", "Il est recommandé de réduire autant que possible le risque de base, "
                            "en proposant une technique anesthésique la moins émétisante "
                            "possible.", "2+"),
        ("Risque modéré/\nélevé", "Il est recommandé d'utiliser une stratégie préventive "
                                     "privilégiant les associations d'antiémétiques, supérieures "
                                     "aux monothérapies, en tenant compte de l'efficacité, des "
                                     "effets secondaires et du coût.", "2+"),
        ("1ère intention", "L'association thérapeutique préconisée en première intention combine "
                            "un AR-5HT3 à la dexaméthasone.", "2+"),
        ("Traitement\nétabli", "Le traitement des NVPO établis ou de leur récidive est extrapolé "
                                 "de celui de l'adulte.", "2+"),
        ("Échec\nprophylaxie", "En cas d'échec d'une prophylaxie, il est recommandé d'utiliser une "
                                  "autre classe antiémétique que celle déjà mise en œuvre.", "2+"),
        ("Réadmin.\nantiémétique", "Il est éventuellement possible de réadministrer le même "
                               "antiémétique après une durée de six heures.", "2+"),
        ("Réadmin.\ndexaméthasone", "Il est recommandé de ne pas réadministrer la "
                                       "dexaméthasone.", "2-"),
        ("Dropéridol —\nusage restreint", "Il est recommandé de n'utiliser le dropéridol qu'en cas "
                                              "d'échec des autres classes et seulement si le patient "
                                              "est hospitalisé.", "2+"),
    ], [26*mm, PAGE_W-2*MARGIN-26*mm-15*mm, 18*mm]))
    return story

def _section_q9tab_q10_trace():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(KeepTogether([
        P("<b>TABLEAU 3</b> — Facteurs de risque de NVPO chez l'enfant", S_H2),
        Spacer(1, 1*mm),
        simple_table(
            ["Facteur de risque"],
            [
                ["Âge supérieur à 3-4 ans"],
                ["Antécédent de NVPO/mal des transports, personnel ou familial"],
                ["Durée de chirurgie supérieure à 30-45 min"],
                ["Chirurgie du strabisme"],
            ], [PAGE_W-2*MARGIN])
    ]))
    story.append(Spacer(1, 3*mm))
    story.append(KeepTogether([
        P("<b>TABLEAU 4</b> — Antiémétiques en pédiatrie : posologies en monothérapie", S_H2),
        Spacer(1, 1*mm),
        simple_table(
            ["Antiémétique", "Posologie (IV, mg/kg)", "Dose maximale (mg)"],
            [
                ["Dropéridol", "50 à 75 µg/kg", "1,25"],
                ["Dexaméthasone", "150 µg/kg", "5,00"],
                ["Ondansétron", "50 à 100 µg/kg", "4,00"],
                ["Dolasétron", "350 µg/kg", "12,50"],
            ], [50*mm, 60*mm, PAGE_W-2*MARGIN-50*mm-60*mm]),
        Spacer(1, 1*mm),
        P("<i>D'après Gan TJ, et al. Anesth Analg 2003;97:62-71. Unité de posologie confirmée "
          "µg/kg par vérification visuelle de la page source (l'extraction automatique du texte "
          "supprime le glyphe µ — bug d'extraction déjà rencontré ailleurs dans ce corpus).</i>", S_NOTE)
    ]))
    story.append(Spacer(1, 4*mm))

    story.append(section_bar("Q10 — Particularités en chirurgie ambulatoire"))
    story.append(Spacer(1, 1.5*mm))
    story.append(P(
        "Les NVPO prolongent le séjour, retardent le retour à domicile, augmentent le risque "
        "d'admission imprévue et diminuent la satisfaction du patient. Aucune stratégie "
        "spécifique à la chirurgie ambulatoire ne réduit la survenue des NVPO au-delà de la "
        "réduction du risque de base (analgésie multimodale, hydratation IV, anesthésie "
        "locorégionale).", S_BODY_SM))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("Haut risque\nambulatoire", "Il est recommandé d'adopter une stratégie antiémétique "
                                        "prophylactique multimodale chez les patients ambulatoires "
                                        "identifiés à haut risque de NVPO.", "1+"),
        ("Après la\nsortie", "Le traitement des NVPO survenant après la sortie repose sur la "
                               "prescription d'antiémétiques validés en prophylaxie, en changeant "
                               "de classe et sous une forme galénique adaptée.", "2+"),
    ], [26*mm, PAGE_W-2*MARGIN-26*mm-15*mm, 15*mm]))
    story.append(Spacer(1, 4*mm))

    story.append(section_bar("Sources et traçabilité", color=GREY))
    story.append(Spacer(1, 2*mm))
    story.append(P(
        "<b>Document source :</b> « Prise en charge des nausées et vomissements postopératoires » "
        "— Conférence d'experts, texte court, SFAR. Coordonnateur : P. Diemunsch (Strasbourg). "
        "10 chapitres rédigés par un panel international d'auteurs (France, Belgique, Suisse, "
        "Allemagne, Finlande, États-Unis).",
        S_SOURCE))
    story.append(Spacer(1, 1.5*mm))
    story.append(P("<b>Publication :</b> Ann Fr Anesth Réanim 2008;27:866-878, disponible en "
                    "ligne le 25/10/2008. DOI 10.1016/j.annfar.2008.09.004.", S_SOURCE))
    story.append(P("<b>Méthodologie :</b> système GRADE, convention de cotation propre au "
                    "document (G1+/G2+/G1-/G2-, pondérée par la balance bénéfices/risques ; pas "
                    "de catégorie « avis d'experts » — items sans recommandation possible "
                    "déclarés explicitement comme tels).", S_SOURCE))
    story.append(P("<b>URL source :</b> https://sfar.org/prise-en-charge-des-nausees-et-vomissements-postoperatoires/", S_SOURCE))
    story.append(Spacer(1, 3*mm))
    story.append(info_panel(P(
        "<b>Avertissement :</b> ce document est une fiche de synthèse indépendante, produite pour "
        "un usage d'aide-mémoire. Il reprend l'intégralité des recommandations graduées, des 4 "
        "items « pas de recommandation » et des 4 tableaux + 1 figure de la conférence d'experts, "
        "mais ne remplace pas le texte intégral et n'est ni édité ni validé par la SFAR. En cas "
        "de doute, se référer au texte intégral et/ou à un avis spécialisé.",
        S_BODY_SM), bg=GREY_LIGHT, border=GREY))
    return story

def _section_1():
    return _section_intro_q12()

def _section_2():
    return _section_q3_q4a() + [Spacer(1, 3*mm)] + _section_q4b()

def _section_3():
    return _section_q4c() + [Spacer(1, 3*mm)] + _section_q5()

def _section_4():
    return _section_q6() + [Spacer(1, 3*mm)] + _section_q6b()

def _section_5():
    return _section_q7_fig1()

def _section_6():
    return _section_q8_q9()

def _section_7():
    return _section_q9tab_q10_trace()

def _section_a():
    return _section_1() + [Spacer(1, 3*mm)] + _section_2()

def _section_b():
    return _section_3() + [Spacer(1, 3*mm)] + _section_4()

def _section_c():
    return _section_5() + [Spacer(1, 3*mm)] + _section_6()

SECTIONS = [
    ("Q1-4 — Introduction, facteurs de risque, sétrons, stéroïdes", _section_a),
    ("Q4-6 — Dropéridol, NK1, autres traitements", _section_b),
    ("Q7-9 — Stratégies, algorithme, situations locales, pédiatrie", _section_c),
    ("Q9-10 — Pédiatrie (suite), ambulatoire, traçabilité", _section_7),
]

def _make_doc():
    return SimpleDocTemplate(OUT, pagesize=A4,
                              leftMargin=MARGIN, rightMargin=MARGIN,
                              topMargin=32*mm, bottomMargin=16*mm,
                              title="Fiche SFAR 2008 - Prise en charge des NVPO",
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
