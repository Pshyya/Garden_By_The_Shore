from pathlib import Path

import pygame

from Interface import WINDOW_SIZE, find_cinematic, play_cinematic, show_menu


def run_game(screen):
	clock = pygame.time.Clock()
	running = True

	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
				running = False

		screen.fill((180, 194, 164))
		title_font = pygame.font.SysFont("georgia", 44, bold=True)
		body_font = pygame.font.SysFont("georgia", 22)
		title = title_font.render("Le jardin s'eveille", True, (38, 58, 43))
		body = body_font.render("La scene de jeu peut maintenant etre ajoutee ici.", True, (56, 72, 57))
		screen.blit(title, title.get_rect(center=(WINDOW_SIZE[0] // 2, 290)))
		screen.blit(body, body.get_rect(center=(WINDOW_SIZE[0] // 2, 360)))
		pygame.display.flip()
		clock.tick(60)


def main():
	pygame.init()
	screen = pygame.display.set_mode(WINDOW_SIZE)
	pygame.display.set_caption("Garden By The Shore")

	try:
		if show_menu(screen):
			project_directory = Path(__file__).resolve().parent
			cinematic = find_cinematic(project_directory / "Videos")
			if play_cinematic(screen, cinematic):
				run_game(screen)
	finally:
		pygame.quit()


if __name__ == "__main__":
	main()
