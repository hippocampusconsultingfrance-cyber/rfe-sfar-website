# -*- coding: utf-8 -*-
"""
Fiche de synthese - XXIe Conference de Consensus SRLF (avec la SFAR, la Societe de
Pneumologie de Langue Francaise et le Groupe Francophone de Reanimation et Urgences
Pediatriques) "Sevrage de la ventilation mecanique (a l'exclusion du nouveau-ne et du
reveil d'anesthesie)", Ecole Normale Superieure, Lyon, jeudi 11 octobre 2001. President
du jury : C. Richard (Le Kremlin-Bicetre). Texte publie dans Reanimation 2001;10:697-8.
Source : sources/sevrage_vm.pdf (12 pages, texte long), extrait en texte integral dans
sources/sevrage_vm.txt. Pas de tampon d'obsolescence sur la page 1 (verifiee visuellement
a 150dpi, cf. sources/sevrage_p1.png) - document non marque "abroge" dans
build/library_final.json.

CHAMP : defini explicitement des le titre - "a l'exclusion du nouveau-ne et du reveil
d'anesthesie" - disclosed tel quel dans le panneau d'introduction.

METHODOLOGIE - meme systeme a DEUX AXES INDEPENDANTS que fiche_civd.py (SRLF, meme
epoque) : une lettre de niveau de preuve de la reference (a/b/c/d) et, quand le jury l'a
juge possible, un chiffre de niveau de recommandation (1/2/3), imprimes entre crochets
attaches a chaque enonce, ex. "[c, 3]" ou "[b]" seul. DIFFERENCE IMPORTANTE PAR RAPPORT A
CIVD, verifiee par grep exhaustif du texte extrait (motif "\\[[^\\]]{1,8}\\]") : ce
document mele, dans les MEMES crochets, deux choses distinctes qui ne sont pas separables
de facon fiable par un simple pattern-matching - (a) les cotations preuve/force
(lettre +/- chiffre, ex. "[a, 1]", "[c, 3]", "[b]") et (b) de simples renvois
bibliographiques numerotes SANS lettre (ex. "[2]", "[3]" seuls - 32 occurrences sur 101
crochets totaux). Plutot que de deviner lesquels des crochets numeriques nus sont "en
realite" une cotation de niveau 2 ou 3 non accompagnee de sa lettre (ce que rien dans le
texte ne permet de trancher avec certitude), CHOIX EXPLICITE ET DISCLOSED ici : tous les
crochets sont reproduits verbatim en petit texte gris entre le texte narratif, SANS les
transformer en puce de couleur (grade_chip), afin de ne jamais fabriquer une cotation
preuve/force a partir d'un simple renvoi bibliographique. Voir avertissement dans le
panneau de methodologie.

FIGURE (page 11 source, organigramme "Procedure de sevrage") : pure organigramme
graphique (boites + fleches), PAS de texte extractible utilisable (page 11 ne contient
qu'une image scannee/vectorielle, verifie par get_images()) - reconstruite ici
integralement a partir d'un rendu visuel de la page a 150dpi (sources/sevrage_p11.png),
jamais devine. Page 12 (legende texte de la Figure 1) recuperee par extraction de texte
standard et reproduite verbatim sous l'organigramme.

Pas de tableau au sens strict dans cette source (uniquement de la prose structuree par
5 questions + une liste d'abreviations) - pas de theme_table/reco_table necessaire pour
un tableau de donnees ; reco_table est neanmoins reutilise ici pour presenter les listes
de criteres/facteurs de risque de facon scannable (colonnes Theme/Enonce), a l'identique
du principe de fiche_civd.py, MAIS avec une colonne unique "Citation(s)" (au lieu de deux
colonnes Preuve/Force separees) puisque les deux types de crochets ne sont pas separables
de facon fiable (voir plus haut) - texte du crochet reproduit tel quel, jamais decompose.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from style import *
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.units import mm

OUT = "/home/user/rfe-sfar-website/output/Fiche_SRLF_SFAR_Sevrage_VM_2001.pdf"

SOURCE_TXT = ("Source : XXIe Conférence de Consensus en Réanimation et Médecine d'Urgence de la Société "
              "de Réanimation de Langue Française (SRLF), avec la participation de la Société Française "
              "d'Anesthésie et de Réanimation (SFAR), de la Société de Pneumologie de Langue Française et "
              "du Groupe Francophone de Réanimation et Urgences Pédiatriques — « Sevrage de la ventilation "
              "mécanique (à l'exclusion du nouveau-né et du réveil d'anesthésie) », Ecole Normale "
              "Supérieure, Lyon, 11 octobre 2001. Président du jury : C. Richard. Fiche de synthèse non "
              "officielle : se référer au texte intégral.")

def P(txt, style=S_CELL):
    return Paragraph(txt, style)

def chip(label, **kw):
    return grade_chip(label, **kw)

S_CITE = pstyle("cite_sevrage", fontSize=7.6, leading=9.6, textColor=GREY, fontName=FONT_ITALIC)

def reco_table(rows, col_widths):
    """rows: (theme, text, citation_or_None) — une seule colonne de citation (texte du
    crochet reproduit verbatim, ex. "[c, 3]" ou "[2]"), jamais decompose en deux puces
    Preuve/Force separees car les crochets numeriques nus ne sont pas distinguables de
    facon fiable d'une cotation de niveau (voir docstring du module)."""
    data = [[P("Thème", S_HEAD_W), P("Énoncé", S_HEAD_W), P("Réf.", S_HEAD_W_C)]]
    for theme, txt, cite in rows:
        cite_cell = P(cite, S_CITE) if cite else P("—", S_CELL_C)
        data.append([P(theme, S_CELL_B), P(txt, S_CELL), cite_cell])
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

def algo_table():
    """Organigramme "Procédure de sevrage" (page 11 source) — reconstruit intégralement
    à partir du rendu visuel (sources/sevrage_p11.png), la page ne contenant aucun texte
    extractible (image pure). Flux vérifié visuellement : pré-requis -> épreuve de VS
    (pièce en T ou AI sans PEP, 30-120 min) -> recherche de signes de mauvaise tolérance
    -> deux branches paralleles (signes présents -> gaz du sang + reprise VM -> sevrage
    difficile ; signes absents -> recherche des critères d'extubation -> extubation) ->
    issues (sevrage difficile : >30j -> échec du sevrage, ou reprise du cycle "AI
    dégressive ou VS/VAC" en retour au pré-requis ; extubation : 48h -> sevrage réussi,
    ou ré-intubation/VNI -> sevrage difficile)."""
    cw = PAGE_W - 2 * MARGIN
    c0 = c1 = cw / 2.0
    S_A = pstyle("sev_a", fontSize=7.8, leading=9.8, textColor=INK, alignment=TA_CENTER)
    S_A_B = pstyle("sev_a_b", fontSize=8.6, leading=10.4, textColor=WHITE, fontName=FONT_BOLD, alignment=TA_CENTER)
    S_A_HEAD = pstyle("sev_a_head", fontSize=7.8, leading=9.8, textColor=INK, fontName=FONT_BOLD, alignment=TA_CENTER)

    def ac(txt, style=S_A):
        return Paragraph(txt, style)

    data = [
        [ac("PRÉ-REQUIS (recherche quotidienne, précoce, par protocole écrit — personnel "
            "infirmier et/ou kinésithérapeutes) : absence d'inotrope et de vasopresseur • "
            "absence de sédation • réponse cohérente aux ordres simples • FiO2 ≤ 50 % • "
            "PEP ≤ 5 cmH2O", S_A_B), ""],
        [ac("↓ ÉPREUVE DE VENTILATION SPONTANÉE (VS) — pièce en T ou aide inspiratoire "
            "(AI) sans PEP, 30 à 120 minutes", S_A_HEAD), ""],
        [ac("↓ Recherche de signes de mauvaise tolérance : FR &gt; 35/min • SpO2 &lt; 90 % "
            "• variation &gt; 20 % de FC ou PAS • sueurs, agitation, troubles de la "
            "vigilance", S_A), ""],
        [ac("Signes présents", S_A_HEAD), ac("Signes absents", S_A_HEAD)],
        [ac("Gaz du sang artériel et reprise de la VM", S_A), ac("Recherche des critères d'extubation", S_A)],
        [ac("↓ SEVRAGE DIFFICILE", S_A_B), ac("↓ EXTUBATION", S_A_B)],
        [ac("&gt; 30 jours <b>→ ÉCHEC DU SEVRAGE</b>. Sinon, reprise du cycle (AI "
            "dégressive ou VS/VAC) → retour au pré-requis.", S_A),
         ac("48 h <b>→ SEVRAGE RÉUSSI</b>. Si ré-intubation ou VNI dans les 48 h → retour "
            "à la case « sevrage difficile ».", S_A)],
    ]
    t = Table(data, colWidths=[c0, c1])
    style_cmds = [
        ("SPAN", (0, 0), (1, 0)), ("SPAN", (0, 1), (1, 1)), ("SPAN", (0, 2), (1, 2)),
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("BACKGROUND", (0, 1), (-1, 1), TEAL_DARK),
        ("BACKGROUND", (0, 2), (-1, 2), BG_PANEL),
        ("BACKGROUND", (0, 3), (-1, 4), WHITE),
        ("BACKGROUND", (0, 5), (-1, 5), TEAL_DARK),
        ("BACKGROUND", (0, 6), (0, 6), RED_LIGHT), ("BACKGROUND", (1, 6), (1, 6), GREEN_LIGHT),
        ("GRID", (0, 0), (-1, -1), 0.5, GREY_LIGHT),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("TOPPADDING", (0, 0), (-1, -1), 3.6), ("BOTTOMPADDING", (0, 0), (-1, -1), 3.6),
        ("LEFTPADDING", (0, 0), (-1, -1), 4), ("RIGHTPADDING", (0, 0), (-1, -1), 4),
    ]
    t.setStyle(TableStyle(style_cmds))
    return t

TOTAL_PAGES = {"n": 6}

def on_page(canvas, doc, page_title):
    header_band(canvas, doc, "SRLF / SFAR — CONFÉRENCE DE CONSENSUS 2001 — FICHE DE SYNTHÈSE",
                "Sevrage de la ventilation mécanique",
                page_title, icon_fn=lambda c, x, y: icon_shield(c, x, y, 13 * mm), color=TEAL_DARK)
    footer_band(canvas, doc, SOURCE_TXT, f"Page {doc.page} / {TOTAL_PAGES['n']}")

# ---------------------------------------------------------------------------
def _section_intro():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Champ :</b> sevrage de la ventilation mécanique (VM) chez l'adulte et "
        "l'enfant, <b>à l'exclusion du nouveau-né et du réveil d'anesthésie</b> "
        "(précision imprimée en couverture de la source, reprise ici sans l'omettre). "
        "XXIe Conférence de Consensus SRLF, avec la participation de la SFAR, de la "
        "Société de Pneumologie de Langue Française et du Groupe Francophone de "
        "Réanimation et Urgences Pédiatriques (GFRUP), Ecole Normale Supérieure, Lyon, "
        "11 octobre 2001.<br/><br/>"
        "<b>Définition retenue par le jury</b> pour le terme « sevrage » : la procédure "
        "en trois étapes (pré-requis à l'épreuve de ventilation spontanée [VS], l'épreuve "
        "de VS, puis une période de 48 heures) aboutissant à l'interruption de la VM "
        "pendant 48 heures ; ce sevrage réussi s'accompagne habituellement de "
        "l'extubation.<br/><br/>"
        "<b>Cinq questions</b> ont été posées au jury : (1) quand débuter le sevrage ? "
        "(2) peut-on prévoir un sevrage difficile ? (3) comment conduire le sevrage ? "
        "(4) particularités selon le terrain ? (5) que faire en cas d'échec du sevrage ?",
        S_BODY), bg=BG_PANEL, border=TEAL))
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("Méthodologie & convention de cette fiche"))
    story.append(Spacer(1, 2 * mm))
    story.append(P(
        "Système <b>Society of Critical Care Medicine Rating System</b> (1997), distinct "
        "de GRADE — <b>identique dans son principe à celui de la conférence CIVD (2002)</b> "
        "de ce même corpus : chaque énoncé peut porter une lettre de <b>niveau de preuve</b> "
        "de la référence (a = essais randomisés &gt; b = études non randomisées &gt; "
        "c = mises au point, revues, séries de cas &gt; d = opinions non revues par des "
        "pairs) et, quand le jury l'a jugé possible, un chiffre de <b>niveau de "
        "recommandation</b> (1 = preuves indiscutables &gt; 2 = preuves + consensus "
        "d'experts &gt; 3 = pas de preuves adéquates, opinion d'experts).",
        S_BODY_SM))
    story.append(Spacer(1, 2 * mm))
    story.append(info_panel(P(
        "<b>⚠ Particularité de ce document, disclosed :</b> le texte source mêle, dans les "
        "mêmes crochets, ces cotations preuve/force (ex. « [a, 1] », « [c, 3] », « [b] » "
        "seul) et de <b>simples renvois bibliographiques numérotés sans lettre</b> (ex. "
        "« [2] », « [3] » seuls — 32 occurrences sur 101 crochets au total, vérifié par "
        "extraction exhaustive du texte). Rien dans la source ne permet de déterminer avec "
        "certitude si un crochet numérique nu est un renvoi bibliographique ordinaire ou "
        "une cotation de niveau non accompagnée de sa lettre. <b>Choix retenu ici : tous "
        "les crochets sont reproduits tels quels, en petit texte gris, à la suite de "
        "l'énoncé concerné</b> — jamais convertis en puce de couleur (grade_chip) ni "
        "réinterprétés, pour ne fabriquer aucune cotation absente de la source.",
        S_BODY_SM), bg=AMBER_LIGHT, border=AMBER))
    story.append(Spacer(1, 2 * mm))
    story.append(P(
        "<b>Abréviations principales</b> utilisées dans cette fiche (liste de la source, "
        "abrégée) : <b>VM</b> = ventilation mécanique ; <b>VS</b> = ventilation spontanée ; "
        "<b>VNI</b> = ventilation non invasive ; <b>AI</b> = aide inspiratoire ; "
        "<b>VACI</b> = ventilation assistée contrôlée intermittente ; <b>PEP</b> = pression "
        "téléexpiratoire positive ; <b>FiO2</b> = fraction inspirée en oxygène ; "
        "<b>FR</b> = fréquence respiratoire ; <b>FR/VT (f/VT)</b> = fréquence respiratoire "
        "sur volume courant ; <b>BPCO</b> = bronchopneumopathie chronique obstructive ; "
        "<b>CV</b> = capacité vitale ; <b>Pimax/Pemax</b> = pressions statiques maximales "
        "inspiratoire/expiratoire.", S_NOTE))
    return story

def _section_q1():
    story = []
    story.append(Spacer(1, 2 * mm))
    story.append(section_bar("Question 1 — Quand débuter le sevrage de la VM ?"))
    story.append(Spacer(1, 2 * mm))
    story.append(P(
        "L'opportunité d'interrompre la VM doit être recherchée <b>dès son instauration</b>, "
        "indépendamment de la pathologie sous-jacente <i>[2]</i>. La procédure débute par la "
        "recherche du pré-requis à l'épreuve de VS, effectuée en règle générale par le "
        "personnel infirmier et/ou les kinésithérapeutes ; cette recherche doit être "
        "<b>précoce</b> <i>[c, 3]</i>, <b>quotidienne</b> <i>[c, 3]</i> et faire l'objet "
        "d'un <b>protocole écrit</b> <i>[a, 1]</i>.", S_BODY_SM))
    story.append(Spacer(1, 2 * mm))
    story.append(reco_table([
        ("Critères généraux", "Absence de vasopresseur et d'inotrope, absence de "
         "sédation, réponse cohérente aux ordres simples. Relèvent du bon sens clinique "
         "mais n'ont pas fait l'objet de travaux spécifiques.", "[c, 3]"),
        ("Critères respiratoires", "FiO2 ≤ 50 % et niveau de PEP ≤ 5 cmH2O. Le médecin "
         "peut s'affranchir d'un ou plusieurs de ces critères (généraux ou respiratoires) "
         "pour décider de l'épreuve de VS.", "[c, 3]"),
        ("Mécanique ventilatoire", "Les paramètres et indices dérivés (pressions, "
         "résistance, compliance, commande ventilatoire) ne sont pas suffisamment "
         "discriminants pour en recommander l'usage systématique. Le sevrage réussit dès "
         "la première tentative chez environ deux tiers des patients sélectionnés sur les "
         "critères ci-dessus ; le taux d'échec qui en découle est jugé acceptable au "
         "regard des risques d'une VM prolongée inutilement.", "[c, 3]"),
    ], [32 * mm, PAGE_W - 2 * MARGIN - 32 * mm - 18 * mm - 20 * mm, 18 * mm]))
    return story

def _section_q2():
    story = []
    story.append(Spacer(1, 2 * mm))
    story.append(section_bar("Question 2 — Peut-on prévoir un sevrage difficile ?"))
    story.append(Spacer(1, 2 * mm))
    story.append(P(
        "Le sevrage de la VM est le plus souvent facile : <b>deux tiers</b> des malades "
        "sont définitivement sevrés à l'issue de la première épreuve de VS <i>[a]</i>. Le "
        "<b>sevrage difficile</b> est défini soit par l'échec de la première épreuve de VS, "
        "soit par la nécessité d'une reprise d'assistance ventilatoire dans les 48 heures "
        "suivant son arrêt programmé <i>[3]</i> — il concerne environ <b>un quart</b> des "
        "patients lors de la première épreuve <i>[b]</i>, et environ <b>15 %</b> des "
        "patients extubés à l'issue de la première épreuve sont ré-intubés dans les 48 "
        "heures <i>[b]</i>. Individualiser les patients à risque est important : la "
        "ré-intubation est associée de manière indépendante à une <b>augmentation de la "
        "mortalité</b> <i>[b, 2]</i>.", S_BODY_SM))
    story.append(Spacer(1, 2 * mm))
    story.append(reco_table([
        ("Facteurs généraux de risque", "Durée de VM précédant le sevrage et score de "
         "gravité élevé (facteurs indépendants) <i>[b]</i>. BPCO <i>[b]</i> ou maladie "
         "neuromusculaire <i>[c]</i> à l'origine de la décompensation initiale : risque au "
         "moins doublé. Insuffisance cardiaque gauche et coronaropathie : facteur de risque "
         "supplémentaire possible <i>[c]</i>. Anxiété/environnement psychologique "
         "défavorable : facteur de risque probable <i>[c]</i>. Âges extrêmes : "
         "<b>non</b> retenus comme facteur de risque indépendant <i>[b]</i>.", None),
        ("Facteurs respiratoires", "Rapport fréquence respiratoire/volume courant (f/VT) "
         "&gt; 105, mesuré 2 min après passage en VS sur pièce en T : détecterait "
         "précocement les patients qui ne toléreront pas l'épreuve <i>[b, 2]</i>, mais "
         "intérêt discutable (valeur variable selon les études, mesure non standardisée, "
         "nécessite un spiromètre) — <b>non recommandé en routine</b> <i>[b, 3]</i>. "
         "D'autres indices (pressions, résistance, compliance) sont insuffisamment "
         "spécifiques/sensibles <i>[b, 3]</i>.", None),
        ("Critères prédictifs de l'échec de l'extubation", "Distincts des critères de "
         "sevrage difficile. Liés à la pathologie sous-jacente (atteinte neurologique "
         "centrale) <i>[b]</i> ou au terrain (enfant, sexe féminin) <i>[b]</i>. Aspiration "
         "trachéale nécessaire au moins toutes les 2 heures, ou toux inefficace : "
         "difficulté d'extubation largement accrue <i>[b]</i>. Un obstacle laryngo-trachéal "
         "peut être recherché par test de fuite (ballonnet dégonflé) ou test d'obstruction "
         "de la sonde, techniques non correctement validées <i>[c, 3]</i>. La présence de "
         "ces facteurs <b>ne doit pas retarder</b> le sevrage, mais impose une vigilance "
         "accrue si l'extubation est décidée.", None),
    ], [32 * mm, PAGE_W - 2 * MARGIN - 32 * mm - 18 * mm - 20 * mm, 18 * mm]))
    return story

def _section_q3():
    story = []
    story.append(Spacer(1, 2 * mm))
    story.append(section_bar("Question 3 — Comment conduire le sevrage ?"))
    story.append(Spacer(1, 2 * mm))
    story.append(KeepTogether([
        P("<b>Intérêt d'un protocole de sevrage</b>", S_CELL_B),
        Spacer(1, 1.5 * mm),
        P(
            "La recherche systématique et quotidienne de critères simples autorisant "
            "l'épreuve de VS évite la prolongation inutile de la VM ; elle peut être "
            "efficacement réalisée par le personnel infirmier et/ou les kinésithérapeutes "
            "dans le cadre d'un protocole <i>[a, 1]</i>. Cette attitude réduit l'incidence "
            "des auto-extubations, des trachéotomies, du nombre de patients ventilés de "
            "façon prolongée et de la durée de séjour en réanimation <i>[a, 1]</i>. Le "
            "protocole doit être écrit, élaboré avec toute l'équipe soignante, simple "
            "d'application, et diffusé largement (objectifs, modalités, résultats) lors de "
            "réunions régulières <i>[3]</i>.", S_BODY_SM),
    ]))
    story.append(Spacer(1, 2.5 * mm))
    story.append(P("<b>L'épreuve de ventilation spontanée (VS)</b>", S_CELL_B))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "Dès que le pré-requis est réuni, l'épreuve de VS doit être réalisée sans délai, "
        "en règle par le personnel infirmier et/ou les kinésithérapeutes <i>[2]</i>. "
        "<b>Modalités :</b> patient informé, rassuré, encouragé, installé en position "
        "semi-assise, aspiration trachéo-bronchique préalable. L'épreuve peut être menée "
        "sur <b>pièce en T</b> (air humidifié et enrichi en oxygène, dispositif anti "
        "ré-inspiration) ou en <b>aide inspiratoire</b> (AI ≈ 7 cmH2O, ballonnet gonflé, "
        "sans PEP associée) — les deux modalités ne diffèrent pas en pourcentage de "
        "patients tolérant l'épreuve ou restant en VS à 48 h <i>[a, 1]</i>. L'AI est "
        "préférée si la sonde d'intubation est de diamètre inadéquat ou à haut risque "
        "d'obstruction <i>[3]</i> ; le choix reste sinon fonction des habitudes de l'unité. "
        "Un filtre échangeur de chaleur et d'humidité accroît l'espace mort instrumental et "
        "nécessite d'augmenter le niveau d'AI <i>[b, 2]</i>. Il n'est pas recommandé "
        "d'ajouter une PEP au niveau d'AI de l'épreuve <i>[3]</i>.", S_BODY_SM))
    story.append(Spacer(1, 2 * mm))
    story.append(P(
        "<b>Durée :</b> 30 à 120 minutes <i>[1]</i>, sauf insuffisance respiratoire "
        "restrictive d'origine neuromusculaire (échec parfois retardé) où une durée d'au "
        "moins 12 heures est souvent proposée <i>[3]</i> ; à l'inverse, la durée peut être "
        "raccourcie à 30 minutes minimum si un sevrage facile est prévisible (décision "
        "médicale) <i>[3]</i>.<br/><br/>"
        "<b>Surveillance :</b> état clinique, monitorage continu de la FR, FC, pression "
        "artérielle et oxymétrie de pouls, aspiration régulière. L'apparition de "
        "<b>signes de mauvaise tolérance</b> — FR &gt; 35/min, SpO2 &lt; 90 %, variation "
        "&gt; 20 % de FC ou de PAS, sueurs, troubles de la vigilance, agitation — impose "
        "de vérifier la perméabilité de la sonde et d'interrompre l'épreuve après "
        "prélèvement des gaz du sang artériel <i>[b, 3]</i> ; en l'absence de signe de "
        "mauvaise tolérance, les gaz du sang ne sont pas systématiques <i>[3]</i>. En cas "
        "de succès, rechercher les facteurs de risque d'échec de l'extubation (Q2) ; en "
        "leur absence et après aspiration gastrique, extuber sur <b>prescription écrite</b> "
        "<i>[3]</i>. Chez l'adulte, aucune corticothérapie systématique n'est justifiée "
        "pour prévenir l'œdème laryngé <i>[a, 1]</i>.", S_BODY_SM))
    story.append(Spacer(1, 2 * mm))
    story.append(info_panel(P(
        "<b>Échec de l'épreuve de VS :</b> rechercher et traiter les causes (obstruction de "
        "sonde/arbre trachéo-bronchique, insuffisance ventriculaire gauche, ischémie "
        "myocardique, neuromyopathie de réanimation, sepsis, anémie, dysfonction "
        "diaphragmatique, bronchospasme, désordres métaboliques/nutritionnels). La "
        "<b>VACI allonge la durée du sevrage et ne doit pas être proposée</b> "
        "<i>[a, 1]</i>. Deux modalités possibles <i>[b, 2]</i> : (1) AI ajustée pour une FR "
        "de 20-30/min, épreuves quotidiennes de VS poursuivies en parallèle avec "
        "décroissance progressive de l'AI ; (2) ventilation volumétrique assistée "
        "contrôlée avec essais de VS quotidiens de durée croissante jusqu'à tolérance de "
        "30-120 min consécutives, puis extubation.",
        S_BODY_SM), bg=RED_LIGHT, border=RED))
    return story

def _section_q4():
    story = []
    story.append(Spacer(1, 2 * mm))
    story.append(section_bar("Question 4 — Particularités selon le terrain"))
    story.append(Spacer(1, 2 * mm))
    story.append(P(
        "Le déroulement de la procédure de sevrage est identique quelle que soit la "
        "maladie et doit débuter le plus tôt possible <i>[c, 2]</i>. Les données "
        "spécifiques concernent surtout les patients BPCO, cardiopathes, neurologiques, "
        "chirurgicaux et pédiatriques.", S_BODY_SM))
    story.append(Spacer(1, 2 * mm))
    cw = [36 * mm, PAGE_W - 2 * MARGIN - 36 * mm - 18 * mm, 18 * mm]
    story.append(reco_table([
        ("BPCO", "Facteur de risque de sevrage difficile <i>[b, 2]</i> (déséquilibre "
         "charge/capacité des muscles respiratoires, hyperinflation dynamique ; aggravé "
         "par une insuffisance ventriculaire gauche associée). Bronchodilatateurs si "
         "bronchospasme : augmentent les chances de succès <i>[c, 3]</i> ; intérêt des "
         "corticoïdes systémiques non évalué. Critères pré-requis identiques à la "
         "population générale <i>[3]</i>. Épreuve de VS en AI ou pièce en T "
         "<i>[a, 1]</i> ; seuil de mauvaise tolérance parfois abaissé à SpO2 &lt; 88 % "
         "<i>[c, 3]</i> ; durée de 120 min privilégiée du fait du risque de sevrage "
         "difficile <i>[c, 3]</i>. En cas d'échec : reprise rapide de la VM en AI + PEP "
         "et bronchodilatateurs <i>[b, 2]</i>. VNI proposable en cas d'échec d'extubation "
         "<i>[b, 2]</i> ; VNI après extubation délibérée malgré échec de l'épreuve encore "
         "en cours d'évaluation, <b>non recommandée actuellement</b> <i>[a] [3]</i>.", None),
        ("Cardiopathie", "Le passage en VS augmente le retour veineux et la postcharge "
         "ventriculaire gauche : peut induire une insuffisance cardiaque aiguë "
         "<i>[b]</i> ; la stimulation catécholaminergique peut causer une ischémie "
         "myocardique chez les patients à risque <i>[b]</i>. Pré-requis identique au cas "
         "général <i>[3]</i>. En cas de sevrage difficile : évaluation par "
         "échocardiographie et/ou cathétérisme cardiaque droit ; réduction de la volémie "
         "(diurétiques) et des résistances vasculaires (vasodilatateurs) théoriquement "
         "préférable à la stimulation de l'inotropisme <i>[c, 3]</i> ; sevrage progressif "
         "logique dans ce contexte <i>[3]</i>.", None),
        ("Neurologique — pathologies cérébrales", "Sevrage envisageable seulement en "
         "l'absence d'hypertension intracrânienne <i>[2]</i>. Chances de succès "
         "augmentent avec le score de Glasgow <i>[b]</i>. Échecs d'extubation plus "
         "fréquents (risque d'encombrement : troubles de déglutition, toux inefficace) "
         "<i>[b]</i> — recours plus fréquent à la trachéotomie <i>[b, 2]</i>.", None),
        ("Neurologique — maladies neuromusculaires", "Évaluation clinique régulière "
         "nécessaire. Dans les affections en voie d'amélioration (ex. polyradiculonévrite "
         "aiguë) : mesures répétées de la capacité vitale (&gt; 8-10 mL/kg), Pimax "
         "(&lt; -20 cmH2O), Pemax (&gt; 40 cmH2O) <i>[c, 3]</i>. Épreuve de VS d'au moins "
         "12 h ; hypercapnie &gt; 45 mmHg = signe de gravité majeure ; toute baisse même "
         "modeste de la SaO2 témoigne d'une hypoventilation grave <i>[2]</i>. CV minimale "
         "de 15 mL/kg proposée pour l'extubation au cours de la polyradiculonévrite "
         "aiguë, en l'absence de trouble de déglutition <i>[c, 3]</i>.", None),
        ("Neurologique — maladies dégénératives", "Au décours de la première "
         "décompensation respiratoire, discuter avec le patient et sa famille les choix "
         "thérapeutiques futurs pour faciliter les décisions ultérieures (non coté).", None),
        ("Patients chirurgicaux", "Assimilés à la population générale, hormis une "
         "dysfonction diaphragmatique postopératoire transitoire (chirurgie thoracique et "
         "abdominale) et la douleur, qui doit être traitée <i>[b, 2]</i>. Taux d'échec "
         "d'extubation le plus faible de toutes les catégories <i>[b]</i>.", None),
        ("Patients pédiatriques", "Procédure identique à celle de l'adulte <i>[c, 2]</i>. "
         "Épreuve de VS en AI ou pièce en T malgré des résistances élevées des tubes de "
         "petit diamètre <i>[a, 1]</i>. Incidence de complications laryngées plus "
         "importante (ventilation habituellement à fuites), potentiellement prévenue par "
         "des corticoïdes 6 à 12 heures avant l'extubation <i>[b]</i>. Indices prédictifs "
         "d'échec pas plus discriminants que chez l'adulte <i>[b]</i>.", None),
    ], cw))
    return story

def _section_q5():
    story = []
    story.append(Spacer(1, 2 * mm))
    story.append(section_bar("Question 5 — Échec du sevrage : que faire ?"))
    story.append(Spacer(1, 2 * mm))
    story.append(P(
        "<b>Définition :</b> persistance d'une dépendance ventilatoire partielle ou totale "
        "malgré des tentatives de sevrage répétées depuis <b>au moins 30 jours</b> — "
        "situation concernant des patients ventilés sur sonde d'intubation, de "
        "trachéotomie, ou même de façon non invasive <i>[3]</i>. Elle représente environ "
        "<b>5 %</b> des patients de réanimation, mais pose un problème majeur de prise en "
        "charge (comas chroniques, insuffisance respiratoire chronique, séquelles de "
        "défaillance multiviscérale, complications postopératoires sévères).", S_BODY_SM))
    story.append(Spacer(1, 2 * mm))
    story.append(reco_table([
        ("Prise en charge en réanimation", "La VNI peut être proposée en cas d'échec du "
         "sevrage de la ventilation endotrachéale <i>[b, 2]</i> (jamais évaluée de façon "
         "prospective et randomisée dans cette indication précise) ; contre-indiquée en "
         "cas de troubles majeurs de la conscience ou de déglutition <i>[b, 2]</i>, "
         "parfois impossible en cas de fuites importantes ou d'intolérance du masque "
         "<i>[c]</i>. La trachéotomie diminue le travail respiratoire <i>[b]</i>, facilite "
         "la toilette bronchique et améliore le confort <i>[d]</i> (intérêt dans le "
         "sevrage jamais démontré) ; proposable en cas de contre-indication ou d'échec de "
         "la VNI, sans critère validé pour définir le moment optimal — décision au cas "
         "par cas <i>[3]</i>.", None),
        ("Hospitalisation hors réanimation", "Objectifs : poursuite du sevrage et mise en "
         "place d'une réhabilitation (entraînement à l'exercice, assistance nutritionnelle, "
         "kinésithérapie, éducation du patient) <i>[b, 2]</i>, dans des unités de soins "
         "intermédiaires respiratoires, unités de soins de suite spécialisées ou unités de "
         "sevrage (équivalent des « weaning centers » nord-américains) <i>[2]</i>.", None),
        ("Prise en charge à domicile", "Très développée en France ; envisageable "
         "seulement avec l'aide de professionnels entraînés <i>[b, 2]</i>. Pour une "
         "dépendance ventilatoire &gt; 16 h/jour : infrastructure dédiée requise (deux "
         "ventilateurs avec alarmes haute/basse pression, batterie de secours, "
         "humidificateur-réchauffeur, aspiration trachéale avec batteries, source "
         "d'oxygène de secours, ballon autogonflable type Ambu® si trachéotomie) et "
         "possibilité de contacter un référent médical et technique 24 h/24. Charge "
         "particulièrement lourde pour la famille <i>[b, 2]</i>.", None),
        ("Limitation de soins", "À envisager lorsque le recours à la VNI ou à la "
         "trachéotomie apparaît comme une obstination déraisonnable, ou lorsque le "
         "patient refuse la procédure de sevrage et/ou la poursuite des soins — sans "
         "négliger le rôle de la famille <i>[3]</i>.", None),
    ], [34 * mm, PAGE_W - 2 * MARGIN - 34 * mm - 18 * mm, 18 * mm]))
    story.append(Spacer(1, 3 * mm))
    story.append(P("<b>Figure 1 — Déroulement de la procédure de sevrage</b> "
                    "(organigramme, reconstruit à partir du rendu visuel de la page source)",
                    S_CELL_B))
    story.append(Spacer(1, 1.5 * mm))
    story.append(algo_table())
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<i>Notes de la figure (verbatim) : 1) Le médecin peut décider que l'un ou "
        "plusieurs des éléments du pré-requis peut(vent) ne pas être présent(s). 2) Le "
        "choix entre les deux techniques et la durée de l'épreuve de VS dépend des "
        "habitudes de l'unité. 3) L'extubation est une décision médicale sur prescription "
        "écrite ; l'absence des critères d'extubation ne conduit pas systématiquement à la "
        "refuser. 4) Le sevrage difficile correspond à l'échec de l'épreuve de VS ou à la "
        "reprise de l'assistance ventilatoire dans les 48 heures suivant son arrêt "
        "programmé. 5) Réussi dès la première épreuve de VS, le sevrage est dit facile. "
        "6) L'échec du sevrage correspond à la persistance d'une ventilation partielle ou "
        "totale malgré des tentatives de sevrage répétées depuis au moins 30 jours.</i>",
        S_NOTE))
    return story

def _section_futur_sources():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("Pistes de recherche & sources", color=GREY))
    story.append(Spacer(1, 2 * mm))
    story.append(P(
        "<b>Pistes de recherche suggérées par le jury :</b> critères prédictifs d'échec de "
        "l'extubation ; intérêt de protocoles de sevrage appliqués à des sous-groupes "
        "homogènes (neuromusculaires, neurochirurgie, chirurgie thoraco-abdominale, "
        "pédiatrie) ; place de la VNI dans la procédure de sevrage (extubation délibérée, "
        "prévention de la ré-intubation) ; place de la trachéotomie dans le sevrage ; place "
        "des algorithmes automatisés.", S_BODY_SM))
    story.append(Spacer(1, 2.5 * mm))
    story.append(P(
        "<b>Document source :</b> XXIe Conférence de Consensus en Réanimation et Médecine "
        "d'Urgence de la Société de Réanimation de Langue Française (SRLF), avec la "
        "participation de la Société Française d'Anesthésie et de Réanimation (SFAR), de la "
        "Société de Pneumologie de Langue Française et du Groupe Francophone de "
        "Réanimation et Urgences Pédiatriques (GFRUP). Ecole Normale Supérieure, 16 allée "
        "d'Italie, Lyon, jeudi 11 octobre 2001. Texte publié dans Réanimation "
        "2001;10:697-8. Organisée conformément aux règles méthodologiques de l'ANAES.",
        S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>Jury :</b> Président C. Richard (Le Kremlin-Bicêtre) ; L. Beydon (Angers), S. "
        "Cantagrel (Tours), A. Cuvelier (Rouen), B. Fauroux (Paris), B. Garo (Brest), L. "
        "Holzapfel (Bourg-en-Bresse), O. Lesieur (La Rochelle), J. Levraut (Nice), E. Maury "
        "(Paris), C. Polet (Rouen), N. Roche (Paris), J. Roeseler (Bruxelles). Conseillers "
        "scientifiques : C. Chopin (Lille), T. Similowski (Lyon). Organisateur local : D. "
        "Robert (Lyon).", S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>Méthodologie :</b> Society of Critical Care Medicine Rating System (1997) — "
        "lettre de niveau de preuve (a &gt; b &gt; c &gt; d) et, quand possible, chiffre de "
        "niveau de recommandation (1 &gt; 2 &gt; 3), imprimés entre crochets. Le texte mêle "
        "ces cotations à de simples renvois bibliographiques numérotés sans lettre — les "
        "deux sont reproduits verbatim dans cette fiche, sans être distingués par une puce "
        "de couleur (voir avertissement méthodologique, page 1).", S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>Couverture :</b> cette fiche reprend l'intégralité des questions 1 à 5 du texte "
        "long de la conférence (critères de début de sevrage, prédiction du sevrage "
        "difficile, conduite de l'épreuve de VS, particularités selon le terrain, conduite "
        "à tenir en cas d'échec), les pistes de recherche du jury et l'organigramme "
        "« Procédure de sevrage » (Figure 1, page 11 de la source), reconstruit à partir "
        "d'un rendu visuel à 150dpi (page composée d'une image, sans texte extractible). "
        "Champ de la conférence : <b>hors nouveau-né et réveil d'anesthésie</b> (voir "
        "intro).", S_SOURCE))
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Avertissement — document de 2001 :</b> cette fiche de synthèse indépendante est "
        "produite pour un usage d'aide-mémoire. Elle reprend l'intégralité des questions "
        "traitées et de l'organigramme du texte source, mais ne remplace pas le texte "
        "intégral (argumentaire complet, références bibliographiques numérotées) et n'est "
        "ni éditée ni validée par la SRLF, la SFAR ou les sociétés partenaires. <b>Les "
        "pratiques de ventilation et de sevrage ont évolué depuis 2001</b> (essais "
        "cliniques ultérieurs sur les protocoles de sevrage automatisés, la VNI post-"
        "extubation, les indices prédictifs) : en cas de doute, se référer au texte "
        "intégral, aux recommandations ultérieures et/ou à un avis spécialisé.",
        S_BODY_SM), bg=GREY_LIGHT, border=GREY))
    return story

def _section_1():
    return _section_intro()

def _section_2():
    return _section_q1() + [Spacer(1, 3 * mm)] + _section_q2()

def _section_3():
    return _section_q3()

def _section_4():
    return _section_q4()

def _section_5():
    return _section_q5()

def _section_6():
    return _section_futur_sources()

# Tried merging Q3+Q4 into one combinator group (pages 3 and 4 individually were <60%
# full): rebuilt and re-measured the ACTUAL page count via _count_pages() rather than
# assuming — it stayed at 6 pages (the merge just redistributed the same content across
# the same number of pages: page 3 became fuller but page 4 correspondingly emptier).
# Reverted to the one-question-per-page layout below: same page count, but clearer
# per-page headers for the reader (each page names exactly the question it covers) —
# same precedent as fiche_civd.py.
SECTIONS = [
    ("Introduction, champ & méthodologie", _section_1),
    ("Q1-Q2 — Début du sevrage & prédiction du sevrage difficile", _section_2),
    ("Q3 — Conduite de l'épreuve de ventilation spontanée", _section_3),
    ("Q4 — Particularités selon le terrain", _section_4),
    ("Q5 — Échec du sevrage & organigramme", _section_5),
    ("Pistes de recherche & sources", _section_6),
]

def _make_doc(path=None):
    return SimpleDocTemplate(path or OUT, pagesize=A4,
                              leftMargin=MARGIN, rightMargin=MARGIN,
                              topMargin=32 * mm, bottomMargin=16 * mm,
                              title="Fiche SRLF/SFAR 2001 - Sevrage de la ventilation mecanique",
                              author="Synthese independante (source SRLF/SFAR)")

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
    # Throwaway measurement builds go to a fresh tempfile.mktemp() path, NEVER to OUT
    # (reusing OUT here was found to corrupt page 1's header_band in the final build).
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
