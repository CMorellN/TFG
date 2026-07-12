import marimo

__generated_with = "0.23.6"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _(mo):
    mo.vstack([
        mo.md("# Welcome"),
        mo.md(f"[ Genomic analysis (VCF)](https://cmorelln.github.io/TFG/app.html?mode=genomic)"),
        mo.md(f"[Quantitative data (CSV)](https://cmorelln.github.io/TFG/app.html?mode=quantitative)"),
        mo.md("[Distance matrix (CSV)](https://cmorelln.github.io/TFG/app.html?mode=dist_matrix)"),
    ]).center()
    return


if __name__ == "__main__":
    app.run()
