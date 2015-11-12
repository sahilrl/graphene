

from graphene import Schema
from graphene.contrib.django.types import DjangoInterface, DjangoNode
from graphene.core.fields import IntField, Field
from graphene.core.types.scalars import String, Int
from graphene.relay.fields import GlobalIDField
from graphql.core.type import GraphQLInterfaceType, GraphQLObjectType
from tests.utils import assert_equal_lists

from .models import Article, Reporter


class Character(DjangoInterface):
    '''Character description'''
    class Meta:
        model = Reporter


class Human(DjangoNode):
    '''Human description'''

    pub_date = IntField()

    def get_node(self, id):
        pass

    class Meta:
        model = Article

schema = Schema()


def test_django_interface():
    assert DjangoNode._meta.is_interface is True


def test_pseudo_interface():
    object_type = schema.T(Character)
    assert Character._meta.is_interface is True
    assert isinstance(object_type, GraphQLInterfaceType)
    assert Character._meta.model == Reporter
    assert_equal_lists(
        object_type.get_fields().keys(),
        ['articles', 'firstName', 'lastName', 'email', 'pets', 'id']
    )


def test_djangonode_idfield():
    idfield = DjangoNode._meta.fields_map['id']
    assert isinstance(idfield, GlobalIDField)


def test_node_idfield():
    idfield = Human._meta.fields_map['id']
    assert isinstance(idfield, GlobalIDField)


def test_node_replacedfield():
    idfield = Human._meta.fields_map['pub_date']
    assert isinstance(idfield, Field)
    assert schema.T(idfield).type == schema.T(Int())


def test_interface_resolve_type():
    resolve_type = Character.resolve_type(schema, Human(object()))
    assert isinstance(resolve_type, GraphQLObjectType)


def test_object_type():
    object_type = schema.T(Human)
    Human._meta.fields_map
    assert Human._meta.is_interface is False
    assert isinstance(object_type, GraphQLObjectType)
    assert_equal_lists(
        object_type.get_fields().keys(),
        ['headline', 'id', 'reporter', 'pubDate']
    )
    # assert object_type.get_fields() == {
    #     'headline': fields_map['headline'].internal_field(schema),
    #     'id': fields_map['id'].internal_field(schema),
    #     'reporter': fields_map['reporter'].internal_field(schema),
    #     'pubDate': fields_map['pub_date'].internal_field(schema),
    # }
    assert schema.T(DjangoNode) in object_type.get_interfaces()


def test_node_notinterface():
    assert Human._meta.is_interface is False
    assert DjangoNode in Human._meta.interfaces
