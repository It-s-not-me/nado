;(function () {
	const THEME_KEY = 'document-system-theme'
	const PROJECTOR_THEME = 'projector'

	function applyTheme(theme) {
		if (theme === PROJECTOR_THEME) {
			document.body.classList.add('projector-theme')
		} else {
			document.body.classList.remove('projector-theme')
		}
	}

	function updateButtonText(button) {
		if (document.body.classList.contains('projector-theme')) {
			button.textContent = 'Обычный стиль'
			button.title = 'Вернуть обычное оформление'
		} else {
			button.textContent = 'Контраст'
			button.title = 'Включить контрастное оформление для проектора'
		}
	}

	function createThemeButton() {
		const button = document.createElement('button')
		button.type = 'button'
		button.className = 'theme-toggle-button'

		updateButtonText(button)

		button.addEventListener('click', function () {
			const isProjectorTheme =
				document.body.classList.contains('projector-theme')

			if (isProjectorTheme) {
				localStorage.setItem(THEME_KEY, 'default')
				applyTheme('default')
			} else {
				localStorage.setItem(THEME_KEY, PROJECTOR_THEME)
				applyTheme(PROJECTOR_THEME)
			}

			updateButtonText(button)
		})

		document.body.appendChild(button)
	}

	document.addEventListener('DOMContentLoaded', function () {
		const savedTheme = localStorage.getItem(THEME_KEY)

		applyTheme(savedTheme)
		createThemeButton()
	})
})()
