# -*- coding: utf-8 -*-
"""
Fiche de synthese - "Strategies de reduction de l'utilisation des
antibiotiques a visee curative en reanimation (adulte et pediatrique)" -
Recommandations Formalisees d'Experts (RFE) SRLF/SFAR, avec GFRUP/SFM/
SPILF/SF2H, Juin 2014. 44 pages, telecharge depuis sfar.org (wp-content/
uploads/2015/09/2_SPILF_Strategies-de-reduction-de-lutilisation-des-
antibiotiques-a-visee-curative-en-reanimation.pdf).

METHODOLOGIE : GRADE pour l'analyse de la litterature (niveau de preuve
fort -> recommandation "forte", il faut/ne faut pas ; niveau modere/faible/
tres faible -> recommandation "optionnelle", il faut probablement/ne faut
probablement pas). Cotation collective derivee de RAND/UCLA (2 tours,
echelle 1-9, mediane + IC, 3 zones accord/indecision/desaccord, "fort" si
l'IC reste dans une zone, "faible" s'il empiete sur une borne). Le texte
source lui-meme est explicite : "54 recommandations... Certaines de ces
recommandations ont ete scindees en differents items (n=74)" - verifie par
extraction programmatique exhaustive de tous les tags "(Accord fort)"/
"(Accord faible)" imprimes (47 fort + 27 faible = 74, correspond
exactement). Contrairement a d'autres RFE de ce corpus, AUCUN symbole
GRADE numerique (1+/1-/2+/2-) n'est imprime par item - seul le tag Accord
Fort/Faible (RAND/UCLA) est explicitement present ; la force "il faut"
vs "il faut probablement" reste donc dans le libelle textuel de chaque
ligne (jamais transformee en chip GRADE invente, puisque non imprimee
par le texte source). Chips locaux "AF" (Accord Fort, vert) / "AF-"
(Accord Faible, ambre) introduits pour cette fiche.

DISCLOSURE - scission des recommandations multi-votees : 11 des 54
recommandations numerotees portent en realite PLUSIEURS votes internes
(bullets "•" ou phrases successives), chacun avec son propre tag Accord
Fort/Faible, parfois DIFFERENTS au sein d'une meme recommandation source
(ex. Q2.7 : antigenurie pneumocoque positive = Accord faible, antigenurie
pneumocoque negative = Accord fort). Conformement a la regle anti-grade-
composite du projet, chaque sous-vote a ete transcrit sur sa PROPRE ligne
avec son PROPRE chip des lors que son niveau d'accord differe de celui
d'un sous-vote adjacent ; les sous-votes de MEME niveau ont ete regroupes
sur une seule ligne (jamais l'inverse - jamais un fort et un faible fondus
en un seul chip). Resultat : 62 lignes de synthese pour 74 votes source
(certaines lignes portent 2-3 faits de meme niveau, aucune n'en porte deux
de niveaux differents). Verifie item par item par re-lecture du texte
source complet avant transcription (pas de decompte devine).

PERIMETRE : integral sur les 5 questions (Q1 resistance/epidemiologie, Q2
donnees microbiologiques, Q3 choix de l'antibiotherapie [colonisation,
carbapenemes, quinolones, anti-SARM probabiliste et documente], Q4
optimiser l'administration [indication formelle, dosage/TDM, modalites
d'administration, associations], Q5 reevaluation et duree). Argumentaire
minimal (regle 2026-09-14) : les etudes/statistiques citees a l'appui de
chaque item ne sont pas transcrites - seul l'enonce actionnable (incluant
les exceptions/conditions cliniques explicites, qui font partie de la
recommandation elle-meme, pas de son argumentaire) est retenu. Distinct de
la fiche existante `infections_nosocomiales_rea` (SFAR/SRLF 2008/2009,
prevention des infections nosocomiales - epidemiologie/organisation/
prevention specifique PAVM-IU-catheters-ISO) : ce document-ci traite
specifiquement des strategies de REDUCTION de l'usage CURATIF des
antibiotiques deja prescrits (desescalade, choix moleculaire, dosage,
duree), perimetre verifie distinct avant construction. Bibliographie
(228 references) et composition nominative du groupe d'experts (page 1,
non reproduite) - non actionnable cliniquement.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from style import *
GRADE_COLORS["AF"] = (GREEN, WHITE)
GRADE_COLORS["AF-"] = (AMBER, WHITE)
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.units import mm

OUT = "/home/user/rfe-sfar-website/output/Fiche_SRLF_SFAR_Reduction_Antibiotiques_Reanimation_2014.pdf"

SOURCE_TXT = ("Source : SRLF/SFAR (GFRUP/SFM/SPILF/SF2H), « Stratégies de réduction de "
              "l'utilisation des antibiotiques à visée curative en réanimation (adulte et "
              "pédiatrique) », RFE, Juin 2014. Fiche de synthèse non officielle : se référer "
              "au texte intégral.")

def P(txt, style=S_CELL):
    return Paragraph(txt, style)

def chip(label, **kw):
    return grade_chip(label, **kw)

CW_FULL = PAGE_W - 2 * MARGIN

def reco_table(rows, col_widths):
    """rows: (ref, text, grade_label)."""
    data = [[P("Réf.", S_HEAD_W), P("Recommandation", S_HEAD_W), P("Cotation", S_HEAD_W_C)]]
    for ref, txt, grade in rows:
        data.append([P(ref, S_CELL_B), P(txt, S_CELL), chip(grade, width=17 * mm)])
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

RCW = [13 * mm, CW_FULL - 13 * mm - 16 * mm, 16 * mm]

def bullets(items, style=S_BODY_SM):
    html = "&bull; " + "<br/>&bull; ".join(items)
    return P(html, style)

def legend_flowable():
    chip_w = 17 * mm
    content_w = CW_FULL
    row = Table([[chip("AF", width=chip_w - 2 * mm),
                  P("<b>AF = Accord Fort</b> / <b>AF- = Accord Faible</b> — cotation à 2 tours "
                    "dérivée de RAND/UCLA (échelle 1-9, médiane + intervalle de confiance, "
                    "3 zones accord/indécision/désaccord). Le texte source n'imprime <b>pas</b> "
                    "de grade GRADE numérique par item (contrairement à d'autres RFE de ce "
                    "corpus) — seule la force verbale « il faut »/« il faut probablement » "
                    "distingue une recommandation forte d'une recommandation optionnelle, déjà "
                    "intégrée dans le libellé de chaque ligne. 54 recommandations comportant "
                    "74 votes internes (47 Accord Fort + 27 Accord Faible) — condensées ici en "
                    "62 lignes, sans jamais fusionner deux niveaux d'accord différents.",
                    S_BADGE_HEAD)]],
                colWidths=[chip_w, content_w - chip_w])
    row.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                              ("LEFTPADDING", (0, 0), (-1, -1), 1),
                              ("RIGHTPADDING", (0, 0), (-1, -1), 1),
                              ("TOPPADDING", (0, 0), (-1, -1), 0),
                              ("BOTTOMPADDING", (0, 0), (-1, -1), 0)]))
    return row

TOTAL_PAGES = {"n": 8}

def on_page(canvas, doc, page_title):
    header_band(canvas, doc, "SRLF / SFAR — RECOMMANDATIONS FORMALISÉES D'EXPERTS, 2014",
                "Réduction de l'utilisation des antibiotiques en réanimation",
                page_title, icon_fn=lambda c, x, y: icon_pill(c, x, y, 13 * mm), color=TEAL_DARK)
    footer_band(canvas, doc, SOURCE_TXT, f"Page {doc.page} / {TOTAL_PAGES['n']}")

# ---------------------------------------------------------------------------
def _section_intro_q1():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Résumé :</b> RFE SRLF/SFAR (adulte et pédiatrique) sur les stratégies de "
        "réduction de l'utilisation curative des antibiotiques en réanimation — 5 questions : "
        "résistance/épidémiologie, données microbiologiques, choix de l'antibiothérapie "
        "(carbapénèmes, quinolones, anti-SARM), optimisation de l'administration "
        "(indication, dosage/TDM, modalités), réévaluation et durée des traitements.",
        S_BODY), bg=BG_PANEL, border=TEAL_DARK))
    story.append(Spacer(1, 2.5 * mm))
    story.append(legend_flowable())
    story.append(Spacer(1, 3 * mm))
    story.append(KeepTogether([
        section_bar("Q1 — Résistance bactérienne, consommation d'antibiotiques et épidémiologie"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("1", "Il existe de nombreux arguments directs et indirects démontrant la relation "
         "entre consommation d'antibiotiques et résistance bactérienne.", "AF"),
        ("2", "Il faut utiliser des données françaises d'épidémiologie bactérienne globales "
         "et locales ; les sociétés savantes doivent diffuser les données des réseaux de "
         "surveillance (dont REARaisin) ; chaque unité/établissement doit disposer de "
         "données locales précisant la fréquence des espèces isolées et des résistances par "
         "espèce.", "AF"),
        ("3", "Il faut mesurer les Doses Définies Journalières (DDJ) d'antibiotiques pour "
         "toutes les unités de réanimation, globales et ciblées sur les classes à risque "
         "(carbapénèmes, fluoroquinolones notamment).", "AF-"),
    ], RCW))
    return story

# ---------------------------------------------------------------------------
def _section_q2():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Q2 — Données microbiologiques pour un moindre usage des antibiotiques"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("1", "Pour une désescalade rapide, il faut réaliser des prélèvements "
         "bactériologiques si possible avant toute antibiothérapie.", "AF"),
        ("2a", "Dans les PAVM, avant antibiothérapie, il faut probablement réaliser des "
         "prélèvements respiratoires avec culture quantitative pour réduire l'exposition "
         "aux antibiotiques ; il faut communiquer rapidement au clinicien l'examen "
         "microscopique direct d'un prélèvement respiratoire profond.", "AF"),
        ("2b", "Sous réserve des critères de qualité du prélèvement : en l'absence de signe "
         "de gravité, si l'examen direct est négatif, il ne faut probablement pas débuter "
         "d'antibiothérapie probabiliste ; en présence de signes de gravité, il faut "
         "probablement débuter une antibiothérapie adaptée à l'examen direct positif.", "AF-"),
        ("3", "Dans les 24h suivant le prélèvement, il faut qu'un premier résultat de "
         "culture soit rendu.", "AF"),
        ("4", "En cas d'hémoculture positive, il faut réaliser l'identification bactérienne "
         "et l'antibiogramme directement à partir du flacon d'hémoculture.", "AF"),
        ("5", "En cas de culture positive, il faut fournir l'identification bactérienne le "
         "plus rapidement possible par spectrométrie de masse, pour une adaptation plus "
         "précoce de l'antibiothérapie.", "AF-"),
        ("6", "Il faut déterminer et communiquer aux cliniciens les CMI recommandées par le "
         "CA-SFM ; il faut probablement, après discussion microbiologiste-clinicien, "
         "déterminer les CMI pour des sites infectés particuliers et certaines espèces "
         "bactériennes.", "AF"),
        ("7a", "Pneumonie communautaire : antigénurie pneumocoque positive → stopper les "
         "antibiotiques anti-bactéries intracellulaires ; antigénurie légionelle positive → "
         "stopper la bêta-lactamine ; antigénurie légionelle négative → ne pas exclure le "
         "diagnostic de légionellose.", "AF-"),
        ("7b", "Antigénurie pneumocoque négative → ne pas exclure le diagnostic de "
         "pneumopathie à pneumocoque.", "AF"),
        ("8", "En cas d'hémoculture positive à cocci Gram positif en amas, il faut utiliser "
         "des tests rapides détectant S. aureus et sa sensibilité à l'oxacilline.", "AF"),
    ], RCW))
    return story

# ---------------------------------------------------------------------------
def _section_q3ab():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Q3a — Impact de la colonisation sur le choix de l'antibiothérapie"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("1", "Il ne faut pas prescrire un traitement antibiotique systématique en cas "
         "d'identification d'une bactérie dans un prélèvement de colonisation, quel qu'en "
         "soit le type (notamment aspiration trachéo-bronchique).", "AF"),
        ("2", "En présence de signes de gravité, il faut intégrer la connaissance d'une "
         "colonisation à bactérie multi-résistante (BMR), quel que soit le site de "
         "prélèvement, dans le choix d'une antibiothérapie probabiliste.", "AF-"),
    ], RCW))
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Q3b — Diminuer l'utilisation des carbapénèmes"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("1a", "En traitement probabiliste, en cas d'infection bactérienne communautaire "
         "suspectée, il ne faut pas prescrire de carbapénème.", "AF"),
        ("1b", "Exception : un carbapénème peut être envisagé si le patient a un antécédent "
         "(&lt; 3 mois) de colonisation/infection à entérobactérie BLSE ou à P. aeruginosa "
         "résistant à la ceftazidime, ET un sepsis sévère ou choc septique.", "AF-"),
        ("2", "En traitement probabiliste, en cas d'infection bactérienne sévère associée "
         "aux soins/nosocomiale suspectée, il ne faut pas prescrire de carbapénème sur le "
         "seul critère du caractère nosocomial de l'infection.", "AF"),
        ("3", "Après documentation bactériologique, il faut rechercher une alternative aux "
         "carbapénèmes selon le site infecté, après discussion entre microbiologistes et "
         "cliniciens.", "AF"),
    ], RCW))
    return story

# ---------------------------------------------------------------------------
def _section_q3cd():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Q3c — Diminuer l'utilisation des quinolones"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("1a", "Il ne faut pas prescrire de fluoroquinolones (FQ) quand d'autres "
         "antibiotiques peuvent être utilisés ; exceptions possibles : légionelloses graves "
         "prouvées (association macrolide/rifampicine), infections osseuses/pied "
         "diabétique après antibiogramme.", "AF-"),
        ("1b", "Exception : prostatites, après antibiogramme.", "AF"),
        ("2", "Il ne faut pas prescrire de FQ de façon répétée chez un même patient "
         "(prendre en compte les prescriptions antérieures de FQ dans les 6 mois "
         "précédents, quelle qu'en soit l'indication).", "AF"),
        ("3", "Il ne faut pas prescrire en probabiliste de FQ en monothérapie dans les "
         "infections nosocomiales sévères.", "AF"),
        ("4", "Il ne faut pas prescrire de FQ sur des souches d'entérobactéries ayant "
         "acquis une résistance de premier niveau (acide nalidixique et/ou pipémidique).",
         "AF"),
        ("5a", "Dans le choc septique, en cas d'association avec une bêta-lactamine, il "
         "faut préférer les aminosides plutôt qu'une FQ.", "AF"),
        ("5b", "... y compris chez l'insuffisant rénal.", "AF-"),
    ], RCW))
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Q3d — Diminuer l'utilisation des anti-SARM — Traitement probabiliste"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("P1", "Il ne faut pas utiliser les anti-SARM dans le traitement probabiliste des "
         "infections communautaires vraies.", "AF"),
        ("P2", "Il faut prendre en compte la possibilité d'un SARM dans les infections "
         "sévères associées aux soins (patients hémodialysés chroniques, porteurs de "
         "plaies chroniques...).", "AF"),
        ("P3", "Il faut utiliser les anti-SARM selon l'épidémiologie locale du service pour "
         "le traitement probabiliste des infections nosocomiales acquises en réanimation.",
         "AF"),
    ], RCW))
    story.append(Spacer(1, 2 * mm))
    story.append(P("<b>Traitement documenté</b>", S_CELL_B))
    story.append(Spacer(1, 1 * mm))
    story.append(reco_table([
        ("D1", "Il ne faut probablement pas traiter une hémoculture isolée à staphylocoque "
         "blanc (SE), résistant ou non à l'oxacilline ; devant plusieurs hémocultures "
         "positives à SE résistant à l'oxacilline (SEMR), il faut probablement changer les "
         "cathéters centraux/artériels et décider d'un traitement selon la gravité, "
         "l'immunodépression et l'antibiotype.", "AF"),
        ("D2", "Sauf chez les patients immunodéprimés, il ne faut probablement pas mettre "
         "en route un traitement anti-SARM devant la présence à concentration "
         "significative de SEMR dans une PAVM.", "AF"),
        ("D3", "Il faut probablement utiliser la daptomycine à fortes doses dans les "
         "endocardites ou septicémies à SARM ayant une CMI à la vancomycine &gt; 1 mg/L.",
         "AF-"),
        ("D4", "Il faut probablement utiliser le linézolide dans les PAVM à SARM.", "AF"),
        ("D5", "Il faut probablement réaliser une CMI du SARM à la vancomycine ; en "
         "l'absence d'amélioration clinique après 3 jours pour une infection à SARM de CMI "
         "&gt; 1 mg/L, il faut probablement utiliser une alternative à la vancomycine.",
         "AF"),
        ("D6", "Il faut probablement discuter, selon le site infecté, l'intérêt d'une "
         "association anti-SARM.", "AF-"),
    ], RCW))
    return story

# ---------------------------------------------------------------------------
def _section_q4ab():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Q4a — Indication formelle de l'antibiothérapie"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("1", "Choc septique : il faut administrer une antibiothérapie probabiliste dans "
         "l'heure suivant la survenue du choc.", "AF"),
        ("2", "Suspicion de pneumonie communautaire sévère : il faut probablement "
         "envisager d'autres diagnostics avant toute antibiothérapie, dans un délai "
         "maximal de 4h après l'admission, pour éviter une prescription inutile.", "AF-"),
        ("3", "Méningite bactérienne : il faut administrer les antibiotiques dans les 3h "
         "après l'admission à l'hôpital, idéalement dans l'heure.", "AF"),
        ("4", "Il faut probablement raccourcir au maximum le délai d'administration de la "
         "1ère dose chez les patients « fragiles » (splénectomisé fébrile, neutropénique "
         "fébrile, dermo-hypodermite bactérienne nécrosante...).", "AF"),
    ], RCW))
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Q4b — Dosage des antibiotiques (TDM)"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("1", "Chez tout patient sévère (adulte ou pédiatrique) de réanimation, du fait "
         "d'une variabilité pharmacocinétique importante et imprévisible, il faut faire "
         "des dosages de certains antibiotiques.", "AF"),
        ("2", "Il faut doser le pic plasmatique d'aminoside 30 min après la 1ère dose "
         "(perfusion en 30 min) chez tout patient sévère ; une concentration inférieure à "
         "l'objectif attendu doit entraîner une augmentation de la dose suivante.", "AF-"),
        ("3", "Il faut un dosage de la concentration résiduelle d'aminoside pour éviter "
         "toute toxicité d'une réinjection trop précoce, a fortiori en cas d'insuffisance "
         "rénale.", "AF-"),
        ("4", "Chez l'adulte comme chez l'enfant, il faut doser la concentration de "
         "vancomycine à l'équilibre (perfusion continue après dose de charge) ou en "
         "résiduelle (perfusion discontinue).", "AF"),
        ("5", "Il faut probablement mesurer la concentration de certaines bêta-lactamines "
         "à large spectre, en résiduelle (administration discontinue/prolongée) ou à "
         "l'équilibre (perfusion continue).", "AF-"),
    ], RCW))
    return story

# ---------------------------------------------------------------------------
def _section_q4cd_q5_sources():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Q4c — Modalités d'administration des antibiotiques"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("1", "Infections sévères en réanimation : il faut probablement maintenir les "
         "concentrations plasmatiques de bêta-lactamines ≥ CMI pendant au moins 70 % du "
         "temps pour garantir le succès thérapeutique.", "AF-"),
        ("2", "Il faut probablement viser un objectif plus élevé (Cmin/CMI &gt; 4-6) dans "
         "certaines situations.", "AF"),
        ("3", "En réanimation, pour les infections sévères (a fortiori si CMI élevées), il "
         "faut probablement administrer les bêta-lactamines (céfépime, "
         "pipéracilline-tazobactam, méropénème...) en perfusion prolongée/continue.", "AF"),
        ("4a", "Il ne faut probablement pas administrer systématiquement les "
         "bêta-lactamines en perfusion continue, malgré un avantage théorique démontré en "
         "pharmacocinétique.", "AF-"),
        ("4b", "Il faut probablement réserver cette modalité (carbapénèmes méropénème/"
         "doripénème, ceftazidime, pipéracilline-tazobactam) au traitement des infections "
         "sévères à risque d'échec pharmacodynamique (foyers profonds, pharmacocinétique "
         "altérée, CMI élevées).", "AF-"),
        ("5", "Il faut probablement administrer la vancomycine en perfusion continue, "
         "après dose de charge, pour obtenir plus rapidement les concentrations cibles.",
         "AF"),
        ("6", "Il faut probablement utiliser des modalités d'administration prolongée/"
         "continue pour prévenir l'émergence de résistance bactérienne (certaines "
         "souches).", "AF-"),
    ], RCW))
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Q4d — Associations d'antibiotiques"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("1", "En l'absence de facteur de risque de BMR, il faut traiter en probabiliste "
         "les pneumopathies nosocomiales en monothérapie.", "AF-"),
        ("2", "Il faut traiter par une association probabiliste les patients en état de "
         "choc, neutropéniques, ou suspects d'infection à BMR.", "AF"),
    ], RCW))
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Q5 — Réévaluation et durée des traitements antibiotiques"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("1", "Il faut une réévaluation de l'antibiothérapie chez tous les patients de "
         "réanimation au plus tard à 48-72h, avec désescalade selon la situation clinique "
         "et les données microbiologiques.", "AF"),
        ("2a", "Procalcitonine (PCT) : il faut probablement l'utiliser pour guider "
         "l'interruption des antibiotiques (notamment infections respiratoires basses) — "
         "PCT &lt; 0,5 ng/mL ou baisse &gt; 80 % du pic → antibiothérapie peut être "
         "arrêtée.", "AF-"),
        ("2b", "Il faut probablement mettre en place des recommandations locales "
         "structurant cette réévaluation pour réduire l'exposition aux antibiotiques.",
         "AF"),
        ("2c", "Il faut probablement doser la PCT toutes les 48-72h au-delà de J3 pour "
         "réduire la durée de l'antibiothérapie.", "AF-"),
        ("3", "PAVM chez un patient non immunodéprimé, antibiothérapie initiale adaptée : "
         "il faut limiter la durée totale de l'antibiothérapie à 8 jours.", "AF-"),
        ("4", "En dehors de situations cliniques particulières, il faut probablement "
         "limiter à 5-7 jours le traitement d'une infection communautaire.", "AF"),
        ("5", "En dehors d'une bactériémie à S. aureus ou compliquée de métastases "
         "infectieuses, il faut probablement limiter à 5-7 jours le traitement d'une "
         "bactériémie liée au cathéter si les hémocultures se négativent.", "AF"),
        ("6", "Il faut probablement mettre en place une concertation pluridisciplinaire "
         "pour améliorer l'adéquation des antibiothérapies, augmenter le taux de "
         "désescalade et limiter leur consommation.", "AF"),
        ("7", "Il faut probablement mettre en place des protocoles d'antibiothérapie pour "
         "améliorer le pronostic des patients et limiter l'émergence de résistances.",
         "AF"),
    ], RCW))
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("Sources et avertissement"))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "SRLF/SFAR, avec GFRUP/SFM/SPILF/SF2H, « Stratégies de réduction de l'utilisation "
        "des antibiotiques à visée curative en réanimation (adulte et pédiatrique) », RFE, "
        "Juin 2014. Méthode GRADE + cotation RAND/UCLA à 2 tours. 228 références "
        "bibliographiques citées dans le texte intégral (non reproduites ici) ; "
        "composition nominative du groupe d'experts (non reproduite).", S_SOURCE))
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Avertissement :</b> cette fiche est une synthèse indépendante, produite pour un "
        "usage d'aide-mémoire. Elle reprend intégralement les 74 votes du texte source "
        "(condensés en 62 lignes, sans jamais fusionner deux niveaux d'accord différents) "
        "mais condense l'argumentaire de chaque item et omet la composition nominative du "
        "groupe d'experts. Elle ne remplace pas le texte intégral et n'est ni éditée ni "
        "validée par la SRLF/SFAR.", S_BODY_SM), bg=GREY_LIGHT, border=GREY))
    return story

# ---------------------------------------------------------------------------
def _section_all():
    story = _section_intro_q1()
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_q2())
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_q3ab())
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_q3cd())
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_q4ab())
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_q4cd_q5_sources())
    return story

SECTIONS = [
    ("Réduction de l'utilisation des antibiotiques en réanimation", _section_all),
]

def _make_doc(path=None):
    return SimpleDocTemplate(path or OUT, pagesize=A4,
                              leftMargin=MARGIN, rightMargin=MARGIN,
                              topMargin=32 * mm, bottomMargin=16 * mm,
                              title="Fiche SRLF-SFAR 2014 - Reduction antibiotiques reanimation",
                              author="Synthèse indépendante (source SRLF/SFAR)")

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

    final_story = _build_upto(fns)
    docf = _make_doc()
    docf.build(final_story, onFirstPage=on_page_final, onLaterPages=on_page_final)
    print("OK ->", OUT, f"({total_pages} pages)")

if __name__ == "__main__":
    build()
