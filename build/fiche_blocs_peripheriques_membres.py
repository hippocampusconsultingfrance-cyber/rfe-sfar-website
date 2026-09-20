# -*- coding: utf-8 -*-
"""
Fiche de synthese - Societe Francaise d'Anesthesie et de Reanimation (SFAR),
avec la Sofcot et la Sofmer. "Les blocs peripheriques des membres chez
l'adulte" - Recommandations pour la Pratique Clinique (RPC), presentees en
session publique le 22 septembre 2001 (43e congres SFAR), publiees Ann Fr
Anesth Reanim 22 (2003) 567-581. 15 pages, telecharge depuis sfar.org
(wp-content/uploads/2015/10/2_AFAR_Les-blocs-peripheriques-des-membres-chez-
l-adulte.pdf).

METHODOLOGIE : grille EBM a 5 niveaux, Grade A (>=2 etudes de niveau I),
Grade B (1 etude de niveau I), Grade C (etude(s) de niveau II), Grade D
(>=1 etude de niveau III), Grade E (etude(s) de niveau IV/V). "Lorsque les
recommandations relevent de l'avis des experts, ceci est mentionne dans le
texte" - transcrit ici comme "consensus professionnel" (chip CP), distinct
du Grade E (etudes de niveau IV/V, incluant des series de cas) qui reste une
categorie de PREUVE au sens de la grille, alors que CP designe une absence
totale d'etude et un avis d'experts pur. Cette distinction A/B/C/D/E vs CP
est celle du texte source lui-meme (pas une invention de cette fiche) - le
texte utilise a la fois "(E)" pour des enonces avec preuve de faible niveau
ET "(consensus professionnel)"/"(avis des experts)" pour des enonces sans
aucune etude, cote a cote dans les memes sections.

PERIMETRE ET CONDENSATION (regle de projet 2026-09-14, argumentaire minimal) :
document tres dense (14 questions, ~90 enonces individuels). Cette fiche
transcrit l'integralite du contenu ACTIONNABLE (quoi faire, quel grade) sous
forme de tableaux thematiques groupes par question/sous-question, mais
condense la prose contextuelle/physiopathologique non actionnable (ex. :
Q1's discussion du droit a l'information, Q13's rappels pharmacocinetiques
generaux) a une phrase de contexte quand necessaire. Le Tableau 1
(indications chirurgicales retenues, membre superieur) et le tableau des
doses maximales (Q13.6) sont reproduits integralement. **Aucune fusion de
grades differents sous un seul chip** : quand un paragraphe du texte source
regroupe plusieurs faits a grades differents, chaque fait est annote
individuellement "(Grade X)" dans le texte descriptif (pas de chip unique
pour le paragraphe) - safety net verifie par grep avant finalisation.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from style import *
GRADE_COLORS["A"] = (GREEN, WHITE)
GRADE_COLORS["B"] = (TEAL, WHITE)
GRADE_COLORS["C"] = (AMBER, WHITE)
GRADE_COLORS["D"] = (NAVY, WHITE)
GRADE_COLORS["E"] = (GREY, WHITE)
GRADE_COLORS["CP"] = (GREY, WHITE)
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.units import mm

OUT = "/home/user/rfe-sfar-website/output/Fiche_SFAR_Blocs_Peripheriques_Membres_2003.pdf"

SOURCE_TXT = ("Source : SFAR/Sofcot/Sofmer, « Les blocs périphériques des membres chez "
              "l'adulte », RPC, Ann Fr Anesth Réanim 22 (2003) 567-581. Fiche de synthèse "
              "non officielle : se référer au texte intégral.")

def P(txt, style=S_CELL):
    return Paragraph(txt, style)

def chip(label, **kw):
    return grade_chip(label, **kw)

CW_FULL = PAGE_W - 2 * MARGIN

def theme_table(rows, col_widths, head=("Thème", "Détail")):
    data = [[P(head[0], S_HEAD_W), P(head[1], S_HEAD_W)]]
    for theme, detail in rows:
        data.append([P(theme, S_CELL_B), P(detail, S_CELL)])
    t = Table(data, colWidths=col_widths, repeatRows=1)
    style_cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), NAVY), ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTNAME", (0, 0), (-1, 0), FONT_BOLD), ("FONTSIZE", (0, 0), (-1, 0), 8),
        ("VALIGN", (0, 0), (-1, -1), "TOP"), ("ALIGN", (0, 1), (0, -1), "LEFT"),
        ("GRID", (0, 0), (-1, -1), 0.5, GREY_LIGHT),
        ("TOPPADDING", (0, 0), (-1, -1), 3.4), ("BOTTOMPADDING", (0, 0), (-1, -1), 3.4),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            style_cmds.append(("BACKGROUND", (0, i), (-1, i), BG_PANEL))
    t.setStyle(TableStyle(style_cmds))
    return t

TCW = [40 * mm, CW_FULL - 40 * mm]

def bullets(items, style=S_BODY_SM):
    html = "&bull; " + "<br/>&bull; ".join(items)
    return P(html, style)

def legend_flowable():
    chip_w = 13.5 * mm
    content_w = CW_FULL
    row = Table([[chip("A", width=chip_w - 2 * mm), chip("B", width=chip_w - 2 * mm),
                  chip("C", width=chip_w - 2 * mm), chip("D", width=chip_w - 2 * mm),
                  chip("E", width=chip_w - 2 * mm), chip("CP", width=chip_w - 2 * mm),
                  P("<b>Grille EBM</b> — <b>A</b> : ≥2 études niveau I ; <b>B</b> : 1 étude "
                    "niveau I ; <b>C</b> : étude(s) niveau II ; <b>D</b> : ≥1 étude niveau "
                    "III ; <b>E</b> : étude(s) niveau IV/V ; <b>CP</b> : consensus "
                    "professionnel/avis d'experts (aucune étude).", S_BADGE_HEAD)]],
                colWidths=[chip_w]*6 + [content_w - 6 * chip_w])
    row.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                              ("LEFTPADDING", (0, 0), (-1, -1), 1),
                              ("RIGHTPADDING", (0, 0), (-1, -1), 1),
                              ("TOPPADDING", (0, 0), (-1, -1), 0),
                              ("BOTTOMPADDING", (0, 0), (-1, -1), 0)]))
    return row

TOTAL_PAGES = {"n": 8}

def on_page(canvas, doc, page_title):
    header_band(canvas, doc, "SFAR / SOFCOT / SOFMER — RPC, 22 SEPTEMBRE 2001",
                "Les blocs périphériques des membres chez l'adulte",
                page_title, icon_fn=lambda c, x, y: icon_pill(c, x, y, 13 * mm), color=TEAL_DARK)
    footer_band(canvas, doc, SOURCE_TXT, f"Page {doc.page} / {TOTAL_PAGES['n']}")

# ---------------------------------------------------------------------------
def _section_intro():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Résumé :</b> 14 questions couvrant l'information du patient, la préparation et "
        "la surveillance, l'anesthésie locorégionale intraveineuse (ALRIV), les techniques "
        "de repérage (neurostimulation), le matériel, les agents pharmacologiques, les "
        "recommandations par territoire (membre supérieur/inférieur) avec leurs indications "
        "chirurgicales, l'analgésie postopératoire, la conduite chez le patient sous "
        "anticoagulant ou porteur d'une pathologie neurologique, la gestion de l'échec, la "
        "toxicité systémique des anesthésiques locaux (AL) et les complications "
        "neurologiques.", S_BODY), bg=BG_PANEL, border=TEAL))
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("Méthodologie — grille EBM"))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "Grade A : au moins 2 études de niveau I (essais randomisés, faible risque α/β, "
        "puissance élevée 5-10 %). Grade B : 1 étude de niveau I. Grade C : étude(s) de "
        "niveau II (risque α élevé ou faible puissance). Grade D : au moins 1 étude de "
        "niveau III (non randomisée, contrôles contemporains). Grade E : étude(s) de niveau "
        "IV (non randomisée, contrôles non contemporains) ou V (séries de cas, avis "
        "d'experts). « Lorsque les recommandations relèvent de l'avis des experts, ceci est "
        "mentionné dans le texte » (citation du texte source) — chip <b>CP</b> (consensus "
        "professionnel) dans cette fiche, distinct du Grade E qui reste une catégorie de "
        "preuve.", S_BODY_SM))
    story.append(Spacer(1, 1.5 * mm))
    story.append(legend_flowable())
    return story

# ---------------------------------------------------------------------------
def _section_q1_q2():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Q1-2. Information du patient, préparation et surveillance"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(theme_table([
        ("Information du patient",
         "Droit du patient, pré-requis au consentement éclairé. Quand un choix AG/ALR "
         "existe, avantages/inconvénients/risques doivent être exposés ; le médecin doit "
         "se conformer à la préférence du patient si compatible avec l'intervention, sinon "
         "expliquer et consigner le désaccord au dossier. Information sur l'échec possible "
         "(recours à l'AG), le changement de technique et le risque de séquelles "
         "neurologiques ou d'accidents graves, même exceptionnels. Note écrite possible en "
         "complément de l'oral. Une tenue appropriée du dossier doit faire apparaître la "
         "démarche d'information (avant et après complication éventuelle)."),
        ("Consultation d'anesthésie",
         "Vérifie l'absence de contre-indication et met en place les substitutions "
         "nécessaires — notamment chez le patient sous anticoagulants chroniques, où le "
         "rapport risque d'arrêt / bénéfice du bloc doit être évalué (traitement "
         "substitutif de courte durée parfois proposé) (Grade E)."),
        ("Programme opératoire",
         "Organisé en tenant compte des anesthésies prévues (CP)."),
        ("Préparation préopératoire immédiate",
         "Prémédication sans particularité avant une ALR périphérique (Grade D). Jeûne "
         "selon les normes habituelles. Voie veineuse mise en place avant l'ALR. Attention "
         "au confort (réchauffement) et à l'intimité du patient (CP)."),
        ("Monitorage et lieu de réalisation",
         "Salle spécifique souhaitable à proximité du bloc opératoire (Grade E). "
         "Monitorage identique à celui d'une AG, effectif avant la réalisation du bloc, "
         "quel que soit le site (CP). Chariot de matériel dédié à l'ALR recommandé."),
        ("Sédation pour la réalisation du bloc",
         "Sédation légère uniquement, réactivité conservée aux stimulations verbales, "
         "patient coopérant. Benzodiazépines (et probablement propofol) évitent la "
         "mémorisation du geste (Grade B) ; rémifentanil évite la douleur liée au geste."),
        ("Sédation peropératoire",
         "Sédation légère uniquement, réactivité conservée (Grade C)."),
        ("Réalisation du bloc — asepsie",
         "Ponction unique sans cathéter : pas de rasage, désinfection en 2 temps. Pose de "
         "cathéter : rasage extemporané/épilation, désinfection non alcoolique type "
         "chirurgicale (CP). Gants/masque/calot recommandés dans tous les cas ; habillage "
         "chirurgical complet pour la pose d'un cathéter (Grade D). Désinfection cutanée "
         "systématique, type chirurgical, large (Grade A). Crème Emla possible."),
        ("Réalisation du bloc — technique",
         "Dose-test adrénalinée : valeur seulement positive ; recommandée pour les blocs "
         "profonds (Grade E). Injections lentes et fractionnées recommandées (Grade D)."),
        ("Surveillance du bloc",
         "Installation surveillée attentivement (toxicité systémique parfois retardée) "
         "(Grade E). Bloc sensitif/moteur testé avant champage ; extension "
         "péridurale/intrathécale recherchée pour les blocs proches du rachis (Grade E). "
         "Décision de conversion en AG prise avant le début de la chirurgie (CP). "
         "Opacification du cathéter non systématique, faite en cas d'inefficacité ou de "
         "doute (Grade E). Efficacité d'un cathéter d'analgésie établie avant la sortie de "
         "SSPI (CP). Pose du cathéter et 1ère injection réservées au médecin anesthésiste ; "
         "réinjections/surveillance/retrait délégables à un infirmier (décret "
         "2002-194)."),
        ("Chronologie AG-ALR",
         "ALR pratiquée avant le geste chirurgical pour bénéficier de l'analgésie régionale "
         "peropératoire (Grade A). ALR réalisée chez un patient éveillé ou sous sédation "
         "légère (Grade E) — la réaliser sous AG ou en zone déjà anesthésiée prive des "
         "signaux de sécurité (paresthésie, douleur) permettant de prévenir une "
         "complication neurologique ou une toxicité systémique."),
    ], TCW, head=("Thème", "Recommandation")))
    return story

# ---------------------------------------------------------------------------
def _section_q3():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Q3. Anesthésie locorégionale intraveineuse (ALRIV)"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(theme_table([
        ("Indication",
         "Chirurgie brève du membre supérieur, urgence ou ambulatoire ; encore 33 % des "
         "blocs du membre supérieur, fiabilité > 85 %."),
        ("Technique du garrot",
         "Garrot double au bras (pression d'occlusion artérielle calculée : POA = "
         "[(PAS-PAD) × circonférence/largeur garrot] + PAD) (Grade A). Garrot d'avant-bras "
         "possible, divise par 2 la dose de lidocaïne (Grade A). Exsanguination à la bande (jamais "
         "bande d'Esmarch) ; membre surélevé 90° 3-5 min en urgence (Grade A). Garrots "
         "gonflés à 50 mmHg au-dessus de la POA, inférieur dégonflé en premier (Grade A). "
         "Regonflage du garrot inférieur/dégonflage du supérieur possible pour soulager le "
         "patient en cours d'ALRIV (Grade B)."),
        ("Anesthésique local",
         "Lidocaïne 0,5 %, 3 mg/kg (0,5-0,6 mL/kg), injectés en > 90 s, seul AL recommandé "
         "actuellement (Grade A) — installation en 10 min. Prilocaïne, mépivacaïne et "
         "surtout bupivacaïne à ne pas utiliser (Grade A). Ropivacaïne non recommandée à ce "
         "jour malgré une anesthésie/analgésie postopératoire raisonnables (Grade B)."),
        ("Durée et lâcher du garrot",
         "Durée minimale 20 min, maximale tolérable 90 min (Grade A). Dégonflage progressif "
         "(2-3 regonflages de 30 s toutes les 15 s) recommandé, allonge le délai avant Cmax "
         "de l'AL (Grade A)."),
        ("Adjuvants et associations non recommandées",
         "Opiacés, AINS, curare et/ou kétamine ajoutés à la lidocaïne : non recommandés "
         "(Grade A). Clonidine 1 µg/kg possible, améliore la tolérance au garrot et "
         "potentialise l'analgésie postopératoire (Grade B)."),
        ("Après le lâcher du garrot",
         "Sensibilité réapparaît en 5 min. Immobilisation du membre ≥ 30 min, contrôle "
         "obligatoire du pouls radial (Grade A)."),
        ("Techniques et indications non recommandées",
         "ALRIV du membre inférieur ou intra-artérielle (Grade B). ALRIV continue (Grade "
         "B). « Nouvelle » ALRIV (ré-exsanguination + lâcher bref à 20 min) (Grade B)."),
    ], TCW, head=("Thème", "Recommandation")))
    return story

# ---------------------------------------------------------------------------
def _section_q4_q5_q6():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Q4-6. Repérage, matériel et agents pharmacologiques"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(theme_table([
        ("Neurostimulation",
         "Technique de référence pour le repérage (CP) — prônée depuis longtemps pour les "
         "blocs profonds/difficiles ; la recherche de paresthésies majore le risque de "
         "complications neurologiques. Semble diminuer le risque de neuropathie "
         "postopératoire (Grade D). Multistimulation (≥3 sites) supérieure à la "
         "monostimulation pour les blocs axillaire/ischiatique : installation plus rapide, "
         "meilleure étendue, moins de blocs complémentaires, sans excès d'effets "
         "secondaires (Grade A)."),
        ("Déroulement du repérage",
         "Séquence stéréotypée après vérification du neurostimulateur : intensité "
         "démarrée à 2 mA/100 µs, mobilisation dans les 3 axes, recherche de l'intensité "
         "minimale, test d'aspiration avant chaque injection, injection lente et "
         "fractionnée (CP). Seuil de stimulation minimal = critère de proximité "
         "aiguille-nerf, sa recherche systématique devrait réduire le risque lésionnel "
         "(injecter à 0,5 mA sans recherche préalable n'est pas sans risque)."),
        ("Repères par abord",
         "Interscalénique : approche latérale/superficielle (CP). Supraclaviculaire : voie "
         "latérale/tangentielle pour limiter ponction vasculaire et pneumothorax (CP). "
         "Infraclaviculaire : réponse flexion avant-bras/main la plus fiable. Plexus "
         "lombaire (voie postérieure) : réponse quadriceps recherchée, sans garantir "
         "l'absence de diffusion périmédullaire (CP). Voie antérieure (fémoral/3-en-1/"
         "iliofascial) : ponction latérale préférée. Sciatique glutéal : bord inférieur du "
         "muscle piriforme (CP), double stimulation (tibiale/fibulaire) plus efficace "
         "qu'une stimulation unique (Grade A). Poplité : ponction haute (10 cm du pli de "
         "flexion) (CP), double réponse plus efficace en abord latéral (Grade A)."),
        ("Matériel — aiguilles",
         "Aiguilles isolées uniquement recommandées. Biseau court (20-30°) recommandé "
         "(Grade A) — moins de lésions nerveuses qu'un biseau long 12-15° (Grade C). "
         "Biseau « pointe-crayon » déconseillé (pénétration tissulaire médiocre)."),
        ("Matériel — cathéters, canules, filtres",
         "Cathéter polyamide/polyéthylène à extrémité fermée, guide métallique souple, 3 "
         "orifices latéraux : recommandé pour l'analgésie perinerveuse continue (Grade B) "
         "— réduit les blocs unilatéraux/insuffisants (Grade C). Cathéters stimulants : "
         "aucune preuve d'avantage. Couleur unique recommandée pour les cathéters d'ALR (E, "
         "avis d'experts). Canules en ETFE préférées au FEP (E, avis d'experts). Filtre sur "
         "cathéter périnerveux maintenu plusieurs jours recommandé par précaution, en "
         "l'absence de preuve formelle (E, avis d'experts) — par analogie aux "
         "recommandations Sfar sur les filtres périduraux (Grade C)."),
        ("AL courte/intermédiaire (lidocaïne, mépivacaïne)",
         "Installation et durée plus longues avec mépivacaïne qu'avec lidocaïne (Grade C). "
         "Pas de différence installation/durée entre mépivacaïne et lidocaïne adrénalinées "
         "(Grade B)."),
        ("AL longue durée (ropivacaïne, bupivacaïne)",
         "Toxicité systémique (cardiaque, neurologique) moindre pour la ropivacaïne à dose "
         "égale (Grade B). Installation plus rapide avec ropivacaïne 0,75 % qu'avec "
         "bupivacaïne 0,5 % (Grade C) ; durée comparable (Grade C)."),
        ("Mélanges d'AL",
         "Lidocaïne/bupivacaïne vs bupivacaïne seule : toxicité neurologique additive "
         "(Grade B) ; toxicité cardiaque du mélange peut-être moindre (Grade D) ; "
         "installation plus rapide (Grade C) ; durée intermédiaire (Grade C)."),
        ("Adjuvants",
         "Adrénaline 5 µg/mL diminue les concentrations plasmatiques de lidocaïne, "
         "mépivacaïne, bupivacaïne et du mélange lidocaïne/bupivacaïne, mais pas de la "
         "ropivacaïne (Grade B) ; prolonge la durée du bloc à la lidocaïne, possiblement à "
         "la mépivacaïne (Grade C). Clonidine périnerveuse (0,5-1 µg/kg) prolonge les "
         "blocs sensitif/moteur et l'analgésie postopératoire avec mépivacaïne/lidocaïne "
         "(Grade B). Opiacés ajoutés aux AL : bénéfice analgésique minime (Grade B), plus "
         "de nausées/vomissements (Grade C). Alcalinisation non recommandée (résultats "
         "hétérogènes)."),
    ], TCW, head=("Thème", "Recommandation")))
    return story

# ---------------------------------------------------------------------------
T1_HEAD = pstyle("bpm_t1_head", fontSize=7.6, leading=9, textColor=WHITE, fontName=FONT_BOLD,
                  alignment=TA_CENTER)
T1_CELL = pstyle("bpm_t1_cell", fontSize=7.6, leading=9.4, textColor=INK, alignment=TA_CENTER)
T1_CELL_L = pstyle("bpm_t1_cell_l", fontSize=7.6, leading=9.4, textColor=INK)

def _table1_indications_ms():
    rows = [
        ("Prothèse d'épaule", "BIS", "+"),
        ("Rupture coiffe des rotateurs", "BIS", "+"),
        ("Arthrolyse d'épaule", "BIS", "+"),
        ("Acromioplastie à ciel ouvert", "BIS", "+"),
        ("Acromioplastie arthroscopique", "BIS", "0"),
        ("Bankart", "BIS", "+ (peu douloureux si arthroscopie)"),
        ("Butée d'épaule", "BIS", "+"),
        ("Luxation acromioclaviculaire", "BIS", "0"),
        ("Luxation d'épaule", "BIS", "0"),
        ("Ostéosynthèse de clavicule", "BIS + plexus cervical superficiel", "0"),
        ("Ostéosynthèse tête humérale", "BSC", "+"),
        ("Ostéosynthèse diaphyse humérale", "BSC ou BIC", "+"),
        ("Fracture palette humérale", "BSC ou BIC, complément canal huméral", "+"),
        ("Arthrolyse du coude", "BSC, BIC ou BAX", "+"),
        ("Arthroscopie du coude", "BSC", "0"),
        ("Fracture de l'olécrane", "BSC ou BIC", "0"),
        ("Épicondylite, neurolyses au coude", "BCH", "0"),
        ("Fractures avant-bras, poignet", "BIC, BAX ou BCH", "0"),
        ("Traumatismes graves de la main", "BIC, BAX, complément canal huméral", "+"),
        ("Chirurgie réglée main/avant-bras/poignet", "BAX, BCH", "+ (en axillaire selon l'acte)"),
        ("Chirurgie de la fistule artério-veineuse", "BAX, BCH", "0"),
    ]
    data = [[Paragraph("Indication chirurgicale", T1_HEAD), Paragraph("Type de bloc", T1_HEAD),
             Paragraph("Cathéter", T1_HEAD)]]
    for a, b, c in rows:
        data.append([Paragraph(a, T1_CELL_L), Paragraph(b, T1_CELL), Paragraph(c, T1_CELL)])
    t = Table(data, colWidths=[62 * mm, 62 * mm, CW_FULL - 124 * mm], repeatRows=1)
    style_cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("GRID", (0, 0), (-1, -1), 0.5, GREY_LIGHT),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 2.4), ("BOTTOMPADDING", (0, 0), (-1, -1), 2.4),
        ("LEFTPADDING", (0, 0), (-1, -1), 3), ("RIGHTPADDING", (0, 0), (-1, -1), 3),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            style_cmds.append(("BACKGROUND", (0, i), (-1, i), BG_PANEL))
    t.setStyle(TableStyle(style_cmds))
    return t

def _section_q7():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Q7. Recommandations — membre supérieur"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(theme_table([
        ("Épaule",
         "Position semi-assise (beach chair) indiquée, y compris arthroscopie (Grade D). "
         "Solutions adrénalinées contre-indiquées en interscalénique assis (risque de "
         "réflexe de Bezold-Jarisch, hypotension/bradycardie) (Grade A) — traitement : "
         "atropine, éphédrine, remplissage (CP). Bloc interscalénique = technique de "
         "référence (C3-C7), extension aux racines C8-T1 souvent absente (Grade C). Blocs "
         "de complément selon la voie chirurgicale (Grade E) : plexus cervical superficiel "
         "+ nerf intercostobrachial (voies antérieures) ; bloc intercostal T2 ou "
         "paravertébral T1-T4 (voies postérieures, préférer une AG associée) (CP) ; nerf "
         "sus-scapulaire ou infiltration traçante (arthroscopie). Fracture extrémité "
         "supérieure humérus : bloc supraclaviculaire préféré à l'interscalénique (Grade "
         "D). Interscalénique utilisable en ambulatoire (moindre consommation "
         "d'antalgiques, sortie précoce) (Grade D)."),
        ("Bras (tiers moyen)",
         "Voies supraclaviculaires indiquées pour la chirurgie orthopédique/vasculaire du "
         "bras ; tester/compléter les territoires intercostobrachial et cutané médial du "
         "bras avant la chirurgie."),
        ("Coude",
         "Anesthésie du coude : bloc des 4 nerfs mixtes + 2 nerfs sensitifs, débordant "
         "largement le site opératoire. Bloc supraclaviculaire adapté mais contre-indiqué "
         "en ambulatoire (risque de pneumothorax à distance) (Grade D) ; souvent complété "
         "par infiltration traçante (intercostobrachial/cutané médial). Bloc "
         "infraclaviculaire (voie sous-coracoïdienne préférée, moindre risque de "
         "pneumothorax) (Grade E) : anesthésie du bras sans mobilisation. Blocs axillaire/"
         "canal huméral suffisants pour la chirurgie réglée — axillaire efficace ~90 %, "
         "recommandé avec blocage sélectif du musculo-cutané (CP), 2 stimulations "
         "supérieures sur le radial (Grade E) ; canal huméral = anesthésie différentielle "
         "des 4 nerfs mixtes (Grade B). Technique transartérielle non recommandée (CP). "
         "Interscalénique insuffisant (extension ulnaire/cutanés aléatoire) (Grade D). "
         "Arthroscopie du coude : supraclaviculaire préféré (extension souvent à "
         "l'axillaire) (Grade B)."),
        ("Avant-bras et main",
         "Garrot pneumatique : bloquer 7 nerfs (médian, ulnaire, radial, musculo-cutané, "
         "cutanés médiaux bras/avant-bras, intercostobrachial). Axillaire (multistimulation "
         "de préférence) efficace (Grade C). Canal huméral : bloc différentiel par "
         "territoire (Grade B). Blocs au coude : limitent le bloc moteur à la main, "
         "réservés aux interventions ≤ 15-30 min de garrot (Grade B) ; garrot > 20 min → "
         "axillaire ou canal huméral. Interventions courtes sans garrot : blocs distaux "
         "(coude/tiers inférieur de l'avant-bras) (CP). Blocs au coude/poignet adaptés à "
         "l'ambulatoire, mieux acceptés, préservent la mobilité peropératoire des doigts. "
         "Anesthésie intrathécale des doigts (gaine des fléchisseurs) : courte durée ou "
         "analgésie prolongée pour les 2e-4e doigts, garrot digital si besoin."),
    ], TCW, head=("Territoire", "Recommandation")))
    story.append(Spacer(1, 2 * mm))
    story.append(P("<b>Tableau 1 — Indications retenues pour la chirurgie du membre "
                    "supérieur</b> (consensus professionnel ; BIS bloc interscalénique, BSC "
                    "supraclaviculaire, BIC infraclaviculaire, BAX axillaire, BCH canal "
                    "huméral ; « + »/« 0 » = cathéter recommandé ou non)", S_CELL_B))
    story.append(Spacer(1, 1 * mm))
    story.append(_table1_indications_ms())
    return story

# ---------------------------------------------------------------------------
def _section_q8():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Q8. Recommandations — membre inférieur"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(theme_table([
        ("Hanche",
         "Bloc du plexus lombaire par voie postérieure : diffusion quasi constante aux 3 "
         "troncs, mais risque d'extension périmédullaire quel que soit le niveau de "
         "ponction (Grade B) — opacification des cathéters recommandée pour vérifier "
         "l'absence d'extension (CP). Voies antérieures (fémoral, 3-en-1, iliofascial) : "
         "moins de complications mais diffusion très aléatoire (Grade A) ; cathéter à ne "
         "pas introduire > 15-20 cm (Grade E). Bloc sciatique nécessaire mais n'atteint pas "
         "toutes les branches du plexus sacré (Grade E). Blocs tronculaires seuls "
         "insuffisants en 1re intention (CP) : association lombaire-sciatique compatible "
         "avec vissage du col/prothèse intermédiaire/ostéosynthèse pertrochantérienne "
         "(Grade C), complétée si besoin par blocs des nerfs de la crête ou "
         "ilio-hypogastrique/ilio-inguinal/génito-fémoral (Grade C)."),
        ("Cuisse",
         "Association plexus lombaire + sciatique adaptée à la chirurgie de cuisse/fémur "
         "(Grade E)."),
        ("Genou",
         "Voies postérieures : extension plus constante que les voies antérieures (Grade "
         "B) ; voies antérieures adaptées et recommandées (Grade A), sans supériorité "
         "démontrée entre inguinal-paravasculaire et iliofascial (Grade B). Bloc sciatique "
         "recommandé en complément du fémoral (Grade A) ; voies parasacrée/postérieure "
         "assurent un bloc du nerf cutané postérieur plus constant, sans supériorité "
         "démontrée entre les deux (Grade E). Association lombaire/sciatique recommandée "
         "pour prothèse, ligamentoplastie, arthroscopie, lavage articulaire (Grade A)."),
        ("Jambe et cheville",
         "Face interne : bloc fémoral ou bloc isolé du nerf saphène, sans avantage de la "
         "voie lombaire postérieure sur une voie antérieure/distale (Grade B). Face "
         "externe/postérieure : bloc sciatique (Grade A). Association "
         "lombaire+sacré : anesthésie complète (Grade C), autorise toute chirurgie de "
         "jambe/cheville (Grade A) ; décubitus ventral : évaluation soigneuse avant "
         "incision (CP). Risque de syndrome des loges : pas une contre-indication au bloc, "
         "sous surveillance adaptée (Grade E)."),
        ("Pied",
         "Bloc sciatique recommandé (CP), complété par bloc du nerf saphène pour la face "
         "antéro-médiale ; aucune voie sciatique privilégiée au-dessus du genou ou au "
         "poplité (Grade B). Double stimulation (fibulaire/tibial) recommandée en abord "
         "poplité latéral (Grade B). Bloc de cheville : simple et efficace pour la chirurgie "
         "mineure (Grade C). Sciatique poplité : adapté à la chirurgie avec garrot cheville, "
         "bloc du nerf saphène pouvant compléter pour limiter la douleur de garrot (Grade C) ; "
         "sciatique au-dessus du genou : garrot cuisse (Grade C)."),
        ("Chirurgie vasculaire du membre inférieur",
         "Réalisable sous bloc tronculaire (Grade C). Bloc fémoral + infiltration du "
         "trigone fémoral pour les varices ; bloc sciatique associé si le territoire "
         "chirurgical déborde le plexus lombaire (Grade E)."),
    ], TCW, head=("Territoire", "Recommandation")))
    return story

# ---------------------------------------------------------------------------
def _section_q9():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Q9. Analgésie postopératoire"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(theme_table([
        ("Épaule (arthroscopique)",
         "BIS en injection unique = technique de choix (Grade A) ; bloc du nerf "
         "sus-scapulaire en alternative si contre-indication (insuffisance respiratoire) "
         "(Grade A)."),
        ("Épaule (chirurgie ouverte)",
         "Cathéter au-dessus de la clavicule recommandé (Grade A)."),
        ("Coude (chirurgie majeure)",
         "Cathéter axillaire sûr et efficace (Grade E) ; abords périclaviculaires en "
         "traumatologie (Grade E)."),
        ("Main (chirurgie majeure)",
         "Cathéter axillaire : analgésie de qualité + sympathoplégie, utile en cas "
         "d'atteinte vasculaire/réimplantation (Grade B). Cathéter au poignet possible pour "
         "certaines interventions spécifiques (ténolyse...) (Grade E)."),
        ("Hanche (arthroplastie totale)",
         "Cathéter fémoral = technique appropriée (Grade B) ; bloc du plexus lombaire "
         "postérieur possible mais en cours d'évaluation (Grade E)."),
        ("Fracture du col du fémur",
         "Bloc fémoral en injection unique peut être efficace (Grade C) ; cathéter dès "
         "l'arrivée en salle d'urgence potentiellement intéressant (Grade E) ; voie "
         "antérieure vs postérieure non tranchée."),
        ("Diaphyse fémorale",
         "Bloc fémoral en injection unique recommandé, cathéter licite (CP)."),
        ("Genou (arthroscopie mineure)",
         "Analgésie intra-articulaire (AL, morphine, clonidine) efficace (Grade A) ; non "
         "recommandée en complément d'une anesthésie chirurgicale par bloc(s) "
         "périphérique(s) (risque de toxicité systémique) (CP)."),
        ("Genou (arthroscopie lourde/ligamentoplastie)",
         "Bloc fémoral injection unique (ambulatoire) ou cathéter (hospitalisé) recommandé "
         "(Grade B)."),
        ("Genou (chirurgie ouverte)",
         "Cathéter fémoral recommandé (Grade A)."),
        ("Pied (chirurgie mineure)",
         "Bloc sciatique injection unique = technique la plus efficace (Grade C)."),
        ("Pied (chirurgie majeure)",
         "Cathéter sciatique poplité recommandé (Grade C)."),
    ], TCW, head=("Situation", "Recommandation")))
    return story

# ---------------------------------------------------------------------------
def _section_q10_q11():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Q10-11. Anticoagulants et pathologie neurologique"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(theme_table([
        ("Anticoagulants — hématome",
         "Survenue exceptionnelle après un bloc périphérique quel qu'il soit (Grade D) ; "
         "imputabilité pas toujours certaine, évolution le plus souvent favorable. 3 "
         "risques : reprise chirurgicale, transfusion, compression nerveuse. Risque "
         "possiblement majoré si anticoagulation efficace, association "
         "anticoagulant/antiagrégant, ou blocs profonds vs superficiels (CP)."),
        ("Anticoagulants — conduite",
         "Surveillance neurologique postopératoire tenant compte du risque d'hématome "
         "(Grade D). Pose d'un cathéter à argumenter spécifiquement (Grade D)."),
        ("Pathologie neurologique — indications",
         "Pas de contre-indication absolue chez un malade atteint d'une pathologie "
         "neurologique stable et bien étiquetée (Grade E). Réserves en cas de "
         "polyradiculonévrite dysimmunitaire (Guillain-Barré, caractère évolutif "
         "imprévisible) (Grade E/D). Atteintes diabétiques/métaboliques : pas de "
         "contre-indication sous réserve d'un diagnostic précis (Grade E). Déficit "
         "neurologique traumatique/vasculaire stabilisé depuis plusieurs mois : pas de "
         "risque spécifique mais examen neurologique préalable documenté nécessaire. "
         "Sclérose en plaques : pas une contre-indication (Grade D). Myopathie "
         "mitochondriale : prudence (myotoxicité de la bupivacaïne) (Grade D), rapport "
         "bénéfice/risque individuel (Grade E)."),
        ("Pathologies à risque potentiel d'aggravation",
         "Neuropathies diabétiques sévères/évolutives avec facteurs aggravants (Grade D) ; "
         "neuropathies post-chimiothérapie (vincristine, cisplatine) (Grade E) ; "
         "neuropathies héréditaires (Charcot-Marie-Tooth, HNPP) (Grade D) ; atteintes "
         "chroniques de la corne antérieure (amyotrophie spinale, séquelles de "
         "poliomyélite) (Grade E) ; neuropathies motrices multifocales avec blocs de "
         "conduction persistants."),
        ("Pathologie neurologique — technique",
         "Avis neurologique recommandé en cas de maladie rare ; aucun examen complémentaire "
         "n'a de valeur indiscutable pour récuser un bloc, l'exploration "
         "électrophysiologique préopératoire peut servir de référence. Seuils de "
         "neurostimulation parfois plus élevés (prudence). Usage prolongé (cathéter) à "
         "éviter (neurotoxicité locale potentielle, surtout fortes concentrations). "
         "Réversibilité du bloc à documenter par un schéma. Avis neurologique spécialisé en "
         "cas de déficit après un bloc (toutes ces recommandations Grade E)."),
    ], TCW, head=("Thème", "Recommandation")))
    return story

# ---------------------------------------------------------------------------
def _section_q12():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Q12. Gestion de l'échec des blocs périphériques"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(theme_table([
        ("Diagnostic de l'échec",
         "Échec total ou partiel diagnostiqué avant le début de l'intervention (CP). "
         "Évaluation systématique par territoire nerveux (motricité, sensibilité "
         "thermo-algique, tactile épicritique, sympathique, proprioceptive), répétée dans "
         "le délai habituel d'installation du bloc (CP)."),
        ("Prévention de l'échec",
         "Multistimulation supérieure à la localisation d'un seul nerf/tronc pour un bloc "
         "plexique/pluri-nerveux (Grade A). Effet volume : augmenter le volume améliore la "
         "diffusion et élargit le territoire bloqué (Grade A) ; à volume égal, augmenter la "
         "concentration améliore l'intensité mais pas l'étendue (Grade B)."),
        ("Échec de repérage",
         "Remettre rapidement en cause la technique ; vérifier le neurostimulateur (Grade "
         "E), les repères anatomiques et le positionnement. Échec persistant : changer de "
         "technique ou faire appel à un autre anesthésiste (Grade E)."),
        ("Impossibilité d'injection",
         "Reflux sanguin au test d'aspiration, contractions persistantes aux premiers mL, "
         "ou prodromes de toxicité : interrompre immédiatement l'injection, retirer et "
         "repositionner l'aiguille (CP)."),
        ("Échec complet",
         "Ne pas attendre au-delà de 30 min (CP). Sédation de complément non substitutive "
         "(Grade E). Réaliser un autre bloc par une autre voie, ou changer de technique "
         "(conversion AG, rachianesthésie) (Grade E)."),
        ("Échec partiel",
         "Anesthésie incomplète parfois suffisante si zone chirurgicale/garrot en "
         "territoire anesthésié. Bloc de complément possible au même site (Grade B). "
         "Réinjection par le même cathéter bénéfique seulement si bloc « presque complet » "
         "(Grade B). Complément par bloc tronculaire plus distal possible — attention à la "
         "dose maximale cumulée."),
    ], TCW, head=("Thème", "Recommandation")))
    return story

# ---------------------------------------------------------------------------
DOSE_HEAD = pstyle("bpm_dose_head", fontSize=8, leading=9.6, textColor=WHITE, fontName=FONT_BOLD,
                    alignment=TA_CENTER)
DOSE_CELL = pstyle("bpm_dose_cell", fontSize=8, leading=9.6, textColor=INK, alignment=TA_CENTER)
DOSE_CELL_L = pstyle("bpm_dose_cell_l", fontSize=8, leading=9.6, textColor=INK)

def _table_doses_max():
    rows = [
        ("lidocaïne adrénalinée", "500 mg", "700 mg"),
        ("mépivacaïne *", "400 mg", "400 mg"),
        ("bupivacaïne adrénalinée", "150 mg", "180 mg"),
        ("ropivacaïne *", "225 mg", "300 mg"),
    ]
    data = [[Paragraph("Agent", DOSE_HEAD), Paragraph("Bloc membre supérieur", DOSE_HEAD),
             Paragraph("Bloc membre inférieur", DOSE_HEAD)]]
    for a, b, c in rows:
        data.append([Paragraph(a, DOSE_CELL_L), Paragraph(b, DOSE_CELL), Paragraph(c, DOSE_CELL)])
    t = Table(data, colWidths=[70 * mm, (CW_FULL - 70 * mm) / 2, (CW_FULL - 70 * mm) / 2],
              repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("GRID", (0, 0), (-1, -1), 0.5, GREY_LIGHT),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING", (0, 0), (-1, -1), 4), ("RIGHTPADDING", (0, 0), (-1, -1), 4),
    ]))
    return t

def _section_q13():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Q13. Toxicité systémique des anesthésiques locaux (AL)"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(theme_table([
        ("Pharmacocinétique",
         "Pic d'absorption décroissant : bloc cervical > intercostal > plexus brachial > "
         "fémoral > ilio-inguinal > sciatique. Adrénaline diminue la concentration "
         "plasmatique des AL (Grade A). Clairance diminuée chez le sujet âgé. AL d'action "
         "courte absorbés plus vite que ceux de longue durée — pour un acte de 1h30, "
         "utiliser un AL de longue durée d'action."),
        ("Toxicité neurologique",
         "Accidents convulsifs pour tous les agents (1/800 à 1/1500 blocs). Antécédents "
         "d'épilepsie : pas une contre-indication. Rapport de toxicité neurologique "
         "bupivacaïne:ropivacaïne:lidocaïne ≈ 4:3:1 (Grade A). Traitement d'un accident "
         "convulsif : liberté des voies aériennes + oxygénation ; benzodiazépines ou "
         "thiopental (< 200 mg) si persistance ; succinylcholine si état de mal (CP)."),
        ("Toxicité cardiaque",
         "Bupivacaïne, étidocaïne et (moindre) ropivacaïne : accidents cardiaques graves "
         "rares, pouvant être mortels. Pas plus fréquents chez la femme enceinte (Grade "
         "A). Troubles de conduction/insuffisance cardiaque : pas des contre-indications "
         "aux AL (Grade A). Bolus d'adrénaline limités à 5-10 µg/kg (tachycardie "
         "ventriculaire/fibrillation). Aucun médicament des arrêts cardiaques d'autre "
         "origine ne doit être utilisé en 1re intention (effets additifs à l'AL) (CP)."),
        ("Toxicité métabolique",
         "Lidocaïne contre-indiquée en cas de porphyrie hépatique (seuls esters et "
         "bupivacaïne utilisables). Méthémoglobinémie possible sous prilocaïne (crème "
         "Emla®, sans risque si dose respectée) — traitement : bleu de méthylène IV "
         "1-5 mg/kg."),
        ("Allergie et adjuvants",
         "Allergie aux AL amides très rare ; solutions adrénalinées contiennent des "
         "conservateurs pouvant provoquer des réactions allergiques. Allergie plus "
         "fréquente avec les esters (non utilisés en clinique). Solutions adrénalinées "
         "proscrites en territoire à vascularisation terminale (ex. bloc des doigts)."),
        ("Prévention des accidents — intervalle entre injections",
         "Intervalle ≥ 1/3 de la demi-vie de l'agent : 30 min (lidocaïne, prilocaïne, "
         "mépivacaïne), 45 min (bupivacaïne, étidocaïne, ropivacaïne) (CP)."),
        ("Prévention des accidents — doses successives",
         "2e injection ≤ 1/3 de la dose maximale initiale après le délai précité, ou "
         "moitié de cette dose après 60/90 min respectivement. À partir de la 3e "
         "injection, pharmacocinétique standard (moitié de dose après une demi-vie, ou "
         "tiers de dose après une demi demi-vie) (CP). Dose totale (même fractionnée) et "
         "somme des doses en cas de mélange doivent être prises en compte. Injection "
         "lente et fractionnée, sans protection totale contre un accident (CP)."),
    ], TCW, head=("Thème", "Recommandation")))
    story.append(Spacer(1, 2 * mm))
    story.append(P("<b>Doses maximales pour la première injection, adulte jeune ASA 1</b> "
                    "(E, avis d'experts) — *pas de solution adrénalinée disponible",
                    S_CELL_B))
    story.append(Spacer(1, 1 * mm))
    story.append(_table_doses_max())
    return story

# ---------------------------------------------------------------------------
def _section_q14():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Q14. Complications neurologiques"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(theme_table([
        ("Agression nerveuse par l'aiguille",
         "Paresthésie au contact du tronc nerveux = risque de blessure. Aiguilles à "
         "biseau court et pointe peu acérée recommandées, moins traumatisantes (Grade B). "
         "Biseau long/pointe acérée : risque accru d'injection intraneurale, majorant la "
         "neurotoxicité locale (Grade B), surtout avec adjuvant adrénaliné ou solution "
         "bicarbonatée."),
        ("Dose et produits",
         "Dose minimale efficace à utiliser — tous les AL sont neurotoxiques à dose/"
         "concentration élevée (Grade A). Clonidine périnerveuse : non neurotoxique (Grade "
         "A)."),
        ("Fréquence et facteurs de risque",
         "Complications neurologiques locales 4× moins fréquentes que les complications "
         "systémiques des AL ou les complications neurologiques périmédullaires (Grade "
         "D). Complications neurologiques le plus souvent liées à l'acte chirurgical "
         "(incidence chirurgicale : 0,1 % membre supérieur, 1 % hanche) (Grade D). "
         "Syndrome de Claude-Bernard-Horner et parésie laryngée : fréquents et "
         "transitoires après bloc interscalénique ; extensions centrales surtout décrites "
         "avec interscalénique, certains sus-claviculaires et blocs du plexus lombaire."),
        ("Lésions après bloc tronculaire",
         "Troubles sensitifs/moteurs souvent de topographie identique à une paresthésie "
         "ressentie pendant le bloc (Grade D). Neurostimulation recommandée — diminue "
         "l'incidence des paresthésies sans les prévenir totalement (Grade D). Injection "
         "intraneurale : douleur immédiate et retardée ; bloc sous AG (supprime ce signal "
         "d'alarme) non recommandé. Facteurs favorisants : âge (Grade D), compressions "
         "rachidiennes (canal étroit), diabète/insuffisance rénale chronique/dénutrition/"
         "alcoolisme chronique (Grade A, sans aggravation démontrée par l'ALR), "
         "pathologies démyélinisantes (HNPP, certaines chimiothérapies) (Grade E)."),
        ("Conduite en cas de complication",
         "Examen neurologique dès que la durée du bloc dépasse largement la durée "
         "prévisible ; avis neurologique rapide recommandé ; examen consigné par écrit et "
         "comparé au bilan préopératoire ; imagerie si cause mécanique suspectée. "
         "Électromyogramme ± potentiels évoqués : 1er examen le plus tôt possible "
         "(référence, avant J3, car dénervation active visible seulement ~3 semaines "
         "après la lésion), 2e examen entre S3 et S4, 3e EMG à ~3 mois. Récupération "
         "compromise si aucune amélioration électrophysiologique à 18 mois (Grade E)."),
    ], TCW, head=("Thème", "Recommandation")))
    return story

# ---------------------------------------------------------------------------
def _section_sources():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("Sources et avertissement"))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "SFAR, avec la Sofcot et la Sofmer, « Les blocs périphériques des membres chez "
        "l'adulte », Recommandations pour la Pratique Clinique, présentées le 22 septembre "
        "2001 (43e Congrès national d'anesthésie et de réanimation), publiées Ann Fr Anesth "
        "Réanim 22 (2003) 567-581.", S_SOURCE))
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Avertissement — document de 2001/2003 :</b> cette fiche est une synthèse "
        "indépendante, produite pour un usage d'aide-mémoire. Elle condense la prose "
        "contextuelle non actionnable du texte source (conformément à la règle de projet "
        "sur l'argumentaire) mais reprend l'intégralité des recommandations et grades "
        "énoncés, ainsi que le Tableau 1 et le tableau des doses maximales. Elle ne "
        "remplace pas le texte intégral et n'est ni éditée ni validée par la SFAR/Sofcot/"
        "Sofmer. Les techniques d'échoguidage (généralisées depuis, cf. la RFE 2011 "
        "« échographie et anesthésie locorégionale » de ce même corpus), les agents "
        "pharmacologiques disponibles et les pratiques de sécurité ayant considérablement "
        "évolué depuis 2001, se référer à un avis spécialisé et aux recommandations "
        "actualisées avant toute décision thérapeutique — ce document RPC 2001 reste "
        "cependant une référence active, non abrogée, complétée mais non remplacée par les "
        "RFE ultérieures sur l'échoguidage.", S_BODY_SM), bg=GREY_LIGHT, border=GREY))
    return story

# ---------------------------------------------------------------------------
def _section_intro_q1_q2_q3():
    story = _section_intro()
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_q1_q2())
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_q3())
    return story

def _section_q7_q8():
    story = _section_q7()
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_q8())
    return story

def _section_q9_q10_q11():
    story = _section_q9()
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_q10_q11())
    return story

def _section_q12_q13():
    story = _section_q12()
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_q13())
    return story

def _section_q14_sources():
    story = _section_q14()
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_sources())
    return story

def _section_q9_to_sources():
    story = _section_q9_q10_q11()
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_q12_q13())
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_q14_sources())
    return story

SECTIONS = [
    ("Méthodologie, Q1-3 — Information, préparation, surveillance, ALRIV", _section_intro_q1_q2_q3),
    ("Q4-6 — Repérage, matériel, agents pharmacologiques", _section_q4_q5_q6),
    ("Q7-8 — Membre supérieur (Tableau 1) & membre inférieur", _section_q7_q8),
    ("Q9-14 — Analgésie, anticoagulants, neurologie, échec, toxicité, "
     "complications & sources", _section_q9_to_sources),
]

def _make_doc(path=None):
    return SimpleDocTemplate(path or OUT, pagesize=A4,
                              leftMargin=MARGIN, rightMargin=MARGIN,
                              topMargin=32 * mm, bottomMargin=16 * mm,
                              title="Fiche SFAR 2003 - Blocs peripheriques des membres chez l'adulte",
                              author="Synthèse indépendante (source SFAR/Sofcot/Sofmer)")

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

    final_story = _build_upto(fns)
    docf = _make_doc()
    docf.build(final_story, onFirstPage=on_page_final, onLaterPages=on_page_final)
    print("OK ->", OUT, f"({total_pages} pages)")

if __name__ == "__main__":
    build()
