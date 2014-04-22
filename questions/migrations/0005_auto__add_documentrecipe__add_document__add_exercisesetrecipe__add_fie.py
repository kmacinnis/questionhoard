# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'DocumentRecipe'
        db.create_table('questions_documentrecipe', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('date_created', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('questions', ['DocumentRecipe'])

        # Adding model 'Document'
        db.create_table('questions_document', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('recipe', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['questions.DocumentRecipe'])),
            ('date_created', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal('questions', ['Document'])

        # Adding model 'ExerciseSetRecipe'
        db.create_table('questions_exercisesetrecipe', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('document', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['questions.DocumentRecipe'])),
            ('order', self.gf('django.db.models.fields.IntegerField')()),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['questions.Question'])),
            ('num_exercises', self.gf('django.db.models.fields.IntegerField')()),
            ('num_columns', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('space_after', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal('questions', ['ExerciseSetRecipe'])

        # Adding field 'Question.created_by'
        db.add_column('questions_question', 'created_by',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], default=1),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'DocumentRecipe'
        db.delete_table('questions_documentrecipe')

        # Deleting model 'Document'
        db.delete_table('questions_document')

        # Deleting model 'ExerciseSetRecipe'
        db.delete_table('questions_exercisesetrecipe')

        # Deleting field 'Question.created_by'
        db.delete_column('questions_question', 'created_by_id')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True', 'symmetrical': 'False'})
        },
        'auth.permission': {
            'Meta': {'object_name': 'Permission', 'unique_together': "(('content_type', 'codename'),)", 'ordering': "('content_type__app_label', 'content_type__model', 'codename')"},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'user_set'", 'blank': 'True', 'to': "orm['auth.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'user_set'", 'blank': 'True', 'to': "orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'db_table': "'django_content_type'", 'object_name': 'ContentType', 'unique_together': "(('app_label', 'model'),)", 'ordering': "('name',)"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'questions.answerchoice': {
            'Meta': {'object_name': 'AnswerChoice'},
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
        'questions.document': {
            'Meta': {'object_name': 'Document'},
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'date_created': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'recipe': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['questions.DocumentRecipe']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '60'})
        },
        'questions.documentrecipe': {
            'Meta': {'object_name': 'DocumentRecipe'},
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'date_created': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '60'})
        },
        'questions.exercise': {
            'Meta': {'object_name': 'Exercise'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['questions.Question']"}),
            'vardict': ('picklefield.fields.PickledObjectField', [], {})
        },
        'questions.exercisesetrecipe': {
            'Meta': {'object_name': 'ExerciseSetRecipe'},
            'document': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['questions.DocumentRecipe']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'num_columns': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'num_exercises': ('django.db.models.fields.IntegerField', [], {}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['questions.Question']"}),
            'space_after': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        'questions.question': {
            'Meta': {'object_name': 'Question'},
            'comment': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'date_added': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_updated': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            'num_poss': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'question_body': ('django.db.models.fields.CharField', [], {'max_length': '240'}),
            'question_code': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'question_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '240'}),
            'question_prompt': ('django.db.models.fields.CharField', [], {'max_length': '240', 'blank': 'True'}),
            'symbol_vars': ('django.db.models.fields.CharField', [], {'max_length': '240', 'blank': 'True'}),
            'validated': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'vardicts': ('picklefield.fields.PickledObjectField', [], {'default': 'None'})
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