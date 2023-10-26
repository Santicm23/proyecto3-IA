
## Proyecto IA 3 - Inferencia Bayesiana

### Dependencias

```
pip install pandas
pip install pyagrum
```

### Ejecución

Para ejecutar el programa, se debe correr un comando con el siguiente formato:

```bash	
python main.py <query> <nombre_tabla1> <direccion_archivo1> ... <nombre_tablaN> <direccion_archivoN>
```

Ejemplo de clase:

```bash
python main.py 'Appointment | none ∧ delayed' rain examples/rain.csv maintenance examples/maintenance.csv appointment examples/appointment.csv train examples/train.csv
```
