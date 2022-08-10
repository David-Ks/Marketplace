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