from io import StringIO

import numpy as np
import streamlit as st

from serenipy.dtaselectfilter import from_dta_select_filter
from exclusionms.db import MassIntervalTree
from exclusionms.components import ExclusionPoint

from utils import get_tolerance

st.header('PaSER Venn! :bar_chart:')

st.write("""
This app is used to generate venn diagrams for protein and peptide overlap between 2 or 3 experiments.
""")

files = st.file_uploader(label='DTASelect-filter.txt files', accept_multiple_files=True, type='.txt')
tolerance = get_tolerance()

if st.button('Run'):

    if len(files) != 2 and len(files) != 3:
        st.warning('Incorrect number of files: {len(files}. Please use only 2 or 3 files!')
        st.stop()

    results = []
    for file in files:
        file_io = StringIO(file.getvalue().decode("utf-8"))
        _, _, dta_select_filter_results, _ = from_dta_select_filter(file_io)
        results.append(dta_select_filter_results)

    trees = []
    points_list = []
    for dta_select_filter_results in results:
        tree = MassIntervalTree()
        points = []
        for result in dta_select_filter_results:
            for peptide_line in result.peptide_lines:
                sequence = peptide_line.sequence[2:-2]
                mass = peptide_line.mass_plus_hydrogen
                intensity = peptide_line.total_intensity
                rt = peptide_line.ret_time
                ook0 = peptide_line.ion_mobility
                charge = peptide_line.charge
                scan_number = peptide_line.low_scan

                point = ExclusionPoint(charge=charge, mass=mass, rt=rt, ook0=ook0, intensity=intensity)
                interval = tolerance.construct_interval(sequence, point)
                tree.add(interval)
                points.append(point)
        points_list.append(points)
        trees.append(tree)

    for i, points in enumerate(points_list):
        for j, tree in enumerate(trees):
            overlaps = []
            for point in points:
                intervals = list(tree.query_by_point(point))
                sequences = {interval.interval_id for interval in intervals}
                overlaps.append(len(sequences))

            print(f'points from {files[i].name} queried against {files[j].name}')
            print(np.mean(overlaps))
