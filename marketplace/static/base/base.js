$('nav.navbar').ready(() => {
	let viewCartBtnCount = $('nav div#viewCartBtnCount');
	let viewSavesBtnCount = $('nav div#viewSavesBtnCount');

	if(viewCartBtnCount.text() == 0) {
		viewCartBtnCount.css('display', 'none');
	} else {
		viewCartBtnCount.css('display', 'block');
	}
	if(+viewSavesBtnCount.text() == 0) {
		viewSavesBtnCount.css('display', 'none');
	} else {
		viewSavesBtnCount.css('display', 'block');
	}
});

window.addEventListener('load', (el) => {
	let toggleBtn = $('nav .product-btn');

	$('div#for-map').append(`<iframe style="width: 100%; height: 300px;" id="gmap_canvas" src="https://maps.google.com/maps?q=%D5%80%D5%A1%D5%B5%D6%84%D5%AB%20%D5%80%D6%80%D5%A1%D5%BA%D5%A1%D6%80%D5%A1%D5%AF%20/%20Hayk%20Square&t=&z=17&ie=UTF8&iwloc=&output=embed&language=hy" frameborder="0" scrolling="no" marginheight="0" marginwidth="0"></iframe>`);

	if(window.screen.width > 780){
		toggleBtn.each(function() {
			let el = $(this);
			let dropDownMenu = $(`ul#${el[0].id}`);
			
			$(this).hover(() => {
				dropDownMenu.addClass('show');
			}, () => {
				dropDownMenu.removeClass('show');
			});

			dropDownMenu.hover((el) => {
				dropDownMenu.addClass('show');
			}, (el) => {
				dropDownMenu.removeClass('show');
			});
		});
	} else {
		$("a.product-btn-for-mobile").click(() => {
			let el = $(this);
			let dropDownMenu = $(`ul#${el[0].id}`);
			
			$(this).hover(() => {
				dropDownMenu.addClass('show');
			}, () => {
				dropDownMenu.removeClass('show');
			});

			dropDownMenu.hover((el) => {
				dropDownMenu.addClass('show');
			}, (el) => {
				dropDownMenu.removeClass('show');
			});
		})
	}

	const params = new URLSearchParams(window.location.search);

	if(params.has('search')) {
		$('nav input.nav-input')[0].value = params.get('search');
	}
});