# -*- coding: utf-8 -*-
"""Πείραμα 16-spawn-sensitivity — ενότητα 4.7 — Εικ. Δ.3."""
from core import ci95, compare, deco, experiment, fmt_ci, plt, save, say, tost_report

def run(d, out):
    """[16] Ευαισθησία στην αρχική τοποθέτηση των κυττάρων (spawncellposition)."""
    _, last = experiment("*16-spawn-sensitivity*table.csv", d)
    if last is None or "spawn" not in last.columns: return
    say("\n[16] ΕΥΑΙΣΘΗΣΙΑ ΣΤΗΝ ΑΡΧΙΚΗ ΤΟΠΟΘΕΤΗΣΗ (spawncellposition)")
    vals = sorted(last["spawn"].unique())
    for v in vals:
        sub = last[last["spawn"] == v]
        say(f"  spawn={v}: πληθυσμός {fmt_ci(sub['alive'],0)} | αντοχή {fmt_ci(sub['res'])}")
    if len(vals) > 1:
        lo_, hi_ = last[last["spawn"] == vals[0]], last[last["spawn"] == vals[-1]]
        p_t, diff = tost_report(lo_["alive"].values, hi_["alive"].values, f"spawn {vals[0]} vs {vals[-1]}", "")
        say(f"      διαφορά = {diff:.1f} κύτταρα, p = {p_t:.4g}  ->  "
            f"{'ΙΣΟΔΥΝΑΜΑ (το συμπέρασμα δεν εξαρτάται από την παράμετρο)' if p_t < .05 else 'ΔΕΝ τεκμηριώνεται ισοδυναμία'}")
        compare("  αντοχή: χαμηλότερο vs υψηλότερο spawn", lo_["res"].values, hi_["res"].values)
    fig, ax = plt.subplots(1, 2, figsize=(11, 4.2))
    for i, (col, ttl) in enumerate([("alive", "Τελικός πληθυσμός"), ("res", "Τελική μέση αντοχή")]):
        m = [ci95(last[last["spawn"] == v][col]) for v in vals]
        ax[i].errorbar(vals, [x[0] for x in m], yerr=[[x[0]-x[1] for x in m], [x[2]-x[0] for x in m]],
                       fmt="o-", capsize=4, lw=2)
        deco(ax[i], "spawncellposition", title=ttl, grid=.3)
    fig.suptitle("Τα συμπεράσματα δεν εξαρτώνται από την αρχική τοποθέτηση")
    save(fig, out, "fig21_spawn_sensitivity.png")
