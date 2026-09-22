# -*- coding: utf-8 -*-
"""
Fiche de synthese - Societe Francaise d'Anesthesie et de Reanimation (SFAR).
"Techniques analgesiques locoregionales et douleur chronique" -
Recommandations Formalisees d'Experts (RFE), 2013. Auteurs : H. Beloeil,
E. Viel, M.-L. Navez, D. Fletcher, D. Peronnet. Ann Fr Anesth Reanim 32
(2013) 275-284 (doi:10.1016/j.annfar.2013.02.021). 10 pages, telecharge
depuis sfar.org (wp-content/uploads/2015/10/2a_AFAR_Techniques-analgesiques
-locoregionales-et-douleur-chronique.pdf).

METHODOLOGIE : GRADE standard (deja utilise dans ce corpus, PAS une
nouvelle convention) - qualite des preuves en 4 categories, force binaire
Forte (1+/1-) ou Faible (2+/2-), vote Delphi. En l'absence d'evaluation
quantifiee, avis d'experts (chip "AE").

DEUX CATEGORIES SUPPLEMENTAIRES DISCLOSED (ni GRADE ni AE au sens habituel,
trouvees en lisant le texte source en integralite) :
- chip "Oe" (Oe = la lettre O barree/cercle, rendue ici "0/") - la source
  formule explicitement, a 9 reprises, qu'aucune recommandation n'est
  possible faute de donnees ("il n'est pas possible de formuler de
  recommandation..."). Ce n'est PAS une recommandation negative (differe
  d'un Grade 1-/2- qui EST une recommandation, juste defavorable) - c'est
  l'absence de toute recommandation. Incoherence source disclosed, pas
  resolue silencieusement : la source elle-meme etiquette 7 des 9 clauses
  "Avis d'experts" malgre etre des non-recommandations (verifie ligne par
  ligne sur le texte extrait : R1/clonidine, R1/blocs sympathiques
  non-SDRC, R1/blocs somatiques non-SDRC, R2/spheno-palatins,
  R3/infiltrations therapeutiques pelviennes, R5/autres blocs
  neurolytiques cancereux, R6/duree-sevrage catheter) ; seules 2 clauses
  n'ont strictement aucun tag terminal (R2/cephalee de tension,
  R5/peridurale dans la douleur cancereuse refractaire - cette derniere
  faisant partie de la meme phrase source qu'une recommandation Grade 1+
  sur l'intrathecale, cf. scission plus bas) - dans tous les cas ce chip
  "0/" est utilise plutot que AE ou un grade, pour ne jamais laisser croire
  qu'une position (meme d'expert) a ete prise.
- chip "NG" (non gradue) - une unique clause (R2, bloc du grand nerf
  occipital en cas de cephalees secondaires a une hypotension intracranienne
  iatrogene ou CI au blood-patch) est formulee de facon permissive ("il est
  possible de...") mais sans qu'aucun grade ni "Avis d'experts" ne lui soit
  explicitement accole dans le texte source (contrairement a la clause
  blood-patch immediatement precedente, elle-meme Grade 2+) - disclosed
  plutot que d'inventer un grade par extrapolation.

29 des 33 recommandations reellement gradees comportent un caveat sur les
details d'application (choix du produit, rythme, nombre de gestes) pour
lesquels la source dit elle-meme "en l'absence de donnees, pas de
recommandation possible" DANS LA MEME PHRASE/le meme paragraphe que la
recommandation positive - ces caveats sont conserves comme partie du texte
de la ligne (pas une fusion de deux grades differents : la source
n'attribue qu'un seul grade a l'ensemble de la phrase), conformement a la
regle anti-grade-composite (qui s'applique quand DEUX grades DIFFERENTS
sont fusionnes, pas quand un caveat sans grade propre accompagne une
recommandation qui, elle, en a un).

UN CAS DE VRAIE SCISSION (regle anti-grade-composite appliquee) : R5,
analgesie intrathecale vs peridurale dans la douleur cancereuse refractaire
- la source enonce "il faut realiser une analgesie intrathecale... (Grade
1+)" PUIS, dans la meme phrase source, "il n'est pas possible de
recommander l'analgesie peridurale" pour un sous-groupe specifique
(esperance de vie courte, hors symptomatologie localisee) - deux
techniques differentes, deux conclusions differentes (1+ vs aucune
recommandation) : scinde en 2 lignes distinctes plutot que fusionne.

COUVERTURE : integralite des 33 recommandations reellement gradees + les
9 "absence de recommandation possible" + la 1 clause non graduee (43
enonces au total), sur les 6 champs de la RFE (medicaments, algies
craniofaciales, douleurs abdomino-pelviennes, douleurs neuropathiques des
membres [SDRC, amputation], douleurs cancereuses, gestion des catheters au
long cours). Argumentaire scientifique (etudes, pourcentages, meta-
analyses) volontairement non transcrit au-dela des elements qui changent
reellement la pratique (doses, seuils temporels) - regle de projet
2026-09-14. Annexes non publiees dans le texte (tableaux d'analyse de la
litterature sur le site SFAR) non couvertes - disclosed en derniere page.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from style import *
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.units import mm

OUT = "/home/user/rfe-sfar-website/output/Fiche_SFAR_ALR_Douleur_Chronique_2013.pdf"

SOURCE_TXT = ("Source : « Techniques analgésiques locorégionales et douleur chronique » — "
              "RFE SFAR, Ann Fr Anesth Réanim 32 (2013) 275-284. Fiche de synthèse non "
              "officielle : se référer au texte intégral.")

def P(txt, style=S_CELL):
    return Paragraph(txt, style)

def chip(label, **kw):
    return grade_chip(label, **kw)

CW_FULL = PAGE_W - 2 * MARGIN
RCW = [CW_FULL - 14 * mm, 14 * mm]

def reco_table(rows, col_widths=RCW):
    """rows: (text, grade_label)."""
    data = [[P("Recommandation", S_HEAD_W), P("Grade", S_HEAD_W_C)]]
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

def legend_flowable():
    chip_w = 14 * mm
    content_w = CW_FULL
    row = Table([[chip("1+", width=chip_w - 2 * mm), chip("1-", width=chip_w - 2 * mm),
                  chip("2+", width=chip_w - 2 * mm), chip("2-", width=chip_w - 2 * mm),
                  chip("AE", width=chip_w - 2 * mm), chip("0/", width=chip_w - 2 * mm),
                  chip("NG", width=chip_w - 2 * mm),
                  P("<b>GRADE</b> — 1+/1- : forte (« il faut »/« il ne faut pas ») ; "
                    "2+/2- : faible (« il est possible »/« il n'est pas recommandé ») ; "
                    "<b>AE</b> : avis d'experts (vraie recommandation, sans évaluation "
                    "quantifiée) ; <b>0/</b> : la source déclare explicitement qu'<b>aucune "
                    "recommandation n'est possible</b> faute de données (n'est PAS un "
                    "grade négatif) ; <b>NG</b> : énoncé permissif de la source sans grade "
                    "ni avis d'experts explicitement accolé (1 occurrence, disclosed).",
                    S_BADGE_HEAD)]],
                colWidths=[chip_w] * 7 + [content_w - 7 * chip_w])
    row.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                              ("LEFTPADDING", (0, 0), (-1, -1), 1),
                              ("RIGHTPADDING", (0, 0), (-1, -1), 1),
                              ("TOPPADDING", (0, 0), (-1, -1), 0),
                              ("BOTTOMPADDING", (0, 0), (-1, -1), 0)]))
    return row

TOTAL_PAGES = {"n": 7}

def on_page(canvas, doc, page_title):
    header_band(canvas, doc, "SFAR — RFE, 2013",
                "Techniques analgésiques locorégionales et douleur chronique",
                page_title, icon_fn=lambda c, x, y: icon_pill(c, x, y, 13 * mm), color=TEAL_DARK)
    footer_band(canvas, doc, SOURCE_TXT, f"Page {doc.page} / {TOTAL_PAGES['n']}")

# ---------------------------------------------------------------------------
def _section_intro():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Résumé :</b> Recommandations Formalisées d'Experts SFAR (2013) sur la place "
        "des techniques d'analgésie locorégionale (ALR) dans la douleur chronique — "
        "aucune recommandation francophone n'existait auparavant sur ce sujet. Six champs : "
        "médicaments utilisés, algies craniofaciales, douleurs abdomino-pelviennes, "
        "douleurs neuropathiques des membres (SDRC, amputation), douleurs cancéreuses, "
        "gestion des cathéters au long cours. Pathologies rachidiennes explicitement "
        "exclues de cette RFE (objet d'une recommandation multi-spécialités séparée).",
        S_BODY), bg=GREY_LIGHT, border=GREY))
    story.append(Spacer(1, 2.5 * mm))
    story.append(P(
        "Méthode GRADE — analyse systématique de la littérature (2001-2011) par 23 experts. "
        "Critère principal : amélioration fonctionnelle / qualité de vie (à défaut, niveau de "
        "douleur et consommation d'antalgiques). La littérature sur l'ALR en douleur chronique "
        "est globalement de faible niveau méthodologique — la force des recommandations est "
        "donc très variable selon le thème.", S_BODY_SM))
    story.append(Spacer(1, 3 * mm))
    story.append(legend_flowable())
    return story

def _section_r1():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("R1 — Médicaments utilisés en ALR pour douleur chronique"),
        Spacer(1, 1.5 * mm),
        P("<b>Voie périmédullaire et intrathécale</b>", S_CELL_B),
    ]))
    story.append(Spacer(1, 1 * mm))
    story.append(reco_table([
        ("Traiter des douleurs prolongées non cancéreuses réfractaires aux traitements "
         "antalgiques conventionnels bien conduits, ou en cas d'intolérance/absence "
         "d'alternative, par administration continue intrathécale ou péridurale "
         "d'anesthésique local (aucun anesthésique local privilégié par la littérature).", "2+"),
        ("Ne pas utiliser la kétamine ni le midazolam par voie périmédullaire, en raison de "
         "l'absence de données toxicologiques.", "AE"),
        ("Clonidine par voie périmédullaire : en l'absence de données, aucune recommandation "
         "n'est possible.", "0/"),
        ("Utiliser la morphine en administration intrathécale chez des patients douloureux "
         "chroniques, en cas d'échec des thérapies conventionnelles après sélection "
         "rigoureuse.", "1+"),
        ("Ne pas réaliser d'injection péridurale de corticoïdes pour douleur "
         "post-zostérienne.", "1-"),
        ("Réaliser une injection péridurale de corticoïdes en cas de radiculalgie résistante "
         "au traitement médical et physiothérapique bien conduit, pour un soulagement à "
         "court terme (réitérable si le patient est répondeur).", "2+"),
        ("Utiliser le ziconotide par voie intrathécale en première intention dans les "
         "douleurs chroniques réfractaires, notamment à composante neuropathique "
         "prédominante — titration lente, dose initiale faible (1 mg/j) ; association à la "
         "morphine possible.", "1+"),
    ]))
    story.append(Spacer(1, 2 * mm))
    story.append(P("<b>Voie périnerveuse / ALR intraveineuse (ALRIV)</b>", S_CELL_B))
    story.append(Spacer(1, 1 * mm))
    story.append(reco_table([
        ("Blocs sympathiques par administration répétée d'anesthésiques locaux, en douleur "
         "chronique non-SDRC (adulte et enfant) : en l'absence de données, aucune "
         "recommandation n'est possible.", "0/"),
        ("Blocs somatiques par administration intermittente d'anesthésiques locaux, en "
         "douleur chronique non-SDRC (adulte et enfant) : en l'absence de données, aucune "
         "recommandation n'est possible.", "0/"),
        ("Ne pas utiliser corticoïdes ni morphiniques lors d'un bloc nerveux périphérique "
         "(somatique ou sympathique) en douleur chronique, adulte et enfant (absence "
         "d'efficacité démontrée).", "2-"),
        ("Utiliser une injection locale de corticoïdes en cas de canal carpien "
         "symptomatique.", "2+"),
    ]))
    return story

def _section_r2():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("R2 — Algies craniofaciales"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("Ne pas faire de bloc du nerf grand occipital (GNO) en cas de céphalées "
         "quotidiennes chroniques ne répondant pas au traitement médical — possible "
         "toutefois en dernier recours après échec de tous les traitements bien conduits "
         "(avis d'experts), maximum 4 blocs itératifs aux anesthésiques locaux.", "2-"),
        ("Bloc du GNO dans la céphalée de tension : en l'absence de données, aucune "
         "recommandation n'est possible.", "0/"),
        ("Réaliser un blood-patch (injection péridurale de sang autologue) en cas de "
         "céphalées secondaires à une hypotension intracrânienne (primaire ou secondaire) "
         "ne répondant pas au traitement médical — plusieurs blood-patches possibles "
         "(jusqu'à 4).", "2+"),
        ("Faire un bloc du GNO en cas de céphalées secondaires à une hypotension "
         "intracrânienne iatrogène ne répondant pas à l'algorithme proposé, ou en cas de "
         "contre-indication au blood-patch — énoncé par la source sans grade ni avis "
         "d'experts explicitement accolé (disclosed, voir méthodologie).", "NG"),
        ("Réaliser un bloc du GNO (nerf d'Arnold) en cas de céphalées cervicogéniques.", "2+"),
        ("Réaliser un bloc du GNO (nerf d'Arnold) en cas d'algie vasculaire de la face ne "
         "répondant pas aux traitements spécifiques bien conduits.", "2+"),
        ("Blocs sphéno-palatins dans l'algie vasculaire de la face rebelle aux traitements "
         "validés (oxygénothérapie, sumatriptan, vérapamil) ou mal tolérés : en l'absence "
         "de données, aucune recommandation n'est possible.", "0/"),
        ("Réaliser un bloc d'une ou plusieurs branches terminales du nerf trijumeau "
         "(V1/V2/V3) dans la névralgie de la face rebelle à la carbamazépine ou mal "
         "tolérée.", "AE"),
    ]))
    return story

def _section_r3():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("R3 — Douleurs abdomino-pelviennes"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("En cas de douleur pelvi-périnéale chronique, pratiquer à titre diagnostique des "
         "infiltrations d'anesthésiques locaux sur le système somatique et sympathique "
         "pelvien, avec une technique de repérage adaptée et fiable, associée à une prise "
         "en charge globale.", "2+"),
        ("Infiltrations à visée thérapeutique (et non diagnostique) sur le système nerveux "
         "somatique ou sympathique pelvien : en l'absence de données, aucune "
         "recommandation n'est possible.", "0/"),
    ]))
    return story

def _section_r4():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("R4 — Douleurs neuropathiques des membres"),
        Spacer(1, 1.5 * mm),
        P("<b>Syndrome douloureux régional complexe (SDRC)</b>", S_CELL_B),
    ]))
    story.append(Spacer(1, 1 * mm))
    story.append(reco_table([
        ("Répéter un bloc sympathique avec anesthésiques locaux dans le traitement d'un "
         "SDRC, si le bénéfice analgésique et fonctionnel a été testé et persiste en cours "
         "de traitement (aucune recommandation possible sur le choix de l'anesthésique "
         "local, le rythme ou le nombre de blocs, faute de données).", "2+"),
        ("Ne pas pratiquer de bloc locorégional intraveineux (ALRIV), quel que soit l'agent "
         "médicamenteux, pour le traitement d'un SDRC.", "2-"),
        ("Réaliser une analgésie locorégionale continue par cathéter périnerveux pour le "
         "traitement des SDRC, en cas d'échec des autres traitements.", "2+"),
        ("Traiter un SDRC avec une ALR centrale ou périphérique chez l'enfant, en cas de "
         "résistance aux traitements systémiques conventionnels bien menés.", "2+"),
        ("Pratiquer des blocs itératifs du ganglion stellaire pour le traitement des SDRC du "
         "membre supérieur chez les patients répondeurs (aucune recommandation possible "
         "sur le rythme ou le nombre de blocs).", "2+"),
        ("Pratiquer des blocs sensitivo-moteurs continus par cathéters pour faciliter la "
         "rééducation fonctionnelle, en cas de résistance aux traitements systémiques bien "
         "conduits et aux traitements par blocs sympathiques.", "2+"),
        ("Toujours associer aux blocs sympathiques et/ou sensitivo-moteurs des traitements "
         "adaptés intensifs de rééducation fonctionnelle lors du traitement des CRPS des "
         "membres.", "2+"),
        ("Mettre en place une stimulation médullaire lors du traitement des CRPS des "
         "membres, en cas de résistance à la kinésithérapie, aux traitements systémiques "
         "bien conduits et aux traitements par blocs sympathiques (aucune recommandation "
         "possible sur le choix chirurgical ou percutané de la technique de pose).", "2+"),
    ]))
    story.append(Spacer(1, 2 * mm))
    story.append(P("<b>Amputation</b>", S_CELL_B))
    story.append(Spacer(1, 1 * mm))
    story.append(reco_table([
        ("Réaliser une analgésie locorégionale chez les patients amputés (adultes et "
         "enfants) — procure une analgésie postopératoire de qualité et diminue "
         "l'incidence des douleurs du moignon.", "1+"),
        ("Les données actuelles ne permettent pas de privilégier une modalité d'ALR à une "
         "autre (analgésie périmédullaire, bloc tronculaire ou plexique) ; privilégier "
         "toutefois les blocs analgésiques périphériques, en raison de l'absence d'effets "
         "secondaires généraux (notamment hémodynamiques) par rapport aux blocs "
         "périmédullaires.", "AE"),
    ]))
    return story

def _section_r5():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("R5 — Douleurs cancéreuses"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("Réaliser précocement un bloc neurolytique splanchnique ou du plexus cœliaque "
         "chez les patients porteurs d'un cancer du pancréas, pour réduire la douleur, la "
         "consommation de morphiniques et leurs effets indésirables.", "2+"),
        ("Réaliser un bloc neurolytique du plexus hypogastrique chez les patients présentant "
         "des douleurs importantes en rapport avec un cancer du petit bassin.", "2+"),
        ("Autres blocs neurolytiques (impar, lombaire, thoracique) chez le patient "
         "cancéreux : en l'absence de données, aucune recommandation n'est possible.", "0/"),
        ("Réaliser une analgésie intrathécale dans les douleurs chroniques cancéreuses "
         "réfractaires malgré un traitement antalgique bien conduit selon les "
         "recommandations de l'OMS, et chez les patients ayant des effets indésirables "
         "graves aux traitements antalgiques.", "1+"),
        ("Analgésie péridurale dans la douleur chronique cancéreuse réfractaire : sauf "
         "symptomatologie localisée chez un patient à espérance de vie courte, aucune "
         "recommandation n'est possible.", "0/"),
        ("Ne pas utiliser de cathéters externalisés.", "1-"),
        ("Mettre en place une pompe implantée, si la survie du patient est estimée à au "
         "moins trois mois.", "AE"),
        ("La morphine est le traitement de référence par voie intrathécale ; les "
         "anesthésiques locaux, la clonidine et le ziconotide peuvent être utilisés en "
         "association.", "AE"),
        ("Chez l'enfant atteint de cancer, traiter des douleurs prolongées réfractaires aux "
         "traitements antalgiques conventionnels bien conduits (ou en cas d'intolérance), "
         "par des techniques d'ALR centrales ou périphériques adaptées au type de "
         "douleur.", "2+"),
    ]))
    return story

def _section_r6():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("R6 — Gestion des cathéters d'ALR au long cours"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("Durée, intérêt des fenêtres thérapeutiques, mode de sevrage d'un cathéter "
         "locorégional au long cours : en l'absence de données, aucune recommandation "
         "n'est possible.", "0/"),
        ("Envisager le recours à l'analgésie péridurale dès lors que l'administration de "
         "produit analgésique prévisible est inférieure à trois mois — le cathéter peut "
         "alors être tunnélisé et relié à distance à un site sous-cutané et une pompe "
         "programmable.", "2+"),
        ("Ne pas utiliser de cathéter péridural au-delà de trois mois, en raison du risque "
         "de cloisonnement et du risque infectieux — un cathéter intrathécal relié à un "
         "dispositif totalement implantable peut alors être mis en place.", "2-"),
    ]))
    return story

def _section_sources():
    story = []
    story.append(section_bar("Sources et traçabilité", color=GREY))
    story.append(Spacer(1, 2 * mm))
    story.append(P(
        "<b>Document source :</b> « Techniques analgésiques locorégionales et douleur "
        "chronique » — Recommandations Formalisées d'Experts (RFE), Société française "
        "d'anesthésie et de réanimation (SFAR). Auteurs : H. Beloeil (Rennes, auteur "
        "correspondant), É. Viel (Nîmes), M.-L. Navez (Saint-Étienne), D. Fletcher "
        "(Garches), D. Peronnet (Mâcon). Groupe de travail : A. Muller, E. Bures, "
        "P. Martin, P. Rault, F. Adam, I. Nègre, D. Dupoiron, J.-M. Pellat, P. Zetlaoui, "
        "C. Dadure, F. Veyckemans, P. Marec-Berard, T. Riant, C. Baude, J.-P. Estèbe, "
        "A. Belbachir, V. Martinez.", S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P("<b>Version :</b> Ann Fr Anesth Réanim 32 (2013) 275-284. "
                    "doi:10.1016/j.annfar.2013.02.021.", S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P("<b>Méthodologie :</b> GRADE standard (qualité des preuves à 4 "
                    "catégories, force forte/faible par vote Delphi) — voir légende en "
                    "page 1 pour les 2 catégories supplémentaires disclosed (« 0/ » : "
                    "aucune recommandation possible ; « NG » : énoncé non gradé "
                    "explicitement, 1 occurrence).", S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>URL source :</b> https://sfar.org/wp-content/uploads/2015/10/"
        "2a_AFAR_Techniques-analgesiques-locoregionales-et-douleur-chronique.pdf",
        S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P("<b>Couverture :</b> intégralité des 33 recommandations réellement "
                    "gradées + les 9 énoncés « aucune recommandation possible » + le 1 "
                    "énoncé non gradé (43 au total), sur les 6 champs de la RFE. "
                    "Pathologies rachidiennes explicitement exclues par la source elle-même "
                    "(objet d'une recommandation séparée multi-spécialités). Argumentaire "
                    "scientifique (études, pourcentages, méta-analyses) volontairement non "
                    "transcrit au-delà des éléments qui changent la pratique. Annexes "
                    "(tableaux d'analyse de la littérature, non publiées dans le texte mais "
                    "sur sfar.org) non couvertes par cette fiche.", S_SOURCE))
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Avertissement — document de 2013 :</b> cette fiche de synthèse indépendante "
        "reprend l'intégralité des recommandations et énoncés du texte source, mais ne le "
        "remplace pas et n'est ni éditée ni validée par la SFAR. Les pratiques et "
        "disponibilités thérapeutiques (ex. ziconotide) ayant pu évoluer depuis 2013, se "
        "référer à un avis spécialisé et aux recommandations actualisées avant toute "
        "décision.", S_BODY_SM), bg=GREY_LIGHT, border=GREY))
    return story

def _section_intro_r1():
    story = _section_intro()
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_r1())
    return story

def _section_r2_r3():
    story = _section_r2()
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_r3())
    return story

def _section_r5_r6_sources():
    story = _section_r5()
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_r6())
    story.append(Spacer(1, 4 * mm))
    story.extend(_section_sources())
    return story

SECTIONS = [
    ("Méthodologie & médicaments (R1)", _section_intro_r1),
    ("Algies craniofaciales & douleurs abdomino-pelviennes (R2-R3)", _section_r2_r3),
    ("Douleurs neuropathiques des membres (R4)", _section_r4),
    ("Douleurs cancéreuses, cathéters au long cours & sources (R5-R6)", _section_r5_r6_sources),
]

def _make_doc(path=None):
    return SimpleDocTemplate(path or OUT, pagesize=A4,
                              leftMargin=MARGIN, rightMargin=MARGIN,
                              topMargin=32 * mm, bottomMargin=16 * mm,
                              title="Fiche SFAR 2013 - Techniques analgesiques "
                                    "locoregionales et douleur chronique",
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

    final_story = _build_upto(fns)
    docf = _make_doc()
    docf.build(final_story, onFirstPage=on_page_final, onLaterPages=on_page_final)
    print("OK ->", OUT, f"({total_pages} pages)")

if __name__ == "__main__":
    build()
