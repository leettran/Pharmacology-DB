# -*- coding: utf-8 -*-
from django import forms
from app.main.criterion import criterion
from app.main.models import Illness, Drug, CompareValue, FarmAction
from lib.mai import Matrix, MAI

class SearchForm(forms.Form):
    type = forms.ChoiceField(choices=criterion.get_matrix_choices())
    strong = forms.BooleanField(required=False)
    farm = forms.ModelChoiceField(queryset=FarmAction.objects.all())
    illness = forms.ModelMultipleChoiceField(queryset=Illness.objects.all(), required=False)
    
    def search(self):
        self._alters = []
        cr_matrix = criterion.get_matrix(int(self.cleaned_data['type']))      
        if not self.cleaned_data['farm']:
            return []
        qs = self._get_qs(self.cleaned_data['farm'], self.cleaned_data['strong'])
        pks = [item.pk for item in qs]
        if not pks:
            return []                
        mai = MAI(cr_matrix, qs)
        for cr in criterion.iter():
            alternative = Matrix()
            print cr[1]
            for drug in qs:
                print drug
                print CompareValue.matrix_row(cr, drug.pk, pks)
                alternative.append(CompareValue.matrix_row(cr, drug.pk, pks))
            self._alters.append({
                'cr': cr,
                'm': alternative
            })
            
            mai.add_alter(alternative)
        return mai.sort() 
    
    def get_alters(self):
        return self._alters
    
    def get_critery(self):
        return criterion.get_critery(int(self.cleaned_data['type']))    
                
    def _get_qs(self, farm, strong):
        illness = self.cleaned_data['illness']
        result = Drug.objects.filter(category=farm)
        result = result.exclude(illnesses__in=illness).distinct('id')
        #if strong:
        #    for item in illness:
        #        result = result.exclude(illnesses=item)
        #else:
            
        return result