# -*- coding: utf-8 -*-
"""
Fiche de synthese - Conference de consensus "Les traumatises craniens
adultes en medecine physique et readaptation : du coma a l'eveil" (texte
court des recommandations du jury), SOFMER, 8 octobre 2001, organisee selon
les regles methodologiques ANAES. Publie Ann Readapt Med Phys 45 (2002)
417-423. 7 pages, telecharge depuis sfar.org (wp-content/uploads/2015/10/
Annales-de-Readaptation-et-de-Medecine-Physique_Les-traumatises-craniens-
adultes-en-medecine-physique-et-readaptation.pdf).

METHODOLOGIE : DEUX grilles A/B/C DIFFERENTES sont utilisees selon la
question traitee (meme piege que fiche_ivg_14sa.py : ne pas confondre des
grilles A/B/C differentes entre documents OU, ici, AU SEIN D'UN MEME
DOCUMENT) - Tableau 1 (Questions 3 et 4, efficacite/tolerance des
traitements, echelle Canadian Task Force on Periodic Health : A = essai
comparatif/meta-analyse ; B = essais non randomises/petits essais ; C =
etudes de cohorte/cas-temoins/series non contemporaines/etudes
descriptives/avis d'experts) ; Tableau 2 (Questions 1 et 2, etudes
pronostiques/de validation d'echelle : A = etude bien menee ; B = etude
avec imperfections methodologiques ; C = etude de qualite mediocre/
descriptive/avis d'experts). Un chip unique A/B/C est utilise ici (la
distinction fine des deux echelles est disclosed en methodologie, sans
recreer deux jeux de chips visuellement identiques). Deux categories
supplementaires, distinctes l'une de l'autre selon le texte source
lui-meme : "avis d'experts" (chip AE - au sein du grade C/niveau III,
mais identifie separement dans le texte) et "accord professionnel" (chip
AP - enonce SANS AUCUNE publication dans la litterature, distinct de AE).

PERIMETRE ET NUMEROTATION : le texte source ne numerote PAS ses
recommandations (contrairement a la plupart des RFE/RPC de ce corpus) -
une numerotation sequentielle par question (Q1.1, Q1.2...) est ASSIGNEE ICI
pour la seule commodite de reference dans le tableau, et disclosed comme
telle (non native au texte source) dans la fiche. Integral sur les 4
questions du jury. La liste nominative des experts/jury/comite (pages 1-2
du PDF source) n'est pas transcrite (renvoi au texte integral).
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from style import *
GRADE_COLORS["A"] = (GREEN, WHITE)
GRADE_COLORS["B"] = (TEAL, WHITE)
GRADE_COLORS["C"] = (AMBER, WHITE)
GRADE_COLORS["AP"] = (NAVY, WHITE)
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.units import mm

OUT = "/home/user/rfe-sfar-website/output/Fiche_SOFMER_TC_Readaptation_Coma_Eveil_2001.pdf"

SOURCE_TXT = ("Source : SOFMER, Conférence de consensus « Les traumatisés crâniens adultes en "
              "médecine physique et réadaptation : du coma à l'éveil », 8 octobre 2001, Ann "
              "Readapt Med Phys 45 (2002) 417-423. Fiche de synthèse non officielle : se référer "
              "au texte intégral.")

def P(txt, style=S_CELL):
    return Paragraph(txt, style)

def chip(label, **kw):
    return grade_chip(label, **kw)

CW_FULL = PAGE_W - 2 * MARGIN

def reco_table(rows, col_widths):
    """rows: (ref, text, grade_label)."""
    data = [[P("Réf.*", S_HEAD_W), P("Constat / recommandation", S_HEAD_W), P("Niveau", S_HEAD_W_C)]]
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

RCW = [16 * mm, CW_FULL - 16 * mm - 18 * mm, 18 * mm]

def bullets(items, style=S_BODY_SM):
    html = "&bull; " + "<br/>&bull; ".join(items)
    return P(html, style)

def legend_flowable():
    chip_w = 15 * mm
    content_w = CW_FULL
    row = Table([[chip("A", width=chip_w - 2 * mm), chip("B", width=chip_w - 2 * mm),
                  chip("C", width=chip_w - 2 * mm), chip("AE", width=chip_w - 2 * mm),
                  chip("AP", width=chip_w - 2 * mm),
                  P("<b>A/B/C</b> — niveau de preuve, deux échelles distinctes selon la question "
                    "(voir méthodologie) ; <b>AE</b> = avis d'experts (au sein du niveau C/III, "
                    "identifié séparément par la source) ; <b>AP</b> = accord professionnel "
                    "(énoncé sans aucune publication dans la littérature — distinct de AE).",
                    S_BADGE_HEAD)]],
                colWidths=[chip_w] * 5 + [content_w - 5 * chip_w])
    row.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                              ("LEFTPADDING", (0, 0), (-1, -1), 1),
                              ("RIGHTPADDING", (0, 0), (-1, -1), 1),
                              ("TOPPADDING", (0, 0), (-1, -1), 0),
                              ("BOTTOMPADDING", (0, 0), (-1, -1), 0)]))
    return row

TOTAL_PAGES = {"n": 5}

def on_page(canvas, doc, page_title):
    header_band(canvas, doc, "SOFMER — CONFÉRENCE DE CONSENSUS, 2001",
                "Traumatisés crâniens : du coma à l'éveil (MPR)",
                page_title, icon_fn=lambda c, x, y: icon_shield(c, x, y, 13 * mm), color=TEAL_DARK)
    footer_band(canvas, doc, SOURCE_TXT, f"Page {doc.page} / {TOTAL_PAGES['n']}")

# ---------------------------------------------------------------------------
def _section_intro():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Résumé :</b> 12 000 traumatisés crâniens graves (TCG) meurent chaque année en "
        "France, 8-10 000 gardent des séquelles, 1 800 perdent leur autonomie (les trois "
        "quarts ont moins "
        "de 30 ans, accidents de la route). Entre le coma et la rééducation, le "
        "« passage » pose problème : pronostic mal établi, isolement des soignants, place "
        "incertaine de la famille, discontinuité des soins. Cette conférence de consensus "
        "SOFMER traite 4 questions : définition clinique du passage coma → éveil, apport "
        "des examens complémentaires, traitements médicamenteux, procédures de "
        "rééducation.", S_BODY), bg=BG_PANEL, border=TEAL))
    story.append(Spacer(1, 2.5 * mm))
    story.append(section_bar("Méthodologie — deux échelles A/B/C distinctes"))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>Questions 3 et 4</b> (efficacité/tolérance des traitements) : échelle Canadian "
        "Task Force on Periodic Health — <b>A</b> = essai comparatif ou méta-analyse "
        "d'essais randomisés ; <b>B</b> = essais non randomisés ou petits essais ; "
        "<b>C</b> = études de cohorte/cas-témoins, comparaisons de séries non "
        "contemporaines, études descriptives ou avis d'experts. <b>Questions 1 et 2</b> "
        "(études pronostiques/de validation d'échelle) : <b>A</b> = étude pronostique/de "
        "validation bien menée ; <b>B</b> = étude avec imperfections méthodologiques ; "
        "<b>C</b> = étude de qualité méthodologique médiocre, descriptive, ou avis "
        "d'experts. <b>Ces deux échelles partagent les lettres A/B/C mais reposent sur des "
        "critères différents</b> — disclosed ici plutôt que fusionné. Les recommandations "
        "« accord professionnel » n'ont fait l'objet d'aucune publication dans la "
        "littérature. <i>Numérotation Q#.# assignée par cette fiche pour référence "
        "uniquement — le texte source ne numérote pas ses recommandations.</i>",
        S_BODY_SM))
    story.append(Spacer(1, 1.5 * mm))
    story.append(legend_flowable())
    return story

# ---------------------------------------------------------------------------
def _section_q1():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Q1 — Modalités et niveaux cliniques du passage coma → éveil"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(P(
        "Coma = « état de non-réponse, yeux fermés, sujet non réveillable ». 1re frontière : "
        "réapparition de périodes yeux ouverts (vigilance). 2e frontière : reprise d'une "
        "activité consciente (graduelle, période transitoire amnésique/confuse/agitée "
        "possible). Sans reprise de conscience : « état végétatif ». États "
        "« pauci-relationnels » (Minimally Conscious/Responsive State) : manifestations "
        "fluctuantes mais identifiables de perception — à distinguer du mutisme akinétique "
        "et du locked-in syndrome (conscience probablement/certainement conservée).",
        S_BODY_SM))
    story.append(Spacer(1, 1.5 * mm))
    story.append(reco_table([
        ("Q1.1", "Le score de Glasgow (GCS), associé à l'observation attentive, reste le "
         "meilleur moyen de coter rapidement les niveaux cliniques.", "AP"),
        ("Q1.2", "La durée de l'amnésie post-traumatique (APT), évaluée par le Galveston "
         "Orientation and Amnesia Test (GOAT), est le meilleur index pronostique global à "
         "la période initiale (par rapport au GCS et à la durée du coma).", "C"),
        ("Q1.3", "La Wessex Head Injury Matrix (WHIM), traduite et validée en français, "
         "évalue les états pauci-relationnels/végétatifs (valeur prédictive non encore "
         "déterminée).", "B"),
        ("Q1.4", "Les stimulations sensorielles peuvent contribuer à distinguer état "
         "pauci-relationnel et état végétatif.", "B"),
        ("Q1.5", "Corrélation entre durée du coma/de l'APT et les résultats de la Glasgow "
         "Outcome Scale (GOS, 5 catégories : décès, état végétatif persistant, handicap "
         "sévère/modéré, bonne récupération ; version étendue à 8 niveaux disponible).",
         "C"),
        ("Q1.6", "Consigner les résultats de ces échelles (GCS, GOAT, WHIM, GOS) et "
         "garantir leur accessibilité à toutes les unités successivement en charge du "
         "patient.", "AP"),
        ("Q1.7", "Le transfert vers une unité de rééducation, souvent différé par manque "
         "de place, devrait intervenir plus précocement ; la mise en place de filières de "
         "soins et l'identification d'une « unité d'éveil » dédiée (proche de la "
         "réanimation) sont recommandées.", "AP"),
    ], RCW))
    return story

# ---------------------------------------------------------------------------
def _section_q2():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Q2 — Apport des examens complémentaires"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(P("<b>Phase aiguë (premiers jours)</b>", S_CELL_B))
    story.append(Spacer(1, 1 * mm))
    story.append(reco_table([
        ("Q2.1", "La TDM est l'examen de l'admission et de la 24e heure (diagnostic en "
         "urgence des lésions accessibles à un traitement neurochirurgical).", "AE"),
        ("Q2.2", "L'IRM précoce peut préciser le diagnostic/pronostic (lésions axonales "
         "diffuses, tronc cérébral), mais n'est pas recommandée systématiquement (risque "
         "au transport, n'influence pas la prise en charge précoce).", "AE"),
        ("Q2.3", "Potentiels évoqués (PE) : PEATC/PES normaux ne permettent pas de se "
         "prononcer favorablement sur le pronostic ; PE cognitifs présents ont une forte "
         "valeur prédictive de l'éveil (mais pas sur la qualité de la récupération), "
         "absents = aucune valeur pronostique.", "A"),
        ("Q2.4", "L'EEG (monitorage continu) détecte les états de mal épileptiques non "
         "convulsifs et a une valeur pronostique sur l'évolution ultérieure.", "B"),
    ], RCW))
    story.append(Spacer(1, 2 * mm))
    story.append(P("<b>Phases subaiguë et chronique</b>", S_CELL_B))
    story.append(Spacer(1, 1 * mm))
    story.append(reco_table([
        ("Q2.5", "La TDM reste le standard de suivi thérapeutique, mais sa valeur "
         "prédictive est inférieure à celle de l'IRM.", "A"),
        ("Q2.6", "Facteurs péjoratifs à l'IRM : profondeur des lésions (corps calleux, "
         "noyaux gris centraux, hippocampe, mésencéphale, tronc cérébral dorso-latéral), "
         "&gt; 3 lésions, association de plusieurs types lésionnels.", "B"),
        ("Q2.7", "Une IRM est recommandée au moment du transfert en rééducation pour tout "
         "traumatisme crânien grave.", "AE"),
        ("Q2.8", "Les PE sensoriels/moteurs sont utiles pour évaluer la perméabilité "
         "sensorielle avant stimulations et identifier le locked-in syndrome ; en phase "
         "subaiguë, la réapparition de PE cognitifs est prédictive d'un réveil proche.",
         "C"),
        ("Q2.9", "Le SPECT (scintigraphie de perfusion) n'est pas recommandé à la phase "
         "des soins initiaux et de l'éveil.", "AP"),
        ("Q2.10", "PET-scan et IRM fonctionnelle (encore du domaine de la recherche) "
         "peuvent apporter des éléments d'individualisation de tableaux complexes "
         "(mutisme akinétique, locked-in syndrome) et de la neurotransmission.", "C"),
    ], RCW))
    return story

# ---------------------------------------------------------------------------
def _section_q3():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Q3 — Traitements médicamenteux favorisant la reprise de conscience"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(P(
        "Molécules étudiées (neurotransmetteurs ciblés) : lévodopa/carbidopa, amantadine, "
        "bromocriptine, dextroamphétamine, méthylphénidate, pémoline, tricycliques, "
        "inhibiteurs de la recapture de la sérotonine. 8 études descriptives au total "
        "(2 lévodopa/carbidopa, 4 amantadine, 1 amphétamines, 1 méthylphénidate) + 1 étude "
        "comparative (bromocriptine) — toutes rapportent un effet positif sauf la "
        "lévodopa/carbidopa, mais avec effets secondaires fréquents (crise comitiale, "
        "tachycardie, insomnie, anxiété, agitation, hallucinations, hyperthermie ; 1 décès "
        "sous amantadine).", S_BODY_SM))
    story.append(Spacer(1, 1.5 * mm))
    story.append(reco_table([
        ("Q3.1", "Le faible niveau de preuve des essais disponibles (critères de jugement "
         "variés/peu sensibles, groupes hétérogènes, mise sous traitement tardive de 3 à "
         "12 mois, durées de traitement diverses) ne permet pas de se prononcer sur "
         "l'efficacité de ces traitements médicamenteux.", "C"),
        ("Q3.2", "Les symptômes associés (spasticité, douleur, comitialité, agitation) "
         "n'ont pas été étudiés quant à leur effet sur l'éveil ; leur traitement approprié "
         "est néanmoins recommandé, en tenant compte de ses effets secondaires "
         "(sédation).", "AP"),
        ("Q3.3", "L'agitation à la phase d'éveil ne dispose d'aucun protocole de "
         "traitement validé à cette phase ; des études sont nécessaires pour préciser la "
         "prise en charge.", "AP"),
    ], RCW))
    return story

# ---------------------------------------------------------------------------
def _section_q4():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Q4 — Procédures de rééducation et prise en charge globale"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(P(
        "4 approches étudiées (27 études, 1969-1996) : neurostimulation cérébrale "
        "profonde/médullaire (NS), stimulation sensorielle (SS), régulation sensorielle "
        "(RS), approche fondée sur la sémiotique (AS). Résultats globalement encourageants "
        "mais de faible niveau de preuve (absence de groupe contrôle, définitions "
        "imprécises, protocoles à peine décrits, population hétérogène) — "
        "<b>aucune recommandation précise ne peut être formulée quant aux approches à "
        "privilégier.</b>", S_BODY_SM))
    story.append(Spacer(1, 1.5 * mm))
    story.append(reco_table([
        ("Q4.1", "La formulation d'un pronostic individuel reste difficile (données "
         "statistiques et scores de force/spécificité limitées) ; le pronostic annoncé "
         "influence l'engagement de l'équipe soignante — un pronostic pessimiste peut "
         "devenir une « prédiction auto-accomplie ».", "C"),
        ("Q4.2", "Élargir le temps de présence de la famille dans les limites de "
         "l'organisation des soins (connaissance du vécu du patient, premiers indices de "
         "conscience) — efficacité non démontrée scientifiquement mais justifiée par "
         "l'argument logique et la compassion.", "AP"),
        ("Q4.3", "Une information cohérente, adaptée au moment, progressive et "
         "pédagogique est recommandée pour les familles.", "AP"),
        ("Q4.4", "La présence de psychologues est nécessaire pour aider les familles et "
         "l'équipe soignante face à la charge émotionnelle.", "AE"),
        ("Q4.5", "Dans l'évaluation médico-légale, les différentes composantes du "
         "préjudice subi par les familles devraient être prises en compte.", "AP"),
    ], RCW))
    return story

# ---------------------------------------------------------------------------
def _section_sources():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("Sources et avertissement"))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "SOFMER (Société française de médecine physique et réadaptation), Conférence de "
        "consensus « Les traumatisés crâniens adultes en médecine physique et "
        "réadaptation : du coma à l'éveil » (texte court des recommandations du jury, "
        "président Pr Jean-Luc Truelle), 8 octobre 2001, organisée selon les règles "
        "méthodologiques ANAES, Ann Readapt Med Phys 45 (2002) 417-423.", S_SOURCE))
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Avertissement — document de 2001 :</b> cette fiche est une synthèse "
        "indépendante, produite pour un usage d'aide-mémoire. Elle reprend intégralement "
        "les constats/recommandations des 4 questions du jury mais omet la liste "
        "nominative des experts. La numérotation Q#.# est assignée par cette fiche pour "
        "référence uniquement — le texte source ne numérote pas ses recommandations. "
        "Elle ne remplace pas le texte intégral et n'est ni éditée ni validée par la "
        "SOFMER/ANAES. Document de 2001 : les techniques d'imagerie/électrophysiologie et "
        "les données pharmacologiques ont évolué depuis — vérifier l'actualité clinique "
        "avant application.",
        S_BODY_SM), bg=GREY_LIGHT, border=GREY))
    return story

# ---------------------------------------------------------------------------
def _section_all():
    story = _section_intro()
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_q1())
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_q2())
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_q3())
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_q4())
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_sources())
    return story

SECTIONS = [
    ("Méthodologie, Q1 (clinique), Q2 (examens), Q3 (traitements), Q4 (rééducation) & sources",
     _section_all),
]

def _make_doc(path=None):
    return SimpleDocTemplate(path or OUT, pagesize=A4,
                              leftMargin=MARGIN, rightMargin=MARGIN,
                              topMargin=32 * mm, bottomMargin=16 * mm,
                              title="Fiche SOFMER 2001 - Traumatises craniens, du coma a l'eveil",
                              author="Synthèse indépendante (source SOFMER)")

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
