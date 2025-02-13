from flask import Flask, render_template

from app.app import create_app



#FIXAR APP KONTEXTEN VIKTIGT ATT DEN ÄR IMPORTAT FRÅN APP OCH INTE ROUTES ELLER MODELS OSV
app = create_app()


if __name__ == '__main__':
    app.run(debug=True)