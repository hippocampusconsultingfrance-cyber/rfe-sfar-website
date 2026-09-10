# -*- coding: utf-8 -*-
"""
Fiche de synthese - Recommandations formalisees d'experts (RFE) SFAR, 2012 :
"Examens preinterventionnels systematiques".
Source : sources/examens_preinterventionnels.pdf (12 pages, Ann Fr Anesth
Reanim 2012;31:752-763), sources/examens_preinterventionnels.txt (texte
extrait integralement, 64796 caracteres). Validee par l'AFC, l'AFU, le
CNGOF, l'EFS, la SCGP, la SFC, la SFCD, le GEHT, la SF2H, la SOFOP, la
SFORL, la SFR-FRI, la SFSCMF et la SPLF. Pas de tampon d'obsolescence
detecte ; library_final.json marque ce document "en vigueur".

METHODOLOGIE - GRADE 1+/1-/2+/2- (chip standard deja dans
style.GRADE_COLORS). VERIFIE PAR grep SUR LE TEXTE APLATI (espaces
normalises, insensible aux retours a la ligne) : 41 occurrences "grade [0-9]"
dont 3 non appliquees (1x reference de methode "methode GRADE1" avec appel
de note, 2x description de l'echelle elle-meme "GRADE 1+ ou 1-"/"GRADE 2+ ou
2-" au chapitre methodologie) - 38 appliquees a une recommandation precise.

DISCLOSURE - LA SOURCE ELLE-MEME OMET LE SIGNE +/- SUR 13 DE CES 38 TAGS
(elle ecrit juste "(GRADE 1)" ou "(GRADE 2)" sans signe) : Retranscrit ici en
resolvant le signe a partir du sens univoque de la phrase elle-meme ("il est
recommande de NE PAS prescrire..." = signe negatif), jamais invente au
niveau (1 vs 2, toujours explicite dans la source) : les 12 "GRADE 1" nus
sont tous rattaches a une formulation negative ("ne pas prescrire"/"n'est
pas recommande") -> retranscrits "1-", coherent avec les 2 autres tags "GRADE
1-" explicitement signes ailleurs dans le MEME document pour des
recommandations negatives strictement analogues (R4 hemogramme, R5
groupage/RAI) qui confirment que ce signe est la convention reelle du
document, pas une supposition. Le seul "GRADE 2" nu (R9, analyse d'urine
risque faible) est de meme resolu en "2-" (formulation "il est probablement
recommande de NE PAS pratiquer"). Total final verifie : 14x1+, 14x1-, 9x2+,
1x2- = 38/38.

PERIMETRE - integralite des 9 recommandations (examens cardiologiques,
respiratoires, hemostase, hemogramme, immunohematologiques, biochimiques,
femme enceinte en prepartum, test de grossesse, depistage infectieux ECBU),
le tableau 1 (indications ECBU/BU) et le tableau 2 (synthese par risque
ASA x type de chirurgie), et l'annexe A (stratification du risque cardiaque
ACC/AHA, deja utilisee comme reference par le texte lui-meme). Comite
d'organisation / groupe de travail / references bibliographiques [1]-[3]
non retranscrits (sans contenu clinique).

_count_pages() : pattern copie de fiche_traumatisme_cranien_grave_precoce.py
(PyMuPDF/fitz, jamais vers OUT, toujours vers tempfile.mktemp()).
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from style import *
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.units import mm

OUT = "/home/user/rfe-sfar-website/output/Fiche_SFAR_Examens_Preinterventionnels_Systematiques_2012.pdf"

SOURCE_TXT = ("Source : SFAR — RFE « Examens préinterventionnels systématiques » (Ann Fr Anesth Reanim "
              "2012;31:752-763). Fiche de synthèse non officielle : se référer au texte intégral.")

def P(txt, style=S_CELL):
    return Paragraph(txt, style)

def chip(label, **kw):
    return grade_chip(label, **kw)

REF_W = 15 * mm
GRADE_W = 14 * mm

def reco_table(rows, col_widths=None):
    """rows: (ref, text, grade_label) - grade_label parmi '1+','1-','2+','2-'."""
    text_w = PAGE_W - 2 * MARGIN - REF_W - GRADE_W
    cw = col_widths or [REF_W, text_w, GRADE_W]
    data = [[P("Réf.", S_HEAD_W_C), P("Recommandation (texte condensé, fidèle à la source)", S_HEAD_W),
              P("Grade", S_HEAD_W_C)]]
    for ref, txt, grade in rows:
        data.append([P(ref, S_CELL_C), P(txt, S_CELL), chip(grade, width=GRADE_W - 2 * mm)])
    t = Table(data, colWidths=cw, repeatRows=1)
    style_cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), NAVY), ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTNAME", (0, 0), (-1, 0), FONT_BOLD), ("FONTSIZE", (0, 0), (-1, 0), 8),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("ALIGN", (0, 0), (0, -1), "CENTER"),
        ("ALIGN", (2, 0), (2, -1), "CENTER"),
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

TOTAL_PAGES = {"n": 5}

def on_page(canvas, doc, page_title):
    header_band(canvas, doc, "SFAR — RFE 2012 — FICHE DE SYNTHÈSE",
                "Examens préinterventionnels systématiques",
                page_title, icon_fn=lambda c, x, y: icon_pill(c, x, y, 13 * mm), color=TEAL_DARK)
    footer_band(canvas, doc, SOURCE_TXT, f"Page {doc.page} / {TOTAL_PAGES['n']}")

# ---------------------------------------------------------------------------
def _section_intro_r1_r2():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Champ :</b> prescription des examens complémentaires <b>préinterventionnels "
        "systématiques</b> — réalisés en routine, en dehors de signes d'appel anamnestiques ou "
        "cliniques, avant une intervention chirurgicale ou une procédure non chirurgicale sous "
        "anesthésie. <b>Exclut</b> les examens spécifiques à l'acte ou à la pathologie du patient "
        "(ex. EFR avant résection pulmonaire), la chirurgie cardiaque/de résection pulmonaire/"
        "intracrânienne, la médecine préventive, et les nouveau-nés (0-28 jours). Actualisation "
        "SFAR 2012 des recommandations Anaes de 1998, validée par 14 sociétés savantes. "
        "Stratification selon le <b>type de chirurgie</b> (risque cardiaque ACC/AHA : faible "
        "&lt;1 %, intermédiaire 1-5 %, élevé &gt;5 % — Annexe A) et la <b>classe ASA</b> du "
        "patient.", S_BODY), bg=BG_PANEL, border=TEAL_DARK))
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Méthodologie GRADE</b> (même schéma que le reste du corpus) : Grade 1+/1- (forte, "
        "« il faut faire/ne pas faire ») ; Grade 2+/2- (faible, « il est possible de faire/ne pas "
        "faire »). <b>Vérifié par grep exhaustif : 38 recommandations tagués (14× 1+, 14× 1-, "
        "9× 2+, 1× 2-).</b> <b>Disclosure :</b> la source omet le signe +/- sur 13 de ces 38 tags "
        "(elle écrit juste « GRADE 1 » ou « GRADE 2 ») ; le signe est ici résolu à partir du sens "
        "univoque de chaque phrase (« il est recommandé de <b>ne pas</b> prescrire... » = "
        "négatif), jamais le niveau (1 vs 2, toujours explicite) — cohérent avec les tags « GRADE "
        "1– » explicitement signés ailleurs dans ce même document pour des recommandations "
        "négatives strictement analogues.", S_BODY_SM), bg=BG_PANEL, border=AMBER))
    story.append(Spacer(1, 3 * mm))

    story.append(section_bar("1 — Examens cardiologiques (ECG, échographie)", color=TEAL_DARK))
    story.append(Spacer(1, 2 * mm))
    story.append(reco_table([
        ("R1", "ECG de repos — quel que soit l'âge : ne pas prescrire un nouvel ECG si un tracé "
         "de moins de 12 mois est disponible sans modification clinique.", "1-"),
        ("R1", "Ne pas prescrire un ECG de repos pour une intervention mineure.", "1-"),
        ("R1", "ECG de repos — avant 65 ans : ne pas prescrire un ECG 12 dérivations avant une "
         "intervention à risque intermédiaire/élevé (sauf artérielle) en l'absence de signes "
         "d'appel, FDR ou pathologie cardiovasculaire.", "1-"),
        ("R1", "ECG de repos — après 65 ans : il faut probablement prescrire un ECG 12 "
         "dérivations avant toute intervention à risque élevé/intermédiaire, même sans signe "
         "clinique, FDR ni pathologie cardiovasculaire.", "2+"),
        ("R1", "Échocardiographie transthoracique : ne pas prescrire de façon systématique une "
         "échocardiographie de repos préinterventionnelle.", "1-"),
        ("R1", "Limiter les indications d'échocardiographie préinterventionnelle aux "
         "sous-groupes bénéficiaires : patients symptomatiques (dyspnée, insuffisance cardiaque "
         "inconnue/aggravée, souffle systolique non connu, suspicion d'HTAP).", "2+"),
    ]))
    story.append(Spacer(1, 3 * mm))

    story.append(section_bar("2 — Examens respiratoires (radio thorax, gaz du sang, EFR)", color=TEAL_DARK))
    story.append(Spacer(1, 2 * mm))
    story.append(reco_table([
        ("R2", "Ne pas prescrire de manière systématique une radiographie de thorax "
         "préinterventionnelle en chirurgie non cardiothoracique, quel que soit l'âge, sauf "
         "pathologie cardiopulmonaire évolutive/aiguë.", "1-"),
        ("R2", "Ne pas prescrire de manière systématique des gaz du sang artériels "
         "préinterventionnels en chirurgie non cardiothoracique, quel que soit l'âge, sauf "
         "pathologie pulmonaire évolutive/aiguë.", "1-"),
        ("R2", "Ne pas prescrire de manière systématique des EFR préinterventionnelles en "
         "chirurgie non cardiothoracique, quel que soit l'âge, sauf pathologie pulmonaire "
         "évolutive/aiguë.", "1-"),
    ]))
    return story


def _section_r3_r4_r5():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("3 — Examens d'hémostase (TP, TCA, plaquettes)", color=TEAL_DARK))
    story.append(Spacer(1, 2 * mm))
    story.append(reco_table([
        ("R3", "Évaluer le risque hémorragique d'après l'anamnèse personnelle/familiale de "
         "diathèse hémorragique et l'examen physique.", "1+"),
        ("R3", "Utiliser probablement un questionnaire standardisé de recherche de "
         "manifestations hémorragiques pour l'anamnèse.", "2+"),
        ("R3", "Ne pas prescrire de façon systématique un bilan d'hémostase si l'anamnèse/examen "
         "clinique ne fait pas suspecter un trouble — quel que soit le grade ASA, le type "
         "d'intervention et l'âge (hors enfants n'ayant pas acquis la marche).", "1-"),
        ("R3", "Ne pas prescrire de façon systématique un bilan d'hémostase si l'anamnèse/examen "
         "clinique ne fait pas suspecter un trouble — quel que soit le type d'anesthésie "
         "(générale, neuraxiale, blocs périphériques/combinées), y compris en obstétrique.", "1-"),
        ("R3", "Demander un avis spécialisé en cas d'anamnèse de diathèse hémorragique "
         "évocatrice d'un trouble de l'hémostase.", "1+"),
        ("R3", "Chez l'enfant n'ayant pas acquis la marche : prescrire probablement un TCA et "
         "une numération plaquettaire (dépistage de pathologies constitutionnelles, ex. "
         "hémophilie).", "2+"),
        ("R3", "Chez l'adulte non interrogeable : prescrire probablement un TP, un TCA et une "
         "numération plaquettaire (pathologies constitutionnelles ou acquises).", "2+"),
    ]))
    story.append(Spacer(1, 2 * mm))
    story.append(info_panel(P(
        "<b>Précisions non graduées (source) :</b> un bilan d'hémostase doit être réalisé en cas "
        "d'hépatopathie, de malabsorption/malnutrition, de maladie hématologique ou de toute "
        "pathologie pouvant entraîner des troubles de l'hémostase, ou de prise d'anticoagulants — "
        "même sans symptôme hémorragique ; il doit être demandé suffisamment à l'avance pour "
        "permettre tout examen complémentaire nécessaire. <b>Aucun examen de laboratoire ne "
        "permet d'évaluer le risque de saignement</b> chez les patients sous antiagrégants "
        "plaquettaires. En cas d'anamnèse évocatrice avec bilan standard normal, le patient doit "
        "être adressé à une consultation spécialisée : des TCA/TP/plaquettes normaux n'excluent "
        "pas une pathologie de l'hémostase exposant à un risque hémorragique péri-interventionnel."
    )))
    story.append(Spacer(1, 3 * mm))

    story.append(section_bar("4 — Hémogramme", color=TEAL_DARK))
    story.append(Spacer(1, 2 * mm))
    story.append(reco_table([
        ("R4", "Intervention à risque mineur, quel que soit l'âge : ne pas prescrire un "
         "hémogramme avant l'acte.", "1-"),
        ("R4", "Intervention à risque intermédiaire ou élevé, quel que soit l'âge : prescrire un "
         "hémogramme avant l'acte (caractère pronostique, stratégie transfusionnelle).", "1+"),
    ]))
    story.append(Spacer(1, 3 * mm))

    story.append(section_bar("5 — Examens immunohématologiques (groupe sanguin, RAI)", color=TEAL_DARK))
    story.append(Spacer(1, 2 * mm))
    story.append(reco_table([
        ("R5", "Risque de transfusion/saignement nul à faible : ne pas prescrire de groupage "
         "sanguin ni de RAI.", "1-"),
        ("R5", "Risque de transfusion intermédiaire/élevé ou de saignement important : prescrire "
         "un groupage sanguin et une RAI.", "1+"),
        ("R5", "Disposer des examens IH et de leurs résultats avant l'intervention en cas de "
         "risque de saignement important (check-list « sécurité au bloc opératoire »).", "1+"),
        ("R5", "Disposer des examens IH et de leurs résultats avant l'intervention en cas de "
         "risque de transfusion intermédiaire/élevé.", "1+"),
        ("R5", "S'assurer probablement que les examens IH soient disponibles avec leurs "
         "résultats lors de la visite préanesthésique.", "2+"),
        ("R5", "Prolonger la durée de validité de la RAI négative de 3 à 21 jours si l'absence "
         "de circonstances immunisantes (transfusion, grossesse, greffe) a été vérifiée dans les "
         "6 mois précédents.", "1+"),
    ]))
    return story


def _section_r6_r7():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("6 — Examens biochimiques", color=TEAL_DARK))
    story.append(Spacer(1, 2 * mm))
    story.append(reco_table([
        ("R6", "Ne pas prescrire d'examen biochimique sanguin préinterventionnel systématique, "
         "en dehors de signes d'appel, en chirurgie mineure.", "1-"),
        ("R6", "Évaluer probablement la fonction rénale (débit de filtration glomérulaire) "
         "préopératoire chez les patients à risque devant bénéficier d'une chirurgie "
         "intermédiaire ou majeure.", "2+"),
        ("R6", "Ne pas prescrire d'examen biochimique urinaire systématique, quel que soit "
         "l'âge, quel que soit le type de chirurgie.", "1-"),
    ]))
    story.append(Spacer(1, 3 * mm))

    story.append(section_bar("7 — Femme enceinte en prépartum", color=TEAL_DARK))
    story.append(Spacer(1, 2 * mm))
    story.append(reco_table([
        ("R7", "Ne pas prescrire un bilan systématique d'hémostase (TQ, TCA, fibrinogène, "
         "plaquettes) dans le cadre d'une grossesse normale sans élément anamnestique/clinique "
         "évocateur, y compris avant une ALR périmédullaire.", "1-"),
        ("R7", "Réévaluer la normalité de la grossesse de façon répétée, notamment à l'arrivée "
         "en salle de naissance par l'équipe obstétricale, et transmettre à l'anesthésiste.", "1+"),
        ("R7", "Ne pas prescrire systématiquement une RAI à l'entrée en salle de travail si "
         "contrôle de moins d'1 mois disponible et grossesse normale. En présence de situations "
         "à risque hémorragique dépistées avant la naissance (ATCD HPP, HELLP, hématome "
         "rétroplacentaire, MFIU, anomalie d'insertion placentaire, grossesse gémellaire, utérus "
         "cicatriciel, chorioamniotite, trouble d'hémostase connu), disposer d'une RAI de moins "
         "de 3 jours.", "1+"),
        ("R7", "Dans le cadre d'une césarienne programmée, disposer d'une RAI de moins de "
         "3 jours.", "1+"),
    ]))
    return story


def _section_r8_r9_sources():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("8 — Test de grossesse", color=TEAL_DARK))
    story.append(Spacer(1, 2 * mm))
    story.append(reco_table([
        ("R8", "Poser la question à toute femme en âge de procréer sur sa méthode de "
         "contraception et une possibilité de grossesse, avant tout acte nécessitant une "
         "anesthésie.", "1+"),
        ("R8", "Si possibilité de grossesse à l'interrogatoire : prescrire un dosage plasmatique "
         "des bHCG après consentement de la patiente.", "1+"),
        ("R8", "Si bHCG plasmatiques positifs : reporter l'intervention chaque fois que "
         "possible.", "1+"),
    ]))
    story.append(Spacer(1, 3 * mm))

    story.append(section_bar("9 — Dépistage infectieux (ECBU)", color=TEAL_DARK))
    story.append(Spacer(1, 2 * mm))
    story.append(reco_table([
        ("R9", "Chirurgie urologique (plaie opératoire en contact avec l'urine, y compris "
         "endoscopique) : réaliser systématiquement un ECBU préopératoire.", "1+"),
        ("R9", "Hors chirurgie urologique, patients avec facteur de risque d'infection urinaire "
         "et chirurgie à risque fort (prolapsus/incontinence gynécologique, orthopédie "
         "prothétique) : réaliser probablement un ECBU préopératoire systématique.", "2+"),
        ("R9", "Patients sans facteur de risque d'IU, chirurgie à risque fort : réaliser "
         "probablement une bandelette urinaire (BU), complétée par un ECBU si positive "
         "(nitrites/leucocyte-estérase).", "2+"),
        ("R9", "Chirurgie à risque faible de complication liée à l'IU, patients sans facteur de "
         "risque : ne pas pratiquer probablement d'analyse d'urine (BU ou ECBU).", "2-"),
    ]))
    story.append(Spacer(1, 1 * mm))
    cw = PAGE_W - 2 * MARGIN
    story.append(KeepTogether([
        P("<b>Tableau 1 — Indication de l'analyse d'urine dans le cadre du bilan préopératoire</b>",
          S_H2),
        Spacer(1, 2 * mm),
        simple_table(
            ["Chirurgie", "Risque élevé IU/CU (symptomatologie IU, diabète, âge physio-avancé, "
             "institution, cathétérisme prolongé)", "Risque bas IU/CU (absence de FDR)"],
            [
                ["Chirurgie des voies urinaires", "ECBU systématique", "ECBU systématique"],
                ["Orthopédie prothétique / gynécologie prolapsus-incontinence",
                 "ECBU systématique", "BU puis ECBU si positive"],
                ["Autres chirurgies (orthopédie sans matériel, gynécologie hors "
                 "prolapsus/incontinence)", "BU puis ECBU si positive", "Rien"],
            ],
            [cw * 0.34, cw * 0.33, cw * 0.33]),
    ]))
    story.append(Spacer(1, 4 * mm))

    story.append(section_bar("Synthèse & Annexe A — Stratification du risque", color=GREY))
    story.append(Spacer(1, 2 * mm))
    story.append(KeepTogether([
        P("<b>Tableau 2 — Prescription des examens complémentaires selon le risque patient/"
          "intervention</b>", S_H2),
        Spacer(1, 2 * mm),
        simple_table(
            ["", "Intervention à risque faible", "Intervention à risque intermédiaire ou élevé"],
            [
                ["Patient ASA I ou II", "Pas d'examens complémentaires systématiques",
                 "Prescription en fonction du risque opératoire"],
                ["Patient ASA III ou IV", "Pas d'examens complémentaires systématiques",
                 "Prescription en fonction de la pathologie du patient et du risque opératoire"],
            ],
            [cw * 0.24, cw * 0.38, cw * 0.38]),
    ]))
    story.append(Spacer(1, 3 * mm))
    story.append(KeepTogether([
        P("<b>Annexe A — Stratification du risque cardiaque pour la chirurgie non cardiaque "
          "(ACC/AHA)</b>", S_H2),
        Spacer(1, 2 * mm),
        simple_table(
            ["Stratification du risque (décès + infarctus du myocarde)", "Exemples d'intervention"],
            [
                ["Élevé (&gt; 5 %)", "Chirurgie aortique ou autre chirurgie vasculaire majeure, "
                 "chirurgie vasculaire périphérique"],
                ["Intermédiaire (1-5 %)", "Chirurgie intrapéritonéale ou intrathoracique, "
                 "endartériectomie carotidienne, chirurgie de la tête et du cou, chirurgie "
                 "orthopédique majeure, chirurgie de prostate"],
                ["Faible (&lt; 1 %)", "Procédures endoscopiques, chirurgie superficielle, "
                 "chirurgie de la cataracte, chirurgie mammaire, chirurgie ambulatoire"],
            ],
            [cw * 0.34, cw * 0.66]),
    ]))
    story.append(Spacer(1, 4 * mm))

    story.append(section_bar("Sources et traçabilité", color=GREY))
    story.append(Spacer(1, 2 * mm))
    story.append(P(
        "<b>Document source :</b> « Examens préinterventionnels systématiques » — Recommandations "
        "formalisées d'experts, SFAR, 2012 (Ann Fr Anesth Reanim 2012;31:752-763). Auteurs : "
        "S. Molliex, S. Pierre, C. Bléry, E. Marret, H. Beloeil. Actualisation des recommandations "
        "Anaes de 1998, à partir d'une analyse systématique de la littérature 2001-2011 par 30 "
        "experts. Validé par l'AFC, l'AFU, le CNGOF, l'EFS, la SCGP, la SFC, la SFCD, le GEHT, la "
        "SF2H, la SOFOP, la SFORL, la SFR-FRI, la SFSCMF et la SPLF.", S_SOURCE))
    story.append(Spacer(1, 2 * mm))
    story.append(P(
        "<b>Méthodologie :</b> GRADE — 38 recommandations tagués (14× 1+, 14× 1-, 9× 2+, 1× 2-), "
        "13 d'entre elles avec un signe +/- résolu à partir du sens univoque de la phrase (voir "
        "disclosure méthodologique en page 1).", S_SOURCE))
    story.append(Spacer(1, 2 * mm))
    story.append(P(
        "<b>Couverture :</b> cette fiche reprend l'intégralité des 9 recommandations (examens "
        "cardiologiques, respiratoires, hémostase, hémogramme, immunohématologiques, "
        "biochimiques, femme enceinte en prépartum, test de grossesse, dépistage infectieux), "
        "le tableau 1 (indications ECBU/BU), le tableau 2 (synthèse ASA × risque chirurgical) et "
        "l'annexe A (stratification du risque cardiaque ACC/AHA). Comité d'organisation, groupe "
        "de travail et références bibliographiques ne sont pas retranscrits (sans contenu "
        "clinique).", S_SOURCE))
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Avertissement — document de 2012 :</b> ce document est une fiche de synthèse "
        "indépendante, produite pour un usage d'aide-mémoire. Elle reprend l'intégralité des "
        "recommandations du texte source, mais ne remplace pas le texte intégral (argumentaire "
        "complet) et n'est ni éditée ni validée par la SFAR. La prescription des examens "
        "complémentaires préinterventionnels ne se substitue en aucun cas à l'interrogatoire et "
        "à l'examen clinique du patient.", S_BODY_SM), bg=BG_PANEL, border=GREY))
    return story


SECTIONS = [
    ("Examens cardiologiques & respiratoires", _section_intro_r1_r2),
    ("Hémostase, hémogramme & immunohématologie", _section_r3_r4_r5),
    ("Biochimie & femme enceinte", _section_r6_r7),
    ("Grossesse, dépistage infectieux & sources", _section_r8_r9_sources),
]

def _make_doc(path=None):
    return SimpleDocTemplate(path or OUT, pagesize=A4,
                              leftMargin=MARGIN, rightMargin=MARGIN,
                              topMargin=32 * mm, bottomMargin=16 * mm,
                              title="SFAR 2012 - Examens preinterventionnels systematiques",
                              author="Synthèse indépendante (source SFAR)")

def _silent_page(canvas, doc_):
    pass

def _build_upto(section_fns):
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
