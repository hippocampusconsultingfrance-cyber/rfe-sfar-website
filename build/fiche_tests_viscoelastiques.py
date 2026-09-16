# -*- coding: utf-8 -*-
"""
Fiche de synthese - GIHP (Groupe d'Interet en Hemostase Perioperatoire),
"Position of the French Working Group on Perioperative Haemostasis (GIHP)
on viscoelastic tests: What role for which indication in bleeding
situations?" Roullet S. et al., Anaesth Crit Care Pain Med 38 (2019)
539-548 (disponible en ligne 3 fevrier 2018). Publie par Elsevier Masson
SAS pour la Sfar, article en libre acces (CC BY-NC-ND). 10 pages source
(texte en anglais), telecharge depuis sfar.org (download/tests-
viscoelastiques-2018/?wpdmdl=34421).

METHODOLOGIE : revue narrative de la litterature (pas de grille GRADE, pas
de niveaux de preuve I-V/grades A-E, pas de cotation Delphi) - le texte
formule des propositions explicites "The GIHP proposes..." integrees a la
prose, une par situation clinique (traumatisme severe, hemorragie du
post-partum, chirurgie cardiaque, transplantation hepatique). Aucune
proposition individuelle n'est cotee par un grade ou un niveau de preuve
- disclosure explicite dans la fiche (meme convention que
fiche_erreurs_medicamenteuses.py / fiche_antibiotherapie_probabiliste.py
pour les sources "sans cotation"). Le safety-net grep rule-4 du projet
(grades composites fabriques) n'a donc pas de sens ici : il n'y a tout
simplement pas de grade a fabriquer.

INVENTAIRE DES POSITIONS GIHP (9 propositions explicitement introduites
par "The GIHP proposes" dans le texte source, retrouvees par lecture
integrale + grep "GIHP propos"): 3 en traumatisme severe (diagnostic
precoce, ne pas guider l'acide tranexamique, inclusion dans algorithmes
ACT), 1 en HPP (evaluation rapide fibrinogene + ne pas guider l'acide
tranexamique), 1 en chirurgie cardiaque (utilisation en fin de CEC/
postoperatoire), 1 en transplantation hepatique (ne pas attendre le trace
typique d'hyperfibrinolyse si signes cliniques). En pediatrie, la source
ne formule AUCUNE position GIHP propre - elle cite seulement une
recommandation EXTERNE (ESA/Kozek-Langenecker 2013, grade 2C) pour la
detection de la coagulopathie de dilution/hyperfibrinolyse - disclosed
comme telle, jamais presentee comme une position du GIHP lui-meme.

PORTEE : couverture complete des principes techniques (TEG vs ROTEM,
parametres, reactifs), des 4 situations cliniques a position GIHP
explicite, de la section pediatrique (absence de position propre
disclosed) et de la section positionnement bedside/laboratoire
(reglementation de la biologie delocalisee).

ARGUMENTAIRE : la source cite des dizaines d'etudes avec RR/OR/IC95%/
effectifs par affirmation. Conformement a la regle de projet 2026-09-14,
seuls les seuils/chiffres directement actionnables (valeurs seuils de
FIBTEM/EXTEM, reductions de transfusion des meta-analyses cles) sont
conserves ; le detail etude-par-etude et les 128 references
bibliographiques ne sont pas repris.

AUDIT INDEPENDANT (subagent, aveugle au brouillon, verifiant a la fois
l'exactitude clinique ET la traduction anglais->francais) : aucune erreur
de sens trouvee - les 2 positions "ne pas guider l'acide tranexamique sur
les TVE" (trauma ET HPP) verifiees correctes et non inversees, la
non-attribution de la position pediatrique au GIHP (grade 2C = ESA,
disclosed) confirmee, la directionnalite hyperfibrinolyse pre/post-
anhepatique (mortalite vs thrombose) confirmee non inversee, aucune
valeur numerique erronee parmi celles retenues. Points MEDIUM corriges
suite a l'audit (omissions d'argumentaire jugees trop importantes,
au-dela de la simple couleur rhetorique de la regle 7) : seuils ACT r-TEG
du trauma completes avec leurs OR/IC95% + ajout de la cohorte Holcomb
(1974 patients, angle r-TEG superieur aux tests de routine, p<0.001) ;
IC95% ajoutes aux 3 meta-analyses de chirurgie cardiaque (Deppe/Cochrane/
Karkouti) ; qualificatif "mais pas plasma/concentres de facteurs" de
Karkouti restaure (son omission risquait de surestimer le benefice) ;
mention de la meta-analyse Bolliger & Tanaka 2013 ajoutee (sur-
prescription de fibrinogene/CCP sans guidage TVE). Note de "Couverture"
en page 4 mise a jour pour disclosed explicitement (regle 5) que
l'argumentaire complet (etudes isolees secondaires, IC95% restants,
128 references) reste condense et non integralement repris, au-dela
des positions GIHP elles-memes (100% couvertes) - les autres items MEDIUM
de l'audit (restaurer l'integralite des sous-etudes d'hyperfibrinolyse du
trauma, etc.) relevent de l'argumentaire au sens strict de la regle 7 et
sont volontairement laisses condenses.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from style import *
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.units import mm

OUT = "/home/user/rfe-sfar-website/output/Fiche_GIHP_Tests_Viscoelastiques_2019.pdf"

SOURCE_TXT = ("Source : Roullet S, et al. « Position of the French Working Group on Perioperative "
              "Haemostasis (GIHP) on viscoelastic tests ». Anaesth Crit Care Pain Med 2019;38:539-548 "
              "(GIHP). Fiche de synthèse non officielle, traduite et condensée : se référer au texte "
              "intégral.")

def P(txt, style=S_CELL):
    return Paragraph(txt, style)

CW_FULL = PAGE_W - 2 * MARGIN

def theme_table(rows, col_widths, head=("Thème", "Détail")):
    data = [[P(head[0], S_HEAD_W), P(head[1], S_HEAD_W)]]
    for theme, detail in rows:
        data.append([P(theme, S_CELL_B), P(detail, S_CELL)])
    t = Table(data, colWidths=col_widths, repeatRows=1)
    style_cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), TEAL_DARK), ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTNAME", (0, 0), (-1, 0), FONT_BOLD), ("FONTSIZE", (0, 0), (-1, 0), 8),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.5, GREY_LIGHT),
        ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            style_cmds.append(("BACKGROUND", (0, i), (-1, i), BG_PANEL))
    t.setStyle(TableStyle(style_cmds))
    return t

def grid_table(head_row, rows, col_widths, head_bg=NAVY):
    data = [[P(h, S_HEAD_W_C) for h in head_row]]
    for row in rows:
        data.append([P(c, S_CELL) for c in row])
    t = Table(data, colWidths=col_widths, repeatRows=1)
    style_cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), head_bg), ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTNAME", (0, 0), (-1, 0), FONT_BOLD), ("FONTSIZE", (0, 0), (-1, 0), 8),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.5, GREY_LIGHT),
        ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            style_cmds.append(("BACKGROUND", (0, i), (-1, i), BG_PANEL))
    t.setStyle(TableStyle(style_cmds))
    return t

def position_panel(text):
    return info_panel(P("<b>Position du GIHP :</b> " + text, S_BODY_SM), bg=BG_PANEL, border=TEAL)

TOTAL_PAGES = {"n": 4}

def on_page(canvas, doc, page_title):
    header_band(canvas, doc, "GIHP — REVUE DE LA LITTÉRATURE, 2019 (SANS COTATION)",
                "Tests viscoélastiques (TEG®/ROTEM®)",
                page_title, icon_fn=lambda c, x, y: icon_drop(c, x, y, 13 * mm), color=TEAL_DARK)
    footer_band(canvas, doc, SOURCE_TXT, f"Page {doc.page} / {TOTAL_PAGES['n']}")

# ---------------------------------------------------------------------------
def _section_intro_principes():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Résumé :</b> position du GIHP sur la place des tests viscoélastiques (TVE) — "
        "thromboélastographie (TEG®) et thromboélastométrie (ROTEM®) — tests globaux de "
        "coagulation sur sang total, dans la prise en charge de l'hémorragie en médecine "
        "d'urgence et périopératoire. Revue narrative de la littérature, <b>sans grille de "
        "cotation</b> (ni niveaux de preuve, ni grades) — chaque situation clinique aboutit à "
        "une position du GIHP formulée en prose, retranscrite intégralement dans cette fiche. "
        "Rôle établi en traumatologie sévère et en chirurgie cardiaque ; rôle encore à définir "
        "en transplantation hépatique, hémorragie du post-partum, chirurgie non cardiaque et "
        "pédiatrie.", S_BODY),
        bg=BG_PANEL, border=TEAL))
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("Principes des tests viscoélastiques"))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "Les TVE analysent les propriétés élastiques et visqueuses du sang total (tubes "
        "citratés, recalcifiés) tout au long des phases de la coagulation, influencées par le "
        "système fibrinolytique — contrairement aux tests classiques (TQ, TCA, fibrinogène) "
        "réalisés sur plasma pauvre en plaquettes. Leur sensibilité aux propriétés mécaniques "
        "du caillot intègre l'effet des plaquettes, leucocytes et érythrocytes. "
        "<b>TEG® et ROTEM® ne sont pas interchangeables</b> : un algorithme construit pour "
        "l'un ne peut pas être utilisé avec l'autre.", S_BODY_SM))
    story.append(Spacer(1, 1.5 * mm))
    story.append(theme_table([
        ("Paramètres communs", "R (TEG®, min) / CT (ROTEM®, s) : temps de latence avant "
         "début de coagulation. K (TEG®) / CFT (ROTEM®) : temps pour atteindre 20 mm "
         "d'amplitude. Angle α : cinétique de formation du caillot. MA (TEG®) / MCF "
         "(ROTEM®) : amplitude maximale = force maximale du caillot. A5/A10 (ROTEM®) : "
         "amplitude à 5/10 min. LY30/LY60 (TEG®) ou LI30/LI60 (ROTEM®) : indices de "
         "lyse à 30/60 min."),
        ("Réactifs TEG®", "Kaolin TEG (± héparinase, interprétable jusqu'à 6 UI/mL "
         "d'héparine) ; r-TEG (kaolin + facteur tissulaire, résultats plus rapides, "
         "fournit l'ACT) ; TEG FF (fibrinogène fonctionnel, via inhibition plaquettaire "
         "par abciximab)."),
        ("Réactifs ROTEM®", "NATEM (recalcification seule) ; NAHEPTEM (+ héparinase) ; "
         "INTEM (voie intrinsèque, acide ellagique) ; HEPTEM (neutralise jusqu'à "
         "7 UI/mL d'héparine) ; EXTEM (voie extrinsèque, facteur tissulaire "
         "recombinant) ; FIBTEM (fibrinogène, cytochalasine D) ; APTEM (discrimine "
         "fibrinolyse vs rétraction plaquettaire, aprotinine/acide tranexamique). "
         "EXTEM/FIBTEM/APTEM neutralisent jusqu'à 5 UI/mL d'héparine."),
        ("Limites techniques", "Coefficients de variation élevés et hétérogènes selon "
         "l'étude (2-14 % pour ROTEM® ; 7-83 % selon une étude multicentrique 2010). "
         "Absence de standardisation internationale des réactifs. Résultats à "
         "interpréter avec prudence chez le patient hypotherme (mesure à 37°C par "
         "défaut ; ROTEM® delta ajustable de 30 à 40°C). Corrélation imparfaite avec "
         "les tests de routine (TQ/TCA) — variable selon l'activateur et le contexte "
         "clinique."),
    ], [34 * mm, CW_FULL - 34 * mm]))
    return story

def _section_trauma():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("Traumatisme sévère"))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "L'hémorragie est la première cause de mortalité chez le traumatisé, compliquée dans "
        "25-30 % des cas d'une coagulopathie aiguë traumatique (CAT) qui multiplie la "
        "mortalité par 4. Les TVE prédisent le recours à la transfusion de CGR et la "
        "transfusion massive.", S_BODY_SM))
    story.append(Spacer(1, 1.5 * mm))
    story.append(theme_table([
        ("Seuils prédictifs — transfusion", "FIBTEM MCF &lt;7 mm prédictif de transfusion de "
         "CGR. EXTEM A5 &gt;35 mm : valeur prédictive négative de 83 % pour la transfusion "
         "de CGR (300 patients) et prédit la transfusion massive (AUC 0,80). r-TEG "
         "ACT &lt;105 s : facteur de risque indépendant d'absence de transfusion à 6h "
         "(OR 1,85 ; IC95 % 1,07-3,18) ; ACT &gt;128 s : facteur de risque indépendant de "
         "transfusion massive à 6h (OR 5,15 ; IC95 % 1,36-19,49). FIBTEM A5 ≤9 mm et "
         "EXTEM A5 ≤40 mm : valeur prédictive de transfusion massive (sensibilité 77,5 % "
         "et 72,2 %, 808 patients). Dans la plus grande cohorte publiée (1974 traumatisés), "
         "l'angle r-TEG prédisait mieux la transfusion massive que les tests de routine "
         "(p&lt;0,001)."),
        ("Seuils prédictifs — hypofibrinogénémie", "FIBTEM A10 ≤5 mm : sensibilité 91 %, "
         "spécificité 85 % pour un fibrinogène &lt;1 g/L. EXTEM A5 &lt;36 mm : sensibilité "
         "53 %, spécificité 87 % pour un fibrinogène &lt;1,5 g/L. Seuils consensuels dans "
         "la littérature (35-40 mm pour EXTEM A5, 8-10 mm pour FIBTEM A5, 7-10 mm pour "
         "FIBTEM MCF) mais encore trop tôt pour recommander des valeurs seuils fermes."),
        ("Hyperfibrinolyse", "Contribue à la CAT et aggrave le pronostic ; diagnostic "
         "difficile (les TVE manquent de sensibilité pour détecter l'activation de la "
         "fibrinolyse). Une lyse complète du caillot en &lt;60 min est prédictive d'une "
         "mortalité de 86 à 96 % selon les séries. L'étude CRASH-2 a montré que l'acide "
         "tranexamique systématique dans les 3 premières heures réduit la mortalité des "
         "traumatisés hémorragiques ; au-delà de 3h, le bénéfice est discutable, en "
         "particulier sans hyperfibrinolyse."),
    ], [38 * mm, CW_FULL - 38 * mm]))
    story.append(Spacer(1, 1.5 * mm))
    story.append(position_panel(
        "les TVE peuvent être utilisés pour le diagnostic précoce de la coagulopathie ; ils "
        "prédisent le besoin de transfusion en CGR ou le recours à une transfusion massive, "
        "et doivent guider le traitement hémostatique et sensibiliser l'équipe à la gravité "
        "du traumatisme. En raison de leur faible sensibilité pour diagnostiquer "
        "l'activation de la fibrinolyse, <b>les TVE ne doivent pas guider l'administration "
        "d'acide tranexamique</b> — celui-ci doit être administré le plus tôt possible ; en "
        "revanche, la détection d'une hyperfibrinolyse par TVE reste un prédicteur de "
        "mortalité. Les TVE doivent être inclus dans des algorithmes locaux, avec des seuils "
        "pré-établis pour guider produits sanguins labiles et concentrés de facteurs — des "
        "études prospectives multicentriques restent nécessaires."))
    return story

def _section_hpp_cardiaque():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("Hémorragie du post-partum (HPP)"))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "L'HPP reste une cause majeure de morbi-mortalité maternelle (~30 % des décès "
        "maternels directs, ~150 000 décès/an dans le monde). Une coagulopathie est observée "
        "dans plus de 20 % des accouchements compliqués. Un fibrinogène ≤2 g/L au diagnostic "
        "d'HPP a une valeur prédictive de 100 % d'HPP sévère (128 patientes sous "
        "prostaglandine E2).", S_BODY_SM))
    story.append(Spacer(1, 1.5 * mm))
    story.append(theme_table([
        ("FIBTEM et fibrinogène", "FIBTEM A5/A15/MCF fortement corrélés au fibrinogène "
         "mesuré au laboratoire (r=0,86 / 0,84 / 0,85 ; 37 patientes). Seuil FIBTEM A5 "
         "&lt;6 mm ou A15 &lt;8 mm : sensibilité excellente (100 %) mais spécificité plus "
         "faible (87 %/84 %) pour un fibrinogène &lt;2 g/L. FIBTEM A5 &lt;10 mm associé à "
         "la progression du saignement (356 patientes). FIBTEM A5 &lt;12 mm : seuil sous "
         "lequel l'administration de fibrinogène réduit transfusion et saignement "
         "(55 patientes)."),
        ("Fibrinolyse & acide tranexamique", "L'activité fibrinolytique diminue pendant la "
         "grossesse puis s'accélère dans l'heure suivant l'accouchement (pic à 3h "
         "post-partum), davantage en cas d'HPP. L'étude WOMAN confirme la réduction des "
         "décès maternels par hémorragie et des laparotomies d'hémostase par l'acide "
         "tranexamique, en particulier administré précocement ; bénéfice plus discutable "
         "au-delà de la 3e heure."),
    ], [38 * mm, CW_FULL - 38 * mm]))
    story.append(Spacer(1, 1.5 * mm))
    story.append(position_panel(
        "en cas d'HPP, la concentration de fibrinogène doit être rapidement évaluée et les "
        "TVE peuvent y être utiles. Compte tenu des limites des TVE dans l'évaluation de "
        "l'activité fibrinolytique, il est proposé de <b>ne pas guider l'administration "
        "d'acide tranexamique sur les TVE</b> mais de l'administrer le plus tôt possible en "
        "cas d'HPP."))
    story.append(Spacer(1, 2.5 * mm))
    story.append(section_bar("Chirurgie cardiaque"))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "Situation la plus étudiée pour les TVE : causes multiples d'hémorragie (chirurgie "
        "complexe, traitement antiplaquettaire/anticoagulant préopératoire, héparine "
        "résiduelle malgré la protamine, consommation/dilution des facteurs et plaquettes). "
        "Utilisation classique après neutralisation de l'héparine par la protamine et retour "
        "aux conditions optimales de température/pH/calcium ionisé ; usage plus systématique "
        "proposé en cas de risque hémorragique élevé (reprise chirurgicale, assistance "
        "circulatoire, transplantation).", S_BODY_SM))
    story.append(Spacer(1, 1.5 * mm))
    story.append(theme_table([
        ("Méta-analyse (Deppe et al., 8332 patients, 17 études)", "Réduction du recours "
         "transfusionnel dans le bras guidé par TVE (OR 0,63 ; IC95 % 0,56-0,71 ; "
         "confirmée dans le sous-groupe randomisé, OR 0,37 ; IC95 % 0,21-0,68), "
         "concernant surtout le plasma frais congelé (OR 0,31 ; IC95 % 0,13-0,74). "
         "Réduction significative de l'insuffisance rénale aiguë, des événements "
         "thromboemboliques et des reprises pour saignement postopératoire. Résultats "
         "concordants avec la méta-analyse de Bolliger &amp; Tanaka (2013, 12 études dont "
         "7 randomisées), qui retrouve en l'absence de guidage par TVE une "
         "sur-prescription de concentrés de fibrinogène (OR 1,56) et de CCP (OR 1,74)."),
        ("Méta-analyse Cochrane 2016 (1493 patients, 17 études)", "Réduction "
         "significative des transfusions de CGR (RR 0,86 ; IC95 % 0,79-0,94), PFC "
         "(RR 0,57 ; IC95 % 0,33-0,96) et plaquettes (RR 0,73 ; IC95 % 0,60-0,88), et "
         "réduction significative de la <b>mortalité</b> (RR 0,52 ; IC95 % 0,28-0,95 ; "
         "surtout portée par les essais ROTEM®, RR 0,44 ; IC95 % 0,21-0,93) et de "
         "l'insuffisance rénale aiguë avec dialyse (RR 0,46 ; IC95 % 0,28-0,76) — niveau "
         "de preuve faible (hétérogénéité, faibles effectifs)."),
        ("Étude randomisée Karkouti et al. (12 centres, 7402 patients)", "L'utilisation "
         "du ROTEM® (algorithme EXTEM CT/A10 + FIBTEM A10 + test plaquettaire) a réduit "
         "la transfusion de CGR (RR 0,91 ; IC95 % 0,85-0,98) et de plaquettes (RR 0,77 ; "
         "IC95 % 0,68-0,87) — <b>mais pas</b> celle de plasma ou de concentrés de "
         "facteurs (fibrinogène, cryoprécipité, CCP) — et l'hémorragie majeure, sans "
         "impact sur les complications, la durée d'hospitalisation ou la mortalité."),
    ], [42 * mm, CW_FULL - 42 * mm]))
    story.append(Spacer(1, 1.5 * mm))
    story.append(position_panel(
        "en chirurgie cardiaque, les TVE doivent être utilisés en cas d'hémorragie en fin "
        "d'intervention et en postopératoire — réalisés essentiellement en fin de CEC, après "
        "neutralisation de l'héparine, pour guider la stratégie thérapeutique. Ils doivent "
        "être inclus dans des algorithmes."))
    return story

def _section_lt_pediatrie_bedside():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("Transplantation hépatique (TH)"))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "Les tests de coagulation de routine (TQ notamment) ne prédisent ni le risque "
        "hémorragique ni le risque thrombotique chez le cirrhotique — ils n'évaluent que les "
        "facteurs pro-coagulants sans tenir compte des systèmes inhibiteurs de la "
        "coagulation, d'où un « nouvel équilibre » hémostatique plus ténu mais souvent "
        "préservé. Plusieurs études montrent l'intérêt des TVE pour réduire le recours "
        "transfusionnel en TH.", S_BODY_SM))
    story.append(Spacer(1, 1.5 * mm))
    story.append(theme_table([
        ("Corrélation FIBTEM/fibrinogène", "Bonne corrélation entre FIBTEM A10 et le "
         "fibrinogène mesuré, permettant un résultat rapide — mais précision "
         "insuffisante en cas de déficit majeur (fibrinogène &lt;1 g/L)."),
        ("Hyperfibrinolyse", "Cause majeure de saignement non chirurgical en TH. "
         "L'hyperfibrinolyse pré-anhépatique détectée par ROTEM® est associée à une "
         "surmortalité à 30 jours et 6 mois ; l'hyperfibrinolyse post-anhépatique est "
         "associée à un risque accru de thrombose porte/artère hépatique. "
         "L'administration systématique d'antifibrinolytique ne semble pas "
         "nécessaire."),
    ], [40 * mm, CW_FULL - 40 * mm]))
    story.append(Spacer(1, 1.5 * mm))
    story.append(position_panel(
        "les TVE peuvent aider en TH à limiter la transfusion de produits sanguins labiles, "
        "probablement au prix d'une augmentation de la transfusion de fibrinogène. Les TVE "
        "manquant de sensibilité pour le diagnostic d'hyperfibrinolyse, il est proposé de "
        "<b>ne pas attendre l'apparition d'un tracé typique d'hyperfibrinolyse</b> pour "
        "utiliser des antifibrinolytiques si d'autres signes cliniques sont présents "
        "(saignement diffus ou massif)."))
    story.append(Spacer(1, 2.5 * mm))
    story.append(section_bar("Pédiatrie", color=AMBER))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "Peu d'études centrées sur la gestion transfusionnelle de l'hémorragie chirurgicale "
        "chez l'enfant. Chez le nouveau-né, les TVE montrent un profil hypercoagulable "
        "(contrairement aux tests de routine, qui suggèrent une hypocoagulation) jusqu'à "
        "6 mois — vérifier les valeurs de référence locales du fait de l'hétérogénéité des "
        "conditions de réalisation entre études. La chirurgie cardiaque est le contexte le "
        "plus étudié, avec des résultats contradictoires sur la valeur prédictive "
        "préopératoire des TVE ; les algorithmes transfusionnels varient fortement d'un "
        "centre à l'autre. Données très éparses pour les autres chirurgies (TH : une seule "
        "étude descriptive ; polytraumatisme pédiatrique : études rétrospectives "
        "uniquement).", S_BODY_SM))
    story.append(Spacer(1, 1.5 * mm))
    story.append(info_panel(P(
        "<b>Absence de position propre du GIHP</b> (disclosed) : la source ne formule "
        "aucune proposition GIHP en pédiatrie, faute d'études suffisantes pour définir le "
        "rôle des TVE dans la prise en charge périopératoire de l'enfant. Elle cite "
        "uniquement une recommandation <b>externe</b> — Société Européenne "
        "d'Anesthésiologie (ESA, Kozek-Langenecker et al., 2013) — suggérant l'usage des TVE "
        "pour détecter rapidement une coagulopathie de dilution ou une hyperfibrinolyse "
        "(<b>grade 2C</b>, grille de cotation propre à l'ESA, distincte de toute position "
        "GIHP).", S_BODY_SM), bg=AMBER_LIGHT, border=AMBER))
    story.append(Spacer(1, 2.5 * mm))
    story.append(section_bar("Positionnement : chevet ou laboratoire ?", color=GREY))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "Le délai d'obtention des tests de routine est présenté comme un facteur limitant "
        "majeur (étude Cotton et al. : 48 min pour les tests de routine vs 15 min pour le "
        "r-TEG). Les paramètres précoces (A5/A10) permettent de réduire encore ce délai. En "
        "France, les dispositifs sont répartis de façon équilibrée entre bloc opératoire et "
        "laboratoire d'hémostase — le choix dépend de l'organisation et des ressources "
        "locales, dans le respect de la réglementation sur la biologie délocalisée.",
        S_BODY_SM))
    story.append(Spacer(1, 1.5 * mm))
    story.append(theme_table([
        ("Critères décisifs", "Le délai d'obtention des résultats est-il compatible avec "
         "la prise en charge optimale du patient hémorragique ? Les ressources "
         "informatiques sont-elles disponibles ? Application de la réglementation sur "
         "la biologie délocalisée si le dispositif est au bloc ; visualisation en temps "
         "réel des tracés sur écrans si positionné au laboratoire."),
        ("Personnel", "Au bloc : nombre de personnes à former, turnover du personnel, "
         "désignation par le biologiste de responsables de maintenance/suivi. Au "
         "laboratoire : disponibilité du personnel 24h/24 pour le prélèvement et "
         "l'utilisation immédiats du TVE."),
    ], [34 * mm, CW_FULL - 34 * mm]))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<i>Nouveaux dispositifs :</i> le TEG® 6s et le ROTEM® Sigma, entièrement "
        "automatisés (cartouches, sans pipetage manuel), simplifient l'utilisation et sont "
        "davantage adaptés à la biologie délocalisée — mais peu d'études disponibles à ce "
        "jour, valeurs de référence et seuils encore à valider. Le choix et la mise en "
        "œuvre d'un TVE ne peuvent se faire que de façon consensuelle entre service clinique "
        "et laboratoire.", S_NOTE))
    return story

def _section_conclusion_sources():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("Conclusion (source)", color=GREY))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "Les TVE doivent être inclus dans des algorithmes de prise en charge de la "
        "coagulopathie et de l'hémorragie, définis dans chaque centre et pour chaque "
        "population de patients. Si leur intérêt en traumatologie et en chirurgie cardiaque "
        "paraît établi, les études de haut niveau de preuve manquent encore en obstétrique, "
        "transplantation hépatique et pédiatrie. En concertation avec le laboratoire de "
        "biologie, le positionnement de ces dispositifs doit être adapté au fonctionnement "
        "de chaque centre.", S_BODY_SM))
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("Sources et traçabilité", color=GREY))
    story.append(Spacer(1, 2 * mm))
    story.append(P(
        "<b>Document source :</b> Roullet S, de Maistre E, Ickx B, Blais N, Susen S, Faraoni "
        "D, Garrigue D, Bonhomme F, Godier A, Lasne D, et le GIHP. « Position of the French "
        "Working Group on Perioperative Haemostasis (GIHP) on viscoelastic tests: What role "
        "for which indication in bleeding situations? » Anaesth Crit Care Pain Med "
        "2019;38:539-548 (en ligne le 03/02/2018). Article en libre accès (CC BY-NC-ND), "
        "publié par Elsevier Masson SAS pour la Sfar.", S_SOURCE))
    story.append(Spacer(1, 1 * mm))
    story.append(P("<b>Méthodologie :</b> revue narrative de la littérature, sans grille de "
                    "cotation — voir détail en page 1.", S_SOURCE))
    story.append(Spacer(1, 1 * mm))
    story.append(P(
        "<b>URL source :</b> https://sfar.org/download/tests-viscoelastiques-2018/"
        "?wpdmdl=34421", S_SOURCE))
    story.append(Spacer(1, 1 * mm))
    story.append(P(
        "<b>Couverture :</b> intégralité des 9 positions du GIHP explicitement formulées "
        "(« The GIHP proposes… ») dans les 4 situations cliniques où la source en énonce "
        "une (traumatisme sévère, HPP, chirurgie cardiaque, transplantation hépatique), plus "
        "la section pédiatrie (absence de position propre disclosed) et le positionnement "
        "bedside/laboratoire. <b>Portée partielle disclosed (règle 5) :</b> au-delà des "
        "positions GIHP elles-mêmes (100 % couvertes) et des seuils/méta-analyses "
        "directement actionnables retenus, l'argumentaire complet — dizaines d'études "
        "isolées citées à l'appui, intervalles de confiance secondaires, 128 références "
        "bibliographiques — est condensé, pas intégralement repris ; se référer au texte "
        "source pour le détail étude-par-étude.", S_SOURCE))
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Avertissement — article publié 2018/2019 :</b> cette fiche de synthèse "
        "indépendante, traduite et condensée de l'anglais, reprend l'intégralité des "
        "positions du GIHP mais ne remplace pas le texte source et n'est ni éditée ni "
        "validée par la SFAR ou le GIHP. Se référer au texte intégral (et à la littérature "
        "plus récente, cet article datant de 2018) pour toute décision clinique.", S_BODY_SM),
        bg=GREY_LIGHT, border=GREY))
    return story

SECTIONS = [
    ("Principes, traumatisme, HPP, chirurgie cardiaque, TH, pédiatrie & sources",
     lambda: _section_intro_principes() + _section_trauma() + _section_hpp_cardiaque()
     + _section_lt_pediatrie_bedside() + _section_conclusion_sources()),
]

def _make_doc(path=None):
    return SimpleDocTemplate(path or OUT, pagesize=A4,
                              leftMargin=MARGIN, rightMargin=MARGIN,
                              topMargin=32 * mm, bottomMargin=16 * mm,
                              title="Fiche GIHP 2019 - Tests viscoelastiques",
                              author="Synthèse indépendante (source GIHP/Sfar)")

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

    doc = _make_doc()
    story = _build_upto(fns)
    doc.build(story, onFirstPage=on_page_final, onLaterPages=on_page_final)
    print("OK ->", OUT, f"({total_pages} pages)")

if __name__ == "__main__":
    build()
