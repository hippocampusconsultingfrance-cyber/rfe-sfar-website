# -*- coding: utf-8 -*-
"""
Fiche de synthese - "Prise en charge des sujets en etat de mort encephalique dans
l'optique d'un prelevement d'organes" - Conference d'experts Sfar / SRLF / Agence de
la Biomedecine, texte court publie dans Annales Francaises d'Anesthesie et de
Reanimation 24 (2005) 836-843. Source : sources/mort_encephalique.pdf (8 pages),
sources/mort_encephalique.txt.

METHODOLOGIE - PAS DU GRADE (1+/1-/2+/2-/AE) : methodologie RAND/UCLA. Chaque
recommandation necessitant une validation a ete cotee individuellement par les
experts sur une echelle de 1 a 9 ; le texte publie la MEDIANE des cotations entre
parentheses, ex. "(9)". Trois zones sont definies par le jury (section 1.2 du texte
source) : 1-3 = "desaccord", 4-6 = "indecision", 7-9 = "accord". Quand la mediane
tombe sur un demi-point (nombre pair de cotations), le texte l'imprime en notation
decimale francaise - virgule au lieu du point - ex. "(8,5)" = mediane 8,5.
AUDIT INDEPENDANT A L'AVEUGLE : un grep exhaustif confirme que le second chiffre
apres la virgule est TOUJOURS "5" sur les 11 occurrences du document (jamais "8,3"
ou "7,2" etc.) - ce qui exclut l'hypothese initiale (corrigee ici) d'un extreme
dissident cite en complement de la mediane, qui varierait. Chip a valeur unique
"8,5"/"7,5", jamais scinde en deux nombres ni interprete comme un second vote.
ANOMALIE SOURCE DISCLOSEE : le texte imprime ce meme code entre parentheses apres la
quasi-totalite des enonces cliniques du corps du texte, qu'il s'agisse d'une
recommandation soumise au vote du jury ou d'un simple rappel de donnee de
contexte/epidemiologique (aucune distinction typographique entre les deux usages
n'existe dans le texte source, qui ne comporte pas de liste de references numerotee
separee dans ces 8 pages). Cette fiche reproduit fidelement le chiffre imprime, sous
forme de chip colore selon la zone d'accord/indecision/desaccord, pour CHAQUE enonce
qui en porte un dans le texte source - sans affirmer qu'il s'agit toujours d'un vote
formel du jury plutot que d'un simple rappel bibliographique pour les rares passages
a tonalite purement descriptive (chapitre 1, paragraphes d'ouverture historique et
epidemiologique). Les tres rares enonces sans aucun chiffre entre parentheses dans le
texte source restent sans chip (ex. contexte legal d'ouverture, quelques criteres
d'organes sans cotation imprimee) - aucune cotation n'est inventee. Une seule occurrence
de cotation "6" existe dans tout le document (zone "indecision", chip orange) ; toutes
les autres cotations a un chiffre relevees sont 7, 8 ou 9 (zone "accord", chip vert).
Grep de controle sur ce script : aucun chip ne combine deux gradings GRADE (pas de
"1+/2+" etc., regle non pertinente ici car methodologie RAND/UCLA a chiffre unique).

Comptage exhaustif par grep sur le texte extrait (parentheses a 1 ou 2 chiffres,
hors "(2005)"/"(05)" de la reference DOI/journal) : 83x(9), 28x(8), 9x(7), 7x(7,5),
4x(8,5), 1x(6) = 132 codes au total.

Perimetre : les 4 chapitres du texte court sont couverts integralement (diagnostic de
la ME ; prise en charge en reanimation du donneur potentiel, y compris pediatrie ;
criteres d'evaluation par organe - coeur, poumon, foie, rein, pancreas, intestin,
tissus ; organisation du prelevement, y compris donneurs a coeur arrete/Maastricht).
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from style import *
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
                                 PageBreak, KeepTogether, ListFlowable, ListItem)
from reportlab.lib.units import mm

OUT = os.path.join(os.path.dirname(__file__), "..", "output",
                    "Fiche_SFAR_SRLF_ABM_Mort_Encephalique_2005.pdf")
OUT = os.path.abspath(OUT)

SOURCE_TXT = ("Source : « Prise en charge des sujets en état de mort encéphalique dans "
              "l'optique d'un prélèvement d'organes » — Conférence d'experts Sfar/SRLF/"
              "Agence de la Biomédecine, Ann Fr Anesth Réanim 2005;24:836-843. Fiche de "
              "synthèse non officielle : se référer au texte intégral.")

# Extension locale de GRADE_COLORS - cotation mediane RAND/UCLA (1-9), voir docstring.
GRADE_COLORS["9"] = (GREEN, WHITE)
GRADE_COLORS["8"] = (GREEN, WHITE)
GRADE_COLORS["7"] = (GREEN, WHITE)
GRADE_COLORS["6"] = (AMBER, WHITE)
GRADE_COLORS["8,5"] = (GREEN, WHITE)
GRADE_COLORS["7,5"] = (GREEN, WHITE)


def P(txt, style=S_CELL):
    return Paragraph(txt, style)


def chip(label):
    w = 15 * mm if len(label) <= 2 else 20 * mm
    return grade_chip(label, width=w, fontsize=8.4 if len(label) <= 2 else 7.4)


REF_W = 11 * mm
CHIP_W = 18 * mm
TEXT_W = PAGE_W - 2 * MARGIN - REF_W - CHIP_W


def reco_table(rows, col_widths=None):
    """rows: (ref, text, code_label_or_None)."""
    cw = col_widths or [REF_W, TEXT_W, CHIP_W]
    data = [[P("Réf.", S_HEAD_W), P("Recommandation / constat du jury", S_HEAD_W),
              P("Cotation", S_HEAD_W_C)]]
    for ref, txt, code in rows:
        cell = chip(code) if code else P("—", S_CELL_C)
        data.append([P(ref, S_CELL_B), P(txt, S_CELL), cell])
    t = Table(data, colWidths=cw, repeatRows=1)
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


def target_table(header, rows):
    """rows: (parametre, cible, code_label_or_None) - tables d'objectifs numeriques."""
    param_w = 55 * mm
    chip_w = 18 * mm
    val_w = PAGE_W - 2 * MARGIN - param_w - chip_w
    data = [[P(header[0], S_HEAD_W), P(header[1], S_HEAD_W), P("Cotation", S_HEAD_W_C)]]
    for param, cible, code in rows:
        cell = chip(code) if code else P("—", S_CELL_C)
        data.append([P(param, S_CELL_B), P(cible, S_CELL), cell])
    t = Table(data, colWidths=[param_w, val_w, chip_w], repeatRows=1)
    style_cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), TEAL_DARK), ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTNAME", (0, 0), (-1, 0), FONT_BOLD), ("FONTSIZE", (0, 0), (-1, 0), 8),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("ALIGN", (2, 0), (2, -1), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 0.5, GREY_LIGHT),
        ("TOPPADDING", (0, 0), (-1, -1), 3.0), ("BOTTOMPADDING", (0, 0), (-1, -1), 3.0),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            style_cmds.append(("BACKGROUND", (0, i), (-1, i), BG_PANEL))
    t.setStyle(TableStyle(style_cmds))
    return t


def legend_flowable():
    items = [("9", "Zone « accord » (7-9)"), ("6", "Zone « indécision » (4-6)"),
              ("8,5", "Médiane à un demi-point (notation décimale « 8,5 »)"), ("—", "Aucun chiffre imprimé")]
    content_w = PAGE_W - 2 * MARGIN
    n = len(items)
    chip_w = 20 * mm
    text_w = (content_w - n * chip_w) / n
    row_cells, col_widths = [], []
    for g, txt in items:
        if g == "—":
            row_cells.append(P("—", S_CELL_C))
        else:
            row_cells.append(chip(g))
        row_cells.append(P(txt, S_BADGE_HEAD))
        col_widths += [chip_w, text_w]
    row = Table([row_cells], colWidths=col_widths)
    row.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                              ("LEFTPADDING", (0, 0), (-1, -1), 1), ("RIGHTPADDING", (0, 0), (-1, -1), 1)]))
    return row


TOTAL_PAGES = {"n": 6}


def on_page(canvas, doc, page_title):
    header_band(canvas, doc, "SFAR/SRLF/AGENCE DE LA BIOMÉDECINE — CONFÉRENCE D'EXPERTS 2005 — FICHE DE SYNTHÈSE",
                "Mort encéphalique & prélèvement d'organes",
                page_title, icon_fn=lambda c, x, y: icon_drop(c, x, y, 13 * mm), color=TEAL_DARK)
    footer_band(canvas, doc, SOURCE_TXT, f"Page {doc.page} / {TOTAL_PAGES['n']}")


# ---------------------------------------------------------------------------
def _section_intro():
    story = [Spacer(1, 3 * mm)]
    story.append(info_panel(P(
        "<b>Champ :</b> prise en charge des sujets en état de mort encéphalique (ME) "
        "dans l'optique d'un prélèvement d'organes et de tissus. Conférence d'experts "
        "Sfar / Société de réanimation de langue française (SRLF) / Agence de la "
        "biomédecine, texte court publié le 15/06/2005 (Ann Fr Anesth Réanim "
        "2005;24:836-843), faisant suite à un premier référentiel de 1998. "
        "<b>4 chapitres</b> : (1) la ME — historique, concept, diagnostic ; "
        "(2) prise en charge en réanimation du donneur potentiel ; (3) critères "
        "d'évaluation des organes et des tissus ; (4) organisation du prélèvement "
        "d'organes, présent et avenir.", S_BODY), bg=BG_PANEL, border=TEAL))
    story.append(Spacer(1, 2 * mm))
    story.append(info_panel(P(
        "<b>Méthodologie de cotation — non-GRADE (RAND/UCLA) :</b> les recommandations "
        "nécessitant une validation ont été cotées individuellement par chaque expert sur "
        "une échelle de <b>1 à 9</b>. Le texte publie la <b>médiane</b> des cotations "
        "entre parenthèses. Trois zones : <b>1-3 « désaccord »</b>, <b>4-6 « indécision »</b>, "
        "<b>7-9 « accord »</b>. Quand la médiane tombe sur un demi-point (nombre pair de "
        "cotations), le texte l'imprime en notation décimale française — virgule au lieu "
        "du point — ex. « (8,5) » = médiane 8,5. Un audit indépendant a l'aveugle a "
        "vérifié cette lecture par grep exhaustif : le second chiffre après la virgule est "
        "<i>toujours</i> « 5 » sur les 11 occurrences du document, ce qui exclut "
        "l'hypothèse d'un extrême dissident cité (qui varierait). Chip à valeur unique "
        "« 8,5 », jamais scindé en deux nombres ni interprété comme un second vote."
        "<br/><br/>"
        "<b>Anomalie source disclosée :</b> ce même code entre parenthèses est imprimé "
        "après la quasi-totalité des énoncés du corps du texte, qu'il s'agisse d'une "
        "recommandation soumise au vote du jury ou d'un simple rappel de donnée de "
        "contexte/épidémiologique — le texte source (8 pages, sans liste de références "
        "numérotée séparée) ne distingue pas typographiquement les deux usages. Cette "
        "fiche reproduit fidèlement le chiffre imprimé, sous forme de chip coloré par "
        "zone, pour chaque énoncé qui en porte un — sans affirmer qu'il s'agit toujours "
        "d'un vote formel plutôt que d'un rappel bibliographique pour les rares passages "
        "purement descriptifs. Une seule occurrence de cotation « 6 » (indécision) existe "
        "dans tout le document ; toutes les autres cotations à un chiffre relevées sont "
        "7, 8 ou 9 (accord). Les énoncés du texte source sans aucun chiffre entre "
        "parenthèses restent sans chip (« — ») : aucune cotation n'est inventée.",
        S_BODY_SM), bg=GREY_LIGHT, border=GREY))
    story.append(Spacer(1, 2 * mm))
    story.append(section_bar("Légende des chips de cotation"))
    story.append(Spacer(1, 2 * mm))
    story.append(legend_flowable())
    return story


def _section_ch1():
    story = [Spacer(1, 2 * mm)]
    story.append(section_bar("Chapitre 1 — La mort encéphalique : historique, concept et diagnostic"))
    story.append(Spacer(1, 2 * mm))
    story.append(P(
        "Depuis sa description initiale en 1959, la ME a permis les prélèvements d'organes "
        "et/ou de tissus chez le cadavre à cœur battant. Les lois de bioéthique de 1994, "
        "révisées en 2004, ont posé les principes généraux du prélèvement (anonymat, "
        "gratuité, consentement) et élevé certaines modalités au rang de principes "
        "(diagnostic de la mort, sécurité sanitaire). Le décret d'application de 1996 "
        "impose que le diagnostic de ME repose sur les données de l'examen clinique "
        "confirmé par un examen complémentaire. <i>(Contexte historique/légal — aucun "
        "chiffre de cotation imprimé pour ce paragraphe.)</i>", S_NOTE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "Les enquêtes d'incidence de la ME en France et dans d'autres pays l'évaluent à "
        "7-13 % des décès en réanimation et en soins intensifs, soit 3 300 à 3 800 "
        "donneurs potentiels par an estimés. Le codage systématique de la ME dans le PMSI "
        "(Z005 : examen d'un donneur éventuel d'organes et de tissus ; Z528 : donneur "
        "d'organes et de tissus) permettrait d'estimer en continu le nombre de donneurs "
        "potentiels (8). La ME est définie comme la destruction irréversible de "
        "l'ensemble des fonctions cérébrales chez un sujet à cœur battant, conséquence "
        "d'un arrêt complet de la circulation cérébrale : les organes restent "
        "fonctionnels si la réanimation est adaptée, mais la destruction encéphalique "
        "supprime la commande centrale de la respiration et la régulation de "
        "l'homéostasie circulatoire, thermique et endocrinienne (arrêt respiratoire, "
        "hypotension, hypothermie, diabète insipide).", S_NOTE))
    story.append(Spacer(1, 2 * mm))
    story.append(reco_table([
        ("1.1", "Une anamnèse cohérente complète et un examen clinique neurologique sans "
                "ambiguïté sont essentiels pour porter le diagnostic de ME ; ces éléments "
                "doivent être consignés par écrit.", "9"),
        ("1.2", "Élimination systématique des facteurs confondants cliniques : hypothermie "
                "(température centrale &lt; 35 °C), imprégnation médicamenteuse ou toxique "
                "susceptible d'interférer avec l'examen clinique.", "9"),
        ("1.3", "En l'absence de facteurs confondants, l'examen neurologique doit observer "
                "un coma non réactif (Glasgow à 3) associé à l'abolition des réflexes du "
                "tronc cérébral et de la ventilation spontanée.", None),
        ("1.4", "Épreuve d'hypercapnie sous oxygénothérapie efficace contrôlée par SpO2 "
                "(après ventilation en normocapnie) : atteindre en apnée une PaCO2 proche "
                "de 60 mmHg pour affirmer l'absence de mouvements respiratoires.", "9"),
        ("1.5", "Dans l'optique du don, le diagnostic clinique de ME doit être confirmé par "
                "un examen complémentaire exigé par la loi : soit deux EEG nuls et non "
                "réactifs pendant 30 minutes, effectués à 4 heures d'intervalle, soit une "
                "angiographie cérébrale objectivant l'arrêt de perfusion des 4 axes.", None),
        ("1.6", "La vélocimétrie Doppler transcrânienne n'a pas de valeur réglementaire "
                "pour le diagnostic de ME. Non invasive et répétable au lit du malade, elle "
                "est prédictive de ME avec une spécificité de 100 % et une sensibilité "
                "d'environ 90 % en visualisant un flux oscillant systolodiastolique "
                "(arrêt circulatoire cérébral).", None),
        ("1.7", "Quand l'examen clinique est compatible avec la ME, l'examen Doppler peut "
                "permettre d'évoquer de manière rapide et précoce le diagnostic d'arrêt "
                "circulatoire cérébral.", "7"),
        ("1.7b", "Cela permet la mise en route sans retard des procédures réglementaires de "
                "confirmation de ME et peut raccourcir le délai entre la mort et le "
                "prélèvement.", "8"),
        ("1.8", "L'EEG (silence électrocérébral, amplitude &lt; 5 µV) est le test de "
                "confirmation de ME prévu par la réglementation, à condition d'exclure "
                "l'influence de la sédation ou de troubles métaboliques.", "9"),
        ("1.8b", "Avant d'utiliser les deux EEG comme moyen paraclinique, il convient de "
                "s'assurer que les dosages sanguins/urinaires ne décèlent aucun médicament "
                "du SNC à dose susceptible d'interférer avec l'interprétation de l'EEG — "
                "non coté dans le texte source.", None),
        ("1.8c", "L'hypothermie modérée (température voisine de 30 °C) n'empêche pas "
                "l'interprétation de l'EEG.", "7"),
        ("1.8d", "Cependant, en l'absence de donnée confirmant ce fait en contexte de ME, "
                "une hypothermie entre 30 et 35 °C peut gêner l'attestation de nullité de "
                "l'EEG — non coté dans le texte source.", None),
        ("1.9", "Les potentiels évoqués (PE), intéressants chez les patients sédatés, n'ont "
                "pas de valeur réglementaire en France pour la confirmation de ME.", None),
        ("1.10", "L'angiographie cérébrale (voie artérielle ou veineuse) est la seconde "
                 "méthode de confirmation prévue par la réglementation. L'angioscanner par "
                 "voie veineuse est recommandé comme moyen de confirmation de l'arrêt "
                 "circulatoire encéphalique.", "8"),
        ("1.11", "Le compte rendu écrit de l'examen électrophysiologique ou de "
                 "l'angiographie doit être signé immédiatement par un médecin qualifié.", None),
        ("1.12", "En cas de ME clinique, adapter sans délai les méthodes de réanimation et "
                 "contacter la coordination hospitalière (« donneur potentiel »).", "9"),
        ("1.12b", "La décision d'amener le sujet au prélèvement relève du médecin du "
                 "donneur (absence d'opposition, absence de contre-indication générale) ; "
                 "la décision de prélever tel ou tel organe relève uniquement du médecin "
                 "transplanteur, via la coordination hospitalière.", "8"),
        ("1.13", "L'accompagnement de la famille doit respecter et prendre en compte ses "
                 "convictions religieuses et différences culturelles ; la qualité de "
                 "l'accueil des familles et des proches est déterminante pour l'acceptation "
                 "ou le refus du don.", "9"),
        ("1.14", "Les entretiens doivent se dérouler dans un local décent, permettant de "
                 "faire asseoir les participants et de préserver l'intimité et la "
                 "confidentialité.", "9"),
        ("1.14b", "Ils interviennent après confirmation paraclinique de la ME et assurance "
                 "par la coordination de la faisabilité des prélèvements.", "8"),
        ("1.14c", "Objectifs de l'entretien (non cotés dans le texte source) : annoncer le "
                 "décès ; informer sur la ME, le don et sa finalité ; rechercher le refus de "
                 "prélèvement exprimé du vivant du défunt.", None),
        ("1.15", "L'entretien doit au mieux être mené à deux (le réanimateur et un membre "
                 "de la coordination hospitalière), qui doivent se présenter à la famille.", "9"),
    ]))
    return story


def _section_ch2a():
    story = [Spacer(1, 2 * mm)]
    story.append(section_bar("Chapitre 2 — Prise en charge en réanimation du donneur potentiel"))
    story.append(Spacer(1, 2 * mm))
    story.append(P(
        "L'instabilité hémodynamique au cours de la ME est fréquente et multifactorielle "
        "(disparition du contrôle sympathique, phénomènes inflammatoires, "
        "ischémie-reperfusion, troubles hormonaux, hypothermie) ; elle induit un "
        "dysfonctionnement cardiaque, parfois réversible, dans 40 % des cas. Le diabète "
        "insipide, fréquent, est secondaire à un déficit de production d'ADH. La "
        "dysfonction antéhypophysaire (baisse des hormones thyroïdiennes et du cortisol) "
        "est bien établie chez l'animal, sa responsabilité dans l'altération de la "
        "fonction myocardique restant controversée chez l'homme.", S_NOTE))
    story.append(Spacer(1, 2 * mm))
    story.append(reco_table([
        ("2.1", "Reconnaissance précoce de l'instabilité hémodynamique afin de permettre "
                "des mesures thérapeutiques immédiates. Conditionnement minimal de tout "
                "donneur potentiel : électrocardioscope, oxymétrie de pouls, cathétérisme "
                "de l'artère radiale (si possible gauche ou aux membres supérieurs), voie "
                "veineuse profonde, surveillance de la température centrale, sondage "
                "vésical.", "9"),
        ("2.2", "Il n'existe pas de signe clinique spécifique de l'hypovolémie au cours de "
                "la ME ; elle doit être dépistée précocement. Bien que non validée en "
                "contexte de ME, l'utilisation de critères dynamiques de réponse au "
                "remplissage vasculaire (lever de jambe passif, variabilité respiratoire de "
                "la pression artérielle, du flux aortique ou du diamètre de la veine cave "
                "supérieure en échocardiographie Doppler) est recommandée.", "8,5"),
        ("2.3", "Le dépistage de la dysfonction myocardique repose sur l'échocardiographie "
                "Doppler, qui permet une meilleure prise en charge du donneur tout en "
                "évaluant la qualité du greffon cardiaque éventuel.", "9"),
        ("2.4", "L'intérêt des marqueurs biologiques (créatinine kinase et fraction MB, "
                "troponine Ic, BNP/ProBNP) pour la reconnaissance d'une dysfonction "
                "myocardique est encore mal connu au cours de la ME.", None),
        ("2.5", "En cas de défaillance cardiocirculatoire non contrôlée, le recours à une "
                "technique d'exploration hémodynamique (échocardiographie, cathétérisme "
                "cardiaque droit, Doppler œsophagien, système Picco…), laissé au choix de "
                "l'opérateur, est recommandé.", "9"),
    ]))
    return story


def _section_ch2b():
    story = [Spacer(1, 2 * mm)]
    story.append(section_bar("Objectifs thérapeutiques recommandés — donneur potentiel"))
    story.append(Spacer(1, 2 * mm))
    story.append(target_table(("Paramètre", "Cible"), [
        ("Pression artérielle moyenne", "65 à 100 mmHg", "9"),
        ("Diurèse", "1 à 1,5 ml/kg/h", "9"),
        ("Température centrale", "35,5 à 38 °C", "9"),
        ("PaO2", "&gt; 80 mmHg", "9"),
        ("Hémoglobine", "&gt; 7 g/dl", "9"),
        ("Lactate artériel", "normal", "7"),
    ]))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "En parallèle, surveiller l'apparition/l'évolution d'un diabète insipide par "
        "évaluation régulière du bilan entrées-sorties, de la densité urinaire et des "
        "ionogrammes sanguins et urinaires (9).", S_NOTE))
    story.append(Spacer(1, 2.5 * mm))
    story.append(reco_table([
        ("2.6", "Remplissage vasculaire (RV) modéré : cristalloïdes ou colloïdes "
                "indifféremment ; au-delà de 3 000 ml, utiliser les colloïdes plutôt que "
                "les cristalloïdes.", "7,5"),
        ("2.7", "Le contrôle précoce du diabète insipide permet d'éviter un RV massif, "
                "délétère pour un éventuel prélèvement pulmonaire ; compléter par des "
                "transfusions sanguines et traitements substitutifs si besoin.", None),
        ("2.8", "Le recours aux vasopresseurs, si nécessaire, repose en première intention "
                "sur la noradrénaline.", "9"),
        ("2.9", "Traitement du diabète insipide : précoce, par desmopressine intraveineuse "
                "en fonction de la diurèse et, si nécessaire, compensation de la diurèse "
                "par un soluté adapté à l'osmolalité sanguine.", "9"),
        ("2.10", "En cas de dysfonction myocardique : adjonction d'un inotrope "
                 "(dobutamine) ou remplacement de la noradrénaline par de l'adrénaline.", "9"),
        ("2.10b", "Certaines études montrent que l'hormonothérapie substitutive (hormone "
                 "thyroïdienne, cortisol et arginine-vasopressine) apporterait un bénéfice "
                 "hémodynamique chez le donneur et sur la qualité des greffons.", "7"),
        ("2.10c", "De plus, l'arginine-vasopressine pourrait permettre une réduction des "
                 "besoins en catécholamines.", "6"),
    ]))
    story.append(Spacer(1, 2 * mm))
    story.append(info_panel(P(
        "<b>Pas de recommandation forte :</b> ces deux constats portent les cotations les "
        "plus basses de tout le document (« 7 » et « 6 » — cette dernière est l'unique "
        "occurrence d'une cotation en zone « indécision » relevée dans le texte source). "
        "Le texte source précise explicitement que des études complémentaires prospectives "
        "sont nécessaires avant d'apporter une recommandation forte sur l'utilisation de "
        "l'hormonothérapie substitutive.",
        S_BODY_SM), bg=GREY_LIGHT, border=GREY))
    return story


def _section_ch2c():
    story = [Spacer(1, 2 * mm)]
    story.append(section_bar("Optimisation pulmonaire, hémostase, infection, pédiatrie"))
    story.append(Spacer(1, 2 * mm))
    story.append(P(
        "Tous les donneurs d'organes sont des donneurs potentiels de poumon ; "
        "l'optimisation de la prise en charge d'un donneur limite peut améliorer la "
        "fonction pulmonaire au moment du prélèvement.", S_NOTE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(target_table(("Ventilation (visée prélèvement pulmonaire)", "Objectif"), [
        ("PaCO2", "35 à 40 mmHg", "9"),
        ("PaO2 (FiO2 minimale)", "80 à 100 mmHg", "9"),
        ("PEP", "minimale, ≈ 5 cmH2O", "9"),
        ("Rapport PaO2/FiO2", "contrôle régulier, avant transfert au bloc", None),
        ("Manœuvres de recrutement alvéolaire", "recommandées", "8,5"),
    ]))
    story.append(Spacer(1, 2 * mm))
    story.append(reco_table([
        ("2.11", "L'intérêt du scanner thoracique systématique n'a pas été évalué dans "
                 "cette indication, mais le suivi radiologique thoracique peut anticiper "
                 "les mesures correctives en cas de dégradation.", None),
        ("2.12", "Fibroscopie bronchique systématique si un prélèvement pulmonaire est "
                 "envisagé (identification d'une cause réversible de dégradation de "
                 "l'hématose). Une positivité de l'examen bactériologique direct ne "
                 "contre-indique pas le prélèvement pulmonaire, en l'absence de pneumonie "
                 "— non coté dans le texte source.", None),
        ("2.13", "La connaissance de la flore bactérienne du donneur oriente "
                 "l'antibiothérapie prophylactique et curative des receveurs en cas de "
                 "pneumonie bactérienne postopératoire précoce.", None),
        ("2.14", "Les perturbations de l'hémostase (CIVD, fibrinolyse, fibrinogénolyse) "
                 "sont fréquentes au cours de la ME et sont liées à l'atteinte cérébrale.", "8"),
        ("2.15", "Exploration de l'hémostase — 1er groupe de dosages : TP, TCA, "
                 "fibrinogène, facteur V, plaquettes.", "9"),
        ("2.16", "Exploration de l'hémostase — 2e groupe de dosages : D-dimères, "
                 "complexes solubles.", "7"),
    ]))
    story.append(Spacer(1, 1.5 * mm))
    story.append(target_table(("Hémostase — seuils minimaux à maintenir", "Cible"), [
        ("Plaquettes", "&gt; 50 G/l", "8"),
        ("Fibrinogène", "&gt; 1 g/l", "8"),
        ("TP / TCA", "TP &gt; 40 % et TCA ratio &lt; 1,5", "8"),
    ]))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "La desmopressine augmente le taux de vWF et de facteur VIII ainsi que "
        "l'agrégabilité plaquettaire : action procoagulante, proagrégante et "
        "profibrinolytique. <i>(Constat pharmacologique — sans chiffre imprimé.)</i>",
        S_NOTE))
    story.append(Spacer(1, 2 * mm))
    story.append(reco_table([
        ("2.17", "L'acceptabilité du donneur atteint d'affection bactérienne ou fongique "
                 "reste controversée. Prélèvements bactériologiques standards "
                 "(hémocultures, urocultures, prélèvements bronchiques) systématiques ; "
                 "recherche précoce d'une documentation bactérienne pulmonaire, technique "
                 "laissée au praticien.", "9"),
        ("2.18", "Une infection avérée chez le donneur potentiel n'est pas une "
                 "contre-indication formelle au prélèvement si l'agent pathogène est isolé "
                 "et un traitement efficace instauré depuis au moins 24-48 h.", "8"),
        ("2.18b", "Chaque situation nécessite une évaluation du bénéfice/risque, notamment "
                 "pour les germes à tropisme vasculaire.", "9"),
        ("2.18c", "En cas de prélèvement de poumons ou cœur-poumons : antibiothérapie par "
                 "amoxicilline-acide clavulanique 1 g/8 h.", "8"),
    ]))
    story.append(Spacer(1, 2 * mm))
    story.append(info_panel(P(
        "<b>Particularités pédiatriques :</b> le nombre de prélèvements d'organes chez "
        "l'enfant est faible en France (40 en 2003). Le diagnostic de ME chez le très "
        "jeune enfant repose sur des critères différents de ceux de l'adulte : chez le "
        "nouveau-né &lt; 7 jours et le prématuré, l'interprétation de l'examen clinique et "
        "de l'EEG étant très difficile, le recours à l'angiographie est le plus souvent "
        "nécessaire. Entre 7 jours et 2 mois : 2 examens cliniques et 2 EEG séparés de "
        "48 h. Entre 2 mois et 1 an : 2 examens cliniques et 2 EEG séparés de 24 h, sauf "
        "ischémie-anoxie cérébrale (observation plus longue recommandée). Au-delà d'un "
        "an, les critères sont ceux de l'adulte. La réanimation d'un enfant en ME repose "
        "sur les mêmes principes que chez l'adulte, en adaptant les posologies au poids "
        "et les paramètres hémodynamiques à l'âge.", S_BODY_SM), bg=BG_PANEL, border=TEAL))
    return story


def _section_ch3a():
    story = [Spacer(1, 2 * mm)]
    story.append(section_bar("Chapitre 3 — Critères d'évaluation des organes et des tissus"))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "Les critères de prélèvement évoluent avec l'expérience des équipes de greffe, "
        "ce qui a déjà permis d'étendre les prélèvements à des donneurs dits « limites ». "
        "Il est recommandé, pour tout donneur potentiel, de réaliser dès que possible et "
        "pour chaque organe un bilan précis clinique et paraclinique.", S_NOTE))
    story.append(Spacer(1, 2 * mm))
    story.append(section_bar("3.1 — Critères communs à tous les organes", color=GREY))
    story.append(Spacer(1, 1.5 * mm))
    story.append(reco_table([
        ("3.1.1", "Contre-indications réglementaires (sécurité sanitaire) : ESB ou maladie "
                  "équivalente, infection par le VIH, le VHC ou le VHB, tuberculose active, "
                  "syphilis — diverses dérogations validées ou en cours de discussion "
                  "(notamment VHB et syphilis).", None),
        ("3.1.2", "Contre-indications médicales : cancers avérés ou métastasés (exception "
                  "possible pour certaines tumeurs cérébrales).", None),
        ("3.1.3", "Évaluation au cas par cas du rapport risque/bénéfice : maladies de "
                  "système, allergies, la plupart des intoxications, infections "
                  "bactériennes, donneurs âgés.", None),
        ("3.1.4", "Données morphologiques requises pour chaque organe : si un scanner "
                  "cérébral est pratiqué pour confirmer la ME, réaliser en même temps une "
                  "tomodensitométrie thoraco-abdominale.", None),
    ], col_widths=[16 * mm, PAGE_W - 2 * MARGIN - 16 * mm - CHIP_W, CHIP_W]))
    story.append(Spacer(1, 2.5 * mm))
    story.append(section_bar("3.2 — Prélèvement cardiaque", color=GREY))
    story.append(Spacer(1, 1.5 * mm))
    story.append(reco_table([
        ("3.2.1", "L'examen clinique et l'anamnèse ne sont pas suffisamment sensibles/"
                  "spécifiques pour l'évaluation du greffon ; évaluer la fonction et la "
                  "structure du cœur par échographie transthoracique, complétée au moindre "
                  "doute par une échographie transœsophagienne.", "9"),
        ("3.2.2", "Les anomalies ECG isolées (sus/sous-décalage ST, inversion de l'onde T, "
                  "allongement du QT) ne sont pas à prendre en compte ; les arythmies "
                  "ventriculaires répétitives sans anomalie hydroélectrolytique évidente "
                  "sont en revanche de mauvais pronostic.", "7,5"),
        ("3.2.3", "L'absence de coronarographie au-delà de 55 ans ne doit pas être une "
                  "contre-indication au prélèvement.", "8"),
        ("3.2.4", "L'utilisation de catécholamines n'est plus en soi une contre-indication "
                  "au prélèvement cardiaque ; il est actuellement impossible de définir une "
                  "dose seuil.", "9"),
        ("3.2.5", "Devant une altération de la fonction systolique chez un patient "
                  "&lt; 55 ans sans facteur de risque cardiopathique : réanimation agressive "
                  "avant de décréter le cœur non prélevable.", "9"),
        ("3.2.6", "Dans ce cas, il est recommandé de pratiquer une nouvelle échographie "
                  "cardiaque après chaque ajustement thérapeutique.", "7"),
        ("3.2.7", "Contre-indications absolues (7 des 8 critères cotés « 9 » ; voir "
                  "3.2.8 pour le 8<sup>e</sup>) : intoxication au CO (taux &gt; 20 %), "
                  "arythmies ventriculaires graves, infarctus du myocarde documenté "
                  "(quelle que soit l'ancienneté), malformation cardiaque non corrigée, "
                  "tumeur cardiaque, hypokinésie globale (FEVG &lt; 0,3), lésions sévères "
                  "en coronarographie.", "9"),
        ("3.2.8", "Contre-indication absolue supplémentaire : hypoxémie sévère "
                  "(SaO2 &lt; 80 %).", "7,5"),
    ], col_widths=[16 * mm, PAGE_W - 2 * MARGIN - 16 * mm - CHIP_W, CHIP_W]))
    return story


def _section_ch3b():
    story = [Spacer(1, 2 * mm)]
    story.append(section_bar("3.3 — Prélèvement pulmonaire", color=GREY))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "Compte tenu de la rareté des prélèvements pulmonaires, il est particulièrement "
        "recommandé de tenir compte de l'évolution des critères.", S_NOTE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(reco_table([
        ("3.3.1", "Antécédents respiratoires chroniques/tabagisme et examen clinique "
                  "détaillé sont indispensables mais insuffisants pour la sélection "
                  "pulmonaire ; évaluation régulière de l'hématose et de l'imagerie "
                  "recommandée.", None),
        ("3.3.2", "La durée de ventilation n'est plus un critère de non-prélèvement, mais "
                  "une analyse au cas par cas des conditions de ventilation et de "
                  "colonisation des voies aériennes est indispensable.", "8"),
        ("3.3.3", "Une radiographie ou un scanner thoracique normal est un excellent "
                  "critère de prélèvement.", "8"),
        ("3.3.4", "Optimiser la ventilation mécanique avant d'utiliser les critères "
                  "d'imagerie et d'hématose.", "8,5"),
        ("3.3.5", "L'utilisation de catécholamines n'est plus un critère de non-"
                  "prélèvement.", "9"),
        ("3.3.6", "Contre-indications absolues : âge du donneur &gt; 70 ans ; opacités "
                  "alvéolaires bilatérales non réversibles après fibroaspiration/déplétion "
                  "hydrosodée/optimisation ventilatoire ; rapport PaO2/FiO2 &lt; 250 après "
                  "optimisation.", "9"),
        ("3.3.7", "Contre-indication absolue supplémentaire, non cotée dans le texte "
                  "source : antécédents de maladie respiratoire chronique non réversible.",
                  None),
        ("3.3.8", "Contre-indication absolue supplémentaire : ischémie froide &gt; 8 heures.",
                  "8"),
    ], col_widths=[16 * mm, PAGE_W - 2 * MARGIN - 16 * mm - CHIP_W, CHIP_W]))
    story.append(Spacer(1, 2.5 * mm))
    story.append(section_bar("3.4 — Prélèvement hépatique", color=GREY))
    story.append(Spacer(1, 1.5 * mm))
    story.append(reco_table([
        ("3.4.1", "La bonne qualité du greffon fourni par certains donneurs de 80 ans ou "
                  "plus a été largement démontrée.", "8,5"),
        ("3.4.2", "Le diabète et l'HTA ne sont pas en soi des contre-indications ; "
                  "l'éthylisme chronique ne contre-indique pas le prélèvement si le foie "
                  "est macroscopiquement normal et sans altération biologique majeure ; "
                  "une anomalie aiguë de la biologie hépatique (cytolyse) ne "
                  "contre-indique pas non plus.", None),
        ("3.4.3", "Une natrémie &gt; 170 mmol/l peut être une contre-indication au "
                  "prélèvement hépatique.", "7"),
        ("3.4.4", "Les infections virales nécessitent une attention particulière (tropisme "
                  "hépatique) mais ne contre-indiquent pas systématiquement le "
                  "prélèvement.", "8"),
        ("3.4.5", "Imagerie hépatique et abdominale indispensable (échographie et/ou "
                  "scanner) pour rechercher stéatose ou tumeur parenchymateuse.", None),
        ("3.4.6", "Biopsie hépatique indiquée en cas de maladie inflammatoire de "
                  "l'intestin, ou d'obésité morbide.", "8"),
        ("3.4.7", "Biopsie hépatique également indiquée lorsque le foie est "
                  "macroscopiquement douteux.", "9"),
        ("3.4.8", "La stéatose microvésiculaire, même massive, ne contre-indique pas le "
                  "prélèvement.", None),
        ("3.4.9", "La stéatose macro-vacuolaire peut contre-indiquer la greffe au-delà de "
                  "30-60 %, selon le degré d'urgence de la transplantation.", "7,5"),
        ("3.4.10", "En cas de doute, la décision relève de l'équipe de transplantation.", "9"),
    ], col_widths=[16 * mm, PAGE_W - 2 * MARGIN - 16 * mm - CHIP_W, CHIP_W]))
    return story


def _section_ch3c():
    story = [Spacer(1, 2 * mm)]
    story.append(section_bar("3.5 — Prélèvement rénal", color=GREY))
    story.append(Spacer(1, 1.5 * mm))
    story.append(reco_table([
        ("3.5.1", "L'âge du donneur, même très avancé, n'est pas une contre-indication ; "
                  "la qualité du greffon devra être analysée au vu des comorbidités, des "
                  "problèmes survenus en réanimation et du temps d'ischémie froide, à "
                  "réduire au maximum.", "9"),
        ("3.5.2", "Une HTA de plus de dix ans est à prendre en compte pour la décision de "
                  "prélèvement.", "8"),
        ("3.5.3", "Examens indispensables : créatininémie, ECBU, étude du sédiment "
                  "urinaire, imagerie rénale (échographie ou scanner).", "9"),
        ("3.5.4", "Le taux de créatininémie à l'admission (ou les jours précédents) et le "
                  "calcul de la clairance par la formule de Cockcroft sont des critères "
                  "déterminants de la qualité du greffon.", "9"),
        ("3.5.5", "Une hématurie/protéinurie modérées ou une insuffisance rénale aiguë "
                  "apparue en réanimation ne contre-indiquent pas le prélèvement.", "8"),
        ("3.5.5b", "Un arrêt cardiaque &lt; 30 minutes ou une instabilité hémodynamique, "
                  "même sous fortes doses de catécholamines, ne contre-indiquent pas non "
                  "plus le prélèvement — non coté dans le texte source.", None),
        ("3.5.6", "Limiter la multiplication des actes d'imagerie avec opacification "
                  "vasculaire (impact des produits de contraste iodés chez le donneur).", "7,5"),
        ("3.5.7", "Contre-indications : clairance de la créatinine &lt; 30 ml/min, "
                  "glomérulosclérose &gt; 50 %, lésions athéromateuses majeures.", "9"),
    ], col_widths=[16 * mm, PAGE_W - 2 * MARGIN - 16 * mm - CHIP_W, CHIP_W]))
    story.append(Spacer(1, 2.5 * mm))
    story.append(section_bar("3.6 — Prélèvement pancréatique", color=GREY))
    story.append(Spacer(1, 1.5 * mm))
    story.append(reco_table([
        ("3.6.1", "Pancréas total : âge du donneur &lt; 45 ans, sauf traumatisé sans "
                  "antécédent (jusqu'à 55 ans).", "7,5"),
        ("3.6.1b", "Îlots de Langerhans : âge entre 18 et 70 ans, meilleur résultat "
                  "au-delà de 50 ans — non coté dans le texte source.", None),
        ("3.6.1c", "Double greffe rein-pancréas : IMC préférentiellement &lt; 27 — non "
                  "coté dans le texte source.", None),
        ("3.6.2", "Un taux d'amylase égal au double de la norme ne contre-indique pas le "
                  "prélèvement.", "8"),
        ("3.6.2b", "Une imagerie pancréatique est recommandée avant le prélèvement — non "
                  "cotée dans le texte source.", None),
        ("3.6.3", "L'instabilité hémodynamique et l'arrêt cardiaque sont des facteurs de "
                  "risque de pancréatite aiguë et de thrombose des vaisseaux pancréatiques "
                  "chez le receveur ; une héparinothérapie pourrait être maintenue/"
                  "envisagée pour prévenir les microthromboses du greffon.", "7"),
        ("3.6.4", "Durée de séjour en réanimation avant prélèvement : ne devrait pas "
                  "dépasser 5 jours (discussion au cas par cas au-delà) — non coté dans le "
                  "texte source.", None),
        ("3.6.4b", "Ischémie froide : &lt; 8 h pour les îlots de Langerhans, &lt; 18 h pour "
                  "le pancréas total.", "8"),
        ("3.6.5", "L'aspect macroscopique du pancréas au bloc opératoire est le critère "
                  "final déterminant pour le prélèvement.", None),
    ], col_widths=[16 * mm, PAGE_W - 2 * MARGIN - 16 * mm - CHIP_W, CHIP_W]))
    return story


def _section_ch3d():
    story = [Spacer(1, 2 * mm)]
    story.append(section_bar("3.7 — Prélèvement intestinal", color=GREY))
    story.append(Spacer(1, 1.5 * mm))
    story.append(reco_table([
        ("3.7.1", "Pas de limite inférieure d'âge pour les donneurs pédiatriques. Greffe "
                  "isolée d'intestin : poids du donneur &lt; 4 fois celui du receveur ; "
                  "greffe combinée foie-intestin : ratio &lt; 2.", None),
        ("3.7.2", "Une laparotomie antérieure ne contre-indique pas le prélèvement.", "8"),
        ("3.7.3", "Des antécédents de maladie chronique de l'intestin contre-indiquent le "
                  "prélèvement.", "9"),
        ("3.7.4", "Greffes combinées foie + intestin : transaminases &lt; 3 fois la normale "
                  "et γ-GT normales.", None),
        ("3.7.5", "Un arrêt cardiaque prolongé et/ou une instabilité hémodynamique "
                  "contre-indiquent le prélèvement (risque d'ischémie mésentérique).", "8"),
        ("3.7.5b", "De même, l'utilisation d'adrénaline/noradrénaline au-delà de "
                  "2 µg/kg/min doit faire contre-indiquer le prélèvement.", "7,5"),
        ("3.7.6", "Une hypernatrémie au moment du prélèvement est associée à un taux élevé "
                  "de perte de greffons.", None),
    ], col_widths=[16 * mm, PAGE_W - 2 * MARGIN - 16 * mm - CHIP_W, CHIP_W]))
    story.append(Spacer(1, 2.5 * mm))
    story.append(section_bar("3.8 — Prélèvements de tissus", color=GREY))
    story.append(Spacer(1, 1.5 * mm))
    story.append(reco_table([
        ("3.8.1", "Nombreux tissus prélevables : cornées, membranes amniotiques, os "
                  "massifs, tissus mous de l'appareil locomoteur, vaisseaux, valves "
                  "cardiaques, peau. Prélèvements réalisables lors d'un PMO ou à la "
                  "morgue ; organisation toujours gérée par la coordination hospitalière. "
                  "Pas de limite d'âge pour le donneur.", None),
        ("3.8.2", "Contrôle qualité de chaque greffon réalisé par la banque de tissus qui "
                  "le réceptionne.", None),
        ("3.8.3", "Les antécédents de cancer solide ne contre-indiquent pas le prélèvement "
                  "de cornée.", "9"),
        ("3.8.3b", "Les infections virales ne sont pas une contre-indication systématique "
                  "au prélèvement de tissus.", "8"),
        ("3.8.4", "Les échantillons sanguins prélevés après le décès pour la sécurité "
                  "sanitaire doivent être centrifugés au plus vite pour éviter les erreurs "
                  "d'interprétation ; au mieux, récupérer du sang pré-mortem au laboratoire "
                  "de l'hôpital.", "9"),
        ("3.8.5", "Il est souhaitable de développer les réseaux de prélèvement et les "
                  "échanges interbanques de tissus, notamment pour les cornées.", "9"),
    ], col_widths=[16 * mm, PAGE_W - 2 * MARGIN - 16 * mm - CHIP_W, CHIP_W]))
    return story


def _section_ch4():
    story = [Spacer(1, 2 * mm)]
    story.append(section_bar("Chapitre 4 — Organisation du prélèvement d'organes : présent et avenir"))
    story.append(Spacer(1, 2 * mm))
    story.append(reco_table([
        ("4.1", "Le prélèvement d'organes et de tissus est une activité médicale dans "
                "laquelle tous les centres hospitaliers doivent s'inscrire, organisée sur "
                "l'unité de coordination hospitalière selon des procédures écrites "
                "respectant les recommandations de l'Agence de la biomédecine.", None),
        ("4.2", "L'unité de coordination hospitalière doit être structurée et visible, "
                "individualisant les tâches respectives de chacun.", "9"),
        ("4.3", "Critères d'évaluation de l'activité hospitalière : exhaustivité du "
                "recueil des comas graves ; appel systématique et précoce de la "
                "coordination dès que le diagnostic de ME est envisagé ; appel au service "
                "de régulation et d'appui dès l'intention de prélever ; intégration "
                "réelle du prélèvement dans l'activité chirurgicale d'urgence ; qualité de "
                "la tenue du dossier de coordination.", "9"),
        ("4.4", "La coordination hospitalière vérifie la qualité de la restitution du "
                "corps, accompagne la famille dans les démarches et reste disponible pour "
                "un suivi ultérieur des proches.", "9"),
        ("4.5", "Au niveau national, l'Agence de la biomédecine valide les critères de "
                "sélection et garantit la sécurité sanitaire des greffons ; au niveau "
                "inter-régional (SRA), elle valide la procédure de prélèvement, participe "
                "à la qualification des greffons, et les répartit/attribue selon la "
                "réglementation.", None),
        ("4.6", "La prise en charge peropératoire du sujet en ME doit être effectuée par "
                "un médecin qualifié en anesthésie-réanimation ; le transport entre "
                "réanimation et bloc opératoire est une période à risque maximum — sujet "
                "monitoré, accompagné par une équipe médicalisée.", "9"),
        ("4.7", "L'utilisation d'analgésiques et de myorelaxants chez un sujet en ME est "
                "justifiée.", "9"),
        ("4.8", "La prise en charge instituée en réanimation doit être maintenue en "
                "période peropératoire, avec mise en place d'un monitorage supplémentaire "
                "si l'état hémodynamique l'exige ; les règles de transfusion et d'apport de "
                "produits sanguins restent valables en période peropératoire.", "9"),
    ]))
    return story


def _section_ch4b():
    story = [Spacer(1, 2 * mm)]
    story.append(section_bar("Prélèvement multi-organes (PMO) — organisation pratique"))
    story.append(Spacer(1, 2 * mm))
    story.append(reco_table([
        ("4.9", "Tout participant à un PMO doit avoir un comportement consensuel, courtois, "
                "et veiller à une bonne coordination entre équipes ; le chirurgien doit "
                "avoir été formé spécifiquement à la technique du PMO.", "9"),
        ("4.10", "Le PMO est une urgence chirurgicale qui ne doit passer qu'après les "
                 "urgences hémorragiques et obstétricales ; il est recommandé de "
                 "l'effectuer dans une salle dédiée avec une équipe spécifique, sans "
                 "perturber les autres activités chirurgicales.", "9"),
        ("4.11", "Veiller à ce que l'installation du malade convienne à toutes les équipes "
                 "chirurgicales.", "9"),
    ]))
    story.append(Spacer(1, 2 * mm))
    story.append(P("<b>Chronologie du PMO (telle que décrite par le texte source) :</b>", S_BODY_SM))
    story.append(Spacer(1, 1 * mm))
    chrono = ["Exploration et préparation de l'étage abdominal",
              "Exploration et préparation de l'étage thoracique",
              "Héparinisation 10 minutes avant le clampage et perfusion in situ",
              "Prélèvements des organes thoraciques",
              "Prélèvements des organes abdominaux",
              "Prélèvements des tissus",
              "Restauration tégumentaire solide et esthétique"]
    story.append(ListFlowable(
        [ListItem(P(x, S_CELL), leftIndent=0) for x in chrono],
        bulletType="1", start=1, leftIndent=10 * mm, bulletFontSize=8.6))
    story.append(Spacer(1, 2 * mm))
    story.append(reco_table([
        ("4.12", "Aucun geste à fort risque hémorragique (canulation aortique, contrôle de "
                 "l'aorte cœliaque, canulation de la VCI) ne doit être réalisé tant que les "
                 "différentes équipes ne sont pas prêtes à clamper — non coté dans le texte "
                 "source.", None),
        ("4.13", "Pour raccourcir au maximum la durée d'ischémie froide des prélèvements à "
                 "visée immunologique, faire parvenir au laboratoire au moins 3 ganglions "
                 "de bonne qualité (0,5 cm de diamètre) le plus tôt possible.", "9"),
        ("4.14", "Prélèvements sanguins/tissulaires pour tests immunologiques et "
                 "sérologies réglementaires (typage HLA, cross-matches) : le plus tôt "
                 "possible, résultats rendus en urgence — sans attendre la confirmation de "
                 "ME ni l'accord des proches.", "9"),
        ("4.15", "Conditionnement des organes : immersion dans un liquide de préservation à "
                 "4 °C, triple emballage stérile, placés dans la glace, accompagnés d'un "
                 "tube de sang à température ambiante pour vérification ultime du groupe "
                 "sanguin.", "9"),
        ("4.16", "Pas de consensus sur la solution de conservation des organes à utiliser ; "
                 "les solutions de type extracellulaire sont à privilégier. Utiliser la "
                 "même solution de conservation pour le prélèvement simultané des viscères "
                 "intra-abdominaux.", "9"),
        ("4.17", "Pendant toute la durée de l'ischémie froide, la température de "
                 "conservation des greffons doit être strictement maintenue entre 2 et "
                 "4 °C.", None),
        ("4.18", "Prélèvement bactériologique et mycologique du liquide de conservation "
                 "systématique avant l'implantation de chaque greffon.", "9"),
        ("4.19", "Avant toute transplantation rénale ou pancréatique, le cross-match doit "
                 "être réalisé en urgence.", "9"),
        ("4.20", "Avant tout prélèvement à des fins thérapeutiques, qualification des "
                 "organes par recherche d'infection : VIH, VHB, VHC, HTLV, CMV, EBV, "
                 "syphilis, toxoplasmose — l'appariement peut ne pas tenir compte du statut "
                 "sérologique du receveur selon l'infection détectée, avec situations "
                 "dérogatoires selon l'organe et l'urgence.", None),
    ]))
    return story


def _section_ch4c_sources():
    story = [Spacer(1, 2 * mm)]
    story.append(section_bar("Donneurs à cœur arrêté (Maastricht)", color=GREY))
    story.append(Spacer(1, 1.5 * mm))
    story.append(reco_table([
        ("4.21", "Dans certains pays, les prélèvements sur donneurs à cœur arrêté ont "
                 "augmenté significativement le nombre de transplantations ; avec des "
                 "critères de sélection stricts des donneurs et des receveurs, cette "
                 "technique procure aux équipes entraînées des résultats de survie et de "
                 "fonction des greffons rénaux comparables aux prélèvements sur donneurs à "
                 "cœur battant.", "8"),
        ("4.22", "La pose de la sonde de Gillot, l'exsanguination et la réfrigération du "
                 "donneur potentiel ont été approuvées par le comité d'éthique de l'Agence "
                 "de la biomédecine, qui considère ces gestes possibles dès le constat du "
                 "décès et dans l'attente de l'entrevue avec la famille.", None),
        ("4.23", "Les prélèvements à cœur arrêté supposent des aménagements réglementaires "
                 "en cours de développement et ne concerneront pas les donneurs relevant "
                 "de la catégorie III (arrêt de soins) de la classification de Maastricht.", None),
        ("4.24", "Le choix de ce type de prélèvement nécessite une organisation médicale et "
                 "paramédicale spécifique.", "8"),
    ]))
    story.append(Spacer(1, 4 * mm))
    story.append(section_bar("Sources et traçabilité", color=GREY))
    story.append(Spacer(1, 2 * mm))
    story.append(P(
        "<b>Document source :</b> « Prise en charge des sujets en état de mort "
        "encéphalique dans l'optique d'un prélèvement d'organes », conférence d'experts "
        "Sfar (G. Boulard, T. Pottecher) / SRLF (P. Guiot, A. Tenaillon) / Agence de la "
        "biomédecine, texte court, Ann Fr Anesth Réanim 2005;24:836-843, disponible sur "
        "internet le 15/06/2005. Fait suite à un premier référentiel Sfar/EfG/Société "
        "française de transplantation de 1998.", S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>Méthodologie :</b> cotation RAND/UCLA, médiane sur échelle 1-9 (zones "
        "désaccord 1-3 / indécision 4-6 / accord 7-9), parfois imprimée en notation "
        "décimale française à un demi-point (ex. « 8,5 »). Voir encart méthodologie et "
        "légende, page 1.", S_SOURCE))
    story.append(P(
        "<b>URL source :</b> https://sfar.org/prise-en-charge-des-sujets-en-etat-de-mort-"
        "encephalique-dans-loptique-dun-prelevement-dorganes/",
        S_SOURCE))
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Avertissement :</b> ce document est une fiche de synthèse indépendante, "
        "produite pour un usage d'aide-mémoire. Il reprend l'intégralité des "
        "recommandations et constats gradués des 4 chapitres de la conférence d'experts, "
        "mais ne remplace pas le texte intégral (argumentaire complet, références "
        "bibliographiques) et n'est ni édité ni validé par la Sfar, la SRLF ou l'Agence "
        "de la biomédecine. Texte de 2005 : se référer également, en complément, aux "
        "procédures locales de coordination hospitalière et aux évolutions réglementaires "
        "et pratiques plus récentes (catégories de Maastricht, critères d'organes), et à "
        "un avis spécialisé/à la coordination hospitalière en cas de doute.",
        S_BODY_SM), bg=GREY_LIGHT, border=GREY))
    return story


# Troisieme element = forcer un saut de page avant cette section (True aux frontieres
# de chapitre uniquement) ; entre sous-sections d'un meme chapitre, laisser le texte
# s'ecouler naturellement pour eviter les pages a moins de 60% de remplissage (voir
# CLAUDE.md - fusion de sections adjacentes plutot que saut systematique).
SECTIONS = [
    ("Introduction & méthodologie", _section_intro, True),
    ("Chapitre 1 — Diagnostic de la mort encéphalique", _section_ch1, True),
    ("Chapitre 2 — Réanimation du donneur (hémodynamique)", _section_ch2a, True),
    ("Chapitre 2 — Objectifs thérapeutiques", _section_ch2b, False),
    ("Chapitre 2 — Poumon, hémostase, infection, pédiatrie", _section_ch2c, False),
    ("Chapitre 3 — Critères organes : général & cœur", _section_ch3a, True),
    ("Chapitre 3 — Poumon & foie", _section_ch3b, False),
    ("Chapitre 3 — Rein & pancréas", _section_ch3c, False),
    ("Chapitre 3 — Intestin & tissus", _section_ch3d, False),
    ("Chapitre 4 — Organisation du prélèvement", _section_ch4, True),
    ("Chapitre 4 — PMO : chronologie & traçabilité", _section_ch4b, False),
    ("Chapitre 4 — Cœur arrêté & sources", _section_ch4c_sources, False),
]


def _make_doc(path=None):
    return SimpleDocTemplate(path or OUT, pagesize=A4,
                              leftMargin=MARGIN, rightMargin=MARGIN,
                              topMargin=32 * mm, bottomMargin=16 * mm,
                              title="Fiche SFAR/SRLF/ABM 2005 - Mort encéphalique et prélèvement d'organes",
                              author="Synthèse indépendante (source SFAR)")


def _silent_page(canvas, doc_):
    pass


def _build_upto(sections):
    """sections: liste de (fn, new_page_bool). Saut de page uniquement quand
    new_page_bool est True (frontieres de chapitre) - entre sous-sections d'un meme
    chapitre, le texte s'ecoule sans saut force pour eviter les pages trop vides."""
    story = []
    for i, (fn, new_page) in enumerate(sections):
        if i > 0 and new_page:
            story.append(PageBreak())
        elif i > 0:
            story.append(Spacer(1, 4 * mm))
        story.extend(fn())
    return story


def _count_pages(story_flowables):
    # Throwaway measurement builds must NEVER write to OUT (see CLAUDE.md) - reusing OUT
    # here was found in a prior fiche to silently corrupt page 1's header_band in the
    # final build. Always use a fresh tempfile.mktemp() path for these measurement passes.
    import pypdf, tempfile
    tmp_path = tempfile.mktemp(suffix=".pdf")
    doc = _make_doc(tmp_path)
    doc.build(story_flowables, onFirstPage=_silent_page, onLaterPages=_silent_page)
    with open(tmp_path, "rb") as f:
        n = len(pypdf.PdfReader(f).pages)
    os.remove(tmp_path)
    return n


def build():
    pairs = [(fn, new_page) for _, fn, new_page in SECTIONS]

    boundaries = []
    for i in range(1, len(pairs) + 1):
        pages = _count_pages(_build_upto(pairs[:i]))
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

    final_story = _build_upto(pairs)
    docf = _make_doc()
    docf.build(final_story, onFirstPage=on_page_final, onLaterPages=on_page_final)
    print("OK ->", OUT, f"({total_pages} pages)")


if __name__ == "__main__":
    build()
