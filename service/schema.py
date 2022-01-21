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

class SectionModelType(DjangoObjectType):
    class Meta:
        model = Section
        fields = '__all__'

class PassTypeType(DjangoObjectType):
    class Meta:
        model = PassType
        fields = '__all__'

class PassModelType(DjangoObjectType):
    class Meta:
        model = Pass
        fields = '__all__'

class EntranceType(DjangoObjectType):
    class Meta:
        model = Entrance
        fields = '__all__'



class Query(graphene.ObjectType):
    clients = graphene.List(ClientType)
    users = graphene.List(InstructorType)
    instructors = graphene.List(InstructorType)
    intervals = graphene.List(IntervalType)
    sectionTypes = graphene.List(SectionTypeType)
    sections = graphene.List(SectionModelType)
    passTypes = graphene.List(PassTypeType)
    passes = graphene.List(PassModelType)
    entrances = graphene.List(EntranceType)
    roles = graphene.List(RoleType)

    user = graphene.Field(InstructorType, token=graphene.String(required=True))
    client = graphene.Field(ClientType, id=graphene.String(required=True))

    def resolve_clients(root, info, **kwargs):
        return Client.objects.all()

    def resolve_users(root, info, **kwargs):
        return Instructor.objects.all()

    def resolve_instructors(root, info, **kwargs):
        return Instructor.objects.filter(role=2)

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

    def resolve_roles(root, info, **kwargs):
        return Role.objects.all()

    def resolve_user(root, info, token=None):
        return Instructor.objects.filter(auth_token=token).first() if token is not None else None

    def resolve_client(root, info, id=None):
        return Client.objects.filter(card_number=id).first() if id is not None else None




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
    role_id = graphene.List(graphene.Int)

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
    interval_id = graphene.Int()
    section_type_id = graphene.Int()
    instructor_id = graphene.Int()

class PassTypeInput(graphene.InputObjectType):
    name = graphene.String()
    price = graphene.Int()
    max_entry_count = graphene.Int()
    expiration_date = graphene.Int()

class PassInput(graphene.InputObjectType):
    month = graphene.Date()
    section_id = graphene.Int()
    pass_type_id = graphene.Int()
    client_id = graphene.String()

class EntranceInput(graphene.InputObjectType):
    date = graphene.Date()
    pass_model_id = graphene.Int()

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
        client.birthday = input.birthday
        client.email = input.email
        client.save()
        return CreateClient(client=client)

class UpdateClient(graphene.Mutation):
    class Arguments:
        input = ClientInput(required=True)
        id = graphene.String()

    client = graphene.Field(ClientType)

    @classmethod
    def mutate(cls, root, info, input, id):
        client = Client.objects.get(pk=id)
        client.first_name = input.first_name if input.first_name is not None else client.first_name
        client.last_name = input.last_name if input.last_name is not None else client.last_name
        client.email = input.email if input.email is not None else client.email
        client.birthday = input.birthday if input.birthday is not None else client.birthday
        client.save()
        return UpdateClient(client=client)

class DeleteClient(graphene.Mutation):
    class Arguments:
        id = graphene.String()

    client = graphene.Field(ClientType)

    @classmethod
    def mutate(cls, root, info, id):
        client = Client.objects.get(pk=id)
        client.delete()
        return None


class CreateInstructor(graphene.Mutation):
    class Arguments:
        input = InstructorInput(required=True)

    instructor = graphene.Field(InstructorType)

    @classmethod
    def mutate(cls, root, info, input):
        instructor = Instructor()
        instructor.first_name = input.first_name
        instructor.last_name = input.last_name
        instructor.password = input.password
        instructor.username = input.username

        roles = [Role.objects.get(pk=index) for index in input.role_id]
        instructor.save()
        instructor.role.set(roles)
        return CreateInstructor(instructor=instructor)

class UpdateInstructor(graphene.Mutation):
    class Arguments:
        input = InstructorInput(required=True)
        id = graphene.ID()

    instructor = graphene.Field(InstructorType)

    @classmethod
    def mutate(cls, root, info, input, id):
        instructor = Instructor.objects.get(pk=id)
        instructor.first_name = input.first_name if input.first_name is not None else instructor.first_name
        instructor.last_name = input.last_name if input.last_name is not None else instructor.last_name
        instructor.password = input.password if input.password is not None else instructor.password
        instructor.username = input.username if input.username is not None else instructor.username

        if input.role_id:
            roles = [Role.objects.get(pk=index) for index in input.role_id]
            instructor.role.set(roles)

        instructor.save()
        return UpdateInstructor(instructor=instructor)

class DeleteInstructor(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    instructor = graphene.Field(InstructorType)

    @classmethod
    def mutate(cls, root, info, id):
        instructor = Instructor.objects.get(pk=id)
        instructor.delete()
        return None



class CreateRole(graphene.Mutation):
    class Arguments:
        input = RoleInput(required=True)

    role = graphene.Field(RoleType)

    @classmethod
    def mutate(cls, root, info, input):
        role = Role.objects.create(**input)
        return CreateRole(role=role)

class UpdateRole(graphene.Mutation):
    class Arguments:
        input = RoleInput(required=True)
        id = graphene.ID()

    role = graphene.Field(RoleType)

    @classmethod
    def mutate(cls, root, info, input, id):
        role = Role.objects.get(pk=id)
        role.name = input.name if input.name is not None else role.name
        role.save()
        return UpdateRole(role=role)

class DeleteRole(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    role = graphene.Field(RoleType)

    @classmethod
    def mutate(cls, root, info, id):
        role = Role.objects.get(pk=id)
        role.delete()
        return None

#instructor jak z managerem
#jak z relacjami


class CreateInterval(graphene.Mutation):
    class Arguments:
        input = IntervalInput(required=True)

    interval = graphene.Field(IntervalType)

    @classmethod
    def mutate(cls, root, info, input):
        interval = Interval.objects.create(**input)
        return CreateInterval(interval=interval)

class UpdateInterval(graphene.Mutation):
    class Arguments:
        input = IntervalInput(required=True)
        id = graphene.ID()

    interval = graphene.Field(IntervalType)

    @classmethod
    def mutate(cls, root, info, input, id):
        interval = Interval.objects.get(pk=id)
        interval.start_time = input.start_time if input.start_time is not None else interval.start_time
        interval.end_time = input.end_time if input.end_time is not None else interval.end_time
        interval.save()
        return UpdateInterval(interval=interval)

class DeleteInterval(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    interval = graphene.Field(IntervalType)

    @classmethod
    def mutate(cls, root, info, id):
        interval = Interval.objects.get(pk=id)
        interval.delete()
        return None


#nie dziala
class CreateSectionType(graphene.Mutation):
    class Arguments:
        input = SectionTypeInput(required=True)

    sectionType = graphene.Field(SectionTypeType)

    @classmethod
    def mutate(cls, root, info, input):
        section_type = SectionType.objects.create(**input)
        return CreateSectionType(sectionType=section_type)

class UpdateSectionType(graphene.Mutation):
    class Arguments:
        input = SectionTypeInput(required=True)
        id = graphene.ID()

    sectionType = graphene.Field(SectionTypeType)

    @classmethod
    def mutate(cls, root, info, input, id):
        sectionType = SectionType.objects.get(pk=id)
        sectionType.name = input.name if input.name is not None else sectionType.name
        sectionType.price = input.price if input.price is not None else sectionType.price
        sectionType.price_once_a_week = input.price_once_a_week if input.price_once_a_week is not None else sectionType.price_once_a_week
        sectionType.max_count = input.max_count if input.max_count is not None else sectionType.max_count
        sectionType.save()
        return UpdateSectionType(sectionType=sectionType)

class DeleteSectionType(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    sectionType = graphene.Field(SectionTypeType)

    @classmethod
    def mutate(cls, root, info, id):
        sectionType = SectionType.objects.get(pk=id)
        sectionType.delete()
        return None



class CreateSection(graphene.Mutation):
    class Arguments:
        input = SectionInput(required=True)

    section = graphene.Field(SectionModelType)

    @classmethod
    def mutate(cls, root, info, input):
        section = Section()
        section.week_day = input.week_day
        section.interval = Interval.objects.get(pk=input.interval_id)
        section.section_type = SectionType.objects.get(pk=input.section_type_id)
        section.instructor = Instructor.objects.get(pk=input.instructor_id)
        section.save()
        return CreateSection(section=section)

class UpdateSection(graphene.Mutation):
    class Arguments:
        input = SectionInput(required=True)
        id = graphene.ID()

    section = graphene.Field(SectionModelType)

    @classmethod
    def mutate(cls, root, info, input, id):
        section = Section.objects.get(pk=id)
        if input.interval_id is not None:
            section.interval = Interval.objects.get(pk=input.interval_id)

        if input.section_type_id is not None:
            section.section_type = SectionType.objects.get(pk=input.section_type_id)

        if input.instructor_id is not None:
            section.instructor = Instructor.objects.get(pk=input.instructor_id)

        section.week_day = input.week_day if input.week_day is not None else section.week_day
        section.save()
        return UpdateSection(section=section)

class DeleteSection(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    section = graphene.Field(SectionModelType)

    @classmethod
    def mutate(cls, root, info, id):
        section = Section.objects.get(pk=id)
        section.delete()
        return None



class CreatePassType(graphene.Mutation):
    class Arguments:
        input = PassTypeInput(required=True)

    passType = graphene.Field(PassTypeType)

    @classmethod
    def mutate(cls, root, info, input):
        passType = PassType.objects.create(**input)
        return CreatePassType(passType=passType)

class UpdatePassType(graphene.Mutation):
    class Arguments:
        input = PassTypeInput(required=True)
        id = graphene.ID()

    passType = graphene.Field(PassTypeType)

    @classmethod
    def mutate(cls, root, info, input, id):
        passType = PassType.objects.get(pk=id)
        passType.name = input.name if input.name is not None else passType.name
        passType.price = input.price if input.price is not None else passType.price
        passType.max_entry_count = input.max_entry_count if input.max_entry_count is not None else passType.max_entry_count
        passType.expiration_date = input.expiration_date if input.expiration_date is not None else passType.expiration_date
        passType.save()
        return UpdatePassType(passType=passType)

class DeletePassType(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    passType = graphene.Field(PassTypeType)

    @classmethod
    def mutate(cls, root, info, id):
        passType = PassType.objects.get(pk=id)
        passType.delete()
        return None



class CreatePass(graphene.Mutation):
    class Arguments:
        input = PassInput(required=True)

    pass_model = graphene.Field(PassModelType)

    @classmethod
    def mutate(cls, root, info, input):
        pass_model = Pass()
        pass_model.month = input.month
        pass_model.pass_type = PassType.objects.get(pk=input.pass_type_id)
        pass_model.section = Section.objects.get(pk=input.section_id)
        pass_model.client = Client.objects.get(pk=input.client_id)
        pass_model.save()
        return CreatePass(pass_model=pass_model)

class UpdatePass(graphene.Mutation):
    class Arguments:
        input = PassInput(required=True)
        id = graphene.ID()

    pass_model = graphene.Field(PassModelType)

    @classmethod
    def mutate(cls, root, info, input, id):
        pass_model = Pass.objects.get(pk=id)
        if input.pass_type_id is not None:
            pass_model.pass_type = PassType.objects.get(pk=input.pass_type_id)

        if input.section_id is not None:
            pass_model.section = Section.objects.get(pk=input.section_id)

        if input.client_id is not None:
            pass_model.client = Client.objects.get(pk=input.client_id)

        pass_model.month = input.month if input.month is not None else pass_model.month
        pass_model.save()
        return UpdatePass(pass_model=pass_model)

class DeletePass(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    pass_model = graphene.Field(PassModelType)

    @classmethod
    def mutate(cls, root, info, id):
        pass_model = Pass.objects.get(pk=id)
        pass_model.delete()
        return None



class CreateEntrance(graphene.Mutation):
    class Arguments:
        input = EntranceInput(required=True)

    entrance = graphene.Field(EntranceType)

    @classmethod
    def mutate(cls, root, info, input):
        entrance = Entrance()
        entrance.date = input.date
        entrance.pass_model = Pass.objects.get(pk=input.pass_model_id)
        entrance.save()
        return CreateEntrance(entrance=entrance)

class UpdateEntrance(graphene.Mutation):
    class Arguments:
        input = EntranceInput(required=True)
        id = graphene.ID()

    entrance = graphene.Field(EntranceType)

    @classmethod
    def mutate(cls, root, info, input, id):
        entrance = Entrance.objects.get(pk=id)

        if input.pass_model_id is not None:
            entrance.pass_model = Pass.objects.get(pk=input.pass_model_id)

        entrance.date = input.date if input.date is not None else entrance.date
        entrance.save()
        return UpdateEntrance(entrance=entrance)

class DeleteEntrance(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    entrance = graphene.Field(EntranceType)

    @classmethod
    def mutate(cls, root, info, id):
        entrance = Entrance.objects.get(pk=id)
        entrance.delete()
        return None



class Mutation(graphene.ObjectType):
    create_client = CreateClient.Field()
    update_client = UpdateClient.Field()
    delete_client = DeleteClient.Field()

    create_instructor = CreateInstructor.Field()
    update_instructor = UpdateInstructor.Field()
    delete_instructor = DeleteInstructor.Field()

    create_role = CreateRole.Field()
    update_role = UpdateRole.Field()
    delete_role = DeleteRole.Field()

    create_interval = CreateInterval.Field()
    update_interval = UpdateInterval.Field()
    delete_interval = DeleteInterval.Field()

    create_sectionType = CreateSectionType.Field()
    update_sectionType = UpdateSectionType.Field()
    delete_sectionType = DeleteSectionType.Field()

    create_section = CreateSection.Field()
    update_section = UpdateSection.Field()
    delete_section = DeleteSection.Field()

    create_passType = CreatePassType.Field()
    update_passType = UpdatePassType.Field()
    delete_passType = DeletePassType.Field()

    create_pass = CreatePass.Field()
    update_pass = UpdatePass.Field()
    delete_pass = DeletePass.Field()

    create_entrance = CreateEntrance.Field()
    update_entrance = UpdateEntrance.Field()
    delete_entrance = DeleteEntrance.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)