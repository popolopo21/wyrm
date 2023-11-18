import type { PageServerLoad } from "./$types";
import * as edgedb from "edgedb";

import { getDomains } from "./getDomains.query"
import { articleDaily } from "./articleDaily.query"
import type {anyad} from "$lib/types"

const client = edgedb.createClient();


export const load = (async () => {
  const articles: anyad[] = []
  const domains = await getDomains(client)
  for (const domain of domains) {
    const res = await articleDaily(client, {domain:domain.domain})
    const res2 = {
      domain: domain.domain,
      articles: res
    }
    articles.push(res2)
  }
  return { articles }
}) satisfies PageServerLoad