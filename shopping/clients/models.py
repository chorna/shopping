# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


from __future__ import unicode_literals

from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.core.mail import send_mail
from django.db import models

# Create your models here.


class MyUserManager(BaseUserManager):
	def _create_user(self, email, password, **extra_fields):
		"""
		Creates and saves a User with the given email and password.
		"""
		if not email:
			raise ValueError('Users must have an email address')
		user = self.model(email=self.normalize_email(email), **extra_fields)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_user(self, email, password=None, **extra_fields):
		"""
		Creates and saves a User with the given email and password.
		"""
		extra_fields.setdefault('is_staff', False)
		extra_fields.setdefault('is_superuser', False)
		return self._create_user(email, password, **extra_fields)

	def create_superuser(self, email, password, **extra_fields):
		"""
		Creates and saves a superuser with the given email and password.
		"""
		extra_fields.setdefault('is_staff', True)
		extra_fields.setdefault('is_superuser', True)
		if extra_fields.get('is_staff') is not True:
			raise ValueError('Superuser must have is_staff=True.')
		if extra_fields.get('is_superuser') is not True:
			raise ValueError('Superuser must have is_superuser=True.')
		return self._create_user(email, password, **extra_fields)


class Client(AbstractBaseUser, PermissionsMixin):
	objects = MyUserManager()
	first_name = models.CharField(max_length=50, null=True, blank=True)
	last_name = models.CharField(max_length=50, null=True, blank=True)
	email = models.EmailField(max_length=100, unique=True)
	phone = models.PositiveIntegerField(null=True, blank=True)
	register_date = models.DateTimeField(auto_now_add=True)
	is_staff = models.BooleanField(default=False)
	is_active = models.BooleanField(default=True)
	extra = models.TextField(null=True)

	USERNAME_FIELD = 'email'

	def __unicode__(self):
		if self.first_name and self.last_name:
			return self.get_full_name()
		return self.email

	def get_full_name(self):
		"""
		Returns the first_name plus the last_name, with a space in between.
		"""
		return "%s %s" % (self.first_name, self.last_name)

	def get_short_name(self):
		"Returns the short name for the user."
		return self.first_name

	def email_user(self, subject, message, from_email=None, **kwargs):
		"""
		Sends an email to this User.
		"""
		send_mail(subject, message, from_email, [self.email], **kwargs)

	class Meta:
		ordering = 'last_name',
		verbose_name = 'Cliente'