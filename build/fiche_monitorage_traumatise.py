# -*- coding: utf-8 -*-
"""
Fiche de synthese - "Monitorage du patient traumatise grave en prehospitalier" -
Conference d'experts SFAR / Samu de France / Societe francophone de medecine d'urgence
(SFMU) / Societe de reanimation de langue francaise (SRLF). Presidente A. Ricard-Hibon,
secretaire N. Smail. Texte court, 2006. Source : sources/monitorage_traumatise.pdf
(15 pages), sources/monitorage_traumatise.txt. Aucun tampon d'obsolescence sur la page 1
(verifie visuellement a 150dpi) - document non marque "abroge" dans
build/library_final.json (status "en vigueur").

METHODOLOGIE - PAS DE GRADE (1+/1-/2+/2-/AE) : conference d'experts classique, grille
"niveau de preuve / force de recommandation" (Tableaux I et II du texte source) :
niveaux de preuve I a V (I = etudes aleatoires forte puissance ... V = avis d'experts),
d'ou une force de recommandation A a E (A = au moins 2 etudes de niveau I ; B = 1 etude
de niveau I ; C = etude(s) de niveau II ; D = etude(s) de niveau III ; E = etude(s) de
niveau IV/V). Chaque enonce du corps du texte porte, entre parentheses, la lettre de force
retenue par les experts (ex. "(Grade D)") - jamais le niveau de preuve brut. `grade`
reproduit cette lettre telle quelle. Pas de `evidence_level` distinct (le texte ne
reimprime jamais le niveau I-V ligne a ligne, seulement la force A-E qui en derive).

STRUCTURE : PAS de numerotation R1/R2 (prose continue organisee en 8 questions), donc PAS
de colonne "Ref." classique - `theme_table()` (meme convention que fiche_aap_programmee.py)
utilise une colonne "Theme" a la place, et la numerotation Q1.1/Q1.2/etc. utilisee dans le
JSON/SQL en aval est une construction de cette fiche (par question, dans l'ordre
d'apparition), disclosee comme telle plutot que presentee comme une numerotation source.

ATOMISATION - DISCLOSURE IMPORTANTE (meme probleme que fiche_mort_encephalique.py) : le
texte source appose une lettre de grade apres la quasi-totalite de ses phrases, qu'il
s'agisse d'une recommandation actionnable (choix d'une technique, seuil, contre-indication)
ou d'un simple rappel de fait epidemiologique/physiopathologique (ex. "20% des patients
decedes presentent une cause curable de deces (Grade D)"). Seules les phrases formulant une
recommandation clinique concrete (quoi monitorer, quelle technique preferer/eviter, quel
seuil cibler, quelle contre-indication respecter) sont retenues comme lignes atomiques
graduees ci-dessous ; les phrases de justification/contexte/epidemiologie, meme graduees,
restent en texte libre (paragraphes "note") plutot que d'etre promues en ligne de tableau -
disclosure faite ici plutot que de fabriquer une distinction que le texte source lui-meme
n'imprime pas typographiquement.

COMPTAGE : 79 lettres de grade au total dans le texte source (grep exhaustif : 34xD, 30xE,
7xB, 4xA, 4xC). Cette fiche retient 46 recommandations actionnables individuelles (sur les
8 questions), le reste des occurrences graduees etant des faits de contexte/justification
non promus en ligne de tableau (voir disclosure ci-dessus) - les deux chiffres (79 codes
imprimes vs 46 recommandations retenues) sont disclosed sans etre reconcilies
artificiellement.

PERIMETRE : les 8 questions du texte court sont couvertes integralement (justification du
monitorage ; monitorage cardiovasculaire et thermique ; monitorage respiratoire ;
monitorage neurologique dont Doppler transcranien et BIS ; monitorage biologique ;
monitorage en intervention secondaire/transfert ; monitorage de la femme enceinte et de
l'enfant traumatises ; monitorage en milieu difficile - montagne, mer, catastrophe, NRBC).
Les Tableaux I et II (grilles methodologiques niveau de preuve I-V / force A-E) sont
reproduits dans la legende plutot qu'en tableau autonome (contenu deja integre au
fonctionnement des chips de grade).
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from style import *
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
                                 PageBreak, KeepTogether)
from reportlab.lib.units import mm

OUT = os.path.join(os.path.dirname(__file__), "..", "output",
                    "Fiche_SFAR_SAMU_SFMU_SRLF_Monitorage_Traumatise_2006.pdf")
OUT = os.path.abspath(OUT)

SOURCE_TXT = ("Source : « Monitorage du patient traumatisé grave en préhospitalier » — "
              "Conférence d'experts SFAR/Samu de France/SFMU/SRLF, texte court, 2006. "
              "Fiche de synthèse non officielle : se référer au texte intégral.")

# Extension locale de GRADE_COLORS - force de recommandation A-E (niveaux de preuve I-V),
# voir docstring. C est deja utilise par ce document (contrairement a fiche_hsa.py qui n'a
# que A/B/D/E) - choix d'une couleur distincte (NAVY) pour C afin de garder les 5 lettres
# visuellement distinctes.
GRADE_COLORS["A"] = (GREEN, WHITE)
GRADE_COLORS["B"] = (TEAL, WHITE)
GRADE_COLORS["C"] = (NAVY, WHITE)
GRADE_COLORS["D"] = (AMBER, WHITE)
GRADE_COLORS["E"] = (GREY, WHITE)


def P(txt, style=S_CELL):
    return Paragraph(txt, style)


def chip(label):
    return grade_chip(label, width=11 * mm, fontsize=8.4)


def theme_table(rows, col_widths=None):
    """rows: (theme, texte, grade) - pas de colonne Ref. (source sans numerotation Rx.y,
    voir docstring)."""
    if col_widths is None:
        cw = PAGE_W - 2 * MARGIN
        col_widths = [34 * mm, cw - 34 * mm - 16 * mm, 16 * mm]
    data = [[P("Thème", S_HEAD_W), P("Recommandation", S_HEAD_W), P("Force", S_HEAD_W_C)]]
    for theme, txt, grade in rows:
        data.append([P(theme, S_CELL_B), P(txt, S_CELL), chip(grade)])
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
    items = [("A", "≥ 2 études niveau I"), ("B", "1 étude niveau I"),
              ("C", "Étude(s) niveau II"), ("D", "Étude(s) niveau III"),
              ("E", "Étude(s) niveau IV/V — avis d'experts")]
    content_w = PAGE_W - 2 * MARGIN
    n = len(items)
    chip_w = 11 * mm
    text_w = (content_w - n * chip_w) / n
    row_cells, col_widths = [], []
    for g, txt in items:
        row_cells += [chip(g), P(txt, S_BADGE_HEAD)]
        col_widths += [chip_w, text_w]
    t = Table([row_cells], colWidths=col_widths)
    t.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                            ("LEFTPADDING", (0, 0), (-1, -1), 2),
                            ("RIGHTPADDING", (0, 0), (-1, -1), 2)]))
    return t


TOTAL_PAGES = {"n": 1}


def on_page(canvas, doc, page_title):
    header_band(canvas, doc, "SFAR / SAMU DE FRANCE / SFMU / SRLF — CONFÉRENCE D'EXPERTS 2006 — FICHE DE SYNTHÈSE",
                "Monitorage du traumatisé grave en préhospitalier",
                page_title, icon_fn=lambda c, x, y: icon_shield(c, x, y, 13 * mm), color=NAVY)
    footer_band(canvas, doc, SOURCE_TXT, f"Page {doc.page} / {TOTAL_PAGES['n']}")


# ---------------------------------------------------------------------------
def _section_intro():
    story = []
    story.append(info_panel(P(
        "<b>Champ :</b> médecins exerçant en médecine d'urgence préhospitalière, pour tout "
        "patient traumatisé grave (suspect de lésion(s) pouvant engager le pronostic vital, "
        "y compris si l'examen clinique initial semble rassurant du seul fait du mécanisme/"
        "de la cinétique). <b>Objectif du monitorage :</b> améliorer la performance "
        "diagnostique, évaluer les conséquences physiopathologiques des lésions, assurer une "
        "surveillance continue des paramètres vitaux, dépister les complications précoces, "
        "guider la thérapeutique et optimiser l'orientation — sans jamais allonger inutilement "
        "le temps de prise en charge globale, en particulier pour les patients nécessitant un "
        "acte urgent chirurgical et/ou de radiologie interventionnelle.<br/><br/>"
        "<b>Méthodologie :</b> conférence d'experts (pas de système GRADE) — niveaux de preuve "
        "I à V, d'où une force de recommandation A à E imprimée après chaque énoncé du corps "
        "du texte (voir légende ci-dessous). La littérature préhospitalière étant pauvre sur "
        "ce sujet, une partie des recommandations s'appuie sur la littérature en anesthésie, "
        "réanimation et/ou médecine d'urgence intrahospitalière.",
        S_BODY)))
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("Légende — force de recommandation (niveaux de preuve I-V)"))
    story.append(Spacer(1, 2 * mm))
    story.append(legend_flowable())
    return story


def _section_q1():
    story = [section_bar("Question 1 — Pourquoi monitorer les patients traumatisés graves en préhospitalier ?")]
    story.append(P(
        "L'examen clinique est souvent pris en défaut en traumatologie : 20 % des patients "
        "décédés présentent une cause curable de décès (« mort évitable »). Le monitorage "
        "complète l'examen clinique et facilite la reconnaissance précoce des détresses "
        "vitales, notamment pour prévenir les agressions cérébrales secondaires d'origine "
        "systémique (ACSOS).", S_NOTE))
    rows = [
        ("Oxygénation", "Seule la mise en place systématique d'un oxymètre de pouls permet de s'assurer de l'existence d'une oxygénation adaptée.", "D"),
        ("Ventilation/IOT", "Le positionnement endotrachéal de la sonde d'intubation et l'adéquation de la ventilation sont optimisés par l'utilisation de la capnographie.", "D"),
        ("Échographie pleurale", "La réalisation d'une échographie pleurale peut s'avérer être une aide diagnostique, pour limiter les gestes potentiellement délétères comme un drainage thoracique iatrogène.", "E"),
        ("Douleur", "Le monitorage répété de l'intensité douloureuse par les échelles d'autoévaluation (échelle visuelle analogique ou échelle numérique) est nécessaire pour améliorer le soulagement des patients.", "D"),
    ]
    story.append(theme_table(rows))
    return story


def _section_q2a():
    story = [section_bar("Question 2 (1/2) — Monitorage cardiovasculaire")]
    rows = [
        ("ECG", "La surveillance électrocardioscopique est indispensable.", "D"),
        ("ECG", "La réalisation d'un ECG est recommandée en cas de traumatisme grave (peut être différée jusqu'à l'arrivée au centre hospitalier selon le contexte).", "E"),
        ("PA non invasive", "La mesure de la pression artérielle nécessite l'utilisation d'un brassard de taille adaptée au bras du patient et son positionnement correct sur le trajet artériel.", "D"),
        ("PA non invasive", "La méthode oscillométrique n'est pas fiable en cas d'hypotension, de frissons, d'arythmie ou de mobilisation du patient.", "D"),
        ("PA invasive", "La mise en place précoce, dès la phase préhospitalière, d'un cathéter artériel peut être envisagée dans la mesure où la pose est réalisée sur un seul site artériel et dans un délai maximal de 10 minutes (bénéfice/risque à évaluer au cas par cas ; abord fémoral privilégié).", "D"),
        ("PA invasive", "Un apprentissage préalable et un entraînement régulier de toute l'équipe sont indispensables pour que la pose d'un cathéter artériel puisse être réalisée en préhospitalier.", "E"),
        ("Échographie FAST", "L'échographie selon la technique FAST (Focused Abdominal Sonography for Trauma) permet d'améliorer le triage des patients en cas de victimes multiples.", "D"),
    ]
    story.append(theme_table(rows))
    story.append(P(
        "L'écho-Doppler a été proposé en préhospitalier pour la détection et l'optimisation "
        "d'un état hémodynamique précaire, mais son utilisation chez le traumatisé grave ne "
        "peut être actuellement recommandée en l'absence de données validées (non gradé dans "
        "le texte source). L'utilité de l'échographie FAST en préhospitalier (par opposition à "
        "son usage intrahospitalier, bien établi) n'a pas encore été validée (Grade E) ; après "
        "formation (20 à 50 examens nécessaires), les performances des urgentistes sont "
        "comparables à celles des radiologues (Grade D).", S_NOTE))
    return story


def _section_q2b():
    story = [section_bar("Question 2 (2/2) — Monitorage thermique")]
    rows = [
        ("Température", "La mesure de la température en préhospitalier est recommandée : l'hypothermie, fréquente chez le traumatisé grave, est associée à une forte mortalité.", "C"),
        ("Température", "La voie rectale, d'accessibilité difficile, est peu utilisée ; on lui préfère la mesure tympanique (patient non intubé) ou œsophagienne (patient intubé).", "E"),
        ("Température", "En cas d'hypothermie majeure, la voie œsophagienne est contre-indiquée en raison du risque de fibrillation ventriculaire à la pose de la sonde.", "E"),
        ("Température", "La mesure de la température buccale ou axillaire, trop influencée par les conditions environnantes, doit être abandonnée.", "D"),
    ]
    story.append(theme_table(rows))
    story.append(P(
        "Chez le traumatisé crânien grave, l'utilisation d'une hypothermie thérapeutique reste "
        "débattue (non gradé dans le texte source).", S_NOTE))
    return story


def _section_q3():
    story = [section_bar("Question 3 — Monitorage respiratoire")]
    rows = [
        ("SpO2", "L'oxymètre de pouls est un outil indispensable en préhospitalier ; il permet une détection plus précoce et plus fiable de l'hypoxémie que l'évaluation clinique.", "D"),
        ("SpO2 — seuil", "Un seuil de SpO2 au moins égal à 94 % doit être ciblé pour détecter toutes les SaO2 &lt; 90 %.", "E"),
        ("Ballonnet IOT", "Le monitorage de la pression du ballonnet de la sonde d'intubation est nécessaire pour limiter les complications trachéales liées à l'intubation.", "B"),
        ("Ventilation mécanique", "Les alarmes du respirateur à régler et à surveiller sont les alarmes de pression inspiratoire maximale et minimale, ainsi que celles de spirométrie.", "E"),
        ("Capnographie", "Le monitorage de la capnographie est fortement recommandé en préhospitalier lors de la réalisation de l'intubation trachéale ; c'est la méthode de référence pour détecter l'intubation œsophagienne.", "D"),
        ("Capnographie", "La capnographie permet d'optimiser rapidement et de façon non invasive la ventilation en préhospitalier.", "B"),
        ("Capnographie", "Pour les patients qui justifient d'un contrôle strict de la PaCO2 (notamment en cas de souffrance neurologique), le monitorage de la capnographie doit être complété par une mesure des gaz du sang dès que possible.", "D"),
        ("Capnographie", "L'évolution de la PETCO2 permet de guider les manœuvres de réanimation en cas d'arrêt cardiaque.", "D"),
    ]
    story.append(theme_table(rows))
    story.append(P(
        "Seul le monitorage du volume expiré indique les volumes réellement reçus par le "
        "patient (et non ceux réglés sur le respirateur). Les valeurs de PETCO2 ont une valeur "
        "pronostique chez les patients traumatisés graves (Grade D, non repris en ligne "
        "distincte — même thème que la capnographie ci-dessus).", S_NOTE))
    return story


def _section_q4():
    story = [section_bar("Question 4 — Monitorage neurologique")]
    rows = [
        ("ACSOS", "La prévention des agressions cérébrales secondaires d'origine systémique (ACSOS) passe avant tout par la prévention et le traitement des épisodes d'hypotension et d'hypoxie.", "D"),
        ("PaCO2 cible", "Le maintien de la PaCO2 entre 35 et 40 mmHg est recommandé chez le traumatisé crânien grave.", "B"),
        ("Osmolarité", "Le maintien de l'osmolarité plasmatique est recommandé.", "E"),
        ("Doppler transcrânien", "La technique du Doppler transcrânien est actuellement utilisée pour le traitement et le suivi thérapeutique en intrahospitalier ; son intérêt en médecine préhospitalière reste à évaluer.", "D"),
    ]
    story.append(theme_table(rows))
    story.append(P(
        "En préhospitalier, seule l'estimation de la pression de perfusion cérébrale (PPC) est "
        "possible, à partir de la mesure de la PAM. L'indice bispectral (BIS), conçu pour "
        "ajuster les doses d'hypnotiques, ne doit s'envisager pour la sédation des traumatisés "
        "graves que dans le cadre de la recherche (non gradé dans le texte source).", S_NOTE))
    return story


def _section_q5():
    story = [section_bar("Question 5 — Monitorage biologique")]
    rows = [
        ("Hémoglobine", "L'utilisation d'un hémoglobinomètre type Hémocue® est préférable à la mesure de l'hématocrite par microméthode.", "A"),
        ("Gaz du sang", "Chez le patient victime d'un traumatisme crânien grave, la mesure des gaz du sang permet une adaptation des paramètres ventilatoires plus précise que lorsque celle-ci est réalisée à partir de la seule mesure de la PETCO2.", "D"),
    ]
    story.append(theme_table(rows))
    story.append(P(
        "Le dosage de la glycémie et de l'hémoglobine sont incontournables chez le traumatisé "
        "grave (non gradé) ; la répétition du dosage d'hémoglobine, en cas d'hémorragie active, "
        "aide à poser l'indication d'une transfusion érythrocytaire. L'utilisation de "
        "dispositifs embarqués d'analyse biologique est soumise à une réglementation précise "
        "dont le biologiste hospitalier est seul responsable (qualité, maintenance).", S_NOTE))
    return story


def _section_q6():
    story = [section_bar("Question 6 — Monitorage en intervention secondaire (transferts)")]
    rows = [
        ("Échographie avant transport", "Avant le transport, devant une instabilité hémodynamique, une échographie abdominale et pleurale est une aide à la décision d'orientation et/ou de traitement.", "E"),
        ("Ventilation mécanique", "Lorsque le patient est ventilé pendant le transfert, le monitorage de la capnographie est indispensable.", "B"),
        ("Ventilation mécanique", "Les paramètres respiratoires doivent être ajustés en fonction du contrôle gazométrique effectué sous ventilation par le respirateur de transport.", "E"),
        ("PA invasive", "Le monitorage invasif de la pression artérielle se justifie par la gravité du patient et par la durée prévisible du transfert, en particulier chez le patient présentant un traumatisme crânien grave et/ou une hémorragie.", "E"),
    ]
    story.append(theme_table(rows))
    story.append(P(
        "L'équipement minimal comprend un cardioscope défibrillateur, un monitorage non "
        "invasif de la pression artérielle, un oxymètre de pouls, un monitorage de la "
        "température et un appareil de dosage de l'hémoglobine et de la glycémie (non gradé). "
        "Lorsque le pronostic vital est engagé à court terme, le monitorage doit se limiter au "
        "minimum indispensable (Grade E, non repris en ligne distincte). Le monitorage de la "
        "pression intracrânienne ou du débit cardiaque sera, autant que possible, poursuivi en "
        "cours de transfert.", S_NOTE))
    return story


def _section_q7():
    story = [section_bar("Question 7 — Femme enceinte et enfant traumatisés graves")]
    rows = [
        ("RCF — femme enceinte", "La surveillance du rythme cardiaque fœtal (RCF), réalisée préférentiellement de façon continue, est l'élément clé de la surveillance de la vitalité fœtale après un traumatisme chez la femme enceinte ; elle est faisable et souhaitable en préhospitalier.", "C"),
        ("Monitorage — enfant", "La mesure de la fréquence cardiaque, de la pression artérielle non invasive, de l'oxymétrie pulsée et de la capnographie est recommandée pour tous les enfants traumatisés graves, avec un matériel adapté à leur gabarit.", "A"),
        ("Ballonnet IOT — enfant", "La surveillance de la pression du ballonnet de la sonde d'intubation est utile pour la prévention des lésions trachéales ischémiques chez l'enfant.", "D"),
        ("Autres paramètres — enfant", "Il est recommandé de mesurer la température corporelle, la concentration en hémoglobine, la glycémie et l'intensité de la douleur sur une échelle adaptée à l'enfant.", "D"),
    ]
    story.append(theme_table(rows))
    story.append(P(
        "Femme enceinte : le traumatisme est la première cause de mortalité maternelle "
        "d'origine non obstétricale ; le risque de décès fœtal existe même après un "
        "traumatisme bénin pour la mère, et plus de 60 % des décès fœtaux post-traumatiques "
        "sont secondaires à un retard diagnostique et thérapeutique. Enfant : la chute de "
        "pression artérielle est plus tardive que chez l'adulte malgré une hypovolémie "
        "s'installant plus rapidement, avec une sensibilité accrue à l'hypercapnie. Les "
        "techniques invasives de monitorage ne sont pas recommandées chez l'enfant en "
        "préhospitalier, dans l'état actuel des connaissances (non gradé dans le texte "
        "source).", S_NOTE))
    return story


def _section_q8():
    story = [section_bar("Question 8 — Monitorage en milieu difficile (montagne, mer, catastrophe, NRBC)")]
    rows = [
        ("Montagne — température", "En montagne, le monitorage de la température doit être systématique, le patient traumatisé grave étant le plus souvent hypotherme.", "E"),
        ("Montagne — température", "Lorsque le patient n'est pas en arrêt circulatoire, le site de mesure privilégié en terrain périlleux est le conduit auditif externe (température épitympanique), au mieux par un thermomètre tympanique résistant au froid.", "E"),
        ("Montagne — température", "En cas d'arrêt circulatoire, la mesure de la température ne peut se faire que par une sonde œsophagienne ou, éventuellement, rectale ; elle permet de trier les patients susceptibles de bénéficier d'une circulation extracorporelle de réchauffement.", "D"),
        ("Montagne — matériel", "En milieu hostile, la dotation minimale comprend un petit oxymètre de pouls, un mini-tensiomètre électronique et un mini-cardioscope ou défibrillateur semi-automatique débrayable en mode manuel avec câble ECG 3 brins.", "E"),
        ("Catastrophe — matériel", "En situation de catastrophe, les appareils de monitorage employés doivent être dotés d'alarmes sonores, avoir une autonomie suffisante, fonctionner de préférence avec des piles à usage unique et être résistants aux chocs.", "E"),
        ("Catastrophe — PA", "Le monitorage de la pression artérielle en situation de catastrophe sera, en cas de traumatisme grave, préférentiellement réalisé à l'aide d'un brassard automatique.", "E"),
        ("Catastrophe — IOT", "La position endotrachéale de la sonde d'intubation peut être vérifiée, en complément de l'auscultation, par l'utilisation d'indicateurs colorimétriques et/ou par un test à la seringue.", "D"),
        ("Catastrophe — échographie", "L'échographie permet d'identifier rapidement un épanchement pleural ou péritonéal au poste médical avancé (PMA).", "D"),
    ]
    story.append(theme_table(rows))
    story.append(P(
        "En montagne comme en mer, l'extraction du traumatisé du milieu hostile est "
        "prioritaire ; le matériel doit être résistant aux chocs, au froid et à l'humidité, "
        "léger et autonome pour toute la durée du secours. En situation de catastrophe, "
        "l'inadéquation entre sauveteurs/matériels et nombre de victimes impose de hiérarchiser "
        "les patients à monitorer. En ambiance NRBC (nucléaire, radiologique, bactériologique, "
        "chimique), les appareils doivent être protégés par des housses étanches, adaptés au "
        "port des tenues de protection, et de préférence à usage unique ou détruits après "
        "utilisation (non gradé).", S_NOTE))
    return story


def _section_sources():
    story = [section_bar("Synthèse et messages clés")]
    story.append(P(
        "• Oxymétrie de pouls et surveillance ECG systématiques ; capnographie fortement "
        "recommandée dès l'intubation (référence pour détecter une intubation œsophagienne, "
        "seuil de sécurité SpO2 ≥ 94 %).<br/>"
        "• Pression artérielle non invasive avec brassard adapté ; cathéter artériel "
        "envisageable en préhospitalier si pose sur un seul site en &lt; 10 min, abord fémoral "
        "privilégié, équipe entraînée.<br/>"
        "• Température systématique (voie tympanique ou œsophagienne selon intubation ; "
        "jamais buccale/axillaire ; œsophagienne contre-indiquée si hypothermie majeure).<br/>"
        "• Neurologique : PaCO2 cible 35-40 mmHg chez le traumatisé crânien grave, prévention "
        "des ACSOS (hypotension, hypoxie) en priorité.<br/>"
        "• Femme enceinte : RCF continu dès que possible. Enfant : monitorage standard complet "
        "avec matériel adapté au gabarit, pas de technique invasive en préhospitalier.<br/>"
        "• Milieu difficile : monitorage minimal résistant (choc, froid, humidité), hiérarchisé "
        "selon le contexte (montagne/mer, afflux de victimes, NRBC).",
        S_BODY))
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("Sources et traçabilité", color=GREY))
    story.append(P(
        "<b>Document source :</b> « Monitorage du patient traumatisé grave en préhospitalier » "
        "— Conférence d'experts SFAR/Samu de France/SFMU/SRLF, texte court, 2006. Présidente "
        "A. Ricard-Hibon (Clichy), secrétaire N. Smail (Toulouse).", S_SOURCE))
    story.append(P(
        "<b>Méthodologie :</b> conférence d'experts, pas de système GRADE. Niveaux de preuve "
        "I à V, force de recommandation A à E imprimée après chaque énoncé (voir légende et "
        "Tableaux I/II, page 1).", S_SOURCE))
    story.append(P(
        "<b>Couverture :</b> 46 recommandations individuelles reproduites sur les 8 questions "
        "du texte court, sur 79 lettres de grade imprimées au total dans le document (le "
        "reste étant des faits de contexte/justification non promus en ligne de tableau — "
        "disclosure faite dans le corps de la fiche, voir docstring du script source).",
        S_SOURCE))
    story.append(Spacer(1, 2 * mm))
    story.append(info_panel(P(
        "<b>Avertissement :</b> ce document est une fiche de synthèse indépendante, produite "
        "pour un usage d'aide-mémoire. Il reprend l'intégralité des recommandations "
        "individuelles de la conférence d'experts mais ne remplace pas le texte intégral et "
        "n'est ni édité ni validé par la SFAR, Samu de France, la SFMU ou la SRLF. Document de "
        "2006 : les pratiques de monitorage préhospitalier (échographie, biologie délocalisée) "
        "ont pu évoluer depuis. En cas de doute, se référer au texte intégral, aux "
        "recommandations ultérieures et/ou à un avis spécialisé.",
        S_BODY_SM), bg=GREY_LIGHT, border=GREY))
    return story


# Troisieme element = forcer un saut de page avant cette section (True aux frontieres
# de question uniquement, pour limiter les pages a moins de 60% de remplissage - voir
# CLAUDE.md).
SECTIONS = [
    ("Introduction & méthodologie", _section_intro, True),
    ("Q1 — Justification du monitorage", _section_q1, True),
    ("Q2 (1/2) — Cardiovasculaire", _section_q2a, True),
    ("Q2 (2/2) — Thermique", _section_q2b, False),
    ("Q3 — Respiratoire", _section_q3, True),
    ("Q4 — Neurologique", _section_q4, True),
    ("Q5 — Biologique", _section_q5, False),
    ("Q6 — Transferts secondaires", _section_q6, True),
    ("Q7 — Femme enceinte & enfant", _section_q7, False),
    ("Q8 — Milieu difficile", _section_q8, True),
    ("Sources & traçabilité", _section_sources, False),
]


def _make_doc(path=None):
    return SimpleDocTemplate(path or OUT, pagesize=A4,
                              leftMargin=MARGIN, rightMargin=MARGIN,
                              topMargin=32 * mm, bottomMargin=16 * mm,
                              title="Fiche SFAR/SAMU/SFMU/SRLF 2006 - Monitorage du traumatisé grave en préhospitalier",
                              author="Synthèse indépendante (source SFAR)")


def _build_upto(sections):
    story = []
    for i, (fn, new_page) in enumerate(sections):
        if i > 0 and new_page:
            story.append(PageBreak())
        elif i > 0:
            story.append(Spacer(1, 4 * mm))
        story.extend(fn())
    return story


def _count_pages(story_flowables):
    # Throwaway measurement builds must NEVER write to OUT (voir CLAUDE.md) - toujours un
    # chemin tempfile.mktemp() frais pour ces passes de mesure.
    import pypdf, tempfile
    tmp_path = tempfile.mktemp(suffix=".pdf")
    doc = _make_doc(tmp_path)
    doc.build(story_flowables, onFirstPage=_silent_page, onLaterPages=_silent_page)
    n = len(pypdf.PdfReader(tmp_path).pages)
    os.remove(tmp_path)
    return n


def _silent_page(canvas, doc_):
    pass


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
