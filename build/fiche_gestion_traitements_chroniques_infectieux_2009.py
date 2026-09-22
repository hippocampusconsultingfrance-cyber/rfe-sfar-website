# -*- coding: utf-8 -*-
"""
Fiche de synthese - "Gestion perioperatoire des traitements chroniques et
dispositifs medicaux. Anti-infectieux, immunosuppresseurs" - Recommandations
Formalisees d'Experts (RFE), SFAR, Ann Fr Anesth Reanim 28 (2009) 1057-1065.
Meme PDF source fusionne que fiche_gestion_traitements_chroniques_
cardio_2009.py (Module 1), _douleur_toxico_2009.py (Module 2) et
_neuro_psy_2011.py (Module 4) - voir le docstring du Module 1 pour le
contexte complet du referentiel composite.

PERIMETRE : cette fiche couvre le MODULE 3/4 du referentiel (pages 23-31 du
PDF fusionne, identifiees par lecture complete) - antituberculeux,
antiretroviraux, et 6 immunosuppresseurs distincts (inhibiteurs de
calcineurine [ciclosporine, tacrolimus], thalidomide, methotrexate,
azathioprine, mycophenolate mofetil, cyclophosphamide, anticorps
monoclonaux anti-TNF). Ce module acheve la couverture des 4 modules
effectivement presents dans le PDF fusionne (Cardiovasculaire, Douleur
chronique/toxicomanie, Infectieux/immunosuppresseurs - cette fiche -, et
Neurologique-psychiatrique/phytotherapie) - voir fiche_gestion_
traitements_chroniques_neuro_psy_2011.py pour la note sur le module
"pathologies endocriniennes" annonce par le preambule mais jamais retrouve
dans ce PDF.

METHODOLOGIE : meme grille ANAES 2004 que les modules 1 et 2 - dans ce
module specifiquement, SEULS deux grades apparaissent effectivement dans le
texte : "grade C" (faible niveau de preuve) et "accord fort" (grade D
renforce par methode Delphi, meme convention que les modules 1 et 2) -
aucune citation A, B ou D nu n'a ete trouvee sur les 9 pages source (verifie
par grep exhaustif : 16 citations "accord fort", 16 citations "grade C",
total 32).

DISCLOSURE - consolidation de citations dans le module anti-TNF (section 9,
3 citations grade C, toutes 3 sur la meme scenario clinique) : (a) section
9.1.2 ("risque") enonce que le traitement par infliximab n'est pas associe
a un risque accru de complications postoperatoires en chirurgie colique
(grade C) ; (b) section 9.3 ("strategie") enonce que le traitement pourra
etre poursuivi chez un patient Crohn/RCH en chirurgie colique (grade C) ;
(c) section 9.5 ("reprise du traitement") repete la phrase de (b) EXACTEMENT
MOT POUR MOT. Ces 3 citations, toutes gradees C et decrivant la meme
situation clinique (anti-TNF + chirurgie colique Crohn/RCH), sont
consolidees en UNE seule ligne de tableau ici (jamais fusionnees avec un
grade different - regle 4 -, uniquement des faits de meme grade portant sur
le meme scenario, dont un doublon litteral (b)=(c)).

DECOMPTE (verifie par regex sur le texte source ET sur le script final) :
32 citations de grade source (accord fort:16, grade C:16), consolidees en
30 lignes de recommandations (accord fort:16, grade C:14 - la consolidation
anti-TNF ci-dessus retire 2 lignes du cote grade C) reparties sur 9 classes
therapeutiques : antituberculeux (2 AF), antiretroviraux (4 AF), inhibiteurs
de calcineurine (5C + 2AF), thalidomide (1 AF), methotrexate (3C + 1AF),
azathioprine (3C + 2AF), mycophenolate mofetil (1C + 2AF), cyclophosphamide
(1C + 2AF), anticorps anti-TNF (1C consolide). De nombreux reperes
pratiques non grades (choix d'agents anesthesiques evitant l'hepatotoxicite
pour les antituberculeux, precautions d'isolement respiratoire, interactions
antiretroviraux/cytochrome P450, etc.) sont regroupes par classe sans grade
invente.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from style import *
GRADE_COLORS["C"] = (AMBER, WHITE)
GRADE_COLORS["AF"] = (GREY, WHITE)
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.units import mm

OUT = "/home/user/rfe-sfar-website/output/Fiche_Gestion_Traitements_Chroniques_Infectieux_2009.pdf"

SOURCE_TXT = ("Source : SFAR, « Gestion périopératoire des traitements chroniques et dispositifs "
              "médicaux — Anti-infectieux, immunosuppresseurs », RFE, Ann Fr Anesth Réanim 28 "
              "(2009) 1057-1065 — Module 3/4 uniquement. Fiche de synthèse non officielle : se "
              "référer au texte intégral.")

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

RCW = [30 * mm, CW_FULL - 30 * mm - 15 * mm, 15 * mm]

def context_note_local(txt):
    return P(f"<i>Précision du source :</i> {txt}", S_NOTE)

def legend_flowable():
    chip_w = 16 * mm
    content_w = CW_FULL
    row = Table([[chip("C", width=chip_w - 2 * mm), chip("AF", width=chip_w - 2 * mm),
                  P("<b>Grille ANAES 2004</b> — seuls deux grades apparaissent effectivement dans "
                    "ce module : <b>C</b> : faible niveau de preuve ; <b>AF</b> : accord fort "
                    "(grade D renforcé par méthode Delphi, même convention que les Modules 1 et "
                    "2). Fiche limitée au Module 3/4 du référentiel (anti-infectieux, "
                    "immunosuppresseurs) — voir encadré de périmètre ci-dessous.", S_BADGE_HEAD)]],
                colWidths=[chip_w] * 2 + [content_w - 2 * chip_w])
    row.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                              ("LEFTPADDING", (0, 0), (-1, -1), 1),
                              ("RIGHTPADDING", (0, 0), (-1, -1), 1),
                              ("TOPPADDING", (0, 0), (-1, -1), 0),
                              ("BOTTOMPADDING", (0, 0), (-1, -1), 0)]))
    return row

TOTAL_PAGES = {"n": 5}

def on_page(canvas, doc, page_title):
    header_band(canvas, doc, "SFAR — RFE 2009 (MODULE 3/4 — PÉRIMÈTRE LIMITÉ)",
                "Gestion périopératoire des traitements chroniques — Anti-infectieux, immunosuppresseurs",
                page_title, icon_fn=lambda c, x, y: icon_pill(c, x, y, 13 * mm), color=TEAL_DARK)
    footer_band(canvas, doc, SOURCE_TXT, f"Page {doc.page} / {TOTAL_PAGES['n']}")

# ---------------------------------------------------------------------------
def _section_intro_tuberculeux():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Périmètre limité :</b> le référentiel SFAR complet (2009-2011) comporte 4 modules "
        "(Cardiovasculaire, Douleur chronique/toxicomanie et Neurologique-psychiatrique/"
        "phytothérapie, traités dans des fiches séparées). Cette fiche couvre le Module 3 — "
        "anti-infectieux, immunosuppresseurs.", S_BODY),
        bg=AMBER_LIGHT, border=AMBER))
    story.append(Spacer(1, 2.5 * mm))
    story.append(legend_flowable())
    story.append(Spacer(1, 3 * mm))
    story.append(KeepTogether([
        section_bar("Antituberculeux"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("Antituberculeux", "Poursuivre le traitement instauré aux mêmes posologies et par voie "
         "orale, ainsi que la supplémentation vitaminique associée (B1 et B6).", "AF"),
        ("Antituberculeux", "En cas de nécessité d'interruption prolongée du traitement, une "
         "prise en charge pluridisciplinaire est recommandée.", "AF"),
    ], RCW))
    story.append(Spacer(1, 1.5 * mm))
    story.append(context_note_local(
        "isoniazide/rifampicine/thioamides favorisent une toxicité hépatique ; la rifampicine "
        "est inductrice enzymatique (majorer de 30-50% la posologie des corticoïdes associés) et "
        "peut provoquer une thrombopénie (à écarter avant chirurgie) ; aminosides "
        "potentiellement néphrotoxiques (monitorage rénal) ; surveillance glycémique sous "
        "thioamides. Agents anesthésiques : thiopental proscrit (induction enzymatique majore "
        "l'hépatotoxicité) ; halothane et enflurane contre-indiqués ; propofol, isoflurane, "
        "desflurane et sévoflurane utilisables raisonnablement avec surveillance hépatique "
        "rapprochée. Curares : mivacurium/atracurium/cisatracurium indiqués si atteinte "
        "hépatique (métabolisme indépendant) ; prudence si traitement par aminoside "
        "(potentialisation du bloc). Isolement respiratoire obligatoire si traitement "
        "< 15 jours (circulaire DGS/VS-DH n° 69 du 29/10/1993) ; BK tubage en urgence au-delà. "
        "Éviter les fortes doses de paracétamol. Relais IV possible pour isoniazide, éthambutol "
        "et rifampicine uniquement ; avis spécialisé indispensable pour les autres molécules "
        "(guidé par l'antibiogramme). Adaptations posologiques en cas d'insuffisance rénale "
        "(clairance < 30 ml/min) et de toxicité hépatique (paliers selon les transaminases) "
        "détaillées dans le texte source."))
    return story

# ---------------------------------------------------------------------------
def _section_antiretroviraux():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Antirétroviraux"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("Antirétroviraux", "En raison de l'importance de l'observance, les arrêts de "
         "traitement doivent être évités en période périopératoire.", "AF"),
        ("Antirétroviraux", "Toute interruption non évitable (jeûne préopératoire) sera la "
         "plus courte possible, au plus 48 heures maximum.", "AF"),
        ("Antirétroviraux", "En cas d'arrêt, tous les antirétroviraux doivent être interrompus "
         "et repris simultanément (éviter une monothérapie, source de résistance virale).", "AF"),
        ("Antirétroviraux", "Tout arrêt de traitement doit faire l'objet d'un avis spécialisé.", "AF"),
    ], RCW))
    story.append(Spacer(1, 1.5 * mm))
    story.append(context_note_local(
        "les inhibiteurs de protéase (IP) nécessitent une prise alimentaire concomitante, "
        "incompatible avec le jeûne préopératoire. Rifampicine contre-indiquée avec les IP non "
        "associés au ritonavir (monitorage thérapeutique obligatoire si nécessité impérative). "
        "Risque d'acutisation d'une hépatite B chronique à l'arrêt prolongé d'un antirétroviral "
        "actif sur ce virus (lamivudine, ténofovir, emtricitabine). Interactions via les "
        "cytochromes P450 (CYP2B6, CYP3A4) avec de nombreux médicaments d'anesthésie ; "
        "midazolam potentiellement majoré (dépression respiratoire, somnolence). Neuropathie "
        "sous INTI (ex. didanosine) à prendre en compte pour l'ALR périnerveuse. En "
        "réanimation prolongée : monitorage thérapeutique nécessaire (absence de forme "
        "injectable pour la plupart des molécules, altération de l'absorption digestive)."))
    return story

# ---------------------------------------------------------------------------
def _section_calcineurine_thalidomide():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Inhibiteurs de calcineurine (ciclosporine, tacrolimus)"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("Inhib. calcineurine", "La poursuite de l'immunosuppression peut s'accompagner d'un "
         "risque plus élevé d'infections postopératoires.", "C"),
        ("Inhib. calcineurine", "Monitorage indispensable (et possible diminution des doses) "
         "des curares non dépolarisants — la ciclosporine peut augmenter l'intensité et la "
         "durée de la curarisation.", "C"),
        ("Inhib. calcineurine", "Le midazolam et la lidocaïne diminueraient le métabolisme du "
         "tacrolimus.", "C"),
        ("Inhib. calcineurine", "De grandes modifications des taux sanguins sont possibles en "
         "cas de remplissage massif périopératoire ou de circulation extracorporelle.", "C"),
        ("Inhib. calcineurine", "Surveiller les taux plasmatiques et la fonction rénale en "
         "concertation avec le spécialiste en charge de l'immunosuppression du patient.", "AF"),
        ("Inhib. calcineurine", "La reprise précoce du traitement est nécessaire (voie orale ou "
         "intraveineuse selon la situation).", "AF"),
        ("Inhib. calcineurine", "Si la voie entérale est compromise, il est possible "
         "d'administrer le traitement par voie intraveineuse.", "C"),
    ], RCW))
    story.append(Spacer(1, 1.5 * mm))
    story.append(context_note_local(
        "ne pas donner la ciclosporine le matin de l'intervention en cas d'AG (le tacrolimus "
        "peut être poursuivi par voie sublinguale) ; éviter les AINS (potentiel néphrotoxique en "
        "association) ; monitorage des taux indispensable quelle que soit la technique "
        "d'anesthésie (C2 pour la ciclosporine, taux résiduel pour le tacrolimus)."))
    story.append(Spacer(1, 3 * mm))
    story.append(KeepTogether([
        section_bar("Thalidomide"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("Thalidomide", "Ne pas interrompre la thalidomide, en tenant compte de la fréquence "
         "des neuropathies et du risque de maladie thromboembolique veineuse.", "AF"),
    ], RCW))
    story.append(Spacer(1, 1.5 * mm))
    story.append(context_note_local(
        "évaluation précise d'une éventuelle neuropathie périphérique avant toute ALR (touche "
        "en particulier les nerfs saphènes externes et médians, peut persister après l'arrêt) ; "
        "prévention efficace du risque thromboembolique veineux périopératoire."))
    return story

# ---------------------------------------------------------------------------
def _section_methotrexate_azathioprine():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Méthotrexate"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("Méthotrexate", "Une toxicité médullaire et muqueuse est fortement suspectée en "
         "présence de protoxyde d'azote.", "C"),
        ("Méthotrexate", "Les AINS sont contre-indiqués pour l'analgésie (potentialisation de "
         "la toxicité hématologique et rénale).", "C"),
        ("Méthotrexate", "Ne pas interrompre le traitement, en tenant compte de la toxicité "
         "hématologique et rénale, en particulier en association avec le protoxyde d'azote ou "
         "les AINS en périopératoire.", "AF"),
        ("Méthotrexate", "En cas de maintien ou de reprise précoce, il est conseillé de ne pas "
         "utiliser de protoxyde d'azote durant l'anesthésie.", "C"),
    ], RCW))
    story.append(Spacer(1, 3 * mm))
    story.append(KeepTogether([
        section_bar("Azathioprine"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("Azathioprine", "Le taux d'infection postopératoire après induction de "
         "l'immunosuppression pour transplantation n'est pas élevé.", "C"),
        ("Azathioprine", "Dans le contexte de la chirurgie colique, le maintien n'est pas "
         "associé à un risque accru de complications postopératoires.", "C"),
        ("Azathioprine", "La posologie de curare semble pouvoir être identique à celle "
         "utilisée chez le sujet sain, malgré une diminution de leur effet par l'azathioprine.", "C"),
        ("Azathioprine", "Administrer le traitement avec la prémédication.", "AF"),
        ("Azathioprine", "En cas d'interruption prolongée, se concerter avec le spécialiste "
         "prenant en charge le patient pour ce traitement.", "AF"),
    ], RCW))
    return story

# ---------------------------------------------------------------------------
def _section_mycophenolate_cyclophosphamide_antitnf():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Mycophénolate mofétil"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("Mycophénolate", "Administrer le traitement avec la prémédication.", "AF"),
        ("Mycophénolate", "En cas d'interruption prolongée, se concerter avec le spécialiste "
         "prenant en charge le patient pour ce traitement.", "AF"),
        ("Mycophénolate", "Il n'y a pas d'intérêt au dosage de la molécule pour le suivi "
         "thérapeutique ou l'adaptation posologique.", "C"),
    ], RCW))
    story.append(Spacer(1, 3 * mm))
    story.append(KeepTogether([
        section_bar("Cyclophosphamide"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("Cyclophosphamide", "L'effet des curares dépolarisants peut être prolongé chez les "
         "patients ayant reçu du cyclophosphamide, même à distance de la prise.", "C"),
        ("Cyclophosphamide", "Administrer le traitement avec la prémédication.", "AF"),
        ("Cyclophosphamide", "En cas d'interruption prolongée, se concerter avec le spécialiste "
         "prenant en charge le patient pour ce traitement.", "AF"),
    ], RCW))
    story.append(Spacer(1, 3 * mm))
    story.append(KeepTogether([
        section_bar("Anticorps monoclonaux anti-TNF (infliximab, adalimumab, étanercept)"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("Anti-TNF", "Dans le contexte de la chirurgie colique (maladie de Crohn ou RCH), le "
         "traitement n'est pas associé à un risque accru de complications postopératoires et "
         "pourra être poursuivi.", "C"),
    ], RCW))
    story.append(Spacer(1, 1.5 * mm))
    story.append(context_note_local(
        "compte tenu du risque potentiel de sepsis et de la demi-vie longue de ces traitements, "
        "il est conseillé de les arrêter une semaine avant une chirurgie programmée (hors "
        "contexte Crohn/RCH ci-dessus) ; reprise possible la semaine suivant l'intervention en "
        "l'absence de complication."))
    return story

# ---------------------------------------------------------------------------
def _section_sources():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("Sources et avertissement", color=GREY))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>Document source :</b> Société française d'anesthésie et de réanimation (SFAR), "
        "« Gestion périopératoire des traitements chroniques et dispositifs médicaux — "
        "Anti-infectieux, immunosuppresseurs », Recommandations Formalisées d'Experts, Annales "
        "Françaises d'Anesthésie et de Réanimation 28 (2009) 1057-1065.", S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>URL source :</b> https://sfar.org/gestion-perioperatoire-des-traitements-chroniques-"
        "et-dispositifs-medicaux-anti-infectieux-immunosuppresseurs/", S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>Couverture :</b> Module 3/4 du référentiel uniquement (anti-infectieux, "
        "immunosuppresseurs) — 30 lignes de recommandations gradées (accord fort:16, grade "
        "C:14 ; consolidation de 3 citations de même grade sur le même scénario clinique dans "
        "le module anti-TNF, dont une phrase source dupliquée mot pour mot). Ce module achève "
        "la couverture des 4 modules effectivement présents dans le "
        "PDF fusionné de ce référentiel (Cardiovasculaire, Douleur chronique/toxicomanie et "
        "Neurologique-psychiatrique/phytothérapie, traités dans des fiches séparées). "
        "Argumentaire scientifique détaillé (document source complet) non reproduit.", S_SOURCE))
    story.append(Spacer(1, 2 * mm))
    story.append(info_panel(P(
        "<b>Avertissement :</b> cette fiche est une synthèse indépendante et PARTIELLE "
        "(Module 3 uniquement). Elle ne remplace pas le texte intégral. Cette fiche n'est ni "
        "éditée ni validée par la SFAR.", S_BODY_SM), bg=GREY_LIGHT, border=GREY))
    return story

# ---------------------------------------------------------------------------
def _section_tuberculeux_retroviraux():
    story = _section_intro_tuberculeux()
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_antiretroviraux())
    return story

def _section_calcineurine_thalidomide_methotrexate_azathioprine():
    story = _section_calcineurine_thalidomide()
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_methotrexate_azathioprine())
    return story

def _section_mycophenolate_cyclophosphamide_antitnf_sources():
    story = _section_mycophenolate_cyclophosphamide_antitnf()
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_sources())
    return story

def _section_calcineurine_through_sources():
    story = _section_calcineurine_thalidomide_methotrexate_azathioprine()
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_mycophenolate_cyclophosphamide_antitnf_sources())
    return story

SECTIONS = [
    ("Antituberculeux & antirétroviraux", _section_tuberculeux_retroviraux),
    ("Immunosuppresseurs & sources", _section_calcineurine_through_sources),
]

def _make_doc(path=None):
    return SimpleDocTemplate(path or OUT, pagesize=A4,
                              leftMargin=MARGIN, rightMargin=MARGIN,
                              topMargin=32 * mm, bottomMargin=16 * mm,
                              title="Fiche SFAR 2009 - Gestion traitements chroniques (Module 3 - Infectieux/Immunosuppresseurs)",
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
