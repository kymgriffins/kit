from django.shortcuts import render


def api_docs(request):
    """Serve API documentation page."""
    return render(request, 'api_docs.html')


def home(request):
    """Home page - serves the Budget Ndio Story landing page."""
    return render(request, 'home.html')


def index(request):
    """Main index page - serves the main app."""
    return render(request, 'index.html')


def config_page(request):
    """Serve UI configuration page."""
    return render(request, 'config.html')
