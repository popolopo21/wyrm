select Article { title, description, url:=.webpage.website.domain ++ .webpage.path}
    filter .title like "%" ++ <str>$title ++ "%"
    limit 10;