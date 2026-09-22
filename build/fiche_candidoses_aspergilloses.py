# -*- coding: utf-8 -*-
"""
Fiche de synthese - SFAR / SPILF / SRLF, Conference de Consensus commune,
13 mai 2004 (Paris, Institut Pasteur), avec la participation de la Societe
Francaise d'Hematologie, de la Societe Francaise de Mycologie Medicale et de
la Societe Francaise de Greffe de Moelle. "Prise en charge des candidoses et
aspergilloses invasives de l'adulte" - texte "RESUME", 8 pages, telecharge
depuis sfar.org (wp-content/uploads/2015/10/2_SFAR_Prise-en-charge-des-
candidoses-et-aspergilloses-invasives-de-ladulte.pdf).

METHODOLOGIE : le texte source cote certaines affirmations avec un code
lettre+chiffre (A1, A2, B2, B3, C3, et une occurrence de "A" seul, sans
chiffre) place entre parentheses juste apres la phrase concernee. AUCUNE
legende / page de definition de ce systeme de cotation n'existe dans ce
document "RESUME" (le tableau des niveaux de preuve figure vraisemblablement
dans le texte long de la conference, non disponible ici - verifie par lecture
integrale du texte extrait : aucune occurrence de "niveau de preuve",
"grade A" defini, ou equivalent). Ceci est un vrai trou de documentation de la
source, pas une incoherence a trancher : disclosure explicite dans le panneau
methodologie de la fiche (jamais d'invention de signification pour le
chiffre). Convention VISUELLE de cette fiche, et uniquement pour faciliter la
lecture : le code est colore selon sa lettre initiale (A = vert, B = bleu-
sarcelle, C = ambre), par coherence avec le systeme Grade A/B/C deja utilise
ailleurs dans ce corpus - mais le code complet (lettre+chiffre) est TOUJOURS
affiche tel quel entre crochets, jamais reduit a la seule lettre. Les
affirmations narratives non suivies d'un code entre crochets ne sont PAS
cotees dans le texte source (le cas le plus notable : la duree de traitement
de la candidose hepato-splenique, question 3 / 1.2.2, n'a aucun code alors
que la phrase precedente et la suivante, sur les memes schemas, sont cotees -
disclosure explicite dans le corps du texte a cet endroit precis).

Une phrase du texte source combine DEUX cotations distinctes sur deux
clauses differentes (l'itraconazole en allogreffe de CSH, question 4 / 2.1) -
"L'itraconazole peut aussi etre prescrit dans l'allogreffe de CSH (A1).
Cependant, sa difficulte d'utilisation justifie de restreindre sa
prescription a certaines situations a risque : corticotherapie prolongee
post-allogreffe de CSH (C3)." Ceci est scinde ici en DEUX affirmations
distinctes, chacune avec son propre code - jamais fusionnees en un chip
composite, conformement a la regle du corpus (grep de securite
'"[12][+-]/[12][+-]' execute avant build, aucune correspondance).

COUVERTURE : integrale des 5 questions du texte "RESUME" (diagnostic/suivi ;
moyens therapeutiques disponibles - spectre d'activite et voies d'admin-
istration/effets indesirables reproduits verbatim depuis un rendu 200dpi des
pages 3-4, aucune n'ayant de couche texte structuree fiable ; strategie des
candidoses systemiques - y compris les DEUX arbres decisionnels de la
question 3/1.1, retranscrits en tableaux Situation/Conduite depuis un rendu
200dpi de la page 5, logique de branchement verifiee exhaustivement ;
chimio-prophylaxie ; strategie des aspergilloses invasives) + le colophon
jury/comite d'organisation (page 8). Rien n'est omis.

CORRECTION POST-AUDIT (branchement de l'Arbre 1, question 3/1.1.1) : un
audit independant (subagent aveugle au brouillon) a signale une erreur sur
la ligne "Creat < 1,5N - non-neutropenique - traitement anterieur par
azole" d'ARBRE1_ROWS, initialement transcrite vers le bloc Cancidas/
Ambisome. Re-verification manuelle a un zoom tres eleve (900dpi, crop cible
sur les seules fleches OUI/NON de cette question) : l'audit avait LUI AUSSI
mal lu ce croisement de fleches (il proposait de fusionner cette ligne avec
la ligne "sans traitement anterieur", ce qui est egalement faux). Lecture
definitive, confirmee par la coherence clinique de l'ensemble de l'arbre 1
(cf. les deux flowables OUI/NON de "NEUTROPENIQUE ... nephrotoxiques ?" et
de "NON-NEUTROPENIQUE ... azole ?" convergent en X : OUI(nephrotoxiques) va
au bloc Cancidas/Ambisome, NON(nephrotoxiques) et OUI(azole anterieur)
convergent tous deux vers "Fungizone IV 1 mg/kg/j" seul, et NON(azole
anterieur) seul va vers "Fungizone OU Triflucan") : la ligne corrigee cible
donc "Fungizone IV 1 mg/kg/j" (monotherapie, pas de Triflucan propose en
cas d'exposition azolee anterieure - coherent avec le reste de l'arbre, qui
retire systematiquement le Triflucan de la liste des options des qu'un
antecedent d'exposition aux azoles existe). Toutes les 6 autres lignes des
deux arbres, deja verifiees par l'audit, restent inchangees.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from style import *
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.units import mm

OUT = "/home/user/rfe-sfar-website/output/Fiche_SFAR_SPILF_SRLF_Candidoses_Aspergilloses_2004.pdf"

SOURCE_TXT = ("Source : « Prise en charge des candidoses et aspergilloses invasives de "
              "l'adulte » — Conférence de Consensus commune, SFAR / SPILF / SRLF, 13 mai "
              "2004. Fiche de synthèse non officielle : se référer au texte intégral.")

def P(txt, style=S_CELL):
    return Paragraph(txt, style)

CW_FULL = PAGE_W - 2 * MARGIN

def _tagcolor(code):
    c0 = code[0]
    return {"A": "#2d8a56", "B": "#0e7c85", "C": "#c8790c"}.get(c0, "#6b7980")

def tag(code):
    """Inline coloured bracket citation for the source's own lettre+chiffre code
    (e.g. [A1], [B3]) - see METHODOLOGIE docstring above for why this is a chip
    Table nor a fabricated legend."""
    return ' <font color="%s"><b>[%s]</b></font>' % (_tagcolor(code), code)

def theme_table(rows, col_widths, head=("Thème", "Détail")):
    """rows: (theme, detail) - pas de gradation dans les cellules elles-memes."""
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

TCW = [56 * mm, CW_FULL - 56 * mm]

def grid_table(head, rows, col_widths, small=False):
    """Generic multi-column data table (used for the two Question-2 antifungal
    tables, reproduced verbatim from a 200dpi render - see docstring)."""
    st_cell = S_BODY_SM if small else S_CELL
    st_head = S_HEAD_W_C
    data = [[P(h, st_head) for h in head]]
    for row in rows:
        data.append([P(str(cell), st_cell) if i == 0 else P(str(cell), S_CELL_C)
                     for i, cell in enumerate(row)])
    t = Table(data, colWidths=col_widths, repeatRows=1)
    style_cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), NAVY), ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTNAME", (0, 0), (-1, 0), FONT_BOLD), ("FONTSIZE", (0, 0), (-1, 0), 7.6),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("ALIGN", (1, 1), (-1, -1), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 0.5, GREY_LIGHT),
        ("TOPPADDING", (0, 0), (-1, -1), 2.6), ("BOTTOMPADDING", (0, 0), (-1, -1), 2.6),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            style_cmds.append(("BACKGROUND", (0, i), (-1, i), BG_PANEL))
    t.setStyle(TableStyle(style_cmds))
    return t

def bullets(items, style=S_BODY_SM):
    html = "&bull; " + "<br/>&bull; ".join(items)
    return P(html, style)

TOTAL_PAGES = {"n": 5}

def on_page(canvas, doc, page_title):
    header_band(canvas, doc, "SFAR / SPILF / SRLF — CONFÉRENCE DE CONSENSUS 2004",
                "Candidoses et aspergilloses invasives de l'adulte",
                page_title, icon_fn=lambda c, x, y: icon_pill(c, x, y, 13 * mm), color=TEAL_DARK)
    footer_band(canvas, doc, SOURCE_TXT, f"Page {doc.page} / {TOTAL_PAGES['n']}")

# ---------------------------------------------------------------------------
def _section_intro():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Champ :</b> prise en charge diagnostique, thérapeutique et prophylactique des "
        "candidoses invasives (CI) et aspergilloses invasives (AI) de l'adulte — patients "
        "d'hématologie, de réanimation et immunodéprimés. Conférence de Consensus commune "
        "SFAR / SPILF / SRLF, avec la participation de la Société Française d'Hématologie, "
        "de la Société Française de Mycologie Médicale et de la Société Française de Greffe "
        "de Mœlle, 13 mai 2004 (Paris, Institut Pasteur). 5 questions.", S_BODY),
        bg=BG_PANEL, border=TEAL))
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Méthodologie — disclosure :</b> le texte source cote certaines affirmations par "
        "un code lettre+chiffre entre parenthèses" + tag("A1") + tag("B3") + tag("C3") +
        " — mais ce document « Résumé » n'en publie <b>aucune légende</b> (le tableau des "
        "niveaux de preuve figure vraisemblablement dans le texte long de la conférence, "
        "non disponible ici). Convention <i>visuelle</i> propre à cette fiche, pour faciliter "
        "la lecture uniquement : le code est coloré selon sa lettre initiale (A = vert, "
        "B = bleu-sarcelle, C = ambre), par cohérence avec le système Grade A/B/C déjà "
        "utilisé ailleurs dans ce corpus — mais <b>aucune signification n'est prêtée au "
        "chiffre</b>, qui reste non défini par la source ; le code complet est toujours "
        "affiché tel quel. Une affirmation sans code entre crochets n'est simplement pas "
        "cotée dans le texte source.", S_BODY_SM), bg=AMBER_LIGHT, border=AMBER))
    return story

def _section_q1():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Question 1 — Diagnostic et suivi des candidoses et aspergilloses "
                    "invasives (CI et AI)"),
        Spacer(1, 1.5 * mm),
        P("La recherche de levures et de champignons filamenteux doit être systématique "
          "chez les patients à risque. Seuls les prélèvements tissulaires ou de sites "
          "normalement stériles sont spécifiques. L'examen direct est crucial — il oriente "
          "le diagnostic et restera parfois le seul argument biologique — donc systématique "
          "et réalisé rapidement avec des techniques spécifiques. L'examen histologique des "
          "tissus permet d'apprécier le caractère invasif de l'infection.", S_BODY),
    ]))
    story.append(Spacer(1, 1.8 * mm))
    story.append(P(
        "La présence de <i>Candida sp.</i> dans les sécrétions des voies aériennes "
        "inférieures (y compris le lavage broncho-alvéolaire) n'a pas de valeur "
        "diagnostique" + tag("B3") + ". La présence d'<i>Aspergillus sp.</i> est à "
        "interpréter en fonction du risque de colonisation bronchique et du degré "
        "d'immunodépression ; elle est prédictive d'aspergillose pulmonaire invasive (API) "
        "chez le patient d'hématologie" + tag("B2") + ".", S_BODY))
    story.append(Spacer(1, 1.8 * mm))
    story.append(P(
        "Les hémocultures sont positives dans seulement 50 % des CI, mais la positivité "
        "d'une seule suffit au diagnostic. Sauf exception, la présence d'<i>Aspergillus "
        "sp.</i> en hémoculture correspond à une contamination.", S_BODY))
    story.append(Spacer(1, 1.8 * mm))
    story.append(P(
        "Culture : milieu de référence = Sabouraud, incubé à 30 °C pendant 21 jours, même "
        "si <i>Candida sp.</i> et <i>Aspergillus sp.</i> se développent le plus souvent sur "
        "les milieux usuels de bactériologie. L'identification au niveau de l'espèce doit "
        "être réalisée pour tous les champignons ; certaines méthodes permettent un gain de "
        "24 à 72 heures dans le diagnostic d'espèce pour les levures.", S_BODY))
    story.append(Spacer(1, 1.8 * mm))
    story.append(P(
        "En hématologie, l'antigénémie aspergillaire par technique ELISA est un examen "
        "sensible lorsqu'il est répété, et spécifique s'il est confirmé par un deuxième "
        "prélèvement à 24-48 heures" + tag("A1") + ". Des faux positifs ont été rapportés "
        "(galactomannanes d'origine alimentaire ou médicamenteuse). L'antigénémie précède "
        "souvent les signes radiologiques et la mise en évidence du champignon ; sa valeur "
        "prédictive de l'efficacité du traitement reste à préciser. Hors hématologie, la "
        "valeur diagnostique de l'antigénémie aspergillaire est moins bien précisée. La "
        "recherche couplée d'anticorps circulants et d'antigènes candidosiques (ELISA) "
        "serait évocatrice de CI, mais son intérêt doit être confirmé. Les techniques de "
        "biologie moléculaire pour la détection/identification ne sont pas standardisées et "
        "non disponibles en routine.", S_BODY))
    story.append(Spacer(1, 1.8 * mm))
    story.append(P(
        "Le choix de l'antifongique repose avant tout sur la connaissance de l'épidémiologie "
        "locale et/ou de l'espèce isolée. La méthode Etest®, réalisable en routine, est la "
        "seule actuellement corrélée à la méthode de référence NCCLS" + tag("B2") +
        " — elle permet de déterminer les concentrations minimales inhibitrices (CMI), pour "
        "<i>Candida sp.</i>, du fluconazole, de l'itraconazole et de la flucytosine ; pour "
        "<i>Aspergillus sp.</i>, l'intérêt de la détermination des CMI n'est pas confirmé.",
        S_BODY))
    story.append(Spacer(1, 1.8 * mm))
    story.append(P(
        "<b>Imagerie de l'API :</b> la radiographie de thorax standard est peu sensible et "
        "peu spécifique. La TDM thoracique en haute résolution est l'examen à réaliser "
        "précocement. Chez le patient d'hématologie en aplasie post-chimiothérapie, le signe "
        "du halo — précoce mais transitoire — est très évocateur ; hors cette population, il "
        "est moins spécifique. L'injection de produit de contraste précise les rapports "
        "entre lésions et structures vasculaires (indication chirurgicale), guide une "
        "éventuelle ponction diagnostique, suit l'évolution et fait le bilan des lésions "
        "résiduelles en vue d'une éventuelle « chirurgie de propreté ». La TDM des sinus "
        "recherche une lyse osseuse (invasion loco-régionale). Dans l'aspergillose "
        "cérébrale, l'IRM est l'examen le plus sensible.", S_BODY_SM))
    story.append(Spacer(1, 1.8 * mm))
    story.append(P(
        "<b>Candidémies :</b> l'examen ophtalmologique est systématique. L'échographie "
        "et/ou la TDM sont utiles pour rechercher des métastases septiques, en particulier "
        "lors de la sortie d'aplasie. L'IRM semble être l'examen le plus sensible dans les "
        "candidoses hépato-spléniques.", S_BODY_SM))
    return story

def _section_intro_q1():
    story = _section_intro()
    story.append(Spacer(1, 2 * mm))
    story.extend(_section_q1())
    return story

# ---------------------------------------------------------------------------
SPECTRE_HEAD = ["Espèce", "Fungizone®", "Ancotil®", "Triflucan®", "Sporanox®", "Vfend®", "Cancidas®"]
SPECTRE_ROWS = [
    ["Candida albicans", "S", "S/R", "S", "S", "S", "S"],
    ["Candida glabrata", "S/I", "S", "SDD/R", "SDD/R", "S/ ??", "S"],
    ["Candida parapsilosis", "S", "S", "S", "S", "S", "S/ ??"],
    ["Candida tropicalis", "S", "S", "S/SDD", "S", "S", "S"],
    ["Candida krusei", "S/I", "I/R", "R", "SDD/R", "S", "S"],
    ["Candida lusitaniae", "S/R", "S", "S", "S", "S", "S"],
    ["Aspergillus fumigatus", "S", "R", "R", "S/R", "S", "S/R"],
    ["Aspergillus flavus", "S", "R", "R", "S", "S", "S"],
    ["Aspergillus terreus", "S", "R", "R", "S", "S", "S"],
]
SPECTRE_CW = [33 * mm] + [ (CW_FULL - 33 * mm) / 6.0 ] * 6

VOIES_HEAD = ["Antifongique", "Voie(s)", "Principaux effets indésirables"]
VOIES_ROWS = [
    ["Fungizone® (amphotéricine B désoxycholate, AmB)", "IV",
     "Hypokaliémie, hypomagnésémie, insuffisance rénale ; fièvre/frissons lors de "
     "l'injection ; cytopénie"],
    ["Ambisome® (AmB liposomale, ABLp) / Abelcet® (AmB lipid complex, ABLC)", "IV",
     "Mêmes complications que la Fungizone®, mais fréquence moindre ; tolérance "
     "supérieure pour l'Ambisome®"],
    ["Ancotil® (flucytosine)", "IV/PO",
     "Troubles digestifs, hématologiques et hépatiques dose-dépendants"],
    ["Sporanox®* (itraconazole)", "IV/PO",
     "Troubles digestifs, cytolyse hépatique, cholestase, réactions allergiques et "
     "cutanées ; insuffisance cardiaque congestive"],
    ["Triflucan® (fluconazole)", "IV/PO",
     "Troubles digestifs, cytolyse hépatique, cholestase, réactions allergiques et "
     "cutanées"],
    ["Vfend®* (voriconazole)", "IV/PO",
     "Troubles digestifs, cytolyse hépatique, cholestase, réactions allergiques et "
     "cutanées ; troubles visuels réversibles"],
    ["Cancidas® (caspofungine)", "IV", "Peu fréquents et bénins"],
]
VOIES_CW = [58 * mm, 14 * mm, CW_FULL - 72 * mm]

def _section_q2():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Question 2 — Moyens thérapeutiques disponibles pour les candidoses et "
                    "aspergilloses invasives"),
        Spacer(1, 1.5 * mm),
        P("Quatre familles d'antifongiques sont disponibles : les polyènes, la flucytosine, "
          "les azolés et les échinocandines.", S_BODY),
        Spacer(1, 2 * mm),
        P("<b>1 — Spectre d'activité</b> (reproduit verbatim, source page 3)", S_CELL_B),
        Spacer(1, 1 * mm),
        grid_table(SPECTRE_HEAD, SPECTRE_ROWS, SPECTRE_CW),
        Spacer(1, 1 * mm),
        P("S : sensible — SDD : sensibilité dose-dépendante — I : intermédiaire — "
          "R : résistant. « S/ ?? » et « S/R » etc. reproduisent des cellules à double "
          "valeur telles qu'imprimées dans le tableau source (deux résultats rapportés pour "
          "l'espèce/l'antifongique concerné, y compris une incertitude « ?? » non levée par "
          "la source elle-même sur 2 cellules — disclosure, non résolue ici).", S_NOTE),
    ]))
    story.append(Spacer(1, 3 * mm))
    story.append(KeepTogether([
        P("<b>Voies d'administration et effets indésirables</b> (reproduit verbatim, "
          "source page 4)", S_CELL_B),
        Spacer(1, 1 * mm),
        grid_table(VOIES_HEAD, VOIES_ROWS, VOIES_CW, small=True),
        Spacer(1, 1 * mm),
        P("* Relais oral précoce recommandé chez l'insuffisant rénal (accumulation d'un "
          "excipient toxique de la forme IV).", S_NOTE),
    ]))
    story.append(Spacer(1, 3 * mm))
    story.append(KeepTogether([
        P("<b>2 — Suivi thérapeutique</b>", S_CELL_B),
        Spacer(1, 1 * mm),
        P("Le suivi des concentrations plasmatiques à l'équilibre est pertinent pour "
          "l'itraconazole (variabilité d'absorption et de métabolisme hépatique, "
          "interactions médicamenteuses fréquentes), le voriconazole (15 à 20 % de "
          "métaboliseurs lents chez les patients d'origine asiatique, interactions "
          "médicamenteuses fréquentes) et la flucytosine (toxicité dose-dépendante).",
          S_BODY_SM),
    ]))
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        P("<b>3 — Interactions médicamenteuses</b>", S_CELL_B),
        Spacer(1, 1 * mm),
        P("La prescription d'AmB est déconseillée avec d'autres médicaments néphrotoxiques "
          "(aminosides, ciclosporine…), avec les digitaliques et les diurétiques "
          "hypokaliémiants. Le voriconazole est contre-indiqué en co-prescription avec le "
          "sirolimus et les inducteurs enzymatiques susceptibles d'en diminuer les "
          "concentrations plasmatiques (rifampicine, carbamazépine, phénobarbital). Les "
          "interactions de l'itraconazole sont proches de celles du voriconazole. Le "
          "fluconazole, l'ABLp et la caspofungine ne présentent pas d'interactions majeures "
          "à l'origine de contre-indications.", S_BODY_SM),
    ]))
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        P("<b>Aspects médico-économiques</b>", S_CELL_B),
        Spacer(1, 1 * mm),
        P("Les nouveaux antifongiques injectables sont coûteux (500 à 650 €/jour) ; si leur "
          "financement a été individualisé en 2004, il s'intègre néanmoins aux dépenses des "
          "établissements de santé. Ces surcoûts contribuent à maintenir l'emploi de l'AmB "
          "malgré ses effets indésirables.", S_BODY_SM),
    ]))
    return story

# ---------------------------------------------------------------------------
# Question 3 - decision trees (source page 5), transcribed as Situation/Conduite
# tables from a 200dpi visual render (no reliable text layer) - branching logic
# fully traced arrow-by-arrow, see module docstring.
ARBRE1_ROWS = [
    ("Créatininémie < 1,5 N — neutropénique — < 2 traitements néphrotoxiques associés",
     "Fungizone® IV 1 mg/kg/j"),
    ("Créatininémie < 1,5 N — neutropénique — ≥ 2 traitements néphrotoxiques associés",
     "Cancidas® IV (70 mg J1 puis 50 mg/j) OU Ambisome® IV 3 mg/kg/j"),
    ("Créatininémie < 1,5 N — non-neutropénique — sans traitement antérieur par azolé",
     "Fungizone® IV 1 mg/kg/j OU Triflucan® IV 12 mg/kg/j"),
    ("Créatininémie < 1,5 N — non-neutropénique — traitement antérieur par azolé",
     "Fungizone® IV 1 mg/kg/j"),
    ("Créatininémie ≥ 1,5 N — non-neutropénique — sans traitement antérieur par azolé",
     "Triflucan® IV 12 mg/kg/j"),
    ("Créatininémie ≥ 1,5 N — non-neutropénique — traitement antérieur par azolé",
     "Cancidas® IV (70 mg J1 puis 50 mg/j) OU Ambisome® IV 3 mg/kg/j"),
    ("Créatininémie ≥ 1,5 N — neutropénique (quel que soit le statut vis-à-vis des "
     "néphrotoxiques)",
     "Cancidas® IV (70 mg J1 puis 50 mg/j) OU Ambisome® IV 3 mg/kg/j"),
]

ARBRE2_ROWS = [
    ("Candida Triflucan®-sensible — neutropénique ou non",
     "Triflucan® IV 6 mg/kg/j, relais per os dès que possible"),
    ("Candida Triflucan®-résistant ou -SDD — créatininémie < 1,5 N — non-neutropénique",
     "Fungizone® IV 1 mg/kg/j"),
    ("Candida Triflucan®-résistant ou -SDD — créatininémie < 1,5 N — neutropénique — "
     "< 2 traitements néphrotoxiques associés",
     "Fungizone® IV 1 mg/kg/j"),
    ("Candida Triflucan®-résistant ou -SDD — créatininémie < 1,5 N — neutropénique — "
     "≥ 2 traitements néphrotoxiques associés",
     "Cancidas® IV 50 mg/j OU Ambisome® IV 3 mg/kg/j OU, si C. krusei, Vfend® 12 mg/kg/j "
     "(J1) puis 8 mg/kg/j"),
    ("Candida Triflucan®-résistant ou -SDD — créatininémie ≥ 1,5 N — neutropénique ou non",
     "Cancidas® IV 50 mg/j OU Ambisome® IV 3 mg/kg/j OU, si C. krusei, Vfend® 12 mg/kg/j "
     "(J1) puis 8 mg/kg/j"),
]

def _section_q3():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Question 3 — Stratégie thérapeutique des candidoses systémiques"),
        Spacer(1, 1.5 * mm),
        P("<b>1 — Choix du traitement curatif / 1.1 — Selon le genre et l'espèce</b>",
          S_CELL_B),
    ]))
    story.append(Spacer(1, 2 * mm))
    story.append(KeepTogether([
        P("<b>1.1.1 — Avant identification de l'espèce</b>" + tag("A1"), S_CELL_B),
        Spacer(1, 1 * mm),
        P("L'augmentation de l'incidence des <i>Candida sp.</i> de sensibilité diminuée ou "
          "résistants aux azolés, une neutropénie, une insuffisance rénale et les "
          "médicaments co-prescrits (néphrotoxicité, interactions) interviennent dans le "
          "choix. Arbre décisionnel du texte source, retranscrit ci-dessous en tableau "
          "Situation / Conduite :", S_BODY_SM),
    ]))
    story.append(Spacer(1, 1.5 * mm))
    story.append(theme_table(ARBRE1_ROWS, TCW, head=("Situation clinique", "Conduite")))
    story.append(Spacer(1, 3 * mm))
    story.append(KeepTogether([
        P("<b>1.1.2 — Après identification de l'espèce de <i>Candida sp.</i></b>" +
          tag("A1"), S_CELL_B),
        Spacer(1, 1 * mm),
    ]))
    story.append(theme_table(ARBRE2_ROWS, TCW, head=("Situation clinique", "Conduite")))
    story.append(Spacer(1, 1 * mm))
    story.append(P(
        "Pour toutes les situations ci-dessus hors <i>Candida</i> Triflucan®-sensible, un "
        "relais par Vfend® oral peut être effectué si l'infection paraît contrôlée "
        "(convergence des branches « Fungizone® » et « Cancidas®/Ambisome®/Vfend® » du "
        "second arbre vers ce relais, tel que dessiné dans le schéma source).", S_NOTE))
    story.append(Spacer(1, 3 * mm))
    story.append(KeepTogether([
        P("<b>1.2 — Selon les localisations</b>", S_CELL_B),
        Spacer(1, 1 * mm),
        P("<b>1.2.1 — Candidémie :</b> pas d'argument pour une association" + tag("B3") +
          " (sauf certaines localisations, cf. 1.2.3). Durée de traitement : 2 semaines "
          "après la dernière hémoculture positive et la disparition des symptômes" +
          tag("C3") + ", ou au moins 7 jours après la correction de la neutropénie. Le "
          "retrait du cathéter intravasculaire est recommandé" + tag("B3") + ".", S_BODY_SM),
        Spacer(1, 1.5 * mm),
        P("<b>1.2.2 — Candidose hépato-splénique (chronique disséminée) :</b> durée du "
          "traitement de 6 mois en moyenne <i>(affirmation non cotée dans le texte source, "
          "à la différence des phrases voisines sur le même thème — disclosure, non "
          "résolue ici)</i>.", S_BODY_SM),
        Spacer(1, 1.5 * mm),
        P("<b>1.2.3 — Autres localisations</b> (associées ou non à une candidémie) : les "
          "mêmes schémas thérapeutiques sont utilisés ; cependant l'association AmB + "
          "flucytosine est proposée dans les localisations oculaires, méningées et "
          "cardiaques" + tag("B3") + ". Les durées de traitement sont souvent plus "
          "prolongées.", S_BODY_SM),
    ]))
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        P("<b>2 — Traitement préemptif en réanimation</b>", S_CELL_B),
        Spacer(1, 1 * mm),
        P("Malgré l'absence de validation, un tableau septique préoccupant, sans autre "
          "documentation microbiologique, avec colonisation de plusieurs sites par "
          "<i>Candida sp.</i> et des facteurs de risque de CI, autorise un traitement "
          "préemptif (mêmes schémas que ci-dessus)" + tag("C3") + ".", S_BODY_SM),
    ]))
    return story

# ---------------------------------------------------------------------------
def _section_q4():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Question 4 — Chimio-prophylaxie antifongique en réanimation et en "
                    "hématologie"),
        Spacer(1, 1.5 * mm),
        P("<b>1 — En réanimation :</b> il n'y a pas d'argument en faveur de l'utilisation "
          "d'une chimioprophylaxie" + tag("A2") + ". L'absence de données suffisantes ne "
          "permet pas d'identifier les patients qui en bénéficieraient.", S_BODY),
    ]))
    story.append(Spacer(1, 2 * mm))
    story.append(P(
        "<b>2 — En hématologie :</b> l'incidence élevée et la mortalité importante "
        "(50 % à 90 %) des infections fongiques ont justifié l'évaluation extensive de la "
        "chimioprophylaxie.", S_BODY))
    story.append(Spacer(1, 1.8 * mm))
    story.append(KeepTogether([
        P("<b>2.1 — La chimio-prophylaxie primaire</b>", S_CELL_B),
        Spacer(1, 1 * mm),
        P("L'AmB par voie respiratoire ou veineuse (quelle que soit la formulation) ne "
          "réduit pas l'incidence des infections invasives. Le fluconazole (400 mg/j) est "
          "recommandé dans l'allogreffe de cellules souches hématopoïétiques (CSH) car il "
          "réduit la fréquence des CI et leur mortalité" + tag("A1") +
          " — cependant, en raison du risque de sélection de souches résistantes, 50 % des "
          "équipes européennes lui préfèrent l'utilisation des polyènes oraux. Pour les LA "
          "et autogreffes, l'incidence habituelle des CI n'a pas permis de documenter "
          "l'intérêt d'une prophylaxie, et le fluconazole n'est pas recommandé.",
          S_BODY_SM),
        Spacer(1, 1.2 * mm),
        P("L'itraconazole peut aussi être prescrit dans l'allogreffe de CSH" + tag("A1") +
          ".", S_BODY_SM),
        Spacer(1, 1 * mm),
        P("Sa difficulté d'utilisation justifie cependant de restreindre sa prescription à "
          "certaines situations à risque : corticothérapie prolongée post-allogreffe de "
          "CSH" + tag("C3") +
          " <i>(deux cotations distinctes fusionnées en une seule phrase dans le texte "
          "source, scindées ici en deux affirmations — cf. docstring du module)</i>.",
          S_BODY_SM),
        Spacer(1, 1.2 * mm),
        P("Aucune donnée n'est actuellement disponible avec le voriconazole.", S_BODY_SM),
    ]))
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        P("<b>2.2 — La chimio-prophylaxie secondaire</b>", S_CELL_B),
        Spacer(1, 1 * mm),
        P("Elle doit être systématique, utiliser une molécule active vis-à-vis du "
          "champignon précédemment isolé ou suspecté, et couvrir la période "
          "d'immunodépression" + tag("C3") + ".", S_BODY_SM),
    ]))
    return story

def _section_q5():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Question 5 — Stratégie thérapeutique des aspergilloses invasives"),
        Spacer(1, 1.5 * mm),
        P("Le mauvais pronostic de l'AI, avec une mortalité de 50 à 90 %, a été récemment "
          "amélioré grâce à la prescription précoce, dès que le diagnostic est présumé, "
          "d'antifongiques plus actifs et mieux tolérés, éventuellement associés à la "
          "chirurgie.", S_BODY),
    ]))
    story.append(Spacer(1, 2 * mm))
    story.append(KeepTogether([
        P("<b>1 — Les moyens thérapeutiques</b>", S_CELL_B),
        Spacer(1, 1 * mm),
        P("<b>Polyènes :</b> une seule étude randomisée prospective a établi la supériorité "
          "d'ABLp sur l'AmB ; les autres études démontrent la meilleure tolérance des "
          "formes lipidiques" + tag("A") + ".", S_BODY_SM),
        Spacer(1, 1 * mm),
        P("<b>Azolés :</b> le taux de réponse avec l'itraconazole (IV/PO) varie de 39 à "
          "63 % dans des essais non contrôlés et limités. Le voriconazole (IV puis per os) "
          "s'est avéré supérieur à l'AmB en termes d'efficacité, de survie et de "
          "tolérance.", S_BODY_SM),
        Spacer(1, 1 * mm),
        P("<b>Échinocandines :</b> le seul essai avec la caspofungine, encore non publié "
          "(dossier d'AMM), rapporte 45 % de réponses favorables dans les formes "
          "réfractaires.", S_BODY_SM),
        Spacer(1, 1 * mm),
        P("<b>Associations d'antifongiques :</b> leur efficacité clinique n'a pas été "
          "démontrée dans des études prospectives.", S_BODY_SM),
    ]))
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        P("<b>2 — Les stratégies du traitement curatif</b>", S_CELL_B),
        Spacer(1, 1 * mm),
        P("Les résultats de l'essai randomisé comparant AmB et voriconazole conduisent à "
          "proposer le voriconazole comme traitement de première ligne de l'AI" +
          tag("A1") + ", mais cette stratégie repose sur une seule étude de "
          "non-infériorité. Le voriconazole n'a pas été comparé aux formes lipidiques "
          "d'AmB, et l'impact de l'utilisation prolongée des triazolés à large spectre sur "
          "l'écologie fongique n'est pas évalué.", S_BODY_SM),
        Spacer(1, 1 * mm),
        P("L'ABLp (3 ou 5 mg/kg/jour) et la caspofungine sont indiqués en deuxième "
          "intention. L'itraconazole IV pourrait constituer une alternative.", S_BODY_SM),
        Spacer(1, 1 * mm),
        P("Chez les malades dont l'infection paraît contrôlée, un relais oral peut être "
          "effectué par du voriconazole ou de l'itraconazole" + tag("C3") +
          ". Le traitement doit être poursuivi jusqu'à la guérison de l'aspergillose et la "
          "disparition des facteurs prédisposants. La place des associations dans le "
          "traitement de l'aspergillose est encore inconnue ; certaines associations "
          "peuvent être potentiellement antagonistes, toxiques et coûteuses.", S_BODY_SM),
    ]))
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        P("<b>3 — Autres traitements</b>", S_CELL_B),
        Spacer(1, 1 * mm),
        P("Certaines situations peuvent imposer un geste chirurgical : en urgence pour "
          "exérèse de lésions pulmonaires au contact d'un gros vaisseau ; secondairement en "
          "cas de lésion persistante circonscrite avant un nouveau traitement aplasiant ; "
          "et, en cas de non-réponse au traitement, à visée de diagnostic mycologique "
          "formel. Aucune étude contrôlée n'a été réalisée avec l'adjonction du G-CSF.",
          S_BODY_SM),
    ]))
    story.append(Spacer(1, 4 * mm))
    story.extend(_section_sources())
    return story

def _section_sources():
    story = []
    story.append(section_bar("Sources et traçabilité", color=GREY))
    story.append(Spacer(1, 2 * mm))
    story.append(P(
        "<b>Document source :</b> « Prise en charge des candidoses et aspergilloses "
        "invasives de l'adulte » — Conférence de Consensus commune, texte « Résumé ». "
        "Société française d'anesthésie et de réanimation (SFAR), Société de Pathologie "
        "Infectieuse de Langue Française (SPILF), Société de Réanimation de Langue "
        "Française (SRLF), avec la participation de la Société Française d'Hématologie, de "
        "la Société Française de Mycologie Médicale et de la Société Française de Greffe de "
        "Mœlle.", S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>Président du jury :</b> B. Regnier (Paris). <b>Jury du consensus :</b> "
        "M. Attal (Toulouse), Y. Bézie (Paris), V. Blanc (Antibes), A. Buzyn (Paris), "
        "P. Choutet (Tours), O. Mimoz (Poitiers), L. Papazian (Marseille), G. Pialoux "
        "(Paris), T. Pottecher (Strasbourg), C. Poyart (Paris), A. Tazi (Paris), P. Tilleul "
        "(Paris).", S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>Comité d'organisation :</b> SFAR — Y. Malledant (Rennes), C. Martin "
        "(Marseille), C. Paugam (Paris) ; SPILF — G. Beaucaire (Lille), B. Dupont (Paris), "
        "O. Lortholary (Paris) ; SRLF — P. Charbonneau (Caen), R. Robert (Poitiers), "
        "M. Wolff (Paris). <b>Coordonnateurs :</b> B. Dupont (Paris), P. Charbonneau "
        "(Caen). <b>Conseillers scientifiques :</b> F. Gouin (SFAR, Marseille), P. Chavanet "
        "(SPILF, Dijon), J. Carlet (SRLF, Paris). <b>Recherche bibliographique :</b> "
        "P.E. Charles (Dijon), L. Velly (Marseille), A. Veinstein (Poitiers).", S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P("<b>Version :</b> 13 mai 2004, Paris, Institut Pasteur.", S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P("<b>Méthodologie :</b> Conférence de Consensus — cotation lettre+chiffre "
                    "(A1, A2, B2, B3, C3…) sans légende publiée dans ce document « Résumé » "
                    "— voir disclosure méthodologique en page 1.", S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>URL source :</b> https://sfar.org/wp-content/uploads/2015/10/"
        "2_SFAR_Prise-en-charge-des-candidoses-et-aspergilloses-invasives-de-ladulte.pdf",
        S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P("<b>Couverture :</b> cette fiche reprend l'intégralité des 5 questions du "
                    "texte « Résumé » (diagnostic/suivi ; moyens thérapeutiques disponibles "
                    "— tableaux spectre d'activité et voies d'administration/effets "
                    "indésirables reproduits verbatim ; stratégie des candidoses systémiques "
                    "— y compris les deux arbres décisionnels ; chimio-prophylaxie ; "
                    "stratégie des aspergilloses invasives) et le colophon jury/comité "
                    "d'organisation.", S_SOURCE))
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Avertissement — document de 2004 :</b> ce document est une fiche de synthèse "
        "indépendante, produite pour un usage d'aide-mémoire. Elle reprend l'intégralité "
        "des informations du texte source « Résumé » (les tableaux et arbres décisionnels "
        "transcrits depuis un rendu visuel du PDF, faute de couche texte fiable), mais ne "
        "remplace pas le texte intégral (argumentaire complet, texte long, références "
        "bibliographiques) et n'est ni éditée ni validée par la SFAR, la SPILF ou la SRLF. "
        "Les posologies, spectres de sensibilité et stratégies antifongiques ayant "
        "considérablement évolué depuis 2004 (nouvelles molécules, résistances émergentes, "
        "recommandations plus récentes), se référer impérativement à un avis spécialisé et "
        "aux recommandations actualisées avant toute décision thérapeutique.",
        S_BODY_SM), bg=GREY_LIGHT, border=GREY))
    return story

def _section_q3_q4_q5_sources():
    # Merged onto one page-group: Q3's tail (1.2 + traitement preemptif) left
    # most of a page white, and Q4/Q5/sources' own tail left another page
    # mostly white - combined per the <60%-full merge rule (CLAUDE.md build
    # pipeline, step 7). Re-verified after merge: no orphaned headers, better
    # fill, same total content.
    story = _section_q3()
    story.append(Spacer(1, 3 * mm))
    story.extend(_section_q4())
    story.append(Spacer(1, 3 * mm))
    story.extend(_section_q5())
    return story

SECTIONS = [
    ("Méthodologie & Q1 — Diagnostic et suivi", _section_intro_q1),
    ("Q2 — Moyens thérapeutiques disponibles", _section_q2),
    ("Q3, Q4 & Q5 — Stratégies, prophylaxie & sources", _section_q3_q4_q5_sources),
]

def _make_doc(path=None):
    return SimpleDocTemplate(path or OUT, pagesize=A4,
                              leftMargin=MARGIN, rightMargin=MARGIN,
                              topMargin=32 * mm, bottomMargin=16 * mm,
                              title="Fiche SFAR/SPILF/SRLF 2004 - Candidoses et "
                                    "aspergilloses invasives de l'adulte",
                              author="Synthèse indépendante (source SFAR/SPILF/SRLF)")

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
    # import) - use PyMuPDF (fitz) instead, per fiche_ponction_lombaire.py.
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
