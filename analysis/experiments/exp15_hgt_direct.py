# -*- coding: utf-8 -*-
"""Πείραμα 15a/15b-hgt-direct — ενότητα 4.6 — Εικ. 4.9 (άμεση μέτρηση HGT)."""
import numpy as np
from core import deco, experiment, fmt_ci, plt, save, say

def run(d, out):
    """[15] ΑΜΕΣΗ μέτρηση των γεγονότων HGT (hgt-count), αντί για έμμεση εκτίμηση από την αντοχή."""
    say("\n[15] ΑΜΕΣΗ ΜΕΤΡΗΣΗ ΓΕΓΟΝΟΤΩΝ HGT (hgt-count)")
    panels = []
    for pat, lbl in [("*15a-hgt-direct-minimal*table.csv", "ελάχιστο μοντέλο"),
                     ("*15b-hgt-direct-extended*table.csv", "εκτεταμένο μοντέλο")]:
        _, last = experiment(pat, d)
        if last is None: continue
        if "hgtn" not in last.columns:
            say(f"  [{lbl}] λείπει η στήλη hgt-count"); continue
        say(f"  -- {lbl} --")
        rows = []
        for (trig, hgt), sub in last.groupby(["trig", "hgt"]):
            n_ev, nz = sub["hgtn"].mean(), 100.0 * (sub["hgtn"] > 0).mean()
            frac = sub["fres"].mean() if "fres" in sub else np.nan
            say(f"    Triggerhgt={trig} HGT={'on ' if hgt else 'off'}: "
                f"γεγονότα HGT {n_ev:>9.1f} | εκτελέσεις με >0 γεγονότα {nz:>5.1f}% "
                f"| ποσοστό ανθεκτικών {frac:.3f} | αντοχή {fmt_ci(sub['res'])}")
            rows.append((trig, hgt, n_ev, nz, frac))
        off = last[~last["hgt"]]["hgtn"]                     # με HGT off ΠΡΕΠΕΙ να είναι ακριβώς 0
        if len(off):
            say(f"    έλεγχος ακεραιότητας: με hgt-enabled?=false τα γεγονότα είναι 0 -> "
                f"{'ΝΑΙ' if (off == 0).all() else 'ΟΧΙ (ΣΦΑΛΜΑ ΜΟΝΤΕΛΟΥ)'}")
        panels.append((lbl, rows))

    if not panels: return
    fig, ax = plt.subplots(1, len(panels), figsize=(6 * len(panels), 4.2), squeeze=False)
    for k, (lbl, rows) in enumerate(panels):
        on = sorted([r for r in rows if r[1]])
        if on:
            ax[0][k].plot([r[0] for r in on], [max(r[2], 0.1) for r in on], "o-", color="#d62728", lw=2)
        ax[0][k].set_yscale("log")
        deco(ax[0][k], "Triggerhgt", "γεγονότα HGT (log)", lbl, grid=.3)
    fig.suptitle("Άμεση μέτρηση HGT: ελάχιστο vs εκτεταμένο μοντέλο")
    save(fig, out, "fig20_hgt_direct.png")
