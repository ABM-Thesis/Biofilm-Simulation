# -*- coding: utf-8 -*-
"""Πείραμα 13-hgt-extended — ενότητα Παρ. Δ — Εικ. Δ.6."""
from core import compare, deco, experiment, fmt_ci, plt, save, say, scatter_means

def run(d, out):
    """[13] Είναι το HGT δομικά κατεσταλμένο στο εκτεταμένο μοντέλο, ή χρειάζεται χαμηλότερο κατώφλι;"""
    _, last = experiment("*13-hgt-extended*table.csv", d, "[13] ΕΚΤΕΤΑΜΕΝΟ ΜΟΝΤΕΛΟ x ΚΑΤΩΦΛΙ HGT — καταστολή ή αναβαθμονόμηση;")
    if last is None: return
    say("  ('ΚΑΘΗΛΩΣΗ' = ποσοστό εκτελέσεων με τελική μέση αντοχή > 0,5· γεγονότα HGT: βλ. [15])")
    xs = sorted(last["trig"].unique())
    pts = [last[last["trig"] == x]["res"].values for x in xs]
    for x, v in zip(xs, pts):
        sub = last[last["trig"] == x]
        frac0 = max(0.0, min(1.0, (0.5 - x) / 0.5))      # ποσοστό αρχικών κυττάρων πάνω από το κατώφλι
        mu = sub["mutations"].mean() if "mutations" in last else float("nan")
        say(f"  Triggerhgt = {x}: αντοχή {fmt_ci(v)} | ΚΑΘΗΛΩΣΗ {(v > 0.5).mean()*100:.0f}% "
            f"| αρχικά κύτταρα >κατωφλίου ~{frac0*100:.0f}% | πληθυσμός {sub['alive'].mean():.0f} | μεταλλάξεις {mu:.0f}")
    if len(pts[0]) > 1 and len(pts[-1]) > 1:
        compare("  αντοχή: χαμηλότερο vs υψηλότερο κατώφλι", pts[0], pts[-1])
    ignites = max((v > 0.5).mean() for v in pts) > 0.5
    say(f"  -> {'καθήλωση σε χαμηλότερο κατώφλι (HGT ενεργό, περιορισμός η σπορά)' if ignites else 'καμία καθήλωση σε κανένα κατώφλι (HGT ενεργό αλλά αναποτελεσματικό, βλ. [15])'}")
    fig, ax = plt.subplots(figsize=(7.5, 4.6))
    scatter_means(ax, xs, pts, [v.mean() for v in pts], "#2ca02c", "Μέση αντοχή (εκτεταμένο)")
    ax.axhline(0.25, ls=":", color="gray", lw=1)
    ax.annotate("αρχικό επίπεδο", (max(xs), 0.27), ha="right", fontsize=8, color="gray")
    deco(ax, "Triggerhgt", "Τελική μέση αντοχή", "Εκτεταμένο μοντέλο: ανάβει το HGT σε χαμηλότερο κατώφλι;", (0, 1.05), {})
    save(fig, out, "fig17_hgt_extended.png")
