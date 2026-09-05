# -*- coding: utf-8 -*-
"""
Fiche de synthese - GIHP & GFHT, en collaboration avec la SFAR (2018)
"Gestion des agents antiplaquettaires en cas de procedure invasive non programmee ou
d'hemorragie" - Propositions (pas une RFE GRADE classique).
Source verifiee : https://sfar.org/download/gestion-perioperatoire-des-patients-sous-aap-en-urgence/?wpdmdl=34414
Publie Anesth Reanim. 2019;5:218-237 (disponible en ligne 23/11/2018).
METHODOLOGIE DISTINCTE : ce document n'utilise PAS le systeme GRADE (pas de niveaux 1+/1-/2+/2-).
Les propositions ont ete redigees par groupes de travail GIHP/GFHT puis validees par un vote
Delphi (n=38) : accord retenu si >=50% d'accord et <20% d'opposition ; "accord fort" si >=70%
d'accord. Le resume du document indique explicitement que TOUTES les propositions retenues ont
recu un accord fort (confirme : aucune occurrence "accord faible" trouvee dans le texte source).
Il n'existe donc pas de distinction de force/direction a la maniere GRADE - chaque proposition
est ici chipee "AE" (avis d'experts / proposition, accord fort), la nuance directionnelle etant
portee par le texte de la proposition elle-meme (faire / ne pas faire / pas de proposition).
20 pages source, document compact -> couverture complete.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from style import *
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.units import mm

OUT = "/private/tmp/claude-501/-Users-macbook-Downloads-claude/65498e3e-5ddf-47a6-b100-3ac535d1faa0/scratchpad/rfe_sfar/output/Fiche_SFAR_AAP_Urgence_2018.pdf"

SOURCE_TXT = ("Source : GIHP & GFHT, en collaboration avec la SFAR — « Gestion des agents "
              "antiplaquettaires en cas de procédure invasive non programmée ou d'hémorragie » — "
              "Propositions, Anesth Reanim. 2019;5:218-237. Fiche de synthèse non officielle : se "
              "référer au texte intégral.")

def P(txt, style=S_CELL):
    return Paragraph(txt, style)

def chip(label, **kw):
    return grade_chip(label, **kw)

def theme_table(rows, col_widths):
    data = [[P("Thème", S_HEAD_W), P("Proposition", S_HEAD_W), P("Accord", S_HEAD_W_C)]]
    for theme, txt, grade in rows:
        data.append([P(theme, S_CELL_B), P(txt, S_CELL), chip(grade)])
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

TOTAL_PAGES = {"n": 6}

def on_page(canvas, doc, page_title):
    header_band(canvas, doc, "GIHP / GFHT / SFAR — PROPOSITIONS 2018 — FICHE DE SYNTHÈSE",
                "Agents antiplaquettaires en urgence",
                page_title, icon_fn=lambda c,x,y: icon_drop(c, x, y, 13*mm), color=RED)
    footer_band(canvas, doc, SOURCE_TXT, f"Page {doc.page} / {TOTAL_PAGES['n']}")

def _section_1():
    story = []
    story.append(Spacer(1, 3*mm))
    story.append(info_panel(P(
        "<b>Champ :</b> gestion des agents antiplaquettaires (AAP) oraux — aspirine, clopidogrel, "
        "prasugrel, ticagrelor — en cas de procédure invasive non programmée ou d'hémorragie. "
        "Complète les propositions 2018 du GIHP/GFHT/SFAR pour la procédure invasive "
        "<b>programmée</b> (fiche distincte).<br/><br/>"
        "<b>Méthodologie — distincte de GRADE :</b> ce document ne comporte pas de niveaux "
        "GRADE 1+/1-/2+/2-. Les propositions ont été rédigées par groupes de travail GIHP/GFHT puis "
        "validées par un vote Delphi (n=38) : accord retenu si ≥50% d'accord et &lt;20% "
        "d'opposition, « accord fort » si ≥70% d'accord. <b>Toutes les propositions retenues dans "
        "ce document ont reçu un accord fort</b> (aucune « accord faible » dans le texte source) — "
        "chaque proposition est donc chipée « AE » (avis d'experts / proposition, accord fort), la "
        "nuance de sens (faire / ne pas faire / pas de proposition possible) étant portée par le "
        "texte lui-même.",
        S_BODY), bg=RED_LIGHT, border=RED))
    story.append(Spacer(1, 3*mm))

    story.append(section_bar("Tableau I — propriétés pharmacologiques des AAP oraux"))
    story.append(Spacer(1, 2*mm))
    cw = PAGE_W - 2*MARGIN
    story.append(simple_table(
        ["AAP", "Mécanisme", "Dose d'entretien", "Pic", "Demi-vie"],
        [
            ["Aspirine", "Inhibiteur irréversible COX-1", "75-300 mg/j", "15-40 min", "15-20 min"],
            ["Clopidogrel", "Inhibiteur irréversible P2Y12", "75 mg × 1/j", "30-60 min", "30 min"],
            ["Prasugrel", "Inhibiteur irréversible P2Y12", "10 mg × 1/j", "30 min", "3,7 h"],
            ["Ticagrelor", "Inhibiteur réversible P2Y12", "90 mg × 2/j", "1,5-3 h", "6,7-9,1 h (métabolite actif 8,5-12,4 h)"],
        ],
        [cw*0.16, cw*0.28, cw*0.18, cw*0.16, cw*0.22]))
    story.append(Spacer(1, 2*mm))
    story.append(P("Seul le ticagrelor a une action réversible. Il n'existe pas d'antidote disponible "
                    "pour les AAP à la date de rédaction du texte source.", S_NOTE))
    story.append(Spacer(1, 4*mm))

    story.append(section_bar("Tests fonctionnels plaquettaires — place dans l'urgence"))
    story.append(Spacer(1, 2*mm))
    story.append(theme_table([
        ("Préopératoire", "Utiliser un test fonctionnel plaquettaire en préopératoire pour identifier "
         "des dysfonctions plaquettaires (liées ou non aux AAP) quand elles sont suspectées sur une "
         "base clinique, dans les équipes ayant ce type de test à disposition et habituées à son "
         "utilisation.", "AE"),
        ("Pontage coronaire semi-urgent", "En cas de chirurgie de pontage coronaire semi-urgente, "
         "utiliser un test fonctionnel plaquettaire pour raccourcir les durées d'arrêt des AAP "
         "(inhibiteurs de P2Y12 en particulier), dans les équipes formées à son utilisation.", "AE"),
        ("Utilisation en POCT", "Si un test fonctionnel plaquettaire est utilisé en dehors du "
         "laboratoire (POCT), le faire en coordination avec l'équipe d'hémostase et le dispositif "
         "local de médecine de laboratoire, en accord avec la réglementation en vigueur, et en "
         "l'insérant dans une organisation codifiée avec les algorithmes transfusionnels retenus "
         "localement.", "AE"),
    ], [34*mm, PAGE_W-2*MARGIN-34*mm-16*mm, 16*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(P(
        "Principaux tests (Tableau II, source) : agrégation photométrique conventionnelle, "
        "thromboxane B2 sérique, test VASP, VerifyNow®, Multiplate®, ROTEM® Platelet, PFA "
        "(100/200), TEG® Platelet Mapping — non interchangeables, contraintes pré-analytiques "
        "variables. Aucun consensus sur la méthode à utiliser, ni sur les seuils de risque "
        "hémorragique. Il apparaît prématuré de recommander leur usage systématique pour évaluer "
        "le risque hémorragique chez tout patient traité par AAP, ou pour guider la transfusion "
        "plaquettaire en cas d'hémorragie.", S_NOTE))
    return story

def _section_2():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Moyens de neutralisation des AAP — propositions"))
    story.append(Spacer(1, 2*mm))
    story.append(theme_table([
        ("Principe", "Tenir compte du type d'AAP et de l'heure de la dernière prise (présence ou non "
         "d'un ou plusieurs métabolites actifs en circulation).", "AE"),
        ("Aspirine", "Transfuser des plaquettes, dose de 0,5 à 0,7 ×10¹¹ pour 10 kg de poids. Avec les "
         "formes galéniques autres qu'à libération prolongée, le produit actif disparaît de la "
         "circulation en moins de 2 heures.", "AE"),
        ("Clopidogrel / prasugrel", "Transfuser des plaquettes, à une dose plus élevée que pour "
         "l'aspirine (au moins le double, plus importante pour le prasugrel que pour le clopidogrel). "
         "Efficacité réduite si la dernière prise date de moins de 6 heures.", "AE"),
        ("Clopidogrel / prasugrel", "Ne pas administrer de rFVIIa pour neutraliser le clopidogrel ou "
         "le prasugrel.", "AE"),
        ("Ticagrelor", "Si dernière prise &lt; 24h : aucune prise en charge spécifique ne peut être "
         "recommandée (transfusion plaquettaire aux doses habituelles inefficace ; efficacité de "
         "fortes doses ou du rFVIIa non évaluée). Si dernière prise &gt; 24h : la transfusion "
         "plaquettaire pourrait permettre une neutralisation partielle.", "AE"),
        ("Acide tranexamique", "Administrer de l'acide tranexamique pour son efficacité à réduire le "
         "saignement, que le patient soit ou non traité par AAP.", "AE"),
        ("Desmopressine", "Ne pas utiliser la desmopressine pour neutraliser les AAP.", "AE"),
    ], [34*mm, PAGE_W-2*MARGIN-34*mm-16*mm, 16*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(P(
        "Le rFVIIa accélère la génération de thrombine mais son effet hémostatique n'est pas observé "
        "pour les thiénopyridines (clopidogrel/prasugrel) ; les données avec le ticagrelor sont "
        "limitées à un modèle animal. L'acide tranexamique n'a pas d'effet direct sur le "
        "fonctionnement plaquettaire mais réduit le saignement par son effet antifibrinolytique — "
        "à administrer dans les 3 premières heures en cas d'hémorragie traumatique.", S_NOTE))
    return story

def _section_3():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Procédure invasive non programmée — propositions"))
    story.append(Spacer(1, 2*mm))
    story.append(theme_table([
        ("Classification NCEPOD", "Distinguer procédures de sauvetage (minutes ; ex. rupture "
         "d'anévrisme aortique, syndrome de loge), procédures urgentes (heures ; ex. péritonite par "
         "perforation, ischémie aiguë de membre), procédures semi-urgentes (jours ; ex. décollement "
         "de rétine, syndrome occlusif sur tumeur).", "AE"),
        ("Durées d'interruption", "Quand possible (procédures semi-urgentes essentiellement), "
         "prendre en compte les durées optimales d'interruption : dernière prise d'aspirine à J-3, "
         "de clopidogrel et ticagrelor à J-5, de prasugrel à J-7 (+2 jours pour la neurochirurgie "
         "intracrânienne, quel que soit l'AAP).", "AE"),
        ("Monothérapie, non réalisable en délai", "Aspirine ou clopidogrel en monothérapie : débuter "
         "la procédure non neurochirurgicale sans neutralisation ; neutraliser avant un acte de "
         "neurochirurgie intracrânienne urgent ou de sauvetage.", "AE"),
        ("Bithérapie, non réalisable en délai", "Débuter la procédure non neurochirurgicale sans "
         "neutralisation — si le saignement per-procédural n'est pas contrôlable par l'opérateur "
         "senior et est attribué à la bithérapie, la neutraliser alors. Réaliser les procédures "
         "semi-urgentes plus de 24h après la dernière prise de prasugrel ou de ticagrelor. "
         "Neutraliser avant un acte de neurochirurgie intracrânienne urgent ou de sauvetage.", "AE"),
        ("ALR rachidienne", "Chez les patients sous inhibiteur de P2Y12 (mono- ou bithérapie), ne pas "
         "réaliser de geste d'anesthésie locorégionale rachidienne (rachianesthésie, péridurale).", "AE"),
    ], [34*mm, PAGE_W-2*MARGIN-34*mm-16*mm, 16*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(P("Encadrés du texte source : fracture du col fémoral — un traitement par "
                    "clopidogrel ne doit pas retarder la chirurgie. Moyens de neutralisation détaillés "
                    "en Question précédente.", S_NOTE))
    story.append(Spacer(1, 4*mm))

    story.append(P(
        "<i>Figure 1 — transcrite depuis l'algorithme de la page 12 du document source (vérifiée "
        "visuellement).</i>", S_NOTE))
    story.append(Spacer(1, 1.5*mm))
    story.append(info_panel(P(
        "<b>Figure 1 — Prise en charge des AAP pour une procédure invasive non programmée :</b><br/>"
        "Procédure réalisable sous AAP ? → <b>Oui</b> : réaliser la procédure. → <b>Non</b> :<br/>"
        "• <b>Procédure de sauvetage ou urgente</b> → neurochirurgicale ? Oui → neutralisation du/des "
        "AAP → réaliser la procédure. Non → commencer la procédure ; si saignement per-procédural "
        "non contrôlable attribué à la bithérapie antiplaquettaire → neutralisation du/des AAP.<br/>"
        "• <b>Procédure semi-urgente</b> → possibilité d'attendre les durées optimales d'interruption "
        "des AAP ? Oui → attendre puis réaliser la procédure. Non → même branche que "
        "sauvetage/urgente (neurochirurgicale ? oui/non...).",
        S_BODY_SM), bg=BG_PANEL, border=TEAL))
    return story

def _section_4():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Hémorragie associée aux AAP — propositions"))
    story.append(Spacer(1, 2*mm))
    story.append(P(
        "<b>Hémorragie grave</b> (définition HAS 2008, reprise pour les AVK) : présence d'au moins un "
        "critère parmi — hémorragie extériorisée non contrôlable par les moyens usuels ; instabilité "
        "hémodynamique (PAS &lt; 90 mmHg ou baisse de 40 mmHg, ou PAM &lt; 65 mmHg, ou tout signe de "
        "choc) ; nécessité d'un geste hémostatique urgent ; nécessité de transfusion de concentrés "
        "érythrocytaires ; localisation menaçant le pronostic vital ou fonctionnel (intracrânienne, "
        "intraspinale, intraoculaire/rétro-orbitaire, hémothorax, hémo-/rétropéritoine, "
        "hémopéricarde, hématome musculaire profond/syndrome de loge, hémorragie digestive aiguë, "
        "hémarthrose).", S_BODY_SM))
    story.append(Spacer(1, 2*mm))
    story.append(theme_table([
        ("Principe général", "Le traitement étiologique (gestes hémostatiques mécaniques) s'impose "
         "dans tous les cas, associé au traitement symptomatique (remplissage, vasopresseurs, "
         "transfusion de CGR, lutte contre l'hypothermie, acide tranexamique précoce).", "AE"),
        ("Hémorragie intracrânienne, neurochirurgie urgente indiquée", "Neutraliser le traitement "
         "antiplaquettaire en préopératoire.", "AE"),
        ("Hémorragie intracrânienne, pas de neurochirurgie urgente", "Ne pas transfuser de plaquettes "
         "si le patient est traité par aspirine et présente un score de Glasgow &gt; 8 à l'arrivée. "
         "Dans les autres cas, aucune proposition ne peut être faite ni en faveur ni en défaveur de "
         "la neutralisation. Interrompre les AAP dans tous les cas.", "AE"),
        ("Choc hémorragique, bithérapie", "Neutraliser le traitement antiplaquettaire.", "AE"),
        ("Autres hémorragies graves", "Neutraliser le traitement antiplaquettaire en cas de "
         "persistance de l'hémorragie après échec des traitements étiologiques et symptomatiques.", "AE"),
        ("Hémorragies non graves", "Traitement symptomatique, sans neutraliser le traitement "
         "antiplaquettaire (réévaluer systématiquement l'indication du traitement en cours).", "AE"),
    ], [34*mm, PAGE_W-2*MARGIN-34*mm-16*mm, 16*mm]))
    return story

def _section_5():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(P(
        "<i>Figure 2 — transcrite depuis l'algorithme de la page 13 du document source (vérifiée "
        "visuellement).</i>", S_NOTE))
    story.append(Spacer(1, 1.5*mm))
    story.append(info_panel(P(
        "<b>Figure 2 — Prise en charge des AAP en cas d'hémorragie :</b> hémorragie chez un patient "
        "traité par AAP → traitement symptomatique et étiologique, selon 4 branches :<br/>"
        "• <b>Hémorragie intracrânienne</b> → indication neurochirurgicale ? Oui → neutralisation du/"
        "des AAP. Non → GCS &gt; 8 : aspirine → pas de neutralisation de l'aspirine ; autre AAP → pas "
        "de proposition, discuter la neutralisation. GCS ≤ 8 → pas de proposition, discuter la "
        "neutralisation.<br/>"
        "• <b>Choc hémorragique</b> → bithérapie antiplaquettaire ? Oui → neutralisation des AAP. "
        "Non → pas de neutralisation des AAP.<br/>"
        "• <b>Hémorragie grave</b> → échec des traitements étiologiques et symptomatiques et "
        "persistance de l'hémorragie ? Oui → neutralisation du/des AAP. Non → pas de neutralisation.<br/>"
        "• <b>Hémorragie non grave</b> → pas de neutralisation du/des AAP.",
        S_BODY_SM), bg=BG_PANEL, border=TEAL))
    story.append(Spacer(1, 3*mm))

    story.append(section_bar("Tableau — moyens de neutralisation proposés (Figure 2)", color=GREY))
    story.append(Spacer(1, 2*mm))
    cw = PAGE_W - 2*MARGIN
    story.append(simple_table(
        ["AAP", "Moyens de neutralisation proposés"],
        [
            ["Aspirine", "Transfusion plaquettaire à dose standard (0,5-0,7 ×10¹¹ pour 10 kg de poids)"],
            ["Clopidogrel", "Transfusion plaquettaire : 2 × dose standard. Efficacité réduite si &lt; 6h après la dernière prise"],
            ["Prasugrel", "Transfusion plaquettaire : &gt; 2 × dose standard. Efficacité réduite si &lt; 6h après la dernière prise"],
            ["Ticagrelor", "Dernière prise &lt; 24h : pas de proposition (transfusion plaquettaire inefficace ; efficacité du rFVIIa non évaluée). Dernière prise &gt; 24h : transfusion plaquettaire pour une neutralisation partielle"],
        ],
        [cw*0.18, cw*0.82]))
    story.append(Spacer(1, 5*mm))

    story.append(section_bar("Sources et traçabilité", color=GREY))
    story.append(Spacer(1, 2*mm))
    story.append(P(
        "<b>Document source :</b> « Gestion des agents antiplaquettaires en cas de procédure "
        "invasive non programmée ou d'hémorragie » — Propositions du Groupe d'intérêt en hémostase "
        "périopératoire (GIHP) et du Groupe français d'études sur l'hémostase et la thrombose "
        "(GFHT), en collaboration avec la SFAR. A. Godier, D. Garrigue, D. Lasne, P. Fontana, "
        "F. Bonhomme, J.-P. Collet, et al. Anesth Reanim. 2019;5:218-237 "
        "(doi:10.1016/j.anrea.2018.10.003), disponible en ligne le 23/11/2018.", S_SOURCE))
    story.append(Spacer(1, 1.5*mm))
    story.append(P("<b>Méthodologie :</b> propositions rédigées par groupes de travail GIHP/GFHT, "
                    "validées par vote Delphi (n=38, accord fort si ≥70% d'accord) — pas de système "
                    "GRADE (voir légende page 1).", S_SOURCE))
    story.append(P("<b>URL source :</b> https://sfar.org/download/gestion-perioperatoire-des-patients-sous-aap-en-urgence/?wpdmdl=34414", S_SOURCE))
    story.append(Spacer(1, 3*mm))
    story.append(info_panel(P(
        "<b>Avertissement :</b> ce document est une fiche de synthèse indépendante, produite pour un "
        "usage d'aide-mémoire. Il reprend l'intégralité des propositions et des 2 algorithmes "
        "(Figures 1 et 2) du document source, mais ne remplace pas le texte intégral (argumentaire "
        "complet, références bibliographiques) et n'est ni édité ni validé par le GIHP, le GFHT ou "
        "la SFAR. En cas de doute, se référer au texte intégral et/ou à un avis spécialisé. Document "
        "de 2018 : vérifier l'existence d'une actualisation plus récente en cas de doute (un "
        "antidote du ticagrelor était en développement au moment de la rédaction).",
        S_BODY_SM), bg=GREY_LIGHT, border=GREY))
    return story

SECTIONS = [
    ("Méthodologie, pharmacologie & tests plaquettaires", _section_1),
    ("Moyens de neutralisation des AAP", _section_2),
    ("Procédure invasive non programmée", _section_3),
    ("Hémorragie associée aux AAP", _section_4),
    ("Algorithme hémorragie & traçabilité", _section_5),
]

def _make_doc():
    return SimpleDocTemplate(OUT, pagesize=A4,
                              leftMargin=MARGIN, rightMargin=MARGIN,
                              topMargin=32*mm, bottomMargin=16*mm,
                              title="Fiche GIHP/GFHT/SFAR 2018 - AAP en urgence",
                              author="Synthèse indépendante (source GIHP/GFHT/SFAR)")

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
