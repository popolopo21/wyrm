import type { PageServerLoad } from './$types';
import * as edgedb from 'edgedb';
import type { GetArticlesReturns } from './getArticles.query';
import { getArticles } from './getArticles.query';
import type { TagCount } from '$lib/types';
import { error, type Actions } from '@sveltejs/kit';

const client = edgedb.createClient();
const domain = '%index%';
const startDate = new Date('2023-09-05');
const endDate = new Date('2023-09-05');

type ChartData = {
	time: Date;
	tags: TagCount;
};
function parseDate(dateStr: string): Date {
	const [datePart, hourPart] = dateStr.split('T');
	const [year, month, day] = datePart.split('-').map(Number);
	const hour = Number(hourPart);

	// JavaScript months are 0-indexed, so subtract 1 from the month
	return new Date(year, month - 1, day, hour);
}

function getd3data(data: GetArticlesReturns, startDate: Date, endDate: Date): ChartData[] {
	let chartData: ChartData[] = [];
	let currentDate = new Date(startDate);

	while (currentDate <= endDate) {
		let tagsCount: TagCount = {};

		for (let hour = 0; hour < 24; hour++) {
			currentDate.setHours(hour);
			let currentHourData = data.find(
				(element) => parseDate(element.key.hour).getTime() === currentDate.getTime()
			);

			if (currentHourData) {
				currentHourData.elements.forEach((el) => {
					el.tags?.forEach((tag) => {
						const clean_tag = tag.toLowerCase().replace(',', '').trim();
						tagsCount[clean_tag] = (tagsCount[clean_tag] || 0) + 1;
					});
				});
			}

			// Push a copy of the aggregated data for the current hour
			chartData.push({ time: new Date(currentDate), tags: { ...tagsCount } });
		}

		// Move to the next day and reset the hour
		currentDate.setDate(currentDate.getDate() + 1);
		currentDate.setHours(0);
	}

	return chartData;
}

export const actions = { 
  default: async ({request}) => {
    const formData =  await request.formData();
    const chatID = formData.get('chatID');
    if (typeof chatID !== 'string' || !chatID) {
      throw error(422, "Wrong||Missing chatID")
    }
    const message = formData.get('message');
    if (typeof message !== 'string' || !message) {
      throw error(422, "Wrong||Missing message")
    }
    if (!(chatID in globalThis.chats)){
      globalThis.chats[chatID] = [{role: 'system', message: 'ANYAD'}];
    }
    globalThis.chats[chatID].push({role: 'user', message});
    const response 
  },
  newChat: async () => {
  }
} satisfies Actions;

// console.debug(dataA);
export const load = (async () => {
	const data = await getArticles(client, {
		domain: domain,
		start_date: startDate,
		end_date: endDate
	});

	const d3Data = getd3data(data, startDate, endDate);
	return { d3Data };
}) satisfies PageServerLoad;
