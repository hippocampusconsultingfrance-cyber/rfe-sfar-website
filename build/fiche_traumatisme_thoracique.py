# -*- coding: utf-8 -*-
"""
Fiche de synthese - RFE commune SFAR-SFMU 2015
Traumatisme thoracique : prise en charge des 48 premieres heures
Source verifiee : Anesth Reanim. 2015;1:272-287, disponible en ligne 23/05/2015. Methodologie
GRADE. Perimetre explicitement defini par la source : tout traumatisme thoracique (isole ou dans
le cadre d'un traumatise severe), EXCLUANT les atteintes cardiaques et diaphragmatiques, limite
aux 48 premieres heures de prise en charge. Resume officiel : 60 recommandations formalisees,
accord fort pour 50 (90%), accord faible pour 10 - la source ne marque PAS quelles recommandations
individuelles portent l'accord faible (contrairement a d'autres fiches du projet type
traumatisme_pelvien/intubation_difficile_adulte qui taguent "ACCORD FORT/FAIBLE" par
recommandation) : ce chiffre agrege est donc cite tel quel dans l'intro, sans etre reparti ligne
par ligne. Cette fiche inventorie ~50 enonces individuellement grades (chaque "Proposition X"
numerotee par la source regroupe souvent 1 a 3 phrases distinctement graduees) - le nombre de
lignes de cette fiche ne correspond donc pas necessairement au chiffre agrege "60" de la source
(meme pattern de non-reconciliation deja rencontre sur traumatisme_abdominal/pre-eclampsie : le
chiffre du resume officiel est cite verbatim, pas recalcule).

Piege d'extraction majeur (nouvelle variante) : le signe moins de "GRADE 1-"/"GRADE 2-" a ete
converti par l'extraction PyMuPDF en un caractere de controle non imprimable (\\x03, ETX) au lieu
d'etre supprime (voies_aeriennes_enfant) ou substitue par une lettre (traumatisme_pelvien) - le
texte source affichait donc "(G1\\x03)"/"(G2\\x03)" pour 5 recommandations distinctes (4.B.3b,
5.C.3, 6.B.1a, 6.B.1b, 7.B.b), toutes a formulation negative ("ne pas utiliser"/"ne proposent pas
de recourir"/"ne recommandent pas"/"si RCP>10-15min sans reponse"). Confirme de facon
particulierement solide ici : le propre paragraphe methodologique de la source (page 3) definit
litteralement "forte : il faut faire ou ne pas faire (GRADE 1+ ou 1\\x03) ; faible : ... (GRADE 2+
ou 2\\x03)" - la meme corruption de glyphe apparait dans la definition-meme de la convention de
gradation, confirmee par rendu visuel de la page 3 a 200dpi ("GRADE 1+ ou 1-" / "GRADE 2+ ou 2-"
imprimes noir sur blanc). Toutes les 5 occurrences corrigees en "-" avant integration.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from style import *
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.units import mm

OUT = "/private/tmp/claude-501/-Users-macbook-Downloads-claude/65498e3e-5ddf-47a6-b100-3ac535d1faa0/scratchpad/rfe_sfar/output/Fiche_SFAR_Traumatisme_Thoracique_2015.pdf"

SOURCE_TXT = ("Source : Recommandations Formalisées d'Experts communes SFAR-SFMU « Traumatisme "
              "thoracique : prise en charge des 48 premières heures » — Anesth Reanim. "
              "2015;1:272-287, disponible en ligne le 23/05/2015. Méthodologie GRADE. Fiche de "
              "synthèse non officielle : se référer au texte intégral.")

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

def legend_flowable():
    items = [("1+", "Il faut faire"), ("1-", "Il ne faut pas faire"),
             ("2+", "Il faut probablement"), ("2-", "Il ne faut probablement pas")]
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

TOTAL_PAGES = {"n": 12}

def on_page(canvas, doc, page_title):
    header_band(canvas, doc, "SFAR / SFMU — RFE 2015 — FICHE DE SYNTHÈSE",
                "Traumatisme thoracique — 48 premières heures",
                page_title, icon_fn=lambda c,x,y: icon_shield(c, x, y, 13*mm), color=RED)
    footer_band(canvas, doc, SOURCE_TXT, f"Page {doc.page} / {TOTAL_PAGES['n']}")

# ---------------------------------------------------------------------------
def _section_intro():
    story = []
    story.append(Spacer(1, 3*mm))
    story.append(info_panel(P(
        "<b>Champ :</b> tout traumatisme thoracique (bénin comme sévère d'emblée), isolé ou "
        "associé à d'autres lésions dans le cadre d'un traumatisé sévère. Exclusions explicites de "
        "la source : atteintes cardiaques et diaphragmatiques, et prise en charge au-delà des 48 "
        "premières heures. Comité SFAR/SFMU, avec la SFCTCV (chirurgie thoracique/cardiovasculaire) "
        "et la SFR ; méthode GRADE®, format PICO, 7 questions.<br/><br/>"
        "<b>Résultats (résumé officiel) :</b> 60 recommandations formalisées ; accord fort pour "
        "50 (90 %), accord faible pour 10 — la source ne précise pas, recommandation par "
        "recommandation, lesquelles portent l'accord faible ; ce chiffre agrégé est donc cité tel "
        "quel plutôt que réparti ligne par ligne.<br/><br/>"
        "<i>Première RFE française sur ce sujet — aucune recommandation antérieure d'une société "
        "savante française n'existait sur la prise en charge spécifique du traumatisme "
        "thoracique.</i>",
        S_BODY), bg=BG_PANEL, border=TEAL))
    story.append(Spacer(1, 3*mm))

    story.append(section_bar("Légende des grades (méthodologie GRADE)"))
    story.append(Spacer(1, 2*mm))
    story.append(legend_flowable())
    return story

def _section_q1():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Question 1 — Critères de gravité et orientation"))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("1A", "Les experts recommandent de considérer comme éléments de gravité potentielle les "
         "antécédents du patient : un âge de plus de 65 ans, une pathologie pulmonaire ou "
         "cardiovasculaire chronique, un trouble de la coagulation congénital ou acquis "
         "(traitement anticoagulant ou antiagrégant), les circonstances de survenue telles qu'un "
         "traumatisme de forte cinétique et/ou un traumatisme pénétrant.", "1+"),
        ("1B (a)", "Les experts recommandent de considérer comme critères de gravité lors d'un "
         "traumatisme thoracique : l'existence de plus de 2 fractures de côtes, surtout chez un "
         "patient âgé de plus de 65 ans, la constatation d'une détresse respiratoire clinique "
         "(FR &gt; 25/min et/ou hypoxémie SpO2 &lt; 90 % sous air ou &lt; 95 % malgré "
         "oxygénothérapie), d'une détresse circulatoire (chute de PAS &gt; 30 % ou PAS "
         "&lt; 110 mmHg).", "1+"),
        ("1B (b)", "Les experts proposent l'utilisation du score de MGAP afin de trier les patients "
         "ne présentant pas de critère de gravité initiale.", "2+"),
        ("1C (a)", "Les experts recommandent un transport médicalisé pour tout patient présentant "
         "des critères potentiels de gravité ou des signes de détresse vitale. L'orientation se "
         "fera vers un centre de référence dès l'existence de signes de détresse respiratoire "
         "et/ou circulatoire.", "1+"),
        ("1C (b)", "Les experts proposent que tout patient présentant un terrain à risque bénéficie "
         "d'un avis spécialisé, si nécessaire par téléphone ou télétransmission. Ces patients "
         "doivent pouvoir être surveillés pendant 24 heures. Les experts proposent de mettre en "
         "place des conventions entre établissements pour organiser les conditions de réalisation "
         "des avis spécialisés.", "AE"),
    ], [16*mm, PAGE_W-2*MARGIN-16*mm-20*mm, 20*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(P("Antécédents pulmonaires sévères, cardiovasculaires ou âge &gt; 65 ans : "
                    "risque de décès ×2-3 (RR = 1,98 IC95 [1,86-2,11]) ; traumatisme pénétrant : "
                    "mortalité ×2,6 (IC95 [2,42-2,85]). PAS &lt; 110 mmHg : reflet d'une défaillance "
                    "circulatoire possible, prédit le recours à une intervention urgente à "
                    "l'admission. Score MGAP (Mécanisme, Glasgow, Âge, Pression Artérielle) : "
                    "permet de trier les patients à faible risque de mortalité. Admission directe "
                    "en centre spécialisé (vs admission préalable en centre non spécialisé) réduit "
                    "significativement la mortalité (RR = 0,88 IC95 [0,6-0,88]) ; une admission "
                    "préalable en hôpital de proximité s'accompagne au contraire d'une "
                    "surmortalité (RR = 2,70 IC95 [1,31-5,6]).", S_NOTE))
    return story

def _section_q2():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Question 2 — Stratégie diagnostique"))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("2A (a)", "En préhospitalier, en complément de l'examen clinique, les experts suggèrent "
         "que l'échographie pleuropulmonaire soit associée à la FAST échographie à la recherche "
         "d'un épanchement gazeux ou liquidien, associée à une évaluation péricardique. Cet examen "
         "doit être réalisé par un praticien expérimenté et ne doit pas retarder la prise en "
         "charge.", "2+"),
        ("2A (b)", "Au déchocage, les experts recommandent l'échographie pleuropulmonaire associée "
         "à la FAST écho- et la radiographie du thorax en première intention.", "1+"),
        ("2B (a)", "Chez les patients avec critères de gravité, les experts recommandent la "
         "réalisation systématique d'une tomodensitométrie thoracique avec injection en tant "
         "qu'élément de la tomodensitométrie corps entier.", "1+"),
        ("2B (b)", "Les experts suggèrent de faire une échographie pleuropulmonaire et de ne pas "
         "réaliser de radiographies du thorax si l'examen clinique ne met en évidence qu'une "
         "lésion pariétale bénigne isolée sans critère de gravité.", "2+"),
        ("2B (c)", "En cas de lésion thoracique, autre que pariétale, suspectée par l'examen "
         "clinique ou révélée par l'échographie pleuropulmonaire ou une radiographie du thorax, "
         "les experts recommandent la réalisation d'une tomodensitométrie thoracique injectée.", "1+"),
    ], [16*mm, PAGE_W-2*MARGIN-16*mm-20*mm, 20*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(P("Échographie pleurale : sensibilité 78,6 % (IC95 [68,1-98,1]) et spécificité "
                    "98,4 % (IC95 [97,3-99,5]) pour le pneumothorax, supérieure à la radiographie "
                    "thoracique — mais la radiographie au lit reste obligatoire comme examen "
                    "radiologique initial des traumatisés graves instables. TDM thoracique injectée "
                    "= examen de référence pour le diagnostic exhaustif ; intégrée à une TDM corps "
                    "entier, réduction relative de mortalité intrahospitalière de 25 % (IC95 "
                    "[14-37]) vs score TRISS et de 13 % (IC95 [4-23]) vs score RISC. Radiographie "
                    "de thorax inutile chez les patients conscients, sans douleur thoracique, avec "
                    "un traumatisme fermé et un examen clinique normal.", S_NOTE))
    return story

def _section_q3():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Question 3 — Support ventilatoire"))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("3.A.1", "En milieu intrahospitalier, face à une hypoxémie, les experts recommandent de "
         "délivrer une ventilation non invasive de type VSAI-PEP après réalisation d'une "
         "tomodensitométrie et du drainage d'un pneumothorax lorsqu'il est indiqué, en l'absence "
         "de contre-indication à la VNI et dans un environnement disposant d'une surveillance "
         "continue.", "1+"),
        ("3.A.2", "La ventilation mécanique après intubation en induction séquence rapide est "
         "recommandée en l'absence d'amélioration clinique ou gazométrique à une heure.", "1+"),
        ("3.B.1", "Les experts recommandent que le volume courant soit réglé entre 6 et 8 mL/kg de "
         "poids idéal en raison du caractère non homogène du poumon traumatisé. La pression "
         "plateau doit être maintenue &lt; 30 cmH2O.", "1+"),
        ("3.B.2", "Chez le patient hypoxémique, les experts proposent d'adapter la PEP afin de "
         "maintenir une FiO2 &lt; 60 % et une SpO2 &gt; 92 % si la tolérance hémodynamique et "
         "ventilatoire le permet. La PEP doit être au moins égale à 5 cmH2O.", "2+"),
    ], [16*mm, PAGE_W-2*MARGIN-16*mm-20*mm, 20*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(P("VNI chez l'hypoxémique (PaO2/FiO2 &lt; 200 mmHg) : réduit le recours à "
                    "l'intubation (RR = 0,32 IC95 [0,12 ; 0,86]), diminue l'incidence des "
                    "pneumopathies (RR = 0,34 IC95 [0,2 ; 0,58]), réduit la durée de séjour "
                    "d'environ 4 jours, diminue la mortalité (OR = 0,26 IC95 [0,09 ; 0,71]). Un "
                    "rapport PaO2/FiO2 &lt; 146 mmHg après 1h de VNI est associé de façon "
                    "indépendante au recours à l'intubation (OR = 2,51 IC95 [1,45 ; 4,35]) — le "
                    "patient traumatisé thoracique est réputé à estomac plein, justifiant une "
                    "induction en séquence rapide. Volume courant 6-8 mL/kg : bénéfice sur la "
                    "mortalité (réduction 20-40 %) extrapolé d'études SDRA comportant peu de "
                    "patients traumatisés, mais les experts considèrent la ventilation mécanique "
                    "comme une « seconde agression » justifiant la même prudence. PEP ≥ 5 cmH2O : "
                    "méta-analyse ALVEOLI/LOVS/EXPRESS — diminution de la mortalité hospitalière "
                    "(OR = 0,90 IC95 [0,81 ; 1,00]) et en réanimation (OR = 0,85 IC95 [0,76 ; "
                    "0,95]) chez l'hypoxémique, niveau de preuve plus faible que pour le volume "
                    "courant (études comportant seulement 6 % de patients traumatisés).", S_NOTE))
    return story

def _section_q4a():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Question 4 — Stratégies analgésiques (1/2) : préhospitalier"))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("4.A.1", "Le contrôle de la douleur est une urgence. Les experts recommandent une "
         "évaluation systématique de l'intensité de la douleur en utilisant une échelle numérique "
         "(EN) de première intention, sinon une échelle verbale simple (EVS). La mesure doit se "
         "faire au repos, mais aussi lors de la toux et de l'inspiration profonde.", "2+"),
        ("4.A.2", "En présence d'une douleur intense, une titration par morphine est recommandée "
         "avec pour objectif le soulagement défini par une EN ≤ 3 ou EVS &lt; 2.", "1+"),
        ("4.A.3 (a)", "Pour la mobilisation du patient, après une titration morphinique bien "
         "conduite mais insuffisante, les experts recommandent l'utilisation de la kétamine.", "AE"),
        ("4.A.3 (b)", "Si un geste invasif s'avère nécessaire, il doit se faire avec une analgésie "
         "sédation efficace.", "AE"),
    ], [18*mm, PAGE_W-2*MARGIN-18*mm-20*mm, 20*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(P("Échelle numérique validée en médecine d'urgence, fortement corrélée à "
                    "l'échelle visuelle analogique, utilisable dans 96 % des cas. Titration "
                    "morphinique aux urgences : efficacité démontrée chez 82 % de 621 patients "
                    "traités pour douleur sévère (Lvovschi). Kétamine en sédation-analgésie "
                    "procédurale : sédation adaptée, taux élevé de satisfaction des patients, taux "
                    "d'apnée/hypoxémie inférieur ou égal au propofol selon les études ; midazolam "
                    "associé à des apnées/hypoxémies et un retard de réveil — sédation en "
                    "ventilation spontanée sans protection des voies aériennes, balance "
                    "bénéfice/risque à mesurer pour chaque patient.", S_NOTE))
    return story

def _section_q4b():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Question 4 — Stratégies analgésiques (2/2) : intrahospitalier"))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("4.B.1", "Les experts suggèrent d'évaluer la douleur spontanée de repos et d'effort (toux "
         "efficace et inspiration profonde) grâce aux échelles EN ou EVS, avec pour objectif cible "
         "une EN ≤ 3 ou une EVS ≤ 2.", "2+"),
        ("4.B.2 (a)", "L'anesthésie locorégionale (ALR) doit pouvoir être proposée chez le patient "
         "à risque ainsi que chez le patient présentant une douleur non contrôlée dans les "
         "12 heures.", "1+"),
        ("4.B.2 (b)", "Il faut probablement préférer le bloc para vertébral à l'analgésie "
         "péridurale lors de lésions costales unilatérales, et si possible sous contrôle "
         "échographique pour la mise en place d'un cathéter.", "2+"),
        ("4.B.2 (c)", "Lors de lésions complexes (multi-étagées) ou bilatérales, les experts "
         "recommandent que l'analgésie péridurale soit proposée, le geste devant être alors "
         "réalisé par un anesthésiste réanimateur.", "1+"),
        ("4.B.3 (a)", "Les experts recommandent que l'analgésie soit multimodale (dans le respect "
         "des contre-indications) en privilégiant la morphine avec une administration par mode PCA "
         "(analgésie contrôlée par le patient). Cette technique peut compléter efficacement un "
         "bloc paravertébral.", "1+"),
        ("4.B.3 (b)", "Les experts suggèrent de ne pas utiliser le mode PCA pour la morphine en "
         "systémique en présence d'une analgésie péridurale.", "2-"),
    ], [18*mm, PAGE_W-2*MARGIN-18*mm-20*mm, 20*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(P("Analgésie péridurale (APD) : supériorité sur la PCA pour le risque de "
                    "pneumonie (RR = 6 IC95 [1-35], Bulger 2004) ; augmentation du volume courant "
                    "de 45 % entre J1-J3 sous péridurale thoracique vs diminution de 56 % sous "
                    "morphine systémique (Moon et al.). Bloc paravertébral vs péridurale : "
                    "supériorité en termes de complications hypotensives (RR = 0,11 IC95 "
                    "[0,05-0,25]) et d'échecs de pose (RR = 0,51 IC95 [0,30-0,86]) — mais ne peut "
                    "être proposé que pour des fractures de côtes unilatérales et peu étendues. "
                    "PCA morphine non associée à la péridurale car des opioïdes y sont déjà "
                    "fréquemment utilisés.", S_NOTE))
    return story

def _section_q5():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Question 5 — Indications et modalités du drainage pleural"))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("5.A (a)", "Les experts recommandent une décompression en urgence en cas de détresse "
         "respiratoire aiguë ou hémodynamique avec forte suspicion de tamponnade gazeuse.", "1+"),
        ("5.A (b)", "Les experts suggèrent une thoracostomie par voie axillaire en cas d'arrêt "
         "cardiaque et/ou en cas d'échec de l'exsufflation.", "2+"),
        ("5.B (a)", "Les experts recommandent de drainer sans délai tout pneumothorax complet, "
         "tout épanchement liquidien ou aérique responsable d'un retentissement respiratoire "
         "et/ou hémodynamique.", "1+"),
        ("5.B (b)", "Les experts suggèrent de drainer un hémothorax évalué à plus de 500 mL "
         "(critère échographique et/ou radio-TDM).", "2+"),
        ("5.B (c)", "En cas de pneumothorax minime, unilatéral et sans retentissement clinique, le "
         "drainage n'est pas systématique : surveillance simple avec nouvelle radiographie de "
         "contrôle à 12 h. En cas de nécessité d'une ventilation mécanique invasive, le drainage "
         "thoracique n'est pas systématique non plus. En cas de bilatéralité du pneumothorax, "
         "s'ils sont minimes, le drainage n'est pas systématique mais discuté au cas par cas selon "
         "le caractère de l'épanchement gazeux.", "AE"),
        ("5.C.1", "Les experts suggèrent que le drainage ou la décompression soit réalisé par voie "
         "axillaire au 4e ou 5e EIC sur la ligne axillaire moyenne plutôt que par voie antérieure. "
         "Les experts suggèrent la mise en place de drains non traumatisants à bout mousse, en "
         "évitant l'usage d'un trocart court et/ou à bout tranchant.", "2+"),
        ("5.C.2", "Les experts proposent l'emploi de drains de faible calibre (18 à 24 F) pour le "
         "drainage des pneumothorax isolés. En cas d'hémothorax, les experts proposent d'utiliser "
         "des drains de gros calibre (28 à 36 F). L'emploi de drains de petit calibre de type "
         "« queue de cochon » est considéré comme une alternative possible pour le drainage des "
         "pneumothorax isolés, sans épanchement hématique associé.", "2+"),
        ("5.C.3", "Les experts ne proposent pas de recourir à une antibioprophylaxie avant "
         "drainage thoracique dans le cas des traumatismes thoraciques fermés.", "2-"),
    ], [16*mm, PAGE_W-2*MARGIN-16*mm-20*mm, 20*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(P("Voie axillaire (triangle de sécurité) : utilisée dans &gt; 90 % des cas dans "
                    "la littérature, sans excès de malposition dans plusieurs séries — mais une "
                    "étude rapporte plus de malpositions par voie axillaire que par voie antérieure "
                    "(25 % vs 9,5 %), sans que l'efficacité du drainage en urgence en soit "
                    "significativement affectée. Drains de faible calibre pour pneumothorax isolé : "
                    "efficacité comparable aux drains de plus gros calibre (échec 18 % vs 21 %, "
                    "p &lt; 0,6), durée de drainage et d'hospitalisation réduites. Drains de gros "
                    "calibre nécessaires pour l'hémothorax (risque d'obstruction par caillots avec "
                    "les petits drains, hémothorax résiduel corrélé à empyème/atélectasies/"
                    "fibrose). Antibioprophylaxie : bénéfice démontré pour les traumatismes "
                    "pénétrants (OR 0,28 IC95 [0,14-0,57]) mais aucune différence significative "
                    "pour les traumatismes fermés — d'où l'absence de recommandation "
                    "d'antibioprophylaxie systématique dans ce contexte spécifique.", S_NOTE))
    return story

def _section_q6():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Question 6 — Chirurgie et radiologie interventionnelle (TT fermé)"))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("6.A.1 (a)", "Les experts recommandent un traitement endovasculaire des lésions "
         "traumatiques de l'isthme aortique en première intention.", "1+"),
        ("6.A.1 (b)", "En l'absence de rupture complète, la prise en charge d'une autre urgence "
         "vitale prime sur la mise en place de l'endoprothèse. Les lésions aortiques minimes "
         "(rupture intimo-médiale) bénéficient d'un avis spécialisé.", "AE"),
        ("6.A.2", "Les experts proposent le traitement endovasculaire des lésions traumatiques "
         "axillaires ou sous-clavières comme une alternative possible à la chirurgie.", "2+"),
        ("6.B.1 (a)", "Les experts ne recommandent pas la réalisation d'une thoracotomie de "
         "ressuscitation en préhospitalier pour le traumatisme thoracique fermé.", "1-"),
        ("6.B.1 (b)", "En intrahospitalier, les experts suggèrent de ne pas réaliser de "
         "thoracotomie de ressuscitation en cas d'arrêt cardiaque après traumatisme thoracique "
         "fermé, si la durée de réanimation cardiopulmonaire dépasse 10 min sans récupération "
         "d'une activité circulatoire, et/ou lors d'une asystolie initiale en l'absence de "
         "tamponnade.", "2-"),
        ("6.B.2", "Les experts proposent qu'une thoracotomie d'hémostase soit réalisée : en cas "
         "d'instabilité hémodynamique et de saignement intrathoracique actif dans le drain "
         "thoracique (sans autre cause de saignement) ; ou en cas de stabilité hémodynamique si le "
         "débit du drain est supérieur à 1500 mL d'emblée avec poursuite &gt; 200 mL/h dès la "
         "première heure, ou inférieur à 1500 mL avec poursuite &gt; 200 mL/h pendant 3 heures.", "AE"),
        ("6.B.3", "Les experts recommandent la réalisation d'une thoracoscopie chirurgicale pour "
         "les hémothorax résiduels malgré un premier drainage thoracique bien conduit.", "1+"),
        ("6.B.4 (a)", "Les experts recommandent une fixation chirurgicale chez le patient "
         "présentant un volet thoracique et ventilé mécaniquement, si l'état respiratoire ne "
         "permet pas un sevrage de la ventilation mécanique dans les 36 heures suivant leur "
         "admission.", "1+"),
        ("6.B.4 (b)", "Les experts proposent que tout fracas costal déplacé ou complexe bénéficie "
         "d'un avis spécialisé.", "AE"),
    ], [18*mm, PAGE_W-2*MARGIN-18*mm-20*mm, 20*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(P("Rupture traumatique de l'isthme aortique : endoprothèse couverte supérieure à "
                    "la chirurgie ouverte ou la surveillance simple en mortalité (9 % vs 19 % vs "
                    "46 %), traitement dans les 24h en l'absence de lésion extra-aortique "
                    "engageant le pronostic vital ; les ruptures de grade IV (complètes) restent "
                    "une urgence chirurgicale absolue. Thoracotomie de ressuscitation (EDT) en "
                    "traumatisme fermé : survie 1,4 % seulement (vs 8,8 % pour le pénétrant, sur "
                    "&gt; 4600 patients) — jugée « futile » au-delà de 10 min de RCP préhospitalière "
                    "sans réponse et/ou asystolie initiale sans tamponnade. Débit de drain "
                    "&gt; 1500 mL d'emblée ou &gt; 200 mL/h : seuils des recommandations "
                    "américaines pour la thoracotomie d'hémostase, mortalité croissant linéairement "
                    "avec le débit du drain. Ostéosynthèse du volet costal : 3 études randomisées + "
                    "1 méta-analyse en faveur du traitement chirurgical (réduction des jours de "
                    "ventilation mécanique, des jours de réanimation, du taux de pneumopathies).", S_NOTE))
    return story

def _section_q7():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Question 7 — Spécificités du traumatisme thoracique pénétrant"))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("7.A (a)", "Les experts suggèrent d'orienter directement sur un centre disposant d'un "
         "plateau technique spécialisé les patients qui présentent un traumatisme pénétrant de "
         "l'aire cardiaque (stable ou instable) ou du thorax avec état circulatoire ou respiratoire "
         "instable ou stabilisé.", "1+"),
        ("7.A (b)", "Les experts suggèrent d'orienter sur le centre chirurgical de proximité les "
         "patients dont l'état hémodynamique ne permet pas le transport vers un centre spécialisé. "
         "Pour les patients stables, transfert secondaire si des lésions intrathoraciques sont "
         "objectivées sur le bilan.", "2+"),
        ("7.B (a)", "Les experts suggèrent la réalisation d'une thoracotomie de ressuscitation en "
         "cas d'arrêt cardiaque après traumatisme thoracique pénétrant, après avoir éliminé un "
         "pneumothorax compressif et en cas de détresse circulatoire majeure chez les patients "
         "échappant aux mesures réanimatoires.", "2+"),
        ("7.B (b)", "En intrahospitalier, les experts suggèrent de ne pas réaliser de thoracotomie "
         "de ressuscitation en cas d'arrêt cardiaque après traumatisme thoracique pénétrant, si la "
         "durée de réanimation cardiopulmonaire dépasse 15 min sans signe de vie, et lors d'une "
         "asystolie initiale en l'absence de tamponnade.", "2-"),
        ("7.C (a)", "Les experts suggèrent l'abord chirurgical du thorax (thoracotomie "
         "antéro-latérale gauche, transverse ou sternotomie) en urgence en cas d'instabilité "
         "hémodynamique et/ou d'épanchement péricardique compressif à l'échographie.", "2+"),
        ("7.C (b)", "Les experts suggèrent une surveillance simple, en milieu spécialisé, en "
         "l'absence d'épanchement péricardique, d'hémothorax et de stabilité hémodynamique stricte "
         "après bilan tomodensitométrique.", "2+"),
        ("7.D", "Les experts suggèrent de réaliser une antibioprophylaxie en cas de traumatisme "
         "pénétrant du thorax. Par exemple, l'association amoxicilline + acide clavulanique et en "
         "cas d'allergie à la pénicilline, l'association clindamycine + aminoside, pendant 24 à "
         "48 h, en fonction de la nature et de l'importance de la plaie.", "2+"),
    ], [17*mm, PAGE_W-2*MARGIN-17*mm-20*mm, 20*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(P("Pronostic amélioré en centre expert, en particulier en cas de choc et/ou de "
                    "coma. Présence d'un chirurgien thoracique en salle : associée à la survie de "
                    "façon indépendante (RR = 4,70 IC95 [1,29-17,13], analyse multivariée sur "
                    "222 patients opérés). Thoracotomie de ressuscitation en traumatisme pénétrant : "
                    "survie 8,8 % (IC95 [7,8-9,8]) globalement, 16,8 % si plaie par arme blanche vs "
                    "4,3 % si arme à feu, 19,4 % si plaie cardiaque — jugée « futile » au-delà de "
                    "15 min de RCP sans signe de vie et/ou asystolie initiale sans tamponnade. "
                    "Échographie pour plaie de l'aire cardiaque : sensibilité 100 % (IC95 "
                    "[88,1-100]), spécificité 97 % — mais des faux négatifs existent en cas "
                    "d'hémothorax associé (décompression du péricarde dans la plèvre), justifiant "
                    "une exploration chirurgicale systématique en cas d'épanchement péricardique "
                    "confirmé.", S_NOTE))
    return story

def _section_synthese():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Synthèse et messages clés"))
    story.append(Spacer(1, 2*mm))
    story.append(P(
        "• Âge &gt; 65 ans, antécédents cardiopulmonaires, trouble de coagulation, cinétique "
        "forte/pénétrant = éléments de gravité potentielle ; &gt; 2 fractures de côtes, détresse "
        "respiratoire ou circulatoire = critères de gravité avérée ; score MGAP pour trier les "
        "patients sans critère initial.<br/>"
        "• Préhospitalier : échographie pleuropulmonaire + FAST + évaluation péricardique sans "
        "retarder la prise en charge. Au déchocage : échographie pleuropulmonaire + FAST + "
        "radiographie thoracique systématiques. TDM thoracique injectée si critère de gravité ou "
        "lésion suspectée non pariétale.<br/>"
        "• VNI (VSAI-PEP) en 1ère intention chez l'hypoxémique après TDM et drainage si indiqué ; "
        "intubation en ISR (estomac plein) si échec à 1h. Ventilation protectrice si intubé : "
        "Vt 6-8 mL/kg poids idéal, Pplateau &lt; 30 cmH2O, PEP ≥ 5 cmH2O.<br/>"
        "• Douleur = urgence dès la prise en charge préhospitalière (EN/EVS, titration morphine, "
        "kétamine pour la mobilisation). Intrahospitalier : ALR privilégiée si risque ou douleur "
        "non contrôlée à 12h — bloc paravertébral pour lésions unilatérales, péridurale (par "
        "anesthésiste réanimateur) pour lésions complexes/bilatérales ; PCA morphine en "
        "complément, probablement pas à associer à la péridurale (opioïdes déjà présents).<br/>"
        "• Décompression en urgence si détresse vitale avec suspicion de tamponnade gazeuse ; "
        "drainage sans délai si pneumothorax complet ou épanchement avec retentissement, "
        "hémothorax &gt; 500 mL ; voie axillaire préférée ; pas d'antibioprophylaxie systématique "
        "pour un drainage en contexte fermé.<br/>"
        "• Lésion de l'isthme aortique : endoprothèse couverte en 1ère intention, &lt; 24h. "
        "Thoracotomie de ressuscitation : proscrite en préhospitalier pour le traumatisme fermé "
        "(quelle que soit la durée de RCP) ; en intrahospitalier, à ne pas réaliser au-delà de "
        "10 min de RCP sans récupération d'activité circulatoire (fermé) ou 15 min sans signe de "
        "vie (pénétrant), ni en cas d'asystolie initiale sans tamponnade. Volet thoracique "
        "ventilé : fixation chirurgicale si échec de sevrage à 36h.<br/>"
        "• Traumatisme pénétrant : orientation directe vers centre spécialisé si aire cardiaque "
        "atteinte ou instabilité ; échographie pour plaie de l'aire cardiaque (prudence si "
        "hémothorax associé, faux négatifs possibles) ; antibioprophylaxie proposée.",
        S_BODY))
    story.append(Spacer(1, 5*mm))

    story.append(section_bar("Sources et traçabilité", color=GREY))
    story.append(Spacer(1, 2*mm))
    story.append(P(
        "<b>Document source :</b> « Traumatisme thoracique : prise en charge des 48 premières "
        "heures » — Recommandations Formalisées d'Experts communes SFAR-SFMU, avec la SFCTCV et "
        "la SFR. Anesth Reanim. 2015;1:272-287, disponible en ligne le 23/05/2015. Président "
        "P. Michelet (SFAR), secrétaire L. Ducros (SFMU).", S_SOURCE))
    story.append(Spacer(1, 1.5*mm))
    story.append(P("<b>Méthodologie :</b> GRADE®, format PICO, cotation Delphi en 2 tours. Tags "
                    "littéraux « (G1+/-) », « (G2+/-) » ou « (Avis d'experts) » imprimés après "
                    "chaque proposition — cités ici tels quels (« AE » = Avis d'experts). Piège "
                    "d'extraction identifié et corrigé avant intégration : le signe moins de "
                    "5 tags « G1- »/« G2- » a été corrompu en caractère de contrôle non imprimable "
                    "par l'extraction automatique du PDF source — confirmé par rendu visuel de la "
                    "page 3 (le paragraphe méthodologique lui-même définit littéralement "
                    "« GRADE 1+ ou 1- » / « GRADE 2+ ou 2- ») avant correction.", S_SOURCE))
    story.append(Spacer(1, 1.5*mm))
    story.append(P("<b>Couverture :</b> ~50 énoncés individuellement gradés reproduits "
                    "intégralement, structurés selon les 7 questions et sous-questions de la "
                    "source (chaque « Proposition » numérotée par la source pouvant regrouper "
                    "plusieurs phrases distinctement graduées, ici éclatées en lignes séparées). Le "
                    "résumé officiel de la source annonce un total agrégé de « 60 recommandations "
                    "formalisées » — chiffre cité tel quel dans l'introduction sans être recalculé "
                    "ni réparti ligne par ligne, la source elle-même ne détaillant pas cette "
                    "correspondance exacte.", S_SOURCE))
    story.append(Spacer(1, 3*mm))
    story.append(info_panel(P(
        "<b>Avertissement :</b> ce document est une fiche de synthèse indépendante, produite pour "
        "un usage d'aide-mémoire. Il reprend l'intégralité des recommandations de la RFE mais ne "
        "remplace pas le texte intégral et n'est ni édité ni validé par la SFAR/SFMU. Les atteintes "
        "cardiaques et diaphragmatiques ainsi que la prise en charge au-delà des 48 premières "
        "heures sont explicitement exclues du champ de cette RFE. En cas de doute, se référer au "
        "texte intégral, aux recommandations ultérieures et/ou à un avis spécialisé.",
        S_BODY_SM), bg=GREY_LIGHT, border=GREY))
    return story

SECTIONS = [
    ("Introduction, méthodologie", _section_intro),
    ("Q1 — Critères de gravité & orientation", _section_q1),
    ("Q2 — Stratégie diagnostique", _section_q2),
    ("Q3 — Support ventilatoire", _section_q3),
    ("Q4 — Analgésie (1/2) préhospitalier", _section_q4a),
    ("Q4 — Analgésie (2/2) intrahospitalier", _section_q4b),
    ("Q5 — Drainage pleural", _section_q5),
    ("Q6 — Chirurgie & radiologie interventionnelle", _section_q6),
    ("Q7 — Traumatisme pénétrant : spécificités", _section_q7),
    ("Synthèse, sources & traçabilité", _section_synthese),
]

def _make_doc():
    return SimpleDocTemplate(OUT, pagesize=A4,
                              leftMargin=MARGIN, rightMargin=MARGIN,
                              topMargin=32*mm, bottomMargin=16*mm,
                              title="Fiche SFAR-SFMU 2015 - Traumatisme thoracique",
                              author="Synthèse indépendante (source SFAR/SFMU)")

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
