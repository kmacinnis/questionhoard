# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Question.comment'
        db.add_column('questions_question', 'comment',
                      self.gf('django.db.models.fields.TextField')(blank=True, default=''),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Question.comment'
        db.delete_column('questions_question', 'comment')


    models = {
        'questions.choice': {
            'Meta': {'object_name': 'Choice'},
            'choice_expr': ('django.db.models.fields.CharField', [], {'max_length': '240'}),
            'choice_text': ('django.db.models.fields.CharField', [], {'default': "'${choice_expr}$'", 'max_length': '240'}),
            'correct': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'explanation': ('django.db.models.fields.CharField', [], {'max_length': '240'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['questions.Question']"})
        },
        'questions.condition': {
            'Meta': {'object_name': 'Condition'},
            'condition_text': ('django.db.models.fields.CharField', [], {'max_length': '240'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['questions.Question']"})
        },
        'questions.exercise': {
            'Meta': {'object_name': 'Exercise'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['questions.Question']"}),
            'vardict': ('picklefield.fields.PickledObjectField', [], {})
        },
        'questions.question': {
            'Meta': {'object_name': 'Question'},
            'comment': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'date_added': ('django.db.models.fields.DateField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_updated': ('django.db.models.fields.DateField', [], {'blank': 'True', 'auto_now': 'True'}),
            'num_poss': ('django.db.models.fields.IntegerField', [], {}),
            'question_body': ('django.db.models.fields.CharField', [], {'max_length': '240'}),
            'question_code': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'question_name': ('django.db.models.fields.CharField', [], {'max_length': '240', 'unique': 'True'}),
            'question_prompt': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '240'}),
            'symbol_vars': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '240'}),
            'vardicts': ('picklefield.fields.PickledObjectField', [], {})
        },
        'questions.randvar': {
            'Meta': {'object_name': 'RandVar'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['questions.Question']"}),
            'varname': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'varposs': ('django.db.models.fields.CharField', [], {'max_length': '240'})
        }
    }

    complete_apps = ['questions']