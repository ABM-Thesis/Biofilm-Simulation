# -*- coding: utf-8 -*-
"""Πείραμα 1 + 5 + 11 — ενότητα 4.7 — Εικ. 4.3 (σύγκριση με μοντέλα αναφοράς)."""
from core import (REG2, deco, finals, find, fit_decay_length, fit_logistic, load, logistic,
                  penetration_depth_theory, plt, save, say)

def run(base_df, wm_df, out, args):
    say("\n[Σ] ΣΥΓΚΡΙΣΗ ΜΕ ΑΝΕΞΑΡΤΗΤΑ ΜΟΝΤΕΛΑ ΑΝΑΦΟΡΑΣ")
    # (α) αναλυτικό βάθος διείσδυσης
    say("  (α) Αναλυτική λύση αντίδρασης-διάχυσης  λ = sqrt(D/k),  D = 0.375·rate,  k = -ln(decay)")
    for nm, r_, dec in [("βασικό (rate 0.2, decay 0.95)", args.base_diffusion, args.base_decay),
                        ("ισχυρή διείσδυση (rate 0.9, decay 0.999)", 0.9, 0.999)]:
        say(f"      {nm}: λ_θεωρία = {penetration_depth_theory(r_, dec):.2f} patches "
            f"(το βιοφίλμ βρίσκεται ~{args.biofilm_depth:.0f} patches από την πηγή)")
    lam_b = penetration_depth_theory(args.base_diffusion, args.base_decay)
    say(f"      -> βασικό καθεστώς: λ ≈ {lam_b:.1f} << {args.biofilm_depth:.0f} (μηδενική έκθεση στη βάση)")

    if wm_df is not None and {"band1","band2","band3","band4"} <= set(wm_df.columns):   # μετρημένο προφίλ
        sub = finals(wm_df)
        sub = sub[~sub["wm"]] if "wm" in sub.columns else sub
        for s_ in sorted(sub["strong"].unique()) if "strong" in sub.columns else [None]:
            ss = sub[sub["strong"] == s_] if s_ is not None else sub
            conc = [ss[b].mean() for b in ("band1", "band2", "band3", "band4")]
            lam_fit, r2 = fit_decay_length([28.5, 20.5, 12.5, 4.0], conc)     # απόσταση από την πηγή
            lam_th = penetration_depth_theory(0.9 if s_ else args.base_diffusion, 0.999 if s_ else args.base_decay)
            say(f"      μετρημένο προφίλ ({REG2(s_)}): λ_προσαρμογή = {lam_fit:.2f} "
                f"(R² = {r2:.3f}) έναντι λ_θεωρία = {lam_th:.2f}")

    # (β) λογιστικό μοντέλο
    if base_df is None: return
    g = base_df.groupby("step")["alive"].mean()
    t, N = g.index.values.astype(float), g.values.astype(float)
    p, r2 = fit_logistic(t, N)
    if p is None: return
    K, r_, N0 = p
    say(f"  (β) Κλασικό λογιστικό μοντέλο dN/dt = rN(1-N/K): K = {K:.0f} κύτταρα, "
        f"r = {r_:.4f} /tick, R² = {r2:.4f}")
    f11 = find("*11-full-model*table.csv", args.data_dir)          # το ίδιο fit στο ΕΚΤΕΤΑΜΕΝΟ
    if f11:
        d11 = load(f11)
        sub = d11[(~d11["strong"]) & (d11["hgt"])]
        if not sub.empty:
            g2 = sub.groupby("step")["alive"].mean()
            N2 = g2.values.astype(float)
            _, r2b = fit_logistic(g2.index.values.astype(float), N2)
            say(f"      το ΙΔΙΟ fit στο εκτεταμένο μοντέλο: R² = {r2b:.4f}")
            say(f"      -> υπερακόντιση στο εκτεταμένο: κορυφή {N2.max():.0f} -> ισορροπία {N2[-1]:.0f}")
    fig, ax = plt.subplots(figsize=(7, 4.2))
    ax.plot(t, N, lw=2, label="ABM (μέσος όρος)")
    ax.plot(t, logistic(t, *p), "--", lw=2, label=f"Λογιστικό μοντέλο (R²={r2:.3f})")
    deco(ax, "ticks", "Ζωντανά κύτταρα", "Σύγκριση ABM με κλασικό λογιστικό μοντέλο", legend={})
    save(fig, out, "fig14_model_comparison.png")
