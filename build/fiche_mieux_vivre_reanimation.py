# -*- coding: utf-8 -*-
"""
Fiche de synthese - Societe Francaise d'Anesthesie et de Reanimation (SFAR)
et Societe de Reanimation de Langue Francaise (SRLF), avec le GFRUP et
l'Adarpef. "Mieux vivre la Reanimation" - 6e Conference de Consensus SFAR-
SRLF (texte long novembre 2009), organisee selon la methodologie de
l'ANAES, Ann Fr Anesth Reanim 29 (2010) 321-330. 10 pages (7 pages de texte
+ 3 pages de bibliographie, 175 references), telecharge depuis sfar.org
(wp-content/uploads/2015/10/2_AFAR_Mieux-vivre-la-reanimation.pdf).

METHODOLOGIE : convention narrative a locutions modales (PAS de grille GRADE
imprimee avec symboles), deja rencontree dans ce corpus (cf.
fiche_aap_programmee.py) - la force de chaque enonce est portee par le verbe
modal lui-meme : « il faut »/« il ne faut pas » = recommandation forte
(equivalent GRADE 1+/1-) ; « il faut probablement »/« il ne faut probablement
pas » = recommandation faible mais jugee importante (equivalent GRADE 2+/2-) ;
« il est... » = constat simple soutenu par des preuves robustes ; « il est
possible » = constat soutenu par des preuves moins robustes. Le sigle RC
(Recommandation Consensuelle) marque les enonces du jury sans reference
scientifique majeure (etudes impossibles pour raisons ethiques, ou evidence
jugee trop manifeste pour necessiter une etude) - transcrit ici comme chip
"RC", distinct des locutions modales gradees qui restent du texte narratif
(pas de chip numerique invente pour un document qui n'en imprime aucun).

PERIMETRE ET CONDENSATION (regle de projet 2026-09-14, argumentaire
minimal) : la Question 1 (barrieres au mieux vivre) est tres majoritairement
descriptive/epidemiologique (constats sans proposition d'action) - condensee
a l'essentiel actionnable ; les Questions 2 a 5 (environnement, soins,
communication, processus decisionnel) portent l'essentiel des enonces
actionnables ("il faut"/"il faut probablement"/RC), integralement repris.
Les 175 references bibliographiques (pages 8-10 du PDF source) ne sont pas
transcrites (renvoi au texte integral).
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from style import *
GRADE_COLORS["RC"] = (GREY, WHITE)
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.units import mm

OUT = "/home/user/rfe-sfar-website/output/Fiche_SFAR_SRLF_Mieux_Vivre_Reanimation_2010.pdf"

SOURCE_TXT = ("Source : SFAR/SRLF, « Mieux vivre la Réanimation », 6e Conférence de Consensus, "
              "Ann Fr Anesth Réanim 29 (2010) 321-330. Fiche de synthèse non officielle : se "
              "référer au texte intégral.")

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

TCW = [42 * mm, CW_FULL - 42 * mm]

def bullets(items, style=S_BODY_SM):
    html = "&bull; " + "<br/>&bull; ".join(items)
    return P(html, style)

TOTAL_PAGES = {"n": 6}

def on_page(canvas, doc, page_title):
    header_band(canvas, doc, "SFAR / SRLF — 6E CONFÉRENCE DE CONSENSUS, NOVEMBRE 2009",
                "Mieux vivre la Réanimation",
                page_title, icon_fn=lambda c, x, y: icon_shield(c, x, y, 13 * mm), color=TEAL_DARK)
    footer_band(canvas, doc, SOURCE_TXT, f"Page {doc.page} / {TOTAL_PAGES['n']}")

# ---------------------------------------------------------------------------
def _section_intro():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Résumé :</b> la réanimation est un lieu de vie mais aussi une agression — pour "
        "les patients, les familles et les soignants. Cette conférence de consensus propose "
        "des recommandations sur 5 thématiques : les barrières au « mieux vivre », "
        "l'amélioration de l'environnement, les soins qui favorisent le mieux vivre, les "
        "stratégies de communication, et la personnalisation du processus décisionnel.",
        S_BODY), bg=BG_PANEL, border=TEAL))
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("Méthodologie — locutions modales (pas de grille GRADE imprimée)"))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "Méthode inspirée de GRADE mais sans symboles imprimés — la force est portée par le "
        "verbe modal du texte lui-même : <b>« il faut » / « il ne faut pas »</b> "
        "(recommandation forte) ; <b>« il faut probablement » / « il ne faut probablement "
        "pas »</b> (recommandation jugée importante mais plus discutable) ; <b>« il est... "
        "»</b> (constat soutenu par des preuves robustes) ; <b>« il est possible »</b> "
        "(constat moins robuste). Le sigle <b>RC</b> (recommandation consensuelle) marque les "
        "énoncés du jury sans référence scientifique majeure — repris tel quel dans cette "
        "fiche, sans chip numérique inventé.", S_BODY_SM))
    return story

# ---------------------------------------------------------------------------
def _section_barrieres():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Q1. Barrières au « mieux vivre » (constats)"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(theme_table([
        ("Patient",
         "Bruit (1re source d'inconfort citée — seuil OMS 45 dB le jour/35 dB la nuit, "
         "alarmes souvent > 80 dB), lumière (absence d'éclairage naturel), manque de "
         "sommeil (2 patients/3), douleur (1 patient/2 — favorise delirium et état de "
         "stress post-traumatique [ESPT]), isolement, contention physique. Le delirium "
         "touche 1 patient/3 et augmente durée de séjour et morbimortalité."),
        ("Familles",
         "Anxiété et dépression fréquentes ; 1 famille/2 comprend mal diagnostic/"
         "pronostic/traitement (facteurs : entretien < 10 min, absence de livret "
         "d'accueil). ESPT chez 1 famille/3 (facteurs : information incomplète, "
         "implication décisionnelle, décès du proche). Charge financière et logistique "
         "souvent sous-estimée — recours à une assistante sociale à proposer "
         "précocement."),
        ("Soignants",
         "Épuisement professionnel (burn-out) chez 1 médecin réanimateur/2 et 1 "
         "infirmier(e)/3 — associé à une moins bonne qualité des soins et plus "
         "d'absentéisme. Facteurs communs au burn-out et à l'ESPT : stress, jeune âge, "
         "conflits, charge de travail, fin de vie. Les soins de « mieux vivre » sont "
         "insuffisamment valorisés et considérés comme non prioritaires."),
    ], TCW, head=("Population", "Constats principaux")))
    return story

# ---------------------------------------------------------------------------
def _section_environnement():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Q2. Comment améliorer l'environnement ?"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(theme_table([
        ("Bruit",
         "<i>Il faut</i> réduire le niveau de bruit, toujours excessif en réanimation. "
         "Mesurer le niveau sonore possible. Moduler l'intensité des alarmes, utiliser des "
         "répétiteurs d'alarme (RC). Politique systématique de réduction du bruit et "
         "sensibilisation des soignants (RC). Tenir compte du bruit pour le choix des "
         "appareils/matériaux et le positionnement des salles (RC)."),
        ("Lumière",
         "<i>Il faut</i> favoriser l'alternance jour/nuit. Intensité modulable (RC). "
         "Favoriser les écrans de veille des moniteurs/ventilateurs. Chambres et locaux de "
         "travail bénéficiant de lumière naturelle (législation)."),
        ("Personnalisation de la chambre",
         "<i>Il faut</i> une chambre particulière (intimité, confidentialité, "
         "participation des familles). <i>Il est possible</i> que l'affichage de photos du "
         "patient influence positivement les soignants. Espaces de rangement à la vue du "
         "patient. Heure et date visibles (RC)."),
        ("Organisation des soins",
         "<i>Il faut</i> organiser les soins pour diminuer les sources d'inconfort et "
         "adapter les procédures à l'état clinique/souhaits du patient. Rechercher les "
         "causes du manque de sommeil (RC). Contention physique tolérée seulement si "
         "sécurité en jeu, prescrite quotidiennement (HAS), minimale, ne se substituant "
         "pas aux mesures d'apaisement (RC). <i>Il faut</i> favoriser l'informatisation "
         "des services (enregistrement automatique des paramètres)."),
        ("Famille",
         "Sous réserve des soins et de la volonté du patient, <i>il faut</i> une présence "
         "des proches sans restriction d'horaires. Présence des enfants facilitée et "
         "encadrée — droit reconnu (charte de l'enfant hospitalisé). Liberté d'accès sans "
         "risque septique ni perte de qualité des soins démontrés. Pas de protection "
         "vestimentaire systématique justifiée scientifiquement. Accès aux représentants "
         "du culte à favoriser."),
    ], TCW, head=("Thème", "Recommandations")))
    return story

def _section_barrieres_environnement():
    story = _section_barrieres()
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_environnement())
    return story

# ---------------------------------------------------------------------------
def _section_soins():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Q3. Quels soins permettent le « mieux vivre » ?"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(theme_table([
        ("Intimité",
         "Rideaux/moyens d'isolement visuel et pancartes signalétiques utilisables pour "
         "améliorer l'intimité — souhait majeur des patients et familles."),
        ("Kinésithérapie et réhabilitation précoce",
         "Mobilisation possible et sûre dès les premiers jours, associée à une "
         "stimulation des gestes de la vie quotidienne (accélère le retour à la marche, "
         "raccourcit ventilation/séjour, diminue les états confusionnels). <i>Il faut</i> "
         "mettre en place un programme de réhabilitation précoce, suivant les "
         "recommandations SKR-SRLF."),
        ("Massages",
         "<i>Il est possible</i> d'utiliser les massages (dos, pieds) à visée anxiolytique "
         "et antalgique, en particulier après chirurgie majeure."),
        ("Musique",
         "<i>Il est possible</i> de faire écouter de la musique pour diminuer l'anxiété "
         "(20-30 min, calme/relaxante par défaut, écouteurs individuels, choix laissé au "
         "patient). Bénéfice à long terme non étudié."),
        ("Hydratation",
         "La soif est une plainte très fréquente (opioïdes, respiration bouche ouverte). "
         "Hors contre-indication absolue, <i>il faut probablement</i> dépister et traiter "
         "la soif par liquides clairs."),
        ("Anxiété et dépression",
         "Prévenues/améliorées surtout par les mesures non pharmacologiques. Fortes doses "
         "de benzodiazépines (BZD) nuisent au sommeil et favorisent l'ESPT. <i>Il est "
         "possible</i> de diminuer les doses de BZD sédatives sans majorer "
         "anxiété/ESPT. Avis spécialisé prudent pour les antidépresseurs (non évalués en "
         "réanimation) ; <i>il est possible</i> d'utiliser de faibles doses de BZD si un "
         "traitement anxiolytique est nécessaire."),
        ("Douleur et agitation",
         "<i>Il faut</i> dépister systématiquement douleur et agitation et les traiter, "
         "sans retard pharmacologique. Scores d'agitation/douleur (ex. Behaviour Pain "
         "Score) et de delirium (RASS, CAM-ICU) utiles pour guider et limiter les doses "
         "de neuroleptiques. <i>Il faut probablement</i> dépister conjointement douleur et "
         "agitation par des scores spécifiques. Aspirations trachéales systématiques sans "
         "avantage vs guidées par la clinique — <i>il faut probablement</i> éviter les "
         "aspirations systématiques."),
        ("Soins centrés sur la famille",
         "Présence accrue des familles possible, souhaitable et bénéfique ; participation "
         "possible à certains soins (massages, soins oculaires, repositionnements, "
         "distractions) — politique de service à définir. <i>Il faut probablement</i> "
         "impliquer les familles dans certains soins, notamment en pédiatrie (programmes "
         "NIDCAP et COPE : réduisent durée d'hospitalisation, stress parental et risque "
         "dépressif ultérieur de l'enfant)."),
    ], TCW, head=("Thème", "Recommandations")))
    return story

# ---------------------------------------------------------------------------
def _section_communication():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Q4. Quelles stratégies de communication ?"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(theme_table([
        ("Soignants-patient",
         "Contact verbal permanent, y compris chez le patient sédaté ; éviter le « on » et "
         "le tutoiement (RC) ; découvrir la personnalité du patient (RC). Outils adaptés : "
         "lecture labiale, questions oui/non en entonnoir, pictogrammes, alphabet, "
         "assistance à la parole (trachéotomie). <i>Il est possible</i> de mettre en place "
         "un journal de bord (patient + famille), qui pourrait prévenir dépression/"
         "anxiété."),
        ("Soignants-famille",
         "Entretiens structurés précoces et réguliers, dans un lieu d'accueil dédié, par "
         "le médecin en présence de l'infirmier(e), durée suffisante. Livret d'accueil "
         "remis au premier entretien. Identifier la personne de confiance/référente et "
         "les directives anticipées. Information claire, loyale, accessible ; transcrite "
         "au dossier. Avertir lors d'événements inhabituels et de la sortie. Interprète "
         "et durée d'entretien allongée pour les familles non francophones. Annonce d'une "
         "mauvaise nouvelle = entretien structuré. <i>Il faut</i> que le médecin soit "
         "disponible pour permettre un temps d'information adéquat. Aide spirituelle si "
         "besoin ; psychologue si déni de réalité (RC)."),
        ("Entre soignants",
         "Dossier de soins = outil de communication (transmissions ciblées). <i>Il est "
         "possible</i> d'établir une fiche de liaison journalière. <i>Il faut</i> repérer "
         "le syndrome d'épuisement professionnel (50 % médecins, 30 % infirmiers) ; sa "
         "prévention repose sur le respect mutuel et l'écoute (RC). Groupes de parole "
         "(RC) et réunions de service organisées."),
        ("Famille-patient",
         "Aide à la communication à proposer aux familles ; communication par le toucher "
         "en l'absence de verbal ; peau à peau chez le nourrisson. <i>Il est possible</i> "
         "de proposer aux proches de participer aux soins (oculaires, bouche, hydratation "
         "des lèvres, toilette), avec formation et accord du patient."),
        ("Sortie du patient",
         "Moment difficile pouvant induire abandon/insécurité — un livret expliquant le "
         "service d'accueil peut améliorer le vécu des proches."),
    ], TCW, head=("Axe", "Recommandations")))
    return story

def _section_soins_communication():
    story = _section_soins()
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_communication())
    return story

# ---------------------------------------------------------------------------
def _section_decisionnel():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Q5. Comment personnaliser un processus décisionnel ?"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(theme_table([
        ("Cadre général",
         "Processus décisionnel = procédures diagnostiques, traitements, recherche "
         "clinique, limitations thérapeutiques, fin de vie, don d'organes — décisions non "
         "figées, actualisées selon l'évolution. Décisions prises dans l'intérêt du "
         "patient, tenant compte de sa volonté (code de santé publique)."),
        ("Le patient",
         "Compétence rarement présente en réanimation (pas de score validé). Diversité "
         "socioculturelle à prendre en compte. Directives anticipées et personne de "
         "confiance à respecter (loi du 22 avril 2005). Pour le mineur/majeur protégé : "
         "consentement du représentant légal, mais information/écoute/participation de "
         "l'enfant adaptées à son degré de maturité."),
        ("Les proches",
         "Personne référente identifiée en l'absence de personne de confiance désignée — "
         "qualité/aptitude à vérifier. L'estimation par les proches de la qualité de vie "
         "du patient diverge souvent de celle du patient lui-même. <i>Il faut</i> "
         "accompagner les proches (support d'information à l'admission) et respecter un "
         "éventuel refus de participer aux décisions."),
        ("Équipe et autres acteurs",
         "Démarche collégiale impliquant l'équipe médicale et soignante. Médecin traitant "
         ": connaissance des préférences du patient, peut être la personne de confiance. "
         "Spécialistes consultants, psychologue, représentants du culte, acteurs "
         "sociaux/bénévoles sollicitables en cas d'échec du consensus."),
        ("Modèle décisionnel",
         "Passage d'un modèle paternaliste à un processus partagé entre équipe médicale "
         "et patient/représentants, aboutissant à une décision consensuelle sous la "
         "responsabilité du médecin. <i>Il est possible</i> qu'un accompagnement pas à "
         "pas des proches améliore leur participation et leur compétence."),
        ("Étapes de personnalisation",
         "(1) En l'absence de directives, ne pas retarder une suppléance vitale. (2) "
         "Apprécier la compétence et rechercher les préférences du patient (loi, RC). (3) "
         "Patient compétent : informé, décision libre respectée. (4) Patient incompétent "
         ": concertation équipe-personne de confiance/autorité parentale/référent/"
         "proches (avis consultatif). (5) Mineur : concertation avec l'autorité "
         "parentale, consentement du mineur recherché s'il peut l'exprimer. (6) La "
         "participation d'un proche au processus augmente le risque de stress "
         "post-traumatique — facteurs prédictifs à rechercher, prise en charge à "
         "favoriser. (7) Maintenir un « espace d'autonomie » pour les soins de confort "
         "même en cas d'incompétence partielle (ex. choix du moment d'un soin)."),
    ], TCW, head=("Volet", "Recommandations")))
    return story

# ---------------------------------------------------------------------------
def _section_sources():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("Sources et avertissement"))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "SFAR/SRLF, « Mieux vivre la Réanimation », 6e Conférence de Consensus (texte long "
        "novembre 2009), organisée selon la méthodologie de l'ANAES, avec la participation "
        "du GFRUP et de l'Adarpef, Ann Fr Anesth Réanim 29 (2010) 321-330. 175 références "
        "bibliographiques dans le texte intégral (non reproduites ici).", S_SOURCE))
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Avertissement — document de 2009/2010 :</b> cette fiche est une synthèse "
        "indépendante, produite pour un usage d'aide-mémoire. Elle condense la partie "
        "descriptive/épidémiologique du texte source (Question 1) mais reprend "
        "l'intégralité des recommandations actionnables des Questions 2 à 5. Elle ne "
        "remplace pas le texte intégral et n'est ni éditée ni validée par la SFAR/SRLF. Le "
        "cadre légal (directives anticipées, personne de confiance) ayant évolué depuis "
        "2009 (notamment la loi Claeys-Leonetti de 2016), se référer aux textes "
        "réglementaires actualisés et à un avis spécialisé avant toute décision.",
        S_BODY_SM), bg=GREY_LIGHT, border=GREY))
    return story

# ---------------------------------------------------------------------------
def _section_all():
    story = _section_intro()
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_barrieres_environnement())
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_soins_communication())
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_decisionnel())
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_sources())
    return story

SECTIONS = [
    ("Méthodologie, Q1-5 (barrières, environnement, soins, communication, "
     "décision) & sources", _section_all),
]

def _make_doc(path=None):
    return SimpleDocTemplate(path or OUT, pagesize=A4,
                              leftMargin=MARGIN, rightMargin=MARGIN,
                              topMargin=32 * mm, bottomMargin=16 * mm,
                              title="Fiche SFAR/SRLF 2010 - Mieux vivre la reanimation",
                              author="Synthèse indépendante (source SFAR/SRLF)")

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
