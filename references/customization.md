# Customization

## Adding New Themes

1. **Create HTML template** in `assets/templates/your-theme.html`:
   ```html
   <!DOCTYPE html>
   <html lang="en">
   <head>
       <meta charset="UTF-8">
       <meta name="viewport" content="width=device-width, initial-scale=1.0">
       <title>Resume</title>
       <style>
           {{CSS}}
       </style>
   </head>
   <body>
       <div class="resume-container">
           {{CONTENT}}
       </div>
   </body>
   </html>
   ```

2. **Create CSS file** in `assets/css/your-theme.css`

3. **Register theme** in `scripts/generate_html.py`:
   Add your theme name to the `--theme` argument's `choices` list.

## Adding New Languages

1. **Register language code** in `scripts/generate_html.py`:
   Add to the `--lang` argument's `choices` list.

2. **Add translations** to the `SECTION_TITLES` dictionary in `scripts/generate_html.py`.

3. **Test**: `python3 scripts/generate_html.py --theme modern --lang your-lang resume.json output.html`

## Modifying Resume Data Structure

To add custom fields:

1. Update the JSON schema in your resume data file
2. Add HTML generation logic in `scripts/generate_html.py` for the new section
3. Add CSS styles for the custom section in your theme's CSS file

## Exporting to Other Formats

- **Markdown**: `pandoc resume.html -o resume.md`
- **Word**: `pandoc resume.html -o resume.docx`
- **Plain Text**: `html2text resume.html > resume.txt`
