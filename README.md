# Petey F PDF generator

Petey F uses [weasyprint](https://weasyprint.org/) to generate PDFs. [Their documentation is pretty good](https://weasyprint.readthedocs.io/en/latest/api.html#python-api), so check it out first.

WeasyPrint takes an HTML/CSS document and converts it to a PDF. On newamerica-cms, the HTML document for a report is rendered using a standard [Django template](https://github.com/newamericafoundation/newamerica-cms/blob/staging/report/templates/report/pdf.html) and [CSS styling](https://github.com/newamericafoundation/newamerica-cms/blob/staging/report/templates/report/pdf_style.html). The rendered HTML is passed to [`weasyprint.HTML`](https://github.com/newamericafoundation/newamerica-cms/blob/staging/report/tasks.py#L21-L23) and the resulting PDF is saved to the report.

And that's really all there is to it.
