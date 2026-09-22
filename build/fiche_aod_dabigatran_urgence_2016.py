# -*- coding: utf-8 -*-
"""
Fiche de synthese - "Prise en charge des hemorragies et des gestes invasifs
urgents chez les patients recevant un anticoagulant oral et direct anti-IIa
(dabigatran)" - Reactualisation des propositions du Groupe d'Interet en
Hemostase Perioperatoire (GIHP), septembre 2016 (Albaladejo P, Pernod G,
Godier A, et al.). 22 pages (21 pages de texte + biblio), telecharge depuis
sfar.org (download/gestion-perioperatoire-des-patients-sous-aod-en-urgence/
?wpdmdl=34412).

METHODOLOGIE : propositions pragmatiques du GIHP, PAS de grille GRADE ni de
recommandations numerotees formellement (meme famille documentaire que
fiche_aod_urgence deja construite : "propositions", pas RFE/RPC). Le coeur
actionnable du texte est 3 algorithmes decisionnels (Figures 1, 2, 3, pages
15/20 du PDF source) - PURES IMAGES sans couche de texte (verifie via
`page.get_images()`), rendues a 200dpi et transcrites visuellement en
tableaux de decision fideles a la logique des figures (colonnes
condition -> conduite), conformement a la regle de projet "reproduire les
tableaux/figures verbatim... rendre et transcrire visuellement si image
pure sans texte". Une transcription en tableau plutot qu'en image redessinee
est jugee plus fidele et plus lisible sur mobile que la reproduction du
graphisme du flowchart lui-meme (coherent avec la regle de projet sur la
lisibilite mobile).

DISTINCT de la fiche deja construite `aod_urgence` (GIHP 2013, dabigatran +
rivaroxaban, PRE-antidote specifique - explicitement disclosed comme datee/
incomplete dans son propre DOC_META). Ce document de 2016 est la
reactualisation dediee spécifiquement au dabigatran (anti-IIa), integrant
l'antidote specifique idarucizumab (Praxbind(R)), disponible depuis. Verifie
par titre + contenu (49 occurrences "idarucizumab") avant construction,
needle href distinct de celui d'aod_urgence (patients-sous-aod-en-urgence vs
aod-en-urgence), aucune collision de cle.

PERIMETRE ET CONDENSATION (regle de projet 2026-09-14, argumentaire
minimal) : le texte source consacre une tres large part (pages 2-14) a la
justification pharmacologique/bibliographique detaillee (etude REVERSE-AD,
mecanisme d'action, donnees precliniques, debat sur l'interet de la
neutralisation en cas d'hemorragie intracranienne...) - condensee a
l'essentiel actionnable (seuils, doses, indications) ; les 3 figures
elles-memes (l'information reellement utilisee au lit du malade) sont
integralement transcrites. L'accident vasculaire cerebral ischemique est
explicitement hors perimetre de ce texte (renvoi aux recommandations des
societes referentes pour la thrombolyse/thrombectomie) - disclosed tel
quel. Les 37 references bibliographiques (page 21-22) ne sont pas
transcrites (renvoi au texte integral).
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from style import *
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.units import mm

OUT = "/home/user/rfe-sfar-website/output/Fiche_GIHP_AOD_Dabigatran_Urgence_2016.pdf"

SOURCE_TXT = ("Source : GIHP, « Prise en charge des hémorragies et des gestes invasifs urgents "
              "chez les patients recevant un anticoagulant oral et direct anti-IIa (dabigatran) », "
              "réactualisation septembre 2016. Fiche de synthèse non officielle : se référer au "
              "texte intégral.")

def P(txt, style=S_CELL):
    return Paragraph(txt, style)

CW_FULL = PAGE_W - 2 * MARGIN

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

def decision_table(rows, col_widths, head=("Situation", "Critère", "Conduite à tenir")):
    data = [[P(h, S_HEAD_W) for h in head]]
    for r in rows:
        data.append([P(r[0], S_CELL_B), P(r[1], S_CELL), P(r[2], S_CELL)])
    t = Table(data, colWidths=col_widths, repeatRows=1)
    style_cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), NAVY), ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTNAME", (0, 0), (-1, 0), FONT_BOLD), ("FONTSIZE", (0, 0), (-1, 0), 8),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
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
DCW = [34 * mm, 62 * mm, CW_FULL - 34 * mm - 62 * mm]

def bullets(items, style=S_BODY_SM):
    html = "&bull; " + "<br/>&bull; ".join(items)
    return P(html, style)

TOTAL_PAGES = {"n": 5}

def on_page(canvas, doc, page_title):
    header_band(canvas, doc, "GIHP — RÉACTUALISATION, SEPTEMBRE 2016",
                "Hémorragies et gestes urgents sous dabigatran",
                page_title, icon_fn=lambda c, x, y: icon_drop(c, x, y, 13 * mm), color=RED)
    footer_band(canvas, doc, SOURCE_TXT, f"Page {doc.page} / {TOTAL_PAGES['n']}")

# ---------------------------------------------------------------------------
def _section_intro_agents():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Résumé :</b> réactualisation 2016 des propositions GIHP de 2013, "
        "spécifiquement pour le <b>dabigatran</b> (anti-IIa), pour lequel un antidote "
        "spécifique — l'<b>idarucizumab</b> (Praxbind®) — est désormais disponible. "
        "Un complément est annoncé pour les AOD anti-Xa (rivaroxaban, apixaban) "
        "lorsqu'un antidote spécifique sera disponible pour eux. "
        "<b>L'AVC ischémique n'est pas abordé</b> — orienter vers les recommandations "
        "des sociétés référentes pour la thrombolyse/thrombectomie sous dabigatran.",
        S_BODY), bg=RED_LIGHT, border=RED))
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("Agents hémostatiques disponibles"))
    story.append(Spacer(1, 1.5 * mm))
    story.append(theme_table([
        ("Idarucizumab (Praxbind®)",
         "<b>Antidote spécifique du dabigatran.</b> Fragment d'anticorps monoclonal "
         "humanisé, forte affinité (≈ 300× celle du dabigatran pour la thrombine). "
         "Dose recommandée : <b>5 g (2 × 2,5 g/50 mL)</b>, sans ajustement à l'âge, à "
         "la concentration, ni à la fonction rénale/hépatique. Ni contre-indication ni "
         "interaction médicamenteuse rapportée. Effet parfois transitoire (redistribution "
         "possible, concentration de dabigatran libre réapparaissant chez 21 % des "
         "patients à 24 h dans l'étude REVERSE-AD) — une 2e dose de 5 g peut être "
         "envisagée si réapparition d'un saignement avec allongement des tests de "
         "coagulation (TCA, dTT ou ECT), ou avant une 2e intervention/geste urgent avec "
         "temps de coagulation encore allongés. Mesurer la concentration de dabigatran "
         "avant et 12-18 h après l'administration si la situation l'exige."),
        ("CCP non activés (4 facteurs) / FEIBA® (activé)",
         "En l'absence d'idarucizumab : <b>CCP non activés 50 U/kg</b> ou <b>FEIBA® "
         "30-50 U/kg</b>, éventuellement renouvelés 8 h après la première administration "
         "(hémorragie dans un organe critique/choc). Efficacité non formellement établie "
         "(pas d'essai clinique, tests in vitro/ex vivo et modèles animaux uniquement). "
         "Risque thrombotique potentiel, non évalué dans ce contexte spécifique — plus "
         "fréquent aux fortes doses. <b>N'ont pas démontré leur capacité à neutraliser le "
         "dabigatran pour permettre une anesthésie périmédullaire ou un bloc nerveux "
         "profond</b> — non recommandés dans cette indication."),
        ("Dialyse / charbon activé",
         "Le dabigatran est dialysable, mais la place de la dialyse n'est pas clairement "
         "établie et la disponibilité de l'idarucizumab en réduit encore l'intérêt "
         "potentiel. Charbon activé proposé pour limiter l'absorption digestive "
         "(mentionné pour de rares cas d'intoxication volontaire)."),
    ], TCW))
    return story

# ---------------------------------------------------------------------------
def _section_seuils():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Seuils de sécurité et tests de coagulation"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(P(
        "Le seuil hémostatique en deçà duquel un saignement ne peut être attribué au "
        "dabigatran est mal connu : il varie entre <b>50 ng/mL</b> (concentration "
        "résiduelle moyenne après 2 demi-vies, sans insuffisance rénale) et "
        "<b>30 ng/mL</b> (après 3-4 demi-vies). Un <b>TT (temps de thrombine) normal</b> "
        "exclut avec certitude une concentration significative de dabigatran (test très "
        "sensible) — à l'inverse, un TCA/TQ normal n'exclut pas une concentration "
        "au-dessus du seuil de sécurité. <b>DDP</b> = délai depuis la dernière prise de "
        "dabigatran ; <b>ClCr</b> = clairance de la créatinine (formule de Cockcroft et "
        "Gault).", S_BODY_SM))
    return story

# ---------------------------------------------------------------------------
def _section_figure1():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Figure 1 — Prise en charge des hémorragies sous dabigatran"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(decision_table([
        ("Hémorragie dans un organe critique ou choc hémorragique",
         "Conc. dabigatran > 50 ng/mL, ou conc. inconnue ET (DDP ≤ 24 h OU ClCr ≤ 50 mL/min)",
         "Idarucizumab ou, si indisponible, CCP ou FEIBA"),
        ("Hémorragie dans un organe critique ou choc hémorragique",
         "Conc. dabigatran ≤ 50 ng/mL, ou conc. inconnue ET DDP > 24 h ET ClCr > 50 mL/min",
         "Mesures non spécifiques"),
        ("Hémorragie grave (autre)",
         "Geste hémostatique (chirurgie, endoscopie, embolisation, tamponnement…) réalisé en premier",
         "Geste efficace → mesures non spécifiques suffisantes ; geste non indiqué ou "
         "saignement persistant → passer aux critères de concentration ci-dessous"),
        ("Hémorragie grave (autre), geste non indiqué/inefficace",
         "Conc. dabigatran > 50 ng/mL, ou conc. inconnue ET (DDP ≤ 24 h OU ClCr ≤ 50 mL/min)",
         "Idarucizumab ou, si indisponible, CCP ou FEIBA"),
        ("Hémorragie grave (autre), geste non indiqué/inefficace",
         "Conc. dabigatran ≤ 50 ng/mL, ou conc. inconnue ET DDP > 24 h ET ClCr > 50 mL/min",
         "Mesures non spécifiques"),
        ("Hémorragie non grave",
         "Absence de tout signe de gravité, quelle que soit la concentration",
         "Traitement symptomatique — pas de neutralisation. Rechercher une contre-"
         "indication au dabigatran (ClCr ≤ 30 mL/min, interactions) ; discuter un simple "
         "saut de prise ou une réévaluation du traitement anticoagulant."),
    ], DCW))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "« Hémorragie grave » (définition HAS/GEHT 2008, reprise ici) : hémorragie "
        "extériorisée non contrôlable, instabilité hémodynamique, nécessité d'un geste "
        "hémostatique urgent ou d'une transfusion, ou localisation menaçant le pronostic "
        "vital/fonctionnel (intracrânienne, intraspinale, intraoculaire, hémothorax, "
        "hémopéritoine, hémopéricarde, hématome profond/syndrome de loge, hémorragie "
        "digestive aiguë, hémarthrose).", S_NOTE))
    return story

# ---------------------------------------------------------------------------
def _section_figure2():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Figure 2 — Geste invasif urgent sous dabigatran"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(P(
        "Trois niveaux de risque hémorragique du geste : <b>très élevé</b> (hémostase "
        "incontrôlable — ex. neurochirurgie, chirurgie hépatique), <b>élevé</b> "
        "(hémostase contrôlable — ex. péritonite, orthopédie), <b>faible</b>.", S_BODY_SM))
    story.append(Spacer(1, 1.5 * mm))
    story.append(decision_table([
        ("Risque très élevé",
         "Conc. > 30 ng/mL ou inconnue — prise en charge ≤ 8 h ou geste d'hémostase",
         "Idarucizumab (ou si indisponible CCP/FEIBA) puis réaliser le geste"),
        ("Risque très élevé",
         "Conc. > 30 ng/mL ou inconnue — prise en charge > 8 h",
         "Reporter et mesurer la concentration, ou administrer idarucizumab (ou CCP/FEIBA) "
         "puis réaliser le geste"),
        ("Risque élevé",
         "Conc. > 50 ng/mL, ou inconnue ET (DDP ≤ 24 h OU ClCr ≤ 50 mL/min) — PEC ≤ 8 h",
         "Réaliser le geste ; si saignement per/postopératoire attribuable au dabigatran : "
         "idarucizumab (ou si indisponible CCP/FEIBA)"),
        ("Risque élevé",
         "Conc. > 50 ng/mL, ou inconnue ET (DDP ≤ 24 h OU ClCr ≤ 50 mL/min) — PEC > 8 h",
         "Reporter et mesurer la concentration, ou réaliser le geste avec la même conduite "
         "qu'en PEC ≤ 8 h si saignement attribuable"),
        ("Risque faible, OU risque élevé avec conc. ≤ 50 ng/mL (ou inconnue ET DDP > 24 h "
         "ET ClCr > 50 mL/min), OU risque très élevé avec conc. ≤ 30 ng/mL",
         "Saignement, s'il survient, ne peut raisonnablement pas être attribué au "
         "dabigatran",
         "Réaliser le geste sans délai — pas de neutralisation"),
    ], DCW))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "Agents hémostatiques à administrer en peropératoire si le saignement n'est pas "
        "contrôlable par le chirurgien, plutôt qu'en prophylaxie préopératoire "
        "systématique.", S_NOTE))
    return story

# ---------------------------------------------------------------------------
def _section_figure3():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Figure 3 — Anesthésie, analgésie et chirurgie urgente sous dabigatran"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(P(
        "L'anesthésie périmédullaire et les gestes neuraxiaux (ponction lombaire, "
        "rachianesthésie, péridurale, injections rachidiennes) sont <b>contre-indiqués "
        "sous anticoagulant</b> — préférer l'anesthésie générale sauf contre-indication "
        "majeure à celle-ci.", S_BODY_SM))
    story.append(Spacer(1, 1.5 * mm))
    story.append(decision_table([
        ("Bloc nerveux superficiel* (risque hémorragique faible)",
         "Conc. dabigatran > 30 ng/mL ou inconnue",
         "Évaluer le rapport bénéfice/risque : favorable au bloc superficiel → réaliser "
         "le geste ; défavorable → autres techniques d'anesthésie/analgésie"),
        ("Bloc nerveux superficiel* (risque hémorragique faible)",
         "Conc. dabigatran ≤ 30 ng/mL",
         "Réaliser le geste"),
        ("Anesthésie périmédullaire** ou bloc nerveux profond* (risque hémorragique très élevé)",
         "Conc. dabigatran ≤ 30 ng/mL",
         "Réaliser le geste"),
        ("Anesthésie périmédullaire** ou bloc nerveux profond* (risque hémorragique très élevé)",
         "Conc. dabigatran > 30 ng/mL ou inconnue",
         "Contre-indication aux autres techniques d'anesthésie/analgésie : si oui → "
         "idarucizumab*** puis réaliser le geste ; si non → autres techniques"),
    ], DCW))
    story.append(Spacer(1, 1.5 * mm))
    story.append(bullets([
        "* Blocs nerveux périphériques réalisés par un opérateur expérimenté et par "
        "échoguidage. Cathéter périnerveux : ne doit pas compromettre la reprise "
        "postopératoire des anticoagulants ; retrait dans des conditions hémostatiques "
        "optimales.",
        "** Anesthésie périmédullaire réalisée par un opérateur expérimenté, en ponction "
        "unique, aiguille fine pour la rachianesthésie. Cathéter péridural : mêmes règles "
        "que la rachianesthésie pour la mise en place et le retrait.",
        "*** Les CCP (activés ou non) n'ont pas démontré leur capacité à neutraliser le "
        "dabigatran — non recommandés pour permettre la réalisation de l'ALR à leur "
        "place.",
    ]))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>Ponction lombaire diagnostique en urgence</b> (ex. suspicion de méningite) : "
        "également contre-indiquée sous dabigatran, mais si jugée indispensable, "
        "l'administration d'idarucizumab avant le geste peut être proposée (CCP non "
        "recommandés dans cette indication faute de garantie sur l'hémostase). La PL doit "
        "être réalisée avec une aiguille fine par un opérateur expérimenté ; une "
        "antibiothérapie probabiliste ne doit pas être retardée par l'attente du geste "
        "(Société de Pathologie Infectieuse de Langue Française).", S_BODY_SM))
    return story

# ---------------------------------------------------------------------------
def _section_sources():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("Sources et avertissement"))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "Albaladejo P, Pernod G, Godier A, de Maistre E, Rosencher N, Mas JL, et al., pour "
        "le GIHP, « Prise en charge des hémorragies et des gestes invasifs urgents chez "
        "les patients recevant un anticoagulant oral et direct anti-IIa (dabigatran) », "
        "réactualisation septembre 2016. 37 références bibliographiques dans le texte "
        "intégral (non reproduites ici).", S_SOURCE))
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Avertissement — périmètre dabigatran uniquement :</b> cette fiche est une "
        "synthèse indépendante, produite pour un usage d'aide-mémoire. Elle condense la "
        "justification pharmacologique détaillée (études, mécanismes) mais reprend "
        "intégralement la logique décisionnelle des 3 figures du texte source, "
        "transcrites en tableaux plutôt qu'en graphique pour une lecture plus rapide sur "
        "mobile/PC. <b>Ce texte ne couvre que le dabigatran</b> — un complément pour les "
        "AOD anti-Xa (rivaroxaban, apixaban) était annoncé pour quand un antidote "
        "spécifique serait disponible pour eux (voir la fiche « AOD : chirurgie et "
        "hémorragie en urgence », 2013, pour les principes généraux applicables aux "
        "AOD anti-Xa en l'absence d'antidote spécifique alors disponible). Elle ne "
        "remplace pas le texte intégral et n'est ni éditée ni validée par le GIHP/SFAR. "
        "Les données d'efficacité de l'idarucizumab reposent sur une étude non "
        "randomisée, non contrôlée (REVERSE-AD, analyse intermédiaire) — vérifier les "
        "données/AMM actualisées avant application.",
        S_BODY_SM), bg=GREY_LIGHT, border=GREY))
    return story

# ---------------------------------------------------------------------------
def _section_all():
    story = _section_intro_agents()
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_seuils())
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_figure1())
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_figure2())
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_figure3())
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_sources())
    return story

SECTIONS = [
    ("Agents hémostatiques, seuils, hémorragies (Fig. 1), gestes urgents (Fig. 2), ALR (Fig. 3) & sources",
     _section_all),
]

def _make_doc(path=None):
    return SimpleDocTemplate(path or OUT, pagesize=A4,
                              leftMargin=MARGIN, rightMargin=MARGIN,
                              topMargin=32 * mm, bottomMargin=16 * mm,
                              title="Fiche GIHP 2016 - Hemorragies et gestes urgents sous dabigatran",
                              author="Synthèse indépendante (source GIHP)")

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
