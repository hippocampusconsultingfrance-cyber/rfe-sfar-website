# -*- coding: utf-8 -*-
"""
Fiche de synthese - "Recommandations sur les indications de l'assistance circulatoire dans
le traitement des arrets cardiaques refractaires" - Conseil francais de reanimation
cardiopulmonaire, SFAR, Societe francaise de cardiologie, Societe francaise de chirurgie
thoracique et cardiovasculaire, SFMU, Societe francaise de pediatrie, GFRUP, Societe
francaise de perfusion, SRLF. Coordonnateur : Bruno Riou. Ann Fr Anesth Reanim 2009;28:182-186,
doi:10.1016/j.annfar.2008.12.011. Sous l'egide de la DGS et de la DHOS. Source :
sources/eclsa.pdf (5 pages), extrait en texte integral dans sources/eclsa.txt. Pas de tampon
d'obsolescence sur la page 1 (verifiee visuellement a 150dpi) - document non marque "abroge"
dans build/library_final.json (status "en vigueur").

METHODOLOGIE - PAS de systeme GRADE, PAS de numerotation R1/R2, PAS de cotation par
proposition individuelle. Le texte est redige en prose continue (introduction, objectifs,
definition, proposition, perspectives) et ne comporte qu'UNE SEULE mention de niveau de
preuve, appliquee globalement a l'ensemble des propositions du groupe d'experts : "les
propositions faites par notre groupe d'experts (recommandations de niveau 5) [14]" - le
niveau 5 designe, dans l'echelle citee en reference [14] (Malinovsky et al., Aide a la
lecture d'une recommandation, SFAR 2000), le niveau le plus bas (avis d'experts, sans preuve
scientifique etablie). Consequence pour la maquette : PAS de reco_table()/theme_table() avec
chips par ligne (ce serait fabriquer une granularite de cotation que la source n'imprime
jamais) - un unique badge global "NIVEAU 5 - AVIS D'EXPERTS" est utilise a la place, dans le
panneau d'introduction et l'en-tete de page, jamais applique ligne par ligne.

FIGURE (Fig. 1, page 3 de la source /page 184 de la revue, "Proposition d'algorithme de
decision d'une assistance circulatoire devant un arret cardiaque (AC) refractaire") : pure
organigramme graphique (boites + fleches), transcrit ici a partir d'un rendu visuel a 170dpi
(build/eclsa_png/eclsa_p3.png), jamais depuis le seul ordre du texte extrait (les boites de
l'organigramme ne sont pas du texte lineaire). Arbre verifie visuellement : trois colonnes
verticales (Indication possible / Incertitude / Pas d'indication) partant d'un noeud commun
"AC refractaire" ; la colonne centrale (Incertitude) se ramifie a chaque etape d'evaluation
(duree de no-flow, rythme, duree de low-flow) vers la gauche (Indication possible) ou la
droite (Pas d'indication) selon les seuils imprimes. Reproduit ici en tableau structure a
spans (meme technique que fiche_civd.py/algo_table()) plutot qu'en graphique vectoriel, avec
toutes les branches et tous les seuils numeriques transcrits verbatim (0-5 min ; >5 min ou
pas de temoin ; ETCO2 >= 10 mmHg ET low-flow <= 100 min ; ETCO2 < 10 mmHg OU low-flow >
100 min) - AUCUNE branche omise, y compris la reintegration des troubles du rythme (TV/TP/FV,
hors rythmes agoniques) dans la voie "indication possible" depuis la colonne "incertitude".

COUVERTURE : ce document est court (5 pages, un seul algorithme, pas de tableau de criteres
separe) mais dense en prose continue. Cette fiche reprend l'integralite du texte : contexte
epidemiologique et historique, les trois "craintes" motivant la demarche du groupe d'experts,
la definition classique de l'AC refractaire et le changement de paradigme introduit par la
possibilite d'une assistance circulatoire, les deux determinants physiopathologiques
(no-flow/low-flow) et les elements cliniques qui remettent en cause leur estimation (signes
de vie, troubles du rythme, hypothermie), le seuil ETCO2, la regle des 15 minutes minimales
de RCP medicalisee avant d'evoquer la technique, les modalites pratiques de mise en oeuvre
(equipe multidisciplinaire, abord vasculaire femoral, perfusionniste), les specificites
pediatriques (<15 kg) et de l'AC hypothermique, et les limites explicitement reconnues par
les auteurs (cohortes monocentriques selectionnees, caractere preliminaire, lacunes de
connaissances identifiees, appel a la formation aux gestes de premier secours).

DOCUMENT DE 2009 - AVERTISSEMENT DE PEREMPTION (disclosure, meme pratique que
fiche_civd.py/fiche_glycemie.py pour les documents anciens) : ce texte precede les grands
essais randomises modernes sur l'ECPR (ARREST 2020, PRAGUE-OHCA 2022, INCEPTION 2023) qui ont
precise (et parfois nuance) la place de l'assistance circulatoire dans l'arret cardiaque
refractaire. Les seuils et l'algorithme reproduits ici sont ceux de 2009, disclose comme tels
plutot que silencieusement mis a jour avec des donnees posterieures non presentes dans la
source.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from style import *
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.units import mm

OUT = "/home/user/rfe-sfar-website/output/Fiche_SFAR_ECLS_AC_Refractaire_2009.pdf"

SOURCE_TXT = ("Source : Riou B, et al. — Conseil français de réanimation cardiopulmonaire, SFAR, "
              "Société française de cardiologie, Société française de chirurgie thoracique et "
              "cardiovasculaire, SFMU, Société française de pédiatrie, GFRUP, Société française de "
              "perfusion, SRLF — « Recommandations sur les indications de l'assistance circulatoire "
              "dans le traitement des arrêts cardiaques réfractaires », Ann Fr Anesth Reanim "
              "2009;28:182-186. Fiche de synthèse non officielle : se référer au texte intégral.")

def P(txt, style=S_CELL):
    return Paragraph(txt, style)

def simple_table(header, rows, col_widths):
    data = [[P(h, S_HEAD_W_C) for h in header]]
    for r in rows:
        data.append([P(c, S_CELL_C) for c in r])
    t = Table(data, colWidths=col_widths, repeatRows=1)
    st = [
        ("BACKGROUND",(0,0),(-1,0), TEAL_DARK), ("TEXTCOLOR",(0,0),(-1,0), WHITE),
        ("FONTNAME",(0,0),(-1,0), FONT_BOLD), ("FONTSIZE",(0,0),(-1,0), 8),
        ("GRID",(0,0),(-1,-1),0.5,GREY_LIGHT), ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
        ("TOPPADDING",(0,0),(-1,-1),3.2), ("BOTTOMPADDING",(0,0),(-1,-1),3.2),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            st.append(("BACKGROUND",(0,i),(-1,i), BG_PANEL))
    t.setStyle(TableStyle(st))
    return t

def algo_table():
    """Organigramme (Fig. 1, page 3 source) - reconstruit a partir du rendu visuel
    (build/eclsa_png/eclsa_p3.png), pas du seul ordre du texte extrait (les boites d'un
    organigramme ne sont pas lineaires dans le flux PyMuPDF). Trois colonnes verticales
    (Indication possible / Incertitude / Pas d'indication) ; toutes les branches et tous les
    seuils numeriques de la source sont transcrits verbatim, y compris la reintegration des
    troubles du rythme (TV/TP/FV) dans la voie "indication possible"."""
    cw = PAGE_W - 2*MARGIN
    c0 = c2 = cw * 0.30
    c1 = cw - c0 - c2
    S_A = pstyle("ecls_a", fontSize=7.6, leading=9.6, textColor=INK, alignment=TA_CENTER)
    S_A_B = pstyle("ecls_a_b", fontSize=8.6, leading=10.4, textColor=WHITE, fontName=FONT_BOLD, alignment=TA_CENTER)
    S_A_HEAD = pstyle("ecls_a_head", fontSize=7.8, leading=9.6, textColor=INK, fontName=FONT_BOLD, alignment=TA_CENTER)
    S_A_HEAD_W = pstyle("ecls_a_head_w", fontSize=8.2, leading=10, textColor=WHITE, fontName=FONT_BOLD, alignment=TA_CENTER)

    def ac(txt, style=S_A):
        return Paragraph(txt, style)

    data = [
        [ac("INDICATION POSSIBLE", S_A_HEAD_W), ac("INCERTITUDE", S_A_HEAD_W), ac("PAS D'INDICATION", S_A_HEAD_W)],
        ["", ac("AC réfractaire", S_A_B), ""],
        [ac("← Intoxication † · Hypothermie † (≤ 32 °C) · Signes de vie per-RCP "
            "(ramènent directement vers cette colonne, quelle que soit la durée de no-flow)", S_A),
         ac("Évaluation de la durée de <b>no-flow</b>", S_A_HEAD), ac("← Comorbidités (limitation légitime des "
            "traitements invasifs : réanimation, chirurgie, angioplastie)", S_A)],
        ["", ac("0–5 min", S_A_HEAD), ac("&gt; 5 min ou pas de témoin", S_A_HEAD)],
        [ac("← TV, TP, FV (hors rythmes agoniques) réintègrent cette colonne "
            "depuis l'évaluation du rythme", S_A),
         ac("Évaluation de la durée de <b>low-flow</b>", S_A_HEAD),
         ac("Évaluation du <b>rythme</b> → Asystole / rythme agonique = pas d'indication", S_A)],
        [ac("<b>ETCO2 ≥ 10 mmHg ET low-flow ≤ 100 min*</b>", S_A_HEAD), "",
         ac("<b>ETCO2 &lt; 10 mmHg OU low-flow &gt; 100 min</b>", S_A_HEAD)],
    ]
    t = Table(data, colWidths=[c0, c1, c2])
    style_cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("BACKGROUND", (0, 1), (-1, 1), TEAL_DARK),
        ("BACKGROUND", (0, 2), (-1, 2), BG_PANEL),
        ("BACKGROUND", (0, 3), (-1, 3), WHITE),
        ("BACKGROUND", (0, 4), (-1, 4), BG_PANEL),
        ("BACKGROUND", (0, 5), (0, 5), GREEN_LIGHT),
        ("BACKGROUND", (2, 5), (2, 5), RED_LIGHT),
        ("GRID", (0, 0), (-1, -1), 0.5, GREY_LIGHT),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("TOPPADDING", (0, 0), (-1, -1), 3.6), ("BOTTOMPADDING", (0, 0), (-1, -1), 3.6),
        ("LEFTPADDING", (0, 0), (-1, -1), 4), ("RIGHTPADDING", (0, 0), (-1, -1), 4),
    ]
    t.setStyle(TableStyle(style_cmds))
    return t

TOTAL_PAGES = {"n": 6}

def on_page(canvas, doc, page_title):
    header_band(canvas, doc, "CFRC / SFAR / SFC / SFMU / SRLF ET AL. — RFE 2009 — FICHE DE SYNTHÈSE",
                "Assistance circulatoire — AC réfractaire",
                page_title, icon_fn=lambda c, x, y: icon_drop(c, x, y, 13*mm), color=NAVY)
    footer_band(canvas, doc, SOURCE_TXT, f"Page {doc.page} / {TOTAL_PAGES['n']}")

# ---------------------------------------------------------------------------
def _section_intro():
    story = []
    story.append(Spacer(1, 3*mm))
    story.append(info_panel(P(
        "<b>Champ :</b> indications et contre-indications de l'<b>assistance circulatoire "
        "(ECLS/ECMO)</b> au cours de la réanimation cardiopulmonaire des <b>arrêts cardiaques "
        "(AC) réfractaires</b>, intra- et extrahospitaliers, adultes et pédiatriques. "
        "Recommandations rédigées sous l'égide de la Direction générale de la santé et de la "
        "Direction des hôpitaux, à la demande de neuf sociétés savantes françaises (Conseil "
        "français de réanimation cardiopulmonaire, SFAR, Société française de cardiologie, "
        "Société française de chirurgie thoracique et cardiovasculaire, SFMU, Société "
        "française de pédiatrie, GFRUP, Société française de perfusion, SRLF). "
        "Coordonnateur : Bruno Riou.<br/><br/>"
        "<b>Méthodologie :</b> texte rédigé en prose continue, <b>sans système GRADE ni "
        "numérotation R1/R2</b>. Une seule mention de niveau de preuve est imprimée, "
        "appliquée globalement à l'ensemble des propositions du groupe d'experts : "
        "« recommandations de <b>niveau 5</b> » — le niveau le plus bas de l'échelle citée "
        "en référence (avis d'experts, sans preuve scientifique établie). Aucune cotation "
        "par proposition individuelle n'est imprimée : ce document n'utilise donc pas de "
        "tableau à chips par ligne.",
        S_BODY), bg=BG_PANEL, border=TEAL))
    story.append(Spacer(1, 2.5*mm))
    row = Table([[
        Paragraph("NIVEAU 5", pstyle("badge5", fontSize=9.4, leading=11, textColor=WHITE,
                                      fontName=FONT_BOLD, alignment=TA_CENTER)),
        P("<b>Avis d'experts</b> — seul niveau de preuve imprimé par la source, appliqué à "
          "l'ensemble du texte (aucune proposition individuelle n'est cotée séparément).",
          S_BADGE_HEAD),
    ]], colWidths=[24*mm, PAGE_W - 2*MARGIN - 24*mm])
    row.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (0,0), GREY), ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("ALIGN", (0,0), (0,0), "CENTER"), ("TOPPADDING", (0,0), (-1,-1), 3),
        ("BOTTOMPADDING", (0,0), (-1,-1), 3), ("LEFTPADDING", (0,0), (-1,-1), 3),
        ("RIGHTPADDING", (1,0), (1,0), 2),
    ]))
    story.append(row)
    story.append(Spacer(1, 3*mm))
    story.append(section_bar("Contexte"))
    story.append(Spacer(1, 2*mm))
    story.append(P(
        "Environ <b>50 000 arrêts cardiaques</b> surviennent chaque année en France ; la "
        "survie des victimes reste faible (de l'ordre de <b>3–5 %</b>). L'assistance "
        "circulatoire a été proposée dès 1976 au cours de la RCP des AC réfractaires, mais "
        "son utilisation est longtemps restée limitée aux AC hypothermiques et à ceux "
        "survenant en chirurgie cardiothoracique, après des essais cliniques initiaux peu "
        "encourageants. La miniaturisation récente des techniques a permis une utilisation "
        "plus fréquente, notamment pour des AC d'origine toxique ou cardiaque survenant "
        "essentiellement en intrahospitalier : des cohortes monocentriques françaises et "
        "taïwanaises rapportent des survies sans séquelle neurologique importante dans "
        "<b>20 à 30 %</b> de ces populations très sélectionnées. À l'inverse, les données "
        "préliminaires françaises pour les AC <b>préhospitaliers</b> sont décevantes, avec "
        "moins de <b>1 % de survie</b> — les délais de mise en place y étant nettement plus "
        "longs que dans les études rapportant une amélioration de la survie intrahospitalière.",
        S_BODY_SM))
    story.append(Spacer(1, 2*mm))
    story.append(P("<b>Trois craintes</b> ont motivé la demande d'un texte de recommandations :", S_CELL_B))
    story.append(P(
        "• un développement anarchique de l'assistance circulatoire en préhospitalier, "
        "nuisible à son essor du fait de résultats médiocres dans des indications mal "
        "choisies ;<br/>"
        "• la survie de patients avec des séquelles neurologiques considérables (l'évolution "
        "défavorable des cas rapportés se faisant toutefois vers la mort encéphalique et non "
        "vers un état de coma chronique) ;<br/>"
        "• une inhomogénéité des critères retenus en France, faute de données solides sur les "
        "indications et contre-indications de cette technique d'exception.", S_BODY_SM))
    story.append(Spacer(1, 2*mm))
    story.append(info_panel(P(
        "<b>Objectif du texte :</b> proposer des indications et contre-indications de "
        "l'assistance circulatoire dans la réanimation des AC réfractaires intra- et "
        "extrahospitaliers. Le groupe d'experts souligne qu'il ne s'agit que "
        "d'<b>indications potentielles</b> : il ne peut y avoir, à ce stade, d'injonction à "
        "pratiquer une thérapeutique d'exception dont le bénéfice n'est pas établi et qui "
        "n'est pas disponible partout ni à tout moment. Ce texte reflète un consensus "
        "d'experts à un moment donné, susceptible d'évoluer avec les avancées d'un domaine "
        "particulièrement dynamique.",
        S_BODY_SM), bg=AMBER_LIGHT, border=AMBER))
    return story

def _section_definition():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Définition de l'AC réfractaire & changement de paradigme"))
    story.append(Spacer(1, 2*mm))
    story.append(P(
        "L'<b>AC réfractaire</b> est habituellement défini par l'absence de reprise d'une "
        "activité circulatoire spontanée (RACS) après <b>au moins 30 minutes de RCP "
        "médicalisée en normothermie</b>. Cette définition est principalement utilisée pour "
        "envisager l'arrêt de la RCP devant une situation jugée sans espoir de survie — "
        "notion reposant sur deux éléments : l'absence d'espoir de récupérer une activité "
        "cardiaque après une RCP inefficace de plus de 30 min, et l'absence d'espoir de "
        "récupérer une activité cérébrale satisfaisante.", S_BODY_SM))
    story.append(Spacer(1, 2*mm))
    story.append(info_panel(P(
        "<b>Changement de paradigme :</b> la possibilité de mettre en place une assistance "
        "circulatoire permet de ne plus considérer, au moins initialement, le premier "
        "élément (absence d'espoir de récupérer une activité cardiaque). Le problème de la "
        "réversibilité de l'atteinte cardiaque ne se pose alors que dans un second temps, une "
        "fois l'assistance en place — pour observer une évolution spontanément favorable "
        "(élimination de toxiques, guérison d'une myocardite), proposer une thérapeutique "
        "réversant l'atteinte (réchauffement d'une hypothermie profonde, angioplastie ou "
        "chirurgie coronaire), ou pallier une atteinte définitive (cœur artificiel, "
        "transplantation). <b>L'espoir de récupérer une activité cérébrale satisfaisante "
        "devient alors l'élément principal de la décision.</b>",
        S_BODY_SM), bg=BG_PANEL, border=TEAL))
    story.append(Spacer(1, 2*mm))
    story.append(P(
        "Il est important de noter que ces propositions <b>ne remettent pas en cause les "
        "bases de la RCP usuelle</b> effectuée pour la plupart des AC non réfractaires. Il "
        "n'est pas nécessaire de modifier la définition classique de l'AC réfractaire "
        "(30 min sans assistance circulatoire) : en revanche, lorsque les conditions sont "
        "requises pour évoquer l'utilité d'une assistance circulatoire, <b>il n'est pas "
        "nécessaire d'attendre ces 30 minutes</b> pour déclencher les opérations — le délai "
        "de mise en œuvre, en particulier en préhospitalier, fait que l'assistance est de "
        "toute façon le plus souvent mise en place au-delà. Il n'est cependant pas "
        "raisonnable d'évoquer l'hypothèse d'une telle technique avant <b>au moins 15 "
        "minutes</b> de RCP médicalisée.", S_BODY_SM))
    return story

def _section_elements():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(KeepTogether([
        section_bar("Éléments cliniques modulant la décision"),
        Spacer(1, 2*mm),
        P("Deux éléments physiopathologiques sont essentiels au raisonnement médical sur la "
          "poursuite ou non de la RCP :", S_BODY_SM),
        Spacer(1, 1.5*mm),
        simple_table(["Déterminant", "Définition", "Poids pronostique"], [
            ["No-flow", "Durée de débit cardiaque nul avant la RCP (suppose un AC constaté "
             "par un témoin)", "Variable ayant l'impact le plus fort sur le pronostic "
             "neurologique — cible prioritaire (no-flow nul = RCP immédiate par témoins)"],
            ["Low-flow", "Durée de bas débit cardiaque pendant la RCP", "Rôle moindre mais "
             "non négligeable : relation inverse avec la survie (Chen et al. : &lt;10 % de "
             "survie au-delà de 100 min de RCP)"],
        ], [26*mm, (PAGE_W-2*MARGIN)-26*mm-58*mm, 58*mm]),
    ]))
    story.append(Spacer(1, 2*mm))
    story.append(P("<b>Situations qui remettent en cause une durée de no-flow estimée "
                    "prolongée</b> (le groupe d'experts recommande d'en tenir compte) :", S_CELL_B))
    story.append(P(
        "• l'<b>hypothermie</b>, en raison de son effet protecteur bien démontré sur "
        "l'ischémie cérébrale (survies rapportées malgré un AC prolongé) ;<br/>"
        "• une <b>estimation probablement imprécise</b> de la durée de no-flow, notamment "
        "lorsque la perte de conscience du patient ne coïncide pas avec le début réel de "
        "l'AC ;<br/>"
        "• des <b>signes de vie</b> constatés pendant la RCP : mouvements spontanés, absence "
        "de mydriase et/ou réactivité pupillaire, voire gasps inspiratoires (probablement de "
        "mauvais pronostic malgré tout) ;<br/>"
        "• certains <b>troubles du rythme</b> — tachycardie ventriculaire (TV), torsades de "
        "pointes (TP), fibrillation ventriculaire (FV) — à l'exclusion des rythmes agoniques.",
        S_BODY_SM))
    story.append(Spacer(1, 2*mm))
    story.append(P(
        "Une durée prolongée de low-flow constitue un risque accru de souffrance cérébrale "
        "et participe au syndrome de défaillance multiviscérale observé après AC — élément "
        "important pour les AC préhospitaliers, où la durée de transport est généralement "
        "connue avec une bonne approximation. <b>Exception disclosée par la source :</b> "
        "dans le cadre des <b>intoxications par les cardiotropes</b>, une durée prolongée de "
        "RCP ne contre-indique pas formellement l'assistance circulatoire (des survies y ont "
        "été rapportées), sans que cela ne doive conduire à prolonger inutilement la RCP "
        "préhospitalière au-delà des 30 minutes recommandées par ailleurs pour ces "
        "intoxications.", S_BODY_SM))
    story.append(Spacer(1, 2*mm))
    story.append(info_panel(P(
        "<b>Monitorage :</b> le monitorage de la RCP par la mesure télé-expiratoire du CO2 "
        "(ETCO2) reflète le débit cardiaque généré — une valeur d'<b>ETCO2 &lt; 10 mmHg</b> "
        "(mesurée après 20 min de RCP médicalisée) est associée à un <b>mauvais pronostic "
        "neurologique</b>.<br/><br/>"
        "<b>Comorbidités :</b> certaines comorbidités rendent déraisonnable toute RCP, quelles "
        "que soient les circonstances — toutes les situations où une limitation des "
        "traitements invasifs (réanimation, chirurgie, angioplastie coronaire) est légitime. "
        "<b>L'âge ne constitue pas en soi</b> une raison suffisante pour limiter la RCP "
        "courante, de la même façon qu'il ne constitue pas en soi une raison suffisante pour "
        "ne pas proposer la réanimation.<br/><br/>"
        "<b>Machines à massage cardiaque :</b> leur diffusion en préhospitalier, sans preuve "
        "démontrée d'efficacité ni d'innocuité sur la survie, ne doit pas modifier les délais "
        "maximums autorisés de RCP.",
        S_BODY_SM), bg=BG_PANEL, border=TEAL))
    return story

def _section_algo():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Algorithme décisionnel (Fig. 1 de la source)"))
    story.append(Spacer(1, 2*mm))
    story.append(P(
        "Un algorithme simple, utilisable dans les conditions de l'urgence, est proposé par "
        "le groupe d'experts. Reproduit ci-dessous à partir du rendu visuel de la source "
        "(les boîtes/flèches de l'organigramme ne sont pas restituables en texte linéaire) : "
        "trois colonnes verticales partant d'un même point de départ (« AC réfractaire »).",
        S_BODY_SM))
    story.append(Spacer(1, 2*mm))
    story.append(algo_table())
    story.append(Spacer(1, 1.5*mm))
    story.append(P(
        "<i>* Une durée de RCP &gt; 100 min peut être acceptée dans le cas des intoxications "
        "par les cardiotropes. † Indications reconnues par l'International Liaison Committee "
        "on Resuscitation (ILCOR). Les comorbidités sont celles qui amèneraient à ne pas "
        "indiquer des soins invasifs (réanimation, chirurgie, angioplastie coronaire par "
        "exemple). La durée du low-flow comprend la RCP de base (témoins et secouristes) et "
        "la RCP médicalisée.</i>", S_NOTE))
    return story

def _section_pratique():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(KeepTogether([
        section_bar("Modalités pratiques de mise en œuvre"),
        Spacer(1, 2*mm),
        P(
            "Du fait de la miniaturisation des dispositifs, il est tentant de considérer que "
            "la diffusion de cette technique peut être large. La prise en charge requiert une "
            "<b>coopération étroite entre équipes préhospitalières et hospitalières</b>, dans "
            "le cadre d'une filière de soins ad hoc, et la gestion des thérapeutiques destinées "
            "à réverser ou pallier la défaillance cardiaque nécessite une équipe "
            "multidisciplinaire.", S_BODY_SM),
    ]))
    story.append(Spacer(1, 2*mm))
    story.append(simple_table(["Intervenant / élément", "Exigence"], [
        ["Abord vasculaire", "Abord direct des vaisseaux fémoraux recommandé"],
        ["Chirurgien", "Concours d'un chirurgien formé à cette technique recommandé"],
        ["Équipe de réanimation", "Équipe de réanimation qualifiée requise pour la gestion "
         "de l'assistance circulatoire"],
        ["Perfusionniste", "Préparation/maintenance du dispositif idéalement effectuées par "
         "un perfusionniste (compétence acquérable par formation appropriée)"],
    ], [55*mm, (PAGE_W-2*MARGIN)-55*mm]))
    story.append(Spacer(1, 2.5*mm))
    story.append(KeepTogether([
        P("<b>Spécificités pédiatriques</b>", S_CELL_B),
        Spacer(1, 1.5*mm),
        P(
            "Ne concernent que les <b>enfants de moins de 15 kg</b> : difficulté technique de "
            "pose nécessitant un <b>chirurgien spécialisé en chirurgie pédiatrique</b>, et "
            "nécessité de disposer du matériel d'assistance adapté et de "
            "<b>sang homologue</b> pour l'amorçage du circuit.", S_BODY_SM),
    ]))
    story.append(Spacer(1, 2.5*mm))
    story.append(KeepTogether([
        P("<b>AC hypothermique</b>", S_CELL_B),
        Spacer(1, 1.5*mm),
        P(
            "L'hypothermie ne permet plus d'estimer la souffrance neurologique pendant les "
            "périodes de no-flow et low-flow. Même dans ces conditions, les équipes habituées "
            "à prendre en charge ces patients (noyades, accidents de montagne) ont limité les "
            "indications de l'assistance circulatoire aux patients présentant des critères "
            "pronostiques favorables (par exemple, présence d'une poche d'air pour les "
            "accidents d'avalanche) ou en s'aidant de critères biologiques (kaliémie).",
            S_BODY_SM),
    ]))
    return story

def _section_perspectives():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Perspectives, limites & lacunes de connaissances"))
    story.append(Spacer(1, 2*mm))
    story.append(info_panel(P(
        "<b>Limites explicitement reconnues par les auteurs :</b> ces recommandations ne "
        "sont basées que sur des <b>résultats préliminaires</b> établis à partir de "
        "<b>cohortes monocentriques de patients très sélectionnés</b>, concernant surtout des "
        "AC intrahospitaliers survenant dans des secteurs privilégiés (personnels médical et "
        "paramédical hautement spécialisés). L'assistance circulatoire reste une "
        "<b>thérapeutique d'exception</b>, non disponible partout ni à tout moment, qui "
        "s'adresse à un faible nombre de patients. Des registres prospectifs et des essais "
        "cliniques seront nécessaires pour valider ou non ces recommandations.",
        S_BODY_SM), bg=AMBER_LIGHT, border=AMBER))
    story.append(Spacer(1, 2*mm))
    story.append(P("<b>Lacunes de connaissances identifiées par le groupe d'experts</b> :", S_CELL_B))
    story.append(P(
        "• précision des mesures de temps et de délais au cours de l'AC et de la RCP ;<br/>"
        "• pertinence des biomarqueurs pour décider ou non d'une assistance circulatoire "
        "(kaliémie en cas d'hypothermie, lactates, pH, créatininémie) ;<br/>"
        "• qualité du débit cardiaque généré pendant la période de low-flow ;<br/>"
        "• efficacité et innocuité des machines à masser ;<br/>"
        "• émergence de techniques innovantes pour l'évaluation initiale et précoce de la "
        "fonction neurologique.", S_BODY_SM))
    story.append(Spacer(1, 2*mm))
    story.append(P(
        "L'utilisation de cet algorithme devrait permettre d'<b>homogénéiser les pratiques "
        "en France</b> concernant les indications potentielles d'assistance circulatoire — "
        "une réponse jugée appropriée par les auteurs à des considérations à la fois "
        "<b>médicales et éthiques</b>. Les techniques d'assistance circulatoire sont par "
        "ailleurs probablement amenées à se développer dans <b>d'autres indications</b>, y "
        "compris la réanimation post-RACS de l'AC et les AC récidivants.", S_BODY_SM))
    story.append(Spacer(1, 2*mm))
    story.append(P(
        "Les auteurs rappellent enfin que les méthodes les plus efficaces pour améliorer la "
        "survie restent celles qui réduisent la durée de no-flow (formation du grand public "
        "aux manœuvres de RCP, défibrillation précoce), et appellent à rattraper le retard "
        "français en la matière par une campagne de formation aux gestes de premier secours "
        "auprès des collèges et lycées.", S_BODY_SM))
    story.append(Spacer(1, 3*mm))
    story.append(section_bar("Sources & traçabilité", color=GREY))
    story.append(Spacer(1, 2*mm))
    story.append(P(
        "<b>Document source :</b> « Recommandations sur les indications de l'assistance "
        "circulatoire dans le traitement des arrêts cardiaques réfractaires », sous l'égide "
        "de la Direction générale de la santé et de la Direction des hôpitaux et de "
        "l'organisation des soins (Ministère de la Santé). Coordonnateur : Bruno Riou "
        "(Service d'accueil des urgences, GH Pitié-Salpêtrière). Experts : F. Adnet, F. Baud, "
        "A. Cariou, P. Carli, A. Combes, D. Devictor, J.L. Dubois-Randé, J.L. Gérard, P.Y. "
        "Gueugniaud, A. Ricard-Hibon, O. Langeron, P. Leprince, D. Longrois, A. Pavie, P. "
        "Pouard, J.C. Rozé, J.N. Trochu, A. Vincentelli. Ann Fr Anesth Reanim 2009;28:182-186, "
        "doi:10.1016/j.annfar.2008.12.011.", S_SOURCE))
    story.append(Spacer(1, 1.5*mm))
    story.append(P(
        "<b>Méthodologie :</b> prose continue, sans GRADE ni numérotation R1/R2. Une seule "
        "mention globale de niveau de preuve : « recommandations de niveau 5 » (avis "
        "d'experts), appliquée à l'ensemble du texte.", S_SOURCE))
    story.append(Spacer(1, 1.5*mm))
    story.append(P(
        "<b>Couverture :</b> cette fiche reprend l'intégralité des sections Introduction, "
        "Objectifs, Définition (changement de paradigme, no-flow/low-flow), Proposition "
        "(algorithme, Fig. 1, reconstruit à partir d'un rendu visuel à 170dpi), modalités "
        "pratiques, spécificités pédiatriques et de l'AC hypothermique, et Perspectives "
        "(limites, lacunes de connaissances) du texte source de 5 pages.", S_SOURCE))
    story.append(Spacer(1, 3*mm))
    story.append(info_panel(P(
        "<b>Avertissement — document de 2009 :</b> cette fiche de synthèse indépendante ne "
        "remplace pas le texte intégral (argumentaire complet, références bibliographiques) "
        "et n'est ni éditée ni validée par les sociétés savantes signataires. <b>Ce texte "
        "précède les grands essais randomisés modernes sur l'ECPR</b> (ARREST 2020, "
        "PRAGUE-OHCA 2022, INCEPTION 2023), qui ont depuis précisé — et parfois nuancé — la "
        "place de l'assistance circulatoire dans l'arrêt cardiaque réfractaire. Les seuils et "
        "l'algorithme reproduits ici sont ceux de 2009. En cas de doute, se référer au texte "
        "intégral, aux recommandations ultérieures et/ou à un avis spécialisé.",
        S_BODY_SM), bg=GREY_LIGHT, border=GREY))
    return story

def _section_1():
    return _section_intro()

def _section_2():
    return _section_definition()

def _section_3():
    return _section_elements()

def _section_4():
    return _section_algo()

def _section_5():
    return _section_pratique()

def _section_6():
    return _section_perspectives()

# Tried merging 1+2, 3+4 and 5+6 into 3 combinator groups (same precedent as
# fiche_civd.py): rebuilt and re-measured the ACTUAL page count via _count_pages() rather
# than assuming - it stayed at 6 pages (one merged group just spilled a short tail
# paragraph onto its own near-empty extra page instead of shrinking the total). Reverted to
# the one-section-per-question layout below: same page count, clearer per-page headers.
SECTIONS = [
    ("Introduction, champ & méthodologie", _section_1),
    ("Définition de l'AC réfractaire & changement de paradigme", _section_2),
    ("Éléments cliniques modulant la décision", _section_3),
    ("Algorithme décisionnel", _section_4),
    ("Modalités pratiques & spécificités", _section_5),
    ("Perspectives, limites & sources", _section_6),
]

def _make_doc(path=None):
    return SimpleDocTemplate(path or OUT, pagesize=A4,
                              leftMargin=MARGIN, rightMargin=MARGIN,
                              topMargin=32*mm, bottomMargin=16*mm,
                              title="Fiche 2009 - Assistance circulatoire AC refractaire",
                              author="Synthese independante (source CFRC/SFAR/SRLF et al.)")

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
