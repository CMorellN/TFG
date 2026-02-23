import marimo

__generated_with = "0.19.6"
app = marimo.App(width="medium")


@app.cell
def _():
    # IMPORTACIONES:
    import marimo as mo # Para los títulitos
    import numpy as np
    from sklearn.decomposition import PCA
    from sklearn.datasets import load_iris
    import pandas
    import matplotlib.pyplot as plt # Para visualizar (2D al menos)
    import mpl_toolkits.mplot3d # Para visualizar 3D
    import pynei # Librería tutor
    from pathlib import Path
    return PCA, load_iris, mo, np, pandas, plt, pynei


@app.cell(hide_code=True)
def _():
    # # EJEMPLOS DE TEXTO:

    # mo.md("""
    # # This is a title

    # This is normal text.

    # ## This is a subtitle

    # - Bullet point
    # - Another bullet

    # **Bold text**, *italic text*

    # /// details | CLICK ME!
    # You should write the drop-downs in different blocks or they will be overlapping""")

    # mo.md("""/// details | Info details 
    #     type: info
    # Algo extra///""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    # Interacturando con el usuario:
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Slicers y datos
    """)
    return


@app.cell
def _(mo):
    slider = mo.ui.slider(1, 10)
    mo.md(f"Choose a value: {slider}")
    return (slider,)


@app.cell
def _(mo, slider):
    mo.md(f"""
    The last submited value is {slider.value}
    """)
    return


@app.cell
def _(mo):
    abcd = mo.ui.slider(2, 10).form()
    # Si escribo form = mo.ui.slider(1,10).form() aparece bonito y con botoncito
    # mo.md(f"Choose a value: {form}")
    # form
    mo.md(f"Choose a value: {abcd}")
    return (abcd,)


@app.cell
def _(abcd, mo):
    mo.md(f"""
    The last submitted value is {abcd.value}
    """)
    return


@app.cell
def _(mo):
    array = mo.ui.array([
        mo.ui.text(),
        mo.ui.slider(1, 10),
        mo.ui.date()
    ])
    array
    return (array,)


@app.cell
def _(array):
    array.value
    return


@app.cell
def _():
    # Create a form with chaining
    # form = mo.ui.slider(1, 100).form()
    return


@app.cell
def _(mo):
    # Create a form with multiple elements
    form = (
        mo.md('''
        **Your form.**

        {name}

        {date}
    ''')
        .batch(
            name=mo.ui.text(label="name"),
            date=mo.ui.date(label="date"),
        )
        .form(show_clear_button=True, bordered=False)
    )
    mo.md(f"Choose a value: {form}")
    return


@app.cell
def _():
    # mo.md(f"LO elegido es: ***{form}*")
    return


@app.cell
def _():
    # Instantiate a form directly
    # form = mo.ui.form(element=mo.ui.slider(1, 100))
    return


@app.cell
def _(mo):
    mo.md("""
    ## Cargar, mostrar y descargar archivos:
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    **Archivo .txt**
    """)
    return


@app.cell
def _(mo):
    #Crear obj file y botón de carga
    f = mo.ui.file(label='Upload .txt') # Se podrían cargar varios archvios entiendo con mo.ui.file([ , ]). CREO
    f
    return (f,)


@app.cell
def _(f, mo):
    mo.md(f"Nombre archivo: {f.name()}") # Mostrar f.name() es igual a f.value[0].name
    return


@app.cell
def _(f, mo):
    mo.md(f"""Contenido: {f.contents()}""") # Mostrar f.contents() es equivalente a f.value[0].contents
    return


@app.cell
def _(f, mo):
    # DESCARGAR:
    text_download = mo.download(
        data=f.contents,
        filename=f.name(),
        mimetype="text/plain",
        label="Download text",
    )

    mo.hstack([text_download])
    return


@app.cell(hide_code=True)
def _():
    # Ahora quiero aprender a pedirle al usuario el nombre que le quiere poner al archivo antes de descargarlo.
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    # Datos puntitos
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## x_pca
    """)
    return


@app.cell
def _(PCA, np):
    X = np.array([[-1, -1], [-2, -1], [-3, -2], [1, 1], [2, 1], [3, 2]]) # Definir datos

    # Varias definiciones posibles de cómo queremos que sea el PCA:
    # pca = PCA(n_components=2)
    pca = PCA(n_components=1, svd_solver='full')
    # pca = PCA(n_components=1, svd_solver='arpack')

    pca.fit(X) # Ajustar el PCA a los datos
    x_pca = pca.transform(X) # Aplicar el PCA a los datos

    print(pca.explained_variance_ratio_) 
    # En qué %(del 0 al 1) explica o define cada carac. el valor de los datos
    # o Fraccion de varianza total que explica cada componente.
    # o Proporción de información que guarda cada eje
    print(pca.singular_values_) 
    # Magnitud bruta de cada componente 
    # o Tamaño absoluto de cada eje principal
    print(x_pca) # Datos obtenidos del PCA (las nuevas carac. que mejor definen nuestros datos)
    return X, x_pca


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Visualización 2D - *plt.scatter*
    """)
    return


@app.cell
def _(X, np, plt, x_pca):
    y = np.array([0,0,0,0,0,0])

    # Las componentes de X por separado:
    plt.scatter(X[:,0], y, c="blue")
    plt.scatter(y, X[:,1], c="blue")
    # X en su conjunto:
    plt.scatter(X[:,0], X[:,1], c="green")

    # Resultado pca:
    plt.scatter(x_pca[:], y, c="red")
    plt.title("Just points")
    plt.xlabel('sus coord en x')
    plt.ylabel('sus coord en y')
    plt.tight_layout(rect=[0, 0, 0.5, 0.6])
    plt.show()

    #Conclusión: eligió la C1 como dim1 = coord en 'x' xq en 'y' se pierde info de algunos puntos xq se solapan
    return (y,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    # IRIS PCA
    """)
    return


@app.cell
def _(PCA, load_iris):
    iris = load_iris(as_frame=True) # Cargar dataset

    print(f"IRIS KEYS: ", iris.keys()) # Mirar para entender
    #print(f"IRIS DATA: ", iris.data)

    # Hacer PCA:
    pca_iris = PCA(n_components=2)
    pca_iris.fit(iris.data)
    data_pca_iris = pca_iris.transform(iris.data)
    return data_pca_iris, iris


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Visualizaciones 2D - *plt.subplots*
    """)
    return


@app.cell
def _(data_pca_iris, iris, plt):

    # Visualizar 2D:
    fig, axs = plt.subplots(2,2)

    axs[0,0].scatter(data_pca_iris[:,0], data_pca_iris[:,1], c="orange")
    axs[0,0].set_title('data_PCA_iris')
    axs[0,0].set_xlabel('C0 pca')
    axs[0,0].set_ylabel('C1 pca')

    axs[0,1].scatter(iris.data.iloc[:,0], iris.data.iloc[:,1])
    axs[0,1].set_title('Puros datos Iris')
    axs[0,1].set_xlabel('C0 (Sepal length)')
    axs[0,1].set_ylabel('C1 (Sepal width)')

    axs[1,1].scatter(iris.data.iloc[:,0], iris.data.iloc[:,2])
    axs[1,1].set_title('Puros datos Iris')
    axs[1,1].set_xlabel('C0 (Sepal length)')
    axs[1,1].set_ylabel('C2 (Petal length)')

    plt.tight_layout(h_pad=1.5, w_pad=1.5)
    plt.show()
    return


@app.cell(hide_code=True)
def _():
    # FORMAS DE ACCEDER A INFORMACIÓN DE UN DATA FRAME DE PANDAS:
    # # Forma 1:
    print('--> Formas de extraer info de una Data Frame de pandas <--')
    # print(f"Forma 1: ", iris.data.iloc[:,2]) 

    # # Forma 2:
    # df_iris = iris.data
    # print(f"Forma 2: ", df_iris["sepal width (cm)"])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Visualización 3D - *fig.add_subplot*
    """)
    return


@app.cell
def _(PCA, iris, plt):

    # Hacer PCA:
    pca_iris3d = PCA(n_components=3)
    pca_iris3d.fit(iris.data)
    data_pca_iris3d= pca_iris3d.transform(iris.data)

    # Visualizar 3D:
    fig3d = plt.figure() # crear la figura
    ax = fig3d.add_subplot(111, projection='3d') # crear un obj con el que trabajar (necesario para el 3D)

    scatter = ax.scatter(data_pca_iris3d[:,0], data_pca_iris3d[:,1], data_pca_iris3d[:,2], c='purple')
    ax.set_title('Esto qué carajo es')
    ax.set_xlabel('C0')
    ax.set_ylabel('C1')
    ax.set_zlabel('C2')

    # Nos borra los números de las coordenaas. Más limpio
    ax.xaxis.set_ticklabels([])
    ax.yaxis.set_ticklabels([])
    ax.zaxis.set_ticklabels([])

    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    # Entendiendo DO_PCA
    """)
    return


@app.cell
def _(pandas, plt, pynei):
    # Datos
    data3d = pandas.read_csv("XYZdata.txt")

    # do_pca
    do_pca_data3d = pynei.do_pca(data3d)

    # resultados
    projections3d = do_pca_data3d["projections"]
    explained_variance = do_pca_data3d["explained_variance (%)"]
    prin_comps = do_pca_data3d["princomps"]

    # mostrar resultados
    print(f"Projections: \n", projections3d)
    print(f"\nExplained variance: \n", explained_variance)
    print(f"\nPrin_comps: \n", prin_comps)

    # Graficar datos
    figure = plt.figure(layout="constrained")

    ax1 = figure.add_subplot(1,2,1, projection='3d') # para datos originales
    ax2 = figure.add_subplot(1,2,2, projection='3d') # para datos de do_pca

    ax1.scatter(data3d.iloc[:,0], data3d.iloc[:,1], data3d.iloc[:,2])
    ax1.set_title('Datos originales')
    ax1.set_xlabel('eje x')
    ax1.set_ylabel('eje y')
    ax1.set_zlabel('eje z')

    ax2.scatter(projections3d.iloc[:,0], projections3d.iloc[:,1], projections3d.iloc[:,2], c='red')
    ax2.set_title('Projections do_pca')
    ax2.set_xlabel('PC0')
    ax2.set_ylabel('PC1')
    ax2.set_zlabel('PC2')

    # plt.tight_layout(w_pad=5)
    plt.show()
    return data3d, projections3d


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    # Comparaciones entre PCAs
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## **PCA** scikitlearn vs **do_pca** Pynei:
    """)
    return


@app.cell
def _(PCA, data3d, pandas, plt, projections3d, pynei):
    # Data (3D data is on the block before)
    data2d = pandas.read_csv("XYdata.txt")

    # PCA from scikit learn
    pca_data2d = PCA(n_components=2).fit_transform(data2d) # => 2D
    pca_data3d = PCA(n_components=3).fit_transform(data3d) # => 3D

    # do_pca from pynei
    do_pca_data2d = pynei.do_pca(data2d) # => 2D
    projections2d = do_pca_data2d["projections"]
    # do_pca => 3D is already done on the block before

    # Graphing data
    figure2 = plt.figure(figsize=(8,8), layout='constrained')

    aux1 = figure2.add_subplot(3,3,1, projection='3d') # 3D original data //
    aux2 = figure2.add_subplot(3,3,2, projection='3d') # 2D original data in 3D plane
    aux3 = figure2.add_subplot(3,3,3) # 2D original data

    aux4 = figure2.add_subplot(3,3,4, projection='3d') # 3D PCA
    aux5 = figure2.add_subplot(3,3,5, projection='3d') # 2D PCA in 3D plane
    aux6 = figure2.add_subplot(3,3,6) # 2D PCA

    aux7 = figure2.add_subplot(3,3,7, projection='3d') # 3D do_pca
    aux8 = figure2.add_subplot(3,3,8, projection='3d') # 2D do_pca in 3D plane
    aux9 = figure2.add_subplot(3,3,9) # 2D do_pca

    # Original data:
    aux1.scatter(data3d.iloc[:,0], data3d.iloc[:,1], data3d.iloc[:,2]) 
    aux1.set_title('3D original data')
    aux1.set_xlabel('x axis')
    aux1.set_ylabel('y axis')
    aux1.set_zlabel('z axis')

    aux2.scatter(data2d.iloc[:,0], data2d.iloc[:,1])
    aux2.set_title('2D original data')
    aux2.set_xlabel('x axis')
    aux2.set_ylabel('y axis')
    aux2.set_zlabel('z axis')

    aux3.scatter(data2d.iloc[:,0], data2d.iloc[:,1])
    aux3.set_title('2D original data')
    aux3.set_xlabel('x axis')
    aux3.set_ylabel('y axis')

    # PCA:
    aux4.scatter(pca_data3d[:,0], pca_data3d[:,1], pca_data3d[:,2], c='orange')
    aux4.set_title('3D PCA')
    aux4.set_xlabel('PC0')
    aux4.set_ylabel('PC1')
    aux4.set_zlabel('PC2')

    aux5.scatter(pca_data2d[:,0], pca_data2d[:,1], c='orange')
    aux5.set_title('2D PCA')
    aux5.set_xlabel('PC0')
    aux5.set_ylabel('PC1')

    aux6.scatter(pca_data2d[:,0], pca_data2d[:,1], c='orange')
    aux6.set_title('2D PCA')
    aux6.set_xlabel('PC0')
    aux6.set_ylabel('PC1')

    # do_pca:
    aux7.scatter(projections3d.iloc[:,0], projections3d.iloc[:,1], projections3d.iloc[:,2], c='red')
    aux7.set_title('3D do_pca')
    aux7.set_xlabel('PC0')
    aux7.set_ylabel('PC1')
    aux7.set_zlabel('PC2')

    aux8.scatter(projections2d.iloc[:,0], projections2d.iloc[:,1], c='red')
    aux8.set_title('2D do_pca')
    aux8.set_xlabel('PC0')
    aux8.set_ylabel('PC1')

    aux9.scatter(projections2d.iloc[:,0], projections2d.iloc[:,1], c='red')
    aux9.set_title('2D do_pca')
    aux9.set_xlabel('PC0')
    aux9.set_ylabel('PC1')

    # plt.tight_layout(w_pad=5)
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    #Creando funciones:
    """)
    return


@app.cell(hide_code=True)
def _(X, plt, y):
    # Probando a crear una funcion:

    def mi_primera_funcion(datos):
        # Las componentes de X por separado:
        plt.scatter(datos[:,0], y, c="blue")
        plt.scatter(y, datos[:,1], c="blue")
        # X en su conjunto:
        plt.scatter(datos[:,0], datos[:,1], c="green")
        plt.show()
        return

    mi_primera_funcion(X)
    return


if __name__ == "__main__":
    app.run()
