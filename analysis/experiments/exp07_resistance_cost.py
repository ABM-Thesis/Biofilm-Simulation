# -*- coding: utf-8 -*-
"""Πείραμα 7-resistance-cost — ενότητα 4.5 — Εικ. 4.6 (κόστος αντοχής)."""
from core import (REG, REG2, REG3, compare, deco, experiment, extremes, fmt_ci, monotonicity_check,
                  plt, save, say)

def run(d, out):
    df, last = experiment("*7-resistance-cost*table.csv", d, "[7] ΚΟΣΤΟΣ ΑΝΤΟΧΗΣ — είναι η καθήλωση αναπόφευκτη;")
    if df is None: return
    regimes = sorted(last["strong"].unique())
    for s_ in regimes:
        say(f"  -- {REG(s_)} --"); mask = last["strong"] == s_
        for c in sorted(last["cost"].unique()):
            sub = last[(last["cost"] == c) & mask]
            if sub.empty: continue
            say(f"    cost = {c}: αντοχή {fmt_ci(sub['res'])} | πληθυσμός {fmt_ci(sub['alive'],0)}")
        a, b = extremes(last, mask, "cost", "res")
        if len(a) > 1 and len(b) > 1:
            compare(f"    αντοχή: μηδενικό vs μέγιστο κόστος ({REG2(s_)})", a, b)
        for col, lbl in [("res", "αντοχή"), ("alive", "πληθυσμός")]:
            gp = last[mask].groupby("cost")[col].mean()
            monotonicity_check(gp.index.values, gp.values, f"κόστος -> {lbl}, {REG2(s_)}")
    fig, ax = plt.subplots(1, 2, figsize=(12, 4.4))
    for k, s_ in enumerate(regimes):
        for c in sorted(df["cost"].unique()):
            sub = df[(df["cost"] == c) & (df["strong"] == s_)]
            if sub.empty: continue
            g = sub.groupby("step")["res"]
            ax[k].plot(g.mean().index, g.mean(), lw=2, label=f"cost={c}")
        deco(ax[k], "ticks", "Μέση αντοχή", REG3(s_), (0, 1.05), {"fontsize": 8})
    fig.suptitle("Με κόστος αντοχής η καθήλωση παύει να είναι αναπόφευκτη")
    save(fig, out, "fig10_resistance_cost.png")
