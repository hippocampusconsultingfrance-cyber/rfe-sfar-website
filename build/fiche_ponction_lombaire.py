# -*- coding: utf-8 -*-
"""
Fiche de synthese - Haute Autorite de Sante (HAS), fiche memo, juin 2019.
"Prevention et prise en charge des effets indesirables pouvant survenir apres
une ponction lombaire". 7 pages, telecharge depuis has-sante.fr
(upload/docs/application/pdf/2019-07/fm_ponction_lombaire.pdf).

METHODOLOGIE : ce document est une "fiche memo" HAS - PAS une RFE/RBP/RPC avec
vote gradue. Il n'y a AUCUNE mention "GRADE", AUCUN tag 1+/2+/AE, AUCUN systeme
d'accord fort/faible nulle part dans le texte source. C'est une synthese de
litterature presentee sous forme de messages cles et de recommandations de
pratique narratives, sans cotation individuelle. 8e convention methodologique
distincte rencontree dans ce corpus (ne pas inventer de chip GRADE ou "Fort" -
a la difference de fiche_bris_dentaires.py / fiche_aap_programmee.py, aucune
mention meme globale de type "accord fort lors du vote" n'existe ici). Le
contenu est donc restitue en panneaux d'information et tableaux thematiques
(theme/detail), jamais en reco_table avec chip.

COUVERTURE : fiche memo integrale, 7 pages source, ~16 000 caracteres extraits.
Sections retranscrites : messages cles (page 1, 9 puces) ; indications
diagnostiques et therapeutiques + contre-indications formelles (page 2) ;
modalites de realisation - installation, repere, asepsie, anesthesie locale,
technique de l'aiguille, reintroduction du mandrin, prelevements, prevention
AES, formation (pages 3-4) ; effets indesirables - syndrome post-PL, signes
d'alerte de complication grave, hematomes, infections, douleurs lombaires
(pages 4-5) ; blood-patch (page 6) ; specificites pediatriques - installation,
choix de l'aiguille, angle de ponction, analgesie, syndrome post-PL chez
l'enfant, prevention et prise en charge (pages 6-7). Rien n'est omis.

NOTE SOURCE : le fichier texte extrait contient 3 occurrences d'une ligne
"..." isolee (fin des pages 3, 4 et 6) - verifie visuellement : il s'agit d'un
filet decoratif en pointilles dans la mise en page du PDF, pas de texte
manquant ni de troncature d'extraction.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from style import *
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.units import mm

OUT = "/home/user/rfe-sfar-website/output/Fiche_HAS_Ponction_Lombaire_2019.pdf"

SOURCE_TXT = ("Source : « Prévention et prise en charge des effets indésirables pouvant "
              "survenir après une ponction lombaire » — Fiche mémo, Haute Autorité de "
              "Santé (HAS), juin 2019. Fiche de synthèse non officielle : se référer au "
              "texte intégral.")

def P(txt, style=S_CELL):
    return Paragraph(txt, style)

CW_FULL = PAGE_W - 2 * MARGIN

def theme_table(rows, col_widths, head=("Thème", "Détail")):
    """rows: (theme, detail) - pas de gradation dans ce document."""
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

TCW = [42 * mm, CW_FULL - 42 * mm]

def bullets(items, style=S_BODY_SM):
    html = "&bull; " + "<br/>&bull; ".join(items)
    return P(html, style)

TOTAL_PAGES = {"n": 5}

def on_page(canvas, doc, page_title):
    header_band(canvas, doc, "HAS — FICHE MÉMO — JUIN 2019",
                "Effets indésirables de la ponction lombaire",
                page_title, icon_fn=lambda c, x, y: icon_shield(c, x, y, 13 * mm), color=NAVY)
    footer_band(canvas, doc, SOURCE_TXT, f"Page {doc.page} / {TOTAL_PAGES['n']}")

# ---------------------------------------------------------------------------
def _section_intro():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Champ :</b> prévention et prise en charge des effets indésirables de la "
        "ponction lombaire (PL), acte diagnostique ou thérapeutique fréquent, invasif, "
        "réalisable par tout médecin. La PL est à risque d'événements indésirables "
        "(exceptionnellement graves) et d'échecs dont la majorité serait évitable — d'où "
        "l'importance de connaître l'anatomie, les contre-indications, la technique, le "
        "matériel et la prévention de ces effets indésirables.", S_BODY), bg=BG_PANEL, border=TEAL))
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Méthodologie :</b> cette « fiche mémo » HAS est une <b>synthèse de la "
        "littérature</b> — elle ne comporte <b>aucun système GRADE</b> et <b>aucune "
        "cotation d'accord</b> (ni 1+/2+, ni « accord fort/faible »), à la différence des "
        "RFE/RBP à vote gradué du reste de ce corpus. Les recommandations sont donc "
        "restituées ici sous forme de messages clés et de tableaux thématiques, sans "
        "chip de force — aucune gradation n'est inventée.", S_BODY_SM), bg=AMBER_LIGHT, border=AMBER))
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("Messages clés"))
    story.append(Spacer(1, 2 * mm))
    story.append(bullets([
        "La PL est un acte médical indispensable et très fréquent.",
        "Le refus explicite ou présumé du patient et les contre-indications formelles "
        "(hypertension intracrânienne, infections au point de ponction, thrombopénie "
        "sévère) doivent être pris en considération avant toute PL.",
        "Les complications graves sont exceptionnelles.",
        "Le syndrome post-PL est l'effet indésirable le plus fréquent. S'il n'est "
        "habituellement pas grave, il est invalidant et engendre des coûts personnel, "
        "social et financier.",
        "Il est recommandé d'utiliser une aiguille atraumatique « à extrémité non "
        "tranchante », avec introducteur, quelle que soit l'indication de la PL réalisée, "
        "chez l'adulte comme en pédiatrie.",
        "Il est recommandé aux médecins de se former à la pratique du geste de la PL, "
        "ainsi qu'à l'utilisation des aiguilles atraumatiques avec introducteur, et de se "
        "faire accompagner pour la réalisation des premières PL sur le patient, aussi "
        "souvent que nécessaire.",
        "Le respect des règles de procédure et l'utilisation des aiguilles atraumatiques "
        "diminuent significativement l'incidence des effets indésirables et le recours au "
        "blood-patch.",
        "Le blood-patch est le traitement le plus performant du syndrome post-PL, mais "
        "c'est un acte invasif qui peut être responsable de complications iatrogènes, "
        "exceptionnellement graves.",
        "Le repos forcé au lit et l'hyperhydratation n'ont pas d'indication.",
        "La PL et le blood-patch sont des gestes invasifs avec risque d'accident "
        "d'exposition au sang : les aiguilles doivent être collectées dans un conteneur "
        "prévu à cet effet.",
    ], style=S_BODY_SM))
    return story

def _section_indications():
    story = []
    story.append(Spacer(1, 2 * mm))
    story.append(KeepTogether([
        section_bar("Dans quels cas une ponction lombaire peut être réalisée"),
        Spacer(1, 1.5 * mm),
        P("Les indications évoluent constamment avec le développement des connaissances "
          "et des techniques. Les indications suivantes sont listées à titre indicatif et "
          "de manière non exhaustive.", S_NOTE),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P("<b>Indications diagnostiques</b>", S_CELL_B))
    story.append(Spacer(1, 1 * mm))
    story.append(bullets([
        "suspicion d'infection du système nerveux central (bactérienne, virale, "
        "parasitaire) ;",
        "survenue d'une céphalée brutale et/ou atypique (hémorragie méningée, "
        "thrombophlébite, dissection vasculaire, etc.) ;",
        "suspicion d'une méningite carcinomateuse ou d'un syndrome paranéoplasique ;",
        "bilan de maladies inflammatoires affectant le système nerveux central (sclérose "
        "en plaques, sarcoïdose, vascularite, encéphalite auto-immune, etc.) ;",
        "bilan d'une neuropathie aiguë ou chronique (syndrome de Guillain-Barré, "
        "neuropathie périphérique, etc.) ;",
        "maladies neurodégénératives (maladie d'Alzheimer, sclérose latérale "
        "amyotrophique, maladie à corps de Lewy, etc.) ;",
        "mesure de pression du liquide cérébro-spinal (LCS) en cas de suspicion de "
        "troubles de la cinétique du LCS (hydrocéphalie à pression normale, hypertension "
        "intracrânienne idiopathique).",
    ]))
    story.append(Spacer(1, 2 * mm))
    story.append(P("<b>Indications thérapeutiques</b>", S_CELL_B))
    story.append(Spacer(1, 1 * mm))
    story.append(bullets([
        "ponction lombaire évacuatrice : hydrocéphalie à pression normale, après "
        "interventions neurochirurgicales ;",
        "rachianesthésie ;",
        "recherche clinique.",
    ]))
    story.append(Spacer(1, 3 * mm))
    story.append(KeepTogether([
        section_bar("Dans quels cas une ponction lombaire ne doit pas être réalisée", color=RED),
        Spacer(1, 1.5 * mm),
        P("Outre le refus explicite ou présumé du patient, les contre-indications "
          "formelles sont les suivantes.", S_NOTE),
        Spacer(1, 1.5 * mm),
        theme_table([
        ("Hypertension intracrânienne",
         "Risque d'engagement cérébral (processus expansif intracrânien, malformation "
         "d'Arnold-Chiari) — la normalité d'un examen neurologique minutieux permet de se "
         "passer de l'imagerie."),
        ("Infections au point de ponction", "Contre-indication formelle."),
        ("Thrombopénie sévère",
         "Nombre de plaquettes inférieur à 50 G/L (50 000/mm³). Pour certaines "
         "pathologies (thrombopénie gestationnelle, purpura thrombopénique immunologique), "
         "une thrombopénie stable ≥ 30 G/L peut être tolérée ; à l'inverse, une "
         "thrombopénie évolutive non stabilisée nécessite une évaluation "
         "pluridisciplinaire du rapport bénéfice/risque."),
        ("Troubles de la coagulation ou traitements modifiant l'hémostase",
         "L'hématome péridural ou sous-arachnoïdien après une PL est exceptionnel, "
         "presque toujours lié à un ou plusieurs facteurs de risque : traitement "
         "anticoagulant à dose thérapeutique ou antiplaquettaire (sauf aspirine et AINS), "
         "trouble congénital ou acquis de la coagulation/hémostase primaire, ponction "
         "difficile/traumatique ou rachis pathologique (ex. spondylarthrite ankylosante). "
         "En urgence : antagoniser le traitement anticoagulant si possible, ou substituer "
         "le déficit en facteurs de coagulation (ex. hémophilie) si nécessaire."),
        ], TCW),
    ]))
    return story

def _section_modalites():
    story = []
    story.append(Spacer(1, 2 * mm))
    story.append(section_bar("Modalités de réalisation de la ponction lombaire"))
    story.append(Spacer(1, 2 * mm))
    story.append(info_panel(P(
        "La PL doit être réalisée dans le cadre d'une hospitalisation (sa réalisation ne "
        "justifie pas, à elle seule, une hospitalisation de plus de 24 heures).",
        S_BODY_SM), bg=BG_PANEL, border=TEAL))
    story.append(Spacer(1, 2 * mm))
    story.append(theme_table([
        ("Installation du patient",
         "Le choix de la position assise ou allongée est laissé à l'appréciation du "
         "médecin et du patient."),
        ("Détermination du point de ponction",
         "Niveaux corrects : espaces interépineux L3-L4, L4-L5 et L5-S1. Il est recommandé "
         "de ponctionner en dessous de la ligne horizontale tracée entre les crêtes "
         "iliaques (la détermination de l'espace à ponctionner est en pratique plus "
         "difficile que classiquement décrit). En cas de difficulté, la PL peut être "
         "réalisée sous imagerie (radioscopie, échographie)."),
        ("Asepsie",
         "Règles d'asepsie chirurgicale à respecter absolument — pour le patient : "
         "désinfection cutanée en deux temps (antiseptique alcoolique) + champ stérile ; "
         "pour le médecin : désinfection des mains (solution hydro-alcoolique), masque "
         "facial, gants stériles."),
        ("Anesthésie locale",
         "Un patch d'anesthésique local peut être proposé en dehors de l'urgence (délai "
         "d'1 heure). Dans les cas prévisibles de ponction difficile, une anesthésie "
         "locale peut être envisagée."),
        ("Réalisation de la ponction",
         "Quelle que soit l'indication, la technique reste identique. Il est recommandé "
         "d'utiliser une aiguille atraumatique « à extrémité non tranchante », diamètre "
         "maximal 22 Gauge (code couleur noir — plus la Gauge est élevée, plus l'aiguille "
         "est fine). L'introducteur fourni avec l'aiguille est indispensable pour franchir "
         "la peau. Il est recommandé aux médecins de se former à son utilisation."),
        ("Réintroduction du mandrin",
         "Il est recommandé de réintroduire complètement le mandrin dans l'aiguille avant "
         "de la retirer."),
        ("Prélèvements",
         "L'incidence des syndromes post-PL immédiats augmente pour un volume prélevé "
         "supérieur à 30 mL."),
        ("Prévention des accidents d'exposition au sang",
         "La PL est un geste invasif avec risque d'accident d'exposition au sang : les "
         "aiguilles doivent être collectées dans un conteneur à disposition et prévu à cet "
         "effet."),
    ], TCW))
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        P("<b>Formation</b>", S_CELL_B),
        Spacer(1, 1 * mm),
        P("La PL nécessite une bonne connaissance de l'anatomie mais aussi de la pratique "
          "du geste. La formation pratique par simulation est recommandée :",
          S_BODY_SM),
        Spacer(1, 1 * mm),
        bullets([
            "avant tout premier geste (formation généralement assurée pendant les études "
            "médicales sur les plateformes de simulation universitaires) ;",
            "pour tout médecin dans le cadre de la mise à jour des conditions de pratique ;",
            "pour tout médecin ayant réalisé peu ou pas de PL ;",
            "dans le cadre de l'accréditation des médecins et des équipes.",
        ]),
        Spacer(1, 1 * mm),
        P("Après formation par simulation, il est recommandé que le médecin soit "
          "accompagné pour la réalisation des premières PL sur le patient aussi souvent "
          "que nécessaire.", S_BODY_SM),
    ]))
    return story

def _section_effets():
    story = []
    story.append(Spacer(1, 2 * mm))
    story.append(section_bar("Effets indésirables de la ponction lombaire"))
    story.append(Spacer(1, 2 * mm))
    story.append(P(
        "La PL est parfois responsable d'effets indésirables : syndrome post-PL "
        "(syndrome d'hypotension intracrânienne), hématomes, infections, douleurs "
        "lombaires, voire paraplégie ou décès de manière très exceptionnelle.",
        S_BODY_SM))
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        P("<b>Syndrome post-PL</b>", S_CELL_B),
        Spacer(1, 1 * mm),
        P("Secondaire à une fuite persistante de LCS, se caractérise par une céphalée "
          "orthostatique. Apparaît habituellement dans les 2 à 4 jours après une PL (mais "
          "parfois plus tardive), apyrétique, partiellement ou totalement soulagée par le "
          "décubitus dorsal. Classiquement bilatérale, occipitale, occipito-frontale ou "
          "diffuse, irradiant dans la nuque, le dos et parfois aux épaules. Parfois "
          "isolée, elle est habituellement accompagnée d'un cortège variable de signes : "
          "nausées et vomissements ; signes auditifs ou visuels (hypoacousie, rarement "
          "hyperacousie, diplopie par atteinte de la VIe paire — la photophobie fait "
          "partie du tableau clinique classique). Un syndrome post-PL atypique, ou dont la "
          "symptomatologie se modifie, nécessite un avis spécialisé. Il existe des cas "
          "exceptionnels de syndrome post-PL sans céphalée (ex. vertiges ou troubles "
          "auditifs isolés).", S_BODY_SM),
        Spacer(1, 1 * mm),
        P("L'incidence peut être minorée par des mesures simples : l'utilisation "
          "d'aiguilles atraumatiques la diminue significativement en incidence et "
          "intensité (incidence < 10 % avec aiguilles atraumatiques, contre jusqu'à 35 % "
          "avec des aiguilles traumatiques).", S_BODY_SM),
    ]))
    story.append(Spacer(1, 2.5 * mm))
    story.append(info_panel(P(
        "<b>Signes d'alerte de complications graves</b> — après une PL, l'apparition de "
        "signes cliniques nouveaux doit conduire à une prise en charge diagnostique et "
        "thérapeutique en urgence : fièvre ; signe neurologique (syndrome complet ou "
        "incomplet de la queue-de-cheval, diplopie, déficit sensitif et/ou moteur, trouble "
        "de conscience, confusion, crise d'épilepsie, coma, etc.) ; modification du "
        "caractère postural de la céphalée post-PL. La baisse de l'acuité visuelle doit "
        "faire évoquer une autre étiologie car il s'agit d'une complication "
        "exceptionnelle.", S_BODY), bg=RED_LIGHT, border=RED))
    story.append(Spacer(1, 2.5 * mm))
    story.append(theme_table([
        ("Hématomes",
         "Très exceptionnels, périmédullaires ou intracrâniens. Favorisés par les "
         "troubles de la coagulation, les traitements modifiant l'hémostase et les "
         "ponctions multiples. Quelle que soit la localisation : urgence diagnostique et "
         "thérapeutique nécessitant une imagerie et un avis spécialisé."),
        ("Infections",
         "Exceptionnelles, liées au non-respect des règles d'asepsie : méningite, abcès "
         "au point de ponction, spondylodiscite, etc."),
        ("Douleurs lombaires", "Possibles après PL, habituellement banales."),
    ], TCW))
    return story

def _section_bloodpatch():
    story = []
    story.append(Spacer(1, 2 * mm))
    story.append(KeepTogether([
        section_bar("Blood-patch"),
        Spacer(1, 2 * mm),
        P("Le blood-patch consiste en l'injection de sang autologue (du patient "
          "lui-même) dans l'espace péridural pour colmater la brèche méningée. Il s'agit "
          "du <b>traitement le plus efficace</b> en cas de non-guérison spontanée du "
          "syndrome post-PL dans les 48 à 72 heures.", S_BODY),
        Spacer(1, 1.5 * mm),
        P("Le blood-patch doit être envisagé après échec des traitements non invasifs et "
          "réalisé :", S_BODY_SM),
        Spacer(1, 1 * mm),
        bullets([
            "dans des conditions d'asepsie chirurgicale, par un médecin expérimenté ;",
            "au cours d'une hospitalisation (sa réalisation ne justifie pas, à elle "
            "seule, une hospitalisation de plus de 24 heures) ;",
            "possiblement en hôpital de jour, en garantissant un temps de surveillance et "
            "de décubitus pour le patient d'au moins 2 heures.",
        ]),
        Spacer(1, 1.5 * mm),
        P("En cas d'inefficacité immédiate ou de récidive à distance, un <b>2e "
          "blood-patch</b> est possible ; mais <b>pas de 3e blood-patch sans imagerie</b> "
          "(IRM et avis spécialisé). Comme la PL, c'est un geste invasif avec risque "
          "d'accident d'exposition au sang : les aiguilles doivent être collectées dans un "
          "conteneur prévu à cet effet.", S_BODY_SM),
    ]))
    return story

def _section_pediatrie():
    story = []
    story.append(Spacer(1, 2 * mm))
    story.append(KeepTogether([
        section_bar("Spécificités pédiatriques"),
        Spacer(1, 2 * mm),
        P("Le syndrome post-PL existe chez l'enfant et doit faire l'objet d'une "
          "prévention. Le taux de succès de la PL chez l'enfant est lié à plusieurs "
          "facteurs : positionnement de l'enfant, choix de l'aiguille, analgésie.",
          S_BODY_SM),
    ]))
    story.append(Spacer(1, 2 * mm))
    story.append(theme_table([
        ("Installation",
         "Nourrisson : position assise sans flexion de hanche et sans flexion de nuque — "
         "dégage le plus large espace intervertébral avec la meilleure tolérance "
         "hémodynamique. Enfant : position assise ou allongée, comme chez l'adulte."),
        ("Choix de l'aiguille",
         "Aiguilles atraumatiques « à extrémité non tranchante », 22 à 27 Gauge, "
         "recommandées en 1ère intention (certaines s'utilisent sans introducteur — 22, "
         "24, 25 G — d'autres avec introducteur — 22, 25, 27 G). Formation recommandée à "
         "l'utilisation des aiguilles atraumatiques avec introducteur. L'usage des "
         "aiguilles traumatiques à biseau tranchant doit rester exceptionnel."),
        ("Angle de pénétration",
         "Angle permettant d'accéder le plus efficacement au LCS : compris entre 50° et "
         "60°. Un repérage échographique (lorsqu'il est disponible) permet un taux de "
         "succès plus important."),
        ("Analgésie",
         "Point clé de la réussite du geste. Options disponibles : crème anesthésiante "
         "lidocaïne + prilocaïne, à appliquer 1 heure avant (hors urgence), quel que soit "
         "l'âge (sauf prématuré < 37 SA d'âge post-conceptionnel) ; sérum glucosé 30 % per "
         "os chez le nourrisson jusqu'à 6 mois ; inhalation d'un mélange équimolaire "
         "oxygène/protoxyde d'azote (MEOPA), à tout âge ; traitements anxiolytiques et "
         "antalgiques intra-rectaux ou morphiniques per os pour une PL programmée ou des "
         "antécédents de vécu douloureux."),
    ], TCW))
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        P("<b>Syndrome post-PL chez l'enfant</b>", S_CELL_B),
        Spacer(1, 1 * mm),
        P("Présentation clinique identique à celle de l'adulte, incidence de 2 à 15 % "
          "selon les études. Chez le nourrisson, le diagnostic reste difficile en "
          "l'absence de critère diagnostique spécifique.", S_BODY_SM),
    ]))
    story.append(Spacer(1, 2 * mm))
    story.append(KeepTogether([
        P("<b>Prévention du syndrome post-PL</b>", S_CELL_B),
        Spacer(1, 1 * mm),
        P("L'utilisation d'aiguilles atraumatiques chez l'enfant diminue l'incidence du "
          "syndrome post-PL, mais nécessite une formation des médecins. En cas "
          "d'utilisation d'aiguilles traumatiques, les éléments suivants sont associés à "
          "un risque moindre chez l'enfant : aiguille de petit diamètre (22 Gauge et "
          "plus) ; position du biseau parallèle à l'axe du rachis ; réintroduction du "
          "mandrin avant retrait de l'aiguille. <b>Il n'y a pas d'indication à l'alitement "
          "strict après la PL chez l'enfant.</b>", S_BODY_SM),
    ]))
    story.append(Spacer(1, 2 * mm))
    story.append(info_panel(P(
        "<b>Prise en charge du syndrome post-PL chez l'enfant :</b> en cas de syndrome "
        "post-PL avéré, le traitement conservateur est recommandé en première intention "
        "(antalgiques). Le repos au lit n'est pas obligatoire ; l'efficacité de "
        "l'hyperhydratation n'est pas prouvée. Comme chez l'adulte, le seul traitement "
        "ayant montré son efficacité en cas de syndrome post-PL persistant et/ou sévère "
        "est le blood-patch (les indications du blood-patch chez l'enfant restent rares).",
        S_BODY_SM), bg=BG_PANEL, border=TEAL))
    story.append(Spacer(1, 4 * mm))
    story.extend(_section_sources())
    return story

def _section_sources():
    story = []
    story.append(section_bar("Sources et traçabilité", color=GREY))
    story.append(Spacer(1, 2 * mm))
    story.append(P(
        "<b>Document source :</b> « Prévention et prise en charge des effets indésirables "
        "pouvant survenir après une ponction lombaire » — Fiche mémo, Haute Autorité de "
        "Santé (HAS).", S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P("<b>Version :</b> Juin 2019.", S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P("<b>Méthodologie :</b> fiche mémo — synthèse de la littérature, sans "
                    "système GRADE ni cotation d'accord (aucun tag 1+/2+/AE, aucune "
                    "mention d'accord fort/faible dans le texte source). Recommandations "
                    "de pratique présentées sous forme de messages clés et de "
                    "recommandations narratives.", S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>URL source :</b> https://www.has-sante.fr/upload/docs/application/pdf/"
        "2019-07/fm_ponction_lombaire.pdf", S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P("<b>Couverture :</b> cette fiche reprend l'intégralité des 7 pages de "
                    "la fiche mémo source : messages clés, indications et "
                    "contre-indications, modalités de réalisation, effets indésirables et "
                    "signes d'alerte, blood-patch, spécificités pédiatriques.", S_SOURCE))
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Avertissement :</b> ce document est une fiche de synthèse indépendante, "
        "produite pour un usage d'aide-mémoire. Elle reprend l'intégralité de la fiche "
        "mémo source, mais ne remplace pas le texte intégral et n'est ni éditée ni "
        "validée par la HAS. En cas de doute ou de situation clinique complexe (échec de "
        "PL, syndrome post-PL atypique, suspicion d'hématome ou d'infection), se référer "
        "au texte intégral et/ou à un avis spécialisé.",
        S_BODY_SM), bg=GREY_LIGHT, border=GREY))
    return story

def _section_intro_indications():
    # Merged onto one page-group: page 1 (messages clés) alone left too much
    # white space, page 2 (indications) had room to spare - combined per the
    # <60%-full merge rule (CLAUDE.md build pipeline, step 7).
    story = _section_intro()
    story.append(Spacer(1, 3 * mm))
    story.extend(_section_indications())
    return story

def _section_effets_bloodpatch():
    # Same merge rationale: blood-patch alone (source page 6) was far too
    # short for its own page-group; folded onto the end of "Effets
    # indésirables" which had spare room.
    story = _section_effets()
    story.append(Spacer(1, 3 * mm))
    story.extend(_section_bloodpatch())
    return story

SECTIONS = [
    ("Messages clés, indications & contre-indications", _section_intro_indications),
    ("Modalités de réalisation", _section_modalites),
    ("Effets indésirables & blood-patch", _section_effets_bloodpatch),
    ("Pédiatrie & sources", _section_pediatrie),
]

def _make_doc(path=None):
    return SimpleDocTemplate(path or OUT, pagesize=A4,
                              leftMargin=MARGIN, rightMargin=MARGIN,
                              topMargin=32 * mm, bottomMargin=16 * mm,
                              title="Fiche HAS 2019 - Ponction lombaire, effets indesirables",
                              author="Synthèse indépendante (source HAS)")

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
