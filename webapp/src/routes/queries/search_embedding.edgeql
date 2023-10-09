select Article {title, description, url:=.webpage.website.domain ++ .webpage.path}
order by ext::pgvector::euclidean_distance(
  .description_embedding, <BertEmbedding>$description_embedding)
empty last
limit 10;