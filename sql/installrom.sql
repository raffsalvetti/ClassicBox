INSERT INTO rom (name, binary_name, emulator_id, genre_id, year, max_players) 
VALUES (
	'Tiny Toon Adventures - Buster''s Hidden Treasure', 
	'Tiny Toon Adventures - Buster''s Hidden Treasure (U) [!].zip', 
	1, 
	(SELECT id FROM genre WHERE name = '2D Platformer'), 
	'1993',
	2);
