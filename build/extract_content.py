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

    def PatchedSectionBar(text, color=None, icon_fn=None, **kw):
        # **kw absorbs PDF-only layout kwargs (height, fontsize, ...) that some fiche
        # scripts pass to the real style.section_bar but that don't affect extracted content.
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


def extract_sevrage_vm():
    import style
    import fiche_sevrage_vm as m
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
    return {"doc": "sevrage_vm", "sections": blocks}


def extract_asthme_aigu_grave():
    import style
    import fiche_asthme_aigu_grave as m
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
    return {"doc": "asthme_aigu_grave", "sections": blocks}


def extract_pancreatite():
    import style
    import fiche_pancreatite as m
    trace = []
    make_module_patches(m, trace)
    make_module_patches(style, trace)

    blocks = []
    for title, fn, _break_flag in m.SECTIONS:
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
    return {"doc": "pancreatite", "sections": blocks}


def extract_corticotherapie():
    import style
    import fiche_corticotherapie as m
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
    return {"doc": "corticotherapie", "sections": blocks}


def extract_antibiotherapie_probabiliste():
    import style
    import fiche_antibiotherapie_probabiliste as m
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
    return {"doc": "antibiotherapie_probabiliste", "sections": blocks}


def extract_hsa():
    import style
    import fiche_hsa as m
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
    return {"doc": "hsa", "sections": blocks}


def extract_sepsis_hemodynamique():
    import style
    import fiche_sepsis_hemodynamique as m
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
    return {"doc": "sepsis_hemodynamique", "sections": blocks}


def extract_securisation_proc():
    import style
    import fiche_securisation_proc as m
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
    return {"doc": "securisation_proc", "sections": blocks}


def extract_mort_encephalique():
    import style
    import fiche_mort_encephalique as m
    trace = []
    make_module_patches(m, trace)
    make_module_patches(style, trace)

    blocks = []
    # SECTIONS here is (title, fn, new_page_bool) - a 3-tuple, unlike most other
    # fiches' 2-tuples, because this fiche uses the chapter-boundary-only
    # pagebreak pattern from CLAUDE.md's build pipeline step 7 - unpack accordingly.
    for title, fn, _new_page in m.SECTIONS:
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
    return {"doc": "mort_encephalique", "sections": blocks}


def extract_voies_aeriennes_adulte():
    import style
    import fiche_voies_aeriennes_adulte as m
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
    return {"doc": "voies_aeriennes_adulte", "sections": blocks}


def extract_urgences_transfusionnelles_obstetricales():
    import style
    import fiche_urgences_transfusionnelles_obstetricales as m
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
    return {"doc": "urgences_transfusionnelles_obstetricales", "sections": blocks}


def extract_sujet_age_esf():
    import style
    import fiche_sujet_age_esf as m
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
    return {"doc": "sujet_age_esf", "sections": blocks}


def extract_douleur_reactualisation_2016():
    import style
    import fiche_douleur_reactualisation_2016 as m
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
    return {"doc": "douleur_reactualisation_2016", "sections": blocks}


def extract_ponction_lombaire():
    import style
    import fiche_ponction_lombaire as m
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
    return {"doc": "ponction_lombaire", "sections": blocks}


def extract_amygdalectomie_enfant():
    import style
    import fiche_amygdalectomie_enfant as m
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
    return {"doc": "amygdalectomie_enfant", "sections": blocks}


def extract_erreurs_medicamenteuses():
    import style
    import fiche_erreurs_medicamenteuses as m
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
    return {"doc": "erreurs_medicamenteuses", "sections": blocks}


def extract_remplissage_perioperatoire():
    import style
    import fiche_remplissage_perioperatoire as m
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
    return {"doc": "remplissage_perioperatoire", "sections": blocks}


def extract_thrombectomie():
    import style
    import fiche_thrombectomie as m
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
    return {"doc": "thrombectomie", "sections": blocks}


def extract_insuffisance_analgesie_cesarienne():
    import style
    import fiche_insuffisance_analgesie_cesarienne as m
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
    return {"doc": "insuffisance_analgesie_cesarienne", "sections": blocks}


def extract_relations_anesth_chir():
    import style
    import fiche_relations_anesth_chir as m
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
    return {"doc": "relations_anesth_chir", "sections": blocks}


def extract_sauv():
    import style
    import fiche_sauv as m
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
    return {"doc": "sauv", "sections": blocks}


def extract_catheters_veineux_centraux():
    import style
    import fiche_catheters_veineux_centraux as m
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
    return {"doc": "catheters_veineux_centraux", "sections": blocks}


def extract_candidoses_aspergilloses():
    import style
    import fiche_candidoses_aspergilloses as m
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
    return {"doc": "candidoses_aspergilloses", "sections": blocks}


def extract_bris_dentaires():
    import style
    import fiche_bris_dentaires as m
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
    return {"doc": "bris_dentaires", "sections": blocks}


def extract_coronarien():
    import style
    import fiche_coronarien as m
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
    return {"doc": "coronarien", "sections": blocks}


def extract_brule_grave():
    import style
    import fiche_brule_grave as m
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
    return {"doc": "brule_grave", "sections": blocks}


def extract_tabagisme():
    import style
    import fiche_tabagisme as m
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
    return {"doc": "tabagisme", "sections": blocks}


def extract_infections_intra_abdominales():
    import style
    import fiche_infections_intra_abdominales as m
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
    return {"doc": "infections_intra_abdominales", "sections": blocks}


def extract_alr_perinerveuse():
    import style
    import fiche_alr_perinerveuse as m
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
    return {"doc": "alr_perinerveuse", "sections": blocks}


def extract_urgences_ob_extrahosp():
    import style
    import fiche_urgences_ob_extrahosp as m
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
    return {"doc": "urgences_ob_extrahosp", "sections": blocks}


def extract_aod_urgence():
    import style
    import fiche_aod_urgence as m
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
    return {"doc": "aod_urgence", "sections": blocks}


def extract_plyo_transfusion():
    import style
    import fiche_plyo_transfusion as m
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
    return {"doc": "plyo_transfusion", "sections": blocks}


def extract_tenue_vestimentaire():
    import style
    import fiche_tenue_vestimentaire as m
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
    return {"doc": "tenue_vestimentaire", "sections": blocks}


def extract_alr_non_specialiste():
    import style
    import fiche_alr_non_specialiste as m
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
    return {"doc": "alr_non_specialiste", "sections": blocks}


def extract_echo_acces_vasculaires():
    import style
    import fiche_echo_acces_vasculaires as m
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
    return {"doc": "echo_acces_vasculaires", "sections": blocks}


def extract_tests_viscoelastiques():
    import style
    import fiche_tests_viscoelastiques as m
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
    return {"doc": "tests_viscoelastiques", "sections": blocks}


def extract_eeg_cortical():
    import style
    import fiche_eeg_cortical as m
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
    return {"doc": "eeg_cortical", "sections": blocks}


def extract_examens_pertinence_rea():
    import style
    import fiche_examens_pertinence_rea as m
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
    return {"doc": "examens_pertinence_rea", "sections": blocks}


def extract_alr_pediatrie():
    import style
    import fiche_alr_pediatrie as m
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
    return {"doc": "alr_pediatrie", "sections": blocks}


def extract_hospit_ambulatoire():
    import style
    import fiche_hospit_ambulatoire as m
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
    return {"doc": "hospit_ambulatoire", "sections": blocks}


def extract_echo_alr():
    import style
    import fiche_echo_alr as m
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
    return {"doc": "echo_alr", "sections": blocks}


def extract_alr_douleur_chronique():
    import style
    import fiche_alr_douleur_chronique as m
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
    return {"doc": "alr_douleur_chronique", "sections": blocks}


def extract_infections_nosocomiales_rea():
    import style
    import fiche_infections_nosocomiales_rea as m
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
    return {"doc": "infections_nosocomiales_rea", "sections": blocks}


def extract_nutrition_perioperatoire():
    import style
    import fiche_nutrition_perioperatoire as m
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
    return {"doc": "nutrition_perioperatoire", "sections": blocks}


def extract_ivg_14sa():
    import style
    import fiche_ivg_14sa as m
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
    return {"doc": "ivg_14sa", "sections": blocks}


def extract_aod_programme():
    import style
    import fiche_aod_programme as m
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
    return {"doc": "aod_programme", "sections": blocks}


def extract_blocs_peripheriques_membres():
    import style
    import fiche_blocs_peripheriques_membres as m
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
    return {"doc": "blocs_peripheriques_membres", "sections": blocks}


def extract_raac_colorectal():
    import style
    import fiche_raac_colorectal as m
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
    return {"doc": "raac_colorectal", "sections": blocks}


def extract_chir_ambu_proctologie():
    import style
    import fiche_chir_ambu_proctologie as m
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
    return {"doc": "chir_ambu_proctologie", "sections": blocks}


def extract_mieux_vivre_reanimation():
    import style
    import fiche_mieux_vivre_reanimation as m
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
    return {"doc": "mieux_vivre_reanimation", "sections": blocks}


def extract_preparation_colique():
    import style
    import fiche_preparation_colique as m
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
    return {"doc": "preparation_colique", "sections": blocks}


def extract_organisation_ar_obstetricale():
    import style
    import fiche_organisation_ar_obstetricale as m
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
    return {"doc": "organisation_ar_obstetricale", "sections": blocks}


def extract_erreurs_medicamenteuses_ar_2016():
    import style
    import fiche_erreurs_medicamenteuses_ar_2016 as m
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
    return {"doc": "erreurs_medicamenteuses_ar_2016", "sections": blocks}


def extract_anesth_pediatrique_structures():
    import style
    import fiche_anesth_pediatrique_structures as m
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
    return {"doc": "anesth_pediatrique_structures", "sections": blocks}


def extract_aod_dabigatran_urgence_2016():
    import style
    import fiche_aod_dabigatran_urgence_2016 as m
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
    return {"doc": "aod_dabigatran_urgence_2016", "sections": blocks}


def extract_tc_readaptation():
    import style
    import fiche_tc_readaptation as m
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
    return {"doc": "tc_readaptation", "sections": blocks}


def extract_impact_environnemental_ag():
    import style
    import fiche_impact_environnemental_ag as m
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
    return {"doc": "impact_environnemental_ag", "sections": blocks}


def extract_diabete_perioperatoire_2025():
    import style
    import fiche_diabete_perioperatoire_2025 as m
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
    return {"doc": "diabete_perioperatoire_2025", "sections": blocks}


def extract_anesth_cardiopathie_congenitale():
    import style
    import fiche_anesth_cardiopathie_congenitale as m
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
    return {"doc": "anesth_cardiopathie_congenitale", "sections": blocks}


def extract_ressources_humaines_anesthesie_2024():
    import style
    import fiche_ressources_humaines_anesthesie_2024 as m
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
    return {"doc": "ressources_humaines_anesthesie_2024", "sections": blocks}


def extract_demarches_anticipees_don_organes_2024():
    import style
    import fiche_demarches_anticipees_don_organes_2024 as m
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
    return {"doc": "demarches_anticipees_don_organes_2024", "sections": blocks}


def extract_raac_orthopedique_2019():
    import style
    import fiche_raac_orthopedique_2019 as m
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
    return {"doc": "raac_orthopedique_2019", "sections": blocks}


def extract_reduction_antibiotiques_reanimation_2014():
    import style
    import fiche_reduction_antibiotiques_reanimation_2014 as m
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
    return {"doc": "reduction_antibiotiques_reanimation_2014", "sections": blocks}


def extract_simulation_soins_critiques_2019():
    import style
    import fiche_simulation_soins_critiques_2019 as m
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
    return {"doc": "simulation_soins_critiques_2019", "sections": blocks}


def extract_optimisation_beta_lactamines_2018():
    import style
    import fiche_optimisation_beta_lactamines_2018 as m
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
    return {"doc": "optimisation_beta_lactamines_2018", "sections": blocks}


def extract_raac_lobectomie_pulmonaire_2019():
    import style
    import fiche_raac_lobectomie_pulmonaire_2019 as m
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
    return {"doc": "raac_lobectomie_pulmonaire_2019", "sections": blocks}


def extract_raac_cardiaque_2021():
    import style
    import fiche_raac_cardiaque_2021 as m
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
    return {"doc": "raac_cardiaque_2021", "sections": blocks}


def extract_optimisation_hemodynamique_pediatrie_2024():
    import style
    import fiche_optimisation_hemodynamique_pediatrie_2024 as m
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
    return {"doc": "optimisation_hemodynamique_pediatrie_2024", "sections": blocks}


def extract_optimisation_hemodynamique_adulte_2024():
    import style
    import fiche_optimisation_hemodynamique_adulte_2024 as m
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
    return {"doc": "optimisation_hemodynamique_adulte_2024", "sections": blocks}


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

    for mn in list(sys.modules):
        if mn in ("fiche_ecbu", "style", "annexe_specialites", "fiche_anticoagulants", "fiche_choc_hemorragique", "fiche_intubation_urgence", "fiche_sepsis", "fiche_urgences_obstetricales", "fiche_anaphylaxie", "fiche_preeclampsie", "fiche_hyperthermie_maligne", "fiche_anticoag_urgence", "fiche_traumatisme_abdominal", "fiche_sedation_reanimation", "fiche_sedation_urgences", "fiche_vni", "fiche_aap_urgence", "fiche_curares", "fiche_remplissage", "fiche_traumatisme_membre", "fiche_voies_aeriennes_enfant", "fiche_intubation_difficile_adulte", "fiche_traumatisme_pelvien", "fiche_traumatisme_thoracique", "fiche_traumatisme_cranien", "fiche_traumatisme_vertebromedullaire", "fiche_intubation_reanimation", "fiche_traumatisme_cranien_leger", "fiche_lat_soins_critiques", "fiche_sdra", "fiche_pavm", "fiche_tracheotomie", "fiche_nutrition", "fiche_eer", "fiche_ira", "fiche_ih", "fiche_epanchement_pleural", "fiche_anemie", "fiche_hypothermie", "fiche_nvpo", "fiche_aap_programmee", "fiche_mtev_perioperatoire", "fiche_glycemie", "fiche_mal_epileptique", "fiche_allergie_prevention", "fiche_antibioprophylaxie", "fiche_controle_temperature", "fiche_tih", "fiche_civd", "fiche_eclsa", "fiche_transport_intrahospitalier", "fiche_transfusion_plasma"):
            del sys.modules[mn]
    sevrage_vm = extract_sevrage_vm()
    with open(os.path.join(BUILD_DIR, "content_sevrage_vm.json"), "w") as f:
        json.dump(sevrage_vm, f, ensure_ascii=False, indent=1)
    print("sevrage_vm sections:", len(sevrage_vm["sections"]),
          "total blocks:", sum(len(s["items"]) for s in sevrage_vm["sections"]))

    for mn in list(sys.modules):
        if mn in ("fiche_ecbu", "style", "annexe_specialites", "fiche_anticoagulants", "fiche_choc_hemorragique", "fiche_intubation_urgence", "fiche_sepsis", "fiche_urgences_obstetricales", "fiche_anaphylaxie", "fiche_preeclampsie", "fiche_hyperthermie_maligne", "fiche_anticoag_urgence", "fiche_traumatisme_abdominal", "fiche_sedation_reanimation", "fiche_sedation_urgences", "fiche_vni", "fiche_aap_urgence", "fiche_curares", "fiche_remplissage", "fiche_traumatisme_membre", "fiche_voies_aeriennes_enfant", "fiche_intubation_difficile_adulte", "fiche_traumatisme_pelvien", "fiche_traumatisme_thoracique", "fiche_traumatisme_cranien", "fiche_traumatisme_vertebromedullaire", "fiche_intubation_reanimation", "fiche_traumatisme_cranien_leger", "fiche_lat_soins_critiques", "fiche_sdra", "fiche_pavm", "fiche_tracheotomie", "fiche_nutrition", "fiche_eer", "fiche_ira", "fiche_ih", "fiche_epanchement_pleural", "fiche_anemie", "fiche_hypothermie", "fiche_nvpo", "fiche_aap_programmee", "fiche_mtev_perioperatoire", "fiche_glycemie", "fiche_mal_epileptique", "fiche_allergie_prevention", "fiche_antibioprophylaxie", "fiche_controle_temperature", "fiche_tih", "fiche_civd", "fiche_eclsa", "fiche_transport_intrahospitalier", "fiche_transfusion_plasma", "fiche_sevrage_vm"):
            del sys.modules[mn]
    asthme_aigu_grave = extract_asthme_aigu_grave()
    with open(os.path.join(BUILD_DIR, "content_asthme_aigu_grave.json"), "w") as f:
        json.dump(asthme_aigu_grave, f, ensure_ascii=False, indent=1)
    print("asthme_aigu_grave sections:", len(asthme_aigu_grave["sections"]),
          "total blocks:", sum(len(s["items"]) for s in asthme_aigu_grave["sections"]))

    for mn in list(sys.modules):
        if mn in ("fiche_ecbu", "style", "annexe_specialites", "fiche_anticoagulants", "fiche_choc_hemorragique", "fiche_intubation_urgence", "fiche_sepsis", "fiche_urgences_obstetricales", "fiche_anaphylaxie", "fiche_preeclampsie", "fiche_hyperthermie_maligne", "fiche_anticoag_urgence", "fiche_traumatisme_abdominal", "fiche_sedation_reanimation", "fiche_sedation_urgences", "fiche_vni", "fiche_aap_urgence", "fiche_curares", "fiche_remplissage", "fiche_traumatisme_membre", "fiche_voies_aeriennes_enfant", "fiche_intubation_difficile_adulte", "fiche_traumatisme_pelvien", "fiche_traumatisme_thoracique", "fiche_traumatisme_cranien", "fiche_traumatisme_vertebromedullaire", "fiche_intubation_reanimation", "fiche_traumatisme_cranien_leger", "fiche_lat_soins_critiques", "fiche_sdra", "fiche_pavm", "fiche_tracheotomie", "fiche_nutrition", "fiche_eer", "fiche_ira", "fiche_ih", "fiche_epanchement_pleural", "fiche_anemie", "fiche_hypothermie", "fiche_nvpo", "fiche_aap_programmee", "fiche_mtev_perioperatoire", "fiche_glycemie", "fiche_mal_epileptique", "fiche_allergie_prevention", "fiche_antibioprophylaxie", "fiche_controle_temperature", "fiche_tih", "fiche_civd", "fiche_eclsa", "fiche_transport_intrahospitalier", "fiche_transfusion_plasma", "fiche_sevrage_vm", "fiche_asthme_aigu_grave"):
            del sys.modules[mn]
    pancreatite = extract_pancreatite()
    with open(os.path.join(BUILD_DIR, "content_pancreatite.json"), "w") as f:
        json.dump(pancreatite, f, ensure_ascii=False, indent=1)
    print("pancreatite sections:", len(pancreatite["sections"]),
          "total blocks:", sum(len(s["items"]) for s in pancreatite["sections"]))

    for mn in list(sys.modules):
        if mn in ("fiche_ecbu", "style", "annexe_specialites", "fiche_anticoagulants", "fiche_choc_hemorragique", "fiche_intubation_urgence", "fiche_sepsis", "fiche_urgences_obstetricales", "fiche_anaphylaxie", "fiche_preeclampsie", "fiche_hyperthermie_maligne", "fiche_anticoag_urgence", "fiche_traumatisme_abdominal", "fiche_sedation_reanimation", "fiche_sedation_urgences", "fiche_vni", "fiche_aap_urgence", "fiche_curares", "fiche_remplissage", "fiche_traumatisme_membre", "fiche_voies_aeriennes_enfant", "fiche_intubation_difficile_adulte", "fiche_traumatisme_pelvien", "fiche_traumatisme_thoracique", "fiche_traumatisme_cranien", "fiche_traumatisme_vertebromedullaire", "fiche_intubation_reanimation", "fiche_traumatisme_cranien_leger", "fiche_lat_soins_critiques", "fiche_sdra", "fiche_pavm", "fiche_tracheotomie", "fiche_nutrition", "fiche_eer", "fiche_ira", "fiche_ih", "fiche_epanchement_pleural", "fiche_anemie", "fiche_hypothermie", "fiche_nvpo", "fiche_aap_programmee", "fiche_mtev_perioperatoire", "fiche_glycemie", "fiche_mal_epileptique", "fiche_allergie_prevention", "fiche_antibioprophylaxie", "fiche_controle_temperature", "fiche_tih", "fiche_civd", "fiche_eclsa", "fiche_transport_intrahospitalier", "fiche_transfusion_plasma", "fiche_sevrage_vm", "fiche_asthme_aigu_grave", "fiche_pancreatite"):
            del sys.modules[mn]
    corticotherapie = extract_corticotherapie()
    with open(os.path.join(BUILD_DIR, "content_corticotherapie.json"), "w") as f:
        json.dump(corticotherapie, f, ensure_ascii=False, indent=1)
    print("corticotherapie sections:", len(corticotherapie["sections"]),
          "total blocks:", sum(len(s["items"]) for s in corticotherapie["sections"]))

    for mn in list(sys.modules):
        if mn in ("fiche_ecbu", "style", "annexe_specialites", "fiche_anticoagulants", "fiche_choc_hemorragique", "fiche_intubation_urgence", "fiche_sepsis", "fiche_urgences_obstetricales", "fiche_anaphylaxie", "fiche_preeclampsie", "fiche_hyperthermie_maligne", "fiche_anticoag_urgence", "fiche_traumatisme_abdominal", "fiche_sedation_reanimation", "fiche_sedation_urgences", "fiche_vni", "fiche_aap_urgence", "fiche_curares", "fiche_remplissage", "fiche_traumatisme_membre", "fiche_voies_aeriennes_enfant", "fiche_intubation_difficile_adulte", "fiche_traumatisme_pelvien", "fiche_traumatisme_thoracique", "fiche_traumatisme_cranien", "fiche_traumatisme_vertebromedullaire", "fiche_intubation_reanimation", "fiche_traumatisme_cranien_leger", "fiche_lat_soins_critiques", "fiche_sdra", "fiche_pavm", "fiche_tracheotomie", "fiche_nutrition", "fiche_eer", "fiche_ira", "fiche_ih", "fiche_epanchement_pleural", "fiche_anemie", "fiche_hypothermie", "fiche_nvpo", "fiche_aap_programmee", "fiche_mtev_perioperatoire", "fiche_glycemie", "fiche_mal_epileptique", "fiche_allergie_prevention", "fiche_antibioprophylaxie", "fiche_controle_temperature", "fiche_tih", "fiche_civd", "fiche_eclsa", "fiche_transport_intrahospitalier", "fiche_transfusion_plasma", "fiche_sevrage_vm", "fiche_asthme_aigu_grave", "fiche_pancreatite", "fiche_corticotherapie"):
            del sys.modules[mn]
    antibiotherapie_probabiliste = extract_antibiotherapie_probabiliste()
    with open(os.path.join(BUILD_DIR, "content_antibiotherapie_probabiliste.json"), "w") as f:
        json.dump(antibiotherapie_probabiliste, f, ensure_ascii=False, indent=1)
    print("antibiotherapie_probabiliste sections:", len(antibiotherapie_probabiliste["sections"]),
          "total blocks:", sum(len(s["items"]) for s in antibiotherapie_probabiliste["sections"]))

    for mn in list(sys.modules):
        if mn in ("fiche_ecbu", "style", "annexe_specialites", "fiche_anticoagulants", "fiche_choc_hemorragique", "fiche_intubation_urgence", "fiche_sepsis", "fiche_urgences_obstetricales", "fiche_anaphylaxie", "fiche_preeclampsie", "fiche_hyperthermie_maligne", "fiche_anticoag_urgence", "fiche_traumatisme_abdominal", "fiche_sedation_reanimation", "fiche_sedation_urgences", "fiche_vni", "fiche_aap_urgence", "fiche_curares", "fiche_remplissage", "fiche_traumatisme_membre", "fiche_voies_aeriennes_enfant", "fiche_intubation_difficile_adulte", "fiche_traumatisme_pelvien", "fiche_traumatisme_thoracique", "fiche_traumatisme_cranien", "fiche_traumatisme_vertebromedullaire", "fiche_intubation_reanimation", "fiche_traumatisme_cranien_leger", "fiche_lat_soins_critiques", "fiche_sdra", "fiche_pavm", "fiche_tracheotomie", "fiche_nutrition", "fiche_eer", "fiche_ira", "fiche_ih", "fiche_epanchement_pleural", "fiche_anemie", "fiche_hypothermie", "fiche_nvpo", "fiche_aap_programmee", "fiche_mtev_perioperatoire", "fiche_glycemie", "fiche_mal_epileptique", "fiche_allergie_prevention", "fiche_antibioprophylaxie", "fiche_controle_temperature", "fiche_tih", "fiche_civd", "fiche_eclsa", "fiche_transport_intrahospitalier", "fiche_transfusion_plasma", "fiche_sevrage_vm", "fiche_asthme_aigu_grave", "fiche_pancreatite", "fiche_corticotherapie", "fiche_antibiotherapie_probabiliste"):
            del sys.modules[mn]
    hsa = extract_hsa()
    with open(os.path.join(BUILD_DIR, "content_hsa.json"), "w") as f:
        json.dump(hsa, f, ensure_ascii=False, indent=1)
    print("hsa sections:", len(hsa["sections"]),
          "total blocks:", sum(len(s["items"]) for s in hsa["sections"]))

    for mn in list(sys.modules):
        if mn in ("fiche_ecbu", "style", "annexe_specialites", "fiche_anticoagulants", "fiche_choc_hemorragique", "fiche_intubation_urgence", "fiche_sepsis", "fiche_urgences_obstetricales", "fiche_anaphylaxie", "fiche_preeclampsie", "fiche_hyperthermie_maligne", "fiche_anticoag_urgence", "fiche_traumatisme_abdominal", "fiche_sedation_reanimation", "fiche_sedation_urgences", "fiche_vni", "fiche_aap_urgence", "fiche_curares", "fiche_remplissage", "fiche_traumatisme_membre", "fiche_voies_aeriennes_enfant", "fiche_intubation_difficile_adulte", "fiche_traumatisme_pelvien", "fiche_traumatisme_thoracique", "fiche_traumatisme_cranien", "fiche_traumatisme_vertebromedullaire", "fiche_intubation_reanimation", "fiche_traumatisme_cranien_leger", "fiche_lat_soins_critiques", "fiche_sdra", "fiche_pavm", "fiche_tracheotomie", "fiche_nutrition", "fiche_eer", "fiche_ira", "fiche_ih", "fiche_epanchement_pleural", "fiche_anemie", "fiche_hypothermie", "fiche_nvpo", "fiche_aap_programmee", "fiche_mtev_perioperatoire", "fiche_glycemie", "fiche_mal_epileptique", "fiche_allergie_prevention", "fiche_antibioprophylaxie", "fiche_controle_temperature", "fiche_tih", "fiche_civd", "fiche_eclsa", "fiche_transport_intrahospitalier", "fiche_transfusion_plasma", "fiche_sevrage_vm", "fiche_asthme_aigu_grave", "fiche_pancreatite", "fiche_corticotherapie", "fiche_antibiotherapie_probabiliste", "fiche_hsa"):
            del sys.modules[mn]
    sepsis_hemodynamique = extract_sepsis_hemodynamique()
    with open(os.path.join(BUILD_DIR, "content_sepsis_hemodynamique.json"), "w") as f:
        json.dump(sepsis_hemodynamique, f, ensure_ascii=False, indent=1)
    print("sepsis_hemodynamique sections:", len(sepsis_hemodynamique["sections"]),
          "total blocks:", sum(len(s["items"]) for s in sepsis_hemodynamique["sections"]))

    for mn in list(sys.modules):
        if mn in ("fiche_ecbu", "style", "annexe_specialites", "fiche_anticoagulants", "fiche_choc_hemorragique", "fiche_intubation_urgence", "fiche_sepsis", "fiche_urgences_obstetricales", "fiche_anaphylaxie", "fiche_preeclampsie", "fiche_hyperthermie_maligne", "fiche_anticoag_urgence", "fiche_traumatisme_abdominal", "fiche_sedation_reanimation", "fiche_sedation_urgences", "fiche_vni", "fiche_aap_urgence", "fiche_curares", "fiche_remplissage", "fiche_traumatisme_membre", "fiche_voies_aeriennes_enfant", "fiche_intubation_difficile_adulte", "fiche_traumatisme_pelvien", "fiche_traumatisme_thoracique", "fiche_traumatisme_cranien", "fiche_traumatisme_vertebromedullaire", "fiche_intubation_reanimation", "fiche_traumatisme_cranien_leger", "fiche_lat_soins_critiques", "fiche_sdra", "fiche_pavm", "fiche_tracheotomie", "fiche_nutrition", "fiche_eer", "fiche_ira", "fiche_ih", "fiche_epanchement_pleural", "fiche_anemie", "fiche_hypothermie", "fiche_nvpo", "fiche_aap_programmee", "fiche_mtev_perioperatoire", "fiche_glycemie", "fiche_mal_epileptique", "fiche_allergie_prevention", "fiche_antibioprophylaxie", "fiche_controle_temperature", "fiche_tih", "fiche_civd", "fiche_eclsa", "fiche_transport_intrahospitalier", "fiche_transfusion_plasma", "fiche_sevrage_vm", "fiche_asthme_aigu_grave", "fiche_pancreatite", "fiche_corticotherapie", "fiche_antibiotherapie_probabiliste", "fiche_hsa", "fiche_sepsis_hemodynamique"):
            del sys.modules[mn]
    securisation_proc = extract_securisation_proc()
    with open(os.path.join(BUILD_DIR, "content_securisation_proc.json"), "w") as f:
        json.dump(securisation_proc, f, ensure_ascii=False, indent=1)
    print("securisation_proc sections:", len(securisation_proc["sections"]),
          "total blocks:", sum(len(s["items"]) for s in securisation_proc["sections"]))

    for mn in list(sys.modules):
        if mn in ("fiche_ecbu", "style", "annexe_specialites", "fiche_anticoagulants", "fiche_choc_hemorragique", "fiche_intubation_urgence", "fiche_sepsis", "fiche_urgences_obstetricales", "fiche_anaphylaxie", "fiche_preeclampsie", "fiche_hyperthermie_maligne", "fiche_anticoag_urgence", "fiche_traumatisme_abdominal", "fiche_sedation_reanimation", "fiche_sedation_urgences", "fiche_vni", "fiche_aap_urgence", "fiche_curares", "fiche_remplissage", "fiche_traumatisme_membre", "fiche_voies_aeriennes_enfant", "fiche_intubation_difficile_adulte", "fiche_traumatisme_pelvien", "fiche_traumatisme_thoracique", "fiche_traumatisme_cranien", "fiche_traumatisme_vertebromedullaire", "fiche_intubation_reanimation", "fiche_traumatisme_cranien_leger", "fiche_lat_soins_critiques", "fiche_sdra", "fiche_pavm", "fiche_tracheotomie", "fiche_nutrition", "fiche_eer", "fiche_ira", "fiche_ih", "fiche_epanchement_pleural", "fiche_anemie", "fiche_hypothermie", "fiche_nvpo", "fiche_aap_programmee", "fiche_mtev_perioperatoire", "fiche_glycemie", "fiche_mal_epileptique", "fiche_allergie_prevention", "fiche_antibioprophylaxie", "fiche_controle_temperature", "fiche_tih", "fiche_civd", "fiche_eclsa", "fiche_transport_intrahospitalier", "fiche_transfusion_plasma", "fiche_sevrage_vm", "fiche_asthme_aigu_grave", "fiche_pancreatite", "fiche_corticotherapie", "fiche_antibiotherapie_probabiliste", "fiche_hsa", "fiche_sepsis_hemodynamique", "fiche_securisation_proc"):
            del sys.modules[mn]
    mort_encephalique = extract_mort_encephalique()
    with open(os.path.join(BUILD_DIR, "content_mort_encephalique.json"), "w") as f:
        json.dump(mort_encephalique, f, ensure_ascii=False, indent=1)
    print("mort_encephalique sections:", len(mort_encephalique["sections"]),
          "total blocks:", sum(len(s["items"]) for s in mort_encephalique["sections"]))

    for mn in list(sys.modules):
        if mn in ("fiche_ecbu", "style", "annexe_specialites", "fiche_anticoagulants", "fiche_choc_hemorragique", "fiche_intubation_urgence", "fiche_sepsis", "fiche_urgences_obstetricales", "fiche_anaphylaxie", "fiche_preeclampsie", "fiche_hyperthermie_maligne", "fiche_anticoag_urgence", "fiche_traumatisme_abdominal", "fiche_sedation_reanimation", "fiche_sedation_urgences", "fiche_vni", "fiche_aap_urgence", "fiche_curares", "fiche_remplissage", "fiche_traumatisme_membre", "fiche_voies_aeriennes_enfant", "fiche_intubation_difficile_adulte", "fiche_traumatisme_pelvien", "fiche_traumatisme_thoracique", "fiche_traumatisme_cranien", "fiche_traumatisme_vertebromedullaire", "fiche_intubation_reanimation", "fiche_traumatisme_cranien_leger", "fiche_lat_soins_critiques", "fiche_sdra", "fiche_pavm", "fiche_tracheotomie", "fiche_nutrition", "fiche_eer", "fiche_ira", "fiche_ih", "fiche_epanchement_pleural", "fiche_anemie", "fiche_hypothermie", "fiche_nvpo", "fiche_aap_programmee", "fiche_mtev_perioperatoire", "fiche_glycemie", "fiche_mal_epileptique", "fiche_allergie_prevention", "fiche_antibioprophylaxie", "fiche_controle_temperature", "fiche_tih", "fiche_civd", "fiche_eclsa", "fiche_transport_intrahospitalier", "fiche_transfusion_plasma", "fiche_sevrage_vm", "fiche_asthme_aigu_grave", "fiche_pancreatite", "fiche_corticotherapie", "fiche_antibiotherapie_probabiliste", "fiche_hsa", "fiche_sepsis_hemodynamique", "fiche_securisation_proc", "fiche_mort_encephalique"):
            del sys.modules[mn]
    voies_aeriennes_adulte = extract_voies_aeriennes_adulte()
    with open(os.path.join(BUILD_DIR, "content_voies_aeriennes_adulte.json"), "w") as f:
        json.dump(voies_aeriennes_adulte, f, ensure_ascii=False, indent=1)
    print("voies_aeriennes_adulte sections:", len(voies_aeriennes_adulte["sections"]),
          "total blocks:", sum(len(s["items"]) for s in voies_aeriennes_adulte["sections"]))

    for mn in list(sys.modules):
        if mn in ("fiche_ecbu", "style", "annexe_specialites", "fiche_anticoagulants", "fiche_choc_hemorragique", "fiche_intubation_urgence", "fiche_sepsis", "fiche_urgences_obstetricales", "fiche_anaphylaxie", "fiche_preeclampsie", "fiche_hyperthermie_maligne", "fiche_anticoag_urgence", "fiche_traumatisme_abdominal", "fiche_sedation_reanimation", "fiche_sedation_urgences", "fiche_vni", "fiche_aap_urgence", "fiche_curares", "fiche_remplissage", "fiche_traumatisme_membre", "fiche_voies_aeriennes_enfant", "fiche_intubation_difficile_adulte", "fiche_traumatisme_pelvien", "fiche_traumatisme_thoracique", "fiche_traumatisme_cranien", "fiche_traumatisme_vertebromedullaire", "fiche_intubation_reanimation", "fiche_traumatisme_cranien_leger", "fiche_lat_soins_critiques", "fiche_sdra", "fiche_pavm", "fiche_tracheotomie", "fiche_nutrition", "fiche_eer", "fiche_ira", "fiche_ih", "fiche_epanchement_pleural", "fiche_anemie", "fiche_hypothermie", "fiche_nvpo", "fiche_aap_programmee", "fiche_mtev_perioperatoire", "fiche_glycemie", "fiche_mal_epileptique", "fiche_allergie_prevention", "fiche_antibioprophylaxie", "fiche_controle_temperature", "fiche_tih", "fiche_civd", "fiche_eclsa", "fiche_transport_intrahospitalier", "fiche_transfusion_plasma", "fiche_sevrage_vm", "fiche_asthme_aigu_grave", "fiche_pancreatite", "fiche_corticotherapie", "fiche_antibiotherapie_probabiliste", "fiche_hsa", "fiche_sepsis_hemodynamique", "fiche_securisation_proc", "fiche_mort_encephalique", "fiche_voies_aeriennes_adulte"):
            del sys.modules[mn]
    urgences_transfusionnelles_obstetricales = extract_urgences_transfusionnelles_obstetricales()
    with open(os.path.join(BUILD_DIR, "content_urgences_transfusionnelles_obstetricales.json"), "w") as f:
        json.dump(urgences_transfusionnelles_obstetricales, f, ensure_ascii=False, indent=1)
    print("urgences_transfusionnelles_obstetricales sections:", len(urgences_transfusionnelles_obstetricales["sections"]),
          "total blocks:", sum(len(s["items"]) for s in urgences_transfusionnelles_obstetricales["sections"]))

    for mn in list(sys.modules):
        if mn in ("fiche_ecbu", "style", "annexe_specialites", "fiche_anticoagulants", "fiche_choc_hemorragique", "fiche_intubation_urgence", "fiche_sepsis", "fiche_urgences_obstetricales", "fiche_anaphylaxie", "fiche_preeclampsie", "fiche_hyperthermie_maligne", "fiche_anticoag_urgence", "fiche_traumatisme_abdominal", "fiche_sedation_reanimation", "fiche_sedation_urgences", "fiche_vni", "fiche_aap_urgence", "fiche_curares", "fiche_remplissage", "fiche_traumatisme_membre", "fiche_voies_aeriennes_enfant", "fiche_intubation_difficile_adulte", "fiche_traumatisme_pelvien", "fiche_traumatisme_thoracique", "fiche_traumatisme_cranien", "fiche_traumatisme_vertebromedullaire", "fiche_intubation_reanimation", "fiche_traumatisme_cranien_leger", "fiche_lat_soins_critiques", "fiche_sdra", "fiche_pavm", "fiche_tracheotomie", "fiche_nutrition", "fiche_eer", "fiche_ira", "fiche_ih", "fiche_epanchement_pleural", "fiche_anemie", "fiche_hypothermie", "fiche_nvpo", "fiche_aap_programmee", "fiche_mtev_perioperatoire", "fiche_glycemie", "fiche_mal_epileptique", "fiche_allergie_prevention", "fiche_antibioprophylaxie", "fiche_controle_temperature", "fiche_tih", "fiche_civd", "fiche_eclsa", "fiche_transport_intrahospitalier", "fiche_transfusion_plasma", "fiche_sevrage_vm", "fiche_asthme_aigu_grave", "fiche_pancreatite", "fiche_corticotherapie", "fiche_antibiotherapie_probabiliste", "fiche_hsa", "fiche_sepsis_hemodynamique", "fiche_securisation_proc", "fiche_mort_encephalique", "fiche_voies_aeriennes_adulte", "fiche_urgences_transfusionnelles_obstetricales"):
            del sys.modules[mn]
    sujet_age_esf = extract_sujet_age_esf()
    with open(os.path.join(BUILD_DIR, "content_sujet_age_esf.json"), "w") as f:
        json.dump(sujet_age_esf, f, ensure_ascii=False, indent=1)
    print("sujet_age_esf sections:", len(sujet_age_esf["sections"]),
          "total blocks:", sum(len(s["items"]) for s in sujet_age_esf["sections"]))

    for mn in list(sys.modules):
        if mn in ("fiche_ecbu", "style", "annexe_specialites", "fiche_anticoagulants", "fiche_choc_hemorragique", "fiche_intubation_urgence", "fiche_sepsis", "fiche_urgences_obstetricales", "fiche_anaphylaxie", "fiche_preeclampsie", "fiche_hyperthermie_maligne", "fiche_anticoag_urgence", "fiche_traumatisme_abdominal", "fiche_sedation_reanimation", "fiche_sedation_urgences", "fiche_vni", "fiche_aap_urgence", "fiche_curares", "fiche_remplissage", "fiche_traumatisme_membre", "fiche_voies_aeriennes_enfant", "fiche_intubation_difficile_adulte", "fiche_traumatisme_pelvien", "fiche_traumatisme_thoracique", "fiche_traumatisme_cranien", "fiche_traumatisme_vertebromedullaire", "fiche_intubation_reanimation", "fiche_traumatisme_cranien_leger", "fiche_lat_soins_critiques", "fiche_sdra", "fiche_pavm", "fiche_tracheotomie", "fiche_nutrition", "fiche_eer", "fiche_ira", "fiche_ih", "fiche_epanchement_pleural", "fiche_anemie", "fiche_hypothermie", "fiche_nvpo", "fiche_aap_programmee", "fiche_mtev_perioperatoire", "fiche_glycemie", "fiche_mal_epileptique", "fiche_allergie_prevention", "fiche_antibioprophylaxie", "fiche_controle_temperature", "fiche_tih", "fiche_civd", "fiche_eclsa", "fiche_transport_intrahospitalier", "fiche_transfusion_plasma", "fiche_sevrage_vm", "fiche_asthme_aigu_grave", "fiche_pancreatite", "fiche_corticotherapie", "fiche_antibiotherapie_probabiliste", "fiche_hsa", "fiche_sepsis_hemodynamique", "fiche_securisation_proc", "fiche_mort_encephalique", "fiche_voies_aeriennes_adulte", "fiche_urgences_transfusionnelles_obstetricales", "fiche_sujet_age_esf"):
            del sys.modules[mn]
    bris_dentaires = extract_bris_dentaires()
    with open(os.path.join(BUILD_DIR, "content_bris_dentaires.json"), "w") as f:
        json.dump(bris_dentaires, f, ensure_ascii=False, indent=1)
    print("bris_dentaires sections:", len(bris_dentaires["sections"]),
          "total blocks:", sum(len(s["items"]) for s in bris_dentaires["sections"]))

    for mn in list(sys.modules):
        if mn.startswith("fiche_") or mn in ("style", "annexe_specialites"):
            del sys.modules[mn]
    douleur_reactualisation_2016 = extract_douleur_reactualisation_2016()
    with open(os.path.join(BUILD_DIR, "content_douleur_reactualisation_2016.json"), "w") as f:
        json.dump(douleur_reactualisation_2016, f, ensure_ascii=False, indent=1)
    print("douleur_reactualisation_2016 sections:", len(douleur_reactualisation_2016["sections"]),
          "total blocks:", sum(len(s["items"]) for s in douleur_reactualisation_2016["sections"]))

    for mn in list(sys.modules):
        if mn.startswith("fiche_") or mn in ("style", "annexe_specialites"):
            del sys.modules[mn]
    ponction_lombaire = extract_ponction_lombaire()
    with open(os.path.join(BUILD_DIR, "content_ponction_lombaire.json"), "w") as f:
        json.dump(ponction_lombaire, f, ensure_ascii=False, indent=1)
    print("ponction_lombaire sections:", len(ponction_lombaire["sections"]),
          "total blocks:", sum(len(s["items"]) for s in ponction_lombaire["sections"]))

    for mn in list(sys.modules):
        if mn.startswith("fiche_") or mn in ("style", "annexe_specialites"):
            del sys.modules[mn]
    amygdalectomie_enfant = extract_amygdalectomie_enfant()
    with open(os.path.join(BUILD_DIR, "content_amygdalectomie_enfant.json"), "w") as f:
        json.dump(amygdalectomie_enfant, f, ensure_ascii=False, indent=1)
    print("amygdalectomie_enfant sections:", len(amygdalectomie_enfant["sections"]),
          "total blocks:", sum(len(s["items"]) for s in amygdalectomie_enfant["sections"]))

    for mn in list(sys.modules):
        if mn.startswith("fiche_") or mn in ("style", "annexe_specialites"):
            del sys.modules[mn]
    candidoses_aspergilloses = extract_candidoses_aspergilloses()
    with open(os.path.join(BUILD_DIR, "content_candidoses_aspergilloses.json"), "w") as f:
        json.dump(candidoses_aspergilloses, f, ensure_ascii=False, indent=1)
    print("candidoses_aspergilloses sections:", len(candidoses_aspergilloses["sections"]),
          "total blocks:", sum(len(s["items"]) for s in candidoses_aspergilloses["sections"]))

    for mn in list(sys.modules):
        if mn.startswith("fiche_") or mn in ("style", "annexe_specialites"):
            del sys.modules[mn]
    catheters_veineux_centraux = extract_catheters_veineux_centraux()
    with open(os.path.join(BUILD_DIR, "content_catheters_veineux_centraux.json"), "w") as f:
        json.dump(catheters_veineux_centraux, f, ensure_ascii=False, indent=1)
    print("catheters_veineux_centraux sections:", len(catheters_veineux_centraux["sections"]),
          "total blocks:", sum(len(s["items"]) for s in catheters_veineux_centraux["sections"]))

    for mn in list(sys.modules):
        if mn.startswith("fiche_") or mn in ("style", "annexe_specialites"):
            del sys.modules[mn]
    sauv = extract_sauv()
    with open(os.path.join(BUILD_DIR, "content_sauv.json"), "w") as f:
        json.dump(sauv, f, ensure_ascii=False, indent=1)
    print("sauv sections:", len(sauv["sections"]),
          "total blocks:", sum(len(s["items"]) for s in sauv["sections"]))

    for mn in list(sys.modules):
        if mn.startswith("fiche_") or mn in ("style", "annexe_specialites"):
            del sys.modules[mn]
    relations_anesth_chir = extract_relations_anesth_chir()
    with open(os.path.join(BUILD_DIR, "content_relations_anesth_chir.json"), "w") as f:
        json.dump(relations_anesth_chir, f, ensure_ascii=False, indent=1)
    print("relations_anesth_chir sections:", len(relations_anesth_chir["sections"]),
          "total blocks:", sum(len(s["items"]) for s in relations_anesth_chir["sections"]))

    for mn in list(sys.modules):
        if mn.startswith("fiche_") or mn in ("style", "annexe_specialites"):
            del sys.modules[mn]
    erreurs_medicamenteuses = extract_erreurs_medicamenteuses()
    with open(os.path.join(BUILD_DIR, "content_erreurs_medicamenteuses.json"), "w") as f:
        json.dump(erreurs_medicamenteuses, f, ensure_ascii=False, indent=1)
    print("erreurs_medicamenteuses sections:", len(erreurs_medicamenteuses["sections"]),
          "total blocks:", sum(len(s["items"]) for s in erreurs_medicamenteuses["sections"]))

    for mn in list(sys.modules):
        if mn.startswith("fiche_") or mn in ("style", "annexe_specialites"):
            del sys.modules[mn]
    remplissage_perioperatoire = extract_remplissage_perioperatoire()
    with open(os.path.join(BUILD_DIR, "content_remplissage_perioperatoire.json"), "w") as f:
        json.dump(remplissage_perioperatoire, f, ensure_ascii=False, indent=1)
    print("remplissage_perioperatoire sections:", len(remplissage_perioperatoire["sections"]),
          "total blocks:", sum(len(s["items"]) for s in remplissage_perioperatoire["sections"]))

    for mn in list(sys.modules):
        if mn.startswith("fiche_") or mn in ("style", "annexe_specialites"):
            del sys.modules[mn]
    thrombectomie = extract_thrombectomie()
    with open(os.path.join(BUILD_DIR, "content_thrombectomie.json"), "w") as f:
        json.dump(thrombectomie, f, ensure_ascii=False, indent=1)
    print("thrombectomie sections:", len(thrombectomie["sections"]),
          "total blocks:", sum(len(s["items"]) for s in thrombectomie["sections"]))

    for mn in list(sys.modules):
        if mn.startswith("fiche_") or mn in ("style", "annexe_specialites"):
            del sys.modules[mn]
    insuffisance_analgesie_cesarienne = extract_insuffisance_analgesie_cesarienne()
    with open(os.path.join(BUILD_DIR, "content_insuffisance_analgesie_cesarienne.json"), "w") as f:
        json.dump(insuffisance_analgesie_cesarienne, f, ensure_ascii=False, indent=1)
    print("insuffisance_analgesie_cesarienne sections:", len(insuffisance_analgesie_cesarienne["sections"]),
          "total blocks:", sum(len(s["items"]) for s in insuffisance_analgesie_cesarienne["sections"]))

    for mn in list(sys.modules):
        if mn.startswith("fiche_") or mn in ("style", "annexe_specialites"):
            del sys.modules[mn]
    coronarien = extract_coronarien()
    with open(os.path.join(BUILD_DIR, "content_coronarien.json"), "w") as f:
        json.dump(coronarien, f, ensure_ascii=False, indent=1)
    print("coronarien sections:", len(coronarien["sections"]),
          "total blocks:", sum(len(s["items"]) for s in coronarien["sections"]))

    for mn in list(sys.modules):
        if mn.startswith("fiche_") or mn in ("style", "annexe_specialites"):
            del sys.modules[mn]
    brule_grave = extract_brule_grave()
    with open(os.path.join(BUILD_DIR, "content_brule_grave.json"), "w") as f:
        json.dump(brule_grave, f, ensure_ascii=False, indent=1)
    print("brule_grave sections:", len(brule_grave["sections"]),
          "total blocks:", sum(len(s["items"]) for s in brule_grave["sections"]))

    for mn in list(sys.modules):
        if mn.startswith("fiche_") or mn in ("style", "annexe_specialites"):
            del sys.modules[mn]
    tabagisme = extract_tabagisme()
    with open(os.path.join(BUILD_DIR, "content_tabagisme.json"), "w") as f:
        json.dump(tabagisme, f, ensure_ascii=False, indent=1)
    print("tabagisme sections:", len(tabagisme["sections"]),
          "total blocks:", sum(len(s["items"]) for s in tabagisme["sections"]))

    for mn in list(sys.modules):
        if mn.startswith("fiche_") or mn in ("style", "annexe_specialites"):
            del sys.modules[mn]
    infections_intra_abdominales = extract_infections_intra_abdominales()
    with open(os.path.join(BUILD_DIR, "content_infections_intra_abdominales.json"), "w") as f:
        json.dump(infections_intra_abdominales, f, ensure_ascii=False, indent=1)
    print("infections_intra_abdominales sections:", len(infections_intra_abdominales["sections"]),
          "total blocks:", sum(len(s["items"]) for s in infections_intra_abdominales["sections"]))

    for mn in list(sys.modules):
        if mn.startswith("fiche_") or mn in ("style", "annexe_specialites"):
            del sys.modules[mn]
    alr_perinerveuse = extract_alr_perinerveuse()
    with open(os.path.join(BUILD_DIR, "content_alr_perinerveuse.json"), "w") as f:
        json.dump(alr_perinerveuse, f, ensure_ascii=False, indent=1)
    print("alr_perinerveuse sections:", len(alr_perinerveuse["sections"]),
          "total blocks:", sum(len(s["items"]) for s in alr_perinerveuse["sections"]))

    for mn in list(sys.modules):
        if mn.startswith("fiche_") or mn in ("style", "annexe_specialites"):
            del sys.modules[mn]
    urgences_ob_extrahosp = extract_urgences_ob_extrahosp()
    with open(os.path.join(BUILD_DIR, "content_urgences_ob_extrahosp.json"), "w") as f:
        json.dump(urgences_ob_extrahosp, f, ensure_ascii=False, indent=1)
    print("urgences_ob_extrahosp sections:", len(urgences_ob_extrahosp["sections"]),
          "total blocks:", sum(len(s["items"]) for s in urgences_ob_extrahosp["sections"]))

    for mn in list(sys.modules):
        if mn.startswith("fiche_") or mn in ("style", "annexe_specialites"):
            del sys.modules[mn]
    aod_urgence = extract_aod_urgence()
    with open(os.path.join(BUILD_DIR, "content_aod_urgence.json"), "w") as f:
        json.dump(aod_urgence, f, ensure_ascii=False, indent=1)
    print("aod_urgence sections:", len(aod_urgence["sections"]),
          "total blocks:", sum(len(s["items"]) for s in aod_urgence["sections"]))

    for mn in list(sys.modules):
        if mn.startswith("fiche_") or mn in ("style", "annexe_specialites"):
            del sys.modules[mn]
    plyo_transfusion = extract_plyo_transfusion()
    with open(os.path.join(BUILD_DIR, "content_plyo_transfusion.json"), "w") as f:
        json.dump(plyo_transfusion, f, ensure_ascii=False, indent=1)
    print("plyo_transfusion sections:", len(plyo_transfusion["sections"]),
          "total blocks:", sum(len(s["items"]) for s in plyo_transfusion["sections"]))

    for mn in list(sys.modules):
        if mn.startswith("fiche_") or mn in ("style", "annexe_specialites"):
            del sys.modules[mn]
    tenue_vestimentaire = extract_tenue_vestimentaire()
    with open(os.path.join(BUILD_DIR, "content_tenue_vestimentaire.json"), "w") as f:
        json.dump(tenue_vestimentaire, f, ensure_ascii=False, indent=1)
    print("tenue_vestimentaire sections:", len(tenue_vestimentaire["sections"]),
          "total blocks:", sum(len(s["items"]) for s in tenue_vestimentaire["sections"]))

    for mn in list(sys.modules):
        if mn.startswith("fiche_") or mn in ("style", "annexe_specialites"):
            del sys.modules[mn]
    alr_non_specialiste = extract_alr_non_specialiste()
    with open(os.path.join(BUILD_DIR, "content_alr_non_specialiste.json"), "w") as f:
        json.dump(alr_non_specialiste, f, ensure_ascii=False, indent=1)
    print("alr_non_specialiste sections:", len(alr_non_specialiste["sections"]),
          "total blocks:", sum(len(s["items"]) for s in alr_non_specialiste["sections"]))

    for mn in list(sys.modules):
        if mn.startswith("fiche_") or mn in ("style", "annexe_specialites"):
            del sys.modules[mn]
    echo_acces_vasculaires = extract_echo_acces_vasculaires()
    with open(os.path.join(BUILD_DIR, "content_echo_acces_vasculaires.json"), "w") as f:
        json.dump(echo_acces_vasculaires, f, ensure_ascii=False, indent=1)
    print("echo_acces_vasculaires sections:", len(echo_acces_vasculaires["sections"]),
          "total blocks:", sum(len(s["items"]) for s in echo_acces_vasculaires["sections"]))

    for mn in list(sys.modules):
        if mn.startswith("fiche_") or mn in ("style", "annexe_specialites"):
            del sys.modules[mn]
    tests_viscoelastiques = extract_tests_viscoelastiques()
    with open(os.path.join(BUILD_DIR, "content_tests_viscoelastiques.json"), "w") as f:
        json.dump(tests_viscoelastiques, f, ensure_ascii=False, indent=1)
    print("tests_viscoelastiques sections:", len(tests_viscoelastiques["sections"]),
          "total blocks:", sum(len(s["items"]) for s in tests_viscoelastiques["sections"]))

    for mn in list(sys.modules):
        if mn.startswith("fiche_") or mn in ("style", "annexe_specialites"):
            del sys.modules[mn]
    eeg_cortical = extract_eeg_cortical()
    with open(os.path.join(BUILD_DIR, "content_eeg_cortical.json"), "w") as f:
        json.dump(eeg_cortical, f, ensure_ascii=False, indent=1)
    print("eeg_cortical sections:", len(eeg_cortical["sections"]),
          "total blocks:", sum(len(s["items"]) for s in eeg_cortical["sections"]))

    for mn in list(sys.modules):
        if mn.startswith("fiche_") or mn in ("style", "annexe_specialites"):
            del sys.modules[mn]
    examens_pertinence_rea = extract_examens_pertinence_rea()
    with open(os.path.join(BUILD_DIR, "content_examens_pertinence_rea.json"), "w") as f:
        json.dump(examens_pertinence_rea, f, ensure_ascii=False, indent=1)
    print("examens_pertinence_rea sections:", len(examens_pertinence_rea["sections"]),
          "total blocks:", sum(len(s["items"]) for s in examens_pertinence_rea["sections"]))

    for mn in list(sys.modules):
        if mn.startswith("fiche_") or mn in ("style", "annexe_specialites"):
            del sys.modules[mn]
    alr_pediatrie = extract_alr_pediatrie()
    with open(os.path.join(BUILD_DIR, "content_alr_pediatrie.json"), "w") as f:
        json.dump(alr_pediatrie, f, ensure_ascii=False, indent=1)
    print("alr_pediatrie sections:", len(alr_pediatrie["sections"]),
          "total blocks:", sum(len(s["items"]) for s in alr_pediatrie["sections"]))

    for mn in list(sys.modules):
        if mn.startswith("fiche_") or mn in ("style", "annexe_specialites"):
            del sys.modules[mn]
    hospit_ambulatoire = extract_hospit_ambulatoire()
    with open(os.path.join(BUILD_DIR, "content_hospit_ambulatoire.json"), "w") as f:
        json.dump(hospit_ambulatoire, f, ensure_ascii=False, indent=1)
    print("hospit_ambulatoire sections:", len(hospit_ambulatoire["sections"]),
          "total blocks:", sum(len(s["items"]) for s in hospit_ambulatoire["sections"]))

    for mn in list(sys.modules):
        if mn.startswith("fiche_") or mn in ("style", "annexe_specialites"):
            del sys.modules[mn]
    echo_alr = extract_echo_alr()
    with open(os.path.join(BUILD_DIR, "content_echo_alr.json"), "w") as f:
        json.dump(echo_alr, f, ensure_ascii=False, indent=1)
    print("echo_alr sections:", len(echo_alr["sections"]),
          "total blocks:", sum(len(s["items"]) for s in echo_alr["sections"]))

    for mn in list(sys.modules):
        if mn.startswith("fiche_") or mn in ("style", "annexe_specialites"):
            del sys.modules[mn]
    alr_douleur_chronique = extract_alr_douleur_chronique()
    with open(os.path.join(BUILD_DIR, "content_alr_douleur_chronique.json"), "w") as f:
        json.dump(alr_douleur_chronique, f, ensure_ascii=False, indent=1)
    print("alr_douleur_chronique sections:", len(alr_douleur_chronique["sections"]),
          "total blocks:", sum(len(s["items"]) for s in alr_douleur_chronique["sections"]))

    for mn in list(sys.modules):
        if mn.startswith("fiche_") or mn in ("style", "annexe_specialites"):
            del sys.modules[mn]
    infections_nosocomiales_rea = extract_infections_nosocomiales_rea()
    with open(os.path.join(BUILD_DIR, "content_infections_nosocomiales_rea.json"), "w") as f:
        json.dump(infections_nosocomiales_rea, f, ensure_ascii=False, indent=1)
    print("infections_nosocomiales_rea sections:", len(infections_nosocomiales_rea["sections"]),
          "total blocks:", sum(len(s["items"]) for s in infections_nosocomiales_rea["sections"]))

    for mn in list(sys.modules):
        if mn.startswith("fiche_") or mn in ("style", "annexe_specialites"):
            del sys.modules[mn]
    nutrition_perioperatoire = extract_nutrition_perioperatoire()
    with open(os.path.join(BUILD_DIR, "content_nutrition_perioperatoire.json"), "w") as f:
        json.dump(nutrition_perioperatoire, f, ensure_ascii=False, indent=1)
    print("nutrition_perioperatoire sections:", len(nutrition_perioperatoire["sections"]),
          "total blocks:", sum(len(s["items"]) for s in nutrition_perioperatoire["sections"]))

    for mn in list(sys.modules):
        if mn.startswith("fiche_") or mn in ("style", "annexe_specialites"):
            del sys.modules[mn]
    ivg_14sa = extract_ivg_14sa()
    with open(os.path.join(BUILD_DIR, "content_ivg_14sa.json"), "w") as f:
        json.dump(ivg_14sa, f, ensure_ascii=False, indent=1)
    print("ivg_14sa sections:", len(ivg_14sa["sections"]),
          "total blocks:", sum(len(s["items"]) for s in ivg_14sa["sections"]))

    for mn in list(sys.modules):
        if mn.startswith("fiche_") or mn in ("style", "annexe_specialites"):
            del sys.modules[mn]
    aod_programme = extract_aod_programme()
    with open(os.path.join(BUILD_DIR, "content_aod_programme.json"), "w") as f:
        json.dump(aod_programme, f, ensure_ascii=False, indent=1)
    print("aod_programme sections:", len(aod_programme["sections"]),
          "total blocks:", sum(len(s["items"]) for s in aod_programme["sections"]))

    for mn in list(sys.modules):
        if mn.startswith("fiche_") or mn in ("style", "annexe_specialites"):
            del sys.modules[mn]
    blocs_peripheriques_membres = extract_blocs_peripheriques_membres()
    with open(os.path.join(BUILD_DIR, "content_blocs_peripheriques_membres.json"), "w") as f:
        json.dump(blocs_peripheriques_membres, f, ensure_ascii=False, indent=1)
    print("blocs_peripheriques_membres sections:", len(blocs_peripheriques_membres["sections"]),
          "total blocks:", sum(len(s["items"]) for s in blocs_peripheriques_membres["sections"]))

    for mn in list(sys.modules):
        if mn.startswith("fiche_") or mn in ("style", "annexe_specialites"):
            del sys.modules[mn]
    raac_colorectal = extract_raac_colorectal()
    with open(os.path.join(BUILD_DIR, "content_raac_colorectal.json"), "w") as f:
        json.dump(raac_colorectal, f, ensure_ascii=False, indent=1)
    print("raac_colorectal sections:", len(raac_colorectal["sections"]),
          "total blocks:", sum(len(s["items"]) for s in raac_colorectal["sections"]))

    for mn in list(sys.modules):
        if mn.startswith("fiche_") or mn in ("style", "annexe_specialites"):
            del sys.modules[mn]
    chir_ambu_proctologie = extract_chir_ambu_proctologie()
    with open(os.path.join(BUILD_DIR, "content_chir_ambu_proctologie.json"), "w") as f:
        json.dump(chir_ambu_proctologie, f, ensure_ascii=False, indent=1)
    print("chir_ambu_proctologie sections:", len(chir_ambu_proctologie["sections"]),
          "total blocks:", sum(len(s["items"]) for s in chir_ambu_proctologie["sections"]))

    for mn in list(sys.modules):
        if mn.startswith("fiche_") or mn in ("style", "annexe_specialites"):
            del sys.modules[mn]
    mieux_vivre_reanimation = extract_mieux_vivre_reanimation()
    with open(os.path.join(BUILD_DIR, "content_mieux_vivre_reanimation.json"), "w") as f:
        json.dump(mieux_vivre_reanimation, f, ensure_ascii=False, indent=1)
    print("mieux_vivre_reanimation sections:", len(mieux_vivre_reanimation["sections"]),
          "total blocks:", sum(len(s["items"]) for s in mieux_vivre_reanimation["sections"]))

    for mn in list(sys.modules):
        if mn.startswith("fiche_") or mn in ("style", "annexe_specialites"):
            del sys.modules[mn]
    preparation_colique = extract_preparation_colique()
    with open(os.path.join(BUILD_DIR, "content_preparation_colique.json"), "w") as f:
        json.dump(preparation_colique, f, ensure_ascii=False, indent=1)
    print("preparation_colique sections:", len(preparation_colique["sections"]),
          "total blocks:", sum(len(s["items"]) for s in preparation_colique["sections"]))

    for mn in list(sys.modules):
        if mn.startswith("fiche_") or mn in ("style", "annexe_specialites"):
            del sys.modules[mn]
    organisation_ar_obstetricale = extract_organisation_ar_obstetricale()
    with open(os.path.join(BUILD_DIR, "content_organisation_ar_obstetricale.json"), "w") as f:
        json.dump(organisation_ar_obstetricale, f, ensure_ascii=False, indent=1)
    print("organisation_ar_obstetricale sections:", len(organisation_ar_obstetricale["sections"]),
          "total blocks:", sum(len(s["items"]) for s in organisation_ar_obstetricale["sections"]))

    for mn in list(sys.modules):
        if mn.startswith("fiche_") or mn in ("style", "annexe_specialites"):
            del sys.modules[mn]
    erreurs_medicamenteuses_ar_2016 = extract_erreurs_medicamenteuses_ar_2016()
    with open(os.path.join(BUILD_DIR, "content_erreurs_medicamenteuses_ar_2016.json"), "w") as f:
        json.dump(erreurs_medicamenteuses_ar_2016, f, ensure_ascii=False, indent=1)
    print("erreurs_medicamenteuses_ar_2016 sections:", len(erreurs_medicamenteuses_ar_2016["sections"]),
          "total blocks:", sum(len(s["items"]) for s in erreurs_medicamenteuses_ar_2016["sections"]))

    for mn in list(sys.modules):
        if mn.startswith("fiche_") or mn in ("style", "annexe_specialites"):
            del sys.modules[mn]
    anesth_pediatrique_structures = extract_anesth_pediatrique_structures()
    with open(os.path.join(BUILD_DIR, "content_anesth_pediatrique_structures.json"), "w") as f:
        json.dump(anesth_pediatrique_structures, f, ensure_ascii=False, indent=1)
    print("anesth_pediatrique_structures sections:", len(anesth_pediatrique_structures["sections"]),
          "total blocks:", sum(len(s["items"]) for s in anesth_pediatrique_structures["sections"]))

    for mn in list(sys.modules):
        if mn.startswith("fiche_") or mn in ("style", "annexe_specialites"):
            del sys.modules[mn]
    aod_dabigatran_urgence_2016 = extract_aod_dabigatran_urgence_2016()
    with open(os.path.join(BUILD_DIR, "content_aod_dabigatran_urgence_2016.json"), "w") as f:
        json.dump(aod_dabigatran_urgence_2016, f, ensure_ascii=False, indent=1)
    print("aod_dabigatran_urgence_2016 sections:", len(aod_dabigatran_urgence_2016["sections"]),
          "total blocks:", sum(len(s["items"]) for s in aod_dabigatran_urgence_2016["sections"]))

    for mn in list(sys.modules):
        if mn.startswith("fiche_") or mn in ("style", "annexe_specialites"):
            del sys.modules[mn]
    tc_readaptation = extract_tc_readaptation()
    with open(os.path.join(BUILD_DIR, "content_tc_readaptation.json"), "w") as f:
        json.dump(tc_readaptation, f, ensure_ascii=False, indent=1)
    print("tc_readaptation sections:", len(tc_readaptation["sections"]),
          "total blocks:", sum(len(s["items"]) for s in tc_readaptation["sections"]))

    for mn in list(sys.modules):
        if mn.startswith("fiche_") or mn in ("style", "annexe_specialites"):
            del sys.modules[mn]
    impact_environnemental_ag = extract_impact_environnemental_ag()
    with open(os.path.join(BUILD_DIR, "content_impact_environnemental_ag.json"), "w") as f:
        json.dump(impact_environnemental_ag, f, ensure_ascii=False, indent=1)
    print("impact_environnemental_ag sections:", len(impact_environnemental_ag["sections"]),
          "total blocks:", sum(len(s["items"]) for s in impact_environnemental_ag["sections"]))

    for mn in list(sys.modules):
        if mn.startswith("fiche_") or mn in ("style", "annexe_specialites"):
            del sys.modules[mn]
    diabete_perioperatoire_2025 = extract_diabete_perioperatoire_2025()
    with open(os.path.join(BUILD_DIR, "content_diabete_perioperatoire_2025.json"), "w") as f:
        json.dump(diabete_perioperatoire_2025, f, ensure_ascii=False, indent=1)
    print("diabete_perioperatoire_2025 sections:", len(diabete_perioperatoire_2025["sections"]),
          "total blocks:", sum(len(s["items"]) for s in diabete_perioperatoire_2025["sections"]))

    for mn in list(sys.modules):
        if mn.startswith("fiche_") or mn in ("style", "annexe_specialites"):
            del sys.modules[mn]
    anesth_cardiopathie_congenitale = extract_anesth_cardiopathie_congenitale()
    with open(os.path.join(BUILD_DIR, "content_anesth_cardiopathie_congenitale.json"), "w") as f:
        json.dump(anesth_cardiopathie_congenitale, f, ensure_ascii=False, indent=1)
    print("anesth_cardiopathie_congenitale sections:", len(anesth_cardiopathie_congenitale["sections"]),
          "total blocks:", sum(len(s["items"]) for s in anesth_cardiopathie_congenitale["sections"]))

    for mn in list(sys.modules):
        if mn.startswith("fiche_") or mn in ("style", "annexe_specialites"):
            del sys.modules[mn]
    ressources_humaines_anesthesie_2024 = extract_ressources_humaines_anesthesie_2024()
    with open(os.path.join(BUILD_DIR, "content_ressources_humaines_anesthesie_2024.json"), "w") as f:
        json.dump(ressources_humaines_anesthesie_2024, f, ensure_ascii=False, indent=1)
    print("ressources_humaines_anesthesie_2024 sections:", len(ressources_humaines_anesthesie_2024["sections"]),
          "total blocks:", sum(len(s["items"]) for s in ressources_humaines_anesthesie_2024["sections"]))

    for mn in list(sys.modules):
        if mn.startswith("fiche_") or mn in ("style", "annexe_specialites"):
            del sys.modules[mn]
    demarches_anticipees_don_organes_2024 = extract_demarches_anticipees_don_organes_2024()
    with open(os.path.join(BUILD_DIR, "content_demarches_anticipees_don_organes_2024.json"), "w") as f:
        json.dump(demarches_anticipees_don_organes_2024, f, ensure_ascii=False, indent=1)
    print("demarches_anticipees_don_organes_2024 sections:", len(demarches_anticipees_don_organes_2024["sections"]),
          "total blocks:", sum(len(s["items"]) for s in demarches_anticipees_don_organes_2024["sections"]))

    for mn in list(sys.modules):
        if mn.startswith("fiche_") or mn in ("style", "annexe_specialites"):
            del sys.modules[mn]
    raac_orthopedique_2019 = extract_raac_orthopedique_2019()
    with open(os.path.join(BUILD_DIR, "content_raac_orthopedique_2019.json"), "w") as f:
        json.dump(raac_orthopedique_2019, f, ensure_ascii=False, indent=1)
    print("raac_orthopedique_2019 sections:", len(raac_orthopedique_2019["sections"]),
          "total blocks:", sum(len(s["items"]) for s in raac_orthopedique_2019["sections"]))

    for mn in list(sys.modules):
        if mn.startswith("fiche_") or mn in ("style", "annexe_specialites"):
            del sys.modules[mn]
    reduction_antibiotiques_reanimation_2014 = extract_reduction_antibiotiques_reanimation_2014()
    with open(os.path.join(BUILD_DIR, "content_reduction_antibiotiques_reanimation_2014.json"), "w") as f:
        json.dump(reduction_antibiotiques_reanimation_2014, f, ensure_ascii=False, indent=1)
    print("reduction_antibiotiques_reanimation_2014 sections:", len(reduction_antibiotiques_reanimation_2014["sections"]),
          "total blocks:", sum(len(s["items"]) for s in reduction_antibiotiques_reanimation_2014["sections"]))

    for mn in list(sys.modules):
        if mn.startswith("fiche_") or mn in ("style", "annexe_specialites"):
            del sys.modules[mn]
    simulation_soins_critiques_2019 = extract_simulation_soins_critiques_2019()
    with open(os.path.join(BUILD_DIR, "content_simulation_soins_critiques_2019.json"), "w") as f:
        json.dump(simulation_soins_critiques_2019, f, ensure_ascii=False, indent=1)
    print("simulation_soins_critiques_2019 sections:", len(simulation_soins_critiques_2019["sections"]),
          "total blocks:", sum(len(s["items"]) for s in simulation_soins_critiques_2019["sections"]))

    for mn in list(sys.modules):
        if mn.startswith("fiche_") or mn in ("style", "annexe_specialites"):
            del sys.modules[mn]
    optimisation_beta_lactamines_2018 = extract_optimisation_beta_lactamines_2018()
    with open(os.path.join(BUILD_DIR, "content_optimisation_beta_lactamines_2018.json"), "w") as f:
        json.dump(optimisation_beta_lactamines_2018, f, ensure_ascii=False, indent=1)
    print("optimisation_beta_lactamines_2018 sections:", len(optimisation_beta_lactamines_2018["sections"]),
          "total blocks:", sum(len(s["items"]) for s in optimisation_beta_lactamines_2018["sections"]))

    for mn in list(sys.modules):
        if mn.startswith("fiche_") or mn in ("style", "annexe_specialites"):
            del sys.modules[mn]
    raac_lobectomie_pulmonaire_2019 = extract_raac_lobectomie_pulmonaire_2019()
    with open(os.path.join(BUILD_DIR, "content_raac_lobectomie_pulmonaire_2019.json"), "w") as f:
        json.dump(raac_lobectomie_pulmonaire_2019, f, ensure_ascii=False, indent=1)
    print("raac_lobectomie_pulmonaire_2019 sections:", len(raac_lobectomie_pulmonaire_2019["sections"]),
          "total blocks:", sum(len(s["items"]) for s in raac_lobectomie_pulmonaire_2019["sections"]))

    for mn in list(sys.modules):
        if mn.startswith("fiche_") or mn in ("style", "annexe_specialites"):
            del sys.modules[mn]
    raac_cardiaque_2021 = extract_raac_cardiaque_2021()
    with open(os.path.join(BUILD_DIR, "content_raac_cardiaque_2021.json"), "w") as f:
        json.dump(raac_cardiaque_2021, f, ensure_ascii=False, indent=1)
    print("raac_cardiaque_2021 sections:", len(raac_cardiaque_2021["sections"]),
          "total blocks:", sum(len(s["items"]) for s in raac_cardiaque_2021["sections"]))

    for mn in list(sys.modules):
        if mn.startswith("fiche_") or mn in ("style", "annexe_specialites"):
            del sys.modules[mn]
    optimisation_hemodynamique_pediatrie_2024 = extract_optimisation_hemodynamique_pediatrie_2024()
    with open(os.path.join(BUILD_DIR, "content_optimisation_hemodynamique_pediatrie_2024.json"), "w") as f:
        json.dump(optimisation_hemodynamique_pediatrie_2024, f, ensure_ascii=False, indent=1)
    print("optimisation_hemodynamique_pediatrie_2024 sections:", len(optimisation_hemodynamique_pediatrie_2024["sections"]),
          "total blocks:", sum(len(s["items"]) for s in optimisation_hemodynamique_pediatrie_2024["sections"]))

    for mn in list(sys.modules):
        if mn.startswith("fiche_") or mn in ("style", "annexe_specialites"):
            del sys.modules[mn]
    optimisation_hemodynamique_adulte_2024 = extract_optimisation_hemodynamique_adulte_2024()
    with open(os.path.join(BUILD_DIR, "content_optimisation_hemodynamique_adulte_2024.json"), "w") as f:
        json.dump(optimisation_hemodynamique_adulte_2024, f, ensure_ascii=False, indent=1)
    print("optimisation_hemodynamique_adulte_2024 sections:", len(optimisation_hemodynamique_adulte_2024["sections"]),
          "total blocks:", sum(len(s["items"]) for s in optimisation_hemodynamique_adulte_2024["sections"]))
