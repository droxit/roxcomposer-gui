describe('search_and_sort', function() {

	// Default alphabetic sort.
	it('default_sort', function() {
		// Function to sort in reversed order.
		function reverse_sort(a, b) {
			if (a < b) {
				return 1;
			}
			if (a > b) {
				return -1;
			}
			return 0;
		}

		// Test with integer array.
		unsorted = [2, -13, 5, 0, 2, 18];
		sorted = [-13, 0, 2, 2, 5, 18];
		sorted_reversed = [18, 5, 2, 2, 0, -13];
		expect(alphabetical_sort(unsorted)).toEqual(sorted);
		expect(sort(unsorted, reverse_sort)).toEqual(sorted_reversed);

		// Test with float array.
		unsorted = [2.1, -13.75, 5.0, 0.0, 2.1, 18.1];
		sorted = [-13.75, 0.0, 2.1, 2.1, 5.0, 18.1];
		sorted_reversed = [18.1, 5.0, 2.1, 2.1, 0.0, -13.75];
		expect(alphabetical_sort(unsorted)).toEqual(sorted);
		expect(sort(unsorted, reverse_sort)).toEqual(sorted_reversed);

		// Test with mixed number array.
		unsorted = [2.3, -13, 5, -0.1, 2.3, 18];
		sorted = [-13, -0.1, 2.3, 2.3, 5, 18];
		sorted_reversed = [18, 5, 2.3, 2.3, -0.1, -13];
		expect(alphabetical_sort(unsorted)).toEqual(sorted);
		expect(sort(unsorted, reverse_sort)).toEqual(sorted_reversed);

		// Test with string array.
		unsorted = ['z', 'zb', 'za', 'c', 'z', 'az'];
		sorted = ['az', 'c', 'z', 'z', 'za', 'zb'];
		sorted_reversed = ['zb', 'za', 'z', 'z', 'c', 'az'];
		expect(alphabetical_sort(unsorted)).toEqual(sorted);
		expect(sort(unsorted, reverse_sort)).toEqual(sorted_reversed);

		// Test empty arrays and null values.
		expect(alphabetical_sort([])).toEqual([]);
		expect(alphabetical_sort(null)).toEqual([]);
		expect(sort([], reverse_sort)).toEqual([]);
		expect(sort(null, reverse_sort)).toEqual([]);
		expect(sort(unsorted, null)).toEqual([]);
	});

	// Custom sort.
	it('custom_sort', function() {
		// Create nested elements.
		var firstTuple = [-42, 13];
		var secondTuple = [2, -756];
		var thirdTuple = [135, 0];
		// Store them in array.
		unsorted = [secondTuple, thirdTuple, firstTuple];

		// Expected result after sorting according to first element.
		sorted = [firstTuple, secondTuple, thirdTuple];
		sorted_reversed = [thirdTuple, secondTuple, firstTuple];

		// Sort according to first element.
		function custom_sort_first_elem(a, b) {
			elemA = a[0];
			elemB = b[0];
			if (elemA < elemB) {
				return -1;
			}
			if (elemA > elemB) {
				return 1;
			}
			return 0;
		}
		expect(sort(unsorted, custom_sort_first_elem)).toEqual(sorted);

		// Sort according to first element in reversed order.
		function custom_reverse_sort_first_elem(a, b) {
			elemA = a[0];
			elemB = b[0];
			if (elemA < elemB) {
				return 1;
			}
			if (elemA > elemB) {
				return -1;
			}
			return 0;
		}
		expect(sort(unsorted, custom_reverse_sort_first_elem)).toEqual(sorted_reversed);

		// Expected result after sorting according to second element.
		sorted = [secondTuple, thirdTuple, firstTuple];
		sorted_reversed = [firstTuple, thirdTuple, secondTuple];

		// Sort according to second element.
		function custom_sort_second_elem(a, b) {
			elemA = a[1];
			elemB = b[1];
			if (elemA < elemB) {
				return -1;
			}
			if (elemA > elemB) {
				return 1;
			}
			return 0;
		}
		expect(sort(unsorted, custom_sort_second_elem)).toEqual(sorted);

		// Sort according to second element in reversed order.
		function custom_reverse_sort_second_elem(a, b) {
			elemA = a[1];
			elemB = b[1];
			if (elemA < elemB) {
				return 1;
			}
			if (elemA > elemB) {
				return -1;
			}
			return 0;
		}
		expect(sort(unsorted, custom_reverse_sort_second_elem)).toEqual(sorted_reversed);

		// Test empty arrays and null values.
		expect(sort([], custom_sort_first_elem)).toEqual([]);
		expect(sort(null, custom_sort_first_elem)).toEqual([]);
		expect(sort(unsorted, null)).toEqual([]);
	});

	// Default filter.
	it('default_filter', function() {
		input = ['Houston, wir haben ein Problem',
			'Ich bin zu alt für so eine Scheiße',
			'Ich liebe den Geruch von Napalm am Morgen',
			'Mein Name ist Bond. James Bond',
			'Ich mache ihm ein Angebot, das er nicht ablehnen kann'
		];

		// Filter Bond quote.
		pattern = 'Bond';
		output = ['Mein Name ist Bond. James Bond']
		expect(search(input, pattern)).toEqual(output);
		expect(search(input, 'bond')).toEqual([]);

		// Filter other quotes.
		pattern = 'Ich';
		output = ['Ich bin zu alt für so eine Scheiße',
			'Ich liebe den Geruch von Napalm am Morgen',
			'Ich mache ihm ein Angebot, das er nicht ablehnen kann'
		];
		expect(search(input, pattern)).toEqual(output);
		pattern = 'ich';
		output = ['Ich mache ihm ein Angebot, das er nicht ablehnen kann'];
		expect(search(input, pattern)).toEqual(output);

		// Test empty arrays and null values.
		expect(search([], pattern)).toEqual([]);
		expect(search(null, pattern)).toEqual([]);
		expect(search(input, "")).toEqual([]);
		expect(search(input, null)).toEqual([]);
	});

	// Custom filter.
	it('custom_filter', function() {
		// Function to filter elements which are too small.
		function too_small(a) {
			return a < 42;
		}

		// Function to filter elements which are too big.
		function too_big(a) {
			return a > 42;
		}

		// Create test array.
		input = [412, 56, 2, -11, 18.5, 29.37];
		output_too_small = [2, -11, 18.5, 29.37];
		output_too_big = [412, 56];

		// Run test.
		expect(custom_filter(input, too_small)).toEqual(output_too_small);
		expect(custom_filter(input, too_big)).toEqual(output_too_big);

		// Test empty arrays and null values.
		expect(custom_filter([], too_small)).toEqual([]);
		expect(custom_filter(null, too_small)).toEqual([]);
		expect(custom_filter(input, null)).toEqual([]);
	});

});
