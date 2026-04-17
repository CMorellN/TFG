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
    import pandas as pd
    import numpy as np

    return Category, Scatter3dWidget, mo, np, plt, pynei


@app.cell
def _():
    # ================================================================================================
    # ===================== PCA / PCoA   F U N C T I O N S   F R O M   P Y N E I =====================
    # ================================================================================================
    return


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
def _():
    # ================================================================================================
    # ================================ F I L E  P R E P A R A T I O N ================================
    # ================================================================================================
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
    # Preparing the file to PCA:

    if button_file.value:

        import tempfile

        if button_file.value is not None:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".vcf") as tmp:
                tmp.write(button_file.contents())
                tmp_path = tmp.name

            data = pynei.vars_from_vcf(vcf_path=tmp_path)

            data
    return (data,)


@app.cell
def _():
    # ===============================================================================================
    # ================================== PCA / PCoA  O P T I O N S ==================================
    # ===============================================================================================
    return


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
def _(mo, slider0, slider1, slider2, slider3):
    mo.accordion({"**Show and edit parameters:** ": mo.vstack([slider0, slider1, slider2, slider3])})
    return


@app.cell
def _():
    # ===============================================================================================
    # ================================ PCA / PCoA  E X E C U T I O N ================================
    # ===============================================================================================
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
def _():
    # ===============================================================================================
    # ============================= P R E P A R I N G   G R A P H I C S =============================
    # ===============================================================================================
    return


@app.cell
def _(mo, results):
    # 2D PROJECTIONS - buttons:
    pc_index = results["projections"].axes[1] # Take the projections indexes 'PC00', 'PC01'...

    dropdown_x = mo.ui.dropdown(options=list(pc_index), value=pc_index[0], label='Horizontal axis: ')
    dropdown_y = mo.ui.dropdown(options=list(pc_index), value=pc_index[1], label='Vertical axis: ')
    return dropdown_x, dropdown_y, pc_index


@app.cell
def _(dropdown_x, dropdown_y, plt, results):
    # 2D PROJECTIONS with scatter:

     # (Note: dorpdown_x.value is the same that dropdown_x.selected_key)

    widget_2d = plt.scatter(results["projections"][dropdown_x.selected_key], results["projections"][dropdown_y.selected_key])
    plt.title('2D Projections')
    plt.xlabel(dropdown_x.selected_key)
    plt.ylabel(dropdown_y.selected_key)
    plt.close()
    return (widget_2d,)


@app.cell
def _(mo, pc_index):
    # 3D PROJECTIONS - buttons:
    dropdown_x_3d = mo.ui.dropdown(options=list(pc_index), value=pc_index[0], label='Horizontal axis: ')
    dropdown_y_3d = mo.ui.dropdown(options=list(pc_index), value=pc_index[1], label='Vertical axis: ')
    dropdown_z_3d = mo.ui.dropdown(options=list(pc_index), value=pc_index[2], label='Depth axis: ')
    return dropdown_x_3d, dropdown_y_3d, dropdown_z_3d


@app.cell
def _(dropdown_x_3d, dropdown_y_3d, dropdown_z_3d, plt, results):
    # 3d PROJECTIONS with scatter:

    figure_3d = plt.figure()
    ax = figure_3d.add_subplot(111, projection='3d')

    scatter = ax.scatter(results["projections"][dropdown_x_3d.value], results["projections"][dropdown_y_3d.value], results["projections"][dropdown_z_3d.value])

    ax.set_title('3D Projections')
    ax.set_xlabel(dropdown_x_3d.value)
    ax.set_ylabel(dropdown_y_3d.value)
    ax.set_zlabel(dropdown_z_3d.value)
    plt.close()
    return (figure_3d,)


@app.cell
def _(Category, Scatter3dWidget, pandas, results):
    # 3D PROJECTIONS with Scatter3dWidget from Pynei:

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
def _(plt, results):
    # EXPLAINED VARIANCE:

    fig, axis = plt.subplots()

    cum_var = results["explained_variance (%)"].cumsum() # The cumulative variance

    cum_var.plot(kind="bar", ax=axis, color="orange", label="Cumulative variance") # cumulative variance - BARS
    # cum_var.plot(ax=axis, color="red", marker="o", linestyle="-", label="Cumulative variance") # cumulative variance - LINES

    results["explained_variance (%)"].plot(kind="bar", ax=axis, color="blue", label="Individual variance") # Explained variance (not cumulative)

    axis.set_title('Cumulative variance')
    axis.set_xlabel('Principal components')
    axis.set_ylabel('Explained variance (%)')
    axis.legend()

    axis.set_yticks(range(0, 101, 10))
    axis.grid(axis='y')

    # fig
    return (fig,)


@app.cell
def _():
    # ===============================================================================================
    # ================================= V I S U A L I Z A T I O N S =================================
    # ===============================================================================================
    return


@app.cell
def _(np, plt, results):
    figSento, axSento = plt.subplots()

    ejex = results["princomps"].iloc[0,:]
    ejey = results["princomps"].iloc[1,:]

    plt.scatter(ejex, ejey)

    # Make vectors (or arrows) without loops:
    plt.quiver(
        np.zeros_like(ejex),  # origen X (todos 0)
        np.zeros_like(ejey),  # origen Y (todos 0)
        ejex,
        ejey,
        angles='xy',
        scale_units='xy',
        scale=1,
        width=0.005,
        color='red',
        alpha=0.5
    )

    for varkk in results["princomps"].columns:
        ldx = results["princomps"].loc["PC00", varkk]
        ldy = results["princomps"].loc["PC01", varkk]

        # axSento.arrow(
        #     0, 0,
        #     ldx,
        #     ldy,
        #     color="red",
        #     alpha=0.6
        # )

        axSento.text(
            ldx,
            ldy,
            str(varkk),
            color="red",
            fontsize=8
        )

    plt.title("Rotación de ejes PCA")
    plt.xlabel('PC00')
    plt.ylabel('PC01')

    plt.axhline(0, color='grey', linewidth=0.5)
    plt.axvline(0, color="grey", linewidth=0.5)
    return (figSento,)


@app.cell
def _(plt, results):
    figkk, axkk = plt.subplots(figsize=(8, 6))

    # 👉 puntos (projections)
    x = results["projections"]["PC00"]
    y = results["projections"]["PC01"]

    # axkk.scatter(x, y, alpha=0.5)

    # 👉 loadings desde TU objeto
    loadings = results["princomps"]


    # 👉 top variables (más importantes en PC00)
    # pc1 = loadings.loc["PC00"]

    # top_vars = pc1.abs().sort_values(ascending=False).head(10).index

    # print(loadings)
    # escala para visualizar
    scale = 5

    for var in loadings.columns:
        lx = loadings.loc["PC00", var]
        ly = loadings.loc["PC01", var]

        axkk.arrow(
            0, 0,
            lx * scale,
            ly * scale,
            color="red",
            alpha=0.6
        )

        axkk.text(
            lx * scale,
            ly * scale,
            str(var),
            color="red",
            fontsize=8
        )
    
    #     print(var, " ===", lx)
    # print(results["princomps"].iloc[0])

    axkk.set_xlabel("x")
    axkk.set_ylabel("y")
    axkk.set_title("Rotación de ejes (PCA)")

    plt.axhline(0, color="grey", linewidth=0.5)
    plt.axvline(0, color="grey", linewidth=0.5)

    plt.close(figkk)

    figkk
    return


@app.cell
def _(plt, results):

    kk = plt.scatter(results["princomps"][0], results["princomps"][1])
    plt.title('What is this?')
    # plt.xlabel()
    # plt.ylabel()
    # plt.close()
    return


@app.cell
def _(results):
    results["princomps"].loc["PC00", :]
    return


@app.cell
def _(results):
    results["projections"]
    return


@app.cell
def _(
    dropdown_x,
    dropdown_x_3d,
    dropdown_y,
    dropdown_y_3d,
    dropdown_z_3d,
    fig,
    figSento,
    figure_3d,
    mo,
    results,
    widget_2d,
    widget_3d,
):
    # # VERSIÓN 1:
    # tabs = mo.ui.tabs({
    #     "Projections 2d scatter": mo.vstack([widget_2d, results["projections"]]),
    #     "Projections 3d scatter": mo.vstack([figure_3d, results["projections"]]),
    #     "Projections 3d tutor": mo.vstack([widget_3d, results["projections"]]),
    #     "Explaines variance": mo.vstack([widget_2d, results["explained_variance (%)"]]),
    #     # "Principal components": 
    #     })
    # tabs

    # VERSIÓN 2:
    tabs = mo.ui.tabs({
        "Projections 2d scatter": mo.ui.tabs({
            'Graphs': mo.hstack([widget_2d, mo.vstack([dropdown_x, dropdown_y])]),
            'Data': results["projections"]
            }),

        "Projections 3d scatter":  mo.ui.tabs({
            'Graphs': mo.hstack([figure_3d, mo.vstack([dropdown_x_3d, dropdown_y_3d, dropdown_z_3d])]),
            'Data': results["projections"]
            }),

        "Projections 3d tutor":  mo.ui.tabs({
            'Graphs': widget_3d,
            'Data': results["projections"]
            }),

        "Explaines variance":  mo.ui.tabs({
            'Graphs': fig,
            'Data': results["explained_variance (%)"]
            }),
        "Principal components": figSento, 
        })
    tabs
    return


if __name__ == "__main__":
    app.run()
