CREATE MIGRATION m1gascfy4xfhm2vbuphjd4swr2b3swcfi2qxs2mmxa4f4tyfzuyqcq
    ONTO initial
{
  CREATE EXTENSION pgvector VERSION '0.4';
  CREATE ABSTRACT TYPE default::Auditable {
      CREATE REQUIRED PROPERTY created_at: std::datetime {
          SET default := (std::datetime_current());
          SET readonly := true;
      };
      CREATE PROPERTY modified_at: std::datetime {
          SET default := (std::datetime_current());
          SET readonly := true;
      };
  };
  CREATE SCALAR TYPE default::TextEmbedding EXTENDING ext::pgvector::vector<1536>;
  CREATE TYPE default::Article EXTENDING default::Auditable {
      CREATE PROPERTY a_modified_at: std::datetime;
      CREATE PROPERTY a_published_at: std::datetime;
      CREATE PROPERTY author: std::str;
      CREATE PROPERTY content_html: std::str;
      CREATE PROPERTY content_text: std::str;
      CREATE PROPERTY content_text_embedding: default::TextEmbedding;
      CREATE PROPERTY title: std::str;
      CREATE PROPERTY url: std::str;
  };
};
