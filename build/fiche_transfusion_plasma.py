# -*- coding: utf-8 -*-
"""
Fiche de synthese - Recommandations ANSM/HAS (juin 2012) "Transfusion de plasma
therapeutique : produits, indications - Actualisation 2012". Source :
sources/transfusion_plasma.pdf (15 pages), sources/transfusion_plasma.txt
(texte extrait, 1026 lignes, incluant les sauts de page). Pas de tampon
d'obsolescence detecte a la lecture integrale (page de titre + sommaire, pas
d'avis de retrait) ; library_final.json marque ce document "en vigueur".
NOTE library : le champ exact_date de library_final.json indique a tort
"2014" alors que le document lui-meme (page de titre et pied de page de
chaque page : "ANSM-HAS-Juin 2012") est date de juin 2012 - disclosure
conservee, non corrigee silencieusement.

METHODOLOGIE - GRADE HAS (A/B/C) + "accord professionnel", PAS GRADE 1+/2+ :
methodologie HAS/ANAES classique (Grade A = preuve scientifique etablie,
Grade B = presomption scientifique, Grade C = faible niveau de preuve ;
"accord professionnel" = absence de preuve, avis du groupe de travail).
VERIFIE PAR GREP EXHAUSTIF (grep -no 'grade [ABC]|accord professionnel' sur le
texte source, insensible a une coquille OCR "arade B" pour "grade B" a la
ligne 860) : un grep ligne-a-ligne naif ne trouve que 30 occurrences, mais 3
tags supplementaires enjambent un saut de ligne dans le texte extrait (1
Grade B pres de "immunomodulateurs", lignes 870-871 ; 2 accord professionnel
lignes 667-668 et 826-827) et ont ete retrouves par lecture manuelle. Total
reel retranscrit dans les tableaux de cette fiche : 33 enonces gradees -
6x Grade B, 11x Grade C, 16x accord professionnel (+ 7 enonces sans tag
explicite, retranscrits "—", voir plus bas). AUCUN Grade A trouve nulle part
dans le document
(disclosure : le corpus ne comporte que des preuves de niveau B/C ou un
consensus d'experts, jamais de preuve de niveau A, pour la transfusion de
plasma). Plusieurs enonces cliniquement importants (ex. definition du risque
hemorragique >1,5 pour le ratio Quick, regles ABO, listes de non-indications
pediatriques) sont formules par le texte source sans aucun tag de grade/accord
explicite a cote de la phrase elle-meme : retranscrits avec un tiret "—" dans
la colonne Accord plutot que de leur attribuer arbitrairement un grade non
present dans la source.

PERIMETRE - 3 parties : (1) les 4 plasmas therapeutiques disponibles
(PFC-SD, PFC-IA, PFC-Se, PLYO) + plasma autologue + transformations + effets
indesirables + contre-indications + compatibilite ABO + tests biologiques
(fond documentaire, non gradee) ; (2) indications du plasma homologue en
chirurgie/traumatologie/obstetrique et en medecine (CIVD, deficits en
proteines, micro-angiopathies thrombotiques, echanges plasmatiques, OAH),
pediatrie/neonatologie, antidote AVK (30 enonces gradees) ; (3) indications
du plasma autologue. Couverture complete verifiee par relecture integrale du
texte extrait (1026 lignes) section par section.

DISCLOSURE - une seule contre-indication ABSOLUE existe dans tout le document
(anticorps anti-IgA chez un sujet deficitaire en IgA) : signale explicitement
comme telle pour eviter toute confusion avec les nombreuses "precautions
d'emploi" (non des contre-indications) enumerees par type de plasma.

CONVENTION DE CHIP : extension locale non invasive de GRADE_COLORS - "B" ->
teal (presomption scientifique), "C" -> amber (faible niveau de preuve), "AP"
-> gris (accord professionnel, pas de preuve), "—" -> gris clair neutre
(enonce non tagge par la source). Aucune fiche precedente n'utilise ce
schema HAS A/B/C + accord professionnel (a la difference du GRADE 1+/2+ ou
du schema RAND/UCLA "accord fort/faible" a un seul axe deja vus ailleurs
dans ce corpus) : premiere fiche de la serie a le retranscrire.

ICONE : icon_drop (goutte de sang/plasma), deja utilisee pour les fiches
d'hemostase/fluides.

_count_pages() : implementation copiee du pattern fiche_aap_programmee.py /
fiche_transport_intrahospitalier.py, utilisant PyMuPDF (fitz) plutot que
pypdf (cet environnement a un pypdf casse : import cryptography -> panic
pyo3, cf. fiche_transport_intrahospitalier.py). Passes de comptage vers un
tempfile.mktemp() jetable, jamais vers OUT.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from style import *
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.units import mm

GRADE_COLORS["B"] = (TEAL, WHITE)
GRADE_COLORS["C"] = (AMBER, WHITE)
GRADE_COLORS["AP"] = (GREY, WHITE)
GRADE_COLORS["—"] = (GREY_LIGHT, INK)

OUT = "/home/user/rfe-sfar-website/output/Fiche_ANSM_HAS_Transfusion_Plasma_Therapeutique_2012.pdf"

SOURCE_TXT = ("Source : ANSM / HAS — « Transfusion de plasma thérapeutique : produits, indications "
              "— Actualisation 2012 » (juin 2012). Fiche de synthèse non officielle : se référer au "
              "texte intégral.")

def P(txt, style=S_CELL):
    return Paragraph(txt, style)

def chip(label, **kw):
    return grade_chip(label, **kw)

REF_W = 0
ACCORD_W = 20 * mm

def prop_table(rows, col_widths=None):
    """rows: (text, grade_label) - grade_label parmi 'B', 'C', 'AP', '—'."""
    text_w = PAGE_W - 2 * MARGIN - ACCORD_W
    cw = col_widths or [text_w, ACCORD_W]
    data = [[P("Recommandation (texte condensé, fidèle à la source)", S_HEAD_W), P("Niveau", S_HEAD_W_C)]]
    for txt, grade in rows:
        data.append([P(txt, S_CELL), chip(grade, width=ACCORD_W - 2 * mm)])
    t = Table(data, colWidths=cw, repeatRows=1)
    style_cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), NAVY), ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTNAME", (0, 0), (-1, 0), FONT_BOLD), ("FONTSIZE", (0, 0), (-1, 0), 8),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("ALIGN", (1, 0), (1, -1), "CENTER"),
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
    data = [[P(h, S_HEAD_W) for h in header]] + [[P(c, S_CELL) for c in row] for row in rows]
    t = Table(data, colWidths=col_widths, repeatRows=1)
    style_cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), NAVY), ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTNAME", (0, 0), (-1, 0), FONT_BOLD), ("FONTSIZE", (0, 0), (-1, 0), 8),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("GRID", (0, 0), (-1, -1), 0.5, GREY_LIGHT),
        ("TOPPADDING", (0, 0), (-1, -1), 3.2), ("BOTTOMPADDING", (0, 0), (-1, -1), 3.2),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            style_cmds.append(("BACKGROUND", (0, i), (-1, i), BG_PANEL))
    t.setStyle(TableStyle(style_cmds))
    return t

TOTAL_PAGES = {"n": 7}

def on_page(canvas, doc, page_title):
    header_band(canvas, doc, "ANSM / HAS — ACTUALISATION 2012 — FICHE DE SYNTHÈSE",
                "Transfusion de plasma thérapeutique",
                page_title, icon_fn=lambda c, x, y: icon_drop(c, x, y, 13 * mm), color=NAVY)
    footer_band(canvas, doc, SOURCE_TXT, f"Page {doc.page} / {TOTAL_PAGES['n']}")

# ---------------------------------------------------------------------------
def _section_intro():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Champ :</b> produits, caractéristiques et indications de la transfusion de plasma "
        "thérapeutique homologue et autologue, chez l'adulte, le nouveau-né et l'enfant. "
        "Actualisation des recommandations de 2002 par l'ANSM et la HAS (juin 2012), suite à "
        "l'abrogation de l'arrêté du 3 décembre 1991 : ces recommandations constituent depuis le "
        "13 juillet 2011 l'unique référence officielle pour la prescription du plasma en France.",
        S_BODY), bg=BG_PANEL, border=TEAL))
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Méthodologie — grades HAS/ANAES (A/B/C) + « accord professionnel », à la différence "
        "du GRADE (1+/2+) utilisé ailleurs dans ce corpus :</b> Grade A = preuve scientifique "
        "établie ; Grade B = présomption scientifique ; Grade C = faible niveau de preuve ; "
        "<b>« accord professionnel »</b> = absence de preuve, avis du groupe de travail après "
        "consultation de groupes de lecture. <b>Vérifié exhaustivement : 33 énoncés tagués "
        "dans le document — 6 Grade B, 11 Grade C, 16 accord professionnel, AUCUN Grade A.</b> "
        "Plusieurs énoncés cliniquement importants ne portent aucun tag explicite dans la source : "
        "reproduits avec « — » dans la colonne Niveau plutôt que de leur attribuer un grade non "
        "présent dans le texte source.", S_BODY_SM), bg=BG_PANEL, border=TEAL))
    story.append(Spacer(1, 3 * mm))

    story.append(section_bar("En bref — indications et non-indications (synthèse de la source)"))
    story.append(Spacer(1, 2 * mm))
    story.append(P("<b>Indiqué :</b> hémorragie modérée/peu évolutive/contrôlée guidée par les "
                    "tests de laboratoire (ratio Quick patient/témoin &gt; 1,5) ; choc "
                    "hémorragique et transfusion massive (ratio PFC:CGR 1:2 à 1:1) ; "
                    "neurochirurgie sans transfusion massive (TP &lt; 50 % en traumatisé crânien "
                    "grave, &lt; 60 % pour pose de capteur de PIC) ; chirurgie cardiaque avec "
                    "saignement microvasculaire persistant et déficit en facteurs (TP ≤ 40 % ou "
                    "TCA &gt; 1,8/témoin) ; CIVD obstétricale non contrôlée par le traitement "
                    "étiologique ; CIVD avec effondrement des facteurs (TP &lt; 35-40 %) et "
                    "hémorragie active/potentielle ; micro-angiopathie thrombotique (PTT, SHU "
                    "grave) ; nouveau-né/enfant : indications similaires à l'adulte, et grand "
                    "prématuré &lt; 29 SA en détresse vitale si facteurs &lt; 20 % même sans "
                    "syndrome hémorragique ; surdosage grave en AVK, seulement en l'absence de "
                    "CCP disponible (ou de CCP sans héparine si antécédent de TIH).", S_BODY_SM))
    story.append(Spacer(1, 2 * mm))
    story.append(P("<b>Non indiqué :</b> prophylaxie du saignement (altération mineure/modérée "
                    "de l'hémostase) ; soluté de remplissage (brûlé compris) ; chirurgie cardiaque "
                    "sans saignement ; insuffisance hépatocellulaire chronique ou insuffisance "
                    "hépatique aiguë sévère sans saignement, dans le seul but de corriger "
                    "l'hémostase ; poussées aiguës d'œdème angioneurotique héréditaire ; "
                    "hémorragie sous anticoagulants oraux directs (aucune donnée clinique) ; chez "
                    "l'enfant : SHU typique post-diarrhéique (STEC+), infection néonatale sans "
                    "CIVD, hypovolémie sans trouble de l'hémostase, prévention des hémorragies "
                    "intraventriculaires du prématuré sans coagulopathie, nouveau-né sain avant "
                    "chirurgie.", S_BODY_SM))
    return story

def _section_types_plasma():
    story = []
    story.append(Spacer(1, 2 * mm))
    story.append(section_bar("Les 4 plasmas thérapeutiques homologues disponibles"))
    story.append(Spacer(1, 2 * mm))
    story.append(P("Aucun argument ni aucune étude ne démontre la supériorité d'une préparation "
                    "par rapport à une autre en termes d'efficacité (<b>Grade B</b>) ni de "
                    "sécurité transfusionnelle (aucune étude comparative disponible).", S_BODY_SM))
    story.append(Spacer(1, 2 * mm))
    cw = PAGE_W - 2 * MARGIN
    story.append(simple_table(
        ["Plasma", "Préparation", "Volume/unité", "Conservation"],
        [
            ["PFC-SD", "Viro-atténué par solvant-détergent (TnBP + Triton X100), mélange de "
             "plasmas d'aphérèse de 100 donneurs de même groupe ABO", "200 mL",
             "≤ -25 °C, 1 an après préparation"],
            ["PFC-IA", "Plasma unitaire déleucocyté traité par amotosalen + UVA, congelé dans "
             "les 8h suivant le prélèvement", "200-300 mL", "≤ -25 °C, 1 an après prélèvement"],
            ["PFC-Se", "Sécurisé par quarantaine (min. 60 jours), congelé dans les 24h suivant "
             "le prélèvement, sans traitement physico-chimique", "200-850 mL",
             "≤ -25 °C, 1 an après prélèvement"],
            ["PLYO", "Lyophilisé à partir de PFC-IA, 10 donneurs max (A/B/AB), usage militaire "
             "principalement (OPEX)", "Reconstitué avec 200 mL d'eau PPI → 210 mL",
             "+2 à +25 °C à l'abri de la lumière, 2 ans après lyophilisation"],
        ],
        [cw * 0.12, cw * 0.48, cw * 0.20, cw * 0.20]))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P("Décongélation au bain-marie +37 °C ± 2 (ou méthode approuvée ANSM) : "
                    "≤ 30 min pour un volume &lt; 400 mL, ≤ 40 min pour 400-600 mL, ≤ 50 min "
                    "pour ≥ 600 mL. Après décongélation, vérification visuelle systématique de "
                    "chaque unité (élimination des poches défectueuses ou d'aspect suspect) ; "
                    "transfusion au plus tard <b>6 heures</b> après décongélation/reconstitution "
                    "— la recongélation est interdite. Norme française facteur VIII : "
                    "≥ 0,7 UI/mL (PFC-Se), ≥ 0,5 UI/mL (PFC-IA, PFC-SD, PLYO) ; PFC-IA : "
                    "≥ 2 g/L de fibrinogène après décongélation.", S_NOTE))
    story.append(Spacer(1, 2 * mm))
    story.append(P("<b>Transformations</b> — « préparation pédiatrique » : unités pédiatriques "
                    "d'au moins 50 mL préparées avant congélation à partir d'un PFC homologue. "
                    "« Sang reconstitué à usage pédiatrique » : mélange d'un CGR et d'un PFC "
                    "homologue décongelé (volume adapté à l'hématocrite visé, ou albumine à la "
                    "place du PFC), produit périmé à 6h. « Mélange de plasmas sécurisés » : "
                    "jusqu'à 12 unités homologues de même groupe ABO et même type de "
                    "sécurisation, mélangées après décongélation.", S_BODY_SM))
    story.append(Spacer(1, 2 * mm))
    story.append(P("<b>Plasma autologue</b> (destiné au même sujet) : utilisable sans "
                    "sécurisation virale, déleucocytation non systématique. Volume minimal "
                    "120 mL (unité adulte) ou 50 mL (unité enfant) pour le PFC autologue issu de "
                    "sang total. Conservation congelée jusqu'à péremption des CGR prélevés chez "
                    "le même patient (42 jours, extensible à 1 an sur protocole), ou 72h entre "
                    "+2 et +6 °C ; utilisation recommandée en moins de 6h après décongélation.",
                    S_BODY_SM))
    story.append(Spacer(1, 2 * mm))
    story.append(P("<b>Compatibilité ABO :</b> règle générale = plasma isogroupe. En cas "
                    "d'indisponibilité (urgence vitale), le plasma AB est utilisable quel que "
                    "soit le groupe du receveur, le plasma A ou B pour un receveur O ; le plasma "
                    "O n'est compatible qu'avec un receveur O (mention obligatoire « Réservé "
                    "exclusivement à une transfusion isogroupe ABO »).", S_BODY_SM))
    story.append(Spacer(1, 2 * mm))
    story.append(info_panel(P(
        "<b>Contre-indication ABSOLUE</b> (tous types de plasma) : présence d'un anticorps "
        "anti-IgA chez un sujet déficitaire en IgA (risque de réaction anaphylactique). "
        "<b>Contre-indication spécifique au PFC-IA</b> : antécédent de réponse allergique à "
        "l'amotosalen ou aux psoralènes (le texte source l'exprime lui-même comme une "
        "contre-indication, non une simple précaution). Les autres mesures listées par type de "
        "plasma (changement de lot/don après une 1<sup>re</sup> réaction allergique pour le "
        "PFC-SD/PFC-Se, précaution de photothérapie néonatale pour le PFC-IA) restent, elles, "
        "des <b>précautions d'emploi</b>.", S_BODY_SM), bg=RED_LIGHT, border=RED))
    story.append(Spacer(1, 2 * mm))
    story.append(P("<b>Effets indésirables :</b> le plasma est le PSL le moins souvent impliqué "
                    "dans les déclarations d'hémovigilance. Deux complications potentiellement "
                    "graves (2006-2010) : <b>TRALI</b> (détresse respiratoire aiguë "
                    "post-transfusionnelle, lié aux anticorps anti-leucocytaires acquis pendant "
                    "la grossesse — prévention : seuls hommes, femmes nullipares, et femmes avec "
                    "enfant à recherche anti-HLA négative sont admis comme donneurs de plasma) et "
                    "<b>réactions allergiques</b> (rares mais toute réaction grave impose des "
                    "explorations allergologiques immédiates — histamine, tryptase — et à "
                    "distance, 4-6 semaines).", S_BODY_SM))
    story.append(Spacer(1, 2 * mm))
    story.append(P("<b>Tests biologiques :</b> le temps de Quick est le test essentiel de "
                    "détection des coagulopathies acquises. L'INR n'est utilisable que sous AVK. "
                    "Le ratio temps de Quick patient/témoin (seuil &gt; 1,5) est la meilleure "
                    "expression du résultat hors AVK, notamment en hémorragie massive. Biologie "
                    "délocalisée (TP délocalisé, thromboélastogramme) : corrélation acceptable, "
                    "utile pour le suivi du fibrinogène et la mise en évidence d'une "
                    "hyperfibrinolyse, mais réservée à des équipes entraînées.", S_BODY_SM))
    return story

def _section_chirurgie():
    story = []
    story.append(Spacer(1, 2 * mm))
    story.append(section_bar("Indications — Chirurgie, traumatologie et obstétrique"))
    story.append(Spacer(1, 2 * mm))
    story.append(prop_table([
        ("Ne pas utiliser le plasma thérapeutique comme soluté de remplissage.", "C"),
        ("Administration prophylactique avant la survenue du saignement, chez un patient à "
         "facteurs normaux ou modérément altérés : non indiquée.", "AP"),
        ("Hémorragie modérée/peu évolutive/contrôlée : administration guidée en priorité par les "
         "tests de laboratoire, réalisée seulement si ratio Quick patient/témoin &gt; 1,5 "
         "(TP ≈ 40 %).", "C"),
        ("Volume initial de plasma à prescrire : 10 à 15 mL/kg ; pas d'argument pour transfuser "
         "plus précocement ou plus massivement dans cette indication.", "AP"),
        ("Choc hémorragique/transfusion massive (&gt; 5 CGR en 3h) : transfuser le plasma en "
         "association aux CGR, ratio PFC:CGR entre 1:2 et 1:1.", "C"),
        ("La transfusion de plasma doit débuter au plus vite, idéalement en même temps que les "
         "concentrés de globules rouges.", "C"),
        ("Transfusion plaquettaire précoce, généralement dès la 2<sup>e</sup> prescription "
         "transfusionnelle.", "C"),
        ("Mise en place de protocoles de transfusion massive dans les centres prenant en charge "
         "des hémorragies massives (réduction des délais : coursiers, décongélation sur appel "
         "SAMU).", "C"),
        ("Surveiller l'évolution du fibrinogène, objectif 1,5-2 g/L au cours de la prise en "
         "charge transfusionnelle.", "C"),
        ("Obstétrique : plasma recommandé dans la coagulopathie obstétricale si le traitement "
         "étiologique ne contrôle pas rapidement l'hémorragie.", "AP"),
        ("Obstétrique : fibrinogène mesuré précocement pour prédire la gravité de l'hémorragie.", "C"),
        ("Obstétrique : décider de la stratégie transfusionnelle pour maintenir le fibrinogène "
         "≥ 2 g/L ; monitorage répété au moins toutes les 2-3h.", "AP"),
        ("Neurochirurgie, sans hémorragie massive : plasma indiqué si TP &lt; 50 % (surveillance "
         "d'un traumatisé crânien grave) ou &lt; 60 % (pose d'un capteur de pression "
         "intracrânienne).", "AP"),
        ("Chirurgie cardiaque : indication seulement si saignement microvasculaire persistant ET "
         "déficit en facteurs (TP ≤ 40 % ou TCA &gt; 1,8/témoin, temps de thrombine normal, ou "
         "facteurs ≤ 40 %).", "AP"),
        ("Chirurgie cardiaque, en l'absence de saignement : pas d'indication au plasma "
         "(prescription prophylactique non justifiée, aucun bénéfice, risques transfusionnels "
         "accrus).", "AP"),
        ("Chaque centre de chirurgie cardiaque doit établir son propre algorithme décisionnel "
         "(réduit la consommation de PSL, les complications post-opératoires et la durée de "
         "séjour).", "B"),
        ("Chirurgie cardiaque : posologie initiale 15 mL/kg, répétée selon réévaluation "
         "clinico-biologique.", "AP"),
        ("Rupture d'anévrysme de l'aorte abdominale : prise en charge intensive et précoce avec "
         "ratio PFC:CGR augmenté jusqu'à 1:1 en peropératoire, associée à une amélioration de la "
         "survie.", "C"),
        ("Insuffisance hépatocellulaire chronique, sans saignement : transfusion de PFC non "
         "recommandée.", "AP"),
        ("Insuffisance hépatique aiguë sévère, sujet ne saignant pas et non exposé à un geste "
         "vulnérant : transfusion systématique/préventive non recommandée dans le seul but de "
         "corriger l'hémostase (aucune preuve de bénéfice, perturbe la valeur pronostique pour "
         "la décision de transplantation). Exception : peut être envisagée, parmi d'autres "
         "traitements hémostatiques et selon les anomalies prédominantes de la coagulation, "
         "avant la pose d'un capteur de pression intracrânienne et après décision de "
         "transplantation hépatique.", "AP"),
        ("Brûlures : plasma comme soluté de remplissage, non justifié.", "AP"),
    ]))
    return story

def _section_medecine():
    story = []
    story.append(Spacer(1, 2 * mm))
    story.append(section_bar("Indications en médecine"))
    story.append(Spacer(1, 2 * mm))
    story.append(prop_table([
        ("CIVD avec effondrement des facteurs (TP &lt; 35-40 %), associée à une hémorragie "
         "active ou potentielle (acte invasif) : transfusion de 10 à 15 mL/kg.", "B"),
        ("Déficit en un facteur pour lequel une préparation purifiée existe mais n'est pas "
         "rapidement disponible : apport de plasma (10-15 mL/kg) licite en situation d'urgence "
         "hémorragique.", "AP"),
        ("Micro-angiopathie thrombotique (PTT, SHU grave) : effet thérapeutique reconnu à "
         "40-60 mL/kg (1 à 1,5 masse plasmatique), préférentiellement par échanges plasmatiques "
         "quotidiens jusqu'à disparition des défaillances d'organe et plaquettes &gt; 150 G/L "
         "pendant ≥ 48h.", "B"),
        ("Traitements immunomodulateurs associés : peuvent diminuer la durée du traitement chez "
         "les patients en réponse sub-optimale.", "B"),
        ("Plasmathérapie au long cours : peut être nécessaire dans les PTT héréditaires "
         "récurrents.", "AP"),
        ("SHU atypique : les échanges plasmatiques constituent le traitement de 1<sup>re</sup> "
         "ligne (ne repose pas sur des essais thérapeutiques).", "AP"),
        ("Échanges plasmatiques aux colloïdes, patient sans risque hémorragique : maintenir le "
         "fibrinogène ≥ 1 g/L (plasma en fin de séance, 10-20 mL/kg). Risque hémorragique lié à "
         "la pathologie : plasma plus précoce et à plus forte dose (30 mL/kg).", "—"),
        ("Avant une intervention chirurgicale à fort risque hémorragique à court terme : utiliser "
         "du PFC (et non un colloïde) lors des échanges plasmatiques.", "AP"),
        ("Œdème angioneurotique héréditaire : le plasma n'est pas le traitement des poussées "
         "aiguës (C1-INH IV ou icatibant SC en 1<sup>re</sup> ligne) ; envisageable seulement en "
         "l'absence de disponibilité immédiate des traitements spécifiques.", "—"),
    ]))
    return story

def _section_pediatrie_avk():
    story = []
    story.append(Spacer(1, 2 * mm))
    story.append(section_bar("Néonatologie et pédiatrie"))
    story.append(Spacer(1, 2 * mm))
    story.append(prop_table([
        ("Utilisation similaire à l'adulte (CIVD, hémorragie massive, insuffisance hépatique).", "—"),
        ("CIVD avec syndrome hémorragique grave : transfusion à 10-20 mL/kg, parallèlement au "
         "traitement de la cause.", "—"),
        ("Circulation extra-corporelle (CEC) : utiliser du sang reconstitué avec du plasma "
         "thérapeutique pour l'amorçage des circuits.", "B"),
        ("Grand prématuré &lt; 29 SA en détresse vitale : transfusion fréquemment utilisée si "
         "facteurs de coagulation &lt; 20 %, même en l'absence de syndrome hémorragique "
         "clinique.", "C"),
        ("Syndrome hémorragique sévère dans l'attente de l'effet de la vitamine K (maladie "
         "hémorragique du nouveau-né) : recours au PFC possible.", "C"),
        ("Non indiqué chez l'enfant/nouveau-né : SHU typique post-diarrhéique (STEC+) sans "
         "critère de gravité ; infection néonatale sans CIVD (adjuvant à l'antibiothérapie) ; "
         "hypovolémie sans syndrome hémorragique ni trouble de l'hémostase ; prévention des "
         "hémorragies intraventriculaires du prématuré sans coagulopathie ; nouveau-né sain "
         "avant chirurgie.", "—"),
    ]))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P("Posologie en néonatologie : 10-20 mL/kg sur 1 à 3h IV au perfuseur "
                    "électrique (débit constant) — le plasma apporte ≈ 170 mmol/L de sodium, à "
                    "prendre en compte dans l'équilibre hydroélectrolytique. Prophylaxie "
                    "systématique de la maladie hémorragique du nouveau-né par vitamine K "
                    "(2 mg à terme / 1 mg/kg si prématuré, renouvelé J2-J7 ; 2 mg/semaine PO si "
                    "allaitement exclusif jusqu'au sevrage).", S_NOTE))
    story.append(Spacer(1, 3 * mm))

    story.append(section_bar("Antidote au surdosage en AVK"))
    story.append(Spacer(1, 2 * mm))
    story.append(P("Encadré par les recommandations HAS de 2008 (toujours valides) : en cas "
                    "d'hémorragie grave sous AVK, la <b>vitamine K</b> et les <b>concentrés de "
                    "complexe prothrombinique (CCP)</b> sont les moyens les plus appropriés. La "
                    "place du PFC est exceptionnelle, limitée à deux situations rares :",
                    S_BODY_SM))
    story.append(Spacer(1, 2 * mm))
    story.append(prop_table([
        ("Absence de disponibilité de CCP pour antagoniser les AVK en cas d'hémorragie grave.", "B"),
        ("Absence de disponibilité de CCP ne contenant pas d'héparine, chez un patient aux "
         "antécédents de thrombopénie induite par l'héparine (TIH).", "—"),
    ]))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P("<i>Hémorragie grave ou potentiellement grave</i> = au moins un critère : "
                    "hémorragie extériorisée non contrôlable ; instabilité hémodynamique "
                    "(PAS &lt; 90 mmHg ou chute de 40 mmHg, PAM &lt; 65 mmHg, tout signe de "
                    "choc) ; geste hémostatique urgent nécessaire (chirurgie, radiologie "
                    "interventionnelle, endoscopie) ; nécessité de transfusion de CGR ; "
                    "localisation menaçant le pronostic vital ou fonctionnel.", S_NOTE))
    story.append(Spacer(1, 3 * mm))

    story.append(section_bar("Plasma autologue — indications"))
    story.append(Spacer(1, 2 * mm))
    story.append(prop_table([
        ("Aucune étude ne définit les indications du plasma autologue. Si aucune perte volémique "
         "importante n'est attendue (recours au plasma non envisagé) : le prélèvement pour "
         "transfusion autologue peut se faire par érythrocytaphérèse (ne fournit pas de plasma "
         "autologue).", "AP"),
        ("Lorsque le plasma autologue est disponible, le choix entre son emploi et les "
         "cristalloïdes/colloïdes doit être pesé au cas par cas (risques relatifs comparables) : "
         "l'emploi systématique comme produit de remplissage ne peut être recommandé.", "—"),
    ]))
    story.append(Spacer(1, 4 * mm))
    story.append(P("Fiche de synthèse indépendante, produite pour un usage d'aide-mémoire. Elle "
                    "reprend l'intégralité des indications gradées et des messages-clés du texte "
                    "source, mais ne remplace pas le texte intégral et n'est ni éditée ni validée "
                    "par l'ANSM ou la HAS. En cas de doute, se référer au texte intégral et/ou à "
                    "un avis spécialisé transfusionnel.", S_SOURCE))
    return story

def _section_all():
    return (_section_intro() + [Spacer(1, 3 * mm)] + _section_types_plasma()
            + [Spacer(1, 3 * mm)] + _section_chirurgie() + [Spacer(1, 3 * mm)] + _section_medecine()
            + [Spacer(1, 3 * mm)] + _section_pediatrie_avk())

SECTIONS = [
    ("Actualisation 2012 — produits, indications, pédiatrie & antidote AVK", _section_all),
]

def _make_doc(path=None):
    return SimpleDocTemplate(path or OUT, pagesize=A4,
                              leftMargin=MARGIN, rightMargin=MARGIN,
                              topMargin=32 * mm, bottomMargin=16 * mm,
                              title="ANSM/HAS 2012 - Transfusion de plasma thérapeutique",
                              author="Synthèse indépendante (source ANSM/HAS)")

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
