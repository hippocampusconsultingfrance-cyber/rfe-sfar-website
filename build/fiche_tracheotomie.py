# -*- coding: utf-8 -*-
"""
Fiche de synthese - RFE commune SRLF-SFAR (avec SFMU/SFORL), "Tracheotomie en reanimation".
Texte valide par le CA SFAR (15/12/2016) et le CA SRLF (13/12/2016), publie Anesth Reanim.
2018;4:508-522 (egalement publie en anglais dans Anaesth Crit Care Pain Med et Ann Intensive
Care). 16 experts + 2 coordonnateurs (SRLF, SFAR), avec la participation de la SFMU et de la
SFORL. Methode GRADE, format PICO. Champ EXPLICITEMENT exclu par la source elle-meme :
la gestion en urgence des voies aeriennes (traumatisme/brulure cervico-faciale) - la fiche ne
couvre donc que la tracheotomie PROGRAMMEE en reanimation chez l'adulte, disclose dans
l'intro.

Resume officiel : 18 recommandations (8 recommandations formalisees + 10 avis d'experts) et
3 protocoles de soins. Parmi les 8 recommandations formalisees : 2 GRADE1 (1+/1-), 6 GRADE2
(2+/2-). Mon propre inventaire independant, item par item (R1.1-R1.4, R2.1-R2.3, R3.1-R3.5,
R4.1-R4.3, R5.1-R5.3 = 18), concorde exactement avec ce total et cette repartition GRADE1/2 -
PAS de mismatch d'agregat pour ce document (troisieme document du corpus, apres LAT et SDRA,
avec une concordance totale y compris sur la repartition GRADE).

BUG D'EXTRACTION CONFIRME (variante deja rencontree plusieurs fois dans ce corpus - glyphe
moins disparaissant a l'extraction PDF->texte) : R1.3 et R3.2 sont imprimes dans la source
"(Grade 1-)" et "(Grade 2-)" respectivement (verifie par rendu image 200dpi des pages 5 et 7 du
PDF source) mais l'extraction texte automatique affiche seulement "(Grade 1)" et "(Grade 2)"
sans le signe moins - corrige ici en utilisant le signe reellement imprime, confirme visuellement,
pas par inference du sens de la phrase (bien que le sens - "il ne faut (probablement) pas..." -
soit egalement coherent avec un signe negatif).

3 protocoles de soins (avis d'experts, tous integralement extractibles en texte SAUF un element
graphique) : protocole associe a R3.5 (tracheotomie percutanee standardisee : materiel/
personnel/preparation/conditions de realisation/apres canulation - texte integral) ; protocole
associe a R4.1 (soins post-tracheotomie : immediats/premiers jours 0-4j/a distance - texte
integral) ; protocole associe a R5.1 (decanulation, d'apres Warnecke et al. Crit Care Med 2013 -
prerequis/conditions d'examen en texte integral, PLUS un algorithme sequentiel en 5 etapes
(etat des secretions salivaires -> deglutition spontanee -> sensibilite laryngee/toux ->
deglutition bolus consistant -> deglutition bolus liquide -> decanulation, chaque etape ayant une
branche "Si OUI = pas de decanulation") qui est une image (page 11 du PDF source, verifiee par
rendu 200dpi) - transcrit ici en tableau sequentiel.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from style import *
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.units import mm

OUT = "/private/tmp/claude-501/-Users-macbook-Downloads-claude/65498e3e-5ddf-47a6-b100-3ac535d1faa0/scratchpad/rfe_sfar/output/Fiche_SRLF_SFAR_Tracheotomie_2016.pdf"

SOURCE_TXT = ("Source : Recommandations Formalisées d'Experts (RFE) communes SRLF-SFAR, avec "
              "la participation de la SFMU et de la SFORL « Trachéotomie en réanimation » — "
              "texte validé par le CA SFAR (15/12/2016) et le CA SRLF (13/12/2016), publié "
              "Anesth Reanim. 2018;4:508-522. Fiche de synthèse non officielle : se référer au "
              "texte intégral.")

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

def no_reco_panel(text):
    return info_panel(P("<b>Absence de recommandation</b> — " + text, S_BODY_SM), bg=GREY_LIGHT, border=GREY)

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

TOTAL_PAGES = {"n": 8}

def on_page(canvas, doc, page_title):
    header_band(canvas, doc, "SRLF / SFAR — RFE 2016 — FICHE DE SYNTHÈSE",
                "Trachéotomie en réanimation",
                page_title, icon_fn=lambda c,x,y: icon_shield(c, x, y, 13*mm), color=NAVY)
    footer_band(canvas, doc, SOURCE_TXT, f"Page {doc.page} / {TOTAL_PAGES['n']}")

# ---------------------------------------------------------------------------
def _section_intro():
    story = []
    story.append(Spacer(1, 3*mm))
    story.append(info_panel(P(
        "<b>Objectif :</b> RFE commune SRLF-SFAR, avec la participation de la SFMU et de la "
        "SFORL — 16 experts + 2 coordonnateurs, méthode GRADE, format PICO. 5 champs : "
        "(1) indications et contre-indications, (2) techniques de mise en place, "
        "(3) conditions nécessaires à la réalisation, (4) prise en charge du patient "
        "trachéotomisé, (5) décanulation.<br/><br/>"
        "<b>Champ explicitement exclu par la source :</b> la gestion en urgence des voies "
        "aériennes (médecine d'urgence, traumatisme ou brûlure cervico-faciale) — ces "
        "recommandations ne couvrent que la <b>trachéotomie programmée</b> en réanimation "
        "chez l'adulte.<br/><br/>"
        "<b>Résultats (résumé officiel) :</b> 18 recommandations (8 recommandations "
        "formalisées + 10 avis d'experts) et 3 protocoles de soins. Parmi les 8 "
        "recommandations formalisées : 2 GRADE 1 (1+/1-), 6 GRADE 2 (2+/2-). Accord fort "
        "pour l'ensemble après 2 tours de cotation et divers amendements.",
        S_BODY), bg=BG_PANEL, border=TEAL))
    story.append(Spacer(1, 3*mm))
    story.append(info_panel(P(
        "<b>Contexte :</b> grandes disparités de pratique selon les équipes (fréquence 5 à "
        "54 %, modalité chirurgicale ou percutanée). Avantages potentiels : réduction des "
        "lésions pharyngolaryngées, moindre risque de sinusite, réduction des besoins de "
        "sédation, hygiène bucco-pharyngée facilitée, confort et communication améliorés, "
        "soins infirmiers facilités, sevrage ventilatoire facilité. Complications les plus "
        "fréquentes mineures (saignement péri-orificiel) ; complications rares mais graves "
        "possibles (lésion du tronc artériel brachiocéphalique). Les essais randomisés "
        "récents n'ont pas confirmé les bénéfices historiquement rapportés (mortalité, "
        "durée de VM/séjour) associés à une réalisation précoce.",
        S_BODY_SM), bg=GREY_LIGHT, border=GREY))
    story.append(Spacer(1, 3*mm))
    story.append(info_panel(P(
        "<b>Note de correction d'extraction (disclosure) :</b> R1.3 et R3.2 sont imprimés "
        "dans la source « (Grade 1-) » et « (Grade 2-) » respectivement — confirmé par rendu "
        "visuel des pages sources — mais l'extraction automatique du texte PDF perd le signe "
        "« moins » pour ces deux tags (bug d'extraction déjà rencontré à plusieurs reprises "
        "dans ce corpus). Corrigé ici avec le signe réellement imprimé.",
        S_BODY_SM), bg=AMBER_LIGHT, border=AMBER))
    return story

def _section_champ1():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Champ 1 — Indications et contre-indications"))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("R1.1", "Les experts suggèrent que la trachéotomie soit proposée en cas de sevrage "
         "ventilatoire prolongé et de pathologie neuromusculaire acquise et potentiellement "
         "réversible (ex. Guillain-Barré, neuromyopathie acquise en réanimation, myasthénie, "
         "myélite lupique).", "AE"),
        ("R1.2", "Les experts suggèrent que l'indication de la trachéotomie chez les "
         "patients ayant une insuffisance respiratoire chronique fasse l'objet d'une "
         "concertation multidisciplinaire.", "AE"),
        ("R1.3", "Il ne faut pas réaliser de trachéotomie en réanimation avant le "
         "quatrième jour de ventilation mécanique.", "1-"),
        ("R1.4", "Les experts suggèrent que la trachéotomie (percutanée ou chirurgicale) ne "
         "soit pas réalisée en réanimation dans les situations à haut risque de "
         "complication.", "AE"),
    ], [13*mm, PAGE_W-2*MARGIN-13*mm-18*mm, 18*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(info_panel(P(
        "<b>R1.4 — Situations à haut risque de complication (contre-indications) :</b> "
        "instabilité hémodynamique • hypertension intracrânienne avec PIC &gt;15 mmHg • "
        "hypoxémie sévère (PaO2/FiO2 &lt;100 mmHg sous PEP &gt;10 cmH2O) • troubles de "
        "l'hémostase non corrigés (plaquettes &lt;50 000/mm³ et/ou INR &gt;1,5 et/ou "
        "TCA &gt;2× la normale) • refus du patient et/ou de la famille • patient moribond "
        "ou suivant une procédure de limitation des thérapeutiques actives.",
        S_BODY_SM), bg=BG_PANEL, border=TEAL))
    story.append(Spacer(1, 2*mm))
    story.append(P("R1.1 : aucune étude n'a démontré formellement un bénéfice sur le "
                    "pronostic vital dans les pathologies neuromusculaires ; trachéotomie "
                    "envisageable si sevrage non effectif &gt;7 jours après la première "
                    "épreuve de ventilation spontanée. Guillain-Barré : à n'envisager qu'en "
                    "l'absence de sevrage effectif au décours de l'immunothérapie — déficit "
                    "de flexion du pied + bloc moteur sciatique prédictifs d'une VM longue "
                    "(&gt;15j) dans 100 % des cas. R1.2 : enjeux éthiques majeurs en SLA — la "
                    "trachéotomie ne modifie pas le pronostic de la maladie causale, à "
                    "discuter avec le patient/les proches et l'équipe référente. R1.3 : "
                    "études prospectives de bonne qualité — la trachéotomie précoce "
                    "(&lt;4e jour) n'est associée ni à une réduction de mortalité, ni de "
                    "l'incidence des PAVM, ni de la durée de VM ; réduirait la consommation "
                    "d'hypnotiques ; les patients brûlés/traumatisés cervico-faciaux relèvent "
                    "de la trachéotomie en urgence, hors champ de cette RFE.", S_NOTE))
    return story

def _section_champ2():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Champ 2 — Techniques de mise en place"))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("R2.1", "Il faut privilégier la trachéotomie percutanée comme la méthode standard "
         "de réalisation d'une trachéotomie chez les patients de réanimation.", "1+"),
        ("R2.2", "Les experts suggèrent qu'une concertation médicochirurgicale décide de la "
         "technique de trachéotomie à utiliser en cas de situation à risque de "
         "complication.", "AE"),
        ("R2.3", "Il faut probablement privilégier la technique de trachéotomie percutanée "
         "par dilatation unique progressive comme la méthode standard de réalisation d'une "
         "trachéotomie percutanée chez les patients de réanimation.", "2+"),
    ], [13*mm, PAGE_W-2*MARGIN-13*mm-18*mm, 18*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(P("R2.1 : méta-analyse 2014 (14 ECR) — aucune supériorité en mortalité ou "
                    "complications majeures entre percutanée et chirurgicale, mais la "
                    "percutanée est associée à un temps de réalisation plus court et moins "
                    "d'infections/inflammation de l'orifice ; nécessite une formation "
                    "préalable des opérateurs. R2.2 : contre-indications relatives à la "
                    "percutanée — rachis cervical instable, plaie/infection cervicale, cou "
                    "remanié (chirurgie/radiothérapie), difficulté de repérage anatomique "
                    "(obésité, cou court), raideur du rachis cervical ; envisageable par une "
                    "équipe expérimentée avec moyens techniques adaptés (fibroscopie, "
                    "échographie-Doppler, kits spéciaux). R2.3 : parmi 6 techniques de "
                    "dilatation percutanée comparées, la dilatation unique progressive a un "
                    "taux d'échec plus faible que la dilatation rotatoire et un taux de "
                    "complications mineures plus faible que la dilatation par ballonnet ou à "
                    "la pince sur guide — seule la trachéotomie trans-laryngée est associée à "
                    "un taux d'échec et de complications majeures supérieur aux autres "
                    "techniques.", S_NOTE))
    return story

def _section_champ3():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Champ 3 — Conditions de réalisation"))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("R3.1", "Il faut probablement réaliser une fibroscopie avant et pendant la "
         "réalisation de la trachéotomie percutanée.", "2+"),
        ("R3.2", "Il ne faut probablement pas recourir à la pose d'un masque laryngé "
         "pendant la réalisation de la trachéotomie percutanée en réanimation.", "2-"),
        ("R3.3", "Il faut probablement réaliser une échographie cervicale lors de la "
         "réalisation d'une trachéotomie percutanée en réanimation.", "2+"),
        ("R3.4", "Les experts suggèrent de ne pas prescrire d'antibioprophylaxie lors de la "
         "réalisation de la trachéotomie.", "AE"),
        ("R3.5", "Les experts suggèrent qu'une procédure standardisée soit mise en place "
         "dans les services de réanimation pratiquant des trachéotomies percutanées.", "AE"),
    ], [13*mm, PAGE_W-2*MARGIN-13*mm-18*mm, 18*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(P("R3.1 : seul essai randomisé disponible (60 patients) — réduction de "
                    "47 % des complications précoces avec fibroscopie (IC95 23-64), et moins "
                    "de ponctions nécessaires. R3.2 : méta-analyse 2014 (8 ECR) — le masque "
                    "laryngé ne réduit ni mortalité, ni complications, ni échecs (preuve "
                    "basse) ; seul le temps de procédure est réduit (-1,46 min) ; un essai "
                    "postérieur retrouve davantage de conversions et de complications "
                    "significatives avec le masque laryngé. R3.3 : 4 ECR ouverts (560 "
                    "patients) — réduction du risque de complication de 44 % (IC95 21-60) "
                    "avec échographie-Doppler, succès au 1er essai 94,9 % vs. 82,9 % sans ; "
                    "niveau 2+ malgré les ECR du fait de la qualité variable des essais et de "
                    "l'usage encore peu répandu de la technique. R3.4 : chirurgie propre "
                    "contaminée, taux d'infection du site 0-4 % pour la percutanée (contre "
                    "plus élevé pour la chirurgicale) ; absence d'ECR évaluant "
                    "l'antibioprophylaxie, preuve très faible ; cohérent avec la conférence "
                    "d'actualisation SFAR 2010 sur l'antibioprophylaxie.", S_NOTE))
    story.append(Spacer(1, 3*mm))
    story.append(section_bar("Protocole de soins associé à R3.5 (avis d'experts) — Trachéotomie percutanée standardisée", color=GREY))
    story.append(Spacer(1, 2*mm))
    story.append(info_panel(P(
        "<b>Matériel :</b> fibroscope bronchique (avec vidéo si possible) • kit de "
        "trachéotomie percutanée • matériel de réintubation • échographe (si expertise "
        "disponible) • monitorage hémodynamique et ventilatoire • hémostase vérifiée (et "
        "corrigée en cas d'anomalie).<br/>"
        "<b>Personnel :</b> 2 médecins (1 opérateur + 1 pour la fibroscopie) • au moins "
        "1 personnel paramédical.<br/>"
        "<b>Préparation :</b> patient intubé et ventilé en mode volumétrique contrôlé sous "
        "FiO2=1 • anesthésie générale avec curarisation • extrémité céphalique en "
        "hyperextension (billot sous les omoplates) • préparation cutanée du champ "
        "opératoire.<br/>"
        "<b>Conditions de réalisation :</b> repérage du point de ponction par palpation et "
        "transillumination (échographie en complément si expertise disponible), idéalement "
        "entre 1er et 2e anneaux • retrait de la sonde d'intubation sous contrôle de la vue, "
        "immobilisation en position sous-glottique, ballonnet gonflé • compenser la fuite "
        "ventilatoire si besoin • ponction trachéale sous contrôle de la vue • poursuite "
        "selon la technique choisie, sous contrôle de la vue • mise en place de la canule "
        "sous contrôle de la vue.<br/>"
        "<b>Après canulation :</b> connexion au ventilateur et ajustement de la ventilation "
        "• maintien/sécurisation de la canule (dispositif adapté à l'état cutané) • "
        "vérification de la position par fibroscopie, toilette bronchique si besoin • "
        "rédaction d'un compte rendu de trachéotomie.",
        S_BODY_SM), bg=BG_PANEL, border=TEAL))
    return story

def _section_champ4():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Champ 4 — Prise en charge du patient trachéotomisé"))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("R4.1", "Les experts suggèrent que les services de réanimation disposent d'un "
         "protocole de soins définissant la gestion de la trachéotomie.", "AE"),
        ("R4.2", "Les experts suggèrent de réaliser une humidification des voies aériennes "
         "chez les patients ayant une trachéotomie en réanimation.", "AE"),
        ("R4.3", "Les experts suggèrent de ne pas changer la canule de trachéotomie de "
         "façon systématique en réanimation.", "AE"),
    ], [13*mm, PAGE_W-2*MARGIN-13*mm-18*mm, 18*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(P("R4.1 : complications secondaires nombreuses (infection cutanée, "
                    "granulome, hémorragie secondaire, sténose trachéale, trachéomalacie, "
                    "érosion vasculaire) ; pression du ballonnet à surveiller sans dépasser "
                    "30 cmH2O (contrôle toutes les 8h) — trop basse : risque d'inhalation ; "
                    "trop élevée : ischémie muqueuse trachéale/sténose. R4.2 : "
                    "recommandations anglaises 2014 — humidification à envisager chez tout "
                    "patient trachéotomisé, adaptée au support ventilatoire et à l'importance "
                    "des sécrétions ; données contradictoires entre les 2 seules études "
                    "disponibles comportant des patients trachéotomisés. R4.3 : aucune donnée "
                    "sur le délai optimal de changement ; pratiques très variables (80 % de "
                    "changement systématique aux USA vs. 60 % des services ne changeant "
                    "jamais aux Pays-Bas) ; changement précoce associé à des risques "
                    "(canulation aberrante, arrêt respiratoire) — à guider par la clinique "
                    "(suspicion d'infection locale, saignement, réduction de calibre pour la "
                    "phonation).", S_NOTE))
    story.append(Spacer(1, 3*mm))
    story.append(section_bar("Protocole de soins associé à R4.1 (avis d'experts) — Gestion de la trachéotomie", color=GREY))
    story.append(Spacer(1, 2*mm))
    cw = PAGE_W - 2*MARGIN
    story.append(simple_table(
        ["Période", "Contenu"],
        [
            ["Soins post-trachéotomie immédiats", "Personnel formé à la gestion de la "
             "trachéotomie • vérification de la position (extrémité de la canule à 4-6 cm de "
             "la carène) et de la fixation (sutures/cordons/velcro, amplitude limitée à "
             "1 doigt) • contrôle de l'accès aux voies aériennes (aspiration trachéale "
             "aisée, ETCO2, pressions de crête vs. valeurs pré-trachéotomie, absence "
             "d'emphysème sous-cutané, stabilité hémodynamique, position par radiographie de "
             "thorax) • pression du ballonnet &lt;30 cmH2O (25-35 selon les équipes) • "
             "matériel de ré-intubation et de trachéotomie à proximité immédiate."],
            ["Premiers jours (0-4j)", "Surveillance de signes hémorragiques toutes les 3h en "
             "postopératoire • examen de la cicatrice (signes d'infection locale) • "
             "pansement refait au sérum physiologique 3×/24h • aspiration trachéale selon "
             "les pratiques, en mesurant la profondeur maximale • humidification des voies "
             "aériennes (humidificateur chauffant si besoin), soins de la canule interne si "
             "chemisée • tête surélevée à 30° et position médiane, préserver l'axe tête-tronc "
             "lors des mobilisations • absence de tension des tuyaux du respirateur sur la "
             "trachéotomie."],
            ["Soins à distance", "Changement de la fixation tous les jours (ou plus souvent "
             "si suintement) • contrôle de la cicatrice tous les jours • soins au sérum "
             "salé isotonique."],
        ],
        [cw*0.22, cw*0.78]))
    return story

def _section_champ5():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Champ 5 — Décanulation"))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("R5.1", "Les experts suggèrent qu'un protocole multidisciplinaire de décanulation "
         "soit disponible dans les services de réanimation.", "AE"),
        ("R5.2", "Il faut probablement envisager de dégonfler le ballonnet de la canule de "
         "trachéotomie lorsque les patients sont en ventilation spontanée.", "2+"),
        ("R5.3", "Il faut probablement réaliser un examen pharyngolaryngé lors ou "
         "au-décours de la décanulation.", "2+"),
    ], [13*mm, PAGE_W-2*MARGIN-13*mm-18*mm, 18*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(P("R5.2 : nombreuses études observationnelles/avant-après — diminution de "
                    "la durée de sevrage, du taux d'échec de décanulation et des "
                    "complications avec un protocole ; ECR monocentrique (195 patients) "
                    "confirmant l'impact du dégonflage précoce dès séparation du "
                    "ventilateur. R5.3 : étude prospective observationnelle comparative en "
                    "aveugle (100 patients neurologiques) — l'examen fibroscopique "
                    "laryngo-trachéal systématisé a permis la décanulation de 27 patients "
                    "pour lesquels l'évaluation clinique seule pronostiquait un échec "
                    "(taux de recanulation 1,9 %) ; autres études : incidence plus élevée de "
                    "troubles de la déglutition chez les patients trachéotomisés/ventilés "
                    "prolongés, et risque accru d'inhalation/lésions pharyngolaryngées en "
                    "cas de trachéotomie prolongée ou de retard de décanulation.", S_NOTE))
    story.append(Spacer(1, 3*mm))
    story.append(section_bar("Protocole de soins associé à R5.1 (avis d'experts) — Décanulation (d'après Warnecke et al., Crit Care Med 2013)", color=GREY))
    story.append(Spacer(1, 2*mm))
    story.append(info_panel(P(
        "<b>Prérequis :</b> sevrage de la ventilation mécanique 24h/24 en cas de pathologie "
        "neurologique préalable.<br/>"
        "<b>Conditions d'examen :</b> ballonnet dégonflé • aspiration préalable des "
        "sécrétions • position assise &gt;70° • aucune anesthésie (pour ne pas générer de "
        "troubles de déglutition) • endoscopie par voie narinaire jusqu'au ballonnet.",
        S_BODY_SM), bg=BG_PANEL, border=TEAL))
    story.append(Spacer(1, 2*mm))
    cw = PAGE_W - 2*MARGIN
    story.append(KeepTogether(simple_table(
        ["Étape (séquentielle)", "Critère évalué / seuil", "Si signe positif"],
        [
            ["1. État des sécrétions salivaires", "Stagnation massive, inhalation occulte",
             "Pas de décanulation"],
            ["2. Déglutition spontanée", "&lt;1/minute, pas de voile blanc",
             "Pas de décanulation"],
            ["3. Sensibilité laryngée / toux", "Anesthésie, pas de toux efficace",
             "Pas de décanulation"],
            ["4. Déglutition bolus consistant", "Type « purée » — inhalation occulte du "
             "bolus", "Pas de décanulation"],
            ["5. Déglutition bolus liquide", "Inhalation occulte sans déclenchement de la "
             "déglutition", "Pas de décanulation"],
            ["→ Décanulation", "Si les 5 étapes sont franchies sans signe positif (« Si "
             "NON » à chaque étape)", "—"],
        ],
        [cw*0.28, cw*0.52, cw*0.20])))
    return story

def _section_synthese():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Synthèse et messages clés"))
    story.append(Spacer(1, 2*mm))
    story.append(P(
        "• Champ d'application : trachéotomie <b>programmée</b> chez l'adulte en "
        "réanimation — la trachéotomie en urgence (traumatisme/brûlure cervico-faciale) est "
        "hors champ de cette RFE.<br/>"
        "• Indications : sevrage ventilatoire prolongé, pathologie neuromusculaire acquise "
        "potentiellement réversible (avis d'experts) ; insuffisance respiratoire chronique — "
        "concertation multidisciplinaire requise, enjeux éthiques majeurs (SLA notamment). "
        "Ne pas réaliser avant le 4e jour de ventilation mécanique (recommandation forte) ni "
        "en cas de situation à haut risque de complication (instabilité hémodynamique, HTIC "
        "&gt;15mmHg, hypoxémie sévère, troubles de l'hémostase non corrigés, refus, patient "
        "moribond/LAT).<br/>"
        "• Technique : trachéotomie percutanée à privilégier en 1ère intention "
        "(recommandation forte), par dilatation unique progressive (probablement "
        "recommandé) ; concertation médicochirurgicale si situation anatomique à risque. "
        "Fibroscopie et échographie cervicale probablement recommandées pour sécuriser le "
        "geste ; masque laryngé probablement à éviter ; pas d'antibioprophylaxie "
        "systématique.<br/>"
        "• Une procédure standardisée (protocole n°1) et un protocole de soins définissant "
        "la gestion de la trachéotomie (protocole n°2, incluant pression du ballonnet "
        "&lt;30 cmH2O) sont suggérés dans chaque service pratiquant des trachéotomies "
        "percutanées. Humidification des voies aériennes suggérée ; pas de changement "
        "systématique de canule (à guider par la clinique).<br/>"
        "• Décanulation : protocole multidisciplinaire suggéré (protocole n°3, algorithme "
        "séquentiel en 5 étapes d'après Warnecke et al.) ; dégonflage du ballonnet en "
        "ventilation spontanée et examen pharyngolaryngé lors/au décours de la décanulation "
        "probablement recommandés.",
        S_BODY))
    story.append(Spacer(1, 5*mm))

    story.append(section_bar("Sources et traçabilité", color=GREY))
    story.append(Spacer(1, 2*mm))
    story.append(P(
        "<b>Document source :</b> « Trachéotomie en réanimation » — Recommandations "
        "Formalisées d'Experts communes SRLF-SFAR, avec la participation de la SFMU et de la "
        "SFORL. Texte validé par le CA SFAR (15/12/2016) et le CA SRLF (13/12/2016), publié "
        "Anesth Reanim. 2018;4:508-522. 16 experts + 2 coordonnateurs, coordination "
        "J-L. Trouillet (SRLF), O. Collange (SFAR).", S_SOURCE))
    story.append(Spacer(1, 1.5*mm))
    story.append(P("<b>Couverture :</b> les 18 recommandations numérotées (R1.1-R1.4, "
                    "R2.1-R2.3, R3.1-R3.5, R4.1-R4.3, R5.1-R5.3) et les 3 protocoles de soins "
                    "associés (R3.5, R4.1, R5.1) sont reproduits intégralement. Concordance "
                    "exacte avec le résumé officiel sur le total (18 = 8 recommandations "
                    "formalisées + 10 avis d'experts) et sur la répartition GRADE (2 GRADE1 + "
                    "6 GRADE2) — aucun mismatch d'agrégat à signaler pour ce document.", S_SOURCE))
    story.append(Spacer(1, 1.5*mm))
    story.append(P("<b>Correction d'extraction :</b> R1.3 et R3.2 sont imprimés dans la "
                    "source « (Grade 1-) » et « (Grade 2-) » (confirmé par rendu visuel des "
                    "pages sources aux emplacements exacts) ; l'extraction automatique du "
                    "texte PDF perd le signe « moins » pour ces deux tags — corrigé ici avec "
                    "le signe réellement imprimé.", S_SOURCE))
    story.append(Spacer(1, 1.5*mm))
    story.append(P("<b>Figure/algorithme :</b> le protocole de décanulation associé à R5.1 "
                    "comporte un algorithme séquentiel en 5 étapes (image, page 11 du texte "
                    "source, d'après Warnecke et al. Crit Care Med 2013), vérifié par rendu "
                    "visuel et transcrit ici en tableau séquentiel.", S_SOURCE))
    story.append(Spacer(1, 3*mm))
    story.append(info_panel(P(
        "<b>Avertissement :</b> ce document est une fiche de synthèse indépendante, produite "
        "pour un usage d'aide-mémoire. Il reprend l'intégralité des recommandations de la "
        "RFE mais ne remplace pas le texte intégral et n'est ni édité ni validé par la "
        "SRLF/SFAR. En cas de doute, se référer au texte intégral, aux recommandations "
        "ultérieures et/ou à un avis spécialisé.",
        S_BODY_SM), bg=GREY_LIGHT, border=GREY))
    return story

def _section_intro_champ1():
    return _section_intro() + [Spacer(1, 4*mm)] + _section_champ1()

def _section_champ2_champ3():
    return _section_champ2() + [Spacer(1, 4*mm)] + _section_champ3()

SECTIONS = [
    ("Introduction & Champ 1 — Indications et contre-indications", _section_intro_champ1),
    ("Champ 2 — Techniques & Champ 3 — Conditions de réalisation", _section_champ2_champ3),
    ("Champ 4 — Prise en charge du patient trachéotomisé", _section_champ4),
    ("Champ 5 — Décanulation", _section_champ5),
    ("Synthèse, sources & traçabilité", _section_synthese),
]

def _make_doc():
    return SimpleDocTemplate(OUT, pagesize=A4,
                              leftMargin=MARGIN, rightMargin=MARGIN,
                              topMargin=32*mm, bottomMargin=16*mm,
                              title="Fiche SRLF-SFAR 2016 - Tracheotomie en reanimation",
                              author="Synthèse indépendante (source SRLF/SFAR)")

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
