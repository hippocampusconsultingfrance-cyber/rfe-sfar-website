# -*- coding: utf-8 -*-
"""
Fiche de synthese - Societe Nationale Francaise de Colo-Proctologie (SNFCP),
avec l'ANAP et la SFAR. "Chirurgie ambulatoire en proctologie : texte des
recommandations SNFCP" - mars 2015. 6 pages, telecharge depuis sfar.org
(wp-content/uploads/2016/08/RECOCHIRAMBUSNFCP-120315.pdf).

METHODOLOGIE : grille a 4 niveaux (A = preuve scientifique etablie, B =
presomption scientifique, C = faible niveau de preuve, AE = accord
d'experts). Sur les 43 recommandations numerotees de ce document, SEULES 3
enonces portent un grade explicite "(grade A)" - tout le reste est "(AE)" ;
les grades B et C, bien que definis dans la grille methodologique du
document, ne sont utilises pour AUCUNE des 43 recommandations (disclosed,
pas une omission de cette fiche).

ANTI-COMPOSITE-GRADE : R15 et R27 fusionnent, dans le texte source, une ou
deux phrases explicitement "(grade A)" avec une phrase suivante non gradee
(donc AE par defaut) dans le meme paragraphe numerote - scindees ici en
lignes distinctes (R15 -> R15a/R15b grade A + R15c AE ; R27 -> R27a grade A
+ R27b AE) conformement a la regle anti-fusion de grade. R34 est un renvoi
explicite ("cf. supra") a la meme recommandation que R15a (limiter les
perfusions IV) reformule dans la section rétention urinaire - traite comme
une recommandation numerotee a part entiere (le document la numerote et la
grade separement) mais son caractere de repetition est disclosed.

DISCLOSURE - 2 recommandations sans marqueur de grade imprime du tout (ni
"(grade A/B/C)" ni "(AE)") : R37 (renvoi a un RPC externe SNFCP 2014) et R40
(discussion multidisciplinaire anticoagulants). Par défaut, en l'absence de
toute autre indication dans un document qui ne definit que 4 categories
(A/B/C/AE) et n'en utilise que 2, ces 2 enonces sont chippes "AE" comme le
reste des recommandations non explicitement gradees A - disclosed comme un
choix de transcription plutot que suppose silencieusement.

PERIMETRE : integral sur les 43 recommandations organisees en 5 sections
(parcours de soin/eligibilite/organisation R1-24, douleur postoperatoire
R25-30, retention d'urines R31-38, risque hemorragique R39-40, reprise du
transit R41-43).
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from style import *
GRADE_COLORS["A"] = (GREEN, WHITE)
GRADE_COLORS["B"] = (TEAL, WHITE)
GRADE_COLORS["C"] = (AMBER, WHITE)
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.units import mm

OUT = "/home/user/rfe-sfar-website/output/Fiche_SNFCP_Chirurgie_Ambulatoire_Proctologie_2015.pdf"

SOURCE_TXT = ("Source : SNFCP/ANAP/SFAR, « Chirurgie ambulatoire en proctologie », mars 2015. "
              "Fiche de synthèse non officielle : se référer au texte intégral.")

def P(txt, style=S_CELL):
    return Paragraph(txt, style)

def chip(label, **kw):
    return grade_chip(label, **kw)

CW_FULL = PAGE_W - 2 * MARGIN

def reco_table(rows, col_widths):
    """rows: (ref, text, grade_label)."""
    data = [[P("Réf.", S_HEAD_W), P("Recommandation", S_HEAD_W), P("Grade", S_HEAD_W_C)]]
    for ref, txt, grade in rows:
        data.append([P(ref, S_CELL_B), P(txt, S_CELL), chip(grade)])
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

RCW = [15 * mm, CW_FULL - 15 * mm - 16 * mm, 16 * mm]

def bullets(items, style=S_BODY_SM):
    html = "&bull; " + "<br/>&bull; ".join(items)
    return P(html, style)

def legend_flowable():
    chip_w = 16 * mm
    content_w = CW_FULL
    row = Table([[chip("A", width=chip_w - 2 * mm), chip("B", width=chip_w - 2 * mm),
                  chip("C", width=chip_w - 2 * mm), chip("AE", width=chip_w - 2 * mm),
                  P("<b>Grille SNFCP</b> — <b>A</b> : preuve scientifique établie ; "
                    "<b>B</b> : présomption scientifique ; <b>C</b> : faible niveau de "
                    "preuve ; <b>AE</b> : accord d'experts (absence d'études). Sur les 43 "
                    "recommandations de ce document, seules 3 portent un grade A explicite "
                    "— les grades B et C, bien que définis, ne sont utilisés pour aucune "
                    "recommandation.", S_BADGE_HEAD)]],
                colWidths=[chip_w] * 4 + [content_w - 4 * chip_w])
    row.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                              ("LEFTPADDING", (0, 0), (-1, -1), 1),
                              ("RIGHTPADDING", (0, 0), (-1, -1), 1),
                              ("TOPPADDING", (0, 0), (-1, -1), 0),
                              ("BOTTOMPADDING", (0, 0), (-1, -1), 0)]))
    return row

TOTAL_PAGES = {"n": 4}

def on_page(canvas, doc, page_title):
    header_band(canvas, doc, "SNFCP / ANAP / SFAR — MARS 2015",
                "Chirurgie ambulatoire en proctologie",
                page_title, icon_fn=lambda c, x, y: icon_pill(c, x, y, 13 * mm), color=TEAL_DARK)
    footer_band(canvas, doc, SOURCE_TXT, f"Page {doc.page} / {TOTAL_PAGES['n']}")

# ---------------------------------------------------------------------------
def _section_intro():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Résumé :</b> 43 recommandations pour développer la chirurgie proctologique "
        "ambulatoire avec les mêmes conditions de qualité et sécurité qu'en hospitalisation "
        "traditionnelle. Volontairement, ce document ne définit pas de liste d'actes "
        "éligibles : « ce n'est pas l'acte qui est ambulatoire mais le trio acte / patient / "
        "organisation de soins ». 5 champs : parcours de soin et organisation, douleur "
        "postopératoire, rétention d'urines, risque hémorragique, reprise du transit.",
        S_BODY), bg=BG_PANEL, border=TEAL))
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("Méthodologie"))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "Grille à 4 niveaux : <b>A</b> (preuve scientifique établie — essais randomisés de "
        "forte puissance, méta-analyses) ; <b>B</b> (présomption scientifique — essais "
        "randomisés de faible puissance, cohortes) ; <b>C</b> (faible niveau de preuve — "
        "cas-témoins, biais importants) ; <b>AE</b> (accord d'experts, en l'absence "
        "d'études). Sur les 43 recommandations, seules 3 énoncés portent un grade A "
        "explicite (limitation des perfusions IV, choix d'anesthésique local pour la "
        "rachianesthésie, analgésie multimodale) ; le reste relève de l'accord d'experts.",
        S_BODY_SM))
    story.append(Spacer(1, 1.5 * mm))
    story.append(legend_flowable())
    return story

# ---------------------------------------------------------------------------
def _section_parcours():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("2.1 Parcours de soin et organisation (R1-24)"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("R1", "Privilégier le mode ambulatoire lorsque les conditions médicales et "
         "psycho-sociales d'éligibilité sont réunies.", "AE"),
        ("R2", "Identifier le médecin traitant et les personnes ressources (accompagnant, "
         "aidant naturel, personne de confiance).", "AE"),
        ("R3", "Vérifier les conditions d'ambulatoire à toutes les étapes ; délai pour "
         "atteindre une structure d'urgence ≤ 1 heure.", "AE"),
        ("R4", "Une déficience physique ou intellectuelle n'interdit pas l'ambulatoire "
         "(nécessite des adaptations spécifiques).", "AE"),
        ("R5", "Le grand âge n'interdit pas l'ambulatoire si les conditions d'éligibilité "
         "sont réunies (diminuerait le risque confusionnel).", "AE"),
        ("R6", "La consultation de programmation opératoire est essentielle : chemin "
         "clinique, coordination des acteurs, information orale et écrite.", "AE"),
        ("R7", "Organisation basée sur la gestion des flux (minimiser les pertes de "
         "temps, optimiser les circuits).", "AE"),
        ("R8", "L'équipe de l'Unité de Chirurgie et Anesthésie Ambulatoire (UCA) doit être "
         "sensibilisée, expérimentée et formée.", "AE"),
        ("R9", "Prise en charge au sein d'une unité d'accueil dédiée (réglementaire), "
         "recommandée à proximité immédiate du bloc opératoire.", "AE"),
        ("R10", "Mettre en place une démarche de gestion des risques au sein de l'UCA.", "AE"),
        ("R11", "Mettre en place une démarche qualité (taux d'échec, événements "
         "indésirables, EPP, RMM).", "AE"),
        ("R12", "Le médecin anesthésiste doit être informé par l'opérateur du choix du "
         "mode ambulatoire et de la technique opératoire.", "AE"),
        ("R13", "L'opérateur doit être informé en cas de réserve de l'anesthésiste sur le "
         "mode ambulatoire.", "AE"),
        ("R14", "Prise en charge anesthésique définie par la RFE SFAR 2009 : jeûne "
         "préopératoire de 6 h (solides) et 2 h (liquides clairs sans pulpe ni gaz).", "AE"),
        ("R15a", "Pour réduire l'incidence des rétentions d'urines, limiter les "
         "perfusions intraveineuses.", "A"),
        ("R15b", "Si rachianesthésie choisie : anesthésique local de courte durée d'action, "
         "proscrire tout morphinique intrathécal.", "A"),
        ("R15c", "Prévenir dès la période opératoire la douleur postopératoire "
         "(antalgiques et techniques d'infiltration appropriées).", "AE"),
        ("R16", "Informer le médecin traitant du caractère ambulatoire dès la consultation "
         "de programmation.", "AE"),
        ("R17", "Le médecin traitant communique les informations utiles avant "
         "l'intervention et reçoit les éléments utiles après (compte-rendu, consignes, "
         "ordonnances).", "AE"),
        ("R18", "Expliquer au patient les modalités et recueillir son assentiment ; "
         "informer de l'importance de respecter les consignes pré- et postopératoires.", "AE"),
        ("R19", "La continuité des soins doit être organisée par l'UCA avec l'opérateur et "
         "l'anesthésiste, et formalisée par écrit.", "AE"),
        ("R20", "Organiser par anticipation les mesures de sortie (ordonnances, consignes, "
         "rendez-vous postopératoire), réévaluées en postopératoire.", "AE"),
        ("R21", "Délivrer au patient un dossier de liaison sur la nature du geste et les "
         "suites prévisibles.", "AE"),
        ("R22", "Formaliser une procédure de contact (numéro de téléphone) pour la "
         "continuité des soins.", "AE"),
        ("R23", "Vérifier la compréhension des consignes préopératoires par appel/SMS "
         "avant admission ; contacter le patient après le retour à domicile.", "AE"),
        ("R24", "Informer le patient des signes évoquant une complication (rétention, "
         "hémorragie, douleur non contrôlée, fécalome) et de la conduite à tenir.", "AE"),
    ], RCW))
    return story

# ---------------------------------------------------------------------------
def _section_douleur():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("2.2 Douleur postopératoire (R25-30)"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("R25", "Donner en préopératoire une information complète et détaillée sur la "
         "douleur postopératoire et sa prise en charge.", "AE"),
        ("R26", "Évaluer systématiquement la douleur (échelle EVA/EVS/EN) et la prendre en "
         "charge rapidement ; n'autoriser le retour à domicile que si le score est faible.",
         "AE"),
        ("R27a", "Privilégier l'analgésie multimodale, notamment par anesthésiques locaux "
         "de longue durée d'action (infiltration périnéale et/ou bloc pudendal).", "A"),
        ("R27b", "Informer le patient sur l'effet et la levée du bloc pudendal — il n'est "
         "pas nécessaire d'attendre la levée du bloc pour autoriser la sortie.", "AE"),
        ("R28", "Privilégier les analgésiques non opiacés (AINS, paracétamol) pour réduire "
         "la consommation d'opiacés et leurs effets secondaires.", "AE"),
        ("R29", "Utiliser les opiacés en cas de contrôle incomplet de la douleur par les "
         "non-opiacés et l'analgésie régionale.", "AE"),
        ("R30", "Fournir une ordonnance pré-établie dès la consultation ; s'assurer que le "
         "patient a anticipé l'achat des antalgiques disponibles à domicile.", "AE"),
    ], RCW))
    return story

def _section_parcours_douleur():
    story = _section_parcours()
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_douleur())
    return story

# ---------------------------------------------------------------------------
def _section_retention():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("2.3 Rétention d'urines postopératoire (R31-38)"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("R31", "Informer le patient du risque élevé de rétention et l'évaluer "
         "systématiquement (âge, diabète, pathologie neurologique, obstacle "
         "uréthro-cervico-prostatique, type de chirurgie et d'anesthésie).", "AE"),
        ("R32", "Obtenir une miction en préopératoire immédiat.", "AE"),
        ("R33", "Limiter les médicaments augmentant le risque (morphiniques, "
         "anticholinergiques/néfopam) — tout en contrôlant la douleur, elle-même facteur "
         "de risque de rétention.", "AE"),
        ("R34", "Limiter les perfusions intraveineuses (cf. R15a — même recommandation, "
         "reformulée dans le contexte de la rétention urinaire).", "A"),
        ("R35", "Chez un patient à faible risque : pas besoin d'attendre la reprise "
         "mictionnelle pour la sortie, sous réserve d'une évaluation du volume vésical.",
         "AE"),
        ("R36", "Chez un patient à risque élevé : quantifier la miction et évaluer le "
         "résidu post-mictionnel (si possible par échographie) avant la sortie.", "AE"),
        ("R37", "En cas de rétention, sondage évacuateur ou maintien d'un cathéter "
         "urétral (cf. RPC traitement de la maladie hémorroïdaire, SNFCP 2014).", "AE"),
        ("R38", "Informer le patient de contacter la structure d'hospitalisation en "
         "l'absence de miction dans les 12 heures.", "AE"),
    ], RCW))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<i>Disclosure :</i> R37 et R40 ne portent, dans le texte source, aucun marqueur "
        "de grade imprimé (ni « grade A/B/C » ni « AE ») — chippées AE ici par défaut, "
        "cohérent avec le reste du document qui ne connaît que ces deux issues (A "
        "explicite ou AE), non résolu silencieusement.", S_NOTE))
    return story

def _section_hemorragie_transit():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("2.6 Risque hémorragique (R39-40)"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("R39", "La gestion du risque hémorragique doit être une préoccupation majeure de "
         "tous les intervenants ; informer patient et médecin traitant du risque précoce "
         "et tardif (jusqu'à 3 semaines), surtout après chirurgie hémorroïdaire ou "
         "résection de tumeur rectale.", "AE"),
        ("R40", "Chez les patients sous antiplaquettaires/anticoagulants, discuter "
         "l'éligibilité à l'ambulatoire et le maintien/relais du traitement entre tous "
         "les intervenants (cardiologue, opérateur, anesthésiste).", "AE"),
    ], RCW))
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("2.7 Reprise du transit (R41-43)"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("R41", "Prescrire en préopératoire des laxatifs et une alimentation enrichie en "
         "fibres pour améliorer le transit et diminuer la douleur aux premières selles.",
         "AE"),
        ("R42", "Remettre avant l'intervention des conseils écrits en cas de constipation "
         "postopératoire.", "AE"),
        ("R43", "Le patient doit contacter un référent médical en l'absence d'évacuation "
         "de selles dans les 72 heures.", "AE"),
    ], RCW))
    return story

def _section_retention_hemorragie_transit():
    story = _section_retention()
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_hemorragie_transit())
    return story

# ---------------------------------------------------------------------------
def _section_sources():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("Sources et avertissement"))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "SNFCP, avec l'ANAP et la SFAR, « Chirurgie ambulatoire en proctologie : texte des "
        "recommandations SNFCP », mars 2015. S'appuie sur un document produit par "
        "l'Association Française d'Urologie (Cuvelier et al., Progrès en Urologie "
        "2013;23:62-66) et sur la RFE SFAR 2009 sur la prise en charge anesthésique en "
        "hospitalisation ambulatoire.", S_SOURCE))
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Avertissement — document de 2015 :</b> cette fiche est une synthèse "
        "indépendante, produite pour un usage d'aide-mémoire. Elle reprend l'intégralité "
        "des 43 recommandations du texte source, mais ne remplace pas le texte intégral et "
        "n'est ni éditée ni validée par la SNFCP/ANAP/SFAR. Les pratiques de chirurgie "
        "ambulatoire ayant pu évoluer depuis 2015, se référer à un avis spécialisé et aux "
        "recommandations actualisées avant toute décision.", S_BODY_SM), bg=GREY_LIGHT,
        border=GREY))
    return story

# ---------------------------------------------------------------------------
def _section_all():
    story = _section_intro()
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_parcours_douleur())
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_retention_hemorragie_transit())
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_sources())
    return story

SECTIONS = [
    ("Méthodologie, R1-43 (parcours, douleur, rétention, hémorragie, transit) & sources",
     _section_all),
]

def _make_doc(path=None):
    return SimpleDocTemplate(path or OUT, pagesize=A4,
                              leftMargin=MARGIN, rightMargin=MARGIN,
                              topMargin=32 * mm, bottomMargin=16 * mm,
                              title="Fiche SNFCP 2015 - Chirurgie ambulatoire en proctologie",
                              author="Synthèse indépendante (source SNFCP/ANAP/SFAR)")

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
