# -*- coding: utf-8 -*-
"""
Fiche de synthese - "Transfusion de globules rouges homologues : produits,
indications, alternatives" - Recommandation de Bonne Pratique (RBP), HAS,
adoptee par le College de la HAS en novembre 2014. Document source complet :
72 pages, telecharge depuis sfar.org (wp-content/uploads/2015/10, meme
fichier que le lien HAS d'origine).

PERIMETRE VOLONTAIREMENT LIMITE (comme les fiches sepsis/anaphylaxie de ce
corpus) : le document HAS complet couvre 4 parties tres heterogenes -
PARTIE 1 (produits/transformations/qualifications de CGR, examens
immuno-hematologiques - bases de medecine transfusionnelle generale, non
specifique a l'anesthesie), PARTIE 2 (anesthesie, reanimation, chirurgie,
urgence - coeur de cible de ce corpus), PARTIE 3 (hematologie-oncologie :
drepanocytose, thalassemie, leucemies, myelodysplasies, geriatrie),
PARTIE 4 (neonatologie : exsanguino-transfusion, seuils chez le
nouveau-ne/premature). Cette fiche couvre INTEGRALEMENT la PARTIE 2
(sections 5 a 8, p.23-31 du source) - la seule directement actionnable
pour un anesthesiste-reanimateur d'adulte au bloc/en reanimation/aux
urgences. Les Parties 1, 3 et 4 (medecine transfusionnelle generale,
hematologie-oncologie specialisee, pediatrie neonatale) sont hors du
perimetre "anesthesie/reanimation adulte" de ce corpus et NE SONT PAS
traitees ici - explicitement disclosed, pas un oubli. Un futur backlog
item pourrait construire une fiche separee pour la Partie 4
(neonatologie) si ce corpus etend son perimetre pediatrique.

METHODOLOGIE : grille HAS classique A/B/C/AE (PAS le format SFAR
1+/1-/2+/2- de la majorite de ce corpus) - A = preuve scientifique
etablie (essais randomises de forte puissance/meta-analyses), B =
presomption scientifique (preuves de niveau intermediaire), C = faible
niveau de preuve, AE = accord d'experts (absence d'etudes). Meme
convention deja utilisee dans ce corpus pour fiche_ivg_14sa.py (chips
A/B/C deja definis avec les memes couleurs GREEN/TEAL/AMBER dans
style.py, reutilises tels quels ; chip "AE" ajoute ici avec la couleur
GREY deja utilisee pour "AP" dans la fiche IVG - meme role d'accord
d'experts/professionnel).

VERIFICATION VISUELLE OBLIGATOIRE (rendu 180dpi, p.23-24 du PDF) : le
texte source presente chaque recommandation gradee dans un ENCADRE
COLORE (jaune pour A/B/C, bleu pour AE) avec le grade a gauche et le
texte a droite - format tableau visuel, pas du texte lineaire. L'extraction
texte lineaire de PyMuPDF conserve neanmoins l'ordre grade-puis-texte
(verifie par rendu visuel comparatif, aucune inversion trouvee). Certains
paragraphes de contexte ("cas particuliers" du patient traumatise, de
la transfusion massive) reprennent le mot "recommande"/"non recommande"
en PROSE, SANS encadre colore ni grade explicite - ce ne sont PAS des
recommandations gradees distinctes mais des renvois/precisions au texte
de la recommandation gradee la plus proche ; ils sont retranscrits ici
en note de contexte, sans grade invente (regle 4 : ne jamais fabriquer
un grade absent du source).

DECOMPTE : 26 recommandations gradees (4 en 5.1, 3 en 5.2, 1 en
Section 6, 6 en Section 7, 2 en 8.1, 3 en 8.2, 2 en 8.3, 2 en 8.4, 2 en
8.5 [chacune couvrant plusieurs points connexes], 1 en 8.6) + 4 absences
de recommandation explicitement enoncees en prose (neuroreanimation ;
duree de conservation des CGR ; acide tranexamique et hemorragie du
post-partum ; rFVIIa et hemorragie du post-partum) = 30 items sur la
Partie 2 integrale. Chaque paire grade/texte relue individuellement sur
le texte source et confrontee au rendu visuel des pages 23-24 avant
d'ecrire ce script.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from style import *
GRADE_COLORS["A"] = (GREEN, WHITE)
GRADE_COLORS["B"] = (TEAL, WHITE)
GRADE_COLORS["C"] = (AMBER, WHITE)
GRADE_COLORS["AE"] = (GREY, WHITE)
GRADE_COLORS["ABS"] = (GREY_LIGHT, INK)
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.units import mm

OUT = "/home/user/rfe-sfar-website/output/Fiche_HAS_Transfusion_GR_Anesthesie_2014.pdf"

SOURCE_TXT = ("Source : HAS, « Transfusion de globules rouges homologues : produits, "
              "indications, alternatives », RBP, novembre 2014 — Partie 2 uniquement "
              "(anesthésie/réanimation/chirurgie/urgence). Fiche de synthèse non officielle : "
              "se référer au texte intégral.")

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

RCW = [16 * mm, CW_FULL - 16 * mm - 15 * mm, 15 * mm]

def absence_note(question_txt):
    return info_panel(P(
        f"<b>ABS — Absence de recommandation</b> (données insuffisantes) : {question_txt}",
        S_BODY_SM), bg=GREY_LIGHT, border=GREY)

def context_note(txt):
    return P(f"<i>Précision du source (non gradée séparément) :</i> {txt}", S_NOTE)

def legend_flowable():
    chip_w = 14 * mm
    content_w = CW_FULL
    row = Table([[chip("A", width=chip_w - 2 * mm), chip("B", width=chip_w - 2 * mm),
                  chip("C", width=chip_w - 2 * mm), chip("AE", width=chip_w - 2 * mm),
                  chip("ABS", width=chip_w - 2 * mm),
                  P("<b>Grille HAS</b> (distincte du format SFAR 1+/1-/2+/2- utilisé "
                    "ailleurs dans ce corpus) — <b>A</b> : preuve scientifique établie ; "
                    "<b>B</b> : présomption scientifique ; <b>C</b> : faible niveau de "
                    "preuve ; <b>AE</b> : accord d'experts (absence d'études) ; "
                    "<b>ABS</b> : absence de recommandation. Fiche limitée à la Partie 2 "
                    "du source (anesthésie/réanimation/chirurgie/urgence) — voir "
                    "encadré de périmètre ci-dessous.", S_BADGE_HEAD)]],
                colWidths=[chip_w] * 5 + [content_w - 5 * chip_w])
    row.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                              ("LEFTPADDING", (0, 0), (-1, -1), 1),
                              ("RIGHTPADDING", (0, 0), (-1, -1), 1),
                              ("TOPPADDING", (0, 0), (-1, -1), 0),
                              ("BOTTOMPADDING", (0, 0), (-1, -1), 0)]))
    return row

TOTAL_PAGES = {"n": 5}

def on_page(canvas, doc, page_title):
    header_band(canvas, doc, "HAS — RBP, NOVEMBRE 2014 (PARTIE 2/4 — PÉRIMÈTRE LIMITÉ)",
                "Transfusion de globules rouges homologues — Anesthésie/Réanimation",
                page_title, icon_fn=lambda c, x, y: icon_drop(c, x, y, 13 * mm), color=TEAL_DARK)
    footer_band(canvas, doc, SOURCE_TXT, f"Page {doc.page} / {TOTAL_PAGES['n']}")

# ---------------------------------------------------------------------------
def _section_intro_5():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Périmètre limité :</b> le document source HAS (2014) comporte 4 parties. "
        "Cette fiche couvre INTÉGRALEMENT la seule <b>Partie 2 — Anesthésie, "
        "réanimation, chirurgie, urgence</b> (sections 5 à 8). Les Parties 1 (produits/"
        "qualifications de CGR — médecine transfusionnelle générale), 3 (hématologie-"
        "oncologie : drépanocytose, thalassémie, leucémies) et 4 (néonatologie : "
        "exsanguino-transfusion) ne sont PAS traitées — hors périmètre anesthésie/"
        "réanimation adulte de ce corpus, disclosed explicitement.", S_BODY),
        bg=AMBER_LIGHT, border=AMBER))
    story.append(Spacer(1, 2.5 * mm))
    story.append(legend_flowable())
    story.append(Spacer(1, 3 * mm))
    story.append(KeepTogether([
        section_bar("Section 5.1 — Seuil transfusionnel en anesthésie"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("—", "Le seuil critique du transport artériel en O<sub>2</sub> (TaO<sub>2</sub> crit) chez l'homme "
         "anesthésié est de l'ordre de 5 ml O<sub>2</sub>/kg/min (repère physiologique).", "B"),
        ("—", "Pour conserver une marge de sécurité, le seuil de sécurité du TaO<sub>2</sub> "
         "recommandé chez l'adulte est de 10 ml O<sub>2</sub>/kg/min. La tolérance à l'anémie "
         "aiguë dépend des possibilités d'augmentation du débit cardiaque — d'où la "
         "priorité à corriger l'hypovolémie, et un seuil plus élevé en cas "
         "d'insuffisance cardiaque.", "AE"),
        ("—", "Seuils transfusionnels d'hémoglobine en période péri-opératoire : "
         "7 g/dl chez les personnes sans antécédents particuliers ; 10 g/dl chez les "
         "personnes ne tolérant pas cliniquement des concentrations inférieures, ou "
         "atteintes d'insuffisance coronarienne aiguë, d'insuffisance cardiaque avérée, "
         "ou bêta-bloquées.", "B"),
        ("—", "Privilégier un seuil transfusionnel de 8-9 g/dl chez les personnes ayant "
         "des antécédents cardio-vasculaires.", "AE"),
    ], RCW))
    story.append(Spacer(1, 3 * mm))
    story.append(KeepTogether([
        section_bar("Section 5.2 — Seuil transfusionnel en réanimation"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("—", "Seuil transfusionnel de 7 g/dl en l'absence d'insuffisance coronarienne "
         "aiguë (y compris chez les patients à cardiopathie chronique équilibrée) ; "
         "10 g/dl d'Hb en présence d'une insuffisance coronarienne aiguë.", "B"),
        ("—", "Patient traumatisé (hors traumatisme crânien) et hors transfusion "
         "massive : seuil transfusionnel de 7 g/dl en l'absence de mauvaise tolérance "
         "clinique.", "B"),
        ("—", "Hémorragie digestive (bonne tolérance clinique, absence de signe de "
         "choc) : seuil transfusionnel de 7 g/dl.", "B"),
    ], RCW))
    story.append(Spacer(1, 1.5 * mm))
    story.append(context_note(
        "chez le patient traumatisé, viser une Hb entre 7 et 9 g/dl en tenant compte "
        "de la cinétique du saignement. En transfusion massive, associer les CGR à du "
        "plasma thérapeutique et des concentrés de plaquettes — en dehors de ce cadre, "
        "ne pas associer systématiquement plasma et CGR (précisions non gradées "
        "séparément)."))
    story.append(Spacer(1, 2 * mm))
    story.append(absence_note(
        "seuil transfusionnel en neuroréanimation — données insuffisantes et "
        "résultats contradictoires."))
    story.append(Spacer(1, 2 * mm))
    story.append(absence_note(
        "âge/durée de conservation des CGR (Section 5.3) — données disponibles "
        "insuffisantes."))
    return story

# ---------------------------------------------------------------------------
def _section_6_7():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Section 6 — Niveaux d'urgence transfusionnelle"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(P(
        "<b>Définitions (Afssaps 2002) :</b> urgence vitale immédiate (UVI) — délivrance "
        "sans délai ; urgence vitale (UV) — obtention en &lt; 30 min ; urgence relative "
        "(UR) — obtention en 2-3 h.", S_BODY_SM))
    story.append(Spacer(1, 1.5 * mm))
    story.append(reco_table([
        ("—", "Le délai d'obtention des CGR prime sur celui des résultats d'examens "
         "immuno-hématologiques.", "AE"),
    ], RCW))
    story.append(Spacer(1, 3 * mm))
    story.append(KeepTogether([
        section_bar("Section 7 — Transfusion en situation d'urgence"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("—", "Chaque établissement doit disposer d'une procédure d'urgence vitale "
         "propre, discutée avec la structure de délivrance (circuits, modalités "
         "d'acheminement, stock de dépôt d'urgence).", "AE"),
        ("—", "En l'absence de résultat de groupe ABO disponible, ou en cas de doute "
         "sur le lien patient-examens, transfuser des CGR de groupe O.", "AE"),
        ("—", "Sans aucune donnée immuno-hématologique : CGR O RH:1 KEL:-1 — sauf pour "
         "la femme de la naissance à la fin de la période procréatrice, pour laquelle "
         "des CGR O RH:-1 KEL:-1 sont recommandés en 1<super>re</super> intention (dans "
         "la limite des disponibilités). Avec une seule détermination ABO-RH1/RH-KEL1 "
         "disponible, délivrer un CGR groupe O compatible avec ce phénotype si "
         "disponible dans les délais.", "AE"),
        ("—", "Communiquer les données d'identité les plus complètes possible (a "
         "minima sexe et âge, avec tout document disponible), pour affiner la "
         "sélection des CGR ou retrouver l'historique du patient.", "AE"),
        ("—", "Femme de groupe RH:1 connu, phénotype RH4 négatif ou inconnu : ne pas "
         "transfuser de CGR RH:-1 de la naissance à la fin de la période procréatrice.",
         "AE"),
        ("—", "En transfusion massive, la disponibilité des CGR prime sur la "
         "compatibilité dans les systèmes de groupes sanguins hors ABO.", "AE"),
    ], RCW))
    return story

# ---------------------------------------------------------------------------
def _section_8a():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Section 8.1-8.2 — Alternatives : fer et EPO"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("8.1", "Le fer est recommandé en anesthésie uniquement en présence d'une "
         "carence martiale.", "B"),
        ("8.1", "L'utilisation systématique du fer n'est pas recommandée en "
         "réanimation.", "C"),
        ("8.2", "L'EPO n'est pas recommandée en réanimation.", "B"),
        ("8.2", "L'EPO est recommandée en préopératoire de chirurgie orthopédique "
         "hémorragique chez les patients modérément anémiques (Hb 10-13 g/dl "
         "attendant des pertes de 900-1 800 ml).", "A"),
        ("8.2", "L'EPO n'est pas recommandée en péri-opératoire de chirurgie "
         "colorectale carcinologique (insuffisance de preuve d'efficacité).", "B"),
    ], RCW))
    return story

def _section_8b():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Section 8.3-8.4 — Alternatives : acide tranexamique et rFVIIa"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("8.3", "Utiliser l'acide tranexamique en péri-opératoire de chirurgie "
         "hémorragique, sauf contre-indication (antécédents thromboemboliques "
         "veineux/artériels, antécédents convulsifs — contre-indications relatives ; "
         "adapter la dose si insuffisance rénale).", "B"),
        ("8.3", "Utiliser l'acide tranexamique dans les 3 premières heures de prise en "
         "charge d'un polytraumatisme : 1 g IV lente sur 10 min, puis 1 g sur 8 h.",
         "A"),
        ("8.4", "Ne pas administrer systématiquement le facteur VIIa recombinant "
         "(rFVIIa) en anesthésie.", "A"),
        ("8.4", "Ne pas administrer systématiquement le rFVIIa en traumatologie "
         "(réanimation).", "B"),
    ], RCW))
    story.append(Spacer(1, 2 * mm))
    story.append(absence_note(
        "acide tranexamique dans l'hémorragie du post-partum — insuffisance de données "
        "sur la balance bénéfice/risque."))
    story.append(Spacer(1, 2 * mm))
    story.append(absence_note(
        "rFVIIa dans l'hémorragie du post-partum — insuffisance de preuve d'efficacité."))
    return story

# ---------------------------------------------------------------------------
def _section_8c_sources():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Section 8.5-8.6 — Retransfusion et transfusion autologue"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("8.5", "Récupération de sang <b>per</b>opératoire : meilleures indications en "
         "chirurgie cardiaque et vasculaire ; non recommandée si champ opératoire "
         "infecté ou colles biologiques utilisées ; volumes non lavés ≤ 1 000 ml par "
         "patient adulte (au-delà, lavage requis).", "AE"),
        ("8.5", "Récupération de sang <b>post</b>opératoire : meilleures indications en "
         "arthroplastie de genou et hémothorax ; recueil limité aux 6 premières heures "
         "postopératoires ; non recommandée en cas d'infection (locale ou générale) ou "
         "d'insuffisance rénale.", "AE"),
        ("8.6", "Ne pas proposer de transfusion autologue programmée (TAP), sauf "
         "groupe sanguin rare ou patient polyimmunisé.", "AE"),
    ], RCW))
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("Sources et avertissement", color=GREY))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>Document source :</b> HAS, « Transfusion de globules rouges homologues : "
        "produits, indications, alternatives », recommandation de bonne pratique, "
        "adoptée par le Collège de la HAS en novembre 2014 (Service des bonnes "
        "pratiques professionnelles).", S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>URL source :</b> https://sfar.org/transfusion-de-globules-rouges-"
        "homologues-produits-indications-alternatives/", S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>Couverture :</b> intégralité de la Partie 2 du source (sections 5 à 8 — "
        "anesthésie, réanimation, chirurgie, urgence) : 26 recommandations gradées et "
        "4 absences de recommandation explicites. Les Parties 1, 3 et 4 du document "
        "(médecine transfusionnelle générale, hématologie-oncologie, néonatologie) ne "
        "sont pas couvertes — hors périmètre anesthésie/réanimation adulte de ce "
        "corpus, disclosed en page 1. Bibliographie et argumentaire scientifique "
        "détaillé (document séparé sur has-sante.fr) non reproduits.", S_SOURCE))
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Avertissement :</b> cette fiche est une synthèse indépendante et "
        "PARTIELLE (Partie 2 uniquement), produite pour un usage d'aide-mémoire en "
        "anesthésie-réanimation adulte. Elle ne remplace pas le texte intégral — en "
        "particulier pour toute situation d'hématologie-oncologie, de pédiatrie ou de "
        "néonatologie, se référer aux Parties 1, 3 et 4 du document HAS complet. "
        "Cette fiche n'est ni éditée ni validée par la HAS.",
        S_BODY_SM), bg=GREY_LIGHT, border=GREY))
    return story

# ---------------------------------------------------------------------------
def _section_6_7_8a():
    story = _section_6_7()
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_8a())
    return story

def _section_8b_8c_sources():
    story = _section_8b()
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_8c_sources())
    return story

SECTIONS = [
    ("Sections 5.1-5.2 — Seuils transfusionnels (anesthésie & réanimation)", _section_intro_5),
    ("Sections 6-8.2 — Urgence transfusionnelle & alternatives (fer/EPO)", _section_6_7_8a),
    ("Section 8.3-8.6 — Alternatives (suite) & sources", _section_8b_8c_sources),
]

def _make_doc(path=None):
    return SimpleDocTemplate(path or OUT, pagesize=A4,
                              leftMargin=MARGIN, rightMargin=MARGIN,
                              topMargin=32 * mm, bottomMargin=16 * mm,
                              title="Fiche HAS 2014 - Transfusion GR (Partie 2 - Anesthesie-Reanimation)",
                              author="Synthèse indépendante (source HAS)")

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
