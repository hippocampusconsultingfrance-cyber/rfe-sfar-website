# -*- coding: utf-8 -*-
"""
Fiche de synthese - Conference de consensus HAS/SAMU de France/Societe francophone
de medecine d'urgence/Societe francaise de cardiologie (23/11/2006, texte des
recommandations version courte, publie fevrier/mai 2007) : "Prise en charge de
l'infarctus du myocarde a la phase aigue en dehors des services de cardiologie".
Source : sources/infarctus_myocarde.pdf (24 pages), sources/infarctus_myocarde.txt
(texte extrait integralement, 876 lignes). Pas de tampon d'obsolescence detecte a
la lecture integrale (page de titre + sommaire + avertissement standard HAS, pas
d'avis de retrait) ; library_final.json marque ce document "en vigueur".

METHODOLOGIE - grades HAS A/B/C (etudes therapeutiques), PAS GRADE 1+/2+ :
Grade A = preuve scientifique etablie (niveau 1) ; Grade B = presomption
scientifique (niveau 2) ; Grade C = faible niveau de preuve (niveau 3-4). En
l'absence de precision, la recommandation repose sur un consensus du jury (aucun
grade impose). VERIFIE PAR grep -n "grade [abc]" CONTRE LE TEXTE SOURCE EXTRAIT
(sources/infarctus_myocarde.txt) : 11 occurrences explicites de "(grade X)" dans
le corps du texte (hors les 3 mentions de l'Annexe 1 qui ne font que DEFINIR
l'echelle de gradation, non compte ici) - 3x grade A (aspirine l.241, clopidogrel
l.243, insuline/GIK l.288), 7x grade B (enoxaparine vs HNF en fibrinolyse l.248 ;
sujet age - stratégie identique au sujet jeune l.325 ET, SEPAREMENT, HNF
preferee aux HBPM chez le >75 ans l.329 - DEUX tags "(grade B)" distincts dans
le meme paragraphe source, verifie ligne par ligne, pas un seul partage ; sujet
diabetique l.371 ; tachycardies - un seul tag couvrant la liste a puces qui suit
immediatement dans le texte source l.413 ; choc cardiogenique - desobstruction
coronaire precoce l.520 ET, SEPAREMENT, CPBIA l.527 - deux tags distincts) ; 1x
grade C (derives nitres l.250). Chaque occurrence est reproduite individuellement
a l'endroit exact du texte qu'elle qualifie (aucun regroupement invente). Tous
les autres enonces (majorite du texte : algorithmes 1-4, filieres, bradycardies,
AC, transferts interhospitaliers) ne portent aucun grade dans la source -
retranscrits avec un tiret "-" plutot qu'un grade invente.

PERIMETRE - integralite des 5 questions du texte court + l'echelle de gradation
(Annexe 1). Les sections "Methode Conference de consensus", "Participants" et
"Fiche descriptive" (pages 13-19, composition des comites/jury/groupe
bibliographique, sans contenu clinique) ne sont pas retranscrites - couverture
clinique complete verifiee par relecture integrale du texte extrait.

ALGORITHMES - 4 algorithmes decisionnels dans le corps du texte (pages 3, 6, 8,
10 de la source), tous avec couche texte extractible mais mise en page en
losanges/boites reliees par des fleches non lineaire pour le texte brut. Rendus
visuellement a 150dpi et verifies un par un (pages PDF 5, 8, 10, 12) avant
transcription. Restructures ici en tableaux de decision (colonnes = variables
de branchement, lignes = issues), sur le meme principe de reconstruction
disclose deja utilise dans ce corpus pour d'autres figures non lineaires (ex.
Figure 1 de sepsis_hemodynamique, algorithme de eclsa/tih) : integralite du
contenu conservee (toutes les branches, tous les seuils numeriques, toutes les
conduites a tenir), sans pretention a une reproduction pixel-exacte des
boites/fleches d'origine.

_count_pages() : pattern copie de fiche_transfusion_plasma.py / fiche_aap_programmee.py
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
GRADE_COLORS["—"] = (GREY_LIGHT, INK)

OUT = "/home/user/rfe-sfar-website/output/Fiche_HAS_SAMU_SFMU_SFC_Infarctus_Myocarde_Phase_Aigue_2006.pdf"

SOURCE_TXT = ("Source : HAS / SAMU de France / Société francophone de médecine d'urgence / Société "
              "française de cardiologie — Conférence de consensus « Prise en charge de l'infarctus du "
              "myocarde à la phase aiguë en dehors des services de cardiologie » (23/11/2006, publiée "
              "2007). Fiche de synthèse non officielle : se référer au texte intégral.")

def P(txt, style=S_CELL):
    return Paragraph(txt, style)

def chip(label, **kw):
    return grade_chip(label, **kw)

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

def grade_note(txt):
    return P(txt, S_NOTE)

TOTAL_PAGES = {"n": 7}

def on_page(canvas, doc, page_title):
    header_band(canvas, doc, "HAS / SAMU DE FRANCE / SFMU / SFC — CDC 2006 — FICHE DE SYNTHÈSE",
                "Infarctus du myocarde — phase aiguë hors cardiologie",
                page_title, icon_fn=lambda c, x, y: icon_drop(c, x, y, 13 * mm), color=RED)
    footer_band(canvas, doc, SOURCE_TXT, f"Page {doc.page} / {TOTAL_PAGES['n']}")

# ---------------------------------------------------------------------------
def _section_intro_q1():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Champ :</b> prise en charge de l'infarctus du myocarde (IDM) à la phase aiguë, "
        "<b>en dehors des services de cardiologie</b> — tout professionnel de santé amené à "
        "prendre en charge un IDM aigu hors cardiologie, en particulier les urgentistes "
        "(SAMU/SMUR, médecins libéraux, sapeurs-pompiers, SOS Médecins, services d'urgences et "
        "de soins non cardiologiques). Conférence de consensus HAS, 23 novembre 2006, promue par "
        "SAMU de France, la Société francophone de médecine d'urgence et la Société française de "
        "cardiologie, avec le partenariat méthodologique de la HAS ; texte court publié en 2007. "
        "<b>5 questions</b> : critères décisionnels de désobstruction coronaire, stratégies de "
        "reperfusion et traitements adjuvants du SCA ST+, filières de prise en charge, situations "
        "particulières, complications initiales.", S_BODY), bg=BG_PANEL, border=RED))
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Méthodologie — grades HAS A/B/C (études thérapeutiques), à la différence du GRADE "
        "1+/2+ utilisé ailleurs dans ce corpus :</b> Grade A = preuve scientifique établie "
        "(essais randomisés de forte puissance/méta-analyses, niveau 1) ; Grade B = présomption "
        "scientifique (essais randomisés de faible puissance/études comparatives non "
        "randomisées, niveau 2) ; Grade C = faible niveau de preuve (études de cohorte/cas-"
        "témoins/rétrospectives, niveaux 3-4). <b>En l'absence de précision, la recommandation "
        "repose sur un consensus du jury</b> — c'est le cas de la grande majorité des énoncés de "
        "ce texte, y compris les 4 algorithmes décisionnels : reproduits ici avec « — » dans la "
        "colonne Grade plutôt qu'un grade inventé. 11 mentions explicites de grade figurent dans "
        "le corps du texte (3×A, 7×B, 1×C), chacune reproduite individuellement à l'endroit exact "
        "qu'elle qualifie — y compris les 2 tags « (grade B) » distincts du paragraphe « sujet "
        "âgé » et les 2 tags distincts du paragraphe « choc cardiogénique ».", S_BODY_SM),
        bg=BG_PANEL, border=AMBER))
    story.append(Spacer(1, 3 * mm))

    story.append(section_bar("Question 1 — Critères décisionnels de désobstruction coronaire", color=RED))
    story.append(Spacer(1, 2 * mm))
    story.append(P(
        "La décision de prescription d'une désobstruction coronaire pour un IDM aigu repose sur "
        "une démarche de type bayésienne : l'évaluation clinique établit une probabilité "
        "initiale, réévaluée par la lecture de l'ECG, permettant de choisir entre débuter la "
        "désobstruction, poursuivre par le dosage de troponines, ou une autre stratégie.",
        S_BODY_SM))
    story.append(Spacer(1, 2 * mm))
    cw = PAGE_W - 2 * MARGIN
    story.append(simple_table(
        ["Probabilité clinique de SCA", "ECG contributif", "Troponines", "Conduite"],
        [
            ["Forte", "Oui", "—", "Désobstruction urgente"],
            ["Forte", "Non", "Positives", "Désobstruction urgente"],
            ["Forte", "Non", "Négatives", "Pas de stratégie invasive (suivi médical, "
             "évaluation secondaire)"],
            ["Faible", "Oui", "—", "Stratégie invasive différée (24-48 h)"],
            ["Faible", "Non", "—", "Pas de stratégie invasive (suivi médical, "
             "évaluation secondaire)"],
        ],
        [cw * 0.20, cw * 0.16, cw * 0.16, cw * 0.48]))
    story.append(Spacer(1, 1 * mm))
    story.append(P("<i>Algorithme 1 de la source, restructuré en tableau de décision (voir "
                    "disclosure méthodologique en tête de fiche).</i>", S_NOTE))
    return story

def _section_q2():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("Question 2 — Reperfusion et traitements adjuvants du SCA ST+", color=RED))
    story.append(Spacer(1, 2 * mm))
    story.append(P(
        "<b>Délais :</b> la pierre angulaire de la stratégie de reperfusion du SCA ST+ est la "
        "réduction du temps écoulé depuis le début des symptômes jusqu'à la reperméabilisation "
        "coronarienne. Le <b>premier contact médical</b> est le moment de l'arrivée auprès du "
        "patient du médecin permettant l'ECG et la confirmation du diagnostic. Pour la prise en "
        "charge hors cardiologie, le jury recommande de scinder le délai international "
        "premier contact médical-expansion du ballonnet (objectif global : 90 minutes) en 2 "
        "délais : le <b>délai porte à porte cardio</b> (premier contact médical → arrivée au "
        "service de cardiologie interventionnelle, seuil décisionnel recommandé : "
        "<b>45 minutes</b>) et le <b>délai porte cardio-ballon</b> (arrivée en cardiologie "
        "interventionnelle → expansion du ballonnet).", S_BODY_SM))
    story.append(Spacer(1, 2 * mm))
    story.append(P(
        "<b>Stratégies de reperfusion :</b> angioplastie coronaire et fibrinolyse. L'angioplastie "
        "primaire est la technique la plus sûre et la plus efficace (réouverture de l'artère "
        "occluse dans ~90 % des cas contre ~60 % pour la fibrinolyse), mais nécessite un plateau "
        "technique. La fibrinolyse a l'avantage de sa simplicité et d'une réalisation possible en "
        "tous lieux ; son efficacité est optimale dans les 3 premières heures suivant le début "
        "des symptômes ; risque hémorragique intracérébral incontournable (0,5-1 %) malgré le "
        "respect strict des contre-indications. <b>Le jury recommande la ténectéplase</b> "
        "(produit fibrino-spécifique, bolus IV unique ~10 secondes, demi-vie courte, adaptable au "
        "poids, dose maximale 10 000 UI/50 mg) ; <b>la streptokinase n'est pas recommandée.</b>",
        S_BODY_SM))
    story.append(Spacer(1, 2 * mm))
    cw = PAGE_W - 2 * MARGIN
    story.append(simple_table(
        ["Délai porte à porte cardio", "Début des symptômes", "Stratégie initiale"],
        [
            ["< 45 min ET somme des 2 délais < 90 min", "< 3 h",
             "Choix fibrinolyse (TL) ou angioplastie primaire (APL), selon procédures locales "
             "écrites et évaluées ; CI à la TL → APL"],
            ["< 45 min ET somme des 2 délais < 90 min", "3-12 h",
             "Angioplastie primaire privilégiée ; CI à la TL → APL"],
            ["> 45 min, ou délai porte cardio-ballon non estimable", "< 3 h ou 3-12 h "
             "(stratégie identique)", "Fibrinolyse ; si échec fibrinolyse → angioplastie de "
             "sauvetage"],
        ],
        [cw * 0.30, cw * 0.22, cw * 0.48]))
    story.append(Spacer(1, 1 * mm))
    story.append(P("<i>Algorithme 2 de la source, restructuré en tableau de décision. Cette "
                    "stratégie justifie 3 recommandations du jury : il est impératif que "
                    "l'ensemble des structures d'urgences (SMUR et accueil des urgences) dispose "
                    "des moyens de pratiquer une fibrinolyse (recommandation unanime du jury) ; "
                    "dans tous les cas, après fibrinolyse, le patient doit être dirigé vers un "
                    "centre disposant d'une salle de coronarographie diagnostique et "
                    "interventionnelle (SCDI) ; le jury recommande la mise en place de registres "
                    "d'évaluation de cette stratégie, destinés à la faire évoluer.</i>", S_NOTE))
    story.append(Spacer(1, 3 * mm))

    story.append(section_bar("Traitements adjuvants", color=TEAL_DARK))
    story.append(Spacer(1, 2 * mm))
    story.append(simple_table(
        ["Traitement", "Recommandation", "Grade"],
        [
            ["Acide acétylsalicylique", "Bénéfice largement démontré dans le traitement des SCA.",
             chip("A", width=16*mm)],
            ["Clopidogrel", "Recommandé à la phase précoce d'un SCA ST+, en association avec "
             "l'aspirine ou seul si celle-ci est contre-indiquée.", chip("A", width=16*mm)],
            ["Antagonistes GPIIb/IIIa", "L'abciximab est utilisé en phase aiguë de SCA ST+ avant "
             "une angioplastie primaire.", chip("—", width=16*mm)],
            ["Anticoagulants", "En cas de fibrinolyse, l'énoxaparine est supérieure à l'HNF chez "
             "les patients de moins de 75 ans à fonction rénale normale. En cas d'angioplastie, "
             "l'HNF est le traitement de référence.", chip("B", width=16*mm)],
            ["Dérivés nitrés", "Non recommandés en dehors de l'OAP et éventuellement d'une "
             "poussée hypertensive.", chip("C", width=16*mm)],
            ["Oxygénothérapie", "Non systématique.", chip("—", width=16*mm)],
            ["Antalgiques", "Traitement de choix : morphine en titration IV.", chip("—", width=16*mm)],
            ["Bêtabloquants", "Administration non préconisée de façon systématique.", chip("—", width=16*mm)],
            ["IEC et antagonistes calciques", "Aucun argument ne permet de les recommander.", chip("—", width=16*mm)],
            ["Insuline", "Recommandée pour corriger une hyperglycémie en phase aiguë d'IDM ; "
             "la solution glucose-insuline-potassium (GIK) n'est pas recommandée.", chip("A", width=16*mm)],
        ],
        [cw * 0.22, cw * 0.62, cw * 0.16]))
    return story

def _section_q3():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("Question 3 — Filières de prise en charge", color=RED))
    story.append(Spacer(1, 2 * mm))
    story.append(P(
        "Compte tenu des pertes de chances induites par le retard diagnostique et thérapeutique, "
        "il faut insister sur la réalisation répétée de campagnes d'éducation du grand public et "
        "des professionnels de santé — objectif : « <b>prescrire le 15</b> ». L'appel (patient ou "
        "tiers) doit aboutir au <b>SAMU-Centre 15</b>, dont le médecin régulateur essaiera d'être "
        "mis directement en relation avec le patient puis déclenchera un effecteur destiné à "
        "amener le patient en SCDI opérationnelle (filière cardiologique). Le jury recommande que "
        "le médecin régulateur du SAMU soit le « <b>gardien du temps</b> » du déroulement de "
        "l'intervention, faisant le lien entre l'équipe d'intervention et l'équipe d'accueil.",
        S_BODY_SM))
    story.append(Spacer(1, 2 * mm))
    story.append(KeepTogether([
        P("<b>Algorithme 3 (source) — Filières de prise en charge d'une douleur thoracique "
          "suspecte d'IDM</b>", S_H2),
        Spacer(1, 2 * mm),
        Table([[
            P("<b>Points d'entrée</b> vers le SAMU-Centre 15 (avec conférence à 3 si besoin) : "
              "appel direct du patient/d'un tiers • association d'urgentistes • régulation "
              "libérale de la permanence des soins • service de soins (patient déjà hospitalisé) "
              "• médecin libéral", S_CELL),
        ]], colWidths=[PAGE_W - 2*MARGIN], style=TableStyle([
            ("BACKGROUND", (0,0), (-1,-1), BG_PANEL), ("BOX", (0,0), (-1,-1), 1, TEAL),
            ("TOPPADDING", (0,0), (-1,-1), 3*mm), ("BOTTOMPADDING", (0,0), (-1,-1), 3*mm),
            ("LEFTPADDING", (0,0), (-1,-1), 3.5*mm), ("RIGHTPADDING", (0,0), (-1,-1), 3.5*mm),
        ])),
    ]))
    story.append(Spacer(1, 1.5 * mm))
    story.append(KeepTogether([
        P("↓", pstyle("arrow_c", base=S_H2, alignment=1, fontSize=13)),
        Table([[
            P("<b>SAMU-Centre 15</b> déclenche un effecteur : une unité mobile hospitalière (UMH) "
              "et/ou, à défaut, un médecin correspondant SAMU / urgentiste libéral conventionné / "
              "médecin pompier + ECG / médecin libéral (accord préalable) + ECG — dans tous les cas "
              "avec <b>défibrillateur semi-automatique (DSA) systématique</b>, ± fibrinolyse selon "
              "l'algorithme 2.", S_CELL),
        ]], colWidths=[PAGE_W - 2*MARGIN], style=TableStyle([
            ("BACKGROUND", (0,0), (-1,-1), _c(219, 230, 242)), ("BOX", (0,0), (-1,-1), 1, NAVY),
            ("TOPPADDING", (0,0), (-1,-1), 3*mm), ("BOTTOMPADDING", (0,0), (-1,-1), 3*mm),
            ("LEFTPADDING", (0,0), (-1,-1), 3.5*mm), ("RIGHTPADDING", (0,0), (-1,-1), 3.5*mm),
        ])),
    ]))
    story.append(Spacer(1, 1.5 * mm))
    story.append(KeepTogether([
        P("↓", pstyle("arrow_c2", base=S_H2, alignment=1, fontSize=13)),
        Table([[
            P("<b>SCDI opérationnelle</b> — le patient y accède directement (vient directement / "
              "urgences hôpital), via une USI (si déjà hospitalisé), ou est réorienté secondairement "
              "en <b>USIC</b> depuis la SCDI.", S_CELL),
        ]], colWidths=[PAGE_W - 2*MARGIN], style=TableStyle([
            ("BACKGROUND", (0,0), (-1,-1), _c(197, 224, 240)), ("BOX", (0,0), (-1,-1), 1.4, TEAL_DARK),
            ("TOPPADDING", (0,0), (-1,-1), 3*mm), ("BOTTOMPADDING", (0,0), (-1,-1), 3*mm),
            ("LEFTPADDING", (0,0), (-1,-1), 3.5*mm), ("RIGHTPADDING", (0,0), (-1,-1), 3.5*mm),
        ])),
    ]))
    story.append(Spacer(1, 2 * mm))
    story.append(P(
        "<b>Moyens engagés minimaux</b> en dehors des UMH : présence d'un médecin avec ECG ; un "
        "vecteur de transport avec au moins DSA et O2. Dans certaines situations d'exception "
        "(isolement, défaut d'accessibilité durable et prévisible aux secours médicalisés et aux "
        "moyens d'évacuation rapides), le jury recommande la rédaction préalable de protocoles "
        "décisionnels.", S_BODY_SM))
    return story

def _section_q4_q5():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("Question 4 — Situations particulières", color=RED))
    story.append(Spacer(1, 2 * mm))
    story.append(P(
        "<b>Personnes âgées :</b> la stratégie thérapeutique globale ne doit pas différer de "
        "celle des sujets jeunes malgré un risque de complications plus élevé (grade B), à "
        "l'exception du choc cardiogénique, où le recours à la reperfusion n'est pas systématique "
        "mais discuté cas par cas. <b>L'HNF est préférée aux HBPM chez le sujet de plus de 75 ans</b> "
        "(grade B).", S_BODY_SM))
    story.append(Spacer(1, 2 * mm))
    story.append(P(
        "<b>Personnes diabétiques :</b> la stratégie globale ne diffère pas de celle des sujets "
        "non diabétiques (grade B). Déterminer la glycémie capillaire au plus tôt, y compris en "
        "préhospitalier ; réduction précoce de l'hyperglycémie par l'insuline et réduction des "
        "apports glucidiques à la phase aiguë.", S_BODY_SM))
    story.append(Spacer(1, 2 * mm))
    story.append(P(
        "<b>IDM survenant dans un service de soins non cardiologiques :</b> prise en charge "
        "organisée par des protocoles locaux pour une réponse dans les plus brefs délais. En cas "
        "de décision de reperfusion en urgence, les patients dans des sites avec plateau de "
        "cardiologie interventionnelle accessible doivent avoir une angioplastie primaire ; dans "
        "les autres cas, la stratégie de reperfusion ne diffère pas de celle proposée en dehors "
        "des structures de soins.", S_BODY_SM))
    story.append(Spacer(1, 2 * mm))
    story.append(P(
        "<b>IDM périopératoires :</b> prévention fondée sur l'analyse du segment ST et la "
        "correction rapide de toute anomalie hémodynamique (hypotension, hypertension, "
        "tachycardie) ou métabolique importante (anémie, hypothermie). Détection par analyse ECG "
        "quotidienne et dosages répétés de troponine postopératoire ; prise en charge graduée "
        "selon la modification du segment ST et la cinétique de la troponine. Le recours "
        "systématique en urgence à une coronarographie n'est licite qu'en cas de sus-décalage "
        "du segment ST.", S_BODY_SM))
    story.append(Spacer(1, 3 * mm))

    story.append(section_bar("Question 5 — Prise en charge des complications initiales", color=RED))
    story.append(Spacer(1, 2 * mm))
    story.append(P(
        "Le traitement spécifique des complications doit être associé à la correction des "
        "facteurs favorisants, notamment les dyskaliémies et l'hypoxie.", S_BODY_SM))
    story.append(Spacer(1, 2 * mm))
    story.append(P("<b>Bradycardies</b> — options thérapeutiques :", S_CELL_B))
    story.append(P(
        "• surveillance électrocardioscopique seule, si bien tolérée et sans risque d'asystolie ;<br/>"
        "• entraînement électrosystolique externe, indiqué devant toute bradycardie symptomatique "
        "avec intolérance hémodynamique (habituellement liée à un BAV de haut degré), en cas de "
        "risque d'asystolie, ou si l'atropine est inefficace ;<br/>"
        "• traitement pharmacologique : en l'absence de cause réversible, <b>l'atropine</b> est la "
        "thérapeutique de choix devant toute bradycardie symptomatique aiguë. "
        "<b>L'isoprénaline n'est pas recommandée</b> et <b>l'adrénaline ne doit être utilisée "
        "qu'en dernier recours.</b>", S_BODY_SM))
    story.append(Spacer(1, 3 * mm))

    story.append(P("<b>Tachycardies</b> (fréquence &gt; 100 bpm, hors défaillance vitale et "
                    "tachycardie bien tolérée) — plusieurs options thérapeutiques", S_CELL_B))
    story.append(P(
        "peuvent être envisagées <b>(grade B)</b> : le patient en arrêt circulatoire nécessite un "
        "choc électrique externe (CEE) immédiat, asynchrone, sans sédation, et une RCP "
        "médicalisée ; le patient en défaillance hémodynamique (hors tachycardie sinusale) "
        "nécessite un CEE immédiat, de préférence synchrone ; le patient conscient sans signes "
        "d'intolérance clinique : les TV soutenues/polymorphes justifient amiodarone et/ou CEE "
        "après sédation, sinon abstention thérapeutique avec surveillance seule. Pour le patient "
        "conscient avec signes d'intolérance (douleur thoracique ou OAP), la stratégie détaillée "
        "figure ci-dessous.", S_BODY_SM))
    story.append(Spacer(1, 2 * mm))
    story.append(P(
        "<b>Mesures initiales, tous les patients :</b> oxygène en fonction de la SpO<sub>2</sub>, "
        "monitoring ECG, surveillance continue de la pression artérielle et de la SpO<sub>2</sub>, "
        "accès veineux.", S_NOTE))
    story.append(Spacer(1, 2 * mm))
    cw = PAGE_W - 2 * MARGIN
    story.append(KeepTogether([
        simple_table(
            ["Situation (patient conscient, signes d'intolérance : OAP/douleur thoracique)",
             "Traitement de 1ère intention", "Si échec"],
            [
                ["Arrêt circulatoire", "RCP médicalisée + CEE asynchrone", "—"],
                ["État de choc cardiogénique / OAP massif",
                 "Sédation si conscient + CEE synchrone si possible + gestes de réanimation", "—"],
                ["Pas d'autres signes d'intolérance", "Surveillance clinique et paraclinique (scope)", "—"],
                ["Rythme irrégulier, QRS fin < 0,12 s (FA rapide)",
                 "Amiodarone IV 300 mg/20-60 min puis 900 mg/24 h",
                 "Esmolol IV (500 µg/kg puis 50-200 µg/kg/4 min) ou aténolol (5 mg IV puis 75 mg PO)"],
                ["Rythme irrégulier, QRS large > 0,12 s (TV polymorphe)",
                 "Amiodarone IV (même schéma)", "CEE synchrone"],
                ["Rythme régulier, QRS fin < 0,12 s (tachycardie sinusale)",
                 "Surveillance attentive", "—"],
                ["Rythme régulier, QRS large > 0,12 s (TV)",
                 "Amiodarone IV (même schéma)", "CEE synchrone"],
            ],
            [cw * 0.34, cw * 0.36, cw * 0.30]),
        Spacer(1, 1 * mm),
        P("<i>Algorithme 4 de la source, restructuré en tableau de décision. En cas de "
          "doute sur le mécanisme (rythme irrégulier QRS large [TV polymorphe] : évoquer de "
          "principe une FA avec conduction aberrante, se reporter à la conduite de la FA rapide ; "
          "rythme régulier QRS fin [tachycardie sinusale] : évoquer de principe un flutter "
          "auriculaire, se reporter à la conduite de la FA rapide ; rythme régulier QRS large "
          "[TV] : évoquer de principe une TSV avec conduction aberrante, se reporter à la "
          "conduite de la tachycardie sinusale).</i>", S_NOTE),
    ]))
    return story

def _section_complications_sources():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(P("<b>Arrêt circulatoire (AC)</b>", S_CELL_B))
    story.append(P(
        "Le contexte ischémique de l'AC ne modifie pas les recommandations générales de la RCP. "
        "Si l'AC survient sur un IDM déjà diagnostiqué et qu'une RACS est obtenue, la stratégie de "
        "reperfusion repose sur l'accès rapide à une SCDI opérationnelle (pas de délai maximal "
        "fourni). Le massage cardiaque externe ne contre-indique pas la fibrinolyse ; chez un "
        "patient fibrinolysé, la survenue d'un AC peut être un signe de reperfusion coronaire — "
        "une réanimation prolongée (60 à 90 minutes après l'injection du fibrinolytique) est "
        "justifiée pour favoriser son efficacité. En l'absence de RACS, il n'y a pas d'argument "
        "scientifique pour recommander ou interdire la fibrinolyse. Si l'AC constitue la première "
        "manifestation de l'IDM, il n'y a pas d'argument pour recommander une fibrinolyse.",
        S_BODY_SM))
    story.append(Spacer(1, 3 * mm))
    story.append(P("<b>Choc cardiogénique</b>", S_CELL_B))
    story.append(P(
        "Stratégie reposant sur le traitement étiologique associé au traitement symptomatique : "
        "<b>désobstruction coronaire précoce, préférentiellement par angioplastie (grade B)</b>, "
        "associée à des mesures de diminution de la consommation myocardique en oxygène "
        "(analgésie, oxygène). Restauration hémodynamique par remplissage vasculaire prudent (en "
        "l'absence de signes d'insuffisance ventriculaire gauche), avec si nécessaire "
        "catécholamines titrées (dobutamine en 1<sup>re</sup> intention, noradrénaline en "
        "2<sup>e</sup> intention). <b>La contre-pulsion par ballonnet intra-aortique (CPBIA) "
        "favorise la stabilisation initiale des patients en choc cardiogénique secondaire à un "
        "IDM (grade B).</b>", S_BODY_SM))
    story.append(Spacer(1, 3 * mm))
    story.append(P("<b>Transferts interhospitaliers des infarctus compliqués</b>", S_CELL_B))
    story.append(P(
        "Toujours des transports médicalisés par le SMUR, dont le premier objectif est de "
        "permettre au patient d'accéder à un niveau de soins supérieur tout en assurant sa "
        "sécurité. Chaque intervenant de la chaîne (médecin d'amont, médecin SMUR, médecin "
        "régulateur, médecin d'accueil) en a une part de responsabilité. Les équipes du SMUR "
        "doivent être formées aux techniques d'assistance circulatoire (CPBIA de plus en plus "
        "couramment utilisée, très rarement assistance circulatoire périphérique) ; l'équipe peut "
        "être complétée par un médecin maîtrisant ces techniques, dans le cadre d'un protocole en "
        "réseau impliquant tous les acteurs concernés.", S_BODY_SM))
    story.append(Spacer(1, 4 * mm))

    story.append(section_bar("Annexe 1 — Échelle de gradation HAS des recommandations", color=GREY))
    story.append(Spacer(1, 2 * mm))
    cw = PAGE_W - 2 * MARGIN
    story.append(simple_table(
        ["Grade", "Niveau de preuve scientifique fourni par la littérature"],
        [
            [chip("A", width=16*mm), "Preuve scientifique établie — essais comparatifs "
             "randomisés de forte puissance, méta-analyse d'essais comparatifs randomisés, "
             "analyse de décision basée sur des études bien menées (niveau de preuve 1)."],
            [chip("B", width=16*mm), "Présomption scientifique — essais comparatifs randomisés "
             "de faible puissance, études comparatives non randomisées bien menées, études de "
             "cohorte (niveau de preuve 2)."],
            [chip("C", width=16*mm), "Faible niveau de preuve — études cas-témoins, études "
             "comparatives comportant des biais importants, études rétrospectives, séries de cas "
             "(niveaux de preuve 3-4)."],
        ],
        [cw * 0.14, cw * 0.86]))
    story.append(Spacer(1, 1 * mm))
    story.append(P("En l'absence de précisions, les recommandations reposent sur un consensus "
                    "exprimé par le jury.", S_NOTE))
    story.append(Spacer(1, 4 * mm))

    story.append(section_bar("Sources et traçabilité", color=GREY))
    story.append(Spacer(1, 2 * mm))
    story.append(P(
        "<b>Document source :</b> « Prise en charge de l'infarctus du myocarde à la phase aiguë "
        "en dehors des services de cardiologie » — Conférence de consensus, 23 novembre 2006 "
        "(Paris, faculté de médecine Paris V), texte des recommandations (version courte), mise "
        "en ligne février 2007, publication mai 2007. Promoteurs : SAMU de France, Société "
        "francophone de médecine d'urgence, Société française de cardiologie ; copromoteurs : "
        "Afssaps, APNET, Bataillon des marins-pompiers de Marseille, Brigade de sapeurs-pompiers "
        "de Paris, SFAR, Société française de biologie clinique, Société française de médecine "
        "sapeur-pompier, SRLF, SOS Médecins France. Président du comité d'organisation : "
        "Pr Frédéric Adnet ; président du jury : Dr Jean-Louis Ducassé. Avec le partenariat "
        "méthodologique et le concours financier de la Haute Autorité de Santé (HAS).",
        S_SOURCE))
    story.append(Spacer(1, 2 * mm))
    story.append(P(
        "<b>Méthodologie :</b> grades HAS A/B/C (échelle de gradation des études thérapeutiques, "
        "Annexe 1 ci-dessus), méthode « Conférence de consensus » HAS — jury de non-experts, "
        "huis clos de 48h après séance publique. 11 mentions de grade explicite figurent dans "
        "le corps du texte (3×A, 7×B, 1×C) ; la quasi-totalité des énoncés (dont les 4 algorithmes "
        "décisionnels) reposent sur un consensus du jury sans grade associé (voir disclosure "
        "méthodologique en page 1).", S_SOURCE))
    story.append(Spacer(1, 2 * mm))
    story.append(P(
        "<b>Couverture :</b> cette fiche reprend l'intégralité des 5 questions du texte court "
        "(critères de désobstruction coronaire, stratégies de reperfusion et traitements "
        "adjuvants du SCA ST+, filières de prise en charge, situations particulières — sujet "
        "âgé/diabétique/service non cardiologique/périopératoire —, complications initiales — "
        "bradycardies/tachycardies/arrêt circulatoire/choc cardiogénique/transferts "
        "interhospitaliers), ainsi que l'échelle de gradation (Annexe 1) et les 4 algorithmes "
        "décisionnels (restructurés en tableaux de décision, voir disclosure). Les sections "
        "méthodologiques sans contenu clinique (méthode « Conférence de consensus », composition "
        "du comité d'organisation/jury/groupe bibliographique, fiche descriptive) ne sont pas "
        "retranscrites.", S_SOURCE))
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Avertissement — document de 2006/2007 :</b> ce document est une fiche de synthèse "
        "indépendante, produite pour un usage d'aide-mémoire. Elle reprend l'intégralité des "
        "recommandations et algorithmes du texte source, mais ne remplace pas le texte intégral "
        "(argumentaire complet, références bibliographiques) et n'est ni éditée ni validée par la "
        "HAS, SAMU de France, la Société francophone de médecine d'urgence ou la Société "
        "française de cardiologie. <b>Les stratégies de reperfusion et les traitements adjuvants "
        "du SCA ST+ ont évolué depuis 2006</b> (nouveaux antiplaquettaires P2Y12, protocoles de "
        "délais, recommandations ESC ultérieures) : se référer en complément aux recommandations "
        "plus récentes et à un avis cardiologique spécialisé en cas de doute.", S_BODY_SM),
        bg=BG_PANEL, border=GREY))
    return story

def _section_all_1():
    return _section_intro_q1() + [Spacer(1, 2*mm)] + _section_q2()

def _section_all_2():
    return _section_q3() + [Spacer(1, 2*mm)] + _section_q4_q5()

def _section_all_3():
    return _section_complications_sources()

SECTIONS = [
    ("Question 1-2 — Désobstruction, reperfusion & traitements adjuvants", _section_all_1),
    ("Question 3-5 — Filières, situations particulières & complications", _section_all_2),
    ("Annexe & sources", _section_all_3),
]

def _make_doc(path=None):
    return SimpleDocTemplate(path or OUT, pagesize=A4,
                              leftMargin=MARGIN, rightMargin=MARGIN,
                              topMargin=32 * mm, bottomMargin=16 * mm,
                              title="HAS/SAMU de France/SFMU/SFC 2006 - Infarctus du myocarde phase aigue",
                              author="Synthèse indépendante (source HAS)")

def _silent_page(canvas, doc_):
    pass

def _build_upto(section_fns):
    # Pages 2 and 4 were <60% full with a forced PageBreak before every
    # top-level section. TRIED: removing the break between Q1-2 and Q3-5 so
    # content flows continuously - this filled page 2 completely, but the
    # total page count stayed at 5 (not 4) and it just pushed the underfill
    # onto page 3/4 instead (and briefly caused the tachycardie table to
    # split awkwardly across the boundary before that was fixed with
    # KeepTogether). Per the pipeline note ("revert if it doesn't help - a
    # merge doesn't always reduce pages"), reverted to a forced PageBreak
    # before every section: predictable per-page structure, no orphaned
    # flowchart arrows, matches this corpus's established convention.
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

    final_story = _build_upto(fns)
    docf = _make_doc()
    docf.build(final_story, onFirstPage=on_page_final, onLaterPages=on_page_final)
    print("OK ->", OUT, f"({total_pages} pages)")

if __name__ == "__main__":
    build()
