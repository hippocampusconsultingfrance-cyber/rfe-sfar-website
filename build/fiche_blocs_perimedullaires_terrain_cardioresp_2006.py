# -*- coding: utf-8 -*-
"""
Fiche de synthese - "Les blocs perimedullaires chez l'adulte" - Question 9
(Anesthesie perimedullaire des malades porteurs d'une pathologie
cardiovasculaire) et Question 10 (... pathologie respiratoire) -
Recommandations pour la Pratique Clinique (RPC), SFAR/Sofcot/Sofmer,
presentees le 24 septembre 2005 (47e congres SFAR), publiees Ann Fr Anesth
Reanim 26 (2007) 720-752.

CINQUIEME INSTALLMENT de ce document (voir fiche_blocs_perimedullaires_ci_2006.py
pour Q1-2, fiche_blocs_perimedullaires_technique_2006.py pour Q3-5,
fiche_blocs_perimedullaires_cesarienne_2006.py pour Q7,
fiche_blocs_perimedullaires_postop_2006.py pour Q8). Perimetre volontairement
limite (meme pattern) : 369 citations de grade au total sur 15 Questions.
Cette fiche couvre INTEGRALEMENT les Questions 9 (terrain cardiovasculaire)
et 10 (terrain respiratoire) - les deux premieres des cinq "Questions
terrain" consecutives du document (9 a 13 : cardiovasculaire, respiratoire,
hemostase, neurologique, infectieux). Les Questions 11-13 (hemostase,
neurologique, infectieux - nettement plus volumineuses, 21+41+8=70 citations
brutes) ne sont PAS couvertes ici, non plus que les Questions 14-15 (gestion
de l'echec, facteurs de risque de complications) - installments futurs.

METHODOLOGIE : grille EBM classique A/B/C (identique aux installments
precedents) + "accord professionnel" (une occurrence dans ce perimetre,
Question 9, cardiopathie hypertrophique) - chip local "AE" reutilise.
Aucune occurrence de "grade D", "consensus professionnel" ni "avis
d'experts" dans ce perimetre - verifie par grep, disclosed.

DECOMPTE - methodologie de consolidation identique aux installments
precedents (disclosed) : grep exhaustif sur le texte source des Questions 9
et 10 (lignes 2199-2339 du fichier texte extrait) trouve 21 citations de
grade individuelles : Question 9 - grade A x1, grade B x6, grade C x7,
accord professionnel x1 (15 au total) ; Question 10 - grade A x3, grade C x3
(6 au total). Plusieurs citations de MEME grade decrivant le MEME point
clinique dans un seul paragraphe source sont regroupees en une seule ligne
(jamais deux grades DIFFERENTS fusionnes dans une seule ligne - verifie par
le safety net regex apres redaction). Apres consolidation : 18 lignes de
recommandations gradees (A:4, B:3, C:10, AE:1), verifie par regex sur le
script final - Question 9 : 12 lignes (A:1, B:3, C:7, AE:1) ; Question 10 :
6 lignes (A:3, C:3, aucune consolidation necessaire, correspondance directe
1:1 avec les 6 citations brutes).

Aucun tableau ni figure dans le perimetre de ces deux Questions (verifie par
grep "Tableau|Figure|Fig\\." sur le texte source correspondant - zero
occurrence).
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from style import *
GRADE_COLORS["A"] = (GREEN, WHITE)
GRADE_COLORS["B"] = (TEAL, WHITE)
GRADE_COLORS["C"] = (AMBER, WHITE)
GRADE_COLORS["AE"] = (GREY, WHITE)
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.units import mm

OUT = "/home/user/rfe-sfar-website/output/Fiche_Blocs_Perimedullaires_Terrain_CardioResp_2006.pdf"

SOURCE_TXT = ("Source : SFAR/Sofcot/Sofmer, « Les blocs périmédullaires chez l'adulte », "
              "RPC, Ann Fr Anesth Réanim 26 (2007) 720-752 — Questions 9-10 uniquement. "
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

def practical_block(title, bullets):
    story = [P(f"<b>{title}</b>", S_BODY_SM)]
    for b in bullets:
        story.append(P(f"• {b}", S_BODY_SM))
    return story

def legend_flowable():
    chip_w = 16 * mm
    content_w = CW_FULL
    row = Table([[chip("A", width=chip_w - 2 * mm), chip("B", width=chip_w - 2 * mm),
                  chip("C", width=chip_w - 2 * mm), chip("AE", width=chip_w - 2 * mm),
                  P("<b>Grille EBM classique</b> — <b>A</b> : essais randomisés de forte "
                    "puissance/méta-analyses ; <b>B</b> : essais randomisés de faible "
                    "puissance/études de cohorte ; <b>C</b> : cas-témoins/études "
                    "rétrospectives ; <b>AE</b> : accord professionnel. Aucune citation "
                    "« grade D », « consensus professionnel » ni « avis d'experts » dans ce "
                    "périmètre. Fiche limitée aux Questions 9-10/15 du document (terrains "
                    "cardiovasculaire et respiratoire).", S_BADGE_HEAD)]],
                colWidths=[chip_w] * 4 + [content_w - 4 * chip_w])
    row.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                              ("LEFTPADDING", (0, 0), (-1, -1), 1),
                              ("RIGHTPADDING", (0, 0), (-1, -1), 1),
                              ("TOPPADDING", (0, 0), (-1, -1), 0),
                              ("BOTTOMPADDING", (0, 0), (-1, -1), 0)]))
    return row

TOTAL_PAGES = {"n": 6}

def on_page(canvas, doc, page_title):
    header_band(canvas, doc, "SFAR/SOFCOT/SOFMER — RPC 2007 (Q9-10/15 — PÉRIMÈTRE LIMITÉ)",
                "Les blocs périmédullaires chez l'adulte",
                page_title, icon_fn=lambda c, x, y: icon_shield(c, x, y, 13 * mm), color=TEAL_DARK)
    footer_band(canvas, doc, SOURCE_TXT, f"Page {doc.page} / {TOTAL_PAGES['n']}")

# ---------------------------------------------------------------------------
def _section_cardiovasculaire():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Périmètre limité — installment 5/n :</b> ce document source compte 15 « Questions » "
        "cliniques et 369 citations de grade au total. Cette fiche couvre INTÉGRALEMENT les "
        "Questions 9 (terrain cardiovasculaire) et 10 (terrain respiratoire) — les deux "
        "premières d'une série de 5 « Questions terrain » consécutives (9 à 13). Les Questions "
        "11-13 (hémostase, neurologique, infectieux — nettement plus volumineuses) et 14-15 "
        "(gestion de l'échec, facteurs de risque de complications) ne sont PAS couvertes ici — "
        "installments futurs. Les Questions 1-2, 3-5, 7 et 8 sont couvertes par des fiches "
        "séparées ; la Question 6 est exclue (superseded par une fiche HAS 2025).", S_BODY),
        bg=AMBER_LIGHT, border=AMBER))
    story.append(Spacer(1, 2.5 * mm))
    story.append(legend_flowable())
    story.append(Spacer(1, 3 * mm))
    story.append(KeepTogether([
        section_bar("Question 9 — Anesthésie périmédullaire et pathologie cardiovasculaire"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("Effets hémodynamiques", "Effets proportionnels à l'étendue du bloc sympathique : "
         "vasodilatation veineuse prédominante (↓retour veineux, ↓débit cardiaque, hypotension "
         "dans 15-50 % des cas) et bradycardie (atteinte des fibres cardioaccélératrices) ; "
         "effets limités si le bloc reste sous T11, importants entre T6-T11, majeurs au-delà de "
         "T6 ou si une AG est associée (hypotension et bradycardie associées dans 1/4 des cas).", "B"),
        ("Prévention/traitement", "Remplissage vasculaire + vasoconstricteur (éphédrine ou "
         "phényléphrine) ; les solutions colloïdes sont plus efficaces que les cristalloïdes.", "C"),
        ("HTA", "Arrêter un traitement inhibiteur du système rénine-angiotensine (IEC/ARA2) en "
         "préopératoire (pas d'effet rebond à l'arrêt).", "B"),
        ("HTA", "Administrer un vasoconstricteur pour compenser les effets de l'APM (bolus "
         "d'éphédrine 3 mg ou de phényléphrine 0,25 mg) ; la terlipressine a été proposée mais "
         "avec un risque connu d'accident coronarien.", "C"),
        ("HTA", "L'APM est contre-indiquée en cas d'HTA mal contrôlée, instable, sévère "
         "(PAD > 110 mmHg) ou maligne, et en cas d'urgence en dehors d'un contexte obstétrical.", "C"),
        ("Coronarien", "Le blocage sympathique a des effets bénéfiques chez le coronarien "
         "instable (via l'analgésie postopératoire induite), mais le risque d'ischémie "
         "myocardique augmente si le bloc est étendu, si une AG est associée, ou lors d'APM "
         "lombaire (tonus sympathique thoracique augmenté).", "B"),
        ("Coronarien", "Un traitement bêta-bloquant pris au long cours n'aggrave pas le risque "
         "coronaire.", "C"),
        ("Insuffisance cardiaque", "Les objectifs thérapeutiques du traitement de l'insuffisance "
         "cardiaque (IEC, ARAII, bêta-bloquant) visent l'augmentation de la fraction d'éjection "
         "par vasodilatation artérielle et la diminution des effets sympathique/SRA — aucun "
         "travail n'a étudié les effets d'une APM chez les patients traités par ces "
         "médicaments.", "A"),
        ("Insuffisance cardiaque", "En cas de cardiopathie dilatée, la baisse de la postcharge "
         "du VG induite par l'APM peut améliorer le volume d'éjection systolique malgré une "
         "diminution de la précharge ventriculaire.", "C"),
        ("Cardiopathie hypertrophique", "Il est possible d'utiliser l'APM, notamment lors de "
         "césarienne, malgré le risque d'hypotension induit par la diminution de la précharge "
         "ventriculaire.", "AE"),
        ("Valvulopathie sténosante", "Les APM sont en principe contre-indiquées.", "C"),
        ("Troubles du rythme", "Chez le patient traité par un antiarythmique, préférer la "
         "lidocaïne aux autres AL administrés en péridurale (la ropivacaïne et la "
         "lévobupivacaïne sont moins arythmogènes que la bupivacaïne).", "C"),
    ], RCW))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<i>Précision du source :</i> en cas de valvulopathie régurgitante, le risque de l'APM "
        "est superposable à celui des patients insuffisants cardiaques (non gradé).", S_NOTE))
    return story

# ---------------------------------------------------------------------------
def _section_respiratoire():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Question 10 — Anesthésie périmédullaire et pathologie respiratoire"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("Effets respiratoires", "Peu importants chez le sujet normal, mais peuvent être "
         "amplifiés par l'administration concomitante de sédatifs.", "A"),
        ("Asthme", "L'APM est recommandée chez l'asthmatique : elle évite l'intubation "
         "trachéale et ne modifie pas le seuil de réactivité bronchique.", "C"),
        ("Altération ventilatoire", "Chez les patients présentant une altération de la "
         "dynamique ventilatoire ou une sécrétion bronchique importante, éviter la paralysie "
         "des muscles respiratoires accessoires (risque d'encombrement bronchopulmonaire, "
         "d'atélectasie, d'infection) ; associer un AL à faible concentration et un opiacé "
         "(réduit les effets moteurs des AL) — solution analgésique de choix.", "C"),
        ("SAOS", "Risque accru d'intubation difficile et sensibilité particulière aux effets "
         "dépresseurs des agents anesthésiques.", "A"),
        ("SAOS", "L'APM sans opiacé est une technique recommandable, en évitant l'administration "
         "d'agents dépresseurs du système nerveux central.", "C"),
        ("Surveillance", "Doit être assurée par du personnel formé, dans des unités "
         "spécialisées selon l'état du patient et la voie d'administration ; un protocole de "
         "surveillance et de traitement des complications doit être écrit et disponible pour "
         "tout le personnel prenant en charge les patients.", "A"),
    ], RCW))
    story.append(Spacer(1, 1.5 * mm))
    story.extend(practical_block("Repères pratiques non gradés :", [
        "Durée de surveillance minimale : 24h après la dernière injection intrathécale de "
        "morphine, 6h après celle d'un opiacé liposoluble.",
        "Contenu de la surveillance : état de conscience, étendue du bloc sensitif, en plus des "
        "paramètres vitaux habituels.",
    ]))
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
        "<b>Couverture :</b> Questions 9-10/15 uniquement (terrains cardiovasculaire et "
        "respiratoire) — 18 recommandations gradées (A:4, B:3, C:10, AE:1). Les Questions "
        "11-13 (hémostase, neurologique, infectieux) et 14-15 (échec, facteurs de risque) ne "
        "sont pas couvertes ici — hors périmètre de cette fiche, installments futurs. "
        "Argumentaire scientifique détaillé (document source complet) non reproduit.", S_SOURCE))
    story.append(Spacer(1, 2 * mm))
    story.append(info_panel(P(
        "<b>Avertissement :</b> cette fiche est une synthèse indépendante et PARTIELLE "
        "(Questions 9-10 uniquement, sur 15). Elle ne remplace pas le texte intégral — en "
        "particulier pour les terrains hémostase/neurologique/infectieux, la gestion de "
        "l'échec, ou les facteurs de risque de complications. Cette fiche n'est ni éditée ni "
        "validée par la SFAR.", S_BODY_SM),
        bg=GREY_LIGHT, border=GREY))
    return story

# ---------------------------------------------------------------------------
SECTIONS = [
    ("Question 9 — Terrain cardiovasculaire", _section_cardiovasculaire),
    ("Question 10 — Terrain respiratoire & sources", _section_respiratoire),
]

def _make_doc(path=None):
    return SimpleDocTemplate(path or OUT, pagesize=A4,
                              leftMargin=MARGIN, rightMargin=MARGIN,
                              topMargin=32 * mm, bottomMargin=16 * mm,
                              title="Fiche SFAR 2007 - Blocs perimedullaires (Q9-10 - Terrain cardioresp)",
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
