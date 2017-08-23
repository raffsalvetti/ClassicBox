-- update rom set binary_name = 'zedblade.zip' where id = 160;
select * from rom where emulator_id = 2 order by binary_name;

update rom set genre_id = 11 where emulator_id = 6

-- delete from rom where binary_name = 'fightfev.zip'
delete from rom where emulator_id = 2

-- insert into rom (emulator_id, name, binary_name, genre_id, max_players) 
-- values (6, 'Yar''s Revenge', 'Yar''s Revenge (1981) (Atari).zip', 2, 11)

select * from genre

-- 1  Shut em Up
-- 2  "Beat'em up"
-- 3  Fighting
-- 4  Maze
-- 5  Pinbal
-- 6  Plataform
-- 7  "Shoot'em up"
-- 8  Horror
-- 9  RPG
-- 10 Sport
-- 11 Other
-- 12 Puzzle

select * from emulator

-- update emulator set executable_full_path = 'D:\ClassicBox\emulator\mess0147b\mess.exe', base_arguments = 'snes -joystick -window -rompath D:\ClassicBox\rom\snes' where id = 2

-- update emulator set base_arguments = 'snes -joystick -window -rompath D:\ClassicBox\rom\snes -cart' where id = 2

select * from log_play_rom
