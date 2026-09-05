# -*- coding: utf-8 -*-
"""
Fiche de synthese - RFE commune SFMU-SFAR 2017 (avec SFR, SSA, AFU, SOFCOT, SFCD)
Prise en charge des traumatises pelviens graves a la phase precoce (24 premieres heures)
Source verifiee : Anesth Reanim. 2019;5:427-442, texte valide CA SFMU et CA SFAR (29/06/2017)
Methodologie GRADE, tags "(GRADE X+/-) ACCORD FORT" imprimes litteralement apres chaque
recommandation. 22 recommandations numerotees R1.1-R1.5 (prehospitalier) et R2.1-R2.17
(hospitalier) - resume officiel "11 GRADE1 + 11 GRADE2 = 22" independamment reverifie item par
item et confirme coherent ; accord fort pour 100% des recommandations (contrairement a la fiche
intubation_difficile_adulte du meme corpus, pas d'exception ici). Particularite methodologique
disclosee explicitement par la source elle-meme : "Pour 9 questions posees, la methode Grade ne
pouvait pas s'appliquer... et les reponses ne pouvaient etre qu'un avis d'expert. Ces questions
n'ont pas ete retenues pour la redaction de ce document" - ces 9 questions n'apparaissent nulle
part dans le texte source lui-meme (contrairement aux autres fiches du projet ou un "pas de
recommandation" explicite est imprime question par question) : rien a reproduire ici au-dela de
cette disclosure, il n'y a pas de "pas de recommandation" a chercher dans le corps du texte.
Piege d'extraction : le signe moins de "GRADE 2-" a ete converti en "S" par l'extraction (R2.2,
R2.5, R2.11 lisaient "GRADE 2S" dans le .txt) - confirme "GRADE 2-" par rendu visuel de la page
source avant integration (meme categorie de piege que le "GRADE 2" sans signe de la fiche
voies_aeriennes_enfant, mais ici le signe a ete substitue plutot que supprime). Deux annexes de
classification (Young-Burgess, Tile) sont des planches anatomiques illustrees (schemas de bassin,
non du texte) - resumees ici en tableau texte (mecanisme/stabilite) plutot que redessinees.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from style import *
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.units import mm

OUT = "/private/tmp/claude-501/-Users-macbook-Downloads-claude/65498e3e-5ddf-47a6-b100-3ac535d1faa0/scratchpad/rfe_sfar/output/Fiche_SFAR_Traumatisme_Pelvien_2017.pdf"

SOURCE_TXT = ("Source : Recommandations Formalisées d'Experts communes SFMU-SFAR, en collaboration "
              "avec la SFR, le SSA, l'AFU, la SOFCOT et la SFCD « Prise en charge des traumatisés "
              "pelviens graves à la phase précoce (24 premières heures) » — Anesth Reanim. "
              "2019;5:427-442, texte validé par le CA SFMU et le CA SFAR le 29/06/2017. "
              "Méthodologie GRADE. Fiche de synthèse non officielle : se référer au texte intégral.")

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
             ("2+", "Il faut probablement"), ("2-", "Il ne faut probablement pas")]
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
    header_band(canvas, doc, "SFMU / SFAR — RFE 2017 — FICHE DE SYNTHÈSE",
                "Traumatisme pelvien grave",
                page_title, icon_fn=lambda c,x,y: icon_shield(c, x, y, 13*mm), color=NAVY)
    footer_band(canvas, doc, SOURCE_TXT, f"Page {doc.page} / {TOTAL_PAGES['n']}")

# ---------------------------------------------------------------------------
def _section_intro():
    story = []
    story.append(Spacer(1, 3*mm))
    story.append(info_panel(P(
        "<b>Champ :</b> prise en charge extra- et intrahospitalière du traumatisé pelvien grave "
        "durant les 24 premières heures. Comité de 22 experts SFMU/SFAR, avec la SFR, le SSA, "
        "l'AFU, la SOFCOT et la SFCD ; méthode GRADE®, format PICO. Le traitement du choc "
        "hémorragique (objet d'une RFE dédiée) est explicitement exclu du champ.<br/><br/>"
        "<b>Résultats (résumé officiel) :</b> 22 recommandations (5 préhospitalières, 17 "
        "hospitalières) ; 11 de niveau de preuve élevé (Grade 1), 11 de niveau de preuve faible "
        "(Grade 2). Accord fort obtenu pour 100 % des recommandations après trois tours de "
        "cotation.<br/><br/>"
        "<i>Pour 9 questions posées, la méthode GRADE ne pouvait pas s'appliquer par manque de "
        "littérature et n'aurait pu produire qu'un avis d'experts — ces 9 questions n'ont "
        "délibérément pas été retenues pour la rédaction du document source lui-même (disclosure "
        "de la source), qui ne contient donc aucun « pas de recommandation » explicite : cette "
        "fiche reproduit les 22 recommandations réellement publiées, intégralement.</i><br/><br/>"
        "<b>Épidémiologie :</b> les fractures du bassin représentent 5 % de l'ensemble des "
        "fractures, présentes chez 10-20 % des traumatisés graves ; mortalité globale 8-15 %, liée "
        "aux lésions hémorragiques pelviennes et aux lésions extra-pelviennes associées.",
        S_BODY), bg=BG_PANEL, border=TEAL))
    story.append(Spacer(1, 3*mm))

    story.append(section_bar("Légende des grades (méthodologie GRADE)"))
    story.append(Spacer(1, 2*mm))
    story.append(legend_flowable())
    return story

def _section_prehospitalier():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Prise en charge préhospitalière"))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("R1.1", "Il est recommandé de considérer la douleur spontanée du pelvis chez un patient "
         "conscient comme un signe évocateur de fracture du bassin. Lorsque le patient est "
         "inconscient ou choqué, il doit être considéré systématiquement comme suspect d'un "
         "traumatisme pelvien.", "1+"),
        ("R1.2", "Il est probablement recommandé de considérer comme critères cliniques de gravité "
         "d'un traumatisme pelvien : un traumatisme pelvien ouvert, l'association avec une autre "
         "lésion traumatique grave, ou des signes cliniques de gravité d'hémorragie.", "2+"),
        ("R1.3", "Il est recommandé de mettre en place le plus tôt possible une contention externe "
         "du bassin chez tout patient suspect d'un traumatisme pelvien grave.", "1+"),
        ("R1.4", "Il est probablement recommandé d'utiliser comme contention externe du bassin une "
         "ceinture pelvienne, sans qu'un type particulier ne soit recommandé (à l'exclusion de "
         "draps noués). Pour avoir une efficacité comparable au C-clamp chirurgical elle doit être "
         "positionnée à hauteur des grands trochanters.", "2+"),
        ("R1.5", "Il est recommandé de transférer par transport médicalisé tous les patients "
         "présentant un traumatisme pelvien grave vers un centre de référence disposant d'un "
         "plateau technique spécialisé en première intention.", "1+"),
    ], [14*mm, PAGE_W-2*MARGIN-14*mm-20*mm, 20*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(P("Méta-analyse (5235 patients, 12 études) : examen clinique par équipe entraînée "
                    "chez un patient conscient non choqué détecte une fracture du bassin avec une "
                    "sensibilité proche de 100 % (seules 3/441 fractures manquées). Mortalité "
                    "majorée si association à un traumatisme crânien grave (OR 4,57 [1,95-10,73]), "
                    "thoracique (OR 2,8 [1,3-6,1]) ou abdominal sévère (OR 5,54 [1,61-18,37]) ; choc "
                    "hémorragique associé : mortalité ×3 à ×5. Traumatisme ouvert : mortalité ×3-4. "
                    "Ceinture pelvienne (positionnée aux grands trochanters) : réduit les besoins "
                    "transfusionnels et les durées de séjour (non retrouvé avec des draps noués) — "
                    "peut aggraver certains types de fracture (B2-B3) et causer des lésions cutanées "
                    "(hommes maigres/âgés). Médicalisation préhospitalière : réduction de mortalité "
                    "de 30 % ; hélicoptère médicalisé : +15 % de survie ; admission en Trauma "
                    "Centre : -20 à -30 % de mortalité.", S_NOTE))
    return story

def _section_imagerie1():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Prise en charge hospitalière — Imagerie initiale (1/2)"))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("R2.1", "Il est probablement recommandé de réaliser une radiographie de bassin de face dès "
         "l'admission si le patient est instable sur le plan hémodynamique ou nécessite des "
         "thérapeutiques urgentes pour contrôler les fonctions vitales.", "2+"),
        ("R2.2", "Il n'est probablement pas recommandé de réaliser une radiographie de bassin de "
         "face en dehors d'une instabilité hémodynamique à l'arrivée en salle d'accueil des "
         "détresses vitales, la réalisation rapide d'une tomodensitométrie thoraco-abdomino-"
         "pelvienne avec injection de produit de contraste pour bilan vasculaire et osseux complet "
         "du pelvis étant alors préférée.", "2-"),
        ("R2.3", "Il est probablement recommandé de réaliser une eFAST échographie chez tous les "
         "patients présentant un traumatisme sévère lors de la prise en charge d'un patient "
         "suspect d'un traumatisme grave du bassin.", "2+"),
    ], [14*mm, PAGE_W-2*MARGIN-14*mm-20*mm, 20*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(P("Chez le patient instable, une décision d'intervention urgente basée sur la "
                    "seule imagerie initiale (radio bassin/thorax, eFAST) était jugée appropriée "
                    "dans 98 % des cas (étude de Peytel et al.). eFAST : diagnostic des fractures "
                    "« open book » par mesure de la symphyse pubienne (anneau ouvert si &gt; 25 mm) "
                    "et des lésions associées ; VPP 97 %, VPN 97 % chez le patient choqué "
                    "(performance réduite en cas d'hémo-rétropéritoine ou de rupture vésicale "
                    "intrapéritonéale). Hémopéritoine associé : foyer le plus souvent abdominal "
                    "(70 % des cas) si fracture pelvienne stable, le plus souvent pelvien (56 % des "
                    "cas) si fracture instable — certitude diagnostique non acquise, l'abondance de "
                    "l'hémopéritoine (nombre de sites positifs) oriente vers la laparotomie.", S_NOTE))
    return story

def _section_imagerie2():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Prise en charge hospitalière — Imagerie initiale (2/2)"))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("R2.4", "Il est recommandé de réaliser une tomodensitométrie thoraco-abdomino-pelvienne "
         "avec injection de produit de contraste avant la réalisation d'une artériographie à visée "
         "thérapeutique chez un patient victime d'un traumatisme pelvien grave si son état "
         "hémodynamique le permet.", "1+"),
        ("R2.5", "Il n'est probablement pas recommandé de réaliser à titre systématique une "
         "imagerie dédiée pour le bas appareil urinaire (opacification de l'urètre et de la "
         "vessie) chez un patient traumatisé pelvien grave.", "2-"),
        ("R2.6", "Il est probablement recommandé de réaliser une opacification rétrograde de "
         "l'urètre et de la vessie, couplée idéalement à une TDM pelvienne chez un patient "
         "traumatisé pelvien grave présentant des symptômes évocateurs de traumatisme de la vessie "
         "(impossibilité d'uriner, hématurie, empâtement sus-pubien douloureux, vessie sur le "
         "trajet d'une plaie pénétrante), en particulier avant tout sondage chez l'homme.", "2+"),
    ], [14*mm, PAGE_W-2*MARGIN-14*mm-20*mm, 20*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(P("TDM injectée vs artériographie (51 patients) : sensibilité 93,9 %, spécificité "
                    "77,8 %, VPP 88,6 %, VPN 87,5 %. Lésions vésicales : 60-90 % liées à une "
                    "fracture du bassin (3,5 % des fractures) ; lésions de l'urètre postérieur "
                    "(surtout chez l'homme) : 4-19 % des fractures, associées surtout aux fractures "
                    "instables (atteinte bilatérale des branches ischiopubiennes + disjonction "
                    "sacro-iliaque) ; lésions associées urètre+vessie : 4-15 % des cas. Ces lésions "
                    "n'engagent jamais le pronostic vital à la phase aiguë (pas de réparation "
                    "urgente impérative) mais leur diagnostic conditionne un drainage adapté. "
                    "Urétrocystographie rétrograde = examen de référence chez l'homme (ballonnet "
                    "gonflé à 1-2 mL seulement, remplissage vésical possible jusqu'à 350 mL), "
                    "surtout si le scanner n'est pas accessible ou le patient instable. "
                    "L'exploration endoscopique rétrograde est une option intéressante (avec "
                    "possibilité de réalignement sur guide en cas de solution de continuité "
                    "urétrale) ; elle est recommandée chez la femme en cas de suspicion, car "
                    "l'urètre féminin, plus court, rend toute opacification rétrograde classique "
                    "peu fiable.", S_NOTE))
    return story

def _section_gravite():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Critères de gravité anatomoradiologiques"))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("R2.7", "Il est probablement recommandé de considérer comme critères anatomoradiologiques "
         "de traumatisme pelvien grave : une fracture du pelvis instable selon les classifications "
         "de Young-Burgess et de Tile, en particulier les fractures dites « open book » et les "
         "ruptures de l'anneau pelvien avec atteinte postérieure ; l'existence d'une extravasation "
         "de produit de contraste au temps artériel observée sur une angioscanographie ou une "
         "tomodensitométrie.", "2+"),
    ], [14*mm, PAGE_W-2*MARGIN-14*mm-20*mm, 20*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(P("Les fractures instables de Tile (type C) et les ruptures de l'anneau à atteinte "
                    "postérieure sont significativement plus associées aux lésions vasculaires "
                    "hémorragiques et nécessitent davantage de transfusions. Les fractures instables "
                    "de Young-Burgess (APC2/3, LC2/3, VS et combinées) ont une mortalité "
                    "significativement plus élevée que les fractures stables (11,5 % vs 7,5 %, "
                    "p &lt; 0,05). L'extravasation de produit de contraste prédit un saignement "
                    "artériel avec une sensibilité de 82-89 % et une spécificité de 75-100 %.", S_NOTE))
    story.append(Spacer(1, 3*mm))
    cw = PAGE_W - 2*MARGIN
    story.append(simple_table(
        ["Classification", "Mécanisme / stabilité", "Types"],
        [
            ["Young-Burgess (Annexe 1)", "Classification par mécanisme lésionnel (planches "
             "anatomiques illustrées, non reproduites ici — voir texte intégral)",
             "Compression antéro-postérieure (I/II/III) • Compression latérale (I/II/III) • "
             "Cisaillement vertical"],
            ["Tile (Annexe 2)", "Classification par stabilité de l'anneau pelvien (planches "
             "anatomiques illustrées, non reproduites ici — voir texte intégral)",
             "Tile A : stable • Tile B : instable dans le plan horizontal • Tile C : instable dans "
             "le plan horizontal ET vertical"],
        ],
        [cw*0.22, cw*0.40, cw*0.38]))
    return story

def _section_hemostase():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Délai et modalités d'hémostase"))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("R2.8", "Il est recommandé de réaliser un geste d'hémostase le plus rapidement possible en "
         "cas d'hémorragie active en lien avec un traumatisme pelvien grave. Le geste d'hémostase "
         "peut être une artériographie avec embolisation ou un tamponnement chirurgical pelvien "
         "pré-péritonéal de sauvetage réalisé par une équipe entraînée.", "1+"),
        ("R2.9", "Il est recommandé que le délai entre l'admission hospitalière et le geste "
         "d'hémostase ne dépasse pas 60 minutes, quelle que soit la technique utilisée.", "1+"),
    ], [14*mm, PAGE_W-2*MARGIN-14*mm-20*mm, 20*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(P("Essai randomisé récent : pas de différence de survie entre tamponnement "
                    "pré-péritonéal et embolisation. Le délai jusqu'à l'embolisation est un facteur "
                    "de risque indépendant de mortalité : mortalité de 16 % à 64 % si le délai "
                    "dépasse 60 minutes ; chaque tranche de 3 minutes perdues augmente la mortalité "
                    "d'environ 1 %.", S_NOTE))
    story.append(Spacer(1, 4*mm))

    story.append(section_bar("Embolisation"))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("R2.10", "Les experts recommandent de réaliser une embolisation non sélective par un abord "
         "fémoral commun chez les patients instables, chez les patients stables présentant de "
         "nombreuses cibles identifiées en TDM ou à l'angiographie et en cas d'échec de "
         "l'embolisation sélective.", "1+"),
        ("R2.11", "Il n'est probablement pas recommandé de réaliser un contrôle artériographique "
         "systématique chez tous les patients ayant bénéficié d'une artério-embolisation à la "
         "phase initiale de prise en charge d'un traumatisme pelvien grave.", "2-"),
    ], [14*mm, PAGE_W-2*MARGIN-14*mm-20*mm, 20*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(P("Embolisation non sélective bilatérale (occlusion des troncs iliaques internes) "
                    "si patient instable et cibles multiples bilatérales ; unilatérale si cibles "
                    "unilatérales ou échec sélectif. Embolisation sélective réservée aux patients "
                    "stables avec cible(s) limitée(s). Contention laissée en place pendant "
                    "l'embolisation ; introducteur à valve anti-retour laissable 24h pour une "
                    "nouvelle embolisation en cas de récidive. Contrôle artériographique "
                    "systématique non recommandé — un contrôle n'est indiqué qu'en cas de doute sur "
                    "une récidive hémorragique, de préférence après TDM.", S_NOTE))
    return story

def _section_tamponnement_fixation():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Tamponnement pelvien et fixation externe"))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("R2.12", "Il est probablement recommandé d'avoir recours à un tamponnement pelvien "
         "pré-péritonéal chirurgical en association avec une fixation externe du bassin en cas "
         "d'instabilité hémodynamique majeure rendant impossible le transfert du patient au "
         "scanner et/ou en embolisation, ou la réalisation d'une artériographie-embolisation dans "
         "un délai de 60 minutes à partir du diagnostic.", "2+"),
        ("R2.13", "Il est recommandé de réaliser une fixation externe précoce du bassin chez les "
         "patients présentant un traumatisme pelvien grave avec instabilité hémodynamique pour "
         "limiter l'expansion de l'hématome pelvien. La fixation externe peut être réalisée par un "
         "Clamp de Ganz ou un fixateur externe antérieur.", "1+"),
        ("R2.14", "Il est recommandé d'utiliser un clamp de Ganz pour les fractures Tile C "
         "essentiellement, après traction lourde du membre ascensionné (15 % du poids corporel). "
         "Il peut être placé en salle d'urgence par des opérateurs entraînés.", "1+"),
        ("R2.15", "Il est recommandé d'utiliser un fixateur externe pour stabiliser les bassins "
         "dans les fractures Tile C et pour les refermer dans les fractures Tile B1 et B3. Il doit "
         "être placé en antéro-inférieur de façon à permettre la réalisation d'une laparotomie.", "1+"),
    ], [14*mm, PAGE_W-2*MARGIN-14*mm-20*mm, 20*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(P("Le tamponnement pré-péritonéal vise une hémostase temporaire jusqu'à "
                    "l'hémostase définitive — technique rapide mais nécessitant formation "
                    "chirurgicale et discussion multidisciplinaire ; ne se substitue pas à "
                    "l'embolisation. La fermeture de l'anneau pelvien limite l'expansion de "
                    "l'hématome quelle que soit la méthode. Clamp de Ganz : referme les structures "
                    "postérieures, permet la réalisation secondaire d'une embolisation, "
                    "laparotomie ou packing pelvien. Fixateur externe : montage en cadre "
                    "trapézoïdal (crêtes iliaques antérieures ou toit du cotyle), doit permettre "
                    "l'accès vasculaire pour embolisation secondaire, packing rétropéritonéal et "
                    "laparotomie. Fixation définitive réalisée à distance, sur patient stabilisé.", S_NOTE))
    return story

def _section_ouvert():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Traumatisme pelvien grave ouvert"))
    story.append(Spacer(1, 2*mm))
    story.append(reco_table([
        ("R2.16", "Il est probablement recommandé d'assurer la prise en charge des traumatismes "
         "pelviens graves ouverts dans les centres de référence car les lésions pelviennes "
         "ouvertes sont rares, leur prise en charge est complexe et fait appel à des équipes "
         "multidisciplinaires.", "2+"),
        ("R2.17", "Il est recommandé de considérer comme objectifs initiaux de la prise en charge "
         "des traumatismes pelviens graves ouverts le contrôle de l'hémorragie et de la "
         "contamination périnéale.", "1+"),
    ], [14*mm, PAGE_W-2*MARGIN-14*mm-20*mm, 20*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(info_panel(P(
        "<b>Rares mais graves :</b> 52/3053 fractures du bassin sont ouvertes (1,7 %), pour une "
        "mortalité pouvant dépasser 50 %. <b>4 priorités :</b> contrôle de l'hémorragie • lavage et "
        "parage des tissus mous • identification et traitement des lésions associées (pelviennes "
        "ou extra-pelviennes) • traitement de la fracture du bassin. Gestes complexes fréquents : "
        "colostomie de décharge, fixateur externe, exceptionnellement hémi-pelvectomie. "
        "Rectosigmoïdoscopie pour écarter une lésion digestive associée. Reprises chirurgicales "
        "multiples souvent nécessaires (lavage/parage/excision des tissus dévitalisés) pour "
        "prévenir l'infection.",
        S_BODY), bg=RED_LIGHT, border=RED))
    return story

def _section_synthese():
    story = []
    story.append(Spacer(1, 2*mm))
    story.append(section_bar("Synthèse et messages clés"))
    story.append(Spacer(1, 2*mm))
    story.append(P(
        "• Douleur pelvienne spontanée (patient conscient) ou tout patient inconscient/choqué = "
        "suspect de traumatisme pelvien ; contention externe (ceinture pelvienne aux grands "
        "trochanters) le plus tôt possible ; transfert médicalisé direct vers un centre de "
        "référence.<br/>"
        "• Radiographie de bassin réservée à l'instabilité hémodynamique ; sinon TDM "
        "thoraco-abdomino-pelvienne injectée d'emblée ; eFAST systématique.<br/>"
        "• TDM injectée avant artériographie si l'état hémodynamique le permet ; pas d'imagerie "
        "urinaire systématique, réservée aux signes d'appel (urétrocystographie rétrograde, "
        "prudence avant tout sondage chez l'homme).<br/>"
        "• Classifications Young-Burgess et Tile pour définir la gravité anatomoradiologique ; "
        "extravasation de contraste au temps artériel = signe de gravité.<br/>"
        "• Hémostase (embolisation ou tamponnement pré-péritonéal) le plus vite possible, délai "
        "cible &lt; 60 minutes depuis l'admission.<br/>"
        "• Fixation externe précoce (Clamp de Ganz si Tile C, fixateur externe) pour limiter "
        "l'expansion de l'hématome pelvien ; tamponnement pré-péritonéal si transfert au "
        "scanner/embolisation impossible dans les délais.<br/>"
        "• Traumatisme ouvert : rare mais mortalité &gt; 50 % — prise en charge en centre de "
        "référence, contrôle hémorragie + contamination périnéale en priorité.",
        S_BODY))
    story.append(Spacer(1, 5*mm))

    story.append(section_bar("Sources et traçabilité", color=GREY))
    story.append(Spacer(1, 2*mm))
    story.append(P(
        "<b>Document source :</b> « Prise en charge des traumatisés pelviens graves à la phase "
        "précoce (24 premières heures) » — Recommandations Formalisées d'Experts communes "
        "SFMU-SFAR, en collaboration avec la SFR, le SSA, l'AFU, la SOFCOT et la SFCD. Anesth "
        "Reanim. 2019;5:427-442. Comité de 22 experts, coordination P. Incagnoli (SFAR), "
        "A. Puidupin (SFMU). Texte validé par le CA SFMU et le CA SFAR le 29/06/2017.", S_SOURCE))
    story.append(Spacer(1, 1.5*mm))
    story.append(P("<b>Méthodologie :</b> GRADE®, tags « (GRADE X+/-) ACCORD FORT » imprimés "
                    "littéralement après chaque recommandation — cités ici tels quels.", S_SOURCE))
    story.append(Spacer(1, 1.5*mm))
    story.append(P("<b>Couverture :</b> 22 recommandations (R1.1-R1.5, R2.1-R2.17) reproduites "
                    "intégralement. Les 2 annexes de classification (Young-Burgess, Tile) sont des "
                    "planches anatomiques illustrées dans la source (schémas de bassin) : leur "
                    "contenu clinique — mécanisme lésionnel et catégories de stabilité — est "
                    "résumé en tableau texte ; pour les planches elles-mêmes, se référer au texte "
                    "intégral. La source elle-même exclut 9 questions n'ayant abouti qu'à un avis "
                    "d'experts (littérature insuffisante pour la méthode GRADE) : ces questions ne "
                    "figurent pas dans le texte publié et ne sont donc pas reproductibles ici.", S_SOURCE))
    story.append(Spacer(1, 3*mm))
    story.append(info_panel(P(
        "<b>Avertissement :</b> ce document est une fiche de synthèse indépendante, produite pour un "
        "usage d'aide-mémoire. Il reprend l'intégralité des recommandations de la RFE mais ne "
        "remplace pas le texte intégral et n'est ni édité ni validé par la SFMU/SFAR. Le traitement "
        "du choc hémorragique est exclu du champ (RFE dédiée). En cas de doute, se référer au texte "
        "intégral, aux recommandations ultérieures et/ou à un avis spécialisé.",
        S_BODY_SM), bg=GREY_LIGHT, border=GREY))
    return story

SECTIONS = [
    ("Introduction, méthodologie", _section_intro),
    ("Prise en charge préhospitalière", _section_prehospitalier),
    ("Imagerie initiale (1/2)", _section_imagerie1),
    ("Imagerie initiale (2/2)", _section_imagerie2),
    ("Critères de gravité & classifications", _section_gravite),
    ("Hémostase & embolisation", _section_hemostase),
    ("Tamponnement pelvien & fixation externe", _section_tamponnement_fixation),
    ("Traumatisme pelvien ouvert", _section_ouvert),
    ("Synthèse, sources & traçabilité", _section_synthese),
]

def _make_doc():
    return SimpleDocTemplate(OUT, pagesize=A4,
                              leftMargin=MARGIN, rightMargin=MARGIN,
                              topMargin=32*mm, bottomMargin=16*mm,
                              title="Fiche SFMU-SFAR 2017 - Traumatisme pelvien grave",
                              author="Synthèse indépendante (source SFMU/SFAR)")

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
