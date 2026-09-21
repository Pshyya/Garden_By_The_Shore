import pygame

from Interface import WINDOW_SIZE, show_menu
from Main_Character import show_story_selection


def run_game(screen, story_index):
	clock = pygame.time.Clock()
	running = True
	story_colors = [
		(174, 67, 67),
		(67, 112, 174),
		(74, 145, 93),
		(205, 169, 54),
		(132, 83, 165),
	]
	story_names = ["Histoire 1", "Histoire 2", "Histoire 3", "Histoire 4", "Histoire 5"]

	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
				running = False

		screen.fill(story_colors[story_index])
		title_font = pygame.font.SysFont("georgia", 44, bold=True)
		body_font = pygame.font.SysFont("georgia", 22)
		title = title_font.render(story_names[story_index], True, (255, 252, 242))
		body = body_font.render("Once upon a time...", True, (255, 252, 242))
		screen.blit(title, title.get_rect(center=(WINDOW_SIZE[0] // 2, 290)))
		screen.blit(body, body.get_rect(center=(WINDOW_SIZE[0] // 2, 360)))
		pygame.display.flip()
		clock.tick(60)


def main():
	pygame.init()
	screen = pygame.display.set_mode(WINDOW_SIZE)
	pygame.display.set_caption("Garden By The Shore")

	try:
		while True:
			menu_result = show_menu(screen)
			if menu_result != "start":
				break

			story_index = show_story_selection(screen)
			if story_index is False:
				break
			if story_index is not None:
				run_game(screen, story_index)
	finally:
		pygame.quit()


if __name__ == "__main__":
	main()
