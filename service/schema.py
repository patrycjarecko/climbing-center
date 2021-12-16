import graphene
from graphene_django import DjangoObjectType
from .models import *

class ClientType(DjangoObjectType):
    class Meta:
        model = Client
        fields = '__all__'

class InstructorType(DjangoObjectType):
    class Meta:
        model = Instructor
        fields = '__all__'

class IntervalType(DjangoObjectType):
    class Meta:
        model = Interval
        fields = '__all__'

class SectionTypeType(DjangoObjectType):
    class Meta:
        model = SectionType
        fields = '__all__'

class SectionType(DjangoObjectType):
    class Meta:
        model = Section
        fields = '__all__'

class PassTypeType(DjangoObjectType):
    class Meta:
        model = PassType
        fields = '__all__'

class PassType(DjangoObjectType):
    class Meta:
        model = Pass
        fields = '__all__'

class EntranceType(DjangoObjectType):
    class Meta:
        model = Entrance
        fields = '__all__'



class Query(graphene.ObjectType):
    clients = graphene.List(ClientType)
    instructors = graphene.List(InstructorType)
    intervals = graphene.List(IntervalType)
    sectionTypes = graphene.List(SectionTypeType)
    sections = graphene.List(SectionType)
    passTypes = graphene.List(PassTypeType)
    passes = graphene.List(PassType)
    entrances = graphene.List(EntranceType)

    def resolve_clients(root, info, **kwargs):
        return Client.objects.all()

    def resolve_instructors(root, info, **kwargs):
        return Instructor.objects.all()

    def resolve_intervals(root, info, **kwargs):
        return Interval.objects.all()

    def resolve_sectionTypes(root, info, **kwargs):
        return SectionType.objects.all()

    def resolve_sections(root, info, **kwargs):
        return Section.objects.all()

    def resolve_passTypes(root, info, **kwargs):
        return PassType.objects.all()

    def resolve_passes(root, info, **kwargs):
        return Pass.objects.all()

    def resolve_entrances(root, info, **kwargs):
        return Entrance.objects.all()


'''
class RoleInput(graphene.InputObjectType):
    name = graphene.String()


class ClientInput(graphene.InputObjectType):
    first_name = graphene.String()
    last_name = graphene.String()
    birthday = graphene.
    email = models.EmailField()


class InstructorInput(graphene.InputObjectType):
    first_name = graphene.String()
    last_name = graphene.String()
    password = graphene.String()
    username = graphene.String()
    role = models.ManyToManyField(Role)

class IntervalInput(graphene.InputObjectType):
    start_time = models.TimeField()
    end_time = models.TimeField()



class SectionTypeInput(graphene.InputObjectType):
    name = graphene.String()
    price = graphene.Int()
    price_once_a_week = graphene.Int()
    max_count = graphene.Int()


class SectionInput(graphene.InputObjectType):
    week_day = graphene.Int()
    interval = models.ForeignKey(Interval, on_delete=models.CASCADE)
    section_type = models.ForeignKey(SectionType, on_delete=models.CASCADE)
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)



class PassTypeInput(graphene.InputObjectType):
    name = graphene.String()
    price = graphene.Int()
    max_entry_count = graphene.Int()
    expiration_date = graphene.Int()



class PassInput(graphene.InputObjectType):
    month = models.DateField()
    section = models.ForeignKey(Section, on_delete=models.CASCADE, blank=True, null=True)
    pass_type = models.ForeignKey(PassType, on_delete=models.CASCADE, blank=True, null=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)


class EntranceInput(graphene.InputObjectType):
    date = models.DateField()
    pass_model = models.ForeignKey(Pass, on_delete=models.CASCADE)'''





schema = graphene.Schema(query=Query)