# -*- coding: utf-8 -*-
"""
Fiche de synthese - Recommandations Formalisees d'Experts (RFE), sous l'egide de
la SRLF, de la SFAR et de la SFMU (2011) : "Transport intrahospitalier des
patients a risque vital (nouveau-ne exclu)". J.-P. Quenot, C. Milesi, A.
Cravoisy, et al. Source : sources/transport_intrahospitalier.pdf (5 pages),
sources/transport_intrahospitalier.txt (texte extrait, 563 lignes, incluant les
sauts de page).

Pas de tampon d'obsolescence sur la page 1 du PDF source (verifie a la lecture
integrale du texte extrait) ; library_final.json marque ce document "en
vigueur".

METHODOLOGIE - UN SEUL NIVEAU DE FORCE, PAS DE GRADE : la source decrit une
cotation RAND/UCLA a deux tours (echelle 1-9 ; zone 1-3 = desaccord, 4-6 =
indecision, 7-9 = accord ; qualifie de "fort" si la mediane reste a l'interieur
d'une des trois zones, "faible" si elle empiete sur une borne), explicitement
"inspiree de GRADE" mais SANS grade de preuve 1+/1-/2+/2- applique aux
propositions elles-memes. VERIFIE PAR GREP EXHAUSTIF (grep -no
'Accord fort|accord fort|Accord faible|accord faible' sur le texte source
extrait) : les 99 propositions portent TOUTES le tag "Accord fort" (une seule
occurrence en minuscules, item 41 du Champ 3, meme sens) - AUCUNE occurrence de
"faible" nulle part dans le document. La colonne Accord est donc constante,
retranscrite telle quelle sur chaque ligne (convention deja etablie par
fiche_tih.py pour un document au meme schema a un seul niveau).

PERIMETRE - 5 champs, 99 propositions numerotees 1 a 19 / 1 a 44 / 1 a 18 / 1 a
8 / 1 a 10, TOUTES couvertes (verifie par comptage regex des puces "N)" sur le
texte source : 19+44+18+8+10 = 99, sequentiel sans saut dans chaque champ).
Champ 1 (epidemiologie/taxonomie EI-EIG-EPR), Champ 2 (materiels/monitorage/
maintenance, le plus dense), Champ 3 (preparation du malade), Champ 4
(ressources humaines/formation), Champ 5 (organisation/architecture/
tracabilite). Reformulations condensees pour tenir en tableau (memes seuils,
memes qualificatifs "accord fort", aucune valeur numerique/clinique omise) ;
aucun tableau ni figure image dans la source (texte pur integral, verifie par
lecture complete du texte extrait - pas de table binaire a re-rendre en PNG).

DISCLOSURE - aucune incoherence source-interne detectee (comptage numerote
1-19/1-44/1-18/1-8/1-10 coherent avec le decompte annonce par les intertitres
"CHAMP 1" a "CHAMP 5" ; pas de divergence entre un total annonce et un tally
direct).

CONVENTION DE CHIP : extension locale non invasive de GRADE_COLORS - "Fort" ->
vert, reprenant la meme convention que fiche_tih.py / fiche_mal_epileptique.py /
fiche_nutrition.py.

ICONE : icon_shield (bouclier/securite), theme naturel pour un texte centre sur
la securisation d'un transport a risque.

_count_pages() : implementation copiee a l'identique de fiche_aap_programmee.py
- les passes de comptage ecrivent vers un tempfile.mktemp() jetable, jamais vers
OUT (bug de corruption du header_band de la page 1 deja documente si l'on
reutilise OUT pour le comptage ET la construction finale).
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from style import *
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.units import mm

GRADE_COLORS["Fort"] = (GREEN, WHITE)

OUT = "/home/user/rfe-sfar-website/output/Fiche_SRLF_SFAR_SFMU_Transport_Intrahospitalier_2011.pdf"

SOURCE_TXT = ("Source : Quenot J.-P., Milesi C., Cravoisy A., et al. — Recommandations "
              "formalisées d'experts SRLF/Sfar/SFMU (2011) « Transport intrahospitalier des "
              "patients à risque vital (nouveau-né exclu) ». Fiche de synthèse non officielle : "
              "se référer au texte intégral.")

def P(txt, style=S_CELL):
    return Paragraph(txt, style)

def chip(label, **kw):
    return grade_chip(label, **kw)

REF_W = 11 * mm
ACCORD_W = 18 * mm

def prop_table(rows, col_widths=None):
    """rows: (ref, text) - Accord est systematiquement 'Fort' dans ce document
    (voir docstring module) donc non passe en parametre par ligne."""
    text_w = PAGE_W - 2 * MARGIN - REF_W - ACCORD_W
    cw = col_widths or [REF_W, text_w, ACCORD_W]
    data = [[P("N°", S_HEAD_W_C), P("Recommandation (texte condensé, fidèle à la source)", S_HEAD_W), P("Accord", S_HEAD_W_C)]]
    for ref, txt in rows:
        data.append([P(ref, S_CELL_C), P(txt, S_CELL), chip("Fort", width=ACCORD_W - 2 * mm)])
    t = Table(data, colWidths=cw, repeatRows=1)
    style_cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), NAVY), ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTNAME", (0, 0), (-1, 0), FONT_BOLD), ("FONTSIZE", (0, 0), (-1, 0), 8),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("ALIGN", (0, 0), (0, -1), "CENTER"),
        ("ALIGN", (2, 0), (2, -1), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 0.5, GREY_LIGHT),
        ("TOPPADDING", (0, 0), (-1, -1), 3.0), ("BOTTOMPADDING", (0, 0), (-1, -1), 3.0),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            style_cmds.append(("BACKGROUND", (0, i), (-1, i), BG_PANEL))
    t.setStyle(TableStyle(style_cmds))
    return t

TOTAL_PAGES = {"n": 8}

def on_page(canvas, doc, page_title):
    header_band(canvas, doc, "SRLF / SFAR / SFMU — RFE 2011 — FICHE DE SYNTHÈSE",
                "Transport intrahospitalier des patients à risque vital",
                page_title, icon_fn=lambda c, x, y: icon_shield(c, x, y, 13 * mm), color=NAVY)
    footer_band(canvas, doc, SOURCE_TXT, f"Page {doc.page} / {TOTAL_PAGES['n']}")

# ---------------------------------------------------------------------------
def _section_intro_champ1():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Champ d'application :</b> tout <b>transport intrahospitalier (TIH)</b> d'un patient "
        "à risque vital (au moins une défaillance ou menace de défaillance vitale), <b>nouveau-né "
        "exclu</b> — pour une procédure diagnostique, thérapeutique, ou une admission dans une "
        "unité spécialisée. Recommandations sous l'égide de la SRLF, de la Sfar et de la SFMU. "
        "<b>5 champs, 99 propositions.</b>", S_BODY), bg=BG_PANEL, border=TEAL))
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Méthodologie — un seul niveau de force, pas de grade de preuve (1+/1-/2+/2-) :</b> "
        "cotation RAND/UCLA à deux tours par le groupe d'experts, échelle 1 à 9 (zone 1-3 = "
        "« désaccord », 4-6 = « indécision », 7-9 = « accord »), qualifiée de <b>« forte »</b> si "
        "l'intervalle de la médiane reste à l'intérieur d'une des trois zones, de « faible » s'il "
        "empiète sur une borne. Méthode inspirée de GRADE mais sans grade de preuve. "
        "<b>Les 99 propositions de ce document ont toutes recueilli un accord fort</b> (vérifié "
        "exhaustivement, aucune occurrence de « faible ») — la colonne Accord est donc constante, "
        "reproduite telle quelle par fidélité à la source qui l'imprime après chaque proposition.",
        S_BODY_SM), bg=BG_PANEL, border=TEAL))
    story.append(Spacer(1, 3 * mm))

    story.append(section_bar("Champ 1 — Épidémiologie des événements indésirables (EI)"))
    story.append(Spacer(1, 2 * mm))
    story.append(P(
        "<b>EIG</b> (événement indésirable grave) : complication directement liée aux soins, "
        "pouvant entraîner un risque vital, une prolongation de séjour, la nécessité de gestes "
        "invasifs, des séquelles invalidantes. <b>EPR</b> (événement porteur de risque) : défini "
        "par le décret sur l'accréditation des médecins des spécialités à risque — regroupe tous "
        "les EI hors EIG (incidents patients mineurs, dysfonctions matériel/organisation).",
        S_BODY_SM))
    story.append(Spacer(1, 2 * mm))
    story.append(prop_table([
        ("1", "Les patients à risque vital, hospitalisés ou non en réanimation, nécessitent "
         "fréquemment un TIH pour une procédure diagnostique, thérapeutique ou une admission "
         "dans une unité spécialisée."),
        ("2", "Les patients à risque vital regroupent l'ensemble des patients présentant au "
         "moins une défaillance ou menace de défaillance vitale."),
        ("3", "Il faut standardiser les définitions des EI et de leur évitabilité au cours du "
         "TIH."),
        ("4", "Les EI sont classés selon leur gravité en deux catégories : les EIG et les EPR."),
        ("5", "Un EIG est une complication directement liée aux soins, pouvant entraîner un "
         "risque vital, une prolongation de séjour, la nécessité de gestes invasifs et des "
         "séquelles invalidantes."),
        ("6", "Les EPR sont définis par le décret sur l'accréditation des médecins exerçant "
         "dans les spécialités à risque : ils regroupent tous les EI à l'exclusion des EIG "
         "(EI patients mineurs, dysfonctions du matériel et/ou de l'organisation)."),
        ("7", "Des incidents sans gravité surviennent régulièrement lors du transport : il faut "
         "définir précisément les EIG/EPR les plus fréquents pour mettre en place des "
         "procédures de surveillance et des mesures correctrices."),
        ("8", "Un EI survenant pendant le transport, nécessitant une intervention thérapeutique "
         "et résolutif après, doit être considéré comme un EPR."),
        ("9", "Un EI nécessitant une intervention thérapeutique qui ne permet pas de corriger "
         "l'anomalie selon l'objectif fixé par le clinicien doit être considéré comme un EIG."),
        ("10", "Un EPR compliqué d'une auto-extubation et/ou d'un arrêt cardiaque est un EIG."),
        ("11", "Une désaturation nécessitant une augmentation de FiO2 ou un autre réglage du "
         "ventilateur est un EPR ; c'est un EIG dès lors qu'elle n'est pas corrigée et reste "
         "sous l'objectif fixé par le clinicien."),
        ("12", "Une baisse de la pression artérielle nécessitant un geste thérapeutique est un "
         "EPR ; c'est un EIG dès lors que le traitement n'atteint pas l'objectif fixé."),
        ("13", "Un état d'agitation ou une désadaptation du respirateur nécessitant un geste "
         "thérapeutique est un EPR ; c'est un EIG s'il n'est pas corrigé par la mesure "
         "thérapeutique."),
        ("14", "Un problème lié au ventilateur nécessitant une modification de réglage, une "
         "ventilation au BAVU ou un changement de matériel est un EPR."),
        ("15", "Un problème lié au ventilateur qui se complique d'un événement clinique est un "
         "EIG."),
        ("16", "Les arrachements de matériels (cathéters, drain, pression intracrânienne...) "
         "sont des EPR sans conséquence clinique directe ; ce sont des EIG dès lors qu'ils sont "
         "compliqués."),
        ("17", "Un EI survenant lors du TIH doit être considéré comme inévitable lorsque "
         "l'ensemble de la procédure a été réalisé conformément à l'état de l'art."),
        ("18", "Les procédures de sécurisation (« safety practices ») sont des procédures de "
         "soins et/ou structurelles/organisationnelles qui préviennent, diminuent la fréquence "
         "ou atténuent les conséquences des erreurs et des EI survenant lors du TIH."),
        ("19", "Il faut faire un signalement des EI pouvant survenir pendant le TIH, qui devront "
         "ensuite être analysés."),
    ]))
    return story

def _section_champ2():
    story = []
    story.append(Spacer(1, 2 * mm))
    story.append(section_bar("Champ 2 — Matériels, monitorage et maintenance (44 propositions)"))
    story.append(Spacer(1, 2 * mm))
    story.append(prop_table([
        ("1", "Le choix de l'équipement doit prendre en compte son encombrement et son "
         "autonomie."),
        ("2", "Il faut vérifier toutes les connexions entre les matériels de monitorage (ex. "
         "capteurs de pression invasive) avant le TIH."),
        ("3", "Le monitorage minimum durant un TIH comprend la fréquence cardiaque "
         "électrocardioscopique, l'oxymétrie de pouls et la pression artérielle non invasive."),
        ("4", "Chez le patient non ventilé, la fréquence ventilatoire doit être surveillée à "
         "intervalle régulier, au mieux de façon monitorée."),
        ("5", "Le monitorage de l'EtCO2 est recommandé pour les patients ayant une souffrance "
         "neurologique et pour ceux nécessitant un contrôle strict de la PaCO2."),
        ("6", "Les principaux paramètres monitorés doivent être couplés à des alarmes dont le "
         "réglage est adapté à chaque patient."),
        ("7", "Il faut un matériel dédié au TIH et identifié au niveau d'une structure de soins, "
         "d'un service ou d'un pôle."),
        ("8", "Le ventilateur de transport doit disposer d'alarmes sonores et visuelles sur les "
         "principaux paramètres ventilatoires monitorés."),
        ("9", "Pour tout patient ventilé lors d'un transport long ou à risque particulier, il "
         "faut disposer immédiatement d'un système d'aspiration, au mieux un appareil "
         "électrique autonome portable."),
        ("10", "Il faut adapter l'autonomie en électricité et en gaz médicaux à la durée du TIH "
         "et à la consommation, et en surveiller l'autonomie restante."),
        ("11", "Les moyens de monitorage doivent être adaptés au type de transport, à la "
         "sévérité du patient et aux thérapeutiques utilisées, selon une procédure écrite."),
        ("12", "La ventilation manuelle au ballon autogonflable doit être évitée lors d'un TIH, "
         "et n'être utilisée qu'en cas de panne du ventilateur (y compris chez l'enfant)."),
        ("13", "Le réglage des consignes machine du ventilateur de transport doit permettre les "
         "mêmes paramètres de ventilation, y compris les modes non invasifs."),
        ("14", "Tout patient ventilé lors d'un TIH doit pouvoir être repris à tout moment, en "
         "ventilation au ballon sur sa prothèse endotrachéale ou au masque."),
        ("15", "Les performances réelles du ventilateur de transport doivent être connues de "
         "l'utilisateur, selon trois catégories : <b>basique/secours</b> (mode VC, PEP, "
         "monitorage réduit) ; <b>intermédiaire</b> (mode VAC, PEP, réglage du débit ou de "
         "l'I/E, spirométrie expiratoire, réglage FiO2 100 %/mélange air-oxygène) ; <b>haute "
         "performance</b> (modes volumétriques/barométriques dont VS-AI-PEP, large plage de "
         "réglage de la FiO2, réglage du débit d'insufflation, triggers performants, "
         "spirométrie expiratoire, au mieux compensation de la compliance du circuit, mode "
         "VNI)."),
        ("16", "La performance, le monitorage et les alarmes du ventilateur doivent être adaptés "
         "à la pathologie : patient très hypoxémique (ex. SDRA) → haute performance ; contrôle "
         "strict de la PaCO2 ou modes assistés → intermédiaire/haute performance ; patient en "
         "VNI → option VNI performante."),
        ("17", "Le mode d'alimentation électrique et de recharge du ventilateur doit être "
         "compatible avec son utilisation à tout moment et avoir une autonomie suffisante."),
        ("18", "Le ventilateur utilisé doit disposer d'une alarme de défaut d'alimentation en "
         "gaz, en électricité, et d'une alarme de panne."),
        ("19", "L'interface du ventilateur de transport ne doit pas permettre de déréglages "
         "accidentels des consignes machine."),
        ("20", "À performances comparables, le ventilateur ayant l'interface la plus simple et "
         "le circuit patient le plus simple doit être privilégié."),
        ("21", "Pour vérifier la bonne tolérance de la ventilation et la stabilité du malade, le "
         "ventilateur de transport doit être branché sur le patient 5 à 10 minutes avant le "
         "départ réel, sur les gaz muraux et l'alimentation secteur."),
        ("22", "Le ventilateur de transport doit être stocké dans un endroit accessible connu "
         "des utilisateurs, avec ses accessoires (circuit complet avec ECH et raccord annelé, "
         "tuyau d'alimentation en gaz médicaux)."),
        ("23", "Le circuit utilisé doit être en accord avec les recommandations du fabricant."),
        ("24", "Lorsque le ventilateur le nécessite, il doit être étalonné en fonction du type "
         "de circuit utilisé."),
        ("25", "Un filtre antibactérien et échangeur de chaleur et d'humidité (ECH) doit être "
         "systématiquement mis en place entre le raccord annelé et le circuit patient."),
        ("26", "Le réglage des consignes machine et des alarmes du ventilateur de transport doit "
         "faire l'objet d'une prescription écrite."),
        ("27", "Le monitorage de la ventilation par le ventilateur de transport doit comporter au "
         "minimum la surveillance de la pression d'insufflation (pic) et la spirométrie "
         "expiratoire."),
        ("28", "Une auto-extubation doit pouvoir être identifiée immédiatement par le monitorage "
         "de la capnographie et/ou de la spirométrie expiratoire."),
        ("29", "L'analyse de la phase expiratoire du capnogramme peut aider à identifier certaines "
         "complications de la ventilation au cours du transport."),
        ("30", "En mode VS-AI-PEP (invasive ou non), le ventilateur de transport doit avoir les "
         "caractéristiques générales requises (performances, monitorage) pour garantir la "
         "qualité de ventilation."),
        ("31", "Certains ventilateurs de transport proposent des modes pouvant évoquer la "
         "VS-AI-PEP mais qui n'en sont pas réellement : il ne faut pas les utiliser."),
        ("32", "En mode CPAP, les systèmes à débit libre indépendants des ventilateurs doivent "
         "être utilisés en tenant compte de leur consommation d'oxygène importante, ce mode "
         "n'étant pas assez performant sur les ventilateurs de transport."),
        ("33", "Un dispositif de mesure invasive et continue de la pression artérielle doit être "
         "utilisé lors du TIH si le patient est traité par des agents vaso-actifs et/ou en cas "
         "d'instabilité hémodynamique, et s'il en bénéficie déjà dans son unité."),
        ("34", "Le monitorage de la pression veineuse centrale n'est pas recommandé lors du "
         "TIH."),
        ("35", "Un stimulateur-défibrillateur doit être facilement accessible au cours du "
         "transport ; au mieux, il s'intègre dans un moniteur multiparamétrique."),
        ("36", "Si le patient est dépendant d'un pacemaker externe, les seuils de celui-ci "
         "doivent être impérativement vérifiés et adaptés, ainsi que l'état de la batterie ; un "
         "pacemaker externe de rechange doit être impérativement disponible."),
        ("37", "En présence d'électrodes de stimulation péricardiques temporaires, un stimulateur "
         "de transport doit être impérativement connecté."),
        ("38", "Le remplacement dans les meilleurs délais d'un matériel indisponible "
         "(maintenance, panne) doit être organisé selon une procédure écrite."),
        ("39", "Les matériels utilisés pour le TIH doivent faire l'objet d'une procédure de "
         "contrôle régulière et tracée (check-list)."),
        ("40", "Après utilisation, le ventilateur doit être nettoyé et désinfecté selon une "
         "procédure écrite et tracée."),
        ("41", "Lors d'un TIH pédiatrique, un jeu complet de matériel et de médicaments de "
         "réanimation pédiatrique doit accompagner l'enfant, notamment un ballon autogonflable, "
         "un masque facial et du matériel d'intubation adaptés à l'âge, ainsi que du matériel de "
         "cathétérisme intra-osseux."),
        ("42", "Le monitorage de l'EtCO2 est recommandé lors du transport en cas de ventilation "
         "manuelle d'un enfant intubé, pour prévenir le risque d'hyperventilation."),
        ("43", "Pour les enfants de moins de 15 kg, il est nécessaire d'avoir un ventilateur "
         "pouvant délivrer des volumes courants faibles, assurer des fréquences élevées et "
         "permettre le maintien d'une pression positive de fin d'expiration."),
        ("44", "La taille et la compliance des tuyaux du circuit doivent être adaptées à l'âge et "
         "au poids de l'enfant pour réduire au maximum le volume compressible (petits tuyaux "
         "pour un poids inférieur à 15 kg)."),
    ]))
    return story

def _section_champ345():
    story = []
    story.append(Spacer(1, 2 * mm))
    story.append(section_bar("Champ 3 — Préparation du malade avant transport (18 propositions)"))
    story.append(Spacer(1, 2 * mm))
    story.append(prop_table([
        ("1", "Il faut faire une évaluation précise de l'état clinique du patient avant le "
         "départ pour un TIH et évaluer le bénéfice/risque du transport ; ces éléments doivent "
         "être colligés dans le dossier médical."),
        ("2", "Il faut vérifier l'absence de contre-indication aux examens complémentaires."),
        ("3", "Le patient doit être porteur d'un bracelet d'identification."),
        ("4", "Il faut au minimum un abord veineux perméable et, si nécessaire, une voie "
         "supplémentaire spécifiquement dédiée aux amines et identifiée ; les voies d'abord "
         "doivent être propres et solidement fixées."),
        ("5", "Les pousse-seringues électriques doivent être identifiés et la quantité des "
         "thérapeutiques adaptée à la durée du TIH ; les cordons d'alimentation doivent être "
         "présents durant le transport et rebranchés sur secteur dès que possible."),
        ("6", "Chez les patients nécessitant un contrôle strict de la PaCO2, un prélèvement "
         "artériel doit être réalisé avant le TIH afin de mesurer le gradient PaCO2-EtCO2."),
        ("7", "Le monitorage de la pression de perfusion cérébrale (PPC) doit être poursuivi au "
         "cours du transport chez les patients neurologiques."),
        ("8", "La position optimale du patient en réanimation doit être poursuivie pendant le "
         "TIH."),
        ("9", "Il faut anticiper, évaluer et traiter les douleurs pouvant être induites par le "
         "TIH et/ou les soins qui seront réalisés."),
        ("10", "Il faut poursuivre la sédation et/ou l'analgésie durant le transport ; elle peut "
         "être modifiée le cas échéant."),
        ("11", "La mobilisation du patient curarisé doit faire l'objet de précautions "
         "particulières."),
        ("12", "Le matériel d'intubation complet (comprenant un mandrin d'Eschmann) doit être "
         "disponible immédiatement."),
        ("13", "À chaque mobilisation du patient, la vérification de la bonne position des "
         "dispositifs invasifs doit être effectuée."),
        ("14", "Un BAVU avec masque adapté, réservoir d'oxygène, prolongateur d'O2 et filtre de "
         "rechange doivent accompagner le patient."),
        ("15", "Il faut prévenir l'hypothermie pendant le TIH, notamment chez l'enfant où la "
         "température devra être monitorée."),
        ("16", "Le matériel à usage unique doit être privilégié."),
        ("17", "La pression du ballonnet du dispositif intratrachéal doit être vérifiée avant et "
         "au retour du TIH."),
        ("18", "Un sac d'intervention d'urgence doit accompagner le patient."),
    ]))
    story.append(Spacer(1, 3 * mm))

    story.append(section_bar("Champ 4 — Soignants : ressources humaines et formation (8 propositions)"))
    story.append(Spacer(1, 2 * mm))
    story.append(prop_table([
        ("1", "Une formation initiale et régulière est obligatoire pour l'ensemble des personnels "
         "assurant les TIH, sur le fonctionnement et la surveillance des matériels utilisés "
         "(ventilateur, moniteur multiparamétrique, défibrillateur...)."),
        ("2", "Il faut une formation au transport pédiatrique, initiale et régulière, du "
         "personnel médical et paramédical assurant les TIH des enfants de moins de 15 kg."),
        ("3", "La formation des personnels en charge des TIH peut se faire sous la forme d'une "
         "simulation de transport."),
        ("4", "L'appréciation du risque et les modalités liées au TIH sont sous la responsabilité "
         "du médecin senior en charge du patient."),
        ("5", "L'équipe de TIH d'un patient à risque vital doit être composée au minimum d'un "
         "médecin expérimenté et d'une personne formée au TIH."),
        ("6", "Une procédure d'appel à l'aide pour un renfort médical et/ou infirmier doit être "
         "disponible et connue de tous en cas de problème lors du TIH."),
        ("7", "Un perfusionniste ou équivalent qualifié doit faire partie de l'équipe de TIH "
         "lorsque le patient est sous circulation extracorporelle (CEC)."),
        ("8", "Si le TIH est confié à l'équipe médicale du Smur, celle-ci doit bénéficier d'une "
         "transmission complète et précise sur l'état du patient par le médecin en charge, et "
         "d'un compte rendu écrit."),
    ]))
    story.append(Spacer(1, 3 * mm))

    story.append(section_bar("Champ 5 — Organisation, architecture et traçabilité (10 propositions)"))
    story.append(Spacer(1, 2 * mm))
    story.append(prop_table([
        ("1", "L'horaire, le lieu de rendez-vous ainsi que la durée d'immobilisation du patient "
         "doivent être précisés et vérifiés avant le TIH."),
        ("2", "Le nom du médecin et les moyens techniques à disposition sur le lieu d'accueil du "
         "patient doivent être connus."),
        ("3", "Avant de partir pour un TIH, il faut s'assurer de la connaissance du circuit "
         "emprunté et de l'accessibilité des couloirs et ascenseurs, en privilégiant le chemin "
         "le plus court et le plus sécurisé."),
        ("4", "Le service d'accueil est prévenu de l'arrivée imminente du patient."),
        ("5", "La traçabilité des paramètres monitorés lors du TIH doit faire l'objet d'un "
         "recueil spécifique sur une feuille de surveillance, ensuite intégrée au dossier du "
         "patient."),
        ("6", "Une traçabilité imprimable des données du monitorage au cours du TIH est "
         "souhaitable."),
        ("7", "Si le médecin qui accueille le patient est compétent pour assurer sa "
         "surveillance, l'équipe de TIH lui transmettra toutes les informations nécessaires."),
        ("8", "En l'absence d'un médecin compétent pour la surveillance du patient sur le lieu "
         "d'accueil, l'équipe du TIH en conservera la charge."),
        ("9", "L'organisation du TIH doit faire l'objet d'une procédure institutionnelle."),
        ("10", "Le TIH doit être un acte valorisé en termes d'activité."),
    ]))
    story.append(Spacer(1, 4 * mm))
    story.append(P("Fiche de synthèse indépendante, produite pour un usage d'aide-mémoire. Elle "
                    "reprend l'intégralité des 99 propositions du texte source, mais ne remplace "
                    "pas le texte intégral et n'est ni éditée ni validée par la SRLF, la Sfar ou "
                    "la SFMU. En cas de doute, se référer au texte intégral et/ou à un avis "
                    "spécialisé.", S_SOURCE))
    return story

def _section_all():
    return (_section_intro_champ1() + [Spacer(1, 3 * mm)] + _section_champ2()
            + [Spacer(1, 3 * mm)] + _section_champ345())

SECTIONS = [
    ("RFE 2011 — 5 champs, 99 propositions (accord fort)", _section_all),
]

def _make_doc(path=None):
    return SimpleDocTemplate(path or OUT, pagesize=A4,
                              leftMargin=MARGIN, rightMargin=MARGIN,
                              topMargin=32 * mm, bottomMargin=16 * mm,
                              title="RFE SRLF/Sfar/SFMU 2011 - Transport intrahospitalier des patients à risque vital",
                              author="Synthèse indépendante (source SRLF/Sfar/SFMU)")

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
    # Uses PyMuPDF (fitz) rather than pypdf: this environment's pypdf pulls in a broken
    # cryptography/_cffi_backend install (pyo3 panic on import) - fitz is already a hard
    # dependency of this pipeline's own PNG-rendering QA step, so it's known-good here.
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
