# -*- coding: utf-8 -*-
"""Πείραμα 6-triggerhgt-fine — ενότητα 4.4 — Εικ. 4.4 (σημείο ανατροπής)."""
import numpy as np
from core import deco, experiment, fmt_ci, plt, save, say

def run(d, out):
    _, last = experiment("*6-triggerhgt-fine*table.csv", d, "[6] ΛΕΠΤΟΜΕΡΗΣ ΣΑΡΩΣΗ ΚΑΤΩΦΛΙΟΥ HGT")
    if last is None: return
    say("  ('ΚΑΘΗΛΩΣΗ' = ποσοστό εκτελέσεων με τελική μέση αντοχή > 0,5)")
    xs = sorted(last["trig"].unique())
    pts = [last[last["trig"] == x]["res"].values for x in xs]
    for x, v in zip(xs, pts):
        say(f"  Triggerhgt = {x}: αντοχή {fmt_ci(v)} | εύρος [{v.min():.2f}, {v.max():.2f}] "
            f"| ΚΑΘΗΛΩΣΗ σε {(v > 0.5).mean()*100:.0f}% των εκτελέσεων")
    crit = xs[int(np.argmax([v.std(ddof=1) for v in pts]))]
    say(f"  -> μέγιστη διακύμανση στο Triggerhgt = {crit} (υπογραφή στοχαστικού σημείου ανατροπής)")
    fig, ax = plt.subplots(figsize=(7.5, 4.6))
    for x, v in zip(xs, pts):
        ax.plot([x]*len(v), v, "o", color="#888", alpha=.5, ms=5)
    ax.plot(xs, [v.mean() for v in pts], "-o", color="#d62728", lw=2, ms=7, label="Μέση αντοχή")
    ax.axvspan(crit - .025, crit + .025, alpha=.12, color="orange")
    ax.annotate(f"κρίσιμο κατώφλι ≈ {crit}", (crit, .75), ha="center", fontsize=9, color="#b8860b")
    deco(ax, "Τιμή αντοχής βακτηρίου στο αντιβιοτικό για την ενεργοποιήση της HGT (Triggerhgt)", "Τελική μέση αντοχή", "Εντοπισμός του σημείου ανατροπής", (0, 1.05), {})
    save(fig, out, "fig9_tipping_fine.png")
