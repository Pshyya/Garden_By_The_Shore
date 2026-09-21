from pathlib import Path

import pygame


INK = (49, 58, 49)
MUTED = (104, 100, 83)
PANEL = (246, 238, 220)
BACKGROUND = (231, 218, 193)
ACCENT = (113, 137, 104)
ACCENT_HOVER = (93, 119, 85)
SKIN_TONES = [(245, 205, 169), (222, 169, 125), (177, 117, 78)]
HAIR_COLORS = [(45, 31, 25), (116, 70, 39), (202, 164, 63)]
EYE_COLORS = [(57, 107, 112), (72, 95, 62), (68, 54, 43)]
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp"}
CATEGORY_ALIASES = {
	"Tete": ("tete", "tête", "head"),
	"Cheveux": ("cheveux", "hair"),
	"Yeux": ("yeux", "eyes"),
	"Nez": ("nez", "nose"),
	"Bouche": ("bouche", "mouth"),
}


def _font(size, bold=False):
	return pygame.font.SysFont("georgia", size, bold=bold)


def _text(surface, value, font, color, position, center=False):
	rendered = font.render(value, True, color)
	rectangle = rendered.get_rect(center=position) if center else rendered.get_rect(topleft=position)
	surface.blit(rendered, rectangle)


def _choice_button(surface, rectangle, label, selected, mouse_position):
	hovered = rectangle.collidepoint(mouse_position)
	color = ACCENT_HOVER if hovered else ACCENT if selected else (214, 204, 181)
	text_color = (255, 252, 242) if selected or hovered else INK
	pygame.draw.rect(surface, color, rectangle, border_radius=7)
	_text(surface, label, _font(18, bold=selected), text_color, rectangle.center, center=True)
	return hovered


def _load_image(path):
	try:
		return pygame.image.load(path).convert_alpha()
	except (pygame.error, OSError):
		return None


def _load_picture_assets(pictures_directory):
	pictures_directory = Path(pictures_directory)
	assets = {category: [] for category in CATEGORY_ALIASES}
	base_image = None
	if not pictures_directory.exists():
		return base_image, assets

	for path in sorted(pictures_directory.rglob("*")):
		if not path.is_file() or path.suffix.lower() not in IMAGE_EXTENSIONS:
			continue
		image = _load_image(path)
		if image is None:
			continue
		name = path.stem.lower()
		if name in {"mc", "personnage", "character", "base"}:
			base_image = image
			continue
		for category, aliases in CATEGORY_ALIASES.items():
			if path.parent.name.lower() in aliases or any(name.startswith(alias + "_") for alias in aliases):
				assets[category].append((path.stem, image))
				break
	return base_image, assets


def _scale_to_box(image, box_size):
	box_width, box_height = box_size
	image_width, image_height = image.get_size()
	scale = min(box_width / image_width, box_height / image_height)
	size = (max(1, int(image_width * scale)), max(1, int(image_height * scale)))
	return pygame.transform.smoothscale(image, size)


def _draw_picture_preview(surface, center, base_image, assets, appearance, category_keys):
	preview = pygame.Surface((300, 390), pygame.SRCALPHA)
	if base_image is not None:
		base = _scale_to_box(base_image, preview.get_size())
		preview.blit(base, base.get_rect(center=preview.get_rect().center))
	else:
		_draw_mc_fallback(preview, (150, 170), appearance)

	for category in CATEGORY_ALIASES:
		choices = assets[category]
		choice_index = appearance[category_keys[category]]
		if choices and choice_index < len(choices):
			layer = _scale_to_box(choices[choice_index][1], preview.get_size())
			preview.blit(layer, layer.get_rect(center=preview.get_rect().center))
	surface.blit(preview, preview.get_rect(center=center))


def _draw_mc_fallback(surface, center, appearance):
	center_x, center_y = center
	skin = SKIN_TONES[appearance["skin"]]
	hair = HAIR_COLORS[appearance["hair"]]
	eye = EYE_COLORS[appearance["eyes"]]

	pygame.draw.ellipse(surface, (205, 190, 163), (center_x - 120, center_y + 175, 240, 42))
	pygame.draw.rect(surface, ACCENT, (center_x - 78, center_y + 72, 156, 130), border_radius=42)
	pygame.draw.circle(surface, skin, (center_x, center_y), 78)
	pygame.draw.circle(surface, hair, (center_x, center_y - 48), 78)
	pygame.draw.rect(surface, hair, (center_x - 78, center_y - 48, 156, 40), border_radius=20)

	for eye_x in (center_x - 28, center_x + 28):
		pygame.draw.ellipse(surface, (255, 252, 242), (eye_x - 13, center_y - 8, 26, 18))
		pygame.draw.circle(surface, eye, (eye_x, center_y + 1), 7)

	pygame.draw.line(surface, (120, 76, 57), (center_x, center_y + 7), (center_x - 5, center_y + 26), 3)
	if appearance["mouth"] == 0:
		pygame.draw.arc(surface, (130, 67, 67), (center_x - 18, center_y + 22, 36, 25), 3.4, 6.0, 3)
	else:
		pygame.draw.line(surface, (130, 67, 67), (center_x - 13, center_y + 34), (center_x + 13, center_y + 34), 3)

	if appearance["hair"] == 1:
		pygame.draw.circle(surface, hair, (center_x - 62, center_y - 5), 24)
		pygame.draw.circle(surface, hair, (center_x + 62, center_y - 5), 24)


def _slide_to_custom(screen):
	clock = pygame.time.Clock()
	width, height = screen.get_size()
	for offset in range(0, width + 1, 64):
		screen.fill(BACKGROUND)
		pygame.draw.rect(screen, PANEL, (120 - offset, 75, width - 240, height - 150), border_radius=18)
		pygame.draw.rect(screen, PANEL, (width - offset, 0, width, height))
		_text(screen, "CUSTOM", _font(48, bold=True), INK, (width - offset + 70, 52))
		pygame.display.flip()
		clock.tick(60)


def show_custom(screen):
	"""Display the MC editor and return True to go back to the main menu."""
	clock = pygame.time.Clock()
	pictures_directory = Path(__file__).resolve().parent / "Pictures"
	base_image, assets = _load_picture_assets(pictures_directory)
	appearance = {"skin": 0, "hair": 0, "eyes": 0, "nose": 0, "mouth": 0}
	categories = ["Tete", "Cheveux", "Yeux", "Nez", "Bouche"]
	fallback_options = {"Tete": ["Clair", "Dore", "Brun"], "Cheveux": ["Noir", "Chatain", "Blond"], "Yeux": ["Bleu", "Vert", "Brun"], "Nez": ["Fin", "Droit", "Doux"], "Bouche": ["Sourire", "Neutre"]}
	category_keys = {"Tete": "skin", "Cheveux": "hair", "Yeux": "eyes", "Nez": "nose", "Bouche": "mouth"}
	active_category = 0
	back_button = pygame.Rect(55, 45, 135, 48)
	category_rectangles = [pygame.Rect(570, 125 + index * 55, 180, 42) for index in range(len(categories))]
	option_rectangles = []

	while True:
		mouse_position = pygame.mouse.get_pos()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				return False
			if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
				return True
			if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
				if back_button.collidepoint(event.pos):
					return True
				for index, rectangle in enumerate(category_rectangles):
					if rectangle.collidepoint(event.pos):
						active_category = index
				key = category_keys[categories[active_category]]
				for option_index, rectangle in enumerate(option_rectangles):
					if rectangle.collidepoint(event.pos):
						appearance[key] = option_index

			width, height = screen.get_size()
			screen.fill(BACKGROUND)
			pygame.draw.rect(screen, PANEL, (35, 25, width - 70, height - 50), border_radius=18)
			_text(screen, "CUSTOM", _font(42, bold=True), INK, (width // 2, 52), center=True)
			pygame.draw.line(screen, (198, 185, 157), (70, 92), (width - 70, 92), 2)
			_text(screen, "MC", _font(22, bold=True), MUTED, (325, 122), center=True)
			_text(screen, "Personnalise ton personnage principal", _font(18), MUTED, (325, 153), center=True)
			_draw_picture_preview(screen, (325, 325), base_image, assets, appearance, category_keys)

			category_rectangles = []
			for index, category in enumerate(categories):
				rectangle = pygame.Rect(570, 125 + index * 55, 180, 42)
				category_rectangles.append(rectangle)
				_choice_button(screen, rectangle, category, active_category == index, mouse_position)

			key = category_keys[categories[active_category]]
			option_rectangles = []
			_text(screen, categories[active_category], _font(25, bold=True), INK, (800, 125))
			category = categories[active_category]
			available_options = assets[category] or [(label, None) for label in fallback_options[category]]
			for index, option in enumerate(available_options):
				rectangle = pygame.Rect(800, 175 + index * 55, 245, 42)
				option_rectangles.append(rectangle)
				_choice_button(screen, rectangle, option[0], appearance[key] == index, mouse_position)

			_choice_button(screen, back_button, "Retour", False, mouse_position)
			pygame.display.flip()
			clock.tick(60)
