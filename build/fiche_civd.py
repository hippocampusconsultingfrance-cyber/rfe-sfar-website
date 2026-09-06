# -*- coding: utf-8 -*-
"""
Fiche de synthese - XXIIe Conference de Consensus SRLF (avec la SFAR, la SFH-GEHT et le
GFRUP) "Coagulations Intra-Vasculaires Disseminees (CIVD) en reanimation - Definition,
classification et traitement" (a l'exclusion des cancers et des hemopathies malignes),
Faculte de Medecine de Lille, jeudi 10 octobre 2002. President du jury : P.E. Bollaert
(Nancy). Source : sources/civd.pdf (6 pages, texte "Resume" de la conference), extrait en
texte integral dans sources/civd.txt. Pas de tampon d'obsolescence sur la page 1 (verifiee
visuellement a 150dpi) - document non marque "abroge" dans build/library_final.json.

CHAMP : defini explicitement des la page de titre - "a l'exclusion des cancers et des
hemopathies malignes" - disclosed tel quel dans le panneau d'introduction (jamais omis
silencieusement).

METHODOLOGIE - PAS de systeme GRADE 1+/1-/2+/2-/AE. Page 6 (jury) imprime EXPLICITEMENT
un systeme a DEUX AXES INDEPENDANTS, chacun optionnel et attache individuellement a
chaque enonce du corps du texte (verifie par grep exhaustif du texte extrait, motif
"([abcd](, [123])?)") :
  - Niveau de preuve de la reference (lettre a/b/c/d) : a = etudes prospectives
    controlees et randomisees ; b = etudes non randomisees, comparaisons simultanees ou
    historiques de cohortes ; c = mises au point, revues generales, editoriaux et etudes
    substantielles de cas en serie, publiees et revisees par des experts exterieurs ;
    d = publications d'opinion (monographies, publications d'organisations officielles)
    sans comite de lecture ni revision externe.
  - Niveau de la recommandation (chiffre 1/2/3), IMPRIME UNIQUEMENT quand le jury l'a
    juge applicable : 1 = preuves scientifiques indiscutables ; 2 = preuves scientifiques
    + soutien consensuel des experts ; 3 = pas de preuves adequates mais soutenu par les
    donnees disponibles et l'opinion des experts.
22 enonces cotes au total dans le corps du texte (grep exhaustif, verifie) : 1x(a), 1x(b),
7x(c) seul, 4x(c,2), 4x(c,3), 5x(d) = 22. La plupart des enonces ne portent QUE la lettre
de preuve, sans chiffre de recommandation associe (le jury ne l'a pas juge necessaire /
possible pour ces enonces) - jamais invente ici : colonne "Niveau reco" affichee "-" pour
ces lignes plutot qu'une cotation inventee. Extension LOCALE, non invasive, de
GRADE_COLORS (meme precedent que fiche_glycemie.py/fiche_aap_programmee.py) pour les
lettres a/b/c/d et les chiffres 1/2/3 - aucune collision avec les cles existantes
("1+","1-","2+","2-","AE","?").

FIGURE (page 5 source, "Strategie devant un syndrome d'activation systemique de la
coagulation") : pure organigramme graphique (boites + fleches), texte extractible mais
ORDRE SCRAMBLE par l'extraction PyMuPDF - reconstruite ici a partir d'un rendu visuel de
la page a 200dpi (build/civd_p5.png), jamais depuis le seul ordre du texte extrait. Arbre
verifie visuellement : SASC -> criteres D-dimeres/plaquettes/TP/fibrinogene = CIVD
BIOLOGIQUE -> CIVD clinique -> CIVD compliquee -> se divise en deux branches paralleles
("Syndrome hemorragique, acte invasif" avec sous-embranchement NON/OUI ; "Syndrome
thrombotique" qui rejoint directement l'encadre "Aucun traitement specifique de la CIVD")
- PAS de connexion entre la branche thrombotique et la sous-decision NON/OUI (verifie sur
le rendu : une seule fleche part de "Syndrome thrombotique", vers l'encadre "Aucun
traitement specifique"). Bandeau lateral "Optimisation du traitement etiologique et
symptomatique" transcrit comme note transverse plutot que graphiquement (s'applique a
l'ensemble de l'arbre).

TABLEAU (page 3, criteres de consommation majeurs/mineurs) : reproduit integralement en
tableau structure (Parametre / Majeur / Mineur), y compris le "-" imprime pour le
fibrinogene en colonne Majeur (aucun seuil majeur defini pour ce parametre - transcrit
verbatim, pas invente).

DOCUMENT DE 2002 - AVERTISSEMENT DE PEREMPTION EXPLICITE (disclosure, pratique deja
etablie sur ce corpus pour les documents anciens, cf. fiche_glycemie.py 2009) : la prise
en charge therapeutique specifique de la CIVD a evolue depuis 2002. En particulier, le
"recombinant active de la PC (drotrecogine alpha, Xigris)" evoque page 4 (sans recul a
l'epoque) a ete RETIRE DU MARCHE MONDIAL en 2011 (etude PROWESS-SHOCK) ; les
recommandations de prise en charge du sepsis et de ses coagulopathies ont egalement
evolue depuis (Surviving Sepsis Campaign). Disclose explicitement dans le panneau
d'avertissement final plutot que silencieusement omis ou corrige.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from style import *
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.units import mm

# Local, non-invasive extension of the shared GRADE_COLORS dict (no collision with
# existing keys "1+","1-","2+","2-","AE","?" - same precedent as fiche_glycemie.py).
GRADE_COLORS["a"] = (GREEN, WHITE)
GRADE_COLORS["b"] = (TEAL, WHITE)
GRADE_COLORS["c"] = (AMBER, WHITE)
GRADE_COLORS["d"] = (GREY, WHITE)
GRADE_COLORS["1"] = (GREEN, WHITE)
GRADE_COLORS["2"] = (TEAL, WHITE)
GRADE_COLORS["3"] = (AMBER, WHITE)

OUT = "/home/user/rfe-sfar-website/output/Fiche_SRLF_SFAR_CIVD_2002.pdf"

SOURCE_TXT = ("Source : XXIIe Conférence de Consensus SRLF, avec la participation de la SFAR, de la "
              "Société Française d'Hématologie (Groupe d'Étude sur l'Hémostase et la Thrombose) et du "
              "Groupe Francophone de Réanimation et Urgences Pédiatriques — « Coagulations Intra-"
              "Vasculaires Disséminées (CIVD) en réanimation : définition, classification et traitement "
              "(à l'exclusion des cancers et des hémopathies malignes) », Faculté de Médecine de Lille, "
              "10 octobre 2002. Président du jury : P.E. Bollaert. Fiche de synthèse non officielle : se "
              "référer au texte intégral.")

def P(txt, style=S_CELL):
    return Paragraph(txt, style)

def chip(label, **kw):
    return grade_chip(label, **kw)

def reco_table(rows, col_widths):
    """rows: (theme, text, preuve_label, force_label_or_None) — ce document n'a pas de
    numerotation R1/R2 (enonces en prose continue), d'ou une colonne Theme comme dans
    theme_table() de fiche_aap_programmee.py ; DEUX colonnes de chip (Preuve a/b/c/d,
    Force 1/2/3) car les deux axes sont independants et pas toujours tous deux imprimes
    (meme principe a deux axes que fiche_glycemie.py, colonnes NGP/Accord)."""
    data = [[P("Thème", S_HEAD_W), P("Énoncé", S_HEAD_W), P("Preuve", S_HEAD_W_C), P("Force", S_HEAD_W_C)]]
    for theme, txt, preuve, force in rows:
        force_cell = chip(force) if force else P("—", S_CELL_C)
        data.append([P(theme, S_CELL_B), P(txt, S_CELL), chip(preuve), force_cell])
    t = Table(data, colWidths=col_widths, repeatRows=1)
    style_cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), NAVY), ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTNAME", (0, 0), (-1, 0), FONT_BOLD), ("FONTSIZE", (0, 0), (-1, 0), 8),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("ALIGN", (2, 0), (3, -1), "CENTER"),
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
    data = [[P(h, S_HEAD_W_C) for h in header]]
    for r in rows:
        data.append([P(c, S_CELL_C) for c in r])
    t = Table(data, colWidths=col_widths, repeatRows=1)
    st = [
        ("BACKGROUND",(0,0),(-1,0), TEAL_DARK), ("TEXTCOLOR",(0,0),(-1,0), WHITE),
        ("FONTNAME",(0,0),(-1,0), FONT_BOLD), ("FONTSIZE",(0,0),(-1,0), 8),
        ("GRID",(0,0),(-1,-1),0.5,GREY_LIGHT), ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
        ("TOPPADDING",(0,0),(-1,-1),3.2), ("BOTTOMPADDING",(0,0),(-1,-1),3.2),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            st.append(("BACKGROUND",(0,i),(-1,i), BG_PANEL))
    t.setStyle(TableStyle(st))
    return t

def legend_flowable():
    chip_w = 14*mm
    content_w = PAGE_W - 2*MARGIN
    text_w = (content_w - 2*chip_w) / 2.0
    row = Table([[
        chip("a-d", width=chip_w-2*mm),
        P("<b>Preuve</b> — niveau de preuve de la référence : a (essais randomisés) &gt; "
          "b (études non randomisées) &gt; c (mises au point, revues, séries de cas) &gt; "
          "d (opinions, publications non revues par des pairs).", S_BADGE_HEAD),
        chip("1-3", width=chip_w-2*mm),
        P("<b>Force</b> — niveau de la recommandation, imprimé seulement quand le jury l'a "
          "jugé possible : 1 (preuves indiscutables) &gt; 2 (preuves + consensus d'experts) "
          "&gt; 3 (pas de preuves adéquates, opinion d'experts). « — » = non coté par le jury.",
          S_BADGE_HEAD),
    ]], colWidths=[chip_w, text_w, chip_w, text_w])
    row.setStyle(TableStyle([("VALIGN",(0,0),(-1,-1),"MIDDLE"), ("LEFTPADDING",(0,0),(-1,-1),2),
                              ("RIGHTPADDING",(0,0),(-1,-1),3)]))
    return row

def algo_table():
    """Organigramme (page 5 source, "Stratégie devant un SASC") — reconstruit à partir du
    rendu visuel (build/civd_p5.png), pas du seul ordre du texte extrait (scramblé par
    PyMuPDF sur ce document). Colonnes finales : NON / OUI (sous-décision de la branche
    "syndrome hémorragique, acte invasif") / Syndrome thrombotique (branche parallèle,
    sans lien avec NON/OUI)."""
    cw = PAGE_W - 2*MARGIN
    c0 = c1 = cw / 3.0
    S_A = pstyle("civd_a", fontSize=7.8, leading=9.8, textColor=INK, alignment=TA_CENTER)
    S_A_B = pstyle("civd_a_b", fontSize=8.4, leading=10.2, textColor=WHITE, fontName=FONT_BOLD, alignment=TA_CENTER)
    S_A_HEAD = pstyle("civd_a_head", fontSize=7.6, leading=9.4, textColor=INK, fontName=FONT_BOLD, alignment=TA_CENTER)

    def ac(txt, style=S_A):
        return Paragraph(txt, style)

    data = [
        [ac("SYNDROME D'ACTIVATION SYSTÉMIQUE DE LA COAGULATION (SASC)", S_A_B), "", ""],
        [ac("D-Dimères &gt; 500 µg/L* — 1 critère majeur (plaquettes &lt; 50 G/L, TP &lt; 50 %) ou 2 "
            "critères mineurs (50 G/L &lt; plaquettes &lt; 100 G/L, 50 % &lt; TP &lt; 65 %, fibrinogène "
            "&lt; 1 g/L). (Critères spécifiques chez le nouveau-né) <b>= CIVD BIOLOGIQUE</b>", S_A), "", ""],
        [ac("↓ CIVD clinique ↓ CIVD compliquée", S_A_HEAD), "", ""],
        [ac("Syndrome hémorragique, acte invasif", S_A_HEAD), "", ac("Syndrome thrombotique", S_A_HEAD)],
        [ac("NON", S_A_HEAD), ac("OUI", S_A_HEAD),
         ac("Aucun traitement spécifique de la CIVD. Héparines, fibrinolytiques, antifibrinolytiques, "
            "AT, PC, PCa non recommandés.", S_A)],
        [ac("Surveillance. Répétition du bilan biologique selon étiologie. Pas de traitement "
            "substitutif.", S_A),
         ac("Traitement substitutif : PFC si TP &lt; 35 %, concentrés plaquettaires si plaquettes "
            "&lt; 50 G/L. Surveillance biologique.", S_A), ""],
    ]
    t = Table(data, colWidths=[c0, c1, cw - c0 - c1])
    style_cmds = [
        ("SPAN", (0, 0), (2, 0)), ("SPAN", (0, 1), (2, 1)), ("SPAN", (0, 2), (2, 2)),
        ("SPAN", (0, 3), (1, 3)), ("SPAN", (2, 4), (2, 5)),
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("BACKGROUND", (0, 1), (-1, 1), BG_PANEL),
        ("BACKGROUND", (0, 2), (-1, 2), WHITE),
        ("BACKGROUND", (0, 3), (-1, 3), TEAL_DARK), ("TEXTCOLOR", (0, 3), (-1, 3), WHITE),
        ("BACKGROUND", (0, 4), (1, 4), GREY_LIGHT),
        ("BACKGROUND", (2, 4), (2, 5), AMBER_LIGHT),
        ("BACKGROUND", (0, 5), (1, 5), WHITE),
        ("GRID", (0, 0), (-1, -1), 0.5, GREY_LIGHT),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("TOPPADDING", (0, 0), (-1, -1), 3.4), ("BOTTOMPADDING", (0, 0), (-1, -1), 3.4),
        ("LEFTPADDING", (0, 0), (-1, -1), 4), ("RIGHTPADDING", (0, 0), (-1, -1), 4),
    ]
    t.setStyle(TableStyle(style_cmds))
    return t

TOTAL_PAGES = {"n": 6}

def on_page(canvas, doc, page_title):
    header_band(canvas, doc, "SRLF / SFAR — CONFÉRENCE DE CONSENSUS 2002 — FICHE DE SYNTHÈSE",
                "CIVD en réanimation",
                page_title, icon_fn=lambda c, x, y: icon_drop(c, x, y, 13*mm), color=RED)
    footer_band(canvas, doc, SOURCE_TXT, f"Page {doc.page} / {TOTAL_PAGES['n']}")

# ---------------------------------------------------------------------------
def _section_intro():
    story = []
    story.append(Spacer(1, 3*mm))
    story.append(info_panel(P(
        "<b>Champ :</b> définition, classification et traitement de la <b>coagulation "
        "intravasculaire disséminée (CIVD)</b> en réanimation, <b>à l'exclusion des cancers et "
        "des hémopathies malignes</b> (précision imprimée en couverture de la source, reprise "
        "ici sans l'omettre). XXIIe Conférence de Consensus SRLF, avec la participation de la "
        "SFAR, de la Société Française d'Hématologie (Groupe d'Étude sur l'Hémostase et la "
        "Thrombose — GEHT) et du Groupe Francophone de Réanimation et Urgences Pédiatriques "
        "(GFRUP), Faculté de Médecine de Lille, 10 octobre 2002.<br/><br/>"
        "<b>Méthodologie — distincte de GRADE :</b> chaque énoncé du corps du texte peut porter "
        "jusqu'à deux cotations indépendantes, imprimées entre parenthèses : une lettre de "
        "<b>niveau de preuve</b> (a/b/c/d, type d'étude sous-jacente) et, quand le jury l'a jugé "
        "possible, un chiffre de <b>niveau de recommandation</b> (1/2/3). La plupart des énoncés "
        "de ce document ne portent que la lettre de preuve, sans chiffre associé — jamais "
        "inventé ici : la colonne « Force » affiche « — » dans ce cas plutôt qu'une cotation "
        "fabriquée. Voir légende ci-dessous.",
        S_BODY), bg=BG_PANEL, border=TEAL))
    story.append(Spacer(1, 3*mm))
    story.append(section_bar("Légende (convention de ce document)"))
    story.append(Spacer(1, 2*mm))
    story.append(legend_flowable())
    return story

def _section_q1():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Question 1 — Définition et classification"))
    story.append(Spacer(1, 2*mm))
    story.append(P(
        "La CIVD est un <b>syndrome acquis</b> secondaire à une activation systémique et "
        "excessive de la coagulation, rencontré dans de nombreuses situations cliniques en "
        "réanimation. Elle se définit par l'association d'anomalies biologiques — avec ou sans "
        "signes cliniques — témoins de la formation exagérée de thrombine et de fibrine, et de "
        "la consommation excessive de plaquettes et de facteurs de la coagulation. Elle "
        "s'inscrit dans un processus qui débute par un <b>syndrome d'activation systémique de "
        "la coagulation (SASC)</b>, difficile à mettre en évidence, puis se poursuit par des "
        "troubles biologiques puis cliniques de l'hémostase pouvant engager le pronostic "
        "vital.", S_BODY_SM))
    story.append(Spacer(1, 2*mm))
    story.append(info_panel(P(
        "<b>Terminologie abandonnée</b> par le jury (par souci de clarification) : « CIVD "
        "compensée/décompensée », « latente/patente », « subclinique/symptomatique ». "
        "<b>Terminologie retenue</b> : CIVD <b>biologique</b> (sans manifestation clinique), "
        "CIVD <b>clinique</b> (manifestations hémorragiques ou ischémiques), CIVD "
        "<b>compliquée</b> (manifestations engageant le pronostic fonctionnel ou vital, ou "
        "association à une ou plusieurs défaillances d'organe).",
        S_BODY_SM), bg=AMBER_LIGHT, border=AMBER))
    story.append(Spacer(1, 2*mm))
    story.append(P("<b>Implications pour la pratique</b> — le jury retient :", S_CELL_B))
    story.append(P(
        "• témoin indirect de la formation excessive de thrombine : l'élévation des "
        "D-dimères ;<br/>"
        "• témoin de la consommation excessive de plaquettes : le purpura, un saignement "
        "diffus et la baisse du nombre de plaquettes ;<br/>"
        "• témoin de la consommation excessive de facteurs de la coagulation : un syndrome "
        "hémorragique, une baisse du taux de prothrombine et de la concentration plasmatique "
        "du fibrinogène.", S_BODY_SM))
    return story

def _section_q2():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(KeepTogether([
        section_bar("Question 2 — Situations cliniques à risque de CIVD"),
        Spacer(1, 2*mm),
        P("<b>a. Mécanismes conduisant à une activation anormale de la coagulation</b> — le "
          "contact entre le facteur tissulaire (FT) et le facteur VII activé (FVIIa) est "
          "l'événement-clé, résultant de trois mécanismes souvent intriqués :", S_BODY_SM),
        Spacer(1, 1.5*mm),
        reco_table([
            ("Mécanisme 1 — induction du FT", "Induction de la synthèse et de l'expression "
             "membranaire du FT par des cellules au contact du sang, en réponse à des stimuli "
             "inflammatoires : le sepsis est la principale cause, mais d'autres situations "
             "peuvent aboutir à une réaction inflammatoire systémique et à une activation de "
             "la coagulation (hypothermie, hyperthermie maligne, choc hémorragique).", "c", None),
            ("Mécanisme 2 — effraction vasculaire", "Contact entre le FT constitutif "
             "extra-vasculaire et le FVIIa lié à une effraction vasculaire : traumatismes "
             "(crâniens en particulier), complications obstétricales (hématome "
             "rétroplacentaire, mort in utero, rétention intra-utérine), brûlures, "
             "pancréatites, complications transfusionnelles, hémolyses.", "c", None),
            ("Mécanisme 3 — cellules anormales", "Contact entre le FT et le FVIIa exprimé à la "
             "surface de cellules anormales : cancers métastasés et hémopathies malignes.", "c", None),
        ], [32*mm, PAGE_W-2*MARGIN-32*mm-24*mm-16*mm, 16*mm, 24*mm]),
    ]))
    story.append(Spacer(1, 2*mm))
    story.append(P(
        "<i>Il existe quelques situations où le mécanisme d'activation est mal élucidé ou "
        "apparaît indépendant du facteur tissulaire (substances « thrombin-like » des venins "
        "de serpents). Chez l'enfant, le purpura fulminans post-infectieux relève d'une "
        "intrication de mécanismes complexes (génétiques et auto-immuns).</i>", S_NOTE))
    story.append(Spacer(1, 2*mm))
    story.append(KeepTogether([
        P("<b>b. Prédisposition génétique</b>", S_CELL_B),
        Spacer(1, 1.5*mm),
        reco_table([
            ("Polymorphismes génétiques", "L'association de polymorphismes génétiques avec la "
             "CIVD reste du domaine de la recherche.", "c", None),
        ], [32*mm, PAGE_W-2*MARGIN-32*mm-24*mm-16*mm, 16*mm, 24*mm]),
        Spacer(1, 1.5*mm),
        P("<i>Le purpura fulminans néonatal est une situation exceptionnelle qui doit faire "
          "évoquer un déficit constitutionnel en protéine C ou S (non coté).</i>", S_NOTE),
    ]))
    return story

def _section_q3():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Question 3 — Diagnostic clinique et biologique"))
    story.append(Spacer(1, 2*mm))
    story.append(P(
        "Par définition, la CIVD comporte des anomalies biologiques non associées (CIVD "
        "biologique) ou associées à des signes cliniques (CIVD clinique) et des complications "
        "(CIVD compliquée).", S_BODY_SM))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("Diagnostic biologique", "Le diagnostic de CIVD biologique est retenu si les "
         "D-dimères sont augmentés et s'il existe un critère majeur ou deux critères mineurs "
         "de consommation (voir tableau ci-dessous). Technique recommandée : test "
         "d'agglutination de particules de latex avec lecture automatisée, seuil 500 µg/L. "
         "L'élévation des D-dimères n'est pas spécifique de CIVD.", "c", "2"),
    ], [32*mm, PAGE_W-2*MARGIN-32*mm-24*mm-16*mm, 16*mm, 24*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(KeepTogether([
        P("<b>Critères de consommation</b>", S_CELL_B),
        Spacer(1, 1.5*mm),
        simple_table(["Paramètre (unité)", "Majeur", "Mineur"], [
            ["Numération plaquettaire (G/L)", "≤ 50", "50 &lt; – ≤ 100"],
            ["Taux de prothrombine (%)", "&lt; 50", "50 ≤ – &lt; 65"],
            ["Concentration en fibrinogène (g/L)", "—", "≤ 1"],
        ], [(PAGE_W-2*MARGIN)*0.46, (PAGE_W-2*MARGIN)*0.27, (PAGE_W-2*MARGIN)*0.27]),
    ]))
    story.append(Spacer(1, 2*mm))
    story.append(P(
        "<b>Diagnostic clinique :</b> retenu en présence de signes hémorragiques ou "
        "thrombotiques, sans caractère spécifique en dehors de deux situations particulières : "
        "le <i>purpura fulminans</i> (manifestations thrombotiques prédominantes) et certaines "
        "CIVD obstétricales (syndrome hémorragique prédominant).<br/><br/>"
        "<b>Diagnostic de CIVD compliquée :</b> manifestations cliniques hémorragiques et "
        "thrombotiques mettant en jeu le pronostic vital ou fonctionnel ; nature et intensité "
        "variables selon l'étiologie et le terrain.", S_BODY_SM))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("Défaillance multiviscérale", "Une association entre syndrome de défaillance "
         "multiviscérale, mortalité et CIVD a été constatée, mais la notion d'imputabilité "
         "directe de la CIVD dans les défaillances d'organe n'est pas démontrée.", "b", None),
    ], [32*mm, PAGE_W-2*MARGIN-32*mm-24*mm-16*mm, 16*mm, 24*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(info_panel(P(
        "<b>Limites du diagnostic :</b> le diagnostic formel de CIVD au cours de "
        "l'insuffisance hépatocellulaire n'est pas possible. Chez le nouveau-né, le taux de "
        "prothrombine n'est pas utilisable et les seuils de numération plaquettaire et de "
        "fibrinogène sont différents (non cotés).",
        S_BODY_SM), bg=GREY_LIGHT, border=GREY))
    return story

def _section_q4():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Question 4 — Moyens thérapeutiques et indications spécifiques"))
    story.append(Spacer(1, 2*mm))
    story.append(P(
        "<b>Le traitement étiologique de la CIVD est fondamental.</b> Les autres moyens "
        "thérapeutiques peuvent être de nature « substitutive » ou « spécifique ».", S_BODY_SM))
    story.append(Spacer(1, 2*mm))
    cw3 = [34*mm, PAGE_W-2*MARGIN-34*mm-24*mm-16*mm, 16*mm, 24*mm]
    story.append(KeepTogether([
        P("<b>Traitements substitutifs</b>", S_CELL_B),
        Spacer(1, 1.5*mm),
        reco_table([
            ("Transfusion plaquettaire", "Indiquée uniquement en cas d'association d'une "
             "thrombopénie &lt; 50 G/L et de facteurs de risque hémorragique (acte invasif, "
             "thrombopathie associée), ou d'hémorragie grave (CIVD compliquée). Choix entre "
             "mélange de concentrés standard et concentré d'aphérèse selon la disponibilité.", "d", None),
            ("Plasma frais congelé (PFC)", "Indiqué (10 à 15 ml/kg) dans les CIVD avec "
             "effondrement des facteurs de coagulation (TP &lt; 35–40 %), associées à une "
             "hémorragie active ou potentielle (acte invasif). Choix entre plasma sécurisé et "
             "plasma viro-atténué (efficacité identique) selon disponibilité et coût.", "d", None),
            ("Fibrinogène", "Aucune indication démontrée à l'utilisation du fibrinogène dans "
             "la CIVD.", "d", None),
            ("Complexe prothrombique (PPSB)", "Potentiellement thrombogène : contre-indiqué au "
             "cours des CIVD.", "d", None),
        ], cw3),
    ]))
    story.append(Spacer(1, 2*mm))
    story.append(KeepTogether([
        P("<b>Traitements spécifiques</b>", S_CELL_B),
        Spacer(1, 1.5*mm),
        P("<i>Les inhibiteurs de la voie du facteur tissulaire n'ont pas été testés dans le "
          "traitement de la CIVD (aucune cotation imprimée par la source pour cet énoncé).</i>",
          S_NOTE),
        Spacer(1, 1.5*mm),
        reco_table([
            ("Concentrés de protéine C", "Administration non validée dans le traitement de la "
             "CIVD.", "c", None),
            ("Protéine C activée recombinante (drotrécogine α)", "Pas d'information sur "
             "l'efficacité dans le traitement de la CIVD.", "d", None),
            ("Antithrombine (AT)", "Améliore la CIVD au cours du sepsis ; la puissance "
             "insuffisante des études ne permet pas de conclure à un effet sur les "
             "défaillances d'organes et la mortalité.", "a", None),
            ("Héparines", "Efficacité non démontrée dans le traitement de la CIVD.", "c", None),
            ("Modulateurs de la fibrinolyse", "Efficacité non démontrée dans le traitement de "
             "la CIVD.", "c", None),
        ], cw3),
    ]))
    return story

def _section_q5():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Question 5 — Stratégie thérapeutique selon la situation clinique"))
    story.append(Spacer(1, 2*mm))
    story.append(P(
        "La stratégie dépend du stade de la CIVD (biologique, clinique, compliquée), de la "
        "prédominance du syndrome hémorragique ou thrombotique, de l'étiologie et de la "
        "nécessité d'un acte invasif. <b>Le traitement optimal de la cause est la condition "
        "<i>sine qua non</i></b> de l'efficacité du traitement de la CIVD, de même que le "
        "traitement symptomatique des défaillances d'organes.", S_BODY_SM))
    story.append(Spacer(1, 2.5*mm))
    story.append(P("<b>Organigramme — stratégie devant un syndrome d'activation systémique de "
                    "la coagulation (SASC)</b>", S_CELL_B))
    story.append(Spacer(1, 1.5*mm))
    story.append(algo_table())
    story.append(Spacer(1, 1.5*mm))
    story.append(P("<i>* Seuil obtenu avec un test d'agglutination au latex avec lecture "
                    "automatisée. Note transverse (bandeau latéral de la source) : "
                    "« optimisation du traitement étiologique et symptomatique » s'applique à "
                    "l'ensemble de la prise en charge, quelle que soit la branche.</i>", S_NOTE))
    story.append(Spacer(1, 3*mm))
    cw3 = [34*mm, PAGE_W-2*MARGIN-34*mm-24*mm-16*mm, 16*mm, 24*mm]
    story.append(reco_table([
        ("CIVD compliquée d'hémorragie grave", "L'objectif thérapeutique est de limiter le "
         "saignement : transfusion de concentrés plaquettaires et de PFC jusqu'à arrêt du "
         "saignement. En cas de procédure invasive, ces produits doivent être transfusés "
         "immédiatement avant sa réalisation.", "c", "2"),
        ("Purpura fulminans / CIVD obstétricale", "La stratégie thérapeutique immédiate repose "
         "sur la symptomatologie clinique.", "c", "3"),
        ("Toute étiologie", "Aucun traitement spécifique de la CIVD n'existe, quelle que soit "
         "l'étiologie : héparines, fibrinolytiques, antifibrinolytiques, AT, PC, PCa ne sont "
         "pas recommandés.", "c", "2"),
    ], cw3))
    story.append(Spacer(1, 2*mm))
    story.append(P("<b>Situations particulières où un traitement est utilisé en pratique "
                    "sans preuve d'efficacité démontrée</b> (non recommandé par le jury) :", S_CELL_B))
    story.append(Spacer(1, 1.5*mm))
    story.append(reco_table([
        ("Hémorragie de la délivrance", "L'utilisation de l'aprotinine est fréquente en cas de "
         "défibrination ; aucune étude n'a démontré son efficacité et son utilisation n'est "
         "pas recommandée.", "c", "3"),
        ("Embolie amniotique", "L'héparinothérapie est habituellement utilisée ; aucune étude "
         "n'a démontré son efficacité et son utilisation n'est pas recommandée.", "c", "3"),
        ("Purpura fulminans post-infectieux", "L'héparinothérapie est souvent utilisée ; "
         "aucune étude n'a démontré son efficacité et son utilisation n'est pas recommandée.", "c", "3"),
    ], cw3))
    return story

def _section_sources():
    story = []
    story.append(Spacer(1, 3*mm))
    story.append(section_bar("Sources, jury & traçabilité", color=GREY))
    story.append(Spacer(1, 2*mm))
    story.append(P(
        "<b>Document source :</b> XXIIe Conférence de Consensus en Réanimation et Médecine "
        "d'Urgence de la Société de Réanimation de Langue Française (SRLF), avec la "
        "participation de la Société Française d'Anesthésie et de Réanimation (SFAR), de la "
        "Société Française d'Hématologie — Groupe d'Étude sur l'Hémostase et la Thrombose "
        "(GEHT) et du Groupe Francophone de Réanimation et Urgences Pédiatriques (GFRUP). "
        "Faculté de Médecine de Lille, jeudi 10 octobre 2002. Président du jury : P.E. "
        "Bollaert (Nancy). Conseillers scientifiques : F. Fourrier (Lille), L. Drouet (Paris).",
        S_SOURCE))
    story.append(Spacer(1, 1.5*mm))
    story.append(P(
        "<b>Jury :</b> D. Annane, H. Aube, J.P. Bedos, T. Boulain, A. Cariou, P. Charbonneau "
        "(secrétaire, commission des référentiels), D. du Cheyron, J.L. Diehl, M. Gaignier, B. "
        "Guidet, B. Guillois, G. Hilbert, O. Jonquet, F. Joye, T. Lecompte, A. Legras, S. "
        "Leteurtre, J. Levraut, P. Lutun, R. Robert, M. Thuong Guyot, B. Vallet (organisateur "
        "local), M. Wolff.", S_SOURCE))
    story.append(Spacer(1, 1.5*mm))
    story.append(P(
        "<b>Méthodologie :</b> pas de système GRADE — chaque énoncé peut porter une lettre de "
        "niveau de preuve (a &gt; b &gt; c &gt; d, selon le type d'étude sous-jacente) et, "
        "quand jugé possible, un chiffre de niveau de recommandation (1 &gt; 2 &gt; 3). 22 "
        "énoncés cotés au total dans le corps du texte : 1×(a), 1×(b), 7×(c) seul, 4×(c, 2), "
        "4×(c, 3), 5×(d) — voir légende page 1.", S_SOURCE))
    story.append(Spacer(1, 1.5*mm))
    story.append(P(
        "<b>Couverture :</b> cette fiche reprend l'intégralité des questions 1 à 5 du texte "
        "« Résumé » de la conférence (définition/classification, situations à risque, "
        "diagnostic, moyens thérapeutiques, stratégie), le tableau des critères de "
        "consommation majeurs/mineurs et l'organigramme de stratégie thérapeutique (page 5), "
        "reconstruit à partir d'un rendu visuel à 200dpi (texte scramblé par l'extraction "
        "automatique sur cette page). Champ de la conférence : <b>hors cancers et "
        "hémopathies malignes</b> (voir intro).", S_SOURCE))
    story.append(Spacer(1, 3*mm))
    story.append(info_panel(P(
        "<b>Avertissement — document de 2002 :</b> ce document est une fiche de synthèse "
        "indépendante, produite pour un usage d'aide-mémoire. Il reprend l'intégralité des "
        "énoncés cotés et de l'organigramme du texte source, mais ne remplace pas le texte "
        "intégral (argumentaire complet, références bibliographiques) et n'est ni édité ni "
        "validé par la SRLF, la SFAR ou les sociétés partenaires. <b>La prise en charge "
        "thérapeutique de la CIVD a évolué depuis 2002</b> : notamment, la protéine C activée "
        "recombinante (drotrécogine α, Xigris®), évoquée en Question 4 sans recul suffisant à "
        "l'époque, a été <b>retirée du marché mondial en 2011</b> (étude PROWESS-SHOCK) ; les "
        "recommandations de prise en charge du sepsis et de ses coagulopathies ont également "
        "évolué depuis (Surviving Sepsis Campaign). En cas de doute, se référer au texte "
        "intégral, aux recommandations ultérieures et/ou à un avis spécialisé.",
        S_BODY_SM), bg=GREY_LIGHT, border=GREY))
    return story

def _section_1():
    return _section_intro()

def _section_2():
    return _section_q1() + [Spacer(1, 3*mm)] + _section_q2()

def _section_3():
    return _section_q3()

def _section_4():
    return _section_q4()

def _section_5():
    return _section_q5()

def _section_6():
    return _section_sources()

# Tried merging sections 1-2, 3-4 and 5-6 into 3 combinator groups (each half-empty page
# individually was <60% full): rebuilt and re-measured the ACTUAL page count via
# _count_pages() rather than assuming — it stayed at 6 pages (merging just redistributed
# the same content across the same number of pages, per-page fullness aside). Reverted to
# the one-section-per-question layout below: same page count, but clearer per-page
# headers/page_titles for the reader (each page names exactly the question it covers).
SECTIONS = [
    ("Introduction, champ & méthodologie", _section_1),
    ("Q1-Q2 — Définition, classification & situations à risque", _section_2),
    ("Q3 — Diagnostic clinique et biologique", _section_3),
    ("Q4 — Moyens thérapeutiques", _section_4),
    ("Q5 — Stratégie thérapeutique & organigramme", _section_5),
    ("Sources, jury & traçabilité", _section_6),
]

def _make_doc(path=None):
    return SimpleDocTemplate(path or OUT, pagesize=A4,
                              leftMargin=MARGIN, rightMargin=MARGIN,
                              topMargin=32*mm, bottomMargin=16*mm,
                              title="Fiche SRLF/SFAR 2002 - CIVD en reanimation",
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
    # Uses fitz (already required for visual QA in this pipeline) rather than pypdf: this
    # environment's pypdf pulls in a broken native `cryptography` binding at import time.
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
