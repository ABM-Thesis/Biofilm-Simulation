# -*- coding: utf-8 -*-
"""Πείραμα 4-strong-penetration — ενότητα 4.4 — Πίν. 4.1, Εικ. 4.5 (επιλογή έναντι HGT)."""
from core import compare, experiment, holm, say, scenario_summary, scenario_timeseries, scenarios

def run(d, out):
    df, last = experiment("*4-strong-penetration*table.csv", d, "[4] ΙΣΧΥΡΗ ΔΙΕΙΣΔΥΣΗ: επιλογή έναντι HGT")
    if df is None: return
    SC = scenarios("Βασικό"); G = scenario_summary(last, SC)
    A, B, C, D = [G[s[0]] for s in SC]
    tests = [("Κατάρρευση πληθυσμού (A vs C)", A["alive"], C["alive"]),
             ("Επιλογή στην αντοχή (B vs C)",  B["res"],   C["res"]),
             ("Επίδραση HGT στην αντοχή (A vs B)", A["res"], B["res"]),
             ("Διάσωση πληθυσμού από HGT (C vs D)", C["alive"], D["alive"])]
    say("  -- κρίσιμες συγκρίσεις --")
    adj = holm([compare(n, a, b) for n, a, b in tests])
    say("  διορθωμένα p (Holm, 4 συγκρίσεις): " +
        ", ".join(f"{n.split('(')[0].strip()}={q:.4g}" for (n, _, _), q in zip(tests, adj)))
    scenario_timeseries(df, SC, out, "fig7_selection_vs_hgt.png")
