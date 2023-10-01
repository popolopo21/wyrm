
insert Article {
    title := <str>$title,
    description := <str>$description,
    authors := <array<str>>$authors,
    section := <str>$section,
    tags := <array<str>>$tags,
    content_text := <str>$content_text,
    title_embedding := <array<float32>>$title_embedding,
    description_embedding := <array<float32>>$description_embedding, 
    a_published_at := <datetime>$a_published_at,
    a_modified_at := <datetime>$a_modified_at,
    webpage := (select Webpage filter .id= <uuid>$webpage_id)
};
