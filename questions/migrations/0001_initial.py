# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Question'
        db.create_table('questions_question', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('question_name', self.gf('django.db.models.fields.CharField')(max_length=240, unique=True)),
            ('question_code', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('question_prompt', self.gf('django.db.models.fields.CharField')(max_length=240, blank=True)),
            ('question_body', self.gf('django.db.models.fields.CharField')(max_length=240)),
            ('symbol_vars', self.gf('django.db.models.fields.CharField')(max_length=240, blank=True)),
            ('date_added', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('last_updated', self.gf('django.db.models.fields.DateField')(blank=True, auto_now=True)),
            ('vardicts', self.gf('picklefield.fields.PickledObjectField')()),
            ('num_poss', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('questions', ['Question'])

        # Adding model 'RandVar'
        db.create_table('questions_randvar', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['questions.Question'])),
            ('varname', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('varposs', self.gf('django.db.models.fields.CharField')(max_length=240)),
        ))
        db.send_create_signal('questions', ['RandVar'])

        # Adding model 'Condition'
        db.create_table('questions_condition', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['questions.Question'])),
            ('condition_text', self.gf('django.db.models.fields.CharField')(max_length=240)),
        ))
        db.send_create_signal('questions', ['Condition'])

        # Adding model 'Choice'
        db.create_table('questions_choice', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['questions.Question'])),
            ('choice_text', self.gf('django.db.models.fields.CharField')(max_length=240, default='${choice_expr}$')),
            ('choice_expr', self.gf('django.db.models.fields.CharField')(max_length=240)),
            ('correct', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('explanation', self.gf('django.db.models.fields.CharField')(max_length=240)),
        ))
        db.send_create_signal('questions', ['Choice'])

        # Adding model 'Exercise'
        db.create_table('questions_exercise', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['questions.Question'])),
            ('vardict', self.gf('picklefield.fields.PickledObjectField')()),
        ))
        db.send_create_signal('questions', ['Exercise'])


    def backwards(self, orm):
        # Deleting model 'Question'
        db.delete_table('questions_question')

        # Deleting model 'RandVar'
        db.delete_table('questions_randvar')

        # Deleting model 'Condition'
        db.delete_table('questions_condition')

        # Deleting model 'Choice'
        db.delete_table('questions_choice')

        # Deleting model 'Exercise'
        db.delete_table('questions_exercise')


    models = {
        'questions.choice': {
            'Meta': {'object_name': 'Choice'},
            'choice_expr': ('django.db.models.fields.CharField', [], {'max_length': '240'}),
            'choice_text': ('django.db.models.fields.CharField', [], {'max_length': '240', 'default': "'${choice_expr}$'"}),
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
            'date_added': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
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