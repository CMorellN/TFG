import marimo

__generated_with = "0.21.1"
app = marimo.App(width="medium")


@app.cell
def _():
    # IMPORTACIONES:
    import marimo as mo # Para los títulitos
    import pynei # Librería tutor
    from pathlib import Path
    import matplotlib.pyplot as plt # Para visualizar (2D al menos)
    import mpl_toolkits.mplot3d # Para visualizar 3D
    import plotly.express as px
    from scatter3d import Scatter3dWidget, Category, LabelListErrorResponse
    import pandas
    import numpy

    return Category, Scatter3dWidget, mo, pandas, plt, pynei


@app.cell(hide_code=True)
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


@app.cell(hide_code=True)
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

    return (do_pca,)


@app.cell(hide_code=True)
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
        print("doing PCoA")
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
    mo.center(mo.md("""# VCFs web space"""))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.center(mo.md("""This is a website to work with VCFs tools, customizing options, were you can visualize the results online and download them."""))
    return


@app.cell
def _(mo):
    button_file = mo.ui.file(multiple=True, kind='button' ,label='Select file')
    mo.hstack([mo.md("Input VCF: "), button_file], justify="start")
    return (button_file,)


@app.cell
def _(button_file, mo):
    if button_file.value:
        _msg = mo.md(f"The **{button_file.value[0].name}** file has been properly upload.")
    else:
        _msg = mo.md("Please, upload a file")
    _msg
    return


@app.cell
def _(button_file, pynei):
    if button_file.value:
        # Preparar para PCA
        import tempfile

        if button_file.value is not None:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".vcf") as tmp:
                tmp.write(button_file.contents())
                tmp_path = tmp.name

            data = pynei.vars_from_vcf(vcf_path=tmp_path)

            data
    return (data,)


@app.cell
def _(mo):
    dropdown_pca_pcoa = mo.ui.dropdown(options=['PCoA', 'PCA'], value='PCoA', label='Choose the type of analysis: ')
    dropdown_pca_pcoa
    return (dropdown_pca_pcoa,)


@app.cell
def _(mo):
    slider0 = mo.ui.slider(start=0, stop=0.3, step=0.01, value=0.05, include_input=True, label='max_sample_gt_missing_rate')
    slider1 = mo.ui.slider(start=0, stop=0.3, step=0.01, value=0.05, include_input=True, label='max_var_gt_missing_rate')
    slider2 = mo.ui.slider(start=0.9, stop=1, step=0.01, value=0.95, include_input=True, label='max_allowed_maf')
    slider3 = mo.ui.slider(start=0.1, stop=0.2, step=0.01, value=0.1, include_input=True, label='min_allowed_r2')
    return slider0, slider1, slider2, slider3


@app.cell
def _(mo):
    checkbox = mo.ui.checkbox(label="Show and edit parameters:")# Create a checkbox to change PCA or PCoA parameters
    checkbox
    return (checkbox,)


@app.cell
def _(checkbox, mo, slider0, slider1, slider2, slider3):
    if checkbox.value:
        _parameters = mo.vstack([slider0, slider1, slider2, slider3])
    _parameters
    return


@app.cell
def _(mo):
    mo.md("""
    /// details | Default parameters
        type: info

        texto de relleno
    """)
    return


@app.cell
def _(mo):
    run_pca_pcoa = mo.ui.run_button(label='Run', kind='warn', full_width=True, tooltip='Click to execute the tool (PCA or PCoA) you have selected')
    run_pca_pcoa
    return (run_pca_pcoa,)


@app.cell
def _(
    button_file,
    data,
    do_pca,
    do_pcoa,
    dropdown_pca_pcoa,
    mo,
    run_pca_pcoa,
    slider0,
    slider1,
    slider2,
    slider3,
):
    if run_pca_pcoa.value:
        if button_file.value:
            if dropdown_pca_pcoa.selected_key == 'PCA':
                _msg = mo.md("*Calculating PCA...*")
                results = do_pca(
                                data, 
                                max_sample_gt_missing_rate = slider0.value,
                                max_var_gt_missing_rate = slider1.value,
                                max_allowed_maf = slider2.value,
                                min_allowed_r2 = slider3.value)
                # _msg = mo.md("") # This idea doesn't works how I thougth
            else:
                _msg = mo.md("*Calculating PCoA...*")
                results = do_pcoa(
                                data, 
                                max_sample_gt_missing_rate = slider0.value,
                                max_var_gt_missing_rate = slider1.value,
                                max_allowed_maf = slider2.value,
                                min_allowed_r2 = slider3.value)
        else:
            print('run false')
            _msg = mo.md("""Please, first upload a VCF file.""")
    _msg
    return (results,)


@app.cell
def _(Category, Scatter3dWidget, pandas, results):
    # 1. Unificar datos en una variable
    xyz = results["projections"].iloc[:,:3]

    # 2. Crear una categoría para todos
    my_cat = Category(pandas.Series(["Hola"]*xyz.shape[0], name="Hola"), editable=False)

    # 2.5. Definir etiquetas posibles en my_category: no necesario xq solo hay 1 categoría

    # 3. Creación del widget 3D
    widget_3d = Scatter3dWidget(
        xyz.to_numpy(), point_ids=list(xyz.index), category=my_cat
    )

    widget_3d.height = 800
    return (widget_3d,)


@app.cell
def _(widget_3d):
    widget_3d
    return


@app.cell
def _(plt, results):
    widget_2d = plt.scatter(results["projections"].iloc[:,0], results["projections"].iloc[:,1])

    return (widget_2d,)


@app.cell
def _():
    # figure = plt.figure()
    # ax = figure.add_subplot([111], projection='3d')
    # scatter = ax.scatter(results["projections"].iloc[:,0], results["projections"].iloc[:,1], results["projections"].iloc[:,2])
    return


@app.cell
def _(mo, results, widget_2d, widget_3d):
    tabs = mo.ui.tabs({
        "Projections 0d": widget_3d,
        "Projections 2d": mo.vstack([widget_2d, results["projections"]]),
        "Projections 3d": mo.vstack([widget_3d, results["projections"]])
        })
    tabs
    return


if __name__ == "__main__":
    app.run()
