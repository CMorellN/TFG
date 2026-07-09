import marimo

__generated_with = "0.23.6"
app = marimo.App(width="medium")


@app.cell
async def _():
    # Necesario para correrlo en web (non local):
    import sys
    if "pyodide" in sys.modules:
        import micropip
        await micropip.install("https://cmorelln.github.io/TFG/pynei-0.1.0-py3-none-any.whl")
    return


@app.cell
def _():
    # IMPORTACIONES:
    import marimo as mo 
    import pynei # PCA and PCoA. Jose Blanca library
    from pynei import Variants

    import io # for the uploads
    import tempfile # for GENOMIC mode
    from pathlib import Path # used for tempfile

    import pandas 
    import numpy 
    import time # for the progress_bar in PCoA


    import matplotlib.pyplot as plt # Para visualizar (2D al menos)
    import mpl_toolkits.mplot3d # Para visualizar 3D

    return Path, Variants, io, mo, numpy, pandas, plt, pynei, tempfile, time


@app.cell
def _(mo):
    from enum import Enum

    # This is to provide 3 app webs. One for VCF data (snips) and another for qualitative data (like Iris Dataset)

    class DataMode(Enum):

        GENOMIC = "genomic" # VSC: uv run marimo run do_pca.py --port 2719 
                            # añadir a url /?mode=genomic

        QUANTITATIVE = "quantitative" # VSC: uv run marimo run do_pca.py --port 2720
                                      # añadir a url /?mode=quantitative

        DIST_MATRIX = "dist_matrix" # para trabjar PCoA directamente sobre la matriz de distancias


    params = mo.query_params()

    mode = DataMode(params.get("mode", "genomic")) # default value
    return DataMode, mode


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


@app.cell
def _():
    # ================================================================================================
    # ================================ F I L E  P R E P A R A T I O N ================================
    # ================================================================================================
    return


@app.cell(hide_code=True)
def _(DataMode, mo, mode):
    # For the three cases of data:
        # Web title --> _title_text
        # Short web description --> _subtitle_text
        # Text in the button --> _label_button
        # Pevios text to the button --> _previous_text_button

    if mode == DataMode.GENOMIC:
        _title_text = 'VCF web space'
        _subtitle_text = 'This is a website to work with Variant Call Format (VCF), running a PCA or PCoA, customizing options and visualizing the results online and downloading them.'
        _label_button = 'Select VCF file'
        _previous_text_button = "Input VCF: "

    elif mode == DataMode.QUANTITATIVE:
        _title_text = 'CSV web space'
        _subtitle_text = 'This is a website to work with genomic CSV (Comma-Separated Values), running a PCA or PCoA, customizing options and visualizing the results online and downloading them.'
        _label_button = 'Select CSV file'
        _previous_text_button = "Input quantitative data (CSV): "

    else:
        _title_text = 'Distance matrix web space'
        _subtitle_text = 'This is a place to work with distance matrices to run PCoAs faster'
        _label_button = 'Select distance matrix file'
        _previous_text_button = "Input quantitative data (CSV): "

    _title = mo.center(mo.md(f"#**{_title_text}**"))
    _subtitle = mo.center(mo.md(_subtitle_text))

    button_file = mo.ui.file(multiple=False, kind='button', label=_label_button, max_size = 100_000_000)
    show_button_file =  mo.hstack([mo.md(_previous_text_button), button_file], justify="start")


    # Show the title and description:
    mo.vstack([_title, _subtitle])
    return button_file, show_button_file


@app.cell
def _(mo):
    a = 2+2
    mo.md("Hola")
    return


@app.cell
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
def _():
    # _filename = button_file.value[0].name
    # _filetype = Path(_filename).suffix

    # # Cheking the correct format file
    # if _filetype != '.csv':
    #     _error = mo.md(f"Incorrect file type. You upload a '{_filetype}' and a **'.csv'** is expected.").callout(kind='danger')

    # else:
    #     try:
    #         _df = pandas.read_csv(io.BytesIO(button_file.contents()), index_col=0)

    #         # Cheking all values are numbers:
    #         if not _df.apply(pandas.api.types.is_numeric_dtype).all():
    #             _error = mo.callout("All columns must contain numeric values.", kind='danger')

    #         # Checking that is a distance matrix and not another type of csv:
    #         elif _df.shape[0] != _df.shape[1]: # square matrix
    #             _error = mo.callout('The file must be a square matrix.', kind='alert')

    #         elif not numpy.allclose(_df.values[:3, :3], _df.values[:3, :3].T): # symetric matrix
    #             _error = mo.callout('The file must be a symetric matrix.', kind='alert')

    #         elif list(_df.index[:3]) != list(_df.columns[:3]): # headers (names) match
    #             _error = mo.callout('The file must be a matrix where row and column names match.', kind='alert')

    #         else:
    #             _data = pynei.dists.Distances.from_square_dists(_df)

    #     # Errors from pandas.read_csv():     
    #     except ValueError as e:
    #         _error = mo.callout(str(e), kind='alert')

    # mo.vstack([_error, _df])
    return


@app.cell(hide_code=True)
def _(Path, io, mo, numpy, pandas, pynei):
    def load_csv_dist_matrix(button_file, error):
       # Expected input: square and simetric matrix because represents the distances between elements, for PCoA
        data = None

        _filename = button_file.value[0].name
        _filetype = Path(_filename).suffix

        # Cheking the correct format file
        if _filetype != '.csv':
            error = mo.md(f"Incorrect file type. You upload a '{_filetype}' and a **'.csv'** is expected.").callout(kind='danger')

        else:
            try:
                _df = pandas.read_csv(io.BytesIO(button_file.contents()), index_col=0)

                # Cheking all values are numbers:
                if not _df.apply(pandas.api.types.is_numeric_dtype).all():
                    error = mo.callout("All columns must contain numeric values.", kind='danger')

                # Checking that is a distance matrix and not another type of csv:
                elif _df.shape[0] != _df.shape[1]: # square matrix
                    error = mo.callout('The file must be a square matrix.', kind='alert')

                elif not numpy.allclose(_df.values[:3, :3], _df.values[:3, :3].T): # symetric matrix
                    error = mo.callout('The file must be a symetric matrix.', kind='alert')

                elif list(_df.index[:3]) != list(_df.columns[:3]): # headers (names) match
                    error = mo.callout('The file must be a matrix where row and column names match.', kind='alert')

                else:
                    data = pynei.dists.Distances.from_square_dists(_df)

            # Errors from pandas.read_csv():     
            except ValueError as e:
                error = mo.callout(str(e), kind='alert')

        return data, error

    return (load_csv_dist_matrix,)


@app.cell(hide_code=True)
def _(Path, io, mo, pandas):
    def load_csv_quantitative(button_file, error):
        # Expected input: any kind of CSV
        data = None

        _filename = button_file.value[0].name
        _filetype = Path(_filename).suffix

        if _filetype != '.csv': # format or type
            error = mo.md(f"Incorrect file type. You upload a '{_filetype}' and a **'.csv'** is expected.").callout(kind='danger')

        else: 
            try: 
                _df = pandas.read_csv(io.BytesIO(button_file.contents()), sep=None, engine='python')


                # if _df.empty: # empty file
                #     error = mo.callout("The file is empty.", kind='danger')

                if not _df.apply(pandas.api.types.is_numeric_dtype).all(): # values not number
                    error = mo.callout("All columns must contain numeric values.", kind='danger')

                else:
                    data=_df

            except ValueError as e:
                error = mo.md(str(e)).callout(kind='danger')


        return data, error

    return (load_csv_quantitative,)


@app.cell(hide_code=True)
def _(Path, mo, pynei, tempfile):
    def load_vcf(button_file, error):
        # Except input: a CSV file well structured.
        # pynei.vars_from_vcf needs to read from disk, not memory, so we created a temporary file (tmp) to do so.
        data = None

        _filename = button_file.value[0].name
        _filetype = Path(_filename).suffix

        if _filetype != '.vcf' and _filetype != '.gz':
            error = mo.md(f"Incorrect file type. You upload a '{_filetype}' and a **'.vcf'** or **'.gz'** is expected.").callout(kind='danger')

        else:

            with tempfile.NamedTemporaryFile(delete=False, suffix=".vcf") as tmp:
                tmp.write(button_file.contents()) # Transfer content
                tmp_path = tmp.name # and name file

            try:
                data = pynei.vars_from_vcf(vcf_path=tmp_path) # Extracting variants (snips)

            except ValueError as e:
                error = mo.md(str(e)).callout(kind='danger')
            except KeyError as e:
                error = mo.callout("Not enough samples.", kind='alert')

        return data, error

    return (load_vcf,)


@app.cell
def _(
    DataMode,
    button_file,
    load_csv_dist_matrix,
    load_csv_quantitative,
    load_vcf,
    mode,
):
    data, _error = None, None

    if button_file.value:
        if mode == DataMode.DIST_MATRIX:
            data, _error = load_csv_dist_matrix(button_file, _error)
        if mode == DataMode.QUANTITATIVE:
            data, _error = load_csv_quantitative(button_file, _error)
        if mode == DataMode.GENOMIC:
            data, _error = load_vcf(button_file, _error)

    _error
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

    checkbox_pcoa_speed = mo.ui.checkbox(label='Click to speed up the PCoA (embedding)')

    slider_max_sample_missing = mo.ui.slider(start=0, stop=0.3, step=0.01, value=0.05, include_input=True, label='max_sample_gt_missing_rate')
    slider_max_var_missing = mo.ui.slider(start=0, stop=0.3, step=0.01, value=0.05, include_input=True, label='max_var_gt_missing_rate')
    slider_max_maf = mo.ui.slider(start=0.9, stop=1, step=0.01, value=0.95, include_input=True, label='max_allowed_maf')
    slider_min_r2 = mo.ui.slider(start=0.1, stop=0.2, step=0.01, value=0.1, include_input=True, label='max_allowed_r2')
    # Take care: in pynei the name is 'min_allowed_r2', but we change the name for the user to make easier the interpretation.

    parameters = mo.accordion({"**Show and edit parameters:** ": mo.vstack([slider_max_sample_missing, slider_max_var_missing, slider_max_maf, slider_min_r2])})
    return (
        checkbox_pcoa_speed,
        dropdown_pca_pcoa,
        parameters,
        slider_max_maf,
        slider_max_sample_missing,
        slider_max_var_missing,
        slider_min_r2,
    )


@app.cell
def _(mo):
    # ===================
    # PROGRAMMER CONTROL:
    # ===================
    # True --> Only while programming: Samples for any PCoA reduced to 50
    # False --> Default mode: Samples not altered.

    reduced_samples = False

    _msg=mo.md('')

    if reduced_samples == True:
        _msg = mo.md("You are in **Reduced Samples** mode for faster run tests")
    _msg
    return (reduced_samples,)


@app.cell
def _(DataMode, checkbox_pcoa_speed, dropdown_pca_pcoa, mo, mode, parameters):
    # Controlling the visualization
    _see = mo.md('')

    if mode != DataMode.DIST_MATRIX:
        _widgets = [dropdown_pca_pcoa]

        if dropdown_pca_pcoa.selected_key == 'PCoA':
            _widgets.append(checkbox_pcoa_speed)

        if mode == DataMode.GENOMIC:
            _widgets.append(parameters)

        _see = mo.vstack(_widgets)

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
        color_run_pca_pcoa = 'success' # green

    elif mode == DataMode.QUANTITATIVE:
        color_run_pca_pcoa = 'info' # blue

    else: 
        color_run_pca_pcoa = 'neutral' # grey
        label = 'Run PCoA'

    run_pca_pcoa = mo.ui.run_button(label=label, kind=color_run_pca_pcoa, full_width=True, tooltip='Click to execute the tool (PCA or PCoA) you have selected')
    run_pca_pcoa
    return (run_pca_pcoa,)


@app.cell
def _(
    DataMode,
    button_file,
    checkbox_pcoa_speed,
    data,
    do_pca,
    dropdown_pca_pcoa,
    get_samples_with_enough_data,
    mo,
    mode,
    pynei,
    reduced_samples,
    run_pca_pcoa,
    slider_max_maf,
    slider_max_sample_missing,
    slider_max_var_missing,
    slider_min_r2,
    time,
):
    # PCA or PCoA execution:
    results = None

    if run_pca_pcoa.value and button_file.value:


    # =============== DIST MATRIX ===============
        if mode == DataMode.DIST_MATRIX: 
            results = pynei.do_pcoa(data)


    # =============== QUANTITATIVE ===============    
        elif mode == DataMode.QUANTITATIVE: 

            if dropdown_pca_pcoa.selected_key == 'PCA': 

                with mo.status.spinner(title = "Calculating PCA..."):
                    results = pynei.do_pca(data)

            elif dropdown_pca_pcoa.selected_key == 'PCoA': 

                # For programmer control:
                if reduced_samples:
                    _df50 = data.iloc[:50]  # primeras 50 filas. data es un DataFrame
                    desired_data = pynei.dists.calc_euclidean_pairwise_dists(_df50)
                    results = pynei.do_pcoa(desired_data)
                else:
                    # The correct PCoA for user:
                    data_dists = pynei.dists.calc_euclidean_pairwise_dists(data)
                    results = pynei.do_pcoa(data_dists)



    # =============== GENOMIC ===============        
        elif mode == DataMode.GENOMIC: 

            if dropdown_pca_pcoa.selected_key == 'PCA': 

                with mo.status.spinner(title = "Calculating PCA..."):
                    results = do_pca(
                        data,
                        max_sample_gt_missing_rate = slider_max_sample_missing.value,
                        max_var_gt_missing_rate = slider_max_var_missing.value, 
                        max_allowed_maf = slider_max_maf.value,
                        min_allowed_r2 = slider_min_r2.value
                        )


            elif dropdown_pca_pcoa.selected_key == 'PCoA':

                # For programmer control:
                if reduced_samples:
                    desired_samples = list(data.samples[:50])

                _variants = data # Because we alter the data

                with mo.status.progress_bar(total=5, title="Calculando PCoA...") as _bar:

                    _bar.update(increment=1, subtitle="Filtering samples") # 1
                    _samples = get_samples_with_enough_data(data, max_missing_rate=slider_max_sample_missing.value)

                    if reduced_samples==True: # For programmer control:
                        _samples = [sample for sample in _samples if sample in desired_samples]

                    _variants = pynei.var_filters.filter_samples(data, _samples)

                    _bar.update(increment=1, subtitle="Filtering variants for lost data") # 2
                    time.sleep(1)
                    _variants = pynei.filter_by_missing_data(_variants, max_allowed_missing_rate=slider_max_var_missing.value)

                    _bar.update(increment=1, subtitle="Filtering by LD and MAF") # 3
                    time.sleep(1)
                    _variants = pynei.filter_by_ld_and_maf(_variants, max_allowed_maf=slider_max_maf.value, min_allowed_r2=slider_min_r2.value)

                    _bar.update(increment=1, subtitle="Calculating Kosman Distances (this will take several minutes)") # 4
                    time.sleep(1)
                    kosman_dists = pynei.calc_pairwise_kosman_dists(_variants, use_approx_embedding_algorithm=checkbox_pcoa_speed.value)

                    _bar.update(increment=1, subtitle="Calculating PCoA") # 5
                    time.sleep(0.2)
                    results = pynei.do_pcoa(kosman_dists)
    return data_dists, kosman_dists, results


@app.cell
def _():
    # data.num_samples
    return


@app.cell
def _():
    # total_marcadores = sum(chunk.num_vars for chunk in data.iter_vars_chunks())
    # print(total_marcadores)
    return


@app.cell
def _():
    # ===============================================================================================
    # ============================= P R E P A R I N G   G R A P H I C S =============================
    # ===============================================================================================
    return


@app.cell(hide_code=True)
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


@app.cell(hide_code=True)
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
def _(mo):
    # EXPLAINED VARIANCE - button:
    dropdown_variance = mo.ui.dropdown(options=['10' ,'20', 'all'], value='10', label='Choose how many Principal Components you want to see:')
    return (dropdown_variance,)


@app.cell(hide_code=True)
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
    return (fig_var_exp,)


@app.cell
def _():
    # ===============================================================================================
    # ================================= V I S U A L I Z A T I O N S =================================
    # ===============================================================================================
    return


@app.cell(hide_code=True)
def _(DataMode, dropdown_pca_pcoa, mode, numpy, plt, results):
    if dropdown_pca_pcoa.value == 'PCA' and mode == DataMode.QUANTITATIVE:
        fig_princomps, ax_princomps = plt.subplots()

        ejex = results["princomps"].iloc[0,:]
        ejey = results["princomps"].iloc[1,:]

        plt.scatter(ejex, ejey)

        # Make vectors (or arrows) without loops:
        plt.quiver(
            numpy.zeros_like(ejex),  # X origin (all 0)
            numpy.zeros_like(ejey),  # Y origin (all 0)
            ejex,
            ejey,
            angles='xy',
            scale_units='xy',
            scale=1,
            width=0.005,
            color='red',
            alpha=0.2
        )

        # The variable name at each arrowhead:
        for i, id in enumerate(results["princomps"].columns):
            ldx = results["princomps"].iloc[0,i]
            ldy = results["princomps"].iloc[1,i]

            ax_princomps.text(
            ldx,
            ldy,
            str(id),
            color="red",
            fontsize=10
        )

        plt.title("PCA Biplot")
        plt.xlabel(results["princomps"].index[0])
        plt.ylabel(results["princomps"].index[1])

        plt.axhline(0, color='grey', linewidth=0.5)
        plt.axvline(0, color="grey", linewidth=0.5)

        plt.close()
    return (fig_princomps,)


@app.cell
def _(mo, results):
    if results is not None:
        _msg = mo.md("""## **Results:**""")
    else:
        _msg = mo.md('')

    _msg
    return


@app.cell
def _(mo):
    radio_2d = mo.ui.radio(['Graphs', 'Data'], value='Graphs')
    radio_3d = mo.ui.radio(['Graphs', 'Data'], value='Graphs')
    radio_var = mo.ui.radio(['Graphs', 'Data'], value='Graphs')
    radio_princomps = mo.ui.radio(['Graphs', 'Data'], value='Graphs')
    return radio_2d, radio_3d, radio_princomps, radio_var


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
    radio_princomps,
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
        "Explained variance": mo.vstack([
            radio_var,
            mo.vstack([dropdown_variance, fig_var_exp]) if radio_var.value == 'Graphs' else results["explained_variance (%)"]
        ]),
    }

    if mode == DataMode.QUANTITATIVE and dropdown_pca_pcoa.value=='PCA':
        tabs_dict["Principal components"] = mo.vstack([
            radio_princomps, 
            fig_princomps if radio_princomps.value == 'Graphs' else results["princomps"]
        ])

    mo.ui.tabs(tabs_dict)
    return


@app.cell
def _(data_dists, dropdown_pca_pcoa, mo):
    # Guardar la matriz de distancias de kosman:
    if dropdown_pca_pcoa.value == 'PCoA':
        csv_bytes_from_quantitative = data_dists.square_dists.to_csv().encode()
            # kosman_dists: debería ser una matriz simétrica cuya diagonal son ceros, por lo que se guarda solo la parte triangular inferior.
            # .square_dists: convierte el vector condensado en una matriz cuadrada de formato DataFrame
            # .to_csv(): de Dataframe a string (texto) en formato CSV
            # .encode(): de string a bytes, xq lo pide mo.download()
        _msg = mo.md("If you want to recalculate the **PCoA faster** on the same data in the future, you can download the distance matrix and enter it as an input file later.")
    else: 
        _msg = mo.md('')

    _msg
    return (csv_bytes_from_quantitative,)


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
def _(csv_bytes_from_quantitative, dropdown_pca_pcoa, mo):
    if dropdown_pca_pcoa.value=='PCoA':
        _msg = mo.download(csv_bytes_from_quantitative, filename="kosman_distances.csv", mimetype="text/csv", label='Download distance matrix')
    else:
        _msg = mo.md('')
    _msg
    return


@app.cell
def _(csv_bytes, dropdown_pca_pcoa, mo):
    if dropdown_pca_pcoa.value=='PCoA':
        _msg = mo.download(csv_bytes, filename="kosman_distances.csv", mimetype="text/csv", label='Download distance matrix')
    else:
        _msg = mo.md('')
    _msg
    return


if __name__ == "__main__":
    app.run()
