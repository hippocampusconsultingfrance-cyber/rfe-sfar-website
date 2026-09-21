# -*- coding: utf-8 -*-
"""
Fiche de synthese - "Preconisations pour les ressources humaines medicales en
anesthesie programmee (hors anesthesie pediatrique et anesthesie obstetricale)"
- SFAR, a l'initiative du CNP ARMPO, Recommandations pour la Pratique
Professionnelle (RPP), texte valide par le CA de la SFAR le 02/12/2024.
18 pages, telecharge depuis sfar.org (wpdmdl=72905).

METHODOLOGIE : methode GRADE grid appliquee a l'analyse de la litterature,
mais format RPP (pas RFE) retenu en amont car peu d'etudes a criteres de
jugement forts - terminologie "les experts suggerent de faire/ne pas faire"
pour les avis d'experts, et "rappel a la reglementation" quand la question
trouve reponse dans un texte legislatif/reglementaire (texte source
explicite, section RESULTATS). 11 preconisations au total : 4 rappels a la
reglementation (R1.1-R1.4) + 7 avis d'experts (R2.1-R2.4, R3.1-R3.3).
"Un accord fort a ete obtenu pour toutes les preconisations des le premier
tour de cotation" (texte source, decompte verifie par transcription
integrale des 11 items - aucune recommandation a accord faible/sans accord).
Deux chips distincts utilises ici (RR / AE) - jamais fusionnes - pour
refleter cette distinction explicite du texte source entre rappel legal et
avis d'experts, meme si les deux ont recueilli un accord fort en cotation.

PERIMETRE : hors urgence et soins critiques, hors anesthesie pediatrique et
obstetricale (exclusions explicites de l'introduction du texte source) ;
hors consultation d'evaluation preoperatoire et medecine perioperatoire
(egalement hors champ) ; hors anesthesie locale seule. Integral sur les 11
preconisations. Argumentaire minimal (regle de projet 2026-09-14) : les
statistiques/etudes de risque citees a l'appui (OR, %, cohortes) ne sont pas
transcrites en detail - seuls les points cliniquement actionnables (roles
des professionnels, limites de salles/patients par MAR, proximite des
salles) sont retenus. Liste nominative des auteurs/relecteurs et les 40
references bibliographiques (23 Question 1 + 13 Question 2 + 4 Question 3,
chaque question ayant sa propre numerotation [1]..[n] dans le texte source)
ne sont pas reproduites (renvoi au texte integral).
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from style import *
GRADE_COLORS["RR"] = (NAVY, WHITE)
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.units import mm

OUT = "/home/user/rfe-sfar-website/output/Fiche_SFAR_Ressources_Humaines_Anesthesie_Programmee_2024.pdf"

SOURCE_TXT = ("Source : SFAR/CNP ARMPO, « Préconisations pour les ressources humaines "
              "médicales en anesthésie programmée », RPP, texte validé par le CA de la SFAR "
              "le 02/12/2024. Fiche de synthèse non officielle : se référer au texte intégral.")

def P(txt, style=S_CELL):
    return Paragraph(txt, style)

def chip(label, **kw):
    return grade_chip(label, **kw)

CW_FULL = PAGE_W - 2 * MARGIN

def reco_table(rows, col_widths):
    """rows: (ref, text, grade_label)."""
    data = [[P("Réf.", S_HEAD_W), P("Préconisation", S_HEAD_W), P("Statut", S_HEAD_W_C)]]
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

RCW = [17 * mm, CW_FULL - 17 * mm - 22 * mm, 22 * mm]

def bullets(items, style=S_BODY_SM):
    html = "&bull; " + "<br/>&bull; ".join(items)
    return P(html, style)

def legend_flowable():
    chip_w = 17 * mm
    content_w = CW_FULL
    row = Table([[chip("RR", width=chip_w - 2 * mm),
                  P("<b>RR = Rappel à la réglementation</b> — la question trouve sa réponse "
                    "dans un texte légal/réglementaire déjà en vigueur (4 préconisations). "
                    "<b>AE = Avis d'experts</b> — méthode GRADE grid, terminologie RPP "
                    "« les experts suggèrent » (7 préconisations). Les 11 préconisations ont "
                    "recueilli un <b>accord fort dès le premier tour de cotation</b>, sans "
                    "distinction de force entre elles — cette distinction RR/AE porte "
                    "uniquement sur la nature de la source (loi vs avis d'expert), jamais "
                    "fusionnée avec un niveau de consensus.", S_BADGE_HEAD)]],
                colWidths=[chip_w, content_w - chip_w])
    row.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                              ("LEFTPADDING", (0, 0), (-1, -1), 1),
                              ("RIGHTPADDING", (0, 0), (-1, -1), 1),
                              ("TOPPADDING", (0, 0), (-1, -1), 0),
                              ("BOTTOMPADDING", (0, 0), (-1, -1), 0)]))
    return row

TOTAL_PAGES = {"n": 3}

def on_page(canvas, doc, page_title):
    header_band(canvas, doc, "SFAR — RECOMMANDATIONS POUR LA PRATIQUE PROFESSIONNELLE, 2024",
                "Ressources humaines médicales en anesthésie programmée",
                page_title, icon_fn=lambda c, x, y: icon_shield(c, x, y, 13 * mm), color=NAVY)
    footer_band(canvas, doc, SOURCE_TXT, f"Page {doc.page} / {TOTAL_PAGES['n']}")

# ---------------------------------------------------------------------------
def _section_intro_q1():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Champ :</b> anesthésie programmée (sédation, AG, ALR axiale et/ou "
        "périphérique) hors urgence, hors soins critiques, <b>hors anesthésie "
        "pédiatrique et obstétricale</b> (fiches dédiées), hors consultation "
        "d'évaluation préanesthésique/médecine périopératoire et hors anesthésie "
        "locale seule. Objectif : cadre organisationnel des ressources humaines "
        "médicales pour sécuriser la prise en charge.", S_BODY), bg=BG_PANEL, border=NAVY))
    story.append(Spacer(1, 2.5 * mm))
    story.append(legend_flowable())
    story.append(Spacer(1, 3 * mm))
    story.append(KeepTogether([
        section_bar("Question 1 — Quelle ressource humaine pour assurer la sécurité ?"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("R1.1", "L'acte d'anesthésie est sous la <b>responsabilité exclusive d'un "
         "MAR</b> (articles R 4311-12 et R 6153-1-2 CSP).", "RR"),
        ("R1.2", "Seuls les <b>IADE</b> sont habilités à accomplir les soins et gestes "
         "d'anesthésie-réanimation peropératoire, sous le <b>contrôle exclusif d'un "
         "MAR</b> (article R 4311-12 CSP).", "RR"),
        ("R1.3", "L'acte d'anesthésie peut être réalisé par un <b>DJ-AR</b> (docteur "
         "junior) en <b>autonomie supervisée</b> (article R 6153-1-2 CSP).", "RR"),
        ("R1.4", "Un professionnel de l'anesthésie doit être présent pour assurer la "
         "<b>surveillance clinique continue</b> du patient anesthésié (articles "
         "R 4311-12 et R 6153-1-2 CSP).", "RR"),
    ], RCW))
    story.append(Spacer(1, 2.5 * mm))
    story.append(P("<b>Qui fait quoi (repères réglementaires) :</b>", S_CELL_B))
    story.append(Spacer(1, 1 * mm))
    story.append(bullets([
        "<b>MAR</b> : responsable de la stratégie anesthésique et de sa mise en œuvre ; "
        "évalue le patient en amont (acte programmé) ; identifié au dossier d'anesthésie.",
        "<b>IADE</b> : agit sous contrôle exclusif du MAR, à condition qu'un MAR soit "
        "présent sur le site et puisse intervenir sans délai (AG, réinjections d'ALR "
        "déjà posée par un MAR, surveillance du monitorage, SSPI immédiate).",
        "<b>DJ-AR</b> : autonomie supervisée sur 1 salle ; extension à 2 salles possible "
        "en phase de consolidation, après accord conjoint interne/RTS/médecin "
        "responsable du site (arrêté du 16/01/2020) ; ne peut pas pratiquer d'anesthésie "
        "délocalisée hors bloc opératoire.",
        "<b>Ne peuvent pas surveiller un patient sous anesthésie en pleine "
        "responsabilité</b>, même sous supervision d'un MAR : étudiants de 3<sup>e</sup> "
        "cycle et élèves IADE. Les IBODE, IDE de SSPI et personnels logistiques "
        "participent aux soins péri-anesthésiques sans se substituer à la surveillance "
        "de l'anesthésie elle-même.",
    ]))
    return story

# ---------------------------------------------------------------------------
def _section_q2():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Question 2 — Combien de patients/salles simultanément par MAR ?"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("R2.1", "Le MAR est <b>seul habilité</b> à décider s'il prend la responsabilité "
         "d'<b>une ou de deux salles simultanées au maximum</b>.", "AE"),
        ("R2.2", "Le MAR est seul habilité à décider de s'adjoindre l'aide d'un IADE par "
         "salle, ou d'un IADE pour deux salles.", "AE"),
        ("R2.3", "Pour des <b>ALR exclusivement périphériques</b>, le MAR peut prendre en "
         "charge plus de deux patients en phase pré-interventionnelle, sous réserve "
         "d'une surveillance continue par un IDE formé, sous supervision du MAR "
         "(article D6124-94 CSP).", "AE"),
        ("R2.4", "Lorsque le MAR a la responsabilité de deux patients simultanément, "
         "les <b>deux salles doivent être suffisamment proches</b> l'une de l'autre pour "
         "permettre son intervention sans délai.", "AE"),
    ], RCW))
    story.append(Spacer(1, 2 * mm))
    story.append(info_panel(P(
        "<b>À noter :</b> la présence d'un IADE en salle n'autorise pas une augmentation "
        "du nombre de patients pris en charge par un seul MAR — l'IADE n'est habilité à "
        "la surveillance d'une anesthésie « qu'à la condition qu'un MAR puisse intervenir "
        "à tout moment » (article R4311-12 CSP). L'usage de salles de pré-induction "
        "contiguës n'est conforme que si elles disposent du même environnement matériel "
        "et du même personnel qu'une salle d'intervention (décret de 1994) — sinon elles "
        "deviennent un site d'anesthésie à part entière, comptant dans le nombre de "
        "patients pris en charge simultanément.", S_BODY_SM), bg=GREY_LIGHT, border=GREY))
    return story

# ---------------------------------------------------------------------------
def _section_q3_sources():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Question 3 — Surveillance continue et recours en situation critique"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("R3.1", "Rédiger une <b>procédure organisationnelle</b> au sein de chaque "
         "établissement, garantissant une surveillance clinique continue de l'anesthésie "
         "par un professionnel de l'AR.", "AE"),
        ("R3.2", "Rédiger une <b>procédure de déclenchement d'un renfort</b> pour faire "
         "face à une situation critique sur le plateau interventionnel (personne(s) "
         "recours identifiée(s), moyens de la/les joindre immédiatement).", "AE"),
        ("R3.3", "Pour la <b>création de nouveaux sites d'anesthésie</b>, prévoir une "
         "architecture avec un nombre de sites suffisant, à proximité les uns des "
         "autres, pour faciliter le recours humain en cas de complication.", "AE"),
    ], RCW))
    story.append(Spacer(1, 2 * mm))
    story.append(bullets([
        "Le recours sera <b>idéalement un MAR</b> ; à défaut, dûment justifié, un médecin "
        "compétent en soins critiques, voire un IADE selon la situation (ex. aide à une "
        "transfusion massive).",
        "Toute création de site doit éviter une activité anesthésique isolée (bloc à 1-2 "
        "salles avec un seul MAR, site hors bloc/plateau technique isolé).",
    ]))
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("Sources et avertissement"))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "SFAR, à l'initiative du CNP ARMPO, « Préconisations pour les ressources "
        "humaines médicales en anesthésie programmée (hors anesthésie pédiatrique et "
        "anesthésie obstétricale) », RPP, texte validé par le CA de la SFAR le "
        "02/12/2024. Méthode GRADE grid ; 40 références bibliographiques et textes "
        "réglementaires cités dans le texte intégral (non reproduites ici).", S_SOURCE))
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Avertissement :</b> cette fiche est une synthèse indépendante, produite pour "
        "un usage d'aide-mémoire. Elle reprend intégralement les 11 préconisations du "
        "texte source mais condense l'argumentaire (études de risque, statistiques) et "
        "omet la liste nominative des auteurs/relecteurs. Elle ne remplace pas le texte "
        "intégral et n'est ni éditée ni validée par la SFAR.",
        S_BODY_SM), bg=GREY_LIGHT, border=GREY))
    return story

# ---------------------------------------------------------------------------
def _section_all():
    story = _section_intro_q1()
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_q2())
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_q3_sources())
    return story

SECTIONS = [
    ("Ressources humaines médicales en anesthésie programmée", _section_all),
]

def _make_doc(path=None):
    return SimpleDocTemplate(path or OUT, pagesize=A4,
                              leftMargin=MARGIN, rightMargin=MARGIN,
                              topMargin=32 * mm, bottomMargin=16 * mm,
                              title="Fiche SFAR 2024 - Ressources humaines medicales en anesthesie programmee",
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
