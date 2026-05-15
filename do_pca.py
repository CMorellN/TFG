import marimo

__generated_with = "0.21.1"
app = marimo.App(width="medium")


@app.cell
def _():
    # IMPORTACIONES:
    import marimo as mo 
    import pynei # JB library
    from pathlib import Path # used for tempfile
    import matplotlib.pyplot as plt # Para visualizar (2D al menos)
    import mpl_toolkits.mplot3d # Para visualizar 3D
    # import plotly.express as px
    from scatter3d import Scatter3dWidget, Category, LabelListErrorResponse # used for 3D visualization JB
    import pandas # used for 3D visualization JB
    import numpy 
    import time # for the progress_bar in PCoA
    import io # for the uploads

    return Category, Path, Scatter3dWidget, io, mo, numpy, pandas, plt, pynei


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

    return


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

    return


@app.cell(hide_code=True)
def _():
    # mo.center(mo.md("""# **VCFs web space**"""))
    return


@app.cell(hide_code=True)
def _():
    # mo.center(mo.md("""This is a website to work with VCFs tools, customizing options, were you can visualize the results online and download them."""))
    return


@app.cell
def _():
    # ================================================================================================
    # ================================ F I L E  P R E P A R A T I O N ================================
    # ================================================================================================
    return


@app.cell
def _(mo):
    from enum import Enum

    # This is to provide 2 app webs. One for VCF data (snips) and another for qualitative data (like Iris Dataset)

    class DataMode(Enum):

        GENOMIC = "genomic" # VSC: uv run marimo run do_pca.py --port 2719 
                            # añadir a url /?mode=genomic

        QUANTITATIVE = "quantitative" # VSC: uv run marimo run do_pca.py --port 2720
                                      # añadir a url /?mode=quantitative

        DIST_MATRIX = "dist_matrix" # para trabjar PCoA directamente sobre la matriz de distancias


    params = mo.query_params()

    mode = DataMode(params.get("mode", "quantitative")) # default value
    return DataMode, mode


@app.cell(hide_code=True)
def _(DataMode, mo, mode):
    # For both cases of data:
        # Web title
        # Short web description
        # Create the button 
        # Add previos text to the button

    if mode == DataMode.GENOMIC:
        _msg_title =  mo.center(mo.md("""# **VCF web space**"""))
        _msg_subtitle = mo.center(mo.md("""This is a website to work with Variant Call Format (VCF), running a PCA or PCoA, customizing options and visualizing the results online and downloading them."""))
        button_file = mo.ui.file(multiple=False, kind='button', label='Select VCF file')
        show_button_file = mo.hstack([mo.md("Input VCF: "), button_file], justify="start") 

    elif mode == DataMode.QUANTITATIVE:
        _msg_title =  mo.center(mo.md("""# **CSV web space**"""))
        _msg_subtitle = mo.center(mo.md("""This is a website to work with Comma-Separated Values (CSV), running a PCA or PCoA, customizing options and visualizing the results online and downloading them.""")) 
        button_file = mo.ui.file(multiple=False, kind='button', label='Select CSV file')
        show_button_file =  mo.hstack([mo.md("Input quantitative data (CSV): "), button_file], justify="start")

    else:
        _msg_title =  mo.center(mo.md("""# **Distance matrix web space**"""))
        _msg_subtitle = mo.center(mo.md("""This is a place to work with distance matrices to run PCoAs faster""")) 
        button_file = mo.ui.file(multiple=False, kind='button', label='Select distance matrix file')
        show_button_file =  mo.hstack([mo.md("Input quantitative data (CSV or txt): "), button_file], justify="start")
    # Show the title and description:
    mo.vstack([_msg_title, _msg_subtitle])
    return button_file, show_button_file


@app.cell(hide_code=True)
def _(show_button_file):
    show_button_file # To show the button
    return


@app.cell
def _(button_file, mo):
    # To show the file name and the format to confirm:

    if button_file.value:
        _msg = mo.md(f"The **{button_file.value[0].name}** file has been upload.")
    else:
        _msg = mo.md("Please, upload a file")
    _msg
    return


@app.cell
def _(DataMode, button_file, io, mode, pandas, pynei):
    if button_file.value and mode == DataMode.DIST_MATRIX:
        _df = pandas.read_csv(io.BytesIO(button_file.contents()), index_col=0)
        data_dists = pynei.dists.Distances.from_square_dists(_df)
        # resultes = pynei.do_pcoa(data_dists)
    return


@app.cell
def _():
    # if button_file.value and mode == DataMode.QUANTITATIVE:
    #     _df = pandas.read_csv(io.BytesIO(button_file.contents()), index_col=0)
    
    #     # DataFrame tiene forma (muestras, snps) → necesitamos (snps, muestras)
    #     _mat = _df.values.T  # shape: (num_snps, num_samples)
    
    #     # Convertir 0/1/2 a array 3D (snps, samples, ploidy=2)
    #     _gt_array = numpy.stack([
    #         numpy.where(_mat == 0, 0, numpy.where(_mat == 1, 0, 1)),  # alelo 1
    #         numpy.where(_mat == 0, 0, numpy.where(_mat == 1, 1, 1)),  # alelo 2
    #     ], axis=-1)
    
    #     data_d = pynei.Variants.from_gt_array(_gt_array, samples=list(_df.index))

    #     resss = do_pca(data_d)
    return


@app.cell
def _(DataMode, Path, button_file, io, mo, mode, numpy, pandas, pynei):
    if button_file.value and mode == DataMode.QUANTITATIVE:
        _df = pandas.read_csv(io.BytesIO(button_file.contents()), index_col=0)
    
        # DataFrame tiene forma (muestras, snps) → necesitamos (snps, muestras)
        _mat = _df.values.T  # shape: (num_snps, num_samples)
    
        # Convertir 0/1/2 a array 3D (snps, samples, ploidy=2)
        _gt_array = numpy.stack([
            numpy.where(_mat == 0, 0, numpy.where(_mat == 1, 0, 1)),  # alelo 1
            numpy.where(_mat == 0, 0, numpy.where(_mat == 1, 1, 1)),  # alelo 2
        ], axis=-1)
    
        data = pynei.Variants.from_gt_array(_gt_array, samples=list(_df.index))
    # EXTRACTING SNIPS from VCF in GENOMIC mode:

    # pynei.vars_from_vcf needs to read from disk, not memory, so we created a temporary file (tmp) to do so.

    _error = None

    if button_file.value and mode == DataMode.GENOMIC:

    # ============= V C F --> G E N O M I C =============

            import tempfile

            with tempfile.NamedTemporaryFile(delete=False, suffix=".vcf") as tmp:
                tmp.write(button_file.contents()) # Transfer content
                tmp_path = tmp.name # and name file

            try:
                data = pynei.vars_from_vcf(vcf_path=tmp_path) # Extracting variants (snips)

            except ValueError as e:
                _filename = button_file.value[0].name
                _filetype = Path(_filename).suffix

                _error = mo.callout(mo.md(f"Invalid file: You have uploaded a *'{_filetype}'* file and a **'.vcf'** is expected."), kind='danger')

            except KeyError as e:
                _error = mo.callout("Not enough samples.", kind='alert')

    # # ============= C S V --> DIST MATRIX=============
    #     else:
    #         data = button_file.contents()
    #         _error = mo.callout(mo.md("IT WORKS"), kind='success')

    _error
    return


@app.cell
def _():
    # ===============================================================================================
    # ================================== PCA / PCoA  O P T I O N S ==================================
    # ===============================================================================================
    return


@app.cell
def _(mo):
    dropdown_pca_pcoa = mo.ui.dropdown(options=['PCoA', 'PCA'], value='PCoA', label='Choose the type of analysis: ')

    checkbox_pcoa_speed = mo.ui.checkbox(label='Click to speed up the PCoA (embedding)')

    slider0 = mo.ui.slider(start=0, stop=0.3, step=0.01, value=0.05, include_input=True, label='max_sample_gt_missing_rate')
    slider1 = mo.ui.slider(start=0, stop=0.3, step=0.01, value=0.05, include_input=True, label='max_var_gt_missing_rate')
    slider2 = mo.ui.slider(start=0.9, stop=1, step=0.01, value=0.95, include_input=True, label='max_allowed_maf')
    slider3 = mo.ui.slider(start=0.1, stop=0.2, step=0.01, value=0.1, include_input=True, label='min_allowed_r2')

    parameters = mo.accordion({"**Show and edit parameters:** ": mo.vstack([slider0, slider1, slider2, slider3])})
    return checkbox_pcoa_speed, dropdown_pca_pcoa, parameters


@app.cell
def _(DataMode, checkbox_pcoa_speed, dropdown_pca_pcoa, mo, mode, parameters):
    # if mode == DataMode.DIST_MATRIX:
    #     _see = parameters
    _see = mo.md('')

    if mode != DataMode.DIST_MATRIX:
        _see = mo.vstack([dropdown_pca_pcoa, parameters])

        if dropdown_pca_pcoa.value == 'PCoA':
            _see = mo.vstack([dropdown_pca_pcoa, checkbox_pcoa_speed, parameters])

    _see
    return


@app.cell
def _():
    # ===============================================================================================
    # ================================ PCA / PCoA  E X E C U T I O N ================================
    # ===============================================================================================
    return


@app.cell
def _(DataMode, mo, mode):
    label = 'Run'

    if mode == DataMode.GENOMIC:
        color_run_pca_pcoa = 'info'

    elif mode == DataMode.QUANTITATIVE:
        color_run_pca_pcoa = 'success'

    else: 
        color_run_pca_pcoa = 'neutral'
        label = 'Run PCoA'

    run_pca_pcoa = mo.ui.run_button(label=label, kind=color_run_pca_pcoa, full_width=True, tooltip='Click to execute the tool (PCA or PCoA) you have selected')
    run_pca_pcoa
    return


@app.cell(hide_code=True)
def _():
    # # OPTION 1:

    # reduced_data = list(data.samples[:50])


    # if run_pca_pcoa.value and button_file.value:

    #     if dropdown_pca_pcoa.selected_key == 'PCA':
    #         results = do_pca(
    #                             data, 
    #                             max_sample_gt_missing_rate = slider0.value,
    #                             max_var_gt_missing_rate = slider1.value,
    #                             max_allowed_maf = slider2.value,
    #                             min_allowed_r2 = slider3.value)
    #     else:
    #         results = do_pcoa(
    #                             data,
    #                             desired_samples = reduced_data,
    #                             max_sample_gt_missing_rate = slider0.value,
    #                             max_var_gt_missing_rate = slider1.value,
    #                             max_allowed_maf = slider2.value,
    #                             min_allowed_r2 = slider3.value,
    #                             use_approx_embedding_algorithm=checkbox_pcoa_speed.value)
    # else:
    #     results = None
    return


@app.cell(hide_code=True)
def _():
    # # OPTION 2:

    # print("Inicio")

    # if mode == DataMode.GENOMIC or DataMode.QUANTITATIVE: 
    #     desired_samples = list(data.samples[:50])
    #     print("desired samples")

    # # if mode == DataMode.QUANTITATIVE:
    # #     desired_samples = data.index[:50]

    # if run_pca_pcoa.value and button_file.value:

    #     print("inside if run")

    #     if dropdown_pca_pcoa.selected_key == 'PCA':

    #         print("==> PCA")

    #         with mo.status.spinner(title = "Calculating PCA..."):
    #             print("spinner")
    #             results = do_pca(
    #                         data, 
    #                         max_sample_gt_missing_rate = slider0.value,
    #                         max_var_gt_missing_rate = slider1.value,
    #                         max_allowed_maf = slider2.value,
    #                         min_allowed_r2 = slider3.value)


    #     else:
    #         print("==> PCoA")

    #         _variants = data # Because we alter the data

    #         if mode == DataMode.DIST_MATRIX:
    #             results = pynei.do_pcoa(data)
    #         else:
    #             with mo.status.progress_bar(total=5, title="Calculando PCoA...") as _bar:
    #                 print("    progress")

    #                 _bar.update(increment=1, subtitle="Filtering samples") # 1

    #                 _samples = get_samples_with_enough_data(data, max_missing_rate=slider0.value)

    #                 if desired_samples:
    #                     _samples = [sample for sample in _samples if sample in desired_samples]

    #                 _variants = pynei.var_filters.filter_samples(data, _samples)

    #                 _bar.update(increment=1, subtitle="Filtering variants for lost data") # 2
    #                 time.sleep(1)
    #                 _variants = pynei.filter_by_missing_data(_variants, max_allowed_missing_rate=slider1.value)

    #                 _bar.update(increment=1, subtitle="Filtering by LD and MAF") # 3
    #                 time.sleep(1)
    #                 _variants = pynei.filter_by_ld_and_maf(_variants, max_allowed_maf=slider2.value, min_allowed_r2=slider3.value)

    #                 _bar.update(increment=1, subtitle="Calculating Kosman Distances (this will take several minutes)") # 4
    #                 time.sleep(1)
    #                 kosman_dists = pynei.calc_pairwise_kosman_dists(_variants, use_approx_embedding_algorithm=checkbox_pcoa_speed.value)

    #                 _bar.update(increment=1, subtitle="Calculating PCoA") # 5
    #                 time.sleep(0.2)
    #                 results = pynei.do_pcoa(kosman_dists)




    # else:
    #     print("else results=None")
    #     results = None
    # print("Finish")
    return


app._unparsable_cell(
    r"""
    # OPTION 3:

    print(" ===> OPCIÓN 3 <===")
    print("Inicio")

    if run_pca_pcoa.value and button_file.value:
        print("inside if run")

        if mode == DataMode.DIST_MATRIX:
            print('mode DIST_MATRIX')
            results = pynei.do_pcoa(data_dists)
            print('do_pcoa(data_dists)')

        else:
            print('mode Genomic or Quantitative')

            if dropdown_pca_pcoa.selected_key == 'PCA':
                print("==> PCA")

                with mo.status.spinner(title = "Calculating PCA..."):
                    print("spinner")
                    results = do_pca(data)

                    # results = do_pca(
                    #     data, 
                    #     max_sample_gt_missing_rate = slider0.value,
                    #     max_var_gt_missing_rate = slider1.value,
                    #     max_allowed_maf = slider2.value,
                    #     min_allowed_r2 = slider3.value)

            else:
                print("==> PCoA")

                    desired_samples = list(data.samples[:50])

                print("desired samples")

                _variants = data # Because we alter the data

                with mo.status.progress_bar(total=5, title="Calculando PCoA...") as _bar:
                    print("    progress")

                    _bar.update(increment=1, subtitle="Filtering samples") # 1

                    _samples = get_samples_with_enough_data(data, max_missing_rate=slider0.value)

                    if desired_samples:
                        _samples = [sample for sample in _samples if sample in desired_samples]

                    _variants = pynei.var_filters.filter_samples(data, _samples)

                    _bar.update(increment=1, subtitle="Filtering variants for lost data") # 2
                    time.sleep(1)
                    _variants = pynei.filter_by_missing_data(_variants, max_allowed_missing_rate=slider1.value)

                    _bar.update(increment=1, subtitle="Filtering by LD and MAF") # 3
                    time.sleep(1)
                    _variants = pynei.filter_by_ld_and_maf(_variants, max_allowed_maf=slider2.value, min_allowed_r2=slider3.value)

                    _bar.update(increment=1, subtitle="Calculating Kosman Distances (this will take several minutes)") # 4
                    time.sleep(1)
                    kosman_dists = pynei.calc_pairwise_kosman_dists(_variants, use_approx_embedding_algorithm=checkbox_pcoa_speed.value)

                    _bar.update(increment=1, subtitle="Calculating PCoA") # 5
                    time.sleep(0.2)
                    results = pynei.do_pcoa(kosman_dists)




    else:
        print("else results=None")
        results = None

    print("Finish")
    """,
    name="_"
)


@app.cell(hide_code=True)
def _():
    # _steps = [
    #     "Filtering samples", 
    #     "Filtering variants for lost data",
    #     "Filtering by LD and MAF", 
    #     "Calculating Kosman Distances (this will take several minutes)", 
    #     "Calculating PCoA"
    # ]

    # for _step in mo.status.progress_bar(_steps, title="Calculando PCoA..."):
    #     # print("STEP: ", _step[])

    #     if _step == "Filtrando muestras":
    #         _samples = get_samples_with_enough_data(_vars, max_missing_rate=slider0.value)
    #         _vars = pynei.var_filters.filter_samples(_vars, _samples)

    #     elif _step == "Filtrando variantes por datos perdidos":
    #         _vars = pynei.filter_by_missing_data(_vars, max_allowed_missing_rate=slider1.value)

    #     elif _step == "Filtrando por LD y MAF":
    #         _vars = pynei.filter_by_ld_and_maf(_vars, max_allowed_maf=slider2.value, min_allowed_r2=slider3.value)

    #     elif _step == "Calculando distancias Kosman":
    #         _dists = pynei.calc_pairwise_kosman_dists(_vars)

    #     elif _step == "Calculando PCoA":
    #         results = pynei.do_pcoa(_dists)
    return


@app.cell
def _():
    # ===============================================================================================
    # ============================= P R E P A R I N G   G R A P H I C S =============================
    # ===============================================================================================
    return


@app.cell
def _(mo, results):
    # 2D PROJECTIONS - buttons:
    index_proj = results["projections"].axes[1] # Take the projections indexes 'PC00', 'PC01'...

    dropdown_x_2d = mo.ui.dropdown(options=list(index_proj), value=index_proj[0], label='Horizontal axis: ')
    dropdown_y_2d = mo.ui.dropdown(options=list(index_proj), value=index_proj[1], label='Vertical axis: ')
    return dropdown_x_2d, dropdown_y_2d, index_proj


@app.cell(hide_code=True)
def _(dropdown_x_2d, dropdown_y_2d, plt, results):
    # 2D PROJECTIONS with scatter:

     # (Note: dorpdown_x_2d.value is the same that dropdown_x_2d.selected_key)

    fig_proj2D = plt.scatter(results["projections"][dropdown_x_2d.selected_key], results["projections"][dropdown_y_2d.selected_key])
    plt.title('2D Projections')
    plt.xlabel(dropdown_x_2d.selected_key)
    plt.ylabel(dropdown_y_2d.selected_key)
    plt.close()
    return (fig_proj2D,)


@app.cell
def _(index_proj, mo):
    # 3D PROJECTIONS - buttons:
    dropdown_x_3d = mo.ui.dropdown(options=list(index_proj), value=index_proj[0], label='Horizontal axis: ')
    dropdown_y_3d = mo.ui.dropdown(options=list(index_proj), value=index_proj[1], label='Vertical axis: ')
    dropdown_z_3d = mo.ui.dropdown(options=list(index_proj), value=index_proj[2], label='Depth axis: ')
    return dropdown_x_3d, dropdown_y_3d, dropdown_z_3d


@app.cell(hide_code=True)
def _(dropdown_x_3d, dropdown_y_3d, dropdown_z_3d, plt, results):
    # 3d PROJECTIONS with scatter:

    fig_proj3D = plt.figure()
    ax_proj3D = fig_proj3D.add_subplot(111, projection='3d')

    scatter = ax_proj3D.scatter(results["projections"][dropdown_x_3d.value], results["projections"][dropdown_y_3d.value], results["projections"][dropdown_z_3d.value])

    ax_proj3D.set_title('3D Projections')
    ax_proj3D.set_xlabel(dropdown_x_3d.value)
    ax_proj3D.set_ylabel(dropdown_y_3d.value)
    ax_proj3D.set_zlabel(dropdown_z_3d.value)
    plt.close()
    return (fig_proj3D,)


@app.cell(hide_code=True)
def _(Category, Scatter3dWidget, pandas, results):
    # 3D PROJECTIONS with Scatter3dWidget from Jose Blanca:

    # 1. Unificar datos en una variable
    xyz = results["projections"].iloc[:,:3]

    # 2. Crear una categoría para todos
    my_cat = Category(pandas.Series(["Hola"]*xyz.shape[0], name="Hola"), editable=False)

    # 2.5. Definir etiquetas posibles en my_category: no necesario xq solo hay 1 categoría

    # 3. Creación del widget 3D
    fig_proj3D_JB = Scatter3dWidget(
        xyz.to_numpy(), point_ids=list(xyz.index), category=my_cat
    )

    fig_proj3D_JB.height = 800
    return


@app.cell
def _(mo):
    # EXPLAINED VARIANCE - button:
    dropdown_variance = mo.ui.dropdown(options=['10' ,'20', 'all'], value='10', label='Choose how many Principal Components you want to see:')
    return (dropdown_variance,)


@app.cell
def _(dropdown_variance, plt, results):
    ## EXPLAINED VARIANCE:

    # Create the figure:
    fig_var_exp, ax_var_exp = plt.subplots()

    # The cumulative variance:
    cum_var = results["explained_variance (%)"].cumsum()

    # Tranforming to int the number of PCs choosen:
    if dropdown_variance.value == 'all':
        xmax = len(cum_var)
    else: 
        xmax = int(dropdown_variance.value)

    # Painting the figure:
    cum_var[:xmax].plot(kind="bar", ax=ax_var_exp, color="orange", label="Cumulative variance") # cumulative variance - BARS
    # cum_var.plot(ax=ax_var_exp, color="red", marker="o", linestyle="-", label="Cumulative variance") # cumulative variance - LINES

    results["explained_variance (%)"][:xmax].plot(kind="bar", ax=ax_var_exp, color="blue", label="Individual variance") # Explained variance (not cumulative)

    ax_var_exp.set_title('Cumulative variance')
    ax_var_exp.set_xlabel('Principal components')
    ax_var_exp.set_ylabel('Explained variance (%)')
    ax_var_exp.legend()

    ax_var_exp.set_yticks(range(0, 101, 10))
    ax_var_exp.grid(axis='y')

    # fig_var_exp
    return (fig_var_exp,)


@app.cell
def _():
    # ===============================================================================================
    # ================================= V I S U A L I Z A T I O N S =================================
    # ===============================================================================================
    return


@app.cell
def _(DataMode, dropdown_pca_pcoa, mode, numpy, plt, results):
    if dropdown_pca_pcoa.value == 'PCA' and mode == DataMode.QUANTITATIVE:
        fig_princomps, ax_princomps = plt.subplots()

        ejex = results["princomps"].iloc[0,:]
        ejey = results["princomps"].iloc[1,:]

        plt.scatter(ejex, ejey)

        # Make vectors (or arrows) without loops:
        plt.quiver(
            numpy.zeros_like(ejex),  # origen X (todos 0)
            numpy.zeros_like(ejey),  # origen Y (todos 0)
            ejex,
            ejey,
            angles='xy',
            scale_units='xy',
            scale=1,
            width=0.005,
            color='red',
            alpha=0.2
        )

        # for snip in results["princomps"].columns: # Recorrer tantas veces como columnas hayan

        #     ldx = results["princomps"].loc["PC00", snip]
        #     ldy = results["princomps"].loc["PC01", snip]

        #     # ax_princomps.arrow(
        #     #     0, 0,
        #     #     ldx,
        #     #     ldy,
        #     #     color="red",
        #     #     alpha=0.6
        #     # )

        #     ax_princomps.text(
        #         ldx,
        #         ldy,
        #         str(snip),
        #         color="red",
        #         fontsize=8
        #     )

        plt.title("Rotación de ejes PCA")
        plt.xlabel('PC00')
        plt.ylabel('PC01')

        plt.axhline(0, color='grey', linewidth=0.5)
        plt.axvline(0, color="grey", linewidth=0.5)

        plt.close()
    return (fig_princomps,)


@app.cell
def _(mo, results):
    if results.values:
        _msg = mo.md("""## **Results:**""")

    _msg

    # "if results.values:" siempre truthy aunque esté vacío. Debería ser "if results is not None:"
    return


@app.cell(hide_code=True)
def _():
    # # VERSIÓN 1:
    # tabs = mo.ui.tabs({
    #     "Projections 2d scatter": mo.ui.tabs({
    #         'Graphs': mo.hstack([fig_proj2D, mo.vstack([dropdown_x_2d, dropdown_y_2d])]),
    #         'Data': results["projections"]
    #         }),

    #     "Projections 3d scatter":  mo.ui.tabs({
    #         'Graphs': mo.hstack([fig_proj3D, mo.vstack([dropdown_x_3d, dropdown_y_3d, dropdown_z_3d])]),
    #         'Data': results["projections"]
    #         }),

    #     "Projections 3d tutor":  mo.ui.tabs({
    #         'Graphs': fig_proj3D_JB,
    #         'Data': results["projections"]
    #         }),

    #     "Explaines variance":  mo.ui.tabs({
    #         'Graphs': fig_var_exp,
    #         'Data': results["explained_variance (%)"]
    #         }),
    #     "Principal components": fig_princomps, 
    #     })
    # tabs
    return


@app.cell
def _(mo):
    radio_2d = mo.ui.radio(['Graphs', 'Data'], value='Graphs')
    radio_3d = mo.ui.radio(['Graphs', 'Data'], value='Graphs')
    radio_3d_jb = mo.ui.radio(['Graphs', 'Data'], value='Graphs')
    radio_var = mo.ui.radio(['Graphs', 'Data'], value='Graphs')
    return radio_2d, radio_3d, radio_var


@app.cell
def _(dropdown_pca_pcoa):
    dropdown_pca_pcoa.value
    return


@app.cell
def _(
    DataMode,
    dropdown_pca_pcoa,
    dropdown_variance,
    dropdown_x_2d,
    dropdown_x_3d,
    dropdown_y_2d,
    dropdown_y_3d,
    dropdown_z_3d,
    fig_princomps,
    fig_proj2D,
    fig_proj3D,
    fig_var_exp,
    mo,
    mode,
    radio_2d,
    radio_3d,
    radio_var,
    results,
):
    tabs_dict = {
        "Projections 2d scatter": mo.vstack([
            radio_2d,
            mo.hstack([fig_proj2D, mo.vstack([dropdown_x_2d, dropdown_y_2d]) ]) if radio_2d.value == 'Graphs' else results["projections"]
        ]),
        "Projections 3d scatter": mo.vstack([
            radio_3d,
            mo.hstack([fig_proj3D, mo.vstack([dropdown_x_3d, dropdown_y_3d, dropdown_z_3d]) ]) if radio_3d.value == 'Graphs' else results["projections"]
        ]),
        # "Projections 3d tutor": mo.vstack([
        #     radio_3d_jb,
        #     fig_proj3D_JB if radio_3d_jb.value == 'Graphs' else results["projections"]
        # ]),
        "Explained variance": mo.vstack([
            radio_var,
            mo.vstack([dropdown_variance, fig_var_exp]) if radio_var.value == 'Graphs' else results["explained_variance (%)"]
        ]),
    }

    if mode == DataMode.QUANTITATIVE and dropdown_pca_pcoa.value=='PCA':
        tabs_dict["Principal components"] = fig_princomps

    mo.ui.tabs(tabs_dict)
    return


@app.cell(hide_code=True)
def _():
    # tabs_dict = {
    #     "Projections 2d scatter": mo.ui.tabs({
    #         'Graphs': mo.hstack([fig_proj2D, mo.vstack([dropdown_x_2d, dropdown_y_2d])]),
    #         'Data': results["projections"]
    #     }),
    #     "Projections 3d scatter": mo.ui.tabs({
    #         'Graphs': mo.hstack([fig_proj3D, mo.vstack([dropdown_x_3d, dropdown_y_3d, dropdown_z_3d])]),
    #         'Data': results["projections"]
    #     }),
    #     "Projections 3d tutor": mo.ui.tabs({
    #         'Graphs': fig_proj3D_JB,
    #         'Data': results["projections"]
    #     }),
    #     "Explained variance": mo.ui.tabs({
    #         'Graphs': mo.vstack([dropdown_variance, fig_var_exp]),
    #         'Data': results["explained_variance (%)"]
    #     }),
    # }

    # if mode == DataMode.QUANTITATIVE:
    #     tabs_dict["Principal components"] = fig_princomps


    # mo.ui.tabs(tabs_dict)
    return


@app.cell
def _(dropdown_pca_pcoa, kosman_dists, mo):
    # Guardar la matriz de distancias de kosman:
    if dropdown_pca_pcoa.value == 'PCoA':
        csv_bytes = kosman_dists.square_dists.to_csv().encode()
            # kosman_dists: debería ser una matriz simétrica cuya diagonal son ceros, por lo que se guarda solo la parte triangular inferior.
            # .square_dists: convierte el vector condensado en una matriz cuadrada de formato DataFrame
            # .to_csv(): de Dataframe a string (texto) en formato CSV
            # .encode(): de string a bytes, xq lo pide mo.download()
        _msg = mo.md("If you want to recalculate the **PCoA faster** on the same data in the future, you can download the distance matrix and enter it as an input file later.")
    else: 
        _msg = mo.md('')

    _msg
    return (csv_bytes,)


@app.cell
def _(csv_bytes, dropdown_pca_pcoa, mo):
    if dropdown_pca_pcoa.value=='PCoA':
        _msg = mo.download(csv_bytes, filename="kosman_distances.csv", mimetype="text/csv", label='Download distance matrix')
    else:
        _msg = mo.md('')
    _msg
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
