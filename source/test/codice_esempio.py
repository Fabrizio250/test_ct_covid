# Importa le librerie necessarie
import pandas as pd  # per manipolare i dati
import numpy as np  # per operazioni numeriche
import matplotlib.pyplot as plt  # per la creazione di grafici
import seaborn as sns  # per grafici avanzati
from scipy import stats  # per statistiche avanzate
from datetime import datetime  # per manipolare date e ore
import json  # per lavorare con file JSON
import logging  # per il logging



# Configura il logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_csv(file_path):
    """Carica i dati da un file CSV."""
    logging.info(f'Loading data from {file_path}')
    return pd.read_csv(file_path)

def preprocess_data(df):
    """Prepara i dati per l'analisi."""
    logging.info('Preprocessing data')
    df['age'] = df['age'].astype(int)
    df['score'] = df['score'].astype(float)
    return df

def calculate_statistics(df):
    """Calcola statistiche sui dati."""
    logging.info('Calculating statistics')
    stats_summary = {
        'mean_age': np.mean(df['age']),
        'mean_score': np.mean(df['score']),
        'median_score': np.median(df['score']),
        'std_score': np.std(df['score']),
        'mode_age': stats.mode(df['age'])[0][0],
        'correlation': df[['age', 'score']].corr().iloc[0, 1]
    }
    return stats_summary

def generate_plots(df):
    """Genera e salva grafici basati sui dati."""
    logging.info('Generating plots')

    # Imposta lo stile del grafico
    sns.set(style='whitegrid')

    # Grafico a dispersione
    plt.figure(figsize=(12, 6))
    sns.scatterplot(x='age', y='score', data=df, hue='name', s=100, palette='viridis')
    plt.title('Age vs Score')
    plt.xlabel('Age')
    plt.ylabel('Score')
    plt.legend(title='Name')
    plt.savefig('scatter_plot.png')
    plt.show()

    # Istogramma dei punteggi
    plt.figure(figsize=(12, 6))
    sns.histplot(df['score'], bins=10, kde=True)
    plt.title('Distribution of Scores')
    plt.xlabel('Score')
    plt.ylabel('Frequency')
    plt.savefig('histogram.png')
    plt.show()

def save_statistics(stats, file_path):
    """Salva le statistiche in un file JSON."""
    logging.info(f'Saving statistics to {file_path}')
    with open(file_path, 'w') as f:
        json.dump(stats, f, indent=4)

def main():
    """Funzione principale per eseguire il flusso di lavoro."""
    start_time = datetime.now()
    logging.info(f'Starting process at {start_time}')

    file_path = 'data/sample_data.csv'
    df = load_csv(file_path)
    df = preprocess_data(df)

    stats_summary = calculate_statistics(df)
    print('Statistics Summary:')
    for key, value in stats_summary.items():
        print(f'{key}: {value}')

    generate_plots(df)
    save_statistics(stats_summary, 'data/statistics_summary.json')

    end_time = datetime.now()
    logging.info(f'Process completed at {end_time}')
    logging.info(f'Total runtime: {end_time - start_time}')

if __name__ == '__main__':
    main()
