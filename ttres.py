import pygame as p

TILE_TYPES = {
	"grass": [[p.K_l, p.K_1], 0, True],
	"water": [[p.K_l, p.K_2], 20, True],

	"path-stone": [[p.K_p, p.K_1], 10, True],
	"path-brick": [[p.K_p, p.K_2], 10, True],

	"road-street": [[p.K_r, p.K_1], 20, True],

	"redflowers": [[p.K_k, p.K_1], 20, True],

	"zone-mixed-low": [[p.K_z, p.K_2], 20, True],
	"zone-mixed-mid": [[p.K_z, p.K_3], 60, True],
	"zone-mixed-high": [[p.K_z, p.K_4], 140, True],

	"zone-res-low": [[p.K_x, p.K_2], 15, True],
	"zone-res-mid": [[p.K_x, p.K_3], 50, True],
	"zone-res-high": [[p.K_x, p.K_4], 120, True],

	"zone-com-low": [[p.K_c, p.K_2], 20, True],
	"zone-com-mid": [[p.K_c, p.K_3], 60, True],
	"zone-com-high": [[p.K_c, p.K_4], 140, True],

	"zone-ind-low": [[p.K_v, p.K_2], 18, True],
	"zone-ind-mid": [[p.K_v, p.K_3], 55, True],
	"zone-ind-high": [[p.K_v, p.K_4], 130, True],
}

BUILDINGS_LIST = {
	"mixed-low": [False, TILE_TYPES["zone-mixed-low"][1]*1],
	"mixed-mid": [False, TILE_TYPES["zone-mixed-mid"][1]*1],
	"mixed-high": [False, TILE_TYPES["zone-mixed-high"][1]*1],
	"res-low": [False, TILE_TYPES["zone-res-low"][1]*1],
	"res-mid": [False, TILE_TYPES["zone-res-mid"][1]*1],
	"res-high": [False, TILE_TYPES["zone-res-high"][1]*1],
	"com-low": [False, TILE_TYPES["zone-com-low"][1]*1],
	"com-mid": [False, TILE_TYPES["zone-com-mid"][1]*1],
	"com-high": [False, TILE_TYPES["zone-com-high"][1]*1],
	"ind-low": [False, TILE_TYPES["zone-ind-low"][1]*1],
	"ind-mid": [False, TILE_TYPES["zone-ind-mid"][1]*1],
	"ind-high": [False, TILE_TYPES["zone-ind-high"][1]*1],

	"1-mixed-low": [False, TILE_TYPES["zone-mixed-low"][1]*1],
	"1-mixed-mid": [False, TILE_TYPES["zone-mixed-mid"][1]*1],
	"1-mixed-high": [False, TILE_TYPES["zone-mixed-high"][1]*1],
	"1-res-low": [False, TILE_TYPES["zone-res-low"][1]*1],
	"1-res-mid": [False, TILE_TYPES["zone-res-mid"][1]*1],
	"1-res-high": [False, TILE_TYPES["zone-res-high"][1]*1],
	"1-com-low": [False, TILE_TYPES["zone-com-low"][1]*1],
	"1-com-mid": [False, TILE_TYPES["zone-com-mid"][1]*1],
	"1-com-high": [False, TILE_TYPES["zone-com-high"][1]*1],
	"1-ind-low": [False, TILE_TYPES["zone-ind-low"][1]*1],
	"1-ind-mid": [False, TILE_TYPES["zone-ind-mid"][1]*1],
	"1-ind-high": [False, TILE_TYPES["zone-ind-high"][1]*1],

	"2-mixed-low": [False, TILE_TYPES["zone-mixed-low"][1]*4],
	"2-mixed-mid": [False, TILE_TYPES["zone-mixed-mid"][1]*4],
	"2-mixed-high": [False, TILE_TYPES["zone-mixed-high"][1]*4],
	"2-res-low": [False, TILE_TYPES["zone-res-low"][1]*4],
	"2-res-mid": [False, TILE_TYPES["zone-res-mid"][1]*4],
	"2-res-high": [False, TILE_TYPES["zone-res-high"][1]*4],
	"2-com-low": [False, TILE_TYPES["zone-com-low"][1]*4],
	"2-com-mid": [False, TILE_TYPES["zone-com-mid"][1]*4],
	"2-com-high": [False, TILE_TYPES["zone-com-high"][1]*4],
	"2-ind-low": [False, TILE_TYPES["zone-ind-low"][1]*4],
	"2-ind-mid": [False, TILE_TYPES["zone-ind-mid"][1]*4],
	"2-ind-high": [False, TILE_TYPES["zone-ind-high"][1]*4],

	"3-mixed-low": [False, TILE_TYPES["zone-mixed-low"][1]*9],
	"3-mixed-mid": [False, TILE_TYPES["zone-mixed-mid"][1]*9],
	"3-mixed-high": [False, TILE_TYPES["zone-mixed-high"][1]*9],
	"3-res-low": [False, TILE_TYPES["zone-res-low"][1]*9],
	"3-res-mid": [False, TILE_TYPES["zone-res-mid"][1]*9],
	"3-res-high": [False, TILE_TYPES["zone-res-high"][1]*9],
	"3-com-low": [False, TILE_TYPES["zone-com-low"][1]*9],
	"3-com-mid": [False, TILE_TYPES["zone-com-mid"][1]*9],
	"3-com-high": [False, TILE_TYPES["zone-com-high"][1]*9],
	"3-ind-low": [False, TILE_TYPES["zone-ind-low"][1]*9],
	"3-ind-mid": [False, TILE_TYPES["zone-ind-mid"][1]*9],
	"3-ind-high": [False, TILE_TYPES["zone-ind-high"][1]*9],
}


IMAGE_LIST = [
	"none",
	"part",
	*TILE_TYPES.keys(),
	*BUILDINGS_LIST.keys()
]
