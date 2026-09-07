# -*- coding: utf-8 -*-
"""
Fiche de synthese - SRLF et SFAR (2008) "Securisation des procedures a risques en
reanimation : risque infectieux exclu" - Recommandations d'experts sur les pratiques de
securite pour les patients de reanimation (safety practices). C. Gervais, L. Donetti,
F. Bonnet, C. Ichai, F. Jacobs, et les Groupes d'experts de la SRLF et de la SFAR. Annales
Francaises d'Anesthesie et de Reanimation 27 (2008) e43-e51, doi:10.1016/j.annfar.2008.09.005,
disponible en ligne le 31 octobre 2008. Source : sources/securisation_proc.pdf (9 pages) /
.txt (texte extrait integral, 923 lignes).

Pas de tampon d'obsolescence sur la page 1 du PDF source (verifie a la lecture integrale
du texte extrait) ; library_final.json marque ce document "en vigueur".

METHODOLOGIE - UN SEUL AXE, PAS DE GRADE : methode SRLF-SFAR derivee de la RAND/UCLA
appropriateness method (RAM), echelle continue de cotation 1 a 9 par chaque expert
(1 = desaccord total, 9 = accord total). Trois zones selon la position de la mediane :
(1-3) desaccord, (4-6) indecision, (7-9) accord. L'accord (ou le desaccord) est dit
"fort" si l'intervalle de la mediane reste a l'interieur d'une des trois zones, "faible"
dans le cas contraire. AUCUN grade de preuve 1+/1-/2+/2- n'est utilise dans ce document.

QUATRIEME CATEGORIE EXPLICITE - ZONE D'INDECISION : le document liste explicitement, en
toute fin de texte (avant les references), "les trois propositions suivantes [qui] ont
ete scorees par les experts dans la zone d'indecision" (corticoides IV avant extubation,
guide echangeur avant extubation prevue, monitorage de la precharge lors d'une depletion
a risque). Categorie disclosee ici comme un troisieme niveau a part entiere ("Indecision"),
JAMAIS reclassee arbitrairement en "Fort" ou "Faible" - il s'agit d'une cotation
explicitement distincte imprimee par les auteurs eux-memes.

DISCLOSURE - PROPOSITIONS SANS TAG D'ACCORD EXPLICITE (incoherence source-interne,
jamais silencieusement resolue) : dans le Champ 3.1 "Structures", une serie de cinq
phrases consecutives (identitovigilance, informatisation du dossier medical et de la
prescription, dispensation medicamenteuse personnalisee, disponibilite des resultats
d'examens biologiques/imagerie dans le service, procedure partagee de transmission des
resultats urgents) suit un item explicitement tagge "(accord fort)" SANS reprendre
elle-meme de tag - verifie par lecture integrale et par grep cible (aucune occurrence de
"accord" entre les lignes 159 et 168 du texte extrait). Ces cinq lignes sont retranscrites
ici avec un chip "?" (non cote dans la source), plutot que rattachees par extrapolation a
l'accord fort qui precede - fidelite a la source exigee par la consigne de tache.

COMPTAGE - 118 occurrences du tag "(accord fort)" ou "(accord faible)" dans le texte
source (grep exhaustif : `grep -nio "(accord fort)\\|(accord faible)"`), consolidees en
~180 lignes de tableau distinctes une fois les listes a puces sous un meme banniere
d'accord decomposees en items individuels quand ils portent un contenu clinique distinct,
et regroupees en une seule ligne quand elles ne sont que les sous-etapes d'une seule
checklist/procedure (meme convention que fiche_mal_epileptique.py) - JAMAIS deux tags
differents fusionnes dans une meme ligne. Les 5 propositions non cotees (Champ 3.1) et
les 3 propositions de la zone d'indecision s'ajoutent a ce total.

PERIMETRE - 8 champs : (1) taxonomie generale EI/EPR + indicateurs, (2) epidemiologie,
(3) procedures structurelles et manageriales (structures, activite, organisation du
travail medical/soignant, protocoles, culture securite, tableau de bord), (4) securisation
du materiel/dispositifs medicaux, (5) ventilation mecanique (intubation, tracheotomie, VM
invasive, sevrage, extubation, VNI), (6) "procedures circulatoires" (medicaments
vasoactifs, catheters arteriels/veineux centraux/arteriels pulmonaires), (7) epuration
extra-renale, (8) specificites pediatriques - TOUS couverts, plus la zone d'indecision
finale. Champ intitule "risque infectieux exclu" des le titre du document : ce perimetre
est rappele explicitement dans le panneau d'introduction (jamais omis silencieusement).

CONVENTION DE CHIP : extension locale non invasive de GRADE_COLORS - "Fort" -> vert,
"Faible" -> teal (meme convention que fiche_mal_epileptique.py/fiche_nutrition.py, seules
autres fiches de ce corpus a un seul axe accord fort/faible sans niveau de preuve GRADE) ;
"Indecision" -> ambre (categorie distincte, jamais confondue avec "faible") ; "?" -> gris
(deja la couleur par defaut de ce chip dans style.py, reprise ici pour les 5 propositions
non cotees du Champ 3.1).

ICONE : icon_shield (bouclier/securite), theme naturel pour un texte centre sur la
securisation des procedures a risque - deja utilise par fiche_transport_intrahospitalier.py
pour un theme apparente (autre document, aucun conflit).

AUDIT INDEPENDANT (agent en aveugle, texte source seul) - constats reconcilies :
- Fixe : le sevrage difficile (Champ 5.4) utilise "AI +/- PEP" (avec ou sans PEP) dans la
  source, pas "AI + PEP" - corrige apres l'audit (2 occurrences).
- Verifie visuellement sur le PDF source a 220dpi (pages e46/e47/e48/e50) et confirme
  EXACT tel quel dans ce script, malgre des artefacts d'extraction texte qui auraient pu
  suggerer une erreur : tete du lit "(> 30 degres)", PEP externe "(<= 5 cmH2O)", dobutamine
  "(<= 5 microg/kg/min)", dilution catecholamines pediatriques "dose (microg/min)" - CE
  DERNIER POINT est notable : l'extraction texte brute affichait "(mg/min)" pour la
  dilution pediatrique (confusion d'unite qui aurait ete cliniquement dangereuse si
  reproduite telle quelle), mais le rendu visuel du PDF confirme sans ambiguite "microg/min".
- Non corrige (curiosite source, sans impact sur le contenu) : Champ 5.1 (avant intubation)
  et Champ 5.6 (VNI) portent chacun un tag "(accord fort)" de bandeau PUIS un re-tag
  individuel redondant "(accord fort)" sur un item du meme bloc - lu ici comme une simple
  emphase redondante de l'auteur (le meme motif apparait deux fois dans le document), pas
  comme une rupture de portee ; le dernier item de 5.6 (arret de la VNI, sans tag propre)
  est donc conserve sous "Fort" (couverture du bandeau de section), non reclasse en "?".
- Disclosure : Champ 7 (EER) renvoie aux recommandations du CLIN sur le risque infectieux
  des catheters veineux centraux, alors meme que le titre du document annonce "risque
  infectieux exclu" - reference telle quelle (renvoi a un referentiel connexe), non
  retiree ni reinterpretee.

_count_pages() : implementation copiee a l'identique de fiche_aap_programmee.py - les
passes de comptage ecrivent vers un tempfile.mktemp() jetable, jamais vers OUT (bug de
corruption du header_band de la page 1 deja documente si l'on reutilise OUT pour le
comptage ET la construction finale).
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from style import *
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.units import mm

# Local, non-invasive extension of the shared GRADE_COLORS dict - no collision with
# existing keys ("1+","1-","2+","2-","AE","?").
GRADE_COLORS["Fort"] = (GREEN, WHITE)
GRADE_COLORS["Faible"] = (TEAL, WHITE)
GRADE_COLORS["Indécision"] = (AMBER, WHITE)

OUT = "/home/user/rfe-sfar-website/output/Fiche_SRLF_SFAR_Securisation_Procedures_Risque_2008.pdf"

SOURCE_TXT = ("Source : Gervais C., Donetti L., Bonnet F., Ichai C., Jacobs F., et les Groupes "
              "d'experts de la SRLF et de la SFAR — « Sécurisation des procédures à risques en "
              "réanimation : risque infectieux exclu », Ann Fr Anesth Reanim 2008;27:e43–e51, "
              "doi:10.1016/j.annfar.2008.09.005. Fiche de synthèse non officielle : se référer au "
              "texte intégral.")

def P(txt, style=S_CELL):
    return Paragraph(txt, style)

def chip(label, **kw):
    return grade_chip(label, **kw)

THEME_W = 26 * mm
ACCORD_W = 20 * mm

def theme_table(rows, col_widths=None, header=("Thème", "Recommandation", "Accord")):
    """rows: (theme, text, accord_label) - pas de reference numerique dans la source :
    'theme' remplace la colonne Ref habituelle."""
    text_w = PAGE_W - 2 * MARGIN - THEME_W - ACCORD_W
    cw = col_widths or [THEME_W, text_w, ACCORD_W]
    data = [[P(header[0], S_HEAD_W), P(header[1], S_HEAD_W), P(header[2], S_HEAD_W_C)]]
    for theme, txt, grade in rows:
        data.append([P(theme, S_CELL_B), P(txt, S_CELL), chip(grade, width=ACCORD_W - 2 * mm)])
    t = Table(data, colWidths=cw, repeatRows=1)
    style_cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), NAVY), ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTNAME", (0, 0), (-1, 0), FONT_BOLD), ("FONTSIZE", (0, 0), (-1, 0), 8),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("ALIGN", (2, 0), (2, -1), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 0.5, GREY_LIGHT),
        ("TOPPADDING", (0, 0), (-1, -1), 3.0), ("BOTTOMPADDING", (0, 0), (-1, -1), 3.0),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            style_cmds.append(("BACKGROUND", (0, i), (-1, i), BG_PANEL))
    t.setStyle(TableStyle(style_cmds))
    return t

def legend_flowable():
    chip_w = 22 * mm
    content_w = PAGE_W - 2 * MARGIN
    gap = 3 * mm
    text_w = (content_w - 4 * chip_w - 3 * gap) / 4.0
    row = Table([[
        chip("Fort", width=chip_w - 2 * mm),
        P("<b>Accord fort</b> — médiane des cotations (1–9) à l'intérieur d'une des trois "
          "zones.", S_BADGE_HEAD),
        chip("Faible", width=chip_w - 2 * mm),
        P("<b>Accord faible</b> — médiane empiétant sur une borne de zone.", S_BADGE_HEAD),
    ]], colWidths=[chip_w, text_w, chip_w, text_w])
    row2 = Table([[
        chip("Indécision", width=chip_w - 2 * mm),
        P("<b>Zone d'indécision</b> — médiane en zone 4–6, ni accord ni désaccord "
          "(3 propositions, cf. fin de fiche).", S_BADGE_HEAD),
        chip("?", width=chip_w - 2 * mm),
        P("<b>Non coté</b> — proposition sans tag d'accord dans le texte source (5 cas, "
          "Champ 3.1, disclosure).", S_BADGE_HEAD),
    ]], colWidths=[chip_w, text_w, chip_w, text_w])
    for r in (row, row2):
        r.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                                ("TOPPADDING", (0, 0), (-1, -1), 1.5),
                                ("BOTTOMPADDING", (0, 0), (-1, -1), 1.5)]))
    return KeepTogether([row, Spacer(1, 1.5 * mm), row2])

TOTAL_PAGES = {"n": 12}

def on_page(canvas, doc, page_title):
    header_band(canvas, doc, "SRLF / SFAR — 2008 — FICHE DE SYNTHÈSE",
                "Sécurisation des procédures à risques en réanimation",
                page_title, icon_fn=lambda c, x, y: icon_shield(c, x, y, 13 * mm), color=NAVY)
    footer_band(canvas, doc, SOURCE_TXT, f"Page {doc.page} / {TOTAL_PAGES['n']}")

# ---------------------------------------------------------------------------
def _section_intro():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Champ d'application :</b> pratiques de sécurité (« safety practices ») pour les "
        "patients de <b>réanimation</b> — <b>risque infectieux explicitement exclu</b> du champ "
        "de ce document (fait l'objet d'autres référentiels SFAR/SRLF/CLIN). Recommandations "
        "d'experts, adulte et enfant (Champs 1 à 7), spécificités pédiatriques regroupées au "
        "Champ 8.", S_BODY), bg=BG_PANEL, border=TEAL))
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Méthodologie — un seul axe, pas de grade de preuve :</b> méthode SRLF-SFAR dérivée "
        "de la RAND/UCLA appropriateness method — chaque expert cote sur une échelle continue "
        "de 1 à 9 (1 = désaccord total, 9 = accord total) ; trois zones selon la position de la "
        "médiane : (1–3) désaccord, (4–6) indécision, (7–9) accord. L'accord (ou le désaccord) "
        "est dit <b>« fort »</b> si l'intervalle de la médiane reste à l'intérieur d'une des "
        "trois zones, <b>« faible »</b> dans le cas contraire. Aucun grade de preuve 1+/1-/2+/2- "
        "n'est utilisé. <b>Une zone d'indécision est explicitement identifiée par les auteurs</b> "
        "pour 3 propositions (reproduites en fin de fiche) — catégorie distincte, jamais "
        "reclassée en « fort » ou « faible ».", S_BODY_SM), bg=BG_PANEL, border=TEAL))
    story.append(Spacer(1, 3 * mm))
    story.append(legend_flowable())
    story.append(Spacer(1, 3 * mm))
    return story

def _section_champ1():
    story = []
    story.append(section_bar("Champ 1 — Sécurisation des soins et indicateurs : taxonomie générale"))
    story.append(Spacer(1, 2 * mm))
    story.append(theme_table([
        ("EI / EPR", "Un événement indésirable (EI) est une situation qui s'écarte des "
         "procédures ou résultats habituellement escomptés, potentiellement source de dommage ; "
         "inclut les erreurs humaines (procédures) et les EI patients (résultats).", "Faible"),
        ("EI / EPR", "L'erreur humaine est un écart par rapport à un objectif non atteint lors "
         "d'une séquence programmée d'activité mentale ou physique.", "Faible"),
        ("EI / EPR", "Les événements porteurs de risque (EPR), définis par le décret sur "
         "l'accréditation des médecins des spécialités à risque, sont des EI à l'exclusion des "
         "EI graves.", "Faible"),
        ("EI / EPR", "Un événement indésirable <b>patient</b> est une complication directement "
         "liée aux soins et non à la pathologie sous-jacente du patient.", "Fort"),
        ("EI / EPR", "Un événement indésirable <b>grave</b> patient est une complication "
         "directement liée aux soins entraînant un risque vital, une prolongation de séjour, la "
         "nécessité de gestes invasifs, ou des séquelles invalidantes.", "Fort"),
        ("EI / EPR", "Un EI ou un EPR doit être considéré comme <b>inévitable</b> lorsque les "
         "soins ont été délivrés conformément à l'état de l'art.", "Fort"),
        ("EI / EPR", "Un EI ou un EPR doit être considéré comme <b>évitable ou possiblement "
         "évitable</b> lorsqu'on a mis en évidence une ou plusieurs erreurs médicales associées "
         "ou non à un ou plusieurs défauts système (structure, organisation, management), ou un "
         "ou plusieurs défauts système sans erreur médicale.", "Fort"),
        ("EI / EPR", "En dehors des situations caricaturales, seule une analyse fine pourra "
         "distinguer les EI évitables de ceux qui ne le sont pas, en raison de l'importance des "
         "comorbidités comme facteurs de risque.", "Faible"),
        ("EI / EPR", "Les procédures à risque pour le patient de réanimation sont principalement "
         "des procédures invasives.", "Faible"),
        ("EI / EPR", "La sécurisation des procédures à risque est une démarche qui permet "
         "d'identifier et de traiter les différentes sources de risque afin de réduire au "
         "minimum le risque pour les patients.", "Fort"),
        ("EI / EPR", "Les procédures de sécurisation (« safety practices ») sont des procédures "
         "de soins et/ou structurelles/organisationnelles qui préviennent, diminuent la "
         "fréquence de survenue, ou atténuent les conséquences des erreurs et des EI.", "Fort"),
        ("Indicateurs", "La mise en place d'un indicateur nécessite au préalable d'avoir défini "
         "l'objectif de sécurisation des soins surveillé par cet indicateur.", "Fort"),
        ("Indicateurs", "Un indicateur doit être analysé systématiquement et de façon "
         "régulière.", "Fort"),
        ("Indicateurs", "En cas de variation d'un indicateur susceptible d'être le témoin d'un "
         "EPR, une analyse systémique doit être réalisée afin d'identifier les causes racines de "
         "l'EPR.", "Fort"),
        ("Indicateurs", "Un indicateur doit être acceptable, valide, pertinent, fiable et "
         "compréhensible.", "Fort"),
        ("Indicateurs", "Les indicateurs concernant la sécurisation d'une procédure de soins "
         "doivent être en nombre limité.", "Fort"),
    ]))
    return story

def _section_champ2():
    story = []
    story.append(Spacer(1, 2 * mm))
    story.append(section_bar("Champ 2 — Épidémiologie"))
    story.append(Spacer(1, 2 * mm))
    story.append(theme_table([
        ("Épidémiologie", "Il faut standardiser les définitions concernant les erreurs "
         "médicales, les EI et leur évitabilité.", "Fort"),
        ("Épidémiologie", "Les erreurs médicales et les EI patients doivent être classés en "
         "fonction de leur gravité.", "Fort"),
        ("Épidémiologie", "La standardisation de la méthode de recueil des erreurs médicales et "
         "des événements indésirables patients est nécessaire.", "Fort"),
        ("Épidémiologie", "Quelle que soit la méthode, il est recommandé que ce recueil soit non "
         "punitif, confidentiel et indépendant.", "Faible"),
        ("Épidémiologie", "Le recueil régulier par la déclaration volontaire, bien que source de "
         "biais, permet de développer une culture sécurité.", "Fort"),
        ("Épidémiologie", "Il est recommandé de privilégier l'analyse des erreurs médicales et "
         "des EI patients évitables.", "Faible"),
        ("Épidémiologie", "Il est important de pouvoir identifier indépendamment les erreurs des "
         "EI patients.", "Faible"),
        ("Épidémiologie", "Il est important d'étudier les facteurs permettant la détection et la "
         "récupération de ces erreurs.", "Fort"),
    ]))
    return story

def _section_champ3():
    story = []
    story.append(Spacer(1, 2 * mm))
    story.append(section_bar("Champ 3 — Procédures de sécurisation structurelles et managériales"))
    story.append(Spacer(1, 2 * mm))
    story.append(theme_table([
        ("3.1 Structures", "Le service de réanimation doit comporter des chambres "
         "individuelles et des lits d'USC situés à proximité des lits de réanimation.", "Fort"),
        ("3.1 Structures", "Le service de réanimation doit pouvoir disposer de résultats "
         "biologiques fiables, obtenus rapidement et dont la traçabilité est assurée "
         "(pneumatique, biologie délocalisée).", "Fort"),
        ("3.1 Structures", "Il existe une procédure chariot d'urgence.", "Fort"),
        ("3.1 Structures", "Informatisation de l'unité de soins.", "Fort"),
        ("3.1 Structures", "L'identitovigilance est assurée.", "?"),
        ("3.1 Structures", "L'informatisation du dossier médical et de la prescription doit "
         "être développée.", "?"),
        ("3.1 Structures", "La dispensation médicamenteuse est personnalisée.", "?"),
        ("3.1 Structures", "Les résultats des examens biologiques et d'imagerie médicale sont "
         "disponibles dans le service.", "?"),
        ("3.1 Structures", "Il existe une procédure partagée avec le plateau médico-technique "
         "pour la transmission des résultats urgents (par exemple : hyperkaliémie).", "?"),
        ("3.2 Activité", "Il existe une relation entre le volume d'actes réalisés et la "
         "performance en termes de sécurité patient.", "Fort"),
        ("3.2 Activité", "Lorsqu'une technique médicale n'est pas disponible localement, "
         "celle-ci doit faire l'objet d'une convention formalisée avec un service "
         "prestataire.", "Fort"),
        ("3.3 Organisation", "Le responsable médical du service et/ou du pôle doit être "
         "impliqué dans la gestion du recrutement du personnel soignant.", "Fort"),
        ("3.3 Organisation", "Les compétences médicales et paramédicales doivent être "
         "identiques en réanimation et en USC.", "Faible"),
        ("3.3.1 Travail médical", "Si le médecin de garde ne fait pas partie de l'équipe "
         "médicale du service, un médecin de cette équipe doit pouvoir être consulté pendant la "
         "garde.", "Fort"),
        ("3.3.1 Travail médical", "Il existe une procédure d'appel du médecin réanimateur (bip, "
         "téléphone…).", "Fort"),
        ("3.3.1 Travail médical", "Il existe un programme de formation dans le service "
         "concernant les internes et les médecins de l'équipe.", "Fort"),
        ("3.3.2 Travail soignant", "Il existe un cadre de santé de proximité dont l'activité "
         "est dédiée à la réanimation.", "Fort"),
        ("3.3.2 Travail soignant", "Les nouvelles IDE doivent bénéficier d'une période "
         "d'intégration d'un mois, faisant l'objet d'une traçabilité (livret d'intégration) ; la "
         "présence d'un infirmier tuteur est souhaitable durant cette période.", "Fort"),
        ("3.3.2 Travail soignant", "Une attention particulière doit être portée sur les équipes "
         "de nuit, qui doivent bénéficier soit de formations spécifiques, soit de périodes de "
         "rotation de jour.", "Fort"),
        ("3.3.2 Travail soignant", "Les transmissions entre équipes médicales et/ou soignantes "
         "doivent être formalisées.", "Fort"),
        ("3.3.2 Travail soignant", "Il est nécessaire d'identifier, selon la dimension du "
         "service, un ou plusieurs agents responsables de la logistique (matériel, chariot "
         "d'urgence et de déplacement extérieur).", "Fort"),
        ("3.3.2 Travail soignant", "Il est souhaitable que le service dispose d'outils "
         "permettant l'évaluation ponctuelle de la charge de travail.", "Fort"),
        ("3.3.3 Protocoles", "L'organisation protocolisée est souhaitable ; les protocoles "
         "concernant les procédures de soins doivent être produits localement ou faire l'objet "
         "d'une appropriation locale s'il s'agit de protocoles extérieurs, et doivent faire "
         "l'objet de fréquents rappels (affiches, aide-mémoire de poche, informatique, staff).",
         "Fort"),
        ("3.3.3 Protocoles", "Les procédures et/ou situations cliniques à risque doivent "
         "périodiquement faire l'objet de procédures de formation (prise en charge de l'arrêt "
         "cardiorespiratoire, de l'intubation difficile, tamponnade).", "Fort"),
        ("3.3.3 Protocoles", "Ces situations doivent faire l'objet, a posteriori, de réunions de "
         "débriefing de l'ensemble de l'équipe médicale et paramédicale.", "Fort"),
        ("3.3.3 Protocoles", "D'une manière générale, le service doit disposer de check-lists "
         "pour les procédures à risques reconnues et identifiées localement, a fortiori "
         "lorsqu'elles ont fait l'objet de recommandations par les sociétés savantes "
         "(SFAR/SRLF).", "Fort"),
        ("3.3.3 Protocoles", "Le service doit disposer d'une procédure écrite de régulation "
         "d'admission des patients.", "Fort"),
        ("3.3.3 Protocoles", "Le service doit disposer d'une procédure écrite de sortie des "
         "patients, comportant impérativement une fiche de liaison IDE et une synthèse médicale "
         "afin d'assurer la continuité des soins.", "Fort"),
        ("3.4 Culture sécurité", "Le service de réanimation doit organiser périodiquement des "
         "réunions de morbi-mortalité, souhaitablement conformes aux recommandations des "
         "sociétés savantes (SFAR/SRLF).", "Fort"),
        ("3.4 Culture sécurité", "Le service dispose d'une méthode de recueil des EI ; chaque "
         "service détermine, a priori, quels EI il va surveiller à partir de quels indicateurs "
         "et avec quel objectif.", "Fort"),
        ("3.4 Culture sécurité", "Certaines procédures à risque doivent faire l'objet d'une "
         "réflexion bénéfice/risque dont la traçabilité est assurée dans le dossier patient.",
         "Fort"),
        ("3.4 Culture sécurité", "Les audits de soins peuvent être intégrés dans l'évaluation "
         "des pratiques professionnelles (EPP) pour le personnel médical ; ils sont réalisés au "
         "mieux à partir des documents élaborés par les sociétés savantes (SFAR/SRLF).", "Fort"),
        ("3.4 Culture sécurité", "Le service doit disposer d'indicateurs d'alerte d'épuisement "
         "professionnel (demandes de changement, absentéisme).", "Fort"),
        ("3.4 Culture sécurité", "Il existe une procédure d'aide pour les agents en difficultés "
         "(raisons personnelles ou professionnelles).", "Fort"),
        ("3.4 Culture sécurité", "Il existe une formalisation et une traçabilité dans le dossier "
         "du patient des décisions de limitation et d'arrêt des thérapeutiques actives et de "
         "toute décision éthique.", "Fort"),
        ("3.5 Tableau de bord", "Le service de réanimation tient un registre des refus "
         "d'admission indiquant les motifs.", "Fort"),
        ("3.5 Tableau de bord", "Le service de réanimation dispose d'indicateurs de procédures "
         "et de résultats spécifiques concernant la sécurité des patients.", "Fort"),
        ("3.5 Tableau de bord", "Le service de réanimation dispose d'indicateurs de résultats "
         "permettant une comparaison interne ou externe.", "Faible"),
    ]))
    return story

def _section_champ4():
    story = []
    story.append(Spacer(1, 2 * mm))
    story.append(section_bar("Champ 4 — Procédures de sécurisation du matériel"))
    story.append(Spacer(1, 2 * mm))
    story.append(theme_table([
        ("4.1 Principes", "Les dispositifs médicaux (DM) induisent une série de risques de leur "
         "conception à leur mise au rebut, notamment le risque d'erreurs humaines qui doivent "
         "être maîtrisées.", "Fort"),
        ("4.1 Principes", "D'une manière générale, les principaux éléments de sécurisation "
         "doivent reposer sur la formation des utilisateurs, l'entretien et la vérification des "
         "DM et l'application rigoureuse des règles de matériovigilance.", "Fort"),
        ("4.1 Principes", "Une collaboration entre services cliniques et services biomédicaux "
         "est nécessaire.", "Fort"),
        ("4.1 Principes", "Les différents acteurs intervenant dans la gestion des DM doivent "
         "être : un référent biomédical ingénieur par service (ou pôle) et/ou par type de "
         "matériel, un référent médical par service ou pôle, enfin un référent paramédical "
         "et/ou un technicien délocalisé par service ou pôle.", "Faible"),
        ("4.1 Principes", "Il est recommandé de mettre en place une gestion informatisée du "
         "parc des DM.", "Fort"),
        ("4.1 Principes", "Le suivi informatisé d'un DM doit notamment prendre en compte la "
         "date de réception, le numéro de série, le lieu de stockage, l'agenda de maintenance et "
         "de mise à niveau, la notification des pannes (type, fréquence et durée "
         "d'immobilisation), enfin la fréquence des défauts utilisateurs.", "Fort"),
        ("4.2 Implantation", "Le cahier des charges définissant précisément le besoin "
         "qualitatif et quantitatif doit être établi en collaboration entre services cliniques "
         "et services biomédicaux.", "Fort"),
        ("4.2 Implantation", "Il faut prendre en compte des éléments tels que : durée de "
         "garantie, contrat de maintenance, proximité et disponibilité du service après-vente.",
         "Fort"),
        ("4.2 Implantation", "Les certificats de conformité aux textes réglementaires "
         "applicables à la classe du dispositif doivent être exigés.", "Fort"),
        ("4.2 Implantation", "Avant implantation, il est recommandé d'effectuer un essai sur "
         "site en conditions réelles avec un panel représentatif d'utilisateurs pour identifier "
         "les situations locales spécifiques à risque.", "Fort"),
        ("4.2 Implantation", "En cas de prêt de matériel, une fiche de mise à disposition doit "
         "être validée et signée par la société, les services cliniques et biomédicaux.",
         "Fort"),
        ("4.3 Mise en service", "Il faut programmer et effectuer la formation des services "
         "cliniques et biomédicaux avant la réception du DM ; cette formation doit faire l'objet "
         "d'une traçabilité.", "Fort"),
        ("4.3 Mise en service", "À la livraison, il faut vérifier que l'équipement correspond à "
         "l'intégralité de la commande (accessoires et consommables éventuels).", "Fort"),
        ("4.3 Mise en service", "Le DM doit être inscrit à l'inventaire du service.", "Fort"),
        ("4.3 Mise en service", "Si le DM est partagé par différents secteurs, il est recommandé "
         "de déterminer son périmètre fonctionnel (par exemple établissement d'une convention "
         "d'utilisation).", "Fort"),
        ("4.4 Utilisation", "L'établissement de check-lists adaptées localement et à chaque "
         "type de matériel est recommandé pour vérifier un bon fonctionnement du DM avant "
         "chaque utilisation ; ces check-lists doivent faire l'objet d'une traçabilité "
         "permettant d'identifier au minimum l'opérateur, la date, le type de dysfonctionnement "
         "et préciser la liste des fonctionnalités non opérationnelles « bloquantes ».", "Fort"),
        ("4.4 Utilisation", "Si des check-lists de contrôle sont prévues par le constructeur et "
         "intégrées au logiciel du matériel, il faut les respecter et les compléter "
         "éventuellement par les check-lists locales.", "Fort"),
        ("4.4 Utilisation", "Il faut rédiger une fiche d'alerte incidente pour tout "
         "dysfonctionnement, panne ou arrêt intempestif, information écran fausse.", "Fort"),
        ("4.4 Utilisation", "Les maintenances préventives et curatives doivent être organisées "
         "par le service biomédical et faire l'objet de procédures écrites et d'une "
         "traçabilité.", "Fort"),
        ("4.4 Utilisation", "Une procédure en cas de panne, adaptée à chaque type de matériel, "
         "doit être prévue par le service biomédical et comporter au minimum la disponibilité "
         "du matériel de suppléance et l'identification des intervenants à contacter 24 h/24 et "
         "7 j/7.", "Fort"),
        ("4.4 Utilisation", "Il est recommandé d'organiser des formations régulièrement pour les "
         "utilisateurs en cas de renouvellement des personnels, en cas de fréquence anormale du "
         "nombre de défauts utilisateurs ou lors de mise à niveau des matériels.", "Fort"),
        ("4.4 Utilisation", "Il faut éviter de laisser le parc atteindre l'obsolescence en "
         "anticipant le remplacement du DM quand nécessaire (année de mise en service, nombre "
         "d'heures d'utilisation, concept dépassé et disparition des consommables).", "Fort"),
        ("4.4 Utilisation", "Lors de la réforme du DM, il faut retirer également les "
         "consommables pour éviter toute confusion avec d'autres DM de même catégorie.", "Fort"),
    ]))
    return story

def _section_champ5():
    story = []
    story.append(Spacer(1, 2 * mm))
    story.append(section_bar("Champ 5 — Sécurisation au cours de la ventilation mécanique"))
    story.append(Spacer(1, 2 * mm))
    story.append(theme_table([
        ("5.1 Intubation", "Chaque unité de réanimation doit disposer d'un chariot d'intubation "
         "dont la composition, vérifiée quotidiennement, est conforme aux recommandations de la "
         "conférence d'experts sur intubation difficile.", "Fort"),
        ("5.1 Intubation", "Avant toute intubation en réanimation, il est recommandé de : "
         "scoper le patient et vérifier la présence du matériel nécessaire dans la chambre ; "
         "s'assurer du bon fonctionnement de l'aspiration et de la source d'oxygène (haut débit "
         "relié au ballon et au masque facial) ; vérifier le bon fonctionnement du respirateur "
         "auquel le patient sera branché immédiatement après l'intubation ; préoxygéner tous les "
         "patients avec une FiO2 à 1.", "Fort"),
        ("5.1 Intubation", "S'il n'y a pas de contre-indications, un remplissage vasculaire est "
         "souhaitable.", "Faible"),
        ("5.1 Intubation", "Deux opérateurs (deux médecins ou un médecin et une infirmière) "
         "doivent être présents systématiquement au moment de l'intubation.", "Faible"),
        ("5.1 Intubation", "Si l'indication d'une sédation continue a été posée, celle-ci doit "
         "être préparée avant et administrée immédiatement après l'intubation.", "Faible"),
        ("5.1 Intubation", "Il est préférable d'utiliser une lame métallique pour la "
         "laryngoscopie.", "Faible"),
        ("5.1 Intubation", "Il faut assurer une traçabilité dans le dossier médical de toutes "
         "les intubations (en particulier difficiles).", "Faible"),
        ("5.1 Intubation", "En dehors des contre-indications, il faut utiliser l'induction à "
         "séquence rapide (ISR).", "Faible"),
        ("5.1 Intubation", "Le contrôle de la bonne position de la sonde d'intubation à l'aide "
         "d'un capnographe (EtCO2) doit être privilégié si le service en est doté.", "Faible"),
        ("5.1 Intubation", "Les paramètres de la ventilation mécanique doivent être réadaptés à "
         "distance de l'intubation.", "Faible"),
        ("5.2 Trachéotomie", "La trachéotomie doit être réalisée sous anesthésie générale avec "
         "curarisation appropriée.", "Faible"),
        ("5.2 Trachéotomie", "Si la technique percutanée a été choisie, un fibroscope bronchique "
         "doit être utilisé.", "Fort"),
        ("5.2 Trachéotomie", "Lorsque l'indication d'une trachéotomie percutanée a été posée, il "
         "faut s'assurer qu'un chirurgien (ORL si possible) puisse, en cas d'échec, réaliser en "
         "urgence une trachéotomie chirurgicale.", "Faible"),
        ("5.2 Trachéotomie", "L'hémostase doit être vérifiée (TP &gt; 50 %, TCA &lt; 1,5 fois le "
         "témoin, plaquettes &gt; 50 000/mm³) et l'héparinothérapie standard curative "
         "interrompue de manière momentanée, avec respect d'un délai en cas d'HBPM.", "Faible"),
        ("5.2 Trachéotomie", "Un plateau d'intubation doit être prêt en cas de difficultés, "
         "ainsi qu'une boîte chirurgicale si la technique percutanée a été choisie.", "Fort"),
        ("5.2 Trachéotomie", "Le système d'aspiration murale avec canule d'aspiration stérile "
         "doit être vérifié.", "Fort"),
        ("5.3 VM invasive", "La prévention de l'auto-extubation et de ses conséquences "
         "éventuelles nécessite : la présence d'un set complet d'intubation dont la vérification "
         "et la traçabilité dans un carnet de bord daté/signé est assurée quotidiennement ; la "
         "présence d'un protocole d'évaluation de la sédation et de la sevrabilité ; le repérage "
         "de la position des sondes après contrôle radiographique retranscrit lors des "
         "transmissions infirmières ; la surveillance de l'état cutané (escarres nez/bouche/"
         "oreilles) et l'adaptation des systèmes d'attaches.", "Faible"),
        ("5.3 VM invasive", "La prévention des autres EI (pneumopathies nosocomiales notamment) "
         "nécessite : la surélévation de la tête du lit (&gt; 30°) ; des soins de bouche une "
         "fois par équipe ; une procédure d'aspiration propre (sonde à usage unique, port de "
         "gants) ; le contrôle radiographique de la sonde gastrique.", "Faible"),
        ("5.3 VM invasive", "L'optimisation de la ventilation mécanique en termes de sécurité "
         "patient nécessite : la vérification de l'intégrité des tuyaux/circuits et de la "
         "présence d'eau dans les humidificateurs (une fois par équipe) ; la surveillance de la "
         "pression du ballonnet une fois par équipe, retranscrite sur la feuille de "
         "surveillance ; la présence permanente d'un système d'aspiration fonctionnel ; la "
         "prescription écrite au démarrage de la VM des conditions de ventilation (alarmes "
         "incluses), refaite à chaque changement de réglage.", "Fort"),
        ("5.4 Sevrage VM", "Le processus de sevrage doit être envisagé aussitôt que possible "
         "dans la prise en charge d'une IRA.", "Fort"),
        ("5.4 Sevrage VM", "Il est recommandé d'évaluer quotidiennement la sevrabilité sur des "
         "critères simples de stabilité respiratoire, hémodynamique et neurologique, et de "
         "réaliser une épreuve de sevrage en VS dès que ces critères sont remplis — les deux "
         "étapes essentielles à l'identification des patients susceptibles d'être sevrés.",
         "Fort"),
        ("5.4 Sevrage VM", "Les critères prédictifs de l'issue du sevrage ne doivent pas être "
         "attendus et/ou obtenus pour réaliser l'épreuve de sevrage.", "Fort"),
        ("5.4 Sevrage VM", "La tolérance clinique d'une épreuve de sevrage doit être considérée "
         "comme le meilleur test pour juger a priori des capacités de déventilation d'un "
         "patient.", "Fort"),
        ("5.4 Sevrage VM", "L'épreuve de sevrage doit être réalisée sur pièce en T (VS/T) ou en "
         "aide inspiratoire (AI) d'un niveau minimal de 7 cmH2O, avec ou sans PEP externe "
         "(≤ 5 cmH2O), pour une durée minimale de 30 minutes.", "Fort"),
        ("5.4 Sevrage VM", "Le succès de l'épreuve de sevrage doit faire procéder à l'extubation "
         "dans les suites immédiates, après avoir éliminé des facteurs d'échec d'extubation.",
         "Fort"),
        ("5.4 Sevrage VM", "L'échec de l'épreuve de sevrage doit faire imposer d'en rechercher "
         "la ou les causes et leur éventuelle réversibilité.", "Fort"),
        ("5.4 Sevrage VM", "Chez le patient difficile ou potentiellement difficile à sevrer, la "
         "sécurisation du sevrage doit comprendre : la réalisation d'une épreuve de sevrage en "
         "AI ± PEP sur 120 minutes maximum ; la réalisation d'un gaz du sang artériel au cours "
         "ou en fin d'épreuve ; le recours à une stratégie de sevrage progressif privilégiant "
         "l'AI ± PEP dégressive.", "Faible"),
        ("5.4 Sevrage VM", "La VNI peut être utilisée comme technique de sevrage permettant "
         "l'extubation précoce chez les patients BPCO hypercapniques.", "Fort"),
        ("5.4 Sevrage VM", "Il peut être utile de mettre en place des protocoles de sevrage.",
         "Faible"),
        ("5.4 Sevrage VM", "Il peut être utile d'utiliser des logiciels informatisés.", "Faible"),
        ("5.5 Extubation", "Avant d'envisager une extubation, il faut évaluer la capacité du "
         "patient à tousser et à évacuer ses sécrétions.", "Fort"),
        ("5.5 Extubation", "Il n'y a pas lieu de réaliser systématiquement un test de fuite lors "
         "de l'extubation des patients de réanimation.", "Faible"),
        ("5.5 Extubation", "Le test de fuite est recommandé chez les patients à risque.", "Fort"),
        ("5.5 Extubation", "Chez les patients à très haut risque, chez qui la réalisation d'une "
         "trachéotomie peut être difficile, il faut discuter la pertinence d'une extubation "
         "réalisée au bloc opératoire en présence d'un chirurgien ORL.", "Faible"),
        ("5.6 VNI", "La VNI doit représenter la stratégie ventilatoire sécuritaire pour la prise "
         "en charge de l'IRA hypercapnique des patients BPCO et de l'OAP cardiogénique.",
         "Fort"),
        ("5.6 VNI", "Dans la prise en charge de l'IRA hypoxémique (cœur et poumons "
         "antérieurement sains), l'analyse du rapport bénéfices/risques doit prendre en compte "
         "le risque accru de mortalité en cas d'échec de la VNI.", "Fort"),
        ("5.6 VNI", "L'application de la VNI à l'IRA hypoxémique doit dans tous les cas être "
         "menée dans un milieu sécurisé de réanimation pour ne pas retarder le moment de "
         "l'intubation.", "Fort"),
        ("5.6 VNI", "Quel que soit le type d'IRA (hypercapnique ou hypoxémique), les patients "
         "les plus graves sous VNI doivent être pris en charge et surveillés en réanimation.",
         "Fort"),
        ("5.6 VNI", "La maîtrise de la VNI doit représenter un objectif de formation théorique "
         "et pratique des personnels médicaux et paramédicaux au sein des services de "
         "réanimation.", "Fort"),
        ("5.6 VNI", "La pratique de la VNI implique une bonne connaissance des indications, des "
         "contre-indications et des facteurs prédictifs d'échec de la technique.", "Fort"),
        ("5.6 VNI", "L'élaboration de protocoles de soins, propres au service, est recommandée "
         "pour favoriser l'implantation de la technique et ses résultats.", "Fort"),
        ("5.6 VNI", "Le matériel de VNI disponible (masques, ventilateurs, humidificateurs) doit "
         "être adapté à la pathologie et à la gravité des patients pris en charge.", "Fort"),
        ("5.6 VNI", "La sécurisation de la VNI passe par l'optimisation de ses modalités "
         "pratiques : choix d'un masque facial en première intention ; humidification des gaz "
         "inspirés (humidificateur chauffant si hypercapnie grave/intolérance) ; retrait du "
         "raccord annelé en cas d'IRA hypercapnique ; choix d'un ventilateur de réanimation chez "
         "les patients les plus à risque d'échec ; choix d'un mode à double niveau de pression "
         "en première intention hors OAP cardiogénique ; augmentation graduelle du niveau "
         "d'assistance jusqu'au réglage optimal ; réglage du trigger inspiratoire, de la pente "
         "de pressurisation, du niveau d'AI et du cyclage inspiration/expiration ; réglage "
         "adapté des alarmes du ventilateur et de la ventilation d'apnée.", "Fort"),
        ("5.6 VNI", "L'application continue de la VNI doit être privilégiée initialement jusqu'à "
         "une amélioration clinique et gazométrique franche, avant d'envisager un mode "
         "séquentiel (alternance VNI/VS).", "Fort"),
        ("5.6 VNI", "Les risques d'échec de la VNI doivent imposer une surveillance initiale "
         "rapprochée au cours des premières heures pour juger de la réponse à la technique.",
         "Fort"),
        ("5.6 VNI", "La surveillance de la VNI doit être avant tout clinique, mais doit s'aider "
         "des gaz du sang, des paramètres et des courbes du ventilateur pour optimiser les "
         "réglages et la tolérance de la technique.", "Fort"),
        ("5.6 VNI", "En l'absence d'échec, l'arrêt de la VNI suppose au préalable une évaluation "
         "clinique et gazométrique de l'autonomie ventilatoire du patient en VS sur une période "
         "de 6 à 12 heures.", "Fort"),
    ]))
    return story

def _section_champ6():
    story = []
    story.append(Spacer(1, 2 * mm))
    story.append(section_bar("Champ 6 — « Procédures circulatoires » : vasoactifs et abords vasculaires"))
    story.append(Spacer(1, 2 * mm))
    story.append(theme_table([
        ("6.1 Vasoactifs", "Le rangement des drogues vasoactives doit tenir compte du risque de "
         "confusion entre différentes ampoules ; l'étiquetage des seringues doit être "
         "suffisamment explicite et clair pour éviter toute confusion.", "Fort"),
        ("6.1 Vasoactifs", "Les médicaments vasoactifs doivent être administrés par voie "
         "intraveineuse et de façon continue grâce à une seringue pour perfusion continue.",
         "Fort"),
        ("6.1 Vasoactifs", "La voie d'administration veineuse centrale doit toujours être "
         "privilégiée ; la voie périphérique est possible pour la dopamine et pour la "
         "dobutamine à faible dose (≤ 5 µg/kg/min) ; en urgence, en attente de l'insertion d'un "
         "cathéter veineux central, l'administration peut être débutée sur une voie veineuse "
         "périphérique.", "Fort"),
        ("6.1 Vasoactifs", "L'utilisation de pompes de perfusion munies de logiciels permettant "
         "le relais automatique des seringues contenant une drogue vasoactive doit être "
         "privilégiée.", "Fort"),
        ("6.1 Vasoactifs", "Le raccord de la voie de perfusion des amines vasoactives à la voie "
         "de perfusion principale doit se faire par l'intermédiaire d'une tubulure de petit "
         "calibre et le plus près possible du patient.", "Fort"),
        ("6.1 Vasoactifs", "Les systèmes utilisés pour le relais des seringues destinées à "
         "l'administration de drogues vasoactives doivent être munis d'une pré-alarme sonore "
         "pour la validation de la procédure automatique du relais.", "Fort"),
        ("6.1 Vasoactifs", "Le relais des seringues doit faire l'objet d'une procédure de soins "
         "standardisée dans le service de réanimation.", "Fort"),
        ("6.1 Vasoactifs", "La dilution des drogues vasoactives doit faire l'objet d'une "
         "procédure de soins standardisée dans le service de réanimation.", "Fort"),
        ("6.2 KT central", "Il faut utiliser du matériel entièrement transparent permettant "
         "d'identifier clairement les bulles présentes dans le circuit de cathétérisme central "
         "artériel ou veineux.", "Fort"),
        ("6.2 KT central", "Les connexions de la ligne de perfusion d'un cathéter central "
         "artériel ou veineux doivent utiliser un système à vis (type Luer-Lock).", "Fort"),
        ("6.2 KT central", "Les robinets de la ligne de perfusion d'un cathéter central artériel "
         "ou veineux doivent être clairement identifiés afin d'éviter le risque d'injections "
         "accidentelles sur cette ligne.", "Fort"),
        ("6.2 KT central", "Après l'ablation d'un cathéter central artériel ou veineux, il faut "
         "vérifier qu'il a été retiré dans son ensemble.", "Fort"),
        ("6.2.1 KT artériel", "Un cathéter artériel ne doit pas être posé sur une artère "
         "terminale (artère humérale).", "Fort"),
        ("6.2.1 KT artériel", "Les sites d'insertion possibles d'un cathéter artériel sont les "
         "artères radiales, fémorales et pédieuses.", "Fort"),
        ("6.2.1 KT artériel", "La recherche d'une circulation collatérale palmaire par le test "
         "d'Allen est un préalable à la pose par voie radiale ; ce test peut être remplacé par "
         "le signal de pléthysmographie aux premiers et derniers doigts de la main.", "Fort"),
        ("6.2.1 KT artériel", "Un cathéter artériel ne doit pas être inséré dans des prothèses "
         "vasculaires ; il faut rechercher régulièrement une ischémie du membre d'aval (retrait "
         "du cathéter et exploration/surveillance de la vascularisation en cas de signe "
         "d'ischémie) ; privilégier les cathéters de petite longueur (3 à 5 cm) pour la voie "
         "radiale.", "Fort"),
        ("6.2.1 KT artériel", "Il faut utiliser un système de purge du cathéter artériel "
         "assurant un débit continu d'au minimum 2 mL/h, incluant la possibilité d'une purge "
         "manuelle.", "Fort"),
        ("6.2.1 KT artériel", "Il n'y a pas d'argument pour pratiquer une anticoagulation "
         "systématique de la ligne artérielle.", "Fort"),
        ("6.2.1 KT artériel", "Après l'ablation du cathéter artériel, il faut comprimer le point "
         "de ponction pendant quelques minutes jusqu'à l'arrêt de tout saignement.", "Fort"),
        ("6.2.2 KT veineux central", "Le cathétérisme veineux central doit être effectué par ou "
         "avec l'aide d'un opérateur expérimenté.", "Fort"),
        ("6.2.2 KT veineux central", "La voie sous-clavière doit être évitée en cas d'anomalie "
         "de l'hémostase, en cas d'hypoxémie sévère (PaO2/FiO2 &lt; 200) et en cas d'anomalie "
         "anatomique.", "Fort"),
        ("6.2.2 KT veineux central", "En cas d'anomalie importante de l'hémostase, la voie "
         "fémorale doit être préférée pour le cathétérisme veineux central.", "Fort"),
        ("6.2.2 KT veineux central", "Lorsque la deuxième tentative de ponction veineuse a "
         "échoué, il est conseillé de changer de site, d'opérateur ou de technique (repérage "
         "ultrasonographique).", "Faible"),
        ("6.2.2 KT veineux central", "Le repérage ultrasonographique peut améliorer le taux de "
         "succès du cathétérisme veineux, surtout pour la voie jugulaire interne, sans "
         "augmenter le temps de cathétérisme.", "Fort"),
        ("6.2.2 KT veineux central", "Un contrôle radiographique du thorax doit être effectué "
         "après la pose d'un cathéter veineux sous-clavier afin de rechercher l'absence de "
         "pneumothorax et de contrôler la bonne position du cathéter.", "Fort"),
        ("6.2.2 KT veineux central", "Afin d'éviter toute érosion endovasculaire et effraction "
         "intra-péricardique, l'extrémité des cathéters veineux insérés dans le territoire cave "
         "supérieur doit être située au niveau de la carène ; en cas de mauvaise position, le "
         "cathéter doit être retiré de quelques centimètres.", "Fort"),
        ("6.3 KT artériel pulmonaire", "La sécurisation de la procédure de pose d'un cathéter "
         "veineux central s'applique à la pose du désilet préalable à l'insertion du cathéter "
         "artériel pulmonaire.", "Fort"),
        ("6.3 KT artériel pulmonaire", "L'utilisation du cathéter artériel pulmonaire est "
         "contre-indiquée par la présence d'une sonde d'entraînement intracardiaque.", "Faible"),
        ("6.3 KT artériel pulmonaire", "Lors de l'introduction du cathéter dans les cavités "
         "cardiaques, une surveillance permanente du rythme doit être effectuée afin de "
         "rechercher les troubles du rythme cardiaque.", "Fort"),
        ("6.3 KT artériel pulmonaire", "Un contrôle de la radiographie de thorax doit être "
         "effectué après l'insertion du cathéter artériel pulmonaire afin de vérifier sa "
         "position.", "Fort"),
        ("6.3 KT artériel pulmonaire", "Le dégonflement du ballonnet doit être systématiquement "
         "vérifié après que ce dernier a été utilisé.", "Fort"),
        ("6.3 KT artériel pulmonaire", "Le matériel et les médicaments nécessaires au traitement "
         "d'un trouble du rythme et d'un trouble conductif doivent être disponibles rapidement "
         "lors de la pose d'un cathéter artériel pulmonaire.", "Fort"),
        ("6.3 KT artériel pulmonaire", "Le cathéter artériel pulmonaire doit être maintenu en "
         "place le moins longtemps possible ; une durée maximale de trois jours est conseillée.",
         "Fort"),
        ("6.3 KT artériel pulmonaire", "La calibration du zéro de référence doit se faire au "
         "niveau de l'oreillette droite et sa recalibration doit s'effectuer régulièrement et en "
         "cas de doute sur les mesures de pression affichées.", "Fort"),
        ("6.3 KT artériel pulmonaire", "La mesure de SvO2 nécessite une calibration régulière "
         "par co-oxymétrie.", "Fort"),
        ("6.3 KT artériel pulmonaire", "Le contrôle radiographique quotidien de la position de "
         "la sonde n'est pas nécessaire ; en cas d'anomalie d'obtention du tracé, la "
         "radiographie de thorax de contrôle s'impose.", "Faible"),
        ("6.3 KT artériel pulmonaire", "À l'ablation du cathéter artériel pulmonaire, il faut "
         "vérifier son intégrité.", "Fort"),
    ]))
    return story

def _section_champ7():
    story = []
    story.append(Spacer(1, 2 * mm))
    story.append(section_bar("Champ 7 — Sécurisation des procédures d'épuration extra-rénale"))
    story.append(Spacer(1, 2 * mm))
    story.append(theme_table([
        ("EER — Prescription", "La prescription d'une séance d'épuration extra-rénale (EER) "
         "intermittente ou continue doit comporter au minimum : la durée ; le type de "
         "membrane ; le débit de la pompe à sang ; le type et la posologie de l'anticoagulation "
         "du circuit extracorporel ; la perte hydrique horaire ou totale ; le débit de "
         "dialysat ; la composition du dialysat en sodium, potassium, calcium, soluté tampon et "
         "glucose ; enfin la température du dialysat.", "Fort"),
        ("EER — Membrane", "La structure de la membrane utilisée pour la réalisation d'une EER "
         "doit être en cellulose modifiée ou synthétique.", "Fort"),
        ("EER — Filtration", "Au cours de l'EER (intermittente ou continue), la filtration à "
         "travers la membrane doit être gérée par un contrôle automatisé.", "Fort"),
        ("EER — Filtration", "Au cours de l'hémofiltration, la fraction de filtration doit être "
         "surveillée en continu et la filtration doit être interrompue lors des situations à "
         "risque de chute du débit sanguin (nursing).", "Faible"),
        ("EER — Mise en route", "Avant toute mise en route d'une EER et en particulier pour "
         "l'hémofiltration, il est nécessaire de : s'assurer de l'absence de coudure du "
         "cathéter ; respecter les procédures de gestion des cathéters veineux centraux ; "
         "s'assurer de son bon positionnement dans le vaisseau (cliché thoracique) ; s'assurer "
         "de sa position adaptée au débit souhaité.", "Fort"),
        ("EER — Cathéters", "La pose et l'entretien des cathéters doivent être conformes aux "
         "recommandations du CLIN concernant la prévention du risque infectieux au cours de la "
         "mise en place des cathéters veineux centraux.", "Fort"),
        ("EER — Surveillance", "La surveillance d'une séance d'EER chez un patient de "
         "réanimation doit comporter au minimum : le monitorage continu de l'ECG et de la "
         "fréquence cardiaque ; la mesure rapprochée de la pression artérielle ; le recueil du "
         "ratio de filtration (techniques convectives), de la pression de retour veineux et de "
         "la pression transmembranaire ; une mesure pluriquotidienne de la température pour "
         "l'EER continue ; un bilan hydrique en fin de séance et chaque jour pour l'EER "
         "continue ; un ionogramme sanguin en fin de séance et toutes les 12 heures pour l'EER "
         "continue ; une évaluation quotidienne (et à chaque modification de posologie) de "
         "l'activité systémique de l'anticoagulant pour l'EER continue ; la mesure quotidienne "
         "de la gazométrie artérielle et à chaque changement du débit de restitution en "
         "bicarbonates au cours de l'hémofiltration continue.", "Fort"),
        ("EER — Citrate", "Dans le cas particulier d'un traitement antithrombotique au citrate, "
         "il faut doser toutes les quatre heures en état stable le calcium ionisé.", "Faible"),
        ("EER — Procédure", "La sécurisation de l'EER continue et intermittente nécessite, en "
         "sus de la surveillance clinique déjà décrite, la mise en place d'une procédure écrite, "
         "facilement disponible.", "Fort"),
        ("EER — Procédure", "Cette procédure doit comporter, en sus de la surveillance déjà "
         "décrite, la description des techniques de montage et de purge du circuit "
         "extracorporel, des techniques de branchement et de débranchement, des paramètres de "
         "surveillance du circuit, et du choix de la composition des solutions pour dialyse et "
         "hémofiltration et de leur remplacement en cours de traitement.", "Fort"),
        ("EER — Générateurs", "Une procédure de désinfection interne des générateurs entre les "
         "séances d'hémodialyse doit être mise en place.", "Fort"),
        ("EER — Qualité de l'eau", "Les responsables d'un service de réanimation dans lequel "
         "sont réalisées des séances d'hémodialyse par un générateur fabriquant un dialysat à "
         "partir de l'eau de distribution publique doivent faire partie des acteurs impliqués "
         "dans le processus de gestion de la qualité de l'eau.", "Fort"),
        ("EER — Qualité de l'eau", "Un tel service doit disposer d'une procédure d'alerte en cas "
         "de non-conformité chimique ou microbiologique de l'eau pour hémodialyse.", "Fort"),
        ("EER — Qualité de l'eau", "La recherche d'un résidu de solution désinfectante dans le "
         "dialysat doit être systématique avant tout branchement d'une séance d'hémodialyse "
         "réalisée par un tel générateur.", "Fort"),
    ]))
    return story

def _section_champ8_indecision():
    story = []
    story.append(Spacer(1, 2 * mm))
    story.append(section_bar("Champ 8 — Spécificités pédiatriques"))
    story.append(Spacer(1, 2 * mm))
    story.append(theme_table([
        ("Pédiatrie", "Tout service de réanimation pédiatrique devrait disposer d'un tableau de "
         "dilution des catécholamines précisant la correspondance entre le débit (mL/h) et la "
         "dose (µg/min).", "Fort"),
        ("Pédiatrie", "Le matériel de monitorage doit être doté d'alarmes adaptées à l'âge de "
         "l'enfant.", "Fort"),
        ("Pédiatrie", "Lorsqu'une voie fémorale a été mise en place dans un contexte d'urgence, "
         "son maintien doit être reconsidéré au bout de 48 heures.", "Fort"),
        ("Pédiatrie", "Les lignes de perfusion artérielle doivent toujours être raccordées à une "
         "tête de pression.", "Fort"),
        ("Pédiatrie", "Un matériel spécifique (pompes, tubulures et sondes), adapté et "
         "clairement identifié, doit être utilisé pour éviter le risque de confusion entre les "
         "perfusions (artérielles ou veineuses) et l'alimentation.", "Fort"),
        ("Pédiatrie", "Une boîte d'intubation pédiatrique doit comporter des lames droites et "
         "des lames courbes de toutes les tailles existantes.", "Fort"),
        ("Pédiatrie", "L'usage de l'aspiration en système clos doit être strictement limité aux "
         "situations où le dérecrutement a des conséquences significatives et persistantes sur "
         "l'oxygénation.", "Fort"),
        ("Pédiatrie", "Tout pôle de réanimation pédiatrique doit être équipé de masques de "
         "ventilation manuelle adaptés à la taille de l'enfant.", "Fort"),
        ("Pédiatrie", "Tout service de réanimation pédiatrique doit pouvoir réaliser des "
         "épurations extra-rénales.", "Faible"),
        ("Pédiatrie", "Les techniques d'EER (cathéters, moniteur, volume extracorporel, débit) "
         "doivent être adaptées à la taille de l'enfant.", "Fort"),
        ("Pédiatrie", "La dialyse péritonéale est une méthode d'EER qui reste utilisable en "
         "réanimation pédiatrique.", "Fort"),
        ("Pédiatrie", "Le maintien de l'expertise du personnel pédiatrique en technique d'EER "
         "fait partie d'une formation continue spécifique.", "Fort"),
    ]))
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("Zone d'indécision — 3 propositions (ni accord ni désaccord)", color=AMBER))
    story.append(Spacer(1, 2 * mm))
    story.append(P(
        "Le texte source identifie explicitement ces trois propositions comme scorées par les "
        "experts dans la <b>zone d'indécision</b> (médiane 4–6, ni accord ni désaccord) — "
        "catégorie distincte, reproduite ici telle quelle plutôt que reclassée en « fort » ou "
        "« faible ».", S_BODY_SM))
    story.append(Spacer(1, 2 * mm))
    story.append(theme_table([
        ("Extubation", "L'administration de corticoïdes par voie IV au moins six heures avant "
         "l'extubation peut être proposée.", "Indécision"),
        ("Extubation", "Si une extubation est prévue, il peut être proposé d'utiliser un guide "
         "échangeur pour faciliter la réintubation éventuelle.", "Indécision"),
        ("Déplétion", "Lorsqu'il est réalisé une déplétion chez un patient à risque, il est "
         "nécessaire de mettre en place un monitorage de la précharge ventriculaire adapté aux "
         "conditions du patient.", "Indécision"),
    ]))
    story.append(Spacer(1, 4 * mm))
    story.append(P("Fiche de synthèse indépendante, produite pour un usage d'aide-mémoire. Elle "
                    "reprend l'intégralité des propositions du texte source (y compris les "
                    "propositions non cotées et la zone d'indécision, disclosées comme telles), "
                    "mais ne remplace pas le texte intégral et n'est ni éditée ni validée par la "
                    "SRLF ou la SFAR. En cas de doute, se référer au texte intégral et/ou à un "
                    "avis spécialisé. Risque infectieux explicitement exclu du champ de ce "
                    "document — voir les référentiels dédiés.", S_SOURCE))
    return story

def _section_all():
    return (_section_intro() + [Spacer(1, 3 * mm)]
            + _section_champ1() + [Spacer(1, 3 * mm)]
            + _section_champ2() + [Spacer(1, 3 * mm)]
            + _section_champ3() + [Spacer(1, 3 * mm)]
            + _section_champ4() + [Spacer(1, 3 * mm)]
            + _section_champ5() + [Spacer(1, 3 * mm)]
            + _section_champ6() + [Spacer(1, 3 * mm)]
            + _section_champ7() + [Spacer(1, 3 * mm)]
            + _section_champ8_indecision())

SECTIONS = [
    ("2008 — 8 champs, accord fort/faible + zone d'indécision", _section_all),
]

def _make_doc(path=None):
    return SimpleDocTemplate(path or OUT, pagesize=A4,
                              leftMargin=MARGIN, rightMargin=MARGIN,
                              topMargin=32 * mm, bottomMargin=16 * mm,
                              title="SRLF/SFAR 2008 - Securisation des procedures a risques en reanimation",
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
    # Throwaway temp path (never OUT): reusing OUT for measurement passes corrupts page 1's
    # header_band in the final build (documented bug, see fiche_aap_programmee.py).
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
