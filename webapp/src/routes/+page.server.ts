import type { PageServerLoad } from "./$types";
import { search_embedding } from "./queries/search_embedding.query";
/* import {generateEmbedding} from "$lib/generateEmbedding"*/
import {client} from '$lib/server/edgedb'
import { HfInference } from "@huggingface/inference"

const hf = new HfInference(process.env.HF_TOKEN)

export const load = (async({url}) => {
    const searchTerm = url.searchParams.get("searchTerm");
    if (!searchTerm) {
        return { results: [] };
    }
    const searchTermEmbed = await hf.featureExtraction({
        model: 'intfloat/multilingual-e5-large',
        inputs: searchTerm??""
    });
    console.debug(searchTermEmbed)
    const results = await search_embedding(client, {description_embedding: searchTermEmbed});
    return {results};
}) satisfies PageServerLoad;
