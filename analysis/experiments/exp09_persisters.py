# -*- coding: utf-8 -*-
"""Πείραμα 9-persisters — ενότητα 4.5 — Εικ. Δ.1."""
from core import (REG, REG2, REG3, compare, deco, errorbars, experiment, extremes, fmt_ci,
                  monotonicity_check, plt, save, say)

def run(d, out):
    _, last = experiment("*9-persisters*table.csv", d, "[9] PERSISTERS (φαινοτυπική ανοχή)")
    if last is None: return
    regimes = sorted(last["strong"].unique())
    for s_ in regimes:
        say(f"  -- {REG(s_)} --"); mask = last["strong"] == s_
        for p_ in sorted(last["psw"].unique()):
            sub = last[(last["psw"] == p_) & mask]
            if sub.empty: continue
            dm = f" | αδρανή {sub['dormant'].mean():.0f}" if "dormant" in sub else ""
            say(f"    switch-prob = {p_}: πληθυσμός {fmt_ci(sub['alive'],0)}{dm}")
        a, b = extremes(last, mask, "psw", "alive")
        if len(a) > 1 and len(b) > 1:
            compare(f"    επιβίωση: χωρίς vs με persisters ({REG2(s_)})", a, b)
        gp = last[mask].groupby("psw")["alive"].mean()      # μονοτονία σε ΟΛΟ το εύρος
        monotonicity_check(gp.index.values, gp.values, f"persisters, {REG2(s_)}")
    fig, ax = plt.subplots(figsize=(7.5, 4.4))
    for s_ in regimes:
        errorbars(ax, last[last["strong"] == s_], "psw", "alive", label=REG3(s_))
    deco(ax, "persister-switch-prob", "Τελικός ζωντανός πληθυσμός", "Συνεισφορά των persisters στην επιβίωση", legend={})
    save(fig, out, "fig12_persisters.png")
