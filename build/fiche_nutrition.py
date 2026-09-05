# -*- coding: utf-8 -*-
"""
Fiche de synthese - RFE commune SFAR-SRLF-SFNEP, "Nutrition artificielle en reanimation".
Publiee Ann Fr Anesth Reanim 2014;33:202-218, validee fevrier 2013. 33 experts + 3 presidents
+ 3 pilotes. Methode GRADE, 10 champs.

PARTICULARITE MAJEURE DE CE DOCUMENT (unique dans ce corpus) : contrairement a toutes les
autres RFE deja traitees, cette source n'imprime JAMAIS de tag numerique "GRADE 1+/1-/2+/2-"
a cote de chaque encadre individuel. Seule la methodologie generale (en prose, en debut de
document) definit que "il faut faire/ne pas faire" = GRADE1 et "il faut probablement faire/ne
pas faire" = GRADE2. Le SEUL tag explicitement imprime a cote de CHAQUE "Encadre X.Y" est
"(Accord fort)" ou "(Accord faible)" - qui designe la force du CONSENSUS des experts (issue
du vote Delphi), un axe distinct du niveau de preuve GRADE. Etant donne que plusieurs encadres
ont une formulation composite/ambigue (ex. 9.8.1 purement descriptif sans "il faut" ; 9.8.3 et
10.2.3 combinant une clause "il faut" et une clause "il ne faut probablement pas" dans la meme
phrase), inferer un tag GRADE 1+/2- synthetique aurait un risque reel d'erreur d'interpretation
non verifiable. Decision methodologique : le chip visuel de cette fiche reproduit donc
directement et fidelement le seul tag que la source imprime explicitement pour chaque item
- "Fort" ou "Faible" (Accord fort/faible) - plutot que d'inventer une correspondance GRADE
1+/1-/2+/2- non imprimee par la source. Le texte integral de chaque encadre (deja verbatim)
porte lui-meme la nuance de force/direction ("il faut" vs "il faut probablement") sans qu'un
codage supplementaire soit necessaire. Couleurs chip ajoutees localement au dictionnaire
GRADE_COLORS partage (sans toucher style.py) : "Fort" -> vert (meme poids visuel que 1+),
"Faible" -> teal (meme poids visuel que 2+) - ce choix est sans risque pour les autres fiches
du corpus car aucune autre fiche n'utilise ces libelles.

ECHELLE DU DOCUMENT (la plus grande de tout ce corpus a ce jour) : resume officiel = "69
recommandations" issues des "six derniers champs" (sur 10 champs au total ; les 3 premiers
champs sont decrits par la methodologie comme de simples "points forts" sans "vraies
cotations"). Mon propre inventaire direct, par grep exhaustif de chaque occurrence litterale
"Encadre X.Y[.Z]" dans le texte source (verifie a la main pour 3 items dont le grep automatique
avait rate la detection a cause d'un retour a la ligne en plein milieu du numero d'encadre -
Encadre 6.3, 9.3.1, 9.8.3), denombre 71 encadres numerotes au total, TOUS portant un tag
explicite "(Accord fort)" ou "(Accord faible)" - y compris les 4 encadres des champs 1-3 (1.1,
2.1, 2.2, 3.1) que la methodologie decrit pourtant comme non cotes formellement. Ceci constitue
donc une divergence source-interne a deux niveaux : (a) le chiffre agrege officiel "69" ne
correspond exactement a aucun sous-ensemble evident de mon propre compte de 71 (ni "71 total",
ni "71 moins les 4 points forts = 67", ni d'autres decoupages testes) ; (b) la description
methodologique ("champs 1-3 non cotes") contredit le fait que ces 4 encadres portent bien un
tag Accord fort/faible identique en format a tous les autres. Disclosure explicite dans
l'intro et la tracabilite plutot que recalcul silencieux, conformement a la pratique etablie
de ce corpus. 2 encadres supplementaires (9.1 Polytraumatise, 9.5 Sepsis/defaillance
multiviscerale) sont explicitement des "absence de specificite" sans aucune recommandation
et un troisieme (9.3.1, Insuffisant hepatique - volet calorique) est une absence de specificite
partielle (avec une seule precision chiffree residuelle, sans tag Accord) - ces 3 items sont
donc traites comme no_reco_panel() plutot que comme des lignes de reco_table().

2 tableaux numeriques integralement extractibles en texte (verifies, aucune image) : Tableau 1
(besoins energetiques du brule grave, formules de Toronto/Schoffield par tranche d'age) ;
Tableau 2 (apports recommandes en glucose parenteral pediatrique, g/kg/j par tranche de poids
et jour j1-j4) - ce dernier confirme par rendu visuel de la page 12 (la mention "(Tableau 2)"
dans le texte s'arretait juste avant le debut de la bibliographie a l'extraction automatique).
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from style import *
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.units import mm

# Local, non-invasive extension of the shared GRADE_COLORS dict (safe: no other fiche in the
# corpus uses these two label strings, so no collision risk for other modules sharing `style`).
GRADE_COLORS["Fort"] = (GREEN, WHITE)
GRADE_COLORS["Faible"] = (TEAL, WHITE)

OUT = "/private/tmp/claude-501/-Users-macbook-Downloads-claude/65498e3e-5ddf-47a6-b100-3ac535d1faa0/scratchpad/rfe_sfar/output/Fiche_SFAR_SRLF_SFNEP_Nutrition_2014.pdf"

SOURCE_TXT = ("Source : Recommandations Formalisées d'Experts (RFE) communes SFAR-SRLF-SFNEP "
              "« Nutrition artificielle en réanimation » — Ann Fr Anesth Reanim 2014;33:202-218, "
              "recommandations validées en février 2013. Fiche de synthèse non officielle : se "
              "référer au texte intégral.")

def P(txt, style=S_CELL):
    return Paragraph(txt, style)

def chip(label, **kw):
    return grade_chip(label, **kw)

def reco_table(rows, col_widths):
    """rows: (ref, text, grade_label_for_chip)"""
    data = [[P("Réf.", S_HEAD_W), P("Recommandation", S_HEAD_W), P("Accord", S_HEAD_W_C)]]
    for ref, txt, grade in rows:
        data.append([P(ref, S_CELL_B), P(txt, S_CELL), chip(grade)])
    t = Table(data, colWidths=col_widths, repeatRows=1)
    style_cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), NAVY), ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTNAME", (0, 0), (-1, 0), FONT_BOLD), ("FONTSIZE", (0, 0), (-1, 0), 8),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("ALIGN", (2, 0), (2, -1), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 0.5, GREY_LIGHT),
        ("TOPPADDING", (0, 0), (-1, -1), 3.2), ("BOTTOMPADDING", (0, 0), (-1, -1), 3.2),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            style_cmds.append(("BACKGROUND", (0, i), (-1, i), BG_PANEL))
    t.setStyle(TableStyle(style_cmds))
    return t

def no_reco_panel(text):
    return info_panel(P("<b>Absence de recommandation spécifique</b> — " + text, S_BODY_SM), bg=GREY_LIGHT, border=GREY)

def simple_table(header, rows, col_widths):
    data = [[P(h, S_HEAD_W) for h in header]]
    for r in rows:
        data.append([P(c, S_CELL) for c in r])
    t = Table(data, colWidths=col_widths, repeatRows=1)
    st = [
        ("BACKGROUND",(0,0),(-1,0), TEAL_DARK), ("TEXTCOLOR",(0,0),(-1,0), WHITE),
        ("FONTNAME",(0,0),(-1,0), FONT_BOLD), ("FONTSIZE",(0,0),(-1,0), 8),
        ("GRID",(0,0),(-1,-1),0.5,GREY_LIGHT), ("VALIGN",(0,0),(-1,-1),"TOP"),
        ("TOPPADDING",(0,0),(-1,-1),3.2), ("BOTTOMPADDING",(0,0),(-1,-1),3.2), ("LEFTPADDING",(0,0),(-1,-1),5),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            st.append(("BACKGROUND",(0,i),(-1,i), BG_PANEL))
    t.setStyle(TableStyle(st))
    return t

TOTAL_PAGES = {"n": 8}

def on_page(canvas, doc, page_title):
    header_band(canvas, doc, "SFAR / SRLF / SFNEP — RFE 2014 — FICHE DE SYNTHÈSE",
                "Nutrition artificielle en réanimation",
                page_title, icon_fn=lambda c,x,y: icon_shield(c, x, y, 13*mm), color=NAVY)
    footer_band(canvas, doc, SOURCE_TXT, f"Page {doc.page} / {TOTAL_PAGES['n']}")

# ---------------------------------------------------------------------------
def _section_intro():
    story = []
    story.append(Spacer(1, 3*mm))
    story.append(info_panel(P(
        "<b>Objectif :</b> RFE commune SFAR-SRLF-SFNEP (Société francophone nutrition "
        "clinique et métabolique) — 33 experts, 3 présidents, 3 pilotes. Méthode GRADE. "
        "10 champs, dont 3 premiers traités comme « points forts » (physiopathologie/"
        "évaluation, jugés non cotables formellement) et 7 derniers ayant conduit à des "
        "recommandations formalisées.<br/><br/>"
        "<b>Résultats (résumé officiel) :</b> « 69 recommandations » issues des six derniers "
        "champs. <b>Terminologie propre à cette source :</b> chaque recommandation "
        "(« Encadré ») porte un tag explicite unique « (Accord fort) » ou « (Accord faible) » "
        "— reflétant la force du consensus des experts (vote Delphi), affiché ici comme "
        "chip coloré. Le niveau de preuve GRADE (1 = fort, 2 = faible) n'est jamais réimprimé "
        "à côté de chaque encadré individuel dans la source — il se déduit du verbe de "
        "l'énoncé lui-même : « il faut (faire/ne pas faire) » = recommandation forte "
        "(GRADE 1) ; « il faut probablement (faire/ne pas faire) » = recommandation "
        "optionnelle (GRADE 2). Cette nuance reste donc directement lisible dans le texte "
        "verbatim de chaque encadré ci-dessous, sans codage GRADE synthétique superposé "
        "(risque d'erreur d'interprétation sur certains énoncés composites).",
        S_BODY), bg=BG_PANEL, border=TEAL))
    story.append(Spacer(1, 3*mm))
    story.append(info_panel(P(
        "<b>Divergence source-interne (disclosure) :</b> notre inventaire direct, item par "
        "item, dénombre <b>71 encadrés numérotés</b> au total (contre « 69 » annoncés par le "
        "résumé officiel), y compris les 4 encadrés des champs 1-3 (1.1, 2.1, 2.2, 3.1) que "
        "la méthodologie décrit pourtant comme de simples « points forts » non formellement "
        "cotés — ces 4 encadrés portent pourtant, dans le texte, un tag « Accord fort/faible » "
        "identique en format à la grande majorité des autres (une seule autre exception "
        "existe par ailleurs : l'encadré 9.3.1 ne porte aucun tag, traité ci-après comme "
        "absence de recommandation). Aucun sous-ensemble testé de notre compte ne "
        "correspond exactement au chiffre « 69 » du résumé. Chaque encadré est néanmoins "
        "reproduit intégralement ci-dessous ; la divergence porte uniquement sur le chiffre "
        "agrégé du résumé.",
        S_BODY_SM), bg=AMBER_LIGHT, border=AMBER))
    story.append(Spacer(1, 3*mm))
    story.append(section_bar("Champs 1-3 — Points forts (physiopathologie et évaluation)"))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("1.1", "Tout patient admis en réanimation pour une durée présumée supérieure à "
         "3 jours est à risque de dénutrition. Cette dernière augmente la morbi-mortalité "
         "(infection en particulier) et les durées de ventilation, de séjour et "
         "d'hospitalisation.", "Fort"),
        ("2.1", "Pour évaluer précisément la dépense énergétique d'un patient de "
         "réanimation, il faut utiliser la calorimétrie indirecte (méthode de référence, en "
         "tenant compte de ses limites d'utilisation) plutôt que les équations prédictives.", "Faible"),
        ("2.2", "Il faut probablement limiter le déficit énergétique précoce (dépenses moins "
         "apports cumulés) durant la première semaine pour réduire la morbi-mortalité en "
         "réanimation.", "Fort"),
        ("3.1", "Il faut probablement évaluer l'état nutritionnel des patients à l'admission "
         "au minimum en calculant l'IMC et en évaluant la perte de poids.", "Faible"),
    ], [10*mm, PAGE_W-2*MARGIN-10*mm-16*mm, 16*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(P("Prévalence de la dénutrition : 0,5 à 100 % selon la population et le "
                    "marqueur retenu ; augmente la morbidité infectieuse, le lâchage de "
                    "sutures, le recours à la trachéotomie, les durées de VM/séjour, et la "
                    "mortalité à l'hôpital et à 6 mois. Dépense énergétique : la calorimétrie "
                    "indirecte reste la référence mais peu généralisable en routine ; les "
                    "équations simples (âge/sexe/poids) ne sont pas fiables. Un déficit "
                    "énergétique précoce &gt;100 kcal/kg cumulés peut s'installer dès la "
                    "1ère semaine — le limiter plutôt que le corriger complètement est la "
                    "stratégie la plus raisonnable (sur/sous-compensation excessive = risque "
                    "de complications). Évaluation nutritionnelle : IMC et perte de poids "
                    "récente sont les marqueurs les plus simples ; circonférence brachiale "
                    "également prédictive ; les autres paramètres (biologiques, "
                    "bioimpédancemétrie, scores composites) ont une association inconstante "
                    "avec la morbi-mortalité.", S_NOTE))
    return story

def _section_champ4_5():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Champ 4 — Stratégie générale du support nutritionnel"))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("4.1", "Il faut administrer dans les 24 premières heures un support nutritionnel "
         "entéral aux patients dénutris ou jugés incapables de s'alimenter suffisamment dans "
         "les 3 jours après l'admission.", "Fort"),
        ("4.2", "Il faut utiliser la nutrition entérale (NE) plutôt que la nutrition "
         "parentérale (NP), en l'absence de contre-indication formelle.", "Fort"),
        ("4.3", "Il ne faut probablement pas utiliser la NE en amont d'une fistule digestive "
         "de haut débit, en cas d'occlusion intestinale, d'ischémie du grêle ou "
         "d'hémorragie digestive active.", "Fort"),
        ("4.4", "Il faut instaurer une NP de complément lorsque la NE n'atteint pas la cible "
         "calorique choisie au plus tard après 1 semaine de séjour en réanimation.", "Fort"),
        ("4.5", "En cas d'utilisation de calorimétrie indirecte, il ne faut probablement pas "
         "dépasser la dépense énergétique mesurée.", "Faible"),
        ("4.6", "En l'absence de calorimétrie indirecte, il faut probablement un objectif "
         "calorique total de 20-25 kcal/kg/j à la phase aiguë et 25-30 kcal/kg/j après "
         "stabilisation.", "Faible"),
        ("4.7", "En l'absence de calorimétrie indirecte, il faut tenir compte du poids "
         "habituel (ou à défaut du poids à l'admission) pour des IMC entre 20 et 35.", "Faible"),
        ("4.8", "Il faut répartir les apports caloriques non protéiques en 60-70 % "
         "glucidiques et 30-40 % lipidiques.", "Fort"),
        ("4.9", "Il faut apporter 1,2 à 1,5 g/kg/j de protéines.", "Fort"),
        ("4.10", "En cas de limitation ou arrêt thérapeutique, il faut discuter de "
         "l'opportunité du support nutritionnel.", "Fort"),
    ], [10*mm, PAGE_W-2*MARGIN-10*mm-16*mm, 16*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(P("Méta-analyses concordantes sur la réduction de morbi-mortalité par NE "
                    "précoce (protection de la trophicité digestive, limitation du déficit "
                    "énergétique) ; la NP est associée à un risque infectieux plus élevé. "
                    "Contre-indications fonctionnelles (ischémie mésentérique) à discuter au "
                    "cas par cas. En cas d'intolérance à la NE, ne pas chercher à compenser "
                    "trop vite/rigoureusement par NP — apports ajustés au déficit mesuré si "
                    "possible. Un excès d'apports caloriques (&gt;100 %) n'améliore pas la "
                    "balance protéique et peut être délétère (métabolisme hépatique, sevrage "
                    "ventilatoire) — la dépense mesurée excède rarement 30 kcal/kg/j sauf "
                    "traumatisé crânien ou brûlé.", S_NOTE))
    story.append(Spacer(1, 3*mm))
    story.append(section_bar("Champ 5 — Compléments oraux"))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("5.1", "Lorsque l'alimentation orale exclusive est insuffisante, il faut "
         "probablement ajouter des compléments nutritionnels oraux (CNO), en dehors des "
         "heures de repas.", "Faible"),
    ], [10*mm, PAGE_W-2*MARGIN-10*mm-16*mm, 16*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(P("Aucune étude n'a confirmé l'intérêt spécifique des CNO en réanimation ; "
                    "leur usage ne doit pas retarder la mise en route d'une NE chez un "
                    "patient ne couvrant pas ses besoins. Argumentaire (non gradé dans la "
                    "source) : il ne faut probablement pas prescrire de CNO spécifiques. "
                    "Utilisation envisageable au début "
                    "de la reprise alimentaire, dans le cadre de la rééducation à la "
                    "déglutition.", S_NOTE))
    return story

def _section_champ6():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Champ 6 — Nutrition entérale"))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("6.1", "Il ne faut pas mesurer le volume résiduel gastrique.", "Faible"),
        ("6.2", "Il faut probablement privilégier la sonde d'alimentation naso- ou "
         "oro-gastrique en première intention (simplicité, moindre coût).", "Fort"),
        ("6.3", "Il faut envisager l'administration de prokinétiques (métoclopramide et/ou "
         "érythromycine) pour améliorer l'apport calorique global en cas de trouble de la "
         "vidange gastrique.", "Fort"),
        ("6.4", "Il faut probablement envisager le site post-pylorique en cas de trouble "
         "persistant (malgré les prokinétiques) de la vidange gastrique.", "Faible"),
        ("6.5", "Il faut installer le patient en position semi-assise (&gt;30°) pendant la NE.", "Fort"),
        ("6.6", "Il faut instituer une stratégie multidisciplinaire formalisée de NE.", "Faible"),
        ("6.7", "Il faut probablement poser une gastrostomie lorsque la durée anticipée "
         "d'une NE dépasse 4 semaines.", "Faible"),
        ("6.8", "Il faut utiliser des mélanges polymériques pour débuter une NE.", "Fort"),
        ("6.9", "Il faut probablement réserver les mélanges semi-élémentaires à certaines "
         "situations digestives spécifiques (grêle court).", "Fort"),
        ("6.10", "Il ne faut pas utiliser de mélanges polymériques spécifiques (diabète, "
         "insuffisance respiratoire).", "Fort"),
        ("6.11", "Il faut administrer le mélange nutritif entéral de manière continue 24h/24 "
         "à l'aide d'une pompe.", "Faible"),
        ("6.12", "Il faut probablement adapter le débit d'administration en vue d'atteindre "
         "la cible nutritionnelle en moins de 48 heures.", "Fort"),
        ("6.13", "Il faut probablement utiliser les mélanges contenant des fibres extraites "
         "de la gomme de guar en cas de diarrhée.", "Fort"),
    ], [10*mm, PAGE_W-2*MARGIN-10*mm-16*mm, 16*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(P("Volume résiduel gastrique : sa mesure ne réduit pas le risque "
                    "d'inhalation mais réduit les apports par les interruptions qu'elle "
                    "impose. Sonde gastrique : simplicité, rapidité, coût limité, faible "
                    "risque mécanique ; sondes de petit calibre (silicone/polyuréthane) mieux "
                    "tolérées. Prokinétiques : érythromycine possiblement supérieure au "
                    "métoclopramide (synergie mais diarrhée majorée) ; métoclopramide "
                    "d'efficacité douteuse et risque d'HTIC chez le neurotraumatisé ; "
                    "tachyphylaxie après quelques jours (pas d'usage préventif). Site "
                    "post-pylorique : bénéfice potentiel sur les pneumopathies d'inhalation, "
                    "à pondérer par la complexité de pose, le coût et le besoin "
                    "d'endoscopie. Position semi-assise : réduit le RGO sur 5-6h, "
                    "recommandation systématique du fait de son innocuité (sauf trauma "
                    "rachidien/instabilité hémodynamique). Mélanges : polymériques "
                    "normocaloriques adaptés à la majorité des situations ; semi-élémentaires "
                    "réservés au grêle court/malabsorption ; pas de bénéfice démontré aux "
                    "mélanges spécifiques diabète/insuffisance respiratoire. Administration "
                    "continue à la pompe : meilleure tolérance (RGO, inhalation, diarrhée) "
                    "qu'en discontinu. Gomme de guar : seule fibre ayant démontré une "
                    "efficacité sur la diarrhée en association à un mélange polymérique.", S_NOTE))
    return story

def _section_champ7_8():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Champ 7 — Nutrition parentérale"))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("7.1", "Il faut utiliser les mélanges prêts à l'emploi plutôt que les flacons "
         "séparés.", "Fort"),
        ("7.2", "Il faut supplémenter le patient en vitamines et éléments traces en cas de "
         "nutrition parentérale.", "Fort"),
        ("7.3", "Il ne faut pas excéder un apport lipidique de 1,5 g/kg/j.", "Fort"),
        ("7.4", "Il faut administrer la nutrition parentérale en continu à l'aide d'une "
         "pompe électrique à régulation de débit, et éviter son administration cyclique.", "Fort"),
        ("7.5", "Il faut utiliser un abord veineux central en cas d'administration de "
         "solutés hyperosmolaires (&gt;850 mOsm/L).", "Fort"),
        ("7.6", "Il faut probablement privilégier l'administration de la nutrition "
         "parentérale sur une voie dédiée du cathéter veineux central.", "Faible"),
        ("7.7", "Il faut évoquer une complication métabolique ou un excès d'apport en cas "
         "d'anomalie(s) du bilan biologique (transaminases, bilirubine, gamma-GT, PAL, "
         "ionogramme, phosphore, glycémie, triglycérides).", "Fort"),
    ], [10*mm, PAGE_W-2*MARGIN-10*mm-16*mm, 16*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(P("Flacons séparés : davantage de manipulations = risque infectieux/"
                    "bactériémie accru. Apport lipidique : au-delà de 1,5 g/kg/j, capacité "
                    "d'oxydation dépassée = accumulation hépatique/réticulo-endothéliale "
                    "toxique. Administration continue : limite les variations "
                    "glycémiques/triglycéridémiques. Voie centrale dédiée : limite le risque "
                    "d'incompatibilité médicamenteuse et de contamination (non validé "
                    "spécifiquement en réanimation). Complications métaboliques à "
                    "rechercher systématiquement : syndrome de renutrition, stéatose "
                    "hépatique, cholestase, dysrégulation glycémique, hypertriglycéridémie.", S_NOTE))
    story.append(Spacer(1, 3*mm))
    story.append(section_bar("Champ 8 — Pharmaconutrition, vitamines, éléments traces"))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("8.1", "Si le patient a bénéficié d'une pharmaconutrition préopératoire (chirurgie "
         "carcinologique digestive), il faut la poursuivre en période postopératoire chez le "
         "patient préalablement dénutri.", "Fort"),
        ("8.2", "Il ne faut pas administrer de solution entérale enrichie en arginine chez "
         "le patient en sepsis sévère.", "Fort"),
        ("8.3", "Il faut probablement associer à la nutrition parentérale exclusive de la "
         "glutamine intraveineuse à la posologie d'au moins 0,35 g/kg/j (sous forme de "
         "dipeptide à ≥0,5 g/kg/j), pendant une période minimale de 10 jours.", "Faible"),
    ], [10*mm, PAGE_W-2*MARGIN-10*mm-16*mm, 16*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(P("Pharmaconutrition préopératoire (arginine, oméga-3, nucléotides) : "
                    "limite les complications postopératoires en chirurgie carcinologique "
                    "digestive, à poursuivre si alimentation artificielle postopératoire "
                    "nécessaire. Arginine en sepsis sévère : augmente les complications, "
                    "allonge le séjour, accroît la mortalité dans certaines études — à "
                    "éviter. Glutamine IV (NP exclusive) : les mélanges standards n'en "
                    "contiennent pas (instabilité) ; l'ajout sous forme de dipeptide réduit "
                    "les complications infectieuses, la durée de séjour et la mortalité.", S_NOTE))
    return story

def _section_champ9():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Champ 9 — Particularités liées au terrain"))
    story.append(Spacer(1, 2*mm))
    story.append(no_reco_panel("polytraumatisé — aucune spécificité nécessitant des "
                                "recommandations particulières dans ce champ."))
    story.append(Spacer(1, 2*mm))
    story.append(P("<b>Insuffisant rénal épuré (tous modes d'épuration extrarénale) :</b>", S_CELL_B))
    story.append(reco_table([
        ("9.2.1", "Il faut probablement majorer l'apport protéique quotidien du patient sous "
         "épuration extrarénale continue à 1,7-2 g/kg/j.", "Faible"),
        ("9.2.2", "Si une supplémentation en glutamine est indiquée, il faut probablement la "
         "majorer.", "Faible"),
        ("9.2.3", "Il faut probablement augmenter les apports en vitamines hydrosolubles "
         "(B1, C) et en éléments trace (sélénium, cuivre) chez les patients sous épuration "
         "extrarénale continue.", "Faible"),
    ], [12*mm, PAGE_W-2*MARGIN-12*mm-16*mm, 16*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(P("Pertes en acides aminés 10-17 % selon la technique ; glutamine "
                    "représentant 30 % de la perte azotée totale (~3,5 g/24h), effet "
                    "néphroprotecteur expérimental. Vitamine C : ne pas excéder 250 mg/j "
                    "(risque d'oxalose) ; en pratique, doubler la dose habituelle d'oligo-"
                    "éléments sous épuration continue.", S_NOTE))
    story.append(Spacer(1, 2*mm))
    story.append(P("<b>Insuffisant hépatique :</b>", S_CELL_B))
    story.append(no_reco_panel("apport calorique — aucune spécificité, en dehors du risque "
                                "hypoglycémique accru nécessitant 2 à 3 g/kg/j de glucose."))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("9.3.2", "Il ne faut probablement pas diminuer l'apport d'acides aminés chez "
         "l'insuffisant hépatique aigu, sauf transitoirement en cas d'encéphalopathie "
         "et/ou d'hyperammoniémie.", "Fort"),
    ], [12*mm, PAGE_W-2*MARGIN-12*mm-16*mm, 16*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(P("<b>SDRA :</b>", S_CELL_B))
    story.append(reco_table([
        ("9.4.1", "Il ne faut pas interrompre systématiquement la nutrition entérale lors de "
         "la mise en décubitus ventral.", "Fort"),
    ], [12*mm, PAGE_W-2*MARGIN-12*mm-16*mm, 16*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(no_reco_panel("sepsis et syndrome de défaillance multiviscérale — aucune "
                                "spécificité nécessitant des recommandations particulières "
                                "dans ce champ."))
    story.append(Spacer(1, 2*mm))
    story.append(P("<b>Obèse</b> (poids idéal théorique, PIT (kg) = 25 × [taille (m)]²) :", S_CELL_B))
    story.append(reco_table([
        ("9.6.1", "Il ne faut pas calculer les apports en fonction du poids réel.", "Fort"),
        ("9.6.2", "Il faut probablement calculer les apports nutritionnels en fonction du "
         "poids ajusté (PIT + 1/4 × [poids réel − PIT]).", "Faible"),
        ("9.6.3", "En tenant compte de ce poids ajusté, il faut probablement apporter "
         "20 kcal/kg/j dont 2 g/kg/j de protéines.", "Faible"),
    ], [12*mm, PAGE_W-2*MARGIN-12*mm-16*mm, 16*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(P("<b>Dénutrition grave et syndrome de renutrition :</b>", S_CELL_B))
    story.append(reco_table([
        ("9.7.1", "En cas de dénutrition sévère et/ou de jeûne prolongé &gt;1 semaine, il "
         "faut probablement débuter la nutrition artificielle à 10 kcal/kg/j, puis "
         "augmenter progressivement selon la tolérance.", "Faible"),
        ("9.7.2", "Il faut supplémenter systématiquement en vitamines (B surtout), éléments "
         "trace et phosphore.", "Fort"),
        ("9.7.3", "En cas de dénutrition sévère et/ou de jeûne prolongé de plus d'une "
         "semaine, il faut doser la phosphatémie au moins 1×/jour ; suspecter un syndrome "
         "de renutrition si hypophosphatémie — dans ce cas, stopper temporairement "
         "l'alimentation et corriger la phosphatémie.", "Fort"),
    ], [12*mm, PAGE_W-2*MARGIN-12*mm-16*mm, 16*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(P("Risques du syndrome de renutrition : troubles hydroélectrolytiques "
                    "(hypophosphatémie, hypokaliémie, hypomagnésémie), déficit en vitamines "
                    "hydrosolubles — complications cardiaques et neuromusculaires "
                    "potentiellement létales, justifiant une montée progressive avec "
                    "surveillance au moins quotidienne.", S_NOTE))
    return story

def _section_champ9_brule():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Champ 9 (suite) — Patient gravement brûlé"))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("9.8.1", "Les besoins énergétiques du patient gravement brûlé sont fortement "
         "augmentés mais variables dans le temps, proportionnels à la surface corporelle "
         "atteinte, mais plafonnant à partir d'une SCB de 60 %.", "Fort"),
        ("9.8.2", "En l'absence de calorimétrie indirecte, il faut déterminer les besoins "
         "énergétiques avec la formule de Toronto (adulte) — les formules fixes conduisent "
         "à une sous/surestimation.", "Fort"),
        ("9.8.3", "Il faut utiliser des mesures non nutritionnelles pour atténuer "
         "l'hypermétabolisme/hypercatabolisme (température ambiante, chirurgie d'excision "
         "précoce, bêtabloquants non sélectifs, oxandrolone). Contrairement à l'adulte, il "
         "faut substituer en rh-GH les enfants brûlés à plus de 60 %.", "Faible"),
        ("9.8.4", "Il faut probablement situer les besoins protéiques à 1,5-2 g/kg/j "
         "(respecter une proportion de l'apport énergétique total chez l'enfant).", "Fort"),
        ("9.8.5", "Il faut probablement supplémenter en glutamine ou en alpha-cétoglutarate "
         "d'ornithine.", "Faible"),
        ("9.8.6", "Il ne faut probablement pas supplémenter en arginine.", "Faible"),
        ("9.8.7", "Il faut probablement associer une supplémentation en zinc, cuivre et "
         "sélénium.", "Faible"),
    ], [12*mm, PAGE_W-2*MARGIN-12*mm-16*mm, 16*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(P("Hypermétabolisme maximal les 2 premières semaines, s'atténuant selon la "
                    "gravité. Bêtabloquants non sélectifs : effets surtout démontrés chez "
                    "l'enfant (réduction hormones de stress/cytokines/hyper-catabolisme). "
                    "Oxandrolone 10 mg/12h (0,1 mg/kg/12h chez l'enfant) : diminuerait perte "
                    "de poids, catabolisme, délai de cicatrisation, durée de séjour et "
                    "mortalité. rh-GH chez l'enfant (0,05-0,2 mg/kg/j) : accélérerait la "
                    "cicatrisation des sites donneurs. Protéines : au-delà de 2,2 g/kg/j "
                    "(adulte) ou 3 g/kg/j (enfant), pas de bénéfice supplémentaire "
                    "démontré. Alpha-cétoglutarate d'ornithine : 30 g/j en 2-3 bolus, "
                    "réduirait les délais de cicatrisation ; arginine non recommandable en "
                    "l'absence de données de posologie/durée établies. Zinc/cuivre/sélénium : "
                    "pertes majeures par les exsudats tant que les plaies sont ouvertes — "
                    "substitution IV 8j (SCB 20-40 %), 15j (40-60 %), 30j (&gt;60 %) ; voie "
                    "entérale inefficace (compétition cuivre/zinc pour le même "
                    "transporteur).", S_NOTE))
    story.append(Spacer(1, 3*mm))
    cw = PAGE_W - 2*MARGIN
    story.append(KeepTogether(simple_table(
        ["Tableau 1 — Besoins énergétiques du brûlé grave (en l'absence de calorimétrie)", "Formule"],
        [
            ["Adulte — formule de Toronto (kcal/j)", "4343 + (10,5 × %SCB) + (0,23 × apport "
             "calorique) + (0,84 × Harris-Benedict) + (114 × t° corporelle) − (4,5 × jour "
             "post-brûlure)"],
            ["Fille 3-10 ans — Schoffield", "(16,97 × poids kg) + (1,618 × taille cm) + 371,2"],
            ["Garçon 3-10 ans — Schoffield", "(19,6 × poids kg) + (1,033 × taille cm) + 414,9"],
            ["Fille 10-18 ans — Schoffield", "(8,365 × poids kg) + (4,65 × taille cm) + 200"],
            ["Garçon 10-18 ans — Schoffield", "(16,25 × poids kg) + (1,372 × taille cm) + 515,5"],
        ],
        [cw*0.42, cw*0.58])))
    return story

def _section_champ10():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Champ 10 — Particularités pédiatriques"))
    story.append(Spacer(1, 2*mm))
    story.append(P("<b>Évaluation de l'état nutritionnel de l'enfant :</b>", S_CELL_B))
    story.append(reco_table([
        ("10.1.1", "Il faut dépister la dénutrition protéino-calorique à l'admission et "
         "surveiller sa survenue en cours de séjour.", "Fort"),
        ("10.1.2", "Il faut rechercher une évolution récente des courbes de croissance "
         "(cassure Poids/Taille/IMC) ou une perte de poids récente.", "Faible"),
        ("10.1.3", "Il faut mesurer poids, taille, périmètre crânien (PC) et périmètre "
         "brachial (PB) pour calculer les indices pédiatriques de dénutrition (rapport "
         "poids-taille, taille/âge, IMC, PB/PC chez les &lt;4 ans).", "Fort"),
        ("10.1.4", "Il faut probablement estimer la taille des patients &gt;1 mètre, alités, "
         "rétractés ou déformés par la mesure de la longueur de l'ulna.", "Faible"),
    ], [14*mm, PAGE_W-2*MARGIN-14*mm-16*mm, 16*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(P("Prévalence de la dénutrition à l'admission en réanimation pédiatrique : "
                    "16-24 % (Europe). Formule d'estimation de la taille par l'ulna : "
                    "T(cm,M) = 4,605×U + 1,308×A + 28,003 ; T(cm,F) = 4,459×U + 1,315×A + "
                    "31,485 (U = longueur ulna en cm, A = âge en années).", S_NOTE))
    story.append(Spacer(1, 2*mm))
    story.append(P("<b>Besoins énergétiques et macronutriments :</b>", S_CELL_B))
    story.append(reco_table([
        ("10.2.1", "Il faut fournir au moins les apports caloriques (100-90 kcal/kg/j "
         "&lt;1 an, nouveau-né exclu ; 90-75 entre 1-6 ans ; 75-60 entre 7-12 ans ; 60-30 "
         "entre 13-18 ans) et protidiques (2-3 g/kg/j &lt;2 ans, nouveau-né exclu ; 1,5-2 "
         "entre 2-12 ans ; 1,5 entre 13-18 ans) adaptés au poids et à l'âge.", "Fort"),
        ("10.2.2", "Il faut probablement majorer les apports caloriques et protidiques en "
         "cas d'augmentation importante du travail respiratoire.", "Faible"),
        ("10.2.3", "Il faut fournir des apports lipidiques couvrant 30-40 % des apports "
         "caloriques totaux ; il ne faut probablement pas dépasser 4 g/kg/j.", "Faible"),
        ("10.2.4", "En situation normale d'hydratation, il faut fournir les apports "
         "liquidiens suivants : 120-150 mL/kg/j (&lt;1 an, nouveau-né exclu) ; 80-120 "
         "(1-2 ans) ; 80-100 (3-5 ans) ; 60-80 (6-12 ans) ; 50-70 (13-18 ans), avec facteur "
         "correctif selon l'état d'hydratation.", "Fort"),
        ("10.2.5", "Il faut assurer les apports recommandés en vitamines et éléments trace "
         "en fonction de l'âge — utiliser des produits spécifiquement destinés à l'enfant.", "Fort"),
    ], [14*mm, PAGE_W-2*MARGIN-14*mm-16*mm, 16*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(P("La calorimétrie indirecte (référence) est peu disponible en routine "
                    "pédiatrique ; utiliser les tables d'apports conseillés (ANC, "
                    "www.anses.fr) selon sexe/âge/poids. Capacité maximale d'oxydation des "
                    "lipides atteinte pour 3-4 g/kg/j chez le nourrisson/enfant. Apports "
                    "glucidiques (non gradés dans la source) : couvrant 50-60 % des apports "
                    "caloriques totaux. Produits adultes non adaptés (acides gras, acides "
                    "aminés essentiels, vitamines, oligo-éléments).", S_NOTE))
    story.append(Spacer(1, 2*mm))
    story.append(P("<b>Stratégie générale du support nutritionnel pédiatrique :</b>", S_CELL_B))
    story.append(reco_table([
        ("10.3.1", "Il faut nourrir tous les enfants hospitalisés en réanimation.", "Fort"),
        ("10.3.2", "Il faut utiliser la voie entérale en première intention chez l'enfant "
         "présentant un tube digestif fonctionnel.", "Fort"),
        ("10.3.3", "Il faut probablement instaurer une nutrition parentérale entre le 3e et "
         "le 5e jour pour atteindre l'objectif calorique, en complément ou exclusivement.", "Fort"),
        ("10.3.4", "Il faut utiliser des solutés de nutrition entérale et parentérale "
         "spécifiquement destinés à l'enfant.", "Fort"),
        ("10.3.5", "Il faut augmenter les apports énergétiques de manière progressive, en "
         "particulier les apports glucosés parentéraux (incrémentation de 2 g/kg/j).", "Faible"),
    ], [14*mm, PAGE_W-2*MARGIN-14*mm-16*mm, 16*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(P("Enfants dénutris = morbi-mortalité plus élevée ; réserves faibles et "
                    "rapidement épuisées en situation d'agression. NP chez l'enfant à "
                    "conduire selon les recommandations de l'ESPGHAN. Montée progressive sur "
                    "3-5 jours, tenant compte de la rupture du cycle entéro-insulaire et de "
                    "la capacité maximale d'oxydation du glucose.", S_NOTE))
    story.append(Spacer(1, 3*mm))
    cw = PAGE_W - 2*MARGIN
    story.append(KeepTogether(simple_table(
        ["Tableau 2 — Apports recommandés en glucose parentéral (g/kg/j)", "j1", "j2", "j3", "j4"],
        [
            ["> 3 kg", "10", "14", "16", "18"],
            ["3-10 kg", "8", "12", "14", "16-18"],
            ["10-15 kg", "6", "8", "10", "12-14"],
            ["15-20 kg", "4", "6", "8", "10-12"],
            ["20-30 kg", "4", "6", "8", "< 12"],
            ["> 30 kg", "3", "5", "8", "< 10"],
        ],
        [cw*0.32, cw*0.17, cw*0.17, cw*0.17, cw*0.17])))
    return story

def _section_synthese():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Synthèse et messages clés"))
    story.append(Spacer(1, 2*mm))
    story.append(P(
        "• Tout patient de réanimation à séjour présumé &gt;3 jours est à risque de "
        "dénutrition — dépistage à l'admission (IMC, perte de poids) et surveillance "
        "continue.<br/>"
        "• Nutrition entérale précoce (&lt;24-72h) en première intention chez le patient "
        "dénutri ou incapable de s'alimenter, sauf contre-indication formelle (fistule haut "
        "débit, occlusion, ischémie du grêle, hémorragie digestive active) ; NP de "
        "complément si cible non atteinte à 1 semaine, sans chercher à compenser trop "
        "vite.<br/>"
        "• Objectifs : 20-25 kcal/kg/j en phase aiguë puis 25-30 après stabilisation (sans "
        "calorimétrie), 1,2-1,5 g/kg/j de protéines ; limiter plutôt que corriger "
        "complètement le déficit énergétique précoce.<br/>"
        "• NE : sonde gastrique en 1ère intention, position semi-assise systématique, "
        "administration continue à la pompe, mélanges polymériques standards sauf "
        "indication spécifique (grêle court), pas de mesure du résidu gastrique, "
        "prokinétiques puis site post-pylorique si trouble de vidange persistant.<br/>"
        "• NP : mélanges prêts à l'emploi, supplémentation systématique en vitamines/"
        "oligo-éléments, lipides ≤1,5 g/kg/j, administration continue ; abord veineux "
        "central si osmolarité &gt;850 mOsm/L, et voie dédiée du cathéter central "
        "probablement à privilégier (recommandations distinctes).<br/>"
        "• Terrains spécifiques : majoration protéique et vitaminique sous épuration "
        "extrarénale continue ; poids ajusté chez l'obèse ; montée très progressive "
        "(10 kcal/kg/j) avec surveillance quotidienne de la phosphatémie en cas de "
        "dénutrition sévère/jeûne prolongé (risque de syndrome de renutrition) ; formule de "
        "Toronto/Schoffield et supplémentation en oligo-éléments prolongée chez le brûlé "
        "grave.<br/>"
        "• Pédiatrie : nourrir systématiquement tout enfant admis, voie entérale en 1ère "
        "intention, produits et solutés spécifiquement pédiatriques, apports "
        "caloriques/protidiques/hydriques dégressifs avec l'âge (cf. tableaux).",
        S_BODY))
    story.append(Spacer(1, 5*mm))

    story.append(section_bar("Sources et traçabilité", color=GREY))
    story.append(Spacer(1, 2*mm))
    story.append(P(
        "<b>Document source :</b> « Nutrition artificielle en réanimation » — "
        "Recommandations Formalisées d'Experts communes SFAR-SRLF-SFNEP. Ann Fr Anesth "
        "Reanim 2014;33:202-218, recommandations validées en février 2013. 33 experts, "
        "3 présidents (J-Y. Lefrant/SFAR, D. Hurel/SRLF, N.J. Cano/SFNEP), 3 pilotes "
        "d'experts.", S_SOURCE))
    story.append(Spacer(1, 1.5*mm))
    story.append(P("<b>Couverture :</b> les 71 encadrés numérotés identifiés dans le texte "
                    "source (1.1 à 10.3.5, répartis sur 10 champs) sont reproduits "
                    "intégralement, y compris les 3 items d'absence de spécificité explicite "
                    "(polytraumatisé, insuffisance hépatique — volet calorique, sepsis/"
                    "défaillance multiviscérale) et les 2 tableaux numériques (besoins "
                    "énergétiques du brûlé, apports glucosés parentéraux pédiatriques).", S_SOURCE))
    story.append(Spacer(1, 1.5*mm))
    story.append(P("<b>Divergence d'agrégat (disclosure) :</b> le résumé officiel de la "
                    "source annonce « 69 recommandations » issues des « six derniers champs » "
                    "— notre inventaire direct dénombre 71 encadrés numérotés au total sur "
                    "l'ensemble des 10 champs, sans qu'aucun sous-ensemble testé ne "
                    "corresponde exactement à 69. La méthodologie de la source décrit par "
                    "ailleurs les champs 1-3 comme non formellement cotés (« points forts »), "
                    "alors que leurs 4 encadrés portent en pratique un tag « Accord fort/"
                    "faible » identique en format à la quasi-totalité des autres (seule "
                    "exception par ailleurs : l'encadré 9.3.1, sans tag, traité comme "
                    "absence de recommandation) — divergence non "
                    "réconciliée, disclosée telle quelle.", S_SOURCE))
    story.append(Spacer(1, 1.5*mm))
    story.append(P("<b>Convention de grading propre à cette source :</b> chaque encadré "
                    "porte un unique tag imprimé « (Accord fort) » ou « (Accord faible) » "
                    "(force du consensus), reproduit ici tel quel comme chip coloré. Le "
                    "niveau de preuve GRADE (fort=« il faut… » / faible=« il faut "
                    "probablement… ») n'est jamais réimprimé individuellement dans la "
                    "source — il reste directement lisible dans le verbe de chaque énoncé "
                    "verbatim, sans codage GRADE synthétique superposé ici (risque "
                    "d'erreur d'interprétation sur les énoncés composites, ex. 9.8.3, "
                    "10.2.3).", S_SOURCE))
    story.append(Spacer(1, 3*mm))
    story.append(info_panel(P(
        "<b>Avertissement :</b> ce document est une fiche de synthèse indépendante, produite "
        "pour un usage d'aide-mémoire. Il reprend l'intégralité des recommandations de la "
        "RFE mais ne remplace pas le texte intégral et n'est ni édité ni validé par la "
        "SFAR/SRLF/SFNEP. En cas de doute, se référer au texte intégral, aux recommandations "
        "ultérieures et/ou à un avis spécialisé.",
        S_BODY_SM), bg=GREY_LIGHT, border=GREY))
    return story

SECTIONS = [
    ("Introduction & Points forts (champs 1-3)", _section_intro),
    ("Champ 4 — Stratégie générale & Champ 5 — Compléments oraux", _section_champ4_5),
    ("Champ 6 — Nutrition entérale", _section_champ6),
    ("Champ 7 — Nutrition parentérale & Champ 8 — Pharmaconutrition", _section_champ7_8),
    ("Champ 9 — Particularités liées au terrain", _section_champ9),
    ("Champ 9 (suite) — Patient gravement brûlé", _section_champ9_brule),
    ("Champ 10 — Particularités pédiatriques", _section_champ10),
    ("Synthèse, sources & traçabilité", _section_synthese),
]

def _make_doc():
    return SimpleDocTemplate(OUT, pagesize=A4,
                              leftMargin=MARGIN, rightMargin=MARGIN,
                              topMargin=32*mm, bottomMargin=16*mm,
                              title="Fiche SFAR-SRLF-SFNEP 2014 - Nutrition artificielle en reanimation",
                              author="Synthèse indépendante (source SFAR/SRLF/SFNEP)")

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
    import pypdf
    doc = _make_doc()
    doc.build(story_flowables, onFirstPage=_silent_page, onLaterPages=_silent_page)
    return len(pypdf.PdfReader(OUT).pages)

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
