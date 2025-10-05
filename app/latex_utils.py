import os
import subprocess
import tempfile

def latex_to_pdf(latex_code: str) -> str:
    """
    Saves LaTeX code to a temporary .tex file, compiles it with pdflatex,
    and returns the path to the generated PDF.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        tex_path = os.path.join(tmpdir, "resume.tex")
        pdf_path = os.path.join(tmpdir, "resume.pdf")

        # Write the LaTeX code to file
        with open(tex_path, "w", encoding="utf-8") as f:
            f.write(latex_code)

        # Compile the LaTeX file to PDF
        try:
            subprocess.run(
                ["pdflatex", "-interaction=nonstopmode", tex_path],
                cwd=tmpdir,
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        except subprocess.CalledProcessError as e:
            raise RuntimeError("LaTeX compilation failed") from e

        if not os.path.exists(pdf_path):
            raise FileNotFoundError("PDF generation failed")

        # Move PDF to a persistent temp file
        final_pdf = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        with open(pdf_path, "rb") as src, open(final_pdf.name, "wb") as dst:
            dst.write(src.read())

        return final_pdf.name
