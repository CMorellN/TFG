import marimo

__generated_with = "0.19.6"
app = marimo.App(width="medium")


@app.cell
def _():
    # IMPORTACIONES:
    import marimo as mo # Para los titulitos

    import numpy as np
    from sklearn.decomposition import PCA

    import matplotlib.pyplot as plt # Para visualizar (2D al menos)

    from sklearn.datasets import load_iris
    import pandas
    return PCA, load_iris, mo, np, plt


@app.cell(hide_code=True)
def _():
    # EJEMPLOS DE TEXTO:

    # mo.md("""
    # # This is a title

    # This is normal text.

    # ## This is a subtitle

    # - Bullet point
    # - Another bullet

    # **Bold text**, *italic text*
    # """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    # Datos puntitos
    ## *x_pca*
    """)
    return


@app.cell
def _(PCA, np):
    X = np.array([[-1, -1], [-2, -1], [-3, -2], [1, 1], [2, 1], [3, 2]])
    # pca = PCA(n_components=2)
    pca = PCA(n_components=1, svd_solver='full')
    # pca = PCA(n_components=1, svd_solver='arpack')
    pca.fit(X)
    x_pca = pca.transform(X)
    print(pca.explained_variance_ratio_)
    print(pca.singular_values_)
    print(x_pca)
    return X, x_pca


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## *Scatter puntitos solapados:*
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

    #Conclusión: eligió la C1 como dim1 = coord en 'x' xq en 'y' se pierde info de algunos puntos xq se solapan
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    # IRIS PCA
    """)
    return


@app.cell
def _(PCA, load_iris, plt):
    iris = load_iris(as_frame=True)

    print(f"IRIS KEYS: ", iris.keys())
    #print(f"IRIS DATA: ", iris.data)

    pca_iris = PCA(n_components=2)
    pca_iris.fit(iris.data)
    data_pca_iris = pca_iris.transform(iris.data)

    # plt.figure()
    # plt.scatter(data_pca_iris[:,0], data_pca_iris[:,1])
    # plt.title("data_pca_iris")
    # plt.xlabel('C0 pca')
    # plt.ylabel('C1 pca')
    # plt.show()

    # plt.figure()
    # plt.scatter(iris.data.iloc[:,0], iris.data.iloc[:,1])
    # plt.title("Puros datos Iris")
    # plt.xlabel('C0 (Sepal length)')
    # plt.ylabel('C1 (Sepal width)')
    # plt.show()

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


if __name__ == "__main__":
    app.run()
