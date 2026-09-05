#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ανάλυση αποτελεσμάτων BehaviorSpace για το μοντέλο βιοφίλμ-αντιβιοτικού.

ΧΡΗΣΗ
    python run.py --data-dir ../data --out ../figures          # όλα τα πειράματα
    python run.py --data-dir ../data --out ../figures --only 7 12   # μόνο τα πειράματα 7 και 12
    python run.py --list                                        # τι πείραμα αντιστοιχεί σε ποια ενότητα

ΔΟΜΗ
    core/            κοινός κώδικας: φόρτωση CSV, στατιστικά, γραφήματα, αναφορά
    experiments/     ένα αρχείο ανά πείραμα BehaviorSpace· καθένα εκθέτει run(d, out[, args])

Κάθε πείραμα αναλύεται μόνο αν βρεθεί το CSV του (*<αριθμός>-<όνομα>*table.csv) στον φάκελο δεδομένων.
Η αναφορά γράφεται στο <out>/stats_report.txt.

ΑΠΑΙΤΗΣΕΙΣ:  pip install pandas numpy scipy matplotlib
"""
import argparse, glob, os, sys
from core import REPORT, say
from experiments import (exp01_baseline, exp02_dose_sweep, exp03_mutation_hgt, exp04_strong_penetration,
                         exp05_wellmixed, exp06_triggerhgt_fine, exp07_resistance_cost, exp08_metabolic,
                         exp09_persisters, exp10_structure_withdrawn, exp11_full_model, exp12_dose_response,
                         exp13_hgt_extended, exp14_structure_validated, exp15_hgt_direct, exp16_spawn,
                         exp17_convergence, exp_seeding_mechanism, exp_scale_calibration, exp_model_comparison)

# (κλειδί για --only, module, ενότητα της εργασίας) — με τη σειρά εκτέλεσης του Κεφαλαίου 4
EXPERIMENTS = [
    ("1",  exp01_baseline,            "4.2  Βασικό καθεστώς — Εικ. 4.1"),
    ("2",  exp02_dose_sweep,          "4.3  Σάρωση δόσης"),
    ("3",  exp03_mutation_hgt,        "4.4  Μετάλλαξη × κατώφλι HGT"),
    ("4",  exp04_strong_penetration,  "4.4  Ισχυρή διείσδυση — Πίν. 4.1, Εικ. 4.5"),
    ("5",  exp05_wellmixed,           "4.3  Έλεγχος χωρικής δομής — Εικ. 4.2"),
    ("6",  exp06_triggerhgt_fine,     "4.4  Σημείο ανατροπής — Εικ. 4.4"),
    ("7",  exp07_resistance_cost,     "4.5  Κόστος αντοχής — Εικ. 4.6"),
    ("8",  exp08_metabolic,           "4.7  Μεταβολικές παράμετροι — Εικ. Δ.2"),
    ("9",  exp09_persisters,          "4.5  Persisters — Εικ. Δ.1"),
    ("10", exp10_structure_withdrawn, "—    Αποσυρμένη ανάλυση (μόνο με --appendix)"),
    ("11", exp11_full_model,          "4.6  Πλήρες μοντέλο — Πίν. 4.2, Εικ. 4.8"),
    ("12", exp12_dose_response,       "Παρ. Δ  Δοσοαπόκριση — Εικ. Δ.5"),
    ("13", exp13_hgt_extended,        "Παρ. Δ  Κατώφλι HGT στο εκτεταμένο — Εικ. Δ.6"),
    ("M",  exp_seeding_mechanism,     "4.6  Μηχανισμός: γιατί σβήνει η HGT (πειράματα 4 + 11)"),
    ("14", exp14_structure_validated, "4.5  Ανάδυση δομής — Εικ. 4.7"),
    ("15", exp15_hgt_direct,          "4.6  Άμεση μέτρηση HGT — Εικ. 4.9"),
    ("16", exp16_spawn,               "4.7  Αρχική τοποθέτηση — Εικ. Δ.3"),
    ("17", exp17_convergence,         "4.7  Στοχαστική σύγκλιση — Εικ. Δ.4"),
    ("18", exp_scale_calibration,     "4.7  Βαθμονόμηση κλίμακας (πείραμα 14)"),
    ("S",  exp_model_comparison,      "4.7  Σύγκριση με μοντέλα αναφοράς — Εικ. 4.3 (πειράματα 1, 5, 11)"),
]

def main():
    ap = argparse.ArgumentParser(description="Ανάλυση BehaviorSpace για το μοντέλο βιοφίλμ.")
    ap.add_argument("--data-dir", default=".", help="φάκελος με τα table CSV")
    ap.add_argument("--out", default="figures", help="φάκελος εξόδου")
    ap.add_argument("--only", nargs="+", metavar="ID", help="εκτέλεση μόνο των πειραμάτων με αυτά τα κλειδιά (π.χ. --only 7 12)")
    ap.add_argument("--list", action="store_true", help="εμφάνιση των πειραμάτων και έξοδος")
    ap.add_argument("--appendix", action="store_true",
                    help="τυπώνει και την αποσυρμένη ανάλυση [10] (μη έγκυρος δείκτης)")
    ap.add_argument("--biofilm-thickness-um", type=float, default=250.0,
                    help="βιβλιογραφικό πάχος ώριμου βιοφίλμ σε μm για τη βαθμονόμηση [18]")
    ap.add_argument("--base-diffusion", type=float, default=0.2)
    ap.add_argument("--base-decay", type=float, default=0.95)
    ap.add_argument("--biofilm-depth", type=float, default=30.0,
                    help="απόσταση βιοφίλμ από την πηγή (patches)")
    args = ap.parse_args()

    if args.list:
        for key, mod, desc in EXPERIMENTS:
            print(f"  {key:>3}  {mod.__name__.split('.')[-1]:28s} {desc}")
        return
    os.makedirs(args.out, exist_ok=True)

    say("=" * 72); say("ΑΝΑΛΥΣΗ ΜΟΝΤΕΛΟΥ ΒΙΟΦΙΛΜ-ΑΝΤΙΒΙΟΤΙΚΟΥ"); say("=" * 72)
    found = glob.glob(os.path.join(args.data_dir, "*table.csv"))
    if not found:
        print(f"Δεν βρέθηκαν αρχεία *table.csv στο '{args.data_dir}'."); sys.exit(1)
    say(f"Βρέθηκαν {len(found)} αρχεία:")
    for f in sorted(found): say(f"  - {os.path.basename(f)}")

    selected = set(args.only) if args.only else None
    d, out, base, wm = args.data_dir, args.out, None, None
    for key, mod, _ in EXPERIMENTS:
        if selected and key not in selected: continue
        if mod is exp01_baseline:              base = mod.run(d, out)
        elif mod is exp05_wellmixed:           wm = mod.run(d, out)
        elif mod is exp10_structure_withdrawn: mod.run(d, out, appendix=args.appendix)
        elif mod is exp_scale_calibration:     mod.run(d, out, args)
        elif mod is exp_model_comparison:      mod.run(base, wm, out, args)
        else:                                  mod.run(d, out)

    say("\n" + "=" * 72)
    say("Μέθοδοι: 95% ΔΕ bootstrap percentile (5000)· Mann-Whitney + Cliff's δ + απόλυτη διαφορά· "
        "Holm-Bonferroni· TOST για ισχυρισμούς ισοδυναμίας· τιμές -999 (εκλιπών πληθυσμός) -> NaN.")
    path = os.path.join(args.out, "stats_report.txt")
    open(path, "w", encoding="utf-8").write("\n".join(REPORT) + "\n")
    print(f"\nΗ αναφορά αποθηκεύτηκε: {path}")

if __name__ == "__main__":
    main()
