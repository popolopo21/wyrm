insert Webpage{
    path:= <str>$path,
    html:= <str>$html,
    lastmod:= <datetime>$lastmod,
    website:= (select Website filter .domain=<str>$domain)
}