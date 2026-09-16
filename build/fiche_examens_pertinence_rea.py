# -*- coding: utf-8 -*-
"""
Fiche de synthese - RFE commune SFAR-SRLF, "Pertinence de la prescription
des examens biologiques et de la radiographie thoracique en reanimation".
Texte valide par le CA de la SFAR (15/12/2016) et de la SRLF (13/12/2016).
26 pages source, telecharge depuis sfar.org (wp-content/uploads/2017/01/
2_RFE-EC-en-rea-version-15-12-16.pdf).

METHODOLOGIE : methode GRADE (r), grille EBM standard (qualite des
preuves haute/moderee/basse/tres basse ; formulation binaire forte/faible,
Grade 1+/1-/2+/2-), methode PICO pour le decoupage des questions,
cotation Delphi/GRADE Grid. 8 "champs" d'application identifies par les
experts.

INCOHERENCE DE COMPTAGE SOURCE DISCLOSED (regle 5, jamais resolue
silencieusement) : le preambule de la source annonce "49 recommandations
... formalisees", "accord fort pour 40 d'entre elles, et ... accord
faible pour 1 d'entre elles", et "3 cas [ou] aucune recommandation n'a ...
ete formulee". Un tally direct et exhaustif du corps du texte (grep
"^R[0-9]+\\.[0-9]+" + verification manuelle) donne 42 items numerotes
uniques (R1.1 a R8.4, avec un trou reel a R7.11 - voir ci-dessous), dont
38 portent un grade explicite (37 "Accord fort" + 1 "Accord faible",
comptage grep confirme egal au nombre de tags Grade 1+/1-/2+/2- : 14+8+
11+5=38) et 4 portent la mention "Avis d'expert" sans grade GRADE (R1.1,
R1.2, R3.1, R3.2). A cela s'ajoutent exactement 3 cas explicites "aucune
recommandation ne peut/n'a pu etre formulee" (troponine hors
postoperatoire, peptides natriuretiques hors postoperatoire,
hemocultures sous hypothermie therapeutique/EER continue) - ce chiffre de
3 correspond exactement a l'annonce de la source. Mais 42 (numerotes) +
3 (sans recommandation) = 45, pas 52 (=49+3) attendu par la source, et le
compte "accord fort 40 / accord faible 1" (41) ne correspond pas non plus
aux 38 grades trouves. Divergence disclosed telle quelle, non resolue -
cette fiche liste les 42 items numerotes exacts de la source, dans leur
numerotation native.

ANOMALIE DE NUMEROTATION SOURCE DISCLOSED : apres R7.10, la source
n'a PAS de "R7.11" - l'item suivant est imprime "R 7.2.5 concernant les
modes de prelevement, les experts renvoient a la recommandation Q2 de la
recommandation SRLF-SFAR «Strategies de reduction de l'utilisation des
antibiotiques...»" - un renvoi vers un autre document SFAR-SPILF, SANS
tag de grade (pas de case "Accord fort/faible" associee, contrairement a
tous les autres items R7.x) et avec une numerotation qui ne suit pas la
sequence R7.x (verifie visuellement sur le rendu PDF a 200dpi, page 15 -
pas un artefact d'extraction texte). Retranscrit ici tel quel (comme un
renvoi, pas une recommandation gradee fabriquee), avec cette numerotation
native "R 7.2.5" preservee et disclosed comme anomalie source, jamais
renumerotee en "R7.11" par cette fiche.

PORTEE : couverture complete des 42 items numerotes (R1.1-R8.4) et des 3
cas explicites "aucune recommandation possible", organises par les 8
champs natifs de la source. Argumentaire tres fortement condense (regle
de projet 2026-09-14) - la source consacre un paragraphe d'argumentaire
bibliographique dense par champ (dizaines de references par champ, ex.
Champ 3 PCT seule cite 10 references) ; seuls les seuils/chiffres
directement actionnables sont conserves (ex. volumes de sang pour
hemocultures, seuils PCT/troponine/BNP, delais ECBU) - pas le detail
etude-par-etude.

AUDIT INDEPENDANT (subagent, aveugle au brouillon, verification
systematique des 42 grades un par un) : les 42 grades, les 4 items "avis
d'expert", les 3 cas "aucune recommandation possible", l'anomalie
R 7.2.5, la divergence de comptage disclosed (49 annonces vs 42 comptes,
re-derivee independamment par grep et confirmee identique), et tous les
seuils cliniques critiques verifies (RCRI R4.1 vs R5.1 non confondus,
volumes hemocultures, fenetre de detection troponine, incidence TIH)
confirmes exacts - aucune erreur HIGH. Une seule correction MEDIUM
apportee : la note "Repere" du Champ 6 associait a tort la qualification
"contexte chirurgical/traumatique" au protocole de surveillance
plaquettaire sous HNF (2x/semaine, 21 jours) - dans la source, cette
qualification appartient au protocole HBPM (document HAS, rythme
different), un protocole distinct que la fiche avait involontairement
fusionne avec celui de l'HNF. Chaque chiffre pris isolement etait exact ;
seul le lien conditionnel entre les deux etait errone - corrige en
separant explicitement les deux protocoles.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from style import *
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.units import mm

OUT = "/home/user/rfe-sfar-website/output/Fiche_SFAR_SRLF_Pertinence_Examens_Reanimation_2017.pdf"

SOURCE_TXT = ("Source : « Pertinence de la prescription des examens biologiques et de la "
              "radiographie thoracique en réanimation » — RFE commune SFAR-SRLF, validée "
              "12/2016 (publiée 2017). Fiche de synthèse non officielle : se référer au texte "
              "intégral.")

def P(txt, style=S_CELL):
    return Paragraph(txt, style)

def chip(label):
    return grade_chip(label, width=13 * mm, fontsize=8.6)

CW_FULL = PAGE_W - 2 * MARGIN

def reco_table(rows, col_widths):
    """rows: (ref, text, grade_label)."""
    data = [[P("N°", S_HEAD_W_C), P("Recommandation", S_HEAD_W), P("Grade", S_HEAD_W_C)]]
    for ref, txt, grade in rows:
        data.append([P(ref, S_CELL_B), P(txt, S_CELL), chip(grade)])
    t = Table(data, colWidths=col_widths, repeatRows=1)
    style_cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), NAVY), ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTNAME", (0, 0), (-1, 0), FONT_BOLD), ("FONTSIZE", (0, 0), (-1, 0), 8),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("ALIGN", (0, 0), (0, -1), "CENTER"),
        ("ALIGN", (2, 0), (2, -1), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 0.5, GREY_LIGHT),
        ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            style_cmds.append(("BACKGROUND", (0, i), (-1, i), BG_PANEL))
    t.setStyle(TableStyle(style_cmds))
    return t

RCW = [15 * mm, CW_FULL - 15 * mm - 15 * mm, 15 * mm]

def no_rec_note(txt):
    return info_panel(P("<b>Aucune recommandation possible</b> (source) : " + txt, S_BODY_SM),
                       bg=AMBER_LIGHT, border=AMBER)

def legend_flowable():
    chip_w = 13 * mm
    content_w = CW_FULL
    col_txt1 = 42 * mm
    col_txt2 = 46 * mm
    col_txt3 = content_w - 3 * chip_w - col_txt1 - col_txt2
    data = [
        [chip("1+"), P("<b>1+</b> Il faut faire (fort).", S_BADGE_HEAD),
         chip("1-"), P("<b>1-</b> Il ne faut pas faire (fort).", S_BADGE_HEAD),
         chip("AE"), P("<b>AE</b> Avis d'expert (pas de grade GRADE).", S_BADGE_HEAD)],
        [chip("2+"), P("<b>2+</b> Il faut probablement faire (faible).", S_BADGE_HEAD),
         chip("2-"), P("<b>2-</b> Il ne faut probablement pas faire (faible).", S_BADGE_HEAD),
         P("", S_BADGE_HEAD), P("", S_BADGE_HEAD)],
    ]
    row = Table(data, colWidths=[chip_w, col_txt1, chip_w, col_txt2, chip_w, col_txt3])
    row.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                              ("LEFTPADDING", (0, 0), (-1, -1), 1),
                              ("RIGHTPADDING", (0, 0), (-1, -1), 3),
                              ("TOPPADDING", (0, 0), (-1, -1), 1.5),
                              ("BOTTOMPADDING", (0, 0), (-1, -1), 1.5)]))
    return row

TOTAL_PAGES = {"n": 10}

def on_page(canvas, doc, page_title):
    header_band(canvas, doc, "SFAR — SRLF, RFE, MÉTHODE GRADE, 2016/2017",
                "Pertinence des examens en réanimation",
                page_title, icon_fn=lambda c, x, y: icon_drop(c, x, y, 13 * mm), color=TEAL_DARK)
    footer_band(canvas, doc, SOURCE_TXT, f"Page {doc.page} / {TOTAL_PAGES['n']}")

# ---------------------------------------------------------------------------
def _section_intro_champ1_2():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Résumé :</b> RFE commune SFAR-SRLF (méthode GRADE) sur la pertinence de la "
        "prescription des examens biologiques et de la radiographie thoracique (RT) au lit en "
        "réanimation — objectif de réduire la spoliation sanguine, les coûts et les risques liés "
        "au transport/à l'irradiation, sans compromettre la sécurité des patients. 8 champs : "
        "bilan d'entrée, bilan quotidien, biomarqueurs du sepsis, troponine, peptides "
        "natriurétiques, hémostase, examens bactériologiques, radiographie thoracique.",
        S_BODY), bg=BG_PANEL, border=TEAL))
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("Méthodologie"))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "Méthode GRADE® — qualité des preuves en 4 catégories (haute/modérée/basse/très "
        "basse), formulation binaire forte/faible, méthode PICO pour cibler chaque question, "
        "cotation Delphi/GRADE Grid. <i>Note de comptage (règle 5, disclosed) :</i> la source "
        "annonce « 49 recommandations formalisées » (« accord fort » pour 40, « accord "
        "faible » pour 1) et 3 cas sans recommandation possible — le compte direct des items "
        "numérotés du corps du texte donne <b>42</b> (38 gradés + 4 « avis d'expert ») + "
        "3 cas sans recommandation confirmés = 45, pas 52 attendu. Divergence non "
        "réconciliable, disclosed telle quelle ; cette fiche liste les 42 items exacts, dans "
        "la numérotation native de la source.", S_BODY_SM))
    story.append(Spacer(1, 1.5 * mm))
    story.append(legend_flowable())
    story.append(Spacer(1, 2.5 * mm))
    story.append(section_bar("Champ 1 — Bilan d'entrée systématique en réanimation ?"))
    story.append(Spacer(1, 1.5 * mm))
    story.append(reco_table([
        ("R1.1", "Réduire autant que possible le nombre de prélèvements sanguins à "
         "l'admission et au quotidien, afin de réduire la spoliation sanguine et le coût "
         "lié aux examens.", "AE"),
        ("R1.2", "Rechercher systématiquement une éventuelle grossesse à l'admission, "
         "soit par l'interrogatoire, soit par un dosage de β-hCG urinaire ou quantitatif "
         "sanguin.", "AE"),
    ], RCW))
    story.append(Spacer(1, 2.5 * mm))
    story.append(section_bar("Champ 2 — Bilan quotidien systématique en réanimation ?"))
    story.append(Spacer(1, 1.5 * mm))
    story.append(reco_table([
        ("R2.1", "Il ne faut probablement pas réaliser de façon systématique et "
         "quotidienne l'ensemble des examens biologiques (NFS, ionogrammes sanguin et "
         "urinaire, gazométrie, bilan hépatique).", "2-"),
        ("R2.2", "Il faut discuter la réalisation des examens biologiques à chaque "
         "évaluation clinique, en vue de restreindre leur nombre.", "1+"),
        ("R2.3", "Il faut probablement réaliser un ionogramme sanguin et urinaire, une "
         "numération sanguine et des gaz du sang artériels quotidiennement chez les "
         "patients instables sur le plan hémodynamique, rénal ou respiratoire.", "2+"),
        ("R2.4", "Il faut probablement écrire un protocole de service pour réduire le "
         "nombre d'examens biologiques et faire connaître le coût des prescriptions.",
         "2+"),
    ], RCW))
    return story

def _section_champ3_4_5():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("Champ 3 — Quels biomarqueurs du sepsis utiliser ?"))
    story.append(Spacer(1, 1.5 * mm))
    story.append(reco_table([
        ("R3.1", "La procalcitonine (PCT), comme tout biomarqueur, ne doit pas être "
         "utilisée ni interprétée indépendamment de l'ensemble des éléments cliniques et "
         "paracliniques, mais s'intégrer dans une démarche globale de prise en charge.",
         "AE"),
        ("R3.2", "Compte tenu de son manque de spécificité, l'utilisation de la CRP "
         "n'est pas recommandée chez tous les patients de réanimation.", "AE"),
        ("R3.3", "Il ne faut pas doser la PCT dans les sepsis évidents dans le seul but "
         "d'en étayer le diagnostic — une valeur précoce peut néanmoins servir de "
         "référence pour la gestion ultérieure de l'antibiothérapie (arrêt plus rapide "
         "ou modification).", "1-"),
        ("R3.4", "Dans certaines situations particulières (patients chirurgicaux, "
         "infections intra-abdominales), l'intérêt de la PCT n'est pas clairement "
         "établi et son utilisation n'est pas recommandée en routine.", "1-"),
    ], RCW))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<i>Repère :</i> une stratégie d'arrêt/non-introduction de l'antibiothérapie basée sur "
        "un seuil de PCT s'est avérée efficace et sûre dans les SIRS d'allure infectieuse sans "
        "foyer ni documentation microbiologique ; la cinétique de la PCT peut aussi réduire la "
        "durée d'antibiothérapie dans les infections confirmées, sans surmortalité.", S_NOTE))
    story.append(Spacer(1, 2.5 * mm))
    story.append(section_bar("Champ 4 — Troponine en dehors de modifications du segment ST"))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P("<i>En contexte postopératoire (hors chirurgie cardiaque) :</i>",
                    S_BODY_SM))
    story.append(Spacer(1, 1 * mm))
    story.append(reco_table([
        ("R4.1", "Il ne faut pas doser systématiquement la troponine en postopératoire "
         "pour les chirurgies à faible risque cardiaque (&lt;1 %). Pour les chirurgies à "
         "risque intermédiaire ou élevé, il ne faut pas la doser systématiquement chez "
         "les patients à faible risque cardiaque (Revised Cardiac Risk Index de Lee "
         "≤1).", "1-"),
        ("R4.2", "Lorsque le motif d'admission en réanimation/surveillance continue est "
         "la gestion du risque cardiaque postopératoire, il faut doser systématiquement "
         "la troponine — la période du jour de l'opération au 3<sup>e</sup> jour "
         "postopératoire est la meilleure fenêtre de détection.", "1+"),
    ], RCW))
    story.append(Spacer(1, 1.5 * mm))
    story.append(no_rec_note(
        "hors contexte postopératoire, il n'est pas possible de formuler de recommandation "
        "sur le dosage systématique de la troponine en réanimation (données insuffisantes "
        "sur le gain pronostique additionnel aux scores de gravité usuels)."))
    story.append(Spacer(1, 2.5 * mm))
    story.append(section_bar("Champ 5 — Place des peptides natriurétiques"))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P("<i>En contexte postopératoire (hors chirurgie cardiaque) :</i>",
                    S_BODY_SM))
    story.append(Spacer(1, 1 * mm))
    story.append(reco_table([
        ("R5.1", "Il ne faut pas doser systématiquement les peptides natriurétiques en "
         "période postopératoire des chirurgies à faible risque cardiaque (&lt;1 %). "
         "Pour les chirurgies à risque intermédiaire/élevé, il ne faut pas les doser "
         "systématiquement chez les patients à faible risque cardiaque (RCRI &lt;2) ou "
         "à très haut risque (RCRI &gt;3).", "1-"),
    ], RCW))
    story.append(Spacer(1, 1.5 * mm))
    story.append(no_rec_note(
        "hors contexte postopératoire, la littérature ne permet de formuler aucune "
        "recommandation sur l'utilisation du BNP — en particulier pour le dépistage d'une "
        "dysfonction cardiaque induite par le sepsis ou d'une cause cardiaque à un échec de "
        "sevrage ventilatoire, malgré des pistes intéressantes (élévation du BNP associée à "
        "un échec d'épreuve de ventilation spontanée dans plusieurs études)."))
    return story

def _section_champ6_7a():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("Champ 6 — Quand prescrire un bilan d'hémostase ?"))
    story.append(Spacer(1, 1.5 * mm))
    story.append(reco_table([
        ("R6.1", "Il faut probablement disposer d'un bilan d'hémostase (TP, TCA, "
         "plaquettes) chez tout patient admis en réanimation.", "2+"),
        ("R6.2", "Il ne faut probablement pas répéter systématiquement les examens "
         "d'hémostase une fois le bilan initial prélevé.", "2-"),
        ("R6.3", "Il faut répéter les examens d'hémostase en cas d'anomalies ou de "
         "survenue d'une affection aiguë pouvant interférer avec l'hémostase.", "1+"),
        ("R6.4", "Il ne faut pas effectuer systématiquement de surveillance biologique "
         "de l'activité anticoagulante des traitements utilisés à dose préventive "
         "(prophylaxie de la MTEV), en dehors de la surveillance plaquettaire lorsque "
         "celle-ci est indiquée.", "1-"),
        ("R6.5", "Il faut probablement surveiller l'effet anticoagulant d'un traitement "
         "par héparine non fractionnée à doses thérapeutiques par la mesure de "
         "l'activité anti-Xa plutôt que par le TCA.", "2+"),
    ], RCW))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<i>Repère :</i> la corrélation TCA/activité anti-Xa est mauvaise (discordante dans "
        "près de la moitié des cas sous HNF). La thrombopénie induite par l'héparine (TIH) "
        "complique jusqu'à 5 % des traitements par HNF et 0,1-0,2 % des HBPM. Sous HNF, "
        "quelle que soit la dose, surveillance plaquettaire systématique 2×/semaine pendant "
        "21 jours. Sous HBPM, se référer au document HAS : rythme différent selon le "
        "contexte (chirurgical/traumatique ou non).", S_NOTE))
    story.append(Spacer(1, 2.5 * mm))
    story.append(section_bar("Champ 7 — Examens bactériologiques standards (1/2 : hémocultures)"))
    story.append(Spacer(1, 1.5 * mm))
    story.append(reco_table([
        ("R7.1", "Il faut prélever des hémocultures devant tout sepsis.", "1+"),
        ("R7.2", "Il ne faut probablement pas répéter ces prélèvements de manière "
         "systématique.", "2-"),
        ("R7.3", "Il faut probablement prélever de nouvelles hémocultures 24h après la "
         "première série en cas de suspicion d'endocardite ou de syndrome infectieux "
         "persistant avec premières hémocultures restant négatives après 24h "
         "d'incubation.", "1+"),
        ("R7.4", "Il faut probablement réduire le nombre de paires d'hémocultures à "
         "2-3 par épisode clinique et par tranche de 24h, pour réduire coûts et "
         "spoliation sanguine.", "2+"),
        ("R7.5", "Il faut prélever par ponction veineuse directe, en une seule fois, un "
         "volume minimum de 40 à 60 mL et le répartir dans 4 à 6 flacons (2-3 aérobies, "
         "2-3 anaérobies), pour minimiser faux positifs (défaut d'antisepsie) et faux "
         "négatifs (volume insuffisant).", "1+"),
    ], RCW))
    story.append(Spacer(1, 1.5 * mm))
    story.append(no_rec_note(
        "sur le prélèvement d'hémocultures systématiques en cas de traitements interférant "
        "avec le monitorage de la température (hypothermie thérapeutique, épuration "
        "extra-rénale continue)."))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<i>Repère :</i> 3 paires d'hémocultures détectent 98 % des bactériémies (contre "
        "73 % avec 1 paire, 90 % avec 2) ; c'est le volume prélevé, pas le nombre de "
        "ponctions, qui conditionne la sensibilité — 20 mL augmente le taux de positivité de "
        "30 % par rapport à 10 mL (minimum souhaitable chez l'adulte).", S_NOTE))
    return story

def _section_champ7b():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("Champ 7 (2/2) — Prélèvements pulmonaires, ECBU, coproculture"))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P("<i>Prélèvements pulmonaires (pneumonies nosocomiales, patients "
                    "immunodéprimés exclus) :</i>", S_BODY_SM))
    story.append(Spacer(1, 1 * mm))
    story.append(reco_table([
        ("R7.6", "Il faut réaliser des prélèvements microbiologiques pulmonaires "
         "uniquement en cas de suspicion de pneumonie nosocomiale, en respectant les "
         "conditions de prélèvement/acheminement pour une interprétation fiable.", "1+"),
        ("R7.7", "Il faut probablement réaliser des prélèvements pulmonaires devant "
         "toute suspicion de pneumonie nosocomiale pour identifier le germe et adapter "
         "l'antibiothérapie.", "2+"),
        ("R7.8", "Il ne faut pas répéter les prélèvements pulmonaires en cas "
         "d'évolution favorable d'une pneumonie nosocomiale.", "1+"),
        ("R7.9", "Il ne faut probablement pas réaliser de prélèvements pulmonaires de "
         "« dépistage » systématiques, y compris chez les patients en SDRA.", "2-"),
        ("R7.10", "Il faut probablement dépister la grippe, même en situation "
         "nosocomiale, en cas de contexte épidémique ou de notion de contage, en "
         "particulier chez les patients avec comorbidités respiratoires ou "
         "cardiovasculaires.", "2+"),
    ], RCW))
    story.append(Spacer(1, 1.5 * mm))
    story.append(info_panel(P(
        "<b>R 7.2.5</b> (numérotation et absence de grade telles qu'imprimées dans la "
        "source — anomalie disclosed, non renumérotée « R7.11 ») : concernant les modes de "
        "prélèvement pulmonaire, les experts renvoient à la recommandation Q2 de la "
        "recommandation SRLF-SFAR-SPILF « Stratégies de réduction de l'utilisation des "
        "antibiotiques à visée curative en réanimation ».", S_BODY_SM),
        bg=GREY_LIGHT, border=GREY))
    story.append(Spacer(1, 2 * mm))
    story.append(P("<i>Examen cytobactériologique des urines (ECBU) :</i>", S_BODY_SM))
    story.append(Spacer(1, 1 * mm))
    story.append(reco_table([
        ("R7.12", "Il faut réaliser un ECBU à visée diagnostique en présence de signes "
         "cliniques d'infection urinaire compliquée (pyélonéphrite aiguë, prostatite) "
         "ou en cas de sepsis sans autre porte d'entrée identifiée.", "1+"),
        ("R7.13", "Il ne faut pas réaliser d'ECBU de contrôle 48-72h après le début de "
         "l'antibiothérapie, sauf en cas de non-réponse clinique au traitement.", "1-"),
        ("R7.14", "Il ne faut pas dépister systématiquement les colonisations "
         "urinaires (bandelette ou ECBU), en dehors de situations à risque (femmes "
         "enceintes, intervention chirurgicale sur les voies urinaires).", "1+"),
    ], RCW))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P("<i>Coproculture :</i>", S_BODY_SM))
    story.append(Spacer(1, 1 * mm))
    story.append(reco_table([
        ("R7.15", "Il faut réaliser une coproculture standard en cas de selles "
         "diarrhéiques uniquement si le patient est hospitalisé depuis moins de "
         "3 jours.", "1+"),
        ("R7.16", "Il ne faut pas réaliser de coproculture standard de contrôle en cas "
         "de première coproculture négative, même si les diarrhées persistent (toutes "
         "les diarrhées n'étant pas d'origine infectieuse).", "2-"),
        ("R7.17", "Il faut rechercher d'autres bactéries entéropathogènes si la "
         "coproculture standard est négative en cas de contexte particulier précisé dès "
         "l'entrée : voyage récent en pays tropical, toxi-infection alimentaire "
         "collective, syndrome cholériforme ou diarrhée hémorragique.", "1+"),
        ("R7.18", "Il ne faut pas réaliser de coproculture standard chez le patient "
         "hospitalisé depuis plus de 3 jours, excepté en cas d'immunodépression.", "2+"),
        ("R7.19", "Il faut rechercher des micro-organismes particuliers en cas de "
         "diarrhée secondaire à un traitement antibiotique (Clostridium difficile, "
         "Klebsiella oxytoca, Pseudomonas aeruginosa, Candida albicans, Clostridium "
         "perfringens producteur d'entérotoxine).", "1+"),
        ("R7.20", "Il faut rechercher le Clostridium difficile de façon spécifique, "
         "sans l'associer à la demande d'une coproculture standard (contexte "
         "totalement différent).", "1+"),
        ("R7.21", "Il ne faut pas réitérer la recherche de Clostridium difficile "
         "lorsqu'elle est positive.", "1-"),
    ], RCW))
    return story

def _section_champ8_sources():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("Champ 8 — Prescrire une radiographie thoracique (RT) au lit ?"))
    story.append(Spacer(1, 1.5 * mm))
    story.append(reco_table([
        ("R8.1", "Il ne faut pas faire de RT au lit quotidienne systématique chez les "
         "patients intubés et ventilés.", "1-"),
        ("R8.2", "Il faut probablement réaliser une RT en cas d'altération des échanges "
         "gazeux, d'augmentation des pressions d'insufflation (pression de plateau) ou "
         "de modifications auscultatoires faisant suspecter une anomalie "
         "parenchymateuse/pleurale — bien que le scanner (voire l'échographie "
         "pulmonaire) soit vraisemblablement supérieur.", "2+"),
        ("R8.3", "Il faut probablement faire une RT au décours de la pose de "
         "dispositifs invasifs (sonde d'intubation, canule de trachéotomie, cathéter "
         "veineux central en territoire cave supérieur, drain thoracique, sonde "
         "gastrique) pour en vérifier la position et l'absence de complications.",
         "2+"),
        ("R8.4", "Il faut probablement envisager l'échographie thoracique comme "
         "alternative à la RT pour détecter des anomalies pleurales (pneumothorax, "
         "pleurésie) voire parenchymateuses (foyer, atélectasie).", "2+"),
    ], RCW))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<i>Repère :</i> une stratégie de RT « à la demande » (sur critères cliniques ou "
        "gazométriques) est efficace et sûre par rapport à la RT quotidienne systématique "
        "(pas de différence de durée de ventilation ni de mortalité). La RT systématique à "
        "l'admission pour détresse respiratoire n'est pas non plus justifiée (scanner plus "
        "performant, échographie cardiaque/pulmonaire rapide et précise) — la RT "
        "d'admission doit être réservée aux situations où scanner et échographie ne "
        "peuvent être réalisés.", S_NOTE))
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("Sources et traçabilité", color=GREY))
    story.append(Spacer(1, 2 * mm))
    story.append(P(
        "<b>Document source :</b> « Pertinence de la prescription des examens biologiques et "
        "de la radiographie thoracique en réanimation » — RFE commune SFAR-SRLF. Texte "
        "validé par le CA de la SFAR (15/12/2016) et de la SRLF (13/12/2016).", S_SOURCE))
    story.append(Spacer(1, 1 * mm))
    story.append(P("<b>Méthodologie :</b> méthode GRADE®, méthode PICO — voir détail en "
                    "page 1.", S_SOURCE))
    story.append(Spacer(1, 1 * mm))
    story.append(P(
        "<b>URL source :</b> https://sfar.org/wp-content/uploads/2017/01/2_RFE-EC-en-rea-"
        "version-15-12-16.pdf", S_SOURCE))
    story.append(Spacer(1, 1 * mm))
    story.append(P(
        "<b>Couverture :</b> intégralité des 42 items numérotés (R1.1-R8.4, y compris "
        "l'anomalie de numérotation « R 7.2.5 ») et des 3 cas explicites « aucune "
        "recommandation possible » — voir disclosure de la divergence de comptage source "
        "(49 annoncées vs 42 comptées) en page 1.", S_SOURCE))
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Avertissement — document validé 2016/2017 :</b> cette fiche de synthèse "
        "indépendante reprend l'intégralité des recommandations du texte source, mais ne le "
        "remplace pas et n'est ni éditée ni validée par la SFAR ou la SRLF. Se référer aux "
        "protocoles locaux et au texte intégral (106 références bibliographiques, non "
        "reprises ici) pour toute décision clinique.", S_BODY_SM), bg=GREY_LIGHT, border=GREY))
    return story

def _section_full():
    return (_section_intro_champ1_2() + _section_champ3_4_5() + _section_champ6_7a()
            + _section_champ7b() + _section_champ8_sources())

SECTIONS = [
    ("Méthodologie, 8 champs, 42 recommandations & sources", _section_full),
]

def _make_doc(path=None):
    return SimpleDocTemplate(path or OUT, pagesize=A4,
                              leftMargin=MARGIN, rightMargin=MARGIN,
                              topMargin=32 * mm, bottomMargin=16 * mm,
                              title="Fiche SFAR-SRLF 2017 - Pertinence des examens en reanimation",
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

    doc = _make_doc()
    story = _build_upto(fns)
    doc.build(story, onFirstPage=on_page_final, onLaterPages=on_page_final)
    print("OK ->", OUT, f"({total_pages} pages)")

if __name__ == "__main__":
    build()
