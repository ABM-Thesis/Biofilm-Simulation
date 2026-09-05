# -*- coding: utf-8 -*-
"""Πείραμα 17-convergence — ενότητα 4.7 — Εικ. Δ.4 (στοχαστική σύγκλιση)."""
import numpy as np
from core import ci95, deco, experiment, plt, save, say

def run(d, out):
    """[17] Στοχαστική σύγκλιση: τεκμηριώνει το n=20 αντί να το υποθέτει."""
    _, last = experiment("*17-convergence*table.csv", d, "[17] ΣΤΟΧΑΣΤΙΚΗ ΣΥΓΚΛΙΣΗ — τεκμηρίωση του αριθμού επαναλήψεων")
    if last is None: return
    fig, ax = plt.subplots(1, 2, figsize=(11, 4.2))
    for i, (col, ttl) in enumerate([("alive", "Τελικός πληθυσμός"), ("res", "Τελική μέση αντοχή")]):
        x = last[col].dropna().values
        if len(x) < 5: continue
        ns = list(range(3, len(x) + 1))
        cis = [ci95(x[:n]) for n in ns]
        means, halfw = np.array([c[0] for c in cis]), np.array([(c[2] - c[1]) / 2 for c in cis])
        ax[i].plot(ns, means, lw=2, color="#1f77b4")
        ax[i].fill_between(ns, means - halfw, means + halfw, alpha=.25, color="#1f77b4")
        ax[i].axvline(20, color="crimson", ls="--", lw=1.5, label="n = 20 (επιλογή)")
        deco(ax[i], "αριθμός επαναλήψεων", title=ttl, legend={"fontsize": 8}, grid=.3)
        hw = {}
        for target in (10, 20, len(x)):
            if target <= len(x):
                m, lo, hi = ci95(x[:target])
                hw[target] = 100*(hi-lo)/2/abs(m) if m else 0
                say(f"  {ttl}, n={target:>3}: μέση {m:.4g} | ημιπλάτος ΔΕ = {(hi-lo)/2:.4g} "
                    f"({hw[target]:.2f}% της μέσης)")
        # ετυμηγορία: σταθεροποιημένο ΔΕ (δεν πέφτει ως 1/sqrt(n)) Ή ήδη <1% της μέσης
        if 20 in hw and len(x) in hw and len(x) > 20:
            drop = hw[20] / hw[len(x)] if hw[len(x)] else np.inf
            expected = np.sqrt(len(x) / 20)   # αναμενόμενη πτώση αν ΔΕΝ έχει συγκλίνει
            PRACTICAL = 1.0                   # % της μέσης
            if hw[20] <= PRACTICAL:
                say(f"  -> {ttl}: ΣΥΓΚΛΙΝΕΙ. Το ΔΕ στο n=20 είναι {hw[20]:.2f}% της μέσης")
                say(f"     (κατώφλι πρακτικής ακρίβειας {PRACTICAL:.0f}%). Το n=20 επαρκεί.")
            elif drop > 0.75 * expected:
                say(f"  -> {ttl}: ΔΕΝ ΕΧΕΙ ΣΥΓΚΛΙΝΕΙ στο n=20. Το ημιπλάτος πέφτει ακόμη")
                say(f"     ως 1/sqrt(n) (παρατηρούμενη πτώση {drop:.2f}x, αναμενόμενη {expected:.2f}x).")
            else:
                say(f"  -> {ttl}: το ημιπλάτος έχει σταθεροποιηθεί (ΔΕ {hw[20]:.2f}%)· "
                    f"το n=20 επαρκεί.")
    fig.suptitle("Σύγκλιση των εκτιμήσεων με τον αριθμό επαναλήψεων")
    save(fig, out, "fig22_convergence.png")
