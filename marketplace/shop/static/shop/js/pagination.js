window.addEventListener("load", () => {
	let pageLink = $('a.page-link');

	pageLink.each((id, elem) => {
		let url = new URL(window.location.href);
		let params = new URLSearchParams(url.search);
		let href = '?';

		if(params.has('cats')) {
			let catParams = params.getAll('cats');
			if(catParams.length != 0) {
				for (let i=0; i<catParams.length; i++) {
					href += `cats=${catParams[i]}&`;
				}
			} else {
				href += `cats=${params.get('cats')}&`;
			}
		}
		if(params.has('search')) {
			href += `search=${params.get('search')}&`;
		}
		if(params.has('min')) {
			href += `min=${params.get('min')}&`;
		}
		if(params.has('max')) {
			href += `max=${params.get('max')}&`;
		}
		elem.href = href + `page=${elem.id}`;
	});
});