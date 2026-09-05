# -*- coding: utf-8 -*-
"""
Fiche de synthese - RFE commune SRLF-SFAR (2016), en collaboration avec l'ANARLF, le GFRUP,
la SFMU et la SFNV : "Controle ciblé de la température en réanimation (hors nouveau-nés)".
Texte valide par le CA de la SRLF et de la SFAR le 18/02/2016. Publie initialement Anaesth
Crit Care Pain Med 2018;37(5):481-91 (doi 10.1016/j.accpm.2017.06.003), puis Anesth Reanim.
2019;5:49-66 (doi 10.1016/j.anrea.2018.10.004). Source verifiee :
https://sfar.org/wp-content/uploads/2019/10/rfe-controle-cible-de-la-temperature-en-reanimation.pdf
18 pages source (references incluses), document compact -> couverture complete.

METHODOLOGIE : methode GRADE classique (format PICO, recherche PubMed/Cochrane sur 10 ans,
cotation individuelle 1-9 puis GRADE grid, seuil 50% pour retenir une recommandation avec
<20% d'opposition, seuil 70% pour un "accord fort"). Resume officiel : 30 recommandations
(6 champs cliniques : arret cardiaque, traumatisme cranien, AVC/hemorragies cerebrales,
autres agressions cerebrales [meningite/etat de mal epileptique], etats de choc, modalites
pratiques de mise en oeuvre et de surveillance), dont 3 fortes (grade 1), 13 faibles
(grade 2) et 14 avis d'experts ; accord fort obtenu pour 100% des 30 recommandations apres
2 tours de cotation.

VERIFICATION INDEPENDANTE (inventaire exhaustif, grep de toutes les occurrences
"(Grade" / "(Avis d'experts)" dans le corps du texte) : exactement 30 items retrouves,
repartition confirmee a l'identique - 3 x "Grade 1"/"Grade 1+" (R1.1, R2.2 Pediatrique,
R6.1), 13 x "Grade 2"/"Grade 2+" (R1.2, R1.4, R1.5, R1.2 Pediatrique, R2.1, R2.2, R2.3,
R5.1, R5.2, R5.3, R6.3, R6.4, R6.2 Pediatrique), 14 x "Avis d'experts" (R1.3, R1.1
Pediatrique, R2.1 Pediatrique, R3.1, R3.2, R3.3, R3.1 Pediatrique, R4.1, R4.2, R4.3, R4.4,
R4.1 Pediatrique, R6.2, R6.1 Pediatrique). Aucune divergence source-interne detectee sur ce
denombrement (contrairement a d'autres fiches du corpus) : le total et la repartition
annonces par le resume officiel concordent exactement avec le comptage direct.

PARTICULARITE DE NOTATION (disclosure) : ce document n'utilise JAMAIS de suffixe "-" (grade
"1-" ou "2-" comme dans d'autres fiches du corpus, ex. fiche_pavm.py). Verification
exhaustive (grep "(Grade [0-9]" sur tout le corps du texte) : seuls "Grade 1+", "Grade 2+",
"Grade 1" (sans signe) et "Grade 2" (sans signe) apparaissent. Le signe "+" n'est imprime que
pour les recommandations de sens positif ("il faut ...") ; les recommandations de sens
negatif ("il ne faut/faudrait pas ...") portent le grade SANS aucun signe, y compris pour une
recommandation forte (R2.2 Pediatrique : "il ne faut pas induire..." -> imprime "(Grade 1)",
pas "(Grade 1-)"). Ce n'est pas une incoherence du document (le sens est de toute façon
explicite dans le texte de chaque item) mais une convention typographique propre a cette RFE,
differente de celle utilisee ailleurs dans ce corpus - disclosee ici plutot que silencieusement
harmonisee. Extension locale, non invasive, de GRADE_COLORS (comme dans fiche_aap_programmee.py
et fiche_nutrition.py) : label "1" (grade fort, sens negatif) -> memes couleurs que "1-" ;
label "2" (grade faible, sens negatif) -> memes couleurs que "2-". Le texte du chip reproduit
neanmoins tel quel le libelle imprime par la source ("1" et "2", jamais "1-"/"2-" invente).

PAS DE TABLEAU NI DE FIGURE dans le corps du texte source (verifie par grep "Tableau"/
"Figure"/"TABLEAU" sur l'integralite du texte extrait : aucune occurrence) - uniquement des
recommandations numerotees R<champ>.<n> (+ variantes "Pediatrique") avec argumentaire en
prose. Chaque recommandation adulte et pediatrique du corps du texte est reprise ici
integralement ; les arguments cles de chaque argumentaire sont resumes (non recopies
integralement - l'argumentaire complet, avec references numerotees, reste dans le texte
source, cf. avertissement de traçabilite).
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from style import *
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.units import mm

# Local, non-invasive extension of the shared GRADE_COLORS dict: this source prints "Grade 1"
# and "Grade 2" (no sign) for negative-direction recommendations instead of "1-"/"2-" used
# elsewhere in the corpus - same color semantics, label reproduced exactly as printed.
GRADE_COLORS["1"] = (RED, WHITE)
GRADE_COLORS["2"] = (AMBER, WHITE)

OUT = "/home/user/rfe-sfar-website/output/Fiche_SRLF_SFAR_Controle_Temperature_2016.pdf"

SOURCE_TXT = ("Source : RFE commune SRLF-SFAR, en collaboration avec l'ANARLF, le GFRUP, la "
              "SFMU et la SFNV — « Contrôle ciblé de la température en réanimation (hors "
              "nouveau-nés) » — texte validé par le CA SRLF et le CA SFAR (18/02/2016), publié "
              "Anesth Reanim. 2019;5:49-66, doi 10.1016/j.anrea.2018.10.004. Fiche de synthèse "
              "non officielle : se référer au texte intégral.")

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

def legend_flowable():
    chip_w = 15*mm
    content_w = PAGE_W - 2*MARGIN
    text_w = content_w - chip_w
    rows_txt = [
        ("1+", "Recommandation forte, sens positif (« il faut »)."),
        ("1", "Recommandation forte, sens négatif (« il ne faut pas ») — imprimée sans signe par la source."),
        ("2+", "Recommandation optionnelle, sens positif (« il faut probablement »)."),
        ("2", "Recommandation optionnelle, sens négatif (« il ne faut probablement pas ») — imprimée sans signe par la source."),
        ("AE", "Avis d'experts (littérature insuffisante pour appliquer la méthode GRADE)."),
    ]
    data = [[chip(lab, width=chip_w-2*mm), P(txt, S_BADGE_HEAD)] for lab, txt in rows_txt]
    t = Table(data, colWidths=[chip_w, text_w])
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 1), ("RIGHTPADDING", (0, 0), (-1, -1), 1),
        ("TOPPADDING", (0, 0), (-1, -1), 1.6), ("BOTTOMPADDING", (0, 0), (-1, -1), 1.6),
    ]))
    return t

TOTAL_PAGES = {"n": 9}

def on_page(canvas, doc, page_title):
    header_band(canvas, doc, "SRLF / SFAR — RFE 2016 — FICHE DE SYNTHÈSE",
                "Contrôle ciblé de la température",
                page_title, icon_fn=lambda c, x, y: icon_drop(c, x, y, 13*mm), color=TEAL_DARK)
    footer_band(canvas, doc, SOURCE_TXT, f"Page {doc.page} / {TOTAL_PAGES['n']}")

# ---------------------------------------------------------------------------
def _section_intro():
    story = []
    story.append(Spacer(1, 3*mm))
    story.append(info_panel(P(
        "<b>Champ :</b> utilisation du contrôle ciblé de la température (CCT) — qui regroupe "
        "toutes les interventions visant à atteindre et maintenir un niveau de température "
        "donné (prévention de la fièvre, maintien de la normothermie, ou hypothermie "
        "induite) — chez l'adulte et l'enfant (hors nouveau-nés) en réanimation, "
        "principalement comme méthode de neuroprotection. RFE commune SRLF-SFAR, avec la "
        "participation de l'ANARLF, du GFRUP, de la SFMU et de la SFNV. 15 experts et 2 "
        "coordinateurs, 6 champs cliniques : arrêt cardiaque, traumatisme crânien, accident "
        "vasculaire cérébral, autres agressions cérébrales, états de choc, et modalités "
        "pratiques de mise en œuvre.<br/><br/>"
        "<b>Méthode GRADE :</b> questions au format PICO, recherche bibliographique PubMed/"
        "Cochrane sur les 10 dernières années (publications postérieures à 2005, anglais ou "
        "français), analyse pédiatrique spécifique. Cotation individuelle de chaque "
        "recommandation par les experts (échelle 1-9), puis cotation collective (méthode "
        "GRADE grid) : une recommandation est retenue si ≥ 50 % des experts vont dans le même "
        "sens (et &lt; 20 % en désaccord) ; l'accord est qualifié de <b>« fort »</b> à partir de "
        "70 %. En l'absence d'accord fort, les recommandations étaient reformulées puis "
        "recotées.",
        S_BODY), bg=BG_PANEL, border=TEAL))
    story.append(Spacer(1, 3*mm))
    story.append(info_panel(P(
        "<b>Résultats :</b> 30 recommandations formalisées — 3 fortes (grade 1), 13 "
        "optionnelles (grade 2), 14 avis d'experts. Accord fort obtenu pour la totalité "
        "(100 %) des 30 recommandations après 2 tours de cotation et plusieurs amendements. "
        "Vérification indépendante (inventaire exhaustif de chaque tag imprimé dans le corps "
        "du texte) : total et répartition confirmés à l'identique — aucune divergence "
        "source-interne détectée sur ce point (contrairement à d'autres documents de ce "
        "corpus).",
        S_BODY_SM), bg=GREY_LIGHT, border=GREY))
    story.append(Spacer(1, 3*mm))
    story.append(info_panel(P(
        "<b>Particularité de notation (disclosure) :</b> cette source n'imprime jamais de "
        "suffixe « - » : les recommandations de sens négatif (« il ne faut/faudrait pas ») "
        "portent leur grade <b>sans aucun signe</b> — y compris pour une recommandation forte "
        "(R2.2 Pédiatrique : « il ne faut pas induire… » est imprimée « (Grade 1) », jamais "
        "« (Grade 1-) »). Ce n'est pas une incohérence de fond (le sens de chaque item reste "
        "explicite dans son texte), mais une convention typographique propre à cette RFE, "
        "différente de celle d'autres fiches de ce corpus — reproduite ici telle quelle "
        "(chips « 1 » et « 2 », jamais « 1- »/« 2- » inventés) plutôt qu'harmonisée "
        "silencieusement.",
        S_BODY_SM), bg=AMBER_LIGHT, border=AMBER))
    story.append(Spacer(1, 3*mm))
    story.append(section_bar("Légende des grades"))
    story.append(Spacer(1, 2*mm))
    story.append(legend_flowable())
    return story

def _section_ac():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Champ 1 — Contrôle ciblé de la température après arrêt cardiaque"))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("R1.1", "Chez les patients comateux après réanimation d'un arrêt cardiaque (AC) "
         "extra-hospitalier avec rythme initial choquable (FV ou TV), il faut pratiquer un "
         "CCT dans le but d'améliorer la survie avec bon pronostic neurologique.", "1+"),
        ("R1.2", "Chez les patients comateux après réanimation d'un AC extra-hospitalier avec "
         "rythme initial non choquable (asystolie ou rythme sans pouls), il faut probablement "
         "pratiquer un CCT dans le but d'améliorer la survie avec bon pronostic "
         "neurologique.", "2+"),
        ("R1.3", "Chez les patients comateux après réanimation d'un AC intra-hospitalier, il "
         "faut probablement pratiquer un CCT dans le but d'améliorer la survie avec bon "
         "pronostic neurologique.", "AE"),
        ("R1.4", "Chez les patients traités par CCT après AC, il faut probablement cibler un "
         "niveau de température entre 32 et 36 °C dans le but d'améliorer la survie avec bon "
         "pronostic neurologique.", "2+"),
        ("R1.5", "Parmi les méthodes de CCT disponibles en préhospitalier, chez les patients "
         "traités par CCT après AC, il ne faut probablement pas débuter le CCT par perfusion "
         "de solutés froids pendant le transport vers l'hôpital, dans le but d'améliorer la "
         "survie avec bon pronostic neurologique.", "2"),
        ("R1.1 P", "<i>(Pédiatrique)</i> Chez les enfants comateux après réanimation d'un AC "
         "intra- ou extra-hospitalier sur rythme non choquable ou choquable, il faut "
         "probablement effectuer un CCT avec pour objectif la normothermie pour améliorer le "
         "pronostic neurologique.", "AE"),
        ("R1.2 P", "<i>(Pédiatrique)</i> Chez les enfants comateux après réanimation d'un AC "
         "extra-hospitalier sur rythme non choquable ou choquable, il ne faut probablement "
         "pas pratiquer un CCT avec un objectif de température entre 32 et 34 °C dans le but "
         "d'améliorer la survie avec bon pronostic neurologique.", "2"),
    ], [15*mm, PAGE_W-2*MARGIN-15*mm-16*mm, 16*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(P(
        "R1.1 : 2 études concordantes (1 randomisée, 1 non randomisée) en faveur du CCT sur "
        "le devenir neurologique pour l'AC sur rythme choquable ; conférence de consensus et "
        "méta-analyse récente également favorables. R1.2 : une méta-analyse spécifique aux "
        "rythmes non choquables retrouve une diminution de la mortalité hospitalière (RR "
        "0,86) sans différence sur le devenir neurologique ; absence d'alternative "
        "thérapeutique et absence d'étude de bon niveau défavorable. R1.4 : étude randomisée "
        "de 939 patients et méta-analyse concordantes — pas de différence entre 33 °C et "
        "36 °C, mais bénéfice d'un CCT &lt;34 °C par rapport à l'absence de CCT. R1.5 : "
        "plusieurs études randomisées, dont une de haut niveau de preuve montrant une "
        "augmentation des récidives d'AC et des œdèmes pulmonaires avec le NaCl froid "
        "préhospitalier. R1.2 pédiatrique : seule étude randomisée disponible (270 enfants) "
        "ne montrant pas de différence de survie avec bon pronostic neurologique entre "
        "hypothermie à 33 °C et CCT à 36-37,5 °C.", S_NOTE))
    return story

def _section_tc():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Champ 2 — Contrôle ciblé de la température après traumatisme crânien"))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("R2.1", "Chez les patients traumatisés crâniens graves, il faut probablement "
         "pratiquer un CCT entre 35 et 37 °C dans le but de prévenir l'hypertension "
         "intracrânienne.", "2+"),
        ("R2.2", "Chez les patients traumatisés crâniens graves, il faut probablement "
         "pratiquer un CCT entre 35 et 37 °C dans le but d'améliorer la survie avec bon "
         "pronostic neurologique.", "2+"),
        ("R2.3", "Chez les patients traumatisés crâniens avec hypertension intracrânienne "
         "malgré un traitement médical bien conduit, il faut probablement pratiquer un CCT "
         "entre 34 et 35 °C dans le but de faire baisser la pression intracrânienne.", "2+"),
        ("R2.1 P", "<i>(Pédiatrique)</i> Chez l'enfant traumatisé crânien grave, il faut faire "
         "un CCT visant à maintenir une normothermie.", "AE"),
        ("R2.2 P", "<i>(Pédiatrique)</i> Chez l'enfant traumatisé crânien grave, il ne faut "
         "pas induire de CCT avec pour but d'obtenir une hypothermie thérapeutique entre 32 "
         "et 34 °C pour améliorer le pronostic ou pour contrôler l'HTIC.", "1"),
    ], [15*mm, PAGE_W-2*MARGIN-15*mm-16*mm, 16*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(P(
        "R2.1/R2.2 : aucune étude randomisée contrôlée ne démontre qu'un CCT à 35-37 °C "
        "prévient l'HTIC ou améliore le pronostic neurologique après TC grave, mais la "
        "gravité du pronostic associé à l'hyperthermie impose, en l'absence d'autres preuves, "
        "de recommander ce CCT ; des études à haut niveau de preuve et des méta-analyses ne "
        "montrent en revanche aucun bénéfice de l'hypothermie thérapeutique (32-35 °C) versus "
        "normothermie sur la mortalité ou le devenir neurologique — échec du concept de "
        "neuroprotection par hypothermie chez le TC grave. R2.3 : résultats discordants — "
        "Polderman et al. montrent la supériorité de l'hypothermie sur les barbituriques "
        "seuls pour contrôler l'HTIC, mais l'essai randomisé Eurotherm (387 patients) montre "
        "un effet négatif du CCT 32-35 °C sur le devenir neurologique à 6 mois (devenir "
        "favorable 26 % vs 37 % ; OR de pronostic défavorable 1,53) ; une durée d'hypothermie "
        "plus longue (5 j vs 2 j) limiterait le rebond d'HTIC au réchauffement. R2.2 "
        "pédiatrique : 2 essais randomisés (225 et 77 patients) concordants pour l'absence de "
        "bénéfice de l'hypothermie modérée, avec davantage d'hypotension et de pression de "
        "perfusion cérébrale basse sous hypothermie.", S_NOTE))
    return story

def _section_avc():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Champ 3 — AVC grave et autres hémorragies cérébrales"))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("R3.1", "Chez les patients à la phase aiguë d'un AVC ischémique grave, il faut "
         "probablement pratiquer un CCT ciblant la normothermie.", "AE"),
        ("R3.2", "Chez les patients comateux avec hématome intraparenchymateux spontané, il "
         "faut probablement réaliser un CCT entre 35 et 37 °C pour faire baisser la pression "
         "intracrânienne.", "AE"),
        ("R3.3", "Chez les patients comateux avec une hémorragie sous-arachnoïdienne, il faut "
         "probablement réaliser un CCT pour faire baisser la pression intracrânienne et/ou "
         "améliorer le pronostic neurologique.", "AE"),
        ("R3.1 P", "<i>(Pédiatrique)</i> Chez l'enfant présentant une hémorragie "
         "sous-arachnoïdienne, il faut probablement faire un CCT avec une température cible "
         "entre 36 et 37,5 °C dans le but de limiter l'HTIC.", "AE"),
    ], [15*mm, PAGE_W-2*MARGIN-15*mm-16*mm, 16*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(P(
        "R3.1 : hyperthermie fréquente (&gt;50 %) et corrélée au mauvais pronostic à la phase "
        "aiguë d'un AVC ischémique, mais l'intérêt de l'hypothermie thérapeutique n'est pas "
        "démontré (6 essais randomisés, effectifs réduits, biais méthodologiques ; 2 essais "
        "randomisés en cours : EuroHYP-1, ICTuS 2/3). Pas de bénéfice démontré des "
        "antipyrétiques systématiques sur le devenir neurologique ou la mortalité "
        "(méta-analyse de 4 essais). R3.2 : études essentiellement observationnelles, "
        "effectifs limités ; effet favorable sur la PIC rapporté mais sans conclusion "
        "possible sur le pronostic neurologique ; essai randomisé CINCH en cours. R3.3 : "
        "fièvre associée au mauvais pronostic dans plusieurs études observationnelles de "
        "grand effectif ; études interventionnelles limitées mais concordantes sur un effet "
        "modeste sur la PIC et une possible amélioration du pronostic à 12 mois "
        "(normothermie ou hypothermie 32-34 °C).", S_NOTE))
    return story

def _section_autres():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Champ 4 — Autres agressions cérébrales (méningite, état de mal épileptique)"))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("R4.1", "Chez les patients avec un état de mal épileptique réfractaire ou "
         "superréfractaire, persistant sous anesthésie générale, il faut probablement faire "
         "un CCT entre 32 et 35 °C pour contrôler l'activité épileptique.", "AE"),
        ("R4.2", "Chez les patients dans le coma avec une méningite ou une "
         "méningo-encéphalite, il ne faut probablement pas pratiquer de CCT lorsque la fièvre "
         "est bien tolérée.", "AE"),
        ("R4.3", "Chez les patients dans le coma avec une méningite bactérienne, en l'absence "
         "d'HTIC, il ne faut probablement pas pratiquer d'hypothermie, en comparaison avec "
         "une normothermie, dans le but d'améliorer la survie avec bon pronostic "
         "neurologique.", "AE"),
        ("R4.4", "Chez les patients dans le coma avec une méningite bactérienne et une HTIC, "
         "il faut probablement pratiquer une hypothermie, en comparaison avec une "
         "normothermie, dans le but d'améliorer la survie avec bon pronostic neurologique.", "AE"),
        ("R4.1 P", "<i>(Pédiatrique)</i> Chez l'enfant présentant un état de mal épileptique, "
         "il faut probablement réaliser un CCT (normothermie) à visée neuroprotectrice.", "AE"),
    ], [15*mm, PAGE_W-2*MARGIN-15*mm-16*mm, 16*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(P(
        "R4.1 : littérature clinique très limitée (état de mal épileptique réfractaire "
        "évoluant depuis plus de 24 h, malgré doses maximales de traitements "
        "antiépileptiques et anesthésiques) ; cas rapportés d'un meilleur contrôle de "
        "l'activité épileptique électrique et d'un tracé de suppression-burst sous CCT 32-35 "
        "°C. R4.2/R4.3 : pas d'étude interventionnelle sur le traitement de l'hyperthermie ; "
        "études observationnelles discordantes selon le contexte (infection du SNC vs autres "
        "agressions cérébrales) ; l'étude randomisée de Mourvillier et al. suggère un effet "
        "délétère de l'hypothermie en cas de méningite bactérienne sans HTIC, mais avec "
        "d'importants biais méthodologiques (choc septique plus fréquent dans le groupe "
        "hypothermie). R4.4 : étude de Kutlesa et al. en faveur de l'hypothermie en cas "
        "d'HTIC associée, mais groupe témoin historique et analyse statistique de faible "
        "valeur ; plusieurs cas d'encéphalites virales avec HTIC favorablement traitées par "
        "hypothermie également rapportés.", S_NOTE))
    return story

def _section_choc():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Champ 5 — États de choc (choc cardiogénique, choc septique)"))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("R5.1", "Chez les patients en choc cardiogénique, il ne faut probablement pas "
         "pratiquer un CCT ciblant une température inférieure à 36 °C dans le but "
         "d'améliorer la survie.", "2"),
        ("R5.2", "Chez les patients en choc septique, il ne faut probablement pas pratiquer "
         "un CCT ciblant une température inférieure à 36 °C dans le but d'améliorer la "
         "survie.", "2"),
        ("R5.3", "Chez les patients en choc septique, il faut probablement pratiquer un CCT "
         "ciblant la normothermie dans le but d'améliorer l'hémodynamique.", "2+"),
    ], [15*mm, PAGE_W-2*MARGIN-15*mm-16*mm, 16*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(P(
        "R5.1 : 4 études de faible niveau de preuve (prospectives vs groupe historique, "
        "rétrospectives ou non randomisées, effectifs faibles) — concluent seulement à la "
        "faisabilité de l'hypothermie modérée dans le choc cardiogénique, sans effet "
        "indésirable accru démontré ; étude prospective en cours (NCT01890317). R5.2/R5.3 : 5 "
        "essais randomisés en double insu, 3 d'entre eux comparant en réalité des AINS à un "
        "placebo (non spécifiquement le CCT) ; seule l'étude de Schortgen et al. évalue "
        "directement le CCT versus l'absence de CCT et montre une diminution significative de "
        "la dose de vasopresseurs et du nombre de jours en choc, avec une réduction de "
        "mortalité à J14 (objectif secondaire) non retrouvée à la sortie de réanimation ou de "
        "l'hôpital ; l'ensemble des études conclut à la faisabilité du CCT dans le choc "
        "septique, sans sur-incidence d'effets indésirables.", S_NOTE))
    return story

def _section_modalites():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Champ 6 — Modalités pratiques de mise en œuvre et de surveillance du CCT"))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("R6.1", "Chez les patients traités par CCT, il faut utiliser des méthodes asservies "
         "à la température corporelle, par comparaison aux méthodes non asservies, dans le "
         "but d'améliorer la qualité du CCT.", "1+"),
        ("R6.2", "Chez les patients traités par CCT, il faut probablement contrôler la "
         "vitesse du réchauffement.", "AE"),
        ("R6.3", "Chez les patients traités par CCT, il faut probablement privilégier des "
         "sites de mesure de température centrale.", "2+"),
        ("R6.4", "Chez les patients traités par CCT, il faut probablement surveiller la "
         "survenue de certaines complications : sepsis, pneumopathie, arythmie, "
         "hypokaliémie.", "2+"),
        ("R6.1 P", "<i>(Pédiatrique)</i> Chez les enfants pour lesquels le CCT a été retenu, "
         "il faut probablement utiliser des méthodes asservies à la température corporelle, "
         "par comparaison aux méthodes non asservies, dans le but d'améliorer la qualité du "
         "CCT.", "AE"),
        ("R6.2 P", "<i>(Pédiatrique)</i> Chez les enfants traités par CCT, il faut "
         "probablement privilégier des sites de mesure de température centrale.", "2+"),
    ], [15*mm, PAGE_W-2*MARGIN-15*mm-16*mm, 16*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(P(
        "R6.1 : essentiellement étudié en post-arrêt cardiaque — meilleure stabilité "
        "thermique en phase de maintien avec les méthodes asservies (3 essais randomisés de "
        "niveau haut à modéré + nombreuses études non randomisées concordantes), effet sur le "
        "devenir neurologique non définitivement établi. R6.2 : aucune étude randomisée "
        "n'évalue la vitesse de réchauffement de façon isolée ; dans le TC et l'AVC, une "
        "vitesse de réchauffement plus lente semble limiter le rebond d'HTIC (études "
        "expérimentales et par analogie). R6.3 : le rectum est le seul site périphérique "
        "validé par rapport à une mesure cérébrale de référence ; bon accord entre sites "
        "centraux (artère pulmonaire, œsophage, vessie, rectum), accord médiocre pour les "
        "sites périphériques (cutané, tympanique — biais rapporté de 1 °C). R6.4 : "
        "méta-analyse à la limite de la significativité pour le sepsis et les pneumopathies, "
        "mais études observationnelles de grand effectif retrouvant une association ; "
        "hypokaliémie &lt;3,5 mmol/L et risque accru d'arythmie rapportés par plusieurs "
        "études comparatives.", S_NOTE))
    return story

def _section_sources():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Sources et traçabilité", color=GREY))
    story.append(Spacer(1, 2*mm))
    story.append(P(
        "<b>Document source :</b> « Contrôle ciblé de la température en réanimation (hors "
        "nouveau-nés) » — RFE commune SRLF-SFAR, en collaboration avec l'ANARLF, le GFRUP, la "
        "SFMU et la SFNV. Alain Cariou, Jean-François Payen de la Garanderie (coordinateurs), "
        "et 15 experts. Texte validé par le CA de la SRLF et de la SFAR le 18/02/2016, publié "
        "initialement Anaesth Crit Care Pain Med 2018;37(5):481-91, puis Anesth Reanim. "
        "2019;5:49-66 (doi 10.1016/j.anrea.2018.10.004).", S_SOURCE))
    story.append(Spacer(1, 1.5*mm))
    story.append(P("<b>Couverture :</b> les 30 recommandations du corps du texte sont "
                    "reprises intégralement — 24 recommandations « adulte » (R1.1-R1.5, "
                    "R2.1-R2.3, R3.1-R3.3, R4.1-R4.4, R5.1-R5.3, R6.1-R6.4) et 6 "
                    "recommandations pédiatriques dédiées (R1.1/R1.2, R2.1/R2.2, R3.1, R4.1, "
                    "R6.1/R6.2 « Pédiatrique ») — avec les éléments clés de chaque "
                    "argumentaire. Aucun tableau ni figure dans le corps du texte source "
                    "(vérifié).", S_SOURCE))
    story.append(Spacer(1, 1.5*mm))
    story.append(P("<b>Vérification indépendante :</b> inventaire exhaustif de chaque tag "
                    "imprimé (« Grade 1/1+/2/2+ » ou « Avis d'experts ») en regard de chaque "
                    "recommandation du corps du texte — total (30) et répartition (3 grade 1, "
                    "13 grade 2, 14 avis d'experts) confirmés à l'identique du résumé "
                    "officiel. Particularité de notation disclosée en introduction : cette "
                    "source n'imprime jamais de suffixe « - », les recommandations de sens "
                    "négatif portant leur grade sans signe.", S_SOURCE))
    story.append(Spacer(1, 3*mm))
    story.append(info_panel(P(
        "<b>Avertissement :</b> ce document est une fiche de synthèse indépendante, produite "
        "pour un usage d'aide-mémoire. Il reprend l'intégralité des recommandations du corps "
        "du texte, avec les éléments clés de leur argumentaire, mais ne remplace pas le texte "
        "intégral (argumentaire complet, références bibliographiques) et n'est ni édité ni "
        "validé par la SRLF ou la SFAR. En cas de doute, se référer au texte intégral et/ou à "
        "un avis spécialisé. Document de 2016 : vérifier l'existence d'une actualisation plus "
        "récente en cas de doute.",
        S_BODY_SM), bg=GREY_LIGHT, border=GREY))
    return story

def _section_ac_tc():
    # KeepTogether around each champ (heading+table+note) - without it, a naive page-fill left
    # a single orphan line of champ 2's note stranded alone at the top of an otherwise-blank
    # page (checked visually at 135dpi). Wrapping moves the whole champ as one unit instead.
    return [KeepTogether(_section_ac())] + [Spacer(1, 3*mm)] + [KeepTogether(_section_tc())]

def _section_avc_autres():
    return [KeepTogether(_section_avc())] + [Spacer(1, 3*mm)] + [KeepTogether(_section_autres())]

def _section_choc_modalites():
    return ([KeepTogether(_section_choc())] + [Spacer(1, 3*mm)]
             + [KeepTogether(_section_modalites())] + [Spacer(1, 4*mm)]
             + _section_sources())

# Sections merged onto shared pages (no forced PageBreak between them) since each individual
# champ only fills 30-45% of a page on its own (checked visually at 135dpi) - merging keeps
# page count down without cramping any single table (verified after rebuild: no table split
# awkwardly, no page overflowing past a single extra page per group).
SECTIONS = [
    ("Introduction, méthodologie & légende", _section_intro),
    ("Champ 1 — Arrêt cardiaque / Champ 2 — Traumatisme crânien", _section_ac_tc),
    ("Champ 3 — AVC & hémorragies / Champ 4 — Autres agressions cérébrales", _section_avc_autres),
    ("Champ 5 — États de choc / Champ 6 — Modalités pratiques & traçabilité", _section_choc_modalites),
]

def _make_doc(path=None):
    return SimpleDocTemplate(path or OUT, pagesize=A4,
                              leftMargin=MARGIN, rightMargin=MARGIN,
                              topMargin=32*mm, bottomMargin=16*mm,
                              title="Fiche SRLF-SFAR 2016 - Controle cible de la temperature en reanimation",
                              author="Synthèse indépendante (source SRLF/SFAR)")

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
    # here was found to corrupt page 1's header_band in the final build (see CLAUDE.md).
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
