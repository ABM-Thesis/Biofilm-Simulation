# -*- coding: utf-8 -*-
"""Πείραμα 1-baseline-replicates — ενότητα 4.2 — Εικ. 4.1 (πληθυσμιακή δυναμική)."""
from core import deco, experiment, fmt_ci, plt, save, say

def run(d, out):
    df, last = experiment("*1-baseline*table.csv", d, "[1] ΒΑΣΙΚΟ ΣΕΝΑΡΙΟ (baseline)")
    if df is None: return None
    for lbl, col in [("τελικός πληθυσμός", "alive"), ("τελική μέση αντοχή", "res"),
                     ("μέσο περιβαλλοντικό αντιβιοτικό", "ab"), ("μεταλλάξεις (σωρευτικά)", "mutations")]:
        if col in last: say(f"  {lbl}: {fmt_ci(last[col])}")
    g = df.groupby("step"); m, s = g.mean(numeric_only=True), g.std(numeric_only=True)
    t = m.index.values
    fig, ax = plt.subplots(figsize=(7, 4.2))
    for col, c, lab in [("alive", "tab:blue", "Ζωντανά"), ("dead", "tab:red", "Νεκρά (σωρευτικά)")]:
        ax.plot(t, m[col], color=c, label=lab); ax.fill_between(t, m[col]-s[col], m[col]+s[col], color=c, alpha=.2)
    deco(ax, "Χρόνος (ticks)", "Αριθμός κυττάρων", "Πληθυσμιακή δυναμική (μέσος όρος ± SD)", legend={})
    save(fig, out, "fig1_population.png")

    fig, ax = plt.subplots(figsize=(7, 4.2))
    ax.plot(t, m["res"], color="tab:green", lw=2, label="Μέση αντοχή")
    ax.fill_between(t, m["res"]-s["res"], m["res"]+s["res"], color="tab:green", alpha=.2, label="± SD")
    deco(ax, "Χρόνος (ticks)", "Μέση αντοχή", "Εξέλιξη μέσης αντοχής", (0, 1.05), {"loc": "lower right"})
    save(fig, out, "fig2_resistance.png")
    return df
