import os
import json
from datetime import datetime
from jinja2 import Environment, FileSystemLoader


# Funzione per trovare la radice del progetto cercando la directory .git
def find_git_root(start_path):
    current_path = os.path.abspath(start_path)
    
    while current_path != os.path.dirname(current_path):  # Fino a quando non siamo nella radice
        if os.path.isdir(os.path.join(current_path, '.git')):  # Controlla se esiste la cartella .git
            return current_path  # Ritorna la radice del progetto
        current_path = os.path.dirname(current_path)  # Risali alla directory superiore

    return None  # Se non trova la radice del progetto


# Funzione per scansionare tutti i file e raccogliere quelli potenzialmente di configurazione
def scan_project_files():
    config_files = []
    project_root = find_git_root(os.getcwd())  # Inizia dalla directory corrente
    print (project_root)
    if project_root is None:
        print("Errore: Radice del progetto non trovata.")
        return config_files

    for root, dirs, files in os.walk(project_root):  # Usa la radice del progetto
        for file in files:
            if file.endswith((".yml", ".yaml", ".json", ".toml", ".ini", ".cfg", ".config", ".xml", ".conf", ".sh",
                              "Dockerfile", "Makefile")):
                config_files.append(os.path.join(root, file))
    return config_files


# Funzione per dedurre informazioni sui file
def deduce_tool_from_file(file_path):
    if "docker" in file_path.lower():
        return "Docker", "Docker Inc.", "https://www.docker.com/support"
    if "gitlab" in file_path.lower():
        return "GitLab CI", "GitLab Inc.", "https://gitlab.com/gitlab-org/gitlab/issues"
    if "travis" in file_path.lower():
        return "Travis CI", "Travis CI Inc.", "https://github.com/travis-ci/travis-ci/issues"
    if "jenkins" in file_path.lower():
        return "Jenkins", "CloudBees, Inc.", "https://issues.jenkins.io"
    if "tox" in file_path.lower():
        return "Tox", "Tox Devs", "https://github.com/tox-dev/tox/issues"
    if "vscode" in file_path.lower():
        return "Visual Studio Code", "Microsoft", "https://github.com/microsoft/vscode/issues"
    if "idea" in file_path.lower() or "pycharm" in file_path.lower():
        return "PyCharm/IntelliJ IDEA", "JetBrains", "https://youtrack.jetbrains.com/issues/IDEA"
    if "github" in file_path.lower():
        return "GitHub", "GitHub, Inc.", "https://github.com/github/feedback/issues"
    if "makefile" in file_path.lower():
        return "Make", "GNU", "https://savannah.gnu.org/bugs/?group=make"
    return "", "", ""  # Restituisce valori vuoti per file non riconosciuti


# Funzione per ottenere la data corrente in formato YYYY-MM-DD
def get_current_date():
    return datetime.now().strftime('%Y-%m-%d')


# Funzione per caricare lo stato precedente della Software List da un file JSON
def load_previous_state(file_path='previous_software_list.json'):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return json.load(file)
    return {}


# Funzione per salvare lo stato corrente della Software List in un file JSON
def save_current_state(software_list, file_path='previous_software_list.json'):
    with open(file_path, 'w') as file:
        json.dump(software_list, file, indent=4)


# Funzione per costruire la Software List in modo generico senza duplicati
def build_generic_software_list():
    software_list = []
    seen_tools = set()  # Set per tenere traccia dei tool già aggiunti
    config_files = scan_project_files()

    for idx, file_path in enumerate(config_files, start=1):
        tool_name, manufacturer, bug_tracker_url = deduce_tool_from_file(file_path)

        # Aggiungi alla lista solo se il tool è riconosciuto e non è già stato inserito
        if tool_name and tool_name not in seen_tools:
            software_list.append({
                'ID': idx,
                'Name': tool_name,
                'Manufacturer': manufacturer,
                'Bug tracker URL': bug_tracker_url,
                'Needs validation?': '-',
                'Next validation': '-',  # non deducibile direttamente
                'Last validation': get_current_date(),
                'Decommissioning': '-'  # inizialmente vuoto
            })
            seen_tools.add(tool_name)  # Aggiungi il tool al set per evitare duplicati

    return software_list


# Funzione per identificare strumenti dismessi
def identify_decommissioned_tools(current_list, previous_list):
    decommissioned_tools = []

    # Crea un dizionario dei tool correnti per nome per facilitare la ricerca
    current_tool_names = {tool['Name'] for tool in current_list}

    # Trova i tool che erano nel passato ma non sono più presenti
    for previous_tool in previous_list:
        if previous_tool['Name'] not in current_tool_names:
            previous_tool['Decommissioning'] = get_current_date()  # Imposta la data di decommisioning
            decommissioned_tools.append(previous_tool)

    return decommissioned_tools


# Funzione per salvare la Software List in un file markdown usando Jinja2
def save_software_list_to_markdown(software_list, template_path, output_path):
    if not software_list:
        print("La lista del software è vuota.")
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
        # Carica il template
        template = env.get_template(template_name)

        # Renderizza il template con i dati
        rendered_content = template.render(software_list=software_list)

        # Assicurati che la directory di output esista
        output_dir = os.path.dirname(output_path)
        os.makedirs(output_dir, exist_ok=True)

        # Salva il contenuto renderizzato nel file di output
        with open(output_path, 'w') as file:
            file.write(rendered_content)

        print(f"File {output_path} aggiornato con successo.")

    except FileNotFoundError as e:
        print(f"Errore: {e}")
    except Exception as e:
        print(f"Si è verificato un errore: {e}")



# Funzione per eseguire il primo script
def run_software_list():
    template_path = '../source/template_docs/software_list_template.md'
    output_path = '../md_docs/software-list.md'

    previous_software_list = load_previous_state()
    current_software_list = build_generic_software_list()
    decommissioned_tools = identify_decommissioned_tools(current_software_list, previous_software_list)
    complete_software_list = current_software_list + decommissioned_tools
    save_current_state(current_software_list)
    save_software_list_to_markdown(complete_software_list, template_path, output_path)


# Esegui la funzione principale
if __name__ == "__main__":
    run_software_list()
