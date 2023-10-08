import type { PageServerLoad } from "./$types";
import { search_embedding } from "./queries/search_embedding.query";
/* import {generateEmbedding} from "$lib/generateEmbedding"*/
import {client} from '$lib/server/edgedb'

export const load = (async({url}) => {
    const searchTerm = url.searchParams.get("searchTerm");

    const results = await search_embedding(client, {title: searchTerm ?? ""});
    return {results};
}) satisfies PageServerLoad;
