# -*- coding: utf-8 -*-
"""Κοινός κώδικας των αναλύσεων."""
from .report import REPORT, say
from .data_io import RULES, load, find, finals, experiment
from .statistics import (ci95, fmt_ci, cliffs_delta, holm, tost, tost_report, compare, monotonicity_check,
                         penetration_depth_theory, fit_decay_length, logistic, fit_logistic)
from .plotting import (plt, REG, REG2, REG3, save, deco, heatmap, errorbars, scatter_means, scenarios,
                       scenario_summary, scenario_timeseries, extremes)
