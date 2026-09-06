# -*- coding: utf-8 -*-
"""
Fiche de synthese - XXe Conference de Consensus en Reanimation et Medecine d'Urgence
(12 octobre 2000) "Corticotherapie au cours du choc septique et du SDRA". Organisee par
la SFAR avec la participation de la Societe de Pathologie Infectieuse de Langue
Francaise, la Societe de Pneumologie de Langue Francaise et le Groupe Francophone de
Reanimation et Urgences Pediatriques. Labellisee ANAES. Source : sources/
corticotherapie_choc_septique.pdf (6 pages, texte "Resume"), sources/
corticotherapie_choc_septique.txt.

METHODOLOGIE - PAS DU GRADE (1+/1-/2+/2-/AE) : la source imprime, entre crochets, un
code combinant DEUX axes independants definis en fin de texte ("Score d'evaluation des
references" a/b/c/d = qualite de la preuve bibliographique ; "Score de recommandations"
1/2/3 = force du consensus du jury) :
  - un code a DEUX caracteres (ex. [1a], [2b]) quand la phrase est a la fois une
    recommandation graduee ET rattachee a un niveau de preuve precis ;
  - un code a UN SEUL caractere - soit une lettre seule ([a],[b],[c]) quand la phrase
    est une donnee de preuve/contexte non formulee comme une recommandation graduee,
    soit un chiffre seul ([2]) quand la phrase est une recommandation du jury sans
    niveau de preuve rattache.
Comptage exhaustif par grep sur le texte extrait : 3x[1a], 2x[2a], 1x[2b], 2x[1b],
3x[2], 4x[a], 7x[b], 1x[c] = 23 codes au total, aucun [3] ni [d] ni [1] seul dans le
corps du texte (l'echelle en prevoit pourtant 3 niveaux et 4 lettres - seuls niveau 3
et preuve d ne sont concretement utilises nulle part dans ce document court).
Chips ici = EXACTEMENT le code imprime par le jury pour cette phrase precise (aucune
fusion de deux phrases distinctement cotees dans un seul chip). Le protocole pratique
complet de la Question 4 (choc septique : indication, posologie, duree, surveillance)
et la posologie pratique de la Question 5 (SDRA) NE PORTENT AUCUN CROCHET dans le texte
source, contrairement au reste du document - anomalie source disclosee ici (chip
"N.C." = non cote dans le texte source, jamais une cotation inventee) plutot que
silencieusement gommee.

GRADE_COLORS etendu localement (meme precedent que fiche_glycemie.py / fiche_nutrition.py
/ fiche_eer.py / fiche_aap_programmee.py) avec les codes litteraux de cette source
("1a","1b","2a","2b","2","a","b","c","N.C.") plutot que reutilises les cles GRADE
existantes (1+/2+/etc.) qui appartiennent a un tout autre referentiel methodologique.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from style import *
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.units import mm

OUT = os.path.join(os.path.dirname(__file__), "..", "output",
                    "Fiche_SFAR_Corticotherapie_Choc_Septique_SDRA_2000.pdf")
OUT = os.path.abspath(OUT)

SOURCE_TXT = ("Source : XXe Conférence de Consensus en Réanimation et Médecine d'Urgence "
              "« Corticothérapie au cours du choc septique et du SDRA » — SFAR/SPILF/SPLF/"
              "GFRUP, 12/10/2000, labellisée ANAES. Fiche de synthèse non officielle : se "
              "référer au texte intégral.")

# Extension locale de GRADE_COLORS - codes propres a ce document (voir docstring).
GRADE_COLORS["1a"] = (NAVY, WHITE)
GRADE_COLORS["1b"] = (NAVY, WHITE)
GRADE_COLORS["2a"] = (TEAL_DARK, WHITE)
GRADE_COLORS["2b"] = (TEAL_DARK, WHITE)
GRADE_COLORS["2"] = (TEAL_DARK, WHITE)
GRADE_COLORS["a"] = (GREY, WHITE)
GRADE_COLORS["b"] = (GREY, WHITE)
GRADE_COLORS["c"] = (GREY, WHITE)
GRADE_COLORS["N.C."] = (GREY_LIGHT, GREY)


def P(txt, style=S_CELL):
    return Paragraph(txt, style)


def chip(label):
    w = 15 * mm if len(label) <= 2 else 18 * mm
    return grade_chip(label, width=w, fontsize=7.6 if len(label) > 2 else 8.4)


def reco_table(rows, col_widths):
    """rows: (ref, text, code_label)"""
    data = [[P("Réf.", S_HEAD_W), P("Recommandation / constat du jury", S_HEAD_W), P("Cotation", S_HEAD_W_C)]]
    for ref, txt, code in rows:
        data.append([P(ref, S_CELL_B), P(txt, S_CELL), chip(code)])
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


def legend_flowable():
    items = [("1a", "Niveau 1 + preuve a"), ("2a", "Niveau 2 + preuve a"),
             ("2", "Niveau 2 seul"), ("a", "Preuve a seule"), ("N.C.", "Non coté")]
    content_w = PAGE_W - 2 * MARGIN
    n = len(items)
    chip_w = 15.5 * mm
    text_w = (content_w - n * chip_w) / n
    row_cells, col_widths = [], []
    for g, txt in items:
        row_cells.append(chip(g))
        row_cells.append(P(txt, S_BADGE_HEAD))
        col_widths += [chip_w, text_w]
    row = Table([row_cells], colWidths=col_widths)
    row.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                              ("LEFTPADDING", (0, 0), (-1, -1), 1), ("RIGHTPADDING", (0, 0), (-1, -1), 1)]))
    return row


TOTAL_PAGES = {"n": 3}


def on_page(canvas, doc, page_title):
    header_band(canvas, doc, "SFAR/SPILF/SPLF/GFRUP — CONFÉRENCE DE CONSENSUS 2000 — FICHE DE SYNTHÈSE",
                "Corticothérapie : choc septique & SDRA",
                page_title, icon_fn=lambda c, x, y: icon_pill(c, x, y, 13 * mm), color=TEAL_DARK)
    footer_band(canvas, doc, SOURCE_TXT, f"Page {doc.page} / {TOTAL_PAGES['n']}")


# ---------------------------------------------------------------------------
def _section_intro():
    story = [Spacer(1, 3 * mm)]
    story.append(info_panel(P(
        "<b>Champ de la conférence :</b> place des glucocorticoïdes (GC) dans le choc "
        "septique et le syndrome de détresse respiratoire aiguë (SDRA) — traitement "
        "discuté depuis 30 ans au moment de la conférence. XXe Conférence de Consensus "
        "en Réanimation et Médecine d'Urgence, 12 octobre 2000, organisée sous l'égide "
        "de la SFAR avec la SPILF, la SPLF et le GFRUP, labellisée par l'ANAES. Jury "
        "présidé par F. Fourrier (Lille). <b>5 questions</b> couvrant : (1) manifestations "
        "du SDRA accessibles à la corticothérapie, (2) conséquences surrénaliennes et "
        "vasculaires du choc septique, (3) bénéfices/risques attendus, (4) indications "
        "et modalités dans le choc septique, (5) indications et modalités dans le SDRA."
        "<br/><br/>"
        "<b>Méthodologie de cotation — non-GRADE :</b> chaque conclusion du jury combine, "
        "quand elle est disponible, un <b>niveau de recommandation</b> (1 = preuves "
        "scientifiques indiscutables ; 2 = preuves scientifiques + soutien consensuel des "
        "experts ; 3 = non reposant sur des preuves adéquates mais soutenu par les données "
        "disponibles et l'opinion des experts) et un <b>niveau de preuve bibliographique</b> "
        "sous-jacent (a = essais prospectifs contrôlés randomisés ; b = études non "
        "randomisées ou comparaisons de cohortes ; c = mises au point/revues/séries de cas ; "
        "d = publications d'opinion). <b>Aucune phrase du corps du texte ne porte le "
        "niveau « 3 » ni la preuve « d »</b> — l'échelle les prévoit mais ils ne sont "
        "concrètement utilisés nulle part dans ce document (constat par lecture "
        "exhaustive, non une omission de cette fiche).", S_BODY), bg=BG_PANEL, border=TEAL))
    story.append(Spacer(1, 2 * mm))
    story.append(section_bar("Légende des cotations (codes imprimés tels quels par le jury)"))
    story.append(Spacer(1, 2 * mm))
    story.append(legend_flowable())
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "Un chip à deux caractères (« 1a », « 2b »…) reprend le code exact imprimé pour "
        "cette phrase précise — jamais la fusion de deux phrases distinctement cotées. "
        "Un chip à un seul caractère correspond à une phrase qui ne porte que l'un des "
        "deux axes dans le texte source. « N.C. » signale un passage du texte source qui "
        "ne porte aucun code entre crochets — voir encart Question 4.", S_NOTE))
    return story


def _section_q1_q2():
    story = [Spacer(1, 1.5 * mm)]
    story.append(section_bar("Question 1 — Manifestations du SDRA accessibles à la corticothérapie"))
    story.append(Spacer(1, 2 * mm))
    story.append(reco_table([
        ("1.1", "Les phénomènes des phases exsudative (phase 1) et de fibrose évoluée "
                "endo-alvéolaire/interstitielle (phase 3) du SDRA ne justifient pas de "
                "corticothérapie.", "1a"),
        ("1.2", "La phase fibro-proliférative (à partir du 7<sup>e</sup> jour environ) ne "
                "justifie un traitement que dans deux situations : intensité excessive de "
                "la réponse, ou durée anormalement prolongée (« late ARDS »).", "2a"),
    ], [11 * mm, PAGE_W - 2 * MARGIN - 11 * mm - 18 * mm, 18 * mm]))
    story.append(Spacer(1, 2 * mm))
    story.append(P(
        "Physiopathologie (preuve seule) : la phase fibro-proliférative est un processus de "
        "réparation qui aboutit habituellement à la restauration d'une architecture pulmonaire "
        "normale (b), initié de façon concomitante au processus lésionnel dans un SDRA "
        "dynamique et hétérogène dans l'espace et le temps (b). Éléments de contexte non "
        "formulés comme recommandations graduées (preuve seule) : la persistance/progression "
        "de la phase fibro-proliférative se traduit par une dégradation de la compliance, une "
        "altération de l'oxygénation et une aggravation du lung injury score (LIS), sans valeur "
        "prédictive initiale (b) ; aucun signe radiologique spécifique n'existe, l'absence "
        "d'amélioration radiologique étant seulement évocatrice (b) ; la fièvre/hyperleucocytose "
        "de cette phase peut simuler un sepsis et s'associer à une défaillance multiviscérale "
        "(c) ; l'utilité pronostique des marqueurs biologiques plasmatiques/du LBA est limitée "
        "par de nombreux facteurs (1b) — certains marqueurs encore en cours d'évaluation "
        "semblent toutefois avoir une valeur péjorative (b) ; il ne faut pas transposer le "
        "modèle de la dysplasie broncho-pulmonaire du prématuré au SDRA du nourrisson (1b).",
        S_NOTE))
    story.append(Spacer(1, 2 * mm))

    story.append(section_bar("Question 2 — Conséquences surrénaliennes et vasculaires du choc septique"))
    story.append(Spacer(1, 2 * mm))
    story.append(reco_table([
        ("2.1", "Doser systématiquement la cortisolémie avant de débuter un traitement par "
                "GC, pour dépister les rares insuffisances surrénales (IS) absolues — seuil "
                "proposé par le jury faute de valeur validée : cortisolémie de base "
                "&lt; 10 µg/dl (≈ 275 nmol/L).", "2"),
        ("2.2", "Ne pas réaliser systématiquement de test au Synacthène (ACTH) : la réponse "
                "normale n'est pas clairement définie au cours du choc septique et son "
                "résultat n'influence pas la conduite thérapeutique.", "N.C."),
        ("2.3", "En cas d'urgence absolue (ex. purpura fulminans), débuter le traitement par "
                "GC sans attendre le dosage préalable de la cortisolémie.", "N.C."),
    ], [11 * mm, PAGE_W - 2 * MARGIN - 11 * mm - 18 * mm, 18 * mm]))
    story.append(Spacer(1, 2 * mm))
    story.append(P(
        "2.2 et 2.3 ne portent aucun code entre crochets dans le texte source, contrairement "
        "au reste de cette question — reproduites ici comme recommandations du jury (texte "
        "explicite « le jury recommande/ne recommande pas ») avec un chip « N.C. » plutôt "
        "qu'une cotation inventée. Contexte (preuve seule) : le choc septique peut associer "
        "IS absolue (rare chez l'adulte), réponse surrénalienne adaptée, ou IS « relative » "
        "(cortisolémie de base normale/élevée sans réponse à l'ACTH, incidence 6–75 % selon "
        "le seuil retenu) ; la réponse vasculaire diminuée aux catécholamines endogènes "
        "impliquerait une désensibilisation des récepteurs α/β que les GC restaureraient "
        "expérimentalement (b).", S_NOTE))
    return story


def _section_q3():
    story = [Spacer(1, 2 * mm)]
    story.append(section_bar("Question 3 — Bénéfices attendus et risques de la corticothérapie"))
    story.append(Spacer(1, 2 * mm))
    story.append(reco_table([
        ("3.1", "Il n'existe aucun bénéfice à un traitement précoce par GC au cours du "
                "SDRA (contrairement à leur administration en cas de fibroprolifération "
                "prolongée et/ou excessive).", "a"),
        ("3.2", "Dans le choc septique, seule l'utilisation de faibles doses d'hydrocortisone "
                "est bénéfique : diminution attendue de la mortalité, amélioration "
                "hémodynamique (baisse de la fréquence cardiaque, hausse des résistances "
                "artérielles systémiques et de la pression artérielle moyenne) permettant un "
                "sevrage plus rapide des amines vasoactives.", "a"),
        ("3.3", "Avant de débuter la corticothérapie (SDRA comme choc septique), rechercher "
                "systématiquement une infection ; en cas d'infection bactérienne, prescrire "
                "une antibiothérapie adaptée au moins 3 jours avant de débuter les GC.", "2"),
        ("3.4", "Surveiller la glycémie pendant toute la durée du traitement par GC "
                "(intolérance glucidique, en particulier chez l'enfant).", "2"),
    ], [11 * mm, PAGE_W - 2 * MARGIN - 11 * mm - 18 * mm, 18 * mm]))
    story.append(Spacer(1, 2 * mm))
    story.append(P(
        "Risques (contexte, non formulés en recommandation graduée) : à doses cumulatives "
        "élevées, la corticothérapie augmente le risque infectieux — les faibles doses "
        "cumulatives d'hydrocortisone du choc septique ne semblent pas majorer ce risque ; "
        "l'absence de fièvre sous traitement ne permet pas d'éliminer une infection, en "
        "particulier pulmonaire (b) ; le risque d'hémorragie digestive ne semble pas accru "
        "(données prospectives insuffisantes) ; risque de neuromyopathie pour des doses "
        "cumulatives &gt; 1000–1500 mg de méthylprednisolone (MP), le plus souvent associées "
        "aux curares.", S_NOTE))
    return story


def _section_q4():
    story = [Spacer(1, 2 * mm)]
    story.append(section_bar("Question 4 — Indications et modalités dans le choc septique"))
    story.append(Spacer(1, 2 * mm))
    story.append(info_panel(P(
        "<b>Anomalie source disclosée :</b> à la différence des questions 1 à 3, "
        "<b>aucune phrase de cette question ne porte de code entre crochets</b> dans le "
        "texte source — le protocole ci-dessous est la reproduction fidèle du texte du "
        "jury, présenté ici avec un chip « N.C. » (non coté) plutôt qu'une cotation "
        "inventée.", S_BODY_SM), bg=GREY_LIGHT, border=GREY))
    story.append(Spacer(1, 2 * mm))
    story.append(reco_table([
        ("4.1", "Indication : choc septique de gravité particulière, nécessitant des doses "
                "élevées et/ou croissantes d'agents vaso-actifs du fait d'une hypotension "
                "persistante malgré un remplissage vasculaire jugé satisfaisant. Avant "
                "traitement : s'assurer du caractère approprié de l'antibiothérapie et de "
                "l'absence d'indication chirurgicale d'éradication d'un foyer infectieux — le "
                "traitement peut alors être instauré, y compris plusieurs jours après "
                "l'installation du choc.", "N.C."),
        ("4.2", "Posologie : hémisuccinate d'hydrocortisone 200 à 300 mg/j, en perfusion "
                "continue ou répartis en 3–4 injections IV, après prélèvement pour dosage de "
                "cortisol (des inducteurs enzymatiques/substrats du cytochrome P3A4 peuvent "
                "modifier le taux sanguin). Chez l'enfant : 100 mg/m²/j en 4 injections/6h, "
                "dès que possible en cas de purpura fulminans.", "N.C."),
        ("4.3", "Durée : au moins 5 jours en cas de réponse clinique, avec réduction "
                "progressive puis arrêt à la disparition des signes de choc (sauf "
                "exceptionnelles IS absolues). Au-delà de 72 h sans réponse hémodynamique "
                "(hausse de la PA, stabilisation/sevrage des vaso-actifs), arrêter le "
                "traitement.", "N.C."),
        ("4.4", "Surveillance : glycémie, natrémie, kaliémie. La modification des signes "
                "systémiques d'inflammation sous GC peut masquer une surinfection.", "N.C."),
    ], [11 * mm, PAGE_W - 2 * MARGIN - 11 * mm - 18 * mm, 18 * mm]))
    return story


def _section_q5_sources():
    story = [Spacer(1, 2 * mm)]
    story.append(section_bar("Question 5 — Indications et modalités dans le SDRA"))
    story.append(Spacer(1, 2 * mm))
    story.append(reco_table([
        ("5.1", "Une corticothérapie n'est indiquée ni en prévention d'un SDRA, ni à la "
                "phase initiale de son évolution ; à ce stade, elle augmente l'incidence des "
                "infections et le taux de mortalité.", "1a"),
        ("5.2", "Une corticothérapie peut se discuter à la phase fibro-proliférative, chez un "
                "nombre restreint de patients : SDRA évoluant depuis 7 jours au moins, avec "
                "LIS ≥ 2,5, sans amélioration malgré une prise en charge adéquate.", "2a"),
        ("5.3", "Aucun marqueur biologique validé ne permet de poser l'indication des GC à ce "
                "stade.", "a"),
        ("5.4", "Une biopsie pulmonaire systématique n'est pas justifiée avant l'instauration "
                "des GC (risques non négligeables et absence de bénéfice documenté).", "2b"),
        ("5.5", "Posologie : méthylprednisolone (MP) 2 mg/kg/j en 4 injections IV, débutée "
                "entre le 7<sup>e</sup> et le 10<sup>e</sup> jour d'évolution du SDRA, "
                "poursuivie 3 à 4 semaines puis arrêtée progressivement (risque de rebond). "
                "Amélioration attendue entre le 5<sup>e</sup> et le 14<sup>e</sup> jour "
                "(clinique, LIS en baisse de plus d'1 point, régression des défaillances "
                "viscérales) ; recherche systématique d'une infection surajoutée pendant tout "
                "le traitement. Chez le nourrisson/l'enfant : protocole identique proposé, en "
                "l'absence de données spécifiques exploitables.", "N.C."),
    ], [11 * mm, PAGE_W - 2 * MARGIN - 11 * mm - 18 * mm, 18 * mm]))
    story.append(Spacer(1, 2 * mm))
    story.append(P(
        "5.3 (preuve seule, « a ») et 5.4 (recommandation graduée « 2b ») sont deux phrases "
        "consécutives du texte source portant deux cotations distinctes — reproduites ici en "
        "deux lignes séparées plutôt que fusionnées en un seul chip composite. 5.5 ne porte "
        "aucun code entre crochets dans le texte source (même anomalie qu'à la Question 4).",
        S_NOTE))
    story.append(Spacer(1, 4 * mm))

    story.append(section_bar("Sources et traçabilité", color=GREY))
    story.append(Spacer(1, 2 * mm))
    story.append(P(
        "<b>Document source :</b> XXe Conférence de Consensus en Réanimation et Médecine "
        "d'Urgence « Corticothérapie au cours du choc septique et du SDRA », 12 octobre 2000. "
        "Jury présidé par F. Fourrier (Lille) ; coordonnateur du Bureau du Consensus : "
        "F. Saulnier (Lille). Organisée par la SFAR avec la Société de Pathologie Infectieuse "
        "de Langue Française, la Société de Pneumologie de Langue Française et le Groupe "
        "Francophone de Réanimation et Urgences Pédiatriques. Conférence labellisée par "
        "l'ANAES (Agence Nationale d'Accréditation et d'Évaluation en Santé).",
        S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>Méthodologie :</b> cotation à deux axes indépendants — niveau de recommandation "
        "(1/2/3) et niveau de preuve bibliographique (a/b/c/d) — non-GRADE. Voir légende "
        "page 1. Niveau « 3 » et preuve « d » définis par l'échelle mais non utilisés dans le "
        "corps du texte.", S_SOURCE))
    story.append(P(
        "<b>URL source :</b> https://sfar.org/corticotherapie-au-cours-du-choc-septique-et-du-sdra/",
        S_SOURCE))
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Avertissement :</b> ce document est une fiche de synthèse indépendante, produite "
        "pour un usage d'aide-mémoire. Il reprend l'intégralité des recommandations et "
        "constats gradués des 5 questions de la conférence de consensus, mais ne remplace pas "
        "le texte intégral (argumentaire complet, références bibliographiques) et n'est ni "
        "édité ni validé par la SFAR. Conférence de 2000 : se référer également, en "
        "complément, aux données et pratiques plus récentes sur la corticothérapie du choc "
        "septique (ex. essais randomisés postérieurs à cette conférence) et à un avis "
        "spécialisé en cas de doute.",
        S_BODY_SM), bg=GREY_LIGHT, border=GREY))
    return story


def _section_1():
    return (_section_intro() + [Spacer(1, 1.5 * mm)] + _section_q1_q2()
            + [Spacer(1, 3 * mm)] + _section_q3())


def _section_2():
    return _section_q4() + [Spacer(1, 3 * mm)] + _section_q5_sources()


SECTIONS = [
    ("Introduction, méthodologie & Questions 1-3", _section_1),
    ("Question 4-5 — Protocoles pratiques & traçabilité", _section_2),
]


def _make_doc(path=None):
    return SimpleDocTemplate(path or OUT, pagesize=A4,
                              leftMargin=MARGIN, rightMargin=MARGIN,
                              topMargin=32 * mm, bottomMargin=16 * mm,
                              title="Fiche SFAR 2000 - Corticothérapie choc septique et SDRA",
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
    # Throwaway measurement builds must NEVER write to OUT (see CLAUDE.md) - reusing OUT
    # here was found in a prior fiche to silently corrupt page 1's header_band in the final
    # build. Always use a fresh tempfile.mktemp() path for these measurement passes.
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
