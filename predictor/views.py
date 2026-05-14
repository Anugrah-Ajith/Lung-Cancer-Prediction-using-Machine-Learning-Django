"""
Views for the lung cancer predictor app.
"""
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import PredictionForm
from .ml_models import predict, load_results


def home_view(request):
    """Landing page with project overview."""
    results = load_results()
    model_accuracies = {}
    if results:
        for name in ['Logistic Regression', 'Decision Tree', 'Random Forest', 'SVM', 'KNN', 'Naive Bayes']:
            if name in results:
                model_accuracies[name] = results[name]['accuracy']
    
    context = {
        'model_accuracies': model_accuracies,
    }
    return render(request, 'predictor/home.html', context)


@login_required
def predict_view(request):
    """Handle prediction form and display results."""
    if request.method == 'POST':
        form = PredictionForm(request.POST)
        if form.is_valid():
            # Get form data
            input_data = form.cleaned_data
            
            # Run prediction
            result = predict(input_data)
            
            if result is None:
                messages.error(request, 'ML models are not trained yet. Please run train_models.py first.')
                return redirect('predict')
            
            context = {
                'result': result,
                'input_data': input_data,
                'form': form,
            }
            return render(request, 'predictor/results.html', context)
        else:
            messages.error(request, 'Please correct the errors in the form.')
    else:
        form = PredictionForm()
    
    return render(request, 'predictor/predict.html', {'form': form})


@login_required
def results_view(request):
    """Display model accuracy comparison."""
    results = load_results()
    if results is None:
        messages.warning(request, 'No model results available. Please train the models first.')
        return redirect('home')
    
    context = {
        'results': results,
    }
    return render(request, 'predictor/accuracy.html', context)
