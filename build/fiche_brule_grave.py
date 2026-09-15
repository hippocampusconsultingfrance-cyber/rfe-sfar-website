# -*- coding: utf-8 -*-
"""
Fiche de synthese - RPP SFAR/SFB/SFMU/Adarpef, "Prise en charge du brule grave
a la phase aigue chez l'adulte et l'enfant", 2019. Auteurs coordinateurs :
M. Legrand, D. Barraud. Texte valide par le Comite des Referentiels
Cliniques (15/05/2019) et le CA de la Sfar (24/05/2019). 38 pages source,
telecharge depuis sfar.org (download/rpp-prise-en-charge-du-brule-grave/
?wpdmdl=24465).

METHODOLOGIE : format RPP (Recommandations pour la Pratique Professionnelle),
PAS RFE - choix explicitement motive par la source (trop peu d'etudes de
puissance suffisante sur le critere mortalite). Analyse de la litterature
methodologie GRADE (niveau de preuve par reference bibliographique), mais LA
FORCE DE CHAQUE RECOMMANDATION N'EST PAS un grade 1+/1-/2+/2- individuel :
formulation uniforme "les experts suggerent de faire/ne pas faire", cotation
Delphi (echelle 1-9, seuil de validation >=70% d'avis convergents et <20%
d'avis contraires). 24 recommandations au total (verifie par comptage direct :
Champ1=5, Champ2=5, Champ3=6, Champ4=3, Champ5=3, Champ6=2), TOUTES a
"Accord FORT" (aucune "Accord faible" nulle part dans le texte - verifie par
grep exhaustif) - meme convention de chip unique que fiche_bris_dentaires.py
(chip "AE", jamais un grade 1+/2+ invente).

LIMITE MAJEURE DE COUVERTURE - ANNEXES ABSENTES DU PDF SOURCE : le texte cite
10 annexes (Annexe 1, 2, 2bis, 3, 4, 4bis, 5, 5bis, 6, 7) contenant des
elements cliniquement centraux - le diagramme de Lund & Browder (Annexe 3),
la/les formule(s) et l'algorithme de remplissage vasculaire adulte et
pediatrique (Annexe 4/4bis), les criteres/algorithme d'intubation et la
posologie d'hydroxocobalamine (Annexe 5/5bis), le choix des pansements
(Annexe 6), les formules nutritionnelles de Toronto/Schofield (Annexe 7).
Verification exhaustive (grep de "Annexe" dans le texte extrait + inventaire
independant par subagent + fitz doc.get_images() sur les 38 pages) : AUCUNE
de ces annexes n'a de contenu extractible ou visible dans ce PDF - zero image
embarquee sur les 38 pages (hors le logo page 1), zero table/figure aux pages
ou elles sont citees (verifie visuellement a 170dpi sur 9 pages cibles :
6, 7, 10, 14, 15, 17, 19, 24, 26). Ce n'est pas un probleme d'extraction de
texte scramble (rien n'est illisible) - le contenu de ces annexes est
simplement absent du fichier telecharge, qui semble etre une version "texte
court" sans son materiel annexe. PER LA REGLE DE PROJET N°1/2, CE CONTENU
N'EST PAS INVENTE NI DEVINE ICI - son absence est disclosed explicitement
dans le panneau d'intro de la fiche plutot que silencieusement omise.
Consequence concrete : R1.1 (Lund & Browder), R2.1.1/R2.2/R2.3 (remplissage),
R3.3 (hydroxocobalamine) et R6.1 (formules nutritionnelles) restent
pleinement couvertes pour leur TEXTE de recommandation (100% par la regle 2),
mais le lecteur est renvoye au texte source pour le detail visuel des
tableaux/algorithmes cites.

ARGUMENTAIRE : volontairement condense (regle de projet 2026-09-14) - seuls
les seuils/doses/delais directement actionnables sont conserves en note
courte sous chaque bloc de recommandations ; la prose de justification
epidemiologique/statistique est omise.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from style import *
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.units import mm

OUT = "/home/user/rfe-sfar-website/output/Fiche_SFAR_Brule_Grave_2019.pdf"

SOURCE_TXT = ("Source : « Prise en charge du brûlé grave à la phase aiguë chez l'adulte et "
              "l'enfant » — RPP SFAR/SFB/SFMU/Adarpef, 2019. Fiche de synthèse non "
              "officielle : se référer au texte intégral.")

def P(txt, style=S_CELL):
    return Paragraph(txt, style)

def chip(label, **kw):
    return grade_chip(label, **kw)

CW_FULL = PAGE_W - 2 * MARGIN

def reco_table(rows, col_widths):
    """rows: (ref, text)."""
    data = [[P("N°", S_HEAD_W_C), P("Recommandation", S_HEAD_W), P("Accord", S_HEAD_W_C)]]
    for ref, txt in rows:
        data.append([P(ref, S_CELL_B), P(txt, S_CELL), chip("AE")])
    t = Table(data, colWidths=col_widths, repeatRows=1)
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

RCW = [14 * mm, CW_FULL - 14 * mm - 20 * mm, 20 * mm]

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

TCW = [46 * mm, CW_FULL - 46 * mm]

TOTAL_PAGES = {"n": 6}

def on_page(canvas, doc, page_title):
    header_band(canvas, doc, "SFAR / SFB / SFMU / ADARPEF — RPP, 2019",
                "Brûlé grave à la phase aiguë",
                page_title, icon_fn=lambda c, x, y: icon_drop(c, x, y, 13 * mm), color=RED)
    footer_band(canvas, doc, SOURCE_TXT, f"Page {doc.page} / {TOTAL_PAGES['n']}")

# ---------------------------------------------------------------------------
def _section_intro():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Résumé :</b> RPP conjointe SFAR/SFB/SFMU/Adarpef sur la prise en charge du "
        "brûlé grave (brûlures thermiques uniquement — brûlures électriques et chimiques "
        "explicitement hors champ) dans les 48 premières heures, chez l'adulte et l'enfant. "
        "6 champs : régulation/admission/télémédecine, réanimation hémodynamique, voies "
        "aériennes/inhalation de fumées, anesthésie-analgésie, traitement local, "
        "traitements autres (nutrition, thromboprophylaxie). 24 recommandations, toutes à "
        "<b>Accord fort</b>. ~10 000 séjours hospitaliers/an en France pour brûlure, dont la "
        "moitié nécessite un centre spécialisé ; incidence 4× plus élevée chez l'enfant.",
        S_BODY), bg=BG_PANEL, border=TEAL))
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>⚠ Limite de cette fiche — annexes absentes du PDF source :</b> le texte cite "
        "10 annexes (Lund &amp; Browder, formule et algorithme de remplissage vasculaire "
        "adulte/enfant, algorithme d'intubation, posologie hydroxocobalamine, choix des "
        "pansements, formules nutritionnelles de Toronto/Schofield). Vérification exhaustive "
        "(recherche textuelle + rendu visuel à 170dpi de 9 pages cibles) : <b>aucune de ces "
        "annexes n'est présente dans le fichier PDF téléchargé</b> — zéro image sur les 38 "
        "pages hors le logo de couverture. Le texte des recommandations elles-mêmes reste "
        "intégralement couvert ci-dessous ; pour le détail visuel des tableaux/algorithmes "
        "cités, se référer à une version complète du document (matériel supplémentaire non "
        "inclus dans le « texte court » téléchargé).", S_BODY_SM), bg=AMBER_LIGHT, border=AMBER))
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("Méthodologie — RPP (et non RFE)", color=RED))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "Analyse de la littérature (depuis janvier 2000) selon la méthodologie GRADE, mais "
        "format <b>RPP</b> retenu plutôt que RFE — la source justifie ce choix par la trop "
        "faible quantité d'études de puissance suffisante sur le critère mortalité. Les "
        "recommandations sont formulées « les experts suggèrent de faire / de ne pas faire », "
        "et cotées par méthode Delphi (échelle 1 à 9) : validées si ≥ 70 % des experts vont "
        "globalement dans le même sens et &lt; 20 % expriment un avis contraire. "
        "<b>Aucun grade 1+/1−/2+/2− individuel n'est attribué</b> — seul un accord global "
        "(fort/faible) est coté ; les 24 recommandations de ce texte sont toutes à "
        "<b>Accord fort</b> (vérifié : aucune occurrence d'« Accord faible »).", S_BODY_SM))
    return story

# ---------------------------------------------------------------------------
def _section_champ1():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Champ 1 — Régulation, admission en centre spécialisé, télémédecine", color=RED),
        Spacer(1, 1.5 * mm),
        P("<b>Définition du « brûlé grave » proposée par les experts</b> (aucune définition "
          "officielle n'existe) :", S_CELL_B),
        Spacer(1, 1 * mm),
        theme_table([
            ("Adulte", "Surface cutanée brûlée (SCB) &gt; 20 %, OU SCB du 3<sup>e</sup> degré "
             "&gt; 5 %, OU syndrome d'inhalation de fumées, OU localisation profonde "
             "(face/mains/pieds/périnée), OU brûlure électrique haut voltage — <b>OU</b> "
             "SCB &lt; 20 % ET terrain particulier (âge &gt; 75 ans, comorbidités sévères, "
             "inhalation suspectée/avérée, brûlure circulaire profonde, localisation "
             "superficielle face/mains/pieds/périnée/plis, SCB &gt; 10 %, 3<sup>e</sup> degré "
             "3-5 %, brûlure électrique bas voltage, brûlure chimique à l'acide "
             "fluorhydrique)."),
            ("Enfant", "SCB &gt; 10 %, OU 3<sup>e</sup> degré &gt; 5 %, OU nourrisson "
             "&lt; 1 an, OU comorbidités sévères, OU inhalation de fumées, OU localisation "
             "profonde (face/mains/pieds/périnée/plis de flexion), OU brûlure circulaire, "
             "OU brûlure électrique ou chimique."),
        ], TCW, head=("Population", "Critères de gravité (risque vital et/ou fonctionnel)")),
    ]))
    story.append(Spacer(1, 2 * mm))
    story.append(reco_table([
        ("R1.1", "Utiliser la méthode standardisée de Lund et Browder (adulte ou "
         "pédiatrique) pour évaluer la SCB."),
        ("R1.2.1", "Requérir sans délai un avis spécialisé en cas de brûlure grave, afin "
         "d'envisager une hospitalisation en Centre de Traitement des Brûlés (CTB)."),
        ("R1.2.2", "Utiliser la télémédecine pour améliorer l'évaluation initiale du "
         "brûlé grave."),
        ("R1.2.3", "Si une hospitalisation en CTB est retenue, privilégier une admission "
         "directe en CTB."),
        ("R1.2.4", "Réaliser une escarrotomie si la brûlure profonde induit une "
         "hyperpression compartimentale des membres/du tronc compromettant voies "
         "aériennes, ventilation et/ou circulation — idéalement en CTB par un praticien "
         "expérimenté."),
    ], RCW))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>Repères :</b> méthode de Lund et Browder = référence (la règle des 9 de "
        "Wallace surestime et n'est pas adaptée à la pédiatrie) ; méthode de la paume + "
        "doigts du patient ≈ 1 % SCB, utile en première intention. Escarrotomie : indication "
        "urgente seulement si compromission des voies aériennes/ventilation/circulation ; "
        "sinon dans les 48 premières heures si hyperpression abdominale ou circulatoire.",
        S_BODY_SM))
    return story

def _section_champ2():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Champ 2 — Réanimation hémodynamique", color=RED),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("R2.1.1", "Administrer 20 mL/kg d'une solution cristalloïde IV dans la première "
         "heure de prise en charge si SCB ≥ 20 % (adulte) ou ≥ 10 % (enfant)."),
        ("R2.1.2", "Utiliser des solutions cristalloïdes balancées (type Ringer Lactate) "
         "dans la prise en charge du brûlé grave."),
        ("R2.2", "Utiliser, au-delà de la 1<sup>re</sup> heure, une formule d'estimation du "
         "remplissage initial intégrant au minimum le poids et la SCB pour définir les "
         "apports en cristalloïdes."),
        ("R2.3", "Ajuster dès que possible les volumes perfusés de réanimation liquidienne "
         "en fonction des données de l'évaluation hémodynamique."),
        ("R2.4", "Utiliser l'albumine humaine si SCB &gt; 30 %, au-delà des 6 premières "
         "heures de prise en charge."),
    ], RCW))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>Repères :</b> cible de diurèse usuelle 0,5-1 mL/kg/h (adulte et enfant), non "
        "formellement validée. Formules historiques citées par la source (détail non "
        "reproduit ici, cf. Annexe 4 — voir limite ci-dessus) : Evans, Baxter/Parkland, "
        "Pruitt/Brooke (2-4 mL/kg/%SCB de Ringer Lactate/24h) ; pédiatrie ≈ 6 mL/kg/%SCB, "
        "souvent Parkland modifié (3-4 mL/kg/%SCB) + règle des « 4-2-1 » pour l'entretien. "
        "Albumine : cible albuminémie &gt; 30 g/L, généralement 1-2 g/kg/j. Les hydroxyéthyl"
        "amidons (HEA) sont <b>contre-indiqués</b> chez le brûlé grave (EMA/ANSM).",
        S_BODY_SM))
    return story

def _section_champ1_2():
    story = _section_champ1()
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_champ2())
    return story

# ---------------------------------------------------------------------------
def _section_champ3():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Champ 3 — Voies aériennes et inhalation de fumées d'incendies", color=RED),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("R3.1.1", "Ne pas intuber systématiquement un patient avec une brûlure du visage "
         "ou du cou."),
        ("R3.1.2", "Intuber si brûlure de la totalité du visage <b>associée à</b> : "
         "(1) brûlure profonde et circulaire du cou, et/ou (2) symptômes d'obstruction des "
         "voies aériennes (voix modifiée, stridor, dyspnée laryngée), et/ou (3) brûlure "
         "très étendue (SCB ≥ 40 %)."),
        ("R3.2", "Ne pas réaliser de fibroscopie bronchique en cas de suspicion "
         "d'inhalation de fumées en dehors d'un centre spécialisé, pour ne pas retarder "
         "le transfert."),
        ("R3.3.1", "Ne pas administrer systématiquement d'hydroxocobalamine en cas "
         "d'inhalation de fumées."),
        ("R3.3.2", "Réserver l'hydroxocobalamine aux cas avec suspicion élevée "
         "d'intoxication majeure aux cyanures (adulte) ou modérée (enfant)."),
        ("R3.4", "Ne pas réaliser systématiquement une séance d'oxygénothérapie hyperbare "
         "en cas de suspicion d'intoxication au CO secondaire à une inhalation de fumées."),
    ], RCW))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>Repères :</b> hydroxocobalamine — dose adulte 5 g (10 g si arrêt cardiaque), "
        "dose enfant 70 mg/kg (max 5 g), en préhospitalier. Critères d'intoxication modérée "
        "chez l'enfant (déclenchant l'administration) : GCS ≤ 13, confusion, stridor, voix "
        "rauque, tachypnée, dyspnée, suie dans les voies aériennes ; critères sévères : "
        "GCS ≤ 8, convulsions, coma, mydriase, trouble hémodynamique sévère, collapsus, "
        "dépression respiratoire. Oxygénothérapie normobare (FiO<sub>2</sub> 100 %) "
        "recommandée sans délai 6-12 h en cas de suspicion/confirmation d'intoxication au "
        "CO — l'oxygénothérapie hyperbare reste non systématique chez l'adulte, y compris "
        "pour l'indication « traitement de la brûlure elle-même » évoquée par une source "
        "externe (ECMH 2016, Type 3/grade C) que les experts n'ont pas retenue.",
        S_BODY_SM))
    return story

def _section_champ4():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Champ 4 — Anesthésie et analgésie", color=RED),
        Spacer(1, 1.5 * mm),
        reco_table([
            ("R4.1.1", "Utiliser une analgésie multimodale, titrée sur des échelles "
             "validées d'évaluation du confort et de l'analgésie."),
            ("R4.1.2", "Utiliser la kétamine IV en titration pour les douleurs intenses "
             "induites par la brûlure, en association avec d'autres antalgiques."),
            ("R4.1.3", "Recourir à des techniques non pharmacologiques en association avec "
             "les antalgiques lors des pansements, chez le patient stable."),
        ], RCW),
    ]))
    return story

def _section_champ3_4():
    story = _section_champ3()
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_champ4())
    return story

# ---------------------------------------------------------------------------
def _section_champ5():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Champ 5 — Traitement local", color=RED),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("R5.1.1", "Refroidir les brûlures si SCB &lt; 20 % (adulte) ou &lt; 10 % (enfant), "
         "en l'absence d'état de choc."),
        ("R5.2", "Couvrir les zones brûlées dès la phase initiale, pour limiter "
         "l'hypothermie et le risque de contamination microbienne, jusqu'à l'avis "
         "spécialisé."),
        ("R5.3", "Ne pas administrer d'antibioprophylaxie systémique en dehors de la "
         "période périopératoire."),
    ], RCW))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>Repères :</b> refroidissement — durée optimale citée 20 minutes (eau ~15 °C), "
        "bénéfice persistant ~3 h ; seuil de SCB au-delà duquel la balance bénéfice/risque "
        "devient défavorable (non formellement établi) proposé par les experts à 10-15 % "
        "chez l'enfant, 20-25 % chez l'adulte (en l'absence de choc). Pansement : nettoyage "
        "mécanique (eau du robinet, sérum physiologique ou antiseptique) avant pansement ; "
        "sulfadiazine argentique associée à une moins bonne cicatrisation en usage prolongé "
        "sur brûlure superficielle ; antibiotiques topiques réservés à une infection "
        "cutanée confirmée.", S_BODY_SM))
    return story

def _section_champ6():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("Champ 6 — Traitements autres (nutrition, thromboprophylaxie)", color=RED),
        Spacer(1, 1.5 * mm),
        reco_table([
            ("R6.1", "Débuter un support nutritionnel dans les 12 heures suivant la "
             "brûlure, en privilégiant la voie orale ou entérale à la voie parentérale."),
            ("R6.2", "Administrer une thromboprophylaxie à la phase initiale chez le "
             "brûlé grave."),
        ], RCW),
    ]))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>Repères :</b> besoins énergétiques estimés par la formule de Toronto (adulte) "
        "ou de Schofield (enfant) — équations non reproduites ici, cf. limite ci-dessus ; "
        "besoins protéiques 1,5-2 g/kg/j (adulte), jusqu'à 3 g/kg/j (enfant) ; "
        "supplémentation en glutamine dès les premiers jours chez le grand brûlé. "
        "Thromboprophylaxie : incidence de MTEV sans prophylaxie 0,9-5,9 % (contre "
        "0,25-2,4 % avec prophylaxie) dans les cohortes rétrospectives ; les posologies "
        "nécessaires peuvent être supérieures aux doses usuelles (déficit en antithrombine "
        "III, volume de distribution et clairance augmentés) — un dosage de l'activité "
        "anti-Xa est suggéré. Pédiatrie : prophylaxie indiquée dès la puberté ou en cas de "
        "cathéter veineux central en place.", S_BODY_SM))
    return story

def _section_sources():
    story = []
    story.append(section_bar("Déclaration d'intérêts, sources et traçabilité", color=GREY))
    story.append(Spacer(1, 2 * mm))
    story.append(P(
        "<b>Déclaration d'intérêts (par société) :</b> SFAR — Mathieu Jeanne déclare un "
        "lien direct ou indirect avec les industriels MDMS, LOOS (France) ; Antoine "
        "Roquilly déclare être consultant pour MSD et bioMérieux. SFB — aucun. SFMU — "
        "Hugues Lefort déclare avoir participé à un comité scientifique du laboratoire "
        "Ethypharm. Adarpef — aucun. Aucun financement par une entreprise commercialisant "
        "un produit de santé.", S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>Document source :</b> « Prise en charge du brûlé grave à la phase aiguë chez "
        "l'adulte et l'enfant » — RPP SFAR, en association avec SFB/SFMU/Adarpef. "
        "Coordonnateurs d'experts : Matthieu Legrand (Paris), Damien Barraud (Metz). "
        "Organisateurs : Alice Blet, Etienne Gayat (Paris). Texte validé par le Comité "
        "des Référentiels Cliniques de la Sfar (15/05/2019) et le CA de la Sfar "
        "(24/05/2019). Champ : brûlures thermiques uniquement — brûlures électriques et "
        "chimiques explicitement hors champ (nécessitent un avis spécialisé dédié).",
        S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P("<b>Version :</b> 2019, 38 pages.", S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P("<b>Méthodologie :</b> RPP (GRADE pour l'analyse de la littérature ; "
                    "cotation Delphi pour l'accord — pas de grade 1+/2+ individuel) — voir "
                    "détail en page 1.", S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>URL source :</b> https://sfar.org/download/rpp-prise-en-charge-du-brule-grave/"
        "?wpdmdl=24465", S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>Couverture :</b> intégralité des 24 recommandations (texte + accord). "
        "<b>Non reproduit</b> — 10 annexes citées par la source (Lund &amp; Browder, "
        "formules/algorithmes de remplissage vasculaire adulte et pédiatrique, algorithme "
        "d'intubation, posologie hydroxocobalamine détaillée, choix des pansements, "
        "formules nutritionnelles de Toronto/Schofield) : absentes du fichier PDF "
        "téléchargé (0 image sur 38 pages hors logo, vérifié par inspection directe et "
        "rendu visuel de 9 pages cibles) — voir panneau d'avertissement en page 1. "
        "L'argumentaire détaillé de chaque recommandation (statistiques d'études, "
        "références bibliographiques) est volontairement condensé aux seuls repères "
        "cliniquement actionnables — se référer au texte intégral (228 références "
        "bibliographiques) pour le détail des études sources.", S_SOURCE))
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Avertissement — document de 2019 :</b> cette fiche de synthèse indépendante "
        "reprend l'intégralité des 24 recommandations du texte source, mais PAS le "
        "contenu de ses annexes (absentes du fichier source disponible, voir ci-dessus). "
        "Elle ne remplace pas le texte intégral et n'est ni éditée ni validée par la Sfar, "
        "la SFB, la SFMU ou l'Adarpef. Les protocoles de remplissage vasculaire, les "
        "posologies et les seuils d'indication ayant pu évoluer depuis 2019, se référer à "
        "un avis spécialisé (Centre de Traitement des Brûlés) et aux recommandations "
        "actualisées avant toute décision thérapeutique.",
        S_BODY_SM), bg=GREY_LIGHT, border=GREY))
    return story

def _section_champ5_6_sources():
    story = _section_champ5()
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_champ6())
    story.append(Spacer(1, 4 * mm))
    story.extend(_section_sources())
    return story

def _section_intro_champ1_2():
    story = _section_intro()
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_champ1_2())
    return story

def _section_intro_champ1_4():
    story = _section_intro_champ1_2()
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_champ3_4())
    return story

SECTIONS = [
    ("Méthodologie & Champ 1-4 — Admission, réanimation, voies aériennes, analgésie", _section_intro_champ1_4),
    ("Champ 5-6 — Traitement local, autres & sources", _section_champ5_6_sources),
]

def _make_doc(path=None):
    return SimpleDocTemplate(path or OUT, pagesize=A4,
                              leftMargin=MARGIN, rightMargin=MARGIN,
                              topMargin=32 * mm, bottomMargin=16 * mm,
                              title="Fiche SFAR 2019 - Brule grave a la phase aigue",
                              author="Synthèse indépendante (source SFAR/SFB/SFMU/Adarpef)")

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
