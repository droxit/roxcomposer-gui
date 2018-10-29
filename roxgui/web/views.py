"""Configuration of web views."""

from django.shortcuts import render


def web_main(request):
    """Main page."""
    context = {}
    return render(request, "web/web.html", context)
