# -*- coding: utf-8 -*-
"""
Fiche de synthese - "Delivrance de l'information a la personne sur son etat
de sante" - Recommandation de Bonne Pratique (RBP), HAS, validee par le
College de la HAS en mai 2012. Telechargee depuis sfar.org (texte court).

DISCLOSURE - divergence de date avec l'index bibliotheque : build/
library_final.json indexe ce document sous l'annee "2010", mais le
document source lui-meme (page de garde, section methode, et chaque page
de pied) affiche explicitement "Mai 2012" comme date de validation par le
College de la HAS. Le "2010" pourrait correspondre a la date du guide
methodologique HAS generique cite en reference ("Elaboration de
recommandations de bonne pratique... Decembre 2010"), pas a la date de ce
document specifique. Disclosed, non resolu arbitrairement en faveur de
l'un ou l'autre - la date effectivement imprimee sur le document (mai
2012) est utilisee dans le corps de la fiche et son DOC_META, avec cette
divergence disclosed ici.

DISCLOSURE - lien source casse dans l'index bibliotheque : le
`direct_pdf_url` de library_final.json contient une coquille
("l-information" avec un tiret) qui ne correspond a aucun fichier reel
(404 - sert une page HTML, pas un PDF) ; l'URL correcte, trouvee en
grattant la page href elle-meme, est
".../2a_HAS_texte-court_Delivrance-de-linformation-a-la-personne-sur-son-etat-de-sante.pdf"
(sans le tiret apres "de-l"). Le fichier `sources/delivrance_information_2012.txt`
de ce depot a ete extrait depuis cette URL corrigee.

CONTEXTE : ce texte actualise (et remplace) « Information des patients -
Recommandations destinees aux medecins » (ANAES, mars 2000) - ce document
de 2000 est lui-meme un lien mort sur sfar.org (verifie, 404) et n'est pas
dans le backlog de ce corpus ; aucun risque de collision de contenu avec
un autre document deja construit.

METHODOLOGIE - PARTICULARITE DISCLOSED : la grille de cotation HAS
classique A/B/C/AE est definie dans le preambule methodologique du
document (page 2), MAIS AUCUNE citation de grade individuelle n'apparait
nulle part dans le corps du texte (verifie par grep exhaustif : zero match
pour "(A)", "(B)", "(C)", "(AE)" sur l'integralite du texte extrait). Le
document lui-meme l'explique explicitement (page 5) : "Les donnees de la
litterature identifiee dans le cadre de ce travail (absence d'etude ou
insuffisance des niveaux de preuve scientifique des etudes) n'ont pas
permis d'etablir de grade pour les recommandations. En consequence,
TOUTES les recommandations reposent sur un accord entre experts du groupe
de travail, apres consultation du groupe de lecture." Chip local "AE"
(deja partage dans ce corpus, GREY/WHITE) applique donc UNIFORMEMENT a
chaque ligne - jamais invente au niveau individuel, explicitement
enonce comme s'appliquant a l'ensemble par la source elle-meme (meme
pattern que fiche_bris_dentaires.py/fiche_organisation_usc_2018.py pour
un chip uniforme different).

PERIMETRE : couverture integrale des 4 sections de recommandations (1.
Contenu et qualites de l'information ; 2. Modalites de la delivrance ; 3.
Information du mineur/majeur protege/majeur inapte a recevoir
l'information ; 4. Evaluation de l'information donnee). Le Preambule
(champ d'application, exclusions explicites du perimetre - risques
inconnus au moment de l'acte, information sur un dommage lie aux soins,
pratiques de bioethique, information en fin de vie) est retranscrit en
encadre de perimetre. L'Annexe 1 (liste reglementaire des professions de
sante, purement definitionnelle) et la section "Participants" ne sont pas
retranscrites - non actionnables au chevet. Citations d'articles de loi
(Code de la sante publique, Code civil) condensees a la reference legale
minimale necessaire, sans reproduire les articles in extenso (regle 7).

DECOMPTE : 28 recommandations/reperes pratiques (tous AE), verifies par
relecture complete du corps du texte (sections 1 a 4), repartis ainsi :
section 1 (6), section 2 (11), section 3 (8), section 4 (3).
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from style import *
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.units import mm

OUT = "/home/user/rfe-sfar-website/output/Fiche_HAS_Delivrance_Information_2012.pdf"

SOURCE_TXT = ("Source : HAS, « Délivrance de l'information à la personne sur son état de "
              "santé », Recommandation de Bonne Pratique, validée par le Collège de la HAS "
              "en mai 2012. Fiche de synthèse non officielle : se référer au texte intégral.")

def P(txt, style=S_CELL):
    return Paragraph(txt, style)

def chip(label, **kw):
    return grade_chip(label, **kw)

CW_FULL = PAGE_W - 2 * MARGIN

def reco_table(rows, col_widths):
    """rows: (ref, text, grade_label)."""
    data = [[P("Thème", S_HEAD_W), P("Recommandation", S_HEAD_W), P("Grade", S_HEAD_W_C)]]
    for ref, txt, grade in rows:
        data.append([P(ref, S_CELL_B), P(txt, S_CELL), chip(grade, width=15 * mm)])
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

RCW = [30 * mm, CW_FULL - 30 * mm - 15 * mm, 15 * mm]

def legend_flowable():
    chip_w = 20 * mm
    content_w = CW_FULL
    row = Table([[chip("AE", width=chip_w - 2 * mm),
                  P("Convention de ce document : la grille HAS A/B/C/AE est définie en "
                    "préambule, mais aucune citation individuelle n'apparaît dans le texte — "
                    "la source énonce explicitement que « toutes les recommandations reposent "
                    "sur un accord entre experts » (absence de données permettant un grade). "
                    "Chip <b>AE</b> (accord d'experts) appliqué uniformément.", S_BADGE_HEAD)]],
                colWidths=[chip_w, content_w - chip_w])
    row.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                              ("LEFTPADDING", (0, 0), (-1, -1), 1),
                              ("RIGHTPADDING", (0, 0), (-1, -1), 1),
                              ("TOPPADDING", (0, 0), (-1, -1), 0),
                              ("BOTTOMPADDING", (0, 0), (-1, -1), 0)]))
    return row

TOTAL_PAGES = {"n": 4}

def on_page(canvas, doc, page_title):
    header_band(canvas, doc, "HAS — RBP, MAI 2012",
                "Délivrance de l'information à la personne sur son état de santé",
                page_title, icon_fn=lambda c, x, y: icon_shield(c, x, y, 13 * mm), color=TEAL_DARK)
    footer_band(canvas, doc, SOURCE_TXT, f"Page {doc.page} / {TOTAL_PAGES['n']}")

# ---------------------------------------------------------------------------
def _section_intro_contenu():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Périmètre :</b> ces recommandations actualisent et remplacent « Information des "
        "patients — Recommandations destinées aux médecins » (ANAES, mars 2000). Elles "
        "N'ABORDENT PAS : l'information sur des risques inconnus au moment de l'acte et "
        "révélés ultérieurement par la science ; l'information sur les circonstances et "
        "causes d'un dommage lié aux soins ; les pratiques de bioéthique ; l'information en "
        "fin de vie (régie par la loi du 22 avril 2005). Elles concernent l'ensemble des "
        "professionnels de santé (pas seulement les médecins).", S_BODY),
        bg=AMBER_LIGHT, border=AMBER))
    story.append(Spacer(1, 2.5 * mm))
    story.append(legend_flowable())
    story.append(Spacer(1, 3 * mm))
    story.append(KeepTogether([
        section_bar("1. Le contenu et les qualités de l'information"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("Contenu", "L'information porte sur l'état de santé, les investigations/traitements/"
         "actions de prévention envisagés, pour permettre à la personne de décider en "
         "connaissance de cause ; le professionnel décrit le suivi proposé et répond aux "
         "questions.", "AE"),
        ("Contenu", "Elle porte sur : l'état de santé et son évolution habituelle (avec et "
         "sans traitement, qualité de vie) ; la description et le déroulement des actes "
         "envisagés et l'existence d'alternatives ; leurs objectifs, bénéfices, "
         "inconvénients, complications et risques fréquents ou graves prévisibles ; les "
         "précautions recommandées ; les modalités de suivi.", "AE"),
        ("Contenu", "Présenter les différents choix possibles pour permettre à la personne de "
         "se représenter les enjeux de sa décision, quelle qu'elle soit (accord ou refus).", "AE"),
        ("Qualités", "L'information est synthétique, hiérarchisée, compréhensible et "
         "personnalisée ; elle présente les alternatives, puis les bénéfices attendus, puis "
         "les inconvénients et risques éventuels.", "AE"),
        ("Qualités", "Elle porte sur les risques fréquents et, pour les risques normalement "
         "prévisibles, sur les risques graves (pronostic vital ou fonctionnel), ainsi que sur "
         "les risques spécifiques à la personne et les précautions particulières associées.", "AE"),
        ("Qualités", "Le professionnel s'assure de la compréhension (ex. faire reformuler), "
         "indique la proposition qu'il préfère en expliquant ses raisons, et propose un "
         "second avis si nécessaire.", "AE"),
    ], RCW))
    return story

# ---------------------------------------------------------------------------
def _section_modalites():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("2. Les modalités de la délivrance de l'information"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("Entretien individuel", "La délivrance se fait toujours dans le cadre d'un entretien "
         "individuel, avec tact et disponibilité ; elle peut être progressive, réitérée et "
         "actualisée si nécessaire.", "AE"),
        ("Entretien individuel", "La volonté d'une personne de ne pas être informée est "
         "respectée, sauf lorsque des tiers sont exposés à un risque de transmission.", "AE"),
        ("Avec accompagnant", "S'assurer du souhait de présence de l'accompagnant et proposer "
         "qu'une partie de l'entretien se fasse en tête-à-tête, sauf opposition de la "
         "personne.", "AE"),
        ("Avec accompagnant", "Recourir à un interprète pour une personne étrangère, ou à un "
         "assistant de communication en cas de handicap sensoriel ou moteur, est recommandé.", "AE"),
        ("Personne de confiance", "Si désignée et si le patient a choisi de s'en faire "
         "assister, l'entretien a lieu en sa présence, avec un temps en tête-à-tête proposé.", "AE"),
        ("Documents écrits", "L'information orale est primordiale ; des documents écrits "
         "peuvent la compléter (jamais à faire signer par la personne).", "AE"),
        ("Documents écrits", "Les documents sont hiérarchisés, fondés sur des données "
         "validées, présentent les bénéfices avant les inconvénients/risques, précisent les "
         "risques fréquents et graves, les moyens de faire face aux complications et les "
         "signes d'alerte ; ils sont synthétiques, clairs et courts.", "AE"),
        ("Documents écrits", "Il est souhaitable de disposer de documents en langues "
         "étrangères et de supports adaptés (malvoyance, troubles du développement…).", "AE"),
        ("Plusieurs professionnels", "Chaque professionnel informe sur son domaine de "
         "compétence sans présumer que l'information a été donnée par un autre, mais s'enquiert "
         "de ce qui a déjà été délivré ; un référent unique remet une synthèse aux différentes "
         "étapes du soin.", "AE"),
        ("Traçabilité", "Le dossier mentionne les informations majeures délivrées, par qui, à "
         "quelle date, et les difficultés éventuellement rencontrées.", "AE"),
        ("Traçabilité", "Ces mentions suffisent comme moyen de preuve en cas de litige — il "
         "n'y a pas lieu de demander à la personne une confirmation signée.", "AE"),
    ], RCW))
    return story

# ---------------------------------------------------------------------------
def _section_mineur_majeur():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("3. Information du mineur, du majeur protégé ou inapte"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("Mineur", "Le droit à l'information est exercé par les titulaires de l'autorité "
         "parentale, mais le mineur reçoit lui-même une information adaptée à son degré de "
         "maturité pour l'associer à la décision (le dossier trace les deux informations).", "AE"),
        ("Mineur", "Si les deux titulaires sont présents : informer les deux ainsi que le "
         "mineur ; un temps d'entretien singulier avec le mineur peut être proposé selon "
         "son âge.", "AE"),
        ("Mineur", "Si un seul titulaire est présent : l'informer et lui exposer la nécessité "
         "d'informer l'autre titulaire (en particulier si les parents sont séparés) ; un "
         "entretien avec les deux parents peut être proposé si le pronostic est grave.", "AE"),
        ("Mineur", "Si l'accompagnant n'est pas titulaire de l'autorité parentale : lui "
         "délivrer une information strictement utile et nécessaire, à compléter avec le(s) "
         "titulaire(s).", "AE"),
        ("Mineur", "Mineur non accompagné : l'informer si sa maturité et la situation clinique "
         "le permettent, en indiquant si besoin la nécessité de réitérer l'information en "
         "présence du/des titulaire(s).", "AE"),
        ("Mineur", "Mineur s'opposant à l'information des titulaires pour garder le secret : le "
         "médecin (seul, et non tout professionnel de santé) peut mettre en œuvre le "
         "traitement nécessaire à la sauvegarde de sa santé sans autorisation parentale, à "
         "condition que le mineur se fasse accompagner d'un majeur de son choix.", "AE"),
        ("Majeur protégé", "Le majeur protégé reçoit lui-même l'information, adaptée à ses "
         "facultés de compréhension (principe d'autonomie, loi du 5 mars 2007) ; le juge des "
         "tutelles peut prévoir que le tuteur la reçoive en sa présence, ou seul si le majeur "
         "n'est pas en état de la recevoir.", "AE"),
        ("Majeur inapte", "Information adaptée aux facultés de compréhension ; consulter la "
         "personne de confiance si désignée alors que la personne avait encore ses facultés, "
         "ou à défaut les proches présents — en traçant dans le dossier le motif et le "
         "contenu de l'information donnée.", "AE"),
    ], RCW))
    return story

# ---------------------------------------------------------------------------
def _section_evaluation_sources():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("4. Évaluation de l'information donnée"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(reco_table([
        ("Satisfaction", "La satisfaction des personnes à l'égard de l'information orale et "
         "écrite fait l'objet d'une évaluation rétrospective par les établissements de "
         "santé (ex. commissions des relations avec les usagers).", "AE"),
        ("Pratiques", "Une évaluation régulière des pratiques d'information devrait s'appuyer "
         "sur des enquêtes auprès des personnes et sur l'analyse rétrospective des dossiers "
         "médicaux.", "AE"),
        ("Documents écrits", "L'évaluation des documents vérifie la méthode d'élaboration et le "
         "contenu scientifique, l'identité des auteurs et la date d'établissement, et "
         "l'absence de toute signature demandée à la personne (contrôlé en visite de "
         "certification HAS).", "AE"),
    ], RCW))
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("Sources et avertissement", color=GREY))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>Document source :</b> Haute Autorité de Santé (HAS), « Délivrance de "
        "l'information à la personne sur son état de santé », Recommandation de Bonne "
        "Pratique, validée par le Collège de la HAS en mai 2012.", S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>URL source :</b> https://sfar.org/delivrance-de-linformation-a-la-personne-sur-"
        "son-etat-de-sante/", S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>Couverture :</b> intégralité des 4 sections de recommandations (28 items, tous "
        "AE — grille A/B/C/AE définie en préambule mais jamais citée individuellement, la "
        "source énonçant explicitement que toutes les recommandations reposent sur un "
        "accord d'experts). Annexe 1 (liste réglementaire des professions de santé) et la "
        "section Participants non reproduites — non actionnables au chevet. Divergence de "
        "date disclosed en tête de script (index bibliothèque : 2010 ; document : mai 2012) "
        "et lien source corrigé (coquille dans l'URL de l'index). Argumentaire scientifique "
        "détaillé (document source complet) non reproduit.", S_SOURCE))
    story.append(Spacer(1, 2 * mm))
    story.append(info_panel(P(
        "<b>Avertissement :</b> cette fiche est une synthèse indépendante, produite pour un "
        "usage d'aide-mémoire en anesthésie-réanimation. Elle ne remplace pas le texte "
        "intégral ni un conseil juridique. Cette fiche n'est ni éditée ni validée par la HAS.",
        S_BODY_SM), bg=GREY_LIGHT, border=GREY))
    return story

# ---------------------------------------------------------------------------
def _section_mineur_majeur_evaluation_sources():
    story = _section_mineur_majeur()
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_evaluation_sources())
    return story

SECTIONS = [
    ("Le contenu et les qualités de l'information", _section_intro_contenu),
    ("Les modalités de la délivrance de l'information", _section_modalites),
    ("Information du mineur/majeur protégé, évaluation & sources", _section_mineur_majeur_evaluation_sources),
]

def _make_doc(path=None):
    return SimpleDocTemplate(path or OUT, pagesize=A4,
                              leftMargin=MARGIN, rightMargin=MARGIN,
                              topMargin=32 * mm, bottomMargin=16 * mm,
                              title="Fiche HAS 2012 - Delivrance de l'information au patient",
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
