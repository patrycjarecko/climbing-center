import graphene
from graphene_django import DjangoObjectType
from django.utils.crypto import get_random_string
from .models import *


class RoleType(DjangoObjectType):
    class Meta:
        model = Role
        fields = '__all__'

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



class RoleInput(graphene.InputObjectType):
    name = graphene.String()


class ClientInput(graphene.InputObjectType):
    first_name = graphene.String()
    last_name = graphene.String()
    birthday = graphene.Date()
    email = graphene.String()


class InstructorInput(graphene.InputObjectType):
    first_name = graphene.String()
    last_name = graphene.String()
    password = graphene.String()
    username = graphene.String()
    role = graphene.Field(RoleType)

class IntervalInput(graphene.InputObjectType):
    start_time = graphene.Time()
    end_time = graphene.Time()

class SectionTypeInput(graphene.InputObjectType):
    name = graphene.String()
    price = graphene.Int()
    price_once_a_week = graphene.Int()
    max_count = graphene.Int()


class SectionInput(graphene.InputObjectType):
    week_day = graphene.Int()
    interval = graphene.Field(IntervalType)
    section_type = graphene.Field(SectionTypeType)
    instructor = graphene.Field(InstructorType)

class PassTypeInput(graphene.InputObjectType):
    name = graphene.String()
    price = graphene.Int()
    max_entry_count = graphene.Int()
    expiration_date = graphene.Int()

class PassInput(graphene.InputObjectType):
    month = graphene.Date()
    section = graphene.Field(SectionType)
    pass_type = graphene.Field(PassTypeType)
    client = graphene.Field(ClientType)


class EntranceInput(graphene.InputObjectType):
    date = graphene.Date()
    pass_model = graphene.Field(PassType)

def generate_card_number():
    number = get_random_string(length=6, allowed_chars='1234567890')
    if Client.objects.filter(card_number=number).count() >0:
        generate_card_number()
    else:
        return number

class CreateClient(graphene.Mutation):
    class Arguments:
        input = ClientInput(required=True)

    client = graphene.Field(ClientType)

    @classmethod
    def mutate(cls, root, info, input):
        client = Client()
        client.card_number = generate_card_number()
        client.first_name = input.first_name
        client.last_name = input.last_name
        client.email = input.email
        client.birthday = input.birthday
        client.save()
        return CreateClient(client=client)


class Mutation(graphene.ObjectType):
    create_client = CreateClient.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)