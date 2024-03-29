// See https://kit.svelte.dev/docs/types#app
// for information about these interfaces
declare global {
	namespace App {
		// interface Error {}
		// interface Locals {}
		// interface PageData {}
		// interface Platform {}
	}
	var chats: {
		[key: string]: {
			timeline: [{ 
				role: 'system' | 'ai' | 'user';
				message: string
			}]};
	};
}

export {};
