# -*- coding: utf-8 -*-
"""
Fiche de synthese - Conseil national de l'Ordre des medecins (CNOM), avec la
collaboration de la SFAR et de nombreuses societes savantes/syndicats.
"Recommandations concernant les relations entre anesthesistes-reanimateurs
et chirurgiens, autres specialistes ou professionnels de sante". Edition
decembre 2001 (actualisation d'un texte de mai 1994). 20 pages, telecharge
depuis sfar.org (wp-content/uploads/2014/04/196-reco-anesth-chir-autres-
2001.pdf).

METHODOLOGIE : 12e convention methodologique distincte de ce corpus - texte
purement DEONTOLOGIQUE/JURIDIQUE (articles du code de deontologie medicale,
decrets, articles du code de la sante publique), AUCUN systeme de cotation
scientifique, AUCUNE mention GRADE/niveau de preuve. Restitue en panneaux
d'information et tableaux thematiques, jamais en reco_table avec chip -
meme traitement que fiche_sauv.py et fiche_ponction_lombaire.py pour ce
type de document sans grille de preuve.

COUVERTURE : integrale - preface (Pr B. Hoerni, 2001), preambule (Pr B.
Glorion, 1994), principes deontologiques (generalites - refus de
collaboration, arbitrage des conflits ; obligation d'information - articles
35/36/64 du code de deontologie, recommandations ANAES, repartition
chirurgien/anesthesiste), principes d'organisation (demarches qualite,
charte de fonctionnement), les structures (etablissement public - service,
structure federative, rattachement des secteurs de soins intensifs ;
etablissement prive - conflits d'honoraires, de gestion), la mise en oeuvre
aux relations anesthesiste-chirurgien (9 points : consultation
pre-anesthesique, consultation de cardiologie, programme operatoire,
surveillance post-interventionnelle, soins intensifs et reanimation
chirurgicale, hospitalisation, anesthesie/sedation par des non-
anesthesistes, chirurgie ambulatoire, transfusions sanguines),
sages-femmes/gynecologues-obstetriciens/anesthesistes-reanimateurs (analgesie
peridurale obstetricale), infirmier(e)s anesthesistes diplome(e)s d'Etat
(IADE - competences, responsabilites exclusives du medecin), et les
remerciements (liste complete du groupe de travail 2001, avec titres de
fonction et le remerciement particulier a Lienhart/Fagniez).

CORRECTIONS POST-AUDIT : un audit independant (subagent aveugle au
brouillon) a trouve que le premier jet, malgre son propre docstring
affirmant "rien n'est omis", omettait en realite : la quasi-totalite du
contenu propre de la Preface 2001 (decrets 95-1000/98-899/98-900,
motivation demographique/juridique) - ajoutee ; le point IVG/sterilisation
contraceptive (loi n 2001-586) en 1.1, et la phrase sur les condamnations
pour manque de cooperation - ajoutes ; l'article 42 (renvoi dans la
citation de l'art. 36) - ajoute ; le point evaluation des pratiques
professionnelles en 2.1 - ajoute ; le detail dossier medical en 1.2,
protocoles therapeutiques en 4.6, info patient en 4.9, materiel/
medicaments des sages-femmes et dossier medical commun en 5, plage
D.712-40 a 51 en 4.1 - ajoutes ; la clause "cardiologue, pneumologue" et
la phrase "intervenir sans delai" en 6 (IADE) - ajoutees ; Mme Rolande
GRENTE (Ordre des sages-femmes), absente de la premiere liste de
remerciements, et le paragraphe de remerciement particulier a Lienhart/
Fagniez - ajoutes, avec restauration des titres de fonction exacts de
chaque personne citee. DISCLOSURE non resolue (regle CLAUDE.md point 5) :
la source cite le meme texte legislatif du 4 juillet 2001 sous deux
numeros differents - "loi n 2001-586" (1.1, clause de conscience
sterilisation) et "loi n 2001-588" (1.2, consentement d'une mineure a
l'IVG) - reproduits tels quels, la divergence signalee explicitement dans
le corps du texte (1.2) plutot que tranchee.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from style import *
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.units import mm

OUT = "/home/user/rfe-sfar-website/output/Fiche_CNOM_SFAR_Relations_Anesthesistes_Chirurgiens_2001.pdf"

SOURCE_TXT = ("Source : « Recommandations concernant les relations entre "
              "anesthésistes-réanimateurs et chirurgiens, autres spécialistes ou "
              "professionnels de santé » — Conseil national de l'Ordre des médecins, "
              "édition décembre 2001. Fiche de synthèse non officielle : se référer au "
              "texte intégral.")

def P(txt, style=S_CELL):
    return Paragraph(txt, style)

CW_FULL = PAGE_W - 2 * MARGIN

def theme_table(rows, col_widths, head=("Thème", "Détail")):
    data = [[P(head[0], S_HEAD_W), P(head[1], S_HEAD_W)]]
    for theme, detail in rows:
        data.append([P(theme, S_CELL_B), P(detail, S_CELL)])
    t = Table(data, colWidths=col_widths, repeatRows=1)
    style_cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), NAVY), ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTNAME", (0, 0), (-1, 0), FONT_BOLD), ("FONTSIZE", (0, 0), (-1, 0), 8),
        ("VALIGN", (0, 0), (-1, -1), "TOP"), ("ALIGN", (0, 1), (0, -1), "LEFT"),
        ("GRID", (0, 0), (-1, -1), 0.5, GREY_LIGHT),
        ("TOPPADDING", (0, 0), (-1, -1), 3.4), ("BOTTOMPADDING", (0, 0), (-1, -1), 3.4),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            style_cmds.append(("BACKGROUND", (0, i), (-1, i), BG_PANEL))
    t.setStyle(TableStyle(style_cmds))
    return t

TCW = [48 * mm, CW_FULL - 48 * mm]

def bullets(items, style=S_BODY_SM):
    html = "&bull; " + "<br/>&bull; ".join(items)
    return P(html, style)

TOTAL_PAGES = {"n": 6}

def on_page(canvas, doc, page_title):
    header_band(canvas, doc, "CONSEIL NATIONAL DE L'ORDRE DES MÉDECINS — ÉDITION 2001",
                "Relations anesthésistes-réanimateurs / chirurgiens",
                page_title, icon_fn=lambda c, x, y: icon_shield(c, x, y, 13 * mm), color=NAVY)
    footer_band(canvas, doc, SOURCE_TXT, f"Page {doc.page} / {TOTAL_PAGES['n']}")

# ---------------------------------------------------------------------------
def _section_intro():
    story = []
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Champ :</b> recommandations du Conseil national de l'Ordre des médecins "
        "(CNOM), avec la collaboration de la SFAR et de nombreuses sociétés savantes "
        "et syndicats, sur les relations entre anesthésistes-réanimateurs et "
        "chirurgiens, autres spécialistes ou professionnels de santé (sages-femmes, "
        "infirmiers anesthésistes). Texte de mai 1994, actualisé et réédité en "
        "décembre 2001.", S_BODY), bg=BG_PANEL, border=TEAL))
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Méthodologie :</b> ce texte est <b>déontologique et juridique</b> — articles "
        "du code de déontologie médicale, décrets, articles du code de la santé "
        "publique, recommandations de l'ANAES. Il ne comporte <b>aucun système de "
        "cotation scientifique</b> (pas de GRADE, pas de niveau de preuve) : chaque "
        "recommandation est une règle de bonne pratique organisationnelle ou une "
        "obligation légale/déontologique, restituée ici en panneaux et tableaux "
        "thématiques, jamais en chip de grade inventé.", S_BODY_SM),
        bg=AMBER_LIGHT, border=AMBER))
    story.append(Spacer(1, 3 * mm))
    story.append(section_bar("Préface (2001) & préambule (1994)"))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>Préface (Pr Bernard Hoerni, 17 octobre 2001) :</b> depuis 1994, de "
        "nouvelles questions sont apparues (dont l'information du patient) et de "
        "nombreux textes réglementaires ont été publiés — le nouveau code de "
        "déontologie médicale (<b>décret n° 95-1000</b> du 6 septembre 1995), le "
        "décret n° 94-1050 du 5 décembre 1994 sur la pratique de l'anesthésie, les "
        "<b>décrets n° 98-899 et 98-900</b> du 9 octobre 1998 sur les activités "
        "d'obstétrique, de néonatologie ou de réanimation néonatale. Les praticiens, "
        "de plus en plus préoccupés par les risques judiciaires, sollicitent l'aide de "
        "leur Ordre et de leurs organisations professionnelles ; les initiatives des "
        "professionnels (référentiels) et des pouvoirs publics (accréditation) en "
        "matière d'assurance qualité se sont multipliées ; le déclin annoncé de la "
        "démographie médicale dans certaines spécialités chirurgicales, et surtout "
        "chez les anesthésistes-réanimateurs, rend impérieux un relèvement du numerus "
        "clausus. D'où l'actualisation de ces recommandations.", S_BODY_SM))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "L'anesthésiste-réanimateur, initialement partenaire du chirurgien, est devenu "
        "le collaborateur privilégié d'un grand nombre de spécialistes. Son statut de "
        "spécialiste à part entière reste original : son action se confond dans le temps "
        "et l'espace avec celle du chirurgien ou du spécialiste avec lequel il "
        "collabore, d'où un consensus incontournable, seule garantie pour le patient. "
        "Ce texte rappelle les responsabilités des uns et des autres, dans un esprit de "
        "respect mutuel et de confraternité.", S_BODY_SM))
    story.append(Spacer(1, 2.5 * mm))
    story.append(section_bar("1 — Les principes déontologiques"))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P("<b>1.1 — Généralités :</b> les règles du code de déontologie "
                    "s'appliquent entre confrères de disciplines différentes mais "
                    "complémentaires — pas d'injure, d'insulte ou de calomnie, pas de "
                    "pression matérielle ou morale. Nul médecin ne doit entreprendre "
                    "d'actes pour lesquels il n'est pas compétent (art. 32 et 70) : "
                    "recours à un tiers compétent chaque fois que nécessaire.",
                    S_BODY_SM))
    story.append(Spacer(1, 1.2 * mm))
    story.append(P(
        "Chirurgien et anesthésiste-réanimateur forment une équipe de spécialités "
        "complémentaires ; le chirurgien, habituellement premier consulté, organise la "
        "prise en charge chirurgicale. La réunion de plusieurs compétences implique une "
        "décision collective, la responsabilité restant individuelle (art. 64). "
        "L'article 64 permet à chaque médecin de refuser librement sa collaboration ou "
        "de la retirer, à condition de ne pas nuire au patient et d'en avertir ses "
        "confrères — faculté à utiliser avec précaution (la juridiction ordinale a "
        "sanctionné des manquements aux devoirs de dévouement et de continuité des "
        "soins, en particulier en situation d'urgence, sans gradation prévue par "
        "l'article 47). Un refus de collaboration suppose une information préalable "
        "argumentée sur des éléments objectifs.", S_BODY_SM))
    story.append(Spacer(1, 1.2 * mm))
    story.append(P(
        "L'échange d'informations réciproques doit être le plus large possible (dialogue "
        "et écrit) : le chirurgien informe l'anesthésiste des constatations de son "
        "examen, des propositions thérapeutiques et de l'importance de l'intervention ; "
        "l'anesthésiste informe l'opérateur de toute contre-indication anesthésique ou "
        "difficulté suspectée. L'opérateur doit tenir compte de l'avis de l'anesthésiste "
        "et ne peut lui imposer d'agir contre sa conscience (clause de conscience pour "
        "l'IVG, art. 18 — de même, selon la loi n° 2001-586 du 4 juillet 2001 relative à "
        "l'IVG et à la contraception, un médecin n'est jamais tenu de pratiquer une "
        "stérilisation à visée contraceptive, mais doit en informer l'intéressée dès la "
        "première consultation). En cas de désaccord, une conciliation doit être "
        "recherchée (confrères, hiérarchie médicale, CME/conférence médicale, instances "
        "ordinales) — le patient ne doit jamais être témoin ou otage du différend. Des "
        "condamnations ont été prononcées contre des chirurgiens et des anesthésistes-"
        "réanimateurs non pas en raison de fautes techniques propres à chaque "
        "discipline, mais pour un manque de coopération préjudiciable au patient.",
        S_BODY_SM))
    return story

def _section_information():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("1.2 — L'obligation d'information"),
        Spacer(1, 1.5 * mm),
        P("Principes fixés par le code de déontologie : <b>art. 35</b> (information "
          "loyale, claire et appropriée) ; <b>art. 36</b> (consentement recherché dans "
          "tous les cas, respect du refus après information des conséquences, "
          "information des proches si le patient ne peut exprimer sa volonté sauf "
          "urgence — les obligations envers un mineur ou un majeur protégé sont "
          "définies à l'<b>art. 42</b>) ; <b>art. 64</b> (médecins collaborant à un "
          "traitement, information mutuelle, chacun veillant à l'information du "
          "malade). L'ANAES recommande que "
          "chaque médecin informe des éléments relevant de sa discipline, sans supposer "
          "que d'autres l'ont déjà fait.", S_BODY),
    ]))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P("Contenu de l'information selon l'ANAES : état du patient et "
                    "évolution prévisible ; description des examens/soins/interventions "
                    "envisagés et de leurs alternatives ; objectif, utilité, bénéfices "
                    "escomptés ; conséquences et inconvénients ; complications et "
                    "risques (y compris exceptionnels) ; précautions recommandées.",
                    S_BODY_SM))
    story.append(Spacer(1, 1.2 * mm))
    story.append(P(
        "<b>Répartition :</b> le chirurgien (ou tout opérateur) informe sur la maladie, "
        "l'évolution sans traitement, le motif et les modalités de l'intervention, ses "
        "avantages/conséquences/inconvénients/risques et alternatives ; l'anesthésiste-"
        "réanimateur informe sur la technique anesthésique envisagée, ses avantages/"
        "inconvénients/risques/alternatives, et sur le terrain du patient. Chevauchement "
        "inévitable entre les deux informations, à gérer avec tact (chacun donne une "
        "idée du risque global, sans esquiver les questions ni les « renvoyer » sur le "
        "confrère). Le dossier médical doit conserver une trace écrite de l'information "
        "donnée, et permettre à tout médecin devant apporter ses soins au patient de "
        "comprendre la nature de l'intervention chirurgicale, de la technique "
        "anesthésique et de l'éventuelle réanimation envisagées ; si le médecin "
        "informant n'est pas celui qui interviendra, il en informe le patient et "
        "transmet les renseignements nécessaires.", S_BODY_SM))
    story.append(Spacer(1, 1.2 * mm))
    story.append(P(
        "Cas particulier : une mineure peut consentir seule à une IVG et aux actes liés "
        "(loi n° 2001-588 du 4 juillet 2001) — l'anesthésiste doit s'assurer que ce "
        "consentement a bien été obtenu. <i>Disclosure : la source cite ce même texte "
        "législatif du 4 juillet 2001 sous deux numéros différents à deux endroits "
        "(« n° 2001-586 » en 1.1 à propos de la clause de conscience pour la "
        "stérilisation contraceptive, « n° 2001-588 » ici) — incohérence interne "
        "reproduite telle quelle, non tranchée par cette fiche.</i>", S_NOTE))
    return story

def _section_intro_information():
    story = _section_intro()
    story.append(Spacer(1, 2 * mm))
    story.extend(_section_information())
    return story

# ---------------------------------------------------------------------------
def _section_organisation_structures():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("2 — Principes d'organisation"),
        Spacer(1, 1.5 * mm),
        P("<b>2.1 — Démarches qualité :</b> l'accréditation des établissements de soins "
          "(décret n° 97-311) engage à la validation de procédures écrites ; il est "
          "recommandé que anesthésistes-réanimateurs, chirurgiens et autres "
          "professionnels rédigent et cosignent des chartes de fonctionnement, prenant "
          "en compte les recommandations de bonne pratique des sociétés savantes "
          "validées par l'ANAES. Le développement de l'évaluation des pratiques "
          "professionnelles, qui a reçu une consécration législative et "
          "réglementaire pour les médecins libéraux, participe de la même évolution.",
          S_BODY),
    ]))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>2.2 — Charte de fonctionnement</b> des équipes anesthésiques et "
        "chirurgicales : nécessaire, portant sur 5 points — la consultation "
        "d'anesthésie, le programme opératoire, le réveil anesthésique, les soins "
        "intensifs/réanimation chirurgicale, et l'hospitalisation. Pour chaque point, "
        "la répartition des tâches et responsabilités (séparées ou solidaires selon "
        "l'organisation publique/privée) doit être explicite.", S_BODY_SM))
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("3 — Les structures"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(theme_table([
        ("3.1 — Établissement public",
         "L'activité s'exerce dans le cadre d'un service (éventuellement regroupé en "
         "structure fédérative en CHU, ou subdivisé en unités fonctionnelles). "
         "Affectation des anesthésistes par le chef de service, en tenant compte de "
         "leur souhait. Ils relèvent de l'autorité du chef de service d'anesthésie-"
         "réanimation, mais participent aux activités du service de chirurgie où ils "
         "travaillent, et disposent de locaux propres. Le médecin anesthésiste est "
         "responsable du fonctionnement de la SSPI. Rattachement des secteurs de soins "
         "intensifs/réanimation chirurgicale selon leur fonctionnement réel : rattaché "
         "à l'anesthésie-réanimation si ouvert à plusieurs services de chirurgie ; si "
         "rattaché à un service de chirurgie, la responsabilité thérapeutique et "
         "l'autorité médicale des anesthésistes y travaillant doivent être reconnues "
         "(désignation d'un praticien responsable par accord entre chefs de service)."),
        ("3.2 — Établissement privé",
         "Relations globalement similaires au public, mais conflits plus spécifiques "
         "liés aux intérêts individuels : fixation des honoraires (secteurs "
         "conventionnels choisis librement, tact et mesure — art. 53/54 — ; difficulté "
         "pour le devis des actes esthétiques, arrêté du 17/10/1996) ; critères de "
         "gestion (le statut de propriétaire/actionnaire majoritaire ne peut justifier "
         "la privation de moyens indispensables aux patients ni des contraintes "
         "abusives — art. 71). Prévention : respect de la déontologie, contrats soumis "
         "à l'Ordre, conférences médicales."),
    ], TCW, head=("Structure", "Points clés")))
    return story

def _section_organisation_structures_information():
    story = _section_intro_information()
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_organisation_structures())
    return story

# ---------------------------------------------------------------------------
MISE_EN_OEUVRE_ROWS = [
    ("4.1 — Consultation pré-anesthésique",
     "Obligatoire (décret n° 94-1050, codifié aux articles D.712-40 à D.712-51 du code "
     "de la santé publique) pour toute anesthésie générale ou locorégionale ; "
     "réalisée à distance de l'intervention pour un consentement libre et éclairé. "
     "L'opérateur rappelle son intérêt et sa nécessité au patient. Intégrée dans une "
     "procédure commune d'évaluation préopératoire. Locaux, moyens et secrétariat "
     "adéquats nécessaires (accord explicite public/privé). Il est préférable que "
     "l'anesthésiste consultant réalise lui-même la visite pré-anesthésique et "
     "l'anesthésie ; sinon, le patient en est informé et le médecin qui opère prend "
     "connaissance du dossier avant l'intervention — d'où l'importance d'un dossier "
     "médical de qualité, lisible. La multiplication injustifiée des intervenants "
     "dilue les responsabilités et augmente les risques de défaut de communication."),
    ("4.2 — Consultation de cardiologie (ou autre spécialiste) à l'occasion d'une "
     "anesthésie",
     "4 principes : (1) demande précise, réponse en rapport ; le consultant informe le "
     "patient si une nouvelle discussion s'impose avant décision définitive ; "
     "(2) anesthésiste et opérateur se tiennent mutuellement informés des demandes et "
     "résultats ; (3) la décision finale de l'indication et des modalités d'anesthésie "
     "relève de l'anesthésiste-réanimateur ; (4) en cas de désaccord, chacun assume ses "
     "responsabilités dans son domaine, mais une concertation réelle doit précéder la "
     "décision."),
    ("4.3 — Le programme opératoire",
     "Établi par les médecins opérateurs, les anesthésistes concernés et le responsable "
     "du secteur opératoire (décret n° 94-1050, art. D.712-42), tenant compte des "
     "disponibilités de chacun — on ne peut imposer plusieurs anesthésies simultanées à "
     "un anesthésiste. Réalisé conjointement (chirurgiens, spécialistes, anesthésistes, "
     "responsables du bloc), horaires/ordre d'un commun accord, ponctualité de tous. "
     "Recommandé par écrit, signé au plus tard la veille. Gestion des urgences définie "
     "à l'avance ; conseils de blocs opératoires encouragés (publics et privés)."),
    ("4.4 — La surveillance post-interventionnelle",
     "Le réveil, temps périlleux de l'anesthésie : fonctionnement de la SSPI "
     "prioritaire (moyens définis au décret n° 94-1050, art. D.712-47/49). Suivi sous "
     "surveillance conjointe chirurgien/anesthésiste ; l'anesthésiste précise par écrit "
     "nature et rythme des soins, le chirurgien consigne par écrit ses prescriptions "
     "post-opératoires immédiates (drains, plaie, aspirations) sur le même document "
     "versé au dossier. Le personnel de SSPI documente chaque acte et l'heure d'entrée/"
     "sortie. La sortie de SSPI n'est décidée que par l'anesthésiste-réanimateur "
     "(examen conscience/fonctions vitales) ; l'orientation ultérieure "
     "(hospitalisation/soins intensifs) est une décision commune."),
    ("4.5 — Les soins intensifs et la réanimation chirurgicale",
     "Le patient orienté en soins intensifs/réanimation chirurgicale est sous la "
     "responsabilité médicale de l'anesthésiste-réanimateur ; certaines décisions "
     "restent au chirurgien (mobilisation, ablation sondes/drains). Techniques de "
     "réanimation et prescriptions médicamenteuses : anesthésiste-réanimateur, sur "
     "protocole écrit précisant les domaines de chacun ; prescriptions écrites, datées "
     "et signées (décret n° 93-221 sur les infirmiers), en particulier pour "
     "antibiotiques/anticoagulants et pour les examens biologiques/radiologiques "
     "(interprétation visée par le prescripteur, jamais anonyme). Entrée/sortie de ces "
     "secteurs sur accord conjoint."),
    ("4.6 — L'hospitalisation",
     "Le patient retourné en hospitalisation est sous la responsabilité de l'opérateur, "
     "qui répond des suites opératoires ; le règlement interne précise les procédures "
     "en cas d'événement inopiné/complication tardive. Règles de fonctionnement "
     "formalisées après concertation plutôt que des accords tacites, pour limiter les "
     "erreurs de transmission. Selon les façons de travailler de l'équipe, les "
     "protocoles thérapeutiques préciseront des modalités strictes ou une politique "
     "plus générale de prescription, dans le but de préserver un plus large espace de "
     "liberté ; les prescriptions devront être consignées par écrit. En urgence, la "
     "déontologie exclut qu'un médecin se retranche derrière sa spécialité pour "
     "s'exonérer de sa mission d'assistance en cas de complication post-opératoire."),
    ("4.7 — Anesthésie/sédation par des spécialistes non anesthésistes-réanimateurs",
     "Une anesthésie générale ou locorégionale ne peut être mise en œuvre sans "
     "anesthésiste-réanimateur (déontologie et code de la santé publique, art. D.712-40 "
     "et suivants ; art. 40 interdisant un risque injustifié). L'anesthésie locale/"
     "sédation par un chirurgien ou autre opérateur requiert formation/expérience "
     "particulières et, le cas échéant, le concours de l'anesthésiste — règlement "
     "écrit fixant les modalités (consultation pré-anesthésique, prémédication, "
     "présence obligatoire ou de recours, passage en SSPI, antalgie post-opératoire). "
     "Spécificité notée pour les cardiologues en USIC. En conclusion : soit un acte "
     "nécessite un anesthésiste, soit non — les situations intermédiaires sont à "
     "éviter."),
    ("4.8 — La chirurgie ambulatoire",
     "Chirurgie programmée et organisée (décret n° 92-1102, art. D.712-30 à 34), "
     "patient au centre du fonctionnement du fait de la très courte durée de séjour. "
     "Contraintes : amplitude d'ouverture ≤ 12 h ; présence minimale permanente d'un "
     "médecin qualifié plus, en sus, présence permanente d'un anesthésiste-réanimateur "
     "dans la structure. Le patient reçoit à sa sortie un bulletin signé mentionnant "
     "les intervenants et les consignes post-opératoires/anesthésiques (art. D.712-33). "
     "Règlement intérieur commun (fonctionnement médical, sortie concertée, "
     "organisation des présences) fait respecter par un médecin coordonnateur (art. "
     "D.712-34)."),
    ("4.9 — Les transfusions sanguines",
     "Responsabilité au chirurgien, à l'anesthésiste, ou aux deux. Préopératoire : le "
     "chirurgien détient l'essentiel de l'information (technique, difficultés "
     "prévisibles, risque hémorragique) à porter au dossier ; l'anesthésiste évalue "
     "les besoins et organise les moyens. Chacun tient le patient informé de "
     "l'éventualité ou de la nécessité de la transfusion. Peropératoire : information "
     "mutuelle, le "
     "chirurgien vérifie sa transmission ; l'anesthésiste commande qualitativement/"
     "quantitativement les produits et réalise la transfusion. Post-opératoire : "
     "responsabilité selon l'organisation (anesthésiste si soins intensifs sous sa "
     "responsabilité continue ; sinon chirurgien). Documents portant toujours le nom "
     "lisible du prescripteur ; motif de la transfusion tracé au dossier ; règlement "
     "intérieur recommandé sur ce point."),
]

def _section_mise_en_oeuvre():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("4 — Mise en œuvre des principes aux relations anesthésiste-"
                    "chirurgien"),
        Spacer(1, 1.5 * mm),
    ]))
    story.append(theme_table(MISE_EN_OEUVRE_ROWS, TCW, head=("Point", "Recommandations")))
    return story

# ---------------------------------------------------------------------------
def _section_sages_femmes():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("5 — Sages-femmes, gynécologues-obstétriciens et anesthésistes-"
                    "réanimateurs"),
        Spacer(1, 1.5 * mm),
        P("Les sages-femmes, profession médicale à part entière (Ordre et code de "
          "déontologie propres), sont régies par des textes législatifs et "
          "réglementaires déterminant leurs règles d'exercice professionnel et fixant "
          "le matériel qu'elles peuvent employer et les médicaments qu'elles peuvent "
          "prescrire. Elles doivent appeler le gynécologue-obstétricien de garde "
          "en cas d'accouchement dystocique ou de suites de couches pathologiques, et "
          "un médecin anesthésiste-réanimateur pour tout acte autorisé susceptible de "
          "nécessiter une anesthésie autre que locale. Pour les autres actes, la "
          "prescription d'intervention est faite par le gynécologue-obstétricien, le "
          "choix de la technique anesthésique revenant à l'anesthésiste.", S_BODY),
    ]))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>Analgésie périmédullaire :</b> pour un accouchement présumé normal, la "
        "demande peut provenir de la parturiente (déjà vue en consultation "
        "pré-anesthésique) — dès accord de principe de l'équipe obstétricale, la "
        "sage-femme apprécie le moment et transmet à l'anesthésiste. Pour une cause "
        "médicale/obstétricale, la demande est faite par le gynécologue-obstétricien. "
        "La décision de réalisation et de technique appartient au médecin "
        "anesthésiste-réanimateur. Si la parturiente n'a jamais consulté dans la "
        "maternité, la demande vient du gynécologue-obstétricien et la réalisation "
        "dépend d'une consultation pré-anesthésique en urgence et des examens de "
        "laboratoire disponibles. La sage-femme s'assure de la disponibilité des "
        "praticiens de garde/astreinte (charte à préciser). L'anesthésiste, s'il le "
        "juge nécessaire, contacte le gynécologue-obstétricien.", S_BODY_SM))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "La sage-femme peut participer à l'entretien de l'analgésie locorégionale "
        "(hors période d'expulsion) si un anesthésiste est à tout moment disponible à "
        "proximité — réinjections par le dispositif posé par le médecin (première "
        "injection médicale obligatoire), selon prescriptions écrites et signées ou "
        "protocoles validés (modalités, temps de sécurité entre injections, "
        "posologies/débit des pompes, ablation du cathéter péridural). La surveillance "
        "de l'analgésie péridurale par la sage-femme suppose sa disponibilité et sa "
        "compétence : elle ne peut être contrainte à d'autres soins pendant cette "
        "surveillance ; tout événement particulier est consigné au dossier "
        "d'anesthésie. L'anesthésiste et le gynécologue-obstétricien restent "
        "disponibles pendant tout le séjour en salle de naissance, avec délais "
        "compatibles avec la sécurité. Toute sage-femme qui s'estime ne pas être en "
        "mesure d'assurer une technique en sécurité peut légitimement refuser sa prise "
        "en charge. De façon générale, la tenue d'un dossier médical rempli par les "
        "différents intervenants et comprenant l'ensemble des données intéressant le "
        "déroulement de l'accouchement permet d'améliorer la prise en charge de la "
        "parturiente. Des réunions de concertation régulières (chartes, protocoles, "
        "information sur les nouveaux produits) sont recommandées.", S_BODY_SM))
    return story

def _section_iade():
    story = []
    story.append(Spacer(1, 2.5 * mm))
    story.append(KeepTogether([
        section_bar("6 — Les infirmier(e)s anesthésistes diplômé(e)s d'État (IADE)"),
        Spacer(1, 1.5 * mm),
        P("L'anesthésie est un acte médical ne pouvant être pratiqué que par un médecin "
          "anesthésiste-réanimateur qualifié. L'IADE aide le médecin mais ne peut "
          "entreprendre seul une anesthésie, quel qu'en soit le type, en l'absence "
          "d'un médecin qualifié. Il est sous la responsabilité exclusive du médecin "
          "anesthésiste-réanimateur et/ou du chef de service — aucun autre spécialiste "
          "ne peut s'y substituer ou l'autoriser à exercer seul.", S_BODY),
    ]))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "Le médecin peut confier temporairement à l'IADE, sous sa propre "
        "responsabilité, la surveillance d'un patient anesthésié ne présentant pas de "
        "risque particulier, à condition d'être immédiatement joignable et disponible "
        "à proximité. L'IADE participe à toute ALR et pratique des réinjections dès "
        "lors que le dispositif a été posé par un médecin, sur prescription écrite. "
        "En cas de protocole écrit de soins d'urgence/actes conservatoires jusqu'à "
        "l'intervention d'un médecin, l'IADE remet un compte rendu écrit, daté et "
        "signé.", S_BODY_SM))
    story.append(Spacer(1, 1.2 * mm))
    story.append(P(
        "L'anesthésiste doit pouvoir être assisté par un autre médecin et/ou un IADE si "
        "nécessaire (début/fin d'anesthésie, moments délicats, complications, actes à "
        "risque spécifique) — la présence d'un médecin anesthésiste auprès d'un IADE "
        "est toujours nécessaire. Hors bloc, les IADE interviennent en SSPI, assurent "
        "le transport intra-établissement des patients anesthésiés/réanimés, exercent "
        "en soins intensifs/réanimation chirurgicale (toujours sous responsabilité "
        "médicale). Le décret n° 94-1050 (art. D.712-49) impose la présence "
        "permanente d'au moins un IDE formé (si possible IADE) en SSPI, et au moins "
        "deux agents dont un IDE formé si la SSPI a ≥ 6 postes occupés — ce personnel "
        "paramédical est placé sous la responsabilité médicale d'un médecin "
        "anesthésiste-réanimateur qui doit pouvoir intervenir sans délai. Les IADE "
        "peuvent participer aux transports inter/intra-hospitaliers et pratiquer des "
        "gestes sur prescription du médecin de l'équipe ; le SMUR étant un service "
        "médicalisé, l'IADE ne peut l'assurer seul.", S_BODY_SM))
    story.append(Spacer(1, 1.2 * mm))
    story.append(P("Responsabilités demeurant du ressort exclusif du médecin "
                    "anesthésiste-réanimateur :", S_BODY_SM))
    story.append(Spacer(1, 1 * mm))
    story.append(bullets([
        "la consultation pré-anesthésique, même si l'anesthésiste peut s'entourer "
        "d'autres avis spécialisés (cardiologue, pneumologue…) ;",
        "la prescription de l'anesthésie (type, agents, modalités de surveillance) ;",
        "le geste technique d'ALR (bloc tronculaire/plexique, rachianesthésie, "
        "péridurale/caudale, anesthésie locale IV) ;",
        "la prescription de médicaments ou transfusions rendus nécessaires en cours "
        "d'anesthésie ;",
        "la mise en œuvre de techniques invasives (voies veineuses profondes, sondes "
        "de Swan-Ganz) ;",
        "la prescription des soins et examens post-opératoires ;",
        "la décision de sortie de la salle de surveillance post-interventionnelle.",
    ]))
    return story

def _section_sources():
    story = []
    story.append(section_bar("Sources et traçabilité", color=GREY))
    story.append(Spacer(1, 2 * mm))
    story.append(P(
        "<b>Document source :</b> « Recommandations concernant les relations entre "
        "anesthésistes-réanimateurs et chirurgiens, autres spécialistes ou "
        "professionnels de santé ». Conseil national de l'Ordre des médecins, en "
        "collaboration avec la SFAR et de nombreuses sociétés savantes/syndicats "
        "(cardiologie, endoscopie digestive, chirurgie digestive, gynécologie-"
        "obstétrique, radiologie, Ordre des sages-femmes, syndicats d'anesthésistes-"
        "réanimateurs).", S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>Version :</b> texte original mai 1994 (Pr Bernard Glorion, préambule) ; "
        "édition actualisée décembre 2001 (Pr Bernard Hoerni, préface), réunions de "
        "travail des 12 janvier, 23 février, 21 mars, 6 avril et 29 juin 2001.",
        S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P("<b>Méthodologie :</b> texte déontologique/juridique — articles du "
                    "code de déontologie médicale, décrets et code de la santé "
                    "publique, recommandations ANAES ; aucun système de cotation "
                    "scientifique — voir disclosure méthodologique en page 1.",
                    S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>URL source :</b> https://sfar.org/wp-content/uploads/2014/04/"
        "196-reco-anesth-chir-autres-2001.pdf", S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P("<b>Couverture :</b> cette fiche reprend l'intégralité du texte "
                    "(préface, préambule, principes déontologiques, principes "
                    "d'organisation, les structures, mise en œuvre en 9 points, "
                    "sages-femmes/gynécologues-obstétriciens, IADE).", S_SOURCE))
    story.append(Spacer(1, 1.5 * mm))
    story.append(P(
        "<b>Remerciements (groupe de travail 2001) :</b> Pr J.-Y. Artigou, Secrétaire "
        "de la Société française de cardiologie ; Mme N. Atéchian, Présidente du "
        "Conseil national de l'Ordre des sages-femmes ; Mme F. Bicheron, Conseil "
        "national de l'Ordre des sages-femmes ; Dr J.-M. Canard, Secrétaire général de "
        "la Société française d'endoscopie digestive ; Dr G.-M. Cousin, Secrétaire "
        "général du Syndicat national des gynécologues et obstétriciens français ; "
        "Dr J.-M. Dumeix, Président du Syndicat national des anesthésiologistes-"
        "réanimateurs français ; Pr J. Escourrou, Société française d'endoscopie "
        "digestive ; Pr P.-L. Fagniez, Président de la section de chirurgie digestive "
        "au Conseil national des Universités ; Dr J. Garric, ex-Président du Syndicat "
        "national des praticiens hospitaliers anesthésistes-réanimateurs ; "
        "Pr J.-R. Giraud, Président du Syndicat national des gynécologues et "
        "obstétriciens français ; Pr B. Glorion, Mme R. Grente, Dr D. Grunwald, "
        "Pr J. Langlois et Dr F.-X. Léandri (Conseil national de l'Ordre des "
        "médecins) ; Pr P. Legmann, Société française de radiologie ; Dr M. Lévy, "
        "Secrétaire général du Syndicat national des anesthésiologistes-réanimateurs "
        "français ; Pr A. Lienhart, Président de la SFAR ; Dr M. Malafosse, Président "
        "de l'Association française de chirurgie ; Dr J. Meurette, Président de "
        "l'Union des chirurgiens français ; Dr M. Palot, SFAR ; Dr R. Torrielli, "
        "Syndicat national des praticiens hospitaliers anesthésistes-réanimateurs "
        "français ; et en collaboration avec le Syndicat national des médecins "
        "anesthésistes-réanimateurs des hôpitaux non universitaires. Remerciement "
        "particulier aux Pr A. Lienhart et Pr P.-L. Fagniez pour la constance de leur "
        "collaboration et la pertinence de leurs réflexions.", S_SOURCE))
    story.append(Spacer(1, 3 * mm))
    story.append(info_panel(P(
        "<b>Avertissement — document de 2001 :</b> ce document est une fiche de "
        "synthèse indépendante, produite pour un usage d'aide-mémoire. Elle reprend "
        "l'intégralité des recommandations du texte source, mais ne remplace pas le "
        "texte intégral et n'est ni éditée ni validée par le CNOM, la SFAR ou les "
        "sociétés associées. De nombreux textes réglementaires cités (décrets de 1992 "
        "à 1998) ont pu être modifiés, abrogés ou recodifiés depuis 2001 (notamment par "
        "le code de la santé publique et le code de déontologie actuels) — se référer "
        "aux textes en vigueur et à un avis juridique/ordinal actualisé avant toute "
        "décision organisationnelle.", S_BODY_SM), bg=GREY_LIGHT, border=GREY))
    return story

def _section_sages_femmes_iade_sources():
    story = _section_sages_femmes()
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_iade())
    story.append(Spacer(1, 4 * mm))
    story.extend(_section_sources())
    return story

def _section_principes_mise_en_oeuvre():
    # Merged onto shared pages (no forced page break): "Methodologie, preambule
    # & principes deontologiques" alone left its 2nd page ~60% white, and "4 -
    # Mise en oeuvre" alone left its 2nd page ~75% white - combined per the
    # <60%-full merge rule (CLAUDE.md build pipeline, step 7).
    story = _section_organisation_structures_information()
    story.append(Spacer(1, 2.5 * mm))
    story.extend(_section_mise_en_oeuvre())
    return story

SECTIONS = [
    ("Méthodologie, préambule, principes déontologiques & mise en œuvre",
     _section_principes_mise_en_oeuvre),
    ("Sages-femmes, IADE & sources", _section_sages_femmes_iade_sources),
]

def _make_doc(path=None):
    return SimpleDocTemplate(path or OUT, pagesize=A4,
                              leftMargin=MARGIN, rightMargin=MARGIN,
                              topMargin=32 * mm, bottomMargin=16 * mm,
                              title="Fiche CNOM/SFAR 2001 - Relations "
                                    "anesthesistes-reanimateurs / chirurgiens",
                              author="Synthèse indépendante (source CNOM/SFAR)")

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
    # NOTE: pypdf/cryptography is broken in this container (pyo3 panic on
    # import) - use PyMuPDF (fitz) instead, per fiche_ponction_lombaire.py.
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
