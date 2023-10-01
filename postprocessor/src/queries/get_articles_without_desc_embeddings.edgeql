select Article {*} filter {
    .description_embedding = <BertEmbedding>array_fill(0,1024) AND
    .website.domain = <str>$domain
};
