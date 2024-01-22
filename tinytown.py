import time
import random
import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import pygame as p
from ttres import *

p.init()

def load_pngs(images, folder, scale):
	pngs = {}
	for image in images:
		image_scale = scale
		image_name = image
		if image[1] == "-":
			image_scale = int(image.split("-")[0])*scale + BORDER_WIDTH*2*(int(image.split("-")[0])-1)
			image = image[2:]
		pngs[image_name] = p.transform.scale(p.image.load(f"{folder}/{image}.png"), (image_scale, image_scale))
	return pngs


def update_images():
	global IMAGES, IMAGE_LIST, SCALE, BORDER_WIDTH
	IMAGES = load_pngs(IMAGE_LIST, scale = SCALE - BORDER_WIDTH*2, folder="res")


def update_zoom():
	global ZOOM, SCALE, WIDTH, HEIGHT, font, large_font
	SCALE = int(32*ZOOM + 1)
	WIDTH = p.display.get_desktop_sizes()[0][0] // SCALE
	HEIGHT = p.display.get_desktop_sizes()[0][1] // SCALE
	update_images()
	font = p.font.SysFont(name="Arial", size=int(0.75*SCALE), bold=True)
	large_font = p.font.SysFont(name="Arial", size=int(1*SCALE), bold=True)


def set_tile_type(x, y, tile_type, roottile=None, affect_bal=True):
	global tiles, loop_iteration, bal
	old_tile = tiles[y][x]
	old_tile_type = old_tile["type"]
	if old_tile_type == tile_type:
		return
	if affect_bal:
		cost = get_price(x, y, {"type": "tile", "tiletype": tile_type})
		if cost:
			if cost >= bal:
				change_message(f"Not enough money! ({bal}/{cost})", "#ffaa88", 2)
				return
			bal -= cost
	if old_tile_type[1] == "-":
		tile_size = int(old_tile_type[0])
		for i in range(tile_size):
			for j in range(tile_size):
				if i == 0 and j == 0:
					continue
				set_tile_type(x+i, y+j, tile_type, affect_bal=True)
	tiles[y][x] = {"type": tile_type}
	if roottile:
		tiles[y][x]["roottile"] = roottile
	if tile_type.startswith("road-") or old_tile_type.startswith("road-"):
		connect_roads_near(x, y)


def draw_tile(x, y, tile_type):
	if tile_type == "none" or tile_type == "part":
		return
	screen.blit(IMAGES[tile_type], (x * SCALE + BORDER_WIDTH, y * SCALE + BORDER_WIDTH))


def draw_tiles(tiles, ofset_x, ofset_y):
	y_bound = 3 if ofset_y >= 3 else ofset_y
	x_bound = 3 if ofset_x >= 3 else ofset_x
	for y, row in enumerate(tiles[ofset_y - y_bound : ofset_y + HEIGHT + 1]):
		for x, tile in enumerate(row[ofset_x - x_bound : ofset_x + WIDTH + 1]):
			draw_tile(x-x_bound, y-y_bound, tile["type"])


def draw_ui_backgrounds():
	surf = p.Surface((SCALE*5, SCALE*3.5))
	surf.fill("#000000")
	surf.set_alpha(63)
	screen.blit(surf, (0, 0))


def draw_ui_score(score):
	score_text = large_font.render(str(score), False, "#ffffff")
	screen.blit(score_text, (1, -2))


def draw_ui_building_counts(res, com, ind):
	res_text = font.render(f"{res} (+{res_cpd})", False, "#ffaaaa")
	screen.blit(res_text, (1, 1.25*SCALE - 2))
	com_text = font.render(f"{com} (+{com_cpd})", False, "#bbbbff")
	screen.blit(com_text, (1, 2.0*SCALE - 2))
	ind_text = font.render(f"{ind} (+{ind_cpd})", False, "#ffdd88")
	screen.blit(ind_text, (1, 2.75*SCALE - 2))


def draw_ui_tool_cost(tool):
	price = get_price(*tile_hovered, tool)
	if price == None:
		return
	cost = f"Cost: {price}" if price >= 0 else f"Sell: +{-price}"
	cost_text = font.render(cost, False, "#bbbbbb")
	screen.blit(cost_text, (SCALE+3, p.display.get_window_size()[1] - SCALE*1.625 - 2))


def display_message(text, colour):
	msg_text = font.render(f"{text}", False, colour)
	screen.blit(msg_text, (SCALE*5, -2))


def draw_ui():
	draw_ui_backgrounds()
	draw_ui_score(bal)
	draw_ui_building_counts(res_count, com_count, ind_count)
	current_tool_tmp = current_tool
	if not current_tool_tmp or current_tool_tmp["type"] == "select" or current_tool_tmp["type"] == "part":
		current_tool_tmp = {"type": "tile", "tiletype": "grass"}
	draw_ui_tool_cost(current_tool_tmp)
	if message_endtime > loop_iteration:
		display_message(message_text, message_colour)


def get_price(x, y, tool):
	x, y = get_tile_at(x, y)
	old_tile_type = tiles[y][x]["type"]
	try:
		occupied_tiles = int(old_tile_type[0]) ** 2
	except:
		occupied_tiles = 1
	if old_tile_type == tool["tiletype"]:
		return None
	if old_tile_type.startswith("road-") and tool["tiletype"].startswith("road-"):
		if old_tile_type.split("-")[:2] == tool["tiletype"].split("-")[:2]:
			return None
	if tool["tiletype"] in TILE_TYPES:
		buy_price = TILE_TYPES[tool["tiletype"]][1] * occupied_tiles
	else:
		buy_price = BUILDINGS_LIST[tool["tiletype"]][1] * occupied_tiles
	if old_tile_type in TILE_TYPES:
		sell_price = int(TILE_TYPES[old_tile_type][1] * 0.8)
	else:
		sell_price = int(BUILDINGS_LIST[old_tile_type][1] * 0.8)
	
	return buy_price - sell_price
	


def gen_world(world_width, world_height):
	world = []
	for y in range(world_height+1):
		world.append([{"type":"grass"}] * (world_width+1))
	return world


def get_tile_at_mouse(x, y):
	tile_pos = [x // SCALE + ofset_x, y // SCALE + ofset_y]
	return get_tile_at(*tile_pos)


def get_tile_at(x, y):
	tile = [x, y]
	if x >= len(tiles[0]) or y >= len(tiles):
		return (0, 0)
	if tiles[tile[1]][tile[0]]["type"] == "part":
		tile = [
			x - tiles[tile[1]][tile[0]]["roottile"][0],
			y - tiles[tile[1]][tile[0]]["roottile"][1],
		]
	return tile



def handle_mousedowns():
	global has_lclicked, has_rclicked, has_mclicked
	if p.mouse.get_pressed()[0] and not has_lclicked:
		has_lclicked = True
		select_tile(*tile_hovered)
	if p.mouse.get_pressed()[2] and not has_rclicked:
		has_rclicked = True
		set_tile_type(*tile_hovered, "grass")
	if p.mouse.get_pressed()[1] and not has_mclicked:
		pick_block(*tile_hovered)
		has_mclicked = True


def handle_keydown(keys):
	global ofset_x, ofset_y, tiles, tile_selected
	global BORDER_WIDTH, IMAGES, SCALE, WIDTH, HEIGHT, ZOOM
	global paused, bal

	if keys[p.K_q]:
		if keys[p.K_LSHIFT]:
			global running
			running = False
		else:
			save()

	if keys[p.K_w]:
		if keys[p.K_LALT]:
			for i in range(4):
				ofset_up()
		ofset_up()

	if keys[p.K_s]:
		if keys[p.K_LALT]:
			for i in range(4):
				ofset_down()
		ofset_down()

	if keys[p.K_a]:
		if keys[p.K_LALT]:
			for i in range(4):
				ofset_left()
		ofset_left()

	if keys[p.K_d]:
		if keys[p.K_LALT]:
			for i in range(4):
				ofset_right()
		ofset_right()

	if keys[p.K_LCTRL] and keys[p.K_p]:
		paused = not paused

	if keys[p.K_RCTRL] and keys[p.K_EQUALS]:
		bal += 1_000
	
	if keys[p.K_RCTRL] and keys[p.K_MINUS]:
		bal -= 1_000

	for tile_type, key_matches in TILE_TYPES.items():
		matches_keys = True
		for key in key_matches[0]:
			if not keys[key]:
				matches_keys = False
				break
		if matches_keys:
			set_tool({
				"type": "tile",
				"tiletype": tile_type
			})
			break
		
	
	if keys[p.K_ESCAPE] or keys[p.K_0]:
		close_tool()

	if keys[p.K_b] and keys[p.K_LCTRL]:
		toggle_borders()

	if keys[p.K_i] and keys[p.K_LCTRL]:
		zoom_in()

	if keys[p.K_o] and keys[p.K_LCTRL]:
		zoom_out()


def ofset_right():
	global ofset_x, tiles
	ofset_x += 1
	if ofset_x + WIDTH >= len(tiles[0]):
		for i in range(len(tiles)):
			tiles[i].append({"type":"grass"})


def ofset_left():
	global ofset_x, tiles, tile_selected
	if ofset_x <= 0:
		ofset_x = 0
		for i in range(len(tiles)):
			tiles[i].insert(0, {"type":"grass"})
		if tile_selected:
			tile_selected[0] += 1
	else:
		ofset_x -= 1


def ofset_up():
	global ofset_y, tiles, tile_selected
	if ofset_y <= 0:
		ofset_y = 0
		tiles.insert(0, [{"type":"grass"}] * len(tiles[0]))
		if tile_selected:
			tile_selected[1] += 1
	else:
		ofset_y -= 1


def ofset_down():
	global ofset_y, tiles
	ofset_y += 1
	if ofset_y + HEIGHT >= len(tiles):
		tiles.append([{"type":"grass"}] * len(tiles[0]))


def close_tool():
	global tile_selected
	set_tool({"type":"select"})
	tile_selected = None


def toggle_borders():
	global BORDER_WIDTH
	BORDER_WIDTH = 0 if BORDER_WIDTH else 0.5
	update_images()


def zoom_in():
	global ZOOM
	if ZOOM >= 5.0:
		return
	ZOOM += 0.2
	update_zoom()


def zoom_out():
	global ZOOM
	if ZOOM <= 0.4:
		return
	ZOOM -= 0.2
	update_zoom()


def change_message(text, colour, duration_s):
	global message_text, message_colour, message_endtime
	message_text = text
	message_colour = colour
	message_endtime = loop_iteration + duration_s*FPS


def set_tool(tool):
	global current_tool, tile_selected
	current_tool = tool
	if tile_selected:
		use_tool(*tile_selected, tool)


def select_tile(x, y):
	global tile_selected
	global current_tool

	if tile_selected == [x, y]:
		tile_selected = None
	elif not current_tool or current_tool["type"] == "select":
		tile_selected = [x, y]
	else:
		use_tool(x, y, current_tool)


def use_tool(x, y, tool):
	global tile_selected, zones
	if tool["type"] == "tile":
		set_tile_type(x, y, tool["tiletype"])
		tile_selected = None
	


def draw_overlay(x, y, colour: tuple):
	x, y = get_tile_at(x, y)
	tile_type = tiles[y][x]["type"]
	size = int(tile_type[0]) if tile_type[1] == "-" else 1
	alpha = 255
	if isinstance(colour, tuple) and len(colour) > 3:
		alpha = colour[3]
		colour = colour[:3]
	s = p.Surface((
		size*SCALE + BORDER_WIDTH*2,
		size*SCALE + BORDER_WIDTH*2
	))
	s.set_alpha(alpha)
	s.fill(colour)
	screen.blit(
		s,
		((x - ofset_x) * SCALE - BORDER_WIDTH,
		(y - ofset_y) * SCALE - BORDER_WIDTH)
	)


# DEPRECATED
# 
# def draw_tile_overlays(overlays):
# 	for overlay in overlays:
# 		overlayed_tile = tiles[overlayed_tile[1]][overlayed_tile[0]]
# 		tile_size = tiles[overlayed_tile[1]][overlayed_tile[0]]["type"][0]
# 		try:
# 			tile_size = int(tile_size[0])
# 		except:
# 			tile_size = 1
# 		if overlay[0]:
# 			overlayed_tile = get_tile_at(*overlay[0])
# 			draw_overlay(
# 				overlayed_tile[0], overlayed_tile[1],
# 				overlay[1], 
# 				size=tile_size
# 			)


def pick_block(x, y):
	global tiles
	tile_type = tiles[y][x]["type"]
	if tile_type[1] == "-":
		tile_type = "zone-" + tile_type[2:]
	set_tool({
		"type": "tile",
		"tiletype": tile_type
	})


def develop_building_of_size(size):
	global tiles
	for y, row in enumerate(tiles):
		for x, tile in enumerate(row):
			if not tile["type"].startswith("zone-"):
				continue
			affected_tiles = []
			for i in range(size):
				for j in range(size):
					affected_tiles.append((y+i, x+j))
			possible_road_tiles = []
			for i in range(size+2):
				possible_road_tiles.append((x+i-1, y-1))
				possible_road_tiles.append((x+i-1, y+size))
			for i in range(size):
				possible_road_tiles.append((x-1, y+i))
				possible_road_tiles.append((x+size, y+i))
			contains_road = False
			for possible_road in possible_road_tiles:
				pr_type = tiles[possible_road[1]][possible_road[0]]["type"]
				if pr_type.startswith("path-") or pr_type.startswith("road-"):
					contains_road = True
					break
			if not contains_road:
				
				# ERROR: IndexError: list index out of range
				# tiles[affected_tile[1]][affected_tile[0]]["unconnected"] = True
				#	~~~~~^^^^^^^^^^^^^^^^^^
				#	IndexError: list index out of range

				# for affected_tile in affected_tiles:
				# 	tiles[affected_tile[1]][affected_tile[0]]["unconnected"] = True
				continue
			unique_nearby_tiles = {tile["type"]}
			for tile_pos in affected_tiles:
				unique_nearby_tiles.add(tiles[tile_pos[0]][tile_pos[1]]["type"])
			if len(unique_nearby_tiles) != 1:
				continue
			if (not tile["type"].endswith("low")) and (not tile["type"].endswith("mid")) and (not tile["type"].endswith("high")):
				tile["type"] += "-" + random.choice(["low", "mid", "high"])
			affected_tiles.remove((y, x))
			for tile_pos in affected_tiles:
				roottile = (tile_pos[1] - x, tile_pos[0] - y)
				set_tile_type(x=tile_pos[1], y=tile_pos[0], tile_type="part", roottile=roottile, affect_bal=False)
			tile["type"] = tile["type"][5:]
			tile_type = f"{size}-{tile['type']}"
			set_tile_type(x=x, y=y, tile_type=tile_type, affect_bal=False)
			return True
	return False


def develop_building():
	global tiles
	if develop_building_of_size(6) or develop_building_of_size(5) or develop_building_of_size(4) or develop_building_of_size(3) or develop_building_of_size(2) or develop_building_of_size(1):
		return True
	return False


def earn_taxes():
	global bal
	bal += res_cpd + com_cpd + ind_cpd


def remove_buildings(building_type, max_removals=100000000):
	total_removed = 0
	for y, row in enumerate(tiles):
		for x, tile in enumerate(row):
			if total_removed >= max_removals:
				return total_removed
			if building_type in tile["type"]:
				total_removed += 1
				set_tile_type(x, y, "grass")
	return total_removed


def building_is_in_surplus(building_type, allow_level):
	if building_type == "res":
		return res_count - allow_level > com_count or res_count - allow_level > ind_count*2
	if building_type == "com":
		return com_count - allow_level > res_count or com_count - allow_level > ind_count*2
	if building_type == "ind":
		return ind_count*2 - allow_level > res_count or ind_count*2 - allow_level > com_count
	return False


def building_is_in_demand(building_type, allow_level):
	# WARNING: this function is not completely tested and may not function as expected.
	# Use with caution.
	if building_type == "res":
		return res_count + allow_level < com_count or res_count + allow_level < ind_count*2
	if building_type == "com":
		return com_count + allow_level < res_count or com_count + allow_level < ind_count*2
	if building_type == "ind":
		return ind_count*2 + allow_level < res_count or ind_count*2 + allow_level < com_count
	return False


def update_abandonment():
	if building_is_in_surplus("res", 100):
		remove_buildings("-res-", 1)
		change_message("A residential building was abandoned", "#ffaa44", 4)
	if building_is_in_surplus("com", 100):
		remove_buildings("-com-", 1)
		change_message("A commercial building was abandoned", "#ffaa44", 4)
	if building_is_in_surplus("ind", 100):
		remove_buildings("-ind-", 1)
		change_message("An industrial building was abandoned", "#ffaa44", 4)


def update_building_count():
	global res_count, com_count, ind_count
	global res_cpd, com_cpd, ind_cpd
	res_count = com_count = ind_count = 0
	density_populations = {
		"low": 1,
		"mid": 3,
		"high": 5
	}
	for row in tiles:
		for tile in row:
			tile_type = tile["type"]
			if tile_type[1:8] == "-mixed-":
				res_count += int(tile_type[0])**2 * density_populations[tile_type[8:]] * 0.6 * 0.5
				com_count += int(tile_type[0])**2 * density_populations[tile_type[8:]] * 0.6 * 0.5
			if tile_type[1:6] == "-res-":
				res_count += int(tile_type[0])**2 * density_populations[tile_type[6:]] * 0.5
			if tile_type[1:6] == "-com-":
				com_count += int(tile_type[0])**2 * density_populations[tile_type[6:]] * 0.5
			if tile_type[1:6] == "-ind-":
				ind_count += int(tile_type[0])**2 * density_populations[tile_type[6:]] * 0.5
	res_cpd = int(res_count * TILE_TYPES["zone-res-low"][2] * 0.5)
	com_cpd = int(com_count * TILE_TYPES["zone-com-low"][2] * 0.5)
	ind_cpd = int(ind_count * TILE_TYPES["zone-com-low"][2] * 0.5)
	res_count = int(res_count)
	com_count = int(com_count)
	ind_count = int(ind_count)

	if building_is_in_demand("res", 50):
		change_message("Residential buildings are in demand", "#ffff22", 5)
	if building_is_in_demand("com", 50):
		change_message("Commercial buildings are in demand", "#ffff22", 5)
	if building_is_in_demand("ind", 50):
		change_message("Industrial buildings are in demand", "#ffff22", 5)


def connect_road(x, y):
	global tiles
	x, y = get_tile_at(x, y)
	if not tiles[y][x]["type"].startswith("road-"):
		return None
	rotation_mod = ""
	if tiles[y-1][x]["type"].startswith("road-"):
		rotation_mod += "n"
	if tiles[y+1][x]["type"].startswith("road-"):
		rotation_mod += "s"
	if tiles[y][x-1]["type"].startswith("road-"):
		rotation_mod += "w"
	if tiles[y][x+1]["type"].startswith("road-"):
		rotation_mod += "e"
	tile_type_list = tiles[y][x]["type"].split("-")
	tile_type_list[2] = rotation_mod
	tile_type = "-".join(tile_type_list)
	set_tile_type(x, y, tile_type)
	return rotation_mod


def connect_roads_near(x, y):
	connect_road(x, y)
	connect_road(x-1, y)
	connect_road(x, y-1)
	connect_road(x+1, y)
	connect_road(x, y+1)


def connect_all_roads():
	for y in range(len(tiles)):
		for x in range(len(tiles[0])):
			connect_road(x, y)


def save():
	data = {
		"ofset_x": ofset_x,
		"ofset_y": ofset_y,
		"tiles": tiles
	}
	with open("worlds/town.tt", "w") as f:
		f.write(f"""\
{bal}
{ofset_x}
{ofset_y}
{BORDER_WIDTH}
{str(tiles)}
""")


def load():
	global tiles
	global ofset_x, ofset_y
	global bal

	if (not os.path.exists("worlds/town.tt")):
		tiles = gen_world(WIDTH, HEIGHT)
		return


	with open("worlds/town.tt") as f:
		meta = f.readlines()
		bal = int(meta[0])
		ofset_x = int(meta[1])
		ofset_y = int(meta[2])
		BORDER_WIDTH = float(meta[3])
		tiles = list(eval(meta[4]))


ZOOM = 1
BORDER_WIDTH = 0.5
update_zoom()

FPS = 30

DEVELOP_BUILDING_DELAY = 6
AUTOSAVE_DELAY = 20


screen = p.display.set_mode((WIDTH*SCALE, HEIGHT*SCALE), p.FULLSCREEN)
p.display.set_caption("TinyTown 0.1")
clock = p.time.Clock()


running = True
loop_iteration = 1
tiles = gen_world(WIDTH, HEIGHT)

ofset_x = ofset_y = 0
tile_selected = tile_hovered = None
current_tool = None
has_lclicked = has_rclicked = had_mclicked = []
message_endtime = 0
paused = False

bal = 2_000
res_count = 0
com_count = 0
ind_count = 0

load()


update_building_count()
connect_all_roads()


while running:

	prev_tile_hovered = tile_hovered
	tile_hovered = get_tile_at_mouse(*p.mouse.get_pos())
	if tile_hovered != prev_tile_hovered:
		has_lclicked = has_rclicked = has_mclicked = False

	for event in p.event.get():
		if event.type == p.QUIT:
			running = False
		if event.type == p.KEYDOWN:
			handle_keydown(p.key.get_pressed())

	handle_mousedowns()
	
	if not loop_iteration % (FPS * DEVELOP_BUILDING_DELAY):
		develop_building()
		update_abandonment()
		update_building_count()
		earn_taxes()
	
	if not loop_iteration % (FPS * AUTOSAVE_DELAY) or loop_iteration == 1:
		save()

	screen.fill("#000000")
	if paused:
		screen.fill("#cc3300")

	draw_overlay(*tile_hovered, (255, 255, 255))
	if tile_selected:
		draw_overlay(*tile_selected, (255, 255, 127))

	if current_tool and current_tool["type"] != "select":
		draw_overlay(ofset_x, ofset_y+int(HEIGHT)-1, (255, 127, 255))
	draw_tiles(tiles, ofset_x, ofset_y)
	if current_tool and current_tool["type"] != "select":
		draw_tile(0, int(HEIGHT)-1, current_tool["tiletype"])
		draw_overlay(ofset_x, ofset_y+int(HEIGHT)-1, (255, 127, 255, 63))
	draw_ui()
	draw_overlay(*tile_hovered, (255, 255, 255, 31))
	if tile_selected:
		draw_overlay(*tile_selected, (255, 255, 127, 91))
	
	clock.tick(FPS)
	p.display.flip()
	p.display.update()

	if not paused:
		loop_iteration += 1


save()

p.quit()
quit()
