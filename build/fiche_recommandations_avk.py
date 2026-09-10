# -*- coding: utf-8 -*-
"""
Fiche de synthese - Recommandations professionnelles HAS/GEHT, avril 2008 :
"Prise en charge des surdosages en antivitamines K, des situations a risque
hemorragique et des accidents hemorragiques chez les patients traites par
antivitamines K en ville et en milieu hospitalier".
Source : sources/recommandations_avk.pdf (21 pages), sources/recommandations_avk.txt
(texte extrait integralement, 1330 lignes).

METHODOLOGIE - grades HAS A/B/C + "accord professionnel" (meme schema que
fiche_avc_precoce.py / fiche_infarctus_myocarde.py / fiche_transfusion_plasma.py).
VERIFIE PAR grep SUR LE TEXTE APLATI (espaces normalises), en ne comptant QUE les
citations parentheses explicites "(grade X)" comme tag officiel de la source - les
mentions "niveau de preuve N" (evidentiaire, cite en marge de certaines phrases) NE
SONT PAS traitees comme un tag de grade officiel quand elles n'accompagnent pas un
"(grade X)" imprime : Recherche confirmee, 28 citations "(grade X)" avant l'annexe 3
methodologique (qui elle-meme n'est pas comptee) : 5x grade A (dont 1x imprimee
"(grade A2)" dans la source - confirme etre un artefact de fusion PDF entre le tag
"(grade A)" et l'appel de note de bas de page "2", PAS un sous-niveau "A2" ; compte
ici comme grade A simple), 2x grade B, 21x grade C. Le reste des recommandations
explicites ("il est recommande de...", "il est propose de...") sans "(grade X)"
imprime sont taguees "AP" (accord professionnel), selon la definition meme donnee par
la source en annexe 3 : "les recommandations non graduees sont celles qui sont
fondees sur un accord professionnel".

DIVERGENCE SOURCE-INTERNE (disclosure, non resolue silencieusement, regle 5
CLAUDE.md) : deux enonces cliniques tres analogues a des enonces explicitement
gradues C dans la meme sous-section NE portent PAS de "(grade X)" imprime :
(1) le relais preoperatoire des AVK chez le patient en ACFA a haut risque
thrombo-embolique (4.2) cite seulement "niveau de preuve 2" en marge, sans grade
letter - a la difference de la clause symetrique "dans les autres cas" de la meme
sous-section qui, elle, porte explicitement "(grade C)" ; (2) la clause MTEV "patients
a risque de recidive modere" (4.4) n'a aucun tag, a la difference de sa clause
symetrique "a haut risque de recidive" qui porte "(grade C)". Ces deux enonces sont
retranscrits ici avec le chip "AP" plutot qu'un "C" invente par analogie - disclose
explicitement dans le panneau de methodologie plutot que resolu en silence.

COMPOSITE-CHIP SAFETY NET : une phrase source porte DEUX tags "(grade C)" distincts
pour deux clauses differentes dans une meme phrase (4.4, ACFA : "un relais
preoperatoire ... est recommande (grade C), preferentiellement par des HBPM
(grade C)") - splittee ici en deux lignes de tableau distinctes (regle 4 CLAUDE.md),
jamais fusionnee en un chip "C/C".

PERIMETRE - integralite des chapitres 2 (surdosage asymptomatique, dont le Tableau 1
integral), 3 (hemorragies spontanees/traumatiques, classification de gravite,
medicaments, conduite a tenir, reintroduction), 4 (chirurgie/acte invasif : 4.1 a 4.5,
dont l'Annexe 2 - schema de relais preoperatoire), et l'Annexe 1 (tableau du risque
hemorragique des actes de rhumatologie, 23 lignes, integral). Comite d'organisation,
groupe de travail, groupe de lecture (~85 noms) et "Fiche descriptive" (pages 19-21,
sans contenu clinique nouveau) ne sont pas retranscrits.

_count_pages() : pattern copie de fiche_aap_programmee.py (PyMuPDF/fitz, jamais vers
OUT, toujours vers tempfile.mktemp()).
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from style import *
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.units import mm

GRADE_COLORS["A"] = (GREEN, WHITE)
GRADE_COLORS["B"] = (TEAL, WHITE)
GRADE_COLORS["C"] = (AMBER, WHITE)
GRADE_COLORS["AP"] = (GREY, WHITE)
GRADE_COLORS["—"] = (GREY_LIGHT, INK)

OUT = "/home/user/rfe-sfar-website/output/Fiche_HAS_GEHT_Recommandations_AVK_2008.pdf"

SOURCE_TXT = ("Source : HAS/GEHT — « Prise en charge des surdosages en antivitamines K, des "
              "situations à risque hémorragique et des accidents hémorragiques chez les patients "
              "traités par AVK en ville et en milieu hospitalier » (avril 2008). Fiche de synthèse "
              "non officielle : se référer au texte intégral.")

def P(txt, style=S_CELL):
    return Paragraph(txt, style)

def chip(label, **kw):
    return grade_chip(label, **kw)

AP_W = 20 * mm

def prop_table(rows, col_widths=None):
    """rows: (text, grade_label) - grade_label parmi 'A', 'B', 'C', 'AP'."""
    text_w = PAGE_W - 2 * MARGIN - AP_W
    cw = col_widths or [text_w, AP_W]
    data = [[P("Recommandation (texte condensé, fidèle à la source)", S_HEAD_W), P("Niveau", S_HEAD_W_C)]]
    for txt, grade in rows:
        data.append([P(txt, S_CELL), chip(grade, width=AP_W - 2 * mm)])
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

def simple_table(header, rows, col_widths, header_style=S_HEAD_W):
    data = [[P(h, header_style) for h in header]] + [
        [c if not isinstance(c, str) else P(c, S_CELL) for c in row] for row in rows
    ]
    t = Table(data, colWidths=col_widths, repeatRows=1)
    style_cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), NAVY), ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTNAME", (0, 0), (-1, 0), FONT_BOLD), ("FONTSIZE", (0, 0), (-1, 0), 8),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
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
    header_band(canvas, doc, "HAS / GEHT — RECOMMANDATIONS AVRIL 2008 — FICHE DE SYNTHÈSE",
                "Surdosages, hémorragies & AVK",
                page_title, icon_fn=lambda c, x, y: icon_drop(c, x, y, 13 * mm), color=RED)
    footer_band(canvas, doc, SOURCE_TXT, f"Page {doc.page} / {TOTAL_PAGES['n']}")

# ---------------------------------------------------------------------------
def _section_intro_surdosage():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Champ :</b> prise en charge des <b>surdosages asymptomatiques</b>, des "
        "<b>hémorragies</b> (spontanées ou traumatiques) et de la <b>chirurgie/acte invasif</b> "
        "chez les patients traités par antivitamines K (AVK). ~600 000 patients traités par AVK "
        "en France chaque année (~1 % de la population). Surdosage asymptomatique : 15-30 % des "
        "contrôles d'INR. Accidents hémorragiques des AVK : 1er rang des accidents iatrogènes "
        "(13 % des hospitalisations pour effet indésirable médicamenteux, ~17 000 "
        "hospitalisations/an). <b>Professionnels concernés :</b> médecins traitants, biologistes, "
        "infirmiers, urgentistes, chirurgiens, anesthésistes-réanimateurs, et médecins des "
        "disciplines liées à l'indication du traitement.", S_BODY), bg=BG_PANEL, border=RED))
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Méthodologie — grades HAS A/B/C + « accord professionnel »</b> : Grade A = preuve "
        "scientifique établie ; Grade B = présomption scientifique ; Grade C = faible niveau de "
        "preuve ; <b>« accord professionnel »</b> (chip « AP ») = en l'absence d'études, avis du "
        "groupe de travail après consultation du groupe de lecture. <b>Vérifié exhaustivement par "
        "grep (texte aplati) : 28 citations « (grade X) » explicites — 5× A (dont 1 imprimée "
        "« grade A2 » dans la source, artefact de fusion entre le tag et un appel de note de bas "
        "de page — comptée ici comme grade A simple), 2× B, 21× C.</b> <b>Disclosure :</b> 2 "
        "énoncés cliniquement très analogues à des clauses gradées C dans la même sous-section "
        "n'ont, dans la source, aucun tag de grade imprimé (relais préopératoire AVK chez le "
        "patient en ACFA à haut risque, §4.2 ; clause MTEV « risque de récidive modéré », §4.4) — "
        "retranscrits ici avec « AP » plutôt qu'un « C » inventé par analogie.", S_BODY_SM),
        bg=BG_PANEL, border=AMBER))
    story.append(Spacer(1, 3 * mm))

    story.append(section_bar("2 — Conduite à tenir en cas de surdosage asymptomatique", color=RED))
    story.append(Spacer(1, 2 * mm))
    story.append(prop_table([
        ("Privilégier une prise en charge ambulatoire, si le contexte médical et social le "
         "permet. L'hospitalisation est préférable s'il existe un ou plusieurs facteurs de risque "
         "hémorragique individuel (âge, antécédent hémorragique, comorbidité). En l'absence "
         "d'hospitalisation : informer le patient et son entourage du risque hémorragique à court "
         "terme et des signes d'alerte (tout saignement, même minime, ou symptôme nouveau → "
         "consultation médicale sans délai).", "AP"),
    ]))
    story.append(Spacer(1, 2 * mm))
    story.append(P("<b>Tableau 1 — Mesures correctrices recommandées</b> en cas de surdosage en "
                    "AVK, en fonction de l'INR mesuré et de l'INR cible.", S_BODY_SM))
    story.append(Spacer(1, 1.5 * mm))
    cw = PAGE_W - 2 * MARGIN
    c0 = 28 * mm
    c1 = c2 = (cw - c0) / 2.0
    story.append(simple_table(
        ["INR mesuré", "INR cible 2,5 (fenêtre 2-3)", "INR cible ≥ 3 (fenêtre 2,5-3,5 ou 3-4,5)"],
        [
            ["INR < 4", "Pas de saut de prise. Pas d'apport de vitamine K.",
             "Sans objet — la source marque cette combinaison d'un hachurage diagonal (« INR "
             "mesuré < 4 » n'est, par définition, pas un surdosage relatif à une INR cible ≥ 3)."],
            ["4 ≤ INR < 6", "Saut d'une prise. Pas d'apport de vitamine K.",
             "Pas de saut de prise. Pas d'apport de vitamine K."],
            ["6 ≤ INR < 10", "Arrêt du traitement par AVK. 1 à 2 mg de vitamine K par voie orale "
             "(1/2 à 1 ampoule buvable forme pédiatrique) — <b>grade A</b>.",
             "Saut d'une prise. Avis spécialisé (ex. cardiologue si prothèse valvulaire "
             "mécanique) recommandé pour discuter un traitement éventuel par 1 à 2 mg de "
             "vitamine K par voie orale."],
            ["INR ≥ 10", "Arrêt du traitement par AVK. 5 mg de vitamine K par voie orale (1/2 "
             "ampoule buvable forme adulte) — <b>grade A</b>.",
             "Avis spécialisé sans délai ou hospitalisation recommandé."],
        ], [c0, c1, c2]))
    story.append(Spacer(1, 2 * mm))
    story.append(prop_table([
        ("À faire dans tous les cas : rechercher la cause du surdosage (prise en compte pour "
         "l'adaptation éventuelle de la posologie). Contrôle de l'INR le lendemain. En cas de "
         "persistance d'un INR suprathérapeutique, les mesures du Tableau 1 restent valables et "
         "doivent être reconduites. Surveillance ultérieure de l'INR calquée sur celle de la mise "
         "en route du traitement.", "AP"),
    ]))
    return story


def _section_hemorragies():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("3 — Hémorragies spontanées ou traumatiques", color=RED))
    story.append(Spacer(1, 2 * mm))
    story.append(info_panel(P(
        "<b>Hémorragie grave ou potentiellement grave</b> (définition, au moins un critère) : "
        "hémorragie extériorisée non contrôlable par les moyens usuels ; instabilité "
        "hémodynamique (PAS &lt; 90 mmHg ou -40 mmHg vs habituelle, ou PAM &lt; 65 mmHg, ou tout "
        "signe de choc) ; nécessité d'un geste hémostatique urgent (chirurgie, radiologie "
        "interventionnelle, endoscopie) ; nécessité de transfusion de culots globulaires ; "
        "localisation menaçant le pronostic vital/fonctionnel (hémorragie intracrânienne/"
        "intraspinale, intraoculaire/rétro-orbitaire, hémothorax, hémo/rétropéritoine, "
        "hémopéricarde, hématome musculaire profond/syndrome de loge, hémorragie digestive aiguë, "
        "hémarthrose). En l'absence de ces critères : hémorragie <b>non grave</b>.", S_BODY_SM)))
    story.append(Spacer(1, 3 * mm))

    story.append(section_bar("Hémorragie non grave", color=TEAL_DARK))
    story.append(Spacer(1, 2 * mm))
    story.append(prop_table([
        ("Prise en charge ambulatoire par le médecin traitant, si l'environnement médico-social "
         "et le type d'hémorragie le permettent (ex. épistaxis rapidement contrôlable).", "AP"),
        ("Mesure de l'INR en urgence. En cas de surdosage : mêmes mesures de correction que pour "
         "le surdosage asymptomatique (Tableau 1). Recherche de la cause du saignement. Absence "
         "de contrôle de l'hémorragie par les moyens usuels = critère de gravité → indication de "
         "prise en charge hospitalière pour antagonisation rapide.", "AP"),
    ]))
    story.append(Spacer(1, 3 * mm))

    story.append(section_bar("Médicaments utilisables en cas d'hémorragie grave", color=TEAL_DARK))
    story.append(Spacer(1, 2 * mm))
    story.append(P(
        "La vitamine K et les concentrés de complexe prothrombinique (CCP/PPSB — Kaskadil® et "
        "Octaplex® commercialisés en France en 2008) sont les moyens médicamenteux les plus "
        "appropriés.", S_BODY_SM))
    story.append(Spacer(1, 2 * mm))
    story.append(prop_table([
        ("Ne pas utiliser le plasma dans le seul but d'antagonisation des effets des AVK, sauf en "
         "cas d'indisponibilité d'un CCP.", "B"),
        ("Ne pas utiliser le facteur VII activé recombinant (eptacog alpha, NovoSeven®) dans le "
         "but d'antagonisation des effets des AVK.", "C"),
    ]))
    story.append(Spacer(1, 3 * mm))

    story.append(section_bar("Conduite à tenir en cas d'hémorragie grave", color=TEAL_DARK))
    story.append(Spacer(1, 2 * mm))
    story.append(prop_table([
        ("Prise en charge hospitalière obligatoire. Formalisation de procédures organisationnelles "
         "pluridisciplinaires (améliore rapidité et qualité de la prise en charge). Geste "
         "hémostatique (chirurgical, endoscopique, endovasculaire) discuté rapidement avec "
         "chirurgiens/radiologues.", "AP"),
        ("Mesurer l'INR en urgence à l'admission — la mise en route du traitement ne doit pas "
         "attendre le résultat si celui-ci ne peut être obtenu rapidement ; INR par microméthode "
         "au lit du patient si délai prévisible &gt; 30-60 min. Objectif : restauration d'une "
         "hémostase normale (INR &lt; 1,5) dans un délai le plus bref possible (quelques "
         "minutes).", "AP"),
        ("Arrêter l'AVK.", "AP"),
        ("Administrer en urgence du CCP et de la vitamine K.", "C"),
        ("Assurer simultanément le traitement usuel d'une éventuelle hémorragie massive "
         "(correction de l'hypovolémie, transfusion de culots globulaires si besoin).", "AP"),
        ("En l'absence de circuit d'approvisionnement rapide : réserve de quelques flacons de CCP "
         "dans les services concernés (urgences, réanimation, certains blocs opératoires), en "
         "accord avec la pharmacie.", "AP"),
        ("Dose de CCP si l'INR contemporain de l'hémorragie n'est pas disponible : 25 UI/kg "
         "d'équivalent facteur IX (1 ml/kg pour un CCP dosé à 25 U/ml). Si l'INR contemporain est "
         "disponible : dose suivant le RCP de la spécialité utilisée.", "C"),
        ("Vitesse d'injection IV du CCP : 4 ml/min préconisé par les fabricants (des données "
         "préliminaires indiquent qu'un bolus de 3 min obtient un taux de correction comparable, "
         "niveau de preuve 4).", "—"),
        ("Administrer 10 mg de vitamine K par voie orale ou IV lente en même temps que le CCP, "
         "quel que soit l'INR de départ.", "C"),
        ("Contrôles biologiques : INR à 30 min après le CCP (complément de CCP si INR &gt; 1,5, "
         "adapté au RCP) ; INR à 6-8h puis quotidien pendant la période critique.", "AP"),
    ]))
    story.append(Spacer(1, 3 * mm))

    story.append(section_bar("Patient victime d'un traumatisme", color=TEAL_DARK))
    story.append(Spacer(1, 2 * mm))
    story.append(prop_table([
        ("Mesurer l'INR en urgence et adopter la même conduite que pour les hémorragies "
         "spontanées (grave ou non grave), suivant la nature du traumatisme.", "AP"),
        ("Traumatisme crânien : hospitalisation systématique pour surveillance ≥ 24h. Scanner "
         "cérébral immédiat si symptomatologie neurologique.", "AP"),
        ("Traumatisme crânien sans symptomatologie neurologique : scanner cérébral dans un délai "
         "rapide (4 à 6 heures).", "C"),
    ]))
    return story


def _section_reintroduction_chirurgie():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("Réintroduction des AVK après une hémorragie grave", color=TEAL_DARK))
    story.append(Spacer(1, 2 * mm))
    story.append(prop_table([
        ("Si l'indication des AVK est maintenue et le saignement contrôlé : traitement par "
         "héparine (HNF ou HBPM) à dose curative en parallèle de la reprise des AVK, en milieu "
         "hospitalier sous surveillance clinique et biologique. Modalités fonction du siège de "
         "l'hémorragie et de l'indication des AVK.", "AP"),
        ("Hémorragie intracrânienne, patient porteur d'une prothèse valvulaire mécanique (PVM) : "
         "la PVM impose la reprise d'une anticoagulation au long cours.", "A"),
        ("Hémorragie intracrânienne, patient porteur d'une PVM : fenêtre thérapeutique de "
         "normocoagulation de 1 à 2 semaines proposée (discussion multidisciplinaire souhaitable "
         "pour en fixer la durée).", "C"),
        ("Hémorragie intracrânienne à localisation hémisphérique et ACFA non valvulaire : arrêt "
         "définitif du traitement anticoagulant recommandé.", "A"),
        ("Hémorragie intracrânienne, patient ayant une MTEV : fenêtre thérapeutique de "
         "normocoagulation de 1 à 2 semaines proposée (discussion multidisciplinaire ; filtre "
         "cave discuté si MTEV &lt; 1 mois).", "C"),
        ("Autres hémorragies graves : fenêtre thérapeutique de 48 à 72h, modulée selon le risque "
         "thromboembolique. Reprise d'autant plus précoce qu'un geste hémostatique garantit une "
         "faible probabilité de récidive.", "AP"),
    ]))
    story.append(Spacer(1, 4 * mm))

    story.append(section_bar("4 — Chirurgie ou acte invasif", color=RED))
    story.append(Spacer(1, 2 * mm))
    story.append(section_bar("4.1 — Procédures réalisables sans interrompre les AVK", color=TEAL_DARK))
    story.append(Spacer(1, 2 * mm))
    story.append(prop_table([
        ("Chirurgie cutanée, dans la zone thérapeutique usuelle (INR 2-3), après vérification de "
         "l'absence de surdosage.", "C"),
        ("Chirurgie de la cataracte, dans la zone thérapeutique usuelle.", "C"),
        ("Actes de rhumatologie à faible risque hémorragique (voir Tableau — Annexe 1) ; certains "
         "actes bucco-dentaires et d'endoscopie digestive (se référer aux recommandations des "
         "sociétés spécialisées correspondantes).", "—"),
        ("Dans les autres cas : arrêt des AVK ou antagonisation en urgence. Seuil d'INR ≤ 1,5 "
         "(≤ 1,2 en neurochirurgie) retenu comme absence de majoration du risque hémorragique "
         "périopératoire. Injections sous-cutanées possibles sans interrompre les AVK ; "
         "injections intramusculaires déconseillées (risque hémorragique).", "AP"),
    ]))
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("4.2 — Situations imposant un relais héparinique (acte programmé)", color=TEAL_DARK))
    story.append(Spacer(1, 2 * mm))
    story.append(prop_table([
        ("Risque thromboembolique élevé (selon l'indication du traitement AVK) : relais pré- et "
         "postopératoire par héparine à dose curative. Dans les autres cas : relais postopératoire "
         "recommandé si la reprise des AVK à 24-48h postopératoires est impossible (voie entérale "
         "indisponible).", "AP"),
        ("PVM cardiaque, quel que soit le type : relais pré- et postopératoire des AVK par les "
         "héparines recommandé.", "C"),
        ("ACFA à haut risque thromboembolique (ATCD d'AVC/AIT ou d'embolie systémique) : relais "
         "pré- et postopératoire des AVK par les héparines recommandé — <i>niveau de preuve 2 "
         "cité par la source, mais sans « (grade X) » imprimé sur cette clause (voir disclosure "
         "méthodologique en page 1).</i>", "AP"),
        ("ACFA, autres cas : l'anticoagulation par AVK peut être interrompue sans relais "
         "préopératoire (reprise à 24-48h postopératoires).", "C"),
        ("MTEV à haut risque thromboembolique (épisode &lt; 3 mois, ou maladie récidivante "
         "idiopathique ≥ 2 épisodes dont ≥ 1 sans facteur déclenchant) : relais pré- et "
         "postopératoire des AVK par les héparines recommandé.", "C"),
        ("MTEV, autres cas : l'anticoagulation par AVK peut être interrompue sans relais "
         "préopératoire (reprise à 24-48h postopératoires).", "C"),
    ]))
    return story


def _section_relais_indication():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("4.3 — Modalités du relais héparinique (acte programmé)", color=TEAL_DARK))
    story.append(Spacer(1, 2 * mm))
    story.append(info_panel(P(
        "<b>Relais préopératoire :</b> mesurer l'INR 7 à 10 jours avant l'intervention. Si en "
        "zone thérapeutique : arrêter l'AVK 4-5 jours avant l'intervention (tous AVK), débuter "
        "l'héparine à dose curative 48h après la dernière prise de fluindione/warfarine, ou 24h "
        "après la dernière prise d'acénocoumarol. Si hors zone thérapeutique : avis de l'équipe "
        "médico-chirurgicale. Hospitaliser au plus tard la veille si le relais n'est pas géré en "
        "ville. INR la veille de l'intervention ; si INR &gt; 1,5 : 5 mg de vitamine K per os "
        "(contrôle le matin de l'intervention). Interventions programmées de préférence le matin. "
        "Arrêt préopératoire des héparines : HNF IV à la seringue électrique 4-6h avant ; HNF SC "
        "8-12h avant ; HBPM, dernière dose 24h avant. Contrôle du TCA/anti-Xa le matin non "
        "nécessaire (voir Annexe 2 pour un exemple de schéma complet).", S_BODY_SM)))
    story.append(Spacer(1, 2 * mm))
    story.append(info_panel(P(
        "<b>Relais postopératoire :</b> héparines à dose curative reprises 6-48h postopératoires "
        "selon le risque hémorragique/thromboembolique (jamais avant la 6e heure — si la reprise "
        "à dose curative n'est pas possible dès la 6e heure, prévention postopératoire de la MTEV "
        "selon les modalités habituelles). AVK repris dans les 24 premières heures (sinon dès que "
        "possible), aux posologies habituelles, sans dose de charge. Si voie entérale indisponible "
        "&gt; 24-48h : poursuivre l'héparine à dose curative jusqu'à reprise possible des AVK. "
        "Héparine interrompue après 2 INR successifs en zone thérapeutique à 24h d'intervalle.",
        S_BODY_SM)))
    story.append(Spacer(1, 4 * mm))

    story.append(section_bar("4.4 — Prise en charge selon l'indication du traitement (acte programmé)", color=TEAL_DARK))
    story.append(Spacer(1, 2 * mm))
    story.append(P("<b>Patient porteur d'une valve mécanique cardiaque</b>", S_BODY_SM))
    story.append(Spacer(1, 1.5 * mm))
    story.append(prop_table([
        ("Relais des AVK par des héparines recommandé en périopératoire.", "C"),
        ("Relais possible par HBPM (hors AMM, dose curative, 2 injections SC/jour — enoxaparine "
         "ou dalteparine), par HNF IV à la seringue électrique, ou par HNF SC (2-3 "
         "injections/jour) à dose curative : ces trois options sont possibles.", "B"),
        ("En l'absence de données périopératoires, pour les procédures à risque hémorragique "
         "modéré ou élevé : l'HBPM à dose curative en une injection/jour ou le fondaparinux ne "
         "peuvent être recommandés. Héparines à dose curative dans les 6-48h postopératoires "
         "(jamais avant la 6e heure ; sinon prévention MTEV postopératoire précoce habituelle).",
         "AP"),
    ]))
    story.append(Spacer(1, 2 * mm))
    story.append(P("<b>Patient traité pour arythmie chronique par fibrillation auriculaire (ACFA)</b>", S_BODY_SM))
    story.append(Spacer(1, 1.5 * mm))
    story.append(prop_table([
        ("Risque thromboembolique élevé : relais préopératoire des AVK par HBPM ou HNF à dose "
         "curative recommandé.", "C"),
        ("Risque thromboembolique élevé : relais préférentiellement par des HBPM.", "C"),
        ("Risque thromboembolique faible ou modéré : l'anticoagulation par AVK peut être "
         "interrompue sans relais préopératoire. Si reprise des AVK impossible à 24-48h "
         "postopératoires : relais postopératoire par HBPM ou HNF à dose curative à envisager.",
         "C"),
        ("Dans tous les cas, en l'absence de données périopératoires, pour les procédures à "
         "risque hémorragique modéré ou élevé : HBPM à dose curative en une injection/jour ou "
         "fondaparinux non recommandés.", "AP"),
    ]))
    story.append(Spacer(1, 2 * mm))
    story.append(P("<b>Patient traité pour un antécédent de MTEV</b>", S_BODY_SM))
    story.append(Spacer(1, 1.5 * mm))
    story.append(prop_table([
        ("Haut risque de récidive : différer une chirurgie réglée si possible, au minimum "
         "au-delà du 1er mois suivant l'épisode, de préférence au-delà du 3e mois.", "AP"),
        ("Haut risque de récidive, chirurgie dans le 1er mois : mise en place d'un filtre cave "
         "préopératoire (éventuellement optionnel) à discuter.", "C"),
        ("Haut risque de récidive : relais préopératoire des AVK par HBPM à dose curative ou par "
         "HNF (IV à la seringue électrique ou SC 2-3 injections/jour) recommandé.", "C"),
        ("Risque de récidive modéré : l'anticoagulation par AVK peut être interrompue sans relais "
         "préopératoire ; reprise des AVK recommandée à 24-48h postopératoires (sinon relais "
         "postopératoire par HBPM/HNF à dose curative). <i>Clause symétrique de son équivalent "
         "« haut risque » ci-dessus, mais sans « (grade X) » imprimé sur cette clause dans la "
         "source (voir disclosure méthodologique en page 1).</i>", "AP"),
        ("Dans tous les cas (MTEV) : prévention postopératoire précoce de la MTEV réalisée "
         "jusqu'à ce que l'INR soit en zone thérapeutique (ou la reprise des héparines à dose "
         "curative). En l'absence de données périopératoires, le fondaparinux à dose curative ne "
         "peut être recommandé. Privilégier l'HBPM à dose curative en 2 injections/jour ; l'HBPM "
         "en une injection/jour peut être discutée au cas par cas.", "AP"),
    ]))
    return story


def _section_urgent_annexes_sources():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("4.5 — Chirurgie ou acte invasif urgent à risque hémorragique", color=TEAL_DARK))
    story.append(Spacer(1, 2 * mm))
    story.append(P(
        "Un acte urgent est défini par sa réalisation indispensable dans un délai ne permettant "
        "pas d'atteindre le seuil hémostatique (INR &lt; 1,5, &lt; 1,2 en neurochirurgie) par la "
        "seule vitamine K.", S_BODY_SM))
    story.append(Spacer(1, 2 * mm))
    story.append(prop_table([
        ("Mesurer l'INR à l'admission du patient.", "AP"),
        ("Administration de CCP recommandée, selon les modalités de la prise en charge de "
         "l'hémorragie grave.", "C"),
        ("Associer 5 mg de vitamine K à l'administration de CCP, sauf si la correction de "
         "l'hémostase n'est nécessaire que pendant moins de 4 heures.", "C"),
        ("Privilégier la voie entérale pour la vitamine K, lorsqu'elle est possible.", "A"),
        ("INR recommandé dans les 30 min suivant le CCP et avant l'acte (complément de CCP si "
         "insuffisamment corrigé) ; INR à 6-8h après l'antagonisation.", "AP"),
        ("Si l'acte est compatible avec une réversion par la seule vitamine K (délai 6-24h selon "
         "l'INR) : CCP non nécessaire ; vitamine K 5-10 mg (voie entérale si possible) ; INR "
         "répété toutes les 6-8h jusqu'à l'intervention. Prise en charge postopératoire identique "
         "à celle d'un acte programmé.", "AP"),
    ]))
    story.append(Spacer(1, 4 * mm))

    story.append(section_bar("Annexe 1 — Risque hémorragique des actes invasifs de rhumatologie", color=GREY))
    story.append(Spacer(1, 2 * mm))
    cw = PAGE_W - 2 * MARGIN
    c0 = cw - 26 * mm
    c1 = 26 * mm
    rhumato_rows = [
        ("Infiltrations périarticulaires", "3"),
        ("Ponction-infiltration simple des articulations périphériques hors coxo-fémorales", "3"),
        ("Ponction-infiltration simple des articulations coxo-fémorales", "2"),
        ("Infiltration canalaire superficielle", "3"),
        ("Infiltration canalaire profonde (cf. Alcock)", "2"),
        ("Ténotomie percutanée", "2"),
        ("Ponction-infiltration rachidienne cervicale ou lombaire, épidurale ou intradurale", "1"),
        ("Ponction-infiltration rachidienne cervicale, foraminale", "1"),
        ("Ponction-infiltration rachidienne lombaire, foraminale", "2"),
        ("Ponction-infiltration rachidienne articulaire postérieure", "2"),
        ("Ponction-infiltration rachidienne dorsale costo-vertébrale", "2"),
        ("Lavage articulaire d'une articulation périphérique", "2"),
        ("Ponction-trituration de l'épaule", "2"),
        ("Biopsie synoviale", "2"),
        ("Biopsie osseuse", "2"),
        ("Ponction-biopsie discale", "1"),
        ("Biopsie des glandes salivaires accessoires", "3"),
        ("Cimentoplastie", "1"),
        ("Infiltration sacro-iliaque", "2"),
        ("Ponction kyste poplité", "2"),
        ("Capsulodistension", "2"),
        ("Ponction-infiltration sterno-claviculaire", "2"),
        ("Ponction-infiltration par le hiatus sacro-coccygien", "2"),
    ]
    story.append(KeepTogether([
        simple_table(["Type d'acte", "Niveau de risque"], rhumato_rows, [c0, c1]),
        Spacer(1, 1.5 * mm),
        P("Cotation : 1 = risque élevé — 2 = risque modéré — 3 = risque faible.", S_NOTE),
    ]))
    story.append(Spacer(1, 4 * mm))

    story.append(section_bar("Annexe 2 — Exemple de relais préopératoire AVK-héparine (acte programmé)", color=GREY))
    story.append(Spacer(1, 2 * mm))
    story.append(P(
        "(INR déterminé 7 à 10 jours avant, en zone thérapeutique) — <b>J-5 :</b> dernière prise "
        "de fluindione/warfarine. <b>J-4 :</b> pas de prise d'AVK. <b>J-3 :</b> première dose "
        "d'HBPM curative sous-cutanée (SC) ou HNF SC le soir. <b>J-2 :</b> HBPM ×2/j SC ou HNF SC "
        "×2-3/j. <b>J-1 :</b> hospitalisation systématique ; HBPM à dose curative le matin ou HNF "
        "SC jusqu'au soir ; ajustement selon le bilan biologique (si INR ≥ 1,5 la veille : 5 mg "
        "de vitamine K per os). <b>J0 :</b> chirurgie.", S_BODY_SM))
    story.append(Spacer(1, 4 * mm))

    story.append(section_bar("Sources et traçabilité", color=GREY))
    story.append(Spacer(1, 2 * mm))
    story.append(P(
        "<b>Document source :</b> « Prise en charge des surdosages en antivitamines K, des "
        "situations à risque hémorragique et des accidents hémorragiques chez les patients "
        "traités par antivitamines K en ville et en milieu hospitalier » — Recommandations "
        "professionnelles, Groupe d'étude sur l'hémostase et la thrombose (GEHT, promoteur), en "
        "partenariat avec la Haute Autorité de Santé (HAS). Validé par le Collège de la HAS en "
        "avril 2008.", S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P("<b>Méthodologie :</b> grades HAS A/B/C + accord professionnel (« AP ») — 28 "
                    "citations « (grade X) » explicites (5× A, 2× B, 21× C) vérifiées par grep "
                    "exhaustif sur le texte aplati ; 2 divergences source-internes disclosées (voir "
                    "méthodologie en page 1).", S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P("<b>Couverture :</b> cette fiche reprend l'intégralité des chapitres 2 "
                    "(surdosage, Tableau 1), 3 (hémorragies), 4 (chirurgie/acte invasif, dont "
                    "Annexe 2) et l'Annexe 1 (risque hémorragique en rhumatologie, 23 lignes). "
                    "Comité d'organisation, groupe de travail, groupe de lecture (~85 noms) et "
                    "« Fiche descriptive » ne sont pas retranscrits (sans contenu clinique "
                    "nouveau).", S_SOURCE))
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Avertissement — document de 2008 :</b> ce document est une fiche de synthèse "
        "indépendante, produite pour un usage d'aide-mémoire. Elle reprend l'intégralité des "
        "recommandations du texte source, mais ne remplace pas le texte intégral (argumentaire "
        "complet) et n'est ni éditée ni validée par la HAS ou le GEHT. Les CCP/PPSB et vitamine K "
        "citées (Kaskadil®, Octaplex®) reflètent les spécialités commercialisées en France en "
        "2008 ; vérifier l'actualité des disponibilités et des posologies (RCP en vigueur) et, en "
        "cas de doute, se référer à un avis spécialisé.",
        S_BODY_SM), bg=GREY_LIGHT, border=GREY))
    return story


SECTIONS = [
    ("Surdosage asymptomatique", _section_intro_surdosage),
    ("Hémorragies spontanées ou traumatiques", _section_hemorragies),
    ("Réintroduction AVK & chirurgie (4.1-4.2)", _section_reintroduction_chirurgie),
    ("Relais héparinique & indication (4.3-4.4)", _section_relais_indication),
    ("Acte urgent, annexes & sources", _section_urgent_annexes_sources),
]

def _make_doc(path=None):
    return SimpleDocTemplate(path or OUT, pagesize=A4,
                              leftMargin=MARGIN, rightMargin=MARGIN,
                              topMargin=32 * mm, bottomMargin=16 * mm,
                              title="HAS/GEHT 2008 - Recommandations AVK",
                              author="Synthèse indépendante (source HAS/GEHT)")

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
