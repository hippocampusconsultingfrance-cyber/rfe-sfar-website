# -*- coding: utf-8 -*-
"""
Fiche de synthese - RFE commune SFAR-SRLF 2019 (avec SFTS, SFVTT)
Gestion et prevention de l'anemie (hors hemorragie aigue) chez le patient adulte de soins
critiques. Valide CA SFAR 20/06/2019, CA SRLF 26/06/2019. Exclut hemorragie aigue et anemies
chroniques. Methodologie GRADE. 16 experts (comptage direct de la liste "Auteurs" en page 1 -
confirme, pas d'ecart a signaler cette fois, contrairement a d'autres fiches recentes du corpus).

3 champs : (1) prevention non pharmacologique, (2) strategies transfusionnelles, (3) traitement
non transfusionnel. 10 recommandations formelles (R1.1, R2.1-2.6, R3.1-3.3) + 1 item numerote
"R3.4" explicitement "Absence de recommandation" (vitamines B12/folates) - distinct des autres
fiches du corpus ou l'absence de recommandation est non-numerotee.

Repartition par grade : 3 Grade 1 (R2.1, R2.2, R2.5) + 4 Grade 2 (R2.3, R2.4, R3.1, R3.3) + 3 avis
d'experts (R1.1, R2.6, R3.2) = 10, correspondant exactement au total annonce par le resume de la
source. Le resume annonce cependant "3 grade eleve + 4 grade faible + 2 avis d'experts" (3+4+2=9,
pas 10) - incoherence arithmetique interne au resume de la source, non reconciliee : un comptage
direct confirme 3 avis d'experts (pas 2), ce qui reconcilie le total a 10.

1 figure (Figure 1, cibles d'hemoglobine transfusionnelles par contexte clinique - bandes
degradees/floues representant l'incertitude, verifiee par rendu visuel a 200dpi de la page 13
source) transcrite en tableau avec les seuils exacts deja donnes par R2.1-R2.4 dans le texte, et
les bornes hautes approximatives lues sur le graphique (le flou du graphique represente lui-meme
l'incertitude des experts - disclose explicitement, pas de fausse precision).
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from style import *
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.units import mm

OUT = "/private/tmp/claude-501/-Users-macbook-Downloads-claude/65498e3e-5ddf-47a6-b100-3ac535d1faa0/scratchpad/rfe_sfar/output/Fiche_SFAR_SRLF_Anemie_2019.pdf"

SOURCE_TXT = ("Source : Recommandations Formalisées d'Experts « Gestion et prévention de l'anémie "
              "(hors hémorragie aigüe) chez le patient adulte de soins critiques » - SFAR, SRLF, avec "
              "SFTS, SFVTT. Publié 2019. Méthodologie GRADE. Fiche de synthèse non officielle : se "
              "référer au texte intégral.")

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

def no_reco_panel(text):
    return info_panel(P("<b>Absence de recommandation (R3.4)</b> — " + text, S_BODY_SM), bg=GREY_LIGHT, border=GREY)

TOTAL_PAGES = {"n": 4}

def on_page(canvas, doc, page_title):
    header_band(canvas, doc, "SFAR / SRLF (avec SFTS, SFVTT) — RFE 2019 — FICHE DE SYNTHÈSE",
                "Gestion et prévention de l'anémie",
                page_title, icon_fn=lambda c,x,y: icon_drop(c, x, y, 13*mm), color=NAVY)
    footer_band(canvas, doc, SOURCE_TXT, f"Page {doc.page} / {TOTAL_PAGES['n']}")

# ---------------------------------------------------------------------------
def _section_intro_champ1():
    story = []
    story.append(Spacer(1, 3*mm))
    story.append(info_panel(P(
        "<b>Champ de la RFE :</b> prévention et prise en charge de l'anémie (définition, seuils "
        "transfusionnels, alternatives à la transfusion) chez le patient adulte de soins critiques "
        "— <b>hors hémorragie aiguë et anémies chroniques</b>, exclues du champ. L'anémie touche "
        "près de 2/3 des patients à l'admission en soins critiques et s'aggrave au cours du séjour "
        "(spoliations sanguines répétées, inflammation, hémodilution) ; elle est associée à la "
        "gravité et à la durée de séjour. RFE sous l'égide de la SFAR et de la SRLF, avec la SFTS "
        "(Société Française de Transfusion Sanguine) et la SFVTT (Société Française de Vigilance "
        "et de Thérapeutique Transfusionnelle) — <b>16 experts</b> (comptage direct de la liste "
        "des auteurs, confirmé — pas d'écart à signaler cette fois, contrairement à d'autres "
        "documents de ce corpus).<br/><br/>"
        "<b>Trois champs :</b> (1) prévention non pharmacologique de l'anémie, (2) stratégies "
        "transfusionnelles, (3) traitement non transfusionnel. <b>10 recommandations</b> "
        "formalisées, réparties en 3 Grade 1 + 4 Grade 2 + 3 avis d'experts (total confirmé par "
        "comptage direct des 10 grades littéraux). Le résumé de la source annonce cependant "
        "« 3 grade élevé, 4 grade faible et 2 avis d'experts » — une somme de 9, pas 10 : "
        "incohérence arithmétique interne au résumé, non reconciliée ici (un comptage direct des "
        "10 recommandations donne bien 3 avis d'experts, ce qui reconcilie le total correct de 10). "
        "Après deux tours de cotation, un accord fort a été obtenu pour l'ensemble des "
        "recommandations. Un item numéroté (R3.4) est une « Absence de recommandation » "
        "explicite (signalée plus bas).",
        S_BODY), bg=BG_PANEL, border=TEAL))
    story.append(Spacer(1, 3*mm))

    story.append(section_bar("Légende des grades (méthodologie GRADE)"))
    story.append(Spacer(1, 2*mm))
    story.append(legend_flowable())
    story.append(Spacer(1, 4*mm))

    story.append(section_bar("Champ 1 — Prévention non pharmacologique de l'anémie"))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("R1.1", "Appliquer une stratégie de réduction des prélèvements sanguins (en volume et en "
                 "nombre) pour diminuer l'incidence de l'anémie et la transfusion en soins "
                 "critiques.", "AE"),
    ], [13*mm, PAGE_W-2*MARGIN-13*mm-15*mm, 15*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(P(
        "Prélèvements sanguins diagnostiques : 40-80 mL/jour en moyenne. Moyens : stratégies de "
        "réduction des examens complémentaires, réduction des volumes prélevés, systèmes de "
        "restitution du sang après prélèvement sur cathéter artériel (réduction du volume prélevé "
        "de 19 à 80 % selon les études).", S_NOTE))
    return story

def _section_champ2a():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Champ 2 — Stratégies transfusionnelles"))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("R2.1", "Suivre une stratégie transfusionnelle restrictive (seuil d'Hb à 7,0 g/dL) chez "
                 "les patients de soins critiques en général, y compris les patients septiques, "
                 "afin de réduire le recours à la transfusion de concentrés érythrocytaires sans "
                 "augmenter la morbi-mortalité.", "1+"),
        ("R2.2", "Suivre une stratégie transfusionnelle restrictive (seuil d'Hb entre 7,5 et "
                 "8,0 g/dL) chez les patients de soins critiques en post-opératoire de chirurgie "
                 "cardiaque, afin de réduire le recours à la transfusion de concentrés "
                 "érythrocytaires sans augmenter la morbi-mortalité.", "1+"),
        ("R2.3", "Ne pas suivre une stratégie transfusionnelle libérale ciblant un objectif d'Hb "
                 "> 10,0 g/dL pour diminuer la morbi-mortalité chez les patients ayant un syndrome "
                 "coronarien aigu, revascularisé ou non.", "2-"),
        ("R2.4", "Ne pas suivre une stratégie transfusionnelle libérale ciblant un objectif d'Hb "
                 "> 10,0 g/dL pour diminuer la morbi-mortalité chez les patients cérébrolésés.", "2-"),
    ], [13*mm, PAGE_W-2*MARGIN-13*mm-15*mm, 15*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(P(
        "Ces cibles s'appliquent en dehors d'hémorragie active ou de mauvaise tolérance de "
        "l'anémie (notamment cardio-vasculaire).", S_NOTE))
    return story

def _section_fig1():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(KeepTogether([
        P("<b>FIGURE 1</b> — Taux d'hémoglobine à cibler en cas de transfusion (avis d'experts)", S_H2),
        Spacer(1, 1*mm),
        P("<i>Redessin en tableau du graphique en bandes dégradées de la page 13 du document "
          "source (vérifié visuellement à 200dpi) — le flou des bandes représente le degré "
          "d'incertitude des experts eux-mêmes ; les valeurs ci-dessous sont donc volontairement "
          "approximatives (fourchettes), pas des seuils exacts, sauf pour R2.1-R2.2 (seuils "
          "précis donnés dans le texte des recommandations elles-mêmes).</i>", S_NOTE),
        Spacer(1, 1.5*mm),
        simple_table(
            ["Contexte clinique", "Hb cible (g/dL, approximatif)", "Grade"],
            [
                ["Réanimation générale", "≈ 7,0 - 9,0", "Grade 1"],
                ["Traumatisme", "≈ 7,0 - 9,0", "Grade 1"],
                ["Sepsis", "≈ 7,0 - 9,0", "Grade 1"],
                ["Lésions cérébrales", "≈ 7,0 - 9,5", "Grade 2"],
                ["Post-opératoire chirurgie cardiaque", "7,5 - 8,0 (R2.2)", "Grade 1"],
                ["Syndrome coronarien aigu", "≈ 7,3 - 9,5 (pas de cible > 10,0, R2.3)", "Grade 2"],
            ], [58*mm, PAGE_W-2*MARGIN-58*mm-22*mm, 22*mm])
    ]))
    return story

def _section_champ2b_champ3a():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("R2.5", "Ne pas choisir les concentrés érythrocytaires en fonction de leur durée de "
                 "stockage pour diminuer la morbi-mortalité chez les patients de soins "
                 "critiques.", "1-"),
        ("R2.6", "Adopter une stratégie transfusionnelle restrictive basée sur la transfusion "
                 "d'un concentré érythrocytaire unitaire suivie d'une réévaluation de "
                 "l'indication transfusionnelle, afin de réduire la consommation de concentrés "
                 "érythrocytaires sans augmenter la morbi-mortalité.", "AE"),
    ], [13*mm, PAGE_W-2*MARGIN-13*mm-15*mm, 15*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(P(
        "R2.5 : durée maximale de conservation en France = 42 jours ; deux essais randomisés de "
        "grande ampleur (ABLE 2430 patients, TRANSFUSE 4828 patients) n'ont retrouvé aucun impact "
        "de la durée de conservation sur le pronostic.", S_NOTE))
    story.append(Spacer(1, 4*mm))

    story.append(section_bar("Champ 3 — Traitement non transfusionnel de l'anémie"))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("R3.1", "Utiliser des agents stimulants de l'érythropoïèse (ASE) chez les patients de "
                 "soins critiques anémiques (Hb ≤ 10-12 g/dL) et/ou traumatisés, en l'absence de "
                 "contre-indication (notamment antécédents cardio-vasculaires ischémiques et/ou "
                 "thrombo-emboliques veineux), afin de réduire le recours à la transfusion de "
                 "concentrés érythrocytaires et de diminuer la mortalité.", "2+"),
        ("R3.2", "Arrêter les agents stimulants de l'érythropoïèse lorsque l'hémoglobine se "
                 "stabilise entre 10,0 et 12,0 g/dL, afin de réduire la morbi-mortalité.", "AE"),
    ], [13*mm, PAGE_W-2*MARGIN-13*mm-15*mm, 15*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(P(
        "R3.1 : dose la plus utilisée = 40 000 UI/semaine SC, associée à un apport de fer. "
        "R3.2 : à partir de 12,0 g/dL (≥12,0), une cible haute d'Hb augmente la mortalité (méta-analyse "
        "hors soins critiques, RR 1,17) et le risque de thrombose des accès vasculaires (RR 1,34).",
        S_NOTE))
    return story

def _section_champ3b_trace():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("R3.3", "En dehors d'une association avec un traitement par agent stimulant de "
                 "l'érythropoïèse, ne pas administrer de fer pour réduire le recours à la "
                 "transfusion érythrocytaire ou la morbi-mortalité.", "2-"),
    ], [13*mm, PAGE_W-2*MARGIN-13*mm-15*mm, 15*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(no_reco_panel(
        "il n'a pas été possible de formuler de recommandation concernant l'administration de "
        "vitamines chez le patient de réanimation dans l'objectif de réduire la transfusion "
        "érythrocytaire et/ou la morbi-mortalité liée à l'anémie ou à la transfusion."))
    story.append(Spacer(1, 2*mm))
    story.append(P(
        "R3.3 : une méta-analyse combinant fer intraveineux (5 études) et fer par voie orale "
        "(1 étude) augmente l'Hb à la sortie de l'hôpital mais sans moindre recours à la "
        "transfusion pendant le séjour, et l'augmentation d'Hb est de pertinence clinique très "
        "faible (+0,31 g/dL). Risque de réaction anaphylactique (fer injectable) : 68/100 000 "
        "(fer dextran), 24/100 000 (fer sans dextran), minimal avec le fer sucrose. "
        "R3.4 (Question 3, vitamine B12/acide folique) : aucune donnée pour la B12 ; deux essais "
        "randomisés inconclusifs pour l'acide folique (absence de groupe contrôle ou déséquilibre "
        "des groupes à l'admission).", S_NOTE))
    story.append(Spacer(1, 4*mm))

    story.append(section_bar("Sources et traçabilité", color=GREY))
    story.append(Spacer(1, 2*mm))
    story.append(P(
        "<b>Document source :</b> « Gestion et prévention de l'anémie (hors hémorragie aiguë) chez "
        "le patient adulte de soins critiques » — Recommandations Formalisées d'Experts, SFAR et "
        "SRLF, avec la SFTS et la SFVTT. Auteurs : S. Lasocki, F. Pène, H. Ait Oufella, C. Aubron, "
        "S. Ausset, P. Buffet, O. Huet, Y. Launey, M. Legrand, T. Lescot, A. Mekontso Dessap, "
        "M. Piagnerelli, H. Quintard, L. Velly, A. Kimmoun, G. Chanques (16 experts). "
        "Coordonnateurs : S. Lasocki (SFAR), F. Pène (SRLF).",
        S_SOURCE))
    story.append(Spacer(1, 1.5*mm))
    story.append(P("<b>Version :</b> texte validé par le CA de la SFAR le 20/06/2019 et le CA de "
                    "la SRLF le 26/06/2019.", S_SOURCE))
    story.append(P("<b>Méthodologie :</b> GRADE (force forte [1+/1-] ou faible [2+/2-] ; avis "
                    "d'experts lorsque la littérature ne permettait pas de graduer). Accord fort "
                    "obtenu pour l'ensemble des recommandations après 2 tours de cotation et un "
                    "amendement.", S_SOURCE))
    story.append(P("<b>URL source :</b> https://sfar.org/gestion-et-prevention-de-lanemie-hors-hemorragie-aigue-chez-le-patient-adulte-de-soins-critiques/", S_SOURCE))
    story.append(Spacer(1, 3*mm))
    story.append(info_panel(P(
        "<b>Avertissement :</b> ce document est une fiche de synthèse indépendante, produite pour "
        "un usage d'aide-mémoire. Il reprend l'intégralité des 10 recommandations, de l'item "
        "« absence de recommandation » (R3.4) et de la Figure 1 de la RFE, mais ne remplace pas "
        "le texte intégral (argumentaire complet, références bibliographiques par recommandation) "
        "et n'est ni édité ni validé par la SFAR ni la SRLF. En cas de doute, se référer au texte "
        "intégral et/ou à un avis spécialisé.",
        S_BODY_SM), bg=GREY_LIGHT, border=GREY))
    return story

def _section_1():
    return _section_intro_champ1() + [Spacer(1, 3*mm)] + _section_champ2a()

def _section_2():
    return (_section_fig1() + [Spacer(1, 3*mm)] + _section_champ2b_champ3a()
            + [Spacer(1, 3*mm)] + _section_champ3b_trace())

SECTIONS = [
    ("Champ 1-2 — Prévention, seuils transfusionnels", _section_1),
    ("Champ 2-3 — Figure, calibre, ASE, fer, traçabilité", _section_2),
]

def _make_doc():
    return SimpleDocTemplate(OUT, pagesize=A4,
                              leftMargin=MARGIN, rightMargin=MARGIN,
                              topMargin=32*mm, bottomMargin=16*mm,
                              title="Fiche SFAR/SRLF 2019 - Gestion et prévention de l'anémie",
                              author="Synthèse indépendante (source SFAR/SRLF/SFTS/SFVTT)")

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
