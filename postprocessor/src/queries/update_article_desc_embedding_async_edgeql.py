# AUTOGENERATED FROM 'postprocessor/src/queries/update_article_desc_embedding.edgeql' WITH:
#     $ edgedb-py


from __future__ import annotations
import dataclasses
import edgedb
import typing
import uuid


DescriptionEmbedding = typing.Sequence[float]


class NoPydanticValidation:
    @classmethod
    def __get_validators__(cls):
        from pydantic.dataclasses import dataclass as pydantic_dataclass
        pydantic_dataclass(cls)
        cls.__pydantic_model__.__get_validators__ = lambda: []
        return []


@dataclasses.dataclass
class UpdateArticleDescEmbeddingResult(NoPydanticValidation):
    id: uuid.UUID


async def update_article_desc_embedding(
    executor: edgedb.AsyncIOExecutor,
    *,
    uuid: uuid.UUID,
    description_embedding: DescriptionEmbedding,
) -> UpdateArticleDescEmbeddingResult | None:
    return await executor.query_single(
        """\
        update Article
        filter .id = <uuid>$uuid
        set {
            description_embedding := <BertEmbedding>$description_embedding
        };\
        """,
        uuid=uuid,
        description_embedding=description_embedding,
    )