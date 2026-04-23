# backend/core/services/base_service.py
from django.db import transaction

class BaseService:
    model = None

    @classmethod
    def get_all(cls):
        return cls.model.objects.all()

    @classmethod
    def get_by_id(cls, id):
        return cls.model.objects.filter(id=id).first()

    @classmethod
    @transaction.atomic
    def create(cls, **data):
        return cls.model.objects.create(**data)

    @classmethod
    @transaction.atomic
    def update(cls, id, **data):
        instance = cls.get_by_id(id)
        if instance:
            for attr, value in data.items():
                setattr(instance, attr, value)
            instance.save()
        return instance