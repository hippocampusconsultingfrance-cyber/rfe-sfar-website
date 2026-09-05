# -*- coding: utf-8 -*-
"""
Fiche de synthese - RFE commune SFAR-SFMU 2021
Choix du solute pour le remplissage vasculaire en situation critique
Source verifiee : sfar.org (texte valide CRC SFAR 10/05/21, CA SFAR 19/05/21, CA SFMU 29/06/21)
Methodologie GRADE, tags "GRADE X+/-, accord FORT" ou "Avis d'experts, accord FORT" imprimes
litteralement apres chaque recommandation (meme convention basse-risque que traumatisme_abdominal/
vni/curares). 9 recommandations numerotees R1.1-R3.2 (dont 1 avis d'experts) + 2 questions "absence
de recommandation" (albumine 2e intention au cours du sepsis ; choix du solute en peripartum) +
1 tableau de composition des solutes (Tableau 1, image source sans texte extractible, verifie
visuellement et retranscrit integralement). Resume officiel entierement coherent en interne
(9 recs = 2 GRADE1 + 6 GRADE2 + 1 avis d'experts ; 2 questions sans recommandation) - pas
d'incoherence arithmetique a signaler ici, contrairement a d'autres fiches du projet. Le resume
mentionne egalement "trois protocoles de prise en charge" qui ne sont PAS presents (texte ni
figure) dans ce PDF source (texte court, 28 pages) malgre verification visuelle exhaustive de
toutes les pages : disclosure explicite faite dans la fiche plutot que contenu invente.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from style import *
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.units import mm

OUT = "/private/tmp/claude-501/-Users-macbook-Downloads-claude/65498e3e-5ddf-47a6-b100-3ac535d1faa0/scratchpad/rfe_sfar/output/Fiche_SFAR_Remplissage_Vasculaire_2021.pdf"

SOURCE_TXT = ("Source : Recommandations Formalisées d'Experts communes SFAR-SFMU « Choix du soluté "
              "pour le remplissage vasculaire en situation critique » (2021) — texte validé par le "
              "Comité des Référentiels Cliniques de la SFAR (10/05/2021), le CA SFAR (19/05/2021) et "
              "le CA SFMU (29/06/2021). Méthodologie GRADE. Fiche de synthèse non officielle : se "
              "référer au texte intégral.")

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

TOTAL_PAGES = {"n": 6}

def on_page(canvas, doc, page_title):
    header_band(canvas, doc, "SFAR / SFMU — RFE 2021 — FICHE DE SYNTHÈSE",
                "Remplissage vasculaire",
                page_title, icon_fn=lambda c,x,y: icon_drop(c, x, y, 13*mm), color=NAVY)
    footer_band(canvas, doc, SOURCE_TXT, f"Page {doc.page} / {TOTAL_PAGES['n']}")

# ---------------------------------------------------------------------------
def _section_intro():
    story = []
    story.append(Spacer(1, 3*mm))
    story.append(info_panel(P(
        "<b>Champ :</b> choix du <b>type</b> de soluté de remplissage vasculaire en situation "
        "critique (ce référentiel ne traite ni de la quantité à administrer, ni des modalités "
        "d'administration). Groupe de 24 experts SFAR/SFMU, méthode GRADE®, format PICO. Quatre "
        "champs cliniques, chacun exploré par 2 questions : (1) un colloïde diminue-t-il la "
        "morbi-mortalité par rapport aux cristalloïdes ? (2) un type particulier de cristalloïde "
        "diminue-t-il la morbi-mortalité ?<br/><br/>"
        "<b>Résultats (résumé officiel) :</b> neuf recommandations formulées ; 2 de niveau de "
        "preuve élevé (GRADE 1+/-), 6 de niveau de preuve faible (GRADE 2+/-), 1 avis d'experts. "
        "Accord fort obtenu pour l'ensemble après deux tours de cotation. Pour 2 questions, "
        "aucune recommandation n'a pu être formulée.<br/><br/>"
        "<b>Périmètre exclu</b> de cette RFE (déjà couvert par d'autres référentiels ou hors "
        "champ) : cirrhose, pancréatite aiguë, SDRA, insuffisance rénale, population "
        "pédiatrique.<br/><br/>"
        "<i>Le résumé officiel mentionne également « trois protocoles de prise en charge » "
        "élaborés par les experts. Après vérification visuelle exhaustive des 28 pages du "
        "document source (texte court), ces protocoles n'y apparaissent ni sous forme de texte "
        "ni sous forme de figure — ils ne sont donc pas reproduits ici. Se référer au texte "
        "long / aux annexes de la RFE pour ces protocoles.</i>",
        S_BODY), bg=BG_PANEL, border=TEAL))
    story.append(Spacer(1, 3*mm))

    story.append(section_bar("Légende des grades (méthodologie GRADE)"))
    story.append(Spacer(1, 2*mm))
    story.append(legend_flowable())
    story.append(Spacer(1, 4*mm))

    story.append(section_bar("Les 4 champs cliniques"))
    story.append(Spacer(1, 2*mm))
    cw = PAGE_W - 2*MARGIN
    story.append(simple_table(
        ["Champ", "Population"],
        [
            ["1", "Patients atteints de sepsis ou de choc septique"],
            ["2", "Patients en situation de choc hémorragique"],
            ["3", "Patients cérébrolésés"],
            ["4", "Patientes en péripartum"],
        ],
        [cw*0.12, cw*0.88]))
    story.append(Spacer(1, 4*mm))

    story.append(section_bar("Tableau 1 — Composition des solutés de remplissage disponibles"))
    story.append(Spacer(1, 2*mm))
    cw = PAGE_W - 2*MARGIN
    cols = [cw*0.20] + [cw*0.16]*5
    story.append(simple_table(
        ["Composition", "Plasma", "NaCl 0,9 %", "Ringer Lactate", "Plasma-lyte", "Isofundine"],
        [
            ["Na+ (mmol/l)", "142", "154", "130", "140", "145"],
            ["K+ (mmol/l)", "4", "—", "4", "5", "4"],
            ["Cl- (mmol/l)", "103", "154", "108", "98", "127"],
            ["Ca2+ (mmol/l)", "2,4", "—", "0,9", "0", "2,5"],
            ["Mg2+ (mmol/l)", "1", "—", "—", "3", "1"],
            ["HCO3- (mmol/l)", "27", "—", "—", "—", "—"],
            ["Autre (mmol/l)", "Lactate 2", "—", "Lactate 27,6", "Acétate 27 / Gluconate 23",
             "Acétate 27 / Malate 5"],
            ["Osmolarité (mOsm/l)", "285", "308", "277", "295", "309"],
            ["pH", "7,4", "5-6,5", "6-7,5", "6,5-7,5", "5-6,5"],
        ],
        cols))
    story.append(Spacer(1, 2*mm))
    story.append(P("Isotoniques : osmolarité 280-310 mOsm/L (NaCl 0,9 %, Plasmalyte, Isofundine). "
                    "Hypotonique : &lt; 280 mOsm/L (Ringer lactate). Hypertoniques : &gt; 310 mOsm/L "
                    "(NaCl 3 %, NaCl 7,5 %). « Solutés balancés » = composition ionique proche du "
                    "plasma (Ringer lactate, Plasmalyte, Isofundine), par opposition au NaCl 0,9 % "
                    "(riche en chlore). Le potassium des solutés balancés (4-5 mmol/l) n'entraîne pas "
                    "d'augmentation de la kaliémie, y compris chez le patient hyperkaliémique "
                    "(études randomisées chez le transplanté rénal).", S_NOTE))
    return story

def _section_champ1():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Champ 1 — Sepsis ou choc septique : colloïdes vs cristalloïdes"))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("R1.1", "Il n'est pas recommandé d'utiliser les hydroxyéthylamidons pour le remplissage "
         "vasculaire au cours du sepsis ou du choc septique, comparativement aux cristalloïdes non "
         "hypertoniques, pour diminuer la mortalité et/ou le recours à l'épuration extrarénale.", "1-"),
        ("R1.2", "Les experts suggèrent de ne pas utiliser les gélatines pour le remplissage "
         "vasculaire au cours du sepsis ou du choc septique, comparativement aux cristalloïdes non "
         "hypertoniques, pour diminuer la mortalité et/ou le recours à l'épuration extrarénale.", "AE"),
        ("R1.3", "Il n'est probablement pas recommandé d'utiliser en première intention de "
         "l'albumine au cours du sepsis ou du choc septique, comparativement aux cristalloïdes, "
         "pour diminuer la mortalité ou le recours à l'épuration extrarénale.", "2-"),
    ], [16*mm, PAGE_W-2*MARGIN-16*mm-20*mm, 20*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(P("Hydroxyéthylamidons (HEA) : essais VISEP et 6S (populations septiques) — "
                    "surmortalité et insuffisance rénale aiguë accrue. CHEST et CRISTAL n'ont pas "
                    "confirmé la surmortalité ; CHEST rapporte en outre un recours accru à "
                    "l'épuration extrarénale dans le groupe HEA. L'Agence européenne des "
                    "médicaments a recommandé en 2013 l'arrêt "
                    "des HEA en réanimation, en particulier chez le patient septique. Gélatines : "
                    "signal d'insuffisance rénale et de réactions anaphylactiques dans certaines "
                    "études, sans supériorité démontrée. Albumine : 5 essais randomisés (dont SAFE, "
                    "ALBIOS, EARSS), aucun bénéfice de survie établi malgré des hypothèses "
                    "physiopathologiques favorables ; une seule méta-analyse sur 6 retrouve un "
                    "bénéfice (Xu et al., OR 0,81).", S_NOTE))
    story.append(Spacer(1, 3*mm))
    story.append(no_reco_panel("Après analyse de la littérature, les experts ne sont pas en mesure "
                                "d'émettre une recommandation concernant l'utilisation d'albumine en "
                                "seconde intention chez les patients atteints d'hypoalbuminémie "
                                "majeure et/ou nécessitant des volumes de remplissage importants."))
    story.append(Spacer(1, 2*mm))
    story.append(P("Plusieurs études (SAFE, ALBIOS) suggèrent un bénéfice de l'albumine sur la "
                    "réduction des volumes de remplissage et l'amélioration de la fonction "
                    "circulatoire, sans que le niveau de preuve soit jugé suffisant par les experts "
                    "pour une recommandation formelle — malgré une suggestion en ce sens de la "
                    "Surviving Sepsis Campaign 2016.", S_NOTE))
    story.append(Spacer(1, 4*mm))

    story.append(section_bar("Champ 1 (suite) — Choix du type de cristalloïde"))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("R1.4", "Chez les patients atteints de sepsis ou de choc septique, il est probablement "
         "recommandé d'utiliser des solutés cristalloïdes balancés pour le remplissage vasculaire "
         "pour diminuer la mortalité et/ou la survenue d'évènements indésirables rénaux.", "2+"),
    ], [16*mm, PAGE_W-2*MARGIN-16*mm-20*mm, 20*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(P("Étude SMART (15 802 patients, sous-groupe sepsis n=2336) : moins d'événements "
                    "rénaux majeurs à 30 jours avec les solutés balancés (OR 0,80). Méta-analyse "
                    "Tseng 2020 (intégrant les données non publiées de CRISTAL) : moindre mortalité "
                    "avec solutés balancés vs NaCl 0,9 % (OR 0,84). Résultat non retrouvé sur la "
                    "survenue d'insuffisance rénale aiguë. Seule l'étude SPLIT (77 patients "
                    "septiques sur &gt; 2000) ne va pas dans ce sens, jugée peu généralisable.", S_NOTE))
    return story

def _section_champ2():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Champ 2 — Choc hémorragique : colloïdes vs cristalloïdes"))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("R2.1", "Chez les patients en situation de choc hémorragique, quel que soit le contexte, "
         "il n'est probablement pas recommandé d'utiliser un colloïde comme soluté de remplissage "
         "vasculaire, comparativement aux cristalloïdes non hypertoniques, pour diminuer la "
         "mortalité et/ou le recours à l'épuration extrarénale.", "2-"),
    ], [16*mm, PAGE_W-2*MARGIN-16*mm-20*mm, 20*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(P("Depuis 2014, la HAS restreint l'usage des hydroxyéthylamidons à la 2e intention "
                    "en cas de pertes sanguines si les cristalloïdes sont jugés insuffisants. "
                    "Méta-analyses les plus récentes : pas de bénéfice de mortalité des HEA/gélatines "
                    "vs cristalloïdes chez le traumatisé. Essais FLASH et Kabon et al. (chirurgie "
                    "abdominale à haut risque hémorragique) : pas de différence sur le critère "
                    "composite principal ; insuffisance rénale plus fréquente sous HEA dans FLASH. "
                    "HEA également associé à un risque hémorragique accru par trouble de l'hémostase "
                    "en périopératoire de chirurgie majeure. Pas d'étude dédiée pour l'albumine au "
                    "cours de l'hémorragie ; il n'est probablement pas recommandé d'en administrer.", S_NOTE))
    story.append(Spacer(1, 4*mm))

    story.append(section_bar("Champ 2 (suite) — Choix du type de cristalloïde"))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("R2.2", "Chez les patients en situation de choc hémorragique, il est probablement "
         "recommandé d'utiliser des solutés cristalloïdes balancés en première intention plutôt "
         "que du NaCl 0,9 % comme soluté de remplissage vasculaire pour diminuer la mortalité "
         "et/ou les évènements indésirables rénaux.", "2+"),
        ("R2.3", "Chez les patients en situation de choc hémorragique, il n'est pas recommandé "
         "d'administrer un soluté salé hypertonique à 3 % ou 7,5 % en première intention comme "
         "soluté de remplissage vasculaire pour diminuer la mortalité.", "1-"),
    ], [16*mm, PAGE_W-2*MARGIN-16*mm-20*mm, 20*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(P("Aucune étude randomisée n'a spécifiquement comparé NaCl 0,9 % et solutés "
                    "balancés au cours du choc hémorragique (volumes typiquement &gt; 5000-10 000 mL "
                    "sur 24 h en traumatologie). Les données disponibles (études observationnelles, "
                    "extrapolations d'essais en réanimation/périopératoire) montrent une association "
                    "entre hyperchlorémie/hauts volumes de solutés riches en chlore et surmortalité, "
                    "orientant le choix vers les solutés balancés en première intention, en l'absence "
                    "d'étude dédiée robuste (d'où un GRADE 2 et non 1).", S_NOTE))
    story.append(Spacer(1, 2*mm))
    story.append(info_panel(P(
        "<b>Exception SSH :</b> les experts soulignent que dans les situations associant choc "
        "hémorragique et traumatisme crânien grave avec signe de focalisation, l'administration "
        "d'un bolus de sérum salé hypertonique reste indiquée pour son effet osmotique.",
        S_BODY), bg=AMBER_LIGHT, border=AMBER))
    return story

def _section_champ3_4():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Champ 3 — Patients cérébrolésés"))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("R3.1", "Il n'est probablement pas recommandé d'utiliser des colloïdes, en particulier "
         "l'albumine, comme soluté de remplissage chez les patients cérébrolésés pour diminuer la "
         "mortalité et/ou améliorer le pronostic neurologique.", "2-"),
        ("R3.2", "Il est probablement recommandé d'utiliser des cristalloïdes isotoniques, en "
         "première intention, comme soluté de remplissage vasculaire chez les patients "
         "cérébrolésés pour diminuer la mortalité et/ou améliorer le pronostic neurologique.", "2+"),
    ], [16*mm, PAGE_W-2*MARGIN-16*mm-20*mm, 20*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(P("Étude SAFE (sous-groupe traumatisés crâniens, n=460) : surmortalité sous "
                    "albumine 4 % (RR 1,63). Étude ALIAS (AVC) : pas de bénéfice de l'albumine 25 %, "
                    "risque accru d'œdème pulmonaire/hématome intracérébral. À l'inverse, dans "
                    "l'hémorragie sous-arachnoïdienne, l'albumine était associée à un meilleur "
                    "pronostic dans une étude rétrospective — données limitées et controversées.<br/>"
                    "Solutés hypotoniques (Ringer lactate, &lt; 280 mOsm/L) à éviter à la phase aiguë "
                    "du fait du risque d'œdème cérébral : une étude préhospitalière retrouve une "
                    "surmortalité avec le Ringer lactate comparé au NaCl 0,9 % chez le traumatisé "
                    "crânien (HR 1,78). Les experts ne peuvent pas se positionner sur une éventuelle "
                    "supériorité des solutés isotoniques balancés par rapport au NaCl 0,9 % dans "
                    "cette population (faible niveau de preuve, 2 petits essais randomisés montrant "
                    "seulement une réduction du risque d'hyperchlorémie).", S_NOTE))
    story.append(Spacer(1, 5*mm))

    story.append(section_bar("Champ 4 — Patientes en péripartum"))
    story.append(Spacer(1, 2*mm))
    story.append(no_reco_panel("Du fait de l'absence de donnée disponible dans la littérature, "
                                "aucune recommandation spécifique ne peut être émise concernant le "
                                "choix du soluté de remplissage vasculaire à utiliser dans la prise "
                                "en charge réanimatoire des femmes en péripartum. Par défaut, le "
                                "soluté de remplissage utilisé sera celui recommandé selon le "
                                "contexte dans la population générale."))
    return story

def _section_synthese():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Synthèse et messages clés"))
    story.append(Spacer(1, 2*mm))
    story.append(P(
        "• <b>Hydroxyéthylamidons :</b> non recommandés en situation critique (sepsis, choc "
        "hémorragique) — signal de surmortalité/insuffisance rénale au cours du sepsis, absence de "
        "bénéfice et risque hémorragique au cours du choc hémorragique.<br/>"
        "• <b>Gélatines :</b> à ne pas utiliser au cours du sepsis (avis d'experts).<br/>"
        "• <b>Albumine :</b> pas de bénéfice de mortalité démontré en 1re intention au cours du "
        "sepsis ; pas de donnée dédiée au choc hémorragique (probablement à ne pas utiliser) ; "
        "probablement délétère chez le cérébrolésé (surmortalité en sous-groupe traumatisme "
        "crânien).<br/>"
        "• <b>Cristalloïdes balancés</b> (Ringer lactate, Plasmalyte, Isofundine) probablement "
        "préférés au NaCl 0,9 % au cours du sepsis et du choc hémorragique (moindre risque rénal, "
        "meilleur équilibre acido-basique) — sans crainte fondée d'hyperkaliémie.<br/>"
        "• <b>Cérébrolésés :</b> cristalloïdes isotoniques en première intention ; éviter les "
        "solutés hypotoniques (Ringer lactate) à la phase aiguë (risque d'œdème cérébral).<br/>"
        "• <b>Sérum salé hypertonique :</b> non recommandé en première intention au cours du choc "
        "hémorragique isolé — sauf association à un traumatisme crânien grave avec signe de "
        "focalisation, où un bolus reste indiqué.<br/>"
        "• <b>Péripartum :</b> aucune donnée spécifique — appliquer les recommandations de la "
        "population générale selon le contexte clinique.",
        S_BODY))
    story.append(Spacer(1, 5*mm))

    story.append(section_bar("Sources et traçabilité", color=GREY))
    story.append(Spacer(1, 2*mm))
    story.append(P(
        "<b>Document source :</b> « Choix du soluté pour le remplissage vasculaire en situation "
        "critique » — Recommandations Formalisées d'Experts communes SFAR-SFMU. Comité de 24 "
        "experts, coordination O. Joannes-Boyau (SFAR), P. Le Conte (SFMU). Texte validé par le "
        "Comité des Référentiels Cliniques de la SFAR le 10/05/2021, le Conseil d'Administration de "
        "la SFAR le 19/05/2021 et le Conseil d'Administration de la SFMU le 29/06/2021.", S_SOURCE))
    story.append(Spacer(1, 1.5*mm))
    story.append(P("<b>Méthodologie :</b> GRADE®, tags « GRADE 1+/1-/2+/2-, accord FORT » et « Avis "
                    "d'experts, accord FORT » imprimés littéralement après chaque recommandation "
                    "dans le texte source — cités ici tels quels.", S_SOURCE))
    story.append(Spacer(1, 1.5*mm))
    story.append(P("<b>Couverture :</b> 9 recommandations (R1.1 à R3.2, dont 1 avis d'experts) et "
                    "2 questions « absence de recommandation » reproduites intégralement, ainsi que "
                    "le Tableau 1 (composition des solutés — image source sans texte extractible, "
                    "vérifiée visuellement et retranscrite intégralement). Le résumé officiel "
                    "mentionne « trois protocoles de prise en charge » qui ne figurent, ni en texte "
                    "ni en figure, dans le document source (texte court) : ils ne sont donc pas "
                    "reproduits ici — se référer au texte long / aux annexes de la RFE.", S_SOURCE))
    story.append(Spacer(1, 3*mm))
    story.append(info_panel(P(
        "<b>Avertissement :</b> ce document est une fiche de synthèse indépendante, produite pour un "
        "usage d'aide-mémoire. Il reprend l'intégralité des recommandations de la RFE mais ne "
        "remplace pas le texte intégral et n'est ni édité ni validé par la SFAR/SFMU. En cas de "
        "doute, se référer au texte intégral, aux recommandations ultérieures et/ou à un avis "
        "spécialisé.",
        S_BODY_SM), bg=GREY_LIGHT, border=GREY))
    return story

SECTIONS = [
    ("Introduction, méthodologie & Tableau 1", _section_intro),
    ("Champ 1 — Sepsis / choc septique", _section_champ1),
    ("Champ 2 — Choc hémorragique", _section_champ2),
    ("Champs 3-4 — Cérébrolésés & péripartum", _section_champ3_4),
    ("Synthèse, sources & traçabilité", _section_synthese),
]

def _make_doc():
    return SimpleDocTemplate(OUT, pagesize=A4,
                              leftMargin=MARGIN, rightMargin=MARGIN,
                              topMargin=32*mm, bottomMargin=16*mm,
                              title="Fiche SFAR-SFMU 2021 - Choix du solute pour le remplissage vasculaire",
                              author="Synthèse indépendante (source SFAR/SFMU)")

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
