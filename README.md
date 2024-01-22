# Welcome to TinyTown!

In this game, your goal is to build a city where the population is happy.

Will you choose to make a nice, walkable city, or will you try to squeeze as much money out of your population as you can?

Be careful, though - if your citizens are unhappy or there is too little demand for a building type, buildings will be abandoned. You will lose the money you spent on it.

Have fun, and good luck building a beautiful city!

- Dylan, the developer

## Controls

Movement:

- Press the keys `WASD` to move around
- Hold the `alt` key and press `WASD` to move 5x faster

Graphics:

- Press `ctrl + i` to zoom in
- Press `ctrl + o` to zoom out
- Press `ctrl + b` to toggle showing borders

Placing tiles:

- To place a tile, you press a letter - representing a type - and a number - representing which item you want.
- You can find a list of the tile placement keys in the [tile keys](#tile-keys) section.

## Tile keys

There are a number of different keys you need to press to place various items.

When you have an item equipped, it will show in the bottom left hand corner.

## Zone tile keys

Mixed-use zoning (`z`):

- `z + 2` - low-density mixed-use zone (costs 30)
- `z + 3` - medium-density mixed-use zone (costs 110)
- `z + 4` - high-density mixed-use zone (costs 250)

Residential zoning (`x`):

- `x + 2` - low-density residential zone (costs 23)
- `x + 3` - medium-density residential zone (costs 92)
- `x + 4` - high-density residential zone (costs 230)

Commercial zoning (`c`):

- `c + 2` - low-density commercial zone (costs 27)
- `c + 3` - medium-density commercial zone (costs 100)
- `c + 4` - high-density commercial zone (costs 240)

Industrial zoning (`v`):

- `v + 2` - low-density industrial zone (costs 23)
- `v + 3` - medium-density industrial zone (costs 92)
- `v + 4` - high-density industrial zone (costs 230)

## Zone demand

Put simply:

- Your city should have an **equal** number of *residential* zones as *commercial* zones.
- You should have around **half** as many *industrial* zones as *commercial* zones.

For example, a balanced city may have:

- 500 residents
- 500 businesses
- 250 industries

### Abandonment requirements

A building will become abandoned if:

- There are over 100 more of that building type than there should be
- Its habitants are very unhappy

If a building is abandoned, it will be deleted from your city. Buildings will continue to be deleted until the building types are balanced ([as shown above](#zone-demand)).
