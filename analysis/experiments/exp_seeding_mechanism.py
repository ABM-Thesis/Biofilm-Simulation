# -*- coding: utf-8 -*-
"""Πείραμα 4 + 11 — ενότητα 4.6 — μηχανισμός: γιατί σβήνει η HGT."""
from core import finals, find, load, plt, save, say

def run(d, out):
    """Τεκμηρίωση του μηχανισμού: γιατί σβήνει το HGT στο εκτεταμένο μοντέλο."""
    f4, f11 = find("*4-strong-penetration*table.csv", d), find("*11-full-model*table.csv", d)
    if not (f4 and f11): return
    say("\n[Μ] ΜΗΧΑΝΙΣΜΟΣ: γιατί δεν πυροδοτείται το HGT στο εκτεταμένο μοντέλο")
    rows = []
    for f, lab in [(f4, "ελάχιστο"), (f11, "εκτεταμένο")]:
        df = load(f)
        base = df[(~df["strong"]) & (df["hgt"])]                 # βασικό φάρμακο, HGT ενεργό
        if base.empty or "mutations" not in base: continue
        last = finals(base)
        ct = base.groupby("run")["alive"].sum()                  # κυτταρο-βήματα = ολοκλήρωμα πληθυσμού
        mu = last.set_index("run")["mutations"]
        common = ct.index.intersection(mu.index)
        rate = 1000 * mu[common] / ct[common]                    # μεταλλάξεις ανά 1000 κυτταρο-βήματα
        rows.append((lab, last["alive"].mean(), mu.mean(), ct.mean(), rate.mean()))
        say(f"  {lab:11s}: πληθυσμός {last['alive'].mean():6.0f} | μεταλλάξεις {mu.mean():6.0f} "
            f"| κυτταρο-βήματα {ct.mean():10.0f} | ρυθμός {rate.mean():.3f} /1000 κυτταρο-βήματα")
    if len(rows) == 2:
        (_, p1, m1, c1, r1), (_, p2, m2, c2, r2) = rows
        say(f"  -> ο πληθυσμός είναι {p1/max(p2,1):.1f}x μικρότερος στο εκτεταμένο")
        say(f"  -> οι ΣΥΝΟΛΙΚΕΣ μεταλλάξεις είναι {m1/max(m2,1):.1f}x λιγότερες")
        say(f"  -> ο ρυθμός ΑΝΑ κυτταρο-βήμα είναι ουσιαστικά ίδιος ({r1:.3f} vs {r2:.3f})")
        fig, ax = plt.subplots(1, 3, figsize=(12, 3.8))
        labs = [r[0] for r in rows]
        for k, (vals, ttl) in enumerate([([r[1] for r in rows], "Τελικός πληθυσμός"),
                                         ([r[2] for r in rows], "Συνολικές μεταλλάξεις"),
                                         ([r[4] for r in rows], "Μεταλλάξεις ανά\n1000 κυτταρο-βήματα")]):
            ax[k].bar(labs, vals, color=["#1f77b4", "#ff7f0e"]); ax[k].set_title(ttl)
            for i, v in enumerate(vals):
                ax[k].text(i, v, f"{v:.3g}", ha="center", va="bottom", fontsize=9)
        fig.suptitle("Ο περιορισμός δεν είναι η μεταλλαξιγένεση αλλά ο αριθμός ευκαιριών")
        save(fig, out, "fig18_seeding.png")
