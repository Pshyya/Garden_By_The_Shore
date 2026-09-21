from pathlib import Path

import pygame


INK = (49, 58, 49)
MUTED = (104, 100, 83)
PANEL = (246, 238, 220)
BACKGROUND = (231, 218, 193)
ACCENT = (113, 137, 104)
SKIN_TONES = [(245, 205, 169), (222, 169, 125), (177, 117, 78)]
HAIR_COLORS = [(45, 31, 25), (116, 70, 39), (202, 164, 63)]
EYE_COLORS = [(57, 107, 112), (72, 95, 62), (68, 54, 43)]
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp"}


def _font(size, bold=False):
	return pygame.font.SysFont("georgia", size, bold=bold)


def _text(surface, value, font, color, position, center=False):
	rendered = font.render(value, True, color)
	rectangle = rendered.get_rect(center=position) if center else rendered.get_rect(topleft=position)
	surface.blit(rendered, rectangle)


def _load_image(path):
	try:
		return pygame.image.load(path).convert_alpha()
	except (pygame.error, OSError):
		return None


def _load_picture_assets(pictures_directory):
	pictures_directory = Path(pictures_directory)
	base_image = None
	if not pictures_directory.exists():
		return base_image

	for path in sorted(pictures_directory.rglob("*")):
		if not path.is_file() or path.suffix.lower() not in IMAGE_EXTENSIONS:
			continue
		image = _load_image(path)
		if image is None:
			continue
		name = path.stem.lower()
		if name in {"mc", "personnage", "character", "base"} or (
			path.parent == pictures_directory and "lily" in name
		):
			base_image = image
	return base_image


def _scale_to_box(image, box_size):
	box_width, box_height = box_size
	image_width, image_height = image.get_size()
	scale = min(box_width / image_width, box_height / image_height)
	size = (max(1, int(image_width * scale)), max(1, int(image_height * scale)))
	return pygame.transform.smoothscale(image, size)


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


def show_story_selection(screen):
	"""Display character selection and return the selected story index."""
	clock = pygame.time.Clock()
	pictures_directory = Path(__file__).resolve().parent / "Pictures"
	base_image = _load_picture_assets(pictures_directory)
	story_colors = [
		(174, 67, 67),
		(67, 112, 174),
		(74, 145, 93),
		(205, 169, 54),
		(132, 83, 165),
	]
	story_names = ["Name1", "Name2", "Name3", "Name4", "Name5"]

	while True:
		width, height = screen.get_size()
		button_width = 125
		button_height = 155
		button_gap = 20
		row_width = button_width * len(story_names) + button_gap * (len(story_names) - 1)
		row_left = (width - row_width) // 2
		story_rectangles = [
			pygame.Rect(row_left + index * (button_width + button_gap), 445, button_width, button_height)
			for index in range(len(story_names))
		]
		mouse_position = pygame.mouse.get_pos()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				return False
			if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
				return None
			if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
				for index, rectangle in enumerate(story_rectangles):
					if rectangle.collidepoint(event.pos):
						return index

		screen.fill(BACKGROUND)
		pygame.draw.rect(screen, PANEL, (35, 25, width - 70, height - 50), border_radius=18)
		_text(screen, "CHARACTERS", _font(42, bold=True), INK, (width // 2, 55), center=True)
		_text(screen, "Choose which story to play", _font(22), MUTED, (width // 2, 100), center=True)
		if base_image is not None:
			preview = _scale_to_box(base_image, (250, 315))
			screen.blit(preview, preview.get_rect(center=(width // 2, 265)))
		else:
			_draw_mc_fallback(screen, (width // 2, 190), {"skin": 0, "hair": 0, "eyes": 0, "mouth": 0})

		for index, rectangle in enumerate(story_rectangles):
			hovered = rectangle.collidepoint(mouse_position)
			color = tuple(min(255, channel + 25) for channel in story_colors[index]) if hovered else story_colors[index]
			pygame.draw.rect(screen, color, rectangle, border_radius=8)
			_text(screen, story_names[index], _font(17, bold=True), (255, 252, 242), rectangle.center, center=True)
			_text(screen, "Lily", _font(15), (255, 252, 242), (rectangle.centerx, rectangle.bottom - 25), center=True)

		pygame.display.flip()
		clock.tick(60)
