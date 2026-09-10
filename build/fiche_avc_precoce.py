# -*- coding: utf-8 -*-
"""
Fiche de synthese - Recommandations de bonne pratique (RPC) HAS, mai 2009 :
"Accident vasculaire cerebral (AVC) : prise en charge precoce (alerte, phase
prehospitaliere, phase hospitaliere initiale, indications de la thrombolyse)".
Source : sources/avc_precoce.pdf (21 pages), sources/avc_precoce.txt (texte
extrait integralement, 1395 lignes).

DISCLOSURE - le PDF source porte en page 1 la mention "DOCUMENT DE TRAVAIL -
NE PAS DIFFUSER" (texte residuel d'une etape de redaction anterieure, non
supprime avant mise en ligne). Ceci n'est PAS un tampon d'obsolescence : le
texte confirme lui-meme, page 2, "Ce document a ete valide par le College de
la Haute Autorite de Sante en mai 2009", et il est heberge publiquement par
SFAR depuis 2015 avec le statut "en vigueur" dans library_final.json. Retenu
pour construction ; disclosure conservee ici plutot que resolue en silence
(regle 5 CLAUDE.md).

METHODOLOGIE - grades HAS A/B/C + "accord professionnel" (PAS GRADE 1+/2+),
meme schema que fiche_infarctus_myocarde.py et fiche_transfusion_plasma.py.
VERIFIE PAR grep SUR LE TEXTE APLATI (espaces normalises, insensible aux
retours a la ligne qui coupent "accord professionnel" en 2 - au moins 5
occurrences du texte source sont coupees ainsi par l'extraction PyMuPDF ;
un premier passage en grep -n ligne-a-ligne naif en manquait donc plusieurs,
corrige ici en repassant sur le texte aplati - meme categorie de piege deja
documentee dans fiche_transfusion_plasma.py) : 11 occurrences "grade [ABC]"
(dont 4 dans la description methodologique du chapitre 1.4 - definitions de
A/B/C, non appliquees a un enonce - et 7 appliquees a un enonce clinique
precis : 1x A, 2x B, 4x C) et 47 occurrences "accord professionnel" (dont 2
phrases generales du chapitre 1.4 et 2 quasi-identiques dans le chapitre
methodologique "Methode RPC" en fin de document, non retranscrit ici - et
43 appliquees a un enonce clinique precis). Total retranscrit dans les
tableaux de cette fiche : 50 enonces tagues explicitement dans la source -
1x grade A, 2x grade B, 4x grade C, 43x accord professionnel (chip "AP",
meme convention que fiche_transfusion_plasma.py) - un pour un contre le
texte source (chaque tag source correspond a exactement une ligne de
tableau ; aucun regroupement de plusieurs tags sous un chip unique). 4
enonces cliniquement pertinents mais explicitement SANS tag dans la source
(ex. "scanner cerebral" a defaut d'IRM, "tout patient ayant un AVC doit
etre propose a une UNV") sont retranscrits avec un tiret "—" plutot qu'un
tag invente - trouve lors de l'audit independant : une premiere version de
cette fiche leur avait a tort attribue le chip "AP", corrige ici (regle 4/5
CLAUDE.md : ne jamais fabriquer un tag absent de la source).

PERIMETRE - integralite des chapitres 1 (introduction : champ, objectifs,
gradation), 2 (l'alerte), 3 (phase prehospitaliere), 4 (phase hospitaliere
initiale, dont l'algorithme de l'annexe 1), 5 (thrombolyse), et annexe 2
(contre-indications de l'alteplase, extrait litteral du RCP/AMM d'ACTILYSE(R)
cite par la source). Les sections "Methode RPC", "Participants" (comite
d'organisation / groupe de travail / groupe de lecture, ~85 noms) et "Fiche
descriptive" (pages 16-21, sans contenu clinique nouveau par rapport au
chapitre 1) ne sont pas retranscrites - couverture clinique complete
verifiee par relecture integrale du texte extrait.

ALGORITHME - Annexe 1 (page 14 source) : algorithme de la filiere de prise en
charge precoce (alerte -> regulation SAMU -> evaluation de gravite ->
transport -> choix de l'etablissement -> admission -> bilan), en boites
reliees par des fleches non lineaire pour le texte brut extrait. Restructure
ici en sequence de boites (meme convention deja disclosee pour l'algorithme 3
de fiche_infarctus_myocarde.py et pour d'autres figures non lineaires de ce
corpus) : integralite du contenu conservee (tous les embranchements, tous
les types d'etablissement, le role de la telemedecine), sans pretention a
une reproduction pixel-exacte des boites/fleches d'origine.

_count_pages() : pattern copie de fiche_infarctus_myocarde.py / fiche_aap_programmee.py
(PyMuPDF/fitz, jamais vers OUT, toujours vers tempfile.mktemp()).
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from style import *
from style import _c
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.units import mm

GRADE_COLORS["A"] = (GREEN, WHITE)
GRADE_COLORS["B"] = (TEAL, WHITE)
GRADE_COLORS["C"] = (AMBER, WHITE)
GRADE_COLORS["AP"] = (GREY, WHITE)

OUT = "/home/user/rfe-sfar-website/output/Fiche_HAS_AVC_Prise_En_Charge_Precoce_2009.pdf"

SOURCE_TXT = ("Source : Haute Autorité de Santé (HAS) — Recommandations de bonne pratique « Accident "
              "vasculaire cérébral : prise en charge précoce » (mai 2009). Fiche de synthèse non "
              "officielle : se référer au texte intégral.")

def P(txt, style=S_CELL):
    return Paragraph(txt, style)

def chip(label, **kw):
    return grade_chip(label, **kw)

AP_W = 20 * mm

def prop_table(rows, col_widths=None):
    """rows: (text, grade_label) - grade_label parmi 'A', 'B', 'C', 'AP'."""
    text_w = PAGE_W - 2 * MARGIN - AP_W
    cw = col_widths or [text_w, AP_W]
    data = [[P("Recommandation (texte condensé, fidèle à la source)", S_HEAD_W), P("Niveau", S_HEAD_W_C)]]
    for txt, grade in rows:
        data.append([P(txt, S_CELL), chip(grade, width=AP_W - 2 * mm)])
    t = Table(data, colWidths=cw, repeatRows=1)
    style_cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), NAVY), ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTNAME", (0, 0), (-1, 0), FONT_BOLD), ("FONTSIZE", (0, 0), (-1, 0), 8),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("ALIGN", (1, 0), (1, -1), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 0.5, GREY_LIGHT),
        ("TOPPADDING", (0, 0), (-1, -1), 3.2), ("BOTTOMPADDING", (0, 0), (-1, -1), 3.2),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            style_cmds.append(("BACKGROUND", (0, i), (-1, i), BG_PANEL))
    t.setStyle(TableStyle(style_cmds))
    return t

def simple_table(header, rows, col_widths, header_style=S_HEAD_W):
    data = [[P(h, header_style) for h in header]] + [
        [c if not isinstance(c, str) else P(c, S_CELL) for c in row] for row in rows
    ]
    t = Table(data, colWidths=col_widths, repeatRows=1)
    style_cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), NAVY), ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTNAME", (0, 0), (-1, 0), FONT_BOLD), ("FONTSIZE", (0, 0), (-1, 0), 8),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("GRID", (0, 0), (-1, -1), 0.5, GREY_LIGHT),
        ("TOPPADDING", (0, 0), (-1, -1), 3.2), ("BOTTOMPADDING", (0, 0), (-1, -1), 3.2),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            style_cmds.append(("BACKGROUND", (0, i), (-1, i), BG_PANEL))
    t.setStyle(TableStyle(style_cmds))
    return t

def flow_box(text, bg, border, border_w=1):
    return Table([[P(text, S_CELL)]], colWidths=[PAGE_W - 2 * MARGIN], style=TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), bg), ("BOX", (0, 0), (-1, -1), border_w, border),
        ("TOPPADDING", (0, 0), (-1, -1), 3 * mm), ("BOTTOMPADDING", (0, 0), (-1, -1), 3 * mm),
        ("LEFTPADDING", (0, 0), (-1, -1), 3.5 * mm), ("RIGHTPADDING", (0, 0), (-1, -1), 3.5 * mm),
    ]))

def arrow():
    return P("↓", pstyle("arrow_avc", base=S_H2, alignment=1, fontSize=13))

TOTAL_PAGES = {"n": 7}

def on_page(canvas, doc, page_title):
    header_band(canvas, doc, "HAS — RECOMMANDATIONS DE BONNE PRATIQUE — MAI 2009 — FICHE DE SYNTHÈSE",
                "Accident vasculaire cérébral — prise en charge précoce",
                page_title, icon_fn=lambda c, x, y: icon_shield(c, x, y, 13 * mm), color=RED)
    footer_band(canvas, doc, SOURCE_TXT, f"Page {doc.page} / {TOTAL_PAGES['n']}")

# ---------------------------------------------------------------------------
def _section_intro_alerte():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Champ :</b> prise en charge précoce de l'accident vasculaire cérébral (AVC) — alerte, "
        "phase préhospitalière, phase hospitalière initiale, indications de la thrombolyse. "
        "Recommandations HAS, mai 2009, à la demande conjointe de la Société française "
        "neuro-vasculaire et de la DHOS. Concerne l'AIT, l'infarctus cérébral (IC) et "
        "l'hémorragie cérébrale (HC) ; <b>exclut l'hémorragie sous-arachnoïdienne</b> (hors champ). "
        "En France : 100 000 à 145 000 AVC/an, 15-20 % de décès à 1 mois, 75 % de survivants avec "
        "séquelles ; 1ère cause de handicap acquis de l'adulte, 2ème cause de démence, 3ème cause "
        "de mortalité ; 25 % des patients ont moins de 65 ans.", S_BODY), bg=BG_PANEL, border=RED))
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Méthodologie — grades HAS A/B/C + « accord professionnel »</b> (même schéma que "
        "d'autres fiches HAS de ce corpus, à la différence du GRADE 1+/2+) : Grade A = preuve "
        "scientifique établie (niveau 1) ; Grade B = présomption scientifique (niveau 2) ; "
        "Grade C = faible niveau de preuve (niveaux 3-4) ; <b>« accord professionnel »</b> = en "
        "l'absence d'études, avis du groupe de travail après consultation du groupe de lecture — "
        "c'est le cas de la <b>grande majorité</b> des recommandations de ce texte. <b>Vérifié "
        "exhaustivement par grep (texte aplati, insensible aux tags coupés par un retour à la "
        "ligne) contre le texte source : 50 énoncés cliniques tagués — 1× grade A, 2× grade B, "
        "4× grade C, 43× accord professionnel (chip « AP ») — retranscrits un pour un contre le "
        "texte source, sans regroupement de plusieurs tags sous un chip unique. Quelques énoncés "
        "cliniquement pertinents mais explicitement <b>sans</b> tag dans la source (ex. le "
        "scanner cérébral à défaut d'IRM) sont retranscrits avec « — » plutôt qu'un tag "
        "inventé.</b>", S_BODY_SM),
        bg=BG_PANEL, border=AMBER))
    story.append(Spacer(1, 3 * mm))

    story.append(section_bar("2 — L'alerte", color=RED))
    story.append(Spacer(1, 2 * mm))
    story.append(P(
        "La prise en charge rapide des patients ayant un AVC nécessite que les symptômes soient "
        "connus par la population générale et les professionnels, et que les filières "
        "préhospitalière et hospitalière soient efficaces.", S_BODY_SM))
    story.append(Spacer(1, 2 * mm))
    story.append(prop_table([
        ("Les symptômes de l'AVC doivent être connus par la population générale et plus "
         "particulièrement par les patients à risque/ATCD vasculaires, ainsi que leur entourage.", "C"),
        ("Il convient de sensibiliser les professionnels pour des filières préhospitalière et "
         "hospitalière initiale efficaces.", "AP"),
        ("Les campagnes d'information grand public doivent être encouragées et répétées (effet "
         "temporaire) ; ne pas se limiter aux patients à risque vasculaire, concerner toute la "
         "population y compris les jeunes.", "C"),
        ("Information du grand public : reconnaissance des symptômes — message <b>FAST</b> (Face "
         "Arm Speech Time, dérivé de l'échelle de Cincinnati) recommandé comme vecteur efficace.", "AP"),
        ("Urgence : la prise en charge et les traitements sont urgents (admission en UNV et "
         "thrombolyse éventuelle), d'autant plus efficaces que précoces ; même régressifs, les "
         "symptômes imposent d'appeler le SAMU-Centre 15.", "AP"),
        ("Nécessité de laisser le patient allongé.", "AP"),
        ("Le médecin traitant doit informer les patients à risque (ATCD vasculaires, HTA, "
         "diabète, artériopathie des MI) et leur entourage des signes de l'AVC ; préconiser "
         "l'appel immédiat au 15 avant tout appel à son cabinet ; expliquer l'importance de noter "
         "l'heure des premiers symptômes.", "AP"),
        ("En cas d'appel direct au médecin traitant : transférer l'appel au SAMU-Centre 15 et, au "
         "mieux, rester en ligne pour une <b>conférence à 3</b> (appelant, médecin traitant, "
         "régulateur).", "AP"),
        ("Formation continue renforcée pour les permanenciers/standardistes des Centre 15, "
         "utilisant les 5 signes d'alerte de l'ASA*.", "AP"),
        ("Programmes de formation renforcés pour les acteurs du premier secours (pompiers, "
         "ambulanciers, secouristes), utilisant le message FAST.", "AP"),
        ("Développer la formation continue auprès de tous les professionnels de la filière "
         "d'urgence (généralistes, spécialistes, IDE, aides-soignants, kinés, orthophonistes...).", "AP"),
        ("Messages clés aux professionnels : tout déficit neurologique brutal, transitoire ou "
         "prolongé = urgence absolue ; noter l'heure exacte de survenue ; connaître l'efficacité "
         "de la prise en charge en UNV et les traitements spécifiques.", "AP"),
        ("L'AIT est une urgence et justifie une prise en charge neuro-vasculaire immédiate pour "
         "confirmer le diagnostic, préciser l'étiologie et instaurer le traitement en urgence.", "C"),
    ]))
    story.append(Spacer(1, 1 * mm))
    story.append(P("<i>* Les 5 signes d'alerte ASA : faiblesse/engourdissement brutal uni ou "
                    "bilatéral de la face/bras/jambe ; baisse/perte de vision uni ou bilatérale ; "
                    "difficulté de langage ou de compréhension ; mal de tête sévère, soudain et "
                    "inhabituel sans cause apparente ; perte d'équilibre/instabilité de la marche/"
                    "chutes inexpliquées, en particulier associées à l'un des signes précédents.</i>",
                    S_NOTE))
    return story


def _section_prehosp_hosp():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("3 — Phase préhospitalière", color=RED))
    story.append(Spacer(1, 2 * mm))
    story.append(prop_table([
        ("Utiliser un nombre limité d'échelles standardisées : échelle <b>FAST</b> (ou équivalent "
         "français) pour les paramédicaux/premiers secours (formation requise).", "AP"),
        ("Tout médecin urgentiste doit savoir utiliser l'échelle <b>NIHSS</b> (National Institute "
         "of Health Stroke Scale) et évaluer la sévérité de l'AVC.", "AP"),
        ("La gestion de l'appel initial pour suspicion d'AVC doit être faite par les centres de "
         "régulation médicale des SAMU-Centre 15.", "AP"),
        ("Des questionnaires ciblés et standardisés doivent être utilisés pour l'évaluation "
         "téléphonique des patients suspects d'AVC et pour aider à la décision du régulateur.", "AP"),
        ("Tout acte de régulation pour suspicion d'AVC/AIT comprend l'appel au médecin de l'UNV "
         "la plus proche ; l'orientation est décidée de concert entre régulateur et médecin UNV.", "AP"),
        ("L'envoi d'une équipe médicale (Smur) ne doit pas retarder la prise en charge ; "
         "nécessaire en cas de troubles de la vigilance, détresse respiratoire ou instabilité "
         "hémodynamique.", "AP"),
        ("Les centres de régulation doivent choisir le moyen de transport le plus rapide. "
         "(Aucune recommandation possible sur l'imagerie embarquée — à évaluer.)", "AP"),
        ("Remplir une fiche standardisée : antécédents, traitements en cours, heure de début des "
         "symptômes, éléments de gravité clinique (NIHSS).", "AP"),
        ("En cas de transport médicalisé, effectuer les prélèvements sanguins pour le bilan "
         "biologique.", "AP"),
        ("Autoriser la réalisation d'une glycémie capillaire en préhospitalier par tous les "
         "acteurs de la chaîne d'urgence ; corriger l'hypoglycémie (pas de preuve pour débuter "
         "l'insuline en préhospitalier en cas d'hyperglycémie).", "AP"),
        ("Réaliser un électrocardiogramme en cas de médicalisation du transport.", "AP"),
        ("Privilégier le transport en décubitus dorsal, sauf signes d'HTIC, troubles de la "
         "vigilance, nausées/vomissements.", "AP"),
        ("Mesurer la pression artérielle ; pas d'argument pour traiter une HTA sauf indication "
         "extraneurologique associée (ex. décompensation cardiaque).", "AP"),
        ("Oxygénothérapie non systématique, sauf si SpO<sub>2</sub> &lt; 95 %.", "AP"),
    ]))
    story.append(Spacer(1, 3 * mm))

    story.append(section_bar("4 — Phase hospitalière initiale", color=RED))
    story.append(Spacer(1, 2 * mm))
    story.append(prop_table([
        ("La filière intrahospitalière neuro-vasculaire doit être organisée au préalable, "
         "coordonnée (urgentistes, neurologues, radiologues, réanimateurs, biologistes) et "
         "formalisée par procédures écrites ; elle doit privilégier la rapidité d'accès à "
         "l'expertise neuro-vasculaire et à l'imagerie cérébrale en organisant au mieux les "
         "aspects structurels et fonctionnels, avec évaluation régulière de la performance de "
         "l'organisation.", "AP"),
        ("Les patients adressés à un établissement avec UNV doivent être pris en charge dès leur "
         "arrivée par un médecin de la filière neuro-vasculaire.", "AP"),
        ("Fiche standardisée (antécédents, traitements, heure de début, NIHSS) remplie dès "
         "l'admission si non faite en préhospitalier.", "AP"),
        ("ECG et bilan biologique (hémostase, hémogramme, glycémie capillaire) réalisés en "
         "urgence si non faits en préhospitalier.", "AP"),
        ("Monitoring de la pression artérielle, du rythme cardiaque, de la SpO<sub>2</sub> et "
         "surveillance de la température.", "AP"),
        ("Les établissements sans UNV doivent structurer une filière de prise en charge des "
         "patients suspects d'AVC en coordination avec une UNV.", "AP"),
        ("Accès prioritaire 24h/24 et 7j/7 à l'imagerie cérébrale, avec protocoles formalisés et "
         "contractualisés avec le service de radiologie.", "AP"),
        ("L'IRM est l'examen le plus performant (ischémie récente précoce + hémorragie "
         "intracrânienne) ; à privilégier. Si accessible en urgence en 1ère intention : "
         "protocole court — séquences diffusion, FLAIR, écho de gradient.", "B"),
        ("À défaut d'IRM en urgence : scanner cérébral (montre inconstamment l'ischémie récente, "
         "visualise l'hémorragie intracrânienne). <i>(non tagué dans la source)</i>", "—"),
        ("Exploration des artères intracrâniennes par ARM cérébrale, angioscanner ou Doppler "
         "transcrânien.", "AP"),
        ("Exploration des artères cervicales précoce devant tout AIC (urgente si AIT, infarctus "
         "mineur, accident fluctuant/évolutif) : écho-Doppler, ARM des vaisseaux "
         "cervico-encéphaliques avec gadolinium, ou angioscanner des troncs supra-aortiques.", "B"),
        ("Tout patient ayant un AVC doit être proposé à une UNV. <i>(non tagué dans la source)</i>", "—"),
        ("Hospitalisation en réanimation : décision au cas par cas, partagée par l'ensemble des "
         "professionnels (réanimateurs, neurologues), en respectant les souhaits du patient.", "AP"),
        ("Les décisions de limitation et d'arrêt de traitement doivent être prises de façon "
         "collégiale.", "AP"),
        ("Les réanimateurs sont aussi impliqués dans la prise en charge des patients en mort "
         "cérébrale.", "AP"),
        ("Avis neurochirurgical (après avis neuro-vasculaire) pour infarctus sylvien malin, "
         "infarctus/hématome cérébelleux compliqué d'HTIC, ou certains hématomes cérébraux "
         "hémisphériques.", "AP"),
    ]))
    return story


def _section_algo_thrombolyse():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("Annexe 1 — Algorithme de prise en charge précoce d'un AVC", color=TEAL_DARK))
    story.append(Spacer(1, 2 * mm))
    story.append(KeepTogether([
        flow_box("<b>Suspicion d'AVC ou d'AIT</b> — appel du patient, de son entourage, ou d'un "
                 "médecin généraliste. Si appel direct au généraliste : <b>conférence à 3</b> "
                 "(appelant, médecin traitant, régulateur) → <b>Appel du 15</b> (SAMU-Centre 15).",
                 BG_PANEL, TEAL),
        arrow(),
        flow_box("<b>Recherche des signes de gravité clinique</b> : troubles de la vigilance, "
                 "détresse respiratoire, instabilité hémodynamique. <b>Oui</b> → envoi d'une "
                 "équipe médicale (Smur), transport médicalisé (TM). <b>Non</b> → transport par le "
                 "moyen le plus rapide.", BG_PANEL, TEAL),
    ]))
    story.append(Spacer(1, 1.5 * mm))
    story.append(KeepTogether([
        arrow(),
        flow_box("<b>Appel du médecin de l'UNV la plus proche</b> — <b>Suspicion d'AVC/AIT "
                 "confirmée ?</b> <b>Non</b> → urgences de proximité ou orientation adaptée. "
                 "<b>Oui</b>, ou en cas de doute avec UNV éloignée (recours à la télémédecine, "
                 "TM), <b>évaluation médicale</b> → choix de l'effecteur approprié.",
                 _c(219, 230, 242), NAVY),
    ]))
    story.append(Spacer(1, 1.5 * mm))
    story.append(KeepTogether([
        arrow(),
        flow_box("<b>Établissement destinataire</b> (l'un des 3 types, selon le tableau clinique "
                 "et l'organisation locale) : établissement disposant d'une UNV • établissement "
                 "disposant d'une UNV + neurochirurgie (NC) + neuroradiologie interventionnelle "
                 "(NRI) • établissement ayant structuré une filière de prise en charge des "
                 "patients suspects d'AVC en coordination avec une UNV. <b>Transport vers "
                 "l'établissement choisi par le moyen le plus rapide.</b>",
                 _c(197, 224, 240), TEAL_DARK, border_w=1.4),
    ]))
    story.append(Spacer(1, 1.5 * mm))
    story.append(KeepTogether([
        arrow(),
        flow_box("<b>À l'arrivée :</b> préparation de l'admission dans la filière organisée "
                 "(urgentistes, neurologues, radiologues, biologistes, réanimateurs), recherche "
                 "des contre-indications à la thrombolyse, puis <b>bilan clinique, biologique, "
                 "imagerie, évaluation pronostique, traitement.</b>", BG_PANEL, TEAL),
    ]))
    story.append(Spacer(1, 1 * mm))
    story.append(P("<i>Algorithme de l'annexe 1 (source), restructuré en séquence de boîtes (voir "
                    "disclosure méthodologique en tête de fiche). NC : neurochirurgie ; "
                    "NRI : neuroradiologie interventionnelle ; TM : télémédecine ; "
                    "UNV : unité neuro-vasculaire.</i>", S_NOTE))
    story.append(Spacer(1, 3 * mm))

    story.append(section_bar("5 — La thrombolyse des infarctus cérébraux", color=RED))
    story.append(Spacer(1, 2 * mm))
    story.append(P("<b>5.1 Thrombolyse intraveineuse (IV)</b>", S_CELL_B))
    story.append(Spacer(1, 1 * mm))
    story.append(prop_table([
        ("La thrombolyse IV par rt-PA des infarctus cérébraux est recommandée jusqu'à 4 h 30 "
         "(hors AMM, cf. annexe 2).", "AP"),
        ("Elle doit être effectuée le plus tôt possible.", "A"),
        ("Peut être envisagée après 80 ans jusqu'à 3 heures.", "AP"),
        ("En dessous de 18 ans : indications discutées au cas par cas avec un neurologue d'UNV.", "AP"),
        ("Une glycémie initiale &gt; 11 mmol/l doit conduire à réévaluer l'indication de la "
         "thrombolyse, du fait du risque hémorragique accru.", "C"),
        ("Les données actuelles ne permettent pas de recommander la sonothrombolyse. "
         "<i>(non gradé)</i>", "—"),
        ("Dans les établissements avec UNV : thrombolyse IV prescrite par un neurologue (AMM) "
         "et/ou un médecin titulaire du DIU de pathologie neuro-vasculaire (hors AMM) ; patient "
         "surveillé au sein de l'UNV.", "AP"),
        ("Dans les établissements sans UNV : indication portée par téléconsultation du médecin "
         "neuro-vasculaire de l'UNV où le patient sera transféré après thrombolyse (hors AMM).", "AP"),
    ]))
    story.append(Spacer(1, 2 * mm))
    story.append(P("<b>5.2 Thrombolyse intra-artérielle, combinée et revascularisation mécanique</b>",
                    S_CELL_B))
    story.append(Spacer(1, 1 * mm))
    story.append(prop_table([
        ("Décisions de thrombolyse intra-artérielle (IA) au cas par cas, après concertation entre "
         "neurologues vasculaires et neuroradiologues, jusqu'à 6 h pour les occlusions de "
         "l'artère cérébrale moyenne, voire au-delà pour les occlusions du tronc basilaire "
         "(gravité extrême) (hors AMM).", "AP"),
        ("La thrombolyse IA doit être réalisée dans un établissement disposant d'un centre de "
         "neuroradiologie interventionnelle autorisé (SIOS) et d'une UNV.", "AP"),
        ("La thrombolyse combinée (IV puis IA) et la revascularisation mécanique (thrombectomie "
         "ou ultrasons par voie endovasculaire) <b>ne sont pas recommandées</b> et doivent être "
         "évaluées. <i>(non gradé)</i>", "—"),
    ]))
    return story


def _section_annexe2_sources():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("Annexe 2 — Contre-indications de l'altéplase (RCP/AMM ACTILYSE®)",
                              color=GREY))
    story.append(Spacer(1, 1 * mm))
    story.append(P("<i>Extrait littéral du résumé des caractéristiques du produit (RCP), cité tel "
                    "quel par la source (guillemets d'origine).</i>", S_NOTE))
    story.append(Spacer(1, 2 * mm))
    story.append(P("« Hypersensibilité à la substance active ou à l'un des excipients. "
                    "Comme tous les agents thrombolytiques, ACTILYSE® est contre-indiqué dans "
                    "tous les cas associés à un risque hémorragique élevé :", S_CELL_B))
    cw = PAGE_W - 2 * MARGIN
    story.append(simple_table(
        ["Contre-indications générales (tout agent thrombolytique)"],
        [[x] for x in [
            "Trouble hémorragique significatif actuel ou au cours des 6 derniers mois",
            "Diathèse hémorragique connue",
            "Traitement concomitant par des anticoagulants oraux (ex. warfarine)",
            "Hémorragie sévère ou potentiellement dangereuse, manifeste ou récente",
            "Antécédents ou suspicion d'hémorragie intracrânienne",
            "Suspicion d'hémorragie sous-arachnoïdienne ou ATCD d'hémorragie sous-arachnoïdienne "
            "liée à un anévrisme",
            "Antécédents de lésion sévère du SNC (néoplasie, anévrisme, intervention chirurgicale "
            "intracérébrale ou intrarachidienne)",
            "Massage cardiaque externe traumatique récent (&lt; 10 jours), accouchement, ponction "
            "récente d'un vaisseau non accessible à la compression (ex. veine sous-clavière/jugulaire)",
            "Hypertension artérielle sévère non contrôlée",
            "Endocardite bactérienne, péricardite",
            "Pancréatite aiguë",
            "Ulcères gastro-intestinaux documentés au cours des 3 derniers mois, varices "
            "œsophagiennes, anévrisme artériel, malformations artérielles ou veineuses",
            "Néoplasie majorant le risque hémorragique",
            "Hépatopathie sévère (insuffisance hépatique, cirrhose, hypertension portale/varices "
            "œsophagiennes, hépatite évolutive)",
            "Intervention chirurgicale ou traumatismes importants au cours des 3 derniers mois",
        ]],
        [cw]))
    story.append(Spacer(1, 2 * mm))
    story.append(P("<b>Contre-indications complémentaires — AVC ischémique à la phase aiguë :</b>",
                    S_CELL_B))
    story.append(simple_table(
        ["Contre-indications spécifiques à l'AVC ischémique"],
        [[x] for x in [
            "Symptômes apparus plus de 3 heures avant l'initiation du traitement, ou heure "
            "d'apparition inconnue",
            "Déficit neurologique mineur ou symptômes s'améliorant rapidement avant l'initiation "
            "du traitement",
            "AVC jugé sévère cliniquement (ex. NIHSS &gt; 25) et/ou par imagerie",
            "Crise convulsive au début de l'AVC",
            "Signes d'hémorragie intracrânienne (HIC) au scanner",
            "Symptômes suggérant une hémorragie sous-arachnoïdienne, même en l'absence "
            "d'anomalie au scanner",
            "Administration d'héparine au cours des 48 heures précédentes avec un TCA dépassant "
            "la limite supérieure de la normale",
            "Patient diabétique présentant des antécédents d'AVC",
            "Antécédent d'AVC au cours des 3 derniers mois",
            "Plaquettes inférieures à 100 000/mm³",
            "PA systolique &gt; 185 mmHg ou PA diastolique &gt; 110 mmHg, ou traitement IV "
            "nécessaire pour réduire la PA à ces valeurs seuils",
            "Glycémie inférieure à 50 ou supérieure à 400 mg/dl",
        ]],
        [cw]))
    story.append(Spacer(1, 1 * mm))
    story.append(P("<i>Utilisation chez l'enfant, l'adolescent et le patient âgé : « ACTILYSE® "
                    "n'est pas indiqué pour le traitement de l'AVC à la phase aiguë chez les "
                    "patients de moins de 18 ans ou de plus de 80 ans » (la plupart des patients "
                    "inclus dans les essais contrôlés randomisés étaient âgés de 18 à 80 ans).</i>",
                    S_NOTE))
    story.append(Spacer(1, 4 * mm))

    story.append(section_bar("Sources et traçabilité", color=GREY))
    story.append(Spacer(1, 2 * mm))
    story.append(P(
        "<b>Document source :</b> « Accident vasculaire cérébral : prise en charge précoce "
        "(alerte, phase préhospitalière, phase hospitalière initiale, indications de la "
        "thrombolyse) » — Recommandations de bonne pratique, Haute Autorité de Santé (HAS), mai "
        "2009. Demandeurs : Société française neuro-vasculaire et Direction de l'hospitalisation "
        "et de l'organisation des soins. Promoteur : HAS, service des bonnes pratiques "
        "professionnelles. Présidente du groupe de travail : Dr France Woimant (neurologie, "
        "Paris). Validé par le Collège de la HAS en mai 2009.", S_SOURCE))
    story.append(Spacer(1, 2 * mm))
    story.append(P(
        "<b>Méthodologie :</b> grades HAS A/B/C (niveaux de preuve 1 à 4) + « accord "
        "professionnel » en l'absence d'études, méthode « Recommandations pour la pratique "
        "clinique » (RPC) — groupe de travail multidisciplinaire + groupe de lecture. 50 énoncés "
        "cliniques tagués dans les sections retranscrites (1× A, 2× B, 4× C, 43× accord "
        "professionnel), un pour un contre le texte source — voir disclosure méthodologique en "
        "page 1.", S_SOURCE))
    story.append(Spacer(1, 2 * mm))
    story.append(P(
        "<b>Couverture :</b> cette fiche reprend l'intégralité des chapitres cliniques du texte — "
        "introduction (champ, objectifs, populations, gradation), l'alerte, la phase "
        "préhospitalière, la phase hospitalière initiale (dont l'algorithme de l'annexe 1, "
        "restructuré en séquence de boîtes), la thrombolyse (IV, IA/combinée/mécanique), et "
        "l'annexe 2 (contre-indications de l'altéplase, extrait littéral du RCP/AMM). Les "
        "sections méthodologiques sans contenu clinique nouveau (méthode RPC, composition des "
        "groupes de travail/lecture — env. 85 noms, fiche descriptive) ne sont pas retranscrites.",
        S_SOURCE))
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Avertissement — document de 2009 :</b> ce document est une fiche de synthèse "
        "indépendante, produite pour un usage d'aide-mémoire. Elle reprend l'intégralité des "
        "recommandations cliniques du texte source, mais ne remplace pas le texte intégral "
        "(argumentaire complet, références bibliographiques) et n'est ni éditée ni validée par la "
        "HAS. <b>Les indications de la thrombolyse et les techniques de revascularisation "
        "mécanique ont évolué depuis 2009</b> (fenêtre thérapeutique élargie, thrombectomie "
        "mécanique désormais recommandée dans certaines indications) : se référer en complément "
        "aux recommandations plus récentes et à un avis neuro-vasculaire spécialisé en cas de "
        "doute.", S_BODY_SM), bg=BG_PANEL, border=GREY))
    return story


SECTIONS = [
    ("Introduction, alerte, phase préhospitalière & hospitalière initiale",
     lambda: _section_intro_alerte() + [Spacer(1, 2 * mm)] + _section_prehosp_hosp()),
    ("Algorithme & thrombolyse", _section_algo_thrombolyse),
    ("Annexe 2 & sources", _section_annexe2_sources),
]

def _make_doc(path=None):
    return SimpleDocTemplate(path or OUT, pagesize=A4,
                              leftMargin=MARGIN, rightMargin=MARGIN,
                              topMargin=32 * mm, bottomMargin=16 * mm,
                              title="HAS 2009 - AVC prise en charge precoce",
                              author="Synthèse indépendante (source HAS)")

def _silent_page(canvas, doc_):
    pass

def _build_upto(section_fns):
    # Forcing a PageBreak before every top-level section left pages 3, 5 and 7
    # severely underfull (~15-20%) - each section's trailing content was a
    # short table tail before the forced break. Letting content flow
    # continuously (no forced break) lets the next section's content climb
    # onto that remaining whitespace instead.
    story = []
    for i, fn in enumerate(section_fns):
        if i > 0:
            story.append(Spacer(1, 4 * mm))
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
