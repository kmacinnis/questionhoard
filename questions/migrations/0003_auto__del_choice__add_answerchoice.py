# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Choice'
        db.delete_table('questions_choice')

        # Adding model 'AnswerChoice'
        db.create_table('questions_answerchoice', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['questions.Question'])),
            ('choice_text', self.gf('django.db.models.fields.CharField')(default='${choice_expr}$', max_length=240)),
            ('choice_expr', self.gf('django.db.models.fields.CharField')(max_length=240)),
            ('correct', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('explanation', self.gf('django.db.models.fields.CharField')(max_length=240)),
        ))
        db.send_create_signal('questions', ['AnswerChoice'])


    def backwards(self, orm):
        # Adding model 'Choice'
        db.create_table('questions_choice', (
            ('correct', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('explanation', self.gf('django.db.models.fields.CharField')(max_length=240)),
            ('choice_text', self.gf('django.db.models.fields.CharField')(default='${choice_expr}$', max_length=240)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('choice_expr', self.gf('django.db.models.fields.CharField')(max_length=240)),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['questions.Question'])),
        ))
        db.send_create_signal('questions', ['Choice'])

        # Deleting model 'AnswerChoice'
        db.delete_table('questions_answerchoice')


    models = {
        'questions.answerchoice': {
            'Meta': {'object_name': 'AnswerChoice'},
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
            'question_prompt': ('django.db.models.fields.CharField', [], {'max_length': '240', 'blank': 'True'}),
            'symbol_vars': ('django.db.models.fields.CharField', [], {'max_length': '240', 'blank': 'True'}),
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