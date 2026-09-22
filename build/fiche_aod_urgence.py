# -*- coding: utf-8 -*-
"""
Fiche de synthese - "Prise en charge des complications hemorragiques graves
et de la chirurgie en urgence chez les patients recevant un anticoagulant
oral anti-IIa ou anti-Xa direct". Propositions du Groupe d'Interet en
Hemostase Perioperatoire (GIHP), publiees Ann Fr Anesth Reanim 2013;32:
691-700 (recu 18/03/2013, accepte 25/04/2013). Auteurs : G. Pernod,
P. Albaladejo (coordinateurs), et 12 co-auteurs. 10 pages source, telecharge
depuis sfar.org (download/gestion-perioperatoire-des-aod-en-urgence/
?wpdmdl=34804 - reference bibliotheque indexee "2021" sur le site SFAR,
mais l'article lui-meme est date et signe 2013 - DIVERGENCE DE DATE
disclosed, non resolue : la date de publication reelle utilisee dans cette
fiche est 2013, celle de l'article source).

METHODOLOGIE - 8e convention distincte de ce corpus : ce n'est ni une RFE,
ni une RPC/CE, ni un format GRADE/Delphi - c'est un article de
"Propositions" du GIHP (groupe d'interet, pas une societe savante
officielle au sens SFAR/HAS), explicitement presente comme non-
recommandation : "le peu de donnees disponibles ne permet pas d'emettre
des recommandations, mais seulement des propositions qui seront amenees a
evoluer" (resume de la source). AUCUN systeme de cotation (pas de grade
A/B/C, pas d'accord fort/faible) - chip "AE" non utilise ici, remplace par
un badge "Proposition GIHP" dans le legend pour eviter de suggerer une
cotation qui n'existe pas dans la source.

PORTEE - LIMITATION TEMPORELLE MAJEURE DISCLOSED (regle de projet 2) :
- La source elle-meme limite son champ au dabigatran et au rivaroxaban
  ("les donnees relatives a l'apixaban et a l'edoxaban etant encore trop
  peu nombreuses" - citation directe du resume). Apixaban et edoxaban NE
  SONT PAS couverts par cette fiche, conformement a la source.
- Document de 2013 : PRECEDE la commercialisation des antidotes
  specifiques (idarucizumab/Praxbind pour le dabigatran, autorise en
  France en 2016 ; andexanet alfa/Ondexxya pour les anti-Xa, autorise en
  2019) - le texte ne mentionne donc AUCUN antidote specifique, seulement
  des agents procoagulants non specifiques (CCP, FEIBA). Un lecteur en
  2026 DOIT se referer aux protocoles actualises integrant ces antidotes
  avant toute decision therapeutique - avertissement explicite en page 1
  et en fin de fiche, pas seulement dans le corps du texte.
- Malgre ces limites, ce document reste le seul de ce type dans le corpus
  SFAR indexe et "en vigueur" au moment de la construction de cette fiche ;
  il est conserve comme reference historique/transitoire des principes
  generaux (dosage plasmatique, seuils de securite hemostatique, delais
  selon fonction renale) qui restent conceptuellement utilises, mais dont
  l'application therapeutique (choix de l'antidote) doit etre actualisee.

DEFAUT DE PRODUCTION DU PDF SOURCE DISCLOSED (regle de projet 5, jamais
resolu silencieusement) : les figures et leurs legendes sont MAL
APPARIEES dans le PDF source lui-meme (verifie par rendu visuel a 200dpi
des pages 4 a 9, pas seulement l'extraction texte) :
- La legende "Fig. 4" (censee etre l'algorithme chirurgie urgente
  rivaroxaban guide par TP/TCA, evoque textuellement section 3.3) est
  imprimee au-dessus d'un diagramme qui est en realite une DUPLICATION de
  l'algorithme "hemorragie grave, dosage disponible" (le futur Fig. 6).
  Le vrai diagramme "rivaroxaban guide par TP/TCA" n'existe DANS AUCUNE
  page du PDF - seul le texte (section 3.3) decrit cette conduite,
  explicitement comme identique a celle du dabigatran (Fig. 3) avec les
  memes seuils de ratio TCA/TQ.
- La legende "Fig. 5" (censee etre la definition HAS 2008 des hemorragies
  graves sous AVK) est imprimee au-dessus du MEME diagramme dupplique
  ("hemorragie grave, dosage disponible") - pas une definition. Le contenu
  reel de cette definition existe bien dans le PDF, mais sous forme du
  Tableau 2 (page 699), pas d'une figure numerotee.
- La legende "Fig. 6" (imprimee correctement en page 699, titree "...sur
  la base de la determination de la concentration de medicament") est
  elle-meme incoherente avec son propre diagramme, qui utilise en realite
  des seuils de ratio TCA/TQ (tests usuels), pas une concentration -
  erreur de legende, pas d'extraction.
CETTE FICHE reconstruit le contenu clinique reel a partir du texte du
corps (section 3.3, explicitement "approche identique a celle du
dabigatran") pour l'algorithme rivaroxaban/TCA manquant, et reproduit
fidelement les 2 diagrammes "hemorragie grave" (guide par concentration
et guide par tests usuels) une seule fois chacun malgre leur duplication
dans le PDF, en disclosant ce defaut de production plutot qu'en le
reproduisant ou en l'ignorant silencieusement.

ARGUMENTAIRE : condense (regle de projet 2026-09-14) - la section 2
"Argumentaire" de la source (pharmacocinetique, tests d'hemostase,
justification du seuil de 30 ng/mL) est resumee a l'essentiel actionnable
(Tableau 1 PK, seuil de 30 ng/mL et sa justification en une phrase) ; la
discussion detaillee des etudes RE-LY/ROCKET-AF et la sensibilite
comparee des reactifs de laboratoire sont omises.

AUDIT INDEPENDANT (2026-09-15, subagent) et corrections appliquees :
1. Bande 200-400 ng/mL (Fig. 1 dabigatran ET Fig. 2 rivaroxaban) : le
   brouillon initial affichait "12-24h" (copie du diagramme original) alors
   que le corps du texte specifie explicitement un "delai minimum de
   24 heures" pour cette bande, pour les DEUX molecules - divergence
   diagramme/texte interne a la source, desormais disclosed dans la fiche
   au lieu d'etre silencieusement tranchee en faveur du diagramme.
2. Algorithme rivaroxaban guide par TCA/TQ (Fig. 4, absente du PDF) :
   le brouillon reutilisait tel quel le tableau dabigatran (Fig. 3) en le
   presentant comme strictement identique, y compris sa clause de dialyse
   a Cockcroft<50. Or le texte du corps (section 3.3) donne des delais
   reellement differents pour le rivaroxaban (12h fixes pour la bande
   intermediaire, contre "12 a 24h selon la fonction renale" pour le
   dabigatran) et ne mentionne JAMAIS la dialyse pour le rivaroxaban a
   cette etape - coherent avec l'absence de dialyse envisageable pour
   cette molecule (deja disclosed ailleurs dans la fiche), mais contredit
   par la reutilisation aveugle du tableau dabigatran. Corrige : tableau
   rivaroxaban distinct reconstruit avec ses propres delais et sans
   clause de dialyse, et la propre affirmation de la source ("approche
   identique") est elle-meme disclosed comme une simplification excessive
   de la source par rapport a ses propres details chiffres.
3. Ajout d'un avertissement manquant (fin de section 2.7 de la source) :
   l'INR n'a aucune place dans la gestion des situations critiques chez un
   patient sous AOD (outil concu pour les AVK) - le rapport M/T du temps
   de Quick doit lui etre prefere. Point de securite actionnable, absent
   du brouillon initial.
4. Restauration d'une note du Tableau 1 (PK) : absence de donnees pour le
   rivaroxaban 15 mg x2/j, les valeurs 10 mg n'etant indicatives qu'a titre
   de repere - supprimee par erreur lors de la condensation initiale.
5. Suppression d'une precision non sourcee ("forte liaison proteique" comme
   justification de la non-faisabilite de la dialyse pour le rivaroxaban)
   - la source elle-meme ne donne aucune justification a cette difference
   avec le dabigatran ; presenter une raison non citee aurait constitue une
   invention non disclosed.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from style import *
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.units import mm

OUT = "/home/user/rfe-sfar-website/output/Fiche_GIHP_AOD_Urgence_2013.pdf"

SOURCE_TXT = ("Source : « Prise en charge des complications hémorragiques graves et de la "
              "chirurgie en urgence chez les patients recevant un anticoagulant oral anti-IIa "
              "ou anti-Xa direct » — Propositions GIHP, Ann Fr Anesth Reanim 2013;32:691-700. "
              "Fiche de synthèse non officielle : se référer au texte intégral.")

def P(txt, style=S_CELL):
    return Paragraph(txt, style)

CW_FULL = PAGE_W - 2 * MARGIN

def grid_table(head_row, rows, col_widths, head_bg=NAVY):
    data = [[P(h, S_HEAD_W_C) for h in head_row]]
    for row in rows:
        data.append([P(c, S_CELL) for c in row])
    t = Table(data, colWidths=col_widths, repeatRows=1)
    style_cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), head_bg), ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
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

def theme_table(rows, col_widths, head=("Thème", "Détail")):
    data = [[P(head[0], S_HEAD_W), P(head[1], S_HEAD_W)]]
    for theme, detail in rows:
        data.append([P(theme, S_CELL_B), P(detail, S_CELL)])
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

TCW = [38 * mm, CW_FULL - 38 * mm]

TOTAL_PAGES = {"n": 7}

def on_page(canvas, doc, page_title):
    header_band(canvas, doc, "GIHP — Propositions, 2013",
                "AOD : chirurgie et hémorragie en urgence",
                page_title, icon_fn=lambda c, x, y: icon_drop(c, x, y, 13 * mm), color=RED)
    footer_band(canvas, doc, SOURCE_TXT, f"Page {doc.page} / {TOTAL_PAGES['n']}")

# ---------------------------------------------------------------------------
def _section_intro():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Résumé :</b> propositions du Groupe d'Intérêt en Hémostase Périopératoire "
        "(GIHP) pour la chirurgie urgente à risque hémorragique et les hémorragies graves "
        "chez un patient traité par <b>dabigatran (Pradaxa®) ou rivaroxaban (Xarelto®)</b> "
        "à dose curative. <b>Portée limitée par la source elle-même</b> à ces 2 molécules "
        "(apixaban/edoxaban explicitement exclus, données insuffisantes en 2013). "
        "<b>Aucun système de cotation</b> : ce ne sont pas des recommandations mais des "
        "« propositions », amenées à évoluer.", S_BODY), bg=BG_PANEL, border=TEAL))
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>⚠ Avertissement majeur — document de 2013, antérieur aux antidotes "
        "spécifiques :</b> ce texte précède la commercialisation de l'idarucizumab "
        "(Praxbind®, antidote du dabigatran, autorisé en France en 2016) et de "
        "l'andexanet alfa (Ondexxya®, antidote des anti-Xa, autorisé en 2019). Il ne "
        "propose donc que des agents procoagulants non spécifiques (CCP, FEIBA) et NE "
        "REFLÈTE PAS la prise en charge actuelle de référence. À utiliser uniquement "
        "comme repère historique des principes généraux (dosage plasmatique, délais "
        "selon fonction rénale) — se référer impérativement aux protocoles actualisés "
        "intégrant les antidotes spécifiques avant toute décision thérapeutique.",
        S_BODY_SM), bg=AMBER_LIGHT, border=AMBER))
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("Méthodologie et contexte"))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "Article publié le 18/03/2013 (accepté 25/04/2013) par le GIHP — ce n'est ni une "
        "RFE, ni une RPC, ni une conférence d'experts SFAR : aucun grade A/B/C, aucun "
        "« accord fort/faible ». La méthodologie repose sur l'analyse de la littérature "
        "pharmacocinétique puis une relecture critique par les membres du GIHP jusqu'à "
        "consensus — la source précise elle-même que « le peu de données disponibles ne "
        "permet pas d'émettre des recommandations, mais seulement des propositions ». "
        "<i>Note de datation :</i> la bibliothèque SFAR indexe ce document sous l'année "
        "« 2021 » (date de mise en ligne/réindexation probable), mais l'article "
        "lui-même est daté et signé 2013 — divergence disclosed, la date d'origine "
        "(2013) est retenue dans cette fiche.", S_BODY_SM))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>Seuil de sécurité hémostatique :</b> une concentration plasmatique "
        "≤ 30 ng/mL, pour le dabigatran comme pour le rivaroxaban, est extrapolée des "
        "protocoles des essais cliniques (RE-LY, ROCKET-AF) comme compatible avec une "
        "chirurgie à risque hémorragique sans majoration du risque. Dans tous les cas, "
        "il faut préciser : âge, poids, nom du médicament, indication, dose, nombre de "
        "prises/jour, heure de la dernière prise, clairance de la créatinine (formule "
        "de Cockcroft et Gault).", S_BODY_SM))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P("<b>Tableau 1 — Données pharmacocinétiques des AOD (repère) :</b>",
                    S_BODY_SM))
    story.append(Spacer(1, 1 * mm))
    story.append(grid_table(
        ["", "Cmax (ng/mL)", "Cmin (ng/mL)"],
        [
            ["Dabigatran 220 mg/j (1 prise)", "183 (5-95 perc : 64-447)", "37 (5-95 perc : "
             "10-96) à 24 h"],
            ["Dabigatran 150 mg × 2/j", "254 (± 70,5)", "80,3 (18,7) à 12 h"],
            ["Rivaroxaban 10 mg/j (1 prise)", "125 (5-95 perc : 91-195)", "9 (5-95 perc : "
             "1-38) à 24 h"],
            ["Rivaroxaban 20 mg/j (1 prise)", "215 (5-95 perc : 22-535)", "32 (5-95 perc : "
             "6-239) à 24 h"],
        ], [55 * mm, CW_FULL - 55 * mm - 45 * mm, 45 * mm]))
    story.append(Spacer(1, 1 * mm))
    story.append(P(
        "<i>Note du Tableau 1 (source) : pas de donnée pour le rivaroxaban 15 mg × 2/j "
        "(schéma initial TVP/EP) ; les données 10 mg sont ici indicatives.</i>", S_NOTE))
    return story

def _section_chirurgie_dosage():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("Chirurgie urgente à risque hémorragique — dosage plasmatique disponible"))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P("<b>Fig. 1 — Dabigatran, selon la concentration plasmatique :</b>",
                    S_BODY_SM))
    story.append(Spacer(1, 1 * mm))
    story.append(grid_table(
        ["Concentration", "Conduite à tenir"],
        [
            ["≤ 30 ng/mL", "Opérer sans délai."],
            ["30-200 ng/mL", "Si un report est possible : attendre jusqu'à 12 h puis "
             "nouveau dosage. Si non : opérer ; en cas de saignement anormal, "
             "antagoniser (CCP 25-50 UI/kg ou FEIBA 30-50 UI/kg selon disponibilité)."],
            ["200-400 ng/mL", "Retarder au maximum l'intervention. Délai minimum de "
             "24 h puis nouveau dosage <i>(le diagramme original de la source indique "
             "« 12-24 h », le corps du texte précise « un délai minimum de 24 heures » "
             "— divergence interne à la source, disclosed)</i>. Si clairance de "
             "Cockcroft &lt; 50 mL/min : discuter la dialyse (35 % du dabigatran est "
             "lié à l'albumine ; l'hémodialyse réduit la concentration de 40-60 % en "
             "4 h)."],
            ["&gt; 400 ng/mL", "Surdosage — risque hémorragique majeur. Discuter la "
             "dialyse avant chirurgie (délai pour atteindre le seuil de 30 ng/mL long "
             "en cas de surdosage, à intégrer dans la décision de report)."],
        ], [30 * mm, CW_FULL - 30 * mm]))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P("<b>Fig. 2 — Rivaroxaban, selon la concentration plasmatique "
                    "(même structure que le dabigatran) :</b>", S_BODY_SM))
    story.append(Spacer(1, 1 * mm))
    story.append(grid_table(
        ["Concentration", "Conduite à tenir"],
        [
            ["≤ 30 ng/mL", "Opérer sans délai."],
            ["30-200 ng/mL", "Si un report est possible : attendre jusqu'à 12 h puis "
             "nouveau dosage. Si non : opérer ; en cas de saignement anormal, "
             "antagoniser (CCP 25-50 UI/kg ou FEIBA 30-50 UI/kg selon disponibilité)."],
            ["200-400 ng/mL", "Retarder au maximum l'intervention. Délai minimum de "
             "24 h puis nouveau dosage <i>(même divergence diagramme/texte que pour le "
             "dabigatran, voir Fig. 1)</i>."],
            ["&gt; 400 ng/mL", "Surdosage — risque hémorragique majeur. <b>Contrairement "
             "au dabigatran, la dialyse n'est pas envisageable</b> avec le rivaroxaban "
             "(motif non précisé par la source). Retarder au maximum l'intervention si "
             "l'état du patient le permet."],
        ], [30 * mm, CW_FULL - 30 * mm]))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<i>CCP/FEIBA — mises en garde communes aux 2 molécules (notes de la source) : "
        "aucune donnée sur le risque thrombotique de fortes doses chez ces patients ; "
        "l'antagonisation par CCP ou FEIBA ne corrige pas complètement les anomalies "
        "biologiques de l'hémostase ; le rFVIIa n'est pas envisagé en première "
        "intention.</i>", S_NOTE))
    return story

def _section_chirurgie_tests_usuels():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("Chirurgie urgente à risque hémorragique — dosage spécifique indisponible"))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "Solution <b>dégradée</b>, seulement en cas d'indisponibilité immédiate du "
        "dosage spécifique — ne garantit pas formellement l'absence de complications "
        "hémorragiques. Combinaison TCA + TP (ou TQ) normaux : conclut avec une "
        "fiabilité relative à une concentration &lt; 30 ng/mL. Le temps de thrombine "
        "(TT, très sensible au dabigatran) peut exclure sa présence s'il est normal, "
        "mais retarde inutilement la décision dans la plupart des situations — peu "
        "utile en urgence.", S_BODY_SM))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P("<b>Fig. 3 — Dabigatran, selon le ratio TCA/TQ malade-témoin (M/T) :</b>",
                    S_BODY_SM))
    story.append(Spacer(1, 1 * mm))
    story.append(grid_table(
        ["Ratio TCA/TQ", "Conduite à tenir"],
        [
            ["TCA ≤ 1,2 ET TQ ≤ 1,2 (TP ≥ 70-80 %)", "Opérer sans délai."],
            ["1,2 &lt; TCA ≤ 1,5, ou TQ &gt; 1,2 (TP &lt; 70-80 %)", "Correspond à "
             "≈ 30-200 ng/mL. Si un report est possible : attendre jusqu'à 12 à 24 h "
             "selon la fonction rénale, obtenir un dosage spécifique + nouveau TP/TCA. "
             "Si non : opérer ; en cas de saignement anormal, antagoniser (CCP "
             "25-50 UI/kg ou FEIBA 30-50 UI/kg)."],
            ["TCA &gt; 1,5", "Correspond à &gt; 200 ng/mL (Cmax). Retarder au maximum "
             "l'intervention. Délai minimum de 24 h, obtenir un dosage spécifique + "
             "nouveau TP/TCA. Si Cockcroft &lt; 50 mL/min : discuter la dialyse."],
        ], [55 * mm, CW_FULL - 55 * mm]))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>Fig. 4 (rivaroxaban) — algorithme absent du PDF source, reconstruit à "
        "partir du texte (§3.3) :</b>", S_BODY_SM))
    story.append(Spacer(1, 1 * mm))
    story.append(grid_table(
        ["Ratio TCA/TQ", "Conduite à tenir"],
        [
            ["TCA ≤ 1,2 ET TQ ≤ 1,2 (ou activité anti-Xa ≤ 0,1 U/mL)", "Opérer sans "
             "délai."],
            ["1,2 &lt; TCA ≤ 1,5", "Correspond à 30-200 ng/mL. Délai d'attente "
             "jusqu'à <b>12 h</b> (pas de qualificatif « selon la fonction rénale » "
             "dans la source pour cette molécule, à la différence du dabigatran), "
             "répéter le TCA, obtenir un dosage spécifique si compatible avec "
             "l'urgence."],
            ["TCA &gt; 1,5", "Correspond à &gt; 200 ng/mL. Délai minimum de 24 h, "
             "obtenir un dosage spécifique dans ce délai. Retarder au maximum "
             "l'intervention. <b>La source ne mentionne pas la dialyse pour cette "
             "situation</b> (cohérent avec l'absence de dialyse envisageable pour le "
             "rivaroxaban, voir Fig. 2)."],
        ], [55 * mm, CW_FULL - 55 * mm]))
    story.append(Spacer(1, 1.5 * mm))
    story.append(info_panel(P(
        "<b>Défaut de production du PDF source disclosed :</b> la source affirme "
        "d'abord (§3.3, en préambule) une « approche identique à celle du dabigatran » "
        "pour le rivaroxaban, mais les délais qu'elle détaille ensuite pour chaque "
        "bande de ratio TCA diffèrent en réalité légèrement de ceux du dabigatran "
        "(12 h vs 12-24 h pour la bande intermédiaire ; aucune mention de dialyse pour "
        "le rivaroxaban) — incohérence interne à la source elle-même, disclosed "
        "plutôt que lissée. Par ailleurs, aucune figure numérotée correcte n'existe "
        "pour cet algorithme dans le PDF publié : l'emplacement annoncé par le texte "
        "(« Fig. 4 ») imprime en réalité, par erreur de mise en page de la source, une "
        "duplication du diagramme « hémorragie grave » (voir page suivante) — le "
        "tableau ci-dessus est donc reconstruit uniquement à partir du texte du "
        "corps. Seule différence testologique avec le dabigatran : la mesure de "
        "l'activité anti-Xa (technique héparine) est très sensible au rivaroxaban — "
        "une activité ≤ 0,1 U/mL exclut sa présence, mais ce test est peu utile en "
        "urgence (retarde la décision).",
        S_BODY_SM), bg=BG_PANEL, border=TEAL))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>⚠ L'INR n'a aucune place</b> dans la gestion des situations critiques "
        "chez un patient traité par AOD (mode d'expression conçu pour les AVK) — lui "
        "préférer le rapport malade/témoin (M/T) du temps de Quick.", S_NOTE))
    story.append(Spacer(1, 2.5 * mm))
    story.append(section_bar("Si la chirurgie ne peut être repoussée et les seuils ne sont pas atteints"))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "Opérer <b>sans</b> administration préventive de médicaments procoagulants. "
        "Recourir à ceux-ci (CCP 25-50 UI/kg, ou FEIBA 30-50 UI/kg — éventuellement "
        "renouvelable une fois en cas d'échec) <b>seulement en cas de saignement "
        "anormal</b> per- ou postopératoire. Privilégier en première ligne la dose la "
        "plus faible proposée.", S_BODY_SM))
    return story

def _section_hemorragie_grave():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("Hémorragie grave spontanée ou chirurgicale"))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "La définition HAS/GEHT 2008 des hémorragies graves sous AVK est reprise par "
        "défaut, faute de définition spécifique aux AOD (voir Tableau 2). Deux "
        "situations sont distinguées.", S_BODY_SM))
    story.append(Spacer(1, 1.5 * mm))
    story.append(KeepTogether([
        P("<b>1 — Hémorragie dans un organe critique</b> (intracérébrale, sous-durale "
          "aiguë, intra-oculaire…) :", S_BODY_SM),
        Spacer(1, 1 * mm),
        theme_table([
            ("Conduite immédiate", "Neutralisation immédiate de l'effet anticoagulant : "
             "FEIBA 30-50 UI/kg <b>ou</b> CPP 50 UI/kg, éventuellement renouvelé une "
             "fois à 8 h d'intervalle — quel que soit le résultat des tests, sans "
             "attendre. Le suivi de la concentration du médicament sera utile pour la "
             "décision opératoire complémentaire."),
        ], TCW),
    ]))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P("<b>2 — Autres hémorragies graves</b> (définition HAS, Tableau 2) :",
                    S_BODY_SM))
    story.append(Spacer(1, 1 * mm))
    story.append(grid_table(
        ["Situation", "Conduite à tenir"],
        [
            ["Geste hémostatique praticable d'emblée (endoscopique, intravasculaire)",
             "À privilégier quel que soit le taux du médicament."],
            ["Concentration ≤ 30 ng/mL", "L'hémorragie ne peut être imputée au seul "
             "médicament — pas d'administration d'agent hémostatique (CCP/FEIBA)."],
            ["Concentration &gt; 30 ng/mL et aucun geste hémostatique adapté",
             "Tenter d'inhiber l'effet anticoagulant (CCP 25-50 UI/kg, ou FEIBA "
             "30-50 UI/kg, éventuellement renouvelable une fois), optimiser la "
             "réanimation ; pour le dabigatran, envisager une épuration par "
             "hémodialyse guidée par la concentration."],
            ["Dosage spécifique non disponible", "Raisonner sur le TCA et le TP, avec "
             "un niveau élevé d'incertitude (même logique que ci-dessus, seuil "
             "indicatif : ratio TCA ≤ 1,2 et TQ ≤ 1,2/TP ≥ 70-80 % → pas "
             "d'antagonisation ; au-delà → discuter l'antagonisation et obtenir un "
             "dosage spécifique)."],
        ], [58 * mm, CW_FULL - 58 * mm]))
    story.append(Spacer(1, 1.5 * mm))
    story.append(info_panel(P(
        "<b>Défaut de production du PDF source disclosed :</b> les 2 diagrammes "
        "correspondant à ce tableau (l'un guidé par la concentration, l'autre par les "
        "tests usuels) sont bien présents dans le PDF, mais leurs légendes sont "
        "incohérentes avec leur propre contenu — le diagramme « guidé par "
        "concentration » est imprimé deux fois sous les légendes erronées « Fig. 4 » "
        "et « Fig. 5 » (au lieu des figures réellement annoncées par le texte à ces "
        "emplacements), et le diagramme correctement légendé « Fig. 6 » décrit dans "
        "son titre une approche par concentration alors qu'il utilise en réalité des "
        "ratios TCA/TQ. Contenu clinique reconstruit ici à partir des diagrammes "
        "réels et du texte du corps, sans dépendre des légendes erronées.",
        S_BODY_SM), bg=GREY_LIGHT, border=GREY))
    story.append(Spacer(1, 2.5 * mm))
    story.append(P("<b>Tableau 2 — Définition HAS 2008 d'une hémorragie grave ou "
                    "potentiellement grave sous AVK</b> (reprise par défaut pour les AOD, "
                    "au moins un critère) :", S_BODY_SM))
    story.append(Spacer(1, 1 * mm))
    story.append(theme_table([
        ("Hémorragie extériorisée", "Non contrôlable par les moyens usuels."),
        ("Instabilité hémodynamique", "PAS &lt; 90 mmHg ou diminution de 40 mmHg par "
         "rapport à la PAS habituelle, ou PAM &lt; 65 mmHg, ou tout signe de choc."),
        ("Geste hémostatique urgent nécessaire", "Chirurgie, radiologie "
         "interventionnelle, endoscopie."),
        ("Transfusion", "Nécessité de transfusion de culots globulaires."),
        ("Localisation menaçant le pronostic vital ou fonctionnel", "Hémorragie "
         "intracrânienne et intraspinale ; hémorragie intraoculaire et rétro-orbitaire ; "
         "hémothorax, hémo- et rétropéritoine, hémopéricarde ; hématome musculaire "
         "profond et/ou syndrome de loge ; hémorragie digestive aiguë ; hémarthrose."),
    ], TCW, head=("Critère", "Détail")))
    return story

def _section_sources():
    story = []
    story.append(Spacer(1, 1.5 * mm))
    story.append(section_bar("Sources et traçabilité", color=GREY))
    story.append(Spacer(1, 1 * mm))
    story.append(P(
        "<b>Document source :</b> « Prise en charge des complications hémorragiques "
        "graves et de la chirurgie en urgence chez les patients recevant un "
        "anticoagulant oral anti-IIa ou anti-Xa direct » — Propositions du GIHP. "
        "Coordinateurs : G. Pernod, P. Albaladejo. Reçu le 18/03/2013, accepté le "
        "25/04/2013.", S_SOURCE))
    story.append(Spacer(1, 1 * mm))
    story.append(P("<b>Version :</b> Ann Fr Anesth Reanim 2013;32:691-700.", S_SOURCE))
    story.append(Spacer(1, 1 * mm))
    story.append(P("<b>Méthodologie :</b> analyse de la littérature + relecture "
                    "critique du GIHP jusqu'à consensus — aucun système de cotation "
                    "(pas de grade, pas d'accord fort/faible). Propositions, pas des "
                    "recommandations (terminologie de la source elle-même).", S_SOURCE))
    story.append(Spacer(1, 1 * mm))
    story.append(P(
        "<b>URL source :</b> https://sfar.org/download/gestion-perioperatoire-des-aod-"
        "en-urgence/?wpdmdl=34804", S_SOURCE))
    story.append(Spacer(1, 1 * mm))
    story.append(P(
        "<b>Couverture :</b> intégralité du contenu actionnable pour le dabigatran et "
        "le rivaroxaban (seules molécules couvertes par la source elle-même). "
        "L'algorithme rivaroxaban/TCA manquant du PDF (défaut de production disclosed "
        "plus haut) est reconstruit fidèlement à partir du texte du corps. Hors champ, "
        "explicitement par la source : apixaban, edoxaban (données insuffisantes en "
        "2013).", S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(info_panel(P(
        "<b>Avertissement — document de 2013, propositions non validées comme "
        "recommandation officielle :</b> cette fiche de synthèse indépendante reprend "
        "l'intégralité du contenu actionnable du texte source, mais ne le remplace "
        "pas et n'est ni éditée ni validée par la SFAR ou le GIHP. Ce document est "
        "antérieur aux antidotes spécifiques (idarucizumab, andexanet alfa) et ne "
        "couvre ni l'apixaban ni l'edoxaban — se référer impérativement aux protocoles "
        "actualisés du centre de prise en charge et à un avis spécialisé "
        "(hématologie/hémostase) avant toute décision thérapeutique.", S_BODY_SM),
        bg=GREY_LIGHT, border=GREY))
    return story

def _section_contexte_chirurgie():
    story = _section_intro()
    story.extend(_section_chirurgie_dosage())
    return story

def _section_tests_hemorragie_sources():
    story = _section_chirurgie_tests_usuels()
    story.extend(_section_hemorragie_grave())
    story.extend(_section_sources())
    return story

SECTIONS = [
    ("Contexte, pharmacocinétique & chirurgie — dosage disponible", _section_contexte_chirurgie),
    ("Chirurgie sans dosage, hémorragie grave & sources", _section_tests_hemorragie_sources),
]

def _make_doc(path=None):
    return SimpleDocTemplate(path or OUT, pagesize=A4,
                              leftMargin=MARGIN, rightMargin=MARGIN,
                              topMargin=32 * mm, bottomMargin=16 * mm,
                              title="Fiche GIHP 2013 - AOD chirurgie et hemorragie en urgence",
                              author="Synthèse indépendante (source GIHP/SFAR)")

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
