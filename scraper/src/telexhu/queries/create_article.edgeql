
insert TelexhuArticle {
    url := <str>$url,
    title := <str>$title,
    author := <str>$author,
    tags := <str>$tags,
    content_html := <str>$content_html,
    content_text := <str>$content_text,
    content_text_embedding := <array<float64>>$content_text_embedding,
    a_published_at := <datetime>$a_published_at,
    a_modified_at := <datetime>$a_modified_at
};
