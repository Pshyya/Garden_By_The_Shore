from pathlib import Path

import pygame


WINDOW_SIZE = (1280, 720)
BACKGROUND = (231, 218, 193)
PANEL = (246, 238, 220)
INK = (49, 58, 49)
MUTED = (104, 100, 83)
ACCENT = (113, 137, 104)
ACCENT_HOVER = (93, 119, 85)


def _font(size, bold=False):
	return pygame.font.SysFont("georgia", size, bold=bold)


def _draw_centered_text(surface, text, font, color, center):
	rendered = font.render(text, True, color)
	surface.blit(rendered, rendered.get_rect(center=center))


def _button(surface, rectangle, label, mouse_position):
	hovered = rectangle.collidepoint(mouse_position)
	color = ACCENT_HOVER if hovered else ACCENT
	pygame.draw.rect(surface, color, rectangle, border_radius=8)
	_draw_centered_text(surface, label, _font(26, bold=True), (255, 252, 242), rectangle.center)
	return hovered


def show_menu(screen):
	"""Display the start menu and return start, custom, or quit."""
	clock = pygame.time.Clock()
	start_button = pygame.Rect(440, 375, 400, 62)
	custom_button = pygame.Rect(440, 455, 400, 62)
	quit_button = pygame.Rect(440, 535, 400, 50)

	while True:
		mouse_position = pygame.mouse.get_pos()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				return False
			if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
				return False
			if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
				if start_button.collidepoint(event.pos):
					return "start"
				if custom_button.collidepoint(event.pos):
					return "custom"
				if quit_button.collidepoint(event.pos):
					return False

		screen.fill(BACKGROUND)
		width, height = screen.get_size()
		pygame.draw.rect(screen, PANEL, (120, 75, width - 240, height - 150), border_radius=18)
		pygame.draw.line(screen, ACCENT, (280, 215), (1000, 215), 2)
		_draw_centered_text(screen, "GARDEN BY THE SHORE", _font(58, bold=True), INK, (width // 2, 150))
		_draw_centered_text(screen, "Une histoire commence au bord de l'eau", _font(24), MUTED, (width // 2, 260))
		_button(screen, start_button, "Entrer dans le jeu", mouse_position)
		_button(screen, custom_button, "Custom", mouse_position)
		_button(screen, quit_button, "Quitter", mouse_position)
		pygame.display.flip()
		clock.tick(60)


def find_cinematic(video_directory):
	video_directory = Path(video_directory)
	if not video_directory.exists():
		return None
	supported_extensions = {".mp4", ".mov", ".avi", ".mkv", ".webm"}
	videos = sorted(path for path in video_directory.iterdir() if path.suffix.lower() in supported_extensions)
	return videos[0] if videos else None


def play_cinematic(screen, video_path):
	"""Play the first video from Videos, or show a useful fallback message."""
	clock = pygame.time.Clock()
	try:
		import cv2
	except ImportError:
		cv2 = None

	if cv2 is None or video_path is None:
		message = "Ajoutez une video dans le dossier Videos pour voir la cinematique."
		return _show_cinematic_message(screen, clock, message)

	capture = cv2.VideoCapture(str(video_path))
	if not capture.isOpened():
		return _show_cinematic_message(screen, clock, "Impossible de lire la cinematique.")

	try:
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					return False
				if event.type == pygame.KEYDOWN and event.key in (pygame.K_ESCAPE, pygame.K_SPACE):
					return True

			success, frame = capture.read()
			if not success:
				return True

			frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
			frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
			frame_surface = _fit_surface(frame_surface, screen.get_size())
			screen.fill((18, 23, 19))
			screen.blit(frame_surface, frame_surface.get_rect(center=screen.get_rect().center))
			pygame.display.flip()
			clock.tick(30)
	finally:
		capture.release()


def _fit_surface(surface, size):
	target_width, target_height = size
	source_width, source_height = surface.get_size()
	scale = min(target_width / source_width, target_height / source_height)
	new_size = (int(source_width * scale), int(source_height * scale))
	return pygame.transform.smoothscale(surface, new_size)


def _show_cinematic_message(screen, clock, message):
	for _ in range(150):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				return False
			if event.type == pygame.KEYDOWN and event.key in (pygame.K_ESCAPE, pygame.K_SPACE):
				return True
		screen.fill((33, 43, 35))
		_draw_centered_text(screen, "CINEMATIQUE", _font(42, bold=True), (235, 226, 202), (640, 280))
		_draw_centered_text(screen, message, _font(22), (235, 226, 202), (640, 360))
		_draw_centered_text(screen, "Echap ou Espace pour continuer", _font(18), (181, 190, 167), (640, 470))
		pygame.display.flip()
		clock.tick(30)
	return True
