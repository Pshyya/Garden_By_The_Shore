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
	"""Display the start menu and return start or quit."""
	clock = pygame.time.Clock()
	start_button = pygame.Rect(440, 375, 400, 62)
	quit_button = pygame.Rect(440, 465, 400, 50)

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
				if quit_button.collidepoint(event.pos):
					return False

		screen.fill(BACKGROUND)
		width, height = screen.get_size()
		pygame.draw.rect(screen, PANEL, (120, 75, width - 240, height - 150), border_radius=18)
		pygame.draw.line(screen, ACCENT, (280, 215), (1000, 215), 2)
		_draw_centered_text(screen, "GARDEN BY THE SHORE", _font(58, bold=True), INK, (width // 2, 150))
		_draw_centered_text(screen, "Let's see what the shore has for us...", _font(24), MUTED, (width // 2, 260))
		_button(screen, start_button, "Enter the Game", mouse_position)
		_button(screen, quit_button, "Quit", mouse_position)
		pygame.display.flip()
		clock.tick(60)
