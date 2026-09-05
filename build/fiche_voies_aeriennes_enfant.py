# -*- coding: utf-8 -*-
"""
Fiche de synthese - RFE communes SFAR-ADARPEF 2018
Gestion des voies aeriennes de l'enfant
Source verifiee : Anesth Reanim. 2019;5:408-426 (texte valide CA SFAR 21/06/2018, CA ADARPEF 24/05/2018)
Methodologie GRADE, tags "(GRADE X+/-) ACCORD FORT" et "AVIS D'EXPERTS" imprimes litteralement apres
chaque recommandation. 12 recommandations numerotees R1-R12 (6 GRADE1 + 6 GRADE2) + 5 avis d'experts
non numerotes R (numerotes 1-5 dans leur propre section) + 3 questions "Pas de recommandation" -
resume officiel parfaitement coherent en interne (12+5=17 items, 6+6=12 GRADE, verifie item par
item ; 3 questions sans recommandation, verifie) - aucune incoherence arithmetique a signaler.
Ne s'applique PAS au nouveau-ne/enfant premature (population exclue explicitement par la source).
R12 : le signe "-" du grade a ete perdu par l'extraction automatique du texte source (glyphe moins
non standard) - confirme "(GRADE 2-)" par rendu visuel de la page 12 source avant integration ;
piege discrete a documenter si une future extraction du meme document se refait a l'identique.
3 algorithmes (Figures 1-3, adaptes de Black AE et al. Pediatr Anesth 2015;25:346-62) : intubation
difficile imprevue, ventilation au masque difficile imprevue, CICO (intubation ET ventilation
impossibles chez l'enfant curarise) - transcrits integralement depuis le rendu visuel des pages
source (diagrammes complexes avec branches multiples, pleinement lisibles a l'image).
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from style import *
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.units import mm

OUT = "/private/tmp/claude-501/-Users-macbook-Downloads-claude/65498e3e-5ddf-47a6-b100-3ac535d1faa0/scratchpad/rfe_sfar/output/Fiche_SFAR_Voies_Aeriennes_Enfant_2018.pdf"

SOURCE_TXT = ("Source : Recommandations Formalisées d'Experts communes SFAR-ADARPEF « Gestion des "
              "voies aériennes de l'enfant » — Anesth Reanim. 2019;5:408-426, texte validé par le CA "
              "SFAR (21/06/2018) et le CA ADARPEF (24/05/2018). Méthodologie GRADE. "
              "Fiche de synthèse non officielle : se référer au texte intégral.")

def P(txt, style=S_CELL):
    return Paragraph(txt, style)

def chip(label, **kw):
    return grade_chip(label, **kw)

def reco_table(rows, col_widths):
    """rows: (ref, text, grade_label_for_chip)"""
    data = [[P("Réf.", S_HEAD_W), P("Recommandation", S_HEAD_W), P("Grade", S_HEAD_W_C)]]
    for ref, txt, grade in rows:
        data.append([P(ref, S_CELL_B), P(txt, S_CELL), chip(grade)])
    t = Table(data, colWidths=col_widths, repeatRows=1)
    style_cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), NAVY), ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTNAME", (0, 0), (-1, 0), FONT_BOLD), ("FONTSIZE", (0, 0), (-1, 0), 8),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("ALIGN", (2, 0), (2, -1), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 0.5, GREY_LIGHT),
        ("TOPPADDING", (0, 0), (-1, -1), 3.4), ("BOTTOMPADDING", (0, 0), (-1, -1), 3.4),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            style_cmds.append(("BACKGROUND", (0, i), (-1, i), BG_PANEL))
    t.setStyle(TableStyle(style_cmds))
    return t

def ae_panel(num, text):
    return info_panel(P(f"<b>Avis d'experts n°{num}</b> — {text}", S_BODY_SM), bg=BG_PANEL, border=TEAL)

def no_reco_panel(text):
    return info_panel(P("<b>Pas de recommandation</b> — " + text, S_BODY_SM), bg=GREY_LIGHT, border=GREY)

def simple_table(header, rows, col_widths):
    data = [[P(h, S_HEAD_W) for h in header]]
    for r in rows:
        data.append([P(c, S_CELL) for c in r])
    t = Table(data, colWidths=col_widths, repeatRows=1)
    st = [
        ("BACKGROUND",(0,0),(-1,0), TEAL_DARK), ("TEXTCOLOR",(0,0),(-1,0), WHITE),
        ("FONTNAME",(0,0),(-1,0), FONT_BOLD), ("FONTSIZE",(0,0),(-1,0), 8),
        ("GRID",(0,0),(-1,-1),0.5,GREY_LIGHT), ("VALIGN",(0,0),(-1,-1),"TOP"),
        ("TOPPADDING",(0,0),(-1,-1),3.4), ("BOTTOMPADDING",(0,0),(-1,-1),3.4), ("LEFTPADDING",(0,0),(-1,-1),5),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            st.append(("BACKGROUND",(0,i),(-1,i), BG_PANEL))
    t.setStyle(TableStyle(st))
    return t

def legend_flowable():
    items = [("1+", "Il faut faire"), ("1-", "Il ne faut pas faire"),
             ("2+", "Il faut probablement"), ("2-", "Il ne faut probablement pas"),
             ("AE", "Avis d'experts")]
    content_w = PAGE_W - 2*MARGIN
    n = len(items)
    chip_w = 15*mm
    text_w = (content_w - n*chip_w) / n
    row_cells, col_widths = [], []
    for g, txt in items:
        row_cells.append(chip(g, width=chip_w-1.5*mm))
        row_cells.append(P(txt, S_BADGE_HEAD))
        col_widths += [chip_w, text_w]
    row = Table([row_cells], colWidths=col_widths)
    row.setStyle(TableStyle([("VALIGN",(0,0),(-1,-1),"MIDDLE"), ("LEFTPADDING",(0,0),(-1,-1),1), ("RIGHTPADDING",(0,0),(-1,-1),1)]))
    return row

TOTAL_PAGES = {"n": 10}

def on_page(canvas, doc, page_title):
    header_band(canvas, doc, "SFAR / ADARPEF — RFE 2018 — FICHE DE SYNTHÈSE",
                "Voies aériennes de l'enfant",
                page_title, icon_fn=lambda c,x,y: icon_pill(c, x, y, 13*mm), color=NAVY)
    footer_band(canvas, doc, SOURCE_TXT, f"Page {doc.page} / {TOTAL_PAGES['n']}")

# ---------------------------------------------------------------------------
def _section_intro():
    story = []
    story.append(Spacer(1, 3*mm))
    story.append(info_panel(P(
        "<b>Champ :</b> gestion des voies aériennes supérieures (VAS) de tout enfant lors d'une "
        "anesthésie générale. Comité de 17 experts SFAR/ADARPEF, méthode GRADE®, format PICO, "
        "7 questions. <b>Ne s'applique pas à la population néonatale et à l'enfant prématuré</b>, "
        "qui ont leurs propres particularités.<br/><br/>"
        "<b>Résultats (résumé officiel) :</b> 17 recommandations ; 6 de niveau de preuve élevé "
        "(Grade 1), 6 de niveau de preuve faible (Grade 2), 5 avis d'experts et 3 algorithmes. "
        "Accord fort obtenu pour 100 % des recommandations après trois tours de cotation. Pour "
        "3 questions, aucune recommandation n'a pu être formulée.<br/><br/>"
        "<b>Contexte :</b> plus de 50 % des événements critiques périopératoires de l'enfant sont "
        "d'origine respiratoire (étude APRICOT).",
        S_BODY), bg=BG_PANEL, border=TEAL))
    story.append(Spacer(1, 3*mm))

    story.append(section_bar("Légende des grades (méthodologie GRADE)"))
    story.append(Spacer(1, 2*mm))
    story.append(legend_flowable())
    story.append(Spacer(1, 4*mm))

    story.append(section_bar("Les 7 champs traités par la RFE"))
    story.append(Spacer(1, 2*mm))
    cw = PAGE_W - 2*MARGIN
    story.append(simple_table(
        ["#", "Question"],
        [
            ["1", "Dispositifs supraglottiques (DSG) : place en chirurgie élective, amygdalectomie/"
             "adénoïdectomie, intubation/ventilation difficile, pose et retrait"],
            ["2", "Sondes à ballonnet dans l'intubation de l'enfant"],
            ["3", "Place des vidéolaryngoscopes en anesthésie pédiatrique"],
            ["4", "Faut-il utiliser un curare pour intuber un enfant ?"],
            ["5", "Induction en séquence rapide (ISR) chez l'enfant"],
            ["6", "Extubation de l'enfant"],
            ["7", "Contrôle des voies aériennes chez l'enfant enrhumé"],
        ],
        [cw*0.08, cw*0.92]))
    return story

def _section_champ1a():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Champ 1 (1/2) — Dispositifs supraglottiques : place générale"))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("R1", "Il est probablement recommandé d'utiliser un dispositif supraglottique plutôt "
         "qu'une sonde d'intubation en cas de chirurgie superficielle programmée de courte durée "
         "afin de diminuer l'incidence des laryngospasmes et des hypoxémies lors du retrait du "
         "dispositif.", "2+"),
    ], [14*mm, PAGE_W-2*MARGIN-14*mm-20*mm, 20*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(P("Deux méta-analyses (littérature 1990-2013) aux conclusions divergentes sur "
                    "laryngospasme/hypoxémie, mais toutes deux confirment une toux postopératoire "
                    "significativement moindre avec un DSG. Étude randomisée (181 nourrissons "
                    "2-12 mois, chirurgie mineure) : risque relatif d'effets indésirables "
                    "respiratoires multiplié par 2,94 avec sonde d'intubation vs masque laryngé "
                    "(laryngospasme/bronchospasme : RR ×5).", S_NOTE))
    story.append(Spacer(1, 3*mm))
    story.append(no_reco_panel("Il n'y a pas d'argument en faveur du retrait du dispositif "
                                "supraglottique chez l'enfant sous anesthésie profonde ou "
                                "totalement réveillé."))
    story.append(Spacer(1, 2*mm))
    story.append(P("Méta-analyse (11 études) : pas de différence sur laryngospasme/désaturation "
                    "entre les deux stratégies, mais risque supérieur d'obstruction des VAS si "
                    "retrait sous AG (résolue par des manœuvres simples, sans événement grave "
                    "rapporté) ; risque de toux supérieur si retrait à l'éveil. Une étude retrouve "
                    "un risque de désaturation et d'obstruction des VAS plus élevé en décubitus "
                    "dorsal qu'en décubitus latéral, quel que soit le niveau de conscience au "
                    "retrait — le décubitus latéral est donc préférable dans les deux cas.", S_NOTE))
    return story

def _section_champ1b():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Champ 1 (2/2) — Amygdalectomie, adénoïdectomie, DSG en situation difficile"))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("R2", "Lors d'une intervention pour amygdalectomie, il est recommandé de protéger les "
         "voies aériennes supérieures à l'aide d'une sonde d'intubation à ballonnet.", "1+"),
    ], [14*mm, PAGE_W-2*MARGIN-14*mm-20*mm, 20*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(ae_panel(1, "Lors d'une intervention pour adénoïdectomie, les experts suggèrent "
                           "de protéger les voies aériennes avec une sonde d'intubation à "
                           "ballonnet. La pratique de l'adénoïdectomie au masque facial est une "
                           "particularité française (67 % des anesthésistes en 2010, majoritairement "
                           "en secteur libéral) sans étude comparative disponible."))
    story.append(Spacer(1, 4*mm))
    story.append(reco_table([
        ("R3", "En cas d'intubation et de ventilation difficiles non prévues, il est recommandé "
         "d'utiliser un dispositif supraglottique pour tenter d'assurer l'oxygénation de l'enfant.", "1+"),
        ("R4", "Il est recommandé d'utiliser un manomètre pour monitorer la pression dans le "
         "coussinet d'un dispositif supraglottique gonflable et de limiter celle-ci à 40 cmH2O.", "1+"),
    ], [14*mm, PAGE_W-2*MARGIN-14*mm-20*mm, 20*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(P("Nombre d'essais d'insertion d'un DSG limité à 2-3 ; en cas d'échec, méthode "
                    "d'oxygénation alternative. Une intubation par fibroscopie à travers le DSG "
                    "est possible (durée &lt; 1 min, taux de succès élevé, opérateurs entraînés). "
                    "Pression du coussinet &lt; 40 cmH2O associée aux moindres fuites/douleurs "
                    "oropharyngées postopératoires ; mesure à répéter en cas d'utilisation de "
                    "protoxyde d'azote.", S_NOTE))
    return story

def _section_champ2_3():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Champ 2 — Sondes à ballonnet"))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("R5", "Pour l'intubation trachéale, il est recommandé d'utiliser des sondes à ballonnet "
         "plutôt que des sondes sans ballonnet, et de monitorer la pression du ballonnet (sans "
         "dépasser 20 cmH2O).", "1+"),
    ], [14*mm, PAGE_W-2*MARGIN-14*mm-20*mm, 20*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(P("Réduction du taux de remplacement de sonde pour fuite excessive, sans "
                    "augmentation des complications respiratoires/laryngées post-extubation. "
                    "Favorise la ventilation à bas débit de gaz frais (réduction de la pollution du "
                    "bloc). Le Groupe Européen d'études sur l'intubation endotrachéale pédiatrique "
                    "recommande de ne pas utiliser de sonde à ballonnet chez l'enfant "
                    "&lt; 3 kg.", S_NOTE))
    story.append(Spacer(1, 4*mm))

    story.append(section_bar("Champ 3 — Vidéolaryngoscopes"))
    story.append(Spacer(1, 2*mm))
    story.append(info_panel(P(
        "<b>Prérequis</b> — un vidéolaryngoscope ne doit pas être utilisé si : ouverture de bouche "
        "insuffisante pour introduire le dispositif • rachis cervical fixé en flexion • obstacle "
        "des VAS avec stridor. Vérifier la possibilité d'introduction avant d'induire une apnée. "
        "Une désaturation &lt; 95 % impose l'arrêt des manœuvres d'intubation au profit de "
        "l'oxygénation — en cas de risque avéré d'hypoxémie, le vidéolaryngoscope ne peut pas se "
        "substituer à un dispositif supraglottique.",
        S_BODY_SM), bg=AMBER_LIGHT, border=AMBER))
    story.append(Spacer(1, 3*mm))
    story.append(reco_table([
        ("R6", "Il est probablement recommandé d'utiliser un vidéolaryngoscope en première "
         "intention chez les patients avec intubation difficile prévue et ventilation au masque "
         "possible, ou après échec de la laryngoscopie directe, afin d'augmenter les chances de "
         "succès de l'intubation.", "2+"),
    ], [14*mm, PAGE_W-2*MARGIN-14*mm-20*mm, 20*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(P("Améliore la vision de la glotte, le score d'intubation difficile et le taux de "
                    "succès dès la première tentative chez l'enfant avec antécédent d'intubation "
                    "difficile ou syndrome polymalformatif. En l'absence de critère d'intubation "
                    "difficile, pas de différence significative avec la laryngoscopie directe "
                    "(lame de Macintosh). Guide préformé non traumatique recommandé pour les "
                    "dispositifs sans gouttière latérale.", S_NOTE))
    return story

def _section_champ4_5():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Champ 4 — Curares pour l'intubation"))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("R7", "Hors situations relevant d'une indication à une induction à séquence rapide et à "
         "l'utilisation d'un curare dépolarisant, il est probablement recommandé d'utiliser un "
         "curare non dépolarisant pour améliorer les conditions d'intubation au cours de "
         "l'anesthésie générale par induction intraveineuse chez l'enfant.", "2+"),
    ], [14*mm, PAGE_W-2*MARGIN-14*mm-20*mm, 20*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(P("Alerte ANSM du 15/12/2017 : un curare dépolarisant ne doit pas être utilisé "
                    "pour une induction intraveineuse ne relevant pas d'une induction en séquence "
                    "rapide. Lors d'une induction inhalatoire, la non-utilisation de curare reste "
                    "très majoritaire en France (92 %) mais son usage est envisageable, notamment "
                    "chez le nourrisson, avec un bénéfice démontré sur les conditions d'intubation "
                    "et les événements respiratoires — à mettre en balance avec un risque "
                    "allergique faible mais réel.", S_NOTE))
    story.append(Spacer(1, 4*mm))

    story.append(section_bar("Champ 5 — Induction en séquence rapide (ISR)"))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("R8", "Dans l'induction en séquence rapide classique, il est recommandé d'utiliser un "
         "curare d'action rapide.", "1+"),
        ("R9", "Dans l'induction en séquence rapide classique, il est probablement recommandé "
         "d'utiliser chez l'enfant la succinylcholine en première intention pour l'induction en "
         "séquence rapide. En cas de contre-indication à la succinylcholine, il est probablement "
         "recommandé d'utiliser du rocuronium.", "2+"),
    ], [14*mm, PAGE_W-2*MARGIN-14*mm-20*mm, 20*mm]))
    story.append(Spacer(1, 2*mm))
    cw = PAGE_W - 2*MARGIN
    story.append(simple_table(
        ["Âge", "Dose de succinylcholine (ISR)"],
        [
            ["&lt; 1 mois", "1,8 mg/kg"],
            ["1 mois - 1 an", "2 mg/kg"],
            ["1 an - 10 ans", "1,2 mg/kg"],
            ["&gt; 10 ans", "1 mg/kg"],
        ],
        [cw*0.4, cw*0.6]))
    story.append(Spacer(1, 2*mm))
    story.append(P("Rocuronium (alternative si CI) : &gt; 0,9 mg/kg (posologie usuelle 0,6-0,9 "
                    "mg/kg) ; sugammadex non autorisé en pédiatrie en 2018. Contre-indications à "
                    "la succinylcholine : risque d'hyperthermie maligne, pathologies musculaires à "
                    "risque de rhabdomyolyse, hyperkaliémie, allergie.", S_NOTE))
    story.append(Spacer(1, 3*mm))
    story.append(ae_panel(2, "Les experts suggèrent de ne pas pratiquer de pression cricoïdienne "
                           "lors de l'induction à séquence rapide chez l'enfant pour diminuer "
                           "l'incidence des complications respiratoires. La pression cricoïdienne "
                           "ne comprime en réalité que l'hypopharynx (déplacement paramédian de "
                           "l'œsophage) et ne protège donc pas d'une inhalation — mais elle peut "
                           "réduire l'insufflation gastrique lors de la ventilation au masque."))
    story.append(Spacer(1, 2*mm))
    story.append(ae_panel(3, "Lors d'une induction en séquence rapide, les experts suggèrent de "
                           "ventiler l'enfant au masque avec une FiO2 ≥ 0,8 et de faibles niveaux "
                           "de pression de ventilation (juste suffisants pour soulever le thorax et "
                           "éviter une insufflation gastrique, idéalement &lt; 15 cmH2O) dès que la "
                           "SpO2 est inférieure à 95 %, afin "
                           "de diminuer le risque d'hypoxémie durant l'intubation et immédiatement "
                           "après (« séquence d'induction rapide contrôlée »)."))
    return story

def _section_champ6():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Champ 6 — Extubation de l'enfant"))
    story.append(Spacer(1, 2*mm))
    story.append(no_reco_panel("Chez un enfant intubé sans difficulté et sans facteur de risque "
                                "d'inhalation, les données actuelles de la littérature ne "
                                "permettent pas de trancher entre une extubation sous anesthésie "
                                "générale profonde et une extubation chez un patient totalement "
                                "réveillé."))
    story.append(Spacer(1, 2*mm))
    story.append(P("Extubation « endormi » : ventilation spontanée efficace (Vt ≥ 5 mL/kg, FR "
                    "normale pour l'âge), au moins 1 MAC d'halogéné maintenu jusqu'à l'extubation "
                    "— expose surtout à un risque d'apnées obstructives postopératoires. "
                    "Extubation « éveillé » : critères conventionnels adaptés à l'âge (Vt 5-8 "
                    "mL/kg, FR 12-25/min, décurarisation complète, SpO2 ≥ 95 % sous FiO2 ≤ 50 %, "
                    "réponse verbale/motrice, réflexe de déglutition récupéré) — expose davantage "
                    "à la toux et aux douleurs laryngées.", S_NOTE))
    story.append(Spacer(1, 3*mm))
    story.append(ae_panel(4, "Les experts suggèrent d'extuber un enfant difficile à intuber après "
                           "réveil complet et une ventilation spontanée en O2 100 % pendant au "
                           "moins 3 minutes, sous monitorage complet, en présence d'un aide "
                           "compétent et d'un chariot de matériel d'intubation difficile. Les "
                           "experts suggèrent d'extuber sur un guide échangeur creux (GEC) un "
                           "enfant chez qui on suspecte une extubation à risque."))
    story.append(Spacer(1, 2*mm))
    story.append(P("Étude rétrospective (137 patients aux VAS difficiles, extubés &lt; 6h avant la "
                    "fin de l'acte) : 95 % de réussite d'extubation (simple ou après technique "
                    "intermédiaire — masque laryngé, GEC, VNI) ; 5 % d'échec avec réintubation "
                    "(dont 2 arrêts cardiaques, 1 trachéotomie en urgence). GEC 8/11/14 Fr bien "
                    "toléré chez le nourrisson/l'enfant, facilite la réintubation ; oxygénation sur "
                    "guide à limiter dans le temps (risque de barotraumatisme). Un test de fuite "
                    "négatif (fuite &lt; 12 % du volume expiré) augmente le risque d'œdème "
                    "laryngé/stridor/réintubation. Stridor post-extubation : aérosol d'adrénaline "
                    "(efficace en 30 min, effet transitoire ~2h, surveillance requise). Scénario "
                    "CICO redouté à l'extubation → présence justifiée d'un chirurgien ORL ou d'un "
                    "praticien entraîné à la trachéotomie.", S_NOTE))
    return story

def _section_champ7():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Champ 7 — Enfant enrhumé"))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("R10", "Chez l'enfant enrhumé, il est recommandé d'utiliser le masque facial si le degré "
         "d'urgence, le type et la durée de la chirurgie le permettent.", "1+"),
    ], [14*mm, PAGE_W-2*MARGIN-14*mm-20*mm, 20*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(no_reco_panel("Chez l'enfant enrhumé, dans les situations où le masque facial "
                                "n'est pas utilisable, il n'est pas possible de formuler de "
                                "recommandation quant à l'usage préférentiel du masque laryngé ou "
                                "de la sonde d'intubation."))
    story.append(Spacer(1, 3*mm))
    story.append(reco_table([
        ("R11", "Chez l'enfant enrhumé, avant l'âge de 6 ans, il est probablement recommandé de "
         "réaliser une nébulisation de salbutamol avant l'anesthésie générale.", "2+"),
        ("R12", "Chez l'enfant enrhumé, il n'est probablement pas recommandé d'administrer à "
         "l'induction de la lidocaïne (IV ou locale) pour diminuer l'incidence des complications "
         "respiratoires.", "2-"),
    ], [14*mm, PAGE_W-2*MARGIN-14*mm-20*mm, 20*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(P("Salbutamol : étude princeps (400 enfants enrhumés, majoritairement masque "
                    "laryngé) — réduction d'environ 50 % de la toux et des bronchospasmes "
                    "peranesthésiques. Dose : 2,5 mg si poids &lt; 20 kg, 5 mg si poids &gt; 20 kg. "
                    "Bénéfice non retrouvé dans une étude portant sur des enfants &gt; 6 ans "
                    "(populations différentes). Lidocaïne : données contradictoires selon la voie "
                    "(spray local controversé, voie IV sans étude négative mais aucune étude "
                    "randomisée contre placebo spécifique à l'enfant enrhumé) — utilisation à "
                    "1-1,5 mg/kg IV envisageable par extrapolation de l'effet chez l'enfant sain, "
                    "dans les 5 minutes avant l'extubation.", S_NOTE))
    story.append(Spacer(1, 3*mm))
    story.append(ae_panel(5, "Chez l'enfant enrhumé, les experts suggèrent de ne pas utiliser le "
                           "desflurane, du fait d'une augmentation des résistances des voies "
                           "aériennes démontrée par rapport au propofol et au sévoflurane chez "
                           "l'enfant à hyperréactivité bronchique. Le choix de l'agent d'induction "
                           "(propofol vs sévoflurane) ne fait pas l'objet d'une recommandation — "
                           "leurs propriétés sont complémentaires (le propofol réduit la réactivité "
                           "laryngée mais pas sous-glottique)."))
    return story

def _section_algo1():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Algorithme 1 — Intubation difficile imprévue (enfant 1-8 ans)", color=GREY))
    story.append(Spacer(1, 1.5*mm))
    story.append(P("Adapté de Black AE et al., Pediatr Anesth 2015;25:346-62 — transcrit "
                    "intégralement depuis le rendu visuel de la source (diagramme, page 411).", S_NOTE))
    story.append(Spacer(1, 2*mm))
    cw = PAGE_W - 2*MARGIN
    story.append(simple_table(
        ["Étape", "Actions", "Résultat / suite"],
        [
            ["Constat initial", "Laryngoscopie directe difficile (2 essais max) → donner "
             "oxygène 100 %, maintenir l'anesthésie → appeler à l'aide, chariot d'intubation "
             "difficile", "—"],
            ["1re étape (intubation, ventilation au masque facile)",
             "Laryngoscopie directe : 2 essais max par sénior. Vérifier flexion du cou/extension "
             "de la tête, technique de laryngoscopie, manipulations externes du larynx, cordes "
             "vocales ouvertes et immobiles. Si vision insuffisante : mandrin long béquillé et/ou "
             "glottiscope.", "Succès → réaliser la chirurgie. Échec (oxygénation OK) → 2e étape."],
            ["2e étape (intubation trachéale)", "Mise en place d'un DSG : 3 essais max. Oxygéner "
             "et ventiler ; si ventilation inadéquate, envisager une taille de DSG plus grande.",
             "Succès → évaluer si la chirurgie est possible en toute sécurité avec le DSG "
             "(possible → réaliser la chirurgie ; évaluer fibroscopie via DSG, 1 essai → succès : "
             "chirurgie / échec : réveiller et reporter ; impossible → réveiller et reporter). "
             "Échec, oxygénation impossible (SpO2 &lt; 90 %) → étape suivante."],
            ["Retour au masque facial", "Optimiser la position de la tête ; oxygéner et ventiler "
             "à 4 mains, canule oro-pharyngée ± naso-pharyngée ; décomprimer l'estomac (sonde) ; "
             "antagoniser la curarisation.", "Succès → réveiller et reporter l'intervention. "
             "Ventilation ET oxygénation impossibles → Algorithme 3 (CICO)."],
        ],
        [cw*0.20, cw*0.52, cw*0.28]))
    story.append(Spacer(1, 2*mm))
    story.append(P("Après une intubation difficile, envisager systématiquement : traumatisme "
                    "laryngé • extubation difficile.", S_NOTE))
    return story

def _section_algo2_3():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Algorithme 2 — Ventilation au masque facial difficile imprévue", color=GREY))
    story.append(Spacer(1, 1.5*mm))
    story.append(P("Adapté de Black AE et al., Pediatr Anesth 2015;25:346-62 — transcrit depuis le "
                    "rendu visuel de la source (page 412).", S_NOTE))
    story.append(Spacer(1, 2*mm))
    cw = PAGE_W - 2*MARGIN
    story.append(simple_table(
        ["Étape", "Actions", "Résultat / suite"],
        [
            ["Constat initial", "Ventilation difficile → administrer oxygène 100 % → appeler à "
             "l'aide", "—"],
            ["1re étape : vérifier", "Position de la tête (subluxation mandibule, rouleau sous "
             "les épaules si &lt; 2 ans, position neutre si &gt; 2 ans, ventiler à 4 mains, "
             "adapter la pression cricoïdienne) ; équipement (masque, circuit, connecteurs, ballon "
             "autoremplisseur si doute) ; profondeur d'anesthésie (approfondir, ajouter CPAP).",
             "→ 2e étape"],
            ["2e étape : canule oro-pharyngée", "Exclure les causes de ventilation difficile "
             "(anesthésie trop légère, laryngospasme, distension gastrique à décomprimer).",
             "Si échec : maintenir la CPAP, approfondir l'anesthésie (propofol) ; si curarisé, "
             "intuber ; si intubation difficile malgré curare → Algorithme 1."],
            ["3e étape : insérer un DSG", "Max 3 essais ; penser à une sonde naso-pharyngée ; "
             "relâcher la pression cricoïdienne.", "VAS dégagées → poursuivre l'anesthésie. VAS "
             "non dégagées + SpO2 &gt; 80 % → rechercher DSG mal positionné/problème matériel/"
             "pneumothorax/bronchospasme → réveiller l'enfant. VAS non dégagées + SpO2 &lt; 80 % "
             "→ essai d'intubation ± curare → succès : poursuivre la chirurgie / échec → "
             "Algorithme 3 (CICO)."],
        ],
        [cw*0.20, cw*0.48, cw*0.32]))
    story.append(Spacer(1, 5*mm))

    story.append(section_bar("Algorithme 3 — CICO : intubation ET ventilation impossibles (enfant curarisé)", color=RED))
    story.append(Spacer(1, 1.5*mm))
    story.append(P("Adapté de Black AE et al., Pediatr Anesth 2015;25:346-62 — transcrit depuis le "
                    "rendu visuel de la source (page 413).", S_NOTE))
    story.append(Spacer(1, 2*mm))
    story.append(simple_table(
        ["Étape", "Actions", "Résultat / suite"],
        [
            ["Constat initial", "Échec d'intubation, ventilation inadéquate → administrer "
             "oxygène 100 % → appeler à l'aide", "—"],
            ["1re étape : continuer d'oxygéner/ventiler", "FiO2 100 % ; optimiser la position de "
             "la tête et la subluxation de la mandibule ; insérer une canule oro-pharyngée ou un "
             "DSG ; ventiler à 4 mains ; décomprimer l'estomac (sonde naso-gastrique).",
             "→ 2e étape si SpO2 &gt; 80 %"],
            ["2e étape : essayer de réveiller l'enfant (si SpO2 &gt; 80 %)", "Si rocuronium ou "
             "vécuronium : envisager sugammadex 16 mg/kg. Se préparer à une technique de sauvetage "
             "si l'état de l'enfant se détériore.", "→ 3e étape si SpO2 &lt; 80 % et/ou chute de "
             "la fréquence cardiaque"],
            ["3e étape : technique de sauvetage", "Appeler un ORL expérimenté. Si disponible : "
             "envisager trachéotomie ou bronchoscopie rigide ± jet-ventilation. Si indisponible : "
             "accès cricothyroïdien percutané avec cathéter court + essai de jet-ventilation "
             "(1 sec, 12/min).", "Jet-ventilation : succès → continuer au niveau de pression le "
             "plus bas + réveiller l'enfant. Échec → cricothyrotomie chirurgicale."],
        ],
        [cw*0.24, cw*0.46, cw*0.30]))
    story.append(Spacer(1, 2*mm))
    story.append(info_panel(P(
        "<b>ATTENTION :</b> les abords par voie cricothyroïdienne sont grevés d'un taux important "
        "d'échec et de complications. <b>Chez l'enfant de moins de 8 ans, l'abord avec un cathéter "
        "n'est plus recommandé.</b>",
        S_BODY), bg=RED_LIGHT, border=RED))
    return story

def _section_synthese():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Synthèse et messages clés"))
    story.append(Spacer(1, 2*mm))
    story.append(P(
        "• DSG plutôt que sonde d'intubation en chirurgie superficielle courte (moins de "
        "laryngospasme/hypoxémie au retrait, moins de toux) — sonde à ballonnet obligatoire pour "
        "l'amygdalectomie (et suggérée pour l'adénoïdectomie).<br/>"
        "• Manomètre systématique pour tout ballonnet/coussinet gonflable : &lt; 40 cmH2O pour un "
        "DSG, &lt; 20 cmH2O pour une sonde d'intubation.<br/>"
        "• DSG en 1re ligne devant une intubation/ventilation difficile non prévue pour assurer "
        "l'oxygénation.<br/>"
        "• Vidéolaryngoscope en 1re intention si intubation difficile prévue avec ventilation au "
        "masque possible, ou après échec de la laryngoscopie directe.<br/>"
        "• ISR classique : curare d'action rapide obligatoire — succinylcholine en 1re intention "
        "(doses par âge), rocuronium (&gt; 0,9 mg/kg) si contre-indication. Pas de pression "
        "cricoïdienne systématique ; ventiler au masque à faible pression si SpO2 &lt; 95 %.<br/>"
        "• Extubation d'un enfant difficile à intuber : réveil complet + 3 min de ventilation "
        "spontanée en O2 100 %, ou extubation sur guide échangeur creux si risque suspecté.<br/>"
        "• Enfant enrhumé : masque facial préféré si possible ; nébulisation de salbutamol avant "
        "6 ans ; pas de lidocaïne à l'induction ; pas de desflurane.<br/>"
        "• Connaître par cœur les 3 algorithmes (intubation difficile, ventilation au masque "
        "difficile, CICO) — le cathéter cricothyroïdien n'est plus recommandé chez l'enfant "
        "&lt; 8 ans en situation de sauvetage.",
        S_BODY))
    story.append(Spacer(1, 5*mm))

    story.append(section_bar("Sources et traçabilité", color=GREY))
    story.append(Spacer(1, 2*mm))
    story.append(P(
        "<b>Document source :</b> « Gestion des voies aériennes de l'enfant » — Recommandations "
        "Formalisées d'Experts communes SFAR-ADARPEF, Anesth Reanim. 2019;5:408-426. Comité de 17 "
        "experts, coordination C. Dadure (SFAR), N. Sabourdin et F. Veyckemans (ADARPEF). Texte "
        "validé par le CA SFAR le 21/06/2018 et le CA ADARPEF le 24/05/2018.", S_SOURCE))
    story.append(Spacer(1, 1.5*mm))
    story.append(P("<b>Méthodologie :</b> GRADE®, tags « (GRADE X+/-) ACCORD FORT » et « AVIS "
                    "D'EXPERTS » imprimés littéralement après chaque recommandation — cités ici tels "
                    "quels.", S_SOURCE))
    story.append(Spacer(1, 1.5*mm))
    story.append(P("<b>Couverture :</b> 12 recommandations (R1 à R12) et 5 avis d'experts reproduits "
                    "intégralement, ainsi que les 3 questions « pas de recommandation » et les 3 "
                    "algorithmes (Figures 1-3, adaptés de Black AE et al., pures images en source, "
                    "vérifiées visuellement et retranscrites intégralement sous forme de tableaux).", S_SOURCE))
    story.append(Spacer(1, 3*mm))
    story.append(info_panel(P(
        "<b>Avertissement :</b> ce document est une fiche de synthèse indépendante, produite pour un "
        "usage d'aide-mémoire. Il reprend l'intégralité des recommandations de la RFE mais ne "
        "remplace pas le texte intégral et n'est ni édité ni validé par la SFAR/ADARPEF. Ne "
        "s'applique pas à la population néonatale et à l'enfant prématuré. En cas de doute, se "
        "référer au texte intégral, aux recommandations ultérieures et/ou à un avis spécialisé.",
        S_BODY_SM), bg=GREY_LIGHT, border=GREY))
    return story

SECTIONS = [
    ("Introduction, méthodologie & les 7 champs", _section_intro),
    ("Champ 1 (1/2) — DSG : place générale", _section_champ1a),
    ("Champ 1 (2/2) — Amygdalectomie & adénoïdectomie", _section_champ1b),
    ("Champs 2-3 — Sondes à ballonnet & vidéolaryngoscopes", _section_champ2_3),
    ("Champs 4-5 — Curares & induction en séquence rapide", _section_champ4_5),
    ("Champ 6 — Extubation de l'enfant", _section_champ6),
    ("Champ 7 — Enfant enrhumé", _section_champ7),
    ("Algorithme 1 — Intubation difficile imprévue", _section_algo1),
    ("Algorithmes 2-3 — Ventilation difficile & CICO", _section_algo2_3),
    ("Synthèse, sources & traçabilité", _section_synthese),
]

def _make_doc():
    return SimpleDocTemplate(OUT, pagesize=A4,
                              leftMargin=MARGIN, rightMargin=MARGIN,
                              topMargin=32*mm, bottomMargin=16*mm,
                              title="Fiche SFAR-ADARPEF 2018 - Gestion des voies aeriennes de l'enfant",
                              author="Synthèse indépendante (source SFAR/ADARPEF)")

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
