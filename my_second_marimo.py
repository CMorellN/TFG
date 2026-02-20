import marimo

__generated_with = "0.19.6"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    #Trabajar con VCFs
    Me descargué uno de prueba de *https://ftp.1000genomes.ebi.ac.uk/vol1/ftp/release/20130502/*, el chr22 a sugerencia de Gepeto.

     Luego copié las funciones necesarias de la librería **tomato25** para hacer un **pca** y **pcoa** .

     Aprendí a abrir el archivo, coger solo los 10 primeros individuos y a crear vcfs más pequeños a través de **Git Bash:** *cat vcf_de_prueba | head -n 20000 > vcf_prueba_20mil.vcf*
    """)
    return


@app.cell
def _():
    # IMPORTACIONES:
    import marimo as mo # Para los títulitos
    import numpy as np
    # from sklearn.decomposition import PCA
    import pandas
    # import matplotlib.pyplot as plt # Para visualizar (2D al menos)
    # import mpl_toolkits.mplot3d # Para visualizar 3D
    import pynei # Librería tutor
    # from pynei.io_vcf import load_vars
    from pathlib import Path
    # from cyvcf2 import VCF
    return Path, mo, pynei


@app.cell(hide_code=True)
def _():
    ## Prueba de lectura de archivo cualquiera:
    # open("XYdata.txt")
    # for line in open("XYdata.txt"):
    #     print(line)
    #     break
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Funciones copiadas de **tomato25**:
    Queremos solo **do_pcoa**, pero como depende de otras las traemos también.
    """)
    return


@app.cell(hide_code=True)
def _(Variants, get_samples_with_enough_data, pynei):
    def do_pca(
        variants: Variants,
        #vars_cache_metadata,
        max_sample_gt_missing_rate=0.05,
        max_var_gt_missing_rate=0.05,
        max_allowed_maf=0.95,
        min_allowed_r2=0.1,
    ):
        print("doing PCA")
        samples = get_samples_with_enough_data(
            variants, max_missing_rate=max_sample_gt_missing_rate
        )

        variants = variants.variants
        variants = pynei.var_filters.filter_samples(variants, samples)
        variants = pynei.filter_by_missing_data(
            variants, max_allowed_missing_rate=max_var_gt_missing_rate
        )
        variants = pynei.filter_by_ld_and_maf(
            variants, max_allowed_maf=max_allowed_maf, min_allowed_r2=min_allowed_r2
        )
        pca = pynei.do_pca_with_vars(variants, transform_to_biallelic=True)
        return pca
    return


@app.cell
def _(Variants, pynei):
    def get_samples_with_enough_data(variants: Variants, max_missing_rate):
        sample_stats = pynei.calc_per_sample_stats(variants)
        samples_with_enough_data = tuple(
            sorted(
                (sample_stats.index[sample_stats["missing_gt_rate"] <= max_missing_rate])
            )
        )
        return samples_with_enough_data
    return (get_samples_with_enough_data,)


@app.cell
def _(Variants, pynei):
    def calc_kosman_dists(
        variants: Variants, use_approx_embedding_algorithm=False, num_processes=1
    ):
        dists = pynei.calc_pairwise_kosman_dists(
            variants,
            num_processes=num_processes,
            use_approx_embedding_algorithm=use_approx_embedding_algorithm,
        )
        return dists
    return (calc_kosman_dists,)


@app.cell
def _(Variants, calc_kosman_dists, get_samples_with_enough_data, pynei):
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
    return (do_pcoa,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    Cargar VCF y visualizar do_pcoa:
    """)
    return


@app.cell
def _(Path, pynei):
    # Cargar el VCF de prueba:
    archivo = Path("D:/DOCUMENTOS/UPV/TFG/VCFs_prueba/vcf_prueba_2000.vcf")
    # archivo = Path("D:/DOCUMENTOS/UPV/TFG/VCFs_prueba/vcf_prueba_20mil.vcf")

    data = pynei.vars_from_vcf(vcf_path=archivo)
    print("data:")
    print(f"individuos: ", data.samples.size)
    print(data.samples)

    less_data = list(data.samples[:10])
    print("\nless_data:")
    print(f"individuos: ", len(less_data))
    print(less_data)
    return data, less_data


@app.cell
def _(data, do_pcoa, less_data):
    # new_pcoa = do_pcoa(data)
    new_pcoa = do_pcoa(data, desired_samples=less_data) # Con solo los 10 primeros individuos

    print(new_pcoa)
    return


if __name__ == "__main__":
    app.run()
