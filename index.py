import marimo

__generated_with = "0.21.1"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _(mo):
    mo.vstack([
        mo.md("# Welcome"),
        mo.md("[VCF analysis](http://localhost:2722?mode=genomic)"),
        mo.md("[Quantitative data](http://localhost:2720?mode=quantitative)"),
        mo.md("[Distance matrix](http://localhost:2721?mode=dist_matrix)"),
    ])
    return


if __name__ == "__main__":
    app.run()
