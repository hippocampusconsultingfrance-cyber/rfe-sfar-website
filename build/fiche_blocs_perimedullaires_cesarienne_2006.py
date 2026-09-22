# -*- coding: utf-8 -*-
"""
Fiche de synthese - "Les blocs perimedullaires chez l'adulte" - Question 7
(Quels blocs perimedullaires faut-il faire pour la cesarienne ?) -
Recommandations pour la Pratique Clinique (RPC), SFAR/Sofcot/Sofmer,
presentees le 24 septembre 2005 (47e congres SFAR), publiees Ann Fr Anesth
Reanim 26 (2007) 720-752.

TROISIEME INSTALLMENT de ce document (voir `fiche_blocs_perimedullaires_ci_2006.py`
pour Q1-2, `fiche_blocs_perimedullaires_technique_2006.py` pour Q3-5).
Perimetre volontairement limite (meme pattern) : 369 citations de grade sur
15 "Questions" au total dans le document source complet.

QUESTION 6 DELIBEREMENT EXCLUE (collision verifiee AVANT redaction, comme
demande par le pipeline standard de ce depot) : la Question 6 ("Quels blocs
perimedullaires pour le travail obstetrical ?") est explicitement superseded
par `douleur_accouchement_2025` (HAS, RBP validee 30 avril 2025), deja
git-trackee dans ce depot - son propre texte source se decrit lui-meme comme
"actualisation des recommandations SFAR de 2006 sur l'analgesie
obstetricale", ce qui est exactement le perimetre de cette Question 6 de
2006. Construire une fiche pour ce contenu de 2006 dupliquerait/entrerait en
conflit avec une reference 2025 deja a jour sur le meme sujet - meme logique
que l'incident prééclampsie 2009/2020 documente dans CLAUDE.md. Question 6
non construite, pas de collision de cle site (aucun contenu n'a ete ajoute
pour elle).

QUESTION 8 (analgesie postoperatoire perimedullaire, hors cesarienne
specifiquement - indications, surveillance, agents) N'EST PAS couverte ici -
c'est un installment separe et plus volumineux (71 citations de grade brutes
contre 34 pour cette Question 7), a construire separement. Les Questions 9 a
15 restent egalement hors perimetre.

NOUVELLE DECOUVERTE METHODOLOGIQUE, disclosed explicitement (incoherence
interne du source, regle 5 - jamais resolue silencieusement) : le preambule
du document ("GRADATION DES RECOMMANDATIONS EN MEDECINE FACTUELLE, ANAES
AVRIL 2004", verifie ligne par ligne) definit UNIQUEMENT Grade A/B/C +
"Accord professionnel" - AUCUN "Grade D" n'y est defini. Pourtant le corps du
texte cite explicitement "(grade D)" a 10 reprises dans l'ensemble du
document (verifie par grep exhaustif sur le fichier source complet, pas
seulement cette Question), dont UNE occurrence dans le perimetre de cette
fiche (Question 7, surveillance maternelle peroperatoire). Ni la fiche
Q1-2 ni la fiche Q3-5 (deja publiees) ne sont concernees - verifie, aucune
occurrence de "grade D" dans leurs perimetres respectifs (lignes 210-1091),
donc aucune correction retroactive necessaire sur ces fiches. Ce "grade D",
n'etant defini nulle part par le source lui-meme, est presente ici avec un
chip visuellement distinct ("D", bleu marine) plutot que d'etre arbitrairement
assimile a un grade C ou a un accord professionnel - un choix qui inventerait
une equivalence que le source ne formule jamais.

FIGURE (Fig. 1, page 734 du document source) : deux algorithmes decisionnels
(choix de la technique d'ALR selon "cesarienne non programmee" / "cesarienne
programmee") presentes sous forme de diagramme visuel (encadres colores +
fleches, pas de texte lineaire extractible par l'extraction automatique -
verifie par rendu visuel du PDF source a 150dpi, page 734, confirmant que le
contenu des encadres n'apparaissait pas dans le texte extrait en ordre de
lecture). Ce corpus n'a pas de pattern etabli pour integrer une image
matricielle dans une fiche reportlab (aucun fiche_*.py existant n'importe
`reportlab.platypus.Image` - verifie par grep) ; le diagramme est donc
retranscrit fidelement sous forme de texte structure (arborescence de
decision), reproduisant CHAQUE encadre et CHAQUE branche du schema source
sans en omettre ni en reformuler le sens clinique, avec disclosure explicite
qu'il s'agit d'une transcription textuelle d'un diagramme visuel plutot que
du diagramme lui-meme.

DECOMPTE - methodologie de consolidation identique aux installments
precedents (disclosed) : grep exhaustif sur le texte source de la Question 7
(lignes 1499-1765 du fichier texte extrait) trouve 34 citations de grade
individuelles : grade A x4, grade B x7, grade C x22, grade D x1. Plusieurs
citations de MEME grade decrivant le MEME point clinique dans un seul
paragraphe source sont regroupees en une seule ligne (jamais deux grades
DIFFERENTS fusionnes dans une seule ligne - verifie par le safety net regex
apres redaction, aucune occurrence trouvee). Apres consolidation : 31 lignes
de recommandations gradees (A:4, B:5, C:20, D:1, AE:1 [« consensus
professionnel », une eclampsie avec HTIC/signes de localisation - meme
variante terminologique deja rencontree en Q3-5]), verifie par regex sur le
script final.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from style import *
GRADE_COLORS["A"] = (GREEN, WHITE)
GRADE_COLORS["B"] = (TEAL, WHITE)
GRADE_COLORS["C"] = (AMBER, WHITE)
GRADE_COLORS["D"] = (NAVY, WHITE)
GRADE_COLORS["AE"] = (GREY, WHITE)
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.units import mm

OUT = "/home/user/rfe-sfar-website/output/Fiche_Blocs_Perimedullaires_Cesarienne_2006.pdf"

SOURCE_TXT = ("Source : SFAR/Sofcot/Sofmer, « Les blocs périmédullaires chez l'adulte », "
              "RPC, Ann Fr Anesth Réanim 26 (2007) 720-752 — Question 7 uniquement. "
              "Fiche de synthèse non officielle : se référer au texte intégral.")

def P(txt, style=S_CELL):
    return Paragraph(txt, style)

def chip(label, **kw):
    return grade_chip(label, **kw)

CW_FULL = PAGE_W - 2 * MARGIN

def reco_table(rows, col_widths):
    """rows: (ref, text, grade_label)."""
    data = [[P("Catégorie", S_HEAD_W), P("Recommandation", S_HEAD_W), P("Grade", S_HEAD_W_C)]]
    for ref, txt, grade in rows:
        data.append([P(ref, S_CELL_B), P(txt, S_CELL), chip(grade, width=15 * mm)])
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

RCW = [32 * mm, CW_FULL - 32 * mm - 15 * mm, 15 * mm]

def context_note_local(txt):
    return P(f"<i>Précision du source :</i> {txt}", S_NOTE)

def practical_block(title, bullets):
    story = [P(f"<b>{title}</b>", S_BODY_SM)]
    for b in bullets:
        story.append(P(f"• {b}", S_BODY_SM))
    return story

def legend_flowable():
    chip_w = 15 * mm
    content_w = CW_FULL
    row = Table([[chip("A", width=chip_w - 2 * mm), chip("B", width=chip_w - 2 * mm),
                  chip("C", width=chip_w - 2 * mm), chip("D", width=chip_w - 2 * mm),
                  chip("AE", width=chip_w - 2 * mm),
                  P("<b>Grille EBM classique</b> — <b>A</b> : essais randomisés de forte "
                    "puissance/méta-analyses ; <b>B</b> : essais randomisés de faible "
                    "puissance/études de cohorte ; <b>C</b> : cas-témoins/études "
                    "rétrospectives ; <b>D</b> : cité par le source mais JAMAIS défini dans "
                    "son propre préambule méthodologique (incohérence du source, disclosed, "
                    "non assimilée à C) ; <b>AE</b> : accord professionnel — regroupe aussi "
                    "« consensus professionnel ». Fiche limitée à la Question 7/15.", S_BADGE_HEAD)]],
                colWidths=[chip_w] * 5 + [content_w - 5 * chip_w])
    row.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                              ("LEFTPADDING", (0, 0), (-1, -1), 1),
                              ("RIGHTPADDING", (0, 0), (-1, -1), 1),
                              ("TOPPADDING", (0, 0), (-1, -1), 0),
                              ("BOTTOMPADDING", (0, 0), (-1, -1), 0)]))
    return row

TOTAL_PAGES = {"n": 6}

def on_page(canvas, doc, page_title):
    header_band(canvas, doc, "SFAR/SOFCOT/SOFMER — RPC 2007 (Q7/15 — PÉRIMÈTRE LIMITÉ)",
                "Les blocs périmédullaires chez l'adulte",
                page_title, icon_fn=lambda c, x, y: icon_shield(c, x, y, 13 * mm), color=TEAL_DARK)
    footer_band(canvas, doc, SOURCE_TXT, f"Page {doc.page} / {TOTAL_PAGES['n']}")

# ---------------------------------------------------------------------------
def _section_preparation():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Périmètre limité — installment 3/n :</b> ce document source compte 15 « Questions » "
        "cliniques et 369 citations de grade au total. Cette fiche couvre INTÉGRALEMENT la "
        "Question 7 (blocs périmédullaires pour la césarienne). La Question 6 (travail "
        "obstétrical) est EXCLUE — superseded par une fiche séparée plus récente "
        "(HAS 2025, « Douleur de l'accouchement »). Les Questions 1-2 et 3-5 sont couvertes par "
        "des fiches séparées. Les Questions 8 à 15 (analgésie postopératoire périmédullaire "
        "générale, terrains spécifiques, échec, facteurs de risque) ne sont PAS couvertes ici — "
        "installments futurs.", S_BODY),
        bg=AMBER_LIGHT, border=AMBER))
    story.append(Spacer(1, 2.5 * mm))
    story.append(legend_flowable())
    story.append(Spacer(1, 3 * mm))
    story.append(KeepTogether([
        section_bar("Question 7 — Blocs périmédullaires pour la césarienne : préparation"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("Jeûne", "Avant une césarienne programmée, un jeûne de 6-8h concernant les solides "
         "est recommandé ; considérer la parturiente comme à risque d'inhalation du contenu "
         "gastrique du fait des modifications physiologiques de la grossesse (risque surtout "
         "présent au cours du travail).", "C"),
        ("Prévention inhalation", "L'administration systématique d'agents anti-H2 (cimétidine "
         "ou ranitidine) combinés à du citrate de sodium (forme effervescente) est recommandée "
         "avant la césarienne.", "C"),
        ("Surveillance fœtale", "En chirurgie programmée, un enregistrement du RCF est réalisé "
         "en préopératoire ; le matériel d'évaluation du RCF doit être disponible à l'arrivée "
         "en salle (avec un membre de l'équipe obstétricale pour l'interpréter), pour guider le "
         "choix de la technique anesthésique selon le délai disponible.", "C"),
        ("Surveillance maternelle", "Surveillance toutes les minutes lors de l'induction de la "
         "rachianesthésie pour césarienne, puis toutes les 2-3 minutes en phase de stabilité ; "
         "mesures plus fréquentes en cas de médicaments vasoactifs (dont ocytocine), "
         "d'hémorragie ou de tout incident (nausées, vomissements).", "D"),
        ("Décubitus", "Un décubitus latéral gauche d'au moins 10° est recommandé jusqu'à "
         "l'extraction fœtale (lève partiellement la compression aortocave, contrairement au "
         "décubitus complet).", "C"),
        ("Oxygénothérapie", "L'intérêt de l'administration d'oxygène est documenté dans les "
         "situations maternelles ou fœtales pathologiques.", "C"),
        ("Qualité du bloc", "Associer systématiquement un morphinique liposoluble à l'AL "
         "utilisé, pour améliorer la qualité de l'APM pour la césarienne.", "A"),
        ("Qualité du bloc", "Contrôler qu'un niveau adéquat d'anesthésie est atteint avant "
         "l'incision — utiliser la perte de perception du toucher léger/de la stimulation "
         "douloureuse (et non le chaud-froid ni le piquer-toucher, non adaptés) ; test "
         "prédictif fiable si le niveau atteint au moins T5.", "C"),
    ], RCW))
    return story

# ---------------------------------------------------------------------------
def _section_techniques():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Choix de la technique et des agents"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("Choix technique", "L'ALR périmédullaire doit être privilégiée chaque fois que "
         "possible pour la césarienne, tout particulièrement en situation non programmée ; "
         "seules les césariennes en extrême urgence (délai décision-extraction < 5-10 min) et "
         "les contre-indications à l'APM doivent indiquer une AG.", "C"),
        ("Rachianesthésie", "Technique de choix pour les césariennes programmées.", "C"),
        ("Rachianesthésie", "Les aiguilles pointe-crayon doivent être utilisées "
         "systématiquement en obstétrique, avec un diamètre ≤ 25G.", "A"),
        ("Rachianesthésie", "L'adjonction d'un morphinique liposoluble (fentanyl ou "
         "sufentanil) est recommandée — améliore la qualité de la rachianesthésie et permet de "
         "réduire la dose d'AL ; dose de fentanyl intrathécal ≈ 10 µg, sufentanil 2,5-5 µg.", "B"),
        ("Rachianesthésie", "Dose de bupivacaïne recommandée ≈ 10 mg pour un taux de réussite "
         "proche de 100 %.", "B"),
        ("Rachianesthésie", "La forme hyperbare est la plus couramment utilisée, mais la forme "
         "isobare donne une anesthésie similaire et constitue une alternative possible.", "C"),
        ("Rachianesthésie", "La dose de ropivacaïne intrathécale efficace doit être majorée de "
         "50 % (≈ 15 mg) par rapport à la bupivacaïne pour un effet équivalent.", "C"),
        ("Rachianesthésie", "Morphine intrathécale 100 µg pour l'analgésie postopératoire "
         "(n'améliore que partiellement la qualité peropératoire — associer un morphinique "
         "liposoluble à l'AL reste recommandé).", "C"),
        ("Péridurale", "Injection de 15-20 ml de lidocaïne 2 % adrénalinée (1:200 000) pour "
         "atteindre un niveau d'anesthésie chirurgicale en 10 minutes dans la plupart des "
         "situations, évitant le recours à une AG.", "C"),
        ("Péridurale", "Addition d'un morphinique liposoluble en bolus recommandée, surtout "
         "s'il n'a pas été utilisé pendant le travail.", "C"),
        ("Péridurale", "Une rachianesthésie supplémentaire pour renforcer une péridurale déjà "
         "en place ou insuffisante n'est pas recommandée (risque important de rachianesthésie "
         "extensive).", "C"),
        ("RPS", "La rachianesthésie-péridurale séquentielle peut être utilisée de deux façons : "
         "dose intrathécale complète avec recours possible au cathéter péridural pour une "
         "difficulté prévisible, ou petite dose intrathécale + complément péridural d'emblée "
         "(titration, effets hémodynamiques moindres — objectif prioritaire) ; fractionner la "
         "dose du cathéter péridural d'une RPS non préalablement utilisé pendant le travail.", "C"),
    ], RCW))
    story.append(Spacer(1, 2 * mm))
    story.append(KeepTogether([
        section_bar("Gestion de l'échec / des imperfections"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("Échec — rachianesthésie", "En cas d'extension insuffisante, attendre quelques "
         "minutes (Trendelenburg modéré ≤10° si solution hyperbare) ; en cas d'échec du bloc, "
         "convertir en AG sans attendre l'incision.", "C"),
        ("Échec — péridurale/RPS", "Réinjecter un AL d'action rapide (lidocaïne 2 % "
         "adrénalinée ou ropivacaïne 0,75 %) ± morphinique liposoluble ; en cas d'échec de ces "
         "compléments ou si le délai d'extraction est urgent, recourir à l'AG.", "C"),
    ], RCW))
    story.append(Spacer(1, 1.5 * mm))
    story.append(info_panel(P(
        "<b>Fig. 1 (source, transcription textuelle du diagramme) — Place de l'ALR dans la "
        "césarienne :</b><br/>"
        "<b>Non programmée</b> → (voie principale) cathéter péridural en place → souffrance "
        "fœtale aiguë : évaluer le degré d'urgence et le risque anesthésique maternel/fœtal → "
        "utilisation du cathéter (majoritaire) ou AG (minoritaire, urgence extrême) ; pas de "
        "souffrance fœtale → utilisation du cathéter. (voie minoritaire) pas de cathéter "
        "péridural → urgence immédiate → AG (majoritaire) ou rachianesthésie ± péridurale selon "
        "urgence/état fœtal (minoritaire) ; urgence différable → rachianesthésie ± péridurale "
        "selon degré d'urgence et état fœtal.<br/>"
        "<b>Programmée</b> → (voie principale) pas de contre-indication à l'ALR → césarienne "
        "techniquement simple → rachianesthésie seule ; césarienne potentiellement longue, "
        "enfant ou mère fragile, nécessité de contrôler le niveau → rachi-péri combinée (ou "
        "péridurale). (voie minoritaire) contre-indication à l'ALR → anesthésie générale.<br/>"
        "<i>NB du source : cet algorithme doit aussi prendre en compte l'organisation de la "
        "structure (locaux, astreinte ou garde sur place…) et l'expérience des intervenants ; "
        "l'épaisseur des flèches du diagramme original traduit la fréquence des différentes "
        "situations.</i>", S_BODY_SM),
        bg=GREY_LIGHT, border=GREY))
    return story

# ---------------------------------------------------------------------------
def _section_situations_analgesie_sources():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Situations obstétricales particulières"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(P(
        "<b>Repères non gradés :</b> l'ALR périmédullaire peut être contre-indiquée en cas de "
        "troubles de la coagulation induits par la pathologie obstétricale (ex. hématome "
        "rétroplacentaire) ou un traitement concomitant (ex. anticoagulant efficace) — mais "
        "l'APM garde de nombreux avantages sur l'AG et peut être réalisable devant des "
        "contre-indications classiquement relatives (analyse bénéfice/risque, à noter au "
        "dossier).", S_BODY_SM))
    story.append(Spacer(1, 1.5 * mm))
    story.append(reco_table([
        ("Prééclampsie/éclampsie", "Il est licite d'utiliser la rachianesthésie ou la RPS en "
         "cas de prééclampsie même sévère — paradoxalement, moins d'hypotension et moindre "
         "besoin en éphédrine sont rapportés chez ces patientes (pas de données sur la "
         "phényléphrine dans cette population). La péridurale reste une alternative.", "C"),
        ("Éclampsie", "L'existence d'une hypertension intracrânienne patente et/ou de signes de "
         "localisation demeure une contre-indication incontournable à l'ALR.", "AE"),
        ("Anomalies placentaires", "L'anesthésie périmédullaire est souhaitable lorsque le "
         "placenta est postérieur ou latéral, même si un saignement minime ou modéré est en "
         "cours.", "C"),
        ("Anomalies placentaires", "En cas de placenta antérieur sur utérus cicatriciel, de "
         "saignement actif en cours, ou d'imagerie évoquant un placenta accreta, l'anesthésie "
         "générale est recommandée.", "C"),
    ], RCW))
    story.append(Spacer(1, 3 * mm))
    story.append(KeepTogether([
        section_bar("Analgésie postopératoire de la césarienne sous ALR périmédullaire"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(P(
        "<b>Repères non gradés :</b> l'analgésie postopératoire après césarienne est "
        "multimodale, la voie périmédullaire en étant l'une des composantes. Chez les "
        "patientes obèses, les morphiniques (périmédullaires ou systémiques) justifient une "
        "surveillance dans une structure adaptée. La clonidine (péridurale ou intrathécale) "
        "augmente la qualité/durée de l'analgésie mais induit une sédation (action courte, 4h, "
        "par voie péridurale) — son utilisation n'est donc pas recommandée.", S_BODY_SM))
    story.append(Spacer(1, 1.5 * mm))
    story.append(reco_table([
        ("Voie périmédullaire", "Supérieure à la voie systémique pour la qualité de "
         "l'analgésie et la moindre sédation, lorsqu'elle est utilisée en monothérapie.", "A"),
        ("Sécurité", "Le risque de dépression respiratoire est documenté pour la morphine à "
         "des doses > 250 µg par voie intrathécale ou > 3 mg par voie péridurale — "
         "l'association de morphiniques par plusieurs voies impose une surveillance "
         "renforcée.", "B"),
        ("Dose péridurale", "Dose optimale de morphine péridurale en bolus : 3-3,75 mg en "
         "monothérapie (risque accru de dépression respiratoire au-delà).", "B"),
        ("Dose péridurale", "Une efficacité équivalente peut être obtenue avec 1-2 mg de "
         "morphine péridurale lorsqu'un AINS est associé par voie systémique.", "B"),
        ("Dose intrathécale", "Pas de bénéfice à utiliser une dose de morphine intrathécale "
         "supérieure à 80-100 µg sans conservateur (effets secondaires majorés au-delà).", "A"),
    ], RCW))
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("Sources et avertissement", color=GREY))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>Document source :</b> SFAR/Sofcot/Sofmer, « Les blocs périmédullaires chez "
        "l'adulte », Recommandations pour la Pratique Clinique, présentées le 24 septembre "
        "2005 (47e congrès SFAR), Annales Françaises d'Anesthésie et de Réanimation 26 "
        "(2007) 720-752.", S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>URL source :</b> https://sfar.org/les-blocs-perimedullaires-chez-ladulte/", S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>Couverture :</b> Question 7/15 uniquement (césarienne) — 31 recommandations "
        "gradées (A:4, B:5, C:20, D:1, AE:1). La Question 6 (travail obstétrical) est EXCLUE "
        "— superseded par une fiche séparée plus récente (HAS 2025). Les Questions 1-2 et 3-5 "
        "sont couvertes par des fiches séparées. Les Questions 8 à 15 ne sont pas couvertes ici "
        "— hors périmètre, installments futurs. Argumentaire scientifique détaillé (document "
        "source complet) non reproduit.", S_SOURCE))
    story.append(Spacer(1, 2 * mm))
    story.append(info_panel(P(
        "<b>Avertissement :</b> cette fiche est une synthèse indépendante et PARTIELLE "
        "(Question 7 uniquement, sur 15). Elle ne remplace pas le texte intégral — en "
        "particulier pour le travail obstétrical (voir la fiche HAS 2025 dédiée), l'analgésie "
        "postopératoire générale, ou tout terrain spécifique. Cette fiche n'est ni éditée ni "
        "validée par la SFAR.", S_BODY_SM),
        bg=GREY_LIGHT, border=GREY))
    return story

# ---------------------------------------------------------------------------
SECTIONS = [
    ("Question 7 — Césarienne : préparation", _section_preparation),
    ("Question 7 — Choix technique & échec", _section_techniques),
    ("Question 7 — Situations particulières, analgésie postop & sources", _section_situations_analgesie_sources),
]

def _make_doc(path=None):
    return SimpleDocTemplate(path or OUT, pagesize=A4,
                              leftMargin=MARGIN, rightMargin=MARGIN,
                              topMargin=32 * mm, bottomMargin=16 * mm,
                              title="Fiche SFAR 2007 - Blocs perimedullaires (Q7 - Cesarienne)",
                              author="Synthèse indépendante (source SFAR/Sofcot/Sofmer)")

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
