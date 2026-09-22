# -*- coding: utf-8 -*-
"""
Fiche de synthese - "Gestion perioperatoire des traitements chroniques et
dispositifs medicaux. Douleur chronique, toxicomanie" - Recommandations
Formalisees d'Experts (RFE), SFAR, 2009 (Ann Fr Anesth Reanim 28 (2009)
1046-1056). Meme PDF source fusionne que fiche_gestion_traitements_
chroniques_cardio_2009.py (Module 1) - voir son docstring pour le contexte
complet du referentiel composite a 4 modules.

PERIMETRE : cette fiche couvre le MODULE 2/4 du referentiel (pages 12-22 du
PDF fusionne, identifiees par lecture complete) - analgesiques morphiniques
et non morphiniques utilises dans la douleur chronique, dispositifs
implantables (catheters intrathecaux/perimedullaires, stimulateurs
medullaires), toxicomanie substituee (methadone/buprenorphine) et active
(cannabis, heroine, cocaine, autres excitants du SNC, medicaments
detournes). Les modules 1 (Cardiovasculaire, deja construit), 3
(Infectieux/immunosuppresseurs) et 4 (Neurologique/psychiatrique) ne sont
PAS couverts ici - disclosed explicitement, a construire separement.

METHODOLOGIE : meme grille ANAES 2004 A/B/C/D que le module 1 (D renforce en
"accord fort" par methode Delphi - chip local "AF"). PARTICULARITE DISCLOSED
DE CE MODULE (differente du module 1) : la tres grande majorite des enonces
prescriptifs de ce module ("il est recommande de...", "il n'est pas
recommande de...") ne portent AUCUNE citation de grade/accord explicite -
seuls 28 enonces sur l'ensemble du module citent effectivement un grade
(A:0, B:4, C:9, accord fort:15). Conformement a la regle 4 (ne jamais
fabriquer un grade absent du source), SEULS ces 28 enonces explicitement
gradés apparaissent dans les tableaux de recommandations gradees ci-dessous
(consolides en lignes lorsque 2 citations consecutives partagent le MEME
grade, jamais lorsque les grades different) ; tous les autres enonces
prescriptifs du texte source (largement majoritaires dans ce module) sont
regroupes en blocs de "reperes pratiques" non grades, disclosed comme tels
une fois par section plutot que par un encadre repete a chaque ligne (ce qui
aurait rendu la fiche exagerement longue pour un module deja tres dense -
regle 7).

DECOMPTE : 26 lignes de recommandations gradees dans les tableaux (portant
28 citations de grade source, 2 lignes consolidant chacune 2 citations du
meme grade) + de tres nombreux reperes pratiques non grades (dosages de
conversion, precautions techniques, contre-indications relatives) regroupes
par classe therapeutique/substance en blocs de texte condense. Table de
correspondance des opioides (paliers 2 vers morphine, IV/orale) et table de
conversion methadone/buprenorphine/morphine reproduites verbatim (regle 1).
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

OUT = "/home/user/rfe-sfar-website/output/Fiche_Gestion_Traitements_Chroniques_Douleur_Toxico_2009.pdf"

SOURCE_TXT = ("Source : SFAR, « Gestion périopératoire des traitements chroniques et dispositifs "
              "médicaux — Douleur chronique, toxicomanie », RFE, Ann Fr Anesth Réanim 28 (2009) "
              "1046-1056 — Module 2/4 uniquement. Fiche de synthèse non officielle : se référer au texte intégral.")

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

RCW = [32 * mm, CW_FULL - 32 * mm - 15 * mm, 15 * mm]

def practical_block(title, txt):
    story = []
    story.append(P(f"<b>{title}</b> <i>(repères non gradés par la source)</i> : {txt}", S_BODY_SM))
    return story

def ungraded_disclosure():
    return info_panel(P(
        "<b>Repères pratiques non gradés :</b> la majorité des énoncés prescriptifs de ce module "
        "ne portent aucune citation de grade dans le texte source. Conformément à la règle "
        "anti-fabrication de grade, ils sont regroupés ci-dessous en repères pratiques par "
        "substance, distincts des tableaux de recommandations effectivement gradées.", S_BODY_SM),
        bg=GREY_LIGHT, border=GREY)

def legend_flowable():
    chip_w = 16 * mm
    content_w = CW_FULL
    row = Table([[chip("A", width=chip_w - 2 * mm), chip("B", width=chip_w - 2 * mm),
                  chip("C", width=chip_w - 2 * mm), chip("AF", width=chip_w - 2 * mm),
                  P("<b>Grille ANAES 2004</b> — <b>A</b> : preuve scientifique établie ; "
                    "<b>B</b> : présomption scientifique ; <b>C</b> : faible niveau de preuve ; "
                    "<b>AF</b> : accord fort (grade D renforcé par méthode Delphi). Fiche limitée "
                    "au Module 2/4 du référentiel (douleur chronique, toxicomanie) — voir encadré "
                    "de périmètre ci-dessous. La majorité des énoncés de ce module ne portent "
                    "aucun grade — voir « repères pratiques non gradés ».", S_BADGE_HEAD)]],
                colWidths=[chip_w] * 4 + [content_w - 4 * chip_w])
    row.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                              ("LEFTPADDING", (0, 0), (-1, -1), 1),
                              ("RIGHTPADDING", (0, 0), (-1, -1), 1),
                              ("TOPPADDING", (0, 0), (-1, -1), 0),
                              ("BOTTOMPADDING", (0, 0), (-1, -1), 0)]))
    return row

def conversion_table(headers, rows, col_widths):
    data = [[P(h, S_HEAD_W_C) for h in headers]]
    for r in rows:
        data.append([P(c, S_CELL) for c in r])
    t = Table(data, colWidths=col_widths, repeatRows=1)
    style_cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), GREY), ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTNAME", (0, 0), (-1, 0), FONT_BOLD), ("FONTSIZE", (0, 0), (-1, 0), 7.6),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 0.5, GREY_LIGHT),
        ("TOPPADDING", (0, 0), (-1, -1), 2.6), ("BOTTOMPADDING", (0, 0), (-1, -1), 2.6),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            style_cmds.append(("BACKGROUND", (0, i), (-1, i), BG_PANEL))
    t.setStyle(TableStyle(style_cmds))
    return t

TOTAL_PAGES = {"n": 5}

def on_page(canvas, doc, page_title):
    header_band(canvas, doc, "SFAR — RFE 2009 (MODULE 2/4 — PÉRIMÈTRE LIMITÉ)",
                "Gestion périopératoire des traitements chroniques — Douleur & toxicomanie",
                page_title, icon_fn=lambda c, x, y: icon_pill(c, x, y, 13 * mm), color=TEAL_DARK)
    footer_band(canvas, doc, SOURCE_TXT, f"Page {doc.page} / {TOTAL_PAGES['n']}")

# ---------------------------------------------------------------------------
def _section_opioides_ains():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Périmètre limité :</b> le référentiel SFAR complet (2009-2011) comporte 4 modules "
        "distincts (Cardiovasculaire, déjà traité dans une fiche séparée ; Douleur chronique/"
        "toxicomanie — cette fiche ; Infectieux/immunosuppresseurs ; Neurologique-psychiatrique "
        "et/ou endocrinien). Les 3 autres modules ne sont pas traités ici — disclosed "
        "explicitement, à construire séparément.", S_BODY),
        bg=AMBER_LIGHT, border=AMBER))
    story.append(Spacer(1, 2.5 * mm))
    story.append(legend_flowable())
    story.append(Spacer(1, 3 * mm))
    story.append(KeepTogether([
        section_bar("Opioïdes (traitement chronique de la douleur)"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("Opioïdes", "Un sevrage ou réajustement thérapeutique ne doit pas être envisagé en "
         "période périopératoire — seulement à distance de l'intervention, en période de "
         "stabilité et lorsque la douleur a significativement diminué.", "C"),
        ("Opioïdes", "Administrer en préopératoire la dose habituelle de morphinique, ou la dose "
         "équianalgésique d'un autre opioïde (voie orale ou IV à l'induction).", "AF"),
        ("Opioïdes", "Un patch de fentanyl ne doit pas être retiré en périopératoire, sauf "
         "substitution par un autre opioïde.", "AF"),
        ("Opioïdes", "Les morphiniques de palier 2 (codéine, dextropropoxyphène, tramadol) "
         "doivent être poursuivis, voire substitués par un autre opioïde (y compris de palier "
         "supérieur) à dose équianalgésique.", "AF"),
        ("Opioïdes", "Éviter, hors urgence, les antagonistes/agonistes partiels/antagonistes μ "
         "(naloxone, naltrexone, nalbuphine, butorphanol, buprénorphine, pentazocine) chez le "
         "patient dépendant aux opioïdes — risque de syndrome de sevrage.", "C"),
    ], RCW))
    story.append(Spacer(1, 2 * mm))
    story.append(conversion_table(
        ["DCI", "Ratio vs. morphine orale", "Équivalence"],
        [
            ["Dextropropoxyphène", "1/6", "60 mg = 10 mg morphine"],
            ["Codéine", "1/6", "60 mg = 10 mg morphine"],
            ["Dihydrocodéine", "1/3", "60 mg = 20 mg morphine"],
            ["Tramadol", "1/5 à 1/6", "50-60 mg = 10 mg morphine"],
            ["Péthidine", "1/5", "50 mg = 10 mg morphine"],
            ["Morphine IV", "3", "1 mg IV = 3 mg morphine orale"],
            ["Morphine SC/IM", "2", "1 mg SC = 2 mg morphine orale"],
            ["Oxycodone orale", "2", "5 mg = 10 mg morphine orale"],
            ["Hydromorphone", "7,5", "4 mg = 30 mg morphine"],
            ["Buprénorphine SL", "30", "0,2 mg = 6 mg morphine orale"],
            ["Fentanyl transdermique", "variable", "25 µg/h ~ 60 mg/j morphine"],
        ], [50 * mm, 32 * mm, CW_FULL - 82 * mm]))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P("<i>10 mg de morphine IV = 1 mg de morphine péridurale = 0,1 mg de morphine "
                    "intrathécale.</i>", S_NOTE))
    story.append(Spacer(1, 3 * mm))
    story.append(KeepTogether([
        section_bar("Analgésiques non morphiniques — AINS et coxibs"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("AINS non sélectifs", "Maintien recommandé en périopératoire si les contre-indications "
         "sont respectées — SAUF pour les chirurgies à risque hémorragique difficile à contrôler "
         "(neurochirurgie intracrânienne, chirurgie urologique, amygdalectomie, chirurgie "
         "ophtalmologique hors cataracte, chirurgie orthopédique lourde), où l'arrêt est "
         "recommandé.", "B"),
        ("Coxibs", "Maintien recommandé en périopératoire chez les patients sans facteur de "
         "risque cardiovasculaire opérés de chirurgie non cardiaque.", "B"),
    ], RCW))
    story.append(Spacer(1, 1.5 * mm))
    story.append(context_note_local(
        "absence de recommandation dégagée par la source elle-même sur le risque "
        "cardiovasculaire périopératoire des coxibs au long cours (absence d'étude spécifique) ; "
        "pas d'arrêt recommandé d'un AINS/coxib avant une ALR périphérique (risque hémorragique "
        "très faible/nul). Stratégie d'arrêt pour chirurgie à risque hémorragique : AINS de "
        "longue demi-vie (oxicams, naproxène) 7 à 10 jours avant, AINS de demi-vie courte "
        "(ibuprofène, kétoprofène, flurbiprofène) 24 heures avant."))
    return story

def context_note_local(txt):
    return P(f"<i>Précision du source :</i> {txt}", S_NOTE)

# ---------------------------------------------------------------------------
def _section_antalgiques_dispositifs():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Antiépileptiques, antidépresseurs & benzodiazépines (douleur chronique)"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("Antiépileptiques", "Poursuivre en périopératoire les traitements prescrits à visée "
         "antalgique (clonazépam, carbamazépine, gabapentine, prégabaline).", "AF"),
        ("Antidépresseurs", "Poursuivre en périopératoire les traitements prescrits à visée "
         "antalgique (tricycliques, IRS, venlafaxine).", "AF"),
        ("Benzodiazépines", "Poursuivre en périopératoire les traitements prescrits à visée "
         "antalgique (ex. clonazépam pour douleur neuropathique).", "AF"),
    ], RCW))
    story.append(Spacer(1, 1.5 * mm))
    story.append(context_note_local(
        "la carbamazépine peut diminuer la durée d'action des curares ; la gabapentine en "
        "prémédication à dose importante (1200 mg) réduit l'hyperalgésie postopératoire. En cas "
        "d'interruption du transit, voie IV possible pour le clonazépam (aucune forme IV pour la "
        "gabapentine — sonde gastrique envisageable)."))
    story.append(Spacer(1, 3 * mm))
    story.append(KeepTogether([
        section_bar("Cathéters intrathécaux/périmédullaires & stimulateurs médullaires"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("Cathéters intrathécaux", "Ne pas interrompre la perfusion des dispositifs analgésiques "
         "(opiacés, baclofène) tout au long de la période périopératoire, pour éviter un "
         "sevrage.", "AF"),
        ("Cathéters intrathécaux", "En cas de risque particulier (effets indésirables du "
         "baclofène, récidive de troubles neurologiques à son arrêt), un contact avec le médecin "
         "référent est souhaitable pour déterminer la stratégie.", "AF"),
        ("Stimulateur médullaire", "Ne pas réaliser d'anesthésie et/ou d'analgésie "
         "périmédullaire chez le porteur d'un stimulateur médullaire.", "AF"),
        ("Stimulateur médullaire", "Précautions d'utilisation au bloc opératoire identiques à "
         "celles des stimulateurs cardiaques (bistouri bipolaire recommandé), en l'absence de "
         "données spécifiques.", "AF"),
    ], RCW))
    story.append(Spacer(1, 1.5 * mm))
    story.append(context_note_local(
        "en cas de tolérance/désensibilisation aux opiacés (cathéter intrathécal au long cours), "
        "il est recommandé d'augmenter les posologies de morphiniques (la kétamine pourrait être "
        "d'un apport intéressant) ; en cas d'anesthésie axiale, peser les bénéfices/risques "
        "(contamination infectieuse du dispositif) et connaître le niveau d'insertion et le "
        "trajet du cathéter."))
    return story

# ---------------------------------------------------------------------------
def _section_toxico_substituee():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Toxicomanie substituée (méthadone, buprénorphine)"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("Subst. opiacés", "Donner oralement, le matin de l'intervention, la dose quotidienne du "
         "traitement substitutif, quelle que soit la technique d'anesthésie choisie.", "AF"),
        ("Subst. opiacés", "Si la voie orale est impossible, administrer la morphine par voie "
         "sous-cutanée ou intraveineuse.", "AF"),
        ("Subst. opiacés", "Poursuivre le traitement substitutif tout au long de "
         "l'hospitalisation, pour assurer les besoins de base en opiacés et éviter un sevrage.", "AF"),
        ("Subst. opiacés", "Favoriser chaque fois que possible une ALR axiale ou périphérique.", "AF"),
        ("Subst. opiacés", "Augmenter les doses de morphine prescrites pour l'analgésie "
         "postopératoire ; la kétamine pourrait présenter un intérêt chez ces patients "
         "tolérants aux opiacés.", "C"),
        ("Subst. opiacés", "Les agonistes-antagonistes et antagonistes des récepteurs μ "
         "(nalbuphine, butorphanol, pentazocine, naloxone) sont formellement contre-indiqués "
         "chez le patient sous traitement substitutif.", "C"),
    ], RCW))
    story.append(Spacer(1, 1.5 * mm))
    story.append(context_note_local(
        "il est recommandé d'arrêter la naltrexone au minimum 24 à 48 heures avant une "
        "intervention (cet antagoniste μ diminue fortement les effets des morphiniques) ; "
        "adresser le patient en consultation avec un médecin spécialisé en toxicomanie ; "
        "prémédication par benzodiazépine souvent adaptée (codépendance fréquente)."))
    story.append(Spacer(1, 2 * mm))
    story.append(conversion_table(
        ["Molécule", "Équivalence (ordre de grandeur)"],
        [
            ["Sulfate de morphine oral", "10 mg (référence)"],
            ["Sulfate de morphine parentéral (IV/SC)", "~ 3,3 mg"],
            ["Méthadone orale", "~ 6–7 mg"],
            ["Buprénorphine", "~ 1,2–1,4 mg"],
        ], [90 * mm, CW_FULL - 90 * mm]))
    return story

# ---------------------------------------------------------------------------
def _section_toxico_active_sources():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Toxicomanie active — cannabis, héroïne, cocaïne, autres substances"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("Cannabis", "S'abstenir de fumer ou de consommer du cannabis avant une chirurgie "
         "réglée (comme pour le tabac).", "AF"),
        ("Héroïne (active)", "Les agonistes-antagonistes et antagonistes μ sont formellement "
         "contre-indiqués (risque de syndrome de sevrage aigu).", "C"),
        ("Héroïne (active)", "Augmenter fréquemment les doses des médicaments hypnotiques et "
         "morphiniques en cas d'anesthésie générale.", "C"),
        ("Cocaïne", "En cas d'ALR axiale, demander au minimum un dosage des plaquettes (risque "
         "de thrombopénie).", "C"),
        ("Médic. détournés", "Risque de crise convulsive lors d'un sevrage des benzodiazépines.", "C"),
        ("Médic. détournés", "Il n'est pas recommandé d'administrer des doses plus élevées de "
         "morphiniques pour l'anesthésie générale ou l'analgésie postopératoire (absence de "
         "tolérance croisée benzodiazépines/morphiniques).", "B"),
    ], RCW))
    story.append(Spacer(1, 1.5 * mm))
    story.append(ungraded_disclosure())
    story.append(Spacer(1, 2 * mm))
    story.extend(practical_block("Cannabis",
        "prudence avec les médicaments tachycardisants (kétamine, pancuronium, atropine, "
        "éphédrine, adrénaline), éviter l'halothane ; potentialise les effets des opiacés "
        "(somnolence, dépression respiratoire)."))
    story.append(Spacer(1, 1.5 * mm))
    story.extend(practical_block("Héroïne (active)",
        "le sevrage en période chirurgicale n'est jamais le bon moment (risque de récidive) ; "
        "établir un contrat de soins explicite avec le patient et l'équipe spécialisée ; "
        "substitution le matin de la chirurgie par une dose équivalente de morphine orale ; en "
        "urgence, considérer le patient comme estomac plein et réaliser une induction en "
        "séquence rapide."))
    story.append(Spacer(1, 1.5 * mm))
    story.extend(practical_block("Cocaïne",
        "sevrage complet d'au moins une semaine avant une intervention programmée (un sevrage "
        "plus court ne protège pas des complications) ; éviter étomidate, kétamine et halothane "
        "en cas d'anesthésie générale ; bêtabloquants contre-indiqués (majoration de la "
        "vasoconstriction) ; benzodiazépines et dérivés nitrés en traitement de première "
        "intention des complications cardiovasculaires ; vérifier le taux de plaquettes avant "
        "ALR axiale chez la parturiente cocaïnomane."))
    story.append(Spacer(1, 1.5 * mm))
    story.extend(practical_block("Autres excitants du SNC (LSD, PCP, ecstasy/MDMA…)",
        "précaution avec les vasopresseurs (éphédrine) ; éviter succinylcholine et halogénés en "
        "cas d'antécédent d'hyperthermie induite par le MDMA ; surveiller les apports hydriques "
        "et le bilan hydroélectrolytique (risque d'hyponatrémie profonde)."))
    story.append(Spacer(1, 1.5 * mm))
    story.extend(practical_block("Médicaments détournés (benzodiazépines)",
        "prescrire une benzodiazépine en périopératoire pour prévenir un syndrome de sevrage ; "
        "réduire les doses d'hypnotiques en cas d'intoxication aiguë."))
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("Sources et avertissement", color=GREY))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>Document source :</b> Société française d'anesthésie et de réanimation (SFAR), "
        "« Gestion périopératoire des traitements chroniques et dispositifs médicaux — Douleur "
        "chronique, toxicomanie », Recommandations Formalisées d'Experts, Annales Françaises "
        "d'Anesthésie et de Réanimation 28 (2009) 1046-1056.", S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>URL source :</b> https://sfar.org/gestion-perioperatoire-des-traitements-chroniques-"
        "et-dispositifs-medicaux-anti-infectieux-immunosuppresseurs/", S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>Couverture :</b> Module 2/4 du référentiel uniquement (douleur chronique, "
        "toxicomanie) — 26 lignes de recommandations gradées (28 citations de grade source, "
        "A:0/B:4/C:9/accord fort:15) + de nombreux repères pratiques non gradés par la source "
        "elle-même, regroupés par substance. Les modules Cardiovasculaire (traité "
        "séparément), Infectieux/immunosuppresseurs, et Neurologique-psychiatrique/endocrinien "
        "ne sont pas couverts ici — hors périmètre de cette fiche, disclosed en page 1. "
        "Argumentaire scientifique détaillé (document source complet) non reproduit.", S_SOURCE))
    story.append(Spacer(1, 2 * mm))
    story.append(info_panel(P(
        "<b>Avertissement :</b> cette fiche est une synthèse indépendante et PARTIELLE "
        "(Module 2 uniquement). Elle ne remplace pas le texte intégral — en particulier pour "
        "toute question relevant des 3 autres modules du référentiel. Cette fiche n'est ni "
        "éditée ni validée par la SFAR.", S_BODY_SM), bg=GREY_LIGHT, border=GREY))
    return story

# ---------------------------------------------------------------------------
def _section_opioides_ains_dispositifs():
    story = _section_opioides_ains()
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_antalgiques_dispositifs())
    return story

def _section_toxico_all():
    story = _section_toxico_substituee()
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_toxico_active_sources())
    return story

SECTIONS = [
    ("Opioïdes, AINS/coxibs, antiépileptiques & dispositifs implantables", _section_opioides_ains_dispositifs),
    ("Toxicomanie substituée & active, sources", _section_toxico_all),
]

def _make_doc(path=None):
    return SimpleDocTemplate(path or OUT, pagesize=A4,
                              leftMargin=MARGIN, rightMargin=MARGIN,
                              topMargin=32 * mm, bottomMargin=16 * mm,
                              title="Fiche SFAR 2009 - Gestion traitements chroniques (Module 2 - Douleur/Toxicomanie)",
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
