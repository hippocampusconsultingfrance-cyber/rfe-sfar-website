# -*- coding: utf-8 -*-
"""
Fiche de synthese - Conference de Consensus SFAR 2002 (Recommandations du Jury, texte
court, publie Ann Fr Anesth Reanim 2003;22:745-749) : "Prise en charge des voies
aeriennes en anesthesie adulte a l'exception de l'intubation difficile".
Source : sources/voies_aeriennes_adulte.pdf (5 pages), sources/voies_aeriennes_adulte.txt
(texte integral extrait par PyMuPDF). Pas de tampon d'obsolescence detecte sur la page 1
(verifie a la lecture integrale du texte) ; library_final.json marque ce document
"en vigueur", exact_type "CC", exact_date "2003".

CHAMP - EXCLUSION EXPLICITE (disclosee telle quelle dans le panneau d'introduction,
jamais omise silencieusement) : sont exclues de cette conference (i) la prise en charge
des voies aeriennes en medecine extrahospitaliere, (ii) en urgence medicale hospitaliere,
(iii) en anesthesie pediatrique, (iv) lors d'une ventilation a poumons separes, et bien
sur (v) l'intubation difficile elle-meme (deja couverte par une fiche separee de ce
corpus, fiche_intubation_difficile_adulte.py).

METHODOLOGIE - PAS DU GRADE (1+/1-/2+/2-) : la source utilise l'echelle ANAES A-E,
EXPLICITEMENT DEFINIE en page 1 du texte (contrairement a fiche_hsa.py ou l'echelle
A/B/D/E n'etait pas definie) :
  A : 2 (ou plus) etudes de niveau de preuve I
  B : une etude de niveau de preuve I
  C : etude(s) de niveau de preuve II
  D : une etude (ou plus) de niveau de preuve III
  E : etude(s) de niveau de preuve IV ou V
GRADE_COLORS etendu localement avec ces 5 lettres (meme precedent que fiche_hsa.py /
fiche_sepsis_hemodynamique.py), sans collision avec les cles GRADE 1+/2+/etc.

COMPTAGE DES RECOMMANDATIONS GRADEES - PIEGE METHODOLOGIQUE EVITE : un grep naif
ligne-par-ligne de "(Grade [A-E])" sur sources/voies_aeriennes_adulte.txt ne retourne
que 49 occurrences, car plusieurs occurrences sont coupees par un retour a la ligne
issu de la mise en page PDF a 2 colonnes (ex. "...hautement probable (Grade" / "D).").
Extraction correcte en reduisant tous les retours a la ligne/espaces multiples a un
espace simple avant recherche : 53 occurrences exactes (verifie par script Python
dedie). Repartition : 2x Grade A, 1x Grade B, 10x Grade C, 14x Grade D, 26x Grade E
(2+1+10+14+26 = 53). Chaque enonce grade est repris ici dans son theme clinique naturel
(Q1 a Q6 du texte source, 4/2/10/15/10/12 items respectivement) ; la reference "Qn.k" de
chaque ligne est une numerotation introduite par cette fiche pour la tracabilite (le
texte source est en prose continue narrative, sans numerotation R1/R2 propre).

ENONCES NON GRADES (disclosure, non fabriques) : plusieurs phrases informatives du
texte source ne portent AUCUN grade explicite entre parentheses et sont donc reproduites
ici comme texte de contexte (narratif, hors reco_table), jamais affublees d'un grade
invente - notamment : "les criteres paracliniques n'ont pas demontre leur interet dans
le depistage d'une ID" (Q1), le paragraphe entier sur la composition du plateau
d'intubation standard et sur la maintenance/hygiene reglementaire du materiel (Q2),
l'effet de l'esmolol 100 mg sur la tachycardie/hypertension peri-intubation (Q4, alors
que la phrase precedente sur la lidocaine IV est bien gradee E), et l'absence de donnees
suffisantes sur le tube laryngue pour en proposer l'usage clinique (Q5).

SAFETY-NET GRADE COMPOSITE : aucune cotation composite GRADE (deux chiffres 1 ou 2 suivis
d'un signe +/- de part et d'autre d'un slash) n'existe dans ce document (echelle A-E
uniquement) - le grep de securite du CLAUDE.md sur ce script renvoie 0 occurrence
(verifie avant commit, cf. CLAUDE.md regle #4).

PERIMETRE DE COUVERTURE : integralite des 6 questions du texte court (criteres
predictifs ID/VMD ; materiel et alternatives a la sonde d'intubation ; pre-oxygenation
et controle de la permeabilite des VAS ; agents d'induction IV/halogenes/morphiniques/
curares et monitorage ; positionnement et techniques d'intubation standard, controle de
la position du tube et du ballonnet, dispositifs alternatifs ; lesions liees a
l'intubation oro/nasotracheale et aux techniques alternatives, prevention de
l'inhalation bronchique). Aucun tableau de donnees ni figure dans ce texte court (texte
narratif continu uniquement, verifie a la lecture integrale) - pas de reproduction de
tableau/figure necessaire ici, a la difference de fiche_hsa.py.

_count_pages() : copie exacte du pattern fiche_hsa.py / fiche_aap_programmee.py, passe
au tempfile.mktemp() jamais a OUT (cf. bug CLAUDE.md etape 5).

AUDIT INDEPENDANT (pas d'outil Task/sous-agent disponible dans cet environnement -
auto-verification rigoureuse a la place, cf. CLAUDE.md point 3) : l'inventaire des 53
enonces gradés a ete reconstruit MECANIQUEMENT depuis sources/voies_aeriennes_adulte.txt
par un script Python dedie (regex sur le texte aplati, independant de la redaction de ce
fiche_*.py), AVANT redaction des lignes du reco_table. Diff final : extraction
automatique de tous les tuples (ref, ..., grade) de ce script et comparaison a la
sequence de grades issue de ce meme regex, question par question - concordance exacte
sur les 53 items (4x Q1, 2x Q2, 10x Q3, 15x Q4, 10x Q5, 12x Q6), aucun ecart, aucune
grade erronee, aucun doublon, aucun oubli.

ICONE : icon_pill, color=NAVY - meme convention que fiche_intubation_difficile_adulte.py
et fiche_voies_aeriennes_enfant.py (documents proches, coherence visuelle voulue, pas de
confusion possible malgre la proximite thematique car les 3 titres restent distincts).
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from style import *
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.units import mm

OUT = os.path.join(os.path.dirname(__file__), "..", "output",
                    "Fiche_SFAR_Voies_Aeriennes_Anesthesie_Adulte_2002.pdf")
OUT = os.path.abspath(OUT)

SOURCE_TXT = ("Source : Conférence de Consensus SFAR — Recommandations du Jury, texte court, 2002 "
              "(publié Ann Fr Anesth Réanim 2003;22:745-749) — « Prise en charge des voies aériennes "
              "en anesthésie adulte à l'exception de l'intubation difficile ». Fiche de synthèse non "
              "officielle : se référer au texte intégral / argumentaire scientifique.")

# Extension locale de GRADE_COLORS - echelle ANAES A-E de cette source, explicitement
# definie en page 1 (voir docstring). Meme precedent que fiche_hsa.py.
GRADE_COLORS["A"] = (GREEN, WHITE)
GRADE_COLORS["B"] = (TEAL, WHITE)
GRADE_COLORS["C"] = (AMBER, WHITE)
GRADE_COLORS["D"] = (NAVY, WHITE)
GRADE_COLORS["E"] = (GREY, WHITE)


def P(txt, style=S_CELL):
    return Paragraph(txt, style)


def chip(label):
    return grade_chip(label, width=13 * mm, fontsize=8.6)


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


def legend_flowable():
    items = [("A", "≥ 2 études de niveau de preuve I"),
             ("B", "1 étude de niveau de preuve I"),
             ("C", "étude(s) de niveau de preuve II"),
             ("D", "≥ 1 étude de niveau de preuve III"),
             ("E", "étude(s) de niveau de preuve IV ou V")]
    content_w = PAGE_W - 2 * MARGIN
    n = len(items)
    chip_w = 13 * mm
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


TOTAL_PAGES = {"n": 1}


def on_page(canvas, doc, page_title):
    header_band(canvas, doc, "SFAR — CONFÉRENCE DE CONSENSUS 2002 (TEXTE COURT)",
                "Voies aériennes en anesthésie adulte",
                page_title, icon_fn=lambda c, x, y: icon_pill(c, x, y, 13 * mm), color=NAVY)
    footer_band(canvas, doc, SOURCE_TXT, f"Page {doc.page} / {TOTAL_PAGES['n']}")


# ---------------------------------------------------------------------------
def _section_intro():
    story = [Spacer(1, 3 * mm)]
    story.append(info_panel(P(
        "<b>Champ :</b> prise en charge des voies aériennes en anesthésie adulte "
        "(intubation standard, alternatives à la sonde d'intubation). "
        "<b>Exclusions explicites de cette conférence</b> (disclosées telles quelles, "
        "jamais omises) : la prise en charge des voies aériennes réalisée en <b>médecine "
        "extrahospitalière</b>, en <b>urgence médicale hospitalière</b>, en <b>anesthésie "
        "pédiatrique</b>, lors d'une <b>ventilation à poumons séparés</b>, et bien sûr "
        "<b>l'intubation difficile elle-même</b> (couverte par une fiche séparée de ce "
        "corpus). Conférence organisée conformément aux règles méthodologiques de "
        "l'Anaes (label qualité attribué), conclusions et recommandations rédigées par "
        "le jury en toute indépendance.",
        S_BODY), bg=BG_PANEL, border=TEAL))
    story.append(Spacer(1, 2.5 * mm))
    story.append(info_panel(P(
        "<b>Méthodologie — disclosure :</b> échelle de grades <b>A à E</b>, explicitement "
        "définie par la source elle-même (légende ci-dessous) — à la différence de "
        "l'échelle GRADE 1+/2+ utilisée par les documents SFAR/SRLF plus récents de ce "
        "corpus. <b>53 recommandations gradées</b> recensées dans le texte (comptage "
        "après consolidation des retours à la ligne issus de la mise en page à 2 "
        "colonnes, un grep naïf ligne-par-ligne n'en trouvant que 49) : "
        "2× Grade A, 1× Grade B, 10× Grade C, 14× Grade D, 26× Grade E. Quelques phrases "
        "informatives du texte ne portent aucun grade explicite (ex. intérêt des "
        "critères paracliniques d'ID, composition du plateau standard, effet de "
        "l'esmolol sur la tachycardie/HTA péri-intubation, données sur le tube laryngé) "
        "— reproduites ici comme texte de contexte, sans grade inventé.",
        S_BODY_SM), bg=AMBER_LIGHT, border=AMBER))
    story.append(Spacer(1, 2.5 * mm))
    story.append(section_bar("Légende des grades (échelle ANAES, définie par la source)"))
    story.append(Spacer(1, 2 * mm))
    story.append(legend_flowable())
    return story


def _section_q1():
    story = [Spacer(1, 2 * mm)]
    story.append(section_bar("Question 1 — Critères prédictifs d'intubation et de ventilation au masque difficiles"))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>Définitions (conférence d'experts Sfar 1996, reprises ici) :</b> une "
        "intubation est dite difficile (ID) lorsqu'elle nécessite plus de 10 min et/ou "
        "plus de 2 laryngoscopies, en position modifiée de Jackson, avec ou sans "
        "manœuvre laryngée. Une ventilation au masque est dite inefficace lorsqu'on "
        "n'obtient pas une SpO<sub>2</sub> &gt; 90 % en ventilant en O<sub>2</sub> pur un "
        "sujet aux poumons non pathologiques (pas de définition consensuelle de la VMD "
        "à ce jour). <i>Les critères paracliniques n'ont pas démontré leur intérêt dans "
        "le dépistage d'une ID (non gradé).</i>",
        S_BODY_SM))
    story.append(Spacer(1, 2 * mm))
    story.append(reco_table([
        ("Q1.1", "La recherche de critères anatomiques, pathologiques et anamnestiques "
                 "est recommandée pour prédire une ID : l'association de plusieurs items "
                 "améliore la prédictibilité par rapport à un critère isolé.", "D"),
        ("Q1.2", "Trois critères anatomiques sont recherchés en priorité : classe de "
                 "Mallampati &gt; 2, distance thyromentale &lt; 65 mm, ouverture de bouche "
                 "&lt; 35 mm — complétés en consultation d'anesthésie par la proéminence "
                 "des incisives supérieures, la mobilité mandibulaire (sub-luxation) et la "
                 "mobilité cervicale (flexion/extension 80–100° ou &lt; 80°).", "D"),
        ("Q1.3", "Cinq critères prédictifs de ventilation au masque difficile (VMD) sont "
                 "recherchés en consultation d'anesthésie : âge &gt; 55 ans, IMC &gt; 26 "
                 "kg/m², édentation, ronflements, barbe (+ anomalies morphologiques "
                 "faciales). En leur absence, une ventilation au masque facile est "
                 "hautement probable.", "D"),
        ("Q1.4", "La détection combinée des facteurs d'ID et de VMD est recommandée, leur "
                 "association identifiant les situations les plus critiques en termes de "
                 "morbidité liée à l'anesthésie.", "E"),
    ], [15 * mm, PAGE_W - 2 * MARGIN - 15 * mm - 16 * mm, 16 * mm]))
    return story


def _section_q2():
    story = [Spacer(1, 2.5 * mm)]
    story.append(section_bar("Question 2 — Matériel, alternatives à la sonde d'intubation, maintenance"))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<i>Non gradé — plateau standard d'intubation :</i> sonde(s) à usage unique, "
        "laryngoscope, plusieurs tailles de lames courbes, lame droite, masque facial "
        "adapté avec filtre antibactérien, canule(s) de Guedel, mandrin(s), pince de "
        "Magill, manomètre de contrôle des pressions, stéthoscope, sparadrap, gels "
        "lubrifiants. <i>Non gradé — maintenance/hygiène :</i> stérilisation conforme "
        "aux textes réglementaires (circulaires DGS/DH n° 645 du 29/12/2000 et "
        "n° DGS/5C/DHOS/E2/2001/138 du 14/03/2001), traçabilité de la procédure et des "
        "dispositifs (décret du 5/12/2001) ; tout matériel réutilisable vérifié avant "
        "chaque utilisation selon une procédure standardisée ; chaque utilisateur "
        "responsable du respect de ces bonnes pratiques.",
        S_BODY_SM))
    story.append(Spacer(1, 2 * mm))
    story.append(reco_table([
        ("Q2.1", "Choisir la plus petite taille de sonde d'intubation compatible avec une "
                 "ventilation efficace sans fuite, en respectant les limites de pression "
                 "du ballonnet (cf. Question 5). Tailles habituelles : 6,5–7–7,5 mm chez "
                 "la femme, 7–7,5–8 mm chez l'homme.", "E"),
        ("Q2.2", "Masque facial, masque laryngé et tube laryngé sont des alternatives à "
                 "l'intubation trachéale, en l'absence de risque de régurgitation.", "E"),
    ], [15 * mm, PAGE_W - 2 * MARGIN - 15 * mm - 16 * mm, 16 * mm]))
    return story


def _section_q3():
    story = [Spacer(1, 2 * mm)]
    story.append(section_bar("Question 3 — Pré-oxygénation et contrôle de la perméabilité des voies aériennes"))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>Physiopathologie (contexte, non gradé) :</b> la pré-oxygénation vise à "
        "réduire le risque d'hypoxémie pendant l'induction en augmentant les réserves en "
        "O<sub>2</sub> de l'organisme. Le temps d'apnée est d'autant plus court que la "
        "CRF est faible, la PAO<sub>2</sub> basse et la consommation d'O<sub>2</sub> "
        "élevée ; en O<sub>2</sub> pur, la dénitrogénation permet de doubler le temps "
        "d'apnée (6 min). Grossesse, obésité, âge avancé, BPCO peuvent modifier la durée "
        "nécessaire et/ou altérer les réserves obtenues.",
        S_BODY_SM))
    story.append(Spacer(1, 2 * mm))
    story.append(reco_table([
        ("Q3.1", "La ventilation spontanée pendant 3 minutes à FiO<sub>2</sub> = 1 est la "
                 "méthode de référence de pré-oxygénation.", "C"),
        ("Q3.2", "D'autres méthodes ont été proposées pour raccourcir la pré-oxygénation "
                 "(4 manœuvres consécutives de capacité vitale ; 8 respirations profondes "
                 "en 1 min), mais restent difficiles à réaliser en pratique.", "D"),
        ("Q3.3", "Quelle que soit la méthode utilisée, le matériel doit être adapté et "
                 "étanche, en particulier au niveau du masque facial.", "D"),
        ("Q3.4", "La pré-oxygénation est impérative en cas de risque de désaturation "
                 "avant la sécurisation des voies aériennes : séquence d'induction "
                 "rapide, critères de VMD ou d'ID, diminution de la CRF…", "E"),
        ("Q3.5", "En dehors de ces situations, une oxygénation préalable est recommandée "
                 "pour se prémunir d'un risque d'hypoxie en cas de VMD ou d'ID non "
                 "prévues.", "E"),
        ("Q3.6", "Le monitorage de la fraction télé-expiratoire d'O<sub>2</sub> "
                 "(FETO<sub>2</sub>) est recommandé pendant la pré-oxygénation — la "
                 "SpO<sub>2</sub> seule ne permet pas d'en apprécier correctement "
                 "l'efficacité.", "E"),
        ("Q3.7", "Il est important de poursuivre la pré-oxygénation au-delà de "
                 "l'obtention d'une FETO<sub>2</sub> &gt; 90 % (témoin d'une "
                 "dénitrogénation optimale, mais pas des réserves tissulaires en "
                 "O<sub>2</sub>).", "E"),
        ("Q3.8", "Il est recommandé d'identifier en consultation d'anesthésie les "
                 "facteurs de risque de désaturation/VMD/ID et de déterminer une "
                 "stratégie d'oxygénation adaptée, avec des techniques alternatives en "
                 "cas d'échec.", "E"),
        ("Q3.9", "Des manœuvres simples (extension de la tête, sub-luxation antérieure de "
                 "la mandibule, canule de Guedel) permettent d'améliorer la perméabilité "
                 "des voies aériennes supérieures, modifiée par les agents anesthésiques.", "E"),
        ("Q3.10", "La ventilation au masque doit s'effectuer à des pressions "
                  "d'insufflation &lt; 25 cmH<sub>2</sub>O (risque d'insufflation "
                  "gastrique) ; il est recommandé de contrôler ces pressions pendant la "
                  "ventilation au masque.", "C"),
    ], [15 * mm, PAGE_W - 2 * MARGIN - 15 * mm - 16 * mm, 16 * mm]))
    return story


def _section_q4():
    story = [Spacer(1, 2 * mm)]
    story.append(section_bar("Question 4 — Agents d'induction (IV, halogénés, morphiniques, curares) et monitorage"))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>Intubation avec curare :</b>",
        pstyle("q4h", base=S_BODY_SM, fontName=FONT_BOLD)))
    story.append(Spacer(1, 1 * mm))
    story.append(reco_table([
        ("Q4.1", "L'utilisation d'un curare améliore les conditions de l'intubation "
                 "trachéale, sous réserve d'une dose suffisante (≥ 2 DA<sub>95</sub>) et "
                 "du respect du délai d'installation de l'effet maximal.", "A"),
        ("Q4.2", "Ce délai d'installation est estimé au mieux par le monitorage de la "
                 "curarisation.", "A"),
        ("Q4.3", "En présence d'un curare, les conditions d'intubation sont toujours "
                 "bonnes ; la réaction somatique et neurovégétative à l'intubation, "
                 "marquée en l'absence de morphinique, peut être diminuée par un "
                 "morphinique à dose modérée.", "C"),
        ("Q4.4", "En administration en bolus, la séquence des 3 agents (hypnotique / "
                 "morphinique / curare) doit être synchronisée pour que leurs pics "
                 "d'action coïncident au moment de la stimulation de l'intubation.", "E"),
        ("Q4.5", "L'association thiopental–succinylcholine reste le protocole de "
                 "référence de l'induction en séquence rapide.", "C"),
        ("Q4.6", "Si un morphinique est utilisé lors d'une induction en séquence rapide, "
                 "le choix d'un agent à délai et durée d'action courts paraît "
                 "raisonnable (aucune donnée validée sur l'indication elle-même du "
                 "morphinique dans ce contexte).", "E"),
    ], [15 * mm, PAGE_W - 2 * MARGIN - 15 * mm - 16 * mm, 16 * mm]))
    story.append(Spacer(1, 2.5 * mm))
    story.append(P(
        "<b>Anesthésie intraveineuse pour intubation sans curare / alternatives à "
        "l'intubation :</b>",
        pstyle("q4h2", base=S_BODY_SM, fontName=FONT_BOLD)))
    story.append(Spacer(1, 1 * mm))
    story.append(reco_table([
        ("Q4.7", "L'intubation sans curare peut être proposée lorsque la curarisation "
                 "n'est pas nécessaire pour la chirurgie ; les conditions d'intubation "
                 "dépendent alors de l'association hypnotique–morphinique.", "C"),
        ("Q4.8", "L'utilisation d'un hypnotique seul (sans curare ni morphinique) n'est "
                 "pas recommandée : elle nécessite des doses très élevées et offre des "
                 "conditions d'intubation médiocres.", "C"),
        ("Q4.9", "L'association d'un morphinique rapproche les conditions d'intubation de "
                 "celles obtenues avec succinylcholine, et diminue par exemple de moitié "
                 "les doses de propofol nécessaires pour contrôler la réaction motrice à "
                 "l'intubation.", "C"),
        ("Q4.10", "La concentration télé-expiratoire de sévoflurane n'est pas un "
                  "estimateur fiable de la concentration cérébrale à l'induction (délai "
                  "d'équilibration) ; elle doit être maintenue un délai suffisant avant "
                  "de tenter l'intubation (&gt; 6 min sous sévoflurane seul, réductible "
                  "de 40 % par midazolam et/ou fentanyl).", "E"),
        ("Q4.11", "La curarisation n'est pas nécessaire pour l'insertion du masque "
                  "laryngé (technique la plus utilisée en alternative à l'intubation).", "E"),
        ("Q4.12", "Le propofol est l'hypnotique IV de choix pour l'insertion du masque "
                  "laryngé (dépression plus marquée des réflexes pharyngolaryngés que le "
                  "thiopental) ; l'ajout d'une faible dose de morphinique améliore "
                  "significativement le taux de succès et diminue d'1/3 la concentration "
                  "cible de propofol en AIVOC.", "D"),
        ("Q4.13", "Le sévoflurane est le seul agent halogéné recommandé pour l'insertion "
                  "du masque laryngé (faible solubilité, absence d'effet irritant sur les "
                  "VAS) ; MAC<sub>95</sub> de l'ordre de 4 %.", "E"),
        ("Q4.14", "L'association d'un morphinique améliore les conditions d'insertion du "
                  "masque laryngé par rapport au sévoflurane seul.", "D"),
        ("Q4.15", "L'efficacité de la lidocaïne IV pour limiter la réaction adrénergique "
                  "à l'intubation est controversée. <i>(L'esmolol 100 mg — non gradé — "
                  "limite significativement la tachycardie, moins nettement "
                  "l'hypertension.)</i>", "E"),
    ], [15 * mm, PAGE_W - 2 * MARGIN - 15 * mm - 16 * mm, 16 * mm]))
    return story


def _section_q5():
    story = [Spacer(1, 2 * mm)]
    story.append(section_bar("Question 5 — Positionnement, techniques d'intubation, contrôle du tube et du ballonnet"))
    story.append(Spacer(1, 1.5 * mm))
    story.append(reco_table([
        ("Q5.1", "L'utilisation systématique et en première intention d'un coussin sous "
                 "la nuque (flexion du cou) n'est pas justifiée, sauf chez les patients "
                 "obèses ou présentant une limitation de la mobilité du rachis "
                 "cervical.", "B"),
        ("Q5.2", "L'intubation endotrachéale sous laryngoscopie directe par voie orale "
                 "est la méthode de référence en anesthésie.", "E"),
        ("Q5.3", "La manœuvre de Sellick (pression cricoïdienne) peut gêner l'exposition "
                 "glottique en laryngoscopie directe.", "D"),
        ("Q5.4", "La manœuvre « BURP » (déplacement postérieur puis céphalique du "
                 "cartilage thyroïde) permet de diminuer l'incidence des laryngoscopies "
                 "difficiles.", "D"),
        ("Q5.5", "Le mandrin long est plus efficace que le mandrin court comme aide à "
                 "l'intubation en cas de difficulté d'exposition (Cormack II–III) ; ces "
                 "mandrins restent des « petits moyens » d'aide à l'intubation.", "C"),
        ("Q5.6", "La mesure de la PETCO<sub>2</sub> est la méthode de référence pour "
                 "contrôler l'absence d'intubation œsophagienne ; les capnogrammes "
                 "doivent être visualisés et stables sur au moins 6 cycles "
                 "ventilatoires.", "E"),
        ("Q5.7", "L'auscultation pulmonaire axillaire est le meilleur moyen de déceler "
                 "une intubation sélective ; à renouveler après chaque changement de "
                 "position du patient.", "E"),
        ("Q5.8", "Si le ballonnet est gonflé à l'air chez un patient ventilé en "
                 "O<sub>2</sub>/N<sub>2</sub>O, le monitorage de la pression du ballonnet "
                 "(dégonflages itératifs si besoin) ou un système d'évacuation "
                 "automatique du gaz en surpression est recommandé (lésions trachéales "
                 "au-delà de 30 cmH<sub>2</sub>O).", "C"),
        ("Q5.9", "Une pression de gonflage de 20 mmHg (≈ 27 cmH<sub>2</sub>O) assure une "
                 "bonne protection des voies aériennes tout en restant sous la pression "
                 "de perfusion de la muqueuse trachéale.", "E"),
        ("Q5.10", "L'utilisation du masque laryngé (LMA) repose sur une analyse "
                  "bénéfice-risque individuelle ; contre-indiquée en cas d'estomac "
                  "plein, de risque de pression ventilatoire élevée, d'absence d'accès "
                  "aux voies aériennes, d'antécédents de reflux gastro-œsophagien, et en "
                  "chirurgie thoracique ou abdominale haute. <i>(Tube laryngé — non "
                  "gradé : trop peu d'études pour en proposer l'usage clinique.)</i>", "E"),
    ], [15 * mm, PAGE_W - 2 * MARGIN - 15 * mm - 16 * mm, 16 * mm]))
    return story


def _section_q6():
    story = [Spacer(1, 2 * mm)]
    story.append(section_bar("Question 6 — Lésions liées à l'intubation, prévention de l'inhalation bronchique"))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<i>Contexte (non gradé) :</i> l'absence d'études prospectives, randomisées, "
        "multicentriques consacrées à ces lésions ne permet pas de préciser exactement "
        "leur prévalence, leurs facteurs de risque ni l'apport des diverses attitudes "
        "préventives proposées.",
        S_BODY_SM))
    story.append(Spacer(1, 2 * mm))
    story.append(P("<b>Lésions liées à l'intubation oro/nasotrachéale :</b>",
                    pstyle("q6h", base=S_BODY_SM, fontName=FONT_BOLD)))
    story.append(Spacer(1, 1 * mm))
    story.append(reco_table([
        ("Q6.1", "Recherche systématique en consultation d'anesthésie d'une "
                 "fragilité/d'un mauvais état dentaire, avec utilisation d'une "
                 "protection dentaire dans les cas à risque.", "E"),
        ("Q6.2", "Choisir la sonde d'intubation de la plus petite taille possible "
                 "(compte tenu des contraintes de ventilation) ; en intubation "
                 "nasotrachéale, rétraction muqueuse par un vasoconstricteur.", "D"),
        ("Q6.3", "Limiter l'hyperextension du cou pour éviter les lésions trachéales.", "E"),
        ("Q6.4", "Le dépistage des complications est clinique (douleur cervicale "
                 "latéralisée, douleur thoracique à irradiation postérieure, "
                 "dysphagie/odynophagie douloureuses, douleur à la palpation, "
                 "crépitation cervicale, fièvre) : cette suspicion doit faire discuter "
                 "l'arrêt de l'alimentation orale, une antibiothérapie, et un avis "
                 "spécialisé.", "E"),
        ("Q6.5", "Une dysphonie intense, persistant au-delà de 48 h, ou associée à une "
                 "otalgie/odynophagie, doit conduire à une consultation ORL spécialisée "
                 "à la recherche de lésions laryngées.", "E"),
    ], [15 * mm, PAGE_W - 2 * MARGIN - 15 * mm - 16 * mm, 16 * mm]))
    story.append(Spacer(1, 2.5 * mm))
    story.append(P(
        "<b>Lésions liées au masque laryngé</b> <i>(symptômes sans substratum fréquents "
        "— maux de gorge — mais lésions anatomiques directes rares, non gradé) :</i>",
        pstyle("q6h2", base=S_BODY_SM, fontName=FONT_BOLD)))
    story.append(Spacer(1, 1 * mm))
    story.append(reco_table([
        ("Q6.6", "S'assurer d'une anesthésie profonde et ne pas multiplier les essais "
                 "d'insertion.", "D"),
        ("Q6.7", "Choisir une taille de masque laryngé appropriée.", "D"),
        ("Q6.8", "Utiliser la méthode d'insertion « coussinet semi-gonflé » — qui majore "
                 "cependant le risque de mauvais positionnement.", "C"),
        ("Q6.9", "Limiter la pression dans le ballonnet du masque laryngé.", "D"),
    ], [15 * mm, PAGE_W - 2 * MARGIN - 15 * mm - 16 * mm, 16 * mm]))
    story.append(Spacer(1, 2.5 * mm))
    story.append(P("<b>Prévention de l'inhalation bronchique :</b>",
                    pstyle("q6h3", base=S_BODY_SM, fontName=FONT_BOLD)))
    story.append(Spacer(1, 1 * mm))
    story.append(reco_table([
        ("Q6.10", "Le jeûne (abstention de liquide clair 2 h, de solides 6 h avant la "
                  "chirurgie) reste l'attitude classique de prévention de l'inhalation "
                  "bronchique, quel que soit le mode d'accès aux voies aériennes.", "E"),
        ("Q6.11", "Dans les situations prédisposant à l'inhalation, l'induction en "
                  "séquence rapide associée à une pression cricoïdienne et à des "
                  "préparations neutralisant l'acidité gastrique est recommandée.", "D"),
        ("Q6.12", "La protection des voies aériennes par le masque laryngé, supposée "
                  "moins efficace que par la sonde endotrachéale, contre-indique son "
                  "utilisation dans les situations à risque d'inhalation.", "E"),
    ], [15 * mm, PAGE_W - 2 * MARGIN - 15 * mm - 16 * mm, 16 * mm]))
    return story


def _section_sources():
    story = [Spacer(1, 3 * mm)]
    story.append(section_bar("Comité d'organisation, jury, experts & sources", color=GREY))
    story.append(Spacer(1, 2 * mm))
    story.append(P(
        "<b>Comité d'organisation :</b> P. Ravussin (Président, Sion), A.-M. Cros "
        "(Bordeaux), M. Gentili (Saint-Grégoire), O. Langeron (Paris), C. Martin "
        "(Marseille), S. Molliex (Saint-Étienne), P. Monnier (Lausanne). "
        "<b>Jury :</b> S. Molliex (Président), J.-C. Berset, V. Billard, É. Bunouf, "
        "S. Delort-Laval, B. Frering, M. Freysz, O. Laccourreyre, D. Lugrin, J.-P. "
        "Mustaki, C. Penon, F. Sztark, O. Tueux. <b>Experts :</b> F. Adnet, B. Bally, "
        "D. Boisson-Bertrand, J.-L. Bourgain, N. Bruder, M. Chollet-Rivies, B. Debaene, "
        "P. Diemunsch, C. Ecoffey, J.-P. Estebe, D. Francon, J. Lacau Saint-Guily, "
        "G. Mion, D. Pean.",
        S_BODY_SM))
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Avertissement :</b> document de 2002 (recommandations imprimées en 2003) — "
        "les pratiques et le matériel de prise en charge des voies aériennes ont évolué "
        "depuis (vidéolaryngoscopie, algorithmes d'oxygénation apnéique, dispositifs "
        "supra-glottiques de 2<sup>e</sup> génération…), disclosé explicitement plutôt "
        "que silencieusement mis à jour ; se référer aux recommandations SFAR "
        "ultérieures pour l'intubation difficile et pour la prise en charge des voies "
        "aériennes de l'enfant.",
        S_BODY_SM), bg=RED_LIGHT, border=RED))
    return story


def _section_1():
    # Merge intro + Q1 onto shared pages (CLAUDE.md step 7: these sections were each
    # <60% full on their own page when built separately). Q2 is merged with Q3 instead
    # of here (see _section_2) - an earlier intro+Q1+Q2 merge left Q2's 2-row table
    # orphaned alone on a near-empty page; re-measured after reverting to this split,
    # which fills pages better without leaving Q2 stranded.
    return _section_intro() + [Spacer(1, 2.5 * mm)] + _section_q1()


def _section_2():
    return _section_q2() + [Spacer(1, 2.5 * mm)] + _section_q3()


def _section_6():
    return _section_q6() + [Spacer(1, 3 * mm)] + _section_sources()


SECTIONS = [
    ("Introduction & critères prédictifs (Question 1)", _section_1),
    ("Matériel & pré-oxygénation (Questions 2-3)", _section_2),
    ("Question 4 — Agents d'induction et monitorage", _section_q4),
    ("Question 5 — Positionnement et techniques d'intubation", _section_q5),
    ("Question 6 — Lésions liées à l'intubation & prévention de l'inhalation", _section_6),
]


def _make_doc(path=None):
    return SimpleDocTemplate(path or OUT, pagesize=A4,
                              leftMargin=MARGIN, rightMargin=MARGIN,
                              topMargin=32 * mm, bottomMargin=16 * mm,
                              title="Fiche SFAR 2002 - Voies aériennes en anesthésie adulte",
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
