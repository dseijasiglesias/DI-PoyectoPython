# -*- coding: utf-8 -*-
 
from distutils.core import setup

files = ["views/*", "views/icons/signed.png", "database.db"]

setup(
    name="Seijas Academy",
    version="1.0",
    description="Software para la asignatura DI",
    author="Daniel Seijas",
    author_email="seijasdeveloper@gmail.com",
    url="url del proyecto",
    packages=["SeijasAcademy"],
    packages_data={"SeijasAcademy": files},
    scripts=["launcher.py"],
    long_description="""Software completo en castellano para la administracion de una academia"""
)

# scripts=["main.py", "panel.py", "informes.py"],
