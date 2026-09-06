# -*- coding: utf-8 -*-
"""
Fiche de synthese - SFAR, Reference d'experts - texte court 2004
"Antibiotherapie probabiliste des etats septiques graves". Coordonnateur : B. Veber
(Rouen). En collaboration avec la Societe de reanimation de langue francaise, la Societe
de pathologie infectieuse de langue francaise, la Societe de microbiologie, la Medecine
militaire, la Societe francaise de medecine d'urgence et la Societe francaise
de pediatrie. Publie Ann Fr Anesth Reanim 23 (2004) 1020-1026. Source : sources/
antibiotherapie_probabiliste.pdf (7 pages), sources/antibiotherapie_probabiliste.txt.
Aucun tampon d'obsolescence sur la page 1 source ; statut "en vigueur" dans
build/library_final.json au 2026-09-06.

METHODOLOGIE - PAS DE COTATION PAR RECOMMANDATION : le texte imprime en Tableau 1 une
grille generale "Niveaux de preuve en medecine factuelle" (I a V, methodologie des
conferences d'experts) mais - verifie par lecture exhaustive du corps du texte - AUCUNE
des propositions d'antibiotherapie des sections 4.1 a 4.12 (ni les paragraphes de
contexte des sections 2/3/5) ne porte de renvoi explicite a l'un de ces niveaux. Il ne
s'agit donc pas d'un document GRADE ni d'un document cote item par item comme
fiche_corticotherapie.py (qui, lui, imprime un code entre crochets a cote de chaque
phrase) : ce texte court presente le tableau des niveaux de preuve comme cadre
methodologique general de la conference, puis des "Propositions d'antibiotherapie
probabiliste" en listes a puces non taguees. Disclosure faite dans le panneau
d'introduction plutot que de fabriquer un chip GRADE ou un niveau de preuve invente pour
chaque ligne (aucun grade_chip() utilise dans ce script - le grep de securite CLAUDE.md
sur '"[12][+-]/[12][+-]' ne peut donc pas matcher).

STRUCTURE DU CORPS (100% du texte, aucune section omise) : 1. Introduction (generalites
antibiotherapie probabiliste) ; 2. Specificite chez l'immunodeprime ; 3. Specificite
pediatrique ; 4. Quelle antibiotherapie probabiliste ? - 12 sous-sections par site
infectieux (4.1 meningites communautaires, 4.2 meningites nosocomiales/abces cerebraux
postoperatoires, 4.3 pneumopathies communautaires, 4.4 pneumopathies nosocomiales/PAVM,
4.5 infections urinaires communautaires et nosocomiales, 4.6 infections intra-
abdominales communautaires et nosocomiales, 4.7 pancreatites, 4.8 angiocholites aigues,
4.9 infections cutanees/tissus mous - gangrenes et cellulites, 4.10 endocardites, 4.11
infection sur catheter, 4.12 sepsis sans porte d'entree suspectee) ; 5. Reevaluation
imperative de l'antibiotherapie initiale probabiliste ; Tableau final (page 7 source) -
posologies de premiere injection des principaux antibiotiques prescrits, reproduit
integralement en tableau structure (9 familles/groupes, 24 molecules).

Posologies reproduites verbatim (aucun arrondi, aucune conversion) ; abreviations du
texte source conservees telles quelles quand deja explicitees par la source elle-meme
entre parentheses (« Cg + (pneumo) » = cocci Gram positif = pneumocoque ; « Bg + » =
bacille Gram positif ; « Bg - » = bacille Gram negatif ; « Cg - » = cocci Gram negatif).
Ligatures de l'extraction PDF (ﬂ/ﬁ) corrigees en texte normal (fl/fi) lors de la
retranscription.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from style import *
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.units import mm

OUT = os.path.join(os.path.dirname(__file__), "..", "output",
                    "Fiche_SFAR_Antibiotherapie_Probabiliste_2004.pdf")
OUT = os.path.abspath(OUT)

SOURCE_TXT = ("Source : SFAR — Référentiels, Conférence d'experts, texte court 2004 « Antibiothérapie "
              "probabiliste des états septiques graves » — Ann Fr Anesth Reanim 23 (2004) 1020-1026, "
              "coord. B. Veber. Fiche de synthèse non officielle : se référer au texte intégral.")


def P(txt, style=S_CELL):
    return Paragraph(txt, style)


def scenario_table(rows, col_widths, header=("Situation clinique", "Antibiothérapie probabiliste proposée")):
    """rows: (situation, texte) — pas de colonne de cotation : ce document n'attribue
    aucun niveau de preuve/grade aux propositions individuelles (voir docstring)."""
    data = [[P(header[0], S_HEAD_W), P(header[1], S_HEAD_W)]]
    for situation, txt in rows:
        data.append([P(situation, S_CELL_B), P(txt, S_CELL)])
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


def posology_table():
    header = ("Famille", "Antibiotique (DCI)", "Posologie 1ère injection", "Voie")
    rows = [
        ("Bêtalactamines", "Amoxicilline", "2 g", "IVL"),
        ("", "Amoxicilline + acide clavulanique", "2 g", "IVL"),
        ("", "Oxacilline", "1 g", "IVL"),
        ("", "Ticarcilline", "5 g", "IVL"),
        ("", "Pipéracilline", "4 g", "IVL"),
        ("", "Pipéracilline + tazobactam", "4 g", "IVL"),
        ("C3G", "Céfotaxime", "2 g", "IVL"),
        ("", "Ceftriaxone", "2 g", "IVL"),
        ("", "Ceftazidime", "2 g", "IVL"),
        ("", "Céfépime", "2 g", "IVL"),
        ("Carbapénème", "Imipénème", "1 g", "IVL"),
        ("Aminosides", "Gentamicine", "5 mg/kg", "Perf. 30 min"),
        ("", "Nétilmicine", "5 mg/kg", "Perf. 30 min"),
        ("", "Amikacine", "20 mg/kg", "Perf. 30 min"),
        ("", "Tobramycine", "5 mg/kg", "Perf. 30 min"),
        ("Glycopeptides", "Vancomycine", "15 mg/kg", "Perf. 1 h"),
        ("Divers anti-staph.", "Rifampicine", "10 mg/kg", "Perf. – p.o."),
        ("", "Fosfomycine", "4 g", "Perf."),
        ("Fluoroquinolones", "Ofloxacine", "400 mg", "IVL – p.o."),
        ("", "Ciprofloxacine", "400 mg ou 800 mg *", "IVL ou p.o."),
        ("", "Lévofloxacine", "500 mg", "IVL"),
        ("Macrolides", "Érythromycine", "1 g", "IVL"),
        ("", "Spiramycine", "3 MU", "IVL"),
        ("Imidazolés", "Métronidazole", "500 mg", "Perf. 30 min"),
    ]
    content_w = PAGE_W - 2 * MARGIN
    col_widths = [32 * mm, 46 * mm, 30 * mm, content_w - 32 * mm - 46 * mm - 30 * mm]
    data = [[P(h, S_HEAD_W) for h in header]]
    for fam, mol, dose, voie in rows:
        data.append([P(fam, S_CELL_B), P(mol, S_CELL), P(dose, S_CELL), P(voie, S_CELL)])
    t = Table(data, colWidths=col_widths, repeatRows=1)
    style_cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), TEAL_DARK), ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTNAME", (0, 0), (-1, 0), FONT_BOLD), ("FONTSIZE", (0, 0), (-1, 0), 8),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("GRID", (0, 0), (-1, -1), 0.5, GREY_LIGHT),
        ("TOPPADDING", (0, 0), (-1, -1), 2.0), ("BOTTOMPADDING", (0, 0), (-1, -1), 2.0),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
    ]
    # Shade one row out of two per family group (family col merges visually via blank cells).
    for i in range(1, len(data)):
        if i % 2 == 0:
            style_cmds.append(("BACKGROUND", (0, i), (-1, i), BG_PANEL))
    t.setStyle(TableStyle(style_cmds))
    return t


TOTAL_PAGES = {"n": 6}


def on_page(canvas, doc, page_title):
    header_band(canvas, doc, "SFAR — CONFÉRENCE D'EXPERTS, TEXTE COURT 2004 — FICHE DE SYNTHÈSE",
                "Antibiothérapie probabiliste des états septiques graves",
                page_title, icon_fn=lambda c, x, y: icon_pill(c, x, y, 13 * mm), color=TEAL_DARK)
    footer_band(canvas, doc, SOURCE_TXT, f"Page {doc.page} / {TOTAL_PAGES['n']}")


# ---------------------------------------------------------------------------
def _section_intro():
    story = [Spacer(1, 3 * mm)]
    story.append(info_panel(P(
        "<b>Champ :</b> stratégies d'antibiothérapie <b>probabiliste</b> (prescription avant "
        "documentation microbiologique) des états septiques graves, par site infectieux. "
        "Référentiel SFAR, Conférence d'experts, texte court 2004 (travail réalisé de 2001 à "
        "2003), coordonnateur B. Veber (Rouen), en collaboration avec la Société de réanimation "
        "de langue française, la Société de pathologie infectieuse de langue française, la "
        "Société de microbiologie, la Médecine militaire, la Société française de "
        "médecine d'urgence et la Société française de pédiatrie."
        "<br/><br/>"
        "<b>Méthodologie et disclosure :</b> le texte présente un tableau général des "
        "« niveaux de preuve en médecine factuelle » (I à V, méthodologie des conférences "
        "d'experts — reproduit ci-dessous). <b>Vérifié par lecture exhaustive du corps du "
        "texte : aucune des propositions d'antibiothérapie (sections 4.1 à 4.12) ni aucun des "
        "paragraphes de contexte ne porte de renvoi explicite à l'un de ces niveaux.</b> Ce "
        "n'est donc pas un document coté item par item (à la différence, par exemple, de la "
        "conférence de consensus « Corticothérapie » de la même année) : les propositions sont "
        "reproduites ci-après telles qu'imprimées, sans cotation associée — aucun niveau n'est "
        "inventé pour combler cette absence.", S_BODY), bg=BG_PANEL, border=TEAL))
    story.append(Spacer(1, 2 * mm))
    story.append(section_bar("Niveaux de preuve en médecine factuelle (cadre méthodologique général)"))
    story.append(Spacer(1, 2 * mm))
    content_w = PAGE_W - 2 * MARGIN
    niv_rows = [
        ("Niveau I", "Études aléatoires avec un faible risque de faux positifs (α) et de faux "
                     "négatifs (β) (puissance élevée : β = 5 à 10 %)"),
        ("Niveau II", "Risque α élevé, ou faible puissance"),
        ("Niveau III", "Études non aléatoires. Sujets « contrôlés » contemporains"),
        ("Niveau IV", "Études non aléatoires. Sujets « contrôlés » non contemporains"),
        ("Niveau V", "Études de cas. Avis d'experts"),
    ]
    data = [[P("Niveau", S_HEAD_W), P("Définition", S_HEAD_W)]]
    for n, d in niv_rows:
        data.append([P(n, S_CELL_B), P(d, S_CELL)])
    t = Table(data, colWidths=[24 * mm, content_w - 24 * mm], repeatRows=1)
    st = [("BACKGROUND", (0, 0), (-1, 0), GREY), ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
          ("FONTNAME", (0, 0), (-1, 0), FONT_BOLD), ("FONTSIZE", (0, 0), (-1, 0), 8),
          ("VALIGN", (0, 0), (-1, -1), "TOP"), ("GRID", (0, 0), (-1, -1), 0.5, GREY_LIGHT),
          ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
          ("LEFTPADDING", (0, 0), (-1, -1), 5)]
    for i in range(1, len(data)):
        if i % 2 == 0:
            st.append(("BACKGROUND", (0, i), (-1, i), BG_PANEL))
    t.setStyle(TableStyle(st))
    story.append(t)
    story.append(Spacer(1, 3 * mm))

    story.append(section_bar("1. Introduction"))
    story.append(Spacer(1, 2 * mm))
    story.append(P(
        "L'antibiothérapie « probabiliste » est une prescription réalisée avant que ne soient "
        "connues la nature et/ou la sensibilité du ou des micro-organismes responsables — ce "
        "n'est pas une antibiothérapie « à l'aveugle » mais une prescription raisonnée prenant "
        "en compte tous les éléments disponibles. L'hypothèse microbiologique est facilitée par "
        "les données épidémiologiques pour les infections communautaires ; pour les infections "
        "nosocomiales, la grande diversité des pathogènes et leur variabilité de sensibilité "
        "imposent une documentation la plus exhaustive possible de l'agent causal avant tout "
        "traitement. L'examen microscopique direct (Gram, May-Grünwald-Giemsa, Ziehl…) donne "
        "rapidement des résultats importants pour la prise en charge diagnostique, mais doit "
        "toujours être confronté secondairement aux résultats des cultures.", S_BODY))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "La prescription répond aux règles de bonnes pratiques de toute antibiothérapie : "
        "prise en compte des paramètres pharmacocinétiques/pharmacodynamiques des classes "
        "prescrites (efficacité temps-dépendante des bêtalactamines → administrations répétées "
        "voire perfusion continue ; efficacité concentration-dépendante des aminosides → dose "
        "unique quotidienne dans la majorité des situations). L'adéquation de l'antibiothérapie "
        "probabiliste initiale vis-à-vis du ou des germes responsables a démontré son impact sur "
        "le pronostic vital en sepsis grave (bactériémies, péritonites, pneumopathies — la "
        "précocité du traitement y a un impact favorable démontré). La décision finale résulte "
        "de la synthèse du pari microbiologique (site infecté, terrain, caractère nosocomial ou "
        "communautaire), de l'écologie bactérienne locale, de la flore colonisante du patient et "
        "des données de l'examen direct.", S_BODY))
    story.append(Spacer(1, 3 * mm))

    story.append(section_bar("2. Spécificité chez l'immunodéprimé", color=GREY))
    story.append(Spacer(1, 2 * mm))
    story.append(P(
        "La prise en charge des infections chez l'immunodéprimé est individualisée en raison de "
        "leur fréquence, de leur lourde mortalité en cas de retard thérapeutique, de la "
        "difficulté d'obtenir un diagnostic microbiologique et des données pharmacocinétiques "
        "particulières (notamment chez les neutropéniques). L'indication d'une antibiothérapie "
        "urgente concerne essentiellement les sepsis sévères du sujet neutropénique ou "
        "splénectomisé : dans ces deux situations, le pronostic vital peut être mis "
        "immédiatement en jeu en cas de retard à la mise en route d'une antibiothérapie "
        "probabiliste lors d'un épisode hyperthermique d'étiologie bactérienne. Au cours des "
        "autres déficits immunitaires (notamment de l'immunité cellulaire), les agents "
        "infectieux sont multiples, les tableaux cliniques variés, et les causes de fièvre ne "
        "sont pas toujours d'origine infectieuse.", S_BODY))
    story.append(Spacer(1, 3 * mm))

    story.append(section_bar("3. Spécificité pédiatrique", color=GREY))
    story.append(Spacer(1, 2 * mm))
    story.append(P(
        "L'évolution d'un processus infectieux sévère est souvent plus rapide que chez l'adulte, "
        "avec un risque précoce d'insuffisance circulatoire : l'administration urgente d'une "
        "antibiothérapie probabiliste est essentielle. La prescription tient compte de la "
        "variation des paramètres pharmacocinétiques selon l'âge (avant 6 mois : volume de "
        "distribution augmenté, demi-vie allongée ; de 6 à 12 mois ces valeurs s'abaissent ; de "
        "5 à 6 ans, caractéristiques proches de l'adulte jeune). Les posologies rapportées au "
        "poids sont proportionnellement plus élevées que chez l'adulte, mais chez le grand "
        "enfant/l'obèse elles ne doivent pas dépasser celles de l'adulte. Une association "
        "d'antibiotiques peut être justifiée dans les sepsis sévères, l'adjonction d'un "
        "aminoside étant le choix le plus fréquent — prescription prudente compte tenu de la "
        "sensibilité de l'enfant à l'oto/néphrotoxicité de ces molécules. Les fluoroquinolones "
        "sont contre-indiquées pendant la croissance (risque toxique sur le cartilage de "
        "conjugaison).", S_BODY))
    return story


def _section_meningites():
    content_w = PAGE_W - 2 * MARGIN
    cw = [40 * mm, content_w - 40 * mm]
    story = [Spacer(1, 1.5 * mm)]
    story.append(section_bar("4. Quelle antibiothérapie probabiliste ? — 4.1 Méningites communautaires"))
    story.append(Spacer(1, 2 * mm))
    story.append(P(
        "Signes de gravité imposant l'hospitalisation en réanimation : état de choc (purpura "
        "fulminans), signes de localisation, troubles graves de la conscience (Glasgow &lt; 8). "
        "En cas de purpura fulminans, le traitement (céfotaxime ou ceftriaxone) est instauré le "
        "plus précocement possible, avant même la ponction lombaire (PL). En cas de signes de "
        "localisation, l'antibiothérapie est débutée avant la TDM cérébrale qui précède la PL. "
        "En cas de méningite comateuse, la PL est réalisée avant l'antibiothérapie. L'examen "
        "direct du LCR doit être pris en compte pour le choix de l'antibiothérapie probabiliste.",
        S_BODY))
    story.append(Spacer(1, 2 * mm))
    story.append(scenario_table([
        ("Purpura fulminans", "C3G (céfotaxime ou ceftriaxone) IV immédiat."),
        ("Signes neurologiques de localisation",
         "C3G + vancomycine, puis TDM cérébrale et PL."),
        ("Examen direct du LCR positif — Cg + (pneumocoque)",
         "C3G + vancomycine (40 à 60 mg/kg/jour)."),
        ("Examen direct du LCR positif — Cg – (méningocoque)", "C3G ou amoxicilline."),
        ("Examen direct du LCR positif — Bg + (listéria)",
         "Amoxicilline (200 mg/kg/jour) + gentamicine (3 à 5 mg/kg/jour)."),
        ("Examen direct du LCR positif — Bg – (Haemophilus influenzae)",
         "C3G (céfotaxime 200 à 300 mg/kg/jour)."),
        ("Examen direct négatif — liquide trouble (PNN), glycorachie basse",
         "C3G + vancomycine."),
        ("Examen direct négatif — LCR clair lymphocytaire, glycorachie basse",
         "Amoxicilline + gentamicine + antibiothérapie antituberculeuse."),
        ("Examen direct négatif — LCR lymphocytaire, glycorachie normale", "Aciclovir."),
    ], cw))
    return story


def _section_meningites_noso():
    content_w = PAGE_W - 2 * MARGIN
    cw = [40 * mm, content_w - 40 * mm]
    story = [Spacer(1, 3 * mm)]
    story.append(section_bar("4.2 Méningites nosocomiales et abcès cérébraux postopératoires"))
    story.append(Spacer(1, 2 * mm))
    story.append(P(
        "Infections méningées iatrogéniques ou traumatiques, pathologies graves de fréquence "
        "croissante, en général consécutives à une intervention neurochirurgicale, un "
        "traumatisme du système nerveux central, la mise en place d'une dérivation du LCR et "
        "plus exceptionnellement une anesthésie péridurale ou une PL. Diagnostic souvent "
        "difficile (faible spécificité des signes) ; la documentation bactériologique par "
        "culture du LCR est indispensable. Germes les plus fréquents dans les méningites "
        "iatrogènes : staphylocoques (dont S. epidermidis) et bacilles à Gram négatif (dont "
        "entérobactéries et P. aeruginosa). Le pneumocoque est en première ligne des méningites "
        "post-traumatiques.", S_BODY))
    story.append(Spacer(1, 2 * mm))
    story.append(scenario_table([
        ("Méningites postopératoires",
         "Examen bactériologique du LCR systématique avant toute antibiothérapie. Céfotaxime + "
         "fosfomycine en première intention ; selon la bactérie suspectée : ceftazidime, "
         "imipénème, fluoroquinolones ou vancomycine."),
        ("Méningites post-traumatiques", "Amoxicilline."),
    ], cw))
    return story


def _section_pneumopathies():
    content_w = PAGE_W - 2 * MARGIN
    cw = [40 * mm, content_w - 40 * mm]
    story = [Spacer(1, 1.5 * mm)]
    story.append(section_bar("4.3 Pneumopathies communautaires"))
    story.append(Spacer(1, 2 * mm))
    story.append(P(
        "La conférence de consensus sur les pneumopathies communautaires permet de recommander "
        "le schéma thérapeutique suivant : association d'antibiotiques par voie intraveineuse.",
        S_BODY))
    story.append(Spacer(1, 2 * mm))
    story.append(scenario_table([
        ("Schéma standard",
         "Amoxicilline–acide clavulanique (2 g/8 h) ou céfotaxime (2 g/8 h) ou ceftriaxone "
         "(2 g/jour) + érythromycine (1 g/8 h) ou ofloxacine (200 mg × 2) ou lévofloxacine "
         "(500 mg × 2)."),
        ("Allergie prouvée aux pénicillines et aux C3G", "Glycopeptide + ofloxacine."),
        ("Risque de P. aeruginosa (antibiothérapie fréquente, DDB, corticothérapie au long "
         "cours)", "Bêtalactamine antipseudomonas + ciprofloxacine (400 mg/8 h)."),
    ], cw))
    story.append(Spacer(1, 3 * mm))

    story.append(section_bar("4.4 Pneumopathies nosocomiales (PAVM)"))
    story.append(Spacer(1, 2 * mm))
    story.append(P(
        "Une antibiothérapie précoce adéquate diminue la mortalité des pneumonies acquises sous "
        "ventilation mécanique. Le traitement probabiliste doit débuter rapidement, après des "
        "prélèvements bactériologiques fiables pour adaptation ultérieure indispensable. Les "
        "schémas doivent intégrer l'écologie microbienne locale, le profil de sensibilité des "
        "bactéries nosocomiales du service, le type de recrutement, une épidémie éventuelle et "
        "la colonisation/infection antérieure à des bactéries multirésistantes (BMR), ainsi que "
        "la durée d'hospitalisation et de ventilation mécanique antérieures et les "
        "antibiothérapies antérieures. Devant une pneumonie nosocomiale tardive sévère, "
        "l'antibiothérapie doit être à large spectre pour ne pas faire d'impasse "
        "microbiologique, en tenant compte des facteurs de risque de BMR. La désescalade "
        "thérapeutique secondaire, guidée par l'antibiogramme des prélèvements fiables, est "
        "indispensable.", S_BODY))
    story.append(Spacer(1, 2 * mm))
    story.append(scenario_table([
        ("PAVM précoce (&lt; 7 jours de ventilation), sans antibiothérapie ni hospitalisation "
         "antérieure dans un service à risque",
         "Bêtalactamine sans activité anti-P. aeruginosa en monothérapie : céfotaxime ou "
         "ceftriaxone ou amoxicilline–acide clavulanique."),
        ("PAVM tardive (≥ 7 jours), ou précoce avec antibiothérapie préalable ou hospitalisation "
         "antérieure dans un service à risque",
         "Bêtalactamine à activité anti-P. aeruginosa + amikacine ou ciprofloxacine ; associer "
         "la vancomycine s'il existe des facteurs de risque de SDMR ; prendre en compte "
         "legionella si facteurs de risque et/ou antigènes urinaires positifs. Retour à "
         "l'antibiothérapie la plus simple efficace dès que possible, sur prélèvements fiables "
         "réalisés avant tout traitement et antibiogramme dès que la culture est positive."),
    ], cw))
    return story


def _section_urinaire_abdo_pancreatite():
    content_w = PAGE_W - 2 * MARGIN
    cw = [40 * mm, content_w - 40 * mm]
    story = [Spacer(1, 1.5 * mm)]
    story.append(section_bar("4.5 Infections urinaires communautaires et nosocomiales"))
    story.append(Spacer(1, 2 * mm))
    story.append(P(
        "Les infections urinaires (IU) parenchymateuses (pyélonéphrites, prostatites) peuvent "
        "être responsables d'un syndrome septique grave où les signes urinaires sont très "
        "rarement au premier plan. Diagnostic : ECBU, hémocultures (15 à 20 % positives), "
        "imagerie (échographie, TDM). Les entérobactéries (E. coli +++) sont de très loin les "
        "bactéries les plus souvent isolées ; les cocci à Gram positif sont retrouvés surtout "
        "après 50 ans et dans les IU nosocomiales. Le caractère nosocomial et/ou des "
        "antibiothérapies antérieures augmentent le risque de bactérie résistante (Pseudomonas "
        "sp, Enterobacter sp, Serratia sp, Citrobacter sp, cocci à Gram négatif, Candida sp).",
        S_BODY))
    story.append(Spacer(1, 2 * mm))
    story.append(scenario_table([
        ("IU communautaires",
         "Fluoroquinolones (ofloxacine ou ciprofloxacine) ou C3G (céfotaxime ou ceftriaxone). "
         "Bithérapie dans les formes graves avec hypotension : C3G + fluoroquinolones ou "
         "aminoside (nétilmicine ou gentamicine) ; ou fluoroquinolones + aminoside en cas "
         "d'allergie aux bêtalactamines. Pendant la grossesse, les fluoroquinolones sont "
         "contre-indiquées : amoxicilline–acide clavulanique + aminoside (surtout si "
         "entérocoque suspecté)."),
        ("IU nosocomiales",
         "Discussion au cas par cas selon la colonisation du patient, l'écologie du service et "
         "l'examen direct de l'ECBU. Chez l'homme, en cas d'infection prostatique, privilégier "
         "les molécules à forte diffusion prostatique : fluoroquinolones ou cotrimoxazole."),
    ], cw))
    story.append(Spacer(1, 3 * mm))

    story.append(section_bar("4.6 Infections intra-abdominales communautaires et nosocomiales"))
    story.append(Spacer(1, 2 * mm))
    story.append(P(
        "Péritonites, angiocholites, angiocholites post-CPRE, infection du liquide d'ascite, "
        "pancréatite. Différents schémas selon le caractère communautaire ou nosocomial ; le "
        "traitement médical est toujours associé au traitement chirurgical quand il est "
        "réalisable.", S_BODY))
    story.append(Spacer(1, 2 * mm))
    story.append(scenario_table([
        ("Péritonites communautaires",
         "Amoxicilline–acide clavulanique (2 g × 3/jour) + aminoside (gentamicine ou "
         "nétilmicine 5 mg/kg) ; ou ticarcilline–acide clavulanique (5 g × 3/jour) + "
         "aminoside ; ou céfotaxime/ceftriaxone + aminoside. Entérocoque : rôle pathogène "
         "reconnu, pas de consensus pour le traitement."),
        ("Péritonites nosocomiales et postopératoires",
         "Pipéracilline–tazobactam (4,5 g × 4/jour) + amikacine (20 mg/kg × 1/jour) ; ou "
         "imipénème (1 g × 3/jour) + amikacine (20 mg/kg) ; ± vancomycine (15 mg/kg) si SAMR "
         "ou entérocoque résistant à l'amoxicilline ; ± fluconazole (800 mg/jour)."),
        ("Péritonites primaires du cirrhotique",
         "Amoxicilline–acide clavulanique (1,2 g/6 h) ou céfotaxime (2 g/8 h) ou ceftriaxone "
         "(2 g/jour)."),
    ], cw))
    story.append(Spacer(1, 3 * mm))

    story.append(section_bar("4.7 Pancréatites"))
    story.append(Spacer(1, 2 * mm))
    story.append(P(
        "Stratégie proposée par la conférence de consensus de 2001. Pas d'indication à une "
        "antibioprophylaxie (cf. consensus 2001). L'antibiothérapie est débutée après "
        "ponctions sous TDM ou prélèvements peropératoires, devant la survenue d'un état "
        "septique. La faible diffusion des antibiotiques dans la nécrose pancréatique impose "
        "de tenir compte des données pharmacocinétiques disponibles pour guider le choix.",
        S_BODY))
    story.append(Spacer(1, 2 * mm))
    story.append(scenario_table([
        ("Sans antibiothérapie préalable",
         "Imipénème, ou fluoroquinolones, ou association céfotaxime + métronidazole."),
        ("Antibiothérapie préalable, hospitalisation prolongée, manœuvres endoscopiques ou "
         "nécrosectomie antérieure",
         "Association imipénème + vancomycine + fluconazole."),
    ], cw))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "Antibiothérapie adaptée secondairement à l'antibiogramme des bactéries retrouvées "
        "dans les prélèvements peropératoires ou par ponction percutanée.", S_NOTE))
    return story


def _section_angiocholite_cutane():
    content_w = PAGE_W - 2 * MARGIN
    cw = [40 * mm, content_w - 40 * mm]
    story = [Spacer(1, 1.5 * mm)]
    story.append(section_bar("4.8 Angiocholites aiguës"))
    story.append(Spacer(1, 2 * mm))
    story.append(scenario_table([
        ("Angiocholite aiguë communautaire",
         "Amoxicilline–acide clavulanique + gentamicine ou nétilmicine ; ou "
         "ticarcilline–acide clavulanique ; ou pipéracilline + métronidazole ; ou céfoxitine ; "
         "ou céfotaxime/ceftriaxone + métronidazole. Si signes de gravité : associer "
         "gentamicine ou nétilmicine."),
        ("Angiocholite nosocomiale ou post-CPRE (facteur de risque identifié d'infection à "
         "entérocoque)",
         "Pipéracilline–tazobactam + amikacine ; ou imipénème + amikacine ; ou ceftazidime + "
         "métronidazole + amikacine."),
    ], cw))
    story.append(Spacer(1, 3 * mm))

    story.append(section_bar("4.9 Infections cutanées et des tissus mous — gangrène et cellulite"))
    story.append(Spacer(1, 2 * mm))
    story.append(P(
        "La conférence de consensus française de janvier 2000 sur l'érysipèle et les fasciites "
        "nécrosantes guide la stratégie. Les formes nécrosantes (dermohypodermites "
        "bactériennes nécrosantes/DHBN et fasciites nécrosantes/FN) diffèrent par la "
        "profondeur de l'atteinte, mais compromettent toutes deux le pronostic fonctionnel et "
        "vital — véritables urgences médicochirurgicales. Dans 40 à 80 % des cas, toutes "
        "localisations confondues, une flore mixte est retrouvée (anaérobies, entérobactéries, "
        "streptocoques, entérocoques, S. aureus) ; Streptococcus pyogenes est retrouvé dans "
        "près de la moitié des prélèvements et 50 % des hémocultures des patients en choc "
        "septique. Le traitement antibiotique n'est qu'un adjuvant du traitement chirurgical, "
        "qui repose sur des excisions larges et reste la priorité absolue. L'oxygénothérapie "
        "hyperbare n'a pas montré d'efficacité de façon méthodologiquement satisfaisante ; le "
        "retard diagnostique et l'attentisme chirurgical sous couvert antibiotique expliquent "
        "une partie des évolutions défavorables.", S_BODY))
    story.append(Spacer(1, 2 * mm))
    story.append(scenario_table([
        ("Atteinte des membres et de la région cervicofaciale",
         "Amoxicilline–acide clavulanique (2 g × 3/jour) + gentamicine ou nétilmicine "
         "(5 mg/kg/jour)."),
        ("Gangrène périnéale communautaire",
         "Céfotaxime/ceftriaxone + métronidazole, ou amoxicilline–acide clavulanique, associés "
         "à gentamicine ou nétilmicine."),
        ("Gangrène postopératoire",
         "Pipéracilline–tazobactam (16 g/jour) ou imipénème (1 g × 3/jour) + amikacine "
         "(20 mg/kg/jour)."),
    ], cw))
    return story


def _section_endocardite_catheter_sepsis():
    content_w = PAGE_W - 2 * MARGIN
    cw = [40 * mm, content_w - 40 * mm]
    story = [Spacer(1, 1.5 * mm)]
    story.append(section_bar("4.10 Endocardites"))
    story.append(Spacer(1, 2 * mm))
    story.append(P(
        "Élément essentiel de la prise en charge des endocardites infectieuses (EI) et des "
        "infections sur prothèse vasculaire (IPV). Extrême urgence : rares formes d'EI "
        "subaiguës avec sepsis grave ou insuffisance cardiaque, EI aiguës, IPV avec menace de "
        "rupture ou sepsis grave. Les EI sur valve native sont majoritairement acquises en "
        "ville ; les EI sur valves prothétiques et les IPV sont fréquemment dues à des germes "
        "hospitaliers, le risque étant d'autant plus élevé que l'infection se révèle "
        "précocement après l'intervention. Pour les prothèses de localisation intra-"
        "abdominale, le spectre doit être élargi aux germes anaérobies intestinaux. Toute "
        "documentation de l'infection implique une réévaluation de ces schémas dès que "
        "possible.", S_BODY))
    story.append(Spacer(1, 2 * mm))
    story.append(scenario_table([
        ("Valve native — suspicion de staphylocoque communautaire",
         "Cloxacilline (2 g/4 h) + gentamicine (1,5 mg/kg/12 h) ou nétilmicine "
         "(3 mg/kg/12 h)."),
        ("Valve native — sans élément d'orientation",
         "Amoxicilline–acide clavulanique (2 g/4 h) + gentamicine (1,5 mg/kg/12 h) ou "
         "nétilmicine (3 mg/kg/12 h)."),
        ("Valve native — allergie vraie aux pénicillines",
         "Vancomycine (15 mg/kg/12 h) + gentamicine (1,5 mg/kg/12 h) ou nétilmicine "
         "(3 mg/kg/12 h)."),
        ("Valve prothétique, quelle que soit l'ancienneté de la chirurgie — cas général",
         "Vancomycine (15 mg/kg/12 h) + rifampicine (600 mg/12 h) + gentamicine "
         "(1,5 mg/kg/12 h) ou nétilmicine (3 mg/kg/12 h)."),
        ("Valve prothétique — si échec ou contexte particulier",
         "Vancomycine (15 mg/kg/12 h) + ceftazidime (2 g/8 h) + gentamicine (1,5 mg/kg/12 h) "
         "ou nétilmicine (3 mg/kg/12 h)."),
    ], cw))
    story.append(Spacer(1, 3 * mm))

    story.append(section_bar("4.11 Infection sur cathéter"))
    story.append(Spacer(1, 2 * mm))
    story.append(P(
        "Il s'agit quasiment toujours d'une infection nosocomiale exposant à un risque élevé "
        "d'infection par une bactérie multirésistante. Stratégie thérapeutique : l'ablation du "
        "cathéter est l'étape la plus importante du traitement — elle permet une culture "
        "quantitative du cathéter et des hémocultures après l'ablation. L'antibiothérapie "
        "probabiliste est débutée devant un état septique grave et/ou une immunodépression, ou "
        "la présence d'une prothèse vasculaire/articulaire ou d'un pace-maker ; elle doit être "
        "antistaphylococcique et anti-BGN. Un sepsis sur cathéter périphérique impose de "
        "discuter une ligature-excision de la veine en cause, notamment en présence de signes "
        "locaux importants, d'une thrombophlébite ou d'un sepsis sévère associé à des "
        "hémocultures toujours positives sous traitement adapté. L'adaptation à "
        "l'antibiogramme est impérative dès le retour de la culture du cathéter et des "
        "hémocultures.", S_BODY))
    story.append(Spacer(1, 2 * mm))
    story.append(scenario_table([
        ("Schémas proposés",
         "Vancomycine (15 mg/kg × 2) + céfépime (2 g × 2) + gentamicine ; ou vancomycine "
         "(15 mg/kg × 2) + ceftazidime + amikacine ; ou vancomycine + imipénème + amikacine."),
        ("Facteurs de risque d'infection à levures", "Discussion de l'amphotéricine B."),
    ], cw))
    story.append(Spacer(1, 3 * mm))

    story.append(section_bar("4.12 Sepsis sans porte d'entrée suspectée"))
    story.append(Spacer(1, 2 * mm))
    story.append(scenario_table([
        ("Infection communautaire",
         "C3G (céfotaxime ou ceftriaxone) + gentamicine ou nétilmicine + métronidazole."),
        ("Infection nosocomiale (y compris patients en institution ou hospitalisés dans les "
         "30 jours précédents)",
         "Imipénème ou ceftazidime ou céfépime + amikacine + vancomycine ± métronidazole "
         "(inutile si imipénème)."),
    ], cw))
    return story


def _section_reeval_posologie_sources():
    story = [Spacer(1, 1.5 * mm)]
    story.append(section_bar("5. Réévaluation impérative de l'antibiothérapie initiale probabiliste"))
    story.append(Spacer(1, 2 * mm))
    story.append(P(
        "L'objectif est de limiter l'utilisation des antibiotiques aux seules situations qui la "
        "justifient et de faire un choix raisonné permettant une efficacité optimale tout en "
        "induisant l'impact le plus faible possible sur l'écologie hospitalière et la flore "
        "barrière des patients. La discussion du bien-fondé d'une association et le retour, "
        "lorsque c'est possible, à une molécule plus simple et/ou de spectre plus étroit "
        "s'intègrent dans les recommandations pour le bon usage des antibiotiques à l'hôpital. "
        "Il est sûrement plus délétère de laisser de façon prolongée une antibiothérapie "
        "empirique que de débuter de façon raisonnée et documentée une antibiothérapie "
        "probabiliste même à spectre large, puis de la simplifier secondairement après "
        "réévaluation. La maîtrise de l'accroissement des résistances bactériennes impose "
        "cette stratégie de réévaluation, afin d'adapter au mieux le traitement en termes de "
        "spectre à la bactérie responsable.", S_BODY))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "Cette réévaluation doit intervenir entre le 2<sup>e</sup> et le 3<sup>e</sup> jour, "
        "date à laquelle l'identification des bactéries responsables et leur profil de "
        "sensibilité sont le plus souvent disponibles, à condition d'avoir effectué "
        "initialement les prélèvements bactériologiques adéquats. Il faut parfois savoir "
        "décider d'un arrêt de l'antibiothérapie probabiliste quand l'ensemble des données "
        "microbiologiques est négatif, et orienter la recherche diagnostique vers une "
        "étiologie non infectieuse. Une deuxième réévaluation doit être effectuée vers le "
        "10<sup>e</sup> jour pour apprécier l'efficacité du traitement entrepris et juger de la "
        "nécessité éventuelle de le poursuivre — une réévaluation régulière est alors "
        "justifiée. Le coût du traitement, sans être un critère prépondérant, doit être "
        "intégré dans la discussion, à efficacité équivalente.", S_BODY))
    story.append(Spacer(1, 4 * mm))

    story.append(section_bar("Principaux antibiotiques prescrits — posologie de la première injection"))
    story.append(Spacer(1, 2 * mm))
    story.append(posology_table())
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "Posologies proposées uniquement chez l'adulte, dans la majorité des situations de "
        "sepsis grave. * Ciprofloxacine 800 mg en cas de suspicion de P. aeruginosa.", S_NOTE))
    story.append(Spacer(1, 4 * mm))

    story.append(section_bar("Sources et traçabilité", color=GREY))
    story.append(Spacer(1, 2 * mm))
    story.append(P(
        "<b>Document source :</b> SFAR — Référentiels, Conférence d'experts, texte court 2004 "
        "« Antibiothérapie probabiliste des états septiques graves », coordonnateur B. Veber "
        "(Rouen), experts C. Martin, P. Montravers, A. Lepape, R. Gauzit, J.-C. Granry, "
        "L. Dube, J.-L. Pourriat, J.-P. Bedos, J.-P. Sollet, M. Wolf, F. Caron, O. Lortholary, "
        "V. Noel, J.-L. Mainardi, J.-M. Saïssy, G. Potel, E. Grimpel. Travail réalisé sur deux "
        "ans (2001–2003), en collaboration avec la Société de réanimation de langue française, "
        "la Société de pathologie infectieuse de langue française, la Société de microbiologie, "
        "la Médecine militaire, la Société française de médecine d'urgence et la "
        "Société française de pédiatrie. Publié in Annales Françaises d'Anesthésie et de "
        "Réanimation 23 (2004) 1020-1026.", S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>Méthodologie :</b> conférence d'experts (recherche bibliographique + synthèse par "
        "un groupe d'experts, validée en séances plénières). Le tableau des niveaux de preuve "
        "(I à V) définit le cadre méthodologique général mais n'est explicitement rattaché à "
        "aucune proposition individuelle du corps du texte (voir disclosure page 1).",
        S_SOURCE))
    story.append(P(
        "<b>URL source :</b> https://sfar.org/antibiotherapie-probabiliste-des-etats-septiques-graves/",
        S_SOURCE))
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Avertissement :</b> ce document est une fiche de synthèse indépendante, produite "
        "pour un usage d'aide-mémoire. Il reprend l'intégralité des sections et propositions "
        "de la conférence d'experts 2004, mais ne remplace pas le texte intégral (argumentaire "
        "complet, références bibliographiques) et n'est ni édité ni validé par la SFAR. "
        "Conférence de 2004 : l'écologie bactérienne, les résistances et les recommandations "
        "d'antibiothérapie évoluent — se référer en complément aux données locales "
        "d'écologie/résistance actualisées, aux référentiels ultérieurs (dont la RFE "
        "« Antibioprophylaxie en chirurgie et médecine interventionnelle » 2018/2023 déjà "
        "disponible sur ce site pour la prophylaxie chirurgicale) et à un avis spécialisé "
        "(infectiologie/réanimation) en cas de doute.",
        S_BODY_SM), bg=GREY_LIGHT, border=GREY))
    return story


def _section_1():
    # Merged intro+méningites+pneumopathies+infections urinaires/intra-abdominales into one
    # continuous section: kept separate, each half left a large blank tail before its forced
    # PageBreak (méningites nosocomiales ends ~15% down page 3; pneumopathies+urinaire ended
    # similarly) - see CLAUDE.md step 7 (pages <60% full -> merge adjacent sections, rebuild,
    # check the ACTUAL page count; reverted if it doesn't help - this merge measured shorter).
    return (_section_intro() + [Spacer(1, 3 * mm)] + _section_meningites()
            + [Spacer(1, 1 * mm)] + _section_meningites_noso()
            + [Spacer(1, 3 * mm)] + _section_pneumopathies()
            + [Spacer(1, 3 * mm)] + _section_urinaire_abdo_pancreatite())


def _section_2():
    # Merged with endocardites/cathéter/sepsis AND with the réévaluation/posologie/sources
    # tail (angiocholites+cutané alone left ~45% of its last page blank, and the reeval
    # section alone left ~80% of its last page blank after the posology table).
    return (_section_angiocholite_cutane() + [Spacer(1, 3 * mm)] + _section_endocardite_catheter_sepsis()
            + [Spacer(1, 3 * mm)] + _section_reeval_posologie_sources())


SECTIONS = [
    ("Introduction, méningites, pneumopathies, urinaires & intra-abdominales", _section_1),
    ("Angiocholites, cutané, endocardites, cathéter, sepsis & posologies", _section_2),
]


def _make_doc(path=None):
    return SimpleDocTemplate(path or OUT, pagesize=A4,
                              leftMargin=MARGIN, rightMargin=MARGIN,
                              topMargin=32 * mm, bottomMargin=16 * mm,
                              title="Fiche SFAR 2004 - Antibiothérapie probabiliste des états septiques graves",
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
    # Throwaway measurement builds must NEVER write to OUT (see CLAUDE.md) - always use a
    # fresh tempfile.mktemp() path for these measurement passes.
    import pypdf, tempfile
    tmp_path = tempfile.mktemp(suffix=".pdf")
    doc = _make_doc(tmp_path)
    doc.build(story_flowables, onFirstPage=_silent_page, onLaterPages=_silent_page)
    with open(tmp_path, "rb") as f:
        n = len(pypdf.PdfReader(f).pages)
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
