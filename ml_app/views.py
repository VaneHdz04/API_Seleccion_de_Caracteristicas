# ml_app/views.py
from django.shortcuts import render, redirect
from django.conf import settings
from django.urls import reverse
from .forms import UploadCSVForm
from .ml_models import process_csv_and_run
import os
import json

def index_view(request):
    """
    Muestra index.html con formulario para subir el CSV.
    """
    form = UploadCSVForm()
    return render(request, 'index.html', {'form': form})


def procesar_view(request):
    """
    Recibe POST con archivo CSV, lo guarda en MEDIA_ROOT/uploads/,
    llama a process_csv_and_run, luego redirige a resultados/<run_id>/
    """
    if request.method == 'POST':
        form = UploadCSVForm(request.POST, request.FILES)
        if form.is_valid():
            f = form.cleaned_data['file']
            uploads_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')
            os.makedirs(uploads_dir, exist_ok=True)
            file_path = os.path.join(uploads_dir, f.name)

            # Guardar archivo
            with open(file_path, 'wb+') as dest:
                for chunk in f.chunks():
                    dest.write(chunk)

            # Ejecutar pipeline (esto puede tardar)
            outputs = process_csv_and_run(
                file_path,
                label_column='calss',  # ⚠️ Verifica si realmente es 'calss' o 'class'
                n_estimators=50,
                top_k=10
            )

            if 'error' in outputs:
                return render(request, 'index.html', {'form': form, 'error': outputs['error']})

            run_id = outputs.get('run_id')
            # Redirigir a la página de resultados
            return redirect(reverse('ml_app:resultados', kwargs={'run_id': run_id}))

    else:
        form = UploadCSVForm()

    return render(request, 'index.html', {'form': form})


def resultados_view(request, run_id):
    """
    Lee el JSON generado y lo muestra en resultados.html
    """
    # Localizar archivo
    results_file = None

    for root in [settings.MEDIA_ROOT, os.path.join(settings.MEDIA_ROOT, 'uploads')]:
        candidate = os.path.join(root, f"results_{run_id}.json")
        if os.path.exists(candidate):
            results_file = candidate
            break

    if not results_file:
        return render(request, 'resultados.html', {'error': 'Resultados no encontrados.'})

    with open(results_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Pasar datos al template
    context = {
        'df_head_html': data.get('df_head_html'),
        'df_describe_html': data.get('df_describe_html'),
        'df_info_text': data.get('df_info_text'),
        'f1_full': data.get('f1_full'),
        'feature_importances_sorted_html': data.get('feature_importances_sorted_html'),
        'top_features': data.get('top_features'),
        'f1_reduced': data.get('f1_reduced'),
        'feature_importances_reduced_html': data.get('feature_importances_reduced_html'),
        'X_train_reduced_head_html': data.get('X_train_reduced_head_html'),
        'importance_plot_url': data.get('importance_plot_url'),
        'f1_plot_url': data.get('f1_plot_url'),
    }

    return render(request, 'resultados.html', context)
