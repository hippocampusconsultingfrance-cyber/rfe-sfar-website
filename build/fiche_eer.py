# -*- coding: utf-8 -*-
"""
Fiche de synthese - RFE sous l'egide de la SRLF, avec SFAR/GFRUP/SFD, "Epuration extrarenale
en reanimation adulte et pediatrique". Publiee Reanimation 2014 (DOI 10.1007/s13546-014-0917-6).
18 experts + coordonnateur + 2 organisateurs. Methode GRADE pour l'analyse de la litterature ;
cotation collective methode RAND/UCLA (et non Delphi/GRADE-grid comme les autres RFE du
corpus) : mediane 1-3 = desaccord, 4-6 = indecision, 7-9 = accord ; "fort" si IC95% des
cotations reste dans une seule des 3 zones, "faible" s'il empiete sur deux zones. 2 tours de
cotation.

MEME PARTICULARITE DE GRADING QUE LA FICHE NUTRITION (fiche 31) : aucun tag numerique
"GRADE 1+/1-/2+/2-" n'est jamais imprime a cote d'un item individuel. Chaque item porte
uniquement "Accord fort" ou "Accord faible" (force du consensus RAND/UCLA), parfois precede de
"(Avis d'experts)" lorsque la litterature etait insuffisante pour une gradation formelle (les
items SANS "(Avis d'experts)" sont donc bases sur une analyse de litterature graduee GRADE, mais
sans tag numerique reimprime). Meme decision methodologique que la fiche nutrition : chip
"Fort"/"Faible" reproduisant le tag reellement imprime, via extension locale (non partagee) du
dict GRADE_COLORS - deja etabli comme pattern reutilisable. La presence ou non de "(avis
d'experts)" est preservee verbatim dans le texte de chaque recommandation.

ECHELLE : 78 recommandations numerotees au total sur 4 champs (1 a 4.3.3.3), TOUTES verifiees
directement depuis le "Tableau recapitulatif" propre de la source (pages 16-19 du texte extrait,
juste avant les references) - la source elle-meme fournit une reprise compacte et verbatim de
CHAQUE recommandation individuelle, utilisee ici comme source canonique pour le texte de chaque
ligne de reco_table (plutot que retranscrite depuis les paragraphes d'argumentaire disperses
des pages 1-15, qui restent la source des notes d'evidence condensees). Aucun ecart de compte
agrege trouve cette fois : la source ne fournit pas de chiffre-resume du type "N recommandations"
dans son texte (contrairement aux fiches precedentes de ce corpus), donc pas de disclosure de
divergence necessaire ici - premiere fiche du corpus dans ce cas precis.

Champ 2.3 (Anticoagulation) et Champ 4.3 (Gestion du circuit) ont une structure hierarchique a
trois niveaux (ex. 2.3.1 "Chez le patient a haut risque hemorragique" -> 2.3.1.1-2.3.1.4) -
preservee ici via des sous-titres de sous-groupe avant chaque bloc de reco_table correspondant.
Champ 4.3 (15 items, checklist procedurale de branchement/pendant/debranchement) est en tres
grande partie du texte purement descriptif sans argumentaire individuel : la source elle-meme
indique explicitement "Les recommandations concernant la gestion pratique des seances d'EER
sont toutes des avis d'experts fondes sur des regles de bonnes pratiques. Aucune publication
scientifique n'en a evalue l'impact." - note unique appliquee a tout le champ 4.3 plutot qu'une
note par item.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from style import *
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.units import mm

GRADE_COLORS["Fort"] = (GREEN, WHITE)
GRADE_COLORS["Faible"] = (TEAL, WHITE)

OUT = "/private/tmp/claude-501/-Users-macbook-Downloads-claude/65498e3e-5ddf-47a6-b100-3ac535d1faa0/scratchpad/rfe_sfar/output/Fiche_SRLF_Epuration_Extrarenale_2014.pdf"

SOURCE_TXT = ("Source : Recommandations Formalisées d'Experts sous l'égide de la SRLF, avec "
              "la participation de la SFAR, du GFRUP et de la SFD « Épuration extrarénale en "
              "réanimation adulte et pédiatrique » — Réanimation 2014, DOI "
              "10.1007/s13546-014-0917-6. Fiche de synthèse non officielle : se référer au "
              "texte intégral.")

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
    return info_panel(P("<b>Absence de recommandation</b> — " + text, S_BODY_SM), bg=GREY_LIGHT, border=GREY)

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
    header_band(canvas, doc, "SRLF, avec SFAR/GFRUP/SFD — RFE 2014 — FICHE DE SYNTHÈSE",
                "Épuration extrarénale en réanimation",
                page_title, icon_fn=lambda c,x,y: icon_kidney(c, x, y, 13*mm), color=NAVY)
    footer_band(canvas, doc, SOURCE_TXT, f"Page {doc.page} / {TOTAL_PAGES['n']}")

# ---------------------------------------------------------------------------
def _section_intro():
    story = []
    story.append(Spacer(1, 3*mm))
    story.append(info_panel(P(
        "<b>Objectif :</b> RFE sous l'égide de la SRLF, avec la participation de la SFAR, du "
        "GFRUP (pédiatrie) et de la SFD (Société francophone de dialyse) — 18 experts + "
        "coordonnateur + 2 organisateurs. 4 champs : (1) critères d'initiation de l'EER, "
        "(2) aspects techniques (voies d'abord, membranes, anticoagulation, eau osmosée), "
        "(3) aspects pratiques (choix de méthode, dialyse péritonéale, dose de dialyse, "
        "réglages), (4) sécurisation des procédures.<br/><br/>"
        "<b>Méthodologie de cotation — particularité de cette source :</b> analyse de la "
        "littérature selon la méthode GRADE, mais cotation collective selon la méthode "
        "RAND/UCLA (et non le GRADE grid des autres RFE du corpus) : chaque expert cote de "
        "1 (désaccord complet) à 9 (accord complet) ; médiane 1-3 = désaccord, 4-6 = "
        "indécision, 7-9 = accord ; qualifié de « fort » si l'intervalle de confiance des "
        "cotations reste dans une seule des 3 zones, « faible » s'il empiète sur deux zones. "
        "2 tours de cotation.<br/><br/>"
        "<b>78 recommandations</b> numérotées au total sur les 4 champs, chacune portant un "
        "tag « Accord fort » ou « Accord faible », parfois précédé de « (Avis d'experts) » "
        "lorsque la littérature était insuffisante pour une analyse graduée — cette mention, "
        "lorsqu'elle existe dans la source, est conservée verbatim dans le texte de chaque "
        "recommandation ci-dessous.",
        S_BODY), bg=BG_PANEL, border=TEAL))
    story.append(Spacer(1, 3*mm))
    story.append(info_panel(P(
        "<b>Contexte :</b> prévalence de l'insuffisance rénale aiguë (IRA) en réanimation "
        "~40 %, recours à l'EER dans un peu moins de 20 % des cas, avec de grandes "
        "disparités entre services (3 à 36 % selon le groupe FINNAKI) sans différence de "
        "mortalité associée. Les dernières recommandations SRLF sur l'épuration continue "
        "dataient de 1997.",
        S_BODY_SM), bg=GREY_LIGHT, border=GREY))
    return story

def _section_champ1():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Champ 1 — Critères d'initiation de l'EER"))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("1.1", "Il faut initier sans délai l'EER dans les situations mettant en jeu le "
         "pronostic vital (hyperkaliémie, acidose métabolique, syndrome de lyse, œdème "
         "pulmonaire réfractaire au traitement médical). (Avis d'experts)", "Fort"),
        ("1.2", "Les données disponibles sont insuffisantes pour définir le délai optimal "
         "avant instauration de l'EER en dehors des situations mettant en jeu le pronostic "
         "vital. (Avis d'experts)", "Fort"),
        ("1.3", "Chez l'enfant, il faut probablement considérer la surcharge hydrosodée de "
         "plus de 10 % et très probablement de plus de 20 % parmi les critères "
         "d'instauration d'une EER. (Avis d'experts)", "Faible"),
        ("1.4", "Il faut considérer « précoce » l'initiation d'une EER, au stade KDIGO 2 ou "
         "dans les 24 heures suivant l'apparition d'une IRA dont la réversibilité semble peu "
         "probable. (Avis d'experts)", "Faible"),
        ("1.5", "Il faut considérer « tardive » l'initiation de l'EER à plus de 48 heures de "
         "la survenue d'une IRA KDIGO 3 ou lors de l'apparition d'une situation mettant en "
         "jeu le pronostic vital et en rapport avec l'IRA. (Avis d'experts)", "Faible"),
    ], [11*mm, PAGE_W-2*MARGIN-11*mm-16*mm, 16*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(P("Les 3 essais randomisés sur l'initiation précoce montrent des résultats "
                    "discordants (absence de bénéfice, effet délétère, ou bénéfice net selon "
                    "l'étude) ; une méta-analyse suggère un bénéfice mais le faible niveau de "
                    "preuve des études, l'hétérogénéité des populations et des définitions "
                    "empêchent toute conclusion définitive — d'où l'absence de "
                    "recommandation sur le délai optimal hors urgence vitale. Chez l'enfant, "
                    "une surcharge hydrique &gt;20 % est associée à une surmortalité majeure "
                    "(OR 8,3) ; entre 10-20 %, le lien est moins net (significatif "
                    "uniquement si &gt;3 défaillances d'organe associées).", S_NOTE))
    return story

def _section_champ2a():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Champ 2.1 — Voies d'abord"))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("2.1.1", "Il faut éviter le recours au site sous-clavier. (Avis d'experts)", "Fort"),
        ("2.1.2", "Il faut considérer les sites veineux fémoraux et jugulaires internes "
         "droits comme équivalents en termes de complications infectieuses.", "Fort"),
        ("2.1.3", "Il faut probablement utiliser le site jugulaire interne pour diminuer le "
         "risque infectieux lié au cathéter pour les patients avec un IMC &gt;28 kg/m².", "Fort"),
        ("2.1.4", "Il faut considérer les sites veineux fémoraux et jugulaires internes "
         "droits comme équivalents en termes de risque de dysfonction de cathéter.", "Faible"),
        ("2.1.5", "Il faut probablement réserver le site jugulaire interne gauche comme "
         "troisième choix.", "Fort"),
        ("2.1.6", "Chez l'enfant, il faut probablement préférer l'abord jugulaire interne "
         "droit à l'abord fémoral pour l'enfant de moins de 20 kg (ou si le cathéter est "
         "&lt;10F).", "Faible"),
        ("2.1.7", "Il faut adapter la taille des cathéters à la morphologie et au poids de "
         "l'enfant : 3-6 kg → 6,5-7 F ; 6-10 kg → 8 F ; 10-20 kg → 8-10 F ; 20-30 kg → "
         "10 F ; &gt;30 kg → 11-13 F. (Avis d'experts)", "Fort"),
        ("2.1.8", "En site fémoral, il faut utiliser des cathéters de diamètre &gt;12 F et "
         "de longueur ≥24 cm. (Avis d'experts)", "Fort"),
        ("2.1.9", "Il faut utiliser l'échoguidage pour la mise en place des cathéters d'EER "
         "par voie jugulaire interne.", "Fort"),
        ("2.1.10", "Il faut probablement utiliser l'échoguidage pour la mise en place des "
         "cathéters d'EER par voie fémorale.", "Faible"),
        ("2.1.11", "Il faut procéder à l'ablation des cathéters d'EER dès que ceux-ci ne "
         "sont plus nécessaires. (Avis d'experts)", "Fort"),
        ("2.1.12", "Il ne faut pas utiliser les fistules artérioveineuses en l'absence "
         "d'expertise dans le domaine. (Avis d'experts)", "Fort"),
    ], [13*mm, PAGE_W-2*MARGIN-13*mm-16*mm, 16*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(P("Site sous-clavier évité par extrapolation des données IRC (risque de "
                    "sténose veineuse compromettant une future fistule artérioveineuse). "
                    "Seule étude randomisée fémoral vs. jugulaire (Cathédia) : pas de "
                    "différence de colonisation globale (40,8 vs 35,7‰ jours-cathéters) ni "
                    "de bactériémie (1,5 vs 2,3‰), sauf chez les patients IMC&gt;28 "
                    "(sur-risque fémoral) ; dysfonction de cathéter comparable entre sites, "
                    "sauf risque accru en jugulaire interne gauche. Échoguidage jugulaire : "
                    "méta-analyse 2011 (7 études, 830 cathéters) — réduction du risque "
                    "d'échec de pose (RR 0,12) et d'échec au 1er essai (RR 0,4). "
                    "Échoguidage fémoral : 1 étude randomisée (110 cathéters) — succès "
                    "98,2 % vs. 80 % par repérage anatomique (p=0,002).", S_NOTE))
    story.append(Spacer(1, 3*mm))
    story.append(section_bar("Champ 2.2 — Membranes"))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("2.2.1", "Il ne faut probablement pas utiliser de membranes en cellulose non "
         "modifiée (cuprophane) pour la prise en charge des patients en IRA.", "Fort"),
        ("2.2.2", "Il faut utiliser des membranes à haute perméabilité hydraulique "
         "(coefficient d'ultrafiltration élevé) pour des techniques convectives d'épuration "
         "(hémofiltration). (Avis d'experts)", "Fort"),
        ("2.2.3", "En hémodialyse intermittente, il ne faut pas utiliser des membranes à "
         "haute perméabilité hydraulique en l'absence de dialysat ultrapure. (Avis "
         "d'experts)", "Fort"),
        ("2.2.4", "Il ne semble pas utile d'utiliser une membrane à haute porosité (cut-off "
         "élevé) ou à forte capacité d'adsorption pour le traitement du choc septique.", "Fort"),
        ("2.2.5", "Il ne faut probablement pas utiliser de membrane couverte par l'héparine "
         "ou captant l'héparine dans le but de diminuer l'anticoagulation du circuit.", "Fort"),
    ], [13*mm, PAGE_W-2*MARGIN-13*mm-16*mm, 16*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(P("Cuprophane : méta-analyses suggérant une tendance à la surmortalité, à "
                    "la limite de la significativité (moins de 650 patients étudiés au "
                    "total) — pas de sur-risque avec l'acétate de cellulose. Membranes à "
                    "haute porosité/adsorption : aucune étude comparative de mortalité "
                    "disponible dans le choc septique — pas de recommandation de membrane "
                    "spécifique. Membranes héparinées : études contradictoires, intérêt non "
                    "démontré.", S_NOTE))
    return story

def _section_champ2b():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Champ 2.3 — Anticoagulation"))
    story.append(Spacer(1, 2*mm))
    story.append(P("<b>Patient à haut risque hémorragique ou coagulopathie :</b>", S_CELL_B))
    story.append(reco_table([
        ("2.3.1.1", "En épuration intermittente, il faut probablement ne pas faire "
         "d'anticoagulation systémique.", "Faible"),
        ("2.3.1.2", "En épuration continue, il faut probablement privilégier, sauf "
         "contre-indication, le recours à l'anticoagulation régionale au citrate par "
         "rapport à l'absence d'anticoagulation.", "Fort"),
        ("2.3.1.3", "En épuration continue, il faut probablement privilégier l'absence "
         "d'anticoagulation s'il existe une contre-indication au citrate. (Avis d'experts)", "Faible"),
        ("2.3.1.4", "Chez l'enfant, il est possible de réaliser l'EER continue sans "
         "anticoagulation ou par anticoagulation régionale au citrate, le choix étant guidé "
         "par l'expérience de l'équipe. (Avis d'experts)", "Fort"),
    ], [15*mm, PAGE_W-2*MARGIN-15*mm-16*mm, 16*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(P("<b>Patient à faible risque hémorragique ne nécessitant pas "
                    "d'anticoagulation systémique :</b>", S_CELL_B))
    story.append(reco_table([
        ("2.3.2.1", "En épuration intermittente, il faut probablement privilégier l'héparine "
         "non fractionnée ou de bas poids moléculaire par rapport à d'autres anticoagulants "
         "systémiques. (Avis d'experts)", "Fort"),
        ("2.3.2.2", "En épuration continue, chez l'adulte, il faut probablement privilégier, "
         "sauf contre-indication, l'anticoagulation régionale au citrate, dans le but de "
         "prolonger la durée de vie du circuit.", "Faible"),
        ("2.3.2.3", "En épuration continue, en présence d'une contre-indication au citrate, "
         "il faut probablement privilégier le recours à une anticoagulation par héparine "
         "non fractionnée. (Avis d'experts)", "Fort"),
        ("2.3.2.4", "Chez l'enfant, en EER continue, il faut utiliser une anticoagulation "
         "soit par citrate soit par héparine non fractionnée, le choix étant guidé par "
         "l'expérience de l'équipe.", "Fort"),
    ], [15*mm, PAGE_W-2*MARGIN-15*mm-16*mm, 16*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(P("<b>Patient nécessitant une anticoagulation systémique :</b>", S_CELL_B))
    story.append(reco_table([
        ("2.3.3.1", "Il faut probablement privilégier l'anticoagulation systémique par "
         "héparine aux autres anticoagulants. (Avis d'experts)", "Fort"),
        ("2.3.3.2", "Chez les patients avec thrombopénie induite à l'héparine (TIH) "
         "suspectée ou avérée, en plus de l'interruption du traitement par héparine, il est "
         "possible d'utiliser une anticoagulation régionale au citrate en complément de "
         "l'anticoagulation de la TIH. (Avis d'experts)", "Fort"),
    ], [15*mm, PAGE_W-2*MARGIN-15*mm-16*mm, 16*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(P("Citrate en épuration continue : 3 études observationnelles chez le "
                    "patient à haut risque hémorragique, toutes en faveur d'une réduction "
                    "des complications hémorragiques ; en épuration continue chez le "
                    "patient à faible risque, 6 études randomisées + 8 observationnelles "
                    "montrent une augmentation significative de la durée de vie des "
                    "circuits, moins de complications hémorragiques, une épargne sanguine "
                    "(transfusionnelle) et une limitation de la consommation plaquettaire, "
                    "sans impact sur la mortalité. Anticoagulation régionale "
                    "héparine-protamine non recommandée (risque de TIH, anaphylaxie à la "
                    "protamine, effet rebond). Objectif TCA en cas d'héparine non "
                    "fractionnée : 1,5× le témoin.", S_NOTE))
    story.append(Spacer(1, 3*mm))
    story.append(section_bar("Champ 2.4 — Eau osmosée"))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("2.4.1", "Il faut élaborer une démarche qualité pour la surveillance de l'eau "
         "osmosée dans le respect des normes réglementaires. (Avis d'experts)", "Fort"),
    ], [13*mm, PAGE_W-2*MARGIN-13*mm-16*mm, 16*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(P("Contrôles réguliers sous responsabilité du pharmacien en lien avec le "
                    "réanimateur, selon les circulaires DGS/DH/AFSSAPS et normes NF S93-310/"
                    "S93-315 en vigueur.", S_NOTE))
    return story

def _section_champ3a():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Champ 3.1 — Choix de la méthode"))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("3.1.1", "Les techniques d'EER continues et intermittentes peuvent être utilisées "
         "indifféremment, mais en tenant compte de la disponibilité de la technique et de "
         "l'expérience de l'équipe.", "Fort"),
        ("3.1.2", "Les techniques d'EER diffusives ou convectives peuvent être utilisées "
         "indifféremment, mais en tenant compte de la disponibilité de la technique et de "
         "l'expérience de l'équipe.", "Fort"),
        ("3.1.3", "Chez les patients cérébrolésés à risque d'hypertension intracrânienne, il "
         "faut probablement préférer une technique d'épuration continue ou prolongée à "
         "faible clairance (SLED). (Avis d'experts)", "Fort"),
    ], [13*mm, PAGE_W-2*MARGIN-13*mm-16*mm, 16*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(P("Aucun bénéfice de survie démontré entre continu/intermittent malgré "
                    "plusieurs essais randomisés ; données discordantes sur la récupération "
                    "rénale (méta-analyse : risque accru en défaveur de l'intermittent, mais "
                    "discordance entre études observationnelles OR 1,99 et randomisées OR "
                    "1,15). Cérébrolésés : les techniques discontinues peuvent entraîner un "
                    "œdème cérébral par syndrome de déséquilibre dialytique (variations "
                    "osmotiques) ; 1 étude observationnelle retrouve une majoration de la "
                    "PIC en hémodialyse intermittente chez le traumatisé crânien.", S_NOTE))
    story.append(Spacer(1, 3*mm))
    story.append(section_bar("Champ 3.2 — Dialyse péritonéale"))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("3.2.1", "En pédiatrie et chez le nouveau-né, il est possible de faire de la "
         "dialyse péritonéale, en particulier en période postopératoire de chirurgie "
         "cardiaque à but de déplétion, en raison de sa facilité d'utilisation.", "Faible"),
        ("3.2.2", "En pédiatrie et chez le nouveau-né, il est possible de faire de la "
         "dialyse péritonéale à but d'épuration lors d'une IRA sans critère de dialyse en "
         "urgence absolue.", "Faible"),
        ("3.2.3", "Chez l'adulte, il ne faut probablement pas recourir à la dialyse "
         "péritonéale en première intention.", "Fort"),
    ], [13*mm, PAGE_W-2*MARGIN-13*mm-16*mm, 16*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(P("Pédiatrie : technique préservant le capital vasculaire, délais "
                    "d'obtention d'une épuration efficace trop longs pour une indication "
                    "urgente ; études de faible qualité méthodologique, pas de supériorité "
                    "démontrée sur les autres techniques. Adulte : 3 seules études "
                    "disponibles, contradictoires sur la mortalité ; délai de contrôle "
                    "métabolique/volémique trop long pour les situations d'urgence vitale.", S_NOTE))
    return story

def _section_champ3b():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Champ 3.3 — Dose de dialyse"))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("3.3.1", "En EER intermittente, il faut probablement que la dose de dialyse "
         "minimale délivrée soit de : 1) trois séances par semaine de 4h au moins avec un "
         "débit sang &gt;200 mL/min et un débit dialysat &gt;500 mL/min, ou 2) l'obtention "
         "d'un Kt/V &gt;3,9 par semaine, ou 3) le maintien d'une urée prédialytique de "
         "20-25 mmol/L.", "Fort"),
        ("3.3.2", "En EER continue, il faut probablement que la dose de dialyse minimale "
         "délivrée soit de 20-25 mL/kg/h d'effluent, obtenus par filtration et/ou "
         "diffusion.", "Fort"),
        ("3.3.3", "Il faut adapter la dose de dialyse délivrée aux besoins du patient en "
         "termes de contrôle du métabolisme, d'équilibre électrolytique et acido-basique. "
         "Il faut prévenir la survenue d'une hypokaliémie et/ou d'une hypophosphatémie. Il "
         "faut adapter la posologie des médicaments éliminés par EER à la dose délivrée. "
         "(Avis d'experts)", "Fort"),
        ("3.3.4", "En EER intermittente, il faut probablement augmenter la durée et/ou la "
         "fréquence des séances en cas d'hypercatabolisme et/ou de désordre métabolique "
         "sévère et/ou d'une indication à une déplétion hydrosodée. (Avis d'experts)", "Fort"),
        ("3.3.5", "En EER continue, il ne faut pas, sur la seule présence d'un sepsis, "
         "intensifier la dose d'épuration.", "Fort"),
    ], [13*mm, PAGE_W-2*MARGIN-13*mm-16*mm, 16*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(P("EER intermittente : 3 ECR, résultats contradictoires — Kt/V "
                    "hebdomadaire supérieur associé à une mortalité réduite dans 1 étude "
                    "(biais possibles), mais absence de différence dans les 2 autres ; "
                    "conclusion = dose minimale (celle des bras témoins) au-delà de "
                    "laquelle pas de bénéfice supplémentaire démontré. EER continue : 2 "
                    "grandes études randomisées multicentriques (VA/NIH, 1124 patients ; "
                    "RENAL, 1508 patients) ne retrouvent aucun bénéfice à intensifier la "
                    "dose au-delà de 25 mL/kg/h, avec davantage de complications "
                    "métaboliques dans les groupes intensifs. Sepsis : méta-analyse (9 "
                    "essais, 1786 patients) — intensification non associée à une réduction "
                    "de mortalité (OR 1,02) ; hémofiltration à haut volume proposée comme "
                    "immunomodulatrice mais jamais confirmée par les essais contrôlés.", S_NOTE))
    return story

def _section_champ3c():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Champ 3.4 — Réglages"))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("3.4.1", "Il ne semble pas nécessaire d'utiliser d'héparine pour le rinçage des "
         "circuits d'EER. (Avis d'experts)", "Faible"),
        ("3.4.2", "Il ne faut pas réduire les apports nutritionnels chez les patients en "
         "EER. (Avis d'experts)", "Fort"),
        ("3.4.3", "En hémofiltration réalisée en post-dilution, il faut ajuster le débit "
         "sanguin de façon à garder une fraction de filtration &lt;25 %. (Avis d'experts)", "Fort"),
        ("3.4.4", "En hémodialyse intermittente d'une durée &lt;6h, le débit sanguin doit "
         "être entre 200 et 300 mL/min et le débit dialysat ≥500 mL/min pour la plupart des "
         "patients. (Avis d'experts)", "Fort"),
        ("3.4.5", "Chez l'enfant, en hémodialyse intermittente d'une durée &lt;6h, le débit "
         "sanguin doit débuter à 3 mL/kg/min pour atteindre 5 mL/kg/min lors des sessions "
         "suivantes, et le débit de dialysat doit être au minimum de 300 mL/min jusqu'à "
         "deux fois le débit sanguin. (Avis d'experts)", "Fort"),
        ("3.4.6", "En hémodialyse intermittente prolongée à faible clairance (SLED), il "
         "faut utiliser des débits sang et dialysat inférieurs. (Avis d'experts)", "Fort"),
        ("3.4.7", "Il faut que le branchement des lignes artérielles et veineuses soit "
         "réalisé de façon simultanée pour éviter la déplétion volémique. (Avis d'experts)", "Fort"),
        ("3.4.8", "En hémodialyse intermittente, il faut probablement recommander la baisse "
         "de la température dans le dialysat pour améliorer la tolérance hémodynamique.", "Fort"),
        ("3.4.9", "En hémodialyse intermittente, il faut probablement augmenter la "
         "concentration en sodium dans le dialysat (conductivité) &gt;145 mmol/L pour "
         "améliorer la tolérance hémodynamique ou lorsque l'urée est très élevée.", "Fort"),
        ("3.4.10", "En hémodialyse intermittente, il faut probablement utiliser un tampon "
         "bicarbonate.", "Fort"),
    ], [13*mm, PAGE_W-2*MARGIN-13*mm-16*mm, 16*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(P("Réglages 3.4.6-3.4.10 visent à optimiser la tolérance hémodynamique en "
                    "hémodialyse intermittente (les hypotensions favorisent l'entretien des "
                    "lésions de nécrose tubulaire) : dialysat modérément hypotherme (limite "
                    "le réchauffement et la baisse du tonus vasomoteur), tampon bicarbonate "
                    "(préféré à l'acétate, vasoplégiant), conductivité sodée élevée (limite "
                    "la baisse rapide d'osmolalité en début de séance) — une étude combinant "
                    "ces réglages montre une amélioration nette de la tolérance "
                    "hémodynamique, comparable à une technique continue. Fraction de "
                    "filtration : maintenue &lt;25 % sous héparine non fractionnée (jusqu'à "
                    "27 % sous citrate) ; hématocrite intrafiltre &lt;40 % comme meilleur "
                    "indice de viscosité.", S_NOTE))
    return story

def _section_champ4():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Champ 4.1-4.2 — Procédures, formation & gestion du cathéter"))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("4.1.1", "La réalisation d'une séance d'EER doit être fondée sur une procédure "
         "interne au service comprenant au minimum une prescription et une surveillance "
         "spécifiques, la description de la réalisation technique de la séance et des "
         "mesures d'hygiène (manipulations, désinfection des moniteurs/générateurs). (Avis "
         "d'experts)", "Fort"),
        ("4.1.2", "Les équipes médicales et paramédicales doivent être formées, en accord "
         "avec les référentiels métiers, pour acquérir les compétences nécessaires à "
         "l'utilisation des moniteurs/générateurs, à la prévention et au traitement des "
         "complications, et à la traçabilité des événements et procédures d'hygiène. (Avis "
         "d'experts)", "Fort"),
        ("4.2.1", "Il faut réserver l'utilisation d'un cathéter de dialyse à l'EER. (Avis "
         "d'experts)", "Fort"),
        ("4.2.2", "Il faut gérer les cathéters d'EER suivant les mêmes recommandations que "
         "celles des cathéters veineux centraux. (Avis d'experts)", "Fort"),
        ("4.2.3", "Il faut probablement considérer comme critère de dysfonction du cathéter "
         "l'impossibilité d'atteindre ou de maintenir un débit de pompe sang nécessaire et "
         "suffisant pour délivrer une dose adéquate de traitement. (Avis d'experts)", "Fort"),
        ("4.2.4", "Il faut éliminer une hypovolémie en présence d'une dysfonction de "
         "cathéter. (Avis d'experts)", "Fort"),
        ("4.2.5", "Il faut éliminer une thrombose en présence d'une dysfonction de cathéter "
         "non liée à une hypovolémie. (Avis d'experts)", "Fort"),
        ("4.2.6", "En hémodialyse intermittente, chez l'adulte, il faut changer le cathéter "
         "dès que possible s'il y a eu nécessité d'inverser les lignes, en l'absence "
         "d'hypovolémie. (Avis d'experts)", "Fort"),
        ("4.2.7", "Il n'est pas possible de recommander un type de verrou plutôt qu'un "
         "autre (sérum physiologique, héparine, citrate…). (Avis d'experts)", "Faible"),
    ], [13*mm, PAGE_W-2*MARGIN-13*mm-16*mm, 16*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(P("Recommandations de sécurisation SRLF/SFAR établies en 2008. Dysfonctions "
                    "précoces (&lt;10j) liées au positionnement (cathéter fémoral : risque "
                    "accru si l'extrémité n'atteint pas la VCI ; jugulaire : si elle "
                    "n'atteint pas l'oreillette droite) ; dysfonctions tardives liées à une "
                    "thrombose. Verrou citraté : 1 étude randomisée récente en faveur du "
                    "critère principal, signal sur un délai de survenue d'infection plus "
                    "tardif — données encore insuffisantes pour recommander un verrou "
                    "spécifique.", S_NOTE))
    story.append(Spacer(1, 3*mm))
    story.append(section_bar("Champ 4.3 — Gestion du circuit extracorporel", color=GREY))
    story.append(Spacer(1, 2*mm))
    story.append(info_panel(P(
        "<b>Toutes les recommandations de ce champ sont des avis d'experts fondés sur des "
        "règles de bonnes pratiques ; la source précise explicitement qu'« aucune "
        "publication scientifique n'en a évalué l'impact ».</b>",
        S_BODY_SM), bg=AMBER_LIGHT, border=AMBER))
    story.append(Spacer(1, 2*mm))
    cw = PAGE_W - 2*MARGIN
    story.append(simple_table(
        ["Étape", "Recommandations (toutes Accord fort sauf *)"],
        [
            ["Au branchement", "Vérifier la perméabilité de l'abord vasculaire avant "
             "branchement • deux personnes pour réaliser le branchement des lignes • "
             "rincer le circuit pour qu'il y reste le moins d'air possible • garder visible "
             "la connectique pendant la séance • prévenir l'agitation du patient • "
             "augmenter progressivement le débit sanguin pour vérifier perméabilité/"
             "étanchéité • en hémofiltration, démarrer la convection une fois le débit cible "
             "atteint."],
            ["Pendant la séance", "Surveiller étroitement les pressions du circuit "
             "(artérielle, veineuse, transmembranaire) et la perte de charge • fixer les "
             "lignes pour éviter toute plicature • réduire le débit de la pompe et "
             "interrompre la convection lors des mobilisations du patient (*Accord faible) "
             "• respecter l'asepsie et éviter toute entrée d'air lors des prélèvements dans "
             "le circuit • maintenir un haut niveau de sang dans le piège à bulles."],
            ["Au débranchement", "Restituer le sang du circuit au patient au sérum "
             "physiologique • installer le patient en décubitus dorsal pour réduire le "
             "risque d'embolie gazeuse (*Accord faible) • chez le nourrisson &lt;15 kg, "
             "débit de restitution probablement ≤2 mL/kg/min (*Accord faible)."],
        ],
        [cw*0.18, cw*0.82]))
    return story

def _section_synthese():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Synthèse et messages clés"))
    story.append(Spacer(1, 2*mm))
    story.append(P(
        "• Initiation : sans délai si pronostic vital engagé (hyperkaliémie, acidose "
        "métabolique, lyse tumorale, OAP réfractaire) ; pas de délai optimal démontré en "
        "dehors de l'urgence vitale ; « précoce » = stade KDIGO 2 ou &lt;24h, « tardive » = "
        "&gt;48h ou KDIGO 3/pronostic vital (repères, non des seuils de déclenchement "
        "prouvés).<br/>"
        "• Voies d'abord : éviter le sous-clavier ; fémoral et jugulaire interne droit "
        "équivalents sauf IMC&gt;28 (préférer jugulaire) ; jugulaire interne gauche en "
        "3e choix ; échoguidage recommandé (jugulaire fortement, fémoral probablement) ; "
        "ablation dès que possible.<br/>"
        "• Membranes : éviter le cuprophane ; haute perméabilité pour l'hémofiltration "
        "seulement (pas en hémodialyse sans dialysat ultrapure) ; pas de membrane "
        "spécifique recommandée dans le choc septique.<br/>"
        "• Anticoagulation : citrate en 1ère intention en épuration continue (haut risque "
        "hémorragique et prolongation de la durée de vie du circuit chez le patient à "
        "faible risque) ; héparine non fractionnée si contre-indication au citrate ; pas "
        "d'anticoagulation systémique pour la seule indication EER chez le patient à haut "
        "risque hémorragique ; héparine-protamine non recommandée.<br/>"
        "• Dose de dialyse : intermittente ≥3×4h/semaine (Kt/V&gt;3,9 ou urée "
        "prédialytique 20-25 mmol/L) ; continue 20-25 mL/kg/h d'effluent — "
        "l'intensification au-delà n'apporte pas de bénéfice supplémentaire (y compris "
        "dans le sepsis) et majore les complications métaboliques.<br/>"
        "• Tolérance hémodynamique en hémodialyse intermittente : dialysat hypotherme, "
        "conductivité sodée élevée, tampon bicarbonate.<br/>"
        "• Sécurisation : procédure de service écrite, personnel formé, cathéter réservé à "
        "l'EER et géré comme un CVC, procédures de branchement/surveillance/débranchement "
        "standardisées (champ 4.3, avis d'experts non évalués par la littérature).<br/>"
        "• Dialyse péritonéale : option pédiatrique/néonatale (postopératoire de chirurgie "
        "cardiaque, IRA non urgente) ; probablement pas en 1ère intention chez l'adulte.",
        S_BODY))
    story.append(Spacer(1, 5*mm))

    story.append(section_bar("Sources et traçabilité", color=GREY))
    story.append(Spacer(1, 2*mm))
    story.append(P(
        "<b>Document source :</b> « Épuration extrarénale en réanimation adulte et "
        "pédiatrique » — Recommandations Formalisées d'Experts sous l'égide de la SRLF, "
        "avec la participation de la SFAR, du GFRUP et de la SFD. Réanimation 2014, DOI "
        "10.1007/s13546-014-0917-6. 18 experts, coordination C. Vinsonneau (Melun).", S_SOURCE))
    story.append(Spacer(1, 1.5*mm))
    story.append(P("<b>Couverture :</b> les 78 recommandations numérotées (1.1-1.5, "
                    "2.1.1-2.4.1, 3.1.1-3.4.10, 4.1.1-4.3.3.3) sont reproduites intégralement, "
                    "en s'appuyant sur le « Tableau récapitulatif » propre de la source "
                    "(pages 16-19 du texte extrait) comme référence canonique verbatim pour "
                    "le texte de chaque item, croisé avec les sections d'argumentaire "
                    "correspondantes (pages 1-15) pour les notes d'évidence. La source ne "
                    "fournit pas de chiffre-résumé agrégé du type « N recommandations » — "
                    "aucune divergence de comptage à signaler pour ce document.", S_SOURCE))
    story.append(Spacer(1, 1.5*mm))
    story.append(P("<b>Convention de grading propre à cette source :</b> comme pour la fiche "
                    "« Nutrition artificielle en réanimation » de ce même corpus, aucun tag "
                    "GRADE numérique (1+/1-/2+/2-) n'est jamais imprimé à côté d'un item "
                    "individuel — seul un tag « Accord fort » ou « Accord faible » (force du "
                    "consensus RAND/UCLA) est indiqué, reproduit ici tel quel comme chip "
                    "coloré. La mention « (Avis d'experts) », lorsqu'elle est imprimée par "
                    "la source (littérature insuffisante pour une analyse graduée), est "
                    "conservée verbatim dans le texte de la recommandation.", S_SOURCE))
    story.append(Spacer(1, 3*mm))
    story.append(info_panel(P(
        "<b>Avertissement :</b> ce document est une fiche de synthèse indépendante, produite "
        "pour un usage d'aide-mémoire. Il reprend l'intégralité des recommandations de la "
        "RFE mais ne remplace pas le texte intégral et n'est ni édité ni validé par la "
        "SRLF/SFAR/GFRUP/SFD. En cas de doute, se référer au texte intégral, aux "
        "recommandations ultérieures et/ou à un avis spécialisé.",
        S_BODY_SM), bg=GREY_LIGHT, border=GREY))
    return story

def _section_intro_champ1():
    return _section_intro() + [Spacer(1, 4*mm)] + _section_champ1()

def _section_champ3a_3b():
    return _section_champ3a() + [Spacer(1, 4*mm)] + _section_champ3b()

SECTIONS = [
    ("Introduction & Champ 1 — Critères d'initiation de l'EER", _section_intro_champ1),
    ("Champ 2.1-2.2 — Voies d'abord & Membranes", _section_champ2a),
    ("Champ 2.3-2.4 — Anticoagulation & Eau osmosée", _section_champ2b),
    ("Champ 3.1-3.3 — Méthode, dialyse péritonéale & dose de dialyse", _section_champ3a_3b),
    ("Champ 3.4 — Réglages", _section_champ3c),
    ("Champ 4 — Sécurisation des procédures", _section_champ4),
    ("Synthèse, sources & traçabilité", _section_synthese),
]

def _make_doc():
    return SimpleDocTemplate(OUT, pagesize=A4,
                              leftMargin=MARGIN, rightMargin=MARGIN,
                              topMargin=32*mm, bottomMargin=16*mm,
                              title="Fiche SRLF 2014 - Epuration extrarenale en reanimation",
                              author="Synthèse indépendante (source SRLF/SFAR/GFRUP/SFD)")

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
