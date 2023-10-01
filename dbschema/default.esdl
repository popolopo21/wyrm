using extension pgvector;


module default {
scalar type BertEmbedding extending
    ext::pgvector::vector<1024>;

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
    multi link webpages:= .<website[is Webpage];
    property sitemap:= (
      json_object_pack((
          for webpage in (select .webpages {path, lastmod})
          union (.domain++webpage.path, <json>webpage.lastmod)
      )) ++ to_json("{}")
    )
  }

  type Webpage extending Auditable {
    required path: str;
    required html: str;
    required lastmod: datetime;
    required website: Website;
    link article:= .<webpage[is Article]
  }


  type Article extending Auditable {
    title: str;
    description: str;
    authors: array<str>;
    section: str;
    tags: array<str>;
    content_text: str;
    title_embedding: BertEmbedding;
    description_embedding: BertEmbedding;
    a_published_at: datetime;
    a_modified_at: datetime{
      default:= .a_published_at
    }
    required webpage: Webpage{
      constraint exclusive
    };
    link website:= .webpage.website;
  }
}