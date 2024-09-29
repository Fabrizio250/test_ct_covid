import os
import re
import requests
import importlib.metadata
import sysconfig
import pkgutil
from jinja2 import Environment, FileSystemLoader

# Trova la radice del repository risalendo nella gerarchia delle directory.
def find_repo_root(start_directory):

    current_directory = os.path.abspath(start_directory)  

    while True:
        if os.path.exists(os.path.join(current_directory, '.git')):
            return current_directory  # Restituisce la directory contenente .git
        parent_directory = os.path.dirname(current_directory)
        if parent_directory == current_directory:  # Se non ci sono più genitori
            break
        current_directory = parent_directory
    return None  # Se non trova la radice del repository

# Restituisce un set di nomi di moduli della libreria standard di Python.
def get_standard_libs():

    standard_libs = set()
    stdlib_path = sysconfig.get_path('stdlib')
    if stdlib_path:
        for _, module_name, _ in pkgutil.iter_modules([stdlib_path]):
            standard_libs.add(module_name)
    return standard_libs


# Estrae le dipendenze dal file requirements.txt.
def parse_requirements(file_path):

    requirements = []
    try:
        with open(file_path, 'r') as file:
            for line in file:
                line = line.strip()
                if line and not line.startswith('#'):
                    requirements.append(line.split('==')[0])  # Rimuovi la versione
    except FileNotFoundError:
        print(f"File {file_path} non trovato.")
    print("Dipendenze lette da requirements.txt:", requirements)  # Debug
    return requirements


# Estrae i moduli importati dal codice sorgente nella directory specificata, escludendo specifici file.
def parse_imports_from_source(directory, excluded_files):
    
    imports = set()
    import_pattern = re.compile(r'^\s*(import|from)\s+([a-zA-Z0-9_.]+)')

    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py') and file not in excluded_files:
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as f:
                    for line in f:
                        match = import_pattern.match(line)
                        if match:
                            module_name = match.group(2).split('.')[0]
                            if module_name:  # Controllo per evitare moduli vuoti
                                imports.add(module_name)

    print("Moduli importati trovati:", imports)  # Debug
    return list(imports)


 #Trova dipendenze sconosciute non presenti in requirements.txt e non standard, escludendo moduli locali.
def find_unknown_dependencies(requirements, imports, standard_libs, excluded_files):

    local_modules = {'maker_software_list', 'maker_soup_list'}
    requirements_set = set(requirements)

    # Moduli da escludere (quelli che causavano errore)
    excluded_dependencies = {'fastapi', 'utils_test', 'tests', 'yaml', 'covidx', 'cv2', 'fastapi[all]', 'itertools'}

    # Filtra importazioni, ignorando quelle locali e quelle standard
    unknown_imports = [imp for imp in imports if imp not in requirements_set and imp not in standard_libs and imp not in excluded_files and imp not in local_modules and imp not in excluded_dependencies ]

    return unknown_imports


# Aggiunge le dipendenze sconosciute al file requirements.txt.
def update_requirements_file(file_path, unknown_dependencies):

    try:
        with open(file_path, 'a') as file:
            for dep in unknown_dependencies:
                file.write(f"{dep}\n")
        print("Dipendenze sconosciute aggiunte a requirements.txt:", unknown_dependencies)  # Debug
    except FileNotFoundError:
        print(f"File {file_path} non trovato. Creazione del file.")
        with open(file_path, 'w') as file:
            for dep in unknown_dependencies:
                file.write(f"{dep}\n")
        print("File requirements.txt creato e dipendenze sconosciute aggiunte.")  # Debug


# Cerca di ottenere il sistema software dal sito PyPI.
def fetch_software_system_from_pypi(package_name):

    url = f"https://pypi.org/pypi/{package_name}/json"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        classifiers = data.get('info', {}).get('classifiers', [])
        for classifier in classifiers:
            if classifier.startswith('Operating System ::'):
                return classifier.split('::')[-1].strip()
        return 'Unknown'
    except requests.exceptions.RequestException as e:
        print(f"Errore nella richiesta di informazioni per {package_name} da PyPI: {e}")
        return 'Unknown'


# Cerca di determinare il linguaggio di programmazione principale di un pacchetto.
def detect_programming_language(package_name):

    try:
        package_spec = importlib.util.find_spec(package_name)
        if package_spec and package_spec.submodule_search_locations:
            package_path = package_spec.submodule_search_locations[0]
            return analyze_files_in_package(package_path)
        return fetch_language_from_pypi(package_name)
    except Exception as e:
        print(f"Errore durante l'analisi del linguaggio per {package_name}: {e}")
        return 'Unknown'


# Analizza i file nel pacchetto per determinare il linguaggio di programmazione principale.
def analyze_files_in_package(package_path):

    file_extensions = {}
    for root, _, files in os.walk(package_path):
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext:
                file_extensions[ext] = file_extensions.get(ext, 0) + 1
    if not file_extensions:
        return 'Unknown'
    main_extension = max(file_extensions, key=file_extensions.get)
    extension_to_language = {
        '.py': 'Python',
        '.c': 'C',
        '.cpp': 'C++',
        '.js': 'JavaScript',
        '.java': 'Java',
        '.rb': 'Ruby',
        '.php': 'PHP',
        '.go': 'Go',
        '.rs': 'Rust',
        '.swift': 'Swift',
        '.kt': 'Kotlin',
    }
    return extension_to_language.get(main_extension, 'Unknown')


 # Cerca di ottenere il linguaggio di programmazione dal sito PyPI.
def fetch_language_from_pypi(package_name):

    url = f"https://pypi.org/pypi/{package_name}/json"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        classifiers = data.get('info', {}).get('classifiers', [])
        for classifier in classifiers:
            if classifier.startswith('Programming Language ::'):
                return classifier.split('::')[-1].strip()
        return 'Unknown'
    except requests.exceptions.RequestException as e:
        print(f"Errore nella richiesta di informazioni per {package_name} da PyPI: {e}")
        return 'Unknown'


def get_last_verified_at_from_pypi(package_name):
    """Cerca di ottenere la data dell'ultima verifica dal sito PyPI."""
    url = f"https://pypi.org/pypi/{package_name}/json"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        # Ottieni la lista degli URL
        urls = data.get('urls', [])
        if urls:  # Controlla se ci sono URL disponibili
            last_modified = urls[0].get('upload_time', 'Unknown')
            return last_modified.split('T')[0]  # Restituisce solo la data
        else:
            return 'Unknown'  # Caso in cui non ci sono URL

    except requests.exceptions.RequestException as e:
        print(f"Errore nella richiesta di informazioni per {package_name} da PyPI: {e}")
        return 'Unknown'

# Funzione per ottenere le informazioni del pacchetto.
def get_package_info(package_name):
    try:
        programming_language = detect_programming_language(package_name)
        software_system = fetch_software_system_from_pypi(package_name)
        last_verified_at = get_last_verified_at_from_pypi(package_name)
        dist = importlib.metadata.distribution(package_name)
        info = {
            'ID': 'unknown',
            'Software System': software_system,
            'Package Name': dist.metadata.get('Name', 'unknown'),
            'Programming Language': programming_language,
            'Version': dist.version,
            'Website': dist.metadata.get('Home-page', 'unknown'),
            'Last verified at': last_verified_at,
            'Risk Level': 'N/A',
            'Requirements': 'N/A',
            'Verification Reasoning': 'N/A'
        }
    except importlib.metadata.PackageNotFoundError:
        programming_language = detect_programming_language(package_name)
        software_system = fetch_software_system_from_pypi(package_name)
        last_verified_at = get_last_verified_at_from_pypi(package_name)
        info = {
            'ID': 'unknown',
            'Software System': software_system,
            'Package Name': package_name,
            'Programming Language': programming_language,
            'Version': 'unknown',
            'Website': 'unknown',
            'Last verified at': last_verified_at,
            'Risk Level': 'unknown',
            'Requirements': 'unknown',
            'Verification Reasoning': 'unknown'
        }
    return info


# Genera la SOUP list con componenti di origine sconosciuta e la restituisce.
def generate_soup_list(requirements, unknown_dependencies):

    soup_list = []

    # Aggiungi componenti già presenti in requirements.txt
    for dep in requirements:
        package_info = get_package_info(dep)
        if package_info:
            soup_list.append(package_info)

    # Aggiungi componenti sconosciuti trovati solo nel codice sorgente
    for dep in unknown_dependencies:
        package_info = get_package_info(dep)
        if package_info:
            soup_list.append(package_info)

    # Assegna ID incrementali
    for index, item in enumerate(soup_list, start=1):
        item['ID'] = index

    # Rimuovi duplicati
    seen = set()
    unique_soup_list = []
    for item in soup_list:
        if (item['Package Name'], item['Software System']) not in seen:
            unique_soup_list.append(item)
            seen.add((item['Package Name'], item['Software System']))

    print("SOUP list generata:", unique_soup_list)  # Debug
    return unique_soup_list


# Genera il contenuto del file markdown basato su una lista SOUP e un template Jinja2.
def generate_soup_list_md(soup_list, template_path, output_md_path):
    if not soup_list:
        print("La SOUP list è vuota.")
        return

    # Ottieni la directory di lavoro corrente
    current_dir = os.path.dirname(os.path.abspath(__file__))
    template_dir = os.path.join(current_dir, os.path.dirname(template_path))
    template_name = os.path.basename(template_path)

    if not os.path.isdir(template_dir):
        print(f"Directory del template {template_dir} non esiste.")
        return

    env = Environment(loader=FileSystemLoader(template_dir))
    try:
        template = env.get_template(template_name)
    except Exception as e:
        print(f"Errore nel caricamento del template: {e}")
        return

    output = template.render(soup_list=soup_list)

    # Assicurati che la directory di output esista
    output_dir = os.path.dirname(output_md_path)
    os.makedirs(output_dir, exist_ok=True)
    with open(output_md_path, 'w') as f:
        f.write(output)
    print(f"File markdown aggiornato: {output_md_path}")

def run_soup_list():
    
    excluded_files = {'maker_software_list.py', 'maker_soup_list.py'} # File da escludere
    source_directory = find_repo_root(os.getcwd())  # root di progetto
    requirements_file = '../../requirements.txt'
    standard_libs = get_standard_libs()
    requirements = parse_requirements(requirements_file)
    source_imports = parse_imports_from_source(source_directory, excluded_files)
    unknown_dependencies = find_unknown_dependencies(requirements, source_imports, standard_libs, excluded_files)
    update_requirements_file(requirements_file, unknown_dependencies)

    # Generazione markdown SOUP list
    soup_list = generate_soup_list(requirements, unknown_dependencies)
    template_path_soup = '../source/template_docs/soup_list_template.md'
    output_md_path_soup = '../md_docs/soup-list.md'
    generate_soup_list_md(soup_list, template_path_soup, output_md_path_soup)