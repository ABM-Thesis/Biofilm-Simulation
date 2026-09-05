# -*- coding: utf-8 -*-
"""Πείραμα 11-full-model — ενότητα 4.6 — Πίν. 4.2, Εικ. 4.8."""
from core import compare, experiment, holm, say, scenario_summary, scenario_timeseries, scenarios

def run(d, out):
    df, last = experiment("*11-full-model*table.csv", d, "[11] ΠΛΗΡΕΣ ΜΟΝΤΕΛΟ (όλοι οι μηχανισμοί ενεργοί)")
    if df is None: return
    SC = scenarios("Βασικό φάρμακο"); G = scenario_summary(last, SC, skip_empty=True)
    A, B, C, _ = [G[s[0]] for s in SC]
    tests = [("HGT χωρίς φαρμακευτική πίεση (A vs B)", A["res"], B["res"]),
             ("Επιλογή υπό διείσδυση (B vs C)",        B["res"], C["res"]),
             ("Κατάρρευση πληθυσμού (A vs C)",         A["alive"], C["alive"])]
    say("  -- κρίσιμες συγκρίσεις --")
    ps = [compare(n, a, b) for n, a, b in tests if len(a) and len(b)]
    if ps: say("  διορθωμένα p (Holm): " + ", ".join(f"{q:.4g}" for q in holm(ps)))
    scenario_timeseries(df, SC, out, "fig15_full_model.png",
                        "Πλήρες μοντέλο: κόστος αντοχής, persisters, αποκλεισμός όγκου, διάχυση θρεπτικών")
