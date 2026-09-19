# -*- coding: utf-8 -*-
"""
Fiche de synthese - SFAR / Adarpef / Carorl, Conference d'experts, texte
court, 2005. "Anesthesie pour amygdalectomie chez l'enfant". 8 pages,
telecharge depuis sfar.org
(wp-content/uploads/2015/10/2a_SFAR_TEXTE-COURT_Anesthesie-pour-amygdalectomie-
chez-lenfant.pdf).

METHODOLOGIE : ce document combine DEUX systemes de cotation distincts (9e
convention methodologique rencontree dans ce corpus) :
  (1) Niveaux de preuve en medecine factuelle (Tableau 1, I a V) donnant lieu
      a une FORCE de recommandation Grade A/B/C/D/E (Tableau 2) - utilise
      pour les propositions reposant sur des donnees de la litterature ;
  (2) Cotation RAND/UCLA modifiee (1 a 9, 3 zones : desaccord [1-3] /
      indecision [4-6] / accord [7-9]) donnant "Accord fort" ou "Accord
      faible" - utilise pour les propositions necessitant une validation par
      les experts en l'absence de preuve suffisante.
Chaque proposition du texte source porte l'UN OU L'AUTRE de ces deux tags,
jamais les deux a la fois - reproduit tel quel ici (chip "A"/"B"/"C" pour le
1er systeme, chip "Fort"/"Faible" pour le 2e). SEULS les grades A, B et C
apparaissent effectivement dans le texte (aucune proposition D ou E) -
verifie par grep sur le texte source aplati.

COUVERTURE : integrale des 5 questions / 12 sous-questions du texte court.
Aucun contenu omis.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from style import *
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.units import mm

GRADE_COLORS["Fort"] = (GREEN, WHITE)
GRADE_COLORS["Faible"] = (AMBER, WHITE)
GRADE_COLORS["A"] = (GREEN, WHITE)
GRADE_COLORS["B"] = (TEAL, WHITE)
GRADE_COLORS["C"] = (AMBER, WHITE)

OUT = "/home/user/rfe-sfar-website/output/Fiche_SFAR_Amygdalectomie_Enfant_2005.pdf"

SOURCE_TXT = ("Source : « Anesthésie pour amygdalectomie chez l'enfant » — Conférence "
              "d'experts, texte court, SFAR / Adarpef / Carorl, 2005. Fiche de synthèse "
              "non officielle : se référer au texte intégral.")

def P(txt, style=S_CELL):
    return Paragraph(txt, style)

def chip(label, **kw):
    return grade_chip(label, **kw)

CW_FULL = PAGE_W - 2 * MARGIN

def reco_table(rows, col_widths):
    """rows: (text, grade_label) - pas de numerotation dans ce document."""
    data = [[P("Proposition", S_HEAD_W), P("Cotation", S_HEAD_W_C)]]
    for txt, grade in rows:
        data.append([P(txt, S_CELL), chip(grade)])
    t = Table(data, colWidths=col_widths, repeatRows=1)
    style_cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), NAVY), ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTNAME", (0, 0), (-1, 0), FONT_BOLD), ("FONTSIZE", (0, 0), (-1, 0), 8),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("ALIGN", (1, 0), (1, -1), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 0.5, GREY_LIGHT),
        ("TOPPADDING", (0, 0), (-1, -1), 3.4), ("BOTTOMPADDING", (0, 0), (-1, -1), 3.4),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            style_cmds.append(("BACKGROUND", (0, i), (-1, i), BG_PANEL))
    t.setStyle(TableStyle(style_cmds))
    return t

RCW = [CW_FULL - 20 * mm, 20 * mm]

def bullets(items, style=S_BODY_SM):
    html = "&bull; " + "<br/>&bull; ".join(items)
    return P(html, style)

def legend_flowable():
    chip_w = 15 * mm
    content_w = CW_FULL
    row1_w = content_w - 3 * chip_w
    row = Table([[chip("A", width=chip_w - 2 * mm), chip("B", width=chip_w - 2 * mm),
                  chip("C", width=chip_w - 2 * mm),
                  P("<b>Niveaux de preuve (Grade A/B/C)</b> — fondés sur la littérature "
                    "(A : ≥2 études de niveau I ; B : 1 étude de niveau I ; C : étude(s) "
                    "de niveau II). Aucune proposition D ou E dans ce texte.", S_BADGE_HEAD)]],
                colWidths=[chip_w, chip_w, chip_w, row1_w])
    row2 = Table([[chip("Fort", width=chip_w - 2 * mm), chip("Faible", width=chip_w - 2 * mm),
                   P("<b>Accord RAND/UCLA modifié (1-9)</b> — cotation individuelle des "
                     "experts en l'absence de preuve suffisante : « Accord fort » "
                     "(intervalle borné dans une seule zone) ou « Accord faible » "
                     "(intervalle empiétant sur une borne).", S_BADGE_HEAD)]],
                 colWidths=[chip_w, chip_w, content_w - 2 * chip_w])
    tbl = Table([[row], [Spacer(1, 1.5 * mm)], [row2]], colWidths=[content_w])
    tbl.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"),
                              ("LEFTPADDING", (0, 0), (-1, -1), 0),
                              ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                              ("TOPPADDING", (0, 0), (-1, -1), 0),
                              ("BOTTOMPADDING", (0, 0), (-1, -1), 0)]))
    for r in (row, row2):
        r.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                                ("LEFTPADDING", (0, 0), (-1, -1), 1),
                                ("RIGHTPADDING", (0, 0), (-1, -1), 1)]))
    return tbl

TOTAL_PAGES = {"n": 6}

def on_page(canvas, doc, page_title):
    header_band(canvas, doc, "SFAR / ADARPEF / CARORL — CONFÉRENCE D'EXPERTS 2005",
                "Anesthésie pour amygdalectomie chez l'enfant",
                page_title, icon_fn=lambda c, x, y: icon_shield(c, x, y, 13 * mm), color=NAVY)
    footer_band(canvas, doc, SOURCE_TXT, f"Page {doc.page} / {TOTAL_PAGES['n']}")

# ---------------------------------------------------------------------------
def _section_intro():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Champ :</b> prise en charge anesthésique péri-opératoire de l'enfant opéré "
        "pour amygdalectomie (avec ou sans adénoïdectomie). En France, l'anesthésie ORL "
        "représente 12 % des actes (3e rang après orthopédie et chirurgie digestive) ; "
        "sur ~670 000 anesthésies ORL annuelles, 17 % le sont pour amygdalectomie. "
        "L'anesthésie ORL représente 25 % des actes chez les moins de 1 an, 64 % chez "
        "les 1-4 ans, 28 % chez les 5-14 ans. Malgré les progrès, il persiste une "
        "morbi-mortalité non négligeable.", S_BODY), bg=BG_PANEL, border=TEAL))
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Méthodologie :</b> ce document combine <b>deux systèmes de cotation</b> — "
        "des propositions fondées sur la littérature (Grade A/B/C selon le niveau de "
        "preuve) et des propositions validées par cotation RAND/UCLA modifiée des "
        "experts en l'absence de preuve suffisante (« Accord fort » ou « Accord "
        "faible »). Chaque proposition du texte source porte l'un ou l'autre de ces deux "
        "tags, jamais les deux à la fois — reproduit tel quel, sans fusionner les deux "
        "échelles.", S_BODY_SM), bg=AMBER_LIGHT, border=AMBER))
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("Légende des cotations"))
    story.append(Spacer(1, 2 * mm))
    story.append(legend_flowable())
    return story

def _section_q1():
    story = []
    story.append(Spacer(1, 2 * mm))
    story.append(KeepTogether([
        section_bar("Question 1 — Évaluation préopératoire et préparation à la chirurgie"),
        Spacer(1, 1.5 * mm),
        P("<b>1.1 — Objectifs et modalités de la consultation d'anesthésie, information "
          "sur le risque</b>", S_CELL_B),
        Spacer(1, 1.5 * mm),
        reco_table([
            ("La consultation d'anesthésie en prévision d'une amygdalectomie a deux buts "
             "essentiels : l'évaluation des risques inhérents à l'acte et l'information "
             "du patient et de ses parents.", "Fort"),
            ("L'évaluation des risques repose sur l'interrogatoire des parents et si "
             "possible de l'enfant, ainsi que sur l'examen clinique de l'enfant.", "Fort"),
            ("Les risques respiratoires et hémorragiques doivent faire l'objet d'une "
             "attention et d'une information particulières.", "Fort"),
            ("Le risque respiratoire est majoré en cas de syndrome d'apnée obstructive "
             "du sommeil (SAOS) grave.", "Fort"),
            ("L'information s'adresse à la fois à l'enfant et aux parents, et doit être "
             "adaptée au degré de compréhension de chacun.", "Fort"),
        ], RCW),
    ]))
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        P("<b>1.2 — Bilan préopératoire</b>", S_CELL_B),
        Spacer(1, 1.5 * mm),
        reco_table([
            ("L'évaluation préopératoire du risque hémorragique repose sur un "
             "interrogatoire précis à la recherche d'antécédents personnels et/ou "
             "familiaux suggérant une anomalie de l'hémostase, et sur un examen "
             "clinique recherchant une symptomatologie hémorragique.", "Fort"),
            ("En cas d'antécédents personnels ou familiaux d'hémorragie connus ou "
             "suspectés, ou lorsque l'évaluation préopératoire ne peut être considérée "
             "comme fiable (notamment chez l'enfant de moins de 3 ans), une étude de "
             "l'hémostase doit être réalisée.", "Fort"),
            ("Les résultats de cette étude initiale, s'ils restent anormaux après "
             "contrôle, doivent être discutés avec un spécialiste de l'hémostase afin "
             "de déterminer l'opportunité d'une étude plus approfondie.", "Fort"),
            ("Si des examens d'hémostase sont prescrits, le temps de céphaline avec "
             "activateur et la numération plaquettaire sont les tests les plus "
             "utiles.", "Fort"),
            ("Chez l'enfant de plus de 3 ans, lorsque l'évaluation clinique "
             "préopératoire ne dépiste pas de risque hémorragique anormal, l'étude "
             "systématique de l'hémostase ne s'impose pas.", "Fort"),
        ], RCW),
    ]))
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        P("<b>1.3 — Gestion d'une infection des voies aériennes supérieures (IVAS) "
          "avant amygdalectomie</b>", S_CELL_B),
        Spacer(1, 1.5 * mm),
        reco_table([
            ("L'amygdalectomie majore le risque de complications respiratoires du fait "
             "de la localisation du site chirurgical sur les voies aériennes "
             "supérieures.", "A"),
            ("Ces complications respiratoires contribuent à générer une morbidité "
             "dénuée de réelle gravité si l'anesthésiste est expérimenté dans ce "
             "contexte.", "B"),
            ("L'IVAS entraîne une fréquence accrue de complications respiratoires "
             "telles que désaturation et pause respiratoire.", "A"),
            ("L'IVAS entraîne une augmentation de la fréquence des bronchospasmes "
             "lorsque l'enfant est intubé.", "A"),
        ], RCW),
    ]))
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        P("<b>1.4 — Critères de report d'intervention en cas d'IVAS</b>", S_CELL_B),
        Spacer(1, 1.5 * mm),
        P("L'intervention est différée si l'enfant présente <i>[Accord fort]</i> :",
          S_BODY_SM),
        Spacer(1, 1 * mm),
        bullets([
            "des signes spastiques bronchiques ;",
            "une laryngite ;",
            "une température supérieure à 38 °C.",
        ]),
        Spacer(1, 1.5 * mm),
        reco_table([
            ("En cas de report d'intervention, le délai de re-programmation est d'au "
             "moins trois semaines.", "Fort"),
        ], RCW),
    ]))
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        P("<b>1.5 — Conséquences du syndrome d'apnée du sommeil (SAOS) sur la prise en "
          "charge anesthésique</b>", S_CELL_B),
        Spacer(1, 1.5 * mm),
        reco_table([
            ("Le SAOS représente environ deux tiers des indications d'amygdalectomie.",
             "Fort"),
            ("Les enfants concernés ont le plus souvent moins de 5 ans.", "Fort"),
            ("En l'absence de critères de gravité, le SAOS ne modifie habituellement "
             "pas la prise en charge anesthésique.", "Fort"),
            ("Les formes graves de SAOS sont plus fréquentes chez le jeune enfant et en "
             "cas de dysmorphie faciale ou de pathologies associées.", "Fort"),
            ("Les formes graves de SAOS nécessitent une évaluation préopératoire du "
             "retentissement cardio-pulmonaire, et justifient une surveillance "
             "postopératoire d'au moins 24 heures dans une structure de type SSPI ou "
             "surveillance continue.", "Fort"),
        ], RCW),
    ]))
    return story

def _section_q2():
    story = []
    story.append(Spacer(1, 2 * mm))
    story.append(KeepTogether([
        section_bar("Question 2 — Prise en charge anesthésique des enfants programmés"),
        Spacer(1, 1.5 * mm),
        P("<b>2.1 — Prise en charge anesthésique des patients</b>", S_CELL_B),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("Les règles de jeûne habituelles, adaptées à l'âge de l'enfant, doivent être "
         "appliquées.", "C"),
        ("En dehors des syndromes obstructifs graves, une prémédication anxiolytique "
         "est utile.", "C"),
        ("Les structures de prise en charge et le matériel utilisé doivent être "
         "conformes aux recommandations de la Sfar et de l'Adarpef.", "Fort"),
        ("La surveillance peropératoire repose sur un monitorage conforme aux "
         "recommandations de la Sfar.", "Fort"),
        ("L'anesthésie générale lors de l'amygdalectomie a pour but d'assurer une "
         "composante hypnotique suffisante pour éviter la mémorisation peropératoire, "
         "et une composante analgésique efficace.", "Fort"),
        ("L'induction par inhalation est la modalité la plus fréquente.", "Fort"),
        ("L'induction intraveineuse est parfois préférée chez les grands enfants ou en "
         "cas de syndrome obstructif sévère.", "Fort"),
        ("L'entretien de l'anesthésie est souvent assuré par un agent halogéné associé "
         "à un morphinique.", "Fort"),
        ("Les apports hydroélectrolytiques peropératoires reposent sur l'utilisation "
         "d'un soluté isotonique en sel, pouvant contenir une faible concentration de "
         "glucose et perfusé à un débit adapté à l'âge de l'enfant.", "Fort"),
        ("Débit de perfusion — règle des 4-2-1 : 4 mL/kg/h pour les 10 premiers kg, "
         "+ 2 mL/kg/h pour les 10 kg suivants, + 1 mL/kg/h pour les 10 kg suivants "
         "(soit 65 mL/h pour un enfant de 25 kg par exemple).", "Fort"),
        ("Il est recommandé d'utiliser un dispositif médical de contrôle du débit de "
         "perfusion.", "Fort"),
        ("L'administration peropératoire de dexaméthasone est recommandée car elle "
         "réduit l'incidence des NVPO et le délai avant la reprise alimentaire.", "B"),
        ("L'administration d'une antibioprophylaxie peropératoire n'a pas démontré son "
         "intérêt, et ne s'impose donc pas systématiquement.", "Fort"),
    ], RCW))
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        P("<b>2.2 — Modalités de contrôle des voies aériennes</b>", S_CELL_B),
        Spacer(1, 1.5 * mm),
        reco_table([
            ("L'amygdalectomie chez l'enfant requiert une anesthésie générale balancée "
             "impliquant une protection des voies aériennes.", "Fort"),
            ("Le contrôle optimal des voies aériennes est assuré par une sonde "
             "d'intubation trachéale à ballonnet.", "Fort"),
            ("L'extubation est réalisée, en présence d'un médecin anesthésiste, au "
             "réveil complet de l'enfant, déterminé par l'ouverture des yeux à la "
             "demande.", "Fort"),
        ], RCW),
    ]))
    return story

def _section_q3():
    story = []
    story.append(Spacer(1, 2 * mm))
    story.append(KeepTogether([
        section_bar("Question 3 — Organisation des soins postopératoires"),
        Spacer(1, 1.5 * mm),
        P("<b>3.1 — Modalités de surveillance postopératoire</b>", S_CELL_B),
        Spacer(1, 1.5 * mm),
        reco_table([
            ("La surveillance en SSPI doit être systématique.", "Fort"),
            ("En plus de la surveillance habituelle, le dépistage et le traitement "
             "éventuel des complications respiratoires et hémorragiques est "
             "indispensable.", "Fort"),
            ("La surveillance en SSPI peut être prolongée chez les jeunes enfants "
             "opérés dans un contexte de SAOS grave.", "Fort"),
            ("La sortie de SSPI est autorisée après vérification des critères "
             "habituels (respiration, état hémodynamique, conscience, douleur, NVPO) "
             "et vérification de l'absence de saignement pharyngé par le chirurgien.",
             "Fort"),
        ], RCW),
    ]))
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        P("<b>3.2 — Perfusion postopératoire, reprise des boissons et de "
          "l'alimentation</b>", S_CELL_B),
        Spacer(1, 1.5 * mm),
        reco_table([
            ("Les apports hydroélectrolytiques postopératoires reposent sur un soluté "
             "isotonique en sel, pouvant contenir une faible concentration de "
             "glucose.", "Fort"),
            ("La perfusion est poursuivie jusqu'à la reprise efficace des boissons.",
             "Fort"),
            ("En raison du risque hémorragique, la reprise de l'alimentation "
             "s'effectue 6 heures après la fin de l'intervention ; la reprise des "
             "liquides clairs est possible dès la 2e heure.", "Fort"),
            ("Un régime alimentaire spécifique n'a pas fait la preuve de sa "
             "supériorité par rapport à une alimentation libre après "
             "amygdalectomie.", "C"),
        ], RCW),
    ]))
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        P("<b>3.3 — Modalités de l'analgésie postopératoire</b>", S_CELL_B),
        Spacer(1, 1.5 * mm),
        P("La douleur post-amygdalectomie est considérée comme une douleur forte à "
          "composante inflammatoire, durant en moyenne 8 jours (maximum les 3 premiers "
          "jours). <i>[Accord fort]</i>", S_BODY_SM),
        Spacer(1, 1.5 * mm),
        reco_table([
            ("L'évaluation et le traitement de la douleur doivent être systématiques, "
             "y compris à domicile.", "C"),
            ("L'utilisation du paracétamol doit être large, quasi-systématique ; les "
             "voies IV et orale sont les plus fiables.", "B"),
            ("Seule la morphine est efficace en monothérapie, administrée par voie IV "
             "en SSPI ; elle est considérée comme l'antalgique de référence. Les "
             "autres analgésiques doivent être utilisés en association et en tenant "
             "compte de leur délai d'action.", "C"),
            ("La posologie de la morphine doit être réduite en cas de SAOS grave.",
             "Fort"),
            ("Les antalgiques du palier II en association avec le paracétamol peuvent "
             "prendre le relais de la morphine IV. Leur administration par voie orale "
             "doit être débutée dès que possible.", "C"),
            ("Les AINS non sélectifs ne sont pas recommandés car ils peuvent "
             "s'associer à une augmentation de la fréquence des reprises "
             "chirurgicales pour saignement.", "Faible"),
        ], RCW),
    ]))
    return story

def _section_q4():
    story = []
    story.append(Spacer(1, 2 * mm))
    story.append(KeepTogether([
        section_bar("Question 4 — Complications postopératoires et prise en charge"),
        Spacer(1, 1.5 * mm),
        P("<b>4.1 — Principales complications postopératoires</b>", S_CELL_B),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("Les principales complications primaires (avant la 24e heure) sont : les "
         "complications respiratoires, l'hémorragie et les nausées et vomissements.",
         "B"),
        ("Les principaux facteurs de risque de complications respiratoires sont : la "
         "gravité du SAOS et l'importance de la désaturation artérielle "
         "préopératoire.", "C"),
        ("Chez les patients atteints de SAOS, 70 % des complications respiratoires "
         "majeures surviennent dans la première heure postopératoire, alors que les "
         "complications mineures surviennent habituellement avant la 6e heure.", "C"),
        ("L'hémorragie postopératoire survient chez 0,5 à 3 % des patients.", "B"),
        ("80 % des hémorragies primaires surviennent avant la 6e heure.", "B"),
        ("Environ 25 % des hémorragies postopératoires vont nécessiter une reprise "
         "chirurgicale.", "C"),
        ("Les patients nécessitant une reprise chirurgicale pour hémostase doivent "
         "être considérés comme ayant l'estomac plein et justifient une induction en "
         "séquence rapide.", "Fort"),
    ], RCW))
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        P("<b>4.2 — Nausées et vomissements postopératoires (NVPO)</b>", S_CELL_B),
        Spacer(1, 1.5 * mm),
        reco_table([
            ("Après amygdalectomie, on observe des nausées et vomissements chez 40 à "
             "70 % des patients.", "C"),
            ("L'utilisation peropératoire de protoxyde d'azote ne modifie pas "
             "l'incidence des NVPO.", "C"),
            ("Les NVPO sont moins fréquentes après injection peropératoire de "
             "propofol.", "C"),
            ("L'administration prophylactique IV de sétron réduit significativement "
             "l'incidence des NVPO après amygdalectomie chez l'enfant.", "C"),
            ("La dexaméthasone réduit significativement l'incidence des NVPO, et "
             "potentialise l'efficacité des sétrons.", "C"),
            ("Des protocoles de prise en charge des NVPO doivent être prévus et "
             "accessibles en SSPI.", "Fort"),
        ], RCW),
    ]))
    return story

def _section_q5():
    story = []
    story.append(Spacer(1, 2 * mm))
    story.append(KeepTogether([
        section_bar("Question 5 — Conditions requises pour l'amygdalectomie en ambulatoire"),
        Spacer(1, 1.5 * mm),
        P("La réalisation de l'amygdalectomie en ambulatoire est possible si "
          "<i>[Accord fort]</i> :", S_BODY_SM),
        Spacer(1, 1 * mm),
        bullets([
            "l'enfant est âgé de plus de 3 ans ;",
            "il n'existe pas de comorbidité majorant notamment le risque "
            "respiratoire ;",
            "il n'existe pas d'anomalie de l'hémostase ;",
            "il n'existe pas de syndrome d'apnée du sommeil grave ;",
            "les critères habituels de proximité et d'entourage familial sont "
            "satisfaits ;",
            "et sous réserve d'un consensus entre le chirurgien, l'anesthésiste et "
            "les parents.",
        ]),
    ]))
    story.append(Spacer(1, 2 * mm))
    story.append(reco_table([
        ("L'intervention doit être réalisée le plus tôt possible dans la matinée afin "
         "de permettre la sortie après une surveillance postopératoire de 6 heures.",
         "Fort"),
        ("La gestion anesthésique doit privilégier la prévention des NVPO, et "
         "l'anticipation peropératoire de l'analgésie postopératoire.", "Fort"),
        ("Le relais antalgique oral devrait être débuté avant la sortie du patient.",
         "Fort"),
        ("Il est recommandé de remettre aux parents un document avec les coordonnées "
         "de la personne à contacter en cas de difficultés, ainsi que l'ordonnance "
         "d'antalgiques de sortie.", "Fort"),
    ], RCW))
    story.append(Spacer(1, 2 * mm))
    story.append(P(
        "La sortie de l'enfant est autorisée après la 6e heure postopératoire, si les "
        "critères suivants sont réunis <i>[Accord fort]</i> :", S_BODY_SM))
    story.append(Spacer(1, 1 * mm))
    story.append(bullets([
        "absence de saignement au niveau des loges amygdaliennes, confirmée par le "
        "chirurgien ;",
        "absence de douleur ;",
        "absence de NVPO ;",
        "accord signé du chirurgien et de l'anesthésiste.",
    ]))
    story.append(Spacer(1, 2 * mm))
    story.append(reco_table([
        ("Un suivi téléphonique du patient à domicile à la 24e heure est souhaitable, "
         "car il améliore la qualité de la prise en charge.", "Fort"),
    ], RCW))
    story.append(Spacer(1, 4 * mm))
    story.extend(_section_sources())
    return story

def _section_sources():
    story = []
    story.append(section_bar("Sources et traçabilité", color=GREY))
    story.append(Spacer(1, 2 * mm))
    story.append(P(
        "<b>Document source :</b> « Anesthésie pour amygdalectomie chez l'enfant » — "
        "Conférence d'experts, texte court. Société française d'anesthésie et de "
        "réanimation (SFAR), Association des anesthésistes réanimateurs pédiatriques "
        "d'expression française (Adarpef), Club de l'anesthésie réanimation en ORL "
        "(Carorl). Secrétaire : Pr I. Constant ; Président : Pr G. Orliaguet.",
        S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P("<b>Version :</b> 2005 (dépôt légal novembre 2006).", S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P("<b>Méthodologie :</b> Conférence d'experts — deux systèmes de "
                    "cotation combinés : niveaux de preuve (Grade A/B/C selon la "
                    "littérature) et cotation RAND/UCLA modifiée (« Accord fort/"
                    "faible ») pour les propositions sans preuve suffisante — voir "
                    "disclosure méthodologique en page 1.", S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>URL source :</b> https://sfar.org/wp-content/uploads/2015/10/"
        "2a_SFAR_TEXTE-COURT_Anesthesie-pour-amygdalectomie-chez-lenfant.pdf",
        S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P("<b>Couverture :</b> cette fiche reprend l'intégralité des 5 "
                    "questions / 12 sous-questions du texte court (évaluation "
                    "préopératoire, prise en charge anesthésique, soins "
                    "postopératoires, complications, ambulatoire).", S_SOURCE))
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Avertissement — document de 2005 :</b> ce document est une fiche de "
        "synthèse indépendante, produite pour un usage d'aide-mémoire. Elle reprend "
        "l'intégralité des propositions du texte source, mais ne remplace pas le texte "
        "intégral (argumentaire complet, références bibliographiques) et n'est ni "
        "éditée ni validée par la SFAR, l'Adarpef ou le Carorl. Les pratiques ayant pu "
        "évoluer depuis 2005, se référer en cas de doute au texte intégral, aux "
        "recommandations plus récentes le cas échéant, et/ou à un avis spécialisé.",
        S_BODY_SM), bg=GREY_LIGHT, border=GREY))
    return story

def _section_intro_q1():
    # Merged onto one page-group: intro/legend alone left most of page 1
    # white, which pushed Q1's tail (1.5) onto an almost-empty page 3 -
    # combined per the <60%-full merge rule (CLAUDE.md build pipeline, step 7).
    story = _section_intro()
    story.append(Spacer(1, 3 * mm))
    story.extend(_section_q1())
    return story

SECTIONS = [
    ("Méthodologie, légende & Q1 — Évaluation préopératoire", _section_intro_q1),
    ("Q2 — Prise en charge anesthésique", _section_q2),
    ("Q3 — Soins postopératoires", _section_q3),
    ("Q4 — Complications postopératoires", _section_q4),
    ("Q5 — Ambulatoire & sources", _section_q5),
]

def _make_doc(path=None):
    return SimpleDocTemplate(path or OUT, pagesize=A4,
                              leftMargin=MARGIN, rightMargin=MARGIN,
                              topMargin=32 * mm, bottomMargin=16 * mm,
                              title="Fiche SFAR/Adarpef/Carorl 2005 - Amygdalectomie chez l'enfant",
                              author="Synthèse indépendante (source SFAR/Adarpef/Carorl)")

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
    # NOTE: pypdf/cryptography is broken in this container (pyo3 panic on
    # import) - use PyMuPDF (fitz) instead, per fiche_ponction_lombaire.py.
    import fitz, tempfile
    tmp_path = tempfile.mktemp(suffix=".pdf")
    doc = _make_doc(tmp_path)
    doc.build(story_flowables, onFirstPage=_silent_page, onLaterPages=_silent_page)
    n = fitz.open(tmp_path).page_count
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
