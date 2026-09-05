# -*- coding: utf-8 -*-
"""
Fiche de synthese - SRLF, avec la participation du GFRUP et de la SFMU (2009)
"Prise en charge en situation d'urgence et en reanimation des etats de mal
epileptiques de l'adulte et de l'enfant (nouveau-ne exclu)" - Recommandations
formalisees d'experts. H. Outin, T. Blanc, I. Vinatier, le groupe d'experts,
Reanimation 2009;18:4-12, doi:10.1016/j.reaurg.2008.07.008, disponible en ligne
le 26 juillet 2008. Source : sources/mal_epileptique.pdf (9 pages) / .txt.

METHODOLOGIE : contrairement au systeme GRADE a deux axes (niveau de preuve
1+/1-/2+/2- puis force d'accord) utilise dans d'autres fiches de ce corpus, et
contrairement au systeme NGP (Niveau de Grade des Preuves) + accord
professionnel utilise par la fiche HAS de ce corpus, ce document RFE SRLF ne
comporte qu'un UNIQUE axe : la force de l'accord des experts, cotee selon une
methode derivee de la RAND/UCLA (echelle continue 1-9, deux tours de cotation,
trois zones de mediane - desaccord (1-3) / indecision (4-6) / accord (7-9) -,
chaque zone etant qualifiee de "forte" si l'intervalle de mediane reste a
l'interieur d'une des trois zones, ou de "faible" s'il empiete sur une borne).
Chaque proposition individuelle du corps du texte porte donc le tag explicite
"(accord fort)" ou "(accord faible)" - aucun niveau de preuve distinct n'est
imprime nulle part dans le document.

RECONCILIATION DU COMPTAGE DES TAGS (disclosure methodologique) : la consigne
de tache suggerait de verifier le compte via `grep -c "accord fort\\|accord
faible"`, qui renvoie 164 (lignes correspondantes) / 165 (occurrences sur une
seule ligne). Une verification plus poussee (normalisation des retours a la
ligne du texte extrait du PDF, qui coupe frequemment le tag "(accord fort)"/
"(accord faible)" entre deux lignes, ex. "...induction (accord\\nfort)." aux
lignes 432-433 source) montre que le TEXTE SOURCE CONTIENT EN REALITE 190
occurrences du tag (167 "accord fort" + 23 "accord faible"), et non ~164 - le
grep naif sur une seule ligne sous-compte de 25 tags scindes par un saut de
ligne dans l'extraction. Ce chiffre de 190 est le denominateur reel utilise ici
pour la verification d'exhaustivite (voir recapitulatif en fin de script et
rapport de construction). Les 190 tags bruts sont consolides en 149 lignes de
tableau distinctes (141 dans les theme_table + 8 dans la classification_table
dediee du champ 1) : chaque enumeration a tags IDENTIQUES au sein d'un meme
item clinique (ex. contre-indications listees dans une seule phrase, sous-
etapes d'une meme posologie) est regroupee en une seule ligne ; en revanche,
JAMAIS deux tags DIFFERENTS ne sont fusionnes dans une meme ligne/puce - c'est
la regle etablie de ce corpus. Exception notable necessitant un eclatement
strict : "les affections degeneratives (accord faible) ou les lesions
cicatricielles (...) (accord fort)" (une seule phrase source, deux tags
differents) est scindee en deux lignes de tableau distinctes.

CLASSIFICATION DES EME (Champ 1) : la liste des huit formes cliniques de l'EME,
classees par degre d'urgence pronostique, porte un tag INDIVIDUEL par forme
clinique et les tags DIFFERENT au sein de la liste (2 formes "accord fort" -
pronostic vital engage a court terme -, 6 formes "accord faible" - pronostic
vital/fonctionnel a moyen terme ou pas de pronostic vital engage a court
terme). Chacune des huit formes est donc restituee individuellement dans un
tableau dedie (classification_table), avec regroupement visuel par degre
d'urgence (SPAN) mais AUCUNE fusion de tag.

RECOMMANDATIONS NEGATIVES : ce document en comporte plusieurs, toutes conservees
avec leur polarite negative explicite, jamais adoucies :
 - "Le midazolam n'est pas recommande en induction" (Champ 5, technique
   d'induction anesthesique) ;
 - "Aucune molecule a visee neuroprotectrice ne peut etre recommandee
   actuellement" (Champ 5) ;
 - "Les vertus neuroprotectrices de l'hypothermie n'ont pas ete confirmees en
   pratique clinique" (Champ 5) ;
 - "L'attitude qui consiste a administrer un complement de dose de phenytoine,
   fosphenytoine ou phenobarbital ne repose sur aucune donnee clinique
   validee" (Champ 7) ;
 - "Il est recommande de NE PAS utiliser le propofol dans le traitement des
   etats de mal convulsifs refractaires [chez l'enfant], en raison de
   l'absence de superiorite demontree ... et du risque d'accident mortel lie
   au syndrome de perfusion de propofol, plus frequent chez l'enfant que chez
   l'adulte" (Champ 8, specificites pediatriques) - LA recommandation negative
   explicitement signalee par la tache, retranscrite ici mot pour mot, en gras.

DOSES EXACTES (retranscrites sans arrondi ni paraphrase) : clonazepam
0,015 mg/kg, diazepam 0,15 mg/kg (adulte), lorazepam 0,1 mg/kg (adulte) ;
phenobarbital adulte 15 mg/kg IV, debit max 100 mg/min ; phenobarbital enfant
15-20 mg/kg, debit max 100 mg/min ; fosphenytoine adulte 20 mg/kg equivalent
phenytoine sodique, debit max 150 mg/min ; phenytoine adulte 20 mg/kg, debit
max 50 mg/min ; phenytoine enfant, dose de charge 20 mg/kg (max 1 g), debit
max 1 mg/kg/min ; fosphenytoine enfant 20 mg/kg equivalent phenytoine, debit
max 3 mg/kg/min ; valproate de sodium 25 mg/kg dose de charge puis 1 a
4 mg/kg/h ; sulfate de magnesium (eclampsie) 4 g/20 min puis 1 g/h ; thiamine
100 mg IV lent ; thiopental bolus 2 mg/kg/20 sec puis 3-5 mg/kg/h ; propofol
bolus 2 mg/kg puis 2-5 mg/kg/h (max 5 mg/kg/h au-dela de 48 h) ; midazolam
bolus 0,1 mg/kg puis 0,05-0,6 mg/kg/h (adulte), 0,15-0,50 mg/kg puis
0,12-1,4 mg/kg/h (enfant) ; pyridoxine (nourrisson) 50 a 100 mg/kg.

CHAMP PEDIATRIQUE : le titre du document couvre explicitement "l'adulte et
l'enfant (nouveau-ne exclu)". Verification directe du texte : il N'EXISTE PAS
de chapitre pediatrique dedie et distinct - les specificites de l'enfant sont
tissees dans chaque champ concerne (definitions, diagnostic differentiel,
enquete etiologique, facteurs pronostiques, posologies de premiere intention,
et posologies de l'EME refractaire), le plus souvent sous forme d'un
paragraphe "Chez l'enfant" a la fin de la section adulte correspondante. Ce
script transcrit systematiquement le volet pediatrique juxtapose au volet
adulte plutot que de l'omettre, et signale chaque ligne pediatrique par la
mention "(enfant)" dans son theme.

ICONE : reprise de icon_shield (deja utilisee avec color=NAVY par
fiche_traumatisme_cranien.py, seule autre fiche neuro-reanimatoire de ce
corpus a utiliser cette combinaison) plutot que d'inventer une icone "cerveau"
- aucune icone neuro dediee n'existe dans style.py, et icon_shield porte deja
la connotation de "protection cerebrale" recurrente dans cette RFE (controle
des facteurs d'agression cerebrale, risque de lesions cerebrales).

CONVENTION DE CHIP : extension locale non invasive de GRADE_COLORS, reprenant
exactement la convention deja etablie par fiche_nutrition.py (seule autre
fiche de ce corpus a utiliser un systeme a un seul axe "accord fort/faible"
sans niveaux GRADE) : "Fort" -> vert, "Faible" -> teal.

_count_pages() : implementation copiee a l'identique de fiche_aap_programmee.py
- les passes de comptage ecrivent vers un tempfile.mktemp() jetable, jamais
vers OUT, pour eviter le bug deja documente (reutiliser OUT pour les passes de
comptage ET la construction finale corrompt silencieusement le header_band de
la page 1).

Pas d'arrondis Unicode (fleches/exposants/emoji) dans le corps du texte -
encodage Helvetica de cette chaine de production.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from style import *
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.units import mm

# Local, non-invasive extension of the shared GRADE_COLORS dict - mirrors the
# precedent set in fiche_nutrition.py (the corpus's other single-axis
# "accord fort/faible" document).
GRADE_COLORS["Fort"] = (GREEN, WHITE)
GRADE_COLORS["Faible"] = (TEAL, WHITE)

OUT = "/private/tmp/claude-501/-Users-macbook-Downloads-claude/65498e3e-5ddf-47a6-b100-3ac535d1faa0/scratchpad/rfe_sfar/output/Fiche_SRLF_Mal_Epileptique_2009.pdf"

SOURCE_TXT = ("Source : Outin H, Blanc T, Vinatier I, le groupe d'experts — SRLF, avec la "
              "participation du GFRUP et de la SFMU — « Prise en charge en situation "
              "d'urgence et en réanimation des états de mal épileptiques de l'adulte et de "
              "l'enfant (nouveau-né exclu) » — Recommandations formalisées d'experts, "
              "Réanimation 2009;18:4—12, doi:10.1016/j.reaurg.2008.07.008. Fiche de synthèse "
              "non officielle : se référer au texte intégral.")

def P(txt, style=S_CELL):
    return Paragraph(txt, style)

def chip(label, **kw):
    return grade_chip(label, **kw)

def theme_table(rows, col_widths, header=("Thème", "Recommandation", "Accord")):
    """rows: (theme, text, grade_label) - 'theme' replaces the usual Réf. column since
    this source has no per-recommendation reference numbers."""
    data = [[P(header[0], S_HEAD_W), P(header[1], S_HEAD_W), P(header[2], S_HEAD_W_C)]]
    for theme, txt, grade in rows:
        data.append([P(theme, S_CELL_B), P(txt, S_CELL), chip(grade)])
    t = Table(data, colWidths=col_widths, repeatRows=1)
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

def legend_flowable():
    chip_w = 18 * mm
    content_w = PAGE_W - 2 * MARGIN
    gap = 4 * mm
    text_w = (content_w - 2 * chip_w - gap) / 2.0
    row = Table([[chip("Fort", width=chip_w - 2 * mm),
                  P("<b>Accord fort</b> — intervalle de médiane des cotations "
                    "(échelle RAND/UCLA 1—9) resté à l'intérieur de la zone "
                    "« accord » (7—9), « désaccord » (1—3) ou « indécision » (4—6).",
                    S_BADGE_HEAD),
                  chip("Faible", width=chip_w - 2 * mm),
                  P("<b>Accord faible</b> — intervalle de médiane empiétant sur une "
                    "borne de zone (ex. intervalle [1—4] ou [6—8]).", S_BADGE_HEAD)]],
                 colWidths=[chip_w, text_w, chip_w, text_w])
    row.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                              ("LEFTPADDING", (0, 0), (-1, -1), 1),
                              ("RIGHTPADDING", (0, 0), (-1, -1), 3)]))
    return row

def classification_table():
    """Champ 1 - classification operationnelle des EME (Fig. texte) : trois degres
    d'urgence pronostique, huit formes cliniques individuellement taguees (tags
    DIFFERENTS au sein de la liste - jamais fusionnes)."""
    cw = PAGE_W - 2 * MARGIN
    c0 = 46 * mm
    c2 = 16 * mm
    c1 = cw - c0 - c2
    S_TIER = pstyle("tier", fontSize=7.9, leading=9.6, textColor=WHITE, fontName=FONT_BOLD)

    def tc(txt, style=S_CELL):
        return Paragraph(txt, style)

    data = [
        [P("Degré d'urgence pronostique", S_HEAD_W), P("Forme clinique d'EME", S_HEAD_W), P("Accord", S_HEAD_W_C)],
        [tc("Pronostic vital engagé à court terme", S_TIER),
         tc("EME convulsif généralisé tonicoclonique (d'emblée ou secondairement généralisé)"), chip("Fort")],
        ["", tc("EME larvé"), chip("Fort")],
        [tc("Pronostic vital et/ou fonctionnel engagé à moyen terme", S_TIER),
         tc("EME confusionnel partiel complexe"), chip("Faible")],
        ["", tc("EME convulsif focal avec ou sans marche Bravais-Jacksonienne"), chip("Faible")],
        [tc("N'engageant pas le pronostic vital à court terme", S_TIER),
         tc("EME convulsif généralisé myoclonique"), chip("Faible")],
        ["", tc("EME absence"), chip("Faible")],
        ["", tc("EME à symptomatologie élémentaire, donc sans rupture de contact "
                "(hallucinations, aphasie...)"), chip("Faible")],
        ["", tc("Épilepsie partielle continue"), chip("Faible")],
    ]
    t = Table(data, colWidths=[c0, c1, c2], repeatRows=1)
    style_cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), NAVY), ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTNAME", (0, 0), (-1, 0), FONT_BOLD), ("FONTSIZE", (0, 0), (-1, 0), 8),
        ("SPAN", (0, 1), (0, 2)), ("SPAN", (0, 3), (0, 4)), ("SPAN", (0, 5), (0, 8)),
        ("BACKGROUND", (0, 1), (0, 2), GREEN), ("BACKGROUND", (0, 3), (0, 4), AMBER),
        ("BACKGROUND", (0, 5), (0, 8), TEAL_DARK),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("ALIGN", (2, 0), (2, -1), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 0.5, GREY_LIGHT),
        ("TOPPADDING", (0, 0), (-1, -1), 3.2), ("BOTTOMPADDING", (0, 0), (-1, -1), 3.2),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            style_cmds.append(("BACKGROUND", (1, i), (-1, i), BG_PANEL))
    t.setStyle(TableStyle(style_cmds))
    return t

TOTAL_PAGES = {"n": 10}

def on_page(canvas, doc, page_title):
    header_band(canvas, doc, "SRLF / GFRUP / SFMU — RFE 2009 — FICHE DE SYNTHÈSE",
                "États de mal épileptiques",
                page_title, icon_fn=lambda c, x, y: icon_shield(c, x, y, 13 * mm), color=NAVY)
    footer_band(canvas, doc, SOURCE_TXT, f"Page {doc.page} / {TOTAL_PAGES['n']}")

# ---------------------------------------------------------------------------
def _section_intro():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Champ :</b> prise en charge en situation d'urgence (préhospitalière et "
        "hospitalière) et en réanimation des <b>états de mal épileptiques (EME)</b>, "
        "convulsifs et non convulsifs, chez l'<b>adulte ET l'enfant</b> — le "
        "<b>nouveau-né est explicitement exclu</b> du champ de ces recommandations. "
        "Dix champs d'application ont été définis par le comité d'organisation, "
        "auxquels s'ajoute un champ transversal dédié aux spécificités "
        "pédiatriques ; en pratique, ces spécificités pédiatriques sont tissées "
        "dans chaque champ concerné plutôt que rassemblées en un chapitre unique "
        "(voir disclosure ci-dessous et repère « (enfant) » sur les lignes "
        "concernées de cette fiche).<br/><br/>"
        "<b>Méthodologie — un seul axe, à la différence de GRADE et du système "
        "NGP+Accord :</b> ces recommandations ne comportent <b>aucun niveau de "
        "preuve GRADE (1+/1-/2+/2-)</b> ni de <b>Niveau de Grade des Preuves "
        "(NGP) associé à un accord professionnel</b> distinct — deux systèmes à "
        "deux axes utilisés par d'autres fiches de ce corpus. Chaque proposition "
        "de ce document porte un <b>unique</b> tag de force d'accord, coté selon "
        "une méthode dérivée de la RAND/UCLA : échelle continue graduée de 1 à "
        "9 (1 = désaccord complet/absence totale de preuve/contre-indication "
        "formelle ; 9 = accord complet/preuve formelle/indication formelle), "
        "deux tours de cotation après élimination des valeurs extrêmes "
        "(experts déviants). Trois zones sont définies selon la position de la "
        "médiane : désaccord (1—3), indécision (4—6), accord (7—9). L'accord "
        "(comme le désaccord ou l'indécision) est dit <b>« fort »</b> si "
        "l'intervalle de médiane reste à l'intérieur d'une des trois zones, et "
        "<b>« faible »</b> s'il empiète sur une borne (ex. intervalle [1—4] ou "
        "[6—8]).",
        S_BODY), bg=BG_PANEL, border=TEAL))
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Reconciliation du comptage des tags (disclosure) :</b> un comptage "
        "naïf ligne par ligne du texte extrait (grep monoligne) trouve environ "
        "164—165 occurrences de « accord fort »/« accord faible ». Une "
        "vérification exhaustive (normalisation des retours à la ligne, le tag "
        "étant fréquemment scindé entre deux lignes par l'extraction PDF, "
        "ex. « ...induction (accord\\nfort). ») montre que le texte source "
        "contient en réalité <b>190 occurrences</b> (167 « fort » + 23 "
        "« faible »). Ce chiffre de 190 est le dénominateur réel de "
        "vérification utilisé pour cette fiche ; il est consolidé en "
        "<b>149 lignes de recommandation distinctes</b> (141 dans les tableaux "
        "thématiques + 8 dans le tableau de classification dédié du champ 1) "
        "par regroupement des tags strictement IDENTIQUES au sein d'un même "
        "item clinique (jamais de "
        "fusion entre tags différents — règle constante de ce corpus). Le détail "
        "de cette consolidation figure dans l'en-tête du script source et dans "
        "« Sources et traçabilité » en fin de document.",
        S_BODY_SM), bg=AMBER_LIGHT, border=AMBER))
    story.append(Spacer(1, 3 * mm))

    story.append(section_bar("Légende (convention de ce document)"))
    story.append(Spacer(1, 2 * mm))
    story.append(legend_flowable())
    return story

def _section_champ1():
    story = []
    story.append(Spacer(1, 2 * mm))
    story.append(P(
        "<i>Épidémiologie (contexte, non tagué) : l'incidence annuelle des EME "
        "convulsifs et non convulsifs est comprise entre 10 et 41 pour "
        "100 000 habitants, plus élevée chez l'enfant et l'adulte de plus de "
        "60 ans. Les lésions cérébrales apparaissent expérimentalement chez le "
        "primate au bout de 60 à 90 minutes d'EME convulsif généralisé.</i>",
        S_NOTE))
    story.append(Spacer(1, 2 * mm))
    story.append(KeepTogether([
        section_bar("Champ 1 — Définitions de l'EME"),
        Spacer(1, 2 * mm),
        theme_table([
            ("Définition générale", "L'EME est défini, de façon générale, par des crises "
             "continues ou par la succession de crises sans amélioration de la conscience "
             "sur une période de 30 minutes.", "Fort"),
            ("EME tonicoclonique généralisé", "Du fait de sa gravité, l'EME tonicoclonique "
             "généralisé requiert une définition spécifique impliquant une prise en charge "
             "plus précoce. Cette définition opérationnelle fait référence à des crises "
             "continues ou subintrantes pendant au moins cinq minutes.", "Fort"),
            ("EME larvé — définition", "L'EME larvé correspond à l'évolution défavorable "
             "d'un EME tonicoclonique généralisé non traité ou traité de façon inadéquate. "
             "Il se caractérise par l'atténuation, voire la disparition des manifestations "
             "motrices chez un patient comateux contrastant avec la persistance d'un EME "
             "électrique.", "Fort"),
            ("Crises sérielles", "Les crises sérielles avec récupération de la conscience "
             "antérieure entre les crises peuvent évoluer vers un état de mal mais ne "
             "rentrent pas dans la définition de celui-ci.", "Fort"),
            ("Définitions chez l'enfant (enfant)", "Chez l'enfant, les définitions sont les "
             "mêmes. L'état de conscience en pédiatrie étant très fluctuant, il est d'autant "
             "plus difficile à apprécier que l'enfant est plus jeune.", "Fort"),
        ], [34 * mm, PAGE_W - 2 * MARGIN - 34 * mm - 16 * mm, 16 * mm]),
    ]))
    story.append(Spacer(1, 3 * mm))
    story.append(KeepTogether([
        section_bar("Formes cliniques et classification"),
        Spacer(1, 2 * mm),
        theme_table([
            ("EME convulsif vs non convulsif", "On distingue sur un plan clinique les EME "
             "convulsifs, dont le diagnostic repose sur les seules données cliniques, des "
             "EME non convulsifs, dont le diagnostic plus difficile nécessite la "
             "réalisation d'un électroencéphalogramme (EEG).", "Fort"),
            ("Classification opérationnelle", "Une classification « opérationnelle » basée "
             "sur le pronostic et donc sur le degré d'urgence thérapeutique est "
             "indispensable dans la pratique quotidienne. La classification proposée "
             "prend en compte trois degrés de mise en jeu du pronostic (détail ci-dessous).",
             "Fort"),
        ], [34 * mm, PAGE_W - 2 * MARGIN - 34 * mm - 16 * mm, 16 * mm]),
    ]))
    story.append(Spacer(1, 2 * mm))
    story.append(classification_table())
    story.append(Spacer(1, 3 * mm))
    story.append(theme_table([
        ("Encéphalopathies épileptiques — tolérance (enfant)", "Dans le cadre des "
         "encéphalopathies épileptiques, chez l'enfant comme chez l'adulte, il faut savoir "
         "tolérer les EME toniques (que les benzodiazépines peuvent aggraver), cloniques ou "
         "myocloniques et ne pas avoir systématiquement recours à des traitements "
         "agressifs.", "Faible"),
    ], [34 * mm, PAGE_W - 2 * MARGIN - 34 * mm - 16 * mm, 16 * mm]))
    return story

def _section_champ2():
    story = []
    story.append(Spacer(1, 2 * mm))
    cw = [30 * mm, PAGE_W - 2 * MARGIN - 30 * mm - 16 * mm, 16 * mm]
    story.append(KeepTogether([
        section_bar("Champ 2 — Diagnostic différentiel"),
        Spacer(1, 2 * mm),
        theme_table([
            ("Réévaluation neurologique", "Tout patient hospitalisé pour un EME doit être "
             "secondairement réévalué par un neurologue, afin de préciser, à distance de "
             "l'épisode aigu, le diagnostic positif, syndromique et différentiel de l'EME, "
             "et d'adapter les éventuels traitements antiépileptiques.", "Fort"),
        ], cw),
    ]))
    story.append(Spacer(1, 2.5 * mm))
    story.append(P("<b>Pseudo état de mal</b>", S_CELL_B))
    story.append(Spacer(1, 1 * mm))
    story.append(theme_table([
        ("Évocation systématique", "Face à des manifestations motrices prolongées atypiques "
         "suggérant un EME convulsif, il convient systématiquement d'évoquer un pseudo état "
         "de mal (origine psychogène).", "Fort"),
        ("Signes cliniques évocateurs", "Les éléments cliniques faisant évoquer ce diagnostic "
         "doivent être connus de tout médecin prenant en charge un EME tonicoclonique : "
         "fermeture des yeux, résistance à l'ouverture des yeux, atypie des mouvements et "
         "contact possible avec le patient.", "Fort"),
        ("EEG en cas de doute", "En cas de doute diagnostique, l'EEG (idéalement couplé à un "
         "enregistrement vidéo) est utile pour distinguer un EME d'un pseudo état de mal.",
         "Faible"),
    ], cw))
    story.append(Spacer(1, 2.5 * mm))
    story.append(P("<b>Mouvements anormaux</b>", S_CELL_B))
    story.append(Spacer(1, 1 * mm))
    story.append(theme_table([
        ("EEG + EMG", "En cas de mouvement anormal dont l'origine épileptique est suspectée, "
         "chez un patient en réanimation, l'enregistrement d'un EEG devrait comporter au "
         "moins une dérivation d'électromyogramme, et doit être au mieux couplé à un "
         "enregistrement vidéo simultané.", "Fort"),
        ("Test benzodiazépine non probant", "La suppression d'un mouvement anormal par "
         "l'injection de benzodiazépine ne prouve pas son origine épileptique.", "Fort"),
    ], cw))
    story.append(Spacer(1, 2.5 * mm))
    story.append(P("<b>Encéphalopathie postanoxique</b>", S_CELL_B))
    story.append(Spacer(1, 1 * mm))
    story.append(theme_table([
        ("Clinique", "L'encéphalopathie postanoxique s'accompagne souvent de myoclonies non "
         "épileptiques d'importance variable, typiquement à prédominance axiale, parfois "
         "déclenchées par des stimulations sonores et tactiles. Elle ne s'accompagne que "
         "rarement de crise d'épilepsie voire d'un EME convulsif.", "Fort"),
        ("EEG — pointes périodiques", "L'EEG lors d'une encéphalopathie postanoxique montre "
         "des anomalies variées, en particulier des pointes périodiques généralisées qui ne "
         "doivent pas faire évoquer des crises voire un état de mal. Des myoclonies non "
         "épileptiques peuvent être associées ou non à ces anomalies EEG.", "Fort"),
        ("Pas de traitement", "Dans un contexte d'anoxie cérébrale, des pointes périodiques "
         "généralisées sur l'EEG, qui ne s'organisent pas en décharge rythmique, et sans "
         "symptôme clinique autre qu'un coma, reflètent un trouble de l'électrogenèse "
         "corticale et ne doivent pas conduire à un traitement.", "Fort"),
        ("Diagnostic différentiel (enfant)", "Le diagnostic différentiel chez l'enfant entre "
         "crise d'épilepsie occipitale prolongée et migraine avec aura est parfois "
         "difficile.", "Fort"),
    ], cw))
    return story

def _section_champ3():
    story = []
    story.append(Spacer(1, 2 * mm))
    cw = [32 * mm, PAGE_W - 2 * MARGIN - 32 * mm - 16 * mm, 16 * mm]
    story.append(KeepTogether([
        section_bar("Champ 3 — Place de l'électroencéphalogramme"),
        Spacer(1, 2 * mm),
        theme_table([
            ("Traitement sans attendre l'EEG", "Le traitement d'un EME dont le diagnostic "
             "est évident doit débuter sans attendre l'EEG.", "Fort"),
            ("Disponibilité de l'EEG", "Celui-ci devrait idéalement être disponible 24 h/24 "
             "pour le diagnostic et le suivi des formes graves.", "Fort"),
        ], cw),
    ]))
    story.append(Spacer(1, 2.5 * mm))
    story.append(P("<b>Un EEG en urgence est indiqué :</b>", S_CELL_B))
    story.append(Spacer(1, 1 * mm))
    story.append(theme_table([
        ("EME convulsif généralisé", "Un EEG en urgence est indiqué dans les EME convulsifs "
         "généralisés, sans en retarder la prise en charge thérapeutique initiale.", "Fort"),
        ("Suspicion EME non convulsif", "Un EEG en urgence est indiqué en cas de suspicion "
         "d'EME non convulsif à expression confusionnelle.", "Fort"),
        ("Doute persistant — pseudo EM", "Un EEG en urgence est indiqué en cas de doute "
         "persistant sur un pseudo état de mal.", "Faible"),
    ], cw))
    story.append(Spacer(1, 2.5 * mm))
    story.append(theme_table([
        ("EEG systématique", "Tout patient hospitalisé pour un EME doit bénéficier d'un EEG "
         "le plus tôt possible.", "Fort"),
        ("Caractéristiques de l'EEG standard", "Un enregistrement EEG standard avec au moins "
         "huit voies, et idéalement 21 voies, durant au moins 20 minutes, et au mieux "
         "30 minutes, est l'examen de référence.", "Fort"),
        ("Couplage vidéo", "Il doit être au mieux couplé à un enregistrement vidéo.", "Faible"),
        ("Utilité de l'EEG", "Il permet de confirmer le diagnostic d'EME, d'écarter les "
         "diagnostics différentiels, de préciser le cas échéant le diagnostic syndromique "
         "voire étiologique, de guider la prise en charge thérapeutique, et de participer "
         "au suivi évolutif de l'EME.", "Fort"),
        ("Test d'injection antiépileptique", "Un test d'injection d'un antiépileptique "
         "d'action rapide lors d'un EEG n'est en faveur d'une activité épileptique que s'il "
         "corrige les anomalies EEG et améliore cliniquement le patient. Ce test "
         "thérapeutique doit se faire en présence d'un médecin.", "Fort"),
        ("Vocabulaire et conclusion", "L'interprétation de l'EEG doit utiliser un "
         "vocabulaire facilement compréhensible et comporter une conclusion qui stipule la "
         "présence (ou la persistance) ou non d'un EME.", "Fort"),
        ("Interprétation contextualisée", "Il ne s'interprète qu'à la lumière des données "
         "cliniques et des différents traitements reçus par le patient.", "Fort"),
        ("Expertise visuelle", "L'expertise visuelle est plus fiable que les logiciels "
         "d'analyse de l'EEG.", "Fort"),
        ("Anomalies diffuses/périodiques — piège", "La présence d'anomalies EEG diffuses et "
         "périodiques, et a fortiori celle d'ondes triphasiques, ne doivent pas faire "
         "évoquer le diagnostic d'EME non convulsif, mais plutôt différents types "
         "d'encéphalopathies (postanoxique, métabolique, infectieuse, toxique et "
         "spongiforme).", "Fort"),
        ("Contexte postanoxique — figures périodiques", "Dans un contexte postanoxique, "
         "l'existence de figures épileptiques diffuses (comme des pointes, des "
         "polypointes), n'évoluant pas de façon rythmique, en décharge, mais de façon "
         "périodique, même si elles sont très fréquentes, ne signe habituellement pas "
         "l'existence d'une crise ou d'un EME.", "Fort"),
        ("EEG de longue durée (enfant)", "Chez l'enfant, l'EEG de longue durée (>12 heures) "
         "est très utile au diagnostic positif d'EME non convulsif et pour surveiller "
         "l'efficacité des traitements.", "Fort"),
    ], cw))
    return story

def _section_champ4_etio():
    story = []
    story.append(Spacer(1, 2 * mm))
    cw = [32 * mm, PAGE_W - 2 * MARGIN - 32 * mm - 16 * mm, 16 * mm]
    story.append(KeepTogether([
        section_bar("Champ 4 — Enquête étiologique"),
        Spacer(1, 2 * mm),
        theme_table([
            ("Recherche rapide", "La recherche étiologique doit être effectuée rapidement, "
             "sans retarder ni la mise en œuvre du traitement antiépileptique ni les "
             "manœuvres de réanimation.", "Fort"),
            ("EME multi-étiologique", "Un EME répond souvent à plusieurs étiologies.", "Faible"),
            ("Étiologie non maîtrisée", "Si une étiologie n'est pas diagnostiquée et "
             "maîtrisée, elle peut être un facteur d'entretien de l'EME.", "Fort"),
        ], cw),
    ]))
    story.append(Spacer(1, 2.5 * mm))
    story.append(theme_table([
        ("Troubles métaboliques", "La recherche de certains troubles métaboliques est "
         "incontournable. Une hypoglycémie, une hyponatrémie et une hypocalcémie doivent "
         "être recherchées et corrigées en urgence.", "Fort"),
        ("Patient épileptique connu — 1re cause", "Chez le patient épileptique connu, la "
         "première cause d'EME est un sevrage de médicaments antiépileptiques relatif ou "
         "absolu par non-observance thérapeutique, adjonction d'un traitement inducteur "
         "enzymatique ou au cours du changement de médicament antiépileptique.", "Fort"),
        ("Patient épileptique connu — autres causes", "Les principales autres causes sont "
         "l'intoxication ou le sevrage alcoolique, la prescription de médicaments "
         "proconvulsivants et les infections intercurrentes.", "Faible"),
        ("Enquête si doute étiologique", "En l'absence de facteur déclenchant évident, en "
         "cas de doute étiologique ou d'EME persistant, l'enquête doit être identique à "
         "celle réalisée devant un EME inaugural, du fait de l'intrication fréquente des "
         "étiologies.", "Fort"),
        ("EME inaugural — étiologies principales", "En cas d'EME inaugural, les principales "
         "étiologies sont les souffrances cérébrales aiguës, qu'elles soient structurelles "
         "(méningoencéphalites, accidents vasculaires cérébraux, traumatismes...) ou "
         "fonctionnelles (hyponatrémie aiguë, intoxications médicamenteuses ou par "
         "substances illicites...).", "Fort"),
        ("EME inaugural — étiologies plus rares", "Plus rarement, car dans ces cas le "
         "patient peut déjà avoir présenté des crises : les lésions cérébrales subaiguës "
         "évolutives (comme les tumeurs, la toxoplasmose cérébrale), les affections "
         "dégénératives.", "Faible"),
        ("EME inaugural — lésions cicatricielles", "Les lésions cicatricielles (comme les "
         "séquelles d'accident vasculaire cérébral et de traumatisme) figurent également "
         "parmi les étiologies possibles, plus rares, d'un EME inaugural.", "Fort"),
        ("Enquête négative", "Dans moins de 10 % des cas, l'enquête est négative.", "Fort"),
    ], cw))
    story.append(Spacer(1, 2.5 * mm))
    story.append(P("<b>Imagerie cérébrale</b>", S_CELL_B))
    story.append(Spacer(1, 1 * mm))
    story.append(theme_table([
        ("Principe — indications larges", "Les indications de l'imagerie cérébrale doivent "
         "rester larges. Il faut tenir compte, chez le patient épileptique connu, des "
         "circonstances de survenue de l'état de mal (par exemple traumatisme en cours de "
         "crise) et des caractéristiques électrocliniques habituelles des crises.", "Fort"),
        ("Indications en urgence", "L'imagerie cérébrale (scanner cérébral sans et avec "
         "injection, ou IRM) est indiquée en urgence, en tenant compte de l'état "
         "neurologique antérieur : s'il existe des signes de localisation ; si une "
         "ponction lombaire est nécessaire ; en cas de notion de traumatisme crânien ; en "
         "cas de notion de néoplasie ; en cas de notion d'immunodépression (VIH, "
         "corticothérapie...) ; si la cause demeure obscure.", "Fort"),
        ("Début électroclinique partiel", "L'imagerie cérébrale est également indiquée en "
         "urgence si le début électro-clinique de l'EME est partiel.", "Faible"),
    ], cw))
    story.append(Spacer(1, 2.5 * mm))
    story.append(P("<b>Ponction lombaire</b>", S_CELL_B))
    story.append(Spacer(1, 1 * mm))
    story.append(theme_table([
        ("Indications", "Une ponction lombaire, en dehors de ses contre-indications, est "
         "préconisée dans un contexte infectieux et en cas d'immunodépression.", "Fort"),
        ("Négativité de l'enquête", "Une ponction lombaire est également préconisée en cas "
         "de négativité de la recherche étiologique.", "Faible"),
        ("Fébrile — ATB + acyclovir sans délai (enfant)", "Chez l'adulte et plus encore "
         "chez l'enfant, en cas d'état de mal convulsif fébrile, lorsque la ponction "
         "lombaire ne peut être réalisée immédiatement, il est recommandé de débuter sans "
         "délai par voie veineuse un traitement antibiotique probabiliste et de "
         "l'acyclovir vis-à-vis d'une possible encéphalite herpétique.", "Fort"),
    ], cw))
    story.append(Spacer(1, 2.5 * mm))
    story.append(theme_table([
        ("Persistance sans étiologie", "La persistance de l'EME sans étiologie identifiée "
         "impose la poursuite des examens, en s'aidant dès que possible des conseils d'un "
         "neurologue.", "Fort"),
        ("Hypocalcémie/hypomagnésémie (enfant)", "Chez l'enfant, une hypocalcémie profonde "
         "(calcémie ionisée &lt; 0,8 mmol/l) ou une hypomagnésémie (&lt; 0,5 mmol/l) "
         "peuvent être responsables d'un EME ; sa correction par voie veineuse ne sera "
         "effectuée qu'après dosage sanguin.", "Faible"),
        ("Pyridoxine — nourrisson (enfant)", "En l'absence de cause évidente à un EME "
         "convulsif chez un nourrisson, une injection de pyridoxine doit être proposée "
         "(50 à 100 mg/kg) en milieu de réanimation sous monitorage et enregistrement EEG.",
         "Fort"),
    ], cw))
    return story

def _section_champ4_pronostic():
    story = []
    story.append(Spacer(1, 2 * mm))
    cw = [32 * mm, PAGE_W - 2 * MARGIN - 32 * mm - 16 * mm, 16 * mm]
    story.append(P(
        "<i>La mortalité des EME est mieux étudiée que leur morbidité : elle est comprise "
        "entre 8 et 39 % des cas (décès survenant dans les 30 premiers jours après le "
        "début de l'EME), et est principalement déterminée par l'étiologie (contexte, non "
        "tagué).</i>", S_NOTE))
    story.append(Spacer(1, 2 * mm))
    story.append(KeepTogether([
        section_bar("Facteurs pronostiques"),
        Spacer(1, 2 * mm),
        theme_table([
            ("Qualité de la prise en charge", "La qualité de la prise en charge améliore "
             "le pronostic.", "Fort"),
            ("Pronostic fonctionnel", "Le pronostic fonctionnel (séquelles motrices, "
             "cognitives, apparition ou aggravation d'une maladie épileptique) est "
             "difficile à déterminer indépendamment des facteurs étiologiques sous-jacents "
             "et des complications liées à la prise en charge.", "Fort"),
            ("Trois déterminants (adulte et enfant)", "Chez l'adulte comme chez l'enfant, "
             "les trois principaux déterminants de la mortalité et des séquelles "
             "neurologiques d'un EME sont l'âge, sa cause et sa durée.", "Fort"),
            ("EME de novo — risque d'épilepsie", "Par rapport à des crises épileptiques "
             "inaugurales, un EME de novo augmente le risque de développer une épilepsie.",
             "Fort"),
            ("Caractère réfractaire", "Le caractère réfractaire d'un EME augmente le risque "
             "de mortalité, le risque de récidive d'EME et possiblement celui de développer "
             "une maladie épileptique.", "Fort"),
            ("Pronostic plus sévère si fébrile (enfant)", "Chez l'enfant, le pronostic de "
             "l'EME est plus sévère lorsqu'il est fébrile, compte tenu du risque de lésions "
             "hippocampiques.", "Fort"),
        ], cw),
    ]))
    return story

def _section_champ5():
    story = []
    story.append(Spacer(1, 2 * mm))
    cw = [32 * mm, PAGE_W - 2 * MARGIN - 32 * mm - 16 * mm, 16 * mm]
    story.append(KeepTogether([
        section_bar("Champ 5 — Prise en charge non spécifique de l'EME convulsif généralisé"),
        Spacer(1, 2 * mm),
        theme_table([
            ("Hospitalisation et transfert en réanimation", "La prise en charge "
             "symptomatique de l'EME convulsif généralisé est une urgence. Elle nécessite, "
             "en préhospitalier, l'intervention d'une équipe médicale d'urgence. "
             "L'hospitalisation est systématique. Le transfert en réanimation est indiqué "
             "en cas de persistance des crises, du trouble de la vigilance ou de "
             "défaillances associées.", "Fort"),
        ], cw),
    ]))
    story.append(Spacer(1, 2.5 * mm))
    story.append(theme_table([
        ("Contrôle des facteurs d'agression cérébrale", "Dans tous les cas, le contrôle des "
         "facteurs d'agression cérébrale est impératif, ce d'autant que l'EME est "
         "consécutif à des lésions cérébrales aiguës.", "Fort"),
        ("Mesures de prise en charge immédiate", "Les mesures de prise en charge immédiate "
         "comportent : la mise en position latérale de sécurité, le maintien de la liberté "
         "des voies aériennes supérieures, une oxygénation avec pour objectif une SpO2 "
         "supérieure ou égale à 95 %, la mise en place d'une voie veineuse périphérique "
         "avec perfusion de sérum physiologique, la mesure de la glycémie capillaire et la "
         "correction d'une éventuelle hypoglycémie.", "Fort"),
        ("Intubation/VM non systématique", "L'intubation et la ventilation mécanique ne "
         "sont pas systématiques d'emblée. Elles sont indiquées en cas de recours à des "
         "agents anesthésiques, de détresse respiratoire aiguë ou d'altération profonde et "
         "prolongée de la vigilance, malgré l'arrêt des convulsions.", "Fort"),
        ("Préhospitalier — délai de recours à la VM", "En préhospitalier, la sécurité du "
         "transport autorise un délai plus court de recours à la ventilation mécanique.",
         "Faible"),
        ("Technique d'induction anesthésique", "La technique d'induction anesthésique "
         "recommandée est celle de la procédure à séquence rapide. L'utilisation de "
         "succinylcholine est recommandée. Les curares de longue durée d'action doivent "
         "être évités. Le thiopental, le propofol, ou l'étomidate peuvent être utilisés "
         "comme agent d'induction. <b>Le midazolam n'est pas recommandé en induction.</b>",
         "Fort"),
        ("Sédation d'entretien en préhospitalier", "En préhospitalier, l'entretien d'une "
         "sédation chez les patients ventilés est souvent nécessaire. Le midazolam est "
         "recommandé et l'adjonction d'un morphinomimétique est utile. Les curares de "
         "longue durée d'action doivent être évités afin de ne pas masquer des "
         "convulsions.", "Fort"),
        ("Interruption de la sédation à l'arrivée", "En dehors des situations "
         "d'hypertension intracrânienne, l'interruption de la sédation est conseillée à "
         "l'arrivée du patient en réanimation, afin de faciliter l'évaluation de l'état "
         "neurologique et de l'activité épileptique.", "Fort"),
        ("Curarisation ponctuelle", "Chez le malade intubé et ventilé, le recours à une "
         "curarisation ponctuelle peut s'avérer nécessaire pour éliminer les artéfacts "
         "musculaires sur l'EEG et pour réaliser une ponction lombaire ou une imagerie "
         "cérébrale.", "Fort"),
    ], cw))
    story.append(Spacer(1, 2.5 * mm))
    story.append(theme_table([
        ("Objectif ventilatoire — normocapnie", "Lorsque la sédation et la ventilation "
         "restent nécessaires, l'objectif est d'obtenir une normoxie et une normocapnie "
         "(35 à 40 mmHg). La ventilation en hypocapnie est contre-indiquée, y compris en "
         "cas d'œdème cérébral.", "Fort"),
        ("Objectif hémodynamique", "Il est recommandé de maintenir une pression artérielle "
         "moyenne entre 70 et 90 mmHg.", "Fort"),
        ("Surveillance ECG", "La surveillance continue du tracé électrocardiographique et "
         "la réalisation dès que possible d'un électrocardiogramme sont indispensables.",
         "Fort"),
        ("Hyperthermie / hypothermie", "La détection et le traitement d'une hyperthermie "
         "font partie intégrante de la prise en charge de l'EME. <b>Les vertus "
         "neuroprotectrices de l'hypothermie n'ont pas été confirmées</b> en pratique "
         "clinique.", "Fort"),
        ("Monitorage glycémie/natrémie", "Le monitorage et le contrôle de la glycémie (en "
         "prévenant tout épisode d'hypoglycémie) et celui de la natrémie sont "
         "systématiques. L'acidose métabolique se corrige généralement avec l'arrêt des "
         "crises, sans que l'administration de bicarbonates soit nécessaire.", "Fort"),
        ("Éthylique — thiamine", "Chez l'éthylique connu ou suspecté, l'injection de "
         "thiamine (vitamine B1 : 100 mg en intraveineux lent) est recommandée.", "Fort"),
        ("HTIC — facteur d'agression secondaire", "En cas d'hypertension intracrânienne "
         "potentielle ou avérée (traumatisme crânien, pathologie cérébrale vasculaire, "
         "infectieuse, tumorale...), l'EME est considéré comme un véritable facteur "
         "d'agression secondaire susceptible d'aggraver l'hypertension intracrânienne.",
         "Fort"),
        ("Neuroprotection médicamenteuse", "<b>Aucune molécule à visée neuroprotectrice ne "
         "peut être recommandée</b> actuellement.", "Fort"),
    ], cw))
    return story

def _section_champ7_schema():
    story = []
    story.append(Spacer(1, 2 * mm))
    cw = [32 * mm, PAGE_W - 2 * MARGIN - 32 * mm - 16 * mm, 16 * mm]
    story.append(P(
        "<i>Champ 6 (pharmacologie, contexte non tagué) : aucune courbe dose—effet n'est "
        "disponible pour les antiépileptiques utilisés dans l'EME, ce qui gêne la "
        "comparaison entre molécules en équipotence ; le choix d'un agent et/ou d'une "
        "stratégie repose donc sur une opinion consensuelle d'experts.</i>", S_NOTE))
    story.append(Spacer(1, 2 * mm))
    story.append(KeepTogether([
        section_bar("Champ 7 — Schéma thérapeutique initial (EME convulsif généralisé)"),
        Spacer(1, 2 * mm),
        theme_table([
            ("Urgence thérapeutique", "Un traitement antiépileptique doit être, une fois le "
             "diagnostic établi, administré en urgence devant des crises convulsives "
             "généralisées continues ou subintrantes persistant au moins cinq minutes. La "
             "pérennisation de l'EME convulsif augmente le risque de lésions cérébrales et "
             "induit une pharmacorésistance dont les mécanismes sont mal connus.", "Fort"),
        ], cw),
    ]))
    story.append(Spacer(1, 2.5 * mm))
    story.append(theme_table([
        ("EME larvé — PEC immédiate", "L'EME larvé nécessite une prise en charge immédiate "
         "sans attendre l'EEG si l'histoire clinique et les manifestations observées sont "
         "évocatrices.", "Fort"),
        ("Monitorage systématique", "Dans tous les cas, un monitorage de la fréquence "
         "cardiaque et respiratoire, de la pression artérielle et de la saturation en "
         "oxygène est mis en place.", "Fort"),
        ("Hypotension sous traitement", "La survenue d'une hypotension ou de troubles du "
         "rythme cardiaque impose la diminution du débit de perfusion de l'antiépileptique "
         "en cours ou son arrêt (éventuellement transitoire) en fonction de la sévérité.",
         "Fort"),
        ("Schéma initial 5—30 minutes", "Quand le patient est pris en charge entre cinq et "
         "30 minutes après le début des convulsions, une benzodiazépine en monothérapie "
         "est recommandée par voie intraveineuse lente (en une à deux minutes au moins). "
         "En cas de persistance des convulsions au bout de cinq minutes, on procédera à "
         "une seconde injection de la même benzodiazépine, à la même dose, associée à un "
         "autre médicament antiépileptique en intraveineux.", "Fort"),
        ("Schéma initial au-delà de 30 minutes", "Quand le patient est pris en charge "
         "au-delà de 30 minutes après le début des convulsions, une injection de "
         "benzodiazépine est effectuée, d'emblée associée à un autre médicament "
         "antiépileptique en intraveineux. En cas de persistance des convulsions, au bout "
         "de cinq minutes, on procédera à une seconde injection de la même benzodiazépine "
         "à la même dose.", "Fort"),
        ("Choix du médicament associé", "Le médicament antiépileptique donné en association "
         "avec la benzodiazépine sera de la phénytoïne/fosphénytoïne ou du phénobarbital. "
         "Le choix tiendra compte de leurs contre-indications, de l'appréciation de leurs "
         "risques iatrogènes et de leur rapidité d'action. Dans des situations "
         "particulières, le valproate de sodium (qui n'a pas l'AMM dans l'EME) pourra être "
         "utilisé.", "Fort"),
        ("Dose intégrale à administrer", "Quelle que soit l'évolution des convulsions, y "
         "compris une éventuelle cessation, l'intégralité de la dose prescrite doit être "
         "administrée.", "Fort"),
        ("EME larvé — schéma applicable", "Le schéma proposé pour l'EME larvé est celui "
         "décrit pour l'EME convulsif évoluant depuis plus de 30 minutes.", "Fort"),
    ], cw))
    story.append(Spacer(1, 2.5 * mm))
    story.append(P("<b>Échec du traitement de première ligne</b> (persistance des "
                    "convulsions 20 min après le début de la perfusion de phénobarbital, ou "
                    "30 min après le début de la perfusion de phénytoïne/fosphénytoïne) :",
                    S_CELL_B))
    story.append(Spacer(1, 1 * mm))
    story.append(theme_table([
        ("Recours au 2e antiépileptique", "On proposera le recours au médicament "
         "antiépileptique non utilisé en première intention (phénobarbital après "
         "phénytoïne/fosphénytoïne, et vice versa) si toutes les conditions suivantes sont "
         "satisfaites : EME évoluant depuis moins de 60 minutes ; probabilité faible de "
         "lésion cérébrale aiguë ; pas de facteur incontrôlé d'agression cérébrale "
         "(instabilité hémodynamique, hypoxie, hyperthermie majeure).", "Fort"),
        ("Condition additionnelle", "Ce recours au second antiépileptique de première ligne "
         "suppose en outre l'absence d'EME larvé.", "Faible"),
        ("Autres situations — anesthésie générale", "Dans les autres situations, le recours "
         "à un traitement par thiopental, midazolam ou propofol, sous couvert d'une "
         "assistance respiratoire, est proposé.", "Fort"),
        ("Valproate — limitation de soins", "Le valproate de sodium peut être utilisé dans "
         "des situations où la mise en œuvre d'une anesthésie générale avec ventilation "
         "mécanique est déraisonnable (limitation de soins).", "Fort"),
        ("Compléments de dose — non fondés", "<b>L'attitude qui consiste à administrer un "
         "complément de dose</b> de phénytoïne, fosphénytoïne ou phénobarbital <b>ne repose "
         "sur aucune donnée clinique validée.</b>", "Fort"),
    ], cw))
    story.append(Spacer(1, 2.5 * mm))
    story.append(P("<b>Après le contrôle de l'état de mal</b>", S_CELL_B))
    story.append(Spacer(1, 1 * mm))
    story.append(theme_table([
        ("Relais par benzodiazépines", "Un relais par benzodiazépines par voie entérale "
         "(clobazam : 5 à 10 mg × 3 ou clonazépam : 1 à 2 mg × 3) ou parentérale discontinue "
         "est indispensable. Ce relais doit être immédiat si l'EME a été contrôlé par une "
         "seule dose de diazépam ou de midazolam, en raison du risque de récidive à court "
         "terme.", "Fort"),
        ("Phénobarbital au long cours", "Pour l'instauration ou l'adaptation d'un éventuel "
         "traitement antiépileptique de fond, un avis spécialisé devra être pris. Le "
         "phénobarbital devrait être évité au long cours.", "Faible"),
    ], cw))
    return story

def _section_champ7_posologies():
    story = []
    story.append(Spacer(1, 2 * mm))
    cw = [32 * mm, PAGE_W - 2 * MARGIN - 32 * mm - 16 * mm, 16 * mm]
    story.append(section_bar("Arsenal thérapeutique — posologies (EME non réfractaire)"))
    story.append(Spacer(1, 2 * mm))
    story.append(P("<b>Benzodiazépines</b>", S_CELL_B))
    story.append(Spacer(1, 1 * mm))
    story.append(theme_table([
        ("Choix de la benzodiazépine", "La durée d'action prolongée de plusieurs heures du "
         "clonazépam amène à privilégier son utilisation en France. S'il n'est pas "
         "disponible, le diazépam sera utilisé.", "Fort"),
        ("Posologie clonazépam / diazépam", "La posologie du clonazépam est de "
         "0,015 mg/kg, celle du diazépam de 0,15 mg/kg.", "Fort"),
        ("Lorazépam", "Le lorazépam, benzodiazépine d'action prolongée validée dans des "
         "essais contrôlés, n'est pas disponible en France sauf dans le cadre de l'ATU. La "
         "posologie du lorazépam est de 0,1 mg/kg.", "Fort"),
        ("Voie IV impossible", "Lorsque l'administration de benzodiazépines par voie "
         "intraveineuse est impossible, le midazolam en intramusculaire (0,15 mg/kg) ou "
         "par voie buccale (0,3 mg/kg) peut être employé.", "Fort"),
    ], cw))
    story.append(Spacer(1, 2.5 * mm))
    story.append(P("<b>Phénobarbital</b>", S_CELL_B))
    story.append(Spacer(1, 1 * mm))
    story.append(theme_table([
        ("Posologie IV", "Le phénobarbital est utilisé en intraveineux à la posologie de "
         "15 mg/kg à un débit de perfusion maximum de 100 mg/min.", "Fort"),
        ("Contre-indication et effets", "Il est contre-indiqué chez l'insuffisant "
         "respiratoire sévère. Il induit une dépression de la vigilance, qui peut gêner "
         "l'appréciation de l'état neurologique, et une dépression respiratoire modérée.",
         "Fort"),
        ("Délai d'action", "Le phénobarbital a un délai d'action rapide qui permet de juger "
         "en pratique de sa pleine efficacité 20 minutes après le début de la perfusion.",
         "Fort"),
    ], cw))
    story.append(Spacer(1, 2.5 * mm))
    story.append(P("<b>Fosphénytoïne / Phénytoïne</b>", S_CELL_B))
    story.append(Spacer(1, 1 * mm))
    story.append(theme_table([
        ("Fosphénytoïne — posologie", "La fosphénytoïne (ampoules de 500 mg en équivalents "
         "de phénytoïne sodique) est utilisée à la posologie de 20 mg/kg en équivalents de "
         "phénytoïne sodique, à un débit de perfusion maximum de 150 mg/min. Ce débit "
         "pourra être réduit chez des patients considérés comme fragiles (sujet âgé, "
         "coronarien).", "Fort"),
        ("Phénytoïne — posologie", "La phénytoïne (ampoules de 250 mg) est utilisée à la "
         "posologie de 20 mg/kg avec un débit de perfusion maximum de 50 mg/min. Ce débit "
         "pourra être réduit chez des patients considérés comme fragiles (sujet âgé, "
         "coronarien).", "Fort"),
        ("Contre-indications et effets", "La phénytoïne et la fosphénytoïne sont "
         "contre-indiquées en cas de troubles de la conduction ou de cardiopathie sévère. "
         "Elles influent peu sur la vigilance et la fonction respiratoire.", "Fort"),
        ("Fosphénytoïne préférée", "La phénytoïne nécessite un cathéter périphérique de "
         "gros calibre et une voie unique. La meilleure tolérance locale et la facilité "
         "d'administration de la fosphénytoïne (compatibilité avec les solutés de "
         "perfusion et autres médicaments) la font privilégier à la phénytoïne.", "Fort"),
        ("Délai d'efficacité", "La phénytoïne et la fosphénytoïne, bien qu'administrées à "
         "un débit différent (trois fois plus rapide pour la fosphénytoïne), agissent dans "
         "le même délai. En pratique, leur pleine efficacité ne pourra être évaluée que "
         "30 minutes après le début de la perfusion.", "Fort"),
    ], cw))
    story.append(Spacer(1, 2.5 * mm))
    story.append(P("<b>Valproate de sodium</b>", S_CELL_B))
    story.append(Spacer(1, 1 * mm))
    story.append(theme_table([
        ("Posologie et indications", "Le valproate de sodium en intraveineux est indiqué en "
         "première intention (associé aux benzodiazépines) à la dose de 25 mg/kg en dose "
         "de charge puis, selon les taux sanguins, de 1 à 4 mg/kg par heure par voie "
         "intraveineuse, en cas de contre-indication à la fosphénytoïne et au "
         "phénobarbital, et en cas d'état de mal secondaire à un sevrage en valproate de "
         "sodium.", "Fort"),
        ("Contre-indication", "Il est contre-indiqué en cas d'hépatopathie préexistante.",
         "Fort"),
    ], cw))
    story.append(Spacer(1, 2.5 * mm))
    story.append(P("<b>Particularités liées à certaines étiologies</b>", S_CELL_B))
    story.append(Spacer(1, 1 * mm))
    story.append(theme_table([
        ("Éclampsie", "Lors de l'éclampsie, outre les benzodiazépines et l'extraction du "
         "fœtus en urgence, il est recommandé d'associer du sulfate de magnésium (4 g en "
         "20 minutes puis 1 g/h en intraveineux continu).", "Fort"),
        ("Porphyrie aiguë", "Lors des crises aiguës de porphyrie, on utilise le clonazépam "
         "ou le lorazépam. L'intérêt potentiel du propofol doit être souligné. Sont "
         "notamment contre-indiqués le diazépam, la phénytoïne et la fosphénytoïne, les "
         "barbituriques, le valproate de sodium, l'étomidate et la kétamine "
         "(www.drugs-porphyria.org).", "Faible"),
        ("Intoxications aiguës", "Lors des intoxications par médicaments ou substances "
         "illicites, les benzodiazépines puis les barbituriques (si nécessaires) sont "
         "conseillés.", "Fort"),
    ], cw))
    story.append(Spacer(1, 2.5 * mm))
    story.append(P("<b>Chez l'enfant — posologies</b>", S_CELL_B))
    story.append(Spacer(1, 1 * mm))
    story.append(theme_table([
        ("Benzodiazépines (enfant)", "Les posologies des benzodiazépines sont les "
         "suivantes : 0,1 mg/kg pour le lorazépam (maximum : 4 mg) ; 0,02 à 0,04 mg/kg "
         "pour le clonazépam (maximum : 1 mg) ; 0,2 à 0,4 mg/kg pour le diazépam "
         "(maximum : 5 mg chez l'enfant de moins de cinq ans, 10 mg pour l'enfant de cinq "
         "ans et plus).", "Fort"),
        ("Voies alternatives (enfant)", "Lorsque l'administration d'une benzodiazépine est "
         "impossible par voie intraveineuse, peuvent être utilisés le diazépam par voie "
         "intrarectale (0,3 à 0,5 mg/kg), ou le midazolam par voie nasale (0,2 à "
         "0,3 mg/kg), buccale (0,2 à 0,3 mg/kg) ou intramusculaire (0,2 à 0,5 mg/kg). Le "
         "choix sera avant tout fonction de l'expérience et des préférences des "
         "professionnels ou des parents.", "Fort"),
        ("Phénobarbital (enfant)", "Le phénobarbital est utilisé par voie veineuse à la "
         "posologie de 15 à 20 mg/kg avec un débit de perfusion maximum de 100 mg/min.",
         "Fort"),
        ("Phénytoïne — dose de charge (enfant)", "La dose de charge de phénytoïne par voie "
         "veineuse est de 20 mg/kg (maximum 1 g) sans dépasser un débit de perfusion de "
         "1 mg/kg par minute.", "Fort"),
        ("Fosphénytoïne — restriction d'AMM (enfant)", "Chez l'enfant, il n'y a pas "
         "actuellement de données cliniques suffisamment fortes pour recommander "
         "d'utiliser la fosphénytoïne à la place de la phénytoïne. La fosphénytoïne n'a "
         "l'AMM que chez l'enfant de plus de cinq ans.", "Fort"),
        ("Fosphénytoïne — posologie (enfant)", "Elle est utilisée à la posologie de "
         "20 mg/kg d'équivalent phénytoïne avec un débit de perfusion maximum de "
         "3 mg/kg par minute d'équivalent phénytoïne.", "Fort"),
    ], cw))
    return story

def _section_champ8():
    story = []
    story.append(Spacer(1, 2 * mm))
    cw = [32 * mm, PAGE_W - 2 * MARGIN - 32 * mm - 16 * mm, 16 * mm]
    story.append(KeepTogether([
        section_bar("Champ 8 — État de mal épileptique réfractaire"),
        Spacer(1, 2 * mm),
        theme_table([
            ("Non convulsif/partiel moteur", "En général, il n'est pas indiqué d'induire un "
             "coma médicamenteux dans les EME réfractaires non convulsifs et partiels "
             "moteurs. Un avis spécialisé est nécessaire.", "Fort"),
        ], cw),
    ]))
    story.append(Spacer(1, 2.5 * mm))
    story.append(P("<b>Définition et diagnostic</b>", S_CELL_B))
    story.append(Spacer(1, 1 * mm))
    story.append(theme_table([
        ("Absence de définition consensuelle", "Il n'existe pas de définition consensuelle "
         "de l'EME réfractaire.", "Fort"),
        ("Définition pragmatique", "En général, on peut définir un EME comme réfractaire "
         "lorsqu'il existe une résistance à au moins deux médicaments antiépileptiques "
         "différents administrés à posologie adaptée.", "Fort"),
        ("Traitement initial incomplet", "Les patients en EME convulsif intubés ventilés, "
         "n'ayant pas reçu l'association benzodiazépine—autre médicament antiépileptique "
         "telle qu'elle a été décrite dans le champ 7, ne doivent pas être considérés "
         "comme étant en EME réfractaire ; le traitement devra être complété avant de les "
         "traiter comme tel.", "Fort"),
        ("Écarter les diagnostics différentiels", "Les diagnostics de pseudo état de mal "
         "(origine psychogène) ou de mouvements anormaux d'autre étiologie qu'épileptique "
         "doivent être considérés avant de retenir le diagnostic d'état de mal "
         "réfractaire.", "Fort"),
        ("Encéphalopathie postanoxique", "Dans un contexte d'encéphalopathie postanoxique, "
         "les myoclonies sont rarement en rapport avec un état de mal réfractaire "
         "nécessitant un traitement antiépileptique.", "Fort"),
    ], cw))
    story.append(Spacer(1, 2.5 * mm))
    story.append(P("<b>Arsenal thérapeutique</b>", S_CELL_B))
    story.append(Spacer(1, 1 * mm))
    story.append(theme_table([
        ("Trois traitements de référence", "Les barbituriques, le propofol et le midazolam "
         "sont les trois traitements utilisés dans l'EME réfractaire. Il n'y a pas de "
         "donnée comparative contrôlée concernant ces trois molécules lors de leur "
         "utilisation en cas d'état de mal réfractaire.", "Fort"),
        ("Association systématique", "Il faut toujours associer des médicaments "
         "antiépileptiques aux agents anesthésiques et s'assurer de taux sanguins "
         "efficaces des antiépileptiques.", "Fort"),
        ("Barbituriques — propriétés", "Les barbituriques ont l'avantage d'être connus "
         "depuis de nombreuses années, et le désavantage de présenter une thésaurisation "
         "tissulaire qui en prolonge considérablement la demi-vie plasmatique lors "
         "d'administration en continu.", "Fort"),
        ("Thiopental — posologie", "Le thiopental est administré en plusieurs bolus de "
         "2 mg/kg en 20 secondes toutes les cinq minutes jusqu'à arrêt des convulsions et "
         "selon la tolérance hémodynamique, puis en attendant l'EEG, avec un débit de 3 à "
         "5 mg/kg par heure. La dose d'entretien est adaptée sur les données EEG, et "
         "dépend de la tolérance hémodynamique.", "Fort"),
        ("Propofol — profil et risque SPP", "Le propofol a l'avantage d'une courte "
         "demi-vie d'élimination, et le désavantage d'exposer au risque de développer un "
         "syndrome de perfusion de propofol (SPP ou Propofol Infusion Syndrome « PRIS »). "
         "Le « SPP » constitue une complication probablement rare mais potentiellement "
         "fatale chez les patients en EME réfractaire.", "Fort"),
        ("Propofol — posologie", "Le propofol est administré en bolus initial de 2 mg/kg, "
         "titré jusqu'à arrêt clinique des convulsions (bolus de 1 mg/kg toutes les cinq "
         "minutes), puis en attendant l'EEG à un débit de 2 à 5 mg/kg par heure (parfois "
         "transitoirement jusqu'à 10 mg/kg par heure). La dose d'entretien sera adaptée "
         "sur les données EEG. Il est recommandé d'y associer des benzodiazépines et de ne "
         "pas dépasser la dose de 5 mg/kg par heure au-delà de 48 heures.", "Fort"),
        ("Propofol — surveillance du SPP", "L'utilisation du propofol, particulièrement à "
         "des fortes posologies et au-delà de 48 heures, impose une détermination au "
         "moins biquotidienne des lactates, des triglycérides et des enzymes musculaires "
         "afin de dépister rapidement un « SPP » qui implique son arrêt immédiat.", "Fort"),
        ("Midazolam — tachyphylaxie", "Le midazolam induit une tachyphylaxie importante "
         "lors de l'administration prolongée.", "Fort"),
        ("Midazolam — posologie", "Le midazolam est administré en bolus initial de "
         "0,1 mg/kg, titré jusqu'à arrêt clinique des convulsions (bolus de 0,05 mg/kg "
         "toutes les cinq minutes), puis en attendant l'EEG à un débit de 0,05 à "
         "0,6 mg/kg par heure. La dose d'entretien sera adaptée sur les données EEG et la "
         "tolérance hémodynamique.", "Fort"),
        ("Associations en cas de résistance", "Dans les cas d'EME réfractaires résistant "
         "aux traitements usuels (barbituriques, propofol, midazolam), il peut être utile "
         "de les associer entre eux. Le topiramate, le lévétiracétam, la kétamine "
         "(contre-indiquée en cas d'hypertension intracrânienne et associée à des "
         "benzodiazépines), voire des anesthésiques inhalés peuvent également être, entre "
         "autres, considérés.", "Fort"),
        ("Durée de traitement non déterminée", "La durée de l'administration des "
         "médicaments anesthésiques et la cinétique de leur décroissance ne sont pas "
         "déterminées.", "Fort"),
    ], cw))
    story.append(Spacer(1, 2.5 * mm))
    story.append(P("<b>Objectif thérapeutique</b>", S_CELL_B))
    story.append(Spacer(1, 1 * mm))
    story.append(theme_table([
        ("Suppression clinique et EEG minimal", "Il est bien entendu indispensable "
         "d'obtenir la suppression clinique de l'EME convulsif. L'objectif minimal sur "
         "l'EEG est la suppression des crises.", "Fort"),
        ("Profondeur de suppression non établie", "La profondeur optimale de la "
         "suppression électroencéphalographique — seule suppression des crises, "
         "bouffées-suppressions (burst-suppression) ou tracé isoélectrique — n'est pas "
         "établie.", "Fort"),
        ("Cible burst-suppression proposée", "L'administration d'un médicament "
         "anesthésique ayant pour cible EEG un tracé de bouffées-suppressions "
         "(burst-suppression) pendant 12 à 24 heures est proposée, suivie d'un sevrage "
         "progressif sur 12 à 24 heures.", "Faible"),
        ("Reprise de l'EME après arrêt", "En cas de reprise de l'EME au décours de l'arrêt "
         "du traitement, on peut soit reprendre l'administration du traitement déjà "
         "utilisé, soit passer à une autre substance.", "Fort"),
        ("Poursuite au long cours", "La poursuite du traitement, même après plusieurs "
         "semaines d'EME réfractaire, est justifiée tant qu'il n'y a pas d'argument qui "
         "atteste d'une atteinte irréversible du cerveau.", "Fort"),
    ], cw))
    story.append(Spacer(1, 2.5 * mm))
    story.append(P("<b>Chez l'enfant</b>", S_CELL_B))
    story.append(Spacer(1, 1 * mm))
    story.append(theme_table([
        ("Thiopental (enfant)", "Le thiopental est très efficace, mais ses nombreux effets "
         "secondaires conduisent à proposer de le réserver aux formes les plus rebelles et "
         "de débuter par une perfusion continue de benzodiazépines à fortes doses. La "
         "posologie proposée est identique à celle de l'adulte (bolus de 2 mg/kg répétés "
         "jusqu'à arrêt des convulsions, suivis d'une perfusion continue de 3 à 5 mg/kg "
         "par heure).", "Fort"),
        ("Midazolam — posologie (enfant)", "Le midazolam est la benzodiazépine la mieux "
         "étudiée, mais le diazépam semble aussi efficace. Les posologies proposées "
         "comportent une dose de charge de 0,15 à 0,50 mg/kg suivie d'une perfusion "
         "continue de 0,12 mg/kg par heure, qui peut être augmentée rapidement par paliers "
         "jusqu'à 1,4 mg/kg par heure.", "Fort"),
        ("Midazolam — mise en garde (enfant)", "La facilité d'emploi du midazolam "
         "(hydrosoluble, demi-vie courte) doit être pondérée par la plus grande fréquence "
         "de récidives des convulsions observée avec ce médicament.", "Fort"),
        ("Propofol NON RECOMMANDÉ (enfant)", "<b>Il est recommandé de ne pas utiliser le "
         "propofol</b> dans le traitement des états de mal convulsifs réfractaires chez "
         "l'enfant, en raison de l'absence de supériorité démontrée par rapport aux autres "
         "traitements et <b>du risque d'accident mortel lié au syndrome de perfusion de "
         "propofol, plus fréquent chez l'enfant que chez l'adulte.</b>", "Fort"),
    ], cw))
    return story

def _section_champ9():
    story = []
    story.append(Spacer(1, 2 * mm))
    cw = [32 * mm, PAGE_W - 2 * MARGIN - 32 * mm - 16 * mm, 16 * mm]
    story.append(KeepTogether([
        section_bar("Champ 9 — États de mal épileptiques non convulsifs"),
        Spacer(1, 2 * mm),
        theme_table([
            ("Expression clinique", "L'expression clinique d'un EME non convulsif est le "
             "plus souvent une confusion mentale d'intensité variable.", "Fort"),
            ("EEG nécessaire dès que possible", "La réalisation d'un EEG est nécessaire dès "
             "que possible lors de la suspicion clinique d'un EME non convulsif.", "Fort"),
        ], cw),
    ]))
    story.append(Spacer(1, 2.5 * mm))
    story.append(theme_table([
        ("Collaboration prescripteur/interprète", "Une collaboration étroite entre le "
         "médecin qui demande l'EEG et celui qui l'interprète est indispensable, car le "
         "diagnostic d'EME non convulsif est clinique et électroencéphalographique.",
         "Fort"),
        ("Test diagnostique et thérapeutique BZD", "L'injection d'une benzodiazépine au "
         "cours de l'EEG constitue un test diagnostique et thérapeutique qui est positif "
         "lorsqu'il normalise l'EEG et fait céder la confusion ou les signes "
         "neurologiques. Cependant, sa négativité n'élimine pas ce diagnostic.", "Fort"),
        ("États d'absence de novo — sujet âgé", "L'enquête étiologique des états "
         "d'absence de novo du sujet âgé doit comporter en premier lieu la recherche de "
         "facteurs toxiques et/ou métaboliques comme un sevrage en benzodiazépines ou une "
         "imprégnation chronique en médicaments psychotropes.", "Fort"),
        ("Aggravation paradoxale", "Il faut savoir évoquer, chez un sujet épileptique qui "
         "présente des états d'absence récurrents, la possibilité d'une aggravation "
         "paradoxale de l'épilepsie par certains médicaments antiépileptiques tels que la "
         "carbamazépine, la phénytoïne, le vigabatrin, la gabapentine, la tiagabine, dans "
         "le cadre d'une épilepsie généralisée idiopathique.", "Fort"),
        ("Bilan étiologique — EME partiel inaugural", "Le bilan étiologique d'un EME "
         "partiel non convulsif inaugural impose de rechercher en premier lieu une "
         "affection aiguë du système nerveux central.", "Fort"),
        ("Résistance aux benzodiazépines", "La résistance aux benzodiazépines concerne "
         "essentiellement les états de mal partiels non convulsifs. Une approche "
         "graduelle doit être privilégiée. La phénytoïne ou la fosphénytoïne semblent "
         "être les molécules de choix.", "Fort"),
    ], cw))
    story.append(Spacer(1, 2.5 * mm))
    story.append(P("<b>Coma et anomalies paroxystiques diffuses à l'EEG</b>", S_CELL_B))
    story.append(Spacer(1, 1 * mm))
    story.append(theme_table([
        ("Comas à exclure du cadre nosographique", "Les comas dus à des encéphalopathies "
         "ou agressions cérébrales sévères qui s'accompagnent d'anomalies paroxystiques "
         "diffuses à l'EEG doivent être exclus du cadre nosographique des états de mal non "
         "convulsifs. La présence d'activités EEG paroxystiques généralisées peut en effet "
         "traduire une atteinte cérébrale sévère (en particulier postanoxique), sans "
         "phénomène épileptique associé.", "Faible"),
        ("Différencier de l'EME larvé/non convulsif", "Les anomalies EEG paroxystiques "
         "généralisées parfois rencontrées lors d'un coma consécutif à une agression "
         "cérébrale sévère (post-traumatique, postanoxique...) sont à différencier de "
         "l'EME larvé, terme évolutif d'un EME convulsif généralisé non ou insuffisamment "
         "traité, et surtout de l'EME non convulsif qui peut s'accompagner au maximum "
         "d'un état catatonique mais non d'un coma.", "Faible"),
        ("PEC thérapeutique non codifiée", "La prise en charge thérapeutique d'anomalies "
         "EEG paroxystiques généralisées parfois rencontrées lors d'un coma postagression "
         "cérébrale n'est pas codifiée. Si un traitement antiépileptique devait être "
         "instauré, en particulier devant des anomalies clairement organisées en "
         "décharges successives, l'absence d'amélioration électroclinique nette ne doit "
         "pas conduire à une escalade thérapeutique.", "Fort"),
    ], cw))
    story.append(Spacer(1, 2.5 * mm))
    story.append(theme_table([
        ("Protocoles de service", "La mise en place de protocoles dans les diverses "
         "structures amenées à prendre en charge des EME est recommandée.", "Fort"),
        ("Actualisation à trois ans", "Ces recommandations, établies début 2008, devront "
         "être réactualisées dans un délai maximum de trois ans.", "Fort"),
    ], cw))
    return story

def _section_sources():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("Sources et traçabilité", color=GREY))
    story.append(Spacer(1, 2 * mm))
    story.append(P(
        "<b>Document source :</b> « Prise en charge en situation d'urgence et en "
        "réanimation des états de mal épileptiques de l'adulte et de l'enfant "
        "(nouveau-né exclu) » — Recommandations formalisées d'experts sous l'égide de la "
        "Société de réanimation de langue française (SRLF), avec la participation du "
        "Groupe francophone de réanimation et urgences pédiatriques (GFRUP) et de la "
        "Société française de médecine d'urgence (SFMU). H. Outin, T. Blanc, I. Vinatier, "
        "le groupe d'experts (B. Clair, A. Crespel, P. Convers, S. Demeret, S. Dupont, "
        "N. Engrand, C. Fischer, P. Gelisse, P. Hubert, J.-X. Mazoit, V. Navarro, "
        "D. Parain, A. Rossetti, F. Santoli, K. Tazarourte, P. Thomas, D. Savary, "
        "L. Vallée). Réanimation 2009;18:4—12.", S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P("<b>Publication :</b> doi:10.1016/j.reaurg.2008.07.008 — disponible sur "
                    "Internet le 26 juillet 2008.", S_SOURCE))
    story.append(P("<b>Méthodologie :</b> méthode dérivée de la RAND/UCLA, cotation "
                    "individuelle des experts sur échelle continue 1—9, deux tours de "
                    "cotation ; un seul axe de force d'accord (« fort » / « faible »), "
                    "sans niveau de preuve GRADE ni NGP distinct (voir panneau "
                    "méthodologique page 1).", S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P("<b>Couverture et reconciliation des tags :</b> cette fiche reprend "
                    "l'intégralité des dix champs du corps du texte (définitions et "
                    "classification de l'EME, diagnostic différentiel, place de l'EEG, "
                    "enquête étiologique et facteurs pronostiques, prise en charge non "
                    "spécifique, schéma thérapeutique initial et posologies par molécule, "
                    "EME réfractaire, EME non convulsifs), avec les spécificités "
                    "pédiatriques tissées dans chaque champ concerné (repère "
                    "« (enfant) »). Vérification exhaustive : le texte source contient "
                    "190 occurrences du tag « (accord fort) »/« (accord faible) » (167 "
                    "fort + 23 faible ; un comptage naïf ligne par ligne du texte extrait "
                    "en trouve ~164—165, 25 tags étant scindés entre deux lignes par "
                    "l'extraction PDF). Ces 190 tags sont consolidés en 149 lignes de "
                    "recommandation (141 en tableaux thématiques + 8 dans la "
                    "classification dédiée du champ 1), par regroupement strict des tags "
                    "IDENTIQUES au sein "
                    "d'un même item clinique (contre-indications ou sous-étapes d'une "
                    "même posologie énoncées dans une seule phrase) — jamais de fusion "
                    "entre tags différents. Les huit formes cliniques de la classification "
                    "opérationnelle de l'EME (champ 1) sont toutes restituées "
                    "individuellement avec leur propre tag, y compris lorsque les tags "
                    "diffèrent au sein de la liste.", S_SOURCE))
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Avertissement :</b> ce document est une fiche de synthèse indépendante, "
        "produite pour un usage d'aide-mémoire. Il reprend l'intégralité des "
        "recommandations du corps du texte, mais ne remplace pas le texte intégral "
        "(argumentaire complet, références bibliographiques, Fig. 1 — diagramme "
        "d'utilisation des médicaments antiépileptiques) et n'est ni édité ni validé par "
        "la SRLF, le GFRUP ou la SFMU. En cas de doute, se référer au texte intégral "
        "et/ou à un avis spécialisé. Ces recommandations, établies début 2008, prévoyaient "
        "explicitement leur propre réactualisation sous trois ans : vérifier l'existence "
        "d'une actualisation plus récente en cas de doute.",
        S_BODY_SM), bg=GREY_LIGHT, border=GREY))
    return story

def _section_1():
    return _section_intro()

def _section_2():
    return _section_champ1()

def _section_3():
    return _section_champ2()

def _section_4():
    return _section_champ3()

def _section_5():
    # Champ 4 (étiologie + pronostic) et Champ 5 (PEC non spécifique) sont fusionnés en
    # une seule section sans saut de page force entre eux : le decoupage precedent (une
    # entree SECTIONS par sous-champ) laissait une page 6 remplie a ~30% (fin de l'enquete
    # etiologique) et une page 8 remplie a ~50% (fin de la PEC non specifique). Densite
    # verifiee apres fusion (voir build()) : gain net de pages sans perte de contenu.
    return (_section_champ4_etio() + [Spacer(1, 3 * mm)] + _section_champ4_pronostic()
            + [Spacer(1, 3 * mm)] + _section_champ5())

def _section_6():
    # Champ 7 schema initial + posologies par molecule : meme logique de fusion - le
    # decoupage precedent laissait une page 10 remplie a ~15% seulement (fin du schema
    # therapeutique, juste 2 lignes de tableau avant le saut de page force).
    return _section_champ7_schema() + [Spacer(1, 3 * mm)] + _section_champ7_posologies()

def _section_7():
    return _section_champ8()

def _section_8():
    return _section_champ9() + [Spacer(1, 4 * mm)] + _section_sources()

SECTIONS = [
    ("Introduction, méthodologie & légende", _section_1),
    ("Champ 1 — Définitions et classification de l'EME", _section_2),
    ("Champ 2 — Diagnostic différentiel", _section_3),
    ("Champ 3 — Place de l'électroencéphalogramme", _section_4),
    ("Champ 4 — Étiologie, pronostic & Champ 5 — PEC non spécifique", _section_5),
    ("Champ 7 — Schéma thérapeutique et posologies", _section_6),
    ("Champ 8 — État de mal épileptique réfractaire", _section_7),
    ("Champ 9 — EME non convulsifs & traçabilité", _section_8),
]

def _make_doc(path=None):
    return SimpleDocTemplate(path or OUT, pagesize=A4,
                              leftMargin=MARGIN, rightMargin=MARGIN,
                              topMargin=32 * mm, bottomMargin=16 * mm,
                              title="Fiche SRLF/GFRUP/SFMU 2009 - États de mal épileptiques",
                              author="Synthèse indépendante (source SRLF/GFRUP/SFMU)")

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
    # Use a throwaway temp path (never OUT) for these measurement-only builds: reusing OUT
    # here was found to corrupt page 1's header_band in the final build (repeated silent
    # builds to the same path as the real output somehow interfered with the last build's
    # first page - reproduced and fixed by isolating counting passes to their own file).
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
