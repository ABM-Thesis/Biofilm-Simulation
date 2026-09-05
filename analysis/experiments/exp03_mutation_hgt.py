# -*- coding: utf-8 -*-
"""Πείραμα 3-mutation-hgt-sensitivity — ενότητα 4.4 — μετάλλαξη × κατώφλι HGT."""
from core import deco, errorbars, experiment, heatmap, plt, save, say

def run(d, out):
    _, last = experiment("*3-mutation-hgt*table.csv", d, "[3] ΕΥΑΙΣΘΗΣΙΑ: μετάλλαξη × κατώφλι HGT")
    if last is None: return
    piv = last.groupby(["mut", "trig"])["res"].mean().unstack()
    say(piv.round(3).to_string())
    fig, ax = plt.subplots(figsize=(6.2, 4.6))
    heatmap(fig, ax, piv, "Τελική μέση αντοχή", ".2f", "Triggerhgt", "mutation-chance",
            fontsize=10, color=None, unit_scale=True, cbar_label="μέση αντοχή")
    save(fig, out, "fig4_sensitivity_heatmap.png")

    fig, ax = plt.subplots(figsize=(8, 4.8))
    for mm in sorted(last["mut"].unique()):
        errorbars(ax, last[last["mut"] == mm], "trig", "res", capsize=3, label=f"mut={mm}")
    deco(ax, "Triggerhgt", "Τελική μέση αντοχή", "Σημείο ανατροπής: η αντοχή εκτοξεύεται μόνο\nαν το κατώφλι HGT είναι προσβάσιμο",
         (0, 1.08), {"title": "mutation-chance", "loc": "center left"}, fontsize=12)
    fig.subplots_adjust(top=.86)
    save(fig, out, "fig5_tipping_point.png")
