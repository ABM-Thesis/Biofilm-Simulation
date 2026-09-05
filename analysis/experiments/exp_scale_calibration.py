# -*- coding: utf-8 -*-
"""Πείραμα 14 — ενότητα 4.7 — βαθμονόμηση κλίμακας (patch -> μm)."""
import numpy as np
from core import experiment, penetration_depth_theory, say

def run(d, out, args):
    """[18] Βαθμονόμηση κλίμακας (patch -> μm) με άγκυρα το πάχος ώριμου βιοφίλμ (Gulati et al. 2018)."""
    _, last = experiment("*14-structure-validated*table.csv", d)
    if last is None or "bfh" not in last.columns: return
    say("\n[18] ΒΑΘΜΟΝΟΜΗΣΗ ΚΛΙΜΑΚΑΣ (patch -> μm) — άγκυρα: πάχος βιοφίλμ C. albicans 240-290 μm "
        "(Gulati et al. 2018)· έλεγχος τάξης μεγέθους, όχι επικύρωση")
    struct = last[(last["maxcells"] > 0) & (last["ndiff"] > 0)]     # το πιο δομημένο καθεστώς
    if struct.empty: return
    h_patches, h_max = struct["bfh"].mean(), struct["bfh"].max()
    if not np.isfinite(h_patches) or h_patches <= 0:
        say("  δεν υπάρχει έγκυρη μέτρηση ύψους"); return
    anchor = float(args.biofilm_thickness_um)
    um_mean = anchor / h_patches
    um_max = anchor / h_max if h_max > 0 else np.nan
    say(f"  μοντέλο: ύψος βιοφίλμ (bf-height, δομημένο καθεστώς) = {h_patches:.2f} patches "
        f"[μέγιστο κελί {h_max:.2f}]")
    say(f"  -> 1 patch ~ {um_mean:.1f} μm  (με βάση τον μέσο όρο)")
    say(f"  -> 1 patch ~ {um_max:.1f} μm  (με βάση το πιο δομημένο κελί)")

    say("  -- έλεγχος ευλογοφάνειας --")                    # πόσα βακτήρια χωράνε σε ένα patch;
    CELL_UM = 1.5          # τυπική διάμετρος βακτηριακού κυττάρου (κόκκος/βάκιλος)
    for mc in sorted(struct["maxcells"].unique()):
        if struct[struct["maxcells"] == mc].empty: continue
        implied_um = CELL_UM * np.sqrt(float(mc))          # γραμμική διάσταση patch για mc κύτταρα σε 2D
        say(f"    max-cells-per-patch={int(mc)}: για κύτταρα ~{CELL_UM} μm το patch θα ήταν "
            f"~{implied_um:.1f} μm | η άγκυρα δίνει {um_mean:.1f} μm "
            f"-> λόγος {um_mean/implied_um:.1f}x")
    ratio = um_mean / (CELL_UM * np.sqrt(struct["maxcells"].mean()))
    say("  -- συμπέρασμα --")
    say(f"    λόγος των δύο υπολογισμών = {ratio:.1f}x -> "
        f"{'η κλίμακα είναι φυσικά εύλογη' if 0.5 <= ratio <= 2.0 else 'ΑΣΥΜΦΩΝΙΑ: το μοντέλο δεν είναι βαθμονομημένο σε φυσικές μονάδες (μόνο ποιοτικά αποτελέσματα)'}")

    lam_base = penetration_depth_theory(args.base_diffusion, args.base_decay)   # το λ σε μm
    say("  -- εφαρμογή στο βάθος διείσδυσης --")
    say(f"    λ (βασικό καθεστώς) = {lam_base:.2f} patches ~ {lam_base*um_mean:.0f} μm")
    say(f"    πάχος βιοφίλμ στο μοντέλο = {h_patches:.2f} patches ~ {anchor:.0f} μm (εξ ορισμού)")
    say(f"    -> το αντιβιοτικό διεισδύει στο {100*lam_base/h_patches:.0f}% του πάχους")

    depth = float(args.biofilm_depth)     # αδιάστατοι λόγοι: το μόνο που δεν εξαρτάται από την άγκυρα
    say("  -- ΑΔΙΑΣΤΑΤΟΙ ΛΟΓΟΙ (ανεξάρτητοι της βαθμονόμησης) --")
    say(f"    λ / πάχος βιοφίλμ          = {lam_base/h_patches:6.2f}  (διεισδυτικότητα ως προς το πάχος)")
    say(f"    απόσταση πηγής / πάχος     = {depth/h_patches:6.2f}  (πόσο μακριά είναι η πηγή σε 'πάχη βιοφίλμ')")
    say(f"    λ / απόσταση πηγής         = {lam_base/depth:6.3f}  (κλάσμα της διαδρομής που καλύπτει το φάρμακο)")
