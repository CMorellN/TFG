# This file contains the do_pca.py functions to test.

import pynei
from pynei import Variants
from pathlib import Path
import tempfile

# =================== PURE FUNCTIONS ===================

def get_samples_with_enough_data(variants: pynei.Variants, max_missing_rate):
    sample_stats = pynei.calc_per_sample_stats(variants)
    samples_with_enough_data = tuple(
        sorted(
            (sample_stats.index[sample_stats["missing_gt_rate"] <= max_missing_rate])
        )
    )
    return samples_with_enough_data


def calc_kosman_dists(
    variants: Variants, use_approx_embedding_algorithm=False, num_processes=1
):
    dists = pynei.calc_pairwise_kosman_dists(
        variants,
        num_processes=num_processes,
        use_approx_embedding_algorithm=use_approx_embedding_algorithm,
    )
    return dists


def do_pca(
    variants: Variants,
    #vars_cache_metadata,
    max_sample_gt_missing_rate=0.05,
    max_var_gt_missing_rate=0.05,
    max_allowed_maf=0.95,
    min_allowed_r2=0.1,
):

    samples = get_samples_with_enough_data(
        variants, max_missing_rate=max_sample_gt_missing_rate
    )

    #variants = variants.variants
    variants = pynei.var_filters.filter_samples(variants, samples)
    variants = pynei.filter_by_missing_data(
        variants, max_allowed_missing_rate=max_var_gt_missing_rate
    )
    variants = pynei.filter_by_ld_and_maf(
        variants, max_allowed_maf=max_allowed_maf, min_allowed_r2=min_allowed_r2
    )
    pca = pynei.do_pca_with_vars(variants, transform_to_biallelic=True)
    return pca


def do_pcoa(
    variants: Variants,
    #vars_cache_metadata,
    max_sample_gt_missing_rate=0.1,
    max_var_gt_missing_rate=0.05,
    max_allowed_maf=0.95,
    min_allowed_r2=0.1,
    use_approx_embedding_algorithm=False,
    num_processes=1,
    desired_samples=None, # Solicita la lista con los individuos deseados,  no el nº
):

    samples = get_samples_with_enough_data(
        variants, max_missing_rate=max_sample_gt_missing_rate
    )

    # variants = variants.variants
    if desired_samples:
        samples = [sample for sample in samples if sample in desired_samples]

    variants = pynei.var_filters.filter_samples(variants, samples)
    variants = pynei.filter_by_missing_data(
        variants, max_allowed_missing_rate=max_var_gt_missing_rate
    )
    variants = pynei.filter_by_ld_and_maf(
        variants, max_allowed_maf=max_allowed_maf, min_allowed_r2=min_allowed_r2
    )

    dists = calc_kosman_dists(
        variants,
        use_approx_embedding_algorithm=use_approx_embedding_algorithm,
        num_processes=num_processes,
    )
    pcoa = pynei.do_pcoa(dists)
    return pcoa
