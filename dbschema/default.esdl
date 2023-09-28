using extension pgvector;


module default {
scalar type TextEmbedding extending
    ext::pgvector::vector<1536>;

  abstract type Auditable {
    required property created_at -> datetime {
      readonly := true;
      default := datetime_current();
    }
    property modified_at -> datetime {
      readonly := true;
      default := datetime_current();
    }
  }

  type Article extending Auditable {
    property url -> str;
    property title -> str;
    property author -> str;
    property tags -> array<str>;
    property content_html -> str;
    property content_text -> str;
    property content_text_embedding -> TextEmbedding;
    property a_published_at -> datetime;
    property a_modified_at -> datetime;
  }
}