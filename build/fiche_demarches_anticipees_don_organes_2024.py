# -*- coding: utf-8 -*-
"""
Fiche de synthese - "Recommandations de bonne pratique relatives aux
demarches anticipees en vue de don d'organes et de tissus" - Agence de la
biomedecine (ABM), septembre 2024, methode RPC (Recommandations pour la
Pratique Clinique, HAS). 21 pages, telecharge depuis sfar.org (miroir d'un
document ABM ; wp-content/uploads/2024/10/RBP-deimarches-anticipeies_12_10_24.pdf).

METHODOLOGIE : cotation individuelle a deux tours (apres elimination des
valeurs extremes) inspiree de RAND/UCLA - echelle continue 1 (desaccord
complet) a 9 (accord complet), 3 zones (1-3 desaccord, 4-6 indecision, 7-9
accord), "fort" si la mediane reste dans une zone, "faible" si elle empiete
sur une borne. Comme fiche_mort_encephalique.py (meme famille RAND/UCLA),
la cotation est imprimee sous forme d'un tag "(accord fort)"/"(accord
faible)" APRES chaque bloc de texte, PAS sous forme de recommandations
numerotees R1/R2 - convention explicite du texte source (note de bas de
page : "les accords signales entre parentheses concernent l'ensemble de ce
qui precede a partir de l'accord precedent"). 29 blocs "accord fort" + 1
seul bloc "accord faible" (verifie par grep exhaustif du texte source,
aucune 3e valeur "desaccord"/"indecision" imprimee). Le bloc a accord
faible (etape 1, conduite a tenir en cas de defaillance vitale immediate)
est transcrit comme une ligne de tableau distincte, jamais fusionne avec
les blocs "accord fort" adjacents (regle anti-grade-composite du projet).
Chips reutilises : "AF" (Accord Fort, vert) / "AF-" (Accord Faible, ambre)
- convention locale a cette fiche (le texte source n'imprime pas de sigle,
seulement les mots en toutes lettres).

PERIMETRE : integral sur les 5 sections de recommandations (I. Prerequis
institutionnels, II. Definitions, III. Prerequis cliniques, IV. Les 4
etapes de la demarche anticipee, V. Formation). Glossaire (definitions des
notes de bas de page 1-6 : demarche anticipee, entretien anticipe, donneur
possible, donneur potentiel, reseau operationnel de proximite, services
partenaires) et abreviations repris sous forme de repere compact, non
comme argumentaire. Bibliographie (52 references), composition nominative
des groupes de travail/lecture (page 19) non reproduites (renvoi au texte
integral) - non actionnable cliniquement. AUCUNE collision de perimetre
avec la fiche existante `mort_encephalique` (SFAR/SRLF/ABM 2005, diagnostic
clinique/paraclinique de mort encephalique et criteres d'evaluation par
organe pour un donneur DEJA en mort encephalique) : ce document-ci traite
d'une etape EN AMONT, chez un patient PAS ENCORE en mort cerebrale
(coma grave sans perspective therapeutique, admission en reanimation dans
le seul but d'un eventuel don) - deux documents, deux perimetres distincts,
verifie par lecture complete avant construction.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from style import *
GRADE_COLORS["AF"] = (GREEN, WHITE)
GRADE_COLORS["AF-"] = (AMBER, WHITE)
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.units import mm

OUT = "/home/user/rfe-sfar-website/output/Fiche_ABM_Demarches_Anticipees_Don_Organes_2024.pdf"

SOURCE_TXT = ("Source : Agence de la biomédecine, « Recommandations de bonne pratique relatives "
              "aux démarches anticipées en vue de don d'organes et de tissus », septembre 2024. "
              "Fiche de synthèse non officielle : se référer au texte intégral.")

def P(txt, style=S_CELL):
    return Paragraph(txt, style)

def chip(label, **kw):
    return grade_chip(label, **kw)

CW_FULL = PAGE_W - 2 * MARGIN

def reco_table(rows, col_widths):
    """rows: (ref, text, grade_label)."""
    data = [[P("§", S_HEAD_W), P("Recommandation", S_HEAD_W), P("Cotation", S_HEAD_W_C)]]
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

RCW = [10 * mm, CW_FULL - 10 * mm - 22 * mm, 22 * mm]

def bullets(items, style=S_BODY_SM):
    html = "&bull; " + "<br/>&bull; ".join(items)
    return P(html, style)

def legend_flowable():
    chip_w = 17 * mm
    content_w = CW_FULL
    row = Table([[chip("AF", width=chip_w - 2 * mm),
                  P("<b>AF = Accord Fort</b> / <b>AF- = Accord Faible</b> — cotation à deux tours "
                    "inspirée de RAND/UCLA (échelle continue 1-9, 3 zones : désaccord 1-3, "
                    "indécision 4-6, accord 7-9 ; « fort » si la médiane reste dans une zone, "
                    "« faible » si elle empiète sur une borne). 29 blocs à accord fort, "
                    "<b>1 seul bloc à accord faible</b> (étape 1, conduite en cas de défaillance "
                    "vitale immédiate) — jamais fusionnés. Sigles AF/AF- introduits par cette "
                    "fiche : le texte source imprime les mots en toutes lettres après chaque "
                    "bloc concerné.", S_BADGE_HEAD)]],
                colWidths=[chip_w, content_w - chip_w])
    row.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                              ("LEFTPADDING", (0, 0), (-1, -1), 1),
                              ("RIGHTPADDING", (0, 0), (-1, -1), 1),
                              ("TOPPADDING", (0, 0), (-1, -1), 0),
                              ("BOTTOMPADDING", (0, 0), (-1, -1), 0)]))
    return row

TOTAL_PAGES = {"n": 4}

def on_page(canvas, doc, page_title):
    header_band(canvas, doc, "AGENCE DE LA BIOMÉDECINE — RECOMMANDATIONS DE BONNE PRATIQUE, 2024",
                "Démarches anticipées en vue de don d'organes et de tissus",
                page_title, icon_fn=lambda c, x, y: icon_kidney(c, x, y, 13 * mm), color=TEAL_DARK)
    footer_band(canvas, doc, SOURCE_TXT, f"Page {doc.page} / {TOTAL_PAGES['n']}")

# ---------------------------------------------------------------------------
def _section_intro():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Champ :</b> patients en coma grave (Glasgow &lt; 8) sans perspective thérapeutique "
        "après lésion cérébrale irréversible (AVC hémorragique/ischémique, traumatisme crânien), "
        "<b>avant</b> la survenue d'une mort cérébrale — admission en réanimation dans le seul but "
        "d'un possible don d'organes/tissus. Distinct de la prise en charge d'un donneur "
        "<b>déjà</b> en mort encéphalique (fiche dédiée « Mort encéphalique et prélèvement "
        "d'organes », SFAR/SRLF/ABM 2005).", S_BODY), bg=BG_PANEL, border=TEAL_DARK))
    story.append(Spacer(1, 2.5 * mm))
    story.append(legend_flowable())
    story.append(Spacer(1, 2.5 * mm))
    story.append(P("<b>Repères (glossaire du texte source) :</b>", S_CELL_B))
    story.append(Spacer(1, 1 * mm))
    story.append(bullets([
        "<b>Donneur possible</b> : patient avec dommage cérébral, signe de gravité (Glasgow &lt; 8), "
        "sans contre-indication médicale d'emblée, avec ≥ 1 organe prélevable.",
        "<b>Donneur potentiel</b> : donneur possible avec clinique de mort cérébrale (constatée ou "
        "probable).",
        "<b>CHPOT</b> : coordination hospitalière des prélèvements d'organes et de tissus.",
        "<b>Services partenaires</b> : urgences, neurologie/USINV, autres USIP, médecine/chirurgie — "
        "de l'établissement ou de son réseau opérationnel de proximité (ROP).",
    ]))
    return story

# ---------------------------------------------------------------------------
def _section_i_ii_iii():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("I — Prérequis à la mise en place d'une démarche anticipée"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("I.1", "La mise en place des démarches anticipées dans un établissement doit "
         "s'accompagner d'une réflexion institutionnelle préalable sur l'information et la "
         "formation des professionnels.", "AF"),
        ("I.2", "La CHPOT identifie les services partenaires où elles pourront être mises en "
         "place, dans son établissement et son réseau opérationnel de proximité (ROP).", "AF"),
        ("I.3", "La CHPOT, les services partenaires et la réanimation élaborent et formalisent "
         "une procédure locale (algorithme, checklist, livret d'information) définissant "
         "collégialement les critères d'admission des donneurs possibles en réanimation.", "AF"),
        ("I.4", "En cas de transfert interhospitalier du donneur possible, les frais de retour du "
         "corps sont à la charge de l'établissement autorisé au prélèvement où le décès a été "
         "déclaré, qu'il y ait eu ou non prélèvement.", "AF"),
    ], RCW))
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("II — Définitions"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("II.1", "La <b>démarche anticipée</b> est un processus conduisant à l'admission en "
         "réanimation d'un patient en coma grave sans perspective thérapeutique, à forte "
         "probabilité d'évolution vers la mort cérébrale, à finalité exclusive de possible "
         "prélèvement — collaboration pluridisciplinaire, étapes successives, "
         "accompagnement de fin de vie.", "AF"),
        ("II.2", "L'<b>entretien anticipé</b> est un entretien soignants-proches pour évoquer en "
         "amont la possibilité du don post mortem et recueillir l'éventuelle expression d'un "
         "refus du patient et l'adhésion des proches. Le terme « abord anticipé » ne doit plus "
         "être utilisé.", "AF"),
    ], RCW))
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("III — Prérequis cliniques à une démarche anticipée"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("III.1", "Deux prérequis : (1) une décision de limitation des traitements actée "
         "collégialement, après avis d'expert(s) (neurochirurgien/neurologue/réanimateur), "
         "devant l'absence de perspective thérapeutique (lésions cérébrales irréversibles, "
         "coma grave Glasgow &lt; 8 ou d'aggravation rapide) ; (2) l'annonce de la gravité, du "
         "pronostic vital engagé et de la mort à venir déjà réalisée par le médecin du service "
         "partenaire, avec vérification de sa compréhension par les proches.", "AF"),
    ], RCW))
    return story

# ---------------------------------------------------------------------------
def _section_iv_etapes12():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("IV — Étape 1 : Repérage d'un donneur possible"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("1.1", "Un donneur possible : lésions cérébrales irréversibles (AVCH, AVCI ou "
         "traumatisme crânien) ; coma grave (Glasgow &lt; 8 ou aggravation rapide) ; sans "
         "perspective thérapeutique après avis d'expert(s) en concertation avec l'équipe de "
         "soins.", "AF"),
        ("1.2", "Patient non ventilé, <b>sans</b> défaillance vitale immédiate : toutes les étapes "
         "de la démarche avant l'éventuelle admission en réanimation/gestes invasifs. Patient "
         "<b>avec</b> défaillance vitale immédiate cardio-respiratoire : gestes invasifs (dont "
         "intubation) envisageables de façon collégiale dans l'attente du recueil d'une "
         "éventuelle opposition ; dans tous les cas, soulagement des souffrances et "
         "accompagnement de fin de vie restent prioritaires.", "AF-"),
        ("1.3", "Ce repérage déclenche l'appel à la CHPOT. Le service partenaire ne se "
         "prononce pas seul sur une contre-indication ou une limite d'âge, sans concertation "
         "avec la CHPOT.", "AF"),
        ("1.4", "Situations particulières : préhospitalier — aucun entretien pour le don, "
         "seule l'évaluation du contexte clinique est possible. Réanimation sous ventilation "
         "invasive — entretien après le diagnostic de mort cérébrale (présence CHPOT "
         "recommandée), sauf cheminement particulier des proches. Réanimation sans "
         "ventilation invasive — toutes les étapes de la démarche.", "AF"),
    ], RCW))
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Étape 2 : Appel à la CHPOT"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("2.1", "Dès le premier appel à la CHPOT, le déplacement d'un soignant CHPOT sur "
         "site dans le service partenaire est recommandé.", "AF"),
        ("2.2", "Évaluation du donneur possible : estimation de la probabilité de mort "
         "cérébrale, vérification de l'absence de contre-indication absolue (dossier médical, "
         "médecin traitant), vérification de la prélevabilité d'au moins un organe (bilan "
         "biologique rénal/hépatique minimal) ; le régulateur de l'Agence de la biomédecine "
         "peut être appelé pour avis.", "AF"),
        ("2.3", "Vérification de l'organisation logistique (recherche d'un lit de réanimation, "
         "anticipée à l'échelle de l'établissement/réseau régional). L'entretien anticipé avec "
         "les proches est possible à ce stade.", "AF"),
    ], RCW))
    return story

# ---------------------------------------------------------------------------
def _section_iv_etape3():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Étape 3 : Entretiens avec les proches — Objectifs"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("3.1", "Vérification de la compréhension par les proches de la gravité, du pronostic "
         "vital engagé, de l'absence de perspective thérapeutique et de la mort à venir avec "
         "forte probabilité d'évolution vers la mort cérébrale.", "AF"),
        ("3.2", "Information sur la possibilité du don après la mort et recueil de l'éventuelle "
         "expression d'un refus du patient (= l'entretien anticipé). Le registre national des "
         "refus (RNR) ne peut être interrogé qu'après la déclaration de décès.", "AF"),
        ("3.3", "En l'absence d'opposition rapportée : information sur les modalités "
         "organisationnelles (transfert en réanimation, gestes spécifiques dont l'intubation, "
         "continuité de l'accompagnement), la durée d'hospitalisation en réanimation "
         "(habituellement 3 à 6 jours, à l'issue de laquelle la mort surviendra après arrêt des "
         "traitements de maintien en vie en l'absence de mort cérébrale), et la possibilité de "
         "non-aboutissement de la démarche.", "AF"),
        ("3.4", "Vérification de l'adhésion des proches à la démarche anticipée ; la situation "
         "est réévaluée avec eux selon leur vécu et l'évolution clinique du patient.", "AF"),
    ], RCW))
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Étape 3 : Spécificités pratiques de l'entretien anticipé"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("3.5", "<b>Qui :</b> un binôme — médecin sénior (service partenaire et/ou réa, le plus "
         "expérimenté) + soignant CHPOT (systématique en ES autorisés au prélèvement, "
         "privilégié dans les ES du ROP), éventuellement accompagné de paramédical(aux) ; "
         "équilibre à respecter entre nombre de proches et de soignants ; recours à un(e) "
         "psychologue souhaitable.", "AF"),
        ("3.6", "<b>Où :</b> salle à proximité du lieu de prise en charge, aménagée pour "
         "recevoir l'ensemble des proches et soignants, confortable, calme, dédiée.", "AF"),
        ("3.7", "<b>Quand :</b> adaptation au cheminement des proches et à l'état clinique du "
         "patient, en respectant l'ordre des étapes ; un entretien en journée est à privilégier.", "AF"),
        ("3.8", "<b>Comment :</b> transparence des informations et incertitude de l'aboutissement "
         "à concilier ; préparation entre soignants (mise en commun des informations, rôle de "
         "chacun, objectifs communs) ; la CHPOT reste disponible pour les questions "
         "spécifiques au prélèvement.", "AF"),
        ("3.9", "<b>Traçabilité :</b> synthèse de l'entretien tracée au dossier ; évaluation via une "
         "grille de débriefing (temporalité, compréhension des proches, présence CHPOT...) ; "
         "une opposition transmise par un proche est retranscrite au dossier par la "
         "coordination hospitalière.", "AF"),
    ], RCW))
    return story

# ---------------------------------------------------------------------------
def _section_iv_etape4_v_sources():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Étape 4 : Transfert et accueil en réanimation"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("4.1", "L'ensemble des étapes est tracé au dossier patient. Le transfert vers la "
         "réanimation est médicalisé ; tous les soignants sont informés des objectifs de "
         "l'admission (accompagnement de fin de vie et réanimation d'organes en vue d'un "
         "éventuel prélèvement).", "AF"),
        ("4.2", "La présence des proches est facilitée dans ce contexte de fin de vie ; "
         "l'accompagnement des proches et la réévaluation de la poursuite de la démarche "
         "sont assurés par la réanimation en partenariat avec la CHPOT.", "AF"),
        ("4.3", "Le soulagement des souffrances réelles ou potentielles est assuré pendant le "
         "séjour, même non évaluables du fait de l'état neurologique (article R4127-37-3 "
         "CSP). En l'absence d'évolution vers la mort cérébrale, un arrêt des traitements de "
         "maintien en vie est mis en œuvre selon le protocole du service, jusqu'au décès.", "AF"),
    ], RCW))
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("V — Formation des professionnels de santé"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("V.1", "Les médecins impliqués sont invités aux formations régionales de l'Agence de "
         "la biomédecine sur les entretiens avec les proches. Les professionnels de "
         "coordination hospitalière bénéficient d'un parcours de formation continue avec "
         "l'Agence ; leur participation aux étapes de la démarche est indispensable. Toutes "
         "les formations abordent les principes généraux des entretiens, certaines incluant "
         "les démarches anticipées.", "AF"),
    ], RCW))
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("Sources et avertissement"))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "Agence de la biomédecine, « Recommandations de bonne pratique relatives aux "
        "démarches anticipées en vue de don d'organes et de tissus », méthode RPC (HAS), "
        "septembre 2024. Cotation RAND/UCLA à 2 tours par un groupe de travail d'experts, "
        "après synthèse bibliographique et relecture par un groupe de lecture de 34 membres "
        "référents ; avis favorable du conseil d'orientation de l'ABM le 19/09/2024. "
        "52 références bibliographiques citées dans le texte intégral (non reproduites ici).",
        S_SOURCE))
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Avertissement :</b> cette fiche est une synthèse indépendante, produite pour un "
        "usage d'aide-mémoire. Elle reprend intégralement les recommandations des 5 sections "
        "du texte source (I à V) mais condense l'introduction, la situation de la "
        "problématique et omet la liste nominative des groupes de travail/lecture. Elle ne "
        "remplace pas le texte intégral et n'est ni éditée ni validée par l'Agence de la "
        "biomédecine.", S_BODY_SM), bg=GREY_LIGHT, border=GREY))
    return story

# ---------------------------------------------------------------------------
def _section_all():
    story = _section_intro()
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_i_ii_iii())
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_iv_etapes12())
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_iv_etape3())
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_iv_etape4_v_sources())
    return story

SECTIONS = [
    ("Démarches anticipées en vue de don d'organes et de tissus", _section_all),
]

def _make_doc(path=None):
    return SimpleDocTemplate(path or OUT, pagesize=A4,
                              leftMargin=MARGIN, rightMargin=MARGIN,
                              topMargin=32 * mm, bottomMargin=16 * mm,
                              title="Fiche ABM 2024 - Demarches anticipees en vue de don d'organes et de tissus",
                              author="Synthèse indépendante (source Agence de la biomédecine)")

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
