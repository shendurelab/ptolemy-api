from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from app import gene


class GeneSchema(SQLAlchemyAutoSchema):

    class Meta:
        model = gene


gene_schema = GeneSchema()
