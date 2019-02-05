/*
# Jasmin tests for the base functions.
#
# devs@droxit.de
#
# Copyright (c) 2019 droxIT GmbH
#
*/

describe('search_and_sort', function() {

	// Search for keywords in list of strings.
	it('keyword_search', function() {
		input = ['Houston, wir haben ein Problem',
			'Ich bin zu alt für so eine Scheiße',
			'Ich liebe den Geruch von Napalm am Morgen',
			'Mein Name ist Bond. James Bond',
			'Ich mache ihm ein Angebot, das er nicht ablehnen kann'
		];

		// Search for "Bond".
		pattern = 'Bond';
		output = ['Mein Name ist Bond. James Bond']
		expect(keyword_search(input, pattern)).toEqual(output);
		expect(keyword_search(input, 'bond')).toEqual([]);

		// Search for "Ich".
		pattern = 'Ich';
		output = ['Ich bin zu alt für so eine Scheiße',
			'Ich liebe den Geruch von Napalm am Morgen',
			'Ich mache ihm ein Angebot, das er nicht ablehnen kann'
		];
		expect(keyword_search(input, pattern)).toEqual(output);
		pattern = 'ich';
		output = ['Ich mache ihm ein Angebot, das er nicht ablehnen kann'];
		expect(keyword_search(input, pattern)).toEqual(output);

		// Test empty arrays and null values.
		expect(keyword_search([], pattern)).toEqual([]);
		expect(keyword_search(null, pattern)).toEqual([]);
		expect(keyword_search(input, "")).toEqual([]);
		expect(keyword_search(input, null)).toEqual([]);
	});

	// Search for keywords in custom data structure.
	it('custom_keyword_search', function() {
		// Sample input.
		input = [
			['delay_service', 'etwas Info'],
			['generator_service', 'nur zum Generieren'],
		];

		// Sample search functions.
		function search_first(elem, pattern) {
			var text = elem[0];
			return text.includes(pattern);
		}

		function search_second(elem, pattern) {
			var text = elem[1];
			return text.includes(pattern);
		}

		// Search for "service".
		pattern = 'service';
		output = [
			['delay_service', 'etwas Info'],
			['generator_service', 'nur zum Generieren']
		];
		expect(custom_keyword_search(input, pattern, search_first)).toEqual(output);
		expect(keyword_search(input, pattern, search_second)).toEqual([]);
		pattern = 'Service';
		expect(custom_keyword_search(input, pattern, search_first)).toEqual([]);
		expect(keyword_search(input, pattern, search_second)).toEqual([]);

		// Search for "Generieren".
		pattern = 'Generieren'
		output = [
			['generator_service', 'nur zum Generieren']
		];
		expect(custom_keyword_search(input, pattern, search_first)).toEqual([]);
		expect(custom_keyword_search(input, pattern, search_second)).toEqual(output);
		pattern = 'generieren';
		expect(custom_keyword_search(input, pattern, search_first)).toEqual([]);
		expect(keyword_search(input, pattern, search_second)).toEqual([]);

		// Test empty arrays and null values.
		expect(keyword_search([], pattern, search_first)).toEqual([]);
		expect(keyword_search(null, pattern, search_first)).toEqual([]);
		expect(keyword_search(input, "", search_first)).toEqual([]);
		expect(keyword_search(input, null, search_first)).toEqual([]);
		expect(keyword_search(input, pattern, null)).toEqual([]);
	});

	// Sort list of numbers or strings in alphabetical order.
	it('alphabetical_sort', function() {
		// Test with integer array.
		unsorted = [2, -13, 5, 0, 2, 18];
		sorted = [-13, 0, 2, 2, 5, 18];
		expect(alphabetical_sort(unsorted)).toEqual(sorted);

		// Test with float array.
		unsorted = [2.1, -13.75, 5.0, 0.0, 2.1, 18.1];
		sorted = [-13.75, 0.0, 2.1, 2.1, 5.0, 18.1];
		expect(alphabetical_sort(unsorted)).toEqual(sorted);

		// Test with mixed number array.
		unsorted = [2.3, -13, 5, -0.1, 2.3, 18];
		sorted = [-13, -0.1, 2.3, 2.3, 5, 18];
		expect(alphabetical_sort(unsorted)).toEqual(sorted);

		// Test with string array.
		unsorted = ['z', 'zb', 'za', 'c', 'z', 'az'];
		sorted = ['az', 'c', 'z', 'z', 'za', 'zb'];
		expect(alphabetical_sort(unsorted)).toEqual(sorted);

		// Test empty arrays and null values.
		expect(alphabetical_sort([])).toEqual([]);
		expect(alphabetical_sort(null)).toEqual([]);
	});

});

describe('string_formatting', function() {

	it('json_strings', function() {
		json_instance = {
			"service": ["image_adder"],
			"active": true
		};
		json_string = '{&quot;services&quot;:[&quot;image_adder&quot;],&quot;active&quot;:true}'
		expect(convert_to_json_string(json_instance)).toEqual(json_string);
	});

});
