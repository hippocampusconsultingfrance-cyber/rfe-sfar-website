# -*- coding: utf-8 -*-
"""
Fiche de synthese - RFE SFAR/SFMU (avec CNGOF, Collège national des sages-
femmes, GFRUP), "Urgences obstetricales extrahospitalieres", validees 3e
trimestre 2010, publiees Ann Fr Anesth Reanim 2012;31:652-665. Coordinateur :
G. Bagou. 9 chapitres traites independamment. 14 pages source, telecharge
depuis sfar.org (wp-content/uploads/2015/10/2_AFAR_Urgences-Obstetricales-
Extrahospitalieres.pdf).

METHODOLOGIE : "methode GRADE" annoncee par la source, mais explicitement
limitee par la faiblesse de la litterature sur ce champ tres specifique
(medecine extrahospitaliere obstetricale) - AUCUN grade 1+/1-/2+/2- ou A/B/C
individuel n'est appose aux recommandations du texte court (verifie par grep
exhaustif : zero occurrence de ces tags dans ce document, a la difference
d'autres fiches du corpus). Cotation Delphi (2 tours), "en dehors des tres
rares situations ou le groupe n'a pu se prononcer, il s'agit toujours d'un
accord fort" (citation directe de la source, p.652) - meme convention de
chip unique "AE"/Accord fort que fiche_brule_grave.py et
fiche_bris_dentaires.py (aucun grade individuel invente).

FORMAT SOURCE - PAS DE R#.# NUMEROTES : contrairement a la majorite du
corpus, ce texte court est une prose continue par chapitre (pas de
recommandations numerotees individuellement). Format retenu ici : tableaux
"Theme / Detail" (comme fiche_brule_grave.py, fiche_aap_programmee.py) qui
condensent chaque item actionnable en une ligne, dans l'ordre du texte
source, sans reformulation qui changerait le sens clinique.

PORTEE / CONDENSATION DISCLOSED (regle de projet 7, 2026-09-14) : les 9
chapitres sont TOUS couverts pour leur contenu clinique actionnable (regle
2 : 100% de couverture), mais la prose discursive/justificative est
systematiquement condensee en items courts par theme. UN SEUL chapitre est
deliberement resume en quelques lignes plutot que detaille integralement,
car organisationnel et non un geste d'urgence : Chapitre 9 (formation,
evaluation des pratiques professionnelles, reseaux de soins - objectifs
qualite, pas de geste clinique). Les 8 autres chapitres (Chapitre 1 -
recours au Samu, accouchement inopine, hemorragies 2e/3e trimestre, HPP,
traumatismes, HTA/preeclampsie/eclampsie, MAP, TIU) recoivent une
couverture complete de leur contenu actionnable.

FIGURES/TABLEAUX RETRANSCRITS : Tableau 1 (signes evocateurs d'urgence
gyneco-obstetricale par terme), Tableau 2 (diagnostic differentiel HRP vs
placenta praevia), Tableau 3 (classification des traumatismes pendant la
grossesse), Tableau 4 (choix du vecteur de transport par situation
clinique), Fig. 1 (algorithme de prise en charge de l'HPP), Fig. 2
(algorithme de titration de l'HTA gravidique, nicardipine/labetalol) - ces
2 figures sont des organigrammes graphiques (boites/fleches) sans texte
alternatif exploitable par une extraction PyMuPDF brute ; RETRANSCRITES ICI
a partir d'un rendu visuel direct des pages sources a 220dpi (pages 7 et 11
du PDF), pas de la seule extraction texte fragmentee - voir AUDIT ci-dessous
pour l'incident qui a rendu cette re-verification necessaire. Aucune image/
photo n'est presente dans le PDF source (verifie par doc.get_images()) hors
le logo SFAR page 1.

ARGUMENTAIRE : condense (regle de projet 2026-09-14) - seuls les seuils/
doses/delais et criteres de decision directement actionnables sont
conserves ; l'epidemiologie generale et la prose de justification
bibliographique sont omises sauf quand un chiffre epidemiologique change la
priorisation clinique (ex. HPP = 1re cause de mortalite maternelle).

AUDIT INDEPENDANT (2026-09-15, subagent) et corrections appliquees :
1. ERREUR CRITIQUE TROUVEE ET CORRIGEE - contamination croisee entre
   documents : le brouillon initial contenait un bloc "Chapitre 1 -
   Information du patient" (devoirs d'information, consentement, analgesie
   peridurale/cesarienne) qui N'EXISTE NULLE PART dans cette source (verifie
   par grep exhaustif - zero occurrence de "peridurale", "cesarienne",
   "information du patient"). Ce contenu provient en realite du DOCUMENT
   "Les blocs perimedullaires chez l'adulte" (2006 RPC), explore et
   ABANDONNE plus tot dans la meme session sans jamais avoir ete construit
   en fiche - son "Question 1 : Quelle information donner au patient..."
   a ete confondu par erreur avec le Chapitre 1 de CE document (qui est en
   realite "Recours au Samu centre 15 pour motif obstetrical", deja
   correctement couvert plus loin dans le brouillon, juste mal numerote
   "2" au lieu de "1"). Corrige : bloc fabrique supprime integralement,
   numerotation des sections 1/2 rectifiee (1 = Samu, 2 = accouchement
   inopine), aucune perte de contenu reel puisque le Chapitre 1 authentique
   etait deja couvert sous un mauvais numero.
2. Fig. 1 (algorithme HPP) et Fig. 2 (titration HTA) INITIALEMENT
   retranscrites depuis le texte OCR fragmente seul (sans rendu visuel),
   en violation de la regle de projet 1 pour les figures graphiques.
   Re-verifiees par rendu direct des pages PDF sources a 220dpi : Fig. 2
   avait une ERREUR D'INVERSION reelle (le brouillon assignait le
   "traitement d'attaque" au seuil d'ENTREE le plus bas et le "traitement
   d'entretien" au seuil le PLUS SEVERE - exactement l'inverse de la
   source, qui reserve l'attaque a PAS>180/PAM>140 et l'entretien a
   PAS<180 et PAM<140). Fig. 1 avait une simplification perdant la
   sous-branche "operateur non forme -> transport rapide direct" et
   inversait l'ordre reel des etapes "possibilite de RU ?" / "sulprostone ?"
   (la source route les deux branches de la RU vers le sulprostone AVANT
   le transport, pas la RU vers le transport directement). Les deux figures
   ont ete entierement reecrites pour suivre fidelement l'organigramme
   visuel.
3. Contre-indication a l'ocytocine manquante ajoutee (placenta incomplet
   + attente de revision uterine -> ne pas administrer d'ocytocine, sauf
   transport long avec hemorragie objectivee).
4. Detail manquant ajoute : perfusion d'entretien ocytocine 5-10 UI/h
   (texte du corps, distinct du schema de la Fig. 1 "10 UI en 20 min" -
   divergence de formulation entre texte et figure dans la source
   elle-meme, disclosed plutot que silencieusement unifiee).
5. Deux corrections d'unite (deja presentes dans le brouillon initial mais
   non disclosed) desormais explicitement disclosed dans le corps de la
   fiche, conformement a la regle 5 : sulprostone "100-500 mg/h" (source)
   -> corrige en 100-500 µg/h (surdosage massif sinon) ; creatininemie
   "135 mmol/L" (source, seuil de preeclampsie severe) -> corrige en
   135 µmol/L (valeur incompatible avec la survie sinon). Meme classe
   d'artefact d'extraction "µ"->"m" que documentee ailleurs dans ce corpus.
6. Deux precisions mineures ajoutees : le score de Malinas B (duree
   moyenne du travail) mentionne dans la decision transport/accouchement
   sur place ; la traction douce sur le cordon + contre-pression sus-
   pubienne comme facteur preventif reconnu de l'HPP (distinct de la mise
   en garde contre une traction ferme, qui restait deja presente).
LECON POUR LES SESSIONS FUTURES : lors de l'exploration puis de
l'abandon d'un candidat de fiche (ici blocs_perimedullaires.py), s'assurer
qu'aucun contenu de ce candidat abandonne ne soit reutilise par erreur dans
un fiche batie ensuite sur un sujet different - la proximite temporelle
dans la meme session a cause une confusion reelle ici, detectee seulement
par l'audit independant et non par la propre relecture visuelle du
constructeur.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from style import *
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.units import mm

OUT = "/home/user/rfe-sfar-website/output/Fiche_SFAR_Urgences_Obstetricales_Extrahospitalieres_2010.pdf"

SOURCE_TXT = ("Source : « Urgences obstétricales extrahospitalières » — RFE SFAR/SFMU, "
              "validée 2010 (Ann Fr Anesth Reanim 2012;31:652-665). Fiche de synthèse non "
              "officielle : se référer au texte intégral.")

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

TCW = [38 * mm, CW_FULL - 38 * mm]

def grid_table(head_row, rows, col_widths):
    """Generic small grid table for Tableaux 1-4 (multi-column)."""
    data = [[P(h, S_HEAD_W_C) for h in head_row]]
    for row in rows:
        data.append([P(c, S_CELL) for c in row])
    t = Table(data, colWidths=col_widths, repeatRows=1)
    style_cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), NAVY), ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTNAME", (0, 0), (-1, 0), FONT_BOLD), ("FONTSIZE", (0, 0), (-1, 0), 8),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.5, GREY_LIGHT),
        ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            style_cmds.append(("BACKGROUND", (0, i), (-1, i), BG_PANEL))
    t.setStyle(TableStyle(style_cmds))
    return t

def legend_flowable():
    chip_w = 20 * mm
    content_w = CW_FULL
    row = Table([[chip("AE", width=chip_w - 2 * mm),
                  P("Toutes les recommandations de ce texte sont validées par vote Delphi "
                    "(2 tours) — <b>Accord fort</b>, sauf de très rares situations sans "
                    "consensus (non détaillées par la source). Aucun grade GRADE 1+/2+/A/B/C "
                    "individuel n'est utilisé dans ce document.", S_BADGE_HEAD)]],
                colWidths=[chip_w, content_w - chip_w])
    row.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                              ("LEFTPADDING", (0, 0), (-1, -1), 1),
                              ("RIGHTPADDING", (0, 0), (-1, -1), 1),
                              ("TOPPADDING", (0, 0), (-1, -1), 0),
                              ("BOTTOMPADDING", (0, 0), (-1, -1), 0)]))
    return row

TOTAL_PAGES = {"n": 9}

def on_page(canvas, doc, page_title):
    header_band(canvas, doc, "SFAR / SFMU — RFE, validée 2010",
                "Urgences obstétricales extrahospitalières",
                page_title, icon_fn=lambda c, x, y: icon_drop(c, x, y, 13 * mm), color=RED)
    footer_band(canvas, doc, SOURCE_TXT, f"Page {doc.page} / {TOTAL_PAGES['n']}")

# ---------------------------------------------------------------------------
def _section_intro_regulation():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Résumé :</b> RFE SFAR/SFMU (avec CNGOF, Collège national des sages-femmes), "
        "9 chapitres sur la prise en charge des urgences obstétricales en dehors d'une "
        "maternité (régulation Samu, accouchement inopiné, hémorragies, traumatismes, "
        "HTA gravidique/prééclampsie/éclampsie, menace d'accouchement prématuré, "
        "transferts in utero). <b>Portée :</b> couverture complète du contenu clinique "
        "actionnable de 8 des 9 chapitres ; seul le chapitre 9 (formation/évaluation "
        "des pratiques), de nature organisationnelle et non un geste d'urgence, est "
        "résumé en quelques lignes — voir texte intégral pour son détail complet.",
        S_BODY), bg=BG_PANEL, border=TEAL))
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("Méthodologie"))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "Méthode GRADE annoncée mais littérature spécifique à ce champ peu abondante : "
        "aucun grade individuel 1+/2+/A/B/C n'est utilisé — chaque item du texte court a "
        "été coté par vote Delphi (2 tours) et, hors de très rares situations sans "
        "consensus, correspond systématiquement à un <b>Accord fort</b>. Validé au "
        "3<sup>e</sup> trimestre 2010.", S_BODY_SM))
    story.append(Spacer(1, 1.5 * mm))
    story.append(legend_flowable())
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("1 — Recours au Samu centre 15 pour motif obstétrical"),
        Spacer(1, 1.5 * mm),
        theme_table([
            ("Numéro d'appel", "Le 15 (Samu) est le seul numéro à composer pour toute "
             "urgence obstétricale extrahospitalière (hors transferts interhospitaliers)."),
            ("Priorisation régulation", "3<sup>e</sup> trimestre ou post-partum précoce → "
             "régulation prioritaire par un médecin urgentiste. Enfant né ou accouchement "
             "en cours → départ réflexe d'une équipe Smur + régulation médicale "
             "prioritaire."),
            ("Scores d'aide à la régulation", "Utilisation recommandée des scores de "
             "Malinas, SPIA et Prémat-SPIA (avant 33 SA) — leur association est "
             "recommandée pour leur complémentarité."),
            ("Orientation", "Maternité adaptée au plateau technique requis ; grossesse à "
             "bas risque → maternité choisie par la patiente ; urgence vitale maternelle "
             "→ maternité la plus proche quel que soit le terme."),
            ("Décision accoucher sur place vs. transporter", "Repose sur l'évaluation de "
             "la rapidité de dilatation (2 touchers vaginaux à 10 min d'intervalle — le "
             "score de Malinas B indique la durée moyenne du travail en population "
             "générale) ; dilatation complète + envie irrépressible de pousser → "
             "accouchement sur place."),
            ("Transport (2<sup>e</sup>/3<sup>e</sup> trimestre)", "Décubitus latéral, "
             "ceinturée — le décubitus dorsal est proscrit. Voie veineuse périphérique "
             "systématique."),
        ], TCW),
    ]))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P("<b>Tableau 1 — Signes évoquant une urgence gynéco-obstétricale et "
                    "justifiant l'envoi d'une équipe Smur, selon le terme :</b>", S_BODY_SM))
    story.append(Spacer(1, 1 * mm))
    story.append(grid_table(
        ["Terme", "Symptômes", "Diagnostics à évoquer"],
        [
            ["Post-partum (≤ 15 j)", "Hémorragie", "Hémorragie de la délivrance"],
            ["Post-partum (≤ 15 j)", "Convulsion", "Éclampsie"],
            ["3e trimestre", "L'enfant est né", "Accouchement réalisé"],
            ["3e trimestre", "Contraction, douleur, métrorragie, envie de pousser, perte "
             "des eaux", "Accouchement imminent"],
            ["3e trimestre", "Antécédent de césarienne ou traumatisme majeur, douleur "
             "abdo intense, baisse des MAF", "Rupture utérine"],
            ["2e/3e trimestre", "Métrorragie peu abondante noirâtre, douleur abdo "
             "intense permanente, absence de MAF", "Hématome rétroplacentaire"],
            ["2e/3e trimestre", "Métrorragie abondante rouge avec caillots, contractions",
             "Placenta prævia hémorragique"],
            ["2e/3e trimestre", "Céphalée, douleur abdo, prise de poids, nausée, "
             "trouble visuel", "Prééclampsie"],
            ["2e/3e trimestre", "Convulsion", "Éclampsie"],
            ["1er trimestre", "Malaise, douleur abdominale, métrorragie", "Grossesse "
             "extra-utérine rompue"],
        ], [30 * mm, CW_FULL - 30 * mm - 38 * mm, 38 * mm]))
    return story

def _section_accouchement_inopine():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("2 — Accouchement inopiné extrahospitalier : mécanique"))
    story.append(Spacer(1, 1.5 * mm))
    story.append(theme_table([
        ("Position / efforts expulsifs", "Favoriser les positions d'hyperflexion des "
         "cuisses sur l'abdomen. Ne débuter les efforts expulsifs que lorsque la "
         "présentation commence à apparaître à la vulve (garantie d'une dilatation "
         "complète)."),
        ("Épisiotomie", "Pas d'épisiotomie systématique. Médiolatérale, au moment d'une "
         "contraction, réservée à : présentation par le siège chez une primipare, "
         "indications fœtales d'accélération de l'expulsion."),
        ("Dégagement / circulaire du cordon", "Une fois la tête dégagée, vérifier un "
         "circulaire du cordon ; si serré et gênant, clamper et sectionner entre 2 "
         "pinces avant de reprendre les efforts expulsifs pour l'épaule antérieure."),
        ("Prévention de l'HPP (4 règles)", "Vessie vide ; utérus vide ; utérus contracté "
         "(massage utérin + ocytocine) ; compensation volémique rapide. Le clampage "
         "précoce du cordon y participe également."),
        ("Délivrance dirigée", "5 UI d'ocytocine en IVD lente à la sortie complète de "
         "l'enfant, au plus tard dans la minute suivant l'expulsion ; délivrance "
         "attendue dans les 30 min ; massage utérin répété (séquences &gt; 15 s) jusqu'à "
         "la prise en charge en maternité."),
        ("Analgésie de l'accouchement inopiné", "MEOPA inhalé possible ; infiltration "
         "locale du périnée recommandée en cas d'épisiotomie."),
        ("Accouchement par le siège", "Attendre l'apparition du siège à la vulve avant "
         "les efforts expulsifs, exclusivement pendant les contractions — ne jamais "
         "tirer sur un siège. 4 gestes : épisiotomie d'indication large, faire tourner "
         "le dos en avant, manœuvre de Lovset si relèvement des bras, technique de "
         "Mauriceau si rétention de la tête dernière."),
        ("Dystocie des épaules", "Le plus souvent une fausse dystocie → manœuvre de "
         "Mac Roberts."),
        ("Procidence d'un bras", "Incompatible avec l'accouchement par voie basse → "
         "transport rapide en décubitus latéral sous oxygène vers la maternité la plus "
         "proche, accueil organisé au bloc opératoire obstétrical."),
        ("Procidence du cordon", "Urgence vitale. Si le cordon bat : refouler la "
         "présentation (poing ou 2 doigts intravaginaux, sans comprimer le cordon), "
         "position de Trendelenburg + décubitus latéral genoux contre poitrine, "
         "tocolyse IV pour bloquer les contractions, transport le plus rapide possible."),
        ("Grossesse gémellaire", "Situation à haut risque (anoxie du 2<sup>e</sup> "
         "jumeau, HPP) — décision transport vs. accouchement sur place au cas par cas ; "
         "demande de renfort recommandée si accouchement hors maternité."),
    ], TCW))
    story.append(Spacer(1, 2.5 * mm))
    story.append(section_bar("Prise en charge du nouveau-né en extrahospitalier"))
    story.append(Spacer(1, 1.5 * mm))
    story.append(theme_table([
        ("5 règles, dans l'ordre", "Clamper/couper/vérifier le cordon (2 artères, "
         "1 veine) ; prévenir l'hypothermie ; évaluer l'état clinique ; prévenir "
         "l'hypoglycémie (&lt; 2,2 mmol/L à 30 min de vie) ; favoriser le peau-à-peau."),
        ("Section du cordon", "Stérile, entre 2 clamps, à ≥ 10 cm de l'ombilic."),
        ("Lutte contre l'hypothermie", "Sécher l'enfant ou utiliser un sac en "
         "polyéthylène sans séchage préalable ; toujours couvrir la tête d'un bonnet ; "
         "peau-à-peau privilégié ; décubitus latéral, liberté des VAS, surveillance "
         "rapprochée."),
        ("Évaluation clinique", "Tonus, ventilation, couleur et/ou SpO2, puis fréquence "
         "cardiaque (auscultation ou pouls ombilical) — le score d'Apgar n'a pas de "
         "valeur décisionnelle pour la réalisation d'un geste. Stimulation possible "
         "pour déclencher la respiration, sans jamais secouer l'enfant."),
        ("Hypoglycémie", "Sérum glucosé à 10 % préférentiellement per os à la seringue "
         "si nouveau-né conscient et terme &gt; 34 SA. Le sérum glucosé à 30 % est "
         "toujours contre-indiqué. Mise au sein recommandée si la mère le souhaite."),
        ("Nouveau-né sans signe de vie", "Prise en charge selon les recommandations "
         "ILCOR ; demande de renfort recommandée."),
        ("Désobstruction des VAS", "Pas de désobstruction systématique si l'enfant va "
         "bien. Si nécessaire : aspiration à dépression réglable &lt; 150 mmHg "
         "(200 cmH2O)."),
        ("Ventilation / oxygénation", "La qualité de la ventilation prime sur la FiO2. "
         "Chez le prématuré, débuter avec une FiO2 de 0,30 à 0,40, objectif SpO2 "
         "85-95 % (risque surtout lié à l'hyperoxie). Intubation de sauvetage orale "
         "possible sans sédation, mais une ventilation au BAVU + masque reste "
         "préférable à des tentatives d'intubation répétées et maladroites."),
        ("RCP néonatale", "Massage cardiaque externe + ventilation efficace dès "
         "bradycardie &lt; 60/min — ratio 2 ventilations pour 6 compressions "
         "thoraciques."),
        ("Certificat d'accouchement / naissance", "Rédigé par le médecin ou la "
         "sage-femme ayant pratiqué l'accouchement ou sectionné le cordon ; le médecin "
         "s'assure de la déclaration à l'état civil dans les 3 jours ouvrables (4 si "
         "dimanche ou jour férié)."),
    ], TCW))
    return story

def _section_hemorragies():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("3 — Hémorragies du 2e et 3e trimestre"))
    story.append(Spacer(1, 1.5 * mm))
    story.append(theme_table([
        ("Étiologies principales", "Hématome rétroplacentaire (HRP) et anomalies "
         "d'insertion du placenta (placenta prævia). Causes cervicales : modérées, "
         "en général après examen gynécologique ou rapport sexuel. Plus rares : "
         "rupture utérine, hémorragie de Benkiser, rupture du sinus marginal."),
        ("Régulation", "Toute métrorragie chez une femme enceinte au 2<sup>e</sup>/"
         "3<sup>e</sup> trimestre doit être régulée par un médecin urgentiste. "
         "Interrogatoire : terme, prævia connu, HTA connue, couleur/abondance du "
         "saignement, douleurs/contractions, mouvements fœtaux. En l'absence de "
         "prævia connu, évoquer un HRP jusqu'à preuve du contraire."),
        ("Prise en charge générale", "Envoi systématique d'une équipe Smur à la moindre "
         "suspicion d'HRP ou de prævia hémorragique ; décubitus latéral ; bloc "
         "opératoire/obstétricien/anesthésiste prévenus et produits sanguins "
         "disponibles dès l'arrivée ; remplissage par cristalloïdes ou amidons ayant "
         "l'AMM chez la femme enceinte (transfusion préhospitalière seulement si "
         "compatible avec un transfert rapide) ; oxygénothérapie de principe."),
        ("Placenta prævia", "Toucher vaginal formellement contre-indiqué si prævia "
         "connu/suspecté. Tocolyse possible en préhospitalier si CU + transport long "
         "+ saignement important (concertation obstétricien). Transport en décubitus "
         "latéral. Recherche du RCF (Doppler/cardiotocographe) possible sans retarder "
         "le transfert. Lieu d'accouchement = maternité la plus proche (idéalement "
         "multidisciplinaire) si prævia recouvrant hémorragique ou suspicion "
         "d'accreta."),
        ("HRP", "Aucun examen ne doit retarder l'extraction fœtale si le fœtus est "
         "vivant ; transport rapide vers la maternité la plus proche que l'enfant soit "
         "vivant ou décédé."),
    ], TCW))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P("<b>Tableau 2 — Diagnostic différentiel placenta prævia / hématome "
                    "rétroplacentaire :</b>", S_BODY_SM))
    story.append(Spacer(1, 1 * mm))
    story.append(grid_table(
        ["", "Placenta prævia", "Hématome rétroplacentaire"],
        [
            ["Facteurs favorisants", "Utérus cicatriciel", "HTA gravidique, "
             "prééclampsie, traumatisme abdominal"],
            ["Douleurs", "Absentes ou peu intenses", "Brutales, intenses, permanentes"],
            ["Utérus", "Souple, indolore en dehors des contractions", "Hypertonie, "
             "hypercinésie, « utérus de bois »"],
            ["Saignement", "Rouge, modéré à abondant, ± caillots", "Noir, peu abondant, "
             "incoagulable"],
        ], [28 * mm, (CW_FULL - 28 * mm) / 2, (CW_FULL - 28 * mm) / 2]))
    story.append(Spacer(1, 2.5 * mm))
    story.append(section_bar("4 — Hémorragie du post-partum (HPP)"))
    story.append(Spacer(1, 1.5 * mm))
    story.append(theme_table([
        ("Enjeu", "1<sup>re</sup> cause de mortalité maternelle en France ; plus de la "
         "moitié des décès maternels sont évitables."),
        ("Facteurs de risque", "Délivrance &gt; 30 min, âge &gt; 35 ans, distension "
         "utérine (grossesse gémellaire), cicatrice utérine, hyperthermie per-travail, "
         "catégorie sociale défavorisée, HRP connu, placenta prævia — la majorité des "
         "HPP survient toutefois sans facteur de risque identifié."),
        ("Diagnostic / gravité", "Le saignement peut atteindre 600 mL/min (sac "
         "collecteur sous les fesses pour l'évaluer). Critères de gravité : hémorragie "
         "intarissable, sang incoagulable, signes de choc. Une perte de 1000 mL peut "
         "être bien tolérée — le retentissement clinique peut être tardif et brutal, "
         "d'où une surveillance attentive systématique après tout accouchement."),
        ("Prévention (accouchement pas encore survenu)", "Délivrance dirigée : 5 UI "
         "d'ocytocine IVD lente (IM à défaut) dans la minute suivant la naissance. Une "
         "traction douce sur le cordon associée au refoulement de l'utérus (contre-"
         "pression sus-pubienne) pour constater le décollement placentaire est un "
         "facteur préventif reconnu de l'HPP — mais il ne faut jamais tirer fermement "
         "sur le cordon pour provoquer le décollement sans formation préalable."),
        ("Ocytocine après délivrance (utérus vide)", "10 UI en IVD lente, renouvelées "
         "et/ou complétées par un débit de perfusion IV de 5 à 10 UI/h, sans dépasser "
         "40 UI au total. <i>Note : la Fig. 1 (ci-dessous) exprime ce même schéma "
         "différemment (10 UI en 20 min ± bolus de 5 UI, maximum 40 UI) — divergence "
         "de formulation entre le texte et la figure de la source elle-même, disclosed "
         "ici plutôt que résolue arbitrairement.</i>"),
        ("Contre-indication à l'ocytocine", "Si le placenta est incomplet et dans "
         "l'attente d'une révision utérine, il ne faut <b>pas</b> recourir à "
         "l'ocytocine — sauf en cas de transport long avec une hémorragie "
         "objectivée."),
    ], TCW))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P("<b>Fig. 1 — Algorithme de prise en charge d'une HPP extrahospitalière "
                    "(organigramme, retranscrit en étapes séquentielles à partir du "
                    "rendu visuel de la source) :</b>", S_BODY_SM))
    story.append(Spacer(1, 1 * mm))
    story.append(theme_table([
        ("Déclencheur", "Hémorragie &gt; 500 mL ou saignements anormaux → la "
         "délivrance a-t-elle eu lieu ?"),
        ("Délivrance non faite → décollement placentaire ?", "Oui → aide à "
         "l'expulsion, puis mesures immédiates (ligne suivante). Non → délivrance "
         "artificielle sous anesthésie générale avec intubation si opérateur formé "
         "(puis mesures immédiates) ; si opérateur non formé → transport rapide "
         "directement, sans attendre les mesures immédiates."),
        ("Mesures immédiates (délivrance faite, ou après aide à l'expulsion/"
         "délivrance artificielle)", "Vacuité vésicale ; ocytocine 10 UI en 20 min "
         "(± bolus de 5 UI, maximum 40 UI) ; massage utérin continu."),
        ("Persistance de l'hémorragie ?", "Non → transport. Oui → rechercher en "
         "parallèle une atonie utérine ET une lésion de la filière génitale (2 lignes "
         "suivantes)."),
        ("→ Atonie utérine", "Ocytocine (maximum 40 UI) + massage utérin continu → "
         "possibilité de révision utérine (RU) ? Oui → révision utérine sous "
         "anesthésie générale avec intubation, puis sulprostone. Non → sulprostone "
         "directement. Dans les 2 cas → sulprostone (100 à 500 µg/h), puis transport "
         "rapide."),
        ("→ Lésion de la filière génitale", "Examen (épisiotomie, périnée, vagin) → "
         "méchage compressif → transport rapide."),
    ], TCW))
    story.append(Spacer(1, 1.5 * mm))
    story.append(theme_table([
        ("Correction d'unité — sulprostone", "La source imprime « 100 à 500 mg/h » "
         "pour la posologie du sulprostone (p.657) — dose incompatible avec une "
         "utilisation clinique (surdosage massif). Lu et corrigé ici en <b>100 à "
         "500 µg/h</b>, posologie standard du sulprostone (Nalador), cohérente avec "
         "un probable artefact d'extraction PDF « µ » → « m », même classe d'artefact "
         "que documentée ailleurs dans ce corpus (cf. fiche_sujet_age_esf.py) — "
         "disclosed plutôt que silencieusement résolu, conformément à la règle du "
         "projet."),
        ("Gestes endo-utérins", "Délivrance artificielle et révision utérine imposent "
         "une anesthésie avec induction en séquence rapide et intubation, maintenues "
         "jusqu'à la prise en charge hospitalière spécialisée. Asepsie rigoureuse et "
         "antibioprophylaxie à large spectre systématiques."),
        ("Lésion de la filière génitale", "Si l'hémorragie persiste : rechercher une "
         "lésion de l'épisiotomie, du périnée ou du vagin — méchage ou compression "
         "maintenus jusqu'à la prise en charge hospitalière."),
        ("Produits sanguins labiles", "Utilisables en préhospitalier (procédures de "
         "transfusion en urgence vitale immédiate) sans retarder le transport ; "
         "acheminer les documents immuno-hématologiques avec la patiente."),
        ("Transfert interhospitalier pour HPP grave", "Situation à haut risque (ex. en "
         "vue d'une embolisation) justifiant une décision réfléchie et médicalisée, "
         "concertée entre équipes obstétricale/anesthésique d'origine et receveuse, "
         "avec réévaluation du rapport bénéfice-risque au moment du départ. Un état "
         "hémodynamique instable malgré une prise en charge bien conduite est une "
         "contre-indication au transport et impose une chirurgie d'hémostase sur "
         "place, si possible conservatrice. La réparation des lésions de la filière "
         "génitale doit être réalisée avant le transfert."),
        ("HPP tardive (&gt; 3 jours)", "Douleur pelvienne + fièvre + lochies "
         "malodorantes + utérus mou non involué → évoquer une endométrite "
         "hémorragique. Retour de couches hémorragique : pas de fièvre ni douleur, "
         "utérus involué, col fermé, pertes inodores. Cause possible : placenta "
         "accreta/percreta résiduel, chute d'escarre après hystérotomie, contraception "
         "progestative microdosée. Orientation vers l'obstétricien référent, sauf "
         "urgence vitale immédiate exceptionnelle."),
    ], TCW))
    return story

def _section_trauma_hta():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("5 — Traumatismes chez la femme enceinte"))
    story.append(Spacer(1, 1.5 * mm))
    story.append(theme_table([
        ("Enjeu", "La majorité des morts fœtales est évitable. Causes principales de "
         "mort fœtale : choc hémorragique maternel (80 %), décollement placentaire, "
         "mort maternelle — rarement un traumatisme direct."),
        ("Prévention", "Port correct d'une ceinture de sécurité homologuée à 3 points ; "
         "son association aux airbags améliore la sécurité des femmes enceintes."),
        ("Régulation", "Rechercher systématiquement : grossesse et terme, mécanisme et "
         "cinétique du traumatisme, métrorragie, contractions utérines, rupture des "
         "membranes. Penser à une possible grossesse chez toute femme en âge de "
         "procréer traumatisée. Rechercher des violences domestiques si le mécanisme "
         "n'est pas évident (lésions face/thorax/abdomen)."),
        ("Brûlures", "Majorer les formules de compensation hydrique (surface corporelle "
         "maternelle augmentée pendant la grossesse) ; interruption de grossesse à "
         "envisager si surface corporelle brûlée &gt; 50 %."),
        ("Intoxication oxycarbonée", "Retentissement fœtal retardé, plus long et plus "
         "sévère que le retentissement maternel. Oxygénothérapie normobare impérative "
         "si symptômes ou HbCO positif, quel que soit le terme. Oxygénothérapie "
         "hyperbare systématique, organisée très précocement avec les centres "
         "d'hyperbarie et les obstétriciens."),
        ("Électrisation", "Surveillance fœtale prolongée 24 à 48 h si le courant passe "
         "entre un membre supérieur et un membre inférieur (lésions fœtales possibles "
         "retardées)."),
    ], TCW))
    story.append(Spacer(1, 1.5 * mm))
    story.append(KeepTogether([
        P("<b>Tableau 3 — Aide à la décision selon l'âge de la grossesse et "
          "l'état clinique maternel :</b>", S_BODY_SM),
        Spacer(1, 1 * mm),
        grid_table(
            ["Groupe 1", "Groupe 2", "Groupe 3", "Groupe 4"],
            [[
                "Début de grossesse ou ignorée — test de grossesse positif chez une "
                "femme en période d'activité génitale ayant eu un traumatisme grave. "
                "Prise en charge essentiellement maternelle.",
                "Terme ≤ 24 SA — fœtus non viable, bien protégé par le bassin "
                "maternel (peu de lésions). Adaptation diagnostique (radios) et "
                "thérapeutique.",
                "Terme &gt; 24 SA — fœtus viable, moins bien protégé par le bassin "
                "maternel. Prise en charge maternelle ET fœtale (monitorage, "
                "échographie, extraction prématurée ?).",
                "Détresse maternelle ou inefficacité circulatoire — nécessité de "
                "délais très courts et problèmes éthiques. Si traitement inefficace : "
                "césarienne post-mortem ?",
            ]],
            [(CW_FULL) / 4.0] * 4),
    ]))
    story.append(Spacer(1, 1.5 * mm))
    story.append(theme_table([
        ("Monitorage", "Suivre les recommandations de monitorage du traumatisé grave, "
         "en tenant compte des modifications ECG physiologiques de la grossesse "
         "(déviation axiale gauche, arythmies bénignes, ST/T, ondes Q) et de "
         "l'hémodilution physiologique pour l'interprétation de l'Hb. Cardiotocographe "
         "portable utilisable en préhospitalier — une souffrance fœtale est possible "
         "malgré un état maternel rassurant, réévaluation fréquente nécessaire."),
        ("Prévention de la compression cave", "Décubitus latéral systématique à toutes "
         "les étapes jusqu'au bloc opératoire ; si la patiente ne peut être mobilisée : "
         "surélever une hanche (droite de préférence) ou récliner manuellement "
         "l'utérus vers la gauche."),
        ("Remplissage / oxygénothérapie", "Débuter un remplissage précoce avant les "
         "signes cliniques d'hypovolémie (perte possible de 30-35 % de la volémie sans "
         "signe clinique). Indications d'oxygénothérapie larges (sensibilité fœtale à "
         "l'hypoxie). Respecter l'hyperventilation physiologique de la grossesse "
         "(PaCO2 ≈ 32 mmHg) en ventilation mécanique."),
        ("Lésions à rechercher systématiquement", "Décollement placentaire (fréquent "
         "même pour un traumatisme mineur, parfois retardé de 24-48 h) ; rupture "
         "splénique (lésion hémorragique intrapéritonéale la plus fréquente) ; rupture "
         "utérine (surtout 3<sup>e</sup> trimestre / traumatisme violent). Pas de "
         "toucher vaginal chez une femme enceinte traumatisée."),
        ("Analgésie", "Pas de contre-indication à l'analgésie chez la femme enceinte : "
         "palier 1 = paracétamol ; palier 2 = dextropropoxyphène ; palier 3 = morphine "
         "(risques de dépression respiratoire et de sevrage néonatal si extraction). "
         "MEOPA utilisable."),
        ("Remplissage / transfusion", "Cristalloïdes ± amidons ayant l'AMM chez la "
         "femme enceinte. Si transfusion de globules rouges nécessaire : concentrés "
         "érythrocytaires O rhésus négatif, si possible Kell négatif. Catécholamines "
         "en complément d'un remplissage bien conduit, malgré le risque de "
         "détournement partiel de la circulation fœtale."),
        ("Intubation trachéale", "Toujours considérée comme difficile et à estomac "
         "plein. Induction en séquence rapide avec manœuvre de Sellick systématique. "
         "Voie nasotrachéale à éviter. Sondes plus petites (diamètre 5,5 à 7). Avoir à "
         "disposition et savoir utiliser rapidement une technique alternative de "
         "contrôle des voies aériennes."),
    ], TCW))
    story.append(Spacer(1, 2.5 * mm))
    story.append(section_bar("6 — HTA, prééclampsie, éclampsie"))
    story.append(Spacer(1, 1.5 * mm))
    story.append(theme_table([
        ("Définitions", "<b>HTA gravidique :</b> PAS ≥ 140 et/ou PAD ≥ 90 mmHg entre la "
         "20<sup>e</sup> SA et le 42<sup>e</sup> jour post-partum. <b>Prééclampsie :</b> "
         "HTA gravidique + protéinurie &gt; 0,3 g/24 h. <b>Prééclampsie sévère :</b> "
         "prééclampsie + au moins un critère parmi : HTA sévère (PAS ≥ 160 et/ou PAD "
         "≥ 110), oligurie &lt; 500 mL/24 h ou créatininémie &gt; 135 µmol/L ou "
         "protéinurie &gt; 5 g/24 h, OAP ou barre épigastrique persistante ou HELLP, "
         "éclampsie ou troubles neurologiques persistants, thrombopénie &lt; 100 G/L, "
         "HRP, retentissement fœtal. <b>Éclampsie :</b> crise convulsive "
         "tonicoclonique en contexte d'HTA gravidique. <b>HELLP :</b> hémolyse + "
         "cytolyse hépatique + thrombopénie. <i>Correction d'unité disclosed : la "
         "source imprime « 135 mmol/L » pour ce seuil de créatininémie (valeur "
         "incompatible avec la survie) — lu et corrigé ici en 135 µmol/L, probable "
         "artefact d'extraction « µ » → « m », même classe que ci-dessus (Fig. 1, "
         "sulprostone).</i>"),
        ("Diagnostic préhospitalier", "Principalement clinique ; mesure de la PA au "
         "repos, en décubitus latéral ou en position semi-assise. L'absence d'œdème "
         "localisé ou de prise de poids brutal n'élimine pas le diagnostic."),
        ("Signes d'alerte à rechercher", "HTA sévère ; signes d'éclampsie imminente "
         "(céphalées rebelles, troubles visuels, ROT polycinétiques) ; signes "
         "neurologiques évocateurs d'AVC ; signes de choc, contracture utérine, "
         "métrorragies (HRP) ; dyspnée/OAP ; douleur épigastrique (HELLP) ; "
         "oligurie/anurie."),
        ("Envoi d'équipe / orientation", "Envoi rapide d'une équipe médicale "
         "recommandé si suspicion de forme sévère/compliquée. Orientation selon des "
         "critères maternels (USI obstétricale ou réanimation adulte) ET fœtaux "
         "(maternité de type adapté à l'âge gestationnel)."),
        ("TIH — indications et contre-indications", "Indiqué vers une maternité de "
         "type adapté si signes de sévérité/complications entre 24 et 36 SA. "
         "Contre-indications : HRP connu/suspecté, instabilité hémodynamique, HTA non "
         "contrôlée, complication systémique (OAP, éclampsie, hématome sous-capsulaire "
         "du foie) — imposent des mesures thérapeutiques sur site avant TIH ultérieur. "
         "Anomalies sévères du RCF → extraction en urgence sur place quel que soit le "
         "type de maternité (pas de TIH). Non systématique si &lt; 24 SA (discuter une "
         "IMG) ou &gt; 36 SA (déclenchement), mais peut se discuter."),
        ("Monitorage", "FC, SpO2, FR, PA non invasive, et capnométrie si ventilation "
         "mécanique — recommandés pendant toute la prise en charge préhospitalière."),
        ("Traitement antihypertenseur — seuil et titration", "À débuter si PAS "
         "&gt; 160 ou PAD &gt; 110 mmHg. Administration par titration (voir Fig. 2). "
         "Ne pas faire descendre la PAM sous 100 mmHg ni la PAS sous 140 mmHg."),
    ], TCW))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P("<b>Fig. 2 — Traitement de l'HTA de la grossesse (organigramme de "
                    "titration, retranscrit à partir du rendu visuel de la source) :</b>",
                    S_BODY_SM))
    story.append(Spacer(1, 1 * mm))
    story.append(grid_table(
        ["Seuil de PA", "Conduite"],
        [
            ["Entrée : PAS &gt; 160 ou PAM &gt; 110 mmHg", "Orienter selon la sévérité "
             "vers l'un des 2 traitements ci-dessous, puis évaluer l'efficacité/"
             "tolérance après 30 min (voir les 4 lignes suivantes)."],
            ["— si en outre PAS &gt; 180 ou PAM &gt; 140 mmHg", "<b>Traitement "
             "d'attaque :</b> nicardipine 0,5-1 mg IV puis 4-7 mg en 30 min."],
            ["— si PAS &lt; 180 et PAM &lt; 140 mmHg", "<b>Traitement d'entretien :</b> "
             "nicardipine 1-6 mg/h IV ou labétalol 5-20 mg/h IV."],
            ["Après 30 min, si PAS &lt; 140 et PAM &lt; 100 mmHg", "Diminution voire "
             "arrêt du traitement."],
            ["Après 30 min, si 140 &lt; PAS &lt; 160 ou 100 &lt; PAM &lt; 120 mmHg",
             "Poursuite du traitement d'entretien : nicardipine 1-6 mg/h ou labétalol "
             "5-20 mg/h."],
            ["Après 30 min, si PAS &gt; 160 ou PAM &gt; 120 mmHg", "Association "
             "nicardipine 6 mg/h + labétalol 5-20 mg/h (ou clonidine 15-40 µg/h si "
             "contre-indication aux bêta-bloquants)."],
            ["Après 30 min, si effets secondaires (céphalées, palpitations…)",
             "Réduction de la nicardipine, associée à labétalol 5-20 mg/h ou clonidine "
             "15-40 µg/h si contre-indication aux bêta-bloquants."],
            ["Dans tous les cas (4 lignes ci-dessus)", "Réévaluation du traitement "
             "après 30 minutes puis chaque heure."],
        ], [55 * mm, CW_FULL - 55 * mm]))
    story.append(Spacer(1, 1.5 * mm))
    story.append(theme_table([
        ("Expansion volémique", "Possible en cas d'hypotension significative à "
         "l'instauration du traitement antihypertenseur, associée au décubitus "
         "latéral — prudente (risque d'OAP), repose sur les cristalloïdes."),
        ("Détresse respiratoire", "Possible chez la patiente prééclamptique, pouvant "
         "nécessiter une intubation — risque majoré d'intubation difficile et de "
         "poussée hypertensive à l'induction, à anticiper et prévenir."),
        ("Éclampsie — traitement", "Mesures générales de la crise convulsive + sulfate "
         "de magnésium 2 à 4 g IV lente puis entretien IV continu 1 g/h, + correction "
         "de l'HTA si présente. Récidive → 2<sup>e</sup> dose de 1,5-2 g. Les "
         "benzodiazépines injectables et la phénytoïne sont utilisables en "
         "préhospitalier mais sont moins efficaces que le sulfate de magnésium."),
        ("Prévention primaire (prééclampsie sévère)", "Sulfate de magnésium indiqué "
         "devant l'apparition de troubles neurologiques persistants (céphalées, "
         "troubles visuels, ROT polycinétiques), en l'absence de contre-indication "
         "(insuffisance rénale, pathologie neuromusculaire). Un inhibiteur calcique "
         "pour l'HTA ne doit pas retarder le sulfate de magnésium ; leur association "
         "justifie une adaptation des posologies."),
        ("Surveillance du sulfate de magnésium", "Évaluation répétée des ROT, de la "
         "fréquence respiratoire et de la conscience. Signes d'hypermagnésémie "
         "(ROT diminués/abolis, FR &lt; 10-12/min, troubles de conscience) → "
         "envisager l'arrêt de la perfusion et l'antagonisation par 1 g de gluconate "
         "de calcium IV."),
    ], TCW))
    return story

def _section_map_tiu_formation():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("7 — Menace d'accouchement prématuré (MAP)"))
    story.append(Spacer(1, 1.5 * mm))
    story.append(theme_table([
        ("Enjeu", "1<sup>re</sup> cause d'hospitalisation pendant la grossesse ; la "
         "morbi-mortalité néonatale est étroitement liée à l'âge gestationnel."),
        ("Diagnostic en régulation", "Contractions utérines régulières et douloureuses "
         "entre la 24<sup>e</sup> et la 36<sup>e</sup> SA révolue. Facteurs de risque à "
         "rechercher : antécédent d'accouchement prématuré, grossesse multiple, "
         "infection maternelle, métrorragies, placenta prævia, malformation utérine, "
         "béance cervico-isthmique, hydramnios."),
        ("Transport", "Décubitus latéral vers la maternité la plus proche de type "
         "adapté à l'âge gestationnel, sauf accouchement imminent justifiant l'envoi "
         "d'une équipe médicalisée."),
        ("Tocolyse préhospitalière", "Exceptionnellement initiée, en concertation avec "
         "l'équipe obstétricale receveuse ; choix selon les disponibilités locales et "
         "les protocoles de réseau."),
        ("Contre-indications / non-indications au transport", "Contre-indications : "
         "risque d'accouchement pendant le transport, souffrance fœtale aiguë patente. "
         "Non-indications médicales : TIU &lt; 24 SA ou &gt; 32 SA, transfert entre "
         "établissements de même type."),
        ("Éléments objectifs du TIU pour MAP", "Longueur et ouverture du col par "
         "échographie endovaginale, recherche de la fibronectine. Vérifier la "
         "réalisation de la 1<sup>re</sup> cure de corticothérapie de maturation "
         "pulmonaire fœtale avant tout transport. Réévaluation de la faisabilité du "
         "transport par l'équipe obstétricale au moment du départ."),
        ("Choix du tocolytique", "<b>Atosiban</b> (antagoniste de l'ocytocine) : "
         "tocolytique de choix en préhospitalier (profil de tolérance favorable, pas "
         "d'effet secondaire grave notable). <b>Inhibiteurs calciques</b> : les plus "
         "utilisés actuellement bien que hors AMM — risques cardiovasculaires "
         "potentiellement graves (hypotension, OAP). <b>Bêtamimétiques</b> : effets "
         "indésirables hémodynamiques fréquents, potentiellement graves. Grossesse "
         "gémellaire : éviter les inhibiteurs calciques, bêtamimétiques "
         "contre-indiqués. Ne jamais associer plusieurs tocolytiques ; ne pas changer "
         "de tocolytique efficace lors d'un transfert médicalisé."),
        ("Surveillance pendant le transport", "FC et PA systématiquement monitorées, "
         "avec rapport de surveillance écrit joint au dossier. Tococardiographie "
         "possible lors d'un transport de classe 3."),
    ], TCW))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P("<b>Tableau 4 — Choix du vecteur de transport selon l'état de la "
                    "patiente (circulaire DHOS/01/2006/273) :</b>", S_BODY_SM))
    story.append(Spacer(1, 1 * mm))
    story.append(grid_table(
        ["Classe", "Situations cliniques"],
        [
            ["Classe 1 — ambulance simple", "Rupture prématurée des membranes isolée ; "
             "MAP sans tocolyse IV (y compris grossesses gémellaires) ; MAP d'une "
             "grossesse simple avec tocolyse IV par antagoniste de l'ocytocine."],
            ["Classe 2 — transport infirmier interhospitalier (T2IH)", "MAP d'une "
             "grossesse simple avec tocolyse IV (médicalisation à discuter au cas par "
             "cas selon le tocolytique) ; MAP gémellaire avec tocolyse IV par "
             "antagoniste de l'ocytocine (à défaut classe 1 si vecteur 2 "
             "indisponible)."],
            ["Classe 3 — transport médicalisé (Smur)", "MAP avec tocolyse IV : "
             "médicalisation à discuter selon le tocolytique ; MAP avec dilatation du "
             "col ≥ 4 cm et terme &lt; 30 SA : à discuter avec le Samu en conférence "
             "téléphonique demandeur/receveur."],
        ], [50 * mm, CW_FULL - 50 * mm]))
    story.append(Spacer(1, 2.5 * mm))
    story.append(section_bar("8 — Transferts in utero (TIU) interhospitaliers"))
    story.append(Spacer(1, 1.5 * mm))
    story.append(theme_table([
        ("Organisation", "Régionale, intégrée aux réseaux de périnatalité (circulaire "
         "DHOS/01/2006/273 du 21/06/2006). Une cellule de périnatalité développe et "
         "applique les protocoles consensuels entre Samu, obstétriciens, "
         "néonatologues, anesthésistes réanimateurs et sages-femmes, et recherche les "
         "places adaptées."),
        ("Indication", "Inadéquation entre la structure d'hospitalisation et la "
         "pathologie maternelle/fœtale ; le bénéfice pour l'enfant est d'autant plus "
         "élevé que le terme est précoce. Si transport maternel pour pathologie non "
         "obstétricale, une surveillance obstétricale adaptée doit être possible dans "
         "la structure d'accueil."),
        ("Contre-indications fœtales", "Anomalies du RCF significatives imposant une "
         "extraction sur place en urgence (engagement anticipé du Smur pédiatrique si "
         "terme &lt; 32 SA ou poids estimé &lt; 1500 g)."),
        ("Contre-indications maternelles", "Risque d'accouchement pendant le "
         "transport, suspicion d'HRP, HTA gravidique sévère non contrôlée, "
         "instabilité hémodynamique, placenta prævia avec métrorragies actives."),
        ("Règles de terme", "Pas d'indication de TIU avant 24 SA (hors cause non liée "
         "à la grossesse) ; au-delà de 32 SA, le terme seul ne justifie pas un "
         "transfert vers un type supérieur ; pas d'indication médicale fœtale entre "
         "établissements de même type."),
        ("Décision pour MAP", "L'équipe demandeuse évalue la longueur du col par "
         "échographie endovaginale. Décision fonction de 5 éléments : dilatation et "
         "longueur du col, contractions utérines, terme, type de l'établissement "
         "demandeur. À partir de 32 SA, une dilatation ≥ 4 cm est une "
         "contre-indication au transfert ; en deçà, l'opportunité se discute selon le "
         "type d'établissement et la durée de transport."),
        ("Orientation par terme", "Type 2 : à partir de 32 SA avec poids fœtal estimé "
         "&gt; 1500 g. Type 3 : menace d'accouchement très prématuré (24 SA à "
         "31 SA + 6 j) ou poids estimé &lt; 1500 g, grossesse triple."),
        ("Décision et modalités", "Accord entre le médecin demandeur (présent auprès "
         "de la patiente) et le médecin receveur, puis avec le médecin régulateur du "
         "Samu et le médecin transporteur du Smur si le transport est médicalisé — les "
         "3 classes de vecteur sont les mêmes que celles du Tableau 4 (rupture "
         "prématurée isolée, diabète gestationnel, cholestase, prééclampsie et "
         "métrorragies de prævia s'ajoutent aux critères MAP selon leur sévérité et la "
         "durée de transport). État clinique réévalué au départ pour confirmer la "
         "faisabilité."),
        ("Pendant le transport", "Décubitus latéral ceinturé (prévention de la "
         "compression cave) ; dossier obstétrical accompagne systématiquement la "
         "patiente ; traçabilité écrite de la surveillance, des événements "
         "intercurrents et des traitements."),
    ], TCW))
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("9 — Formation, évaluation des pratiques, réseaux (résumé)",
                    color=GREY),
        Spacer(1, 1.5 * mm),
        P(
            "Formation initiale puis continue recommandée pour tous les professionnels "
            "Samu/Smur aux urgences obstétricales préhospitalières (accouchement "
            "physiologique et situations complexes : procidence du cordon, dystocie "
            "des épaules, siège, hémorragies) — stages en maternité, supports "
            "multimédias, simulation sur mannequins. Programme d'évaluation des "
            "pratiques professionnelles selon une méthode HAS, avec objectifs de "
            "qualité en régulation (formation des permanenciers/régulateurs, items "
            "systématiques du compte rendu, indicateurs de délai) et en Smur "
            "(formation continue, liste et entretien du matériel dédié à "
            "l'accouchement, protocoles de renfort — sage-femme, Smur pédiatrique). "
            "Développement recommandé de réseaux périnatals régionaux associant "
            "obstétriciens, sages-femmes, néonatologues/pédiatres, anesthésistes "
            "réanimateurs et Samu-Smur, avec protocoles partagés et transferts "
            "périnatals systématiquement régulés par le Samu.", S_BODY_SM),
    ]))
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("Sources et traçabilité", color=GREY))
    story.append(Spacer(1, 2 * mm))
    story.append(P(
        "<b>Document source :</b> « Urgences obstétricales extrahospitalières » — RFE "
        "SFAR/SFMU (avec CNGOF, Collège national des sages-femmes, GFRUP). Groupe de "
        "travail présidé par G. Bagou (SFAR/SFMU), secrétaire V. Hamel. 9 chapitres "
        "traités indépendamment. Recommandations validées au 3<sup>e</sup> trimestre "
        "2010.", S_SOURCE))
    story.append(Spacer(1, 1 * mm))
    story.append(P("<b>Version :</b> Ann Fr Anesth Reanim 2012;31:652-665. "
                    "doi:10.1016/j.annfar.2012.06.001.", S_SOURCE))
    story.append(Spacer(1, 1 * mm))
    story.append(P("<b>Méthodologie :</b> méthode GRADE annoncée, cotation Delphi "
                    "(2 tours), sans grade individuel 1+/2+/A/B/C — accord fort quasi "
                    "systématique. Voir détail en page 1.", S_SOURCE))
    story.append(Spacer(1, 1 * mm))
    story.append(P(
        "<b>URL source :</b> https://sfar.org/wp-content/uploads/2015/10/"
        "2_AFAR_Urgences-Obstetricales-Extrahospitalieres.pdf", S_SOURCE))
    story.append(Spacer(1, 1 * mm))
    story.append(P(
        "<b>Couverture :</b> intégralité du contenu clinique actionnable de 8 des 9 "
        "chapitres (1 à 8), condensé en tableaux Thème/Détail ; seul le chapitre 9, "
        "de nature organisationnelle (formation/évaluation des pratiques), est "
        "résumé — voir texte intégral pour son détail complet. 4 tableaux et 2 "
        "figures (algorithmes HPP et HTA) retranscrits intégralement à partir d'un "
        "rendu visuel des pages sources.", S_SOURCE))
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Avertissement — document validé 2010 :</b> cette fiche de synthèse "
        "indépendante reprend l'intégralité du contenu clinique actionnable du texte "
        "source, mais ne le remplace pas et n'est ni éditée ni validée par la SFAR ou "
        "la SFMU. Les seuils, posologies (notamment tocolytiques, antihypertenseurs, "
        "sulfate de magnésium) et protocoles de régulation/transport ayant pu évoluer "
        "depuis 2010, se référer à un avis spécialisé et aux recommandations "
        "actualisées avant toute décision thérapeutique.", S_BODY_SM),
        bg=GREY_LIGHT, border=GREY))
    return story

def _section_regulation_accouchement():
    story = _section_intro_regulation()
    story.extend(_section_accouchement_inopine())
    return story

def _section_hemorragies_trauma_hta():
    story = _section_hemorragies()
    story.extend(_section_trauma_hta())
    return story

SECTIONS = [
    ("Régulation Samu, accouchement inopiné & nouveau-né", _section_regulation_accouchement),
    ("Hémorragies, traumatismes & HTA gravidique", _section_hemorragies_trauma_hta),
    ("MAP, transferts in utero, formation & sources", _section_map_tiu_formation),
]

def _make_doc(path=None):
    return SimpleDocTemplate(path or OUT, pagesize=A4,
                              leftMargin=MARGIN, rightMargin=MARGIN,
                              topMargin=32 * mm, bottomMargin=16 * mm,
                              title="Fiche SFAR 2010 - Urgences obstetricales extrahospitalieres",
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

    doc = _make_doc()
    story = _build_upto(fns)
    doc.build(story, onFirstPage=on_page_final, onLaterPages=on_page_final)
    print("OK ->", OUT, f"({total_pages} pages)")

if __name__ == "__main__":
    build()
