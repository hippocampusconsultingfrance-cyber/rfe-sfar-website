# -*- coding: utf-8 -*-
"""
Fiche de synthese - RFE Sfar/SRLF 2009 "Controle de la glycemie en reanimation et en
anesthesie" ("Glycemic control in intensive care unit and during anaesthesia").
Carole Ichai (coordonnatrice) et al., Ann Fr Anesth Reanim 2009;28:410-415, doi
10.1016/j.annfar.2009.02.020. Disponible en ligne le 27 mars 2009. Recommandations
validees definitivement en juillet 2008. Groupe de travail de 21 experts francophones
(France, Belgique, Suisse), en partenariat avec l'Alfediam, l'Adarpef, le Gefrup, la
Sbar (Societe belge d'anesthesie-reanimation), la SFNEP et la SIZ (Societe de
reanimation belge intensive zorgen). Source : sources/glycemie.pdf (6 pages),
sources/glycemie.txt (texte extrait, ~663 lignes).

METHODOLOGIE - DEUX AXES INDEPENDANTS (pas du GRADE classique 1+/1-/2+/2-/AE) : la
methode Grade a servi de cadre general (qualite des etudes, criteres de jugement,
balance benefice/risque) mais la source imprime, apres CHAQUE recommandation, DEUX
cotations distinctes et independantes :
  - le NGP (Niveau Global de Preuve) : Fort / Modere / Faible - reflete la solidite
    de la litterature sous-tendant la recommandation ;
  - l'Accord : Fort / Faible (+ un cas unique "Indecision") - reflete la force du
    consensus du groupe d'experts, cote de 1 a 9 (mediane) en 3 zones (1-3 desaccord,
    4-6 indecision, 7-9 accord), "fort" si l'intervalle de la mediane reste dans une
    seule zone, "faible" sinon.
Le texte source le dit explicitement (Introduction et methodologie) : "il est possible
d'obtenir un accord fort sur une proposition avec faible NGP et inversement" - les deux
axes sont donc bien decorreles et doivent etre lus independamment, jamais fusionnes en
un seul chip composite. Ce document est la SEULE fiche du corpus a utiliser ce systeme
a deux axes ; toutes les autres fiches SFAR/SRLF de ce corpus utilisent soit un GRADE
1+/1-/2+/2-/AE a un seul axe, soit un simple tag "accord fort" a un seul axe. D'ou une
reco_table() locale a QUATRE colonnes (Theme, Recommandation, NGP, Accord) au lieu des
trois colonnes habituelles (Ref./Theme, Recommandation, Grade OU Accord) utilisees
partout ailleurs dans ce corpus - aucune fiche existante (fiche_ira.py, fiche_ih.py,
fiche_epanchement_pleural.py verifies) n'a de colonnes Grade+Accord simultanees malgre
la suggestion initiale de tache ; ce pattern a deux colonnes de chips est donc concu
ici specifiquement pour ce document.

Extension LOCALE, non invasive, de GRADE_COLORS (meme precedent que fiche_nutrition.py/
fiche_eer.py/fiche_aap_programmee.py) : "Fort" -> vert, "Modere" -> teal (ton
intermediaire), "Faible" -> ambre, "Indecision" -> gris plein, "N/D" -> gris pale
(distinct visuellement de "Indecision" : "N/D" = aucune cotation imprimee du tout dans
la source, ce n'est pas un resultat de vote, cf. anomalie ci-dessous).

DEUX ANOMALIES SOURCE-INTERNES CONFIRMEES PAR LECTURE DIRECTE DU PDF A 250 DPI (page 4
et page 5), disclosees ici telles quelles plutot que resolues silencieusement (meme
principe deja applique dans fiche_aap_programmee.py) :

(1) 74 recommandations au total dans les champs 5-10, mais UNE SEULE n'a AUCUNE
    cotation imprimee : la derniere phrase du champ 7 ("Chez les patients a risque, il
    faut realiser une mesure de glycemie durant le sejour en salle de surveillance
    post-interventionnelle (SSPI).") ne porte ni "(NGP ...)" ni "(accord ...)" - verifie
    par grep exhaustif sur le texte extrait ET par rendu visuel de la page source (page
    4 de l'article, page 5 du PDF) : la phrase se termine bien par un simple point,
    sans aucune parenthese de cotation, contrairement a toutes les 73 autres phrases du
    meme type dans les champs 5-10. Traitee ici comme la 74e recommandation, avec un
    chip "N/D" (gris pale) sur ses deux colonnes NGP et Accord plutot qu'une cotation
    inventee, et une note explicite juste sous le tableau du champ 7.
    Ceci concilie les deux comptages de la source : "74 recommandations" (Introduction,
    §1) et "73 [seulement] ont fait l'objet d'un accord (fort ou faible) et une seule
    est restee en indecision" (73 + 1 = 74) - les 73 recommandations avec un tag
    "accord" au sens strict de la source sont : 72 avec accord fort/faible + 1 avec
    l'unique "accord modere" imprime (anomalie 2 ci-dessous, qui n'est ni "fort" ni
    "faible" au sens strict de la methodologie declaree) + 1 indecision = 74, moins la
    phrase SSPI sans aucune cotation = 73 phrases cotees + 1 phrase non cotee = 74
    recommandations au total, chiffre qui concorde avec celui du resume de la source.

(2) La methodologie (§1) ne definit QUE deux niveaux pour l'axe Accord : "fort" et
    "faible" (formule explicite : "il nous a semble necessaire de fournir ... le NGP").
    Pourtant, une recommandation (champ 8, sous-section "Les apports glucidiques",
    premiere phrase : interruption de l'insuline IV a la reprise d'une alimentation
    orale) porte litteralement le tag "(accord modere)" dans le texte source - un
    niveau non prevu par la methodologie declaree pour cet axe (le niveau "modere"
    n'existe, dans la methodologie, que pour l'axe NGP). Transcrit ici verbatim, sans
    le forcer vers "fort" ou "faible", avec disclosure dans le panneau d'introduction.

Le seul cas d'"indecision" (ni accord ni desaccord) est le champ 8, sous-section "Les
apports glucidiques", 3e recommandation ("... il ne faut probablement pas proscrire
l'apport de glucose [chez le cerebrolese] a condition de controler la glycemie (NGP
faible) (indecision).") - traite avec un chip "Indecision" gris distinct, jamais un
chip Accord standard.

Champs 1-4 (physiologie/physiopathologie) : la source dit explicitement qu'ils "ne
pouvaient pas faire l'objet de recommandations avec de vraies cotations" et sont
"resumes sous forme de points forts elabores par les experts" - traites ici comme un
panneau de synthese compact (points forts), SANS chip NGP/Accord invente.

74/74 recommandations des champs 5-10 verifiees : grep -c "(NGP" sur le texte source
extrait donne 74 occurrences brutes, dont UNE est la simple definition de l'acronyme
dans le paragraphe methodologique ("... le niveau global de preuve (NGP) pour chacune
des recommandations") et non une cotation de recommandation - ce qui ramene a 73 le
nombre de cotations "(NGP xxx)" reellement attachees a une recommandation, plus la
74e recommandation (SSPI) sans aucune cotation imprimee = 74 recommandations au total,
comme detaille en (1) ci-dessus. Aucun chip composite "X/Y" n'est utilise nulle part
(verifie par grep, cf. script de construction) - non pertinent ici de toute facon
puisqu'il n'existe aucune notation GRADE 1+/2+ dans cette source.

Pas d'arrondis Unicode (fleches/exposants/emoji) dans le corps du texte - encodage
Helvetica de cette chaine de production.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from style import *
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.units import mm

# Local, non-invasive extension of the shared GRADE_COLORS dict (safe: this script runs
# as its own process ; mirrors the precedent set in fiche_nutrition.py / fiche_eer.py /
# fiche_aap_programmee.py, each of which locally adds "Fort"/"Faible" entries).
GRADE_COLORS["Fort"] = (GREEN, WHITE)
GRADE_COLORS["Modéré"] = (TEAL, WHITE)
GRADE_COLORS["Faible"] = (AMBER, WHITE)
GRADE_COLORS["Indécision"] = (GREY, WHITE)
GRADE_COLORS["N/D"] = (GREY_LIGHT, GREY)

OUT = "/private/tmp/claude-501/-Users-macbook-Downloads-claude/65498e3e-5ddf-47a6-b100-3ac535d1faa0/scratchpad/rfe_sfar/output/Fiche_SFAR_SRLF_Glycemie_2009.pdf"

SOURCE_TXT = ("Source : Ichai C, et al., Sfar/SRLF (avec Alfediam, Adarpef, Gefrup, Sbar, SFNEP, SIZ) — "
              "« Contrôle de la glycémie en réanimation et en anesthésie » — Recommandations formalisées "
              "d'experts, Ann Fr Anesth Reanim 2009;28:410-415, doi 10.1016/j.annfar.2009.02.020. Validées "
              "juillet 2008. Fiche de synthèse non officielle : se référer au texte intégral.")

def P(txt, style=S_CELL):
    return Paragraph(txt, style)

def chip(label, **kw):
    return grade_chip(label, **kw)

NGP_W = 16 * mm
ACCORD_W = 20 * mm

def reco_table(rows, theme_w, col_widths=None):
    """rows: (theme, text, ngp_label, accord_label) — 'theme' replaces the usual Réf.
    column since this source has no per-recommendation numbering (R1/R2). Two
    independent chip columns (NGP, Accord) — see module docstring for why this fiche
    needs a 4-column pattern not used anywhere else in the corpus."""
    text_w = PAGE_W - 2 * MARGIN - theme_w - NGP_W - ACCORD_W
    cw = col_widths or [theme_w, text_w, NGP_W, ACCORD_W]
    data = [[P("Thème", S_HEAD_W), P("Recommandation (texte intégral)", S_HEAD_W),
              P("NGP", S_HEAD_W_C), P("Accord", S_HEAD_W_C)]]
    for theme, txt, ngp, accord in rows:
        data.append([P(theme, S_CELL_B), P(txt, S_CELL),
                      chip(ngp, width=NGP_W - 2 * mm), chip(accord, width=ACCORD_W - 2 * mm)])
    t = Table(data, colWidths=cw, repeatRows=1)
    style_cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), NAVY), ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTNAME", (0, 0), (-1, 0), FONT_BOLD), ("FONTSIZE", (0, 0), (-1, 0), 8),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ALIGN", (2, 0), (3, -1), "CENTER"),
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
    items = [("Fort", "Fort"), ("Modéré", "Modéré"), ("Faible", "Faible")]
    chip_w = 20 * mm
    content_w = PAGE_W - 2 * MARGIN
    n = len(items)
    text_w = (content_w - n * chip_w) / n
    row_cells, col_widths = [], []
    for g, txt in items:
        row_cells.append(chip(g, width=chip_w - 2 * mm))
        row_cells.append(P(txt, S_BADGE_HEAD))
        col_widths += [chip_w, text_w]
    row = Table([row_cells], colWidths=col_widths)
    row.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                              ("LEFTPADDING", (0, 0), (-1, -1), 1), ("RIGHTPADDING", (0, 0), (-1, -1), 1)]))
    return row

def physio_panel(title, bullets):
    lines = ["<b>%s</b>" % title]
    for b in bullets:
        lines.append("&bull; " + b)
    return P("<br/>".join(lines), S_BODY_SM)

TOTAL_PAGES = {"n": 8}

def on_page(canvas, doc, page_title):
    header_band(canvas, doc, "SFAR / SRLF — RFE 2009 — FICHE DE SYNTHÈSE",
                "Contrôle de la glycémie en réanimation et en anesthésie",
                page_title, icon_fn=lambda c, x, y: icon_drop(c, x, y, 13 * mm), color=TEAL_DARK)
    footer_band(canvas, doc, SOURCE_TXT, f"Page {doc.page} / {TOTAL_PAGES['n']}")

# ---------------------------------------------------------------------------
def _section_intro():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Champ :</b> contrôle de la glycémie chez l'adulte et l'enfant, en réanimation et en "
        "anesthésie-période périopératoire. Recommandations formalisées d'experts (RFE) Sfar/SRLF, "
        "élaborées par un groupe de <b>21 experts francophones</b> (France, Belgique, Suisse) coordonné "
        "par Carole Ichai, en partenariat avec l'Alfediam, l'Adarpef, le Gefrup, la Société belge "
        "d'anesthésie-réanimation (Sbar), la SFNEP et la SIZ. Dix champs d'application ont été répartis "
        "entre les experts. Recommandations validées définitivement en juillet 2008.",
        S_BODY), bg=BG_PANEL, border=TEAL))
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Méthodologie — système à DEUX axes indépendants (spécifique à cette fiche) :</b> la méthode "
        "Grade a servi de cadre général, mais chaque recommandation des champs 5 à 10 porte, dans le "
        "texte source, <b>deux cotations distinctes et indépendantes</b>, à lire séparément :<br/>"
        "&bull; <b>NGP</b> (Niveau Global de Preuve) — Fort / Modéré / Faible — solidité de la "
        "littérature sous-jacente ;<br/>"
        "&bull; <b>Accord</b> — Fort / Faible (+ un cas unique « Indécision ») — force du consensus des "
        "experts, coté de 1 à 9 par vote (médiane), 3 zones : 1-3 désaccord, 4-6 indécision, 7-9 accord ; "
        "« fort » si l'intervalle de la médiane reste dans une seule zone, « faible » sinon.<br/>"
        "La source le précise explicitement : « il est possible d'obtenir un accord fort sur une "
        "proposition avec faible NGP et inversement ». Les deux chips ci-dessous ne doivent donc "
        "<b>jamais</b> être fusionnés en un seul.<br/><br/>"
        "Les <b>quatre premiers champs</b> (physiologie/physiopathologie du glucose et de l'insuline) "
        "\"ne pouvaient pas faire l'objet de recommandations avec de vraies cotations\" (dixit la source) "
        "et sont résumés en points forts, sans chip NGP/Accord. Les <b>six derniers champs</b> ont produit "
        "74 recommandations formellement cotées.",
        S_BODY_SM), bg=BG_PANEL, border=TEAL))
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Disclosure — deux anomalies source confirmées par lecture directe du PDF (250 dpi) :</b><br/>"
        "(1) Sur les 74 recommandations des champs 5-10, une seule (dernière phrase du champ 7, à propos "
        "de la mesure de glycémie en SSPI) ne porte <b>aucune</b> cotation imprimée dans le texte source — "
        "ni NGP ni Accord. Traitée ici avec un chip neutre « N/D » sur ses deux colonnes plutôt qu'une "
        "cotation inventée (voir note sous le tableau du champ 7).<br/>"
        "(2) La méthodologie ne définit que « fort »/« faible » pour l'axe Accord — pourtant une "
        "recommandation (champ 8, apports glucidiques, 1re phrase) porte littéralement le "
        "tag « (accord modéré) », niveau non prévu par la méthodologie déclarée pour cet axe. Transcrit "
        "verbatim, sans le forcer vers fort/faible.<br/>"
        "Ces deux constats sont disclosés tels quels, sans résolution silencieuse (même principe déjà "
        "appliqué ailleurs dans ce corpus).",
        S_BODY_SM), bg=AMBER_LIGHT, border=AMBER))
    story.append(Spacer(1, 3 * mm))

    story.append(section_bar("Légende — NGP et Accord (deux axes indépendants)"))
    story.append(Spacer(1, 2 * mm))
    story.append(legend_flowable())
    story.append(Spacer(1, 1.5 * mm))
    row2 = Table([[chip("Indécision", width=20 * mm - 2 * mm),
                   P("Cas unique (1/74) où le vote des experts n'a atteint ni l'accord ni le désaccord — "
                     "champ 8, apports glucidiques.", S_BADGE_HEAD),
                   chip("N/D", width=20 * mm - 2 * mm),
                   P("Recommandation sans aucune cotation imprimée dans la source (anomalie 1 "
                     "ci-dessus) — pas un résultat de vote.", S_BADGE_HEAD)]],
                  colWidths=[20 * mm, 66 * mm, 20 * mm, 66 * mm])
    row2.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                               ("LEFTPADDING", (0, 0), (-1, -1), 1), ("RIGHTPADDING", (0, 0), (-1, -1), 1)]))
    story.append(row2)
    return story

def _section_physio():
    story = []
    story.append(Spacer(1, 2 * mm))
    story.append(section_bar("Champs 1 à 4 — Notions de physiologie et de physiopathologie : les points forts"))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<i>Le groupe d'experts a jugé que ces quatre champs ne pouvaient pas faire l'objet de "
        "recommandations avec de vraies cotations ; ils sont résumés ci-dessous sous forme de points "
        "forts, sans chip NGP/Accord.</i>", S_NOTE))
    story.append(Spacer(1, 2 * mm))

    p1 = physio_panel("Champ 1 — Métabolisme du glucose en situation physiologique", [
        "Glycémie normale ~5 mmol/l (0,8 g/l), hors postprandial immédiat ; toute variation traduit un "
        "déséquilibre entrée/utilisation tissulaire du glucose.",
        "Transporteurs GLUT4 (insulino-dépendants : muscle, cœur, adipocytes) vs autres GLUT "
        "(non-insulino-dépendants).",
        "Régulation par l'insuline et les hormones de contre-régulation (glucagon, adrénaline, GH, "
        "cortisol), le GLP-1/GIP digestifs et le système nerveux central.",
        "Jeûne court : baisse insuline, hormones de stress maintiennent la production hépatique de "
        "glucose ; alimentation : hausse insuline, stockage.",
        "Hypoglycémie : réponse hormonale hiérarchisée — arrêt de la sécrétion d'insuline &lt; 4,4 "
        "mmol/l ; glucagon/adrénaline/GH &lt; 3,7 mmol/l ; cortisol &lt; 3,1 mmol/l.",
    ])
    p2 = physio_panel("Champ 2 — Métabolisme du glucose en situation pathologique aiguë", [
        "Hyperglycémie de stress (« diabète de stress ») : hormones de contre-régulation et médiateurs "
        "de l'inflammation, puis insulinorésistance et baisse de la sécrétion pancréatique d'insuline.",
        "Cercle d'auto-aggravation entre hyperglycémie et inflammation.",
        "Insulinorésistance hépatique (néoglucogenèse/glycogénolyse accrues) et périphérique "
        "(muscle, adipocytes : baisse de l'utilisation du glucose).",
        "Résultat : pénétration accrue de glucose dans les tissus non-insulino-dépendants (cellules "
        "immunitaires, inflammatoires, tissus lésés).",
        "Sepsis/hypoxie : anomalies mitochondriales déviant la glycolyse (lactate, shunt des pentoses, "
        "voies des hexosamines/polyols) ; HIF-1 impliqué lors de l'hypoxie.",
    ])
    p3 = physio_panel("Champ 3 — Les effets du glucose : de la cellule à l'organisme entier", [
        "Substrat énergétique (glycolyse puis cycle de Krebs, ATP) ; capacité maximale d'oxydation "
        "2 à 4 mg/kg/min.",
        "En situation critique, la perfusion de glucose ne freine que partiellement la production "
        "endogène : risque d'hyperglycémie si l'apport dépasse 2 à 3 mg/kg/min.",
        "Rendement énergétique : 4 kcal/g pour le glucose contre 9 kcal/g pour les lipides ; mais le "
        "glucose devient le substrat le plus rentable en hypoxie (dette en O2).",
        "Hyperglycémie aiguë : adaptative au début mais toxique si prolongée — effet pro-inflammatoire "
        "(cellules immunes, endothéliales, hépatocytes), stress oxydant.",
    ])
    p4 = physio_panel("Champ 4 — Les effets de l'insuline : de la cellule à l'organisme entier", [
        "Hormone protéique (cellules bêta des îlots de Langerhans), essentielle à l'homéostasie du "
        "glucose ; inhibe la production hépatique de glucose et la lipolyse.",
        "Deux voies de signalisation : MAPK (croissance) et IRS/PI-3 kinase (métabolique) ; "
        "l'inflammation et les acides gras libres favorisent l'insulinorésistance (IRS, TLR4/NF-kB).",
        "Effets pléiotropes : anti-inflammatoire, vasodilatateur (eNOS/NO), inotrope positif ; en "
        "réanimation, l'insulinothérapie à forte dose améliore la fonction rénale.",
        "Effets essentiels sur le cerveau, notamment pour sa croissance.",
    ])
    row1 = Table([[p1, p2]], colWidths=[(PAGE_W - 2 * MARGIN - 4 * mm) / 2.0] * 2)
    row1.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"),
                               ("BACKGROUND", (0, 0), (-1, -1), BG_PANEL),
                               ("BOX", (0, 0), (0, 0), 0.8, TEAL), ("BOX", (1, 0), (1, 0), 0.8, TEAL),
                               ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
                               ("LEFTPADDING", (0, 0), (-1, -1), 3.5), ("RIGHTPADDING", (0, 0), (-1, -1), 3.5)]))
    row2 = Table([[p3, p4]], colWidths=[(PAGE_W - 2 * MARGIN - 4 * mm) / 2.0] * 2)
    row2.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"),
                               ("BACKGROUND", (0, 0), (-1, -1), BG_PANEL),
                               ("BOX", (0, 0), (0, 0), 0.8, TEAL), ("BOX", (1, 0), (1, 0), 0.8, TEAL),
                               ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
                               ("LEFTPADDING", (0, 0), (-1, -1), 3.5), ("RIGHTPADDING", (0, 0), (-1, -1), 3.5)]))
    story.append(row1)
    story.append(Spacer(1, 2 * mm))
    story.append(row2)
    return story

# ---------------------------------------------------------------------------
def _section_champ5():
    story = []
    story.append(Spacer(1, 2 * mm))
    story.append(section_bar("Champ 5 — L'hypoglycémie : diagnostic et risques"))
    story.append(Spacer(1, 2 * mm))
    story.append(reco_table([
            ("Seuil hypoglycémie", "Chez les patients de réanimation, il faut probablement un seuil "
             "glycémique inférieur à 3,3 mmol/l (0,6 g/l) pour définir une hypoglycémie.", "Faible", "Faible"),
            ("Seuil hypoglycémie sévère", "Chez les patients de réanimation, il faut probablement un "
             "seuil glycémique inférieur à 2,2 mmol/l (0,4 g/l) pour définir une hypoglycémie sévère.",
             "Faible", "Fort"),
            ("Durée prolongée", "Par analogie avec le patient diabétique, il est probable que le "
             "caractère prolongé d'une hypoglycémie se définisse pour une durée de plus de deux heures.",
             "Faible", "Faible"),
            ("Contrôle strict — incidence", "Il est possible que l'application de stratégies publiées de "
             "contrôle glycémique strict expose à une augmentation de l'incidence des hypoglycémies "
             "sévères.", "Fort", "Fort"),
            ("Contrôle strict — durée", "Il est possible que l'application de stratégies publiées de "
             "contrôle glycémique strict expose à une augmentation de la durée des hypoglycémies sévères.",
             "Fort", "Fort"),
            ("Risque cérébral", "Une hypoglycémie sévère et prolongée peut induire des lésions "
             "cérébrales irréversibles.", "Fort", "Fort"),
            ("Dépistage clinique insuffisant", "Chez les patients de réanimation ne pouvant pas "
             "s'exprimer, il ne faut pas se baser uniquement sur les signes cliniques évocateurs pour "
             "dépister les épisodes d'hypoglycémies.", "Fort", "Fort"),
            ("Surmortalité", "Il est probable que la survenue d'une hypoglycémie sévère soit associée à "
             "un risque de surmortalité, sans lien démontré de causalité entre les deux.", "Modéré", "Faible"),
            ("Recharge en glucose", "Il est possible que les lésions neurologiques observées au décours "
             "des hypoglycémies soient en partie liées à la recharge excessive en glucose.", "Faible", "Fort"),
            ("Surveillance rapprochée", "Dans le cadre d'une stratégie de contrôle glycémique strict, il "
             "faut réaliser une surveillance rapprochée des mesures de glycémie pour le dépistage précoce "
             "des hypoglycémies sévères.", "Fort", "Fort"),
            ("Choix du prélèvement", "Chez les patients de réanimation chez qui on suspecte une "
             "hypoglycémie, l'utilisation d'échantillons artériels ou veineux est plus appropriée que "
             "celle réalisée sur l'échantillon capillaire qui surestime le plus souvent la valeur de la "
             "glycémie.", "Fort", "Fort"),
        ], theme_w=30 * mm))
    return story

def _section_champ6():
    story = []
    story.append(Spacer(1, 2 * mm))
    story.append(section_bar("Champ 6 — Le contrôle glycémique en réanimation"))
    story.append(Spacer(1, 2 * mm))
    story.append(reco_table([
            ("Cible < 6,1 mmol/l — adultes", "Il faut probablement exercer un contrôle du niveau "
             "glycémique avec une cible inférieur à 6,1 mmol/l (1,1 g/l) chez les patients adultes en "
             "réanimation car ce contrôle permet de diminuer les complications pendant l'hospitalisation.",
             "Fort", "Faible"),
            ("Contrôle strict — chirurgicaux", "Il faut exercer un contrôle strict de la glycémie "
             "(&lt; 6,1 mmol/l ou 1,1 g/l) chez les patients adultes chirurgicaux en réanimation.",
             "Fort", "Faible"),
            ("Chirurgie cardiaque", "Il faut maintenir une glycémie inférieure à 6,1 mmol/l (1,1 g/l) "
             "chez les patients de chirurgie cardiaque en réanimation.", "Fort", "Faible"),
            ("Contrôle strict en urgence", "Il n'est pas raisonnable de recommander un contrôle strict "
             "de la glycémie en urgence.", "Faible", "Fort"),
            ("Variations glycémiques", "En réanimation, il faut probablement éviter les variations "
             "glycémiques trop importantes.", "Faible", "Fort"),
            ("Voie d'administration", "En dehors de l'insuline intraveineuse, il n'est pas possible "
             "d'utiliser d'autres moyens pour le contrôle glycémique en réanimation.", "Fort", "Faible"),
            ("Perfusion GIK", "La perfusion de glucose-insuline-potassium (GIK), n'a probablement pas "
             "d'effet bénéfique si le niveau glycémique n'est pas contrôlé.", "Fort", "Faible"),
        ], theme_w=32 * mm))
    return story

def _section_champ7():
    story = []
    story.append(Spacer(1, 2 * mm))
    story.append(section_bar("Champ 7 — Le contrôle glycémique en périopératoire"))
    story.append(Spacer(1, 2 * mm))
    story.append(reco_table([
            ("Insulinorésistance périop.", "L'insulinorésistance, cause principale de l'hyperglycémie "
             "périopératoire, peut apparaître dans les premières heures de l'intervention et se prolonger "
             "au moins deux à trois semaines en postopératoire.", "Fort", "Faible"),
            ("Insuline exogène", "Il est possible de diminuer l'hyperglycémie périopératoire induite par "
             "l'insulinorésistance en apportant de l'insuline exogène durant cette période.", "Fort", "Faible"),
            ("Durée de séjour", "Il est possible de diminuer la durée de séjour postopératoire en "
             "limitant l'insulinorésistance périopératoire avec maintien d'une normoglycémie.", "Fort", "Faible"),
            ("Facteurs aggravants", "Il faut lutter contre l'hypothermie, les pertes sanguines, "
             "l'agression chirurgicale intense qui accentuent l'insulinorésistance périopératoire.",
             "Modéré", "Fort"),
            ("Réhabilitation précoce", "Il faut favoriser la réhabilitation postopératoire précoce de "
             "façon à limiter l'insulinorésistance postopératoire.", "Modéré", "Fort"),
            ("Jeûne glucidique", "Le jeûne glucidique préopératoire de plus de 12 heures aggrave "
             "l'insulinorésistance périopératoire. Il faut le limiter, quand cela est possible, en "
             "autorisant les liquides clairs jusqu'à deux à trois heures préopératoires.", "Modéré", "Fort"),
            ("Apport HC préopératoire", "En dehors des patients à estomac plein (occlusion, grossesse, "
             "diabète, etc.), l'apport d'hydrates de carbone en préopératoire (100 g la veille et 50 g "
             "trois heures avant l'intervention) peut être recommandé afin de limiter l'insulinorésistance "
             "périopératoire.", "Modéré", "Fort"),
            ("HC peropératoire", "En dehors des patients diabétiques et des nourrissons, il ne faut "
             "probablement pas administrer d'hydrates de carbone en peropératoire.", "Faible", "Faible"),
            ("Chirurgie à risque", "Au cours de la chirurgie à risque (cardiovasculaire, obèse, âgé, "
             "chirurgie de longue durée ou urgente), il faut probablement éviter l'hyperglycémie "
             "supérieure à 10 mmol/l (1,8 g/l).", "Faible", "Fort"),
            ("Voie IV peropératoire", "L'insulinothérapie peropératoire doit être intraveineuse continue "
             "et impose un contrôle glycémique toutes les 30 minutes.", "Fort", "Faible"),
            ("Cibles adaptées", "Il faut adapter les valeurs cibles de glycémie périopératoire aux "
             "ressources disponibles et à l'expérience de l'unité en charge du patient, en privilégiant "
             "des niveaux d'exigences croissants.", "Fort", "Faible"),
            ("Mesure peropératoire", "Il faut probablement mesurer la glycémie peropératoire au cours "
             "des interventions à risque.", "Faible", "Fort"),
            ("Mesure en SSPI", "Chez les patients à risque, il faut réaliser une mesure de glycémie "
             "durant le séjour en salle de surveillance post-interventionnelle (SSPI).", "N/D", "N/D"),
        ], theme_w=32 * mm))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P("<i>Note — « Mesure en SSPI » : cette phrase, formulée comme une recommandation (« il faut »), "
          "ne porte aucune cotation NGP/Accord dans le texte source (vérifié par lecture directe du PDF "
          "à 250 dpi) — chip « N/D » plutôt qu'une cotation inventée. Voir disclosure en page 1.</i>",
          S_NOTE))
    return story

def _section_champ8():
    story = []
    story.append(Spacer(1, 2 * mm))
    story.append(KeepTogether([
        section_bar("Champ 8 — Réalisation pratique du contrôle glycémique"),
        Spacer(1, 1.5 * mm),
        P("<b>6.1. Les apports glucidiques</b>", S_H2),
    ]))
    story.append(Spacer(1, 1.5 * mm))
    story.append(reco_table([
            ("Arrêt insuline IV / relais", "L'insuline intraveineuse à la seringue électrique doit "
             "probablement être interrompue lorsque le patient a repris une alimentation orale et la "
             "surveillance glycémique doit être poursuivie par au moins trois contrôles préprandiaux.",
             "Faible", "Modéré"),
            ("Apports maximaux", "Durant la phase aiguë, la quantité maximale de glucose intraveineux "
             "ne doit pas dépasser 100 g/24 h ; la quantité totale d'hydrates de carbone (entérale et "
             "parentérale) ne doit pas dépasser 200 g/24 h.", "Faible", "Fort"),
            ("Glucose chez le cérébrolésé", "Durant la phase aiguë, chez tous les patients et y compris "
             "chez le cérébrolésé, il ne faut probablement pas proscrire l'apport de glucose à condition "
             "de contrôler la glycémie.", "Faible", "Indécision"),
            ("Adaptation nutrition/insuline", "Il est possible que l'adaptation combinée du débit "
             "d'infusion de la nutrition entérale et du débit de perfusion d'insuline puisse améliorer "
             "l'observance de la cible glycémique.", "Faible", "Faible"),
        ], theme_w=32 * mm))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<i>Note — « Arrêt insuline IV / relais » : le tag « (accord modéré) » est imprimé tel quel dans "
        "la source, alors que la méthodologie ne définit que « fort »/« faible » pour l'axe Accord — "
        "anomalie disclosée en page 1, non résolue silencieusement.</i>", S_NOTE))
    story.append(Spacer(1, 2 * mm))

    story.append(KeepTogether([
        P("<b>6.2. Les modalités de surveillance</b>", S_H2),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
            ("Référence laboratoire", "Il faut considérer que la glycémie mesurée au laboratoire est "
             "actuellement la valeur de référence.", "Fort", "Fort"),
            ("Ordre des prélèvements", "Il faut probablement privilégier dans l'ordre, le prélèvement "
             "artériel, puis veineux, puis capillaire.", "Fort", "Fort"),
            ("Sang total vs plasma", "Du fait des différences de valeur entre sang total et plasma, il "
             "faut connaître les caractéristiques précises du lecteur de glycémie que l'on utilise (seuls "
             "certains appliquent directement le facteur de correction).", "Fort", "Fort"),
            ("Interférences physicochimiques", "Du fait de nombreuses interférences physicochimiques "
             "endogènes et exogènes, il faut connaître les caractéristiques précises du lecteur de "
             "glycémie et des bandelettes que l'on utilise.", "Fort", "Fort"),
        ], theme_w=32 * mm))
    return story

def _section_champ8b():
    story = []
    story.append(Spacer(1, 2 * mm))
    story.append(KeepTogether([
        P("<b>6.3. Algorithmes et protocoles</b>", S_H2),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
            ("Protocole unique d'équipe", "Au sein d'une équipe, il faut choisir le même protocole "
             "formalisé de contrôle glycémique.", "Fort", "Fort"),
            ("Insuline rapide obligatoire", "Tout protocole de contrôle glycémique strict doit inclure au "
             "minimum des recommandations relatives à l'utilisation d'une insuline d'action rapide en "
             "perfusion continue à la seringue électrique.", "Fort", "Fort"),
            ("Procédures anti-hypoglycémie", "Tout protocole de contrôle glycémique strict doit inclure "
             "au minimum des procédures de correction et de surveillance des épisodes d'hypoglycémie.",
             "Fort", "Fort"),
            ("Voie à débit constant", "Il faut probablement privilégier l'utilisation d'une voie "
             "permettant d'assurer un débit constant pour administrer l'insuline intraveineuse en "
             "continu.", "Modéré", "Fort"),
            ("Pas de protocole supérieur", "Parmi les différents protocoles de contrôle glycémique "
             "strict existants, il est impossible d'en privilégier un par rapport aux autres.",
             "Fort", "Faible"),
            ("Abandon des protocoles statiques", "Il faut abandonner les protocoles de contrôle "
             "glycémique statiques qui déterminent le débit d'insuline uniquement à partir de la glycémie "
             "la plus récente.", "Modéré", "Fort"),
            ("Prise en compte des apports HC", "Tout protocole de contrôle glycémique devrait prendre en "
             "compte les apports d'hydrate de carbone pour la détermination du débit d'insuline.",
             "Modéré", "Fort"),
            ("Protocole informatisé", "Un protocole de contrôle glycémique strict basé sur plus de deux "
             "paramètres d'entrée et de sortie devrait être géré par un logiciel informatique.",
             "Modéré", "Faible"),
            ("Charge de travail paramédical", "L'augmentation de charge de travail paramédical doit être "
             "prise en compte lors de la mise en œuvre d'un protocole de contrôle glycémique strict.",
             "Fort", "Fort"),
            ("Formation du personnel", "Il faut prévoir un temps de formation du personnel soignant pour "
             "mettre en route un protocole de contrôle glycémique.", "Fort", "Fort"),
            ("Critères d'efficacité", "L'efficacité d'un protocole de contrôle glycémique strict doit "
             "reposer sur l'ensemble des critères suivants : temps de formation, performance du contrôle, "
             "risque d'hypoglycémie sévère, taux moyen d'erreur, charge en soins infirmiers.",
             "Modéré", "Faible"),
            ("Paramètres d'évaluation", "Il est souhaitable d'évaluer l'efficacité d'un protocole de "
             "contrôle glycémique strict par les principaux paramètres suivants : pourcentage de temps "
             "passé dans la cible glycémique et au dessus de cette cible, index d'hyperglycémie, "
             "variabilité de la glycémie.", "Faible", "Faible"),
        ], theme_w=32 * mm))
    return story

def _section_champ9():
    story = []
    story.append(Spacer(1, 2 * mm))
    story.append(section_bar("Champ 9 — Les spécificités du patient diabétique"))
    story.append(Spacer(1, 2 * mm))
    story.append(reco_table([
            ("Surveillance systématique", "La glycémie doit être surveillée régulièrement chez tout "
             "patient diabétique admis en réanimation.", "Fort", "Fort"),
            ("Impact du contrôle strict", "Chez le patient diabétique admis en réanimation, l'impact "
             "d'un contrôle strict de la glycémie (4,4-6,1 mmol/l ou 0,8-1,1 g/l) sur la morbimortalité "
             "n'est pas démontré.", "Modéré", "Fort"),
            ("Seuil de traitement", "Il est indispensable de proposer un traitement de l'hyperglycémie "
             "pour tout patient diabétique admis en réanimation dont la glycémie est supérieure à "
             "10 mmol/l (1,8 g/l). Entre 8,3 et 10 mmol/l (1,5 et 1,8 g/l), un tel traitement apparaît "
             "souhaitable bien que le bénéfice ne soit pas totalement établi.", "Modéré", "Fort"),
            ("Objectif non défini", "L'objectif de traitement de l'hyperglycémie des patients diabétiques "
             "admis en réanimation n'est pas formellement défini. Néanmoins, des valeurs de glycémie "
             "inférieures à 6,1 mmol/l (1,1 g/l) et supérieures ou égales à 8,3 mmol/l (1,5 g/l) semblent "
             "délétères et doivent être évitées.", "Faible", "Faible"),
            ("Cible péri-opératoire", "En peropératoire, il faut probablement maintenir un niveau "
             "glycémique inférieur à 8,3 mmol/l (1,5 g/l) chez les patients diabétiques. En postopératoire, "
             "il semble souhaitable de maintenir cet objectif de traitement pendant trois jours (en "
             "l'absence de complications).", "Modéré", "Faible"),
            ("Insuline IV selon contexte", "Chez le patient diabétique, il faut choisir l'insuline en "
             "perfusion intraveineuse continue pour contrôler la glycémie en cas de déséquilibre "
             "préopératoire, ainsi qu'en périopératoire d'une chirurgie majeure ou réalisée en urgence, ou "
             "en cas d'admission postopératoire en réanimation. Il ne faut probablement pas modifier "
             "l'insulinothérapie périopératoire du patient diabétique bien équilibré bénéficiant d'une "
             "chirurgie mineure sous réserve de la mise en place d'une perfusion de sérum glucosé pendant "
             "et après l'intervention avec surveillance glycémique rapprochée.", "Fort", "Fort"),
            ("Reprise des antidiabétiques oraux", "Pour les patients diabétiques traités antérieurement "
             "par des antidiabétiques oraux, la reprise orale du traitement doit être réévaluée après la "
             "phase aiguë de réanimation, en respectant les contre-indications de ces médicaments.",
             "Fort", "Fort"),
            ("Insuline antérieure jamais interrompue", "Pour les patients diabétiques traités "
             "antérieurement par insuline, il est impératif de ne jamais interrompre ce traitement sauf "
             "si l'arrêt est transitoire et justifié par une hypoglycémie.", "Fort", "Faible"),
            ("Dépistage post-hyperglycémie", "Les patients admis en réanimation avec une hyperglycémie "
             "persistante, mais sans notion de diabète, devraient bénéficier d'une évaluation métabolique "
             "ultérieure et si possible avant la sortie de l'hôpital. Cette évaluation pourrait inclure "
             "une glycémie à jeun et une mesure de l'hémoglobine A1c. Une hyperglycémie provoquée par voie "
             "orale peut être utile dans certains cas.", "Modéré", "Faible"),
            ("Sortie de réanimation", "À la sortie de la réanimation et avant la sortie de l'hôpital, une "
             "prise en charge optimale du contrôle glycémique doit probablement être proposée pour les "
             "patients diabétiques, nouveaux diagnostiqués ou insulinorésistants.", "Faible", "Faible"),
        ], theme_w=34 * mm))
    return story

def _section_champ10():
    story = []
    story.append(Spacer(1, 2 * mm))
    story.append(section_bar("Champ 10 — Les spécificités en pédiatrie"))
    story.append(Spacer(1, 2 * mm))
    story.append(reco_table([
            ("Risque accru — jeune enfant", "Le risque d'hypoglycémie est d'autant plus important que "
             "l'enfant est jeune et que la période de jeûne se prolonge.", "Fort", "Fort"),
            ("Signes d'alerte", "Il faut rechercher les signes d'alerte d'hypoglycémie, difficiles à "
             "détecter chez le jeune enfant incapable d'exprimer une sensation de malaise.", "Fort", "Faible"),
            ("Développement cérébral", "La survenue d'hypoglycémies sévères et récidivantes chez le "
             "jeune enfant peut altérer définitivement le développement cérébral et psychomoteur.",
             "Modéré", "Fort"),
            ("Traitement — bolus IV", "Le traitement des hypoglycémies en réanimation ou en période "
             "périopératoire repose sur l'administration intraveineuse d'un bolus de 2 à 5 mg/kg de "
             "soluté glucosé à 10 % (0,2 à 0,5 g/kg), renouvelable selon le contrôle effectué 30 minutes "
             "plus tard.", "Faible", "Faible"),
            ("Besoins de base", "Les besoins de base en glucose sont deux à trois fois plus importants "
             "chez le nourrisson (5-8 mg/kg par minute) que chez l'adulte.", "Fort", "Fort"),
            ("Mesure systématique", "Il faut réaliser une mesure de la glycémie dès l'admission et au "
             "moins une fois par jour pendant la phase aiguë en réanimation chez l'enfant, même en "
             "l'absence d'insulinothérapie.", "Fort", "Fort"),
            ("Alimentation parentérale", "Chez l'enfant, une alimentation parentérale ne doit pas être "
             "brutalement interrompue.", "Faible", "Faible"),
            ("Pas de contrôle strict", "Il n'est pas possible actuellement de recommander en pédiatrie "
             "une stratégie de contrôle glycémique strict par insulinothérapie en réanimation ou en "
             "période périopératoire.", "Modéré", "Fort"),
            ("Mesure chez le nourrisson", "Chez le nourrisson, en cas de jeûne prolongé (plus de quatre "
             "heures) ou de chirurgie longue (plus d'une heure), une mesure de la glycémie peropératoire "
             "doit être faite.", "Faible", "Fort"),
            ("Apports hydroélectrolytiques", "Les apports hydroélectrolytiques du nourrisson au cours "
             "d'une chirurgie longue doivent être basés sur la perfusion de solutions contenant du NaCl "
             "(0,7-0,8 %) et du glucose (1-2,5 %).", "Modéré", "Faible"),
            ("Solutions avec ions", "Il ne faut jamais prescrire de solutions glucosés sans ions chez le "
             "nourrisson et l'enfant, quel que soit l'âge, en raison du risque d'encéphalopathie "
             "hyponatrémique potentiellement létal.", "Fort", "Fort"),
            ("Posologie / absence de modèle", "En situation aiguë, les posologies d'insuline à action "
             "rapide en perfusion intraveineuse varient de 0,02 à 0,15 UI/kg par heure. Il n'est "
             "actuellement pas possible de recommander un modèle de protocole et de seuil glycémique "
             "cible en pédiatrie.", "Faible", "Fort"),
            ("Acidocétose diabétique", "L'acidocétose diabétique doit être prise en charge en tenant "
             "compte d'un risque particulièrement important de survenue d'œdème cérébral.", "Modéré", "Faible"),
        ], theme_w=34 * mm))
    return story

def _section_sources():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("Sources et traçabilité", color=GREY))
    story.append(Spacer(1, 2 * mm))
    story.append(P(
        "<b>Document source :</b> « Contrôle de la glycémie en réanimation et en anesthésie » — "
        "Recommandations formalisées d'experts, Société française d'anesthésie et de réanimation (Sfar) "
        "et Société de réanimation de langue française (SRLF), en partenariat avec l'Alfediam, l'Adarpef, "
        "le Gefrup, la Sbar (Société belge d'anesthésie-réanimation), la SFNEP et la SIZ. Coordonnatrice : "
        "Carole Ichai. Comités des référentiels : Marc Léone, Benoît Veber (Sfar) ; Alain Cariou, Didier "
        "Barnoud (SRLF). 21 experts (France, Belgique, Suisse). Ann Fr Anesth Reanim 2009;28:410-415.",
        S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P("<b>Publication :</b> doi 10.1016/j.annfar.2009.02.020, disponible en ligne le 27 mars "
                    "2009. Recommandations validées définitivement en juillet 2008.", S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P("<b>Méthodologie :</b> méthode Grade adaptée à deux axes indépendants (NGP et Accord, "
                    "voir légende page 1) ; cotation du consensus par vote gradué de 1 à 9 (médiane, 3 "
                    "zones). Champs 1-4 : points forts non cotés. Champs 5-10 : 74 recommandations, dont "
                    "73 portent une cotation NGP + Accord (ou Indécision pour 1 d'entre elles) et 1 "
                    "(mesure en SSPI, champ 7) ne porte aucune cotation imprimée — voir disclosure page 1.",
                    S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P("<b>Couverture :</b> cette fiche reprend l'intégralité des 74 recommandations des "
                    "champs 5 à 10 (transcription verbatim, sans paraphrase), ainsi qu'une synthèse "
                    "compacte des points forts de physiologie/physiopathologie des champs 1 à 4.",
                    S_SOURCE))
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Avertissement :</b> ce document est une fiche de synthèse indépendante, produite pour un "
        "usage d'aide-mémoire. Il reprend l'intégralité des recommandations cotées du texte source, mais "
        "ne remplace pas le texte intégral (argumentaire complet, références bibliographiques) et n'est "
        "ni édité ni validé par la Sfar, la SRLF ou les sociétés partenaires. En cas de doute, se référer "
        "au texte intégral et/ou à un avis spécialisé. Document de 2009 : vérifier l'existence d'une "
        "actualisation plus récente en cas de doute (les cibles glycémiques en réanimation ont notamment "
        "évolué depuis dans la littérature).",
        S_BODY_SM), bg=GREY_LIGHT, border=GREY))
    return story

# ---------------------------------------------------------------------------
# Density note: these three combinator functions each merge several champs into ONE
# SECTIONS entry (no PageBreak inserted between the champs they contain — only between
# entries in SECTIONS itself, via _build_upto). This was tightened after the first build
# (7 SECTIONS entries, one per champ/group) produced 10 pages with several pages only
# ~55% full and one page (avertissement alone) ~15% full: every SECTIONS entry always
# starts on a fresh page regardless of how much room was left on the previous one, so a
# short champ (7-13 short rows) stranded on its own page wasted roughly half of it. Also
# removed the outer KeepTogether() that previously wrapped each ENTIRE multi-row
# reco_table as one atomic block (kept only around small heading+spacer pairs) — that
# atomic wrapping was forcing whole 12-20-row tables to jump to a fresh page instead of
# splitting at a row boundary with their header repeating (repeatRows=1 already handles
# that natively). Combining both fixes: 10 pages -> rebuilt and re-verified below.
def _section_A():
    return (_section_intro() + [Spacer(1, 3 * mm)] + _section_physio()
            + [Spacer(1, 3 * mm)] + _section_champ5())

def _section_B():
    return (_section_champ6() + [Spacer(1, 3 * mm)] + _section_champ7()
            + [Spacer(1, 3 * mm)] + _section_champ8() + [Spacer(1, 3 * mm)] + _section_champ8b())

def _section_C():
    return _section_champ9() + [Spacer(1, 3 * mm)] + _section_champ10() + [Spacer(1, 4 * mm)] + _section_sources()

SECTIONS = [
    ("Introduction, méthodologie, physiologie & Champ 5", _section_A),
    ("Champs 6-8 — Contrôle glycémique & réalisation pratique", _section_B),
    ("Champs 9-10 — Diabète, pédiatrie & traçabilité", _section_C),
]

def _make_doc(path=None):
    return SimpleDocTemplate(path or OUT, pagesize=A4,
                              leftMargin=MARGIN, rightMargin=MARGIN,
                              topMargin=32 * mm, bottomMargin=16 * mm,
                              title="Fiche Sfar/SRLF 2009 - Contrôle de la glycémie en réanimation et en anesthésie",
                              author="Synthèse indépendante (source Sfar/SRLF)")

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
    # first page — reproduced and fixed by isolating counting passes to their own file).
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
