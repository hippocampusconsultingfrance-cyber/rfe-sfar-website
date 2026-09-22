# -*- coding: utf-8 -*-
"""
Fiche de synthese - "Anesthesie pour chirurgie non cardiaque des patients
adultes porteurs de cardiopathie congenitale" - Recommandations de
Pratiques Professionnelles (RPP), SFAR en association avec la SFC, la SFP,
le CARO et la SFCTCV, 2023. 44 pages (texte principal + argumentaire +
bibliographie), telecharge depuis sfar.org.

PIEGE DE TELECHARGEMENT SFAR TROUVE ET CORRIGE : la page SFAR propose 2
fichiers - "...cardiopathie-congenitale" (wpdmdl=50051) et
"...cardiopathie-congenitale-annexes" (wpdmdl=50052). CONTRAIREMENT A CE
QUE SUGGERENT LES NOMS DE FICHIERS, c'est le lien SANS "-annexes"
(wpdmdl=50051) qui sert en realite les 10 pages de FICHES PRATIQUES
(annexes visuelles), et le lien AVEC "-annexes" dans son slug
(wpdmdl=50052) qui sert le texte principal complet de 44 pages avec les 11
recommandations - verifie par inspection du contenu des deux fichiers, pas
seulement de leurs noms. `library_final.json` pointe vers wpdmdl=50051
(les fiches pratiques seules) - a corriger si ce champ est reutilise pour
retelecharger ce document. Cette fiche synthetise le texte PRINCIPAL
(wpdmdl=50052).

METHODOLOGIE : methode GRADE(R) Grid - "apres synthese du travail des
experts et application de la methode GRADE, 11 recommandations ont ete
formalisees... un accord fort a ete obtenu pour 100% des recommandations"
(texte source explicite). PAS de grade GRADE numerique 1+/1-/2+/2- imprime
- toutes les 11 recommandations sont "Avis d'experts (Accord fort)", chip
unique (meme convention que fiche_impact_environnemental_ag.py et
fiche_bris_dentaires.py).

PERIMETRE ET SCOPE-LIMITING DISCLOSED : le score de risque composite (R1.1)
combine 3 axes - risque lie au type de cardiopathie (classification AHA
2018, tableau exhaustif par lesion cardiaque specifique), statut
physiologique A-D (Tableau 3, reproduit integralement ici - compact et
utilisable seul) et risque chirurgical (Tableau 5, reproduit integralement
ici - compact et utilisable seul). Le tableau de croisement final (Tableau
6, croisant les 3 axes pour obtenir le risque composite final par lesion
cardiaque specifique) N'EST PAS reproduit ici : il s'agit d'une
classification cardiologique exhaustive lesion-par-lesion (plusieurs pages
du texte source), disclosed comme hors perimetre de cette fiche - se
referer au texte integral (Tableaux 2, 4 et 6) pour calculer le risque
composite exact d'un patient donne. Les 6 "fiches pratiques" annexes
(algorithmes visuels : pieges du monitorage, principes d'anesthesie,
protocoles d'urgence HTAP/Fontan, conduite obstetricale) ne sont
transcrites que pour la Fiche pratique #1 (tableau de gestion des
traitements, extractible en texte propre) - les fiches #2 a #6 sont des
infographies visuelles denses, resumees par leur titre/objet uniquement et
disclosed comme non transcrites integralement dans cette passe (renvoi aux
annexes du texte source, fichier wpdmdl=50051 malgre son nom trompeur).
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from style import *
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.units import mm

OUT = "/home/user/rfe-sfar-website/output/Fiche_SFAR_Anesth_Cardiopathie_Congenitale_2023.pdf"

SOURCE_TXT = ("Source : SFAR/SFC/SFP/CARO/SFCTCV, « Anesthésie pour chirurgie non cardiaque des "
              "patients adultes porteurs de cardiopathie congénitale », RPP, 2023. Fiche de "
              "synthèse non officielle : se référer au texte intégral.")

def P(txt, style=S_CELL):
    return Paragraph(txt, style)

def chip(label, **kw):
    return grade_chip(label, **kw)

CW_FULL = PAGE_W - 2 * MARGIN

def reco_table(rows, col_widths):
    """rows: (ref, text, grade_label)."""
    data = [[P("Réf.", S_HEAD_W), P("Recommandation", S_HEAD_W), P("Niveau", S_HEAD_W_C)]]
    for ref, txt, grade in rows:
        data.append([P(ref, S_CELL_B), P(txt, S_CELL), chip(grade, width=17 * mm)])
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

RCW = [16 * mm, CW_FULL - 16 * mm - 20 * mm, 20 * mm]

def theme_table(rows, col_widths, head=("Thème", "Détail")):
    data = [[P(head[0], S_HEAD_W), P(head[1], S_HEAD_W)]]
    for theme, detail in rows:
        data.append([P(theme, S_CELL_B), P(detail, S_CELL)])
    t = Table(data, colWidths=col_widths, repeatRows=1)
    style_cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), NAVY), ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTNAME", (0, 0), (-1, 0), FONT_BOLD), ("FONTSIZE", (0, 0), (-1, 0), 8),
        ("VALIGN", (0, 0), (-1, -1), "TOP"), ("ALIGN", (0, 1), (0, -1), "LEFT"),
        ("GRID", (0, 0), (-1, -1), 0.5, GREY_LIGHT),
        ("TOPPADDING", (0, 0), (-1, -1), 3.4), ("BOTTOMPADDING", (0, 0), (-1, -1), 3.4),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            style_cmds.append(("BACKGROUND", (0, i), (-1, i), BG_PANEL))
    t.setStyle(TableStyle(style_cmds))
    return t

def bullets(items, style=S_BODY_SM):
    html = "&bull; " + "<br/>&bull; ".join(items)
    return P(html, style)

def legend_flowable():
    chip_w = 20 * mm
    content_w = CW_FULL
    row = Table([[chip("AE", width=chip_w - 2 * mm),
                  P("<b>AE = Avis d'experts (Accord fort).</b> Méthode GRADE® Grid, 2 tours de "
                    "cotation : accord fort obtenu pour les 11 recommandations (100 %) — aucune "
                    "n'est graduée GRADE 1+/1-/2+/2-.", S_BADGE_HEAD)]],
                colWidths=[chip_w, content_w - chip_w])
    row.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                              ("LEFTPADDING", (0, 0), (-1, -1), 1),
                              ("RIGHTPADDING", (0, 0), (-1, -1), 1),
                              ("TOPPADDING", (0, 0), (-1, -1), 0),
                              ("BOTTOMPADDING", (0, 0), (-1, -1), 0)]))
    return row

TOTAL_PAGES = {"n": 6}

def on_page(canvas, doc, page_title):
    header_band(canvas, doc, "SFAR / SFC / SFP / CARO / SFCTCV — RPP, 2023",
                "Anesthésie et cardiopathie congénitale de l'adulte",
                page_title, icon_fn=lambda c, x, y: icon_shield(c, x, y, 13 * mm), color=RED)
    footer_band(canvas, doc, SOURCE_TXT, f"Page {doc.page} / {TOTAL_PAGES['n']}")

# ---------------------------------------------------------------------------
def _section_intro_risque():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Résumé :</b> la mortalité périopératoire en chirurgie non cardiaque est 2 à 7 % "
        "chez l'adulte porteur de cardiopathie congénitale (CC), contre une population "
        "témoin bien plus faible — la CC est un facteur de risque indépendant de mortalité. "
        "60 % des complications surviennent en période postopératoire. 11 recommandations "
        "en 4 champs : risque préopératoire, stratégie anesthésique, prise en charge "
        "postopératoire, obstétrique.", S_BODY), bg=RED_LIGHT, border=RED))
    story.append(Spacer(1, 2.5 * mm))
    story.append(legend_flowable())
    story.append(Spacer(1, 3 * mm))
    story.append(KeepTogether([
        section_bar("Champ 1 — Risque préopératoire : score composite"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("R1.1", "Utiliser un score composite associant (1) le risque lié au type de "
         "cardiopathie (classification AHA 2018), (2) le statut physiologique A-D "
         "(Tableau 3 ci-dessous) et (3) le risque chirurgical (Tableau 5 ci-dessous), pour "
         "évaluer le risque périopératoire en chirurgie non cardiaque. Une procédure sous "
         "ALR périphérique est considérée à score composite faible quel que soit le statut "
         "de la cardiopathie.", "AE"),
        ("R1.2", "Chez un patient à score composite intermédiaire ou élevé, prise en charge "
         "en centre expert en cardiopathies congénitales, pour diminuer la survenue de "
         "complications périopératoires.", "AE"),
    ], RCW))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<i>Le tableau de croisement complet (Tableau 6, risque composite final par lésion "
        "cardiaque spécifique) n'est pas reproduit ici — classification cardiologique "
        "exhaustive lésion par lésion sur plusieurs pages du texte source ; se référer au "
        "texte intégral pour calculer le score composite exact d'un patient donné.</i>",
        S_NOTE))
    story.append(Spacer(1, 2 * mm))
    story.append(P("<b>Tableau 3 — Statut physiologique (classification AHA 2018)</b>", S_CELL_B))
    story.append(Spacer(1, 1 * mm))
    story.append(theme_table([
        ("A", "NYHA I. Absence de séquelle hémodynamique ou anatomique. Rythme sinusal, "
         "absence d'arythmie. Capacité physique normale. Fonctions rénale, hépatique et "
         "pulmonaire normales."),
        ("B", "Séquelles hémodynamiques modérées (dilatation aortique/ventriculaire "
         "modérée, dysfonction ventriculaire modérée). Valvulopathie modérée. Shunt "
         "trivial. Arythmie ne nécessitant pas de traitement. Limitation cardiaque "
         "objective à l'effort."),
        ("C", "NYHA III. Valvulopathie ou dysfonction ventriculaire modérée à importante. "
         "Dilatation aortique modérée. Sténose veineuse ou artérielle. Hypoxémie, cyanose. "
         "Shunt significatif. Arythmie contrôlée par traitement. HTAP non sévère. "
         "Dysfonction d'organe répondant au traitement."),
        ("D", "NYHA IV. Dysfonction ventriculaire sévère. Dilatation aortique sévère. "
         "Arythmie réfractaire au traitement. Hypoxémie sévère (souvent avec cyanose). "
         "HTAP sévère, syndrome d'Eisenmenger. Dysfonction d'organe réfractaire au "
         "traitement."),
    ], [14 * mm, CW_FULL - 14 * mm]))
    return story

# ---------------------------------------------------------------------------
def _section_tableau5_champ2():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        P("<b>Tableau 5 — Risque chirurgical</b> (approximation du risque de décès à 30 "
          "jours et d'infarctus, sans tenir compte des comorbidités — adapté des "
          "recommandations ESC/ESA 2014) :", S_CELL_B),
        Spacer(1, 1 * mm),
    ]))
    story.append(theme_table([
        ("Faible (< 1 %)",
         "Chirurgie superficielle, du sein, dentaire, thyroïdienne ; ophtalmologie ; "
         "chirurgie reconstructrice ; carotide asymptomatique ; gynécologie mineure ; "
         "orthopédie mineure (ex. méniscectomie) ; urologie mineure (RTUP)."),
        ("Intermédiaire (1-5 %)",
         "Splénectomie, hernie hiatale, cholécystectomie ; carotide symptomatique ; "
         "angioplastie périphérique ; anévrysme par voie endovasculaire ; chirurgie tête "
         "et cou ; neurochirurgie ; orthopédie majeure (hanche, rachis) ; urologie/"
         "gynécologie majeure ; transplantation rénale ; chirurgie thoracique non "
         "majeure ; obstétrique."),
        ("Élevé (> 5 %)",
         "Chirurgie aortique et vasculaire majeure (revascularisation AOMI, amputation) ; "
         "chirurgie duodéno-pancréatique ; hépatectomie, voies biliaires ; "
         "œsophagectomie ; perforation digestive ; phéochromocytome ; cystectomie ; "
         "pneumonectomie ; transplantation (foie ou poumon)."),
    ], [30 * mm, CW_FULL - 30 * mm]))
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Champ 2 — Stratégie anesthésique"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("R2.1.1", "Recourir à l'anesthésie locorégionale plutôt qu'à l'anesthésie "
         "générale chaque fois que possible, pour réduire la morbi-mortalité "
         "périopératoire.", "AE"),
        ("R2.1.2", "Pour une ALR neuraxiale, privilégier la technique titrée ou continue "
         "par rapport à la technique non titrée.", "AE"),
        ("R2.2", "Adapter la stratégie anesthésique au risque : monitorage standard si "
         "risque composite faible ; monitorage hémodynamique continu et invasif de la "
         "pression artérielle + mesures régulières de PaO2/PaCO2 si risque composite "
         "intermédiaire ou élevé ; ajout d'un monitorage de la pression veineuse centrale "
         "continue en cas de circulation de Fontan (cf. fiche pratique #5).", "AE"),
    ], RCW))
    return story

# ---------------------------------------------------------------------------
def _section_champ3_4():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Champ 3 — Prise en charge postopératoire"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("R3.1", "Prise en charge systématique en unité de soins critiques en "
         "postopératoire pour les patients à score composite intermédiaire ou élevé — 60 "
         "% des complications surviennent en période postopératoire ; surveillance "
         "rapprochée en particulier si FEVG préopératoire &lt; 30 % ou cyanose "
         "préopératoire (patients Fontan).", "AE"),
        ("R3.2", "Prendre un avis spécialisé de cardiologie congénitale adulte en "
         "postopératoire : pour les patients à risque composite intermédiaire ou élevé ; "
         "en cas de survenue d'une complication quelle que soit sa sévérité ; en cas de "
         "chirurgie en urgence sans avis cardiologique préalable.", "AE"),
    ], RCW))
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Champ 4 — Prise en charge en obstétrique"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("R4.1", "Évaluation de la cardiopathie en centre expert dès le début de la "
         "grossesse (statut physiologique, complications), pour toute patiente enceinte "
         "porteuse d'une CC.", "AE"),
        ("R4.2", "Prise en charge péripartum en centre expert (équipe pluridisciplinaire "
         "cardiologue/obstétricien/anesthésiste) pour les patientes à score composite "
         "intermédiaire ou élevé — un plan de prise en charge pluridisciplinaire "
         "personnalisé est recommandé, en particulier en cas d'HTAP.", "AE"),
        ("R4.3", "Privilégier l'anesthésie locorégionale titrée par rapport à l'ALR non "
         "titrée ou à l'anesthésie générale, pour réduire la morbi-mortalité "
         "péripartum.", "AE"),
        ("R4.4", "Surveillance systématique en unité de soins critiques en postpartum pour "
         "les patientes à score composite intermédiaire ou élevé — le postpartum "
         "immédiat est une période à haut risque de décompensation (défaillance "
         "cardiaque, arythmie), notamment entre J0 et J4 en cas d'HTAP.", "AE"),
    ], RCW))
    return story

# ---------------------------------------------------------------------------
def _section_annexes():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Annexe — Fiche pratique #1 : gestion périopératoire des traitements"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(theme_table([
        ("Diurétiques", "Poursuite la veille ; arrêt le matin de l'intervention ; contrôle "
         "de la kaliémie souhaitable, optimisation de la volémie périopératoire."),
        ("IEC", "Poursuite la veille ; arrêt le matin (≥ 12h si traitement de l'HTA) ; "
         "poursuite si insuffisance cardiaque et/ou FE ventricule systémique &lt; 40 %."),
        ("Bêtabloquants", "Poursuite la veille et le matin ; en l'absence d'urgence, "
         "discuter l'arrêt avec le cardiologue congénitaliste référent."),
        ("Inhibiteurs SRAA", "Poursuite la veille ; arrêt le matin ; poursuite si "
         "insuffisance cardiaque et/ou FE ventricule systémique &lt; 40 %."),
        ("Anti-arythmiques", "Classe I (flécaïne...) : arrêt la veille et le matin. Classe "
         "II/III (cordarone) : poursuite. Digoxine : aucune recommandation ; discuter "
         "l'arrêt avec le cardiologue référent en l'absence d'urgence."),
        ("Antihypertenseurs pulmonaires (sildénafil, bosentan, prostacycline)",
         "Poursuite la veille et le matin."),
        ("AOD (rivaroxaban, apixaban, edoxaban, dabigatran)", "Voir les recommandations "
         "GIHP ; en l'absence d'urgence, discuter l'arrêt avec le cardiologue référent."),
        ("AVK", "Interrompre 5 jours avant une chirurgie à risque hémorragique élevé, "
         "relais HBPM/HNF selon la catégorie de risque ; en l'absence d'urgence, discuter "
         "du relais/de l'arrêt avec le cardiologue référent (notamment ventricules "
         "uniques en prévention primaire)."),
        ("Antiagrégants plaquettaires", "Aspirine : dernière prise J-3 (avis d'expert, "
         "arrêt sauf shunt systémico-pulmonaire type Blalock-Taussig ou stent du canal "
         "artériel). Clopidogrel/ticagrelor : dernière prise J-5. Prasugrel : dernière "
         "prise J-7. Discuter un relais HBPM/HNF postopératoire avec le cardiologue "
         "référent."),
    ], [46 * mm, CW_FULL - 46 * mm]))
    story.append(Spacer(1, 2 * mm))
    story.append(P(
        "<b>Autres fiches pratiques du texte source (annexes visuelles, non transcrites "
        "intégralement ici — infographies denses, se référer au fichier annexes) :</b>",
        S_CELL_B))
    story.append(Spacer(1, 1 * mm))
    story.append(bullets([
        "Fiche pratique #2 — Pièges du monitorage chez l'adulte porteur de CC (PVC, "
        "pression artérielle, débit cardiaque, EtCO2, SpO2, abord vasculaire)",
        "Fiche pratique #3 — Principes d'anesthésie des patients porteurs de CC hors "
        "chirurgie cardiaque",
        "Fiche pratique #4 — Protocole pour l'anesthésie en urgence d'un patient porteur "
        "d'une HTAP iso- ou supra-systémique",
        "Fiche pratique #5 — Protocole pour l'anesthésie en urgence d'un patient porteur "
        "d'une dérivation cavo-pulmonaire (Fontan)",
        "Fiche pratique #6 — Conduite à tenir par situation physiopathologique en "
        "anesthésie obstétricale",
    ]))
    return story

# ---------------------------------------------------------------------------
def _section_sources():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("Sources et avertissement"))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "SFAR, en association avec la Société Française de Cardiologie (SFC), la Société "
        "Française de Pédiatrie (SFP), le Club Anesthésie-Réanimation en Obstétrique "
        "(CARO) et la Société Française de Chirurgie Thoracique et Cardio-Vasculaire "
        "(SFCTCV), « Anesthésie pour chirurgie non cardiaque des patients adultes "
        "porteurs de cardiopathie congénitale », RPP, 2023. Comité de 16 experts. "
        "Bibliographie extensive dans le texte intégral (non reproduite ici).", S_SOURCE))
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Avertissement :</b> cette fiche est une synthèse indépendante, produite pour "
        "un usage d'aide-mémoire. Elle reprend intégralement le texte des 11 "
        "recommandations et les Tableaux 3 et 5 (statut physiologique, risque "
        "chirurgical), mais ne reproduit pas le Tableau 6 (croisement complet risque "
        "composite par lésion cardiaque spécifique — classification cardiologique "
        "exhaustive) ni les fiches pratiques annexes #2 à #6 (infographies visuelles), "
        "disclosed comme hors périmètre de cette passe. Elle ne remplace pas le texte "
        "intégral et n'est ni éditée ni validée par la SFAR. <b>Note sur le "
        "téléchargement :</b> les deux fichiers proposés par sfar.org pour ce document "
        "ont des noms trompeurs — le fichier sans « -annexes » dans son nom contient en "
        "réalité les fiches pratiques visuelles, celui avec « -annexes » contient le "
        "texte principal complet synthétisé ici.",
        S_BODY_SM), bg=GREY_LIGHT, border=GREY))
    return story

# ---------------------------------------------------------------------------
def _section_all():
    story = _section_intro_risque()
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_tableau5_champ2())
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_champ3_4())
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_annexes())
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_sources())
    return story

SECTIONS = [
    ("Risque préopératoire, stratégie anesthésique, postopératoire, obstétrique, annexes & sources",
     _section_all),
]

def _make_doc(path=None):
    return SimpleDocTemplate(path or OUT, pagesize=A4,
                              leftMargin=MARGIN, rightMargin=MARGIN,
                              topMargin=32 * mm, bottomMargin=16 * mm,
                              title="Fiche SFAR 2023 - Anesthesie et cardiopathie congenitale de l'adulte",
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
