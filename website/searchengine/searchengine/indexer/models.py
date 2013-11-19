from django.db import models

# Create your models here.

class Inv_Index(models.Model):

	word = models.CharField(max_length=200)
	doc_name = models.CharField(max_length=200)
	word_pos = models.IntegerField()
	
	
	def __unicode__(self):
		return self.word


class term_Frequency(models.Model):
	word = models.CharField(max_length=200)
	doc_name = models.CharField(max_length=200)
	word_freq = models.IntegerField(default=0)
	term_freq = models.FloatField(default = 0)
	tf_idf = models.FloatField(default=0)
	
	
	def __unicode__(self):
		return self.word
		
	

class IDF(models.Model):
	word = models.CharField(max_length=200)
	idf = models.FloatField()
	
	def __unicode__(self):
		return self.word	

class Stop_Word(models.Model):
	word = models.CharField(max_length=200)
	
	def __unicode__(self):
		return self.word		

		
