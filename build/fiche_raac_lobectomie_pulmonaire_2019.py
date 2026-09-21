# -*- coding: utf-8 -*-
"""
Fiche de synthese - "Rehabilitation amelioree apres lobectomie pulmonaire"
- Recommandations Formalisees d'Experts (RFE) SFAR/SFCTCV, 20/09/2019. 46
pages, telecharge depuis sfar.org (wpdmdl=24440).

METHODOLOGIE : GRADE standard (meme famille que fiche_raac_orthopedique_
2019.py et fiche_raac_colorectal.py). Synthese du texte source : "32
recommandations... un accord fort a ete obtenu pour 31 recommandations et
un accord faible pour une seule recommandation. Parmi ces recommandations,
7 ont un niveau de preuve eleve (GRADE 1+), 23 ont un niveau de preuve
modere a faible (18 GRADE 2+ et 5 GRADE 2-) et 2 sont des avis d'experts."
Decompte verifie exact par extraction integrale des 32 items numerotes
(R1.1 a R5.5, y compris les sous-items X.Y.Z qui correspondent ici
directement a des recommandations individuelles distinctes, PAS a des
sous-votes d'un parent comme dans fiche_optimisation_beta_lactamines_2018.py
- verifie : 32 items numerotes = 32 recommandations annoncees, aucun
regroupement necessaire).

DISCLOSURE - incoherence de comptage sur les "questions sans reponse" :
le RESUME en tete de document annonce "pour 2 questions, aucune
recommandation n'a pu etre formulee", mais la section "Synthese des
resultats" du corps du texte annonce "pour 3 questions, aucune
recommandation n'a pu etre formulee" - ecart de 1, non resolu. Verifie par
recherche exhaustive : 2 tags explicites "ABSENCE DE RECOMMANDATION"
imprimes (Champ 2 Question 4 - premedication ; Champ 4 Question 4,
sous-partie "mise en aspiration du drain thoracique") + 1 troisieme cas
mentionne uniquement en prose dans l'argumentaire de la Question 5 du
Champ 2 (decolonisation nasale au S. aureus - absence de donnee
specifique a la chirurgie thoracique, "aucune recommandation ne peut etre
effectuee dans ce contexte"), qui n'a pas sa propre question numerotee
dediee ni son propre tag "ABSENCE DE RECOMMANDATION" (il partage la
Question 5 avec R2.4, qui elle est bien gradee). Les 3 sont neanmoins
transcrites ici comme 3 notes distinctes, le lecteur etant laisse juge des
deux comptages du texte source.

PERIMETRE : integral sur les 32 recommandations des 5 champs (selection du
parcours patient/information, gestion et prehabilitation preoperatoire,
anesthesie et analgesie, strategie chirurgicale, rehabilitation
postoperatoire) et les 3 "absences de recommandation" disclosed ci-dessus.
Argumentaire minimal (regle 2026-09-14) : les etudes citees a l'appui de
chaque recommandation ne sont pas transcrites - seul l'enonce actionnable
est retenu. Bibliographie par question et composition nominative du
groupe d'experts (non reproduites) - non actionnable cliniquement.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from style import *
GRADE_COLORS["2+*"] = (AMBER, WHITE)
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.units import mm

OUT = "/home/user/rfe-sfar-website/output/Fiche_SFAR_SFCTCV_RAAC_Lobectomie_Pulmonaire_2019.pdf"

SOURCE_TXT = ("Source : SFAR/SFCTCV, « Réhabilitation améliorée après lobectomie "
              "pulmonaire », RFE, 20/09/2019. Fiche de synthèse non officielle : se référer "
              "au texte intégral.")

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

def absence_note(question_txt):
    return info_panel(P(
        f"<b>Absence de recommandation</b> (données insuffisantes) : {question_txt}",
        S_BODY_SM), bg=GREY_LIGHT, border=GREY)

def legend_flowable():
    chip_w = 14 * mm
    content_w = CW_FULL
    row = Table([[chip("1+", width=chip_w - 2 * mm), chip("2+", width=chip_w - 2 * mm),
                  chip("2-", width=chip_w - 2 * mm), chip("2+*", width=chip_w - 2 * mm),
                  chip("AE", width=chip_w - 2 * mm),
                  P("<b>GRADE</b> — 1+ : forte (aucune recommandation « 1- » dans ce "
                    "document) ; 2+/2- : faible ; <b>AE</b> : avis d'experts (2/32, méthode "
                    "GRADE non applicable). <b>2+* : seule recommandation à accord faible</b> "
                    "(R2.5.2) — 31 des 32 recommandations sont à accord fort. ⚠ Le résumé en "
                    "tête de document et la section « Synthèse des résultats » se "
                    "contredisent sur le nombre de questions sans réponse (2 vs 3) — "
                    "disclosed, non résolu, les 3 cas trouvés sont listés dans cette fiche.",
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
    header_band(canvas, doc, "SFAR / SFCTCV — RECOMMANDATIONS FORMALISÉES D'EXPERTS, 2019",
                "Réhabilitation améliorée après lobectomie pulmonaire",
                page_title, icon_fn=lambda c, x, y: icon_shield(c, x, y, 13 * mm), color=TEAL_DARK)
    footer_band(canvas, doc, SOURCE_TXT, f"Page {doc.page} / {TOTAL_PAGES['n']}")

# ---------------------------------------------------------------------------
def _section_intro_champ1():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Résumé :</b> 32 recommandations GRADE (SFAR/SFCTCV) organisées en 5 champs pour "
        "la réhabilitation améliorée après lobectomie pulmonaire (chirurgie thoracique, "
        "population pédiatrique exclue) : parcours patient/information, prise en charge et "
        "préhabilitation préopératoire, anesthésie/analgésie, stratégie chirurgicale, "
        "réhabilitation postopératoire.", S_BODY), bg=BG_PANEL, border=TEAL_DARK))
    story.append(Spacer(1, 2.5 * mm))
    story.append(legend_flowable())
    story.append(Spacer(1, 3 * mm))
    story.append(KeepTogether([
        section_bar("Champ 1 — Sélection du parcours patient et information"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("R1.1", "Opérer les patients dans un centre chirurgical à haut volume d'activité, "
         "pour diminuer l'incidence des complications postopératoires et la durée "
         "d'hospitalisation.", "2+"),
        ("R1.2.1", "Ne pas hospitaliser systématiquement en réanimation les patients "
         "s'inscrivant dans un programme de RAC, pour diminuer complications/DMS.", "2-"),
        ("R1.2.2", "Discuter l'hospitalisation en unité de soins continus des patients à "
         "risque de complications (comorbidités, événements peropératoires).", "AE"),
        ("R1.3", "Délivrer une information de qualité à l'aide de plusieurs supports avant "
         "chirurgie, pour diminuer l'incidence des complications (anxiété, douleurs "
         "postopératoires).", "1+"),
    ], RCW))
    return story

# ---------------------------------------------------------------------------
def _section_champ2():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Champ 2 — Prise en charge et préhabilitation préopératoire"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("R2.1.1", "Dépister la dénutrition avant chirurgie, pour optimiser la "
         "réhabilitation postopératoire.", "2+"),
        ("R2.1.2", "Corriger une dénutrition dépistée en préopératoire par une stratégie "
         "nutritionnelle personnalisée.", "AE"),
        ("R2.2", "Encourager systématiquement l'arrêt préopératoire du tabac, "
         "indépendamment de la date de la lobectomie, pour diminuer les complications.",
         "1+"),
    ], RCW))
    story.append(Spacer(1, 2 * mm))
    story.append(absence_note(
        "impact des modalités de prémédication préopératoire — absence de preuve "
        "spécifique à la chirurgie thoracique ; rappel d'éviter les benzodiazépines de "
        "longue durée d'action chez ces patients (âge moyen élevé, comorbidités "
        "respiratoires fréquentes)."))
    story.append(Spacer(1, 2 * mm))
    story.append(reco_table([
        ("R2.3", "Proposer un programme de réhabilitation préopératoire aux patients les "
         "plus à risque, pour diminuer complications et DMS.", "2+"),
        ("R2.4", "Réaliser une désinfection oropharyngée préopératoire à base de "
         "chlorhexidine, pour diminuer les infections du site opératoire et les "
         "bactériémies postopératoires.", "2+"),
    ], RCW))
    story.append(Spacer(1, 2 * mm))
    story.append(absence_note(
        "décolonisation nasale du portage de S. aureus avant chirurgie — aucune donnée "
        "spécifique à la lobectomie pulmonaire disponible (mentionné en prose dans "
        "l'argumentaire de la question sur la désinfection oropharyngée, sans question "
        "numérotée ni tag dédié — l'un des 2 ou 3 cas selon la section du texte source, "
        "cf. légende ci-dessus)."))
    story.append(Spacer(1, 2 * mm))
    story.append(reco_table([
        ("R2.5.1", "Poursuivre le traitement habituel par inhibiteurs calciques, "
         "bêtabloquants, IEC ou autre anti-arythmique en périopératoire chez les patients "
         "déjà traités, pour prévenir l'ACFA postopératoire.", "2+"),
        ("R2.5.2", "Introduire en péri/postopératoire immédiat, selon la balance "
         "bénéfice-risque, un traitement anti-arythmique (inhibiteur calcique type "
         "vérapamil/diltiazem ou bêtabloquant) chez les patients non traités.", "2+*"),
    ], RCW))
    return story

# ---------------------------------------------------------------------------
def _section_champ3():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Champ 3 — Anesthésie et analgésie pour lobectomie"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("R3.1", "Ne pas privilégier une technique d'entretien de l'anesthésie plutôt "
         "qu'une autre (IV propofol ou inhalatoire halogénés).", "2-"),
        ("R3.2", "Utiliser une stratégie multimodale de ventilation protectrice (Vt ≤ 6 "
         "mL/kg de poids idéal, PEP, manœuvres de recrutement) en ventilation "
         "unipulmonaire.", "2+"),
        ("R3.3.1", "Administrer des apports liquidiens peropératoires de base entre 2 et 6 "
         "mL/kg/h, pour diminuer les complications respiratoires postopératoires.", "2+"),
        ("R3.3.2", "Titrer le remplissage vasculaire peropératoire à l'aide d'un "
         "monitorage hémodynamique, en privilégiant le Doppler œsophagien.", "2+"),
        ("R3.4.1", "Utiliser une technique d'analgésie locorégionale en postopératoire de "
         "lobectomie par thoracotomie, pour améliorer le contrôle de la douleur.", "1+"),
        ("R3.4.2", "Utiliser une technique d'analgésie locorégionale en postopératoire de "
         "lobectomie par thoracoscopie.", "2+"),
        ("R3.5", "Privilégier en 1ère intention le bloc paravertébral continu à "
         "l'analgésie péridurale thoracique, pour un meilleur profil de tolérance.", "2+"),
        ("R3.6", "Utiliser des AINS en cure courte dans le cadre de l'analgésie "
         "multimodale systémique.", "2+"),
        ("R3.7", "Utiliser une analgésie IV contrôlée par le patient (PCA) morphinique en "
         "cas de contre-indication/échec/inefficacité des techniques locorégionales.",
         "2+"),
    ], RCW))
    return story

# ---------------------------------------------------------------------------
def _section_champ4():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Champ 4 — Stratégie chirurgicale pour lobectomie"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("R4.1", "Favoriser les approches minimalement invasives par thoracoscopie plutôt "
         "que par thoracotomie, pour diminuer complications et DMS.", "2+"),
        ("R4.2", "En cas de thoracotomie, ne pas privilégier une thoracotomie latérale "
         "d'épargne musculaire par rapport à une thoracotomie postérolatérale.", "2-"),
        ("R4.3", "Utiliser un dispositif à visée aérostatique (colle ou patch) en cas de "
         "fuite aérique peropératoire, pour diminuer les fuites aériques prolongées et la "
         "DMS.", "1+"),
        ("R4.4.1", "Ne placer qu'un seul drain thoracique pour la gestion des "
         "épanchements pleuraux postopératoires.", "1+"),
        ("R4.4.2", "Utiliser un système d'aspiration électronique autonome en cas de mise "
         "en aspiration du drain thoracique, pour faciliter la réhabilitation.", "2+"),
    ], RCW))
    story.append(Spacer(1, 2 * mm))
    story.append(absence_note(
        "impact de la mise en aspiration du drain thoracique — données discordantes dans "
        "la littérature (études randomisées de bonne qualité méthodologique retrouvant "
        "des résultats opposés)."))
    story.append(Spacer(1, 2 * mm))
    story.append(reco_table([
        ("R4.4.3", "Enlever le(s) drain(s) thoracique(s) le plus rapidement possible en "
         "postopératoire, pour diminuer la durée de drainage et d'hospitalisation.", "1+"),
        ("R4.4.4", "Enlever le(s) drain(s) dès qu'il n'y a plus de fuite aérique et un "
         "débit liquidien non sanglant/non chyleux ≤ 300 mL/j.", "2+"),
    ], RCW))
    return story

# ---------------------------------------------------------------------------
def _section_champ5_sources():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Champ 5 — Réhabilitation postopératoire"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("R5.1", "Ne pas utiliser la ventilation non-invasive préventive chez tous les "
         "patients.", "2-"),
        ("R5.2", "Ne pas utiliser l'oxygénothérapie à haut débit préventive chez tous les "
         "patients.", "2-"),
        ("R5.3", "Utiliser la VNI ou l'oxygénothérapie à haut débit pour traiter une "
         "complication pulmonaire postopératoire (hypoxémie, détresse respiratoire), pour "
         "diminuer le recours à l'intubation.", "2+"),
        ("R5.4", "Utiliser un programme de réhabilitation amélioré après chirurgie, "
         "incluant la mobilisation précoce postopératoire.", "1+"),
        ("R5.5", "Réaliser de la kinésithérapie multimodale postopératoire, et non des "
         "techniques isolées de kinésithérapie respiratoire.", "2+"),
    ], RCW))
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("Sources et avertissement"))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "SFAR/SFCTCV, « Réhabilitation améliorée après lobectomie pulmonaire », RFE, "
        "validée le 20/09/2019. Méthode GRADE (2 tours de cotation, plusieurs "
        "amendements). Références bibliographiques par question et composition "
        "nominative du groupe d'experts (non reproduites ici).", S_SOURCE))
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Avertissement :</b> cette fiche est une synthèse indépendante, produite pour un "
        "usage d'aide-mémoire. Elle reprend intégralement les 32 recommandations et les 3 "
        "cas d'absence de recommandation trouvés dans le texte source, mais condense "
        "l'argumentaire de chaque item et omet la composition nominative du groupe "
        "d'experts. Elle ne remplace pas le texte intégral et n'est ni éditée ni validée "
        "par la SFAR/SFCTCV.", S_BODY_SM), bg=GREY_LIGHT, border=GREY))
    return story

# ---------------------------------------------------------------------------
def _section_all():
    story = _section_intro_champ1()
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_champ2())
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_champ3())
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_champ4())
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_champ5_sources())
    return story

SECTIONS = [
    ("Réhabilitation améliorée après lobectomie pulmonaire", _section_all),
]

def _make_doc(path=None):
    return SimpleDocTemplate(path or OUT, pagesize=A4,
                              leftMargin=MARGIN, rightMargin=MARGIN,
                              topMargin=32 * mm, bottomMargin=16 * mm,
                              title="Fiche SFAR-SFCTCV 2019 - RAAC lobectomie pulmonaire",
                              author="Synthèse indépendante (source SFAR/SFCTCV)")

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
