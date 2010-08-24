# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Changing field 'NoteType.template'
        db.alter_column('notes_notetype', 'template', self.gf('django.db.models.fields.CharField')(max_length=200, null=True))

        # Changing field 'NoteType.print_method'
        db.alter_column('notes_notetype', 'print_method', self.gf('django.db.models.fields.CharField')(max_length=20, null=True))


    def backwards(self, orm):
        
        # Changing field 'NoteType.template'
        db.alter_column('notes_notetype', 'template', self.gf('django.db.models.fields.CharField')(max_length=200))

        # Changing field 'NoteType.print_method'
        db.alter_column('notes_notetype', 'print_method', self.gf('django.db.models.fields.CharField')(max_length=20))


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'unique': 'True'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
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
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '30', 'unique': 'True'})
        },
        'contacts.company': {
            'Meta': {'object_name': 'Company'},
            'activity': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dsbe.Activity']", 'null': 'True', 'blank': 'True'}),
            'addr1': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'city': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['countries.City']", 'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['countries.Country']", 'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'gsm': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'language': ('django.db.models.fields.related.ForeignKey', [], {'default': "'de'", 'to': "orm['countries.Language']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'prefix': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'region': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'remarks': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'street': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'street_box': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'street_no': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contacts.CompanyType']", 'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'vat_id': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'zip_code': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'})
        },
        'contacts.companytype': {
            'Meta': {'object_name': 'CompanyType'},
            'abbr': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'contacts.person': {
            'Meta': {'object_name': 'Person'},
            'accepts_shift': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'accepts_we': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'activity': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dsbe.Activity']", 'null': 'True', 'blank': 'True'}),
            'addr1': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'birth_country': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'by_birth_place'", 'blank': 'True', 'null': 'True', 'to': "orm['countries.Country']"}),
            'birth_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'birth_date_circa': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'birth_place': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'can_bus': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'can_clark': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'can_truck': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'card_number': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['countries.City']", 'null': 'True', 'blank': 'True'}),
            'civil_state': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['countries.Country']", 'null': 'True', 'blank': 'True'}),
            'driving_license': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dsbe.DrivingLicense']", 'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'gsm': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'has_own_car': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_cpas': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_minor': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_senior': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'it_knowledge': ('lino.modlib.fields.PercentageField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'language': ('django.db.models.fields.related.ForeignKey', [], {'default': "'de'", 'to': "orm['countries.Language']"}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'national_id': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'nationality': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'by_nationality'", 'blank': 'True', 'null': 'True', 'to': "orm['countries.Country']"}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'region': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'remarks': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'sex': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'street': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'street_box': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'street_no': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'zip_code': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'countries.city': {
            'Meta': {'object_name': 'City'},
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['countries.Country']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'zip_code': ('django.db.models.fields.CharField', [], {'max_length': '8', 'blank': 'True'})
        },
        'countries.country': {
            'Meta': {'object_name': 'Country'},
            'isocode': ('django.db.models.fields.CharField', [], {'max_length': '4', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'short_code': ('django.db.models.fields.CharField', [], {'max_length': '4', 'blank': 'True'})
        },
        'countries.language': {
            'Meta': {'object_name': 'Language'},
            'id': ('django.db.models.fields.CharField', [], {'max_length': '2', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'dsbe.activity': {
            'Meta': {'object_name': 'Activity'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lst104': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'dsbe.drivinglicense': {
            'Meta': {'object_name': 'DrivingLicense'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'notes.note': {
            'Meta': {'object_name': 'Note'},
            'body': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contacts.Company']", 'null': 'True', 'blank': 'True'}),
            'date': ('lino.modlib.fields.MyDateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.related.ForeignKey', [], {'default': "'de'", 'to': "orm['countries.Language']"}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contacts.Person']", 'null': 'True', 'blank': 'True'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['notes.NoteType']", 'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'})
        },
        'notes.notetype': {
            'Meta': {'object_name': 'NoteType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'print_method': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'template': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['notes']
