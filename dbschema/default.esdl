using extension pgvector;


module default {
scalar type TextEmbedding extending
    ext::pgvector::vector<1536>;

  abstract type Auditable {
    required  created_at: datetime {
      readonly:= true;
      default:= datetime_of_statement();
    }
    required  modified_at: datetime {
      default:= datetime_of_statement();
      rewrite insert, update using (datetime_of_statement())
    }
  }

  type Website extending Auditable {
    required domain: str {
      constraint exclusive
    }
    multi link articles:= .<website[is Article];
    property sitemap:= (
      json_object_pack((
        for article in (select .articles {url, sitemap_date})
        union (article.url, <json>article.sitemap_date)
      ))
    )
  }

  type Article extending Auditable {
    required url: str;
    title: str;
    author: str;
    tags: array<str>;
    content_html: str;
    content_text: str;
    content_text_embedding: TextEmbedding;
    required sitemap_date: datetime;
    a_published_at: datetime;
    a_modified_at: datetime;
    required website: Website;
  }
}