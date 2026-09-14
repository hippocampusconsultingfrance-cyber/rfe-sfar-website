# -*- coding: utf-8 -*-
"""
Fiche de synthese - Societe Francophone de Medecine d'Urgence (SFMU) / Samu
de France / SRLF / SFAR, "Recommandations concernant la mise en place, la
gestion, l'utilisation et l'evaluation d'une salle d'accueil des urgences
vitales (SAUV)". Recu et accepte le 5 novembre 2003, publie 2004 (Annales
Francaises d'Anesthesie et de Reanimation 23 (2004) 850-855). 6 pages,
telecharge depuis sfar.org (wp-content/uploads/2016/01/Recommandations-
concernant-la-mise-en-place-la-gestion-l-utilisation-et-l-evaluation-d-une-
salle-d-accueil-des-urgences-vitales.pdf).

METHODOLOGIE : 11e convention methodologique distincte de ce corpus - AUCUN
systeme de cotation, AUCUNE mention GRADE/niveau/score nulle part dans le
texte source. Ce document est un texte organisationnel/reglementaire de
recommandations pour l'implantation et le fonctionnement d'une SAUV (salle
de dechoquage), presente sous forme de listes normatives et de criteres
minimaux d'equipement/architecture/personnel, jamais de propositions
individuellement cotees. Restitue en panneaux d'information et listes a
puces/tableaux thematiques, jamais en reco_table avec chip - meme
convention que fiche_ponction_lombaire.py (8e convention) pour ce type de
document HAS/reglementaire sans grille de preuve.

COUVERTURE : integrale du texte - preambule, definition (SAUV = salle de
dechoquage), criteres d'admission, architecture (localisation, acces,
structure), equipement (Niveau 1 pour services non-SAU, Niveau 2 pour SAU -
reanimation respiratoire, cardiovasculaire, medicaments, immobilisation,
divers), duree de prise en charge, collaboration (Samu-Smur, anesthesie-
reanimation, consultants, services medicotechniques, services d'aval,
contractualisation), ressources humaines (formation, effectifs minimaux),
procedures et protocoles, evaluation (registre d'activite), et le groupe de
travail complet. Ces recommandations excluent explicitement les urgences
pediatriques (POSU pediatriques) - disclosure reprise telle quelle depuis
la source, non une omission de cette fiche.

SCOPE PARTIEL DISCLOSE : la liste des 10 references reglementaires [1]-[10]
(decrets/circulaires 1991-2001) et les affiliations institutionnelles
completes de chaque membre du groupe de travail (hopital/service/ville) ne
sont PAS detaillees individuellement dans cette fiche - seules la societe
savante de chaque membre et la reference generale sont reprises. Disclosure
explicite dans le panneau "Sources et tracabilite" ; se referer au texte
integral pour le detail complet.

CORRECTIONS POST-AUDIT : un audit independant (subagent aveugle au
brouillon) a trouve une erreur d'attribution factuelle en 7.1 - le
brouillon fusionnait "les patients amenes par le Smur sont annonces par le
Samu" et "le Smur indique toute modification clinique" en une seule phrase
dont le "qui" se rattachait grammaticalement au Samu au lieu du Smur (la
source distingue clairement les deux acteurs) - corrige. L'audit a aussi
signale une distorsion en 5.1 (Reanimation respiratoire) : "capnographe CO2
(quantitatif souhaitable)" laissait entendre que le caractere quantitatif
etait optionnel, alors que la source ne rend "souhaitable" que l'affichage
des courbes (le monitorage quantitatif etant la base requise) - reformule.
Omissions mineures comblees : "si possible assujetties a la spirometrie"
(ventilateur), "controle des" (aimant), "plusieurs" (immobilisation),
"quantitative ou qualitative" (activite justifiant un equipement SAU), et
la phrase sur la coordination des acteurs comme "facteur essentiel de
qualite" (7.1).
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from style import *
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.units import mm

OUT = "/home/user/rfe-sfar-website/output/Fiche_SFMU_Samu_SRLF_SFAR_SAUV_2004.pdf"

SOURCE_TXT = ("Source : « Recommandations concernant la mise en place, la gestion, "
              "l'utilisation et l'évaluation d'une salle d'accueil des urgences vitales "
              "(SAUV) » — SFMU / Samu de France / SRLF / SFAR, Ann Fr Anesth Réanim 23 "
              "(2004) 850-855. Fiche de synthèse non officielle : se référer au texte "
              "intégral.")

def P(txt, style=S_CELL):
    return Paragraph(txt, style)

CW_FULL = PAGE_W - 2 * MARGIN

def theme_table(rows, col_widths, head=("Thème", "Détail")):
    data = [[P(head[0], S_HEAD_W), P(head[1], S_HEAD_W)]]
    for theme, detail in rows:
        data.append([P(theme, S_CELL_B), P(detail, S_CELL)])
    t = Table(data, colWidths=col_widths, repeatRows=1)
    style_cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), NAVY), ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTNAME", (0, 0), (-1, 0), FONT_BOLD), ("FONTSIZE", (0, 0), (-1, 0), 8),
        ("VALIGN", (0, 0), (-1, -1), "TOP"), ("ALIGN", (0, 1), (0, -1), "LEFT"),
        ("GRID", (0, 0), (-1, -1), 0.5, GREY_LIGHT),
        ("TOPPADDING", (0, 0), (-1, -1), 3.4), ("BOTTOMPADDING", (0, 0), (-1, -1), 3.4),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            style_cmds.append(("BACKGROUND", (0, i), (-1, i), BG_PANEL))
    t.setStyle(TableStyle(style_cmds))
    return t

TCW = [42 * mm, CW_FULL - 42 * mm]

def bullets(items, style=S_BODY_SM):
    html = "&bull; " + "<br/>&bull; ".join(items)
    return P(html, style)

TOTAL_PAGES = {"n": 5}

def on_page(canvas, doc, page_title):
    header_band(canvas, doc, "SFMU / SAMU DE FRANCE / SRLF / SFAR — RECOMMANDATIONS 2004",
                "Salle d'accueil des urgences vitales (SAUV)",
                page_title, icon_fn=lambda c, x, y: icon_shield(c, x, y, 13 * mm), color=RED)
    footer_band(canvas, doc, SOURCE_TXT, f"Page {doc.page} / {TOTAL_PAGES['n']}")

# ---------------------------------------------------------------------------
def _section_intro():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Champ :</b> recommandations pour la mise en place, la gestion, l'utilisation "
        "et l'évaluation d'une salle d'accueil des urgences vitales (SAUV, « salle de "
        "déchoquage ») au sein d'un service d'urgence. Élaborées à l'initiative de la "
        "SFMU, avec la Société francophone de médecine d'urgence, Samu de France, la "
        "SRLF et la SFAR. Reçu et accepté le 5 novembre 2003.", S_BODY),
        bg=BG_PANEL, border=TEAL))
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Méthodologie :</b> ce texte est un référentiel organisationnel — critères "
        "minimaux d'architecture, d'équipement, de personnel et de procédures. Il ne "
        "comporte <b>aucun système de cotation</b> (pas de GRADE, pas de niveau de "
        "preuve individuel) : chaque recommandation est une norme collective, jamais "
        "gradée individuellement — restituée ici en listes et tableaux thématiques, "
        "jamais en chip de grade inventé.", S_BODY_SM), bg=AMBER_LIGHT, border=AMBER))
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("1-2 — Préambule & définition"))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "Bien que les urgences vitales ne constituent qu'une minorité des cas dans un "
        "service d'urgence, elles nécessitent une stratégie préétablie d'organisation "
        "des moyens humains et matériels. En l'absence d'élément réglementaire ou "
        "législatif précis concernant la SAUV, ces recommandations s'adressent à "
        "l'ensemble des acteurs médicaux et paramédicaux des urgences, et aux "
        "responsables administratifs des établissements de santé.", S_BODY_SM))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>La SAUV</b>, ou salle de déchoquage, est un lieu d'accueil, au sein du "
        "service d'urgence, des patients ayant une détresse vitale existante ou "
        "potentielle — dans le cadre d'un service d'accueil des urgences (SAU) ou d'une "
        "unité de proximité d'accueil, de traitement et d'orientation des urgences "
        "(UPATOU). Les pôles spécialisés d'urgence (POSU) non pédiatriques déterminent, "
        "selon le type de patients pris en charge, si une SAUV doit être mise en place ; "
        "si tel est le cas, ces recommandations s'y appliquent. <b>Exclusion explicite "
        "de la source :</b> ces recommandations excluent la prise en charge des urgences "
        "pédiatriques, notamment les POSU pédiatriques (objet d'un texte "
        "complémentaire).", S_BODY_SM))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P("Principes directeurs d'une SAUV :", S_BODY_SM))
    story.append(Spacer(1, 1 * mm))
    story.append(bullets([
        "ouverte 24 heures/24 ;",
        "ne correspond ni à un lit de réanimation ni à un lieu d'hospitalisation ;",
        "doit être libérée dès que possible ;",
        "polyvalente, médicochirurgicale.",
    ]))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "Une structure accueillant déjà régulièrement des patients en détresse vitale "
        "(SSPI, unité de réanimation d'urgence) peut être utilisée comme SAUV — sans "
        "s'y substituer ni être substituée par elle — à condition d'être à proximité "
        "immédiate des urgences et de suivre l'ensemble de ces recommandations. Toute "
        "restructuration architecturale à venir devra intégrer la SAUV au sein du "
        "service d'urgence.", S_BODY_SM))
    return story

def _section_admission():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("3 — Critères d'admission"),
        Spacer(1, 1.5 * mm),
        P("L'admission dans une SAUV concerne tous les patients en situation de détresse "
          "vitale existante ou potentielle. La décision d'admission est prise par le "
          "médecin du service des urgences, et le cas échéant par l'infirmière d'accueil "
          "et d'orientation (IAO), le médecin du SMUR, ou le médecin régulateur du Samu — "
          "en s'appuyant sur des procédures cliniques, si possible à partir de scores de "
          "gravité validés et partagés. La prise en charge des urgences internes de "
          "l'établissement dans la SAUV doit rester exceptionnelle ; en l'absence "
          "d'alternative, la décision repose sur le médecin responsable de la SAUV ou son "
          "représentant désigné.", S_BODY),
    ]))
    return story

def _section_intro_admission():
    story = _section_intro()
    story.append(Spacer(1, 2 * mm))
    story.extend(_section_admission())
    return story

# ---------------------------------------------------------------------------
def _section_architecture():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("4 — Architecture"),
        Spacer(1, 1.5 * mm),
        P("<b>4.1 — Localisation :</b> de préférence dans l'enceinte du service des "
          "urgences, sinon à proximité immédiate — emplacement réduisant les durées de "
          "transport vers le plateau technique (imagerie, réanimation, bloc opératoire).",
          S_BODY_SM),
        Spacer(1, 1.2 * mm),
        P("<b>4.2 — Accès :</b> signalétique spécifique dès l'arrivée aux urgences ; "
          "couloirs de plain-pied entre sas d'arrivée, urgences et SAUV ; couloirs vers "
          "le plateau technique larges, permettant le croisement de brancards, sans "
          "mobilier entravant la circulation.", S_BODY_SM),
    ]))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P("<b>4.3 — Structure :</b> un ou plusieurs emplacements (poste de "
                    "soins pour un patient), nombre adapté à l'activité (passages, "
                    "gravité, durée de séjour), avec au minimum :", S_BODY_SM))
    story.append(Spacer(1, 1 * mm))
    story.append(bullets([
        "au moins 1 emplacement pour les services d'urgence non SAU ; au moins 2 pour "
        "les services > 15 000 passages/an et pour les SAU ;",
        "par emplacement : ≥ 2 prises oxygène, ≥ 1 prise air, ≥ 3 prises vide, ≥ 6 "
        "prises électricité (dont 2 sécurisées souhaitables), 1 système d'accrochage "
        "perfusions, 1 support pour appareils de surveillance/pousse-seringues ;",
        "surface SAUV ≥ 25 m² (≥ 15 m²/emplacement hors rangements si plusieurs "
        "emplacements) ; rangements réservés exclusivement au matériel de la SAUV ;",
        "par pièce : ≥ 1 poste de lavage des mains, ≥ 1 dispositif d'affichage des "
        "radiographies, ≥ 1 plan de travail ;",
        "communication : ≥ 1 téléphone par pièce avec accès extérieur, ≥ 1 téléphone "
        "dédié à une liaison Samu, un dispositif d'appel de renfort sans quitter la "
        "pièce ; ordinateur avec accès réseau hospitalier et transfert d'images "
        "souhaitables ;",
        "alimentation électrique permettant le branchement d'appareils lourds "
        "(amplificateur de brillance, radiographie mobile, échographe) dans chaque "
        "pièce ; éclairage permettant les gestes techniques + éclairage mobile "
        "complémentaire ; possibilité d'obscurcissement pour les échographies.",
    ]))
    return story

EQUIP_N1_ROWS = [
    ("Réanimation respiratoire",
     "Fluides médicaux + bouteille O2 de secours (PP) ; ventilateur type transport "
     "(ventilation contrôlée/assistée, PEP, monitorage volumes/pressions, alarmes "
     "sonores conformes assujetties aux variations de pression, si possible assujetties "
     "à la spirométrie) (PP) ; VNI souhaitable (PS) ; matériel d'intubation trachéale, "
     "insufflateur manuel + réservoir O2, masques adaptés ; matériel d'intubation "
     "difficile (PP) ; aspirateur électrique + sondes protégées (PP) ; aspiration "
     "manuelle de secours (PP) ; monitorage SpO2 (affichage des courbes souhaité) + "
     "capnographe CO2 expiratoire quantitatif (courbes souhaitables) (PP) ; débitmètre "
     "de pointe (PP) ; drainage thoracique (PP)."),
    ("Réanimation cardiovasculaire",
     "Électrocardioscope ; tensiomètre automatique + manuel (brassards adaptés) (PP) ; "
     "défibrillateur (PS) ; stimulation transthoracique (PS) ; ECG multipiste (PS) ; "
     "≥ 2 pousse-seringues électriques ; matériel d'accès veineux périphérique/central "
     "préconditionné ; accélérateur-réchauffeur de perfusion (PP), autotransfusion (PS), "
     "garrot pneumatique (PS) ; kit transfusionnel (PP) ; mesure de l'hémoglobine (PP) ; "
     "aimant pour contrôle des dispositifs implantés (PS)."),
    ("Médicaments",
     "Ensemble des médicaments pour défaillances respiratoires/circulatoires/"
     "neurologiques ; solutés de perfusion et de remplissage ; liste pré-établie connue "
     "de tous — analgésiques, sédatifs, antibiotiques, catécholamines, thrombolytiques, "
     "principaux antidotes."),
    ("Immobilisation",
     "Matelas à dépression et/ou dispositif de transfert (PP) ; plusieurs dispositifs "
     "adaptés d'immobilisation du rachis et des membres."),
    ("Divers",
     "Brancard radiotransparent (réanimation, transport, contention) ; glycémie "
     "capillaire (PP) ; thermomètres dont un adapté à l'hypothermie (PS) ; réchauffement "
     "corporel (PP) ; sondes gastriques + poches de récupération (PP) ; drainage "
     "urinaire, y compris sus-pubien (PP) ; imagerie mobile + échographe (PS). Moyens "
     "propres pour mobiliser un patient ventilé avec tout son monitorage et ses "
     "dispositifs de traitement."),
]

def _section_equipement():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("5 — Équipement — Niveau 1 (services d'urgence non SAU)"),
        Spacer(1, 1.5 * mm),
        P("Deux niveaux d'équipement minimum : Niveau 1 pour les services d'urgence non "
          "SAU, Niveau 2 pour les SAU (certaines structures non SAU doivent toutefois "
          "s'équiper selon les critères SAU, du fait d'une activité particulière — "
          "quantitative ou qualitative — et/ou d'un isolement géographique). "
          "Recommandations par emplacement, sauf mention "
          "« PP » (par pièce) ou « PS » (par SAUV).", S_BODY_SM),
    ]))
    story.append(Spacer(1, 1.5 * mm))
    story.append(theme_table(EQUIP_N1_ROWS, TCW, head=("Domaine", "Équipement minimal")))
    return story

def _section_architecture_equipement():
    story = _section_architecture()
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_equipement())
    return story

# ---------------------------------------------------------------------------
def _section_equipement_n2():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("5.2 — Équipement — Niveau 2 (SAU)"),
        Spacer(1, 1.5 * mm),
        P("Tous les moyens du Niveau 1 doivent être présents. Moyens supplémentaires : "
          "au moins un ventilateur dit « de réanimation », permettant plusieurs modes "
          "ventilatoires, en volume ou en pression (PS). Il est en outre souhaitable que "
          "la SAUV puisse disposer de la mesure de la pression artérielle invasive (PP) "
          "et de la fibroscopie bronchique (PS).", S_BODY_SM),
    ]))
    story.append(Spacer(1, 2 * mm))
    story.append(KeepTogether([
        section_bar("6 — Durée de prise en charge"),
        Spacer(1, 1.5 * mm),
        P("La durée doit être la plus courte possible : le médecin de la SAUV doit avoir "
          "pour objectif la prise en charge immédiate, continue et coordonnée du patient, "
          "pour la remise en disponibilité rapide de la SAUV.", S_BODY_SM),
    ]))
    story.append(Spacer(1, 2 * mm))
    story.append(KeepTogether([
        section_bar("7 — Collaboration"),
        Spacer(1, 1.5 * mm),
        P("<b>7.1 — Relation avec le Samu-Smur :</b> l'admission directe dans un service "
          "spécialisé est chaque fois privilégiée, mais les relations Samu/SAUV sont "
          "essentielles pour l'admission et l'orientation — ces relations concernent au "
          "quotidien la prise en charge des patients, la coordination des acteurs étant "
          "un facteur essentiel de qualité. Le Samu prévient la SAUV des difficultés "
          "d'aval (absence de lits de réanimation). Les patients amenés par le Smur sont "
          "systématiquement annoncés par le Samu ; le Smur indique toute modification de "
          "l'état clinique du patient, et le médecin du Smur peut à tout moment joindre "
          "le médecin de la SAUV via la régulation. Transmission de médecin à médecin et "
          "d'infirmier à infirmier, dossier complet et vérifié ; l'équipe du Smur ne "
          "quitte le patient qu'une fois la transmission effectuée et la sécurité "
          "assurée. Les transferts interhospitaliers médicalisés depuis la SAUV se "
          "décident entre le médecin de la SAUV et le médecin régulateur, même si "
          "l'établissement dispose d'un Smur propre.", S_BODY_SM),
    ]))
    return story

def _section_equipement_n2_duree_collab():
    return _section_equipement_n2()

# ---------------------------------------------------------------------------
def _section_collab_suite():
    story = []
    story.append(Spacer(1, 2 * mm))
    story.append(P("<b>7.2 — Relations et collaboration avec les autres services</b>",
                    S_CELL_B))
    story.append(Spacer(1, 1 * mm))
    story.append(theme_table([
        ("7.2.1 — Anesthésie-réanimation et réanimations",
         "Procédures établies avec le service d'anesthésie-réanimation et/ou les "
         "services de réanimation ; l'anesthésiste-réanimateur et/ou le réanimateur doit "
         "venir renforcer la SAUV à la demande de l'équipe. Si la SAUV est intégrée "
         "provisoirement dans une structure accueillant régulièrement des détresses "
         "vitales (SSPI, unité de réanimation d'urgence), un contrat entre les deux "
         "services doit en définir clairement le fonctionnement."),
        ("7.2.2 — Les consultants",
         "La SAUV doit disposer des listes actualisées de gardes et astreintes de tous "
         "les spécialistes de l'établissement, et pouvoir les contacter directement sans "
         "passer par leur service d'origine. Ces médecins interviennent selon des "
         "modalités et délais définis à l'avance, par discipline, dans un règlement "
         "intérieur validé par les instances médico-administratives. Liste actualisée "
         "également des spécialistes non couverts par la permanence médicale de "
         "l'établissement."),
        ("7.2.3 — Services médicotechniques",
         "Accès privilégié à l'imagerie (priorités définies si le plateau technique "
         "n'est pas dédié aux urgences) et au(x) laboratoire(s), pour accélérer "
         "l'obtention des résultats ; biologie délocalisée en l'absence d'alternative."),
        ("7.2.4 — Services d'aval",
         "Les patients de la SAUV sont acceptés en priorité et sans délai dès que leur "
         "départ peut être envisagé, pour maintenir la capacité d'accueil des urgences "
         "vitales. Les protocoles de transfert interne détaillent le personnel et le "
         "matériel engagés, sans compromettre la sécurité de la SAUV."),
        ("7.2.5 — Contractualisation",
         "L'ensemble des collaborations nécessaires au fonctionnement en sécurité de la "
         "SAUV doit faire l'objet d'un protocole d'accord validé par les instances "
         "médico-administratives de l'établissement."),
    ], TCW, head=("Sous-section", "Détail")))
    return story

def _section_ressources_humaines():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("8 — Ressources humaines"),
        Spacer(1, 1.5 * mm),
        P("Le chef de service des urgences est responsable de l'organisation de la SAUV "
          "ou délègue cette responsabilité à un médecin de l'établissement ; un médecin "
          "nominativement identifié est en permanence mobilisable pour l'accueil et la "
          "prise en charge des patients.", S_BODY),
    ]))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>8.1 — Formation de l'équipe :</b> le personnel médical et paramédical "
        "(infirmier(e), aide-soignant(e) ou agent hospitalier) affecté à la SAUV doit "
        "avoir bénéficié d'une formation lui permettant de prendre en charge l'ensemble "
        "des situations menaçant le pronostic vital (procédures techniques et "
        "thérapeutiques), ainsi que d'une formation d'adaptation à l'emploi. Sur le plan "
        "du savoir-être, il doit savoir rester calme et communiquer avec l'équipe, les "
        "référents extérieurs et l'entourage du patient.", S_BODY_SM))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>8.2 — Équipe soignante :</b> effectif dépendant du flux de patients, mais au "
        "minimum un médecin, un(e) infirmier(e) et un(e) aide-soignant(e) ou agent "
        "hospitalier par SAUV, quels que soient l'heure et le jour. Ce personnel peut "
        "exercer d'autres fonctions mais doit pouvoir se libérer immédiatement — il est "
        "ainsi impossible, sauf circonstances exceptionnelles, que le médecin de la SAUV "
        "assure seul et simultanément la régulation Samu et/ou les interventions Smur. "
        "Le cadre infirmier supérieur des urgences est responsable de l'organisation "
        "paramédicale (ou délègue à un cadre/infirmier(e) nominativement identifié) ; un "
        "infirmier(e) et un aide-soignant/agent hospitalier au moins sont en permanence "
        "mobilisables.", S_BODY_SM))
    return story

def _section_procedures_evaluation():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("9 — Procédures et protocoles"),
        Spacer(1, 1.5 * mm),
        P("L'application de procédures clairement identifiées par chaque membre d'une "
          "équipe, sous la responsabilité d'un coordinateur, améliore la performance "
          "collective — la coordination n'est pas spontanée et demande une "
          "préparation : identification du rôle de chacun, standardisation des "
          "procédures, capacité de communication, et identification d'un chef d'équipe "
          "lorsqu'un événement survient.", S_BODY),
    ]))
    story.append(Spacer(1, 1.2 * mm))
    story.append(P("Procédures devant être mises en place dans la SAUV :", S_BODY_SM))
    story.append(Spacer(1, 1 * mm))
    story.append(bullets([
        "procédure d'alerte ; procédures d'appel des membres de l'équipe ; procédures "
        "de recours à un avis spécialisé ;",
        "préparation de la SAUV ; organisation du travail ; accueil du patient et sa "
        "prise en charge initiale ;",
        "protocoles de prise en charge des pathologies les plus fréquentes, fondés sur "
        "les données de la médecine fondée sur les preuves ;",
        "critères et modalités de transfert inter- ou intrahospitalier ; contenu des "
        "informations à transmettre avec le patient ;",
        "formation d'adaptation à l'emploi à la SAUV (médecins, infirmier(e)s, "
        "aides-soignant(e)s ou agents hospitaliers).",
    ]))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "La liste nominative et actualisée de l'équipe affectée à la SAUV, comportant "
        "obligatoirement le moyen d'appel d'urgence du personnel, doit être affichée "
        "dans la SAUV. L'ensemble du matériel doit être prêt à une utilisation "
        "immédiate : vérifié après chaque utilisation et au moins une fois par jour "
        "(check-lists régulièrement mises à jour, vérification quotidienne par "
        "attribution nominative sous la responsabilité du cadre infirmier, apparaissant "
        "dans un registre ad hoc).", S_BODY_SM))
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("10 — Évaluation"),
        Spacer(1, 1.5 * mm),
        P("Un registre de l'activité de la SAUV doit être mis en place, comportant au "
          "minimum : état civil et origine du patient ; mode d'admission ; horaires et "
          "durée de prise en charge ; motif d'admission ; actes diagnostiques et "
          "thérapeutiques réalisés ; devenir et orientation du patient. Il est "
          "souhaitable de prévoir une analyse qualitative régulière des dossiers "
          "(démarche qualité) et une analyse collective par l'équipe des situations "
          "ayant conduit à un dysfonctionnement ou un décès.", S_BODY_SM),
    ]))
    return story

def _section_ressources_procedures():
    story = _section_ressources_humaines()
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_procedures_evaluation())
    return story

def _section_sources():
    story = []
    story.append(section_bar("Sources et traçabilité", color=GREY))
    story.append(Spacer(1, 2 * mm))
    story.append(P(
        "<b>Document source :</b> « Recommandations concernant la mise en place, la "
        "gestion, l'utilisation et l'évaluation d'une salle d'accueil des urgences "
        "vitales (SAUV) ». Société francophone de médecine d'urgence (SFMU, à "
        "l'initiative), Samu de France, Société de réanimation de langue française "
        "(SRLF), Société française d'anesthésie et de réanimation (SFAR).", S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>Groupe de travail :</b> Dr P. Mardegan (SFMU, coordinateur), Dr L. Maillard "
        "(SRLF, secrétaire), C. Babatasi (SFMU), Pr P. Carli (Samu de France), "
        "Dr J.-L. Ducassé (SFMU), Pr J.-E. de La Coussaye (SFAR), Dr P. Goldstein (Samu "
        "de France), Dr P. Le Conte (SRLF), Pr B. Riou (SFAR), Dr B. Vermeulen (SFMU).",
        S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P("<b>Version :</b> reçu et accepté le 5 novembre 2003 ; publié dans "
                    "Ann Fr Anesth Réanim 23 (2004) 850-855 et le Journal Européen des "
                    "Urgences 2003;16:15165-15170.", S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P("<b>Méthodologie :</b> texte organisationnel/réglementaire, sans "
                    "système de cotation ni niveau de preuve individuel — voir "
                    "disclosure méthodologique en page 1.", S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>URL source :</b> https://sfar.org/wp-content/uploads/2016/01/"
        "Recommandations-concernant-la-mise-en-place-la-gestion-l-utilisation-et-"
        "l-evaluation-d-une-salle-d-accueil-des-urgences-vitales.pdf", S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P("<b>Couverture :</b> cette fiche reprend l'intégralité du texte "
                    "(préambule, définition, critères d'admission, architecture, "
                    "équipement Niveaux 1 et 2, durée de prise en charge, collaboration, "
                    "ressources humaines, procédures/protocoles, évaluation). Les 10 "
                    "références réglementaires citées (décrets/circulaires 1991-2001) ne "
                    "sont pas détaillées individuellement — se référer au texte intégral "
                    "pour leurs références complètes.", S_SOURCE))
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Avertissement — document de 2004 (recommandations de 2003) :</b> ce document "
        "est une fiche de synthèse indépendante, produite pour un usage d'aide-mémoire. "
        "Elle reprend l'intégralité des recommandations du texte source, mais ne "
        "remplace pas le texte intégral (dont les références réglementaires complètes) "
        "et n'est ni éditée ni validée par la SFMU, Samu de France, la SRLF ou la SFAR. "
        "Le cadre réglementaire français de l'accueil des urgences ayant évolué depuis "
        "2003-2004, se référer aux textes réglementaires en vigueur et aux "
        "recommandations plus récentes le cas échéant.",
        S_BODY_SM), bg=GREY_LIGHT, border=GREY))
    return story

def _section_ressources_procedures_sources():
    story = _section_ressources_procedures()
    story.append(Spacer(1, 4 * mm))
    story.extend(_section_sources())
    return story

def _section_equip_n2_collab_full():
    # Merged onto one page-group (no forced page break): "Equipement Niveau
    # 2, duree & collaboration 7.1" alone left a page ~25% white, and
    # "Collaboration (suite) 7.2" alone left the next page ~50% white -
    # combined per the <60%-full merge rule (CLAUDE.md build pipeline,
    # step 7).
    story = _section_equipement_n2_duree_collab()
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_collab_suite())
    return story

SECTIONS = [
    ("Méthodologie, préambule, définition & admission", _section_intro_admission),
    ("Architecture & équipement Niveau 1", _section_architecture_equipement),
    ("Équipement Niveau 2, durée & collaboration", _section_equip_n2_collab_full),
    ("Ressources humaines, procédures, évaluation & sources",
     _section_ressources_procedures_sources),
]
# NOTE on page-fill: the closing Avertissement panel spills onto its own
# ~15%-full final page (section 4 is otherwise ~95% full). Accepted as-is,
# consistent with the same trailing-whitespace call already made on
# fiche_catheters_veineux_centraux.py (see its own NOTE) - per CLAUDE.md
# build pipeline step 7, a merge is worth trying only when it plausibly
# helps; here the preceding page has no slack left to absorb it.

def _make_doc(path=None):
    return SimpleDocTemplate(path or OUT, pagesize=A4,
                              leftMargin=MARGIN, rightMargin=MARGIN,
                              topMargin=32 * mm, bottomMargin=16 * mm,
                              title="Fiche SFMU/Samu de France/SRLF/SFAR 2004 - SAUV",
                              author="Synthèse indépendante (source SFMU/Samu de "
                                     "France/SRLF/SFAR)")

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
