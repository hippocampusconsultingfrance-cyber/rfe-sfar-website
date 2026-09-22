# -*- coding: utf-8 -*-
"""
Fiche de synthese - "Gestion perioperatoire des traitements chroniques et
dispositifs medicaux. Pathologies cardiovasculaires" - Recommandations
Formalisees d'Experts (RFE), SFAR, 2009 (Ann Fr Anesth Reanim 28 (2009)
1037-1045). Telechargee depuis sfar.org (meme fichier PDF fusionne que
plusieurs autres modules de ce referentiel).

PERIMETRE VOLONTAIREMENT LIMITE (meme pattern que transfusion_gr_anesth_2014,
sepsis, anaphylaxie de ce corpus) : le PDF source telecharge (36 pages) est en
realite un document COMPOSITE fusionnant plusieurs articles AFAR distincts
publies entre 2009 et 2011, correspondant aux 5 "modules" annonces par le
referentiel (Préambule, § 4 CHAMP D'APPLICATION) : 1. Pathologies
cardiovasculaires (pages 3-11 du PDF, ce que couvre cette fiche) ; 2. Douleur
chronique, toxicomanie (pages 12-21 environ) ; 3. Pathologies infectieuses /
immunosuppresseurs (pages 22-31 environ) ; et un dernier module public. en
2011 (pages 32-36, Ann Fr Anesth Reanim 30 (2011) 191-200, module non
identifie precisement sans lecture dediee - vraisemblablement pathologies
neurologiques/psychiatriques et/ou endocriniennes, les 2 modules restants
annonces par le Preambule). CETTE FICHE COUVRE UNIQUEMENT LE MODULE 1
(Pathologies cardiovasculaires, pages 3-11 du PDF fusionne) - le module le
plus directement transversal a toute anesthesie programmee. Les 3 autres
modules NE SONT PAS traites ici - hors perimetre de cette fiche, explicitement
disclosed, a construire separement dans une session future (chacun necessite
sa propre lecture/audit dediee pour identifier precisement ses limites de
pages et son contenu, le fichier PDF ne les separant pas explicitement).

Le Preambule (module 1 de tous, non recommandations en soi) precise aussi que
les traitements ANTITHROMBOTIQUES (antiagregants plaquettaires, AVK) sont
EXPLICITEMENT EXCLUS de tout ce referentiel par le comite d'organisation
lui-meme, car deja couverts par d'autres textes SFAR/HAS distincts (deja
git-traques dans ce corpus sous forme d'autres fiches, ex. aap_programmee) -
aucun risque de collision/chevauchement avec ces documents.

METHODOLOGIE : grille ANAES avril 2004, A/B/C/D - A = preuve scientifique
etablie (essais randomises de forte puissance/meta-analyses), B = presomption
scientifique (essais randomises de faible puissance/etudes de cohorte), C =
niveau de preuve faible (cas-temoins/etudes retrospectives), D = accord
professionnel (absence d'etude). Particularite disclosed par le Preambule
lui-meme : les recommandations de grade D jugees les plus importantes/
cruciales par les experts ont ete "renforcees" par une methode Delphi a deux
tours, aboutissant dans la grande majorite des cas a un "accord fort" - c'est
la SEULE forme de grade D effectivement imprimee dans le module 1 (aucune
occurrence de "accord professionnel" nu, seulement "accord fort" a chaque
fois) - chip local "AF" (accord fort) reutilise pour ce role, distinct du
chip "AE" (avis d'experts/absence de donnees) utilise ailleurs dans ce corpus
pour un sens legerement different (balance benefice/risque indeterminee vs.
ici accord de consensus explicite renforce par methode Delphi).

DECOMPTE (Module 1 - Pathologies cardiovasculaires uniquement) : 15
recommandations gradees (A:0, B:3, C:3, AF:9 - aucune recommandation d'action
n'est directement citee grade A dans ce module ; les rares citations de
grade A du texte source portent sur des observations descriptives, reportees
en note de contexte, non sur une ligne d'action) + 1 recommandation
explicitement NON GRADEE par la source elle-meme (antiarythmiques classe I,
interruption 24h avant chirurgie programmee - seul enonce prescriptif de
toute la section sans grade attache, regle 4 : aucun grade invente pour
cette ligne) = 16 items sur les 9 classes therapeutiques cardiovasculaires
couvertes (betabloquants, inhibiteurs calciques, diuretiques, activateurs
des canaux potassiques [nicorandil], inhibiteurs du SRAA [IEC/sartans],
derives nitres, statines, antiarythmiques classe I, antiarythmiques classe
III [amiodarone, sotalol]) + 1 section distincte non gradee (stimulateurs
cardiaques/defibrillateurs automatiques implantables - DCI) traitee en
reference pratique condensee, la source n'y attachant AUCUN grade A/B/C/D a
aucun moment (disclosed comme telle, deux points explicitement signales par
la source elle-meme comme ne faisant PAS l'objet d'un consensus : la
reprogrammation preoperatoire en mode asynchrone chez le patient
stimulo-dependant, et la deprogrammation de la fonction d'asservissement -
ni l'un ni l'autre n'est donc affiche avec un chip de grade invente).

DISCLOSURE - doublons de citation de grade au sein d'une meme classe
therapeutique : plusieurs sections (betabloquants, statines) enoncent la
meme recommandation d'action ("ne pas interrompre") DEUX FOIS dans des
sous-sections differentes du texte source, chacune avec un grade different
attache (ex. betabloquants : grade C dans la sous-section "quel est le
risque d'evenement", puis "accord fort" dans la sous-section "proposer une
strategie d'arret/de maintien/de substitution"). Cette fiche ne fusionne
JAMAIS ces deux citations en un chip composite (regle 4) : le grade retenu
pour la ligne de recommandation d'action est celui de la sous-section
"strategie" (la plus specifiquement prescriptive) ; la citation de grade de
la sous-section "risque d'evenement" (le plus souvent une observation de
tolerance/effet rebond, non une action) est reportee separement dans une
note de contexte italique, jamais supprimee.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from style import *
GRADE_COLORS["A"] = (GREEN, WHITE)
GRADE_COLORS["B"] = (TEAL, WHITE)
GRADE_COLORS["C"] = (AMBER, WHITE)
GRADE_COLORS["AF"] = (GREY, WHITE)
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.units import mm

OUT = "/home/user/rfe-sfar-website/output/Fiche_Gestion_Traitements_Chroniques_Cardio_2009.pdf"

SOURCE_TXT = ("Source : SFAR, « Gestion périopératoire des traitements chroniques et dispositifs "
              "médicaux — Pathologies cardiovasculaires », RFE, Ann Fr Anesth Réanim 28 (2009) "
              "1037-1045 — Module 1/4 uniquement. Fiche de synthèse non officielle : se référer au texte intégral.")

def P(txt, style=S_CELL):
    return Paragraph(txt, style)

def chip(label, **kw):
    return grade_chip(label, **kw)

CW_FULL = PAGE_W - 2 * MARGIN

def reco_table(rows, col_widths):
    """rows: (ref, text, grade_label)."""
    data = [[P("Classe", S_HEAD_W), P("Recommandation", S_HEAD_W), P("Grade", S_HEAD_W_C)]]
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

RCW = [26 * mm, CW_FULL - 26 * mm - 15 * mm, 15 * mm]

def context_note(txt):
    return P(f"<i>Précision du source :</i> {txt}", S_NOTE)

def ungraded_note(txt):
    return info_panel(P(
        f"<b>Non gradée par la source :</b> {txt}", S_BODY_SM), bg=GREY_LIGHT, border=GREY)

def no_consensus_note(txt):
    return info_panel(P(
        f"<b>Absence de consensus (signalée par la source elle-même) :</b> {txt}", S_BODY_SM),
        bg=GREY_LIGHT, border=GREY)

def legend_flowable():
    chip_w = 16 * mm
    content_w = CW_FULL
    row = Table([[chip("A", width=chip_w - 2 * mm), chip("B", width=chip_w - 2 * mm),
                  chip("C", width=chip_w - 2 * mm), chip("AF", width=chip_w - 2 * mm),
                  P("<b>Grille ANAES 2004</b> — <b>A</b> : preuve scientifique établie ; "
                    "<b>B</b> : présomption scientifique ; <b>C</b> : faible niveau de preuve ; "
                    "<b>AF</b> : accord fort (grade D — accord professionnel — renforcé par "
                    "méthode Delphi à 2 tours, seule forme de grade D imprimée dans ce module). "
                    "Fiche limitée au Module 1/4 du référentiel (pathologies cardiovasculaires) — "
                    "voir encadré de périmètre ci-dessous.", S_BADGE_HEAD)]],
                colWidths=[chip_w] * 4 + [content_w - 4 * chip_w])
    row.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                              ("LEFTPADDING", (0, 0), (-1, -1), 1),
                              ("RIGHTPADDING", (0, 0), (-1, -1), 1),
                              ("TOPPADDING", (0, 0), (-1, -1), 0),
                              ("BOTTOMPADDING", (0, 0), (-1, -1), 0)]))
    return row

TOTAL_PAGES = {"n": 4}

def on_page(canvas, doc, page_title):
    header_band(canvas, doc, "SFAR — RFE 2009 (MODULE 1/4 — PÉRIMÈTRE LIMITÉ)",
                "Gestion périopératoire des traitements chroniques — Cardiovasculaire",
                page_title, icon_fn=lambda c, x, y: icon_pill(c, x, y, 13 * mm), color=TEAL_DARK)
    footer_band(canvas, doc, SOURCE_TXT, f"Page {doc.page} / {TOTAL_PAGES['n']}")

# ---------------------------------------------------------------------------
def _section_intro_bb_ic():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Périmètre limité :</b> le référentiel SFAR complet (2009-2011) comporte 4 modules "
        "distincts (Cardiovasculaire ; Douleur chronique/toxicomanie ; Infectieux/"
        "immunosuppresseurs ; Neurologique-psychiatrique et/ou endocrinien). Cette fiche couvre "
        "UNIQUEMENT le <b>Module 1 — Pathologies cardiovasculaires</b> (le plus transversal à "
        "toute anesthésie programmée). Les 3 autres modules ne sont pas traités — hors périmètre "
        "de cette fiche, disclosed explicitement, à construire séparément. Les traitements "
        "antithrombotiques (antiagrégants plaquettaires, AVK) sont explicitement exclus de "
        "l'ensemble du référentiel par son comité d'organisation lui-même (déjà couverts par "
        "d'autres textes SFAR/HAS distincts).", S_BODY),
        bg=AMBER_LIGHT, border=AMBER))
    story.append(Spacer(1, 2.5 * mm))
    story.append(legend_flowable())
    story.append(Spacer(1, 3 * mm))
    story.append(KeepTogether([
        section_bar("Bêtabloquants"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("Bêtabloquants", "Ne pas interrompre le traitement chronique en périopératoire ; "
         "administrer le matin de l'intervention avec la prémédication, reprendre le plus "
         "rapidement possible (relais parentéral si voie orale indisponible).", "AF"),
    ], RCW))
    story.append(Spacer(1, 1.5 * mm))
    story.append(context_note(
        "traitement chronique bien toléré sur le plan hémodynamique en périopératoire (grade C) ; "
        "possibilité d'hypotension artérielle ou de bradycardie lors de l'anesthésie si la "
        "posologie est titrée sur la fréquence cardiaque, d'autant plus que l'intensité du "
        "traitement est forte (grade A). Avis cardiologique non indispensable ; aucune technique "
        "d'anesthésie n'est spécifiquement contre-indiquée."))
    story.append(Spacer(1, 3 * mm))
    story.append(KeepTogether([
        section_bar("Inhibiteurs calciques"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("Inhib. calciques", "Poursuite du traitement (visée antiarythmique ou antihypertensive) "
         "recommandée en périopératoire.", "C"),
        ("Inhib. calciques", "Éviter la bupivacaïne périmédullaire (notamment péridurale) chez le "
         "patient traité au long cours par vérapamil (risque d'hypotension ou de bradycardie).", "C"),
        ("Inhib. calciques", "Préférer l'isoflurane, le desflurane ou le sévoflurane à l'halothane "
         "chez le patient traité par vérapamil (association délétère par addition d'effets "
         "dépresseurs myocardiques).", "B"),
        ("Inhib. calciques", "Préférer la lidocaïne à la bupivacaïne pour toute ALR chez le patient "
         "traité par diltiazem ou vérapamil — mais cette association peut augmenter "
         "expérimentalement la toxicité cardiaque de la lidocaïne.", "B"),
    ], RCW))
    return story

# ---------------------------------------------------------------------------
def _section_diuretiques_nicorandil_sraa():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Diurétiques"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("Diurétiques", "Ne pas administrer les diurétiques le matin de l'intervention "
         "(contrôle de la kaliémie souhaitable).", "AF"),
    ], RCW))
    story.append(Spacer(1, 3 * mm))
    story.append(KeepTogether([
        section_bar("Activateurs des canaux potassiques (nicorandil)"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("Nicorandil", "Ne pas interrompre le nicorandil en préopératoire.", "AF"),
        ("Nicorandil", "À la posologie orale de 20 mg/j, peut être poursuivi et administré en "
         "prémédication sans conséquence hémodynamique notoire lors de l'anesthésie.", "B"),
    ], RCW))
    story.append(Spacer(1, 3 * mm))
    story.append(KeepTogether([
        section_bar("Inhibiteurs du SRAA (IEC et sartans)"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("IEC / sartans", "Interrompre au moins 12 heures avant l'intervention lorsqu'ils "
         "constituent un traitement de fond de l'hypertension artérielle.", "AF"),
        ("IEC / sartans", "Maintenir lorsqu'ils sont prescrits dans le cadre d'une insuffisance "
         "cardiaque — risque d'hypotension à prendre en compte si chirurgie majeure ou "
         "rachianesthésie.", "AF"),
    ], RCW))
    return story

# ---------------------------------------------------------------------------
def _section_nitres_statines_aa1():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Dérivés nitrés"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("Dérivés nitrés", "Ne pas interrompre les dérivés nitrés par voie orale en "
         "préopératoire.", "AF"),
    ], RCW))
    story.append(Spacer(1, 3 * mm))
    story.append(KeepTogether([
        section_bar("Statines"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("Statines", "Ne pas interrompre le traitement chronique en périopératoire ; "
         "administrer le soir précédant l'intervention, reprendre le soir de l'intervention.", "AF"),
        ("Statines", "En cas d'interruption du transit intestinal et d'absence de forme "
         "parentérale disponible, une administration par sonde nasogastrique est recommandée.", "C"),
    ], RCW))
    story.append(Spacer(1, 1.5 * mm))
    story.append(context_note(
        "l'arrêt d'un traitement chronique par statines est associé à une augmentation des "
        "complications coronaires postopératoires par effet rebond (grade C) ; la fréquence des "
        "élévations des marqueurs musculaires biologiques n'est pas augmentée en cas de "
        "traitement chronique, malgré un risque théorique de rhabdomyolyse (grade C, absence de "
        "preuve liée au caractère exceptionnel de cette complication). Avis cardiologique non "
        "nécessaire."))
    story.append(Spacer(1, 3 * mm))
    story.append(KeepTogether([
        section_bar("Antiarythmiques — classe I de Vaughan-Williams"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(ungraded_note(
        "interrompre 24 heures avant une intervention chirurgicale programmée un traitement "
        "oral par antiarythmique de classe I (quinidine, procaïnamide, disopyramide, lidocaïne, "
        "mexilétine, diphénylhydantoïne, flécaïnide, propafénone, cibenzoline) prescrit en "
        "prévention primaire de la fibrillation auriculaire — seul énoncé prescriptif de cette "
        "section sans grade ni accord attaché par la source elle-même (aucun grade inventé ici)."))
    return story

# ---------------------------------------------------------------------------
def _section_aa3_stimulateurs():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Antiarythmiques — classe III de Vaughan-Williams"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("Amiodarone", "Poursuivie sans interruption jusqu'au matin de l'intervention (en "
         "raison de sa longue demi-vie d'élimination).", "AF"),
        ("Sotalol", "Ne doit pas être interrompu brutalement avant une intervention chirurgicale "
         "(risque de troubles du rythme graves, d'infarctus ou de mort subite chez le patient "
         "coronarien).", "AF"),
    ], RCW))
    story.append(Spacer(1, 3 * mm))
    story.append(KeepTogether([
        section_bar("Stimulateurs cardiaques et défibrillateurs automatiques implantables (DCI)",
                    color=GREY),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(P(
        "<b>Section non gradée par la source</b> (aucun A/B/C/D attaché à aucun moment) — "
        "reproduite ici en repère pratique condensé plutôt qu'en tableau de recommandations "
        "gradées, pour ne pas inventer de grade absent du texte source.", S_BODY_SM))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>Interférences électromagnétiques (IEM)</b> : risques — inhibition de la stimulation "
        "(bradycardie ventriculaire), passage transitoire en mode asynchrone, reprogrammation "
        "aléatoire (exceptionnelle). Sources : bistouri électrique (favorisé par courant "
        "puissant, mode monopolaire, application prolongée, boîtier dans l'axe plaque-site), "
        "ablation par radiofréquence, lithotripsie, IRM (contre-indiquée).", S_BODY_SM))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>Bistouri électrique</b> : privilégier le mode bipolaire ; courant de coagulation le "
        "plus faible possible ; application brève et intermittente ; boîtier hors de l'axe "
        "reliant le site de coagulation et la plaque de terre.", S_BODY_SM))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>Aimant sur le boîtier</b> : pour un DCI implanté en France, inhibe la fonction "
        "antiarythmique sans modifier la stimulation, le temps de l'application. Certains DCI "
        "(non implantés en France au moment du texte) peuvent voir cette fonction inhibée de "
        "façon permanente après application prolongée (&gt; 30 min) — surveillance continue du "
        "rythme jusqu'à confirmation de la réactivation.", S_BODY_SM))
    story.append(Spacer(1, 2 * mm))
    story.append(no_consensus_note(
        "la reprogrammation préopératoire du stimulateur en mode asynchrone chez le patient "
        "stimulo-dépendant, et la déprogrammation de la fonction d'asservissement, peuvent être "
        "proposées mais ne font l'une ni l'autre l'objet d'un consensus selon la source."))
    story.append(Spacer(1, 2 * mm))
    story.append(P(
        "<b>Avis spécialisé</b> (cardiologue traitant) à obtenir si : symptômes fonctionnels ; "
        "dernier contrôle ancien (stimulateur &gt; 1 an, DCI &gt; 3 mois) ; besoin de "
        "reprogrammation. <b>Choc électrique externe (CEE)</b> : vérification du "
        "stimulateur/DCI indispensable après le choc ; électrodes en position antéropostérieure "
        "chez le porteur d'un DCI actif. <b>Postopératoire</b> : vérification du "
        "stimulateur/DCI exposé à une IEM recommandée ; reprogrammation si anomalie ou si le "
        "programme avait été modifié en préopératoire.", S_BODY_SM))
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("Sources et avertissement", color=GREY))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>Document source :</b> Société française d'anesthésie et de réanimation (SFAR), "
        "« Gestion périopératoire des traitements chroniques et dispositifs médicaux — "
        "Pathologies cardiovasculaires », Recommandations Formalisées d'Experts, "
        "Annales Françaises d'Anesthésie et de Réanimation 28 (2009) 1037-1045.", S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>URL source :</b> https://sfar.org/gestion-perioperatoire-des-traitements-chroniques-"
        "et-dispositifs-medicaux-anti-infectieux-immunosuppresseurs/", S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>Couverture :</b> Module 1/4 du référentiel uniquement (pathologies "
        "cardiovasculaires) — 15 recommandations gradées (A/B/C/accord fort) + 1 recommandation "
        "explicitement non gradée par la source + 1 section pratique non gradée (stimulateurs "
        "cardiaques/DCI). Les modules Douleur chronique/toxicomanie, Infectieux/"
        "immunosuppresseurs, et Neurologique-psychiatrique/endocrinien ne sont pas couverts — "
        "hors périmètre de cette fiche, disclosed en page 1. Traitements antithrombotiques "
        "(antiagrégants, AVK) hors périmètre de l'ensemble du référentiel (couverts par "
        "d'autres textes SFAR/HAS). Argumentaire scientifique détaillé (document source complet) "
        "non reproduit.", S_SOURCE))
    story.append(Spacer(1, 2 * mm))
    story.append(info_panel(P(
        "<b>Avertissement :</b> cette fiche est une synthèse indépendante et PARTIELLE "
        "(Module 1 uniquement). Elle ne remplace pas le texte intégral — en particulier pour "
        "toute question relevant des 3 autres modules du référentiel. Cette fiche n'est ni "
        "éditée ni validée par la SFAR.", S_BODY_SM), bg=GREY_LIGHT, border=GREY))
    return story

# ---------------------------------------------------------------------------
SECTIONS = [
    ("Bêtabloquants & inhibiteurs calciques", _section_intro_bb_ic),
    ("Diurétiques, nicorandil & inhibiteurs du SRAA", _section_diuretiques_nicorandil_sraa),
    ("Dérivés nitrés, statines & antiarythmiques classe I", _section_nitres_statines_aa1),
    ("Antiarythmiques classe III & stimulateurs cardiaques", _section_aa3_stimulateurs),
]

def _make_doc(path=None):
    return SimpleDocTemplate(path or OUT, pagesize=A4,
                              leftMargin=MARGIN, rightMargin=MARGIN,
                              topMargin=32 * mm, bottomMargin=16 * mm,
                              title="Fiche SFAR 2009 - Gestion traitements chroniques (Module 1 - Cardiovasculaire)",
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
