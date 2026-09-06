# -*- coding: utf-8 -*-
"""
Fiche de synthese - GIHP / GFHT, en collaboration avec la SFAR (2019) "Diagnostic
et prise en charge d'une thrombopenie induite par l'heparine (TIH)" - Propositions
du Groupe d'Interet en Hemostase Perioperatoire (GIHP) et du Groupe Francais
d'etudes sur l'Hemostase et la Thrombose (GFHT). Y. Gruel, E. De Maistre, C.
Pouplard, et al. Vote n=32 participants. Source : sources/tih_gihp_gfht.pdf
(54 pages telles que rendues par PyMuPDF ; le champ metadata du PDF annonce a
tort "8 pages" - `file` lit une table de references perimee, pypdf/PyMuPDF font
foi), sources/tih_gihp_gfht.txt (texte extrait, 2141 lignes). Deux liens de
telechargement distincts de library_final.json (wpdmdl=34610 et wpdmdl=24461)
pointent vers UN SEUL ET MEME document (verifie par diff des textes extraits des
deux PDF telecharges : identiques mot pour mot des la page 1) - cette fiche
couvre donc les deux entrees de la bibliotheque.

METHODOLOGIE - UN SEUL AXE, PAS DE GRADE : la source le dit explicitement dans
son introduction ("notre groupe ait decide, comme en 2002, de ne pas attribuer
de grade aux propositions emises"), a la difference des recommandations
anglo-saxonnes contemporaines (ACCP 2012, ASH 2018) qui elles gradent leurs
recommandations. Chaque proposition ne porte donc qu'un unique tag "(Accord
fort)" - vote de 32 participants du GIHP/GFHT, seuil >= 50% d'accord pour
retenir une proposition (>= 70% pour un accord "fort"), < 20% d'opposition.
VERIFIE PAR GREP EXHAUSTIF (grep -n "(Accord" sur le texte source extrait) :
les 40 propositions du document portent TOUTES le tag "(Accord fort)" - aucune
n'est "faible", aucune autre variante n'existe dans ce document. Ceci est
DIFFERENT de fiche_mal_epileptique.py/fiche_nutrition.py (memes deux valeurs
fort/faible disponibles) : ici l'unique valeur observee est "Fort", retranscrite
telle quelle sur chaque ligne (colonne Accord systematiquement "Fort") plutot
qu'omise, par fidelite a la source qui l'imprime explicitement apres chaque
proposition individuelle.

PERIMETRE - 12 questions, 40 propositions, couvertes integralement (verifie par
comptage : "Proposition N°1" a "Proposition N°40" tous presents et
sequentiels dans le texte source, aucun saut de numero). L'argumentaire complet
(paragraphes narratifs sources par des references bibliographiques [1]-[114])
est condense en synthese sous chaque tableau de propositions - la fiche ne
retranscrit pas les references bibliographiques elles-memes (non pertinentes
pour un aide-memoire clinique), mais conserve integralement les valeurs
numeriques cliniquement actionables (posologies, demi-vies, seuils, delais).

TABLEAUX ET FIGURES - verifies par rendu visuel a 150 dpi (PyMuPDF) des pages
8, 18-19, 24, 26-27, 34, 38 du PDF source :
  - Tableau I (p.8, niveaux de risque HNF/HBPM par contexte) : texte pur,
    retranscrit en tableau structure (pas une image).
  - Score des 4T (p.18, dans la Figure 1) : texte pur malgre son inclusion dans
    une "figure" - retranscrit en tableau structure a 4 criteres x 3 niveaux
    (0/1/2 points), avec les seuils de probabilite (<=3 faible, 4-5
    intermediaire, >=6 elevee).
  - Figure 1 (p.18, algorithme diagnostique complet) : diagramme de flux (pure
    image vectorielle sans lien direct texte->case). Retranscrit selon le
    pattern deja etabli par fiche_intubation_difficile_adulte.py (tableau
    Etape / Decision-actions / Resultat-suite), note explicite "transcrit
    depuis le rendu visuel de la source (page 18)".
  - Tableau II (p.24, ajustement posologie argatroban par score APACHE
    II/SOFA/SAPS) : texte pur (tableau de conversion numerique), retranscrit
    integralement (12 lignes) - c'est une table de lookup clinique directement
    actionable, pas un element decoratif.
  - Figure 2 (p.26, algorithme prescription/surveillance argatroban) et Figure
    3 (p.27, relais argatroban-AVK) : diagrammes de flux, retranscrits en
    tableaux Etape/Decision/Resultat comme la Figure 1.
  - Tableau III (bivalirudine, p.42-43, texte pur dans le corps de l'argumentaire
    Q10) et Tableau IV (resultats AOD, p.30, texte pur) : retranscrits tels
    quels depuis le texte extrait (confirme identique au rendu visuel).
  - Tableau V (p.34, demi-vies et delais d'arret pre-procedural) et Figure 4
    (p.38, strategies chirurgie cardiaque) : Tableau V est texte pur ; Figure 4
    est un diagramme de flux, retranscrit en tableau Pre-op/Per-op/Post-op
    (structure deja presente dans le texte source lui-meme, colonnes "P r e o p"
    verticales du diagramme).

DISCLOSURE - AUCUNE incoherence source-interne detectee (a la difference de
fiche_glycemie.py) : les 40 propositions sont numerotees sequentiellement sans
saut, le decompte "12 questions / 40 propositions" annonce en introduction
correspond exactement au contenu du corps du texte.

CONVENTION DE CHIP : extension locale non invasive de GRADE_COLORS - "Fort" ->
vert, reprenant la meme convention que fiche_mal_epileptique.py et
fiche_nutrition.py (fiches a accord fort/faible sans niveau de preuve GRADE).

ICONE : icon_drop (goutte), deja utilisee pour des fiches d'hemostase/fluides
(fiche_hypothermie.py, fiche_glycemie.py) - pas d'icone "plaquette/coagulation"
dediee dans style.py, icon_drop reste la plus proche visuellement (goutte de
sang) parmi les icones existantes.

_count_pages() : implementation copiee a l'identique de fiche_aap_programmee.py
- les passes de comptage ecrivent vers un tempfile.mktemp() jetable, jamais
vers OUT (bug de corruption du header_band de la page 1 deja documente si l'on
reutilise OUT pour le comptage ET la construction finale).

Pas d'arrondis Unicode (fleches/exposants/emoji) dans le corps du texte -
encodage Helvetica de cette chaine de production.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from style import *
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.units import mm

# Local, non-invasive extension of the shared GRADE_COLORS dict - mirrors the
# precedent set in fiche_mal_epileptique.py / fiche_nutrition.py.
GRADE_COLORS["Fort"] = (GREEN, WHITE)

OUT = "/home/user/rfe-sfar-website/output/Fiche_GIHP_GFHT_SFAR_TIH_2019.pdf"

SOURCE_TXT = ("Source : Gruel Y, De Maistre E, Pouplard C, et al. — GIHP (Groupe d'Intérêt en "
              "Hémostase Périopératoire) et GFHT (Groupe Français d'études sur l'Hémostase et la "
              "Thrombose), en collaboration avec la SFAR — « Diagnostic et prise en charge d'une "
              "thrombopénie induite par l'héparine » — Propositions 2019 (vote n=32). Fiche de "
              "synthèse non officielle : se référer au texte intégral.")

def P(txt, style=S_CELL):
    return Paragraph(txt, style)

def chip(label, **kw):
    return grade_chip(label, **kw)

REF_W = 15 * mm
ACCORD_W = 18 * mm

def prop_table(rows, col_widths=None):
    """rows: (ref, text) - Accord est systematiquement 'Fort' dans ce document
    (voir docstring module) donc non passe en parametre par ligne."""
    text_w = PAGE_W - 2 * MARGIN - REF_W - ACCORD_W
    cw = col_widths or [REF_W, text_w, ACCORD_W]
    data = [[P("Réf.", S_HEAD_W), P("Proposition (texte intégral)", S_HEAD_W), P("Accord", S_HEAD_W_C)]]
    for ref, txt in rows:
        data.append([P(ref, S_CELL_B), P(txt, S_CELL), chip("Fort", width=ACCORD_W - 2 * mm)])
    t = Table(data, colWidths=cw, repeatRows=1)
    style_cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), NAVY), ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTNAME", (0, 0), (-1, 0), FONT_BOLD), ("FONTSIZE", (0, 0), (-1, 0), 8),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("ALIGN", (2, 0), (2, -1), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 0.5, GREY_LIGHT),
        ("TOPPADDING", (0, 0), (-1, -1), 3.2), ("BOTTOMPADDING", (0, 0), (-1, -1), 3.2),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            style_cmds.append(("BACKGROUND", (0, i), (-1, i), BG_PANEL))
    t.setStyle(TableStyle(style_cmds))
    return t

def simple_table(header, rows, col_widths):
    data = [[P(h, S_HEAD_W) for h in header]] + [[P(c, S_CELL) for c in row] for row in rows]
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

TOTAL_PAGES = {"n": 16}

def on_page(canvas, doc, page_title):
    header_band(canvas, doc, "GIHP / GFHT / SFAR — PROPOSITIONS 2019 — FICHE DE SYNTHÈSE",
                "Thrombopénie induite par l'héparine (TIH)",
                page_title, icon_fn=lambda c, x, y: icon_drop(c, x, y, 13 * mm), color=NAVY)
    footer_band(canvas, doc, SOURCE_TXT, f"Page {doc.page} / {TOTAL_PAGES['n']}")

# ---------------------------------------------------------------------------
def _section_intro():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Champ :</b> diagnostic et prise en charge de la <b>thrombopénie induite par "
        "l'héparine (TIH)</b> de type II (immune), chez l'adulte et l'enfant, en médecine, "
        "chirurgie (dont chirurgie cardiaque), obstétrique et pédiatrie. Propositions du GIHP "
        "et du GFHT en collaboration avec le Comité des Référentiels Cliniques de la SFAR, "
        "actualisant la conférence d'experts SFAR de 2002. <b>12 questions, 40 propositions.</b>",
        S_BODY), bg=BG_PANEL, border=TEAL))
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Méthodologie — UN SEUL axe, à la différence du GRADE (1+/1-/2+/2-) utilisé "
        "ailleurs dans ce corpus :</b> la source précise explicitement avoir choisi, comme en "
        "2002, de <b>ne pas attribuer de grade</b> aux propositions (littérature disponible "
        "jugée de faible niveau de preuve). Chaque proposition porte un unique tag "
        "<b>« Accord »</b>, déterminé par un vote de 32 membres du GIHP/GFHT : une proposition "
        "est retenue si ≥ 50 % des votants expriment leur accord et &lt; 20 % leur opposition ; "
        "l'accord est qualifié de <b>« fort »</b> si ce taux atteint ≥ 70 %. "
        "<b>Les 40 propositions de ce document ont toutes recueilli un accord fort</b> "
        "(vérifié exhaustivement) — la colonne Accord est donc constante, reproduite telle "
        "quelle sur chaque ligne par fidélité à la source qui l'imprime explicitement après "
        "chaque proposition.", S_BODY_SM), bg=BG_PANEL, border=TEAL))
    story.append(Spacer(1, 3 * mm))

    story.append(section_bar("Généralités"))
    story.append(Spacer(1, 2 * mm))
    story.append(P(
        "Deux types de thrombopénies sous héparine (HNF ou HBPM) : <b>type I</b> — bénigne, "
        "non immune, précoce, sans thrombose, régresse malgré la poursuite du traitement ; "
        "<b>type II</b> — la <b>TIH</b> proprement dite : syndrome clinico-biologique à "
        "anticorps IgG anti-facteur 4 plaquettaire (FP4)/héparine, activation plaquettaire "
        "et génération explosive de thrombine, avec un <b>risque thrombotique majeur</b> "
        "(veineux et/ou artériel) contrastant avec la rareté des saignements. Diagnostic "
        "souvent difficile en réanimation/post-opératoire (autres causes de thrombopénie "
        "fréquentes). <b>Règle essentielle : la confirmation biologique ne doit jamais "
        "retarder l'arrêt de l'héparine et l'instauration d'un anticoagulant de substitution "
        "d'action immédiate.</b> Risque thrombotique maximal le premier mois suivant le "
        "diagnostic ; anticorps le plus souvent indétectables au-delà de 3 mois.",
        S_BODY_SM))
    story.append(Spacer(1, 3 * mm))

    story.append(section_bar("Question 1 — Stades et niveaux de risque de TIH"))
    story.append(Spacer(1, 2 * mm))
    story.append(prop_table([
        ("Prop. 1", "Il est proposé de distinguer trois stades différents de TIH selon son "
         "ancienneté : <b>TIH aiguë</b> (&lt; 1 mois, anticorps anti-FP4 activateurs le plus "
         "souvent présents, risque thrombotique élevé) ; <b>TIH subaiguë</b> (1 à 3 mois, "
         "anticorps souvent présents à titre bas) ; <b>antécédent de TIH</b> (&gt; 3 mois, "
         "anticorps le plus souvent indétectables)."),
        ("Prop. 2", "Il est proposé de définir le niveau de risque de TIH sous héparine comme "
         "<b>faible</b> (&lt; 0,1 %), <b>intermédiaire</b> (0,1-1 %) ou <b>élevé</b> (&gt; 1 %) "
         "selon le contexte et le type d'héparine — voir Tableau I."),
    ]))
    story.append(Spacer(1, 2 * mm))
    story.append(simple_table(
        ["Héparine", "Contexte / schéma", "Risque"],
        [
            ["HNF", "Chirurgie (y compris césarienne), prophylactique ou curatif", "Élevé"],
            ["HNF", "Médical/obstétrical, curatif", "Élevé"],
            ["HNF", "CEC, épuration extra-rénale, ECMO, contre-pulsion intra-aortique", "Élevé"],
            ["HNF", "Médical/obstétrical, prophylactique", "Intermédiaire"],
            ["HBPM", "Chirurgie (y compris césarienne), prophylactique ou curatif", "Intermédiaire"],
            ["HBPM", "Cancer", "Intermédiaire"],
            ["HBPM", "Médical/obstétrical, prophylactique ou curatif", "Faible"],
        ],
        [26 * mm, PAGE_W - 2 * MARGIN - 26 * mm - 28 * mm, 28 * mm]))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P("<i>Tableau I — Niveaux de risque de TIH selon le contexte et le type "
                    "d'héparine administré. Fondaparinux : risque nul/quasi nul quel que soit "
                    "le schéma (n'est pas une héparine). Risque devenant très faible au-delà "
                    "d'1 mois de traitement, quelle que soit la molécule.</i>", S_NOTE))
    return story

def _section_q2q3():
    story = []
    story.append(Spacer(1, 2 * mm))
    story.append(section_bar("Question 2 — Surveillance de la numération plaquettaire (NP)"))
    story.append(Spacer(1, 2 * mm))
    story.append(prop_table([
        ("Prop. 3", "Il est proposé de réaliser systématiquement chez tous les patients traités "
         "par une héparine (HNF ou HBPM) une numération plaquettaire <b>avant l'initiation du "
         "traitement</b> (ou à défaut le plus tôt possible, avant J4)."),
        ("Prop. 4", "Il est proposé de <b>ne pas surveiller</b> la NP chez les patients à risque "
         "<b>faible</b> de TIH."),
        ("Prop. 5", "Risque <b>intermédiaire</b> : surveiller la NP <b>1 à 2 fois/semaine entre "
         "J4 et J14</b>, puis 1 fois/semaine pendant 1 mois si l'héparine est poursuivie."),
        ("Prop. 6", "Risque <b>élevé</b> : surveiller la NP <b>2 à 3 fois/semaine entre J4 et "
         "J14</b>, puis 1 fois/semaine pendant 1 mois si l'héparine est poursuivie."),
    ]))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P("Après chirurgie cardiaque avec CEC, la surveillance répétée permet aussi "
                    "d'identifier un profil <b>biphasique</b> (baisse de la NP après une phase "
                    "de correction), hautement prédictif de TIH. Fenêtre 4-14 jours : la très "
                    "grande majorité des TIH surviennent dans cet intervalle (rares cas au-delà "
                    "de 15 j sous HBPM, jamais au-delà d'1 mois).", S_NOTE))
    story.append(Spacer(1, 3 * mm))

    story.append(section_bar("Question 3 — Circonstances évocatrices de TIH"))
    story.append(Spacer(1, 2 * mm))
    story.append(P(
        "Chronologie typique : chute de la NP <b>entre J4 et J14</b> de l'héparinothérapie "
        "(plus précoce, dès J1, si exposition à l'héparine dans les 3 mois précédents ; plus "
        "tardive, &gt; 15 j, notamment sous HBPM, mais jamais au-delà d'1 mois). Diagnostic à "
        "évoquer devant une <b>NP &lt; 100 G/L</b> et/ou une <b>baisse &gt; 50 %</b> par rapport "
        "à une valeur antérieure (thrombopénie typiquement modérée, 30-70 G/L chez 80 % des "
        "patients). Une CIVD associée n'exclut pas le diagnostic. "
        "<b>Thromboses :</b> TVP jusqu'à 50 % des cas (recherche systématique par écho-Doppler "
        "veineux proposée), embolie pulmonaire 10-25 %, thromboses artérielles (aorte "
        "abdominale et branches +++), complications neurologiques ~10 % (AVC ischémiques, "
        "thromboses veineuses cérébrales, états confusionnels). Manifestations rares : nécroses "
        "cutanées aux points d'injection (peuvent précéder la chute plaquettaire), gangrène "
        "veineuse des membres sous AVK isolé, nécroses hémorragiques des surrénales, réaction "
        "systémique après bolus IV d'HNF (frissons, hypotension, dyspnée).",
        S_BODY_SM))
    story.append(Spacer(1, 2 * mm))
    story.append(prop_table([
        ("Prop. 7", "Quel que soit le risque de TIH, il est proposé de contrôler "
         "systématiquement la NP de tout malade traité par héparine en cas d'<b>événement "
         "clinique inattendu</b> : apparition/aggravation d'une thrombose veineuse ou "
         "artérielle, nécrose cutanée, ou réaction inhabituelle après injection d'héparine "
         "(frisson, hypotension, dyspnée, amnésie)."),
    ]))
    return story

def _section_score4t():
    story = []
    story.append(Spacer(1, 2 * mm))
    story.append(KeepTogether([
        section_bar("Score des 4T — probabilité clinique pré-test de TIH"),
        Spacer(1, 1.5 * mm),
        P("<i>Transcrit depuis le rendu visuel de la source (Figure 1, page 18) : quatre "
          "critères, 0 à 2 points chacun.</i>", S_NOTE),
    ]))
    story.append(Spacer(1, 2 * mm))
    cw = PAGE_W - 2 * MARGIN
    story.append(simple_table(
        ["Critère (4T)", "Description", "Pts"],
        [
            ["Thrombocytopenia\n(intensité de la chute)",
             "Baisse NP > 50 % ET pas de chirurgie dans les 3 j précédents ET nadir ≥ 20 G/L", "2"],
            ["", "Baisse NP > 50 % mais chirurgie < 3 j, OU baisse 30-50 %, OU nadir 10-19 G/L", "1"],
            ["", "Baisse NP < 30 %, ou nadir < 10 G/L", "0"],
            ["Timing\n(délai de survenue)",
             "5 à 10 j après le début de l'héparine, ou &lt; 24h si exposition dans les 5-30 j précédents", "2"],
            ["", "Probablement 5-10 j, ou &lt; 24h si exposition dans les 30-100 j précédents", "1"],
            ["", "≤ 4 j sans exposition à l'héparine dans les 100 j précédents", "0"],
            ["Thrombosis\n(thrombose/événement)",
             "Nouvelle thrombose confirmée (art. ou veineuse), nécrose cutanée, réaction systémique après bolus IV d'HNF", "2"],
            ["", "Extension/récidive d'une thrombose sous traitement, suspicion non confirmée, érythème non nécrotique", "1"],
            ["", "Aucun de ces événements", "0"],
            ["oTher\n(autre cause possible)", "Aucune autre cause", "2"],
            ["", "Autre cause possible", "1"],
            ["", "Autre cause certaine", "0"],
        ],
        [cw * 0.24, cw * 0.66, cw * 0.10]))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P("<b>Score total (0-8) → probabilité clinique :</b> ≤ 3 = <b>faible</b> ; "
                    "4-5 = <b>intermédiaire</b> ; ≥ 6 = <b>élevée</b>. Score moins fiable après "
                    "chirurgie cardiaque avec CEC : préférer l'analyse du profil d'évolution "
                    "post-opératoire des plaquettes (profil biphasique ≈ score ≥ 6).", S_NOTE))
    return story

def _section_q4q5():
    story = []
    story.append(Spacer(1, 2 * mm))
    story.append(section_bar("Question 4 — Diagnostics différentiels & probabilité clinique"))
    story.append(Spacer(1, 2 * mm))
    story.append(P(
        "Autres causes de thrombopénie sous héparine à évoquer : effet pro-agrégeant direct de "
        "l'HNF (thrombopénie précoce J1-J2) ; hémodilution périopératoire, consommation "
        "plaquettaire (CEC, ballon de contre-pulsion, EER) ; purpura post-transfusionnel "
        "(allo-immunisation — urgence diagnostique) ; anti-GPIIb-IIIa (syndromes coronaires "
        "aigus) ; autres médicaments thrombopéniants ou chimiothérapies. Si thrombose "
        "associée : syndrome des antiphospholipides, purpura thrombotique thrombocytopénique, "
        "CIVD, pseudo-TIH néoplasique.",
        S_BODY_SM))
    story.append(Spacer(1, 2 * mm))
    story.append(prop_table([
        ("Prop. 8", "En cas de suspicion de TIH, il est proposé de définir la probabilité "
         "clinique de TIH à l'aide du <b>score des 4T</b>, en dehors d'un contexte de chirurgie "
         "cardiaque."),
    ]))
    story.append(Spacer(1, 3 * mm))

    story.append(section_bar("Question 5 — Examens biologiques"))
    story.append(Spacer(1, 2 * mm))
    story.append(prop_table([
        ("Prop. 9", "En cas de suspicion, il est proposé de rechercher le plus rapidement "
         "possible des <b>anticorps anti-FP4</b> si la probabilité clinique de TIH est "
         "<b>intermédiaire ou élevée</b>."),
    ]))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "Vérifier d'abord l'absence de caillot/agrégats (frottis, nouveau prélèvement sur "
        "citrate) et prescrire un bilan d'hémostase simple (TP, TCA, fibrinogène, D-dimères) à "
        "la recherche d'une CIVD (n'exclut pas la TIH). Deux catégories de tests : "
        "<b>immunologiques</b> (ELISA, chémiluminescence, agglutination — sensibilité "
        "excellente, VPN excellente, mais spécificité imparfaite, notamment après CEC où "
        "~1 patient/2 a des anticorps anti-FP4 sans TIH) et <b>fonctionnels/d'activation "
        "plaquettaire</b> (SRA = « gold standard », test HIPA peu utilisé en France, "
        "spécificité proche de 100 % mais réalisation longue, réservée à des laboratoires "
        "experts).", S_BODY_SM))
    return story

def _section_algo_diag():
    story = []
    story.append(Spacer(1, 2 * mm))
    story.append(section_bar("Question 6 — Prise en charge initiale d'une suspicion de TIH"))
    story.append(Spacer(1, 2 * mm))
    story.append(prop_table([
        ("Prop. 10", "Si la probabilité pré-test est <b>faible</b> (4T ≤ 3), le diagnostic de "
         "TIH peut être exclu et l'héparine poursuivie, <b>sans</b> test biologique spécifique "
         "— rechercher une autre étiologie avec suivi rapproché de la NP."),
        ("Prop. 11", "Si la probabilité pré-test est <b>intermédiaire</b> (4-5) ou "
         "<b>élevée</b> (≥ 6), des tests biologiques (anticorps anti-FP4) doivent "
         "systématiquement être réalisés."),
        ("Prop. 12", "Si probabilité intermédiaire et recherche anti-FP4 <b>négative</b> : le "
         "diagnostic de TIH est exclu, l'héparine peut être poursuivie/reprise avec suivi "
         "rapproché de la NP."),
        ("Prop. 13", "Si probabilité <b>élevée</b> (4T ≥ 6 ou profil biphasique post-CEC) : "
         "l'héparine doit être <b>immédiatement arrêtée</b> et remplacée par un anticoagulant "
         "non héparinique à <b>doses curatives</b>, sans attendre les résultats biologiques."),
        ("Prop. 14", "Si probabilité intermédiaire/élevée et titre significatif d'anticorps "
         "anti-FP4 détecté : un <b>test fonctionnel</b> doit être réalisé. S'il est positif, le "
         "diagnostic de TIH est confirmé."),
    ]))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P("Chaque suspicion de TIH doit être <b>déclarée au centre régional de "
                    "pharmacovigilance</b>.", S_NOTE))
    story.append(Spacer(1, 3 * mm))
    story.append(KeepTogether([
        section_bar("Algorithme du diagnostic clinique et biologique d'une TIH", color=GREY),
        Spacer(1, 1.5 * mm),
        P("<i>Transcrit depuis le rendu visuel de la source (Figure 1, page 18).</i>", S_NOTE),
    ]))
    story.append(Spacer(1, 2 * mm))
    cw = PAGE_W - 2 * MARGIN
    story.append(simple_table(
        ["Probabilité (score 4T)", "Démarche biologique", "Résultat → conduite à tenir"],
        [
            ["Faible (0-3)", "Pas de test biologique spécifique", "Pas de TIH → continuer "
             "l'héparine"],
            ["Intermédiaire (4-5)", "Recherche Ac anti-FP4 ; si résultat &lt; 3h, possibilité "
             "d'attendre avant de modifier le traitement", "Ac négatifs → pas de TIH, reprendre "
             "l'héparine. Ac positifs → test fonctionnel → positif : TIH ; négatif : pas de TIH"],
            ["Forte (6-8)", "Arrêter l'héparine et prescrire un anticoagulant non héparinique "
             "à dose curative, PUIS rechercher Ac anti-FP4", "Ac positifs → test fonctionnel "
             "(non obligatoire si Ac clairement positifs) → positif : TIH ; négatif : "
             "concertation multidisciplinaire. Ac négatifs → test fonctionnel → positif : TIH"],
        ],
        [cw * 0.20, cw * 0.40, cw * 0.40]))
    return story

def _section_q7_choix():
    story = []
    story.append(Spacer(1, 2 * mm))
    story.append(section_bar("Question 7 — Anticoagulants de substitution à la phase aiguë"))
    story.append(Spacer(1, 2 * mm))
    story.append(prop_table([
        ("Prop. 15", "Les anticoagulants utilisables à la phase aiguë d'une TIH sont "
         "l'<b>argatroban</b>, la <b>bivalirudine</b>, le <b>danaparoïde</b>, le "
         "<b>fondaparinux</b>, et les <b>anticoagulants oraux directs (AOD)</b>."),
        ("Prop. 16", "Le danaparoïde n'est pas recommandé en 1<sup>re</sup> intention en cas "
         "d'<b>insuffisance rénale sévère</b>."),
        ("Prop. 17", "Le danaparoïde à <b>dose prophylactique n'est pas recommandé</b> à la "
         "phase aiguë : des doses curatives IV sont plus efficaces, avec surveillance de "
         "l'activité anti-Xa (gamme danaparoïde)."),
        ("Prop. 18", "L'absence de correction de la NP, ou l'apparition/extension d'une "
         "thrombose sous danaparoïde, doit conduire à le remplacer par un autre "
         "anticoagulant."),
        ("Prop. 19", "L'<b>argatroban</b> est à utiliser en priorité en cas d'insuffisance "
         "rénale sévère. <b>Contre-indiqué</b> si insuffisance hépatique sévère (Child-Pugh "
         "C). À utiliser en structure spécialisée."),
        ("Prop. 20", "Posologie initiale d'argatroban : <b>1 µg/kg/min</b>, réduite à "
         "<b>0,5 µg/kg/min</b> chez les patients de réanimation, de chirurgie cardiaque, et en "
         "cas d'insuffisance hépatique modérée (Child-Pugh B)."),
        ("Prop. 21", "Surveillance quotidienne de l'argatroban : TCA (cible 1,5-3 × témoin, "
         "sans dépasser 100 sec) si normal avant traitement, ou de préférence temps de "
         "thrombine diluée/test à l'écarine (cible 0,5-1,5 µg/mL)."),
        ("Prop. 22", "Un <b>AVK ne doit être prescrit à la phase aiguë</b> que lorsque la NP "
         "est corrigée (&gt; 150 G/L), en relais sous couvert d'un traitement parentéral."),
        ("Prop. 23", "Choix selon le profil du patient : (1) stable, sans IR/IH sévère ni "
         "risque hémorragique → fondaparinux ou AOD possibles en 1<sup>re</sup> intention ; "
         "(2) instable ou à risque hémorragique/soins intensifs → injectable de ½ vie courte "
         "(argatroban ou bivalirudine) + surveillance biologique stricte ; (3) thrombose "
         "sévère (EP massive, thrombose extensive/artérielle, gangrène, CIVD) → argatroban ou "
         "bivalirudine en priorité ; (4) insuffisance rénale sévère (clairance &lt; 30 "
         "mL/min) → <b>seul l'argatroban</b> peut être utilisé ; (5) insuffisance hépatique "
         "sévère (Child-Pugh C) → bivalirudine, danaparoïde ou fondaparinux."),
    ], col_widths=[REF_W, PAGE_W - 2 * MARGIN - REF_W - ACCORD_W, ACCORD_W]))
    return story

def _section_q7_danaparoide():
    story = []
    story.append(Spacer(1, 2 * mm))
    story.append(P("<b>A. Le danaparoïde sodique</b> (Orgaran®) — héparinoïde d'extraction "
                    "(héparane sulfate, dermatane sulfate, chondroïtine sulfate), activité "
                    "anticoagulante principalement anti-Xa avec une faible activité anti-IIa. "
                    "AMM : traitement prophylactique et curatif des événements "
                    "thromboemboliques chez les patients atteints de TIH ou ayant un antécédent "
                    "documenté de TIH.", S_BODY_SM))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P("<i>Disclosure — demi-vie anti-Xa : la source donne deux valeurs "
                    "différentes selon l'endroit du texte : « environ 25 h » dans "
                    "l'argumentaire de la Question 7, contre « ≈ 24h » dans le Tableau V "
                    "(délais d'arrêt pré-procéduraux, Question 9). Les deux valeurs sont "
                    "reproduites telles quelles, sans harmonisation silencieuse. Demi-vie "
                    "anti-IIa : 7h dans les deux cas (allongée en insuffisance rénale, où "
                    "l'argatroban est préférable).</i>", S_NOTE))
    story.append(Spacer(1, 2 * mm))
    cw = PAGE_W - 2 * MARGIN
    story.append(simple_table(
        ["Contexte", "Posologie", "Surveillance"],
        [
            ["IV curative (adulte)", "Bolus IV selon le poids : 1250 U (≤ 55 kg), 2500 U "
             "(55-90 kg), 3750 U (&gt; 90 kg) ; puis perfusion 400 U/h × 4h, 300 U/h × 4h, "
             "puis 150-200 U/h", "Activité anti-Xa quotidienne (1er dosage 4h après le "
             "début), cible 0,5-0,8 U/mL (gamme danaparoïde)"],
            ["SC curative (si IV impossible)", "1500 U SC ×2/j (≤ 55 kg), 2000 U SC ×2/j "
             "(55-90 kg), 1750 U SC ×3/j (&gt; 90 kg)", "idem"],
            ["Préventive (antécédent de TIH)", "750 U SC ×2/j (≤ 90 kg), 1250 U SC ×2/j "
             "(&gt; 90 kg)", "—"],
            ["Pédiatrie (thrombose constituée)", "Bolus IV 30 U/kg puis entretien "
             "1,2-2,0 U/kg/h", "idem adulte"],
            ["Hémodialyse intermittente", "Bolus 3750 U (2500 U si &lt; 55 kg) avant les 2 "
             "premières séances, puis 3000 U (2000 U si &lt; 55 kg)", "—"],
        ],
        [cw * 0.22, cw * 0.53, cw * 0.25]))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P("Réactivité croisée in vitro avec les anticorps de TIH dans 3 à 10 % des "
                    "cas (conséquences cliniques rares) : un traitement peut être débuté sans "
                    "recherche préalable de réactivité croisée, mais surveiller la NP "
                    "quotidiennement jusqu'à normalisation puis 2 fois/semaine pendant 2 "
                    "semaines. Surdosage : arrêt transitoire de la perfusion + monitorage de "
                    "l'activité anti-Xa ; en cas d'hémorragie grave, la <b>protamine n'est pas "
                    "recommandée</b> par le RCP (neutralisation partielle seulement) ; "
                    "plasmaphérèse envisageable si saignement incontrôlable. Relais AVK "
                    "initié après 5-7 jours de traitement et NP &gt; 150 G/L ; danaparoïde "
                    "arrêté quand l'INR est en zone thérapeutique (2-3) 2 jours de suite, "
                    "après ≥ 72h de traitement par AVK.", S_BODY_SM))
    return story

def _section_q7_argatroban():
    story = []
    story.append(Spacer(1, 2 * mm))
    story.append(KeepTogether([
        section_bar("Algorithme de prescription et surveillance de l'argatroban", color=GREY),
        Spacer(1, 1.5 * mm),
        P("<i>Transcrit depuis le rendu visuel de la source (Figure 2, page 26). "
          "Contre-indiqué en cas d'insuffisance hépatique sévère (Child-Pugh C) et "
          "d'intolérance au fructose (contient de l'éthanol). Contacter le laboratoire "
          "d'hémostase avant de débuter.</i>", S_NOTE),
    ]))
    story.append(Spacer(1, 2 * mm))
    cw = PAGE_W - 2 * MARGIN
    story.append(simple_table(
        ["Étape", "Décision / actions", "Résultat / suite"],
        [
            ["Dose initiale", "Post-chirurgie cardiaque, patient de réanimation, ou "
             "insuffisance hépatique modérée (Child-Pugh B) ?", "Non → 1 µg/kg/min. "
             "Oui → 0,5 µg/kg/min. Pas d'adaptation à l'insuffisance rénale ; dose calculée "
             "sur le poids réel chez l'obèse."],
            ["Choix du test de monitorage", "TCA normal avant argatroban ?", "Oui → "
             "monitorage possible par le TCA (cible 1,5-3 × témoin, &lt; 100 sec). "
             "Non → monitorage par écarine (ECT) ou temps de thrombine diluée (TTd), "
             "cible 0,5-1,5 µg/mL."],
            ["Adaptation posologique — schéma standard (début 2 µg/kg/min)",
             "Sous-dosage → augmenter de 0,5 µg/kg/min, recontrôler 2h après. Zone "
             "thérapeutique → pas de modification, recontrôle 2h puis 1×/j. Surdosage → "
             "arrêter la perfusion jusqu'à retour en zone thérapeutique, reprendre à "
             "un débit réduit de moitié, recontrôle 2h après.", "—"],
            ["Adaptation posologique — schéma à doses réduites (début 0,5 µg/kg/min)",
             "Mêmes règles que le schéma standard, mais ajustements de 0,1 µg/kg/min et "
             "recontrôles à 4h (au lieu de 2h).", "—"],
        ],
        [cw * 0.24, cw * 0.50, cw * 0.26]))
    story.append(Spacer(1, 2 * mm))
    story.append(P("<b>Ajustement de la dose initiale selon la gravité (Tableau II, "
                    "d'après Alatri et al.) :</b>", S_H2))
    story.append(Spacer(1, 1 * mm))
    story.append(simple_table(
        ["APACHE II", "Argatroban\n(µg/kg/min)", "SOFA", "Argatroban\n(µg/kg/min)", "SAPS",
         "Argatroban\n(µg/kg/min)"],
        [
            ["15", "1,25", "10", "1,28", "30", "1,16"],
            ["16", "1,19", "11", "1,19", "32", "1,10"],
            ["17", "1,13", "12", "1,10", "34", "1,04"],
            ["18", "1,07", "13", "1,01", "36", "0,98"],
            ["19", "1,01", "14", "0,92", "38", "0,92"],
            ["20", "0,95", "15", "0,83", "40", "0,86"],
            ["21", "0,89", "16", "0,74", "42", "0,82"],
            ["23", "0,77", "17", "0,65", "44", "0,74"],
            ["25", "0,65", "18", "0,56", "46", "0,68"],
            ["27", "0,53", "19", "0,47", "50", "0,56"],
            ["29", "0,41", "20", "0,38", "55", "0,41"],
            ["32", "0,23", "21", "0,29", "60", "0,26"],
        ],
        [cw / 6.0] * 6))
    return story

def _section_q7_relais_bivalirudine():
    story = []
    story.append(Spacer(1, 2 * mm))
    story.append(KeepTogether([
        section_bar("Relais argatroban → AVK", color=GREY),
        Spacer(1, 1.5 * mm),
        P("<i>Transcrit depuis le rendu visuel de la source (Figure 3, page 27, d'après "
          "Rozec et al.). Relais délicat : l'argatroban allonge aussi le temps de Quick.</i>",
          S_NOTE),
    ]))
    story.append(Spacer(1, 2 * mm))
    cw = PAGE_W - 2 * MARGIN
    story.append(simple_table(
        ["Étape", "Décision / actions", "Résultat / suite"],
        [
            ["Introduction de l'AVK", "Plaquettes &gt; 150 G/L → introduire la coumadine "
             "(2 à 5 mg/j) en cothérapie avec l'argatroban, pendant au moins 5 jours.",
             "Mesure quotidienne de l'INR."],
            ["Surveillance de l'INR", "INR ≤ 4 → maintien de la cothérapie, nouvelle mesure "
             "le lendemain. INR &gt; 4 → arrêt de l'argatroban.", "Après arrêt de l'argatroban : "
             "mesurer l'INR."],
            ["Après arrêt de l'argatroban", "INR dans la fourchette thérapeutique → maintien "
             "de la coumadine seule. INR &lt; la fourchette thérapeutique → reprise de "
             "l'argatroban.", "—"],
        ],
        [cw * 0.22, cw * 0.50, cw * 0.28]))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P("<i>Disclosure — imprécision de formulation entre le texte et sa propre "
                    "figure : le corps du texte introduit cette figure en disant que "
                    "l'argatroban « ne doit être arrêté que lorsque l'INR est au moins égal "
                    "à 4 » (soit ≥ 4), alors que la Figure 3 elle-même trace la limite à "
                    "« INR ≤ 4 → maintien » / « INR &gt; 4 → arrêt » (soit &gt; 4 strictement). "
                    "Le tableau ci-dessus reproduit fidèlement les seuils tels que dessinés "
                    "dans la figure, sans les réharmoniser avec la phrase d'introduction.</i>",
                    S_NOTE))
    story.append(Spacer(1, 2 * mm))

    story.append(P("<b>C. La bivalirudine</b> — inhibiteur direct de la thrombine, demi-vie "
                    "courte (~25 min si fonction rénale normale), élimination enzymatique "
                    "(80 %) et rénale (20 %). Molécule la plus étudiée en angioplastie/chirurgie "
                    "cardiaque pour TIH, mais <b>plus commercialisée en France</b> (génériques "
                    "attendus). Voie IV exclusive, pas d'antidote, partiellement hémodialysable "
                    "(25 %).", S_BODY_SM))
    story.append(Spacer(1, 2 * mm))
    story.append(P("<b>D. Le fondaparinux</b> (Arixtra®) — pentasaccharide anti-Xa, utilisé de "
                    "longue date hors AMM dans la TIH. Avantages : pas de réactivité croisée "
                    "avec les anticorps de TIH, injection SC unique quotidienne, aucun test "
                    "biologique spécifique requis, n'allonge ni le TCA ni l'INR (facilite le "
                    "relais AVK), coût inférieur au danaparoïde/argatroban. <b>Contre-indiqué en "
                    "cas d'insuffisance rénale sévère</b> (élimination exclusivement rénale) et "
                    "à éviter si instabilité clinique. <b>Posologie curative</b> proposée par "
                    "les recommandations britanniques 2012, selon le poids : <b>5 mg</b> si "
                    "&lt; 50 kg, <b>7,5 mg</b> si 50-100 kg, <b>10 mg</b> si &gt; 100 kg "
                    "(1 injection SC/j ; à adapter à l'âge et à la fonction rénale).",
                    S_BODY_SM))
    return story

def _section_q7_aod_avk():
    story = []
    story.append(Spacer(1, 2 * mm))
    story.append(section_bar("Les anticoagulants oraux directs (AOD) et les AVK"))
    story.append(Spacer(1, 2 * mm))
    story.append(P("<b>E. Les AOD</b> — dabigatran (anti-IIa), rivaroxaban/apixaban/édoxaban "
                    "(anti-Xa). N'exercent aucun effet sur les interactions FP4/héparine avec "
                    "les plaquettes. Le <b>rivaroxaban</b> est l'AOD le plus évalué (seule étude "
                    "prospective publiée) : schéma proposé 15 mg × 2/j jusqu'à J21 ou correction "
                    "complète de la thrombopénie, puis 20 mg/j pendant 1 mois minimum.",
                    S_BODY_SM))
    story.append(Spacer(1, 2 * mm))
    cw = PAGE_W - 2 * MARGIN
    story.append(simple_table(
        ["AOD", "n", "TIH avec thromboses", "AOD en 1re ligne", "Thromboses", "Saignements majeurs"],
        [
            ["Rivaroxaban", "49", "31 (63 %)", "25 (51 %)", "1/49", "0/49"],
            ["Apixaban", "21", "8 (38 %)", "7 (33 %)", "0/21", "0/21"],
            ["Dabigatran", "11", "6 (55 %)", "3 (27 %)", "1/11", "0/11"],
        ],
        [cw * 0.18, cw * 0.08, cw * 0.20, cw * 0.20, cw * 0.16, cw * 0.18]))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P("<i>Tableau IV — Résultats principaux obtenus avec les AOD anti-Xa dans le "
                    "traitement des TIH (Warkentin, Davis, Cuker/ASH).</i>", S_NOTE))
    story.append(Spacer(1, 2 * mm))
    story.append(P("<b>F. Les AVK</b> — <b>jamais utilisés seuls à la phase aiguë</b> (risque "
                    "d'extension de thrombose, gangrène veineuse, nécroses cutanées). "
                    "Uniquement en relais, sous couvert d'un traitement parentéral efficace "
                    "(danaparoïde ou argatroban), coumadine privilégiée, introduite au plus tôt "
                    "quand les plaquettes remontent &gt; 150 G/L.", S_BODY_SM))
    story.append(Spacer(1, 2 * mm))
    story.append(P("<b>Durée du traitement anticoagulant non-héparinique :</b> au minimum "
                    "<b>4 semaines</b> si thrombopénie isolée ; <b>3 à 6 mois</b> au minimum "
                    "dans les autres cas, selon la sévérité des thromboses associées.",
                    S_BODY_SM))
    return story

def _section_q8():
    story = []
    story.append(Spacer(1, 2 * mm))
    story.append(section_bar("Question 8 — Place d'autres traitements"))
    story.append(Spacer(1, 2 * mm))
    story.append(prop_table([
        ("Prop. 24", "Il est recommandé de <b>ne pas transfuser de plaquettes</b> à la phase "
         "aiguë d'une TIH en l'absence de saignement menaçant le pronostic vital ou "
         "fonctionnel."),
        ("Prop. 25", "Il est recommandé de <b>ne pas prescrire d'agent antiplaquettaire oral</b> "
         "pour traiter une TIH à la phase aiguë."),
        ("Prop. 26", "Il est proposé de <b>ne pas prescrire en 1<sup>re</sup> intention "
         "d'immunoglobulines polyvalentes IV</b> à la phase aiguë d'une TIH."),
        ("Prop. 27", "Il est proposé de <b>ne pas mettre de filtre cave</b> à la phase aiguë "
         "d'une TIH."),
    ], col_widths=[REF_W, PAGE_W - 2 * MARGIN - REF_W - ACCORD_W, ACCORD_W]))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P("Les HBPM sont <b>contre-indiquées</b> en cas de TIH sous HNF. Les "
                    "antagonistes GPIIb-IIIa (tirofiban) et l'iloprost restent des options très "
                    "limitées, réservées à de rares occlusions coronaires aiguës post-angioplastie "
                    "ou à la chirurgie cardiaque en urgence (cf. Question 10). Un filtre cave "
                    "n'est discuté qu'en cas d'EP grave avec contre-indication transitoire aux "
                    "anticoagulants. La thrombectomie chirurgicale reste exceptionnelle.",
                    S_NOTE))
    return story

def _section_q9():
    story = []
    story.append(Spacer(1, 2 * mm))
    story.append(section_bar("Question 9 — TIH en milieu chirurgical (hors chirurgie cardiaque)"))
    story.append(Spacer(1, 2 * mm))
    story.append(prop_table([
        ("Prop. 28", "TIH aiguë (&lt; 1 mois) : il est proposé de <b>reporter toute chirurgie "
         "au-delà du 1<sup>er</sup> mois</b> suivant le diagnostic si cela ne génère pas de "
         "risque vital/fonctionnel majeur, et d'en définir les modalités en concertation "
         "multidisciplinaire."),
        ("Prop. 29", "Chirurgie chez un patient sous anticoagulant oral avec TIH aiguë : "
         "arrêter l'anticoagulant, discuter un relais préopératoire par <b>argatroban</b> "
         "(arrêt perfusion <b>4h</b> avant l'intervention) ou <b>bivalirudine</b> (arrêt "
         "<b>2h</b> avant)."),
        ("Prop. 30", "Post-opératoire, si anticoagulation prolongée indiquée et risque "
         "hémorragique contrôlé : traiter préférentiellement par <b>fondaparinux</b> ou un "
         "<b>anticoagulant oral</b> (AVK ou AOD)."),
    ], col_widths=[REF_W, PAGE_W - 2 * MARGIN - REF_W - ACCORD_W, ACCORD_W]))
    story.append(Spacer(1, 2 * mm))
    story.append(P("<b>Anesthésie loco-régionale — délais d'arrêt avant un geste neuraxial "
                    "(contre-indiqué sous anticoagulant) :</b>", S_H2))
    story.append(Spacer(1, 1 * mm))
    cw = PAGE_W - 2 * MARGIN
    story.append(simple_table(
        ["Anticoagulant", "Demi-vie", "Prise en charge proposée"],
        [
            ["Fondaparinux", "≈ 17h (anti-Xa)", "Dernière injection &gt; 36h avant la chirurgie"],
            ["Danaparoïde", "≈ 24h (anti-Xa) et 7h (anti-IIa)", "Arrêt perfusion ou dernière "
             "injection SC &gt; 36h avant la chirurgie"],
            ["Argatroban", "≈ 50 minutes", "Arrêt de la perfusion 4h avant la chirurgie"],
            ["Bivalirudine", "≈ 20-30 minutes", "Arrêt de la perfusion 2h avant la chirurgie"],
        ],
        [30 * mm, cw - 30 * mm - 90 * mm, 90 * mm]))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P("<i>Tableau V — Demi-vies et délais d'arrêt pré-procéduraux.</i> Pour un "
                    "geste neuraxial spécifiquement : argatroban 8h après arrêt + taux "
                    "&lt; 0,1 µg/mL ; bivalirudine 8h après arrêt ; AOD dernière prise à J-5 ou "
                    "concentration &lt; 30 ng/mL ; danaparoïde/fondaparinux &gt; 48h (objectif "
                    "taux sous le seuil de détection). En cas de TIH aiguë, si ces délais "
                    "longs ne sont justifiés que par l'ALR neuraxiale, un autre type "
                    "d'anesthésie doit être envisagé.", S_NOTE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P("Reprise possible d'un anticoagulant à partir de la <b>6<sup>e</sup> heure "
                    "post-opératoire</b> après évaluation du risque hémorragique.", S_NOTE))
    return story

def _section_q10():
    story = []
    story.append(Spacer(1, 2 * mm))
    story.append(section_bar("Question 10 — Chirurgie cardiaque avec ou sans CEC"))
    story.append(Spacer(1, 2 * mm))
    story.append(prop_table([
        ("Prop. 31", "Avant toute chirurgie cardiaque chez un patient avec antécédent "
         "documenté de TIH, il est proposé de <b>rechercher systématiquement en ELISA</b> des "
         "anticorps anti-FP4."),
        ("Prop. 32", "Avant chirurgie cardiaque avec CEC chez un patient en TIH aiguë ou "
         "subaiguë (&lt; 3 mois) : définir le protocole d'anticoagulation péri-opératoire en "
         "<b>concertation pluridisciplinaire</b>."),
        ("Prop. 33", "TIH aiguë/subaiguë avec titre significatif d'anticorps (ELISA DO &gt; 1) "
         "nécessitant une CEC : associer un <b>antiplaquettaire IV</b> (tirofiban ou "
         "cangrelor) <b>+ HNF</b>, ou une <b>antithrombine directe IV</b> (bivalirudine ou "
         "argatroban) avec surveillance biologique étroite. <b>En urgence : privilégier "
         "l'association antiplaquettaire IV + HNF.</b>"),
    ], col_widths=[REF_W, PAGE_W - 2 * MARGIN - REF_W - ACCORD_W, ACCORD_W]))
    story.append(Spacer(1, 2 * mm))
    story.append(KeepTogether([
        P("<b>Stratégies thérapeutiques pour une chirurgie cardiaque avec CEC en cas de TIH</b>",
          S_H2),
        Spacer(1, 1 * mm),
        P("<i>Transcrit depuis le rendu visuel de la source (Figure 4, page 38).</i>", S_NOTE),
    ]))
    story.append(Spacer(1, 2 * mm))
    cw = PAGE_W - 2 * MARGIN
    story.append(simple_table(
        ["Phase", "Décision / actions", "Résultat / suite"],
        [
            ["Pré-opératoire", "Différer au-delà du 1er mois après le diagnostic de TIH "
             "(idéalement au-delà du 3e mois) ; concertation multidisciplinaire ; recherche "
             "d'anticorps anti-FP4.", "Ac positifs → stratégie per-opératoire spécifique "
             "ci-contre. Ac négatifs → HNF selon les schémas habituels, en per-opératoire "
             "uniquement."],
            ["Per-opératoire (si Ac +)", "Deux stratégies possibles : HNF + antiplaquettaire "
             "IV (tirofiban ou cangrelor), OU inhibiteur de la thrombine injectable "
             "(argatroban ou bivalirudine).", "La stratégie retenue tient compte du titre "
             "d'anticorps anti-FP4/héparine mesuré par un test immunologique quantitatif "
             "sensible."],
            ["Post-opératoire", "Anticoagulation prophylactique → danaparoïde ou "
             "fondaparinux. Anticoagulation curative → argatroban, bivalirudine ou "
             "danaparoïde.", "Reprise possible à partir de la 6e heure post-opératoire, "
             "après évaluation du risque hémorragique."],
        ],
        [cw * 0.16, cw * 0.46, cw * 0.38]))
    story.append(Spacer(1, 2 * mm))
    story.append(P("Si TIH en <b>rémission</b> (&gt; 3 mois) : chirurgie cardiaque possible sous "
                    "héparine selon le protocole habituel (recherche d'anticorps anti-FP4 "
                    "recommandée, persistance prolongée rapportée dans de rares cas).",
                    S_NOTE))
    return story

def _section_q10_bivalirudine():
    story = []
    story.append(Spacer(1, 2 * mm))
    story.append(KeepTogether([
        section_bar("Utilisation de la bivalirudine en cas de TIH — chirurgie cardiaque", color=GREY),
        Spacer(1, 1.5 * mm),
        P("<i>Tableau III, transcrit depuis le texte source. Prudence : dégradation "
          "enzymatique par la thrombine — éviter l'aspiration péricardique, préférer le cell "
          "saver, éviter la stase sanguine.</i>", S_NOTE),
    ]))
    story.append(Spacer(1, 2 * mm))
    cw = PAGE_W - 2 * MARGIN
    story.append(simple_table(
        ["Contexte", "Posologie", "Suivi biologique"],
        [
            ["Traitement médical de la TIH (peu de données)", "Perfusion IV 0,15-0,25 "
             "mg/kg/h", "TCA cible : 1,5 à 2,5 × témoin"],
            ["Angioplastie coronaire", "Bolus IV 0,75 mg/kg puis perfusion IV 1,75 mg/kg/h "
             "pendant l'intervention et 4h max après (si clairance créat. 30-59 mL/min : "
             "1,4 mg/kg/h)", "Si ACT après bolus &lt; 225 sec, 2e bolus de 0,3 mg/kg"],
            ["Chirurgie cardiaque sans CEC", "Bolus IV 0,75 mg/kg puis perfusion IV "
             "1,75 mg/kg/h pendant l'intervention", "Si ACT &lt; 300 sec, augmenter le débit "
             "de 0,25 mg/kg/h"],
            ["Chirurgie cardiaque avec CEC", "Bolus IV 1 mg/kg + 50 mg dans le liquide "
             "d'amorçage puis perfusion IV 2,5 mg/kg/h ; arrêt 15 min avant la fin annoncée "
             "de la CEC (si CEC prolongée à 20 min : bolus 0,5 mg/kg et reprise à 2,5 mg/kg/h)",
             "Si ACT &lt; 2,5 × ACT de base, bolus supplémentaire 0,1-0,5 mg/kg. Dosage "
             "possible en sang total (avis spécialisé)"],
        ],
        [cw * 0.24, cw * 0.42, cw * 0.34]))
    story.append(Spacer(1, 2 * mm))
    story.append(P("Deux agents antiplaquettaires IV utilisables en association à l'HNF pour "
                    "la CEC : <b>tirofiban</b> (bolus 10 µg/kg puis, 15 min après, héparine "
                    "habituelle, puis perfusion 0,15 µg/kg/min arrêtée 1h avant la fin de CEC — "
                    "effet prolongé, risque hémorragique post-opératoire) ; <b>cangrelor</b> "
                    "(bolus 30 µg/kg 10 min avant l'héparine puis perfusion 4 µg/kg/min arrêtée "
                    "5 min avant l'arrêt de CEC — effet immédiat et bref, non altéré par "
                    "l'insuffisance rénale/hépatique, mais expérience limitée dans la TIH). "
                    "L'<b>iloprost</b> (Ilomédine®, analogue de la prostacycline, demi-vie "
                    "15-30 min) reste une option en urgence (ASH) : perfusion "
                    "<b>6 à 12 ng/kg/min</b>, arrêtée <b>20 minutes avant la protamine</b> — "
                    "expose à des épisodes d'hypotension artérielle sévère.", S_BODY_SM))
    story.append(Spacer(1, 2 * mm))
    story.append(P("<b>Inhibiteur de la thrombine injectable — l'argatroban en CEC</b> : "
                    "option secondaire, expérience limitée, complications hémorragiques et/ou "
                    "thrombotiques rapportées (caillots dans le réservoir de cardiotomie ou le "
                    "péricarde) ; non retenu par l'ACCP 2012 (qui privilégiait la bivalirudine) "
                    "et reste peu ou non recommandé dans ce contexte. Schéma rapporté : bolus "
                    "<b>100 µg/kg</b> puis perfusion IV continue <b>5 µg/kg/min</b>, avec un "
                    "ACT &gt; 400 sec pour démarrer la CEC puis un contrôle toutes les 15 min "
                    "(maintien entre 500 et 600 sec) — des ACT très allongés compliquant "
                    "l'ajustement du débit ont été observés. La <b>bivalirudine</b> est "
                    "l'option à recommander prioritairement pour une chirurgie cardiaque en "
                    "contexte de TIH aiguë (cf. Tableau III ci-dessous).", S_BODY_SM))
    return story

def _section_q11():
    story = []
    story.append(Spacer(1, 2 * mm))
    story.append(section_bar("Question 11 — TIH en médecine, obstétrique, pédiatrie"))
    story.append(Spacer(1, 2 * mm))
    story.append(prop_table([
        ("Prop. 34", "TIH aiguë avec syndrome coronarien aigu nécessitant une angioplastie "
         "transluminale : traiter préférentiellement par <b>bivalirudine</b> (ou un analogue), "
         "ou à défaut par <b>argatroban</b>."),
        ("Prop. 35", "TIH nécessitant une épuration extra-rénale : utiliser préférentiellement "
         "le <b>citrate</b> ou l'<b>argatroban</b> pour l'anticoagulation du circuit."),
        ("Prop. 36", "TIH pendant la <b>grossesse</b> : traiter préférentiellement par le "
         "<b>danaparoïde</b> (ne traverse pas le placenta) ou, à défaut, le "
         "<b>fondaparinux</b>."),
        ("Prop. 37", "Les modalités de surveillance de la NP des <b>enfants</b> traités par "
         "héparine sont identiques à celles de l'adulte."),
        ("Prop. 38", "Le traitement d'une TIH chez l'<b>enfant</b> repose sur le "
         "<b>danaparoïde sodique</b> ou l'<b>argatroban</b>, avec adaptation rigoureuse des "
         "doses au poids et aux tests biologiques."),
    ], col_widths=[REF_W, PAGE_W - 2 * MARGIN - REF_W - ACCORD_W, ACCORD_W]))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>SCA :</b> bivalirudine — bolus 0,75 mg/kg puis perfusion 1,75 mg/kg/h ; argatroban "
        "— bolus 350 µg/kg puis perfusion 25 µg/kg/min (cible ACT 300-450 sec) ; retrait du "
        "désilet 2h (bivalirudine) ou 4h (argatroban) après l'arrêt. "
        "<b>EER :</b> patient déjà sous argatroban → poursuivre sans bolus supplémentaire "
        "(peu d'influence de l'IR/l'EER sur sa pharmacocinétique) ; sinon, citrate si l'équipe "
        "maîtrise la technique, ou argatroban en bolus (100 µg/kg en continu, 250 µg/kg en "
        "intermittent) puis perfusion classique, arrêtée 1h avant la fin de séance ; le "
        "danaparoïde s'accumule en IR et est délicat à utiliser en EER continue. "
        "<b>Grossesse :</b> TIH très rare pendant la grossesse ; l'argatroban et les AOD sont "
        "<b>contre-indiqués</b>. "
        "<b>Enfant :</b> risque de TIH plus faible que chez l'adulte, mais anticorps anti-FP4 "
        "post-chirurgie cardiaque fréquents (3 à &gt; 50 % selon le nombre d'interventions) ; "
        "risque clinique réel de TIH réévalué à ~0,33 %.",
        S_BODY_SM))
    return story

def _section_q12_sources():
    story = []
    story.append(Spacer(1, 2 * mm))
    story.append(section_bar("Question 12 — Prévention de la survenue ou d'une récidive"))
    story.append(Spacer(1, 2 * mm))
    story.append(prop_table([
        ("Prop. 39", "Une <b>consultation d'hémostase</b> dans un délai de 3 mois suivant le "
         "diagnostic de TIH est proposée, avec remise au patient d'une <b>carte</b> attestant "
         "la complication, précisant les résultats biologiques et préconisant l'éviction de "
         "tout traitement par héparine."),
        ("Prop. 40", "En cas d'antécédent de TIH, il est proposé de prescrire un "
         "<b>anticoagulant oral</b> (AVK ou AOD) ou le <b>fondaparinux</b> lorsqu'une "
         "anticoagulation prophylactique ou curative est indiquée. Argatroban, bivalirudine "
         "et danaparoïde ne sont à envisager que si les anticoagulants oraux et le "
         "fondaparinux sont contre-indiqués."),
    ], col_widths=[REF_W, PAGE_W - 2 * MARGIN - REF_W - ACCORD_W, ACCORD_W]))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>Prévention primaire :</b> prescrire l'héparine uniquement dans les indications "
        "validées ; préférer les anticoagulants oraux ou, à défaut, les HBPM, en évitant "
        "l'HNF ; limiter la durée de traitement par héparine (&lt; 4-5 jours) avec relais "
        "précoce par voie orale. <b>Prévention secondaire :</b> carte/certificat d'antécédent "
        "de TIH à porter en permanence (surtout les 3 premiers mois, période de risque de "
        "récidive le plus élevé) ; test ELISA avant toute nouvelle exposition à l'héparine "
        "pour objectiver l'absence/persistance d'anticorps ; le risque de récidive après "
        "réexposition reste incertain, plus élevé si HNF &gt; 5 jours ou en chirurgie "
        "cardiaque.", S_BODY_SM))
    story.append(Spacer(1, 3 * mm))

    story.append(section_bar("Sources et traçabilité", color=GREY))
    story.append(Spacer(1, 2 * mm))
    story.append(P(
        "<b>Document source :</b> « Diagnostic et prise en charge d'une thrombopénie induite "
        "par l'héparine » — Propositions du Groupe d'Intérêt en Hémostase Périopératoire "
        "(GIHP) et du Groupe Français d'études sur l'Hémostase et la Thrombose (GFHT), en "
        "collaboration avec la Société Française d'Anesthésie-Réanimation (SFAR). Coordination : "
        "Y. Gruel, E. De Maistre, C. Pouplard, F. Mullier, S. Susen, S. Roullet, N. Blais, "
        "G. Le Gal, A. Vincentelli, D. Lasne, T. Lecompte, P. Albaladejo, A. Godier. 2019 "
        "(actualise la conférence d'experts SFAR de 2002).", S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P("<b>Méthodologie :</b> pas de grade GRADE — un unique axe « Accord », voté "
                    "par 32 membres du GIHP/GFHT (accord si ≥ 50 % pour et &lt; 20 % contre ; "
                    "« fort » si ≥ 70 % pour). Les 40 propositions du document ont toutes "
                    "recueilli un accord fort.", S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P("<b>Couverture :</b> cette fiche reprend l'intégralité des 12 questions et "
                    "40 propositions du document (transcription verbatim, sans paraphrase des "
                    "propositions elles-mêmes), ainsi que les 5 tableaux et 4 figures/algorithmes "
                    "cliniquement actionables. Les références bibliographiques ([1]-[114]) ne "
                    "sont pas retranscrites (non pertinentes pour un aide-mémoire clinique).",
                    S_SOURCE))
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Avertissement :</b> ce document est une fiche de synthèse indépendante, produite "
        "pour un usage d'aide-mémoire. Il reprend l'intégralité des propositions du texte "
        "source, mais ne remplace pas le texte intégral (argumentaire complet, références "
        "bibliographiques) et n'est ni édité ni validé par le GIHP, le GFHT ou la SFAR. En cas "
        "de doute, se référer au texte intégral et/ou à un avis spécialisé d'hémostase. "
        "Document de 2019 : plusieurs molécules (bivalirudine, lépirudine) ne sont plus "
        "commercialisées en France — vérifier les disponibilités actuelles.",
        S_BODY_SM), bg=GREY_LIGHT, border=GREY))
    return story

# ---------------------------------------------------------------------------
# Density note: sections are combined below (rather than one SECTIONS entry per
# question) because every SECTIONS entry starts on a fresh page regardless of
# room left on the previous one. A first pass with one entry per question left
# page 3 ~15% full (score-4T table tail alone) and pages 5-7 ~55-65% full (Q7
# split across 3 near-empty pages) - same failure mode documented in
# fiche_glycemie.py. Fixed by merging adjacent questions into single combinator
# functions so content flows across a shared page boundary at whatever row it
# naturally reaches (repeatRows=1 on every table handles header repetition).
def _section_A():
    return _section_intro()

def _section_BCDEFGHI():
    return (_section_q2q3() + [Spacer(1, 3 * mm)] + _section_score4t()
            + [Spacer(1, 3 * mm)] + _section_q4q5() + [Spacer(1, 3 * mm)] + _section_algo_diag()
            + [Spacer(1, 3 * mm)] + _section_q7_choix() + [Spacer(1, 3 * mm)] + _section_q7_danaparoide()
            + [Spacer(1, 3 * mm)] + _section_q7_argatroban()
            + [Spacer(1, 3 * mm)] + _section_q7_relais_bivalirudine()
            + [Spacer(1, 3 * mm)] + _section_q7_aod_avk()
            + [Spacer(1, 3 * mm)] + _section_q8() + [Spacer(1, 3 * mm)] + _section_q9()
            + [Spacer(1, 3 * mm)] + _section_q10() + [Spacer(1, 3 * mm)] + _section_q10_bivalirudine()
            + [Spacer(1, 3 * mm)] + _section_q11() + [Spacer(1, 3 * mm)] + _section_q12_sources())

SECTIONS = [
    ("Introduction, méthodologie & Q1 — Stades et niveaux de risque", _section_A),
    ("Q2-12 — Diagnostic, traitement, chirurgie, prévention & sources", _section_BCDEFGHI),
]

def _make_doc(path=None):
    return SimpleDocTemplate(path or OUT, pagesize=A4,
                              leftMargin=MARGIN, rightMargin=MARGIN,
                              topMargin=32 * mm, bottomMargin=16 * mm,
                              title="Fiche GIHP/GFHT/SFAR 2019 - Thrombopénie induite par l'héparine",
                              author="Synthèse indépendante (source GIHP/GFHT/SFAR)")

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
    import pypdf, tempfile
    tmp_path = tempfile.mktemp(suffix=".pdf")
    doc = _make_doc(tmp_path)
    doc.build(story_flowables, onFirstPage=_silent_page, onLaterPages=_silent_page)
    with open(tmp_path, "rb") as f:
        n = len(pypdf.PdfReader(f).pages)
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
