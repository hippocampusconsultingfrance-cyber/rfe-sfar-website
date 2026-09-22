# -*- coding: utf-8 -*-
"""
Fiche de synthese - RFE SFAR, "Recommandations sur l'utilisation de
l'echographie lors de la mise en place des acces vasculaires", 2015
(Anesth Reanim. 2015;1:183-189, doi:10.1016/j.anrea.2014.12.008). Document
valide par le CA de la Sfar le 12 septembre 2014. 7 pages source,
telecharge depuis sfar.org (wp-content/uploads/2015/09/2_AFAR_utilisation-
de-lechographie-lors-de-la-mise-en-place-des-acces-vasculaires.pdf).

METHODOLOGIE : methode GRADE(r) standard - qualite des preuves en 4
categories (haute/moderee/basse/tres basse), formulation binaire positive/
negative x forte/faible (Grade 1+/1-/2+/2-). Utilise directement les grades
GRADE_COLORS deja definis dans style.py (1+/2+/AE/? ) - aucune extension
locale necessaire, contrairement aux fiches a grille EBM narrative (Niveaux
I-V / Grades A-E) rencontrees ailleurs dans ce corpus.

PORTEE : couverture complete des 10 recommandations natives (R1-R10,
numerotation native de la source - pas de reference synthetique
necessaire ici). Champ exclu par la source elle-meme et disclosed comme
tel : l'echoguidage de l'artere femorale (adulte et enfant) n'a pas ete
aborde faute de donnees bibliographiques ; les techniques d'echo-reperage
ou de Doppler seul (moins performantes) ne sont pas non plus dans le
champ. Recommandation 7 (sous-clavière enfant) est un cas particulier
disclosed : "Aucune recommandation ne peut etre proposee" (absence
d'essai randomise chez l'enfant pour ce site) - retranscrite telle quelle,
sans grade fabrique, avec un badge "?" dedie (meme convention que
fiche_civd.py / fiche_asthme_aigu_grave.py pour ce cas).

ARGUMENTAIRE : la source consacre un paragraphe statistique detaille
(risque relatif, IC95%, nombre d'etudes/patients) par recommandation.
Conformement a la regle de projet 2026-09-14 (minimiser l'argumentaire),
chaque ligne ne retient que les chiffres de reduction de risque cles et le
niveau global de preuve - pas le detail complet RR/IC95%/etudes qui
alourdirait la lecture sans changer la pratique clinique (le grade
lui-meme resume deja la force de la recommandation).

AUDIT INDEPENDANT (subagent, aveugle au brouillon) : les 10 grades et tous
les pourcentages de reduction de risque verifies exacts (aucune erreur
numerique, aucun grade errone, R7 correctement distingue). Corrections
MEDIUM apportees suite a l'audit : R1 - le qualificatif "possible" de
l'hemothorax (IC95% traversant 1 dans la source) avait ete perdu, et le
compte "13 etudes/2675 patients" agregeait a tort 5 criteres dont un seul
etaye par 1 etude/900 patients - remplace par une fourchette disclosed
"1 a 13 etudes, 900 a 2675 patients" (meme convention que R4/R9). R2 - la
raison de la qualite "elevee malgre..." citait a tort le "faible nombre
d'etudes" au lieu de l'heterogeneite/imprecision reellement citees par la
source. Resume - la phrase d'exclusion de champ melangeait 2 raisons
distinctes (femorale : donnees bibliographiques absentes ; echo-
reperage/Doppler : juges moins performants) - separees. R5/R9/R10 -
raisons de qualite de preuve (imprecision/heterogeneite) ajoutees pour
coherence avec R1/R3/R4/R6/R8 qui les mentionnaient deja.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from style import *
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.units import mm

OUT = "/home/user/rfe-sfar-website/output/Fiche_SFAR_Echo_Acces_Vasculaires_2015.pdf"

SOURCE_TXT = ("Source : « Recommandations sur l'utilisation de l'échographie lors de la mise en "
              "place des accès vasculaires » — RFE SFAR, 2015 (Anesth Réanim. 2015;1:183-189). "
              "Fiche de synthèse non officielle : se référer au texte intégral.")

def P(txt, style=S_CELL):
    return Paragraph(txt, style)

def chip(label):
    return grade_chip(label, width=13 * mm, fontsize=8.6)

CW_FULL = PAGE_W - 2 * MARGIN

def reco_table(rows, col_widths):
    """rows: (ref, text, grade_label)."""
    data = [[P("N°", S_HEAD_W_C), P("Recommandation", S_HEAD_W), P("Grade", S_HEAD_W_C)]]
    for ref, txt, grade in rows:
        data.append([P(ref, S_CELL_B), P(txt, S_CELL), chip(grade)])
    t = Table(data, colWidths=col_widths, repeatRows=1)
    style_cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), NAVY), ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTNAME", (0, 0), (-1, 0), FONT_BOLD), ("FONTSIZE", (0, 0), (-1, 0), 8),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("ALIGN", (0, 0), (0, -1), "CENTER"),
        ("ALIGN", (2, 0), (2, -1), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 0.5, GREY_LIGHT),
        ("TOPPADDING", (0, 0), (-1, -1), 3.2), ("BOTTOMPADDING", (0, 0), (-1, -1), 3.2),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            style_cmds.append(("BACKGROUND", (0, i), (-1, i), BG_PANEL))
    t.setStyle(TableStyle(style_cmds))
    return t

RCW = [12 * mm, CW_FULL - 12 * mm - 15 * mm, 15 * mm]

def theme_table(rows, col_widths, head=("Thème", "Détail")):
    data = [[P(head[0], S_HEAD_W), P(head[1], S_HEAD_W)]]
    for theme, detail in rows:
        data.append([P(theme, S_CELL_B), P(detail, S_CELL)])
    t = Table(data, colWidths=col_widths, repeatRows=1)
    style_cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), TEAL_DARK), ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTNAME", (0, 0), (-1, 0), FONT_BOLD), ("FONTSIZE", (0, 0), (-1, 0), 8),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.5, GREY_LIGHT),
        ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            style_cmds.append(("BACKGROUND", (0, i), (-1, i), BG_PANEL))
    t.setStyle(TableStyle(style_cmds))
    return t

def legend_flowable():
    chip_w = 15 * mm
    content_w = CW_FULL
    row = Table([[chip("1+"),
                  P("<b>Grade 1+</b> : il est recommandé de faire (forte).", S_BADGE_HEAD),
                  chip("2+"),
                  P("<b>Grade 2+</b> : il est probablement recommandé de faire (faible).",
                    S_BADGE_HEAD)]],
                colWidths=[chip_w, content_w * 0.35, chip_w, content_w * 0.65 - 2 * chip_w])
    row.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                              ("LEFTPADDING", (0, 0), (-1, -1), 1),
                              ("RIGHTPADDING", (0, 0), (-1, -1), 3),
                              ("TOPPADDING", (0, 0), (-1, -1), 0),
                              ("BOTTOMPADDING", (0, 0), (-1, -1), 0)]))
    return row

TOTAL_PAGES = {"n": 2}

def on_page(canvas, doc, page_title):
    header_band(canvas, doc, "SFAR — RFE, MÉTHODE GRADE, 2015",
                "Échographie & accès vasculaires",
                page_title, icon_fn=lambda c, x, y: icon_drop(c, x, y, 13 * mm), color=TEAL_DARK)
    footer_band(canvas, doc, SOURCE_TXT, f"Page {doc.page} / {TOTAL_PAGES['n']}")

# ---------------------------------------------------------------------------
def _section_all():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Résumé :</b> RFE SFAR (méthode GRADE) sur l'utilisation de l'échoguidage lors de "
        "la pose d'accès vasculaires veineux centraux, artériels et veineux périphériques "
        "(a priori difficiles), chez l'adulte et l'enfant. La ponction échoguidée réduit "
        "significativement les échecs de canulation, les ponctions artérielles accidentelles, "
        "les hématomes et — pour les voies centrales — le pneumothorax/hémothorax, par "
        "rapport au repérage anatomique seul. <b>Champ exclu par la source</b> : l'échoguidage "
        "de l'artère fémorale, adulte et enfant (absence de données bibliographiques), et les "
        "techniques d'écho-repérage ou de Doppler seul, jugées moins performantes.", S_BODY),
        bg=BG_PANEL, border=TEAL))
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("Méthodologie"))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "Méthode GRADE® : qualité des preuves en 4 catégories — <b>haute</b> (les recherches "
        "futures ne changeront très probablement pas la confiance dans l'estimation de "
        "l'effet), <b>modérée</b>, <b>basse</b>, <b>très basse</b> (estimation très "
        "incertaine). Formulation finale toujours binaire : positive/négative et forte/"
        "faible. Critères de jugement retenus : échec de ponction, ponction artérielle, "
        "pneumothorax/hémothorax pour les voies centrales ; taux de succès seul pour les "
        "autres accès. Populations étudiées séparément : adulte et enfant, par site "
        "d'insertion (jugulaire interne, sous-clavière, fémorale, radiale, veine "
        "périphérique a priori difficile).", S_BODY_SM))
    story.append(Spacer(1, 1.5 * mm))
    story.append(legend_flowable())
    story.append(Spacer(1, 2.5 * mm))
    story.append(section_bar("Recommandations — accès vasculaires chez l'adulte"))
    story.append(Spacer(1, 1.5 * mm))
    story.append(reco_table([
        ("R1", "<b>Veine jugulaire interne :</b> il est recommandé d'utiliser une technique "
         "échoguidée plutôt que le repérage anatomique. Réduction des échecs de canulation "
         "de 86 %, des ponctions artérielles de 80 %, des hématomes de 78 %, du pneumothorax "
         "de 90 % et possible réduction de l'hémothorax de 94 % (IC 95 % traversant 1) — "
         "1 à 13 études selon le critère, 900 à 2675 patients. Qualité de preuve "
         "<b>élevée</b>.", "1+"),
        ("R2", "<b>Veine sous-clavière :</b> il est recommandé d'utiliser une technique "
         "échoguidée. Réduction des échecs de 94 %, des ponctions artérielles de 82 %, des "
         "hématomes de 77 %, du pneumothorax de 78 % et de l'hémothorax de 95 % (3 études, "
         "~450-500 patients). Qualité <b>élevée</b> malgré l'hétérogénéité et l'imprécision "
         "des résultats pour certains critères (études peu nombreuses pour cette voie).",
         "1+"),
        ("R3", "<b>Veine fémorale :</b> il est recommandé d'utiliser une technique "
         "échoguidée. Réduction des échecs de 85 %, des ponctions artérielles de 86 % "
         "(2 études, 150 patients) et possible réduction des hématomes de 50 % (1 étude, "
         "110 patients). Qualité <b>modérée</b> (imprécision des résultats).", "1+"),
        ("R4", "<b>Artère radiale :</b> il est probablement recommandé d'utiliser une "
         "technique échoguidée. Réduction des échecs au premier essai de 39 % et des "
         "hématomes de 83 % (2-4 études, 132-281 patients). Qualité <b>basse</b> "
         "(imprécision et hétérogénéité).", "2+"),
        ("R5", "<b>Veine périphérique a priori difficile :</b> il est probablement recommandé "
         "d'utiliser une technique échoguidée. Augmentation du taux de succès de 20 % "
         "(3 études, 154 patients). Qualité <b>modérée</b> (imprécision des résultats).",
         "2+"),
    ], RCW))
    story.append(Spacer(1, 2.5 * mm))
    story.append(section_bar("Recommandations — accès vasculaires chez l'enfant"))
    story.append(Spacer(1, 1.5 * mm))
    story.append(reco_table([
        ("R6", "<b>Veine jugulaire interne :</b> il est recommandé d'utiliser une technique "
         "échoguidée. Réduction des échecs de 69 % et des ponctions artérielles de 77 % "
         "(4 études, 460 patients). Qualité <b>modérée</b> (hétérogénéité des résultats).",
         "1+"),
        ("R7", "<b>Veine sous-clavière :</b> aucune recommandation ne peut être proposée — "
         "aucun essai randomisé contrôlé disponible chez l'enfant pour ce site. Seules des "
         "études de faisabilité existent (7 publications, &gt;400 enfants/nourrissons, "
         "aucune complication — ponction artérielle ou pneumothorax — rapportée) ; une "
         "expertise complémentaire et des études contrôlées sont nécessaires.", "?"),
        ("R8", "<b>Veine fémorale :</b> il est recommandé d'utiliser une technique "
         "échoguidée. Réduction des échecs de 62 % et des ponctions artérielles de 65 % "
         "(3 études, 215 patients). Qualité <b>modérée</b> (risque de biais, imprécision).",
         "1+"),
        ("R9", "<b>Artère radiale :</b> il est probablement recommandé d'utiliser une "
         "technique échoguidée. Réduction des échecs au premier essai de 33 % et des "
         "hématomes de 80 % (1-3 études, 118-300 patients). Qualité <b>modérée</b> "
         "(hétérogénéité des résultats).", "2+"),
        ("R10", "<b>Veine périphérique a priori difficile :</b> il est probablement "
         "recommandé d'utiliser une technique échoguidée. Augmentation probable du taux de "
         "succès de 20 % (3 études, 134 patients). Qualité <b>basse</b> (imprécision des "
         "résultats).", "2+"),
    ], RCW))
    story.append(Spacer(1, 2.5 * mm))
    story.append(section_bar("Analyse médico-économique", color=GREY))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "Analyse du National Health Service (Calvert et al., 2003, modèle de décision "
        "analytique) : le coût marginal de l'utilisation de l'échographie pour la pose d'un "
        "cathéter veineux central est inférieur à 12 € (scénario ≥15 procédures/semaine). "
        "Gain estimé &gt;2000 € pour 1000 procédures réalisées, compte tenu du coût d'achat "
        "et de maintenance de l'échographe, des dispositifs à usage unique et de la "
        "formation — résultats sensibles au nombre de procédures réalisées.", S_BODY_SM))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<i>Note des auteurs :</i> la disponibilité des échographes peut encore être limitée "
        "dans certaines structures, et tous les praticiens ne sont pas encore parfaitement "
        "formés à la ponction échoguidée — cette RFE doit servir de socle à la mise en place "
        "de programmes de formation et de référence opposable pour la mise à disposition du "
        "matériel adapté (échographe et matériel ancillaire).", S_NOTE))
    return story

def _section_sources():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("Sources et traçabilité", color=GREY))
    story.append(Spacer(1, 2 * mm))
    story.append(P(
        "<b>Document source :</b> « Recommandations sur l'utilisation de l'échographie lors "
        "de la mise en place des accès vasculaires » — RFE, Société française d'anesthésie "
        "et de réanimation (SFAR), 2015. Validée par le CA de la SFAR le 12/09/2014. Publié "
        "Anesth Réanim. 2015;1:183-189.", S_SOURCE))
    story.append(Spacer(1, 1 * mm))
    story.append(P("<b>Méthodologie :</b> méthode GRADE® — voir détail en page 1.", S_SOURCE))
    story.append(Spacer(1, 1 * mm))
    story.append(P(
        "<b>URL source :</b> https://sfar.org/wp-content/uploads/2015/09/2_AFAR_utilisation-"
        "de-lechographie-lors-de-la-mise-en-place-des-acces-vasculaires.pdf", S_SOURCE))
    story.append(Spacer(1, 1 * mm))
    story.append(P(
        "<b>Couverture :</b> intégralité des 10 recommandations (R1-R10, numérotation native "
        "de la source). Champ exclu par la source elle-même (disclosed) : échoguidage de "
        "l'artère fémorale et techniques d'écho-repérage/Doppler seul.", S_SOURCE))
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Avertissement — document validé 2014/2015 :</b> cette fiche de synthèse "
        "indépendante reprend l'intégralité des recommandations du texte source, mais ne le "
        "remplace pas et n'est ni éditée ni validée par la SFAR. Se référer au texte intégral "
        "(y compris son matériel complémentaire et ses 16 références bibliographiques, non "
        "reprises ici) pour toute décision clinique.", S_BODY_SM), bg=GREY_LIGHT, border=GREY))
    return story

SECTIONS = [
    ("Méthodologie, recommandations & sources", lambda: _section_all() + _section_sources()),
]

def _make_doc(path=None):
    return SimpleDocTemplate(path or OUT, pagesize=A4,
                              leftMargin=MARGIN, rightMargin=MARGIN,
                              topMargin=32 * mm, bottomMargin=16 * mm,
                              title="Fiche SFAR 2015 - Echographie et acces vasculaires",
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

    doc = _make_doc()
    story = _build_upto(fns)
    doc.build(story, onFirstPage=on_page_final, onLaterPages=on_page_final)
    print("OK ->", OUT, f"({total_pages} pages)")

if __name__ == "__main__":
    build()
