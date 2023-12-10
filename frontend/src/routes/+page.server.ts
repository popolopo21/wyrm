import { redirect } from '@sveltejs/kit';
import { BACKEND_URL } from '$env/static/private';
export const actions = {
    default:async ({event, request}) => {
        const data = await request.formData();
        // const userID = data.get('userID');
        const text = data.get('text');
        const startDate = data.get('startDate');
        const endDate = data.get('endDate');

        //TODO: make a fetch request to do server
        await new Promise((fulfil) => setTimeout(fulfil, 1000));
        const response = await fetch(BACKEND_URL);
        const res = await response.json();
        const url = `/search/${res.uuid}`;
        throw redirect(302, url);
    }
}