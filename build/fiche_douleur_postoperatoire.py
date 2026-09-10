# -*- coding: utf-8 -*-
"""
Fiche de synthese - Recommandations formalisees d'experts (RFE) 2008, Sfar (comite
douleur-anesthesie locoregionale et comite des referentiels) : "Prise en charge de la
douleur postoperatoire chez l'adulte et l'enfant" (actualisation de la conference de
consensus de 1997). Ann Fr Anesth Reanim 2008;27:1035-1041.

METHODOLOGIE - PARTICULARITE MAJEURE : cette source n'imprime JAMAIS de tag individuel
(ni "(grade X)", ni "(Accord fort/faible)", ni "GRADE 1+/2+") a cote de chaque
recommandation. La methode GRADE y est utilisee mais la force est encodee UNIQUEMENT
dans le verbe de la phrase elle-meme, selon une convention que la source definit
explicitement en section 3 : « on ne prevoit de formuler que des "recommandations
fortes" ("il faut faire ou ne pas faire ou nous recommandons fortement de...") et des
recommandations "optionnelles" ("il est possible ou probable de faire ou de ne pas
faire ou nous proposons d'eventuellement faire...") ». Chip "Fort" attribue ici a
chaque phrase utilisant "il est recommande"/"il faut"/"nous recommandons fortement"
(y compris ses formes negatives "il n'est pas recommande"/"il ne faut pas") ; chip
"Faible" attribue aux phrases utilisant "il est probablement recommande"/"il est
possible/probable de"/"il faut probablement" (et negatives "il n'est probablement pas
recommande"/"ne peut etre recommande"). C'est une resolution TEXTUELLE, phrase par
phrase, a partir de la regle que la source elle-meme enonce - pas une invention de
tag absent (meme principe que la resolution de signe +/- de fiche_avc_precoce.py et
fiche_examens_preinterventionnels.py, disclosee explicitement plutot que silencieuse).
Extension locale non invasive du dictionnaire GRADE_COLORS partage (meme precedent que
fiche_nutrition.py, seule autre fiche du corpus a utiliser exactement ces 2 libelles) :
"Fort" -> vert, "Faible" -> teal.

DECOMPTE - la source annonce elle-meme, en introduction : « quatre tours de cotations
ont ete necessaires pour elaborer 124 recommandations consensuelles », reparties par
theme : PEC/qualite (14), morphiniques (26), antalgiques non morphiniques (16),
antihyperalgesiques (9), prevention de la chronicisation (6), infiltration (16), ALR
(30), analgesie ambulatoire (7) = 124. Le texte source ne numerote cependant AUCUNE
recommandation individuellement (pas de "R1"/"Encadre X.Y") - contrairement a
fiche_nutrition.py qui pouvait recouper son propre compte contre des "Encadre X.Y"
numerotes, il n'existe ici aucun marqueur verifiable permettant de recouper mon propre
decoupage en lignes de tableau contre le chiffre agrege "124" par theme. Cette fiche
retranscrit l'integralite du contenu prescriptif de chaque theme, condense en lignes
thematiques (plusieurs clauses consecutives de meme force et de meme sujet regroupees
sous une seule ligne, jamais deux clauses de force differente fusionnees sous un
chip unique - meme garde-fou que la regle 4 CLAUDE.md sur les chips composites) ; le
nombre de lignes obtenu par theme ne correspond donc pas necessairement au chiffre
official annonce par theme - disclosure explicite plutot que forcer une correspondance
artificielle.

PERIMETRE - integralite des sections 4 a 11 (les 8 themes prescriptifs). Sections 1-3
(introduction, justification RFE, justification GRADE) sont resumees dans le panneau
de methodologie plutot que retranscrites in extenso (contenu procedural sur
l'elaboration du referentiel, pas des recommandations cliniques).
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from style import *
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.units import mm

GRADE_COLORS["Fort"] = (GREEN, WHITE)
GRADE_COLORS["Faible"] = (TEAL, WHITE)
GRADE_COLORS["—"] = (GREY_LIGHT, INK)

OUT = "/home/user/rfe-sfar-website/output/Fiche_SFAR_Douleur_Postoperatoire_2008.pdf"

SOURCE_TXT = ("Source : Sfar (comité douleur-ALR et comité des référentiels) — « Prise en charge "
              "de la douleur postopératoire chez l'adulte et l'enfant » — RFE 2008, Ann Fr Anesth "
              "Reanim 2008;27:1035-1041. Fiche de synthèse non officielle : se référer au texte "
              "intégral.")

def P(txt, style=S_CELL):
    return Paragraph(txt, style)

def chip(label, **kw):
    return grade_chip(label, **kw)

FORCE_W = 20 * mm

def reco_table(rows, col_widths=None):
    """rows: (theme, text, force) - force parmi 'Fort', 'Faible'. Pas de numerotation
    individuelle dans la source (voir docstring) : 'theme' remplace la colonne Réf."""
    text_w = PAGE_W - 2 * MARGIN - FORCE_W
    cw = col_widths or [text_w, FORCE_W]
    data = [[P("Recommandation (texte condensé, fidèle à la source)", S_HEAD_W), P("Force", S_HEAD_W_C)]]
    for txt, force in rows:
        data.append([P(txt, S_CELL), chip(force, width=FORCE_W - 2 * mm)])
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

TOTAL_PAGES = {"n": 9}

def on_page(canvas, doc, page_title):
    header_band(canvas, doc, "SFAR — RFE 2008 — FICHE DE SYNTHÈSE",
                "Douleur postopératoire — adulte & enfant",
                page_title, icon_fn=lambda c, x, y: icon_pill(c, x, y, 13 * mm), color=TEAL_DARK)
    footer_band(canvas, doc, SOURCE_TXT, f"Page {doc.page} / {TOTAL_PAGES['n']}")

# ---------------------------------------------------------------------------
def _section_intro_pec():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Champ :</b> prise en charge de la douleur postopératoire (DPO) chez l'adulte et "
        "l'enfant — actualisation de la conférence de consensus de 1997. RFE Sfar 2008, comité "
        "douleur-ALR et comité des référentiels, 22 experts. <b>8 thèmes traités, 124 "
        "recommandations consensuelles</b> (4 tours de cotation) : évaluation/amélioration de la "
        "PEC (14), utilisation des morphiniques (26), antalgiques non morphiniques (16), agents "
        "antihyperalgésiques (9), prévention de la chronicisation (6), infiltration du site "
        "opératoire (16), place de l'ALR (30), analgésie en chirurgie ambulatoire (7).",
        S_BODY), bg=BG_PANEL, border=TEAL_DARK))
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Méthodologie — particularité :</b> cette source n'imprime <b>aucun tag individuel</b> "
        "(pas de « grade X », pas de « Accord fort/faible ») à côté de chaque recommandation. La "
        "méthode GRADE y est utilisée mais la force est encodée <b>dans le verbe de chaque "
        "phrase</b>, selon la convention que la source définit elle-même : « recommandation "
        "forte » = « il est recommandé »/« il faut »/« nous recommandons fortement » (et ses "
        "formes négatives « il n'est pas recommandé ») ; « recommandation optionnelle » = « il "
        "est probablement recommandé »/« il est possible/probable de » (et formes négatives). "
        "<b>Chip « Fort »/« Faible » attribué ici phrase par phrase selon cette règle explicite "
        "de la source</b> — résolution textuelle disclosée, jamais un tag inventé. La source ne "
        "numérote aucune recommandation individuellement : le découpage en lignes ci-dessous est "
        "thématique (regroupement de clauses consécutives de même sujet et même force ; jamais "
        "deux forces différentes fusionnées sous un chip unique), et son nombre de lignes par "
        "thème ne recoupe donc pas nécessairement le chiffre agrégé « 124 » annoncé par la "
        "source.", S_BODY_SM), bg=BG_PANEL, border=AMBER))
    story.append(Spacer(1, 3 * mm))

    story.append(section_bar("1 — Évaluer et améliorer la prise en charge de la DPO", color=TEAL_DARK))
    story.append(Spacer(1, 2 * mm))
    story.append(reco_table([
        ("Insister sur l'importance d'une implication institutionnelle avec des objectifs "
         "concernant la douleur dans le projet de l'établissement ; inscrire la qualité de la "
         "PEC de la DPO dans la réhabilitation postopératoire (récupération fonctionnelle "
         "rapide).", "Fort"),
        ("Démarche concertée multidisciplinaire avec définition de référents et "
         "responsabilisation des acteurs ; aborder conjointement organisation d'équipes, "
         "formation, désignation de personnel référent, information du patient, évaluation de la "
         "douleur et procédures de soins.", "Fort"),
        ("Développer des postes d'infirmier référent douleur.", "Fort"),
        ("Informer le patient oralement en pré- puis postopératoire, avec support écrit ; tracer "
         "cette information dans le dossier.", "Fort"),
        ("Évaluer l'intensité de la douleur par autoévaluation chiffrée (échelle numérique ou "
         "verbale) en préopératoire et en SSPI (critère de sortie de SSPI) ; poursuivre "
         "régulièrement en postopératoire (repos, mouvement, après traitement), associée à "
         "l'évaluation de la sédation et de la ventilation, et tracée dans le dossier. Évaluer "
         "aussi l'incidence de la douleur chronique postchirurgicale (DCPC).", "Fort"),
        ("Développer des protocoles de traitement utilisant les techniques efficaces (ACP "
         "morphinique, analgésie multimodale, ALR), intégrant surveillance, prévention et "
         "traitement des effets secondaires.", "Fort"),
        ("La prescription à la demande n'est pas recommandée ; prescrire des doses de secours "
         "sur des critères fiables (score d'intensité douloureuse).", "Fort"),
        ("Standardisation, prérédaction, voire informatisation des prescriptions dans le cadre "
         "de procédures thérapeutiques.", "Fort"),
        ("Mesurer la qualité de la PEC de la DPO en évaluant parallèlement structure, procédures "
         "et résultats pour le patient, de façon continue et prolongée.", "Fort"),
        ("Pour la structure : recenser le nombre d'infirmières référentes douleur, les moyens "
         "financiers/matériels/humains et les formations dispensées ; faire participer l'équipe "
         "à toutes les étapes de la démarche qualité.", "Fort"),
        ("Utiliser d'autres méthodes d'évaluation des pratiques professionnelles (chemin "
         "clinique, réunions de morbi-mortalité, suivi d'indicateurs — dont ceux de la HAS —, "
         "staffs EPP).", "Fort"),
        ("Réaliser des enquêtes « patients » pour évaluer les résultats ; associer l'intensité "
         "douloureuse et les effets indésirables (la satisfaction seule est un critère "
         "insuffisamment spécifique).", "Fort"),
    ]))
    story.append(Spacer(1, 4 * mm))

    story.append(section_bar("2 — Utiliser les morphiniques en périopératoire", color=TEAL_DARK))
    story.append(Spacer(1, 2 * mm))
    story.append(P("<b>Morphiniques oraux</b>", S_BODY_SM))
    story.append(Spacer(1, 1.5 * mm))
    story.append(reco_table([
        ("Réserver les voies sous-cutanée et IV aux patients pour lesquels la voie orale n'est "
         "pas disponible ; utiliser la morphine à libération immédiate par voie orale en "
         "postopératoire immédiat ou en relais de la voie parentérale (le traitement peut "
         "débuter avec la reprise de l'alimentation orale).", "Fort"),
        ("Il n'y a pas de place pour la titration morphinique par voie orale en postopératoire "
         "immédiat — la titration IV est préférable.", "Fort"),
        ("Ne pas utiliser le dextropropoxyphène dans l'analgésie postopératoire.", "Fort"),
        ("Utiliser le tramadol, seul ou associé aux antalgiques non morphiniques, en cas de "
         "chirurgie à douleur modérée (non contre-indiqué avec la morphine).", "Fort"),
    ]))
    story.append(Spacer(1, 2 * mm))
    story.append(P("<b>Titration intraveineuse & ACP morphine</b>", S_BODY_SM))
    story.append(Spacer(1, 1.5 * mm))
    story.append(reco_table([
        ("La morphine est l'opioïde recommandé pour une titration IV postopératoire immédiate, à "
         "partir d'une valeur seuil d'intensité douloureuse (échelle d'auto- ou "
         "d'hétéroévaluation, patients non somnolents).", "Fort"),
        ("Bolus de 2 ou 3 mg toutes les 5 minutes.", "Faible"),
        ("Interrompre la titration en cas de somnolence ; surveiller (neurologique, respiratoire, "
         "hémodynamique) pendant la titration et jusqu'à 1h après (pic d'action de la morphine, "
         "risque de dépression respiratoire).", "Fort"),
        ("Une titration IV postopératoire en morphine n'est pas recommandée dans les unités "
         "d'hospitalisation chirurgicale conventionnelle.", "Fort"),
        ("En cas de chirurgie à douleur modérée ou sévère prédictible nécessitant des "
         "morphiniques : utiliser l'ACP (morphine, opiacé de choix — aucun avantage à la "
         "remplacer par le tramadol), associée à une analgésie multimodale.", "Fort"),
        ("L'association perfusion continue + mode bolus n'améliore pas l'analgésie et majore le "
         "risque de dépression respiratoire (seule indication : substitution d'un traitement "
         "morphinique préopératoire).", "—"),
        ("En prévention des NVPO (effet indésirable le plus fréquent) : associer en première "
         "intention le dropéridol à la morphine dans la pompe d'ACP.", "Fort"),
        ("Le dispositif analgésique transdermique iontophorétique a une efficacité comparable à "
         "l'ACP morphine (chirurgie à douleur modérée/sévère prédictible) ; appliquer les mêmes "
         "modalités de surveillance.", "Fort"),
    ]))
    return story


def _section_morphiniques_suite_anm():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(P("<b>Spécificités : sujet âgé et enfant</b>", S_BODY_SM))
    story.append(Spacer(1, 1.5 * mm))
    story.append(reco_table([
        ("Chez le sujet âgé : titration selon les mêmes modalités que chez le sujet plus jeune, "
         "mais dose titrée réduite au-delà de 85 ans, en cas d'altération rénale/hépatique ou de "
         "troubles des fonctions supérieures.", "Faible"),
        ("Réduire les doses unitaires de morphine SC et/ou augmenter l'intervalle entre "
         "injections chez le sujet âgé, en tenant compte des scores de douleur. L'ACP n'est pas "
         "contre-indiquée (programmation identique, mais oxygénothérapie systématique et dose "
         "limite horaire).", "Fort"),
        ("Ne pas utiliser le dextropropoxyphène chez le sujet âgé.", "Fort"),
        ("Chez le nouveau-né, le nourrisson et l'enfant, après chirurgie majeure : utiliser la "
         "morphine plutôt que les agonistes de palier II (doses réduites chez le nouveau-né et "
         "le nourrisson &lt; 3 mois, immaturité hépatique).", "Fort"),
        ("L'ACP est recommandée dès que le niveau de participation est suffisant (en pratique "
         "dès 6-7 ans) ; ne pas utiliser la morphine par voie sous-cutanée chez l'enfant "
         "(injection douloureuse).", "Fort"),
    ]))
    story.append(Spacer(1, 4 * mm))

    story.append(section_bar("3 — Antalgiques non morphiniques (ANM)", color=TEAL_DARK))
    story.append(Spacer(1, 2 * mm))
    story.append(P(
        "Analgésie multimodale/balancée : associer plusieurs analgésiques à mécanismes d'action "
        "différents pour renforcer l'analgésie et/ou réduire les besoins en morphiniques et leurs "
        "effets secondaires.", S_BODY_SM))
    story.append(Spacer(1, 2 * mm))
    story.append(reco_table([
        ("Associer au moins un ANM lorsque la morphine est utilisée en postopératoire par voie "
         "systémique.", "Fort"),
        ("Associer un AINS à la morphine en l'absence de contre-indications ; ne pas utiliser "
         "les AINS/coxibs en cas d'hypoperfusion rénale ; prendre en compte la majoration du "
         "risque hémorragique (AINS non sélectif) et les facteurs de risque athérothrombotique "
         "pour les coxibs (respecter les contre-indications Afssaps).", "Fort"),
        ("Ne pas utiliser seul le paracétamol associé à la morphine dans les chirurgies à "
         "douleur modérée à sévère ; ne pas l'administrer par voie IV dès que la voie orale est "
         "utilisable.", "Fort"),
        ("Néfopam probablement recommandé après chirurgie à douleur modérée à sévère en "
         "association avec les morphiniques — utiliser probablement avec prudence chez le "
         "patient coronarien (risque de tachycardie).", "Faible"),
        ("Chez l'enfant : corriger déshydratation/hypovolémie avant AINS ; kétoprofène IV "
         "probablement utilisable dès 1 an (hors AMM) ; diclofénac probablement préférable à "
         "l'acide niflumique par voie rectale ; pas de recommandation pour les coxibs chez "
         "l'enfant (données insuffisantes).", "Faible"),
        ("Ne pas prescrire d'AINS pour l'analgésie postamygdalectomie (risque hémorragique, "
         "reprise chirurgicale).", "Fort"),
        ("Chez l'enfant : ne pas administrer le paracétamol par voie IV dès que la voie orale est "
         "utilisable, ni par voie rectale (biodisponibilité faible/imprévisible) ; l'administrer "
         "de façon systématique et non « à la demande ».", "Fort"),
    ]))
    return story


def _section_antihyperalgesiques_chronicisation():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("4 — Agents antihyperalgésiques", color=TEAL_DARK))
    story.append(Spacer(1, 2 * mm))
    story.append(P(
        "L'hyperalgésie postopératoire (périphérique/primaire ou secondaire/centrale) majore la "
        "DPO, la consommation d'opioïdes et l'incidence des douleurs chroniques résiduelles.",
        S_BODY_SM))
    story.append(Spacer(1, 2 * mm))
    story.append(reco_table([
        ("Limiter probablement la consommation d'opioïdes peropératoires pour réduire le risque "
         "de tolérance aiguë à la morphine en postopératoire immédiat.", "Faible"),
        ("Kétamine (antagoniste NMDA le plus efficace) : bolus peropératoire 0,15-0,50 mg/kg, "
         "relais 0,125-0,25 mg/kg/h si chirurgie &gt; 2h, arrêt de la perfusion 30 min avant la "
         "fin de l'anesthésie ; administrer le premier bolus après l'induction (éviter les effets "
         "psychodysleptiques).", "Fort"),
        ("Ne pas utiliser l'association morphine-kétamine dans l'ACP postopératoire.", "Fort"),
        ("Ne pas utiliser le magnésium IV (ne limite pas la douleur ni la consommation de "
         "morphine) ni la clonidine (effets indésirables hémodynamiques trop marqués) en "
         "prévention de l'hyperalgésie.", "—"),
        ("Gabapentine en prémédication probablement recommandée (épargne morphinique, réduction "
         "des scores de douleur).", "Faible"),
        ("Lidocaïne IV probablement recommandée pour l'analgésie après chirurgie abdominale en "
         "l'absence d'ALR.", "Faible"),
    ]))
    story.append(Spacer(1, 4 * mm))

    story.append(section_bar("5 — Prévenir la chronicisation de la DPO (DCPC)", color=TEAL_DARK))
    story.append(Spacer(1, 2 * mm))
    story.append(P(
        "DCPC = douleur persistant &gt; 2 mois après chirurgie, sans étiologie identifiée ni "
        "continuité avec un problème préopératoire ; incidence difficile à estimer (grande "
        "variabilité méthodologique).", S_BODY_SM))
    story.append(Spacer(1, 2 * mm))
    story.append(reco_table([
        ("Prendre en compte la possibilité d'une chronicisation ; rechercher probablement en "
         "préopératoire les facteurs de risque (intensité de la douleur préopératoire, type de "
         "chirurgie, technique opératoire).", "Fort"),
        ("Une forte DPO (surtout neuropathique) est prédictive d'un risque élevé de DCPC : "
         "diagnostiquer et prendre en charge rapidement une douleur neuropathique "
         "postopératoire ; utiliser probablement le questionnaire DN4 comme outil de dépistage.",
         "Fort"),
        ("Chirurgie très ou modérément douloureuse : utiliser de faibles doses de kétamine "
         "peropératoire pour prévenir la DCPC.", "Fort"),
        ("Infiltration d'anesthésiques locaux du site chirurgical : limite probablement la DCPC "
         "après prise de greffon osseux iliaque.", "Faible"),
        ("Bloc paravertébral probablement recommandé pour réduire la DCPC après chirurgie "
         "majeure du sein.", "Faible"),
    ]))
    return story


def _section_infiltration():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("6 — Infiltration du site opératoire", color=TEAL_DARK))
    story.append(Spacer(1, 2 * mm))
    story.append(P(
        "Administration d'un agent analgésique directement dans les berges d'une cicatrice "
        "chirurgicale ou à distance (certains « blocs » comme ilio-inguinal/iliohypogastrique ou "
        "plexus cervical superficiel relèvent de cette définition). Respecter les doses maximales "
        "d'anesthésiques locaux.", S_BODY_SM))
    story.append(Spacer(1, 2 * mm))
    story.append(P("<b>Infiltrations en injection unique</b>", S_BODY_SM))
    story.append(Spacer(1, 1.5 * mm))
    story.append(reco_table([
        ("Infiltrer la cicatrice de cholécystectomie par laparotomie ; utiliser le bloc des "
         "droits pour la cure de hernie ombilicale.", "Fort"),
        ("Cholécystectomie et chirurgie gynécologique par laparoscopie : infiltration des "
         "orifices de trocarts et instillation intrapéritonéale recommandées. Pour les autres "
         "laparotomies abdominales, l'infiltration cicatricielle en injection unique n'a pas "
         "d'intérêt significatif en dehors du TAP block.", "Fort"),
        ("Cure de hernie inguinale : infiltration avec un anesthésique local à longue durée "
         "d'action (injection en plans profonds ou bloc ilio-inguinal plus efficaces que "
         "l'injection SC) ; s'applique aussi aux cicatrices transversales basses (ex. "
         "césarienne sous AG).", "Fort"),
        ("Chirurgie hémorroïdaire : infiltration périanale « en quadrants » ou bloc pudendal "
         "avec neurostimulation.", "Fort"),
        ("Infiltrer la cicatrice de thyroïdectomie avec des anesthésiques locaux à longue durée "
         "d'action.", "Fort"),
    ]))
    story.append(Spacer(1, 2 * mm))
    story.append(P("<b>Infiltrations continues</b>", S_BODY_SM))
    story.append(Spacer(1, 1.5 * mm))
    story.append(reco_table([
        ("Perfusion continue cicatricielle sur laparotomies sous-costales et médianes (cathéter "
         "en plans profonds/prépéritonéal) ; infiltration continue en plans profonds après "
         "hystérectomie par voie abdominale et césarienne.", "Fort"),
        ("Chirurgie majeure du sein et curage axillaire : perfusion continue cicatricielle "
         "probablement recommandée (alternative au bloc paravertébral, recommandé en priorité).",
         "Faible"),
        ("Cure de hernie inguinale : perfusion continue cicatricielle probablement pas utile "
         "(malgré une efficacité démontrée).", "Faible"),
        ("Chirurgie cardiaque : infiltration continue cicatricielle (cathéter sur la face "
         "antérieure du sternum).", "Fort"),
        ("Chirurgie de l'épaule : infiltration continue subacromiale d'un anesthésique local "
         "(en chirurgie ouverte, cathéter possible en sous-cutané, efficacité inférieure à une "
         "ALR plexique).", "Fort"),
        ("Prise de greffon iliaque : infiltration continue à proximité de l'os.", "Fort"),
        ("Chirurgie du genou : cathéter intra-articulaire probablement pas recommandé "
         "(efficacité limitée, risque pour le cartilage).", "Faible"),
    ]))
    return story


def _section_alr():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("7 — Place de l'ALR dans l'analgésie postopératoire", color=TEAL_DARK))
    story.append(Spacer(1, 2 * mm))
    story.append(P("<b>Règles générales</b>", S_BODY_SM))
    story.append(Spacer(1, 1.5 * mm))
    story.append(reco_table([
        ("Proposer une technique d'analgésie aux anesthésiques locaux chaque fois que possible ; "
         "préférer les blocs périphériques aux blocs centraux dès que possible (meilleur rapport "
         "bénéfice/risque).", "Fort"),
        ("Utiliser de préférence la ropivacaïne ou la lévobupivacaïne pour l'analgésie "
         "péridurale ou les blocs périphériques (moindre toxicité cardiaque que la "
         "bupivacaïne).", "Faible"),
        ("Respecter les recommandations de pratique clinique de l'ALR pour l'information, la "
         "pose et la surveillance des cathéters nerveux/périduraux ; respecter les règles "
         "d'asepsie chirurgicale (le repérage échographique est une alternative pour localiser "
         "les nerfs périphériques).", "Fort"),
        ("Associer probablement une analgésie multimodale à l'ALR pour compléter l'efficacité "
         "et/ou prévenir la douleur à la levée du bloc.", "Faible"),
    ]))
    story.append(Spacer(1, 2 * mm))
    story.append(P("<b>Blocs du tronc</b>", S_BODY_SM))
    story.append(Spacer(1, 1.5 * mm))
    story.append(reco_table([
        ("Bloc paravertébral (injection unique ou cathéter) pour diminuer les scores de douleur "
         "et l'incidence des NVPO après chirurgie thoracique (alternative utile à la péridurale).",
         "Fort"),
        ("Bloc paravertébral probablement recommandé après chirurgie majeure du sein.", "Faible"),
        ("Le bloc interpleural ne peut être recommandé (bénéfice limité ne contrebalançant pas "
         "le risque de résorption systémique des anesthésiques locaux).", "—"),
    ]))
    story.append(Spacer(1, 2 * mm))
    story.append(P("<b>Blocs nerveux périphériques</b>", S_BODY_SM))
    story.append(Spacer(1, 1.5 * mm))
    story.append(reco_table([
        ("Cathéter nerveux périphérique recommandé dès lors que la douleur prévisible modérée à "
         "sévère dure &gt; 24h ; mode continu + ACP périnerveuse probablement recommandé pour "
         "l'administration d'anesthésiques locaux.", "Fort"),
        ("Le risque de syndrome des loges n'est pas une contre-indication au bloc (sous "
         "surveillance adaptée) ; ne pas poser de cathéter en cas d'immobilisation plâtrée "
         "postopératoire.", "Fort"),
        ("Épaule : bloc interscalénique recommandé ; si contre-indiqué, bloc suprascapulaire et "
         "infiltrations intra-articulaires probablement recommandés.", "Fort"),
        ("Bras et coude : blocs supraclaviculaire ou infraclaviculaire probablement recommandés.",
         "Faible"),
        ("Avant-bras, poignet, main : blocs axillaire ou au canal huméral probablement "
         "recommandés.", "Faible"),
        ("Doigts (rééducation active nécessaire) : blocs tronculaires distaux probablement "
         "recommandés.", "Faible"),
        ("Membre inférieur : ne pas utiliser l'analgésie péridurale (blocs périphériques aussi "
         "efficaces, moins d'effets indésirables).", "Fort"),
        ("Hanche : bloc fémoral probablement recommandé.", "Faible"),
        ("Diaphyse fémorale, chirurgie ou traumatisme (adulte et enfant) : bloc fémoral "
         "recommandé.", "Fort"),
        ("Chirurgie invasive du genou (ex. prothèse totale) : cathéter fémoral recommandé ; bloc "
         "sciatique en injection unique probablement recommandé en complément.", "Fort"),
        ("Chirurgie ligamentaire du genou : bloc fémoral (cathéter ou injection unique) "
         "probablement recommandé.", "Faible"),
        ("Arthroscopie mineure du genou : administration intra-articulaire d'anesthésique local "
         "(± adjuvant) ou bloc fémoral en injection unique recommandés.", "Fort"),
        ("Jambe, cheville, pied (adulte et enfant) : bloc sciatique recommandé.", "Fort"),
        ("Chirurgie mineure du pied : bloc de cheville probablement recommandé (cathéter "
         "possible au niveau du nerf tibial).", "Faible"),
    ]))
    return story


def _section_alr_suite_ambulatoire_sources():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(P("<b>Analgésie périmédullaire</b>", S_BODY_SM))
    story.append(Spacer(1, 1.5 * mm))
    story.append(reco_table([
        ("Injection intrathécale de morphine ≤ 0,1 mg chez le sujet ASA I/II : surveillance "
         "possible en secteur traditionnel.", "—"),
        ("Analgésie péridurale : anesthésiques locaux à faible concentration + morphinique, "
         "cathéter inséré au milieu de la zone des dermatomes à bloquer.", "Fort"),
        ("Analgésie périmédullaire recommandée après chirurgie thoracique ou intra-abdominale "
         "majeure (gastrique, pancréatique, colique, grêle, œsophage, cystectomie) — améliore "
         "l'analgésie, réduit la durée de l'iléus, raccourcit le délai d'extubation.", "Fort"),
        ("Ne pas utiliser probablement l'analgésie péridurale après chirurgie vasculaire "
         "périphérique (aucun impact sur l'analgésie, la morbidité respiratoire/"
         "cardiovasculaire).", "Faible"),
        ("Enfant : réaliser un bloc pénien pour l'analgésie après circoncision.", "Fort"),
    ]))
    story.append(Spacer(1, 4 * mm))

    story.append(section_bar("8 — Organiser l'analgésie en chirurgie ambulatoire", color=TEAL_DARK))
    story.append(Spacer(1, 2 * mm))
    story.append(reco_table([
        ("Les établissements ayant une activité ambulatoire doivent développer une stratégie "
         "spécifique d'évaluation/traitement de la DPO à domicile, évaluée régulièrement et de "
         "façon pluridisciplinaire.", "Fort"),
        ("Apprécier les éléments prédictifs de la DPO et de la tolérance aux analgésiques "
         "prescrits à domicile ; expliquer les modalités de l'analgésie orale dès la "
         "consultation préopératoire (chirurgie, anesthésie).", "Fort"),
        ("Remettre les ordonnances d'antalgiques dès la consultation de chirurgie/anesthésie, "
         "précisant les horaires de prise systématique et les conditions de recours à un palier "
         "supérieur si nécessaire.", "Fort"),
        ("PEC de la DPO à domicile par voie locorégionale : informer le médecin traitant par "
         "avance et le prévenir de la sortie du patient.", "Fort"),
        ("Utiliser les infiltrations et blocs périphériques en injection unique pour la "
         "chirurgie ambulatoire lorsque l'indication opératoire s'y prête ; la sortie malgré "
         "l'absence de levée du bloc est possible si analgésie de secours, attelles, "
         "information écrite, assistance à domicile et procédures d'appel sont prévues.", "Fort"),
        ("Cathéters périnerveux à domicile : réserver aux interventions dont la DPO est "
         "totalement (ou en grande partie) couverte par le bloc périnerveux ; contact "
         "téléphonique quotidien recommandé.", "Fort"),
    ]))
    story.append(Spacer(1, 4 * mm))

    story.append(section_bar("Sources et traçabilité", color=GREY))
    story.append(Spacer(1, 2 * mm))
    story.append(P(
        "<b>Document source :</b> « Prise en charge de la douleur postopératoire chez l'adulte "
        "et l'enfant » (Information professionnelle, RFE 2008, actualisation de la conférence de "
        "consensus de 1997). Comité douleur-anesthésie locorégionale et comité des référentiels "
        "de la Sfar. Coordonnateurs : D. Fletcher, F. Aubrun. 22 experts + 1 infirmière "
        "référente douleur. Ann Fr Anesth Reanim 2008;27:1035-1041.", S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P("<b>Méthodologie :</b> méthode GRADE, force codée dans le verbe de chaque "
                    "phrase (« il est recommandé » = Fort, « il est probablement recommandé » = "
                    "Faible — voir disclosure méthodologique en page 1), 4 tours de cotation, 124 "
                    "recommandations consensuelles annoncées par la source (8 thèmes).",
                    S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P("<b>Couverture :</b> cette fiche reprend l'intégralité du contenu prescriptif "
                    "des 8 thèmes (sections 4 à 11 de la source). Les sections 1-3 (introduction, "
                    "justification du choix RFE/GRADE) sont résumées dans le panneau de "
                    "méthodologie plutôt que retranscrites in extenso (contenu procédural sur "
                    "l'élaboration du référentiel, sans recommandation clinique).", S_SOURCE))
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Avertissement — document de 2008 :</b> ce document est une fiche de synthèse "
        "indépendante, produite pour un usage d'aide-mémoire. Elle reprend l'intégralité des "
        "recommandations du texte source, mais ne remplace pas le texte intégral (argumentaire "
        "complet) et n'est ni éditée ni validée par la Sfar. Certaines pratiques (ex. molécules, "
        "voies d'administration) peuvent avoir évolué depuis 2008 : en cas de doute, se référer "
        "au texte intégral et/ou à un avis spécialisé.",
        S_BODY_SM), bg=GREY_LIGHT, border=GREY))
    return story


SECTIONS = [
    ("Évaluer la PEC & morphiniques (1/2)", _section_intro_pec),
    ("Morphiniques (2/2) & antalgiques non morphiniques", _section_morphiniques_suite_anm),
    ("Antihyperalgésiques & prévention de la chronicisation", _section_antihyperalgesiques_chronicisation),
    ("Infiltration du site opératoire", _section_infiltration),
    ("Place de l'ALR (1/2)", _section_alr),
    ("ALR (2/2), ambulatoire & sources", _section_alr_suite_ambulatoire_sources),
]

def _make_doc(path=None):
    return SimpleDocTemplate(path or OUT, pagesize=A4,
                              leftMargin=MARGIN, rightMargin=MARGIN,
                              topMargin=32 * mm, bottomMargin=16 * mm,
                              title="Sfar 2008 - Douleur postoperatoire adulte et enfant",
                              author="Synthèse indépendante (source Sfar)")

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
