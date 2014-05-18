#!/bin/bash

echo 1- Se elimina cualquier tabla con el el nombre sgpdb de la base de datos

sudo -u postgres dropdb mp

echo 2- Creacion de la base de datos

sudo -u postgres createdb mp

echo 3- La base de datos se ha creado con exito

echo 4- Se crean las tablas para el proyecto

python manage.py syncdb