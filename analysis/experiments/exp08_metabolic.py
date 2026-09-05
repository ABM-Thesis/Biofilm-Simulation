# -*- coding: utf-8 -*-
"""Πείραμα 8-metabolic-sensitivity — ενότητα 4.7 — Εικ. Δ.2."""
from core import experiment, heatmap, plt, save, say

def run(d, out):
    _, last = experiment("*8-metabolic*table.csv", d, "[8] ΕΥΑΙΣΘΗΣΙΑ ΜΕΤΑΒΟΛΙΚΩΝ ΠΑΡΑΜΕΤΡΩΝ (χωρητικότητα)")
    if last is None: return
    piv = last.groupby(["met", "repthr"])["alive"].mean().unstack()
    say(piv.round(0).to_string())
    rel = (piv.values.max() - piv.values.min()) / piv.values.mean()
    say(f"  σχετικό εύρος χωρητικότητας: {rel*100:.0f}%  "
        f"({'ισχυρή' if rel > .5 else 'μέτρια' if rel > .2 else 'ασθενής'} εξάρτηση)")
    pr = last.groupby(["met", "repthr"])["res"].mean().unstack()
    say("  τελική αντοχή (ίδιο πλέγμα):"); say(pr.round(3).to_string())
    fig, ax = plt.subplots(1, 2, figsize=(11, 4.2))
    for k, (p_, ttl, fmtv) in enumerate([(piv, "Τελικός πληθυσμός", ".0f"), (pr, "Τελική μέση αντοχή", ".2f")]):
        heatmap(fig, ax[k], p_, ttl, fmtv, "reproduction-energy-threshold", "metabolic-rate")
    fig.suptitle("Ευαισθησία στις μεταβολικές σταθερές")
    save(fig, out, "fig11_metabolic_sensitivity.png")
