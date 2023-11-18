// GENERATED by @edgedb/generate v0.4.1

import type {Executor} from "edgedb";

export type GetArticlesArgs = {
  "domain": string;
  "start_date": Date;
  "end_date": Date;
};

export type GetArticlesReturns = {
  "key": {
    "hour": string;
  };
  "grouping": string[];
  "elements": {
    "tags": string[] | null;
  }[];
}[];

export async function getArticles(client: Executor, args: GetArticlesArgs): Promise<GetArticlesReturns> {
  return client.query(`\
with M:= (select Article {*}
    filter 
        .website.domain like <str>$domain and
        datetime_truncate(.a_published_at, "days") >= <datetime>$start_date and
        datetime_truncate(.a_published_at, "days") <= <datetime>$end_date)
group M {tags}
using hour := to_str(.a_published_at)[0:13]
by hour;`, args);

}
