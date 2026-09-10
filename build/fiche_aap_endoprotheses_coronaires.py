# -*- coding: utf-8 -*-
"""
Fiche de synthese - SFAR, "Information professionnelle" (2006)
"Gestion du traitement antiplaquettaire oral chez les patients porteurs
d'endoprothèses coronaires" - Albaladejo P, Marret E, Piriou V, Samama CM, et le
groupe de travail. Ann Fr Anesth Reanim 2006;25:796-798.

CONTEXTE : ce document precede de 12 ans les propositions GIHP/GFHT/SFAR 2018 deja
construites dans ce corpus (fiche_aap_programmee.py pour la procedure programmee,
fiche_aap_urgence.py pour l'urgence/hemorragie). Il est plus ancien, beaucoup plus
court (3 pages source), et porte SPECIFIQUEMENT sur les patients porteurs
d'endoprotheses coronaires (EC/stents) - un sous-cas plus etroit que les fiches 2018
qui couvrent tout AAP (prevention primaire, secondaire, EC). Conserve comme document
distinct plutot que fusionne : c'est le document historique cite en reference [1] par
la fiche "aap_programmee", et il contient une matrice de decision (Tableau 1) propre
a ce contexte specifique (double critere thrombose du stent x risque hemorragique de
l'intervention) qui n'est pas reproduite telle quelle dans les fiches 2018. Une
cross-reference vers les 2 fiches 2018 est incluse dans le panneau d'introduction.

METHODOLOGIE : PAS de systeme GRADE, pas de vote/pourcentage d'accord formalise (a
la difference des propositions GIHP/GFHT 2018). Le document est explicitement un
« avis d'un groupe d'experts » (10 propositions listees a puces, "PROPOSITIONS DU
GROUPE D'EXPERTS, 31 MARS 2006" - les 2 dernieres, registre et carte de liaison,
condensees en une seule ligne thematique ici puisqu'elles partagent un theme "suivi/
tracabilite" commun, sans perte de contenu), sans tag de force individuel imprime a cote de
chaque proposition. La source elle-meme souligne a plusieurs reprises l'absence de
preuve de haut niveau ("Cette proposition ne repose sur aucune etude prospective",
"reposent sur des avis d'experts, en l'absence d'etude de haut niveau de preuve") -
disclosure reprise telle quelle dans le panneau de methodologie plutot que de
suggerer une force uniforme non imprimee par la source. Aucun chip GRADE n'est donc
invente ici (a la difference de fiche_aap_programmee.py qui utilise un chip "Fort"
imprime explicitement par CETTE AUTRE source) : les propositions sont presentees en
liste thematique sans colonne de grade.

TABLEAU 1 (page 2 source, matrice de decision) : pure image/mise en page graphique,
sans couche de texte extractible en tableau (confirme par extraction PyMuPDF -
seul le libelle "Tableau 1" et son renvoi textuel sont extractibles, pas son
contenu). Rendu visuellement a 220dpi et retranscrit integralement ici sans
paraphrase : matrice 2 lignes (risque de thrombose du stent : Majeur/Modere) x
3 colonnes (risque hemorragique de l'intervention : Majeur/Intermediaire/Mineur),
plus les 2 encadres de definition des criteres et la note de bas de tableau.

COUVERTURE : 10/10 propositions du corps du texte (condensees en 9 lignes thematiques,
voir note methodologie ci-dessus) + Tableau 1 integral + reference a
la carte de liaison AAP. Comite de redaction, adresses institutionnelles et les 13
references bibliographiques ne sont pas retranscrits (sans contenu clinique
actionnable).
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from style import *
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.units import mm

OUT = "/home/user/rfe-sfar-website/output/Fiche_SFAR_AAP_Endoprotheses_Coronaires_2006.pdf"

SOURCE_TXT = ("Source : Albaladejo P, Marret E, Piriou V, Samama CM, et le groupe de travail — "
              "« Gestion du traitement antiplaquettaire oral chez les patients porteurs "
              "d'endoprothèses coronaires » — SFAR, Ann Fr Anesth Reanim 2006;25:796-798. Fiche de "
              "synthèse non officielle : se référer au texte intégral.")

def P(txt, style=S_CELL):
    return Paragraph(txt, style)

def prop_table(rows, col_widths=None):
    """rows: (theme, text) - ce document n'a ni numerotation R1/R2 ni tag de force
    individuel ; theme remplace la colonne Ref./Grade habituelle."""
    cw = PAGE_W - 2 * MARGIN
    if col_widths is None:
        theme_w = 34 * mm
        col_widths = [theme_w, cw - theme_w]
    data = [[P("Thème", S_HEAD_W), P("Proposition (texte condensé, fidèle à la source)", S_HEAD_W)]]
    for theme, txt in rows:
        data.append([P(theme, S_CELL_B), P(txt, S_CELL)])
    t = Table(data, colWidths=col_widths, repeatRows=1)
    style_cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), NAVY), ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTNAME", (0, 0), (-1, 0), FONT_BOLD), ("FONTSIZE", (0, 0), (-1, 0), 8),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.5, GREY_LIGHT),
        ("TOPPADDING", (0, 0), (-1, -1), 3.4), ("BOTTOMPADDING", (0, 0), (-1, -1), 3.4),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            style_cmds.append(("BACKGROUND", (0, i), (-1, i), BG_PANEL))
    t.setStyle(TableStyle(style_cmds))
    return t

def risk_matrix_table():
    """Tableau 1 (page 797 source) - matrice de decision : risque de thrombose du
    stent (lignes, a evaluer avec le cardiologue) x risque hemorragique de
    l'intervention (colonnes, a evaluer avec le chirurgien). Contenu retranscrit
    depuis le rendu visuel 220dpi de la page source (pas de texte extractible -
    voir docstring du module)."""
    cw = PAGE_W - 2 * MARGIN
    c0 = 26 * mm
    c1 = c2 = c3 = (cw - c0) / 3.0

    S_MX = pstyle("mx2", fontSize=7.5, leading=9.2, textColor=INK)
    S_MX_HEAD = pstyle("mx2_head", fontSize=8.0, leading=9.8, textColor=WHITE, fontName=FONT_BOLD, alignment=TA_CENTER)
    S_MX_ROW = pstyle("mx2_row", fontSize=7.8, leading=9.4, textColor=WHITE, fontName=FONT_BOLD, alignment=TA_CENTER)

    def mc(txt, style=S_MX):
        return Paragraph(txt, style)

    data = [
        [mc("Risque de thrombose du stent \\ Risque hémorragique de l'intervention", S_MX_HEAD),
         mc("Majeur", S_MX_HEAD), mc("Intermédiaire", S_MX_HEAD), mc("Mineur", S_MX_HEAD)],
        [mc("Majeur", S_MX_ROW),
         mc("Reporter l'intervention au-delà de 6 mois à 1 an après la pose de l'EC. "
            "Si impossible : arrêt aspirine-clopidogrel 5 jours, ou arrêt aspirine-clopidogrel "
            "10 jours maxi et substitution."),
         mc("Reporter l'intervention au-delà de 6 mois à 1 an après la pose de l'EC. "
            "Si impossible : maintien aspirine, arrêt clopidogrel 5 jours."),
         mc("Maintien aspirine et clopidogrel.")],
        [mc("Modéré", S_MX_ROW),
         mc("Arrêt aspirine-clopidogrel 5 jours, ou arrêt aspirine-clopidogrel 10 jours maxi "
            "et substitution."),
         mc("Maintien aspirine, arrêt clopidogrel 5 jours."),
         mc("Maintien aspirine et clopidogrel, ou maintien aspirine et arrêt clopidogrel "
            "5 jours.")],
    ]
    t = Table(data, colWidths=[c0, c1, c2, c3])
    style_cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), TEAL_DARK),
        ("BACKGROUND", (0, 1), (0, 1), NAVY), ("BACKGROUND", (0, 2), (0, 2), NAVY),
        ("BACKGROUND", (1, 1), (-1, 1), WHITE),
        ("BACKGROUND", (1, 2), (-1, 2), BG_PANEL),
        ("GRID", (0, 0), (-1, -1), 0.5, GREY_LIGHT),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 3.4), ("BOTTOMPADDING", (0, 0), (-1, -1), 3.4),
        ("LEFTPADDING", (0, 0), (-1, -1), 4), ("RIGHTPADDING", (0, 0), (-1, -1), 4),
    ]
    t.setStyle(TableStyle(style_cmds))
    return t

TOTAL_PAGES = {"n": 2}

def on_page(canvas, doc, page_title):
    header_band(canvas, doc, "SFAR — 2006 — FICHE DE SYNTHÈSE",
                "AAP oral & endoprothèses coronaires",
                page_title, icon_fn=lambda c, x, y: icon_pill(c, x, y, 13 * mm), color=NAVY)
    footer_band(canvas, doc, SOURCE_TXT, f"Page {doc.page} / {TOTAL_PAGES['n']}")

# ---------------------------------------------------------------------------
def _section_propositions():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Champ :</b> gestion périopératoire du traitement antiplaquettaire oral (AAP — "
        "aspirine, clopidogrel) chez les patients porteurs d'une <b>endoprothèse coronaire</b> "
        "(EC, « stent »), nue ou pharmacoactive, devant subir un acte invasif médical ou "
        "chirurgical. Document historique (2006), <b>antérieur aux propositions GIHP/GFHT/SFAR "
        "2018</b> déjà couvertes dans ce corpus pour la gestion générale des AAP (voir fiches "
        "« AAP — procédure programmée » et « AAP — procédure non programmée / hémorragie »), "
        "mais conservé ici pour son objet plus étroit et sa matrice de décision propre au "
        "contexte « stent coronaire ».", S_BODY), bg=BG_PANEL, border=NAVY))
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Méthodologie :</b> avis d'un groupe d'experts (« Propositions du groupe d'experts, "
        "31 mars 2006 »), <b>sans système GRADE et sans vote/pourcentage d'accord formalisé</b> "
        "(à la différence des propositions GIHP/GFHT 2018 plus récentes). La source souligne "
        "elle-même, à plusieurs reprises, l'absence de données de haut niveau de preuve "
        "(« ne repose sur aucune étude prospective », « avis d'experts, en l'absence d'étude de "
        "haut niveau de preuve ») — disclosure reprise ici telle quelle plutôt que de suggérer "
        "une force uniforme non imprimée par la source.", S_BODY_SM), bg=BG_PANEL, border=AMBER))
    story.append(Spacer(1, 3 * mm))

    story.append(section_bar("Propositions du groupe d'experts (31 mars 2006)", color=TEAL_DARK))
    story.append(Spacer(1, 2 * mm))
    story.append(prop_table([
        ("Durée du double traitement AAP", "Maintenir le double traitement AAP au moins 4 à "
         "6 semaines après l'implantation d'une EC nue, et au moins 6 à 12 mois en cas d'EC "
         "pharmacoactive."),
        ("Risque de thrombose", "En cas de traitement AAP bien conduit, le risque de thrombose "
         "aiguë serait le même quelle que soit la nature de l'EC. L'arrêt des AAP est un "
         "facteur de risque majeur de thrombose pour tous les stents, en particulier de "
         "thrombose tardive pour les EC pharmacoactives — ce qui justifie a priori un "
         "traitement AAP prolongé. <i>La fréquence réelle de thrombose d'EC pharmacoactive en "
         "contexte périopératoire reste inconnue à ce jour : seuls des cas cliniques isolés "
         "sont rapportés dans la littérature.</i>"),
        ("Choix du stent avant chirurgie prévue", "La pose d'une EC doit toujours être discutée "
         "en amont ; si une chirurgie est envisagée dans les 6 à 12 mois, la pose d'une EC nue "
         "est préférable. Avant l'implantation d'une EC pharmacoactive, la possible réalisation "
         "d'une chirurgie ultérieure doit toujours être évoquée."),
        ("Patients à très haut risque de thrombose", "Identifier en particulier : arrêt des AAP "
         "dans les 6 à 12 mois après la pose de l'EC, antécédent de thrombose de stent, "
         "plusieurs stents ou stent(s) de grande longueur ou posé(s) sur une bifurcation, "
         "patients tri-tronculaires non complètement revascularisés, récidive sous traitement, "
         "diabète, fraction d'éjection basse."),
        ("Discussion pluridisciplinaire", "Obligatoire pour guider la prise en charge : "
         "cardiologue, spécialiste de l'hémostase, chirurgien/médecin réalisant l'acte invasif, "
         "et anesthésiste-réanimateur. Le risque hémorragique (chirurgie sous AAP) et le risque "
         "thrombotique (arrêt d'AAP) doivent être discutés collégialement pour décider de la "
         "prise en charge périopératoire, voire d'un report ou d'une annulation du geste. Un "
         "relevé de conclusions doit être rédigé, disponible dans le dossier, et le patient "
         "informé."),
        ("EC pharmacoactive, bithérapie non interruptible", "Si l'intervention doit survenir "
         "pendant une période où la bithérapie ne peut pas être arrêtée totalement (risque "
         "thrombotique élevé) : poursuite de l'aspirine hautement souhaitable, fenêtre courte "
         "de 5 jours d'arrêt du clopidogrel envisageable (voir Tableau 1) — <i>proposition ne "
         "reposant sur aucune étude prospective, mais sur un compromis entre la durée de vie des "
         "plaquettes (10 jours), le risque hémorragique de la poursuite et le risque "
         "thrombotique de l'interruption.</i> Reprise postopératoire la plus précoce possible ; "
         "dose de charge de clopidogrel ≥ 300 mg évoquée par certains experts."),
        ("EC pharmacoactive, quel que soit le délai", "Il est préférable d'opérer sous aspirine "
         "(voir Tableau 1). Prudence et discussion collégiale particulièrement recommandées si "
         "l'hémostase chirurgicale est difficile (grands décollements, aorte, prostate, "
         "neurochirurgie, ORL, segment postérieur de l'œil). Hors chirurgie cardiaque, aucune "
         "donnée de la littérature sur le risque hémorragique périopératoire sous clopidogrel ; "
         "les données sous ticlopidine (risque hémorragique équivalent) sont très peu "
         "nombreuses, même si un accroissement du risque hémorragique par rapport à l'aspirine "
         "a été rapporté. <b>EC nue au-delà de la 6<sup>e</sup> semaine :</b> aucune "
         "recommandation forte ne pourra être formulée avant les résultats de l'étude "
         "STRATAGEM (qui peut inclure les patients porteurs d'EC nues au-delà du 30<sup>e</sup> "
         "jour)."),
        ("Si aucun AAP ne peut être maintenu", "Risque hémorragique de la chirurgie considéré "
         "comme majeur ou impossibilité de surseoir à l'intervention : l'arrêt complet du "
         "traitement (bithérapie) doit être discuté au cas par cas (risque thrombotique "
         "redoutable). Pas d'argument en faveur d'une substitution par AINS (flurbiprofène "
         "50 mg × 2, arrêt 24h avant) ou par HBPM à dose anticoagulante (85-100 UI Axa/kg/12h "
         "SC, non préventive) — substitution exposant elle-même à un risque hémorragique "
         "périopératoire non négligeable."),
        ("Registre & carte de liaison", "Mise en place proposée d'un registre des événements "
         "périopératoires chez les patients porteurs de stent (services d'anesthésie/cardiologie "
         "volontaires, cadre EPP, sous l'égide du Cfar). Diffusion d'une carte de liaison pour "
         "les patients sous AAP oraux au long cours (motif, type/nombre d'AAP, durée, "
         "coordonnées du médecin à contacter en cas d'interruption envisagée)."),
    ]))
    return story


def _section_tableau_sources():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("Tableau 1 — Matrice de décision périopératoire", color=TEAL_DARK))
    story.append(Spacer(1, 2 * mm))
    story.append(P(
        "<b>Endoprothèse coronaire (EC) pharmacoactive.</b> Risque de thrombose du stent : "
        "<i>à évaluer avec le cardiologue.</i> Risque hémorragique de l'intervention : "
        "<i>à évaluer avec le responsable du geste invasif ou le chirurgien.</i>", S_NOTE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(KeepTogether([risk_matrix_table(), Spacer(1, 1.5 * mm),
        P("Risque hémorragique — Majeur : intervention ne pouvant être réalisée sous AAP. "
          "Modéré : intervention réalisable sous aspirine seule. Mineur : intervention "
          "réalisable sous aspirine et clopidogrel.", S_NOTE),
        P("Risque de thrombose d'EC pharmacoactive — Majeur : mise en place depuis moins de 6 "
          "mois à 1 an, ou patient nécessitant un traitement par aspirine-clopidogrel, ou "
          "patient avec facteur de risque. Modéré : mise en place depuis plus de 6 mois à 1 an.",
          S_NOTE),
    ]))
    story.append(Spacer(1, 1.5 * mm))
    story.append(info_panel(P(
        "Dans tous les cas, l'intervention doit être reportée au-delà de six semaines d'un "
        "syndrome coronaire aigu dans la mesure du possible.", S_BODY_SM), bg=GREY_LIGHT, border=GREY))
    story.append(Spacer(1, 4 * mm))

    story.append(section_bar("Sources et traçabilité", color=GREY))
    story.append(Spacer(1, 2 * mm))
    story.append(P(
        "<b>Document source :</b> « Gestion du traitement antiplaquettaire oral chez les "
        "patients porteurs d'endoprothèses coronaires » (Information professionnelle). "
        "P. Albaladejo, E. Marret, V. Piriou, C.-M. Samama, et le groupe de travail (Didier "
        "Blanchard, Yvonnick Blanloeil, Jean-Philippe Collet, Nicolas Danchin, Christophe "
        "Decoene, Jean-Jacques Domerego, Hélène Eltchaninoff, Ismaël Elalamy, Émile Ferrari, "
        "Gérard Helft, Brigitte Jude, Thomas Lecompte, Jean Mantz, Claude Girard, Jean-Jacques "
        "Lehot, Rémy Nizard, Gabriel Steg, Annick Steib, Claude Tayar). Ann Fr Anesth Reanim "
        "2006;25:796-798.", S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P("<b>Méthodologie :</b> avis d'un groupe d'experts, propositions du 31 mars "
                    "2006, sans système GRADE ni vote/pourcentage d'accord formalisé (voir "
                    "disclosure méthodologique en page 1).", S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P("<b>Couverture :</b> cette fiche reprend l'intégralité des 10 propositions du "
                    "corps du texte (les 2 dernières, registre et carte de liaison, condensées en "
                    "une seule ligne thématique « suivi/traçabilité », sans perte de contenu) et "
                    "le Tableau 1 (matrice de décision), reproduit intégralement à partir du "
                    "rendu visuel de la page source (pas de texte extractible). Comité de "
                    "rédaction, adresses institutionnelles et les 13 "
                    "références bibliographiques ne sont pas retranscrits (sans contenu clinique "
                    "actionnable).", S_SOURCE))
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Avertissement — document de 2006 :</b> ce document est une fiche de synthèse "
        "indépendante, produite pour un usage d'aide-mémoire. Elle reprend l'intégralité des "
        "propositions du texte source, mais ne remplace pas le texte intégral et n'est ni "
        "éditée ni validée par la SFAR. Document ancien et étroit (stents coronaires "
        "uniquement) : pour la gestion périopératoire générale des AAP, se référer aux "
        "propositions GIHP/GFHT/SFAR 2018 (fiches « AAP — procédure programmée » et « AAP — "
        "procédure non programmée / hémorragie ») et, en cas de doute, à un avis spécialisé.",
        S_BODY_SM), bg=GREY_LIGHT, border=GREY))
    return story


SECTIONS = [
    ("Propositions du groupe d'experts", _section_propositions),
    ("Tableau 1 & sources", _section_tableau_sources),
]

def _make_doc(path=None):
    return SimpleDocTemplate(path or OUT, pagesize=A4,
                              leftMargin=MARGIN, rightMargin=MARGIN,
                              topMargin=32 * mm, bottomMargin=16 * mm,
                              title="SFAR 2006 - AAP oral et endoprotheses coronaires",
                              author="Synthèse indépendante (source SFAR)")

def _silent_page(canvas, doc_):
    pass

def _build_upto(section_fns):
    story = []
    for i, fn in enumerate(section_fns):
        if i > 0:
            story.append(Spacer(1, 4 * mm))
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
