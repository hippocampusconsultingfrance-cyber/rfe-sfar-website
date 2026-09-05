# -*- coding: utf-8 -*-
"""
Fiche de synthese - RFE SFAR 2018
Prevention de l'hypothermie peroperatoire accidentelle au bloc operatoire chez l'adulte.
Texte valide CRC SFAR 12/06/2018, CA SFAR 21/06/2018. Methodologie GRADE.

14 recommandations formalisees (R1-R14) + 1 item "PAS DE RECOMMANDATION" non numerote
(Question 8, rechauffement des fluides gazeux/CO2 coelioscopie - entre R7 et R8, d'ou le
decalage : R8 correspond a la Question 9, pas 8). Repartition per le resume de la source :
5 Grade 1 + 7 Grade 2 + 2 avis d'experts = 14, exactement coherent avec un comptage direct
des 14 items (aucun ecart a signaler cette fois). Accord fort obtenu pour 93% des
recommandations (13/14) - R8 (liquides d'irrigation) est la seule exception avec "Accord
faible" malgre un grade numerique (meme pattern que d'autres fiches du corpus).

R14 est une "Proposition de strategie" (algorithme chronologique accueil -> induction ->
bloc -> SSPI -> sortie SSPI), entierement extractible en texte (pas une image pure) -
transcrite en tableau sequentiel par phase.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from style import *
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.units import mm

OUT = "/private/tmp/claude-501/-Users-macbook-Downloads-claude/65498e3e-5ddf-47a6-b100-3ac535d1faa0/scratchpad/rfe_sfar/output/Fiche_SFAR_Hypothermie_2018.pdf"

SOURCE_TXT = ("Source : Recommandations Formalisées d'Experts « Prévention de l'hypothermie "
              "peropératoire accidentelle au bloc opératoire chez l'adulte » - SFAR. Publié 2018. "
              "Méthodologie GRADE. Fiche de synthèse non officielle : se référer au texte intégral.")

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
    return info_panel(P("<b>Pas de recommandation (Question 8)</b> — " + text, S_BODY_SM), bg=GREY_LIGHT, border=GREY)

TOTAL_PAGES = {"n": 5}

def on_page(canvas, doc, page_title):
    header_band(canvas, doc, "SFAR — RFE 2018 — FICHE DE SYNTHÈSE",
                "Prévention de l'hypothermie peropératoire",
                page_title, icon_fn=lambda c,x,y: icon_drop(c, x, y, 13*mm), color=NAVY)
    footer_band(canvas, doc, SOURCE_TXT, f"Page {doc.page} / {TOTAL_PAGES['n']}")

# ---------------------------------------------------------------------------
def _section_intro_p1():
    story = []
    story.append(Spacer(1, 3*mm))
    story.append(info_panel(P(
        "<b>Champ de la RFE :</b> prévention de l'hypothermie péri-opératoire accidentelle chez "
        "l'adulte au bloc opératoire — première RFE française sur ce sujet. L'hypothermie "
        "péri-opératoire favorise infections, saignements, accidents cardiovasculaires et "
        "surmortalité péri-opératoire ; malgré des moyens de prévention largement utilisés, "
        "une enquête française de 2015 (893 patients) a montré que plus d'1 patient sur 2 arrivait "
        "en SSPI avec une T°C &lt; 36°C (alors que 9 patients sur 10 étaient activement réchauffés — "
        "principal facteur en cause : usage impropre des moyens de réchauffement, démarrage trop "
        "tardif et arrêt trop précoce). RFE sous l'égide de la SFAR.<br/><br/>"
        "<b>14 recommandations</b> formalisées, réparties en 5 Grade 1 + 7 Grade 2 + 2 avis "
        "d'experts (total confirmé par comptage direct des 14 grades littéraux, conforme au "
        "résumé de la source — aucun écart à signaler cette fois). Après trois tours de cotation, "
        "un accord fort a été obtenu pour <b>93 % des recommandations (13/14)</b> — R8 "
        "(réchauffement des liquides d'irrigation) est la seule exception avec un « Accord "
        "faible » malgré son grade numérique 2+. Pour une question (réchauffement des fluides "
        "gazeux/CO2 de cœlioscopie), aucun consensus n'a pu être obtenu : « Pas de "
        "recommandation » (signalé plus bas, entre R7 et R8 — d'où le décalage de numérotation "
        "avec les questions posées).<br/><br/>"
        "<b>Normothermie péri-opératoire :</b> définie par convention comme une température "
        "centrale (T°C) comprise entre 36,5°C et 37,5°C. Sans moyen de réchauffement, la T°C peut "
        "chuter de 2 à 4°C pendant l'anesthésie, principalement par redistribution interne de la "
        "chaleur (80 % de la baisse en anesthésie générale, 89 % en anesthésie neuraxiale durant "
        "la 1<sup>ère</sup> heure).",
        S_BODY), bg=BG_PANEL, border=TEAL))
    story.append(Spacer(1, 3*mm))

    story.append(section_bar("Légende des grades (méthodologie GRADE)"))
    story.append(Spacer(1, 2*mm))
    story.append(legend_flowable())
    story.append(Spacer(1, 4*mm))

    story.append(section_bar("Partie I — Hypothermie : conséquences et seuil cible"))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("R1", "Lutter contre l'hypothermie péri-opératoire afin de diminuer la survenue des "
               "complications infectieuses, cardio-vasculaires et hémorragiques chez le patient "
               "anesthésié.", "1+"),
        ("R2", "Maintenir une T°C ≥ 36,5°C afin de diminuer les complications hémorragiques chez "
               "le patient anesthésié.", "2+"),
    ], [13*mm, PAGE_W-2*MARGIN-13*mm-15*mm, 15*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(P(
        "R1 : essais randomisés (Kurz, Melling — infections de paroi ; Frank, Elmore — événements "
        "cardiaques) ; méta-analyse Rajagopalan (14 études) — lien hypothermie/saignement/"
        "transfusion ; étude Scott (45 304 patients) — compliance aux objectifs de lutte contre "
        "l'hypothermie associée à moins de complications et de mortalité. R2 : 4 études (150, 116, "
        "59, 59 patients) montrent des pertes sanguines significativement plus faibles chez les "
        "patients « normothermes » (T°C ≥ 36,5°C) vs « hypothermes » (T°C proche de 36°C).",
        S_NOTE))
    return story

def _section_partie2a():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Partie II — Techniques de réchauffement"))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("R3", "Effectuer un réchauffement cutané actif avant l'induction de l'anesthésie "
               "(pré-warming) pour prévenir l'hypothermie et/ou diminuer la fréquence des "
               "complications infectieuses.", "2+"),
        ("R4", "Utiliser le réchauffement cutané actif pour diminuer les complications de "
               "l'hypothermie chez le patient anesthésié.", "1+"),
        ("R5", "Privilégier le réchauffement cutané actif au réchauffement passif par isolation "
               "cutanée (vêtements ou couvertures réfléchissants) pour maintenir la T°C.", "2+"),
    ], [13*mm, PAGE_W-2*MARGIN-13*mm-15*mm, 15*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(P(
        "R3 : pré-warming efficace surtout par air pulsé, débuté &gt; 10 min avant l'induction "
        "(réduction du taux d'hypothermie de 52 % en peropératoire et 41 % en postopératoire dans "
        "une étude avant/après de plus de 3800 patients par groupe) — le réchauffement actif doit être "
        "maintenu pendant l'induction pour conserver ce bénéfice. R4 : méta-analyse Madrid, "
        "47 essais — RR infections 0,36 (IC95% 0,20-0,66). R5 : méta-analyse Alderson — pas de "
        "gain à associer réchauffement passif et actif.", S_NOTE))
    return story

def _section_partie2b():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("R6", "Lorsque le volume administré est important, réchauffer les fluides i.v. avec un "
               "matériel dédié, toujours en association avec un réchauffement cutané actif, afin "
               "de limiter la chute de la T°C.", "1+"),
        ("R7", "Réchauffer les produits sanguins labiles avec un matériel dédié, toujours en "
               "association avec un réchauffement cutané actif, afin de limiter la chute de la "
               "T°C et les complications cardiaques liées à leur basse température.", "1+"),
    ], [13*mm, PAGE_W-2*MARGIN-13*mm-15*mm, 15*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(no_reco_panel(
        "les données de la littérature n'ont pas permis d'aboutir à un consensus des experts "
        "concernant le réchauffement des fluides gazeux (gaz anesthésiques, CO2 pour "
        "cœlioscopie) ; aucune recommandation n'a pu être rédigée."))
    story.append(Spacer(1, 2*mm))
    story.append(P(
        "R6 : réchauffement des fluides i.v. maintient une T°C 0,5°C plus élevée (méta-analyse "
        "Campbell) ; pas de volume seuil établi par la littérature — les experts proposent de "
        "réchauffer en cas de volumes inhabituellement importants. R7 : concentrés globulaires "
        "conservés à 4°C — administration rapide/volumes importants abaisse la T°C sous 30°C "
        "(risque d'arythmies/arrêts cardiaques) ; le réchauffement entre 30 et 36°C a réduit "
        "l'incidence des arrêts cardiaques de 58,3 % à 6,8 % lors de transfusions massives.",
        S_NOTE))
    return story

def _section_partie2c():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("R8", "Réchauffer les liquides d'irrigation chirurgicaux avant de les administrer dans "
               "le but de maintenir une T°C > 36°C. Le réchauffement des liquides d'irrigation "
               "seul est cependant insuffisant et doit être accompagné de techniques de "
               "réchauffement cutané actif.", "2+"),
        ("R9", "Ne pas utiliser les aminoacides i.v. pour limiter la chute de la T°C et/ou "
               "diminuer les complications hémorragiques des patients anesthésiés.", "2-"),
        ("R10", "Utiliser les dispositifs de réchauffement actifs sans craindre une augmentation "
                "du risque infectieux attribuable à leur utilisation.", "2+"),
    ], [13*mm, PAGE_W-2*MARGIN-13*mm-15*mm, 15*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(P(
        "<b>R8 est la seule des 14 recommandations à n'avoir obtenu qu'un « Accord Faible »</b> "
        "malgré son grade GRADE 2+ — niveau de preuve faible (essais de faible effectif, "
        "hétérogénéité importante) et un essai annoncé randomisé mais non publié. R9 : aucune "
        "des 3 méta-analyses n'a évalué le maintien d'une T°C &gt; 36°C par les aminoacides. R10 : "
        "13 méta-analyses, aucune n'a montré de risque infectieux ; revue Haeberle (8 études, "
        "chirurgie orthopédique) conclut à l'intérêt des dispositifs à air pulsé malgré des études "
        "de faible niveau de preuve suggérant un risque de contamination.", S_NOTE))
    return story

def _section_partie2d():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("R11", "Les dispositifs de réchauffement actif peuvent être pourvoyeurs de complications "
                "à type de brûlure en cas d'usage inapproprié.", "AE"),
    ], [13*mm, PAGE_W-2*MARGIN-13*mm-15*mm, 15*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(P(
        "Couvertures à air pulsé : accidents le plus souvent dus à une mauvaise utilisation "
        "(générateur non rattaché à une couverture/combinaison dédiée, objets déposés sur la "
        "couverture, réchauffement à température maximale prolongé) ; surveillance cutanée "
        "renforcée si zone insensibilisée, mal perfusée ou en pédiatrie. Dispositifs électriques et "
        "à eau chauffée : risque de surchauffe/escarres. Méthodes « artisanales » (solutés ou "
        "draps chauffés non homologués) : première cause de brûlures péri-opératoires — à "
        "proscrire. Produits sanguins : pas de contre-indication à réchauffer jusqu'à 43-45°C "
        "(hémolyse négligeable).", S_NOTE))
    return story

def _section_partie2e_fig_trace():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("R12", "En cas d'hypothermie à l'arrivée en SSPI, utiliser un dispositif de réchauffement "
                "cutané actif pour atteindre la normothermie le plus rapidement possible.", "1+"),
        ("R13", "Préférer les dispositifs utilisant l'air chaud pulsé aux dispositifs à circulation "
                "d'eau chaude pour atteindre la normothermie.", "2+"),
    ], [13*mm, PAGE_W-2*MARGIN-13*mm-15*mm, 15*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(P(
        "R12-R13 : méta-analyse Warttig (11 essais, 699 patients) — le réchauffement cutané actif "
        "atteint la normothermie 32 min plus vite qu'une couverture en coton préalablement "
        "chauffée, et 89 min plus vite qu'une couverture en coton non chauffée ; l'air chaud pulsé "
        "est plus rapide de 54 min que la circulation d'eau chaude (niveau de preuve faible, "
        "2 études, 36 patients/bras).", S_NOTE))
    story.append(Spacer(1, 4*mm))

    story.append(KeepTogether([
        P("<b>R14 — Proposition de stratégie de prévention de l'hypothermie accidentelle "
          "péri-anesthésique</b>", S_H2),
        Spacer(1, 1*mm),
        chip("AE", width=15*mm),
        Spacer(1, 1*mm),
        simple_table(
            ["Phase", "Actions"],
            [
                ["Accueil du patient\n(bloc opératoire)",
                 "T° salle d'opération : 20°C à l'accueil et pendant l'induction. Mesure T°C de "
                 "départ. Réchauffement cutané actif avant l'induction (pré-warming, R3 — 2+) puis "
                 "pendant l'induction. Objectifs : réchauffer, dépister une hypothermie."],
                ["Per-anesthésie\n(bloc opératoire)",
                 "Monitorage per-anesthésique continu de la T°C. Réchauffement : cutané actif "
                 "(R4 — 1+), fluides i.v. (R6 — 1+), produits sanguins labiles (R7 — 1+), liquides "
                 "d'irrigation (R8 — 2+). Objectifs : réchauffer, maintenir la T°C à 36,5°C, ne pas "
                 "passer sous le seuil de 36°C."],
                ["SSPI (service)",
                 "Mesure T°C à l'arrivée en SSPI. Réchauffement cutané actif si hypothermie "
                 "(R12 — 1+), par air chaud pulsé de préférence (R13 — 2+). Mesure T°C à la sortie "
                 "de SSPI. Objectifs : réchauffer, T°C à 36,5°C."],
            ], [32*mm, PAGE_W-2*MARGIN-32*mm])
    ]))
    story.append(Spacer(1, 4*mm))

    story.append(section_bar("Sources et traçabilité", color=GREY))
    story.append(Spacer(1, 2*mm))
    story.append(P(
        "<b>Document source :</b> « Prévention de l'hypothermie peropératoire accidentelle au "
        "bloc opératoire chez l'adulte » — Recommandations Formalisées d'Experts, SFAR. Auteurs : "
        "P. Alfonsi, F. Espitalier, M.-P. Bonnet, S. Bekka, L. Brocker, F. Garnier, M. Louis, "
        "I. Macquer, P. Pilloy, C. Hallynck, Y. Camus. Coordonnateur : P. Alfonsi. Comité "
        "d'organisation : F. Espitalier.",
        S_SOURCE))
    story.append(Spacer(1, 1.5*mm))
    story.append(P("<b>Version :</b> texte validé par le Comité des Référentiels Cliniques de la "
                    "SFAR le 12/06/2018 et le Conseil d'Administration de la SFAR le 21/06/2018.",
                    S_SOURCE))
    story.append(P("<b>Méthodologie :</b> GRADE (force forte [1+/1-] ou faible [2+/2-] ; avis "
                    "d'experts lorsque la littérature ne permettait pas de graduer). Accord fort "
                    "obtenu pour 93 % des recommandations (13/14) après 3 tours de cotation.",
                    S_SOURCE))
    story.append(P("<b>URL source :</b> https://sfar.org/prevention-de-lhypothermie-peroperatoire-accidentelle-au-bloc-operatoire-chez-ladulte/", S_SOURCE))
    story.append(Spacer(1, 3*mm))
    story.append(info_panel(P(
        "<b>Avertissement :</b> ce document est une fiche de synthèse indépendante, produite pour "
        "un usage d'aide-mémoire. Il reprend l'intégralité des 14 recommandations, de l'item "
        "« pas de recommandation » et de la stratégie proposée (R14) de la RFE, mais ne remplace "
        "pas le texte intégral (argumentaire complet, références bibliographiques par "
        "recommandation) et n'est ni édité ni validé par la SFAR. En cas de doute, se référer au "
        "texte intégral et/ou à un avis spécialisé.",
        S_BODY_SM), bg=GREY_LIGHT, border=GREY))
    return story

def _section_1():
    return _section_intro_p1()

def _section_2():
    return (_section_partie2a() + [Spacer(1, 3*mm)] + _section_partie2b()
            + [Spacer(1, 3*mm)] + _section_partie2c())

def _section_3():
    return _section_partie2d() + [Spacer(1, 3*mm)] + _section_partie2e_fig_trace()

SECTIONS = [
    ("Partie I — Hypothermie, conséquences, seuil", _section_1),
    ("Partie II — Réchauffement cutané, fluides, irrigation", _section_2),
    ("Partie II — Brûlures, SSPI, stratégie, traçabilité", _section_3),
]

def _make_doc():
    return SimpleDocTemplate(OUT, pagesize=A4,
                              leftMargin=MARGIN, rightMargin=MARGIN,
                              topMargin=32*mm, bottomMargin=16*mm,
                              title="Fiche SFAR 2018 - Prévention de l'hypothermie peropératoire",
                              author="Synthèse indépendante (source SFAR)")

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
