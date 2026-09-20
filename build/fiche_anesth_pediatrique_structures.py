# -*- coding: utf-8 -*-
"""
Fiche de synthese - "Recommandations pour les structures et le materiel de
l'anesthesie pediatrique" - SFAR, septembre 2000. Groupe d'experts coordonne
par C. Ecoffey (Rennes). 7 pages, telecharge depuis sfar.org (wp-content/
uploads/2015/10/2_SFAR_Recommandations-pour-les-structures-et-le-materiel-
de-lanesthesie-pediatrique.pdf).

METHODOLOGIE : texte narratif de specifications pratiques (structures +
materiel), organise en 2 parties (I - Structures, II - Materiel) et leurs
sous-sections numerotees - AUCUN systeme de cotation GRADE, aucune
recommandation numerotee R1/R2 (meme convention que fiche_preparation_
colique.py / fiche_erreurs_medicamenteuses_ar_2016.py : "il faut"/constats
factuels/specifications materielles chiffrees, sans grille formelle). Les
dispositions generales SFAR (surveillance peranesthesique, decret du 5
decembre 1994) s'appliquent en pediatrie ; ce texte precise UNIQUEMENT les
particularites liees au jeune age.

DISTINCT du document "Organisation de l'anesthesie pediatrique" (SFAR RPP
2023, deja repertorie dans library_final.json sous une URL/portee
differente - organisation des centres/typologie, pas structures physiques
et materiel) - non construit dans cette session, verifie par grep de titre
avant construction, aucune collision de cle.

PERIMETRE : integral sur les 2 parties (Structures + Materiel) et leurs
sous-sections. La liste nominative du groupe d'experts (page 1) n'est pas
transcrite (renvoi au texte integral).
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from style import *
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.units import mm

OUT = "/home/user/rfe-sfar-website/output/Fiche_SFAR_Structures_Materiel_Anesthesie_Pediatrique_2000.pdf"

SOURCE_TXT = ("Source : SFAR, « Recommandations pour les structures et le matériel de l'anesthésie "
              "pédiatrique », septembre 2000. Fiche de synthèse non officielle : se référer au texte "
              "intégral.")

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

TCW = [40 * mm, CW_FULL - 40 * mm]

def bullets(items, style=S_BODY_SM):
    html = "&bull; " + "<br/>&bull; ".join(items)
    return P(html, style)

TOTAL_PAGES = {"n": 4}

def on_page(canvas, doc, page_title):
    header_band(canvas, doc, "SFAR — RECOMMANDATIONS, SEPTEMBRE 2000",
                "Structures et matériel de l'anesthésie pédiatrique",
                page_title, icon_fn=lambda c, x, y: icon_shield(c, x, y, 13 * mm), color=TEAL_DARK)
    footer_band(canvas, doc, SOURCE_TXT, f"Page {doc.page} / {TOTAL_PAGES['n']}")

# ---------------------------------------------------------------------------
def _section_structures():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Résumé :</b> les dispositions SFAR sur la surveillance péri-anesthésique et le "
        "décret du 5 décembre 1994 (sécurité en anesthésie) s'appliquent en pédiatrie. Ce "
        "texte précise les particularités liées au jeune âge, pour la chirurgie réglée "
        "comme pour l'urgence — sans créer de monopole pour les grands centres, mais pour "
        "fixer un standard de l'anesthésie pédiatrique.", S_BODY), bg=BG_PANEL, border=TEAL))
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("I — Structures"))
    story.append(Spacer(1, 1.5 * mm))
    story.append(theme_table([
        ("1. Salle d'intervention",
         "Idéalement, bloc opératoire spécifiquement pédiatrique avec SSPI dédiée "
         "(ergonomie/hygiène : mêmes recommandations SFAR). Personnel selon l'âge : "
         "0-1 mois — au minimum un médecin anesthésiste-réanimateur assisté d'un(e) "
         "infirmier(e) ou d'un autre anesthésiste-réanimateur ; 1 mois-10 ans — "
         "assistance infirmière à l'induction/extubation (voire pendant l'anesthésie) "
         "si le médecin le juge nécessaire selon la chirurgie/le terrain."),
        ("2. Transferts entre unités (post-opératoire)",
         "Structures contiguës, interventions lourdes : transport dans le lit/table de "
         "réanimation/incubateur sans rupture de soins/monitorage, sous surveillance "
         "directe du médecin. Interventions mineures : transmissions écrites "
         "suffisantes, complétées à l'oral si besoin. Structures éloignées : transfert "
         "par équipe mobile médicalisée avec matériel adapté (cf. Matériel de "
         "transport)."),
        ("3. Salle de surveillance post-interventionnelle (SSPI)",
         "Même matériel que le bloc, adapté à l'âge. Emplacements : &gt; 1,5, "
         "probablement 2 par salle d'opération (chirurgie pédiatrique plus courte), "
         "adapté au flux (ORL, ambulatoire). Personnel conforme aux recommandations "
         "SFAR, adapté si surcroît de surveillance nécessaire (âge préscolaire). "
         "Qualification conforme au décret du 5 décembre 1994 ; infirmier(e) "
         "puériculteur(trice) utile si SSPI pédiatrique dédiée. À défaut de structure "
         "dédiée : individualiser un secteur du bloc/SSPI polyvalent pour l'activité "
         "pédiatrique."),
        ("4. Prise en charge post-opératoire (hospitalisation)",
         "Idéalement service d'hospitalisation spécifiquement pédiatrique (secteur "
         "traditionnel, soins intensifs, réanimation). En structure mixte, respecter "
         "la circulaire n°83-24 du 1er août 1983 et la charte de l'enfant hospitalisé "
         "(EACH/parlement européen/Conseil de l'Europe/OMS) : présence des parents "
         "facilitée, pas d'hospitalisation en service adulte, réduction des durées "
         "(hospitalisation de jour), regroupement par tranches d'âge, visites libres "
         "sans limite d'âge, environnement adapté (physique/affectif), formation des "
         "soignants aux besoins psychologiques, intimité préservée. <b>L'hospitalisation "
         "d'enfants de moins de 10 ans en réanimation adulte ne se justifie pas</b> — "
         "transfert vers un service pédiatrique spécifique à distance si besoin."),
        ("5. Laboratoires et examens complémentaires",
         "Non problématique en hôpital d'enfants avec plateau technique dédié. "
         "Ailleurs : réseau de correspondants formés à la pratique pédiatrique."),
    ], TCW))
    return story

# ---------------------------------------------------------------------------
def _section_materiel_respiratoire():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("II — Matériel : assistance respiratoire"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(P(
        "Hors centre à vocation pédiatrique exclusive : chariot spécifique regroupant le "
        "matériel adapté au poids/âge de l'enfant. Masques, canules, sondes, lames de "
        "laryngoscope et ballons doivent être adaptés à la taille de l'enfant.", S_BODY_SM))
    story.append(Spacer(1, 1.5 * mm))
    story.append(theme_table([
        ("Masque facial", "Si possible transparent, à petit espace mort ; masque rond à "
         "bourrelet chez le nouveau-né. Tailles disponibles : 00 à 4."),
        ("Canule oro-pharyngée", "Disponible mais non obligatoire si la langue n'obstrue "
         "pas le flux gazeux. Tailles : 00 à 4."),
        ("Ballons", "Adaptés au volume courant (tailles 500/750/1000/1500 ml — pression "
         "en ventilation contrôlée proportionnelle au carré du rayon). Ballons "
         "auto-gonflables adaptés à l'âge impératifs."),
        ("Valves", "Système de détrompage obligatoire (arrêté du 30 août 1996). "
         "Induction : valve de David® ou circuit respirateur (avec réinhalation), ou "
         "valve de Ruben®/Ambu® enfant-adulte (sans réinhalation) — circuit machine "
         "théoriquement inutilisable avant 1 an. Entretien : mêmes valves + valve de "
         "Digby-Leigh® (sans réinhalation), le plus souvent circuit du respirateur."),
        ("Plateau d'intubation", "Manche de laryngoscope, lames droites (Miller 0/1/2) "
         "et courbes (Macintosh 1/2/3) selon l'âge, pinces de Magill (adulte/enfant), "
         "mandrins atraumatiques, seringue de gonflage, manomètre de pression du "
         "ballonnet, système de fixation."),
        ("Sondes d'intubation", "Tailles 2,5 à 6,5 ; diamètre calculé par formule "
         "au-dessus de 2 ans. Sondes armées ou préformées selon le type de chirurgie."),
        ("Masque laryngé", "Alternative au masque facial/à la sonde d'intubation. "
         "Tailles disponibles : 1 à 3."),
        ("Respirateurs d'anesthésie", "Volume courant adapté à l'âge/poids (faibles "
         "volumes &lt; 50 ml, fréquences élevées jusqu'à 80 c/min), PEP disponible, "
         "réglage précis du rapport I/E, adaptation d'évaporateurs différents sans "
         "fonctionnement simultané possible. Tuyaux de taille/compliance adaptés "
         "(petits tuyaux &lt; 10 kg), correction automatique de compliance "
         "préférable. Circuit à bas débit (≈ 1 L/min) utilisable &gt; 5 kg (nécessite "
         "débitmètres de précision ; capnographie moins fiable &gt; 30 c/min). "
         "Ventilateur de réanimation exceptionnellement nécessaire (compliance "
         "thoraco-pulmonaire très basse). Filtre antimicrobien recommandé (Recos "
         "hygiène SFAR 1997), taille adaptée (filtre spécifique &lt; 10 kg)."),
        ("Intubation difficile", "Algorithme obligatoire par équipe, maîtrise d'au "
         "moins une technique d'attente et une de sauvetage, matériel adapté à l'âge/"
         "poids."),
        ("Drain pleural", "Tailles disponibles : 8 à 14."),
    ], TCW, head=("Matériel", "Spécifications")))
    return story

# ---------------------------------------------------------------------------
def _section_materiel_autre():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("II — Matériel : abord vasculaire, monitorage, hypothermie, transport"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(theme_table([
        ("Abord vasculaire", "Périphérique : gamme complète de cathéters courts, du "
         "24G au 14G. Central : cathéters simples/multi-voies adaptés à l'âge/"
         "indication/abord ; contrôle radiologique indispensable (amplificateur de "
         "brillance au bloc). Abord intra-osseux disponible en urgence vitale si "
         "échec de l'abord veineux conventionnel."),
        ("Défibrillateur", "Palettes pédiatriques et réglage de l'intensité "
         "obligatoires."),
        ("Monitorage — fonction cardiovasculaire", "Électrodes ECG adaptées à la "
         "taille. PA non invasive par oscillométrie : jeu complet de brassards "
         "(tailles 1 à 4 et adulte), brassard couvrant les 2/3 du bras. PA invasive : "
         "cathéters courts transcutanés ou spécifiques à l'abord artériel. Oxymétrie "
         "de pouls : capteurs de taille adaptée. PVC : ponction jugulaire, "
         "sous-clavière ou fémorale."),
        ("Monitorage — fonction ventilatoire", "Capnographie interprétable "
         "normalement (sous-estimation possible &gt; 30 c/min) — monitorage le plus "
         "distal, débit aspiratif élevé (&gt; 150 ml/min), analyse rapide ; capteur "
         "pédiatrique si capnographe non aspiratif et enfant &lt; 20 kg. Pressions "
         "transcutanées O2/CO2 utiles chez le nouveau-né/petit nourrisson."),
        ("Monitorage — divers", "Analyse continue de la FiO2 et des gaz halogénés "
         "obligatoire. Température : sonde rectale ou (mieux) œsophagienne. "
         "Curarisation : même matériel que l'adulte."),
        ("Prévention de l'hypothermie", "D'autant plus impérative que l'enfant est "
         "petit ; monitorée. Mesures : bonnet/manchons de jersey ; matelas chauffant "
         "avec alarmes ou couverture à air pulsé (forme adaptée, usage unique) ; "
         "réchauffement/humidification des gaz ; température de la salle 20-26 °C, "
         "limitation des allées-venues ; réchauffement des perfusions/transfusions, "
         "antiseptiques, champs opératoires, solutions de cystoscopie. Chez les plus "
         "petits : lampe infrarouge/table radiante à l'induction, couveuse/table "
         "radiante au réveil."),
        ("Matériel de transport", "Recommandations SFAR sur les transferts "
         "interhospitaliers (1992) et intrahospitaliers (1994) médicalisés. "
         "Spécificités pédiatriques : monitorage et réchauffement (tables "
         "radiantes/couveuses sur batterie). Respirateur de transport adapté au poids "
         "requis pour les patients intubés-ventilés (mode pression contrôlée chez le "
         "nouveau-né/nourrisson, volume contrôlé chez l'enfant plus grand)."),
        ("Solutés", "Solutés poly-ioniques glucosés (G1/2,5/5/10 %) ; compensations "
         "par sérum salé 0,9 % ou Ringer lactate — un seul type de soluté "
         "d'entretien/compensation recommandé pour simplifier les protocoles. "
         "Remplissage : albumine chez le nouveau-né/petit nourrisson, cristalloïdes/"
         "colloïdes de synthèse chez l'enfant plus grand. Contrôle du débit "
         "indispensable &lt; 100 ml/h (pompe, seringue électrique, ou à défaut "
         "perfuseurs de précision) — régulateurs par réduction de calibre (type "
         "Dial-a-Flow®) à manier avec prudence, non fiables chez le petit enfant."),
    ], TCW, head=("Matériel", "Spécifications")))
    return story

# ---------------------------------------------------------------------------
def _section_sources():
    story = []
    story.append(Spacer(1, 1.5 * mm))
    story.append(section_bar("Sources et avertissement"))
    story.append(Spacer(1, 1 * mm))
    story.append(P(
        "SFAR, « Recommandations pour les structures et le matériel de l'anesthésie "
        "pédiatrique », septembre 2000, groupe d'experts coordonné par C. Ecoffey "
        "(Rennes).", S_SOURCE))
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Avertissement — document de 2000 :</b> cette fiche est une synthèse "
        "indépendante, produite pour un usage d'aide-mémoire. Elle reprend "
        "intégralement les 2 parties (Structures, Matériel) du texte source mais omet "
        "la liste nominative des experts. Elle ne remplace pas le texte intégral et "
        "n'est ni éditée ni validée par la SFAR. Les textes réglementaires cités "
        "(décret du 5 décembre 1994, arrêté du 30 août 1996, circulaire de 1983) et "
        "les données constructeur (tailles/références commerciales) datent de la "
        "publication — vérifier leur actualité et celle du matériel disponible avant "
        "application. Document distinct de la RPP SFAR 2023 « Organisation de "
        "l'anesthésie pédiatrique » (organisation des centres), non traitée ici.",
        S_BODY_SM), bg=GREY_LIGHT, border=GREY))
    return story

# ---------------------------------------------------------------------------
def _section_all():
    story = _section_structures()
    story.append(Spacer(1, 1.5 * mm))
    story.extend(_section_materiel_respiratoire())
    story.append(Spacer(1, 1.5 * mm))
    story.extend(_section_materiel_autre())
    story.append(Spacer(1, 1.5 * mm))
    story.extend(_section_sources())
    return story

SECTIONS = [
    ("Structures, matériel (respiratoire, vasculaire, monitorage, hypothermie, transport) & sources",
     _section_all),
]

def _make_doc(path=None):
    return SimpleDocTemplate(path or OUT, pagesize=A4,
                              leftMargin=MARGIN, rightMargin=MARGIN,
                              topMargin=32 * mm, bottomMargin=16 * mm,
                              title="Fiche SFAR 2000 - Structures et materiel de l'anesthesie pediatrique",
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
