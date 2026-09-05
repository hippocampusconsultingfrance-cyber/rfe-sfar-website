# -*- coding: utf-8 -*-
"""
Fiche de synthese - RFE GIHP, en collaboration avec la SFAR, la SFTH et la SFMV (2024)
"Prevention de la maladie thromboembolique veineuse peri-operatoire" - actualisation des
recommandations SFAR de 2011. Texte valide SFAR (30.04.2024), SFTH (23.02.24), SFVM (janvier
2024). Endosse par la SFCD (02/2024), la SFPT (05/2024) et le reseau INNOVTE (12/2023).
Source verifiee : sources/mtev_perioperatoire.pdf (79 pages), texte extrait
sources/mtev_perioperatoire.txt (~251 000 caracteres), integralement lu ligne a ligne (1-3934).

METHODOLOGIE : GRADE, format PICO. Niveau de preuve fort -> recommandation FORTE (GRADE
1+/1-) ; niveau modere/faible -> recommandation OPTIONNELLE (GRADE 2+/2-) ; litterature
insuffisante -> AVIS D'EXPERTS (AE). Validation par vote (n=37) : accord "fort" si >=70% pour
et <20% contre ; sinon reformulation et nouveau vote.

PARTICULARITE DE CE DOCUMENT (verifiee par grep exhaustif sur l'extraction texte complete,
motifs "^Fort *$" et "^Faible *$") : contrairement a plusieurs autres fiches du corpus (ex.
fiche_ira.py, R2.1 = seule exception a "Accord Fort"), CE document ne comporte AUCUNE occurrence
de "Faible" comme valeur d'accord nulle part dans les 79 pages - les 77 recommandations
graduees retrouvees portent TOUTES la mention d'accord "Fort" (100%). En consequence, cette
fiche n'affiche pas de colonne "Accord" separee (elle serait constante et non informative) :
seule la colonne "Grade" (GRADE 1+/1-/2+/2-/AE, standard grade_chip()) est montree dans les
tableaux, avec l'accord fort a 100% disclose une seule fois dans le panneau d'introduction.

COUVERTURE : les 14 questions PICO du sommaire (dont plusieurs comportent des sous-themes
distincts, ex. 5 sous-chirurgies en orthopedie/traumatologie, 2 sous-themes en monitorage
biologique) sont toutes traitees, soit 21 sous-sections cliniques. Comptage exhaustif (grep des
motifs de grade + verification manuelle ligne a ligne) : 77 recommandations individuelles
graduees, toutes transcrites. Double-extraction : un agent independant (contexte vierge, meme
texte source complet) a produit son propre inventaire section par section - total confirme a
77/77, meme repartition par section (1,2,3,2,5,3,5,3,7,5,3,1,3,4,5,2,9,1,5,1,7), aucun ecart.

FIGURES : Figure 1 (PTH/PTG, p.16), Figure 2 (TVP distale post-operatoire, p.74) et Figure 3
(schema de synthese, p.79) sont des images pures (verifie par rendu visuel a 200-400dpi, aucun
texte extractible dans la couche PDF a ces emplacements) - reproduites ici sous forme de
tableaux/panneaux structures fideles au contenu clinique et aux grades imprimes sur le
diagramme source (meme technique que la Figure 1 de fiche_ira.py ou la matrix_table() de
fiche_aap_programmee.py), et non comme un clone visuel boite-par-boite du flowchart original.
Le tableau couleur "Thromboprophylaxie et fonction renale" (p.52, image pure) est en revanche
reproduit verbatim cellule par cellule (rouge/orange/vert), sa structure etant nativement
tabulaire. Idem pour le tableau des delais avant geste neuraxial (p.41, texte extractible) et
les tableaux 1/2/3 de meta-analyses de la section reanimation (p.63-64, texte extractible).

ANOMALIE SOURCE DISCLOSEE (non corrigee, reproduite telle quelle) : le Tableau 2 (p.63,
sous-groupe de l'essai PROTECT) imprime litteralement l'en-tete "Hazard Ratio (IC85%)" -
verifie par rendu visuel a 200dpi, ce n'est pas un artefact d'extraction texte (contrairement
au bug µmol/L de fiche_ira.py) : la valeur "85%" est bien celle imprimee dans le PDF source,
tres probablement une coquille des auteurs pour "IC95%" (convention non-standard sinon). Non
corrige silencieusement ; disclose ici et par une note en bas du tableau dans la fiche.

Pas d'arrondis Unicode (fleches/exposants/emoji) dans le corps du texte - encodage Helvetica.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from style import *
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.units import mm

OUT = "/private/tmp/claude-501/-Users-macbook-Downloads-claude/65498e3e-5ddf-47a6-b100-3ac535d1faa0/scratchpad/rfe_sfar/output/Fiche_GIHP_SFAR_SFTH_SFMV_MTEV_Perioperatoire_2024.pdf"

SOURCE_TXT = ("Source : Recommandations Formalisees d'Experts « Prevention de la maladie "
              "thromboembolique veineuse peri-operatoire » — GIHP, en collaboration avec la SFAR, "
              "la SFTH et la SFMV, endossees par la SFCD, la SFPT et le reseau INNOVTE. "
              "Actualisation 2024 des recommandations SFAR 2011. Methodologie GRADE, vote n=37. "
              "Fiche de synthese non officielle : se referer au texte integral.")

def P(txt, style=S_CELL):
    return Paragraph(txt, style)

def chip(label, **kw):
    return grade_chip(label, **kw)

def reco_table(rows, col_widths):
    """rows: (theme, texte, grade_label). Colonne 'Grade' unique (voir note methodologie :
    l'accord est fort a 100% dans ce document, donc pas de colonne Accord separee)."""
    data = [[P("Thème", S_HEAD_W), P("Recommandation", S_HEAD_W), P("Grade", S_HEAD_W_C)]]
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

def simple_table(header, rows, col_widths):
    data = [[P(h, S_HEAD_W) for h in header]]
    for r in rows:
        data.append([P(c, S_CELL) for c in r])
    t = Table(data, colWidths=col_widths, repeatRows=1)
    st = [
        ("BACKGROUND",(0,0),(-1,0), TEAL_DARK), ("TEXTCOLOR",(0,0),(-1,0), WHITE),
        ("FONTNAME",(0,0),(-1,0), FONT_BOLD), ("FONTSIZE",(0,0),(-1,0), 8),
        ("GRID",(0,0),(-1,-1),0.5,GREY_LIGHT), ("VALIGN",(0,0),(-1,-1),"TOP"),
        ("TOPPADDING",(0,0),(-1,-1),3.2), ("BOTTOMPADDING",(0,0),(-1,-1),3.2), ("LEFTPADDING",(0,0),(-1,-1),5),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            st.append(("BACKGROUND",(0,i),(-1,i), BG_PANEL))
    t.setStyle(TableStyle(st))
    return t

def legend_flowable():
    items = [("1+", "Recommandé (forte)"), ("1-", "Non recommandé (forte)"),
             ("2+", "Proposé (optionnel)"), ("2-", "Proposé de ne pas faire"),
             ("AE", "Avis d'experts")]
    content_w = PAGE_W - 2*MARGIN
    n = len(items)
    chip_w = 15*mm
    text_w = (content_w - n*chip_w) / n
    row_cells, col_widths = [], []
    for g, txt in items:
        row_cells.append(chip(g, width=chip_w-1.5*mm))
        row_cells.append(P(txt, S_BADGE_HEAD))
        col_widths += [chip_w, text_w]
    row = Table([row_cells], colWidths=col_widths)
    row.setStyle(TableStyle([("VALIGN",(0,0),(-1,-1),"MIDDLE"), ("LEFTPADDING",(0,0),(-1,-1),1), ("RIGHTPADDING",(0,0),(-1,-1),1)]))
    return row

def flow_row(text, grade, bg, chip_w=15*mm):
    """Une 'boite' de flowchart redessine : texte + chip de grade individuel (jamais de chip
    composite), fond colore pour distinguer les branches d'une figure source."""
    content_w = PAGE_W - 2*MARGIN
    text_w = content_w - chip_w
    t = Table([[P(text, S_BODY_SM), chip(grade, width=chip_w-2*mm)]], colWidths=[text_w, chip_w])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), bg),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("ALIGN", (1,0), (1,-1), "CENTER"),
        ("BOX", (0,0), (-1,-1), 0.6, GREY_LIGHT),
        ("TOPPADDING", (0,0), (-1,-1), 2.6), ("BOTTOMPADDING", (0,0), (-1,-1), 2.6),
        ("LEFTPADDING", (0,0), (-1,-1), 4), ("RIGHTPADDING", (0,0), (-1,-1), 3),
    ]))
    return t

def flow_label(text, bg=NAVY, fg=WHITE):
    st = pstyle("flow_lbl", fontSize=8.4, leading=10, textColor=fg, fontName=FONT_BOLD)
    t = Table([[Paragraph(text, st)]], colWidths=[PAGE_W-2*MARGIN])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), bg), ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("LEFTPADDING", (0,0), (-1,-1), 4), ("TOPPADDING", (0,0), (-1,-1), 2.4),
        ("BOTTOMPADDING", (0,0), (-1,-1), 2.4),
    ]))
    return t

def renal_grid_table():
    """Reproduction verbatim (case par case) du tableau couleur p.52 'Thromboprophylaxie et
    fonction renale' (image pure dans la source) : DFG estime en 5 tranches, 6 molecules,
    code couleur rouge/orange/vert identique a l'original."""
    S_G = pstyle("grid", fontSize=7.6, leading=9, textColor=WHITE, fontName=FONT_BOLD, alignment=TA_CENTER)
    S_GH = pstyle("gridh", fontSize=8, leading=9.6, textColor=INK, fontName=FONT_BOLD, alignment=TA_CENTER)
    S_GD = pstyle("gridd", fontSize=8.2, leading=9.8, textColor=INK, fontName=FONT_BOLD)
    def gc(txt=""):
        return Paragraph(txt, S_G)
    def gd(txt):
        return Paragraph(txt, S_GD)
    cw = PAGE_W - 2*MARGIN
    c0 = 40*mm
    cN = (cw - c0) / 5.0
    RED_C, AMB_C, GRN_C = RED, AMBER, GREEN
    data = [
        [Paragraph("DFG estimé (mL/min/1,73 m²)", S_GH), Paragraph("&lt;15", S_GH), Paragraph("15-20", S_GH),
         Paragraph("20-30", S_GH), Paragraph("30-50", S_GH), Paragraph("&gt;50", S_GH)],
        [gd("HNF"), gc(), gc(), gc(), gc(), gc()],
        [gd("tinzaparine"), gc(), gc(), gc(), gc(), gc()],
        [gd("enoxaparine"), gc(), gc("½ dose"), gc("½ dose"), gc(), gc()],
        [gd("fondaparinux 2,5 mg"), gc(), gc(), gc(), gc(), gc()],
        [gd("apixaban / rivaroxaban"), gc(), gc(), gc(), gc(), gc()],
        [gd("dabigatran"), gc(), gc(), gc(), gc(), gc()],
    ]
    t = Table(data, colWidths=[c0, cN, cN, cN, cN, cN])
    colors_grid = {
        1: [GRN_C, AMB_C, AMB_C, AMB_C, AMB_C],
        2: [RED_C, RED_C, GRN_C, GRN_C, GRN_C],
        3: [RED_C, GRN_C, GRN_C, GRN_C, GRN_C],
        4: [RED_C, RED_C, RED_C, RED_C, GRN_C],
        5: [RED_C, GRN_C, GRN_C, GRN_C, GRN_C],
        6: [RED_C, RED_C, RED_C, GRN_C, GRN_C],
    }
    style_cmds = [
        ("BACKGROUND", (0,0), (-1,0), TEAL_DARK), ("TEXTCOLOR", (0,0),(-1,0), WHITE),
        ("GRID", (0,0), (-1,-1), 0.7, WHITE),
        ("BOX", (0,0), (-1,-1), 0.8, INK),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("TOPPADDING", (0,0), (-1,-1), 3.6), ("BOTTOMPADDING", (0,0), (-1,-1), 3.6),
        ("LEFTPADDING", (0,0), (-1,-1), 4),
        ("BACKGROUND", (0,1), (0,-1), WHITE),
    ]
    for row_i, cols in colors_grid.items():
        for col_i, c in enumerate(cols, start=1):
            style_cmds.append(("BACKGROUND", (col_i, row_i), (col_i, row_i), c))
    t.setStyle(TableStyle(style_cmds))
    return t

TOTAL_PAGES = {"n": 18}

def on_page(canvas, doc, page_title):
    header_band(canvas, doc, "GIHP / SFAR / SFTH / SFMV — RFE 2024 — FICHE DE SYNTHÈSE",
                "Prévention de la MTEV péri-opératoire",
                page_title, icon_fn=lambda c, x, y: icon_drop(c, x, y, 13*mm), color=TEAL_DARK)
    footer_band(canvas, doc, SOURCE_TXT, f"Page {doc.page} / {TOTAL_PAGES['n']}")

# ---------------------------------------------------------------------------
# SECTION 1 — Introduction, méthodologie, légende, portée
# ---------------------------------------------------------------------------
def _section_intro():
    story = []
    story.append(Spacer(1, 3*mm))
    story.append(info_panel(P(
        "<b>Champ :</b> prévention de la maladie thromboembolique veineuse (MTEV) péri-opératoire "
        "chez l'adulte (toutes chirurgies) et chez l'enfant, actualisant les recommandations SFAR "
        "de 2011. RFE du Groupe d'intérêt en Hémostase Péri-opératoire (GIHP), en collaboration "
        "avec la SFAR, la Société Française de Thrombose et d'Hémostase (SFTH) et la Société "
        "Française de Médecine Vasculaire (SFMV) ; endossée par la Société Française de Chirurgie "
        "Digestive (SFCD), la Société Française de Pharmacologie et de Thérapeutique (SFPT) et le "
        "réseau INNOVTE. <b>Les patients ayant une pathologie hémorragique constitutionnelle ne "
        "sont pas concernés par ces recommandations.</b><br/><br/>"
        "<b>Méthodologie GRADE, format PICO :</b> un niveau de preuve global fort permet une "
        "recommandation <b>forte</b> (« il est recommandé de » — GRADE 1+/1-) ; un niveau modéré ou "
        "faible aboutit à une recommandation <b>optionnelle</b> (« il est proposé de » — GRADE "
        "2+/2-) ; en l'absence de littérature suffisante, un <b>avis d'experts</b> (AE) est formulé. "
        "Chaque recommandation est ensuite validée par un vote (n = 37 participants) : accord "
        "<b>fort</b> si ≥ 70 % d'accord et &lt; 20 % d'opposition ; à défaut, reformulation et "
        "nouveau vote.",
        S_BODY), bg=BG_PANEL, border=TEAL))
    story.append(Spacer(1, 3*mm))
    story.append(info_panel(P(
        "<b>Particularité de ce document (vérifiée par recherche exhaustive sur l'extraction "
        "texte complète) :</b> à la différence d'autres RFE de ce corpus, <b>100 % des 77 "
        "recommandations graduées retrouvées portent la mention d'accord « Fort »</b> — aucune "
        "occurrence d'« Accord Faible » n'apparaît nulle part dans les 79 pages sources. Cette "
        "fiche n'affiche donc pas de colonne « Accord » séparée (elle serait constante et non "
        "informative) : seule la colonne <b>Grade</b> (GRADE 1+/1-/2+/2-/AE) figure dans les "
        "tableaux ci-après.",
        S_BODY_SM), bg=GREEN_LIGHT, border=GREEN))
    story.append(Spacer(1, 3*mm))

    story.append(section_bar("Légende des grades (méthodologie GRADE)"))
    story.append(Spacer(1, 2*mm))
    story.append(legend_flowable())
    story.append(Spacer(1, 4*mm))

    story.append(section_bar("Couverture de cette fiche", color=GREY))
    story.append(Spacer(1, 2*mm))
    story.append(P(
        "Cette fiche reprend l'intégralité des <b>77 recommandations individuelles graduées</b> "
        "des 14 questions PICO du document (comportant au total 21 sous-thèmes cliniques, ex. "
        "5 sous-chirurgies orthopédiques distinctes), ainsi que les 3 figures (PTH/PTG p.16 ; TVP "
        "distale post-opératoire p.74 ; schéma de synthèse p.79 — images pures, redessinées ici en "
        "tableaux/panneaux structurés fidèles au contenu et aux grades imprimés) et les tableaux "
        "chiffrés (fonction rénale p.52 ; délais avant geste neuraxial p.41 ; méta-analyses de la "
        "section réanimation p.63-64). L'argumentaire complet (littérature discutée, figures de "
        "recherche) et les ~400 références bibliographiques ne sont <b>pas</b> repris : se référer "
        "au texte intégral. Une brève note d'évidence (1-2 phrases) accompagne chaque table de "
        "recommandations lorsqu'utile.",
        S_BODY_SM))
    return story

# ---------------------------------------------------------------------------
# SECTION 2 — Q1 implémentation + Q2 facteurs de risque liés au patient
# ---------------------------------------------------------------------------
def _section_q1_q2():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(KeepTogether([
        section_bar("Q1 — Impact de l'implémentation de protocoles de thromboprophylaxie"),
        Spacer(1, 2*mm),
        reco_table([
            ("Protocoles locaux", "Il est recommandé d'implémenter localement des protocoles de "
             "thromboprophylaxie veineuse pour réduire le risque de complications "
             "péri-opératoires. Ces protocoles incluent la déambulation précoce et la "
             "thromboprophylaxie pharmacologique et mécanique, dont l'indication, les modalités "
             "et la durée dépendent du risque thromboembolique veineux de la chirurgie et du "
             "patient, du risque hémorragique et du parcours de soin.", "1+"),
        ], [34*mm, PAGE_W-2*MARGIN-34*mm-16*mm, 16*mm]),
    ]))
    story.append(Spacer(1, 3*mm))

    story.append(KeepTogether([
        section_bar("Q2 — Facteurs de risque thromboembolique veineux liés au patient"),
        Spacer(1, 2*mm),
        reco_table([
            ("Chirurgie faible risque + FdR patient", "Après une chirurgie à faible risque "
             "thromboembolique veineux, si le patient présente un facteur de risque majeur ou "
             "plusieurs facteurs de risque mineurs, il est proposé de prescrire une "
             "thromboprophylaxie par anticoagulant pendant une durée minimale de 7 jours.", "2+"),
            ("Thrombophilie majeure sans AC", "En cas de thrombophilie majeure sans traitement "
             "anticoagulant au long cours, il est suggéré de se rapprocher d'un centre spécialisé "
             "afin de documenter la thrombophilie et d'évaluer le risque thromboembolique "
             "veineux.", "AE"),
        ], [34*mm, PAGE_W-2*MARGIN-34*mm-16*mm, 16*mm]),
    ]))
    story.append(Spacer(1, 2.5*mm))

    cw = PAGE_W - 2*MARGIN
    story.append(info_panel([
        P("<b>Facteurs de risque majeurs</b> (# — seuils de continuum, cf argumentaire) : "
          "antécédent(s) personnel(s) d'ETEV • thrombophilie majeure connue (syndrome des "
          "anticorps antiphospholipides, déficit AT/PC/PS, polymorphismes homozygotes ou "
          "hétérozygoties composites Leiden/facteur II) • cancer actif (traitement &lt;6 mois) • "
          "obésité de classe III ou plus (IMC ≥ 40 kg/m²).", S_BODY_SM),
        Spacer(1, 1.5*mm),
        P("<b>Facteurs de risque modérés ou mineurs :</b> âge ≥ 75 ans • insuffisance cardiaque "
          "ou respiratoire, BPCO • insuffisance rénale sévère (DFG &lt; 30 mL/min/1,73 m²) • "
          "maladie inflammatoire chronique (PR, MICI, lupus) • traitement hormonal œstrogénique • "
          "grossesse en cours ou post-partum • obésité de classe I-II (IMC 30-40) • alitement "
          "prolongé récent • déficit neurologique &lt;1 mois (AVC, lésion médullaire) • "
          "immobilisation orthopédique ou alitement post-opératoire.", S_BODY_SM),
    ], bg=BG_PANEL, border=TEAL))
    story.append(Spacer(1, 1.5*mm))
    story.append(P(
        "<i>Thrombophilie majeure + anticoagulation au long cours :</i> thromboprophylaxie "
        "post-opératoire tant que le traitement antérieur n'est pas repris. <i>Thrombophilie "
        "mineure :</i> pas de thromboprophylaxie systématique. <i>Pas de thrombophilie connue :</i> "
        "pas d'indication à un bilan de thrombophilie pour stratifier le risque post-opératoire "
        "(sauf antécédent familial documenté). Durée minimale d'une semaine proposée pour couvrir "
        "la période la plus à risque (délai médian de survenue d'un ETEV post-opératoire : "
        "8 jours [IQR 5-13] en chirurgie ambulatoire).", S_NOTE))
    return story

# ---------------------------------------------------------------------------
# SECTION 3 — Q3a PTH/PTG + Figure 1
# ---------------------------------------------------------------------------
def _section_pth_ptg():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(KeepTogether([
        section_bar("Orthopédie — Prothèse totale de hanche (PTH) ou de genou (PTG), hors fracture"),
        Spacer(1, 2*mm),
        reco_table([
            ("Indication", "Il est recommandé de prescrire une thromboprophylaxie pharmacologique "
             "après PTH ou PTG.", "1+"),
            ("Durée", "Il est recommandé que la durée de thromboprophylaxie pharmacologique soit "
             "de 35 jours après PTH et 14 jours après PTG.", "1+"),
            ("Modalités", "Il est recommandé de prescrire soit un anticoagulant (AOD, HBPM ou "
             "fondaparinux) pendant toute la durée, soit une thromboprophylaxie séquentielle "
             "(5 jours d'anticoagulant puis aspirine 75-100 mg/j pendant 30 jours après PTH ou "
             "9 jours après PTG) si le patient est pris en charge dans un parcours de RAAC réussi "
             "et sans facteur de risque thromboembolique veineux majeur** ni plusieurs facteurs "
             "mineurs.", "1+"),
        ], [26*mm, PAGE_W-2*MARGIN-26*mm-16*mm, 16*mm]),
        P("** Facteurs de risque majeurs : antécédents personnels d'ETEV, thrombophilie majeure "
          "connue, cancer actif, obésité morbide (IMC ≥ 40 kg/m²) — cf Q2.", S_NOTE),
    ]))
    story.append(Spacer(1, 2*mm))
    story.append(P(
        "<i>Posologies :</i> apixaban 2,5 mg x2/j (débuté à H12-H24) ; rivaroxaban 10 mg x1/j "
        "(H6-H8) ; dabigatran 220 mg x1/j (150 mg si &gt;75 ans, ClCr 30-50, ou interaction "
        "vérapamil/amiodarone/quinidine) ; fondaparinux 2,5 mg x1/j SC (≥ H8) ; HBPM ≥ 4000 UI "
        "anti-Xa. Parcours optimisé (RAAC/ambulatoire) = chirurgie &lt;120 min ET marche avec "
        "déroulé du pas &lt;24h ET hospitalisation &lt;5 jours.", S_NOTE))
    story.append(Spacer(1, 3*mm))

    story.append(section_bar("Figure 1 (p.16) — Thromboprophylaxie après PTH ou PTG", color=TEAL_DARK))
    story.append(Spacer(1, 1.5*mm))
    story.append(P(
        "<i>Redessin structuré du diagramme source (image pure) — mêmes issues cliniques et "
        "grades imprimés sur le schéma original, sous forme de tableau.</i>", S_NOTE))
    story.append(Spacer(1, 1.5*mm))
    story.append(flow_label("PTH ou PTG — parcours de RAAC/ambulatoire prévu ET réussi (chirurgie <120 min, marche <24h, hospitalisation <5j) ET absence de FdR thromboembolique majeur ou de plusieurs FdR mineurs"))
    story.append(flow_row(
        "-> Thromboprophylaxie SÉQUENTIELLE : anticoagulant 5 jours puis aspirine 75-100 mg/j "
        "pendant 30 jours (PTH) ou 9 jours (PTG).", "1+", GREEN_LIGHT))
    story.append(Spacer(1, 1*mm))
    story.append(flow_label("Sinon (RAAC non prévu, conditions RAAC finalement non respectées, ou FdR thromboembolique veineux du patient présent)", bg=NAVY))
    story.append(flow_row(
        "-> Thromboprophylaxie par ANTICOAGULANT SEUL pendant toute la durée : HBPM, apixaban, "
        "dabigatran ou rivaroxaban, ou fondaparinux, débuté entre H12 et H24 post-opératoires "
        "(entre H6 et H12 si risque thromboembolique veineux élevé lié au patient — cf Q7 pour le "
        "détail des délais). Durée : 35 j (PTH) / 14 j (PTG).", "2+", BG_PANEL))
    story.append(Spacer(1, 1*mm))
    story.append(flow_row(
        "Si très haut risque thromboembolique veineux, associer une compression pneumatique "
        "intermittente (CPI) — cf Q8.", "2+", BG_PANEL))
    story.append(Spacer(1, 1*mm))
    story.append(flow_row(
        "Dans tous les cas : déambulation précoce et hydratation optimale.", "2+", AMBER_LIGHT))
    story.append(flow_row(
        "Dans tous les cas : pas de contention élastique graduée.", "1-", AMBER_LIGHT))
    story.append(Spacer(1, 1.5*mm))
    story.append(P("<i>Liste complète des facteurs de risque thromboembolique veineux du "
                    "patient : cf Q2, page précédente.</i>", S_NOTE))
    return story

# ---------------------------------------------------------------------------
# SECTION 4 — fracture ESF + fracture diaphyse/etc + ligamentoplastie/etc
# ---------------------------------------------------------------------------
def _section_fractures():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(KeepTogether([
        section_bar("Fracture de l'extrémité supérieure du fémur (ESF)"),
        Spacer(1, 2*mm),
        reco_table([
            ("Anticoagulant", "Une thromboprophylaxie par anticoagulant (HBPM ou fondaparinux) "
             "est recommandée pendant 4 semaines après la chirurgie.", "1+"),
            ("Chirurgie retardée", "Si la chirurgie est retardée, il est proposé de débuter la "
             "thromboprophylaxie en pré-opératoire, en préférant une HBPM et en respectant un "
             "délai de 12h entre la dernière injection d'HBPM et la chirurgie.", "2+"),
        ], [30*mm, PAGE_W-2*MARGIN-30*mm-16*mm, 16*mm]),
    ]))
    story.append(Spacer(1, 1.5*mm))
    story.append(P("<i>Fondaparinux 2,5 mg x1/j SC (poids &gt;50 kg, DFG &gt;50) débuté ≥ H8. "
                    "Aspirine non recommandée dans cette indication à haut risque thrombotique "
                    "(non comparée aux HBPM).</i>", S_NOTE))
    story.append(Spacer(1, 3*mm))

    story.append(KeepTogether([
        section_bar("Fracture diaphyse fémorale, plateau tibial, rotule, tibia, cheville, tendon d'Achille"),
        Spacer(1, 2*mm),
        reco_table([
            ("Anticoagulant", "Une thromboprophylaxie par anticoagulant (AOD anti-Xa ou HBPM) est "
             "recommandée après chirurgie pour ces fractures/ruptures.", "1+"),
            ("Choix", "Il est proposé de préférer un AOD anti-Xa à une HBPM (essai PRONOMOS : "
             "rivaroxaban plus efficace que l'enoxaparine sans excès hémorragique).", "2+"),
            ("Chirurgie différée", "Si l'intervention est prévue plus de 12h après "
             "l'hospitalisation, une thromboprophylaxie pré-opératoire par HBPM est proposée "
             "(délai 12h avant la chirurgie).", "2+"),
            ("Durée", "Il est proposé de poursuivre jusqu'à l'appui plantaire avec déroulé du "
             "pied, durée minimale 7 jours.", "2+"),
            ("Aspirine", "Il n'est pas recommandé de prescrire de l'aspirine pour la "
             "thromboprophylaxie veineuse.", "1-"),
        ], [30*mm, PAGE_W-2*MARGIN-30*mm-16*mm, 16*mm]),
    ]))
    story.append(Spacer(1, 3*mm))

    story.append(KeepTogether([
        section_bar("Ligamentoplastie du genou, arthroscopie simple, méniscectomie, chir. avant-pied, ablation de matériel"),
        Spacer(1, 2*mm),
        reco_table([
            ("Pas de systématique", "Il est proposé de ne pas prescrire de thromboprophylaxie "
             "pharmacologique systématique après ces gestes.", "2-"),
            ("Si FdR patient", "Si le patient présente un facteur de risque thromboembolique "
             "veineux majeur ou plusieurs facteurs mineurs, une thromboprophylaxie par "
             "anticoagulant (AOD anti-Xa ou HBPM) est proposée.", "2+"),
            ("Durée si prescrite", "Si une thromboprophylaxie pharmacologique est prescrite, une "
             "durée de 7 jours minimum est suggérée.", "AE"),
        ], [30*mm, PAGE_W-2*MARGIN-30*mm-16*mm, 16*mm]),
    ]))
    return story

# ---------------------------------------------------------------------------
# SECTION 5 — Q4 abdomino-pelvien + Q5 carcinologique
# ---------------------------------------------------------------------------
def _section_abdo_carcino():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(KeepTogether([
        section_bar("Chirurgie abdomino-pelvienne (carcinologique ou non)"),
        Spacer(1, 2*mm),
        reco_table([
            ("Risque élevé — HBPM", "Après chirurgie abdomino-pelvienne à risque élevé "
             "(carcinologique ou non), il est recommandé de prescrire une thromboprophylaxie par "
             "HBPM pour une durée de 4 semaines, y compris en cas de chirurgie mini-invasive ou "
             "de parcours de RAAC.", "1+"),
            ("Risque élevé — fondaparinux", "Il est proposé que le fondaparinux puisse être "
             "utilisé en alternative aux HBPM.", "2+"),
            ("Risque élevé — AOD en relais", "Il est proposé que les AOD anti-Xa puissent être "
             "utilisés en relais des HBPM après reprise du transit.", "2+"),
            ("Risque intermédiaire", "Il est proposé de prescrire une thromboprophylaxie par "
             "HBPM pour une durée minimale de 7 jours.", "2+"),
            ("Risque faible", "Il est proposé de ne pas prescrire de thromboprophylaxie "
             "pharmacologique systématique. Elle est proposée si le patient présente un facteur "
             "de risque majeur, plusieurs facteurs mineurs, une chirurgie prolongée ou une "
             "complication post-opératoire.", "2-"),
        ], [34*mm, PAGE_W-2*MARGIN-34*mm-16*mm, 16*mm]),
    ]))
    story.append(Spacer(1, 1.5*mm))
    story.append(P("<i>Chirurgie à risque élevé (durée &gt;2h, résection étendue, maladie "
                    "carcinologique/inflammatoire) : ex. hépatectomie majeure, colectomie, "
                    "gastrectomie, prostatectomie, cystectomie, néphrectomie, hystérectomie par "
                    "voie haute, chirurgie du cancer de l'utérus/ovaire. Risque intermédiaire : "
                    "ex. sigmoïdectomie à distance d'une poussée, néphrectomie pour don vivant. "
                    "Risque faible : ex. cholécystectomie programmée, RTUP, conisation, "
                    "hystéroscopie.</i>", S_NOTE))
    story.append(Spacer(1, 3*mm))

    story.append(KeepTogether([
        section_bar("Chirurgie carcinologique (hors abdomino-pelvienne : sein, ORL, poumon…)"),
        Spacer(1, 2*mm),
        reco_table([
            ("Risque élevé", "Après chirurgie carcinologique à risque thromboembolique élevé, il "
             "est recommandé de prescrire une thromboprophylaxie par HBPM pour une durée minimale "
             "de 7 jours.", "1+"),
            ("Délai", "Il est proposé de commencer la thromboprophylaxie pharmacologique en "
             "post-opératoire.", "2+"),
            ("CPI", "Il est proposé d'utiliser la CPI en per- et post-opératoire en cas de très "
             "haut risque thromboembolique veineux# ou de contre-indication à la "
             "thromboprophylaxie pharmacologique.", "2+"),
        ], [26*mm, PAGE_W-2*MARGIN-26*mm-16*mm, 16*mm]),
    ]))
    story.append(Spacer(1, 1.5*mm))
    story.append(P("<i># Combinaison d'un FdR majeur lié au patient et d'un risque chirurgical "
                    "élevé. Sein : risque bas (&lt;0,5%), pas de prophylaxie systématique sauf "
                    "mastectomie avec reconstruction, chimiothérapie péri-opératoire ou "
                    "tamoxifène. ORL : majorité ambulatoire sans prophylaxie, prophylaxie si "
                    "chirurgie majeure avec lambeau. Poumon : incidence élevée (2-5% à 1 mois) "
                    "malgré prophylaxie, durée optimale non établie (certaines recommandations "
                    "suggèrent jusqu'à 1 mois par analogie).</i>", S_NOTE))
    return story

# ---------------------------------------------------------------------------
# SECTION 6 — Q6 chirurgie vasculaire
# ---------------------------------------------------------------------------
def _section_vasculaire():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(KeepTogether([
        section_bar("Chirurgie vasculaire"),
        Spacer(1, 2*mm),
        reco_table([
            ("Carotidienne", "Après chirurgie carotidienne, il est proposé de ne pas prescrire de "
             "thromboprophylaxie veineuse systématique.", "2-"),
            ("Aortique / revasc. MI ouverte", "Après chirurgie aortique abdominale (ouverte ou "
             "endoprothèse) ou revascularisation artérielle des membres inférieurs par voie "
             "ouverte, il est proposé de prescrire une thromboprophylaxie jusqu'à reprise de la "
             "marche.", "2+"),
            ("Endovasculaire MI", "Après procédure endovasculaire artérielle (angioplastie et/ou "
             "endoprothèse) des membres inférieurs, il est proposé de ne pas prescrire de "
             "thromboprophylaxie systématique.", "2-"),
            ("Revasc. MI + rivaroxaban", "Chez un patient éligible au rivaroxaban 2,5 mg x2/j + "
             "aspirine 100 mg/j (prévention cardiovasculaire), il est proposé de différer "
             "l'introduction du rivaroxaban à la fin de la thromboprophylaxie veineuse par HBPM "
             "lorsque celle-ci est indiquée.", "2+"),
            ("CPI contre-indiquée", "Il est proposé de ne pas utiliser de CPI en péri-opératoire "
             "de chirurgie de revascularisation artérielle des membres inférieurs (risque "
             "d'altération de la perfusion artérielle).", "AE"),
            ("Varices — chirurgie ouverte", "Après chirurgie ouverte de varices (stripping), il "
             "est proposé de réaliser une thromboprophylaxie de courte durée (≤ 7 jours).", "2+"),
            ("Varices — endoveineux thermique", "Après procédure thermique endovasculaire des "
             "varices, il est proposé de ne pas prescrire de thromboprophylaxie sauf en cas de "
             "facteurs de risque liés au patient.", "2-"),
        ], [38*mm, PAGE_W-2*MARGIN-38*mm-16*mm, 16*mm]),
    ]))
    story.append(Spacer(1, 1.5*mm))
    story.append(P("<i>Rivaroxaban 2,5 mg x2/j + aspirine : AMM post-opératoire de chirurgie "
                    "vasculaire artérielle des MI (essai VOYAGER PAD) en prévention des "
                    "évènements cardiaques et vasculaires majeurs, initié dans les 10 jours "
                    "post-opératoires ; si HBPM veineuse prescrite, décaler le rivaroxaban à "
                    "l'arrêt de l'HBPM (J5-J10).</i>", S_NOTE))
    return story

# ---------------------------------------------------------------------------
# SECTION 7 — Q7 délai d'introduction + ALR + tableau délais neuraxiaux
# ---------------------------------------------------------------------------
def _section_delai():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(KeepTogether([
        section_bar("Délai d'introduction de la thromboprophylaxie pharmacologique"),
        Spacer(1, 2*mm),
        reco_table([
            ("Post-opératoire", "En chirurgie programmée, lorsqu'une thromboprophylaxie "
             "pharmacologique est indiquée, il est proposé d'en administrer la première dose en "
             "post-opératoire pour réduire le risque hémorragique.", "2+"),
            ("H12-H24", "Il est proposé de débuter la thromboprophylaxie entre la 12e et la 24e "
             "heure post-opératoire (le lendemain matin pour la chirurgie programmée).", "2+"),
            ("H6-H12 si FdR élevé", "En cas de risque thromboembolique veineux élevé lié au "
             "patient# les experts proposent de débuter entre la 6e et la 12e heure "
             "post-opératoire, en commençant par une HBPM quel que soit l'anticoagulant du "
             "lendemain.", "AE"),
            ("Chirurgie urgente différée", "En cas de chirurgie urgente différée de plus de 12h, "
             "il est proposé de débuter la thromboprophylaxie en pré-opératoire par une HBPM, en "
             "respectant un délai de 12h avant la chirurgie.", "2+"),
            ("Délais avant ALR", "Il est recommandé de respecter les délais minimaux de sécurité "
             "entre la thromboprophylaxie pharmacologique et la réalisation de procédures d'ALR "
             "neuraxiale.", "1+"),
        ], [34*mm, PAGE_W-2*MARGIN-34*mm-16*mm, 16*mm]),
        P("# lié au patient : antécédent personnel d'ETEV, thrombophilie majeure connue, cancer "
          "actif, IMC ≥ 40 kg/m², ou association de plusieurs facteurs de risque (cf Q2).", S_NOTE),
    ]))
    story.append(Spacer(1, 3*mm))

    story.append(P("<b>Délais entre thromboprophylaxie pharmacologique et geste neuraxial</b> "
                    "(rachianesthésie, péridurale, péri-rachi combinée, y compris retrait de "
                    "cathéter)", S_H2))
    story.append(Spacer(1, 1*mm))
    cw = PAGE_W - 2*MARGIN
    story.append(simple_table(
        ["Anticoagulant (dose préventive)", "Demi-vie", "Délai minimum avant le geste neuraxial"],
        [
            ["HBPM", "5-7h", "12h (si DFG &gt; 30 mL/min/1,73 m²)"],
            ["HNF SC", "2h", "4h"],
            ["Apixaban", "12h*", "36h"],
            ["Rivaroxaban", "5-9h (11-13h chez le sujet âgé)*", "24h (si DFG &gt; 30 mL/min/1,73 m²)"],
            ["Dabigatran", "11-15h si DFG &gt; 50*", "24-36h (si DFG &gt; 50 mL/min/1,73 m²)"],
            ["Fondaparinux", "17h (21h chez le sujet âgé)*", "36h (si DFG &gt; 50 mL/min/1,73 m²)"],
        ], [34*mm, cw-34*mm-70*mm, 70*mm]))
    story.append(Spacer(1, 1.5*mm))
    story.append(P("<i>* Données du RCP. Discuter d'allonger les délais ou de réaliser un dosage "
                    "en cas d'insuffisance rénale (DFG &lt;50), petit poids, ou sujet âgé. Seuils "
                    "de sécurité hémostatique si dosage réalisé : [AOD] ≤ 30 ng/mL ; anti-Xa HBPM "
                    "≤ 0,1 UI/mL ; anti-Xa fondaparinux ≤ 0,1 µg/mL (ou &lt; limite de "
                    "quantification du laboratoire).</i>", S_NOTE))
    return story

# ---------------------------------------------------------------------------
# SECTION 8 — Q8 CPI + Q9 contentions + Q10 filtre cave
# ---------------------------------------------------------------------------
def _section_cpi_contention_filtre():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(KeepTogether([
        section_bar("Compression pneumatique intermittente (CPI)"),
        Spacer(1, 2*mm),
        reco_table([
            ("Si AC contre-indiqués", "Il est recommandé d'utiliser la CPI si une "
             "thromboprophylaxie veineuse est indiquée mais que les anticoagulants sont "
             "contre-indiqués.", "1+"),
            ("Très haut risque", "En cas de très haut risque thromboembolique veineux§, il est "
             "proposé d'associer la CPI en per- et post-opératoire à la thromboprophylaxie "
             "pharmacologique.", "2+"),
            ("Déambulation", "Il est proposé que l'usage de la CPI ne retarde pas la reprise de "
             "la déambulation.", "AE"),
        ], [30*mm, PAGE_W-2*MARGIN-30*mm-16*mm, 16*mm]),
        P("§ Combinaison d'un FdR thromboembolique majeur lié au patient et d'une chirurgie à "
          "risque élevé.", S_NOTE),
    ]))
    story.append(Spacer(1, 3*mm))

    story.append(KeepTogether([
        section_bar("Contentions élastiques graduées"),
        Spacer(1, 2*mm),
        reco_table([
            ("Non recommandées", "Les contentions élastiques graduées ne sont pas recommandées "
             "pour la thromboprophylaxie péri-opératoire, quel que soit le risque "
             "thromboembolique veineux.", "1-"),
        ], [30*mm, PAGE_W-2*MARGIN-30*mm-16*mm, 16*mm]),
    ]))
    story.append(Spacer(1, 1.5*mm))
    story.append(P("<i>Essai GAPS (n=1858, ajout de contentions à une HBPM) : aucun bénéfice. "
                    "Registre médico-économique (n=24273) : RR=0,999 (IC95% 0,998-1,000). Les "
                    "contentions augmentent les lésions cutanées et les coûts sans réduire les "
                    "ETEV.</i>", S_NOTE))
    story.append(Spacer(1, 3*mm))

    story.append(KeepTogether([
        section_bar("Filtre cave"),
        Spacer(1, 2*mm),
        reco_table([
            ("Prévention primaire", "Il est proposé de ne pas poser de filtre cave pour la "
             "thromboprophylaxie veineuse péri-opératoire primaire.", "2-"),
            ("Prévention secondaire — pose", "Il est proposé de discuter la mise en place d'un "
             "filtre cave optionnel en pré-opératoire d'une chirurgie à risque hémorragique "
             "lorsque celle-ci doit être réalisée moins d'un mois après une EP et/ou une TVP "
             "proximale des membres inférieurs.", "2+"),
            ("Retrait", "Il est recommandé de programmer le retrait du filtre cave dès que le "
             "traitement anticoagulant curatif a pu être repris sans complication.", "1+"),
        ], [38*mm, PAGE_W-2*MARGIN-38*mm-16*mm, 16*mm]),
    ]))
    return story

# ---------------------------------------------------------------------------
# SECTION 9 — Q11 insuffisance rénale + tableau DFG
# ---------------------------------------------------------------------------
def _section_irc():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(KeepTogether([
        section_bar("Insuffisance rénale"),
        Spacer(1, 2*mm),
        reco_table([
            ("Adapter à la fonction rénale", "Il est recommandé d'adapter les modalités de "
             "thromboprophylaxie pharmacologique à la fonction rénale.", "1+"),
            ("IR sévère — 1re intention", "En cas d'insuffisance rénale sévère (DFG estimé 15-30 "
             "mL/min/1,73 m²), il est proposé d'utiliser les HBPM en première intention plutôt "
             "que l'HNF ou les AOD.", "2+"),
            ("IR sévère — schémas AMM", "Il est recommandé d'utiliser : enoxaparine 2000 UI x1/j "
             "SC si DFG 15-30 ; tinzaparine 4500 UI x1/j SC si DFG &gt; 20.", "1+"),
            ("IR terminale (DFG &lt;15)", "En cas d'insuffisance rénale terminale, il est "
             "recommandé d'utiliser la calciparine (HNF) 5000 UI x2/j SC, les autres "
             "thérapeutiques n'étant pas recommandées.", "1+"),
        ], [38*mm, PAGE_W-2*MARGIN-38*mm-16*mm, 16*mm]),
    ]))
    story.append(Spacer(1, 3*mm))
    story.append(P("<b>Tableau — Thromboprophylaxie et fonction rénale</b> (reproduction verbatim "
                    "du tableau-image source p.52)", S_H2))
    story.append(Spacer(1, 1.5*mm))
    story.append(renal_grid_table())
    story.append(Spacer(1, 1.5*mm))
    story.append(P("<i>En rouge : non recommandé par l'AMM ; en orange : non recommandé par le "
                    "GIHP ; en vert : recommandé. Dabigatran 150 mg x1/j si DFG 30-50, "
                    "contre-indiqué si DFG &lt;30. Apixaban/rivaroxaban : pas d'ajustement si DFG "
                    "15-30 mais données péri-opératoires très limitées ; contre-indiqués si DFG "
                    "&lt;15. Fondaparinux 2,5 mg contre-indiqué si DFG &lt;50 (fondaparinux 1,5 mg "
                    "non disponible en France).</i>", S_NOTE))
    return story

# ---------------------------------------------------------------------------
# SECTION 10 — Q12 obésité et poids extrêmes
# ---------------------------------------------------------------------------
def _section_obesite():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(KeepTogether([
        section_bar("Obésité et poids extrêmes"),
        Spacer(1, 2*mm),
        reco_table([
            ("Classe I-II (IMC 30-39)", "Chez les patients présentant une obésité de classe I ou "
             "II nécessitant une thromboprophylaxie pharmacologique, il est proposé d'utiliser un "
             "schéma posologique standard.", "2+"),
            ("Classe III+ (IMC ≥40)", "Il est proposé d'utiliser : enoxaparine 4000 UI x2/j SC "
             "(ou 6000 UI x1/j ; 6000 UI x2/j réservé aux patients &gt;150 kg) ; daltéparine 5000 "
             "UI x2/j SC ; tinzaparine 75 UI/kg (poids réel) x1/j SC ; fondaparinux 5 mg x1/j SC ; "
             "apixaban 2,5 mg x2/j PO ; rivaroxaban 10 mg x1/j PO (peu d'expérience AOD si IMC "
             "&gt;50 ou poids &gt;150 kg).", "2+"),
            ("Classe III + chirurgie à risque élevé", "Il est proposé d'associer une CPI à la "
             "thromboprophylaxie pharmacologique.", "2+"),
            ("Chirurgie bariatrique", "Il est proposé de prescrire une thromboprophylaxie "
             "post-opératoire par HBPM ou fondaparinux pour une durée minimale de 10 jours.", "2+"),
            ("Petit poids", "Chez les patients de petit poids, il est proposé d'adapter les "
             "schémas posologiques (risque d'accumulation et d'hémorragie).", "2+"),
        ], [38*mm, PAGE_W-2*MARGIN-38*mm-16*mm, 16*mm]),
    ]))
    story.append(Spacer(1, 1.5*mm))
    story.append(P("<i>C'est l'IMC (et non le poids seul) qui guide la discussion de "
                    "thromboprophylaxie chez l'obèse ; le poids guide l'adaptation posologique "
                    "chez le patient de grande taille sans obésité. Seule la tinzaparine a une "
                    "AMM d'ajustement au poids réel. Petit poids : ex. réduire l'enoxaparine à "
                    "2000 UI ; le RCP du fondaparinux déconseille son usage si poids &lt;50 kg. "
                    "AOD : apixaban/rivaroxaban sans adaptation nécessaire à petit poids selon "
                    "leur RCP ; données limitées pour le dabigatran.</i>", S_NOTE))
    return story

# ---------------------------------------------------------------------------
# SECTION 11 — Q13 pédiatrie + Q14 réanimation (recommandations) — Tableaux 1/2/3
# séparés dans _section_reanimation_tableaux() pour un meilleur remplissage des pages
# (voir combinators _section_9() et _section_10() plus bas).
# ---------------------------------------------------------------------------
def _section_pediatrie_reanimation():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(KeepTogether([
        section_bar("Chirurgie pédiatrique"),
        Spacer(1, 2*mm),
        reco_table([
            ("Dès la puberté / 14 ans", "Il est proposé qu'à partir de la puberté ou de l'âge de "
             "14 ans, la thromboprophylaxie pharmacologique réponde aux mêmes recommandations que "
             "chez l'adulte.", "2+"),
            ("Avant la puberté / 14 ans", "Les experts suggèrent que la présence de plusieurs "
             "facteurs de risque thromboembolique veineux conduise à discuter au cas par cas le "
             "bénéfice-risque d'une thromboprophylaxie pharmacologique.", "AE"),
        ], [38*mm, PAGE_W-2*MARGIN-38*mm-16*mm, 16*mm]),
    ]))
    story.append(Spacer(1, 1.5*mm))
    story.append(P("<i>Schémas proposés pour l'enfant &lt;40 kg autour de la puberté (non "
                    "formellement évalués) : 50 UI/kg/j d'enoxaparine (1-2 injections/j) ou 50 "
                    "UI/kg de tinzaparine x1/j. Risque hémorragique conséquent chez l'enfant "
                    "(0,4-3% saignements majeurs, jusqu'à 21% mineurs). AOD sans AMM en "
                    "prévention primaire pédiatrique (fin 2023).</i>", S_NOTE))
    story.append(Spacer(1, 3*mm))

    story.append(KeepTogether([
        section_bar("Patient de réanimation"),
        Spacer(1, 2*mm),
        reco_table([
            ("Indication", "Il est recommandé d'administrer une thromboprophylaxie "
             "pharmacologique chez les patients de réanimation pour réduire les complications "
             "thromboemboliques veineuses.", "1+"),
            ("HBPM > HNF", "En l'absence d'insuffisance rénale terminale, il est recommandé de "
             "prescrire des HBPM à doses prophylactiques plutôt que de l'HNF.", "1+"),
            ("Pas de monitorage anti-Xa", "Lors d'une thromboprophylaxie par HBPM, il est proposé "
             "de ne pas monitorer l'activité anti-Xa pour adapter les posologies.", "2-"),
            ("Adapter les posologies", "Il est proposé d'adapter les posologies d'HBPM chez les "
             "patients de petits poids, les obèses de classe III et plus, et en cas "
             "d'insuffisance rénale sévère.", "2+"),
            ("IR sévère stable", "En cas d'insuffisance rénale sévère stable (DFG 15-30), il est "
             "proposé d'utiliser les HBPM en 1re intention selon les schémas AMM (enoxaparine "
             "2000 UI x1/j si DFG 15-30 ; tinzaparine 4500 UI x1/j si DFG &gt;20).", "2+"),
            ("IR terminale", "En cas d'insuffisance rénale terminale (DFG &lt;15), il est "
             "recommandé d'utiliser la calciparine 5000 UI x2/j SC.", "1+"),
            ("Pas de CPI systématique associée", "Il n'est pas recommandé d'associer "
             "systématiquement une CPI à une thromboprophylaxie pharmacologique.", "1-"),
            ("CPI si contre-indication", "La CPI est recommandée en cas de contre-indication à "
             "une thromboprophylaxie par anticoagulants, en particulier si risque hémorragique "
             "élevé.", "1+"),
            ("Contentions non recommandées", "Les contentions élastiques graduées ne sont pas "
             "recommandées, quel que soit le risque thromboembolique veineux.", "1-"),
        ], [38*mm, PAGE_W-2*MARGIN-38*mm-16*mm, 16*mm]),
    ]))
    return story

def _section_reanimation_tableaux():
    """Tableaux 1/2/3 de la section réanimation (méta-analyses), séparés de la table de
    recommandations ci-dessus pour un meilleur remplissage des pages — combinés plus bas avec
    la section acide tranexamique / monitorage biologique."""
    story = []
    cw = PAGE_W - 2*MARGIN
    story.append(P("<b>Tableau 1</b> — Méta-analyse en réseau HBPM vs HNF en réanimation", S_H2))
    story.append(Spacer(1, 1*mm))
    story.append(simple_table(
        ["Événement", "N études", "N patients", "Odds ratio (IC95%)"],
        [
            ["TVP", "6", "5645", "0,78 (0,65 – 0,95)"],
            ["EP", "3", "4447", "0,67 (0,36 – 1,22)"],
            ["Hémorragie majeure", "4", "1002", "1,71 (0,49 – 5,95)"],
            ["TIH", "3", "4447", "0,38 (0,15 – 0,98)"],
            ["Mortalité totale", "2", "1408", "0,90 (0,68 – 1,18)"],
        ], [45*mm, 25*mm, 28*mm, cw-45*mm-25*mm-28*mm]))
    story.append(Spacer(1, 2.5*mm))

    story.append(P("<b>Tableau 2</b> — Sous-groupe PROTECT : daltéparine vs HNF selon la fonction "
                    "rénale (insuffisance rénale sévère, n=590)", S_H2))
    story.append(Spacer(1, 1*mm))
    story.append(simple_table(
        ["Événement", "Daltéparine", "HNF", "Hazard ratio (IC85% *)"],
        [
            ["MTEV", "10,0 %", "6,4 %", "1,87 (0,96 – 3,63)"],
            ["Hémorragie majeure", "8,9 %", "11,0 %", "0,89 (0,51 – 1,53)"],
        ], [45*mm, 25*mm, 25*mm, cw-45*mm-25*mm-25*mm]))
    story.append(Spacer(1, 1.5*mm))
    story.append(P("<i>* « IC85% » est bien l'intitulé imprimé dans le document source "
                    "(vérifié par rendu visuel de la page — pas un artefact d'extraction texte), "
                    "très probablement une coquille des auteurs pour IC95%. Non corrigé "
                    "silencieusement, reproduit tel quel.</i>", S_NOTE))
    story.append(Spacer(1, 2.5*mm))

    story.append(P("<b>Tableau 3</b> — Méta-analyse de la CPI en réanimation", S_H2))
    story.append(Spacer(1, 1*mm))
    story.append(simple_table(
        ["Comparaison", "Événement", "n études / n patients", "Risque relatif (IC95%)"],
        [
            ["CPI vs contrôle", "MTEV", "4 / 1120", "0,35 (0,18 – 0,68)"],
            ["CPI vs contrôle", "EP", "2 / 402", "0,17 (0,06 – 0,50)"],
            ["CPI + héparine vs héparine", "MTEV", "4 / 2777", "0,55 (0,24 – 1,27)"],
            ["CPI + héparine vs héparine", "EP", "3 / 2661", "0,72 (0,31 – 1,69)"],
        ], [42*mm, 20*mm, 38*mm, cw-42*mm-20*mm-38*mm]))
    return story

# ---------------------------------------------------------------------------
# SECTION 12 — Q15 acide tranexamique + Q16 monitorage biologique
# ---------------------------------------------------------------------------
def _section_atx_monitorage():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(KeepTogether([
        section_bar("Acide tranexamique et thromboprophylaxie veineuse"),
        Spacer(1, 2*mm),
        reco_table([
            ("Pas de modification", "Il est recommandé de ne pas modifier les modalités de "
             "thromboprophylaxie en cas d'administration d'acide tranexamique.", "1-"),
        ], [34*mm, PAGE_W-2*MARGIN-34*mm-16*mm, 16*mm]),
    ]))
    story.append(Spacer(1, 1.5*mm))
    story.append(P("<i>Essais randomisés et méta-analyses concordants : l'acide tranexamique "
                    "n'augmente pas l'incidence des ETEV péri-opératoires (chirurgie générale, "
                    "orthopédique, cardiaque, obstétrique, traumatologie), y compris lorsque "
                    "l'initiation de l'AOD est repoussée au lendemain d'une chirurgie "
                    "orthopédique majeure.</i>", S_NOTE))
    story.append(Spacer(1, 3*mm))

    story.append(KeepTogether([
        section_bar("Monitorage biologique — surveillance du niveau d'anticoagulation"),
        Spacer(1, 2*mm),
        reco_table([
            ("Pas de mesure sous HBPM", "Il est proposé de ne pas mesurer l'activité anti-Xa au "
             "cours d'une thromboprophylaxie par HBPM.", "2-"),
            ("Pas de mesure AOD/fondaparinux/HNF", "Les experts proposent de ne pas mesurer le "
             "niveau d'anticoagulation au cours d'une prophylaxie par AOD, fondaparinux ou HNF.", "AE"),
            ("Poids extrêmes / IR", "Chez les patients de poids extrêmes et les insuffisants "
             "rénaux, il est proposé de ne pas mesurer le niveau d'anticoagulation.", "2-"),
            ("Si hémorragie", "En cas d'hémorragie sous thromboprophylaxie (AOD, HBPM, HNF, "
             "fondaparinux), les experts suggèrent de déterminer le niveau d'anticoagulation pour "
             "estimer sa contribution à l'hémorragie et aider la prise en charge.*", "AE"),
            ("Procédure d'établissement", "Les experts suggèrent d'établir une procédure "
             "institutionnelle définissant le bon usage de la mesure du niveau d'anticoagulation "
             "(conditions de prélèvement, valeurs seuils) et la prise en charge.", "AE"),
        ], [38*mm, PAGE_W-2*MARGIN-38*mm-16*mm, 16*mm]),
        P("* Cf RFE 2024 SFMU/SFAR/GIHP/SFTH dédiée à la prise en charge des hémorragies sous "
          "anticoagulant.", S_NOTE),
    ]))
    story.append(Spacer(1, 1.5*mm))
    story.append(P("<i>Activités anti-Xa habituellement observées sous enoxaparine 1 injection/j "
                    ": 0,2-0,5 UI/mL au pic (H4). Aucun essai randomisé n'a démontré le bénéfice "
                    "d'une adaptation posologique guidée par l'anti-Xa pour réduire les "
                    "complications ; variabilité inter-tests importante (CV 12-33% pour "
                    "&lt;0,35 UI/mL).</i>", S_NOTE))
    story.append(Spacer(1, 3*mm))

    story.append(KeepTogether([
        section_bar("Monitorage biologique — surveillance plaquettaire et risque de TIH"),
        Spacer(1, 2*mm),
        reco_table([
            ("Numération plaquettaire", "Il est proposé de surveiller la numération plaquettaire "
             "pour un dépistage précoce de TIH : sous HBPM, une à deux fois par semaine entre J4 "
             "et J14 puis une fois par semaine pendant un mois si le traitement est poursuivi ; "
             "sous HNF, deux à trois fois par semaine entre J4 et J14 puis une fois par semaine "
             "pendant un mois ; et en cas de survenue d'une thrombose malgré la "
             "thromboprophylaxie.", "2+"),
        ], [38*mm, PAGE_W-2*MARGIN-38*mm-16*mm, 16*mm]),
    ]))
    return story

# ---------------------------------------------------------------------------
# SECTION 13 — Q17 TVP distale post-opératoire + Figure 2
# ---------------------------------------------------------------------------
def _section_tvp_distale():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(KeepTogether([
        section_bar("Découverte d'une thrombose veineuse profonde distale post-opératoire"),
        Spacer(1, 2*mm),
        reco_table([
            ("Pas de dépistage systématique", "Il est recommandé de ne pas faire de dépistage "
             "systématique des TVP asymptomatiques post-opératoires.", "1-"),
            ("Pas de traitement systématique", "Il est recommandé de ne pas traiter "
             "systématiquement les TVP distales isolées post-opératoires par un anticoagulant à "
             "dose curative.", "1-"),
            ("Évaluer les risques", "En cas de TVP distale isolée post-opératoire, il est "
             "recommandé d'évaluer le risque d'extension thrombotique (TVPd bilatérale ou "
             "multiple, antécédent de MTEV, cancer actif) et le risque hémorragique (patient et "
             "procédure) pour décider des modalités thérapeutiques.", "1+"),
            ("Sans FdR d'extension", "En l'absence de facteur de risque d'extension, il est "
             "proposé d'introduire ou poursuivre la thromboprophylaxie par anticoagulant pendant "
             "35 jours, sans contrôle écho-Doppler.", "2+"),
            ("FdR extension + risque hémorragique faible", "Il est proposé d'introduire un "
             "traitement anticoagulant à dose curative pendant 6 à 12 semaines.", "2+"),
            ("FdR extension + risque hémorragique élevé", "Les experts proposent d'introduire ou "
             "poursuivre la thromboprophylaxie pendant 6 à 12 semaines (contrôle écho-Doppler "
             "possible à J7 ; passage à dose curative si le risque hémorragique diminue).", "AE"),
            ("Anticoagulant contre-indiqué", "En cas de contre-indication à un traitement "
             "anticoagulant préventif, il est proposé de ne pas anticoaguler, de ne pas poser de "
             "filtre cave, et de contrôler l'écho-Doppler à J7 (recherche d'extension "
             "proximale).", "2-"),
        ], [40*mm, PAGE_W-2*MARGIN-40*mm-16*mm, 16*mm]),
    ]))
    story.append(Spacer(1, 1.5*mm))
    story.append(P("<i>Les TVP distales (sous-poplitées, troncs jambiers et veines musculaires) "
                    "représentent jusqu'à la moitié des TVP diagnostiquées, le plus souvent "
                    "asymptomatiques (33-46% de dépistage systématique après PTG). Risque "
                    "d'extension proximale/EP sans anticoagulant : 5-10% (jusqu'à 20% si cancer). "
                    "Essai PROTHEGE : prophylaxie étendue à 35j réduit les complications des TVPd "
                    "vs prophylaxie courte de 10j (extension/récidive 4,5% vs 14,8%, p&lt;0,001).</i>", S_NOTE))
    story.append(Spacer(1, 3*mm))

    story.append(section_bar("Figure 2 (p.74) — Prise en charge d'une TVP distale post-opératoire", color=TEAL_DARK))
    story.append(Spacer(1, 1.5*mm))
    story.append(P("<i>Redessin structuré du diagramme source (image pure).</i>", S_NOTE))
    story.append(Spacer(1, 1.5*mm))
    story.append(flow_label("TVP distale isolée post-opératoire — Risque d'extension thrombotique ? (TVPd bilatérale ou multiple >1 veine ; antécédent de MTEV ; cancer actif)"))
    story.append(flow_row("Absence de facteur de risque d'extension -> thromboprophylaxie par "
                           "anticoagulant pendant 35 jours.", "2+", GREEN_LIGHT))
    story.append(Spacer(1, 1*mm))
    story.append(flow_label("Présence d'un facteur de risque d'extension -> Risque hémorragique lié au patient ou à la procédure ?", bg=NAVY))
    story.append(flow_row("Risque hémorragique FAIBLE -> traitement anticoagulant à dose "
                           "curative pendant 6 à 12 semaines.", "2+", BG_PANEL))
    story.append(Spacer(1, 1*mm))
    story.append(flow_row("Risque hémorragique ÉLEVÉ -> thromboprophylaxie par anticoagulant "
                           "pendant 6 à 12 semaines, ± écho-Doppler à J7, ± relais secondaire par "
                           "traitement à dose curative si le risque diminue.", "AE", BG_PANEL))
    story.append(Spacer(1, 1*mm))
    story.append(flow_row("Anticoagulant contre-indiqué -> pas de traitement anticoagulant, pas "
                           "de filtre cave, contrôle écho-Doppler à J7 (extension proximale).",
                           "2-", AMBER_LIGHT))
    return story

# ---------------------------------------------------------------------------
# SECTION 14 — Figure 3 (synthèse) + Sources et traçabilité
# ---------------------------------------------------------------------------
def _section_synthese():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Figure 3 (p.79) — Thromboprophylaxie post-opératoire : schéma de synthèse", color=TEAL_DARK))
    story.append(Spacer(1, 1.5*mm))
    story.append(P(
        "<i>Redessin structuré du diagramme-image source (le plus utile du document : condense "
        "en un seul schéma la quasi-totalité des recommandations générales déjà détaillées dans "
        "cette fiche). La thromboprophylaxie après PTH/PTG fait l'objet de la Figure 1 dédiée "
        "(page précédente), non reprise ici.</i>", S_NOTE))
    story.append(Spacer(1, 2*mm))

    story.append(flow_label("Risque thromboembolique veineux de la chirurgie ?"))
    story.append(flow_row("FAIBLE + absence de FdR thromboembolique veineux du patient# -> pas "
                           "de prophylaxie pharmacologique ni mécanique.", "1+", GREEN_LIGHT))
    story.append(Spacer(1, 1*mm))
    story.append(flow_row("FAIBLE + FdR patient# présent (1 majeur ou plusieurs mineurs) -> "
                           "anticoagulant, durée minimum 7 jours.", "2+", GREEN_LIGHT))
    story.append(Spacer(1, 1*mm))
    story.append(flow_row("ÉLEVÉ -> anticoagulant, durée fonction de la chirurgie (minimum 7 "
                           "jours ; 4 semaines pour la chirurgie abdomino-pelvienne à risque "
                           "élevé).", "1+", BG_PANEL))
    story.append(Spacer(1, 2*mm))

    story.append(flow_label("Règles transversales (tous les cas)", bg=GREY))
    story.append(flow_row("Déambulation précoce et hydratation optimale, dans tous les cas.",
                           "2+", AMBER_LIGHT))
    story.append(flow_row("Chirurgie programmée : anticoagulant à débuter en post-opératoire, "
                           "entre H12 et H24 (entre H6 et H12 si risque thromboembolique veineux "
                           "élevé lié au patient).", "2+", AMBER_LIGHT))
    story.append(flow_row("Associer anticoagulant + CPI si très haut risque thromboembolique "
                           "veineux (ex. FdR majeur lié au patient + risque chirurgical élevé).",
                           "2+", AMBER_LIGHT))
    story.append(flow_row("Il n'y a pas d'indication à la contention élastique graduée.",
                           "1-", AMBER_LIGHT))
    story.append(Spacer(1, 2*mm))

    cw = PAGE_W - 2*MARGIN
    story.append(info_panel([
        P("<b>Rappel — facteurs de risque thromboembolique veineux du patient# :</b> détail "
          "complet en Q2 (page 2 de cette fiche). Majeurs : ATCD personnel d'ETEV, thrombophilie "
          "majeure connue, cancer actif, obésité morbide (IMC ≥ 40). Modérés/mineurs : âge ≥ 75 "
          "ans, insuffisance cardiorespiratoire/BPCO, insuffisance rénale sévère, maladie "
          "inflammatoire chronique, œstrogènes, grossesse/post-partum, obésité classe I-II, "
          "alitement, déficit neurologique récent, immobilisation post-opératoire.", S_BODY_SM),
        Spacer(1, 1.5*mm),
        P("<b>Rappel — fonction rénale (DFG &lt;30) :</b> enoxaparine 2000 UI x1/j si DFG 15-30 ; "
          "tinzaparine 4500 UI x1/j si DFG &gt;20 ; calciparine 5000 UI x2/j si DFG &lt;15 "
          "(tableau complet en Q11).", S_BODY_SM),
        Spacer(1, 1.5*mm),
        P("<b>Rappel — obésité (IMC ≥ 40) :</b> HBPM (enoxaparine 4000 UI x2/j, ou 6000 UI x2/j "
          "si &gt;150 kg ; daltéparine 5000 UI x2/j ; tinzaparine 75 UI/kg x1/j) ou fondaparinux "
          "5 mg x1/j ou AOD à posologie habituelle. IMC 30-39 : schémas posologiques standards "
          "(détail en Q12).", S_BODY_SM),
    ], bg=BG_PANEL, border=TEAL))
    story.append(Spacer(1, 4*mm))

    story.append(section_bar("Sources et traçabilité", color=GREY))
    story.append(Spacer(1, 2*mm))
    story.append(P(
        "<b>Document source :</b> « Prévention de la maladie thromboembolique veineuse "
        "péri-opératoire » — Recommandations Formalisées d'Experts du Groupe d'intérêt en "
        "Hémostase Péri-opératoire (GIHP), en collaboration avec la SFAR, la SFTH et la SFMV, "
        "endossées par la SFCD, la SFPT et le réseau INNOVTE. Actualisation des recommandations "
        "SFAR de 2011. Coordination : A. Godier, D. Lasne, G. Pernod, et al. ; 37 experts "
        "GIHP/SFTH/SFMV répartis en groupes de travail par question PICO.", S_SOURCE))
    story.append(Spacer(1, 1.5*mm))
    story.append(P("<b>Version :</b> 16.5.2024. Validation SFAR le 30.04.2024, SFTH le 23.02.2024, "
                    "SFVM en janvier 2024. Endossement SFCD (02/2024), SFPT (05/2024), réseau "
                    "INNOVTE (12/2023).", S_SOURCE))
    story.append(P("<b>Méthodologie :</b> GRADE, format PICO. Recommandation forte (1+/1-) si "
                    "niveau de preuve global fort ; optionnelle (2+/2-) si modéré/faible ; avis "
                    "d'experts (AE) en l'absence de littérature suffisante. Validation par vote "
                    "(n=37) : accord fort si ≥70% pour et &lt;20% contre. Vérification exhaustive "
                    "sur l'extraction texte complète (79 pages) : 100% des 77 recommandations "
                    "retrouvées portent la mention d'accord « Fort », aucune exception — d'où "
                    "l'absence de colonne « Accord » dans cette fiche (voir page 1).", S_SOURCE))
    story.append(Spacer(1, 1.5*mm))
    story.append(P("<b>Couverture :</b> intégralité des 77 recommandations individuelles graduées "
                    "des 14 questions PICO (21 sous-thèmes cliniques), transcrites ici en tableaux "
                    "compacts thème/recommandation/grade. Les 3 figures (PTH/PTG p.16 ; TVP "
                    "distale p.74 ; synthèse p.79 — images pures) sont redessinées en "
                    "tableaux/panneaux structurés fidèles aux issues cliniques et grades imprimés "
                    "sur les diagrammes originaux. Le tableau couleur « fonction rénale » (p.52, "
                    "image pure) est reproduit verbatim cellule par cellule. Les tableaux des "
                    "délais neuraxiaux (p.41) et des méta-analyses réanimation (p.63-64, Tableaux "
                    "1-3) sont reproduits verbatim. L'argumentaire complet et les références "
                    "bibliographiques (~400 citations) ne sont pas repris : se référer au texte "
                    "intégral.", S_SOURCE))
    story.append(Spacer(1, 1.5*mm))
    story.append(P("<b>Double extraction :</b> un agent indépendant (contexte vierge, même texte "
                    "source complet) a produit son propre inventaire exhaustif section par "
                    "section ; le total de 77/77 recommandations et leur répartition par section "
                    "ont été confirmés à l'identique, sans écart.", S_SOURCE))
    story.append(Spacer(1, 3*mm))
    story.append(info_panel(P(
        "<b>Avertissement :</b> ce document est une fiche de synthèse indépendante, produite pour "
        "un usage d'aide-mémoire. Il reprend l'intégralité des recommandations graduées et des "
        "tableaux/figures de la RFE source, mais ne remplace pas le texte intégral (argumentaire "
        "complet, ~400 références bibliographiques) et n'est ni édité ni validé par le GIHP, la "
        "SFAR, la SFTH ou la SFMV. En cas de doute, se référer au texte intégral et/ou à un avis "
        "spécialisé.",
        S_BODY_SM), bg=GREY_LIGHT, border=GREY))
    return story

# ---------------------------------------------------------------------------
# Combinators de densité : sections courtes regroupées pour limiter les pages < 60% pleines
# (cf règle de densité du corpus) — toujours rebuild + vérifier le nombre de pages réel après
# fusion (voir rapport final).
def _section_abdo_carcino_vasculaire():
    return _section_abdo_carcino() + [Spacer(1, 3*mm)] + _section_vasculaire()

def _section_irc_obesite():
    return _section_irc() + [Spacer(1, 3*mm)] + _section_obesite()

def _section_reatables_atx_monitorage():
    story = [Spacer(1, 2*mm)]
    story.append(section_bar("Patient de réanimation — méta-analyses (suite)"))
    story.append(Spacer(1, 2*mm))
    story.extend(_section_reanimation_tableaux())
    story.append(Spacer(1, 3*mm))
    story.extend(_section_atx_monitorage())
    return story

SECTIONS = [
    ("Introduction, méthodologie & légende", _section_intro),
    ("Impact des protocoles & facteurs de risque liés au patient", _section_q1_q2),
    ("Orthopédie — PTH/PTG & Figure 1", _section_pth_ptg),
    ("Orthopédie/traumatologie — fractures & gestes non majeurs", _section_fractures),
    ("Chirurgie abdomino-pelvienne, carcinologique & vasculaire", _section_abdo_carcino_vasculaire),
    ("Délai d'introduction & anesthésie locorégionale", _section_delai),
    ("CPI, contentions élastiques & filtre cave", _section_cpi_contention_filtre),
    ("Insuffisance rénale & obésité", _section_irc_obesite),
    ("Pédiatrie & patient de réanimation", _section_pediatrie_reanimation),
    ("Réanimation (méta-analyses), acide tranexamique & monitorage", _section_reatables_atx_monitorage),
    ("TVP distale post-opératoire & Figure 2", _section_tvp_distale),
    ("Figure de synthèse & sources", _section_synthese),
]

def _make_doc(path=None):
    return SimpleDocTemplate(path or OUT, pagesize=A4,
                              leftMargin=MARGIN, rightMargin=MARGIN,
                              topMargin=32*mm, bottomMargin=16*mm,
                              title="RFE GIHP/SFAR/SFTH/SFMV 2024 - Prévention de la MTEV péri-opératoire",
                              author="Synthèse indépendante (source GIHP/SFAR/SFTH/SFMV)")

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
    # Use a throwaway temp path (never OUT) for these measurement-only builds — reusing OUT here
    # was found to corrupt page 1's header_band in the final build of fiche_aap_programmee.py
    # (repeated silent builds to the same path as the real output interfered with the last
    # build's first page). Fixed here from the start by isolating counting passes to their own
    # temp file, explicitly closed and removed after each measurement.
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
