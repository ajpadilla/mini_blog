from marshmallow import fields

from app import ma


class ProductSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    description = fields.String()
    price = fields.Float()


class PostProductSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    title = fields.String()
    title_slug = fields.String()
    content = fields.String()
    product_id = fields.Integer()
    product_parent = fields.Nested('ProductSchema')


class CommentProductSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    content = fields.String()
    post_id = fields.Integer()
    post_parent = fields.Nested('PostProductSchema')