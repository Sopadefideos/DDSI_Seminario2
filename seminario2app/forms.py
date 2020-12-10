from django import forms


class addPedido(forms.Form):
    cliente = forms.CharField()
    producto = forms.IntegerField()
    cantidad = forms.IntegerField()