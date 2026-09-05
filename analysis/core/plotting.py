# -*- coding: utf-8 -*-
"""Βοηθητικά γραφημάτων: αποθήκευση, ετικέτες, θερμικοί χάρτες, σενάρια strong × hgt."""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from .report import say
from .statistics import fmt_ci

plt.rcParams.update({"figure.dpi": 130, "font.size": 11, "axes.grid": True,
                     "grid.alpha": 0.3, "axes.spines.top": False, "axes.spines.right": False})

# Ετικέτες καθεστώτος (strong-penetration? = True / False)
REG  = lambda s: "ισχυρή διείσδυση" if s else "βασικό καθεστώς"
REG2 = lambda s: "ισχυρή" if s else "βασική"
REG3 = lambda s: "Ισχυρή διείσδυση" if s else "Βασικό καθεστώς"

def save(fig, out, name):
    path = os.path.join(out, name)
    fig.savefig(path, bbox_inches="tight"); plt.close(fig)
    print(f"    -> {path}")

def deco(ax, xlabel=None, ylabel=None, title=None, ylim=None, legend=None, grid=None, **tkw):
    """Ετικέτες αξόνων, τίτλος, όρια και υπόμνημα σε μία κλήση."""
    if xlabel: ax.set_xlabel(xlabel)
    if ylabel: ax.set_ylabel(ylabel)
    if title: ax.set_title(title, **tkw)
    if ylim: ax.set_ylim(*ylim)
    if legend is not None: ax.legend(**legend)
    if grid is not None: ax.grid(alpha=grid)

def heatmap(fig, ax, piv, title, fmt, xlabel, ylabel, fontsize=9, color="w",
            unit_scale=False, cbar_label=None, nan_dash=False, title_fs=None):
    """Θερμικός χάρτης pivot-πίνακα με τις τιμές τυπωμένες στα κελιά."""
    im = ax.imshow(piv.values, origin="lower", aspect="auto", cmap="viridis",
                   **({"vmin": 0, "vmax": 1} if unit_scale else {}))
    ax.set_xticks(range(len(piv.columns))); ax.set_xticklabels(piv.columns)
    ax.set_yticks(range(len(piv.index)));   ax.set_yticklabels(piv.index)
    deco(ax, xlabel, ylabel, title, **({"fontsize": title_fs} if title_fs else {}))
    for i in range(piv.shape[0]):
        for j in range(piv.shape[1]):
            v = piv.values[i, j]
            txt = "—" if nan_dash and np.isnan(v) else format(v, fmt)
            c = color if color else ("white" if v < .6 else "black")
            ax.text(j, i, txt, ha="center", va="center", color=c, fontsize=fontsize)
    fig.colorbar(im, ax=ax, **({"label": cbar_label} if cbar_label else {}))

def errorbars(ax, sub, xcol, ycol, capsize=4, **kw):
    """Μέσος ± SD του ycol ανά τιμή του xcol."""
    g = sub.groupby(xcol)[ycol].agg(["mean", "std"])
    ax.errorbar(g.index, g["mean"], yerr=g["std"], marker="o", capsize=capsize, lw=2, **kw)

def scatter_means(ax, xs, pts, means, color, label):
    """Μεμονωμένες εκτελέσεις (γκρι) + μέσος όρος ανά τιμή παραμέτρου."""
    for x, v in zip(xs, pts):
        ax.plot([x] * len(v), v, "o", color="#888", alpha=.45, ms=5)
    ax.plot(xs, means, "-o", color=color, lw=2, ms=7, label=label)

def scenarios(prefix):
    return [(f"A: {prefix}, HGT on", False, True, "#1f77b4", "-"),
            (f"B: {prefix}, HGT OFF", False, False, "#2ca02c", "--"),
            ("C: Ισχυρή διείσδυση, HGT OFF", True, False, "#d62728", "-"),
            ("D: Ισχυρή διείσδυση, HGT on", True, True, "#ff7f0e", "-.")]

def scenario_summary(last, SC, skip_empty=False):
    """Πληθυσμός/αντοχή ανά σενάριο· επιστρέφει λεξικό {όνομα: υποσύνολο}."""
    G = {}
    for nm, s_, h_, *_ in SC:
        sub = last[(last["strong"] == s_) & (last["hgt"] == h_)]
        G[nm] = sub
        if skip_empty and sub.empty: continue
        mu = f" | μεταλλάξεις {sub['mutations'].mean():.0f}" if "mutations" in sub else ""
        say(f"  {nm:32s} πληθυσμός {fmt_ci(sub['alive'],0)} | αντοχή {fmt_ci(sub['res'])}{mu}")
    return G

def scenario_timeseries(df, SC, out, name, suptitle=None):
    """Δύο πάνελ (πληθυσμός, αντοχή) με μέσο ± SD ανά σενάριο."""
    fig, ax = plt.subplots(1, 2, figsize=(12, 4.6))
    for nm, s_, h_, c, ls in SC:
        sub = df[(df["strong"] == s_) & (df["hgt"] == h_)]
        if sub.empty: continue
        for k, col in enumerate(["alive", "res"]):
            g = sub.groupby("step")[col]; m, sd = g.mean(), g.std()
            ax[k].plot(m.index, m, color=c, linestyle=ls, lw=2, label=nm)
            ax[k].fill_between(m.index, m - sd, m + sd, color=c, alpha=.15)
    deco(ax[0], "ticks", title="Ζωντανός πληθυσμός", legend={"fontsize": 8})
    deco(ax[1], "ticks", title="Μέση αντοχή", ylim=(0, 1.05), legend={"fontsize": 8})
    if suptitle: fig.suptitle(suptitle)
    save(fig, out, name)

def extremes(last, mask, pcol, ycol, lo=0):
    """Τιμές του ycol στο χαμηλότερο (lo) και στο μέγιστο επίπεδο της παραμέτρου pcol."""
    a = last[(last[pcol] == lo) & mask][ycol].values
    b = last[(last[pcol] == last[pcol].max()) & mask][ycol].values
    return a, b
