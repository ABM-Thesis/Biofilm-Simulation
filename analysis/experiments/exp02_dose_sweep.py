# -*- coding: utf-8 -*-
"""Πείραμα 2-antibiotic-dose-sweep — ενότητα 4.3 — σάρωση δόσης, TOST ισοδυναμίας."""
from scipy import stats
from core import ci95, deco, experiment, plt, save, say, tost_report

def run(d, out):
    _, last = experiment("*2-antibiotic-dose*table.csv", d, "[2] ΣΑΡΩΣΗ ΔΟΣΗΣ — ισχύει ο ισχυρισμός 'καμία επίδραση';")
    if last is None: return
    lv = sorted(last["dose"].unique())
    for col, lbl in [("ab", "αντιβιοτικό"), ("alive", "πληθυσμός"), ("res", "αντοχή")]:
        groups = [last[last["dose"] == L][col].values for L in lv]
        H, p = stats.kruskal(*groups)
        say(f"  {lbl}: Kruskal-Wallis H = {H:.2f}, p = {p:.4g}"
            f"  ->  {'ΔΙΑΦΕΡΕΙ' if p < .05 else 'δεν ανιχνεύεται διαφορά'}")
        say("      " + " | ".join(f"δόση {L}: {ci95(g)[0]:.3f}" for L, g in zip(lv, groups)))
    a = last[last["dose"] == lv[0]]["alive"].values
    b = last[last["dose"] == lv[-1]]["alive"].values
    p_eq, diff = tost_report(a, b, f"δόση {lv[0]} vs {lv[-1]}", " κύτταρα")
    say(f"      διαφορά = {diff:.1f} κύτταρα, p = {p_eq:.4g}  ->  "
        f"{'ΙΣΟΔΥΝΑΜΑ (τεκμηριωμένη απουσία επίδρασης)' if p_eq < .05 else 'μη τεκμηριωμένη ισοδυναμία'}")

    dg = last.groupby("dose").agg(alive=("alive","mean"), alive_sd=("alive","std"),
                                  res=("res","mean"), res_sd=("res","std"),
                                  ab=("ab","mean"), ab_sd=("ab","std"))
    x = [str(v) for v in dg.index.values]
    fig, axs = plt.subplots(1, 3, figsize=(12, 3.8))
    for ax, (col, sd, c, ttl) in zip(axs, [("ab","ab_sd","tab:orange","Μέσο περιβαλλοντικό αντιβιοτικό"),
                                           ("alive","alive_sd","tab:blue","Τελικός ζωντανός πληθυσμός"),
                                           ("res","res_sd","tab:green","Τελική μέση αντοχή")]):
        ax.bar(x, dg[col], yerr=dg[sd], color=c, capsize=3)
        deco(ax, "Πάχος πηγής (σειρές)", title=ttl)
    fig.suptitle("Σάρωση δόσης: η διείσδυση αυξάνεται, ο πληθυσμός δεν μεταβάλλεται")
    save(fig, out, "fig6_dose_sweep.png")
