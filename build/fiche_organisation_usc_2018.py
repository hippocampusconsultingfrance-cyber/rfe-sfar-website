# -*- coding: utf-8 -*-
"""
Fiche de synthese - "Recommandations pour le fonctionnement des Unites de
Surveillance Continue (USC) dans les Etablissements de Sante" - texte
elabore par les Conseils Nationaux Professionnels de Medecine Intensive
Reanimation, Anesthesie-Reanimation et Medecine d'Urgence, 2018. 62
pages, telecharge depuis sfar.org (wpdmdl non applicable, URL directe
wp-content).

METHODOLOGIE : convention "Accord Fort" uniforme (pas de grille GRADE
1+/1-/2+/2- imprimee) - chaque recommandation est suivie de la seule
mention "Accord Fort", sans niveau de preuve ni avis d'experts distinct.
Meme pattern deja rencontre dans ce corpus pour fiche_bris_dentaires.py
(chip local "Fort", GREEN/WHITE, deja defini dans style.py - reutilise
tel quel ici, pas de nouvelle definition necessaire).

DECOMPTE : 26 recommandations numerotees (R1.1-R1.5, R2.1-R2.7,
R3.1-R3.5, R4.1-R4.5, R5.1-R5.4) sur 5 champs, toutes "Accord Fort".
Decompte verifie par extraction integrale, motif de numerotation
regulier sans saut ni doublon trouve (contrairement a plusieurs autres
fiches RPP/RFE de ce corpus).

PERIMETRE : integral sur les 5 champs (typologie des patients ; structure
des USC ; organisation et management paramedical ; organisation et
management medical ; USC dans le contexte des GHT) et les 26
recommandations. Le Tableau 4 du source (criteres d'admission en USC de
l'American College of Critical Care, une reference externe reproduite
dans le texte source, pas une recommandation SFAR propre) est retranscrit
en tableau condense par appareil - directement actionnable pour une
decision d'admission. L'Annexe 1 (liste des actes consommateurs de temps
IDE, utilisee pour le calcul des ratios de personnel) et les Tableaux
1-3 (elements de valorisation tarifaire, avantages/inconvenients
organisationnels, charge en soins) ne sont pas retranscrits en detail -
administratifs/methodologiques, non directement actionnables au chevet.
Bibliographie et composition nominative du groupe de travail non
reproduites. Argumentaire minimal (regle de projet 2026-09-14) : le texte
narratif entre les recommandations (justifications, references
bibliographiques) n'est pas transcrit - seul l'enonce actionnable de
chaque recommandation est retenu.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from style import *
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.units import mm

OUT = "/home/user/rfe-sfar-website/output/Fiche_CNP_Organisation_USC_2018.pdf"

SOURCE_TXT = ("Source : Conseils Nationaux Professionnels (Médecine Intensive Réanimation, "
              "Anesthésie-Réanimation, Médecine d'Urgence), « Recommandations pour le "
              "fonctionnement des USC dans les établissements de santé », 2018. Fiche de "
              "synthèse non officielle : se référer au texte intégral.")

def P(txt, style=S_CELL):
    return Paragraph(txt, style)

def chip(label, **kw):
    return grade_chip(label, **kw)

CW_FULL = PAGE_W - 2 * MARGIN

def reco_table(rows, col_widths):
    """rows: (ref, text, grade_label)."""
    data = [[P("Réf.", S_HEAD_W), P("Recommandation", S_HEAD_W), P("Grade", S_HEAD_W_C)]]
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

RCW = [15 * mm, CW_FULL - 15 * mm - 18 * mm, 18 * mm]

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

TCW = [40 * mm, CW_FULL - 40 * mm]

def legend_flowable():
    chip_w = 20 * mm
    content_w = CW_FULL
    row = Table([[chip("Fort", width=chip_w - 2 * mm),
                  P("Convention de ce document : chaque recommandation est suivie de la "
                    "seule mention <b>« Accord Fort »</b> — pas de grille GRADE numérique, "
                    "pas de distinction avis d'experts/recommandation graduée. 26 "
                    "recommandations, toutes à accord fort, sur 5 champs. Aucune absence de "
                    "recommandation dans ce document.", S_BADGE_HEAD)]],
                colWidths=[chip_w] + [content_w - chip_w])
    row.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                              ("LEFTPADDING", (0, 0), (-1, -1), 1),
                              ("RIGHTPADDING", (0, 0), (-1, -1), 1),
                              ("TOPPADDING", (0, 0), (-1, -1), 0),
                              ("BOTTOMPADDING", (0, 0), (-1, -1), 0)]))
    return row

TOTAL_PAGES = {"n": 5}

def on_page(canvas, doc, page_title):
    header_band(canvas, doc, "CNP MIR / AR / MU — RECOMMANDATIONS, 2018",
                "Fonctionnement des Unités de Surveillance Continue (USC)",
                page_title, icon_fn=lambda c, x, y: icon_shield(c, x, y, 13 * mm), color=TEAL_DARK)
    footer_band(canvas, doc, SOURCE_TXT, f"Page {doc.page} / {TOTAL_PAGES['n']}")

# ---------------------------------------------------------------------------
def _section_intro_champ1_2():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Résumé :</b> recommandations conjointes des Conseils Nationaux Professionnels "
        "de Médecine Intensive Réanimation, Anesthésie-Réanimation et Médecine d'Urgence "
        "(2018) sur l'organisation des Unités de Surveillance Continue (USC) — « soins "
        "intermédiaires » entre unité standard et réanimation. 26 recommandations (accord "
        "fort) sur 5 champs : typologie des patients, structure des USC, organisation "
        "paramédicale, organisation médicale, USC dans le contexte des GHT.", S_BODY),
        bg=BG_PANEL, border=TEAL_DARK))
    story.append(Spacer(1, 2.5 * mm))
    story.append(legend_flowable())
    story.append(Spacer(1, 3 * mm))
    story.append(KeepTogether([
        section_bar("Champ 1 — Typologie des patients"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("R1.1", "Sélectionner les patients pris en charge en USC dans un objectif de "
         "sécurité médicale, et non d'éligibilité à un tarif.", "Fort"),
        ("R1.2", "Organiser les USC pour prendre en charge des patients à risque de "
         "défaillance vitale nécessitant une surveillance rapprochée, avec capacité de "
         "faire face à la défaillance et de préparer un transfert rapide en réanimation.",
         "Fort"),
        ("R1.3", "Adapter les moyens et compétences des USC aux filières de "
         "l'établissement (post-opératoire, urgences, post-réanimation, activités à "
         "risque) ; dans les centres sans réanimation, tenir compte des délais de "
         "transfert.", "Fort"),
        ("R1.4", "Les USC n'ont pas pour mission d'assurer la suppléance d'organe des "
         "patients en défaillance, en dehors de la préparation d'un transfert en "
         "réanimation.", "Fort"),
        ("R1.5", "Les USC ne doivent pas recevoir de patients pour engager un processus de "
         "fin de vie.", "Fort"),
    ], RCW))
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Champ 2 — Structure des USC"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("R2.1", "L'existence de lits d'USC dans une structure hospitalière devrait être "
         "soumise à autorisation.", "Fort"),
        ("R2.2", "Si l'établissement comporte une unité de réanimation, l'USC doit être "
         "placée sous la même autorité médicale et paramédicale que cette unité.", "Fort"),
        ("R2.3", "Une USC doit avoir un projet médical et paramédical qui lui est "
         "spécifique.", "Fort"),
        ("R2.4", "Sans unité de réanimation sur site, la mission et l'organisation de "
         "l'USC doivent être précisées et intégrées au projet médical des soins critiques "
         "du GHT.", "Fort"),
        ("R2.5", "Avec unité de réanimation, les lits d'USC peuvent être intégrés à cette "
         "unité ou constituer une unité distincte à proximité.", "Fort"),
        ("R2.6", "Regrouper le plus possible les lits de soins critiques au sein d'une "
         "structure hospitalière.", "Fort"),
        ("R2.7", "Ne pas descendre, hors particularités géographiques, en dessous de 6 "
         "lits pour une USC.", "Fort"),
    ], RCW))
    return story

# ---------------------------------------------------------------------------
def _section_champ3_4():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Champ 3 — Organisation et management paramédical"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("R3.1", "L'équipe paramédicale d'une USC doit faire l'objet d'une organisation et "
         "d'un projet de soins spécifiques.", "Fort"),
        ("R3.2", "Les paramédicaux exerçant en USC doivent recevoir une formation "
         "d'adaptation à l'emploi spécifique aux patients à risque de défaillance vitale.",
         "Fort"),
        ("R3.3", "Cette formation doit aborder les aspects techniques, de prévention/"
         "qualité, et humains/psychologiques.", "Fort"),
        ("R3.4", "L'effectif paramédical (IDE + AS) physiquement présent et affecté aux "
         "soins doit être ≥ 0,4 par lit ouvert.", "Fort"),
        ("R3.5", "Avec réanimation sur site, mutualiser le planning IDE entre USC et "
         "réanimation (rotation des personnels) ; sans réanimation, mutualiser avec les "
         "autres soins critiques (urgences, soins intensifs).", "Fort"),
    ], RCW))
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Champ 4 — Organisation et management médical"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("R4.1", "Les médecins exerçant en USC doivent avoir une formation initiale ou "
         "attestée à l'activité de soins critiques (anesthésie-réanimation, médecine "
         "intensive-réanimation ou médecine d'urgence).", "Fort"),
        ("R4.2", "L'équipe médicale d'une USC rattachée à un service de réanimation doit "
         "être sous la même responsabilité que ce service.", "Fort"),
        ("R4.3", "Sans unité de réanimation, l'équipe médicale de l'USC doit être sous la "
         "responsabilité d'un médecin exerçant à temps majoritaire dans l'USC.", "Fort"),
        ("R4.4", "Assurer la présence d'un médecin sur site 24h/24, 7j/7 (répondant aux "
         "critères de R4.1) ; mutualiser la permanence de nuit/week-end/jours fériés avec "
         "le service de rattachement (ou les autres soins critiques si pas de "
         "réanimation).", "Fort"),
        ("R4.5", "Sans service de réanimation, assurer la formation continue et "
         "l'évaluation des pratiques en coopération avec le réseau de soins critiques du "
         "GHT.", "Fort"),
    ], RCW))
    return story

# ---------------------------------------------------------------------------
def _section_champ5_sources():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Champ 5 — USC dans le contexte des GHT"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("R5.1", "Les GHT doivent organiser la filière de soins critiques intégrant les "
         "USC selon le volume et la gravité des filières de patients « à risque ».",
         "Fort"),
        ("R5.2", "Sans unité de réanimation in situ, l'USC doit établir une convention "
         "avec l'unité de réanimation du GHT.", "Fort"),
        ("R5.3", "Une USC doit avoir un projet d'unité précisant ses missions au sein du "
         "GHT, ses objectifs, et les catégories de patients qu'elle prend en charge.",
         "Fort"),
        ("R5.4", "Pour les USC isolées, favoriser le partage de temps médical avec des "
         "réanimations partenaires (« pôle de soins critiques inter-établissements »), "
         "pour éviter l'isolement et les problèmes d'attractivité.", "Fort"),
    ], RCW))
    story.append(Spacer(1, 3 * mm))
    story.append(KeepTogether([
        section_bar("Tableau — Critères d'admission en USC (American College of Critical "
                    "Care, cité par le source)", color=GREY),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(theme_table([
        ("Cardiovasculaire", "Suspicion d'IDM ou IDM hémodynamiquement stable ; troubles "
         "du rythme bien tolérés ; entraînement électrosystolique stable ; décompensation "
         "cardiaque modérée (NYHA 1-2) ; urgence hypertensive sans défaillance d'organe."),
        ("Respiratoire", "Sevrage ventilatoire avec soins chroniques ; défaillance "
         "respiratoire stable nécessitant surveillance rapprochée et/ou CPAP ; besoin de "
         "soins/kinésithérapie respiratoire intense."),
        ("Neurologique", "AVC stable nécessitant évaluations/nursing rapprochés ; "
         "traumatisme crânien aigu Glasgow &gt; 9 sous surveillance ; surveillance "
         "post-traitement d'anévrysme cérébral ; fuite de LCR ; trauma médullaire "
         "cervical stable ; hémorragie méningée non sévère en attente de sécurisation."),
        ("Intoxications", "Surveillance cardiaque/pulmonaire/neurologique après "
         "intoxication médicamenteuse chez un patient stable."),
        ("Digestif", "Hémorragie digestive modérée répondant au remplissage ; rupture de "
         "VO de faible intensité chez un patient stable ; insuffisance hépatocellulaire "
         "aiguë sans gravité vitale."),
        ("Endocrinien", "Acidocétose ou décompensation hyperosmolaire sans coma ; "
         "thyrotoxicose/coma myxœdémateux."),
        ("Chirurgical", "Transfusion/remplissage postopératoire chez un patient stable ; "
         "24 premières heures postopératoires à soins infirmiers rapprochés (carotide, "
         "chirurgie vasculaire périphérique, neurochirurgie, greffe rénale…)."),
        ("Divers", "Sepsis stable sans choc ni défaillance d'organe ; monitorage du "
         "remplissage vasculaire ; pré-éclampsie/éclampsie ; soins infirmiers lourds ou "
         "pansements complexes."),
    ], TCW, head=("Appareil", "Indications d'admission en USC")))
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("Sources et avertissement", color=GREY))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>Document source :</b> Conseils Nationaux Professionnels de Médecine Intensive "
        "Réanimation, d'Anesthésie-Réanimation et de Médecine d'Urgence, "
        "« Recommandations pour le fonctionnement des Unités de Surveillance Continue "
        "(USC) dans les Établissements de Santé », 2018.", S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>URL source :</b> https://sfar.org/wp-content/uploads/2018/05/EXTE-USC-CNP.pdf",
        S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>Couverture :</b> intégralité des 26 recommandations (5 champs), toutes à "
        "accord fort — aucune absence de recommandation dans ce document. Le tableau des "
        "critères d'admission ACCC (référence externe citée par le source) est reproduit "
        "intégralement. L'Annexe 1 (actes consommateurs de temps IDE) et les Tableaux 1-3 "
        "(valorisation tarifaire, organisation, charge en soins) ne sont pas retranscrits "
        "— administratifs/méthodologiques, non actionnables au chevet. Bibliographie et "
        "composition nominative du groupe de travail non reproduites.", S_SOURCE))
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Avertissement :</b> cette fiche est une synthèse indépendante, produite pour "
        "un usage d'aide-mémoire. Elle reprend intégralement les 26 recommandations du "
        "texte source, mais condense l'argumentaire de chaque item. Elle ne remplace pas "
        "le texte intégral et n'est ni éditée ni validée par les Conseils Nationaux "
        "Professionnels concernés.", S_BODY_SM), bg=GREY_LIGHT, border=GREY))
    return story

# ---------------------------------------------------------------------------
SECTIONS = [
    ("Champs 1-2 — Typologie des patients & structure des USC", _section_intro_champ1_2),
    ("Champs 3-4 — Organisation paramédicale & médicale", _section_champ3_4),
    ("Champ 5 — GHT, critères d'admission & sources", _section_champ5_sources),
]

def _make_doc(path=None):
    return SimpleDocTemplate(path or OUT, pagesize=A4,
                              leftMargin=MARGIN, rightMargin=MARGIN,
                              topMargin=32 * mm, bottomMargin=16 * mm,
                              title="Fiche CNP 2018 - Fonctionnement des USC",
                              author="Synthèse indépendante (source CNP MIR/AR/MU)")

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
