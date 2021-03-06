# -*- encoding: utf-8 -*-
"""
Argon Dashboard - coded in Flask

Author  : AppSeed App Generator
Design  : Creative-Tim.com
License : MIT 
Support : https://appseed.us/support 
"""

# used by the static export
import click
from   flask_frozen import Freezer

from app import app

# define custom command 
@app.cli.command()
def build():
    freezer = Freezer(app)
    freezer.freeze()

if __name__ == "__main__":
    app.run(debug=True) 
