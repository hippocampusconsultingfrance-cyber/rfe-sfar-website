# -*- coding: utf-8 -*-
"""
Fiche de synthese - "Gestion perioperatoire des traitements chroniques et
dispositifs medicaux. Pathologies neurologiques et psychiatriques" (+
"Phytotherapie", texte court distinct mais bundled dans le meme PDF source)
- Recommandations Formalisees d'Experts (RFE), SFAR, Ann Fr Anesth Reanim 30
(2011) 191-194 et 200. Meme PDF source fusionne que fiche_gestion_
traitements_chroniques_cardio_2009.py (Module 1) et fiche_gestion_
traitements_chroniques_douleur_toxico_2009.py (Module 2) - voir le
docstring du Module 1 pour le contexte complet du referentiel composite.

PERIMETRE : cette fiche couvre le MODULE 4 du referentiel (pages 32-36 du
PDF fusionne, identifiees par lecture complete) - antiparkinsoniens,
antidepresseurs (dont sous-section IMAO dediee), ET un texte court distinct
sur la phytotherapie (meme auteur/responsable - Pr Christophe Baillard -
publie a la suite immediate dans le meme PDF sous une pagination Ann Fr
Anesth Reanim differente [30 (2011) 200], bundled dans cette fiche plutot
qu'une fiche separee vu sa taille tres reduite - moins d'une page source).
Le Module 3 (Infectieux/immunosuppresseurs, pages 23-31) n'est PAS couvert
ici - disclosed explicitement, a construire separement. Note : le Preambule
du referentiel (voir Module 1) annoncait un module "pathologies
endocriniennes" qui n'apparait dans AUCUNE des 36 pages de ce PDF fusionne
- probablement jamais publie sous cette forme, ou publie ailleurs hors de
ce telechargement ; ce module reste donc absent de ce corpus, sans qu'on
puisse le construire faute de source identifiee.

METHODOLOGIE - DIVERGENCE DISCLOSED PAR RAPPORT AUX MODULES 1 ET 2 : ce
module (publie 2011, groupe de travail different - Pr Christophe Baillard
et al., distinct du Module 1's Pr Piriou/Samain et du Module 2's Pr
Fletcher/Keita-Meyer) utilise EFFECTIVEMENT la grille ANAES A/B/C/D complete
SANS renforcement systematique du grade D en "accord fort" par methode
Delphi - contrairement aux modules 1 et 2 ou SEUL "accord fort" apparaissait
jamais pour le grade D. Ici, "grade D" (avis d'expert) ET "accord fort"
coexistent comme DEUX notations distinctes dans le meme texte, non
interchangeables - chip local "D" (nouvelle couleur, distincte du chip "AF"
deja utilise) ajoute pour ce module uniquement. DEUXIEME DIVERGENCE : une
citation source imprime explicitement un grade hesitant "(grade B ou C)"
(association imipraminique-anticholinergique) - conformement a la regle 5
(jamais resoudre silencieusement une incertitude du source), cette citation
est reproduite telle quelle avec un chip local "B/C" neutre, sans trancher
arbitrairement en faveur de B ou de C.

DECOMPTE (verifie par regex sur le script final, pas seulement estime a la
lecture) : Antiparkinsoniens 3 items (AF:3) ; Antidepresseurs hors IMAO 14
items (A:2, B:4, C:4, AF:3, B/C:1 - la citation hesitante) ; IMAO
(sous-section dediee) 8 items (AF:2, D:4, A:1, C:1) ; Phytotherapie 2 items
(C:1, B:1) + reperes pratiques non grades par plante (echinacee, ephedra,
ail, ginkgo, millepertuis). Total : 27 lignes de recommandations/reperes
grades sur les 4 sections (A:3, B:5, C:6, D:4, AF:8, B/C:1).
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from style import *
GRADE_COLORS["A"] = (GREEN, WHITE)
GRADE_COLORS["B"] = (TEAL, WHITE)
GRADE_COLORS["C"] = (AMBER, WHITE)
GRADE_COLORS["D"] = (NAVY, WHITE)
GRADE_COLORS["AF"] = (GREY, WHITE)
GRADE_COLORS["B/C"] = (GREY_LIGHT, INK)
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.units import mm

OUT = "/home/user/rfe-sfar-website/output/Fiche_Gestion_Traitements_Chroniques_Neuro_Psy_2011.pdf"

SOURCE_TXT = ("Source : SFAR, « Gestion périopératoire des traitements chroniques et dispositifs "
              "médicaux — Pathologies neurologiques et psychiatriques » + « Phytothérapie », RFE, "
              "Ann Fr Anesth Réanim 30 (2011) 191-194 et 200 — Module 4/4 uniquement. Fiche de "
              "synthèse non officielle : se référer au texte intégral.")

def P(txt, style=S_CELL):
    return Paragraph(txt, style)

def chip(label, **kw):
    return grade_chip(label, **kw)

CW_FULL = PAGE_W - 2 * MARGIN

def reco_table(rows, col_widths):
    """rows: (ref, text, grade_label)."""
    data = [[P("Classe", S_HEAD_W), P("Recommandation", S_HEAD_W), P("Grade", S_HEAD_W_C)]]
    for ref, txt, grade in rows:
        data.append([P(ref, S_CELL_B), P(txt, S_CELL), chip(grade, width=16 * mm)])
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

RCW = [32 * mm, CW_FULL - 32 * mm - 16 * mm, 16 * mm]

def context_note_local(txt):
    return P(f"<i>Précision du source :</i> {txt}", S_NOTE)

def practical_block(title, txt):
    return P(f"<b>{title}</b> <i>(repère non gradé par la source)</i> : {txt}", S_BODY_SM)

def legend_flowable():
    chip_w = 14 * mm
    content_w = CW_FULL
    row = Table([[chip("A", width=chip_w - 2 * mm), chip("B", width=chip_w - 2 * mm),
                  chip("C", width=chip_w - 2 * mm), chip("D", width=chip_w - 2 * mm),
                  chip("AF", width=chip_w - 2 * mm), chip("B/C", width=chip_w - 2 * mm),
                  P("<b>Grille ANAES 2004</b> — <b>A</b> : preuve établie ; <b>B</b> : présomption "
                    "scientifique ; <b>C</b> : faible niveau de preuve ; <b>D</b> : avis d'expert "
                    "(distinct d'« accord fort » dans CE module — divergence disclosed, voir "
                    "encadré ci-dessous) ; <b>AF</b> : accord fort ; <b>B/C</b> : incertitude de "
                    "grade imprimée telle quelle par la source elle-même (jamais tranchée "
                    "arbitrairement). Fiche limitée au Module 4/4 du référentiel.", S_BADGE_HEAD)]],
                colWidths=[chip_w] * 6 + [content_w - 6 * chip_w])
    row.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                              ("LEFTPADDING", (0, 0), (-1, -1), 1),
                              ("RIGHTPADDING", (0, 0), (-1, -1), 1),
                              ("TOPPADDING", (0, 0), (-1, -1), 0),
                              ("BOTTOMPADDING", (0, 0), (-1, -1), 0)]))
    return row

TOTAL_PAGES = {"n": 4}

def on_page(canvas, doc, page_title):
    header_band(canvas, doc, "SFAR — RFE 2011 (MODULE 4/4 — PÉRIMÈTRE LIMITÉ)",
                "Gestion périopératoire des traitements chroniques — Neuro/psychiatrique & phytothérapie",
                page_title, icon_fn=lambda c, x, y: icon_pill(c, x, y, 13 * mm), color=TEAL_DARK)
    footer_band(canvas, doc, SOURCE_TXT, f"Page {doc.page} / {TOTAL_PAGES['n']}")

# ---------------------------------------------------------------------------
def _section_intro_parkinson():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Périmètre limité :</b> le référentiel SFAR complet (2009-2011) comporte plusieurs "
        "modules (Cardiovasculaire et Douleur chronique/toxicomanie, déjà traités dans des "
        "fiches séparées ; Infectieux/immunosuppresseurs, non traité ici). Cette fiche couvre le "
        "Module 4 — Pathologies neurologiques et psychiatriques, avec le texte court "
        "« Phytothérapie » publié à la suite dans le même document. Un module « pathologies "
        "endocriniennes » était annoncé par le préambule du référentiel mais n'apparaît dans "
        "aucune page du PDF source téléchargé — probablement non publié sous cette forme ou "
        "publié ailleurs ; il reste donc absent de ce corpus.", S_BODY),
        bg=AMBER_LIGHT, border=AMBER))
    story.append(Spacer(1, 2 * mm))
    story.append(info_panel(P(
        "<b>Divergence méthodologique disclosed :</b> contrairement aux Modules 1 et 2 de ce "
        "référentiel (où le grade D n'apparaissait jamais autrement que relabellisé « accord "
        "fort »), ce Module 4 utilise « grade D » et « accord fort » comme DEUX notations "
        "distinctes et non interchangeables — reproduites ici avec deux chips séparés (D / AF), "
        "sans les fusionner.", S_BODY_SM), bg=GREY_LIGHT, border=GREY))
    story.append(Spacer(1, 2.5 * mm))
    story.append(legend_flowable())
    story.append(Spacer(1, 3 * mm))
    story.append(KeepTogether([
        section_bar("Antiparkinsoniens"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("Antiparkinsoniens", "Ne pas arrêter le traitement antiparkinsonien en périopératoire — "
         "maintenir exactement le schéma habituel du patient jusqu'à l'intervention.", "AF"),
        ("Antiparkinsoniens", "Ne pas arrêter un stimulateur cérébral profond — appliquer les "
         "mêmes précautions périopératoires que pour un stimulateur cardiaque.", "AF"),
        ("Antiparkinsoniens", "Prévoir une stratégie de substitution en cas d'indisponibilité de "
         "la voie orale/digestive (Modopar® dispersible par sonde gastrique toutes les 2h à dose "
         "équivalente en dopa ; Apokinon® sous-cutané selon protocole/titration ; dompéridone "
         "pour ses propriétés prokinétiques et antidopaminergiques périphériques).", "AF"),
    ], RCW))
    story.append(Spacer(1, 1.5 * mm))
    story.append(context_note_local(
        "l'ALR permet le maintien du traitement antiparkinsonien tout au long de la période "
        "périopératoire. Dropéridol contre-indiqué en cas de vomissements ; neuroleptiques "
        "classiques (halopéridol, loxapine) contre-indiqués en cas de troubles psychiatriques "
        "(hydroxyzine et benzodiazépines utilisables). En cas de troubles psychiatriques, "
        "ajuster en arrêtant/diminuant dans l'ordre : anticholinergiques, amantadine, sélégiline, "
        "agonistes dopaminergiques, puis L-dopa en dernier recours (clozapine en ultime recours, "
        "risque d'agranulocytose)."))
    return story

# ---------------------------------------------------------------------------
def _section_antidepresseurs():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Antidépresseurs — risque, interactions & stratégie générale"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("Antidépresseurs", "L'arrêt brutal expose à un risque de récidive symptomatique de "
         "dépression.", "A"),
        ("Antidépresseurs", "En l'absence de décroissance progressive, un syndrome de sevrage "
         "peut apparaître (4 à 8 jours) ; il cède à la reprise du traitement à la dose "
         "antérieure.", "A"),
        ("Antidépresseurs", "Maintenir les antidépresseurs jusqu'au matin de l'intervention et "
         "les reprendre précocement.", "AF"),
        ("Antidépresseurs", "Le syndrome anticholinergique doit être recherché devant des signes "
         "spécifiques : muqueuses sèches, érythème cutané, peau sèche au toucher, mydriase, "
         "absence de bruits intestinaux.", "C"),
        ("Antidépresseurs", "L'association d'un imipraminique à un médicament à action "
         "anticholinergique peut provoquer un syndrome anticholinergique.", "B/C"),
        ("Antidépresseurs", "Le syndrome sérotoninergique doit être recherché devant des signes "
         "spécifiques : hypersialorrhée, sueurs profuses, bruits intestinaux importants, "
         "hyperréflexie, clonus, rigidité musculaire.", "B"),
        ("Antidépresseurs", "L'association d'un IMAO, ISRS, IRSN ou ATD de mécanisme différent à "
         "la péthidine, au fentanyl ou au tramadol peut provoquer un syndrome sérotoninergique.", "C"),
        ("Antidépresseurs", "L'association d'un ATD au linézolide peut provoquer un syndrome "
         "sérotoninergique.", "B"),
        ("Antidépresseurs", "Le risque d'interactions médicamenteuses peropératoires avec les "
         "imipraminiques pour les conséquences cardiovasculaires apparaît faible.", "B"),
        ("Antidépresseurs", "Le rôle des imipraminiques dans la confusion postopératoire existe, "
         "mais est sans doute sous-estimé.", "C"),
        ("Antidépresseurs", "Les imipraminiques peuvent être maintenus en périopératoire chez les "
         "patients ASA I-II indemnes de pathologie cardiovasculaire.", "AF"),
        ("Antidépresseurs", "Il est souhaitable d'interrompre les imipraminiques chez les "
         "patients avec pathologie cardiovasculaire (interaction possible imipraminiques/terrain "
         "CV/anesthésie).", "AF"),
        ("Antidépresseurs", "Les autres morphiniques que la péthidine, le fentanyl et le tramadol "
         "sont utilisables sans risque majoré de syndrome sérotoninergique.", "B"),
        ("Antidépresseurs", "Le linézolide peut être utilisé si nécessaire chez un patient sous "
         "ISRS, sous surveillance clinique étroite et avec arrêt de l'ISRS à la moindre "
         "suspicion de syndrome sérotoninergique.", "C"),
    ], RCW))
    story.append(Spacer(1, 1.5 * mm))
    story.append(context_note_local(
        "en cas de relais nécessaire (imipraminiques interrompus), la substitution immédiate sur "
        "avis psychiatrique dès la consultation préopératoire, le traitement des modifications "
        "hémodynamiques (remplissage puis éphédrine titrée puis noradrénaline si échec), la "
        "recherche systématique des signes de syndrome anticholinergique/sérotoninergique devant "
        "une confusion postopératoire, et la discussion de l'association aux antiplaquettaires "
        "(aspirine) en cas de chirurgie à risque hémorragique élevé, sont toutes gradées D par la "
        "source (avis d'expert, distinct d'« accord fort » dans ce module)."))
    return story

# ---------------------------------------------------------------------------
def _section_imao_phyto():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Antidépresseurs — IMAO (sous-section dédiée)"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("IMAO ancienne gén.", "Un traitement par IMAO ancienne génération (iproniazide) doit "
         "être maintenu avec une discussion pluridisciplinaire si le risque de décompensation "
         "psychiatrique apparaît important.", "AF"),
        ("IMAO ancienne gén.", "Si maintenu, éviter la péthidine, le fentanyl et le tramadol "
         "(autres morphiniques utilisables).", "D"),
        ("IMAO ancienne gén.", "Si suspendu, l'arrêter au moins 2 semaines avant l'intervention "
         "(mécanisme d'action du médicament).", "A"),
        ("IMAO ancienne gén.", "Un relais avec un autre antidépresseur peut être proposé en "
         "accord avec un psychiatre.", "D"),
        ("IMAO nouvelle gén.", "Un traitement par IMAO nouvelle génération (moclobémide) peut "
         "être maintenu en période périopératoire.", "AF"),
        ("IMAO nouvelle gén.", "Éviter, de principe, la péthidine, le fentanyl et le tramadol "
         "(autres morphiniques utilisables).", "D"),
        ("IMAO nouvelle gén.", "Toute hypotension artérielle peropératoire doit être traitée par "
         "remplissage vasculaire en première intention ; utilisation prudente des vasopresseurs "
         "possible par titration en commençant au tiers de la dose habituelle.", "C"),
        ("IMAO (tous)", "Un syndrome sérotoninergique est favorisé par l'association aux ISRS, "
         "IRSN et, à moindre degré, aux autres antidépresseurs — association à éviter en "
         "période périopératoire.", "D"),
    ], RCW))
    story.append(Spacer(1, 3 * mm))
    story.append(KeepTogether([
        section_bar("Phytothérapie"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("Phytothérapie", "Rechercher en consultation d'anesthésie l'adhésion du patient à une "
         "phytothérapie — elle n'est pas spontanément révélée.", "C"),
        ("Phytothérapie", "La prescription d'extraits de plantes favorise des anomalies "
         "préopératoires (coagulation, hypokaliémie) pouvant nécessiter des mesures "
         "correctrices ou une modification du protocole anesthésique.", "B"),
    ], RCW))
    story.append(Spacer(1, 1.5 * mm))
    story.append(context_note_local(
        "si les extraits consommés ne sont pas précisément connus, la prudence est d'interrompre "
        "la phytothérapie une dizaine de jours avant l'anesthésie ; sinon, l'attitude peut être "
        "adaptée à l'extrait :"))
    story.append(Spacer(1, 1 * mm))
    story.append(practical_block("Échinacée",
        "interrompre le plus précocement possible chez les patients avec maladie auto-immune, "
        "sous corticoïde/immunosuppresseur, ou en attente de transplantation (propriétés "
        "immunostimulantes)."))
    story.append(Spacer(1, 1 * mm))
    story.append(practical_block("Éphédra", "interruption conseillée 24 heures avant l'anesthésie."))
    story.append(Spacer(1, 1 * mm))
    story.append(practical_block("Ail",
        "interruption 10 jours avant si l'on souhaite éviter l'effet antiagrégant plaquettaire "
        "(délai de renouvellement plaquettaire)."))
    story.append(Spacer(1, 1 * mm))
    story.append(practical_block("Ginkgo", "interruption d'au moins 36 heures (effet antiagrégant)."))
    story.append(Spacer(1, 1 * mm))
    story.append(practical_block("Millepertuis",
        "interruption d'au moins 5 jours si l'on souhaite s'affranchir des effets résiduels "
        "(induction du système des cytochromes P-450, réduction d'efficacité des médicaments "
        "utilisant ce système)."))
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
        "Pathologies neurologiques et psychiatriques » et « Phytothérapie », Recommandations "
        "Formalisées d'Experts, Annales Françaises d'Anesthésie et de Réanimation 30 (2011) "
        "191-194 et 200.", S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>URL source :</b> https://sfar.org/gestion-perioperatoire-des-traitements-chroniques-"
        "et-dispositifs-medicaux-anti-infectieux-immunosuppresseurs/", S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>Couverture :</b> Module 4/4 du référentiel uniquement (pathologies neurologiques et "
        "psychiatriques + phytothérapie) — 27 lignes de recommandations/repères gradés (A:3, "
        "B:5, C:6, D:4, accord fort:8, B/C:1). Le Module 3 (Infectieux/immunosuppresseurs) n'est "
        "pas couvert ici — hors périmètre de cette fiche, disclosed en page 1. Un module "
        "« pathologies endocriniennes » annoncé par le préambule du référentiel n'a pas été "
        "retrouvé dans le PDF source. Argumentaire scientifique détaillé (document source "
        "complet) non reproduit.", S_SOURCE))
    story.append(Spacer(1, 2 * mm))
    story.append(info_panel(P(
        "<b>Avertissement :</b> cette fiche est une synthèse indépendante et PARTIELLE "
        "(Module 4 uniquement). Elle ne remplace pas le texte intégral — en particulier pour "
        "toute question relevant du Module 3 de ce référentiel. Cette fiche n'est ni éditée ni "
        "validée par la SFAR.", S_BODY_SM), bg=GREY_LIGHT, border=GREY))
    return story

# ---------------------------------------------------------------------------
SECTIONS = [
    ("Antiparkinsoniens", _section_intro_parkinson),
    ("Antidépresseurs — risque, interactions & stratégie générale", _section_antidepresseurs),
    ("Antidépresseurs (IMAO) & phytothérapie", _section_imao_phyto),
    ("Sources", _section_sources),
]

def _make_doc(path=None):
    return SimpleDocTemplate(path or OUT, pagesize=A4,
                              leftMargin=MARGIN, rightMargin=MARGIN,
                              topMargin=32 * mm, bottomMargin=16 * mm,
                              title="Fiche SFAR 2011 - Gestion traitements chroniques (Module 4 - Neuro/Psy & Phytotherapie)",
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
