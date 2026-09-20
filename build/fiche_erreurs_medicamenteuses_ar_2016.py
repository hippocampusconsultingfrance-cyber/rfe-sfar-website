# -*- coding: utf-8 -*-
"""
Fiche de synthese - "Prevention des erreurs medicamenteuses en anesthesie et
en reanimation (texte court)" - Synthese des preconisations de la SFAR en
partenariat avec la Societe Francaise de Pharmacie Clinique (SFPC),
actualisation 2016 (Comite de pilotage : V. Piriou ; coordinateurs : R.
Collomp, A. Theissen). Valide par les Conseils d'administration de la SFAR
et de la SFPC. 12 pages (9 pages de contenu + bibliographie de 32
references), telecharge depuis sfar.org (wp-content/uploads/2016/11/texte-
court-preco-erreurs-med-2016-SFAR-SFPC-version-finale-25-oct-2016.pdf).

METHODOLOGIE : 10 preconisations numerotees (1 a 10), chacune enoncee en
gras dans le texte source puis suivie d'un paragraphe d'elaboration - AUCUN
systeme de cotation GRADE ni niveau de preuve individuel (meme convention
que fiche_aod_programme.py : "propositions" pragmatiques sans grille
formelle). Pas de chip invente ici non plus.

DISTINCT du document deja construit fiche_erreurs_medicamenteuses.py
(site/app.js key "erreurs_medicamenteuses", SFAR seule, novembre 2006,
"Prevention des erreurs medicamenteuses en anesthesie") : celui-ci est
l'actualisation 2016, coecrite avec la SFPC, qui elargit explicitement le
perimetre a la reanimation ("en A-R" = anesthesie-reanimation) et ajoute
une preconisation dediee aux specificites de la reanimation/soins
critiques (Preconisation 5) - verifie par grep needle sur les deux URLs
sfar.org (preverreurmedic_recos.pdf vs texte-court-preco-erreurs-med-2016),
aucune collision de cle.

PERIMETRE : integral sur les 10 preconisations. La liste nominative des
auteurs/relecteurs (page 2 du PDF source) et les 32 references
bibliographiques (pages 9-12) ne sont pas transcrites (renvoi au texte
integral), conformement a la regle de projet 2026-09-14 (argumentaire
minimal) - non actionnable cliniquement.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from style import *
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.units import mm

OUT = "/home/user/rfe-sfar-website/output/Fiche_SFAR_SFPC_Erreurs_Medicamenteuses_AR_2016.pdf"

SOURCE_TXT = ("Source : SFAR/SFPC, « Prévention des erreurs médicamenteuses en anesthésie et en "
              "réanimation » (texte court), actualisation 2016. Fiche de synthèse non officielle : "
              "se référer au texte intégral.")

def P(txt, style=S_CELL):
    return Paragraph(txt, style)

CW_FULL = PAGE_W - 2 * MARGIN

def theme_table(rows, col_widths, head=("N°", "Préconisation")):
    data = [[P(head[0], S_HEAD_W), P(head[1], S_HEAD_W)]]
    for theme, detail in rows:
        data.append([P(theme, S_CELL_B), P(detail, S_CELL)])
    t = Table(data, colWidths=col_widths, repeatRows=1)
    style_cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), NAVY), ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTNAME", (0, 0), (-1, 0), FONT_BOLD), ("FONTSIZE", (0, 0), (-1, 0), 8),
        ("VALIGN", (0, 0), (-1, -1), "TOP"), ("ALIGN", (0, 1), (0, -1), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 0.5, GREY_LIGHT),
        ("TOPPADDING", (0, 0), (-1, -1), 3.4), ("BOTTOMPADDING", (0, 0), (-1, -1), 3.4),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            style_cmds.append(("BACKGROUND", (0, i), (-1, i), BG_PANEL))
    t.setStyle(TableStyle(style_cmds))
    return t

TCW = [12 * mm, CW_FULL - 12 * mm]

def bullets(items, style=S_BODY_SM):
    html = "&bull; " + "<br/>&bull; ".join(items)
    return P(html, style)

TOTAL_PAGES = {"n": 4}

def on_page(canvas, doc, page_title):
    header_band(canvas, doc, "SFAR / SFPC — PRÉCONISATIONS, ACTUALISATION 2016",
                "Prévention des erreurs médicamenteuses en anesthésie-réanimation",
                page_title, icon_fn=lambda c, x, y: icon_pill(c, x, y, 13 * mm), color=TEAL_DARK)
    footer_band(canvas, doc, SOURCE_TXT, f"Page {doc.page} / {TOTAL_PAGES['n']}")

# ---------------------------------------------------------------------------
def _section_intro_strategie():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Résumé :</b> la fréquence élevée des erreurs médicamenteuses (EM) en "
        "anesthésie-réanimation, leur gravité potentielle et leur caractère évitable "
        "justifient l'actualisation des préconisations SFAR de 2006, désormais "
        "coécrites avec la Société Française de Pharmacie Clinique (SFPC) et élargies "
        "à la réanimation. Une grille d'évaluation spécifique (auto-évaluation, audit "
        "croisé, préparation à la certification HAS/EPP) accompagne ces 10 "
        "préconisations.", S_BODY), bg=BG_PANEL, border=TEAL))
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("Niveau stratégique et organisationnel"))
    story.append(Spacer(1, 1.5 * mm))
    story.append(theme_table([
        ("1", "Toute structure réalisant anesthésies et/ou réanimation met en œuvre, de "
         "manière pérenne, des mesures écrites et cohérentes avec la démarche "
         "institutionnelle vis-à-vis de la prévention et du traitement des EM ainsi que "
         "du retour d'expérience (REX) associé — analyse selon des méthodes validées "
         "(REMED, ALARM, RMM), mesures d'impact et réévaluation régulière."),
        ("2", "Une équipe pluriprofessionnelle dédiée à la sécurisation de la prise en "
         "charge médicamenteuse (PECM) — au minimum médecin anesthésiste-réanimateur, "
         "cadre de santé, IADE et IDE de SSPI/réanimation, pharmacien — réalise des "
         "analyses a priori (cartographie des risques) et a posteriori (analyse des "
         "EM) sur tout le parcours de soins, de l'admission à la sortie du patient."),
    ], TCW))
    return story

# ---------------------------------------------------------------------------
def _section_risques_formation():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Facteurs de risque, formation et spécificités"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(theme_table([
        ("3", "Étudier particulièrement : gestion des traitements habituels du patient, "
         "médicaments à haut risque et « never events », informatisation de la "
         "prescription et ses interfaces, facteurs humains/organisationnels, "
         "interruptions de tâches. Conciliation médicamenteuse dès la consultation "
         "d'anesthésie (dossier pharmaceutique) ; rôles des chirurgiens/anesthésistes/"
         "IDE/pharmaciens à formaliser pour la gestion du traitement personnel du "
         "patient."),
        ("4", "Formation continue pluriprofessionnelle à la gestion des risques et à la "
         "bonne utilisation des dispositifs d'administration (pompes/pousse-seringues "
         "électriques, lignes de perfusion, ergonomie), ciblant la prévention des "
         "erreurs de préparation/reconstitution et d'administration — privilégier la "
         "simulation en santé, l'e-learning, la « chambre des erreurs » ou le « chariot "
         "piégé »."),
        ("5", "Spécificités réanimation/soins critiques : étiquetage code couleur "
         "international (seringues, voies, poches, PCA/PCEA, chariots), lecture "
         "attentive de l'étiquetage avant administration, règle des <b>5B</b> (bon "
         "médicament, bonne dose, bon moment, bonne voie, bon patient), détrompeurs et "
         "lecteurs code-barres, limitation de la liste des médicaments en dotation "
         "(éviter similitudes forme/couleur/dénomination), déclaration/analyse des EM. "
         "Spécifique à la réanimation : implication régulière d'un pharmacien dans "
         "l'unité, pousse-seringues programmables reliés à des bases intelligentes, "
         "organisation du chariot d'urgence, vigilance particulière pour les sédatifs "
         "et vasopresseurs (les plus souvent en cause)."),
    ], TCW))
    return story

# ---------------------------------------------------------------------------
def _section_prevention_rangement():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Prévention active/passive, rangement et étiquetage"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(theme_table([
        ("6", "Combiner mesures actives de contrôle (humaines, informatiques type "
         "codes-barres) et mesures passives (étiquetages, systèmes mécaniques). "
         "Préparation/administration par la même personne + règle des 5B ; double "
         "lecture par une seconde personne ou seringues à code-barres en complément. "
         "Prévention des erreurs de voie : contrôle du point d'insertion, étiquetage "
         "spécifique par voie, détrompeurs (norme ISO TC210 JWG4 en cours, non encore "
         "commercialisés en France), cathéters/tubulures de couleur ou forme "
         "différente en alternative."),
        ("7", "Système de rangement clair, formalisé et commun à tous les sites de "
         "travail (dotations d'urgence, chariot d'ALR, chariots d'urgence, table "
         "d'anesthésie, plateaux). Responsables du rangement/vérification identifiés, "
         "vérification périodique tracée. Seuls les médicaments strictement "
         "nécessaires sont présents, sans préparation à l'avance. Stockage du KCl et "
         "autres médicaments à haut risque évité au maximum ; si réalisé : précautions "
         "de stockage/étiquetage/délivrance renforcées et personnel sensibilisé."),
        ("8", "Étiquetages spécifiques : (a) voies d'administration — étiquettes "
         "couleur/bordure normées, apposées en proximal et distal ; (b) seringues — "
         "codes couleurs internationaux par classe pharmacologique (norme ISO 26825), "
         "vigilance renforcée pour les curares (risque de confusion avec le "
         "midazolam) ; (c) poches/flacons de préparation — DCI, quantité/concentration, "
         "date/heure et identité du préparateur, identité du patient (code-barres) ; "
         "(d) préparations PCA/PCEA/PSE — identité patient, médicament et dose, volume, "
         "solvant/concentration, date/heure, voie d'administration (couleur "
         "correspondante) ; (e) chariots/dispositifs de stockage — mode de rangement "
         "cohérent avec les règles de l'établissement."),
    ], TCW))
    return story

# ---------------------------------------------------------------------------
def _section_protocoles_rex():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Protocoles et gestion des erreurs (retour d'expérience)"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(theme_table([
        ("9", "Procédures et protocoles validés de prescription/préparation/"
         "administration précisant dilution, solvant, durée, vitesse et voie — "
         "système uniforme formalisé et disponible dans toutes les salles concernées. "
         "Plateaux d'anesthésie préparés selon un plan prédéfini (date/heure, "
         "préparateur, étiquette patient) ; éviter plusieurs concentrations d'un même "
         "médicament simultanément disponibles ; seringues préremplies prioritaires "
         "pour les médicaments d'urgence peu utilisés (atropine, éphédrine, "
         "phényléphrine). <b>Vigilance renforcée antiseptique/anesthésique injectable</b> "
         "(confusion notamment avec la chlorhexidine) : seuls des antiseptiques colorés "
         "doivent être utilisés, avec double lecture à voix haute (molécule, quantité, "
         "volume, concentration) entre celui qui donne l'agent et celui qui le "
         "prépare."),
        ("10", "Toute erreur médicamenteuse (avérée ou potentielle) est analysée selon "
         "une méthode validée (REMED, ALARM), avec retour d'expérience (REX) organisé "
         "auprès de l'équipe concernée et, si pertinent, d'autres secteurs (CREX, RMM, "
         "staffs dédiés). Sont a minima concernées : les erreurs à conséquences graves, "
         "les « Never Events » (liste ANSM) et les événements porteurs de risque. "
         "Déclaration obligatoire au Centre régional de pharmacovigilance (CRPV) en "
         "cas d'impact patient, et possible au Guichet Erreurs Médicamenteuses de "
         "l'ANSM pour toute EM potentielle ou avérée sans événement indésirable."),
    ], TCW))
    return story

# ---------------------------------------------------------------------------
def _section_sources():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("Sources et avertissement"))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "SFAR, en partenariat avec la Société Française de Pharmacie Clinique (SFPC), "
        "« Prévention des erreurs médicamenteuses en anesthésie et en réanimation » "
        "(texte court), actualisation 2016, validée par les Conseils d'administration "
        "de la SFAR et de la SFPC. Une version détaillée à visée pédagogique est "
        "disponible séparément. 32 références bibliographiques dans le texte intégral "
        "(non reproduites ici).", S_SOURCE))
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Avertissement :</b> cette fiche est une synthèse indépendante, produite pour "
        "un usage d'aide-mémoire. Elle reprend intégralement les 10 préconisations du "
        "texte source mais omet la liste nominative des auteurs/relecteurs et la "
        "bibliographie. Elle ne remplace pas le texte intégral (ni la version détaillée "
        "pédagogique) et n'est ni éditée ni validée par la SFAR/SFPC. Document distinct "
        "de la fiche « Prévention des erreurs médicamenteuses en anesthésie » (SFAR "
        "seule, 2006), qu'il actualise et complète pour la réanimation.",
        S_BODY_SM), bg=GREY_LIGHT, border=GREY))
    return story

# ---------------------------------------------------------------------------
def _section_all():
    story = _section_intro_strategie()
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_risques_formation())
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_prevention_rangement())
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_protocoles_rex())
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_sources())
    return story

SECTIONS = [
    ("Stratégie, facteurs de risque, prévention/rangement, protocoles/REX & sources",
     _section_all),
]

def _make_doc(path=None):
    return SimpleDocTemplate(path or OUT, pagesize=A4,
                              leftMargin=MARGIN, rightMargin=MARGIN,
                              topMargin=32 * mm, bottomMargin=16 * mm,
                              title="Fiche SFAR/SFPC 2016 - Prevention des erreurs medicamenteuses en AR",
                              author="Synthèse indépendante (source SFAR/SFPC)")

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
