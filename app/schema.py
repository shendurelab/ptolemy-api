from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from app import gene_filtered


class GeneSchema(SQLAlchemyAutoSchema):

    class Meta:
        model = gene_filtered


gene_schema = GeneSchema()
