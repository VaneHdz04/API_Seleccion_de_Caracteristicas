# ml_app/ml_models.py
import pandas as pd
import numpy as np
import os
import uuid
import json
import io
from django.conf import settings
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score
import matplotlib.pyplot as plt


def train_val_test_split(df, rstate=42, shuffle=True, stratify=None):
    strat = df[stratify] if stratify else None
    train_set, test_set = train_test_split(
        df, test_size=0.4, random_state=rstate, shuffle=shuffle, stratify=strat
    )
    strat = test_set[stratify] if stratify else None
    val_set, test_set = train_test_split(
        test_set, test_size=0.5, random_state=rstate, shuffle=shuffle, stratify=strat
    )
    return (train_set, val_set, test_set)


def remove_labels(df, label_name):
    X = df.drop(label_name, axis=1)
    y = df[label_name].copy()
    return (X, y)


def process_csv_and_run(path_csv, label_column='class', n_estimators=50, top_k=10):
    """
    Lee un CSV, entrena modelos RandomForest con todas las características y con las top_k más importantes.
    Devuelve un diccionario con resultados listos para renderizar en los templates.
    """
    # === 🔹 Leer CSV ===
    df = pd.read_csv(path_csv)

    outputs = {}
    outputs['df_head'] = df.head(10).to_html(classes='table table-sm table-striped', index=False)
    outputs['df_describe'] = df.describe().to_html(classes='table table-sm table-striped')

    # === 🔹 Capturar info() ===
    buf = io.StringIO()
    df.info(buf=buf)
    outputs['df_info'] = buf.getvalue()

    # === 🔹 Verificar existencia de la columna label ===
    if label_column not in df.columns:
        outputs['error'] = f"Columna de etiqueta '{label_column}' no encontrada en el CSV."
        return outputs

    # === 🔹 Convertir etiquetas a valores numéricos ===
    X_full = df.copy()
    X_full[label_column] = X_full[label_column].factorize()[0]

    # === 🔹 División de datos ===
    train_set, val_set, test_set = train_val_test_split(X_full, stratify=label_column)
    X_train, y_train = remove_labels(train_set, label_column)
    X_val, y_val = remove_labels(val_set, label_column)

    # === 🔹 Entrenar modelo con todas las características ===
    clf = RandomForestClassifier(n_estimators=n_estimators, random_state=42, n_jobs=-1)
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_val)
    f1_full = f1_score(y_pred, y_val, average='weighted')
    outputs['f1_full'] = float(f1_full)

    # === 🔹 Importancias de características ===
    importances = clf.feature_importances_
    feature_importances = {
        name: float(score) for name, score in zip(list(X_train.columns), importances)
    }
    feature_importances_sorted = pd.Series(feature_importances).sort_values(ascending=False)
    outputs['feature_importances_sorted_html'] = (
        feature_importances_sorted.head(20)
        .to_frame(name='importance')
        .to_html(classes='table table-sm table-striped')
    )

    # === 🔹 Seleccionar top_k ===
    top_cols = list(feature_importances_sorted.head(top_k).index)
    outputs['top_features'] = top_cols

    # === 🔹 Entrenar modelo reducido ===
    X_train_reduced = X_train[top_cols].copy()
    X_val_reduced = X_val[top_cols].copy()
    clf2 = RandomForestClassifier(n_estimators=n_estimators, random_state=42, n_jobs=-1)
    clf2.fit(X_train_reduced, y_train)
    y_pred2 = clf2.predict(X_val_reduced)
    f1_reduced = f1_score(y_pred2, y_val, average='weighted')
    outputs['f1_reduced'] = float(f1_reduced)

    # === 🔹 Importancias reducidas ===
    outputs['feature_importances_reduced'] = {
        name: float(score) for name, score in zip(top_cols, clf2.feature_importances_)
    }
    outputs['feature_importances_reduced_html'] = (
        pd.Series(outputs['feature_importances_reduced'])
        .sort_values(ascending=False)
        .to_frame(name='importance')
        .to_html(classes='table table-sm table-striped')
    )

    outputs['X_train_reduced_head_html'] = X_train_reduced.head(10).to_html(
        classes='table table-sm table-striped', index=False
    )

    # === 🔹 Identificador de ejecución ===
    run_id = str(uuid.uuid4())
    results_path = os.path.join(os.path.dirname(path_csv), f"results_{run_id}.json")

    # === 🔹 Crear carpeta de plots ===
    plots_dir = os.path.join(settings.MEDIA_ROOT, 'plots')
    os.makedirs(plots_dir, exist_ok=True)

    # === 🔹 Gráfica 1: Importancia de características ===
    plt.figure(figsize=(10, 6))
    top_features = feature_importances_sorted.head(20)
    top_features.plot(kind='barh', color='skyblue')
    plt.gca().invert_yaxis()
    plt.title('Importancia de las Características según Random Forest', fontsize=14)
    plt.xlabel('Importancia')
    plt.ylabel('Características')
    plt.grid(axis='x', linestyle='--', alpha=0.7)

    importance_path = os.path.join(plots_dir, f"importance_{run_id}.png")
    plt.tight_layout()
    plt.savefig(importance_path)
    plt.close()

    # === 🔹 Gráfica 2: Comparativa F1-Score ===
    plt.figure(figsize=(6, 4))
    plt.bar(['Modelo Completo', 'Modelo Reducido'], [f1_full, f1_reduced],
            color=['steelblue', 'lightgreen'])
    plt.title('Comparativa del rendimiento F1-Score', fontsize=14)
    plt.ylabel('F1-Score')
    plt.ylim(0, 1)

    f1_path = os.path.join(plots_dir, f"f1_comparison_{run_id}.png")
    plt.tight_layout()
    plt.savefig(f1_path)
    plt.close()

    # === 🔹 Guardar rutas en el diccionario de salida ===
    outputs['importance_plot_url'] = f"/media/plots/importance_{run_id}.png"
    outputs['f1_plot_url'] = f"/media/plots/f1_comparison_{run_id}.png"

    # === 🔹 Guardar resultados principales ===
    save_dict = {
        'df_head_html': outputs['df_head'],
        'df_describe_html': outputs['df_describe'],
        'df_info_text': outputs['df_info'],
        'f1_full': outputs['f1_full'],
        'feature_importances_sorted_html': outputs['feature_importances_sorted_html'],
        'top_features': outputs['top_features'],
        'f1_reduced': outputs['f1_reduced'],
        'feature_importances_reduced_html': outputs['feature_importances_reduced_html'],
        'X_train_reduced_head_html': outputs['X_train_reduced_head_html'],
    }

    # === ✅ Agregar rutas de las gráficas al JSON ===
    save_dict['importance_plot_url'] = outputs['importance_plot_url']
    save_dict['f1_plot_url'] = outputs['f1_plot_url']

    with open(results_path, 'w', encoding='utf-8') as f:
        json.dump(save_dict, f, ensure_ascii=False, indent=2)

    outputs['run_id'] = run_id
    outputs['results_path'] = results_path

    return outputs
