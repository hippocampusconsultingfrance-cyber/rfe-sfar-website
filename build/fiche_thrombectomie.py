# -*- coding: utf-8 -*-
"""
Fiche de synthese - "Prise en charge anesthesique peri-procedurale d'une
revascularisation cerebrale par thrombectomie" - Recommandations de Pratiques
Professionnelles (RPP), SFAR en association avec l'ANARLF, avec la participation
de la SFNR, de la SFNV et du GFHT. Texte valide par le Comite des Referentiels
Cliniques de la SFAR le 16/05/2022, le CA de la SFAR le 29/06/2022, le bureau de
l'ANARLF le 29/06/2022, le CS/CA de la SFNV le 07/10/2022 et le CS de la SFNR le
16/08/2022. Auteurs : H. Quintard, V. Degos et al. Source telechargee :
sfar.org/download/prise-en-charge-anesthesique-peri-procedurale-dune-
revascularisation-cerebrale-par-thrombectomie/?wpdmdl=37892 (33 pages).

METHODOLOGIE : format RPP (Recommandations pour la Pratique Professionnelle) et
non RFE - choix explicitement motive par la source (faible quantite d'etudes
repondant avec la puissance necessaire au critere de jugement majeur). La
methodologie GRADE(R) a neanmoins ete appliquee pour l'analyse de la litterature
(niveau de preuve par reference bibliographique). Toutes les 18 preconisations
formalisees portent la MEME mention imprimee : "Avis d'experts (Accord fort)" -
accord fort obtenu pour 100% des recommandations apres 2 tours de cotation GRADE
Grid. Aucune distinction GRADE 1+/1-/2+/2- individuelle n'existe dans ce document
(a la difference de la majorite du corpus) - chip unique "AE" pour les 18
preconisations, jamais un grade numerique invente. 15 questions ont ete traitees
sur 4 champs ; 2 d'entre elles n'ont debouche sur AUCUNE recommandation
("ABSENCE DE RECOMMANDATION" imprime tel quel par la source) - reproduites
comme telles, jamais omises ni transformees en avis negatif.

ARGUMENTAIRE : condense au strict necessaire (regle de projet 2026-09-14) - la
source consacre un tres long developpement narratif par question (16 sections
"Argumentaire" distinctes, chacune avec sa propre liste de references numerotee
localement 1-n, restant a ce jour non consolidees en une bibliographie globale
unique) recapitulant en detail chaque etude citee. Cette fiche NE reproduit PAS
ces developpements ni les references associees : le texte de chaque
preconisation (integralement conserve, c'est lui qui porte l'information
actionnable - cibles de PA/SpO2/etCO2, criteres de choix anesthesique, etc.) est
deja auto-suffisant. Seules les rares precisions qui changent reellement la
pratique sans etre deja dans la ligne de recommandation elle-meme sont ajoutees
en 1-2 phrases. Se referer au texte integral pour le detail des etudes et leurs
references completes.

COUVERTURE : integralite des 4 champs, des 18 preconisations (texte complet +
grade), des 2 questions sans recommandation (disclosure explicite), de la
methodologie et de la declaration relative aux conflits d'interets. Bibliographie
(16 listes locales, non consolidee) explicitement exclue du champ de cette fiche
- disclosure en section Sources.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from style import *
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.units import mm

OUT = "/home/user/rfe-sfar-website/output/Fiche_SFAR_ANARLF_Thrombectomie_2022.pdf"

SOURCE_TXT = ("Source : « Prise en charge anesthésique péri-procédurale d'une "
              "revascularisation cérébrale par thrombectomie » — SFAR/ANARLF/SFNR/"
              "SFNV/GFHT, RPP 2022. Fiche de synthèse non officielle : se référer "
              "au texte intégral.")

def P(txt, style=S_CELL):
    return Paragraph(txt, style)

def chip(label, **kw):
    return grade_chip(label, **kw)

def reco_table(rows, col_widths):
    """rows: (ref, text, grade_label)"""
    data = [[P("Réf.", S_HEAD_W_C), P("Recommandation", S_HEAD_W), P("Accord", S_HEAD_W_C)]]
    for ref, txt, grade in rows:
        data.append([P(ref, S_CELL_B), P(txt, S_CELL), chip(grade)])
    t = Table(data, colWidths=col_widths, repeatRows=1)
    style_cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), NAVY), ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTNAME", (0, 0), (-1, 0), FONT_BOLD), ("FONTSIZE", (0, 0), (-1, 0), 8),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("ALIGN", (0, 0), (0, -1), "CENTER"),
        ("ALIGN", (2, 0), (2, -1), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 0.5, GREY_LIGHT),
        ("TOPPADDING", (0, 0), (-1, -1), 3.4), ("BOTTOMPADDING", (0, 0), (-1, -1), 3.4),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            style_cmds.append(("BACKGROUND", (0, i), (-1, i), BG_PANEL))
    t.setStyle(TableStyle(style_cmds))
    return t

def no_reco_panel(question, text):
    return info_panel(P(f"<b>Absence de recommandation</b> — <i>{question}</i><br/>{text}",
                         S_BODY_SM), bg=GREY_LIGHT, border=GREY)

def bullets(items, style=S_CELL):
    html = "&bull; " + "<br/>&bull; ".join(items)
    return P(html, style)

def legend_flowable():
    chip_w = 18 * mm
    content_w = PAGE_W - 2 * MARGIN
    text_w = content_w - chip_w
    row = Table([[chip("AE", width=chip_w - 2 * mm),
                  P("Les 18 préconisations de ce document portent toutes la même "
                    "mention imprimée par la source : <b>« Avis d'experts (Accord "
                    "fort) »</b> — format RPP, pas de distinction GRADE 1+/1-/2+/2- "
                    "individuelle (voir disclosure méthodologique en page 1).",
                    S_BADGE_HEAD)]], colWidths=[chip_w, text_w])
    row.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                              ("LEFTPADDING", (0, 0), (-1, -1), 1),
                              ("RIGHTPADDING", (0, 0), (-1, -1), 1)]))
    return row

RCW = [14 * mm, PAGE_W - 2 * MARGIN - 14 * mm - 18 * mm, 18 * mm]

TOTAL_PAGES = {"n": 4}

def on_page(canvas, doc, page_title):
    header_band(canvas, doc, "SFAR / ANARLF — RPP 2022 — FICHE DE SYNTHÈSE",
                "Thrombectomie cérébrale — prise en charge anesthésique",
                page_title, icon_fn=lambda c, x, y: icon_shield(c, x, y, 13 * mm), color=NAVY)
    footer_band(canvas, doc, SOURCE_TXT, f"Page {doc.page} / {TOTAL_PAGES['n']}")

# ---------------------------------------------------------------------------
def _section_intro():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Champ :</b> recommandations sur la prise en charge anesthésique et "
        "péri-interventionnelle lors d'une procédure de thrombectomie mécanique "
        "(TM) chez les patients victimes d'un AVC ischémique par occlusion "
        "artérielle cérébrale. Comité de 15 experts (SFAR, ANARLF, SFNV, SFNR) "
        "sous la supervision de 2 coordonnateurs. Processus mené indépendamment "
        "de tout financement industriel. 4 champs : (1) modalités de prise en "
        "charge per-interventionnelle (type d'anesthésie), (2) gestion des ACSOS "
        "(agressions cérébrales secondaires d'origine systémique), (3) gestion "
        "des antiagrégants plaquettaires et anticoagulants, (4) gestion "
        "post-interventionnelle et orientation.",
        S_BODY), bg=BG_PANEL, border=TEAL))
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Méthodologie :</b> format <b>RPP</b> (Recommandations pour la "
        "Pratique Professionnelle) plutôt que RFE — choix motivé par la source "
        "elle-même (trop peu d'études de puissance suffisante sur le critère de "
        "jugement majeur, le pronostic neurologique à 3 mois/score de Rankin). "
        "La méthodologie GRADE® a néanmoins guidé l'analyse de la littérature "
        "(niveau de preuve par référence). 15 questions traitées sur les 4 "
        "champs ; 18 préconisations formalisées, <b>toutes accord fort après 2 "
        "tours de cotation</b> ; 2 questions n'ont donné lieu à <b>aucune "
        "recommandation</b> (littérature insuffisante), disclosure explicite "
        "reproduite telle quelle plutôt qu'omise.", S_BODY_SM),
        bg=AMBER_LIGHT, border=AMBER))
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("Légende"))
    story.append(Spacer(1, 2 * mm))
    story.append(legend_flowable())
    return story

def _section_champ1():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Champ 1 — Modalités de prise en charge per-interventionnelle"),
        Spacer(1, 1.5 * mm),
        P("<b>Question :</b> l'anesthésie locale seule, comparativement à "
          "l'anesthésie générale (AG) ou à la sédation procédurale (SP), "
          "permet-elle d'améliorer le pronostic neurologique à 3 mois ?",
          S_BODY_SM),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("R1.1.1", "Les experts suggèrent de privilégier l'AG avec intubation "
         "orotrachéale, réalisée par une équipe anesthésique, plutôt que "
         "l'anesthésie locale seule, lorsqu'au moins une des situations "
         "suivantes est présente : atteinte de la circulation postérieure ; "
         "neuronavigation radiologique prévue délicate ; NIHSS ≥ 15 ; "
         "altération de la vigilance ; défaillance respiratoire ; agitation "
         "du patient ; vomissements.", "AE"),
        ("R1.1.2", "À l'exception des situations ci-dessus nécessitant une "
         "intubation, les experts suggèrent de ne pas privilégier l'AG par "
         "rapport à une anesthésie locale sous surveillance par une équipe "
         "d'anesthésie.", "AE"),
    ], RCW))
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        P("<b>Question :</b> la sédation procédurale (SP), comparativement à "
          "l'AG, permet-elle d'améliorer le pronostic neurologique à 3 mois ?",
          S_BODY_SM),
        Spacer(1, 1.5 * mm),
        reco_table([
            ("R1.2", "À l'exception des situations nécessitant une intubation "
             "(cf. R1.1.1), les experts suggèrent de ne pas privilégier l'AG "
             "par rapport à une SP, l'une et l'autre réalisées par une équipe "
             "anesthésique.", "AE"),
        ], RCW),
    ]))
    return story

def _section_champ2():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Champ 2 — Gestion des ACSOS"),
        Spacer(1, 1.5 * mm),
        P("<b>Question :</b> une cible de pression artérielle (PA) en "
          "post-recanalisation est-elle associée à une amélioration du "
          "pronostic neurologique à 3 mois ?", S_BODY_SM),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("R2.1.1", "En cas de recanalisation TICI &lt;2b, les experts "
         "suggèrent de maintenir une PA systolique post-procédure entre "
         "130 et 180 mmHg.", "AE"),
        ("R2.1.2", "En cas de recanalisation TICI ≥2b, les experts suggèrent "
         "de maintenir une PA systolique post-procédure entre 130 et "
         "160 mmHg.", "AE"),
        ("R2.2", "Les experts suggèrent de maintenir la SpO2 du patient "
         "≥ 95 % en per- et post-procédure.", "AE"),
        ("R2.3", "Lors des procédures sous AG, les experts suggèrent de "
         "surveiller l'etCO2 et de le maintenir entre 35 et 40 mmHg.", "AE"),
        ("R2.4", "Lors des procédures sous sédation, les experts suggèrent de "
         "monitorer en continu l'etCO2 afin de surveiller la persistance de "
         "la ventilation spontanée.", "AE"),
        ("R2.5", "Les experts suggèrent de monitorer et traiter les épisodes "
         "d'hyperglycémie, tout en évitant les hypoglycémies induites par ce "
         "contrôle.", "AE"),
    ], RCW))
    return story

def _section_intro_ch1_ch2():
    story = _section_intro()
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_champ1())
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_champ2())
    return story

# ---------------------------------------------------------------------------
def _section_champ3():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Champ 3 — Gestion des anticoagulants et antiagrégants "
                    "plaquettaires"),
        Spacer(1, 1.5 * mm),
        P("<i>Disclosure :</i> la source intitule ce champ de 3 façons "
          "légèrement différentes selon l'endroit du document (« Gestion "
          "des anticoagulants et antiagrégants plaquettaires » en en-tête "
          "de section, « Gestion des antiagrégants plaquettaires et des "
          "anticoagulants » dans le résumé des champs) — titre d'en-tête "
          "retenu ici, divergence non résolue par la source elle-même.",
          S_NOTE),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("R3.1", "Chez les patients ayant bénéficié préalablement d'une "
         "thrombolyse intraveineuse, les experts suggèrent de ne pas "
         "procéder à une héparinisation systémique en per-procédure.", "AE"),
    ], RCW))
    story.append(Spacer(1, 1.8 * mm))
    story.append(no_reco_panel(
        "chez le patient sans thrombolyse intraveineuse préalable, "
        "l'héparinisation systémique per-procédure permet-elle d'améliorer "
        "le pronostic neurologique à 3 mois ?",
        "À ce jour, la littérature disponible ne permet pas de se prononcer "
        "sur un éventuel intérêt de l'héparinisation systémique chez ces "
        "patients."))
    story.append(Spacer(1, 1.8 * mm))
    story.append(reco_table([
        ("R3.2", "En l'absence de thrombolyse intraveineuse préalable, les "
         "experts suggèrent de ne pas administrer systématiquement à tous "
         "les patients une antiagrégation plaquettaire par anti-GPIIb/IIIa "
         "ou inhibiteur direct de la thrombine ; ce traitement peut être "
         "proposé en cas d'emboles distaux pendant la procédure ou "
         "d'occlusion persistante en fin de procédure.", "AE"),
        ("R3.3", "Les experts suggèrent de ne pas administrer d'aspirine en "
         "per-procédure, que les patients aient bénéficié ou non d'une "
         "thrombolyse intraveineuse préalable, afin de ne pas augmenter le "
         "risque d'hémorragie intra-parenchymateuse symptomatique.", "AE"),
        ("R3.4.1", "Les experts suggèrent d'utiliser une antiagrégation "
         "plaquettaire (simple ou double) lors de la pose d'un stent pour "
         "éviter sa thrombose.", "AE"),
        ("R3.4.2", "Les experts suggèrent de n'initier cette antiagrégation "
         "qu'après avoir éliminé une hémorragie cérébrale par imagerie de "
         "contrôle au cours des premières 24 heures suivant le geste.", "AE"),
    ], RCW))
    return story

def _section_champ4():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Champ 4 — Prise en charge post-interventionnelle et "
                    "orientation"),
        Spacer(1, 1.5 * mm),
        P("<i>Disclosure :</i> la source intitule ce champ « Prise en "
          "charge post-interventionnelle immédiate et orientation » en "
          "en-tête de section, et « Gestion post-interventionnelle et "
          "orientation » dans le résumé des champs — divergence non "
          "résolue par la source elle-même.", S_NOTE),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("R4.1.1", "Les experts suggèrent d'arrêter les médicaments "
         "d'anesthésie dès la fin de la procédure de TM en l'absence de "
         "défaillance ventilatoire ou de complications faisant craindre une "
         "HTIC ou un état de mal épileptique.", "AE"),
        ("R4.1.2", "Les experts suggèrent d'extuber le patient immédiatement "
         "après la procédure si les prérequis habituels sont présents et "
         "l'état de vigilance satisfaisant (composante visuelle du score de "
         "Glasgow ≥ 3 ; la réponse aux ordres n'est pas nécessaire). "
         "Déglutition et toux à évaluer spécifiquement pour les occlusions "
         "de la circulation postérieure.", "AE"),
    ], RCW))
    story.append(Spacer(1, 1.8 * mm))
    story.append(no_reco_panel(
        "chez le patient ayant bénéficié d'une thrombectomie cérébrale "
        "sous anesthésie générale, une stratégie d'extubation précoce "
        "guidée par des échelles (score VISAGE, etc.) permet-elle "
        "d'améliorer la morbi-mortalité ?",
        "À ce jour, la littérature disponible ne permet pas de se prononcer "
        "sur un éventuel intérêt de l'utilisation d'échelles ou de scores "
        "pour guider l'extubation précoce dans cette population."))
    story.append(Spacer(1, 1.8 * mm))
    story.append(reco_table([
        ("R4.2", "Les experts suggèrent que le patient soit admis en unité "
         "de soins critiques, en priorité en USINV, avec surveillance "
         "clinique (glycémie, température) et monitorage (PA, SpO2, ECG), au "
         "minimum jusqu'à l'imagerie cérébrale de contrôle à H24.", "AE"),
        ("R4.3", "Les experts suggèrent de ne pas ré-adresser le patient "
         "immédiatement après la procédure vers le centre adresseur en cas "
         "d'instabilité hémodynamique, de déficit neurologique sévère "
         "(NIHSS ≥ 15), ou de résultat incomplet au contrôle de la "
         "procédure (TICI &lt;2b).", "AE"),
    ], RCW))
    return story

def _section_sources():
    story = []
    story.append(section_bar("Sources et traçabilité", color=GREY))
    story.append(Spacer(1, 2 * mm))
    story.append(P("<b>Déclaration d'intérêts :</b> une politique officielle "
                    "de gestion des conflits d'intérêts a été élaborée dès le "
                    "début du processus et appliquée tout au long de "
                    "celui-ci ; l'ensemble du processus a été mené "
                    "indépendamment de tout financement industriel.",
                    S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>Document source :</b> « Prise en charge anesthésique "
        "péri-procédurale d'une revascularisation cérébrale par "
        "thrombectomie » — RPP, SFAR en association avec l'ANARLF, avec la "
        "participation de la SFNR, de la SFNV et du GFHT. Texte validé par "
        "le Comité des Référentiels Cliniques de la SFAR (16/05/2022), le CA "
        "de la SFAR (29/06/2022), le bureau de l'ANARLF (29/06/2022), le "
        "CS/CA de la SFNV (07/10/2022) et le CS de la SFNR (16/08/2022). "
        "Auteurs : H. Quintard, V. Degos, M. Mazighi, J. Berge, P. "
        "Boussemart, R. Chabanne, S. Figueiredo, T. Geeraerts, Y. Launey, L. "
        "Meuret, J.-M. Olivot, J. Pottecher, F. Rapido, S. Richard, V. "
        "Siguret-Depasse, O. Naggara, H. De Courson, M. Garnier.",
        S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P("<b>Version :</b> 2022.", S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P("<b>Méthodologie :</b> format RPP, analyse de la "
                    "littérature selon GRADE®, cotation collective GRADE "
                    "Grid — voir détail en page 1.", S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>URL source :</b> https://sfar.org/download/prise-en-charge-"
        "anesthesique-peri-procedurale-dune-revascularisation-cerebrale-"
        "par-thrombectomie/?wpdmdl=37892", S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P("<b>Couverture :</b> intégralité des 4 champs, des 18 "
                    "préconisations (texte complet + grade) et des 2 "
                    "questions sans recommandation. La bibliographie du "
                    "document source est répartie en 16 listes de "
                    "références numérotées localement par question "
                    "(non consolidées en une liste unique) et détaille "
                    "l'argumentaire de chaque préconisation — cette fiche "
                    "condense l'argumentaire à ses éléments réellement "
                    "actionnables et exclut explicitement ces listes de "
                    "références : se référer au texte intégral pour le "
                    "détail des études.", S_SOURCE))
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Avertissement — document de 2022 :</b> ce document est une "
        "fiche de synthèse indépendante, produite pour un usage "
        "d'aide-mémoire. Elle reprend l'intégralité des 18 préconisations "
        "et des 2 disclosures d'absence de recommandation, mais ne "
        "remplace pas le texte intégral (argumentaire complet, références "
        "bibliographiques) et n'est ni éditée ni validée par la SFAR, "
        "l'ANARLF, la SFNR, la SFNV ou le GFHT. En cas de doute, se référer "
        "au texte intégral et/ou à un avis spécialisé.",
        S_BODY_SM), bg=GREY_LIGHT, border=GREY))
    return story

def _section_champ3_champ4_sources():
    story = _section_champ3()
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_champ4())
    story.append(Spacer(1, 4 * mm))
    story.extend(_section_sources())
    return story

def _section_all():
    story = _section_intro_ch1_ch2()
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_champ3_champ4_sources())
    return story

SECTIONS = [
    ("Méthodologie, 4 champs (18 préconisations) & sources", _section_all),
]

def _make_doc(path=None):
    return SimpleDocTemplate(path or OUT, pagesize=A4,
                              leftMargin=MARGIN, rightMargin=MARGIN,
                              topMargin=32 * mm, bottomMargin=16 * mm,
                              title="Fiche SFAR 2022 - Thrombectomie cerebrale - prise en charge anesthesique",
                              author="Synthèse indépendante (source SFAR/ANARLF)")

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
    # NOTE: pypdf/cryptography is broken in this container (pyo3 panic on
    # import) - use PyMuPDF (fitz) instead. Also: this MUST write to a fresh
    # tempfile, never to OUT - reusing OUT for both the throwaway measurement
    # build and the final build was found to silently corrupt page 1's
    # header_band in the final PDF (see CLAUDE.md build pipeline step 5).
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

    final_story = _build_upto(fns)

    doc = _make_doc()
    page_counter = {"n": 0}

    def _on_first(canvas, doc_):
        page_counter["n"] = 1
        on_page(canvas, doc_, page_titles[0])

    def _on_later(canvas, doc_):
        page_counter["n"] += 1
        idx = min(page_counter["n"] - 1, len(page_titles) - 1)
        on_page(canvas, doc_, page_titles[idx])

    doc.build(final_story, onFirstPage=_on_first, onLaterPages=_on_later)
    print(f"OK -> {OUT} ({total_pages} pages)")

if __name__ == "__main__":
    build()
