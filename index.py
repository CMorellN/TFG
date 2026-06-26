import marimo

__generated_with = "0.23.6"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _():
    # mo.vstack([
    #     mo.md("# Welcome"),
    #     mo.md(f"{mo.icon('lucide:leaf', color='green')}[ Genomic analysis (VCF)](https://cmorelln.github.io/TFG/app.html?mode=genomic)"),
    #     mo.md(f"[Quantitative data (CSV)](https://cmorelln.github.io/TFG/app.html?mode=quantitative) {mo.icon('lucide:alarm-clock', color='red')}"),
    #     mo.md("[Distance matrix (CSV)](https://cmorelln.github.io/TFG/app.html?mode=dist_matrix)"),
    # ]).center()
    return


@app.cell
def _(mo):
    mo.Html("""
        <div style="font-family: sans-serif; background: #f5f0e8; min-height: 100vh; margin: 0; padding: 0;">

          <div style="width: 100%; height: 180px; overflow: hidden; position: relative; background: linear-gradient(135deg, #0a2240 0%, #1a4a6e 50%, #0d3352 100%);">
            <div style="position: absolute; inset: 0; display: flex; align-items: center; justify-content: space-between; padding: 0 3rem;">
              <div>
                <p style="color: #a8c8e8; font-size: 13px; letter-spacing: 0.1em; text-transform: uppercase; margin: 0 0 8px;">Population genetics</p>
                <h1 style="color: #ffffff; font-size: 28px; font-weight: 500; margin: 0; line-height: 1.2;">Web app for geneticists</h1>
                <p style="color: #7fb3d3; font-size: 14px; margin: 8px 0 0;">PCA and PCoA analysis without installing anything</p>
              </div>
              <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/4/4c/DNA_Structure%2BKey%2BLabelled.pn_NoBB.png/220px-DNA_Structure%2BKey%2BLabelled.pn_NoBB.png"
                   alt="DNA double helix"
                   style="height: 160px; opacity: 0.85;">
            </div>
            <div style="position: absolute; bottom: 0; left: 0; right: 0; height: 3px; background: linear-gradient(90deg, #1a6b4a, #2196a0, #1a4a6e);"></div>
          </div>

          <div style="max-width: 700px; margin: 0 auto; padding: 2.5rem 2rem;">
            <p style="color: #5a5a52; font-size: 15px; line-height: 1.7; margin: 0 0 2.5rem; text-align: center;">
              Upload your genomic or phenotypic data and explore population structure through interactive PCA and PCoA plots. No installation required — everything runs in your browser.
            </p>

            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 1.25rem;">

              <div style="background: #ffffff; border: 0.5px solid #d4cfc4; border-radius: 12px; padding: 1.5rem 1.25rem; display: flex; flex-direction: column; align-items: center; text-align: center;">
                <h2 style="font-size: 15px; font-weight: 500; color: #2c2c2a; margin: 0 0 0.5rem;">Genomic</h2>
                <p style="font-size: 13px; color: #888780; line-height: 1.5; margin: 0 0 1.25rem;">VCF files — SNP-based PCA and PCoA with Kosman distances</p>
                <a href="app.html?mode=genomic" style="display: block; width: 100%; box-sizing: border-box; padding: 0.6rem; background: #1a6b4a; color: #ffffff; border-radius: 6px; text-decoration: none; font-size: 13px; font-weight: 500; text-align: center;">Open</a>
              </div>

              <div style="background: #ffffff; border: 0.5px solid #d4cfc4; border-radius: 12px; padding: 1.5rem 1.25rem; display: flex; flex-direction: column; align-items: center; text-align: center;">
                <h2 style="font-size: 15px; font-weight: 500; color: #2c2c2a; margin: 0 0 0.5rem;">Quantitative</h2>
                <p style="font-size: 13px; color: #888780; line-height: 1.5; margin: 0 0 1.25rem;">CSV files — morphological or phenotypic data PCA</p>
                <a href="app.html?mode=quantitative" style="display: block; width: 100%; box-sizing: border-box; padding: 0.6rem; background: #185fa5; color: #ffffff; border-radius: 6px; text-decoration: none; font-size: 13px; font-weight: 500; text-align: center;">Open</a>
              </div>

              <div style="background: #ffffff; border: 0.5px solid #d4cfc4; border-radius: 12px; padding: 1.5rem 1.25rem; display: flex; flex-direction: column; align-items: center; text-align: center;">
                <h2 style="font-size: 15px; font-weight: 500; color: #2c2c2a; margin: 0 0 0.5rem;">Distance matrix</h2>
                <p style="font-size: 13px; color: #888780; line-height: 1.5; margin: 0 0 1.25rem;">CSV files — PCoA directly from a precomputed distance matrix</p>
                <a href="app.html?mode=dist_matrix" style="display: block; width: 100%; box-sizing: border-box; padding: 0.6rem; background: #854f0b; color: #ffffff; border-radius: 6px; text-decoration: none; font-size: 13px; font-weight: 500; text-align: center;">Open</a>
              </div>

            </div>

            <div style="margin-top: 2.5rem; padding: 1rem 1.25rem; background: #eef5f1; border-left: 3px solid #1a6b4a; border-radius: 0 6px 6px 0;">
              <p style="font-size: 13px; color: #3b6d11; margin: 0; line-height: 1.6;">
                <strong>Data privacy:</strong> Your files are processed entirely in your browser. No data is sent to any server or stored anywhere.
              </p>
            </div>
          </div>
        </div>
        """)
    return


if __name__ == "__main__":
    app.run()
