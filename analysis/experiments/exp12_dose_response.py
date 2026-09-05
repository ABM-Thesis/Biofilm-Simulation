# -*- coding: utf-8 -*-
"""Πείραμα 12-fullmodel-doseresponse — ενότητα Παρ. Δ — Εικ. Δ.5."""
from scipy import stats
from core import deco, errorbars, experiment, fmt_ci, plt, save, say

def run(d, out):
    _, last = experiment("*12-fullmodel-dose*table.csv", d,
                         "[12] ΠΛΗΡΕΣ ΜΟΝΤΕΛΟ — δοσο-απόκριση (πού ασκείται επιλογή χωρίς εξαφάνιση;)")
    if last is None: return
    lv = sorted(last["srcconc"].unique())
    for h in [True, False]:
        say(f"  -- HGT {'ενεργό' if h else 'ανενεργό'} --")
        for c in lv:
            sub = last[(last["srcconc"] == c) & (last["hgt"] == h)]
            if sub.empty: continue
            mu = f" | μεταλλ. {sub['mutations'].mean():.0f}" if "mutations" in sub else ""
            say(f"    πηγή = {c}: πληθυσμός {fmt_ci(sub['alive'],0)} | αντοχή {fmt_ci(sub['res'])} "
                f"| επιβίωσαν {(sub['alive'] > 0).mean()*100:.0f}% | αντιβ. βάσης {sub['ab_base'].mean():.3f}{mu}")
    say("  -- εξελικτική διάσωση (ποσοστό εκτελέσεων που επιβίωσαν) --")
    for c in lv:
        a = last[(last["srcconc"] == c) & (last["hgt"])]["alive"]
        b = last[(last["srcconc"] == c) & (~last["hgt"])]["alive"]
        if len(a) < 2 or len(b) < 2: continue
        ta, tb = int((a > 0).sum()), int((b > 0).sum())
        if ta == len(a) and tb == len(b): continue          # και τα δύο 100%, τίποτα να ελεγχθεί
        p = stats.fisher_exact([[ta, len(a) - ta], [tb, len(b) - tb]], alternative="two-sided")[1]
        verdict = ("ΔΙΑΣΩΣΗ από HGT" if p < .05 and ta > tb else
                   "ΑΝΤΙΣΤΡΟΦΗ: το HGT ΜΕΙΩΝΕΙ την επιβίωση" if p < .05 and tb > ta else
                   "καμία σημαντική διαφορά (η φορά είναι ΑΝΤΙΘΕΤΗ της διάσωσης)" if tb > ta else
                   "καμία σημαντική διαφορά")
        say(f"    πηγή = {c}: HGT on {ta}/{len(a)} vs off {tb}/{len(b)} | Fisher p = {p:.4f} -> {verdict}")

    fig, ax = plt.subplots(1, 2, figsize=(12, 4.4))
    for h, c_ in [(True, "#ff7f0e"), (False, "#d62728")]:
        sub = last[last["hgt"] == h]
        if sub.empty: continue
        for k, col in enumerate(["alive", "res"]):
            errorbars(ax[k], sub, "srcconc", col, color=c_, label=f"HGT {'on' if h else 'off'}")
    deco(ax[0], "source-concentration", "Τελικός πληθυσμός", legend={})
    deco(ax[1], "source-concentration", "Τελική μέση αντοχή", ylim=(0, 1.05), legend={})
    fig.suptitle("Πλήρες μοντέλο: δοσο-απόκριση")
    save(fig, out, "fig16_dose_response.png")
