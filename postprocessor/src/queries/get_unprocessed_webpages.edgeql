select Webpage {*} filter {
    not exists .article AND
    .website.domain =<str>$domain
};