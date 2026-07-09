from pathlib import Path
import tempfile
# from unittest import result 
import pandas
import pynei
import utils
import numpy
import pytest



# The normal VCF:
VCF_PATH = Path(__file__).parent / "test_fixtures" / "vcf_test_247rows.vcf"

# =================== PURE FUNCTIONS ===================

def test_get_samples_returns_tuple():
    # variants = pynei.vars_from_vcf(VCF_PATH)

    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(VCF_PATH.read_bytes())
        tmp.flush() ## fuerza a que los datos del buffer se vuelquen al disco antes de que vars_from_vcf los lea.
        variants = pynei.vars_from_vcf(Path(tmp.name))
    
        result = utils.get_samples_with_enough_data(variants, max_missing_rate=0.05)

        assert isinstance(result, tuple) # Is it a tuple?
        assert len(result) > 0  # Is it not empty?
        assert all(isinstance(s, str) for s in result)  # Are all elements strings?
        assert result == tuple(sorted(result))  # Is it sorted?
        assert len(result) == len(set(result))  # Are all elements unique?

@pytest.mark.slow
def test_calc_kosman_dists_returns_square_matrix():
    variants = pynei.vars_from_vcf(VCF_PATH)
    result = utils.calc_kosman_dists(variants, use_approx_embedding_algorithm=False, num_processes=1) # Remember that this is a triangular matrix expressed in a vector

    assert isinstance(result, pynei.dists.Distances) # Is it a Distances object?

    matrix = result.square_dists
    assert matrix.shape[0] == matrix.shape[1] # Is it square?
    assert matrix.shape[0] == len(variants.samples) # Does it match the number of samples?
    assert numpy.allclose(matrix.values[:3, :3], matrix.values[:3, :3].T) # Is it symmetric?
    assert list(matrix.index[:3]) == list(matrix.columns[:3]) # Do row and column names match?
    assert numpy.all(numpy.diag(matrix.values) == 0) # Are diagonal elements zero?


def test_do_pca():
    variants = pynei.vars_from_vcf(VCF_PATH)
    result = utils.do_pca(variants, max_sample_gt_missing_rate=0.05, max_var_gt_missing_rate=0.05, max_allowed_maf=0.95, min_allowed_r2=0.1)

    assert isinstance(result, dict) # Is it a dict?
    assert set(result.keys()) == {"projections", "explained_variance (%)", "princomps"} # Does it have the expected keys?
    assert result["projections"].shape[0] <= len(variants.samples) # Filtering reduces or mainteined samples?

    assert isinstance(result["projections"], pandas.DataFrame) # Is "projections" a DataFrame?
    assert result["projections"].shape[0] > 0 # Does "projections" have rows?

    assert isinstance(result["explained_variance (%)"], pandas.Series) # Is "explained_variance (%)" a Series?
    assert numpy.all(result["explained_variance (%)"] >= 0) # Are all explained variance values non-negative?
    assert numpy.isclose(result["explained_variance (%)"].sum(), 100) # Does the explained variance sum to 100%?

    assert isinstance(result["princomps"], pandas.DataFrame) # Is "princomps" a DataFrame?
    assert len(result["princomps"]) > 0 # Does "princomps" have rows?

@pytest.mark.slow
def test_do_pcoa():
    variants = pynei.vars_from_vcf(VCF_PATH)
    result = utils.do_pcoa(variants)

    assert isinstance(result, dict) # Is it a dict?
    assert set(result.keys()) == {"projections", "explained_variance (%)"} # Does it have the expected keys?
    assert result["projections"].shape[0] <= len(variants.samples) # Filtering reduces or mainteined samples?

    assert isinstance(result["projections"], pandas.DataFrame) # Is "projections" a DataFrame?
    assert result["projections"].shape[0] > 0 # Does "projections" have rows?

    assert isinstance(result["explained_variance (%)"], pandas.Series) # Is "explained_variance (%)" a Series?
    assert numpy.isclose(result["explained_variance (%)"].sum(), 100) # Does the explained variance sum to 100%?
