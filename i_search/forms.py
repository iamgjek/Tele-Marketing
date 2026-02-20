from django import forms
from django.forms import Form
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.forms.utils import ErrorDict

from datetime import date, datetime
from decimal import Decimal
import json, re

class UploadFileForm(forms.Form):
    file = forms.FileField()
