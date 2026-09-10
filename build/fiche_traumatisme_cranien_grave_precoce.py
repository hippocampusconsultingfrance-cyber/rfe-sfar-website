# -*- coding: utf-8 -*-
"""
Fiche de synthese - Recommandations formalisees d'experts (RFE, actualisation)
SFAR/Anarlf/SFMU/SFNC/GFRUP/Adarpef, decembre 2016 : "Prise en charge des
traumatises craniens graves a la phase precoce (24 premieres heures)".
Source : sources/traumatisme_cranien_grave_precoce.pdf (23 pages, revue
Anesth Reanim. 2016;2:431-453), sources/traumatisme_cranien_grave_precoce.txt
(texte extrait integralement, 149012 caracteres). Texte valide par le Conseil
d'administration de la Sfar le 21/09/2016. Pas de tampon d'obsolescence
detecte ; library_final.json marque ce document "en vigueur".

PAS UN DOUBLON : le corpus a deja une fiche "traumatisme_cranien" (source
differente : "Prise en charge neurochirurgicales des traumatismes
cranio-encephaliques de l'adulte et de l'enfant a la phase initiale") et une
fiche "traumatisme_cranien_leger" (TC legers/moderes) - verifie par
comparaison des href/pdf-url dans library_final.json : 3 documents distincts,
aucun chevauchement de source.

METHODOLOGIE - GRADE 1+/1-/2+/2-/AE (chip standard deja dans
style.GRADE_COLORS, pas d'extension locale necessaire). VERIFIE PAR RELECTURE
INTEGRALE ET RECOMPTAGE UN A UN CONTRE LA PROPRE SYNTHESE DU DOCUMENT (page
441 : "32 recommandations ont ete formalisees [...] 10 sont fortes (Grade 1),
18 sont faibles (Grade 2) et, pour 4 recommandations, la methode GRADE ne
peut pas s'appliquer et donnent lieu a des avis d'experts") : recompte exact
R1.1-R11.3 = 10x Grade1 (1+/-), 18x Grade2 (2+/-), 4x avis d'experts (AE) =
32/32, correspond exactement au total revendique par la source - AUCUN
enonce fabrique ou omis. "Accord FORT obtenu pour 100% des recommandations"
(texte source, 2 tours de cotation GRADE Grid) : pas de colonne "Accord"
distincte necessaire dans les tableaux (valeur constante, disclosee une
seule fois en methodologie plutot que repetee 32 fois).

PERIMETRE - integralite des 11 champs cliniques de cette RFE (gravite
initiale, prehospitalier, imagerie, indications neurochirurgicales,
sedation/analgesie, monitorage cerebral, HTIC medicale, polytraumatise,
epilepsie, homeostasie biologique, particularites enfant) = 32
recommandations completes avec leur rationnel clinique condense (l'
argumentaire complet de chaque recommandation, tres etoffe dans la source
avec revue de litterature detaillee, est condense ici en 1-3 phrases de
rationnel clinique + les seuils numeriques actionnables, sans reproduire la
bibliographie [1]-[302]). Introduction/Methodologie GRADE et
Participants/Conflits d'interets ne sont pas retranscrits (sans contenu
clinique).

DOUBLON PARTIEL DISCLOSE - le champ 12 de la source ("Controle cible de la
temperature (CCT) apres traumatisme cranien", R12.1-R12.6) est explicitement
une "Retranscription partielle des RFE 2016 SFAR/SRLF <<controle cible de la
temperature en reanimation>>" (texte source, note en tete de ce champ) : ces
6 recommandations sont DEJA integralement retranscrites dans la fiche
"controle_temperature" de ce corpus (build/fiche_controle_temperature.py,
Champ 2, R2.1-R2.3 + versions pediatriques R2.1P/R2.2P - verifie ligne a
ligne, texte identique). Non redupliquees ici : un encadre de renvoi resume
les seuils (35-37 degC prevention, 34-35 degC HTIC refractaire, enfant
normothermie) et pointe vers la fiche dediee, conformement a l'objectif du
projet d'eviter le contenu redondant.

_count_pages() : pattern copie de fiche_avc_precoce.py / fiche_aap_programmee.py
(PyMuPDF/fitz, jamais vers OUT, toujours vers tempfile.mktemp()).
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from style import *
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.units import mm

OUT = "/home/user/rfe-sfar-website/output/Fiche_SFAR_Traumatisme_Cranien_Grave_Phase_Precoce_2016.pdf"

SOURCE_TXT = ("Source : SFAR / Anarlf / SFMU / SFNC / GFRUP / Adarpef — RFE (actualisation) « Prise en "
              "charge des traumatisés crâniens graves à la phase précoce (24 premières heures) » "
              "(Anesth Reanim. 2016;2:431-453). Fiche de synthèse non officielle : se référer au texte "
              "intégral.")

def P(txt, style=S_CELL):
    return Paragraph(txt, style)

def chip(label, **kw):
    return grade_chip(label, **kw)

REF_W = 15 * mm
GRADE_W = 14 * mm

def reco_table(rows, col_widths=None):
    """rows: (ref, text, grade_label) - grade_label parmi '1+','1-','2+','2-','AE'."""
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

TOTAL_PAGES = {"n": 8}

def on_page(canvas, doc, page_title):
    header_band(canvas, doc, "SFAR/ANARLF/SFMU/SFNC/GFRUP/ADARPEF — RFE 2016 — FICHE DE SYNTHÈSE",
                "Traumatisme crânien grave — phase précoce (24 premières heures)",
                page_title, icon_fn=lambda c, x, y: icon_shield(c, x, y, 13 * mm), color=RED)
    footer_band(canvas, doc, SOURCE_TXT, f"Page {doc.page} / {TOTAL_PAGES['n']}")

# ---------------------------------------------------------------------------
def _section_intro_champ1_2():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Champ :</b> prise en charge des traumatisés crâniens (TC) <b>graves</b> "
        "(score de Glasgow ≤ 8) à la phase <b>précoce</b> (24 premières heures) — n'inclut pas "
        "les TC légers/modérés ni la neuroréanimation plus tardive. Actualisation SFAR/Anarlf/"
        "SFMU/SFNC/GFRUP/Adarpef, décembre 2016, des recommandations françaises de 1998 : ne "
        "présente que les évolutions significatives depuis 1998 sur 11 champs cliniques (le "
        "lecteur est renvoyé aux recommandations de 1998, toujours valables pour le reste). "
        "<b>32 recommandations formalisées</b> après méthode GRADE (2 tours de cotation "
        "GRADE Grid) : <b>accord FORT obtenu pour 100 % des recommandations</b> — 10 fortes "
        "(Grade 1), 18 faibles (Grade 2), 4 avis d'experts.", S_BODY), bg=BG_PANEL, border=RED))
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Méthodologie GRADE</b> (même schéma que le reste du corpus) : Grade <b>1+/1-</b> "
        "(preuve forte, « il faut/il ne faut pas faire ») ; Grade <b>2+/2-</b> (preuve modérée/"
        "faible/très faible, « il faut probablement/probablement pas faire ») ; <b>AE</b> (avis "
        "d'experts, littérature inexistante ou trop pauvre, validé à plus de 70 % d'accord). "
        "Vérifié par recomptage exhaustif un pour un contre la propre synthèse du document "
        "(page 441) : 10× Grade 1, 18× Grade 2, 4× AE = 32/32, exactement le total revendiqué "
        "par la source.", S_BODY_SM), bg=BG_PANEL, border=AMBER))
    story.append(Spacer(1, 3 * mm))

    story.append(section_bar("1 — Décrire et évaluer la gravité initiale", color=RED))
    story.append(Spacer(1, 2 * mm))
    cw = PAGE_W - 2 * MARGIN
    story.append(reco_table([
        ("R1.1", "Évaluer la gravité initiale à l'aide de l'échelle de Glasgow (en rapportant "
         "obligatoirement sa <b>composante motrice</b>, seule robuste sous sédation/intubation) "
         "ainsi que la taille et la réactivité pupillaire. Répéter l'examen clinique pendant la "
         "prise en charge initiale ; toute baisse ≥ 2 points du Glasgow doit faire réaliser en "
         "urgence une nouvelle TDM cérébrale.", "1+"),
        ("R1.2", "Rechercher et traiter les facteurs systémiques d'agression cérébrale "
         "secondaire : l'hypotension artérielle (PAS &lt; 90 mmHg ≥ 5 min) double la mortalité ; "
         "l'hypoxémie (~20 % des patients) est associée à une surmortalité ; leur association "
         "atteint jusqu'à 75 % de mortalité.", "1+"),
        ("R1.3", "Évaluer la gravité initiale sur des critères cliniques ET radiologiques "
         "(TDM). Scanner cérébral et du rachis cervical systématique et sans délai chez tout TC "
         "grave (GCS ≤ 8) ou modéré (GCS 9-13).", "1+"),
        ("R1.4", "Évaluer probablement la gravité initiale à l'aide du <b>Doppler "
         "transcrânien</b> (DTC) — index de pulsatilité (IP), vélocité diastolique (Vd) : "
         "doit faire partie du bilan initial du polytraumatisé au même titre que "
         "l'échographie abdominale ; abandonner après 10 min si difficultés techniques.", "2+"),
        ("R1.5", "Ne pas doser probablement les biomarqueurs (S100β, NSE, UCH-L1, GFAP, "
         "protéine tau...) en routine clinique pour évaluer la gravité initiale : performance "
         "insuffisante, valeur ajoutée non démontrée.", "2-"),
    ]))
    story.append(Spacer(1, 3 * mm))

    story.append(section_bar("2 — Prise en charge préhospitalière", color=RED))
    story.append(Spacer(1, 2 * mm))
    story.append(reco_table([
        ("R2.1", "Le TC grave doit être pris en charge par une équipe médicale préhospitalière, "
         "régulé par le SAMU, et adressé dès que possible dans un <b>centre spécialisé</b> avec "
         "plateau technique neurochirurgical — améliore le pronostic même pour un patient ne "
         "nécessitant finalement pas de neurochirurgie (expertise et disponibilité de l'équipe).", "1+"),
        ("R2.2", "Maintenir probablement une <b>PAS &gt; 110 mmHg</b> avant de disposer d'un "
         "monitorage cérébral : prévenir toute hypotension (pas d'hypnotique hypotenseur à "
         "l'induction, sédation continue, lutte contre l'hypovolémie) ; traitement rapide par "
         "amines vasopressives (phényléphrine et/ou noradrénaline) en cas d'hypotension.", "2+"),
        ("R2.3", "Contrôler la ventilation par intubation trachéale, ventilation mécanique et "
         "surveillance du CO<sub>2</sub> expiré (EtCO<sub>2</sub>) dès la prise en charge "
         "préhospitalière — cible EtCO<sub>2</sub> autour de <b>30-35 mmHg</b> (l'hypocapnie est "
         "vasoconstrictrice et ischémiante).", "1+"),
    ]))
    return story


def _section_champ3_6():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("3 — Stratégie de l'imagerie médicale", color=RED))
    story.append(Spacer(1, 2 * mm))
    story.append(reco_table([
        ("R3.1", "Réaliser sans délai une TDM cérébrale et du rachis cervical (sans injection) "
         "— coupes natives inframillimétriques, double fenêtrage (parenchyme + os). Examen de "
         "1er choix, conditionne la prise en charge neurochirurgicale et le choix du monitorage.", "1+"),
        ("R3.2", "Faire probablement précocement une angio-TDM des troncs supra-aortiques et "
         "vaisseaux intracrâniens chez les patients à risque de dissection traumatique "
         "(fracture du rachis cervical, déficit neurologique focal inexpliqué, syndrome de "
         "Claude Bernard Horner, fractures faciales Lefort II/III ou de la base du crâne, "
         "lésions des tissus mous du cou) — élargir probablement les indications chez les "
         "patients les plus graves (examen neurologique peu contributif).", "2+"),
    ]))
    story.append(Spacer(1, 3 * mm))

    story.append(section_bar("4 — Indications neurochirurgicales (hors monitorage)", color=RED))
    story.append(Spacer(1, 2 * mm))
    story.append(reco_table([
        ("R4.1", "Réaliser probablement un <b>drainage ventriculaire externe</b> pour contrôler "
         "l'HTIC après échec du traitement de 1ère ligne. Indications neurochirurgicales "
         "formelles précoces : évacuation d'un hématome extra-dural symptomatique (quelle que "
         "soit sa localisation), d'un hématome sous-dural aigu significatif (épaisseur &gt; 5 mm, "
         "déviation ligne médiane &gt; 5 mm), drainage d'une hydrocéphalie aiguë, parage/"
         "fermeture immédiate des embarrures ouvertes ; embarrure fermée compressive à opérer.", "2+"),
        ("R4.2", "Réaliser probablement une <b>craniectomie décompressive</b> pour contrôler la "
         "PIC en cas d'HTIC réfractaire, dans le cadre d'une discussion multidisciplinaire — "
         "décision au cas par cas (côté de la lésion indifférent). Étude RESCUE-ICP : mortalité "
         "réduite à 26,9 % (vs 48,9 % traitement médical) mais davantage de comas végétatifs/"
         "états pauci-relationnels (8,5 % vs 2,1 %) ; devenir favorable global inchangé.", "2+"),
    ]))
    story.append(Spacer(1, 3 * mm))

    story.append(section_bar("5 — Sédation, analgésie", color=RED))
    story.append(Spacer(1, 2 * mm))
    story.append(reco_table([
        ("R5.1", "En dehors d'une HTIC ou d'un état de mal épileptique, appliquer aux TC graves "
         "les <b>mêmes recommandations</b> de maintien/arrêt de la sédation-analgésie que pour "
         "les autres patients de réanimation. Priorité au contrôle de l'hémodynamique systémique "
         "dans le choix des drogues (barbituriques, bolus de midazolam ou fortes doses de "
         "morphiniques en bolus peuvent provoquer une hypotension délétère).", "AE"),
    ]))
    story.append(Spacer(1, 3 * mm))

    story.append(section_bar("6 — Monitorage cérébral", color=RED))
    story.append(Spacer(1, 2 * mm))
    story.append(reco_table([
        ("R6.1", "Avoir recours probablement à un <b>monitorage systématique de la PIC</b> "
         "après TC grave pour détecter une HTIC si : signe(s) d'HTIC sur l'imagerie, chirurgie "
         "périphérique urgente (hors urgence vitale), ou évaluation neurologique impossible. "
         "PIC 20-40 mmHg : risque de mortalité ×3 ; PIC &gt; 40 mmHg : ×7.", "2+"),
        ("R6.2", "Ne pas avoir recours probablement à un monitorage systématique de la PIC si "
         "le TC grave est isolé, la TDM initiale normale, sans critère de gravité clinique ni "
         "anomalie au DTC — bénéfice non démontré (étude BEST-TRIP), risques du monitorage "
         "(échec de pose ~10 %, infection 2,5-10 %, hémorragie 0-4 %). Si décidé malgré tout : "
         "préférer les fibres intra-parenchymateuses aux drains ventriculaires.", "2-"),
        ("R6.3", "Avoir recours probablement à un monitorage systématique de la PIC après "
         "évacuation d'un hématome intracrânien post-traumatique si <b>1 seul critère suffit</b> : "
         "Glasgow moteur préop ≤ 5, anisocorie/mydriase bilatérale préop, instabilité "
         "hémodynamique préop, signes de gravité à l'imagerie préop, œdème peropératoire, ou "
         "nouvelles lésions à l'imagerie postopératoire.", "2+"),
        ("R6.4", "Recourir à un monitorage <b>multimodal</b> (DTC et/ou pression tissulaire "
         "cérébrale en oxygène PtiO<sub>2</sub>) pour optimiser le débit sanguin et "
         "l'oxygénation cérébrale. Seuil ischémique PtiO<sub>2</sub> ≈ 15-20 mmHg (seuils "
         "modulés selon durée : &lt; 5 mmHg/30 min, &lt; 10 mmHg/1h45, &lt; 15 mmHg/4h).", "AE"),
    ]))
    return story


def _section_champ7_8():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("7 — Prise en charge médicale de l'hypertension intracrânienne", color=RED))
    story.append(Spacer(1, 2 * mm))
    story.append(reco_table([
        ("R7.1", "Individualiser probablement les objectifs de PIC et de PPC correspondant à la "
         "meilleure autorégulation cérébrale, sur la base du monitorage multimodal (index de "
         "réactivité pressionnelle PRx). PIC entre 20 et 25 mmHg généralement retenue comme "
         "critère de gravité ; réflexion thérapeutique dès que la PIC dépasse 20 mmHg.", "2+"),
        ("R7.2", "En l'absence de monitorage multimodal, cibler probablement une <b>PPC entre "
         "60 et 70 mmHg</b> (PPC = PAM − PIC, PAM mesurée au niveau du tragus). Une PPC &gt; "
         "70 mmHg systématique n'est pas recommandée (5× plus de détresses respiratoires, sans "
         "bénéfice neurologique) ; une PPC spontanément &gt; 90 mmHg est associée à un moins bon "
         "devenir (majoration de l'œdème vasogénique).", "2+"),
        ("R7.3", "Administrer du <b>mannitol 20 %</b> ou du <b>sérum salé hypertonique</b> "
         "(250 mosmol) en 15-20 min en traitement d'urgence d'une HTIC sévère ou de signes "
         "d'engagement, après contrôle des agressions cérébrales secondaires — efficacité "
         "comparable à dose équi-osmotique ; effet maximal 10-15 min, durée théorique 2-4h.", "1+"),
        ("R7.4", "Ne pas faire probablement d'<b>hypocapnie</b> comme traitement d'une HTIC "
         "(hyperventilation prolongée non recommandée sans monitorage de l'oxygénation "
         "cérébrale pour vérifier l'absence d'hypoxie induite) — objectif de normocapnie "
         "recherché.", "2-"),
        ("R7.5", "Ne pas administrer probablement d'<b>albumine à 4 %</b> comme soluté de "
         "remplissage chez le TC grave — étude SAFE : surmortalité chez les TC graves réanimés "
         "à l'albumine (24,5 % vs 15,1 % au NaCl 0,9 %).", "2-"),
    ]))
    story.append(Spacer(1, 3 * mm))

    story.append(section_bar("8 — Stratégie de prise en charge du polytraumatisé avec TC grave", color=RED))
    story.append(Spacer(1, 2 * mm))
    story.append(reco_table([
        ("R8.1", "En cas de polytraumatisme associé, privilégier la <b>stabilisation "
         "hémodynamique et respiratoire</b> avant la TDM corps entier injectée — incidence des "
         "lésions neurochirurgicales faible comparée aux lésions nécessitant une chirurgie "
         "d'hémostase (2,5 % vs 21 %). TDM cérébrale obligatoire dès stabilisation, intégrée à "
         "la TDM corps entier.", "AE"),
        ("R8.2", "En dehors de l'urgence vitale immédiate, ne pas réaliser de chirurgie à "
         "risque hémorragique dans un contexte d'HTIC (aggravation des lésions cérébrales, "
         "risque de SDRA/défaillance multiviscérale) — les gestes orthopédiques peu "
         "hémorragiques restent réalisables précocement (&lt; 24h) si HTIC absente.", "AE"),
        ("R8.3", "Mettre en place ou poursuivre probablement le <b>monitorage intracérébral</b> "
         "pendant la procédure chirurgicale — une étude retrouve 82 % de mortalité en cas "
         "d'hypotension peropératoire (PAS &lt; 90 mmHg) vs 32 % sans hypotension.", "2+"),
    ]))
    return story


def _section_champ9_11_sources():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("9 — Détection et traitement préventif des crises épileptiques", color=RED))
    story.append(Spacer(1, 2 * mm))
    story.append(reco_table([
        ("R9.1", "Chez l'adulte, ne pas administrer probablement de médicament antiépileptique "
         "en <b>prévention primaire</b> systématique de l'épilepsie post-traumatique (incidence "
         "clinique 1,5-5 % quel que soit le traitement, aucun bénéfice net démontré sur 11 "
         "essais). Peut être envisagée en cas de facteur de risque (contusion, hématome "
         "sous-dural aigu, embarrure, fracture du crâne, PC/amnésie &gt; 24h, âge &gt; 65 ans, "
         "craniectomie) : préférer alors le <b>lévétiracétam</b> à la phénytoïne (moins "
         "d'effets secondaires).", "2-"),
    ]))
    story.append(Spacer(1, 3 * mm))

    story.append(section_bar("10 — Homéostasie biologique (osmolarité, glycémie, axe cortico-surrénalien)",
                              color=RED))
    story.append(Spacer(1, 2 * mm))
    story.append(reco_table([
        ("R10.1", "Ne pas induire probablement une <b>hypernatrémie prolongée</b> pour "
         "contrôler la PIC — pas d'étude randomisée validant cette stratégie chez l'adulte ; "
         "risque de rebond de PIC à la correction, d'aggravation des contusions si "
         "barrière hémato-encéphalique lésée, d'hyperchlorémie délétère.", "2-"),
        ("R10.2", "<b>Ne pas administrer de glucocorticoïdes à forte dose</b> après un TC "
         "grave — l'étude CRASH (&gt; 10 000 patients) a montré une surmortalité importante "
         "dans le groupe traité.", "1-"),
        ("R10.3", "Surveiller étroitement la glycémie et réaliser un contrôle glycémique "
         "ciblant <b>8-11 mM/L (1,4-2 g/L)</b> chez le TC grave, adulte et enfant — "
         "l'hyperglycémie &gt; 2 g/L majore la mortalité et la morbidité neurologique ; le "
         "contrôle « strict » &lt; 6-7 mM n'apporte aucun bénéfice et expose à "
         "l'hypoglycémie et à la crise énergétique cérébrale (microdialyse).", "1+"),
    ]))
    story.append(Spacer(1, 3 * mm))

    story.append(section_bar("11 — Particularités du traumatisme crânien grave chez l'enfant", color=RED))
    story.append(Spacer(1, 2 * mm))
    cw = PAGE_W - 2 * MARGIN
    story.append(reco_table([
        ("R11.1", "Mesurer probablement la <b>PIC</b> après TC grave de l'enfant, y compris "
         "chez le nourrisson et en cas de traumatisme crânien infligé — le TC infligé est une "
         "étiologie prépondérante chez le nourrisson (&lt; 2 ans), à risque élevé d'HTIC et de "
         "pronostic péjoratif ; pas de surrisque de complications du monitorage démontré dans "
         "ce sous-groupe.", "2+"),
        ("R11.2", "Adapter probablement les <b>seuils minimaux de PPC</b> selon l'âge : "
         "40 mmHg pour 0-5 ans, 50 mmHg pour 5-11 ans, 50-60 mmHg au-delà de 11 ans. Seuil "
         "de traitement de la PIC généralement 20 mmHg (envisager un seuil plus bas dans les "
         "tranches d'âge les plus jeunes selon des données encore limitées).", "2+"),
        ("R11.3", "Prendre en charge l'enfant TC grave dans un <b>Trauma Center pédiatrique</b>, "
         "ou à défaut un Trauma Center adulte avec compétences pédiatriques — réduit la "
         "morbi-mortalité (nombreuses études, niveaux de preuve faible à modéré mais effectifs "
         "cumulés importants).", "1+"),
    ]))
    story.append(Spacer(1, 4 * mm))

    story.append(section_bar("Contrôle ciblé de la température (CCT) — renvoi", color=GREY))
    story.append(Spacer(1, 2 * mm))
    story.append(info_panel(P(
        "Cette RFE consacre un champ supplémentaire (R12.1-R12.6) au CCT après traumatisme "
        "crânien, <b>explicitement présenté par la source elle-même comme une « retranscription "
        "partielle » de la RFE 2016 SFAR/SRLF « Contrôle ciblé de la température en "
        "réanimation »</b> — ces 6 recommandations sont déjà intégralement disponibles dans la "
        "fiche dédiée <b>« Contrôle ciblé de la température »</b> de ce corpus (mêmes énoncés, "
        "mêmes grades, vérifié ligne à ligne) et ne sont pas redupliquées ici. Pour mémoire, les "
        "seuils : CCT 35-37 °C pour prévenir l'HTIC et améliorer la survie (grade 2+) ; CCT "
        "34-35 °C si HTIC réfractaire à un traitement médical bien conduit (grade 2+) ; durée/"
        "profondeur à adapter à l'HTIC (avis d'experts) ; chez l'enfant, CCT visant la "
        "normothermie (avis d'experts) — <b>pas d'hypothermie thérapeutique (32-34 °C) chez "
        "l'enfant</b> (grade 1-, aucun bénéfice démontré sur le pronostic ni le contrôle de "
        "l'HTIC).", S_BODY_SM), bg=BG_PANEL, border=GREY))
    story.append(Spacer(1, 4 * mm))

    story.append(section_bar("Sources et traçabilité", color=GREY))
    story.append(Spacer(1, 2 * mm))
    story.append(P(
        "<b>Document source :</b> « Prise en charge des traumatisés crâniens graves à la phase "
        "précoce (24 premières heures) » — Recommandations formalisées d'experts (actualisation), "
        "Société française d'anesthésie et de réanimation (Sfar), en collaboration avec l'Anarlf, "
        "la SFMU, la SFNC, le GFRUP et l'Adarpef. Coordonnateurs d'experts : Thomas Geeraerts "
        "(CHU Toulouse), Jean-François Payen (CHU Grenoble-Alpes). Anesth Reanim. "
        "2016;2:431-453. Texte validé par le Conseil d'administration de la Sfar le 21/09/2016.",
        S_SOURCE))
    story.append(Spacer(1, 2 * mm))
    story.append(P(
        "<b>Méthodologie :</b> GRADE (Grade of Recommendation Assessment, Development and "
        "Evaluation) — recherche bibliographique PubMed/Cochrane depuis 1998, niveau de preuve "
        "par critère de jugement, cotation collective GRADE Grid (2 tours). 32 recommandations "
        "formalisées, toutes avec accord FORT (10 grade 1, 18 grade 2, 4 avis d'experts) — "
        "recompté un pour un contre la synthèse de la source, voir disclosure méthodologique "
        "en page 1.", S_SOURCE))
    story.append(Spacer(1, 2 * mm))
    story.append(P(
        "<b>Couverture :</b> cette fiche reprend l'intégralité des 11 champs cliniques propres à "
        "cette RFE (gravité initiale, prise en charge préhospitalière, imagerie, indications "
        "neurochirurgicales, sédation/analgésie, monitorage cérébral, HTIC médicale, "
        "polytraumatisé, épilepsie, homéostasie biologique, particularités enfant) = 32/32 "
        "recommandations. Le champ 12 (contrôle ciblé de la température), explicitement "
        "retranscrit par la source elle-même depuis une autre RFE, renvoie à la fiche dédiée de "
        "ce corpus plutôt que d'être redupliqué (voir encadré ci-dessus). L'argumentaire complet "
        "de chaque recommandation (revue de littérature détaillée, références [1]-[302]) n'est "
        "pas reproduit — condensé en un rationnel clinique et les seuils numériques "
        "actionnables ; se référer au texte intégral pour l'argumentaire complet.", S_SOURCE))
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Avertissement — document de 2016 :</b> ce document est une fiche de synthèse "
        "indépendante, produite pour un usage d'aide-mémoire. Elle reprend l'intégralité des "
        "32 recommandations propres à cette RFE, mais ne remplace pas le texte intégral "
        "(argumentaire complet, 302 références bibliographiques) et n'est ni éditée ni validée "
        "par la SFAR. Cette actualisation ne présente que les évolutions par rapport aux "
        "recommandations françaises de 1998 (toujours en grande partie valables) : se référer "
        "en complément à ces dernières et à un avis neuro-réanimatoire spécialisé en cas de "
        "doute.", S_BODY_SM), bg=BG_PANEL, border=GREY))
    return story


SECTIONS = [
    ("Gravité initiale & prise en charge préhospitalière", _section_intro_champ1_2),
    ("Imagerie, neurochirurgie, sédation & monitorage", _section_champ3_6),
    ("HTIC médicale & polytraumatisé", _section_champ7_8),
    ("Épilepsie, homéostasie, enfant & sources", _section_champ9_11_sources),
]

def _make_doc(path=None):
    return SimpleDocTemplate(path or OUT, pagesize=A4,
                              leftMargin=MARGIN, rightMargin=MARGIN,
                              topMargin=32 * mm, bottomMargin=16 * mm,
                              title="SFAR 2016 - Traumatisme cranien grave phase precoce",
                              author="Synthèse indépendante (source SFAR)")

def _silent_page(canvas, doc_):
    pass

def _build_upto(section_fns):
    # Forcing a PageBreak before every top-level section left pages 3 and 5
    # underfull (~55% and ~15%). Letting content flow continuously (no forced
    # break) lets the next section climb onto that remaining whitespace
    # instead - same fix already validated on fiche_avc_precoce.py.
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
