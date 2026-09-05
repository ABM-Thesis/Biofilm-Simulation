# -*- coding: utf-8 -*-
"""Πείραμα 14-structure-validated — ενότητα 4.5 — Εικ. 4.7 (ανάδυση δομής)."""
from core import compare, experiment, heatmap, plt, save, say

def run(d, out):
    """[14] Ανάδυση δομής με τους δείκτες bf-height, bf-spread, bf-occupancy."""
    _, last = experiment("*14-structure-validated*table.csv", d, "[14] ΑΝΑΔΥΣΗ ΔΟΜΗΣ — ΕΠΙΚΥΡΩΣΗ ΜΕ ΔΙΟΡΘΩΜΕΝΕΣ ΜΕΤΡΙΚΕΣ")
    if last is None: return
    pivots = []
    for col, ttl, fm in [("bfh", "bf-height (95ο εκατ. ύψους)", ".2f"), ("bfs", "bf-spread (SD ύψους)", ".2f"),
                         ("bfo", "bf-occupancy (κύτταρα/patch)", ".2f"), ("alive", "τελικός πληθυσμός", ".0f")]:
        if col not in last.columns: continue
        piv = last.groupby(["ndiff", "maxcells"])[col].mean().unstack()
        n_ext = last[last[col].isna()].shape[0]
        say(f"  {ttl}:" + (f"   [{n_ext} εκτελέσεις εξαφανίστηκαν -> NaN]" if n_ext else ""))
        say(piv.round(2).to_string())
        pivots.append((piv, ttl, fm))

    say("  -- απαιτούνται και οι δύο μηχανισμοί; --")       # ΚΑΙ αποκλεισμός όγκου ΚΑΙ διάχυση;
    vol, dif = last["maxcells"] > 0, last["ndiff"] > 0
    for col, lbl in [("bfh", "ύψος"), ("bfs", "spread")]:
        if col not in last.columns: continue
        both_ = last[vol & dif][col].values
        for lab, sel in [("μόνο αποκλεισμός όγκου", vol & ~dif), ("μόνο διάχυση", ~vol & dif), ("κανένας", ~vol & ~dif)]:
            other = last[sel][col].values
            if len(both_) > 1 and len(other) > 1:
                compare(f"  {lbl}: {lab} vs ΚΑΙ ΤΑ ΔΥΟ", both_, other)

    if not pivots: return
    n = len(pivots)
    fig, ax = plt.subplots(1, n, figsize=(4.2 * n, 4.2))
    if n == 1: ax = [ax]
    for k, (p_, ttl, fm) in enumerate(pivots):
        heatmap(fig, ax[k], p_, ttl, fm, "max-cells-per-patch (0 = χωρίς όριο)", "nutrient-diffusion",
                fontsize=8, nan_dash=True, title_fs=10)
    fig.suptitle("Ανάδυση δομής — διορθωμένες μετρικές (10 επαναλήψεις/κελί)")
    save(fig, out, "fig19_structure_validated.png")
