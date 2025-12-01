import os
import math
from distutils.log import debug
from fileinput import filename
from flask import *
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['CARGAR_ARCHIVO'] = "subida"
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 2

@app.route('/')  
def main():  
    return render_template("index.html")

@app.route('/rename',methods=['POST'])
def rename():
    old = request.form["oldname"]
    new = secure_filename(request.form["newname"])
    old_path = os.path.join(app.config['CARGAR_ARCHIVO'], old)
    print(os.path.exists(old_path))
    new_path = os.path.join(app.config['CARGAR_ARCHIVO'], new)
    os.rename(old_path, new_path)
    return ver_archivos()
    
@app.route('/reload_index',methods=['POST'])
def reload_index():
    return render_template("index.html")
           
@app.route('/upload_file', methods = ['POST'])  
def upload_file():  
    if request.method == 'POST':  
        f = request.files['file']
        safe_name = os.path.join(app.config['CARGAR_ARCHIVO'],secure_filename(f.filename))
        f.save(safe_name)
        return render_template("subida_correcta_archivos.html", name = safe_name)  

@app.route('/delete', methods = ['POST'])
def delete_file():
    none = request.form["to_be_deleted"]
    file_path = os.path.join(app.config['CARGAR_ARCHIVO'], none)
    try:
        
        os.remove(file_path)
        return render_template("archivo_eliminado_correctamente.html")
    except FileNotFoundError:
        return 'Archivo no encontrado.', 404

@app.route('/view', methods = ['POST'])
def ver_archivos():
    selected = {}
    pesos = 0

    if request.method == "POST":
        seleccionados = request.form.getlist("selected")
        selected = {s:valor_archivos(s) for s in seleccionados}
        pesos = sum(selected.values())
        selected = {k: (format_size(v)) for k, v in selected.items()}
    archivos = os.listdir(app.config['CARGAR_ARCHIVO'])
    return render_template("Visor_archivos.html", files = archivos, num_archivos = len(archivos), selected=selected, pesos=format_size(pesos) )

def valor_archivos(archivo):
    path = os.path.join(app.config['CARGAR_ARCHIVO'], archivo)
    size = os.path.getsize(path)
    return size

def format_size(size_bytes, decimals=2):

    if size_bytes == 0:
        return "0 Bytes"
    
    power = 1024
    units = ["Bytes", "KB", "MB", "GB", "TB", "PB"]
    i = int(math.floor(math.log(size_bytes, power)))
    
    return f"{size_bytes / (power ** i):.{decimals}f} {units[i]}"



if __name__ == "__main__":
     app.run(host="0.0.0.0", port=5000)
     

