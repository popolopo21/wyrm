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
    link required website: Website;
    link article:= .<webpage[is Article]
  }


  type Article extending Auditable {
    title: str;
    description: str;
    authors: array<str>;
    section: str;
    tags: array<str>;
    content_text: str;
    a_published_at: datetime;
    a_modified_at: datetime{
      default:= .a_published_at
    }
    required webpage: Webpage{
      constraint exclusive
    };
    link website:= .webpage.website;
    link enhanced_article: .<article[is EnhancedArticle];
  }

  type EnhancedArticle extends Auditable {
    link required article: Article;
    multi link title_embedding: TextEmbedding
    multi link description_embedding: TextEmbedding
    multi link content_embedding: TextEmbedding
    content_keywords: array<str>



  type TextEmbedding {
    # Link back to EnhancedArticle
    link required enhanced_article: EnhancedArticle
    
    # Indicates which part of the text this embedding represents
    required text_part: enum<'title', 'description', 'content'>;
    
    # Order of the embedding for texts that require multiple embeddings
    required order: int;
    
    required text: string;

    # The embedding vector
    required embedding: BertEmbedding;
  }
}