# -*- coding: utf-8 -*-
"""
Fiche de synthese - RFE commune SFAR-SFMU 2020 (avec SOFCOT, SCVE, SSA)
Prise en charge des patients presentant un traumatisme severe de membre(s)
Source verifiee : sfar.org (texte valide CRC 16/06/2020, CA SFAR 25/08/2020, CA SFMU 15/09/2020)
Methodologie GRADE, tags "Grade X+/-" et "Avis d'expert(s)" imprimes litteralement apres chaque
recommandation. 19 recommandations numerotees R1 a R11 (dont 3 avis d'experts) - resume officiel
parfaitement coherent en interne (4 GRADE1 + 12 GRADE2 + 3 avis d'experts = 19, verifie item par
item) - aucune incoherence arithmetique a signaler ici. Aucun item "PAS DE RECOMMANDATION" dans ce
document (les 11 questions ont chacune abouti a au moins une recommandation). 2 tableaux sources
(criteres de Vittel, classification de Gustilo) et 1 tableau de gradation du risque, tous en texte
extractible et reproduits verbatim ; 2 figures (Figure 3 algorithme de stabilisation, Figure 4
checklist de prevention infectieuse) sont pures images (49 pages source, pages 25 et 32) et ont ete
transcrites depuis le rendu visuel de la page. Annexe 1 (codes AIS techniques, tres volumineuse et
non clinique) resumee en prose plutot que reproduite code par code - disclosure explicite en fin de
fiche. Pairs naturellement avec la fiche traumatisme_abdominal (meme trio SFAR/SFMU + SOFCOT/SCVE/
SSA, structure de RFE similaire).
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from style import *
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.units import mm

OUT = "/private/tmp/claude-501/-Users-macbook-Downloads-claude/65498e3e-5ddf-47a6-b100-3ac535d1faa0/scratchpad/rfe_sfar/output/Fiche_SFAR_Traumatisme_Membre_2020.pdf"

SOURCE_TXT = ("Source : Recommandations Formalisées d'Experts communes SFAR-SFMU, en association avec "
              "la SOFCOT, la SCVE et le SSA « Prise en charge des patients présentant un traumatisme "
              "sévère de membre(s) » (2020) — texte validé par le Comité des Référentiels Cliniques "
              "(16/06/2020), le CA SFAR (25/08/2020) et le CA SFMU (15/09/2020). Méthodologie GRADE. "
              "Fiche de synthèse non officielle : se référer au texte intégral.")

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
        ("TOPPADDING",(0,0),(-1,-1),3.4), ("BOTTOMPADDING",(0,0),(-1,-1),3.4), ("LEFTPADDING",(0,0),(-1,-1),5),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            st.append(("BACKGROUND",(0,i),(-1,i), BG_PANEL))
    t.setStyle(TableStyle(st))
    return t

def legend_flowable():
    items = [("1+", "Il faut faire"), ("1-", "Il ne faut pas faire"),
             ("2+", "Il faut probablement"), ("2-", "Il ne faut probablement pas"),
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

TOTAL_PAGES = {"n": 9}

def on_page(canvas, doc, page_title):
    header_band(canvas, doc, "SFAR / SFMU — RFE 2020 — FICHE DE SYNTHÈSE",
                "Traumatisme sévère de membre(s)",
                page_title, icon_fn=lambda c,x,y: icon_shield(c, x, y, 13*mm), color=NAVY)
    footer_band(canvas, doc, SOURCE_TXT, f"Page {doc.page} / {TOTAL_PAGES['n']}")

# ---------------------------------------------------------------------------
def _section_intro():
    story = []
    story.append(Spacer(1, 3*mm))
    story.append(info_panel(P(
        "<b>Champ :</b> prise en charge initiale, pré- et intra-hospitalière, du patient victime d'un "
        "traumatisme sévère de membre(s) (TSM). Comité de 21 experts SFAR/SFMU/SOFCOT/SCVE/SSA, "
        "méthode GRADE®, format PICO, 11 questions. Les traumatismes pelviens (RFE dédiée) sont "
        "exclus du champ.<br/><br/>"
        "<b>Définition opérationnelle du TSM</b> : traumatisme de membre(s) réunissant au moins un "
        "critère de Vittel <i>et</i> une classification AIS ≥ 3 — notamment amputation, dégantage, "
        "écrasement plus proximal que la cheville/le poignet, ischémie aiguë de membre, lésion "
        "vasculaire ischémique ou hémorragique, fractures de deux os longs proximaux (humérus/fémur), "
        "traumatisme pénétrant plus proximal que le coude/le genou.<br/><br/>"
        "<b>Résultats (résumé officiel) :</b> 19 recommandations ; 4 de niveau de preuve élevé "
        "(GRADE 1+/-), 12 de niveau de preuve faible (GRADE 2+/-), 3 avis d'experts. Accord fort "
        "obtenu pour l'ensemble après deux tours de cotation.",
        S_BODY), bg=BG_PANEL, border=TEAL))
    story.append(Spacer(1, 3*mm))

    story.append(section_bar("Légende des grades (méthodologie GRADE)"))
    story.append(Spacer(1, 2*mm))
    story.append(legend_flowable())
    story.append(Spacer(1, 4*mm))

    story.append(section_bar("Figure 1 — Critères de Vittel (un seul critère présent = traumatisé grave)"))
    story.append(Spacer(1, 2*mm))
    cw = PAGE_W - 2*MARGIN
    story.append(simple_table(
        ["Catégorie", "Critères"],
        [
            ["Examen initial du patient", "Score de Glasgow &lt; 13 • Saturation &lt; 90 % en air ambiant • "
             "Pression artérielle systolique &lt; 90 mmHg"],
            ["Circonstances de l'accident", "Victime éjectée, projetée ou écrasée • Au moins une victime "
             "décédée dans l'accident • Chute de plus de 6 mètres • Explosion ou blast"],
            ["Prise en charge préhospitalière", "Ventilation assistée • Remplissage vasculaire &gt; 1 litre • "
             "Perfusion de catécholamines"],
            ["Lésions observées ou suspectées", "Traumatisme pénétrant • Volet thoracique • Brûlure • "
             "Traumatisme du bassin • Amputation de membre • Ischémie aiguë de membre • Suspicion de "
             "lésion médullaire"],
            ["Caractéristiques du patient", "Âge &gt; 65 ans • Grossesse au 2e ou 3e trimestre • "
             "Pathologies associées (insuffisance cardiaque, respiratoire, anomalie de l'hémostase)"],
        ],
        [cw*0.26, cw*0.74]))
    story.append(Spacer(1, 4*mm))

    story.append(section_bar("Figure 2 — Classification de Gustilo des fractures ouvertes"))
    story.append(Spacer(1, 2*mm))
    story.append(simple_table(
        ["Type", "Description", "Taux d'infection"],
        [
            ["1", "Plaie &lt; 1 cm, contamination minimale", "&lt; 2 %"],
            ["2", "Plaie de 1 à 10 cm, sans lésion extensive des tissus mous", "2 à 5 %"],
            ["3.A", "Lésion tissulaire étendue &gt; 10 cm, comminution importante, couverture cutanée possible", "5 à 10 %"],
            ["3.B", "Exposition osseuse, comminution importante", "10 à 50 %"],
            ["3.C", "Lésion artérielle associée", "25 à 50 %"],
        ],
        [cw*0.12, cw*0.62, cw*0.26]))
    return story

def _section_q1_q2():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Question 1 — Orientation vers un centre spécialisé"))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("R1", "Chez les patients victimes de traumatisme sévère de membre(s), il est recommandé "
         "d'admettre en centre spécialisé de traumatologie grave les patients ayant au moins un "
         "critère de Vittel en préhospitalier.", "1+"),
    ], [14*mm, PAGE_W-2*MARGIN-14*mm-20*mm, 20*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(P("Une survie additionnelle de 3-4 patients pour 100 admis avec ISS &gt; 15 (et de "
                    "11/100 si ISS &gt; 24) a été rapportée au Royaume-Uni. Critères spécifiques "
                    "de gravité pour un membre : ≥ 2 fractures des os longs, amputation proximale "
                    "au-dessus du poignet/de la cheville, délabrement majeur (dégantage, "
                    "écrasement, ischémie aiguë).", S_NOTE))
    story.append(Spacer(1, 4*mm))

    story.append(section_bar("Question 2 — Réduire le saignement en préhospitalier"))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("R2.1", "En cas d'hémorragie active de membre et d'inefficacité de la compression directe, "
         "d'amputation, de corps étranger au sein de la plaie hémorragique, d'absence de pouls "
         "radial (critère hémodynamique) ou de multiples actions simultanées à mener, il est "
         "probablement recommandé de mettre en place un garrot.", "2+"),
        ("R2.2", "En cas de pose d'un garrot, les experts suggèrent de réévaluer, dès que possible, "
         "son efficacité, son utilité et sa localisation sur le membre, y compris lors de la phase "
         "pré-hospitalière, afin de limiter sa morbidité (temps de pose le plus court et zone "
         "d'ischémie la plus limitée possible).", "AE"),
    ], [14*mm, PAGE_W-2*MARGIN-14*mm-20*mm, 20*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(P("Efficacité du garrot pour arrêter une hémorragie active : 69-97 % selon les "
                    "modèles. Étude cas-témoins (186 vs 840 patients) : survie accrue avec garrot, "
                    "OR 5,86 [1,40-24,57]. Délai à respecter : &lt; 1 heure entre lésion artérielle "
                    "et bloc opératoire (risque d'amputation 6 % → 11,7 % au-delà, p &lt; 0,01). "
                    "Complications locales rapportées (méta-analyse 2018) : syndrome compartimental "
                    "2-18 %, infection 7-9 %, parésie nerveuse 1-6 %, TVP 9 %, amputation 12-59 % "
                    "(imputabilité difficile à établir vs. lésion initiale) ; systémiques : "
                    "rhabdomyolyse 2 %, IRA 2-3 %.", S_NOTE))
    return story

def _section_q3():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Question 3 — Dépister une lésion vasculaire (imagerie injectée)"))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("R3", "Pour ne pas méconnaître une lésion vasculaire chez un traumatisé grave de membre(s), "
         "il est probablement recommandé de réaliser en première intention un angioscanner en cas "
         "de présence d'un ou plusieurs des éléments suivants : notion de saignement extériorisé "
         "d'origine artérielle • proximité du traumatisme avec un axe vasculaire principal • "
         "présence d'un hématome non expansif • déficit neurologique isolé • Indice de pression "
         "systolique (IPS) cheville-bras &lt; 0,9.", "2+"),
    ], [14*mm, PAGE_W-2*MARGIN-14*mm-20*mm, 20*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(P("Signes « forts » (saignement extériorisé important, hématome expansif/pulsatile, "
                    "syndrome ischémique, souffle/thrill) → exploration chirurgicale immédiate ou "
                    "angioscanner/artériographie rapide si patient stabilisé. Signes « faibles » "
                    "(ci-dessus) → présence d'une lésion artérielle dans 3-25 % des cas. IPS &lt; 0,9 : "
                    "sensibilité 87 %, spécificité 97 % (série de 93 patients). Méta-analyse récente : "
                    "en l'absence de tout signe et avec IPS normal, probabilité de lésion vasculaire "
                    "virtuellement nulle (rapport de vraisemblance négatif 0,01). Angioscanner : "
                    "sensibilité/spécificité 96,2 %/99,2 % (méta-analyse, 11 études, 891 patients) — "
                    "a remplacé l'artériographie en 1re intention, celle-ci gardant sa place en 2e "
                    "intention (ex. artefacts métalliques).", S_NOTE))
    return story

def _section_q4():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Question 4 — Moment et modalités de l'ostéosynthèse"))
    story.append(Spacer(1, 2*mm))
    story.append(P("Une approche clinique globale et personnalisée est nécessaire pour chaque patient "
                    "par le biais d'une discussion multidisciplinaire fondée sur l'état clinique et "
                    "le bilan lésionnel.", S_NOTE))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("R4.1", "En l'absence d'autre lésion traumatique sévère (cérébrale, thoraco-abdomino-"
         "pelvienne ou médullaire), d'état de choc hémorragique, d'instabilité circulatoire ou "
         "respiratoire, il est recommandé de réaliser l'ostéosynthèse définitive et sûre du (des) "
         "foyer(s) de fracture des os longs dans les 24 premières heures afin de réduire l'incidence "
         "de complications locales ou systémiques associées, particulièrement pour les fractures "
         "diaphysaires fémorales et tibiales à haut risque de complications respiratoires (SDRA, "
         "embolie graisseuse).", "1+"),
        ("R4.2", "En présence d'une ou plusieurs lésions traumatiques sévères (cérébrale, "
         "thoraco-abdomino-pelvienne ou médullaire) ou d'un état de choc hémorragique, d'une "
         "instabilité circulatoire ou d'une atteinte respiratoire sévère, il est probablement "
         "recommandé de retarder l'ostéosynthèse définitive au profit d'une stabilisation "
         "temporaire (fixateur externe ou traction selon les délais envisagés) pour réduire la "
         "survenue de complications systémiques induites par l'agression chirurgicale, les pertes "
         "sanguines péri-opératoires, la coagulopathie, ainsi que le risque d'embolie graisseuse. "
         "L'ostéosynthèse définitive et sûre devra être réalisée le plus précocement possible par "
         "la suite.", "2+"),
    ], [14*mm, PAGE_W-2*MARGIN-14*mm-20*mm, 20*mm]))
    story.append(Spacer(1, 3*mm))
    story.append(P("Concepts clés : « stabilisation précoce appropriée » (Early appropriate care) et "
                    "« chirurgie séquentielle avec stabilisation temporaire » (Damage control "
                    "orthopaedic surgery). Une stabilisation par fixateur externe est associée à une "
                    "réduction de 15 % du risque de SDRA vs. traction, pour les fractures "
                    "diaphysaires fémorales — à privilégier si la chirurgie définitive n'est pas "
                    "envisagée dans un délai de 24 à 36 heures.", S_NOTE))
    story.append(Spacer(1, 4*mm))

    story.append(section_bar("Tableau 1 — Gradation du risque de complications secondaires"))
    story.append(Spacer(1, 2*mm))
    cw = PAGE_W - 2*MARGIN
    cols = [cw*0.16, cw*0.28, cw*0.28, cw*0.28]
    story.append(simple_table(
        ["", "Risque faible", "Risque intermédiaire", "Risque élevé"],
        [
            ["Statut circulatoire", "Stable (pas de noradrénaline ou débit &lt; 2 mg/h, pas de "
             "transfusion, lactate &lt; 2,5 mmol/L)", "Choc modéré (noradrénaline 2-4 mg/h, "
             "transfusion 1-4 CGR, lactate 2,5-4 mmol/L)", "Choc profond (noradrénaline &gt; 4 mg/h, "
             "transfusion ≥ 5 CGR, lactate &gt; 4 mmol/L)"],
            ["Coagulation", "TQr &lt; 1,2, fibrinogène ≥ 1,5 g/L, plaquettes ≥ 100 G/L", "TQr 1,2-1,5, "
             "fibrinogène 1-1,5 g/L, plaquettes 50-100 G/L", "TQr &gt; 1,5, fibrinogène &lt; 1 g/L, "
             "plaquettes &lt; 50 G/L"],
            ["Respiratoire / thermique", "PaO2/FiO2 &gt; 300, hypothermie &gt; 35°C", "PaO2/FiO2 "
             "&lt; 300, hypothermie 32-35°C, rhabdomyolyse massive (myoglobine ≥ 10 000 UI/L)",
             "PaO2/FiO2 &lt; 150, hypothermie &lt; 32°C, rhabdomyolyse massive (myoglobine "
             "≥ 20 000 UI/L)"],
            ["Orientation (Fig. 3)", "Chirurgie définitive sûre précoce", "Réanimation appropriée, "
             "réévaluations répétées dans les 24h", "Chirurgie définitive sûre retardée + "
             "stabilisation temporaire (si diaphyse de membre inférieur)"],
        ],
        cols))
    story.append(Spacer(1, 2*mm))
    story.append(P("<i>Figure 3 (algorithme visuel, page 25 de la source, transcrit ci-dessus sous "
                    "forme de tableau) : évaluation individualisée (terrain, statut physiologique, "
                    "profil lésionnel/local) → gradation du risque (tableau ci-dessus) → orientation "
                    "vers la stratégie appropriée. En cas de stabilisation temporaire, réévaluation "
                    "quotidienne (état circulatoire, coagulation, respiratoire, état local) : "
                    "poursuite vers l'ostéosynthèse définitive retardée si les critères sont "
                    "favorables, sinon non-réintervention et rééducation.</i>", S_NOTE))
    return story

def _section_q5():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Question 5 — Sauvetage de membre ou amputation"))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("R5.1", "En cas de stabilité hémodynamique, il est probablement recommandé de procéder à "
         "un sauvetage du membre.", "2+"),
        ("R5.2", "En cas de choc hémorragique associé à un traumatisme grave de membre(s), il est "
         "probablement recommandé d'appliquer une stratégie de damage control. Aucun critère de "
         "gravité considéré isolément n'impose le recours à une amputation.", "2+"),
    ], [14*mm, PAGE_W-2*MARGIN-14*mm-20*mm, 20*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(P("Résultats fonctionnels équivalents possibles entre sauvetage et amputation "
                    "(la décision doit se fonder sur l'état du membre, les comorbidités, les "
                    "préférences du patient et le savoir-faire du chirurgien) — le sauvetage "
                    "nécessite souvent plusieurs interventions et plus de réhospitalisations, "
                    "l'amputation offre une réadaptation plus courte mais un vécu psychologique "
                    "parfois moins bon. Score MESS &gt; 7 et score MESI &gt; 20 largement cités "
                    "comme seuils d'amputation initiale, mais le MESS n'est <b>pas</b> un facteur de "
                    "risque indépendant en analyse multivariée et ne doit pas être considéré "
                    "isolément. Ischémie froide &gt; 6h : échec de réimplantation 87 % vs 61 % en "
                    "deçà — à considérer comme un critère relatif, pas un marqueur prédictif "
                    "indépendant. Situations favorisant une amputation initiale en contexte "
                    "hémorragique : amputation traumatique complète, perte de substance rendant "
                    "impossible tout recouvrement cutané, section avérée du nerf tibial, fractures "
                    "multiples avec perte osseuse ou lésions vasculaires ischémiques.", S_NOTE))
    return story

def _section_q6():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Question 6 — Prévention du risque septique"))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("R6.1", "Il est probablement recommandé d'administrer une antibioprophylaxie en cas de "
         "traumatisme sévère avec fracture ouverte de membres le plus rapidement possible et pour "
         "une durée maximale de 48 à 72 heures (à l'exception d'une infection avérée).", "2+"),
        ("R6.2", "Il ne faut probablement pas réaliser de prélèvements microbiologiques "
         "systématiques au bloc opératoire lors d'un traumatisme sévère avec fracture ouverte de "
         "membres.", "2-"),
    ], [14*mm, PAGE_W-2*MARGIN-14*mm-20*mm, 20*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(P("Taux d'infection : ~1 % après traumatisme fermé, 6-44 % après fracture ouverte "
                    "selon le type/terrain/définition retenue. Type de molécule selon la "
                    "classification de Gustilo (Figure 2) et l'écologie locale. Prélèvements "
                    "préopératoires non contributifs dans 47 % des cas (étude rétrospective, "
                    "245 patients) ; pathogène responsable retrouvé dans seulement 0-56 % des "
                    "prélèvements peropératoires selon l'étude. Infections fongiques invasives : "
                    "rares mais mortalité 7,8 % — prélèvement mycologique ciblé possible en cas de "
                    "nécrose cutanée étendue/persistante ou de moisissures visibles sur la plaie "
                    "(pas de dépistage systématique en population civile, faute de données).", S_NOTE))
    story.append(Spacer(1, 3*mm))
    story.append(info_panel(P(
        "<b>Figure 4 — Mesures de prévention du risque infectieux</b> (transcrite depuis l'affiche "
        "de la source, page 32, pure image, vérifiée visuellement) — à réaliser le plus tôt possible : "
        "<b>1.</b> Antibioprophylaxie systématique active sur les cocci Gram positifs et les "
        "anaérobies (amoxicilline + acide clavulanique ou céphalosporines — RFE SFAR 2018 ; si "
        "allergie : clindamycine ± gentamicine). <b>2.</b> Lavage abondant de la plaie. "
        "<b>3.</b> Emballage dans un pansement stérile humide. <b>4.</b> Immobilisation de la "
        "fracture. <b>5.</b> Vérification du statut antitétanique par test immunochromatographique "
        "et SAT/VAT selon HAS 2013. <b>6.</b> Prise en charge chirurgicale : irrigation, débridement "
        "± parage, stabilisation de la fracture, recherche de lésions associées vasculo-nerveuses, "
        "couverture cutanée.",
        S_BODY_SM), bg=BG_PANEL, border=TEAL))
    return story

def _section_q7_q8():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Question 7 — Prévention de la maladie thromboembolique veineuse"))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("R7.1", "Chez les patients victimes de traumatisme sévère de membre(s) inférieur(s), il est "
         "recommandé d'instaurer une thromboprophylaxie médicamenteuse précoce par héparine de bas "
         "poids moléculaire (HBPM), après contrôle de l'hémorragie et de l'hémostase, dont le délai "
         "d'instauration sera modulé par le bilan lésionnel.", "1+"),
        ("R7.2", "Il n'est pas recommandé de mettre en place un filtre cave chez des patients à "
         "risque thrombo-embolique majeur en dehors d'une contre-indication au traitement "
         "pharmacologique et mécanique (par compression veineuse intermittente).", "1-"),
    ], [14*mm, PAGE_W-2*MARGIN-14*mm-20*mm, 20*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(P("Risque thromboembolique selon la zone : élevé pour fémur/plateau tibial, modéré "
                    "pour tibia/cheville/pied/rupture du tendon d'Achille/immobilisation plâtrée. "
                    "HBPM = traitement de référence depuis &gt; 20 ans ; instauration dans les 36 "
                    "premières heures jugée sûre y compris avec lésion d'organe solide ou "
                    "traumatisme crânien, sans majoration significative du saignement. Filtre cave "
                    "optionnel envisageable si contre-indication formelle, avec retrait prévu "
                    "d'emblée à distance (2+) — méta-analyse : pas de différence de mortalité, "
                    "1 embolie pulmonaire évitée pour 109/962 patients avec filtre.", S_NOTE))
    story.append(Spacer(1, 4*mm))

    story.append(section_bar("Question 8 — Syndrome des loges"))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("R8", "Chez le patient traumatisé sévère de membre(s), les experts suggèrent d'effectuer "
         "une fasciotomie précoce en cas de syndrome de loge récemment constitué pour réduire "
         "l'incidence des répercussions fonctionnelles.", "AE"),
    ], [14*mm, PAGE_W-2*MARGIN-14*mm-20*mm, 20*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(info_panel(P(
        "<b>Recherche répétée (toutes les 30 min à 2h) pendant les 24 premières heures</b> chez le "
        "patient à risque (fracture, écrasement, lésion hémorragique/reperfusion, hypotension) : "
        "les « 4P » — <i>pain</i> (douleur spontanée ou à la mise sous tension), <i>paresthesia</i>, "
        "<i>paresis</i> — sont des signes précoces à haute valeur prédictive négative mais faible "
        "sensibilité. <i>Pulselessness</i> et <i>pallor</i> (pâleur, abolition du pouls) sont des "
        "signes tardifs traduisant un caractère déjà souvent irréversible — leur absence ne rassure "
        "pas. Pression intracompartimentale ≥ 30 mmHg ou pression différentielle (PA diastolique − "
        "pression intracompartimentale) &lt; 30 mmHg : utiles au dépistage. Traitement : fasciotomie "
        "précoce, incision large peau/tissu sous-cutané/fascia, ouverture de toutes les loges du "
        "segment.",
        S_BODY), bg=RED_LIGHT, border=RED))
    return story

def _section_q9_q10():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Question 9 — Rhabdomyolyse aiguë post-traumatique"))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("R9.1", "Pour détecter le risque de survenue d'une insuffisance rénale aiguë chez le "
         "patient atteint de rhabdomyolyse aiguë post-traumatique après traumatisme de membre(s), "
         "il est probablement recommandé de réaliser : un bilan biologique répété associant un "
         "dosage plasmatique de la myoglobine, de la créatine phosphokinase (CPK) et de la "
         "kaliémie ; un sondage urinaire permettant de monitorer la diurèse horaire et le pH "
         "urinaire (objectif ≥ 6,5).", "2+"),
        ("R9.2", "Concernant les mesures de prévention de l'insuffisance rénale aiguë chez le "
         "patient atteint de rhabdomyolyse aiguë post-traumatique après traumatisme de membre, les "
         "préconisations sont celles des recommandations formalisées d'experts SFAR-SRLF de 2016 "
         "« insuffisance rénale aiguë en péri-opératoire et en réanimation ».", "2+"),
    ], [14*mm, PAGE_W-2*MARGIN-14*mm-20*mm, 20*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(P("CPK &gt; 5× la normale (~1000 UI/L) signe la rhabdomyolyse ; CPK &gt; 75 000 UI/L "
                    "associé à &gt; 80 % de défaillance rénale (cohorte crush syndrome, séisme). "
                    "Myoglobine : pic plasmatique plus précoce, potentiellement plus sensible/"
                    "spécifique que les CPK pour le risque rénal. Remplissage par cristalloïdes "
                    "balancés : &gt; 6 L/j si rhabdomyolyse sévère (CPK &gt; 15 000 UI/L), 3-6 L/j si "
                    "modérée (étude rétrospective post-séisme, 638 patients) — le délai "
                    "d'instauration du remplissage est associé au risque de survenue d'une IRA.", S_NOTE))
    story.append(Spacer(1, 4*mm))

    story.append(section_bar("Question 10 — Embolie graisseuse et atteintes inflammatoires systémiques"))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("R10.1", "Il est probablement recommandé de réaliser un traitement chirurgical d'une "
         "fracture de la diaphyse des os longs dans les 24 premières heures post-traumatiques pour "
         "limiter les complications respiratoires à type de SDRA ou d'embolie graisseuse.", "2+"),
        ("R10.2", "Il est probablement recommandé de réaliser en première intention une "
         "ostéosynthèse définitive des fractures diaphysaires d'os longs pour prévenir le risque de "
         "SDRA et d'embolie graisseuse. Chez les patients hémodynamiquement instables ou présentant "
         "une atteinte respiratoire sévère en préopératoire, la balance bénéfice-risque entre une "
         "ostéosynthèse définitive ou la pose d'un fixateur externe doit faire l'objet d'une "
         "discussion multidisciplinaire.", "2+"),
        ("R10.3", "Il est probablement recommandé de ne pas administrer de corticoïdes pour "
         "prévenir l'embolie graisseuse en cas de fracture diaphysaire des os longs.", "2-"),
    ], [14*mm, PAGE_W-2*MARGIN-14*mm-20*mm, 20*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(P("Recommandations centrées sur les fractures de diaphyse fémorale (données de la "
                    "littérature). Chirurgie dans les 10 premières heures associée à un risque "
                    "moindre d'embolie graisseuse dans une étude. Étude « borderline » (42/165 "
                    "patients) : OR d'ALI 6,69 [1,01-44,08] dans le groupe enclouage précoce, à "
                    "mettre en balance avec une durée de ventilation plus courte chez les patients "
                    "stables traités par ostéosynthèse définitive. Corticoïdes : méta-analyse "
                    "ancienne (7 études dont 6 réalisées entre 1977 et 1987, 430 patients, délai "
                    "opératoire &gt; 5 jours, "
                    "fortes doses 6-30 mg/kg de méthylprednisolone) montrait un effet protecteur "
                    "(RR 0,22) mais validité externe faible et effets délétères démontrés par "
                    "ailleurs (traumatisme crânien, blessés médullaires) — non recommandé en "
                    "pratique actuelle avec prise en charge chirurgicale précoce.", S_NOTE))
    return story

def _section_q11_synthese():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Question 11 — Contrôle de la douleur aiguë"))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("R11", "Les experts suggèrent qu'en cas de traumatisme sévère de membre(s) l'utilisation "
         "d'une stratégie d'analgésie multimodale soit favorisée et que le rapport bénéfice/risque "
         "des molécules choisies soit évalué à l'aune de la volémie et de l'atteinte musculaire.", "AE"),
    ], [14*mm, PAGE_W-2*MARGIN-14*mm-20*mm, 20*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(P("Renvoi aux RFE SFMU (sédation-analgésie en structure d'urgence) et SFAR "
                    "(douleur postopératoire). Titration IV de morphine = technique de référence "
                    "(efficace dans 82 % des cas), sans dose de charge préalable nécessaire. "
                    "Kétamine 0,15-0,3 mg/kg en association à la morphine titrée : améliore "
                    "l'analgésie et réduit les doses de morphine. MEOPA efficace sans effet "
                    "indésirable majeur si contre-indications respectées. Sufentanil intranasal "
                    "efficace (matériel adapté requis, taux non négligeable d'effets indésirables). "
                    "ALR : bloc fémoral (ilio-fascial ou voie directe avec repérage nerveux) "
                    "réalisable en préhospitalier ; blocs plus complexes évalués au cas par cas en "
                    "intrahospitalier.", S_NOTE))
    story.append(Spacer(1, 5*mm))

    story.append(section_bar("Synthèse et messages clés"))
    story.append(Spacer(1, 2*mm))
    story.append(P(
        "• Admission en centre spécialisé dès qu'un seul critère de Vittel est présent.<br/>"
        "• Garrot en 1re intention si hémorragie active de membre non contrôlée par compression, "
        "avec réévaluation itérative de son efficacité/utilité/localisation.<br/>"
        "• Angioscanner en 1re intention devant tout signe (fort ou faible) de lésion vasculaire, "
        "ou IPS cheville-bras &lt; 0,9.<br/>"
        "• Ostéosynthèse définitive et sûre dans les 24h si le patient est stable ; stabilisation "
        "temporaire (damage control orthopaedic surgery) puis ostéosynthèse différée si lésions "
        "sévères associées ou instabilité — orientation guidée par la gradation du risque "
        "(Tableau 1/Figure 3).<br/>"
        "• Aucun critère de gravité isolé n'impose une amputation d'emblée — décision "
        "multidisciplinaire fondée sur l'ensemble du tableau clinique.<br/>"
        "• Antibioprophylaxie précoce (48-72h max) en cas de fracture ouverte ; pas de "
        "prélèvements microbiologiques systématiques.<br/>"
        "• Thromboprophylaxie par HBPM précoce ; pas de filtre cave hors contre-indication "
        "formelle.<br/>"
        "• Recherche répétée des « 4P » (pain, paresthesia, paresis + douleur à l'étirement passif) "
        "pour le syndrome des loges — pâleur et abolition du pouls sont des signes tardifs.<br/>"
        "• Bilan biologique répété (myoglobine, CPK, kaliémie) et diurèse alcaline en cas de "
        "rhabdomyolyse ; pas de corticoïdes pour prévenir l'embolie graisseuse.<br/>"
        "• Analgésie multimodale, titration morphinique sans dose de charge, kétamine à faible "
        "dose en adjuvant.",
        S_BODY))
    story.append(Spacer(1, 5*mm))

    story.append(section_bar("Sources et traçabilité", color=GREY))
    story.append(Spacer(1, 2*mm))
    story.append(P(
        "<b>Document source :</b> « Prise en charge des patients présentant un traumatisme sévère "
        "de membre(s) » — Recommandations Formalisées d'Experts communes SFAR-SFMU, en association "
        "avec la SOFCOT, la SCVE et le SSA. Comité de 21 experts, coordination J. Pottecher (SFAR), "
        "H. Lefort (SFMU). Texte validé par le Comité des Référentiels Cliniques le 16/06/2020, le "
        "CA SFAR le 25/08/2020 et le CA SFMU le 15/09/2020.", S_SOURCE))
    story.append(Spacer(1, 1.5*mm))
    story.append(P("<b>Méthodologie :</b> GRADE®, tags « Grade 1+/1-/2+/2- (Accord FORT) » et "
                    "« Avis d'expert(s) (Accord FORT) » imprimés littéralement après chaque "
                    "recommandation — cités ici tels quels.", S_SOURCE))
    story.append(Spacer(1, 1.5*mm))
    story.append(P("<b>Couverture :</b> 19 recommandations (R1 à R11, dont 3 avis d'experts) "
                    "reproduites intégralement, ainsi que les Figures 1 et 2 (critères de Vittel, "
                    "classification de Gustilo) et le Tableau 1 de gradation du risque. La Figure 3 "
                    "(algorithme d'orientation) et la Figure 4 (checklist de prévention infectieuse), "
                    "pages 25 et 32 de la source — pures images, sans texte extractible — ont été "
                    "vérifiées visuellement et retranscrites sous forme de tableau/liste structurés. "
                    "L'Annexe 1 (codes techniques AIS détaillés par lésion, plusieurs centaines "
                    "d'entrées) n'est <b>pas</b> reproduite ici : son contenu clinique essentiel — "
                    "seuil AIS ≥ 3 et catégories de lésions définissant un TSM — est intégré dans le "
                    "panneau d'introduction ; pour le codage AIS détaillé, se référer au texte "
                    "intégral.", S_SOURCE))
    story.append(Spacer(1, 3*mm))
    story.append(info_panel(P(
        "<b>Avertissement :</b> ce document est une fiche de synthèse indépendante, produite pour un "
        "usage d'aide-mémoire. Il reprend l'intégralité des recommandations de la RFE mais ne "
        "remplace pas le texte intégral et n'est ni édité ni validé par la SFAR/SFMU. En cas de "
        "doute, se référer au texte intégral, aux recommandations ultérieures et/ou à un avis "
        "spécialisé.",
        S_BODY_SM), bg=GREY_LIGHT, border=GREY))
    return story

SECTIONS = [
    ("Introduction, méthodologie & critères de gravité", _section_intro),
    ("Q1-Q2 — Orientation & contrôle du saignement", _section_q1_q2),
    ("Q3 — Dépistage d'une lésion vasculaire", _section_q3),
    ("Q4 — Moment et modalités de l'ostéosynthèse", _section_q4),
    ("Q5 — Sauvetage de membre ou amputation", _section_q5),
    ("Q6 — Prévention du risque septique", _section_q6),
    ("Q7-Q8 — Thromboprophylaxie & syndrome des loges", _section_q7_q8),
    ("Q9-Q10 — Rhabdomyolyse & embolie graisseuse", _section_q9_q10),
    ("Q11, synthèse, sources & traçabilité", _section_q11_synthese),
]

def _make_doc():
    return SimpleDocTemplate(OUT, pagesize=A4,
                              leftMargin=MARGIN, rightMargin=MARGIN,
                              topMargin=32*mm, bottomMargin=16*mm,
                              title="Fiche SFAR-SFMU 2020 - Traumatisme severe de membre(s)",
                              author="Synthèse indépendante (source SFAR/SFMU)")

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
