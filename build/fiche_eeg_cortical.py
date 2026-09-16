# -*- coding: utf-8 -*-
"""
Fiche de synthese - RFE SFAR 2010 (texte court), "Monitorage de
l'adequation/profondeur de l'anesthesie a partir de l'analyse de l'EEG
cortical". SFAR, septembre 2009. 11 pages source, telecharge depuis
sfar.org (wp-content/uploads/2015/10/2_SFAR_Monitorage-de-ladequation-
profondeur-de-lanesthesie-a-partir-de-lanalyse-de-lEEG-cortical.pdf).

METHODOLOGIE : format Question/Reponse (pas de RPP/GRADE, pas de niveaux
de preuve I-V ni de grades A-E, pas de cotation Delphi) - chaque "Reponse"
est une synthese d'expert du groupe de travail SFAR, une seule mention
explicite "avis d'experts" dans tout le texte (Q2). Structure native en 2
modules : <b>Module A</b> (connaissances necessaires - Questions 1a a 1e)
que la source elle-meme dit explicitement NE PAS avoir ete concu pour
etre des recommandations ("Cette partie explicative n'a pas ete concue
pour faire l'objet des recommandations") - traite ici comme contexte/
connaissances de base, distinct des reponses cliniques du Module B
(benefice clinique - Questions 2 a 6). Aucun grade a fabriquer - meme
convention "sans cotation" que fiche_tests_viscoelastiques.py /
fiche_erreurs_medicamenteuses.py.

PORTEE : couverture complete des 6 questions du Module A (1a, 1b, 1b
complementaire, 1c, 1d, 1e) et des 5 questions du Module B (2 a 6), y
compris la figure dose-reponse des halogenes (BIS vs concentration
desflurane/isoflurane/sevoflurane) - source rendue en page a 220dpi et
transcrite VISUELLEMENT (regle 1), pas devinee : le croisement des 3
courbes vers 0,7 CAM et l'isoflurane finissant la plus basse (au lieu
d'etre uniformement intermediaire, comme une premiere lecture trop rapide
l'avait laisse croire avant re-verification sur le rendu haute resolution)
sont des details cliniquement reels de la courbe, pas une simplification -
et la liste complete (non exhaustive selon la source) des situations
cliniques du Module B question 5.

ARGUMENTAIRE : ce texte court de 2010 est deja tres condense nativement
(format Question/Reponse direct, pas de section "argumentaire" separee a
trimmer) - chaque "Reponse" EST le contenu actionnable, integralement
repris.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from style import *
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.units import mm

OUT = "/home/user/rfe-sfar-website/output/Fiche_SFAR_Monitorage_EEG_Cortical_2010.pdf"

SOURCE_TXT = ("Source : « Monitorage de l'adéquation/profondeur de l'anesthésie à partir de "
              "l'analyse de l'EEG cortical » — RFE SFAR, texte court, septembre 2009 (publié 2010). "
              "Fiche de synthèse non officielle : se référer au texte intégral.")

def P(txt, style=S_CELL):
    return Paragraph(txt, style)

CW_FULL = PAGE_W - 2 * MARGIN

def theme_table(rows, col_widths, head=("Question", "Réponse")):
    data = [[P(head[0], S_HEAD_W), P(head[1], S_HEAD_W)]]
    for theme, detail in rows:
        data.append([P(theme, S_CELL_B), P(detail, S_CELL)])
    t = Table(data, colWidths=col_widths, repeatRows=1)
    style_cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), TEAL_DARK), ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTNAME", (0, 0), (-1, 0), FONT_BOLD), ("FONTSIZE", (0, 0), (-1, 0), 8),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.5, GREY_LIGHT),
        ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            style_cmds.append(("BACKGROUND", (0, i), (-1, i), BG_PANEL))
    t.setStyle(TableStyle(style_cmds))
    return t

def grid_table(head_row, rows, col_widths, head_bg=NAVY):
    data = [[P(h, S_HEAD_W_C) for h in head_row]]
    for row in rows:
        data.append([P(c, S_CELL) for c in row])
    t = Table(data, colWidths=col_widths, repeatRows=1)
    style_cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), head_bg), ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTNAME", (0, 0), (-1, 0), FONT_BOLD), ("FONTSIZE", (0, 0), (-1, 0), 8),
        ("VALIGN", (0, 0), (-1, -1), "TOP"), ("ALIGN", (1, 1), (-1, -1), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 0.5, GREY_LIGHT),
        ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            style_cmds.append(("BACKGROUND", (0, i), (-1, i), BG_PANEL))
    t.setStyle(TableStyle(style_cmds))
    return t

def bullets(items, style=S_BODY_SM):
    return [P("• " + it, style) for it in items]

TOTAL_PAGES = {"n": 3}

def on_page(canvas, doc, page_title):
    header_band(canvas, doc, "SFAR — RFE, TEXTE COURT, 2010 (FORMAT QUESTION/RÉPONSE)",
                "Monitorage EEG cortical de l'anesthésie",
                page_title, icon_fn=lambda c, x, y: icon_pill(c, x, y, 13 * mm), color=TEAL_DARK)
    footer_band(canvas, doc, SOURCE_TXT, f"Page {doc.page} / {TOTAL_PAGES['n']}")

# ---------------------------------------------------------------------------
def _section_intro_module_a():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Résumé :</b> RFE SFAR (format Question/Réponse, sans grille de cotation) sur "
        "l'utilisation clinique des moniteurs de profondeur d'anesthésie basés sur l'analyse "
        "de l'EEG cortical (BIS®, Entropie® — les deux moniteurs commercialisés en France en "
        "2010). Structure en 2 modules : <b>Module A</b> — connaissances nécessaires "
        "(explicatif, non conçu comme des recommandations selon la source elle-même) ; "
        "<b>Module B</b> — bénéfice clinique et indications potentielles.", S_BODY),
        bg=BG_PANEL, border=TEAL))
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("Module A — Connaissances nécessaires (contexte, non des recommandations)"))
    story.append(Spacer(1, 1.5 * mm))
    story.append(theme_table([
        ("1a. L'EEG de surface est-il utilisable pour monitorer tous les effets de "
         "l'anesthésie ?", "Non — il explore surtout la composante hypnotique et "
         "l'éventuelle réaction d'éveil cortical à une stimulation nociceptive. Sa "
         "performance diagnostique/prédictive seul n'est pas suffisante pour toute la "
         "pharmacologie des anesthésiques."),
        ("1b. Principaux algorithmes des moniteurs commercialisés en France",
         "Deux moniteurs : BIS® (Aspect Medical) et Entropie® (GE Healthcare) — "
         "algorithmes partiellement ou totalement publiés par les fabricants. En "
         "connaître les principes aide à l'interprétation clinique (reconnaissance des "
         "artefacts). Au-delà de l'index, les moniteurs fournissent le tracé EEG brut "
         "et d'autres paramètres (rapport de suppression, composante EMG) qui "
         "améliorent le raisonnement médical."),
        ("1b (complémentaire). Les moniteurs sont-ils interchangeables ?",
         "<b>Non</b> — les différences d'algorithme entre moniteurs (et parfois entre "
         "versions d'un même moniteur) sont suffisamment importantes pour rendre "
         "difficile l'extrapolation des résultats publiés d'un moniteur à un autre."),
        ("1c. Les index sont-ils corrélés linéairement aux concentrations d'hypnotiques "
         "et aux signes cliniques, pour tous les hypnotiques ?",
         "Une corrélation existe (propofol, halogénés) mais <b>n'est pas linéaire</b> "
         "sur toute la plage de concentrations utilisées en anesthésie — variations "
         "faibles des index possibles pour des changements importants de "
         "concentration. Le burst suppression (EEG isoélectrique) signe une anesthésie "
         "très profonde, pris en compte différemment selon les algorithmes. La "
         "kétamine et le N2O ne modifient pas (ou très peu) les index malgré des "
         "signes cliniques de perte de conscience."),
        ("1d. Les morphiniques modifient-ils la relation "
         "concentration-hypnotique/index ?", "Peu, en l'absence de stimulation "
         "nociceptive, même à concentration élevée. Lors d'une stimulation "
         "nociceptive, un morphinique atténue la réaction d'éveil cortical "
         "(accélération EEG + augmentation de l'index) ; la présence de cette "
         "réaction lors d'une stimulation peut traduire une analgésie insuffisante "
         "pour le niveau hypnotique donné."),
        ("1e. Limites de l'EEG pour estimer les effets des agents anesthésiques",
         "Tout facteur physiopathologique modifiant l'EEG modifie les index : "
         "ischémie cérébrale, hypothermie, hypoglycémie (ralentissent) ; activité "
         "épileptoïde (accélère). Les artefacts élèvent artificiellement les index. "
         "Certains médicaments (bêta-bloquants, éphédrine, neuroleptiques) modifient "
         "la relation index/concentration. Les curares, en atténuant le signal EMG "
         "frontal, diminuent en général les valeurs des index."),
    ], [58 * mm, CW_FULL - 58 * mm]))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<i>Figure source (« Courbes doses réponse des halogénés ») — page rendue à "
        "220dpi et transcrite visuellement (règle 1) :</i> relation entre index "
        "bispectral (BIS) et concentration au site effet d'halogéné, en CAM (0 à 3), "
        "pour desflurane, isoflurane et sévoflurane. Les trois courbes partent de "
        "~100 à CAM=0. Le désflurane et le sévoflurane chutent tôt et rapidement, dès "
        "~0,3-0,4 CAM, jusqu'à ~50 vers 0,5-0,6 CAM ; l'isoflurane reste proche de 100 "
        "plus longtemps (jusqu'à ~0,5 CAM) puis chute brutalement, croisant les deux "
        "autres courbes vers 0,7 CAM (~42-45 pour les trois agents). Entre 0,7 et "
        "2 CAM, les trois courbes restent proches (BIS ~28-42) mais l'isoflurane "
        "devient progressivement la plus basse. Au-delà de 2 CAM, l'isoflurane "
        "décroît le plus nettement, jusqu'à un BIS ~12 au point le plus extrême de sa "
        "courbe (~2,8 CAM) — la plage de concentration testée la plus étendue des "
        "trois agents — tandis que le désflurane reste le plus élevé en fin de "
        "courbe (BIS ~28-30 vers 2,5 CAM). Le sévoflurane se situe entre les deux, "
        "sa courbe s'arrêtant vers 2,3 CAM (BIS ~15).", S_NOTE))
    story.append(Spacer(1, 1 * mm))
    story.append(grid_table(
        ["Concentration (CAM)", "0,5", "1,0", "1,5", "2,0", "Fin de courbe"],
        [
            ["Désflurane", "~50", "~42", "~40", "~38", "~28-30 (CAM ≈2,5)"],
            ["Isoflurane", "~95", "~42", "~38", "~33", "~12 (CAM ≈2,8)"],
            ["Sévoflurane", "~50", "~40", "~35", "~28", "~15 (CAM ≈2,3)"],
        ], [30 * mm, 17 * mm, 17 * mm, 17 * mm, 17 * mm, CW_FULL - 98 * mm], head_bg=GREY))
    story.append(Spacer(1, 1 * mm))
    story.append(P(
        "Valeurs lues visuellement sur le graphique source (celui-ci ne fournit pas de "
        "tableau numérique) — approximatives, à l'échelle du pixel près ; se référer au "
        "graphique source pour toute utilisation exigeant une précision fine.", S_NOTE))
    return story

def _section_module_b():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("Module B — Bénéfice clinique et indications"))
    story.append(Spacer(1, 1.5 * mm))
    story.append(theme_table([
        ("2. L'EEG apporte-t-il une information complémentaire aux signes cliniques et "
         "autres moyens paracliniques ?", "Les index estiment la variabilité "
         "inter-individuelle et intra-individuelle des besoins anesthésiques, "
         "complétant les concentrations prédites de propofol ou téléexpiratoires "
         "d'halogénés. Les moniteurs pourraient détecter un sous- ou surdosage "
         "anesthésique (<b>avis d'experts</b>), notamment quand les signes cliniques "
         "sont modifiés par les curares, les comorbidités ou une instabilité "
         "hémodynamique peropératoire."),
        ("3. Le monitorage change-t-il la conduite de l'anesthésie ?",
         "Diminution de 10 à 40 % des doses cumulées d'hypnotiques — mais pas dans "
         "toutes les études ni toutes les situations cliniques. Associée à une "
         "diminution statistiquement significative mais <b>cliniquement "
         "négligeable</b> des délais de réveil et des durées de séjour en SSPI."),
        ("4. Le monitorage diminue-t-il la morbidité de l'anesthésie ?",
         "Le BIS® peut dépister certains épisodes de mémorisation explicite "
         "(surtout populations à risque) mais <b>n'abolit pas</b> la mémorisation "
         "explicite. L'entropie est, comme le BIS®, corrélée à la perte de "
         "conscience mais présente le même chevauchement de valeurs entre états "
         "conscient et non-conscient. Le monitorage par BIS® peut diminuer "
         "l'incidence des NVPO sous halogénés <b>en l'absence</b> de prévention "
         "systématique des NVPO — sans effet supplémentaire si une prévention "
         "systématique est déjà en place. Influence sur la stabilité hémodynamique "
         "peropératoire faible et inconstante, sans corrélation démontrée avec des "
         "complications postopératoires. Le BIS® <b>ne détecte pas spécifiquement</b> "
         "les tracés épileptiformes observables à l'induction au sévoflurane. Aucune "
         "donnée ne permet à ce jour d'affirmer un bénéfice sur le devenir à long "
         "terme ou les complications tardives après anesthésie générale."),
    ], [58 * mm, CW_FULL - 58 * mm]))
    story.append(Spacer(1, 2 * mm))
    story.append(P(
        "<b>5. Quelles catégories de patients/situations cliniques peuvent représenter des "
        "indications (critères intermédiaires) au monitorage de profondeur d'anesthésie ?</b> "
        "— utile pour affiner le raisonnement médical, en particulier lorsque la relation "
        "dose-concentration-effets des anesthésiques est inhabituelle, facilitant la "
        "détection du sous- ou surdosage. Liste <b>non exhaustive</b> (source) :",
        S_BODY_SM))
    story.append(Spacer(1, 1 * mm))
    story.append(P("<i>Terrain / traitements modifiant la relation dose-effet :</i>", S_NOTE))
    for b in bullets([
        "Traitement chronique prolongé par antiépileptiques, morphiniques, "
        "benzodiazépines, ou toxicomanie à la cocaïne",
        "Consommation quotidienne d'alcool",
        "Utilisation préopératoire de bêta-bloquants",
        "FEVG &lt;30 % ou index cardiaque &lt;2 L/min/m²",
        "Antécédent de mémorisation explicite",
        "Antécédent d'intubation difficile ou intubation difficile prévue",
        "ASA 4/5",
        "Rétrécissement aortique sévère",
        "Maladies respiratoires graves",
        "Faible tolérance à l'effort",
        "Hypertension artérielle pulmonaire (HTAP)",
    ]):
        story.append(b)
    story.append(Spacer(1, 1.5 * mm))
    story.append(P("<i>Type de chirurgie / situation peropératoire :</i>", S_NOTE))
    for b in bullets([
        "Chirurgie cardiaque (avec ou sans CEC)",
        "Césarienne",
        "Patients polytraumatisés avec hypovolémie",
        "Insuffisance hépatique sévère",
        "Traitement par inhibiteurs des protéases",
        "Hypotension artérielle peropératoire nécessitant un traitement",
    ]):
        story.append(b)
    story.append(Spacer(1, 2 * mm))
    story.append(KeepTogether([
        section_bar("6. Particularités en pédiatrie"),
        Spacer(1, 1.5 * mm),
        P(
            "Les deux moniteurs commercialisés en France reposent sur des algorithmes "
            "validés chez l'adulte. Chez l'enfant de plus de 2 ans, leur utilisation "
            "présente actuellement les mêmes qualités et réserves que chez l'adulte — la "
            "concentration d'hypnotique nécessaire pour un effet EEG cortical donné (ou "
            "une valeur de BIS® donnée) semble toutefois plus importante que chez "
            "l'adulte.", S_BODY_SM),
    ]))
    story.append(Spacer(1, 1.5 * mm))
    story.append(theme_table([
        ("Enfant &gt;2 ans (AIVOC/TIVA)", "Compte tenu de la grande variabilité "
         "interindividuelle pharmacodynamique et pharmacocinétique chez l'enfant, "
         "l'utilisation du BIS® (moniteur le plus étudié) <b>peut être recommandée</b> "
         "dans le contexte d'une anesthésie intraveineuse à objectif de concentration "
         "(AIVOC)/totale intraveineuse (TIVA)."),
        ("Enfant &lt;2 ans (et surtout &lt;6 mois)", "<b>Aucune étude</b> ne permet "
         "actuellement de recommander l'utilisation du monitorage EEG cortical dans "
         "cette tranche d'âge — pourtant probablement la population la plus "
         "vulnérable face aux effets délétères potentiels des anesthésiques généraux "
         "et aux processus de mémorisation implicite."),
    ], [42 * mm, CW_FULL - 42 * mm]))
    return story

def _section_sources():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("Sources et traçabilité", color=GREY))
    story.append(Spacer(1, 2 * mm))
    story.append(P(
        "<b>Document source :</b> « Monitorage de l'adéquation/profondeur de l'anesthésie à "
        "partir de l'analyse de l'EEG cortical » — Recommandations Formalisées d'Experts, "
        "texte court, Société française d'anesthésie et de réanimation (SFAR), septembre "
        "2009 (publié 2010).", S_SOURCE))
    story.append(Spacer(1, 1 * mm))
    story.append(P(
        "<b>Méthodologie :</b> format Question/Réponse, sans grille de cotation (ni niveaux "
        "de preuve, ni grades) — voir détail en page 1.", S_SOURCE))
    story.append(Spacer(1, 1 * mm))
    story.append(P(
        "<b>URL source :</b> https://sfar.org/wp-content/uploads/2015/10/2_SFAR_Monitorage-"
        "de-ladequation-profondeur-de-lanesthesie-a-partir-de-lanalyse-de-lEEG-cortical.pdf",
        S_SOURCE))
    story.append(Spacer(1, 1 * mm))
    story.append(P(
        "<b>Couverture :</b> intégralité des 6 questions du Module A (connaissances, non "
        "recommandations selon la source) et des 5 questions du Module B (bénéfice "
        "clinique/indications), y compris la liste complète des situations cliniques de la "
        "question 5. Les valeurs de la figure dose-réponse des halogénés (question 1c) sont "
        "lues approximativement sur le graphique source, disclosed comme telles — la "
        "source ne fournit pas de tableau numérique pour cette figure.", S_SOURCE))
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Avertissement — document validé 2009/2010 :</b> cette fiche de synthèse "
        "indépendante reprend l'intégralité du contenu du texte source, mais ne le "
        "remplace pas et n'est ni éditée ni validée par la SFAR. Se référer au texte "
        "intégral pour toute décision clinique.", S_BODY_SM), bg=GREY_LIGHT, border=GREY))
    return story

SECTIONS = [
    ("Module A — connaissances nécessaires", _section_intro_module_a),
    ("Module B — bénéfice clinique, pédiatrie & sources",
     lambda: _section_module_b() + _section_sources()),
]

def _make_doc(path=None):
    return SimpleDocTemplate(path or OUT, pagesize=A4,
                              leftMargin=MARGIN, rightMargin=MARGIN,
                              topMargin=32 * mm, bottomMargin=16 * mm,
                              title="Fiche SFAR 2010 - Monitorage EEG cortical de l'anesthesie",
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

    doc = _make_doc()
    story = _build_upto(fns)
    doc.build(story, onFirstPage=on_page_final, onLaterPages=on_page_final)
    print("OK ->", OUT, f"({total_pages} pages)")

if __name__ == "__main__":
    build()
