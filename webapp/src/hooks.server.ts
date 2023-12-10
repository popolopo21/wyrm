import type { Handle } from "@sveltejs/kit";

export const handle = (async ({event, resolve}) =>  {
    if (!("chats" in globalThis))
    {
        globalThis.chats = {};
    }
    return resolve(event);
}) satisfies Handle