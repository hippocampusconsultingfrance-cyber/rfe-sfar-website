# -*- coding: utf-8 -*-
"""
Fiche de synthese - Societe Francaise d'Anesthesie et de Reanimation (SFAR) &
Societe de Reanimation de Langue Francaise (SRLF). "Prevention des infections
nosocomiales en reanimation (transmission croisee et nouveau-ne exclus)" -
5e Conference de Consensus, 20 novembre 2008 (en ligne 31/10/2009). President
du jury : J. Duranteau. Ann Fr Anesth Reanim 28 (2009) 912-920
(doi:10.1016/j.annfar.2009.09.007). 9 pages, telecharge depuis sfar.org
(wp-content/uploads/2015/10/2_AFAR_Prevention-des-infections-nosocomiales-en
-reanimation-transmission-croisee-et-nouveau-ne-exclus.pdf).

METHODOLOGIE - CONVENTION BESPOKE (10e distincte de ce corpus) : le texte
source annonce explicitement s'inspirer de GRADE, mais n'imprime JAMAIS de
symbole "Grade 1+/2-" - la force est exprimee uniquement par la locution
verbale elle-meme, que le texte source associe lui-meme a la distinction
GRADE forte/faible ("la formulation des recommandations - il faut faire ou
il ne faut pas faire, il faut probablement faire ou ne pas faire - a des
implications claires"). Chips utilises, transcription directe de cette
equivalence explicitement enoncee par la source (pas une invention) :
1+ = "il faut" / "est recommande" / "le Jury recommande" (fort, positif) ;
1- = "il ne faut pas" / "n'est pas recommande(e)" / "doit etre proscrit(e)"
(fort, negatif) ; 2+ = "il faut probablement" / "peut probablement etre
recommande(e)" (faible, positif) ; 2- = "il ne faut (probablement) pas"
(faible, negatif). Chip "0/" (meme convention que la fiche alr_douleur_
chronique de ce corpus) pour les enonces ou le jury declare explicitement
qu'aucune recommandation/position n'est possible ("le jury ne peut se
prononcer", "donnees insuffisantes pour recommander", "peu d'arguments
pour preconiser") - distinct d'un grade negatif.

COUVERTURE : integralite des enonces de recommandation des 5 questions
(epidemiologie/definitions, organisation architecturale, antibiotherapie,
preventions specifiques [poumon/PAVM, urine, catheters, site operatoire,
C. difficile], strategie globale). Les 5 encadres de criteres diagnostiques
(pneumopathies, IU, bacteriemies, ILC, ISO) sont condenses en tableaux de
reference (seuils numeriques et criteres cles preserves verbatim) plutot
que retranscrits en prose integrale - ce sont des definitions/criteres
diagnostiques, pas des recommandations gradees, et leur formulation
source est tres repetitive/tabulable. Le Tableau 1 (epidemiologie
descriptive REA Raisin 2006) est reproduit verbatim en tant que vrai
tableau chiffre. Argumentaire scientifique minimal (regle de projet
2026-09-14) - conserves uniquement les seuils/valeurs qui changent la
pratique (ex. 25-30 cmH2O pour la pression du ballonnet, surpression
15 Pa pour les chambres a haut risque aspergillaire).
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from style import *
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.units import mm

OUT = "/home/user/rfe-sfar-website/output/Fiche_SFAR_SRLF_Infections_Nosocomiales_Reanimation_2009.pdf"

SOURCE_TXT = ("Source : « Prévention des infections nosocomiales en réanimation » — "
              "5e Conférence de Consensus SFAR/SRLF, Ann Fr Anesth Réanim 28 (2009) "
              "912-920. Fiche de synthèse non officielle : se référer au texte intégral.")

def P(txt, style=S_CELL):
    return Paragraph(txt, style)

def chip(label, **kw):
    return grade_chip(label, **kw)

CW_FULL = PAGE_W - 2 * MARGIN
RCW = [CW_FULL - 14 * mm, 14 * mm]
TCW = [50 * mm, CW_FULL - 50 * mm]

def reco_table(rows, col_widths=RCW):
    data = [[P("Recommandation", S_HEAD_W), P("Force", S_HEAD_W_C)]]
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

def theme_table(rows, col_widths=TCW, head=("Type", "Critères / seuils clés")):
    data = [[P(head[0], S_HEAD_W), P(head[1], S_HEAD_W)]]
    for theme, detail in rows:
        data.append([P(theme, S_CELL_B), P(detail, S_CELL)])
    t = Table(data, colWidths=col_widths, repeatRows=1)
    style_cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), NAVY), ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTNAME", (0, 0), (-1, 0), FONT_BOLD), ("FONTSIZE", (0, 0), (-1, 0), 8),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
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
    chip_w = 14 * mm
    content_w = CW_FULL
    row = Table([[chip("1+", width=chip_w - 2 * mm), chip("1-", width=chip_w - 2 * mm),
                  chip("2+", width=chip_w - 2 * mm), chip("2-", width=chip_w - 2 * mm),
                  chip("0/", width=chip_w - 2 * mm),
                  P("<b>Force</b> — cette conférence de consensus n'imprime jamais de "
                    "symbole GRADE ; les chips ci-dessous sont une transcription directe "
                    "des locutions du texte, que la source associe elle-même à la "
                    "distinction GRADE forte/faible. <b>1+</b> = « il faut »/recommandé "
                    "(fort, positif) ; <b>1-</b> = « il ne faut pas »/non recommandé "
                    "(fort, négatif) ; <b>2+</b> = « il faut probablement » (faible, "
                    "positif) ; <b>2-</b> = « il ne faut (probablement) pas » (faible, "
                    "négatif) ; <b>0/</b> = le jury déclare explicitement qu'aucune "
                    "position n'est possible (absence de donnée) — n'est PAS un grade "
                    "négatif.", S_BADGE_HEAD)]],
                colWidths=[chip_w] * 5 + [content_w - 5 * chip_w])
    row.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                              ("LEFTPADDING", (0, 0), (-1, -1), 1),
                              ("RIGHTPADDING", (0, 0), (-1, -1), 1),
                              ("TOPPADDING", (0, 0), (-1, -1), 0),
                              ("BOTTOMPADDING", (0, 0), (-1, -1), 0)]))
    return row

TOTAL_PAGES = {"n": 8}

def on_page(canvas, doc, page_title):
    header_band(canvas, doc, "SFAR / SRLF — 5e Conférence de Consensus, 2008/2009",
                "Prévention des infections nosocomiales en réanimation",
                page_title, icon_fn=lambda c, x, y: icon_shield(c, x, y, 13 * mm), color=TEAL_DARK)
    footer_band(canvas, doc, SOURCE_TXT, f"Page {doc.page} / {TOTAL_PAGES['n']}")

# ---------------------------------------------------------------------------
def _section_intro():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Résumé :</b> 5e Conférence de Consensus SFAR/SRLF (2008/2009) sur la "
        "prévention des infections nosocomiales (IN) en réanimation adulte et "
        "pédiatrique — transmission croisée et nouveau-né explicitement exclus du "
        "champ (traités par d'autres textes). Cinq questions : épidémiologie et "
        "définitions, organisation architecturale, impact de l'antibiothérapie, "
        "préventions spécifiques (poumon, cathéter, urine, site opératoire, autres), "
        "stratégie globale.", S_BODY), bg=GREY_LIGHT, border=GREY))
    story.append(Spacer(1, 2.5 * mm))
    story.append(legend_flowable())
    return story

def _section_q1():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Q1 — Épidémiologie et définitions"),
        Spacer(1, 1.5 * mm),
        P("Une infection nosocomiale (IN) en réanimation se définit comme une "
          "infection contractée en réanimation, absente et non en incubation à "
          "l'admission, avec un délai d'au moins 48h entre l'admission et l'état "
          "infectieux. En 2006, prévalence France IN réa adulte : 22,4 % (InVS) ; "
          "taux d'attaque global 15 % (réseau REA Raisin). Les pneumopathies "
          "nosocomiales sont les IN les plus fréquentes chez l'adulte.", S_BODY_SM),
    ]))
    story.append(Spacer(1, 1.5 * mm))
    story.append(reco_table([
        ("Surveiller la survenue des IN dans les unités de réanimation (taux "
         "d'attaque, taux d'incidence, écologie bactérienne).", "1+"),
        ("Pour les IN prises en compte par les réseaux français (pneumopathies, "
         "infections urinaires, bactériémies, infections liées aux cathéters), "
         "utiliser les critères diagnostiques du CTINILS, compatibles avec le "
         "réseau européen HELICS ICU.", "1+"),
    ]))
    story.append(Spacer(1, 2 * mm))
    story.append(P("<b>Critères diagnostiques clés</b> (Encadrés 1-5 de la source, "
                    "condensés — seuils numériques préservés verbatim)", S_CELL_B))
    story.append(Spacer(1, 1 * mm))
    story.append(theme_table([
        ("Pneumopathie", "Signes radiologiques + fièvre >38°C ou leucopénie "
         "(<4000/mm³)/hyperleucocytose (>12 000/mm³) + signes respiratoires. "
         "Documentation microbiologique fortement recommandée : LBA >10<super>4</super> UFC/mL, "
         "brosse de Wimberley >10<super>3</super> UFC/mL, PDP >10<super>3</super> UFC/mL (cas 1) ; bactériologie "
         "quantitative sécrétions bronchiques >10<super>6</super> UFC/mL sans ATB antérieure "
         "(cas 2) ; méthodes alternatives — hémocultures, culture pleurale, "
         "histologie (cas 3). Cas 4/5 (sans critère quantitatif ou microbiologique) "
         "= pneumonie possible/clinique."),
        ("Infection urinaire", "Signe clinique (fièvre >38°C, impériosité, "
         "pollakiurie, brûlure mictionnelle, douleur sus-pubienne) + sans sondage : "
         "leucocyturie ≥10<super>4</super>/mL et uroculture ≥10<super>3</super> microorg./mL (≤2 espèces) ; avec "
         "sondage (en cours ou <7j) : uroculture ≥10<super>5</super> microorg./mL (≤2 espèces)."),
        ("Bactériémie", "Au moins 1 hémoculture positive justifiée cliniquement ; "
         "pour les germes saprophytes/commensaux (staph. coagulase-négative, "
         "Bacillus spp., Corynebacterium spp., etc.), 2 hémocultures positives au "
         "même germe, prélevées à des moments différents (délai max 48h)."),
        ("Infection liée au cathéter (ILC)", "CVC : bactériémie/fongémie dans les "
         "48h encadrant le retrait + culture positive du site/CVC ≥10<super>3</super> UFC/mL, ou "
         "hémocultures centrale/périphérique positives au même germe (ratio >5 ou "
         "délai différentiel >2h). Sans bactériémie : culture CVC ≥10<super>3</super> UFC/mL + "
         "purulence de l'orifice (ILC locale) ou régression des signes généraux "
         "sous 48h après ablation (ILC générale)."),
        ("Infection du site opératoire (ISO)", "Superficielle : dans les 30 jours, "
         "écoulement purulent, ou germe + polynucléaires à l'examen direct, ou "
         "ouverture par le chirurgien + signe inflammatoire. Profonde : dans les "
         "30 jours (1 an si implant/prothèse), écoulement purulent d'un drain "
         "sous-aponévrotique, ou déhiscence/ouverture + fièvre >38°C ou douleur "
         "localisée, avec documentation microbiologique."),
    ]))
    story.append(Spacer(1, 2 * mm))
    story.append(KeepTogether([
        P("<b>Tableau 1 — Épidémiologie descriptive des IN en réanimation "
          "adulte</b> (réseau REA Raisin 2006, taux pour 100 patients ou "
          "1000 jours d'exposition, reproduit verbatim).", S_CELL_B),
        Spacer(1, 1 * mm),
        _tableau1_epidemio(),
    ]))
    return story

def _tableau1_epidemio():
    head = ["Indicateur", "Pneumonies", "IU", "Bactériémies", "ILC (CVC)"]
    rows = [
        ["Incidence globale / 100 patients", "8,52", "6,46", "3,42", "1,30"],
        ["Attaque spécifique / 100 patients exposés", "13,49", "7,82", "3,42", "2,18"],
        ["Incidence / 1000 jours d'exposition", "16,17", "7,94", "3,27", "1,86"],
    ]
    data = [[P(h, S_HEAD_W_C) for h in head]]
    for r in rows:
        data.append([P(r[0], S_CELL_B)] + [P(v, S_CELL_C) for v in r[1:]])
    cw = [CW_FULL * 0.40] + [CW_FULL * 0.15] * 4
    t = Table(data, colWidths=cw, repeatRows=1)
    style_cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), NAVY), ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTNAME", (0, 0), (-1, 0), FONT_BOLD), ("FONTSIZE", (0, 0), (-1, 0), 7.6),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("GRID", (0, 0), (-1, -1), 0.5, GREY_LIGHT),
        ("TOPPADDING", (0, 0), (-1, -1), 3.2), ("BOTTOMPADDING", (0, 0), (-1, -1), 3.2),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            style_cmds.append(("BACKGROUND", (0, i), (-1, i), BG_PANEL))
    t.setStyle(TableStyle(style_cmds))
    return t

def _section_q2():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Q2 — Organisation architecturale"),
        Spacer(1, 1.5 * mm),
        P("Question centrée sur le lien entre architecture et prévention des IN "
          "(circulaire DHOS/SDO n°2003/413 du 27 août 2003).", S_BODY_SM),
    ]))
    story.append(Spacer(1, 1 * mm))
    story.append(reco_table([
        ("Répartir les lits en sous-unités, pour une meilleure sectorisation des "
         "patients et professionnels en cas d'épidémie.", "2+"),
        ("Prévoir des chambres individuelles d'au moins 20 m² (lien avec la "
         "prévention des IN non formellement démontré, mais recommandé par le "
         "Jury dans le cadre d'une stratégie globale).", "1+"),
        ("Un seul point d'eau par chambre est probablement suffisant (la qualité "
         "d'eau recommandée étant identique pour l'hygiène des mains et la "
         "toilette du patient) — le Jury nuance ainsi la circulaire qui en "
         "recommande deux.", "2+"),
        ("Le point d'eau doit être équipé d'une vasque large et profonde, de "
         "forme arrondie et sans aspérité, dépourvue de trop-plein, avec une "
         "commande autre que manuelle et un col de cygne démontable fixé au "
         "mur ; le matériau des surfaces doit répondre aux textes "
         "réglementaires.", "1+"),
        ("Ne pas recommander de filtre antibactérien sur le point d'eau si la "
         "qualité de l'eau est maîtrisée.", "1-"),
        ("Une porte à commande autre que manuelle est souhaitable, en tenant "
         "compte des conséquences pour le patient (sécurité, isolement).", "2+"),
        ("À l'occasion d'une restructuration, prévoir un traitement d'air adapté : "
         "patients à haut risque aspergillaire — surpression 15 Pa, ≥20 volumes "
         "d'air/heure, filtre HEPA (ou système portable à défaut) ; patients à "
         "risque aéroporté — dépression 2,5 Pa, ~12 volumes/heure, extraction "
         "directe vers l'extérieur.", "1+"),
        ("Utiliser de l'eau stérile pour toutes les situations de soins à "
         "risque ; réserver l'eau chaude sanitaire à la toilette, au nettoyage du "
         "matériel et à l'entretien des locaux.", "1+"),
    ]))
    return story

def _section_q3():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Q3 — Impact de l'antibiothérapie sur la prévention des IN"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("Appliquer la désescalade antibiotique (réévaluation systématique entre "
         "H24 et H72 selon les résultats microbiologiques) pour prévenir "
         "l'émergence de germes résistants.", "1+"),
        ("Appliquer également la désescalade pour prévenir les IN elles-mêmes ; "
         "si l'infection n'est pas confirmée, interrompre l'antibiothérapie "
         "plutôt que la maintenir.", "2+"),
        ("Pour les PAVM, réduire la durée de traitement antibiotique de 15 à "
         "8 jours, en dehors des infections à bacilles Gram négatif non "
         "fermentants (Pseudomonas, Acinetobacter, Stenotrophomonas).", "1+"),
        ("En contexte épidémique, mettre en place une politique restrictive "
         "d'utilisation des antibiotiques, avec séniorisation de la prescription "
         "et collaboration avec un référent en antibiothérapie.", "2+"),
        ("Ne pas recommander la rotation programmée (cycling) des antibiotiques "
         "en usage courant, en raison du risque d'émergence de résistance.", "1-"),
        ("En situation épidémique, utiliser probablement la rotation en cycles "
         "courts d'un mois maximum.", "2+"),
        ("Le mélange programmé (mixing) d'antibiothérapie sur patients "
         "consécutifs : le jury ne peut se prononcer sur son intérêt dans la "
         "prévention des IN (données actuelles insuffisantes).", "0/"),
        ("Mettre en place une stratégie de rationalisation de l'antibiothérapie "
         "(désescalade, durée, gestion des épidémies à BMR) — réduit "
         "l'émergence de résistances, la survenue d'IN et le coût du "
         "traitement. Recommandations identiques chez l'enfant.", "1+"),
    ]))
    return story

def _section_q4_poumon():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Q4 — Préventions spécifiques : infections pulmonaires (PAVM)"),
        Spacer(1, 1.5 * mm),
        P("PAVM précoces (≤5 jours d'intubation, germes communautaires) vs. "
          "tardives (>5 jours, flore hospitalière).", S_BODY_SM),
    ]))
    story.append(Spacer(1, 1 * mm))
    story.append(reco_table([
        ("Ne pas recommander l'antibioprophylaxie systématique après "
         "l'intubation (diminue les PAVM précoces mais sans effet sur la "
         "mortalité, les PAVM tardives ou la durée de ventilation).", "2-"),
        ("Recommander probablement la décontamination naso- et oropharyngée par "
         "solution antiseptique (rapport bénéfice/risque favorable).", "2+"),
        ("Ne pas recommander l'utilisation d'un antibiotique local (seul ou "
         "associé à l'antiseptique) — efficacité non démontrée.", "1-"),
        ("La décontamination digestive sélective (DDS) associée à une "
         "antibiothérapie systémique peut probablement être recommandée "
         "(diminue PAVM et mortalité) ; ne pas la recommander dans les unités à "
         "forte prévalence de SARM ou entérocoques résistants à la "
         "vancomycine (surveillance renforcée de l'écologie bactérienne "
         "requise).", "2+"),
        ("Chez l'enfant, la DDS seule ne peut pas être recommandée (efficacité "
         "non prouvée).", "1-"),
        ("Ne pas recommander l'antibiothérapie inhalée/en instillation "
         "trachéale, ni les peptides antimicrobiens, dans la prévention des "
         "PAVM.", "1-"),
        ("Utiliser un algorithme de sédation-analgésie pour réduire la durée de "
         "ventilation mécanique (adulte et enfant) ; une procédure prévenant "
         "les extubations non programmées est recommandée.", "1+"),
        ("Privilégier la ventilation non invasive dans ses indications reconnues "
         "(bénéfice sur l'incidence des PAVM, notamment chez le patient BPCO).", "1+"),
        ("Utiliser probablement l'intubation orotrachéale plutôt que "
         "nasotrachéale pour diminuer la survenue de sinusites (lien non "
         "formellement démontré).", "2+"),
        ("Chez le nourrisson (sinus maxillaires non pneumatisés avant 6-8 ans, "
         "et la voie orale augmente le risque de micro-inhalations et "
         "d'extubation accidentelle), l'intubation nasotrachéale doit être "
         "recommandée.", "1+"),
        ("Maintenir la pression du ballonnet des sondes entre 25 et 30 cmH2O, "
         "pour limiter les micro-inhalations tout en préservant la muqueuse "
         "trachéale (20-25 cmH2O chez l'enfant avec sonde à ballonnet).", "1+"),
        ("Chez l'enfant, utiliser probablement des sondes à ballonnet (protection "
         "possible contre les micro-inhalations, sans majoration du risque "
         "d'œdème sous-glottique) ; l'aspiration sous-glottique n'est pas "
         "applicable en dessous de 10 ans faute de dispositif adapté.", "2+"),
        ("Privilégier une sonde d'intubation à aspiration sous-glottique "
         "(réduit probablement l'incidence des PAVM précoces), en aspiration "
         "discontinue plutôt que continue.", "2+"),
        ("Éviter le décubitus dorsal strict sauf indication particulière ; "
         "privilégier une position proclive d'au moins 30°.", "1+"),
        ("Ne pas recommander le système clos d'aspiration trachéale dans le "
         "seul objectif de prévenir les PAVM.", "1-"),
    ]))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P("<i>Sans effet démontré sur l'incidence des PAVM (ni recommandés "
                    "ni déconseillés pour cet objectif précis) : sondes imprégnées "
                    "d'antiseptiques, trachéotomie précoce, lit rotatif, systèmes "
                    "d'humidification des gaz inspirés, décubitus ventral, nutrition "
                    "entérale ; la prévention anti-ulcéreuse n'augmente pas l'incidence "
                    "des PAVM.</i>", S_NOTE))
    return story

def _section_q4_urine():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Q4 — Infection urinaire"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("Ne pas rechercher systématiquement une bactériurie chez les patients "
         "asymptomatiques porteurs d'un cathéter vésical.", "1-"),
        ("En cas de bactériurie asymptomatique, ne pas changer systématiquement "
         "la sonde urinaire (risque de bactériémie) ; peu d'arguments pour une "
         "antibiothérapie systémique lors d'un changement de sonde.", "1-"),
        ("Discuter systématiquement l'indication du sondage urinaire et en "
         "limiter la durée au strict nécessaire (évaluation quotidienne).", "1+"),
        ("Ne pas recommander l'utilisation de sondes imprégnées (antiseptiques, "
         "antibiotiques, argent) — aucune efficacité supérieure démontrée ; "
         "aucun système de drainage fermé complexe n'a montré de supériorité "
         "sur un système semi-ouvert.", "1-"),
        ("Ne pas recommander l'irrigation vésicale par antibiotique/antiseptique "
         "ni l'adjonction d'un antimicrobien dans le système clos.", "1-"),
    ]))
    return story

def _section_q4_catheters():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Q4 — Infections liées aux cathéters (ILC)"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("Ne pas recommander l'utilisation systématique de cathéters imprégnés "
         "d'antiseptiques/antibiotiques (coût élevé, risque de sélection de "
         "BMR/levures) ; ils peuvent trouver leur indication dans les unités où "
         "l'incidence d'ILC reste élevée malgré les autres mesures.", "1-"),
        ("Utiliser une solution antiseptique alcoolique (chlorhexidine ou "
         "povidone iodée) pour la préparation cutanée ; proscrire les "
         "solutions aqueuses.", "1+"),
        ("Insérer les cathéters en territoire cave supérieur plutôt qu'inférieur "
         "(risque accru d'ILC en territoire cave inférieur) ; encadrer ce geste "
         "par un médecin expérimenté.", "1+"),
        ("Ne pas refaire le pansement plus d'une fois toutes les 72 heures, sauf "
         "souillure ou perte d'étanchéité ; les lignes de perfusion peuvent "
         "n'être changées que tous les 3-4 jours ; changer les tubulures après "
         "chaque transfusion ou quotidiennement lors de perfusion d'émulsions "
         "lipidiques.", "1+"),
        ("Ne pas recommander (efficacité non démontrée) : antibioprophylaxie à "
         "l'insertion, pommade antibiotique, filtres antibactériens, boîtiers "
         "protecteurs, changement systématique du cathéter à intervalle "
         "régulier.", "1-"),
        ("Chez l'enfant, les données sont insuffisantes pour recommander la "
         "tunnélisation systématique des cathéters fémoraux (réduit la "
         "colonisation mais pas les infections), ni l'utilisation de patch "
         "cutané à la chlorhexidine (dermites rapportées).", "0/"),
        ("Chez l'enfant de moins de 30 mois, utiliser la chlorhexidine "
         "alcoolique (povidone iodée répétée contre-indiquée, risque "
         "d'hypothyroïdie).", "1+"),
        ("Ne pas recommander les verrous antibiotiques ni l'imprégnation "
         "antibiotique systématique des cathéters.", "1-"),
        ("Il n'y a pas de preuve qu'une prophylaxie antithrombotique prévienne "
         "la survenue d'ILC (le jury ne peut se prononcer sur les cathéters "
         "imprégnés d'héparine, données insuffisantes).", "0/"),
        ("Recommander le site radial pour les cathéters artériels (études "
         "observationnelles).", "1+"),
    ]))
    return story

def _section_q4_iso_cdiff():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Q4 — Infection du site opératoire (ISO) & autres"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("Antibioprophylaxie périopératoire, patient communautaire admis en "
         "réanimation pour être opéré : respecter les règles habituelles.", "1+"),
        ("Antibioprophylaxie périopératoire, patient déjà hospitalisé et devant "
         "être opéré : tenir probablement compte de l'écologie bactérienne de "
         "l'unité et/ou de la colonisation du patient.", "2+"),
        ("Antibioprophylaxie périopératoire, patient déjà sous antibiothérapie "
         "et devant être opéré : poursuivre l'antibiothérapie en cours "
         "(l'antibioprophylaxie devrait tenir compte du traitement en cours, du "
         "site opéré et de l'écologie bactérienne de l'unité).", "1+"),
        ("Le contrôle glycémique peut probablement être recommandé pour prévenir "
         "les ISO en chirurgie cardiaque spécifiquement (données insuffisantes "
         "pour les autres mesures en réanimation : décontamination "
         "naso-oropharyngée, type de pansement, oxygénothérapie, contrôle de "
         "la température).", "2+"),
    ]))
    story.append(Spacer(1, 2 * mm))
    story.append(P("<b>Infection digestive à Clostridium difficile</b> — diarrhée ou "
                    "mégacolon toxique sans autre cause, avec toxine A/B dans les "
                    "selles ou colite pseudomembraneuse ; incidence faible (<5 %), "
                    "favorisée par clindamycine, céphalosporines, fluoroquinolones.",
                    S_BODY_SM))
    story.append(Spacer(1, 1 * mm))
    story.append(reco_table([
        ("Éradiquer les spores par désinfection du matériel et nettoyage des "
         "surfaces par solutions chlorées ; le lavage des mains au savon doux "
         "reste nécessaire (les solutions hydroalcooliques n'éliminent pas les "
         "spores).", "1+"),
        ("Ne pas traiter de façon préventive les patients sous antibiotiques ou "
         "porteurs asymptomatiques.", "1-"),
    ]))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P("<i>Chez l'enfant, les colites à C. difficile sont exceptionnelles "
                    "— la majorité des IN digestives pédiatriques est due au "
                    "Rotavirus, dont les seules mesures préventives sont celles de la "
                    "transmission croisée (hors champ de cette conférence).</i>",
                    S_NOTE))
    return story

def _section_q5_sources():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Q5 — Stratégie globale"),
        Spacer(1, 1.5 * mm),
        P("Le respect du ratio réglementaire des effectifs soignants est un "
          "prérequis fondamental à toute stratégie de prévention.", S_BODY_SM),
    ]))
    story.append(Spacer(1, 1 * mm))
    story.append(reco_table([
        ("Utiliser une stratégie globale de prévention des ILC et des PAVM "
         "(adulte et enfant) — combine surveillance épidémiologique, programme "
         "d'éducation multidisciplinaire, mesures générales et spécifiques.", "1+"),
        ("Généraliser probablement cette stratégie globale aux autres IN "
         "(infection urinaire, ISO), malgré l'absence de données spécifiques "
         "les concernant.", "2+"),
        ("Intégrer un réseau régional ou national de surveillance des IN.", "2+"),
        ("Mettre en place un programme de formation et d'éducation de tous les "
         "acteurs de soin aux règles d'hygiène et procédures spécifiques, avec "
         "pratiques standardisées et diffusées à l'ensemble des équipes.", "1+"),
        ("Respecter les bonnes pratiques d'hygiène hospitalière de base "
         "(asepsie, port de gants, lavage des mains), associées à des "
         "précautions additionnelles selon le contexte (isolement, masque) ; "
         "limiter l'exposition aux dispositifs invasifs par évaluation "
         "quotidienne de leur indication.", "1+"),
        ("Le contrôle glycémique permet probablement de limiter la survenue "
         "d'IN, dans le cadre d'une politique de bon usage des antibiotiques "
         "(restriction, désescalade, limitation des durées).", "2+"),
    ]))
    story.append(Spacer(1, 4 * mm))
    story.append(section_bar("Sources et traçabilité", color=GREY))
    story.append(Spacer(1, 2 * mm))
    story.append(P(
        "<b>Document source :</b> « Prévention des infections nosocomiales en "
        "réanimation (transmission croisée et nouveau-né exclus) » — 5e Conférence "
        "de Consensus, SFAR/SRLF, jeudi 20 novembre 2008. Président du jury : "
        "J. Duranteau (Le Kremlin-Bicêtre). Membres du jury : R. Amathieu, "
        "C. Guérin, P. Guiot, C. Guitton, C. Ichai, N. Kermarrec, C. Lejus, "
        "F. Lesage, J. Mantz, P.-F. Perrigault, C. Schwebel, M. Sirodot. Comité "
        "d'organisation : E. L'Her (président).", S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P("<b>Version :</b> Ann Fr Anesth Réanim 28 (2009) 912-920, en ligne "
                    "le 31/10/2009. doi:10.1016/j.annfar.2009.09.007.", S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P("<b>Méthodologie :</b> inspirée de GRADE, formulée en locutions "
                    "verbales (« il faut »/« il faut probablement ») plutôt qu'en "
                    "symboles imprimés — voir légende en page 1.", S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>URL source :</b> https://sfar.org/wp-content/uploads/2015/10/"
        "2_AFAR_Prevention-des-infections-nosocomiales-en-reanimation-transmission"
        "-croisee-et-nouveau-ne-exclus.pdf", S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P("<b>Couverture :</b> intégralité des recommandations des 5 "
                    "questions. Transmission croisée et nouveau-né explicitement "
                    "exclus du champ par la source elle-même (traités par d'autres "
                    "textes). Encadrés diagnostiques condensés en tableaux de "
                    "référence (seuils numériques préservés) plutôt que retranscrits "
                    "en prose intégrale.", S_SOURCE))
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Avertissement — document de 2008/2009 :</b> cette fiche de synthèse "
        "indépendante reprend l'intégralité des recommandations du texte source, "
        "mais ne le remplace pas et n'est ni éditée ni validée par la SFAR/SRLF. "
        "Les pratiques de prévention des infections nosocomiales ayant pu évoluer "
        "depuis 2009, se référer à un avis spécialisé et aux recommandations "
        "actualisées avant toute décision.", S_BODY_SM), bg=GREY_LIGHT, border=GREY))
    return story

def _section_intro_q1():
    story = _section_intro()
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_q1())
    return story

def _section_q3_poumon():
    story = _section_q3()
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_q4_poumon())
    return story

def _section_catheters_iso_cdiff_q5_sources():
    story = _section_q4_catheters()
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_q4_iso_cdiff())
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_q5_sources())
    return story

def _section_intro_q1_q2():
    story = _section_intro_q1()
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_q2())
    return story

def _section_q3_poumon_urine():
    story = _section_q3_poumon()
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_q4_urine())
    return story

SECTIONS = [
    ("Épidémiologie, définitions & organisation architecturale (Q1-Q2)", _section_intro_q1_q2),
    ("Antibiothérapie, PAVM & infection urinaire (Q3-Q4)", _section_q3_poumon_urine),
    ("Cathéters, site opératoire, C. difficile, stratégie globale & sources (Q4-Q5)",
     _section_catheters_iso_cdiff_q5_sources),
]

def _make_doc(path=None):
    return SimpleDocTemplate(path or OUT, pagesize=A4,
                              leftMargin=MARGIN, rightMargin=MARGIN,
                              topMargin=32 * mm, bottomMargin=16 * mm,
                              title="Fiche SFAR-SRLF 2009 - Prevention des "
                                    "infections nosocomiales en reanimation",
                              author="Synthèse indépendante (source SFAR/SRLF)")

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
