# -*- coding: utf-8 -*-
"""
Fiche de synthese - RFE commune SFAR / SOFCOT / SFGG / SFPC, 2017 (publiee 2019)
"Recommandation sur l'anesthesie du sujet age : l'exemple de fracture de l'extremite
superieure du femur (FESF)". F. Aubrun et al., Anesth Reanim. 2019;5:122-138,
doi 10.1016/j.anrea.2018.12.002. Texte valide par le CA de la SFAR le 29/06/2017.
Source telechargee : sfar.org/wp-content/uploads/2019/10/rfe-anesthesie-du-sujet-age.pdf
(17 pages, dont les pages 13-17 sont l'integralite des references [1]-[178] : aucun contenu
clinique/recommandation au-dela de R8.2, page 13).

CHAMP : la RFE ne se limite pas formellement a la FESF (elle vise la prise en charge
perioperatoire du "sujet age" en general, avec 3 profils distingues des l'introduction :
vigoureux/fragiles/dependants-polypathologiques), mais le groupe d'experts a choisi la FESF
comme "modele" pour rediger des recommandations concretes et gradees GRADE(R) - c'est
explicitement le titre du document lui-meme. Les 26 recommandations qui suivent portent donc
toutes, specifiquement, sur la FESF (texte le precise a chaque item : "chirurgie de la FESF",
"patients ages presentant une FESF", etc.) ; le contenu narratif plus general sur le sujet age
(profils de fragilite, evaluation cognitive/renale) est repris fidelement mais les 26
recommandations elles-memes sont toutes un enonce FESF-specifique.

METHODOLOGIE GRADE(R) a DEUX AXES INDEPENDANTS, imprimes cote a cote sur chaque tag - a ne
jamais fusionner en un chip invente (regle qualite #4) :
  (1) FORCE de la recommandation : GRADE 1+/1- (forte, "il faut faire / ne pas faire") ou
      GRADE 2+/2- (faible, "il faut probablement faire / ne pas faire") ; ou "AVIS D'EXPERTS"
      quand aucune meta-analyse ne permettait d'appliquer GRADE en totalite (revue
      systematique + vote >=70% requis).
  (2) ACCORD du vote d'experts (methode Delphi/GRADE Grid) : "(ACCORD FORT)" par defaut ;
      seuls 2 items sur 26 portent "(ACCORD FAIBLE)" - R1.4 et R5.1. Cette nuance d'accord
      est disclosee par un simple texte "(accord faible)" a la fin de la cellule concernee,
      jamais par un second chip (aucun autre chip "accord fort/faible" n'existe dans ce
      corpus a cote d'un chip GRADE numerique deja present).

BUG D'EXTRACTION PDF CORRIGE (verifie par rendu visuel a 200dpi, PAS une supposition) : le
texte brut extrait par PyMuPDF affiche "GRADE 2S (ACCORD FAIBLE)" (R5.1), "GRADE 1S (ACCORD
FORT)" (R6.1) et "GRADE 2S (ACCORD FORT)" (R8.1) - la lettre "S" est un artefact du sous-jeu
de police du PDF source qui mappe le glyphe tiret cadratin/moins "-" a "S" lors de
l'extraction texte. Confirme par rendu image (pages 8, 10 et 12 du PDF source a 200dpi) :
le texte imprime est bien "GRADE 2- (ACCORD FAIBLE)", "GRADE 1- (ACCORD FORT)" et
"GRADE 2- (ACCORD FORT)" respectivement - resolus ici en "2-"/"1-"/"2-", jamais laisses
tels quels ni devines sans verification visuelle.

INCOHERENCE SOURCE-INTERNE DISCLOSEE (verifiee par rendu visuel, page 7 du PDF source a
200dpi - PAS une erreur d'extraction cette fois) : R3.3 ("Pour l'anxiolyse, il ne faut
probablement pas utiliser d'agent medicamenteux") et R3.4 ("il ne faut probablement pas
administrer de l'hydroxyzine, de la gabapentine et de la pregabaline") sont toutes deux
formulees negativement mais imprimees "GRADE 2+ (ACCORD FORT)" - alors que la propre
Methodologie du document (page 3-4 source) definit "GRADE 2+" comme "il faut probablement
FAIRE" et "GRADE 2-" comme "il faut probablement NE PAS faire". Ces deux items violent donc
la convention +/- que le document enonce lui-meme. Le tag imprime fait foi (chippe "2+" tel
quel, comme pour toute incoherence de ce type deja rencontree dans ce corpus) ; l'incoherence
est disclosee dans le panneau de methodologie plutot que "corrigee" silencieusement en 2-.

COMPTAGE VERIFIE (par script, recompte exhaustif R1.1-R8.2 contre le texte source aplati) :
26 recommandations, exactement le chiffre annonce par le Resume de la source ("26
recommandations"). Grades : 8x GRADE 1 (7x 1+, 1x 1-), 14x GRADE 2 (12x 2+, 2x 2-), 4x AVIS
D'EXPERTS (R1.3, R2.2, R6.2, + R7.4 imprime "AVIS D'EXPERT" singulier dans la source - variante
orthographique sans consequence sur le sens, chippee "AE" comme les 3 autres). 8+14+4 = 26.

PERIMETRE EXCLU (disclosure) : le tableau I (delai d'intervention des FESF par etude,
8 references) est reproduit integralement. Les references bibliographiques [1]-[178] (pages
13-17 de la source) ne sont pas retranscrites (liste nominative sans contenu clinique
actionnable au-dela de ce que l'argumentaire cite deja).
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from style import *
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.units import mm

OUT = "/home/user/rfe-sfar-website/output/Fiche_SFAR_Anesthesie_Sujet_Age_ESF_2017.pdf"

SOURCE_TXT = ("Source : « Recommandation sur l'anesthésie du sujet âgé : l'exemple de "
              "fracture de l'extrémité supérieure du fémur » — SFAR/SOFCOT/SFGG/SFPC, RFE "
              "2017 (Anesth Reanim. 2019;5:122-138). Fiche de synthèse non officielle : se "
              "référer au texte intégral.")

def P(txt, style=S_CELL):
    return Paragraph(txt, style)

def chip(label, **kw):
    return grade_chip(label, **kw)

def reco_table(rows, col_widths):
    """rows: (ref, text, grade_label)"""
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
    items = [("1+", "Il faut faire"), ("1-", "Il ne faut pas faire"),
             ("2+", "Il faut probablement faire"), ("2-", "Il ne faut probablement pas faire"),
             ("AE", "Avis d'experts")]
    content_w = PAGE_W - 2*MARGIN
    n = len(items)
    chip_w = 13.5*mm
    text_w = (content_w - n*chip_w) / n
    row_cells, col_widths = [], []
    for g, txt in items:
        row_cells.append(chip(g, width=chip_w-1.5*mm))
        row_cells.append(P(txt, S_BADGE_HEAD))
        col_widths += [chip_w, text_w]
    row = Table([row_cells], colWidths=col_widths)
    row.setStyle(TableStyle([("VALIGN",(0,0),(-1,-1),"MIDDLE"), ("LEFTPADDING",(0,0),(-1,-1),1), ("RIGHTPADDING",(0,0),(-1,-1),1)]))
    return row

RCW = [15*mm, PAGE_W-2*MARGIN-15*mm-20*mm, 20*mm]

TOTAL_PAGES = {"n": 9}

def on_page(canvas, doc, page_title):
    header_band(canvas, doc, "SFAR / SOFCOT / SFGG / SFPC — RFE 2017 — FICHE DE SYNTHÈSE",
                "Anesthésie du sujet âgé — exemple de la FESF",
                page_title, icon_fn=lambda c, x, y: icon_shield(c, x, y, 13*mm), color=NAVY)
    footer_band(canvas, doc, SOURCE_TXT, f"Page {doc.page} / {TOTAL_PAGES['n']}")

# ---------------------------------------------------------------------------
def _section_intro():
    story = []
    story.append(Spacer(1, 3*mm))
    story.append(info_panel(P(
        "<b>Champ :</b> prise en charge périopératoire du patient âgé, en prenant pour "
        "<b>modèle</b> une des interventions les plus fréquentes chez le sujet âgé — la "
        "<b>fracture de l'extrémité supérieure du fémur (FESF)</b> — pour rédiger des "
        "recommandations concrètes et gradées. Plus de 65 000 FESF/an en France (jusqu'à "
        "150 000/an projetés en 2050) ; mortalité 3,9 % à l'hospitalisation, 24 % à 6 mois. "
        "3 profils de personnes âgées distingués par les experts, à âge identique : les "
        "« vigoureux/robustes » (vieillissement réussi, peu de comorbidités), les "
        "« fragiles » (réserves diminuées, haut risque en cas d'évènement intercurrent) et les "
        "« dépendants-polypathologiques » (l'essentiel de la population dite gériatrique). "
        "RFE commune SFAR, SOFCOT (orthogériatrie), SFGG et SFPC, 8 questions, "
        "<b>26 recommandations</b>.",
        S_BODY), bg=BG_PANEL, border=TEAL))
    story.append(Spacer(1, 3*mm))
    story.append(info_panel(P(
        "<b>Méthodologie GRADE® — deux axes indépendants, imprimés côte à côte :</b> "
        "(1) la <b>force</b> — qualité des preuves classée haute/modérée/basse/très basse, "
        "aboutissant à un énoncé toujours binaire positif/négatif et fort/faible : "
        "<b>1+/1-</b> (« il faut faire / ne pas faire ») ou <b>2+/2-</b> (« il faut "
        "probablement faire / ne pas faire ») ; ou un <b>avis d'experts</b> quand aucune "
        "méta-analyse ne permettait d'appliquer GRADE en totalité (revue systématique puis "
        "vote, validé si ≥ 70 % d'accord). (2) l'<b>accord</b> du vote d'experts (méthode "
        "Delphi/GRADE Grid) : « accord fort » par défaut (≥ 70 %) ; <b>seuls 2 items sur 26 "
        "portent la mention « accord faible »</b> (R1.4 et R5.1), signalée par un texte entre "
        "parenthèses plutôt que par un second chip inventé.<br/><br/>"
        "<b>Disclosure — bug d'extraction PDF corrigé :</b> le texte brut extrait du PDF "
        "source affiche « GRADE 2<i>S</i> » pour 3 recommandations (R5.1, R6.1, R8.1) — "
        "artefact de police du PDF qui substitue la lettre « S » au tiret « − ». Vérifié par "
        "rendu visuel à 200 dpi : le texte réellement imprimé est bien « GRADE 2− »/« GRADE "
        "1− », corrigé ici en conséquence, jamais laissé tel quel.<br/><br/>"
        "<b>Disclosure — incohérence interne au document source</b> (vérifiée par rendu "
        "visuel, non une erreur d'extraction) : R3.3 et R3.4 sont formulées négativement "
        "(« il ne faut probablement pas… ») mais imprimées « GRADE 2+ », alors que la "
        "Méthodologie du document définit elle-même 2+ = « il faut probablement faire » et "
        "2- = « il faut probablement ne pas faire ». Le tag imprimé fait foi (chippé « 2+ » "
        "tel quel) ; l'incohérence n'est pas corrigée silencieusement.",
        S_BODY_SM), bg=AMBER_LIGHT, border=AMBER))
    story.append(Spacer(1, 3*mm))
    story.append(section_bar("Légende des grades"))
    story.append(Spacer(1, 2*mm))
    story.append(legend_flowable())
    return story

def _section_q1():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(KeepTogether([
        section_bar("Question 1 — Prise en charge préopératoire des patients"),
        Spacer(1, 1.5*mm),
        P("<b>Risque cardiovasculaire, fonctions cognitives, fonction rénale</b>", S_CELL_B),
        Spacer(1, 1.5*mm),
        reco_table([
            ("R1.1", "Il faut réaliser un score de Lee classique pour évaluer le risque "
             "cardiovasculaire. Sa VPN reste &gt; 98 % quel que soit l'âge pour les patients "
             "peu à risque (RCRI = 1, 63 % des patients de plus de 85 ans dans une étude "
             "danoise de 257 342 patients) — pas d'examen complémentaire inutile chez eux ; sa "
             "VPP pour prédire une complication cardiaque postopératoire augmente avec l'âge "
             "(jusqu'à 6,5 % si &gt; 85 ans et RCRI &gt; 1).", "1+"),
            ("R1.2", "Pour un score de Lee de classe I, l'ECG est suffisant. Pour une classe "
             "&gt; I, chirurgie à risque majeur et capacité à l'effort difficilement "
             "évaluable par l'interrogatoire : il faut probablement affiner le risque "
             "postopératoire par le dosage de biomarqueurs et/ou un test cardiopulmonaire.", "2+"),
            ("R1.3", "Évaluer le risque de confusion ou de troubles cognitifs postopératoires "
             "en repérant en préopératoire une plainte cognitive, des troubles de l'humeur "
             "et/ou une maladie neurodégénérative (interrogatoire ciblé ; le 6-CIT, rapide "
             "[3 min], a une bonne sensibilité/spécificité comparé au MMSE [15 min]).", "AE"),
            ("R1.4", "Évaluer probablement la fonction rénale en préopératoire selon 2 "
             "situations : situation stable et chirurgie programmée (RFE 2012 examens "
             "préinterventionnels) ; insuffisance rénale aiguë (RFE 2015 IRA périopératoire). "
             "Interrompre les antihypertenseurs au long cours 48-72 h autour de la chirurgie "
             "pour éviter une hypovolémie source d'IRA iatrogène. <i>(accord faible)</i>", "2+"),
        ], RCW),
    ]))
    return story

def _section_q2():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(KeepTogether([
        section_bar("Question 2 — Programme spécifique & chirurgie ambulatoire"),
        Spacer(1, 1.5*mm),
        reco_table([
            ("R2.1", "Prise en charge multidisciplinaire spécialisée périopératoire associant "
             "urgentistes, anesthésistes-réanimateurs, chirurgiens, gériatres, pharmaciens et "
             "soignants, afin d'améliorer le devenir postopératoire des patients âgés opérés "
             "en chirurgie orthopédique — 46/58 (79 %) des études d'évaluation "
             "orthogériatrique rapportent un bénéfice ; plusieurs recommandations "
             "internationales (NICE, AAOS, AAGBI, New Zealand Guidelines, SIGN, Clinical "
             "Excellence Commission australienne) convergent vers ce modèle.", "1+"),
            ("R2.2", "Privilégier la chirurgie ambulatoire chez le patient âgé quel que soit "
             "son âge — semble ne pas augmenter, voire diminuer, les complications "
             "postopératoires (dysfonction cognitive, morbidité cardiorespiratoire), à "
             "condition d'optimiser la période peropératoire (hémodynamique, respiratoire, "
             "thermorégulation) ; surveillance postopératoire du globe vésical et de la "
             "douleur particulièrement importante.", "AE"),
        ], RCW),
    ]))
    return story

def _section_q3():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(KeepTogether([
        section_bar("Question 3 — Traitements confusiogènes & anxiété préopératoire"),
        Spacer(1, 1.5*mm),
        P("<b>Gestion des traitements pouvant engendrer une confusion postopératoire</b>", S_CELL_B),
        Spacer(1, 1.5*mm),
        reco_table([
            ("R3.1", "Identifier les médicaments à risque de confusion postopératoire "
             "(benzodiazépines à demi-vie longue, antidépresseurs tricycliques et IMAO B, "
             "antihistaminiques, neuroleptiques, morphiniques — mépéridine et tramadol "
             "notamment) et alléger les traitements anticholinergiques et sédatifs, si "
             "possible via une conciliation médicamenteuse. Ne pas prescrire <i>de novo</i> "
             "un de ces produits devant un trouble dysthymique/psycho-comportemental ; "
             "préférer alors une benzodiazépine à demi-vie courte ou un IRS/IRS-NA. Ne pas "
             "sevrer brutalement un traitement chronique.", "1+"),
        ], RCW),
    ]))
    story.append(Spacer(1, 3*mm))
    story.append(KeepTogether([
        P("<b>Évaluation et prise en charge de l'anxiété préopératoire</b>", S_CELL_B),
        Spacer(1, 1.5*mm),
        reco_table([
            ("R3.2", "Utiliser probablement une échelle objective et validée — Amsterdam "
             "Preoperative Anxiety and Information Scale (APAIS, 6 items) ou Hospital Anxiety "
             "and Depression Scale (HADS) — pour mesurer l'anxiété préopératoire : "
             "l'hétéro-évaluation par le soignant est peu efficiente (chirurgiens et "
             "anesthésistes surestiment notablement l'anxiété du patient).", "2+"),
            ("R3.3", "Pour l'anxiolyse, il ne faut probablement pas utiliser d'agent "
             "médicamenteux — nombreuses approches non pharmacologiques efficaces "
             "(information/éducation, hypnose, écoute musicale).", "2+"),
            ("R3.4", "Lorsqu'une prémédication pharmacologique est envisagée, il ne faut "
             "probablement pas administrer d'hydroxyzine (ANSM : risques anticholinergiques "
             "— confusion, tachycardie, hypotension, rétention urinaire), de gabapentine ni "
             "de prégabaline (données insuffisantes pour conclure).", "2+"),
            ("R3.5", "Si une prémédication médicamenteuse est requise, il faut probablement "
             "privilégier une benzodiazépine ou apparenté à demi-vie courte — l'âge "
             "&gt; 60 ans et/ou une prémédication majorent le risque de complications "
             "respiratoires postopératoires ; poursuivre un traitement chronique par "
             "benzodiazépine pour éviter un syndrome de sevrage.", "2+"),
        ], RCW),
    ]))
    return story

def _section_q4():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(KeepTogether([
        section_bar("Question 4 — Délai d'intervention de la FESF"),
        Spacer(1, 1.5*mm),
        reco_table([
            ("R4.1", "Réaliser la chirurgie d'une FESF dans les <b>48 heures</b> suivant "
             "l'admission du patient afin de réduire la mortalité postopératoire — une "
             "méta-analyse de 35 études (191 873 patients) montre qu'une chirurgie précoce "
             "réduit la mortalité (OR 0,74 [0,67 ; 0,81]) ; retarder la chirurgie reste "
             "prudent pour les patients ayant des situations pathologiques instables.", "1+"),
        ], RCW),
    ]))
    story.append(Spacer(1, 2.5*mm))
    story.append(KeepTogether([
        P("<b>TABLEAU I</b> — Délai d'intervention des FESF (proportion de patients opérés "
          "dans les 24 h, par étude)", S_H2),
        Spacer(1, 1*mm),
        simple_table(
            ["Référence", "Proportion opérée dans les 24 h"],
            [
                ["Siegmeth et al., 2005", "74 %"],
                ["Smektala et al., 2005", "64 %"],
                ["MacKenzie et al., 2006", "60 %"],
                ["Beringer et al., 1996", "57 %"],
                ["Bottle et al., 2006", "56 %"],
                ["Boddaert et al., 2014", "&gt; 50 %"],
                ["Charalambous et al., 2003", "44 %"],
                ["Parker et al., 1992", "34 %"],
            ], [(PAGE_W-2*MARGIN)*0.6, (PAGE_W-2*MARGIN)*0.4]),
    ]))
    return story

def _section_q5():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(KeepTogether([
        section_bar("Question 5 — Monitorage"),
        Spacer(1, 1.5*mm),
        P("<b>Hémodynamique, pression artérielle, oxygénation cérébrale</b>", S_CELL_B),
        Spacer(1, 1.5*mm),
        reco_table([
            ("R5.1", "Il ne faut probablement pas réaliser de monitorage systématique du "
             "débit cardiaque pour diriger le remplissage vasculaire peropératoire chez les "
             "patients âgés présentant une FESF — une méta-analyse Cochrane récente conclut à "
             "l'absence de preuve d'amélioration du devenir avec ces stratégies "
             "d'optimisation. Chez les patients à risque accru de complications de par leurs "
             "comorbidités, il reste recommandé de titrer le remplissage en se guidant sur le "
             "volume d'éjection systolique (RFE SFAR 2013). <i>(accord faible)</i>", "2-"),
        ], RCW),
    ]))
    story.append(Spacer(1, 2.5*mm))
    story.append(KeepTogether([
        reco_table([
            ("R5.2", "Maintenir probablement la pression artérielle moyenne peropératoire "
             "au-dessus d'un seuil correspondant à <b>70 % de la PAM de référence</b> "
             "mesurée avant l'intervention, d'autant plus que le patient présente des "
             "facteurs de risque de complications postopératoires — plus de 50 définitions "
             "de l'hypotension existent dans la littérature, sans seuil commun établi ; le "
             "seuil de PAM est préféré à la PAS (moins sujette aux distorsions de mesure).", "2+"),
            ("R5.3", "Traiter probablement sans délai toute hypotension peropératoire chez "
             "le sujet âgé afin de limiter le risque de complications rénales ou "
             "myocardiques.", "2+"),
            ("R5.4", "Il ne faut probablement pas utiliser en routine, chez le sujet âgé, un "
             "monitorage de l'oxygénation cérébrale (spectroscopie proche infrarouge, "
             "rSO<sub>2</sub>) "
             "pour des chirurgies ne présentant pas de risque neurologique spécifique — "
             "littérature de (très) faible qualité, essentiellement observationnelle, "
             "méthodologies hétérogènes.", "2+"),
        ], RCW),
    ]))
    story.append(Spacer(1, 2.5*mm))
    story.append(KeepTogether([
        P("<b>Température centrale</b>", S_CELL_B),
        Spacer(1, 1.5*mm),
        reco_table([
            ("R5.5", "Monitorer la température centrale de tout sujet âgé opéré afin de "
             "détecter et prévenir les conséquences de l'hypothermie — vasoconstriction et "
             "frissons moins efficaces avec le vieillissement, seuil vasoconstricteur abaissé "
             "d'environ 1 °C entre 60-80 ans vs 30-50 ans ; les recommandations générales sur "
             "l'hypothermie périopératoire de l'adulte s'appliquent tout particulièrement au "
             "sujet âgé.", "1+"),
        ], RCW),
    ]))
    return story

def _section_q6():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(KeepTogether([
        section_bar("Question 6 — Techniques et agents anesthésiques"),
        Spacer(1, 1.5*mm),
        reco_table([
            ("R6.1", "Il ne faut pas privilégier une technique d'anesthésie (AG vs ALR) pour "
             "diminuer la mortalité après chirurgie de la FESF — aucune étude prospective "
             "randomisée ne permet de trancher ; études rétrospectives contradictoires ; la "
             "mortalité postopératoire est probablement multifactorielle, l'anesthésie "
             "jouant un rôle à court terme mais pas à moyen/long terme.", "1-"),
            ("R6.2", "Lors d'une anesthésie générale, effectuer une titration avec des "
             "agents anesthésiques de courte durée d'action, à des doses adaptées à la "
             "pharmacologie du patient âgé et à un monitorage de la profondeur de "
             "l'anesthésie — pharmacocinétique/pharmacodynamique des hypnotiques et "
             "morphiniques modifiées par le vieillissement (pas les curares) ; induction "
             "progressive par titration (propofol ~1 mg/kg lentement, ou AIVOC modèle de "
             "Schnider) ; seul l'étomidate prévient avec certitude l'hypotension à "
             "l'induction ; rémifentanil particulièrement utile (clairance réduite, "
             "sensibilité aux morphiniques augmentée) ; sugammadex peut éviter "
             "l'anticholinergique après rocuronium ; protoxyde d'azote souvent mal toléré, à "
             "éviter.", "AE"),
            ("R6.3", "Réduire, ou titrer, les doses d'anesthésiques locaux lors d'une "
             "rachianesthésie pour réduire les hypotensions peropératoires — pharmacocinétique "
             "et pharmacodynamique des anesthésiques locaux modifiées par le vieillissement ; "
             "une rachianesthésie titrée (cathéter) réduit les épisodes hypotensifs versus "
             "une injection unique ; monitorer la profondeur de la sédation associée pour "
             "éviter une sédation trop profonde.", "1+"),
        ], RCW),
    ]))
    return story

def _section_q7():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(KeepTogether([
        section_bar("Question 7 — Décompensations cognitives postopératoires"),
        Spacer(1, 1.5*mm),
        P("<b>Syndrome confusionnel postopératoire :</b> trouble aigu de la vigilance, "
          "fréquent (incidence 26-52 % après prothèse totale de hanche), associé à une "
          "surmortalité, un risque de déclin cognitif/fonctionnel, un allongement de séjour "
          "et des coûts accrus. Facteurs prédisposants majeurs : altération des fonctions "
          "cognitives, déficience visuelle/auditive, déshydratation. Diagnostic : DSM-V ou "
          "Confusion Assessment Method (CAM) ; intensité évaluée par la Memorial Delirium "
          "Assessment Scale (MDAS).", S_BODY_SM),
        Spacer(1, 1.5*mm),
        reco_table([
            ("R7.1", "Mettre probablement en place un programme de prévention non "
             "médicamenteuse de la confusion postopératoire, favorisant la ré-afférentation "
             "sensorielle, l'orientation temporo-spatiale, le rythme veille-sommeil, et "
             "contrôlant hydratation, douleur et iatrogénie — le programme non "
             "pharmacologique « Elder Life Program » (ELP) diminue l'incidence (15,5 % vs "
             "9,9 %) et la durée du syndrome confusionnel en médecine ; une consultation "
             "gériatrique dans les 48 h préop ou 24 h postop réduit l'incidence (50 % vs "
             "32 %) et l'intensité des épisodes chez les patients de plus de 65 ans.", "1+"),
            ("R7.2", "En cas de confusion, identifier probablement les facteurs favorisants, "
             "rechercher et traiter une cause directe pour en limiter l'intensité et la "
             "durée — traitement associant prise en charge de la cause directe, mesures de "
             "prévention, et usage minimum de psychotropes sédatifs (uniquement en cas de "
             "trouble du comportement mettant en danger le patient et/ou son entourage).", "2+"),
            ("R7.3", "Administrer probablement une benzodiazépine à demi-vie courte ou un "
             "neuroleptique de dernière génération en cas d'anxiété majeure ou de trouble du "
             "comportement, pour limiter le danger induit pour le patient et/ou son "
             "entourage.", "2+"),
            ("R7.4", "N'utiliser la contention physique qu'en dernier recours et pour une "
             "durée la plus courte possible, réévaluée à court terme.", "AE"),
        ], RCW),
    ]))
    return story

def _section_q8():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(KeepTogether([
        section_bar("Question 8 — Analgésie postopératoire"),
        Spacer(1, 1.5*mm),
        P("Les recommandations SFAR 2016 sur la douleur postopératoire (déjà couvertes dans "
          "ce corpus) s'appliquent au sujet âgé ; ne sont repris ici que quelques points "
          "complémentaires propres au patient âgé avec FESF. Morphine : reste l'agent de "
          "choix, à condition d'un protocole personnalisé tenant compte de la fonction "
          "rénale (risque d'événement indésirable sévère avec une stratégie « aveugle », "
          "1511 patients, White et al.), au mieux via une PCA si le patient comprend son "
          "fonctionnement. Néfopam déconseillé chez le sujet âgé (effets anticholinergiques, "
          "ANSM). Paracétamol : dose maximale 3 g/j si poids &lt; 50 kg, 2 g/j si poids "
          "≤ 33 kg (ANSM).", S_BODY_SM),
        Spacer(1, 1.5*mm),
        reco_table([
            ("R8.1", "Il ne faut probablement pas infiltrer en intra-articulaire et/ou en "
             "sous-cutané avec des anesthésiques locaux en cas de chirurgie après fracture "
             "du col fémoral et/ou d'arthroplastie de hanche — analgésie obtenue inconstante, "
             "dépendante de la technique ; une méta-analyse (756 patients d'arthroplastie de "
             "hanche) ne montre pas d'effet analgésique en période postopératoire immédiate "
             "en cas de stratégie multimodale associée.", "2-"),
            ("R8.2", "Réaliser probablement un bloc fémoral ou iliofascial pour assurer "
             "l'analgésie en cas de FESF — une revue Cochrane (17 études, 888 patients) "
             "montre une diminution des scores de douleur et de la consommation "
             "d'antalgiques de secours, sans complication majeure ni surrisque d'événement "
             "indésirable ; le bénéfice est plus net lors de la mobilisation de la hanche "
             "qu'au repos, et le taux de confusion postopératoire est atténué chez les "
             "patients à risque moyen (pas chez les patients à risque élevé).", "2+"),
        ], RCW),
    ]))
    story.append(Spacer(1, 4*mm))
    story.extend(_section_sources())
    return story

def _section_sources():
    story = []
    story.append(section_bar("Sources et traçabilité", color=GREY))
    story.append(Spacer(1, 2*mm))
    story.append(P(
        "<b>Document source :</b> « Recommandation sur l'anesthésie du sujet âgé : l'exemple "
        "de fracture de l'extrémité supérieure du fémur » — RFE commune Société française "
        "d'anesthésie et de réanimation (SFAR), Société française de chirurgie orthopédique "
        "(SOFCOT/orthogériatrie), Société française de gériatrie et gérontologie (SFGG), "
        "Société française de pharmacie clinique (SFPC). Coordonnateur : Frédéric Aubrun. "
        "Anesth Reanim. 2019;5:122-138, doi 10.1016/j.anrea.2018.12.002. Texte validé par le "
        "Conseil d'administration de la SFAR le 29/06/2017.", S_SOURCE))
    story.append(Spacer(1, 1.5*mm))
    story.append(P("<b>Méthodologie :</b> GRADE® — force (1+/1-/2+/2- ou avis d'experts) et "
                    "accord du vote Delphi/GRADE Grid (fort ≥ 70 % par défaut ; faible pour "
                    "2 items sur 26, disclosés en texte) imprimés côte à côte sur chaque tag "
                    "— voir disclosure méthodologique en page 1 (bug d'extraction PDF corrigé "
                    "par vérification visuelle ; incohérence source-interne sur R3.3/R3.4 "
                    "signalée, non résolue silencieusement).", S_SOURCE))
    story.append(Spacer(1, 1.5*mm))
    story.append(P("<b>Couverture :</b> cette fiche reprend l'intégralité des 26 "
                    "recommandations (R1.1-R8.2) réparties sur les 8 questions du texte "
                    "(évaluation préopératoire, programme spécifique et chirurgie "
                    "ambulatoire, gestion des traitements confusiogènes et de l'anxiété, "
                    "délai d'intervention avec le Tableau I, monitorage, techniques et "
                    "agents anesthésiques, décompensations cognitives postopératoires, "
                    "analgésie postopératoire). Comité d'organisation, groupe de lecture et "
                    "les 178 références bibliographiques (pages 13-17 de la source) ne sont "
                    "pas retranscrits (sans contenu clinique actionnable au-delà de ce que "
                    "l'argumentaire cite déjà).", S_SOURCE))
    story.append(Spacer(1, 3*mm))
    story.append(info_panel(P(
        "<b>Avertissement — document de 2017/2019 :</b> ce document est une fiche de "
        "synthèse indépendante, produite pour un usage d'aide-mémoire. Elle reprend "
        "l'intégralité des 26 recommandations du texte source, mais ne remplace pas le texte "
        "intégral (argumentaire complet, 178 références bibliographiques) et n'est ni éditée "
        "ni validée par la SFAR, la SOFCOT, la SFGG ou la SFPC. Les recommandations "
        "elles-mêmes portent spécifiquement sur la fracture de l'extrémité supérieure du "
        "fémur (FESF), modèle choisi par les experts pour illustrer la prise en charge "
        "périopératoire du sujet âgé en général — se référer en complément aux "
        "recommandations SFAR sur la douleur postopératoire (2016), les examens "
        "préinterventionnels (2012) et l'insuffisance rénale aiguë périopératoire (2015), "
        "déjà couvertes dans ce corpus, et à un avis gériatrique/anesthésique spécialisé en "
        "cas de doute.",
        S_BODY_SM), bg=GREY_LIGHT, border=GREY))
    return story

def _section_q1_q2():
    return _section_q1() + [Spacer(1, 3*mm)] + _section_q2()

def _section_q4_q5():
    return _section_q4() + [Spacer(1, 3*mm)] + _section_q5()

def _section_q6_q7():
    return _section_q6() + [Spacer(1, 3*mm)] + _section_q7()

SECTIONS = [
    ("Introduction, méthodologie & légende", _section_intro),
    ("Q1-Q2 — Évaluation préopératoire & programme spécifique", _section_q1_q2),
    ("Q3 — Traitements confusiogènes & anxiété", _section_q3),
    ("Q4-Q5 — Délai d'intervention & monitorage", _section_q4_q5),
    ("Q6-Q7 — Techniques anesthésiques & confusion postopératoire", _section_q6_q7),
    ("Q8 — Analgésie postopératoire & sources", _section_q8),
]

def _make_doc(path=None):
    return SimpleDocTemplate(path or OUT, pagesize=A4,
                              leftMargin=MARGIN, rightMargin=MARGIN,
                              topMargin=32*mm, bottomMargin=16*mm,
                              title="Fiche SFAR/SOFCOT/SFGG/SFPC 2017 - Anesthesie du sujet age (FESF)",
                              author="Synthèse indépendante (source SFAR/SOFCOT/SFGG/SFPC)")

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
    # Throwaway temp path (never OUT) for measurement-only builds — see CLAUDE.md critical
    # bug note: reusing OUT here was found (in a prior fiche) to silently corrupt page 1's
    # header_band in the final build.
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
