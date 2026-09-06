# -*- coding: utf-8 -*-
"""
Extract the verified fiche content directly from the already-audited Python
build scripts (not by re-typing it) into JSON, so the website reuses the
exact same recommendation text / grades / table rows as the checked PDFs.

Works by monkeypatching Paragraph/Table/grade_chip/section_bar/info_panel in
each module's namespace with lightweight recorder stand-ins, then calling the
module's real content-building functions (build_story()/build_annex()) and
serializing what was recorded, in document order.
"""
import sys, os, json, html as htmlmod
from reportlab.platypus import KeepTogether

BUILD_DIR = os.path.dirname(__file__)
sys.path.insert(0, BUILD_DIR)

# ---------- lightweight recorder objects ----------

class ParaRec:
    __slots__ = ("text", "style")
    def __init__(self, text, style=None):
        self.text = text
        self.style = style

class ChipRec:
    __slots__ = ("label",)
    def __init__(self, label):
        self.label = label

class TableRec:
    __slots__ = ("grid",)
    def __init__(self, grid):
        self.grid = grid
    def setStyle(self, *a, **kw):
        pass

class PanelRec:
    __slots__ = ("content", "kind", "tone")
    def __init__(self, content, kind="panel", tone="default"):
        self.content = content
        self.kind = kind
        self.tone = tone

class SectionRec:
    __slots__ = ("text", "color")
    def __init__(self, text, color=None):
        self.text = text
        self.color = color

class NoOp:
    def setStyle(self, *a, **kw):
        pass


def resolve(obj):
    """Recursively turn recorder objects into JSON-safe structures."""
    if obj is None:
        return None
    if isinstance(obj, str):
        return obj
    if isinstance(obj, ParaRec):
        return {"t": "p", "html": obj.text, "style": obj.style}
    if isinstance(obj, ChipRec):
        return {"t": "chip", "label": obj.label}
    if isinstance(obj, TableRec):
        return {"t": "table", "rows": [[resolve(c) for c in row] for row in obj.grid]}
    if isinstance(obj, PanelRec):
        return {"t": obj.kind, "tone": obj.tone, "content": resolve(obj.content)}
    if isinstance(obj, SectionRec):
        return {"t": "section", "text": obj.text, "color": obj.color}
    if isinstance(obj, (list, tuple)):
        return [resolve(x) for x in obj]
    if isinstance(obj, KeepTogether):
        # KeepTogether is a real (unpatched) reportlab flowable used purely as a print-layout
        # hint to avoid orphan lines when merging short sections onto shared pages (see
        # fiche_controle_temperature.py) - transparent for content extraction: flatten its
        # wrapped flowables in place rather than dropping them (previously fell through to the
        # "unknown flowable" case below and silently lost every item inside it).
        return [resolve(x) for x in obj._content]
    # fallback: unknown flowable (Spacer, etc.) -> ignore
    return None


def make_module_patches(mod, trace):
    """Patch Paragraph/Table/grade_chip/section_bar/info_panel in `mod`'s namespace."""
    def PatchedParagraph(text, style=None, *a, **kw):
        return ParaRec(text, getattr(style, "name", None))

    def PatchedTable(data, *a, **kw):
        return TableRec(data)

    def PatchedSpacer(*a, **kw):
        return None

    def PatchedPageBreak(*a, **kw):
        rec = {"t": "pagebreak"}
        trace.append(rec)
        return rec

    real_grade_chip = getattr(mod, "grade_chip", None)
    def PatchedGradeChip(label, **kw):
        return ChipRec(label)

    def PatchedSectionBar(text, color=None, icon_fn=None):
        return SectionRec(text, _color_name(color))

    def PatchedInfoPanel(flowable, bg=None, border=None, pad=6):
        tone_name = _color_name(border)
        tone = {"red": "crit", "grey": "grey", "green": "good"}.get(tone_name, "default")
        return PanelRec(flowable, kind="panel", tone=tone)

    mod.Paragraph = PatchedParagraph
    mod.Table = PatchedTable
    mod.Spacer = PatchedSpacer
    mod.PageBreak = PatchedPageBreak
    if hasattr(mod, "grade_chip"):
        mod.grade_chip = PatchedGradeChip
    if hasattr(mod, "section_bar"):
        mod.section_bar = PatchedSectionBar
    if hasattr(mod, "info_panel"):
        mod.info_panel = PatchedInfoPanel


_COLOR_NAMES = {}

def _color_name(color_obj):
    # style.py colors are reportlab HexColor instances; map by identity to a friendly name
    try:
        from style import NAVY, TEAL, TEAL_DARK, RED, GREEN, AMBER, GREY
        mapping = {id(NAVY): "navy", id(TEAL): "teal", id(TEAL_DARK): "teal-dark",
                   id(RED): "red", id(GREEN): "green", id(AMBER): "amber", id(GREY): "grey"}
        return mapping.get(id(color_obj), "navy")
    except Exception:
        return "navy"


def extract_anticoagulants():
    trace = []
    import style
    import fiche_anticoagulants as m
    make_module_patches(m, trace)
    make_module_patches(style, trace)  # in case some helpers reference style.* directly

    blocks = []
    # capture each top-level story.append(...) call by patching list.append via wrapping build funcs
    # Simpler: call each _section_N and build_annex, and just take their return values (already lists)
    for title, fn in m.SECTIONS:
        items = fn()
        items = [resolve(x) for x in items]
        items = [x for x in items if x is not None]
        blocks.append({"title": title, "items": items})

    import annexe_specialites as ax
    make_module_patches(ax, trace)
    annex_items = ax.build_annex()
    annex_items = [resolve(x) for x in annex_items]
    annex_items = [x for x in annex_items if x is not None]
    blocks.append({"title": "Annexe — Classification du risque hémorragique par spécialité", "items": annex_items})

    tail_items = [resolve(x) for x in m._section_tail()]
    tail_items = [x for x in tail_items if x is not None]
    blocks.append({"title": "Situations particulières & sources", "items": tail_items})

    return {"doc": "anticoagulants", "sections": blocks}


def extract_ecbu():
    import style
    import fiche_ecbu as m
    trace = []
    make_module_patches(m, trace)
    make_module_patches(style, trace)

    blocks = []
    for title, fn in m.SECTIONS:
        items = fn()
        items = [resolve(x) for x in items]
        items = [x for x in items if x is not None]
        blocks.append({"title": title, "items": items})
    return {"doc": "ecbu", "sections": blocks}


def extract_choc_hemorragique():
    import style
    import fiche_choc_hemorragique as m
    trace = []
    make_module_patches(m, trace)
    make_module_patches(style, trace)

    blocks = []
    for title, fn in m.SECTIONS:
        items = fn()
        items = [resolve(x) for x in items]
        items = [x for x in items if x is not None]
        blocks.append({"title": title, "items": items})
    return {"doc": "choc_hemorragique", "sections": blocks}


def extract_intubation_urgence():
    import style
    import fiche_intubation_urgence as m
    trace = []
    make_module_patches(m, trace)
    make_module_patches(style, trace)

    blocks = []
    for title, fn in m.SECTIONS:
        items = fn()
        items = [resolve(x) for x in items]
        items = [x for x in items if x is not None]
        blocks.append({"title": title, "items": items})
    return {"doc": "intubation_urgence", "sections": blocks}


def extract_sepsis():
    import style
    import fiche_sepsis as m
    trace = []
    make_module_patches(m, trace)
    make_module_patches(style, trace)

    blocks = []
    for title, fn in m.SECTIONS:
        items = fn()
        items = [resolve(x) for x in items]
        items = [x for x in items if x is not None]
        blocks.append({"title": title, "items": items})
    return {"doc": "sepsis", "sections": blocks}


def extract_urgences_obstetricales():
    import style
    import fiche_urgences_obstetricales as m
    trace = []
    make_module_patches(m, trace)
    make_module_patches(style, trace)

    blocks = []
    for title, fn in m.SECTIONS:
        items = fn()
        items = [resolve(x) for x in items]
        items = [x for x in items if x is not None]
        blocks.append({"title": title, "items": items})
    return {"doc": "urgences_obstetricales", "sections": blocks}


def extract_anaphylaxie():
    import style
    import fiche_anaphylaxie as m
    trace = []
    make_module_patches(m, trace)
    make_module_patches(style, trace)

    blocks = []
    for title, fn in m.SECTIONS:
        items = fn()
        items = [resolve(x) for x in items]
        items = [x for x in items if x is not None]
        blocks.append({"title": title, "items": items})
    return {"doc": "anaphylaxie", "sections": blocks}


def extract_preeclampsie():
    import style
    import fiche_preeclampsie as m
    trace = []
    make_module_patches(m, trace)
    make_module_patches(style, trace)

    blocks = []
    for title, fn in m.SECTIONS:
        items = fn()
        items = [resolve(x) for x in items]
        items = [x for x in items if x is not None]
        blocks.append({"title": title, "items": items})
    return {"doc": "preeclampsie", "sections": blocks}


def extract_hyperthermie_maligne():
    import style
    import fiche_hyperthermie_maligne as m
    trace = []
    make_module_patches(m, trace)
    make_module_patches(style, trace)

    blocks = []
    for title, fn in m.SECTIONS:
        items = fn()
        items = [resolve(x) for x in items]
        items = [x for x in items if x is not None]
        blocks.append({"title": title, "items": items})
    return {"doc": "hyperthermie_maligne", "sections": blocks}


def extract_anticoag_urgence():
    import style
    import fiche_anticoag_urgence as m
    trace = []
    make_module_patches(m, trace)
    make_module_patches(style, trace)

    blocks = []
    for title, fn in m.SECTIONS:
        items = fn()
        items = [resolve(x) for x in items]
        items = [x for x in items if x is not None]
        blocks.append({"title": title, "items": items})
    return {"doc": "anticoag_urgence", "sections": blocks}


def extract_traumatisme_abdominal():
    import style
    import fiche_traumatisme_abdominal as m
    trace = []
    make_module_patches(m, trace)
    make_module_patches(style, trace)

    blocks = []
    for title, fn in m.SECTIONS:
        items = fn()
        items = [resolve(x) for x in items]
        items = [x for x in items if x is not None]
        blocks.append({"title": title, "items": items})
    return {"doc": "traumatisme_abdominal", "sections": blocks}


def extract_sedation_reanimation():
    import style
    import fiche_sedation_reanimation as m
    trace = []
    make_module_patches(m, trace)
    make_module_patches(style, trace)

    blocks = []
    for title, fn in m.SECTIONS:
        items = fn()
        items = [resolve(x) for x in items]
        items = [x for x in items if x is not None]
        blocks.append({"title": title, "items": items})
    return {"doc": "sedation_reanimation", "sections": blocks}


def extract_sedation_urgences():
    import style
    import fiche_sedation_urgences as m
    trace = []
    make_module_patches(m, trace)
    make_module_patches(style, trace)

    blocks = []
    for title, fn in m.SECTIONS:
        items = fn()
        items = [resolve(x) for x in items]
        items = [x for x in items if x is not None]
        blocks.append({"title": title, "items": items})
    return {"doc": "sedation_urgences", "sections": blocks}


def extract_vni():
    import style
    import fiche_vni as m
    trace = []
    make_module_patches(m, trace)
    make_module_patches(style, trace)

    blocks = []
    for title, fn in m.SECTIONS:
        items = fn()
        items = [resolve(x) for x in items]
        items = [x for x in items if x is not None]
        blocks.append({"title": title, "items": items})
    return {"doc": "vni", "sections": blocks}


def extract_aap_urgence():
    import style
    import fiche_aap_urgence as m
    trace = []
    make_module_patches(m, trace)
    make_module_patches(style, trace)

    blocks = []
    for title, fn in m.SECTIONS:
        items = fn()
        items = [resolve(x) for x in items]
        items = [x for x in items if x is not None]
        blocks.append({"title": title, "items": items})
    return {"doc": "aap_urgence", "sections": blocks}


def extract_curares():
    import style
    import fiche_curares as m
    trace = []
    make_module_patches(m, trace)
    make_module_patches(style, trace)

    blocks = []
    for title, fn in m.SECTIONS:
        items = fn()
        items = [resolve(x) for x in items]
        items = [x for x in items if x is not None]
        blocks.append({"title": title, "items": items})
    return {"doc": "curares", "sections": blocks}


def extract_remplissage():
    import style
    import fiche_remplissage as m
    trace = []
    make_module_patches(m, trace)
    make_module_patches(style, trace)

    blocks = []
    for title, fn in m.SECTIONS:
        items = fn()
        items = [resolve(x) for x in items]
        items = [x for x in items if x is not None]
        blocks.append({"title": title, "items": items})
    return {"doc": "remplissage", "sections": blocks}


def extract_traumatisme_membre():
    import style
    import fiche_traumatisme_membre as m
    trace = []
    make_module_patches(m, trace)
    make_module_patches(style, trace)

    blocks = []
    for title, fn in m.SECTIONS:
        items = fn()
        items = [resolve(x) for x in items]
        items = [x for x in items if x is not None]
        blocks.append({"title": title, "items": items})
    return {"doc": "traumatisme_membre", "sections": blocks}


def extract_voies_aeriennes_enfant():
    import style
    import fiche_voies_aeriennes_enfant as m
    trace = []
    make_module_patches(m, trace)
    make_module_patches(style, trace)

    blocks = []
    for title, fn in m.SECTIONS:
        items = fn()
        items = [resolve(x) for x in items]
        items = [x for x in items if x is not None]
        blocks.append({"title": title, "items": items})
    return {"doc": "voies_aeriennes_enfant", "sections": blocks}


def extract_intubation_difficile_adulte():
    import style
    import fiche_intubation_difficile_adulte as m
    trace = []
    make_module_patches(m, trace)
    make_module_patches(style, trace)

    blocks = []
    for title, fn in m.SECTIONS:
        items = fn()
        items = [resolve(x) for x in items]
        items = [x for x in items if x is not None]
        blocks.append({"title": title, "items": items})
    return {"doc": "intubation_difficile_adulte", "sections": blocks}


def extract_traumatisme_pelvien():
    import style
    import fiche_traumatisme_pelvien as m
    trace = []
    make_module_patches(m, trace)
    make_module_patches(style, trace)

    blocks = []
    for title, fn in m.SECTIONS:
        items = fn()
        items = [resolve(x) for x in items]
        items = [x for x in items if x is not None]
        blocks.append({"title": title, "items": items})
    return {"doc": "traumatisme_pelvien", "sections": blocks}


def extract_traumatisme_thoracique():
    import style
    import fiche_traumatisme_thoracique as m
    trace = []
    make_module_patches(m, trace)
    make_module_patches(style, trace)

    blocks = []
    for title, fn in m.SECTIONS:
        items = fn()
        items = [resolve(x) for x in items]
        items = [x for x in items if x is not None]
        blocks.append({"title": title, "items": items})
    return {"doc": "traumatisme_thoracique", "sections": blocks}


def extract_traumatisme_cranien():
    import style
    import fiche_traumatisme_cranien as m
    trace = []
    make_module_patches(m, trace)
    make_module_patches(style, trace)

    blocks = []
    for title, fn in m.SECTIONS:
        items = fn()
        items = [resolve(x) for x in items]
        items = [x for x in items if x is not None]
        blocks.append({"title": title, "items": items})
    return {"doc": "traumatisme_cranien", "sections": blocks}


def extract_traumatisme_vertebromedullaire():
    import style
    import fiche_traumatisme_vertebromedullaire as m
    trace = []
    make_module_patches(m, trace)
    make_module_patches(style, trace)

    blocks = []
    for title, fn in m.SECTIONS:
        items = fn()
        items = [resolve(x) for x in items]
        items = [x for x in items if x is not None]
        blocks.append({"title": title, "items": items})
    return {"doc": "traumatisme_vertebromedullaire", "sections": blocks}


def extract_intubation_reanimation():
    import style
    import fiche_intubation_reanimation as m
    trace = []
    make_module_patches(m, trace)
    make_module_patches(style, trace)

    blocks = []
    for title, fn in m.SECTIONS:
        items = fn()
        items = [resolve(x) for x in items]
        items = [x for x in items if x is not None]
        blocks.append({"title": title, "items": items})
    return {"doc": "intubation_reanimation", "sections": blocks}


def extract_traumatisme_cranien_leger():
    import style
    import fiche_traumatisme_cranien_leger as m
    trace = []
    make_module_patches(m, trace)
    make_module_patches(style, trace)

    blocks = []
    for title, fn in m.SECTIONS:
        items = fn()
        items = [resolve(x) for x in items]
        items = [x for x in items if x is not None]
        blocks.append({"title": title, "items": items})
    return {"doc": "traumatisme_cranien_leger", "sections": blocks}


def extract_lat_soins_critiques():
    import style
    import fiche_lat_soins_critiques as m
    trace = []
    make_module_patches(m, trace)
    make_module_patches(style, trace)

    blocks = []
    for title, fn in m.SECTIONS:
        items = fn()
        items = [resolve(x) for x in items]
        items = [x for x in items if x is not None]
        blocks.append({"title": title, "items": items})
    return {"doc": "lat_soins_critiques", "sections": blocks}


def extract_sdra():
    import style
    import fiche_sdra as m
    trace = []
    make_module_patches(m, trace)
    make_module_patches(style, trace)

    blocks = []
    for title, fn in m.SECTIONS:
        items = fn()
        items = [resolve(x) for x in items]
        items = [x for x in items if x is not None]
        blocks.append({"title": title, "items": items})
    return {"doc": "sdra", "sections": blocks}


def extract_pavm():
    import style
    import fiche_pavm as m
    trace = []
    make_module_patches(m, trace)
    make_module_patches(style, trace)

    blocks = []
    for title, fn in m.SECTIONS:
        items = fn()
        items = [resolve(x) for x in items]
        items = [x for x in items if x is not None]
        blocks.append({"title": title, "items": items})
    return {"doc": "pavm", "sections": blocks}


def extract_tracheotomie():
    import style
    import fiche_tracheotomie as m
    trace = []
    make_module_patches(m, trace)
    make_module_patches(style, trace)

    blocks = []
    for title, fn in m.SECTIONS:
        items = fn()
        items = [resolve(x) for x in items]
        items = [x for x in items if x is not None]
        blocks.append({"title": title, "items": items})
    return {"doc": "tracheotomie", "sections": blocks}


def extract_nutrition():
    import style
    import fiche_nutrition as m
    trace = []
    make_module_patches(m, trace)
    make_module_patches(style, trace)

    blocks = []
    for title, fn in m.SECTIONS:
        items = fn()
        items = [resolve(x) for x in items]
        items = [x for x in items if x is not None]
        blocks.append({"title": title, "items": items})
    return {"doc": "nutrition", "sections": blocks}


def extract_eer():
    import style
    import fiche_eer as m
    trace = []
    make_module_patches(m, trace)
    make_module_patches(style, trace)

    blocks = []
    for title, fn in m.SECTIONS:
        items = fn()
        items = [resolve(x) for x in items]
        items = [x for x in items if x is not None]
        blocks.append({"title": title, "items": items})
    return {"doc": "eer", "sections": blocks}


def extract_ira():
    import style
    import fiche_ira as m
    trace = []
    make_module_patches(m, trace)
    make_module_patches(style, trace)

    blocks = []
    for title, fn in m.SECTIONS:
        items = fn()
        items = [resolve(x) for x in items]
        items = [x for x in items if x is not None]
        blocks.append({"title": title, "items": items})
    return {"doc": "ira", "sections": blocks}


def extract_ih():
    import style
    import fiche_ih as m
    trace = []
    make_module_patches(m, trace)
    make_module_patches(style, trace)

    blocks = []
    for title, fn in m.SECTIONS:
        items = fn()
        items = [resolve(x) for x in items]
        items = [x for x in items if x is not None]
        blocks.append({"title": title, "items": items})
    return {"doc": "ih", "sections": blocks}


def extract_epanchement_pleural():
    import style
    import fiche_epanchement_pleural as m
    trace = []
    make_module_patches(m, trace)
    make_module_patches(style, trace)

    blocks = []
    for title, fn in m.SECTIONS:
        items = fn()
        items = [resolve(x) for x in items]
        items = [x for x in items if x is not None]
        blocks.append({"title": title, "items": items})
    return {"doc": "epanchement_pleural", "sections": blocks}


def extract_anemie():
    import style
    import fiche_anemie as m
    trace = []
    make_module_patches(m, trace)
    make_module_patches(style, trace)

    blocks = []
    for title, fn in m.SECTIONS:
        items = fn()
        items = [resolve(x) for x in items]
        items = [x for x in items if x is not None]
        blocks.append({"title": title, "items": items})
    return {"doc": "anemie", "sections": blocks}


def extract_hypothermie():
    import style
    import fiche_hypothermie as m
    trace = []
    make_module_patches(m, trace)
    make_module_patches(style, trace)

    blocks = []
    for title, fn in m.SECTIONS:
        items = fn()
        items = [resolve(x) for x in items]
        items = [x for x in items if x is not None]
        blocks.append({"title": title, "items": items})
    return {"doc": "hypothermie", "sections": blocks}


def extract_nvpo():
    import style
    import fiche_nvpo as m
    trace = []
    make_module_patches(m, trace)
    make_module_patches(style, trace)

    blocks = []
    for title, fn in m.SECTIONS:
        items = fn()
        items = [resolve(x) for x in items]
        items = [x for x in items if x is not None]
        blocks.append({"title": title, "items": items})
    return {"doc": "nvpo", "sections": blocks}


def extract_aap_programmee():
    import style
    import fiche_aap_programmee as m
    trace = []
    make_module_patches(m, trace)
    make_module_patches(style, trace)

    blocks = []
    for title, fn in m.SECTIONS:
        items = fn()
        items = [resolve(x) for x in items]
        items = [x for x in items if x is not None]
        blocks.append({"title": title, "items": items})
    return {"doc": "aap_programmee", "sections": blocks}


def extract_mtev_perioperatoire():
    import style
    import fiche_mtev_perioperatoire as m
    trace = []
    make_module_patches(m, trace)
    make_module_patches(style, trace)

    blocks = []
    for title, fn in m.SECTIONS:
        items = fn()
        items = [resolve(x) for x in items]
        items = [x for x in items if x is not None]
        blocks.append({"title": title, "items": items})
    return {"doc": "mtev_perioperatoire", "sections": blocks}


def extract_glycemie():
    import style
    import fiche_glycemie as m
    trace = []
    make_module_patches(m, trace)
    make_module_patches(style, trace)

    blocks = []
    for title, fn in m.SECTIONS:
        items = fn()
        items = [resolve(x) for x in items]
        items = [x for x in items if x is not None]
        blocks.append({"title": title, "items": items})
    return {"doc": "glycemie", "sections": blocks}


def extract_mal_epileptique():
    import style
    import fiche_mal_epileptique as m
    trace = []
    make_module_patches(m, trace)
    make_module_patches(style, trace)

    blocks = []
    for title, fn in m.SECTIONS:
        items = fn()
        items = [resolve(x) for x in items]
        items = [x for x in items if x is not None]
        blocks.append({"title": title, "items": items})
    return {"doc": "mal_epileptique", "sections": blocks}


def extract_allergie_prevention():
    import style
    import fiche_allergie_prevention as m
    trace = []
    make_module_patches(m, trace)
    make_module_patches(style, trace)

    blocks = []
    for title, fn in m.SECTIONS:
        items = fn()
        items = [resolve(x) for x in items]
        items = [x for x in items if x is not None]
        blocks.append({"title": title, "items": items})
    return {"doc": "allergie_prevention", "sections": blocks}


def extract_antibioprophylaxie():
    import style
    import fiche_antibioprophylaxie as m
    trace = []
    make_module_patches(m, trace)
    make_module_patches(style, trace)

    blocks = []
    for title, fn in m.SECTIONS:
        items = fn()
        items = [resolve(x) for x in items]
        items = [x for x in items if x is not None]
        blocks.append({"title": title, "items": items})
    return {"doc": "antibioprophylaxie", "sections": blocks}


def extract_controle_temperature():
    import style
    import fiche_controle_temperature as m
    trace = []
    make_module_patches(m, trace)
    make_module_patches(style, trace)

    blocks = []
    for title, fn in m.SECTIONS:
        # This fiche wraps some champs in a real (unpatched) KeepTogether - a print-layout
        # hint to avoid orphan lines when merging short champs onto shared pages - which
        # resolve() now flattens into a list-of-items rather than a single item. Flatten one
        # level here so "items" stays the flat list the site's renderer expects (no other
        # fiche in the corpus needs this: none of them append a nested list at top level).
        items = fn()
        resolved = []
        for x in items:
            r = resolve(x)
            if r is None:
                continue
            if isinstance(r, list):
                resolved.extend(v for v in r if v is not None)
            else:
                resolved.append(r)
        blocks.append({"title": title, "items": resolved})
    return {"doc": "controle_temperature", "sections": blocks}


def extract_tih():
    import style
    import fiche_tih as m
    trace = []
    make_module_patches(m, trace)
    make_module_patches(style, trace)

    blocks = []
    for title, fn in m.SECTIONS:
        # Same KeepTogether-flattening as extract_controle_temperature(): several _section_*
        # helpers in fiche_tih.py wrap a heading+note pair in a real (unpatched) KeepTogether
        # to avoid orphan lines when algorithm tables are merged onto shared pages - resolve()
        # turns that into a list-of-items rather than a single item, so flatten one level here.
        items = fn()
        resolved = []
        for x in items:
            r = resolve(x)
            if r is None:
                continue
            if isinstance(r, list):
                resolved.extend(v for v in r if v is not None)
            else:
                resolved.append(r)
        blocks.append({"title": title, "items": resolved})
    return {"doc": "tih", "sections": blocks}


def extract_civd():
    import style
    import fiche_civd as m
    trace = []
    make_module_patches(m, trace)
    make_module_patches(style, trace)

    blocks = []
    for title, fn in m.SECTIONS:
        # Same KeepTogether-flattening as extract_tih()/extract_controle_temperature():
        # several _section_* helpers in fiche_civd.py wrap a heading+table pair in a real
        # (unpatched) KeepTogether to avoid orphan lines - resolve() turns that into a
        # list-of-items rather than a single item, so flatten one level here.
        items = fn()
        resolved = []
        for x in items:
            r = resolve(x)
            if r is None:
                continue
            if isinstance(r, list):
                resolved.extend(v for v in r if v is not None)
            else:
                resolved.append(r)
        blocks.append({"title": title, "items": resolved})
    return {"doc": "civd", "sections": blocks}


def extract_eclsa():
    import style
    import fiche_eclsa as m
    trace = []
    make_module_patches(m, trace)
    make_module_patches(style, trace)

    blocks = []
    for title, fn in m.SECTIONS:
        # Same KeepTogether-flattening as extract_tih()/extract_civd(): several
        # _section_* helpers in fiche_eclsa.py wrap a heading+table pair in a real
        # (unpatched) KeepTogether to avoid orphan lines - resolve() turns that into a
        # list-of-items rather than a single item, so flatten one level here.
        items = fn()
        resolved = []
        for x in items:
            r = resolve(x)
            if r is None:
                continue
            if isinstance(r, list):
                resolved.extend(v for v in r if v is not None)
            else:
                resolved.append(r)
        blocks.append({"title": title, "items": resolved})
    return {"doc": "eclsa", "sections": blocks}


def extract_transport_intrahospitalier():
    import style
    import fiche_transport_intrahospitalier as m
    trace = []
    make_module_patches(m, trace)
    make_module_patches(style, trace)

    blocks = []
    for title, fn in m.SECTIONS:
        # Same KeepTogether-flattening as extract_tih()/extract_civd()/extract_eclsa():
        # not actually used by fiche_transport_intrahospitalier.py's single combined
        # section, but kept for consistency with the shared extraction pattern.
        items = fn()
        resolved = []
        for x in items:
            r = resolve(x)
            if r is None:
                continue
            if isinstance(r, list):
                resolved.extend(v for v in r if v is not None)
            else:
                resolved.append(r)
        blocks.append({"title": title, "items": resolved})
    return {"doc": "transport_intrahospitalier", "sections": blocks}


def extract_transfusion_plasma():
    import style
    import fiche_transfusion_plasma as m
    trace = []
    make_module_patches(m, trace)
    make_module_patches(style, trace)

    blocks = []
    for title, fn in m.SECTIONS:
        items = fn()
        resolved = []
        for x in items:
            r = resolve(x)
            if r is None:
                continue
            if isinstance(r, list):
                resolved.extend(v for v in r if v is not None)
            else:
                resolved.append(r)
        blocks.append({"title": title, "items": resolved})
    return {"doc": "transfusion_plasma", "sections": blocks}


if __name__ == "__main__":
    # NOTE 2026-09-04: fiche_anticoagulants.py, fiche_ecbu.py and annexe_specialites.py
    # were lost from the /tmp scratchpad (along with style.py) during a long idle gap,
    # apparently swept as the oldest-untouched files in the project. Their already-generated
    # content_anticoagulants.json / content_ecbu.json are intact on disk and correct (they
    # predate the loss and don't need regenerating), so these two extractions are skipped
    # rather than crashing the whole pipeline. See project memory for the full incident.
    try:
        anticoag = extract_anticoagulants()
        with open(os.path.join(BUILD_DIR, "content_anticoagulants.json"), "w") as f:
            json.dump(anticoag, f, ensure_ascii=False, indent=1)
        print("anticoagulants sections:", len(anticoag["sections"]),
              "total blocks:", sum(len(s["items"]) for s in anticoag["sections"]))
    except ModuleNotFoundError as e:
        print("SKIPPED anticoagulants extraction (source module missing):", e,
              "-- existing content_anticoagulants.json left untouched")

    # ECBU: reset module cache to avoid state leaking from the anticoagulants extraction
    for mn in list(sys.modules):
        if mn in ("fiche_ecbu", "style", "annexe_specialites", "fiche_anticoagulants"):
            del sys.modules[mn]
    try:
        ecbu = extract_ecbu()
        with open(os.path.join(BUILD_DIR, "content_ecbu.json"), "w") as f:
            json.dump(ecbu, f, ensure_ascii=False, indent=1)
        print("ecbu sections:", len(ecbu["sections"]),
              "total blocks:", sum(len(s["items"]) for s in ecbu["sections"]))
    except ModuleNotFoundError as e:
        print("SKIPPED ecbu extraction (source module missing):", e,
              "-- existing content_ecbu.json left untouched")

    for mn in list(sys.modules):
        if mn in ("fiche_ecbu", "style", "annexe_specialites", "fiche_anticoagulants", "fiche_choc_hemorragique"):
            del sys.modules[mn]
    try:
        choc = extract_choc_hemorragique()
        with open(os.path.join(BUILD_DIR, "content_choc_hemorragique.json"), "w") as f:
            json.dump(choc, f, ensure_ascii=False, indent=1)
        print("choc_hemorragique sections:", len(choc["sections"]),
              "total blocks:", sum(len(s["items"]) for s in choc["sections"]))
    except ModuleNotFoundError as e:
        print("SKIPPED choc_hemorragique extraction (source module missing):", e,
              "-- existing content_choc_hemorragique.json left untouched")

    for mn in list(sys.modules):
        if mn in ("fiche_ecbu", "style", "annexe_specialites", "fiche_anticoagulants", "fiche_choc_hemorragique", "fiche_intubation_urgence"):
            del sys.modules[mn]
    try:
        intub = extract_intubation_urgence()
        with open(os.path.join(BUILD_DIR, "content_intubation_urgence.json"), "w") as f:
            json.dump(intub, f, ensure_ascii=False, indent=1)
        print("intubation_urgence sections:", len(intub["sections"]),
              "total blocks:", sum(len(s["items"]) for s in intub["sections"]))
    except ModuleNotFoundError as e:
        print("SKIPPED intubation_urgence extraction (source module missing):", e,
              "-- existing content_intubation_urgence.json left untouched")

    for mn in list(sys.modules):
        if mn in ("fiche_ecbu", "style", "annexe_specialites", "fiche_anticoagulants", "fiche_choc_hemorragique", "fiche_intubation_urgence", "fiche_sepsis"):
            del sys.modules[mn]
    try:
        sepsis = extract_sepsis()
        with open(os.path.join(BUILD_DIR, "content_sepsis.json"), "w") as f:
            json.dump(sepsis, f, ensure_ascii=False, indent=1)
        print("sepsis sections:", len(sepsis["sections"]),
              "total blocks:", sum(len(s["items"]) for s in sepsis["sections"]))
    except ModuleNotFoundError as e:
        print("SKIPPED sepsis extraction (source module missing):", e,
              "-- existing content_sepsis.json left untouched")

    for mn in list(sys.modules):
        if mn in ("fiche_ecbu", "style", "annexe_specialites", "fiche_anticoagulants", "fiche_choc_hemorragique", "fiche_intubation_urgence", "fiche_sepsis", "fiche_urgences_obstetricales"):
            del sys.modules[mn]
    try:
        urg_obst = extract_urgences_obstetricales()
        with open(os.path.join(BUILD_DIR, "content_urgences_obstetricales.json"), "w") as f:
            json.dump(urg_obst, f, ensure_ascii=False, indent=1)
        print("urgences_obstetricales sections:", len(urg_obst["sections"]),
              "total blocks:", sum(len(s["items"]) for s in urg_obst["sections"]))
    except ModuleNotFoundError as e:
        print("SKIPPED urgences_obstetricales extraction (source module missing):", e,
              "-- existing content_urgences_obstetricales.json left untouched")

    for mn in list(sys.modules):
        if mn in ("fiche_ecbu", "style", "annexe_specialites", "fiche_anticoagulants", "fiche_choc_hemorragique", "fiche_intubation_urgence", "fiche_sepsis", "fiche_urgences_obstetricales", "fiche_anaphylaxie"):
            del sys.modules[mn]
    try:
        anaph = extract_anaphylaxie()
        with open(os.path.join(BUILD_DIR, "content_anaphylaxie.json"), "w") as f:
            json.dump(anaph, f, ensure_ascii=False, indent=1)
        print("anaphylaxie sections:", len(anaph["sections"]),
              "total blocks:", sum(len(s["items"]) for s in anaph["sections"]))
    except ModuleNotFoundError as e:
        print("SKIPPED anaphylaxie extraction (source module missing):", e,
              "-- existing content_anaphylaxie.json left untouched")

    for mn in list(sys.modules):
        if mn in ("fiche_ecbu", "style", "annexe_specialites", "fiche_anticoagulants", "fiche_choc_hemorragique", "fiche_intubation_urgence", "fiche_sepsis", "fiche_urgences_obstetricales", "fiche_anaphylaxie", "fiche_preeclampsie"):
            del sys.modules[mn]
    try:
        preec = extract_preeclampsie()
        with open(os.path.join(BUILD_DIR, "content_preeclampsie.json"), "w") as f:
            json.dump(preec, f, ensure_ascii=False, indent=1)
        print("preeclampsie sections:", len(preec["sections"]),
              "total blocks:", sum(len(s["items"]) for s in preec["sections"]))
    except ModuleNotFoundError as e:
        print("SKIPPED preeclampsie extraction (source module missing):", e,
              "-- existing content_preeclampsie.json left untouched")

    for mn in list(sys.modules):
        if mn in ("fiche_ecbu", "style", "annexe_specialites", "fiche_anticoagulants", "fiche_choc_hemorragique", "fiche_intubation_urgence", "fiche_sepsis", "fiche_urgences_obstetricales", "fiche_anaphylaxie", "fiche_preeclampsie", "fiche_hyperthermie_maligne"):
            del sys.modules[mn]
    try:
        hm = extract_hyperthermie_maligne()
        with open(os.path.join(BUILD_DIR, "content_hyperthermie_maligne.json"), "w") as f:
            json.dump(hm, f, ensure_ascii=False, indent=1)
        print("hyperthermie_maligne sections:", len(hm["sections"]),
              "total blocks:", sum(len(s["items"]) for s in hm["sections"]))
    except ModuleNotFoundError as e:
        print("SKIPPED hyperthermie_maligne extraction (source module missing):", e,
              "-- existing content_hyperthermie_maligne.json left untouched")

    for mn in list(sys.modules):
        if mn in ("fiche_ecbu", "style", "annexe_specialites", "fiche_anticoagulants", "fiche_choc_hemorragique", "fiche_intubation_urgence", "fiche_sepsis", "fiche_urgences_obstetricales", "fiche_anaphylaxie", "fiche_preeclampsie", "fiche_hyperthermie_maligne", "fiche_anticoag_urgence"):
            del sys.modules[mn]
    try:
        anticoagU = extract_anticoag_urgence()
        with open(os.path.join(BUILD_DIR, "content_anticoag_urgence.json"), "w") as f:
            json.dump(anticoagU, f, ensure_ascii=False, indent=1)
        print("anticoag_urgence sections:", len(anticoagU["sections"]),
              "total blocks:", sum(len(s["items"]) for s in anticoagU["sections"]))
    except ModuleNotFoundError as e:
        print("SKIPPED anticoag_urgence extraction (source module missing):", e,
              "-- existing content_anticoag_urgence.json left untouched")

    for mn in list(sys.modules):
        if mn in ("fiche_ecbu", "style", "annexe_specialites", "fiche_anticoagulants", "fiche_choc_hemorragique", "fiche_intubation_urgence", "fiche_sepsis", "fiche_urgences_obstetricales", "fiche_anaphylaxie", "fiche_preeclampsie", "fiche_hyperthermie_maligne", "fiche_anticoag_urgence", "fiche_traumatisme_abdominal"):
            del sys.modules[mn]
    try:
        trauma_abdo = extract_traumatisme_abdominal()
        with open(os.path.join(BUILD_DIR, "content_traumatisme_abdominal.json"), "w") as f:
            json.dump(trauma_abdo, f, ensure_ascii=False, indent=1)
        print("traumatisme_abdominal sections:", len(trauma_abdo["sections"]),
              "total blocks:", sum(len(s["items"]) for s in trauma_abdo["sections"]))
    except ModuleNotFoundError as e:
        print("SKIPPED traumatisme_abdominal extraction (source module missing):", e,
              "-- existing content_traumatisme_abdominal.json left untouched")

    for mn in list(sys.modules):
        if mn in ("fiche_ecbu", "style", "annexe_specialites", "fiche_anticoagulants", "fiche_choc_hemorragique", "fiche_intubation_urgence", "fiche_sepsis", "fiche_urgences_obstetricales", "fiche_anaphylaxie", "fiche_preeclampsie", "fiche_hyperthermie_maligne", "fiche_anticoag_urgence", "fiche_traumatisme_abdominal", "fiche_sedation_reanimation"):
            del sys.modules[mn]
    try:
        sedation = extract_sedation_reanimation()
        with open(os.path.join(BUILD_DIR, "content_sedation_reanimation.json"), "w") as f:
            json.dump(sedation, f, ensure_ascii=False, indent=1)
        print("sedation_reanimation sections:", len(sedation["sections"]),
              "total blocks:", sum(len(s["items"]) for s in sedation["sections"]))
    except ModuleNotFoundError as e:
        print("SKIPPED sedation_reanimation extraction (source module missing):", e,
              "-- existing content_sedation_reanimation.json left untouched")

    for mn in list(sys.modules):
        if mn in ("fiche_ecbu", "style", "annexe_specialites", "fiche_anticoagulants", "fiche_choc_hemorragique", "fiche_intubation_urgence", "fiche_sepsis", "fiche_urgences_obstetricales", "fiche_anaphylaxie", "fiche_preeclampsie", "fiche_hyperthermie_maligne", "fiche_anticoag_urgence", "fiche_traumatisme_abdominal", "fiche_sedation_reanimation", "fiche_sedation_urgences"):
            del sys.modules[mn]
    try:
        sedation_urg = extract_sedation_urgences()
        with open(os.path.join(BUILD_DIR, "content_sedation_urgences.json"), "w") as f:
            json.dump(sedation_urg, f, ensure_ascii=False, indent=1)
        print("sedation_urgences sections:", len(sedation_urg["sections"]),
              "total blocks:", sum(len(s["items"]) for s in sedation_urg["sections"]))
    except ModuleNotFoundError as e:
        print("SKIPPED sedation_urgences extraction (source module missing):", e,
              "-- existing content_sedation_urgences.json left untouched")

    for mn in list(sys.modules):
        if mn in ("fiche_ecbu", "style", "annexe_specialites", "fiche_anticoagulants", "fiche_choc_hemorragique", "fiche_intubation_urgence", "fiche_sepsis", "fiche_urgences_obstetricales", "fiche_anaphylaxie", "fiche_preeclampsie", "fiche_hyperthermie_maligne", "fiche_anticoag_urgence", "fiche_traumatisme_abdominal", "fiche_sedation_reanimation", "fiche_sedation_urgences", "fiche_vni"):
            del sys.modules[mn]
    try:
        vni = extract_vni()
        with open(os.path.join(BUILD_DIR, "content_vni.json"), "w") as f:
            json.dump(vni, f, ensure_ascii=False, indent=1)
        print("vni sections:", len(vni["sections"]),
              "total blocks:", sum(len(s["items"]) for s in vni["sections"]))
    except ModuleNotFoundError as e:
        print("SKIPPED vni extraction (source module missing):", e,
              "-- existing content_vni.json left untouched")

    for mn in list(sys.modules):
        if mn in ("fiche_ecbu", "style", "annexe_specialites", "fiche_anticoagulants", "fiche_choc_hemorragique", "fiche_intubation_urgence", "fiche_sepsis", "fiche_urgences_obstetricales", "fiche_anaphylaxie", "fiche_preeclampsie", "fiche_hyperthermie_maligne", "fiche_anticoag_urgence", "fiche_traumatisme_abdominal", "fiche_sedation_reanimation", "fiche_sedation_urgences", "fiche_vni", "fiche_aap_urgence"):
            del sys.modules[mn]
    aap = extract_aap_urgence()
    with open(os.path.join(BUILD_DIR, "content_aap_urgence.json"), "w") as f:
        json.dump(aap, f, ensure_ascii=False, indent=1)
    print("aap_urgence sections:", len(aap["sections"]),
          "total blocks:", sum(len(s["items"]) for s in aap["sections"]))

    for mn in list(sys.modules):
        if mn in ("fiche_ecbu", "style", "annexe_specialites", "fiche_anticoagulants", "fiche_choc_hemorragique", "fiche_intubation_urgence", "fiche_sepsis", "fiche_urgences_obstetricales", "fiche_anaphylaxie", "fiche_preeclampsie", "fiche_hyperthermie_maligne", "fiche_anticoag_urgence", "fiche_traumatisme_abdominal", "fiche_sedation_reanimation", "fiche_sedation_urgences", "fiche_vni", "fiche_aap_urgence", "fiche_curares"):
            del sys.modules[mn]
    curares = extract_curares()
    with open(os.path.join(BUILD_DIR, "content_curares.json"), "w") as f:
        json.dump(curares, f, ensure_ascii=False, indent=1)
    print("curares sections:", len(curares["sections"]),
          "total blocks:", sum(len(s["items"]) for s in curares["sections"]))

    for mn in list(sys.modules):
        if mn in ("fiche_ecbu", "style", "annexe_specialites", "fiche_anticoagulants", "fiche_choc_hemorragique", "fiche_intubation_urgence", "fiche_sepsis", "fiche_urgences_obstetricales", "fiche_anaphylaxie", "fiche_preeclampsie", "fiche_hyperthermie_maligne", "fiche_anticoag_urgence", "fiche_traumatisme_abdominal", "fiche_sedation_reanimation", "fiche_sedation_urgences", "fiche_vni", "fiche_aap_urgence", "fiche_curares", "fiche_remplissage"):
            del sys.modules[mn]
    remplissage = extract_remplissage()
    with open(os.path.join(BUILD_DIR, "content_remplissage.json"), "w") as f:
        json.dump(remplissage, f, ensure_ascii=False, indent=1)
    print("remplissage sections:", len(remplissage["sections"]),
          "total blocks:", sum(len(s["items"]) for s in remplissage["sections"]))

    for mn in list(sys.modules):
        if mn in ("fiche_ecbu", "style", "annexe_specialites", "fiche_anticoagulants", "fiche_choc_hemorragique", "fiche_intubation_urgence", "fiche_sepsis", "fiche_urgences_obstetricales", "fiche_anaphylaxie", "fiche_preeclampsie", "fiche_hyperthermie_maligne", "fiche_anticoag_urgence", "fiche_traumatisme_abdominal", "fiche_sedation_reanimation", "fiche_sedation_urgences", "fiche_vni", "fiche_aap_urgence", "fiche_curares", "fiche_remplissage", "fiche_traumatisme_membre"):
            del sys.modules[mn]
    trauma_membre = extract_traumatisme_membre()
    with open(os.path.join(BUILD_DIR, "content_traumatisme_membre.json"), "w") as f:
        json.dump(trauma_membre, f, ensure_ascii=False, indent=1)
    print("traumatisme_membre sections:", len(trauma_membre["sections"]),
          "total blocks:", sum(len(s["items"]) for s in trauma_membre["sections"]))

    for mn in list(sys.modules):
        if mn in ("fiche_ecbu", "style", "annexe_specialites", "fiche_anticoagulants", "fiche_choc_hemorragique", "fiche_intubation_urgence", "fiche_sepsis", "fiche_urgences_obstetricales", "fiche_anaphylaxie", "fiche_preeclampsie", "fiche_hyperthermie_maligne", "fiche_anticoag_urgence", "fiche_traumatisme_abdominal", "fiche_sedation_reanimation", "fiche_sedation_urgences", "fiche_vni", "fiche_aap_urgence", "fiche_curares", "fiche_remplissage", "fiche_traumatisme_membre", "fiche_voies_aeriennes_enfant"):
            del sys.modules[mn]
    voies_enfant = extract_voies_aeriennes_enfant()
    with open(os.path.join(BUILD_DIR, "content_voies_aeriennes_enfant.json"), "w") as f:
        json.dump(voies_enfant, f, ensure_ascii=False, indent=1)
    print("voies_aeriennes_enfant sections:", len(voies_enfant["sections"]),
          "total blocks:", sum(len(s["items"]) for s in voies_enfant["sections"]))

    for mn in list(sys.modules):
        if mn in ("fiche_ecbu", "style", "annexe_specialites", "fiche_anticoagulants", "fiche_choc_hemorragique", "fiche_intubation_urgence", "fiche_sepsis", "fiche_urgences_obstetricales", "fiche_anaphylaxie", "fiche_preeclampsie", "fiche_hyperthermie_maligne", "fiche_anticoag_urgence", "fiche_traumatisme_abdominal", "fiche_sedation_reanimation", "fiche_sedation_urgences", "fiche_vni", "fiche_aap_urgence", "fiche_curares", "fiche_remplissage", "fiche_traumatisme_membre", "fiche_voies_aeriennes_enfant", "fiche_intubation_difficile_adulte"):
            del sys.modules[mn]
    intub_diff = extract_intubation_difficile_adulte()
    with open(os.path.join(BUILD_DIR, "content_intubation_difficile_adulte.json"), "w") as f:
        json.dump(intub_diff, f, ensure_ascii=False, indent=1)
    print("intubation_difficile_adulte sections:", len(intub_diff["sections"]),
          "total blocks:", sum(len(s["items"]) for s in intub_diff["sections"]))

    for mn in list(sys.modules):
        if mn in ("fiche_ecbu", "style", "annexe_specialites", "fiche_anticoagulants", "fiche_choc_hemorragique", "fiche_intubation_urgence", "fiche_sepsis", "fiche_urgences_obstetricales", "fiche_anaphylaxie", "fiche_preeclampsie", "fiche_hyperthermie_maligne", "fiche_anticoag_urgence", "fiche_traumatisme_abdominal", "fiche_sedation_reanimation", "fiche_sedation_urgences", "fiche_vni", "fiche_aap_urgence", "fiche_curares", "fiche_remplissage", "fiche_traumatisme_membre", "fiche_voies_aeriennes_enfant", "fiche_intubation_difficile_adulte", "fiche_traumatisme_pelvien"):
            del sys.modules[mn]
    trauma_pelvien = extract_traumatisme_pelvien()
    with open(os.path.join(BUILD_DIR, "content_traumatisme_pelvien.json"), "w") as f:
        json.dump(trauma_pelvien, f, ensure_ascii=False, indent=1)
    print("traumatisme_pelvien sections:", len(trauma_pelvien["sections"]),
          "total blocks:", sum(len(s["items"]) for s in trauma_pelvien["sections"]))

    for mn in list(sys.modules):
        if mn in ("fiche_ecbu", "style", "annexe_specialites", "fiche_anticoagulants", "fiche_choc_hemorragique", "fiche_intubation_urgence", "fiche_sepsis", "fiche_urgences_obstetricales", "fiche_anaphylaxie", "fiche_preeclampsie", "fiche_hyperthermie_maligne", "fiche_anticoag_urgence", "fiche_traumatisme_abdominal", "fiche_sedation_reanimation", "fiche_sedation_urgences", "fiche_vni", "fiche_aap_urgence", "fiche_curares", "fiche_remplissage", "fiche_traumatisme_membre", "fiche_voies_aeriennes_enfant", "fiche_intubation_difficile_adulte", "fiche_traumatisme_pelvien", "fiche_traumatisme_thoracique"):
            del sys.modules[mn]
    trauma_thorax = extract_traumatisme_thoracique()
    with open(os.path.join(BUILD_DIR, "content_traumatisme_thoracique.json"), "w") as f:
        json.dump(trauma_thorax, f, ensure_ascii=False, indent=1)
    print("traumatisme_thoracique sections:", len(trauma_thorax["sections"]),
          "total blocks:", sum(len(s["items"]) for s in trauma_thorax["sections"]))

    for mn in list(sys.modules):
        if mn in ("fiche_ecbu", "style", "annexe_specialites", "fiche_anticoagulants", "fiche_choc_hemorragique", "fiche_intubation_urgence", "fiche_sepsis", "fiche_urgences_obstetricales", "fiche_anaphylaxie", "fiche_preeclampsie", "fiche_hyperthermie_maligne", "fiche_anticoag_urgence", "fiche_traumatisme_abdominal", "fiche_sedation_reanimation", "fiche_sedation_urgences", "fiche_vni", "fiche_aap_urgence", "fiche_curares", "fiche_remplissage", "fiche_traumatisme_membre", "fiche_voies_aeriennes_enfant", "fiche_intubation_difficile_adulte", "fiche_traumatisme_pelvien", "fiche_traumatisme_thoracique", "fiche_traumatisme_cranien"):
            del sys.modules[mn]
    trauma_cranien = extract_traumatisme_cranien()
    with open(os.path.join(BUILD_DIR, "content_traumatisme_cranien.json"), "w") as f:
        json.dump(trauma_cranien, f, ensure_ascii=False, indent=1)
    print("traumatisme_cranien sections:", len(trauma_cranien["sections"]),
          "total blocks:", sum(len(s["items"]) for s in trauma_cranien["sections"]))

    for mn in list(sys.modules):
        if mn in ("fiche_ecbu", "style", "annexe_specialites", "fiche_anticoagulants", "fiche_choc_hemorragique", "fiche_intubation_urgence", "fiche_sepsis", "fiche_urgences_obstetricales", "fiche_anaphylaxie", "fiche_preeclampsie", "fiche_hyperthermie_maligne", "fiche_anticoag_urgence", "fiche_traumatisme_abdominal", "fiche_sedation_reanimation", "fiche_sedation_urgences", "fiche_vni", "fiche_aap_urgence", "fiche_curares", "fiche_remplissage", "fiche_traumatisme_membre", "fiche_voies_aeriennes_enfant", "fiche_intubation_difficile_adulte", "fiche_traumatisme_pelvien", "fiche_traumatisme_thoracique", "fiche_traumatisme_cranien", "fiche_traumatisme_vertebromedullaire"):
            del sys.modules[mn]
    trauma_vert = extract_traumatisme_vertebromedullaire()
    with open(os.path.join(BUILD_DIR, "content_traumatisme_vertebromedullaire.json"), "w") as f:
        json.dump(trauma_vert, f, ensure_ascii=False, indent=1)
    print("traumatisme_vertebromedullaire sections:", len(trauma_vert["sections"]),
          "total blocks:", sum(len(s["items"]) for s in trauma_vert["sections"]))

    for mn in list(sys.modules):
        if mn in ("fiche_ecbu", "style", "annexe_specialites", "fiche_anticoagulants", "fiche_choc_hemorragique", "fiche_intubation_urgence", "fiche_sepsis", "fiche_urgences_obstetricales", "fiche_anaphylaxie", "fiche_preeclampsie", "fiche_hyperthermie_maligne", "fiche_anticoag_urgence", "fiche_traumatisme_abdominal", "fiche_sedation_reanimation", "fiche_sedation_urgences", "fiche_vni", "fiche_aap_urgence", "fiche_curares", "fiche_remplissage", "fiche_traumatisme_membre", "fiche_voies_aeriennes_enfant", "fiche_intubation_difficile_adulte", "fiche_traumatisme_pelvien", "fiche_traumatisme_thoracique", "fiche_traumatisme_cranien", "fiche_traumatisme_vertebromedullaire", "fiche_intubation_reanimation"):
            del sys.modules[mn]
    intub_reanim = extract_intubation_reanimation()
    with open(os.path.join(BUILD_DIR, "content_intubation_reanimation.json"), "w") as f:
        json.dump(intub_reanim, f, ensure_ascii=False, indent=1)
    print("intubation_reanimation sections:", len(intub_reanim["sections"]),
          "total blocks:", sum(len(s["items"]) for s in intub_reanim["sections"]))

    for mn in list(sys.modules):
        if mn in ("fiche_ecbu", "style", "annexe_specialites", "fiche_anticoagulants", "fiche_choc_hemorragique", "fiche_intubation_urgence", "fiche_sepsis", "fiche_urgences_obstetricales", "fiche_anaphylaxie", "fiche_preeclampsie", "fiche_hyperthermie_maligne", "fiche_anticoag_urgence", "fiche_traumatisme_abdominal", "fiche_sedation_reanimation", "fiche_sedation_urgences", "fiche_vni", "fiche_aap_urgence", "fiche_curares", "fiche_remplissage", "fiche_traumatisme_membre", "fiche_voies_aeriennes_enfant", "fiche_intubation_difficile_adulte", "fiche_traumatisme_pelvien", "fiche_traumatisme_thoracique", "fiche_traumatisme_cranien", "fiche_traumatisme_vertebromedullaire", "fiche_intubation_reanimation", "fiche_traumatisme_cranien_leger"):
            del sys.modules[mn]
    tcl = extract_traumatisme_cranien_leger()
    with open(os.path.join(BUILD_DIR, "content_traumatisme_cranien_leger.json"), "w") as f:
        json.dump(tcl, f, ensure_ascii=False, indent=1)
    print("traumatisme_cranien_leger sections:", len(tcl["sections"]),
          "total blocks:", sum(len(s["items"]) for s in tcl["sections"]))

    for mn in list(sys.modules):
        if mn in ("fiche_ecbu", "style", "annexe_specialites", "fiche_anticoagulants", "fiche_choc_hemorragique", "fiche_intubation_urgence", "fiche_sepsis", "fiche_urgences_obstetricales", "fiche_anaphylaxie", "fiche_preeclampsie", "fiche_hyperthermie_maligne", "fiche_anticoag_urgence", "fiche_traumatisme_abdominal", "fiche_sedation_reanimation", "fiche_sedation_urgences", "fiche_vni", "fiche_aap_urgence", "fiche_curares", "fiche_remplissage", "fiche_traumatisme_membre", "fiche_voies_aeriennes_enfant", "fiche_intubation_difficile_adulte", "fiche_traumatisme_pelvien", "fiche_traumatisme_thoracique", "fiche_traumatisme_cranien", "fiche_traumatisme_vertebromedullaire", "fiche_intubation_reanimation", "fiche_traumatisme_cranien_leger", "fiche_lat_soins_critiques"):
            del sys.modules[mn]
    lat = extract_lat_soins_critiques()
    with open(os.path.join(BUILD_DIR, "content_lat_soins_critiques.json"), "w") as f:
        json.dump(lat, f, ensure_ascii=False, indent=1)
    print("lat_soins_critiques sections:", len(lat["sections"]),
          "total blocks:", sum(len(s["items"]) for s in lat["sections"]))

    for mn in list(sys.modules):
        if mn in ("fiche_ecbu", "style", "annexe_specialites", "fiche_anticoagulants", "fiche_choc_hemorragique", "fiche_intubation_urgence", "fiche_sepsis", "fiche_urgences_obstetricales", "fiche_anaphylaxie", "fiche_preeclampsie", "fiche_hyperthermie_maligne", "fiche_anticoag_urgence", "fiche_traumatisme_abdominal", "fiche_sedation_reanimation", "fiche_sedation_urgences", "fiche_vni", "fiche_aap_urgence", "fiche_curares", "fiche_remplissage", "fiche_traumatisme_membre", "fiche_voies_aeriennes_enfant", "fiche_intubation_difficile_adulte", "fiche_traumatisme_pelvien", "fiche_traumatisme_thoracique", "fiche_traumatisme_cranien", "fiche_traumatisme_vertebromedullaire", "fiche_intubation_reanimation", "fiche_traumatisme_cranien_leger", "fiche_lat_soins_critiques", "fiche_sdra"):
            del sys.modules[mn]
    sdra = extract_sdra()
    with open(os.path.join(BUILD_DIR, "content_sdra.json"), "w") as f:
        json.dump(sdra, f, ensure_ascii=False, indent=1)
    print("sdra sections:", len(sdra["sections"]),
          "total blocks:", sum(len(s["items"]) for s in sdra["sections"]))

    for mn in list(sys.modules):
        if mn in ("fiche_ecbu", "style", "annexe_specialites", "fiche_anticoagulants", "fiche_choc_hemorragique", "fiche_intubation_urgence", "fiche_sepsis", "fiche_urgences_obstetricales", "fiche_anaphylaxie", "fiche_preeclampsie", "fiche_hyperthermie_maligne", "fiche_anticoag_urgence", "fiche_traumatisme_abdominal", "fiche_sedation_reanimation", "fiche_sedation_urgences", "fiche_vni", "fiche_aap_urgence", "fiche_curares", "fiche_remplissage", "fiche_traumatisme_membre", "fiche_voies_aeriennes_enfant", "fiche_intubation_difficile_adulte", "fiche_traumatisme_pelvien", "fiche_traumatisme_thoracique", "fiche_traumatisme_cranien", "fiche_traumatisme_vertebromedullaire", "fiche_intubation_reanimation", "fiche_traumatisme_cranien_leger", "fiche_lat_soins_critiques", "fiche_sdra", "fiche_pavm"):
            del sys.modules[mn]
    pavm = extract_pavm()
    with open(os.path.join(BUILD_DIR, "content_pavm.json"), "w") as f:
        json.dump(pavm, f, ensure_ascii=False, indent=1)
    print("pavm sections:", len(pavm["sections"]),
          "total blocks:", sum(len(s["items"]) for s in pavm["sections"]))

    for mn in list(sys.modules):
        if mn in ("fiche_ecbu", "style", "annexe_specialites", "fiche_anticoagulants", "fiche_choc_hemorragique", "fiche_intubation_urgence", "fiche_sepsis", "fiche_urgences_obstetricales", "fiche_anaphylaxie", "fiche_preeclampsie", "fiche_hyperthermie_maligne", "fiche_anticoag_urgence", "fiche_traumatisme_abdominal", "fiche_sedation_reanimation", "fiche_sedation_urgences", "fiche_vni", "fiche_aap_urgence", "fiche_curares", "fiche_remplissage", "fiche_traumatisme_membre", "fiche_voies_aeriennes_enfant", "fiche_intubation_difficile_adulte", "fiche_traumatisme_pelvien", "fiche_traumatisme_thoracique", "fiche_traumatisme_cranien", "fiche_traumatisme_vertebromedullaire", "fiche_intubation_reanimation", "fiche_traumatisme_cranien_leger", "fiche_lat_soins_critiques", "fiche_sdra", "fiche_pavm", "fiche_tracheotomie"):
            del sys.modules[mn]
    tracheo = extract_tracheotomie()
    with open(os.path.join(BUILD_DIR, "content_tracheotomie.json"), "w") as f:
        json.dump(tracheo, f, ensure_ascii=False, indent=1)
    print("tracheotomie sections:", len(tracheo["sections"]),
          "total blocks:", sum(len(s["items"]) for s in tracheo["sections"]))

    for mn in list(sys.modules):
        if mn in ("fiche_ecbu", "style", "annexe_specialites", "fiche_anticoagulants", "fiche_choc_hemorragique", "fiche_intubation_urgence", "fiche_sepsis", "fiche_urgences_obstetricales", "fiche_anaphylaxie", "fiche_preeclampsie", "fiche_hyperthermie_maligne", "fiche_anticoag_urgence", "fiche_traumatisme_abdominal", "fiche_sedation_reanimation", "fiche_sedation_urgences", "fiche_vni", "fiche_aap_urgence", "fiche_curares", "fiche_remplissage", "fiche_traumatisme_membre", "fiche_voies_aeriennes_enfant", "fiche_intubation_difficile_adulte", "fiche_traumatisme_pelvien", "fiche_traumatisme_thoracique", "fiche_traumatisme_cranien", "fiche_traumatisme_vertebromedullaire", "fiche_intubation_reanimation", "fiche_traumatisme_cranien_leger", "fiche_lat_soins_critiques", "fiche_sdra", "fiche_pavm", "fiche_tracheotomie", "fiche_nutrition"):
            del sys.modules[mn]
    nutrition = extract_nutrition()
    with open(os.path.join(BUILD_DIR, "content_nutrition.json"), "w") as f:
        json.dump(nutrition, f, ensure_ascii=False, indent=1)
    print("nutrition sections:", len(nutrition["sections"]),
          "total blocks:", sum(len(s["items"]) for s in nutrition["sections"]))

    for mn in list(sys.modules):
        if mn in ("fiche_ecbu", "style", "annexe_specialites", "fiche_anticoagulants", "fiche_choc_hemorragique", "fiche_intubation_urgence", "fiche_sepsis", "fiche_urgences_obstetricales", "fiche_anaphylaxie", "fiche_preeclampsie", "fiche_hyperthermie_maligne", "fiche_anticoag_urgence", "fiche_traumatisme_abdominal", "fiche_sedation_reanimation", "fiche_sedation_urgences", "fiche_vni", "fiche_aap_urgence", "fiche_curares", "fiche_remplissage", "fiche_traumatisme_membre", "fiche_voies_aeriennes_enfant", "fiche_intubation_difficile_adulte", "fiche_traumatisme_pelvien", "fiche_traumatisme_thoracique", "fiche_traumatisme_cranien", "fiche_traumatisme_vertebromedullaire", "fiche_intubation_reanimation", "fiche_traumatisme_cranien_leger", "fiche_lat_soins_critiques", "fiche_sdra", "fiche_pavm", "fiche_tracheotomie", "fiche_nutrition", "fiche_eer"):
            del sys.modules[mn]
    eer = extract_eer()
    with open(os.path.join(BUILD_DIR, "content_eer.json"), "w") as f:
        json.dump(eer, f, ensure_ascii=False, indent=1)
    print("eer sections:", len(eer["sections"]),
          "total blocks:", sum(len(s["items"]) for s in eer["sections"]))

    for mn in list(sys.modules):
        if mn in ("fiche_ecbu", "style", "annexe_specialites", "fiche_anticoagulants", "fiche_choc_hemorragique", "fiche_intubation_urgence", "fiche_sepsis", "fiche_urgences_obstetricales", "fiche_anaphylaxie", "fiche_preeclampsie", "fiche_hyperthermie_maligne", "fiche_anticoag_urgence", "fiche_traumatisme_abdominal", "fiche_sedation_reanimation", "fiche_sedation_urgences", "fiche_vni", "fiche_aap_urgence", "fiche_curares", "fiche_remplissage", "fiche_traumatisme_membre", "fiche_voies_aeriennes_enfant", "fiche_intubation_difficile_adulte", "fiche_traumatisme_pelvien", "fiche_traumatisme_thoracique", "fiche_traumatisme_cranien", "fiche_traumatisme_vertebromedullaire", "fiche_intubation_reanimation", "fiche_traumatisme_cranien_leger", "fiche_lat_soins_critiques", "fiche_sdra", "fiche_pavm", "fiche_tracheotomie", "fiche_nutrition", "fiche_eer"):
            del sys.modules[mn]
    ira = extract_ira()
    with open(os.path.join(BUILD_DIR, "content_ira.json"), "w") as f:
        json.dump(ira, f, ensure_ascii=False, indent=1)
    print("ira sections:", len(ira["sections"]),
          "total blocks:", sum(len(s["items"]) for s in ira["sections"]))

    for mn in list(sys.modules):
        if mn in ("fiche_ecbu", "style", "annexe_specialites", "fiche_anticoagulants", "fiche_choc_hemorragique", "fiche_intubation_urgence", "fiche_sepsis", "fiche_urgences_obstetricales", "fiche_anaphylaxie", "fiche_preeclampsie", "fiche_hyperthermie_maligne", "fiche_anticoag_urgence", "fiche_traumatisme_abdominal", "fiche_sedation_reanimation", "fiche_sedation_urgences", "fiche_vni", "fiche_aap_urgence", "fiche_curares", "fiche_remplissage", "fiche_traumatisme_membre", "fiche_voies_aeriennes_enfant", "fiche_intubation_difficile_adulte", "fiche_traumatisme_pelvien", "fiche_traumatisme_thoracique", "fiche_traumatisme_cranien", "fiche_traumatisme_vertebromedullaire", "fiche_intubation_reanimation", "fiche_traumatisme_cranien_leger", "fiche_lat_soins_critiques", "fiche_sdra", "fiche_pavm", "fiche_tracheotomie", "fiche_nutrition", "fiche_eer", "fiche_ira"):
            del sys.modules[mn]
    ih = extract_ih()
    with open(os.path.join(BUILD_DIR, "content_ih.json"), "w") as f:
        json.dump(ih, f, ensure_ascii=False, indent=1)
    print("ih sections:", len(ih["sections"]),
          "total blocks:", sum(len(s["items"]) for s in ih["sections"]))

    for mn in list(sys.modules):
        if mn in ("fiche_ecbu", "style", "annexe_specialites", "fiche_anticoagulants", "fiche_choc_hemorragique", "fiche_intubation_urgence", "fiche_sepsis", "fiche_urgences_obstetricales", "fiche_anaphylaxie", "fiche_preeclampsie", "fiche_hyperthermie_maligne", "fiche_anticoag_urgence", "fiche_traumatisme_abdominal", "fiche_sedation_reanimation", "fiche_sedation_urgences", "fiche_vni", "fiche_aap_urgence", "fiche_curares", "fiche_remplissage", "fiche_traumatisme_membre", "fiche_voies_aeriennes_enfant", "fiche_intubation_difficile_adulte", "fiche_traumatisme_pelvien", "fiche_traumatisme_thoracique", "fiche_traumatisme_cranien", "fiche_traumatisme_vertebromedullaire", "fiche_intubation_reanimation", "fiche_traumatisme_cranien_leger", "fiche_lat_soins_critiques", "fiche_sdra", "fiche_pavm", "fiche_tracheotomie", "fiche_nutrition", "fiche_eer", "fiche_ira", "fiche_ih"):
            del sys.modules[mn]
    epanchement_pleural = extract_epanchement_pleural()
    with open(os.path.join(BUILD_DIR, "content_epanchement_pleural.json"), "w") as f:
        json.dump(epanchement_pleural, f, ensure_ascii=False, indent=1)
    print("epanchement_pleural sections:", len(epanchement_pleural["sections"]),
          "total blocks:", sum(len(s["items"]) for s in epanchement_pleural["sections"]))

    for mn in list(sys.modules):
        if mn in ("fiche_ecbu", "style", "annexe_specialites", "fiche_anticoagulants", "fiche_choc_hemorragique", "fiche_intubation_urgence", "fiche_sepsis", "fiche_urgences_obstetricales", "fiche_anaphylaxie", "fiche_preeclampsie", "fiche_hyperthermie_maligne", "fiche_anticoag_urgence", "fiche_traumatisme_abdominal", "fiche_sedation_reanimation", "fiche_sedation_urgences", "fiche_vni", "fiche_aap_urgence", "fiche_curares", "fiche_remplissage", "fiche_traumatisme_membre", "fiche_voies_aeriennes_enfant", "fiche_intubation_difficile_adulte", "fiche_traumatisme_pelvien", "fiche_traumatisme_thoracique", "fiche_traumatisme_cranien", "fiche_traumatisme_vertebromedullaire", "fiche_intubation_reanimation", "fiche_traumatisme_cranien_leger", "fiche_lat_soins_critiques", "fiche_sdra", "fiche_pavm", "fiche_tracheotomie", "fiche_nutrition", "fiche_eer", "fiche_ira", "fiche_ih", "fiche_epanchement_pleural"):
            del sys.modules[mn]
    anemie = extract_anemie()
    with open(os.path.join(BUILD_DIR, "content_anemie.json"), "w") as f:
        json.dump(anemie, f, ensure_ascii=False, indent=1)
    print("anemie sections:", len(anemie["sections"]),
          "total blocks:", sum(len(s["items"]) for s in anemie["sections"]))

    for mn in list(sys.modules):
        if mn in ("fiche_ecbu", "style", "annexe_specialites", "fiche_anticoagulants", "fiche_choc_hemorragique", "fiche_intubation_urgence", "fiche_sepsis", "fiche_urgences_obstetricales", "fiche_anaphylaxie", "fiche_preeclampsie", "fiche_hyperthermie_maligne", "fiche_anticoag_urgence", "fiche_traumatisme_abdominal", "fiche_sedation_reanimation", "fiche_sedation_urgences", "fiche_vni", "fiche_aap_urgence", "fiche_curares", "fiche_remplissage", "fiche_traumatisme_membre", "fiche_voies_aeriennes_enfant", "fiche_intubation_difficile_adulte", "fiche_traumatisme_pelvien", "fiche_traumatisme_thoracique", "fiche_traumatisme_cranien", "fiche_traumatisme_vertebromedullaire", "fiche_intubation_reanimation", "fiche_traumatisme_cranien_leger", "fiche_lat_soins_critiques", "fiche_sdra", "fiche_pavm", "fiche_tracheotomie", "fiche_nutrition", "fiche_eer", "fiche_ira", "fiche_ih", "fiche_epanchement_pleural", "fiche_anemie"):
            del sys.modules[mn]
    hypothermie = extract_hypothermie()
    with open(os.path.join(BUILD_DIR, "content_hypothermie.json"), "w") as f:
        json.dump(hypothermie, f, ensure_ascii=False, indent=1)
    print("hypothermie sections:", len(hypothermie["sections"]),
          "total blocks:", sum(len(s["items"]) for s in hypothermie["sections"]))

    for mn in list(sys.modules):
        if mn in ("fiche_ecbu", "style", "annexe_specialites", "fiche_anticoagulants", "fiche_choc_hemorragique", "fiche_intubation_urgence", "fiche_sepsis", "fiche_urgences_obstetricales", "fiche_anaphylaxie", "fiche_preeclampsie", "fiche_hyperthermie_maligne", "fiche_anticoag_urgence", "fiche_traumatisme_abdominal", "fiche_sedation_reanimation", "fiche_sedation_urgences", "fiche_vni", "fiche_aap_urgence", "fiche_curares", "fiche_remplissage", "fiche_traumatisme_membre", "fiche_voies_aeriennes_enfant", "fiche_intubation_difficile_adulte", "fiche_traumatisme_pelvien", "fiche_traumatisme_thoracique", "fiche_traumatisme_cranien", "fiche_traumatisme_vertebromedullaire", "fiche_intubation_reanimation", "fiche_traumatisme_cranien_leger", "fiche_lat_soins_critiques", "fiche_sdra", "fiche_pavm", "fiche_tracheotomie", "fiche_nutrition", "fiche_eer", "fiche_ira", "fiche_ih", "fiche_epanchement_pleural", "fiche_anemie", "fiche_hypothermie"):
            del sys.modules[mn]
    nvpo = extract_nvpo()
    with open(os.path.join(BUILD_DIR, "content_nvpo.json"), "w") as f:
        json.dump(nvpo, f, ensure_ascii=False, indent=1)
    print("nvpo sections:", len(nvpo["sections"]),
          "total blocks:", sum(len(s["items"]) for s in nvpo["sections"]))

    for mn in list(sys.modules):
        if mn in ("fiche_ecbu", "style", "annexe_specialites", "fiche_anticoagulants", "fiche_choc_hemorragique", "fiche_intubation_urgence", "fiche_sepsis", "fiche_urgences_obstetricales", "fiche_anaphylaxie", "fiche_preeclampsie", "fiche_hyperthermie_maligne", "fiche_anticoag_urgence", "fiche_traumatisme_abdominal", "fiche_sedation_reanimation", "fiche_sedation_urgences", "fiche_vni", "fiche_aap_urgence", "fiche_curares", "fiche_remplissage", "fiche_traumatisme_membre", "fiche_voies_aeriennes_enfant", "fiche_intubation_difficile_adulte", "fiche_traumatisme_pelvien", "fiche_traumatisme_thoracique", "fiche_traumatisme_cranien", "fiche_traumatisme_vertebromedullaire", "fiche_intubation_reanimation", "fiche_traumatisme_cranien_leger", "fiche_lat_soins_critiques", "fiche_sdra", "fiche_pavm", "fiche_tracheotomie", "fiche_nutrition", "fiche_eer", "fiche_ira", "fiche_ih", "fiche_epanchement_pleural", "fiche_anemie", "fiche_hypothermie", "fiche_nvpo"):
            del sys.modules[mn]
    aap_programmee = extract_aap_programmee()
    with open(os.path.join(BUILD_DIR, "content_aap_programmee.json"), "w") as f:
        json.dump(aap_programmee, f, ensure_ascii=False, indent=1)
    print("aap_programmee sections:", len(aap_programmee["sections"]),
          "total blocks:", sum(len(s["items"]) for s in aap_programmee["sections"]))

    for mn in list(sys.modules):
        if mn in ("fiche_ecbu", "style", "annexe_specialites", "fiche_anticoagulants", "fiche_choc_hemorragique", "fiche_intubation_urgence", "fiche_sepsis", "fiche_urgences_obstetricales", "fiche_anaphylaxie", "fiche_preeclampsie", "fiche_hyperthermie_maligne", "fiche_anticoag_urgence", "fiche_traumatisme_abdominal", "fiche_sedation_reanimation", "fiche_sedation_urgences", "fiche_vni", "fiche_aap_urgence", "fiche_curares", "fiche_remplissage", "fiche_traumatisme_membre", "fiche_voies_aeriennes_enfant", "fiche_intubation_difficile_adulte", "fiche_traumatisme_pelvien", "fiche_traumatisme_thoracique", "fiche_traumatisme_cranien", "fiche_traumatisme_vertebromedullaire", "fiche_intubation_reanimation", "fiche_traumatisme_cranien_leger", "fiche_lat_soins_critiques", "fiche_sdra", "fiche_pavm", "fiche_tracheotomie", "fiche_nutrition", "fiche_eer", "fiche_ira", "fiche_ih", "fiche_epanchement_pleural", "fiche_anemie", "fiche_hypothermie", "fiche_nvpo", "fiche_aap_programmee"):
            del sys.modules[mn]
    mtev_perioperatoire = extract_mtev_perioperatoire()
    with open(os.path.join(BUILD_DIR, "content_mtev_perioperatoire.json"), "w") as f:
        json.dump(mtev_perioperatoire, f, ensure_ascii=False, indent=1)
    print("mtev_perioperatoire sections:", len(mtev_perioperatoire["sections"]),
          "total blocks:", sum(len(s["items"]) for s in mtev_perioperatoire["sections"]))

    for mn in list(sys.modules):
        if mn in ("fiche_ecbu", "style", "annexe_specialites", "fiche_anticoagulants", "fiche_choc_hemorragique", "fiche_intubation_urgence", "fiche_sepsis", "fiche_urgences_obstetricales", "fiche_anaphylaxie", "fiche_preeclampsie", "fiche_hyperthermie_maligne", "fiche_anticoag_urgence", "fiche_traumatisme_abdominal", "fiche_sedation_reanimation", "fiche_sedation_urgences", "fiche_vni", "fiche_aap_urgence", "fiche_curares", "fiche_remplissage", "fiche_traumatisme_membre", "fiche_voies_aeriennes_enfant", "fiche_intubation_difficile_adulte", "fiche_traumatisme_pelvien", "fiche_traumatisme_thoracique", "fiche_traumatisme_cranien", "fiche_traumatisme_vertebromedullaire", "fiche_intubation_reanimation", "fiche_traumatisme_cranien_leger", "fiche_lat_soins_critiques", "fiche_sdra", "fiche_pavm", "fiche_tracheotomie", "fiche_nutrition", "fiche_eer", "fiche_ira", "fiche_ih", "fiche_epanchement_pleural", "fiche_anemie", "fiche_hypothermie", "fiche_nvpo", "fiche_aap_programmee", "fiche_mtev_perioperatoire"):
            del sys.modules[mn]
    glycemie = extract_glycemie()
    with open(os.path.join(BUILD_DIR, "content_glycemie.json"), "w") as f:
        json.dump(glycemie, f, ensure_ascii=False, indent=1)
    print("glycemie sections:", len(glycemie["sections"]),
          "total blocks:", sum(len(s["items"]) for s in glycemie["sections"]))

    for mn in list(sys.modules):
        if mn in ("fiche_ecbu", "style", "annexe_specialites", "fiche_anticoagulants", "fiche_choc_hemorragique", "fiche_intubation_urgence", "fiche_sepsis", "fiche_urgences_obstetricales", "fiche_anaphylaxie", "fiche_preeclampsie", "fiche_hyperthermie_maligne", "fiche_anticoag_urgence", "fiche_traumatisme_abdominal", "fiche_sedation_reanimation", "fiche_sedation_urgences", "fiche_vni", "fiche_aap_urgence", "fiche_curares", "fiche_remplissage", "fiche_traumatisme_membre", "fiche_voies_aeriennes_enfant", "fiche_intubation_difficile_adulte", "fiche_traumatisme_pelvien", "fiche_traumatisme_thoracique", "fiche_traumatisme_cranien", "fiche_traumatisme_vertebromedullaire", "fiche_intubation_reanimation", "fiche_traumatisme_cranien_leger", "fiche_lat_soins_critiques", "fiche_sdra", "fiche_pavm", "fiche_tracheotomie", "fiche_nutrition", "fiche_eer", "fiche_ira", "fiche_ih", "fiche_epanchement_pleural", "fiche_anemie", "fiche_hypothermie", "fiche_nvpo", "fiche_aap_programmee", "fiche_mtev_perioperatoire", "fiche_glycemie"):
            del sys.modules[mn]
    mal_epileptique = extract_mal_epileptique()
    with open(os.path.join(BUILD_DIR, "content_mal_epileptique.json"), "w") as f:
        json.dump(mal_epileptique, f, ensure_ascii=False, indent=1)
    print("mal_epileptique sections:", len(mal_epileptique["sections"]),
          "total blocks:", sum(len(s["items"]) for s in mal_epileptique["sections"]))

    for mn in list(sys.modules):
        if mn in ("fiche_ecbu", "style", "annexe_specialites", "fiche_anticoagulants", "fiche_choc_hemorragique", "fiche_intubation_urgence", "fiche_sepsis", "fiche_urgences_obstetricales", "fiche_anaphylaxie", "fiche_preeclampsie", "fiche_hyperthermie_maligne", "fiche_anticoag_urgence", "fiche_traumatisme_abdominal", "fiche_sedation_reanimation", "fiche_sedation_urgences", "fiche_vni", "fiche_aap_urgence", "fiche_curares", "fiche_remplissage", "fiche_traumatisme_membre", "fiche_voies_aeriennes_enfant", "fiche_intubation_difficile_adulte", "fiche_traumatisme_pelvien", "fiche_traumatisme_thoracique", "fiche_traumatisme_cranien", "fiche_traumatisme_vertebromedullaire", "fiche_intubation_reanimation", "fiche_traumatisme_cranien_leger", "fiche_lat_soins_critiques", "fiche_sdra", "fiche_pavm", "fiche_tracheotomie", "fiche_nutrition", "fiche_eer", "fiche_ira", "fiche_ih", "fiche_epanchement_pleural", "fiche_anemie", "fiche_hypothermie", "fiche_nvpo", "fiche_aap_programmee", "fiche_mtev_perioperatoire", "fiche_glycemie", "fiche_mal_epileptique"):
            del sys.modules[mn]
    allergie_prevention = extract_allergie_prevention()
    with open(os.path.join(BUILD_DIR, "content_allergie_prevention.json"), "w") as f:
        json.dump(allergie_prevention, f, ensure_ascii=False, indent=1)
    print("allergie_prevention sections:", len(allergie_prevention["sections"]),
          "total blocks:", sum(len(s["items"]) for s in allergie_prevention["sections"]))

    for mn in list(sys.modules):
        if mn in ("fiche_ecbu", "style", "annexe_specialites", "fiche_anticoagulants", "fiche_choc_hemorragique", "fiche_intubation_urgence", "fiche_sepsis", "fiche_urgences_obstetricales", "fiche_anaphylaxie", "fiche_preeclampsie", "fiche_hyperthermie_maligne", "fiche_anticoag_urgence", "fiche_traumatisme_abdominal", "fiche_sedation_reanimation", "fiche_sedation_urgences", "fiche_vni", "fiche_aap_urgence", "fiche_curares", "fiche_remplissage", "fiche_traumatisme_membre", "fiche_voies_aeriennes_enfant", "fiche_intubation_difficile_adulte", "fiche_traumatisme_pelvien", "fiche_traumatisme_thoracique", "fiche_traumatisme_cranien", "fiche_traumatisme_vertebromedullaire", "fiche_intubation_reanimation", "fiche_traumatisme_cranien_leger", "fiche_lat_soins_critiques", "fiche_sdra", "fiche_pavm", "fiche_tracheotomie", "fiche_nutrition", "fiche_eer", "fiche_ira", "fiche_ih", "fiche_epanchement_pleural", "fiche_anemie", "fiche_hypothermie", "fiche_nvpo", "fiche_aap_programmee", "fiche_mtev_perioperatoire", "fiche_glycemie", "fiche_mal_epileptique", "fiche_allergie_prevention"):
            del sys.modules[mn]
    antibioprophylaxie = extract_antibioprophylaxie()
    with open(os.path.join(BUILD_DIR, "content_antibioprophylaxie.json"), "w") as f:
        json.dump(antibioprophylaxie, f, ensure_ascii=False, indent=1)
    print("antibioprophylaxie sections:", len(antibioprophylaxie["sections"]),
          "total blocks:", sum(len(s["items"]) for s in antibioprophylaxie["sections"]))

    for mn in list(sys.modules):
        if mn in ("fiche_ecbu", "style", "annexe_specialites", "fiche_anticoagulants", "fiche_choc_hemorragique", "fiche_intubation_urgence", "fiche_sepsis", "fiche_urgences_obstetricales", "fiche_anaphylaxie", "fiche_preeclampsie", "fiche_hyperthermie_maligne", "fiche_anticoag_urgence", "fiche_traumatisme_abdominal", "fiche_sedation_reanimation", "fiche_sedation_urgences", "fiche_vni", "fiche_aap_urgence", "fiche_curares", "fiche_remplissage", "fiche_traumatisme_membre", "fiche_voies_aeriennes_enfant", "fiche_intubation_difficile_adulte", "fiche_traumatisme_pelvien", "fiche_traumatisme_thoracique", "fiche_traumatisme_cranien", "fiche_traumatisme_vertebromedullaire", "fiche_intubation_reanimation", "fiche_traumatisme_cranien_leger", "fiche_lat_soins_critiques", "fiche_sdra", "fiche_pavm", "fiche_tracheotomie", "fiche_nutrition", "fiche_eer", "fiche_ira", "fiche_ih", "fiche_epanchement_pleural", "fiche_anemie", "fiche_hypothermie", "fiche_nvpo", "fiche_aap_programmee", "fiche_mtev_perioperatoire", "fiche_glycemie", "fiche_mal_epileptique", "fiche_allergie_prevention", "fiche_antibioprophylaxie"):
            del sys.modules[mn]
    controle_temperature = extract_controle_temperature()
    with open(os.path.join(BUILD_DIR, "content_controle_temperature.json"), "w") as f:
        json.dump(controle_temperature, f, ensure_ascii=False, indent=1)
    print("controle_temperature sections:", len(controle_temperature["sections"]),
          "total blocks:", sum(len(s["items"]) for s in controle_temperature["sections"]))

    for mn in list(sys.modules):
        if mn in ("fiche_ecbu", "style", "annexe_specialites", "fiche_anticoagulants", "fiche_choc_hemorragique", "fiche_intubation_urgence", "fiche_sepsis", "fiche_urgences_obstetricales", "fiche_anaphylaxie", "fiche_preeclampsie", "fiche_hyperthermie_maligne", "fiche_anticoag_urgence", "fiche_traumatisme_abdominal", "fiche_sedation_reanimation", "fiche_sedation_urgences", "fiche_vni", "fiche_aap_urgence", "fiche_curares", "fiche_remplissage", "fiche_traumatisme_membre", "fiche_voies_aeriennes_enfant", "fiche_intubation_difficile_adulte", "fiche_traumatisme_pelvien", "fiche_traumatisme_thoracique", "fiche_traumatisme_cranien", "fiche_traumatisme_vertebromedullaire", "fiche_intubation_reanimation", "fiche_traumatisme_cranien_leger", "fiche_lat_soins_critiques", "fiche_sdra", "fiche_pavm", "fiche_tracheotomie", "fiche_nutrition", "fiche_eer", "fiche_ira", "fiche_ih", "fiche_epanchement_pleural", "fiche_anemie", "fiche_hypothermie", "fiche_nvpo", "fiche_aap_programmee", "fiche_mtev_perioperatoire", "fiche_glycemie", "fiche_mal_epileptique", "fiche_allergie_prevention", "fiche_antibioprophylaxie", "fiche_controle_temperature"):
            del sys.modules[mn]
    tih = extract_tih()
    with open(os.path.join(BUILD_DIR, "content_tih.json"), "w") as f:
        json.dump(tih, f, ensure_ascii=False, indent=1)
    print("tih sections:", len(tih["sections"]),
          "total blocks:", sum(len(s["items"]) for s in tih["sections"]))

    for mn in list(sys.modules):
        if mn in ("fiche_ecbu", "style", "annexe_specialites", "fiche_anticoagulants", "fiche_choc_hemorragique", "fiche_intubation_urgence", "fiche_sepsis", "fiche_urgences_obstetricales", "fiche_anaphylaxie", "fiche_preeclampsie", "fiche_hyperthermie_maligne", "fiche_anticoag_urgence", "fiche_traumatisme_abdominal", "fiche_sedation_reanimation", "fiche_sedation_urgences", "fiche_vni", "fiche_aap_urgence", "fiche_curares", "fiche_remplissage", "fiche_traumatisme_membre", "fiche_voies_aeriennes_enfant", "fiche_intubation_difficile_adulte", "fiche_traumatisme_pelvien", "fiche_traumatisme_thoracique", "fiche_traumatisme_cranien", "fiche_traumatisme_vertebromedullaire", "fiche_intubation_reanimation", "fiche_traumatisme_cranien_leger", "fiche_lat_soins_critiques", "fiche_sdra", "fiche_pavm", "fiche_tracheotomie", "fiche_nutrition", "fiche_eer", "fiche_ira", "fiche_ih", "fiche_epanchement_pleural", "fiche_anemie", "fiche_hypothermie", "fiche_nvpo", "fiche_aap_programmee", "fiche_mtev_perioperatoire", "fiche_glycemie", "fiche_mal_epileptique", "fiche_allergie_prevention", "fiche_antibioprophylaxie", "fiche_controle_temperature", "fiche_tih"):
            del sys.modules[mn]
    civd = extract_civd()
    with open(os.path.join(BUILD_DIR, "content_civd.json"), "w") as f:
        json.dump(civd, f, ensure_ascii=False, indent=1)
    print("civd sections:", len(civd["sections"]),
          "total blocks:", sum(len(s["items"]) for s in civd["sections"]))

    for mn in list(sys.modules):
        if mn in ("fiche_ecbu", "style", "annexe_specialites", "fiche_anticoagulants", "fiche_choc_hemorragique", "fiche_intubation_urgence", "fiche_sepsis", "fiche_urgences_obstetricales", "fiche_anaphylaxie", "fiche_preeclampsie", "fiche_hyperthermie_maligne", "fiche_anticoag_urgence", "fiche_traumatisme_abdominal", "fiche_sedation_reanimation", "fiche_sedation_urgences", "fiche_vni", "fiche_aap_urgence", "fiche_curares", "fiche_remplissage", "fiche_traumatisme_membre", "fiche_voies_aeriennes_enfant", "fiche_intubation_difficile_adulte", "fiche_traumatisme_pelvien", "fiche_traumatisme_thoracique", "fiche_traumatisme_cranien", "fiche_traumatisme_vertebromedullaire", "fiche_intubation_reanimation", "fiche_traumatisme_cranien_leger", "fiche_lat_soins_critiques", "fiche_sdra", "fiche_pavm", "fiche_tracheotomie", "fiche_nutrition", "fiche_eer", "fiche_ira", "fiche_ih", "fiche_epanchement_pleural", "fiche_anemie", "fiche_hypothermie", "fiche_nvpo", "fiche_aap_programmee", "fiche_mtev_perioperatoire", "fiche_glycemie", "fiche_mal_epileptique", "fiche_allergie_prevention", "fiche_antibioprophylaxie", "fiche_controle_temperature", "fiche_tih", "fiche_civd"):
            del sys.modules[mn]
    eclsa = extract_eclsa()
    with open(os.path.join(BUILD_DIR, "content_eclsa.json"), "w") as f:
        json.dump(eclsa, f, ensure_ascii=False, indent=1)
    print("eclsa sections:", len(eclsa["sections"]),
          "total blocks:", sum(len(s["items"]) for s in eclsa["sections"]))

    for mn in list(sys.modules):
        if mn in ("fiche_ecbu", "style", "annexe_specialites", "fiche_anticoagulants", "fiche_choc_hemorragique", "fiche_intubation_urgence", "fiche_sepsis", "fiche_urgences_obstetricales", "fiche_anaphylaxie", "fiche_preeclampsie", "fiche_hyperthermie_maligne", "fiche_anticoag_urgence", "fiche_traumatisme_abdominal", "fiche_sedation_reanimation", "fiche_sedation_urgences", "fiche_vni", "fiche_aap_urgence", "fiche_curares", "fiche_remplissage", "fiche_traumatisme_membre", "fiche_voies_aeriennes_enfant", "fiche_intubation_difficile_adulte", "fiche_traumatisme_pelvien", "fiche_traumatisme_thoracique", "fiche_traumatisme_cranien", "fiche_traumatisme_vertebromedullaire", "fiche_intubation_reanimation", "fiche_traumatisme_cranien_leger", "fiche_lat_soins_critiques", "fiche_sdra", "fiche_pavm", "fiche_tracheotomie", "fiche_nutrition", "fiche_eer", "fiche_ira", "fiche_ih", "fiche_epanchement_pleural", "fiche_anemie", "fiche_hypothermie", "fiche_nvpo", "fiche_aap_programmee", "fiche_mtev_perioperatoire", "fiche_glycemie", "fiche_mal_epileptique", "fiche_allergie_prevention", "fiche_antibioprophylaxie", "fiche_controle_temperature", "fiche_tih", "fiche_civd", "fiche_eclsa"):
            del sys.modules[mn]
    transport_ih = extract_transport_intrahospitalier()
    with open(os.path.join(BUILD_DIR, "content_transport_intrahospitalier.json"), "w") as f:
        json.dump(transport_ih, f, ensure_ascii=False, indent=1)
    print("transport_intrahospitalier sections:", len(transport_ih["sections"]),
          "total blocks:", sum(len(s["items"]) for s in transport_ih["sections"]))

    for mn in list(sys.modules):
        if mn in ("fiche_ecbu", "style", "annexe_specialites", "fiche_anticoagulants", "fiche_choc_hemorragique", "fiche_intubation_urgence", "fiche_sepsis", "fiche_urgences_obstetricales", "fiche_anaphylaxie", "fiche_preeclampsie", "fiche_hyperthermie_maligne", "fiche_anticoag_urgence", "fiche_traumatisme_abdominal", "fiche_sedation_reanimation", "fiche_sedation_urgences", "fiche_vni", "fiche_aap_urgence", "fiche_curares", "fiche_remplissage", "fiche_traumatisme_membre", "fiche_voies_aeriennes_enfant", "fiche_intubation_difficile_adulte", "fiche_traumatisme_pelvien", "fiche_traumatisme_thoracique", "fiche_traumatisme_cranien", "fiche_traumatisme_vertebromedullaire", "fiche_intubation_reanimation", "fiche_traumatisme_cranien_leger", "fiche_lat_soins_critiques", "fiche_sdra", "fiche_pavm", "fiche_tracheotomie", "fiche_nutrition", "fiche_eer", "fiche_ira", "fiche_ih", "fiche_epanchement_pleural", "fiche_anemie", "fiche_hypothermie", "fiche_nvpo", "fiche_aap_programmee", "fiche_mtev_perioperatoire", "fiche_glycemie", "fiche_mal_epileptique", "fiche_allergie_prevention", "fiche_antibioprophylaxie", "fiche_controle_temperature", "fiche_tih", "fiche_civd", "fiche_eclsa", "fiche_transport_intrahospitalier"):
            del sys.modules[mn]
    transfusion_plasma = extract_transfusion_plasma()
    with open(os.path.join(BUILD_DIR, "content_transfusion_plasma.json"), "w") as f:
        json.dump(transfusion_plasma, f, ensure_ascii=False, indent=1)
    print("transfusion_plasma sections:", len(transfusion_plasma["sections"]),
          "total blocks:", sum(len(s["items"]) for s in transfusion_plasma["sections"]))
