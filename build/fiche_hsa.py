# -*- coding: utf-8 -*-
"""
Fiche de synthese - Conference d'experts SFAR 2004 (en partenariat avec l'ANARLF,
la Societe francaise de neurochirurgie et la Societe francaise de neuroradiologie)
"Hemorragie sous-arachnoidienne grave" - texte court, 12 pages.
Source : sources/hsa.pdf, sources/hsa.txt.
URL : https://sfar.org/hemorragie-sous-arachnoidienne-hsa-grave/

METHODOLOGIE - PAS DU GRADE (1+/1-/2+/2-/AE) : la source utilise une echelle de grades
A/B/D/E (comptage exhaustif par grep sur le texte extrait : 2x Grade A, 1x Grade B,
10x Grade D, 48x Grade E - AUCUNE occurrence de Grade C dans le corps du texte). Ce
"texte court" ne definit nulle part la signification de ces lettres (l'echelle complete
est presumee figurer dans le "texte long" / l'argumentaire scientifique complet de cette
conference, non disponible ici) - disclosure explicite dans le panneau d'introduction
plutot qu'une definition inventee de A/B/D/E.

GRADE_COLORS etendu localement (meme precedent que fiche_corticotherapie.py /
fiche_transfusion_plasma.py) avec les lettres A/B/D/E de cette source, distinctes des
cles GRADE 1+/2+/etc. qui appartiennent a un autre referentiel methodologique.

DUPLICATION SOURCE-INTERNE (disclosure, non resolue silencieusement) : le Doppler
transcranien quotidien est recommande (Grade E) a deux endroits distincts du texte
source - une fois dans la section "Diagnostic : imagerie du vasospasme", une fois dans
"Strategie de suivi du malade" (section 4, Doppler) - avec un enonce quasi identique.
Reproduit ici comme DEUX lignes de recommandation distinctes (V5 et S3), a leur place
naturelle dans chacune des deux sections du texte, plutot que fusionne en une seule ligne
qui gommerait la repetition du texte source.
De meme, "poser la DVE avant l'embolisation" est justifie deux fois (une fois section
HTIC/hydrocephalie, une fois section traitement endovasculaire) - reproduit comme deux
lignes distinctes (C.5 et T.13) pour la meme raison.

COMPTAGE DES RECOMMANDATIONS GRADEES : 61 phrases portant un grade explicite (Grade
A/B/D/E) recensees dans le corps du texte, organisees ci-dessous par theme clinique
(le document source est en prose narrative continue, sans numerotation R1/R2 propre -
comme fiche_corticotherapie.py, la reference "X.n" de chaque ligne est une numerotation
introduite par cette fiche pour la tracabilite, pas une numerotation de la source).
Verifie par grep -c "Grade [A-Z]" sur sources/hsa.txt = 61 occurrences totales (2+1+10+48).

TABLEAUX REPRODUITS INTEGRALEMENT (pas de texte source purement graphique/image dans ce
PDF - texte extractible pour les 4 tableaux) : Tableau 1 (classification WFNS), Tableau 2
(classification de Hunt et Hess), Tableau 3 (echelle scanographique de Fisher), et le
tableau de l'index bicaude normal par tranche d'age (associe a la Figure de la page 5,
qui elle-meme n'est qu'un schema explicatif du rapport A/B sans donnees chiffrees
supplementaires par rapport au tableau adjacent - non reproduite en image, sa legende
textuelle est integralement retranscrite a la place).
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from style import *
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.units import mm

OUT = os.path.join(os.path.dirname(__file__), "..", "output",
                    "Fiche_SFAR_Hemorragie_Sous_Arachnoidienne_2004.pdf")
OUT = os.path.abspath(OUT)

SOURCE_TXT = ("Source : Conférence d'experts SFAR, en partenariat avec l'ANARLF, la Société "
              "française de neurochirurgie et la Société française de neuroradiologie — "
              "« Hémorragie sous-arachnoïdienne grave », texte court, 2004. Fiche de synthèse "
              "non officielle : se référer au texte intégral / argumentaire scientifique.")

# Extension locale de GRADE_COLORS - lettres propres a cette source (voir docstring).
GRADE_COLORS["A"] = (GREEN, WHITE)
GRADE_COLORS["B"] = (TEAL, WHITE)
GRADE_COLORS["D"] = (AMBER, WHITE)
GRADE_COLORS["E"] = (GREY, WHITE)


def P(txt, style=S_CELL):
    return Paragraph(txt, style)


def chip(label):
    return grade_chip(label, width=13 * mm, fontsize=8.6)


def reco_table(rows, col_widths):
    """rows: (ref, text, grade_label)"""
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


def simple_table(header, rows, col_widths):
    data = [[P(h, S_HEAD_W_C) for h in header]]
    for r in rows:
        data.append([P(c, S_CELL_C) for c in r])
    t = Table(data, colWidths=col_widths, repeatRows=1)
    st = [
        ("BACKGROUND", (0, 0), (-1, 0), TEAL_DARK), ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTNAME", (0, 0), (-1, 0), FONT_BOLD), ("FONTSIZE", (0, 0), (-1, 0), 8),
        ("GRID", (0, 0), (-1, -1), 0.5, GREY_LIGHT), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 3.2), ("BOTTOMPADDING", (0, 0), (-1, -1), 3.2),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            st.append(("BACKGROUND", (0, i), (-1, i), BG_PANEL))
    t.setStyle(TableStyle(st))
    return t


def legend_flowable():
    items = [("A", "Preuve scientifique forte (littéralement « Grade A » de la source)"),
             ("B", "Présomption scientifique (« Grade B »)"),
             ("D", "« Grade D » — signification non définie dans le texte court"),
             ("E", "« Grade E » — signification non définie dans le texte court")]
    content_w = PAGE_W - 2 * MARGIN
    n = len(items)
    chip_w = 13 * mm
    text_w = (content_w - n * chip_w) / n
    row_cells, col_widths = [], []
    for g, txt in items:
        row_cells.append(chip(g))
        row_cells.append(P(txt, S_BADGE_HEAD))
        col_widths += [chip_w, text_w]
    row = Table([row_cells], colWidths=col_widths)
    row.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                              ("LEFTPADDING", (0, 0), (-1, -1), 1), ("RIGHTPADDING", (0, 0), (-1, -1), 1)]))
    return row


TOTAL_PAGES = {"n": 12}


def on_page(canvas, doc, page_title):
    header_band(canvas, doc, "SFAR / ANARLF / NEUROCHIRURGIE / NEURORADIOLOGIE — CONFÉRENCE D'EXPERTS 2004",
                "Hémorragie sous-arachnoïdienne grave",
                page_title, icon_fn=lambda c, x, y: icon_shield(c, x, y, 13 * mm), color=NAVY)
    footer_band(canvas, doc, SOURCE_TXT, f"Page {doc.page} / {TOTAL_PAGES['n']}")


# ---------------------------------------------------------------------------
def _section_intro():
    story = [Spacer(1, 3 * mm)]
    story.append(info_panel(P(
        "<b>Champ :</b> prise en charge de l'hémorragie sous-arachnoïdienne (HSA) grave par "
        "rupture d'anévrysme (WFNS III à V, <i>Grade D</i>) — pathologie touchant une "
        "population le plus souvent jeune et en bonne santé, au pronostic incertain, dont le "
        "traitement urgent met en jeu une filière complexe et multidisciplinaire. Conférence "
        "d'experts organisée par la SFAR en partenariat avec l'Association de "
        "neuroanesthésie-réanimation de langue française (ANARLF), la Société française de "
        "neurochirurgie et la Société française de neuroradiologie, en réponse à "
        "l'obsolescence des recommandations américaines (1994) et canadiennes (1997) sur le "
        "sujet. Panel présidé par le Pr L. Beydon (Angers).",
        S_BODY), bg=BG_PANEL, border=TEAL))
    story.append(Spacer(1, 2.5 * mm))
    story.append(info_panel(P(
        "<b>Méthodologie — disclosure :</b> le « faible niveau de preuve » de la majorité des "
        "études disponibles a justifié le choix méthodologique d'une <b>conférence "
        "d'experts</b> plutôt qu'une recommandation GRADE. Chaque proposition du jury porte un "
        "grade parmi <b>A, B, D, E</b> (comptage exhaustif du corps du texte : 2× Grade A, "
        "1× Grade B, 10× Grade D, 48× Grade E — <b>aucune occurrence de Grade C</b>). Le "
        "« texte court » exploité ici <b>ne définit nulle part</b> la signification précise de "
        "ces lettres ; cette définition figure vraisemblablement dans l'argumentaire "
        "scientifique complet (texte long), non disponible pour cette fiche. Les deux faits "
        "sont disclosés tels quels plutôt que résolus par une définition devinée.",
        S_BODY_SM), bg=AMBER_LIGHT, border=AMBER))
    story.append(Spacer(1, 2.5 * mm))
    story.append(section_bar("Légende des grades (tels qu'imprimés par le jury)"))
    story.append(Spacer(1, 2 * mm))
    story.append(legend_flowable())
    return story


def _section_diagnostic():
    story = [Spacer(1, 2 * mm)]
    story.append(section_bar("Diagnostic en hôpital général et prise en charge initiale"))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>Épidémiologie :</b> âge moyen ~50 ans, prédominance féminine (~60 %). Incidence en "
        "France de 5 à 7/100 000 sujets-année. Facteurs de risque identifiés : hypertension "
        "artérielle, tabagisme. Formes familiales/génétiques rares, justifiant des "
        "explorations.<br/>"
        "<b>Clinique :</b> céphalée brutale, intense, inhabituelle, souvent suivie de "
        "vomissements — pierre angulaire du diagnostic. Perte de conscience fréquente (sa "
        "prolongation est de mauvais pronostic) ; convulsions accompagnant la céphalée "
        "hautement évocatrices. Le syndrome méningé peut apparaître plusieurs heures après "
        "l'HSA et peut donc manquer à l'admission.",
        S_BODY_SM))
    story.append(Spacer(1, 2 * mm))
    story.append(KeepTogether([
        P("<b>Tableau 1</b> — Classification de la World Federation of Neurological Surgeons (WFNS)", S_H2),
        Spacer(1, 1 * mm),
        simple_table(["Grade", "Score de Glasgow", "Déficit moteur"], [
            ["I", "15", "absent"], ["II", "13-14", "absent"], ["III", "13-14", "présent"],
            ["IV", "7-12", "présent ou absent"], ["V", "3-6", "présent ou absent"],
        ], [24 * mm, 44 * mm, PAGE_W - 2 * MARGIN - 24 * mm - 44 * mm]),
    ]))
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        P("<b>Tableau 2</b> — Classification de Hunt et Hess", S_H2),
        Spacer(1, 1 * mm),
        simple_table(["Grade", "Description clinique"], [
            ["0", "Anévrysme non rompu"],
            ["1", "Asymptomatique ou céphalée minime"],
            ["2", "Céphalée modérée à sévère, raideur de nuque"],
            ["3", "Somnolence, confusion, déficit focal minime"],
            ["4", "Coma léger, déficit focal, troubles végétatifs"],
            ["5", "Coma profond, moribond"],
        ], [24 * mm, PAGE_W - 2 * MARGIN - 24 * mm]),
    ]))
    story.append(Spacer(1, 2.5 * mm))
    story.append(reco_table([
        ("D.1", "Le score de Glasgow doit être utilisé en complément de ces échelles pour "
                "quantifier la gravité de l'HSA tout au long de l'évolution clinique.", "E"),
        ("D.2", "On retient la définition d'HSA <b>grave</b> pour des HSA cotées III à V dans "
                "l'échelle de la WFNS, qui doit être privilégiée par rapport à celle de Hunt "
                "et Hess.", "D"),
    ], [11 * mm, PAGE_W - 2 * MARGIN - 11 * mm - 16 * mm, 16 * mm]))
    return story


def _section_imagerie():
    story = [Spacer(1, 2 * mm)]
    story.append(section_bar("Imagerie, ponction lombaire, transfert"))
    story.append(Spacer(1, 2 * mm))
    story.append(KeepTogether([
        P("<b>Tableau 3</b> — Échelle scanographique de Fisher", S_H2),
        Spacer(1, 1 * mm),
        simple_table(["Grade", "Aspect scanner"], [
            ["1", "Absence de sang"],
            ["2", "Dépôts de moins de 1 mm d'épaisseur"],
            ["3", "Dépôts de plus de 1 mm d'épaisseur"],
            ["4", "Hématome parenchymateux ou hémorragie ventriculaire"],
        ], [24 * mm, PAGE_W - 2 * MARGIN - 24 * mm]),
    ]))
    story.append(Spacer(1, 2.5 * mm))
    story.append(reco_table([
        ("D.3", "Tout patient suspect d'HSA doit être exploré par un scanner cérébral, en "
                "urgence — permettant d'évaluer l'importance de l'HSA et ses conséquences "
                "(hydrocéphalie, hématome, infarctus).", "D"),
        ("D.4", "En cas de doute d'interprétation, les images feront l'objet d'une "
                "télétransmission vers un centre de référence.", "E"),
        ("D.5", "L'intérêt de pratiquer un angio-scanner pour rechercher la cause de l'HSA en "
                "dehors d'un centre neurochirurgical est discutable — cet examen n'a qu'un "
                "intérêt préthérapeutique et n'est donc pas utile pour la décision de "
                "transfert.", "E"),
        ("D.6", "Toute dégradation neurologique impose la réalisation d'un nouveau scanner.", "D"),
        ("D.7", "La ponction lombaire n'a aucune indication lorsque l'HSA est visualisée sur le "
                "scanner cérébral. On y recourt pour l'éliminer lorsque la symptomatologie est "
                "évocatrice et le scanner normal — exceptionnel dans les formes graves.", "D"),
        ("D.8", "Le diagnostic d'HSA impose le transfert dans un centre de référence incluant "
                "des équipes de neurochirurgie, de neuroradiologie et de neuroanesthésie-"
                "réanimation, comportant une unité compétente en neuro-réanimation.", "E"),
    ], [11 * mm, PAGE_W - 2 * MARGIN - 11 * mm - 16 * mm, 16 * mm]))
    return story


def _section_complications():
    story = [Spacer(1, 2 * mm)]
    story.append(section_bar("Complications précoces — HTIC, hydrocéphalie, resaignement, épilepsie"))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "L'HSA anévrysmale s'accompagne d'une HTIC quasi constante pour les grades cliniques "
        "élevés, résultant d'un hématome intracérébral compressif (20 % des cas), d'un œdème "
        "cérébral et/ou d'une hydrocéphalie aiguë par trouble de résorption du LCS. Facteurs "
        "prédictifs de l'hydrocéphalie : âge, hémorragie intraventriculaire, importance de "
        "l'HSA, localisation postérieure de l'anévrysme. Une réaction de Cushing (HTA + "
        "bradycardie + ataxie respiratoire) contribue au maintien d'un niveau minimal de PPC.",
        S_BODY_SM))
    story.append(Spacer(1, 2 * mm))
    story.append(KeepTogether([
        P("<b>Index bicaudé</b> — signes scanographiques d'hydrocéphalie discrets dans les "
          "premières heures : dilatation des cornes temporales ou augmentation de l'index "
          "bicaudé (rapport A/B : A = largeur des cornes frontales au niveau des noyaux "
          "caudés ; B = diamètre cérébral au même niveau). Valeur normale décroissant avec "
          "l'âge :", S_BODY_SM),
        Spacer(1, 1 * mm),
        simple_table(["Âge (ans)", "Index bicaudé normal"], [
            ["≤ 30", "&lt; 0,16"], ["50", "&lt; 0,18"], ["60", "&lt; 0,19"],
            ["80", "&lt; 0,21"], ["100", "&lt; 0,25"],
        ], [40 * mm, PAGE_W - 2 * MARGIN - 40 * mm]),
    ]))
    story.append(Spacer(1, 2 * mm))
    story.append(reco_table([
        ("C.1", "Un hématome intracérébral compressif doit être évacué chirurgicalement, "
                "geste associé au traitement chirurgical de l'anévrysme.", "D"),
        ("C.2", "En cas d'engagement cérébral avec localisation de l'hématome suffisamment "
                "informative au scanner, le traitement chirurgical de l'anévrysme peut être "
                "réalisé sans angiographie diagnostique (pronostic dépendant de la précocité du "
                "traitement).", "E"),
        ("C.3", "Un œdème cérébral impose un monitorage de la PIC, au mieux par cathéter "
                "intraventriculaire.", "E"),
        ("C.4", "Une hydrocéphalie impose une dérivation ventriculaire externe (DVE) en "
                "urgence.", "E"),
        ("C.5", "Si un geste endovasculaire est envisagé, la DVE devrait être posée avant "
                "l'embolisation (l'héparinothérapie péri-embolisation gênerait sa pose "
                "ultérieure) ; elle est maintenue à 15 cm au-dessus de l'orifice du conduit "
                "auditif externe.", "E"),
        ("C.6", "En cas de doute sur une HTIC, le Doppler transcrânien (DTC) peut permettre "
                "d'en objectiver des signes.", "E"),
        ("C.7", "Le traitement de l'HTA relève d'un nécessaire compromis entre le risque de "
                "resaignement et celui d'hypoperfusion cérébrale.", "E"),
        ("C.8", "L'objectif premier du traitement de l'anévrysme est d'éviter la récidive "
                "hémorragique (mortalité &gt; 70 % en cas de resaignement) par une exclusion "
                "précoce.", "D"),
        ("C.9", "Une prophylaxie anti-épileptique peut être envisagée chez les patients à haut "
                "risque de convulsions (sang dans les citernes, infarctus cérébral, lésion "
                "focale, hématome sous-dural) — aucune donnée ne permet de statuer sur la durée "
                "de cette prophylaxie.", "E"),
    ], [11 * mm, PAGE_W - 2 * MARGIN - 11 * mm - 16 * mm, 16 * mm]))
    return story


def _section_complications2():
    story = [Spacer(1, 2 * mm)]
    story.append(section_bar("Complications précoces — retentissement cardio-pulmonaire, natrémie"))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "L'hyperactivation sympathique/décharge noradrénergique de l'HSA peut entraîner "
        "troubles du rythme, altération de la fonction myocardique et œdème pulmonaire "
        "« neurogénique » (pouvant aboutir à un SDRA). Diagnostic par la clinique, les "
        "marqueurs biologiques (troponine I sensible mais peu spécifique ; BNP) et "
        "l'échocardiographie/cathétérisme droit. Une hyponatrémie (natrémie &lt; 135 mmol/l), "
        "généralement différée (J4-J10), peut traduire un « Cerebral Salt Wasting Syndrome » "
        "(CSWS) — hypovolémie + natriurèse augmentée ; le syndrome de sécrétion inappropriée "
        "d'ADH est souvent évoqué à tort. Une hypernatrémie (natrémie &gt; 145 mmol/l, densité "
        "urinaire &lt; 1005) doit faire rechercher un diabète insipide.",
        S_BODY_SM))
    story.append(Spacer(1, 2 * mm))
    story.append(reco_table([
        ("C.10", "Des taux élevés de troponine I doivent inciter à réaliser un bilan "
                 "échocardiographique.", "E"),
        ("C.11", "Une défaillance cardiovasculaire et/ou respiratoire sévère peut nécessiter de "
                 "différer le traitement étiologique de l'anévrysme, réalisé dès la situation "
                 "contrôlée.", "E"),
        ("C.12", "En cas de CSWS (hyponatrémie + hypovolémie + natriurèse augmentée), remplacer "
                 "les pertes en eau et en sel et proscrire toute restriction hydrique "
                 "(minéralocorticoïdes possibles en complément).", "E"),
        ("C.13", "En cas d'hyponatrémie symptomatique, une correction initiale rapide, "
                 "objectif natrémie 125 mmol/l, est recommandée.", "E"),
        ("C.14", "En cas d'hypernatrémie (diabète insipide à rechercher), la correction ne doit "
                 "pas être trop rapide (&lt; 12 mmol/l/24 h) — elle peut majorer une éventuelle "
                 "HTIC.", "E"),
    ], [13 * mm, PAGE_W - 2 * MARGIN - 13 * mm - 16 * mm, 16 * mm]))
    return story


def _section_traitement():
    story = [Spacer(1, 2 * mm)]
    story.append(section_bar("Traitement de l'anévrysme"))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "Le traitement précoce du sac anévrysmal a deux objectifs : mettre à l'abri du "
        "resaignement et optimiser la PPC pour prévenir les conséquences ischémiques de "
        "l'HTIC. Le choix chirurgie / endovasculaire tient compte de la localisation et de la "
        "morphologie de l'anévrysme, de l'état clinique et des antécédents du patient, ainsi "
        "que de la disponibilité et de l'expérience des équipes.",
        S_BODY_SM))
    story.append(Spacer(1, 2 * mm))
    story.append(reco_table([
        ("T.1", "Le traitement précoce (dans les 72 premières heures) du sac anévrysmal "
                "s'impose.", "E"),
        ("T.2", "La décision du choix thérapeutique doit résulter d'une discussion entre "
                "chirurgiens, radiologues et neuro-anesthésistes.", "E"),
        ("T.3", "Un traitement intensif des patients en grade clinique élevé (monitorage de la "
                "PIC, drainage du LCS, monitorage hémodynamique, « triple H » thérapie précoce) "
                "améliore significativement leur pronostic.", "D"),
        ("T.4", "Quand le traitement endovasculaire et chirurgical sont tous deux possibles, en "
                "dehors des hématomes compressifs, le traitement endovasculaire est "
                "probablement l'option thérapeutique appropriée (extrapolation de l'étude ISAT, "
                "menée sur des grades WFNS faibles, aux grades élevés).", "B"),
        ("T.5", "Le choix thérapeutique ne doit pas retarder la mise en place d'une DVE ; en "
                "cas de défaillance cardiaque, le traitement du sac anévrysmal doit être "
                "différé jusqu'à stabilisation de la fonction cardiaque.", "E"),
        ("T.6", "Traitement chirurgical : le volet doit être large en raison de l'HTIC souvent "
                "associée aux formes graves d'HSA.", "E"),
        ("T.7", "Traitement chirurgical : l'hypotension artérielle est à proscrire, sauf "
                "conditions de sauvetage sur rupture incontrôlable.", "E"),
        ("T.8", "Traitement endovasculaire : une héparinothérapie à dose efficace est "
                "nécessaire durant le geste.", "E"),
        ("T.9", "Traitement endovasculaire : en cas de rupture durant la procédure, il convient "
                "de poursuivre le remplissage de la poche anévrysmale le plus rapidement "
                "possible.", "E"),
        ("T.10", "Traitement endovasculaire : avant de reprendre un éventuel traitement "
                 "anticoagulant, un scanner de contrôle est indiqué.", "E"),
        ("T.11", "Traitement endovasculaire : une thrombose en cours d'embolisation doit faire "
                 "envisager un traitement par fibrinolytique in situ ou par agent "
                 "antiplaquettaire.", "E"),
        ("T.12", "Traitement endovasculaire : en cas de déficit neurologique apparaissant dans "
                 "les suites de la procédure, une exploration tomodensitométrique doit être "
                 "impérativement réalisée pour écarter un resaignement.", "E"),
        ("T.13", "Traitement endovasculaire : il est particulièrement indiqué de poser la DVE "
                 "avant l'embolisation (arrêt/antagonisation de l'héparine circulante requis "
                 "sinon, ce qui n'est pas sans danger) — même justification que C.5.", "E"),
    ], [11 * mm, PAGE_W - 2 * MARGIN - 11 * mm - 16 * mm, 16 * mm]))
    return story


def _section_anesthesie_douleur():
    story = [Spacer(1, 2 * mm)]
    story.append(section_bar("Anesthésie et traitement de la douleur"))
    story.append(Spacer(1, 2 * mm))
    story.append(reco_table([
        ("A.1", "En cas d'HSA grave avec HTIC, l'anesthésie intraveineuse est clairement à "
                "préférer ; l'injection de fortes doses de morphiniques en bolus est à éviter "
                "(risque d'augmentation de la PIC). Objectif peranesthésique : éviter les "
                "poussées hypertensives (risque de rupture) et l'hypotension (hypoperfusion "
                "cérébrale).", "D"),
        ("A.2", "Les principes de l'anesthésie pour le traitement endovasculaire sont les mêmes "
                "que ceux de la chirurgie : maintien d'une PPC suffisante et immobilité "
                "absolue.", "E"),
        ("A.3", "Les patients d'HSA grave hospitalisés en réanimation et ventilés ne présentent "
                "aucune contre-indication aux opiacés ; l'utilisation du paracétamol est "
                "intéressante par son effet antipyrétique associé.", "E"),
        ("A.4", "Les AINS sont à discuter, car ils induisent des risques mal documentés.", "E"),
    ], [11 * mm, PAGE_W - 2 * MARGIN - 11 * mm - 16 * mm, 16 * mm]))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<i>Note :</i> les curares, à l'exception de la succinylcholine, n'ont pas d'effet sur "
        "la circulation cérébrale et la pression intracrânienne.", S_NOTE))
    return story


def _section_vasospasme():
    story = [Spacer(1, 2 * mm)]
    story.append(section_bar("Vasospasme — aspects cliniques et diagnostic"))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "Le vasospasme est une réduction réversible de la lumière d'une artère de l'espace "
        "sous-arachnoïdien, débutant le plus souvent entre J4 et J14, identifiable par "
        "angiographie dans 30 à 70 % des cas. Il peut aboutir à un « déficit neurologique "
        "ischémique retardé » (DNI, 17-40 % des HSA anévrysmales) : altération de conscience, "
        "céphalées croissantes, déficit focal (hémiparésie, aphasie), souvent avec fièvre, "
        "HTA, leucocytose et/ou hyponatrémie. Diagnostic clinique difficile chez les patients "
        "de grade élevé ou sous sédation ; peut évoluer vers l'infarctus cérébral.",
        S_BODY_SM))
    story.append(Spacer(1, 2 * mm))
    story.append(reco_table([
        ("V.1", "La première étape du diagnostic par imagerie consiste à éliminer les autres "
                "causes d'aggravation neurologique (ischémie postopératoire, hydrocéphalie, "
                "resaignement, troubles hydroélectrolytiques, convulsions infracliniques) ; on "
                "réalisera un scanner de façon systématique.", "E"),
        ("V.2", "La réalisation quotidienne d'un Doppler transcrânien est recommandée. Seul le "
                "vasospasme de l'artère sylvienne peut être prédit avec une sensibilité et une "
                "spécificité suffisantes pour être validé en pratique clinique.", "E"),
        ("V.3", "La valeur seuil de 120 cm/s pour la vitesse moyenne du flux sanguin de "
                "l'artère cérébrale moyenne est celle retenue habituellement ; un rapport "
                "vitesse ACM/carotide interne extra-crânienne &gt; 3 traduit un vasospasme, "
                "&gt; 6 un vasospasme sévère.", "E"),
        ("V.4", "Un accroissement des vitesses supérieur à 50 cm/s par jour est un facteur "
                "prédictif de déficit neurologique.", "E"),
        ("V.5", "En cas de doute et pour pallier les limites du Doppler, l'IRM, le scanner de "
                "perfusion, ou toute imagerie évaluant le débit sanguin cérébral peuvent être "
                "utilisés, selon les possibilités locales.", "E"),
    ], [12 * mm, PAGE_W - 2 * MARGIN - 12 * mm - 16 * mm, 16 * mm]))
    return story


def _section_vasospasme_traitement():
    story = [Spacer(1, 2 * mm)]
    story.append(section_bar("Vasospasme — traitement préventif, curatif et endovasculaire"))
    story.append(Spacer(1, 2 * mm))
    story.append(reco_table([
        ("V.6", "La prévention pharmacologique du vasospasme cérébral dans les suites d'une HSA "
                "est basée sur l'utilisation de nimodipine (nombre de sujets à traiter pour une "
                "bonne évolution neurologique supplémentaire : 7 à 13).", "A"),
        ("V.7", "La nimodipine doit être administrée par voie orale à la dose de 360 mg/j "
                "pendant 21 jours (voie IV 1-2 mg/h selon le poids = alternative courante en "
                "France, à risque d'hypotension systémique).", "A"),
        ("V.8", "Cette durée de 21 jours pourrait être abrégée à 15 jours.", "D"),
        ("V.9", "L'hypotension sous nimodipine IV doit impérativement être corrigée.", "E"),
        ("V.10", "Le traitement hyperdynamique (« triple H therapy » : hypervolémie, "
                 "hypertension, hémodilution) n'a démontré son efficacité dans aucune étude "
                 "contrôlée randomisée ; la stratégie est réduite, dans la plupart des centres, "
                 "au contrôle de la volémie associé à l'HTA, une fois l'anévrysme sécurisé.", "E"),
        ("V.11", "Un objectif de PAM jusqu'à 100-120 mmHg peut être envisagé en l'absence "
                 "d'infarctus constitué (l'HTA contrôlée doit être limitée en cas d'infarctus, "
                 "pour réduire le risque de transformation hémorragique).", "E"),
        ("V.12", "Le traitement hyperdynamique nécessite un monitorage continu approprié "
                 "(mesure invasive de la PA et de la PVC au minimum) et un contrôle fréquent de "
                 "la natrémie, de la glycémie et de la température.", "E"),
        ("V.13", "L'infusion intra-artérielle de vasodilatateur (papavérine, nimodipine diluée) "
                 "et/ou l'angioplastie par ballonnet sont deux techniques endovasculaires "
                 "utilisables pour le traitement du vasospasme (évaluation en cours, "
                 "indications non généralisables).", "E"),
        ("V.14", "L'efficacité du traitement endovasculaire du vasospasme est corrélée à la "
                 "précocité de l'intervention.", "E"),
    ], [12 * mm, PAGE_W - 2 * MARGIN - 12 * mm - 16 * mm, 16 * mm]))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<i>Contexte (non gradé dans le texte source) :</i> en dehors de la nimodipine, aucun "
        "médicament (nicardipine, tirilazad, magnésium) n'a une efficacité démontrée dans la "
        "prévention du vasospasme après HSA. <i>Complications de la « triple H therapy » :</i> "
        "œdème cérébral et HTIC, hémorragie cérébrale, œdème pulmonaire. <i>Complications du "
        "traitement endovasculaire du vasospasme :</i> rares et habituellement transitoires "
        "(perfusions trop rapides) ; rupture artérielle en cours de dilatation par ballonnet = "
        "complication majeure, généralement catastrophique mais rare.", S_NOTE))
    return story


def _section_suivi_filiere():
    story = [Spacer(1, 2 * mm)]
    story.append(section_bar("Stratégie de suivi du malade"))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>Marqueurs et monitorage :</b> la protéine S100b (LCS et sang périphérique) "
        "augmente proportionnellement à la sévérité de l'HSA et est corrélée au pronostic à "
        "six mois ; une élévation secondaire est prédictive d'un vasospasme. Le monitorage "
        "métabolique invasif (PO2/PCO2/pH tissulaires) contribue à déceler HTIC et ischémie — "
        "la microdialyse est prometteuse mais lourde et discontinue ; la spectroscopie proche "
        "infrarouge n'a pas fait la preuve de sa fiabilité.",
        S_BODY_SM))
    story.append(Spacer(1, 2 * mm))
    story.append(reco_table([
        ("S.1", "La protéine S100b peut s'intégrer dans le monitorage multimodal des patients "
                "ayant une HSA d'origine anévrysmale.", "E"),
        ("S.2", "Chez les patients en grade sévère d'HSA, un monitorage systématique de la PIC "
                "par une DVE ou, à défaut, par capteur intraparenchymateux, est recommandé ; la "
                "DVE est utilisée avec une contre-pression de 15 cmH2O.", "E"),
        ("S.3", "Pendant la phase aiguë, la réalisation d'un Doppler par jour est utile pour "
                "détecter l'apparition d'un vasospasme, principalement sur le territoire "
                "sylvien — même recommandation que V.2, répétée par la source dans cette "
                "section dédiée au suivi.", "E"),
    ], [11 * mm, PAGE_W - 2 * MARGIN - 11 * mm - 16 * mm, 16 * mm]))
    story.append(Spacer(1, 3 * mm))

    story.append(section_bar("Filière de prise en charge de l'HSA"))
    story.append(Spacer(1, 2 * mm))
    story.append(reco_table([
        ("F.1", "Une filière de prise en charge permettant l'hospitalisation dans le centre de "
                "référence dans les plus brefs délais doit être préalablement établie dans "
                "chaque région ; l'information des différents acteurs potentiels de la filière "
                "d'amont doit être assurée.", "E"),
        ("F.2", "Le centre de référence doit traiter un nombre suffisant de patients souffrant "
                "d'HSA pour entretenir une filière interne efficace.", "E"),
        ("F.3", "Cette filière doit prendre en compte les particularités propres à chaque "
                "établissement.", "E"),
        ("F.4", "Cela implique : en amont, un diagnostic précoce reposant sur la qualité de "
                "formation des médecins généralistes et urgentistes ; au cours de "
                "l'hospitalisation, le traitement précoce du sac anévrysmal dès que les "
                "conditions physiologiques le permettent.", "E"),
    ], [11 * mm, PAGE_W - 2 * MARGIN - 11 * mm - 16 * mm, 16 * mm]))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<i>Note :</i> le centre de référence doit assurer une prise en charge "
        "multidisciplinaire (neuroradiologue, neurochirurgien, neuroanesthésiste-réanimateur) "
        "et pouvoir réaliser rapidement bilan neuroradiologique, radiologie interventionnelle "
        "et intervention neurochirurgicale. L'accord du centre de référence doit être obtenu "
        "avant transfert par un échange téléphonique de senior à senior, sans exclure la "
        "transmission d'un dossier circonstancié. L'échange d'informations et la coopération "
        "avec les centres de rééducation sont importants pour la récupération à long terme.",
        S_NOTE))
    return story


def _section_sources():
    story = [Spacer(1, 3 * mm)]
    story.append(section_bar("Sources et traçabilité", color=GREY))
    story.append(Spacer(1, 2 * mm))
    story.append(P(
        "<b>Document source :</b> « Hémorragie sous-arachnoïdienne grave », conférence "
        "d'experts, texte court, 2004. Société française d'anesthésie et de réanimation "
        "(SFAR), en partenariat avec l'Association de neuroanesthésie-réanimation de langue "
        "française (ANARLF), la Société française de neurochirurgie et la Société française "
        "de neuroradiologie. Panel présidé par le Pr L. Beydon (Angers).", S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>Méthodologie :</b> conférence d'experts (et non recommandation GRADE), motivée par "
        "le faible niveau de preuve de la majorité des études disponibles. Grades A/B/D/E "
        "imprimés par le jury ; signification précise non définie dans ce texte court (voir "
        "disclosure, page 1) ; aucune occurrence de Grade C dans le corps du texte.",
        S_SOURCE))
    story.append(P(
        "<b>URL source :</b> https://sfar.org/hemorragie-sous-arachnoidienne-hsa-grave/",
        S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>Couverture :</b> cette fiche reprend l'intégralité des recommandations graduées du "
        "corps du texte (diagnostic et prise en charge initiale, complications précoces, "
        "traitement de l'anévrysme, anesthésie et douleur, vasospasme, stratégie de suivi, "
        "filière de prise en charge), ainsi que les 4 tableaux de classification (WFNS, Hunt "
        "et Hess, échelle de Fisher, index bicaudé). Les listes de composition du panel "
        "d'experts et du groupe de lecture (noms et villes) ne sont pas reproduites.",
        S_SOURCE))
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Avertissement :</b> ce document est une fiche de synthèse indépendante, produite "
        "pour un usage d'aide-mémoire. Il reprend l'intégralité des recommandations graduées "
        "du texte source, mais ne remplace pas le texte intégral (argumentaire scientifique "
        "complet, références bibliographiques) et n'est ni édité ni validé par la SFAR, "
        "l'ANARLF, la Société française de neurochirurgie ou la Société française de "
        "neuroradiologie. Conférence de 2004 : se référer également, en complément, aux "
        "recommandations et pratiques plus récentes sur la prise en charge de l'HSA "
        "anévrysmale et à un avis spécialisé (centre de référence neurovasculaire) en cas de "
        "doute.",
        S_BODY_SM), bg=GREY_LIGHT, border=GREY))
    return story


def _section_1():
    return (_section_intro() + [Spacer(1, 3 * mm)] + _section_diagnostic()
            + [Spacer(1, 2 * mm)] + _section_imagerie())


def _section_2():
    return (_section_complications() + [Spacer(1, 3 * mm)] + _section_complications2()
            + [Spacer(1, 3 * mm)] + _section_traitement())


def _section_3():
    return _section_anesthesie_douleur() + [Spacer(1, 3 * mm)] + _section_vasospasme()


def _section_4():
    return _section_vasospasme_traitement()


def _section_5():
    return _section_suivi_filiere() + [Spacer(1, 3 * mm)] + _section_sources()


SECTIONS = [
    ("Introduction, méthodologie, diagnostic initial & imagerie", _section_1),
    ("Complications précoces & traitement de l'anévrysme", _section_2),
    ("Anesthésie, douleur & vasospasme (clinique)", _section_3),
    ("Vasospasme — traitement", _section_4),
    ("Suivi, filière & traçabilité", _section_5),
]


def _make_doc(path=None):
    return SimpleDocTemplate(path or OUT, pagesize=A4,
                              leftMargin=MARGIN, rightMargin=MARGIN,
                              topMargin=32 * mm, bottomMargin=16 * mm,
                              title="Fiche SFAR 2004 - Hémorragie sous-arachnoïdienne grave",
                              author="Synthèse indépendante (source SFAR/ANARLF)")


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
    # Throwaway measurement builds must NEVER write to OUT (see CLAUDE.md) - reusing OUT
    # here was found in a prior fiche to silently corrupt page 1's header_band in the final
    # build. Always use a fresh tempfile.mktemp() path for these measurement passes.
    import pypdf, tempfile
    tmp_path = tempfile.mktemp(suffix=".pdf")
    doc = _make_doc(tmp_path)
    doc.build(story_flowables, onFirstPage=_silent_page, onLaterPages=_silent_page)
    with open(tmp_path, "rb") as f:
        n = len(pypdf.PdfReader(f).pages)
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
