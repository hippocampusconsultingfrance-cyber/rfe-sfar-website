# -*- coding: utf-8 -*-
"""
Fiche de synthese - Conclusions de la table ronde organisee par l'EFS sur
« Le traitement des urgences transfusionnelles obstetricales » (table ronde
reunie le 26 septembre 2000 ; texte finalise/date sur chaque page 21/12/01 et
07/06/01 ; mis en ligne sur sfar.org le 29/09/2015, article WordPress
"datePublished":"2015-09-29"). Soumis pour avis a la SFAR, au College des
Obstetriciens, aux Directeurs d'etablissement de l'EFS et a la Societe
Francaise de Transfusion Sanguine (SFTS). PDF source : 7 pages, aucune pagination
figee (Tableau I + liste d'items en fin de document).

DIVERGENCE / INCOHERENCE SOURCE DISCLOSUREE (ne pas resoudre silencieusement) :
`build/library_final.json` (item index 139) intitule ce document "Hemorragies
du post-partum immediat" avec `exact_date: "2014"` alors que (a) le href et le
direct_pdf_url de CE MEME item pointent vers ce document precis (verifie :
needle "urgences-transfusionnelles-obstetricales" trouve exactement 1 entree
dans href, needle "Traitement-des-urgences-transfusionnelles-obstetricales"
trouve exactement 1 entree dans direct_pdf_url), (b) le contenu du PDF
lui-meme est une table ronde EFS datee 2000/2001 (aucune mention "2014" nulle
part dans le texte), et (c) la page sfar.org qui l'heberge affiche
datePublished 2015-09-29. Aucune version 2014 alternative n'a ete trouvee sur
la page source (un seul PDF lie, verifie par grep de tous les liens .pdf de la
page). Les trois dates (library_final.json "2014", table ronde "2000/2001",
mise en ligne sfar.org "2015") sont disclosees telles quelles ci-dessous, sans
deviner laquelle est "la bonne". Vu l'age reel du contenu (~25 ans), ce
document est traite comme `revision_detectee` cote migration (meme convention
que hsa/0023, eclsa/0019, glycemie/0022, voies_aeriennes_adulte/0060), malgre
un statut `library_final.json` "en vigueur".

METHODOLOGIE : PAS de systeme GRADE, PAS de cotation RAND/UCLA, PAS de vote
chiffre, PAS d'echelle ANAES. C'est une synthese de "conclusions" d'une table
ronde d'experts multidisciplinaire (immuno-hematologistes, anesthesistes-
reanimateurs, obstetriciens, transfuseurs) : chaque proposition du texte est
imprimee en prose continue, SANS aucun tag de force/preuve individuel. Aucun
chip de grade n'est donc invente nulle part dans cette fiche (contrairement
a la quasi-totalite du corpus SFAR/SRLF) : reproduire un GRADE_COLORS
inexistant dans la source serait une fabrication interdite par la regle 4 du
standing quality bar. Les propositions sont presentees ici en tableaux
thematiques (2 colonnes : Theme / Contenu) et listes a puces fideles a la
structure ES / ST / ES+ST du texte source (sections III-1/III-2/III-3), sans
colonne de grade.

COUVERTURE : integralite des 4 chapitres du corps du texte (I. Definition des
niveaux d'urgence ; II. Regles de surveillance immuno-hematologique de la
grossesse ; III. Propositions d'organisation, ES / ST / ES+ST ; IV.
Evaluation et suivi des actions), plus le Tableau I (procedure d'urgence
vitale, reproduit integralement comme sequence de tableaux) et la "Liste des
items" (checklist de procedure generale, en fin de document). Les 8
references bibliographiques du texte source sont citees dans Sources et
tracabilite (pas de PDF a part reproduire).
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from style import *
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.units import mm

OUT = os.path.join(os.path.dirname(__file__), "..", "output",
                    "Fiche_SFAR_EFS_Urgences_Transfusionnelles_Obstetricales_2001.pdf")
OUT = os.path.abspath(OUT)

SOURCE_TXT = ("Source : Conclusions de la table ronde organisée par l'Établissement Français du "
              "Sang (EFS) — « Le traitement des urgences transfusionnelles obstétricales » (table "
              "ronde du 26/09/2000, texte daté 21/12/01-07/06/01, mis en ligne sfar.org 2015). "
              "Soumis pour avis à la SFAR, au Collège des Obstétriciens, aux Directeurs "
              "d'établissement de l'EFS et à la SFTS. Fiche de synthèse non officielle : se "
              "référer au texte intégral.")


def P(txt, style=S_CELL):
    return Paragraph(txt, style)


def theme_table(rows, col_widths, header=("Theme", "Contenu")):
    """rows: (theme, text) — pas de colonne de grade : cette source n'imprime AUCUN tag de
    force/preuve individuel (voir docstring du module), donc aucune colonne d'accord/grade
    n'est ajoutee ici (a la difference du theme_table() a 3 colonnes utilise par les fiches
    GIHP/GFHT qui, elles, impriment "(accord fort)")."""
    data = [[P(header[0], S_HEAD_W), P(header[1], S_HEAD_W)]]
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


def simple_table(header, rows, col_widths):
    data = [[P(h, S_HEAD_W) for h in header]]
    for r in rows:
        data.append([P(c, S_CELL) for c in r])
    t = Table(data, colWidths=col_widths, repeatRows=1)
    st = [
        ("BACKGROUND", (0, 0), (-1, 0), TEAL_DARK), ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTNAME", (0, 0), (-1, 0), FONT_BOLD), ("FONTSIZE", (0, 0), (-1, 0), 8),
        ("GRID", (0, 0), (-1, -1), 0.5, GREY_LIGHT), ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 3.2), ("BOTTOMPADDING", (0, 0), (-1, -1), 3.2), ("LEFTPADDING", (0, 0), (-1, -1), 5),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            st.append(("BACKGROUND", (0, i), (-1, i), BG_PANEL))
    t.setStyle(TableStyle(st))
    return t


def bullet_list(items, style=S_BODY_SM):
    """items: list of html-formatted strings. Reproduces the source's own '-'/bullet-point
    structure (sections III-1/III-2/III-3) without inventing numbering the source doesn't
    use."""
    html = "<br/><br/>".join("• " + it for it in items)
    return P(html, style)


TOTAL_PAGES = {"n": 6}


def on_page(canvas, doc, page_title):
    header_band(canvas, doc, "EFS / SFAR (POUR AVIS) — TABLE RONDE 2000-2001 — FICHE DE SYNTHÈSE",
                "Urgences transfusionnelles obstétricales",
                page_title, icon_fn=lambda c, x, y: icon_drop(c, x, y, 13 * mm), color=NAVY)
    footer_band(canvas, doc, SOURCE_TXT, f"Page {doc.page} / {TOTAL_PAGES['n']}")


# ---------------------------------------------------------------------------
def _section_intro():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Champ :</b> organisation de la réponse transfusionnelle à l'hémorragie du "
        "péripartum — définition de niveaux d'urgence, surveillance immuno-hématologique de "
        "la grossesse, et propositions d'organisation entre établissement de santé (ES) et "
        "site transfusionnel (ST). Conclusions d'une <b>table ronde EFS</b> réunie le "
        "26 septembre 2000, réunissant gynécologues-obstétriciens, anesthésistes-réanimateurs, "
        "biologistes et spécialistes des produits sanguins.<br/><br/>"
        "<b>Épidémiologie (texte source) :</b> en obstétrique, l'hémorragie du péripartum est "
        "la <b>1<sup rise=\"2\" size=\"6\">re</sup> cause de mortalité maternelle en France "
        "(33 %)</b>. L'incidence des transfusions en péripartum est faible (1 à 2,5 % pour "
        "les accouchements par voie basse ; 3,1 à 5 % pour les césariennes), mais "
        "l'hémorragie survient de façon imprévisible et, dans <b>84 % des cas</b>, chez des "
        "femmes sans facteur de risque particulier (en dehors de placenta prævia, hématome "
        "rétro-placentaire, multiparité…).",
        S_BODY), bg=BG_PANEL, border=TEAL))
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Méthodologie — absence de grading (disclosure) :</b> ce document ne comporte "
        "<b>aucun système de gradation</b> (ni GRADE, ni cotation RAND/UCLA, ni vote chiffré, "
        "ni échelle ANAES) : chaque proposition est imprimée en prose continue par le groupe "
        "d'experts, sans tag de force ou de niveau de preuve individuel. Aucun chip de grade "
        "n'est donc utilisé dans cette fiche — en inventer un serait fabriquer une information "
        "absente de la source.",
        S_BODY_SM), bg=AMBER_LIGHT, border=AMBER))
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Incohérence de métadonnées disclosurée :</b> l'index interne du projet "
        "(`library_final.json`) intitule cet item « Hémorragies du post-partum immédiat » "
        "avec une date « 2014 ». Le href et le PDF source de ce même item pointent "
        "pourtant, vérification faite (correspondance unique), vers CE document précis — dont "
        "le contenu intégral est daté 2000 (table ronde) / 2001 (texte finalisé, tamponné "
        "« 21/12/01 » et « 07/06/01 » sur chaque page), mis en ligne sur sfar.org le "
        "29/09/2015 (métadonnée « datePublished » de la page). Aucune mention « 2014 » "
        "n'apparaît nulle part dans le texte, et aucune autre version PDF n'est liée depuis la "
        "page source (vérifié). Les trois dates (2014 index / 2000-2001 contenu / 2015 mise en "
        "ligne) sont rapportées ici telles quelles, sans qu'aucune ne soit écartée par "
        "supposition.",
        S_BODY_SM), bg=RED_LIGHT, border=RED))
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("Deux types de risque (texte source)"))
    story.append(Spacer(1, 2 * mm))
    story.append(theme_table([
        ("Risque immunologique", "Lié au passage d'hématies fœtales pendant la grossesse. "
         "Impose une gestion des analyses immuno-hématologiques adaptée à ces urgences, en "
         "particulier la recherche d'anticorps anti-érythrocytaires (agglutinines "
         "irrégulières, RAI)."),
        ("Risque lié au retard à la transfusion", "Dans certains cas en péripartum, la "
         "disponibilité des produits sanguins labiles (PSL) doit être immédiate. Malgré "
         "l'existence de textes réglementaires pour la périnatologie, l'analyse des "
         "prescriptions de PSL et des examens d'immuno-hématologie, comme les modalités de la "
         "distribution en urgence, montrent une grande hétérogénéité des pratiques."),
    ], [40 * mm, PAGE_W - 2 * MARGIN - 40 * mm]))
    story.append(Spacer(1, 2 * mm))
    story.append(P(
        "<i>Les recommandations qui suivent sont regroupées en quatre chapitres, comme dans le "
        "texte source : I. définition de niveaux d'urgence ; II. règles de surveillance "
        "immuno-hématologique de la grossesse ; III. propositions pour répondre à l'urgence "
        "vitale transfusionnelle ; IV. évaluation et suivi des actions.</i>", S_NOTE))
    return story


def _section_niveaux():
    story = []
    story.append(Spacer(1, 2 * mm))
    story.append(KeepTogether([
        section_bar("I — Définition des niveaux d'urgence"),
        Spacer(1, 2 * mm),
        P("Pour permettre une bonne communication entre l'établissement de soin et le site "
          "transfusionnel, il convient de distinguer, selon la brutalité de survenue et la "
          "gravité du saignement, trois niveaux d'urgence, et d'en mesurer les conséquences en "
          "matière de distribution :", S_BODY_SM),
        Spacer(1, 2 * mm),
        simple_table(
            ["Niveau d'urgence", "Délai d'obtention des PSL", "Modalités"],
            [
                ["Urgence vitale immédiate (UVI)", "Sans délai",
                 "Les CGR sont distribués immédiatement, éventuellement sans groupe sanguin "
                 "s'il n'est pas disponible. La prescription le mentionne ; les prélèvements "
                 "pour les analyses immuno-hématologiques sont acheminés dès que possible."],
                ["Urgence vitale (UV)", "&lt; 30 minutes",
                 "Les CGR sont distribués avec un groupe conforme, éventuellement sans RAI si "
                 "l'examen n'est pas disponible. La prescription le mentionne, les échantillons "
                 "l'accompagnent. La RAI est réalisée dès que possible."],
                ["Transfusion urgente", "2 à 3 heures, le plus souvent",
                 "Permet la réalisation de l'ensemble des examens immuno-hématologiques (dont la "
                 "RAI si elle date de plus de 3 jours) et l'obtention de PSL isogroupes et, au "
                 "besoin, compatibilisés."],
            ],
            [36 * mm, 28 * mm, PAGE_W - 2 * MARGIN - 36 * mm - 28 * mm]),
        Spacer(1, 1.5 * mm),
        P("<i>La situation hémorragique pouvant se modifier à tout moment, il est possible de "
          "requalifier le niveau de l'urgence à tout instant.</i>", S_NOTE),
    ]))
    return story


def _section_surveillance():
    story = []
    story.append(Spacer(1, 2 * mm))
    story.append(KeepTogether([
        section_bar("II — Surveillance immuno-hématologique de la grossesse"),
        Spacer(1, 2 * mm),
        P("<b>Principe :</b> le risque hémorragique se situant au moment de l'accouchement, il "
          "convient de prévoir, pendant les différentes consultations prénatales, l'ensemble "
          "des analyses biologiques nécessaires à la sécurité transfusionnelle (typage "
          "érythrocytaire, recherche d'anticorps anti-érythrocytaires), en tenant compte du "
          "fait que le risque de passages fœto-placentaires se situe en fin de gestation "
          "(situation privilégiée d'immunisation).", S_BODY_SM),
    ]))
    story.append(Spacer(1, 2 * mm))
    story.append(KeepTogether([
        P("<b>II-1 — Typage érythrocytaire</b>", S_H2),
        Spacer(1, 1 * mm),
        P("Les recommandations du décret n°92-143 sont jugées bien adaptées : pour une première "
          "grossesse, lors du premier examen prénatal (3<sup rise=\"2\" size=\"6\">e</sup> "
          "mois), si la patiente ne possède pas de carte de groupe sanguin complète avec un "
          "phénotype Rh et Kell, une première détermination des groupes sanguins ABO, Rh et "
          "Kell est réalisée, puis une deuxième détermination lors du 8<sup rise=\"2\" "
          "size=\"6\">e</sup> (6<sup rise=\"2\" size=\"6\">e</sup> examen prénatal) ou "
          "9<sup rise=\"2\" size=\"6\">e</sup> mois (7<sup rise=\"2\" size=\"6\">e</sup> examen "
          "prénatal) de grossesse, si nécessaire.", S_BODY_SM),
    ]))
    story.append(Spacer(1, 2 * mm))
    story.append(P("<b>II-2 — Recherche d'anticorps anti-érythrocytaires (RAI) — dépistage</b>", S_H2))
    story.append(Spacer(1, 1 * mm))
    story.append(theme_table([
        ("RhD négatif (± ATCD transfusionnel) ou RhD positif avec ATCD transfusionnel/obstétrical",
         "Surveillance du décret n° 92-143 jugée bien adaptée : RAI lors du 3<sup rise=\"2\" "
         "size=\"6\">e</sup> mois (1er examen prénatal), puis aux 6<sup rise=\"2\" "
         "size=\"6\">e</sup> (4<sup rise=\"2\" size=\"6\">e</sup> examen), 8<sup rise=\"2\" "
         "size=\"6\">e</sup> (6<sup rise=\"2\" size=\"6\">e</sup> examen) et 9<sup rise=\"2\" "
         "size=\"6\">e</sup> mois (7<sup rise=\"2\" size=\"6\">e</sup> examen)."),
        ("RhD positif, sans antécédent transfusionnel",
         "RAI au moins à 2 reprises avant l'accouchement (Arrêté du 19/04/1985 + décret "
         "n°92-143, synthèse ANAES) : avant la fin du 3<sup rise=\"2\" size=\"6\">e</sup> mois "
         "(1er examen) et au cours du 8<sup rise=\"2\" size=\"6\">e</sup> ou 9<sup rise=\"2\" "
         "size=\"6\">e</sup> mois (6<sup rise=\"2\" size=\"6\">e</sup>/7<sup rise=\"2\" "
         "size=\"6\">e</sup> examen), avec une préférence au 9<sup rise=\"2\" size=\"6\">e</sup> "
         "mois si la 1re recherche était négative (fréquence des hémorragies fœto-maternelles "
         "au 3<sup rise=\"2\" size=\"6\">e</sup> trimestre)."),
        ("RhD positif, sans ATCD transfusionnel, mais manœuvres obstétricales à risque",
         "Ponction amniotique, chute ou traumatisme, décollement d'un placenta normalement ou "
         "anormalement inséré… : il convient d'évaluer au cas par cas l'opportunité d'une RAI "
         "supplémentaire."),
        ("Surveillance en post-partum",
         "Une grossesse étant considérée comme un épisode transfusionnel (transfusion in "
         "utero), la surveillance de la survenue d'une immunisation secondaire par une RAI "
         "« serait à préconiser » — point jugé <b>insuffisamment documenté par la source "
         "elle-même</b>, « à confirmer par une étude prospective sur la surveillance des "
         "immunisations post-natales chez la femme RhD positif » (disclosure : la source "
         "signale elle-même cette incertitude, non résolue ici)."),
    ], [58 * mm, PAGE_W - 2 * MARGIN - 58 * mm]))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>II-2-2 — Identification :</b> en cas de dépistage positif, une identification et un "
        "titrage des anticorps sont immédiatement réalisés ; le rythme des examens ultérieurs "
        "est décidé en fonction de la spécificité, du titre et de la concentration des "
        "anticorps.", S_NOTE))
    return story


def _section_organisation_es_st():
    story = []
    story.append(Spacer(1, 2 * mm))
    story.append(section_bar("III — Propositions d'organisation"))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<i>Afin d'améliorer la réponse à l'urgence, le texte précise les modalités qui "
        "reviennent soit à l'établissement de santé (ES), soit au site transfusionnel (ST), "
        "soit à l'ensemble des deux, en gardant à l'esprit que tout défaut de communication "
        "peut aggraver le risque.</i>", S_NOTE))
    story.append(Spacer(1, 2 * mm))
    story.append(P("<b>III-1 — Ce qui revient à l'établissement de santé (ES)</b>", S_H2))
    story.append(Spacer(1, 1 * mm))
    story.append(bullet_list([
        "<b>Disposer des résultats au moment opportun</b> dès l'entrée de la femme en salle de "
        "travail, en vérifiant la conformité de tous les documents nécessaires à une "
        "transfusion (carte de groupe sanguin complète, résultat de la RAI du dernier examen "
        "prénatal). La meilleure solution serait la disponibilité des résultats par "
        "transmission informatique, réalisant la compatibilité électronique avec la "
        "distribution des PSL.",
        "<b>Avertir le site transfusionnel (ST)</b> du caractère de l'urgence (UVI, UV ou "
        "urgence transfusionnelle classique) afin que toutes les procédures soient mises en "
        "œuvre immédiatement — par exemple identification claire de l'urgence vitale sur la "
        "fiche de prescription accompagnée d'un appel téléphonique, transmission d'un fax "
        "complétée d'un appel téléphonique, etc.",
        "<b>Avertir le ST en cas de RAI positive</b>, afin que des produits sanguins "
        "compatibles soient préparés le plus rapidement possible en vue d'une éventuelle "
        "transfusion.",
        "<b>Dépister les usurpations d'identité</b> et, en cas de doute, contrôler sur de "
        "nouveaux échantillons, notamment pour les patientes prises en charge en urgence et "
        "n'ayant pas fait l'objet d'un contrôle de groupe sanguin en cours de grossesse.",
    ]))
    story.append(Spacer(1, 3 * mm))
    story.append(P("<b>III-2 — Ce qui revient au site transfusionnel (ST)</b>", S_H2))
    story.append(Spacer(1, 1 * mm))
    story.append(bullet_list([
        "<b>Reconnaître les prescriptions</b> de PSL relevant d'une UVI, d'une UV ou d'une "
        "transfusion urgente et y répondre par une distribution adéquate : distribution "
        "immédiate, distribution différée (sang préparé mais gardé en réserve au ST), ou "
        "acheminement de précaution vers le dépôt (pose le problème des produits inutilisés — "
        "réflexion spécifique nécessaire, non tranchée par la source).",
        "<b>Mettre en route les examens immuno-hématologiques</b> dès réception des "
        "échantillons, en communiquant les résultats au prescripteur le plus rapidement "
        "possible. Le prélèvement de la RAI (&lt; 3 jours) doit permettre de mettre en évidence "
        "un anticorps d'apparition récente, même si la RAI de fin de grossesse diminue déjà le "
        "risque immunologique.",
        "<b>Réaliser une association informatique</b> combinant les résultats "
        "immuno-hématologiques et les produits distribués par le ST — transfert informatique "
        "des données validées du laboratoire vers le service de distribution ; en cas de "
        "prise en compte manuelle de résultats issus d'un autre laboratoire, ces données "
        "doivent obligatoirement répondre aux critères réglementaires en vigueur.",
        "<b>Prendre en compte un résultat de RAI négatif</b> réalisé dans un autre laboratoire "
        "que celui du site distributeur, dès lors que l'analyse a été réalisée selon les "
        "critères réglementaires.",
    ]))
    return story


def _section_organisation_commune():
    story = []
    story.append(Spacer(1, 2 * mm))
    story.append(P("<b>III-3 — Ce qui revient à la fois à l'établissement de soins et au site "
                    "transfusionnel</b>", S_H2))
    story.append(Spacer(1, 1 * mm))
    story.append(bullet_list([
        "<b>Analyser le maillage</b>, dans chaque département, entre services de "
        "gynéco-obstétrique et sites transfusionnels, en concertation avec les services "
        "déconcentrés de l'État et l'Agence Régionale d'Hospitalisation. Les établissements "
        "pratiquant des accouchements doivent pouvoir disposer de CGR en <b>≤ 30 minutes, "
        "24 h/24 toute l'année</b> — trois solutions possibles : un site transfusionnel EFS à "
        "proximité, un dépôt de sang autorisé dans l'établissement, ou un dépôt d'urgence "
        "vitale autorisé sous conditions strictement réglementées. Le nombre de dépôts "
        "d'urgence doit être réduit à son strict minimum pour une bonne gestion des stocks "
        "phénotypés. Ce maillage, pour être réussi, suppose une concertation parfaite entre "
        "tous les acteurs, en gardant à l'esprit l'enjeu majeur d'éviter le décès maternel ; "
        "il doit évoluer en fonction de la restructuration de l'organisation nationale des "
        "maternités.",
        "<b>Établir la quantité et la qualité des stocks d'urgence vitale</b> : stock "
        "volontairement réduit (but : assurer la survie de la mère et de l'enfant pendant "
        "l'acheminement des autres CGR) ; composition conseillée : 2 CGR O RH:-1-2-3 KEL:-1 "
        "(anciennement ccddee, K-) et 2 CGR O RH:12-3-45 KEL:-1 (anciennement CCDee). La "
        "qualification CMV négatif <b>n'est pas nécessaire</b> dans ce contexte.",
        "<b>Réaliser des procédures de prescription d'urgence vitale</b> avec l'ensemble des "
        "acteurs (comités de sécurité transfusionnelle et d'hémovigilance), au niveau de l'ES "
        "et du ST, en clarifiant les modalités de communication (fax, téléphone — appels "
        "internes/externes, informatisation…), pouvant prendre la forme d'un arbre "
        "décisionnel d'utilisation des CGR en urgence vitale (voir Tableau I).",
        "<b>Prévoir le réapprovisionnement du dépôt d'urgence</b> : les hémorragies du "
        "péripartum étant souvent importantes et de survenue brutale, la capacité de réponse "
        "d'un dépôt peut être rapidement dépassée — le responsable du dépôt doit être prévenu "
        "sans attendre pour alerter le site transfusionnel.",
        "<b>Organiser les transports</b> — problème « ni réglé, ni même défini » selon la "
        "source elle-même (absence de bonnes pratiques de transport). Doivent être précisés : "
        "qui apporte les examens, qui transporte le sang, dans quels délais (notion "
        "essentielle pour le temps de réponse à l'UVI/UV), horaires d'ouverture et modalités "
        "des jours fériés, moyens utilisés (type de véhicule, containers, conservation sous "
        "contrôle), et qui réapprovisionne le dépôt. Un cahier des charges précis et/ou un "
        "contrat d'engagement doit définir clairement les points du transport liant ES, ST et "
        "transporteur.",
    ]))
    story.append(Spacer(1, 3 * mm))
    story.append(KeepTogether([
        section_bar("IV — Évaluation et suivi des actions"),
        Spacer(1, 2 * mm),
        bullet_list([
            "L'évaluation de l'efficacité des mesures mises en place doit être clairement "
            "définie dans un calendrier : conseillée hebdomadaire dans un premier temps, puis "
            "mensuelle, puis trimestrielle.",
            "Elle doit être réalisée à la fois par l'établissement de santé et par le site "
            "transfusionnel (liste des items indispensables fournie en annexe à titre "
            "d'exemple, reproduite ci-après).",
            "Il est recommandé que toute trace écrite des éventuels événements figure dans le "
            "dossier clinique, à des fins d'enquête ou d'évaluation ultérieure.",
        ]),
    ]))
    return story


def _annexe_flowchart_rows():
    cw = PAGE_W - 2 * MARGIN
    c0 = cw / 3.0
    return simple_table(
        ["Documents IH disponibles complets", "Documents IH incomplets (1 seule détermination "
         "de groupe, ou RAI &gt; 3 j)", "Absence de documents IH"],
        [[
            "Sang isogroupe si disponible immédiatement ; sinon 2 CGR O Rh nég Kell nég (ou "
            "2 CGR O Rh pos [c-, E-] Kell nég), puis poursuivre par CGR compatibles.",
            "2 CGR O Rh nég Kell nég (ou 2 CGR O Rh pos [c-, E-] Kell nég) ; prélever pour RAI "
            "et pour la 2<sup rise=\"2\" size=\"6\">e</sup> détermination de groupe + phénotype "
            "Rh Kell si besoin ; poursuivre selon le résultat.",
            "2 CGR O Rh nég Kell nég (ou 2 CGR O Rh pos [c-, E-] Kell nég) ; prélever pour RAI "
            "+ groupe sanguin avec phénotype Rh-Kell, dans une séquence différente pour la "
            "2<sup rise=\"2\" size=\"6\">e</sup> détermination ; poursuivre selon ces derniers "
            "résultats.",
        ]],
        [c0, c0, c0])


def _section_tableau1():
    story = []
    story.append(Spacer(1, 2 * mm))
    story.append(section_bar("Tableau I — Procédure d'urgence vitale"))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P("<i>Séquence reproduite intégralement depuis le Tableau I du document "
                    "source (arbre décisionnel d'utilisation des CGR en urgence vitale).</i>",
                    S_NOTE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(bullet_list([
        "Poser l'indication de la transfusion.",
        "Rédiger l'ordonnance de prescription de PSL.",
        "Avertir le site transfusionnel (ST) ou le dépôt de sang du niveau d'urgence : UVI ou "
        "UV (n<sup rise=\"2\" size=\"6\">os</sup> de tél./fax accessibles 24 h/24).",
        "Avertir le moyen de transport accessible 24 h/24 (interne ou externe à "
        "l'établissement).",
        "Faire parvenir l'ordonnance et les documents au ST ou au dépôt (fax, etc.) et, le cas "
        "échéant, les prélèvements nécessaires.",
        "Distribuer immédiatement (ou faire distribuer selon l'organisation locale) les PSL "
        "— voir les 3 cas de figure ci-dessous.",
    ], style=S_BODY_SM))
    story.append(Spacer(1, 2 * mm))
    story.append(_annexe_flowchart_rows())
    story.append(Spacer(1, 2 * mm))
    story.append(bullet_list([
        "Avertir le laboratoire d'immuno-hématologie (téléphone/fax 24 h/24).",
        "Réceptionner les PSL. Contrôler les documents (si disponibles) + contrôle ultime au "
        "lit du patient, puis transfusion des PSL (informer la patiente si son état de "
        "conscience le permet).",
        "Prévenir le ST ou le dépôt des besoins ultérieurs en PSL.",
        "Traçabilité + évaluation régulière de la procédure.",
    ], style=S_BODY_SM))
    return story


def _section_checklist():
    story = []
    story.append(Spacer(1, 2 * mm))
    story.append(section_bar("Liste des items — procédure générale (prescription de PSL à l'acte transfusionnel)"))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P("<i>Toute procédure doit définir au moins, selon le document source :</i>",
                    S_NOTE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(simple_table(
        ["Item"],
        [[x] for x in [
            "Les différents acteurs intervenants : qui prescrit et qui pose l'indication de la "
            "transfusion",
            "Les 3 niveaux d'urgence (UVI, UV et transfusion urgente)",
            "Les documents nécessaires (référencés, en documents associés)",
            "Les identifiants de l'unité de distribution : site transfusionnel ou dépôt (lieu, "
            "téléphone, fax, heures d'ouverture, noms des responsables) — inclure les "
            "procédures de distribution, dont celle pour une urgence vitale",
            "Le(s) correspondant(s) en charge du transport (local ou extérieur), procédures "
            "d'appels, conditions selon horaires et jours fériés, convention…",
            "Le laboratoire d'immuno-hématologie : téléphone, fax, horaires, conditions de "
            "prise en charge des urgences",
            "Définition des prélèvements nécessaires, des documents, sans oublier les "
            "contrôles pré-transfusionnels obligatoires (hémovigilance)",
            "Conditions d'acheminement des documents et des prélèvements",
            "Information de la patiente",
            "Modalités de réception des PSL",
            "Modalités de l'acte transfusionnel lui-même : vérification des documents, "
            "contrôle ultime pré-transfusionnel…",
            "La tenue du dossier transfusionnel",
            "La traçabilité",
            "Les contrôles post-transfusionnels",
            "L'évaluation régulière des procédures mises en place (essentiellement pour "
            "l'urgence vitale), leur pertinence et leur efficacité",
        ]],
        [PAGE_W - 2 * MARGIN]))
    return story


def _section_sources():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("Sources et traçabilité", color=GREY))
    story.append(Spacer(1, 2 * mm))
    story.append(P(
        "<b>Document source :</b> « Le traitement des urgences transfusionnelles "
        "obstétricales » — Conclusions de la table ronde organisée par l'EFS (réunie le "
        "26 septembre 2000). Participants : G. Andreu, D. Benhamou, B. Carbonne, J. Chiaroni, "
        "F. Courtois, A.-S. Ducloy-Bouthors, A. François, P. Hervé, B. Maria, M. Palot, "
        "F. Roubinet, M. Tournaire. Experts de validation : A. Blond, F. Ferrer Le Cœur, "
        "M. Jeanne, C. Krause, A. Lienhart, R. Mortelecque, L. Mannessier et le Groupe "
        "Immuno-Hématologie de la SFTS, P. Rouger. Soumis pour avis à la SFAR, au Collège des "
        "Obstétriciens, aux Directeurs d'établissement de l'EFS et à la Société Française de "
        "Transfusion Sanguine.", S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P("<b>Références citées par le texte source (8) :</b> 1. Arrêté du 19/04/1985 "
                    "modifiant l'arrêté du 27/08/1971 (examens médicaux pré/post-nataux). "
                    "2. Circulaire DGS/3B/552 du 17/05/1985 (prévention des accidents "
                    "transfusionnels et d'allo-immunisation). 3. Décret n°92-143 du 14/02/1992 "
                    "(examens obligatoires prénuptial, pré et post-natal). 4. Arrêté du "
                    "04/08/1994 (bonnes pratiques de distribution des PSL). 5. Arrêté du "
                    "25/04/2000 (locaux de prétravail/travail, dispositifs médicaux et examens "
                    "en néonatologie/réanimation néonatale). 6. Coeuret-Pellicer M, "
                    "Bouvier-Colle M.H, Salanave B, Groupe Moms, J Gynecol Obstet Biol Reprod "
                    "1999;28:62-68. 7. Synthèse des textes réglementaires — ANAES, juillet 1997. "
                    "8. Bowman JM, Pollock JM, Biggins KR, Methods in Haematology, Churchill "
                    "Livingston 1988;2,3:129-50.", S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P("<b>Méthodologie :</b> aucun système de gradation imprimé par la source "
                    "(pas de GRADE, pas de RAND/UCLA, pas de vote chiffré, pas d'échelle ANAES) "
                    "— conclusions de table ronde en prose continue. Aucun chip de grade "
                    "n'est donc utilisé dans cette fiche.", S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P("<b>Couverture :</b> intégralité des 4 chapitres du corps du texte (niveaux "
                    "d'urgence, surveillance immuno-hématologique, propositions d'organisation "
                    "ES/ST/ES+ST, évaluation et suivi), du Tableau I (procédure d'urgence "
                    "vitale) et de la liste des items de la procédure générale.", S_SOURCE))
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Avertissement :</b> ce document est une fiche de synthèse indépendante, produite "
        "pour un usage d'aide-mémoire. Il reprend l'intégralité des conclusions de la table "
        "ronde EFS, mais ne remplace pas le texte intégral et n'est ni édité ni validé par "
        "l'EFS, la SFAR, le Collège des Obstétriciens ou la SFTS. <b>Document dont le contenu "
        "date de 2000-2001</b> (voir disclosure de l'incohérence de métadonnées en page 1) : "
        "les pratiques et la réglementation transfusionnelle ont évolué depuis — vérifier "
        "l'existence d'une actualisation et se référer aux textes réglementaires en vigueur "
        "en cas de doute.",
        S_BODY_SM), bg=GREY_LIGHT, border=GREY))
    return story


def _section_1():
    return _section_intro()


def _section_2():
    return _section_niveaux() + [Spacer(1, 3 * mm)] + _section_surveillance()


def _section_3():
    return _section_organisation_es_st()


def _section_4():
    return _section_organisation_commune()


def _section_5():
    return (_section_tableau1() + [Spacer(1, 3 * mm)] + _section_checklist()
            + [Spacer(1, 4 * mm)] + _section_sources())


SECTIONS = [
    ("Introduction, épidémiologie & méthodologie", _section_1),
    ("I. Niveaux d'urgence & II. Surveillance immuno-hématologique", _section_2),
    ("III. Organisation — établissement de santé & site transfusionnel", _section_3),
    ("III. Organisation commune & IV. Évaluation-suivi", _section_4),
    ("Tableau I, liste des items & sources", _section_5),
]


def _make_doc(path=None):
    return SimpleDocTemplate(path or OUT, pagesize=A4,
                              leftMargin=MARGIN, rightMargin=MARGIN,
                              topMargin=32 * mm, bottomMargin=16 * mm,
                              title="Fiche EFS/SFAR (pour avis) 2001 - Urgences transfusionnelles obstetricales",
                              author="Synthese independante (source EFS, table ronde 2000)")


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
    # Throwaway temp path (never OUT) for measurement-only builds — see CLAUDE.md's
    # "critical bug to avoid" (reusing OUT here previously corrupted page 1's header_band).
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
