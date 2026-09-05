# -*- coding: utf-8 -*-
"""Στατιστικά εργαλεία: bootstrap ΔΕ, Cliff's δ, Holm, TOST, μονοτονία, μοντέλα αναφοράς."""
import numpy as np
from scipy import stats, optimize
from .report import say

def ci95(x, boot=True, n_boot=5000, seed=0):
    """Bootstrap percentile 95% ΔΕ (το t-ΔΕ δίνει αρνητικά όρια σε πληθυσμούς με μάζα στο μηδέν)."""
    x = np.asarray(x, float); x = x[~np.isnan(x)]
    if len(x) == 0: return np.nan, np.nan, np.nan
    m, n = x.mean(), len(x)
    if n < 2: return m, m, m
    if not boot:
        h = stats.t.ppf(0.975, n - 1) * x.std(ddof=1) / np.sqrt(n)
        return m, m - h, m + h
    means = np.random.default_rng(seed).choice(x, (n_boot, n), replace=True).mean(axis=1)
    lo, hi = np.percentile(means, [2.5, 97.5])
    return m, lo, hi

def fmt_ci(x, dec=3):
    m, lo, hi = ci95(x)
    return f"{m:.{dec}f} [95% ΔΕ {lo:.{dec}f}, {hi:.{dec}f}]"

def cliffs_delta(a, b, n_boot=2000, seed=0):
    """Μέγεθος επίδρασης Cliff's delta + bootstrap 95% ΔΕ."""
    a, b = np.asarray(a, float), np.asarray(b, float)
    def d(x, y):
        gt = sum((xi > y).sum() for xi in x); lt = sum((xi < y).sum() for xi in x)
        return (gt - lt) / (len(x) * len(y))
    est = d(a, b)
    rng = np.random.default_rng(seed)
    boot = [d(rng.choice(a, len(a), True), rng.choice(b, len(b), True)) for _ in range(n_boot)]
    lo, hi = np.percentile(boot, [2.5, 97.5])
    mag = ("αμελητέο" if abs(est) < .147 else "μικρό" if abs(est) < .33
           else "μέτριο" if abs(est) < .474 else "μεγάλο")
    return est, lo, hi, mag

def holm(pvals):
    """Διόρθωση Holm-Bonferroni για πολλαπλές συγκρίσεις."""
    p = np.asarray(pvals, float); order = np.argsort(p); m = len(p)
    adj = np.empty(m); run_max = 0.0
    for rank, idx in enumerate(order):
        run_max = max(run_max, (m - rank) * p[idx])
        adj[idx] = min(1.0, run_max)
    return adj

def tost(a, b, bound):
    """Έλεγχος ισοδυναμίας TOST. Επιστρέφει (p, διαφορά). p < 0.05 => ΙΣΟΔΥΝΑΜΕΣ εντός ±bound."""
    a, b = np.asarray(a, float), np.asarray(b, float)
    d = a.mean() - b.mean()
    va, vb, na, nb = a.var(ddof=1), b.var(ddof=1), len(a), len(b)
    se = np.sqrt(va / na + vb / nb)
    if se == 0: return (0.0 if abs(d) < bound else 1.0), d
    dof = (va / na + vb / nb) ** 2 / ((va / na) ** 2 / (na - 1) + (vb / nb) ** 2 / (nb - 1))
    p1 = 1 - stats.t.cdf((d + bound) / se, dof)     # H0: d <= -bound
    p2 = stats.t.cdf((d - bound) / se, dof)         # H0: d >= +bound
    return max(p1, p2), d

def tost_report(a, b, what, unit_note):
    """TOST με όριο ±5% του μέσου πληθυσμού· τυπώνει δύο γραμμές αναφοράς."""
    bound = 0.05 * np.nanmean(np.concatenate([a, b]))
    p_eq, diff = tost(a, b, bound)
    say(f"  TOST ισοδυναμίας πληθυσμού ({what}, όριο ±5% = ±{bound:.0f}{unit_note}):")
    return p_eq, diff

def compare(name, a, b, alpha_note="", unit=""):
    """Mann-Whitney + Cliff's delta + απόλυτη διαφορά. Επιστρέφει το p."""
    a = np.asarray(a, float); a = a[~np.isnan(a)]
    b = np.asarray(b, float); b = b[~np.isnan(b)]
    if len(a) < 2 or len(b) < 2:
        say(f"  {name}: πολύ λίγες εκτελέσεις"); return 1.0
    p = stats.mannwhitneyu(a, b, alternative="two-sided").pvalue
    est, lo, hi, mag = cliffs_delta(a, b)
    d_abs, bm = a.mean() - b.mean(), b.mean()
    # σχετική διαφορά μόνο όταν η βάση είναι ουσιωδώς μη μηδενική
    rel = f", {100 * d_abs / bm:+.1f}%" if abs(bm) > 1e-9 and abs(d_abs / bm) < 10 else ""
    say(f"  {name}: Mann-Whitney p = {p:.5f} | Cliff's δ = {est:+.2f} "
        f"[{lo:+.2f}, {hi:+.2f}] ({mag}) | διαφορά μέσων = {d_abs:+.3g}{unit}{rel} {alpha_note}")
    return p

def monotonicity_check(xs, ys, label, indent="    "):
    """Είναι η απόκριση μονότονη ως προς την παράμετρο; (Spearman + αλλαγές φοράς)"""
    xs = np.asarray(xs, float); ys = np.asarray(ys, float)
    ok = np.isfinite(xs) & np.isfinite(ys)
    xs, ys = xs[ok], ys[ok]
    if len(xs) < 3: return None
    rho, p_s = stats.spearmanr(xs, ys)
    d = np.diff(ys)
    mono = bool(np.all(d >= 0) or np.all(d <= 0))
    viol = int(np.sum(np.sign(d[:-1]) * np.sign(d[1:]) < 0))
    say(f"{indent}έλεγχος μονοτονίας ({label}): Spearman rho = {rho:+.2f}, p = {p_s:.4g} | "
        f"{'ΜΟΝΟΤΟΝΗ' if mono else f'ΜΗ ΜΟΝΟΤΟΝΗ ({viol} αλλαγές φοράς)'}")
    if not mono:
        strong_trend = abs(rho) >= 0.8 and p_s < 0.05 and viol <= 1
        say(f"{indent}  -> {'ισχυρή μονότονη ΤΑΣΗ με μία τοπική εξαίρεση' if strong_trend else 'ΚΑΜΙΑ συνεπής τάση'}")
    return mono

def penetration_depth_theory(diffusion_rate, decay):
    """λ = sqrt(D/k) για αντίδραση-διάχυση σε σταθερή κατάσταση. Στο NetLogo το
    `diffuse r` δίνει D_eff = 0.375 r (patch²/tick)· η αποδόμηση ανά tick k = -ln(decay)."""
    D, k = 0.375 * diffusion_rate, -np.log(decay)
    return np.inf if k <= 0 else np.sqrt(D / k)

def fit_decay_length(x, c):
    """Προσαρμογή C(x) = C0·exp(-x/λ) -> επιστρέφει λ (και R²)."""
    x, c = np.asarray(x, float), np.asarray(c, float)
    ok = c > 1e-9
    if ok.sum() < 2: return np.nan, np.nan
    sl, ic, r, *_ = stats.linregress(x[ok], np.log(c[ok]))
    return (-1 / sl if sl < 0 else np.nan), r ** 2

def logistic(t, K, r, N0):
    return K / (1 + ((K - N0) / N0) * np.exp(-r * t))

def fit_logistic(t, N):
    try:
        p, _ = optimize.curve_fit(logistic, t, N, p0=[max(N), 0.02, max(N[0], 1)], maxfev=20000)
        pred = logistic(t, *p)
        return p, 1 - np.sum((N - pred) ** 2) / np.sum((N - N.mean()) ** 2)
    except Exception:
        return None, np.nan
