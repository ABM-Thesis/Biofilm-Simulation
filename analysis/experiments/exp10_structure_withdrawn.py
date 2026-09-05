# -*- coding: utf-8 -*-
"""Πείραμα 10-structure-emergence — ενότητα αποσυρμένη ανάλυση (μόνο --appendix)."""
from core import compare, experiment, heatmap, plt, save, say

def run(d, out, appendix=False):
    """[10] Αποσυρμένη ανάλυση (μη έγκυρος δείκτης shape-factor)· μόνο με --appendix."""
    if not appendix: return
    _, last = experiment("*10-structure*table.csv", d, "[ΠΑΡΑΡΤΗΜΑ 10] ΑΠΟΣΥΡΜΕΝΗ ΑΝΑΛΥΣΗ — ΜΗ ΕΓΚΥΡΟΣ ΔΕΙΚΤΗΣ")
    if last is None: return
    say("  !! μη έγκυρος δείκτης (shape-factor) — δεν αναφέρεται ως αποτέλεσμα· έγκυρη ανάλυση: [14]")
    piv = last.groupby(["ndiff", "maxcells"])["shape"].mean().unstack()
    say("  shape factor (πάχος βιοφίλμ):"); say(piv.round(2).to_string())
    pivN = last.groupby(["ndiff", "maxcells"])["alive"].mean().unstack()
    say("  τελικός πληθυσμός:"); say(pivN.round(0).to_string())
    a = last[(last["maxcells"] == 0)]["shape"].values
    b = last[(last["maxcells"] > 0) & (last["ndiff"] > 0)]["shape"].values
    if len(a) > 1 and len(b) > 1:
        compare("  shape: χωρίς περιορισμούς vs αποκλεισμός όγκου + διάχυση θρεπτικών", a, b)
    fig, ax = plt.subplots(1, 2, figsize=(11, 4.2))
    for k, (p_, ttl, fm) in enumerate([(piv, "Shape factor (πάχος βιοφίλμ)", ".2f"), (pivN, "Τελικός πληθυσμός", ".0f")]):
        heatmap(fig, ax[k], p_, ttl, fm, "max-cells-per-patch (0 = χωρίς όριο)", "nutrient-diffusion")
    fig.suptitle("Η κατακόρυφη δομή απαιτεί ΚΑΙ αποκλεισμό όγκου ΚΑΙ διάχυση θρεπτικών")
    save(fig, out, "fig13_structure_emergence.png")
