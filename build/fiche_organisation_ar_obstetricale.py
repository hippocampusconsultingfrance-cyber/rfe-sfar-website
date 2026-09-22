# -*- coding: utf-8 -*-
"""
Fiche de synthese - "Organisation de l'anesthesie-reanimation obstetricale"
- Ducloy-Bouthors AS, Tourres J, Malinovsky JM, pour le groupe d'experts de
la Sfar et des societes/groupements associes (Caro, CNGOF, CNSF, SFN).
Recommandations professionnelles (RP), texte valide par le Conseil
d'administration de la Sfar le 11 decembre 2015, publie Anesth Reanim.
2016;2:206-212. 7 pages, telecharge depuis sfar.org (wp-content/
uploads/2018/03/RFE-ANREA-Organisation-de-l-anesthesie-reanimation-
obstetricale.pdf).

METHODOLOGIE : 30 Recommandations Professionnelles (RP) numerotees (RP1,
RP2.1-2.6 avec sous-items RP2.5.1-2.5.3, RP3.1-3.14, RP4.1-4.6), toutes
soumises a une cotation Delphi (echelle 1-9, 2 tours) - "un accord fort a
ete obtenu pour les 30 (100%) recommandations" (texte source explicite,
decompte verifie par transcription integrale des 30 items). PAS de grille
GRADE ni de niveaux de preuve differencies - une seule force de consensus
pour l'ensemble du texte, chippee uniformement "AF" (Accord Fort), meme
convention que fiche_bris_dentaires.py (chip unique quand la source
n'imprime qu'un seul niveau). PARTICULARITE : certaines RP relevent en outre
d'une disposition legale (decrets/arretes cites), signalees par un
asterisque (*) dans le texte source lui-meme - convention reprise ici a
l'identique (ref. "RP2.5.2*" etc.), jamais fusionnee avec le chip de
consensus.

PERIMETRE : integral sur les 30 RP et l'Annexe 1 (soins maternels de
recours, liste de conditions operationnelles). La liste nominative des
membres du groupe d'experts/groupe de lecture (page 2-3 du PDF source) et
les 9 references bibliographiques ne sont pas transcrites (renvoi au texte
integral) - non actionnable cliniquement, conformement a la regle de
projet 2026-09-14 (argumentaire minimal).
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from style import *
GRADE_COLORS["AF"] = (GREEN, WHITE)
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.units import mm

OUT = "/home/user/rfe-sfar-website/output/Fiche_SFAR_Organisation_AR_Obstetricale_2016.pdf"

SOURCE_TXT = ("Source : Ducloy-Bouthors AS, Tourres J, Malinovsky JM (Sfar/Caro/CNGOF/CNSF/SFN), "
              "« Organisation de l'anesthésie-réanimation obstétricale », RP, Anesth Réanim "
              "2016;2:206-212. Fiche de synthèse non officielle : se référer au texte intégral.")

def P(txt, style=S_CELL):
    return Paragraph(txt, style)

def chip(label, **kw):
    return grade_chip(label, **kw)

CW_FULL = PAGE_W - 2 * MARGIN

def reco_table(rows, col_widths):
    """rows: (ref, text, grade_label)."""
    data = [[P("Réf.", S_HEAD_W), P("Recommandation", S_HEAD_W), P("Consensus", S_HEAD_W_C)]]
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

RCW = [20 * mm, CW_FULL - 20 * mm - 22 * mm, 22 * mm]

def bullets(items, style=S_BODY_SM):
    html = "&bull; " + "<br/>&bull; ".join(items)
    return P(html, style)

def legend_flowable():
    chip_w = 17 * mm
    content_w = CW_FULL
    row = Table([[chip("AF", width=chip_w - 2 * mm),
                  P("<b>AF = Accord Fort</b> — cotation Delphi (échelle 1-9, 2 tours) : "
                    "accord fort obtenu pour les 30 recommandations (100 %), aucune "
                    "recommandation à accord faible. Les références suivies d'un "
                    "<b>astérisque (*)</b> relèvent en outre d'une <b>disposition légale ou "
                    "réglementaire</b> (décret/arrêté cité dans le texte source) — convention "
                    "reprise telle quelle du texte source.", S_BADGE_HEAD)]],
                colWidths=[chip_w, content_w - chip_w])
    row.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                              ("LEFTPADDING", (0, 0), (-1, -1), 1),
                              ("RIGHTPADDING", (0, 0), (-1, -1), 1),
                              ("TOPPADDING", (0, 0), (-1, -1), 0),
                              ("BOTTOMPADDING", (0, 0), (-1, -1), 0)]))
    return row

TOTAL_PAGES = {"n": 4}

def on_page(canvas, doc, page_title):
    header_band(canvas, doc, "SFAR — RECOMMANDATIONS PROFESSIONNELLES, 2016",
                "Organisation de l'anesthésie-réanimation obstétricale",
                page_title, icon_fn=lambda c, x, y: icon_shield(c, x, y, 13 * mm), color=TEAL_DARK)
    footer_band(canvas, doc, SOURCE_TXT, f"Page {doc.page} / {TOTAL_PAGES['n']}")

# ---------------------------------------------------------------------------
def _section_intro_locaux_personnel():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Résumé :</b> ces 30 Recommandations Professionnelles (RP) portent sur "
        "l'organisation de l'anesthésie, de l'analgésie et de la réanimation dans les "
        "établissements habilités à pratiquer l'obstétrique. Objectif : réduire la "
        "morbidité maternelle par une prise en charge pluridisciplinaire et "
        "multiprofessionnelle coordonnée (obstétricien, sage-femme, anesthésiste-"
        "réanimateur, pédiatre, IADE, IBODE...). Élaborées avec le Caro, le CNGOF, le "
        "CNSF et la Société française de néonatologie.", S_BODY), bg=BG_PANEL, border=TEAL))
    story.append(Spacer(1, 2.5 * mm))
    story.append(legend_flowable())
    story.append(Spacer(1, 3 * mm))
    story.append(KeepTogether([
        section_bar("Locaux, équipements et matériels"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("RP1*", "Chaque établissement habilité à exercer l'obstétrique dispose des "
         "locaux/équipements nécessaires : accès permanent à ≥ 1 salle d'intervention "
         "dédiée à la chirurgie obstétricale d'urgence, contiguë au secteur de "
         "naissance ; équipement d'analgésie/anesthésie-réanimation obstétricales "
         "conforme au décret n°94-1050 dans chaque salle d'accouchement (fixe et/ou "
         "chariot mobile) ; chariot d'urgence adapté aux situations critiques "
         "obstétricales ; accès aux produits sanguins labiles/stables ; procédures de "
         "vérification, maintenance et matériovigilance tracées.", "AF"),
    ], RCW))
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Personnels, effectifs et permanence de soins"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("RP2.1*", "Quel que soit le nombre d'accouchements, l'anesthésiste-réanimateur "
         "doit être disponible dans des délais compatibles avec l'impératif de "
         "sécurité.", "AF"),
        ("RP2.2", "L'anesthésiste-réanimateur dispose de l'assistance d'un ou plusieurs "
         "personnels supplémentaires pour l'activité non programmée (options : 2e "
         "anesthésiste, anesthésiste en formation, IADE, IDE formé(e) à la SSPI, "
         "personnel médical/paramédical obstétrical) — identifié(s) quotidiennement "
         "dans la charte de fonctionnement.", "AF"),
        ("RP2.3", "L'adéquation des ressources humaines dédiées à l'obstétrique tient "
         "compte : du nombre d'accouchements et des épisodes de suractivité/charge des "
         "grossesses à haut risque (effectifs des consultations préanesthésiques "
         "comptés séparément) ; de l'identification et de la hiérarchisation des "
         "situations à risque (patiente, tâches, compétence, équipe, environnement, "
         "organisation).", "AF"),
        ("RP2.4", "Ces ressources sont revues à périodicité définie de 2 ans maximum, "
         "selon les résultats de l'analyse des événements indésirables associés aux "
         "soins (EIAS) et l'évolution du nombre annuel d'accouchements.", "AF"),
        ("RP2.5", "Anticiper et optimiser la sécurité de la prise en charge par une mise "
         "à disposition de ressources d'anesthésie-réanimation identifiées et "
         "organisées au sein de chaque structure.", "AF"),
        ("RP2.5.1", "Si activité < 2000 accouchements/an et anesthésiste non dédié : "
         "organisation hiérarchisée assurant sécurité/continuité des soins dans les "
         "secteurs mutualisés, avec priorité à l'obstétrique urgente.", "AF"),
        ("RP2.5.2*", "Si activité > 2000 accouchements/an : l'anesthésiste-réanimateur "
         "doit être dédié au secteur naissance (décret n°98-900).", "AF"),
        ("RP2.5.3", "Au-delà de 2000 accouchements/an : personnel soignant suffisant + "
         "organisation écrite, connue et validée de renfort ponctuel.", "AF"),
        ("RP2.6*", "Ces organisations sont opérationnelles 24 h/24 pour assurer la "
         "continuité et la permanence des soins.", "AF"),
    ], RCW))
    return story

# ---------------------------------------------------------------------------
def _section_parcours():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Parcours de soins — Procédures"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(P("<b>Consultation préanesthésique</b>", S_CELL_B))
    story.append(Spacer(1, 1 * mm))
    story.append(reco_table([
        ("RP3.1*", "Consultation préanesthésique obligatoire et réglementaire : évaluer "
         "le risque anesthésique, proposer une stratégie analgésique/anesthésique, "
         "informer la patiente ; visite préanesthésique avant l'acte.", "AF"),
        ("RP3.2", "En l'absence de consultation/visite préanesthésique : interrogatoire "
         "+ examen clinique minimal compatible avec le degré d'urgence, en s'assurant "
         "de l'absence de contre-indication apparente au geste.", "AF"),
    ], RCW))
    story.append(Spacer(1, 2 * mm))
    story.append(P("<b>Analgésie en salle de travail</b>", S_CELL_B))
    story.append(Spacer(1, 1 * mm))
    story.append(reco_table([
        ("RP3.3", "Procédure d'analgésie obstétricale (périmédullaire ou autre) "
         "organisée et consignée dans la charte : demande relayée par sage-femme/"
         "obstétricien ; personnels identifiés pour la mise en place, l'entretien et la "
         "surveillance mère/fœtus ; protocoles écrits de gestion des complications ; "
         "modalités de retrait du cathéter et surveillance du post-partum.", "AF"),
    ], RCW))
    story.append(Spacer(1, 2 * mm))
    story.append(P("<b>Anesthésie-réanimation en salle d'intervention (chirurgie obstétricale)</b>",
                    S_CELL_B))
    story.append(Spacer(1, 1 * mm))
    story.append(reco_table([
        ("RP3.4*", "Appliquer et consigner dans la charte du bloc/secteur de naissance "
         "les directives des décrets n°94-1050 et n°98-900.", "AF"),
        ("RP3.5", "Établir avec l'équipe obstétricale un code de communication "
         "définissant clairement le degré d'urgence de l'intervention.", "AF"),
        ("RP3.6*", "Le dossier d'anesthésie-réanimation comporte la consultation "
         "préanesthésique et l'ensemble des données/événements liés à la patiente, à "
         "l'intervention et à l'analgésie/anesthésie — partie intégrante du dossier "
         "médical.", "AF"),
    ], RCW))
    story.append(Spacer(1, 2 * mm))
    story.append(P("<b>Réanimation du nouveau-né en salle de naissance/césarienne</b>", S_CELL_B))
    story.append(Spacer(1, 1 * mm))
    story.append(reco_table([
        ("RP3.7", "Identifier avant chaque naissance un membre de l'équipe pour "
         "accueillir le nouveau-né ; présence anticipée d'un pédiatre formé si risque "
         "materno-fœtal. À défaut en situation urgente, l'anesthésiste-réanimateur peut "
         "participer aux premiers soins/initier la réanimation néonatale en attendant "
         "l'équipe pédiatrique (formation à la réanimation néonatale souhaitable).", "AF"),
    ], RCW))
    story.append(Spacer(1, 2 * mm))
    story.append(P("<b>Surveillance post-anesthésique et post-interventionnelle</b>", S_CELL_B))
    story.append(Spacer(1, 1 * mm))
    story.append(reco_table([
        ("RP3.8*", "Surveillance postanesthésique continue, par personnel dédié et "
         "formé ; communication organisée avec l'équipe obstétricale, décisions "
         "écrites.", "AF"),
        ("RP3.9*", "Surveillance effectuée en SSPI (proche de la salle dédiée aux "
         "césariennes, ou centralisée avec personnel dédié 24 h/24) ou en salle de "
         "travail si personnel dédié et formé présent.", "AF"),
        ("RP3.10", "Organisation de cette surveillance prévue et écrite dans la charte "
         "du secteur de naissance.", "AF"),
        ("RP3.11", "Dispositions architecturales et procédures favorisant la relation "
         "mère-père-nouveau-né ; modalités de surveillance du nouveau-né précisées.", "AF"),
    ], RCW))
    story.append(Spacer(1, 2 * mm))
    story.append(P("<b>Réhabilitation post-partum</b>", S_CELL_B))
    story.append(Spacer(1, 1 * mm))
    story.append(reco_table([
        ("RP3.12", "Prise en charge de la douleur et programme de réhabilitation rapide "
         "pluridisciplinaire après accouchement (voie basse ou césarienne).", "AF"),
    ], RCW))
    story.append(Spacer(1, 2 * mm))
    story.append(P("<b>Surveillance continue et réanimation en obstétrique</b>", S_CELL_B))
    story.append(Spacer(1, 1 * mm))
    story.append(reco_table([
        ("RP3.13", "Anticiper/organiser la surveillance continue des patientes à risque "
         "de défaillance d'organe (pathologie obstétricale sévère ou maternelle "
         "compliquée par la grossesse) ; orientation vers une unité de réanimation "
         "adulte selon convention établie si l'établissement n'en dispose pas.", "AF"),
        ("RP3.14*", "La convention précise le partage du dossier et de la feuille de "
         "surveillance, la traçabilité des produits sanguins administrés, les critères "
         "et conditions du transfert.", "AF"),
    ], RCW))
    return story

# ---------------------------------------------------------------------------
def _section_qualite_annexe():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Qualité des soins — Formation — Évaluation"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("RP4.1", "Mettre en place des protocoles de soins et des démarches "
         "d'évaluation/amélioration de la qualité en équipe par analyses de "
         "morbimortalité (équipe médicale et paramédicale d'anesthésie-réanimation "
         "obstétricale).", "AF"),
        ("RP4.2", "Mettre en place ces démarches de gestion des risques "
         "interdisciplinaires et pluriprofessionnelles incluant les personnels "
         "d'anesthésie-réanimation, au sein du réseau de périnatalité.", "AF"),
        ("RP4.3*", "Prévoir les orientations et modalités de transfert entre "
         "maternités selon les recommandations HAS 2012 (transferts in utero) et la "
         "circulaire du 21 juin 2006.", "AF"),
        ("RP4.4*", "Consigner dans la convention les conditions de prise en charge "
         "anesthésique des patientes transférées d'une maison de naissance "
         "expérimentale (consultation d'anesthésie, procédure opérationnelle, gestion "
         "des risques a priori).", "AF"),
        ("RP4.5*", "Dans le cadre du DPC, actualiser les compétences et participer à "
         "l'évaluation des pratiques professionnelles individuelles et collectives, "
         "dont les revues de morbimortalité.", "AF"),
        ("RP4.6", "Mettre en place des démarches d'évaluation/amélioration de la "
         "qualité en équipe : procédures validées de situation de crise (césarienne "
         "urgente code couleur, check-list), analyse des EIAS en RMM/CREX, formation "
         "en équipe à la communication et à la simulation, suivi d'indicateurs "
         "(IPAQSS, taux d'HPP grave, taux de transfusion, taux de césarienne, délai "
         "décision-incision).", "AF"),
    ], RCW))
    story.append(Spacer(1, 3 * mm))
    story.append(KeepTogether([
        section_bar("Annexe 1 — Soins maternels de recours"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(P(
        "Les soins maternels de recours définissent l'accès aux soins d'urgence et de "
        "réanimation maternelle, indépendamment du type de soins de néonatologie — une "
        "pathologie maternelle et fœtale simultanée conduit à les associer comme "
        "éléments d'orientation du transfert. Conditions opérationnelles, à titre "
        "indicatif :", S_BODY_SM))
    story.append(Spacer(1, 1 * mm))
    story.append(bullets([
        "Équipe de recours d'anesthésie-réanimation dédiée aux situations obstétricales "
        "critiques et détachable des soins cliniques courants",
        "Salle d'intervention chirurgicale accessible et disponible 24 h/24",
        "Procédures et protocoles multidisciplinaires pour pathologies préexistantes à "
        "la grossesse et pathologies gravidiques",
        "Moyens de communication téléphoniques, fax et informatiques",
        "Laboratoire d'immunohématologie",
        "Stock de concentrés érythrocytaires d'urgence vitale + procédure de "
        "réapprovisionnement à partir d'un dépôt conventionné",
        "Centre de réanimation adulte conventionné (composante réanimation "
        "obstétricale ou unité de soins continus maternels)",
        "Centre d'embolisation",
        "Organisation en réseau de santé en périnatalité incluant les SAMU, prévoyant "
        "et régulant les procédures de transfert et d'orientation",
    ]))
    return story

# ---------------------------------------------------------------------------
def _section_sources():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("Sources et avertissement"))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "Ducloy-Bouthors AS, Tourres J, Malinovsky JM, pour le groupe d'experts de la "
        "Sfar et des sociétés/groupements professionnels associés (Caro, CNGOF, CNSF, "
        "SFN), « Organisation de l'anesthésie-réanimation obstétricale », "
        "Recommandations Professionnelles, texte validé par le Conseil d'administration "
        "de la Sfar le 11 décembre 2015, Anesth Réanim 2016;2:206-212. 9 références "
        "bibliographiques et textes réglementaires cités dans le texte intégral (non "
        "reproduits ici).", S_SOURCE))
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Avertissement :</b> cette fiche est une synthèse indépendante, produite pour "
        "un usage d'aide-mémoire. Elle reprend intégralement les 30 Recommandations "
        "Professionnelles et l'Annexe 1 du texte source, mais condense le préambule "
        "méthodologique et omet la liste nominative des experts. Elle ne remplace pas le "
        "texte intégral et n'est ni éditée ni validée par la Sfar. Le cadre réglementaire "
        "cité (décrets de 1994/1998, circulaire de 2006) date de la publication (2016) — "
        "vérifier l'actualité des textes réglementaires avant application.",
        S_BODY_SM), bg=GREY_LIGHT, border=GREY))
    return story

# ---------------------------------------------------------------------------
def _section_all():
    story = _section_intro_locaux_personnel()
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_parcours())
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_qualite_annexe())
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_sources())
    return story

SECTIONS = [
    ("Locaux, personnels, parcours de soins, qualité, annexe & sources", _section_all),
]

def _make_doc(path=None):
    return SimpleDocTemplate(path or OUT, pagesize=A4,
                              leftMargin=MARGIN, rightMargin=MARGIN,
                              topMargin=32 * mm, bottomMargin=16 * mm,
                              title="Fiche SFAR 2016 - Organisation de l'anesthesie-reanimation obstetricale",
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
