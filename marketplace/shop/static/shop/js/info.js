window.addEventListener('load', () => {

	const urlParams = new URLSearchParams(window.location.search);
	let openObjId = urlParams.get('op');
	if (openObjId !== null) {
		let accordingItems = $(`#inf${openObjId}`);


		let button = accordingItems.children('h2').children('.accordion-button');
		let collapse = accordingItems.children('.accordion-collapse');

		if (button.hasClass('collapsed')) {
			button.removeClass('collapsed');
			button['aria-expanded'] = true;
		}

		if (!collapse.hasClass('show')) {
			collapse.addClass('show');
		}
	}
});