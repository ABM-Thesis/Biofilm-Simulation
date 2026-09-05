# -*- coding: utf-8 -*-
"""Πείραμα 5a/5b-wellmixed — ενότητα 4.3 — Εικ. 4.2 (έλεγχος χωρικής δομής)."""
import numpy as np
from core import compare, deco, experiment, fmt_ci, plt, save, say

def run(d, out):
    R, dfs = {}, []
    for pat, lab in [("*5a-wellmixed*table.csv", "Βασική δόση"), ("*5b-wellmixed*table.csv", "Ισχυρή διείσδυση")]:
        df, last = experiment(pat, d)
        if df is None: continue
        dfs.append(df)
        if not R: say("\n[5] ΕΛΕΓΧΟΣ ΧΩΡΙΚΗΣ ΔΟΜΗΣ (ισοδοσικός: ίδια μέση συγκέντρωση)")
        for wm in [False, True]:
            sub = last[last["wm"] == wm]
            if sub.empty: continue
            say(f"  {lab} / {'ΟΜΟΙΟΜΟΡΦΟ' if wm else 'με δομή':10s}: πληθυσμός {fmt_ci(sub['alive'],0)} "
                f"| μέσο αντιβιοτικό {sub['ab'].mean():.3f} | στη βάση {sub['ab_base'].mean():.3f}")
            R[(lab, wm)] = (sub["alive"].mean(), sub["alive"].std())
        a_ = last[~last["wm"]]["alive"].values; b_ = last[last["wm"]]["alive"].values
        if len(a_) and len(b_):
            gm, wmm = last[~last['wm']]['ab'].mean(), last[last['wm']]['ab'].mean()
            note_ = "" if abs(gm - wmm) < 0.05 else f"  [ΠΡΟΣΟΧΗ: δόσεις {gm:.2f} vs {wmm:.2f} - ΜΗ ισοδοσικό]"
            compare(f"  δομή vs ομοιόμορφο ({lab})", a_, b_, note_)
    if R:
        fig, ax = plt.subplots(figsize=(7.5, 4.6))
        labs = sorted(set(k[0] for k in R), reverse=True)
        x = np.arange(len(labs)); w = .35
        val = lambda wm, i: [R.get((L, wm), (0, 0))[i] for L in labs]
        ax.bar(x - w/2, val(False, 0), w, yerr=val(False, 1), capsize=4, label="Με χωρική δομή", color="#1f77b4")
        ax.bar(x + w/2, val(True, 0), w, yerr=val(True, 1), capsize=4, label="Χωρίς δομή (ομοιόμορφο)", color="#d62728")
        ax.set_xticks(x); ax.set_xticklabels(labs)
        deco(ax, ylabel="Ζωντανά κύτταρα (τελικό)", title="Έλεγχος χωρικής δομής (ισοδοσικός)", legend={})
        save(fig, out, "fig8_spatial_control.png")
    return dfs[0] if dfs else None
