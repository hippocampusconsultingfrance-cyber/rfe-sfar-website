# -*- coding: utf-8 -*-
"""
Fiche de synthese - SFAR, Conference d'experts 2002 (texte court)
"Thrombopenie induite par l'heparine" (TIH) - Comite d'organisation Y. Blanloeil,
en collaboration avec le Groupe d'etude hemostase et thrombose de la SFH, la Societe
francaise de cardiologie et la SRLF. Ann Fr Anesth Reanim 2003;22:150-159.

METHODOLOGIE : conference d'experts SANS systeme de grade formel. La source le dit
explicitement des l'introduction : "le niveau de preuve des etudes est faible [...]
les experts ont donc estime inutile d'assortir chaque proposition d'un grade de
recommandation". Aucun chip GRADE/force n'est donc invente ici : toutes les
propositions sont presentees en tableaux thematiques sans colonne de grade (meme
convention que fiche_aap_endoprotheses_coronaires.py). Le safety-net grep du projet
(grep -n '"[12][+-]/[12][+-]') ne s'applique pas a cette convention - aucun tag
numerique n'existe dans la source, donc pas de risque de fusion de grades differents.

AVERTISSEMENT CLINIQUE IMPORTANT (disclosure ajoutee, absente de la source) : ce
texte date de 2002/2003. Les criteres diagnostiques cliniques et biologiques restent
valides, mais le paysage therapeutique a evolue depuis : la lepirudine (Refludan(R)),
presentee ici comme option de premiere ligne, a ete RETIREE DU MARCHE en Europe en
2012 (arret de commercialisation Bayer) et n'est plus disponible. L'argatroban et le
fondaparinux, cites dans la source comme "non encore disponibles en France" / "non
encore rapportes dans la TIH" en 2002, sont aujourd'hui les alternatives les plus
utilisees en pratique courante. Cette fiche reproduit fidelement le contenu du texte
source (c'est l'objet du projet), mais un encadre d'avertissement dedie signale cette
obsolescence therapeutique des la premiere page et avant le tableau des traitements de
substitution, avec renvoi explicite a un protocole local/national actualise avant toute
prescription. Rien n'est invente ni ajoute au contenu clinique lui-meme : l'avertissement
porte uniquement sur la disponibilite actuelle des molecules, pas sur une reinterpretation
des recommandations.

RELATION AVEC LE DOCUMENT GIHP/GFHT 2019 DEJA PRESENT DANS CE CORPUS (fiche_tih.py,
cle site "tih") : le corpus contient DEJA une fiche batie sur les "Propositions du
GIHP et du GFHT pour le diagnostic et la prise en charge d'une TIH" (2019, 40
propositions, argatroban/bivalirudine/AOD inclus) - c'est le document ACTUEL de
reference sur ce sujet, verifie distinct au niveau de library_final.json (3 entrees
separees : les 2 URLs du document 2019 - deja couvertes par fiche_tih.py - et 1
URL propre a CE document de 2002, jamais couverte avant cette fiche). Les 2 documents
portent sur le meme sujet clinique general (diagnostic/PEC de la TIH) mais ce
document de 2002 est plus ancien et therapeutiquement depasse (voir avertissement
ci-dessus). Il est conserve ici comme document HISTORIQUE distinct plutot que fusionne
- a la difference de fiche_aap_endoprotheses_coronaires.py (2006, egalement historique
et cite en cross-reference vers ses successeurs 2018) - avec : (a) la cle site
"tih_2002" (distincte de "tih") pour eviter toute confusion, (b) un renvoi explicite
vers fiche_tih.py comme reference ACTUELLE des la premiere page de cette fiche, (c) un
badge "Historique" dans DOC_META. Interet documentaire preserve : criteres cliniques/
biologiques de 2002 largement toujours valides (diagnostic, 4T non encore formalise a
l'epoque mais seuils/delais concordants), et protocoles de chirurgie cardiaque CEC
detailles absents sous cette forme narrative du document 2019.

STRUCTURE SOURCE : 12 questions numerotees (Q1 a Q12) + 1 tableau explicite ("Tableau 1
- Principes generaux de prise en charge"). Reprises ici en 9 sections thematiques
(regroupements sans perte de contenu, indiques dans chaque section) :
 1. Contexte, definitions, physiopathologie, methodologie (intro source)
 2. Diagnostic clinique - circonstances evocatrices (Q1)
 3. Diagnostic biologique et demarche pratique (Q2 + Q3)
 4. Diagnostic differentiel, prevention, surveillance (Q4 + Q5 + Q6)
 5. Traitements de substitution - tableau comparatif (Q7)
 6. Contre-indications et Tableau 1 source (Q8 + Tableau 1)
 7. Autres traitements possibles (Q9, hors Tableau 1 deja couvert en 6)
 8. Strategies par contexte clinique - milieu medical et chirurgical non cardiaque
    (Q10 + Q12)
 9. Strategie en chirurgie cardiaque avec/sans CEC (Q11) + sources

COUVERTURE : 100% du contenu clinique des 12 questions + Tableau 1, y compris toutes
les posologies chiffrees (danaparoide, lepirudine, desirudine, tirofiban, protocoles
CEC). Comite d'organisation, groupe de lecture (listes nominatives) et la
bibliographie ne sont pas retranscrits (sans contenu clinique actionnable).
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from style import *
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.units import mm

OUT = "/home/user/rfe-sfar-website/output/Fiche_SFAR_Thrombopenie_Induite_Heparine_2002.pdf"

SOURCE_TXT = ("Source : SFAR, Conférence d'experts 2002 (Comité d'organisation Y. Blanloeil) — "
              "« Thrombopénie induite par l'héparine » — Ann Fr Anesth Reanim 2003;22:150-159. "
              "Fiche de synthèse non officielle : se référer au texte intégral.")

def P(txt, style=S_CELL):
    return Paragraph(txt, style)

def theme_table(rows, col_widths=None, head_theme="Thème", head_txt="Contenu (fidèle à la source)"):
    """rows: (theme, text) - pas de grade/force impirime par cette source (voir
    docstring module) : theme remplace la colonne Grade habituelle."""
    cw = PAGE_W - 2 * MARGIN
    if col_widths is None:
        theme_w = 36 * mm
        col_widths = [theme_w, cw - theme_w]
    data = [[P(head_theme, S_HEAD_W), P(head_txt, S_HEAD_W)]]
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

def drug_table():
    """Q7 - tableau comparatif des 3 traitements de substitution. Contenu integral
    (mecanisme, demi-vie, voie, posologie, surveillance, particularites) issu du
    texte source, pas d'une source graphique."""
    cw = PAGE_W - 2 * MARGIN
    c0 = 26 * mm
    c1 = c2 = c3 = (cw - c0) / 3.0
    S_DH = pstyle("dh", fontSize=7.9, leading=9.6, textColor=WHITE, fontName=FONT_BOLD, alignment=TA_CENTER)
    S_DC = pstyle("dc", fontSize=7.6, leading=9.4, textColor=INK)
    S_DCB = pstyle("dcb", fontSize=7.8, leading=9.6, textColor=WHITE, fontName=FONT_BOLD, alignment=TA_CENTER)
    def dc(txt, style=S_DC):
        return Paragraph(txt, style)
    data = [
        [dc("", S_DH), dc("Danaparoïde sodique<br/>(Orgaran®)", S_DH),
         dc("Lépirudine<br/>(Refludan®) — <b>retirée du marché depuis 2012</b>", S_DH),
         dc("Désirudine<br/>(Revasc®)", S_DH)],
        [dc("Mécanisme", S_DCB),
         dc("Héparinoïde : activité anti-Xa prédominante, faible activité anti-IIa.", S_DC),
         dc("Hirudine recombinante, inhibiteur direct de la thrombine (bloque fibrinoformation "
            "et activation plaquettaire).", S_DC),
         dc("Hirudine recombinante, SC uniquement.", S_DC)],
        [dc("Demi-vie", S_DCB),
         dc("Anti-Xa ≈ 25 h ; anti-IIa ≈ 7 h.", S_DC),
         dc("0,8 à 1,7 h ; élimination essentiellement rénale.", S_DC),
         dc("2 à 3 h ; élimination urinaire 40-50 % de la dose.", S_DC)],
        [dc("Voie / indication", S_DCB),
         dc("SC (prophylaxie) ou IV continue (bolus + entretien). AMM : prophylaxie MTEV "
            "chirurgie onco./orthopédique ; prophylaxie et traitement curatif des "
            "manifestations thromboemboliques de la TIH.", S_DC),
         dc("IV uniquement. AMM : traitement des patients adultes atteints de TIH et de "
            "maladie thromboembolique.", S_DC),
         dc("SC uniquement, 15 mg × 2/j sans adaptation au poids. AMM : prévention de la "
            "thrombose veineuse après prothèse de hanche/genou — <b>non étudiée en TIH à la "
            "phase aiguë</b>, proposable en prévention chez un patient aux antécédents de TIH.",
            S_DC)],
        [dc("Posologie phase aiguë TIH", S_DCB),
         dc("SC prophylactique, phase aiguë : 750 U ×3/j (≤90 kg) ou 1250 U ×3/j (>90 kg) ; "
            "<i>à distance de la TIH</i> : 750 U ×2/j (≤90 kg) ou 1250 U ×2/j (>90 kg). "
            "IV curatif — charge selon poids : <b>1250 U (≤55 kg), 2500 U (55-90 kg), "
            "3750 U (>90 kg)</b>, puis entretien 400 U/h (4h), 300 U/h (4h), puis 150-200 U/h "
            "ajusté à l'activité anti-Xa (cible curative 0,5-0,8 U/ml). SC curatif — entretien "
            "selon poids : 1500 U ×2/j (≤55 kg), 2000 U ×2/j (55-90 kg), 1750 U ×3/j (>90 kg). "
            "Pédiatrie (thrombose constituée) : bolus 30 U/kg puis entretien 1,2-2,0 U/kg/h.",
            S_DC),
         dc("Bolus IV 0,4 mg/kg puis perfusion continue 0,15 mg/kg/h. En cas d'insuffisance "
            "rénale : adapter bolus et débit selon la clairance de la créatinine et les tests "
            "biologiques (<i>certaines équipes préconisent de diminuer systématiquement de "
            "moitié le bolus initial</i>). Grande variabilité intra/interindividuelle : le "
            "débit de perfusion doit souvent être réduit dès les premières heures.",
            S_DC),
         dc("15 mg SC × 2/j fixe. Précautions si risque hémorragique accru.", S_DC)],
        [dc("Surveillance", S_DCB),
         dc("Numération plaquettaire quotidienne jusqu'à normalisation ; au moins 2×/semaine "
            "pendant les 2 premières semaines de traitement. Activité anti-Xa si besoin (cible "
            "0,5-0,8 U/ml).", S_DC),
         dc("TCA (limites reconnues par les experts) ; centres spécialisés recommandés compte "
            "tenu de la difficulté du suivi biologique.", S_DC),
         dc("TCA en cas d'insuffisance rénale (ratio <2 au pic, 1-3 h post-injection).", S_DC)],
        [dc("Échec / surdosage", S_DCB),
         dc("Si la numération ne remonte pas — a fortiori si thrombopénie et/ou thrombose "
            "persiste sous danaparoïde — <b>évoquer une réactivité croisée et envisager la "
            "lépirudine.</b> Surdosage : arrêter le danaparoïde ; la protamine neutralise "
            "partiellement son activité mais n'est pas recommandée par le RCP ; en cas "
            "d'hémorragie grave, transfusion de plasma frais/plaquettes, plasmaphérèse si "
            "hémorragie incontrôlable.", S_DC),
         dc("Pas d'antagoniste ; en cas d'hémorragie menaçante, hémofiltration/hémodialyse à "
            "haut flux (membrane ≤50 000 daltons) peuvent être utiles selon le RCP. Risque "
            "hémorragique majoré par : insuffisance rénale, traitement thrombolytique associé, "
            "chirurgie ou cathétérisme récents.", S_DC),
         dc("Non étudiée en TIH à la phase aiguë (voir ligne Voie/indication). Pas "
            "d'antagoniste connu.", S_DC)],
        [dc("Particularités", S_DCB),
         dc("Réactivité croisée in vitro 5-10 %, conséquences cliniques rares. Élimination "
            "rénale : adapter selon activité anti-Xa. Prudence avec aspirine (risque "
            "hémorragique). Relais AVK possible après 5-7 j de traitement et plaquettes "
            ">100 G/L ; <b>n'arrêter le danaparoïde que lorsque l'INR est en zone thérapeutique "
            "2 j de suite et après un minimum de 72 h d'AVK.</b> <b>Ne passe pas la barrière "
            "placentaire</b> : recommandé chez la femme enceinte. AMM couvre aussi les "
            "patients aux antécédents documentés de TIH.", S_DC),
         dc("<b>Contre-indiquée chez la femme enceinte.</b> Relais AVK débuté seulement après "
            "réduction progressive de la lépirudine (TCA ≈1,5×témoin), arrêt à INR = 2.",
            S_DC),
         dc("", S_DC)],
    ]
    t = Table(data, colWidths=[c0, c1, c2, c3], repeatRows=1)
    style_cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), TEAL_DARK),
        ("BACKGROUND", (0, 1), (0, -1), NAVY),
        ("GRID", (0, 0), (-1, -1), 0.5, GREY_LIGHT),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 3.2), ("BOTTOMPADDING", (0, 0), (-1, -1), 3.2),
        ("LEFTPADDING", (0, 0), (-1, -1), 4), ("RIGHTPADDING", (0, 0), (-1, -1), 4),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            style_cmds.append(("BACKGROUND", (1, i), (-1, i), BG_PANEL))
    t.setStyle(TableStyle(style_cmds))
    return t

def tableau1():
    """Tableau 1 source - Principes generaux de prise en charge (texte integral, pas
    une figure graphique - reproduit ici comme tableau texte 2 lignes thematiques
    conforme a la structure source : antecedents de TIH / phase aigue de TIH)."""
    cw = PAGE_W - 2 * MARGIN
    c0 = 40 * mm
    data = [
        [P("Situation", S_HEAD_W), P("Conduite proposée par la source", S_HEAD_W)],
        [P("1. Antécédents de TIH, anticoagulation nécessaire", S_CELL_B),
         P("Éviter la réintroduction d'héparine sous quelque forme/dose que ce soit, en "
           "particulier dans les 3 mois suivant la TIH et si anticorps encore détectables en "
           "ELISA. Exception : CEC en chirurgie cardiaque, HNF seule envisageable en l'absence "
           "d'anticorps détectables, ou sous couvert d'un antiplaquettaire (iloprost/"
           "époprosténol) si anticorps persistants — uniquement en période peropératoire. "
           "Danaparoïde sodique SC recommandé pour la prophylaxie médicale/chirurgicale, sauf "
           "possiblement en chirurgie de prothèse de hanche/genou où la désirudine peut être "
           "préférée.")],
        [P("2. Phase aiguë de TIH — pour tous les patients", S_CELL_B),
         P("Dès suspicion : arrêter immédiatement toute héparine (y compris purges de "
           "cathéter) ; supprimer toute ligne intravasculaire pré-enduite d'héparine ; "
           "hospitaliser en unité de soins intensifs ; contacter un laboratoire d'hémostase "
           "spécialisé ; rechercher systématiquement une TVP ; rechercher quotidiennement par "
           "l'examen clinique une complication thromboembolique.")],
        [P("2a. Sans indication de traitement curatif", S_CELL_B),
         P("Danaparoïde sodique à doses au moins prophylactiques jusqu'à correction plaquettaire, "
           "relais AVK envisagé si prévention prolongée. Lépirudine semble aussi efficace "
           "(moins de patients étudiés dans cette situation) mais risque hémorragique "
           "probablement plus élevé qu'avec le danaparoïde (pas de comparaison randomisée "
           "directe) ; sans AMM française dans cette indication.")],
        [P("2b. Avec thrombose artérielle ou veineuse", S_CELL_B),
         P("Danaparoïde sodique ou lépirudine à doses curatives — efficacité voisine, risque "
           "hémorragique probablement plus élevé avec la lépirudine (pas de comparaison "
           "randomisée directe). Adapter la dose à la fonction rénale et à la surveillance "
           "biologique dans les deux cas. Si pronostic fonctionnel du membre et/ou vital "
           "engagé : thrombolyse médicamenteuse ou geste chirurgical/radiologique sous "
           "danaparoïde ou lépirudine.")],
    ]
    t = Table(data, colWidths=[c0, cw - c0], repeatRows=1)
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

TOTAL_PAGES = {"n": 2}

def on_page(canvas, doc, page_title):
    header_band(canvas, doc, "SFAR — 2002 — CONFÉRENCE D'EXPERTS, TEXTE COURT — HISTORIQUE",
                "Thrombopénie induite par l'héparine (2002)",
                page_title, icon_fn=lambda c, x, y: icon_drop(c, x, y, 13 * mm), color=NAVY)
    footer_band(canvas, doc, SOURCE_TXT, f"Page {doc.page} / {TOTAL_PAGES['n']}")

# ---------------------------------------------------------------------------
def _section_intro():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Champ :</b> diagnostic, prévention et traitement de la <b>thrombopénie induite "
        "par l'héparine de type II (TIH)</b> — thrombopénie immuno-allergique rare mais "
        "potentiellement grave, survenant sous héparine non fractionnée (HNF) ou héparine de "
        "bas poids moléculaire (HBPM). On distingue la thrombopénie de type I (bénigne, non "
        "immune, précoce, régressant malgré la poursuite de l'héparine — n'est PAS une TIH) de "
        "la thrombopénie de type II, potentiellement grave et d'origine immune, qui seule est "
        "désignée « TIH » dans ce document.", S_BODY), bg=BG_PANEL, border=NAVY))
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>📖 Document historique — une fiche plus récente existe dans cette bibliothèque :</b> "
        "les <b>« Propositions du GIHP et du GFHT pour le diagnostic et la prise en charge d'une "
        "TIH » (2019)</b> sont le document de référence ACTUEL sur ce sujet (40 propositions, "
        "score des 4T, argatroban, bivalirudine, anticoagulants oraux directs). Consultez-les en "
        "priorité pour une décision thérapeutique. Cette fiche de 2002, plus ancienne, est "
        "conservée séparément pour sa valeur documentaire (critères diagnostiques cliniques et "
        "biologiques largement toujours pertinents, protocoles détaillés de chirurgie cardiaque "
        "sous CEC) — voir l'avertissement sur l'obsolescence thérapeutique ci-dessous.",
        S_BODY_SM), bg=AMBER_LIGHT, border=AMBER))
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Méthodologie :</b> conférence d'experts (2002), <b>sans système de grade formel.</b> "
        "La source le dit explicitement : « le niveau de preuve des études est faible et la "
        "force des recommandations en médecine factuelle [...] est du niveau le plus bas. Les "
        "experts ont donc estimé inutile d'assortir chaque proposition d'un grade de "
        "recommandation » — malgré cela, la gravité potentielle et les difficultés "
        "diagnostiques/thérapeutiques justifient la conférence. Aucun grade n'est donc affiché "
        "dans cette fiche : sa colonne « Thème » remplace la colonne de grade habituelle.",
        S_BODY_SM), bg=BG_PANEL, border=AMBER))
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>⚠ Avertissement sur l'actualité thérapeutique (ajout de cette fiche, absent de la "
        "source) :</b> ce document date de 2002/2003. Les critères diagnostiques cliniques et "
        "biologiques restent valables, mais l'arsenal thérapeutique a évolué depuis : la "
        "<b>lépirudine (Refludan®), présentée ci-après comme option de 1<sup>re</sup> ligne, a "
        "été retirée du marché en Europe en 2012</b> et n'est plus disponible. L'argatroban et "
        "le fondaparinux — cités par la source comme « non encore disponibles en France » / "
        "« non encore rapportés dans la TIH » en 2002 — sont aujourd'hui des alternatives "
        "courantes. <b>Vérifier le protocole local/les molécules effectivement disponibles "
        "avant toute prescription.</b>", S_BODY_SM), bg=RED_LIGHT, border=RED))
    story.append(Spacer(1, 4 * mm))

    story.append(section_bar("Définitions et physiopathologie", color=TEAL_DARK))
    story.append(Spacer(1, 2 * mm))
    story.append(theme_table([
        ("Type I vs type II", "Depuis 1980, deux types de thrombopénie sous héparine sont "
         "distingués. <b>Type I</b> : bénigne, non immune, précoce, sans complication "
         "thrombotique, régresse malgré la poursuite de l'héparine. <b>Type II</b> : "
         "potentiellement grave, d'origine immune, d'apparition en règle plus tardive — c'est "
         "la TIH proprement dite, qu'elle survienne sous HNF ou HBPM."),
        ("Mécanisme", "Syndrome clinico-biologique induit par des anticorps (souvent IgG) "
         "reconnaissant le facteur 4 plaquettaire (F4P) modifié par l'héparine, avec activation "
         "plaquettaire intense et activation de la coagulation pouvant aboutir à des "
         "thromboses veineuses et/ou artérielles. La thrombopénie résulte de l'activation "
         "massive des plaquettes in vivo et de leur élimination par le système des phagocytes "
         "mononucléés. Les thromboses résultent d'une activation pluricellulaire (plaquettes, "
         "cellules endothéliales, monocytes)."),
        ("Épidémiologie", "Fréquence de la TIH sous HNF plus élevée en milieu chirurgical "
         "(≈3 % en moyenne) qu'en milieu médical (≈1 % en moyenne), pouvant atteindre 5 % en "
         "chirurgie cardiaque et orthopédique. Sous HBPM, la TIH est plus rare mais possible."),
        ("Difficulté diagnostique", "Le diagnostic est difficile lorsque d'autres causes de "
         "thrombopénie existent, notamment en période postopératoire ou en réanimation — "
         "l'arrêt systématique de l'héparine devant toute thrombopénie peut poser des problèmes "
         "thérapeutiques. Le diagnostic doit intégrer les circonstances cliniques et les "
         "traitements associés ; il ne peut être établi formellement que plusieurs jours après "
         "la suspicion et <b>ne doit jamais retarder l'arrêt de l'héparine et la prescription "
         "d'un antithrombotique de substitution à action immédiate.</b>"),
    ]))
    return story

def _section_diagnostic_clinique():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("Circonstances évocatrices du diagnostic (Q1)", color=TEAL_DARK))
    story.append(Spacer(1, 2 * mm))
    story.append(theme_table([
        ("Particularités", "Deux éléments caractérisent la TIH : la chronologie de la "
         "thrombopénie par rapport à l'administration d'héparine, et la rareté des "
         "manifestations hémorragiques contrastant avec la fréquence des accidents "
         "thrombotiques veineux et/ou artériels."),
        ("Délai de survenue", "Typiquement 5 à 8 jours après le début de l'héparinothérapie. "
         "Peut être plus court (avant le 5<sup>e</sup> jour, voire dès le 1<sup>er</sup> jour) "
         "chez un patient exposé à l'héparine dans les 3 mois précédents. Peut aussi être plus "
         "long, notamment avec les HBPM, pouvant excéder 3 semaines."),
        ("Seuil numération", "Diagnostic à évoquer devant une numération plaquettaire "
         "&lt;100 G/l et/ou une diminution &gt;40 % par rapport à la numération initiale ; la "
         "thrombopénie est comprise entre 30 et 70 G/l chez 80 % des patients. Une CIVD est "
         "rapportée dans 10-20 % des cas selon les critères diagnostiques — elle n'exclut pas "
         "le diagnostic de TIH et aggrave la thrombopénie. En réanimation/postopératoire, la "
         "coexistence d'autres pathologies (sepsis, hémorragie, transfusion massive, CIVD) peut "
         "aboutir à une thrombopénie plus profonde. Plus rarement, des complications "
         "thrombotiques surviennent en l'absence de thrombopénie vraie."),
        ("Complications thrombotiques", "Très évocatrices. TVP chez 50 % des patients avec TIH "
         "(recherche systématique justifiée) ; embolie pulmonaire dans 10 à 25 % des cas. "
         "Gangrène veineuse des membres : rare, peut compliquer une TIH quand un traitement par "
         "AVK a été institué sans autre antithrombotique. Résistance à l'héparinothérapie avec "
         "extension du processus thrombotique initial : circonstance de découverte à ne pas "
         "méconnaître. Thromboses artérielles : les plus typiques bien que moins fréquentes que "
         "les veineuses, tous territoires possibles, plus grande fréquence pour l'aorte "
         "abdominale et ses branches. Complications neurologiques chez 9,5 % des patients : "
         "AVC ischémiques, thromboses veineuses cérébrales, états confusionnels, amnésies "
         "transitoires (par ordre de fréquence décroissante)."),
        ("Autres complications", "Plus rarement observées : lésions dermatologiques (nécroses "
         "cutanées aux points d'injection d'héparine, pouvant être inaugurales et précéder la "
         "thrombopénie) ; nécroses hémorragiques des surrénales ; complications hémorragiques "
         "(rares, favorisées par une CIVD, associées à une mortalité élevée)."),
    ]))
    return story

def _section_diagnostic_bio():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("Diagnostic biologique et démarche pratique (Q2 + Q3)", color=TEAL_DARK))
    story.append(Spacer(1, 2 * mm))
    story.append(theme_table([
        ("Confirmation", "La confirmation de la thrombopénie est indispensable et urgente : "
         "prélèvement sur tube citraté et/ou capillaire, avec contrôle sur lame. Une CIVD doit "
         "être recherchée systématiquement."),
        ("Tests Elisa", "Détectent les anticorps (IgG, IgM, IgA) dirigés contre le F4P en "
         "présence d'héparine — simples, sensibilité ≈95 %. Peuvent être positifs sans TIH "
         "associée, notamment au décours d'une CEC. Dans de rares cas, le test Elisa F4P-héparine "
         "est négatif car le F4P n'est pas la cible antigénique des anticorps."),
        ("Tests d'activation plaquettaire", "Tests fonctionnels (agrégation plaquettaire — AP, "
         "ou sérotonine radiomarquée — SRA) montrant la présence d'anticorps IgG "
         "héparine-dépendants activant les plaquettes. AP : spécificité jusqu'à 80 %, "
         "sensibilité jusqu'à 91 % avec plaquettes de plusieurs témoins (les plaquettes témoins "
         "lavées améliorent les performances) ; test long et délicat. SRA : sensibilité "
         "supérieure à l'AP mais n'atteignant pas 100 %, meilleure spécificité (≈100 %), réactif "
         "radiomarqué disponible dans quelques laboratoires seulement."),
        ("Démarche pratique", "Le diagnostic repose sur un faisceau d'arguments : chronologiques "
         "(numération/héparine), séméiologiques (accidents thromboemboliques), biologiques "
         "(anticorps héparine-dépendants), après recherche rigoureuse d'une autre cause. La "
         "normalisation de la numération à l'arrêt de l'héparine est capitale (élément "
         "rétrospectif) : ré-ascension dès la 48<sup>e</sup> h, correction moyenne au-dessus de "
         "150 G/l en 4 à 7 j (jusqu'à 2 semaines si thrombopénie très marquée et/ou CIVD). "
         "Éliminer une pseudothrombopénie (contacter l'hématologie biologique en cas de "
         "persistance sur tube citraté). Une authentique TIH peut survenir sans thrombopénie "
         "vraie : seule une baisse &gt;40 % par rapport à une référence préthérapeutique suffit."),
        ("Autres éléments", "Interrogatoire/anamnèse rigoureux (traitements associés "
         "potentiellement thrombopéniants : antibiotiques, diurétiques...) ; rechercher une "
         "autre pathologie hématologique aiguë et une allo-immunisation antiplaquettaire en cas "
         "de transfusion récente. L'arrêt de l'héparine et son remplacement par un "
         "antithrombotique d'action immédiate doivent être décidés dès la suspicion, sans "
         "attendre les résultats biologiques. Prélèvement pour recherche d'anticorps de "
         "préférence après l'arrêt de l'héparine ; délai de résultat optimal 48-72 h."),
        ("Interprétation combinée", "Les deux types de tests (Elisa + fonctionnel) sont "
         "complémentaires, à réaliser systématiquement ensemble : si les 2 sont positifs, TIH "
         "très probable ; si les 2 sont négatifs, TIH peu probable (mais non formellement "
         "exclue si la probabilité clinique reste élevée) ; plus rarement, un seul test positif "
         "peut correspondre à une authentique TIH (ex. Elisa seul positif = anticorps IgA/IgM "
         "n'activant pas les plaquettes in vitro — insuffisant après CEC pour retenir seul le "
         "diagnostic)."),
        ("Conclusion et déclaration", "Au terme de l'épisode, aboutir à une conclusion "
         "diagnostique claire intégrant l'évolution plaquettaire. <b>Déclaration obligatoire</b> "
         "au centre régional de pharmacovigilance de toute suspicion de TIH."),
    ]))
    return story

def _section_diff_prevention():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("Diagnostic différentiel, prévention, surveillance (Q4-Q6)", color=TEAL_DARK))
    story.append(Spacer(1, 2 * mm))
    story.append(theme_table([
        ("Diagnostic différentiel — lié à l'héparine", "Une thrombopénie précoce (2 premiers "
         "jours), modérée, peut résulter de l'effet proagrégant de l'HNF, ou témoigner d'une "
         "TIH de survenue précoce après réintroduction d'héparine chez un patient déjà "
         "sensibilisé."),
        ("Diagnostic différentiel — autres causes", "Hémodilution postopératoire, consommation "
         "plaquettaire dans les circuits extracorporels ou par contre-pulsion intra-aortique "
         "(circonstances généralement faciles à identifier). Purpura post-transfusionnel "
         "(allo-immunisation, baisse majeure brutale des plaquettes + contexte hémorragique) : "
         "diagnostic indispensable compte tenu de l'attitude différente et de l'urgence de la "
         "décision. Inhibiteurs des glycoprotéines GPIIb-IIIa (syndromes coronaires aigus) : "
         "thrombopénie précoce et majeure possible. Chimiothérapies antimitotiques chez le "
         "patient cancéreux : diagnostic de TIH formel délicat du fait des facteurs confondants."),
        ("Prévention primaire", "Trois axes : utiliser les héparines uniquement dans les "
         "indications validées ; durée d'utilisation la plus courte possible avec relais "
         "précoce par AVK ; utilisation préférentielle des HBPM dans les indications démontrées."),
        ("Prévention secondaire", "Établissement, pour chaque patient ayant présenté une TIH, "
         "d'un certificat médical attestant le diagnostic."),
        ("Surveillance systématique", "S'applique à tous les patients recevant de l'héparine, "
         "quels que soient poids moléculaire, dose et voie d'administration (IV, SC, purge de "
         "cathéter, cathéter/circuit pré-enduit d'héparine). Numération plaquettaire avant le "
         "début du traitement, puis à partir du 5<sup>e</sup> jour, au moins 2 fois par semaine "
         "pendant au moins le premier mois. Chez le patient chirurgical, les numérations "
         "péri-opératoires immédiates servent de référence, permettant de détecter l'absence de "
         "ré-ascension des plaquettes ou leur diminution de 40 % après leur ré-ascension. Chez "
         "un patient déjà exposé à "
         "l'héparine dans les 3 mois précédents : surveillance dès les premières heures après "
         "réintroduction. Rechercher une TIH quelle que soit l'évolution plaquettaire chez tout "
         "patient présentant une thrombose ou une aggravation d'une thrombose préexistante sous "
         "héparine."),
    ]))
    return story

def _section_traitements():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("Traitements de substitution (Q7)", color=TEAL_DARK))
    story.append(Spacer(1, 1.5 * mm))
    story.append(info_panel(P(
        "⚠ Voir l'avertissement d'actualité thérapeutique en page 1 : la <b>lépirudine "
        "(Refludan®) n'est plus commercialisée</b> depuis 2012. Les posologies ci-dessous sont "
        "reproduites fidèlement depuis le texte source de 2002 à titre documentaire.",
        S_BODY_SM), bg=RED_LIGHT, border=RED))
    story.append(Spacer(1, 2 * mm))
    story.append(drug_table())
    story.append(Spacer(1, 1.5 * mm))
    story.append(P("Aucune étude comparative directe entre danaparoïde sodique et lépirudine "
                    "(efficacité ni tolérance) ; aucun antagoniste pharmacologique pour ces deux "
                    "médicaments.", S_NOTE))
    return story

def _section_ci_tableau1():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("Thérapeutiques dangereuses (Q8)", color=TEAL_DARK))
    story.append(Spacer(1, 2 * mm))
    story.append(theme_table([
        ("Contre-indications formelles", "Les HBPM sont formellement contre-indiquées en cas de "
         "TIH sous HNF. Les AVK ne doivent jamais être utilisés seuls."),
        ("Transfusion plaquettaire", "Non recommandée car elle peut favoriser la survenue de "
         "thromboses ou le processus de consommation. Les hémorragies associées à la TIH sont "
         "exceptionnelles, mais des transfusions plaquettaires sont envisageables en cas de "
         "saignement grave."),
    ]))
    story.append(Spacer(1, 4 * mm))
    story.append(section_bar("Tableau 1 — Principes généraux de prise en charge", color=TEAL_DARK))
    story.append(Spacer(1, 2 * mm))
    story.append(tableau1())
    return story

def _section_autres_traitements():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("Autres traitements possibles (Q9)", color=TEAL_DARK))
    story.append(Spacer(1, 2 * mm))
    story.append(theme_table([
        ("Antagonistes de la vitamine K", "Ne doivent jamais être utilisés seuls à la phase "
         "aiguë ; introduits au plus tôt lorsque la ré-ascension plaquettaire est confirmée, "
         "sous couvert d'un anticoagulant efficace (danaparoïde ou hirudine). Relais "
         "danaparoïde-AVK ou lépirudine-AVK nécessitent des précautions (RCP)."),
        ("Agents antiplaquettaires", "Ne peuvent être utilisés seuls. Intérêt discutable de "
         "l'association à un anticoagulant dans certains cas de TIH avec complications "
         "thrombotiques artérielles ; l'association aspirine + anticoagulant augmente le risque "
         "hémorragique, sans efficacité validée. Iloprost et époprosténol : risque "
         "d'hypotension sévère, non indiqués hors chirurgie cardiovasculaire. Antagonistes des "
         "récepteurs GPIIb-IIIa utilisés avec succès dans de rares cas d'occlusion coronaire "
         "aiguë post-angioplastie au cours de TIH ; tirofiban utilisé pour la réalisation de "
         "CEC en chirurgie cardiaque."),
        ("Thrombolytiques", "Indication possible dans la prise en charge des complications "
         "thrombotiques graves survenant au cours des TIH."),
        ("Immunoglobulines, plasmaphérèses", "Utilisées exceptionnellement."),
        ("Interruption cave", "Pose d'un filtre proposable en cas d'embolie pulmonaire grave "
         "associée à un risque hémorragique élevé, mais avec un risque d'oblitération "
         "thrombotique aiguë du filtre."),
        ("Chirurgie", "La thromboembolectomie chirurgicale fait partie de l'éventail "
         "thérapeutique, mais sa pratique est exceptionnelle — justifiée lorsque l'ischémie "
         "menace le pronostic fonctionnel du membre et/ou le pronostic vital."),
        ("Molécules non disponibles en France en 2002", "L'argatroban (antithrombine directe, "
         "déjà autorisée pour la TIH au Japon et en Amérique du Nord) et le ximelagatran "
         "(antithrombine directe orale) sont cités comme potentiellement intéressants mais non "
         "encore disponibles/rapportés dans la TIH à la date de la source. Le fondaparinux "
         "(Arixtra®, pentasaccharide anti-Xa pur) : utilisation thérapeutique dans la TIH non "
         "encore rapportée à la date de la source. <i>Voir l'avertissement d'actualité "
         "thérapeutique en page 1 — ces molécules sont aujourd'hui d'usage courant.</i>"),
    ]))
    return story

def _section_strategies_contextes():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("Stratégies — milieu médical (Q10)", color=TEAL_DARK))
    story.append(Spacer(1, 2 * mm))
    story.append(theme_table([
        ("Anticoagulation curative", "MTEV, insuffisance coronaire aiguë, cardiopathies "
         "arythmiques : lépirudine ou danaparoïde sodique utilisés prioritairement selon le "
         "terrain (risque hémorragique, insuffisance rénale) et les possibilités locales de "
         "surveillance biologique."),
        ("Prophylaxie MTEV", "Usage préférentiel du danaparoïde sodique recommandé."),
        ("Radiologie interventionnelle", "Lépirudine recommandée ; danaparoïde sodique "
         "possible."),
        ("Hémodialyse séquentielle", "Danaparoïde sodique utilisable avec surveillance "
         "biologique étroite (activité anti-Xa résiduelle non négligeable en fin de séance + "
         "demi-vie longue → risque hémorragique plusieurs heures après la fin de la dialyse). "
         "Lépirudine envisageable avec membranes de faible perméabilité, mais risque "
         "hémorragique augmenté. Citrate de sodium ou prostacycline envisageables en centres "
         "expérimentés."),
        ("Hémofiltration", "Danaparoïde sodique : solution la plus logique (mêmes limitations "
         "que pour l'hémodialyse séquentielle). Lépirudine en 2<sup>e</sup> intention (expérience "
         "limitée). Citrate de sodium (contraintes techniques) et prostacycline (risque "
         "d'instabilité hémodynamique) : facteurs limitants majeurs."),
        ("Héparinisation des cathéters", "Arrêt impératif de toute héparinisation et ablation "
         "des matériels imprégnés d'héparine. Perméabilité maintenue sans anticoagulant ou avec "
         "citrate de sodium ; coumadine à dose fixe 1 mg/j : alternative possible. Chambres "
         "implantables : absence d'anticoagulation possible, sinon citrate de sodium ou "
         "danaparoïde sodique."),
        ("Femme enceinte", "Danaparoïde sodique recommandé (ne passe pas la barrière "
         "placentaire). Lépirudine contre-indiquée."),
        ("Enfant", "Danaparoïde sodique ou lépirudine utilisables avec adaptation des doses et "
         "surveillance biologique adaptée."),
    ]))
    story.append(Spacer(1, 4 * mm))
    story.append(section_bar("Stratégies — chirurgie non cardiaque (Q12)", color=TEAL_DARK))
    story.append(Spacer(1, 2 * mm))
    story.append(theme_table([
        ("Chirurgie vasculaire", "Protocoles de chirurgie cardiaque proposables pour la "
         "chirurgie aortique si anticoagulation péri-opératoire nécessaire. Certaines "
         "chirurgies artérielles proximales réalisables sans anticoagulant."),
        ("Thrombose artérielle", "Désobstruction chirurgicale ou thrombolyse à discuter."),
        ("Antécédent de TIH + anticoagulation préventive nécessaire", "Danaparoïde sodique "
         "préférentiellement indiqué. Alternative après prothèse de hanche/genou : désirudine, "
         "avec relais précoce par AVK si nécessaire."),
        ("Antécédent de TIH + anticoagulation curative nécessaire", "Danaparoïde sodique en "
         "1<sup>re</sup> intention, relais AVK entre le 5<sup>e</sup> et le 7<sup>e</sup> jour."),
        ("TIH en cours, sans thrombose", "Danaparoïde sodique, relais AVK si possible entre le "
         "5<sup>e</sup> et le 7<sup>e</sup> jour."),
        ("TIH en cours, avec thrombose", "Danaparoïde sodique ou lépirudine, relais AVK entre le "
         "5<sup>e</sup> et le 7<sup>e</sup> jour."),
        ("Embolie pulmonaire grave + anticoagulant contre-indiqué", "Barrage cave à discuter."),
    ]))
    return story

def _section_cardiaque():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("Stratégies en chirurgie cardiaque avec/sans CEC (Q11)", color=TEAL_DARK))
    story.append(Spacer(1, 2 * mm))
    story.append(theme_table([
        ("Choix de 1<sup>re</sup> intention", "Deux possibilités : HNF associée à un antiplaquettaire "
         "puissant, ou lépirudine. Choix basé sur la disponibilité des médicaments et des "
         "moyens de surveillance biologique, l'expérience de l'équipe médico-chirurgicale et les "
         "morbidités associées du patient (insuffisance rénale, risque d'hypotension artérielle "
         "prolongée...)."),
        ("HNF + iloprost/époprosténol", "Anticoagulation per-CEC par HNF aux doses habituelles + "
         "inhibiteur puissant des fonctions plaquettaires. Iloprost débuté dès l'induction "
         "(3 ng/kg/min, paliers jusqu'à 30-50 ng/kg/min) avec vérification de l'inhibition de "
         "l'agrégation plaquettaire avant l'injection d'HNF (300 U/kg) ; en fin de CEC, iloprost "
         "réduit à 6 ng/kg/min puis arrêté après administration de protamine. L'augmentation des "
         "doses d'iloprost entraîne souvent une hypotension corrigée par noradrénaline à doses "
         "parfois élevées. Époprosténol utilisable en remplacement de l'iloprost."),
        ("HNF + tirofiban", "Protocole : tirofiban 10 µg/kg en bolus 5 min avant l'héparine, "
         "puis perfusion continue 0,15 µg/kg/min arrêtée au déclampage aortique. HNF 400 UI/kg "
         "en bolus avant la CEC, injections supplémentaires pour ACT &gt;480 s, neutralisée par "
         "protamine en fin de CEC. Aprotinine souvent associée. Recommandé pour les patients "
         "avec insuffisance rénale préopératoire (risque de saignement excessif majoré avec la "
         "lépirudine). Choix justifié par l'absence d'effet hémodynamique et la récupération des "
         "fonctions plaquettaires en 8 h après l'arrêt."),
        ("Lépirudine (protocole CEC)", "Bolus 0,25 mg/kg + 0,20 mg/kg dans le volume d'amorçage "
         "de la CEC, puis perfusion continue 0,15 mg/kg/h (réservoir de cardiotomie de "
         "préférence). Surveillance par ECT (temps de coagulation à l'écarine) toutes les "
         "15 min — déplacement d'une équipe d'hémostase au bloc le plus souvent nécessaire ; "
         "une CEC réglée sans monitorage ECT n'est pas raisonnable sous lépirudine. Aprotinine "
         "possible. Monitorage TCA avant/après CEC (limites reconnues). Demi-vie prolongée en "
         "insuffisance rénale, risque de saignement excessif élevé — hémofiltration "
         "veino-veineuse sans anticoagulant, jusqu'à thrombose du filtre, proposable pour "
         "l'élimination de la lépirudine circulante."),
        ("Danaparoïde sodique en CEC", "<b>Non recommandé en 1<sup>re</sup> intention</b> pour "
         "l'anticoagulation per-CEC en raison de sa demi-vie longue (≈25 h pour l'activité "
         "anti-Xa) et de la fréquence élevée de saignements postopératoires excessifs "
         "rapportés — sauf en l'absence de toute autre alternative, en suivant les "
         "recommandations du RCP."),
        ("Anticoagulation postopératoire", "Après antiplaquettaire + HNF : relais par "
         "danaparoïde sodique (SC ou IV si bas débit cardiaque) ou lépirudine. Après "
         "lépirudine : relais par lépirudine (0,05-0,1 mg/kg/h, adaptée aux résultats "
         "biologiques) ou danaparoïde sodique. Après danaparoïde sodique : traitement continué."),
        ("Circuits pré-héparinés", "Si l'anticoagulation de la CEC est réalisée avec HNF + "
         "antiplaquettaire, le choix d'un circuit pré-héparinés ne modifie pas les problèmes "
         "liés à la TIH. Si l'anticoagulation est réalisée avec un anticoagulant autre que "
         "l'HNF, les circuits pré-héparinés ne doivent pas être utilisés."),
        ("Stratégie chez le patient en TIH active", "HNF seule est interdite dans tous les cas. "
         "Chirurgie non urgente : attendre la disparition des anticorps. Chirurgie non "
         "différable, fonction rénale normale : HNF + antiplaquettaire puissant ou lépirudine, "
         "voire danaparoïde sodique. Fonction rénale altérée : HNF + antiplaquettaire puissant, "
         "voire lépirudine avec hémofiltration ; envisager d'adresser le patient à un centre "
         "médico-chirurgical expérimenté pour une chirurgie réglée."),
        ("Stratégie chez le patient aux antécédents de TIH", "Rechercher la présence "
         "d'anticorps anti-F4P-héparine. Anticorps présents : même conduite que ci-dessus si "
         "l'intervention ne peut être différée, ou attente d'au moins 3 mois pour leur "
         "disparition. Anticorps absents : HNF proscrite en pré/postopératoire mais utilisable "
         "seule pendant l'intervention ; danaparoïde sodique ou lépirudine recommandés en "
         "postopératoire. L'aspirine ne doit jamais être utilisée seule après pontage "
         "aorto-coronarien."),
        ("En urgence", "Difficulté principale : obtenir une surveillance biologique à toute "
         "heure (nuit, jours non ouvrables). Pour la lépirudine sans monitorage ECT disponible : "
         "bolus 0,25 mg/kg + 0,20 mg/kg dans le volume d'amorçage puis perfusion continue "
         "0,15 mg/kg/h, monitorage par ACT (Hémochron) toutes les 15 min, ajusté pour ACT "
         "&gt;400 s. Après l'arrêt de la CEC : élimination par diurèse forcée (furosémide + "
         "mannitol 20 % 200 ml). Patients oligo-anuriques : hémofiltration veino-veineuse sans "
         "anticoagulant jusqu'à thrombose du filtre ; élimination du circuit de CEC/réservoir "
         "de cardiotomie par ultrafiltration (balance nulle) sur hémofiltre en polysulfone. "
         "Aprotinine associable, avec les limites connues en insuffisance rénale."),
        ("Revascularisation coronaire sans CEC", "Danaparoïde sodique utilisable (expérience "
         "clinique limitée). Protocole proposé : bolus 2250 U IV au début du prélèvement de "
         "l'artère mammaire interne, puis perfusion continue 150 U/h arrêtée 45 min avant la fin "
         "présumée de l'intervention. Surveillance par activité anti-Xa toutes les 15 min, "
         "cible thérapeutique 0,6 U anti-Xa/ml."),
    ]))
    story.append(Spacer(1, 4 * mm))

    story.append(section_bar("Sources et traçabilité", color=GREY))
    story.append(Spacer(1, 2 * mm))
    story.append(P(
        "<b>Document source :</b> Société française d'anesthésie et de réanimation, en "
        "collaboration avec le Groupe d'étude hémostase et thrombose de la Société française "
        "d'hématologie, la Société française de cardiologie et la Société de réanimation de "
        "langue française. Conférence d'experts, comité d'organisation Y. Blanloeil (Nantes). "
        "« Thrombopénie induite par l'héparine ». Ann Fr Anesth Reanim 2003;22:150-159. "
        "DOI: 10.1016/S0750-7658(02)00853-5.", S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P("<b>Méthodologie :</b> conférence d'experts (2002), sans système de grade "
                    "formel (voir disclosure méthodologique en page 1).", S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P("<b>Couverture :</b> cette fiche reprend l'intégralité du contenu clinique des "
                    "12 questions de la source (circonstances évocatrices, diagnostic biologique "
                    "et démarche pratique, diagnostic différentiel, prévention, surveillance, "
                    "traitements de substitution avec posologies complètes, contre-indications, "
                    "Tableau 1, autres traitements, stratégies par contexte clinique y compris le "
                    "détail des protocoles de chirurgie cardiaque avec/sans CEC) ainsi que le "
                    "Tableau 1 source. Comité d'organisation, groupe de lecture (listes "
                    "nominatives) et la bibliographie ne sont pas retranscrits (sans contenu "
                    "clinique actionnable).", S_SOURCE))
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Avertissement :</b> cette fiche de synthèse indépendante reprend l'intégralité du "
        "contenu clinique de la conférence d'experts SFAR 2002, mais ne remplace pas le texte "
        "intégral et n'est ni éditée ni validée par la SFAR. <b>Document ancien</b> : la "
        "lépirudine (Refludan®) n'est plus commercialisée depuis 2012 (voir avertissement en "
        "page 1) — vérifier le protocole local actualisé et les molécules effectivement "
        "disponibles (argatroban, fondaparinux, etc.) avant toute décision thérapeutique. "
        "<b>Pour une décision thérapeutique, se référer en priorité aux « Propositions du GIHP "
        "et du GFHT pour le diagnostic et la prise en charge d'une TIH » (2019)</b>, document de "
        "référence actuel également disponible dans cette bibliothèque. En cas de doute, "
        "solliciter un avis spécialisé (hémostase, hématologie).",
        S_BODY_SM), bg=GREY_LIGHT, border=GREY))
    return story


SECTIONS = [
    ("Contexte & méthodologie", _section_intro),
    ("Diagnostic clinique", _section_diagnostic_clinique),
    ("Diagnostic biologique", _section_diagnostic_bio),
    ("Diagnostic différentiel, prévention", _section_diff_prevention),
    ("Traitements de substitution", _section_traitements),
    ("Contre-indications & Tableau 1", _section_ci_tableau1),
    ("Autres traitements possibles", _section_autres_traitements),
    ("Stratégies par contexte clinique", _section_strategies_contextes),
    ("Chirurgie cardiaque (CEC) & sources", _section_cardiaque),
]

def _make_doc(path=None):
    return SimpleDocTemplate(path or OUT, pagesize=A4,
                              leftMargin=MARGIN, rightMargin=MARGIN,
                              topMargin=32 * mm, bottomMargin=16 * mm,
                              title="SFAR 2002 - Thrombopenie induite par l'heparine",
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
