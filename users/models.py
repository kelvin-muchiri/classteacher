"""
User related models
"""

import datetime
import uuid
import jwt

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.utils import timezone

from common.utilities import (
	GENDER_CHOICES,
	validate_phone_number,
)



class CustomUserManager(BaseUserManager):
	"""
	Django requires that custom users define their own Manager class.
	By inheriting from `BaseUserManager`, we get a lot of the same code used by
	Django to create a `User`.

	All we have to do is override the `create_user` function which we will use
	to create `User` objects.
	"""

	def _create_user(self, username, first_name, phone_number, email, password, **extra_fields):
		if not (phone_number or email):
			raise ValueError('Provide an email or phone number for this user')

		if not username:
			raise ValueError('Provide a first username for this user')

		if not first_name:
			raise ValueError('Provide a first name for this user')

		if phone_number:
			validate_phone_number(phone_number)

		user = self.model(
			username=username,
			first_name=first_name,
			phone_number = phone_number, 
			email= self.normalize_email(email), 
			**extra_fields
			)
		user.set_password(password)
		user.save(using=self._db)

		return user

	def create_user(self, username, first_name, phone_number=None, 
		email=None, password=None, **extra_fields):
		"""
		Creates and saves a User with the given 
		(phone number or email) and password.
		"""
		return self._create_user(username, first_name, phone_number, 
			email, password, **extra_fields)

	def create_staff(self, username, first_name, password, phone_number=None, 
		email=None, **extra_fields):
		"""
		Create a user and return a `User` with staff permissions
		"""
		if password is None:
			raise TypeError('Staff must have a password.')

		extra_fields.setdefault('is_staff', True)

		return self._create_user(username, first_name, phone_number, email, 
			password, **extra_fields)

	def create_superuser(self, username, first_name, password, phone_number=None, 
		email=None, **extra_fields):
		"""
		Create a user and return a `User` with superuser permissions
		"""
		if password is None:
			raise TypeError('Superusers must have a password.')

		extra_fields.setdefault('is_superuser', True)
		extra_fields.setdefault('is_staff', True)

		return self._create_user(username, first_name, phone_number, email, 
			password, **extra_fields)


class User(AbstractBaseUser):
	"""A custom user manager."""

	REQUIRED_FIELDS = ['username', 'first_name']
	USERNAME_FIELD = 'phone_number'

	id = models.UUIDField(
		primary_key=True, default=uuid.uuid4, editable=False)
	first_name = models.CharField(max_length=255)
	last_name = models.CharField(
		max_length=255,
		null=True,
		blank=True
	)
	other_names = models.CharField(
		max_length=255,
		null=True,
	    blank=True
	)
	username = models.CharField(
	 	max_length=10, 
	 	unique=True
	)
	email = models.EmailField(
		unique=True, 
		blank=True, 
		null=True, 
		default=None
	)
	phone_number = models.CharField(
		unique=True, 
		max_length=25, 
		null=True, 
		blank=True, 
		default=None
	)
	gender = models.CharField(
		max_length=1, 
		choices=GENDER_CHOICES, 
		null=True,
		blank=True, 
		
	)
	date_of_birth = models.DateField(null=True, blank=True)
	is_staff = models.BooleanField(default=False)
	is_superuser = models.BooleanField(default=False)
	is_active = models.BooleanField(default=True)
	is_deleted = models.BooleanField(default=False)
	date_joined = models.DateTimeField(default=timezone.now)

	objects = CustomUserManager()

	def __str__(self):
		return "{}".format(self.full_name)

	@property
	def full_name(self):
		return " ".join([
			self.first_name, self.last_name or "", self.other_names or ""
		]).strip()

	@property
	def token(self):
		"""
		Allows us to get a user's token by calling `user.token` instead of
		`user.generate_jwt_token().

		The `@property` decorator above makes this possible. `token` is called
		a "dynamic property".
		"""
		return self._generate_jwt_token()

	def _generate_jwt_token(self):
		"""
		Generates a JSON Web Token that stores this user's ID and has an expiry
		date set to 5 minutes into the future.
		"""
		dt = datetime.datetime.now() + datetime.timedelta(days=30)

		token = jwt.encode({
			'id': self.pk.__str__(),
			'exp': int(dt.strftime('%s'))
		}, settings.SECRET_KEY, algorithm='HS256')

		return token.decode('utf-8')

	def save(self, *args, **kwargs):
		self.full_clean(exclude=None)

		if not self.phone_number:
			self.phone_number = None

		if not self.email:
			self.email = None

		super(User, self).save(*args, **kwargs)

	class Meta:
		ordering = ('-date_joined', 'first_name')