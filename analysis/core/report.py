# -*- coding: utf-8 -*-
"""Συλλογή γραμμών αναφοράς: κάθε say() τυπώνει και αποθηκεύει για το stats_report.txt."""

REPORT = []
def say(line=""):
    print(line)
    REPORT.append(str(line))
