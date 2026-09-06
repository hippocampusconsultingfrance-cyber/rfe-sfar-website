# -*- coding: utf-8 -*-
"""
Fiche de synthese - Revision de la 3e Conference de Consensus en Reanimation et Medecine
d'Urgence de 1988 (Societe de Reanimation de Langue Francaise, SRLF) : "Prise en charge
des crises d'asthme aigues graves de l'adulte et de l'enfant (a l'exclusion du
nourrisson)". Auteur/coordinateur : E. L'Her (Brest). Publie dans Reanimation 2002;11:1-9,
recu et accepte le 28 fevrier 2002.
Source : sources/asthme_aigu_grave.pdf (9 pages, texte integral Elsevier), extrait en
texte integral dans sources/asthme_aigu_grave.txt. Pas de tampon d'obsolescence sur la
page 1 (verifie visuellement a 140dpi, cf. build/asthme_p1_check.png) ni sur la page
sfar.org du document (grep "abroge/retire/obsolete/annule" -> aucune occurrence) -
document non marque "abroge" dans build/library_final.json ("status": "en vigueur").

CHAMP : defini explicitement des le titre - adulte ET enfant, mais EXCLUSION EXPLICITE du
nourrisson - disclosed tel quel dans le panneau d'introduction, jamais omis.

METHODOLOGIE - systeme a DEUX AXES INDEPENDANTS (Score d'evaluation / Niveau de
recommandation, page 2 de la source), plus simple que fiche_civd.py/fiche_sevrage_vm.py
(meme epoque, meme grille SRLF) car ICI LES DEUX AXES SONT TOUJOURS PROPREMENT SEPARABLES
- verifie par extraction exhaustive de tous les groupes entre parentheses courtes (regex
"\\([^)]{1,8}\\)") du texte extrait : exactement 3 formes rencontrees pour les cotations
(en excluant les renvois bibliographiques entre CROCHETS, seulement 2 occurrences "[1]"/
"[2]", clairement distincts et renvoyant a la liste "REFERENCES" en fin de texte) -
(a) "(chiffre-lettre)" ex. "(1-a)", "(2-b)", "(3-c)" - les deux axes cotes ;
(b) une lettre seule ex. "(a)", "(b)", "(c)" - Preuve seule, Force non cotee par le jury ;
(c) un chiffre seul ex. "(1)", "(2)", "(3)" - Force seule (rare, Preuve non precisee).
Aucune ambiguite du type sevrage_vm/civd (pas de renvoi bibliographique numerique nu
confondu avec une cotation) : les deux axes sont donc restitues ici dans DEUX COLONNES
SEPAREES (chip Preuve a/b/c, chip Force 1/2/3, "-" si non cote), a l'identique du
reco_table de fiche_civd.py.

Tableau I (criteres de gravite, page 3 source) et Tableau II (agonistes beta-2
disponibles, page 4 source) : DEUX vrais tableaux de donnees dans le texte source (pas
des images - texte extractible standard, verifie), reproduits ici verbatim ligne par
ligne (aucune paraphrase des seuils chiffres/posologies).

PERIMETRE DE COUVERTURE : integralite des 5 questions du texte long (gravite immediate,
voie des beta-2 mimetiques, autres therapeutiques, indications d'hospitalisation,
modalites de ventilation mecanique), du Tableau I, du Tableau II, de la conclusion et des
elements de methodologie/jury. Pas de figure/organigramme dans cette source (a la
difference de fiche_sevrage_vm.py) - uniquement les deux tableaux ci-dessus et du texte
structure par question.

AVERTISSEMENT DISCLOSED : document de 2002 (revision d'une conference de 1988) - les
pratiques ont evolue depuis (ex. usage plus large du sulfate de magnesium et de la VNI
dans les recommandations ulterieures SFMU/GINA/SPLF) ; signale explicitement dans le
panneau d'avertissement final plutot que silencieusement mis a jour.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from style import *
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.units import mm

# Local, non-invasive extension of the shared GRADE_COLORS dict (no collision with
# existing keys "1+","1-","2+","2-","AE","?" - same precedent as fiche_civd.py).
GRADE_COLORS["a"] = (GREEN, WHITE)
GRADE_COLORS["b"] = (TEAL, WHITE)
GRADE_COLORS["c"] = (AMBER, WHITE)
GRADE_COLORS["1"] = (GREEN, WHITE)
GRADE_COLORS["2"] = (TEAL, WHITE)
GRADE_COLORS["3"] = (AMBER, WHITE)

OUT = "/home/user/rfe-sfar-website/output/Fiche_SRLF_Asthme_Aigu_Grave_2002.pdf"

SOURCE_TXT = ("Source : Révision de la 3e Conférence de Consensus en Réanimation et Médecine d'Urgence "
              "de 1988 — Société de Réanimation de Langue Française (SRLF) — « Prise en charge des "
              "crises d'asthme aiguës graves de l'adulte et de l'enfant (à l'exclusion du nourrisson) », "
              "E. L'Her (Brest), Réanimation 2002;11:1-9 (reçu et accepté le 28 février 2002). Fiche de "
              "synthèse non officielle : se référer au texte intégral.")

def P(txt, style=S_CELL):
    return Paragraph(txt, style)

def chip(label, **kw):
    return grade_chip(label, **kw)

def reco_table(rows, col_widths):
    """rows: (theme, text, preuve_label_or_None, force_label_or_None) - deux axes
    toujours separables dans cette source (voir docstring du module)."""
    data = [[P("Thème", S_HEAD_W), P("Énoncé", S_HEAD_W), P("Preuve", S_HEAD_W_C), P("Force", S_HEAD_W_C)]]
    for theme, txt, preuve, force in rows:
        preuve_cell = chip(preuve) if preuve else P("—", S_CELL_C)
        force_cell = chip(force) if force else P("—", S_CELL_C)
        data.append([P(theme, S_CELL_B), P(txt, S_CELL), preuve_cell, force_cell])
    t = Table(data, colWidths=col_widths, repeatRows=1)
    style_cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), NAVY), ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTNAME", (0, 0), (-1, 0), FONT_BOLD), ("FONTSIZE", (0, 0), (-1, 0), 8),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("ALIGN", (2, 0), (3, -1), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 0.5, GREY_LIGHT),
        ("TOPPADDING", (0, 0), (-1, -1), 3.4), ("BOTTOMPADDING", (0, 0), (-1, -1), 3.4),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            style_cmds.append(("BACKGROUND", (0, i), (-1, i), BG_PANEL))
    t.setStyle(TableStyle(style_cmds))
    return t

def simple_table(header, rows, col_widths, header_color=TEAL_DARK):
    data = [[P(h, S_HEAD_W) for h in header]]
    for r in rows:
        data.append([P(c, S_CELL) for c in r])
    t = Table(data, colWidths=col_widths, repeatRows=1)
    st = [
        ("BACKGROUND", (0, 0), (-1, 0), header_color), ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTNAME", (0, 0), (-1, 0), FONT_BOLD), ("FONTSIZE", (0, 0), (-1, 0), 8),
        ("GRID", (0, 0), (-1, -1), 0.5, GREY_LIGHT), ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 3.2), ("BOTTOMPADDING", (0, 0), (-1, -1), 3.2),
        ("LEFTPADDING", (0, 0), (-1, -1), 4.5),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            st.append(("BACKGROUND", (0, i), (-1, i), BG_PANEL))
    t.setStyle(TableStyle(st))
    return t

def legend_flowable():
    chip_w = 14 * mm
    content_w = PAGE_W - 2 * MARGIN
    text_w = (content_w - 2 * chip_w) / 2.0
    row = Table([[
        chip("a-c", width=chip_w - 2 * mm),
        P("<b>Preuve</b> — niveau de preuve de la référence : a (essais prospectifs, contrôlés, "
          "randomisés) &gt; b (études non randomisées, comparaisons de cohortes) &gt; c (mises au "
          "point, revues générales, éditoriaux, séries de cas revues par des experts) &gt; d "
          "(publications d'opinion non revues, non rencontrée dans ce texte).", S_BADGE_HEAD),
        chip("1-3", width=chip_w - 2 * mm),
        P("<b>Force</b> — niveau de la recommandation, imprimé seulement quand le jury l'a jugé "
          "possible : 1 (preuves scientifiques indiscutables) &gt; 2 (preuves + consensus d'experts) "
          "&gt; 3 (pas de preuves adéquates, opinion d'experts). « — » = axe non imprimé par le jury "
          "pour cet énoncé.", S_BADGE_HEAD),
    ]], colWidths=[chip_w, text_w, chip_w, text_w])
    row.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("LEFTPADDING", (0, 0), (-1, -1), 2),
                              ("RIGHTPADDING", (0, 0), (-1, -1), 3)]))
    return row

TOTAL_PAGES = {"n": 8}

def on_page(canvas, doc, page_title):
    header_band(canvas, doc, "SRLF — RÉVISION CONFÉRENCE DE CONSENSUS 2002 — FICHE DE SYNTHÈSE",
                "Crises d'asthme aiguës graves",
                page_title, icon_fn=lambda c, x, y: icon_shield(c, x, y, 13 * mm), color=TEAL_DARK)
    footer_band(canvas, doc, SOURCE_TXT, f"Page {doc.page} / {TOTAL_PAGES['n']}")

# ---------------------------------------------------------------------------
def _section_intro():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Champ :</b> crises d'asthme aiguës graves (AAG) de l'<b>adulte</b> et de "
        "l'<b>enfant</b>, à <b>l'exclusion explicite du nourrisson</b> (précision imprimée "
        "dans le titre même de la source, reprise ici sans l'omettre). Révision de la 3<sup>e</sup> "
        "Conférence de Consensus en Réanimation et Médecine d'Urgence de 1988, organisée par la "
        "Société de Réanimation de Langue Française (SRLF). Coordinateur : E. L'Her (Brest). "
        "Publiée dans <i>Réanimation</i> 2002;11:1-9 (reçu et accepté le 28 février 2002).<br/><br/>"
        "<b>Cinq questions</b> posées au jury : (1) peut-on prévoir la gravité immédiate d'une "
        "crise d'asthme ? (2) quelle est la voie d'utilisation préférentielle des bêta-2 "
        "mimétiques et quel schéma thérapeutique ? (3) quelle est la place des autres "
        "thérapeutiques à la phase initiale ? (4) quelles sont les indications et modalités de "
        "l'hospitalisation ? (5) quelles sont les modalités de la ventilation mécanique ?",
        S_BODY), bg=BG_PANEL, border=TEAL))
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("Méthodologie & convention de cette fiche"))
    story.append(Spacer(1, 2 * mm))
    story.append(P(
        "Grille SRLF à <b>deux axes indépendants</b> : une lettre de <b>niveau de preuve</b> de la "
        "référence bibliographique et, quand le jury l'a jugé possible, un chiffre de <b>niveau de "
        "recommandation</b>, imprimés ensemble entre parenthèses (ex. « (1-a) », « (2-b) », "
        "« (3-c) ») ou, pour une partie des énoncés, sur un seul des deux axes (ex. « (a) » seul, "
        "« (3) » seul). Les deux axes sont restitués ici dans deux colonnes séparées "
        "(Preuve / Force) plutôt que fusionnés en une seule puce, aucun énoncé de cette source ne "
        "mêlant cotation et simple renvoi bibliographique (vérifié par extraction exhaustive du "
        "texte : seules 2 citations entre crochets figurent dans tout le document, renvoyant "
        "explicitement à la liste « RÉFÉRENCES » en fin de texte, jamais confondues avec une "
        "cotation).", S_BODY_SM))
    story.append(Spacer(1, 2 * mm))
    story.append(legend_flowable())
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("Incidence actuelle de l'asthme aigu grave et mortalité induite", color=GREY))
    story.append(Spacer(1, 2 * mm))
    story.append(P(
        "Données épidémiologiques rares et difficilement comparables (définition non univoque de "
        "l'AAG). Estimation à partir de la littérature : <b>50 000 à 100 000</b> hospitalisations "
        "annuelles en France pour exacerbations aiguës d'asthme, dont <b>8 000 à 16 000</b> pour "
        "AAG — chiffres <b>vraisemblablement surestimés</b> (disclosed tel quel par la source). Le "
        "nombre d'admissions en réanimation pour AAG est stable sur les dix dernières années, ainsi "
        "que le pourcentage de patients ventilés (environ <b>13 %</b> chez l'adulte). Baisse de la "
        "mortalité par AAG (concordance internationale ; en France, baisse du nombre absolu de "
        "décès malgré une population croissante). Environ <b>60 %</b> des patients décédés avaient "
        "plus de 75 ans, avec une possible surestimation de la mortalité liée à l'asthme "
        "(pathologies associées, diagnostics erronés). La majorité des décès survient <b>en dehors "
        "des services de réanimation</b>, par anoxie cérébrale pré-hospitalière ; la fréquence des "
        "décès en réanimation varie de <b>0 à 15 %</b> selon les séries.", S_BODY_SM))
    return story

def _section_tableau1():
    story = []
    story.append(Spacer(1, 2 * mm))
    story.append(section_bar("Question 1 — Peut-on prévoir la gravité immédiate d'une crise d'asthme ?"))
    story.append(Spacer(1, 2 * mm))
    story.append(P(
        "Il reste fondamental devant toute crise d'asthme d'en reconnaître la gravité — évaluation "
        "détaillée dans le texte de 1988 qui reste d'actualité (Tableau I). Actualisation limitée "
        "à quelques points (détail dans le tableau des recommandations ci-dessous, dont le devenir "
        "de la mesure du <b>pouls paradoxal</b> proposée en 1988).", S_BODY_SM))
    story.append(Spacer(1, 2 * mm))
    story.append(P("<b>Tableau I — Critères de gravité d'un AAG</b>, d'après la conférence de consensus "
                    "de 1988, adaptée à la pédiatrie (reproduit verbatim)", S_CELL_B))
    story.append(Spacer(1, 1.5 * mm))
    cw = [42 * mm, PAGE_W - 2 * MARGIN - 42 * mm]
    story.append(simple_table(["Catégorie", "Critères"], [
        ("Signes cliniques de gravité extrême", "Troubles de la conscience, pause respiratoire, "
         "collapsus, silence auscultatoire. Chez l'enfant : augmentation de la fréquence "
         "respiratoire &gt; 50 % pour l'âge."),
        ("Facteurs liés au terrain", "Asthme ancien, instable, sous-traité, déjà hospitalisé pour "
         "une crise grave ; enfant très jeune (&lt; 4 ans) et adolescents."),
        ("Facteurs liés aux faits récents (« syndrome de menace »)", "Augmentation de la fréquence "
         "et de la sévérité des crises, moindre sensibilité aux thérapeutiques usuelles, épisodes "
         "intercritiques de moins en moins « asymptomatiques ». Chez l'enfant : crises déclenchées "
         "par l'ingestion d'aliments ; troubles socio-psychologiques du patient ou de la cellule "
         "familiale."),
        ("Facteurs liés au caractère de la crise", "Crise ressentie par le malade comme inhabituelle "
         "par son évolution rapide et la présence de signes de gravité ; difficulté à parler, à "
         "tousser ; orthopnée ; agitation ; sueurs ; cyanose ; contraction permanente des "
         "sterno-cléido-mastoïdiens."),
        ("Fréquence respiratoire", "&gt; 30/min chez l'adulte et l'enfant de plus de 5 ans ; "
         "&gt; 40/min chez l'enfant de 2-5 ans."),
        ("Fréquence cardiaque", "&gt; 120 battements/min chez l'adulte. Chez l'enfant, une "
         "tachycardie, à condition qu'elle reste &lt; 200/min, n'est pas toujours un signe de "
         "gravité."),
        ("Tension artérielle chez l'enfant*", "Signe de gravité si inférieure à : 68-36 mmHg "
         "(TA syst.-diast.) à 3-5 ans ; 78-41 mmHg à 7-8 ans ; 82-44 mmHg à 10-11 ans."),
        ("Débit expiratoire de pointe (DEP)", "Chez l'adulte, toute valeur &lt; 150 L/min témoigne "
         "d'une crise grave. Chez l'enfant, un DEP &lt; 50 % de la valeur prédite ou habituelle "
         "témoigne d'une crise aiguë sévère, et &lt; 33 % d'une crise grave."),
        ("Gaz du sang", "La constatation d'une normo- ou d'une hypercapnie est un signe de gravité "
         "indiscutable."),
    ], cw))
    story.append(Spacer(1, 1 * mm))
    story.append(P("<i>* Valeurs chez le garçon ; valeur moyenne − 2 déviations standard.</i>", S_NOTE))
    return story

def _section_q1_reco():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(reco_table([
        ("Pouls paradoxal", "Mesure proposée par le texte de 1988, peu utilisée en routine en "
         "France (difficultés et erreurs de mesure sur le terrain, intérêt réel peu probable) : "
         "son recueil peut être abandonné.", "c", "3"),
        ("Facteurs de risque épidémiologiques", "Sexe masculin ; hospitalisation pour crise "
         "d'asthme durant l'année précédente ; antécédent d'intubation ; corticothérapie dans les "
         "trois mois précédents pour crise d'asthme.", "b", None),
        ("Facteurs de risque (suite)", "Tabagisme, également considéré comme facteur de risque "
         "d'AAG.", "b", None),
        ("Facteurs de risque (suite)", "Abus de sédatifs, hypnotiques, stupéfiants, également "
         "considéré comme facteur de risque d'AAG.", "c", None),
        ("Score clinique", "Il n'existe toujours pas de score clinique validé permettant de "
         "prédire la gravité d'une crise d'asthme dès l'admission.", None, None),
        ("Suivi du DEP", "Le suivi évolutif du débit expiratoire de pointe, mesuré 30 min à 2 h "
         "après un traitement initial optimal, est proposé chez les patients présentant un asthme "
         "aigu sévère.", "b", "2"),
        ("Enfant — critères de gravité", "Critères superposables à l'adulte (importance du "
         "caractère évolutif du DEP et des gaz du sang artériel), en dehors des particularités de "
         "l'examen clinique (Tableau I).", None, None),
        ("Enfant — DEP après 6 ans", "L'utilisation du DEP est indispensable chez l'enfant de plus "
         "de six ans.", None, "2"),
        ("Enfant — DEP entre 5 et 10 ans", "Mesure possible chez plus de la moitié des enfants "
         "âgés de cinq à neuf ans, et chez les trois quarts des enfants de plus de dix ans.",
         "a", None),
    ], [40 * mm, PAGE_W - 2 * MARGIN - 40 * mm - 15 * mm - 15 * mm, 15 * mm, 15 * mm]))
    return story

def _section_q2_intro():
    story = []
    story.append(Spacer(1, 2 * mm))
    story.append(section_bar("Question 2 — Voie d'utilisation préférentielle des bêta-2 mimétiques et schéma thérapeutique"))
    story.append(Spacer(1, 2 * mm))
    story.append(reco_table([
        ("Priorité du traitement", "Les bêta-2 mimétiques sont les bronchodilatateurs les plus "
         "puissants et les plus rapides, à index thérapeutique élevé : ils constituent "
         "indiscutablement la priorité du traitement de la crise d'asthme.", "a", "1"),
        ("Voie prioritaire", "La voie inhalée est prioritaire dans tous les cas, en raison de son "
         "efficacité liée à la pénétration locale et de ses effets systémiques limités.", "a", "1"),
        ("Molécules à écarter", "Les bêta-2 mimétiques d'action prolongée (formotérol, salmétérol) "
         "ainsi que les formes orales n'ont pas leur place dans le traitement de l'AAG "
         "(non coté).", None, None),
        ("Nébulisation — supériorité", "La supériorité de la nébulisation par rapport à la voie "
         "intraveineuse est établie, en termes de rapport efficacité/tolérance, dans le traitement "
         "initial de l'AAG.", "a", "1"),
        ("Nébulisation — modalités", "Utilisable quel que soit l'âge, sans nécessiter la "
         "coopération du patient ; utilisable même en cas d'obstruction bronchique majeure ou de "
         "troubles de conscience débutants.", "a", "1"),
        ("Nébulisation — posologie adulte (1<sup>re</sup> heure)", "2,5 à 7,5 mg de salbutamol, ou 5 mg de "
         "terbutaline, au masque avec 6-8 L/min d'O2, 10-15 min, répétée toutes les 20 min. "
         "Posologie licite : 3 × 5 mg/h durant la première heure.", "a", "2"),
        ("Nébulisation — posologie adulte (heures suivantes)", "Puis une nébulisation de 5 mg "
         "toutes les 3 h (ou 2,5 mg/h) pendant les six heures suivantes.", "b", "3"),
        ("Nébulisation continue vs intermittente", "Pas de différence significative entre "
         "nébulisation continue et intermittente à posologie cumulée identique. Le mélange "
         "hélium-oxygène comme gaz vecteur ne semble pas supérieur à l'oxygène seul.", "a", None),
        ("Nébulisation — enfant", "0,05 à 0,15 mg/kg (dose minimale 0,5-1,5 mg) ; doses usuelles de "
         "2,5 mg (&lt; 20 kg) et 5 mg (&gt; 20 kg). Nébulisation continue proposée en cas "
         "d'obstruction persistante malgré les nébulisations intermittentes.", "b", "2"),
        ("Aérosols doseurs seuls", "N'ont pas leur place dans cette situation, en raison d'un "
         "maniement difficile et d'une efficacité limitée par l'insuffisance de la dose délivrée.",
         "a", "1"),
        ("Aérosols doseurs + chambre d'inhalation — adulte", "Alternative intéressante à la "
         "nébulisation, sous réserve d'une utilisation adéquate du dispositif : 2 à 4 bouffées de "
         "100 µg répétées toutes les 5-10 min si besoin.", "a", "2"),
        ("Aérosols doseurs + chambre d'inhalation — enfant", "À proposer en première intention : "
         "5 à 10 bouffées de 100 µg à renouveler, sous réserve d'une utilisation adéquate du "
         "dispositif et de la coopération de l'enfant.", "a", "1"),
    ], [38 * mm, PAGE_W - 2 * MARGIN - 38 * mm - 15 * mm - 15 * mm, 15 * mm, 15 * mm]))
    return story

def _section_q2_tableau2():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(P(
        "<b>Autres modalités d'inhalation</b> (poudres, systèmes auto-déclenchés) : peu d'études "
        "réalisées, ne permettent pas de les recommander au cours de l'AAG (utilisation par le "
        "patient possiblement utile dans l'attente des secours médicalisés).<br/><br/>"
        "<b>Voie sous-cutanée :</b> place marginale dans la prise en charge des AAG par les équipes "
        "médicalisées, mais pourrait être utile en médecine de ville dans l'attente des secours "
        "<i>(3)</i>. Chez l'enfant : 10 µg/kg de terbutaline ; auto-médication par injection "
        "sous-cutanée préconisée si le début de la crise est très rapide <i>(2-c)</i>.<br/><br/>"
        "<b>Perfusion intraveineuse :</b> place difficile à définir malgré une utilisation très "
        "large en France, peu de données scientifiques la justifiant <i>(2)</i> — dans les cas "
        "rapportés comme justifiant l'IV, l'inhalation n'avait été délivrée ni de façon optimale ni "
        "à posologie adéquate. Débit continu au pousse-seringue, posologies croissantes débutant "
        "vers 0,25-0,5 mg/h de salbutamol, sans utilité au-delà de 5 mg/h <i>(2-b)</i>. Chez "
        "l'enfant : paliers de 0,2 µg/kg/min débutant à 0,5 µg/kg/min (0,1 µg/kg/min pour la "
        "terbutaline), sans utilité au-delà de 5 µg/kg/min <i>(3-c)</i>. Peu de données sur "
        "l'association IV + inhalée, mais la durée d'hospitalisation peut être écourtée par "
        "l'administration précoce de 15 µg/kg de salbutamol intraveineux <i>(2-b)</i>.",
        S_BODY_SM))
    story.append(Spacer(1, 3 * mm))
    story.append(P("<b>Tableau II — Agonistes bêta-2 mimétiques utilisables dans l'asthme aigu grave</b> "
                    "(reproduit verbatim)", S_CELL_B))
    story.append(Spacer(1, 1.5 * mm))
    cw = [30 * mm, 46 * mm, PAGE_W - 2 * MARGIN - 30 * mm - 46 * mm]
    story.append(simple_table(["Molécule", "Forme galénique", "Dosages / présentations"], [
        ("Salbutamol", "Solution injectable", "Salbutamol® 0,5 mg/5 mL ; Salbumol fort® 5 mg/5 mL ; "
         "Salbumol® 0,5 mg/1 mL ; Ventoline® inj. SC 0,5 mg/1 mL"),
        ("", "Solution pour aérosoliseur", "Ventoline 0,5 %® 50 mg/10 mL ; Ventoline unidose® "
         "1,25 / 2,5 / 5 mg par unidose de 2,5 mL"),
        ("", "Aérosol doseur (chambre d'inhalation)", "Ventoline®, Airomir® / Autohaler®, Spréor® : "
         "200 bouffées à 100 µg"),
        ("", "Aérosol-poudre", "Asmasal Clickhaler® 200 bouffées à 90 µg ; Buventol Easyhaler® "
         "200 bouffées à 100 µg ; Ventodisk® 56 doses à 200 µg"),
        ("Terbutaline", "Solution injectable (SC ou IV)", "Bricanyl® injectable 0,5 mg/1 mL"),
        ("", "Solution pour aérosoliseur", "Bricanyl unidose® 5 mg par unidose de 2,5 mL"),
        ("", "Aérosol doseur (chambre d'inhalation)", "Bricanyl® 200 bouffées à 250 µg"),
        ("", "Aérosol-poudre", "Bricanyl Turbuhaler® 200 bouffées à 500 µg"),
        ("Adrénaline", "Solution injectable", "Adrénaline® 0,25 mg/1 mL ; 0,5 mg/1 mL ; 1 mg/1 mL"),
        ("Autres molécules", "Aérosol doseur / poudre", "Fénotérol (Bérotec®) 100 µg ; Pirbutérol "
         "(Maxair®) 250 µg"),
        ("Associations bêta-2 + atropiniques", "Aérosol doseur / poudre", "Fénotérol + ipratropium "
         "(Bronchodual®) 50/20 µg (doseur, 200 bouffées) ou 100/40 µg (poudre, 30 doses) ; "
         "Salbutamol + ipratropium (Combivent®) 50/20 µg, doseur, 200 bouffées"),
    ], cw))
    return story

def _section_q3():
    story = []
    story.append(Spacer(1, 2 * mm))
    story.append(section_bar("Question 3 — Place des autres thérapeutiques à la phase initiale"))
    story.append(Spacer(1, 2 * mm))
    story.append(reco_table([
        ("Oxygénothérapie — indication", "Indication formelle, débit ≥ 6-8 L/min, "
         "préférentiellement au masque à réserve.", None, "2"),
        ("Oxygénothérapie — hypercapnie", "L'hypoxémie (inhomogénéité VA/Q, aggravée par les "
         "bêta-2 mimétiques) est corrigée sans difficulté par l'enrichissement en O2 ; "
         "l'aggravation potentielle de l'hypercapnie n'est que théorique.", "c", None),
        ("Oxygénothérapie — surveillance", "Monitorage de la SpO2 indispensable tant que "
         "persistent les signes de gravité.", None, "3"),
        ("Corticothérapie — principe", "Intérêt de la prescription précoce et systématique non "
         "discuté (bases physiopathologiques établies : effets anti-inflammatoires, augmentation "
         "du nombre et de l'affinité des récepteurs bêta-2), efficacité clinique en 6-8 h.",
         "b", None),
        ("Corticothérapie — posologies élevées", "Les posologies élevées sont inutiles.", "a", "1"),
        ("Corticothérapie — posologie recommandée", "1 à 2 mg/kg/j d'équivalent "
         "méthylprednisolone.", "b", "2"),
        ("Corticothérapie — équivalence des voies", "De nombreuses études tendent à prouver une "
         "équivalence de la voie orale par rapport à la voie IV (la plus utilisée en pratique).",
         "a", None),
        ("Corticothérapie — voie orale en pratique", "En l'absence de contre-indication, la voie "
         "orale peut être utilisée (utile si un abord veineux n'est pas encore disponible, ex. "
         "domicile).", "a", "2"),
        ("Corticothérapie — corticoïdes inhalés", "Pas leur place chez l'adulte dans cette "
         "indication ; preuves insuffisantes chez l'enfant pour les juger aussi efficaces que la "
         "voie systémique (non coté par le jury).", None, None),
        ("Anticholinergiques — profil pharmacologique", "Effet bronchodilatateur moins puissant et "
         "plus progressif que les bêta-2 mimétiques : maximal entre 30 et 90 min après inhalation, "
         "persistant 3 à 9 h.", "a", None),
        ("Anticholinergiques — efficacité & tolérance", "Place dans l'AAG discutée, mais les formes "
         "les plus graves répondraient mieux ; effets secondaires minimes même à doses élevées.",
         "b", None),
        ("Anticholinergiques — posologie adulte", "Bromure d'ipratropium : 3 nébulisations de "
         "500 µg dans la première heure, couplées aux nébulisations de bêta-2 mimétique (pas de "
         "données au-delà de ce délai).", "c", "3"),
        ("Anticholinergiques — posologie enfant", "3 nébulisations de 250 µg (&lt; 6 ans) ou "
         "500 µg (&gt; 6 ans) de bromure d'ipratropium dans la première heure, en association aux "
         "bêta-2 mimétiques (pas de données sur la durée optimale au-delà).", "a", "1"),
        ("Adrénaline — profil", "Aucun argument ne permet d'affirmer une supériorité de "
         "l'adrénaline par rapport aux bêta-2 mimétiques, tant pour la forme inhalée que "
         "parentérale.", "a", None),
        ("Adrénaline — tolérance en nébulisée", "Effets systémiques modérés en cas d'utilisation "
         "de la voie nébulisée, pour des posologies inférieures à 3 mg.", "b", None),
        ("Adrénaline — usages non validés", "Formes graves résistantes : administration IV "
         "continue proposée par certaines équipes, sans étude validant cette pratique. Voie SC "
         "(0,25-0,5 mg adulte, 10 µg/kg enfant) encore utilisée dans les pays anglo-saxons et en "
         "pédiatrie (non coté par le jury).", None, None),
        ("Aminophylline — adulte", "Utilisation des dérivés xanthiques injustifiée chez l'adulte "
         "(index thérapeutique faible, interactions médicamenteuses), y compris en association aux "
         "bêta-2 en cas de résistance au traitement conventionnel.", "a", "1"),
        ("Aminophylline — enfant", "Garde sa place en deuxième intention pour certaines équipes : "
         "attaque de 6 à 10 mg/kg sur une heure, puis entretien de 0,7 à 1 mg/kg/h, sous réserve de "
         "mesurer la théophyllinémie et de réduire les doses de bêta-2 mimétiques.", "b", "3"),
        ("Sulfate de magnésium", "Mécanisme mal précisé ; pourrait être réservé aux patients "
         "victimes d'une crise grave (DEP &lt; 30 % de la valeur théorique et/ou non-réponse au "
         "traitement initial bien conduit). Posologie IV usuelle 1-2 g en 20 min chez l'adulte "
         "(doses plus élevées parfois administrées, non recommandables) ; 40 mg/kg IV chez l'enfant "
         "(bonne tolérance rapportée).", "b", "3"),
        ("Mélange hélium-oxygène", "Gaz rare sans effet biologique ni propriété bronchodilatatrice "
         "propres ; intérêt théorique lié à sa basse densité et haute viscosité (réduction des "
         "résistances des voies aériennes), perdu si la FiO2 dépasse 40 à 60 %. Résultats des "
         "études cliniques trop divergents pour établir une recommandation.", "b", None),
        ("Antibiothérapie — indication", "Antibiotiques réservés aux patients présentant une "
         "infection broncho-pulmonaire patente.", "b", "2"),
        ("Antibiothérapie — choix", "Bêta-lactamines préférentiellement utilisées hors allergie "
         "vraie antérieurement connue ; évoquer un micro-organisme atypique (Mycoplasma "
         "pneumoniae) chez l'enfant de plus de quatre ans.", "c", "1"),
        ("Kinésithérapie", "N'a pas démontré d'efficacité spécifique dans l'AAG.", "c", None),
        ("Mesures adjuvantes non systématiques", "Réhydratation non "
         "systématique (indiquée en cas de fièvre, sueurs abondantes, signes de déshydratation, "
         "polypnée). Agents mucolytiques non recommandés (risque de diminuer les possibilités de "
         "toux et d'aggraver l'obstruction, voire de majorer le bronchospasme). Anxiolytiques et "
         "hypnotiques <b>contre-indiqués</b> dans les formes sévères d'AAG.", "c", "3"),
    ], [34 * mm, PAGE_W - 2 * MARGIN - 34 * mm - 17 * mm - 17 * mm, 17 * mm, 17 * mm]))
    return story

def _section_q4():
    story = []
    story.append(Spacer(1, 2 * mm))
    story.append(section_bar("Question 4 — Indications et modalités de l'hospitalisation"))
    story.append(Spacer(1, 2 * mm))
    story.append(reco_table([
        ("Transfert hospitalier", "En l'absence de score clinique validé, l'évolution imprévisible "
         "et la nécessité d'une surveillance continue imposent le transfert en milieu hospitalier "
         "de toute crise d'asthme présentant des signes de gravité.", "b", "1"),
        ("Prise en charge préhospitalière", "Ces patients doivent être pris en charge en "
         "préhospitalier par une équipe médicalisée, envoyée dans les plus brefs délais au "
         "domicile ; admission dans une structure disposant du personnel/matériel de surveillance "
         "continue et pouvant mettre en œuvre rapidement une ventilation mécanique.", "c", "2"),
        ("Critères prédictifs — adulte", "Fondés sur l'évolution du DEP après traitement "
         "bronchodilatateur. À 2 h : DEP ≥ 70 % → bonne réponse (retour possible au domicile) ; "
         "DEP &lt; 70 % → réponse insuffisante, traitement complémentaire. Réévaluation 3-4 h plus "
         "tard : DEP &gt; 70 % → retour au domicile ; DEP 50-70 % → orientation au cas par cas ; "
         "DEP &lt; 50 % → hospitalisation.", "b", "2"),
        ("Limite disclosed de ces critères", "Réduction du taux d'hospitalisation sans hausse "
         "notable du taux de rechute à 2 semaines, <b>mais</b> ces schémas ont été validés pour une "
         "population générale d'asthme aigu sévère et <b>non spécifiquement pour l'AAG</b> — en "
         "aucun cas un patient ayant présenté des signes cliniques de gravité ne peut être renvoyé "
         "directement à domicile (précision de la source, non un ajout de cette fiche).",
         None, None),
        ("Suite de prise en charge", "Poursuivie en milieu pneumologique, afin d'optimiser la "
         "fonction respiratoire, d'initier un traitement de fond si absent, et d'entreprendre "
         "l'éducation du patient.", None, None),
        ("Critères de sortie — enfant", "Poursuite de l'hospitalisation non indispensable si, après "
         "2 h de traitement : DEP &gt; 60 % (ou 70 % si facteurs de risque), FR &lt; 30/min "
         "(&gt; 5 ans), absence de tirage/battement des ailes du nez, enfant se disant bien, "
         "parents comprenant le plan de traitement et les signes d'aggravation, accès rapide à "
         "l'hôpital possible, médicaments disponibles, SpO2 &gt; 91 % sous air.", "b", "2"),
    ], [36 * mm, PAGE_W - 2 * MARGIN - 36 * mm - 17 * mm - 17 * mm, 17 * mm, 17 * mm]))
    return story

def _section_q5():
    story = []
    story.append(Spacer(1, 2 * mm))
    story.append(section_bar("Question 5 — Modalités de la ventilation mécanique"))
    story.append(Spacer(1, 2 * mm))
    story.append(reco_table([
        ("Indications de l'intubation", "Morbidité et mortalité immédiate non négligeables. À "
         "envisager lors d'une dégradation clinique malgré un traitement conventionnel bien "
         "conduit, ou lorsque la présentation est grave d'emblée (trouble significatif de la "
         "conscience, bradypnée, cyanose, voire arrêt cardio-respiratoire).", "c", None),
        ("Modalités d'induction", "En l'absence d'arrêt circulatoire : décubitus dorsal, "
         "préoxygénation, induction en séquence rapide en position assise. La kétamine associée à "
         "un curare d'action rapide pourrait être intéressante (propriétés bronchodilatatrices "
         "potentielles).", "c", "2"),
        ("Choix de la sonde", "Sonde à ballonnet du plus grand diamètre possible recommandée, "
         "même chez l'enfant.", "c", "3"),
        ("Réglages ventilatoires", "Objectif : améliorer l'oxygénation sans pressions des voies "
         "aériennes trop élevées. Fréquence basse (6-10/min adulte, 8-12/min grand enfant), volume "
         "courant restreint (6-8 mL/kg), débit d'insufflation élevé, FiO2 augmentée. Cible : "
         "pression de plateau télé-inspiratoire (Pplat) ≈ 30 cmH2O et PaO2 ≥ 80 mmHg, sans utiliser "
         "la capnie comme critère de décision. Mode volumétrique préféré par certaines équipes "
         "(Ppointe plus élevée sans effet délétère théorique attendu). Pas d'indication à ajouter "
         "une PEP en ventilation contrôlée en dehors de situations mécaniques particulières.",
         "b", "2"),
        ("Sédation et curarisation", "Sédation profonde le plus souvent requise par la stratégie "
         "d'hypoventilation contrôlée (pas de recommandation spécifique). Curarisation, si jugée "
         "nécessaire chez un patient sédaté au préalable de façon optimale, préférentiellement par "
         "bolus intermittents sous surveillance par neurostimulateur, compte tenu de la relation "
         "entre risque neuromyopathique et dose totale de curares.", "c", "2"),
        ("Nébulisation chez le patient ventilé", "Pas d'étude comparant nébulisation et voie IV "
         "chez le patient ventilé. Poursuite logique du traitement bronchodilatateur si conditions "
         "techniques adéquates (aérosols doseurs avec chambre d'inhalation sur le circuit "
         "inspiratoire, nébuliseurs pneumatiques ou ultrasoniques) ; les rares études comparatives "
         "plaident pour les dispositifs ultrasoniques (masses inhalées plus élevées).", None, None),
        ("Sevrage ventilatoire", "Habituellement rapide, sans problème particulier. Des difficultés "
         "de sevrage alors que l'obstruction est levée doivent faire évoquer une atteinte "
         "neuro-myopathique, le plus souvent liée à l'association corticostéroïdes + curarisation "
         "non dépolarisante, combinaison fréquente lors de la VM pour asthme grave.", "c", "3"),
        ("Agents halogénés", "Action broncho-dilatatrice connue mais mécanismes mal élucidés ; "
         "respirateurs de réanimation actuels ne permettant en règle pas leur usage (à l'exception "
         "du Servo 900 C™). Halothane à proscrire (toxicité hépatique). Isoflurane bien évalué en "
         "réanimation, effet bronchodilatateur important et rapide — usage en routine non "
         "recommandé faute d'études suffisantes.", None, "1"),
        ("Ventilation non invasive (VNI)", "Intérêt suggéré par quelques séries cliniques, mais "
         "difficultés pratiques chez le patient asthmatique et caractère anecdotique des études "
         "disponibles : usage au cours de l'AAG <b>non recommandé</b> par le jury.", None, None),
    ], [34 * mm, PAGE_W - 2 * MARGIN - 34 * mm - 17 * mm - 17 * mm, 17 * mm, 17 * mm]))
    return story

def _section_conclusion():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(section_bar("Conclusion du jury (verbatim, condensée)", color=GREY))
    story.append(Spacer(1, 2 * mm))
    story.append(info_panel(P(
        "« Cette réactualisation permet de répondre à un bon nombre de questions restées en "
        "suspens lors de la conférence de consensus initiale. Il n'y a cependant toujours pas de "
        "score de gravité validé, et la place de l'administration des bêta-2 mimétiques par voie "
        "intraveineuse en cas d'absence de réponse aux nébulisations n'est pas établie. »",
        S_BODY_SM), bg=BG_PANEL, border=TEAL))
    return story

def _section_sources():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("Jury, méthodologie & sources", color=GREY))
    story.append(Spacer(1, 2 * mm))
    story.append(P(
        "<b>Groupe de travail pour la révision :</b> E. L'Her (Brest, coordinateur), M. Fayon "
        "(Bordeaux), Y. Castaing (Bordeaux), Ph. Gajdos (Garches), L. Holzapfel (Bourg-en-Bresse), "
        "F. Joye (Carcassonne), R. Robert (Poitiers). <b>Conseillers scientifiques :</b> F. Saulnier "
        "pour la partie Adulte (Lille), P. Hubert pour la partie Pédiatrie (Paris). <b>Liste des "
        "experts</b> et <b>groupe de lecture</b> : voir texte intégral (27 experts et lecteurs "
        "nommément cités dans la source).", S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>Document source :</b> Révision de la 3<sup>e</sup> Conférence de Consensus en "
        "Réanimation et Médecine d'Urgence de 1988, Société de Réanimation de Langue Française "
        "(SRLF). Publiée dans <i>Réanimation</i> 2002;11:1-9, © 2002 Éditions scientifiques et "
        "médicales Elsevier SAS. Analyse bibliographique fondée sur environ 350 articles recensés "
        "pour la population adulte depuis la conférence de 1988 (&gt; 40 essais thérapeutiques "
        "randomisés, 140 études de cohorte/épidémiologiques, 70 études physiopathologiques, 70 "
        "revues générales).", S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>Méthodologie :</b> grille SRLF à deux axes — niveau de preuve de la référence (a &gt; "
        "b &gt; c &gt; d, selon le type d'étude) et, quand jugé possible par le jury, niveau de "
        "recommandation (1 &gt; 2 &gt; 3). Voir panneau méthodologique, page 1.", S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>Couverture :</b> cette fiche reprend l'intégralité des 5 questions du texte long "
        "(gravité immédiate et Tableau I, voie des bêta-2 mimétiques et Tableau II, autres "
        "thérapeutiques, indications d'hospitalisation, modalités de ventilation mécanique), ainsi "
        "que la conclusion du jury. Champ de la conférence : adulte et enfant, "
        "<b>hors nouveau-né et hors nourrisson</b> (voir intro).", S_SOURCE))
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Avertissement — document de 2002 (révision d'une conférence de 1988) :</b> cette fiche "
        "de synthèse indépendante est produite pour un usage d'aide-mémoire. Elle reprend "
        "l'intégralité des questions traitées et des deux tableaux du texte source, mais ne "
        "remplace pas le texte intégral (argumentaire complet, références bibliographiques "
        "numérotées) et n'est ni éditée ni validée par la SRLF. <b>Les pratiques de prise en "
        "charge de l'asthme aigu grave ont évolué depuis 2002</b> (place élargie du sulfate de "
        "magnésium et de la VNI dans des recommandations ultérieures, ex. SFMU/SPLF/GINA) : en cas "
        "de doute, se référer au texte intégral, aux recommandations ultérieures et/ou à un avis "
        "spécialisé.", S_BODY_SM), bg=GREY_LIGHT, border=GREY))
    return story

# Merge attempt (per CLAUDE.md step 7): intro+Q1, Q3+Q4 and Q5+conclusion were each
# spilling their last few lines onto a near-empty trailing page (verified visually at
# 135dpi: pages 1, 3, 7, 8, 10 were all <60% full in the one-section-per-page cut).
# Merging removes the forced PageBreak between these adjacent sections so content
# reflows continuously; actual page count re-measured below via _count_pages() rather
# than assumed (this has NOT always helped in this corpus, e.g. fiche_sevrage_vm.py's
# Q3+Q4 merge attempt left the page count unchanged and was reverted there).
def _section_1():
    return _section_intro() + [Spacer(1, 3 * mm)] + _section_tableau1() + [Spacer(1, 1 * mm)] + _section_q1_reco()

def _section_2():
    return _section_q2_intro()

def _section_3():
    return _section_q2_tableau2()

def _section_4():
    return _section_q3() + [Spacer(1, 3 * mm)] + _section_q4()

def _section_5():
    return _section_q5() + [Spacer(1, 3 * mm)] + _section_conclusion() + [Spacer(1, 1 * mm)] + _section_sources()

SECTIONS = [
    ("Introduction, champ, méthodologie & Q1 — Gravité (Tableau I)", _section_1),
    ("Q2 — Bêta-2 mimétiques : schéma thérapeutique", _section_2),
    ("Q2 — Bêta-2 mimétiques : Tableau II & voies", _section_3),
    ("Q3-Q4 — Autres thérapeutiques & indications d'hospitalisation", _section_4),
    ("Q5 — Ventilation mécanique, conclusion & sources", _section_5),
]

def _make_doc(path=None):
    return SimpleDocTemplate(path or OUT, pagesize=A4,
                              leftMargin=MARGIN, rightMargin=MARGIN,
                              topMargin=32 * mm, bottomMargin=16 * mm,
                              title="Fiche SRLF 2002 - Asthme aigu grave",
                              author="Synthese independante (source SRLF)")

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
    # Throwaway measurement builds go to a fresh tempfile.mktemp() path, NEVER to OUT
    # (reusing OUT here was found to corrupt page 1's header_band in the final build).
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
