# -*- coding: utf-8 -*-
"""
Fiche de synthese - Conference de consensus 2002 (texte court publie 2003), Sfar/Anaes :
"Prise en charge des voies aeriennes en anesthesie adulte a l'exception de l'intubation
difficile". Ann Fr Anesth Reanim 2003;22:745-749.

DISCLOSURE - PERIMETRE : la source exclut explicitement de son cadre (preambule) : la
prise en charge des voies aeriennes en medecine extrahospitaliere, en urgence medicale
hospitaliere, en anesthesie pediatrique, et lors d'une ventilation a poumons separes -
et bien sur l'intubation difficile elle-meme (deja traitee par fiche_intubation_
difficile_adulte.py, RFE 2017, document plus recent et complementaire). Cette fiche ne
retranscrit donc QUE la prise en charge standard (non difficile) des voies aeriennes en
anesthesie adulte programmee - perimetre etroit, mais integralement couvert.

METHODOLOGIE - grades Anaes A a E (echelle de niveau de preuve, PAS le schema HAS A/B/C
utilise ailleurs dans ce corpus, ni le schema GRADE 1+/2+) : A = 2 etudes ou plus de
niveau I ; B = une etude de niveau I ; C = etude(s) de niveau II ; D = une etude ou plus
de niveau III ; E = etude(s) de niveau IV ou V. VERIFIE PAR grep exhaustif sur le texte
aplati : 53 citations "(Grade X)" explicites - 2x A, 1x B, 10x C, 14x D, 26x E. Chaque
recommandation de cette fiche porte le grade explicitement imprime par la source, un
pour un (aucune fusion de deux citations sous un chip unique). Extension locale non
invasive du dictionnaire GRADE_COLORS partage (les lettres A/B/C sont deja utilisees
ailleurs dans ce corpus pour le schema HAS accord-professionnel - collision de LIBELLE
uniquement, pas de collision de SENS puisque chaque fiche definit son propre mapping
localement ; D et E sont des libelles nouveaux, sans collision) : A=vert, B=teal,
C=ambre, D=gris, E=gris clair - degrade visuel decroissant reproduisant la hierarchie
de preuve decroissante de la source.

_count_pages() : pattern copie de fiche_aap_programmee.py (PyMuPDF/fitz, jamais vers
OUT, toujours vers tempfile.mktemp()).
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from style import *
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.units import mm

GRADE_COLORS["A"] = (GREEN, WHITE)
GRADE_COLORS["B"] = (TEAL, WHITE)
GRADE_COLORS["C"] = (AMBER, WHITE)
GRADE_COLORS["D"] = (GREY, WHITE)
GRADE_COLORS["E"] = (GREY_LIGHT, INK)
GRADE_COLORS["—"] = (GREY_LIGHT, INK)

OUT = "/home/user/rfe-sfar-website/output/Fiche_SFAR_Voies_Aeriennes_Anesthesie_Adulte_2002.pdf"

SOURCE_TXT = ("Source : Sfar/Anaes — Conférence de consensus « Prise en charge des voies "
              "aériennes en anesthésie adulte à l'exception de l'intubation difficile » (2002, "
              "texte court publié 2003), Ann Fr Anesth Reanim 2003;22:745-749. Fiche de synthèse "
              "non officielle : se référer au texte intégral.")

def P(txt, style=S_CELL):
    return Paragraph(txt, style)

def chip(label, **kw):
    return grade_chip(label, **kw)

GRADE_W = 15 * mm

def reco_table(rows, col_widths=None):
    """rows: (theme, text, grade_label) - grade_label parmi 'A'-'E'."""
    text_w = PAGE_W - 2 * MARGIN - GRADE_W
    cw = col_widths or [text_w, GRADE_W]
    data = [[P("Recommandation (texte condensé, fidèle à la source)", S_HEAD_W), P("Grade", S_HEAD_W_C)]]
    for txt, grade in rows:
        data.append([P(txt, S_CELL), chip(grade, width=GRADE_W - 2 * mm)])
    t = Table(data, colWidths=cw, repeatRows=1)
    style_cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), NAVY), ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTNAME", (0, 0), (-1, 0), FONT_BOLD), ("FONTSIZE", (0, 0), (-1, 0), 8),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("ALIGN", (1, 0), (1, -1), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 0.5, GREY_LIGHT),
        ("TOPPADDING", (0, 0), (-1, -1), 3.2), ("BOTTOMPADDING", (0, 0), (-1, -1), 3.2),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            style_cmds.append(("BACKGROUND", (0, i), (-1, i), BG_PANEL))
    t.setStyle(TableStyle(style_cmds))
    return t

TOTAL_PAGES = {"n": 4}

def on_page(canvas, doc, page_title):
    header_band(canvas, doc, "SFAR / ANAES — CONFÉRENCE DE CONSENSUS 2002 — FICHE DE SYNTHÈSE",
                "Voies aériennes en anesthésie adulte",
                page_title, icon_fn=lambda c, x, y: icon_shield(c, x, y, 13 * mm), color=NAVY)
    footer_band(canvas, doc, SOURCE_TXT, f"Page {doc.page} / {TOTAL_PAGES['n']}")

# ---------------------------------------------------------------------------
def _section_intro_q1_q2():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Champ :</b> prise en charge <b>standard (non difficile)</b> des voies aériennes en "
        "anesthésie adulte — critères prédictifs, matériel, pré-oxygénation, agents d'induction, "
        "techniques d'intubation, lésions liées à l'intubation. <b>Exclut</b> explicitement (hors "
        "champ de la source) : la prise en charge en médecine extrahospitalière, en urgence "
        "médicale hospitalière, en anesthésie pédiatrique, lors d'une ventilation à poumons "
        "séparés, et <b>l'intubation difficile elle-même</b> (traitée séparément par la RFE 2017, "
        "déjà couverte dans ce corpus — fiche « Intubation difficile — adulte »).",
        S_BODY), bg=BG_PANEL, border=NAVY))
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Méthodologie — grades Anaes A à E</b> (échelle de niveau de preuve, distincte du "
        "schéma HAS A/B/C et du schéma GRADE 1+/2+ utilisés ailleurs dans ce corpus) : "
        "<b>A</b> = 2 études ou plus de niveau I ; <b>B</b> = une étude de niveau I ; <b>C</b> = "
        "étude(s) de niveau II ; <b>D</b> = une étude ou plus de niveau III ; <b>E</b> = étude(s) "
        "de niveau IV ou V. <b>Vérifié par grep exhaustif : 53 citations « (Grade X) » "
        "explicites — 2× A, 1× B, 10× C, 14× D, 26× E</b> — retranscrites un pour un contre le "
        "texte source.", S_BODY_SM), bg=BG_PANEL, border=AMBER))
    story.append(Spacer(1, 3 * mm))

    story.append(section_bar("1 — Critères d'intubation et de ventilation au masque difficiles", color=NAVY))
    story.append(Spacer(1, 2 * mm))
    story.append(P(
        "Intubation difficile (ID) : &gt; 10 min et/ou &gt; 2 laryngoscopies en position de "
        "Jackson modifiée, avec ou sans manœuvre laryngée (définition Sfar 1996).", S_BODY_SM))
    story.append(Spacer(1, 2 * mm))
    story.append(reco_table([
        ("La recherche de critères anatomiques, pathologiques et anamnestiques améliore la "
         "prédictibilité de l'ID par rapport à chaque item pris isolément.", "D"),
        ("3 critères anatomiques préconisés pour envisager une ID chez l'adulte : classe de "
         "Mallampati &gt; 2, distance thyromentale &lt; 65 mm, ouverture de bouche &lt; 35 mm — "
         "complétables par la proéminence des incisives supérieures, la mobilité mandibulaire "
         "(sub-luxation nulle/impossible) et cervicale (80-100° ou &lt; 80°).", "D"),
        ("Ventilation au masque difficile (VMD) : 5 critères prédictifs retenus — âge &gt; "
         "55 ans, IMC &gt; 26 kg/m², édentation, ronflements, barbe — à rechercher en "
         "consultation d'anesthésie avec les anomalies morphologiques faciales. En leur "
         "absence, une ventilation au masque facile est hautement probable.", "D"),
        ("La détection de facteurs d'ID doit s'accompagner de la recherche de facteurs de VMD "
         "(leur association dépiste les situations les plus critiques).", "E"),
    ]))
    story.append(Spacer(1, 4 * mm))

    story.append(section_bar("2 — Matériel pour la prise en charge des voies aériennes", color=NAVY))
    story.append(Spacer(1, 2 * mm))
    story.append(P(
        "Plateau standard d'intubation : sonde(s) à usage unique, laryngoscope, lames courbes "
        "(plusieurs tailles) et droite, masque facial avec filtre antibactérien, canule(s) de "
        "Guedel, mandrin(s), pince de Magill, manomètre de contrôle des pressions, "
        "stéthoscope, sparadrap, gels lubrifiants.", S_BODY_SM))
    story.append(Spacer(1, 2 * mm))
    story.append(reco_table([
        ("Choisir la plus petite taille de sonde compatible avec une ventilation efficace sans "
         "fuite et une pression de ballonnet dans les limites préconisées. Tailles habituelles : "
         "6,5-7-7,5 mm chez la femme, 7-7,5-8 mm chez l'homme.", "E"),
        ("Masque facial, masques laryngés ou tube laryngé sont des alternatives à l'intubation "
         "en l'absence de risque de régurgitation.", "E"),
        ("Stérilisation conforme aux textes réglementaires (traçabilité de la procédure et suivi "
         "des dispositifs traités) ; vérifier tout matériel réutilisable avant chaque "
         "utilisation selon une procédure standardisée. Chaque utilisateur est responsable du "
         "respect de ces bonnes pratiques.", "—"),
    ]))
    return story


def _section_q3():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("3 — Pré-oxygénation et perméabilité des voies aériennes", color=NAVY))
    story.append(Spacer(1, 2 * mm))
    story.append(P(
        "La pré-oxygénation réduit le risque d'hypoxémie pendant l'induction en augmentant les "
        "réserves en oxygène ; en O2 pur, la dénitrogénation et les réserves tissulaires "
        "permettent de doubler le temps d'apnée (~6 min). Grossesse, obésité, sujet âgé et BPCO "
        "peuvent modifier la durée nécessaire à une dénitrogénation complète.", S_BODY_SM))
    story.append(Spacer(1, 2 * mm))
    story.append(reco_table([
        ("Ventilation spontanée pendant 3 min à FIO2 = 1 : méthode de référence.", "C"),
        ("Méthodes alternatives pour raccourcir la pré-oxygénation (4 manœuvres consécutives de "
         "capacité vitale, 8 respirations profondes en 1 min) : difficiles à réaliser.", "D"),
        ("Quelle que soit la méthode : matériel adapté et étanche, particulièrement au niveau du "
         "masque facial. La coopération du patient (facilitée par une information préalable en "
         "consultation) est déterminante.", "D"),
        ("Pré-oxygénation impérative en cas de risque de désaturation avant sécurisation des "
         "voies aériennes (séquence d'induction rapide, critères de VMD/ID, CRF diminuée).", "E"),
        ("En dehors de ces situations : pré-oxygénation recommandée pour se prémunir contre "
         "l'hypoxie en cas de VMD/ID non prévues.", "E"),
        ("Le monitorage de la FETO2 est recommandé pendant la pré-oxygénation — la SpO2 "
         "n'apprécie pas correctement son efficacité. FETO2 &gt; 90 % = dénitrogénation "
         "optimale (mais n'apprécie pas les réserves tissulaires) ; poursuivre la "
         "pré-oxygénation au-delà.", "E"),
        ("Identifier en consultation d'anesthésie les facteurs de risque de désaturation, de VMD "
         "ou d'ID, et déterminer une stratégie d'oxygénation adaptée avec techniques "
         "alternatives en cas d'échec.", "E"),
        ("Des manœuvres simples (extension de la tête, sub-luxation antérieure de la mandibule, "
         "canule de Guedel) améliorent la perméabilité des voies aériennes supérieures, modifiée "
         "par les agents anesthésiques.", "E"),
        ("Ventilation au masque à des pressions d'insufflation &lt; 25 cmH2O (risque "
         "d'insufflation gastrique) ; contrôler les pressions d'insufflation pendant la "
         "ventilation au masque. La baisse de la SpO2 est un critère tardif de ventilation "
         "inefficace.", "C"),
    ]))
    return story


def _section_q4():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("4 — Agents d'induction : IV, halogénés, morphiniques, curares", color=NAVY))
    story.append(Spacer(1, 2 * mm))
    story.append(P("<b>Intubation avec curare</b>", S_BODY_SM))
    story.append(Spacer(1, 1.5 * mm))
    story.append(reco_table([
        ("Un curare améliore les conditions d'intubation, sous réserve d'une dose suffisante "
         "(≥ 2 DA95) et du respect du délai d'installation de l'effet maximal.", "A"),
        ("Ce délai est estimé au mieux par le monitorage de la curarisation.", "A"),
        ("En présence d'un curare, les conditions d'intubation sont toujours bonnes ; la "
         "réaction somatique/neurovégétative à l'intubation, marquée en l'absence de "
         "morphinique, peut être diminuée par leur utilisation à doses modérées.", "C"),
        ("Si administration en bolus : synchroniser la séquence pour être proche du pic d'action "
         "des 3 agents au moment de la stimulation d'intubation. Perfusion continue précédée "
         "d'un bolus, ou AIVOC, sont des alternatives à considérer.", "E"),
        ("L'association thiopental-succinylcholine reste le protocole de référence en induction "
         "en séquence rapide.", "C"),
        ("Si un morphinique est utilisé en séquence rapide : privilégier un agent de délai et "
         "durée d'action courts (aucune donnée validée sur l'indication elle-même).", "E"),
    ]))
    story.append(Spacer(1, 2 * mm))
    story.append(P("<b>Anesthésie IV pour intubation sans curare</b>", S_BODY_SM))
    story.append(Spacer(1, 1.5 * mm))
    story.append(reco_table([
        ("L'intubation sans curare peut être proposée lorsque la curarisation n'est pas "
         "nécessaire pour la chirurgie (conditions/tolérance conditionnées par l'association "
         "hypnotique-morphinique).", "C"),
        ("Un hypnotique seul n'est pas recommandé (doses très élevées nécessaires, conditions "
         "d'intubation médiocres).", "C"),
        ("L'association d'un morphinique rapproche des conditions obtenues avec succinylcholine "
         "et divise par 2 les doses de propofol nécessaires pour contrôler la réaction motrice. "
         "Des doses élevées de morphinique apportent peu de bénéfice supplémentaire mais "
         "peuvent induire une baisse significative de la pression artérielle et de la fréquence "
         "cardiaque.", "C"),
    ]))
    story.append(Spacer(1, 2 * mm))
    story.append(P("<b>Induction au sévoflurane & alternatives à l'intubation</b>", S_BODY_SM))
    story.append(Spacer(1, 1.5 * mm))
    story.append(reco_table([
        ("La concentration télé-expiratoire de sévoflurane n'est pas un estimateur fiable de la "
         "concentration cérébrale à l'induction (délai d'équilibration) : la maintenir un délai "
         "suffisant avant l'intubation (&gt; 6 min sous sévoflurane seul, réductible de 40 % "
         "par midazolam et/ou fentanyl).", "E"),
        ("La curarisation n'est pas nécessaire pour l'insertion du masque laryngé.", "E"),
        ("Le propofol est l'hypnotique IV de choix pour l'insertion du masque laryngé (déprime "
         "plus les réflexes pharyngolaryngés que le thiopental). L'adjonction d'une faible dose "
         "de morphinique améliore le taux de succès et diminue d'1/3 la concentration cible de "
         "propofol en AIVOC.", "D"),
        ("Le sévoflurane est le seul halogéné recommandé pour l'insertion du masque laryngé "
         "(faible solubilité, absence d'effet irritant). MAC95 ≈ 4 % ; l'association d'un "
         "morphinique améliore les conditions d'insertion par rapport au sévoflurane seul.", "E"),
        ("L'association sévoflurane + morphinique améliore les conditions d'insertion du masque "
         "laryngé par rapport au sévoflurane seul.", "D"),
        ("Traitement symptomatique de la réaction adrénergique à l'intubation : efficacité de la "
         "lidocaïne IV controversée ; l'esmolol 100 mg limite significativement la tachycardie "
         "(moins nettement l'hypertension).", "E"),
    ]))
    return story


def _section_q5_q6_sources():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("5 — Positionnement, techniques d'intubation & dispositifs alternatifs", color=NAVY))
    story.append(Spacer(1, 2 * mm))
    story.append(reco_table([
        ("Le coussin systématique sous la nuque (flexion du cou) n'est pas justifié en première "
         "intention, sauf patients obèses ou limitation de mobilité du rachis cervical.", "B"),
        ("L'intubation endotrachéale sous laryngoscopie directe par voie orale reste la méthode "
         "de référence en anesthésie.", "E"),
        ("La manœuvre de Sellick peut gêner l'exposition glottique en laryngoscopie directe.",
         "D"),
        ("La manœuvre de « BURP » (déplacement postérieur puis céphalique du cartilage "
         "thyroïdien) diminue l'incidence de laryngoscopies difficiles.", "D"),
        ("Le mandrin long est plus efficace que le mandrin court en cas de difficulté "
         "d'exposition (Cormack II/III) — petit moyen d'aide à l'intubation.", "C"),
        ("La PETCO2 est la méthode de référence pour contrôler l'absence d'intubation "
         "œsophagienne (capnogrammes visualisés et stables ≥ 6 cycles ventilatoires).", "E"),
        ("L'auscultation pulmonaire axillaire est le meilleur moyen de déceler l'intubation "
         "sélective — à renouveler après chaque changement de position du patient.", "E"),
        ("Monitorer la pression du ballonnet (dégonflages itératifs si besoin) ou utiliser un "
         "système d'évacuation automatique du gaz en surpression, si ballonnet gonflé à l'air "
         "et ventilation O2/N2O (lésions trachéales si pression &gt; 30 cmH2O).", "C"),
        ("Une pression de gonflage de 20 mmHg (~27 cmH2O) assure une bonne protection tout en "
         "restant sous la pression de perfusion de la muqueuse trachéale.", "E"),
        ("L'utilisation du masque laryngé (LMA) repose sur une analyse individuelle "
         "bénéfice-risque : contre-indiqué en cas d'estomac plein, risque de pression "
         "ventilatoire élevée, absence d'accès aux voies aériennes, antécédent de RGO, "
         "chirurgie thoracique ou abdominale haute.", "E"),
        ("Le faible nombre d'études sur le tube laryngé ne permet pas de proposer son "
         "utilisation clinique.", "—"),
    ]))
    story.append(Spacer(1, 4 * mm))

    story.append(section_bar("6 — Lésions liées à l'intubation & prévention de l'inhalation", color=NAVY))
    story.append(Spacer(1, 2 * mm))
    story.append(P("<b>Lésions liées à l'intubation oro/nasotrachéale</b>", S_BODY_SM))
    story.append(Spacer(1, 1.5 * mm))
    story.append(reco_table([
        ("Rechercher systématiquement en consultation d'anesthésie une fragilité/mauvais état "
         "dentaire ; utiliser une protection dentaire dans les cas à risque (dents fragilisées, "
         "chirurgie à risque dentaire).", "E"),
        ("Choisir la plus petite taille de sonde possible (contraintes de ventilation) ; "
         "rétraction muqueuse par vasoconstricteur lors d'une intubation nasotrachéale.", "D"),
        ("Limiter l'hyperextension du cou pour éviter les lésions trachéales.", "E"),
        ("Dépistage clinique des complications (douleur cervicale latéralisée, douleur "
         "thoracique à irradiation postérieure, dysphagie/odynophagie douloureuse, douleur à la "
         "palpation, crépitation cervicale, fièvre) : discuter interruption de l'alimentation "
         "orale, antibiothérapie, avis spécialisé. Dysphonie intense, persistant &gt; 48h ou "
         "associée à otalgie/odynophagie : consultation ORL à la recherche de lésions "
         "laryngées.", "E"),
    ]))
    story.append(Spacer(1, 2 * mm))
    story.append(P("<b>Lésions liées au masque laryngé</b>", S_BODY_SM))
    story.append(Spacer(1, 1.5 * mm))
    story.append(reco_table([
        ("S'assurer d'une anesthésie profonde et ne pas multiplier les essais.", "D"),
        ("Choisir une taille de masque appropriée.", "D"),
        ("Utiliser la méthode d'insertion « coussinet semi-gonflé » (majore cependant le risque "
         "de mauvais positionnement).", "C"),
        ("Limiter la pression dans le ballonnet.", "D"),
    ]))
    story.append(Spacer(1, 2 * mm))
    story.append(P("<b>Prévention de l'inhalation bronchique</b>", S_BODY_SM))
    story.append(Spacer(1, 1.5 * mm))
    story.append(reco_table([
        ("Jeûne (abstention liquide clair 2h, solides 6h avant chirurgie), quel que soit le mode "
         "d'accès aux voies aériennes.", "E"),
        ("Situations prédisposant à l'inhalation : induction en séquence rapide + pression "
         "cricoïdienne + neutralisation de l'acidité gastrique.", "D"),
        ("Le masque laryngé, supposé moins protecteur que la sonde endotrachéale, est "
         "contre-indiqué dans les situations à risque d'inhalation.", "E"),
    ]))
    story.append(Spacer(1, 4 * mm))

    story.append(section_bar("Sources et traçabilité", color=GREY))
    story.append(Spacer(1, 2 * mm))
    story.append(P(
        "<b>Document source :</b> « Prise en charge des voies aériennes en anesthésie adulte à "
        "l'exception de l'intubation difficile » — Conférence de consensus Sfar/Anaes, texte "
        "court, 2002 (publié 2003). Président du comité d'organisation : P. Ravussin. Président "
        "du jury : S. Molliex. Ann Fr Anesth Reanim 2003;22:745-749.", S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P("<b>Méthodologie :</b> grades Anaes A à E (niveau de preuve) — 53 citations "
                    "« (Grade X) » explicites (2× A, 1× B, 10× C, 14× D, 26× E), vérifiées par "
                    "grep exhaustif sur le texte aplati.", S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P("<b>Couverture :</b> cette fiche reprend l'intégralité des 6 questions "
                    "traitées par la conférence (critères d'ID/VMD, matériel, pré-oxygénation, "
                    "agents d'induction, positionnement/techniques d'intubation, lésions liées à "
                    "l'intubation). Comité d'organisation, jury et experts (listes nominatives) "
                    "ne sont pas retranscrits (sans contenu clinique).", S_SOURCE))
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Avertissement — document de 2002/2003 :</b> ce document est une fiche de synthèse "
        "indépendante, produite pour un usage d'aide-mémoire. Elle reprend l'intégralité des "
        "recommandations du texte source, mais ne remplace pas le texte intégral et n'est ni "
        "éditée ni validée par la Sfar. Document ancien et de périmètre étroit (exclut "
        "l'intubation difficile, la pédiatrie, l'urgence extrahospitalière) : se référer aux "
        "fiches dédiées de ce corpus pour ces situations, et à un avis spécialisé en cas de "
        "doute — certaines pratiques (ex. molécules, dispositifs) ont pu évoluer depuis.",
        S_BODY_SM), bg=GREY_LIGHT, border=GREY))
    return story


SECTIONS = [
    ("Critères ID/VMD & matériel", _section_intro_q1_q2),
    ("Pré-oxygénation", _section_q3),
    ("Agents d'induction", _section_q4),
    ("Techniques, lésions & sources", _section_q5_q6_sources),
]

def _make_doc(path=None):
    return SimpleDocTemplate(path or OUT, pagesize=A4,
                              leftMargin=MARGIN, rightMargin=MARGIN,
                              topMargin=32 * mm, bottomMargin=16 * mm,
                              title="Sfar/Anaes 2002 - Voies aeriennes en anesthesie adulte",
                              author="Synthèse indépendante (source Sfar/Anaes)")

def _silent_page(canvas, doc_):
    pass

def _build_upto(section_fns):
    story = []
    for i, fn in enumerate(section_fns):
        if i > 0:
            story.append(Spacer(1, 4 * mm))
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

    final_story = _build_upto(fns)
    docf = _make_doc()
    docf.build(final_story, onFirstPage=on_page_final, onLaterPages=on_page_final)
    print("OK ->", OUT, f"({total_pages} pages)")

if __name__ == "__main__":
    build()
