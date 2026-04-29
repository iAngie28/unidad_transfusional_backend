class BaseService:
    model = None

    @classmethod
    def get_all(cls):
        return cls.model.objects.all()

    @classmethod
    def get_by_id(cls, id):
        return cls.model.objects.filter(id=id).first()