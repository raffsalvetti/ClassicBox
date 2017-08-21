use classicbox

-- ultimo jogo
select * from temp_game
order by id desc
limit 50;

select count(*) from temp_game

-- quantidade por plataforma
select platform, count(*) as qtd
from temp_game
group by platform
order by qtd desc;

-- jogos por plataforma
select *
from temp_game
where platform = 'GEN'
order by name;

-- todas as plataformas
select platform
from temp_game
group by platform
order by platform;

-- todos os generos
select genre
from temp_game
group by genre
order by genre;

-- todos os generos das plataformas mais conhecidas
select genre
from temp_game
where platform in ('SNES', 'GEN', 'NEO', 'SMS', '2600', 'N64', 'GC', 'GBC', 'GBA', 'GB')
group by genre
order by genre;

select * from temp_game
where name like '%Tiny Toon Adventures%'
and platform = 'GEN'
order by name

select * from temp_game
where platform in ('NEO')
and name like '%metal slug%'
order by name
