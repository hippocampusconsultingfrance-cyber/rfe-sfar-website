# -*- coding: utf-8 -*-
"""
Fiche de synthese - "Insuffisance d'analgesie au cours de la cesarienne sous
anesthesie perimedullaire : prevention - prise en charge immediate et
differee" - Preconisations du Club d'Anesthesie Reanimation Obstetricale
(CARO), avec le CNGOF, la SFAR, la SFMP, le CNSF, la SoFraSimS, des experts
en medecine legale, IADE, IBODE, le CIANE, l'association Cesarine et la
SFPP. Comite de pilotage : D. Benhamou, H. Keita-Meyer (auteur
correspondant), P. Deruelle, A. Evrard. Date document : 05/03/2021 (metadata
PDF). Source telechargee : sfar.org/download/preconisations-insuffisance-
danalgesie-au-cours-de-la-cesarienne-sous-anesthesie-perimedullaire-
prevention-prise-en-charge-immediate-et-differee/?wpdmdl=32629 (25 pages).

METHODOLOGIE : PAS de systeme GRADE, PAS de mention d'un processus de
cotation/vote formel (Delphi, GRADE Grid ou autre) nulle part dans le
document - a la difference de la quasi-totalite du corpus. Chaque
preconisation est simplement introduite par "Les experts suggerent que..."
ou "Les experts rappellent que...", sans tag de force individuelle imprime.
Le resume officiel indique que 10 des 24 preconisations ont ete identifiees
comme "cles" par les experts (liste separee, reproduite en synthese) - ceci
est une selection editoriale, pas un niveau de preuve ou une force de
recommandation. Aucun chip GRADE n'est donc invente ici : chaque
preconisation est presentee dans un simple tableau Ref./Preconisation, et
les 10 cles sont marquees par une puce distincte plutot qu'un grade.

COMPTAGE VERIFIE (regex sur le texte source aplati) : 24 preconisations
numerotees P1.1-P1.9, P2.1-P2.4, P3.1-P3.5, P4.1-P4.3, P5.1-P5.3 sur 5
themes, sans lacune. Une divergence source-interne notee et disclosee : P1.7
et P1.8 sont imprimees avec un texte rigoureusement identique dans le corps
du document ("qu'une analgesie peridurale imparfaite... memes criteres de
bonne pratique sont requis") - possible doublon d'impression de la source,
non resolu silencieusement.

ARGUMENTAIRE : condense au strict necessaire (regle de projet 2026-09-14) -
chaque preconisation source est suivie d'un paragraphe "Rationnel" plus ou
moins long recapitulant la litterature (avec references numerotees 1-34,
consolidees cette fois en UNE liste globale, a la difference d'autres
fiches recentes du corpus). Cette fiche NE reproduit PAS ces rationnels en
extenso : seules les precisions posologiques/pratiques qui changent
reellement la conduite a tenir sont conservees (doses de bupivacaine,
sufentanil, alfentanil/remifentanil, niveaux sensitifs T6/T3). Se referer au
texte integral pour le detail des 34 references bibliographiques.

COUVERTURE : integralite des 24 preconisations (texte complet), du tableau
"Facteurs de risque d'echec des differentes techniques d'APM", de l'annexe
"Aide a la decision" (algorithme visuel transcrit en tableau depuis un rendu
a 200dpi - aucune couche texte fiable pour ce schema dans le PDF source) et
de la synthese des 10 preconisations cles.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from style import *
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.units import mm

OUT = "/home/user/rfe-sfar-website/output/Fiche_CARO_Insuffisance_Analgesie_Cesarienne_2021.pdf"

SOURCE_TXT = ("Source : « Insuffisance d'analgésie au cours de la césarienne sous "
              "anesthésie périmédullaire : prévention - prise en charge immédiate "
              "et différée » — CARO/CNGOF/SFAR/SFMP/CNSF, Préconisations 2021. "
              "Fiche de synthèse non officielle : se référer au texte intégral.")

def P(txt, style=S_CELL):
    return Paragraph(txt, style)

def plain_table(rows, col_widths, key_refs=()):
    """rows: (ref, text). key_refs: set of ref strings to mark as 'clé'."""
    data = [[P("Réf.", S_HEAD_W_C), P("Préconisation", S_HEAD_W)]]
    for ref, txt in rows:
        label = ref + (" ★" if ref in key_refs else "")
        data.append([P(label, S_CELL_B), P(txt, S_CELL)])
    t = Table(data, colWidths=col_widths, repeatRows=1)
    style_cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), NAVY), ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTNAME", (0, 0), (-1, 0), FONT_BOLD), ("FONTSIZE", (0, 0), (-1, 0), 8),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("ALIGN", (0, 0), (0, -1), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 0.5, GREY_LIGHT),
        ("TOPPADDING", (0, 0), (-1, -1), 3.4), ("BOTTOMPADDING", (0, 0), (-1, -1), 3.4),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            style_cmds.append(("BACKGROUND", (0, i), (-1, i), BG_PANEL))
    t.setStyle(TableStyle(style_cmds))
    return t

def simple_table(header, rows, col_widths):
    data = [[P(h, S_HEAD_W) for h in header]]
    for r in rows:
        data.append([P(c, S_CELL) for c in r])
    t = Table(data, colWidths=col_widths, repeatRows=1)
    st = [
        ("BACKGROUND", (0, 0), (-1, 0), TEAL_DARK), ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTNAME", (0, 0), (-1, 0), FONT_BOLD), ("FONTSIZE", (0, 0), (-1, 0), 8),
        ("GRID", (0, 0), (-1, -1), 0.5, GREY_LIGHT), ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 3.4), ("BOTTOMPADDING", (0, 0), (-1, -1), 3.4),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            st.append(("BACKGROUND", (0, i), (-1, i), BG_PANEL))
    t.setStyle(TableStyle(st))
    return t

def bullets(items, style=S_CELL):
    html = "&bull; " + "<br/>&bull; ".join(items)
    return P(html, style)

RCW = [15 * mm, PAGE_W - 2 * MARGIN - 15 * mm]

TOTAL_PAGES = {"n": 4}

def on_page(canvas, doc, page_title):
    header_band(canvas, doc, "CARO / CNGOF / SFAR — PRÉCONISATIONS 2021 — FICHE DE SYNTHÈSE",
                "Insuffisance d'analgésie — césarienne sous APM",
                page_title, icon_fn=lambda c, x, y: icon_drop(c, x, y, 13 * mm), color=NAVY)
    footer_band(canvas, doc, SOURCE_TXT, f"Page {doc.page} / {TOTAL_PAGES['n']}")

KEY_REFS = {"P1.1", "P1.2", "P1.7", "P1.9", "P1.3", "P2.1", "P3.2", "P3.1", "P3.4", "P4.2", "P2.4"}

# ---------------------------------------------------------------------------
def _section_intro():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Champ :</b> prévention, reconnaissance et prise en charge de "
        "l'insuffisance et de l'échec d'analgésie au cours de la césarienne "
        "sous anesthésie périmédullaire (APM) — Club d'Anesthésie "
        "Réanimation Obstétricale (CARO), avec le CNGOF, la SFAR, la SFMP, "
        "le CNSF, la SoFraSimS, des experts médecine légale, IADE, IBODE, "
        "le CIANE, l'association Césarine et la SFPP. Fréquence rapportée "
        "de l'insuffisance d'analgésie : 0,5-17 % pour la rachianesthésie, "
        "1,7-20 % pour l'extension d'analgésie péridurale. 5 thèmes : (1) "
        "évaluation du bloc avant incision, (2) délai décision-naissance, "
        "(3) reconnaître et gérer la douleur avant/après incision, (4) "
        "prévention et gestion de l'état de stress post-traumatique (ESPT), "
        "(5) aspects médico-légaux.", S_BODY), bg=BG_PANEL, border=TEAL))
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Méthodologie :</b> ce document ne comporte <b>aucun système "
        "GRADE</b> et ne décrit <b>aucun processus de cotation/vote "
        "formel</b> — chaque préconisation est introduite par « Les "
        "experts suggèrent que… » ou « Les experts rappellent que… », sans "
        "tag de force individuelle imprimé. <b>24 préconisations</b> au "
        "total sur les 5 thèmes ; parmi elles, <b>10 ont été identifiées "
        "comme « clés »</b> par les experts (marquées ★ dans les tableaux "
        "ci-après) — sélection éditoriale, pas un niveau de preuve.",
        S_BODY_SM), bg=AMBER_LIGHT, border=AMBER))
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Disclosure :</b> P1.7 et P1.8 sont imprimées avec un texte "
        "rigoureusement identique dans le corps du document source "
        "(« qu'une analgésie péridurale imparfaite… mêmes critères de "
        "bonne pratique sont requis ») — possible doublon d'impression de "
        "la source, reproduit tel quel plutôt que silencieusement fusionné "
        "ou supprimé. Par ailleurs, la fréquence de l'insuffisance "
        "d'analgésie est chiffrée deux fois différemment dans la source, "
        "sans réconciliation : 0,5-17 % (RA)/1,7-20 % (extension d'APD) "
        "dans le résumé/l'introduction, contre « 5 à 10 % des cas » dans "
        "l'encart « Informer » du schéma décisionnel (Annexe) — les deux "
        "chiffrages sont reproduits ici tels quels.", S_BODY_SM),
        bg=GREY_LIGHT, border=GREY))
    return story

def _section_synthese():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(section_bar("Les 10 préconisations clés (synthèse officielle)"))
    story.append(Spacer(1, 1.5 * mm))
    story.append(bullets([
        "L'insuffisance et l'échec d'analgésie sont définis comme toute "
        "anesthésie périmédullaire conduisant à un complément souhaité par "
        "la patiente.",
        "Le confort exprimé par la patiente est tout aussi important que "
        "l'évaluation du niveau d'anesthésie ; un inconfort majeur doit "
        "être pris en compte.",
        "Une analgésie péridurale imparfaite pendant le travail expose au "
        "risque d'échec de conversion pour la césarienne en cours de "
        "travail ; l'échec peut aussi survenir lors d'une césarienne "
        "programmée sous rachianesthésie (mêmes critères de bonne "
        "pratique).",
        "L'évaluation du niveau sensitif avant l'incision repose sur le "
        "toucher léger ou le froid : niveau sensitif supérieur bilatéral "
        "et symétrique en T6 au toucher ± T3 au froid requis (T6 = pointe "
        "xiphoïde, T4 = ligne mamelonnaire).",
        "En cas de suspicion d'acidose fœtale, l'obstétricien décide du "
        "degré d'urgence et communique de manière intelligible (ex. code "
        "couleur validé en équipe).",
        "Une anesthésie générale doit être réalisée en présence d'une "
        "insuffisance d'anesthésie constatée juste avant ou dès l'incision "
        "pour césarienne code rouge.",
        "Une pause opératoire doit être faite en cas de douleur "
        "peropératoire afin d'évaluer et traiter la douleur de manière "
        "adaptée au contexte.",
        "Une anesthésie générale doit être réalisée en cas d'échec de la "
        "gestion médicamenteuse de la douleur, même avant clampage du "
        "cordon.",
        "L'insuffisance d'analgésie doit être tracée, l'anesthésie "
        "renforcée, la naissance accompagnée, puis l'expérience "
        "douloureuse débriefée avec l'équipe, en particulier les "
        "soignants impliqués dans la prise en charge.",
        "Une évaluation des pratiques doit être réalisée (taux et "
        "indications des césariennes en extrême urgence, taux de "
        "conversion en AG suite à un échec d'APM).",
    ]))
    return story

def _section_intro_synthese():
    story = _section_intro()
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_synthese())
    return story

# ---------------------------------------------------------------------------
def _section_theme1():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Thème 1 — Évaluation du bloc avant incision"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(plain_table([
        ("P1.1", "L'insuffisance et l'échec d'analgésie sont définis comme "
         "toute anesthésie périmédullaire conduisant à un complément "
         "nécessaire par la patiente."),
        ("P1.2", "Le confort exprimé par la patiente est tout aussi "
         "important que l'évaluation du niveau d'anesthésie. L'existence "
         "d'un inconfort majeur doit être pris en compte."),
        ("P1.3", "L'évaluation de l'adéquation du niveau sensitif repose "
         "sur la sensation de toucher ± de froid. Un niveau sensitif "
         "supérieur bilatéral et symétrique en T6 au toucher ± en T3 au "
         "froid est requis (T6 = pointe xiphoïde, T4 = ligne mamelonnaire)."),
        ("P1.4", "Le test de pincement cutané par l'obstétricien doit être "
         "systématiquement réalisé, même en urgence, au niveau de la zone "
         "d'incision, toujours au plus haut, en limite du champ opératoire "
         "(ombilic)."),
        ("P1.5", "Pour la rachianesthésie (RA), une dose de bupivacaïne "
         "hyperbare (HB) supérieure à 10 mg limiterait le risque d'échec "
         "— dose à adapter aux tailles extrêmes et à la présence d'un "
         "syndrome de compression cave."),
        ("P1.6", "La rachianesthésie-péridurale combinée (RPC) peut "
         "limiter le risque d'échec par la présence du cathéter péridural "
         "permettant l'injection d'un complément anesthésique."),
        ("P1.7", "Une analgésie péridurale imparfaite pendant le travail "
         "obstétrical expose au risque d'échec de conversion de la "
         "péridurale analgésique en péridurale anesthésique pour la "
         "césarienne en cours de travail."),
        ("P1.8", "Une analgésie péridurale imparfaite pendant le travail "
         "obstétrical expose au risque d'échec de conversion de la "
         "péridurale analgésique en péridurale anesthésique pour la "
         "césarienne en cours de travail. <i>(texte identique à P1.7 dans "
         "la source — voir disclosure page 1.)</i>"),
        ("P1.9", "L'échec peut également survenir lors d'une césarienne "
         "programmée avec une rachianesthésie et les mêmes critères de "
         "bonne pratique sont requis."),
    ], RCW, KEY_REFS))
    story.append(Spacer(1, 1.8 * mm))
    story.append(P(
        "<b>Précisions :</b> dose de bupivacaïne HB à minorer/majorer de "
        "± 1 mg si taille &lt;155 cm ou &gt;170 cm ; adjonction de "
        "sufentanil (2,5-5 µg) pour optimiser la qualité de l'anesthésie "
        "et allonger la durée d'action, sans effet délétère néonatal "
        "rapporté. RPC : bupivacaïne HB 5-8 mg intrathécale + morphinique "
        "liposoluble et morphine, cathéter péridural ajusté secondairement "
        "à la lidocaïne 20 mg/mL adrénalinée ou ropivacaïne 5-7,5 mg/mL "
        "après dose test.", S_BODY_SM))
    story.append(Spacer(1, 1.8 * mm))
    story.append(P("<b>Tableau — Facteurs de risque d'échec des "
                    "différentes techniques d'APM</b> (reproduit "
                    "verbatim)", S_CELL_B))
    story.append(Spacer(1, 1 * mm))
    story.append(simple_table(
        ["Type d'APM", "Facteurs de risque d'échec"],
        [
            ["Rachianesthésie",
             "Ponction effectuée trop basse (L5S1) ; dose insuffisante "
             "et/ou perte d'une partie de la solution ; ponction « à "
             "cheval » (orifice de l'aiguille entre dure-mère et "
             "arachnoïde) ; antécédent de chirurgie du rachis."],
            ["Extension péridurale",
             "Nombre de bolus administrés en péridurale pendant le "
             "travail ; scores de douleur élevés (EVA ≥ 4) dans les 2 h "
             "précédant la césarienne ; degré d'urgence de la césarienne ; "
             "parturiente de grande taille. <i>FDR controversés dans la "
             "littérature :</i> dilatation cervicale lors de la "
             "césarienne, IMC maternel, APD plutôt que RPC initiale, "
             "entretien par perfusion continue plutôt que PCEA/PIEB, "
             "durée du travail et dose totale de mélange analgésique "
             "reçue."],
        ], [45 * mm, PAGE_W - 2 * MARGIN - 45 * mm]))
    return story

def _section_theme2():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Thème 2 — Délai décision-naissance & communication"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(plain_table([
        ("P2.1", "En cas de suspicion d'acidose fœtale, l'obstétricien "
         "décide du degré d'urgence de la césarienne et communique de "
         "manière intelligible avec les autres acteurs, par exemple à "
         "l'aide d'un système de communication simplifié et validé en "
         "équipe (type code couleur)."),
        ("P2.2", "Dans chaque maternité, les procédures de transfert, "
         "d'installation des patientes et de modalité d'anesthésie en "
         "salle de césarienne doivent être optimisées pour minimiser le "
         "temps décision-incision."),
        ("P2.3", "La possibilité de réaliser un enregistrement du rythme "
         "cardiaque fœtal (RCF) à l'arrivée en salle de césarienne est une "
         "préconisation forte du CNGOF et du CNEMM (Comité National "
         "d'Experts sur les Morts Maternelles)."),
        ("P2.4", "Une évaluation des pratiques pourrait être réalisée avec "
         "comme indicateurs le taux et les indications des césariennes en "
         "extrême urgence, ainsi que le taux de conversion en anesthésie "
         "générale suite à un échec d'APM."),
    ], RCW, KEY_REFS))
    story.append(Spacer(1, 1.8 * mm))
    story.append(P(
        "<b>Précisions :</b> le risque d'insuffisance d'analgésie lors de "
        "conversion des péridurales pour césarienne en urgence est "
        "rapporté 40 fois plus fréquent dans les césariennes code rouge — "
        "contrôler le RCF à l'arrivée au bloc peut faire reconsidérer le "
        "délai décision-incision. <i>(Disclosure : le résumé/la méthode "
        "de la source nomme ce thème « délai décision-extraction », le "
        "titre de section retenu ici — « délai décision-naissance » — "
        "est celui imprimé en tête de la section correspondante.)</i>",
        S_BODY_SM))
    return story

def _section_intro_th1_th2():
    story = _section_intro_synthese()
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_theme1())
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_theme2())
    return story

# ---------------------------------------------------------------------------
def _section_theme3():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Thème 3 — Reconnaître et gérer la douleur avant/après incision"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(plain_table([
        ("P3.1", "Réaliser une pause opératoire en cas de douleur "
         "peropératoire afin d'évaluer et traiter la douleur de manière "
         "adaptée au contexte."),
        ("P3.2", "Réaliser une anesthésie générale en cas d'échec constaté "
         "d'une APM juste avant ou dès l'incision pour césarienne code "
         "rouge."),
        ("P3.3", "Administrer par voie intraveineuse de faibles doses "
         "d'un opioïde de courte durée d'action (alfentanil ou "
         "rémifentanil) ou des doses infra-anesthésiques de propofol ou "
         "kétamine en cas d'insuffisance d'analgésie constatée en cours "
         "d'intervention."),
        ("P3.4", "Réaliser une anesthésie générale en cas d'échec de la "
         "gestion médicamenteuse de la douleur, même avant le clampage du "
         "cordon."),
        ("P3.5", "L'efficacité de toute action de complément d'anesthésie "
         "doit être réévaluée."),
    ], RCW, KEY_REFS))
    story.append(Spacer(1, 1.8 * mm))
    story.append(P(
        "<b>Précisions :</b> le délai décision-extraction (15-30 min) "
        "restreint le choix technique lors d'une césarienne code rouge — "
        "l'AG s'impose en cas de douleur dès l'incision. Complément IV : "
        "privilégier les opiacés en 1<sup>re</sup> intention (préserver la "
        "ventilation spontanée, associer une oxygénation) ; hypnotiques "
        "envisageables (propofol, kétamine) ; opioïdes/hypnotiques avant "
        "clampage du cordon peuvent dégrader transitoirement le score "
        "Apgar — à signaler au néonatologue.", S_BODY_SM))
    return story

def _section_theme4():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Thème 4 — Prévention et gestion de l'état de stress "
                    "post-traumatique (ESPT)"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(plain_table([
        ("P4.1", "Informer les femmes, en préparation à l'accouchement et "
         "dans les feuillets d'information, de l'éventualité d'une "
         "analgésie insuffisante et des solutions possibles, y compris en "
         "cas de césarienne."),
        ("P4.2", "Tracer l'insuffisance d'analgésie en cours de "
         "césarienne, renforcer l'anesthésie locorégionale et/ou "
         "générale, accompagner la naissance puis débriefer l'expérience "
         "douloureuse avec l'équipe, en particulier les soignants "
         "impliqués."),
        ("P4.3", "Identifier la sidération et réaliser le soin psychique "
         "d'urgence (defusing) en postpartum ; à distance, diagnostiquer "
         "l'ESPT en explorant le bien-être maternel et la relation "
         "mère-enfant, puis confier la patiente à des spécialistes de "
         "l'ESPT pour une psychothérapie adaptée."),
    ], RCW, KEY_REFS))
    story.append(Spacer(1, 1.8 * mm))
    story.append(P(
        "<b>Précisions :</b> l'état de sidération se manifeste par un "
        "mutisme ou un discours pauvre, un comportement maternel "
        "« opératoire »/automatique face au bébé, une absence d'émotions "
        "positives ou négatives — le témoignage du conjoint peut aider à "
        "le détecter. Le defusing (« déchocage psychologique ») vise à "
        "éviter un nouveau traumatisme et à soutenir activement les "
        "mécanismes de défense de la patiente.", S_BODY_SM))
    return story

def _section_theme5():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Thème 5 — Aspects médico-légaux"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(plain_table([
        ("P5.1", "Une information préanesthésique adaptée (art. D. "
         "6124-91 et D. 6124-92 du Code de la Santé Publique) est le "
         "fondement d'un consentement libre et éclairé, mais doit aussi "
         "en situer les limites, imperfections ou échecs."),
        ("P5.2", "L'article L 1110-5-3 du Code de la Santé Publique "
         "dispose que « toute personne a le droit de recevoir des "
         "traitements et des soins visant à soulager sa souffrance […] "
         "celle-ci devant être, en toutes circonstances, prévenue, prise "
         "en compte, évaluée et traitée »."),
        ("P5.3", "En termes de préjudice corporel, les dommages les plus "
         "fréquemment observés incluent la prolongation et la majoration "
         "de l'intensité des gênes temporaires partielles, une "
         "chronicisation des douleurs et l'apparition de troubles "
         "neuropsychologiques pouvant témoigner d'un syndrome de stress "
         "post-traumatique."),
    ], RCW, KEY_REFS))
    return story

def _section_annexe():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Annexe — Aide à la décision", color=GREY),
        Spacer(1, 1 * mm),
        P("<i>Reproduit en tableau depuis un rendu visuel à 200dpi de la "
          "source page 25 — aucune couche texte fiable pour ce schéma "
          "dans le PDF source.</i>", S_NOTE),
        Spacer(1, 1.5 * mm),
        simple_table(
            ["Étape", "Contenu"],
            [
                ["1. Informer / Surveiller (en amont)",
                 "<b>Informer :</b> techniques anesthésiques en cas de "
                 "césarienne urgente/programmée ; possibilité d'échec des "
                 "techniques d'APM ; stratégies proposées en cas d'échec ; "
                 "fréquence 5-10 % des cas. <b>Surveiller :</b> qualité et "
                 "symétrie de l'APD en cours de travail ; dose suffisante "
                 "réinjectée en cas de conversion APD (15-20 mL de "
                 "lidocaïne 2 % adrénalinée) ; niveaux sensitifs "
                 "symétriques en T6 au toucher/T3 au froid (mamelon) avant "
                 "incision ; analgésie cutanée au test à la pince."],
                ["2. Insuffisance au test à la pince / à l'incision",
                 "Pause opératoire — évaluation MAR/obstétricien du délai "
                 "d'extraction attendu, puis conduite selon le type de "
                 "césarienne (programmée/urgence différable, urgence, "
                 "urgence extrême — réaliser selon le contexte : critères "
                 "d'intubation difficile, repères anatomiques difficiles, "
                 "antécédent de chirurgie rachidienne)."],
                ["3a. Programmée/urgence différable — échec complet à "
                 "30 min (aucun niveau)",
                 "Privilégier la PRC, sinon 2<sup>e</sup> rachianesthésie "
                 "(même dose) ou AG."],
                ["3b. Programmée/urgence différable — bloc partiel à "
                 "30 min",
                 "Privilégier la PRC avec bupivacaïne dose minorée "
                 "(5 mg) puis anesthésique local en APD ; ou APD ; ou "
                 "rachi (bupivacaïne HB dose minorée 7-8 mg) ; ou AG en "
                 "induction séquence rapide."],
                ["3c. Urgence", "Communication avec l'obstétricien. APD : "
                 "poursuite de l'extension. AG : induction séquence "
                 "rapide."],
                ["3d. Urgence extrême", "AG d'emblée : informer la "
                 "patiente, préoxygénation, induction séquence rapide."],
                ["4. Insuffisance d'analgésie pendant la césarienne",
                 "Pause opératoire — évaluation de l'intensité de la "
                 "douleur selon le contexte et la sévérité."],
                ["5a. Complément intraveineux",
                 "Opioïdes : alfentanil 5-10 µg/kg, ou rémifentanil bolus "
                 "0,3 µg/kg en 1 min puis 0,1 µg/kg/min. Hypnotiques à "
                 "dose infra-anesthésique : kétamine, propofol. Prévenir "
                 "le pédiatre."],
                ["5b. Anesthésie générale", "En induction séquence "
                 "rapide (option parallèle au complément intraveineux "
                 "selon le contexte)."],
                ["6. Après coup",
                 "Savoir accepter l'échec d'ALR menant à l'AG ; tracer "
                 "l'insuffisance d'analgésie ; débriefer avec l'équipe ; "
                 "visite postopératoire ; identifier l'état de stress "
                 "post-traumatique."],
            ], [50 * mm, PAGE_W - 2 * MARGIN - 50 * mm]),
    ]))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P("<i>Abréviations de la source :</i> APM = analgésie "
                    "périmédullaire ; APD = analgésie péridurale ; RA = "
                    "rachianesthésie ; AG = anesthésie générale ; PRC = "
                    "péri-rachi combinée (annexe) ; KT = cathéter ; VS = "
                    "ventilation spontanée. <i>Incohérence de la source :</i> "
                    "le corps du texte (P1.6) emploie l'acronyme RPC pour "
                    "la même technique.", S_NOTE))
    return story

def _section_sources():
    story = []
    story.append(section_bar("Sources et traçabilité", color=GREY))
    story.append(Spacer(1, 2 * mm))
    story.append(P("<b>Déclaration d'intérêts :</b> non précisée dans le "
                    "document source (aucune section dédiée identifiée).",
                    S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>Document source :</b> « Insuffisance d'analgésie au cours de "
        "la césarienne sous anesthésie périmédullaire : prévention - "
        "prise en charge immédiate et différée » — Préconisations du "
        "Club d'Anesthésie Réanimation Obstétricale (CARO), avec le "
        "CNGOF, la SFAR, la SFMP, le CNSF, la SoFraSimS, des experts "
        "médecine légale, IADE, IBODE, le CIANE, l'association Césarine "
        "et la SFPP. Comité de pilotage : D. Benhamou, H. Keita-Meyer "
        "(auteur correspondant), P. Deruelle, A. Evrard.", S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P("<b>Version :</b> 2021.", S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P("<b>Méthodologie :</b> aucun système GRADE, aucun "
                    "processus de cotation/vote formel décrit — voir "
                    "détail en page 1.", S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>URL source :</b> https://sfar.org/download/preconisations-"
        "insuffisance-danalgesie-au-cours-de-la-cesarienne-sous-"
        "anesthesie-perimedullaire-prevention-prise-en-charge-immediate-"
        "et-differee/?wpdmdl=32629", S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P("<b>Couverture :</b> intégralité des 24 préconisations "
                    "(5 thèmes), de la synthèse des 10 préconisations "
                    "clés, du tableau des facteurs de risque d'échec des "
                    "techniques d'APM et de l'annexe « Aide à la décision "
                    "». Bibliographie source : 34 références consolidées "
                    "en une liste unique — non reproduite ici, "
                    "l'argumentaire de chaque préconisation étant "
                    "volontairement condensé à ses éléments actionnables "
                    "(se référer au texte intégral pour le détail des "
                    "études).", S_SOURCE))
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Avertissement — document de 2021 :</b> ce document est une "
        "fiche de synthèse indépendante, produite pour un usage "
        "d'aide-mémoire. Elle reprend l'intégralité des 24 préconisations "
        "et de l'annexe décisionnelle, mais ne remplace pas le texte "
        "intégral (rationnels complets, références bibliographiques) et "
        "n'est ni éditée ni validée par le CARO, le CNGOF, la SFAR ou "
        "leurs partenaires. En cas de doute, se référer au texte intégral "
        "et/ou à un avis spécialisé.", S_BODY_SM), bg=GREY_LIGHT, border=GREY))
    return story

def _section_th3_th4_th5_annexe_sources():
    story = _section_theme3()
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_theme4())
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_theme5())
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_annexe())
    story.append(Spacer(1, 4 * mm))
    story.extend(_section_sources())
    return story

SECTIONS = [
    ("Méthodologie, synthèse & Thèmes 1-2 (bloc, délai décision-naissance)", _section_intro_th1_th2),
    ("Thèmes 3-5 (douleur, ESPT, médico-légal), annexe décisionnelle & sources", _section_th3_th4_th5_annexe_sources),
]

def _make_doc(path=None):
    return SimpleDocTemplate(path or OUT, pagesize=A4,
                              leftMargin=MARGIN, rightMargin=MARGIN,
                              topMargin=32 * mm, bottomMargin=16 * mm,
                              title="Fiche CARO 2021 - Insuffisance analgesie cesarienne APM",
                              author="Synthèse indépendante (source CARO/CNGOF/SFAR)")

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
    # import) - use PyMuPDF (fitz) instead. Also: this MUST write to a fresh
    # tempfile, never to OUT - reusing OUT for both the throwaway measurement
    # build and the final build was found to silently corrupt page 1's
    # header_band in the final PDF (see CLAUDE.md build pipeline step 5).
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

    final_story = _build_upto(fns)

    doc = _make_doc()
    page_counter = {"n": 0}

    def _on_first(canvas, doc_):
        page_counter["n"] = 1
        on_page(canvas, doc_, page_titles[0])

    def _on_later(canvas, doc_):
        page_counter["n"] += 1
        idx = min(page_counter["n"] - 1, len(page_titles) - 1)
        on_page(canvas, doc_, page_titles[idx])

    doc.build(final_story, onFirstPage=_on_first, onLaterPages=_on_later)
    print(f"OK -> {OUT} ({total_pages} pages)")

if __name__ == "__main__":
    build()
