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
        mo.md(f"{mo.icon('lucide:leaf', color='green')}[ Genomic analysis (VCF)](https://cmorelln.github.io/TFG/app.html?mode=genomic)"),
        mo.md(f"[Quantitative data (CSV)](https://cmorelln.github.io/TFG/app.html?mode=quantitative) {mo.icon('lucide:alarm-clock', color='red')}"),
        mo.md("[Distance matrix (CSV)](https://cmorelln.github.io/TFG/app.html?mode=dist_matrix)"),
    ]).center()
    return


@app.cell
def _():
    return


@app.cell
def _(mo):
    mo.Html("""
    <div><a href="https://cmorelln.github.io/TFG/app.html?mode=dist_matrix">
        <button>Genomic</button></a>
    
    <div><a href="https://cmorelln.github.io/TFG/app.html?mode=dist_matrix">
        <button>Quantitative</button></a>
    
    <div><a href="https://cmorelln.github.io/TFG/app.html?mode=dist_matrix">
        <button>Dist Kosman</button></a>
    """)
    return


@app.cell
def _(mo):
    mo.md(f"""
    # {mo.icon('lucide:leaf', color='green')} Leaf
    """)
    return


@app.cell
def _(mo):
    mo.ui.button(
        label=f"{mo.icon('lucide:rocket', color='red')} Submit",
    )
    return


if __name__ == "__main__":
    app.run()
