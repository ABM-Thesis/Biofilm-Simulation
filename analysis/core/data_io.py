# -*- coding: utf-8 -*-
"""Φόρτωση πινάκων BehaviorSpace (6 γραμμές μεταδεδομένων, κεφαλίδα στην 7η)."""
import glob, os
import pandas as pd
from .report import say

RULES = [  # (υπόστροφο που ψάχνουμε στο όνομα στήλης, νέο όνομα)  — η σειρά μετράει
    ("run number", "run"), ("[step]", "step"),
    ("count turtles with [alive?]", "alive"), ("count turtles with [not alive?]", "dead"),
    ("alive? and dormant?", "dormant"), ("mean [resistance]", "res"), ("mean [pycor]", "meany"),
    ("pycor < min-pycor + 4", "ab_base"), ("pycor < min-pycor + 8", "band1"),
    ("min-pycor + 8 and", "band2"), ("min-pycor + 16 and", "band3"), ("pycor >= min-pycor + 24", "band4"),
    ("mean [antibiotic] of patches", "ab"), ("shape-factor", "shape"), ("mutation-count", "mutations"),
    ("bf-height", "bfh"), ("bf-spread", "bfs"), ("bf-occupancy", "bfo"),
    ("hgt-count", "hgtn"), ("frac-resistant", "fres"), ("mean-resistance-safe", "res"),
    ("spawncellposition", "spawn"), ("Triggerhgt", "trig"), ("mutation-chance", "mut"),
    ("antibioticapplication-belowtop", "dose"), ("hgt-enabled?", "hgt"), ("strong-penetration?", "strong"),
    ("well-mixed?", "wm"), ("resistance-cost", "cost"), ("persister-switch-prob", "psw"),
    ("max-cells-per-patch", "maxcells"), ("metabolic-rate", "met"), ("reproduction-energy-threshold", "repthr"),
    ("nutrient-diffusion", "ndiff"), ("mean [nutrient]", "nut"), ("wellmixed-level", "wmlevel"),
    ("source-concentration", "srcconc"),
]

def load(path):
    df = pd.read_csv(path, skiprows=6)
    df.columns = [c.strip() for c in df.columns]
    ren, used = {}, set()
    for col in df.columns:
        for pat, new in RULES:
            if pat in col and new not in used:
                ren[col] = new; used.add(new); break
    df = df.rename(columns=ren)
    for b in ("hgt", "strong", "wm"):                 # booleans -> bool
        if b in df.columns:
            df[b] = df[b].astype(str).str.strip().str.lower().eq("true")
    # Το μοντέλο εκπέμπει -999 όταν δεν υπάρχει ζωντανό κύτταρο (sentinel):
    # μετατρέπεται σε NaN και αποκλείεται από κάθε στατιστικό.
    for c in ("bfh", "bfs", "bfo", "res", "fres"):
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce").mask(lambda v: v <= -998)
    return df

def find(pattern, data_dir):
    hits = sorted(glob.glob(os.path.join(data_dir, pattern)))
    return hits[0] if hits else None

def finals(df):
    """Τελευταία γραμμή κάθε εκτέλεσης (τελική κατάσταση)."""
    return df.sort_values("step").groupby("run").tail(1) if "step" in df.columns else df

def experiment(pattern, d, title=None):
    """find + load + finals + τίτλος ενότητας. Επιστρέφει (df, last) ή (None, None)."""
    f = find(pattern, d)
    if not f: return None, None
    df = load(f)
    if title: say("\n" + title)
    return df, finals(df)
